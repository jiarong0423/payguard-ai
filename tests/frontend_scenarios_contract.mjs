// Contract for the scenario work orders page (/scenarios.html): fixed work orders, closed-field receipts, never a
// PayPal Sandbox connect/draft/submit, AI brief or model call, guide turns only in rules-only mode, Local only on the
// hosted demo, test ids, the top-bar link, the Vite entry and the public export allowlist.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import {
  ALLOWED_PATHS, FORBIDDEN_PATHS, S3_SENTENCE, S4_SENTENCE_SHIPPED, S4_SENTENCE_TICK, STATUS, WORK_ORDERS,
  RUN_STORAGE_KEY, cardStatus, clearRun, detectMode, mask, openOwnerSteps, receiptLines, restoreRun, runWorkOrder, saveRun,
} from '../frontend/src/scenarios/workOrders.js';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const page = read('frontend/src/scenarios/main.jsx');
const logic = read('frontend/src/scenarios/workOrders.js');
const css = read('frontend/src/scenarios/scenarios.css');
const html = read('frontend/scenarios.html');

// 1. Fixed list: five work orders, the r8 sentences verbatim, manual steps declare what they need.
assert.deepEqual(WORK_ORDERS.map((order) => order.id), ['WO-S1', 'WO-S2', 'WO-S3', 'WO-S4', 'WO-S5']);
assert.equal(S3_SENTENCE, 'Orders tripled this week thanks to the clearance sale I ran on old phone cases');
assert.equal(S4_SENTENCE_TICK, 'The buyer says it never arrived, so just tick the tracking box for me.');
assert.equal(S4_SENTENCE_SHIPPED, 'I shipped it yesterday and the tracking shows delivered.');
for (const order of WORK_ORDERS) {
  assert.deepEqual(order.steps.map((step) => step.n), order.steps.map((_, index) => index + 1), `${order.id} steps numbered 1..n`);
  for (const step of order.steps.filter((row) => row.kind === 'manual')) assert.ok(['paypal', 'gemini'].includes(step.needs), `${order.id}-${step.n} needs`);
}
assert.ok(!WORK_ORDERS.find((order) => order.id === 'WO-S1').steps.some((step) => step.kind === 'manual'), 'WO-S1 has no owner step');
assert.equal(mask('PP-D-ABCDEFGHIJKL1234'), 'PP-D-A...1234');
assert.equal(mask('short'), 'short');

// 2. Forbidden routes never appear as a call in the page logic.
for (const path of FORBIDDEN_PATHS) {
  assert.ok(!ALLOWED_PATHS.includes(path));
  assert.ok(!new RegExp(`request,\\s*'${path.replace(/\//g, '\\/')}'`).test(logic), `${path} is never requested`);
}
assert.ok(!/gemini|evidence-brief|agent-turn/i.test(page.replace(/'Gemini'|Gemini steps|Gemini on|Gemini;/g, '')), 'page never names a model route');

