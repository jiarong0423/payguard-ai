import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { displayDisputeId, isShownDisputeId, DISPUTE_ID_HIDDEN } from '../frontend/src/disputeDisplay.js';
import { buildEvidenceBoard, restorePlans } from '../frontend/src/board/boardData.js';

// (2026-11-11) One display mapping for dispute ids (frontend/src/disputeDisplay.js). (a) What it shows for hosted codes,
// raw local ids and bad input. (b) The comparisons are independent of it: pairing, the send lock, sentByCaseRef, API
// payloads and storage keys keep the raw id or App.jsx maskDisputeId, so changing the shown format cannot change pairing.
const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');
const app = read('../frontend/src/App.jsx');
const boardData = read('../frontend/src/board/boardData.js');
const board = read('../frontend/src/board/EvidenceBoard.jsx');
const mapping = read('../frontend/src/disputeDisplay.js');

// ---- (a) mapping outputs -------------------------------------------------------------------------------------------
// Codes the server already masked (backend/app/demo_mode.py _code_for: head + "-XXXX" + last 4, "-n" after a clash).
for (const code of ['PP-R-VAF-XXXX7877', 'PP-R-EAK-XXXX0123', 'PP-D-XXXX4567', 'PP-R-BNP-XXXX7173-2', 'PP-R-ABC-XXXXA1B2']) {
  assert.equal(displayDisputeId(code), code, `hosted code shown as is: ${code}`);
  assert.equal(isShownDisputeId(code), true);
}
// Raw local ids: the short form (first 5, "…", last 2), the same text maskDisputeId gives today.
assert.equal(displayDisputeId('PP-R-NHX-10133829'), 'PP-R-…29');
assert.equal(displayDisputeId('PP-D-SANDBOX01'), 'PP-D-…01');
assert.equal(displayDisputeId('PP-D-123456789'), 'PP-D-…89');
assert.equal(isShownDisputeId('PP-R-NHX-10133829'), false);
// The short form itself (server mask_dispute_id, guard.dispute_masked) is shown as is: the mapping is idempotent.
for (const value of ['PP-R-…29', 'PP-D-…01', '…']) assert.equal(displayDisputeId(value), value, `short form kept: ${value}`);
for (const raw of ['PP-R-NHX-10133829', 'PP-R-VAF-XXXX7877', 'PP-D-SANDBOX01', '', 'x']) {
  assert.equal(displayDisputeId(displayDisputeId(raw)), displayDisputeId(raw), `idempotent: ${raw}`);
}
// Empty, too short, not a string: hidden.
for (const bad of ['', 'PP-D-1', '12345678', null, undefined, 42, {}, ['PP-R-VAF-XXXX7877']]) {
  assert.equal(displayDisputeId(bad), DISPUTE_ID_HIDDEN, `hidden: ${JSON.stringify(bad)}`);
}
// A look-alike that is not a server code (lower case, markup, no digits after XXXX) is not passed through as is.
for (const odd of ['pp-r-vaf-xxxx7877', '<b>PP-R-XXXX1234</b>', 'PP-R-VAF-XXXX', 'PP-R-VAF-XXXX78777', 'XXXX7877']) {
  assert.notEqual(displayDisputeId(odd), odd, `not shown verbatim: ${odd}`);
}
assert.equal(displayDisputeId('<img src=x onerror=1>-XXXX1234'), '<img …34', 'markup is never passed through whole (React and the board escape the rest)');
// The mapping module has no comparison or storage role.
assert.ok(!/sessionStorage|localStorage|apiRequest|fetch\(/u.test(mapping), 'display module touches no storage or network');

// ---- (b) comparisons use the full id; the display mapping only names it ---------------------------------------------
// (round2 X, B 2c/5a) Pairing, "sent to", the lock and stored receipts compare the full dispute id the API returned (hosted
// code or raw local id). maskDisputeId stays byte for byte: it only adds a hold when the server's short form disagrees.
assert.ok(app.includes("const maskDisputeId = (value) => (typeof value === 'string' && value.length > 8 ? `${value.slice(0, 5)}…${value.slice(-2)}` : '…');"), 'maskDisputeId unchanged');
assert.ok(!app.includes('shownDisputeId'), 'the earlier per-site display helper is gone (one mapping only)');
assert.ok(app.includes("if (result?.external_send === 'SUBMITTED' && typeof result.dispute_id === 'string') sentByCaseRef.current[result.case_ref] = result.dispute_id;"), 'sentByCaseRef stores the full id');
assert.ok(app.includes("if (result?.send_guard?.bound_dispute_masked && typeof result.dispute_id === 'string') boundByCaseRef.current[result.case_ref] = result.dispute_id;"), 'boundByCaseRef stores the full id, not the server short form');
assert.ok(!/(sentByCaseRef|boundByCaseRef)\.current\[[^\]]*\] = [^;\n]*(maskDisputeId|bound_dispute_masked)/u.test(app), 'no short form stored as a pairing or sent key');
const section = app.slice(app.indexOf('// (r25 send guard) Safeguards'), app.indexOf('// What is being sent: evidence files'));
const grab = (name) => section.match(new RegExp(`(?:const ${name} = [^\\n]*\\n|function ${name}\\([\\s\\S]*?\\n\\}\\n)`, 'u'))[0];
const guardSource = grab('sendGuardBlock');
assert.ok(guardSource.includes('const here = detail.dispute_id;'), 'pairing/lock check `here` is the full id');
assert.ok(guardSource.includes("if (typeof previewId !== 'string' || previewId !== here)"), 'the preview is matched by its own full id');
assert.ok(!/guard\.dispute_masked !== here|bound !== maskDisputeId|sentTo === maskDisputeId/u.test(guardSource), 'no short-form identity match');
for (const line of guardSource.split('\n').filter((row) => row.includes('displayDisputeId('))) {
  assert.ok(/return [^\n]*`[^`]*\$\{displayDisputeId\(/u.test(line) || /^\s*: `[^`]*\$\{displayDisputeId\(/u.test(line), `display only inside a returned sentence: ${line.trim()}`);
}
// Every displayDisputeId use in App.jsx is one of the known display sites, inside rendered output or a shown sentence.
const DISPLAY_SITES = [
  'const sentToShown = sentTo ? displayDisputeId(sentTo) : null;',
  '<strong>{displayDisputeId(row.dispute_id)}</strong>',
  '<small>Dispute {displayDisputeId(evidencePreview.dispute_id)} · Sandbox test data',
  "['Dispute', displayDisputeId(providerDisputeDetail.dispute_id)],",
  'This case was already sent to ${displayDisputeId(bound)}; it cannot also go to ${displayDisputeId(here)}.`',
  '`Paired with ${displayDisputeId(bound)} (preview only).',
  '<strong>{displayDisputeId(detail.dispute_id)}</strong>',
  '`This case was sent to ${displayDisputeId(sentTo)}.`',
  '`This case is paired with ${displayDisputeId(boundTo)} (preview only).`',
  // (B 2c) The dialog names this dispute's code only when the preview's own full id is this dispute's id; two disputes whose
  // short forms collide (PP-R-…01) are never resolved to the wrong code. Otherwise the guard's short form.
  '<dd data-testid="send-confirm-dispute">{displayDisputeId(typeof previewDisputeId === \'string\' && previewDisputeId === detail?.dispute_id ? detail.dispute_id : guard?.dispute_masked)}</dd>',
];
assert.ok(app.includes("previewDisputeId={(sendConfirm === 'tracking' ? trackingPreview : evidencePreview)?.dispute_id}"), 'dialog gets the preview\'s own full id');
assert.ok(!/displayDisputeId\([^\n]*=== maskDisputeId\(/u.test(app), 'no short-form match inside a display call');
for (const site of DISPLAY_SITES) assert.equal(app.split(site).length - 1, 1, `display site present once: ${site}`);
const uses = (app.match(/displayDisputeId\(/gu) || []).length;
assert.equal(uses, 11, `no displayDisputeId use outside the listed display sites (found ${uses})`);
for (const line of app.split('\n').filter((row) => row.includes('displayDisputeId('))) {
  assert.ok(!/displayDisputeId\([^)]*\)\s*[!=]==|[!=]==\s*displayDisputeId\(/u.test(line), 'never compared');
  assert.ok(!/(sentByCaseRef|boundByCaseRef|sentReceipts)\.current\[[^\]]*displayDisputeId|setItem\([^)]*displayDisputeId|submitBody\([^)]*displayDisputeId|apiRequest\([^)]*displayDisputeId|key=\{displayDisputeId/u.test(line), 'never a key, payload or stored value');
}
// The click, the keys and the payloads keep the raw id.
for (const raw of ["onClick={() => loadProviderDispute(row.dispute_id)}", 'key={row.dispute_id}', "providerDisputeDetail?.dispute_id === row.dispute_id ? 'case-selected' : ''",
  "{ dispute_id: providerDisputeDetail.dispute_id, case_ref: caseItem.case_ref }", '[result.dispute_id]: { result, readback, sent_at: sentAt }']) {
  assert.ok(app.includes(raw), `raw id kept: ${raw}`);
}

// Behaviour: sendGuardBlock built from its own source. The display mapping only names disputes in the sentence; the
// hold decision is the same whatever it returns.
const factory = new Function('operatorLabel', 'displayDisputeId', `${grab('maskDisputeId')}${section.match(/const ACCOUNT_LINES = \{[\s\S]*?\n\};\n/u)[0]}${grab('sameMoney')}${guardSource}return { maskDisputeId, sendGuardBlock };`);
const label = (value, fallback = 'Needs review') => value || fallback;
const { maskDisputeId, sendGuardBlock } = factory(label, displayDisputeId);
const odd = factory(label, () => '<<shown>>');
const hostedDetail = { dispute_id: 'PP-R-VAF-XXXX7877', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', source: 'paypal_sandbox', dispute_amount: { currency_code: 'USD', value: '48.00' } };
const hostedGuard = { dispute_masked: maskDisputeId(hostedDetail.dispute_id), bound_dispute_masked: maskDisputeId(hostedDetail.dispute_id), case_reason: hostedDetail.reason, dispute_amount: hostedDetail.dispute_amount };
const C = { case_ref: 'case-ref-001' };
assert.equal(sendGuardBlock(hostedGuard, hostedDetail, C, null, null, hostedDetail.dispute_id), null, 'hosted code, own preview: send not held');
assert.equal(sendGuardBlock(hostedGuard, hostedDetail, C, hostedDetail.dispute_id, null, hostedDetail.dispute_id), null, 'bound to the same dispute: not held');
assert.equal(sendGuardBlock(hostedGuard, hostedDetail, C, 'PP-R-QQQ-XXXX1177', null, hostedDetail.dispute_id), 'Paired with PP-R-QQQ-XXXX1177 (preview only). Reset demo to pair it with another dispute.', 'bound to a look-alike (same short form): held, full code named');
assert.equal(odd.sendGuardBlock(hostedGuard, hostedDetail, C, hostedDetail.dispute_id, null, hostedDetail.dispute_id), null, 'decision independent of the display format');
assert.match(odd.sendGuardBlock(hostedGuard, hostedDetail, C, 'PP-R-QQQ-XXXX1177', null, hostedDetail.dispute_id), /^Paired with <<shown>>/u, 'display only names it');
const localDetail = { ...hostedDetail, dispute_id: 'PP-R-NHX-10133829' };
const localGuard = { ...hostedGuard, dispute_masked: maskDisputeId(localDetail.dispute_id), bound_dispute_masked: maskDisputeId(localDetail.dispute_id) };
assert.equal(sendGuardBlock(localGuard, localDetail, C, null, null, localDetail.dispute_id), null, 'raw local id pairs: send not held');
assert.equal(sendGuardBlock(localGuard, localDetail, C, 'PP-R-NHX-99999929', null, localDetail.dispute_id), 'Paired with PP-R-…29 (preview only). Reset demo to pair it with another dispute.', 'raw look-alike: held');
assert.notEqual(displayDisputeId(hostedDetail.dispute_id), maskDisputeId(hostedDetail.dispute_id));
assert.equal(displayDisputeId(localDetail.dispute_id), maskDisputeId(localDetail.dispute_id));

// ---- the board: row ids, plan keys and lookups keep the true id; only caseRefShown is mapped -----------------------
assert.ok(boardData.includes("import { displayDisputeId } from '../disputeDisplay.js';"));
assert.equal((boardData.match(/displayDisputeId\(/gu) || []).length, 1, 'boardData maps in one place');
assert.ok(boardData.includes('caseRefShown: fromSandbox ? displayDisputeId(id) : id,'), 'only Sandbox rows are mapped; sample case refs unchanged');
assert.ok(boardData.includes('const id = dispute.case_ref;') && boardData.includes('case_ref: row.dispute_id, reason: row.reason'), 'row id is the raw dispute id');
assert.ok(!/displayDisputeId\(|disputeDisplay\.js/u.test(board), 'EvidenceBoard shows caseRefShown and never maps or compares ids itself');
assert.ok(board.includes('id: row.id, name: `${row.caseRefShown} · ${row.reason}`, caseRef: row.caseRefShown,'), 'resource id stays row.id; caseRef field carries the shown code');
assert.ok(board.includes('<div className="board-row-head"><strong>{row.caseRefShown}</strong>'), 'card shows the shown code');
assert.ok(board.includes("store.getById(`${row.id}-plan`)") && board.includes('const ref = String(record.resourceId);'), 'plan lookups keep the row id');
const now = Date.parse('2026-11-11T00:00:00Z');
const item = (id) => ({ dispute_id: id, reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', status: 'WAITING_FOR_SELLER_RESPONSE', dispute_amount: { value: '48.00', currency_code: 'USD' }, create_time: '2026-11-01T00:00:00Z', seller_response_due_date: '2026-11-20T00:00:00Z' });
const built = buildEvidenceBoard({ disputes: [{ case_ref: 'case-ref-001', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', opened_at: '2026-11-01T00:00:00Z', seller_response_due_date: '2026-11-20T00:00:00Z' }], sandbox: [item('PP-R-VAF-XXXX7877'), item('PP-R-NHX-10133829')], now });
const byId = Object.fromEntries(built.rows.map((row) => [row.id, row]));
assert.deepEqual(Object.keys(byId).sort(), ['PP-R-NHX-10133829', 'PP-R-VAF-XXXX7877', 'case-ref-001'], 'row ids are the true values');
assert.equal(byId['PP-R-VAF-XXXX7877'].caseRefShown, 'PP-R-VAF-XXXX7877');
assert.equal(byId['PP-R-NHX-10133829'].caseRefShown, 'PP-R-…29');
assert.equal(byId['PP-R-NHX-10133829'].caseRef, 'PP-R-NHX-10133829', 'caseRef keeps the true value');
assert.equal(byId['case-ref-001'].caseRefShown, 'case-ref-001', 'sample case ref shown as is');
assert.ok(built.events.every((event) => byId[event.resourceId]), 'events point at true row ids');
const stored = { 'PP-R-NHX-10133829': { start: '2026-11-12T00:00:00.000Z', end: '2026-11-12T05:00:00.000Z' } };
assert.deepEqual(Object.keys(restorePlans(stored, built.rows, now)).sort(), ['PP-R-NHX-10133829', 'case-ref-001'], 'stored plans are keyed by the true id');

console.log('frontend_dispute_display_map: ok');
