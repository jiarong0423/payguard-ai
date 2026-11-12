// (F 2026-11-12) One format and one source vocabulary for the console pages (review_INTEG.md section 4 items 1-3, 5, 7).
//   1. theme/format.js: money "USD 48.00", dateLabel "9 Nov 2026", dateTimeLabel "9 Nov 2026, 06:24 GMT+8".
//   2. data/source_labels_v1.json: four labels, one sentence each; every source key names a file that exists, every cited
//      line exists, dated keys carry the date their file is headed with; the ledger and Overview figures agree with it.
//   3. theme/sources.js renders a key to the same words everywhere (line wraps, path in the title).
//   4. Overview, Check a sale, Proof and For judges use theme/sources.js only: no local source component, no local
//      legend, no typed source words; every key they name exists.
//   5. The Channel3 "readers" definition quotes docs/CHANNEL3_NOTES.md:144.
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { createRequire, register, registerHooks } from 'node:module';

const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');
let checks = 0;
const ok = (value, message) => { assert.ok(value, message); checks += 1; };
const eq = (actual, expected, message) => { assert.equal(actual, expected, message); checks += 1; };

// Node imports the Vite source as-is: JSON with its type attribute, CSS as an empty module.
const hookSource = `
export function resolve(specifier, context, next) {
  const result = next(specifier, context);
  return result.url.endsWith('.json') ? { ...result, importAttributes: { type: 'json' } } : result;
}
export function load(url, context, next) {
  return url.endsWith('.css') ? { format: 'module', source: '', shortCircuit: true } : next(url, context);
}`;
if (registerHooks) {
  registerHooks({
    resolve(specifier, context, next) {
      const result = next(specifier, context);
      return result.url.endsWith('.json') ? { ...result, importAttributes: { type: 'json' } } : result;
    },
    load(url, context, next) {
      return url.endsWith('.css') ? { format: 'module', source: '', shortCircuit: true } : next(url, context);
    },
  });
} else {
  register(`data:text/javascript,${encodeURIComponent(hookSource.replace(/export function (resolve|load)\(([^)]*)\) \{/gu, 'export async function $1($2) {').replace(/next\(([^)]*)\)/gu, 'await next($1)'))}`);
}

const format = await import('../frontend/src/theme/format.js');
const sources = await import('../frontend/src/theme/sources.js');
const requireFrontend = createRequire(new URL('frontend/package.json', root));
const { createElement } = requireFrontend('react');
const { renderToStaticMarkup } = requireFrontend('react-dom/server');

// 1. format.js
eq(format.money(48), 'USD 48.00', 'money: code first');
eq(format.money('1234.5', 'usd'), 'USD 1,234.50', 'money: thousands, upper-case code');
eq(format.money(null), format.DASH, 'money: missing');
assert.deepEqual(format.moneyParts(48, 'EUR'), { code: 'EUR', amount: '48.00' }); checks += 1;
eq(Object.keys(format.moneyParts(1)).join(','), 'code,amount', 'moneyParts in display order');
eq(format.dateLabel('2026-11-09'), '9 Nov 2026', 'dateLabel: calendar day');
eq(format.dateLabel('2026-11-10'), '10 Nov 2026', 'dateLabel: two-digit day');
eq(format.dateLabel('2026-11-08T22:24:00Z'), '8 Nov 2026', 'dateLabel: timestamp read in UTC by default');
eq(format.dateLabel('2026-11-08T22:24:00Z', 'GMT+8'), '9 Nov 2026', 'dateLabel: timestamp in a zone');
eq(format.dateLabel('2026-02-30'), format.DASH, 'dateLabel: no such day');
eq(format.dateLabel('soon'), format.DASH, 'dateLabel: not a date');
eq(format.dateTimeLabel('2026-11-08T22:24:00Z', 'GMT+8'), '9 Nov 2026, 06:24 GMT+8', 'dateTimeLabel: GMT+8');
eq(format.dateTimeLabel('2026-11-09T06:24:00+08:00', 'UTC'), '8 Nov 2026, 22:24 UTC', 'dateTimeLabel: UTC');
eq(format.dateTimeLabel('2026-11-09T03:00:00Z', 'GMT-5'), '8 Nov 2026, 22:00 GMT-5', 'dateTimeLabel: west of UTC');
eq(format.dateTimeLabel('2026-11-09T00:00:00Z', 'GMT+5:30'), '9 Nov 2026, 05:30 GMT+5:30', 'dateTimeLabel: half-hour zone');
eq(format.dateTimeLabel('2026-11-09T00:00:00Z', 'Mars'), format.DASH, 'dateTimeLabel: unknown zone label');
eq(format.dateTimeLabel('2026-11-09', 'GMT+8'), format.DASH, 'dateTimeLabel: a calendar day has no clock');
{
  const at = new Date('2026-11-09T00:00:00Z');
  const local = format.dateTimeLabel(at);
  ok(local.endsWith(` ${format.zoneLabel(-at.getTimezoneOffset())}`) && /^\d{1,2} [A-Z][a-z]{2} \d{4}, \d{2}:\d{2} (?:GMT|UTC)/u.test(local), `dateTimeLabel: viewer zone named (${local})`);
}
eq(format.zoneLabel(480), 'GMT+8', 'zoneLabel');
// (vteam viz r7) Offset 0 is named UTC, the same word the chart axis uses (was GMT on the facts, UTC on the chart).
eq(format.zoneLabel(0), 'UTC', 'zoneLabel offset 0');
eq(format.zoneLabel(-330), 'GMT-5:30', 'zoneLabel half hour');

