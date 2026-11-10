# TradeGlot Mainline Contract (US Sandbox seller; the optional ten-country rules check is advisory)

> Update 2026-11-10: the current video is the 2:59 cut (https://youtu.be/o0A-zj2_1rc); "the 2:50 video" below means the earlier cut. Six evidence sends are recorded now: five from the local console and one from the hosted demo on 2026-11-10 (see README "Real vs simulated" and `docs/evidence/RECEIPT_20261110_hosted_live.md`). The rest of this file is the design record as dated.

Status: current accepted canonical local design for a US Sandbox seller; the optional ten-country rules check is advisory. The English conversion and three-stage contract are current. Real PayPal Sandbox runs: OAuth and unsent invoice drafts (2026-10-06, 2026-10-31 and one during the video recording on 2026-11-05, UTC+8), dispute list and detail reads (2026-10-31) and two gated `provide-evidence` sends, each to its own author-created test dispute (2026-11-04 and 2026-11-05 in UTC+8; see "Sandbox contract"). One recorded fixed-synthetic `gemini-3.8-flash` result is from 2026-10-06. Each is a record of its own captured execution. They do not prove current-byte live behavior or bind a later source candidate. A judge-facing execution claim requires showing the bounded path live. This contract supersedes prior product narratives for the active runtime; historical evidence retains its original claims and bytes. The Devpost project is submitted; later source revisions retain a separate release gate.

Current objective state: the local product baseline is `O (Done)`. Release state is determined by the package manifest and exact anonymous public readback, not by this contract or a historical receipt. When the manifest is `PUBLIC_SOURCE_PUBLISHED` with `publication_authorized=true` and the same bytes pass exact anonymous readback, public source publication is complete. In that published-source state, the Devpost project is submitted; the 2:50 demonstration is already public. A package marked `LOCAL_EXPORT_CANDIDATE_REVIEW_REQUIRED` has not crossed the public-source gate. A hosted demo is optional and is not mandatory.

## Locked product statement

TradeGlot is an advisory console for a PayPal Sandbox merchant journey of a US Sandbox seller; the optional ten-country rules check is advisory. It applies deterministic validation before AI and presents three stages:

1. US AUP warning before an invoice draft;
2. sales spike and fulfillment evidence readiness;
3. dispute evidence mediation after a transaction.

The product is an interception and evidence-preparation funnel. It does not replace PayPal review. Humans control local edit, cancel, acknowledge and review actions. PayPal retains final authority for PayPal policy, account and internal-dispute decisions. A bank or card issuer retains authority for an external dispute.

## Functional demonstration contract

The functional-demo requirement can be satisfied by complete repository run instructions or by a hosted demo URL. This candidate selects the repository-instructions path in `README.md` and `docs/submission/quickstart.md`. The optional hosted-demo path is unperformed. This selection establishes neither public nor production hosting and does not expand the local process-bound AI control into a multi-user or multi-instance deployment.

## Provider identity

- `demo_market=US`
- `provider_environment=PAYPAL_SANDBOX`
- `developer_login_identity=EXISTING_PAYPAL_ACCOUNT`
- `sandbox_merchant_role=BUSINESS`
- `sandbox_buyer_role=PERSONAL` when required
- `provider_account_region=US` only after trusted Dashboard confirmation
- `merchant_legal_region=UNKNOWN` for a fictitious sandbox merchant
- `external_action_authorized=false` by default

The existing login is not converted or described as a live Business account. A Business sandbox seller is a virtual merchant persona. Operator-visible country and Invoicing confirmation exists only in the recorded Sandbox run for its captured execution and does not establish current-byte behavior, live-account status or production eligibility.

## Policy and source state

The active policy reminder is the official PayPal US Acceptable Use Policy. The profile remains `REFERENCE_ONLY`. A visible page update date is stored separately from the unknown effective interval.

- `current_policy_applicability=NOT_ESTABLISHED`
- `compliance_decision=NOT_MADE`
- `external_action_authorized=false`
- unsupported jurisdictions fail before load
- no cross-region fallback exists

The active corpus contains official PayPal US policy summaries, jurisdiction-neutral PayPal Developer guidance and official U.S. court procedural summaries. Developer guidance is not US law. Court procedure is not current policy, an individual merits result or training truth.

## Stage outcomes

| Stage | Local output | Human choice | External authority |
| --- | --- | --- | --- |
| US AUP warning | `NO_MATCH` or `REVIEW_SIGNAL`; source and limitations | Edit, cancel, acknowledge and continue | PayPal |
| Sales spike readiness | Local baseline ratio, provenance and window; `review_velocity` when the local threshold is exceeded | Inspect capacity and prepare records | PayPal |
| Dispute mediation | Reason-bound chronology, requested-evidence draft and review flags; no provider-case routing | Review local draft | PayPal or the bank/card issuer, according to the actual external process |

No stage produces approval, prohibition, hidden provider risk, evidence authenticity, program eligibility, outcome prediction or financial action.

## AI contract

AI receives only accepted structured synthetic facts and pinned citations after deterministic preflight. It may summarize facts, chronology, missing evidence and limitations. It cannot select jurisdiction, add facts, resolve conflicts, authenticate evidence, change a rule result, acknowledge a warning or choose a provider action.

The recorded Gemini run is limited to one human-reviewed `gemini-3.8-flash` response over fixed synthetic facts. The receipt (raw responses are not stored in this repository) records one captured invocation, no automatic retry and no workflow or external-action authority. It does not establish current-byte live behavior, repeatability, other-stage quality, real-record behavior, provider retention behavior, policy correctness or production readiness.

## Sandbox contract

Outbound access is disabled by default. The recorded Sandbox run of 2026-10-06 is limited to the OAuth result and one unsent USD `10.00` invoice `DRAFT` creation result using the operator-confirmed US Business sandbox seller path with Invoicing available. It proves only that captured execution, not current-byte live behavior. Public source alone does not authenticate the result.

A second run on 2026-10-31 repeated OAuth and one unsent invoice `DRAFT` and read one author-created Sandbox test dispute (list and detail; [masked receipt](../../evidence/RECEIPT_20261031_live.md)). When a Sandbox app is connected the console reads the seller's Sandbox disputes. The `provide-evidence` request is sent only behind a recorded local approval, `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, an explicit `submit: true` and the server's single-use send confirmation. Six sends went out this way (five local, one hosted; see README "Real vs simulated"), the first two as follows: on 2026-11-04 to an author-created Sandbox test dispute ([masked receipt](../../evidence/RECEIPT_20261104_live.md)) and on 2026-11-05 (UTC+8) to a newly filed one ([masked receipt](../../evidence/RECEIPT_20261105_live.md)); already-answered, different-reason and different-amount disputes were refused. PayPal Sandbox accepting a request is not PayPal accepting the evidence.

Invoice send, payment, capture, refund, dispute mutations other than that gated request, production and automatic retry after uncertain creation remain frozen. A create response is not described as a separate GET readback.

## Public-case limitation

The active official U.S. court records establish settlement approval or arbitration procedure and preserve historical allegations. They do not establish current policy, final individual merits, a rapid-volume-only trigger or a provider threshold. The supported sales spike story comes from the public US User Agreement's risk examples, with confidential-model limitations preserved.

## Readiness

Local code, tests, source integrity and rendered UI can establish only local contract behavior. They cannot establish:

- the operator's Dashboard access;
- sandbox seller country or Invoicing entitlement beyond the recorded Sandbox run;
- Sandbox or model behavior beyond the recorded Sandbox and Gemini executions;
- current legal completeness;
- production readiness;
- public or production hosting or restart-safe multi-user AI operation;
- Devpost submitted-state evidence; the 2:50 video is public, while every candidate's public repository readiness requires its own matching manifest and exact anonymous readback. A historical anonymous readback applies only to its captured bytes.

Canonical state remains governed by `config/module_registry.json` and `config/missing_registry.json`. No document closes a gap.

See [architecture](architecture.md), [source register](us_official_source_register.md), [policy engine](policy_engine_v1.md), [case intake](case_intake_contract.md), [console contract](console_contract.md), [threat model](threat_model.md) and the [architecture overview diagram](../../submission/diagrams/architecture_overview.svg).
