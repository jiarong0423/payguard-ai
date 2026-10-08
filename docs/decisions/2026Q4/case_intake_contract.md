# PayGuard US Case Intake and Evidence Contract

Status: current US-only local contract. This is an authored review schema, not a PayPal submission schema and not a substitute for the live provider response.

## Processing order

Every request follows the same deterministic sequence:

1. validate a closed request envelope;
2. validate types, formats, identifiers, amounts and timezone-aware timestamps;
3. require exactly one supported theme;
4. check required fields and evidence references;
5. check chronology, currency, amount and identifier consistency;
6. apply deterministic routing and fixed reference matching;
7. prepare an advisory record for human review;
8. optionally create an AI summary from accepted structured facts;
9. leave every provider or adjudicator action outside the local contract.

AI never fills a required field, guesses a jurisdiction, resolves a contradiction, authenticates evidence or selects an external action.

## Common envelope

| Field | Rule |
| --- | --- |
| `schema_version` | Exact supported integer |
| `request_kind` | Exactly one of `source_compliance`, `velocity_guard`, `dispute_mediation` |
| `jurisdiction` | Exact `US` |
| `as_of` | Timezone-aware ISO timestamp |
| `source` | `synthetic` in the current demo; public citations remain `public_reference` |
| `case_id` | Bounded stable identifier |
| `evidence_items` | Bounded list with unique `evidence_id` values |
| `references` | Exact source/chunk pairs from the active US profile |

Unsupported or foreign jurisdiction input is rejected before any policy package, corpus or scenario-card load. Multiple themes produce `needs_clarification`. Unknown fields are rejected.

## Evidence item

Each evidence item contains:

- `evidence_id` — unique bounded identifier;
- `evidence_type` — allowlisted local type;
- `source_class` — synthetic or public reference in the current scope;
- `provided_at` — timezone-aware timestamp or explicit unknown state;
- `content_digest` — digest of the accepted bounded payload when applicable;
- `verification_state` — supplied/unverified, document-stated, conflicting, unknown or not applicable;
- `field_refs` — exact request fields supported by the item;
- `limitations` — what the item cannot establish.

Evidence presence is not authenticity. Authenticity is not sufficiency. Sufficiency is not program eligibility or outcome prediction.

## Route 1 — US AUP preflight warning funnel

### Required fields

| Field | Requirement |
| --- | --- |
| `product_id` | Required bounded identifier |
| `title` | Required non-empty text |
| `description` | Required bounded text |
| `category` | Required explicit merchant category |
| `amount` | Finite positive decimal string |
| `currency` | Exact `USD` |
| `seller_statement` | Required merchant-authored statement or explicit unknown state |
| `approval_status` | `CONFIRMED`, `NOT_CONFIRMED` or `UNKNOWN`; never inferred |
| `policy_context` | Exact US `REFERENCE_ONLY` profile |

### Deterministic results

- `POTENTIAL_PROHIBITED_CATEGORY_MATCH`
- `POTENTIAL_PREAPPROVAL_CATEGORY_MATCH`
- `AMBIGUOUS_POLICY_MATCH`
- `NO_LOCAL_RULE_MATCH`

These are local labels. The output remains `NO_MATCH` or `REVIEW_SIGNAL`, `compliance_decision=NOT_MADE` and `current_policy_applicability=NOT_ESTABLISHED`.

### Warning choices

- `RETURN_TO_EDIT`
- `CANCEL`
- `ACKNOWLEDGE_AND_CONTINUE`

Acknowledgement is bound to the description digest, session, actor role, policy source, evaluation identity and expiry. Editing, reset, session change or expiry revokes it. Acknowledgement does not certify compliance.

## Route 2 — Fulfillment and velocity evidence readiness

### Executable fields

