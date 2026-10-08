# PayGuard Policy Engine v1 — US Advisory Contract

Status: design locked for the US-only warning funnel and `REFERENCE_ONLY` metadata runtime. A full declarative policy interpreter, effective-policy certification and enforced workflow tier remain pending.

## Non-negotiable invariants

1. The active jurisdiction is US.
2. Unsupported jurisdictions fail before policy package or corpus loading.
3. There is no cross-region fallback, union or “most restrictive country” substitution.
4. The active US package is statically pinned and loaded read-only.
5. A visible source update date is not an effective interval.
6. `current_policy_applicability` remains `NOT_ESTABLISHED`.
7. A deterministic AUP match produces a warning, not a compliance verdict.
8. The merchant may edit, cancel, or acknowledge and continue to ordinary provider-gated review.
9. AI runs only after deterministic validation and cannot change jurisdiction, rule output or authority.
10. No policy result authorizes a PayPal action, invoice send, payment, refund, dispute mutation or production call.

## Context contract

The resolver accepts a closed host-owned context:

```json
{
  "provider_account_region": "US",
  "merchant_legal_region": "UNKNOWN",
  "buyer_destination_region": "US",
  "issuer_region_signal": "UNKNOWN",
  "ip_country_signal": "UNKNOWN",
  "policy_domain": "AUP",
  "event_time": "2026-10-06T00:00:00Z"
}
```

This example is a schema illustration. It does not assert facts about the operator. `provider_account_region=US` is permitted only after trusted Dashboard confirmation. The Sandbox host, browser locale, currency, IP address and operator residence cannot establish it. A fictitious sandbox merchant is not a verified legal entity, so `merchant_legal_region` may remain `UNKNOWN`.

Auxiliary destination, issuer and IP signals do not choose the policy jurisdiction. A conflict produces a review signal rather than a geographic guess. Raw PAN, full BIN and raw IP do not enter the policy layer.

## Source package

The active package is a versioned US AUP reference profile under `policies/US/paypal_aup_reference_v1/`. It must bind:

- package ID and schema version;
- jurisdiction `US`;
- policy domain `AUP`;
- source ID and exact official URL;
- visible source update date and status;
- retrieval/observation time;
- unknown effective interval;
- file digests;
- tier `REFERENCE_ONLY`;
- no external-action authority.

The registry contains only the current US profile. Historical packages may remain as immutable evidence outside the active graph, but no request can resolve them.

## Loader boundary

The loader:

- uses fixed project-owned paths;
- performs no request-time dynamic import or expression evaluation;
- accepts no caller path, loader, root, hash, tier or approval override;
- rejects symlinks, FIFOs, directories, oversize files, duplicate JSON keys, non-finite values, unknown keys, schema drift and digest mismatch;
- validates the registry, manifest and source index before returning a detached read-only snapshot;
- fails closed without a last-minute foreign or stale fallback.

## Execution tiers

| Tier | Evaluation behavior | Local workflow effect |
| --- | --- | --- |
| `DISABLED` | Package is not loaded or evaluated | No output |
| `REFERENCE_ONLY` | Return validated source metadata and limitations | Human reference only; no verdict or workflow block |
| `SHADOW` | Future fixed-operator evaluation with audit output | No operator warning and no workflow effect |
| `ACTIVE_ADVISORY` | Future fixed-operator evaluation with visible warning | Human may review and continue under the warning-funnel contract |
| `ACTIVE_ENFORCED` | Future explicitly approved internal-workflow rule | May restrict a PayGuard-local action only; never freeze or control PayPal |
| `UNSUPPORTED` | No accepted active package/context | `MANUAL_REVIEW` or safe refusal; no fallback |

The current accepted runtime is `REFERENCE_ONLY` plus the separate deterministic warning-funnel slice. It is not `ACTIVE_ENFORCED` and does not execute a full rule package.

## Deterministic AUP preflight warning funnel

### Inputs

- required product fields;
- explicit US reference context;
- bounded description text;
- fixed category/term rules;
- current package identity and source metadata.

### Outputs

- `NO_MATCH` or `REVIEW_SIGNAL`;
- finding category and rule ID when matched;
- `compliance_decision=NOT_MADE`;
- `current_policy_applicability=NOT_ESTABLISHED`;
- official US AUP link;
- source date and limitations;
- expiry and description digest;
- `advisory_only=true`;
- `external_action_authorized=false`.

