// (evloop) PayPal error reasons the seller can read: api.js accepts the optional paypal_issue on an error body, checks
// it again, maps the documented codes to plain English and shows any other code as "PayPal said: CODE"; App.jsx
// shows the lines and the PayPal-Debug-Id in the error banner. No browser, no network.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { ApiError, PAYPAL_ISSUE_TEXT, apiRequest, paypalIssueLines, readPaypalIssue } from '../frontend/src/api.js';

const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');

// 1. Every mapped code is one PayPal's docs list (the Disputes, Tracking and Invoicing error tables and examples), and
//    each has the closed code shape. The examples a reviewer named but PayPal does not document are not invented.
const DOCUMENTED = new Set([
  'INVALID_EVIDENCE_FILE', 'MISSING_EVIDENCE_INFO', 'MISSING_EVIDENCE_TYPE', 'MISSING_TRACKING_INFO', 'MANDATORY_PARAMETER_MISSING',
  'ACTION_NOT_ALLOWED_IN_CURRENT_DISPUTE_STATE', 'INVALID_EVIDENCE_TYPE_PROOF_OF_FULFILLMENT', 'ITEM_ID_IS_MANDATORY_FOR_MULTIPLE_EVIDENCES',
  'PERMISSION_DENIED', 'NOT_AUTHORIZED', 'AUTHENTICATION_FAILURE', 'INPUT_VALIDATION_ERROR', 'INVALID_PARAMETER_VALUE',
  'INVALID_PARAMETER_SYNTAX', 'RESOURCE_NOT_FOUND', 'RATE_LIMIT_REACHED', 'INTERNAL_SERVER_ERROR', 'INVALID_REQUEST', 'UNPROCESSABLE_ENTITY',
]);
assert.deepEqual(Object.keys(PAYPAL_ISSUE_TEXT).sort(), [...DOCUMENTED].sort());
for (const [code, text] of Object.entries(PAYPAL_ISSUE_TEXT)) {
  assert.match(code, /^[A-Z0-9_]{1,64}$/u);
  assert.ok(text.length > 10 && text.length <= 140 && !/[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]/u.test(text), `${code} plain English`);
}
for (const undocumented of ['MISSING_REQUIRED_PARAMETER', 'CANNOT_PROVIDE_EVIDENCE_IN_CURRENT_STATE', 'INVALID_TRACKING_NUMBER']) {
  assert.equal(Object.hasOwn(PAYPAL_ISSUE_TEXT, undocumented), false, `${undocumented} is not in PayPal's docs`);
}

// 2. Mapping: issue codes first, the name only when no issue is given, unknown codes as "PayPal said: CODE".
assert.deepEqual(paypalIssueLines({ name: 'UNPROCESSABLE_ENTITY', issues: ['INVALID_EVIDENCE_FILE'] }), [PAYPAL_ISSUE_TEXT.INVALID_EVIDENCE_FILE]);
assert.match(paypalIssueLines({ name: 'UNPROCESSABLE_ENTITY', issues: ['INVALID_EVIDENCE_FILE'] })[0], /JPG, GIF, PNG or PDF/u);
assert.deepEqual(paypalIssueLines({ name: 'UNPROCESSABLE_ENTITY', issues: ['ACTION_NOT_ALLOWED_IN_CURRENT_DISPUTE_STATE', 'SOMETHING_NEW_42'] }),
  [PAYPAL_ISSUE_TEXT.ACTION_NOT_ALLOWED_IN_CURRENT_DISPUTE_STATE, 'PayPal said: SOMETHING_NEW_42']);
assert.deepEqual(paypalIssueLines({ name: 'NOT_AUTHORIZED', issues: [] }), [PAYPAL_ISSUE_TEXT.NOT_AUTHORIZED]);
assert.deepEqual(paypalIssueLines({ name: 'BRAND_NEW_NAME', issues: [] }), ['PayPal said: BRAND_NEW_NAME']);
assert.deepEqual(paypalIssueLines({ name: null, issues: ['PERMISSION_DENIED', 'PERMISSION_DENIED'] }), [PAYPAL_ISSUE_TEXT.PERMISSION_DENIED]);
assert.deepEqual(paypalIssueLines({ name: 'INVALID_REQUEST', issues: ['INPUT_VALIDATION_ERROR', 'MISSING_TRACKING_INFO', 'INVALID_PARAMETER_VALUE'] }),
  [PAYPAL_ISSUE_TEXT.INPUT_VALIDATION_ERROR, PAYPAL_ISSUE_TEXT.MISSING_TRACKING_INFO, PAYPAL_ISSUE_TEXT.INVALID_PARAMETER_VALUE]);

