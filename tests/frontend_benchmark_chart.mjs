// Benchmark charts: every number shown comes from docs/evidence/guide_benchmark_v1.json, and the claims hold.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { callRows, callSaving, headroom, historyRows, roundRows, wrongValuesTotal } from '../frontend/src/charts/benchmarkChartData.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const chartData = JSON.parse(readFileSync(resolve(root, 'frontend/src/data/guide_benchmark_v1.json'), 'utf8'));
const evidence = JSON.parse(readFileSync(resolve(root, 'docs/evidence/guide_benchmark_v1.json'), 'utf8'));
const total = (flow, key) => Object.values(evidence.flows[flow]).reduce((sum, row) => sum + row.honest[key], 0);
const careless = (flow) => Object.values(evidence.flows[flow]).reduce((sum, row) => sum + row.careless_wrong_filled, 0);

assert.equal(chartData.cases, total('echo_only', 'cases'));
assert.equal(chartData.form_only_rounds, total('echo_only', 'form_only_rounds'));
for (const flow of ['echo_only', 'hybrid', 'hybrid_one_save']) {
  const row = chartData.flows.find((entry) => entry.id === flow);
  assert.equal(row.model_calls, total(flow, 'model_calls'), flow);
  assert.equal(row.rounds, total(flow, 'rounds'), flow);
  assert.equal(row.wrong_honest, total(flow, 'wrong_filled'), flow);
  assert.equal(row.wrong_careless, careless(flow), flow);
}
assert.equal(chartData.flows[0].model_calls, chartData.cases, 'every sentence to the AI = one call per case');
assert.equal(wrongValuesTotal(chartData), 0, 'no wrong value may reach the form');
const saving = callSaving(chartData);
assert.ok(saving.current < saving.all && saving.percent > 0);
assert.equal(callRows(chartData).length, 4);
assert.equal(roundRows(chartData)[0].label, 'Plain form');
assert.ok(headroom(roundRows(chartData).map((row) => row.rounds)) > Math.max(...roundRows(chartData).map((row) => row.rounds)));
assert.equal(historyRows(chartData).at(-1).rounds,
  evidence.flows.hybrid_one_save.evidence_guide_keyword_blind_v4.honest.rounds, 'last history step equals the current blind v4 result');
// The charts live on a separate evidence page for reviewers, never in the seller console.
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const page = readFileSync(resolve(root, 'frontend/src/evidence.jsx'), 'utf8');
assert.ok(!app.includes('BenchmarkCharts'), 'the seller console does not show the benchmark');
assert.ok(page.includes('BenchmarkCharts'), 'the evidence page shows it');
console.log(JSON.stringify({ status: 'PASS', calls: `${saving.all}->${saving.current}`, saving_percent: saving.percent, wrong_values: 0 }));
