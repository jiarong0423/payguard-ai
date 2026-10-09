# PayGuard Unified Console Contract

Status: current US-only local contract. The console is an advisory and evidence-readiness interface, not a PayPal decision system.

## User journey

The console presents one fixed sequence:

1. **US AUP Preflight Warning Funnel** — inspect a product description before an invoice draft; the operator-facing screen is labeled `AUP Preflight Screen`.
2. **Velocity and Fulfillment Readiness** — inspect a local anomaly and missing fulfillment evidence.
3. **Dispute Evidence Mediation** — organize a synthetic dispute draft for human review.

The three stages remain separate. Stage 1 does not collect arrival photos. Stage 2 does not claim a provider threshold or account outcome. Stage 3 does not auto-submit evidence, refund or adjudicate.

## Provider-context banner

The optional Sandbox disclosure displays these boundaries before its connect and draft actions become visible:

- `Demo market: United States`
- `Provider environment: PayPal Sandbox`
- `Developer login: existing PayPal login; live account type not inferred`
- `Merchant role: fictitious Business sandbox seller`
- `Buyer role: fictitious Personal sandbox account when required`
- `Sandbox seller country: unconfirmed until Dashboard readback`
- `Invoicing eligibility: unconfirmed until bounded provider evidence`
- `External action: disabled by default`

The Sandbox endpoint, browser locale, IP signal, currency and operator residence are not proof of the sandbox seller's country or merchant legal region.

## Backend-owned truth

The backend owns:

- input validation and deterministic routing;
- AUP findings and warning state;
- velocity windows, baselines, ratios and limitations;
- dispute chronology, missing evidence and adjudicator route;
- source identities, dates, digests and applicability limitations;
- acknowledgement/review identity, digest, nonce and expiry;
- synthetic/authentic evidence classification;
- provider and model availability state.

The frontend may format, filter and sort supplied values. It must not recompute risk, infer policy applicability, invent fallback data, reconstruct a rejected citation or change an authority state.

## Session and HTTP boundary

- The API binds to loopback in the local prototype.
- Mutation requests require the current session and CSRF token.
- Origin and Host are exact allowlists.
- Bodies, nested documents, rows, activity, rates and sessions are bounded.
- Unknown keys, duplicate JSON keys, non-finite numbers, malformed UTF-8, unsupported enums and control characters fail closed.
- Errors are fixed and sanitized; they do not echo product, buyer, credential or source content.
- Reset and expiry revoke drafts, acknowledgements, reviews, tokens and pending UI results.
- Aborted or stale responses cannot reappear after context, session or revision changes.

## Stage 1 UI contract

The panel shows:

- a bounded product/service description editor;
- explicit US policy context;
- deterministic findings;
- `NO_MATCH` or `REVIEW_SIGNAL`;
- `NOT_MADE`, `NOT_ESTABLISHED` and advisory-only labels;
- the official PayPal US AUP link and source limitation;
- a second-warning dialog with edit, cancel and acknowledge/continue choices.

The acknowledgement is single-use and bound to the exact description digest. The ordinary invoice review remains separate. A warning acknowledgement does not authorize invoice creation. A reviewed invoice draft does not authorize sending.

## Stage 2 UI contract

AG Grid displays backend-supplied synthetic transactions and exact backend calculations. The panel shows:

- observation window;
- transaction count and amount;
- local baseline and provenance;
- ratio and local signal;
- a general fulfillment-capacity and tracking/delivery preparation reminder, explicitly marked as not supplied by the synthetic capture stream;
- limitations stating that Stage 2 has not verified per-order proof or classified missing merchant evidence; detailed requested-proof state belongs to Stage 3;
- public US User Agreement reference.

The UI must say that the result does not predict a hold, limitation, reserve or release. It must never display AML, money laundering, fraud or PayPal risk-score conclusions derived from the local signal.

## Stage 3 UI contract

The panel shows:

- non-identifying synthetic case and order references plus source label;
- reason, status and lifecycle stage;
- internal or external adjudicator boundary;
- requested evidence types and sources;
- seller response due date and allowed response options when present;
- a deterministic route state and per-request structural evidence state;
- restricted original custody/count summary with no returned file content or proof values;
- order, shipment, delivery, dispute and refund chronology;
- pseudonymization method and limitations;
- missing, conflicting and unverified evidence;
- a local human-review control bound to the draft digest.

The current action is **record local draft review**. The review control is enabled only for `READY_FOR_LOCAL_REVIEW`, and its digest binds both the visible draft and the recomputed, verified hidden restricted-layer digest. Raw provider case, order and request identifiers are never browser fields. Provide Evidence, Send Message, Make Offer, Accept Claim, Acknowledge Return, Appeal, refund and every production mutation are unavailable.

## Sponsor analytics UI contract

The sponsor analytics workspace is lazy-loaded after an explicit operator action. It uses AG Grid Community and first-party React components with:

- the same light PayGuard presentation tokens as the main console;
- custom lifecycle, authority-map and evidence-pulse widgets;
- one sortable, filterable and resizable AG Grid transaction stream with order, amount, currency and capture-time columns supplied by the backend;
- a deterministic local dashboard guide limited to the visible in-memory snapshot;
- a dedicated single-open mobile review accordion that hides the desktop grid below 721 pixels, opens the lifecycle section by default and keeps all four evidence sections keyboard reachable.

The local guide has no provider, payment, workflow or external-model tool. It stores only the current in-memory session. The active analytics dependency boundary is AG Grid Community under MIT, and no Commercial AG package is included in the current frontend contract.