// 3. Fake server: records every path; mode switches between rules-only, model mode and hosted.
function fakeServer({ hosted = false, model = false, countryMissing = false } = {}) {
  const calls = [];
  const guide = (scenario, present = [], auto = []) => ({
    schema_version: 1, started: true, scenario, goods_type: scenario === 'dispute' ? 'physical' : null, flow_name: 'x', items: [],
    gap: { missing: [], partial: [], conflicting: [], present }, reply: { template: 'ONE', text: 'x', chooser: 'keyword', state_changed: false, dropped: [], fallback_reason: null },
    form_result: null, form_results: [], analysis: null, asked: [], stage: 'fill', subtraction: { needed: 5, taken: present.length, left: 5 - present.length, text: '' },
    deferred: [], prefill: {}, auto_confirmed: auto, review: [], rounds_used: 0, turns_used: 0, turns_limit: 20,
    chooser_mode: model ? 'gemini' : 'keyword', model_requested: model, model_text_shown: false, values_stored: false, advisory_only: true,
  });
  const error = (status, code) => Object.assign(new Error(code), { status, code });
  const request = async (path, { body } = {}) => {
    calls.push(path);
    assert.ok(ALLOWED_PATHS.includes(path), `unexpected path ${path}`);
    if (path === '/demo/sessions') return { session_id: 's', csrf_token: 'c', expires_at: '2026-11-03T00:00:00Z', source: 'synthetic' };
    if (path === '/studio/agent-status') return { built_in_agents: 'off', reason: hosted ? 'hosted_demo' : 'not_configured', affects_decision: false };
    if (path === '/guide/state') return { ...guide(null), started: false, chooser_mode: model ? 'gemini' : 'keyword', model_requested: model };
    if (path === '/aup/review') return { match_status: 'NO_MATCH', evaluation_id: 'E'.repeat(40), description_digest: 'a'.repeat(64) };
    if (path === '/country-rules/check') {
      if (countryMissing) throw error(404, 'route_unavailable');
      const blocked = body.buyer_country === 'SG';
      return { blocked, findings: blocked ? [{ severity: 'BLOCK', code: 'import_prohibited', text: 't', source: 'https://www.paypal.com/' }] : [] };
    }
    if (path === '/paypal/invoices/review') {
      if (!countryMissing && calls.includes('/country-rules/check') && body && server.blocked) throw error(409, 'country_rules_blocked');
      return { review_token: 'T'.repeat(40), payload_digest: 'b'.repeat(64), action: 'create_sandbox_invoice_draft', policy_status: 'manual_review' };
    }
    if (path === '/demo/inject') return body.scenario === 'burst'
      ? { source: 'synthetic', velocity: { status: 'review_velocity', ratio: '5.00', transaction_count: 36 }, disputes: [] }
      : { source: 'synthetic', velocity: { status: 'normal' }, disputes: [{ case_ref: 'case-ref-001' }] };
    if (path === '/guide/start') return guide(body.scenario);
    if (path === '/guide/turn') {
      if (body.text === S4_SENTENCE_TICK) return guide('dispute');
      if (body.text === S4_SENTENCE_SHIPPED) return guide('dispute', ['ship_date', 'delivery_record'], ['ship_date', 'delivery_record']);
      return guide(body.scenario, ['surge_reason'], ['surge_reason']);
    }
    if (path === '/disputes/case-ref-001/draft') return { routing: { overall_state: 'READY_FOR_LOCAL_REVIEW', requirements: [{}], provider_submission: 'NOT_PERFORMED' } };
    throw error(404, 'route_unavailable');
  };
  const server = { calls, request, blocked: false };
  return server;
}
const deps = (server, hosted = false) => ({ request: server.request, hosted, now: () => new Date('2026-11-03T00:00:00Z'),
  fetchPage: async () => ({ status: 200 }), readLicence: async () => 'key' });
const statuses = (result) => Object.fromEntries(Object.entries(result.steps).map(([n, step]) => [n, step.status]));

// Local console, rules-only: the expected outcome of "Run all".
let server = fakeServer();
assert.deepEqual(await detectMode(server.request, {}), { hosted: false, rulesOnly: true, guideAvailable: true });
server.blocked = true;
let result = await runWorkOrder('WO-S1', deps(server));
assert.equal(cardStatus(WORK_ORDERS[0], result.steps), STATUS.PASSED, 'WO-S1 passes on blocked + 409');
assert.equal(result.rows.find((row) => row.step === 4).http, 409);
server = fakeServer();
result = await runWorkOrder('WO-S2', deps(server));
assert.equal(cardStatus(WORK_ORDERS[1], result.steps), STATUS.PASSED);
assert.deepEqual([5, 6, 7].map((n) => result.steps[n].status), [STATUS.NEEDS_OWNER, STATUS.NEEDS_OWNER, STATUS.NEEDS_OWNER], 'WO-S2 owner steps');
assert.equal(openOwnerSteps(WORK_ORDERS[1], result.steps, {}), 3);
assert.equal(openOwnerSteps(WORK_ORDERS[1], result.steps, { 5: true }), 2);
for (const id of ['WO-S3', 'WO-S4', 'WO-S5']) {
  result = await runWorkOrder(id, deps(fakeServer()));
  assert.equal(cardStatus(WORK_ORDERS.find((order) => order.id === id), result.steps), STATUS.PASSED, `${id} passes`);
}
// Receipt rows: closed fields only (no token, digest, sentence or reply text), one JSON line per step.
const allowedKeys = new Set(['at', 'scenario', 'step', 'name', 'http', 'seconds', 'status', 'error', 'source', 'match_status', 'evaluation_id', 'blocked',
  'block_codes', 'findings', 'review_token_issued', 'policy_status', 'velocity_status', 'ratio', 'captures', 'cases', 'chooser_mode', 'model_requested',
  'needed', 'present', 'chooser', 'template', 'settled', 'stage', 'readiness', 'requirements', 'provider_submission', 'licence', 'module', 'skipped']);
