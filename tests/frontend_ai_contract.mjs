import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import { assertAiBrief, assertReferences, assertSandboxReceipt, REFERENCE_TYPES } from '../frontend/src/api.js';
import {
  REFERENCE_COMBINED_DIGEST,
  REFERENCE_CORPUS_ID,
  REFERENCE_ROWS,
  REFERENCE_SOURCE_DIGEST,
  REFERENCE_CHUNK_DIGEST,
} from '../frontend/src/referenceContract.js';
import { buildPseudonymizedEvidenceExport, downloadPseudonymizedEvidence } from '../frontend/src/pseudonymizedExport.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const rawChunks = readFileSync(resolve(projectRoot, 'data/knowledge/payguard_us_official_v2/chunks.jsonl'));
assert.equal(createHash('sha256').update(rawChunks).digest('hex'), REFERENCE_CHUNK_DIGEST);
assert.equal(
  createHash('sha256').update(`${REFERENCE_SOURCE_DIGEST}\n${REFERENCE_CHUNK_DIGEST}`, 'ascii').digest('hex'),
  REFERENCE_COMBINED_DIGEST,
);
const clone = (value) => structuredClone(value);
const request = { stage: 'source_compliance' };
const valid = {
  schema_version: '1.0',
  status: 'completed',
  stage: 'source_compliance',
  fixture_id: 'payguard-fixed-synthetic-brief-v1',
  context_digest: 'a'.repeat(64),
  corpus_digest: 'b'.repeat(64),
  model: 'gemini-3.8-flash',
  prompt_contract_id: 'payguard-bounded-advisory-v2',
  prompt_contract_digest: '2f870a865397a3e41a00bd51f85d96be5cce9ba77ad517d86d779dd3e15f2941',
  execution_evidence: 'SYNTHETIC_TEST_RESPONSE',
  brief: {
    summary: 'Synthetic evidence requires human review.',
    evidence_points: ['A deterministic signal exists.'],
    missing_evidence: ['Provider evidence is missing.'],
    citation_ids: ['PP-US-AUP-POLICY'],
  },
  ai_generated: true,
  advisory_only: true,
  human_review_required: true,
  compliance_decision: 'NOT_MADE',
  current_policy_applicability: 'NOT_ESTABLISHED',
  external_action_authorized: false,
  workflow_transition_authorized: false,
  semantic_entailment: 'NOT_EVALUATED',
  limitations: ['Fixed synthetic fixture.', 'Citation meaning is not verified.', 'No action is authorized.'],
};

assert.deepEqual(assertAiBrief(clone(valid), request), valid);
const validLocal = clone(valid);
validLocal.model = 'nvidia-nemotron-3-nano-4b';
validLocal.execution_evidence = 'LOCAL_RUNTIME_RESPONSE';
assert.deepEqual(assertAiBrief(clone(validLocal), request), validLocal);

const invalidGeminiLocalEvidence = clone(valid);
invalidGeminiLocalEvidence.execution_evidence = 'LOCAL_RUNTIME_RESPONSE';
assert.throws(() => assertAiBrief(invalidGeminiLocalEvidence, request));
const invalidLocalCloudEvidence = clone(validLocal);
invalidLocalCloudEvidence.execution_evidence = 'OPERATOR_LIVE_RESPONSE';
assert.throws(() => assertAiBrief(invalidLocalCloudEvidence, request));

const mutations = [
  (value) => { value.extra = true; },
  (value) => { value.stage = 'velocity_guard'; },
  (value) => { value.model = 'floating-model'; },
  (value) => { value.prompt_contract_id = 'caller-controlled'; },
  (value) => { value.prompt_contract_digest = '0'.repeat(64); },
  (value) => { value.execution_evidence = 'AUTHENTIC_SANDBOX_RESPONSE'; },
  (value) => { value.external_action_authorized = true; },
  (value) => { value.human_review_required = 1; },
  (value) => { value.brief.citation_ids = ['PP-FOREIGN-CITATION']; },
  (value) => { value.brief.evidence_points = []; },
  (value) => { value.brief.missing_evidence = Array(6).fill('missing'); },
  (value) => { value.brief.missing_evidence = []; },
  (value) => { value.brief.summary = 'x'.repeat(1201); },
  (value) => { value.limitations = ['only one']; },
  (value) => { value.limitations[0] = 'bad\ncontrol'; },
];
for (const mutate of mutations) {
  const value = clone(valid);
  mutate(value);
  assert.throws(() => assertAiBrief(value, request));
}

