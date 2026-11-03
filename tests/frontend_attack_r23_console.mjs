// attack r23 (2026-11-04): main-console fixes from the desktop and phone attack reports stay pinned.
// The behaviour was checked in headless Chrome against a throwaway server of the worktree (429/503 with Retry-After
// simulated by request interception, a 40 s session TTL for the expiry notice); this file pins the source and runs the
// pure helpers, so a later edit cannot quietly undo it.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { ApiError, apiRequest, parseRetryAfter, retrySecondsLeft, waitText, withoutFixedWait } from '../frontend/src/api.js';

const read = (path) => readFileSync(new URL(`../frontend/${path}`, import.meta.url), 'utf8');
const app = read('src/App.jsx');
const panel = read('src/CountryRules.jsx');
const guide = read('src/GuideLive.jsx');
const css = read('src/index.css');

// P1 #1: Retry-After is read into the error.
assert.equal(parseRetryAfter('37'), 37);
assert.equal(parseRetryAfter(new Date(Date.now() + 20000).toUTCString()), 20);
for (const bad of [null, '', '0', '-3', 'soon', '601']) assert.equal(parseRetryAfter(bad), null, `ignored: ${bad}`);
{
  const failure = new ApiError('x', 429, 'rate_limited', 10);
  assert.ok(failure.retryAt > Date.now() && retrySecondsLeft(failure) === 10, 'retryAt and seconds left');
  assert.equal(retrySecondsLeft(new ApiError('x', 500, 'request_failed')), 0, 'no wait without Retry-After');
}
assert.equal(waitText(1), 'Try again in 1 second.');
assert.equal(waitText(37), 'Try again in 37 seconds.');
for (const [message, expected] of [
  ['Too many requests from this address; slow down and try again.', 'Too many requests from this address; slow down.'],
  ['The demo is busy right now; try again in a few seconds.', 'The demo is busy right now.'],
  ['Five policy checks are already open in the last two minutes. Try again in 37 seconds.', 'Five policy checks are already open in the last two minutes.'],
  ['Too many new sessions; try again in 12 seconds.', 'Too many new sessions.'],
  ['The local request or sample limit was reached.', 'The local request or sample limit was reached.'],
]) assert.equal(withoutFixedWait(message), expected, 'the fixed wait gives way to the countdown');
{
  const realFetch = globalThis.fetch;
  for (const [status, header, body, code] of [[429, '9', JSON.stringify({ error: { code: 'aup_capacity', message: 'm' } }), 'aup_capacity'],
    [503, '5', '<html>busy</html>', 'server_busy'], [500, '5', JSON.stringify({ error: { code: 'x', message: 'm' } }), 'x']]) {
    globalThis.fetch = async () => new Response(body, { status, headers: { 'Retry-After': header, 'Content-Type': 'application/json' } });
    const failure = await apiRequest('/demo/state', { session: { session_id: 's', csrf_token: 'c' } }).catch((error) => error);
    assert.equal(failure.code, code);
    assert.equal(failure.retryAfter, status === 500 ? null : Number(header), `${status}: Retry-After only on 429/503`);
  }
  globalThis.fetch = realFetch;
}
// Every action: one hold per action key, set from the failure; the guard refuses while it runs.
assert.ok(app.includes("if (busyRef.current || !sessionRef.current || coolingNow(key)) return false;"), 'actions held during the wait');
assert.ok(app.includes('holdAfter(key, failure);'), 'the failing action is held');
assert.ok(app.includes("const blocked = blockedProp || waiting;"), 'Button waiting = blocked look and aria-disabled');
for (const key of ['aup', 'burst', 'dispute', 'draft', 'approve', 'reset', 'invoice-review', 'invoice', 'connect']) assert.ok(app.includes(`waiting={waitLeft('${key}') > 0}`), `${key} button held`);
assert.ok(app.includes("if (coolingNow('aup')) return;"), 'Run Policy Check refuses during the wait');
assert.ok(app.includes('<WaitLine until={error.retryAt} now={now} testId="retry-wait" />'), 'banner counts down');
assert.ok(guide.includes("export function useWaitClock(until) {") && guide.includes("'You can try again now.'"), 'shared countdown');
assert.ok(panel.includes('if (busy || Date.now() < waitUntil) return;') && panel.includes('aria-disabled={busy || waiting || undefined}'), 'country check held');
assert.ok(panel.includes('<WaitLine until={waitUntil} now={now} testId="country-wait" />'), 'country check counts down');
assert.ok(guide.includes('if (!session || busy || Date.now() < waitUntil) return null;') && guide.includes('aria-disabled={busy || waiting || undefined} aria-busy={busy}>Send'), 'guide send held');
// Boot and Reconnect: one request at a time, held during the wait, one automatic retry after a 503.
assert.ok(app.includes("const reconnect = () => { if (bootingRef.current || coolingNow('boot')) return; bootstrap(); };"), 'Reconnect guarded');
assert.ok(app.includes("if (failure.status === 503 && retrySecondsLeft(failure) && !auto) {"), 'one automatic retry after a 503');
assert.ok(app.includes("bootstrapRef.current?.({ auto: true });"), 'the retry is marked automatic');
// Step 02/03 automatic load refused with Retry-After loads again when the step is opened after the wait.
assert.ok(app.includes("if (scenario && autoLoadedRef.current[scenario] === 'failed' && cooldownRef.current[scenario] && !coolingNow(scenario)) autoLoadedRef.current[scenario] = false;"), 'reopen retries');
assert.ok(app.includes('aria-label="Dismiss error message"'), 'the banner can be dismissed');

