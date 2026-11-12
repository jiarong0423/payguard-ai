// (vteam viz 2026-11-12) One place for every AG Charts colour, read from theme/tokens.js: no literal hex in the chart
// option builders. Loaded only with the lazy chart chunks (VelocityChart, BenchmarkCharts), never on first load.
//
// Roles (CONSENSUS.md s2-s3):
// - plot sits on the page paper (viz.bg = canvas) so the faint ledger grid (paperGrid, 1.15:1, decoration only) shows;
// - non-semantic series use the categorical layers --pg-cat-1..4 (charcoal, olive, chestnut, khaki) and never red,
//   green or amber; khaki (2.4:1) is for lines only, never a bar fill;
// - the comparison / usual-value bars use viz.base (3.7:1 on canvas);
// - above the review line = warn (check first), always with a ▲ and a direct label, never colour alone.
import { categorical, color, viz } from '../theme/tokens.js';

export const chartColor = Object.freeze({
  plot: viz.bg,
  ink: color.ink,
  muted: color.muted,
  grid: color.paperGrid,
  gridStrong: color.khaki,
  usual: viz.base,
  under: color.context,
  over: viz.alert,
  reviewLine: color.warn,
  outline: color.rule,
  panel: color.panel,
  series: categorical,
});

// Horizontal ledger lines only: the value axis carries the grid, the category axis has none.
export const valueGrid = Object.freeze({ enabled: true, width: 1, style: [{ stroke: chartColor.grid, lineDash: [] }] });
export const noGrid = Object.freeze({ enabled: false });

export const axisText = Object.freeze({ fontSize: 12, color: chartColor.muted });
export const valueLabel = Object.freeze({ color: chartColor.ink, fontSize: 13, fontWeight: 600 });
