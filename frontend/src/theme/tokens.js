// Design tokens: the single JS source (docs/design/VISUAL_SPEC_r7.md sections 2, 5 and 6, r7.3).
// theme/tokens.css is a static mirror of cssVariables(); tests/frontend_tokens.mjs keeps them equal.
// Type sizes live in the index.css token block (pinned by tests/frontend_type_scale.mjs); `type` below
// mirrors that block for JS consumers (charts, grids, Studio) and the parity test checks it.

export const color = Object.freeze({
  // 2026-11-12 P0 round 3: "Editorial Newsprint", red option 2 (owner decision). Names kept; values changed.
  // Ink does every interactive job; red means risk and nothing else (always with an icon). Round 5 removed the
  // decorative headline red (`masthead` token) so the rule has no exception.
  canvas: '#f1ede3',          // L0 newsprint
  panel: '#f8f5ee',           // inputs and raised paper
  recede: '#e8e2d5',          // surface, a shade darker than the page
  // Round 5 (owner: "all black is too heavy"; style reference: charcoal, not black): rules and every interactive job
  // move to charcoal #2b2d30; running text stays ink #111111. Paper on charcoal 12.7:1, charcoal on canvas 11.8:1.
  rule: '#2b2d30',            // rules (cards, sections, masthead): charcoal
  ruleSoft: '#cfc8b8',        // row separators inside tables and lists
  controlLine: '#8a857a',     // newsprint grey: control edges and marks (3.1:1 on canvas, WCAG 1.4.11)
  ink: '#111111',
  muted: '#5a554c',           // secondary text (6.3:1 on canvas, 5.7:1 on surface)
  subtle: '#5a554c',
  accent: '#2b2d30',          // interactive = charcoal: buttons, segment frames, current nav, focus
  accentStrong: '#1f2124',    // primary hover, one step darker (14.8:1 under paper)
  accentTint: '#e8e2d5',
  accentSelected: '#e8e2d5',  // selected rows: surface fill + 3px ink bar
  context: '#8a857a',         // marks only (3.1:1), never text
  model: '#5a554c',
  ok: '#2f6b3a',              // holds / sent (5.5:1 on canvas)
  watch: '#7a5000',           // check first / due soon (6.0:1 on canvas)
  warn: '#7a5000',
  risk: '#c8102e',            // risk ONLY (rule match, missed / <= 1 day deadline), always with an icon (5.0:1 on canvas)
  info: '#5a554c',
  band: '#111111',
  bandShade: '#1c1b19',
  bandText: '#f1ede3',
  bandMuted: '#bdb6a6',
  bandAmber: '#e8b04a',
  bandGreen: '#8fc79a',
  focus: '#2b2d30',           // 2px charcoal ring with a 3px gap, :focus-visible only
  onAccent: '#f8f5ee',        // text on ink fills
  chip: '#ddd6c6',            // neutral count badge
  hover: '#ebe6da',           // row / item hover
  disabledLine: '#cfc8b8',
  disabledText: '#9a958a',
  // v2 (2026-11-12, design-system pass): added only; nothing above changed. Contrast in tests/frontend_design_system_v2.mjs.
  line: '#cfc6b4',            // hairline: card / fold / tag frames. Decorative (1.45:1); control edges stay controlLine
  rowHover: '#efe9dd',        // row / item hover (`hover` above keeps its value for existing pages)
  sel: '#e2dac8',             // THE selection tint: selected row, active step, queue card, linked row (+3px ink bar)
  surface2: '#ebe5d7',        // sunk surface: folds, summary ledgers
  riskTint: '#f7e4e4',        // note / stamp backgrounds; text on them stays its own hue (risk 4.8, ok 5.3, warn 5.8)
  okTint: '#e4ece0',
  warnTint: '#f2e8d0',
  ink3: '#8a8478',            // disabled text and non-text meta marks only (3.2:1 on canvas): never running text
  // UI round 5 (style reference, review_STYLEREF s2): ONE dark surface, the Proof verify panel ("vault"). Status hues on it
  // are their own light values (the paper hues fail on dark: ok 2.8, risk 3.0, warn 2.5). Ratios on vault: ink 15.2,
  // muted 8.5, ok 9.2, warn 9.1, risk 7.5. The vault itself never means risk and never carries an error.
  vault: '#16181b',
  vaultInk: '#f1ede3',
  vaultMuted: '#b9b3a6',
  vaultRule: '#4b4b4a',       // hairline on the vault (decorative, 2.0:1)
  vaultOk: '#8fc79a',
  vaultWarn: '#e8b04a',
  vaultRisk: '#f28b8b',
});

// Rules (round 5): fine hairline between rows, double rule to open a block. Ink only.
export const rule = Object.freeze({ fine: '1px solid #2b2d30', double: '3px double #2b2d30' });

// Tracked small caps (round 5): eyebrow, stamp and tag only; never body text or IDs.
export const label = Object.freeze({ tracking: '.16em' }); // round 5: wider, tailored small caps

