// (P2 2026-11-12) Overview figures: every value in frontend/src/data/overview_figures_v1.json is recounted here from
// its committed source, so the Overview never shows a number that drifted from the file it cites.
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const figures = JSON.parse(read('frontend/src/data/overview_figures_v1.json'));
const facts = JSON.parse(read('frontend/src/data/proof_facts_v1.json'));

// Country rules: counts and the step 01 example rule.
const rulesText = read(figures.country_rules.source);
const pack = JSON.parse(rulesText);
const count = (side) => Object.values(pack[side]).reduce((sum, country) => sum + country.rules.length, 0);
assert.equal(figures.country_rules.import_rules, count('import_rules'), 'import rule count');
assert.equal(figures.country_rules.export_rules, count('export_rules'), 'export rule count');
assert.equal(figures.country_rules.countries, Object.keys(pack.countries).length, 'country count');
const example = figures.step1_example;
const rule = Object.values(pack.import_rules).flatMap((country) => country.rules).find((item) => item.id === example.rule_id);
assert.ok(rule, 'example rule exists');
assert.equal(rule.tag, 'e_cigarettes');
assert.equal(rule.route, '*->SG');
assert.equal(rule.statute, example.statute);
assert.equal(rule.article, example.article);
assert.equal(rule.tier, example.tier);
assert.equal(rulesText.split('\n')[example.line - 1].trim(), `"id": "${example.rule_id}",`, 'cited line holds the rule id');

// Step 03: the hosted send row and the receipt line that names the case and amount.
const send = figures.step3_send;
const row = facts.rows.find((item) => item.id === send.proof_row);
assert.ok(row && row.method === 'REAL_SANDBOX' && row.source === send.source, 'proof row cites the receipt');
assert.ok(row.quotes.some((quote) => /PayPal-Debug-Id of the send: \w+/u.test(quote)), 'Debug-Id quoted in the row');
assert.match(row.how, /read-back right after showed the status [A-Za-z ]+? with/u, 'read-back status in the row');
const receiptLine = read(send.source).split('\n')[send.line - 1];
assert.ok(receiptLine.includes(`${send.case_ref} (item not received, ${send.amount.currency} ${send.amount.value}`), 'cited receipt line names the case and amount');