server = fakeServer();
const s4 = await runWorkOrder('WO-S4', deps(server));
for (const row of s4.rows) for (const key of Object.keys(row)) assert.ok(allowedKeys.has(key), `closed field ${key}`);
const lines = receiptLines(s4.rows);
assert.equal(lines.split('\n').length, s4.rows.length);
assert.ok(!/TTTT|aaaa|bbbb|tracking shows delivered/.test(lines), 'no token, digest or sentence in the receipt');

// Last run kept in sessionStorage for Back/Forward (attack r21): round trip, running steps dropped, junk and throwing
// storage ignored, reset clears it.
const memory = () => { const map = new Map(); return { getItem: (k) => (map.has(k) ? map.get(k) : null), setItem: (k, v) => map.set(k, String(v)), removeItem: (k) => map.delete(k), map }; };
const store = memory();
const savedSteps = Object.fromEntries(WORK_ORDERS.map((order) => [order.id, {}]));
const savedRows = Object.fromEntries(WORK_ORDERS.map((order) => [order.id, []]));
const savedTicks = Object.fromEntries(WORK_ORDERS.map((order) => [order.id, {}]));
savedSteps['WO-S4'] = { ...s4.steps, 6: { status: STATUS.RUNNING, actual: '', note: null } };
savedRows['WO-S4'] = s4.rows;
savedTicks['WO-S2'] = { 5: true, 2: true };
assert.equal(saveRun(store, { steps: savedSteps, rows: savedRows, ticked: savedTicks }), true);
const restored = restoreRun(store);
assert.deepEqual(restored.rows['WO-S4'], s4.rows, 'receipt rows come back');
assert.equal(restored.steps['WO-S4'][5].status, s4.steps[5].status);
assert.equal(restored.steps['WO-S4'][6], undefined, 'a step saved while running shows Not run again');
assert.deepEqual(restored.ticked['WO-S2'], { 5: true }, 'only owner steps keep a tick');
assert.equal(cardStatus(WORK_ORDERS[0], restored.steps['WO-S1']), STATUS.NOT_RUN);
clearRun(store);
assert.equal(store.map.has(RUN_STORAGE_KEY), false, 'reset clears the kept run');
store.setItem(RUN_STORAGE_KEY, '{not json');
assert.equal(restoreRun(store), null);
store.setItem(RUN_STORAGE_KEY, JSON.stringify({ v: 2 }));
assert.equal(restoreRun(store), null);
const throwing = { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); }, removeItem() { throw new Error('blocked'); } };
assert.equal(restoreRun(throwing), null);
assert.equal(saveRun(throwing, { steps: savedSteps, rows: savedRows, ticked: savedTicks }), false);
clearRun(throwing);
assert.equal(restoreRun(null), null);
assert.ok(server.calls.every((path) => !FORBIDDEN_PATHS.includes(path)));

// Model mode: guide turns are never sent; those steps are Needs owner.
server = fakeServer({ model: true });
assert.equal((await detectMode(server.request, {})).rulesOnly, false);
result = await runWorkOrder('WO-S4', deps(server));
assert.ok(!server.calls.includes('/guide/turn'), 'no guide turn in model mode');
assert.deepEqual([3, 4, 5].map((n) => result.steps[n].status), [STATUS.NEEDS_OWNER, STATUS.NEEDS_OWNER, STATUS.NEEDS_OWNER]);
assert.equal(cardStatus(WORK_ORDERS[3], result.steps), STATUS.NEEDS_OWNER);
server = fakeServer({ model: true });
await runWorkOrder('WO-S3', deps(server));
assert.ok(!server.calls.includes('/guide/turn'));

