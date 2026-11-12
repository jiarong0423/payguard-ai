// Pure helpers for the stage 02 hourly chart. No network, no clock: everything is
// derived from the backend `velocity` block and the synthetic `transactions` list.

import { axisText, chartColor, noGrid, valueGrid } from './chartTheme.js';
import { money, zoneLabel } from '../theme/format.js';

// (vteam viz) Amounts use the site format from theme/format.js: "USD 500.00" (code first), never "500.00 USD".
export { money };

const HOUR_MS = 3600 * 1000;
const MAX_BASELINE_BUCKETS = 48;
const MAX_SPIKE_BUCKETS = 24;

function toMs(value) {
  if (typeof value !== 'string') return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : null;
}

function toCents(value) {
  const number = Number(value);
  return Number.isFinite(number) ? Math.round(number * 100) : null;
}

// (vteam viz r7 T5) One time zone per screen: the chart reads hours in the viewer's own zone, like the facts above it
// ("Window ends ... GMT+8"). offsetMinutes 0 keeps UTC (tests, server-side use); the chart passes the viewer's offset.
export function chartZone(offsetMinutes = 0) {
  return zoneLabel(offsetMinutes); // the same label dateTimeLabel prints (UTC at offset 0)
}
export function hourLabel(ms, offsetMinutes = 0) {
  const date = new Date(ms + offsetMinutes * 60000);
  return `${String(date.getUTCHours()).padStart(2, '0')}:${String(date.getUTCMinutes()).padStart(2, '0')}`;
}

/**
 * Build one row per hour: the baseline window first, then the spike (observation) window.
 * Baseline rows carry the usual rate (demo) the velocity signal compares against;
 * spike rows carry the captured amount summed from demo transactions in that hour.
 * The spike window is left-open, right-closed, the same boundary the backend uses.
 */
export function buildVelocityHourlyRows(velocity, transactions, { offsetMinutes = 0 } = {}) {
  if (!velocity || typeof velocity !== 'object') return { rows: [], reviewLine: null, currency: 'USD' };
  const baselineStart = toMs(velocity.baseline_window_start);
  const baselineEnd = toMs(velocity.baseline_window_end);
  const spikeStart = toMs(velocity.window_start);
  const spikeEnd = toMs(velocity.window_end);
  const baselineRateCents = toCents(velocity.baseline_amount_per_hour);
  const thresholdNumber = Number(velocity.threshold);
  const currency = velocity.currency || 'USD';
  const rows = [];

  if (baselineStart !== null && baselineEnd !== null && baselineEnd > baselineStart && baselineRateCents !== null) {
    const buckets = Math.min(MAX_BASELINE_BUCKETS, Math.ceil((baselineEnd - baselineStart) / HOUR_MS));
    for (let index = 0; index < buckets; index += 1) {
      const start = baselineStart + index * HOUR_MS;
      rows.push({
        key: `baseline-${index}`,
        label: hourLabel(start, offsetMinutes),
        window: 'baseline',
        start: new Date(start).toISOString(),
        end: new Date(Math.min(start + HOUR_MS, baselineEnd)).toISOString(),
        baseline: baselineRateCents / 100,
        spike: null,
      });
    }
  }

  if (spikeStart !== null && spikeEnd !== null && spikeEnd > spikeStart) {
    const buckets = Math.min(MAX_SPIKE_BUCKETS, Math.ceil((spikeEnd - spikeStart) / HOUR_MS));
    const sums = new Array(buckets).fill(0);
    const counts = new Array(buckets).fill(0);
    for (const transaction of Array.isArray(transactions) ? transactions : []) {
      if (!transaction || (velocity.currency && transaction.currency !== velocity.currency)) continue;
      const at = toMs(transaction.occurred_at);
      const cents = toCents(transaction.amount);
      if (at === null || cents === null || at <= spikeStart || at > spikeEnd) continue;
      const index = Math.min(buckets - 1, Math.floor((at - spikeStart - 1) / HOUR_MS));
      sums[index] += cents;
      counts[index] += 1;
    }
    for (let index = 0; index < buckets; index += 1) {
      const start = spikeStart + index * HOUR_MS;
      rows.push({
        key: `spike-${index}`,
        label: `${hourLabel(start, offsetMinutes)} ▲`,
        window: 'spike',
        start: new Date(start).toISOString(),
        end: new Date(Math.min(start + HOUR_MS, spikeEnd)).toISOString(),
        baseline: null,
        spike: sums[index] / 100,
        captures: counts[index],
      });
    }
  }

  const reviewLine = baselineRateCents !== null && Number.isFinite(thresholdNumber)
    ? Math.round(baselineRateCents * thresholdNumber) / 100
    : null;
  return { rows, reviewLine, currency, offsetMinutes, zone: chartZone(offsetMinutes) };
}

