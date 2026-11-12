import { useCallback, useEffect, useId, useMemo, useRef, useState } from 'react';
import { AgGridReact, GRID_FLOATING_FILTERS_HEIGHT } from './grid/agGrid.jsx';
import replays from './data/guide_replays_v1.json';
import './GuideReplay.css';

// (F2 2026-11-12, OFFICIAL_FIX_GUIDE s1) No separate slate theme any more: null means "the console grid theme"
// (grid/agGrid.jsx picks the desktop or phone instance of theme/chartTheme.js gridParams()). GuideLive reads this export.
export const gapGridTheme = null;
// Below this width the Source column is hidden (AG Grid grid-size: hide the column that does not fit), so Item
// and the whole status label still fit; the CSV export names its columns and still carries Source.
export const GAP_NARROW_WIDTH = 560;
// Below this width even Item (min 120) + the whole Status label (224) do not fit, e.g. the 285px phone column: the rows
// the grid shows (after its filters) are listed as cards, like the live guide's phone list; the grid stays mounted for
// the shown-row count and the CSV export.
export const GAP_CARDS_WIDTH = 346;

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
// (r34 #14) Item wraps and grows the row (wrapText + autoHeight) instead of ending in "…" at 1280 px.
// (F2 2026-11-12, D-P3) Status and Source are custom chip renderers: wrapText does not apply to them (AG Grid row-height),
// so the chips never wrap and the column is at least as wide as the longest label ("Mentioned, not confirmed").
const GAP_COLUMNS = [
  { field: 'label', headerName: 'Item', flex: 1.4, minWidth: 120, wrapText: true, autoHeight: true, sortable: true, filter: 'agTextColumnFilter', floatingFilter: true },
  { field: 'status', headerName: 'Status', flex: 1.6, minWidth: 224, suppressSizeToFit: true, cellRenderer: ({ value }) => <StatusChip value={value} />, sortable: true,
    filter: 'agTextColumnFilter', floatingFilter: true, filterValueGetter: ({ data }) => statusText(data.status),
    getQuickFilterText: ({ data }) => statusText(data.status) },
  { field: 'source', headerName: 'Source', flex: 1, minWidth: 160, cellRenderer: ({ data }) => <SourceChip data={data} />, sortable: true,
    filter: 'agTextColumnFilter', floatingFilter: true, filterValueGetter: ({ data }) => sourceText(data),
    getQuickFilterText: ({ data }) => sourceText(data) },
];

export function GapGrid({ items, csvFileName = 'tradeglot-gap-table.csv', exportLabel = 'Export as CSV', testIdPrefix = 'gap' }) {
  const gridRef = useRef(null);
  const filterId = useId();
  const [quickFilter, setQuickFilter] = useState('');
  const [shownCount, setShownCount] = useState(items.length);
  const [cards, setCards] = useState(null);

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

  // Card mode follows the width of the replay column (ResizeObserver on the tools row, which is never hidden).
  const toolsRef = useRef(null);
  const [carded, setCarded] = useState(false);
  const [narrow, setNarrow] = useState(false);
  useEffect(() => {
    const box = toolsRef.current;
    if (!box || typeof ResizeObserver === 'undefined') return undefined;
    const update = () => { const width = box.clientWidth; if (width > 0) { setCarded(width < GAP_CARDS_WIDTH); setNarrow(width < GAP_NARROW_WIDTH); } };
    update();
    const observer = new ResizeObserver(update);
    observer.observe(box);
    return () => observer.disconnect();
  }, []);
  const syncCards = useCallback((api) => {
    if (!carded) { setCards(null); return; }
    const shown = [];
    api.forEachNodeAfterFilterAndSort((node) => { if (node.data) shown.push(node.data); });
    setCards(shown);
  }, [carded]);
  useEffect(() => { const api = gridRef.current?.api; if (api) syncCards(api); else if (!carded) setCards(null); }, [syncCards, carded, items]);

  // Narrow column: Source hidden (AG Grid grid-size, column `hide`); measured on the tools row because an autoHeight
  // grid does not report onGridSizeChanged on its first layout.
  const columns = useMemo(() => GAP_COLUMNS.map((column) => (column.field === 'source' ? { ...column, hide: narrow } : column)), [narrow]);

  return <>
    <div className="guide-replay-tools" ref={toolsRef}>
      <label htmlFor={filterId}>Filter items</label>
      <input id={filterId} data-testid={`${testIdPrefix}-quick-filter`} type="search" value={quickFilter}
        onChange={(event) => setQuickFilter(event.target.value)} placeholder="Item, status or source" />
      <output data-testid={`${testIdPrefix}-shown-count`} aria-live="polite">{shownCount} of {items.length} items shown</output>
      <button type="button" data-testid={`${testIdPrefix}-export-csv`} onClick={exportCsv}>{exportLabel}</button>
    </div>
    {cards && <ul className="guide-live-cards" data-testid={`${testIdPrefix}-cards`}>
      {cards.map((item) => <li key={item.id} className="guide-live-card"><strong>{item.label}</strong><span><StatusChip value={item.status} /><SourceChip data={item} /></span></li>)}
    </ul>}
    <div className={`guide-replay-grid${cards ? ' is-carded' : ''}`} data-testid={`${testIdPrefix}-grid`}>
      <AgGridReact ref={gridRef} theme={gapGridTheme} rowData={items} columnDefs={columns} getRowId={({ data }) => data.id}
        quickFilterText={quickFilter} onModelUpdated={({ api }) => { setShownCount(api.getDisplayedRowCount()); syncCards(api); }}
        domLayout="autoHeight" floatingFiltersHeight={GRID_FLOATING_FILTERS_HEIGHT} suppressCellFocus />
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
        <GapGrid items={step.items} testIdPrefix="replay" csvFileName={`tradeglot-replay-${scenario.id}-step-${stepIndex + 1}.csv`}
          exportLabel={`Export step ${stepIndex + 1} as CSV`} />
        <p className="guide-replay-note">The CSV holds every item of this step, whatever the filters show. It is a demo replay, not a PayPal record. Only a form field that passes the rule check can make an item structurally present. A model reply can mark an item at most as mentioned.</p>
      </div>
    </div>
  </section>;
}
