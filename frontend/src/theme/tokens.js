// Design tokens: the single JS source (docs/design/VISUAL_SPEC_r7.md sections 2, 5 and 6, r7.3).
// theme/tokens.css is a static mirror of cssVariables(); tests/frontend_tokens.mjs keeps them equal.
// Type sizes live in the index.css token block (pinned by tests/frontend_type_scale.mjs); `type` below
// mirrors that block for JS consumers (charts, grids, Studio) and the parity test checks it.

export const color = Object.freeze({
  canvas: '#eceae5',          // L0 page canvas: Morandi warm grey (2026-11-03 owner: Morandi accents, indigo stays)
  panel: '#ffffff',           // L1/L2 card surface
  recede: '#f4f2ee',          // done / inactive surface (no shadow), Morandi warm
  rule: '#dcd7cf',
  ink: '#0f172a',
  muted: '#475569',
  subtle: '#5b6678',          // minimum contrast for text (5.8:1 on white)
  accent: '#4f46e5',
  accentStrong: '#4338ca',
  accentTint: '#ecebf3',      // active headers (Morandi plan A: warm the cold indigo tint)
  accentSelected: '#e2e0f0',  // selected rows
  context: '#7c8799',         // marks only (3.6:1), never text
  model: '#0f766e',           // D9: model = teal
  ok: '#4a6a4e',               // Morandi sage (5.0:1 on white)
  watch: '#875f30',           // Morandi ochre, reserved for watch / due soon (4.7:1 on white)
  risk: '#93454a',             // Morandi dusty rose, held (5.5:1 on white)
  info: '#4f46e5',
  band: '#0b1b33',            // navy KPI band, top of its shade
  bandShade: '#13284a',       // bottom of the band shade
  bandText: '#e6edf7',
  bandMuted: '#9fb0c8',
  bandAmber: '#fbbf24',
  bandGreen: '#4ade80',
  focus: '#4f46e5',
});

// Status chips: text colour plus an 8% tint of the same colour as the background.
export const statusTint = Object.freeze({ ok: '#e8eee6', watch: '#f3eadd', risk: '#f4e5e4', info: 'rgba(79,70,229,.08)' });

// D9 categorical meaning: code/rules = indigo, model = teal, then two spare hues.
export const categorical = Object.freeze(['#4f46e5', '#0f766e', '#a21caf', '#0369a1']);
export const sequential = Object.freeze(['#e0e7ff', '#a5b4fc', '#6366f1', '#4338ca', '#312e81']);

export const space = Object.freeze({ 1: 4, 2: 8, 3: 12, 4: 16, 5: 24, 6: 32, 7: 48, 8: 64 }); // px

export const radius = Object.freeze({ chip: 6, control: 8, card: 12, pill: 999 }); // px

// r7.3 elevation levels. L0 is the canvas itself; done/inactive elements recede to `recede` with no shadow.
export const elevation = Object.freeze({
  l0: 'none',
  l1: '0 0 0 1px #dcd7cf, 0 1px 2px rgba(15,23,42,.06)',
  l2: '0 0 0 1px rgba(79,70,229,.35), 0 8px 24px rgba(15,23,42,.10), 0 2px 6px rgba(15,23,42,.06)',
  l3: '0 12px 32px rgba(15,23,42,.16)',
  activeBar: '4px',           // left accent bar on the L2 element
});

export const motion = Object.freeze({
  hover: 120, state: 180, dataMin: 240, dataMax: 400, max: 500, revealMax: 2500, // ms
  easeOut: 'cubic-bezier(.2,.8,.2,1)',
  easeIn: 'cubic-bezier(.4,0,1,1)',
});

export const font = Object.freeze({
  sans: "'Inter Variable', Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif",
  mono: 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
  numeric: '"tnum" 1',        // font-feature-settings for every number
});

// Mirrors the index.css type token block (px). Chart/axis/grid sizes follow spec section 2.
export const type = Object.freeze({
  stageTitle: 22, sectionTitle: 17, body: 16, control: 16, data: 16, support: 15, meta: 14, kpi: 40, kpiBand: 28,
  chartTitle: 16, chartAxis: 14, gridCell: 16,
});

export const layout = Object.freeze({
  maxWidth: 1200, topBar: 56, band: 56, actionBar: 56, gridRow: 40, gridRowPhone: 44, sectionGap: 48, sectionGapPhone: 32,
  cardPad: 20, cardPadWide: 24, heroPad: 32, cardGap: 24, phone: 640,
});

const kebab = (name) => String(name).replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`);

// The exact custom properties tokens.css must declare (name -> value). Lengths carry px.
export function cssVariables() {
  const vars = {};
  for (const [k, v] of Object.entries(color)) vars[`--pg-color-${kebab(k)}`] = v;
  for (const [k, v] of Object.entries(statusTint)) vars[`--pg-tint-${kebab(k)}`] = v;
  categorical.forEach((v, i) => { vars[`--pg-cat-${i + 1}`] = v; });
  sequential.forEach((v, i) => { vars[`--pg-seq-${i + 1}`] = v; });
  for (const [k, v] of Object.entries(space)) vars[`--pg-space-${k}`] = `${v}px`;
  for (const [k, v] of Object.entries(radius)) vars[`--pg-radius-${kebab(k)}`] = `${v}px`;
  for (const [k, v] of Object.entries(elevation)) vars[`--pg-elev-${kebab(k)}`] = v;
  for (const [k, v] of Object.entries(motion)) vars[`--pg-motion-${kebab(k)}`] = typeof v === 'number' ? `${v}ms` : v;
  for (const [k, v] of Object.entries(font)) vars[`--pg-font-${kebab(k)}`] = v;
  for (const [k, v] of Object.entries(layout)) vars[`--pg-layout-${kebab(k)}`] = `${v}px`;
  return vars;
}

// The tokens.css text, exactly. Run `node frontend/src/theme/writeTokensCss.mjs` after changing a token.
export function tokensCss() {
  const lines = Object.entries(cssVariables()).map(([k, v]) => `  ${k}: ${v};`);
  return `/* Generated from theme/tokens.js by theme/writeTokensCss.mjs; do not edit by hand (tests/frontend_tokens.mjs checks parity). */\n:root {\n${lines.join('\n')}\n}\n`;
}
