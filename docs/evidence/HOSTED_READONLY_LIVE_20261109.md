# Hosted demo, read-only Sandbox reads, live check, 2026-11-09

Checked by the author from a browser against the public hosted demo (Render, commit `b017f5d`), with the read-only Sandbox switch on and the author's own PayPal Sandbox test credentials stored as Render secrets (never shown here). Dispute ids are not reproduced in this file.

| Check | Result |
| --- | --- |
| `GET /api/v1/connections` | 200, `mode: hosted_demo`, `sandbox_reads: true` |
| `POST /api/v1/paypal/connect` (OAuth) | 200, status `connected`, environment `sandbox`, receipt action `OAUTH_CONNECT`, PayPal-Debug-Id `ca57912b83dab` |
| `GET /api/v1/paypal/disputes` | 200, source `paypal_sandbox`, evidence class `AUTHENTIC_SANDBOX_RESPONSE`, `provider_submission: NOT_PERFORMED`, readback `GET_LIST`, PayPal-Debug-Id `ca57913a83e52`, 8 disputes (author-created Sandbox test cases, USD 48.00 to 158.00) |
| the six write and provider routes (`invoices/draft`, `provide-evidence`, `add-tracking`, `webhooks/verify`, `ai/evidence-brief`, `studio/agent-turn`) | all 503 |

## What this shows
The hosted site really calls PayPal's Sandbox for reads (OAuth token and the dispute list), and every write route is refused. The PayPal-Debug-Ids are PayPal's own response identifiers for those two calls.

## Known gap found during this check, and the change made
The check above was made on commit `b017f5d`, whose list API returned the Sandbox dispute ids in full (test ids from the author's Sandbox account; no real payment, read-only, nothing can be sent), although the wording said they were masked. After this check the hosted wrapper was changed to return masked codes (for example `PP-R-XXX-XXXX1234`) and to keep the real id only in server memory; opening a case by its real id is refused. The change has unit tests and was not yet deployed or re-checked live when this file was written. An opened case still carries its Sandbox transaction id.

## Re-check after the masking change was deployed (commit `d10c0ed`, 2026-11-09)
Same checks, same browser method, after the hosted demo was redeployed from commit `d10c0ed`.

| Check | Result |
| --- | --- |
| `GET /api/v1/paypal/disputes` | 200, `AUTHENTIC_SANDBOX_RESPONSE`, 8 disputes, **0 full dispute ids**; each id is a masked code such as `PP-R-XXX-XXXX1234` |
| opening one case by its masked code | 200, the reply holds no full dispute id |
| opening a case by an unknown or a full id | 404 |
| the six write and provider routes | all 503 |

An opened case still carries its Sandbox transaction id (test data; read-only; nothing can be sent).
