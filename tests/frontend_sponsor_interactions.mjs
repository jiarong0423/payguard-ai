// Sponsor-tool interactions (2026-11-09): each sponsor view gets a one-click highlight and quick-classify chips that use the
// tool's own feature, with live counts, Reset and aria-pressed. No network, no personal data. Source-level and pure-function
// checks; the chips were also exercised in a browser against the built console.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(root, path), 'utf8');

// AG Grid (orders): amount bands as the grid's own number filter, a row highlight through getRowClass.
const grid = read('frontend/src/AnalyticsDashboard.jsx');
assert.ok(grid.includes('setFilterModel') && grid.includes('getRowClass=') && grid.includes("filter: 'agNumberColumnFilter'"), 'AG Grid: number filter model and getRowClass');
for (const id of ['analytics-band-', 'analytics-highlight-large', 'analytics-grid-reset']) assert.ok(grid.includes(id), id);
assert.ok(grid.includes('aria-pressed={band === entry.id}') && grid.includes('aria-pressed={highlight}'), 'AG Grid chips expose aria-pressed');
assert.ok(grid.includes('They are not a risk score'), 'the bands say they are not a risk score');
const amounts = ['4.50', '12.00', '7.25', '18.00', '9.75', '6.50', '15.00', '11.25', '8.00', '7.75'];
const bands = { low: (n) => n < 8, mid: (n) => n >= 8 && n < 12, high: (n) => n >= 12 };
const counts = Object.fromEntries(Object.entries(bands).map(([key, test]) => [key, amounts.filter((value) => test(Number(value))).length * 5]));
assert.deepEqual(counts, { low: 20, mid: 15, high: 15 }, 'the 50 synthetic orders split 20 / 15 / 15');

// AG Charts (hourly chart): outline the peak hour or the hours above the review line, with counts and Reset.
const chartData = await import('../frontend/src/charts/velocityChartData.js');
const rows = [
  { key: 'b', window: 'baseline', baseline: 100, spike: null },
  { key: 's1', window: 'spike', spike: 120, label: '10:00' }, { key: 's2', window: 'spike', spike: 500, label: '11:00' }, { key: 's3', window: 'spike', spike: 80, label: '12:00' },
];
assert.equal(chartData.peakHourOf(rows).key, 's2', 'peak hour is the largest spike hour');
assert.equal(chartData.peakHourOf([]), null);
assert.deepEqual(chartData.hoursAbove(rows, 350).map((row) => row.key), ['s2']);
assert.deepEqual(chartData.hoursAbove(rows, null), []);
const options = (mark) => chartData.velocityChartOptions({ rows, reviewLine: 350, currency: 'USD' }, null, { mark });
const styler = (mark, key) => options(mark).series[1].itemStyler({ datum: rows.find((row) => row.key === key) });
assert.equal(styler('peak', 's2').strokeWidth, 3, 'the peak bar is outlined');
assert.equal(styler('peak', 's1').fillOpacity, 0.3, 'other bars are softened');
assert.equal(styler('over', 's2').strokeWidth, 3);
assert.equal(styler('', 's1').fillOpacity, undefined, 'no mark, no change');
const chart = read('frontend/src/charts/VelocityChart.jsx');
for (const id of ['velocity-mark-peak', 'velocity-mark-over', 'velocity-mark-reset']) assert.ok(chart.includes(id), id);
assert.ok(chart.includes("aria-pressed={mark === 'peak'}") && chart.includes('aria-live="polite" data-testid="velocity-mark-note"'), 'chart chips: aria-pressed and a live note');

