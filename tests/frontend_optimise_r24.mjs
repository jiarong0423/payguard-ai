import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { apiRequest } from '../frontend/src/api.js';

// (optimise r24) Console optimisations for the three scenarios: source pins for the new cards and the response
// contracts for the optional backend fields (paypal_debug_id, payload_sha256) and the add-tracking preview.
const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const panel = readFileSync(new URL('../frontend/src/CountryRules.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const panelCss = readFileSync(new URL('../frontend/src/CountryRules.css', import.meta.url), 'utf8');

// Scenario 1: before/after card, line-by-line status, expiry warning, different default countries, neutral label.
assert.ok(panel.includes('export const LINE_CHECKED = Object.freeze({ TW: \'2026-11-02\', CN: \'2026-11-02\' });'), 'only TW and CN are line-checked');
assert.ok(panel.includes('reviews/r10_e768aaf/5_rules_accuracy.md'), 'line-check list cites its source');
assert.ok(panel.includes('data-testid="country-verdict-line-check"') && panel.includes('data-testid="country-row-line-check"'), 'verdict and rows show the status');
assert.ok(panel.includes('data-testid="country-row-source-date"> · source read {retrievedAt}'), 'rows show the source date');
assert.ok(panel.includes('Stopped at {clockTime(before.at)} → {after.word} at {clockTime(after.at)}'), 'before/after line with both times');
assert.ok(panel.includes('{!result.blocked && unlock?.after && <BeforeAfter record={unlock} names={names} />}'), 'card only after a later non-stop result');
assert.ok(panel.includes("setUnlock((current) => (payload.blocked ? { before: entry, after: null } : current ? { before: current.before, after: entry } : null));"), 'a Stop starts a new pair');
assert.ok(panel.includes("const away = [home === 'US' ? 'CA' : 'US', ...codes].find((code) => code !== home && codes.includes(code)) || home;"), 'ships-to default differs');
assert.ok(panel.includes('setForm({ seller_country: home, buyer_country: away,'), 'defaults use two countries');
assert.ok(app.includes("{aup ? (aup.match_status === 'REVIEW_SIGNAL' ? 'REVIEW SIGNAL' : 'POLICY CHECK') : aupPhase === 'loading' ? 'CHECKING' : 'NOT CHECKED YET'}"), 'no REVIEW SIGNAL before a check');
assert.equal(app.includes('<span className="meta-label">REVIEW SIGNAL</span>'), false, 'unconditional label removed');
assert.ok(app.includes('const AUP_WARN_MS = 30000;') && app.includes('data-testid="aup-keep-result"'), 'expiry warning with Keep');
assert.ok(app.includes('That uses one of the 5 policy checks allowed per 2 minutes.'), 'Keep states its cost');
assert.ok(app.includes('if (aupCheckedTextRef.current !== description) {'), 'Keep re-runs only for the same text');
assert.equal(/extend|\/aup\/keep|\/aup\/renew/.test(app.match(/const keepAupResult = \(\) => \{[\s\S]*?\n  \};/u)[0]), false, 'no invented extension endpoint');

// Scenario 2: records card and phone window.
assert.ok(app.includes('<SpikeRecordsCard velocity={velocity} transactions={state?.transactions} />'), 'records card under the chart');
assert.ok(app.includes("const RESERVE_CASE_URL = 'https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf';"), 'reserve case link');
const card = app.match(/function SpikeRecordsCard\([\s\S]*?\n\}\n/u)[0];
assert.equal(/predict|will be (held|limited)|likely to be (held|limited)/i.test(card), false, 'no prediction wording');
assert.ok(app.includes('function phoneChartVelocity(velocity, narrow) {'), 'phone chart window');

// Scenario 3: exact payload card, step 01 labels, tracking preview behind the same gates.
assert.ok(app.includes('<details className="approval-payload" data-testid="approval-payload" open>'), 'approval payload open by default');
assert.ok(app.includes("{current.payload_sha256 || '—'}"), 'sha256 or a dash');
assert.ok(app.indexOf('<ApprovalPayloadCard ') > app.indexOf("'Confirm local draft review'}</Button>"), 'card sits beside the approval');
assert.ok(app.includes('data-testid="step-one-evidence"') && app.includes('data-testid="zip-from-step-01"'), 'step 01 evidence labelled');
assert.ok(app.includes("const trackingSubmitReady = Boolean(receipt) && trackingPreview?.submit_flag_enabled === true && trackingPreview?.source === 'paypal_sandbox' && trackingPreview?.external_send === 'FROZEN' && !trackingBlock;"), 'tracking send gates (plus the r25 send guard)');
assert.ok(app.includes('disabled={disabled || !trackingSubmitReady}'), 'tracking send disabled until the gates pass');
assert.ok(app.includes("const itemNotReceived = providerDisputeDetail?.reason === 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED';"), 'tracking only for item not received');
assert.ok(app.indexOf('data-testid="tracking-submit"') < app.indexOf('</>}', app.indexOf('hosted-note-evidence')), 'tracking buttons sit inside the local branch');
for (const selector of ['.aup-expiry', '.spike-records', '.approval-payload', '.step-one-evidence']) assert.ok(css.includes(selector), selector);
assert.ok(panelCss.includes('.country-before-after'), 'before/after styles');

// Contracts: the fixture answers the backend returns today (probe 2026-11-04) plus the optional fields.
const session = { session_id: 's', csrf_token: 'c' };
const reply = (payload) => async () => ({ ok: true, status: 200, json: async () => payload });
const envelope = { source: 'synthetic_fixture', data_source_label: 'Fixture', environment: 'sandbox', evidence_class: 'SYNTHETIC_FIXTURE',
  observed_at: '2026-11-03T17:16:11.979995Z', provider_submission: 'NOT_PERFORMED', paypal_debug_id: null };
const list = { ...envelope, readback: 'GET_LIST', items: [{ dispute_id: 'PP-D-00000001', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', status: 'WAITING_FOR_SELLER_RESPONSE',
  dispute_life_cycle_stage: 'INQUIRY', dispute_state: null, dispute_amount: { currency_code: 'USD', value: '25.00' }, create_time: '2026-11-01T00:00:00.000Z',
  update_time: null, seller_response_due_date: null }] };
globalThis.fetch = reply(list);
assert.deepEqual(await apiRequest('/paypal/disputes', { session }), list, 'list with paypal_debug_id null');
const { paypal_debug_id: _dropped, ...oldList } = list;
globalThis.fetch = reply(oldList);
assert.deepEqual(await apiRequest('/paypal/disputes', { session }), oldList, 'list without paypal_debug_id still accepted');
globalThis.fetch = reply({ ...list, paypal_debug_id: 'abc123def' });
await assert.rejects(apiRequest('/paypal/disputes', { session }), /contract mismatch/, 'a fixture never carries a Debug-Id');

const evidenceBody = { dispute_id: 'PP-D-00000001', case_ref: 'case-ref-001', submit: false };
const preview = { ...envelope, readback: 'PROVIDE_EVIDENCE_PREVIEW', dispute_id: 'PP-D-00000001', case_ref: 'case-ref-001', method: 'POST',
  path: '/v1/customer/disputes/PP-D-00000001/provide-evidence', content_type: 'multipart/form-data',
  input: { evidences: [{ evidence_type: 'PROOF_OF_FULFILLMENT', evidence_info: { tracking_info: [{ carrier_name: 'OTHER', carrier_name_other: 'SYNTHETIC_CARRIER', tracking_number: '*******************001' }] }, notes: 'Shipment tracking for this order, provided by the seller.' }] },
  files: [{ name: 'file1', filename: 'synthetic-delivery.pdf', content_type: 'application/pdf', byte_length: 43 }],
  external_send: 'FROZEN', submit_flag_enabled: false, human_review_required: true };
globalThis.fetch = reply(preview);
assert.deepEqual(await apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: evidenceBody, session }), preview, 'preview without sha256');
const hashed = { ...preview, payload_sha256: 'a'.repeat(64) };
globalThis.fetch = reply(hashed);
assert.deepEqual(await apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: evidenceBody, session }), hashed, 'preview with sha256');
globalThis.fetch = reply({ ...preview, payload_sha256: 'not-a-hash' });
await assert.rejects(apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: evidenceBody, session }), /contract mismatch/, 'bad sha256 refused');
globalThis.fetch = reply({ ...preview, surprise: 1 });
await assert.rejects(apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: evidenceBody, session }), /contract mismatch/, 'unknown keys still refused');

