// Public proof page (/proof.html, optimise r24): every row traces word for word to a committed evidence file, the three
// scenarios plus "Cross-cutting" are present, the legend separates real from simulated, ids stay masked, nothing secret
// is copied, the page calls nothing and uses the console tokens, and Vite builds it as its own page. No browser.
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { METHOD_ORDER, PROOF_SCHEMA, channel3Summary, dateLabel, groupProof, methodCounts } from '../frontend/src/proof/proofData.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(projectRoot, path), 'utf8');
const json = (path) => JSON.parse(read(path));

const facts = json('frontend/src/data/proof_facts_v1.json');
const receipts = json('frontend/src/data/channel3_receipts_v1.json');

// 1. Shape: schema, four sections in order, four methods with a real/simulated flag.
assert.equal(facts.schema_version, PROOF_SCHEMA);
assert.deepEqual(facts.scenarios.map((scenario) => [scenario.id, scenario.label]), [
  ['policy', 'Policy pre-check'], ['velocity', 'Sales spike'], ['dispute', 'Dispute evidence'], ['cross', 'Cross-cutting']]);
assert.deepEqual(Object.keys(facts.methods), METHOD_ORDER);
assert.deepEqual(METHOD_ORDER.map((method) => facts.methods[method].simulated), [false, false, true, true], 'real vs simulated');
for (const method of METHOD_ORDER) assert.ok(facts.methods[method].label && facts.methods[method].meaning, `${method} explained`);
assert.match(facts.source_note, /tests\/frontend_proof_contract\.mjs/u, 'source note names the check');

// 2. Rows: unique ids, known scenario and method, ISO dates, a committed source file, quotes found verbatim in it.
const SOURCES = new Set(['docs/evidence/RECEIPT_20261031_live.md', 'docs/evidence/channel3_receipts_v1.json', 'docs/evidence/GEMINI_GUIDE_RUNS_20261103.md', 'docs/evidence/RED_TEAM_ROUNDS_20261104.md']);
const ids = new Set();
for (const row of facts.rows) {
  assert.ok(!ids.has(row.id), `${row.id} unique`);
  ids.add(row.id);
  assert.ok(facts.scenarios.some((scenario) => scenario.id === row.scenario), `${row.id} scenario`);
  assert.ok(METHOD_ORDER.includes(row.method), `${row.id} method`);
  assert.match(row.date, /^2026-\d{2}-\d{2}$/u, `${row.id} date`);
  if (row.date_end) assert.ok(row.date_end >= row.date, `${row.id} date range`);
  assert.ok(row.proven.length > 20 && row.how.length > 20, `${row.id} says what and how`);
  assert.ok(SOURCES.has(row.source) && existsSync(join(projectRoot, row.source)), `${row.id} source ${row.source}`);
  const source = read(row.source);
  if (row.check === 'channel3_receipts') {
    assert.deepEqual(row.quotes, []);
  } else {
    assert.ok(row.quotes.length >= 1, `${row.id} quotes its source`);
    for (const quote of row.quotes) assert.ok(source.includes(quote), `${row.id}: "${quote}" not found in ${row.source}`);
  }
}
for (const scenario of facts.scenarios) assert.ok(facts.rows.filter((row) => row.scenario === scenario.id).length >= 2, `${scenario.id} has rows`);
// The Sandbox rows come from the live receipt and only from it; the sales burst is the synthetic one.
assert.deepEqual(facts.rows.filter((row) => row.method === 'REAL_SANDBOX').map((row) => row.id), ['policy-invoice-draft', 'dispute-list-read', 'dispute-single-read']);
assert.ok(facts.rows.filter((row) => row.method === 'REAL_SANDBOX').every((row) => row.source === 'docs/evidence/RECEIPT_20261031_live.md'));
assert.deepEqual(facts.rows.filter((row) => row.method === 'SYNTHETIC').map((row) => row.id), ['velocity-synthetic-burst']);
assert.ok(facts.rows.filter((row) => row.source === 'docs/evidence/RED_TEAM_ROUNDS_20261104.md').every((row) => row.method === 'TEST'), 'attack rounds are tests');
// Dates agree with the files they come from.
assert.ok(read('docs/evidence/RECEIPT_20261031_live.md').startsWith('# PayGuard live Sandbox receipt, 2026-10-31'));
assert.ok(read('docs/evidence/GEMINI_GUIDE_RUNS_20261103.md').includes('Run 2026-11-03'));
assert.ok(read('docs/evidence/RED_TEAM_ROUNDS_20261104.md').startsWith('# Red-team and stress-test rounds (2026-11-03 to 2026-11-04)'));
for (const row of facts.rows) {
  if (row.source.includes('RECEIPT_20261031')) assert.equal(row.date, '2026-10-31', row.id);
  if (row.source.includes('GEMINI_GUIDE_RUNS_20261103')) assert.equal(row.date, '2026-11-03', row.id);
  if (row.source.includes('RED_TEAM_ROUNDS_20261104')) assert.equal(dateLabel(row), '2026-11-03 to 2026-11-04', row.id);
}

