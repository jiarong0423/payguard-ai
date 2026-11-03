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
const FIRST_LOAD_BUDGET = 180 * 1024;
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