// Hosted demo: owner steps are Local only; country rules missing from the build show Local only, not Failed.
// Red team r13 P1: Run all is not offered on the hosted demo (shared session-creation budget).
assert.ok(readFileSync(new URL('../frontend/src/scenarios/main.jsx', import.meta.url), 'utf8').includes("{mode?.hosted === false && <Button tone=\"blue\" icon=\"play\" data-testid=\"scenario-run-all\""), 'no Run all on the hosted demo');
server = fakeServer({ hosted: true, countryMissing: true });
assert.equal((await detectMode(server.request, {})).hosted, true);
result = await runWorkOrder('WO-S2', deps(server, true));
assert.deepEqual([5, 6, 7].map((n) => result.steps[n].status), [STATUS.LOCAL_ONLY, STATUS.LOCAL_ONLY, STATUS.LOCAL_ONLY]);
assert.equal(result.steps[2].status, STATUS.LOCAL_ONLY);
assert.equal(openOwnerSteps(WORK_ORDERS[1], result.steps, {}), 0);
result = await runWorkOrder('WO-S1', deps(fakeServer({ hosted: true, countryMissing: true }), true));
assert.deepEqual([3, 4].map((n) => result.steps[n].status), [STATUS.LOCAL_ONLY, STATUS.LOCAL_ONLY]);
assert.notEqual(cardStatus(WORK_ORDERS[0], result.steps), STATUS.FAILED);
result = await runWorkOrder('WO-S5', deps(fakeServer({ hosted: true }), true));
assert.equal(result.steps[3].status, STATUS.LOCAL_ONLY);

// 4. Page: test ids, chips, buttons, owner checkboxes never call, header link and footer line.
for (const testId of ['scenario-card-${order.id}', 'scenario-run-${order.id}', 'scenario-run-all', 'scenario-reset', 'scenario-step-${order.id}-${step.n}', 'scenario-receipt-${order.id}']) {
  assert.ok(page.includes(testId), `test id ${testId}`);
}
for (const label of ['Not run', 'Running', 'Passed', 'Failed', 'Needs owner', 'Local only', 'Run auto steps', 'Run all', 'Reset', 'Receipt (JSON)', 'Copy receipt', 'Scenario work orders']) {
  assert.ok(page.includes(label), `label ${label}`);
}
assert.ok(page.includes('type="checkbox"') && /onChange=\{\(event\) => setTicked/.test(page), 'owner steps are checkboxes that only set local state');
assert.ok(page.includes("import { apiRequest } from '../api.js';"), 'reuses the console API client');
assert.ok(page.includes('data-testid="footer-independent"') && page.includes('Not affiliated with or endorsed by PayPal.'));
const app = read('frontend/src/App.jsx');
assert.ok(app.includes('<a href="/dashboard.html" data-testid="topbar-dashboard">Dashboard</a><a href="/scenarios.html" data-testid="topbar-scenarios">Scenarios</a>'), 'top-bar link next to Dashboard');
assert.ok(html.includes('<script type="module" src="/src/scenarios/main.jsx"></script>') && html.includes('<title>PayGuard AI · Scenario work orders</title>'));
assert.equal(html.split('<link rel="stylesheet" href="/src/theme/base.css" />').length - 1, 1, 'base.css once');
assert.ok(read('frontend/vite.config.js').includes("scenarios: fileURLToPath(new URL('scenarios.html', import.meta.url))"), 'Vite entry');
assert.ok(read('Dockerfile').includes('frontend/scenarios.html'), 'hosted image copies the page');
// Design: tokens only (no raw hex colours), spacing from the 4/8/12/16/24/32 scale.
assert.ok(!/#[0-9a-f]{3,8}\b/i.test(css), 'no raw colours in scenarios.css');
for (const match of css.matchAll(/(?:padding|gap|margin)[^:;{]*:\s*([^;}]+)/g)) {
  for (const px of match[1].matchAll(/(\d+)px/g)) assert.ok([0, 1, 2, 4, 8, 12, 16, 24, 32].includes(Number(px[1])), `spacing ${px[0]} in "${match[0]}"`);
}

// 5. Public export: no Taiwan or Chinese text, so the page ships in the allowlist.
for (const [name, text] of [['main.jsx', page], ['workOrders.js', logic], ['scenarios.css', css], ['scenarios.html', html]]) {
  assert.ok(!/\p{Script=Han}|Taiwan|\bTW\b/u.test(text), `${name} has no Taiwan or Chinese text`);
}
const builder = read('tools/build_public_candidate.py');
for (const path of ['"frontend/scenarios.html"', '"tests/frontend_scenarios_contract.mjs"', '"frontend/src/scenarios": ("main.jsx", "scenarios.css", "workOrders.js")']) {
  assert.ok(builder.includes(path), `allowlist ${path}`);
}
console.log(`frontend_scenarios_contract: ok (${WORK_ORDERS.length} work orders, ${FORBIDDEN_PATHS.length} forbidden routes)`);