// 3. The optional field is checked again in the console: free text, lower case, oversize, extra keys or too many issues
//    give no line at all.
for (const bad of [
  null, undefined, 'INVALID_REQUEST', [], { name: 'Invalid request.', issues: [] }, { name: 'invalid_request', issues: [] },
  { name: 'A'.repeat(65), issues: [] }, { name: null, issues: ['free text here'] }, { name: null, issues: [] },
  { name: 'X', issues: ['A', 'B', 'C', 'D'] }, { name: 'X', issues: ['A'], message: 'PayPal free text' }, { name: 'X' },
  { name: 'X', issues: 'A' }, { name: 'X', issues: [7] }, { name: 'X\n', issues: [] },
]) {
  assert.equal(readPaypalIssue(bad), null, JSON.stringify(bad));
  assert.deepEqual(paypalIssueLines(bad), [], JSON.stringify(bad));
}
assert.deepEqual(readPaypalIssue({ issues: ['A'], name: null }), { name: null, issues: ['A'] });

// 4. apiRequest carries the field from a failed provide-evidence, tracking or invoice answer onto the ApiError.
const session = { session_id: 'session-paypal-issue', csrf_token: 'csrf-paypal-issue' };
const routes = [
  ['/paypal/disputes/provide-evidence', { dispute_id: 'PP-D-SANDBOX01', case_ref: 'case-ref-001', submit: true }],
  ['/paypal/disputes/add-tracking', { dispute_id: 'PP-D-SANDBOX01', case_ref: 'case-ref-001', submit: true }],
  ['/paypal/invoices/draft', { description: 'Synthetic item', amount: '10.00', currency: 'USD', review_token: 'r'.repeat(32), payload_digest: 'd'.repeat(64) }],
];
const failing = (error) => async () => ({ ok: false, status: 502, headers: { get: () => null }, json: async () => ({ error }) });
for (const [path, body] of routes) {
  globalThis.fetch = failing({ code: 'provider_upstream_failure', message: 'The provider request could not be completed.',
    paypal_issue: { name: 'UNPROCESSABLE_ENTITY', issues: ['INVALID_EVIDENCE_FILE'] }, paypal_debug_id: 'f00dbabe12345' });
  await assert.rejects(apiRequest(path, { method: 'POST', body, session }), (error) => {
    assert.ok(error instanceof ApiError);
    assert.equal(error.code, 'provider_upstream_failure');
    assert.deepEqual(error.paypalIssue, { name: 'UNPROCESSABLE_ENTITY', issues: ['INVALID_EVIDENCE_FILE'] });
    assert.equal(error.paypalDebugId, 'f00dbabe12345');
    return true;
  }, path);
  // Without the optional fields (an older backend) the error is unchanged; a malformed field is dropped.
  globalThis.fetch = failing({ code: 'provider_upstream_failure', message: 'The provider request could not be completed.' });
  await assert.rejects(apiRequest(path, { method: 'POST', body, session }), (error) => error.paypalIssue === null && error.paypalDebugId === null, path);
  globalThis.fetch = failing({ code: 'provider_upstream_failure', message: 'x', paypal_issue: { name: 'Free text', issues: [] }, paypal_debug_id: 'not a debug id!' });
  await assert.rejects(apiRequest(path, { method: 'POST', body, session }), (error) => error.paypalIssue === null && error.paypalDebugId === null, path);
}
assert.equal(new ApiError('m', 502, 'c').paypalIssue, null, 'older callers need no options');

// 5. App.jsx shows the lines and the debug id in the error banner, from the checked fields only.
const app = read('../frontend/src/App.jsx');
assert.ok(app.includes("import { ApiError, apiRequest, paypalIssueLines, retrySecondsLeft } from './api.js';"));
assert.ok(app.includes('{waitFailureMessage(error)}<PaypalIssueNote error={error} />'), 'banner shows the PayPal reason');
const note = app.slice(app.indexOf('function PaypalIssueNote('), app.indexOf('\n}\n', app.indexOf('function PaypalIssueNote(')));
assert.ok(note.includes('paypalIssueLines(error?.paypalIssue)') && note.includes('error.paypalDebugId'));
assert.ok(note.includes('data-testid="paypal-issue-line"') && note.includes('PayPal request ID'));
assert.equal(/paypal_issue|dangerouslySetInnerHTML/u.test(note), false, 'only the checked ApiError fields reach the page');
assert.equal(/[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]/u.test(note), false, 'English only');

console.log(`frontend_paypal_issue: ok (${Object.keys(PAYPAL_ISSUE_TEXT).length} documented codes mapped, ${routes.length} routes carry paypal_issue)`);
