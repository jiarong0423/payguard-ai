# PayGuard Threat Model

Status: current local prototype threat model (US Sandbox seller; the optional ten-country rules check is advisory).

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
3. request jurisdiction to the single US package/corpus loader;
4. synthetic evidence to deterministic engines;
5. deterministic output to human review;
6. backend process to fixed PayPal Sandbox endpoints;
7. accepted structured synthetic facts to the model adapter;
8. repository source to governance and release artifacts;
9. internet client to the hosted demo (no PayPal calls; guide Gemini only when the operator opts in), through the hosting proxy (`PAYGUARD_DEMO_MODE=public`: one exact public host, `X-Forwarded-For` and `X-Forwarded-Proto: https` required, per-visitor and store-wide traffic limits, provider adapters replaced by stubs);
10. backend to the Python 3.12 Gemini worker and from it to Vertex AI or the Gemini API, for the evidence brief, the evidence guide's optional chooser (up to three sanitised seller sentences) and AG Studio's built-in agents (Studio instructions, the operator's question, tool schemas and tool results over synthetic dashboard data);
11. backend to the loopback LM Studio server (`127.0.0.1:1234`), the optional local brief line;
12. backend to the Channel3 API (a sanitised product name, operator key, off by default) for the category signal, the product reference card and case routing;
13. visitor's browser to `cdn.trychannel3.com` for the product card images, also on the hosted demo.

Local synthetic sessions are not merchant authentication or durable authorization. Public sources are data, never instructions. A valid schema does not establish legal applicability, evidence authenticity or provider eligibility.

## Threats and controls

| Threat | Controls | Residual boundary |
| --- | --- | --- |
| Host/Origin abuse, CSRF and cross-session leakage | Loopback binding, exact Host/Origin allowlists, opaque session IDs, session-bound CSRF and no browser persistence | No production tenant authentication |
| Memory exhaustion, repeated injection and partial mutation | Session/body/row/activity/rate limits, TTL, idempotent synthetic scenarios, validation before mutation and reset | Local process remains a prototype |
| Foreign policy or case fallback | single-value US request enum, validation before loader invocation, one active package, pinned corpus and no fallback | Source completeness and legal review remain open |
| Source substitution, stale data or hash drift | Exact URL/host/path allowlists, source class, separate dates, pinned hashes and fail-closed loader | Public pages may later change and require a new versioned refresh |
| Policy laundering | `REFERENCE_ONLY`, `NOT_ESTABLISHED`, `NOT_MADE`, warning-only result and explicit limitations | Full current-policy applicability is unverified |
| Prompt injection or source-content execution | Stage-only caller request, server-owned prompt contract and digest, fixed typed synthetic facts, opaque citation IDs, closed JSON Schema enums, no raw HTML, no caller model/config/path/schema/tool, disabled tools/function calling/retrieval/streaming and strict post-validation | A permitted enum can still be semantically poor; inventory review remains required whenever the sentence set changes |
| AI authority escalation | AI after deterministic preflight, fixed citations, server-stamped authority fields, no session mutation, no external action and human semantic review | One fixed-synthetic Gemini execution is accepted; repeatability, other stages and real-record behavior remain unverified |
| Model request flooding or denial of wallet | Atomic reserve before execution, three permanent process-local attempts, one per stage, failures count, no automatic retry, and no reset through session lifecycle | Process restart or another worker/instance creates another local budget; public deployment requires a durable shared quota and gateway cost circuit breaker |
| False Sandbox connection | Connected state only after a validated authentic receipt; mock and authentic evidence classes remain distinct | Dashboard identity, country and feature availability remain unknown until operator readback |
| Credential or token disclosure | Backend process environment only, fixed Sandbox host, no redirect, no frontend/token return, sanitized errors and no payload logging | Operator endpoint security remains outside the local prototype |
| Duplicate or uncertain invoice creation | One-shot review binding, idempotency where supported, no automatic retry after uncertain success, DRAFT-only scope | No separate GET readback is claimed |
| Provider-action expansion | Default-off outbound, exact endpoint/action allowlist and frozen send/payment/capture/refund/dispute mutation | Production is unavailable; Sandbox evidence submission needs the submit flag, a connected Sandbox and local approval |
| PII leakage | Synthetic default data, bounded allowlists, in-memory pseudonymization, no reverse map/raw log and manual review | Pattern detection is incomplete and is not legal anonymization |
| Evidence overclaim | Separate presence, authenticity, verification, sufficiency, eligibility and outcome states | A human can still misinterpret a draft; UI limitations remain mandatory |
| Dispute-authority confusion | Documented authority distinction and explicit statement that the current demo performs no provider-case routing | A real case requires current provider fields and an independently validated adapter |
| Procedural record promoted to merits | Source class `HISTORICAL_US_COURT_PROCEDURE`, explicit limitations and final-decision rejection | No complete official individual-outcome library exists |
| Sales spike signal promoted to fraud/AML | Local baseline provenance, backend-owned calculation and forbidden-label tests | Proprietary provider criteria are unavailable by design |
| Approval reuse or stale UI state | Case/action/payload digest, nonce, actor role, expiry, abort controllers and generation checks | Durable restart/concurrency authority remains open |
| Supply-chain and artifact drift | Locked dependencies, disabled npm lifecycle scripts, one writer, isolation diff, module audit and no-op readback | Full SAST, history scan and vendor review remain release gates |

## US Sandbox account boundary

The existing PayPal login is a Developer-login identity. The merchant role is a fictitious Business sandbox seller; the buyer role is a fictitious Personal sandbox account. These roles do not change or prove the live-account type.

The UI may say `PayPal Sandbox` before seller-country confirmation. It may say `US Business sandbox seller` only after trusted Dashboard confirmation. Invoicing availability also requires confirmation. The Sandbox host and browser locale are not country evidence.

The recorded Sandbox runs cover only their sanitized authentic results: on 2026-10-06 OAuth and one unsent invoice `DRAFT`; on 2026-10-31 OAuth, a second unsent `DRAFT` and a list and detail read of one author-created Sandbox test dispute ([masked receipt](../../evidence/RECEIPT_20261031_live.md)). Two gated `provide-evidence` sends followed, each to its own author-created Sandbox test dispute: 2026-11-04 ([masked receipt](../../evidence/RECEIPT_20261104_live.md)) and 2026-11-05 in UTC+8 ([masked receipt](../../evidence/RECEIPT_20261105_live.md)); none was made before 2026-11-04, and PayPal Sandbox accepting a request is not PayPal accepting the evidence. MockTransport results, screenshots and local UI state did not and cannot expand that accepted provider-evidence boundary.

## AUP boundary

The deterministic matcher can surface public US AUP categories and distinguish potential prohibited-category, prior-approval-category, ambiguous and no-local-match results. It cannot decide a violation, approval, legality or safety.

The second warning offers edit, cancel, or acknowledge and continue. Acknowledgement authorizes only a local next step and is revoked by content/session changes or expiry. Required-field validation may stop an incomplete local draft; the AUP warning itself is not a substitute PayPal block.

## Sales spike boundary

The public US User Agreement supports the narrow statement that rapidly increasing typical sales volume is one of several listed risk examples and that some criteria may be confidential. PayGuard does not know a provider threshold or hidden model.

The local signal cannot be labelled AML, fraud, money laundering or a predicted hold, limitation, reserve or release. Tracking may be relevant but cannot guarantee a provider action.

## Dispute boundary

The resolver runs on the closed synthetic sample cases in the session. With a Sandbox connection the merchant's Sandbox disputes are read in the same response shape, projected, listed and paired with a session case for the gated `provide-evidence` preview and send; the resolver does not run on them. Either response contains reason, status, lifecycle stage, seller-response due date, normalized available actions and evidence requests with source and action. Only exact `REQUESTED_FROM_SELLER` plus `PROVIDE_EVIDENCE` rows can create preparation tasks. It accepts only separately bound synthetic proof records and attachment bytes, and validates their signature, type and size; the bytes stay in expiring session memory, never reach the browser or the Internal Review ZIP, and are read again only for the gated multipart `provide-evidence` send. For the synthetic cases, raw provider case, order and request identifiers remain restricted server-side and the browser receives non-identifying references. A connected Sandbox read returns the Sandbox `dispute_id` and `seller_transaction_id` to the console, which needs them to show and pair that test case. The restricted digest is recomputed before reuse, AI eligibility and local approval so nested tampering fails closed. A real adapter must additionally retain current PayPal response options and HATEOAS links without treating them as action authority. Every fixture field remains explicitly synthetic, and a Sandbox row carries the label `Sandbox`.

PayGuard may prepare and pseudonymize a local draft. It provides evidence to PayPal only through the gated `provide-evidence` request (local reviewer approval, `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, a connected Sandbox and an explicit `submit: true`); it cannot send a message, make an offer, accept a claim, acknowledge a return, appeal, refund or adjudicate. Internal claims remain under PayPal authority; external disputes remain under the bank/card issuer's authority.

Counterfeit goods may be a Purchase Protection SNAD condition. SNAD is outside US Seller Protection. Photos are possible evidence, not a universal requirement.

## Data retention and privacy

- no real business or personal data enters the default sample data;
- queries and filters remain bounded in request memory and are not logged;
- session state expires and is not durable authorization;
- pseudonymization keys remain memory-only;
- provider credentials and tokens remain backend-memory only;
- provider records do not enter the synthetic pool;
- model calls cannot receive real case data under current authority;
- process-local model attempt reservations are not a production distributed rate limiter;
- no database, scheduler, cloud sync or public storage is enabled.

## Release blockers

- the recorded Gemini run: one fixed-synthetic response with human semantic review, with every broader model claim out of scope;
- durable authenticated review/submission authority;
- real PII lifecycle and retention;
- security, rights, public export and deployment acceptance.

The implementation must fail closed at the first schema, source, identity, privacy, evidence, authority or provider mismatch. Local validation cannot promote an external or release state.
