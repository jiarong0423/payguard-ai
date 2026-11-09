import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { apiRequest } from '../frontend/src/api.js';
import { hostedCopy } from '../frontend/src/hostedCopy.js';

// Hosted demo (PAYGUARD_DEMO_MODE=public, GET /api/v1/connections -> {"mode":"hosted_demo"}): no control that the
// backend answers 503 hosted_demo_disabled is rendered; each is replaced by one line with a hosted-note-* test id.
// Local mode keeps every control and test id unchanged.
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const css = readFileSync(resolve(root, 'frontend/src/index.css'), 'utf8');
const workOrders = readFileSync(resolve(root, 'frontend/src/scenarios/workOrders.js'), 'utf8');
const scenarios = readFileSync(resolve(root, 'frontend/src/scenarios/main.jsx'), 'utf8');

// 1. The hosted flag comes only from the backend mode, read once per session, and never from storage.
assert.ok(app.includes("apiRequest('/connections', { session, signal }).catch(() => null)"), 'mode is read with the session; a failed read keeps local');
assert.ok(app.includes("setHosted(connections ? connections.mode === 'hosted_demo' : !['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname));"), 'hosted on mode hosted_demo, and off this machine when the mode cannot be read');
assert.equal((app.match(/setHosted\(/g) || []).length, 1, 'one place sets the hosted flag');
// attack r23: the console keeps only this tab's session id, CSRF token and the seller's inputs in sessionStorage
// (resume after Back or reload); never localStorage, and never the hosted flag.
assert.ok(!/localStorage/.test(app), 'no localStorage in the console');
assert.equal((app.match(/window\.sessionStorage/g) || []).length, 1, 'one sessionStorage accessor');
assert.ok(!/writeStored\([^)]*hosted/.test(app) && !/storeSession\([^)]*mode/.test(app), 'the hosted flag is never stored');

// 2. The response contract is closed: the mode and nothing else (no key presence, no variable names).
const session = { session_id: 'session-1', csrf_token: 'csrf-1', expires_at: '2099-01-01T00:00:00Z' };
const serve = (payload) => { globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(payload) }); };
for (const mode of ['local', 'hosted_demo']) {
  serve({ mode });
  assert.deepEqual(await apiRequest('/connections', { session }), { mode });
}
for (const payload of [{ mode: 'public' }, { mode: 'hosted_demo', paypal: { configured: true } }, { mode: 'local', missing: ['PAYPAL_CLIENT_ID'] }, {}]) {
  serve(payload);
  await assert.rejects(apiRequest('/connections', { session }), (error) => error.code === 'contract_error', JSON.stringify(payload));
}