// (P4 2026-11-12, review_FULL s3a) Token colours only, and each legend swatch is its bars' colour: every past hour is a
// thin bar at the usual rate (viz.base, 3.7:1 on the paper), a spike hour above the review line is amber (viz.alert,
// warn: "check first", not risk red) and is also marked with a ▲ and its multiple, a spike hour under it is grey
// (context), the review threshold is a 1px amber dashed line. (vteam viz) Colours come from chartTheme.js; the plot sits
// on the page paper with faint horizontal ledger lines. No teal, orange or indigo.
const BASELINE_FILL = chartColor.usual;
const SPIKE_FILL = chartColor.under;
const REVIEW_STROKE = chartColor.reviewLine;
const FLAG_FILL = chartColor.over;
const AVERAGE_STROKE = chartColor.muted;
const MONTH_STROKE = chartColor.ink;

// (r32 J5 P3-3) Chart titles and subtitles wrap onto up to three lines instead of being cut with an ellipsis at
// phone width.
const CAPTION_WRAP = Object.freeze({ wrapping: 'on-space', maxHeight: 60 });


export function rangeLabel(datum, offsetMinutes = 0) {
  const fmt = (iso) => hourLabel(Date.parse(iso), offsetMinutes);
  return `${fmt(datum.start)}–${fmt(datum.end)} ${chartZone(offsetMinutes)}`;
}

// compact: phones, where the page shows its own unpaginated legend (App.jsx PhoneChartLegend) because this one pages.
// The spike-window hour with the largest amount, and the hours above the review line (counts for the chart's highlight chips).
export function peakHourOf(rows) {
  const spikes = (rows || []).filter((row) => row.window === 'spike' && Number.isFinite(row.spike));
  return spikes.length ? spikes.reduce((best, row) => (row.spike > best.spike ? row : best)) : null;
}
export function hoursAbove(rows, reviewLine) {
  return reviewLine === null ? [] : (rows || []).filter((row) => row.window === 'spike' && row.spike > reviewLine);
}