const receipt = {
  schema_version: 1,
  environment: 'sandbox',
  action: 'OAUTH_CONNECT',
  status: 'CONNECTED',
  observed_at: '2026-10-06T00:00:00Z',
  invoice_id: null,
  evidence_class: 'SYNTHETIC_TEST_RESPONSE',
  proof_kind: 'POST_RESPONSE_ONLY',
  separate_get_readback: false,
  external_send: 'FROZEN',
};
assert.deepEqual(assertSandboxReceipt(clone(receipt), 'OAUTH_CONNECT'), receipt);
const authentic = clone(receipt);
authentic.evidence_class = 'AUTHENTIC_SANDBOX_RESPONSE';
assert.deepEqual(assertSandboxReceipt(authentic, 'OAUTH_CONNECT'), authentic);
for (const mutate of [
  (value) => { value.evidence_class = 'OPERATOR_LIVE_RESPONSE'; },
  (value) => { value.proof_kind = 'GET_READBACK'; },
  (value) => { value.separate_get_readback = true; },
  (value) => { value.secret = 'forbidden'; },
]) {
  const value = clone(receipt);
  mutate(value);
  assert.throws(() => assertSandboxReceipt(value, 'OAUTH_CONNECT'));
}

const appSource = readFileSync(resolve(projectRoot, 'frontend/src/App.jsx'), 'utf8');
const apiSource = readFileSync(resolve(projectRoot, 'frontend/src/api.js'), 'utf8');
const referencePanelSource = readFileSync(resolve(projectRoot, 'frontend/src/ReferencePanel.jsx'), 'utf8');
const policyPanelSource = readFileSync(resolve(projectRoot, 'frontend/src/PolicyPanel.jsx'), 'utf8');
const operatorLabelsSource = readFileSync(resolve(projectRoot, 'frontend/src/operatorLabels.js'), 'utf8');
const analyticsSource = readFileSync(resolve(projectRoot, 'frontend/src/AnalyticsDashboard.jsx'), 'utf8');
const indexSource = readFileSync(resolve(projectRoot, 'frontend/index.html'), 'utf8');
const readmeSource = readFileSync(resolve(projectRoot, 'README.md'), 'utf8');
const architectureSource = readFileSync(resolve(projectRoot, 'docs/decisions/2026Q4/architecture.md'), 'utf8');
const consoleContractSource = readFileSync(resolve(projectRoot, 'docs/decisions/2026Q4/console_contract.md'), 'utf8');
const quickstartSource = readFileSync(resolve(projectRoot, 'docs/submission/quickstart.md'), 'utf8');
for (const required of [
  'Generate AI brief',
  'Uses only backend-fixed synthetic facts',
  'at most three model attempts per process and one attempt per stage',
  'AI brief generated',
  'aiControllerRef.current?.abort()',
  "stage=\"source_compliance\"",
  "stage=\"velocity_guard\"",
  "stage=\"dispute_mediation\"",
  'sandboxEvidenceLabel',
  'sandboxReadbackLabel',
  '{brief.model}',
  'data-testid="aup-applicability"',
  'data-testid="velocity-baseline"',
  'data-testid="dispute-scenario-match"',
  'Bound synthetic scenario',
  'DETERMINISTIC CASE MATCH',
  "aup?.match_status === 'REVIEW_SIGNAL' && !aupConsumed",
  "caseItem?.reason === 'INR' && draft?.evidence?.reason === 'INR' && draft?.routing?.overall_state === 'READY_FOR_LOCAL_REVIEW' && !draft?.review_reasons?.includes('unsupported_reason')",
  'data-testid="dispute-route"',
  'data-testid="dispute-due-state"',
  'data-testid="dispute-due-at"',
  'data-testid="dispute-actions"',
  'draft.routing?.seller_response_due_date',
  'operatorLabels(draft.routing?.available_actions)',
  'row.request_id',
  "operatorLabel(row.action, 'No action requested')",
  'data-testid="dispute-requirements"',
  'data-testid="restricted-original-summary"',
  'data-testid="internal-review-profile"',
  'data-testid="download-pseudonymized-evidence"',
  'Download review file',
  'Pseudonymized evidence file downloaded locally; no file was submitted to PayPal.',
]) assert.ok(appSource.includes(required), required);
for (const required of [
  'NOT_MADE',
  'No decision made',
  'NOT_ESTABLISHED',
  'Not established',
  'REQUESTED_FROM_SELLER',
  'Requested from seller',
  'PROVIDE_EVIDENCE',
  'Prepare evidence',
  'STRUCTURALLY_PRESENT',
  'Required fields present',
  'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  'Reference only · no action authorized',
  'PAYLOAD_DIGEST_BOUND',
  'Draft details locked for this review',
  'SEPARATE_READBACK_FALSE',
  'Verified from the creation response only',
  "fallback = 'Needs review'",
]) assert.ok(operatorLabelsSource.includes(required), required);
for (const forbidden of ['Sandbox OAuth returned authentic verification', 'Created an authentic Sandbox invoice draft']) {
  assert.equal(appSource.includes(forbidden), false, forbidden);
}
for (const forbidden of [
  '{invoice.invoice_id}',
  '{invoice.evidence_receipt.proof_kind}',
  'separate GET readback',
  'Backend payload digest bound',
  '{brief.prompt_contract_id}',
  '{brief.execution_evidence}',
  '{aup.compliance_decision}',
  '{aup.current_policy_applicability}',
  '{draft.routing?.overall_state}',
  '{row.requirement_state}',
]) assert.equal(appSource.includes(forbidden), false, forbidden);

