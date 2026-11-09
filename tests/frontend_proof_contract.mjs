// Public proof page (/proof.html, optimise r24): every row traces word for word to a committed evidence file, the three
// scenarios plus "Cross-cutting" are present, the legend separates real from simulated, ids stay masked, nothing secret
// is copied, the page calls nothing and uses the console tokens, and Vite builds it as its own page. No browser.
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { METHOD_ORDER, PROOF_SCHEMA, REFUSED_LABEL, channel3Summary, dateLabel, groupProof, methodCounts, refusedCount } from '../frontend/src/proof/proofData.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(projectRoot, path), 'utf8');
const json = (path) => JSON.parse(read(path));
const pageMain = () => read('frontend/src/proof/main.jsx');

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
const SANDBOX_RECEIPTS = ['docs/evidence/RECEIPT_20261031_live.md', 'docs/evidence/RECEIPT_20261104_live.md', 'docs/evidence/RECEIPT_20261105_live.md'];
// (2026-11-09) Evidence files added that day: a read-back, the hosted read-only live check, a second Channel3 round, and three tool runs.
const NEW_SANDBOX_SOURCES = ['docs/evidence/READBACK_20261109.md', 'docs/evidence/HOSTED_READONLY_LIVE_20261109.md'];
const NEW_OTHER_SOURCES = ['docs/evidence/channel3_receipts_20261109.json', 'docs/evidence/POSTMAN_RUN_20261109.md', 'docs/evidence/RENDER_WORKFLOW_RUN_20261109.md', 'docs/evidence/APIMATIC_RUN_20261109.md'];
const SOURCES = new Set([...SANDBOX_RECEIPTS, ...NEW_SANDBOX_SOURCES, ...NEW_OTHER_SOURCES, 'docs/evidence/channel3_receipts_v1.json', 'docs/evidence/GEMINI_GUIDE_RUNS_20261103.md', 'docs/evidence/RED_TEAM_ROUNDS_20261104.md']);
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
// The Sandbox rows come from the three masked live receipts (10-31 reads, 11-04 send, 11-05 recorded send) only; the sales burst is the synthetic one.
assert.deepEqual(facts.rows.filter((row) => row.method === 'REAL_SANDBOX').map((row) => row.id), ['policy-invoice-draft', 'policy-invoice-draft-recorded', 'dispute-list-read', 'dispute-single-read', 'dispute-evidence-sent', 'dispute-mismatch-refused', 'dispute-unauthorized-refused', 'dispute-evidence-sent-recorded', 'dispute-resend-amount-refused', 'dispute-submit-gated', 'dispute-readback-hash-match', 'dispute-readback-404-fixed', 'dispute-hosted-readonly-live']);
// (2026-11-05) The gate row states the current fact: two gated Sandbox sends, not the retired 2026-10-31 "mocked-transport tests only" wording.
assert.ok(!JSON.stringify(facts).includes('mocked-transport tests only'), 'no retired submit wording on /proof.html');
assert.ok(/two sends/u.test(facts.rows.find((row) => row.id === 'dispute-submit-gated').proven), 'gate row names the two sends');
// (r34) Each send row names the PayPal-Debug-Id from its receipt, and the page footer names every Sandbox receipt.
assert.ok(facts.rows.find((row) => row.id === 'dispute-evidence-sent').how.includes('PayPal-Debug-Id f908765a01293'), 'send row names the Debug-Id');
assert.ok(facts.rows.find((row) => row.id === 'dispute-evidence-sent-recorded').how.includes('PayPal-Debug-Id f2088142a6218'), 'recorded send row names the Debug-Id');
// (r48) The recorded send row names its readback Debug-Id; refusals are labelled apart from the real calls.
assert.ok(facts.rows.find((row) => row.id === 'dispute-evidence-sent-recorded').how.includes('ca5554cf42ef6'), 'recorded send row names the readback Debug-Id');
assert.deepEqual(facts.rows.filter((row) => row.refused).map((row) => row.id), ['dispute-mismatch-refused', 'dispute-unauthorized-refused', 'dispute-resend-amount-refused']);
assert.equal(refusedCount(facts), 3);
assert.equal(REFUSED_LABEL, 'refused before any send call');
assert.ok(pageMain().includes('data-testid="proof-refused">{REFUSED_LABEL}</span>'), 'refusal rows carry their own label');
for (const receipt of [...SANDBOX_RECEIPTS, ...NEW_SANDBOX_SOURCES, ...NEW_OTHER_SOURCES]) {
  assert.ok(facts.source_note.includes(receipt), `footer source list names ${receipt}`);
}
// (2026-11-04) Each real evidence send has its own masked receipt.
assert.ok(facts.rows.filter((row) => row.method === 'REAL_SANDBOX').every((row) => [...SANDBOX_RECEIPTS, ...NEW_SANDBOX_SOURCES].includes(row.source)));
assert.deepEqual(facts.rows.filter((row) => row.method === 'SYNTHETIC').map((row) => row.id), ['velocity-synthetic-burst']);
assert.ok(facts.rows.filter((row) => row.source === 'docs/evidence/RED_TEAM_ROUNDS_20261104.md').every((row) => row.method === 'TEST'), 'attack rounds are tests');
// Dates agree with the files they come from.
assert.ok(read('docs/evidence/RECEIPT_20261031_live.md').startsWith('# PayGuard live Sandbox receipt, 2026-10-31'));
assert.ok(read('docs/evidence/RECEIPT_20261104_live.md').startsWith('# PayGuard live Sandbox receipt, 2026-11-04'));
assert.ok(read('docs/evidence/RECEIPT_20261105_live.md').startsWith('# PayGuard live Sandbox receipt, 2026-11-05'));
assert.ok(read('docs/evidence/GEMINI_GUIDE_RUNS_20261103.md').includes('Run 2026-11-03'));
assert.ok(read('docs/evidence/RED_TEAM_ROUNDS_20261104.md').startsWith('# Red-team and stress-test rounds (2026-11-03 to 2026-11-04)'));
for (const row of facts.rows) {
  if (row.source.includes('RECEIPT_20261031')) assert.equal(row.date, '2026-10-31', row.id);
  if (row.source.includes('RECEIPT_20261104')) assert.equal(row.date, '2026-11-04', row.id);
  if (row.source.includes('RECEIPT_20261105')) assert.equal(row.date, '2026-11-05', row.id);
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

// 3b. (2026-11-09) The second Channel3 round: numbers recomputed from its receipts file; the 11-09 rows say TradeGlot and carry their date.
{
  const round2 = JSON.parse(read('docs/evidence/channel3_receipts_20261109.json'));
  const summary = channel3Summary(round2);
  assert.deepEqual(summary, { count: 5, allOk: true, cards: [3], minLatency: 1.138, maxLatency: 2.126, dates: ['2026-11-09'] });
  const row = facts.rows.find((item) => item.id === 'policy-channel3-search-round2');
  assert.equal(row.date, '2026-11-09');
  assert.ok(row.proven.includes(`${summary.count} live Channel3 searches`) && row.proven.includes('HTTP 200') && row.proven.includes(`${summary.cards[0]} product cards each`));
  assert.ok(row.how.includes(`latency ${Math.floor(summary.minLatency * 10) / 10} to ${Math.round(summary.maxLatency * 10) / 10} s`));
  const newRows = facts.rows.filter((item) => item.date === '2026-11-09');
  assert.deepEqual(newRows.map((item) => item.id), ['dispute-readback-hash-match', 'dispute-readback-404-fixed', 'dispute-hosted-readonly-live', 'policy-channel3-search-round2', 'cross-postman-newman-run', 'cross-render-workflow-run', 'cross-apimatic-run']);
  for (const item of newRows) {
    assert.ok(!/PayGuard/u.test(JSON.stringify(item)), `${item.id} uses the new name`);
    assert.ok(NEW_SANDBOX_SOURCES.includes(item.source) || NEW_OTHER_SOURCES.includes(item.source), `${item.id} source`);
  }
  assert.equal(read('docs/evidence/READBACK_20261109.md').includes('2026-11-09'), true);
  const readback = facts.rows.find((item) => item.id === 'dispute-readback-hash-match');
  assert.ok(/two of them|For two of them/u.test(readback.proven) && /not compared/u.test(readback.proven), 'read-back row says two matched and one was not compared');
  assert.ok(!/byte-identical|byte for byte/iu.test(JSON.stringify(newRows)), 'claims the same SHA-256, nothing stronger');
  const hosted = facts.rows.find((item) => item.id === 'dispute-hosted-readonly-live');
  assert.ok(/returned the Sandbox dispute ids in full/u.test(hosted.how) && /0 full dispute ids/u.test(hosted.how) && /d10c0ed/u.test(hosted.how), 'hosted row states the first-deployment gap and the re-check after masking');
  assert.ok(!/not yet deployed/u.test(JSON.stringify(hosted)), 'the retired not-yet-deployed wording is gone');
  assert.ok(/schedule/u.test(facts.rows.find((item) => item.id === 'cross-render-workflow-run').how) && /no nightly claim/u.test(facts.rows.find((item) => item.id === 'cross-render-workflow-run').how), 'workflow row makes no nightly claim');
}

// 4. Masking and secrets: masked ids exactly as in the receipt, no full PayPal ids, e-mails, tokens or hashes copied.
const factsText = read('frontend/src/data/proof_facts_v1.json');
for (const masked of ['INV2-U3KH-...-PQCK (masked)', 'PP-R-OJX-... (masked)']) {
  assert.ok(factsText.includes(masked) && read('docs/evidence/RECEIPT_20261031_live.md').includes(masked), `${masked} kept masked`);
}
// (2026-11-04) The send receipt keeps dispute ids at the type prefix only (PP-R-WAH-...), with no digits after it.
const receipt1104 = read('docs/evidence/RECEIPT_20261104_live.md');
assert.equal(/PP-[A-Z]-[A-Z0-9]{3}-[^.]/u.test(receipt1104), false, '11-04 receipt ids masked to the prefix');
for (const masked of ['PP-R-WAH-...', 'PP-R-KTG-...', 'PP-R-BHF-...']) assert.ok(receipt1104.includes(masked), `${masked} kept masked`);
// (2026-11-05) The recorded send receipt follows the same rule.
const receipt1105 = read('docs/evidence/RECEIPT_20261105_live.md');
assert.equal(/PP-[A-Z]-[A-Z0-9]{3}-[^.]/u.test(receipt1105), false, '11-05 receipt ids masked to the prefix');
for (const masked of ['PP-R-QIL-...', 'PP-R-KTG-...', 'PP-R-BHF-...', 'PP-R-OJX-...']) assert.ok(receipt1105.includes(masked), `${masked} kept masked`);
const pageSources = ['frontend/src/proof/main.jsx', 'frontend/src/proof/proofData.js', 'frontend/src/proof/proof.css', 'frontend/proof.html'].map(read);
for (const text of [factsText, receipt1104, receipt1105, ...pageSources]) {
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
assert.ok(html.includes('<title>TradeGlot · Proof</title>'));
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

// 7. (2026-11-08) Recorded real send: a text timeline of the 2026-11-05 send. Each quote must be in the receipt; the page calls nothing.
{
  const send = facts.recorded_send;
  assert.ok(send && Array.isArray(send.steps) && send.steps.length >= 6, 'recorded send has its steps');
  const receipt = read(send.receipt);
  for (const step of send.steps) assert.ok(receipt.includes(step.quote), `recorded send step "${step.at}": quote not found in ${send.receipt}`);
  assert.ok(read(send.file_source).includes(send.file_quote), 'placeholder file note is quoted from its receipt');
  assert.ok(send.file_note.includes('43-byte'), 'the page says the file was a 43-byte placeholder');
  assert.ok(!/byte-identical|bytes match/iu.test(JSON.stringify(send)), 'no byte-identical claim before a read-back has run');
  assert.ok(pageMain().includes('data-testid="recorded-send"') && pageMain().includes('Recorded, not live'), 'page renders the recorded send, labelled');
  assert.ok(!/fetch\(|XMLHttpRequest/u.test(pageMain()), 'proof page still makes no request');
}

console.log(`frontend_proof_contract: ok (${facts.rows.length} rows; ${METHOD_ORDER.map((method) => `${method} ${counts[method]}`).join(', ')}; every quote found in its source)`);
