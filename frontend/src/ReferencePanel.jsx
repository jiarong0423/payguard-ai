import { useEffect, useRef, useState } from 'react';
import { apiRequest, REFERENCE_TYPES } from './api.js';

const themeLabels = { source_compliance: 'Official Policy Sources', velocity_guard: 'Legal & Policy Citations', dispute_mediation: 'Legal & Procedural Citations' };
const defaults = { source_compliance: 'acceptable use prior approval', velocity_guard: 'sales volume account limitation', dispute_mediation: 'INR evidence' };
const materialLabels = { official_api_reference: 'Official PayPal API reference', official_policy: 'Official PayPal US policy', public_court_order_copy: 'Official US court procedural record' };
const stageLabels = { any: 'All source stages', procedural_order: 'Procedural order (not final merits)', not_applicable: 'Policy or API document (not a case decision)' };
const outcomeLabels = { SETTLEMENT_APPROVAL_NOT_FINAL_MERITS: 'Settlement approval; not a final merits finding', ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED: 'Arbitration compelled; underlying merits not decided' };
const statusLabels = { DOCUMENT_STATED: 'Document stated', MISSING: 'Date missing', NOT_VERIFIED: 'Not verified', NOT_STATED_IN_REVIEWED_DOCUMENT: 'Not stated in the reviewed document', NOT_APPLICABLE: 'Not applicable' };

function DateField({ label, value, status }) {
  return <div><dt>{label}</dt><dd>{value === null ? '— (missing)' : value}<small>{status === undefined ? 'Raw field; no decision date is inferred' : statusLabels[status] ?? status}</small></dd></div>;
}

