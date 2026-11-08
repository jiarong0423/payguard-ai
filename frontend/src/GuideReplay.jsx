import { useCallback, useId, useRef, useState } from 'react';
import { AgGridReact, themeQuartz } from './grid/agGrid.jsx';
import replays from './data/guide_replays_v1.json';
import './GuideReplay.css';

export const gapGridTheme = themeQuartz.withParams({
  accentColor: '#2563eb',
  backgroundColor: '#ffffff',
  borderColor: '#dbe3ec',
  browserColorScheme: 'light',
  foregroundColor: '#1e293b',
  headerBackgroundColor: '#f1f5f9',
  headerTextColor: '#334155',
  oddRowBackgroundColor: '#f8fafc',
  rowHoverColor: '#eff6ff',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  fontSize: 15,
});

const SITUATIONS = [
  ['preflight', 'Policy pre-check'],
  ['velocity', 'Sales spike'],
  ['dispute', 'Dispute evidence'],
];

const STATUS_TEXT = {
  MISSING: ['Not filled in', 'missing'],
  PARTIAL: ['Mentioned, not confirmed', 'partial'],
  UNCLEAR: ['Unclear', 'partial'],
  CONFLICTING: ['Two different answers', 'conflict'],
  STRUCTURALLY_PRESENT: ['Filled in (not checked)', 'present'],
  NOT_APPLICABLE: ['Not applicable', 'muted'],
};

const KIND_TEXT = {
  recorded: ['Recorded model reply', 'recorded'],
  authored: ['Simulated example, not a model run', 'authored'],
};

const statusText = (value) => (STATUS_TEXT[value] || [value])[0];
const sourceText = (data) => (data?.source === 'OFFICIAL' ? 'Official mention' : 'Suggestion');

export function StatusChip({ value }) {
  const [text, tone] = STATUS_TEXT[value] || [value, 'muted'];
  return <span className={`gap-chip gap-chip-${tone}`}>{text}</span>;
}

export function SourceChip({ data }) {
  const official = data.source === 'OFFICIAL';
  return <span className={`gap-chip ${official ? 'gap-chip-official' : 'gap-chip-suggestion'}`}
    title={official ? `Official material mentions this and it may be relevant (${data.chunk}). It is not a PayPal requirement.` : 'TradeGlot organising suggestion, not a PayPal requirement.'}>
    {official ? 'Official mention' : 'Suggestion'}
  </span>;
}

// Gap table shared by the replay and the live guide: AG Grid Community with floating text
// filters, a quick filter, a shown-rows counter and CSV export of every row passed in.
// (r34 #14) Item, Status and Source wrap and grow the row (wrapText + autoHeight) instead of ending in "…" at 1280 px.
const GAP_COLUMNS = [
  { field: 'label', headerName: 'Item', flex: 1.4, minWidth: 180, wrapText: true, autoHeight: true, sortable: true, filter: 'agTextColumnFilter', floatingFilter: true },
  { field: 'status', headerName: 'Status', flex: 1.6, minWidth: 160, wrapText: true, autoHeight: true, cellRenderer: ({ value }) => <StatusChip value={value} />, sortable: true,
    filter: 'agTextColumnFilter', floatingFilter: true, filterValueGetter: ({ data }) => statusText(data.status),
    getQuickFilterText: ({ data }) => statusText(data.status) },
  { field: 'source', headerName: 'Source', flex: 1, minWidth: 120, wrapText: true, autoHeight: true, cellRenderer: ({ data }) => <SourceChip data={data} />, sortable: true,
    filter: 'agTextColumnFilter', floatingFilter: true, filterValueGetter: ({ data }) => sourceText(data),
    getQuickFilterText: ({ data }) => sourceText(data) },
];

export function GapGrid({ items, csvFileName = 'payguard-gap-table.csv', exportLabel = 'Export as CSV', testIdPrefix = 'gap' }) {
  const gridRef = useRef(null);
  const filterId = useId();
  const [quickFilter, setQuickFilter] = useState('');
  const [shownCount, setShownCount] = useState(items.length);

  // CSV export (AG Grid Community CsvExportModule) of every row, with the same plain-English
  // wording the table shows instead of internal status codes.
  const exportCsv = useCallback(() => {
    gridRef.current?.api?.exportDataAsCsv({
      fileName: csvFileName,
      exportedRows: 'all',
      columnKeys: ['label', 'status', 'source'],
      processCellCallback: ({ column, node, value }) => {
        if (column.getColId() === 'status') return statusText(value);
        if (column.getColId() === 'source') return sourceText(node.data);
        return value;
      },
    });
  }, [csvFileName]);

  return <>
    <div className="guide-replay-tools">
      <label htmlFor={filterId}>Filter items</label>
      <input id={filterId} data-testid={`${testIdPrefix}-quick-filter`} type="search" value={quickFilter}
        onChange={(event) => setQuickFilter(event.target.value)} placeholder="Item, status or source" />
      <output data-testid={`${testIdPrefix}-shown-count`} aria-live="polite">{shownCount} of {items.length} items shown</output>
      <button type="button" data-testid={`${testIdPrefix}-export-csv`} onClick={exportCsv}>{exportLabel}</button>
    </div>
    <div className="guide-replay-grid" data-testid={`${testIdPrefix}-grid`}>
      <AgGridReact ref={gridRef} theme={gapGridTheme} rowData={items} columnDefs={GAP_COLUMNS} getRowId={({ data }) => data.id}
        quickFilterText={quickFilter} onModelUpdated={({ api }) => setShownCount(api.getDisplayedRowCount())}
        domLayout="autoHeight" rowHeight={46} headerHeight={46} floatingFiltersHeight={40} suppressCellFocus />
    </div>
  </>;
}

