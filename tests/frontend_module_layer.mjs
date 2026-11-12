// Module layer contract (static, no browser). The module layer (theme/modules.css + module class names in the JSX)
// only refines named page modules and never reaches outside them:
//   1. modules.css exists and main.jsx imports it exactly once.
//   2. modules.css (CSS escapes decoded first, so @\69mport is @import): only @media, @supports, @layer, @container and
//      @keyframes; no custom property other than --tg-* is declared (tokens are never rebound here). The subject of every
//      selector carries a module class (tg-mod / tg-block / tg-box / tg-lift, outside :has() / :not()), or is a named
//      class / id inside a module; a type, universal or attribute-only subject (`.tg-box input`), or a subject outside
//      every module (`body:has(.tg-mod) button`, `.tg-mod ~ *`), fails unless module_map.json selector_allowlist
//      lists that exact selector with a reason.
//   3. modules.css values carry no literal colour: colours come from var() and color-mix() only.
//   4. The .90 dimming sits only inside (hover: hover) and (pointer: fine), never dims a block that carries risk text,
//      and reduced-motion and forced-colors fallbacks exist.
//   5. Allowlist (MX3): tg-mod / tg-block / tg-box / tg-lift only on elements registered in module_map.json
//      module_elements (file + tag + data-testid, else className without module tokens, else id); tabIndex (any value)
//      and tg-lift only on elements registered in focus_elements, with the raw tabIndex value pinned; a duplicated
//      attribute in one tag (a second tabIndex overriding the first) fails.
//   6. Every module named in tests/fixtures/module_map.json (the list the scratch module_health.mjs checks in a browser)
//      still exists as a module element in the JSX file the map names.
//   8. Outside the module layer: frontend/index.html keeps its one pinned boot <style> block (sha in the map) and no
//      style= attribute; every stylesheet imported from frontend/src is a file the public package lists.
// A self-test runs the CSS checks on known-bad input first, so a check that stops catching fails the test.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'frontend/src');
const MAP_RAW = readFileSync(join(ROOT, 'tests/fixtures/module_map.json'));
const MAP = JSON.parse(MAP_RAW.toString('utf8'));
const git = (...args) => spawnSync('git', ['-C', ROOT, ...args], { encoding: 'buffer', maxBuffer: 64 * 1024 * 1024 });
const IN_GIT = git('rev-parse', '--is-inside-work-tree').status === 0;

// ---- 0. registry trust: the map must be the committed one (or a reviewed sha) ----------------------------------------
// The allowlist below is only as good as the map; a map edited in the same change that uses it is not reviewed.
{
  const sha = createHash('sha256').update(MAP_RAW).digest('hex');
  if (!IN_GIT) {
    console.log('frontend_module_layer: UNVERIFIABLE REGISTRY_BASE (not a git checkout; map not compared with HEAD)');
  } else {
    const head = git('show', 'HEAD:tests/fixtures/module_map.json');
    const same = head.status === 0 && Buffer.compare(head.stdout, MAP_RAW) === 0;
    if (!same && process.env.PAYGUARD_REGISTRY_REVIEWED !== sha) {
      console.error(`ERROR REGISTRY_CHANGED_UNREVIEWED: tests/fixtures/module_map.json ${head.status === 0 ? 'differs from' : 'is not in'} git HEAD (sha256 ${sha}); set PAYGUARD_REGISTRY_REVIEWED=<that sha> only after review`);
      process.exit(1);
    }
    if (!same) console.log(`frontend_module_layer: registry change accepted by PAYGUARD_REGISTRY_REVIEWED (sha256 ${sha})`);
  }
}
const CLASS_ALT = MAP.module_classes.map((c) => `${c}(?:--[a-z0-9-]+)?`).join('|');
const MODULE_SEL = new RegExp(`\\.(?:${CLASS_ALT})(?![\\w-])`);
const TOKEN = new RegExp(`(?<![\\w-])(?:${CLASS_ALT})(?![\\w-])`, 'g');
const INTERACTIVE = new Set(['button', 'a', 'input', 'select', 'textarea', 'summary', 'option', 'label']);
const ALLOWED_AT = ['@media', '@supports', '@layer', '@container', '@keyframes'];
const NAMED_COLOURS = /(?<![\w-])(?:white|black|red|green|blue|gray|grey|silver|maroon|purple|fuchsia|lime|olive|yellow|navy|teal|aqua|orange|pink|brown|gold|beige|ivory|tan|khaki|coral|crimson|indigo|violet|cyan|magenta)(?![\w-])/i;