export default function ReferencePanel({ theme, session, revision, unavailable, onSessionExpired, open = false, onToggle }) {
  const [query, setQuery] = useState(defaults[theme]);
  const [stage, setStage] = useState('any');
  const [types, setTypes] = useState([...REFERENCE_TYPES]);
  const [knownDate, setKnownDate] = useState(false);
  const [age, setAge] = useState('');
  const [asOf, setAsOf] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const generation = useRef(0);
  const request = useRef(null);
  const current = useRef({ session, revision, unavailable });
  current.current = { session, revision, unavailable };
  const sessionId = session?.session_id;
  const prefix = `reference-${theme}`;

  function invalidate() {
    generation.current += 1;
    request.current?.abort();
    request.current = null;
    setResult(null);
    setError(null);
    setLoading(false);
  }

  useEffect(() => {
    invalidate();
    return () => { generation.current += 1; request.current?.abort(); request.current = null; };
  }, [sessionId, revision, unavailable]);

  function change(setter, value) {
    invalidate();
    setter(value);
  }

  function toggleType(type) {
    invalidate();
    setTypes((previous) => previous.includes(type) ? previous.filter((item) => item !== type) : [...previous, type]);
  }

  async function search(event) {
    event.preventDefault();
    if (unavailable || !session || !query.trim() || !types.length || (age !== '' && !asOf.trim())) return;
    invalidate();
    const token = generation.current;
    const controller = new AbortController();
    request.current = controller;
    const identity = session.session_id;
    const revisionAtStart = revision;
    const body = { query, theme, jurisdiction: 'US', case_stage: stage, material_types: [...types], limit: 3, require_known_source_date: knownDate };
    if (age !== '') body.max_source_age_days = Number(age);
    if (asOf.trim()) body.as_of = asOf.trim();
    const isCurrent = () => generation.current === token && !controller.signal.aborted && current.current.session?.session_id === identity && current.current.revision === revisionAtStart && !current.current.unavailable;
    setLoading(true);
    try {
      const next = await apiRequest('/references/search', { method: 'POST', body, session, signal: controller.signal });
      if (isCurrent()) setResult(next);
    } catch (failure) {
      if (!isCurrent() || failure.code === 'request_cancelled') return;
      setError(failure);
      if (failure.status === 401) onSessionExpired(failure, identity, revisionAtStart);
    } finally {
      if (isCurrent()) { setLoading(false); request.current = null; }
    }
  }

  const disabled = unavailable || !session;
  return <details className="reference-panel" data-testid={`reference-panel-${theme}`} open={open} onToggle={(event) => onToggle?.(event.currentTarget.open)}>
    <summary id={`${prefix}-summary`} aria-controls={`${prefix}-content`}><span>US official sources and procedural records</span><span>{themeLabels[theme] ?? theme}</span></summary>
    <div className="reference-inner" id={`${prefix}-content`} role="region" aria-labelledby={`${prefix}-summary`}>
      <p className="reference-boundary"><strong>US reference profile · not a decision for this case</strong> · Official PayPal sources and US court procedural records support human review only and authorize no payment, refund, or dispute submission.</p>
      <form onSubmit={search} className="reference-form">
        <label className="reference-query" htmlFor={`${prefix}-query`}>Public search query<input id={`${prefix}-query`} data-testid={`reference-query-${theme}`} type="text" value={query} maxLength={512} disabled={disabled} onChange={(event) => change(setQuery, event.target.value)} /></label>
        <div className="reference-fixed-context" data-testid={`reference-jurisdiction-${theme}`}><span>Active jurisdiction</span><strong>United States (US)</strong><small>Foreign jurisdiction input is unsupported and is never substituted.</small></div>
        <label htmlFor={`${prefix}-stage`}>Case stage<select id={`${prefix}-stage`} data-testid={`reference-stage-${theme}`} value={stage} disabled={disabled} onChange={(event) => change(setStage, event.target.value)}>{Object.entries(stageLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
        <fieldset className="reference-type-options" disabled={disabled}><legend>Source types (multiple allowed)</legend>{REFERENCE_TYPES.map((type) => <label key={type}><input type="checkbox" data-testid={`reference-type-${theme}-${type}`} checked={types.includes(type)} onChange={() => toggleType(type)} /><span>{materialLabels[type] ?? type}</span></label>)}</fieldset>
        <div className="reference-date-controls"><label><input type="checkbox" data-testid={`reference-known-date-${theme}`} checked={knownDate} disabled={disabled} onChange={(event) => change(setKnownDate, event.target.checked)} />Require a known document update date</label><label htmlFor={`${prefix}-age`}>Maximum source age from the comparison date (optional)<input id={`${prefix}-age`} type="number" min="0" max="365000" step="1" value={age} disabled={disabled} onChange={(event) => change(setAge, event.target.value)} /></label><label htmlFor={`${prefix}-as-of`}>Timezone-aware comparison point (optional)<input id={`${prefix}-as-of`} type="text" placeholder="YYYY-MM-DDTHH:mm:ss+08:00" maxLength={64} value={asOf} disabled={disabled} onChange={(event) => change(setAsOf, event.target.value)} /></label></div>
        <div className="reference-search-row"><p>The backend evaluates the fixed US reference profile. Jurisdiction-neutral PayPal Developer documentation remains provider guidance, not US law or account eligibility evidence.<small>Only the public query in this field is sent after Search. Product descriptions and buyer data are never inserted automatically.</small></p><button className="button button-secondary" type="submit" data-testid={`reference-search-${theme}`} disabled={disabled || loading || !query.trim() || !types.length || (age !== '' && !asOf.trim())} aria-busy={loading}>{loading ? 'Searching' : 'Search US references'}</button></div>
      </form>
      <div className="reference-status" aria-live="polite" aria-atomic="true">{loading ? 'Validating the local corpus and searching.' : !session ? 'The demo session is unavailable; connect first.' : !result && !error ? 'No search has run.' : result?.status === 'evidence_missing' ? 'No reference matches these filters; no substitute data is used.' : result ? `Found ${result.results.length} public references.` : ''}</div>
      {error && <div className="reference-error" role="alert" data-testid={`reference-error-${theme}`}><strong>{error.status === 401 ? 'Demo session expired' : error.code === 'contract_error' ? 'Reference contract mismatch; display stopped' : 'Reference search incomplete'}</strong><span>{error.message}</span></div>}
      {result && <div data-testid={`reference-results-${theme}`} className="reference-results">
        {result.results.map((row) => <article className="reference-card" key={row.chunk_id} data-testid={`reference-citation-${row.chunk_id}`}>
          <div className="reference-card-header"><strong>{row.title}</strong><span>{row.jurisdiction} · {materialLabels[row.material_type] ?? row.material_type}</span></div>
          <p className="reference-stage">{stageLabels[row.case_stage] ?? row.case_stage} · {row.case_outcome === null ? 'Not a case decision' : outcomeLabels[row.case_outcome] ?? row.case_outcome}</p>
          <p className="reference-summary">{row.text}</p>
          <a className="reference-source-link" href={row.url} target="_blank" rel="noopener noreferrer">Original source: {row.source_title}</a><p className="reference-locator">Source locator: {row.locator}</p>
          <dl className="reference-dates"><DateField label="Document update date" value={row.source_updated_date} status={row.source_updated_date_status} /><DateField label="Policy effective date" value={row.effective_date} status={row.effective_date_status} /><DateField label="Decision date" value={row.decision_date} status={row.decision_date_status} /><DateField label="Decision acceptance deadline" value={row.decision_acceptance_deadline} /></dl>
          <p className="reference-retrieved">Material retrieved at: {row.retrieved_at} · lexical match score: {row.relevance_score} (not a confidence score)</p>
          <details className="reference-provenance"><summary>Source identity and validation</summary><dl><dt>Original source-region label</dt><dd>{row.jurisdiction_label}</dd><dt>Source ID</dt><dd>{row.source_id}</dd><dt>Chunk ID</dt><dd>{row.chunk_id}</dd><dt>Text SHA-256</dt><dd>{row.text_sha256}</dd><dt>Source URL</dt><dd>{row.url}</dd></dl></details>
        </article>)}
        <details className="reference-limitations"><summary>Backend reference limitations</summary><ul>{result.limitations.map((item) => <li key={item}>{item}</li>)}</ul><p>Source: {result.source} · corpus version: {result.corpus_id}</p><details><summary>Corpus version validation</summary><p>{result.corpus_digest}</p><p>Sources: {result.corpus_digests.sources_sha256}</p><p>Chunks: {result.corpus_digests.chunks_sha256}</p></details></details>
      </div>}
    </div>
  </details>;
}
