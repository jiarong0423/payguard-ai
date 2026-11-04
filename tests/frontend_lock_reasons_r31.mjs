import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// (r31 judges A2/A3/A4) The "Session resumed" text comes from what the server really holds; the ~2-minute policy
// expiry says so (neutral message, the draft dialog keeps a line, the locked buttons say why); every locked primary
// action shows one seller-readable line. The pure parts are tested by behaviour, the wiring on the source.
import { approveLockReason, draftLockReason, POLICY_EXPIRED_LOCK, SESSION_LOCK, sendLockReason } from '../frontend/src/lockReasons.js';
import { resumedNotice } from '../frontend/src/resumeNotice.js';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const block = (name) => {
  const start = app.indexOf(`function ${name}(`);
  assert.ok(start > 0, `${name} present`);
  return app.slice(start, app.indexOf('\n}\n', start));
};
const seen = new Set();
const note = (text) => { if (text) seen.add(text); return text; };

// ---- A2: Session resumed ----
assert.equal(resumedNotice(null, []), null);
const emptyAfterReset = { transactions: [], disputes: [], scenario: { burst: false, dispute: false } };
assert.equal(resumedNotice(emptyAfterReset, []), null, 'Reset demo then reload: no message at all');
assert.equal(resumedNotice({ transactions: [{}, {}], disputes: [] }, []),
  'Session resumed: sample sales are back. Policy and country check results are not kept; run them again.');
assert.equal(resumedNotice({ transactions: [], disputes: [{ status: 'needs_review' }] }, []),
  'Session resumed: 1 dispute case is back. Policy and country check results are not kept; run them again.');
assert.equal(resumedNotice({ transactions: [{}], disputes: [{ status: 'draft_ready' }, { status: 'local_draft_reviewed' }] }, [{ case_ref: 'case-ref-001' }, { case_ref: 'case-ref-002' }]),
  'Session resumed: sample sales, 2 dispute cases, 2 evidence drafts and 1 recorded local review are back. Policy and country check results are not kept; run them again.');
