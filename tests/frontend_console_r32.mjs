import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// (r32 judges J1 J2 J4) Console fixes: a ready send looks ready (solid primary, no lock icon) and is the phone bar's
// action; one primary per Dispute step; the preview lock names "select a dispute" before one is picked; a deliberate
// Run Policy Check re-press renews the 2-minute window and the time left is on screen; system wording moved to Limits
// and safety; toasts top-right on desktop and inline on phones; lock lines tied to their buttons; dialogs return focus.
import { SELECT_DISPUTE_LOCK, sendLockReason } from '../frontend/src/lockReasons.js';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const block = (name) => {
  const start = app.indexOf(`function ${name}(`);
  assert.ok(start > 0, `${name} present`);
  return app.slice(start, app.indexOf('\n}\n', start));
};

// ---- J2 #6: the preview lock. Null exactly when Ready, now over the dispute-selected dimension too (416 combos). ----
const ready = ({ receipt, preview, block: held }) => Boolean(receipt) && preview?.submit_flag_enabled === true && preview?.source === 'paypal_sandbox' && preview?.external_send === 'FROZEN' && !held;
let combos = 0;
for (const disputeSelected of [false, true]) for (const draft of [null, { case_ref: 'case-ref-001' }]) for (const receipt of [null, { reviewer: 'r' }])
  for (const held of [null, 'Select a PayPal dispute first.'])
    for (const preview of [null, ...['FROZEN', 'SUBMITTED', 'BLOCKED'].flatMap((external_send) => ['paypal_sandbox', 'synthetic_fixture'].flatMap((source) => [true, false].map((submit_flag_enabled) => ({ external_send, source, submit_flag_enabled }))))])
      for (const kind of ['evidence', 'tracking']) {
        combos += 1;
        const reason = sendLockReason({ kind, draft, receipt, preview, block: held, disputeSelected });
        assert.equal(reason === null, ready({ receipt, preview, block: held }), JSON.stringify({ kind, draft, receipt, preview, held, disputeSelected }));
        // The loop is gone: with no dispute open and no preview, the line never asks for the preview.
        if (!disputeSelected && !preview && receipt) assert.equal(reason, SELECT_DISPUTE_LOCK);
        if (!disputeSelected && !preview) assert.equal(/preview/u.test(reason), false, reason);
      }
assert.equal(combos, 2 * 2 * 2 * 2 * 13 * 2);
assert.equal(SELECT_DISPUTE_LOCK, 'Locked: select a PayPal Sandbox dispute first.');
assert.equal(sendLockReason({ draft: {}, receipt: {}, disputeSelected: true }), 'Locked: prepare the evidence request preview first.', 'dispute open: the preview is the next step');
assert.equal(sendLockReason({ draft: {}, receipt: {}, sessionExpired: true, disputeSelected: false }), 'Locked: the demo session expired. Select Reconnect first.');
assert.ok(app.includes('disputeSelected: Boolean(providerDisputeDetail), sellerEvidence, refusal: evidenceRefusal });') && app.includes('disputeSelected: Boolean(providerDisputeDetail), refusal: trackingRefusal });'), 'App passes the dispute row state (r34: and the seller-evidence and refusal state)');

// ---- J4 P1-2 / J1: a ready send looks ready; one primary per step. ----
assert.ok(app.includes("data-testid=\"evidence-submit\" icon={evidenceSubmitReady ? 'arrow' : 'lock'} tone={evidenceSubmitReady ? 'blue' : 'ghost'}"), 'Submit: solid blue, no lock, when ready');
assert.ok(app.includes("data-testid=\"tracking-submit\" icon={trackingSubmitReady ? 'arrow' : 'lock'} tone={trackingSendTone}"), 'tracking: lock only while locked');
assert.ok(app.includes("const trackingSendTone = !trackingSubmitReady ? 'ghost' : evidenceSubmitReady ? 'secondary' : 'blue';"), 'tracking is secondary while the evidence send is next');
// The Ready flags that gate both sends are unchanged (the style follows them, it never enables anything).
assert.ok(app.includes('disabled={disabled || !evidenceSubmitReady}') && app.includes('disabled={disabled || !trackingSubmitReady}'));
const sendDialog = block('SendConfirmDialog');
assert.ok(sendDialog.includes("icon={left > 0 ? 'lock' : 'arrow'} disabled={left > 0 || sending}"), 'green Send: lock only during the hold');
assert.equal(sendDialog.includes('icon="lock"'), false);

// ---- J4 P1-2: phone bar = next step (preview, then the ready send), opening the same two-step dialog. ----
const bar = app.slice(app.indexOf('const phoneAction = '), app.indexOf('const phoneActionKey'));
assert.ok(bar.includes("? { key: 'evidence-submit', label: 'Submit to PayPal Sandbox (test)', icon: 'arrow', onClick: () => setSendConfirm('evidence'), disabled: disabled || !evidenceSubmitReady"), 'bar: Submit when it is next');
assert.ok(bar.includes("? { key: 'tracking-submit', label: 'Send tracking to PayPal Sandbox (test)', icon: 'arrow', onClick: () => setSendConfirm('tracking'), disabled: disabled || !trackingSubmitReady"), 'bar: tracking when it is next');
assert.ok(bar.indexOf("key: 'evidence-submit'") < bar.indexOf("key: 'tracking-submit'"), 'evidence first');
assert.ok(bar.includes("? { key: 'evidence-preview', label: 'Prepare evidence request (preview)', icon: 'file', onClick: previewEvidence"), 'bar: preview after the review');
assert.equal(/submitEvidence|submitTracking|confirmSend/u.test(bar), false, 'the bar never sends directly');
assert.ok(app.includes('inert={warningOpen || draftConfirm || resetConfirm || sendConfirm ? true : undefined}'), 'bar inert while the send dialog is open');

