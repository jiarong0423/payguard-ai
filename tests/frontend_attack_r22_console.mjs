// attack r22 (2026-11-03): main-console fixes from the desktop and phone attack reports stay pinned.
// The behaviour was checked in headless Chrome against the built console; this file pins the source so a later edit
// cannot quietly undo it.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../frontend/${path}`, import.meta.url), 'utf8');
const app = read('src/App.jsx');
const panel = read('src/CountryRules.jsx');
const guide = read('src/GuideLive.jsx');
const css = read('src/index.css');
const html = read('index.html');

// Desktop P1: focus after Reset demo from 02/03 and after Confirm local draft review. A single requestAnimationFrame
// was not enough; the move is tried at once, then on the next frame or after a timeout, with a late check.
{
  const flush = app.slice(app.indexOf('const flushFocus = () => {'), app.indexOf('const focusWhenIdle = '));
  assert.ok(flush.includes('attempt();'), 'focus move is tried at once');
  assert.ok(flush.includes('afterRender(attempt);'), 'and retried on the next frame or timeout');
  assert.ok(flush.includes('if (tries > FOCUS_RETRIES) return;'), 'retries are bounded');
  assert.ok(flush.includes("if (token !== focusTokenRef.current || (tries > 0 && !lost())) return;"), 'a newer request or a seller who moved on stops the retries');
  assert.ok(flush.includes("behavior: 'instant'"), 'an off-screen target jumps into view when the smooth scroll never ran');
  assert.ok(!flush.includes('window.requestAnimationFrame(() => {'), 'no rAF-only focus move');
}
assert.ok(app.includes("const afterRender = (run) => { let done = false; const once = () => { if (!done) { done = true; run(); } }; window.requestAnimationFrame(once); window.setTimeout(once, FOCUS_RETRY_MS); };"), 'frame-or-timeout helper');
assert.ok(app.includes("focusWhenIdle(['[data-testid=\"dispute-result\"]'], { scroll: true });"), 'approve focuses the receipt');
assert.ok(app.includes("focusWhenIdle(['#compliance [data-testid=\"demo-reset\"]', '#stage-trigger-compliance'], { scroll: 'fallback' });"), 'Reset focuses step 01 Reset demo');
assert.ok(app.includes('<div className="receipt" data-testid="dispute-result" tabIndex={-1}>'), 'receipt takes focus');

// P2: over 200 characters, Run Policy Check is visibly disabled (aria-disabled) and its click shows the message.
assert.ok(app.includes("aria-disabled={busyHold || blocked || undefined}"), 'Button blocked state is aria-disabled');
assert.ok(app.includes("blocked={Boolean(descriptionProblem(description))} aria-describedby={descriptionProblem(description) ? 'description-note' : undefined}"), 'in-page Run Policy Check blocked with the note');
assert.ok(app.includes("blocked: Boolean(descriptionProblem(description))"), 'phone bar Run Policy Check blocked too');
assert.ok(css.includes('.button.is-blocked { cursor: not-allowed; opacity: .45; }'), 'blocked looks disabled');

// P2: one policy check at a time, and no repeat while a result for this exact text is showing (desktop CPU x6 and the
// phone bar's repeated taps both burned the 5-per-2-minute budget).
{
  const guard = app.slice(app.indexOf('const runPolicyCheck = () => {'), app.indexOf('const scan = () =>'));
  assert.ok(guard.indexOf('if (busyRef.current) return;') > -1 && guard.indexOf('if (busyRef.current) return;') < guard.indexOf('scan();'), 'busy clicks ignored');
  assert.ok(guard.includes('if (aup && !aupConsumed) {') && guard.indexOf('if (aup && !aupConsumed) {') < guard.indexOf('scan();'), 'fresh result: no repeat request');
  // attack r23: neutral info that stays until the description changes, not the green toast.
  // (r32 J4 P1-1) A press 30 s or more after the check runs it again (new 2-minute window); a burst still sends nothing.
  assert.ok(guard.includes("setInfo({ kind: 'already', text: 'Already checked. To restart the 2-minute window, press Run Policy Check again 30 seconds after a check.' });"), 'repeat click says why');
  assert.ok(guard.includes('if (Date.now() - aupCheckedAtRef.current >= AUP_RENEW_AFTER_MS) { scan(); return; }'), 'renewal only after the settle time');
  assert.ok(app.includes('const AUP_RENEW_AFTER_MS = 30000;'), 'renewal settle time');
}

// P2: the phone bar's Check country rules shows loading and aria-busy from the panel's own request.
assert.ok(panel.includes('export default function CountryRules({ session, onResult, onContinue, onSessionExpired, onBusy, onExample, autoExample = false, verdictTarget = null }) {'), 'panel reports busy (P3 2026-11-12: autoExample prop added; R5 2026-11-12: verdictTarget slot under the sample cards)');
assert.ok(panel.includes('useEffect(() => { onBusy?.(busy); }, [busy]);'), 'busy forwarded');
assert.ok(app.includes('onBusy={setCountryBusy}') && app.includes('loading: countryBusy })'), 'bar uses it');