assert.equal(/samples and dispute drafts are back/u.test(app), false, 'the old fixed text is gone');
assert.ok(app.includes("const resumed = resumedNotice(nextState, drafts);\n        if (resumed) setInfo({ kind: 'resumed', text: resumed });"), 'shown only when something came back');
// (r32 J4) Every lasting info message (resumed, already checked, expired) can be dismissed.
assert.ok(app.includes("{info.text}<button type=\"button\" className=\"icon-button\" aria-label=\"Dismiss message\" data-testid=\"console-info-dismiss\" onClick={() => setInfo(null)}>"), 'dismissible');
assert.ok(css.includes('.feedback-region .message-info[data-testid="console-info"] { pointer-events: auto; }'), 'the close button takes taps');
assert.match(css, /\.message-info \.icon-button \{ min-width: 44px; min-height: 44px;/u, '44 px target');

// ---- A3: the 120 s policy result ----
// (b) neutral info, not the green notice.
assert.ok(app.includes("setNotice(''); setInfo({ kind: 'expired', text: 'The description check expired. Run it again before continuing.' });"), 'expiry is a neutral info');
assert.equal(app.includes("setNotice('The description check expired"), false, 'no green toast for the expiry');
// (a) the open draft dialog stays with a message instead of closing itself.
assert.ok(app.includes("const DRAFT_EXPIRED_TEXT = 'The check expired after 2 minutes. Run Policy Check again, then create the draft.';"));
assert.ok(app.includes('invalidateAup(); setAupExpired(true); if (draftConfirmRef.current) setDraftExpired(true);'), 'expiry marks an open dialog');
assert.ok(app.includes("if (draftConfirm && ((!invoiceReview && !draftExpired) || disabled || countryHeld || sandbox?.status !== 'connected')) setDraftConfirm(false);"), 'only the expiry keeps it open');
assert.ok(app.includes('useEffect(() => { if (!draftConfirm) setDraftExpired(false); }, [draftConfirm]);'), 'a new dialog starts unexpired');
const draftDialog = block('DraftConfirmDialog');
assert.match(draftDialog, /\{expired \? <>\s*<p className="send-confirm-expired" role="alert" data-testid="draft-confirm-expired"><Icon name="clock" size=\{16\} \/>\{DRAFT_EXPIRED_TEXT\}<\/p>/u);
const expiredBranch = draftDialog.slice(draftDialog.indexOf('{expired ? <>'), draftDialog.indexOf(': step === 1 ? <>'));
assert.equal(expiredBranch.includes('draft-confirm-create') || expiredBranch.includes('draft-confirm-continue'), false, 'nothing can be created after expiry');
assert.ok(expiredBranch.includes('data-testid="draft-confirm-expired-back"'));
assert.ok(app.includes('expired={draftExpired}'));
// The durations are the server's: 120 s policy result (store.py) and 3 s hold; the console does not change them.
const store = readFileSync(new URL('../backend/app/store.py', import.meta.url), 'utf8');
assert.ok(store.includes('expires = min(session.expires_at, now + timedelta(seconds=120))'), 'policy result 120 s');
assert.ok(app.includes('const SEND_HOLD_SECONDS = 3;') && app.includes('const AUP_WARN_MS = 30000;'));
// (c) Confirm Draft Context greyed by the expiry says why.
assert.equal(draftLockReason({ aup: null, aupExpired: true }), POLICY_EXPIRED_LOCK);
assert.equal(POLICY_EXPIRED_LOCK, 'Locked: the description check expired after 2 minutes. Run Policy Check again.');

// ---- A4: draft pair ----
const draftBase = { aup: { evaluation_id: 'e' }, invoiceChecked: true, connected: true };
assert.equal(note(draftLockReason({})), 'Locked: run Policy Check on the description first.');
assert.equal(note(draftLockReason({ ...draftBase, sessionExpired: true })), SESSION_LOCK);
assert.equal(draftLockReason({ ...draftBase, countryHeld: true }), null, 'the country Stop line already sits next to it');
assert.equal(note(draftLockReason({ ...draftBase, descriptionTooLong: true })), 'Locked: shorten the description to 200 characters first.');
assert.equal(note(draftLockReason({ ...draftBase, invoiceChecked: false })), 'Locked: tick the box above to confirm the draft context.');
assert.equal(note(draftLockReason(draftBase)), 'Locked: confirm the draft context first, then create the draft.');
assert.equal(draftLockReason({ ...draftBase, hosted: true }), null, 'hosted: the draft note covers Create');
const consumed = { ...draftBase, aupConsumed: true, invoiceReview: { review_token: 'r' } };
assert.equal(draftLockReason(consumed), null, 'Create is usable');
assert.equal(note(draftLockReason({ ...consumed, invoiceChecked: false })), 'Locked: tick the box above first.');
assert.equal(note(draftLockReason({ ...consumed, connected: false })), 'Locked: connect the US Sandbox first.');
assert.equal(note(draftLockReason({ ...consumed, invoiceReview: null })), 'Locked: confirm the draft context first.');
assert.equal(draftLockReason({ ...consumed, invoiceReview: null, invoice: { invoice_id: 'INV2-X' } }), null, 'draft created: nothing locked');
note(POLICY_EXPIRED_LOCK);
// The inputs are the button's own disabled conditions.
assert.ok(app.includes("disabled={disabled || countryHeld || !invoiceChecked || !aup || aupConsumed || description.length > 200}"), 'Confirm Draft Context');
assert.ok(app.includes("disabled={disabled || countryHeld || !invoiceReview || !invoiceChecked || sandbox?.status !== 'connected'}"), 'Create Sandbox draft');
assert.ok(app.includes("<LockReason testId=\"invoice-lock-reason\" reason={draftLockReason({ sessionExpired: error?.status === 401, hosted, countryHeld, aup, aupExpired, aupConsumed,\n          descriptionTooLong: description.length > DESCRIPTION_LIMIT, invoiceChecked, invoiceReview, invoice, connected: sandbox?.status === 'connected' })} /></div>"));

// ---- A4: sends. sendLockReason is null exactly when the console's Ready flag is true. ----
const readyFormula = "Boolean(receipt) && evidencePreview?.submit_flag_enabled === true && evidencePreview?.source === 'paypal_sandbox' && evidencePreview?.external_send === 'FROZEN' && !evidenceBlock";
// (r34 #2) The evidence send also stays locked while PayPal already has seller evidence for the dispute.
assert.ok(app.includes(`const evidenceSubmitReady = ${readyFormula} && !sellerEvidence;`), 'evidence Ready flag (r34: plus seller evidence)');
assert.ok(app.includes(`const trackingSubmitReady = ${readyFormula.replaceAll('evidence', 'tracking')};`), 'tracking Ready flag unchanged');
const ready = ({ receipt, preview, block }) => Boolean(receipt) && preview?.submit_flag_enabled === true && preview?.source === 'paypal_sandbox' && preview?.external_send === 'FROZEN' && !block;
let combos = 0;
for (const draft of [null, { case_ref: 'case-ref-001' }]) for (const receipt of [null, { reviewer: 'r' }]) for (const block of [null, 'Select a PayPal dispute first.'])
  for (const preview of [null, ...['FROZEN', 'SUBMITTED', 'BLOCKED'].flatMap((external_send) => ['paypal_sandbox', 'synthetic_fixture'].flatMap((source) => [true, false].map((submit_flag_enabled) => ({ external_send, source, submit_flag_enabled }))))])
    for (const kind of ['evidence', 'tracking']) {
      combos += 1;
      const reason = note(sendLockReason({ kind, draft, receipt, preview, block }));
      assert.equal(reason === null, ready({ receipt, preview, block }), JSON.stringify({ kind, draft, receipt, preview, block }));
    }
assert.equal(combos, 2 * 2 * 2 * 13 * 2);
const sandboxPreview = { external_send: 'FROZEN', source: 'paypal_sandbox', submit_flag_enabled: false };
assert.equal(sendLockReason({ draft: {}, receipt: {}, preview: sandboxPreview }), 'Locked: sending is turned off on this console.');
assert.equal(sendLockReason({ draft: {}, receipt: null, preview: sandboxPreview }), 'Locked: confirm the local review first.');
assert.equal(sendLockReason({ draft: null }), 'Locked: prepare the evidence draft first.');
assert.equal(sendLockReason({ kind: 'tracking', draft: {}, receipt: {} }), 'Locked: preview the tracking for PayPal first.');
assert.equal(sendLockReason({ draft: {}, receipt: {}, preview: sandboxPreview, sessionExpired: true }), SESSION_LOCK);
assert.ok(app.includes("const evidenceLock = sendLockReason({ kind: 'evidence', sessionExpired, draft, receipt, preview: evidencePreview, block: evidenceBlock, disputeSelected: Boolean(providerDisputeDetail), sellerEvidence, refusal: evidenceRefusal });"));
assert.ok(app.includes("const trackingLock = sendLockReason({ kind: 'tracking', sessionExpired, draft, receipt, preview: trackingPreview, block: trackingBlock, disputeSelected: Boolean(providerDisputeDetail), refusal: trackingRefusal });"));
assert.ok(app.includes('>Submit to PayPal Sandbox (test)</Button><LockReason testId="evidence-lock-reason" reason={evidenceLock} />'));
assert.ok(app.includes('>Send tracking to PayPal Sandbox (test)</Button><LockReason testId="tracking-lock-reason" reason={trackingLock} />'));

// ---- A4: Confirm local draft review ----
const draftReady = { draft_digest: 'd', routing: { overall_state: 'READY_FOR_LOCAL_REVIEW' } };
assert.equal(approveLockReason({ draft: draftReady, reviewChecked: true }), null);
assert.equal(note(approveLockReason({ draft: draftReady })), 'Locked: tick the review box above first.');
assert.equal(note(approveLockReason({ draft: { ...draftReady, routing: { overall_state: 'NEEDS_SELLER_INPUT' } } })), 'Locked: this draft is not ready for a local review.');
assert.equal(approveLockReason({ draft: draftReady, receipt: { reviewer: 'r' } }), null, 'recorded: the button says so');
assert.equal(approveLockReason({ draft: draftReady, reviewedOnServer: true }), null);
assert.ok(app.includes('<LockReason testId="approve-lock-reason" reason={approveLockReason({ sessionExpired: error?.status === 401, draft, receipt, reviewedOnServer, reviewChecked })} />'));

// Every line: one short sentence a seller can read; never an environment variable or an API path.
for (const text of seen) {
  assert.ok(/^(Locked|Sent): /u.test(text), text);
  assert.equal(/PAYGUARD_|[A-Z]{3,}_[A-Z]{3,}|=|\/v1\//u.test(text), false, `no operator detail: ${text}`);
  assert.ok(text.length <= 96, `compact on a 360 px phone: ${text} (${text.length})`);
}
assert.ok(seen.size >= 16, `${seen.size} distinct lines seen`);
const lockReason = block('LockReason');
assert.match(lockReason, /if \(!reason\) return null;/u);
assert.match(lockReason, /<p className="lock-reason" id=\{testId\} data-testid=\{testId\}><Icon name="lock" size=\{14\} \/><span>\{reason\}<\/span><\/p>/u);
assert.match(css, /\.lock-reason \{ display: flex; flex-basis: 100%;/u, 'own row under the button');

console.log(JSON.stringify({ status: 'PASS', checks: ['resumed text from state', 'expiry neutral + dialog line', 'draft lock reasons', `send lock reasons ${combos} combos`, 'approve lock reasons', 'no env names'] }));
