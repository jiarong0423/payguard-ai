# PayGuard US Official Source Register

Status: current public-reference register for the US-only profile. Review date: 2026-10-06 UTC. This document records reviewed public facts and limitations; it is not legal advice or account-specific policy certification.

## Date rule

For PayPal pages, `Visible date` is the page's displayed `Last updated` value observed during the review. It is not a complete effective interval. For court records, the date is the filing date printed on the official order. Retrieval time, visible update date, effective date, filing date and response deadline remain separate fields.

## PayPal Developer and Sandbox sources

| Source ID | Official source | Visible date | Allowed claim | Required limitation |
| --- | --- | --- | --- | --- |
| `PP-DEV-REST-GET-STARTED` | https://developer.paypal.com/api/get-started/ | 2026-06-17 | A PayPal Developer account can test US integrations; REST authentication uses OAuth 2.0; default test roles include a Personal sandbox buyer and Business sandbox seller. | Does not prove this operator's Dashboard access, seller country, app state, entitlement or production eligibility. |
| `PP-DEV-SANDBOX-OVERVIEW` | https://developer.paypal.com/sandbox-testing/overview/ | 2026-07-30 | Sandbox is a self-contained virtual environment using fictitious accounts and Sandbox endpoints without touching live accounts. An existing PayPal login may be used for Developer access. | Does not change the live account type or prove production behavior. |
| `PP-DEV-SANDBOX-ACCOUNTS` | https://developer.paypal.com/sandbox-testing/accounts | 2026-07-24 | Personal sandbox accounts represent customers; Business sandbox accounts represent merchants; additional test accounts can be assigned a selected country. | A Business sandbox account is not a live Business account. The selected seller's country remains unconfirmed until read back. |
| `PP-DEV-INVOICING` | https://developer.paypal.com/api/invoicing | 2026-09-03 | Invoicing lists a Business account with Invoicing enabled and Sandbox credentials as prerequisites. Create and send are separate operations; a newly created invoice is a DRAFT. | Does not prove entitlement for the selected seller. Send, payment, reminder, refund and production remain out of scope. |

## PayPal US policy sources

| Source ID | Official source | Visible date | Allowed claim | Required limitation |
| --- | --- | --- | --- | --- |
| `PP-US-AUP` | https://www.paypal.com/us/legalhub/paypal/acceptableuse-full?country.x=US&locale.x=en_US | 2022-10-29 | The public AUP separates prohibited activity from activity requiring prior approval; the approval table is non-exhaustive. | A keyword/category match is not an account-specific violation. A no-match is not clearance. Approval status is unknown unless PayPal confirms it. |
| `PP-US-UA` | https://www.paypal.com/us/legalhub/paypal/useragreement-full?country.x=US&locale.x=en_US | 2026-09-14 | The agreement applies to US PayPal accounts and publishes terms for account types, holds, limitations and reserves, including several risk examples. | Does not prove the operator has a US account, reveal proprietary thresholds or predict any provider action or release. |
| `PP-US-PURCHASE-PROTECTION` | https://www.paypal.com/us/legalhub/paypal/buyer-protection?country.x=US&locale.x=en_US | 2026-01-26 | Purchase Protection may cover eligible INR and SNAD claims; counterfeit goods may qualify as SNAD; PayPal decides eligibility. | Does not require photos in every case or guarantee a buyer outcome. |
| `PP-US-SELLER-PROTECTION` | https://www.paypal.com/us/legalhub/paypal/seller-protection?country.x=US&locale.x=en_US | 2026-01-26 | Seller Protection may apply to eligible PayPal-hosted Unauthorized Transaction and INR claims when requirements are met; proof-of-shipment and delivery fields matter. | SNAD is ineligible. Tracking does not guarantee eligibility, victory, release or limitation removal. |

## Dispute process and evidence sources

