// Pure helpers for the stage 02 hourly chart. No network, no clock: everything is
// derived from the backend `velocity` block and the synthetic `transactions` list.

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

export function hourLabel(ms) {
  const date = new Date(ms);
  return `${String(date.getUTCHours()).padStart(2, '0')}:${String(date.getUTCMinutes()).padStart(2, '0')}`;
}

/**
 * Build one row per hour: the baseline window first, then the spike (observation) window.
 * Baseline rows carry the synthetic baseline rate the velocity signal compares against;
 * spike rows carry the captured amount summed from synthetic transactions in that hour.
 * The spike window is left-open, right-closed, the same boundary the backend uses.
 */
export function buildVelocityHourlyRows(velocity, transactions) {
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
        label: hourLabel(start),
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
        label: `${hourLabel(start)} ▲`,
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
  return { rows, reviewLine, currency };
}

const BASELINE_FILL = '#94a3b8';
const SPIKE_FILL = '#0f766e';
const REVIEW_STROKE = '#875f30';
// A bar above the review line is drawn in amber so the hour to look at stands out; the rest stay teal.
const FLAG_FILL = '#b45309';
const AVERAGE_STROKE = '#6366f1';

// (r32 J5 P3-3) Chart titles and subtitles wrap onto up to three lines instead of being cut with an ellipsis at
// phone width.
const CAPTION_WRAP = Object.freeze({ wrapping: 'on-space', maxHeight: 60 });

export function money(value) {
  return Number(value).toFixed(2);
}

function rangeLabel(datum) {
  const fmt = (iso) => new Date(iso).toISOString().slice(11, 16);
  return `${fmt(datum.start)}–${fmt(datum.end)} UTC`;
}

// compact: phones, where the page shows its own unpaginated legend (App.jsx PhoneChartLegend) because this one pages.
export function velocityChartOptions({ rows, reviewLine, currency }, container, { compact = false } = {}) {
  const baselineRate = rows.find((row) => row.window === 'baseline')?.baseline || null;
  return {
    container,
    data: rows,
    title: { text: 'Hourly amount: baseline vs spike', fontSize: 14, fontWeight: 600, color: '#0f172a', ...CAPTION_WRAP },
    subtitle: { text: 'Sample data · times in UTC · amber = above the review line', fontSize: 13, color: '#64748b', ...CAPTION_WRAP },
    background: { fill: '#ffffff' },
    padding: { top: 12, right: 16, bottom: 8, left: 8 },
    series: [
      {
        // The baseline is one declared synthetic rate, so it is drawn as a flat dashed line (like a stock chart's
        // average line) instead of 24 identical bars.
        type: 'line', xKey: 'label', yKey: 'baseline', yName: 'Usual rate', stroke: BASELINE_FILL,
        strokeWidth: 2, lineDash: [5, 4], marker: { enabled: false },
        tooltip: { renderer: ({ datum }) => ({ heading: 'Baseline window', title: rangeLabel(datum),
          data: [{ label: 'Synthetic baseline rate', value: `${money(datum.baseline)} ${currency}/h` }] }) },
      },
      {
        type: 'bar', xKey: 'label', yKey: 'spike', yName: 'Spike window (amber = above the line)', fill: SPIKE_FILL,
        cornerRadius: 3,
        itemStyler: ({ datum }) => (reviewLine !== null && datum && datum.spike > reviewLine ? { fill: FLAG_FILL } : {}),
        label: { enabled: true, placement: 'outside-end', fontSize: 16, fontWeight: 700, color: SPIKE_FILL,
          formatter: ({ value }) => (value && baselineRate > 0 ? `×${(value / baselineRate).toFixed(1)}` : '') },
        tooltip: { renderer: ({ datum }) => ({ heading: 'Spike window', title: rangeLabel(datum),
          data: [{ label: 'Captured amount', value: `${money(datum.spike)} ${currency}` }, { label: 'Orders', value: String(datum.captures ?? 0) }] }) },
      },
    ],
    axes: {
      x: { type: 'category', position: 'bottom', label: { fontSize: 13, color: '#475569' } },
      y: {
        type: 'number', position: 'left', min: 0, nice: true,
        title: { text: `${currency} per hour`, fontSize: 13, color: '#475569' },
        label: { fontSize: 13, color: '#475569' },
        crossLines: reviewLine === null ? [] : [{
          type: 'line', value: reviewLine, stroke: REVIEW_STROKE, strokeWidth: 1.5, lineDash: [6, 4],
          // (r32 J1 J4) On a phone the long label ran under the spike bar and its "USD/h" was hidden; the short one
          // ends before the bars, and the page legend below still names the line "Review threshold".
          label: { text: `${compact ? 'Review' : 'Review threshold'} ${money(reviewLine)} ${currency}/h`, position: 'top-left', color: '#92400e', fontSize: 13 },
        }],
      },
    },
    legend: { enabled: !compact, position: 'bottom', item: { label: { fontSize: 13, color: '#334155' } } },
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
      { label: 'Captured amount', value: `${money(datum.amount)} ${currency}` },
      { label: '3-month average', value: datum.ma3 === null ? '—' : `${money(datum.ma3)} ${currency}` },
      { label: 'Change vs previous month', value: percent(datum.change) },
    ] }) };
  return {
    container,
    data: rows,
    title: { text: 'Monthly amount and 3-month average', fontSize: 14, fontWeight: 600, color: '#1e293b', ...CAPTION_WRAP },
    subtitle: { text: 'Illustrative demo data · not used by the review signal', fontSize: 12, color: '#64748b', ...CAPTION_WRAP },
    background: { fill: '#ffffff' },
    padding: { top: 12, right: 44, bottom: 8, left: 8 },
    series: [
      {
        type: 'line', xKey: 'label', yKey: 'amount', yName: 'Month', stroke: SPIKE_FILL, strokeWidth: 2.5,
        marker: { enabled: true, size: 7, fill: SPIKE_FILL, stroke: '#ffffff', strokeWidth: 1.5 },
        tooltip,
      },
      {
        // Indigo, not the review-threshold orange: one colour, one meaning across both charts (review r8).
        type: 'line', xKey: 'label', yKey: 'ma3', yName: '3-mo average', stroke: AVERAGE_STROKE, strokeWidth: 1.5,
        lineDash: [6, 4], marker: { enabled: false }, tooltip,
      },
    ],
    axes: {
      x: { type: 'category', position: 'bottom', label: { fontSize: 12, color: '#475569' } },
      y: { type: 'number', position: 'left', min: 0, nice: true, title: { text: `${currency} per month`, fontSize: 13, color: '#475569' },
        label: { fontSize: 12, color: '#475569', formatter: ({ value }) => `${Math.round(value / 1000)}k` } },
    },
    // AG Charts 14.2 has no legend.item.paddingX (it logged "Unknown option" on every load); item.padding with left and
    // right gives the same horizontal gap (attack r21).
    legend: { position: 'bottom', spacing: 12, item: { padding: { left: 5, right: 5 }, marker: { size: 10 }, label: { fontSize: 12, color: '#334155' } } },
  };
}
