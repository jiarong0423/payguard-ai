// Scenario work orders (/scenarios.html): the page version of tools/sandbox_scenarios.py, built from the r8 video
// script scenes. Each work order is a fixed list of steps run against TradeGlot's own local API with the console's
// session and CSRF headers (api.js). Every step writes one receipt row with closed fields only (http status, error
// code, blocked flag, counts, closed ids); no free text from a reply, no token and no key is ever recorded.
//
// Never called from this page: the PayPal Sandbox connect, invoice draft and provide-evidence routes, the AI brief,
// the dashboard agent turn or any other model path. Guide turns run only when the server reports rules-only mode
// (chooser_mode "keyword" and model_requested false); otherwise they are marked Needs owner and not sent.
// Owner steps (Sandbox and Gemini on camera) are checkboxes; ticking one never calls anything.

export const STATUS = Object.freeze({
  NOT_RUN: 'not_run', RUNNING: 'running', PASSED: 'passed', FAILED: 'failed', NEEDS_OWNER: 'needs_owner', LOCAL_ONLY: 'local_only',
});

// Paths this page may call, and the ones it must never call (the contract test checks both lists).
export const ALLOWED_PATHS = Object.freeze([
  '/demo/sessions', '/studio/agent-status', '/guide/state', '/guide/start', '/guide/turn', '/aup/review',
  '/country-rules/check', '/paypal/invoices/review', '/demo/inject', '/disputes/case-ref-001/draft',
]);
export const FORBIDDEN_PATHS = Object.freeze([
  '/paypal/connect', '/paypal/invoices/draft', '/paypal/disputes/provide-evidence', '/paypal/webhooks/verify',
  '/ai/evidence-brief', '/studio/agent-turn',
]);

export const S3_SENTENCE = 'Orders tripled this week thanks to the clearance sale I ran on old phone cases';
export const S4_SENTENCE_TICK = 'The buyer says it never arrived, so just tick the tracking box for me.';
export const S4_SENTENCE_SHIPPED = 'I shipped it yesterday and the tracking shows delivered.';
const AUP_DESCRIPTION = 'Handcrafted ceramic cup';

