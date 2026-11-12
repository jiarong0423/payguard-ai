// (vteam icon 2026-11-12) The shared icon sprite stays what the Phosphor files and theme/iconMap.js say it is.
//   1. build-sprite.mjs --check passes: sprite.svg equals what the single files give, and every value in the icon maps
//      (FOCUS, STEP, STATUS, ROLE, ACTION, SOURCE, LEGACY) is a sprite name.
//   2. The 23 files added on 2026-11-12 are byte-for-byte the Phosphor core files (commit 2b75f3ad, assets/regular).
//   3. The sprite is a separate asset (?no-inline), symbols are path data only, the licence is beside them.
//   4. Negative: on a copy, a map value that is not in the sprite, a sprite name with no file, and an edited sprite
//      each make --check exit non-zero with an ERROR line.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const themeRoot = join(projectRoot, 'frontend', 'src', 'theme');
const iconsRoot = join(themeRoot, 'icons');
const script = join(iconsRoot, 'build-sprite.mjs');

const runCheck = (path) => spawnSync(process.execPath, [path, '--check'], { encoding: 'utf8' });

// 1. The real tree passes.
const real = runCheck(script);
assert.equal(real.status, 0, `build-sprite --check failed: ${real.stderr.trim()}`);
assert.match(real.stdout, /^build-sprite: ok \(\d+ symbols, \d+ bytes\)/u);

// 2. Added files match the downloaded Phosphor files (sha256 recorded at download, scratchpad/icons_quarantine/manifest.tsv).
// Source: https://raw.githubusercontent.com/phosphor-icons/core/2b75f3ad12b420c9504ef05df8d2564a28f8500e/assets/regular/<name>.svg
const ADDED = [
  ['arrow-u-down-left', '55fcf6036cc0192eb2b4f96911c660f3fccc422a88274f893d41568a17b387d7'],
  ['arrows-clockwise', '2e80fbc9c5c37553934c9ebbd6324bf7fabe9a4b4d7c2445d99edfce55cc22df'],
  ['buildings', '76f3325b87588fc6786953e8b964d5b7cae58983b3dc1399f7b7a672a6c1b553'],
  ['check', 'cbb89a8c42f283d4f846eb935e05d88c1be04462f16480e068c0f82b9ce40b12'],
  ['cloud-check', 'd9b0bdd1047bb0bee3c0436f2b14ccc0f35c377c3cff57ae0ac0e356303642e5'],
  ['copy', '5a892fc6a72866e60c67db2088a87653cf44b57b1a5d183b36e950cdc5dd66b3'],
  ['database', 'da7d3598430cbe3b334c308c03ca41e8c4c7bbbfa7891e914d7aa8e87d847423'],
  ['dot-outline', '1c99dafbc881699a083da5367f3e5cd73bc6783a83d5fae3b6611458c76c2253'],
  ['flask', '6fe1929c860962cadddc917a3d119145444537ccaee6a9d618e7d856c16f8501'],
  ['lightning', '3a50c776266b21812f8ec5b5a841a81f54aa942569a31eb03a36fb0a5bfbe66e'],
  ['link-simple', '7a97dad4b2f16c3a386ea69ba78d29bf3a71c311f2e34100d79143559ba13151'],
  ['lock-simple', 'b99d3713ac86cb610eb66974d69de2aa1223c4f6387fb1053e3d375e62f5dc1c'],
  ['note-pencil', '85f05d1a02f8d808ca9b023e765e7dec7ec2d706313dddf464010f35c9469264'],
  ['paper-plane-tilt', '0dbff2ada31c963dfd95bfe2ab2cb39a90fe7100eb7c1724577444a1d8a7c26d'],
  ['play', '885b3ed2095889c4ff063dac35dc424cb9f6c00273ab44e2f90dc9dadbee661a'],
  ['plugs-connected', 'cca84487a9a3b1a3c413576efe1fc400f119cfff59bcc5fc336e5b3d8e1788ea'],
  ['stack', 'ee9eaaeb345e8a28c9662cf8a59147cb86080bd922e41f143444189e0116ea7e'],
  ['storefront', 'b1e1288fc8b38ddf011dfc23a5f1754d30c296a56d143c67b4ed710ff58d8a62'],
  ['test-tube', '1abc795b2c617d3a829024765aae29055bf783357c5471a0feea806e1d4662ce'],
  ['user', '787434f7fef95f20e137d309d3c6b8b471548c55c9dfc137ae10625d70959d11'],
  ['user-check', '39b6cda4c963ef987a4998a9c9becb2e5edcacb327346b44b2b945f11e1f93e8'],
  ['warning-octagon', '47db99799b11ee693baa8437f3cd1122f844b2dc28ec8abaafc3ca572cb9c35a'],
  ['x', '7397b15e1fa66eaf6ff9b59fe91d483cb5c3bcf75b2fe052097ab6f0593b513a'],
];
assert.equal(ADDED.length, 23, '23 added Phosphor files');
for (const [name, sha] of ADDED) {
  const file = join(iconsRoot, `${name}.svg`);
  assert.ok(existsSync(file), `${name}.svg present`);
  assert.equal(createHash('sha256').update(readFileSync(file)).digest('hex'), sha, `${name}.svg is the Phosphor file`);
}

