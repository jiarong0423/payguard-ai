# PayGuard live Sandbox receipt, 2026-11-04 (masked)

Everything below is PayPal Sandbox test data created by the author with Sandbox test accounts. It is not a real merchant case, and it proves only that PayGuard can send evidence to a Sandbox dispute and read the result back. Identifiers are masked; no response body, e-mail address, token or secret is kept here.

## Setup
- The author paid three Sandbox payments of USD 48.00 from a Sandbox buyer test account to the Sandbox seller test account, then filed three test disputes from the buyer side, each marked as a Sandbox test in its text: item not received (PP-R-WAH-..., masked), item not as described (PP-R-KTG-..., masked) and unauthorized (the filing page showed PP-R-RFH-...; the seller-side list later showed it as PP-R-BHF-..., masked).
- The local console ran with the evidence send switch on and the merchant id of the seller test account set; the browser sent the server-issued single-use confirmation from the send dialog.

## Flow 3: evidence sent to the item-not-received dispute (POST /v1/customer/disputes/{id}/provide-evidence through PayGuard)
- Local case case-ref-001 (item not received, USD 48.00) paired with PP-R-WAH-... (item not received, USD 48.00); declared account check MATCH, compared with the configured merchant id and not verified with PayPal (sending account and dispute seller both TV...CP2C, masked).
- Before the send: evidence draft prepared, review file 2328 bytes and review ZIP 14028 bytes downloaded, all 7 ZIP entries matched the manifest sha256, size and CRC-32, local draft review recorded at 2026-11-04T13:04:50Z.
- The send went out within the 5-minute local review window, after the tick, the orange Continue and the 3-second hold, on the green Send.
- result: external_send SUBMITTED, readback PROVIDE_EVIDENCE_SUBMITTED, PayPal-Debug-Id f908765a01293
- fresh read after the send (GET /v1/customer/disputes/{id}): status WAITING_FOR_BUYER_RESPONSE (before: WAITING_FOR_SELLER_RESPONSE), stage INQUIRY; evidence entries were the buyer's CREATE and PROOF_OF_FULFILLMENT SUBMITTED_BY_SELLER.
- The evidence file was a synthetic placeholder PDF (43 bytes) with one masked synthetic tracking row.

## Refusal: the item-not-as-described dispute
- Preview of PP-R-KTG-... with case-ref-001 selected: refused with "This dispute does not match the selected case (reason or amount differ)." The send stayed locked and no provide-evidence call was made for it.
- Later read of the unauthorized dispute PP-R-BHF-...: reason UNAUTHORISED, stage CHARGEBACK, PayPal requested proof of fulfillment, proof of refund and other evidence. Preview with case-ref-001 selected: refused with the same message; the send stayed locked and nothing was sent.

## Limits to state
One test send by the author between Sandbox test accounts, not a real merchant case. PayPal Sandbox accepted the request and the dispute moved to waiting for the buyer; this does not mean PayPal accepted the evidence or would decide the case for the seller. The unauthorized test dispute appeared in the seller-side list only later (about an hour after filing), so it was tested after the send.
