# PayGuard live Sandbox receipt, 2026-10-31 (masked)

Everything below is PayPal Sandbox test data created by the author with two Sandbox test accounts. It is not a real merchant case, and it proves only that PayGuard can make and read Sandbox calls. Identifiers are masked; no response body, e-mail address, token or secret is kept here.

## Flow 1: policy preflight, then an unsent invoice draft (POST /v2/invoicing/invoices through PayGuard)
- status DRAFT, external_send FROZEN (not sent), environment sandbox
- evidence_class AUTHENTIC_SANDBOX_RESPONSE, proof_kind POST_RESPONSE_ONLY (the creation response only, no separate GET read-back)
- observed_at 2026-10-31T02:30:46Z, invoice id INV2-U3KH-...-PQCK (masked)

## Flow 2: sales burst
- synthetic orders, labelled Synthetic in the UI. There is no Sandbox source for this flow.

## Flow 3: dispute read-back (GET /v1/customer/disputes and GET /v1/customer/disputes/{id} through PayGuard)
- The author filed one test dispute (Item Not Received, TWD 158.00, text marked as a hackathon test) from a Sandbox buyer test account against the Sandbox seller test account.
- case created 2026-10-31T02:19:15Z, updated 02:22:43Z
- list reads: 01:57:xx and 02:02:xx UTC were made before the case existed (empty, no information); 02:21:38Z (2.4 minutes after creation) was empty; 02:31:59Z (12.7 minutes after creation) listed the case. One sample only: no official delay figure is claimed.
- list row: source paypal_sandbox, label "Sandbox data", evidence_class AUTHENTIC_SANDBOX_RESPONSE, provider_submission NOT_PERFORMED, dispute_id PP-R-OJX-... (masked), reason MERCHANDISE_OR_SERVICE_NOT_RECEIVED, status WAITING_FOR_SELLER_RESPONSE, stage INQUIRY, state REQUIRED_ACTION, seller_response_due_date 2026-11-20
- single read at 02:39:53Z (HTTP 200): the disputed transaction was HELD; evidence entries were the buyer's CREATE and a PROOF_OF_FULFILLMENT request to the seller.
- No provide-evidence call was made. The submit button stayed disabled (flag off).

## Limits to state
One test dispute made by the author between two Sandbox accounts, not a real merchant case. First live read of a non-empty list. The submission path is covered by mocked-transport tests only.