// Data viz (v2): no teal, no orange, no white. Above the review line = check first (amber), not risk (red).
export const viz = Object.freeze({ base: '#bdb6a6', line: '#5a554c', alert: '#7a5000', bg: '#e8e2d5' });

// Composition (v2): 1040 content, 12 columns of 64 with 24 gutters (12*64 + 11*24 = 1032 + 8 slack), 68ch measure.
export const grid = Object.freeze({ columns: 12, measure: '68ch' });

// Status chips: text colour on a light tint of the same hue (all >= 4.5:1).
export const statusTint = Object.freeze({ ok: '#dfe8da', watch: '#efe2c4', risk: '#f6dfe0', info: '#e8e2d5', accent: '#e8e2d5' });

// Categorical / sequential: ink and greys only (red is reserved for risk).
export const categorical = Object.freeze(['#111111', '#5a554c', '#8a857a', '#bdb6a6']);
export const sequential = Object.freeze(['#e8e2d5', '#cfc8b8', '#8a857a', '#5a554c', '#111111']);

export const space = Object.freeze({ 1: 4, 2: 8, 3: 12, 4: 16, 5: 24, 6: 32, 7: 48, 8: 64 }); // px, 8 steps

export const radius = Object.freeze({ chip: 0, control: 0, card: 0, pill: 999, status: 2 }); // px: square print; v2 status labels 2px (pill kept for old pages)

// Flat print: black rules instead of shadows; only floating layers (tooltip, popover, menu) cast a shadow.
export const elevation = Object.freeze({
  l0: 'none',
  l1: '0 0 0 1px #111111',
  l2: '0 0 0 2px #111111',   // active card: double-weight ink rule
  l3: '0 8px 24px rgba(17,17,17,.12), 0 1px 2px rgba(17,17,17,.08)',
  activeBar: '3px',           // left bar on the active card / selected row
});

export const motion = Object.freeze({
  hover: 120, state: 180, dataMin: 240, dataMax: 400, max: 500, revealMax: 2500, // ms
  easeOut: 'cubic-bezier(.2,.8,.2,1)',
  easeIn: 'cubic-bezier(.4,0,1,1)',
  // Round 5: precise micro-interactions, 160-240 ms, no overshoot; off under prefers-reduced-motion.
  quick: 160, sweep: 200, settle: 240, precise: 'cubic-bezier(.2,0,0,1)',
});

export const font = Object.freeze({
  sans: "'Public Sans', 'Inter Variable', Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif", // text and UI; Public Sans self-hosted (OFL-1.1), Inter fallback
  serif: "'Newsreader', 'Iowan Old Style', Georgia, serif", // headings and quotes; self-hosted (OFL-1.1); pairing D chosen 2026-11-12
  mono: 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
  numeric: '"tnum" 1',        // font-feature-settings for every number
});

// Mirrors the index.css type token block (px). Chart/axis/grid sizes follow spec section 2.
export const type = Object.freeze({
  stageTitle: 22, sectionTitle: 17, body: 16, control: 16, data: 16, support: 15, meta: 14, kpi: 40, kpiBand: 28,
  chartTitle: 16, chartAxis: 14, gridCell: 16,
});

// 7-step type scale for the restyle (px); 12 only for uppercase tracked labels (eyebrow, stamp). The --type-* block in index.css stays as is (pinned by frontend_type_scale.mjs).
export const scale = Object.freeze({ 1: 12, 2: 14, 3: 16, 4: 20, 5: 28, 6: 40, 7: 56 });

export const layout = Object.freeze({
  maxWidth: 1200, topBar: 56, band: 56, actionBar: 56, gridRow: 40, gridRowPhone: 44, sectionGap: 48, sectionGapPhone: 32,
  cardPad: 20, cardPadWide: 24, heroPad: 32, cardGap: 24, phone: 640, content: 1040, focusRing: 2, ruleHeavy: 3,
  gridCol: 64, gridGutter: 24, stepHead: 72, // v2
  ruleBlock: 2, // round 5: 3px (ruleHeavy) is for the masthead only; a block opens with 2px
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
  for (const [k, v] of Object.entries(scale)) vars[`--pg-text-${k}`] = `${v}px`;
  for (const [k, v] of Object.entries(layout)) vars[`--pg-layout-${kebab(k)}`] = `${v}px`;
  for (const [k, v] of Object.entries(viz)) vars[`--pg-viz-${k}`] = v;
  for (const [k, v] of Object.entries(grid)) vars[`--pg-grid-${k}`] = String(v);
  for (const [k, v] of Object.entries(rule)) vars[`--pg-rule-${k}`] = v;
  for (const [k, v] of Object.entries(label)) vars[`--pg-label-${k}`] = v;
  return vars;
}

// The tokens.css text, exactly. Run `node frontend/src/theme/writeTokensCss.mjs` after changing a token.
export function tokensCss() {
  const lines = Object.entries(cssVariables()).map(([k, v]) => `  ${k}: ${v};`);
  return `/* Generated from theme/tokens.js by theme/writeTokensCss.mjs; do not edit by hand (tests/frontend_tokens.mjs checks parity). */\n:root {\n${lines.join('\n')}\n}\n`;
}