// ---- CSS helpers -------------------------------------------------------------------------------------------------
const decodeEscapes = (css) => css.replace(/\\([0-9a-fA-F]{1,6})\s?/g, (m, hex) => String.fromCodePoint(Math.min(parseInt(hex, 16), 0x10ffff))).replace(/\\(.)/g, '$1');
const stripComments = (css) => decodeEscapes(css.replace(/\/\*[\s\S]*?\*\//g, ''));
const ALLOW_SELECTORS = new Set((MAP.selector_allowlist || []).filter((e) => e.reason).map((e) => e.selector.replace(/\s+/g, ' ')));
function splitList(prelude) {
  const parts = []; let depth = 0; let cur = '';
  for (const ch of prelude) {
    if ('(['.includes(ch)) depth++;
    if (')]'.includes(ch)) depth--;
    if (ch === ',' && depth === 0) { parts.push(cur); cur = ''; } else cur += ch;
  }
  parts.push(cur);
  return parts.map((p) => p.trim()).filter(Boolean);
}
function selectorVerdict(part) {
  // 'module' | 'named-inside' | 'bare-inside' | 'outside' (same rule as the scratch guard_module_separation.py).
  // :is()/:where() whose every argument is a module selector stands for a module compound; of plain classes / ids, a named one.
  let s = part.replace(/:(?:is|where)\(([^()]*)\)/g, (m, args) => (args.split(',').every((a) => MODULE_SEL.test(a)) ? '.tg-mod'
    : args.split(',').every((a) => /^\s*[.#][A-Za-z_][\w-]*\s*$/.test(a)) ? '.named' : m));
  let flat = ''; let depth = 0;
  for (const ch of s) {
    if (ch === '(') { depth++; flat += depth === 1 ? '(' : '_'; } else if (ch === ')') { depth--; flat += depth === 0 ? ')' : '_'; } else flat += depth ? '_' : ch;
  }
  flat = flat.replace(/\[[^\]]*\]/g, '[]').trim();
  const seq = []; let comb = ' ';
  for (const t of flat.split(/\s*([>+~])\s*|\s+/)) {
    if (!t) continue;
    if ('>+~'.includes(t) && t.length === 1) { comb = t; continue; }
    seq.push([comb, t]); comb = ' ';
  }
  let state = 'outside';
  for (const [c, compound] of seq) {
    if (MODULE_SEL.test(compound)) state = 'module';
    else if (c === ' ' || c === '>') state = state === 'module' || state === 'inside' ? 'inside' : 'outside';
    else state = state === 'inside' ? 'inside' : 'outside';
  }
  if (state === 'module') return 'module';
  if (state === 'inside') return /[.#][A-Za-z_]/.test(seq[seq.length - 1][1].replace(/:[\w-]+(\([^)]*\))?/g, '')) ? 'named-inside' : 'bare-inside';
  return 'outside';
}
const selectorOk = (part) => ['module', 'named-inside'].includes(selectorVerdict(part)) || ALLOW_SELECTORS.has(part.replace(/\s+/g, ' '));
function cssRules(css) {
  // Flat list of { prelude, body, at: [enclosing @-preludes] }.
  const rules = []; const stack = []; let buf = '';
  for (const ch of stripComments(css)) {
    if (ch === '{') { stack.push({ prelude: buf.trim(), body: '' }); buf = ''; continue; }
    if (ch === '}') {
      const top = stack.pop(); if (!top) { buf = ''; continue; }
      if (!top.prelude.startsWith('@')) rules.push({ prelude: top.prelude, body: buf.trim(), at: stack.map((x) => x.prelude) });
      buf = ''; continue;
    }
    if (ch === ';' && !stack.length) { if (buf.trim().startsWith('@')) rules.push({ prelude: buf.trim(), body: '', at: [], statement: true }); buf = ''; continue; }
    buf += ch;
  }
  return rules;
}
function cssViolations(css) {
  const out = [];
  for (const at of stripComments(css).match(/@[a-zA-Z-]+/g) || []) if (!ALLOWED_AT.some((a) => at.startsWith(a))) out.push(`at-rule ${at}`);
  for (const rule of cssRules(css)) {
    if (rule.statement) continue;
    const inKeyframes = rule.at.some((a) => a.startsWith('@keyframes'));
    if (!inKeyframes) for (const part of splitList(rule.prelude)) if (!selectorOk(part)) out.push(`selector subject ${selectorVerdict(part)}: ${part}`);
    for (const decl of rule.body.split(';')) {
      const i = decl.indexOf(':'); if (i < 0) continue;
      const prop = decl.slice(0, i).trim(); let value = decl.slice(i + 1).trim();
      if (prop.startsWith('--') && !prop.startsWith('--tg-')) out.push(`declares ${prop} (only --tg-* here; tokens are not rebound)`);
      if (prop.startsWith('--') && !/color|colour|edge|tone/.test(prop)) continue;
      value = value.replace(/var\([^()]*(?:\([^()]*\)[^()]*)*\)/g, 'VAR');
      if (/#[0-9a-f]{3,8}\b/i.test(value) || /\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\(/i.test(value) || NAMED_COLOURS.test(value)) out.push(`literal colour in ${prop}: ${value.slice(0, 60)}`);
    }
  }
  return out;
}

// Self-test: each known-bad input must be caught.
for (const bad of ['button { display: none; }', '@import url("../index.css");', 'body:has(.tg-mod) button { display: none; }', '.tg-mod ~ * { color: var(--x); }',
  '.tg-mod { color: #fff; }', '.tg-box { background: rgb(0 0 0); }', '.tg-lift { border-color: white; }', '@font-face { font-family: x; }',
  '.tg-box input { height: 10px; }', '@\\69mport url("./components.css");', '.tg-box { --pg-color-ink: var(--pg-color-paper); }', '.tg-mod > * { margin: 0; }']) {
  assert.ok(cssViolations(bad).length > 0, `self-test: the CSS checks must reject ${bad}`);
}
for (const good of ['.tg-mod .x > .y { color: var(--pg-color-ink); }', '.tg-box--a > .b + .c { margin: 0; }', ':is(.tg-box--a, .tg-box--b) > .s { display: none; }', '.tg-mod > :is(.a, .b) { gap: 0; }', '.tg-lift { --tg-edge: var(--a); }',
  '.tg-lift.ds-head + .tg-block { box-shadow: 0 0 0 color-mix(in srgb, var(--a) 20%, transparent); }', '@media (min-width: 1px) { #x .y.tg-mod { gap: 0; } }']) {
  assert.deepEqual(cssViolations(good), [], `self-test: the CSS checks must accept ${good}`);
}

// ---- 1. stylesheet and import -------------------------------------------------------------------------------------
const modulesPath = join(SRC, 'theme/modules.css');
assert.ok(statSync(modulesPath).isFile(), 'frontend/src/theme/modules.css exists');
const modulesCss = readFileSync(modulesPath, 'utf8');
const mainJsx = readFileSync(join(SRC, 'main.jsx'), 'utf8');
assert.equal((mainJsx.match(/^\s*import\s+['"]\.\/theme\/modules\.css['"];?\s*$/gm) || []).length, 1, 'main.jsx imports theme/modules.css exactly once');

// ---- 2 + 3. selectors and colours -----------------------------------------------------------------------------------
assert.deepEqual(cssViolations(modulesCss), [], 'modules.css: every selector inside a module, no forbidden at-rule, no literal colour');

// ---- 4. dimming and fallbacks ---------------------------------------------------------------------------------------
const rules = cssRules(modulesCss);
const dimRules = rules.filter((r) => /brightness\(/.test(r.body));
assert.ok(dimRules.length > 0, 'the lift dims its sibling blocks');
for (const r of dimRules) {
  assert.ok(r.at.some((a) => /\(hover:\s*hover\)\s*and\s*\(pointer:\s*fine\)/.test(a)), `brightness only on a fine pointer: ${r.prelude.slice(0, 80)}`);
  assert.match(r.prelude, /:not\([^{]*:has\([^{]*\[class\*=risk\]/, 'a block that carries risk text is never dimmed');
}
assert.ok(rules.some((r) => r.at.some((a) => /prefers-reduced-motion:\s*reduce/.test(a)) && /transition:\s*none/.test(r.body)), 'reduced-motion fallback');
assert.ok(rules.some((r) => r.at.some((a) => /forced-colors:\s*active/.test(a)) && /filter:\s*none/.test(r.body)), 'forced-colors fallback');

// ---- JSX scanning ---------------------------------------------------------------------------------------------------
function* filesWith(dir, ext) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* filesWith(p, ext); else if (name.endsWith(ext)) yield p;
  }
}
const jsxFiles = (dir) => filesWith(dir, '.jsx');
const jsFiles = (dir) => filesWith(dir, '.js');
function* openTags(text) {
  for (const m of text.matchAll(/<([A-Za-z][\w.]*)/g)) {
    const prev = text[m.index - 1];
    if (prev && /[\w)\]]/.test(prev)) continue;
    let depth = 0; let quote = null;
    for (let i = m.index + m[0].length; i < text.length; i++) {
      const ch = text[i];
      if (quote) { if (ch === '\\') i++; else if (ch === quote) quote = null; continue; }
      if ('"\'`'.includes(ch)) quote = ch;
      else if (ch === '{') depth++;
      else if (ch === '}') depth--;
      else if (ch === '>' && depth === 0) { yield { name: m[1], tag: text.slice(m.index, i + 1), index: m.index }; break; } else if (ch === '<' && depth === 0 && /[A-Za-z]/.test(text[i + 1] || '')) break;
    }
  }
}
function classValue(tag) {
  const m = tag.match(/\bclassName=(?:"([^"]*)"|'([^']*)'|\{`([^`]*)`\}|\{'([^']*)'\})/);
  return m ? (m[1] ?? m[2] ?? m[3] ?? m[4]) : '';
}
const literal = (tag, attr) => (tag.match(new RegExp(`\\b${attr}="([^"]+)"`)) || [])[1];
function moduleName(tag) {
  // Same order as module_health.mjs nameOf(): modifier, else data-testid, else id, else first non-tg class.
  const cls = classValue(tag).split(/\s+/).filter(Boolean);
  const mod = cls.find((c) => /^tg-(mod|block)--/.test(c));
  if (mod) return mod.replace(/^tg-(mod|block)--/, '');
  return literal(tag, 'data-testid') || literal(tag, 'id') || cls.find((c) => !c.startsWith('tg-') && !c.includes('${')) || cls[0];
}
// ---- JSX attribute parsing (same rules as the scratch module_registry.py used by the guard) -------------------------
function balancedEnd(text, i) {
  let depth = 0; let quote = null;
  for (; i < text.length; i++) {
    const ch = text[i];
    if (quote) { if (ch === '\\') i++; else if (ch === quote) quote = null; continue; }
    if ('"\'`'.includes(ch)) quote = ch;
    else if (ch === '{') depth++;
    else if (ch === '}') { depth--; if (depth === 0) return i + 1; }
  }
  return i;
}
function* parsedTags(text) {
  for (const m of text.matchAll(/<([A-Za-z][\w.]*)/g)) {
    const prev = text[m.index - 1];
    if (prev && /[\w)\]]/.test(prev)) continue;
    let i = m.index + m[0].length; const attrs = []; let ok = false;
    while (i < text.length) {
      while (i < text.length && /\s/.test(text[i])) i++;
      if (i >= text.length) break;
      if (text[i] === '>') { ok = true; i++; break; }
      if (text.startsWith('/>', i)) { ok = true; i += 2; break; }
      if (text[i] === '{') { const j = balancedEnd(text, i); attrs.push(['...', text.slice(i, j)]); i = j; continue; }
      const am = /^[A-Za-z_][\w:.-]*/.exec(text.slice(i, i + 200)); if (!am) break;
      const name = am[0]; i += name.length;
      let k = i; while (k < text.length && ' \t'.includes(text[k])) k++;
      if (text[k] === '=') {
        k++; while (k < text.length && /\s/.test(text[k])) k++;
        if (text[k] === '"' || text[k] === "'") { const e = text.indexOf(text[k], k + 1); if (e < 0) break; attrs.push([name, text.slice(k, e + 1)]); i = e + 1; }
        else if (text[k] === '{') { const e = balancedEnd(text, k); attrs.push([name, text.slice(k, e)]); i = e; }
        else break;
      } else attrs.push([name, null]);
    }
    if (ok) yield { name: m[1], tag: text.slice(m.index, i), attrs };
  }
}
const attrClass = (attrs) => (attrs.find(([n, v]) => n === 'className' && v !== null) || [, ''])[1];
function elementKey(name, attrs) {
  const vals = Object.fromEntries(attrs.filter(([n]) => n !== '...'));
  if (vals['data-testid']) return `${name}|testid=${vals['data-testid']}`;
  const cls = attrClass(attrs);
  if (cls) return `${name}|class=${cls.replace(TOKEN, '').replace(/\s+/g, ' ').replace(/" /g, '"').replace(/ "/g, '"').replace(/` /g, '`').replace(/ `/g, '`')}`;
  if (vals.id) return `${name}|id=${vals.id}`;
  return `${name}|attrs=${attrs.map(([n]) => n).sort().join(',')}`;
}
const LIFT = /(?<![\w-])tg-lift(?![\w-])/;

// ---- 5 + 7. allowlist: module classes, tabIndex and tg-lift only on registered elements -------------------------------
for (const kind of ['module_elements', 'focus_elements']) {
  const keys = MAP[kind].map((e) => `${e.file} ${e.key}`);
  const dup = keys.filter((k, i) => keys.indexOf(k) !== i);
  assert.deepEqual(dup, [], `module_map.json ${kind}: every key unique (twins use #n/total)`);
  assert.ok(MAP[kind].every((e) => (e.count ?? 1) === 1), `module_map.json ${kind}: count is 1 for every key`);
}
const modReg = new Map(MAP.module_elements.map((e) => [`${e.file}\u0000${e.key}`, e]));
const focReg = new Map(MAP.focus_elements.filter((e) => e.reason).map((e) => [`${e.file}\u0000${e.key}`, e]));
const modSeen = new Map(); const focSeen = new Map();
const found = new Map(); // module name -> Set(files)
const moduleTags = new Map(); // file -> [opening tags of module elements]
const registryFindings = [];
for (const file of jsxFiles(SRC)) {
  const rel = relative(ROOT, file);
  const text = readFileSync(file, 'utf8');
  const tagsHere = [...parsedTags(text)];
  const baseKeys = tagsHere.map((t) => elementKey(t.name, t.attrs));
  const totals = baseKeys.reduce((m, k) => m.set(k, (m.get(k) || 0) + 1), new Map());
  const ord = new Map();
  for (const [ti, t] of tagsHere.entries()) {
    const names = t.attrs.map(([n]) => n).filter((n) => n !== '...');
    const dups = [...new Set(names.filter((n, i) => names.indexOf(n) !== i))];
    if (dups.length) registryFindings.push(`${rel}: duplicate attribute ${dups} in ${t.tag.slice(0, 90)}`);
    const cls = attrClass(t.attrs);
    const mods = [...new Set(cls.match(TOKEN) || [])].sort();
    // A key shared by twins in one file gets #n/total (document order): moving a module class to a twin changes the key.
    const b = baseKeys[ti]; ord.set(b, (ord.get(b) || 0) + 1);
    const key = totals.get(b) > 1 ? `${b}#${ord.get(b)}/${totals.get(b)}` : b; const id = `${rel}\u0000${key}`;
    for (const [n, v] of t.attrs) if (n === '...' && /^\{\s*\.\.\.\s*\{/.test(v)) registryFindings.push(`${rel}: literal object spread ${v.slice(0, 50)} in ${t.tag.slice(0, 80)}`);
    if (/(?<![\w-])tg-(mod|block)(?![\w-])/.test(cls)) { if (!moduleTags.has(rel)) moduleTags.set(rel, []); moduleTags.get(rel).push(t.tag); const n = moduleName(t.tag); if (!found.has(n)) found.set(n, new Set()); found.get(n).add(rel); }
    if (mods.length) {
      const e = modReg.get(id); modSeen.set(id, (modSeen.get(id) || 0) + 1);
      if (!e) registryFindings.push(`${rel}: module class ${mods} on an unregistered element ${key.slice(0, 90)}`);
      else if (!mods.every((c) => e.module_classes.includes(c))) registryFindings.push(`${rel}: module classes ${mods} not registered for ${key.slice(0, 90)}`);
      else if (modSeen.get(id) > 1) registryFindings.push(`${rel}: module element ${key.slice(0, 90)} appears more often than registered`);
    }
    const tabs = t.attrs.filter(([n]) => n === 'tabIndex').map(([, v]) => v);
    const lift = LIFT.test(cls);
    if (tabs.length || lift) {
      const e = focReg.get(id); focSeen.set(id, (focSeen.get(id) || 0) + 1);
      const tab = tabs.length ? tabs[0] : null;
      if (!e) registryFindings.push(`${rel}: tabIndex/tg-lift on an unregistered element ${key.slice(0, 90)} (tabIndex=${tab})`);
      else if (e.tabindex !== tab || Boolean(e.lift) !== lift) registryFindings.push(`${rel}: focus element ${key.slice(0, 90)} changed: tabIndex ${tab} lift ${lift} (registered ${e.tabindex} / ${e.lift})`);
      else if (focSeen.get(id) > 1) registryFindings.push(`${rel}: focus element ${key.slice(0, 90)} appears more often than registered`);
    }
  }
}
assert.deepEqual(registryFindings, [], 'module classes / tabIndex / tg-lift only on elements registered in module_map.json; no duplicated attribute');
for (const e of [...MAP.module_elements, ...MAP.focus_elements]) assert.ok(readFileSync(join(ROOT, e.file), 'utf8').length > 0, `registered file exists: ${e.file}`);

// ---- 9. spreads on changed lines (git diff HEAD): a spread {...x} added must have been on a removed line of that file ---
if (IN_GIT) {
  const diff = git('diff', '-U0', '--no-color', 'HEAD', '--', 'frontend/src').stdout.toString('utf8');
  const per = new Map(); let cur = null;
  for (const line of diff.split('\n')) {
    if (line.startsWith('+++ ')) { cur = line.startsWith('+++ b/') ? line.slice(6) : null; if (cur && !per.has(cur)) per.set(cur, [[], []]); }
    else if (cur && line.startsWith('-') && !line.startsWith('---')) per.get(cur)[0].push(line.slice(1));
    else if (cur && line.startsWith('+')) per.get(cur)[1].push(line.slice(1));
  }
  for (const f of git('ls-files', '--others', '--exclude-standard', '--', 'frontend/src').stdout.toString('utf8').split('\n').filter(Boolean)) per.set(f, [[], readFileSync(join(ROOT, f), 'utf8').split('\n')]);
  const spreads = (lines) => { const c = new Map(); for (const l of lines) for (const m of l.matchAll(/\{\s*\.\.\./g)) { const s = l.slice(m.index, balancedEnd(l, m.index)).replace(/\s+/g, ''); c.set(s, (c.get(s) || 0) + 1); } return c; };
  const added = [];
  for (const [f, [rem, add]] of per) { const r = spreads(rem); for (const [s, n] of spreads(add)) if (n > (r.get(s) || 0)) added.push(`${f}: spread ${s.slice(0, 60)} on a changed line`); }
  assert.deepEqual(added, [], 'no new JSX/object spread on a changed line (props must be written out)');
} else console.log('frontend_module_layer: UNVERIFIABLE SPREAD_DIFF (not a git checkout)');

// ---- 8. outside the module layer -------------------------------------------------------------------------------------
const indexHtml = readFileSync(join(ROOT, 'frontend/index.html'), 'utf8');
const styles = [...indexHtml.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => createHash('sha256').update(m[1]).digest('hex').slice(0, 16));
assert.deepEqual(styles, MAP.index_html_style_sha16, 'frontend/index.html: only the pinned boot <style> block');
assert.equal(/\sstyle\s*=/.test(indexHtml), false, 'frontend/index.html: no style= attribute');
const publicList = readFileSync(join(ROOT, 'tools/build_public_candidate.py'), 'utf8');
const cssImports = [];
for (const file of [...jsxFiles(SRC), ...jsFiles(SRC)]) {
  for (const m of readFileSync(file, 'utf8').matchAll(/import\s+['"](\.{1,2}\/[^'"]+\.css)['"]/g)) {
    const target = relative(ROOT, join(dirname(file), m[1]));
    const dir = dirname(target); const base = target.slice(dir.length + 1);
    const listed = new RegExp(`"${dir.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')}":\\s*\\(([^)]*)\\)`).exec(publicList);
    if (!listed || !listed[1].includes(`"${base}"`)) cssImports.push(`${relative(ROOT, file)} imports ${target}, which the public package does not list`);
  }
}
assert.deepEqual(cssImports, [], 'every stylesheet imported from frontend/src is a listed package file');

// ---- 6. module map --------------------------------------------------------------------------------------------------
let names = 0;
for (const [page, entries] of Object.entries(MAP.pages)) {
  for (const entry of entries) {
    names++;
    if (entry.marker) { assert.ok((moduleTags.get(entry.file) || []).some((tag) => tag.includes(entry.marker)), `${page}: module "${entry.name}" (marker ${entry.marker}) has no module element in ${entry.file}`); continue; }
    assert.ok(found.has(entry.name), `${page}: module "${entry.name}" has no tg-mod / tg-block element in the JSX`);
    assert.ok(found.get(entry.name).has(entry.file), `${page}: module "${entry.name}" expected in ${entry.file}, found in ${[...found.get(entry.name)].join(', ')}`);
  }
}

console.log(JSON.stringify({ status: 'PASS', css_rules: rules.length, map_version: MAP.version, modules_checked: names, module_elements_in_jsx: found.size }));
