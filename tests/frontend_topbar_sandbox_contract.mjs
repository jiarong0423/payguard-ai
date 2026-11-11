// Top-bar Sandbox card (owner 2026-11-03): local runs show it on every step; an orange "Connect" face flips over to
// a green "connected" face with a breathing dot; the hosted demo never shows it; the step 01 button stays.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');

const start = app.indexOf('<header className="topbar"');
const topbar = app.slice(start, app.indexOf('</header>', start));
assert.ok(topbar.includes("{!hosted && <TopbarSandbox connected={sandbox?.status === 'connected'} disabled={disabled} loading={busy === 'connect'} onConnect={connectSandbox} />}"),
  'local only, follows the Sandbox status, same connect action and busy rules as step 01');
const card = app.slice(app.indexOf('function TopbarSandbox('), app.indexOf('// "Start here" box'));
assert.ok(card.includes('data-testid="topbar-sandbox-connect"') && card.includes('disabled={disabled || connected}'), 'front face: connect button');
assert.ok(card.includes('data-testid="topbar-sandbox-status"') && card.includes('Sandbox connected'), 'back face: connected');
assert.equal(card.split('topbar-sandbox-breath').length - 1, 2, 'breathing light on both faces');
assert.ok(card.includes("aria-hidden={connected ? undefined : true}") && card.includes('tabIndex={connected ? -1 : undefined}'), 'hidden face is not read or focused');
assert.ok(app.includes('<Button data-testid="sandbox-connect"'), 'step 01 button kept');

// (P1 2026-11-12) Orange and its glow left the palette: the Connect face is the ink-outline secondary button until connected.
assert.ok(/\.topbar \.topbar-sandbox-front \{[^}]*border: 1px solid var\(--pg-color-ink\)[^}]*color: var\(--pg-color-ink\)/.test(css), 'ink outline until connected');
assert.ok(!/#e06c1e|pg-sandbox-glow/.test(css), 'no orange face and no glow');
assert.ok(/\.topbar \.topbar-sandbox-back \{[^}]*background: var\(--pg-color-ok\)/.test(css), 'green back face');
assert.ok(/\.topbar \.topbar-sandbox\.is-connected \.topbar-sandbox-back \{ transform: rotateY\(0deg\); visibility: visible;/.test(css), 'flips in when connected');
assert.ok(/\.topbar \.topbar-sandbox\.is-connected \.topbar-sandbox-front \{ transform: rotateY\(90deg\); visibility: hidden;/.test(css), 'front turns away and hides');
assert.ok(!/backface-visibility:/.test(css), 'flip does not depend on backface-visibility');
assert.ok(/@keyframes pg-sandbox-breath \{[^\n]*opacity: \.1;/.test(css), 'signal light blinks off and on');
assert.ok(/prefers-reduced-motion: reduce\) \{[^\n]*topbar-sandbox-breath \{ animation: none/.test(css), 'reduced motion respected');
assert.ok(/@media \(max-width: 400px\) \{\s*\.topbar \.environment:not\(\.environment-hosted\) \{ display: flex; \}/.test(css), 'visible on narrow phones');

// r20 UX-8: on 360px phones the card keeps a visible short label, not an unlabeled orange dot.
const narrow = css.slice(css.indexOf('@media (max-width: 400px) {\n  .topbar .environment:not(.environment-hosted) { display: flex; }'));
const narrowBlock = narrow.slice(0, narrow.indexOf('\n}\n'));
assert.ok(/\.topbar \.topbar-sandbox-short \{ display: inline;/.test(narrowBlock), 'short label visible at 400px and below');
assert.equal(/topbar-sandbox-short \{[^}]*clip:/.test(narrowBlock), false, 'short label is not screen-reader only');
assert.ok(/\.topbar \.topbar-sandbox-face \{[^}]*min-height: 44px/.test(narrowBlock), '44px touch target');
assert.ok(card.includes('<span className="topbar-sandbox-short">Sandbox</span>') && card.includes('<span className="topbar-sandbox-short">Connected</span>'), 'short labels on both faces');

console.log('frontend_topbar_sandbox_contract: ok');