// 3. Top bar: the hosted pill replaces LOCAL DEMO; the Why? popover is fixed text and calls no API.
assert.ok(app.includes("{hosted ? <HostedBadge guideChooser={guideChooser} sandboxReads={sandboxReads} /> : <Badge tone=\"blue\" dot>LOCAL DEMO</Badge>}"), 'LOCAL DEMO stays the local badge');
const badge = app.slice(app.indexOf('function HostedBadge({ guideChooser = null, sandboxReads = false })'), app.indexOf('export default function App()'));
assert.ok(badge.length > 0, 'HostedBadge component present');
assert.ok(!/apiRequest|fetch\(|connectSandbox|generateAiBrief/.test(badge), 'the popover calls no API');
assert.ok(badge.includes('data-testid="connections-hosted"') && badge.includes('aria-expanded={open}'), 'pill is the popover toggle');
// (r34 #1) The pill and the Gemini lines come from hostedCopy(guideChooser), the guide API's chooser status.
assert.ok(badge.includes('const copy = hostedCopy(guideChooser, sandboxReads);') && badge.includes('<span className="hosted-label-full">{copy.pill}</span>'), 'pill text from the chooser status');
assert.equal(hostedCopy({ chooser_mode: 'keyword', model_requested: false }).pill, 'Hosted demo · rules only · no PayPal calls', 'pill text, rules only');
assert.ok(badge.includes('<span className="hosted-label-short">Hosted demo</span>'), 'narrow-screen pill text');
assert.ok(badge.includes('data-testid="connections-why"') && badge.includes('>Why?<'), 'Why? popover');
for (const text of [
  'Why is this a hosted demo?',
  'Works here', 'Policy pre-check, sales spike and dispute evidence (rules + your review)', 'Review file and review ZIP downloads',
  'Local only', 'PayPal Sandbox connect, invoice draft, evidence request', 'demo video', 'README › Run locally',
  '{copy.intro}', '{copy.guides}', '{copy.local}', '<dd data-testid="connections-why-gemini">{copy.gemini}</dd>',
]) assert.ok(badge.includes(text), `popover text: ${text}`);
const off = hostedCopy({ chooser_mode: 'keyword', model_requested: false });
assert.equal(off.intro, "This public copy runs the same code with no keys. It never calls PayPal or Gemini, so no account or API credit is used.");
assert.equal(off.guides, 'Guides in rules-only mode and recorded replays');
assert.equal(off.local, 'Gemini evidence brief and Gemini guide');
assert.equal(off.gemini, 'Off in hosted demo');
assert.equal((badge.match(/<button|<Button|<input/g) || []).length, 1, 'no switch or button inside the popover: the pill is the only control');
assert.ok(badge.includes("event.key === 'Escape'") && badge.includes('buttonRef.current?.focus()'), 'Esc closes and returns focus');
assert.ok(badge.includes("'pointerdown'"), 'outside click closes');
assert.ok(/@media \(max-width: 400px\) \{\s*\.topbar \.environment\.environment-hosted \{ display: flex; \}/.test(css), 'pill visible on narrow phones');

// 4. Each 503 control: local branch keeps the button and its test id; the hosted branch renders one line instead.
const NOTES = {
  sandbox: 'Sandbox connect is off in the hosted demo. Run locally to connect your own Sandbox app.',
  invoice: 'Sandbox drafts are created only in a local run.',
  ai: 'AI brief is off in the hosted demo (no model calls). The sample summary below shows the format.',
  disputes: 'Sample cases (not real). The hosted demo does not read a Sandbox account.',
  evidence: 'Evidence requests are built and sent only in a local run.',
};
for (const [key, text] of Object.entries(NOTES)) assert.ok(app.includes(`  ${key}: '${text.replace(/'/g, "\\'")}',`), `hosted note ${key}`);
const swaps = [
  ['{hosted && !sandboxReads ? <p className="hosted-note" data-testid="hosted-note-sandbox">{HOSTED_NOTES.sandbox}</p> : <Button data-testid="sandbox-connect"', 'Connect US Sandbox'],
  ['{hosted ? <p className="hosted-note" data-testid="hosted-note-invoice">{HOSTED_NOTES.invoice}</p> : <Button data-testid="invoice-create"', 'Create Sandbox draft'],
  ['{hosted ? null : <Button data-testid={`ai-generate-${stage}`}', 'Generate AI brief'],
  ['{hosted ? <p className="hosted-note" data-testid="hosted-note-evidence">{HOSTED_NOTES.evidence}</p> : <><Button data-testid="evidence-preview"', 'Prepare evidence request (preview)'],
];
// The top-bar Sandbox card (owner 2026-11-03) is one other place, and it renders only when not hosted. The phone bar
// after Confirm Draft Context (attack r22) is the other: it offers Connect or Create Sandbox draft only when not hosted.
// (r32 J4 P1-2) The phone bar's Dispute step offers the preview after the local review, only when not hosted.
// (read-only Sandbox) The disputes list adds one more Connect, shown only when sandboxReads is on.
const extraPlaces = { 'Connect US Sandbox': 3, 'Create Sandbox draft': 1, 'Prepare evidence request (preview)': 1 };
assert.ok(app.includes("receipt && !hosted && providerDisputeDetail && !evidencePreview\n            ? { key: 'evidence-preview', label: 'Prepare evidence request (preview)'"), 'phone bar preview is local only');
assert.ok(app.includes("? (reviewRecorded && !hosted && evidenceSubmitReady\n") && app.includes(": reviewRecorded && !hosted && trackingSubmitReady\n"), 'phone bar sends are local only');
assert.ok(app.includes('{!hosted && <TopbarSandbox '), 'top-bar Sandbox card is local only');
assert.ok(app.includes(": invoiceReview ? (hosted ? null : sandbox?.status === 'connected'"), 'phone bar draft actions are local only');
for (const [swap, label] of swaps) {
  assert.ok(app.includes(swap), `hosted swap for ${label}`);
  assert.equal(app.split(label).length - 1, 1 + (extraPlaces[label] || 0), `${label} is rendered only from its known places`);
}
assert.ok(app.includes('{hosted && <p className="hosted-note" data-testid={`hosted-note-ai-${stage}`}>{HOSTED_NOTES.ai}</p>}'), 'AI note per stage');
assert.equal((app.match(/onGenerateAi=\{generateAiBrief\} hosted=\{hosted\}/g) || []).length, 3, 'all three AI brief panels know the mode');
assert.ok(app.includes('data-testid="evidence-submit"') && app.indexOf('data-testid="evidence-submit"') < app.indexOf('</>}', app.indexOf('hosted-note-evidence')), 'Submit sits inside the local branch');
assert.ok(app.includes('<details className="technical-details" data-testid="evidence-technical-details">'), 'technical details stay in both modes');
// Step 03 text no longer points a hosted visitor at Connect.
assert.ok(app.includes(": hosted && !sandboxReads ? <span data-testid=\"hosted-note-disputes\">{HOSTED_NOTES.disputes}</span> : 'Sample cases. Connect the Sandbox in Step 01 to see real Sandbox cases.'}"), 'step 03 hosted text');
// Sandbox status badge and footer.
assert.ok(app.includes("{hosted && !sandboxReads ? 'Local run only' : sandbox?.status === 'not_configured' ? 'Awaiting connection'"), 'sandbox badge');
assert.ok(app.includes("{hosted ? <span data-testid=\"hosted-note-footer\">Hosted demo</span> : 'Local prototype'}"), 'footer');
// Second line of defense: a 503 hosted_demo_disabled becomes a neutral notice, not the red error box.
assert.ok(app.includes("if (failure.code === 'hosted_demo_disabled') { setNotice(HOSTED_DISABLED_NOTICE); return; }"), 'actions: neutral notice');
assert.ok(app.includes("if (failure.code === 'hosted_demo_disabled') { setAiNotices({ [stage]: HOSTED_NOTES.ai }); return; }"), 'AI brief: neutral notice');

// 5. Local test ids are all still present.
for (const id of ['sandbox-connect', 'sandbox-status', 'invoice-review', 'invoice-create', 'invoice-confirm', 'evidence-preview', 'evidence-submit',
  'provider-disputes', 'dispute-data-source', 'footer-independent']) assert.ok(app.includes(`data-testid="${id}"`), `local test id ${id}`);
assert.ok(app.includes('data-testid={`ai-generate-${stage}`}'), 'local AI test id');

// 6. The Scenarios page agrees: hosted from the same server mode (agent-status reason), manual steps Local only.
assert.ok(workOrders.includes("status.payload.reason === 'hosted_demo'"), 'scenarios read hosted from the server');
assert.ok(workOrders.includes('const ownerStatus = deps.hosted ? STATUS.LOCAL_ONLY : STATUS.NEEDS_OWNER;'), 'owner steps Local only when hosted');
assert.ok(scenarios.includes("[STATUS.LOCAL_ONLY]: { label: 'Local only'"), 'Local only label');

console.log('frontend hosted contract: ok');