// `mark`: '' (none), 'peak' (outline the largest hour, soften the rest) or 'over' (outline the hours above the review line).
// `onPick`: called with the clicked hour's row (vteam viz: the frosted hour detail), or omitted.
export function velocityChartOptions({ rows, reviewLine, currency, offsetMinutes = 0 }, container, { compact = false, mark = '', onPick = null } = {}) {
  const peak = mark === 'peak' ? peakHourOf(rows) : null;
  const picked = (datum) => (mark === 'peak' ? Boolean(peak) && datum.key === peak.key : mark === 'over' ? reviewLine !== null && datum.spike > reviewLine : true);
  const baselineRate = rows.find((row) => row.window === 'baseline')?.baseline || null;
  return {
    container,
    data: rows,
    title: { text: 'Hourly amount: baseline vs spike', fontSize: 14, fontWeight: 600, color: chartColor.ink, ...CAPTION_WRAP },
    // (r7 T5) Phone: one subtitle line, so the bars stay on the first screen under the period switch.
    subtitle: { text: compact ? 'Sample data · ▲ above the line · tap an hour' : 'Sample data · amber ▲ = above the review line · click an hour for its detail', fontSize: 12, color: chartColor.muted, ...CAPTION_WRAP },
    background: { fill: chartColor.plot },
    // (UI r5) left 8 -> 20: the rotated y-axis title ('USD per hour') lost its first letter at the canvas edge.
    padding: { top: 12, right: 16, bottom: 8, left: 20 },
    series: [
      {
        // (P4) Every past hour as a thin bar at the declared synthetic rate, so the spike reads against a row of usual hours.
        type: 'bar', xKey: 'label', yKey: 'baseline', yName: 'Usual hours', fill: BASELINE_FILL, stacked: true, cornerRadius: 0, strokeWidth: 0,
        // (vteam viz) With the clicked-hour panel (onPick) the default white tooltip is off: one detail layer, not two.
        tooltip: { enabled: !onPick, renderer: ({ datum }) => ({ heading: 'Baseline window', title: rangeLabel(datum, offsetMinutes),
          data: [{ label: 'Usual rate (demo)', value: `${money(datum.baseline, currency)}/h` }] }) },
      },
      {
        type: 'bar', xKey: 'label', yKey: 'spike', yName: 'Spike hour above the review line', fill: FLAG_FILL, stacked: true,
        cornerRadius: 0,
        itemStyler: ({ datum }) => {
          const base = reviewLine !== null && datum && datum.spike > reviewLine ? {} : { fill: SPIKE_FILL };
          if (!mark || !datum) return base;
          return picked(datum) ? { ...base, stroke: chartColor.outline, strokeWidth: 3 } : { ...base, fillOpacity: 0.3 };
        },
        // Direct label: the multiple of the usual rate; an hour above the review line also gets the ▲ (shape, not colour).
        label: { enabled: true, placement: 'outside-end', fontSize: 16, fontWeight: 700, color: chartColor.ink,
          formatter: ({ value }) => (value && baselineRate > 0 ? `${reviewLine !== null && value > reviewLine ? '▲ ' : ''}×${(value / baselineRate).toFixed(1)}` : '') },
        tooltip: { enabled: !onPick, renderer: ({ datum }) => ({ heading: 'Spike window', title: rangeLabel(datum, offsetMinutes),
          data: [{ label: 'Captured amount', value: money(datum.spike, currency) }, { label: 'Orders', value: String(datum.captures ?? 0) }] }) },
      },
    ],
    axes: {
      // (vteam viz r7 T5) The axis names the zone of its hours: the viewer's own, the same as the facts above the chart.
      x: { type: 'category', position: 'bottom', title: { text: `Hour (${chartZone(offsetMinutes)})`, ...axisText }, label: { ...axisText, autoRotate: false }, gridLine: noGrid },
      y: {
        type: 'number', position: 'left', min: 0, nice: true,
        title: { text: `${currency} per hour`, ...axisText },
        label: axisText, gridLine: valueGrid,
        crossLines: reviewLine === null ? [] : [{
          type: 'line', value: reviewLine, stroke: REVIEW_STROKE, strokeWidth: 1, lineDash: [4, 3],
          // (r32 J1 J4) On a phone the long label ran under the spike bar and its "USD/h" was hidden; the short one
          // ends before the bars, and the page legend below still names the line "Review threshold".
          label: { text: `${compact ? 'Review' : 'Review threshold'} ${money(reviewLine, currency)}/h`, position: 'top-left', color: chartColor.reviewLine, fontSize: 12 },
        }],
      },
    },
    legend: { enabled: !compact, position: 'bottom', item: { label: { fontSize: 12, color: chartColor.ink } } },
    ...(onPick ? { listeners: { seriesNodeClick: ({ datum }) => onPick(datum || null) } } : {}),
  };
}

