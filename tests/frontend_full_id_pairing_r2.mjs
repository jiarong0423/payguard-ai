// (round2 X, 2026-11-11) Red team B 2c/5a and 6a/6d, judge C #4. Behaviour checks built from App.jsx's own source:
// (1) pairing, "sent to", the lock and stored receipts compare the full dispute id (two hosted codes that share the
// short form PP-R-…01 never cross-match); (2) a receipt read back from this tab's storage is SUBMITTED only when the
// fresh read-back confirms it, and a tampered record shows a note without the stamp; (3) the phone bar's send action
// waits before it can be tapped.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { displayDisputeId } from '../frontend/src/disputeDisplay.js';
import { operatorLabel } from '../frontend/src/operatorLabels.js';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const between = (from, to) => {
  const start = app.indexOf(from);
  const end = app.indexOf(to, start);
  assert.ok(start >= 0 && end > start, `source slice ${from}`);
  return app.slice(start, end);
};
const block = (pattern, name) => {
  const match = app.match(pattern);
  assert.ok(match, `source of ${name}`);
  return match[0];
};

// ---- the code under test, taken from App.jsx ------------------------------------------------------------------------
const storeSource = between("const SENT_STORE_KEY = 'payguard.console.sent.v1';", 'const storedToken = ');
const guardSection = between('// (r25 send guard) Safeguards', '// What is being sent: evidence files');
const grab = (name) => guardSection.match(new RegExp(`(?:const ${name} = [^\\n]*\\n|function ${name}\\([\\s\\S]*?\\n\\}\\n)`, 'u'))[0];
const guardSource = `${grab('maskDisputeId')}${guardSection.match(/const ACCOUNT_LINES = \{[\s\S]*?\n\};\n/u)[0]}${grab('sameMoney')}${grab('sendGuardBlock')}`;
const rememberBinding = block(/const rememberBinding = \(result\) => \{\n[\s\S]*?\n {2}\};\n/u, 'rememberBinding');
const rememberSent = block(/const rememberSent = \(result\) => \{\n[\s\S]*?\n {2}\};\n/u, 'rememberSent');
const rememberReceipt = block(/const rememberReceipt = \(session, result, readback\) => \{\n[\s\S]*?\n {2}\};\n/u, 'rememberReceipt');
const openDecision = between('const mine = sentReceipts.current[disputeId] || null;', '    setProviderDisputeDetail(result); setEvidencePreview(kept ? kept.result : null);');
const resetLine = 'sentReceipts.current = {}; boundByCaseRef.current = {}; sentByCaseRef.current = {}; setPreviewRefusal(null); setRestoredSend(null);';
assert.equal(app.split(resetLine).length - 1, 2, 'Reset demo and a new session forget pairings, sends and the restored note');
assert.ok(app.includes('writeStored(RAN_STORE_KEY, null); writeStored(SENT_STORE_KEY, null);'), 'Reset demo clears the stored receipts');

const label = (value, fallback = 'Needs review') => (value ? operatorLabel(value) : fallback);
const fakeStorage = () => {
  const map = new Map();
  return { map, getItem: (key) => (map.has(key) ? map.get(key) : null), setItem: (key, value) => map.set(key, String(value)), removeItem: (key) => map.delete(key) };
};
// One "page": module helpers bound to a tab storage, plus the component's own memory and handlers.
const page = (storage) => new Function('window', 'operatorLabel', 'displayDisputeId', `${storeSource}${guardSource}
  const sentReceipts = { current: {} }; const boundByCaseRef = { current: {} }; const sentByCaseRef = { current: {} };
  const setPreviewRefusal = () => {}; const setRestoredSend = () => {};
  ${rememberBinding}${rememberSent}${rememberReceipt}
  const open = (session, disputeId, result) => { ${openDecision} return { kept, restored }; };
  const reset = () => { ${resetLine} writeStored(SENT_STORE_KEY, null); };
  const guard = (caseRef, detail, preview) => sendGuardBlock(preview?.send_guard || null, detail, { case_ref: caseRef },
    boundByCaseRef.current[caseRef] || null, sentByCaseRef.current[caseRef] || null, preview?.dispute_id);
  return { open, reset, guard, rememberBinding, rememberSent, rememberReceipt, sentReceipts, boundByCaseRef, sentByCaseRef,
    readStoredReceipts, restoredSendState, keptSendText, maskDisputeId, SENT_STORE_KEY };`)({ sessionStorage: storage }, label, displayDisputeId);

