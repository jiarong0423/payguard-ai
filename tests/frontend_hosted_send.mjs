// Hosted evidence send (owner decision 2026-11-10; GET /connections -> sandbox_send true with send_state counts) and the
// deadline board fed by live Sandbox disputes. Source and pure-module checks; no browser.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { apiRequest } from '../frontend/src/api.js';
import { hostedCopy } from '../frontend/src/hostedCopy.js';
import { buildEvidenceBoard, restorePlans, sandboxCases, TRIAGE_CAPTION, UNSCHEDULED_LABEL, unscheduledRows } from '../frontend/src/board/boardData.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const boardSource = readFileSync(resolve(root, 'frontend/src/board/EvidenceBoard.jsx'), 'utf8');
const session = { session_id: 'session-1', csrf_token: 'csrf-1', expires_at: '2099-01-01T00:00:00Z' };
const serve = (payload) => { globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(payload) }); };

// 1. /connections: the send shape is accepted only complete, with hosted_demo and sandbox_reads; counts only.
const good = { mode: 'hosted_demo', sandbox_reads: true, sandbox_send: true,
  send_state: { sends_left_window: 3, sends_left_day: 15, window_minutes: 10, disputes_sent: 0 } };
serve(good);
assert.deepEqual(await apiRequest('/connections', { session }), good);
for (const payload of [
  { ...good, sandbox_send: false }, { ...good, sandbox_reads: false }, { ...good, mode: 'local' },
  { mode: 'hosted_demo', sandbox_reads: true, sandbox_send: true },
  { ...good, send_state: { ...good.send_state, dispute_id: 'PP-D-1' } },
  { ...good, send_state: { ...good.send_state, sends_left_day: -1 } },
  { ...good, send_state: { ...good.send_state, window_minutes: 0 } },
  { ...good, secret: 'x' },
]) {
  serve(payload);
  await assert.rejects(apiRequest('/connections', { session }), (error) => error.code === 'contract_error', JSON.stringify(payload));
}

// 2. Wording follows the flags: no "never calls PayPal" while the send is on.
const live = hostedCopy({ chooser_mode: 'gemini' }, true, true);
assert.equal(live.pill, 'Hosted demo · Sandbox reads + capped send');
assert.ok(live.intro.includes('never a live account') && live.intro.includes('once per dispute and once per visit'));
assert.ok(!/never calls PayPal|cannot write|no PayPal/u.test(live.intro + live.pill));
assert.equal(hostedCopy({ chooser_mode: 'gemini' }, true, false).pill, 'Hosted demo · read-only Sandbox', 'read-only wording unchanged');
assert.equal(hostedCopy({ chooser_mode: 'gemini' }, false, true).pill, 'Hosted demo · no PayPal calls', 'the send flag alone changes nothing');

