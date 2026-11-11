// theme/connect.js contract (ui_mock/CONTAINER_SPEC.md, "linked tags"): exports initConnect / elbowPath / pathLength,
// has no imports, no network and no timers of its own, honours prefers-reduced-motion, and draws right-angle paths.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import * as connect from '../frontend/src/theme/connect.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = readFileSync(join(root, 'frontend/src/theme/connect.js'), 'utf8');
const code = source.replace(/\/\/.*$/gm, '');

// 1. Exports and dependency-free source.
assert.deepEqual(Object.keys(connect).sort(), ['elbowPath', 'initConnect', 'pathLength']);
assert.equal(typeof connect.initConnect, 'function');
assert.equal(/^\s*import\s/m.test(code) || /\brequire\(/.test(code) || /\bimport\(/.test(code), false, 'no imports');
assert.equal(/\bfetch\(|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage|setInterval|eval\(|new Function/.test(code), false, 'no network, storage, timers or eval');
assert.match(code, /prefers-reduced-motion: reduce/, 'checks reduced motion');
assert.match(code, /addEventListener\('resize'/, 'redraws on resize');
assert.match(code, /focusin/, 'keyboard focus triggers');
assert.match(code, /'click'/, 'tap toggles');

// 2. No DOM: initConnect is a safe no-op that returns a disposer.
assert.equal(typeof connect.initConnect(null), 'function');
assert.equal(typeof connect.initConnect({ querySelectorAll: () => [] }, { win: null }), 'function');

// 3. Right-angle geometry: neighbours only, 4px off the outline, edge midpoints, one turn at most.
const a = { left: 0, top: 0, width: 100, height: 20 };
const sameRow = connect.elbowPath(a, { left: 200, top: 5, width: 80, height: 20 });
assert.equal(sameRow.d, 'M104 13H196', 'overlapping rows: one horizontal line');
const sameCol = connect.elbowPath(a, { left: 20, top: 200, width: 100, height: 40 });
assert.equal(sameCol.d, 'M60 24V196', 'overlapping columns: one vertical line');
const diag = connect.elbowPath(a, { left: 200, top: 100, width: 80, height: 20 });
assert.equal(diag.d, 'M104 10H240V96', 'horizontal first by default');
assert.deepEqual([diag.start, diag.end], [{ x: 104, y: 10 }, { x: 240, y: 96 }]);
const avoid = connect.elbowPath(a, { left: 200, top: 100, width: 80, height: 20 }, [{ left: 150, top: 0, width: 40, height: 30 }]);
assert.equal(avoid.d, 'M50 24V110H196', 'switches to vertical first when the default crosses another highlighted box');
for (const p of [sameRow, sameCol, diag, avoid]) assert.equal(/[LCQA]/.test(p.d), false, 'only horizontal and vertical segments');
assert.equal(connect.pathLength(diag.d), 136 + 86);
assert.equal(connect.pathLength(avoid.d), 86 + 146);

// 4. Styles exist for every class the module writes.
const css = readFileSync(join(root, 'frontend/src/theme/components.css'), 'utf8');
for (const cls of ['.tg-connect', '.tg-connect--risk', '.tg-connect.is-drawing', '.is-linked', '.tg-tag']) assert.ok(css.includes(cls), `${cls} is styled`);

console.log(JSON.stringify({ status: 'PASS', exports: Object.keys(connect).length }));