// P2: after Confirm Draft Context the bar offers the draft step's action, not Run Policy Check.
assert.ok(app.includes(": invoiceReview ? (hosted ? null : sandbox?.status === 'connected'"), 'bar follows the bound draft context');
// (foolproofing 2026-11-04) The bar's Create Sandbox draft opens the two-step dialog, like the in-page button.
assert.ok(app.includes("{ key: 'invoice', label: 'Create Sandbox draft', icon: 'file', onClick: () => setDraftConfirm(true),"), 'connected: Create Sandbox draft');
assert.ok(app.includes("{ key: 'connect', label: 'Connect US Sandbox', icon: 'link', onClick: connectSandbox,"), 'not connected: connect first');
assert.ok(css.includes('.app-shell.phone-action-invoice [data-testid="invoice-create"]'), 'in-page twin hides like the others');

// P2: long-press on the bar selects no text.
assert.ok(css.includes('.phone-action-bar, .phone-action-bar * { -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; }'), 'bar not selectable');

// P2: error banner close button is 44px and the offline text is plain.
// (UI r5) The error is .tg-toast (theme/components.css) now; .message-error is gone.
assert.ok(readFileSync(new URL('../frontend/src/theme/components.css', import.meta.url), 'utf8').includes('.tg-toast .icon-button { min-width: 44px; min-height: 44px; }'), '44px close button');
assert.ok(guide.includes("export const OFFLINE_TEXT = 'TradeGlot could not be reached. Check your internet connection, then try again.';"), 'plain offline sentence');
assert.ok(guide.includes("failure?.code === 'backend_unavailable' ? OFFLINE_TEXT"), 'offline code mapped');
// attack r23: waitFailureMessage wraps plainFailureMessage and only drops a fixed Retry-After sentence.
assert.ok(guide.includes('? withoutFixedWait(plainFailureMessage(failure, fallback)) : plainFailureMessage(failure, fallback));'), 'wait wrapper keeps the plain text');
assert.ok(app.includes('<span>{waitFailureMessage(error)}'), 'console banner uses it');
assert.ok(!guide.includes("failure.message || 'The request failed. Try again.'"), 'guide errors use it');
assert.equal((panel.match(/waitFailureMessage\(failure/g) || []).length, 2, 'country panel errors use it');

// P2: an invalid amount is not focused on a touch screen (the keyboard hid the message); the message scrolls into view.
assert.ok(app.includes("if (!coarsePointer()) document.getElementById('invoice-amount')?.focus({ preventScroll: true });"), 'draft amount: no keyboard on touch');
assert.ok(app.includes("document.getElementById('invoice-amount-note')?.scrollIntoView({ block: 'center' });"), 'draft amount message in view');
assert.ok(panel.includes("if (!window.matchMedia('(pointer: coarse)').matches) document.getElementById('country-amount-input')?.focus({ preventScroll: true });"), 'country amount: no keyboard on touch');
assert.ok(panel.includes("document.getElementById('country-amount-note')?.scrollIntoView({ block: 'center' });"), 'country amount message in view');

// P2: a slow first load shows a static message that the app replaces.
assert.ok(html.includes('<div id="root"><div class="boot-loading" role="status" data-testid="boot-loading">'), 'static loading message inside #root');
assert.ok(/<style>[\s\S]*\.boot-loading \{/.test(html), 'styled without the app CSS');

// P2: print hides the step bar, toasts and the phone bar; very short viewports get a non-sticky step bar.
assert.ok(css.includes('@media print {\n  .journey, .feedback-region, .phone-action-bar, .skip-link { display: none !important; }'), 'print rules');
assert.ok(css.includes('@media (max-height: 480px) { .journey { position: static; } }'), 'short viewport rule');

// P2: the phone top bar links to Scenarios where it fits (hosted from 360px, local from 540px).
assert.ok(css.includes('.topbar[data-hosted="true"] nav a[data-testid="topbar-scenarios"] { display: inline-flex; }'), 'hosted phone bar shows Scenarios');
assert.ok(css.includes('@media (min-width: 540px) and (max-width: 640px) {\n  .topbar nav { gap: 12px; }\n  .topbar nav a[data-testid="topbar-scenarios"] { display: inline-flex; }'), 'local phone bar shows Scenarios from 540px');
assert.ok(app.includes('<a href="/scenarios.html" data-testid="topbar-scenarios">Scenarios</a>'), 'Scenarios link kept');

console.log('frontend_attack_r22_console: ok');