// 2. The table.
const table = JSON.parse(read('frontend/src/data/source_labels_v1.json'));
const KINDS = ['RECORDED', 'RECOUNTED', 'SYNTHETIC', 'HOSTED DEMO'];
assert.deepEqual(table.labels.map((item) => item.kind), KINDS); checks += 1;
ok(table.labels.every((item) => /^[A-Z][^.]*[^.]\.$/u.test(item.meaning) && item.meaning.split('. ').length === 1), 'one sentence per label');
assert.deepEqual(Object.keys(sources.SOURCE_LABELS), KINDS); checks += 1;
for (const [key, entry] of Object.entries(table.sources)) {
  ok(existsSync(new URL(entry.path, root)), `${key}: ${entry.path} exists`);
  const lines = read(entry.path).split('\n');
  for (const line of entry.lines) ok(line >= 1 && line <= lines.length && lines[line - 1].trim() !== '', `${key}: line ${line} exists and is not blank`);
  if (entry.show === 'line') ok(entry.lines.length > 0, `${key}: shows its first line`);
  if (entry.show === 'date') ok(/^\d{4}-\d{2}-\d{2}$/u.test(entry.date) && lines[0].includes(entry.date), `${key}: dated ${entry.date} as its file says`);
  if (entry.show === undefined) ok(entry.date === undefined, `${key}: no hidden date`);
}
// Same file, same words.
const byPath = new Map();
for (const entry of Object.values(table.sources)) byPath.set(entry.path, [...(byPath.get(entry.path) || []), entry.text]);
for (const [path, texts] of byPath) {
  const base = new Set(texts.map((text) => text.replace(/, send \d$/u, '')));
  ok(base.size === 1, `${path}: one name (${[...base].join(' / ')})`);
}
// Cited lines hold what they are cited for.
const rulesLines = read(table.sources.country_rules_sg_ecig.path).split('\n');
eq(rulesLines[3946].trim(), '"id": "SG-IM-EC-01",', 'line 3947 is the Singapore e-cigarette rule');
eq(rulesLines[9751].trim(), '"id": "US-EX-EC-01",', 'line 9752 is the US post-only rule');
const figures = JSON.parse(read('frontend/src/data/overview_figures_v1.json'));
eq(table.sources.demo_burst.lines.join(','), [figures.step2_example.lines.burst_rows, figures.step2_example.lines.baseline, figures.step2_example.lines.amounts].join(','), 'demo burst lines = the Overview figures');
const ledger = JSON.parse(read('frontend/src/data/proof_ledger_v1.json'));
for (const send of ledger.sends) {
  const entry = table.sources[send.source_key];
  ok(entry && entry.path === send.file && entry.date === send.date.value, `${send.id}: source key ${send.source_key} names its file and date`);
  for (const field of ['debug_id', 'readback', 'file_check']) if (send[field]) ok(entry.lines.includes(send[field].line), `${send.id}: ${field} line ${send[field].line} cited`);
}
ok(table.sources.readback_send3.lines.includes(ledger.verify.recorded_sha256.line) && table.sources.readback_send3.lines.includes(ledger.verify.served_bytes.line), 'the verified send cites its SHA-256 and byte-count lines');

