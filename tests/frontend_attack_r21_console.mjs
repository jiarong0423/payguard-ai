// attack r21 (2026-11-03): main-console fixes from the desktop and phone attack reports stay pinned.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../frontend/src/${path}`, import.meta.url), 'utf8');
const app = read('App.jsx');
const panel = read('CountryRules.jsx');
const guide = read('GuideLive.jsx');
const css = read('index.css');

// Desktop #1: a country check in flight when Reset remounts the panel never writes its old result back.
assert.ok(panel.includes('const liveRef = useRef(true);') && panel.includes('const runTokenRef = useRef(0);'), 'panel tracks mount and run token');
assert.ok(panel.includes('useEffect(() => { liveRef.current = true; return () => { liveRef.current = false; runTokenRef.current += 1; }; }, []);'), 'unmount retires the token');
{
  const run = panel.slice(panel.indexOf('async function runCheck(values) {'), panel.indexOf('const select = '));
  assert.ok(run.indexOf('if (!current()) return;') > -1 && run.indexOf('if (!current()) return;') < run.indexOf('onResult?.(payload)'), 'late result dropped before onResult');
}

// Desktop #3: the top bar fits between the phone layout and 1440px.
assert.ok(css.includes('@media (min-width: 641px) and (max-width: 1440px) {\n  .topbar { gap: 16px;'), 'tight top bar up to 1440px');
assert.ok(css.includes('.topbar .environment:not(.environment-hosted) { flex-shrink: 0; gap: 12px; }'), 'Sandbox card never squeezed out');
assert.ok(css.includes('.topbar .pwa-install-button { width: 44px; padding: 0; }'), 'Install app turns into an icon');
assert.ok(/@media \(min-width: 641px\) and \(max-width: 1180px\) \{\s*\.topbar \.topbar-sandbox-full \{ display: none; \}/.test(css), 'short Sandbox label up to 1180px');

// Phone #1/#10: no :focus switch; a JS "typing" state with a release delay and a Back-closes-keyboard blur.
assert.ok(!/:has\(input[^)]*:focus/.test(css), 'no :focus based hiding of the action bar or in-page buttons');
assert.ok(css.includes('.app-shell.is-typing .phone-action-bar { display: none; }'), 'bar hides while typing');
assert.ok(css.includes('.app-shell.has-phone-action.is-typing :is([data-testid="aup-review"]'), 'in-page action shows while typing');
assert.ok(app.includes("${typing ? ' is-typing' : ''}"), 'shell carries the typing class');
assert.ok(app.includes('const TYPING_RELEASE_MS = 700;') && app.includes('}, TYPING_RELEASE_MS);'), 'typing outlives the blur');
assert.ok(app.includes('if (keyboardSeen && isTextEntry(document.activeElement)) { keyboardSeen = false; document.activeElement.blur(); }'), 'keyboard closed by Back blurs the field');

// Phone #2: the warning dialog owns a history entry; Back closes it.
assert.ok(app.includes("window.history.pushState({ ...(window.history.state || {}), pgWarningDialog: true }, '');"), 'dialog pushes a history entry');
assert.ok(app.includes("if (!popped && window.history.state?.pgWarningDialog) { dialogPopRef.current.ignore = true; window.history.back(); }"), 'closing by a button pops it again');
assert.ok(app.includes('if (dialogPopRef.current.open || dialogPopRef.current.ignore) { dialogPopRef.current.ignore = false; return; }'), 'dialog pops do not re-run hash navigation');

// Phone #3: the bar ignores a tap right after its action changed.
assert.ok(app.includes('const PHONE_ACTION_SETTLE_MS = 600;') && app.includes('if (Date.now() - phoneActionRef.current.at < PHONE_ACTION_SETTLE_MS) return;'), 'bar settle window');
assert.ok(app.includes('onClick={phoneActionClick}>{phoneAction.label}</Button>'), 'bar uses the guarded click');

// Client-side checks: description over 200 and invalid amounts never reach the server.
const amountPattern = new RegExp(app.match(/const INVOICE_AMOUNT = \/(.+)\/;/)[1]);
const invoiceOk = (value) => amountPattern.test(value) && Number(value) > 0;
for (const bad of ['-5', 'abc', '1e309', '10.001', '45.6.7', '0', '0.00', '', '12345678.00']) assert.equal(invoiceOk(bad), false, `invoice amount ${bad} rejected`);
for (const good of ['10', '10.5', '10.00', '9999999.99']) assert.equal(invoiceOk(good), true, `invoice amount ${good} accepted`);
assert.ok(app.includes('const invoiceAmountValue = (value) => Number(String(value).trim()).toFixed(2);'), 'amount sent with two decimals');
assert.equal(app.split('amount: invoiceAmountValue(invoiceAmount)').length - 1, 2, 'review and draft send the same normalized amount');
assert.ok(app.includes('if (amountProblem) { setAmountNote(amountProblem);'), 'bad amount stops Confirm Draft Context with a field message');
assert.ok(app.includes('!keepsPolicyResult(failure)) invalidateAup();'), 'an amount error keeps the policy result');
assert.ok(app.includes('data-testid="aup-description-note"') && app.includes('const runPolicyCheck = () => {'), 'over-limit description has a visible note and is not sent');
const countryPattern = new RegExp(panel.match(/const AMOUNT = \/(.+)\/;/)[1]);
const countryOk = (value) => !value || (countryPattern.test(value) && Number(value) > 0);
for (const bad of ['-1', '-5', 'abc', '1e309', '10.001', '45.6.7', '0']) assert.equal(countryOk(bad), false, `country amount ${bad} rejected`);
for (const good of ['', '120', '120.50']) assert.equal(countryOk(good), true, `country amount ${good} accepted`);
assert.ok(!panel.includes(".replace(/[^0-9.]/g, '')"), 'typed amount is not silently rewritten');
assert.ok(panel.includes("onKeyDown={(event) => { if (event.key === 'Enter') { event.preventDefault(); run(); } }}"), 'Enter in the amount runs the check');
assert.ok(panel.includes('data-testid="country-amount-note"'), 'country amount field message');

// Guide Send keeps the text until the turn is accepted.
{
  const send = guide.slice(guide.indexOf('const send = async (event) => {'), guide.indexOf('const saveRound'));
  assert.ok(!send.includes("setText('');"), 'text not cleared before the request');
  assert.ok(send.includes("if (!result) { setLog((rows) => rows.filter((row) => row.id !== sentId)); return; }"), 'failed turn removes the bubble');
  assert.ok(send.includes("setText((current) => (current.trim() === message ? '' : current));"), 'text cleared after success');
}

// Focus: receipt after approve, a visible control after Reset, Escape after a backdrop click, no keyboard on Cancel.
assert.ok(app.includes("focusWhenIdle(['[data-testid=\"dispute-result\"]'], { scroll: true });"), 'approve focuses the receipt after the action');
// attack r22: the same targets, with a jump into view only when the page's own scroll left the button off screen.
assert.ok(app.includes("inject('reset'); focusWhenIdle(['#compliance [data-testid=\"demo-reset\"]', '#stage-trigger-compliance'], { scroll: 'fallback' });"), 'reset focuses a visible control');
assert.ok(app.includes("document.addEventListener('keydown', onKey);") && app.includes("if (!busyRef.current) chooseWarningRef.current('CANCEL');"), 'Escape handled on the document');
assert.ok(app.includes('<div className="aup-warning-backdrop" onMouseDown={holdWarningFocus}>'), 'backdrop click keeps focus in the dialog');
assert.ok(app.includes("if (how === 'RETURN_TO_EDIT') { focusWhenIdle(['#description']); return; }"), 'only Return to edit focuses the description');
assert.ok(app.includes("focusWhenIdle(['[data-testid=\"aup-review\"]', '[data-testid=\"phone-action-aup\"]', '#stage-trigger-compliance']);"), 'Cancel lands on a button');

// Phones: error banner full width; offline recovery; result above the bar; stale banner cleared; download repeats.
assert.ok(css.includes('.feedback-region .message-error .button { order: 3; flex: 1 0 100%; margin-left: 0; justify-content: center; }'), 'Reconnect on its own row');
assert.ok(app.includes("autoLoadedRef.current[scenario] = ok === true ? true : 'failed';"), 'auto-load marked done only after success');
assert.ok(app.includes("window.addEventListener('online', onOnline);"), 'coming back online retries');
assert.ok(css.includes('[data-testid="aup-result"] { scroll-margin-bottom: calc(56px + 24px + env(safe-area-inset-bottom)); }'), 'policy result clears the bar');
assert.ok(app.includes("if (errorSourceRef.current === 'aup' && value.trim() && value.length <= DESCRIPTION_LIMIT)"), 'valid description clears a stale policy error');
assert.ok(app.includes("if (!firstClick('redacted')) return;") && app.includes("if (!firstClick('zip')) return;") && app.includes('const DOWNLOAD_REPEAT_MS = 1000;'), 'download repeat clicks ignored');

// 401 in the country panel and the guides uses the console's Reconnect flow.
assert.ok(app.includes('onContinue={continueToDraft} onSessionExpired={panelSessionExpired} onBusy={setCountryBusy} onExample={() => editDescription(EXAMPLE_DESCRIPTION)} autoExample={currentPage === \'compliance\'} />'), 'country panel reports 401 (attack r22: and its busy state; P3 2026-11-12: autoExample prop added)');
assert.equal(app.split('request={guideRequest} onSessionExpired={panelSessionExpired} />').length - 1, 3, 'all three guides report 401');
assert.ok(panel.includes('onSessionExpired?.(failure, session);') && guide.includes('if (failure.status === 401) onSessionExpired?.(failure, session);'), 'panels call it');
assert.ok(!guide.includes('Reload the page to start a new one'), 'no reload instruction left');

console.log('frontend_attack_r21_console: ok');