| Field | Requirement |
| --- | --- |
| `transactions` | Required non-empty bounded list for intake. Each row is a closed object. The dashboard arithmetic engine may separately render an empty initial state; that state is not an accepted intake submission. |
| `transactions[].order_id` | Required unique bounded identifier. There is no separate executable `transaction_id`. |
| `transactions[].amount` | Required finite positive decimal string. |
| `transactions[].currency` | Required uppercase three-letter value; all rows must agree. The demo uses `USD`. |
| `transactions[].occurred_at` | Required timezone-aware timestamp. |
| `baseline_amount_per_hour` | Required finite nonnegative decimal string. Zero is structurally valid but routes to `manual_review` with `insufficient_baseline`; no ratio is calculated or invented. |
| `baseline_provenance` | Required exact value: `SYNTHETIC_BASELINE` or `CALLER_SUPPLIED_UNVERIFIED`. `UNKNOWN` is an intake-only missing-information sentinel and never reaches the engine. |
| `baseline_window_start`, `baseline_window_end` | Required timezone-aware comparison period for either supported provenance. It must be complete, ordered and nonoverlapping with the observation window. |
| `baseline_evidence_ref` | Additionally required for `CALLER_SUPPLIED_UNVERIFIED`; it must join a `BASELINE` evidence item bound to this field. |
| `window_hours` | Required strict integer from 1 through 24. The observation window is derived as `(as_of - window_hours, as_of]`; the payload has no submitted observation start or end field. |
| `threshold` | Required finite positive decimal string used only by the local arithmetic rule. It is not a PayPal threshold. |
| `limitation_review_requested` | Optional strict boolean. When true, `limitation_notice_ref`, `limitation_type` and `limitation_status` are required. |
| `hold_started_at`, `hold_expected_end_at` | Optional timezone-aware limitation chronology. |
| `kyc_request_status` | Optional exact state. When `REQUESTED`, `kyc_response_status` and `kyc_request_evidence_ref` are required. |
| `fulfillment_review_requested` | Optional strict boolean. When true, `fulfillment_capacity_status` and `fulfillment_evidence_ref` are required. |

### Consistency rules

- transaction and order identifiers must join without duplicates;
- amounts must share the declared currency;
- transactions after `as_of` require clarification;
- at least one transaction must fall in `(as_of - window_hours, as_of]`;
- the baseline must satisfy `baseline_window_start < baseline_window_end <= as_of - window_hours`;
- a zero baseline is incomplete for comparison and routes to manual review; a non-finite baseline is invalid;
- caller labels and evidence remain unverified and cannot be presented as provider data or a PayPal threshold;
- evidence claims must reference existing evidence items.

Carrier, tracking, shipment-date and destination-match claims belong inside separately bound evidence records; they are not executable Route 2 payload fields. The intake result is one of the contract states listed below. After accepted intake, the arithmetic engine may return `review_velocity`, `insufficient_baseline` or `normal`. It never establishes fraud, AML, a provider score or a predicted account action.

## Route 3 — Dispute evidence mediation

### Required executable local fields

| Field | Requirement |
| --- | --- |
| `merchant_case_ref` | Required bounded local case identifier |
| `order_id` | Required bounded order identifier |
| `reason_code` | Exact supported reason enum; `INR` normalizes to `MERCHANDISE_OR_SERVICE_NOT_RECEIVED` |
| `case_status` | `OPEN`, `WAITING_FOR_SELLER_RESPONSE`, `WAITING_FOR_BUYER_RESPONSE`, `UNDER_REVIEW`, `RESOLVED`, `CLOSED` or `UNKNOWN` |
| `case_stage` | `INQUIRY`, `CHARGEBACK`, `PRE_ARBITRATION`, `ARBITRATION` or `UNKNOWN` |
| `seller_response_due_date` | Required timezone-aware response timestamp retained without inference |
| `available_actions` | Bounded normalized action identifiers from the synthetic response fixture; not PayPal `allowed_response_options` |
| `evidences` | Current bounded evidence requests with request ID, provider evidence type, source, mandatory flag and action |
| `opened_at` | Timezone-aware timestamp |
| `order_created_at` | Timezone-aware timestamp |

A synthetic fixture must label every value synthetic. It cannot be described as a current PayPal response.

The current local intake has no provider `transaction_id`, PayPal `allowed_response_options`, raw HATEOAS `links`, buyer statement or seller statement field. It receives only a closed synthetic provider-response fixture. Those omitted fields remain future provider-adapter requirements and cannot be presented as current runtime capability.

### Supported reason matrix

