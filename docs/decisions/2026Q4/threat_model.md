# PayGuard Threat Model

Status: current US-only local prototype threat model.

## Assets

- synthetic orders, transactions, disputes and evidence;
- product descriptions and deterministic findings;
- public source identities, dates, limitations and digests;
- short-lived session, CSRF, acknowledgement and review state;
- pseudonymization keys and tokens;
- backend-only Sandbox credentials and access tokens when separately enabled;
- sanitized provider and model receipts when separately authorized;
- module registries, input hashes, rollback manifests and validation evidence.

## Trust boundaries

1. browser to loopback API;
2. untrusted HTTP input to strict schema validation;
3. request jurisdiction to the US-only package/corpus loader;
4. synthetic evidence to deterministic engines;
5. deterministic output to human review;
6. backend process to fixed PayPal Sandbox endpoints;
7. accepted structured synthetic facts to the optional model adapter;
8. repository source to governance and release artifacts.

Local synthetic sessions are not merchant authentication or durable authorization. Public sources are data, never instructions. A valid schema does not establish legal applicability, evidence authenticity or provider eligibility.

## Threats and controls

| Threat | Controls | Residual boundary |
| --- | --- | --- |
| Host/Origin abuse, CSRF and cross-session leakage | Loopback binding, exact Host/Origin allowlists, opaque session IDs, session-bound CSRF and no browser persistence | No production tenant authentication |
| Memory exhaustion, repeated injection and partial mutation | Session/body/row/activity/rate limits, TTL, idempotent synthetic scenarios, validation before mutation and reset | Local process remains a prototype |
| Foreign policy or case fallback | US-only request enum, validation before loader invocation, one active package, pinned corpus and no fallback | Source completeness and legal review remain open |
| Source substitution, stale data or hash drift | Exact URL/host/path allowlists, source class, separate dates, pinned hashes and fail-closed loader | Public pages may later change and require a new versioned refresh |
| Policy laundering | `REFERENCE_ONLY`, `NOT_ESTABLISHED`, `NOT_MADE`, warning-only result and explicit limitations | Full current-policy applicability is unverified |
| Prompt injection or source-content execution | Stage-only caller request, server-owned prompt contract and digest, fixed typed synthetic facts, opaque citation IDs, closed JSON Schema enums, no raw HTML, no caller model/config/path/schema/tool, disabled tools/function calling/retrieval/streaming and strict post-validation | A permitted enum can still be semantically poor; inventory review remains required whenever the sentence set changes |
| AI authority escalation | AI after deterministic preflight, fixed citations, server-stamped authority fields, no session mutation, no external action and human semantic review | One fixed-synthetic Gemini execution is accepted; repeatability, other stages and real-record behavior remain unverified |
| Model request flooding or denial of wallet | Atomic reserve before execution, three permanent process-local attempts, one per stage, failures count, no automatic retry, and no reset through session lifecycle | Process restart or another worker/instance creates another local budget; public deployment requires a durable shared quota and gateway cost circuit breaker |
| False Sandbox connection | Connected state only after a validated authentic receipt; mock and authentic evidence classes remain distinct | Dashboard identity, country and feature availability remain unknown until operator readback |
| Credential or token disclosure | Backend process environment only, fixed Sandbox host, no redirect, no frontend/token return, sanitized errors and no payload logging | Operator endpoint security remains outside the local prototype |
| Duplicate or uncertain invoice creation | One-shot review binding, idempotency where supported, no automatic retry after uncertain success, DRAFT-only scope | No separate GET readback is claimed |
| Provider-action expansion | Default-off outbound, exact endpoint/action allowlist and frozen send/payment/capture/refund/dispute mutation | Production and external submission remain unavailable |
| PII leakage | Synthetic default data, bounded allowlists, in-memory pseudonymization, no reverse map/raw log and manual review | Pattern detection is incomplete and is not legal anonymization |
| Evidence overclaim | Separate presence, authenticity, verification, sufficiency, eligibility and outcome states | A human can still misinterpret a draft; UI limitations remain mandatory |
| Dispute-authority confusion | Documented authority distinction and explicit statement that the current demo performs no provider-case routing | A real case requires current provider fields and an independently validated adapter |
| Procedural record promoted to merits | Source class `HISTORICAL_US_COURT_PROCEDURE`, explicit limitations and final-decision rejection | No complete official individual-outcome library exists |
| Velocity signal promoted to fraud/AML | Local baseline provenance, backend-owned calculation and forbidden-label tests | Proprietary provider criteria are unavailable by design |
| Approval reuse or stale UI state | Case/action/payload digest, nonce, actor role, expiry, abort controllers and generation checks | Durable restart/concurrency authority remains open |
| Supply-chain and artifact drift | Locked dependencies, disabled npm lifecycle scripts, one writer, isolation diff, module audit and no-op readback | Full SAST, history scan and vendor review remain release gates |

