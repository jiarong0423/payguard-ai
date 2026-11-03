// Attack r23, secondary pages (dashboard auditor panel, evidence charts). Source contract checks; the browser
// behaviour (scroll into view, no keyboard on touch, one named node per chart) is checked in headless Chrome.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(projectRoot, path), 'utf8');
const dashboard = read('frontend/src/dashboard/main.jsx');
const charts = read('frontend/src/charts/BenchmarkCharts.jsx');

// 1. Opening the auditor scrolls the Studio area into view under the top bar (the message box was at top 887 px).
assert.ok(dashboard.includes('function scrollStudioIntoView(studio)'), 'scroll helper');
assert.ok(dashboard.includes("window.getComputedStyle(topbar).position === 'sticky'"), 'offset only for the sticky top bar');
assert.ok(dashboard.includes('scrollStudioIntoView(root); // the panel was focused off screen (attack r23)'), 'panel scrolled into view when focused');

// 2. Compact by width, short height or a coarse pointer; touch focuses the panel heading, not the message box.
assert.ok(dashboard.includes('window.matchMedia(`(max-width: ${COMPACT_BREAKPOINT}px), (max-height: ${SHORT_BREAKPOINT}px)`)'), 'compact query: size only, tablets keep the wide layout');
assert.ok(dashboard.includes("const touchQuery = window.matchMedia('(pointer: coarse), (hover: none)');"), 'touch query');
assert.ok(dashboard.includes("? root?.querySelector('.ag-studio-panel-header')"), 'touch or compact: heading');
assert.equal((dashboard.match(/panelFocusTarget\(root\)/gu) || []).length, 2, 'open and chip tap share one focus rule');
assert.equal(/compactQuery\.matches \? root/u.test(dashboard), false, 'no width-only focus choice left');

// 3. Evidence charts: the wrapper is unnamed, the focusable surface carries this chart's own label.
assert.equal(/role="figure" aria-label=\{label\}/u.test(charts), false, 'wrapper has no role or name');
assert.ok(charts.includes('if (name && name.textContent !== label) name.textContent = label;'), 'surface named after its chart');
assert.equal(charts.includes('FOCUS_SURFACE_NAME'), false, 'no shared generic surface name');
assert.ok(charts.includes("proxy.setAttribute('role', 'presentation')"), 'canvas proxy stays presentational');
const labels = [...charts.matchAll(/<Chart build=\{\w+\} testId="[\w-]+" label=\{?[`"]([^`"]+)[`"]/gu)].map((m) => m[1]);
assert.equal(labels.length, 3, 'three charts');
assert.equal(new Set(labels).size, 3, 'three distinct chart names');

console.log('frontend attack r23 secondary contract OK');
