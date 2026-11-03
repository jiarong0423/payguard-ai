import { useEffect, useRef } from 'react';
import {
  AgCharts,
  BarSeriesModule,
  CartesianChartModule,
  CategoryAxisModule,
  CrossLinesModule,
  LocaleModule,
  ModuleRegistry,
  NumberAxisModule,
} from 'ag-charts-community';
import benchmark from '../data/guide_benchmark_v1.json';
import { callChartOptions, callSaving, historyChartOptions, roundChartOptions, wrongValuesTotal } from './benchmarkChartData.js';
import './charts.css';

// LocaleModule carries the chart names below (attack r21).
ModuleRegistry.registerModules([CartesianChartModule, BarSeriesModule, CategoryAxisModule, NumberAxisModule, CrossLinesModule, LocaleModule]);

// Phone width: wrapped labels need taller charts (see NARROW_PX in benchmarkChartData.js).
const NARROW_SCREEN = typeof window !== 'undefined' && window.matchMedia('(max-width: 560px)').matches;

// AG Charts names its canvas "chart, 1 series" and its focusable surface (div.ag-charts-swapchain, role img,
// tabindex 0) "interactive chart", so the three charts had no name of their own (attack r21). The canvas takes this
// chart's label through the locale hook (every other text keeps AG Charts' default: undefined falls back to it).
// The surface reads its first text before options apply, so once the chart has drawn, the hidden label element it
// points at (aria-labelledby) gets the chart's label. The wrapper must not be an img: an img's children are
// presentational, which also hid the focusable surface's name (since attack r23 it has no role at all).
const CHART_NAME_KEYS = new Set(['ariaInitSeriesArea', 'ariaAnnounceChart']);
export function namedChartOptions(options, label) {
  return { ...options, locale: { getLocaleText: ({ key }) => (CHART_NAME_KEYS.has(key) ? label : undefined) } };
}
// That left each chart three times in the accessibility tree under the same name: this wrapper (figure), AG Charts'
// canvas proxy (figure) and the focusable surface (img) (attack r22). Renaming the surface still left two named nodes
// per chart, and the three surfaces shared one generic name (attack r23). Now each chart has exactly one named node:
// the focusable surface (img) carries this chart's own label, the proxy is presentational and the wrapper is a plain,
// unnamed div. The arrow-key hint goes in the surface's description, not its name.
export const FOCUS_SURFACE_HINT = 'Use the arrow keys to read each bar.';
function nameFocusSurfaces(container, label) {
  for (const surface of container.querySelectorAll('.ag-charts-swapchain[aria-labelledby]')) {
    const name = document.getElementById(surface.getAttribute('aria-labelledby'));
    if (name && name.textContent !== label) name.textContent = label;
    if (surface.getAttribute('aria-description') !== FOCUS_SURFACE_HINT) surface.setAttribute('aria-description', FOCUS_SURFACE_HINT);
  }
  for (const proxy of container.querySelectorAll('.ag-charts-canvas-proxy')) {
    if (proxy.getAttribute('role') !== 'presentation') proxy.setAttribute('role', 'presentation');
    if (proxy.hasAttribute('aria-label')) proxy.removeAttribute('aria-label');
  }
}

function Chart({ build, testId, label, height = 260, narrowHeight = 360 }) {
  const ref = useRef(null);
  useEffect(() => {
    const container = ref.current;
    if (!container) return undefined;
    let live = true;
    const chart = AgCharts.create(namedChartOptions(build(benchmark, container), label));
    chart.waitForUpdate().then(() => { if (live) nameFocusSurfaces(container, label); }, () => {});
    // AG Charts may redraw its DOM (resize); the names are put back each time (attack r22).
    const observer = new MutationObserver(() => nameFocusSurfaces(container, label));
    observer.observe(container, { childList: true, subtree: true, attributes: true, attributeFilter: ['role', 'aria-label', 'aria-description'] });
    return () => { live = false; observer.disconnect(); chart.destroy(); };
  }, [build, label]);
  return <div ref={ref} className="benchmark-chart-canvas" style={{ height: NARROW_SCREEN ? narrowHeight : height }} data-testid={testId} />; // unnamed: the surface inside carries the label (attack r23)
}

export default function BenchmarkCharts() {
  const saving = callSaving(benchmark);
  const wrong = wrongValuesTotal(benchmark);
  const history = benchmark.history_blind_v4.filter((row) => row.kept);
  return (
    <section className="benchmark-charts" data-testid="benchmark-charts" aria-label="How the guide was measured">
      <ul className="benchmark-facts">
        <li><strong>Drift control: {wrong} wrong values</strong> reached the form in {benchmark.cases} simulated cases, even when the simulated seller confirmed everything without reading. The AI can only pre-fill; rules and the seller decide.</li>
        <li><strong>Cost: {saving.percent}% fewer model calls</strong> than the earlier measured flow ({saving.baseline}: {saving.all} to {saving.current}){saving.computed ? <>, and {saving.computedPercent}% fewer than sending every sentence to the AI ({saving.computed}: one call for each case)</> : null}; rules and Python settle what they can first.</li>
        <li><strong>Live models: 601 real model replies</strong> in 16 runs, 273 of them through the Gemini API, scored for drift; confident wrong claims fell from 1-2 per run in early rounds to 0 in all three final-round runs (GUIDE_STRESS_TEST.md).</li>
        <li><strong>Rounds {history[0].rounds} to {history[history.length - 1].rounds}</strong> across the design steps on the clean blind set ({Math.round((1 - history[history.length - 1].rounds / history[0].rounds) * 100)}% fewer), now below a plain form's {benchmark.history_form_only_rounds}; over all {benchmark.cases} cases {benchmark.flows[benchmark.flows.length - 1].rounds} versus {benchmark.form_only_rounds} for a plain form, with no wrong value filled.</li>
      </ul>
      <Chart build={callChartOptions} testId="benchmark-calls" label={`Model calls: ${saving.baseline} ${saving.all}, current flow ${saving.current}; every sentence to the AI ${saving.computed}, one call for each case`} />
      <Chart build={roundChartOptions} testId="benchmark-rounds" label="Guide rounds to finish compared with a plain form" />
      <Chart build={historyChartOptions} testId="benchmark-history" label="Rounds for each design step on the clean blind set" height={300} />
      <p className="benchmark-note">Simulated sellers on one-sentence test cases (four blind sets written by people who never saw the rules); not a study of real sellers. Source: {benchmark.source}. Charts: AG Charts Community.</p>
    </section>
  );
}
