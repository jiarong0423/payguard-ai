// Bryntum gateway and optional timeline: pinned MIT Community tier only, one import gateway, pure model.
// The board-specific contract is in tests/frontend_bryntum_board_contract.mjs.
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import optionalBryntumTimeline, {
  BRYNTUM_IMPORTED_PACKAGES, BRYNTUM_PACKAGE, BUILD_FLAG, VIRTUAL_ID, auditBryntumDeclarations, detectBryntum, virtualModuleSource,
} from '../frontend/src/optional/vitePlugin.js';
import { TIMELINE_LANES, buildTimelineModel, utcWallClock, viewPresetFor } from '../frontend/src/optional/timelineModel.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');

// 1. A pinned dependency: every declared or locked Bryntum package is the MIT Community tier.
const manifest = JSON.parse(readFileSync(join(frontendRoot, 'package.json'), 'utf8'));
const lock = JSON.parse(readFileSync(join(frontendRoot, 'package-lock.json'), 'utf8'));
for (const name of BRYNTUM_IMPORTED_PACKAGES) assert.match(manifest.dependencies[name] ?? '', /^\d+\.\d+\.\d+/u, `${name} declared with an exact version`);
assert.deepEqual(auditBryntumDeclarations(manifest, lock), [], 'BRYNTUM_DECLARATIONS_NOT_MIT_COMMUNITY');
for (const field of ['devDependencies', 'optionalDependencies', 'peerDependencies']) {
  assert.deepEqual(Object.keys(manifest[field] || {}).filter((name) => name.startsWith('@bryntum/')), [], `BRYNTUM_DECLARED_IN_${field}`);
}

