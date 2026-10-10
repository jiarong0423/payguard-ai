import { useMemo, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { themeQuartz } from 'ag-grid-community';
import './AnalyticsDashboard.css';

const analyticsGridTheme = themeQuartz.withParams({
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

function statusTone(status) {
  if (status === 'Advisory review' || status === 'Needs evidence') return 'amber';
  if (status === 'Ready for human review' || status === 'Review recorded') return 'green';
  return 'muted';
}

function utcDateTime(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return `${date.toLocaleString('en-US', {
    month: '2-digit', day: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false, timeZone: 'UTC',
  })} UTC`;
}

function LifecycleWidget({ stages }) {
  return <section className="analytics-card analytics-lifecycle" data-testid="analytics-lifecycle-widget">
    <div className="analytics-card-header">
      <div><span>MERCHANT EVIDENCE BUFFER</span><strong>Three-stage review path</strong></div>
      <em>Advisory only</em>
    </div>
    <div className="analytics-stage-track">
      {stages.map((stage, index) => <div className="analytics-stage" key={stage.id}>
        <div className="analytics-stage-index">0{index + 1}</div>
        <div className="analytics-stage-copy"><span>{stage.phase}</span><strong>{stage.label}</strong><small>{stage.detail}</small></div>
        <span className={`analytics-status analytics-status-${statusTone(stage.status)}`}>{stage.status}</span>
        {index < stages.length - 1 && <span className="analytics-stage-line" aria-hidden="true" />}
      </div>)}
    </div>
  </section>;
}

function AuthorityWidget({ boundaries }) {
  return <section className="analytics-card analytics-authority" data-testid="analytics-authority-widget">
    <div className="analytics-card-header">
      <div><span>AUTHORITY MAP</span><strong>Who decides what</strong></div>
      <em>Human controlled</em>
    </div>
    <ul>{boundaries.map((item) => <li key={item.label}><span>{item.label}</span><strong>{item.authority}</strong></li>)}</ul>
    <p>No analytics action can send an invoice, move money, submit evidence, or decide a PayPal outcome.</p>
  </section>;
}

function EvidencePulseWidget({ evidenceCounts }) {
  const maximum = Math.max(1, ...evidenceCounts.map((item) => item.value));

  return <section className="analytics-card analytics-pulse" data-testid="analytics-evidence-pulse-widget">
    <div className="analytics-card-header">
      <div><span>VISIBLE EVIDENCE PULSE</span><strong>Session item counts</strong></div>
      <em>Not a risk score</em>
    </div>
    <div className="analytics-pulse-list">
      {evidenceCounts.map((item) => {
        const percentage = item.value ? Math.max(6, (item.value / maximum) * 100) : 0;
        return <div className="analytics-pulse-row" key={item.id}>
          <div><span>{item.label}</span><strong>{item.value}</strong></div>
          <div className="analytics-pulse-track" role="progressbar" aria-label={item.label} aria-valuemin="0" aria-valuemax={maximum} aria-valuenow={item.value}>
            <span style={{ width: `${percentage}%` }} />
          </div>
        </div>;
      })}
    </div>
    <p>Counts describe visible synthetic session items only. They do not rank merchants or predict PayPal action.</p>
  </section>;
}

function MobileAccordionSection({ activeSection, badge, children, eyebrow, id, onActivate, title }) {
  const expanded = activeSection === id;
  const buttonId = `mobile-accordion-${id}`;
  const panelId = `mobile-section-${id}`;

  return <section className="analytics-mobile-section" aria-labelledby={buttonId}>
    <button
      type="button"
      className="analytics-mobile-trigger"
      data-testid={`analytics-mobile-trigger-${id}`}
      id={buttonId}
      aria-controls={panelId}
      aria-expanded={expanded}
      onClick={() => onActivate(id)}
    >
      <span className="analytics-mobile-copy"><span>{eyebrow}</span><strong>{title}</strong></span>
      <span className="analytics-mobile-meta"><em>{badge}</em><span className="analytics-mobile-chevron" aria-hidden="true" /></span>
    </button>
    <div className="analytics-mobile-content" id={panelId} role="region" aria-labelledby={buttonId} hidden={!expanded}>
      {children}
    </div>
  </section>;
}

function MobileAnalyticsSummary({ boundaries, evidenceCounts, stages, transactions }) {
  const [activeSection, setActiveSection] = useState('lifecycle');

  return <div className="analytics-mobile-summary" data-testid="analytics-mobile-summary">
    <div className="analytics-mobile-notice">
      <span>RESPONSIVE REVIEW MODE</span>
      <strong>Evidence overview</strong>
      <p>The full AG Grid analytics workspace is available on desktop. This mobile view keeps the complete review story readable without horizontal scrolling.</p>
    </div>

    <MobileAccordionSection activeSection={activeSection} badge="Advisory only" eyebrow="MERCHANT EVIDENCE LIFECYCLE" id="lifecycle" onActivate={setActiveSection} title="Three-stage evidence funnel">
      <div className="analytics-mobile-stage-list">
        {stages.map((stage, index) => <article className="analytics-mobile-stage" key={stage.id}>
          <div className="analytics-mobile-stage-number">0{index + 1}</div>
          <div><span>{stage.phase}</span><strong>{stage.label}</strong><p>{stage.detail}</p></div>
          <span className={`analytics-status analytics-status-${statusTone(stage.status)}`}>{stage.status}</span>
        </article>)}
      </div>
    </MobileAccordionSection>

    <MobileAccordionSection activeSection={activeSection} badge="Not a risk score" eyebrow="VISIBLE EVIDENCE PULSE" id="pulse" onActivate={setActiveSection} title="Session item counts">
      <div className="analytics-mobile-metrics">
        {evidenceCounts.map((item) => <div key={item.id}><strong>{item.value}</strong><span>{item.label}</span></div>)}
      </div>
    </MobileAccordionSection>

    <MobileAccordionSection activeSection={activeSection} badge={`${transactions.length} total`} eyebrow="TRANSACTION TABLE" id="stream" onActivate={setActiveSection} title="Recent synthetic transactions">
      {transactions.length ? <div className="analytics-mobile-transactions">
        {transactions.slice(0, 3).map((transaction) => <article key={transaction.order_id}>
          <div><span>Order</span><strong>{transaction.order_id}</strong></div>
          <div><span>Amount</span><strong>{Number(transaction.amount).toFixed(2)} {transaction.currency}</strong></div>
          <div><span>Captured at</span><strong>{utcDateTime(transaction.occurred_at)}</strong></div>
        </article>)}
      </div> : <p className="analytics-mobile-empty">Select Load sales burst to view the transaction table.</p>}
    </MobileAccordionSection>

    <MobileAccordionSection activeSection={activeSection} badge="Human controlled" eyebrow="AUTHORITY MAP" id="authority" onActivate={setActiveSection} title="Who decides what">
      <ul className="analytics-mobile-authority">{boundaries.map((item) => <li key={item.label}><span>{item.label}</span><strong>{item.authority}</strong></li>)}</ul>
      <p className="analytics-mobile-boundary">No analytics action can send an invoice, move money, submit evidence, or decide a PayPal outcome.</p>
    </MobileAccordionSection>
  </div>;
}

function responseFor(prompt, snapshot) {
  const normalized = prompt.toLowerCase();
  const attention = snapshot.stages.filter((stage) => ['Advisory review', 'Needs evidence'].includes(stage.status));
  if (normalized.includes('authority') || normalized.includes('decide')) {
    return 'Authority boundary: PayGuard prepares local advisory evidence. The merchant controls local review actions. PayPal retains PayPal policy and internal dispute authority, while a bank or card issuer retains external dispute authority.';
  }
  if (normalized.includes('attention') || normalized.includes('review')) {
    const labels = attention.length ? attention.map((stage) => stage.label).join(', ') : 'no stage currently shows a review signal';
    return `Current synthetic dashboard review: ${labels}. This is a presentation summary of backend state, not a fraud, compliance, limitation, or dispute decision.`;
  }
  return `Dashboard snapshot: ${snapshot.transactionCount} synthetic transactions, ${snapshot.disputeCount} synthetic disputes, and ${snapshot.aupFindingCount} AUP review findings are visible. This deterministic summary uses only the current in-memory session.`;
}

export default function AnalyticsDashboard({ aup, state }) {
  const [mode, setMode] = useState('view');
  const [guideResponse, setGuideResponse] = useState('Select a bounded prompt to explain the current synthetic dashboard.');
  const [quickFilter, setQuickFilter] = useState('');
  const transactionCount = state?.transactions?.length || 0;
  const disputeCount = state?.disputes?.length || 0;
  const aupFindingCount = aup?.findings?.length || 0;
  const velocity = state?.velocity;
  const transactions = state?.transactions || [];
  const disputeStatuses = state?.disputes?.map((item) => item.status) || [];
  const disputeStatus = disputeStatuses.includes('needs_review')
    ? 'Needs evidence'
    : disputeStatuses.includes('draft_ready')
      ? 'Ready for human review'
      : disputeStatuses.length && disputeStatuses.every((status) => status === 'local_draft_reviewed')
        ? 'Review recorded'
        : 'Awaiting case';

  const stages = useMemo(() => [
    {
      id: 'aup', phase: 'PRE-TRANSACTION', label: 'AUP preflight screen',
      status: !aup ? 'Awaiting review' : aup.match_status === 'REVIEW_SIGNAL' ? 'Advisory review' : 'No demo match',
      detail: !aup ? 'Run the deterministic description check.' : `${aupFindingCount} configured review signal${aupFindingCount === 1 ? '' : 's'} visible.`,
    },
    {
      id: 'velocity', phase: 'FULFILLMENT', label: 'Velocity evidence readiness',
      status: velocity?.alert ? 'Needs evidence' : velocity?.transaction_count > 0 ? 'No review signal' : 'No in-window data',
      detail: velocity ? `${velocity.transaction_count} captures across the ${velocity.window_hours}-hour synthetic window.` : 'Waiting for backend state.',
    },
    {
      id: 'dispute', phase: 'POST-TRANSACTION', label: 'Dispute evidence mediation',
      status: disputeStatus,
      detail: disputeCount ? `${disputeCount} synthetic case${disputeCount === 1 ? '' : 's'}; status comes from the case workflow.` : 'Load dispute case to open the evidence workspace.',
    },
  ], [aup, aupFindingCount, disputeCount, disputeStatus, velocity]);

  const boundaries = useMemo(() => [
    { label: 'Policy reminder', authority: 'Merchant review, PayPal final authority' },
    { label: 'Velocity signal', authority: 'Merchant evidence preparation' },
    { label: 'Dispute packet', authority: 'Human confirmation before any external process' },
  ], []);

  const evidenceCounts = useMemo(() => [
    { id: 'aup', label: 'AUP findings', value: aupFindingCount },
    { id: 'transactions', label: 'Transactions', value: transactionCount },
    { id: 'disputes', label: 'Disputes', value: disputeCount },
  ], [aupFindingCount, disputeCount, transactionCount]);

  const snapshot = useMemo(() => ({ aupFindingCount, disputeCount, stages, transactionCount }), [aupFindingCount, disputeCount, stages, transactionCount]);
  const rowData = useMemo(() => transactions, [transactions]);
  const columnDefs = useMemo(() => [
    { field: 'order_id', headerName: 'Order', minWidth: 150, flex: 1.3 },
    { field: 'amount', headerName: 'Amount', minWidth: 110, valueFormatter: ({ value }) => Number(value).toFixed(2) },
    { field: 'currency', headerName: 'Currency', minWidth: 100 },
    { field: 'occurred_at', headerName: 'Captured at', minWidth: 220, flex: 1.2, valueFormatter: ({ value }) => utcDateTime(value) },
  ], []);

  const prompts = [
    { id: 'attention', label: 'What needs attention?', prompt: 'Which stages need human attention in this synthetic dashboard?' },
    { id: 'authority', label: 'Explain authority', prompt: 'Explain who has authority to decide each outcome.' },
    { id: 'snapshot', label: 'Summarize snapshot', prompt: 'Summarize the current synthetic dashboard snapshot.' },
  ];

  return <div className={`analytics-feature analytics-feature-${mode}`} data-testid="community-analytics-dashboard">
    <div className="analytics-toolbar">
      <div>
        <span>REVIEW ANALYTICS</span>
        <strong>Merchant Evidence Buffer</strong>
        <small>Review AUP signals, fulfillment readiness, and dispute preparation in one workspace.</small>
      </div>
      <div className="analytics-mode-switch" role="group" aria-label="Analytics layout">
        <button type="button" aria-pressed={mode === 'view'} className={mode === 'view' ? 'active' : ''} onClick={() => setMode('view')}>Review overview</button>
        <button type="button" aria-pressed={mode === 'inspect'} className={mode === 'inspect' ? 'active' : ''} onClick={() => setMode('inspect')}>Transaction table</button>
      </div>
    </div>
    <div className="analytics-rights-note" role="note">
      <strong>AG Grid Community</strong>
      <span>Built with AG Grid Community and first-party React components. Synthetic session data only.</span>
    </div>

    <MobileAnalyticsSummary boundaries={boundaries} evidenceCounts={evidenceCounts} stages={stages} transactions={transactions} />

    <div className="analytics-desktop-workspace" data-testid="analytics-desktop-workspace">
      <LifecycleWidget stages={stages} />
      <AuthorityWidget boundaries={boundaries} />
      <EvidencePulseWidget evidenceCounts={evidenceCounts} />

      <section className="analytics-card analytics-grid-widget" data-testid="analytics-grid-widget">
        <div className="analytics-card-header">
          <div><span>TRANSACTION REVIEW</span><strong>Synthetic transaction table</strong></div>
          <em>AG Grid Community · {transactions.length} rows</em>
        </div>
        <div className="analytics-grid-tools">
          <label htmlFor="analytics-grid-filter">Filter visible rows</label>
          <input id="analytics-grid-filter" type="search" value={quickFilter} onChange={(event) => setQuickFilter(event.target.value)} placeholder="Order or currency" />
        </div>
        <div className="analytics-grid-frame" aria-label="AG Grid Community synthetic transaction analytics">
          <AgGridReact
            theme={analyticsGridTheme}
            rowData={rowData}
            columnDefs={columnDefs}
            defaultColDef={{ filter: true, resizable: true, sortable: true }}
            getRowId={({ data }) => data.order_id}
            headerHeight={42}
            rowHeight={42}
            quickFilterText={quickFilter}
            overlayNoRowsTemplate="Select Load sales burst to view transactions"
          />
        </div>
      </section>

      <section className="analytics-card analytics-guide" data-testid="analytics-guide-widget">
        <div className="analytics-card-header">
          <div><span>BOUNDED DASHBOARD GUIDE</span><strong>Explain the visible session</strong></div>
          <em>Read only</em>
        </div>
        <div className="analytics-guide-prompts">
          {prompts.map((item) => <button key={item.id} type="button" onClick={() => setGuideResponse(responseFor(item.prompt, snapshot))}>{item.label}</button>)}
        </div>
        <p className="analytics-guide-response" role="status" aria-live="polite">{guideResponse}</p>
        <small>This deterministic guide reads the same in-memory values shown above. It does not call a model or change workflow state.</small>
      </section>
    </div>

    <div className="analytics-footer">
      <span>Grid: AG Grid Community</span>
      <span>Session storage: temporary</span>
      <span>Review actions: local only</span>
    </div>
  </div>;
}