// Bryntum (deadline board): urgency chips and a glow on tight deadlines through the events' own styling.
const board = await import('../frontend/src/board/boardData.js');
const caseRows = [{ status: 'DUE_SOON_NO_DRAFT' }, { status: 'PAST_DUE' }, { status: 'OPEN' }, { status: 'DUE_SOON' }];
assert.deepEqual(board.urgencyCounts(caseRows), { all: 4, tight: 3, open: 1 });
assert.equal(board.barClasses(caseRows[0], { glow: true }), 'payguard-board-glow');
assert.equal(board.barClasses(caseRows[2], { glow: true }), '');
assert.equal(board.barClasses(caseRows[2], { focus: 'tight' }), 'payguard-board-dim');
assert.equal(board.barClasses(caseRows[0], { focus: 'open', glow: true }), 'payguard-board-glow payguard-board-dim');
assert.equal(board.barClasses(caseRows[0], {}), '');
const boardSrc = read('frontend/src/board/EvidenceBoard.jsx');
for (const id of ['evidence-board-urgency-', 'evidence-board-glow', 'evidence-board-urgency-reset']) assert.ok(boardSrc.includes(id), id);
assert.ok(boardSrc.includes('aria-pressed={focus === key}') && boardSrc.includes('aria-pressed={glow}'), 'board chips expose aria-pressed');

// Sponsor map: the text is the SPONSOR_TECH_MAP.md text, and each link goes to the proof filter or to where it runs.
const { SPONSOR_MAP, sponsorHref } = await import('../frontend/src/sponsorMap.js');
const techMap = read('docs/SPONSOR_TECH_MAP.md');
const { PROOF_SPONSORS } = await import('../frontend/src/proof/proofData.js');
for (const entry of SPONSOR_MAP) {
  assert.ok(techMap.includes(entry.what), `${entry.name}: text is copied from docs/SPONSOR_TECH_MAP.md`);
  if (entry.proof) { assert.ok(PROOF_SPONSORS.includes(entry.proof), entry.name); assert.ok(sponsorHref(entry).startsWith('/proof.html#sponsor='), entry.name); }
  else assert.ok(entry.href.startsWith('/'), entry.name);
}
// (fix r1 F7) Bryntum has no proof row, so its link goes to the deadline board; a tool with proof rows keeps the filter link.
assert.equal(sponsorHref(SPONSOR_MAP.find((entry) => entry.name === 'Bryntum')), '/#evidence-board');
assert.equal(sponsorHref(SPONSOR_MAP.find((entry) => entry.name === 'PayPal')), '/proof.html#sponsor=PayPal');
assert.ok(read('frontend/src/App.jsx').includes('data-testid="sponsor-map"'), 'the footer has the Sponsor map');

// Hosted dashboard: one-click replay of the four recorded runs, a visible step list, the recorded badge. Nothing is called.
const { replaySchedule, REPLAY_BADGE, validateRecording } = await import('../frontend/src/dashboard/agentRecording.js');
const recording = validateRecording(JSON.parse(read('frontend/src/data/studio_agent_run_v1.json')));
assert.equal(recording.runs.length, 4);
const schedule = replaySchedule(recording.runs[1]);
assert.ok(schedule.length >= 3 && schedule.every((step, index) => index === 0 || step.at > schedule[index - 1].at), 'steps appear in order');
assert.deepEqual(schedule.map((step) => step.tool).slice(0, 3), ['view_schema', 'execute_query', 'complete_task']);
assert.equal(REPLAY_BADGE, 'Recorded live run, no model call');
const replaySrc = read('frontend/src/dashboard/RecordedRuns.jsx');
assert.ok(replaySrc.includes('data-testid={`replay-run-${index}`}') && replaySrc.includes('aria-live="polite" data-testid="replay-output"'), 'replay buttons and a live output');
assert.ok(!/fetch\(|XMLHttpRequest|apiRequest/u.test(replaySrc), 'replay makes no request');
for (const file of ['frontend/src/AnalyticsDashboard.jsx', 'frontend/src/charts/VelocityChart.jsx', 'frontend/src/board/EvidenceBoard.jsx']) {
  const text = read(file);
  assert.ok(!/localStorage|fetch\(/u.test(text.slice(text.indexOf('export default'))) || file.endsWith('EvidenceBoard.jsx'), `${file}: no new network call`);
}
console.log('frontend_sponsor_interactions: ok');