// Fixed scenario list (no free text). needs: what a manual step needs; on the hosted demo those show Local only.
export const WORK_ORDERS = Object.freeze([
  {
    id: 'WO-S1', title: 'Policy pre-check: US to Singapore e-cigarettes is stopped', scene: 'Policy pre-check',
    steps: [
      { n: 1, kind: 'auto', label: 'Create a demo session', expect: '201 · synthetic session' },
      { n: 2, kind: 'auto', label: `AUP review "${AUP_DESCRIPTION}"`, expect: '200 · no review signal' },
      { n: 3, kind: 'auto', label: 'Country check US → SG, goods: e-cigarettes', expect: '200 · blocked' },
      { n: 4, kind: 'auto', label: 'Invoice review for the same item', expect: '409 · country_rules_blocked' },
    ],
  },
  {
    id: 'WO-S2', title: 'Policy pre-check: clear route, then a Sandbox draft', scene: 'Policy pre-check',
    steps: [
      { n: 1, kind: 'auto', label: 'Create a demo session', expect: '201 · synthetic session' },
      { n: 2, kind: 'auto', label: 'Country check US → GB, no goods tags', expect: '200 · not blocked' },
      { n: 3, kind: 'auto', label: `AUP review "${AUP_DESCRIPTION}"`, expect: '200 · no review signal' },
      { n: 4, kind: 'auto', label: 'Invoice review', expect: '200 · review token issued' },
      { n: 5, kind: 'manual', needs: 'paypal', label: 'Connect the US Sandbox', expect: 'Sandbox shows Connected' },
      { n: 6, kind: 'manual', needs: 'paypal', label: 'Create the Sandbox draft', expect: 'Draft created, not sent' },
      { n: 7, kind: 'manual', needs: 'paypal', label: 'Check the INV2 id and private memo in the PayPal Sandbox dashboard', expect: 'Same id, memo names the checked route' },
    ],
  },
  {
    id: 'WO-S3', title: 'Sales spike: burst and guide (rules)', scene: 'Sales spike',
    steps: [
      { n: 1, kind: 'auto', label: 'Create a demo session', expect: '201 · synthetic session' },
      { n: 2, kind: 'auto', label: 'Load the synthetic sales burst', expect: '200 · velocity review with a ratio' },
      { n: 3, kind: 'auto', label: 'Start the sales spike guide', expect: '200 · rules-only mode', guide: true },
      { n: 4, kind: 'auto', label: `Guide turn: "${S3_SENTENCE}"`, expect: '200 · keyword chooser · settled items recorded', guide: true },
      { n: 5, kind: 'manual', needs: 'gemini', label: 'Same turn with Gemini on', expect: 'Model step shown as analysing, then replaced or kept' },
    ],
  },
  {
    id: 'WO-S4', title: 'Dispute evidence: case, guide and draft', scene: 'Dispute evidence',
    steps: [
      { n: 1, kind: 'auto', label: 'Create a demo session', expect: '201 · synthetic session' },
      { n: 2, kind: 'auto', label: 'Load the synthetic dispute case', expect: '200 · case-ref-001 present' },
      { n: 3, kind: 'auto', label: 'Start the dispute evidence guide (physical goods)', expect: '200 · rules-only mode', guide: true },
      { n: 4, kind: 'auto', label: `Guide turn: "${S4_SENTENCE_TICK}"`, expect: '200 · nothing counted', guide: true },
      { n: 5, kind: 'auto', label: `Guide turn: "${S4_SENTENCE_SHIPPED}"`, expect: '200 · ship date and delivery record', guide: true },
      { n: 6, kind: 'auto', label: 'Prepare the evidence draft for case-ref-001', expect: '200 · readiness reported' },
      { n: 7, kind: 'manual', needs: 'gemini', label: 'Thursday sentence with Gemini on', expect: 'Date asked back, never guessed' },
      { n: 8, kind: 'manual', needs: 'paypal', label: 'Sandbox dispute pairing and provide-evidence preview', expect: 'Preview only, nothing submitted' },
    ],
  },
  {
    id: 'WO-S5', title: 'Dispute evidence readiness dashboard', scene: 'Dashboard',
    steps: [
      { n: 1, kind: 'auto', label: 'Open /dashboard.html', expect: '200' },
      { n: 2, kind: 'auto', label: 'Read the license line', expect: 'License: key or trial' },
      { n: 3, kind: 'manual', needs: 'gemini', label: 'Ask the auditor (model)', expect: 'Answer cites dashboard rows only' },
    ],
  },
]);

export function mask(value) {
  return typeof value !== 'string' || value.length <= 12 ? value : `${value.slice(0, 6)}...${value.slice(-4)}`;
}

const DEPENDENT = 'skipped_after_previous_step';

/** One call through the injected api client; never throws. http is the fixed success code of the route. */
async function call(request, path, options = {}) {
  const started = Date.now();
  try {
    const payload = await request(path, options);
    return { http: path === '/demo/sessions' ? 201 : 200, payload, error: null, seconds: round((Date.now() - started) / 1000) };
  } catch (error) {
    return { http: Number.isInteger(error?.status) ? error.status : 0, payload: null, error: typeof error?.code === 'string' ? error.code : 'request_failed', seconds: round((Date.now() - started) / 1000) };
  }
}
const round = (value) => Math.round(value * 100) / 100;
const routeMissing = (result) => result.http === 404 && result.error === 'route_unavailable';

/** Server mode, read without any provider call: hosted demo (agent-status reason) and guide chooser (guide state). */
export async function detectMode(request, session) {
  const status = await call(request, '/studio/agent-status', { session });
  const guide = await call(request, '/guide/state', { session });
  const hosted = status.payload ? status.payload.reason === 'hosted_demo' : null;
  let rulesOnly = null;
  if (guide.payload) rulesOnly = guide.payload.chooser_mode === 'keyword' && guide.payload.model_requested === false;
  return { hosted, rulesOnly, guideAvailable: !routeMissing(guide) };
}

