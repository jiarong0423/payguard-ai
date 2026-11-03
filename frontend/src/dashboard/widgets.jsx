// Two custom AG Studio widgets. Both read their rows through widgetApi.getData, so page filters,
// filter widgets and cross-filters from other widgets apply to them automatically. The checklist also
// sets a cross-filter when a case is clicked. Neither writes data or decides anything.
import { useEffect, useMemo, useRef, useState } from 'react';
import { CHECKLIST_WIDGET, DEADLINE_WIDGET, NO_ATTACHMENT } from './layout.js';
import { DUE_SOON_DAYS } from './dashboardData.js';

const fieldName = (field) => String(field?.fieldId || field?.id || '').split('.').pop();

// crossFilter 'filter' returns only the rows other widgets' selections allow; 'highlight' returns every
// row plus that filtered subset, so a widget can keep its own choices visible and dim the rest.
function useWidgetRows(params, mappingKey, crossFilter = 'filter') {
  const fields = params.dataMapping?.[mappingKey] || [];
  const [state, setState] = useState({ rows: [], highlighted: null, selections: [], loaded: false });
  useEffect(() => {
    let live = true;
    if (!fields.length) { setState({ rows: [], highlighted: null, selections: [], loaded: true }); return undefined; }
    const toRows = (result) => (result?.rows || []).map((row) => Object.fromEntries(fields.map((field) => [fieldName(field), row[field.key]])));
    params.widgetApi.setDisplayState('loading', { prominent: false });
    params.widgetApi.getData({ fields }, { crossFilter }).then((response) => {
      if (!live) return;
      const rows = toRows(response?.results);
      const highlighted = response?.crossFilter ? toRows(response.crossFilter) : null;
      setState({ rows, highlighted, selections: params.widgetApi.getCrossFilterSelections() || [], loaded: true });
      params.widgetApi.setDisplayState(rows.length ? 'displayed' : 'noData');
    }).catch(() => { if (live) { setState((previous) => ({ ...previous, loaded: true })); params.widgetApi.setDisplayState('noData'); } });
    return () => { live = false; };
  // Studio hands a new params object whenever the widget's data, filters or format change.
  }, [params]); // eslint-disable-line react-hooks/exhaustive-deps
  return { ...state, fields };
}

