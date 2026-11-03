// Render proof for the evidence deadline board (step 03) in headless Chromium, with the real backend's
// synthetic cases. It mounts the board with one prepared draft and then adds the others, the way the
// console fills it as the seller prepares drafts, and checks that the Bryntum time axis still runs from
// the earliest event to the latest due date (round 5: it used to end before the last response window),
// that the due-soon case with a missing item is the one highlighted, that amounts are shown, and (optimise r24)
// that the seller's plan bars move in whole hours and refuse a drop before now.
// Skipped when the Bryntum package is not installed (before npm ci) or Playwright is absent.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { BRYNTUM_PACKAGE, detectBryntum } from '../frontend/src/optional/vitePlugin.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');

function skip(reason) {
  console.log(`frontend_bryntum_board_render: SKIP (${reason})`);
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

// 1. state.disputes and every draft from the real backend (synthetic data, current clock, no provider calls).
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');
const pythonProgram = String.raw`
import json
import httpx
from fastapi.testclient import TestClient
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore

def reject_provider_call(request):
    raise AssertionError("provider call forbidden")
provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(reject_provider_call))
with TestClient(create_app(store=SessionStore(), paypal=provider), base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001)) as client:
    origin = "http://localhost:5173"
    root = "/api/v1"
    session = client.post(root + "/demo/sessions", json={}, headers={"Origin": origin}).json()
    headers = {"Origin": origin, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
    state = client.post(root + "/demo/inject", json={"scenario": "dispute"}, headers=headers)
    assert state.status_code == 200, state.text
    drafts = {}
    for row in state.json()["disputes"]:
        draft = client.post(root + "/disputes/" + row["case_ref"] + "/draft", json={}, headers=headers)
        assert draft.status_code == 200, draft.text
        drafts[row["case_ref"]] = draft.json()
    disputes = client.get(root + "/demo/state", headers=headers).json()["disputes"]
    print(json.dumps({"disputes": disputes, "drafts": drafts}, sort_keys=True))
`;
const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${join(projectRoot, 'src')}:${join(projectRoot, 'backend')}` },
  encoding: 'utf8',
  maxBuffer: 4 * 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const { disputes, drafts } = JSON.parse(generated.stdout.trim());
assert.deepEqual(disputes.map((row) => row.case_ref), ['case-ref-001', 'case-ref-002', 'case-ref-003']);

// 2. Harness: first render with no draft at all (case data only, evloop), then all drafts.
const cacheRoot = join(frontendRoot, 'node_modules', '.cache');
mkdirSync(cacheRoot, { recursive: true });
const harness = mkdtempSync(join(cacheRoot, 'payguard-board-render-'));
const server = createServer();
let browser;
try {
  writeFileSync(join(harness, 'index.html'), '<!doctype html><html><head><meta charset="utf-8"><title>board render check</title></head><body style="margin:0"><div id="root" style="width:1376px;padding:24px"></div><script type="module" src="./main.jsx"></script></body></html>\n');
  writeFileSync(join(harness, 'main.jsx'), [
    "import { useEffect, useState } from 'react';",
    "import { createRoot } from 'react-dom/client';",
    `import '${join(frontendRoot, 'src', 'index.css')}';`,
    `import EvidenceBoard from '${join(frontendRoot, 'src', 'board', 'EvidenceBoard.jsx')}';`,
    `const disputes = ${JSON.stringify(disputes)};`,
    `const drafts = ${JSON.stringify(drafts)};`,
    'function Harness() {',
    '  const [held, setHeld] = useState({});',
    "  useEffect(() => { window.payguardShowDrafts = () => { setHeld(drafts); document.body.dataset.step = 'all'; }; document.body.dataset.step = 'none'; }, []);",
    '  return <EvidenceBoard disputes={disputes} drafts={held} />;',
    '}',
    "createRoot(document.getElementById('root')).render(<Harness />);",
    '',
  ].join('\n'));
  writeFileSync(join(harness, 'vite.config.mjs'), [
    "import react from '@vitejs/plugin-react';",
    "import tailwindcss from '@tailwindcss/vite';",
    `import optionalBryntumTimeline from '${join(frontendRoot, 'src', 'optional', 'vitePlugin.js')}';`,
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

  // 3. Desktop width, as in the report: the axis must hold every bar after the drafts are added.
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const problems = [];
  page.on('pageerror', (error) => problems.push(`pageerror ${error}`));
  page.on('console', (message) => { if (['error', 'warning'].includes(message.type())) problems.push(`${message.type()} ${message.text()}`); });
  page.on('request', (request) => { if (!request.url().startsWith(origin)) problems.push(`external ${request.url()}`); });
  await page.goto(origin, { waitUntil: 'networkidle' });
  await page.locator('[data-testid="evidence-board-timeline"] .b-scheduler').waitFor({ timeout: 20000 });
  // evloop: before any draft, the case data alone draws every response window, due line, the now line and a plan bar.
  await page.locator('body[data-step="none"]').waitFor({ timeout: 20000 });
  await page.waitForFunction(() => document.querySelectorAll('[data-testid="evidence-board-timeline"] .payguard-board-window').length === 3
    && document.querySelectorAll('[data-testid="evidence-board-timeline"] .payguard-board-plan').length === 3
    && document.querySelectorAll('.payguard-board-line-due').length === 3 && document.querySelectorAll('.payguard-board-line-now').length === 1, null, { timeout: 20000 });
  const caseOnly = await page.evaluate(() => ({
    statuses: [...document.querySelectorAll('[data-testid="evidence-board-row"]')].map((row) => row.dataset.status),
    text: document.querySelector('[data-testid="evidence-board"]')?.textContent ?? '',
  }));
  assert.deepEqual(caseOnly.statuses, ['DUE_SOON_NO_DRAFT', 'DUE_SOON_NO_DRAFT', 'DUE_SOON_NO_DRAFT'], 'CASE_ONLY_STATUSES');
  assert.equal(caseOnly.text.includes('Prepare the draft'), false, 'CASE_ONLY_NO_PREPARE_PROMPT');
  await page.evaluate(() => window.payguardShowDrafts());
  await page.locator('body[data-step="all"]').waitFor({ timeout: 20000 });
  await page.waitForFunction(() => document.querySelectorAll('[data-testid="evidence-board-timeline"] .payguard-board-window').length === 3, null, { timeout: 20000 });
  await page.waitForTimeout(800);

  const rendered = await page.evaluate(() => {
    const element = document.querySelector('[data-testid="evidence-board-timeline"] .b-scheduler');
    const namespace = window.bryntum;
    const Widget = namespace?.core?.Widget || namespace?.scheduler?.Widget || namespace?.Widget;
    const scheduler = Widget?.fromElement?.(element);
    const records = scheduler ? scheduler.eventStore.records : [];
    const canvas = document.querySelector('[data-testid="evidence-board-timeline"] .b-sch-foreground-canvas');
    return {
      found: Boolean(scheduler),
      start: scheduler?.startDate?.getTime(),
      end: scheduler?.endDate?.getTime(),
      eventStart: Math.min(...records.map((record) => record.startDate.getTime())),
      eventEnd: Math.max(...records.map((record) => record.endDate.getTime())),
      windowEnds: records.filter((record) => record.get('kind') === 'RESPONSE_WINDOW').map((record) => record.endDate.getTime()),
      canvasOverflow: canvas ? canvas.scrollWidth - canvas.clientWidth : null,
      statuses: [...document.querySelectorAll('[data-testid="evidence-board-row"]')].map((row) => row.dataset.status),
      amounts: [...document.querySelectorAll('[data-testid="evidence-board-row"]')].map((row) => [...row.querySelectorAll('dt')].find((dt) => dt.textContent === 'Amount')?.nextElementSibling?.textContent),
      summary: document.querySelector('[data-testid="evidence-board-summary"]')?.textContent ?? '',
    };
  });
  assert.ok(rendered.found, 'SCHEDULER_INSTANCE_NOT_FOUND');
  assert.equal(rendered.windowEnds.length, 3, 'one response window per case');
  assert.ok(rendered.start <= rendered.eventStart, 'AXIS_STARTS_AFTER_EARLIEST_EVENT');
  assert.ok(rendered.end >= rendered.eventEnd, 'AXIS_ENDS_BEFORE_LATEST_DUE_DATE');
  assert.ok(rendered.end >= Math.max(...rendered.windowEnds), 'AXIS_ENDS_BEFORE_A_RESPONSE_WINDOW');
  assert.ok(rendered.canvasOverflow !== null && rendered.canvasOverflow <= 1, `TIMELINE_CANVAS_OVERFLOWS_${rendered.canvasOverflow}`);
  assert.deepEqual(rendered.statuses, ['DUE_SOON', 'DUE_SOON', 'DUE_SOON_MISSING']);
  assert.deepEqual(rendered.amounts, disputes.map((row) => `${row.dispute_amount.value} ${row.dispute_amount.currency_code} · synthetic`));
  assert.match(rendered.summary, /^3 cases · 1 due within 3 days with evidence missing/u);
  // (optimise r24) Plan bars: one "Collect evidence" bar per case, a now line and one due line per case. A drag
  // moves a bar in whole hours and is kept in this tab's sessionStorage; a drop before now snaps back with a
  // message; the read-only response window does not move. The same steps were run over CDP in headless Chrome.
  const HOUR = 3600 * 1000;
  const planState = () => page.evaluate(() => {
    const element = document.querySelector('[data-testid="evidence-board-timeline"] .b-scheduler');
    const namespace = window.bryntum;
    const scheduler = (namespace?.core?.Widget || namespace?.scheduler?.Widget || namespace?.Widget)?.fromElement?.(element);
    const utc = (date) => Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes());
    const span = (id) => { const record = scheduler.eventStore.getById(id); return record && { start: utc(record.startDate), end: utc(record.endDate) }; };
    const box = (id) => { const bar = document.querySelector(`[data-event-id="${id}"]`); if (!bar) return null; const r = bar.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; };
    return {
      pxPerHour: (scheduler.getCoordinateFromDate(new Date(scheduler.startDate.getTime() + 10 * 3600000), true) - scheduler.getCoordinateFromDate(scheduler.startDate, true)) / 10,
      plan: span('case-ref-001-plan'), planBox: box('case-ref-001-plan'), window: span('case-ref-001-window'), windowBox: box('case-ref-001-window'),
      bars: document.querySelectorAll('[data-testid="evidence-board-timeline"] .payguard-board-plan').length,
      nowLines: document.querySelectorAll('.payguard-board-line-now').length, dueLines: document.querySelectorAll('.payguard-board-line-due').length,
      message: document.querySelector('[data-testid="evidence-board-plan-message"]')?.textContent || '',
      stored: sessionStorage.getItem('payguard.board.plan.v1'),
    };
  });
  const dragBy = async (box, dx) => {
    const x = box.x + box.w / 2;
    const y = box.y + box.h / 2;
    await page.mouse.move(x, y);
    await page.mouse.down();
    await page.mouse.move(x + dx, y, { steps: 12 });
    await page.waitForTimeout(150);
    await page.mouse.up();
    await page.waitForTimeout(500);
  };
  const p0 = await planState();
  assert.equal(p0.bars, 3, 'PLAN_BAR_PER_CASE');
  assert.equal(p0.nowLines, 1, 'NOW_LINE');
  assert.equal(p0.dueLines, 3, 'DUE_LINE_PER_CASE');
  assert.ok(p0.plan.start % HOUR === 0 && p0.plan.end % HOUR === 0 && p0.plan.start >= Date.now() - HOUR, 'PLAN_ON_HOURS_FROM_NOW');
  await dragBy(p0.planBox, p0.pxPerHour * 3);
  const p1 = await planState();
  assert.equal(p1.plan.start - p0.plan.start, 3 * HOUR, 'PLAN_DRAG_MOVES_WHOLE_HOURS');
  assert.match(p1.message, /Kept in this tab only, not sent\./u);
  assert.equal(JSON.parse(p1.stored).plans['case-ref-001'].start, new Date(p1.plan.start).toISOString(), 'PLAN_IN_SESSION_STORAGE');
  await dragBy(p1.planBox, -p0.pxPerHour * 30);
  const p2 = await planState();
  assert.deepEqual(p2.plan, p1.plan, 'PLAN_BEFORE_NOW_SNAPS_BACK');
  assert.match(p2.message, /moved back\. Cannot start before now\./u);
  await dragBy(p2.windowBox, 80);
  assert.deepEqual((await planState()).window, p0.window, 'RESPONSE_WINDOW_READ_ONLY');
  assert.deepEqual(problems, [], 'BROWSER_PROBLEMS');
  if (process.env.PAYGUARD_RENDER_SCREENSHOT) {
    await page.locator('#root').screenshot({ path: resolve(process.env.PAYGUARD_RENDER_SCREENSHOT) });
  }
  console.log(`frontend_bryntum_board_render: ok (${BRYNTUM_PACKAGE}@${bryntum.version} MIT; 3 rows, axis ${new Date(rendered.start).toISOString().slice(0, 10)} to ${new Date(rendered.end).toISOString().slice(0, 10)} holds every response window; urgent case-ref-003)`);
} finally {
  if (browser) await browser.close();
  server.close();
  rmSync(harness, { recursive: true, force: true });
}
