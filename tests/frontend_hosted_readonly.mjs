import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { apiRequest } from '../frontend/src/api.js';
import { hostedCopy } from '../frontend/src/hostedCopy.js';

// Hosted read-only Sandbox (GET /connections -> {"mode":"hosted_demo","sandbox_reads":true}): the page may show Connect US
// Sandbox, the Sandbox dispute list and read-only detail. Every write control stays hidden exactly as in the hosted demo.
// FRONTEND_ROOT lets the negative control point this test at a scratch copy.
const root = process.env.FRONTEND_ROOT || resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const session = { session_id: 'session-1', csrf_token: 'csrf-1', expires_at: '2099-01-01T00:00:00Z' };
const serve = (payload) => { globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(payload) }); };

// 1. /connections shape: sandbox_reads true is accepted only with hosted_demo; everything else is still refused.
serve({ mode: 'hosted_demo', sandbox_reads: true });
assert.deepEqual(await apiRequest('/connections', { session }), { mode: 'hosted_demo', sandbox_reads: true });
for (const mode of ['local', 'hosted_demo']) { serve({ mode }); assert.deepEqual(await apiRequest('/connections', { session }), { mode }); }
for (const payload of [{ mode: 'local', sandbox_reads: true }, { mode: 'hosted_demo', sandbox_reads: false }, { mode: 'hosted_demo', sandbox_reads: 'yes' },
  { mode: 'hosted_demo', sandbox_reads: true, paypal: {} }, { sandbox_reads: true }, { mode: 'public', sandbox_reads: true }]) {
  serve(payload);
  await assert.rejects(apiRequest('/connections', { session }), (error) => error.code === 'contract_error', JSON.stringify(payload));
}

// 2. The flag comes only from the backend answer, and only together with hosted_demo.
assert.ok(app.includes("setSandboxReads(connections?.mode === 'hosted_demo' && connections.sandbox_reads === true);"), 'flag from /connections only');
assert.equal((app.match(/setSandboxReads\(/g) || []).length, 1, 'one place sets it');
assert.ok(!/writeStored\([^)]*sandboxReads/.test(app), 'never stored');

// 3. Write controls are still replaced by hosted notes whatever sandboxReads says (they test `hosted`, not the new flag).
for (const note of ['hosted-note-invoice', 'hosted-note-evidence']) {
  assert.ok(new RegExp(`\\{hosted \\? <p className="hosted-note" data-testid="${note}"`).test(app), `${note} still keyed on hosted alone`);
}
for (const guarded of ['receipt && !hosted && evidenceSubmitReady', 'receipt && !hosted && trackingSubmitReady', 'invoiceReview ? (hosted ? null :']) {
  assert.ok(app.includes(guarded), guarded);
}
assert.ok(!/sandboxReads[^;]{0,80}(evidence-submit|tracking-submit|invoice-create|provide-evidence|add-tracking)/.test(app), 'no write control reads the new flag');
assert.ok(app.includes('{hosted && !sandboxReads ? <p className="hosted-note" data-testid="hosted-note-sandbox">'), 'connect appears only with sandboxReads');
assert.ok(!app.includes("apiRequest('/paypal/invoices/draft'") || app.includes('sendConfirmTokens'), 'no new write call was added');

// 4. Polling: 60 s, only while visible, on the disputes stage and connected; any error (a 429 included) pauses with one line.
const poll = app.slice(app.indexOf('// Hosted read-only Sandbox: refresh'), app.indexOf('const loadProviderDispute'));
assert.ok(app.includes('    }, 60000);'), 'sixty seconds');
for (const part of ["sandboxReads", "activeStage !== 'disputes'", "sandbox?.status !== 'connected'",
  "document.visibilityState !== 'visible'", "apiRequest('/paypal/disputes'", '.catch(() => { window.clearInterval(timer); if (mounted.current) setNotice(HOSTED_NOTES.paused); })', 'return () => window.clearInterval(timer);']) {
  assert.ok(poll.includes(part), 'poll effect: ' + part);
}
assert.ok(!poll.includes("method: 'POST'"), 'polling only reads');
assert.ok(app.includes("paused: 'Refresh paused."), 'one paused notice');

// 5. Copy: without the flag the hosted text is unchanged; with it the pill no longer claims "no PayPal calls".
assert.equal(hostedCopy(null).pill, 'Hosted demo · no PayPal calls');
assert.equal(hostedCopy({ chooser_mode: 'keyword', model_requested: false }, false).pill, 'Hosted demo · rules only · no PayPal calls');
assert.ok(!/no PayPal calls|never calls PayPal/.test(JSON.stringify(hostedCopy({ chooser_mode: 'keyword' }, true))), 'reads copy is honest');
// 6. The list shows the dispute id as the API returns it (masked by the server in hosted read-only mode, never masked twice).
assert.ok(app.includes('<strong>{row.dispute_id}</strong>') && !/sandboxReads \? maskDisputeId/u.test(app), 'the list shows the id the API returned (the server already masks it in hosted read-only mode)');
assert.ok(app.includes("onClick={() => loadProviderDispute(row.dispute_id)}"), 'the click still sends the real id');
console.log('frontend_hosted_readonly: ok');