### Merchant choices

- `RETURN_TO_EDIT`
- `CANCEL`
- `ACKNOWLEDGE_AND_CONTINUE`

Acknowledgement is bound to the exact evaluation, description digest, session, role and expiry. It authorizes only the next local review step. Any edit, reset, session change or expiry revokes it.

### Forbidden interpretations

- A match is not a PayPal violation finding.
- A no-match is not compliance clearance.
- Rewording does not make an underlying activity compliant.
- Acknowledgement is not PayPal approval.
- The local engine cannot prevent, reverse or appeal an account action.

## Future declarative interpreter

A future full interpreter may use only a fixed allowlist of operators:

- `EQUALS`
- `IN`
- `NOT_IN`
- `CONTAINS_ANY`
- `AND`
- `OR`
- `GREATER_THAN`
- `IS_EFFECTIVE_BETWEEN`

Rules remain declarative JSON. No code, shell, template execution, regular-expression injection or caller-defined expression is permitted. Any addition requires a versioned schema, threat review, negative tests, signed approval metadata and isolation promotion.

## Time semantics

The engine keeps these dates separate:

- event time;
- evaluation time;
- retrieval/observation time;
- visible source update date;
- policy effective start/end when explicitly established;
- case filing or decision date;
- response deadline.

No field substitutes for another. Unknown stays unknown. A fresh observation does not establish a current effective interval.

## Conflict handling

Conflicts are domain-scoped. Product-policy context, shipment destination, issuer signal and IP signal remain separate. The reducer never selects a country by fuzzy matching and never merges incompatible regional policy packages.

Current outcomes include:

- `REFERENCE_METADATA_ONLY`
- `CONTEXT_CONFLICT`
- `PACKAGE_UNAVAILABLE`
- `SOURCE_INTEGRITY_FAILURE`
- `EFFECTIVE_INTERVAL_UNKNOWN`
- `MANUAL_REVIEW`

All preserve no-action authority.

## Audit record

Each accepted local evaluation should record only bounded metadata:

```json
{
  "evaluation_id": "bounded-generated-id",
  "jurisdiction": "US",
  "policy_domain": "AUP",
  "package_id": "current-pinned-package",
  "execution_tier": "REFERENCE_ONLY",
  "source_ids": ["PP-US-AUP"],
  "matched_rule_ids": [],
  "result": "REFERENCE_METADATA_ONLY",
  "current_policy_applicability": "NOT_ESTABLISHED",
  "compliance_decision": "NOT_MADE",
  "external_action_authorized": false
}
```

Do not store the raw description, credentials, provider token, private business data or caller-supplied authority claims in this audit structure.

## AI advisory boundary

AI may summarize fixed accepted synthetic facts and pinned citations after preflight. It cannot:

- select or infer jurisdiction;
- modify a deterministic match;
- claim legal or policy applicability;
- authenticate evidence;
- choose an external response;
- acknowledge a warning;
- create provider authority.

`BLK-02B` has one independently accepted fixed-synthetic `gemini-3.8-flash` response and human semantic review. A local mock or schema-valid fixture proves only the consumer contract, and the accepted invocation proves no repeatability, other-stage quality, policy correctness or real-record behavior.

## Promotion gate

Any tier change requires:

1. versioned package and schema;
2. exact source identities and digests;
3. established effective interval or an explicit unknown state compatible with the tier;
4. approver identity and approval time where required;
5. deterministic positive, negative, boundary and conflict tests;
6. source-integrity and foreign-before-load tests;
7. independent review;
8. isolation apply, module audit publication, second no-op audit and canonical readback;
9. unchanged external-action boundary.

The US narrative conversion is not a promotion event.

## Open work

- full fixed-operator interpreter;
- policy-effective interval governance;
- atomic reload and last-known-good lifecycle;
- durable audit and override authority;
- any model claim beyond the accepted one-execution `BLK-02B` boundary;
- provider behavior beyond the exact accepted `BLK-01B` evidence pair;
- legal review and public-release acceptance.

Until those gates pass, the engine remains an advisory warning and reference system.
