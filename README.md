# PayGuard AI

PayGuard is a US-only defensive buffer layer between merchant operations and provider review workflows for a PayPal Sandbox demonstration. It helps merchants review earlier, complete missing records, and prepare for provider review without making provider decisions. It presents one end-to-end story:

1. **Before a transaction:** surface a US Acceptable Use Policy warning before an invoice draft.
2. **During payment and fulfillment:** detect a local sales-velocity anomaly and prepare fulfillment evidence.
3. **After a transaction:** organize a dispute timeline and requested evidence for human review.

The console uses FastAPI, React, Tailwind and AG Grid Community. Its lazy-loaded analytics workspace combines a sortable and filterable AG Grid transaction stream with order, amount, currency and capture-time columns, three first-party evidence widgets, a single-open mobile evidence accordion and a deterministic local dashboard guide. Deterministic validation runs first. Optional AI creates bounded advisory summaries afterward. Humans control local workflow choices. PayPal retains final authority for PayPal policy, account and internal-dispute decisions; a bank or card issuer retains authority for an external dispute.

The active analytics dependency boundary is AG Grid Community under the MIT licence. No Commercial AG packages are part of the current frontend dependency or lock contract. The MIT license, contributor-rights attestation, third-party notices and exact export manifest travel with the public source package.

**Source release contract:** The complete repository run instructions below are the selected functional-demo path. A hosted demo URL is optional and unperformed. The default export mode creates `LOCAL_EXPORT_CANDIDATE_REVIEW_REQUIRED` with final-byte security review, independent red-team acceptance, repository visibility, video publication and Devpost submission still gated. After the repository source is published, the explicit `--published-source` mode records `PUBLIC_SOURCE_PUBLISHED` with only video publication and Devpost submission remaining. The published-source state covers source availability only. The English US-only synthetic implementation and its bounded Sandbox and optional AI paths do not prove provider telemetry, a separate GET, invoice sending, payment, repeatability, real-record behavior, policy correctness, provider retention behavior, public or production hosting, multi-user AI operation or production readiness.

## US Sandbox identity boundary

The demo target is the United States and the provider environment is PayPal Sandbox.

- The existing PayPal login is only the Developer-login identity.
- A fictitious Business sandbox account represents the merchant.
- A fictitious Personal sandbox account represents the buyer when needed.
- The operator's live-account type is not changed or inferred.
- A US merchant claim requires an operator-confirmed US Business sandbox seller.
- Any Invoicing evidence is limited to its separately reviewed bounded Sandbox path; this source package does not establish live-account or production eligibility.

Sandbox is a virtual test environment. It does not establish production eligibility, a US legal entity, current policy applicability or live-account behavior.

## Run locally

Required console prerequisites: Python 3.13, Node.js 20.19 or newer or Node.js 22.12 or newer, npm and uv. The Gemini profile is optional and separately requires Python 3.12. The optional local-model line requires a separately installed LM Studio server with the exact `nvidia-nemotron-3-nano-4b` model reachable only at `127.0.0.1:1234`. Run from the repository root. The project does not load `.env` files.

Windows users must run the POSIX `sh` commands in WSL 2; native Command Prompt and PowerShell runners are not supported.

The public console uses the official PayPal Sandbox REST APIs through its reviewed gateway. The optional Agent Toolkit dependency profile is excluded from this public package; no SDK installation is needed for the demonstrated flow. Start the local API with Python 3.13 using `./tools/run.sh api`.

```sh
python3.13 -m venv .venv
uv pip install --python .venv/bin/python3 -r requirements.lock
./tools/run.sh test
./tools/run.sh api
```

The Gemini profile is optional and is not required to start or judge the deterministic console. To validate it separately:

```sh
uv venv --python python3.12 integrations/gemini/.venv
uv pip sync integrations/gemini/requirements.lock --python integrations/gemini/.venv/bin/python3 --require-hashes
./tools/run.sh gemini-check
./tools/run.sh gemini-test
```

