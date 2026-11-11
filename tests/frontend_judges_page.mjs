// (P5 2026-11-12) Console For judges page: a 90-second route whose every value comes from a committed data file.
//   1. judges_route_v1.json: 3 to 4 steps, seconds add up to total_seconds (90), numbered 01.. in order.
//   2. Every deep link targets a console page App.jsx defines; the three steps keep their #compliance #velocity #disputes.
//   3. The values the steps point at agree across the data files (hosted Debug-Id, recorded SHA-256, the example rule).
//   4. JudgesPage.jsx types no number, id, hash or date by hand; one primary button; JudgesPage.css uses tokens only.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const route = JSON.parse(read('frontend/src/data/judges_route_v1.json'));
const figures = JSON.parse(read('frontend/src/data/overview_figures_v1.json'));
const facts = JSON.parse(read('frontend/src/data/proof_facts_v1.json'));
const ledger = JSON.parse(read('frontend/src/data/proof_ledger_v1.json'));
const app = read('frontend/src/App.jsx');
let checks = 0;
const ok = (value, message) => { assert.ok(value, message); checks += 1; };

// 1. The route.
ok(route.steps.length >= 3 && route.steps.length <= 4, '3 to 4 steps');
ok(route.total_seconds === 90, 'a 90-second route');
ok(route.steps.reduce((sum, step) => sum + step.seconds, 0) === route.total_seconds, 'seconds add up');
route.steps.forEach((step, index) => ok(step.n === String(index + 1).padStart(2, '0'), `step ${step.page} numbered ${step.n}`));
ok(route.steps.every((step) => step.title && step.action && !/\d/u.test(step.action)), 'actions carry no figures');

// 2. Deep links: each target is a console page in App.jsx, and the step hashes are the ones App.jsx uses.
const pagesLine = app.split('\n').find((line) => line.startsWith('const CONSOLE_PAGES = '));
ok(pagesLine, 'App.jsx defines CONSOLE_PAGES');
for (const step of route.steps) {
  ok(pagesLine.includes(`['${step.page}', '${step.title}'`), `App.jsx has the page ${step.page} titled ${step.title}`);
  if (['compliance', 'velocity', 'disputes'].includes(step.page)) ok(app.includes(`'#${step.page}'`), `App.jsx uses the hash #${step.page}`);
}
ok(/window\.history\.pushState\(null, '', `#\$\{page\}`\)/u.test(app), 'App.jsx writes #<page> for console pages (Proof)');

// 3. Values across files.
const hosted = ledger.sends.find((send) => send.basis === 'HOSTED DEMO');
const hostedRow = facts.rows.find((row) => row.id === figures.step3_send.proof_row);
ok(hosted && hostedRow, 'hosted send in the ledger and the proof facts');
ok(hostedRow.quotes.some((quote) => quote.includes(hosted.debug_id.value)), 'hosted Debug-Id quoted in the proof row');
ok(figures.receipt_sends.some((item) => item.debug_id === hosted.debug_id.value && item.file === hosted.file), 'hosted Debug-Id on the Overview');
ok(hostedRow.how.includes(`status ${hosted.readback.value}`), 'read-back status agrees');
ok(figures.step2_example.ratio === '5.0', 'the spike ratio the step shows (recounted by frontend_overview_figures.mjs)');
const readback = facts.rows.find((row) => row.id === 'dispute-readback-hash-match');
ok(readback && readback.source === ledger.verify.file, 'the MATCH step cites the read-back record');

// 4. Source hygiene.
const strip = (text) => text.replace(/\/\*[\s\S]*?\*\//gu, '').split('\n').filter((line) => !/^\s*(\/\/|import )/u.test(line)).join('\n');
const jsx = strip(read('frontend/src/pages/JudgesPage.jsx'));
ok(!/\b[0-9a-f]{8,}\b/u.test(jsx), 'no hash or Debug-Id typed');
ok(!/\d{4}-\d{2}-\d{2}/u.test(jsx), 'no ISO date typed');
ok(!/\b\d{2,}\b/u.test(jsx), 'no two-digit number typed');
ok(!jsx.includes(figures.step1_example.rule_id) && !jsx.includes(figures.step1_example.statute), 'example rule not typed');
ok(jsx.includes('href={`#${step.page}`}'), 'deep links are hashes from the route');
ok(jsx.includes("index === 0 ? 'tg-btn--primary' : 'tg-btn--secondary'"), 'one primary button: the first step');
ok(jsx.includes('tg-clip tg-clip--step') && jsx.includes('tg-clip__quote') && jsx.includes('tg-clip__source'), 'steps are shared clip containers');
for (const label of ['RECOUNTED', 'SYNTHETIC', 'HOSTED DEMO']) ok(jsx.includes(`'${label}'`), `source label ${label}`);
ok(!/https?:\/\//u.test(jsx) && !/fetch\(/u.test(jsx), 'nothing requested');
const css = strip(read('frontend/src/pages/JudgesPage.css'));
ok(!/#[0-9a-f]{3,8}\b/iu.test(css), 'no hex colour');
ok(!/border-radius|font-family:\s*['"a-z]/iu.test(css.replace(/var\(--pg-[a-z-]+\)/gu, '')), 'no radius or font family literal');
ok(!/font-size:\s*\d/u.test(css), 'font sizes are tokens');
ok(!/\b(?!1px\b)\d+px\b/u.test(css.replace(/@media \(max-width: \d+px\)/gu, '')), 'no px literal except 1px rules and breakpoints');
ok(!/(^|[,}])\s*\.tg-[a-z_-]+\s*[,{]/mu.test(css), 'no top-level styles for shared .tg-* classes');

console.log(`frontend_judges_page: ${checks} checks passed`);
