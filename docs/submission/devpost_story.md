# TradeGlot (formerly PayGuard AI) — Submitted Devpost Story

Tagline: Turns a seller's records into a reviewed dispute evidence package and, after one human approval, sends it to PayPal Sandbox. Policy and optional country checks come first.

Devpost: https://devpost.com/software/payguard-ai-zbsp9l · Repository: https://github.com/jiarong0423/payguard-ai (MIT) · Video: https://youtu.be/_GORnHWShU4 (public, 2:50)

Naming note: the project was called PayGuard AI when the video and the receipts were made, so the video, the receipts, the Devpost address and the repository address still use the old name. [Download and click through on your computer](https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip) (11 MB zip; its file fingerprint (SHA-256) starts `442969a14a1b7a7e...` and the full value is on the start page).

---

Selling across borders means rules you only learn after an order is stopped. TradeGlot checks what you sell against PayPal's published policy and a curated set of rules for ten countries, each with its official source, before you ship. If a buyer later files a dispute, it organizes your own records into dispute evidence for a person to review. Code decides, the AI only picks from fixed options, a person approves every send, and PayPal makes every real decision.

**A buyer says the parcel never arrived. TradeGlot turns the seller's order records into a reviewed evidence package, and after one person approves, sends it to the PayPal Sandbox dispute.** PayPal Sandbox accepted that request five times (2026-11-04, 2026-11-05 and three times on 2026-11-09, UTC+8) and each dispute moved to waiting for the buyer. That is Sandbox acceptance, not a decision on the evidence.

**What makes it different:** one flow covers three moments, not only the dispute itself: a shipping and policy check before you send, a sales-spike review when orders jump, and evidence preparation when a buyer opens a dispute.

## Judge path: three clicks

Hosted demo, no sign-in, synthetic data plus read-only Sandbox reads. The first visit can take about a minute while the free server wakes. Button labels may be reworded before judging.