// P1 #2: the session survives Dashboard, reload and Back; per-tab sessionStorage, try/catch, 401 starts anew.
assert.ok(app.includes("const tabStorage = () => { try { return window.sessionStorage; } catch { return null; } };"), 'guarded storage');
assert.ok(app.includes('sessionStorage is per tab'), 'tab isolation documented');
assert.ok(app.includes("resumedState = await apiRequest('/demo/state', { session: stored, signal });"), 'resume with GET /demo/state');
assert.ok(app.includes('if (failure.status !== 401) throw failure;') && app.includes("if (!session) session = await apiRequest('/demo/sessions'"), 'a 401 starts a new session');
assert.ok(app.includes("['draft_ready', 'local_draft_reviewed'].includes(row.status)"), 'only drafts the server holds are read again');
assert.ok(app.includes("const reviewedOnServer = !receipt && caseItem?.status === 'local_draft_reviewed';"), 'a server-recorded review is shown, no receipt invented');
assert.ok(!/writeStored\([^)]*aup/.test(app), 'no check result is stored');

// P2 #3: the notice appears when expires_at passes, after asking the server.
{
  const timer = app.slice(app.indexOf('The session has a fixed expires_at'), app.indexOf('const generateAiBrief'));
  assert.ok(timer.includes("const end = () => expireSession(new ApiError(SESSION_EXPIRED_TEXT, 401, 'session_expired')"), 'expiry uses the Reconnect banner');
  assert.ok(timer.includes("await apiRequest('/demo/state', { session });") && timer.includes('if (failure.status === 401) end();'), 'server confirms');
  assert.ok(timer.includes("document.addEventListener('visibilitychange', onVisible);"), 'a sleeping tab checks on return');
}
assert.ok(app.includes("const SESSION_EXPIRED_TEXT = 'Session expired — select Reconnect"), 'plain expiry text');

// P2 #4: Enter on Confirm Draft Context moves focus to the next control.
assert.ok(app.includes("focusWhenIdle(AFTER_DRAFT_CONTEXT, { scroll: 'fallback' });"), 'focus after Confirm Draft Context');
assert.ok(app.includes("if (how === 'ACKNOWLEDGE_AND_CONTINUE') return;"), 'the dialog close does not steal it back');

// P2 #5: "Already checked" is neutral info and stays until the description changes.
assert.ok(app.includes("setInfo({ kind: 'already', text: 'Already checked. Edit the description to check it again.' });"), 'neutral info');
assert.ok(app.includes("setInfo((current) => (current?.kind === 'already' ? null : current));"), 'cleared with the result it points at');
assert.ok(app.includes('<div className="message message-info" data-testid="console-info" data-kind={info.kind}>'), 'info style');
assert.ok(css.includes('.wait-line { font-variant-numeric: tabular-nums; }'), 'steady countdown width');

console.log('frontend_attack_r23_console: ok');