// ---- J4 P1-1: Run Policy Check re-press renews the window; the time left is shown. ----
const guard = app.slice(app.indexOf('const runPolicyCheck = () => {'), app.indexOf('const scan = () =>'));
const renew = guard.indexOf('if (Date.now() - aupCheckedAtRef.current >= AUP_RENEW_AFTER_MS) { scan(); return; }');
assert.ok(renew > 0 && guard.indexOf('if (busyRef.current) return;') < renew, 'busy first');
assert.ok(guard.indexOf("if (coolingNow('aup')) return;") < renew, 'Retry-After still holds the renewal');
assert.ok(guard.indexOf('if (aup && !aupConsumed) {') < renew, 'only for the result on screen');
assert.ok(app.includes('aupCheckedTextRef.current = description; aupCheckedAtRef.current = Date.now();'), 'time of the shown check');
const validFor = block('AupValidFor');
assert.ok(validFor.includes("<span aria-hidden=\"true\">Check valid for {Math.floor(left / 60)}:{String(left % 60).padStart(2, '0')} more</span>"), 'visible m:ss');
assert.ok(validFor.includes('<span className="sr-only">This check is valid for 2 minutes.</span>'), 'announced once');
assert.ok(app.includes('<AupValidFor key={`valid-${aup.evaluation_id}`} expiresAt={aup.expires_at} />'));
const fmt = (left) => `${Math.floor(left / 60)}:${String(left % 60).padStart(2, '0')}`;
assert.equal(fmt(72), '1:12'); assert.equal(fmt(120), '2:00'); assert.equal(fmt(9), '0:09');

// ---- J1: system wording out of the main reading path, disclosures kept. ----
assert.ok(app.includes("{productRef?.status !== 'OFF' && <ProductReference "), 'no "Product lookup is off" card in the result');
assert.ok(app.includes('Product lookup is off on this console (no Channel3 key), so no product cards are shown. The policy result does not use it.'), 'kept in Limits and safety');
assert.ok(app.includes("{receipt.reviewer === 'DEMO_OPERATOR_UNAUTHENTICATED' ? 'Demo operator (no sign-in)' : operatorLabel(receipt.reviewer)} ·"), 'plain reviewer words');
assert.equal(app.includes('identity not authenticated'), false, 'the alarming label is not used by the console');
assert.ok(app.includes("The local review is recorded for a demo operator. This demo has no sign-in, so the reviewer's identity is not checked."), 'disclosure kept');

// ---- J4: toasts never over the form. ----
assert.match(css, /\.feedback-region \{ position: fixed; right: max\(18px, calc\(\(100vw - 1200px\) \/ 2\)\); top: 164px;/u, 'desktop: top-right under the step bar');
assert.ok(css.includes('  .feedback-region { position: static; width: auto; margin: 0 16px; }'), 'phone: inline');
assert.ok(app.includes('{info.text}<button type="button" className="icon-button" aria-label="Dismiss message" data-testid="console-info-dismiss"'), 'every info message dismissible');

// ---- J4 a11y: lock lines described-by; focus back to the opener. ----
assert.ok(block('LockReason').includes('<p className="lock-reason" id={testId} data-testid={testId}>'));
for (const [button, id] of [['evidence-submit', "aria-describedby={evidenceLock ? 'evidence-lock-reason' : undefined}"], ['tracking-submit', "aria-describedby={trackingLock ? 'tracking-lock-reason' : undefined}"],
  ['invoice-review', 'aria-describedby="invoice-lock-reason"'], ['invoice-create', 'aria-describedby="invoice-lock-reason"'], ['dispute-approve', 'aria-describedby="approve-lock-reason"']]) {
  const at = app.indexOf(`<Button data-testid="${button}"`);
  assert.ok(at > 0 && app.slice(at, app.indexOf('onClick', at)).includes(id), `${button} -> ${id}`);
}
const restore = block('restoreFocus');
assert.ok(restore.includes('element.isConnected && !element.disabled'), 'a usable element only');
assert.ok(sendDialog.includes('return () => restoreFocus(trigger, returnFocus);'));
assert.ok(block('useDialogFocus').includes('return () => restoreFocus(trigger, returnFocus);'));
assert.ok(app.includes('returnFocus={[`[data-testid="${sendConfirm}-submit"]`, `[data-testid="phone-action-${sendConfirm}-submit"]`]}'), 'send dialog returns to its Submit');
assert.ok(app.includes(`returnFocus={['[data-testid="invoice-create"]', '[data-testid="phone-action-invoice"]']}`), 'draft dialog returns to Create');
assert.ok(app.includes('const keyDown = useDialogFocus(boxRef, onCancel, returnFocus);'));

console.log(JSON.stringify({ status: 'PASS', checks: [`send lock reasons ${combos} combos`, 'ready send style', 'phone bar next step', 'policy renew + time left', 'wording moved', 'toast placement', 'a11y'] }));
