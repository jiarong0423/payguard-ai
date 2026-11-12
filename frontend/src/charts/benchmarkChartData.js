// Pure helpers for the guide benchmark charts. The numbers come only from data/guide_benchmark_v1.json,
// which is generated from docs/evidence/guide_benchmark_v1.json (tools/run_guide_benchmark.py).

import { axisText, chartColor, noGrid, valueGrid, valueLabel } from './chartTheme.js';

// (vteam viz 2026-11-12) Was indigo on white. Now the design steps run through the categorical layers toward charcoal
// (olive, chestnut, charcoal = the current flow); every comparison (every sentence to the AI, a plain form, a dropped
// step) is the usual-value grey (viz.base, 3.7:1 on the paper). All colours come from chartTheme.js (tokens).
const [CAT_CHARCOAL, CAT_OLIVE, CAT_CHESTNUT] = chartColor.series;
const STEP_FILLS = [chartColor.usual, CAT_OLIVE, CAT_CHESTNUT, CAT_CHARCOAL];
const COMPARE_FILL = chartColor.usual;
const BASE_FILL = chartColor.usual;
const DROPPED_FILL = chartColor.usual;
const KEPT_FILL = CAT_CHARCOAL;

// The every-sentence row is the case count (one call for each one-sentence case); the flows in
// docs/evidence/GUIDE_BENCHMARK.md count calls in the flow simulation. The headline compares two simulated flows (Q7)
// and names the every-sentence figure for what it is. Live model replies are a separate record (GUIDE_STRESS_TEST.md).
const DERIVED_FLOWS = new Set(['every_sentence_to_ai']);

export function callRows(benchmark) {
  return benchmark.flows.map((flow) => ({ label: DERIVED_FLOWS.has(flow.id) ? `${flow.label} (1 per case)` : flow.label, calls: flow.model_calls }));
}

export function callSaving(benchmark) {
  const measured = benchmark.flows.filter((flow) => !DERIVED_FLOWS.has(flow.id));
  const all = measured[0].model_calls;
  const current = measured[measured.length - 1].model_calls;
  const computed = benchmark.flows.find((flow) => DERIVED_FLOWS.has(flow.id))?.model_calls ?? null;
  return { all, current, baseline: measured[0].label, percent: Math.round((1 - current / all) * 100),
    computed, computedPercent: computed ? Math.round((1 - current / computed) * 100) : null };
}

export function roundRows(benchmark) {
  return [
    { label: 'Plain form', rounds: benchmark.form_only_rounds, kind: 'base' },
    ...benchmark.flows.filter((flow) => flow.rounds !== null).map((flow) => ({ label: flow.label, rounds: flow.rounds, kind: 'flow' })),
  ];
}

export function historyRows(benchmark) {
  return benchmark.history_blind_v4.map((row) => ({ label: `${row.step}`, rounds: row.rounds, kept: row.kept, commit: row.commit }));
}

export function wrongValuesTotal(benchmark) {
  return benchmark.flows.filter((flow) => flow.wrong_honest !== null)
    .reduce((sum, flow) => sum + flow.wrong_honest + flow.wrong_careless, 0);
}

const AXIS_LABEL = { ...axisText, fontSize: 13 };
// Phone width (a 375 px screen gives a chart about 330 px): AG Charts clipped long category labels at the left
// edge and cut titles short, so below NARROW_PX labels and titles get explicit line breaks at word boundaries.
export const NARROW_PX = 520;
export function wrapWords(text, width) {
  const lines = [];
  for (const word of String(text).split(' ')) {
    const last = lines.at(-1);
    if (last !== undefined && (last + ' ' + word).length <= width) lines[lines.length - 1] = `${last} ${word}`;
    else lines.push(word);
  }
  return lines.join('\n');
}
const isNarrow = (container) => (container?.clientWidth ?? 800) < NARROW_PX;
const categoryLabel = (container, { stepNumbers = false } = {}) => (isNarrow(container)
  ? { ...AXIS_LABEL, fontSize: 12, autoRotate: false, avoidCollisions: false,
    formatter: ({ value }) => (stepNumbers ? String(value).split(' ')[0] : wrapWords(value, 14)) }
  // (2026-11-11, 768px review) A long label ("+ topology, one Save, summary on last round") was cut at the left edge on
  // tablets too: wider charts wrap labels over 30 characters onto two lines.
  : { ...AXIS_LABEL, autoRotate: false, formatter: ({ value }) => (String(value).length > 30 ? wrapWords(value, 26) : String(value)) });
