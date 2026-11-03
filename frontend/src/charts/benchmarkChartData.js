// Pure helpers for the guide benchmark charts. The numbers come only from data/guide_benchmark_v1.json,
// which is generated from docs/evidence/guide_benchmark_v1.json (tools/run_guide_benchmark.py).

// One hue that deepens with each design step; the comparison (every sentence to the AI, a plain form) in warm grey.
const STEP_FILLS = ['#a5b4fc', '#818cf8', '#6366f1', '#4338ca'];
const COMPARE_FILL = '#e7a98f';
const BASE_FILL = '#d6d3d1';
const DROPPED_FILL = '#d6d3d1';
const KEPT_FILL = '#6366f1';

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

const AXIS_LABEL = { fontSize: 13, color: '#475569' };
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
  : { ...AXIS_LABEL, autoRotate: false });
// Titles and subtitles may take two lines at phone width instead of being cut short.
const captionFit = (container, lines) => (isNarrow(container) ? { wrapping: 'on-space', maxHeight: lines * 22 } : {});
// Room for the value label outside the longest bar.
export const headroom = (values) => Math.ceil((Math.max(...values) * 1.12) / 100) * 100;
const TITLE = (text, container) => ({ text, fontSize: 16, fontWeight: 700, color: '#1e1b4b', ...captionFit(container, 2) });

export function callChartOptions(benchmark, container) {
  return {
    container,
    data: callRows(benchmark),
    title: TITLE('Model calls for the same 268 seller sentences', container),
    subtitle: { text: 'Lower is cheaper · rules and Python settle what they can before any model call', fontSize: 13, color: '#64748b', ...captionFit(container, 3) },
    background: { fill: '#ffffff' },
    series: [{
      type: 'bar', direction: 'horizontal', xKey: 'label', yKey: 'calls', yName: 'Model calls', cornerRadius: 6,
      label: { enabled: true, color: '#1e1b4b', fontSize: 13, fontWeight: 600, placement: 'outside-end' },
      itemStyler: ({ datum }) => ({ fill: datum.label === benchmark.flows[0].label ? COMPARE_FILL : STEP_FILLS[benchmark.flows.findIndex((flow) => flow.label === datum.label)] }),
    }],
    axes: { x: { type: 'category', position: 'left', label: categoryLabel(container) },
      y: { type: 'number', position: 'bottom', min: 0, max: headroom(callRows(benchmark).map((row) => row.calls)), label: AXIS_LABEL } },
    legend: { enabled: false },
  };
}

export function roundChartOptions(benchmark, container) {
  return {
    container,
    data: roundRows(benchmark),
    title: TITLE('Guide rounds to finish, 268 cases', container),
    subtitle: { text: 'Grey bar: the same items as a plain fixed-input form', fontSize: 13, color: '#64748b', ...captionFit(container, 3) },
    background: { fill: '#ffffff' },
    series: [{
      type: 'bar', direction: 'horizontal', xKey: 'label', yKey: 'rounds', yName: 'Rounds', cornerRadius: 6,
      label: { enabled: true, color: '#1e1b4b', fontSize: 13, fontWeight: 600, placement: 'outside-end' },
      itemStyler: ({ datum }) => ({ fill: datum.kind === 'base' ? BASE_FILL : STEP_FILLS[benchmark.flows.findIndex((flow) => flow.label === datum.label)] }),
    }],
    axes: { x: { type: 'category', position: 'left', label: categoryLabel(container) },
      y: { type: 'number', position: 'bottom', min: 0, max: headroom(roundRows(benchmark).map((row) => row.rounds)), label: AXIS_LABEL } },
    legend: { enabled: false },
  };
}

export function historyChartOptions(benchmark, container) {
  return {
    container,
    data: historyRows(benchmark),
    title: TITLE('Each design step on the clean blind set (40 cases)', container),
    subtitle: { text: `Indigo: kept · grey: tried and dropped · dashed line: plain form (${benchmark.history_form_only_rounds})${isNarrow(container) ? ` · steps: ${historyRows(benchmark).map((row) => row.label).join(' · ')}` : ''}`,
      fontSize: 13, color: '#64748b', ...captionFit(container, isNarrow(container) ? 5 : 3) },
    background: { fill: '#ffffff' },
    series: [{
      type: 'bar', xKey: 'label', yKey: 'rounds', yName: 'Rounds', cornerRadius: 6,
      label: { enabled: true, color: '#1e1b4b', fontSize: 13, fontWeight: 600, placement: 'outside-end' },
      itemStyler: ({ datum }) => ({ fill: datum.kept ? KEPT_FILL : DROPPED_FILL }),
    }],
    axes: {
      x: { type: 'category', position: 'bottom', label: categoryLabel(container, { stepNumbers: true }) },
      y: {
        type: 'number', position: 'left', min: 0, label: AXIS_LABEL,
        crossLines: [{ type: 'line', value: benchmark.history_form_only_rounds, stroke: '#c2410c', strokeWidth: 1.5, lineDash: [6, 4],
          label: { text: 'Plain form', position: 'inside-bottom-right', color: '#9a3412', fontSize: 13 } }],
      },
    },
    legend: { enabled: false },
  };
}
