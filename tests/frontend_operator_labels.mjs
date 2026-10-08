import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  OPERATOR_LABELS,
  operatorLabel,
  operatorLabels,
  sandboxReadbackLabel,
} from '../frontend/src/operatorLabels.js';

const required = {
  NOT_MADE: 'No decision made',
  NOT_ESTABLISHED: 'Not established',
  REQUESTED_FROM_SELLER: 'Requested from seller',
  PROVIDE_EVIDENCE: 'Prepare evidence',
  STRUCTURALLY_PRESENT: 'Required fields present',
  REFERENCE_ONLY_NO_ACTION_AUTHORIZATION: 'Reference only · no action authorized',
  READY_FOR_LOCAL_REVIEW: 'Ready for human review',
  INCOMPLETE_POLICY_EVIDENCE: 'Policy evidence incomplete',
  SUMMARY_COVERAGE_INCOMPLETE: 'Source coverage is incomplete',
  CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED: 'Current policy applicability is not established',
  'payguard-bounded-advisory-v2': 'Fixed advisory contract',
  SYNTHETIC_TEST_RESPONSE: 'Synthetic test run',
  OPERATOR_LIVE_RESPONSE: 'Live model response',
  LOCAL_RUNTIME_RESPONSE: 'Local model response',
  PAYLOAD_DIGEST_BOUND: 'Draft details locked for this review',
};

assert.equal(Object.isFrozen(OPERATOR_LABELS), true);
for (const [code, label] of Object.entries(required)) {
  assert.equal(operatorLabel(code), label, code);
}
assert.equal(operatorLabel('UNEXPECTED_BACKEND_STATUS'), 'Needs review');
assert.equal(operatorLabel(null), 'Needs review');
assert.equal(operatorLabel('UNEXPECTED_BACKEND_STATUS', 'Review unavailable'), 'Review unavailable');
assert.deepEqual(
  operatorLabels(['REQUESTED_FROM_SELLER', 'UNEXPECTED_BACKEND_STATUS', 'PROVIDE_EVIDENCE']),
  ['Requested from seller', 'Needs review', 'Prepare evidence'],
);
assert.deepEqual(operatorLabels(null), []);
assert.equal(sandboxReadbackLabel(false), 'Verified from the creation response only');
assert.equal(sandboxReadbackLabel(true), 'Verified by a separate status check');

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const policy = readFileSync(resolve(root, 'frontend/src/PolicyPanel.jsx'), 'utf8');
const references = readFileSync(resolve(root, 'frontend/src/ReferencePanel.jsx'), 'utf8');

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
]) assert.equal(app.includes(forbidden), false, forbidden);

for (const requiredSource of [
  'operatorLabels(assessment.reason_codes)',
  'operatorLabels(source.reason_codes)',
  'operatorLabel(gate.status)',
  'operatorLabels(g.reason_codes)',
]) assert.equal(policy.includes(requiredSource), true, requiredSource);

assert.equal(references.includes('placeholder="YYYY-MM-DDTHH:mm:ssZ"'), true);
assert.equal(references.includes('placeholder="YYYY-MM-DDTHH:mm:ss+08:00"'), false);

console.log(JSON.stringify({ status: 'PASS', required_mappings: Object.keys(required).length, unknown_fallback: 'Needs review' }));