const A = 'PP-R-AAA-XXXX0101';
const B = 'PP-R-BBB-XXXX7701';
const CASE = 'case-ref-001';
const session = { session_id: 'S'.repeat(24) };
const amount = { currency_code: 'USD', value: '48.00' };
const detail = (id, status = 'WAITING_FOR_SELLER_RESPONSE') => ({ dispute_id: id, status, reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', source: 'paypal_sandbox', dispute_amount: amount });
const preview = (id, p) => ({ dispute_id: id, case_ref: CASE, external_send: 'NOT_SUBMITTED',
  send_guard: { case_ref: CASE, case_reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', dispute_masked: p.maskDisputeId(id), bound_dispute_masked: p.maskDisputeId(id), dispute_amount: amount, send_refusal: null } });
const sent = (id) => ({ dispute_id: id, case_ref: CASE, external_send: 'SUBMITTED', paypal_debug_id: 'f2088142a6218', files: [], input: { evidences: [{ evidence_info: { tracking_info: [] } }] } });

// ---- (1) look-alikes never cross-match ------------------------------------------------------------------------------
{
  const storage = fakeStorage();
  const p = page(storage);
  assert.equal(p.maskDisputeId(A), p.maskDisputeId(B), 'the two codes share the short form (the collision under test)');
  assert.equal(p.maskDisputeId(A), 'PP-R-…01');
  // Pairing to A: A sends freely, B is locked and the line names A's full masked code.
  const pa = preview(A, p);
  p.rememberBinding(pa);
  assert.equal(p.boundByCaseRef.current[CASE], A, 'pairing key is the full code');
  assert.equal(p.guard(CASE, detail(A), pa), null, 'A, its own preview: not held');
  assert.equal(p.guard(CASE, detail(B), null), `Paired with ${A} (preview only). Reset demo to pair it with another dispute.`, 'B is locked by the pairing to A');
  assert.equal(p.guard(CASE, detail(B), pa), `Paired with ${A} (preview only). Reset demo to pair it with another dispute.`, 'A\'s preview cannot be used on B');
  // A preview whose full id is B's never counts for A, although the short forms match.
  p.reset();
  assert.equal(p.boundByCaseRef.current[CASE], undefined, 'reset clears the pairing');
  assert.equal(p.guard(CASE, detail(A), preview(B, p)), 'The preview is for another dispute; prepare it again for this one.', 'a look-alike preview is another dispute');
  // After Reset demo, B can be paired and A is now the locked one.
  const pb = preview(B, p);
  p.rememberBinding(pb);
  assert.equal(p.guard(CASE, detail(B), pb), null, 'after reset B pairs');
  assert.match(p.guard(CASE, detail(A), null), new RegExp(`^Paired with ${B}`, 'u'), 'and A is locked by B');
  p.reset();
  // Send on A: B says "already sent to" A's full code, never that B was sent.
  p.rememberBinding(pa);
  const sa = sent(A);
  p.rememberSent(sa); p.rememberReceipt(session, sa, null);
  assert.equal(p.sentByCaseRef.current[CASE], A, 'sent key is the full code');
  assert.equal(p.guard(CASE, detail(B), null), `This case was already sent to ${A}; it cannot also go to ${B}.`, 'B names A as the sent dispute');
  assert.deepEqual(Object.keys(JSON.parse(storage.getItem(p.SENT_STORE_KEY)).items), [A], 'only A stored, under its full code');
  assert.ok(typeof JSON.parse(storage.getItem(p.SENT_STORE_KEY)).items[A].sent_at === 'string', 'send time kept for the label');

  // Reload: a fresh page on the same tab storage. A's receipt comes back (read-back under review); B shows none.
  const q = page(storage);
  const openA = q.open(session, A, detail(A, 'UNDER_REVIEW'));
  assert.equal(openA.kept?.result.dispute_id, A, 'A: receipt restored');
  assert.equal(openA.restored.confirmed, true, 'A: confirmed by the read-back');
  assert.match(q.keptSendText(openA.restored), /^Kept in this tab from your send at \d\d:\d\d; PayPal read-back: Under review$/u, 'A: labelled as kept in this tab');
  q.rememberBinding(openA.kept.result); q.rememberSent(openA.kept.result);
  const openB = q.open(session, B, detail(B));
  assert.equal(openB.kept, null, 'B: no receipt after reload');
  assert.equal(openB.restored, null, 'B: no stored note either');
  assert.equal(q.guard(CASE, detail(B), null), `This case was already sent to ${A}; it cannot also go to ${B}.`, 'B after reload: still names A');
  assert.equal(Object.keys(q.sentReceipts.current).length, 0, 'stored rows are not copied into page memory');
  // Reset clears the stored receipt too.
  q.reset();
  assert.equal(storage.getItem(q.SENT_STORE_KEY), null, 'Reset demo drops stored receipts');
  assert.equal(page(storage).open(session, A, detail(A, 'UNDER_REVIEW')).kept, null, 'nothing restored after reset');
}

// ---- (2) stored records: old short keys dropped, tampered records never stamped ---------------------------------------
{
  const storage = fakeStorage();
  const p = page(storage);
  const row = { result: sent(A), readback: null, sent_at: '2026-11-11T01:02:00.000Z' };
  // An older entry under the short form, and one whose key and dispute_id disagree: both dropped.
  storage.setItem(p.SENT_STORE_KEY, JSON.stringify({ session_id: session.session_id, items: {
    'PP-R-…01': { ...row, result: { ...row.result, dispute_id: 'PP-R-…01' } }, [B]: row } }));
  assert.deepEqual(p.readStoredReceipts(session.session_id), {}, 'short-form key and mismatched key dropped, not misapplied');
  assert.equal(p.open(session, B, detail(B, 'UNDER_REVIEW')).kept, null, 'not applied to the look-alike B');

  // Tamper (B 6a): A's receipt copied under B's code, B never sent (WAITING_FOR_SELLER_RESPONSE): note only, no stamp.
  storage.setItem(p.SENT_STORE_KEY, JSON.stringify({ session_id: session.session_id, items: { [B]: { ...row, result: sent(B) } } }));
  const forged = p.open(session, B, detail(B));
  assert.equal(forged.kept, null, 'tampered record: no SUBMITTED card, nothing locked by it');
  assert.equal(forged.restored.confirmed, false);
  assert.match(p.keptSendText(forged.restored), /^Kept in this tab from your send at \d\d:\d\d; PayPal read-back: Waiting for seller response$/u, 'the note says where it came from and what PayPal reports');
  assert.equal(p.boundByCaseRef.current[CASE], undefined, 'no pairing taken from it');
  assert.equal(p.sentByCaseRef.current[CASE], undefined, 'no "sent to" taken from it');
  // Hand-built minimal record (B 6d) with a junk time and no read-back status: note only, time not invented.
  storage.setItem(p.SENT_STORE_KEY, JSON.stringify({ session_id: session.session_id, items: { [B]: { result: sent(B), sent_at: 'yesterday' } } }));
  const minimal = p.open(session, B, { ...detail(B), status: undefined });
  assert.equal(minimal.kept, null);
  assert.equal(p.keptSendText(minimal.restored), 'Kept in this tab from your send earlier in this visit; PayPal read-back: unavailable');
  // Another session's store is ignored altogether.
  storage.setItem(p.SENT_STORE_KEY, JSON.stringify({ session_id: 'T'.repeat(24), items: { [A]: row } }));
  assert.equal(p.open(session, A, detail(A, 'UNDER_REVIEW')).restored, null, 'other session: ignored');
  // Not JSON: ignored.
  storage.setItem(p.SENT_STORE_KEY, '{not json');
  assert.deepEqual(p.readStoredReceipts(session.session_id), {});
  // This page's own send is shown whatever the read-back says (it saw the SUBMITTED reply itself).
  const own = page(fakeStorage());
  own.rememberReceipt(session, sent(A), null);
  assert.equal(own.open(session, A, detail(A, 'WAITING_FOR_SELLER_RESPONSE')).kept.result.dispute_id, A, 'own send kept');
}

// ---- (2b) the screen: stamp only when confirmed, labelled; no Debug-Id invented -------------------------------------
{
  assert.ok(app.includes('const keptReceipt = Boolean(evidenceSent && restoredSend?.confirmed && restoredSend.dispute_id === evidencePreview?.dispute_id);'));
  assert.ok(app.includes('{keptReceipt && <span data-testid="send-receipt-kept">{keptSendText(restoredSend)}</span>}'), 'restored stamp is labelled');
  assert.ok(app.includes("PayPal request ID{keptReceipt ? ' (from that send, kept in this tab)' : ''}: {evidencePreview.paypal_debug_id || 'not returned'}"), 'Debug-Id is the stored one, labelled; never made up');
  const note = app.split('\n').find((line) => line.includes('data-testid="send-restored-note"'));
  assert.ok(note && note.includes('!restoredSend.confirmed') && !/paypal_debug_id|SUBMITTED to PayPal/u.test(note), 'unconfirmed note: no stamp and no Debug-Id');
  assert.equal(app.split('setRestoredSend(restored);').length - 1, 1, 'set from the fresh read only');
}

// ---- (3) phone bar: the send action waits after it appears -------------------------------------------------------------
{
  assert.ok(app.includes('const PHONE_SEND_HOLD_MS = 1200;'));
  assert.ok(app.includes("const PHONE_SEND_KEYS = ['evidence-submit', 'tracking-submit'];"));
  assert.ok(app.includes('const phoneSendHeld = PHONE_SEND_KEYS.includes(phoneActionKey) && Date.now() - phoneActionRef.current.at < PHONE_SEND_HOLD_MS;'));
  assert.ok(app.includes('disabled={phoneAction.disabled || phoneSendHeld}'), 'greyed out while held');
  assert.ok(app.includes('    if (phoneSendHeld) return;\n'), 'a tap while held does nothing');
  assert.ok(app.includes("const PHONE_SEND_HOLD_TEXT = 'Ready in a moment: check the preview above first.';") && app.includes('const phoneReason = phoneSendHeld && !phoneAction.disabled ? PHONE_SEND_HOLD_TEXT'), 'visible "ready in a moment" line');
  assert.ok(app.includes("onClick: () => setSendConfirm('evidence')"), 'the bar still opens the two-step dialog, never sends directly');
}

console.log('frontend_full_id_pairing_r2: ok');
