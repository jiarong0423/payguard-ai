// Design system v2 contract (2026-11-12): new tokens were only added (old names and values unchanged), every new
// colour meets its contrast role, red stays risk-only, and components.css ships the v2 classes writers compose with.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import * as tokens from '../frontend/src/theme/tokens.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(root, path), 'utf8');
const { color, viz, grid, layout, radius, scale } = tokens;

// 1. Pre-v2 tokens keep their values (the pages finished before v2 build on them).
const before = {
  canvas: '#f1ede3', panel: '#f8f5ee', recede: '#e8e2d5', rule: '#2b2d30', ruleSoft: '#cfc8b8', controlLine: '#8a857a',
  ink: '#111111', muted: '#5a554c', accent: '#2b2d30', accentSelected: '#e8e2d5', ok: '#2f6b3a', warn: '#7a5000',
  risk: '#c8102e', hover: '#ebe6da', disabledLine: '#cfc8b8', disabledText: '#9a958a',
};
// (round 5) rule and accent moved #111111 -> charcoal #2b2d30 on purpose (owner: all black is too heavy); ink text did not.
for (const [k, v] of Object.entries(before)) assert.equal(color[k], v, `pre-v2 token ${k} as pinned`);
assert.equal(radius.pill, 999, 'pill radius kept for old pages');

// 2. The v2 values (coordinator decision 2026-11-12).
assert.deepEqual(
  Object.fromEntries(['line', 'rowHover', 'sel', 'surface2', 'riskTint', 'okTint', 'warnTint', 'ink3'].map((k) => [k, color[k]])),
  { line: '#cfc6b4', rowHover: '#efe9dd', sel: '#e2dac8', surface2: '#ebe5d7', riskTint: '#f7e4e4', okTint: '#e4ece0', warnTint: '#f2e8d0', ink3: '#8a8478' },
);
assert.deepEqual({ ...viz }, { base: '#bdb6a6', line: '#5a554c', alert: color.warn, bg: color.recede }, 'viz: alert = check first amber, bg = surface');
assert.notEqual(viz.alert, color.risk, 'above the review line is check first, not risk');
assert.equal(radius.status, 2);
assert.deepEqual({ ...grid }, { columns: 12, measure: '68ch' });
assert.equal(layout.content, 1040); assert.equal(layout.gridCol, 64); assert.equal(layout.gridGutter, 24); assert.equal(layout.stepHead, 72);
assert.ok(grid.columns * layout.gridCol + (grid.columns - 1) * layout.gridGutter <= layout.content, '12 x 64 + 11 x 24 fits 1040');
for (const v of [layout.cardPad, layout.sectionGap, layout.gridGutter, layout.stepHead]) assert.equal(v % 4, 0, `${v} on the 4/8 grid`);
assert.ok(Object.values(scale).includes(28) && !Object.values(scale).includes(32), 'step title uses the 28 step; the scale has no 32');

// 3. Contrast (WCAG 2.x relative luminance).
const lum = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const cr = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const ratios = {};
// Text: ink and muted read on every new background.
for (const bg of ['rowHover', 'sel', 'surface2', 'riskTint', 'okTint', 'warnTint']) {
  for (const fg of ['ink', 'muted']) { const r = cr(color[fg], color[bg]); ratios[`${fg}/${bg}`] = +r.toFixed(2); assert.ok(r >= 4.5, `${fg} on ${bg}: ${r.toFixed(2)}`); }
}
// Status text on its own tint.
for (const [fg, bg] of [['risk', 'riskTint'], ['ok', 'okTint'], ['warn', 'warnTint']]) {
  const r = cr(color[fg], color[bg]); ratios[`${fg}/${bg}`] = +r.toFixed(2); assert.ok(r >= 4.5, `${fg} on ${bg}: ${r.toFixed(2)}`);
}
// ok and warn read on the selection tint; risk does not (4.23), so components.css puts selected red text on its tint.
for (const fg of ['ok', 'warn']) assert.ok(cr(color[fg], color.sel) >= 4.5, `${fg} on sel`);
ratios['risk/sel'] = +cr(color.risk, color.sel).toFixed(2);
assert.ok(ratios['risk/sel'] < 4.5, 'risk on sel is below 4.5 (documented; see .tg-is-sel .tg-deadline--due)');
// Non-text: ink-3 is for disabled controls (exempt) and marks; it must still reach 3:1 on the page and paper.
for (const bg of ['canvas', 'panel']) { const r = cr(color.ink3, color[bg]); ratios[`ink3/${bg}`] = +r.toFixed(2); assert.ok(r >= 3, `ink3 on ${bg}: ${r.toFixed(2)}`); }
assert.ok(cr(color.ink3, color.canvas) < 4.5, 'ink3 is below text contrast, so it may never be running text');
// Viz: the information marks reach 3:1 on the chart background; viz-base is context only.
for (const k of ['line', 'alert']) { const r = cr(viz[k], viz.bg); ratios[`viz.${k}/bg`] = +r.toFixed(2); assert.ok(r >= 3, `viz.${k} on viz.bg`); }
// Control edges stay controlLine (3:1); the hairline is decorative.
assert.ok(cr(color.controlLine, color.canvas) >= 3);
ratios['line/canvas'] = +cr(color.line, color.canvas).toFixed(2);
assert.ok(ratios['line/canvas'] < 3, 'line is a hairline, not a control edge');
assert.ok(cr(color.onAccent, color.ink) >= 4.5, 'selected segment: paper on ink');

