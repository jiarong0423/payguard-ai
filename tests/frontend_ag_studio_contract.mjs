// Contract for the AG Studio dispute evidence readiness dashboard (/dashboard.html).
//   1. Packages: ag-studio and ag-studio-react pinned exactly; React 19 inside their peer range.
//   2. Entry: a third Vite page, linked from the evidence page only, copied into the hosted image.
//   3. Licence: read from import.meta.env.VITE_AG_STUDIO_LICENSE at build time; no key in the repository.
//   4. Data: every table comes from a file in the repository; the dispute file has no drift against the
//      real backend (tools/build_dashboard_data.py --check); the Channel3 copy is byte-identical.
//   5. Layout: every mapped field exists, no widget overlaps another, the phone layout stacks cleanly.
//   6. Auditor: answers fixed questions with code, shows them with Studio tools, never decides, and its
//      canvas filter selects exactly the rows its code selected.
//   7. Render (skipped without Playwright): a fresh build in headless Chromium, the auditor answers on the
//      canvas and the page requests nothing but its own origin.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readdirSync, readFileSync, rmSync } from 'node:fs';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { benchmarkRows, caseRows, daysBetween, rebaseDisputes, receiptRows, requirementRows, studioData, timeEventRows } from '../frontend/src/dashboard/dashboardData.js';
import { ANSWER_SLOT as LAYOUT_SLOT, ANSWER_SLOT_ID, CHECKLIST_WIDGET, compactLayout, DEADLINE_WIDGET, GUIDE_ANSWER_SLOT_ID, initialReport, READINESS_PAGE_ID } from '../frontend/src/dashboard/layout.js';
import { ANSWER_PAGE_ID, ANSWER_SLOT, ANSWER_SLOTS, ANSWER_WIDGET_ID, BOUNDARY, BUILT_IN_OFF, createEvidenceAuditor, matchQuestion, pageSelections, PROMPT_STARTERS, QUESTIONS } from '../frontend/src/dashboard/auditor.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');
const read = (path) => readFileSync(resolve(projectRoot, path), 'utf8');
const json = (path) => JSON.parse(read(path));

// 1. Packages
const packageJson = json('frontend/package.json');
const lock = json('frontend/package-lock.json');
for (const name of ['ag-studio', 'ag-studio-react']) {
  assert.equal(packageJson.dependencies[name], '3.0.0', `${name} pinned exactly`);
  assert.equal(lock.packages[`node_modules/${name}`].version, '3.0.0', `${name} locked at 3.0.0`);
  assert.equal(lock.packages[`node_modules/${name}`].license, 'Commercial');
}
assert.equal(lock.packages['node_modules/ag-studio-react'].peerDependencies.react, '^17.0.0 || ^18.0.0 || ^19.0.0');
assert.match(packageJson.dependencies.react, /^19\./u, 'React 19 is inside the ag-studio-react peer range');
assert.equal(lock.packages['node_modules/ag-grid-enterprise'].version, lock.packages['node_modules/ag-grid-community'].version, 'one AG Grid version');
const notices = read('THIRD_PARTY_NOTICES.md');
for (const token of ['ag-studio@3.0.0', 'ag-studio-react@3.0.0', 'ag-grid-enterprise@36.2.0', 'ag-charts-enterprise@14.2.0', 'tslib@2.9.1']) {
  assert.ok(notices.includes(`\`${token}\``), `notice lists ${token}`);
}

// 2. Entry and links
const viteConfig = read('frontend/vite.config.js');
assert.ok(viteConfig.includes("dashboard: fileURLToPath(new URL('dashboard.html', import.meta.url))"), 'third Vite entry');
assert.ok(read('frontend/dashboard.html').includes('<script type="module" src="/src/dashboard/main.jsx"></script>'));
assert.ok(read('frontend/src/evidence.jsx').includes('href="/dashboard.html"'), 'linked from the evidence page');
// Round 6: linked from the console too (top bar and step 03), and the dashboard links back.
const appSource = read('frontend/src/App.jsx');
assert.ok(appSource.includes('<a href="/dashboard.html" data-testid="topbar-dashboard">Dashboard</a>'), 'top-bar link');
assert.ok(appSource.includes('href="/dashboard.html" data-testid="dispute-dashboard-cta"'), 'step 03 call to action next to the case review');
assert.ok(read('frontend/src/dashboard/main.jsx').includes('<a className="pg-back" href="/" data-testid="dashboard-back-to-console">Back to console</a>'));
assert.ok(read('Dockerfile').includes('frontend/dashboard.html'), 'hosted image copies the dashboard page');