In a second terminal:

```sh
cd frontend
npm ci --ignore-scripts --no-audit --no-fund
npm run dev
```

Open `http://127.0.0.1:5173`. The API listens on `http://127.0.0.1:8000`, and Vite proxies `/api`. Stop each process with `Ctrl+C`. Missing runtime dependencies fail closed. API failure displays an error instead of switching to a hidden mock dataset.

See the [judge quickstart](docs/submission/quickstart.md) for the bounded walkthrough.

## Three-stage contract

### 1. US AUP preflight screen

PayGuard checks required product fields and deterministic terms against a pinned public US AUP reference. A match produces `REVIEW_SIGNAL`; no match produces `NO_MATCH`. Both retain `compliance_decision=NOT_MADE` and `current_policy_applicability=NOT_ESTABLISHED`.

When a warning appears, the merchant may edit, cancel, or acknowledge and continue to the ordinary provider-gated review. PayGuard does not declare the activity compliant, prohibited, legal, approved or safe. It never rewrites wording to evade a policy.

### 2. Fulfillment and velocity evidence readiness

PayGuard compares synthetic transaction counts and values with a declared local baseline and its preceding comparison window. It may produce `review_velocity`. The result is a local anomaly and evidence-readiness signal. It is not a PayPal risk score, AML finding, fraud finding or prediction of a hold, limitation, reserve or release.

Tracking, shipment and delivery information may be relevant evidence. They do not guarantee Seller Protection, early fund release, removal of a limitation or a dispute outcome.

### 3. Dispute evidence mediation

PayGuard resolves a closed synthetic provider-response fixture by its current reason, status, lifecycle stage, seller-response due date, available actions and evidence requests. Only exact `REQUESTED_FROM_SELLER` plus `PROVIDE_EVIDENCE` requests create seller requirements. It validates separately bound proof and attachment metadata, keeps raw provider identifiers and the restricted synthetic layer in expiring server-side session memory, exposes only non-identifying case/order/request references, creates a pseudonymized internal review copy and can package that safe projection into an integrity-checked Internal Review ZIP. The archive is local, excludes restricted originals and attachment bytes, and retains `NOT_PERFORMED`, `NOT_MADE` and human-review authority boundaries. The backend recomputes the restricted digest before reuse, optional AI eligibility or local approval. The runtime does not consume or mutate live PayPal disputes, persist real PII, or route cases between PayPal and bank or card issuers. A generic checklist never overrides the current provider response.

Evidence completeness is separate from authenticity, sufficiency, program eligibility and outcome. Counterfeit goods may be a Purchase Protection SNAD issue, while SNAD is outside US Seller Protection. Photos are optional evidence unless the current case specifically requests them.

## Official-reference profile

The active profile is `data/knowledge/payguard_us_official_v2/` and contains:

- 16 official source identities;
- 29 bounded English paraphrase chunks;
- three synthetic scenario cards for the three stages.

It includes official PayPal US policy pages, jurisdiction-neutral PayPal Developer documentation and two official U.S. court procedural records. Developer documentation is not US law. The court records describe allegations and procedural outcomes; they are not current policy or final individual merits findings. No reviewed official case proves that rapid sales growth alone caused an account limitation.

See the [official source register](docs/decisions/2026Q4/us_official_source_register.md) and [US mainline contract](docs/decisions/2026Q4/us_mainline_contract.md).

## Optional provider and model evidence

Outbound Sandbox access is disabled by default and requires the operator's explicit local opt-in. Credentials remain in the backend process environment and must never enter the repository, frontend, screenshots, prompts or reports.

The reviewed local records are operator-attested evidence limited to one bounded Sandbox OAuth result and one unsent USD `10.00` invoice `DRAFT`. They are not publicly reproducible from this source; a judge-facing execution claim requires showing that bounded path live with credentials kept off-screen. Invoice creation and invoice sending remain separate operations. A create response is not a separate GET readback. Production, invoice send, payment, capture, refund and dispute mutation remain frozen.

