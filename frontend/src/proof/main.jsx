// Public proof page (/proof.html, optimise r24). A static page built only from committed JSON in this repository: what
// was shown for each scenario, how (real PayPal Sandbox call, recorded real run, automated test or synthetic data),
// when, and the file it comes from. It calls nothing: no fetch, no API, no session. Not linked from other pages yet.
import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import facts from '../data/proof_facts_v1.json';
import receipts from '../data/channel3_receipts_v1.json';
import { HISTORY_CUTOFF, LATEST_ALSO, LATEST_DATE, LATEST_ROWS, METHOD_ORDER, REFUSED_LABEL, channel3Summary, dateLabel, groupProof, methodCounts, refusedCount, splitHistory, PROOF_SPONSORS, PROOF_METHOD_CHIPS, emptyProofNote, parseProofHash, proofHash, resolveProofFilter, rowMatches } from './proofData.js';
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
  return <details className="proof-history" data-testid="recorded-send-fold"><summary>The recorded send of 2026-11-04 17:16 UTC (2026-11-05 in UTC+8), step by step (history)</summary><section className="proof-recorded" aria-labelledby="proof-recorded-title" data-testid="recorded-send">
    <h2 id="proof-recorded-title">{send.title}</h2>
    <p className="proof-recorded-intro">{send.intro} <span className="proof-chip proof-chip-info" data-testid="recorded-send-label"><Icon name="recorded" size={14} />Recorded, not live</span></p>
    <ol className="proof-recorded-steps">{send.steps.map((step) => <li key={step.at} data-testid="recorded-send-step">
      <span className="proof-recorded-at">{step.at}</span><span className="proof-recorded-what">{step.what}</span>
    </li>)}</ol>
    <p className="proof-recorded-file" data-testid="recorded-send-file">{send.file_note}</p>
    <p className="proof-recorded-limit">{send.limit}</p>
    <p className="proof-recorded-source">Source: <code>{send.receipt}</code> and <code>{send.file_source}</code>, masked as committed.</p>
  </section></details>;
}

// Three lines at the top: the newest evidence, each pointing at its row below.
function Latest() {
  const byId = new Map(facts.rows.map((row) => [row.id, row]));
  const also = LATEST_ALSO.filter(([id]) => byId.has(id));
  return <section className="proof-latest" aria-labelledby="proof-latest-title" data-testid="proof-latest">
    <h2 id="proof-latest-title">Latest evidence ({LATEST_DATE})</h2>
    <ul>
      {LATEST_ROWS.filter((id) => byId.has(id)).map((id) => <li key={id}>{byId.get(id).proven} <a href={`#row-${id}`}>See the row</a></li>)}
      <li>Also run on {HISTORY_CUTOFF}: {also.map(([id, label], index) => <span key={id}>{index > 0 && (index === also.length - 1 ? ' and ' : ', ')}<a href={`#row-${id}`}>{label}</a></span>)}.</li>
    </ul>
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
  return <li className="proof-row" id={`row-${row.id}`} data-testid="proof-row" data-row-id={row.id} data-method={row.method}>
    <div className="proof-row-head"><MethodChip method={row.method} />{row.refused && <span className="proof-chip proof-chip-muted" data-testid="proof-refused">{REFUSED_LABEL}</span>}<time dateTime={row.date}>{dateLabel(row)}</time></div>
    <p className="proof-proven">{row.proven}</p>
    <dl className="proof-meta">
      <div><dt>How</dt><dd>{row.how}</dd></div>
      <div><dt>Source</dt><dd><code data-testid="proof-source">{row.source}</code></dd></div>
    </dl>
  </li>;
}


// Filter chips (2026-11-09): by how it was shown and by sponsor tool. Hides rows only; "Latest evidence" stays. The state is
// kept in the URL hash (#sponsor=Bryntum) so a judge can link to a view. Pure page state: no request.
function ProofFilters({ filter, setFilter, shown, total }) {
  // Live counts: each chip says how many rows it would show with the other filter kept.
  const countFor = (next) => facts.rows.filter((row) => rowMatches(row, next)).length;
  const active = filter.method !== 'ALL' || filter.sponsor !== '';
  const pick = (change) => resolveProofFilter(facts.rows, filter, change);
  const note = shown === 0 ? emptyProofNote(facts.rows, filter) : '';
  return <section className="proof-filters" aria-labelledby="proof-filters-title" data-testid="proof-filters">
    <h2 id="proof-filters-title">Filter the rows</h2>
    <div className="proof-chip-row" role="group" aria-label="How it was shown" data-testid="proof-method-chips">
      {PROOF_METHOD_CHIPS.map(([value, label]) => <button key={value} type="button" className="proof-filter-chip" aria-pressed={filter.method === value} data-testid={`proof-filter-${value}`} onClick={() => setFilter(pick({ method: value }))}>{label} <span className="proof-chip-count">{countFor(pick({ method: value }))}</span></button>)}
    </div>
    <div className="proof-chip-row" role="group" aria-label="Sponsor tool" data-testid="proof-sponsor-chips">
      {PROOF_SPONSORS.filter((name) => filter.sponsor === name || facts.rows.some((row) => row.sponsors?.includes(name))).map((name) => <button key={name} type="button" className="proof-filter-chip" aria-pressed={filter.sponsor === name} data-testid={`proof-sponsor-${name.replace(/\s+/gu, '-')}`} onClick={() => setFilter(filter.sponsor === name ? { ...filter, sponsor: '' } : pick({ sponsor: name }))}>{name} <span className="proof-chip-count">{countFor(pick({ sponsor: name }))}</span></button>)}
    </div>
    <button type="button" className="proof-filter-chip proof-filter-reset" data-testid="proof-filter-reset" disabled={!active} onClick={() => setFilter({ method: 'ALL', sponsor: '' })}>Reset</button>
    <p className="proof-filter-count" role="status" aria-live="polite" data-testid="proof-filter-count">Showing {shown} of {total}{note ? `. ${note}` : ''}</p>
  </section>;
}

