// Bryntum Scheduler gateway for the console (evidence deadline board, optional time evidence timeline).
//
// @bryntum/scheduler-community and its React wrapper are pinned dependencies of this project
// (exact versions in package.json and package-lock.json). This Vite plugin is the only place that
// imports them: it writes `virtual:payguard-optional-timeline`, which re-exports Scheduler and
// BryntumScheduler. If the packages are missing from node_modules the virtual module is a stub and
// the console falls back to its plain lists.
//
// Only the MIT-licensed Community tier is accepted. The build stops when package.json or the lock
// file declares a Bryntum trial, Business, Enterprise or other non-MIT package, or when an installed
// Bryntum package does not declare MIT.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const BRYNTUM_PACKAGE = '@bryntum/scheduler-community';
export const BRYNTUM_REACT_PACKAGE = '@bryntum/scheduler-react-community';
export const BRYNTUM_IMPORTED_PACKAGES = [BRYNTUM_PACKAGE, BRYNTUM_REACT_PACKAGE];
export const BRYNTUM_LICENSE = 'MIT';
export const VIRTUAL_ID = 'virtual:payguard-optional-timeline';
export const BUILD_FLAG = '__PAYGUARD_BRYNTUM_TIMELINE__';
const RESOLVED_ID = `\0${VIRTUAL_ID}`;
const DEPENDENCY_FIELDS = ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies'];
const EXACT_VERSION = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/u;
// Loaded with the Bryntum chunk only, so the console's first load gets no extra CSS.
export const TIMELINE_CSS = fileURLToPath(new URL('./timeline.css', import.meta.url));

export function isCommunityName(name) {
  return typeof name === 'string' && /^@bryntum\/[a-z-]+-community$/u.test(name)
    && !/(?:^|-)(?:trial|business|enterprise)(?:-|$)/u.test(name.slice('@bryntum/'.length));
}

// Returns a list of violations for the declared Bryntum packages; empty means MIT Community only.
export function auditBryntumDeclarations(manifest, lock) {
  const problems = [];
  for (const field of DEPENDENCY_FIELDS) {
    for (const [name, version] of Object.entries(manifest?.[field] || {})) {
      if (!name.startsWith('@bryntum/')) continue;
      if (!isCommunityName(name)) problems.push(`NOT_COMMUNITY_TIER:${name}`);
      if (!EXACT_VERSION.test(String(version))) problems.push(`VERSION_NOT_PINNED:${name}@${version}`);
    }
  }
  for (const [key, entry] of Object.entries(lock?.packages || {})) {
    const index = key.lastIndexOf('node_modules/@bryntum/');
    if (index === -1) continue;
    const name = key.slice(index + 'node_modules/'.length);
    if (!isCommunityName(name)) problems.push(`NOT_COMMUNITY_TIER:${name}`);
    if (entry?.license !== BRYNTUM_LICENSE) problems.push(`LICENSE_NOT_MIT:${name}:${entry?.license ?? 'NONE'}`);
  }
  return problems;
}

function readJson(path) {
  try { return JSON.parse(readFileSync(path, 'utf8')); } catch { return null; }
}

// Returns { installed, reason, version } for the imported packages seen from `root`.
export function detectBryntum(root) {
  const require = createRequire(join(root, 'package.json'));
  let version = null;
  for (const name of BRYNTUM_IMPORTED_PACKAGES) {
    let manifestPath;
    try {
      manifestPath = require.resolve(`${name}/package.json`);
    } catch {
      return { installed: false, reason: 'NOT_INSTALLED', version: null };
    }
    const manifest = readJson(manifestPath);
    if (!manifest) return { installed: false, reason: 'MANIFEST_UNREADABLE', version: null };
    if (manifest.name !== name || manifest.license !== BRYNTUM_LICENSE) {
      return { installed: false, reason: 'LICENSE_NOT_MIT_COMMUNITY', version: manifest.version ?? null };
    }
    if (name === BRYNTUM_PACKAGE) version = manifest.version ?? null;
  }
  return { installed: true, reason: 'MIT_COMMUNITY_TIER', version };
}

export function virtualModuleSource(installed) {
  if (!installed) return 'export const Scheduler = null;\nexport const BryntumScheduler = null;\nexport const available = false;\n';
  return [
    // Local Font Awesome from the MIT core package, so Bryntum never falls back to a CDN.
    "import '@bryntum/core-community/fontawesome/css/fontawesome.css';",
    "import '@bryntum/core-community/fontawesome/css/solid.css';",
    `import '${BRYNTUM_PACKAGE}/scheduler.css';`,
    `import '${BRYNTUM_PACKAGE}/stockholm-light.css';`,
    `import ${JSON.stringify(TIMELINE_CSS)};`,
    `export { Scheduler } from '${BRYNTUM_PACKAGE}';`,
    `export { BryntumScheduler } from '${BRYNTUM_REACT_PACKAGE}';`,
    'export const available = true;',
    '',
  ].join('\n');
}

function readDeclarations(root) {
  return { manifest: readJson(join(root, 'package.json')), lock: readJson(join(root, 'package-lock.json')) };
}

export default function optionalBryntumTimeline({ root = process.cwd(), detect = detectBryntum, declarations = readDeclarations } = {}) {
  const { manifest, lock } = declarations(root);
  const problems = auditBryntumDeclarations(manifest, lock);
  if (problems.length) throw new Error(`Bryntum licence guard: only the MIT Community tier is allowed (${problems.join(', ')})`);
  const state = detect(root);
  if (state.reason === 'LICENSE_NOT_MIT_COMMUNITY') throw new Error(`Bryntum licence guard: installed ${BRYNTUM_PACKAGE} does not declare MIT`);
  return {
    name: 'payguard-bryntum-community',
    config() {
      return { define: { [BUILD_FLAG]: JSON.stringify(state.installed) } };
    },
    configResolved(config) {
      const note = state.installed
        ? `Bryntum Scheduler: on (${BRYNTUM_PACKAGE}@${state.version}, MIT Community tier)`
        : `Bryntum Scheduler: off (${state.reason}); the board falls back to its list`;
      config.logger.info(note);
    },
    resolveId(id) {
      return id === VIRTUAL_ID ? RESOLVED_ID : null;
    },
    load(id) {
      return id === RESOLVED_ID ? virtualModuleSource(state.installed) : null;
    },
  };
}