// ---- Monthly view (owner 2026-11-02: monthly nodes, an average line and the change, like a stock chart) ----------
// Illustrative synthetic history: twelve months derived from the declared baseline rate with a fixed seasonal
// pattern, plus the excess of the observed spike window in the current month. It is context for the seller and is
// never read by the review signal, which compares hourly amounts only.
const SEASONAL = [0.94, 0.97, 1.0, 0.98, 1.03, 1.05, 1.01, 0.99, 1.04, 1.06, 1.02, 1.0];
const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export function buildMonthlyHistory(velocity) {
  const end = toMs(velocity?.window_end);
  const rateCents = toCents(velocity?.baseline_amount_per_hour);
  if (end === null || rateCents === null || rateCents <= 0) return { rows: [], currency: 'USD' };
  const currency = velocity.currency || 'USD';
  const last = new Date(end);
  const totalCents = toCents(velocity.total_amount) ?? 0;
  const hours = Number(velocity.window_hours) > 0 ? Number(velocity.window_hours) : 1;
  const excessCents = Math.max(0, totalCents - rateCents * hours);
  const rows = [];
  for (let back = 11; back >= 0; back -= 1) {
    const year = last.getUTCFullYear();
    const monthIndex = last.getUTCMonth() - back;
    const first = new Date(Date.UTC(year, monthIndex, 1));
    const days = new Date(Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 0)).getUTCDate();
    const cents = Math.round(rateCents * 24 * days * SEASONAL[11 - back]) + (back === 0 ? excessCents : 0);
    rows.push({
      key: `${first.getUTCFullYear()}-${String(first.getUTCMonth() + 1).padStart(2, '0')}`,
      label: `${MONTH_NAMES[first.getUTCMonth()]} ${String(first.getUTCFullYear()).slice(2)}`,
      amount: cents / 100,
      current: back === 0,
    });
  }
  rows.forEach((row, index) => {
    row.ma3 = index >= 2 ? Math.round(((rows[index].amount + rows[index - 1].amount + rows[index - 2].amount) / 3) * 100) / 100 : null;
    row.change = index >= 1 && rows[index - 1].amount > 0 ? Math.round(((row.amount - rows[index - 1].amount) / rows[index - 1].amount) * 1000) / 10 : null;
  });
  return { rows, currency };
}

export function percent(change) {
  return change === null || change === undefined ? '—' : `${change > 0 ? '+' : ''}${change.toFixed(1)}%`;
}

export function monthlyChartOptions({ rows, currency }, container) {
  const tooltip = { renderer: ({ datum }) => ({ heading: datum.current ? 'Current month (includes the spike window)' : 'Month',
    title: datum.label, data: [
      { label: 'Captured amount', value: money(datum.amount, currency) },
      { label: '3-month average', value: datum.ma3 === null ? '—' : money(datum.ma3, currency) },
      { label: 'Change vs previous month', value: percent(datum.change) },
    ] }) };
  return {
    container,
    data: rows,
    title: { text: 'Monthly amount and 3-month average', fontSize: 14, fontWeight: 600, color: chartColor.ink, ...CAPTION_WRAP },
    subtitle: { text: 'Illustrative demo data · not used by the review signal', fontSize: 12, color: chartColor.muted, ...CAPTION_WRAP },
    background: { fill: chartColor.plot },
    padding: { top: 12, right: 44, bottom: 8, left: 20 },
    series: [
      {
        type: 'line', xKey: 'label', yKey: 'amount', yName: 'Month', stroke: MONTH_STROKE, strokeWidth: 2.5,
        marker: { enabled: true, size: 7, fill: MONTH_STROKE, stroke: chartColor.panel, strokeWidth: 1.5 },
        tooltip,
      },
      {
        // Muted dashed, not the review-threshold amber: one colour, one meaning across both charts (review r8).
        type: 'line', xKey: 'label', yKey: 'ma3', yName: '3-mo average', stroke: AVERAGE_STROKE, strokeWidth: 1.5,
        lineDash: [6, 4], marker: { enabled: false }, tooltip,
      },
    ],
    axes: {
      x: { type: 'category', position: 'bottom', label: axisText, gridLine: noGrid },
      y: { type: 'number', position: 'left', min: 0, nice: true, title: { text: `${currency} per month`, ...axisText }, gridLine: valueGrid,
        label: { ...axisText, formatter: ({ value }) => `${Math.round(value / 1000)}k` } },
    },
    // AG Charts 14.2 has no legend.item.paddingX (it logged "Unknown option" on every load); item.padding with left and
    // right gives the same horizontal gap (attack r21).
    legend: { position: 'bottom', spacing: 12, item: { padding: { left: 5, right: 5 }, marker: { size: 10 }, label: { fontSize: 12, color: chartColor.ink } } },
  };
}