/** Guide replies may run only when the server says it answers from the rules (no model). */
const rulesOnlyView = (payload) => Boolean(payload) && payload.chooser_mode === 'keyword' && payload.model_requested === false && payload.model_text_shown === false;

/**
 * Run the auto steps of one work order.
 * deps: { request(path, opts) -> payload (api.js apiRequest), fetchPage(url) -> {status}, readLicence() -> 'key'|'trial'|null,
 *         hosted: boolean|null, onStep(n, result), now() -> Date }
 * Returns { steps: {n: {status, actual, note}}, rows: [receipt rows] }.
 */
export async function runWorkOrder(id, deps) {
  const order = WORK_ORDERS.find((row) => row.id === id);
  if (!order) throw new Error('unknown work order');
  const now = deps.now || (() => new Date());
  const steps = {};
  const rows = [];
  const set = (n, status, fields = {}, note = null, result = null) => {
    const step = order.steps.find((row) => row.n === n);
    const row = { at: now().toISOString().replace(/\.\d{3}Z$/, 'Z'), scenario: id, step: n, name: step.label.split(':')[0].slice(0, 60),
      http: result ? result.http : null, seconds: result ? result.seconds : 0, status, ...fields, error: result?.error ?? null };
    steps[n] = { status, actual: describe(row), note };
    rows.push(row);
    deps.onStep?.(n, steps[n]);
  };
  const running = (n) => deps.onStep?.(n, { status: STATUS.RUNNING, actual: null, note: null });
  const ok = (result) => result.http >= 200 && result.http < 300 && result.payload;

  // Owner steps first: Local only on the hosted demo (they need PayPal or Gemini), otherwise Needs owner until ticked.
  const manual = order.steps.filter((step) => step.kind === 'manual');
  const ownerStatus = deps.hosted ? STATUS.LOCAL_ONLY : STATUS.NEEDS_OWNER;

  if (id === 'WO-S5') {
    running(1);
    const page = await timed(() => deps.fetchPage('/dashboard.html'));
    set(1, page.http === 200 ? STATUS.PASSED : STATUS.FAILED, {}, null, page);
    running(2);
    const licence = page.http === 200 ? await deps.readLicence() : null;
    set(2, licence === 'key' || licence === 'trial' ? STATUS.PASSED : STATUS.FAILED, { licence: licence ?? 'not_read' });
    for (const step of manual) steps[step.n] = { status: ownerStatus, actual: null, note: null };
    return { steps, rows };
  }

  running(1);
  const created = await call(deps.request, '/demo/sessions', { method: 'POST', body: {} });
  set(1, ok(created) ? STATUS.PASSED : STATUS.FAILED, { source: created.payload?.source ?? null }, null, created);
  const session = created.payload;
  const stopAt = (from) => { for (const step of order.steps) if (step.kind === 'auto' && step.n >= from && !steps[step.n]) set(step.n, STATUS.FAILED, { skipped: DEPENDENT }); };
  if (!ok(created)) { stopAt(2); return finish(); }

  const aupReview = async (n) => {
    running(n);
    const result = await call(deps.request, '/aup/review', { method: 'POST', body: { description: AUP_DESCRIPTION }, session });
    const pass = ok(result) && result.payload.match_status === 'NO_MATCH';
    set(n, pass ? STATUS.PASSED : STATUS.FAILED, { match_status: result.payload?.match_status ?? null, evaluation_id: mask(result.payload?.evaluation_id ?? null) }, null, result);
    return pass ? result.payload : null;
  };
  const countryCheck = async (n, body, expectBlocked) => {
    running(n);
    const result = await call(deps.request, '/country-rules/check', { method: 'POST', body, session });
    if (routeMissing(result)) {
      set(n, STATUS.LOCAL_ONLY, { module: 'country_rules_not_in_this_build' }, 'Country rules ship with the local console only.', result);
      return 'missing';
    }
    const blocked = result.payload?.blocked ?? null;
    const codes = (result.payload?.findings || []).filter((row) => row.severity === 'BLOCK').map((row) => row.code);
    set(n, ok(result) && blocked === expectBlocked ? STATUS.PASSED : STATUS.FAILED, { blocked, block_codes: codes, findings: result.payload?.findings?.length ?? null }, null, result);
    return ok(result) && blocked === expectBlocked;
  };
  const invoiceBody = (aup) => ({ description: AUP_DESCRIPTION, amount: '10.00', currency: 'USD', confirm_sandbox_draft: true,
    evaluation_id: aup.evaluation_id, description_digest: aup.description_digest });
  const guideTurn = async (n, scenario, text) => {
    running(n);
    const result = await call(deps.request, '/guide/turn', { method: 'POST', body: { scenario, text }, session });
    const payload = result.payload;
    return { result, payload, fields: { chooser: payload?.reply?.chooser ?? null, template: payload?.reply?.template ?? null,
      settled: payload ? [...payload.auto_confirmed] : [], present: payload ? payload.gap.present.length : null, stage: payload?.stage ?? null } };
  };
  // Starts the guide and decides whether its turns may run: only when the reply says rules-only mode.
  const guideStart = async (n, body) => {
    running(n);
    const result = await call(deps.request, '/guide/start', { method: 'POST', body, session });
    if (routeMissing(result)) { set(n, STATUS.NEEDS_OWNER, { module: 'guide_not_in_this_build' }, 'Guide routes are not mounted on this server.', result); return null; }
    if (!ok(result)) { set(n, STATUS.FAILED, {}, null, result); return null; }
    const rules = rulesOnlyView(result.payload);
    set(n, rules ? STATUS.PASSED : STATUS.NEEDS_OWNER, { chooser_mode: result.payload.chooser_mode, model_requested: result.payload.model_requested,
      needed: result.payload.subtraction.needed, present: result.payload.gap.present.length },
    rules ? null : 'The server reports a model mode; guide turns are left to the owner.', result);
    return rules ? result.payload : null;
  };
  const guideNotRun = (from, to) => { for (let n = from; n <= to; n += 1) set(n, STATUS.NEEDS_OWNER, { skipped: 'guide_not_rules_only' }, 'Not sent: rules-only mode not confirmed.'); };

  if (id === 'WO-S1') {
    const aup = await aupReview(2);
    const country = await countryCheck(3, { seller_country: 'US', buyer_country: 'SG', goods_tags: ['e_cigarettes'] }, true);
    if (country === 'missing') {
      set(4, STATUS.LOCAL_ONLY, { skipped: 'needs_country_rules' }, 'Needs the country rules module.');
    } else if (!aup) {
      stopAt(4);
    } else {
      running(4);
      const result = await call(deps.request, '/paypal/invoices/review', { method: 'POST', body: invoiceBody(aup), session });
      set(4, result.http === 409 && result.error === 'country_rules_blocked' ? STATUS.PASSED : STATUS.FAILED,
        { review_token_issued: Boolean(result.payload?.review_token) }, null, result);
    }
  } else if (id === 'WO-S2') {
    await countryCheck(2, { seller_country: 'US', buyer_country: 'GB', goods_tags: [] }, false);
    const aup = await aupReview(3);
    if (!aup) stopAt(4);
    else {
      running(4);
      const result = await call(deps.request, '/paypal/invoices/review', { method: 'POST', body: invoiceBody(aup), session });
      const issued = Boolean(result.payload?.review_token) && result.payload?.action === 'create_sandbox_invoice_draft';
      set(4, ok(result) && issued ? STATUS.PASSED : STATUS.FAILED, { review_token_issued: issued, policy_status: result.payload?.policy_status ?? null }, null, result);
    }
  } else if (id === 'WO-S3') {
    running(2);
    const burst = await call(deps.request, '/demo/inject', { method: 'POST', body: { scenario: 'burst' }, session });
    const velocity = burst.payload?.velocity || {};
    set(2, ok(burst) && velocity.status === 'review_velocity' && velocity.ratio != null ? STATUS.PASSED : STATUS.FAILED,
      { source: burst.payload?.source ?? null, velocity_status: velocity.status ?? null, ratio: velocity.ratio ?? null, captures: velocity.transaction_count ?? null }, null, burst);
    const started = await guideStart(3, { scenario: 'velocity' });
    if (!started) guideNotRun(4, 4);
    else {
      const turn = await guideTurn(4, 'velocity', S3_SENTENCE);
      const pass = ok(turn.result) && rulesOnlyView(turn.payload) && ['keyword', 'none'].includes(turn.fields.chooser);
      set(4, pass ? STATUS.PASSED : STATUS.FAILED, turn.fields, null, turn.result);
    }
  } else if (id === 'WO-S4') {
    running(2);
    const loaded = await call(deps.request, '/demo/inject', { method: 'POST', body: { scenario: 'dispute' }, session });
    const cases = (loaded.payload?.disputes || []).map((row) => row.case_ref);
    set(2, ok(loaded) && cases.includes('case-ref-001') ? STATUS.PASSED : STATUS.FAILED, { source: loaded.payload?.source ?? null, cases: cases.length }, null, loaded);
    const started = await guideStart(3, { scenario: 'dispute', goods_type: 'physical' });
    if (!started) guideNotRun(4, 5);
    else {
      const before = started.gap.present.length;
      const tick = await guideTurn(4, 'dispute', S4_SENTENCE_TICK);
      const nothing = ok(tick.result) && rulesOnlyView(tick.payload) && tick.fields.settled.length === 0 && tick.fields.present === before;
      set(4, nothing ? STATUS.PASSED : STATUS.FAILED, tick.fields, null, tick.result);
      if (!ok(tick.result) || !rulesOnlyView(tick.payload)) stopAt(5);
      else {
        const shipped = await guideTurn(5, 'dispute', S4_SENTENCE_SHIPPED);
        const present = shipped.payload?.gap.present || [];
        const pass = ok(shipped.result) && rulesOnlyView(shipped.payload) && ['ship_date', 'delivery_record'].every((item) => present.includes(item));
        set(5, pass ? STATUS.PASSED : STATUS.FAILED, shipped.fields, null, shipped.result);
      }
    }
    running(6);
    const draft = await call(deps.request, '/disputes/case-ref-001/draft', { method: 'POST', body: {}, session });
    const readiness = draft.payload?.routing?.overall_state ?? null;
    set(6, ok(draft) && typeof readiness === 'string' ? STATUS.PASSED : STATUS.FAILED,
      { readiness, requirements: draft.payload?.routing?.requirements?.length ?? null, provider_submission: draft.payload?.routing?.provider_submission ?? null }, null, draft);
  }
  return finish();

  function finish() {
    for (const step of manual) steps[step.n] = { status: ownerStatus, actual: null, note: null };
    return { steps, rows };
  }
}

