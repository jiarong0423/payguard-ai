import { useMemo, useState } from 'react';
import { AgGridReact, themeQuartz } from './grid/agGrid.jsx';
import { operatorLabel } from './operatorLabels.js';
import './charts/charts.css';

// Registered here too, not only in App.jsx: the view is also mounted on its own (the optional timeline wrapper and
// its render check), and AG Grid needs the filter, quick-filter and tooltip modules wherever the grid appears.
// Registering the same Community modules twice is a no-op.

const timeGridTheme = themeQuartz.withParams({
  accentColor: '#74b5ff',
  backgroundColor: '#0f1b2b',
  borderColor: '#2a3b55',
  browserColorScheme: 'dark',
  foregroundColor: '#dbe7f6',
  headerBackgroundColor: '#14243a',
  headerTextColor: '#9fb6d3',
  oddRowBackgroundColor: '#122135',
  rowHoverColor: '#1a2d47',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  fontSize: 14,
  wrapperBorderRadius: 8,
});

const GAP_NAMES = [
  ['payment_to_order_record', 'Payment to order record'],
  ['payment_to_delivery', 'Payment to delivery'],
  ['delivery_to_claim', 'Delivery to claim'],
  ['payment_to_claim', 'Payment to claim'],
];

function whenLabel(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return `${date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}

function gapLabel(seconds) {
  if (seconds === null || seconds === undefined) return 'Not recorded';
  const sign = seconds < 0 ? '−' : '';
  const total = Math.abs(seconds);
  const days = Math.floor(total / 86400);
  const hours = Math.floor((total % 86400) / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  if (days > 0) return `${sign}${days} d ${hours} h`;
  if (hours > 0) return `${sign}${hours} h ${minutes} min`;
  return `${sign}${minutes} min`;
}

function eventDetail(event) {
  return event.kind === 'MESSAGE' ? `${operatorLabel(event.channel)} · ${operatorLabel(event.direction)} · ${operatorLabel(event.topic)}` : '';
}

// Rows for the AG Grid view. The backend already orders the events; the gap is measured
// from the event directly above in that order, so the first row has no gap.
export function timeEventRows(events) {
  return (Array.isArray(events) ? events : []).map((event, index, list) => {
    const at = Date.parse(event.at);
    const previous = index > 0 ? Date.parse(list[index - 1].at) : NaN;
    const gap = index > 0 && Number.isFinite(at) && Number.isFinite(previous) ? Math.round((at - previous) / 1000) : null;
    return {
      id: `${index}-${event.kind}-${event.at}`,
      order: index + 1,
      kind: event.kind,
      event: operatorLabel(event.kind),
      detail: eventDetail(event),
      at: event.at,
      source: operatorLabel(event.source),
      gapSeconds: gap,
    };
  });
}

function EventCell({ data }) {
  return <span className={`te-kind te-kind-${String(data.kind).toLowerCase()}`}>
    <i className="te-kind-dot" aria-hidden="true" />
    <span>{data.event}{data.detail && <small> · {data.detail}</small>}</span>
  </span>;
}

function TimeCell({ value }) {
  return <time className="te-time" dateTime={value}>{whenLabel(value)}</time>;
}

function SourceCell({ value }) {
  return <span className="te-source">{value}</span>;
}

function GapCell({ value }) {
  if (value === null || value === undefined) return <span className="te-gap te-gap-first">First event</span>;
  return <span className={`te-gap${value < 0 ? ' te-gap-negative' : ''}`}>{value === 0 ? 'Same time' : value < 0 ? gapLabel(value) : `+${gapLabel(value)}`}</span>;
}

export default function TimeEvidenceView({ evidence }) {
  const [view, setView] = useState('table');
  const rows = useMemo(() => timeEventRows(evidence?.events), [evidence]);
  const columns = useMemo(() => [
    { field: 'order', headerName: '#', width: 64, minWidth: 64, sort: 'asc', filter: 'agNumberColumnFilter' },
    { field: 'event', headerName: 'Event', flex: 1.6, minWidth: 220, cellRenderer: EventCell, filter: 'agTextColumnFilter',
      getQuickFilterText: ({ data }) => `${data.event} ${data.detail}`,
      tooltipValueGetter: ({ data }) => (data.detail ? `${data.event} · ${data.detail}` : data.event) },
    { field: 'at', headerName: 'Timestamp', flex: 1, minWidth: 170, cellRenderer: TimeCell, filter: 'agTextColumnFilter',
      filterValueGetter: ({ data }) => whenLabel(data.at), getQuickFilterText: ({ data }) => whenLabel(data.at) },
    { field: 'source', headerName: 'Source', flex: 1.2, minWidth: 220, cellRenderer: SourceCell, filter: 'agTextColumnFilter' },
    { field: 'gapSeconds', headerName: 'Gap to previous', flex: 0.9, minWidth: 150, cellRenderer: GapCell, filter: 'agNumberColumnFilter',
      headerTooltip: 'Time since the event in the row above, in the backend order. Filter values are seconds.' },
  ], []);
  if (!evidence || !Array.isArray(evidence.events)) return null;
  return (
    <section className="time-evidence" data-testid="time-evidence" aria-label="Time evidence">
      <div className="mini-heading"><span>Time evidence · ordered, not judged</span><span className="badge badge-amber">SYNTHETIC</span></div>
      <div className="time-evidence-views" role="group" aria-label="Time evidence view">
        <button type="button" aria-pressed={view === 'table'} className={view === 'table' ? 'is-active' : ''} data-testid="time-evidence-view-table" onClick={() => setView('table')}>Table</button>
        <button type="button" aria-pressed={view === 'timeline'} className={view === 'timeline' ? 'is-active' : ''} data-testid="time-evidence-view-timeline" onClick={() => setView('timeline')}>Timeline</button>
      </div>
      {view === 'table' ? <div className="time-evidence-grid" data-testid="time-evidence-grid">
        <div className="time-evidence-grid-caption"><span>{rows.length} events · sort or filter any column</span><span>AG Grid Community</span></div>
        <AgGridReact theme={timeGridTheme} rowData={rows} columnDefs={columns} getRowId={({ data }) => data.id}
          defaultColDef={{ sortable: true, resizable: true, floatingFilter: false }} domLayout="autoHeight"
          rowHeight={42} headerHeight={42} suppressCellFocus tooltipShowDelay={300} />
      </div> : <ol className="time-events">
        {evidence.events.map((event, index) => (
          <li key={`${event.kind}-${event.at}-${index}`} className={`time-event time-event-${event.kind.toLowerCase()}`}>
            <time dateTime={event.at}>{whenLabel(event.at)}</time>
            <strong>{operatorLabel(event.kind)}</strong>
            {event.kind === 'MESSAGE' && <span>{operatorLabel(event.channel)} · {operatorLabel(event.direction)} · {operatorLabel(event.topic)}</span>}
            <em>{operatorLabel(event.source)}</em>
          </li>
        ))}
      </ol>}
      <div className="time-gaps">
        {GAP_NAMES.map(([key, label]) => (
          <div key={key}><span>{label}</span><strong>{gapLabel(evidence.gaps_seconds?.[key])}</strong></div>
        ))}
      </div>
      {evidence.flags?.length > 0 && (
        <p className="time-flags">{evidence.flags.map((flag) => <span key={flag} className="badge badge-muted">{operatorLabel(flag)}</span>)}</p>
      )}
      <p className="time-note">TradeGlot orders and preserves times. It states no intent, predicts no outcome and gives no legal advice. Messages are kept as a topic and a keyed digest, never as text. A negative gap means the second event is earlier than the first.</p>
    </section>
  );
}