// 3. Rendering: a key reads the same wherever it is used.
const expected = {
  country_rules: 'Country rules file',
  // (R6 2026-11-12, S33) Line numbers only in the title, or on the visible line where exact is asked (Proof).
  country_rules_sg_ecig: 'Country rules file',
  demo_burst: 'Demo order generator',
  hosted_receipt: 'Hosted send receipt · 10 Nov 2026',
  readback_send3: 'Read-back record, send 3 · 9 Nov 2026',
  gemini_guide_runs: 'Gemini guide runs · 3 Nov 2026',
};
for (const [key, text] of Object.entries(expected)) eq(sources.sourceCitation(key).text, text, `${key} reads "${text}"`);
eq(sources.sourceCitation('country_rules_sg_ecig', { exact: true }).text, 'Country rules file · line 3947', 'exact: the line number shows');
eq(sources.sourceCitation('demo_burst', { exact: true }).text, 'Demo order generator · line 708', 'exact: the burst line');
ok(sources.sourceCitation('country_rules_sg_ecig').title.includes(':3947'), 'the line stays in the title');
assert.deepEqual(Object.values(sources.SOURCE_NAMES), ['Recorded', 'Recounted', 'Synthetic', 'Hosted demo']); checks += 1;
for (const key of Object.keys(table.sources)) {
  const cite = sources.sourceCitation(key);
  ok(cite.title.startsWith(table.sources[key].path), `${key}: full path in the title`);
  const html = renderToStaticMarkup(createElement(sources.SourceLine, { kind: 'RECORDED', source: key }));
  ok(html.includes('class="tg-source tg-source--wrap"') && html.includes('>Recorded</span>') && html.includes(cite.text.replace(/'/gu, '&#x27;')), `${key}: rendered line, label in sentence case`);
}
ok(renderToStaticMarkup(createElement(sources.SourceLine, { kind: 'RECORDED', source: ['gemini_guide_runs', 'proof_table'] })).includes('Gemini guide runs · 3 Nov 2026; Proof table'), 'two keys on one line');
{
  // An unknown key or label is logged as ERROR and shown as is; it never takes the page down.
  const logged = [];
  const original = console.error;
  console.error = (message) => logged.push(String(message));
  try {
    ok(renderToStaticMarkup(createElement(sources.SourceLine, { kind: 'REAL', source: 'proof_table' })).includes('Proof table'), 'unknown label still renders');
    ok(sources.sourceCitation('nope').unknown === true, 'unknown key flagged');
  } finally { console.error = original; }
  ok(logged.length === 2 && logged.every((line) => line.startsWith('ERROR ')), 'both logged as ERROR');
}
const legend = renderToStaticMarkup(createElement(sources.SourceLegend, { testId: 'x' }));
ok(table.labels.every((item) => legend.includes(`<b>${item.name}</b>`) && legend.includes(item.meaning)) && !legend.includes('<b>RECORDED</b>'), 'legend: four sentence-case labels with their sentence');
const sourcesCss = read('frontend/src/theme/sources.css').replace(/\/\*[\s\S]*?\*\//gu, '');
// (R5 2026-11-12) The wrap rule moved from sources.css into components.css (.tg-source); check it there.
const sourceRule = (read('frontend/src/theme/components.css').match(/^\.tg-source \{[^}]*\}/mu) || [''])[0];
ok(/overflow-wrap: anywhere/u.test(sourceRule) && !/ellipsis|nowrap/u.test(sourceRule) && !/ellipsis/u.test(sourcesCss), 'source lines wrap, never an ellipsis');
ok(!/#[0-9a-f]{3,8}\b|font-size|font-family|border-radius/iu.test(sourcesCss), 'sources.css: tokens only');

// 4. The four pages.
const PAGES = ['frontend/src/OverviewFlow.jsx', 'frontend/src/CheckSaleExtras.jsx', 'frontend/src/pages/ProofPage.jsx', 'frontend/src/pages/JudgesPage.jsx'];
const usedKeys = new Set();
for (const page of PAGES) {
  const text = read(page);
  const code = text.replace(/^\s*\/\/.*$/gmu, '').replace(/\{\/\*[\s\S]*?\*\/\}/gu, '');
  ok(/from '(\.\.\/|\.\/)theme\/sources\.js'/u.test(text), `${page}: uses theme/sources.js`);
  ok(!/function Source\b|function BasisLegend\b|SOURCE_LEGEND|className="tg-legend"|className="tg-source"/u.test(code), `${page}: no local source line or legend`);
  ok(!/'(Country rules file|Demo order generator|Demo generator|Hosted send receipt|Hosted receipt|PayPal receipt)/u.test(code) && !/· (row|line) \{/u.test(code), `${page}: no typed source words`);
  ok(!/\bplainDate\b|\bshortDate\b|MONTHS = \[/u.test(code), `${page}: dates through format.js`);
  for (const match of code.matchAll(/source="([a-z0-9_]+)"/gu)) usedKeys.add(match[1]);
  for (const match of code.matchAll(/'([a-z0-9]+_[a-z0-9_]+)'/gu)) if (table.sources[match[1]]) usedKeys.add(match[1]);
}
// Every SourceLine in frontend/src (other writers' files too) names a known key and label.
{
  const { readdirSync, statSync } = await import('node:fs');
  const walk = (dir) => readdirSync(new URL(dir, root)).flatMap((name) => (statSync(new URL(`${dir}/${name}`, root)).isDirectory() ? walk(`${dir}/${name}`) : [`${dir}/${name}`]));
  for (const file of walk('frontend/src').filter((path) => /\.(jsx?|mjs)$/u.test(path))) {
    for (const match of read(file).matchAll(/<SourceLine kind="([^"]+)"(?: source="([^"]+)")?/gu)) {
      ok(KINDS.includes(match[1]), `${file}: label ${match[1]}`);
      if (match[2]) { ok(table.sources[match[2]], `${file}: key ${match[2]} exists`); usedKeys.add(match[2]); }
    }
  }
}
for (const value of [figures.country_rules.source_key, figures.step1_example.source_key, figures.step2_example.source_key, figures.step3_send.source_key, ...ledger.sends.map((send) => send.source_key)]) usedKeys.add(value);
for (const key of usedKeys) ok(table.sources[key], `key ${key} exists`);
ok(Object.keys(table.sources).every((key) => usedKeys.has(key)), 'every key in the table is used');
ok(!read('frontend/src/OverviewFlow.jsx').includes('Real Sandbox send'), 'Overview card 03: "Sandbox send"');
// The Overview AI band quotes the Gemini guide's policy row (GEMINI_GUIDE_RUNS_20261103.md:15), recomputed here.
{
  const guide = JSON.parse(read('frontend/src/data/check_sale_examples_v1.json')).guide_ai;
  const row = read(guide.source).split('\n')[guide.line - 1].split('|').map((cell) => cell.trim());
  eq(row[2], guide.format_invalid, 'format-invalid replies from the record');
  eq(row[3], guide.precision, 'precision from the record');
  eq(row[4], guide.recall, 'recall from the record');
  eq(guide.format_invalid.split('/')[1], String(guide.sentences), 'sentence count from the record');
  eq(table.sources.gemini_guide_runs.lines[0], guide.line, 'the AI band cites that line');
  const page = read('frontend/src/OverviewFlow.jsx');
  ok(page.includes('{guide.format_invalid} format-invalid replies, precision {guide.precision}, recall {guide.recall}') && page.indexOf('data-testid="overview-ai"') > page.indexOf('<SourceLegend'), 'AI band: numbers, under the figures');
}

// 5. Readers.
const readers = table.channel3_readers;
ok(read(readers.path).split('\n')[readers.line - 1].includes(readers.quote), `readers quote is on ${readers.path}:${readers.line}`);
ok(readers.text.includes('three Claude reviewers') && readers.text.includes("who did not see each other's answers") && readers.text.includes('two other-vendor models (DeepSeek, Qwen)'), 'readers line keeps the notes\' words');
ok(read('frontend/src/CheckSaleExtras.jsx').includes('{CHANNEL3_READERS.text}'), 'the Channel3 block shows the definition');

console.log(`frontend_source_labels: ${checks} checks passed`);
