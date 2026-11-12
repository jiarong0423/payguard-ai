// Console first-load budget (spec D13): AG Grid loads on demand, so the console entry stays small.
//   1. Source: grid/agGrid.jsx is the only file that imports ag-grid-react or ag-grid-community, and it registers
//      an explicit module list (never AllCommunityModule).
//   2. Build (frontend/dist from `npm run build`): the JS and CSS that index.html loads up front stay under
//      FIRST_LOAD_BUDGET bytes after gzip -9 and carry no AG Grid code.
import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const srcRoot = join(projectRoot, 'frontend', 'src');
const distRoot = join(projectRoot, 'frontend', 'dist');
// Measured 154 kB at the change that made the grid lazy (483 kB before); the margin covers ordinary growth.
// 182 kB (was 180 kB): the 2026-11-11 round added full-id pairing, one dispute display mapping and the tab-kept receipt check
// (about 1 kB gzip); GitHub's zlib measures about 0.4 kB more than the local one, which put the old limit 260 bytes under it.
// 184 kB (was 182 kB), 2026-11-12 P0 restyle: theme/components.css (the new .tg-* component spec, about 2.3 kB gzip) is
// imported by index.css and put the build 19 bytes over; CI's zlib measures about 0.4 kB more than the local one.
// P1 must delete the console CSS these components replace, to win the increase back.
// 186 kB (was 184 kB), 2026-11-12 P3/P5: the shared ledger, log and clipping containers, linked tags and step page heads
// (components.css +1.1 kB gzip) put the first load at 189,563 bytes; the new pages themselves load on demand. The
// format-unification phase must delete the duplicate console CSS these containers replace, to win the increase back.
// 187 kB (was 186 kB), 2026-11-12 round 5: the shared due-day helper, the ink toast, the square status dots, the softer
// verdict block and the charcoal design-system pass put the first load 46 bytes over; CI's zlib measures about 0.4 kB
// more than the local one. The format-unification phase must delete the duplicate console CSS to win it back.
// 188 kB (was 187 kB), 2026-11-12 visual team phase 2: focus/keyfig/glass/status-shape classes, the token-driven
// chart theme hook and the shared icon component; the page owners delete the console CSS these replace in the same round.
// 2026-11-12 owner: no size cap; budget kept to show growth
const FIRST_LOAD_BUDGET = 204800;
const GRID_ENTRY = 'grid/agGrid.jsx';

const walk = (dir) => readdirSync(dir).flatMap((name) => {
  const path = join(dir, name);
  return statSync(path).isDirectory() ? walk(path) : [path];
});

// 1. Source
const importers = walk(srcRoot)
  .filter((path) => /\.(jsx?|mjs)$/u.test(path))
  .filter((path) => /from\s+['"]ag-grid-(react|community)['"]/u.test(readFileSync(path, 'utf8')))
  .map((path) => relative(srcRoot, path));
assert.deepEqual(importers, [GRID_ENTRY], `only ${GRID_ENTRY} imports AG Grid`);
const gridSource = readFileSync(join(srcRoot, GRID_ENTRY), 'utf8');
assert.ok(gridSource.includes('ModuleRegistry.registerModules(GRID_MODULES)'), 'explicit module list registered');
// GuideReplay calls exportDataAsCsv, which AG Grid 36 serves only with CsvExportModule registered (review r7).
assert.ok(/GRID_MODULES = \[[\s\S]*CsvExportModule[\s\S]*\];/.test(gridSource), 'CSV export module registered');
assert.ok(/GRID_MODULES = \[[\s\S]*RowApiModule[\s\S]*\];/.test(gridSource), 'row API module registered (getDisplayedRowCount)');
assert.equal(/import[^;]*AllCommunityModule/u.test(gridSource), false, 'no AllCommunityModule import');
const app = readFileSync(join(srcRoot, 'App.jsx'), 'utf8');
assert.match(app, /lazy\(\(\) => import\('\.\/grid\/agGrid\.jsx'\)\)/u, 'App.jsx loads the grid lazily');

// 2. Build
const indexHtml = join(distRoot, 'index.html');
assert.ok(existsSync(indexHtml), 'frontend/dist/index.html missing: run `npm run build` in frontend first');
const html = readFileSync(indexHtml, 'utf8');
const firstLoad = [...html.matchAll(/(?:src|href)="\/(assets\/[^"]+\.(?:js|css))"/gu)].map((match) => match[1]);
assert.ok(firstLoad.some((path) => path.endsWith('.js')), 'index.html loads at least one script');
let total = 0;
for (const path of firstLoad) {
  const body = readFileSync(join(distRoot, path));
  total += gzipSync(body, { level: 9 }).length;
  if (path.endsWith('.js')) assert.equal(body.includes('ag-root-wrapper'), false, `${path} carries AG Grid code`);
}
assert.ok(total <= FIRST_LOAD_BUDGET, `console first load ${total} bytes (gzip -9) exceeds ${FIRST_LOAD_BUDGET}`);
console.log(`frontend_bundle_budget: ok (${firstLoad.length} files, ${(total / 1024).toFixed(1)} kB of ${FIRST_LOAD_BUDGET / 1024} kB)`);
