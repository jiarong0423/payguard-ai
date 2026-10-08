import { useEffect, useRef, useState } from 'react';
import { apiRequest, POLICY_CLAIM_TYPES, policyInstant } from './api.js';
import { operatorLabel, operatorLabels } from './operatorLabels.js';

const labels = { source_compliance: 'AUP preflight screen', velocity_guard: 'Velocity and account-risk signals', dispute_mediation: 'Dispute mediation' };
const panelLabels = { source_compliance: 'Deterministic Screening', velocity_guard: 'Deterministic Rule Engine', dispute_mediation: 'Policy Assertion Engine' };
const syntheticText = 'Authored synthetic reference statement requiring human review.';
const authority = 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION';
function SourceDate({ label, value, status }) {
  return <div><dt>{label}</dt><dd>{value ?? '— (unknown)'}<small>{status === undefined ? 'No status supplied; human review required' : operatorLabel(status)}</small></dd></div>;
}

export default function PolicyPanel({ theme, session, revision, unavailable, onSessionExpired, open = false, onToggle }) {
  const [asOf, setAsOf] = useState(() => new Date().toISOString());
  const [budget, setBudget] = useState('30');
  const [claimType, setClaimType] = useState('policy_reference');
  const [citation, setCitation] = useState('');
  const [assessment, setAssessment] = useState(null);
  const [gate, setGate] = useState(null);
  const [assessmentError, setAssessmentError] = useState(null);
  const [gateError, setGateError] = useState(null);
  const [assessing, setAssessing] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const assessGeneration = useRef(0);
  const gateGeneration = useRef(0);
  const assessController = useRef(null);
  const gateController = useRef(null);
  const current = useRef(null);
  current.current = { session, revision, unavailable };
  const prefix = `policy-${theme}`;
  const disabled = unavailable || !session;
  const contextValid = policyInstant(asOf.trim()) !== null && /^\d+$/.test(budget) && Number.isInteger(Number(budget)) && Number(budget) <= 365000;

  function clearGate() {
    gateGeneration.current += 1;
    gateController.current?.abort();
    gateController.current = null;
    setGate(null); setGateError(null); setEvaluating(false);
  }
  function clearBoth() {
    assessGeneration.current += 1;
    assessController.current?.abort();
    assessController.current = null;
    clearGate();
    setAssessment(null); setAssessmentError(null); setAssessing(false); setCitation('');
  }
  useEffect(() => {
    clearBoth();
    return () => {
      assessGeneration.current += 1; gateGeneration.current += 1;
      assessController.current?.abort(); gateController.current?.abort();
      assessController.current = null; gateController.current = null;
    };
  }, [session?.session_id, revision, unavailable, theme]);
  function changeContext(setter, value) { clearBoth(); setter(value); }
  function changeGate(setter, value) { clearGate(); setter(value); }
  function context() { return { jurisdiction: 'US', theme, as_of: asOf.trim(), observation_max_age_days: Number(budget) }; }
  function alive(controller, identity, revisionAtStart) {
    return !controller.signal.aborted && current.current.session?.session_id === identity && current.current.revision === revisionAtStart && !current.current.unavailable;
  }
  async function assess(event) {
    event.preventDefault();
    if (disabled || !contextValid) return;
    clearBoth();
    const token = assessGeneration.current;
    const controller = new AbortController(); assessController.current = controller;
    const identity = session.session_id; const revisionAtStart = revision;
    const isCurrent = () => assessGeneration.current === token && alive(controller, identity, revisionAtStart);
    setAssessing(true);
    try {
      const next = await apiRequest('/policy/assess', { method: 'POST', body: context(), session, signal: controller.signal });
      if (isCurrent()) { setAssessment(next); setCitation(next.chunks[0]?.chunk_id ?? ''); }
    } catch (failure) {
      if (!isCurrent() || failure.code === 'request_cancelled') return;
      setAssessmentError(failure);
      if (failure.status === 401) onSessionExpired(failure, identity, revisionAtStart);
    } finally { if (isCurrent()) { setAssessing(false); assessController.current = null; } }
  }
  async function evaluate() {
    if (disabled || !assessment || !citation || assessing || !contextValid || !assessment.chunks.some(c => c.chunk_id === citation)) return;
    clearGate();
    const token = gateGeneration.current; const assessmentToken = assessGeneration.current;
    const controller = new AbortController(); gateController.current = controller;
    const identity = session.session_id; const revisionAtStart = revision;
    const isCurrent = () => gateGeneration.current === token && assessGeneration.current === assessmentToken && alive(controller, identity, revisionAtStart);
    const ctx = context();
    const candidate = { schema_version: 1, jurisdiction: ctx.jurisdiction, theme, as_of: ctx.as_of, status: 'manual_review', advisory_only: true, operational_authority: authority, claims: [{ claim_id: 'SYNTHETIC_CLAIM', claim_type: claimType, text: syntheticText, citation_chunk_ids: [citation] }] };
    setEvaluating(true);
    try {
      const next = await apiRequest('/advisory/evaluate', { method: 'POST', body: { ...ctx, candidate_json: JSON.stringify(candidate) }, session, signal: controller.signal });
      if (isCurrent()) setGate(next);
    } catch (failure) {
      if (!isCurrent() || failure.code === 'request_cancelled') return;
      setGateError(failure);
      if (failure.status === 401) onSessionExpired(failure, identity, revisionAtStart);
    } finally { if (isCurrent()) { setEvaluating(false); gateController.current = null; } }
  }
  return <details open={open} onToggle={(event) => onToggle?.(event.currentTarget.open)} className="reference-panel policy-panel" data-testid={`policy-panel-${theme}`}>
    <summary id={`${prefix}-summary`} aria-controls={`${prefix}-content`}><span>Policy evidence and synthetic-claim check</span><span>{panelLabels[theme] ?? theme}</span></summary>
    <div className="reference-inner" id={`${prefix}-content`} role="region" aria-labelledby={`${prefix}-summary`}>
      <p className="reference-boundary"><strong>Human reference · not current-policy applicability certification</strong> · No payment, refund, assurance, or submission authority. This panel uses fixed public summaries and runs no AI model.</p>
      <form className="reference-form" onSubmit={assess}>
        <div className="reference-fixed-context" data-testid={`policy-jurisdiction-${theme}`}><span>Active policy context</span><strong>United States (US)</strong><small>The browser cannot select or substitute another jurisdiction.</small></div>
        <label htmlFor={`${prefix}-budget`}>Maximum observation age (days)<input id={`${prefix}-budget`} data-testid={`policy-budget-${theme}`} type="number" min="0" max="365000" step="1" value={budget} disabled={disabled} onChange={e => changeContext(setBudget,e.target.value)} /></label>
        <label className="reference-query" htmlFor={`${prefix}-as-of`}>Evaluation time (UTC ISO)<input id={`${prefix}-as-of`} data-testid={`policy-as-of-${theme}`} type="text" maxLength={64} value={asOf} disabled={disabled} onChange={e => changeContext(setAsOf,e.target.value)} /></label>
        <button data-testid={`policy-assess-${theme}`} type="submit" disabled={disabled || !contextValid || assessing}>{assessing ? 'Assessing evidence' : 'Assess policy evidence'}</button>
      </form>
      {!contextValid && <p className="reference-error" role="status">Enter a valid UTC ISO timestamp and an integer from 0 to 365000 days.</p>}
      {assessmentError && <p className="reference-error" role="alert" data-testid={`policy-assess-error-${theme}`}>{assessmentError.message}</p>}
      <section aria-label={`${labels[theme]} policy evidence result`} aria-live="polite" aria-busy={assessing} data-testid={`policy-assessment-${theme}`}>
        {!assessment && !assessing && <p>Not assessed. Retrieve the fixed public evidence manually.</p>}
        {assessment && <>
          <p><strong>{operatorLabel(assessment.status)}</strong> · current-policy applicability: {operatorLabel(assessment.current_policy_applicability)}; human review is required.</p>
          <p>US-profile sources: {assessment.coverage.regional_source_count}; sources for this theme: {assessment.coverage.selected_source_count}; citations: {assessment.coverage.selected_chunk_count}. Coverage complete: {String(assessment.coverage.complete)}.</p>
          <p>Official-policy citations by theme: {Object.entries(assessment.coverage.official_policy_chunk_count_by_theme).map(([t,n]) => `${labels[t]} ${n}`).join('; ')}. Themes without official-policy coverage: {assessment.coverage.missing_official_policy_themes.map(t=>labels[t]).join(', ') || 'none; summaries still do not equal complete policy'}</p>
          {assessment.chunks.length === 0 && <p>No reference coverage exists for this region and theme; synthetic-claim checking is disabled.</p>}
          <p className="policy-code">{operatorLabels(assessment.reason_codes).join(' · ')}</p>
          {assessment.sources.map(source => <details key={source.source_id} className="policy-source">
            <summary>{source.title} · {operatorLabel(source.observation_status)}</summary>
            <p>{operatorLabel(source.material_type)} · {source.jurisdiction} · United States profile</p>
            <dl className="reference-dates"><SourceDate label="Document update date" value={source.source_updated_date} status={source.source_updated_date_status} /><SourceDate label="Effective date" value={source.effective_date} status={source.effective_date_status} /><SourceDate label="Case decision date" value={source.decision_date} status={source.decision_date_status} /><SourceDate label="Decision acceptance deadline" value={source.decision_acceptance_deadline} /><SourceDate label="Saved retrieval time" value={source.retrieved_at} /><SourceDate label="Evaluation time" value={assessment.filters_applied.as_of} /></dl>
            <p>Source-age basis: {operatorLabel(source.observation_age_basis)}. An unknown effective date does not establish applicability.</p>
            <p className="policy-code">Source ID: {source.source_id}<br />{operatorLabels(source.reason_codes).join(' · ')}</p>
            <a href={source.url} target="_blank" rel="noopener noreferrer">Open public source for human review</a>
            {assessment.chunks.filter(c=>c.source_id===source.source_id).map(c=><p className="policy-code" key={c.chunk_id}>Citation {c.chunk_id} · {operatorLabel(c.case_stage)} · {operatorLabel(c.case_outcome, 'No case outcome stated')}<br />Text SHA-256: {c.text_sha256}</p>)}
          </details>)}
          <details className="policy-source"><summary>Corpus identity and limitations</summary><p className="policy-code">{assessment.corpus_id}<br />{assessment.corpus_digest}<br />Sources: {assessment.corpus_digests.sources_sha256}<br />Chunks: {assessment.corpus_digests.chunks_sha256}</p>{assessment.limitations.map((s,i)=><p key={i}>{s}</p>)}</details>
        </>}
      </section>
      <div className="policy-gate-form reference-form">
        <label htmlFor={`${prefix}-citation`}>Fixed evidence citation<select id={`${prefix}-citation`} data-testid={`policy-citation-${theme}`} disabled={disabled || !assessment || assessing || !assessment.chunks.length} value={citation} onChange={e=>changeGate(setCitation,e.target.value)}><option value="">Assess first, then select a citation</option>{assessment?.chunks.map(c=><option key={c.chunk_id} value={c.chunk_id}>{c.chunk_id} · {operatorLabel(c.material_type)} · {operatorLabel(c.case_stage)}</option>)}</select></label>
        <label htmlFor={`${prefix}-claim-type`}>Synthetic claim type<select id={`${prefix}-claim-type`} data-testid={`policy-claim-type-${theme}`} disabled={disabled} value={claimType} onChange={e=>changeGate(setClaimType,e.target.value)}>{POLICY_CLAIM_TYPES.map(t=><option key={t} value={t}>{operatorLabel(t)}</option>)}</select></label>
        <p className="reference-query">Fixed synthetic sentence: {syntheticText} (synthetic test only). This sentence tests structure only and reads no product description, customer data, or other query.</p>
        <button type="button" data-testid={`policy-evaluate-${theme}`} disabled={disabled || !assessment || !citation || assessing || evaluating || !contextValid} onClick={evaluate}>{evaluating ? 'Checking structure' : 'Check synthetic claim'}</button>
      </div>
      {gateError && <p className="reference-error" role="alert" data-testid={`policy-gate-error-${theme}`}>{gateError.message}</p>}
      <section aria-label={`${labels[theme]} synthetic claim result`} data-testid={`policy-gate-${theme}`} aria-live="polite" aria-busy={evaluating}>
        {gate && <><p><strong>{operatorLabel(gate.status)}</strong></p>{gate.claim_gates.map(g=><p className="policy-code" key={g.claim_index}>{operatorLabel(g.claim_type)} · {operatorLabel(g.status)}<br />Citations: {g.trusted_citation_chunk_ids.join(', ') || 'no trusted citations'}<br />{operatorLabels(g.reason_codes).join(' · ') || 'No structural rejection reason'}</p>)}<p>Semantic meaning, personal-data handling, prompt-injection resistance, and action wording require human review. No AI model runs in this check. A structural pass does not prove semantic grounding, policy applicability, or financial authority.</p><details><summary>Structural-check limitations</summary>{gate.limitations.map((s,i)=><p key={i}>{s}</p>)}</details></>}
      </section>
    </div>
  </details>;
}