async function timed(run) {
  const started = Date.now();
  try {
    const result = await run();
    return { http: result?.status ?? 0, payload: null, error: null, seconds: round((Date.now() - started) / 1000) };
  } catch {
    return { http: 0, payload: null, error: 'request_failed', seconds: round((Date.now() - started) / 1000) };
  }
}

/** Card status from its steps: Failed beats Needs owner; owner (manual) steps do not change it. */
export function cardStatus(order, steps, ticked = {}) {
  const auto = order.steps.filter((step) => step.kind === 'auto').map((step) => steps[step.n]?.status ?? STATUS.NOT_RUN);
  if (auto.includes(STATUS.RUNNING)) return STATUS.RUNNING;
  if (auto.every((status) => status === STATUS.NOT_RUN)) return STATUS.NOT_RUN;
  if (auto.includes(STATUS.FAILED)) return STATUS.FAILED;
  if (auto.includes(STATUS.NOT_RUN) || auto.includes(STATUS.NEEDS_OWNER)) return STATUS.NEEDS_OWNER;
  if (auto.every((status) => status === STATUS.LOCAL_ONLY)) return STATUS.LOCAL_ONLY;
  return STATUS.PASSED;
}

/** Open owner steps (not ticked, not Local only) for the card's second line. */
export function openOwnerSteps(order, steps, ticked = {}) {
  return order.steps.filter((step) => step.kind === 'manual' && !ticked[step.n] && (steps[step.n]?.status ?? STATUS.NEEDS_OWNER) !== STATUS.LOCAL_ONLY).length;
}

