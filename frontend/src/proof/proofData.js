// Public proof page data (optimise r24). Pure functions over the committed JSON only: frontend/src/data/proof_facts_v1.json
// (facts copied from the evidence files, with their source named per row) and frontend/src/data/channel3_receipts_v1.json
// (copy of docs/evidence/channel3_receipts_v1.json). No fetch, no API, no Bryntum; runs in plain Node for the contract test.

export const PROOF_SCHEMA = 'payguard.proof_facts.v1';
export const METHOD_ORDER = ['REAL_SANDBOX', 'RECORDED', 'TEST', 'SYNTHETIC'];

// Numbers the Channel3 row states, recomputed from the receipts.
export function channel3Summary(receipts) {
  const rows = Array.isArray(receipts?.receipts) ? receipts.receipts : [];
  const latencies = rows.map((row) => Number(row.latency_seconds)).filter(Number.isFinite);
  return {
    count: rows.length,
    allOk: rows.length > 0 && rows.every((row) => row.http_status === 200 && row.result_status === 'FOUND'),
    cards: [...new Set(rows.map((row) => row.cards))],
    minLatency: latencies.length ? Math.min(...latencies) : null,
    maxLatency: latencies.length ? Math.max(...latencies) : null,
    dates: [...new Set(rows.map((row) => String(row.called_at).slice(0, 10)))],
  };
}

export function dateLabel(row) {
  return row.date_end && row.date_end !== row.date ? `${row.date} to ${row.date_end}` : row.date;
}

// Sections in the JSON's scenario order; rows keep their JSON order inside a section.
export function groupProof(facts) {
  const scenarios = Array.isArray(facts?.scenarios) ? facts.scenarios : [];
  const rows = Array.isArray(facts?.rows) ? facts.rows : [];
  return scenarios.map((scenario) => ({ ...scenario, rows: rows.filter((row) => row.scenario === scenario.id) }));
}

// (2026-11-09) The newest evidence shows first; older rows go to a closed "Earlier runs (history)" fold per scenario. Rows dated
// on or after HISTORY_CUTOFF stay open; a scenario with fewer than MIN_OPEN of them is topped up with its newest older rows,
// so no scenario opens empty. Nothing is dropped or reworded: every row appears exactly once, in its original order.
export const HISTORY_CUTOFF = '2026-11-09';
export const MIN_OPEN = 2;
export function splitHistory(rows) {
  const list = Array.isArray(rows) ? rows : [];
  const open = new Set(list.filter((row) => row.date >= HISTORY_CUTOFF));
  const older = list.filter((row) => !open.has(row)).map((row, index) => ({ row, index }))
    .sort((left, right) => (left.row.date < right.row.date ? 1 : left.row.date > right.row.date ? -1 : left.index - right.index));
  for (const { row } of older) { if (open.size >= MIN_OPEN) break; open.add(row); }
  // Open rows read newest first (ties keep their original order); the fold keeps the original order.
  const current = list.map((row, index) => ({ row, index })).filter(({ row }) => open.has(row))
    .sort((left, right) => (left.row.date < right.row.date ? 1 : left.row.date > right.row.date ? -1 : left.index - right.index)).map(({ row }) => row);
  return { current, history: list.filter((row) => !open.has(row)) };
}

// The "Latest evidence" strip at the top of the page: the two headline rows quoted by their own `proven` sentence, then the other
// runs of the same day by name. Nothing here is a new fact: each line comes from a row below.
export const LATEST_ROWS = Object.freeze(['dispute-readback-hash-match', 'dispute-hosted-readonly-live']);
export const LATEST_ALSO = Object.freeze([['cross-render-workflow-run', 'Render Workflow run'], ['cross-postman-newman-run', 'Postman run'], ['policy-channel3-search-round2', 'Channel3 searches'], ['cross-apimatic-run', 'APIMatic validation']]);

// (r48) Real Sandbox rows that are refusals: TradeGlot sent no evidence to that dispute. Counted apart so the real-call
// count is not read as sends.
export const REFUSED_LABEL = 'refused before any send call';
export function refusedCount(facts) {
  return (facts?.rows || []).filter((row) => row.refused === true && row.method === 'REAL_SANDBOX').length;
}

export function methodCounts(facts) {
  const counts = Object.fromEntries(METHOD_ORDER.map((method) => [method, 0]));
  for (const row of facts?.rows || []) if (row.method in counts) counts[row.method] += 1;
  return counts;
}
