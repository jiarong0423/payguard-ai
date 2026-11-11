// (P3 2026-11-12) Check a sale: the rule grid counts and the rule-chain copy are recounted from the rule pack itself,
// and the page keeps its display-only contract (no new request, no change to a result, one solid button per screen).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const examples = JSON.parse(read('frontend/src/data/check_sale_examples_v1.json'));
const index = JSON.parse(read('frontend/src/data/country_rules_index_v1.json'));
const packText = read('data/country_rules/paypal_country_rules_v1.json');
const pack = JSON.parse(packText);
const packLines = packText.split('\n');
const ORDER = ['US', 'CA', 'GB', 'DE', 'AU', 'JP', 'SG', 'HK', 'TW', 'CN'];

// C. Grid counts: every cell and both totals from the pack (expected 368 import, 313 export).
const grid = examples.rule_grid;
assert.equal(grid.source, 'data/country_rules/paypal_country_rules_v1.json');
assert.equal(grid.retrieved_at, pack.retrieved_at);
assert.deepEqual(grid.countries.map((row) => row.code), ORDER);
assert.deepEqual(Object.keys(pack.countries).sort(), [...ORDER].sort(), 'the pack has exactly the ten countries');
for (const side of ['import', 'export']) {
  for (const code of ORDER) {
    assert.equal(grid.counts[side][code], pack[`${side}_rules`][code].rules.length, `${code} ${side} count`);
    assert.equal(grid.countries.find((row) => row.code === code).name, pack.countries[code].name, `${code} name`);
  }
  assert.equal(grid.totals[side], Object.values(pack[`${side}_rules`]).reduce((sum, block) => sum + block.rules.length, 0), `${side} total`);
}
assert.equal(grid.totals.import, 368);
assert.equal(grid.totals.export, 313);
assert.deepEqual({ US: [grid.counts.import.US, grid.counts.export.US], TW: [grid.counts.import.TW, grid.counts.export.TW] }, { US: [37, 38], TW: [49, 39] });
assert.deepEqual(index.counts, grid.counts, 'the index copy and the grid agree');

// A. Rule chain copy: one row per pack rule, every shown field equal to the pack, and the cited line holds the id.
const KEEP = ['id', 'tag', 'tier', 'route', 'channel', 'scope', 'statute', 'statute_en', 'article', 'agency', 'page_date', 'retrieved_at', 'url', 'rule'];
const packRules = ORDER.flatMap((code) => ['import', 'export'].flatMap((side) => pack[`${side}_rules`][code].rules.map((rule) => ({ side, code, rule }))));
assert.equal(index.rules.length, packRules.length, 'one index row per pack rule');
for (const [at, { side, code, rule }] of packRules.entries()) {
  const row = index.rules.find((item) => item.id === rule.id && item.side === side);
  assert.ok(row, `${rule.id} in the index`);
  assert.equal(row.country, code);
  for (const key of KEEP) assert.equal(row[key], rule[key] ?? undefined, `${rule.id} ${key}`);
  assert.equal(packLines[row.line - 1].trim(), `"id": "${rule.id}",`, `${rule.id} line`);
  if (at === 0) assert.ok(row.line > 0);
}
// The chain matches a row by side, source page and rule sentence: no two pack rules on one side and page may nest.
for (const a of index.rules) {
  const nested = index.rules.filter((b) => b !== a && b.side === a.side && b.url === a.url && b.rule.includes(a.rule));
  assert.equal(nested.length, 0, `${a.id} sentence is not inside another rule on the same page`);
}

// B. Rule match card: the pack rows it names.
const ruleCard = examples.examples.find((item) => item.id === 'rule_match');
const sg = index.rules.find((rule) => rule.id === ruleCard.rule_id);
assert.equal(sg.tier, 'prohibited');
assert.equal(sg.route, '*->SG');
assert.equal(ruleCard.result, `${sg.statute} ${sg.article}`);
assert.equal(ruleCard.result, 'Tobacco and Vaporisers Control Act s. 16');
const usps = index.rules.find((rule) => rule.id === ruleCard.also.rule_id);
assert.equal(usps.channel, 'post', 'USPS row is a post-only rule, so it shows as Check first');
assert.equal(ruleCard.also.statute, usps.statute);
assert.match(usps.statute, /^USPS Publication 52/u);