export default function GuideReplay() {
  const [scenarioId, setScenarioId] = useState(replays.scenarios[0].id);
  const [stepIndex, setStepIndex] = useState(0);
  const scenario = replays.scenarios.find((entry) => entry.id === scenarioId);
  const step = scenario.steps[stepIndex];
  const kind = step.model_called ? KIND_TEXT[step.reply_kind] : null;
  const gridRef = useRef(null);
  const [quickFilter, setQuickFilter] = useState('');
  const [shownCount, setShownCount] = useState(step.items.length);

  const choose = (id) => { setScenarioId(id); setStepIndex(0); };

  return <section className="guide-replay" data-testid="guide-replay" aria-label="Guided gap filling replay">
    <p className="guide-replay-label" data-testid="guide-replay-label">{replays.label}</p>
    <div className="guide-replay-layout">
      <nav className="guide-replay-list" aria-label="Replay examples">
        {SITUATIONS.map(([situation, title]) => <div key={situation}>
          <strong>{title}</strong>
          <ul>
            {replays.scenarios.filter((entry) => entry.situation === situation).map((entry) => <li key={entry.id}>
              <button type="button" className={entry.id === scenarioId ? 'is-active' : ''} aria-pressed={entry.id === scenarioId}
                data-testid={`replay-pick-${entry.id}`} onClick={() => choose(entry.id)}>{entry.title}</button>
            </li>)}
          </ul>
        </div>)}
      </nav>
      <div className="guide-replay-main">
        <div className="guide-replay-steps">
          <button type="button" data-testid="replay-prev" disabled={stepIndex === 0} onClick={() => setStepIndex(stepIndex - 1)}>Previous</button>
          <span aria-live="polite">Step {stepIndex + 1} of {scenario.steps.length}</span>
          <button type="button" data-testid="replay-next" disabled={stepIndex === scenario.steps.length - 1} onClick={() => setStepIndex(stepIndex + 1)}>Next</button>
        </div>
        <div className="guide-replay-turn">
          <span className="guide-replay-tag">Seller typed</span>
          <blockquote data-testid="replay-seller">{step.seller_text}</blockquote>
        </div>
        <div className="guide-replay-turn">
          <span className="guide-replay-tag">What the AI returned</span>
          {kind
            ? <span className={`gap-chip gap-chip-${kind[1]}`} data-testid="replay-kind">{kind[0]}</span>
            : <span className="gap-chip gap-chip-muted" data-testid="replay-kind">Model not called. A fixed rule answered before any model.</span>}
          {/* Closed by default and reset on every step, so the raw reply is opt-in. */}
          <details className="guide-replay-details" key={`${scenario.id}-${stepIndex}`} data-testid="replay-reply-details">
            <summary>Show the model's closed reply</summary>
            <div className="guide-replay-details-body">
              {kind
                ? <><small>{step.reply_from.model}, {step.reply_from.date}</small>
                  <pre aria-label="Closed reply from the model" data-testid="replay-reply">{JSON.stringify(step.reply)}</pre>
                  <small>The reply passes the same strict check as a live reply. Its text is never shown to the seller.</small></>
                : <small>No reply for this step: the model was not called.</small>}
              <small data-testid="replay-template">Template: {step.template}</small>
            </div>
          </details>
        </div>
        <div className="guide-replay-turn">
          <span className="guide-replay-tag">TradeGlot says (fixed wording)</span>
          <p className="guide-replay-say" data-testid="replay-say" aria-live="polite">{step.assistant_text}</p>
        </div>
        <GapGrid items={step.items} testIdPrefix="replay" csvFileName={`payguard-replay-${scenario.id}-step-${stepIndex + 1}.csv`}
          exportLabel={`Export step ${stepIndex + 1} as CSV`} />
        <p className="guide-replay-note">The CSV holds every item of this step, whatever the filters show. It is a demo replay, not a PayPal record. Only a form field that passes the rule check can make an item structurally present. A model reply can mark an item at most as mentioned.</p>
      </div>
    </div>
  </section>;
}
