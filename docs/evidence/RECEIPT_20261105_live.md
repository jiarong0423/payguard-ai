# PayGuard live Sandbox receipt, 2026-11-05 (masked)

Everything below is PayPal Sandbox test data created by the author with Sandbox test accounts. It is not a real merchant case. This is the second evidence send, made while recording the demo video, plus the refusals recorded right after it and an unsent invoice draft shown in the same recording. Identifiers are masked; no response body, e-mail address, token or secret is kept here. The receipt is dated in UTC+8; the events ran from 2026-11-04 16:58 UTC to 17:22 UTC.

## Setup
- The author paid one more Sandbox payment of USD 48.00 from a Sandbox buyer test account to the Sandbox seller test account and filed one item-not-received test dispute from the buyer side at 2026-11-04 16:58 UTC, marked as a Sandbox test in its text (PP-R-QIL-..., masked).
- The dispute first appeared in the seller-side list as UNDER_REVIEW; a few minutes later it read WAITING_FOR_SELLER_RESPONSE, and only then was it previewed.
- The local console ran with the evidence send switch on and the merchant id of the seller test account set.

## Send: evidence to the new item-not-received dispute (POST /v1/customer/disputes/{id}/provide-evidence through PayGuard)
- Local case case-ref-001 (item not received, USD 48.00) paired with PP-R-QIL-... (item not received, USD 48.00); the send dialog showed Case amount 48.00 USD and Dispute amount 48.00 USD; declared account check MATCH, compared with the configured merchant id and not verified with PayPal (sending account and dispute seller both TV...CP2C, masked).
- First attempt: the local demo session (15 minutes) had expired by the time the send was confirmed; the server refused it and nothing was sent. A read right after still showed WAITING_FOR_SELLER_RESPONSE and the seller's proof of fulfillment still REQUESTED_FROM_SELLER.
- After Reconnect, the draft, local review and preview were redone and the owner pressed the green Send; PayPal recorded the seller's evidence at 2026-11-04 17:16 UTC.
- result: Submitted to Sandbox, PayPal-Debug-Id f2088142a6218
- fresh read after the send (GET /v1/customer/disputes/{id}): status WAITING_FOR_BUYER_RESPONSE (before: WAITING_FOR_SELLER_RESPONSE), stage INQUIRY; evidence entries were the buyer's CREATE and PROOF_OF_FULFILLMENT SUBMITTED_BY_SELLER. PayPal-Debug-Id of that read: ca5554cf42ef6.
- The review ZIP downloaded in that session (14028 bytes, 7 entries: 6 listed files and the manifest) passed all 8 local checks; the 6 listed files matched the manifest sha256, size and CRC-32.

## Refusals recorded after the send (new session, case-ref-001 selected, nothing sent)
- PP-R-QIL-... again: the preview stayed locked with "Locked: PayPal already has seller evidence for this dispute."
- PP-R-BHF-... (unauthorized, chargeback) and PP-R-KTG-... (item not as described): refused with "This dispute does not match the selected case (reason or amount differ)."
- PP-R-OJX-... (item not received, TWD 158.00): refused with "The dispute amount in PayPal (158.00 TWD) differs from the selected case's amount (48.00 USD). Select the case it belongs to. Nothing was sent."

## Invoice draft recorded during the demo video (POST /v2/invoicing/invoices through PayGuard)
- Recorded during the demo video recording on 2026-11-05 (UTC+8); the frame at about 1:08 to 1:12 of the 2:50 video is the only record kept.
- What the frame shows: the PayPal Sandbox draft card marked Connected, "Connection evidence: Live Sandbox response · Verified from the creation response only", draft amount USD 10.00, the reminder that the draft has no shipping country and that the checked route (US to SG) is in the draft's private memo, and the line "Sandbox invoice draft created · INV2-...RG5U · Draft · not sent · Live Sandbox response · Verified from the creation response only · Not submitted".
- status: DRAFT, not sent to the buyer. The full invoice id and the response body are not kept.

## Limits to state
A second test send by the author between Sandbox test accounts, not a real merchant case. PayPal Sandbox accepted the request and the dispute moved to waiting for the buyer; this does not mean PayPal accepted the evidence or would decide the case for the seller.