const documentRedaction = {
  export_profile: 'INTERNAL_REVIEW_ONLY_V1',
  redacted_text: 'Order [MANUAL_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa] belongs to [NAME_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb].',
  replacement_count: 2,
  counts: { manual: 1, name: 1 },
  types: ['manual', 'name'],
  method: 'HMAC-SHA256 document pseudonymization v1',
  limited_detection: true,
  manual_review_required: true,
  source: 'synthetic',
  reversibility: false,
  limitations: ['Manual review is required.'],
};
const exportedEvidence = buildPseudonymizedEvidenceExport(documentRedaction);
assert.deepEqual(Object.keys(exportedEvidence), ['schema_version', 'export_profile', 'evidence_class', 'redacted_text', 'redaction', 'limitations', 'authority']);
assert.equal(exportedEvidence.redacted_text, documentRedaction.redacted_text);
assert.equal(exportedEvidence.authority.provider_submission, 'NOT_PERFORMED');
assert.equal(exportedEvidence.authority.dispute_decision, 'NOT_MADE');
for (const forbiddenKey of ['case_id', 'order_id', 'draft_digest', 'identity_redaction', 'session_id']) {
  assert.equal(JSON.stringify(exportedEvidence).includes(forbiddenKey), false, forbiddenKey);
}
for (const mutate of [
  (value) => { value.method = 'unknown'; },
  (value) => { value.export_profile = 'PAYPAL_SUBMISSION'; },
  (value) => { value.reversibility = true; },
  (value) => { value.counts.manual = 2; },
  (value) => { value.types = ['manual', 'unknown']; },
  (value) => { value.source = 'operator'; },
]) {
  const value = clone(documentRedaction);
  mutate(value);
  assert.throws(() => buildPseudonymizedEvidenceExport(value));
}
const originalDocument = globalThis.document;
const originalUrl = globalThis.URL;
const originalBlob = globalThis.Blob;
let downloadAnchorRemoved = false;
let downloadUrlRevoked = false;
try {
  globalThis.document = {
    createElement: () => ({
      click: () => { throw new Error('synthetic_download_click_failure'); },
      remove: () => { downloadAnchorRemoved = true; },
    }),
    body: { appendChild: () => {} },
  };
  globalThis.URL = {
    createObjectURL: () => 'blob:synthetic-pseudonymized-export',
    revokeObjectURL: () => { downloadUrlRevoked = true; },
  };
  globalThis.Blob = class SyntheticBlob {};
  assert.throws(
    () => downloadPseudonymizedEvidence(documentRedaction),
    /synthetic_download_click_failure/,
  );
  assert.equal(downloadAnchorRemoved, true);
  assert.equal(downloadUrlRevoked, true);
} finally {
  if (originalDocument === undefined) delete globalThis.document;
  else globalThis.document = originalDocument;
  globalThis.URL = originalUrl;
  globalThis.Blob = originalBlob;
}
assert.ok(readmeSource.includes('AG Grid transaction stream with order, amount, currency and capture-time columns'));
assert.equal(readmeSource.includes('custom review-state cells'), false);
assert.ok(architectureSource.includes('a four-column backend-supplied transaction stream'));
assert.equal(architectureSource.includes('custom review-state cells'), false);
assert.ok(consoleContractSource.includes('order, amount, currency and capture-time columns supplied by the backend'));
assert.equal(consoleContractSource.includes('custom backend-state cell'), false);
assert.ok(indexSource.includes('<title>PayGuard AI · Merchant Evidence Buffer</title>'));
assert.equal(indexSource.includes('Merchant Command Center'), false);
for (const required of ['MERCHANT EVIDENCE BUFFER', 'Three-stage evidence buffer', 'SYNTHETIC CAPTURES', 'AG Grid Community']) {
  assert.ok(appSource.includes(required), required);
}
assert.equal(appSource.includes('Backend-owned data'), false, 'operator view should not show the removed engineering badge');
for (const forbidden of ['MERCHANT COMMAND CENTER', 'Eight-layer architecture', 'Layer 8: Presentation']) {
  assert.equal(appSource.includes(forbidden), false, forbidden);
}
for (const column of [
  "field: 'order_id', headerName: 'Order'",
  "field: 'amount', headerName: 'Amount'",
  "field: 'currency', headerName: 'Currency'",
  "field: 'occurred_at', headerName: 'Captured at'",
]) {
  assert.equal(analyticsSource.split(column).length - 1, 1, column);
}
assert.equal(analyticsSource.includes('cellRenderer'), false, 'analytics grid must not claim a custom state cell');
for (const required of [
  'REVIEW ANALYTICS',
  'Review overview',
  'Transaction table',
  'AG Grid Community',
  'Built with AG Grid Community and first-party React components. Synthetic session data only.',
  'Session storage: temporary',
  'Review actions: local only',
  'quickFilterText={quickFilter}',
  'data-testid="analytics-lifecycle-widget"',
  'data-testid="analytics-authority-widget"',
  'data-testid="analytics-evidence-pulse-widget"',
  'data-testid="analytics-grid-widget"',
  'data-testid="analytics-guide-widget"',
]) {
  assert.ok(analyticsSource.includes(required), required);
}
for (const retired of [
  'AG GRID COMMUNITY · NO COMMERCIAL AG PACKAGES',
  'Open-source presentation boundary',
  'Judge view',
  'Inspect data',
  'Persistence: memory session',
]) {
  assert.equal(analyticsSource.includes(retired), false, retired);
}
assert.ok(apiSource.includes("path === '/ai/evidence-brief' ? 65000 : 15000"));
for (const required of ['**Synthetic baseline**', '`compliance_decision=NOT_MADE`', '`current_policy_applicability=NOT_ESTABLISHED`']) {
  assert.ok(quickstartSource.includes(required), required);
}
for (const forbidden of ['missing fulfillment evidence', 'lifecycle fields, chronology, evidence items, missing fields']) {
  assert.equal(quickstartSource.includes(forbidden), false, forbidden);
}

