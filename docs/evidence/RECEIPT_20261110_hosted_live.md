# TradeGlot hosted live Sandbox receipt, 2026-11-10 (masked)

Everything below is PayPal Sandbox test data created by the author with Sandbox test accounts. It is not a real merchant case. This is the first evidence send made from the public hosted demo rather than the local console. The dispute id is masked exactly as the hosted page showed it; the full id, any response body, e-mail address, token or secret are not kept here. Times are UTC+8.

## Setup
- Hosted demo on Render (`https://payguard-demo-j2b3.onrender.com`), deployed from commit `b50aa6d`, with `PAYGUARD_DEMO_MODE=public`, the read-only Sandbox switch and the hosted send switch on. Before the send, `GET /api/v1/connections` answered `sandbox_reads: true`, `sandbox_send: true` and a send state of 3 sends left in the 10-minute window, 15 left for the day and 0 disputes sent.
- On 2026-11-10 the author opened 8 new item-not-received test disputes of USD 48.00 each from a Sandbox buyer test account against the Sandbox seller test account. The hosted list showed their seller response due date as 11/30.
- The send was made by the author, in a browser, on the public hosted page (not the local console), and screen-recorded.

## Send: evidence from the hosted page (POST /v1/customer/disputes/{id}/provide-evidence through TradeGlot)
- About 13:46 on 2026-11-10: local demo case case-ref-001 (item not received, USD 48.00, synthetic seller records) paired with the Sandbox dispute shown as `PP-R-VAF-XXXX7877` (item not received, USD 48.00).
- Path on the page: Connect US Sandbox, open the dispute, Prepare evidence draft, the local review, the preview, then the two-step send dialog (tick, Continue, 3-second hold, Send).
- Result shown on the page: "SUBMITTED to PayPal Sandbox".
- PayPal-Debug-Id of the send: f869050ae2a63
- The page's read-back right after the send (GET /v1/customer/disputes/{id}): status "Under review".
- PayPal-Debug-Id of that read-back: f2530346edb95
- Afterwards the step 03 receipt line for the case read "Submitted to Sandbox (PP-R-...77)".

## Recording
The screen recording `take_20261110_1346_hosted_live_send.mov` is kept locally by the author and is not published.

## What this shows
- The public hosted demo can make a real Sandbox `provide-evidence` call through the same gates as the local console (a recorded local review of the draft, the single-use send confirmation, the account check against the configured seller id, the fresh PayPal read), with the hosted caps on.
- PayPal Sandbox accepted the request: it answered with its own Debug-Id, and the fresh read moved the dispute out of waiting for the seller.

## Limits to state
- One send, by the author, to an author-created Sandbox test dispute. It is not a real merchant case, and PayPal Sandbox accepting a request is not PayPal accepting the evidence or deciding the case.
- The read-back status was "Under review", not "Waiting for buyer response" as after the local sends; the reason for the difference is not known.
- A later read-back from the hosted site on 2026-11-11 showed this dispute as "Waiting for buyer response": PayPal Sandbox moved the case on after the evidence arrived. TradeGlot did not send anything else to it.
- The file PayPal stores was not downloaded and compared byte for byte for this send.
- The hosted send caps and the record of sent disputes live in server memory; a restart resets them.
- Risk: the stock of hosted test disputes was listed as due on 11/30, before the 12/1 to 12/15 judging window; the author plans to open new ones around 11/25 to 11/28.
- The 2:32 video shows the hosted send of 2026-11-10 (receipt in this file); an earlier cut, since removed, showed a separate local send that has no receipt and is not counted.
