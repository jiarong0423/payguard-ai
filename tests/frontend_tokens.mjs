// C4-0 design-system contract (docs/design/VISUAL_SPEC_r7.md sections 2, 5, 6):
// tokens.js <-> tokens.css parity, type mirror of the index.css block, Inter self-hosted and pinned exactly,
// and the behaviour of format.js, motion.js, shared/asOf.js, shared/sessionLedger.js and chartTheme.js.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import * as tokens from '../frontend/src/theme/tokens.js';
import * as format from '../frontend/src/theme/format.js';
import { countUpValue, easeOut, onceInView, prefersReducedMotion } from '../frontend/src/theme/motion.js';
import { chartTheme, gridParams } from '../frontend/src/theme/chartTheme.js';
import { daysUntil, parseAsOf, resolveAsOf } from '../frontend/src/shared/asOf.js';
import { createSessionLedger } from '../frontend/src/shared/sessionLedger.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(root, path), 'utf8');

// 1. tokens.css is exactly the generated mirror of tokens.js.
const tokensCss = read('frontend/src/theme/tokens.css');
assert.equal(tokensCss, tokens.tokensCss(), 'tokens.css drifted from tokens.js; run node frontend/src/theme/writeTokensCss.mjs');
const declared = Object.fromEntries([...tokensCss.matchAll(/^\s*(--pg-[a-z0-9-]+):\s*([^;]+);$/gm)].map((m) => [m[1], m[2]]));
assert.deepEqual(declared, tokens.cssVariables(), 'every CSS variable mirrors its JS token');

// Spec values that other sessions build on.
// 2026-11-12 P0 restyle, round 3 ("Editorial Newsprint", red option 2; owner decision, ui_mock/red_compare.html):
// colour, radius and elevation values changed on purpose; names are unchanged. Previous pins: accent #4f46e5,
// canvas #eceae5, band #0b1b33/#13284a, context #7c8799, radius {6,8,12,999}, elevation l1-l3 indigo/slate shadows.
assert.equal(tokens.color.accent, '#111111', 'interactive elements are ink');
assert.equal(tokens.color.canvas, '#f1ede3', 'L0 canvas: newsprint');
assert.equal(tokens.color.recede, '#e8e2d5');
assert.equal(tokens.color.ink, '#111111');
assert.equal(tokens.color.risk, '#c8102e', 'red means rule match / risk only');
assert.equal(tokens.color.masthead, undefined, 'round 5: no decorative red token; red means risk only');
assert.equal(tokens.color.focus, '#111111', 'focus ring in ink');
assert.equal(tokens.color.band, '#111111');
assert.equal(tokens.color.bandShade, '#1c1b19');
assert.equal(tokens.color.context, '#8a857a');
assert.ok(!Object.entries(tokens.color).some(([k, v]) => v === tokens.color.risk && !['risk'].includes(k)), 'no other token reuses the risk red');
assert.deepEqual(Object.values(tokens.space), [4, 8, 12, 16, 24, 32, 48, 64]);
assert.deepEqual(Object.values(tokens.scale), [12, 14, 16, 20, 28, 40, 56], 'seven-step type scale (P0 round 2)');
assert.deepEqual({ ...tokens.radius }, { chip: 0, control: 0, card: 0, pill: 999 }, 'square print; pills stay round');
assert.equal(tokens.elevation.l1, '0 0 0 1px #111111', 'cards: thin black rule, no shadow');
assert.equal(tokens.elevation.l2, '0 0 0 2px #111111');
assert.equal(tokens.elevation.l3, '0 8px 24px rgba(17,17,17,.12), 0 1px 2px rgba(17,17,17,.08)', 'only floating layers cast a shadow');
assert.ok(tokens.motion.max <= 500 && tokens.motion.revealMax <= 2500);
assert.equal(tokens.layout.maxWidth, 1200);