const referenceRequest = {
  query: 'acceptable use',
  theme: 'source_compliance',
  jurisdiction: 'US',
  case_stage: 'any',
  material_types: [...REFERENCE_TYPES],
  limit: 3,
  require_known_source_date: false,
};
const referenceEnvelope = {
  schema_version: 1,
  status: 'references_found',
  corpus_id: REFERENCE_CORPUS_ID,
  corpus_digest: REFERENCE_COMBINED_DIGEST,
  corpus_digests: { sources_sha256: REFERENCE_SOURCE_DIGEST, chunks_sha256: REFERENCE_CHUNK_DIGEST },
  filters_applied: {
    theme: 'source_compliance', jurisdiction: 'US', case_stage: 'any', material_types: [...REFERENCE_TYPES].sort(), limit: 3,
    require_known_source_date: false, max_source_age_days: null, age_basis: 'source_updated_date_utc_calendar', as_of: null,
  },
  results: [{ ...REFERENCE_ROWS['PP-US-AUP-POLICY'], relevance_score: 1 }],
  limitations: ['References are advisory and authorize no action.'],
  advisory_only: true,
  operational_authority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  source: 'public_reference',
};
assert.deepEqual(assertReferences(clone(referenceEnvelope), referenceRequest), referenceEnvelope);
for (const mutate of [
  (value) => { value.corpus_id = 'retired-corpus'; },
  (value) => { value.corpus_digests.sources_sha256 = '0'.repeat(64); },
  (value) => { value.results[0].text = 'Tampered summary.'; },
  (value) => { value.results[0].url = 'https://example.com/untrusted'; },
  (value) => { value.results[0].case_outcome = 'FINAL_MERITS'; },
]) {
  const value = clone(referenceEnvelope);
  mutate(value);
  assert.throws(() => assertReferences(value, referenceRequest));
}
assert.throws(() => assertReferences(clone(referenceEnvelope), { ...referenceRequest, jurisdiction: 'CA' }));
assert.equal(referencePanelSource.includes('reference-region-'), false);
assert.equal(policyPanelSource.includes('policy-region-'), false);
const nonEnglishCjkPattern = /[\u3400-\u9fff]|[\uFF1A\uFF0C\u3002\uFF08\uFF09]/u;
const retiredRegionPattern = new RegExp(`\\b(?:${'T' + 'W'}|${'U' + 'K'})\\b`, 'u');
for (const [name, source] of [['App', appSource], ['API', apiSource], ['Reference panel', referencePanelSource], ['Policy panel', policyPanelSource]]) {
  assert.equal(nonEnglishCjkPattern.test(source), false, `${name} contains non-English CJK text or punctuation`);
  assert.equal(retiredRegionPattern.test(source), false, `${name} contains a retired jurisdiction token`);
}

console.log(JSON.stringify({ status: 'PASS', ai_mutations: mutations.length, sandbox_mutations: 4, reference_mutations: 6, source_checks: 49 }));