## US Sandbox account boundary

The existing PayPal login is a Developer-login identity. The merchant role is a fictitious Business sandbox seller; the buyer role is a fictitious Personal sandbox account. These roles do not change or prove the live-account type.

The UI may say `PayPal Sandbox` before seller-country confirmation. It may say `US Business sandbox seller` only after trusted Dashboard confirmation. Invoicing availability also requires confirmation. The Sandbox host and browser locale are not country evidence.

`BLK-01B` is closed only for the independently reviewed sanitized authentic OAuth result and one unsent invoice `DRAFT` result. MockTransport results, screenshots and local UI state did not and cannot expand that accepted provider-evidence boundary.

## AUP boundary

The deterministic matcher can surface public US AUP categories and distinguish potential prohibited-category, prior-approval-category, ambiguous and no-local-match results. It cannot decide a violation, approval, legality or safety.

The second warning offers edit, cancel, or acknowledge and continue. Acknowledgement authorizes only a local next step and is revoked by content/session changes or expiry. Required-field validation may stop an incomplete local draft; the AUP warning itself is not a substitute PayPal block.

## Velocity boundary

The public US User Agreement supports the narrow statement that rapidly increasing typical sales volume is one of several listed risk examples and that some criteria may be confidential. PayGuard does not know a provider threshold or hidden model.

The local signal cannot be labelled AML, fraud, money laundering or a predicted hold, limitation, reserve or release. Tracking may be relevant but cannot guarantee a provider action.

## Dispute boundary

The current synthetic resolver reads a closed fixture containing reason, status, lifecycle stage, seller-response due date, normalized available actions and evidence requests with source and action. Only exact `REQUESTED_FROM_SELLER` plus `PROVIDE_EVIDENCE` rows can create preparation tasks. It accepts only separately bound synthetic proof records and attachment bytes, then discards the bytes after signature/type/size validation. Raw provider case, order and request identifiers remain restricted server-side; the browser receives non-identifying references. The restricted digest is recomputed before reuse, AI eligibility and local approval so nested tampering fails closed. A real adapter must additionally retain current PayPal response options and HATEOAS links without treating them as action authority. Every fixture field remains explicitly synthetic.

PayGuard may prepare and pseudonymize a local draft. It cannot provide evidence, send a message, make an offer, accept a claim, acknowledge a return, appeal, refund or adjudicate. Internal claims remain under PayPal authority; external disputes remain under the bank/card issuer's authority.

Counterfeit goods may be a Purchase Protection SNAD condition. SNAD is outside US Seller Protection. Photos are possible evidence, not a universal requirement.

## Data retention and privacy

- no real business or personal data enters default fixtures;
- queries and filters remain bounded in request memory and are not logged;
- session state expires and is not durable authorization;
- pseudonymization keys remain memory-only;
- provider credentials and tokens remain backend-memory only;
- provider records do not enter the synthetic pool;
- model calls cannot receive real case data under current authority;
- process-local model attempt reservations are not a production distributed rate limiter;
- no database, scheduler, cloud sync or public storage is enabled.

## Release blockers

- `BLK-02B`: one accepted fixed-synthetic Gemini response and human semantic review, with every broader model claim still out of scope;
- `PG-003`: durable authenticated review/submission authority;
- `PG-004`: real PII lifecycle and retention;
- `PG-006`: security, rights, public export and deployment acceptance.

The implementation must fail closed at the first schema, source, identity, privacy, evidence, authority or provider mismatch. Local validation cannot promote an external or release state.