## Reference panel

The active profile is US-only. There is no region selector and no cross-region fallback. The reference panel may display:

- official PayPal US policy sources;
- jurisdiction-neutral PayPal Developer API/process sources;
- official U.S. court procedural records with an explicit procedural caveat.

Developer documentation cannot satisfy policy coverage. Court records cannot become current policy or final individual merits. Empty evidence returns an explicit missing/unsupported/manual-review state.

Source links are restricted to the exact allowlisted official hosts and paths. All source text renders as plain React text; source data is never executed as HTML or instructions.

## Optional AI panel

The AI button remains disabled until the stage's deterministic preflight has produced accepted structured synthetic facts. The request cannot include arbitrary user documents, private business data, credentials, loader paths, model configuration or action authority.

The response contract includes:

- summary;
- bounded evidence points;
- bounded missing-evidence list;
- pinned citation identities;
- execution evidence class;
- `compliance_decision=NOT_MADE`;
- `current_policy_applicability=NOT_ESTABLISHED`;
- semantic review state;
- `external_action_authorized=false`.

The caller submits only the fixed stage enum. The server owns prompt contract `payguard-bounded-advisory-v2` and records its SHA-256 digest in each accepted response. The model receives fixed synthetic facts and opaque pinned citation IDs. It cannot accept a caller prompt, choose a model, change a stage or schema, add a citation, call a tool, retrieve a URL, browse, stream, perform a function call or request an external action. Every generated sentence must be selected verbatim from the stage-specific JSON Schema enum; backend post-validation rejects any free text, cross-stage text, reordered citation, extra field, tool/thought part or authority change.

Two startup-selected adapters implement this single contract. The default `api` command uses Gemini. The explicit `local-ai-api` command uses the fixed LM Studio loopback model. A running process has one adapter only; the API has no provider field, no automatic fallback and no provider racing. Valid response identity pairs are `gemini-3.8-flash` with `SYNTHETIC_TEST_RESPONSE` or `OPERATOR_LIVE_RESPONSE`, and `nvidia-nemotron-3-nano-4b` with `LOCAL_RUNTIME_RESPONSE`.

The backend owns a single process-local attempt budget with exactly three permanent reservations, one per fixed stage. It validates deterministic readiness and atomically reserves the stage before invoking the adapter. A provider failure, timeout, cancellation, worker crash or invalid response consumes the reservation. Session reset, expiry, purge and replacement do not return it. SDK retry count remains one total invocation. A fourth attempt receives `429 ai_attempt_limit`; an earlier repeat of an already reserved stage receives `409 ai_stage_attempt_exhausted`.

This budget does not survive process restart and is not shared between workers, pods or regions. Before public multi-instance deployment, the same reserve-first contract must move to a strongly consistent shared store or one authoritative Redis cluster with an atomic script, durable persistence and fail-closed behavior. The quota identity must be authenticated or server-signed, and an API gateway must enforce request-rate and daily-cost circuit breakers. No model output can mutate the merchant session, acknowledge a warning, approve a draft or call a provider. `BLK-02B` has one independently accepted fixed-synthetic Gemini execution and human review; no broader model behavior is established.

## Optional Sandbox panel

Outbound access is disabled by default. Credentials come only from the operator-owned backend process environment and never enter frontend state or activity logs.

The only accepted `BLK-01B` sequence is:

1. operator confirms an eligible US Business sandbox seller and Invoicing availability;
2. operator explicitly enables the bounded Sandbox path;
3. backend performs one OAuth request to the fixed Sandbox host;
4. UI displays connected only after a validated authentic response;
5. human reviews the exact synthetic invoice payload and action;
6. backend may create one unsent invoice `DRAFT`;
7. the sanitized response receipt is independently reviewed;
8. no automatic retry occurs after an uncertain create result.

Invoice send, reminders, QR distribution, payment, capture, refund, dispute mutation and production remain frozen. A POST create response is the accepted creation receipt, not a separate GET readback.

## Accessibility and stale-state requirements

- Preserve stable accessible names and test IDs.
- Dialog focus enters the warning, stays trapped, and returns to the invoking control.
- Escape performs the cancel path where allowed.
- Status changes use bounded `aria-live` regions.
- Keyboard-only operation reaches every local action.
- Desktop and 390 px mobile layouts expose the same authority and limitation text.
- Changing description, source context, session or revision clears stale result and gate state.

## Evidence labels

| Label | Meaning |
| --- | --- |
| `synthetic` | Local authored fixture; no provider or model execution |
| `public_reference` | Public source summary; no account-specific applicability |
| `SYNTHETIC_TEST_RESPONSE` | Mock transport result; not authentic provider proof |
| `AUTHENTIC_SANDBOX_RESPONSE` | Sanitized evidence of the exact accepted Sandbox call only |
| `MODEL_EXECUTION_UNVERIFIED` | No accepted authentic model receipt |
| `AUTHENTIC_MODEL_RESPONSE` | Sanitized evidence of the exact bounded model call only, still subject to human review |

The UI may not relabel one class as another.

## Acceptance

Acceptance requires source scans, component tests, API tests, session/CSRF negatives, foreign-before-load tests, focused warning/acknowledgement tests, full project tests, frontend build, desktop/mobile/keyboard browser review, module audit publication, no-op audit and canonical readback.

Documentation or rendered appearance alone cannot close `BLK-01B`, expand the one-execution `BLK-02B` evidence or close any release gap.
