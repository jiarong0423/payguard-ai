# PayGuard Judge Quickstart

This walkthrough uses synthetic data and a US-only official-reference profile. It does not require a new outbound provider call. Any recorded provider or model evidence supports only its exact sanitized request and response.

For the competition recording sequence and exact opening narration, see [PayGuard AI Demonstration Script](video_script.md).

Status: the complete repository run instructions in this document are the selected functional-demo path. A hosted demo URL is optional and unperformed. The default export records `LOCAL_EXPORT_CANDIDATE_REVIEW_REQUIRED` with final-byte security review, independent red-team acceptance, repository visibility, video publication and Devpost submission still gated. After repository source publication, `--published-source` records `PUBLIC_SOURCE_PUBLISHED` with exactly video publication and Devpost submission remaining. Neither state establishes a public or production-hosted service.

## Start the console

From the repository root:

```sh
python3.13 -m venv .venv
uv pip install --python .venv/bin/python3 -r requirements.lock
uv venv --python python3.12 integrations/gemini/.venv
uv pip sync integrations/gemini/requirements.lock --python integrations/gemini/.venv/bin/python3 --require-hashes
./tools/run.sh test
./tools/run.sh gemini-check
./tools/run.sh gemini-test
./tools/run.sh api
```

In a second terminal:

```sh
cd frontend
npm ci --ignore-scripts --no-audit --no-fund
npm run dev
```

Open `http://127.0.0.1:5173`. Keep both processes running. If the API is unavailable, the UI fails visibly instead of loading a hidden mock.

This loopback walkthrough is the selected functional-demo path. It does not establish a public or production-hosted service.

## Understand the banner before the demo

The target market is the United States. The provider environment is PayPal Sandbox. The existing PayPal login is only the Developer-login identity. A fictitious Business sandbox account represents the merchant, and a fictitious Personal sandbox account represents the buyer when needed.

Any separately reviewed Sandbox proof must identify a US Business Sandbox seller and confirm Invoicing only for that bounded path. This source package does not establish the operator's live-account type or production eligibility. No credential should appear in the browser, repository, prompt, screenshot or report.

## Three-stage walkthrough

### Stage 1 — US AUP preflight screen

1. Open **US AUP Preflight Screen**.
2. Run the normal-product preset. Confirm the result is `NO_MATCH`, with no compliance clearance.
3. Run a preset that matches a review category. Confirm the result is `REVIEW_SIGNAL` and the official PayPal US AUP link is visible.
4. Open the second warning. Verify the three choices: **Return to edit**, **Cancel**, and **Acknowledge and continue**.
5. Acknowledge the warning and continue to the ordinary invoice-review step. Confirm that the result still says `NOT_MADE` and `NOT_ESTABLISHED`.
6. Edit the description. Confirm the previous acknowledgement is revoked and a new review is required.

Expected boundary: PayGuard surfaces a public-policy category and a warning. It does not declare the product compliant, prohibited, legal, approved or safe. It does not send an invoice.

### Stage 2 — Fulfillment and velocity evidence readiness

1. Open **Velocity and Fulfillment Readiness**.
2. Inspect the AG Grid table. Values come from the backend contract.
3. Inject the synthetic sales burst.
4. Confirm that the backend-calculated ratio and local baseline are displayed.
5. Inspect the declared baseline amount, `SYNTHETIC_BASELINE` provenance, preceding baseline window and the official US User Agreement reference.

Expected boundary: the signal means the synthetic activity exceeded a local demonstration baseline. It is not a PayPal threshold, risk score, AML finding, fraud finding or prediction of a hold, limitation, reserve or release. Tracking may be relevant evidence but cannot guarantee release or program eligibility.

### Stage 3 — Dispute evidence mediation

1. Open **Dispute Evidence Mediation**.
2. Inject the synthetic dispute and select the case.
3. Generate the local evidence draft.
4. Inspect the provider-response route, lifecycle status, seller-response due state and each current evidence requirement. Confirm that the fulfillment request is `REQUESTED_FROM_SELLER`, `PROVIDE_EVIDENCE` and `STRUCTURALLY_PRESENT`, and that only non-identifying case, order and requirement references are visible.
5. Inspect the restricted original summary. It must say session-memory only, no persistent vault, no returned content and no provider submission.
6. Download the standalone pseudonymized internal review copy and inspect its explicit `NOT_PERFORMED` provider-submission boundary.
7. Download the **Internal Review ZIP**. Confirm that its persistent warning says internal review only, incomplete official evidence, no original PayPal case data or attachment bytes, no provider submission and human review required. The fixed archive contains a README, manifest, response-driven requirements, timeline, public citations and the pseudonymized evidence document; it contains no raw case ID, order ID, request ID, identity token, session ID, draft digest, proof value, attachment name or attachment bytes.
8. Check the human-review box and record the local review.

