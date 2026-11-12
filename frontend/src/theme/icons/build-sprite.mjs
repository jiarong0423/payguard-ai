// (vteam icon 2026-11-12) Builds theme/icons/sprite.svg from the single Phosphor files in this folder.
// The list of names is SPRITE_NAMES in theme/iconMap.js, so the sprite and the map cannot drift apart.
//   node frontend/src/theme/icons/build-sprite.mjs           write sprite.svg
//   node frontend/src/theme/icons/build-sprite.mjs --check   exit 1 if sprite.svg is not what the files give
// Each file must be one Phosphor Regular svg: viewBox 0 0 256 256, fill currentColor, only <path d="..."> inside.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const check = process.argv.includes('--check');

function fail(message) {
  console.error(`ERROR build-sprite: ${message}`);
  process.exit(1);
}

let mapSource;
try {
  mapSource = readFileSync(join(here, '..', 'iconMap.js'), 'utf8');
} catch (error) {
  fail(`cannot read iconMap.js (${error.message})`);
}
const listMatch = mapSource.match(/export const SPRITE_NAMES = \[([\s\S]*?)\];/u);
if (!listMatch) fail('SPRITE_NAMES not found in iconMap.js');
const names = [...listMatch[1].matchAll(/'([a-z0-9-]+)'/gu)].map((m) => m[1]);
if (names.length === 0) fail('SPRITE_NAMES is empty');
if (new Set(names).size !== names.length) fail('SPRITE_NAMES has a duplicate');

// Every icon name the maps hand out must be in the sprite.
const known = new Set(names);
const mapBlocks = [...mapSource.matchAll(/export const (FOCUS|STEP|STATUS|ROLE|ACTION|SOURCE|LEGACY) = \{([\s\S]*?)\};/gu)];
if (mapBlocks.length !== 7) fail(`expected 7 icon maps in iconMap.js, found ${mapBlocks.length}`);
for (const [, mapName, body] of mapBlocks) {
  for (const value of body.matchAll(/:\s*'([a-z0-9-]+)'/gu)) {
    if (!known.has(value[1])) fail(`${mapName} uses "${value[1]}", which is not in SPRITE_NAMES`);
  }
}

const HEAD ='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor">';
const symbols = names.map((name) => {
  const file = join(here, `${name}.svg`);
  if (!existsSync(file)) fail(`${name}.svg missing`);
  const text = readFileSync(file, 'utf8').trim();
  if (!text.startsWith(HEAD) || !text.endsWith('</svg>')) fail(`${name}.svg is not a Phosphor Regular file`);
  const body = text.slice(HEAD.length, -'</svg>'.length);
  if (!/^(<path d="[^"<>]+"\/>)+$/u.test(body)) fail(`${name}.svg holds more than path data`);
  return `<symbol id="ph-${name}" viewBox="0 0 256 256">${body}</symbol>`;
});

// Phosphor Icons, MIT licence (see LICENSE in this folder).
const sprite = `<svg xmlns="http://www.w3.org/2000/svg"><!-- Phosphor Icons Regular, MIT (theme/icons/LICENSE). Built by build-sprite.mjs; do not edit. -->\n${symbols.join('\n')}\n</svg>\n`;
const target = join(here, 'sprite.svg');

if (check) {
  const current = existsSync(target) ? readFileSync(target, 'utf8') : '';
  if (current !== sprite) fail('sprite.svg is out of date: run node frontend/src/theme/icons/build-sprite.mjs');
  console.log(`build-sprite: ok (${names.length} symbols, ${Buffer.byteLength(sprite)} bytes)`);
} else {
  writeFileSync(target, sprite);
  console.log(`build-sprite: wrote sprite.svg (${names.length} symbols, ${Buffer.byteLength(sprite)} bytes)`);
}