| Reason | Evidence classes to check only when requested |
| --- | --- |
| `MERCHANDISE_OR_SERVICE_NOT_RECEIVED` | Proof of fulfillment, carrier/tracking, signature/receipt, proof of refund |
| `MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED` | Description/listing, item URL, return policy, authenticity/condition material, proof of refund |
| `UNAUTHORISED` | Proof of fulfillment, signature/receipt, proof of refund, other requested records |
| `CREDIT_NOT_PROCESSED` | Refund identifier or explanation for the credit basis |
| `DUPLICATE_TRANSACTION` | Transaction pair, refund identifier and supporting explanation |
| `INCORRECT_AMOUNT` | Charged, expected and refunded amounts with currency and explanation |
| `PAYMENT_BY_OTHER_MEANS` | Alternate payment record and refund identifier when requested |
| `CANCELED_RECURRING_BILLING` | Subscription agreement, cancellation time, billing time and refund identifier |
| `OTHER` | The actual requested evidence and mandatory human classification |

The provider's current requested evidence controls. A static checklist is never a substitute.

### Evidence retention and pseudonymized export boundary

PayPal's current dispute response is the routing authority for a real case. The executable synthetic resolver now retains, without guessing, the fixture's `dispute_id`, `order_id`, `reason`, `status`, `dispute_life_cycle_stage`, `seller_response_due_date`, normalized available actions, and each current evidence object's `request_id`, `evidence_type`, `source`, `mandatory` state and action. A seller preparation requirement is created only when both `source=REQUESTED_FROM_SELLER` and `action=PROVIDE_EVIDENCE`; null, unknown or mismatched actions remain `CONTEXT_ONLY`. A future live adapter must preserve the same boundary and additionally retain raw provider response options and HATEOAS links without converting them into authority.

Reason-specific source records remain separate evidence items:

- fulfillment records: carrier name, tracking number, shipment date, delivery date/status, destination-match result, and supporting carrier document;
- refund records: exact refund identifier, amount, currency, and time;
- item-description records: product description, item URL or listing snapshot, return policy, contract or affidavit, condition/authenticity material, and relevant photographs;
- transaction records: charged and expected amount, currency, duplicate transaction pair, alternate payment record, subscription agreement, cancellation time, and billing time as applicable;
- chronology records: order creation, provider notice, dispute open, seller-response due date, shipment, delivery, return, refund, and human review times.

This requires two different data products:

1. **Restricted original evidence.** The unmodified carrier, transaction, listing, communication, photo, receipt, address-match and refund records needed for provider review. Required proof fields must not be removed merely to make an AI-safe copy. The current synthetic runtime validates proof joins and attachment signatures/types/sizes, reduces attachment bytes to content-free metadata, stores the resulting restricted object only in expiring session memory and returns only a count/custody summary to the browser. Raw provider case, order and request identifiers remain in this layer; the browser receives only non-identifying session references. The backend recomputes and constant-time checks the restricted object digest before reuse, AI eligibility or local approval. Real-record storage, access control, deletion and retention remain frozen under `PG-004`; the current demo does not persist such records.
2. **Pseudonymized internal review copy.** A derived, minimum-field document for local human review or bounded AI summarization. It must carry the backend-issued `INTERNAL_REVIEW_ONLY_V1` export profile and may contain only backend-produced redacted text, redaction method/counts/types, limitations and advisory authority flags. It must exclude raw identity fields, case/order identifiers, session identifiers, identity tokens, draft digests, credentials and provider submission authority. A missing or different export profile fails closed.

Frontend downloads contain the second product only. The operator may download the pseudonymized document as a standalone JSON file or create a deterministic six-entry Internal Review ZIP containing `README.txt`, `manifest.json`, the response-driven requirement projection, the synthetic timeline, pinned public-source citations and the same pseudonymized document. The ZIP manifest binds every non-manifest payload by byte length, CRC-32 and SHA-256. Before browser download, PayGuard parses the completed ZIP and revalidates its fixed names and order, ZIP metadata, canonical JSON, manifest semantics and payload digests. Both formats are internal review artifacts and are not PayPal-supported evidence attachment formats.

The ZIP carries only a non-sensitive custody/count summary for the restricted layer. It excludes raw provider and local identifiers, session references, identity tokens, restricted digests, proof values, attachment names and attachment bytes. Its fixed authority remains `provider_submission=NOT_PERFORMED`, `dispute_decision=NOT_MADE` and `human_review_required=true`. A malformed, mutated or semantically altered package fails closed before download.