// Titles and subtitles may take two lines at phone width instead of being cut short.
const captionFit = (container, lines) => (isNarrow(container) ? { wrapping: 'on-space', maxHeight: lines * 22 } : {});
// Room for the value label outside the longest bar.
export const headroom = (values) => Math.ceil((Math.max(...values) * 1.12) / 100) * 100;
const TITLE = (text, container) => ({ text, fontSize: 16, fontWeight: 700, color: chartColor.ink, ...captionFit(container, 2) });
const SUBTITLE = { fontSize: 13, color: chartColor.muted };

export function callChartOptions(benchmark, container) {
  return {
    container,
    data: callRows(benchmark),
    title: TITLE('Model calls for the same 268 seller sentences', container),
    subtitle: { text: 'Lower is cheaper · grey: the comparison · rules and Python settle what they can before any model call', ...SUBTITLE, ...captionFit(container, 3) },
    background: { fill: chartColor.plot },
    series: [{
      type: 'bar', direction: 'horizontal', xKey: 'label', yKey: 'calls', yName: 'Model calls', cornerRadius: 0,
      label: { enabled: true, ...valueLabel, placement: 'outside-end' },
      // (vteam viz) The every-sentence row is labelled "... (1 per case)", so an exact label match missed it and the bar
      // fell back to AG Charts' default blue. Match the flow by its label prefix; the first flow is the comparison.
      itemStyler: ({ datum }) => { const index = benchmark.flows.findIndex((flow) => String(datum.label).startsWith(flow.label));
        return { fill: index <= 0 ? COMPARE_FILL : STEP_FILLS[index] }; },
    }],
    axes: { x: { type: 'category', position: 'left', label: categoryLabel(container), gridLine: noGrid },
      y: { type: 'number', position: 'bottom', min: 0, max: headroom(callRows(benchmark).map((row) => row.calls)), label: AXIS_LABEL, gridLine: valueGrid } },
    legend: { enabled: false },
  };
}

export function roundChartOptions(benchmark, container) {
  return {
    container,
    data: roundRows(benchmark),
    title: TITLE('Guide rounds to finish, 268 cases', container),
    subtitle: { text: 'Grey bar: the same items as a plain fixed-input form', ...SUBTITLE, ...captionFit(container, 3) },
    background: { fill: chartColor.plot },
    series: [{
      type: 'bar', direction: 'horizontal', xKey: 'label', yKey: 'rounds', yName: 'Rounds', cornerRadius: 0,
      label: { enabled: true, ...valueLabel, placement: 'outside-end' },
      itemStyler: ({ datum }) => ({ fill: datum.kind === 'base' ? BASE_FILL : STEP_FILLS[benchmark.flows.findIndex((flow) => flow.label === datum.label)] }),
    }],
    axes: { x: { type: 'category', position: 'left', label: categoryLabel(container), gridLine: noGrid },
      y: { type: 'number', position: 'bottom', min: 0, max: headroom(roundRows(benchmark).map((row) => row.rounds)), label: AXIS_LABEL, gridLine: valueGrid } },
    legend: { enabled: false },
  };
}

export function historyChartOptions(benchmark, container) {
  return {
    container,
    data: historyRows(benchmark),
    title: TITLE('Each design step on the clean blind set (40 cases)', container),
    subtitle: { text: `Charcoal: kept · grey: tried and dropped · dashed line: plain form (${benchmark.history_form_only_rounds})${isNarrow(container) ? ` · steps: ${historyRows(benchmark).map((row) => row.label).join(' · ')}` : ''}`,
      ...SUBTITLE, ...captionFit(container, isNarrow(container) ? 5 : 3) },
    background: { fill: chartColor.plot },
    series: [{
      type: 'bar', xKey: 'label', yKey: 'rounds', yName: 'Rounds', cornerRadius: 0,
      label: { enabled: true, ...valueLabel, placement: 'outside-end' },
      itemStyler: ({ datum }) => ({ fill: datum.kept ? KEPT_FILL : DROPPED_FILL }),
    }],
    axes: {
      x: { type: 'category', position: 'bottom', label: categoryLabel(container, { stepNumbers: true }), gridLine: noGrid },
      y: {
        type: 'number', position: 'left', min: 0, label: AXIS_LABEL, gridLine: valueGrid,
        crossLines: [{ type: 'line', value: benchmark.history_form_only_rounds, stroke: chartColor.muted, strokeWidth: 1.5, lineDash: [6, 4],
          // (vteam viz) Phone: the label collided with the value labels of bars 4 and 5; the subtitle already names the line.
          label: { enabled: !isNarrow(container), text: 'Plain form', position: 'top-right', color: chartColor.muted, fontSize: 13 } }],
      },
    },
    legend: { enabled: false },
  };
}
