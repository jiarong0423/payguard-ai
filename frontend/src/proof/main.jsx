// Public proof page (/proof.html, optimise r24). A static page built only from committed JSON in this repository: what
// was shown for each scenario, how (real PayPal Sandbox call, recorded real run, automated test or synthetic data),
// when, and the file it comes from. It calls nothing: no fetch, no API, no session. Not linked from other pages yet.
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import facts from '../data/proof_facts_v1.json';
import receipts from '../data/channel3_receipts_v1.json';
import { METHOD_ORDER, REFUSED_LABEL, channel3Summary, dateLabel, groupProof, methodCounts, refusedCount } from './proofData.js';
import './proof.css';

const ICONS = {
  sandbox: <><path d="M12 3.25 4.75 6.25v5.5c0 4.85 3.1 7.95 7.25 9 4.15-1.05 7.25-4.15 7.25-9v-5.5L12 3.25Z" /><path d="m9 12.25 2.1 2.1 4.15-4.35" /></>,
  recorded: <><rect x="4.75" y="4.75" width="14.5" height="14.5" rx="2" /><path d="M8.5 9h7M8.5 12h7M8.5 15h4" /></>,
  test: <><path d="M9.5 4.75v5.5L5 18a1.5 1.5 0 0 0 1.3 2.25h11.4A1.5 1.5 0 0 0 19 18l-4.5-7.75v-5.5" /><path d="M8.5 4.75h7" /></>,
  synthetic: <><circle cx="12" cy="12" r="7.25" strokeDasharray="3 3" /><path d="M12 8.5v7M8.5 12h7" /></>,
};
const METHOD_STYLE = {
  REAL_SANDBOX: { icon: 'sandbox', tone: 'ok' },
  RECORDED: { icon: 'recorded', tone: 'info' },
  TEST: { icon: 'test', tone: 'watch' },
  SYNTHETIC: { icon: 'synthetic', tone: 'muted' },
};

function Icon({ name, size = 16 }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{ICONS[name]}</svg>;
}

function MethodChip({ method }) {
  const style = METHOD_STYLE[method] || METHOD_STYLE.SYNTHETIC;
  const meta = facts.methods[method];
  return <span className={`proof-chip proof-chip-${style.tone}`} data-testid="proof-method" data-method={method}>
    <Icon name={style.icon} size={14} />{meta?.label ?? method}<span className="proof-chip-kind">{meta?.simulated ? 'simulated' : 'real'}</span>
  </span>;
}

// The 2026-11-05 send as the committed receipt records it. Text only, from proof_facts_v1.json; each step's quote is checked
// against the receipt by tests/frontend_proof_contract.mjs. The page still calls nothing.
function RecordedSend() {
  const send = facts.recorded_send;
  if (!send) return null;
  return <section className="proof-recorded" aria-labelledby="proof-recorded-title" data-testid="recorded-send">
    <h2 id="proof-recorded-title">{send.title}</h2>
    <p className="proof-recorded-intro">{send.intro} <span className="proof-chip proof-chip-info" data-testid="recorded-send-label"><Icon name="recorded" size={14} />Recorded, not live</span></p>
    <ol className="proof-recorded-steps">{send.steps.map((step) => <li key={step.at} data-testid="recorded-send-step">
      <span className="proof-recorded-at">{step.at}</span><span className="proof-recorded-what">{step.what}</span>
    </li>)}</ol>
    <p className="proof-recorded-file" data-testid="recorded-send-file">{send.file_note}</p>
    <p className="proof-recorded-limit">{send.limit}</p>
    <p className="proof-recorded-source">Source: <code>{send.receipt}</code> and <code>{send.file_source}</code>, masked as committed.</p>
  </section>;
}

function Legend() {
  const counts = methodCounts(facts);
  const refused = refusedCount(facts);
  return <section className="proof-legend" aria-labelledby="proof-legend-title" data-testid="proof-legend">
    <h2 id="proof-legend-title">Real vs simulated</h2>
    <dl>{METHOD_ORDER.map((method) => <div key={method} className="proof-legend-item">
      <dt><MethodChip method={method} /> <span className="proof-legend-count">{method === 'REAL_SANDBOX' && refused
        ? `${counts[method] - refused} rows, plus ${refused} ${REFUSED_LABEL}`
        : `${counts[method]} row${counts[method] === 1 ? '' : 's'}`}</span></dt>
      <dd>{facts.methods[method].meaning}</dd>
    </div>)}</dl>
  </section>;
}

function ProofRow({ row }) {
  return <li className="proof-row" data-testid="proof-row" data-row-id={row.id} data-method={row.method}>
    <div className="proof-row-head"><MethodChip method={row.method} />{row.refused && <span className="proof-chip proof-chip-muted" data-testid="proof-refused">{REFUSED_LABEL}</span>}<time dateTime={row.date}>{dateLabel(row)}</time></div>
    <p className="proof-proven">{row.proven}</p>
    <dl className="proof-meta">
      <div><dt>How</dt><dd>{row.how}</dd></div>
      <div><dt>Source</dt><dd><code data-testid="proof-source">{row.source}</code></dd></div>
    </dl>
  </li>;
}

function ProofPage() {
  const sections = groupProof(facts);
  const channel3 = channel3Summary(receipts);
  return <div className="proof-shell">
    <a className="proof-skip" href="#proof-main">Skip to the proof</a>
    <header className="proof-band"><div className="proof-band-inner"><strong>TradeGlot</strong><span>Proof</span></div></header>
    <main id="proof-main" className="proof-main" tabIndex={-1}>
      <div className="proof-intro">
        <h1>What has been shown, and how</h1>
        <p>Each row says what was proven, whether it came from a real PayPal Sandbox call, a recorded run, an automated test or synthetic data, when, and the committed file it comes from. This page is static: it calls nothing and reads only files in the repository.</p>
        <p className="proof-note">Identifiers are masked as in the receipts. Sandbox rows are test data the author created with two Sandbox test accounts, not a real merchant case.</p>
      </div>
      <RecordedSend />
      <Legend />
      {sections.map((section) => <section key={section.id} className="proof-section" aria-labelledby={`proof-${section.id}`} data-testid="proof-section" data-scenario={section.id}>
        <h2 id={`proof-${section.id}`}>{section.number && <span className="proof-number">{section.number}</span>}{section.label}</h2>
        <ul className="proof-rows">{section.rows.map((row) => <ProofRow key={row.id} row={row} />)}</ul>
      </section>)}
      <footer className="proof-foot" data-testid="proof-foot">
        <p>Channel3 receipts on this page: {channel3.count} searches on {channel3.dates.join(', ')}, latency {channel3.minLatency} to {channel3.maxLatency} s, recomputed from <code>frontend/src/data/channel3_receipts_v1.json</code>.</p>
        <p>{facts.source_note}</p>
      </footer>
    </main>
  </div>;
}

createRoot(document.getElementById('root')).render(<StrictMode><ProofPage /></StrictMode>);
