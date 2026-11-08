// A real Sandbox send returns the plain SHA-256 of each file it posted (`sent_files`). The browser must accept that on a
// send, refuse it on a preview, and refuse a send that lacks it or whose entries do not describe the listed files.
// Without this the page answered "The API returned invalid content" right after PayPal had received the evidence.
import assert from 'node:assert/strict';

import { apiRequest } from '../frontend/src/api.js';

const session = { session_id: 's'.repeat(43), csrf_token: 'c'.repeat(43) };
let reply = null;
globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(reply), headers: { get: () => null } });

const disputeId = 'PP-D-00000001';
const body = { dispute_id: disputeId, case_ref: 'case-ref-001', submit: true };
const part = { name: 'file1', filename: 'synthetic-delivery.pdf', content_type: 'application/pdf', byte_length: 2015 };
const sent = { filename: 'synthetic-delivery.pdf', content_type: 'application/pdf', byte_length: 2015, sha256: 'a'.repeat(64) };
const base = {
  source: 'paypal_sandbox', data_source_label: 'Sandbox', environment: 'sandbox', evidence_class: 'AUTHENTIC_SANDBOX_RESPONSE',
  observed_at: '2026-11-09T05:44:00Z', provider_submission: 'PERFORMED', paypal_debug_id: 'f530251c4d37a',
  readback: 'PROVIDE_EVIDENCE_SUBMITTED', dispute_id: disputeId, case_ref: 'case-ref-001', method: 'POST',
  path: `/v1/customer/disputes/${disputeId}/provide-evidence`, content_type: 'multipart/form-data',
  input: { evidences: [{ evidence_type: 'PROOF_OF_FULFILLMENT', evidence_info: { tracking_info: [{ carrier_name: 'UPS', tracking_number: '1Z***001' }] }, notes: 'n' }] },
  files: [part], external_send: 'SUBMITTED', submit_flag_enabled: true, human_review_required: true,
  payload_sha256: 'b'.repeat(64), confirm_token: null,
  send_guard: { case_ref: 'case-ref-001', case_reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', dispute_masked: 'PP-D-…01', dispute_reason: null,
    dispute_amount: null, bound_dispute_masked: null, sending_account_masked: null, dispute_seller_masked: null, account_status: 'MATCH', send_refusal: null },
  sent_files: [sent],
};
const preview = { ...base, provider_submission: 'NOT_PERFORMED', readback: 'PROVIDE_EVIDENCE_PREVIEW', external_send: 'FROZEN', paypal_debug_id: null };
delete preview.sent_files;

async function check(payload, ok, label) {
  reply = payload;
  const run = apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body, session });
  if (ok) assert.deepEqual(await run, payload, label);
  else await assert.rejects(run, (error) => error.code === 'contract_error' || error.code === 'invalid_response' || /invalid/i.test(error.message), label);
}

await check(base, true, 'a real send with its fingerprint is accepted');
await check(preview, true, 'a preview without the field is accepted');
await check({ ...preview, sent_files: null }, true, 'a preview with null is accepted');
for (const [label, change] of [
  ['preview carrying a hash', { ...preview, sent_files: [sent] }],
  ['send without the field', (() => { const copy = { ...base }; delete copy.sent_files; return copy; })()],
  ['send with null', { ...base, sent_files: null }],
  ['send with an empty list', { ...base, sent_files: [] }],
  ['two hashes for one file', { ...base, sent_files: [sent, sent] }],
  ['wrong file name', { ...base, sent_files: [{ ...sent, filename: 'other.pdf' }] }],
  ['wrong size', { ...base, sent_files: [{ ...sent, byte_length: 2016 }] }],
  ['wrong media type', { ...base, sent_files: [{ ...sent, content_type: 'image/png' }] }],
  ['short hash', { ...base, sent_files: [{ ...sent, sha256: 'a'.repeat(63) }] }],
  ['upper-case hash', { ...base, sent_files: [{ ...sent, sha256: 'A'.repeat(64) }] }],
  ['extra key', { ...base, sent_files: [{ ...sent, content: 'x' }] }],
  ['hash as a string', { ...base, sent_files: 'a'.repeat(64) }],
]) await check(change, false, label);

console.log(JSON.stringify({ status: 'PASS', checks: ['send accepted with fingerprint', 'preview accepted without', '12 refusals'] }));