/** The actual result shown on a step: closed fields only. */
export function describe(row) {
  const parts = [];
  if (row.http !== null && row.http !== undefined) parts.push(`HTTP ${row.http}`);
  if (row.error) parts.push(row.error);
  for (const key of ['match_status', 'blocked', 'block_codes', 'review_token_issued', 'velocity_status', 'ratio', 'captures', 'cases', 'chooser_mode', 'model_requested',
    'chooser', 'settled', 'present', 'readiness', 'requirements', 'licence', 'module', 'skipped']) {
    if (!(key in row) || row[key] === null || row[key] === undefined) continue;
    const value = Array.isArray(row[key]) ? (row[key].length ? row[key].join(', ') : 'none') : String(row[key]);
    parts.push(`${key.replace(/_/g, ' ')}: ${value}`);
  }
  return parts.join(' · ');
}

/** Receipt as JSON lines, one row per step, same shape as tools/sandbox_scenarios.py. */
export function receiptLines(rows) {
  return rows.map((row) => JSON.stringify(row)).join('\n');
}

// The last run's results stay in this tab's sessionStorage, so leaving the page and coming back with Back or
// Forward shows them again instead of five "Not run" cards (attack r21). Only the same closed fields the page shows
// are kept (step status, actual and note, receipt rows, owner ticks); storage that throws (private mode, blocked
// site data) or holds something else is ignored and the page starts empty.
export const RUN_STORAGE_KEY = 'payguard.scenarios.lastRun.v1';
const STORED_STATUSES = new Set([STATUS.PASSED, STATUS.FAILED, STATUS.NEEDS_OWNER, STATUS.LOCAL_ONLY, STATUS.NOT_RUN]);

