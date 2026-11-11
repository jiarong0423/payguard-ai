import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { buildMonthlyHistory, buildVelocityHourlyRows, monthlyChartOptions, velocityChartOptions } from '../frontend/src/charts/velocityChartData.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(projectRoot, path), 'utf8');

// 1. Dependency pin: AG Charts Community at the exact version AG Grid 36.2 is built against.
const packageJson = JSON.parse(read('frontend/package.json'));
const lock = JSON.parse(read('frontend/package-lock.json'));
assert.equal(packageJson.dependencies['ag-charts-community'], '14.2.0', 'ag-charts-community pinned exactly');
assert.equal(packageJson.dependencies['ag-grid-community'], '36.2.0');
assert.equal(lock.packages[''].dependencies['ag-charts-community'], '14.2.0', 'lockfile root lists ag-charts-community');
assert.equal(lock.packages['node_modules/ag-charts-community'].version, '14.2.0');
assert.equal(
  lock.packages['node_modules/ag-grid-community'].dependencies['ag-charts-types'],
  lock.packages['node_modules/ag-charts-community'].dependencies['ag-charts-types'],
  'AG Grid and AG Charts share one ag-charts-types version',
);
// Round 4 added AG Studio (commercial) for the separate /dashboard.html entry only. The seller console and
// the evidence page stay Community: no enterprise package is a direct dependency, the enterprise packages
// in the lockfile are there only because ag-studio needs them, and no source outside src/dashboard imports
// AG Studio or an enterprise package.
const COMMERCIAL_DIRECT = new Set(['ag-studio', 'ag-studio-react']);
for (const name of Object.keys({ ...packageJson.dependencies, ...packageJson.devDependencies })) {
  assert.equal(/enterprise/u.test(name), false, `no direct enterprise dependency: ${name}`);
}
const studioDeps = new Set([
  ...Object.keys(lock.packages['node_modules/ag-studio']?.dependencies || {}),
  ...Object.keys(lock.packages['node_modules/ag-studio-react']?.dependencies || {}),
]);
for (const [key, entry] of Object.entries(lock.packages)) {
  const name = key.replace(/^node_modules\//u, '');
  if (/enterprise/u.test(key)) assert.ok(studioDeps.has(name), `enterprise package only as an ag-studio dependency: ${key}`);
  if (key && entry.license === 'Commercial') assert.ok(COMMERCIAL_DIRECT.has(name) || studioDeps.has(name), `commercial package only for AG Studio: ${key}`);
}
function sourceFiles(dir) {
  return readdirSync(resolve(projectRoot, dir), { withFileTypes: true }).flatMap((entry) => (entry.isDirectory()
    ? sourceFiles(`${dir}/${entry.name}`) : /\.(jsx?|mjs)$/u.test(entry.name) ? [`${dir}/${entry.name}`] : []));
}
for (const file of sourceFiles('frontend/src').filter((path) => !path.startsWith('frontend/src/dashboard/'))) {
  assert.equal(/from\s+['"](ag-studio|ag-studio-react|ag-grid-enterprise|ag-charts-enterprise)['"]/u.test(read(file)), false, `${file} must not import AG Studio or an enterprise package`);
}

// 2. Source contract: lazy chart, one mount above the grid, Community features only, no network.
const appSource = read('frontend/src/App.jsx');
const chartSource = read('frontend/src/charts/VelocityChart.jsx');
const chartDataSource = read('frontend/src/charts/velocityChartData.js');
const timeSource = read('frontend/src/TimeEvidenceView.jsx');
const replaySource = read('frontend/src/GuideReplay.jsx');

assert.equal((appSource.match(/charts\/VelocityChart/gu) || []).length, 1, 'App.jsx references the chart module once');
// Built from parts so the export import-integrity scan does not read this expected text as an import of the test file.
const lazyChartLine = 'const VelocityChart = lazy(() => ' + 'import(' + "'./charts/VelocityChart.jsx'));";
assert.ok(appSource.includes(lazyChartLine), 'chart is lazy-loaded');
assert.equal(/import\s+VelocityChart\s+from/u.test(appSource), false, 'chart is never imported statically');
assert.equal((appSource.match(/<VelocityChart /gu) || []).length, 1, 'chart mounted once');
assert.ok(appSource.indexOf('<VelocityChart ') < appSource.indexOf('data-testid="velocity-grid"'), 'chart sits above the transaction grid');
// (optimise r24) Phones get the last hours before the spike (phoneChartVelocity trims the baseline window only).
assert.ok(appSource.includes('<VelocityChart velocity={chartVelocity} transactions={state?.transactions} compact={narrowScreen} />'), 'chart reads existing state only (compact = phone legend swap)');
assert.ok(appSource.includes('const chartVelocity = useMemo(() => phoneChartVelocity(velocity, narrowScreen), [velocity, narrowScreen]);'), 'chart velocity derives from state');
assert.ok(appSource.includes('const SPIKE_PHONE_BASELINE_HOURS = 10;'), 'phone window is about 11 bars');
for (const module of ['CartesianChartModule', 'BarSeriesModule', 'LineSeriesModule', 'CategoryAxisModule', 'NumberAxisModule', 'CrossLinesModule', 'LegendModule']) {
  assert.ok(chartSource.includes(module), `chart registers ${module}`);
}
assert.ok(chartSource.includes("from 'ag-charts-community'"));
assert.ok(chartSource.includes('chartRef.current?.destroy()'), 'chart is destroyed on unmount');
assert.ok(chartSource.includes('data-testid="velocity-chart"'));

const sourcesUnderTest = { chartSource, chartDataSource, timeSource, replaySource };
for (const [name, source] of Object.entries(sourcesUnderTest)) {
  for (const forbidden of ['fetch(', 'XMLHttpRequest', 'WebSocket', 'http://', 'https://', 'enterprise', 'LicenseManager']) {
    assert.equal(source.includes(forbidden), false, `${name} must not contain ${forbidden}`);
  }
}
for (const file of readdirSync(resolve(projectRoot, 'frontend/src/charts'))) {
  const source = read(`frontend/src/charts/${file}`);
  assert.equal(/fetch\(|XMLHttpRequest|https?:\/\//u.test(source), false, `charts/${file} makes no network call`);
}

// Time evidence grid keeps the old test id and timeline, and adds an AG Grid view with renderers.
assert.ok(timeSource.includes('data-testid="time-evidence"'), 'existing time-evidence test id kept');
assert.ok(timeSource.includes('<ol className="time-events">'), 'timeline list still available');
assert.ok(timeSource.includes('data-testid="time-evidence-grid"'));
assert.ok(timeSource.includes('<AgGridReact'));
for (const renderer of ['cellRenderer: EventCell', 'cellRenderer: TimeCell', 'cellRenderer: SourceCell', 'cellRenderer: GapCell']) {
  assert.ok(timeSource.includes(renderer), `time grid uses ${renderer}`);
}
for (const header of ["headerName: 'Event'", "headerName: 'Timestamp'", "headerName: 'Source'", "headerName: 'Gap to previous'"]) {
  assert.ok(timeSource.includes(header), `time grid column ${header}`);
}

// Gap table: named export for reuse, column filters, quick filter, CSV export of the current step.
assert.ok(replaySource.includes('export function GapGrid('), 'GapGrid is a named export');
assert.ok(replaySource.includes('<GapGrid items={step.items} testIdPrefix="replay"'), 'replay keeps replay-* test ids');
assert.ok(replaySource.includes('data-testid={`${testIdPrefix}-grid`}'), 'replay-grid test id preserved via prefix');
assert.equal((replaySource.match(/filter: 'agTextColumnFilter', floatingFilter: true/gu) || []).length, 3, 'three filtered columns');
assert.ok(replaySource.includes('quickFilterText={quickFilter}'));
assert.ok(replaySource.includes('exportDataAsCsv('));
assert.ok(replaySource.includes("exportedRows: 'all'"));
assert.ok(replaySource.includes('csvFileName={`tradeglot-replay-${scenario.id}-step-${stepIndex + 1}.csv`}'), 'CSV is per step');

// Replay layout: the raw model reply and template sit in a closed disclosure; C6 imports keep working.
const replayCss = read('frontend/src/GuideReplay.css');
for (const name of ['export const gapGridTheme', 'export function StatusChip', 'export function SourceChip']) {
  assert.ok(replaySource.includes(name), `C6 import kept: ${name}`);
}
assert.ok(replaySource.includes('<span className="guide-replay-tag">What the AI returned</span>'));
assert.equal(replaySource.includes('<span className="guide-replay-tag">Model</span>'), false, 'old Model tag removed');
const disclosure = replaySource.match(/<details className="guide-replay-details"[^>]*>[\s\S]*?<\/details>/u);
assert.ok(disclosure, 'reply disclosure exists');
assert.equal(/<details[^>]*\bopen\b/u.test(disclosure[0]), false, 'disclosure starts closed');
assert.ok(disclosure[0].includes("<summary>Show the model's closed reply</summary>"));
assert.ok(disclosure[0].includes('data-testid="replay-reply"'), 'replay-reply stays on the pre inside the disclosure');
assert.ok(disclosure[0].includes('Template: {step.template}'), 'template line inside the disclosure');
assert.equal((replaySource.match(/Template: \{step\.template\}/gu) || []).length, 1, 'template shown once');
assert.ok(/\.guide-replay-list button \{[^}]*min-height: 44px/u.test(replayCss), 'list buttons are 44px touch targets');
assert.ok(/\.guide-replay-note \{[^}]*font-size: 14px/u.test(replayCss));
assert.ok(/\.gap-chip \{[^}]*font-size: 14px/u.test(replayCss));

// 3. Chart data on a hand-built velocity block: boundaries, currency, threshold line.
const handVelocity = {
  status: 'review_velocity', window_start: '2026-10-08T07:00:00Z', window_end: '2026-10-08T08:00:00Z', window_hours: 1,
  currency: 'USD', total_amount: '30.00', baseline_amount_per_hour: '100.00', baseline_provenance: 'SYNTHETIC_BASELINE',
  baseline_window_start: '2026-10-07T07:00:00Z', baseline_window_end: '2026-10-08T07:00:00Z', threshold: '3.5',
};
const handRows = buildVelocityHourlyRows(handVelocity, [
  { order_id: 'a', amount: '10.00', currency: 'USD', occurred_at: '2026-10-08T07:00:00Z' }, // left-open boundary: excluded
  { order_id: 'b', amount: '12.50', currency: 'USD', occurred_at: '2026-10-08T07:30:00Z' },
  { order_id: 'c', amount: '17.50', currency: 'USD', occurred_at: '2026-10-08T08:00:00Z' }, // right-closed boundary: included
  { order_id: 'd', amount: '99.00', currency: 'EUR', occurred_at: '2026-10-08T07:45:00Z' }, // other currency: excluded
  { order_id: 'e', amount: '5.00', currency: 'USD', occurred_at: '2026-10-08T08:00:01Z' }, // future: excluded
]);
assert.equal(handRows.rows.length, 25, '24 baseline hours + 1 spike hour');
assert.deepEqual(handRows.rows.slice(0, 24).map((row) => row.baseline), new Array(24).fill(100));
assert.ok(handRows.rows.slice(0, 24).every((row) => row.window === 'baseline' && row.spike === null));
assert.equal(handRows.rows[0].label, '07:00');
const handSpike = handRows.rows[24];
assert.equal(handSpike.window, 'spike');
assert.equal(handSpike.spike, 30);
assert.equal(handSpike.captures, 2);
assert.equal(handRows.reviewLine, 350);
assert.deepEqual(buildVelocityHourlyRows(null, []), { rows: [], reviewLine: null, currency: 'USD' });

// Monthly view: twelve nodes ending in the spike's month, a 3-month average from the third node, month-over-month change.
const monthly = buildMonthlyHistory(handVelocity);
assert.equal(monthly.rows.length, 12);
assert.equal(monthly.rows[11].key, '2026-10');
assert.equal(monthly.rows[11].current, true);
assert.deepEqual([monthly.rows[0].ma3, monthly.rows[1].ma3], [null, null]);
assert.equal(monthly.rows[2].ma3, Math.round(((monthly.rows[0].amount + monthly.rows[1].amount + monthly.rows[2].amount) / 3) * 100) / 100);
assert.equal(monthly.rows[0].change, null);
assert.equal(monthly.rows[5].change, Math.round(((monthly.rows[5].amount - monthly.rows[4].amount) / monthly.rows[4].amount) * 1000) / 10);
assert.deepEqual(buildMonthlyHistory(null), { rows: [], currency: 'USD' });
assert.deepEqual(buildMonthlyHistory({ ...handVelocity, baseline_amount_per_hour: '0' }), { rows: [], currency: 'USD' }, 'zero baseline: no NaN or Infinity');
const monthlyOptions = monthlyChartOptions(monthly, null);
// AG Charts 14.2 has no legend.item.paddingX: it logged "Unknown option" on every load (attack r21).
assert.equal('paddingX' in (monthlyOptions.legend?.item || {}), false, 'no legend.item.paddingX');
assert.deepEqual(monthlyOptions.legend.item.padding, { left: 5, right: 5 });
assert.deepEqual(monthlyOptions.series.map((series) => [series.type, series.yKey]), [['line', 'amount'], ['line', 'ma3']]);
assert.ok(monthlyOptions.subtitle.text.includes('not used by the review signal'), 'monthly view says it is illustrative');
assert.notEqual(monthlyOptions.series[1].stroke, velocityChartOptions(handRows, null).axes.y.crossLines[0].stroke, 'average line never reuses the review-threshold colour');
assert.equal(monthlyOptions.axes.y.min, 0, 'monthly axis starts at zero');

const options = velocityChartOptions(handRows, null);
// (P4 2026-11-12, review_FULL s3a) Every past hour is a thin bar at the usual rate (was one flat dashed line).
assert.deepEqual(options.series.map((series) => [series.type, series.yKey]), [['bar', 'baseline'], ['bar', 'spike']]);
assert.equal(options.legend.enabled, true, 'desktop keeps the chart legend');
assert.equal(velocityChartOptions(handRows, null, { compact: true }).legend.enabled, false, 'phones hide the paging chart legend (the page lists it once)');
assert.equal(options.series[1].label.formatter({ value: 300 }), '×3.0', 'spike bar shows its multiple of the baseline');
assert.equal(options.axes.x.type, 'category');
assert.equal(options.axes.y.type, 'number');
assert.equal(options.axes.y.crossLines[0].value, 350);
const tip = options.series[1].tooltip.renderer({ datum: handSpike });
assert.equal(tip.heading, 'Spike window');
assert.deepEqual(tip.data, [{ label: 'Captured amount', value: '30.00 USD' }, { label: 'Orders', value: '2' }]);

// 4. Parity with the real backend: the spike bars add up to the backend's window total.
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');
const pythonProgram = String.raw`
import json
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import create_app
from app.store import SessionStore

now = datetime(2026, 10, 8, 8, 0, tzinfo=timezone.utc)
store = SessionStore(clock=lambda: now)
application = create_app(store=store)
with TestClient(application, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55002)) as client:
    origin = "http://localhost:5173"
    session = client.post("/api/v1/demo/sessions", json={}, headers={"Origin": origin}).json()
    headers = {"Origin": origin, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
    empty = client.get("/api/v1/demo/state", headers=headers)
    burst = client.post("/api/v1/demo/inject", json={"scenario": "burst"}, headers=headers)
    assert empty.status_code == 200, empty.text
    assert burst.status_code == 200, burst.text
    print(json.dumps({"empty": empty.json(), "burst": burst.json()}, separators=(",", ":")))
`;
const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${resolve(projectRoot, 'src')}:${resolve(projectRoot, 'backend')}` },
  encoding: 'utf8',
  maxBuffer: 4 * 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const { empty, burst } = JSON.parse(generated.stdout.trim());

const sumSpike = (model) => model.rows.filter((row) => row.window === 'spike').reduce((sum, row) => sum + Math.round(row.spike * 100), 0);
const emptyModel = buildVelocityHourlyRows(empty.velocity, empty.transactions);
assert.equal(sumSpike(emptyModel), 0, 'no captures before the burst');
assert.equal(emptyModel.rows.filter((row) => row.window === 'baseline').length, 24);

const burstModel = buildVelocityHourlyRows(burst.velocity, burst.transactions);
assert.equal(burst.velocity.status, 'review_velocity');
assert.equal(sumSpike(burstModel), Math.round(Number(burst.velocity.total_amount) * 100), 'spike bars equal backend window total');
assert.equal(burstModel.rows.filter((row) => row.window === 'spike').reduce((sum, row) => sum + row.captures, 0), burst.velocity.transaction_count);
assert.equal(burstModel.rows.filter((row) => row.window === 'baseline')[0].baseline, Number(burst.velocity.baseline_amount_per_hour));
assert.equal(burstModel.reviewLine, Number(burst.velocity.baseline_amount_per_hour) * Number(burst.velocity.threshold));
assert.equal(burstModel.rows[0].start, new Date(burst.velocity.baseline_window_start).toISOString());

console.log(JSON.stringify({
  status: 'PASS',
  ag_charts_community: packageJson.dependencies['ag-charts-community'],
  chart_rows: burstModel.rows.length,
  spike_total: burst.velocity.total_amount,
  spike_captures: burst.velocity.transaction_count,
  review_line: burstModel.reviewLine,
}));