The local resolver accepts only JPG, JPEG, GIF, PNG and PDF signatures, requires each synthetic attachment to be smaller than 10 MB and caps the set at 50 MB. This validation proves local shape only. A future provider submission must re-check the live response and current provider attachment rules, select the necessary restricted original evidence, and obtain separate human authorization. PayGuard does not upload either local download.

### Protection and counterfeit boundary

Counterfeit goods may be a Purchase Protection SNAD condition. Photos, listing snapshots, serial numbers, supplier records and third-party evaluations may help describe the record, but no single item is universally required unless the current case requests it.

SNAD is outside US Seller Protection. Proof of shipment or delivery can support eligible INR or Unauthorized Transaction requirements but cannot establish eligibility, sufficiency or victory.

## Deterministic result priority

Apply the first matching state:

1. `invalid_input` — malformed schema, type, format, amount, time, identifier or forbidden field;
2. `needs_clarification` — multiple themes, ambiguous route, future transaction, empty observation window or contradictory chronology;
3. `needs_input` — required field or evidence reference is missing;
4. `manual_review` — input is structurally complete but conflicting, unverified, procedurally limited, authority-bound or uses an accepted reason outside the synthetic INR engine;
5. `ready_for_local_rules` — required local fields are complete and consistent enough for deterministic local processing.

`ready_for_local_rules` does not mean ready for provider submission.

A reason outside the accepted reason enum is `invalid_input`. The accepted `OTHER` reason and accepted non-INR reasons route to `manual_review`; they are never silently treated as INR.

## Scenario and historical record boundary

The active scenario catalog contains three synthetic cards:

- `US-DEMO-AUP-WARNING`;
- `US-DEMO-VELOCITY-READINESS`;
- `US-DEMO-DISPUTE-EVIDENCE`.

They demonstrate routing and evidence fields. They are not real cases, provider decisions or model training truth.

The active public profile also contains two official U.S. court procedural records. One concerns settlement approval; the other compels arbitration and expressly does not decide the underlying merits. Neither record may be used as a final individual outcome, current policy, risk label or proof of a rapid-volume trigger.

## AI boundary

AI may receive only accepted structured synthetic facts and pinned citation identities after deterministic preflight. It may summarize:

- accepted facts;
- missing evidence;
- chronology;
- source limitations;
- questions for human review.

It may not add facts, authenticate documents, choose jurisdiction, resolve conflicts, select a provider action, predict a result or change any deterministic status. `BLK-02B` has one independently accepted fixed-synthetic `gemini-3.8-flash` execution; that evidence does not establish repeatability, other-stage quality or real-record behavior.

## Acceptance tests

- normal complete request;
- each missing required field;
- invalid decimal, currency, timestamp, identifier and enum;
- duplicate IDs and broken evidence joins;
- contradictory chronology, amounts and destination state;
- multiple/unknown route;
- foreign jurisdiction rejected before loader invocation;
- corrupted source/card digest fails closed;
- US procedural record rejected as final merits;
- complete evidence never promoted to authentic, sufficient, eligible or successful;
- AI invocation unavailable before deterministic acceptance;
- edit/reset/session/expiry revokes acknowledgement and review.
- only current `REQUESTED_FROM_SELLER` rows create seller requirements; buyer/context rows never do;
- missing mandatory evidence, unknown provider evidence types, expired due dates and unavailable actions never fall back to static INR requirements;
- attachment extension, declared media type, magic signature, per-file size, aggregate size and evidence joins fail closed;
- browser response returns the restricted-layer custody/count summary but no proof fields, attachment filename, attachment bytes or restricted digest;
- local review digest changes when either the visible draft or hidden restricted-layer digest changes;
- internal export contains only the pseudonymized document allowlist and no case ID, order ID, identity token, session ID or draft digest;
- order identifiers embedded in the synthetic narrative are pseudonymized before export;
- export failure is fail-closed and performs no provider submission;
- a pseudonymized internal JSON file and Internal Review ZIP are never labeled as PayPal-supported evidence attachments;
- the ZIP contains exactly six fixed entries and no restricted original, raw attachment, raw identifier, proof value or credential;
- completed ZIP bytes are parsed before download and must match the manifest's fixed authority, canonical JSON, byte length, CRC-32 and SHA-256 declarations;
- binary corruption, manifest semantic mutation and sensitive free-text markers fail closed before download.
