import { useEffect, useMemo, useRef, useState } from 'react';
import {
  AgCharts,
  BarSeriesModule,
  CartesianChartModule,
  CategoryAxisModule,
  CrossLinesModule,
  LegendModule,
  LineSeriesModule,
  ModuleRegistry,
  NumberAxisModule,
} from 'ag-charts-community';
import { buildMonthlyHistory, buildVelocityHourlyRows, hoursAbove, peakHourOf, monthlyChartOptions, money, percent, rangeLabel, velocityChartOptions } from './velocityChartData.js';
import './charts.css';

// Only the AG Charts Community modules this chart needs, so the lazy chunk stays small.
ModuleRegistry.registerModules([CartesianChartModule, BarSeriesModule, LineSeriesModule, CategoryAxisModule, NumberAxisModule, CrossLinesModule, LegendModule]);

export default function VelocityChart({ velocity, transactions, compact = false }) {
  const containerRef = useRef(null);
  const chartRef = useRef(null);
  const monthlyRef = useRef(null);
  const monthlyChartRef = useRef(null);
  const [view, setView] = useState('hourly');
  const [mark, setMark] = useState('');
  const [hour, setHour] = useState(null); // (vteam viz) the clicked hour, shown in the frosted detail
  // (vteam viz r7 T5) Hours in the viewer's own zone, the zone the facts above the chart use (App.jsx dateLabel).
  const offsetMinutes = useMemo(() => -new Date(velocity?.window_end || 0).getTimezoneOffset(), [velocity?.window_end]);
  const model = useMemo(() => buildVelocityHourlyRows(velocity, transactions, { offsetMinutes }), [velocity, transactions, offsetMinutes]);
  const monthly = useMemo(() => buildMonthlyHistory(velocity), [velocity]);
  const currentMonth = monthly.rows[monthly.rows.length - 1];
  const spikeTotal = model.rows.filter((row) => row.window === 'spike').reduce((sum, row) => sum + row.spike, 0);
  const peak = peakHourOf(model.rows);
  const overCount = hoursAbove(model.rows, model.reviewLine).length;
  const baselineRow = model.rows.find((row) => row.window === 'baseline');

  useEffect(() => {
    if (!containerRef.current || model.rows.length === 0) return undefined;
    const options = velocityChartOptions(model, containerRef.current, { compact, mark, onPick: setHour });
    if (chartRef.current) chartRef.current.update(options);
    else chartRef.current = AgCharts.create(options);
    return undefined;
  }, [model, compact, mark]);

  useEffect(() => {
    if (!monthlyRef.current || monthly.rows.length === 0) return undefined;
    const options = monthlyChartOptions(monthly, monthlyRef.current);
    if (monthlyChartRef.current) monthlyChartRef.current.update(options);
    else monthlyChartRef.current = AgCharts.create(options);
    return undefined;
  }, [monthly]);

  useEffect(() => () => {
    chartRef.current?.destroy();
    chartRef.current = null;
    monthlyChartRef.current?.destroy();
    monthlyChartRef.current = null;
  }, []);

  if (model.rows.length === 0) return null;
  // Hourly or Monthly, one at a time (plan r2 B8); both charts stay mounted and the hidden one keeps its test ids.
  const choose = (next) => {
    setView(next);
    if (next === 'monthly') window.requestAnimationFrame(() => monthlyChartRef.current?.resize?.());
  };
  return (<div className="velocity-chart-wrap">
    {/* (vteam viz r7 T5) The Hourly / Monthly switch heads the chart: first in the DOM and first on screen (top right of
        the chart's title row from 1024px, its own row above the chart below that); the highlight buttons follow the
        plot. DOM order = visual order at every width (a11y phase 2 item 8). */}
    {monthly.rows.length > 0 && <div className="segmented tg-seg velocity-period" role="tablist" aria-label="Chart period" data-testid="velocity-monthly-details">
      {[['hourly', 'Hourly'], ['monthly', 'Monthly']].map(([key, label]) => <button key={key} type="button" role="tab" id={`velocity-period-${key}`} aria-selected={view === key} aria-controls={`velocity-period-pane-${key}`} className={view === key ? 'is-active' : ''} onClick={() => choose(key)}>{label}</button>)}
    </div>}
    <figure id="velocity-period-pane-hourly" role="tabpanel" aria-labelledby="velocity-period-hourly" hidden={view !== 'hourly'} className="velocity-chart" data-testid="velocity-chart" aria-label="Hourly amount chart, baseline window versus spike window">
      <div className="velocity-chart-plot">
        <div ref={containerRef} className="velocity-chart-canvas" />
      </div>
      {/* (fix F3 D-P17) The hour detail sits under the plot, so every bar stays visible and clickable while it is open. */}
      {hour && <HourDetail row={hour} model={model} onClose={() => setHour(null)} />}
      <div className="velocity-mark-chips" role="group" aria-label="Highlight on the chart" data-testid="velocity-mark-chips">
        <button type="button" aria-pressed={mark === 'peak'} disabled={!peak} data-testid="velocity-mark-peak" onClick={() => setMark(mark === 'peak' ? '' : 'peak')}>Highlight peak hour <span>{peak ? 1 : 0}</span></button>
        <button type="button" aria-pressed={mark === 'over'} disabled={!overCount} data-testid="velocity-mark-over" onClick={() => setMark(mark === 'over' ? '' : 'over')}>Highlight hours above the line <span>{overCount}</span></button>
        <button type="button" disabled={!mark} data-testid="velocity-mark-reset" onClick={() => setMark('')}>Reset</button>
      </div>
      {mark === 'peak' && peak && <p className="velocity-mark-note" role="status" aria-live="polite" data-testid="velocity-mark-note">Peak hour {peak.label.replace(' ▲', '')} {model.zone}: {money(peak.spike, model.currency)}.</p>}
      <figcaption data-testid="velocity-chart-summary">
        Spike {money(spikeTotal, model.currency)} vs usual {baselineRow ? `${money(baselineRow.baseline, model.currency)}/h` : '—'}. No PayPal action predicted.
      </figcaption>
    </figure>
    {monthly.rows.length > 0 && <figure id="velocity-period-pane-monthly" role="tabpanel" aria-labelledby="velocity-period-monthly" hidden={view !== 'monthly'} className="velocity-chart" data-testid="velocity-monthly-chart" aria-label="Monthly amount with a three-month average and the change versus the previous month">
      <div ref={monthlyRef} className="velocity-chart-canvas" />
      <figcaption data-testid="velocity-monthly-summary">
        The month barely moves ({percent(currentMonth.change)} vs last month) because the spike is a few hours. That is why the review compares hours. Illustrative demo history.
      </figcaption>
    </figure>}
  </div>);
}

