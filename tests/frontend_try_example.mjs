import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// "Try the example" (judge self-test): the contract of the one-click Step 01 example. Source-level, no server, no network.
const panel = readFileSync(new URL('../frontend/src/CountryRules.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/CountryRules.css', import.meta.url), 'utf8');
const readme = readFileSync(new URL('../README.md', import.meta.url), 'utf8');

// Button exists, with its label and test id.
assert.ok(panel.includes('data-testid="country-try-example"'), 'button has a test id');
assert.ok(/onClick=\{tryExample\}>Fill from example<\/button>/.test(panel), 'the card button reads "Fill from example" (the hero reads "Run the step 1 example") and runs tryExample');
// Prefill values: United States to Singapore, E-cigarettes only.
assert.ok(panel.includes("seller_country: 'US', buyer_country: 'SG', goods_tags: Object.freeze(['e_cigarettes'])"), 'example is US to SG with e_cigarettes');
assert.ok(panel.includes('const next = { ...form, ...EXAMPLE_ROUTE, goods_tags: [...EXAMPLE_ROUTE.goods_tags] };'), 'example overwrites route and goods on the existing form state');
assert.ok(panel.includes('setForm(next);') && panel.includes('runCheck(next);'), 'form is filled, then the check runs with those values');
// It uses the existing check, not a new path: Check country rules calls the same function; one apiRequest call in the file besides the catalog.
assert.ok(panel.includes('const run = () => runCheck(form);'), 'Check country rules and the example share runCheck');
assert.ok(panel.includes("onClick={run}>{busy ? 'Checking…' : 'Check country rules'}"), 'the existing check button is unchanged');
const targets = [...panel.matchAll(/apiRequest\(\s*'([^']+)'/g)].map((match) => match[1]).sort();
assert.deepEqual(targets, ['/country-rules/check', '/country-rules/countries'], 'no new request target in the panel');
assert.ok(!/\bfetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket|EventSource/.test(panel), 'the panel makes no direct network call');
assert.ok(!/\/(guide|gemini|evidence|sandbox|disputes)\b/i.test(targets.join(' ')), 'no PayPal, guide or model route is requested');
// Busy and Retry-After wait hold it like the normal button; a missing country in the build is an explicit message.
assert.ok(panel.includes('if (busy || Date.now() < waitUntil) return;'), 'held while a check runs or a wait is active');
assert.ok(panel.includes('The example needs the United States and Singapore'), 'missing countries are reported, not ignored');
// Result stays the existing verdict, and scrolls into view smoothly (instant under reduced motion).
assert.ok(panel.includes('A rule may stop this sale.'), 'verdict text unchanged');
assert.ok(panel.includes("block: fromExample ? 'start' : 'nearest', behavior: reducedMotion ? 'auto' : 'smooth'"), 'result scrolls into view');
// Phone: the button is not hidden at any width, is 44px high, and fills the width at 640px and below.
assert.ok(/\.country-try-example\s*\{[^}]*min-height:\s*44px/.test(css), 'touch size 44px');
assert.ok(/@media \(max-width: 640px\)\s*\{\s*\.country-try-example\s*\{[^}]*width:\s*100%/.test(css), 'phone width rule exists');
assert.ok(!/\.country-try-example\s*\{[^}]*display:\s*none/.test(css), 'never hidden');
assert.ok(panel.includes('Synthetic data, no PayPal calls'), 'the note under the button says synthetic data and no PayPal calls');
assert.ok(!readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8').includes('<p>Results show here.</p>'), 'right pane no longer reads as empty');
// README step 1 names the button; the phone Proof link is named in step 5.
assert.ok(readme.includes('select **Run the step 1 example**'), 'README step 1 uses the button');
assert.ok(readme.includes('**Next: dispute evidence**') && readme.includes('**Load dispute case**'), 'README step 4 names the path');
assert.ok(readme.includes('**Proof and receipts** link under the page title'), 'README step 5 names the phone link');

// (2026-11-08) A first-screen entry: the hero button clicks the country card's own example button, so it adds no request or logic.
{
  const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
  assert.ok(app.includes('data-testid="hero-try-example"'), 'hero has a Try the example button');
  assert.ok(app.includes("document.querySelector('[data-testid=\"country-try-example\"]')?.click()"), 'hero button clicks the existing example button');
  const heroLine = app.split('\n').find((line) => line.includes('data-testid="hero-try-example"')) || '';
  assert.ok(!/fetch\(/u.test(heroLine), 'hero button adds no request');
}

console.log('frontend_try_example: ok');
