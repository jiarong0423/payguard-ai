// Shared AG Charts theme and AG Grid theme params built from tokens. Plain objects only: no AG import here,
// so importing this module never pulls a chart or grid library into a bundle.
//   AG Charts:  AgCharts.create({ ...options, theme: chartTheme() })
//   AG Grid:    themeQuartz.withParams(gridParams())   (gridParams({ phone: true }) under 640 px)
import { categorical, color, font, layout, radius, space, type } from './tokens.js';

// Render effects: a short entry animation and a hover emphasis (the hovered bar gets an outline, the others recede).
// The animation is switched off when the visitor asks the system for reduced motion.
function reducedMotion() {
  try { return typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return false; }
}

export function chartTheme({ palette = categorical } = {}) {
  const label = { fontFamily: font.sans, fontSize: type.chartAxis, color: color.muted };
  return {
    baseTheme: 'ag-default',
    palette: { fills: [...palette], strokes: [...palette] },
    params: { fontFamily: font.sans, fontSize: type.chartAxis, foregroundColor: color.ink, backgroundColor: 'transparent' },
    overrides: {
      common: {
        background: { visible: false },
        animation: { enabled: !reducedMotion(), duration: 800 },
        title: { fontFamily: font.sans, fontSize: type.chartTitle, fontWeight: 600, color: color.ink, textAlign: 'left' },
        subtitle: { ...label },
        legend: { item: { label: { ...label } } },
        axes: {
          category: { label: { ...label }, title: { ...label }, line: { stroke: color.rule }, gridLine: { style: [{ stroke: color.rule }] } },
          number: { label: { ...label }, title: { ...label }, line: { stroke: color.rule }, gridLine: { style: [{ stroke: color.rule }] } },
          time: { label: { ...label }, title: { ...label }, line: { stroke: color.rule }, gridLine: { style: [{ stroke: color.rule }] } },
        },
      },
      bar: { series: { highlight: { highlightedItem: { stroke: color.ink, strokeWidth: 2 }, unhighlightedItem: { opacity: 0.55 } } } },
    },
  };
}

// The "context" colour for every mark except the one highlighted mark (spec section 6).
export const CONTEXT_MARK = color.context;

// (F2 2026-11-12, OFFICIAL_FIX_GUIDE s1-s2) The ONE grid theme for G1, G2, G4, G5 (grid/agGrid.jsx consoleGridTheme):
// square, receded 600-weight header, panel rows without zebra, 1px rule-soft row lines, Public Sans, charcoal focus.
// Every name below exists in ag-grid-community 36.2.0 (dist/types theming parts); headerFontFamily does not, so the
// header inherits fontFamily. inputHeight 44 = console input height (spec A); floatingFiltersHeight follows it.
export const GRID_INPUT_HEIGHT = 44;
export const GRID_FLOATING_FILTERS_HEIGHT = GRID_INPUT_HEIGHT + space[2] * 2;
export function gridParams({ phone = false, compact = false } = {}) {
  const hairline = { width: 1, style: 'solid', color: color.ruleSoft };
  return {
    accentColor: color.focus,
    rangeSelectionBorderColor: color.focus,
    focusShadow: { spread: layout.focusRing, color: color.focus },
    backgroundColor: color.panel,
    oddRowBackgroundColor: color.panel,
    rowHoverColor: color.rowHover,
    selectedRowBackgroundColor: color.sel,
    foregroundColor: color.ink,
    borderColor: color.rule,
    rowBorder: hairline,
    headerBackgroundColor: color.recede,
    headerTextColor: color.muted,
    headerFontWeight: 600,
    fontFamily: font.sans,
    cellFontFamily: font.sans,
    fontSize: compact ? type.meta : type.gridCell,
    headerFontSize: type.meta,
    rowHeight: phone ? layout.gridRowPhone : layout.gridRow,
    headerHeight: phone ? layout.gridRowPhone : layout.gridRow,
    cellHorizontalPadding: phone ? space[2] : space[3],
    wrapperBorderRadius: radius.card,
    borderRadius: radius.control,
    buttonBorderRadius: radius.control,
    checkboxBorderRadius: radius.control,
    inputBorderRadius: radius.control,
    inputHeight: GRID_INPUT_HEIGHT,
    inputBackgroundColor: color.panel,
    inputBorder: { width: 1, style: 'solid', color: color.controlLine },
    inputFocusBorder: { width: 1, style: 'solid', color: color.focus },
    inputPaddingStart: space[2],
    inputTextColor: color.ink,
    inputPlaceholderTextColor: color.muted,
  };
}