const tracking = { ...envelope, readback: 'ADD_TRACKING_PREVIEW', dispute_id: 'PP-D-00000001', case_ref: 'case-ref-001', method: 'POST',
  path: '/v1/shipping/trackers-batch', content_type: 'application/json',
  body: { trackers: [{ transaction_id: '***************001', tracking_number: '*******************001', status: 'SHIPPED', carrier: 'OTHER', carrier_name_other: 'SYNTHETIC_CARRIER' }] },
  external_send: 'FROZEN', submit_flag_enabled: false, human_review_required: true };
globalThis.fetch = reply(tracking);
assert.deepEqual(await apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: evidenceBody, session }), tracking, 'tracking preview accepted');
const trackingHashed = { ...tracking, payload_sha256: 'b'.repeat(64) };
globalThis.fetch = reply(trackingHashed);
assert.deepEqual(await apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: evidenceBody, session }), trackingHashed, 'tracking preview with sha256');
for (const broken of [
  { ...tracking, path: '/v1/shipping/trackers' },
  { ...tracking, external_send: 'SUBMITTED' },
  { ...tracking, body: { trackers: [{ ...tracking.body.trackers[0], carrier: 'OTHER', carrier_name_other: null }] } },
  { ...tracking, body: { trackers: [] } },
  { ...tracking, case_ref: 'case-ref-002' },
  { ...tracking, payload_sha256: 'short' },
]) {
  globalThis.fetch = reply(broken);
  await assert.rejects(apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: evidenceBody, session }), /contract mismatch/);
}

console.log(JSON.stringify({ status: 'PASS', checks: 'optimise r24' }));
