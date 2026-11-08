// Shared AG Charts theme and AG Grid theme params built from tokens. Plain objects only: no AG import here,
// so importing this module never pulls a chart or grid library into a bundle.
//   AG Charts:  AgCharts.create({ ...options, theme: chartTheme() })
//   AG Grid:    themeQuartz.withParams(gridParams())   (gridParams({ phone: true }) under 640 px)
import { categorical, color, font, layout, type } from './tokens.js';

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

export function gridParams({ phone = false } = {}) {
  return {
    accentColor: color.accent,
    backgroundColor: color.panel,
    foregroundColor: color.ink,
    borderColor: color.rule,
    headerBackgroundColor: color.recede,
    headerTextColor: color.muted,
    selectedRowBackgroundColor: color.accentSelected,
    fontFamily: font.sans,
    fontSize: type.gridCell,
    headerFontSize: type.meta,
    rowHeight: phone ? layout.gridRowPhone : layout.gridRow,
    headerHeight: phone ? layout.gridRowPhone : layout.gridRow,
    wrapperBorderRadius: 12,
    borderRadius: 8,
  };
}
