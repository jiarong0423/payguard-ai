# TradeGlot — Submitted Devpost Story

Project: TradeGlot

Tagline: Turns a seller's records into a reviewed dispute evidence package and, after one human approval, sends it to PayPal Sandbox. Policy and optional country checks come first.

Devpost: https://devpost.com/software/payguard-ai-zbsp9l

Repository: https://github.com/jiarong0423/payguard-ai

Video: https://youtu.be/_GORnHWShU4 (public, 2:50)

---

TradeGlot is an advisory tool translating cross-border policies for merchants before shipping and formatting seller records into human-approved PayPal dispute evidence.

*Translating international shipping rules and merchant records for PayPal dispute evidence.* Formerly called PayGuard AI (the name used in the video and the receipts). [Repository](https://github.com/jiarong0423/payguard-ai).

**A buyer says the parcel never arrived. TradeGlot turns the seller's order records into a reviewed evidence package, and after one person approves, sends it to the PayPal Sandbox dispute.** PayPal Sandbox accepted that request twice (2026-11-04 and 2026-11-05, UTC+8) and the dispute moved to waiting for the buyer.

**Rules first. AI only picks from closed options. One person's approval sends.**

Real PayPal Sandbox runs, with masked receipts: [2026-10-31](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261031_live.md) (OAuth, an unsent invoice draft, dispute list and detail reads), [2026-11-04](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261104_live.md) (evidence send, PayPal-Debug-Id `f908765a01293`, fresh read after it) and [2026-11-05](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261105_live.md) (second send, PayPal-Debug-Id `f2088142a6218`, readback `ca5554cf42ef6`, recorded during the video).

**Try it:** [hosted demo](https://payguard-demo-j2b3.onrender.com) (synthetic data, no PayPal calls) · [Proof page](https://payguard-demo-j2b3.onrender.com/proof.html) · [2:50 video](https://youtu.be/_GORnHWShU4) · [public repository](https://github.com/jiarong0423/payguard-ai) (MIT)

Try it in two minutes (hosted demo, synthetic data, no PayPal calls):
1. Policy pre-check: ship from **United States** to **Singapore**, tick **E-cigarettes**, select **Check country rules**. The result reads "This sale is likely to be stopped." (a cited PayPal, government or post rule matches; PayPal's own decision may differ).
2. Step 02: read the AG Charts spike and the records behind it.
3. Step 03: open the evidence deadline board and select **Download review ZIP**.
4. Open **Proof** in the top bar: each claim, how it was shown, the date and the source file.

## Why I built TradeGlot

A seller may notice a policy warning, a sudden sales spike, or a dispute only after the records have become difficult to assemble. TradeGlot helps a small seller check a sale before shipping and prepare the evidence if PayPal asks, while every decision stays with the seller and the payment provider. It works alongside PayPal's Resolution Center and seller protection and decides no case.

**Why these three situations:** the stages follow three published decisions of the UK Financial Ombudsman Service about PayPal accounts, checked against the published PDFs on 2026-10-31: [DRN-3621543](https://www.financial-ombudsman.org.uk/decision/DRN-3621543.pdf) (goods that needed pre-approval under the Acceptable Use Policy), [DRN-5706769](https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf) (a sharp rise in sales, funds held and a 15% rolling reserve) and [DRN-3526295](https://www.financial-ombudsman.org.uk/decision/DRN-3526295.pdf) (an item-not-as-described claim, decided on the buyer's side, which TradeGlot does not act for). They are UK decisions, not US cases, and three cases show a pattern, not an incidence rate.

## What it does

1. **Before an invoice draft: policy pre-check.** Deterministic checks compare the product description with pinned references to PayPal's published US Acceptable Use Policy; the seller can edit, cancel, or acknowledge the warning. An optional **ten-country rules check** answers from two layers, each row linked to its source: 140 clauses paraphrased from PayPal's legal hub pages for ten country profiles (a recorded spot-check on 2026-11-08 compared 24 of them with PayPal's pages: 14 consistent, 1 source page newer than its pinned date, 5 incomplete, 3 with a minor inconsistency, 1 not found; see [the record](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/PAYPAL_CLAUSES_SPOTCHECK_20261108.md); the other 116 are unchecked), and 681 official export and import rules (313 export, 368 import) from government pages and postal operators. Once a check has found a PayPal or government ban in the session, the server refuses the Sandbox invoice draft (HTTP 409), not only the button. A recorded spot-check on 2026-11-08 sampled 48 of the 681 rules and compared 44 with their official pages (34 consistent, 10 wording differs but meaning consistent, 0 inconsistent; 4 could not be opened); an earlier sample of 36 rules from two countries was compared on 2026-11-02 without a record file; the other rules are not checked line by line. The check is advisory, not legal advice, and PayPal's Acceptable Use Policy still applies. After review, the PayPal Sandbox path creates one **unsent** invoice draft.
2. **When sales jump.** A backend comparison flags a synthetic burst (50 orders, 500.00 USD, 5 times the declared local baseline). **AG Charts** draws the last hour against the review line, and **AG Grid** renders the order stream with sorting, filters, quick-filter search, custom cell renderers, value formatters, stable row ids and the Quartz theme; selecting an order shows its amount, currency and capture time. The card lists the records that back the signal and the ones still missing. It is a local preparation signal, not a PayPal risk score or a prediction of a hold.
3. **After a dispute: evidence preparation and a gated send.** Step 03 reads the seller's disputes (`GET /v1/customer/disputes`, `GET /v1/customer/disputes/{id}`), builds a pseudonymized, integrity-checked **Internal Review ZIP** (7 entries: 6 listed files and the manifest; the 6 listed files are re-hashed against it), and previews the multipart `provide-evidence` request. A person reviews the package; only then can the request be sent, through a two-step dialog that shows the case and the PayPal dispute side by side. A **Bryntum Scheduler** board shows each case's response window up to its due date.

An **AG Studio** evidence dashboard (`/dashboard.html`) shows the synthetic cases, their requested evidence and their time evidence. Its custom evidence auditor answers fixed questions with plain code; a question outside that set asks for confirmation first, then goes to Studio's built-in agents through a governed Gemini route with call caps (20 per session, an 8-turn stop). On 2026-11-04 the built-in agents ran live on my local console more than once. The first attempts failed (a 422 on an over-long tool description, then a 502; both fixed). One question then ran six agent turns, all HTTP 200. Before the data-agent change the reason-code question twice used all 20 calls without a summary; after it, the same question finished twice in 3 calls. On 2026-11-08 one question was recorded, and the hosted dashboard replays that recording, labelled as recorded, with no model call.

### Why the AI part drifts so little

Rules and code run first. The model only maps a seller's sentence to closed form items and a closed tag, and code, not the model, decides what is complete. Across the 601 scored replies, 0 of 601 were outside the closed JSON format (limit: 328 of the 601 were pasted by hand from a desktop session, and this is a fixed corpus, not a measure of decision accuracy). There were 0 confident-wrong fills in all v4 runs (limit: 268 form-guidance cases, not verdict correctness). A change only counts as an improvement if wrong values stay at 0. Evidence: [GUIDE_STRESS_TEST.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/GUIDE_STRESS_TEST.md), [GUIDE_BENCHMARK.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/GUIDE_BENCHMARK.md).

### Foolproofing you can see

Every action that writes to PayPal Sandbox, spends the Studio allowance or wipes the session asks first (`tests/frontend_foolproof_20261104.mjs`). A send needs a local review, a two-step dialog, a 3-second hold and a single-use server confirmation (`tests/frontend_send_confirm_r31.mjs`, `tests/frontend_send_guard_r25.mjs`, `tests/test_send_confirmation.py`). Locked buttons say why (`tests/frontend_lock_reasons_r31.mjs`). A send to a dispute whose reason or amount differs, or that already has seller evidence, is refused and nothing is sent ([RECEIPT_20261104_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261104_live.md), [RECEIPT_20261105_live.md](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RECEIPT_20261105_live.md)); the 15-minute demo session expiry refused a send in the recorded run (RECEIPT_20261105_live.md). These are guards that stop mistakes, not proof that PayPal accepts the evidence.

## Built and measured

Counted on the public repository on 2026-11-08 with `.venv/bin/python3 -B tools/verify_public_numbers.py` (no network):

- 350 tracked files. Python: 21,222 lines of backend, source and tools plus 17,626 lines of tests. Front end: 13,545 lines (21 JSX components, 5 pages). 37 API routes.
- 1,070 Python tests (9 skipped) passed in the author's last local run of this file set (recorded in `docs/evidence/TEST_RUN_20261108.md`; the earlier CI run covered 1,058), plus 46 Node contract and browser tests (6,775 lines) and a red-team request matrix of 1,727 requests (0 broken, 0 gaps); the test count and the matrix line are printed at the end of `./tools/run.sh test`.
- 39 Markdown files, about 71,709 words; 22 evidence files; 22 diagrams and images.
- Data: 140 PayPal clauses and 681 export and import rules for ten countries; a 268-case evidence-guide benchmark; 601 scored guide replies.
- Attack rounds r21 to r23 also ran on a real Android phone (86 sequences) and in a desktop browser (94 sequences), besides backend matrices of 143 and 119 cases.
- The public history had 46 commits on 2026-11-09 (the count grows with each push); the development history behind it had 261 commits over 12 working days (2026-10-08 to 2026-11-05). Only the public count can be reproduced (`git rev-list --count HEAD`); the development count is the author's own.

## Checks added on 2026-11-08

- [Answer-key evaluation](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/CHECKLIST_ANSWER_KEY_EVAL.md): 30 synthetic dispute cases. The key was written from PayPal's published reasons-and-evidence page before the program was run. The first run agreed on 22 of 30 (5 dangerous errors, all on author-logic cases). Three real gaps were then fixed (delivery before shipment, a future delivery date, a placeholder tracking number) and the same key, unchanged, now gives 25 of 30 and 2 dangerous errors (amount and currency are not inputs of that function). The key was drafted by the author and an AI. On 2026-11-09 a separate AI rater that had not seen the keys labelled all 50 cases (v1 and v2) from the written definitions: verdict agreement 47 of 50, kappa 0.903, three differences listed in [the record](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/SECOND_RATER_20261109.md). That is not an expert or third-party review.
- [Rules source spot-check](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RULES_SPOTCHECK_20261108.md): 48 of the 681 rules, drawn with a fixed seed, 44 of them compared with their official pages on 2026-11-08 (42 against the page text, 2 against a table of contents only): 34 consistent, 10 wording differs but meaning consistent, 0 inconsistent; 4 could not be opened. One pass by one reviewer.
- [Public real cases](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/REAL_CASES_PUBLIC_20261108.md): 15 further UK Financial Ombudsman decisions about PayPal sellers, summarised with sources. The most common gap was proof of delivery: a delivered tracking status, often with an address that matches the transaction (6 of 15; the cases are listed in the statistics section of that file). It is a small sample, skewed toward cases the seller had already lost.
- [Red-team record r30 to r37 and r48](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/RED_TEAM_ROUNDS_ADDENDUM_20261108.md) and [how every number was counted](https://github.com/jiarong0423/payguard-ai/blob/main/docs/evidence/HOW_NUMBERS_WERE_COUNTED.md).

## Proven against the PayPal Sandbox

All Sandbox data below was created by the author with Sandbox test accounts; it is not a real seller case. Identifiers are masked as in the receipts in `docs/evidence/`. Dates are UTC+8 unless marked UTC; receipts also give UTC.

- **2026-10-06 17:44 UTC:** OAuth client-credentials, then one unsent USD 10.00 invoice draft (`INV2-...-W5UW`, status `DRAFT`). A second unsent draft followed on 2026-10-31, and a third (`INV2-...RG5U`, `DRAFT`, not sent) during the video recording on 2026-11-05.
- **2026-10-31:** one author-filed test dispute (item not received) was listed 12.7 minutes after filing (a read at 2.4 minutes was empty) and read back in detail with HTTP 200 (`PP-R-...`, waiting for the seller's response).
- **2026-11-04:** evidence sent to a second test dispute (item not received, USD 48.00) after the local review and the two-step dialog. PayPal Sandbox accepted the request (PayPal-Debug-Id `f908765a01293`) and a fresh read showed `WAITING_FOR_BUYER_RESPONSE`. The evidence file sent was a 43-byte synthetic placeholder PDF.
- **2026-11-05 (UTC+8):** evidence sent to a newly filed test dispute of the same kind while the video was recorded (PayPal-Debug-Id `f2088142a6218`). The fresh read after the send (PayPal-Debug-Id `ca5554cf42ef6`) showed `WAITING_FOR_BUYER_RESPONSE` and the seller's proof of fulfillment as submitted. The review ZIP from that session (14028 bytes, 7 entries: 6 listed files and the manifest) passed all 8 local checks. The evidence file sent was again the 43-byte synthetic placeholder PDF.
- **Refusals, nothing sent:** a dispute that already had seller evidence ("Locked: PayPal already has seller evidence for this dispute."), disputes with a different reason (item not as described; unauthorized chargeback), and a dispute with a different amount (158.00 TWD against a 48.00 USD case). An attempt after the local session expired was also refused.

Sandbox acceptance means PayPal Sandbox recorded the request and moved the dispute to waiting for the buyer. It is not PayPal accepting the evidence or deciding the case for the seller.

## How I built it

The working stack is the PayPal Sandbox REST APIs and OAuth behind one reviewed gateway, FastAPI on Python 3.13, deterministic policy and country rules, React with Tailwind built by Vite, AG Grid, AG Charts and AG Studio, Bryntum Scheduler Community, and Gemini (`gemini-3.8-flash`) in a separate Python 3.12 worker. Rules run before AI, and fixed code keeps every decision: the policy findings, the country-rule stop, the sales-spike signal, the dispute checklist and the pinned citations. Every output stays advisory: a person reviews it, and nothing acts outside the app on its own.

Gemini only chooses among closed options. For the evidence brief it selects each sentence from a closed, pre-approved inventory for the stage, and the backend rejects anything outside the schema. In the evidence guide it maps a seller sentence to closed form items, and code never lets it mark evidence present; the guide ran live on 2026-11-02 (116 calls, 0 errors, an earlier prompt contract), on 2026-11-03 (36 calls, 0 errors) and on 2026-11-04 on my local console (five scenario sentences, 12 rounds each; four used the model and one was settled by the rule layer with no model call). No model has tool authority to change a rule, send an invoice, submit evidence or decide a dispute.

Sending evidence passes nine checks: off by default, a person approves a reviewed draft bound by digest, one case is bound to one dispute, a two-step confirm with a single-use server confirmation, the same payload as approved, a fresh read from PayPal, a declared account match, a re-check under a lock, and an allow-listed call that keeps the PayPal-Debug-Id as the receipt.

## Challenge and learning

The hard part was letting the app write to PayPal Sandbox without letting AI decide anything. Rules decide, AI only picks from closed options that code checks, and every send needs one person's approval. Every verdict stays with PayPal or the card issuer.

## Limits and access

- There was no user study; the guide's numbers are measured on a fixed corpus.
- Of the 681 rules, 48 were sampled and 44 compared with their pages (34 consistent, 10 wording differs; 2 of the 44 against a table of contents only), and 4 could not be opened; an earlier sample of 36 had no record file; the rest have not been checked line by line.
- In both Sandbox sends (2026-11-04 and 2026-11-05) the attached file was a 43-byte synthetic placeholder PDF; Sandbox acceptance is not a decision on the evidence.
- Shipment tracking and webhook signature checks are built and tested but have not been run against the Sandbox. The current Gemini evidence-brief contract was tested against fake models and has run live once, on 2026-11-09 on my local console; one run is not a benchmark.
- AG Studio's built-in agents ran live on my local console on 2026-11-04 (several runs, none saved) and again on 2026-11-08, when one question was recorded; the hosted dashboard replays that recording, labelled as recorded, with no model call.
- Pinned references are older than PayPal's pages: PayPal's US Acceptable Use Policy and User Agreement pages both show "Last updated on November 4, 2026" (read 2026-11-08); TradeGlot's pinned references are dated 2022-10-29 and 2026-09-14 and were not refreshed. The 18 pre-approval categories still match; the prohibited-list paraphrase is incomplete. A recorded spot-check of the PayPal clauses is in docs/evidence/PAYPAL_CLAUSES_SPOTCHECK_20261108.md.
- Seller Protection has conditions and exclusions and PayPal decides eligibility per transaction; TradeGlot shows no eligibility and predicts none.

This is a **US Sandbox demo with synthetic data** and author-created Sandbox test accounts. It gives the seller local preparation signals, not a PayPal risk score; PayPal decides policy and dispute matters, and a bank or card issuer decides an external dispute.

The [hosted demo](https://payguard-demo-j2b3.onrender.com) runs the synthetic stages, the country rules check, the review ZIP, the AG Studio dashboard and the [Proof page](https://payguard-demo-j2b3.onrender.com/proof.html), which lists each claim, how it was shown, the date and the source file. It makes no PayPal calls; its evidence guide can use Gemini only when the operator opts in (at most 5 calls a minute and 20 a day). It runs on Render's free plan, so the first load after an idle period can take about a minute. The Sandbox steps, the AI brief and the Studio agents need the local run (Testing instructions below). The first commit of the repository is dated 2026-10-08. The [2:50 video](https://youtu.be/_GORnHWShU4) shows the seller workflow.

## Turning on PayPal and Gemini (for judges running it)

The console and all three stages run in sample-data mode with no keys. Set these in the shell that starts the API (`./tools/run.sh api`):

- **PayPal Sandbox reads and drafts:** `PAYGUARD_PAYPAL_OUTBOUND=enabled`, plus `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` from your own PayPal Developer Sandbox app. Then select **Connect US Sandbox**; step 03 lists your Sandbox disputes with the badge **Sandbox**. Without credentials the connection answers `provider_disabled` and nothing is simulated.
- **Sandbox evidence send (optional):** also export `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, record the local review for the case, then use the send dialog (tick, orange **Continue**, 3-second hold, green **Send to PayPal**). Without the server's single-use confirmation a send gets 409 `confirmation_required` and nothing is sent. The console never sets the flag for you.
- **Gemini evidence brief:** `PAYGUARD_GEMINI_OUTBOUND=enabled` and `PAYGUARD_VERTEX_PROJECT=<your Google Cloud project id>`, signed in with Application Default Credentials (`gcloud auth application-default login`). It calls `gemini-3.8-flash` on Vertex AI (location `global`), billed to your project. Leave `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_GENAI_USE_ENTERPRISE`, `OPENAI_API_KEY`, `PAYGUARD_OPENAI_OUTBOUND` and `PAYGUARD_GEMINI_PYTHON_BIN` unset in that terminal, and use the same project for Application Default Credentials and `PAYGUARD_VERTEX_PROJECT`; otherwise the brief refuses with `ai_configuration_ambiguous`. Set up the separate Python 3.12 Gemini profile first (README, Run locally).
- **Gemini evidence guide (optional):** `PAYGUARD_GUIDE_MODEL=gemini` with the Vertex AI setup above, or `PAYGUARD_GEMINI_TRANSPORT=api_key` with an AI Studio `GEMINI_API_KEY` and no Vertex or outbound switch set (so the brief stays off in that terminal). It has its own call caps.

## What really calls PayPal (and what uses sample data)

TradeGlot calls the **PayPal Sandbox REST API** (`api-m.sandbox.paypal.com`) through one reviewed gateway with an allow-list of paths.

| Call | Endpoint | Real or sample |
|---|---|---|
| Seller connection | `POST /v1/oauth2/token` (client-credentials) | Real Sandbox call, 2026-10-06 and 2026-10-31, and for the reads, sends and the third draft on 2026-11-04 and 2026-11-05; needs `PAYGUARD_PAYPAL_OUTBOUND=enabled` and your Sandbox app credentials |
| Unsent invoice draft after the policy pre-check | `POST /v2/invoicing/invoices` | Real Sandbox call, 2026-10-06, 2026-10-31 and one during the video recording on 2026-11-05 (UTC+8); status `DRAFT`, never sent; refused by the server (HTTP 409) after a country-rules ban |
| Dispute list | `GET /v1/customer/disputes` | Real Sandbox read, 2026-10-31 (one author-created test dispute), and again around the sends on 2026-11-04 and 2026-11-05. Without a connection sample data in the same JSON shape is used, labelled **Sample** |
| Dispute detail | `GET /v1/customer/disputes/{id}` | Real Sandbox read, 2026-10-31 (HTTP 200), and the fresh reads after each send on 2026-11-04 and 2026-11-05 (readback PayPal-Debug-Id `ca5554cf42ef6` on 2026-11-05) |
| Evidence send | `POST /v1/customer/disputes/{id}/provide-evidence` | Real Sandbox send, 2026-11-04 and 2026-11-05 (UTC+8), each to its own author-created test dispute; PayPal Sandbox accepted the request and the dispute moved to waiting for the buyer (not a decision on the evidence). Sent only after the local review, `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, `submit: true` and the single-use confirmation; mismatched, already-answered and different-amount disputes are refused |
| Sales-spike orders, dispute checklist, evidence ZIP | local synthetic data | Sample data by design |

Shipment tracking and webhook signature checks are also built and tested, but have not yet been run against the Sandbox.

Masked receipts: `docs/evidence/RECEIPT_20261031_live.md`, `RECEIPT_20261104_live.md`, `RECEIPT_20261105_live.md`. Credentials never enter the repository, logs, browser or evidence files.

## Testing instructions (judges)

**Fastest path, no install:** open the [hosted demo](https://payguard-demo-j2b3.onrender.com) and use **Start here**: (1) in the country rules card ship from **United States** to **Singapore**, tick **E-cigarettes** and select **Check country rules**; the result reads "This sale is likely to be stopped." (PayPal's own decision may differ) and the server refuses the draft; untick it and check again for "No cited rule stops this sale." followed by "This is not clearance." (this shows the check reacts to the declared goods; declare what you actually sell); (2) in step 02, read the AG Charts spike and the records behind it; (3) in step 03, open the **Evidence deadline board** and select **Download review ZIP**; (4) open **Proof** in the top bar.

**Full local run** (Sandbox, AI brief, Studio agents). It needs Python 3.13 and uv, Node 20.19+ or 22.12+, and Python 3.12 for the Gemini profile (Windows: WSL 2):

```sh
git clone https://github.com/jiarong0423/payguard-ai
cd payguard-ai
python3.13 -m venv .venv
uv pip install --python .venv/bin/python3 -r requirements.lock
./tools/run.sh test        # runs the Python suite and prints the count
./tools/run.sh api         # API on http://127.0.0.1:8000
```

Second terminal:

```sh
cd frontend && npm ci --ignore-scripts --no-audit --no-fund && npm run dev   # open http://127.0.0.1:5183
```

(`./tools/run.sh start` instead builds the console and serves it on `http://127.0.0.1:8000`.)

What to look for: (1) the policy warning and the optional country check appear before any draft; (2) the AG Grid order stream sorts and filters the synthetic spike against the declared baseline; (3) the dispute checklist builds the Internal Review ZIP; with a Sandbox connection, step 03 lists your Sandbox disputes and previews the `provide-evidence` request. **Generate AI brief** shows "Gemini profile not configured" until the Gemini settings are present; `./tools/run.sh gemini-check` validates the profile without calling the model.

## Update log

- 2026-11-05: Dispute list and detail ran against a live Sandbox test dispute on 2026-10-31. The gated `provide-evidence` request was accepted by PayPal Sandbox for two author-created test disputes (2026-11-04 and 2026-11-05, UTC+8); already-answered, different-reason and different-amount test disputes were refused with nothing sent. Added the ten-country rules check, AG Charts, the AG Studio dashboard, the Bryntum deadline board, the hosted demo with its Proof page, and the new 2:50 video.
