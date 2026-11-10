# TradeGlot

Tagline: A small seller's records become reviewed dispute evidence, sent to PayPal Sandbox only after a person approves.

**TL;DR**
- **One seller:** a small online seller who ships across borders.
- **One loss:** a buyer says the parcel never arrived. 48.00 USD is at stake.
- **One PayPal action:** TradeGlot builds the evidence from the seller's own records, and after one human approval of the reviewed draft plus a two-step send confirmation, sends it with PayPal's `provide-evidence` call.

**Verified, with files you can open**
- **Real sends:** six `provide-evidence` sends to author-created Sandbox test disputes (five local, one from the hosted demo); for two of them the file PayPal serves back has the same SHA-256 as the file recorded at send time.
- **Sourced rules:** 681 official export and import rules across ten countries and 140 PayPal clauses, each row linked to its source; 112 of the rules were sampled and 92 compared with their pages by an AI reader.
- **Tests and attacks:** the last recorded full run (2026-11-09, Run 1 in TEST_RUN_20261109_SKIPPED.md) passed 1,170 tests; the attack request matrix in the suite sends 1,727 hostile requests, with 0 broken in every run recorded in TEST_RUN_20261108.md.

**The PayPal main line**

List disputes → read one → one human approval of the reviewed draft plus a two-step send confirmation → provide evidence → PayPal-Debug-Id → read-back match.

1. **List disputes.** `GET /v1/customer/disputes` reads the seller's Sandbox disputes.
2. **Read one.** `GET /v1/customer/disputes/{id}` opens it. Reason and amount must match the local case, or the send stays locked.
3. **One approval, two-step confirmation.** The seller approves the reviewed evidence draft once. The send then needs a two-step confirmation: tick, Continue, a 3-second hold, Send.
4. **Provide evidence.** `POST /v1/customer/disputes/{id}/provide-evidence` goes out with a single-use server confirmation.
5. **PayPal-Debug-Id.** PayPal answers with its own id. Example from 2026-11-09: `ca5782cf8df90`.
6. **Read-back match.** A fresh read shows `WAITING_FOR_BUYER_RESPONSE`. The file PayPal serves back (2,015 bytes) has the same SHA-256 as the file recorded at send time.

Video (2:32): https://youtu.be/upx5eZYOmC0 · Repository (MIT): https://github.com/jiarong0423/payguard-ai · Proof page: https://payguard-demo-j2b3.onrender.com/proof.html

## What it proved against PayPal Sandbox

All Sandbox data was created by the author with Sandbox test accounts. Ids are masked.

- **Six evidence sends**, each to its own test dispute (item not received): from the local console on 2026-11-04, 2026-11-05 and three on 2026-11-09, after each of which a fresh read showed the dispute waiting for the buyer; and one from the public hosted demo on 2026-11-10, after which the fresh read showed it under review.
- **PayPal-Debug-Ids kept:** `f908765a01293` (2026-11-04), `f2088142a6218` with read-back `ca5554cf42ef6` (2026-11-05), `ca5782cf8df90` and `f492438834396` (2026-11-09), `f869050ae2a63` with read-back `f2530346edb95` (2026-11-10, hosted).
- **Byte match:** two of the three 2026-11-09 sends were compared, and both matched.
- **Wrong sends refused, nothing sent:** a dispute that already had seller evidence, disputes with a different reason, a dispute with a different amount (158.00 TWD against 48.00 USD), and a send after the 15-minute session expired.
- **Unsent invoice drafts** (status `DRAFT`, never sent) on 2026-10-06, 2026-10-31 and 2026-11-05.

Receipts: [RECEIPT_20261104_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261104_live.md), [RECEIPT_20261105_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261105_live.md), [RECEIPT_20261110_hosted_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261110_hosted_live.md), [READBACK_20261109.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/READBACK_20261109.md), [RECEIPT_20261031_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261031_live.md).

## Try it online