// (vteam viz 2026-11-12, CONSENSUS s4c) The clicked hour, on a frosted panel directly under the plot (fix F3 D-P17): the one
// chart place that uses the frosted surface (.tg-glass, components.css): opacity .92, blur 8px; without backdrop-filter or
// with reduced transparency it is the plain panel colour. Text is ink / muted only; the state word carries a ▲.
function HourDetail({ row, model, onClose }) {
  const isSpike = row.window === 'spike';
  const value = isSpike ? row.spike : row.baseline;
  const over = isSpike && model.reviewLine !== null && row.spike > model.reviewLine;
  return (
    <aside className="velocity-hour-pop tg-glass" role="status" aria-live="polite" aria-label="Selected hour" data-testid="velocity-hour-detail">
      <p className="velocity-hour-pop__when">{isSpike ? 'Spike window' : 'Usual hour'} · {rangeLabel(row, model.offsetMinutes)}</p>
      <button type="button" className="velocity-hour-pop__close" onClick={onClose} data-testid="velocity-hour-close">Close</button>
      <p className="velocity-hour-pop__value">{money(value, model.currency)}{isSpike ? '' : '/h'}
        <span className="velocity-hour-pop__meta">{isSpike ? <>{row.captures ?? 0} orders · {over ? <strong>▲ above the review line</strong> : 'under the review line'}</> : 'synthetic baseline rate'}</span></p>
    </aside>
  );
}