function dateText(value) {
  const ms = value instanceof Date ? value.getTime() : typeof value === 'number' ? value : Date.parse(value);
  if (!Number.isFinite(ms)) return '—';
  return `${new Date(ms).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}

const daysLabel = (days) => `${days} ${Number(days) === 1 ? 'day' : 'days'}`;

export function DeadlineTile(params) {
  const { rows, loaded } = useWidgetRows(params, 'fields');
  const sorted = useMemo(() => [...rows].sort((a, b) => Number(a.days_to_due) - Number(b.days_to_due)), [rows]);
  const next = sorted[0];
  // Until the first answer arrives Studio shows its own loading overlay; say "no case" only after data.
  if (!next) return <div className="pg-widget pg-empty" data-testid="widget-deadline">{loaded ? 'No case matches the current filters.' : ''}</div>;
  const soon = Number(next.days_to_due) <= DUE_SOON_DAYS;
  const soonCount = sorted.filter((row) => Number(row.days_to_due) <= DUE_SOON_DAYS).length;
  return (
    <div className="pg-widget pg-deadline" data-testid="widget-deadline">
      <div className={`pg-deadline-hero${soon ? ' is-soon' : ''}`}>
        <span className="pg-deadline-days">{Number(next.days_to_due)}</span>
        <span className="pg-deadline-unit"><strong>{Number(next.days_to_due) === 1 ? 'day' : 'days'} to the next due date</strong>
          <span>{soonCount} of {sorted.length} due within {DUE_SOON_DAYS} days</span></span>
      </div>
      <ul className="pg-deadline-list">
        {sorted.map((row) => (
          <li key={row.case_ref} title={row.readiness || undefined}>
            <strong>{row.case_ref}</strong>
            <span>{dateText(row.due_date).replace(/, .*$/u, '')}<span className="pg-time">{dateText(row.due_date).replace(/^[^,]*/u, '')}</span></span>
            <span className={`pg-chip ${Number(row.days_to_due) <= DUE_SOON_DAYS ? 'pg-chip-watch' : 'pg-chip-info'}`}>{daysLabel(Number(row.days_to_due))}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

const prefersReducedMotion = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

export function EvidenceChecklist(params) {
  const { rows, highlighted, selections, fields, loaded } = useWidgetRows(params, 'fields', 'highlight');
  const caseField = fields.find((field) => fieldName(field) === 'case_ref');
  const trackRef = useRef(null);
  const [index, setIndex] = useState(0);
  // A case is "in" the current cross-filter when it appears in the filtered subset.
  const filtering = selections.length > 0 && Array.isArray(highlighted);
  const inFilter = new Set((highlighted || []).map((row) => row.case_ref));
  // One card per case, cases that need attention (no accepted attachment or a review flag) first.
  const byCase = useMemo(() => {
    const groups = new Map();
    for (const row of rows) {
      if (!groups.has(row.case_ref)) groups.set(row.case_ref, []);
      groups.get(row.case_ref).push(row);
    }
    const needsAttention = ([, items]) => (items[0].delivery_proof === NO_ATTACHMENT ? 0 : 1) + (items[0].review_flag === 'None' ? 1 : 0);
    return [...groups.entries()].sort((a, b) => needsAttention(a) - needsAttention(b) || a[0].localeCompare(b[0]));
  }, [rows]);
  if (!byCase.length) return <div className="pg-widget pg-empty" data-testid="widget-checklist">{loaded ? 'No case matches the current filters.' : ''}</div>;
  const toggle = (caseRef) => {
    if (!caseField) return;
    // group is required in AG Studio 3.0.0 (BaseWidgetCrossFilterParams.group): this widget holds one selection.
    params.widgetApi.toggleCrossFilter({ type: 'value', field: caseField, value: caseRef, group: 0 });
  };
  const go = (step) => {
    const track = trackRef.current;
    if (!track) return;
    const target = Math.max(0, Math.min(byCase.length - 1, index + step));
    track.scrollTo({ left: target * track.clientWidth, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    setIndex(target);
  };
  const onScroll = () => {
    const track = trackRef.current;
    if (track && track.clientWidth) setIndex(Math.round(track.scrollLeft / track.clientWidth));
  };
  return (
    <div className="pg-widget pg-checklist" data-testid="widget-checklist">
      <div className="pg-check-track" ref={trackRef} onScroll={onScroll}>
        {byCase.map(([caseRef, items]) => {
          const first = items[0];
          const attachment = first.delivery_proof !== NO_ATTACHMENT;
          const flagged = first.review_flag !== 'None';
          const selected = filtering && inFilter.has(caseRef);
          return (
            <article key={caseRef} className={`pg-check-card${selected ? ' is-selected' : ''}${filtering && !selected ? ' is-dimmed' : ''}`}>
              <button type="button" className="pg-check-case" aria-pressed={selected} onClick={() => toggle(caseRef)} data-testid={`checklist-case-${caseRef}`}>
                <strong>{caseRef}</strong>
                <span className={`pg-chip ${attachment && !flagged ? 'pg-chip-ok' : 'pg-chip-watch'}`}>{attachment && !flagged ? 'Fields present' : `${(attachment ? 0 : 1) + (flagged ? 1 : 0)} to check`}</span>
                <span className="pg-check-action">{selected ? 'Filtering · clear' : 'Filter page'}</span>
              </button>
              <span className="pg-check-row">
                <i className={`pg-dot ${attachment ? 'pg-dot-ok' : 'pg-dot-gap'}`} aria-hidden="true" />
                <span>{attachment ? 'Accepted delivery attachment on file' : 'No accepted delivery attachment'}</span>
              </span>
              <span className="pg-check-row">
                <i className={`pg-dot ${flagged ? 'pg-dot-flag' : 'pg-dot-ok'}`} aria-hidden="true" />
                <span>{flagged ? `Review flag: ${first.review_flag}` : 'No review flag'}</span>
              </span>
              <details className="pg-check-more">
                <summary>Requested evidence ({items.length})</summary>
                {items.map((item) => (
                  <span className="pg-check-row" key={`${caseRef}-${item.evidence_type}`}>
                    <i className="pg-dot pg-dot-ok" aria-hidden="true" />
                    <span>{item.evidence_type}: {String(item.state).toLowerCase()} · {item.proof_count} proof record{Number(item.proof_count) === 1 ? '' : 's'}</span>
                  </span>
                ))}
              </details>
            </article>
          );
        })}
      </div>
      {byCase.length > 1 && (
        <nav className="pg-pager-nav" aria-label="Evidence checklist cases">
          <button type="button" onClick={() => go(-1)} disabled={index === 0} aria-label="Previous case">‹</button>
          <span aria-live="polite">Case {index + 1} of {byCase.length}</span>
          <span className="pg-pager-dots" aria-hidden="true">{byCase.map(([caseRef], dot) => <i key={caseRef} className={dot === index ? 'is-on' : ''} />)}</span>
          <button type="button" onClick={() => go(1)} disabled={index === byCase.length - 1} aria-label="Next case">›</button>
        </nav>
      )}
    </div>
  );
}

const fieldset = { fields: { type: 'fieldset', supportedRoles: ['category', 'numeric', 'temporal'] } };
const form = (formParams) => formParams.createDefaults({ dataMappingItems: [{ key: 'fields', label: 'Fields' }] });
// The checklist reads with crossFilter 'highlight', so it declares highlight support and shows the highlight option.
const highlightForm = (formParams) => formParams.createDefaults({ dataMappingItems: [{ key: 'fields', label: 'Fields' }], supportsCrossHighlight: true });

export const CUSTOM_WIDGETS = [
  {
    id: DEADLINE_WIDGET, label: 'Deadline tile', comp: DeadlineTile, dataMapping: fieldset, form,
    defaultSize: { width: 8, height: 12 }, minSize: { width: 4, height: 8 },
    ai: { label: 'Deadline tile', description: 'Days to each seller response due date, nearest first.' },
  },
  {
    id: CHECKLIST_WIDGET, label: 'Evidence checklist', comp: EvidenceChecklist, dataMapping: fieldset, form: highlightForm,
    featureConfig: { crossFilter: { supportsHighlight: true } },
    defaultSize: { width: 10, height: 18 }, minSize: { width: 6, height: 10 },
    ai: { label: 'Evidence checklist', description: 'Requested evidence per case with structural state; click a case to cross-filter.' },
  },
];
