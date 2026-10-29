# PayGuard AI

A merchant may notice a policy warning, a sudden sales spike, or a dispute only after the records have become difficult to assemble. PayGuard AI is a **merchant defense buffer layer**: it helps the merchant identify evidence gaps early and prepare evidence, while keeping every decision with the merchant and the relevant payment provider.

This is a US-only, synthetic-data PayPal Sandbox demonstration with one end-to-end merchant workflow:

**At a glance:** AUP warning before a draft → sales-velocity evidence review → dispute evidence ZIP and optional AI brief. The merchant checks each step; PayPal or the applicable issuer keeps the final decision.

**Working stack:** PayPal Sandbox OAuth, an unsent invoice draft and read-only Disputes readback · FastAPI and deterministic rules · React, Tailwind and AG Grid Community · optional bounded Gemini on Vertex AI.

**Verified once against the real Sandbox:** on 2026-10-07 the gateway authenticated with OAuth client-credentials and created one unsent USD 10.00 invoice draft, Sandbox id `INV2-2MTA-PRPQ-4CAJ-W5UW`, status `DRAFT`. `./tools/run.sh test` runs 436 tests (2 skipped) in about eight seconds.

**Website / video:** [youtu.be/K28N9QhRp1E](https://youtu.be/K28N9QhRp1E) (2:02) · **Devpost:** [devpost.com/software/payguard-ai-zbsp9l](https://devpost.com/software/payguard-ai-zbsp9l)

| What the console does | PayPal call | Real or fixture |
| --- | --- | --- |
| Connect the merchant | `POST /v1/oauth2/token` (client-credentials) | Real Sandbox call |
| Unsent invoice draft after the AUP preflight | `POST /v2/invoicing/invoices` | Real Sandbox call, status `DRAFT`, never sent |
| Webhook signature check | `POST /v1/notifications/verify-webhook-signature` | Real endpoint, exercised with recorded fixtures in tests |
| Read the merchant's dispute list (STEP 03) | `GET /v1/customer/disputes` | Real Sandbox call when connected; otherwise a synthetic fixture in the same JSON shape, labelled **Fixture data** in the UI |
| Read one dispute | `GET /v1/customer/disputes/{id}` | Real Sandbox call when connected; otherwise the fixture |
| Assemble the evidence response | `POST /v1/customer/disputes/{id}/provide-evidence` | Multipart request is built and previewed from the local draft for a dispute id the console itself returned; it is sent only after the local review approval, with `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, a Sandbox connection and an explicit `submit: true` |
| Sales-velocity stream, dispute checklist, evidence ZIP | none | Local synthetic data by design |

![Concept illustration of a merchant reviewing AUP warnings, sales velocity and dispute evidence with PayGuard AI](docs/submission/payguard_cover.png)

*Synthetic merchant-side cover illustration. The working console is designed to demonstrate the Sandbox, AG Grid, and bounded Gemini actions live; the cover is not a product screenshot.*

![PayGuard AI workflow map: policy warning, sales-velocity review, and dispute evidence preparation](docs/submission/payguard_judge_overview.png)

*Three-stage workflow map for the US-only synthetic demo; rules and merchants guide local actions, while PayPal and issuers retain final authority.*

## Architecture and tools at a glance

**What PayGuard does well:** one merchant-side path covers policy warning, sales-velocity review and dispute preparation. Deterministic checks make each signal inspectable; AG Grid makes transaction evidence usable; the ZIP and optional Gemini brief help a person review without claiming an outcome.

```mermaid
flowchart TB
    A["01 AUP preflight<br/>FastAPI deterministic warning"] --> H1["Merchant edits, cancels or acknowledges"]
    H1 -->|Only after acknowledgment| S["PayPal Sandbox OAuth<br/>unsent invoice draft"]
    S --> B["02 Velocity readiness<br/>Backend signal + AG Grid review"]
    B --> C["03 Dispute evidence<br/>Internal Review ZIP + optional Gemini"]
    C --> H2["Merchant reviews the evidence"]
    H2 -.->|Final decision stays outside PayGuard| P["PayPal or bank / card issuer"]
```

| Part | What the judge can see | Responsibility and limit |
| --- | --- | --- |
| PayPal Sandbox | OAuth connection, one unsent invoice draft and read-only dispute readback | Provider test environment; no payment, invoice send or dispute mutation unless the submit flag is set |
| FastAPI + deterministic rules | AUP warning, local sales-baseline comparison, current-case evidence requests | Produce review signals before any optional AI brief |
| React + Tailwind + AG Grid Community | Merchant console and sortable, filterable transaction evidence | Show the three stages and let a human inspect the records |
| Optional Gemini on Vertex AI | Bounded evidence brief from fixed synthetic facts and pinned citations | Suggest what to review; no submission or decision authority |
| Internal Review ZIP | Pseudonymized evidence copy | Download for human review; not a PayPal submission package |

![PayGuard AI eight-layer system architecture showing the three merchant stages, deterministic checks, UI, optional AI and provider authority boundaries](docs/decisions/2026Q4/payguard_us_architecture_status.svg)

*System architecture. The diagram separates merchant actions, deterministic checks, optional AI and PayPal or issuer authority.*

The [judge quickstart](docs/submission/quickstart.md) walks through the working console; the [editable workflow diagram](docs/submission/payguard_judge_overview.svg) and [detailed architecture diagram](docs/decisions/2026Q4/payguard_us_architecture_status.svg) show the review and implementation boundaries.

Watch the [2:02 public demonstration](https://youtu.be/K28N9QhRp1E) and the [submitted Devpost project](https://devpost.com/software/payguard-ai-zbsp9l). The [submitted project story](docs/submission/devpost_story.md) preserves the current Devpost wording. It shows the synthetic merchant workflow; the [recording script](docs/submission/video_script.md) preserves the longer pre-edit timing plan.

1. **Before a draft — AUP preflight:** use pinned PayPal US AUP references and deterministic rule checks to surface a warning; after merchant review, PayPal Sandbox OAuth supports one unsent invoice draft.
2. **During fulfillment — velocity readiness:** use a backend comparison against a declared local baseline to flag synthetic sales spikes (fifty captures with varied amounts between USD 4.50 and 18.00, totalling 500.00 against a 100.00 per hour baseline); AG Grid Community lets reviewers sort, filter and select the transaction evidence.
3. **After a dispute — evidence preparation:** read the merchant's disputes through the PayPal Disputes API (Sandbox when connected, fixture otherwise), match the current synthetic case's requested seller items, produce a pseudonymized Internal Review ZIP, preview the multipart `provide-evidence` request and, on request, a bounded Gemini evidence brief for human review.

The console uses FastAPI, React, Tailwind and AG Grid Community. Its lazy-loaded analytics workspace combines a sortable and filterable AG Grid transaction stream with order, amount, currency and capture-time columns, three first-party evidence widgets, a single-open mobile evidence accordion and a deterministic local dashboard guide. Deterministic validation runs first. Optional AI creates bounded advisory summaries afterward. Humans control local workflow choices. PayPal retains final authority for PayPal policy, account and internal-dispute decisions; a bank or card issuer retains authority for an external dispute.

The active analytics dependency boundary is AG Grid Community under the MIT licence. No Commercial AG packages are part of the current frontend dependency or lock contract. The MIT license, contributor-rights attestation, third-party notices and exact export manifest travel with the public source package.

**Release status:** the Devpost project is submitted and the 2:02 demonstration is public. The complete repository run instructions below are the functional-demo path; a hosted demo URL is optional and unperformed (hosting was not part of this entry). The default run uses synthetic data and needs no credentials.

## US Sandbox identity boundary

The demo target is the United States and the provider environment is PayPal Sandbox.

- The existing PayPal login is only the Developer-login identity.
- A fictitious Business sandbox account represents the merchant.
- A fictitious Personal sandbox account represents the buyer when needed.
- The operator's live-account type is not changed or inferred.
- A US merchant claim requires an operator-confirmed US Business sandbox seller.
- The Invoicing evidence is one authenticated Sandbox run on 2026-10-07 (OAuth + one unsent USD 10.00 draft, `INV2-2MTA-PRPQ-4CAJ-W5UW`). Production accounts were out of scope by design.

Scope: a fictitious US Business Sandbox seller. Production eligibility and live-account behaviour were not tested.

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

Each stage loads its synthetic scenario when you open it: STEP 02 loads the fifty-capture sales burst and STEP 03 loads the dispute case and the provider dispute readback. The **Load** buttons remain for reloading; loading again never duplicates records. The fixture disputes use dates relative to the request time (response due in 7 and 5 days), so they never show as expired.

### Turning on PayPal

The console runs without any key. To exercise the real Sandbox calls, export these variables in the terminal that starts `./tools/run.sh api`, using a Sandbox REST app from your own PayPal Developer Dashboard:

```sh
export PAYGUARD_PAYPAL_OUTBOUND=enabled
export PAYPAL_CLIENT_ID=...          # Sandbox app client id
export PAYPAL_CLIENT_SECRET=...      # Sandbox app secret
./tools/run.sh api
```

Then expand **Optional PayPal US Sandbox connection** in STEP 01 and select **Connect US Sandbox**. After the OAuth receipt shows, STEP 03 reads `GET /v1/customer/disputes` from that account and labels the rows **Sandbox data**. The `provide-evidence` request stays a preview unless you also export `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`, record the local review approval for the case and submit with the console's gated button (or `submit: true` on the API). An id the console did not return, or a case without approval, is refused (404 or 422). The console never sets that flag for you. The project does not read `.env` files, and credentials never reach the browser, logs or evidence files.

### Turning on Gemini

Without the Gemini profile, **Generate AI brief** shows "Gemini profile not configured" instead of a brief. To enable it, create the Python 3.12 profile shown below, set `PAYGUARD_GEMINI_OUTBOUND=enabled` together with your Vertex AI project through Application Default Credentials in the API terminal, and restart `./tools/run.sh api`. `./tools/run.sh gemini-check` validates the profile without calling the model.

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

Operator-attested Sandbox evidence: at 2026-10-06 17:44 UTC (2026-10-07 in UTC+8) one run under the operator's own US Business Sandbox app completed an OAuth client-credentials request and created one unsent USD `10.00` invoice (Sandbox id `INV2-2MTA-PRPQ-4CAJ-W5UW`, status `DRAFT`), with no send, payment, capture, refund or retry. The receipt is a local operator record. To replay the Sandbox path yourself, set `PAYGUARD_PAYPAL_OUTBOUND=enabled` with your own Sandbox app credentials (see "Turning on PayPal" above); the fixture mode shows the same three stages without any key. Invoice creation and invoice sending remain separate operations. I did not issue a GET for the invoice after creating it. Production, invoice send, payment, capture and refund remain frozen; dispute evidence submission is a separate opt-in (`PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`) and is off by default.

The optional Gemini path is bounded to fixed synthetic facts, pinned citation identities and no automatic retry. The Gemini brief was run once against Vertex AI `gemini-3.8-flash` by the operator; to reproduce it you need your own Vertex AI project (see "Turning on Gemini"). The model cannot select jurisdiction, change deterministic results or authorize a provider action, and the console runs without it.

The current runtime adds a process-local denial-of-wallet guard around this optional path: three permanent attempt reservations total, one for each fixed stage. Disabled or invalidly configured AI requests do not consume a reservation. After enablement and deterministic context validation, reservation occurs atomically before the provider call; failures, timeouts, cancellation and invalid responses still consume the stage slot. Session reset, expiry and new sessions do not restore it. This is a local prototype control, not a production distributed quota. A public multi-worker or multi-instance deployment must use a durable shared atomic reservation store plus API-gateway rate and budget circuit breakers so restart, another worker or another instance cannot restore capacity.

The server-owned `payguard-bounded-advisory-v2` prompt contract accepts no caller prompt. It treats every value as data, uses only fixed synthetic facts and opaque pinned citation IDs, disables tools, function calling, streaming, external retrieval and automatic retry, and permits generated text only from stage-specific response-schema enums. Backend validation rechecks the exact prompt-contract digest, citation order, text inventory and authority fields after generation.

The AI integration is a dual-line adapter boundary. `./tools/run.sh api` keeps the existing default Gemini line. `./tools/run.sh local-ai-api` explicitly selects the default-off LM Studio line; it has no key, proxy, remote URL, caller-supplied model or automatic fallback. Both lines share the same stage-only request, prompt digest, closed text inventory, citation order, no-action fields and process-local three-attempt budget. The frontend accepts only the valid model/evidence pairs. The two providers are never called together.

The local line fixes the endpoint to `http://127.0.0.1:1234/v1/chat/completions`, the model to `nvidia-nemotron-3-nano-4b`, structured JSON output, `reasoning_effort=none`, no tools, one serialized in-flight inference and no retry. The public source contains structural and synthetic tests for this contract. The Gemini brief was exercised against Vertex AI `gemini-3.8-flash` in a single operator-run call (no retry); it is optional, bounded to fixed synthetic facts, and the console runs without it.

## Validation

**Public package versus the private export.** The project's private working export also ran two local-only test files, `tests/test_governance.py` and `tests/test_submission_readiness.py`, which check export tooling, module registries and release receipts that are not part of this repository. They account for the 471 count quoted in earlier notes; the public package does not contain them. The number you can reproduce from this repository is the one `./tools/run.sh test` prints (436 tests, 2 skipped).

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

Measured scope: `./tools/run.sh test` runs 436 tests (2 skipped) against synthetic data, mocked transports and the built-in fixture; the Sandbox calls are covered by one operator-run receipt (2026-10-07) and by MockTransport tests. Not covered: multi-instance or hosted operation and real-record behaviour.

## Architecture, privacy and release boundary

- [Current architecture and status](docs/decisions/2026Q4/architecture.md)
- [Console contract](docs/decisions/2026Q4/console_contract.md)
- [Policy engine contract](docs/decisions/2026Q4/policy_engine_v1.md)
- [Case intake contract](docs/decisions/2026Q4/case_intake_contract.md)
- [Threat model](docs/decisions/2026Q4/threat_model.md)
- [Standalone architecture/status visual](docs/decisions/2026Q4/payguard_us_architecture_status.svg)
- [Security policy](SECURITY.md)

The default dataset is synthetic and session-bound. Pseudonymization is not complete anonymization. What is in this release: the three-stage console, 436 tests, the Sandbox gateway (OAuth, unsent invoice draft, Disputes readback, gated provide-evidence) and the fixture data. What is not: multi-tenant auth, logistics feeds, automatic dispute ingestion, cloud deployment.

The MIT license, contributor-rights attestation and third-party notices are present in the source package. The manifest distinguishes the default local-review state from the explicit published-source state. The demonstration video is public; the Devpost project is submitted. Later source revisions require fresh release review.