The optional Gemini path is bounded to fixed synthetic facts, pinned citation identities and no automatic retry. Its prior reviewed result is operator-attested and should be presented to a judge as an execution only when shown live; public source establishes the adapter contract, not an external run. The model cannot select jurisdiction, change deterministic results, establish policy applicability or authorize a provider action. No repeatability, other-stage quality, real-record behavior or production claim is made.

The current runtime adds a process-local denial-of-wallet guard around this optional path: three permanent attempt reservations total, one for each fixed stage. Disabled or invalidly configured AI requests do not consume a reservation. After enablement and deterministic context validation, reservation occurs atomically before the provider call; failures, timeouts, cancellation and invalid responses still consume the stage slot. Session reset, expiry and new sessions do not restore it. This is a local prototype control, not a production distributed quota. A public multi-worker or multi-instance deployment must use a durable shared atomic reservation store plus API-gateway rate and budget circuit breakers so restart, another worker or another instance cannot restore capacity.

The server-owned `payguard-bounded-advisory-v2` prompt contract accepts no caller prompt. It treats every value as data, uses only fixed synthetic facts and opaque pinned citation IDs, disables tools, function calling, streaming, external retrieval and automatic retry, and permits generated text only from stage-specific response-schema enums. Backend validation rechecks the exact prompt-contract digest, citation order, text inventory and authority fields after generation.

The AI integration is a dual-line adapter boundary. `./tools/run.sh api` keeps the existing default Gemini line. `./tools/run.sh local-ai-api` explicitly selects the default-off LM Studio line; it has no key, proxy, remote URL, caller-supplied model or automatic fallback. Both lines share the same stage-only request, prompt digest, closed text inventory, citation order, no-action fields and process-local three-attempt budget. The frontend accepts only the valid model/evidence pairs. The two providers are never called together.

The local line fixes the endpoint to `http://127.0.0.1:1234/v1/chat/completions`, the model to `nvidia-nemotron-3-nano-4b`, structured JSON output, `reasoning_effort=none`, no tools, one serialized in-flight inference and no retry. The public source contains structural and synthetic tests for this contract. It does not establish a live model run, model-weight identity, license clearance, public hosting, restart-safe quota, production readiness or real-record safety.

## Validation

Use the project-local runner and frontend build:

```sh
./tools/run.sh test
./tools/run.sh demo
./tools/run.sh evaluate
npm --prefix frontend run build
node tests/frontend_ai_contract.mjs
node tests/frontend_operator_labels.mjs
node tests/frontend_recording_contract.mjs
node tests/frontend_zip_contract.mjs
node tests/frontend_zip_api_parity.mjs
```

Optional Gemini-profile validation remains separate:

```sh
./tools/run.sh gemini-check
./tools/run.sh gemini-test
```

Local tests, screenshots and mock transports validate only their recorded runtime and source contracts. The export manifest carries the exact source-release state. These checks do not close video or submission gates, and they do not prove public or production hosting or multi-user AI operation.

## Architecture, privacy and release boundary

- [Current architecture and status](docs/decisions/2026Q4/architecture.md)
- [Console contract](docs/decisions/2026Q4/console_contract.md)
- [Policy engine contract](docs/decisions/2026Q4/policy_engine_v1.md)
- [Case intake contract](docs/decisions/2026Q4/case_intake_contract.md)
- [Threat model](docs/decisions/2026Q4/threat_model.md)
- [Standalone architecture/status visual](docs/decisions/2026Q4/payguard_us_architecture_status.svg)
- [Security policy](SECURITY.md)

The default dataset is synthetic and session-bound. Pseudonymization is not complete anonymization. Source publication does not establish a production tenant system, durable merchant authorization, real logistics integration, real dispute ingestion or cloud deployment.

The MIT license, contributor-rights attestation and third-party notices are present in the source package. The manifest distinguishes the default local-review state from the explicit published-source state. Demonstration-video upload and Devpost submission remain separate owner actions.