The [hosted demo](https://payguard-demo-j2b3.onrender.com) makes live PayPal Sandbox reads. It lists and opens the author's own Sandbox test disputes, with ids shown as masked codes. All visitors share a read budget of 20 a minute and 500 a day. Its evidence guide can call Gemini when the operator turns it on, at most 5 calls a minute and 20 a day across all visitors; past those caps, or without the opt-in, it answers from keyword rules. You can also make one real evidence send to a prepared Sandbox test dispute, with the same gate as the local console: one human approval of the reviewed draft plus a two-step send confirmation. The evidence is built from the demo's synthetic seller records (case-ref-001, item not received, 48.00 USD), and PayPal is read again before the send: only a dispute still waiting for the seller, with the same reason and amount, is sent. Each dispute takes one send and each visit one send, with at most 2 sends per address per day; all visitors together get at most 3 sends per 10 minutes and 15 a day (counted per server run, so a free-plan restart resets the count), from a pool of Sandbox test disputes the author opens. When no test dispute is left waiting for the seller, or the shared limit is used up, the page says so and opens the labelled recorded replay of an earlier send. The author made one such send on 2026-11-10 ([RECEIPT_20261110_hosted_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261110_hosted_live.md)). The test disputes opened that day are listed as due 11/30; new ones are planned around 11/25 to 11/28.

The first visit can take about a minute while the free Render server wakes.

**Three clicks:**
1. Open the [start page](https://payguard-demo-j2b3.onrender.com/start.html). Press **Run the step 1 example**. Expect "A rule may stop this sale.", each row linked to its source.
2. Select **Dispute evidence** (03) in the top stepper. Select a case. Press **Prepare evidence draft**, then **Download review ZIP** (7 entries: 6 files and the manifest).
3. Open **Proof**. Each claim shows how it was shown (real Sandbox call, recorded run, automated test or synthetic data), the date and the source file.

Offline copy: [demo package, 11 MB zip](https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip); its SHA-256 starts `442969a14a1b7a7e`.

## Why a seller needs this

A seller often notices a dispute, a policy warning or a sales spike only after the records are hard to collect. TradeGlot works on the seller's side, alongside PayPal's Resolution Center. It decides no case.

The three stages follow three published UK Financial Ombudsman decisions about PayPal accounts: [DRN-3621543](https://www.financial-ombudsman.org.uk/decision/DRN-3621543.pdf) (goods that needed PayPal pre-approval), [DRN-5706769](https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf) (a sharp sales rise, funds held and a 15% rolling reserve) and [DRN-3526295](https://www.financial-ombudsman.org.uk/decision/DRN-3526295.pdf) (an item-not-as-described claim, decided on the buyer's side).

## What it does

1. **After a dispute (main path):** reads the dispute, builds an Internal Review ZIP with personal details replaced by codes, previews the `provide-evidence` request, and sends only after one human approval of the reviewed draft plus a two-step send confirmation. A **Bryntum Scheduler** board shows each case's response window up to its due date.
2. **Before shipping:** a policy check against PayPal's published US Acceptable Use Policy, plus an optional ten-country rules check: 140 PayPal clauses and 681 official export and import rules (313 export, 368 import), each linked to its source. A ban found by the check stops the Sandbox invoice draft on the server (HTTP 409).
3. **When sales jump:** a synthetic burst of 50 orders, 500.00 USD, 5 times the declared baseline. **AG Charts** draws the hour; **AG Grid** lists the orders. It is a preparation signal, not a PayPal risk score.

## How the AI is kept in its lane

Rules and code run first. Gemini only maps a seller's sentence to closed form items. Code decides what is complete. In the guide stress test, 0 of 601 scored replies were outside the closed JSON format. No model can send, change a rule or decide a dispute.

A send passes nine checks, from "off by default" to an allow-listed call that keeps the PayPal-Debug-Id. The last recorded full run (2026-11-09, Run 1 in TEST_RUN_20261109_SKIPPED.md) passed 1,170 tests; the attack request matrix in the suite sends 1,727 hostile requests, with 0 broken in every run recorded in TEST_RUN_20261108.md. These are tests of the author's own build, not an outside audit.

## Sponsor tools

- **PayPal Sandbox API:** OAuth, invoice drafts, dispute list and detail, `provide-evidence`. PayPal's official MCP server ran once, read-only (`disputes.list`, `disputes.get`).
- **Bryntum Scheduler (Community):** evidence deadline board with a draggable "Collect evidence" bar.
- **AG Grid, AG Charts, AG Studio:** order grid, hourly chart, evidence dashboard. AG Studio's built-in agents ran live on the local console on 2026-11-04 (several runs, none saved), on 2026-11-08 (one run, recorded) and on 2026-11-09 (three runs, 11 tool calls, recorded); the hosted dashboard replays the recording dated 2026-11-09, with its four questions, and calls no model.
- **Render:** hosts the demo; a Workflow service deployed from this GitHub repository ran three times (started on demand from the Render dashboard, no schedule), 4 to 4.2 s each.
- **Gemini:** closed-option guide, evidence brief, Studio agent turns. The brief and the Studio agents run on the local console only; the hosted dashboard replays the recording dated 2026-11-09, with its four questions, and calls no model.
- **Postman:** 25-request run covering 21 of 37 operations, 82 assertions, 0 failed; the routes that reach PayPal or a model were not run. **APIMatic:** OpenAPI 3.1, 0 errors after fixes (first run 345).
- **Channel3:** product search for a reference card; 5 searches replayed, 5 more with receipts.
- **TradeGlot's own MCP server:** five read-only tools, local only.

Full table: [SPONSOR_TECH_MAP.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/SPONSOR_TECH_MAP.md).

## Scope

- **Sandbox only.** All PayPal calls are Sandbox. All disputes are author-created test cases between Sandbox test accounts. Orders, cases and evidence files are synthetic.
- **Acceptance is not a verdict.** "Accepted" means PayPal Sandbox recorded the request and the dispute left waiting for the seller: waiting for the buyer after the local sends, under review after the hosted send. It is not PayPal accepting the evidence or deciding the case.
- **Byte match covers two of six sends.** The first 2026-11-09 send was made before fingerprints were recorded. The 2026-11-04 send carried a 43-byte placeholder PDF.
- **The video's send.** The 2:32 video shows the hosted send of 2026-11-10, the sixth of the six, with its read-back and masked receipt (docs/evidence/RECEIPT_20261110_hosted_live.md); an earlier cut, since removed, showed a separate local send that has no receipt and is not counted.
- **Account match is declared.** The seller id is set by the operator and compared with the dispute's seller. It is not verified with PayPal.
- **Country rules are sampled.** 112 of 681 rules were sampled and 92 compared with their pages: 62 consistent, 30 worded differently, 0 contradicted, 20 could not be opened. An AI reader judged them, with no human re-read. The rest are unchecked. Advisory, not legal advice.
- **Pinned PayPal references are older** than PayPal's current pages (pinned 2022-10-29 and 2026-09-14).
- **Not run live yet:** shipment tracking and webhook signature checks (tests only). The evidence brief ran live once, on the local console.
- **No user study.** The guide numbers are measured on a fixed corpus; 328 of the 601 replies were pasted by hand.
- **Hosted limits:** shared read budget and send limits (counted per server run) and the free-plan wake-up delay; the hosted send was made live once (2026-11-10), and its stored file was not compared byte for byte.
- **Seller Protection** has conditions PayPal decides per transaction. TradeGlot shows no eligibility and predicts none.
- **Old name.** The project was called PayGuard AI when the receipts were made. The receipts, the Devpost address and the repository address still use that name.

## Built with

PayPal Sandbox REST APIs, FastAPI on Python 3.13, React, Tailwind, Vite, AG Grid, AG Charts, AG Studio, Bryntum Scheduler Community, Gemini (`gemini-3.8-flash`), Render, Postman, APIMatic, Channel3.
