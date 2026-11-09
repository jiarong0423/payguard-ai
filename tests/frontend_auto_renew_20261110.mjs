// Owner 2026-11-10: the 15-minute session, the 2-minute policy check and the 5-minute dispute draft renew by
// themselves instead of making the seller (or a judge) press Reconnect / Run Policy Check / Prepare again.
// This file pins the source so a later edit cannot quietly undo it; the behaviour was checked in the browser.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');

// Session: a 401 starts a new session by itself, a limited number of times, then says what was cleared.
assert.ok(app.includes('const AUTO_RENEW_LIMIT = 3;'), 'session renewals are capped');
assert.ok(app.includes("if (failure?.status === 401 && autoRenewCountRef.current < AUTO_RENEW_LIMIT) {"), 'expiry renews');
assert.ok(app.includes('window.setTimeout(() => bootstrapRef.current?.({ renewed: true }), AUTO_RENEW_DELAY_MS);'), 'renewal goes through bootstrap');
assert.ok(app.includes("if (renewed && !resumedState) setInfo({ kind: 'resumed', text: SESSION_RENEWED_TEXT });"), 'renewal is announced');
// Idle expiry: the timer takes the server's later expires_at instead of ending the session.
assert.ok(app.includes("if (Date.parse(fresh?.expires_at || '') > expires) {"), 'timer follows the moved end');

// Policy check: re-run shortly before the end, only when nothing depends on this exact result.
{
  const guard = app.slice(app.indexOf('aupAutoRef.current = {'), app.indexOf('const getDraft = () =>'));
  for (const condition of ['!busyRef.current', '!aupConsumed', '!productConfirm', '!draftConfirmRef.current',
    'aupCheckedTextRef.current === description', "!coolingNow('aup')", "document.visibilityState === 'visible'",
    'aupAutoRenewsRef.current < AUP_AUTO_RENEW_LIMIT']) assert.ok(guard.includes(condition), `policy renewal guard: ${condition}`);
}
assert.ok(app.includes('const AUP_AUTO_RENEW_LIMIT = 5;'), 'policy renewals are capped');
assert.ok(app.includes('fallback = setTimeout(expire, Math.max(0, Date.parse(aup.expires_at) - Date.now()));'), 'otherwise it expires as before');
assert.ok(app.includes('if (!quiet) window.requestAnimationFrame('), 'an automatic run does not scroll the page');
assert.ok(/const runPolicyCheck = \(\) => \{\s*if \(busyRef\.current\) return;\s*aupAutoRenewsRef\.current = 0;/u.test(app), 'a press of the seller resets the count');

// Dispute draft: renewed only before its review; a recorded review is never renewed.
{
  const guard = app.slice(app.indexOf('draftAutoRef.current = {'), app.indexOf('aupAutoRef.current = {'));
  for (const condition of ['!receipt', '!reviewedOnServer', 'draft.case_ref === caseRef', 'caseItem?.case_ref === caseRef',
    'draftAutoRenewsRef.current < DRAFT_AUTO_RENEW_LIMIT']) assert.ok(guard.includes(condition), `draft renewal guard: ${condition}`);
}
assert.ok(app.includes('if (!draft || receipt) return undefined;'), 'no timer once reviewed');
assert.ok(app.includes('const DRAFT_AUTO_RENEW_AFTER_MS = DRAFT_WINDOW_MS + 1000;'), 'renewal runs after the server window');
assert.ok(app.includes('if (!quiet) setReviewChecked(false);'), 'an automatic draft keeps the tick');
assert.ok(app.includes("if (quiet) { setInfo({ kind: 'resumed', text: DRAFT_RENEWED_TEXT }); return; }"), 'draft renewal is announced');

console.log('frontend_auto_renew_20261110: ok');

// 2026-11-10 recording fixes: a live preview with "note": null passes the contract check, and a review the server
// recorded before a reload unlocks the sends like this page's own receipt (the server still checks the approval).
{
  const api = readFileSync(new URL('../frontend/src/api.js', import.meta.url), 'utf8');
  assert.ok(api.includes("...optional('paypal_debug_id', 'note')"), 'note is an optional envelope key');
  assert.ok(api.includes("const noteValid = !has('note') || payload.note === null || (typeof payload.note === 'string' && payload.note.length <= 300);"), 'note shape');
  assert.ok(api.includes('&& debugIdValid && noteValid;'), 'note checked');
  assert.ok(app.includes("const reviewRecorded = Boolean(receipt) || (caseItem?.status === 'local_draft_reviewed' && draft?.case_ref === caseItem?.case_ref);"), 'restored review counts');
  assert.ok(app.includes('const evidenceSubmitReady = reviewRecorded && evidencePreview'), 'evidence send uses it');
  assert.ok(app.includes('const trackingSubmitReady = reviewRecorded && trackingPreview'), 'tracking send uses it');
  assert.ok(!app.includes('const evidenceSubmitReady = Boolean(receipt)'), 'old receipt-only gate gone');
}
console.log('frontend_auto_renew_20261110 (recording fixes): ok');
