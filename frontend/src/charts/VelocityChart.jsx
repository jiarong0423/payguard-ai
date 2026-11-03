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
import { buildMonthlyHistory, buildVelocityHourlyRows, monthlyChartOptions, money, percent, velocityChartOptions } from './velocityChartData.js';
import './charts.css';

// Only the AG Charts Community modules this chart needs, so the lazy chunk stays small.
ModuleRegistry.registerModules([CartesianChartModule, BarSeriesModule, LineSeriesModule, CategoryAxisModule, NumberAxisModule, CrossLinesModule, LegendModule]);

export default function VelocityChart({ velocity, transactions, compact = false }) {
  const containerRef = useRef(null);
  const chartRef = useRef(null);
  const monthlyRef = useRef(null);
  const monthlyChartRef = useRef(null);
  const [view, setView] = useState('hourly');
  const model = useMemo(() => buildVelocityHourlyRows(velocity, transactions), [velocity, transactions]);
  const monthly = useMemo(() => buildMonthlyHistory(velocity), [velocity]);
  const currentMonth = monthly.rows[monthly.rows.length - 1];
  const spikeTotal = model.rows.filter((row) => row.window === 'spike').reduce((sum, row) => sum + row.spike, 0);
  const baselineRow = model.rows.find((row) => row.window === 'baseline');

  useEffect(() => {
    if (!containerRef.current || model.rows.length === 0) return undefined;
    const options = velocityChartOptions(model, containerRef.current, { compact });
    if (chartRef.current) chartRef.current.update(options);
    else chartRef.current = AgCharts.create(options);
    return undefined;
  }, [model, compact]);

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
  return (<>
    {monthly.rows.length > 0 && <div className="segmented velocity-period" role="tablist" aria-label="Chart period" data-testid="velocity-monthly-details">
      {[['hourly', 'Hourly'], ['monthly', 'Monthly']].map(([key, label]) => <button key={key} type="button" role="tab" id={`velocity-period-${key}`} aria-selected={view === key} aria-controls={`velocity-period-pane-${key}`} className={view === key ? 'is-active' : ''} onClick={() => choose(key)}>{label}</button>)}
    </div>}
    <figure id="velocity-period-pane-hourly" role="tabpanel" aria-labelledby="velocity-period-hourly" hidden={view !== 'hourly'} className="velocity-chart" data-testid="velocity-chart" aria-label="Hourly amount chart, baseline window versus spike window">
      <div ref={containerRef} className="velocity-chart-canvas" />
      <figcaption data-testid="velocity-chart-summary">
        Spike {money(spikeTotal)} {model.currency} vs usual {baselineRow ? `${money(baselineRow.baseline)} ${model.currency}/h` : '—'}. No PayPal action predicted.
      </figcaption>
    </figure>
    {monthly.rows.length > 0 && <figure id="velocity-period-pane-monthly" role="tabpanel" aria-labelledby="velocity-period-monthly" hidden={view !== 'monthly'} className="velocity-chart" data-testid="velocity-monthly-chart" aria-label="Monthly amount with a three-month average and the change versus the previous month">
      <div ref={monthlyRef} className="velocity-chart-canvas" />
      <figcaption data-testid="velocity-monthly-summary">
        The month barely moves ({percent(currentMonth.change)} vs last month) because the spike is a few hours. That is why the review compares hours. Illustrative demo history.
      </figcaption>
    </figure>}
  </>);
}