Expected boundary: the draft remains local and synthetic. PayGuard does not submit evidence, message a buyer, make an offer, accept a claim, refund, appeal or adjudicate. PayPal decides escalated internal claims. A bank or card issuer decides an external dispute, with PayPal acting as intermediary.

## Sponsor analytics walkthrough

1. Open **Merchant Evidence Analytics** and select **Launch analytics**. The AG Grid Community workspace loads only after this explicit action.
2. Confirm that **Judge view** shows the three-stage lifecycle widget, the authority map, the session evidence pulse and the AG Grid transaction stream.
3. Use the quick-filter input, column sorting and column filters to inspect the synthetic rows. Confirm that row data remains synthetic and backend-owned workflow state is not recalculated by the grid.
4. Select **Inspect data** and verify that the transaction grid moves to the primary review position without changing row identity or backend state.
5. Use **What needs attention?**, **Explain authority** and **Summarize snapshot**. Confirm that the deterministic local guide performs no external request and cannot send an invoice, move money, submit evidence or decide an outcome.
6. On a mobile viewport, confirm that the single-column review summary replaces the desktop grid. Its single-open accordion starts on the three-stage lifecycle; opening item counts, the compact transaction preview or the authority map closes the prior section.

Expected boundary: the analytics workspace presents backend-owned synthetic state through AG Grid Community and first-party React components. The local guide never changes the AUP, velocity or dispute decisions. The exact source-release state comes from the export manifest; video publication and Devpost submission remain separate gates.

## Optional AI evidence brief

After deterministic preflight, each stage may expose **Generate AI evidence brief**. This action uses fixed synthetic facts and pinned citation identities. The expected output summarizes evidence and missing items while retaining:

- `compliance_decision=NOT_MADE`;
- `current_policy_applicability=NOT_ESTABLISHED`;
- `semantic_entailment=NOT_EVALUATED` until human review;
- `external_action_authorized=false`.

The UI validates closed model and evidence identity pairs. The default Gemini line uses `gemini-3.8-flash` with `SYNTHETIC_TEST_RESPONSE` or the separately evidenced `OPERATOR_LIVE_RESPONSE` class. The explicit local line uses `nvidia-nemotron-3-nano-4b` with `LOCAL_RUNTIME_RESPONSE`. Enum support in source does not prove an external execution. The backend launcher selects one line for the process; the browser cannot select a provider and no automatic fallback calls the other line. Neither identity authorizes a provider or workflow action.

## Public references and case caveat

The active source profile contains official PayPal US policy pages, jurisdiction-neutral Developer documentation and two official U.S. court procedural records. The court records describe settlement approval or arbitration procedure. They do not establish final individual merits, current policy or a provider threshold.

No reviewed official case proves that rapid sales growth alone caused an account limitation. The narrower supported statement is that the public US User Agreement lists rapidly increasing typical sales volume among multiple risk examples and says some criteria are confidential.

## Optional bounded Sandbox proof

Any `BLK-01B` proof remains external to this source package and must be operator-authorized, sanitized and independently reviewed. Its maximum scope is one Sandbox OAuth result plus one unsent USD `10.00` invoice `DRAFT` creation result.

- Use a fictitious Business sandbox seller for the merchant role.
- Confirm its country as US before calling it a US seller.
- Confirm Invoicing availability before attempting the draft.
- Keep outbound access off until the operator explicitly enables the bounded attempt.
- Do not retry an uncertain successful create automatically.
- Do not send the invoice or perform payment, capture, refund or dispute mutation.

Mock transport, screenshots and local UI state do not count as authentic provider evidence.

## Verification commands

```sh
./tools/run.sh test
./tools/run.sh demo
./tools/run.sh evaluate
./tools/run.sh gemini-check
./tools/run.sh gemini-test
cd frontend
npm run build
```

These commands validate the local runtime and source contract. The export manifest records the exact source-release state. No verification command authorizes a provider action.

## What the demo proves

- A deterministic warning funnel can surface public US AUP categories before an invoice draft.
- A backend calculation can show a local velocity anomaly against a declared synthetic baseline and preceding comparison window.
- A deterministic intake can organize a synthetic dispute and produce an integrity-checked internal review ZIP while preserving the correct adjudicator boundary.
- A bounded AI adapter can be placed after deterministic validation without receiving decision authority.

## What the demo does not prove

- The operator owns or qualifies for a US live account.
- A selected sandbox seller is US or Invoicing-enabled without readback.
- PayPal will approve a product, prevent a limitation, release funds or decide a dispute in a particular way.
- Evidence is authentic, sufficient or eligible merely because all local fields are complete.
- Authentic Sandbox execution, model repeatability, real-record model behavior, production readiness or public-submission readiness.
- Public or production hosting, restart-safe multi-user AI operation or a hosted-demo URL.

See the [current architecture](../decisions/2026Q4/architecture.md), [official source register](../decisions/2026Q4/us_official_source_register.md) and [US mainline contract](../decisions/2026Q4/us_mainline_contract.md).