// 3. Shape of the sprite and the map.
const sprite = readFileSync(join(iconsRoot, 'sprite.svg'), 'utf8');
assert.ok(!/<script|href=|url\(|\son[a-z]+=|<foreignObject|<style/iu.test(sprite), 'sprite holds no script, link or style');
const symbols = [...sprite.matchAll(/<symbol id="ph-([a-z0-9-]+)" viewBox="0 0 256 256">(.*?)<\/symbol>/gu)];
const mapSource = readFileSync(join(themeRoot, 'iconMap.js'), 'utf8');
const names = [...mapSource.match(/export const SPRITE_NAMES = \[([\s\S]*?)\];/u)[1].matchAll(/'([a-z0-9-]+)'/gu)].map((m) => m[1]);
assert.deepEqual(symbols.map((m) => m[1]), names, 'one symbol per SPRITE_NAMES entry, in order');
for (const [, name, body] of symbols) assert.match(body, /^(<path d="[^"<>]+"\/>)+$/u, `${name}: path data only`);
for (const [name] of ADDED) assert.ok(names.includes(name), `${name} is in the sprite`);
assert.ok(mapSource.includes("from './icons/sprite.svg?no-inline'"), 'sprite imported as a separate asset (<use href> cannot use a data URL)');
assert.ok(readFileSync(join(iconsRoot, 'LICENSE'), 'utf8').startsWith('MIT License'), 'Phosphor MIT licence beside the icons');

// 4. Negative cases on a throwaway copy of theme/.
function negative(label, mutate, expected) {
  const dir = mkdtempSync(join(tmpdir(), 'icon-sprite-'));
  try {
    cpSync(join(themeRoot, 'iconMap.js'), join(dir, 'iconMap.js'));
    cpSync(iconsRoot, join(dir, 'icons'), { recursive: true });
    mutate(dir);
    const result = runCheck(join(dir, 'icons', 'build-sprite.mjs'));
    assert.notEqual(result.status, 0, `${label}: --check must fail`);
    assert.match(result.stderr, /^ERROR build-sprite: /mu, `${label}: grep-able ERROR line`);
    assert.match(result.stderr, expected, `${label}: names the problem`);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}
const edit = (path, from, to) => {
  const text = readFileSync(path, 'utf8');
  assert.ok(text.includes(from), `fixture text "${from}" present`);
  writeFileSync(path, text.replace(from, to));
};
negative('unknown map value', (dir) => edit(join(dir, 'iconMap.js'), "close: 'x',", "close: 'no-such-icon',"), /ACTION uses "no-such-icon"/u);
negative('sprite name without a file', (dir) => edit(join(dir, 'iconMap.js'), "'arrow-right', ", "'arrow-right', 'no-such-icon', "), /no-such-icon\.svg missing/u);
negative('edited sprite', (dir) => edit(join(dir, 'icons', 'sprite.svg'), 'id="ph-user"', 'id="ph-user2"'), /sprite\.svg is out of date/u);

console.log(`frontend_icon_sprite: ok (${names.length} symbols, ${ADDED.length} added files verified, 3 negative cases)`);
