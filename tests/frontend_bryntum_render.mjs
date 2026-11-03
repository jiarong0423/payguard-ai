// Render proof for the Bryntum timeline (MIT Community tier, a pinned dependency since the evidence
// deadline board). Skipped when the package is not installed (before npm ci) or Playwright is absent.
// It builds a small harness around TimeEvidenceWithTimeline, feeds it the
// real backend time evidence for synthetic case case-ref-002, opens it in headless Chromium
// and checks the Bryntum DOM. Set PAYGUARD_RENDER_SCREENSHOT=<path.png> to keep a screenshot.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { BRYNTUM_PACKAGE, detectBryntum } from '../frontend/src/optional/vitePlugin.js';
import { buildTimelineModel } from '../frontend/src/optional/timelineModel.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');
const optionalRoot = join(frontendRoot, 'src', 'optional');

function skip(reason) {
  console.log(`frontend_bryntum_render: SKIP (${reason})`);
  process.exit(0);
}

const bryntum = detectBryntum(frontendRoot);
if (!bryntum.installed) skip(`${BRYNTUM_PACKAGE} ${bryntum.reason}`);

let chromium;
try {
  ({ chromium } = createRequire(import.meta.url)('playwright'));
} catch {
  skip('playwright is not available');
}

// 1. Real backend time evidence for case-ref-002 (synthetic data, fixed clock, no provider calls).
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');
const pythonProgram = String.raw`
import json
from datetime import datetime, timezone
from fastapi.testclient import TestClient
import httpx
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore

now = datetime(2026, 10, 8, 8, 0, tzinfo=timezone.utc)
def reject_provider_call(request):
    raise AssertionError("provider call forbidden")
store = SessionStore(clock=lambda: now)
provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(reject_provider_call), clock=lambda: now)
with TestClient(create_app(store=store, paypal=provider), base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001)) as client:
    origin = "http://localhost:5173"
    root = "/api/v1"
    session = client.post(root + "/demo/sessions", json={}, headers={"Origin": origin}).json()
    headers = {"Origin": origin, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
    assert client.post(root + "/demo/inject", json={"scenario": "dispute"}, headers=headers).status_code == 200
    draft = client.post(root + "/disputes/case-ref-002/draft", json={}, headers=headers)
    assert draft.status_code == 200, draft.text
    print(json.dumps(draft.json()["time_evidence"], sort_keys=True))
`;
const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${join(projectRoot, 'src')}:${join(projectRoot, 'backend')}` },
  encoding: 'utf8',
  maxBuffer: 2 * 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const evidence = JSON.parse(generated.stdout.trim());
const model = buildTimelineModel(evidence);
assert.ok(model, 'TIME_EVIDENCE_NOT_DRAWABLE');

// 2. Harness build inside frontend/node_modules/.cache so React, Vite and Bryntum resolve
//    from the frontend install. Nothing here is committed; the directory is removed at the end.
const cacheRoot = join(frontendRoot, 'node_modules', '.cache');
mkdirSync(cacheRoot, { recursive: true });
const harness = mkdtempSync(join(cacheRoot, 'payguard-bryntum-render-'));
const server = createServer();
let browser;
try {
  writeFileSync(join(harness, 'index.html'), '<!doctype html><html><head><meta charset="utf-8"><title>render check</title></head><body style="margin:0;background:#0b1626"><div id="root" style="width:1180px;padding:24px"></div><script type="module" src="./main.jsx"></script></body></html>\n');
  writeFileSync(join(harness, 'main.jsx'), [
    "import { createRoot } from 'react-dom/client';",
    // Same AG Grid registration as App.jsx: the time evidence view's table needs the community modules.
    "import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';",
    'ModuleRegistry.registerModules([AllCommunityModule]);',
    `import '${join(frontendRoot, 'src', 'index.css')}';`,
    `import TimeEvidenceWithTimeline from '${join(optionalRoot, 'TimeEvidenceWithTimeline.jsx')}';`,
    `const evidence = ${JSON.stringify(evidence)};`,
    "createRoot(document.getElementById('root')).render(<TimeEvidenceWithTimeline evidence={evidence} />);",
    '',
  ].join('\n'));
  writeFileSync(join(harness, 'vite.config.mjs'), [
    "import react from '@vitejs/plugin-react';",
    "import tailwindcss from '@tailwindcss/vite';",
    `import optionalBryntumTimeline from '${join(optionalRoot, 'vitePlugin.js')}';`,
    'export default {',
    `  root: ${JSON.stringify(harness)},`,
    "  logLevel: 'warn',",
    `  plugins: [react(), tailwindcss(), optionalBryntumTimeline({ root: ${JSON.stringify(frontendRoot)} })],`,
    `  build: { outDir: ${JSON.stringify(join(harness, 'dist'))}, emptyOutDir: true, chunkSizeWarningLimit: 4000 },`,
    '};',
    '',
  ].join('\n'));
  const viteBin = join(frontendRoot, 'node_modules', 'vite', 'bin', 'vite.js');
  const built = spawnSync(process.execPath, [viteBin, 'build', '--config', join(harness, 'vite.config.mjs')], { cwd: harness, encoding: 'utf8' });
  assert.equal(built.status, 0, built.stderr || built.stdout);

  // 3. Serve the build on 127.0.0.1 only.
  const dist = join(harness, 'dist');
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.svg': 'image/svg+xml' };
  server.on('request', (request, response) => {
    const path = normalize(join(dist, decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname)));
    const file = path === dist || path === `${dist}${sep}` ? join(dist, 'index.html') : path;
    if (!file.startsWith(dist) || !existsSync(file)) { response.writeHead(404).end(); return; }
    response.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' }).end(readFileSync(file));
  });
  await new Promise((done) => server.listen(0, '127.0.0.1', done));
  const origin = `http://127.0.0.1:${server.address().port}`;

  // 4. Headless Chromium: the Bryntum timeline renders the same records as the list.
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1240, height: 900 } });
  const problems = [];
  page.on('pageerror', (error) => problems.push(`pageerror ${error}`));
  page.on('console', (message) => { if (['error', 'warning'].includes(message.type())) problems.push(`${message.type()} ${message.text()}`); });
  page.on('request', (request) => { if (!request.url().startsWith(origin)) problems.push(`external ${request.url()}`); });
  await page.goto(origin, { waitUntil: 'networkidle' });
  const timeline = page.locator('[data-testid="time-evidence-timeline"][data-state="ready"]');
  await timeline.waitFor({ timeout: 20000 });
  // The time evidence view opens on its AG Grid table (a8f305b); the ordered list this test compares
  // with the Bryntum milestones is the "Timeline" view.
  await page.getByTestId('time-evidence-view-timeline').click();
  await page.waitForTimeout(500);

  const rendered = await page.evaluate(() => ({
    listItems: document.querySelectorAll('[data-testid="time-evidence"] .time-event').length,
    schedulers: document.querySelectorAll('[data-testid="time-evidence-timeline"] .b-scheduler').length,
    rows: [...document.querySelectorAll('[data-testid="time-evidence-timeline"] .b-grid-sub-grid-locked .b-grid-row')].map((row) => row.textContent.trim()),
    milestones: [...document.querySelectorAll('[data-testid="time-evidence-timeline"] .b-sch-event-wrap')].map((node) => node.textContent.trim()),
    header: document.querySelector('[data-testid="time-evidence-timeline"] .b-sch-header-row-0')?.textContent ?? '',
  }));
  assert.equal(rendered.listItems, evidence.events.length, 'LIST_CHANGED');
  assert.equal(rendered.schedulers, 1, 'SCHEDULER_NOT_RENDERED');
  assert.deepEqual(rendered.rows, model.resources.map((row) => row.name), 'TIMELINE_ROWS');
  assert.equal(rendered.milestones.length, model.events.length, 'MILESTONE_COUNT');
  assert.deepEqual([...rendered.milestones].sort(), model.events.map((event) => event.name).sort(), 'MILESTONE_LABELS');
  assert.ok(rendered.header.length > 0, 'TIME_AXIS_HEADER_EMPTY');
  assert.deepEqual(problems, [], 'BROWSER_PROBLEMS');

  if (process.env.PAYGUARD_RENDER_SCREENSHOT) {
    await page.locator('#root').screenshot({ path: resolve(process.env.PAYGUARD_RENDER_SCREENSHOT) });
  }
  console.log(`frontend_bryntum_render: ok (${BRYNTUM_PACKAGE}@${bryntum.version} MIT; ${rendered.rows.length} rows, ${rendered.milestones.length} milestones, ${rendered.listItems} list items, header "${rendered.header.trim()}")`);
} finally {
  if (browser) await browser.close();
  server.close();
  rmSync(harness, { recursive: true, force: true });
}
