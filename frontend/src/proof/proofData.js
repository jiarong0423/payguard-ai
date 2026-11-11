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
// (2026-11-10) The hosted live send leads the strip; its title carries that date. Rows from HISTORY_CUTOFF on stay open.
export const LATEST_DATE = '2026-11-10';
export const LATEST_ROWS = Object.freeze(['dispute-hosted-send-live', 'dispute-readback-hash-match', 'dispute-hosted-readonly-live']);
export const LATEST_ALSO = Object.freeze([['cross-render-workflow-run', 'Render Workflow run'], ['cross-postman-newman-run', 'Postman run'], ['policy-channel3-search-round2', 'Channel3 searches'], ['cross-apimatic-run', 'APIMatic validation']]);

// (r48) Real Sandbox rows that are refusals: TradeGlot sent no evidence to that dispute. Counted apart so the real-call
// count is not read as sends.
export const REFUSED_LABEL = 'declined before any send call';
export function refusedCount(facts) {
  return (facts?.rows || []).filter((row) => row.refused === true && row.method === 'REAL_SANDBOX').length;
}

export function methodCounts(facts) {
  const counts = Object.fromEntries(METHOD_ORDER.map((method) => [method, 0]));
  for (const row of facts?.rows || []) if (row.method in counts) counts[row.method] += 1;
  return counts;
}

// (2026-11-09) Filters on the proof page: how it was shown (method) and which sponsor tool a row involves. A row's
// `sponsors` array in proof_facts_v1.json names only tools its own evidence file shows; rows without it match no
// sponsor chip. The state lives in the URL hash so a judge can link to it, for example #sponsor=Bryntum.
export const PROOF_SPONSORS = Object.freeze(['PayPal', 'AG Grid', 'Bryntum', 'Channel3', 'APIMatic', 'Postman', 'Render', 'Gemini']);
export const PROOF_METHOD_CHIPS = Object.freeze([['ALL', 'All'], ['REAL_SANDBOX', 'Real Sandbox'], ['RECORDED', 'Recorded'], ['TEST', 'Test'], ['SYNTHETIC', 'Synthetic']]);

// '#sponsor=Bryntum&method=RECORDED' -> { method, sponsor }. Any other hash (a row anchor, none) is no filter.
export function parseProofHash(hash) {
  const state = { method: 'ALL', sponsor: '' };
  const text = String(hash || '').replace(/^#/u, '');
  if (!text.includes('=')) return state;
  for (const part of text.split('&')) {
    const [key, raw = ''] = part.split('=');
    let value = '';
    try { value = decodeURIComponent(raw.replace(/\+/gu, ' ')); } catch { value = ''; }
    if (key === 'sponsor' && PROOF_SPONSORS.includes(value)) state.sponsor = value;
    if (key === 'method' && METHOD_ORDER.includes(value)) state.method = value;
  }
  return state;
}
export function proofHash({ method = 'ALL', sponsor = '' } = {}) {
  const parts = [];
  if (sponsor) parts.push(`sponsor=${encodeURIComponent(sponsor)}`);
  if (method && method !== 'ALL') parts.push(`method=${method}`);
  return parts.length ? `#${parts.join('&')}` : '';
}
// (fix r1 F8) Pressing a chip never lands on an empty list when that chip has rows of its own: if the new chip and
// the other group's chip share no row, the other group goes back to its neutral value. The chip counts use the same
// rule, so a chip's number is what pressing it shows. `change` is { method } or { sponsor }.
export function resolveProofFilter(rows, filter, change) {
  const next = { method: filter?.method || 'ALL', sponsor: filter?.sponsor || '', ...change };
  const count = (state) => (rows || []).filter((row) => rowMatches(row, state)).length;
  if (count(next) > 0) return next;
  const alone = 'method' in change ? { method: next.method, sponsor: '' } : { method: 'ALL', sponsor: next.sponsor };
  return count(alone) > 0 ? alone : next;
}
// The line after "Showing 0 of N": names the real reason (no row for that tool at all, or no row for the pair).
export function emptyProofNote(rows, { method = 'ALL', sponsor = '' } = {}) {
  if ((rows || []).some((row) => rowMatches(row, { method, sponsor }))) return '';
  if (sponsor && !(rows || []).some((row) => rowMatches(row, { sponsor }))) return `No proof row names ${sponsor}; it is shown in the product itself (see the Sponsor map in the console footer).`;
  if (sponsor && method !== 'ALL') return `${sponsor} has proof rows, but none shown this way. Press Reset or another chip.`;
  return method !== 'ALL' ? 'No proof row was shown this way.' : '';
}
export function rowMatches(row, { method = 'ALL', sponsor = '' } = {}) {
  if (method !== 'ALL' && row.method !== method) return false;
  if (sponsor && !(Array.isArray(row.sponsors) && row.sponsors.includes(sponsor))) return false;
  return true;
}