// 3. Console: flag from /connections only; receipt in large text with SUBMITTED, Debug-Id and the read-back.
assert.equal((app.match(/setSandboxSend\(/g) || []).length, 1, 'one place sets the send flag');
assert.ok(app.includes("setSandboxSend(connections?.mode === 'hosted_demo' && connections.sandbox_send === true);"));
for (const id of ['send-receipt', 'send-receipt-debug-id', 'send-receipt-readback', 'dispute-list-debug-id', 'hosted-send-none-left']) {
  assert.ok(app.includes(`data-testid="${id}"`), id);
}
assert.ok(app.includes('<strong>SUBMITTED to PayPal Sandbox</strong>'));
assert.ok(app.includes("apiRequest(`/paypal/disputes/${result.dispute_id}`, { session }).then((fresh) => { setSendReadback({ status: fresh.status, debug: fresh.paypal_debug_id });"), 'one GET read-back after a send');
assert.ok(app.includes('row.dispute_id === fresh.dispute_id ? { ...row, status: fresh.status } : row'), 'the read-back status also updates the list and the board');
// Tracking and invoices never show on the hosted demo.
assert.ok(app.includes('{itemNotReceived && !hosted && <>'));
assert.ok(app.includes(": reviewRecorded && !hosted && trackingSubmitReady\n"));

// 4. Nothing left to send (no listed dispute waits for the seller, or the shared cap is used): say so and open the replay.
assert.ok(app.includes("!(providerDisputes.items || []).some((row) => row.status === 'WAITING_FOR_SELLER_RESPONSE')"));
assert.ok(app.includes('(sendState.sends_left_day === 0 || sendState.sends_left_window === 0)'));
assert.ok(app.includes("{sendNoneLeft && <p className=\"hosted-note\" role=\"status\" data-testid=\"hosted-send-none-left\">{sendCapped ? HOSTED_NOTES.capped : HOSTED_NOTES.noneLeft}</p>}"));
assert.ok(app.includes('open={sendNoneLeft || undefined} className="sandbox-details stage-fold" data-testid="replay-fold"'), 'replay fold opens when nothing is left');
assert.ok(app.includes("noneLeft: 'No Sandbox test dispute is waiting for a seller response right now, so there is nothing left to send here. The recorded replay below shows the same send.'"));
assert.ok(app.includes('<RecordedSendReplay />'), 'the existing labelled replay is the fallback');

// 5. Board: Sandbox rows from the list read, with the seller response due date; no automatic slot for them.
const NOW = Date.parse('2026-11-10T08:00:00Z');
const items = [
  { dispute_id: 'PP-R-XXXX7173', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', status: 'WAITING_FOR_SELLER_RESPONSE', dispute_life_cycle_stage: 'INQUIRY',
    dispute_amount: { value: '48.00', currency_code: 'USD' }, create_time: '2026-11-09T08:00:00Z', seller_response_due_date: '2026-11-29T08:00:00Z' },
  { dispute_id: 'PP-R-XXXX0001', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', status: 'WAITING_FOR_BUYER_RESPONSE', dispute_life_cycle_stage: 'INQUIRY',
    dispute_amount: { value: '48.00', currency_code: 'USD' }, create_time: '2026-11-04T08:00:00Z', seller_response_due_date: '2026-11-24T08:00:00Z' },
  { dispute_id: 'PP-R-XXXX0002', reason: 'UNAUTHORISED', status: 'WAITING_FOR_SELLER_RESPONSE', dispute_life_cycle_stage: 'CHARGEBACK',
    dispute_amount: { value: '60.00', currency_code: 'USD' }, create_time: '2026-11-08T08:00:00Z', seller_response_due_date: '2026-11-11T08:00:00Z' },
];
assert.equal(sandboxCases(items).length, 3);
const board = buildEvidenceBoard({ disputes: [], drafts: {}, now: NOW, sandbox: items });
assert.equal(board.rows.length, 3);
assert.deepEqual(board.rows.map((row) => [row.id, row.source, row.dueAt, row.amount]), [
  ['PP-R-XXXX7173', 'sandbox', '2026-11-29T08:00:00Z', '48.00 USD'],
  ['PP-R-XXXX0001', 'sandbox', '2026-11-24T08:00:00Z', '48.00 USD'],
  ['PP-R-XXXX0002', 'sandbox', '2026-11-11T08:00:00Z', '60.00 USD'],
]);
assert.deepEqual(board.rows.map((row) => row.status), ['OPEN', 'NOT_AWAITING_SELLER', 'DUE_SOON']);
assert.ok(board.events.some((event) => event.id === 'PP-R-XXXX7173-window' && event.source === 'PayPal Sandbox · seller response due date'));
const plans = restorePlans({}, board.rows, NOW);
assert.deepEqual(plans, {}, 'Sandbox rows get no automatic evidence slot');
assert.deepEqual(unscheduledRows(board.rows, plans, NOW).map((row) => row.id), ['PP-R-XXXX7173', 'PP-R-XXXX0002'],
  'deadline but no slot; a dispute PayPal no longer waits on is not flagged');
const scheduled = { 'PP-R-XXXX7173': { startMs: NOW + 3600000, endMs: NOW + 7200000 } };
assert.deepEqual(unscheduledRows(board.rows, scheduled, NOW).map((row) => row.id), ['PP-R-XXXX0002']);
// A stored slot for a Sandbox row comes back; sample cases keep their default plan as before.
const stored = { 'PP-R-XXXX7173': { start: new Date(NOW + 3600000).toISOString(), end: new Date(NOW + 7200000).toISOString() } };
assert.deepEqual(Object.keys(restorePlans(stored, board.rows, NOW)), ['PP-R-XXXX7173']);
const mixed = buildEvidenceBoard({ disputes: [{ case_ref: 'case-ref-001', reason: 'INR', status: 'needs_review', opened_at: '2026-11-09T08:00:00Z',
  seller_response_due_date: '2026-11-12T08:00:00Z' }], drafts: {}, now: NOW, sandbox: items });
assert.deepEqual(mixed.rows.map((row) => row.source), ['sandbox', 'sandbox', 'sandbox', 'synthetic']);
assert.ok(restorePlans({}, mixed.rows, NOW)['case-ref-001'], 'sample cases still get the default plan');
// Reads off: the synthetic board is unchanged.
assert.equal(buildEvidenceBoard({ disputes: [], drafts: {}, now: NOW, sandbox: null }), null);

// 6. Bryntum's own wording (J4 sponsor review quotes "disputed amount, response deadline, and evidence readiness").
assert.equal(TRIAGE_CAPTION, 'Each case: amount, deadline, evidence');
assert.equal(UNSCHEDULED_LABEL, 'Deadline set · no evidence slot scheduled');
assert.ok(boardSource.includes('data-testid="evidence-board-triage"') && boardSource.includes('data-testid="evidence-board-unscheduled"') && boardSource.includes('data-testid="evidence-board-schedule"'));
assert.ok(boardSource.includes('with a deadline but no evidence slot scheduled'));
assert.ok(!/apiRequest|fetch\(/u.test(boardSource), 'the board makes no request');

console.log('frontend_hosted_send: ok');
