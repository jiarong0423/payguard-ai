// Type-scale contract for frontend/src/index.css:
// - every --type-* token is defined exactly once (one :root block) and none is below 13px;
// - no font-size declaration is below 13px unless its selector is in EXCEPTIONS with a reason;
// - every var(--type-*) used in a font-size names a defined token.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const FLOOR_PX = 13;

// Documented exceptions: selector -> reason. Keep this empty unless a sub-13px size is truly needed
// (for example text that is never visible). Every entry must explain itself.
const EXCEPTIONS = new Map([]);

const source = readFileSync(resolve(projectRoot, 'frontend/src/index.css'), 'utf8');
const css = source.replace(/\/\*[\s\S]*?\*\//g, (comment) => comment.replace(/[^\n]/g, ' '));

const toPx = (value, unit) => (unit === 'px' ? value : value * 16);
const lineOf = (index) => css.slice(0, index).split('\n').length;
const selectorBefore = (index) => {
  const open = css.lastIndexOf('{', index);
  const start = Math.max(css.lastIndexOf('}', open), css.lastIndexOf(';', open), css.lastIndexOf('{', open - 1)) + 1;
  return css.slice(start, open).trim().replace(/\s+/g, ' ');
};

// 1. Tokens: one definition each, none below the floor.
const tokens = new Map();
for (const match of css.matchAll(/(--type-[a-z-]+)\s*:\s*([^;]+);/g)) {
  const [, name, value] = match;
  assert.equal(tokens.has(name), false, `${name} is defined twice (line ${lineOf(match.index)}); keep one type-scale block`);
  tokens.set(name, value.trim());
  for (const size of value.matchAll(/([\d.]+)(px|rem|em)/g)) {
    assert.ok(toPx(Number(size[1]), size[2]) >= FLOOR_PX, `${name} uses ${size[0]} below ${FLOOR_PX}px`);
  }
}
for (const required of ['--type-display', '--type-stage-title', '--type-section-title', '--type-body', '--type-support', '--type-meta']) {
  assert.ok(tokens.has(required), `missing token ${required}`);
}
assert.equal(tokens.get('--type-stage-title'), '22px', 'step h2 is 22px');
assert.equal(tokens.get('--type-section-title'), '17px', 'section h3 is 17px');
assert.equal(tokens.get('--type-body'), '16px', 'body is 16px');
for (const name of ['--type-support', '--type-meta']) {
  const px = Number(tokens.get(name).replace('px', ''));
  assert.ok(px >= 14, `${name} is at least 14px`);
}

// 2. Declarations: nothing below the floor outside the exception list; tokens referenced must exist.
const violations = [];
let declarations = 0;
for (const match of css.matchAll(/(?<![-\w])font-size\s*:\s*([^;}]+)/g)) {
  declarations += 1;
  const value = match[1].trim();
  const selector = selectorBefore(match.index);
  for (const ref of value.matchAll(/var\((--type-[a-z-]+)/g)) {
    assert.ok(tokens.has(ref[1]), `${selector}: unknown token ${ref[1]} (line ${lineOf(match.index)})`);
  }
  for (const size of value.matchAll(/([\d.]+)(px|rem|em)\b/g)) {
    if (toPx(Number(size[1]), size[2]) < FLOOR_PX && !EXCEPTIONS.has(selector)) {
      violations.push(`line ${lineOf(match.index)}: ${selector} { font-size: ${value} }`);
    }
  }
  assert.ok(!/^(x+-small|small|smaller)$/.test(value), `${selector}: keyword size ${value} can fall below ${FLOOR_PX}px`);
}
for (const [selector, reason] of EXCEPTIONS) assert.ok(reason && reason.length > 10, `exception ${selector} needs a reason`);
assert.deepEqual(violations, [], `font-size below ${FLOOR_PX}px outside EXCEPTIONS:\n${violations.join('\n')}`);

// 3. The browser default `small { font-size: smaller }` is replaced by the meta token.
assert.match(css, /(^|\n)small\s*\{\s*font-size:\s*var\(--type-meta\)/, 'small text uses the meta token, not the browser default');

console.log(JSON.stringify({ status: 'PASS', tokens: tokens.size, font_size_declarations: declarations, exceptions: EXCEPTIONS.size }));
