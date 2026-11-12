import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// (r33 M1-M5) Console UI follow-ups from the r32 judges: one Technical details in the dispute evidence area,
// "Checking with Gemini…" as the only wait text, the newest guide reply and the dashboard starter answer kept in view
// on a phone, the open guide items named in the Step 3 draft, and a muted hint in the space a hidden phone action keeps.
const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const app = read('frontend/src/App.jsx');
const css = read('frontend/src/index.css');
const guide = read('frontend/src/GuideLive.jsx');
const dashboard = read('frontend/src/dashboard/main.jsx');

// ---- M1: one collapsed Technical details for the evidence area, after both previews, with all of its information. ----
{
  const start = app.indexOf('<div className="provider-disputes-body">');
  const body = app.slice(start, app.indexOf('</details>\n        <StepSection id="guide-replay"', start));
  assert.ok(start > 0 && body.length > 0, 'evidence area found');
  assert.equal(body.split('<summary>Technical details</summary>').length - 1, 1, 'one Technical details in the evidence area');
  const details = body.indexOf('<details className="technical-details" data-testid="evidence-technical-details">');
  assert.ok(details > body.indexOf('{evidencePreview && <div className="evidence-preview"'), 'after the evidence preview');
  assert.ok(details > body.indexOf('{trackingPreview && <div className="evidence-preview tracking-preview"'), 'after the tracking preview');
  const merged = body.slice(details, body.indexOf('</details>', details));
  for (const kept of ['Builds the multipart POST /v1/customer/disputes/', 'PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled', 'a preview has been prepared.',
    '{evidencePreview && <div className="evidence-technical-request" data-testid="evidence-technical-request">',
    '<Badge tone="blue">{evidencePreview.method} {evidencePreview.path}</Badge>', '<Badge tone="muted">{evidencePreview.content_type}</Badge>',
    '<pre>{JSON.stringify(evidencePreview.input, null, 2)}</pre>']) assert.ok(merged.includes(kept), `kept: ${kept}`);
  assert.equal(/<details[^>]*\sopen/u.test(merged), false, 'collapsed by default');
}

