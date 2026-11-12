import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// "Start here" box: one button per guide situation, each a #guide-<situation> link that opens the live guide on that
// situation, starts it unless the same situation is already running, and scrolls to its form.
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');
const guide = readFileSync(resolve(root, 'frontend/src/GuideLive.jsx'), 'utf8');

const situations = [...guide.matchAll(/\['(\w+)', '[^']+'\]/g)].map((match) => match[1]).filter((id) => ['dispute', 'velocity', 'preflight'].includes(id));
assert.deepEqual([...new Set(situations)].sort(), ['dispute', 'preflight', 'velocity'], 'guide situations changed');

const box = app.match(/const START_HERE = (\[.*\]);/);
assert.ok(box, 'START_HERE list missing');
const buttons = [...box[1].matchAll(/\['(\w+)', '\w+', '[^']+'\]/g)].map((match) => match[1]);
assert.deepEqual(buttons.sort(), ['dispute', 'preflight', 'velocity'], 'one Start here button per guide situation');

assert.ok(app.includes('data-testid="start-here"'), 'box test id');
assert.ok(app.includes('data-testid={`start-here-${scenario}`}'), 'button test ids');
assert.ok(app.includes('href={`#guide-${scenario}`}'), 'buttons are deep links');
assert.ok(app.includes('target === `guide-${scenario}`'), 'hash #guide-<situation> opens the guide on load and on hashchange');
assert.ok(app.includes('request={guideRequest}'), 'App passes the jump request to the guide');

// Three situations, three separate guides (owner 2026-11-02): each step mounts its own, every call names it.
// attack r21: the guide also reports a 401 to the console's Reconnect flow.
assert.ok(guide.includes('function GuideLive({ session, Disclosure, Badge, request, scenario, onSessionExpired, onOpenItems, onChooser })' /* (r33 M4, r34 #1) */), 'guide takes its own situation');
assert.ok(!guide.includes('guide-live-scenario') && !guide.includes('setScenario'), 'no situation selector inside a guide');
assert.ok(guide.includes("body: path === '/guide/start' ? body : { ...body, scenario }"), 'every guide call names its situation');
assert.ok(guide.includes('`/guide/state?scenario=${scenario}`'), 'state is read per situation');
assert.ok(!guide.includes("apiRequest('/guide/state'"), 'no state read (including the analysis poll) omits the situation');
assert.ok(guide.includes('request.scenario !== scenario'), 'a jump for another situation is ignored by this guide');
assert.ok(guide.includes('if (view.started) reveal();'), 'a running guide is kept, never restarted by a jump');
assert.ok(guide.includes('}, [open, view, busy, request]);'), 'a click while the guide is already open still runs the jump');
assert.ok(guide.includes('document.getElementById(sectionId)?.scrollIntoView'), 'jump scrolls to this guide');
assert.ok(guide.includes("prefers-reduced-motion: reduce"), 'scroll honours reduced motion');
for (const [situation, stage] of [['preflight', 'compliance'], ['velocity', 'velocity'], ['dispute', 'disputes']]) {
  assert.ok(app.includes(`scenario="${situation}" session={sessionRef.current}`), `${situation} guide is mounted`);
  assert.ok(app.includes(`${situation}: '${stage}'`), `${situation} opens step ${stage}`);
}
const api = readFileSync(resolve(root, 'frontend/src/api.js'), 'utf8');
assert.ok(api.includes('if (body?.scenario !== undefined && payload.scenario !== body.scenario) fail();'), 'a reply for another situation is refused');

// Cross-check 2026-11-03 A6: redesign controls (step views, step "More", phone bar, short labels, case summary).
assert.ok(app.includes("const [velocityView, setVelocityView] = useState('chart');"), 'step 02 opens on the chart');
assert.ok(app.includes("setVelocityView('orders'); window.requestAnimationFrame(() => document.getElementById('velocity-quick-filter')?.focus());"), 'Inspect orders switches to the table and focuses the filter');
for (const view of ['chart', 'orders']) assert.ok(app.includes(`['${view}',`), `velocity view ${view}`);
assert.ok(app.includes('data-testid={`velocity-view-${key}`}'), 'velocity view test ids');
// (R7 T4) Step 03's More takes a label and opens itself for the board or after a draft, so it carries props.
for (const stage of ['compliance', 'velocity']) assert.ok(app.includes(`<StepMore id="${stage}" intro=`), `step ${stage} has its More disclosure (N1 C38: with its one-line intro)`);
assert.ok(app.includes('<StepMore id="disputes" label='), 'step disputes has its More disclosure');
assert.ok(app.includes('data-testid={`step-more-${id}`}'), 'StepMore test id');
const shortLabels = app.match(/const SHORT_LABEL = (\{[^}]*\});/);
assert.ok(shortLabels, 'SHORT_LABEL map');
assert.deepEqual([...shortLabels[1].matchAll(/'([^']+)':/g)].map((m) => m[1]), ['Policy pre-check', 'Sales spike', 'Dispute evidence'], 'three short phone labels');
assert.ok(app.includes('<span className="label-short">'), 'short label span');
assert.ok(app.includes("{ key: 'country', label: 'Check country rules'"), 'phone bar runs the country check when it is in view');
assert.ok(app.includes("{ key: 'country-next', label: hasPostalBan(countryCheck) ? 'Continue with another carrier' : 'Continue to draft'"), 'phone bar offers Continue to draft after a clear check');
assert.ok(app.includes('data-testid={`phone-action-${phoneAction.key}`}'), 'phone action test id');
assert.ok(app.includes('id="sandbox-draft"') && app.includes('<span>PayPal Sandbox draft (optional)</span>'), 'Sandbox draft block');
assert.ok(app.includes("document.querySelector('#sandbox-draft summary')?.focus({ preventScroll: true });"), 'Continue to draft moves focus to the draft block');
assert.ok(app.includes('data-testid="footer-independent"'), 'independence footer');
// (P4 2026-11-12) The case summary is the case head in steps/CaseViews.jsx (loaded with the step).
const caseViews = readFileSync(resolve(root, 'frontend/src/steps/CaseViews.jsx'), 'utf8');
assert.ok(caseViews.includes('data-testid="case-summary"'), 'case summary');
assert.ok(caseViews.includes('Seller Protection: PayPal decides if it applies'), 'case summary names Seller Protection without inventing a flag');
assert.ok(app.includes("['Seller Protection', sellerProtectionLabel(providerDisputeDetail)]"), 'dispute detail shows the Seller Protection line');
assert.ok(app.includes("if (detail?.source !== 'paypal_sandbox') return 'PayPal decides if it applies';"), 'sample cases show no invented flag');
assert.ok(guide.includes('id={`guide-live-text-${scenario}`}') && guide.includes('htmlFor={`guide-live-text-${scenario}`}'), 'one guide input id per step');
const claimTypes = api.match(/export const POLICY_CLAIM_TYPES = \[([^\]]*)\];/);
assert.ok(claimTypes, 'claim type list');
const backendTypes = readFileSync(resolve(root, 'src/payguard/advisory_eval.py'), 'utf8').match(/CLAIM_TYPES = frozenset\(\{([^}]*)\}\)/);
const names = (text) => [...text.matchAll(/['"](\w+)['"]/g)].map((m) => m[1]).sort();
assert.deepEqual(names(claimTypes[1]), names(backendTypes[1]), 'the policy check offers only claim types the backend accepts');

console.log('frontend_start_here: ok');

// Download-the-demo link (2026-11-09): direct GitHub asset, new tab, no opener; console footer and Proof page.
// (K1 G9 2026-11-13) The console has one copy, in the footer: the header More menu copy (hero-download-demo) is gone.
{
  const url = 'https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip';
  const appSrc = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
  const proofSrc = readFileSync(new URL('../frontend/src/proof/main.jsx', import.meta.url), 'utf8');
  assert.equal(appSrc.split(`href="${url}"`).length - 1, 1, 'the console shows the demo download once (footer)');
  assert.ok(!appSrc.includes('data-testid="hero-download-demo"'), 'the header More menu has no demo download');
  assert.ok(/<footer>[\s\S]*data-testid="footer-download-demo"[\s\S]*<\/footer>/.test(appSrc), 'the console download sits in the footer');
  for (const [name, src, id] of [['footer', appSrc, 'footer-download-demo'], ['proof', proofSrc, 'proof-download-demo']]) {
    const tag = src.match(new RegExp(`<a [^>]*data-testid="${id}"[^>]*>[\\s\\S]*?</a>`))?.[0] || '';
    assert.ok(tag.includes(`href="${url}"`), `${name} download link has the exact asset URL`);
    assert.ok(tag.includes('rel="noopener noreferrer"') && tag.includes('target="_blank"'), `${name} download link opens a new tab without opener`);
    assert.ok(tag.includes('Download the demo (11 MB)') && tag.includes('Same demo, one command, no keys.'), `${name} download link has the label and hint`);
  }
}