// Source wiring and the display-only contract.
const extras = read('frontend/src/CheckSaleExtras.jsx');
const panel = read('frontend/src/CountryRules.jsx');
const product = read('frontend/src/ProductReference.jsx');
const app = read('frontend/src/App.jsx');
assert.ok(!/apiRequest|\bfetch\s*\(|XMLHttpRequest|sendBeacon/u.test(extras), 'the extras make no request');
assert.ok(extras.includes("const sideOf = (code) => (code.startsWith('import') ? 'import' : 'export');"), 'chain matches the row side');
assert.ok(extras.includes("'by post'") && extras.includes('only, other channels may differ'), 'a post-only rule reads "by post only, other channels may differ"');
assert.ok(extras.includes('<span className="tg-source__label">{label}</span>'), 'one source line format');
for (const label of extras.matchAll(/<Source label="([A-Z ]+)"/gu)) assert.ok(['RECORDED', 'RECOUNTED', 'SYNTHETIC', 'HOSTED DEMO'].includes(label[1]), label[1]);
// The cards use the page's own controls: the Quick tests texts are the two descriptions.
const presets = [...app.matchAll(/onClick=\{\(\) => editDescription\('([^']+)'\)\}>/gu)].map((match) => match[1]);
assert.deepEqual(presets.slice(0, 2), examples.examples.filter((item) => item.kind === 'description').map((item) => item.description), 'Quick tests buttons hold the card texts in order');
assert.ok(extras.includes("rule_match: '[data-testid=\"country-try-example\"]'"), 'the rule card uses Fill from example');
// Auto example: the existing tryExample once per page load, only when the page is shown; no scroll.
assert.ok(panel.includes('let autoExampleDone = false;') && panel.includes('autoRef.current = tryExample;'), 'page entry runs the existing example once');
assert.ok(app.includes("autoExample={currentPage === 'compliance'}"), 'only on the Check a sale page');
// One solid button: Run Policy Check stays primary; Check country rules is an outline button.
assert.ok(panel.includes('className={`button button-secondary${waiting ? \' is-blocked\' : \'\'}`} data-testid="country-check"'), 'country check is secondary');
assert.ok(app.includes('<Button data-testid="aup-review" icon="shield" tone="blue"'), 'policy check stays the primary');
assert.ok(panel.includes('data-testid="rule-chain-trigger" aria-describedby={tipId}'), 'chain opens on hover and keyboard focus');
assert.ok(product.includes('<Suspense fallback={null}><CategoryReference category={card.category} /></Suspense>'), 'Channel3 reference under each card');
assert.ok(extras.includes('Reference, does not change the result'), 'reference label');
// D. The card names its category only; the tree-vs-AUP comparison is one page block, values from the notes and the CSV.
assert.ok(extras.includes('Channel3 category: <strong>{category}</strong></p>') && !extras.includes('Not among the'), 'card shows the category only');
assert.ok(app.includes('<Suspense fallback={null}><Channel3Reference /></Suspense>'), 'reference block on the page');
{
  const tree = examples.channel3_tree;
  const notes = read(tree.notes).split('\n');
  assert.match(notes[tree.notes_line - 1], new RegExp(`${tree.categories_read.toLocaleString('en-US')} categories, read once`, 'u'), 'categories read, from the notes line');
  const csvLines = read(tree.csv).trimEnd().split('\n');
  assert.equal(tree.mapped, csvLines.length - 1, 'mapped rows = CSV rows');
  assert.equal(tree.mapped, 191);
  assert.equal(tree.examples.length, 3);
  for (const row of tree.examples) {
    const line = csvLines[row.line - 1];
    for (const value of [row.path, row.paypal_aup_item, row.agreement]) assert.ok(line.includes(value), `CSV line ${row.line} holds ${value}`);
  }
  assert.ok(tree.csv_url.endsWith(`/${tree.csv}`));
}
// Linked tags: result, law and source share a key; connect.js starts on Check a sale and Proof, loaded on demand, cleaned up.
assert.ok(panel.includes("const link = { 'data-link': statute ? `law:${statute}` : `row:${chain.key}`"), 'rows carry linked-tag keys');
assert.ok(extras.includes("data-link={example.kind === 'route' ? `law:${example.result}` : undefined}"), 'rule card links to the rows citing its law');
assert.ok(app.includes(['import(', "'./theme/connect.js').then(({ initConnect }) =>"].join('')) && app.includes("['stage-content-compliance', 'page-proof']"), 'connect on both roots');
assert.ok(app.includes("stops.forEach((stop) => (typeof stop === 'function' ? stop() : undefined))"), 'connect cleaned up');

// The page CSS uses tokens only: no colour, radius or font-size literal.
const css = read('frontend/src/CheckSaleExtras.css');
assert.equal(/#[0-9a-f]{3,8}\b/iu.test(css.replace(/#compliance|#guide-live-preflight/gu, '')), false, 'no hex colour');
assert.equal(/border-radius:\s*[1-9]/u.test(css), false, 'no radius literal');
assert.equal(/font-size:\s*[0-9]/u.test(css), false, 'no font-size literal');
assert.equal(/font-family:(?!\s*var\()/u.test(css), false, 'no font-family literal');

console.log(`frontend_check_sale_p3: ok (${grid.totals.import} import + ${grid.totals.export} export rules, ${index.rules.length} chain rows)`);