| Source ID | Official source | Visible date | Allowed claim | Required limitation |
| --- | --- | --- | --- | --- |
| `PP-DISPUTES-OVERVIEW` | https://developer.paypal.com/disputes/overview | 2026-06-11 | Internal disputes allow buyer/merchant communication before escalation; PayPal adjudicates internal claims; a bank/card issuer adjudicates external disputes with PayPal as intermediary. | The actual case response determines current route and stage. |
| `PP-DISPUTES-API` | https://developer.paypal.com/api/disputes/ | 2026-07-21 | Dispute details expose reason, status, lifecycle stage, requested evidence, source, seller due date, allowed options and HATEOAS links. | Documentation does not authorize PayGuard to submit, accept, refund or infer an unavailable action. |
| `PP-DISPUTE-REASONS-EVIDENCE` | https://developer.paypal.com/disputes/reasons-evidence/ | 2026-06-05 | Requested evidence varies by reason and `evidence_type`; the actual response controls the checklist. | A generic checklist cannot replace the live request; completeness is not sufficiency. |
| `PP-DISPUTE-FILES` | https://developer.paypal.com/platforms/disputes/reference/supported-file-types-sizes/ | 2026-05-15 | Evidence supports JPG, JPEG, GIF, PNG and PDF; each file is under 10 MB and a call supports up to 50 MB total. | This is a future upload contract. It does not make photos mandatory or authorize an upload. |
| `PP-DISPUTES-SETUP` | https://developer.paypal.com/disputes/set-up/ | 2026-06-26 | A sandbox dispute uses a Personal sandbox account to create the dispute and a Business sandbox account to handle it. | Does not prove app scopes or create a transaction. |
| `PP-DISPUTES-TEST-GO-LIVE` | https://developer.paypal.com/disputes/test-go-live | 2026-08-17 | PayPal documents a Sandbox-only end-to-end dispute simulation and dedicated test endpoints. | The flow requires test credentials, a synthetic transaction, app setup and mutation calls that are not authorized by the current work order. |

## Official U.S. court procedural records

| Source ID | Official source | Filing date | Allowed claim | Required limitation |
| --- | --- | --- | --- | --- |
| `US-COURT-ZEPEDA-2017-DOC357` | https://www.govinfo.gov/content/pkg/USCOURTS-cand-4_10-cv-02500/pdf/USCOURTS-cand-4_10-cv-02500-57.pdf | 2017-03-24 | The court approved a class settlement and recorded historical allegations involving holds, reserves, closure or suspension. | Settlement approval is not a finding that every allegation was true, not current PayPal policy, not an individual dispute merits result and not proof of a rapid-volume trigger. |
| `US-COURT-EVANS-2022-DOC37` | https://www.govinfo.gov/content/pkg/USCOURTS-cand-5_22-cv-00248/pdf/USCOURTS-cand-5_22-cv-00248-0.pdf | 2022-06-02 | The complaint alleged account freezes, limitations and fund seizures tied to alleged AUP violations; the court compelled arbitration and dismissed without prejudice to later award review. | The court did not decide the underlying merits. Allegations are not verified violation or outcome facts and must not be training truth. |

## Product claim boundaries by stage

| Stage | Sources | Supported statement | Unsupported statement |
| --- | --- | --- | --- |
| AUP warning | `PP-US-AUP`, `PP-US-UA` | The description matched a category in the public US AUP and requires human/provider review. | The merchant violated policy, is approved, or becomes compliant after rewording. |
| Velocity readiness | `PP-US-UA`, seller and Sandbox sources | Rapidly increasing typical sales volume is one of several public risk examples; local evidence readiness can be checked. | A known PayPal threshold, AML/fraud finding, predicted limitation or guaranteed release. |
| Dispute mediation | Purchase/Seller Protection and Disputes sources | Route by actual reason/stage/requested evidence; prepare a human-reviewed draft. | Automatic eligibility, evidence sufficiency, dispute victory, refund or submission authority. |

No reviewed official individual case proves that rapid sales growth alone caused an account limitation. The public US User Agreement is the controlling source for the narrower risk-example statement.

## Runtime requirements

- Active source metadata stores exact URL, source class, visible/filing date, retrieval timestamp, representation, limitations and digest.
- `effective_date` remains unknown unless separately established.
- Jurisdiction-neutral Developer documentation cannot satisfy US policy coverage.
- Procedural court records cannot satisfy a final-merits filter.
- Missing, changed or redirected sources fail closed and require a new versioned refresh.
- Public source text is treated as data and never grants tool, provider or financial authority.
