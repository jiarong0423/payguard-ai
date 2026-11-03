// Regenerates theme/tokens.css from theme/tokens.js: node frontend/src/theme/writeTokensCss.mjs
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { tokensCss } from './tokens.js';

const target = fileURLToPath(new URL('./tokens.css', import.meta.url));
writeFileSync(target, tokensCss());
console.log(`wrote ${target}`);