// Text colours meet 4.5:1 on white; `context` is for marks only and is below it.
const luminance = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (a, b = '#ffffff') => { const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
for (const name of ['ink', 'muted', 'subtle', 'accent', 'accentStrong', 'ok', 'watch', 'warn', 'risk']) {
  for (const bg of [tokens.color.canvas, tokens.color.recede, tokens.color.panel]) assert.ok(contrast(tokens.color[name], bg) >= 4.5, `${name} reaches 4.5:1 on ${bg}`);
  assert.ok(contrast(tokens.color[name]) >= 4.5, `${name} ${tokens.color[name]} must reach 4.5:1 on white (got ${contrast(tokens.color[name]).toFixed(2)})`);
}
assert.ok(contrast(tokens.color.context) < 4.5, 'context grey stays a mark colour');
assert.ok(contrast(tokens.color.controlLine, tokens.color.canvas) >= 3, 'control edges reach 3:1 (WCAG 1.4.11)');
for (const [hue, tint] of [['ok', 'ok'], ['watch', 'watch'], ['risk', 'risk'], ['info', 'info'], ['accent', 'accent']]) {
  assert.ok(contrast(tokens.color[hue], tokens.statusTint[tint]) >= 4.5, `${hue} text reads on its tint`);
}
assert.ok(contrast(tokens.color.onAccent, tokens.color.accent) >= 4.5, 'button text on accent');
for (const name of ['bandText', 'bandMuted', 'bandAmber', 'bandGreen']) {
  assert.ok(contrast(tokens.color[name], tokens.color.bandShade) >= 4.5, `${name} reads on the navy band`);
}

// 2. The JS type mirror equals the index.css token block (which frontend_type_scale.mjs pins).
const indexCss = read('frontend/src/index.css').replace(/\/\*[\s\S]*?\*\//g, '');
const typeTokens = Object.fromEntries([...indexCss.matchAll(/(--type-[a-z-]+)\s*:\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
for (const [js, css] of Object.entries({ stageTitle: '--type-stage-title', sectionTitle: '--type-section-title', body: '--type-body', control: '--type-control', data: '--type-data', support: '--type-support', meta: '--type-meta', kpi: '--type-kpi', kpiBand: '--type-kpi-band' })) {
  assert.equal(typeTokens[css], `${tokens.type[js]}px`, `${css} equals tokens.type.${js}`);
}
for (const size of [tokens.type.chartTitle, tokens.type.chartAxis, tokens.type.gridCell]) assert.ok(size >= 14);

// 3. Inter: one exact pin, OFL-1.1 in the lock, linked once per page, no font CDN anywhere.
const pkg = JSON.parse(read('frontend/package.json'));
const pin = pkg.dependencies['@fontsource-variable/inter'];
assert.match(pin, /^\d+\.\d+\.\d+$/, 'Inter is pinned to one exact version');
const lock = JSON.parse(read('frontend/package-lock.json'));
const locked = lock.packages['node_modules/@fontsource-variable/inter'];
assert.equal(locked.version, pin);
assert.equal(locked.license, 'OFL-1.1');
assert.match(locked.integrity, /^sha512-/);
assert.equal(lock.packages[''].dependencies['@fontsource-variable/inter'], pin);
const notices = read('THIRD_PARTY_NOTICES.md');
assert.ok(notices.includes(`\`@fontsource-variable/inter@${pin}\``) && notices.includes('OFL-1.1'), 'THIRD_PARTY_NOTICES lists Inter under OFL-1.1');
const base = read('frontend/src/theme/base.css');
assert.match(base, /@import '@fontsource-variable\/inter\/index\.css';/);
assert.match(base, /@import '\.\/tokens\.css';/);
for (const page of ['index.html', 'evidence.html', 'dashboard.html']) {
  const html = read(`frontend/${page}`);
  assert.equal(html.split('<link rel="stylesheet" href="/src/theme/base.css" />').length - 1, 1, `${page} links theme/base.css once`);
  const link = html.indexOf('theme/base.css'); const script = html.indexOf('<script type="module"');
  assert.ok(link > 0 && link < script, `${page}: base.css loads before the page script`);
}
const walk = (dir) => readdirSync(dir).flatMap((name) => { const path = join(dir, name); return statSync(path).isDirectory() ? walk(path) : [path]; });
const frontendFiles = [...walk(join(root, 'frontend/src')), ...['index.html', 'evidence.html', 'dashboard.html'].map((p) => join(root, 'frontend', p))]
  .filter((path) => /\.(jsx?|mjs|css|html)$/.test(path));
for (const path of frontendFiles) {
  const text = readFileSync(path, 'utf8');
  assert.equal(/fonts\.(googleapis|gstatic)\.com|JetBrains Mono/i.test(text), false, `${path}: no font CDN or JetBrains Mono`);
}
assert.match(read('frontend/src/index.css'), /--font-sans: "Public Sans", "Inter Variable"/, 'the Tailwind sans stack starts with the self-hosted families');
// Pairing D (owner choice 2026-11-12): Newsreader + Public Sans, self-hosted with real italics; Inter stays the pinned fallback.
assert.ok(tokens.font.sans.startsWith("'Public Sans', 'Inter Variable'"), 'body/UI font: Public Sans, then Inter');
assert.ok(tokens.font.serif.startsWith("'Newsreader'"), 'heading font: Newsreader');
assert.match(base, /font-synthesis: none;/, 'no synthesised italics or bold');
for (const [file, sha] of Object.entries({
  'Newsreader-latin-var.woff2': '344d5d2b3c1f343f6c4e8f348c9727016c327f9664b3b8906f9dc72d6ec6e456',
  'Newsreader-Italic-latin-var.woff2': 'e6404648dd76ba80cfa357c4d0ca2e454d5316974c9671e58a0757ea11dc98fe',
  'PublicSans-latin-var.woff2': '6bac9ce7df65e20a8d6aca944457e961f9f10480e03c4788ddda3f472c32cad8',
  'PublicSans-Italic-latin-var.woff2': '8798913b11f08c1f088a576bcff3895e123b70268c65fe0889b39519685c6b82',
})) {
  assert.equal(createHash('sha256').update(readFileSync(join(root, 'frontend/public/fonts', file))).digest('hex'), sha, `${file} is the recorded build`);
  assert.ok(base.includes(`url('/fonts/${file}')`), `base.css declares ${file}`);
  assert.ok(read('frontend/public/fonts/SOURCES.txt').includes(sha), `SOURCES.txt records ${file}`);
}
for (const ofl of ['OFL-newsreader.txt', 'OFL-publicsans.txt']) assert.match(read(`frontend/public/fonts/${ofl}`), /SIL OPEN FONT LICENSE Version 1\.1/, `${ofl} ships`);

// 4. format.js
assert.equal(format.money(500), '500.00 USD');
assert.equal(format.money('1234.5', 'usd'), '1,234.50 USD');
assert.deepEqual(format.moneyParts(48, 'USD'), { amount: '48.00', code: 'USD' });
assert.equal(format.money(null), '—');
assert.equal(format.ratio(5), '5.0×');
assert.equal(format.ratio('3.456', 2), '3.46×');
assert.equal(format.delta(36), '+36');
assert.equal(format.delta(-36), '−36');
assert.equal(format.delta(0), '0');
assert.equal(format.delta(-2, { unit: 'd' }), '−2 d');
assert.equal(format.percent(19), '19%');
assert.equal(format.percent(0.191, { fraction: true, digits: 1 }), '19.1%');
assert.equal(format.integer(1234.4), '1,234');
assert.equal(format.utcTime('2026-11-01T15:42:09Z'), 'Nov 01 · 15:42 UTC');
assert.equal(format.utcTime('2026-11-01T00:05:00Z'), 'Nov 01 · 00:05 UTC');
assert.equal(format.utcDay('2026-11-08T23:59:00Z'), 'Nov 08');
assert.equal(format.utcTime('not a date'), '—');
assert.equal(format.isoDate('2026-11-01T12:00:00Z'), '2026-11-01T12:00:00.000Z');
assert.equal(format.isoDate(undefined), null);

// 5. motion.js
assert.equal(prefersReducedMotion({ matchMedia: () => ({ matches: true }) }), true);
assert.equal(prefersReducedMotion({ matchMedia: () => ({ matches: false }) }), false);
assert.equal(prefersReducedMotion(undefined), false);
assert.equal(prefersReducedMotion({ matchMedia: () => { throw new Error('x'); } }), false);
assert.equal(easeOut(0), 0); assert.equal(easeOut(1), 1); assert.ok(easeOut(0.5) > 0.5);
assert.equal(countUpValue(19, 0, 400), 0);
assert.equal(countUpValue(19, 400, 400), 19);
assert.equal(countUpValue(19, 9999, 400), 19);
assert.ok(countUpValue(19, 200, 400) > 9 && countUpValue(19, 200, 400) < 19);
let ran = 0;
onceInView({}, () => { ran += 1; }, { win: { matchMedia: () => ({ matches: true }), IntersectionObserver: class {} } });
assert.equal(ran, 1, 'reduced motion runs the final frame at once');
let observed = null; let disconnected = false;
class FakeObserver { constructor(cb) { observed = cb; } observe() {} disconnect() { disconnected = true; } }
const stop = onceInView({}, () => { ran += 1; }, { win: { matchMedia: () => ({ matches: false }), IntersectionObserver: FakeObserver } });
observed([{ isIntersecting: false }]); assert.equal(ran, 1);
observed([{ isIntersecting: true }]); observed([{ isIntersecting: true }]); assert.equal(ran, 2, 'runs once');
assert.equal(disconnected, true); stop();

// 6. chartTheme() / gridParams()
const theme = chartTheme();
assert.deepEqual(theme.palette.fills, [...tokens.categorical]);
assert.equal(theme.params.fontFamily, tokens.font.sans);
const sizes = JSON.stringify(theme).match(/"fontSize":\d+/g).map((s) => Number(s.split(':')[1]));
assert.ok(sizes.every((s) => s >= 14), `chart text >= 14 px (${sizes})`);
assert.equal(theme.overrides.common.background.visible, false, 'no hard-coded chart background');
assert.equal(gridParams().rowHeight, 40);
assert.equal(gridParams({ phone: true }).rowHeight, 44);
assert.equal(gridParams().accentColor, '#111111');
assert.ok(gridParams().fontSize >= 14 && gridParams().headerFontSize >= 14);

// 7. shared/asOf.js: the dashboard file is the only source; ?asof= only in public demo mode.
const fileAsOf = JSON.parse(read('frontend/src/data/dashboard_disputes_v1.json')).as_of;
assert.equal(resolveAsOf({ fileAsOf, search: '?asof=2030-01-01T00:00:00Z', publicDemo: false }), parseAsOf(fileAsOf));
assert.equal(resolveAsOf({ fileAsOf, search: '?asof=2030-01-01T00:00:00Z', publicDemo: true }), '2030-01-01T00:00:00.000Z');
assert.equal(resolveAsOf({ fileAsOf, search: '?asof=tomorrow', publicDemo: true }), parseAsOf(fileAsOf));
assert.throws(() => resolveAsOf({ fileAsOf: undefined }), /AS_OF_SOURCE_INVALID/);
assert.equal(parseAsOf('2026-11-01 12:00'), null);
assert.equal(daysUntil('2026-11-03T08:00:00Z', '2026-11-01T23:00:00Z'), 2);
assert.equal(daysUntil('2026-10-31T08:00:00Z', '2026-11-01T00:00:00Z'), -1);
const asOfSource = read('frontend/src/shared/asOfSource.js');
assert.match(asOfSource, /import \{ as_of as fileAsOf \} from '\.\.\/data\/dashboard_disputes_v1\.json';/);
assert.equal(/Date\.now\(\)|new Date\(\)/.test(asOfSource + read('frontend/src/shared/asOf.js')), false, 'no wall clock in the as-of source');

// 8. shared/sessionLedger.js
class MemoryStorage { constructor() { this.map = new Map(); } getItem(k) { return this.map.has(k) ? this.map.get(k) : null; } setItem(k, v) { this.map.set(k, String(v)); } removeItem(k) { this.map.delete(k); } }
const handlers = {};
const win = { addEventListener: (t, h) => { handlers[t] = h; }, removeEventListener: (t) => { delete handlers[t]; } };
const storage = new MemoryStorage();
const ledger = createSessionLedger({ storage, win });
const seen = [];
const unsubscribe = ledger.subscribe((entries) => seen.push(entries));
assert.ok(handlers.storage, 'listens for other tabs');
ledger.set('block:case-ref-002:tracking', { start: '2026-11-03T00:00:00Z' });
assert.deepEqual(ledger.get('block:case-ref-002:tracking'), { start: '2026-11-03T00:00:00Z' });
assert.equal(seen.length, 1);
assert.deepEqual(JSON.parse(storage.getItem('payguard.ledger.v1')), { version: 1, entries: { 'block:case-ref-002:tracking': { start: '2026-11-03T00:00:00Z' } } });
storage.setItem('payguard.ledger.v1', JSON.stringify({ version: 1, entries: { 'todo:case-ref-001': true } }));
handlers.storage({ key: 'payguard.ledger.v1' });
assert.deepEqual({ ...seen.at(-1) }, { 'todo:case-ref-001': true }, 'another tab\'s write reaches subscribers');
assert.throws(() => ledger.set('Bad Key', 1), /LEDGER_KEY_INVALID/);
assert.throws(() => ledger.set('ok', () => 1), /LEDGER_VALUE_INVALID/);
assert.throws(() => ledger.set('ok', Number.NaN), /LEDGER_VALUE_INVALID/);
ledger.remove('todo:case-ref-001'); assert.deepEqual({ ...ledger.entries() }, {});
storage.setItem('payguard.ledger.v1', '{not json'); assert.deepEqual({ ...ledger.entries() }, {}, 'corrupt storage reads as empty');
unsubscribe(); assert.equal(handlers.storage, undefined, 'last unsubscribe removes the storage listener');
const broken = { getItem() { throw new Error('denied'); }, setItem() { throw new Error('quota'); }, removeItem() { throw new Error('denied'); } };
const fallback = createSessionLedger({ storage: broken, win: null });
fallback.set('gap:case-ref-002:tracking', 'filled');
assert.equal(fallback.get('gap:case-ref-002:tracking'), 'filled', 'storage failures fall back to memory');
fallback.clear();
assert.equal(fallback.get('gap:case-ref-002:tracking'), undefined);

console.log(JSON.stringify({ status: 'PASS', css_variables: Object.keys(declared).length, font_pin: pin }));
