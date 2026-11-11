// TradeGlot theme for AG Studio. (P1 2026-11-12) Colours come from the design tokens (theme/tokens.js, "Editorial
// Newsprint"): ink does the interactive jobs, newsprint surfaces and rules, the four greys as the chart palette.
// The indigo hex values that were written here (VISUAL_SPEC_r7 D2) are gone.
import { studioTheme } from 'ag-studio';
import { categorical, color } from '../theme/tokens.js';

export const PAYGUARD_ACCENT = Object.freeze({
  ink: color.ink, text: color.ink, muted: color.muted, subtle: color.subtle, accent: color.accent, accentDark: color.accentStrong,
  canvas: color.canvas, panel: color.panel, border: color.ruleSoft, grid: color.recede, tint: color.hover,
  selected: color.accentSelected,
  series: [...categorical],
});

const C = PAYGUARD_ACCENT;
const palette = Object.fromEntries(C.series.flatMap((color, index) => [
  [`chartPaletteFills${index + 1}Color`, color],
  [`chartPaletteStrokes${index + 1}Color`, color],
]));

export const payguardTheme = studioTheme.withParams({
  fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, sans-serif',
  fontSize: 14,
  textColor: C.text,
  foregroundColor: C.text,
  subtleTextColor: C.subtle,
  accentColor: C.accent,
  backgroundColor: C.panel,
  borderColor: C.border,
  borderRadius: 8,
  rowHoverColor: C.tint,
  // Small screens: let the canvas shrink to a phone width instead of Studio's 600/720 px minimums.
  studioMinWidth: 320,
  studioMinHeight: 480,
  studioCanvasMinWidth: 320,
  studioCanvasBackgroundColor: C.canvas,
  studioCanvasPadding: 16,
  studioWidgetPadding: 12,
  studioValueWidgetFontSize: 28,
  studioCanvasRowHeight: 16,
  studioCanvasFontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, sans-serif',
  studioWidgetBackgroundColor: C.panel,
  studioWidgetBorderRadius: 12,
  studioWidgetBorder: { color: C.border, width: 1 },
  studioWidgetTitleFontSize: 16,
  studioWidgetTitleFontWeight: 600,
  studioWidgetTitleTextColor: C.ink,
  studioWidgetSubtitleFontSize: 14,
  studioWidgetSubtitleTextColor: C.subtle,
  // Selected toggle: surface fill, ink rule and ink text (solid accent on accent text hid the label).
  studioToggleButtonActiveBackgroundColor: C.selected,
  studioToggleButtonActiveBorderColor: C.accent,
  studioToggleButtonActiveColor: C.ink,
  studioWidgetNoDataOverlayBackgroundColor: C.grid,
  gridHeaderBackgroundColor: C.grid,
  gridHeaderTextColor: C.muted,
  gridHeaderFontWeight: 600,
  gridOddRowBackgroundColor: C.panel,
  gridRowHoverColor: C.tint,
  gridAccentColor: C.accent,
  gridFontSize: 14,
  // Cases table rows: 40px (44 on phones), not Studio's 24px default (plan r2 F23).
  gridRowHeight: 40,
  chartTextColor: C.muted,
  chartSubtleTextColor: C.subtle,
  chartGridLineColor: C.canvas,
  chartAxisLineColor: C.border,
  chartAccentColor: C.accent,
  chartFontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, sans-serif',
  ...palette,
});

// Phones (<= 720 px): the AI panel takes the screen width and the canvas may shrink behind it, so nothing is
// clipped; the page shell returns to view mode after an answer so the canvas shows it.
export function compactTheme(viewportWidth) {
  return payguardTheme.withParams({
    studioMinWidth: 280,
    gridRowHeight: 44,
    studioCanvasMinWidth: 40,
    studioAiPanelWidth: Math.max(240, Math.min(viewportWidth - 72, 480)),
  });
}