1. Open the [start page](https://payguard-demo-j2b3.onrender.com/start.html) (or the [demo](https://payguard-demo-j2b3.onrender.com)) and press **Run the step 1 example** in step 01. Expect "This sale is likely to be stopped.", each row linked to its source.
2. Open step 03, select a case, press **Prepare evidence draft**, then **Download review ZIP**.
3. Open **Proof** in the top bar ([proof.html](https://payguard-demo-j2b3.onrender.com/proof.html)): each claim, how it was shown (real Sandbox call, recorded run, automated test or synthetic data), the date and the source file.

## Sponsor tools at a glance

Full table with versions and file names: [SPONSOR_TECH_MAP.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/SPONSOR_TECH_MAP.md).

| Tool | What ran | Honest scope | Evidence |
| --- | --- | --- | --- |
| PayPal Sandbox API | PayPal login token, unsent invoice drafts, dispute list and detail reads, the gated `provide-evidence` send | Five sends to author-created test disputes; the hosted demo only reads, sends are local and shown as receipts | [2026-11-04](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261104_live.md), [2026-11-05](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261105_live.md), [2026-11-09 read-back](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/READBACK_20261109.md) |
| Our own MCP server (not PayPal's) | Five read-only tools over stdio: acceptable-use check, ten-country rules, clause search, sales-spike comparison | Runs on your computer only. It is TradeGlot's own server. PayPal's official MCP server was also run once, read-only, against the Sandbox (next row) | [MCP_SERVER.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/MCP_SERVER.md) |
| PayPal's official MCP server (`@paypal/mcp`) | `disputes.list` and `disputes.get` only | One read-only run on 2026-11-09: both calls succeeded; not part of the product path | [Run note](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/OFFICIAL_PAYPAL_MCP_RUN_20261109.md) |
| AG Grid, AG Charts, AG Studio | Grid of orders and cases, charts, an evidence dashboard with custom widgets and a custom evidence auditor | Community Grid and Charts; no AG Grid Enterprise features. Studio's built-in agents ran live on the local console only; one recorded run is replayed on the hosted page | [AG_GRID_USAGE.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/AG_GRID_USAGE.md), [AG_STUDIO_NOTES.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/AG_STUDIO_NOTES.md) |
| Bryntum Scheduler | Evidence deadline board, one row per case; the "Collect evidence" bar can be dragged under validators | Community tier only; hosted | [BRYNTUM_LICENSE_CHECK.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/BRYNTUM_LICENSE_CHECK.md) |
| Channel3 | Product search for the seller-confirmed reference card in the review ZIP; a category signal that never affects a decision | Five real searches replayed on the hosted demo; five more on 2026-11-09 with receipts, not replayed; live search is local only | [channel3_receipts_v1.json](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/channel3_receipts_v1.json), [channel3_receipts_20261109.json](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/channel3_receipts_20261109.json) |
| APIMatic | OpenAPI 3.1 description of the local console API (37 operations) validated; portal, SDKs and `llms.txt` generated locally | 0 errors after fixes (the first run found 345); nothing published, outputs not in the repository, no score exists or is claimed | [APIMATIC_RUN_20261109.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/APIMATIC_RUN_20261109.md) |
| Postman | Collection generated from the OpenAPI (37 requests), run with Newman | 10 of 37 requests run (read-only subset), 19 assertions, 0 failed; the other 27 not run; local console, not a Postman cloud monitor | [POSTMAN_RUN_20261109.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/POSTMAN_RUN_20261109.md) |
| Render | Free Docker web service from a Blueprint hosts the demo; a Render Workflow service with two checks was deployed from the repository | The Workflow was run once by hand on 2026-11-09 (4.2 s, receipt `ok:true`); not scheduled | [RENDER_WORKFLOW_RUN_20261109.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RENDER_WORKFLOW_RUN_20261109.md) |
| Gemini | Closed-option evidence guide, evidence brief, Studio agent turns, each behind code validation and call caps | Brief and Studio agents are local only; the hosted guide runs on keyword rules and uses Gemini only if the operator opts in (at most 5 calls a minute and 20 a day, then back to keywords). The current brief contract has one live run | [BRIEF_LIVE_RUN_20261109.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/BRIEF_LIVE_RUN_20261109.md), [GUIDE_BENCHMARK.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/GUIDE_BENCHMARK.md) |

## Why I built TradeGlot

A seller may notice a policy warning, a sudden sales spike, or a dispute only after the records have become difficult to assemble. TradeGlot helps a small seller check a sale before shipping and prepare the evidence if PayPal asks, while every decision stays with the seller and the payment provider. It works alongside PayPal's Resolution Center and seller protection and decides no case.

**Why these three situations:** the stages follow three published decisions of the UK Financial Ombudsman Service about PayPal accounts, checked against the published PDFs on 2026-10-31: [DRN-3621543](https://www.financial-ombudsman.org.uk/decision/DRN-3621543.pdf) (goods that needed pre-approval under the Acceptable Use Policy), [DRN-5706769](https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf) (a sharp rise in sales, funds held and a 15% rolling reserve) and [DRN-3526295](https://www.financial-ombudsman.org.uk/decision/DRN-3526295.pdf) (an item-not-as-described claim, decided on the buyer's side, which TradeGlot does not act for). They are UK decisions, not US cases, and three cases show a pattern, not an incidence rate. Fifteen more decisions are summarised in [REAL_CASES_PUBLIC_20261108.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/REAL_CASES_PUBLIC_20261108.md).

## What it does

1. **Before an invoice draft: policy pre-check.** Fixed code compares the product description with pinned references to PayPal's published US Acceptable Use Policy; the seller can edit, cancel, or acknowledge the warning. An optional **ten-country rules check** answers from 140 clauses paraphrased from PayPal's legal hub pages and 681 official export and import rules from government pages and postal operators, each row linked to its source. Once a check has found a PayPal or government ban, the server refuses the Sandbox invoice draft, not only the button. Only samples of these were compared with their sources, by an AI reader with no human re-read: see [PAYPAL_CLAUSES_SPOTCHECK_20261108.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/PAYPAL_CLAUSES_SPOTCHECK_20261108.md), [RULES_SPOTCHECK_20261108.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RULES_SPOTCHECK_20261108.md) and [RULES_SPOTCHECK_20261110.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RULES_SPOTCHECK_20261110.md). The check is advisory, not legal advice. After review, the Sandbox path creates one **unsent** invoice draft.
2. **When sales jump.** A backend comparison flags a synthetic burst (50 orders, 500.00 USD, 5 times the declared local baseline). **AG Charts** draws the last hour against the review line and **AG Grid** shows the order stream. The card lists the records that back the signal and the ones still missing. It is a local preparation signal, not a PayPal risk score or a prediction of a hold.
3. **After a dispute: evidence preparation and a gated send.** Step 03 reads the seller's disputes, builds a **Internal Review ZIP** with personal details replaced by codes and a fingerprint check (7 entries: 6 listed files and the manifest; [what each holds](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/REVIEW_ZIP_CONTENTS.md)), and previews the `provide-evidence` request. A person reviews the package; only then can the request be sent, through a two-step dialog that shows the case and the PayPal dispute side by side. A **Bryntum Scheduler** board shows each case's response window up to its due date.

An **AG Studio** dashboard (`/dashboard.html`) shows the synthetic cases and their time evidence. Its custom evidence auditor answers fixed questions with plain code; a question outside that set asks for confirmation first, then goes to Studio's built-in agents through a governed Gemini route with call caps. The hosted dashboard replays one recorded question, labelled as recorded, with no model call.

### Why the AI part drifts so little

Rules and code run first. The model only maps a seller's sentence to closed form items and a closed tag, and code, not the model, decides what is complete. A change only counts as an improvement if wrong values stay at 0. The measurements, with their limits stated first (part of the corpus was pasted by hand; it measures form guidance, not verdict accuracy), are in [GUIDE_STRESS_TEST.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/GUIDE_STRESS_TEST.md) and [GUIDE_BENCHMARK.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/GUIDE_BENCHMARK.md).

### Foolproofing you can see

Every action that writes to PayPal Sandbox, spends the Studio allowance or wipes the session asks first. A send needs a local review, a two-step dialog, a 3-second hold and a single-use server confirmation. A send to a dispute whose reason or amount differs, or that already has seller evidence, is refused and nothing is sent ([RECEIPT_20261104_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261104_live.md), [RECEIPT_20261105_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261105_live.md)). These are guards that stop mistakes, not proof that PayPal accepts the evidence. Attack and review rounds: [RED_TEAM_ROUNDS_20261104.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RED_TEAM_ROUNDS_20261104.md) and [the 11-08 addendum](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RED_TEAM_ROUNDS_ADDENDUM_20261108.md).

## Built and measured

Counts (files, lines, tests, API routes, rules, benchmark size) are printed by `.venv/bin/python3 -B tools/verify_public_numbers.py` (no network) and explained in [HOW_NUMBERS_WERE_COUNTED.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/HOW_NUMBERS_WERE_COUNTED.md). The last recorded local test run is [TEST_RUN_20261108.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/TEST_RUN_20261108.md); `./tools/run.sh test` prints the test count and the red-team request-matrix line. Other checks: the [answer-key evaluation](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/CHECKLIST_ANSWER_KEY_EVAL.md) of 30 synthetic dispute cases and the [second rater](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/SECOND_RATER_20261109.md) (an AI, not an expert or third-party review).

## Proven against the PayPal Sandbox

All Sandbox data was created by the author with Sandbox test accounts; it is not a real seller case. Identifiers are masked as in the receipts. Dates are UTC+8 unless marked UTC.

- **Connection and drafts:** A PayPal login token and unsent USD 10.00 invoice drafts (status `DRAFT`, never sent) on 2026-10-06 (UTC), 2026-10-31 and 2026-11-05 ([RECEIPT_20261031_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261031_live.md)).
- **Reads:** a test dispute (item not received) was listed and read back in detail with HTTP 200 on 2026-10-31.
- **Sends:** 2026-11-04 (PayPal's receipt number `f908765a01293`), 2026-11-05 (receipt number `f2088142a6218`, read-back `ca5554cf42ef6`, recorded during the video) and three on 2026-11-09. After each, a fresh read showed `WAITING_FOR_BUYER_RESPONSE`.
- **Refusals, nothing sent:** a dispute that already had seller evidence, disputes with a different reason, a dispute with a different amount, and an attempt after the local session expired.

Sandbox acceptance means PayPal Sandbox recorded the request and moved the dispute to waiting for the buyer. It is not PayPal accepting the evidence or deciding the case for the seller.

## How I built it

The working stack is the PayPal Sandbox REST APIs and login behind one reviewed gateway, FastAPI on Python 3.13, fixed-code policy and country rules, React with Tailwind built by Vite, AG Grid, AG Charts and AG Studio, Bryntum Scheduler Community, and Gemini (`gemini-3.8-flash`) in a separate Python 3.12 worker. Rules run before AI, and fixed code keeps every decision: the policy findings, the country-rule stop, the sales-spike signal, the dispute checklist and the pinned citations. Gemini only chooses among closed options, and the backend rejects anything outside the schema; no model has tool authority to change a rule, send an invoice, submit evidence or decide a dispute.

Sending evidence passes nine checks: off by default, a person approves a reviewed draft tied to its file fingerprint, one case is bound to one dispute, a two-step confirm with a single-use server confirmation, the same payload as approved, a fresh read from PayPal, a declared account match, a re-check under a lock, and an allow-listed call that keeps PayPal's receipt number (the PayPal-Debug-Id).

## Challenge and learning

The hard part was letting the app write to PayPal Sandbox without letting AI decide anything. Rules decide, AI only picks from closed options that code checks, and every send needs one person's approval. Every verdict stays with PayPal or the card issuer.

## Limits and access

This is a **US Sandbox demo with synthetic data** and author-created Sandbox test accounts; it gives the seller local preparation signals, not a PayPal risk score, and PayPal decides policy and dispute matters. There was no user study. Real PayPal calls are Sandbox only, and the hosted demo makes only read-only Sandbox reads (ids in the list are masked codes; every write route answers 503), so the sends can be checked only through the receipts. For one of the three sends of 2026-11-09 the stored file was not compared with the file recorded at send time, and a match for the other two does not mean PayPal accepted the evidence; the first two sends carried a 43-byte synthetic placeholder PDF. The country-rule and PayPal-clause checks are samples judged by an AI reader with no human re-read, some pages could not be opened, and the pinned PayPal policy references are older than PayPal's current pages, so the rest are not checked line by line (details in the spot-check files above). Shipment tracking and webhook signature checks are built and tested but have never run against the Sandbox; the evidence brief and the Studio agents ran live only on the local console, and one brief run is not a benchmark. Seller Protection has conditions and exclusions that PayPal decides per transaction; TradeGlot shows no eligibility and predicts none.

The [hosted demo](https://payguard-demo-j2b3.onrender.com) runs the synthetic stages, the country rules check, the review ZIP, the AG Studio dashboard and the [Proof page](https://payguard-demo-j2b3.onrender.com/proof.html). Its Sandbox reads are shared across visitors and capped (20 a minute, 500 a day). It runs on Render's free plan, so the first load after idle can take about a minute. The Sandbox writes (draft, evidence send, tracking), the AI brief and the Studio agents need the local run; keys, flags and commands are in the README (Run locally, Turning on PayPal, Turning on Gemini). Every call, real or sample, is listed in the README section "Real vs simulated".

## Update log

- Through 2026-11-09: five author-created test disputes accepted a gated `provide-evidence` request in total (2026-11-04, 2026-11-05, three on 2026-11-09); already-answered, different-reason and different-amount test disputes were refused with nothing sent. Added the ten-country rules check, AG Charts, the AG Studio dashboard, the Bryntum deadline board, the hosted demo with its Proof page and the 2:50 video.