// 2. No source file imports Bryntum directly; only the virtual module may reach it.
function sourceFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) return sourceFiles(path);
    return /\.(jsx?|mjs|css)$/.test(entry.name) ? [path] : [];
  });
}
// vitePlugin.js is the one gateway: it writes the import lines for the virtual module.
const gateway = join(frontendRoot, 'src', 'optional', 'vitePlugin.js');
for (const path of sourceFiles(join(frontendRoot, 'src')).filter((path) => path !== gateway)) {
  const text = readFileSync(path, 'utf8');
  const direct = /(?:from\s+|import\s*\(\s*|import\s+|@import\s+)['"]@bryntum\//.test(text);
  assert.equal(direct, false, `DIRECT_BRYNTUM_IMPORT:${path}`);
}
assert.equal(readFileSync(join(frontendRoot, 'vite.config.js'), 'utf8').includes('@bryntum/'), false, 'BRYNTUM_IN_VITE_CONFIG');

// 3. Detection: missing package, commercial package and MIT Community package.
const scratch = mkdtempSync(join(tmpdir(), 'payguard-bryntum-'));
try {
  writeFileSync(join(scratch, 'package.json'), '{"name":"probe","private":true}');
  assert.deepEqual(detectBryntum(scratch), { installed: false, reason: 'NOT_INSTALLED', version: null });
  const probe = (name, license) => {
    const packageDir = join(scratch, 'node_modules', ...name.split('/'));
    mkdirSync(packageDir, { recursive: true });
    writeFileSync(join(packageDir, 'package.json'), JSON.stringify({ name, version: '0.0.0-probe', license }));
  };
  probe(BRYNTUM_PACKAGE, 'Commercial');
  assert.equal(detectBryntum(scratch).reason, 'LICENSE_NOT_MIT_COMMUNITY');
  assert.equal(detectBryntum(scratch).installed, false);
  probe(BRYNTUM_PACKAGE, 'MIT');
  assert.equal(detectBryntum(scratch).reason, 'NOT_INSTALLED', 'the React wrapper is required too');
  probe('@bryntum/scheduler-react-community', 'Commercial');
  assert.equal(detectBryntum(scratch).reason, 'LICENSE_NOT_MIT_COMMUNITY');
  probe('@bryntum/scheduler-react-community', 'MIT');
  assert.deepEqual(detectBryntum(scratch), { installed: true, reason: 'MIT_COMMUNITY_TIER', version: '0.0.0-probe' });
} finally {
  rmSync(scratch, { recursive: true, force: true });
}

// 4. Virtual module and plugin hooks for both states.
assert.equal(virtualModuleSource(false).includes('@bryntum/'), false);
assert.match(virtualModuleSource(false), /export const available = false;/);
assert.match(virtualModuleSource(true), /export \{ Scheduler \} from '@bryntum\/scheduler-community';/);
assert.match(virtualModuleSource(true), /export const available = true;/);
assert.match(virtualModuleSource(true), /export \{ BryntumScheduler \} from '@bryntum\/scheduler-react-community';/);
assert.match(virtualModuleSource(false), /export const BryntumScheduler = null;/);
for (const installed of [false, true]) {
  const plugin = optionalBryntumTimeline({ root: frontendRoot, detect: () => ({ installed, reason: 'PROBE', version: null }) });
  assert.deepEqual(plugin.config(), { define: { [BUILD_FLAG]: JSON.stringify(installed) } });
  const resolved = plugin.resolveId(VIRTUAL_ID);
  assert.ok(resolved.startsWith('\0'));
  assert.equal(plugin.resolveId('react'), null);
  assert.equal(plugin.load(resolved), virtualModuleSource(installed));
  assert.equal(plugin.load('/some/other/file.js'), null);
}

// 5. Pure model: lanes, zero-length milestones, UTC axis, bad input.
const evidence = {
  events: [
    { kind: 'PAYMENT', at: '2026-10-01T09:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
    { kind: 'ORDER_RECORD_CREATED', at: '2026-10-01T09:02:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
    { kind: 'DELIVERY', at: '2026-10-01T09:05:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
    { kind: 'MESSAGE', at: '2026-10-02T10:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED', channel: 'EMAIL', direction: 'INBOUND', topic: 'DELIVERY_NOTICE', message_digest: 'a'.repeat(64) },
    { kind: 'CLAIM_OPENED', at: '2026-10-04T12:00:00Z', source: 'PROVIDER' },
  ],
  gaps_seconds: {},
  flags: [],
};
const model = buildTimelineModel(evidence);
assert.deepEqual(model.resources.map((row) => row.id), TIMELINE_LANES.map(([id]) => id));
assert.equal(model.events.length, 5);
for (const event of model.events) assert.equal(event.startDate.getTime(), event.endDate.getTime());
assert.equal(model.events[3].name, 'Message record · Delivery notice');
assert.equal(model.events[0].name, 'Payment');
assert.ok(model.startDate < model.events[0].startDate && model.endDate > model.events[4].startDate);
assert.equal(model.viewPreset, 'dayAndWeek');
assert.equal(JSON.stringify(model).includes('a'.repeat(64)), false, 'MESSAGE_DIGEST_NOT_DRAWN');

const wall = utcWallClock('2026-10-01T09:05:00Z');
assert.deepEqual([wall.getFullYear(), wall.getMonth(), wall.getDate(), wall.getHours(), wall.getMinutes()], [2026, 9, 1, 9, 5]);
assert.equal(utcWallClock('not a time'), null);

const partial = buildTimelineModel({ events: [
  { kind: 'PAYMENT', at: '2026-10-01T09:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
  { kind: 'CLAIM_OPENED', at: '2026-10-01T09:30:00Z', source: 'PROVIDER' },
  { kind: 'UNKNOWN_KIND', at: '2026-10-01T09:10:00Z', source: 'PROVIDER' },
  { kind: 'DELIVERY', at: 'broken', source: 'SELLER_PROVIDED_UNVERIFIED' },
] });
assert.deepEqual(partial.resources.map((row) => row.id), ['PAYMENT', 'CLAIM_OPENED']);
assert.equal(partial.viewPreset, 'hourAndDay');
assert.equal(buildTimelineModel(null), null);
assert.equal(buildTimelineModel({}), null);
assert.equal(buildTimelineModel({ events: [] }), null);
assert.equal(viewPresetFor(200 * 24 * 3600 * 1000), 'monthAndYear');

// 6. The local install is the MIT Community tier (absent only before npm ci).
const local = detectBryntum(frontendRoot);
assert.ok(['NOT_INSTALLED', 'MIT_COMMUNITY_TIER'].includes(local.reason), `LOCAL_BRYNTUM_${local.reason}`);
if (local.installed) assert.equal(local.version, manifest.dependencies[BRYNTUM_PACKAGE], 'installed version matches the pin');
console.log(`frontend_optional_timeline: ok (pinned ${manifest.dependencies[BRYNTUM_PACKAGE]}; ${local.installed ? `installed ${local.version}` : 'not installed'})`);