// Step 02: the synthetic burst, recounted from backend/app/store.py's own text (constants and the burst row range).
const step2 = figures.step2_example;
const store = read(step2.source);
const storeLines = store.split('\n');
assert.match(storeLines[step2.lines.baseline - 1], /^DEMO_VELOCITY_BASELINE = MappingProxyType\(\{/u, 'baseline line');
const baseline = store.match(/DEMO_VELOCITY_BASELINE = MappingProxyType\(\{\s*"amount_per_hour": "([\d.]+)",[\s\S]*?"observation_hours": (\d+),/u);
const amountsLine = storeLines[step2.lines.amounts - 1].match(/^DEMO_BURST_AMOUNTS = \(([^)]*)\)/u);
const range = storeLines[step2.lines.burst_rows - 1].match(/for index in range\((\d+), (\d+)\)\)/u);
assert.ok(baseline && amountsLine && range, 'store.py lines found');
const cents = (text) => Math.round(Number(text) * 100);
const amounts = [...amountsLine[1].matchAll(/"([\d.]+)"/gu)].map((match) => cents(match[1]));
const indexes = Array.from({ length: Number(range[2]) - Number(range[1]) }, (_, i) => Number(range[1]) + i);
const totalCents = indexes.reduce((sum, index) => sum + amounts[(index - 1) % amounts.length], 0);
assert.equal(step2.orders, indexes.length, 'burst order count');
assert.equal(cents(step2.total), totalCents, 'burst total');
assert.equal(step2.baseline_per_hour, baseline[1], 'baseline per hour');
assert.equal(step2.window_hours, Number(baseline[2]), 'observation window');
assert.equal(Number(step2.ratio), totalCents / step2.window_hours / cents(baseline[1]), 'ratio = total / hours / baseline');

// Sends: every send Debug-Id in docs/evidence/RECEIPT_*.md, no more and no fewer.
const receiptDir = new URL('../docs/evidence/', import.meta.url);
const found = readdirSync(receiptDir).filter((name) => /^RECEIPT_.*\.md$/u.test(name)).sort().flatMap((name) => read(`docs/evidence/${name}`).split('\n')
  .map((line, index) => ({ line, index }))
  .filter(({ line }) => /^- (result: .*(SUBMITTED|Submitted).*PayPal-Debug-Id|PayPal-Debug-Id of the send:) /u.test(line))
  .map(({ line, index }) => ({ file: `docs/evidence/${name}`, line: index + 1, debug_id: line.match(/PayPal-Debug-Id(?: of the send:)? (\w+)/u)[1] })));
assert.deepEqual(figures.receipt_sends, found, 'send Debug-Ids in the receipt files');
assert.equal(found.length, 3, 'exactly three send Debug-Ids in the RECEIPT files');
// The 2026-11-09 sends: the "## Send N" sections of READBACK_20261109.md, each with its console Debug-Id when it has one.
const readbackFile = 'docs/evidence/READBACK_20261109.md';
const readbackLines = read(readbackFile).split('\n');
const sections = readbackLines.map((line, index) => ({ line, index })).filter(({ line }) => /^## Send \d+\b/u.test(line));
const readbackFound = sections.map(({ index }, n) => {
  const end = n + 1 < sections.length ? sections[n + 1].index : readbackLines.length;
  const result = readbackLines.slice(index, end).find((line) => /^\| console result \|.*PayPal-Debug-Id `\w+`/u.test(line));
  return { file: readbackFile, line: index + 1, debug_id: result ? result.match(/PayPal-Debug-Id `(\w+)`/u)[1] : null };
});
assert.equal(readbackFound.length, 3, 'exactly three Send sections in the read-back file');
assert.deepEqual(figures.readback_sends, readbackFound, 'read-back sends and their Debug-Ids');
const allSends = [...found, ...readbackFound];
assert.equal(allSends.length, 6, 'six sends on file');
assert.equal(allSends.filter((item) => item.debug_id).length, 5, 'five with a PayPal-Debug-Id');

// (C 2026-11-12) Plain source lines, the replay date, the AI line and the legend.
assert.equal(figures.step1_example.source_plain, 'Country rules file');
assert.equal(figures.country_rules.source_plain, 'Country rules file');
assert.equal(figures.step2_example.source_plain, 'Demo generator (synthetic)');
assert.equal(figures.step3_send.source_plain, 'PayPal receipt');
assert.equal(row.date, '2026-11-10', 'card 03 is the hosted send of 2026-11-10');
assert.ok(read(send.source).includes('2026-11-10'), 'the hosted receipt is dated 2026-11-10');
const replay = figures.replay;
assert.notEqual(replay.date, row.date, 'the replay is a different send from card 03');
assert.ok(read(replay.source).includes(replay.date), 'the replay receipt carries its date');
assert.ok(read(replay.component).includes(`${replay.date} 17:16 UTC`), 'the replay component replays that send');
assert.equal(figures.receipt_sends[0].file, replay.source, 'the replay send is one of the counted sends');
const ai = figures.ai;
assert.ok(read(ai.guide_source).length > 0 && ai.guide_source.includes(ai.guide_date.replaceAll('-', '')), 'Gemini guide record');
assert.ok(read(ai.studio_source).length > 0 && ai.studio_source.includes(ai.studio_date.replaceAll('-', '')), 'AG Studio record');
const readme = read('README.md').split('\n');
assert.ok(readme[130].includes("The model only maps a seller's sentence to closed form items and a closed tag, and code, not the model, decides what is complete."), 'README.md:131 AI boundary');
assert.ok(/^\| Gemini \| used \| Closed-option evidence guide/u.test(readme[45]), 'README.md:46 Gemini row');
assert.ok(readme[41].includes(`replays the recording dated ${ai.studio_date}, with its four questions`) && ai.studio_questions === 4, 'README.md:42 AG Studio replay');
assert.ok(read('docs/SPONSOR_TECH_MAP.md').split('\n')[18].startsWith('| Gemini | Closed-option guide chooser'), 'SPONSOR_TECH_MAP.md:19');

// The page reads these files only, nothing typed in.
const page = read('frontend/src/OverviewFlow.jsx');
assert.ok(!/\b(681|368|313|48\.00|f869050ae2a63|f908765a01293|f2088142a6218|ca5782cf8df90|f492438834396|500\.00|100\.00|5\.0)\b/u.test(page), 'no figure written into the page source');
assert.ok(!/fetch\(|apiRequest/u.test(page), 'the page makes no request');
// Display contract: one-line plain sources with the full path in the title, at most one source per clip, the legend's
// four labels, Phosphor icons copied from theme/icons, tokens only in OverviewFlow.css.
for (const label of ['Recorded', 'Recounted', 'Synthetic', 'Hosted demo']) assert.ok(page.includes(`['${label}', '`), `legend: ${label}`);
const clips = page.split('<figure className="tg-clip').slice(1).map((part) => part.split('</figure>')[0]);
assert.equal(clips.length, 8, 'AI clip, three step clips, four figure clips');
for (const clip of clips) assert.equal((clip.match(/<Source |className="tg-source"/gu) || []).length, 1, 'exactly one source per clip');
assert.ok(!/RECEIPT_|docs\/evidence\/|\.json[^']/u.test(page.replace(/^import .*$/gmu, '').replace(/title=(\{`[^`]*`\}|\{[\w.]+\}|"[^"]*")/gu, '').replace(/^\s*\/\/.*$/gmu, '').replace(/\{\/\*[\s\S]*?\*\/\}/gu, '')), 'no file path in visible text');
assert.ok(page.includes('{shortDate(sendRow?.date)} hosted send') && page.includes('{shortDate(replay.date)} local send: recorded replay (nothing is sent now)'), 'card 03 and the replay name their dates (2026-11-12: replay summary reworded on request)');
for (const name of ['warning', 'check-circle', 'arrow-right']) {
  const d = read(`frontend/src/theme/icons/${name}.svg`).match(/ d="([^"]+)"/u)[1];
  assert.ok(page.includes(`icon('${d}')`), `Phosphor ${name} path copied verbatim`);
}
const css = read('frontend/src/OverviewFlow.css').replace(/\/\*[\s\S]*?\*\//gu, '');
assert.ok(!/#[0-9a-f]{3,8}\b/iu.test(css), 'no hex colour');
for (const m of css.matchAll(/(font-size|border-radius|font-family)\s*:\s*([^;}]+)/gu)) assert.match(m[2].trim(), /^var\(--pg-/u, `${m[1]} from tokens only`);
assert.deepEqual([...css.matchAll(/(\d+(?:\.\d+)?)px/gu)].map((m) => m[1]), ['900', '640'], 'px only in the two media queries');
console.log('frontend_overview_figures: ok');