// 3. Channel3: the page copy is the drift-tested copy of the receipts; the row's numbers are recomputed from it.
assert.equal(read('frontend/src/data/channel3_receipts_v1.json'), read('docs/evidence/channel3_receipts_v1.json'), 'receipts copy matches docs/evidence');
const channel3 = channel3Summary(receipts);
assert.deepEqual(channel3, { count: 5, allOk: true, cards: [3], minLatency: 1.122, maxLatency: 1.602, dates: ['2026-11-01'] });
const channelRow = facts.rows.find((row) => row.check === 'channel3_receipts');
assert.equal(channelRow.date, channel3.dates[0]);
assert.ok(channelRow.proven.includes(`${channel3.count} searches, all HTTP 200, ${channel3.cards[0]} product cards each`));
assert.ok(channelRow.how.includes(`latency ${Math.floor(channel3.minLatency * 10) / 10} to ${Math.round(channel3.maxLatency * 10) / 10} s`));

// 4. Masking and secrets: masked ids exactly as in the receipt, no full PayPal ids, e-mails, tokens or hashes copied.
const factsText = read('frontend/src/data/proof_facts_v1.json');
for (const masked of ['INV2-U3KH-...-PQCK (masked)', 'PP-R-OJX-... (masked)']) {
  assert.ok(factsText.includes(masked) && read('docs/evidence/RECEIPT_20261031_live.md').includes(masked), `${masked} kept masked`);
}
const pageSources = ['frontend/src/proof/main.jsx', 'frontend/src/proof/proofData.js', 'frontend/src/proof/proof.css', 'frontend/proof.html'].map(read);
for (const text of [factsText, ...pageSources]) {
  assert.equal(/INV2(?:-[A-Z0-9]{4}){4}/u.test(text), false, 'no full invoice id');
  assert.equal(/PP-[A-Z]-[A-Z0-9]{3}-\d+|PP-D-\d{3,}/u.test(text), false, 'no full dispute id');
  assert.equal(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/u.test(text), false, 'no e-mail address');
  assert.equal(/access_token|client_secret|Bearer\s|api[_-]?key\s*[:=]|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{16,}/iu.test(text), false, 'no secret');
  assert.equal(/\b[0-9a-f]{64}\b/u.test(text), false, 'no reply hash copied');
}

// 5. The page: static, calls nothing, console tokens, own entry, not linked by this change.
const [main, data, css, html] = pageSources;
for (const source of [main, data]) {
  assert.equal(/\bfetch\(|XMLHttpRequest|sendBeacon|WebSocket|EventSource|apiRequest|from '\.\.\/api\.js'|import\(/u.test(source), false, 'calls nothing');
  assert.equal(/@bryntum|ag-grid|ag-charts|ag-studio|localStorage|sessionStorage/u.test(source), false, 'no heavy libraries or storage');
}
assert.ok(main.includes("import facts from '../data/proof_facts_v1.json';") && main.includes("import receipts from '../data/channel3_receipts_v1.json';"), 'built from committed JSON');
assert.ok(main.includes('Real vs simulated') || main.includes('proof-legend-title'), 'legend');
assert.ok(main.includes('<code data-testid="proof-source">{row.source}</code>'), 'each row names its file');
assert.ok(html.includes('<link rel="stylesheet" href="/src/theme/base.css" />') && html.includes('<script type="module" src="/src/proof/main.jsx"></script>'), 'console theme and own entry');
assert.ok(html.includes('<title>PayGuard AI · Proof</title>'));
const tokens = new Set([...read('frontend/src/theme/tokens.css').matchAll(/--(pg-[a-z0-9-]+):/gu)].map((match) => match[1]));
const used = [...css.matchAll(/var\(--(pg-[a-z0-9-]+)\)/gu)].map((match) => match[1]);
assert.ok(used.length > 20, 'uses the console tokens');
for (const token of used) assert.ok(tokens.has(token), `--${token} is a console token`);
assert.equal(/#[0-9a-f]{3,8}\b|rgba?\(/iu.test(css.replace(/\/\*[\s\S]*?\*\//gu, '')), false, 'no colours outside the tokens');
for (const size of css.matchAll(/font-size:\s*(\d+)px/gu)) assert.ok(Number(size[1]) >= 14, `font-size ${size[1]}px >= 14px`);
const vite = read('frontend/vite.config.js');
assert.ok(vite.includes("proof: fileURLToPath(new URL('proof.html', import.meta.url))"), 'Vite builds proof.html');

// 6. Grouping helpers.
const sections = groupProof(facts);
assert.deepEqual(sections.map((section) => section.id), ['policy', 'velocity', 'dispute', 'cross']);
assert.equal(sections.reduce((sum, section) => sum + section.rows.length, 0), facts.rows.length, 'every row in a section');
const counts = methodCounts(facts);
assert.equal(Object.values(counts).reduce((sum, value) => sum + value, 0), facts.rows.length);
assert.deepEqual(groupProof({}), []);
assert.deepEqual(channel3Summary({}), { count: 0, allOk: false, cards: [], minLatency: null, maxLatency: null, dates: [] });

console.log(`frontend_proof_contract: ok (${facts.rows.length} rows; ${METHOD_ORDER.map((method) => `${method} ${counts[method]}`).join(', ')}; every quote found in its source)`);