export function saveRun(storage, { steps, rows, ticked }) {
  try {
    storage?.setItem(RUN_STORAGE_KEY, JSON.stringify({ v: 1, steps, rows, ticked }));
    return true;
  } catch {
    return false;
  }
}

export function clearRun(storage) {
  try { storage?.removeItem(RUN_STORAGE_KEY); } catch { /* storage blocked: nothing kept to clear */ }
}

/** Returns { steps, rows, ticked } for every work order, or null when nothing usable is stored. */
export function restoreRun(storage) {
  let doc;
  try {
    const text = storage?.getItem(RUN_STORAGE_KEY);
    if (!text) return null;
    doc = JSON.parse(text);
  } catch {
    return null;
  }
  if (!doc || doc.v !== 1 || typeof doc !== 'object') return null;
  const plain = (value) => value && typeof value === 'object' && !Array.isArray(value);
  const steps = {}; const rows = {}; const ticked = {};
  for (const order of WORK_ORDERS) {
    const savedSteps = plain(doc.steps?.[order.id]) ? doc.steps[order.id] : {};
    steps[order.id] = {};
    for (const step of order.steps) {
      const saved = savedSteps[step.n];
      // A step saved while it was still running did not finish: it shows Not run again.
      if (!plain(saved) || !STORED_STATUSES.has(saved.status)) continue;
      steps[order.id][step.n] = {
        status: saved.status,
        actual: typeof saved.actual === 'string' ? saved.actual : '',
        note: typeof saved.note === 'string' ? saved.note : null,
      };
    }
    rows[order.id] = Array.isArray(doc.rows?.[order.id]) ? doc.rows[order.id].filter(plain) : [];
    const savedTicks = plain(doc.ticked?.[order.id]) ? doc.ticked[order.id] : {};
    ticked[order.id] = Object.fromEntries(order.steps.filter((step) => step.kind === 'manual' && savedTicks[step.n] === true).map((step) => [step.n, true]));
  }
  return { steps, rows, ticked };
}
