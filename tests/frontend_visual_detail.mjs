// Visual team r6 (2026-11-12, red-team phase 2 return): theme/components.css keeps the detail rules the consensus fixed.
//   1. Status is shape as well as colour: risk / warn / ok stamps have three different frames (deuteranopia: risk vs warn dE 9).
//   2. .tg-glass is solid paper by default; blur only inside @supports, and prefers-reduced-transparency turns it back to solid.
//   3. .tg-focus carries status, so its rule is charcoal: no structure / chestnut colour in it.
//   4. Layout guards: no container-type on .tg-cards3 cards (it turns subgrid off); no focus bleed on phones (sideways scroll).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const css = readFileSync(new URL('../frontend/src/theme/components.css', import.meta.url), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const rule = (sel) => {
  const esc = sel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const m = css.match(new RegExp(`(?:^|[}\\s,])${esc}\\s*\\{([^}]*)\\}`, 'm'));
  assert.ok(m, `components.css defines ${sel}`);
  return m[1];
};
const block = (head) => {
  const start = css.indexOf(head);
  assert.ok(start >= 0, `components.css has ${head}`);
  let depth = 0;
  for (let i = css.indexOf('{', start); i < css.length; i += 1) {
    if (css[i] === '{') depth += 1;
    if (css[i] === '}') { depth -= 1; if (depth === 0) return css.slice(start, i + 1); }
  }
  return assert.fail(`${head} is not closed`);
};

// 1. Three status frames.
const stamp = rule('.tg-stamp');
const ok = rule('.tg-stamp--ok');
const warn = rule('.tg-stamp--warn');
const risk = rule('.tg-stamp--risk');
assert.match(stamp, /border: 1px solid var\(--tg-tone\); box-shadow: inset 0 0 0 2px var\(--pg-color-canvas\), inset 0 0 0 3px var\(--tg-tone\);/, 'ok (base): double-ruled seal');
assert.doesNotMatch(ok, /border-style|box-shadow/, 'ok keeps the base seal');
assert.match(warn, /border-style: dashed;/, 'warn: dashed frame');
assert.match(warn, /box-shadow: none;/, 'warn: single frame (no inner seal line)');
assert.match(risk, /box-shadow: inset 3px 0 0 var\(--tg-tone\), inset 0 0 0 2px var\(--pg-color-canvas\), inset 0 0 0 3px var\(--tg-tone\);/, 'risk: seal plus a 3px solid left bar');
assert.doesNotMatch(risk, /dashed/, 'risk is solid');
assert.equal(new Set([ok, warn, risk].map((body) => body.replace(/--tg-tone:[^;]*;/, '').trim())).size, 3, 'three different frame declarations');
assert.match(rule('.tg-pill--warn'), /outline: 1px dashed;/, 'warn pill: dashed frame');
assert.match(rule('.tg-note--risk'), /border-left-color: var\(--pg-color-risk\)/);
assert.match(css, /\.tg-note--check \{ border-left-style: dashed; \}/, 'check-first note: dashed bar, risk note: solid bar');

// 2. Glass with two fallbacks.
assert.match(rule('html .tg-glass'), /^\s*background: var\(--pg-color-canvas\);\s*$/, 'default: solid paper, no blur');
const supports = block('@supports (backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))');
const blur = [...supports.slice(supports.indexOf('{')).matchAll(/backdrop-filter: blur\((\d+)px\)/g)].map((m) => Number(m[1]));
assert.ok(blur.length === 2 && blur.every((px) => px <= 8), `blur <= 8px, prefixed and unprefixed: ${blur}`);
const mix = supports.match(/color-mix\(in srgb, var\(--pg-color-canvas\) (\d+)%, transparent\)/);
assert.ok(mix && Number(mix[1]) >= 92, 'glass paper at least 92% opaque');
const transparency = block('@media (prefers-reduced-transparency: reduce)');
assert.match(transparency, /html \.tg-glass \{ background: var\(--pg-color-canvas\); -webkit-backdrop-filter: none; backdrop-filter: none; \}/, 'reduced transparency: solid paper');
assert.ok(css.indexOf('@media (prefers-reduced-transparency: reduce)') > css.indexOf('@supports (backdrop-filter'), 'the reduced-transparency rule comes after (and wins over) the blur');

// 3. Focus area: charcoal rule, no chestnut beside status.
const focus = rule('.tg-focus');
assert.match(focus, /border-top: 2px solid var\(--pg-color-rule\);/, 'focus rule: 2px charcoal');
assert.doesNotMatch(focus, /structure|chestnut|rule-head/, 'focus carries no structure / chestnut colour');
assert.match(rule('.tg-focus:not(.tg-vault) .tg-eyebrow'), /color: var\(--pg-color-muted\);/, 'eyebrow in a focus area is muted, not chestnut');
assert.match(rule('.tg-focus:not(.tg-vault)'), /background: var\(--pg-color-panel\);/, 'focus surface is panel (lighter than canvas), never recede: sunlight risk contrast');
assert.doesNotMatch(css, /\.tg-focus[^{]*\{[^}]*recede/, 'no recede under a focus area');
assert.match(rule('.tg-due'), /box-shadow: inset 4px 0 0 var\(--pg-color-risk\);/, 'due: solid red left bar');

// 4. Layout guards.
assert.doesNotMatch(rule('.tg-cards3 > *'), /container-type/, 'cards keep subgrid: container queries sit on .tg-cq');
assert.match(rule('.tg-cq'), /container-type: inline-size;/);
assert.match(block('@media (prefers-reduced-motion: reduce) { ::view-transition'), /animation: none;/, 'view transitions off under reduced motion');
assert.match(rule('.tg-focus--bleed'), /^\s*margin-inline: 0;\s*$/, 'focus stays inside the content column at every width (no sideways scroll, aligned with the masthead)');
assert.equal((css.match(/\.tg-focus--bleed \{/g) || []).length, 1, 'one bleed rule, no width overrides');

console.log('frontend_visual_detail: ok (status frames, glass fallbacks, charcoal focus, layout guards)');
