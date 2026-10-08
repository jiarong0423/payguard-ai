import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { AllCommunityModule, ModuleRegistry, themeQuartz } from 'ag-grid-community';
import { apiRequest } from './api.js';
import ReferencePanel from './ReferencePanel.jsx';
import PolicyPanel from './PolicyPanel.jsx';
import { downloadPseudonymizedEvidence } from './pseudonymizedExport.js';
import { downloadInternalReviewZip, INTERNAL_REVIEW_ZIP_CONTENTS } from './reviewZip.js';
import { operatorLabel, operatorLabels, sandboxReadbackLabel } from './operatorLabels.js';

const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard.jsx'));

ModuleRegistry.registerModules([AllCommunityModule]);

const gridTheme = themeQuartz.withParams({
  backgroundColor: '#ffffff', foregroundColor: '#1e293b', borderColor: '#e2e8f0',
  headerBackgroundColor: '#f8fafc', headerTextColor: '#475569', accentColor: '#0d9488',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', fontSize: 14,
  wrapperBorderRadius: 10, rowHoverColor: '#f0fdfa', cellHorizontalPadding: 18,
});

function Icon({ name, size = 18, ...props }) {
  const paths = {
    shield: <><path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Z" /><path d="m8 12 3 3 5-6" /></>,
    arrow: <><path d="M5 12h14M13 6l6 6-6 6" /></>,
    bolt: <path d="m13 2-9 12h7l-1 8 10-13h-7l0-7Z" />,
    chart: <><path d="M4 4v16h16M7 15l4-5 4 3 5-7" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    layers: <><path d="m12 3 9 5-9 5-9-5 9-5ZM3 12l9 5 9-5M3 16l9 5 9-5" /></>,
    file: <><path d="M14 3H5v18h14V8l-5-5Z" /><path d="M14 3v6h5M8 13h8M8 17h6" /></>,
    refresh: <><path d="M20 7v5h-5M4 17v-5h5" /><path d="M5.6 7a8 8 0 0 1 13-2L20 7M4 17l1.4 2a8 8 0 0 0 13-2" /></>,
    link: <><path d="m10 13 4-4M8 16l-1 1a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0M16 8l1-1a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6 0" /></>,
    alert: <><path d="m12 3 10 18H2L12 3Z" /><path d="M12 9v5M12 17h.01" /></>,
    lock: <><rect x="5" y="10" width="14" height="11" rx="2" /><path d="M8 10V6a4 4 0 0 1 8 0v4M12 14v3" /></>,
    close: <path d="m6 6 12 12M18 6 6 18" />,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>{paths[name] || paths.shield}</svg>;
}

function Badge({ children, tone = 'muted', dot = false }) {
  return <span className={`badge badge-${tone}`}>{dot && <span className="status-dot" />}{children}</span>;
}

function Button({ children, icon, tone = 'secondary', loading = false, ...props }) {
  return <button className={`button button-${tone}`} {...props} aria-busy={loading}>{loading ? <span className="spinner" /> : icon && <Icon name={icon} size={16} />}{children}</button>;
}

function SectionTitle({ number, title, subtitle, icon, children }) {
  return <div className="section-heading"><div className="section-label"><span className="section-number">{number}</span><div><h2><Icon name={icon} size={19} />{title}</h2><p>{subtitle}</p></div></div>{children}</div>;
}

function StageAccordion({ id, number, title, subtitle, icon, status, open, onOpen, children }) {
  const triggerId = `stage-trigger-${id}`;
  const contentId = `stage-content-${id}`;
  return <section id={id} className={`panel stage-accordion stage-${number} ${open ? 'is-open' : 'is-collapsed'}`}>
    <h2 className="stage-heading"><button id={triggerId} data-testid={`stage-toggle-${id}`} className="stage-trigger" type="button" aria-expanded={open} aria-controls={contentId} onClick={() => onOpen(id)}><span className="stage-trigger-label"><span className="stage-number">{number}</span><span><span className="stage-title"><Icon name={icon} size={19} />{title}</span><small>{subtitle}</small></span></span><span className="stage-trigger-meta">{status}<span className="stage-chevron" aria-hidden="true" /></span></button></h2>
    <div id={contentId} className="stage-content" role="region" aria-labelledby={triggerId} hidden={!open}>{children}</div>
  </section>;
}

function OptionalDisclosure({ id, title, subtitle, icon, badge, open, onToggle, children, testId }) {
  const triggerId = `${id}-trigger`;
  const contentId = `${id}-content`;
  return <section id={id} className={`optional-disclosure ${open ? 'is-open' : ''}`}>
    <h2><button id={triggerId} data-testid={testId} className="optional-trigger" type="button" aria-expanded={open} aria-controls={contentId} onClick={() => onToggle(!open)}><span><Icon name={icon} size={18} /><span><strong>{title}</strong><small>{subtitle}</small></span></span><span className="optional-trigger-meta">{badge}<span className="stage-chevron" aria-hidden="true" /></span></button></h2>
    <div id={contentId} className="optional-content" role="region" aria-labelledby={triggerId} hidden={!open}>{children}</div>
  </section>;
}

function dateLabel(value) {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : `${date.toLocaleString('en-US', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}

function sandboxEvidenceLabel(receipt) {
  return operatorLabel(receipt?.evidence_class, 'Connection not verified');
}

function velocityStageStatusLabel(velocity) {
  if (velocity?.status === 'review_velocity') return 'Needs fulfillment review';
  if (velocity?.status === 'normal') return 'No review signal';
  return 'Baseline unavailable';
}

function AiBriefPanel({ stage, available, brief, loading, onGenerate }) {
  const [open, setOpen] = useState(false);
  useEffect(() => { if (brief) setOpen(true); }, [brief]);
  return <section className="ai-brief-panel" data-testid={`ai-brief-${stage}`}>
    <div className="ai-brief-heading"><div><span className="meta-label">OPTIONAL AI EVIDENCE BRIEF</span><h3>{brief ? 'Generated evidence brief' : 'Fixed synthetic evidence brief'}</h3></div><Button data-testid={`ai-generate-${stage}`} icon="layers" tone="secondary" loading={loading} disabled={!available || loading || Boolean(brief)} onClick={() => onGenerate(stage)}>{brief ? 'AI brief generated' : 'Generate AI brief'}</Button></div>
    <details className="ai-brief-details" open={open} onToggle={(event) => setOpen(event.currentTarget.open)}><summary>{brief ? 'View evidence, citations, and limitations' : 'Why this optional AI call is bounded'}</summary><div className="ai-brief-detail-body"><p className="ai-boundary">Uses only backend-fixed synthetic facts and pinned citation IDs. It does not use current merchant, product, transaction, or case data. The backend permits at most three model attempts per process and one attempt per stage; failed attempts count and no automatic retry occurs. AI makes no compliance or dispute decision and authorizes no PayPal action.</p>{!available && <p className="text-dim">Complete deterministic preflight first, then let a human decide whether to call AI.</p>}{brief && <div className="ai-brief-result" aria-live="polite"><div className="ai-brief-badges"><Badge tone="blue">AI GENERATED</Badge><Badge tone="blue">{brief.model}</Badge><Badge tone="muted">{operatorLabel(brief.prompt_contract_id)}</Badge><Badge tone="muted">{operatorLabel(brief.execution_evidence)}</Badge><Badge tone="amber">HUMAN REVIEW REQUIRED</Badge></div><p className="ai-summary">{brief.brief.summary}</p><div className="ai-brief-columns"><div><strong>Evidence points</strong><ul>{brief.brief.evidence_points.map((item) => <li key={item}>{item}</li>)}</ul></div><div><strong>Missing evidence</strong><ul>{brief.brief.missing_evidence.map((item) => <li key={item}>{item}</li>)}</ul></div></div><p className="ai-citations">Source references: {brief.brief.citation_ids.join(' · ')}</p><ul className="ai-limitations">{brief.limitations.map((item) => <li key={item}>{item}</li>)}</ul><p className="ai-authority">{operatorLabel(brief.compliance_decision)} · {operatorLabel(brief.current_policy_applicability)} · {operatorLabel(brief.semantic_entailment)} · {operatorLabel(brief.external_action_authorized === false ? 'EXTERNAL_ACTION_FALSE' : '')}</p></div>}</div></details>
  </section>;
}

const AUP_POLICY_URL = 'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full';

const findingLabels = {
  unsupported_financial_promise: 'Unsupported return claim', weapons: 'Weapons-related goods',
  controlled_substances: 'Controlled substances', counterfeit_goods: 'Counterfeit goods', regulated_activity: 'Regulated activity',
};

export default function App() {
  const sessionRef = useRef(null);
  const mounted = useRef(true);
  const [state, setState] = useState(null);
  const [sandbox, setSandbox] = useState(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [error, setError] = useState(null);
  const [notice, setNotice] = useState('');
  const [aiBriefs, setAiBriefs] = useState({});
  const [aiBusyStage, setAiBusyStage] = useState('');
  const [analyticsOpen, setAnalyticsOpen] = useState(false);
  const [activeStage, setActiveStage] = useState('compliance');
  const [analyticsExpanded, setAnalyticsExpanded] = useState(false);
  const [activityExpanded, setActivityExpanded] = useState(false);
  const [openSecondary, setOpenSecondary] = useState({ source_compliance: null, velocity_guard: null, dispute_mediation: null });
  const toggleSecondary = useCallback((theme, panel, nextOpen) => {
    setOpenSecondary((current) => {
      if (nextOpen) return current[theme] === panel ? current : { ...current, [theme]: panel };
      return current[theme] === panel ? { ...current, [theme]: null } : current;
    });
  }, []);
  const openStage = useCallback((stage, { updateHash = false, scroll = false } = {}) => {
    if (!['compliance', 'velocity', 'disputes'].includes(stage)) return;
    setActiveStage(stage);
    if (updateHash && window.location.hash !== `#${stage}`) window.history.pushState(null, '', `#${stage}`);
    if (scroll) window.requestAnimationFrame(() => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      document.getElementById(stage)?.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    });
  }, []);
  useEffect(() => {
    const syncFromHash = () => {
      const target = window.location.hash.slice(1);
      if (['compliance', 'velocity', 'disputes'].includes(target)) setActiveStage(target);
      setAnalyticsExpanded(target === 'analytics');
    };
    syncFromHash();
    window.addEventListener('hashchange', syncFromHash);
    window.addEventListener('popstate', syncFromHash);
    return () => {
      window.removeEventListener('hashchange', syncFromHash);
      window.removeEventListener('popstate', syncFromHash);
    };
  }, []);
  useEffect(() => {
    const focused = document.activeElement;
    if (focused instanceof Element && focused.closest('.stage-content[hidden]')) {
      document.getElementById(`stage-trigger-${activeStage}`)?.focus();
    }
  }, [activeStage]);
  useEffect(() => {
    if (!notice) return undefined;
    const timer = window.setTimeout(() => setNotice(''), 3600);
    return () => window.clearTimeout(timer);
  }, [notice]);
  const aiRevisionRef = useRef(0);
  const aiControllerRef = useRef(null);
  const invalidateAi = useCallback(() => {
    aiRevisionRef.current += 1;
    aiControllerRef.current?.abort();
    aiControllerRef.current = null;
    setAiBriefs({});
    setAiBusyStage('');
  }, []);
  const [description, setDescription] = useState('Handcrafted ceramic coffee cup — set of two');
  const [aup, setAup] = useState(null);
  const [aupPhase, setAupPhase] = useState('empty');
  const [aupConsumed, setAupConsumed] = useState(false);
  const [warningOpen, setWarningOpen] = useState(false);
  const aupRevisionRef = useRef(0);
  const aupControllerRef = useRef(null);
  const busyRef = useRef('');
  const warningRef = useRef(null);
  const invalidateAup = useCallback(() => {
    invalidateAi();
    aupRevisionRef.current += 1;
    aupControllerRef.current?.abort();
    aupControllerRef.current = null;
    setAup(null); setAupPhase('empty'); setAupConsumed(false); setWarningOpen(false);
    setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false);
  }, [invalidateAi]);
  const editDescription = (value) => { invalidateAup(); setDescription(value); };
  useEffect(() => {
    if (!aup) return;
    const timer = setTimeout(() => {
      invalidateAup(); setNotice('The description check expired. Run it again before continuing.');
    }, Math.max(0, Date.parse(aup.expires_at) - Date.now()));
    return () => clearTimeout(timer);
  }, [aup, invalidateAup]);
  useEffect(() => {
    if (!warningOpen) return;
    const previous = document.activeElement;
    warningRef.current?.querySelector('button')?.focus();
    return () => {
      if (previous?.isConnected && !previous.disabled) previous.focus();
      else document.getElementById('description')?.focus();
    };
  }, [warningOpen]);
  const [selectedCase, setSelectedCase] = useState('');
  const [draft, setDraft] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [reviewChecked, setReviewChecked] = useState(false);
  const [invoiceAmount, setInvoiceAmount] = useState('10.00');
  const [invoiceReview, setInvoiceReview] = useState(null);
  const [invoice, setInvoice] = useState(null);
  const [invoiceChecked, setInvoiceChecked] = useState(false);
  const [velocityQuickFilter, setVelocityQuickFilter] = useState('');
  const [selectedVelocityTransaction, setSelectedVelocityTransaction] = useState(null);
  const editInvoiceAmount = (value) => {
    if (invoiceReview || invoice || aupConsumed) {
      invalidateAup();
      setNotice('Draft amount changed. Run Policy Check again before confirming the draft context.');
    } else {
      setInvoiceReview(null);
      setInvoice(null);
      setInvoiceChecked(false);
    }
    setInvoiceAmount(value);
  };
  const referenceRevisionRef = useRef(0);
  const [referenceRevision, setReferenceRevision] = useState(0);
  const invalidateReferences = useCallback(() => {
    referenceRevisionRef.current += 1;
    setReferenceRevision(referenceRevisionRef.current);
  }, []);
  const expireSession = useCallback((failure, identity, expectedRevision) => {
    if (sessionRef.current?.session_id !== identity || referenceRevisionRef.current !== expectedRevision) return;
    invalidateReferences();
    invalidateAup();
    sessionRef.current = null;
    setState(null); setDraft(null); setReceipt(null); setSelectedCase('');
    setReviewChecked(false); setAup(null); setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false);
    setVelocityQuickFilter(''); setSelectedVelocityTransaction(null);
    setError(failure);
  }, [invalidateReferences, invalidateAup]);

  const bootstrap = useCallback(async (signal) => {
    invalidateReferences();
    invalidateAup();
    setLoading(true);
    setError(null);
    setState(null);
    sessionRef.current = null;
    setDraft(null);
    setReceipt(null);
    setAup(null);
    setSelectedCase('');
    setInvoiceReview(null);
    setInvoice(null);
    setInvoiceChecked(false);
    setVelocityQuickFilter('');
    setSelectedVelocityTransaction(null);
    try {
      const session = await apiRequest('/demo/sessions', { method: 'POST', body: {}, signal });
      if (signal?.aborted || !mounted.current) return;
      sessionRef.current = session;
      const [nextState, status] = await Promise.all([
        apiRequest('/demo/state', { session, signal }), apiRequest('/paypal/status', { session, signal }),
      ]);
      if (signal?.aborted || !mounted.current) return;
      setState(nextState);
      setSandbox(status);
    } catch (failure) {
      if (!signal?.aborted && mounted.current) setError(failure);
    } finally {
      if (!signal?.aborted && mounted.current) setLoading(false);
    }
  }, [invalidateReferences, invalidateAup]);

  useEffect(() => {
    mounted.current = true;
    const controller = new AbortController();
    bootstrap(controller.signal);
    return () => { mounted.current = false; sessionRef.current = null; aupControllerRef.current?.abort(); aiControllerRef.current?.abort(); controller.abort(); };
  }, [bootstrap]);

  const action = async (key, run) => {
    if (busyRef.current || !sessionRef.current) return;
    const identity = sessionRef.current.session_id;
    let revision = referenceRevisionRef.current;
    busyRef.current = key;
    setBusy(key);
    setError(null);
    setNotice('');
    if (key === 'reset') { invalidateReferences(); invalidateAup(); revision = referenceRevisionRef.current; }
    try { await run(sessionRef.current); }
    catch (failure) {
      if (failure.code === 'request_cancelled' || sessionRef.current?.session_id !== identity) return;
      setError(failure);
      if (failure.status === 401) expireSession(failure, identity, revision);
    }
    finally { busyRef.current = ''; if (mounted.current) setBusy(''); }
  };

  const generateAiBrief = async (stage) => {
    if (aiControllerRef.current || busyRef.current || !sessionRef.current) return;
    invalidateAi();
    const controller = new AbortController();
    aiControllerRef.current = controller;
    const revision = aiRevisionRef.current;
    const identity = sessionRef.current.session_id;
    const session = sessionRef.current;
    const referenceRevision = referenceRevisionRef.current;
    setAiBusyStage(stage);
    setError(null);
    setNotice('');
    try {
      const result = await apiRequest('/ai/evidence-brief', { method: 'POST', body: { stage }, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aiRevisionRef.current || sessionRef.current?.session_id !== identity) return;
      setAiBriefs({ [stage]: result });
    } catch (failure) {
      if (controller.signal.aborted || revision !== aiRevisionRef.current || sessionRef.current?.session_id !== identity) return;
      setAiBriefs({});
      setError(failure);
      if (failure.status === 401) expireSession(failure, identity, referenceRevision);
    } finally {
      if (aiControllerRef.current === controller) aiControllerRef.current = null;
      if (mounted.current && revision === aiRevisionRef.current) setAiBusyStage('');
    }
  };

  const inject = (scenario) => action(scenario, async (session) => {
    invalidateAi();
    const nextState = await apiRequest('/demo/inject', { method: 'POST', body: { scenario }, session });
    setState(nextState);
    if (scenario === 'reset') {
      setDraft(null); setReceipt(null); setSelectedCase(''); setReviewChecked(false);
      setAup(null); setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false);
      setVelocityQuickFilter(''); setSelectedVelocityTransaction(null);
    }
    setNotice(scenario === 'reset' ? 'Demo data reset; the session remains active.' : 'Synthetic scenario injected; repeated injection adds no duplicate data.');
  });

  const disabled = loading || Boolean(busy) || !state || error?.status === 401;
  const referenceProps = { session: state ? sessionRef.current : null, revision: referenceRevision, unavailable: disabled, onSessionExpired: expireSession };
  const velocity = state?.velocity;
  const caseItem = state?.disputes?.find((item) => item.case_ref === selectedCase) || state?.disputes?.[0];
  useEffect(() => {
    if (!selectedVelocityTransaction) return;
    const current = state?.transactions?.find((transaction) => transaction.order_id === selectedVelocityTransaction.order_id);
    if (!current) {
      setSelectedVelocityTransaction(null);
      setVelocityQuickFilter('');
    } else if (current !== selectedVelocityTransaction) {
      setSelectedVelocityTransaction(current);
    }
  }, [selectedVelocityTransaction, state?.transactions]);
  const columns = useMemo(() => [
    { field: 'order_id', headerName: 'ORDER ID', minWidth: 190, flex: 1.4, cellRenderer: ({ value }) => <span className="grid-order"><span className="tiny-dot" />{value}</span> },
    { field: 'amount', headerName: 'AMOUNT', minWidth: 120, flex: 1, cellClass: 'grid-amount', valueFormatter: ({ value }) => value ?? '—' },
    { field: 'currency', headerName: 'CURRENCY', minWidth: 100, flex: 0.7 },
    { field: 'occurred_at', headerName: 'CAPTURED AT', minWidth: 180, flex: 1.2, valueFormatter: ({ value }) => dateLabel(value) },
  ], []);

  const scan = () => action('aup', async (session) => {
    invalidateAup();
    const revision = aupRevisionRef.current;
    const controller = new AbortController();
    aupControllerRef.current = controller;
    setAupPhase('loading');
    try {
      const result = await apiRequest('/aup/review', { method: 'POST', body: { description }, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
      setAup(result); setAupPhase('completed');
    } catch (failure) {
      if (!controller.signal.aborted && revision === aupRevisionRef.current) setAupPhase('error');
      throw failure;
    } finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
  });
  const getDraft = () => action('draft', async (session) => {
    invalidateAi();
    const result = await apiRequest(`/disputes/${encodeURIComponent(caseItem.case_ref)}/draft`, { method: 'POST', body: {}, session });
    setSelectedCase(caseItem.case_ref); setDraft(result); setReceipt(null); setReviewChecked(false);
    setState(await apiRequest('/demo/state', { session }));
  });
  const approve = () => action('approve', async (session) => {
    const result = await apiRequest(`/disputes/${encodeURIComponent(draft.case_ref)}/approve`, { method: 'POST', body: { draft_digest: draft.draft_digest }, session });
    setReceipt(result);
    setState(await apiRequest('/demo/state', { session }));
    setNotice('Local draft review recorded; no evidence was submitted to PayPal.');
  });
  const downloadRedactedFile = () => {
    try {
      downloadPseudonymizedEvidence(draft?.document_redaction);
      setError(null);
      setNotice('Pseudonymized evidence file downloaded locally; no file was submitted to PayPal.');
    } catch {
      setNotice('');
      setError({ status: 422, code: 'pseudonymized_export_invalid', message: 'The pseudonymized file could not be created from this draft.' });
    }
  };
  const downloadReviewZip = () => {
    try {
      downloadInternalReviewZip(draft);
      setError(null);
      setNotice('Internal review ZIP downloaded locally. It is not a PayPal evidence attachment, is not complete official evidence, and was not submitted. Verify the live dispute response and original evidence before any external use.');
    } catch {
      setNotice('');
      setError({ status: 422, code: 'internal_review_zip_invalid', message: 'Internal Review ZIP creation failed. No file was downloaded or submitted to PayPal.' });
    }
  };
  const bindInvoice = async (session, evaluation, acknowledgementToken, revision, signal) => {
    const result = await apiRequest('/paypal/invoices/review', { method: 'POST', body: {
      description, amount: invoiceAmount, currency: 'USD', confirm_sandbox_draft: true,
      evaluation_id: evaluation.evaluation_id, description_digest: evaluation.description_digest,
      acknowledgement_token: acknowledgementToken,
    }, session, signal });
    if (!mounted.current || signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
    setInvoiceReview(result); setInvoice(null); setAupConsumed(true); setWarningOpen(false);
  };
  const reviewInvoice = () => {
    if (!aup || aupConsumed || busyRef.current) return;
    if (aup.match_status === 'REVIEW_SIGNAL') { setWarningOpen(true); return; }
    return action('invoice-review', async (session) => {
      const revision = aupRevisionRef.current;
      const controller = new AbortController(); aupControllerRef.current = controller;
      try { await bindInvoice(session, aup, null, revision, controller.signal); }
      catch (failure) { if (!controller.signal.aborted && revision === aupRevisionRef.current) invalidateAup(); throw failure; }
      finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
    });
  };
  const chooseWarning = (choice) => action('aup-choice', async (session) => {
    const evaluation = aup;
    if (!evaluation || !warningOpen) return;
    const revision = aupRevisionRef.current;
    const controller = new AbortController(); aupControllerRef.current = controller;
    try {
      const result = await apiRequest('/aup/acknowledge', { method: 'POST', body: {
        evaluation_id: evaluation.evaluation_id, description_digest: evaluation.description_digest, choice,
      }, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
      if (choice === 'ACKNOWLEDGE_AND_CONTINUE') {
        await bindInvoice(session, evaluation, result.acknowledgement_token, revision, controller.signal);
      } else {
        invalidateAup();
        setNotice(choice === 'RETURN_TO_EDIT' ? 'Returned to editing. Recheck the description after changes.' : 'Draft flow canceled. Recheck the description before continuing again.');
      }
    } catch (failure) { if (!controller.signal.aborted && revision === aupRevisionRef.current) invalidateAup(); throw failure; }
    finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
  });
  const warningKeys = (event) => {
    if (event.key === 'Escape') { event.preventDefault(); if (!busyRef.current) chooseWarning('CANCEL'); return; }
    if (event.key !== 'Tab') return;
    const controls = [...warningRef.current.querySelectorAll('a[href],button:not(:disabled)')];
    if (!controls.length) { event.preventDefault(); return; }
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && (document.activeElement === first || !controls.includes(document.activeElement))) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && (document.activeElement === last || !controls.includes(document.activeElement))) { event.preventDefault(); first.focus(); }
  };
  const connectSandbox = () => action('connect', async (session) => {
    setSandbox(null);
    try {
      const result = await apiRequest('/paypal/connect', { method: 'POST', body: {}, session });
      setSandbox(result);
      setNotice(result.evidence_receipt?.evidence_class === 'AUTHENTIC_SANDBOX_RESPONSE'
        ? 'Live Sandbox connection verified · credentials remain off-screen.'
        : 'Synthetic Sandbox test response · no live provider verification claimed; credentials remain off-screen.');
    } catch (failure) {
      try { setSandbox(await apiRequest('/paypal/status', { session })); }
      catch { setSandbox(null); }
      throw failure;
    }
  });
  const createInvoice = () => action('invoice', async (session) => {
    const result = await apiRequest('/paypal/invoices/draft', { method: 'POST', body: { description, amount: invoiceAmount, currency: 'USD', review_token: invoiceReview.review_token, payload_digest: invoiceReview.payload_digest }, session });
    setInvoice(result); setInvoiceReview(null); setInvoiceChecked(false);
    setNotice(`Sandbox invoice draft created; ${sandboxReadbackLabel(result.evidence_receipt?.separate_get_readback).toLowerCase()}, and nothing was sent.`);
  });

  return <div className="app-shell">
    <a className="skip-link" href="#main">Skip to console</a>
    <header className="topbar" inert={warningOpen ? true : undefined}>
      <a className="brand" href="#main" aria-label="PayGuard AI console"><span className="brand-mark"><Icon name="shield" size={23} /></span><span>PayGuard<span className="brand-ai"> AI</span><small>MERCHANT EVIDENCE BUFFER</small></span></a>
      <nav aria-label="Primary navigation"><a href="#compliance" aria-current={activeStage === 'compliance' ? 'page' : undefined} onClick={() => setActiveStage('compliance')}>AUP preflight</a><a href="#velocity" aria-current={activeStage === 'velocity' ? 'page' : undefined} onClick={() => setActiveStage('velocity')}>Velocity guard</a><a href="#disputes" aria-current={activeStage === 'disputes' ? 'page' : undefined} onClick={() => setActiveStage('disputes')}>Dispute review</a><a href="#analytics" onClick={() => { setAnalyticsExpanded(true); setAnalyticsOpen(true); }}>Grid analytics</a></nav>
      <div className="environment"><Badge tone="blue" dot>LOCAL DEMO</Badge><span className="avatar">PG</span></div>
    </header>

    <main id="main" tabIndex={-1} inert={warningOpen ? true : undefined} className="main-content" data-testid={state ? "session-ready" : "session-unavailable"}>
      <div className="hero hero-compact">
        <div><div className="eyebrow"><span className="tiny-dot" /> MERCHANT DEFENSE BUFFER</div><h1>Catch missing evidence <span>before provider review.</span></h1><p>When sales spike, PayGuard connects AUP warnings, fulfillment readiness, and dispute evidence while PayPal and external issuers retain final authority.</p></div>
        <div className="hero-meta"><span className="meta-label">WORKSPACE</span><strong>PayGuard / Demo</strong><span><Icon name="layers" size={14} /> Three-stage evidence buffer</span></div>
      </div>

      <div className="journey" aria-label="End-to-end flow">
        {[
          ['01', 'shield', 'AUP preflight screen', 'Product description · policy reminder', '#compliance'],
          ['02', 'chart', 'Sales burst readiness', 'Synthetic transactions · velocity signal', '#velocity'],
          ['03', 'file', 'Dispute mediation', 'Pseudonymization · human review', '#disputes'],
        ].map(([number, icon, title, subtitle, href], index) => <a className={`journey-step ${activeStage === href.slice(1) ? 'is-active' : ''}`} href={href} aria-current={activeStage === href.slice(1) ? 'step' : undefined} onClick={(event) => { event.preventDefault(); openStage(href.slice(1), { updateHash: true, scroll: true }); }} key={number}><span className={`journey-icon journey-icon-${index}`}><Icon name={icon} size={22} /></span><div><span className="journey-kicker">STEP {number}</span><strong>{title}</strong><small>{subtitle}</small></div>{index < 2 && <Icon name="arrow" className="journey-arrow" />}</a>)}
      </div>

      <div className="feedback-region" aria-live="polite" aria-atomic="true">
        {loading && <div className="message message-info"><span className="spinner" />Creating an isolated demo session and loading backend state.</div>}
        {error && <div className="message message-error" role="alert" data-testid="global-error"><Icon name="alert" /><div><strong>{error.status === 401 ? 'Demo session expired' : error.code === 'backend_unavailable' ? 'Backend service unavailable' : 'Action not completed'}</strong><span>{error.message}</span></div>{(!state || error.status === 401) && <Button disabled={loading || Boolean(busy)} icon="refresh" onClick={() => bootstrap()}>Reconnect</Button>}<button className="icon-button" aria-label="Dismiss error message" onClick={() => setError(null)}><Icon name="close" /></button></div>}
        {notice && <div className="message message-success"><Icon name="check" />{notice}</div>}
      </div>

      <section className="overview-panel" aria-label="Demo controls and key indicators">
        <div className="demo-toolbar"><div className="demo-caption"><span className="demo-icon"><Icon name="bolt" /></span><div><strong>Demo control</strong><small>Synthetic scenarios · memory session</small></div></div><div className="demo-actions"><Button data-testid="demo-burst" icon="bolt" tone="blue" disabled={disabled} loading={busy === 'burst'} onClick={() => { openStage('velocity', { updateHash: true, scroll: true }); inject('burst'); }}>Inject sales burst</Button><Button data-testid="demo-dispute" icon="file" disabled={disabled} loading={busy === 'dispute'} onClick={() => { openStage('disputes', { updateHash: true, scroll: true }); inject('dispute'); }}>Inject dispute</Button><Button data-testid="demo-reset" icon="refresh" tone="ghost" disabled={disabled} loading={busy === 'reset'} onClick={() => { openStage('compliance', { updateHash: true, scroll: true }); inject('reset'); }}>Reset</Button></div></div>
        <div className="metrics-grid">
          <Metric label="Window sales" value={velocity?.total_amount ?? '—'} unit={velocity?.currency || 'USD'} icon="chart" detail={`${velocity?.window_hours ?? '—'} hour observation window · synthetic data`} />
          <Metric testId="velocity-ratio" label="Velocity ratio" value={velocity?.ratio ?? '—'} unit="× baseline" icon="bolt" detail={`Backend threshold ${velocity?.threshold ?? '—'}×`} alert={velocity?.alert === true} />
          <Metric label="Window captures" value={velocity?.transaction_count ?? '—'} unit="captures" icon="layers" detail="Unique transaction IDs · backend validated" />
          <Metric label="Sandbox connection" value={sandbox?.status === 'connected' ? 'Connected' : sandbox?.status === 'not_configured' ? 'Not configured' : sandbox?.status === 'error' ? 'Error' : sandbox?.status === 'disconnected' ? 'Disconnected' : '—'} icon="link" detail={sandbox?.last_verified_at ? `${sandboxEvidenceLabel(sandbox.evidence_receipt)} · ${dateLabel(sandbox.last_verified_at)}` : 'Waiting for an explicit OAuth POST response'} compact statusTone={sandbox?.status === 'connected' ? 'success' : sandbox?.status === 'error' ? 'danger' : 'neutral'} />
        </div>
      </section>

      <StageAccordion id="compliance" number="01" title="Pre-transaction / AUP Preflight Screen" subtitle="Review the actual goods or activity before preparing an invoice draft." icon="shield" status={<Badge tone="amber">ADVISORY REVIEW</Badge>} open={activeStage === 'compliance'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className="compliance-layout"><div className="invoice-editor"><div className="description-toolbar"><label className="mini-heading description-label" htmlFor="description">Product or Service Description</label><div className="description-presets"><span>Quick tests</span><button disabled={Boolean(busy)} onClick={() => editDescription('Handcrafted ceramic coffee cup — set of two')}>Standard Item</button><button disabled={Boolean(busy)} onClick={() => editDescription('Guaranteed 30% ROI investment package')}>High-risk Claim</button></div></div><textarea data-testid="aup-description" id="description" maxLength={4000} value={description} onChange={(event) => editDescription(event.target.value)} rows={3} disabled={Boolean(busy)} /><div className="editor-bottom"><span className="text-dim">{description.length} / 4,000 characters</span><Button data-testid="aup-review" icon="shield" tone="blue" onClick={scan} disabled={disabled || !description.trim()} loading={busy === 'aup'}>Run Policy Check</Button></div></div><div data-testid="aup-result" data-state={aupPhase} aria-live="polite" className={`aup-result ${aup?.findings?.length ? 'aup-warning' : ''}`}><div className="result-heading"><span className="result-symbol"><Icon name={aup?.findings?.length ? 'alert' : 'shield'} size={25} /></span><div><span className="meta-label">REVIEW SIGNAL</span><h3>{aupPhase === 'loading' ? 'Checking description' : aupPhase === 'error' ? 'Check incomplete; try again' : !aup ? 'Waiting for description check' : aup.match_status === 'REVIEW_SIGNAL' ? 'Review signal matched' : 'No demo rule matched'}</h3></div></div>{aup ? <><div className="finding-list">{aup.findings.length ? aup.findings.map((finding) => <Badge tone="amber" key={finding.category}>{findingLabels[finding.category] || 'Needs review'}</Badge>) : <Badge tone="muted">No configured demo keyword matched</Badge>}</div><p>{aup.recommendation}</p><span className="result-footnote">{aup.policy_version} · {operatorLabel(aup.compliance_decision)} · <strong data-testid="aup-applicability">{operatorLabel(aup.current_policy_applicability)}</strong> · valid until {dateLabel(aup.expires_at)}</span></> : <><p>Bounded keyword rules produce review signals. Humans confirm the actual goods and applicable policy.</p><span className="result-footnote">Wording changes do not hide restricted activity.</span></>}</div></div>
        <p className="aup-policy-link"><a data-testid="aup-policy-link" href={AUP_POLICY_URL} target="_blank" rel="noopener noreferrer">PayPal US Acceptable Use Policy (official source)</a><span>A match only prompts policy review. PayGuard makes no policy decision.</span></p>
        <p data-testid="aup-invoice-limit" className="text-dim">Input limit: 4,000 characters for screening, 200 for invoice drafts. {description.length > 200 && 'Shorten the description and run the check again before continuing.'}</p>
        <details className="sandbox-details"><summary><Icon name="link" size={16} /><span>Optional PayPal US Sandbox connection</span><span data-testid="sandbox-status"><Badge tone={sandbox?.status === 'connected' ? 'green' : 'muted'} dot>{operatorLabel(sandbox?.status, 'Status not loaded')}</Badge></span></summary><div className="sandbox-inner"><p>Sandbox OAuth runs only after an explicit connect action. Credentials remain in the backend process environment. The flow creates an unsent draft only, and every receipt is labeled as live Sandbox evidence or synthetic test evidence.</p><div className="sandbox-connect"><Button data-testid="sandbox-connect" icon="link" disabled={disabled} loading={busy === 'connect'} onClick={connectSandbox}>Connect US Sandbox</Button>{!sandbox?.configured && <span className="text-dim">Connect checks backend configuration and reports disabled outbound access explicitly.</span>}</div>{sandbox?.evidence_receipt && <p className="sandbox-readback">Connection evidence: {sandboxEvidenceLabel(sandbox.evidence_receipt)} · {sandboxReadbackLabel(sandbox.evidence_receipt.separate_get_readback)}</p>}<div className="invoice-draft-form"><label>Draft amount <span className="text-dim">USD</span><input type="text" inputMode="decimal" value={invoiceAmount} maxLength={20} disabled={Boolean(busy)} onChange={(event) => editInvoiceAmount(event.target.value)} /></label><label className="checkbox-label"><input data-testid="invoice-confirm" type="checkbox" checked={invoiceChecked} disabled={Boolean(busy)} onChange={(event) => setInvoiceChecked(event.target.checked)} /><span>I reviewed the description and amount and confirm that this action creates a Sandbox draft only.</span></label><Button data-testid="invoice-review" icon="check" disabled={disabled || !invoiceChecked || !aup || aupConsumed || description.length > 200} loading={busy === 'invoice-review'} onClick={reviewInvoice}>Confirm Draft Context</Button><Button data-testid="invoice-create" icon="file" tone="blue" disabled={disabled || !invoiceReview || !invoiceChecked || sandbox?.status !== 'connected'} loading={busy === 'invoice'} onClick={createInvoice}>Create Sandbox draft</Button></div>{invoiceReview && <p className="sandbox-readback">{operatorLabel('PAYLOAD_DIGEST_BOUND')} · valid until {dateLabel(invoiceReview.expires_at)}</p>}{invoice && <p className="sandbox-readback">Sandbox invoice draft created · {operatorLabel(invoice.status)} · {sandboxEvidenceLabel(invoice.evidence_receipt)} · {sandboxReadbackLabel(invoice.evidence_receipt.separate_get_readback)} · {operatorLabel(invoice.external_send)}</p>}</div></details>
        <ReferencePanel theme="source_compliance" {...referenceProps} open={openSecondary.source_compliance === 'reference'} onToggle={(nextOpen) => toggleSecondary('source_compliance', 'reference', nextOpen)} />
        <PolicyPanel theme="source_compliance" {...referenceProps} open={openSecondary.source_compliance === 'policy'} onToggle={(nextOpen) => toggleSecondary('source_compliance', 'policy', nextOpen)} />
        <AiBriefPanel stage="source_compliance" available={aup?.match_status === 'REVIEW_SIGNAL' && !aupConsumed && !disabled && !busy && !aiBusyStage} brief={aiBriefs.source_compliance} loading={aiBusyStage === 'source_compliance'} onGenerate={generateAiBrief} />
      </StageAccordion>

      <StageAccordion id="velocity" number="02" title="Fulfillment / Velocity Guard" subtitle="Compares local sales velocity and surfaces evidence-readiness gaps for human review." icon="chart" status={<Badge tone={velocity?.alert ? 'amber' : velocity?.transaction_count > 0 && velocity?.status === 'normal' ? 'green' : 'muted'} dot>{velocity ? velocity.status === 'review_velocity' ? 'Needs evidence' : velocity.transaction_count > 0 ? 'Within demo threshold' : 'No in-window data' : 'Waiting'}</Badge>} open={activeStage === 'velocity'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className={`velocity-summary ${velocity?.alert ? 'velocity-alert' : ''}`}><div><Icon name={velocity?.alert ? 'alert' : 'chart'} /><span>{velocity?.alert ? 'Velocity exceeds the demo threshold. Review orders and fulfillment evidence.' : velocity?.transaction_count > 0 ? 'The backend calculated an in-window signal from synthetic captures.' : 'No synthetic captures fall inside the current observation window.'}</span></div><span className="velocity-window"><Icon name="clock" size={14} />{dateLabel(velocity?.window_end)}</span></div>
        <div className="grid-caption"><span><span className="tiny-dot" /> SYNTHETIC CAPTURE STREAM</span><span>AG Grid Community <Badge tone="muted">Backend-owned data</Badge></span></div>
        <div className="velocity-grid-tools"><label htmlFor="velocity-quick-filter">Filter transactions</label><input data-testid="velocity-filter" id="velocity-quick-filter" type="text" value={velocityQuickFilter} onChange={(event) => setVelocityQuickFilter(event.target.value)} placeholder="Order reference, amount, currency, or capture time" disabled={disabled} /></div>
        <div className="transaction-grid" data-testid="velocity-grid" aria-label="Synthetic transaction table"><AgGridReact theme={gridTheme} rowData={state?.transactions || []} columnDefs={columns} defaultColDef={{ sortable: true, resizable: true, filter: true }} getRowId={({ data }) => data.order_id} getRowClass={({ data }) => data?.order_id === selectedVelocityTransaction?.order_id ? 'ag-row-selected-transaction' : ''} quickFilterText={velocityQuickFilter} onRowClicked={({ data }) => setSelectedVelocityTransaction(data)} rowHeight={43} headerHeight={42} animateRows loading={loading || !state} overlayLoadingTemplate="Loading backend data" overlayNoRowsTemplate="No transactions; inject a sales-burst scenario" /></div>
        {selectedVelocityTransaction && <section className="velocity-selected-detail" data-testid="velocity-selected-detail" aria-label="Selected transaction details"><div className="velocity-selected-heading"><div><span className="meta-label">SELECTED TRANSACTION</span><h3>{selectedVelocityTransaction.order_id}</h3></div><Badge tone={velocity?.status === 'review_velocity' ? 'amber' : velocity?.status === 'normal' ? 'green' : 'muted'}><span data-testid="velocity-stage-status">{velocityStageStatusLabel(velocity)}</span></Badge></div><dl><div><dt>Order reference</dt><dd>{selectedVelocityTransaction.order_id}</dd></div><div><dt>Amount</dt><dd>{selectedVelocityTransaction.amount ?? '—'} {selectedVelocityTransaction.currency || '—'}</dd></div><div><dt>Captured at</dt><dd>{dateLabel(selectedVelocityTransaction.occurred_at)}</dd></div><div><dt>Stage evidence checklist</dt><dd>{velocityStageStatusLabel(velocity)}</dd></div></dl><p>This stage-level signal is not a per-order fraud classification and does not predict any PayPal action.</p></section>}
        <div className="panel-foot"><span><Icon name="lock" size={13} /> This signal does not predict PayPal account limitations and does not initiate payments or provider filings.</span><span data-testid="velocity-baseline">Baseline {velocity?.baseline_amount_per_hour ?? '—'} USD/hour · {operatorLabel(velocity?.baseline_provenance)} · {dateLabel(velocity?.baseline_window_start)} to {dateLabel(velocity?.baseline_window_end)}</span><span>{state?.policy_version || 'POLICY —'}</span></div>
        <ReferencePanel theme="velocity_guard" {...referenceProps} open={openSecondary.velocity_guard === 'reference'} onToggle={(nextOpen) => toggleSecondary('velocity_guard', 'reference', nextOpen)} />
        <PolicyPanel theme="velocity_guard" {...referenceProps} open={openSecondary.velocity_guard === 'policy'} onToggle={(nextOpen) => toggleSecondary('velocity_guard', 'policy', nextOpen)} />
        <AiBriefPanel stage="velocity_guard" available={velocity?.status === 'review_velocity' && !disabled && !busy && !aiBusyStage} brief={aiBriefs.velocity_guard} loading={aiBusyStage === 'velocity_guard'} onGenerate={generateAiBrief} />
      </StageAccordion>

      <StageAccordion id="disputes" number="03" title="Post-transaction / Dispute Center" subtitle="Prepare pseudonymized evidence, then record a human review." icon="file" status={<Badge tone="frozen"><Icon name="lock" size={12} /> HUMAN REVIEW GATE</Badge>} open={activeStage === 'disputes'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className="dispute-layout"><div className="case-list"><div className="mini-heading"><span>Case queue</span><span className="text-dim">Synthetic cases</span></div>{state?.disputes?.length ? state.disputes.map((item) => <button key={item.case_ref} className={`case-card ${caseItem?.case_ref === item.case_ref ? 'case-selected' : ''}`} disabled={Boolean(busy)} onClick={() => { invalidateAi(); setSelectedCase(item.case_ref); setDraft(null); setReceipt(null); setReviewChecked(false); }}><div><Icon name="file" /><strong>{item.case_ref}</strong><Badge tone="amber">{operatorLabel(item.reason)}</Badge></div><span>{item.order_ref}</span><small>{dateLabel(item.opened_at)} · {operatorLabel(item.status)}</small></button>) : <div className="empty-state"><Icon name="file" size={32} /><strong>No dispute cases</strong><p>Use "Inject dispute" above to load test data.</p></div>}<div className="case-note"><Icon name="shield" size={15} /><p>A delivery event is one evidence point. It does not establish buyer intent or decide the dispute.</p></div></div><div className="evidence-workspace"><div className="evidence-toolbar"><div><span className="meta-label">EVIDENCE WORKSPACE</span><h3>{receipt ? 'Local draft review recorded' : draft ? 'Draft created · awaiting human review' : caseItem ? 'Prepare objective evidence draft' : 'Human in the loop'}</h3></div><Button data-testid="dispute-draft" icon="file" disabled={disabled || !caseItem || caseItem.status === 'local_draft_reviewed'} loading={busy === 'draft'} onClick={getDraft}>Generate evidence draft</Button></div>{draft ? <><div className="evidence-grid">{[['Case reason', operatorLabel(draft.evidence?.reason)], ['Carrier status', operatorLabel(draft.evidence?.carrier_status)], ['Order created', dateLabel(draft.evidence?.order_created_at)], ['Delivery event', dateLabel(draft.evidence?.delivered_at)], ['Dispute opened', dateLabel(draft.evidence?.opened_at)], ['Evidence source', operatorLabel(draft.evidence?.evidence_source)]].map(([label, value]) => <div key={label}><span>{label}</span><strong>{value || '—'}</strong></div>)}</div><div className="dispute-route" data-testid="dispute-route"><div><span>Provider-response route</span><strong>{operatorLabel(draft.routing?.overall_state)}</strong><small>{operatorLabel(draft.routing?.reason)} · {operatorLabel(draft.routing?.dispute_life_cycle_stage)} · {operatorLabel(draft.routing?.status)}</small><small data-testid="dispute-due-at">Due {dateLabel(draft.routing?.seller_response_due_date)}</small><small data-testid="dispute-actions">Available actions: {operatorLabels(draft.routing?.available_actions).join(', ') || 'None'}</small></div><Badge tone={draft.routing?.due_state === 'OPEN' ? 'green' : 'danger'}><span data-testid="dispute-due-state">{operatorLabel(draft.routing?.due_state)}</span></Badge></div><div className="requirement-list" data-testid="dispute-requirements">{draft.routing?.requirements?.map((row) => <div key={row.request_id}><div><strong>{operatorLabel(row.provider_evidence_type)}</strong><span>{operatorLabel(row.source)}</span><small>Next step: {operatorLabel(row.action, 'No action requested')}</small></div><Badge tone={row.requirement_state === 'STRUCTURALLY_PRESENT' ? 'green' : row.requirement_state.includes('MISSING') ? 'amber' : 'muted'}>{operatorLabel(row.requirement_state)}</Badge><small>{row.proof_count} proof record(s) · {row.accepted_attachment_count} accepted attachment(s)</small></div>)}</div><div className="restricted-summary" data-testid="restricted-original-summary"><Icon name="lock" /><div><strong>Original identifiers stay in this demo session</strong><span>{draft.restricted_original_summary?.proof_record_count} proof record(s) · {draft.restricted_original_summary?.attachment_count} attachment metadata record(s)</span><small>No original file content is included, and nothing is submitted externally.</small></div></div><div className="privacy-strip" data-testid="internal-review-profile"><Icon name="lock" /><div><strong>Internal pseudonymized review copy</strong><span>{draft.document_redaction?.method || '—'} · {draft.document_redaction?.replacement_count ?? 0} replacements</span><small>Limited detection; manual review is required. Pseudonymization is not anonymization.</small></div><Button data-testid="download-pseudonymized-evidence" className="privacy-download" icon="file" onClick={downloadRedactedFile} disabled={disabled || !draft.document_redaction}>Download pseudonymized file</Button><Button data-testid="download-internal-review-zip" icon="file" onClick={downloadReviewZip} disabled={disabled || !draft}>Download Internal Review ZIP</Button></div><div className="zip-contents" data-testid="internal-review-zip-contents"><strong>Internal Review ZIP contents</strong><ul>{INTERNAL_REVIEW_ZIP_CONTENTS.map((name) => <li key={name}>{name}</li>)}</ul><small>Six fixed files · generated locally · not sent to PayPal</small></div><p className="review-warning" data-testid="internal-review-zip-boundary"><strong>INTERNAL REVIEW ONLY</strong> — This synthetic, pseudonymized preparation package is not a PayPal-supported attachment. Required fields present does not prove authenticity, sufficiency, eligibility, completeness, or outcome. PayPal or the external issuer keeps final authority, and nothing was submitted.</p><ScenarioMatchPanel match={draft.scenario_match} />{draft.review_reasons?.length > 0 && <p className="review-warning">Review flags: {operatorLabels(draft.review_reasons).join(', ')}</p>}<div className="human-review"><label className="checkbox-label"><input type="checkbox" checked={reviewChecked} disabled={Boolean(busy) || Boolean(receipt) || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW'} onChange={(event) => setReviewChecked(event.target.checked)} /><span>I reviewed the evidence and timeline and confirm this review is recorded only in the local demo.</span></label><Button data-testid="dispute-approve" tone={receipt ? 'secondary' : 'blue'} icon="check" onClick={approve} disabled={disabled || !reviewChecked || !draft.draft_digest || Boolean(receipt) || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW'} loading={busy === 'approve'}>{receipt ? 'Local review recorded' : 'Confirm local draft review'}</Button></div>{receipt && <div className="receipt" data-testid="dispute-result"><Icon name="check" /><span>Local draft reviewed · {operatorLabel(receipt.reviewer)} · {dateLabel(receipt.reviewed_at)} · {operatorLabel(receipt.retention)} · {operatorLabel(receipt.external_submission || 'FROZEN')}</span></div>}</> : <div className="evidence-placeholder"><div className="placeholder-nodes"><span><Icon name="layers" /></span><i /><span><Icon name="lock" /></span><i /><span><Icon name="check" /></span></div><h3>Evidence → Pseudonymization → Review</h3><p>Generate a review draft, then confirm the same evidence and timeline before recording the local review.<br />Real carrier, payment, and case verification still require official sources.</p></div>}</div></div>
        <ReferencePanel theme="dispute_mediation" {...referenceProps} open={openSecondary.dispute_mediation === 'reference'} onToggle={(nextOpen) => toggleSecondary('dispute_mediation', 'reference', nextOpen)} />
        <PolicyPanel theme="dispute_mediation" {...referenceProps} open={openSecondary.dispute_mediation === 'policy'} onToggle={(nextOpen) => toggleSecondary('dispute_mediation', 'policy', nextOpen)} />
        <AiBriefPanel stage="dispute_mediation" available={Boolean(draft) && caseItem?.reason === 'INR' && draft?.evidence?.reason === 'INR' && draft?.routing?.overall_state === 'READY_FOR_LOCAL_REVIEW' && !draft?.review_reasons?.includes('unsupported_reason') && !disabled && !busy && !aiBusyStage} brief={aiBriefs.dispute_mediation} loading={aiBusyStage === 'dispute_mediation'} onGenerate={generateAiBrief} />
      </StageAccordion>

      <OptionalDisclosure id="analytics" title="Merchant Evidence Buffer" subtitle="Optional AG Grid Community review workspace" icon="layers" badge={<Badge tone="blue">AG GRID COMMUNITY</Badge>} open={analyticsExpanded} onToggle={setAnalyticsExpanded} testId="optional-toggle-analytics">{analyticsOpen ? <Suspense fallback={<div className="analytics-loading" role="status"><span className="spinner" />Loading the isolated analytics workspace.</div>}><AnalyticsDashboard aup={aup} state={state} /></Suspense> : <div className="analytics-launch-card"><div className="analytics-launch-copy"><span className="meta-label">OPTIONAL SPONSOR EXPERIENCE</span><strong>Open the PayGuard evidence buffer</strong><p>Explore an AG Grid Community evidence table, quick filtering, first-party lifecycle widgets, and a bounded local dashboard guide.</p><div className="analytics-launch-tags"><span>AG Grid Community</span><span>Backend-owned workflow state</span><span>Quick filtering</span><span>Human review</span></div></div><Button data-testid="analytics-launch" icon="layers" tone="blue" disabled={!state} onClick={() => setAnalyticsOpen(true)}>Launch analytics</Button></div>}</OptionalDisclosure>

      <OptionalDisclosure id="activity" title="Session activity" subtitle={`${state?.activity?.length || 0} local events · maximum 30`} icon="clock" open={activityExpanded} onToggle={setActivityExpanded} testId="optional-toggle-activity"><section className="activity-panel" aria-label="Demo activity log"><ol>{state?.activity?.length ? state.activity.slice().reverse().map((event) => <li key={event.id}><span className="activity-dot" /><time>{dateLabel(event.at)}</time><strong>{event.label}</strong><Badge tone="muted">{event.source}</Badge></li>) : <li className="activity-empty">No activity yet. Demo actions will appear here.</li>}</ol></section></OptionalDisclosure>
      <footer><span><Icon name="shield" size={15} /> PayGuard AI <span className="footer-divider">/</span> Local prototype</span><span>Synthetic data · deterministic advisory · human review · external actions restricted</span></footer>
    </main>
    {warningOpen && <div className="aup-warning-backdrop"><div ref={warningRef} className="aup-warning-dialog" role="dialog" aria-modal="true" aria-labelledby="aup-warning-title" aria-describedby="aup-warning-copy" data-testid="aup-warning-dialog" onKeyDown={warningKeys} tabIndex={-1}>
      <Badge tone="amber">Second reminder · REVIEW_SIGNAL</Badge>
      <h2 id="aup-warning-title">Review the actual goods or activity before continuing</h2>
      <p id="aup-warning-copy">The description matched a demo rule. This is a reminder only. Review the official policy; after acknowledging the reminder, you may continue the ordinary Sandbox draft-review flow.</p>
      <p>Acknowledgement is not compliance certification, PayPal policy review, or invoice send. Description changes require a new check.</p>
      <a data-testid="aup-warning-policy-link" href={AUP_POLICY_URL} target="_blank" rel="noopener noreferrer">Review the PayPal US Acceptable Use Policy</a>
      <div className="aup-warning-actions">
        <Button data-testid="aup-return-to-edit" disabled={Boolean(busy)} onClick={() => chooseWarning('RETURN_TO_EDIT')}>Return to edit</Button>
        <Button data-testid="aup-cancel" disabled={Boolean(busy)} onClick={() => chooseWarning('CANCEL')}>Cancel flow</Button>
        <Button data-testid="aup-acknowledge" tone="blue" loading={busy === 'aup-choice'} disabled={Boolean(busy)} onClick={() => chooseWarning('ACKNOWLEDGE_AND_CONTINUE')}>Acknowledge and continue</Button>
      </div>
    </div></div>}
  </div>;
}

function ScenarioMatchPanel({ match }) {
  const scenario = match?.scenario;
  if (!scenario) return null;
  return <details className="scenario-match" data-testid="dispute-scenario-match"><summary><Icon name="link" size={15} /><span>Bound synthetic scenario</span><Badge tone="muted">{scenario.citations.length} pinned citations</Badge></summary><div className="scenario-match-body"><div className="scenario-match-heading"><div><span className="meta-label">DETERMINISTIC CASE MATCH</span><strong>{scenario.title}</strong></div><Badge tone="amber">HUMAN REVIEW REQUIRED</Badge></div><ul>{scenario.citations.map((citation) => <li key={citation.chunk_id}><a href={citation.url} target="_blank" rel="noopener noreferrer">{citation.title}</a><span>{citation.locator}</span><code>{citation.chunk_id}</code></li>)}</ul><p>{operatorLabel(match.provenance)} · {operatorLabel(match.current_policy_applicability)} · {operatorLabel(match.operational_authority)}</p></div></details>;
}

function Metric({ label, value, unit, icon, detail, alert = false, compact = false, statusTone = 'neutral', testId }) {
  return <div data-testid={testId} className={`metric ${alert ? 'metric-alert' : ''} ${compact ? `metric-status metric-status-${statusTone}` : ''}`}><div className="metric-top"><span>{label}</span><Icon name={icon} /></div><div className={`metric-value ${compact ? 'metric-compact' : ''}`}><strong>{value}</strong>{unit && <span>{unit}</span>}</div><small>{detail}</small></div>;
}