// 4. Red means risk only: no v2 token reuses it, no tint is reddish except riskTint.
for (const [k, v] of Object.entries({ ...color, ...Object.fromEntries(Object.entries(viz).map(([k2, v2]) => [`viz.${k2}`, v2])) })) {
  if (k !== 'risk') assert.notEqual(v.toLowerCase(), color.risk, `${k} reuses risk red`);
}

// 5. tokens.css carries the v2 variables (parity itself is pinned by frontend_tokens.mjs).
const tokensCss = read('frontend/src/theme/tokens.css');
for (const name of ['--pg-color-line', '--pg-color-row-hover', '--pg-color-sel', '--pg-color-surface2', '--pg-color-risk-tint', '--pg-color-ok-tint',
  '--pg-color-warn-tint', '--pg-color-ink3', '--pg-viz-base', '--pg-viz-line', '--pg-viz-alert', '--pg-viz-bg', '--pg-grid-columns',
  '--pg-grid-measure', '--pg-layout-grid-gutter', '--pg-layout-step-head', '--pg-radius-status']) {
  assert.match(tokensCss, new RegExp(`${name}:`), `tokens.css declares ${name}`);
}

// 6. components.css: v2 classes exist and follow the rules.
const css = read('frontend/src/theme/components.css').replace(/\/\*[\s\S]*?\*\//g, '');
const rule = (sel) => {
  const esc = sel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const m = css.match(new RegExp(`(?:^|[}\\s,])${esc}\\s*\\{([^}]*)\\}`, 'm'));
  assert.ok(m, `components.css defines ${sel}`); return m[1];
};
const classes = ['.tg-page', '.tg-grid', '.tg-span-3', '.tg-span-4', '.tg-span-5', '.tg-span-6', '.tg-span-7', '.tg-span-8', '.tg-span-12',
  '.tg-measure', '.tg-pad', '.tg-seg', '.tg-fold', '.tg-fold__body', '.tg-tag--neutral', '.tg-stephead', '.tg-stephead__title',
  '.tg-stephead__actions', '.tg-note--check', '.tg-note--risk', '.tg-is-sel', '.tg-card--cta'];
for (const c of classes) rule(c);
assert.match(css, /\.tg-stack-48 > \* \+ \* \{ margin-top: var\(--pg-space-7\); \}/, 'stack-48 = space-7 (48px)');
assert.match(rule('.tg-grid'), /repeat\(var\(--pg-grid-columns\), minmax\(0, 1fr\)\)/);
assert.match(rule('.tg-grid'), /gap: var\(--pg-layout-grid-gutter\)/);
assert.match(rule('.tg-measure'), /max-width: var\(--pg-grid-measure\)/);
assert.match(rule('.tg-seg'), /border: 1px solid var\(--pg-color-rule\)/, 'segmented: 1px charcoal frame');
assert.match(css, /\.tg-seg > button\[aria-pressed="true"\], \.tg-seg > button\[aria-selected="true"\], \.tg-seg > button\.is-active \{ background: var\(--pg-color-sel\); color: var\(--pg-color-ink\); box-shadow: inset 0 -2px 0 var\(--pg-color-accent\); \}/, 'selected segment: tint + charcoal underline, not a solid block (round 5)');
assert.match(rule('.tg-fold'), /border: 1px solid var\(--pg-color-line\)/, 'fold: 1px hairline, never 2px ink');
assert.match(rule('.tg-tag--neutral'), /border-color: var\(--pg-color-line\)/);
assert.match(rule('.tg-stephead'), /min-height: var\(--pg-layout-step-head\)/);
assert.match(rule('.tg-stephead__title'), /var\(--pg-text-5\)/, 'step title 28px (scale step 5)');
assert.match(rule('.tg-note--check'), /border-left-color: var\(--pg-color-warn\); background: var\(--pg-color-warn-tint\)/);
assert.match(rule('.tg-note--risk'), /border-left-color: var\(--pg-color-risk\); background: var\(--pg-color-risk-tint\)/);
assert.match(rule('.tg-note'), /border-left: 4px solid/);
// Table states paint the row (no per-cell patches on phones); selection is the one tint + 3px ink bar.
assert.match(css, /\.tg-ledger__table tbody tr:hover \{ background: var\(--pg-color-row-hover\); \}/);
assert.match(css, /\.tg-ledger__table tbody tr\.is-selected, \.tg-is-sel \{ background: var\(--pg-color-sel\); \}/);
// (UI r5) .tg-table / .tg-row / .tg-figure / .tg-dialog / .tg-field / .tg-input / .tg-count were unused in the app and removed
// for the first-load budget; the ledger is the one table container.
assert.equal(/\.tg-(table|row|figure|figures|dialog|field|input|count)\b/.test(css), false, 'retired component families stay out');
assert.equal(/tr[^{]*td\s*\{[^}]*background/.test(css), false, 'no cell-level row backgrounds');
assert.equal(/accent-selected|var\(--pg-color-hover\)/.test(css), false, 'components.css uses sel / row-hover only');
assert.match(css, /\.tg-btn:disabled, \.tg-btn\[aria-disabled="true"\] \{[^}]*border: 1px dashed var\(--pg-color-line\); color: var\(--pg-color-ink3\);/);
assert.match(css, /outline: var\(--pg-layout-focus-ring\) solid var\(--pg-color-focus\); outline-offset: 3px;/, 'focus: 2px charcoal, 3px gap (round 5)');
// Corners: square everywhere; status labels 2px; no pill radius left in components.css.
for (const m of css.matchAll(/([^{}]+)\{[^}]*radius-pill[^}]*\}/g)) assert.match(m[1], /\.tg-dot\b/, `pill radius only on round dots: ${m[1].trim()}`);
for (const m of css.matchAll(/border-radius:\s*([^;]+);/g)) {
  assert.ok(/^(0|var\(--pg-radius-(status|control|pill)\)|50%)$/.test(m[1].trim()), `radius ${m[1]} is square, 2px status or a dot`);
}
// ink-3 only for disabled text and marks; red only through risk tokens.
for (const m of css.matchAll(/([^{}]+)\{[^}]*var\(--pg-color-ink3\)[^}]*\}/g)) {
  assert.ok(/disabled|tg-meta-mark/.test(m[1]), `ink3 used outside disabled / marks: ${m[1].trim()}`);
}
assert.equal(/#c8102e|#[cC]8102[eE]/.test(css), false, 'no literal red in components.css');
// Font sizes in the v2 block come from the 7-step scale.
const v2 = css.slice(css.indexOf('.tg-page {'));
assert.ok(css.indexOf('.tg-page {') > 0);
for (const m of v2.matchAll(/font(?:-size)?:[^;]*?(\d+)px/g)) assert.fail(`literal px font size in v2 block: ${m[0]}`);

// 7. UI round 5: style-reference tokens and classes (review_STYLEREF, coordinator decision 2026-11-12).
const { rule: ruleTokens, label, motion } = tokens;
assert.deepEqual({ ...ruleTokens }, { fine: '1px solid #2b2d30', double: '3px double #2b2d30' });
assert.equal(label.tracking, '.16em');
for (const k of ['quick', 'sweep', 'settle']) assert.ok(motion[k] >= 160 && motion[k] <= 240, `${k} within 160-240 ms`);
assert.equal(motion.precise, 'cubic-bezier(.2,0,0,1)', 'no overshoot (no control value above 1)');
assert.deepEqual(['vault', 'vaultInk', 'vaultMuted'].map((k) => color[k]), ['#16181b', '#f1ede3', '#b9b3a6']);
for (const [fg, min] of [['vaultInk', 4.5], ['vaultMuted', 4.5], ['vaultOk', 4.5], ['vaultWarn', 4.5], ['vaultRisk', 4.5]]) {
  const r = cr(color[fg], color.vault); ratios[`${fg}/vault`] = +r.toFixed(2); assert.ok(r >= min, `${fg} on vault: ${r.toFixed(2)}`);
}
for (const k of ['ok', 'warn', 'risk']) assert.ok(cr(color[k], color.vault) < 4.5, `paper ${k} fails on the vault, so it needs vault${k[0].toUpperCase()}${k.slice(1)}`);
for (const c of ['.tg-toast', '.tg-dot', '.tg-fold--guide', '.tg-redact', '.tg-vault', '.tg-id, .tg-ts']) rule(c);
assert.equal(/\.tg-toast \{[^}]*(risk|#c8102e)/.test(css), false, 'system messages are ink, never red');
assert.match(rule('.tg-toast'), /width: min\(var\(--pg-layout-content\), calc\(100vw - 32px\)\)/, 'toast spans the content column');
assert.match(rule('.tg-redact'), /background: var\(--pg-color-accent\)/); // round 5: charcoal like every other solid block
assert.equal(/\.tg-redact[^{]*\{[^}]*content:/.test(css), false, 'the bar renders no text: the value is not in the DOM');
assert.match(css, /letter-spacing: var\(--pg-label-tracking\)/, 'labels use the tracking token');
assert.match(css, /@media \(prefers-reduced-motion: reduce\) \{[^}]*\.tg-stamp\.is-new[^}]*animation: none;/, 'motion off under reduced motion');
assert.match(css, /(^|\n)\.tg-source \{[^}]*overflow-wrap: anywhere/, 'source lines wrap, no ellipsis');
assert.equal(/\.tg-source \{[^}]*text-overflow: ellipsis/.test(css), false);
assert.match(rule('.tg-clip__quote'), /border-left: 2px solid var\(--pg-color-rule\)/, 'quotes: 2px charcoal rule, no lone opening mark');
assert.equal(/\.tg-clip__quote::before/.test(css), false);
assert.match(css, /\.tg-seg > button \{ height: 36px;[^}]*white-space: nowrap;/, 'one control height, labels never wrap');
for (const k of ['vault', 'vault-ink', 'vault-muted', 'vault-ok', 'vault-warn', 'vault-risk']) assert.match(tokensCss, new RegExp(`--pg-color-${k}:`));
assert.match(tokensCss, /--pg-rule-double: 3px double #2b2d30;/);

// 8. Round 5 weight: charcoal controls and rules, 3px only in the masthead, finer seals, stitched day-book line.
for (const bg of ['canvas', 'recede', 'sel']) assert.ok(cr(color.accent, color[bg]) >= 3, `charcoal control edge on ${bg}`);
assert.ok(cr(color.onAccent, color.accent) >= 4.5 && cr(color.onAccent, color.accentStrong) >= 4.5, 'paper text on charcoal and on its hover');
assert.ok(cr(color.ink, color.canvas) > cr(color.accent, color.canvas), 'text stays darker than the controls');
assert.equal(layout.ruleHeavy, 3); assert.equal(layout.ruleBlock, 2);
assert.equal((css.match(/rule-heavy/g) || []).length, 1, 'the 3px rule appears once: the masthead');
assert.match(rule('.tg-stamp'), /border: 1px solid var\(--tg-tone\); box-shadow: inset 0 0 0 2px var\(--pg-color-canvas\), inset 0 0 0 3px var\(--tg-tone\);/, 'seal: 1px, 2px air, 1px');
assert.match(css, /\.tg-log__entry \+ \.tg-log__entry \{ background: linear-gradient\(90deg, var\(--pg-color-control-line\) 2px, transparent 0\) 0 0 \/ 5px 1px repeat-x; \}/, 'stitched line across the whole log row');
assert.equal(/[a-z-]+: [^;{}]*var\(--pg-color-ink\)/.test(css.replace(/(^|[;{\s])color: var\(--pg-color-ink\)/g, '')), false, 'ink is for text only; lines and controls are charcoal');

console.log(JSON.stringify({ status: 'PASS', v2_tokens: 17, r5_tokens: 15, classes: classes.length + 9, ratios }));