// 3. Licence: build-time variable only, never a committed key
const mainSource = read('frontend/src/dashboard/main.jsx');
assert.ok(mainSource.includes('import.meta.env.VITE_AG_STUDIO_LICENSE'), 'key read from the build-time variable');
assert.ok(mainSource.includes('<AgStudioProvider licenseKey={LICENSE_KEY}'), 'key handed to the provider, nowhere else');
assert.equal(/setLicenseKey\(\s*['"`]/u.test(mainSource), false, 'no literal key');
// (optimise r24) CI sets PAYGUARD_SKIP_ENV_LOCAL_CHECK=1: only this local .env* key check is skipped, and no .env* file
// is opened then. A CI checkout has no .env file; every other assertion of this test still runs.
if (process.env.PAYGUARD_SKIP_ENV_LOCAL_CHECK !== '1') {
  for (const name of readdirSync(frontendRoot)) {
    if (name.startsWith('.env')) assert.equal(/VITE_AG_STUDIO_LICENSE\s*=\s*\S/u.test(readFileSync(join(frontendRoot, name), 'utf8')), false, `${name} holds no key`);
  }
}
const dashboardDir = 'frontend/src/dashboard';
const dashboardSources = Object.fromEntries(readdirSync(resolve(projectRoot, dashboardDir)).filter((file) => /\.(jsx?|css)$/u.test(file)).map((file) => [file, read(`${dashboardDir}/${file}`)]));
for (const [file, source] of Object.entries(dashboardSources)) {
  assert.equal(/_Enterprise_key|\[TRIAL\]|AG_Studio_key|licen[cs]eKey\s*[:=]\s*['"`][A-Za-z0-9]/u.test(source), false, `${file} holds no licence key`);
  assert.equal(/fetch\(|XMLHttpRequest|WebSocket|EventSource|https?:\/\//u.test(source), false, `${file} makes no network call`);
  // Only the agent client talks to the backend, and only to the session, status and governed turn routes.
  if (file === 'studioAgentClient.js') {
    assert.deepEqual([...new Set(source.match(/\/api\/v1\/[a-z/-]+/gu))].sort(), ['/api/v1/demo/sessions', '/api/v1/studio/agent-status', '/api/v1/studio/agent-turn']);
  } else {
    assert.equal(/apiRequest|\/api\/v1|fetchImpl/u.test(source), false, `${file} does not call the backend`);
  }
}
assert.ok(mainSource.includes('loadThemeGoogleFonts={false}'), 'no font download');
assert.ok(dashboardSources['theme.js'].includes('studioTheme.withParams('), 'custom Studio theme');
// Round 6: the same accent as the seller console's buttons. (P1 2026-11-12) The accent now comes from the design tokens
// (ink, "Editorial Newsprint") instead of the written indigo '#4f46e5'; the check follows the token, not a hex value.
assert.ok(dashboardSources['theme.js'].includes("import { categorical, color } from '../theme/tokens.js';") && dashboardSources['theme.js'].includes('accent: color.accent'), 'console accent from the design tokens');
assert.equal(/#[0-9a-f]{6}/iu.test(dashboardSources['theme.js']), false, 'no written hex colours in the Studio theme');
assert.ok(read('frontend/src/index.css').includes('.button-blue { background: #2563eb;'), 'console button accent');

// 4. Data: real files only, no drift, numbers traced to their source
const disputes = json('frontend/src/data/dashboard_disputes_v1.json');
const benchmark = json('frontend/src/data/guide_benchmark_v1.json');
const receipts = json('frontend/src/data/channel3_receipts_v1.json');
assert.equal(read('frontend/src/data/channel3_receipts_v1.json'), read('docs/evidence/channel3_receipts_v1.json'), 'Channel3 copy is byte-identical');
assert.equal(disputes.synthetic, true);
assert.equal(disputes.affects_decision, false);
// Three since round 5: case-ref-003 is the synthetic "due within 3 days, evidence missing" case.
assert.equal(disputes.cases.length, 3);
for (const item of disputes.cases) {
  assert.equal(item.provider_submission, 'NOT_PERFORMED', 'nothing submitted');
  assert.equal(item.human_review_required, true);
  if (item.time_evidence) assert.equal(item.time_evidence.judgement, 'NOT_MADE');
}
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');
const drift = spawnSync(python, ['tools/build_dashboard_data.py', '--check'], {
  cwd: projectRoot, encoding: 'utf8', env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' },
});
assert.equal(drift.status, 0, `dashboard data drift: ${drift.stdout}${drift.stderr}`);

const cases = caseRows(disputes);
assert.deepEqual(cases.map((row) => row.days_to_due), disputes.cases.map((item) => daysBetween(disputes.as_of, item.seller_response_due_date)));
assert.deepEqual(cases.map((row) => row.delivery_proof), disputes.cases.map((item) => (item.requirements.some((row) => row.accepted_attachment_count > 0) ? 'Attachment on file' : 'No attachment on file')));
assert.deepEqual(cases.map((row) => row.time_flag_count), disputes.cases.map((item) => item.time_evidence?.flags.length || 0));
assert.deepEqual(requirementRows(disputes).map((row) => [row.proof_count, row.attachment_count]),
  disputes.cases.flatMap((item) => item.requirements.map((row) => [row.proof_count, row.accepted_attachment_count])));
assert.equal(timeEventRows(disputes).length, disputes.cases.reduce((sum, item) => sum + (item.time_evidence?.events.length || 0), 0));
// r20 UX-1: the page moves the cases to its own clock, like the console; days to due and gaps stay as built.
const NOW_ISO = '2026-11-03T11:10:19.000Z';
const rebased = rebaseDisputes(disputes, NOW_ISO);
assert.equal(rebased.as_of, NOW_ISO);
assert.equal(rebased.built_as_of, disputes.as_of);
assert.deepEqual(caseRows(rebased).map((row) => row.days_to_due), cases.map((row) => row.days_to_due));
assert.deepEqual(timeEventRows(rebased).map((row) => row.gap_hours), timeEventRows(disputes).map((row) => row.gap_hours));
const shiftMs = Date.parse(NOW_ISO) - Date.parse(disputes.as_of);
assert.deepEqual(rebased.cases.map((item) => Date.parse(item.seller_response_due_date)), disputes.cases.map((item) => Date.parse(item.seller_response_due_date) + shiftMs));
assert.ok(read('frontend/src/dashboard/main.jsx').includes('const disputes = rebaseDisputes(disputesFile,'), 'dashboard uses the rebased cases');
assert.deepEqual(benchmarkRows(benchmark).map((row) => row.model_calls), benchmark.flows.map((flow) => flow.model_calls));
assert.deepEqual(receiptRows(receipts).map((row) => [row.query, row.latency_seconds, row.cards]), receipts.receipts.map((row) => [row.query, row.latency_seconds, row.cards]));
const data = studioData({ disputes, benchmark, receipts });
assert.deepEqual(data.sources.map((source) => source.id), ['cases', 'requirements', 'time_events', 'benchmark', 'receipts']);
const fieldIds = new Set(data.sources.flatMap((source) => source.fields.map((field) => `${source.id}.${field.id}`)));
for (const source of data.sources) {
  for (const row of source.data) assert.deepEqual(Object.keys(row).sort(), source.fields.map((field) => field.id).sort(), `${source.id} rows match their fields`);
}
for (const relation of data.relationships) {
  assert.ok(fieldIds.has(`${relation.source.tableId}.${relation.source.fieldId}`) && fieldIds.has(`${relation.target.tableId}.${relation.target.fieldId}`));
}

// 5. Layout
function assertNoOverlap(layout, context) {
  const boxes = Object.entries(layout);
  for (const [id, box] of boxes) {
    assert.ok(box.xTrack >= 0 && box.xTrack + box.xSpan <= 24 && box.yTrack >= 0 && box.ySpan > 0, `${context}: ${id} inside the 24-column canvas`);
  }
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      const [a, A] = boxes[i];
      const [b, B] = boxes[j];
      const apart = A.xTrack + A.xSpan <= B.xTrack || B.xTrack + B.xSpan <= A.xTrack || A.yTrack + A.ySpan <= B.yTrack || B.yTrack + B.ySpan <= A.yTrack;
      assert.ok(apart, `${context}: ${a} overlaps ${b}`);
    }
  }
}
const customTypes = new Set([DEADLINE_WIDGET, CHECKLIST_WIDGET]);
for (const compact of [false, true]) {
  const report = initialReport({ compact });
  for (const page of report.pages) {
    assert.deepEqual(Object.keys(page.widgets).sort(), Object.keys(page.widgetLayout).sort(), `${page.id}: every widget has a place`);
    assertNoOverlap(page.widgetLayout, `${page.id}${compact ? ' (phone)' : ''}`);
    for (const [id, widget] of Object.entries(page.widgets)) {
      for (const refs of Object.values(widget.dataMapping)) for (const ref of refs) assert.ok(fieldIds.has(ref.id), `${page.id}.${id} maps a real field: ${ref.id}`);
      if (customTypes.has(widget.type)) customTypes.delete(widget.type);
    }
    for (const filters of Object.values(page.filter?.widget || {})) for (const filter of filters) assert.ok(fieldIds.has(filter.field.id));
  }
  if (compact) for (const page of report.pages) assert.ok(Object.values(page.widgetLayout).every((box) => box.xSpan >= 12), 'phone layout: no widget narrower than half the screen');
}
assert.equal(customTypes.size, 0, 'both custom widgets are on the canvas');
assert.ok(dashboardSources['widgets.jsx'].includes('id: DEADLINE_WIDGET') && dashboardSources['widgets.jsx'].includes('id: CHECKLIST_WIDGET'), 'custom widgets registered');
assert.ok(dashboardSources['widgets.jsx'].includes('widgetApi.toggleCrossFilter('), 'checklist cross-filters the page');
assert.ok(dashboardSources['widgets.jsx'].includes("widgetApi.getData({ fields }, { crossFilter })"), 'custom widgets read filtered data from Studio');
assert.deepEqual(compactLayout({ a: { xTrack: 0, yTrack: 0, xSpan: 8, ySpan: 6 }, b: { xTrack: 8, yTrack: 0, xSpan: 8, ySpan: 6 }, c: { xTrack: 0, yTrack: 6, xSpan: 24, ySpan: 20 } }),
  { a: { xTrack: 0, yTrack: 0, xSpan: 12, ySpan: 6 }, b: { xTrack: 12, yTrack: 0, xSpan: 12, ySpan: 6 }, c: { xTrack: 0, yTrack: 6, xSpan: 24, ySpan: 20 } });

// 6. Auditor with stand-in Studio tools: seven closed questions, one per part of the dashboard.
assert.equal(ANSWER_WIDGET_ID, ANSWER_SLOT_ID);
assert.equal(ANSWER_SLOTS.guide, GUIDE_ANSWER_SLOT_ID);
assert.equal(ANSWER_PAGE_ID, READINESS_PAGE_ID);
assert.deepEqual(ANSWER_SLOT, LAYOUT_SLOT, 'the answer fills exactly the reserved slot');
assert.deepEqual(PROMPT_STARTERS.slice(0, 3).map((entry) => entry.prompt), ['Which cases lack proof of delivery?', 'Which are due within 3 days?', 'Which cases have time flags?']);

function standInStudio(failOn) {
  const calls = [];
  const make = (name, toolName) => (...bind) => ({
    name: toolName, description: name, kind: 'client', schema: () => ({}),
    async execute(invocation, ctx) {
      calls.push({ name, tool: toolName, bind, args: invocation.args });
      assert.equal(typeof ctx.success, 'function');
      return name === failOn ? ctx.error('stand-in failure') : ctx.success(`${toolName} ok`);
    },
  });
  return {
    calls,
    studio: { addWidget: make('addWidget', 'add_widget'), removeWidget: make('removeWidget', 'remove_widget'),
      configureWidget: make('configureWidget', 'configure_widget'), addWidgetFilter: make('addWidgetFilter', 'add_widget_filter') },
  };
}
const tables = Object.fromEntries(data.sources.map((source) => [source.id, source.data]));
const stateWithSlot = initialReport();
async function ask(text, { failOn, state = stateWithSlot } = {}) {
  const { studio, calls } = standInStudio(failOn);
  const pages = [];
  const technical = [];
  const agent = createEvidenceAuditor({ studio, getState: () => state, data: tables, onAnswer: (page, steps) => { pages.push(page); technical.push(steps); } });
  const events = [];
  for await (const event of agent.run({ threadId: 't1', runId: `r-${events.length}`, messages: [{ id: 'u1', role: 'user', content: text }], tools: [], state: null, context: [], forwardedProps: {} })) events.push(event);
  const reply = events.filter((event) => event.type === 'TEXT_MESSAGE_CONTENT').map((event) => event.delta).join('');
  return { events, calls, reply, pages, technical, finished: events.find((event) => event.type === 'RUN_FINISHED') };
}
function applyFilter(filter, row) {
  const value = row[filter.field.id.split('.').pop()];
  const { operator, value: target } = filter.model;
  if (value === null) return false;
  if (operator === 'equals') return value === target;
  if (operator === 'lessThanOrEqual') return value <= target;
  if (operator === 'greaterThan') return value > target;
  if (operator === 'greaterThanOrEqual') return value >= target;
  throw new Error(`unexpected operator ${operator}`);
}
const FORBIDDEN_REPLY = /\b(win|lose|guarantee|approved?|reject(ed)?|fraud|liable|will be resolved|should refund)\b/iu;

// The expected answers are derived here from the files, independently of the auditor's own code.
const maxGap = Math.max(...tables.time_events.map((row) => row.gap_hours ?? -1));
const minCalls = Math.min(...benchmark.flows.map((flow) => flow.model_calls));
const maxLatency = Math.max(...receipts.receipts.map((row) => row.latency_seconds));
const expected = {
  'Which cases lack proof of delivery?': { page: 'readiness', table: 'cases', refs: disputes.cases.filter((item) => !item.requirements.some((row) => row.accepted_attachment_count > 0)).map((item) => item.case_ref) },
  'Which are due within 3 days?': { page: 'readiness', table: 'cases', refs: tables.cases.filter((row) => row.days_to_due <= 3).map((row) => row.case_ref) },
  'Which cases have time flags?': { page: 'readiness', table: 'cases', refs: disputes.cases.filter((item) => item.time_evidence?.flags.length).map((item) => item.case_ref) },
  'Where is the longest gap between recorded events?': { page: 'readiness', table: 'time_events', refs: tables.time_events.filter((row) => row.gap_hours === maxGap).map((row) => row.event_id) },
  'What evidence does each case still need?': { page: 'readiness', table: 'requirements', refs: tables.requirements.filter((row) => row.mandatory === 'Mandatory').map((row) => row.requirement_id) },
  'Which guide flow needs the fewest model calls?': { page: 'guide', table: 'benchmark', refs: benchmark.flows.filter((flow) => flow.model_calls === minCalls).map((flow) => flow.id) },
  'Which Channel3 search was slowest?': { page: 'guide', table: 'receipts', refs: tables.receipts.filter((row) => row.latency_seconds === maxLatency).map((row) => row.receipt_id) },
};
assert.equal(QUESTIONS.length, Object.keys(expected).length, 'seven closed questions');
const keyOf = { cases: 'case_ref', time_events: 'event_id', requirements: 'requirement_id', benchmark: 'flow_id', receipts: 'receipt_id' };
// Which Studio tool calls each question makes, recorded (round 6, item 2).
const studioCalls = {};
for (const [question, want] of Object.entries(expected)) {
  const { events, calls, reply, pages, technical, finished } = await ask(question);
  assert.ok(want.refs.length > 0, `${question}: the data has an answer`);
  assert.equal(events[0].type, 'RUN_STARTED');
  assert.equal(events.at(-1).type, 'RUN_FINISHED', `${question}: run finishes`);
  assert.deepEqual(finished.result.refs, want.refs, `${question}: answered from the data`);
  studioCalls[question] = calls.map((call) => `${call.tool}@${call.bind.at(-1).pageId}`);
  assert.deepEqual(studioCalls[question], ['remove_widget', 'add_widget', 'configure_widget', 'add_widget_filter'].map((tool) => `${tool}@${want.page}`),
    `${question}: built with Studio tools on the ${want.page} page`);
  const slot = ANSWER_SLOTS[want.page];
  assert.deepEqual(calls[0].args, { widgetId: slot });
  assert.deepEqual(calls[1].args, { widgetId: slot, type: 'grid', ...ANSWER_SLOT });
  assert.equal(calls[2].bind[0].widgetId, slot);
  assert.ok(calls[2].args.value.dataMapping.cols.every((col) => fieldIds.has(col.id) && col.id.startsWith(`${want.table}.`)));
  const filter = calls[3].args.value;
  assert.ok(fieldIds.has(filter.field.id));
  assert.deepEqual(tables[want.table].filter((row) => applyFilter(filter, row)).map((row) => row[keyOf[want.table]]), want.refs, `${question}: canvas filter selects the same rows`);
  assert.equal(events.filter((event) => event.type === 'TOOL_CALL_START').length, 4);
  assert.equal(events.filter((event) => event.type === 'TOOL_CALL_RESULT').length, 4);
  // (r31 J1 J4) The AI panel says the four steps in plain words, in the order of the Studio calls; no tool name or
  // backtick on screen. The exact tool names reach the dashboard's collapsed "Technical steps" in the same order.
  const tableWords = want.table.replace(/_/gu, ' ');
  const pageWords = want.page === 'guide' ? 'Guide and Channel3 evidence' : 'Evidence readiness';
  const op = { equals: '=', lessThanOrEqual: '≤', greaterThan: '>', greaterThanOrEqual: '≥' }[filter.model.operator];
  const filterWords = `${filter.field.id.split('.').pop().replace(/_/gu, ' ')} ${op} ${typeof filter.model.value === 'string' ? `"${filter.model.value}"` : filter.model.value}`;
  // (r32 J3 P3) On a fresh page the slot holds the page's own table, so the first step names it.
  const pageTable = stateWithSlot.pages.find((page) => page.id === want.page).widgets[slot].format.title.text;
  assert.ok(reply.includes(`How I built this: 1. Replaced the page's ${pageTable} table with the answer. 2. Added a table under the headline tiles of the ${pageWords} page. 3. Showed ${calls[2].args.value.dataMapping.cols.length} columns from ${tableWords}. 4. Filtered: ${filterWords}. `),
    `${question}: build steps shown in plain words in the AI panel`);
  assert.equal(/`|remove_widget|add_widget|configure_widget|add_widget_filter|_[a-z]/u.test(reply.slice(reply.indexOf('How I built this'))), false, `${question}: no tool name, id or backtick in the reply`);
  assert.equal(technical.length, 1, `${question}: technical steps handed to the dashboard once`);
  assert.deepEqual(technical[0].map((step) => step.tool), calls.map((call) => call.tool), `${question}: technical steps name the exact tools in call order`);
  assert.equal(technical[0][3].detail, `${filter.field.id} ${op} ${JSON.stringify(filter.model.value)}`, `${question}: technical filter keeps the exact field id`);
  assert.ok(reply.includes(BOUNDARY), `${question}: boundary stated`);
  assert.deepEqual(pages, [want.page], `${question}: the dashboard shows the page that changed`);
  assert.equal(FORBIDDEN_REPLY.test(reply.replace(BOUNDARY, '')), false, `${question}: no decision language`);
}
const unknown = await ask('Please approve case-ref-001 and refund it');
assert.equal(matchQuestion('Please approve case-ref-001 and refund it').id, 'unknown');
assert.equal(matchQuestion('Make a widget comparing cases by days to due').id, 'unknown', 'the delegation example is not one of the fixed questions');
assert.equal(matchQuestion('Which reason code appears most often across the three cases?').id, 'unknown', 'the live starter question is delegated, not answered by a fixed question');
assert.deepEqual(unknown.calls, [], 'an unknown request changes nothing on the canvas');
assert.ok(unknown.reply.includes('I answer fixed questions with code'));
const builtIn = await ask('Are the built-in agents on?');
assert.deepEqual(builtIn.calls, []);
assert.ok(builtIn.reply.includes(BUILT_IN_OFF));
const noSlot = await ask('Which cases lack proof of delivery?', { state: { selectedPageId: 'readiness', pages: [{ id: 'readiness', widgets: {}, widgetLayout: {} }] } });
assert.deepEqual(noSlot.calls.map((call) => call.name), ['addWidget', 'configureWidget', 'addWidgetFilter'], 'nothing to remove when the slot is gone');
assert.deepEqual(noSlot.technical[0].map((step) => step.tool), ['add_widget', 'configure_widget', 'add_widget_filter'], 'technical steps follow the calls');
assert.ok(noSlot.reply.includes('How I built this: 1. Added a table under the headline tiles of the Evidence readiness page. 2. Showed 5 columns from cases.'), 'plain steps renumber without the remove step');
// (r31 J1 J4) The dashboard: tool names only under the collapsed "Technical steps" in the drawer; no "Changes stay in
// this tab" chip (the drawer's "Edit mode:" line keeps that information).
const dashMain = read('frontend/src/dashboard/main.jsx');
assert.ok(dashMain.includes('const onAnswer = (page, technical, { textOnly = false } = {}) => {') && dashMain.includes('if (technical) setTechnical(technical);'), 'the dashboard keeps the tool steps of the last answer');
assert.ok(dashMain.includes('{technical && <details className="pg-technical" data-testid="dashboard-technical-steps">\n            <summary>Technical steps</summary>'), 'collapsed Technical steps');
assert.equal(/<details className="pg-technical"[^>]*\sopen/u.test(dashMain), false, 'Technical steps collapsed by default');
const drawerBody = dashMain.slice(dashMain.indexOf('<div className="pg-drawer-body">'), dashMain.indexOf('</details>\n      <main'));
assert.ok(drawerBody.includes('data-testid="dashboard-technical-steps"'), 'Technical steps sit inside the collapsed drawer');
assert.ok(drawerBody.includes('<strong>Edit mode:</strong> the auditor and layout changes stay in this tab and are not saved.'), 'the tab-only information is kept in the drawer');
assert.equal(dashMain.includes('Changes stay in this tab</li>'), false, 'no tab chip on camera');
// (r32 J3 P3) After an answer, the slot holds the auditor's grid, and the step says the previous answer went.
const afterAnswer = structuredClone(stateWithSlot);
afterAnswer.pages.find((page) => page.id === 'readiness').widgets[ANSWER_SLOTS.readiness].format.title.text = 'Evidence auditor · Cases due within 3 days';
const second = await ask('Which cases lack proof of delivery?', { state: afterAnswer });
assert.ok(second.reply.includes('How I built this: 1. Removed the previous answer. 2. Added a table'), 'second answer: removed the previous answer');
assert.equal(second.technical[0][0].detail, 'the previous answer');
// (r32 J3 P2) A case selection on the page (cross filter from a click, or Filter by case) would narrow the answer
// grid, so "3 of 3" would sit next to 1 row. The auditor clears it first and says so; the grid then shows exactly
// the rows of the reply. Without the clear hook the reply names the selection instead.
const selectedState = structuredClone(stateWithSlot);
const readinessPage = selectedState.pages.find((page) => page.id === 'readiness');
readinessPage.crossFilter = { values: { checklist: [{ type: 'value', group: 0, field: { id: 'cases.case_ref' }, values: ['case-ref-002'] }],
  [ANSWER_SLOTS.readiness]: [{ type: 'value', group: 0, field: { id: 'cases.case_ref' }, values: ['case-ref-001'] }] } };
readinessPage.filter = { ...(readinessPage.filter || {}), page: [...(readinessPage.filter?.page || []).map((entry) => ({ ...entry, model: undefined })),
  { field: { id: 'cases.reason' }, filterWidgetId: 'stand-in', model: { operator: 'equals', value: 'Item not received' } }] };
assert.deepEqual(pageSelections(selectedState, 'readiness'), ['case ref = case-ref-002', 'reason = Item not received'],
  "the answer grid's own selection is not counted; page filters with a value are");
assert.deepEqual(pageSelections(selectedState, 'guide'), [], 'a selection on one page does not touch the other');
assert.deepEqual(pageSelections(stateWithSlot, 'readiness'), [], 'the initial dashboard has no selection');
{
  const cleared = [];
  const { studio, calls } = standInStudio();
  const live = { state: selectedState };
  const agent = createEvidenceAuditor({ studio, getState: () => live.state, data: tables,
    clearSelections: (pageId) => { cleared.push(pageId); live.state = structuredClone(stateWithSlot); } });
  const events = [];
  for await (const event of agent.run({ threadId: 't9', runId: 'r9', messages: [{ id: 'u9', role: 'user', content: 'Which are due within 3 days?' }], tools: [], state: null, context: [], forwardedProps: {} })) events.push(event);
  const reply = events.filter((event) => event.type === 'TEXT_MESSAGE_CONTENT').map((event) => event.delta).join('');
  assert.deepEqual(cleared, ['readiness'], 'the selection on the answer page is cleared once, before the Studio calls');
  assert.deepEqual(calls.map((call) => call.tool), ['remove_widget', 'add_widget', 'configure_widget', 'add_widget_filter'], 'clearing is not a Studio tool call');
  const due = tables.cases.filter((row) => row.days_to_due <= 3);
  assert.ok(reply.startsWith(`${due.length} of ${tables.cases.length} synthetic case`), 'the count is over every case');
  assert.ok(reply.includes("How I built this: 1. Cleared the page's own selection (case ref = case-ref-002; reason = Item not received) so the table shows every matching row. 2. Replaced the page's Cases table with the answer."),
    'the reply says the selection was cleared');
  assert.equal(/_[a-z]/u.test(reply.slice(reply.indexOf('How I built this'), reply.indexOf(' 2. '))), false, 'plain step: no field id');
  assert.equal(tables.cases.filter((row) => applyFilter(calls[3].args.value, row)).length, due.length, 'with no selection left, the grid rows equal the count in the reply');
  assert.equal(events.filter((event) => event.type === 'TOOL_CALL_START').length, 4);
}
{
  const noHook = await ask('Which are due within 3 days?', { state: selectedState });
  assert.ok(noHook.reply.includes('The page also has its own selection (case ref = case-ref-002; reason = Item not received), so the table shows only the matching rows inside it.'),
    'without the clear hook the reply names the selection');
  assert.equal(noHook.reply.includes('Cleared the page'), false);
}
const dashMainR32 = read('frontend/src/dashboard/main.jsx');
assert.ok(dashMainR32.includes('clearSelections: (pageId) => clearPageSelections(api, pageId),'), 'the dashboard gives the auditor the clear hook');
assert.ok(/function clearPageSelections\(api, pageId\) \{[\s\S]*?crossFilter: undefined,[\s\S]*?page\.filter\.page\?\.map\(\(\{ model, \.\.\.rest \}\) => rest\)/u.test(dashMainR32),
  'the hook clears the cross filter and the page filter values of that page');
const cleared = await ask('clear the answers');
assert.deepEqual(cleared.calls.map((call) => `${call.tool}:${call.args.widgetId}`), ['remove_widget:auditor-answer', 'remove_widget:auditor-answer-guide']);
const failed = await ask('Which are due within 3 days?', { failOn: 'addWidgetFilter' });
assert.equal(failed.events.at(-1).type, 'RUN_ERROR', 'a failing tool ends the run with an error');
assert.ok(read('frontend/src/dashboard/layout.js').includes(`Recorded guide benchmark, ${benchmark.cases} cases`), 'benchmark subtitle quotes the case count from the file');

// 7. Render in headless Chromium (optional)
let render = 'SKIP (playwright is not available)';
let chromium;
try { ({ chromium } = createRequire(import.meta.url)('playwright')); } catch { chromium = null; }
if (chromium && existsSync(join(frontendRoot, 'node_modules', '.bin', 'vite'))) {
  const outDir = mkdtempSync(join(tmpdir(), 'payguard-dashboard-'));
  const built = spawnSync(join(frontendRoot, 'node_modules', '.bin', 'vite'), ['build', '--outDir', outDir, '--emptyOutDir', '--logLevel', 'error'],
    { cwd: frontendRoot, encoding: 'utf8', env: { ...process.env, VITE_AG_STUDIO_LICENSE: '' } });
  assert.equal(built.status, 0, built.stderr || built.stdout);
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json', '.png': 'image/png' };
  const server = createServer((request, response) => {
    const path = normalize(join(outDir, decodeURIComponent(new URL(request.url, 'http://x').pathname)));
    if (!path.startsWith(outDir + sep) || !existsSync(path)) { response.writeHead(404); response.end(); return; }
    response.writeHead(200, { 'content-type': types[extname(path)] || 'application/octet-stream' });
    response.end(readFileSync(path));
  });
  await new Promise((done) => server.listen(0, '127.0.0.1', done));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
    const hosts = new Set();
    const errors = [];
    page.on('request', (request) => hosts.add(new URL(request.url()).origin));
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(`${origin}/dashboard.html`);
    await page.waitForFunction(() => document.querySelector('[data-testid=widget-deadline]')?.textContent.includes('case-ref-002')
      && document.querySelector('[data-testid=widget-checklist]')?.textContent.includes('case-ref-002'), null, { timeout: 30000 });
    assert.match(await page.getByTestId('widget-deadline').innerText(), /case-ref-001[\s\S]*case-ref-002/u);
    assert.match(await page.getByTestId('widget-checklist').innerText(), /No accepted delivery attachment/u);
    await page.getByTestId('checklist-case-case-ref-001').click();
    await page.waitForFunction(() => !document.querySelector('[data-testid=widget-deadline]')?.textContent.includes('case-ref-002'), null, { timeout: 15000 });
    await page.getByTestId('checklist-case-case-ref-001').click();
    // Studio's own button filter widget narrows the custom widgets too (class name of the pinned 3.0.0 widget).
    const caseButton = page.locator('.ag-studio-button-filter-widget-item', { hasText: /^case-ref-002$/u });
    await caseButton.click();
    await page.waitForFunction(() => !document.querySelector('[data-testid=widget-deadline]')?.textContent.includes('case-ref-001'), null, { timeout: 15000 });
    await caseButton.click();
    await page.getByTestId('dashboard-mode').click();
    await page.locator('button', { hasText: 'Which cases lack proof of delivery?' }).last().click();
    await page.getByText('Evidence auditor · Cases with no delivery attachment on file').first().waitFor({ timeout: 15000 });
    await page.getByText(/1 of 3 synthetic cases: case-ref-002/u).first().waitFor({ timeout: 15000 });
    if (process.env.PAYGUARD_RENDER_SCREENSHOT) await page.screenshot({ path: process.env.PAYGUARD_RENDER_SCREENSHOT });
    assert.deepEqual([...hosts], [origin], 'the dashboard requests nothing but its own origin');
    assert.deepEqual(errors, []);
    render = 'PASS';
  } finally {
    await browser.close();
    server.close();
    rmSync(outDir, { recursive: true, force: true });
  }
}

console.log(JSON.stringify({
  status: 'PASS',
  sources: data.sources.map((source) => `${source.id}:${source.data.length}`),
  auditor_questions: QUESTIONS.length,
  studio_calls_per_question: Object.fromEntries(Object.entries(studioCalls).map(([question, calls]) => [question, calls.join(' ')])),
  custom_widgets: [DEADLINE_WIDGET, CHECKLIST_WIDGET],
  render,
}));
