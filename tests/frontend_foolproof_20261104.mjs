import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// (foolproofing 2026-11-04) Every action that writes to PayPal Sandbox, spends the Studio allowance or wipes the
// session asks first: the invoice draft gets the same two steps as a send, Reset demo asks once, and the evidence
// result shows PayPal's Debug-Id. Checked on the source, like frontend_send_guard_r25.mjs.
const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const block = (name) => {
  const start = app.indexOf(`function ${name}(`);
  assert.ok(start > 0, `${name} present`);
  return app.slice(start, app.indexOf('\n}\n', start));
};

// Invoice draft: no button calls createInvoice directly; only the dialog's green button does, after the hold.
assert.equal((app.match(/onClick[=:]\s*\{?createInvoice\b/gu) || []).length, 0, 'no button creates a draft in one click');
assert.equal((app.match(/onClick[:=] ?\{?\(\) => setDraftConfirm\(true\)/gu) || []).length, 2, 'desktop button and phone bar both open the dialog');
assert.match(app, /onCreate=\{async \(\) => \{ setDraftConfirm\(false\); await createInvoice\(\); \}\}/u);
const draft = block('DraftConfirmDialog');
assert.match(draft, /data-testid="draft-confirm-continue" className="button-confirm-continue"[^>]*disabled=\{!checked\}/u, 'orange Continue needs the tick');
assert.match(draft, /data-testid="draft-confirm-create" className=\{`button-confirm-send\$\{left > 0 \? ' is-holding' : ''\}`\}[^>]*disabled=\{left > 0 \|\| creating\}/u, 'green Create waits for the hold and runs once');
assert.match(draft, /useState\(SEND_HOLD_SECONDS\)/u);
assert.match(draft, /It is not sent to the buyer\./u);
for (const id of ['draft-confirm-description', 'draft-confirm-amount', 'draft-confirm-route', 'draft-confirm-tick', 'draft-confirm-back', 'draft-confirm-cancel']) {
  assert.ok(draft.includes(`data-testid="${id}"`), id);
}
assert.match(draft, /role="dialog" aria-modal="true"/u);

// Reset demo: the button only opens the dialog; the dialog's button runs the reset.
assert.match(app, /data-testid="demo-reset"[^\n]*onClick=\{\(\) => setResetConfirm\(true\)\}>Reset demo<\/Button>/u);
assert.equal((app.match(/inject\('reset'\)/gu) || []).length, 1, 'one reset path');
assert.match(app, /const runReset = \(\) => \{ setResetConfirm\(false\);[^\n]*inject\('reset'\)/u);
const reset = block('ResetConfirmDialog');
assert.match(reset, /data-testid="reset-confirm-reset"[^>]*onClick=\{onReset\}/u);
assert.match(reset, /Your text and the Sandbox connection stay\. A draft already in PayPal Sandbox is not deleted\./u);

// Shared focus handling: Escape cancels in both new dialogs.
const focus = block('useDialogFocus');
assert.match(focus, /event\.key === 'Escape'\) \{ event\.preventDefault\(\); onCancel\(\);/u);

// Send dialog: amount and opening date sit next to the 2-character masked dispute id.
const send = block('SendConfirmDialog');
assert.match(send, /function SendConfirmDialog\(\{ kind, guard, detail,/u);
assert.ok(send.includes('data-testid="send-confirm-amount"') && send.includes('data-testid="send-confirm-opened"'));
assert.match(app, /<SendConfirmDialog kind=\{sendConfirm\} detail=\{providerDisputeDetail\}/u);

// Evidence result: PayPal's Debug-Id is visible, not only inside Technical details.
// (fix r1 U4) Only until the send: after it the SUBMITTED card carries the one Debug-Id line.
assert.match(app, /\{!evidenceSent && evidencePreview\.paypal_debug_id && <p className="evidence-debug-id" data-testid="evidence-debug-id">PayPal-Debug-Id: \{evidencePreview\.paypal_debug_id\}<\/p>\}/u);

// Colours are the send dialog's (orange then green), already contrast-checked in frontend_send_guard_r25.mjs.
// (P4 2026-11-12) Continue is the ink primary token (the orange #c2410c left the palette); Send stays sage green.
assert.match(css, /\.button\.button-confirm-continue \{ background: var\(--pg-color-accent\);/u); // round 5: charcoal, not ink
assert.match(css, /\.button\.button-confirm-send \{ background: #4a6a4e;/u);

// (r30 J2 P2-1) The server's single-use confirmation: the dialog's re-check keeps it and the send carries it.
const api = readFileSync(new URL('../frontend/src/api.js', import.meta.url), 'utf8');
// (r31 J5 A6) The logic itself lives in sendConfirm.js and is tested by behaviour in frontend_send_confirm_r31.mjs;
// here the console must use it at the same three points: re-check (after the payload and guard checks), send, clear.
const recheck = app.slice(app.indexOf('const recheckSend = async (kind) => {'), app.indexOf('const confirmSend = async (kind) => {'));
assert.ok(recheck.indexOf('sendConfirmTokens.current.clear(kind);') < recheck.indexOf('await apiRequest('), 'a re-check first drops the old token');
assert.ok(recheck.indexOf('if (!before?.payload_sha256 || fresh.payload_sha256 !== before.payload_sha256 || held) {') < recheck.indexOf('sendConfirmTokens.current.remember(kind, fresh);'), 'kept only after the payload and guard checks pass');
assert.match(app, /const submitEvidence = \(\) => action\('evidence-submit', async \(session\) => \{\n    const result = await apiRequest\('\/paypal\/disputes\/provide-evidence', \{ method: 'POST', body: sendConfirmTokens\.current\.submitBody\('evidence', \{ dispute_id: providerDisputeDetail\.dispute_id, case_ref: caseItem\.case_ref \}\), session \}\);/u);
assert.match(app, /const submitTracking = \(\) => action\('tracking-submit', async \(session\) => \{\n    const result = await apiRequest\('\/paypal\/disputes\/add-tracking', \{ method: 'POST', body: sendConfirmTokens\.current\.submitBody\('tracking', \{ dispute_id: providerDisputeDetail\.dispute_id, case_ref: caseItem\.case_ref \}\), session \}\);/u);
assert.match(app, /await \(kind === 'tracking' \? submitTracking\(\) : submitEvidence\(\)\);\n    sendConfirmTokens\.current\.clear\(kind\);/u);
assert.equal((app.match(/^(?!\s*\/\/).*submit: true/gmu) || []).length, 0, 'no other path builds a submit body (comments aside)');
assert.equal((app.match(/sendConfirmTokens\.current\.clearAll\(\);/gu) || []).length, 3, 'new session, expired session and Reset demo drop both tokens');
// The add-tracking response keeps the original optional list; the provide-evidence response also allows `sent_files`
// (the plain SHA-256 of each file a send posted) and checks its shape.
assert.equal((api.match(/optional\('payload_sha256', 'send_guard', 'confirm_token'\)\]\) && sendGuardValid && confirmTokenValid(?! && sentFilesValid)/gu) || []).length, 1);
assert.equal((api.match(/optional\('payload_sha256', 'send_guard', 'confirm_token', 'sent_files'\)\]\) && sendGuardValid && confirmTokenValid && sentFilesValid/gu) || []).length, 1);

console.log(JSON.stringify({ status: 'PASS', checks: ['draft two-step', 'reset confirm', 'send dialog amount and date', 'evidence debug id', 'server send confirmation'] }));