// ---- M2: every wait for Gemini in the UI reads "Checking with Gemini…"; the retired wordings are gone. ----
{
  const root = fileURLToPath(new URL('../frontend/src/', import.meta.url));
  const files = [];
  const walk = (dir) => { for (const name of readdirSync(dir)) { const path = join(dir, name); if (statSync(path).isDirectory()) walk(path); else if (/\.(jsx?|html)$/u.test(name)) files.push(path); } };
  walk(root);
  const strip = (source) => source.replace(/\/\*[\s\S]*?\*\//gu, '').replace(/^\s*\/\/.*$/gmu, '');
  for (const path of files) {
    const code = strip(readFileSync(path, 'utf8'));
    for (const retired of [/governed model/iu, /Analy[sz]ing with/iu, /Asking Gemini/iu, /Waiting for Gemini/iu]) {
      assert.equal(retired.test(code), false, `${path}: ${retired}`);
    }
  }
  assert.ok(guide.includes("const RUNNING_TEXT = 'Checking with Gemini…';"), 'the one wait text');
  assert.equal(guide.split('Checking with Gemini…').length - 1, 1, 'defined once, used through RUNNING_TEXT');
}

// ---- M3: the newest reply's top stays in the log's view; the dashboard answer is scrolled to and re-checked. ----
{
  const effect = guide.slice(guide.indexOf('// (r33 M3)'), guide.indexOf('}, [log]);') + 10);
  assert.ok(effect.includes('const newest = box.lastElementChild;'), 'newest reply');
  assert.ok(effect.includes('box.scrollTo({ top: Math.max(0, Math.min(newestTop, box.scrollHeight - box.clientHeight)) });'), 'its top, or the bottom when it fits');
  assert.equal(guide.includes('logRef.current?.scrollTo?.({ top: logRef.current.scrollHeight });'), false, 'bottom-only scroll gone');
  // Behaviour: the same arithmetic over a 300px box.
  const target = (scrollTop, newestOffset, scrollHeight, clientHeight = 300, pad = 8) => Math.max(0, Math.min(scrollTop + newestOffset - pad, scrollHeight - clientHeight));
  assert.equal(target(0, 500, 700), 400, 'a short newest reply: bottom');
  assert.equal(target(0, 500, 1200), 492, 'a newest reply taller than the box: its top');
  assert.ok(dashboard.includes('function scrollAnswerIntoView(widget) {'), 'answer scroll helper');
  assert.ok(dashboard.includes('      scrollAnswerIntoView(widget);\n'), 'used by focusAnswer');
  assert.equal(dashboard.includes("widget.scrollIntoView({ behavior: 'smooth', block: 'start' });"), false, 'single smooth scroll gone');
  const helper = dashboard.slice(dashboard.indexOf('function scrollAnswerIntoView'), dashboard.indexOf('function Dashboard('));
  assert.ok(helper.includes("document.querySelector('.pg-topbar')") && helper.includes('if (top < 0 || top > window.innerHeight * 0.5) go(\'auto\');'), 'under the top bar, re-checked after layout');
}

// ---- M4: the Step 3 guide reports its open items; the draft shows one plain line only when N > 0. ----
{
  assert.ok(guide.includes('export default function GuideLive({ session, Disclosure, Badge, request, scenario, onSessionExpired, onOpenItems, onChooser }) {'), 'callback prop');
  assert.ok(guide.includes("const openCount = started ? (view.items || []).filter((item) => item.status !== 'STRUCTURALLY_PRESENT' && item.status !== 'NOT_APPLICABLE').length : 0;"), 'open = not present, not n/a; 0 before start');
  assert.ok(guide.includes('useEffect(() => { onOpenItems?.(openCount); }, [openCount]);'), 'reported on change');
  assert.ok(guide.includes('useEffect(() => () => onOpenItems?.(0), []);'), 'reset on unmount');
  assert.equal(app.split('onOpenItems={setGuideOpenItems}').length - 1, 1, 'only the dispute guide reports');
  assert.ok(/<GuideLive key=\{`dispute-[^\n]*onOpenItems=\{setGuideOpenItems\} request=\{guideRequest\} onSessionExpired=\{panelSessionExpired\} \/>/u.test(app), 'on the dispute guide');
  assert.ok(app.includes('const [guideOpenItems, setGuideOpenItems] = useState(0);'), 'starts at 0');
  const line = '{guideOpenItems > 0 && <p className="guide-open-items text-dim" data-testid="guide-open-items">Guide items still open: {guideOpenItems}; they are not part of this draft.</p>}';
  assert.ok(app.includes(line), 'one plain line, hidden at 0');
  const draftArea = app.indexOf('{draft ? <><div className="dispute-route"');
  assert.ok(draftArea > 0 && app.indexOf(line) > draftArea && app.indexOf(line) < app.indexOf('<div className="privacy-strip"', draftArea), 'inside the evidence draft');
}

// ---- M5: hidden in-page actions keep their space (r2 P0) and show a muted pointer to the bar, out of flow. ----
{
  assert.ok(css.includes('.app-shell.phone-action-approve [data-testid="dispute-approve"] { visibility: hidden; }'), 'space kept');
  const start = css.indexOf('/* (r33 M5)');
  const rule = css.slice(start, css.indexOf('}\n', css.indexOf('::after {', start)) + 2);
  assert.ok(start > 0 && rule.includes('.app-shell.has-phone-action:not(.is-typing)'), 'not while typing (the button is back)');
  for (const id of ['aup-review', 'country-check', 'country-continue-draft', 'demo-burst', 'dispute-draft', 'dispute-approve', 'invoice-create', 'sandbox-connect']) {
    assert.ok(rule.includes(`[data-testid="${id}"])::after`) || rule.includes(`[data-testid="${id}"], `), `hint for ${id}`);
  }
  for (const part of ['content: "Your next step is in the bar below";', 'position: absolute; inset: 0;', 'visibility: visible; pointer-events: none;', 'color: var(--pg-color-muted);']) {
    assert.ok(rule.includes(part), part);
  }
  assert.equal(/::after\s*\{[^}]*(height|margin|padding-block|display:\s*block)/u.test(rule.replace('padding: 0 2px;', '')), false, 'no size change of the kept space');
}

console.log(JSON.stringify({ status: 'PASS', checks: 'r33 M1-M5' }));