function ProofPage() {
  const [filter, setFilterState] = useState(() => parseProofHash(window.location.hash));
  const setFilter = (next) => { setFilterState(next); window.history.replaceState(null, '', `${window.location.pathname}${window.location.search}${proofHash(next)}`); };
  useEffect(() => {
    // A link to a view (#sponsor=...) or to a row (#row-...) from anywhere on the page. A row anchor clears the filters so the row exists, then scrolls to it.
    const onHash = () => {
      setFilterState(parseProofHash(window.location.hash));
      if (window.location.hash.startsWith('#row-')) window.requestAnimationFrame(() => document.getElementById(window.location.hash.slice(1))?.scrollIntoView());
    };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);
  const sections = groupProof(facts).map((section) => ({ ...section, rows: section.rows.filter((row) => rowMatches(row, filter)) })).filter((section) => section.rows.length > 0 || (!filter.sponsor && filter.method === 'ALL'));
  const shownCount = sections.reduce((sum, section) => sum + section.rows.length, 0);
  const channel3 = channel3Summary(receipts);
  return <div className="proof-shell">
    <a className="proof-skip" href="#proof-main">Skip to the proof</a>
    <header className="proof-band"><div className="proof-band-inner"><strong>TradeGlot</strong><span>Proof</span></div></header>
    <main id="proof-main" className="proof-main" tabIndex={-1}>
      <div className="proof-intro">
        <h1>What has been shown, and how</h1>
        <p>Each row says what was proven, whether it came from a real PayPal Sandbox call, a recorded run, an automated test or synthetic data, when, and the committed file it comes from. This page is static: it calls nothing and reads only files in the repository.</p>
        <p>Short codes such as b017f5d are commits, kept so each claim can be traced. Most open in this repository on GitHub; two older ones (653111a, 7e49835) come from the earlier development history and do not open here.</p>
        <p className="proof-note">Identifiers are masked as in the receipts. Sandbox rows are test data the author created with two Sandbox test accounts, not a real merchant case. TradeGlot was called PayGuard AI until 2026-11-09, so the receipt files and recordings dated before then carry the old name.</p>
      </div>
      <Latest />
      <Legend />
      <ProofFilters filter={filter} setFilter={setFilter} shown={shownCount} total={facts.rows.length} />
      {(!filter.sponsor || filter.sponsor === 'PayPal') && (filter.method === 'ALL' || filter.method === 'REAL_SANDBOX') && <RecordedSend />}
      {sections.map((section) => <section key={section.id} className="proof-section" aria-labelledby={`proof-${section.id}`} data-testid="proof-section" data-scenario={section.id}>
        <h2 id={`proof-${section.id}`}>{section.number && <span className="proof-number">{section.number}</span>}{section.label}</h2>
        {(() => {
          const { current, history } = splitHistory(section.rows);
          return <>
            <ul className="proof-rows">{current.map((row) => <ProofRow key={row.id} row={row} />)}</ul>
            {history.length > 0 && <details className="proof-history" data-testid="proof-history"><summary>Earlier runs (history) · {history.length} row{history.length === 1 ? '' : 's'}</summary>
              <ul className="proof-rows">{history.map((row) => <ProofRow key={row.id} row={row} />)}</ul></details>}
          </>;
        })()}
      </section>)}
      <footer className="proof-foot" data-testid="proof-foot">
        <p>Channel3 receipts on this page: {channel3.count} searches on {channel3.dates.join(', ')}, latency {channel3.minLatency} to {channel3.maxLatency} s, recomputed from <code>frontend/src/data/channel3_receipts_v1.json</code>.</p>
        <p>{facts.source_note}</p>
        <a className="proof-download-demo" href="https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip" target="_blank" rel="noopener noreferrer" title="Same demo, one command, no keys." aria-label="Download the demo (11 MB). Same demo, one command, no keys." data-testid="proof-download-demo"><svg className="download-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 4v10.5" /><path d="m7.5 10.5 4.5 4.5 4.5-4.5" /><path d="M5 19.25h14" /></svg><span>Download the demo (11 MB)</span></a>
      </footer>
    </main>
  </div>;
}

createRoot(document.getElementById('root')).render(<StrictMode><ProofPage /></StrictMode>);
