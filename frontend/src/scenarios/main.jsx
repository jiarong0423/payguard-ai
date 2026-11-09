// Scenario work orders (/scenarios.html), linked from the console top bar. Runs the fixed work orders in
// workOrders.js against this server's own local API; owner steps are checkboxes that never call anything.
import { useCallback, useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { apiRequest } from '../api.js';
import { STATUS, WORK_ORDERS, cardStatus, clearRun, detectMode, openOwnerSteps, receiptLines, restoreRun, runWorkOrder, saveRun } from './workOrders.js';
import '../index.css';
import './scenarios.css';

const ICONS = {
  shield: <><path d="M12 3.25 4.75 6.25v5.5c0 4.85 3.1 7.95 7.25 9 4.15-1.05 7.25-4.15 7.25-9v-5.5L12 3.25Z" /><path d="m9 12.25 2.1 2.1 4.15-4.35" /></>,
  check: <path d="m5.25 12.5 4.25 4.25 9.25-9.5" />,
  cross: <><path d="m7 7 10 10" /><path d="M17 7 7 17" /></>,
  clock: <><circle cx="12" cy="12" r="8.5" /><path d="M12 7.5v4.75l3.25 2" /></>,
  user: <><circle cx="12" cy="8.5" r="3.5" /><path d="M5 19.5c1.2-3.3 3.8-5 7-5s5.8 1.7 7 5" /></>,
  lock: <><rect x="5.5" y="10.5" width="13" height="9" rx="2" /><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5" /></>,
  dot: <circle cx="12" cy="12" r="3.5" />,
  play: <path d="M8 5.5v13l10-6.5-10-6.5Z" />,
  refresh: <><path d="M19.25 12a7.25 7.25 0 1 1-2.12-5.13" /><path d="M19.25 4.75v4.5h-4.5" /></>,
  copy: <><rect x="8.5" y="8.5" width="11" height="11" rx="2" /><path d="M15.5 8.5v-2a2 2 0 0 0-2-2h-7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h2" /></>,
};
function Icon({ name, size = 18 }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{ICONS[name]}</svg>;
}

const CHIP = {
  [STATUS.NOT_RUN]: { label: 'Not run', tone: 'muted', icon: 'dot' },
  [STATUS.RUNNING]: { label: 'Running', tone: 'blue', icon: 'clock' },
  [STATUS.PASSED]: { label: 'Passed', tone: 'green', icon: 'check' },
  [STATUS.FAILED]: { label: 'Failed', tone: 'danger', icon: 'cross' },
  [STATUS.NEEDS_OWNER]: { label: 'Needs owner', tone: 'amber', icon: 'user' },
  [STATUS.LOCAL_ONLY]: { label: 'Local only', tone: 'muted', icon: 'lock' },
};
function Chip({ status, label }) {
  const chip = CHIP[status] || CHIP[STATUS.NOT_RUN];
  return <span className={`badge badge-${chip.tone} scenario-chip`}><Icon name={chip.icon} size={14} />{label || chip.label}</span>;
}

function Button({ tone = 'secondary', icon, children, ...props }) {
  return <button type="button" className={`button button-${tone}`} {...props}>{icon && <Icon name={icon} size={16} />}<span>{children}</span></button>;
}

async function fetchPage(url) {
  return fetch(url, { method: 'GET', credentials: 'omit', cache: 'no-store', redirect: 'error' });
}

// The licence line is drawn by the dashboard itself; read it from a hidden same-origin frame, then remove the frame.
function readLicence() {
  return new Promise((resolve) => {
    const frame = document.createElement('iframe');
    frame.title = 'Dashboard licence check';
    frame.setAttribute('aria-hidden', 'true');
    frame.tabIndex = -1;
    frame.className = 'scenario-probe-frame';
    frame.src = '/dashboard.html';
    let done = false;
    const finish = (value) => { if (done) return; done = true; clearInterval(timer); frame.remove(); resolve(value); };
    const timer = setInterval(() => {
      try {
        const text = frame.contentDocument?.querySelector('[data-testid="dashboard-licence"]')?.textContent || '';
        if (text) finish(/key supplied/i.test(text) ? 'key' : /no key|trial/i.test(text) ? 'trial' : null);
      } catch { finish(null); }
    }, 250);
    setTimeout(() => finish(null), 20000);
    document.body.appendChild(frame);
  });
}

const emptySteps = () => Object.fromEntries(WORK_ORDERS.map((order) => [order.id, {}]));
const emptyRows = () => Object.fromEntries(WORK_ORDERS.map((order) => [order.id, []]));
// This tab's sessionStorage; reading the property itself can throw when site data is blocked (attack r21).
function runStorage() {
  try { return window.sessionStorage; } catch { return null; }
}
// Read once, when the page loads (Back or Forward to it included).
const RESTORED = restoreRun(runStorage());

function modeText(mode) {
  if (!mode) return { label: 'Reading server mode', tone: STATUS.RUNNING };
  if (mode.error) return { label: 'Server mode unknown · guide turns need the owner', tone: STATUS.NEEDS_OWNER };
  if (mode.hosted) return { label: 'Hosted demo · PayPal and Gemini steps are local only', tone: STATUS.LOCAL_ONLY };
  if (mode.rulesOnly) return { label: 'Local console · guide answers from rules only', tone: STATUS.PASSED };
  if (mode.rulesOnly === false) return { label: 'Local console · model mode on, guide turns need the owner', tone: STATUS.NEEDS_OWNER };
  return { label: 'Local console · guide mode unknown, guide turns need the owner', tone: STATUS.NEEDS_OWNER };
}

function ScenariosPage() {
  const [mode, setMode] = useState(null);
  const [steps, setSteps] = useState(() => RESTORED?.steps || emptySteps());
  const [rows, setRows] = useState(() => RESTORED?.rows || emptyRows());
  const [ticked, setTicked] = useState(() => RESTORED?.ticked || Object.fromEntries(WORK_ORDERS.map((order) => [order.id, {}])));
  const [busy, setBusy] = useState(null);
  // Keep the last finished results for Back and Forward (attack r21); nothing is written while a run is going.
  useEffect(() => {
    if (!busy) saveRun(runStorage(), { steps, rows, ticked });
  }, [busy, steps, rows, ticked]);
  const [copied, setCopied] = useState(null);
  const [copyFailed, setCopyFailed] = useState(null);
  const modeRef = useRef(null);

  const readMode = useCallback(async () => {
    try {
      const session = await apiRequest('/demo/sessions', { method: 'POST', body: {} });
      const found = await detectMode(apiRequest, session);
      modeRef.current = found;
    } catch {
      modeRef.current = { hosted: null, rulesOnly: null, error: true };
    }
    setMode(modeRef.current);
    return modeRef.current;
  }, []);
  useEffect(() => { readMode(); }, [readMode]);

  const runOne = useCallback(async (id) => {
    const current = modeRef.current || await readMode();
    setSteps((all) => ({ ...all, [id]: {} }));
    setRows((all) => ({ ...all, [id]: [] }));
    const result = await runWorkOrder(id, {
      request: apiRequest, fetchPage, readLicence, hosted: current?.hosted !== false, // unknown mode runs as hosted (r15)
      onStep: (n, step) => setSteps((all) => ({ ...all, [id]: { ...all[id], [n]: step } })),
    });
    setSteps((all) => ({ ...all, [id]: result.steps }));
    setRows((all) => ({ ...all, [id]: result.rows }));
  }, [readMode]);

  const run = async (ids) => {
    setBusy(ids.length > 1 ? 'all' : ids[0]);
    try { for (const id of ids) await runOne(id); } finally { setBusy(null); }
  };
  const reset = () => {
    clearRun(runStorage());
    setSteps(emptySteps()); setRows(emptyRows()); setCopied(null);
    setTicked(Object.fromEntries(WORK_ORDERS.map((order) => [order.id, {}])));
  };
  const copy = async (id) => {
    try { await navigator.clipboard.writeText(receiptLines(rows[id])); setCopied(id); setCopyFailed(false); } catch { setCopied(null); setCopyFailed(id); }
  };
  const shownMode = modeText(mode);

  return <div className="app-shell scenarios-shell">
    <a className="skip-link" href="#main">Skip to work orders</a>
    <header className="topbar">
      <a className="brand" href="/" aria-label="TradeGlot console"><span className="brand-mark"><Icon name="shield" size={23} /></span><span>TradeGlot<small>MERCHANT EVIDENCE BUFFER</small></span></a>
      <nav aria-label="Additional workspace"><a href="/">Console</a><a href="/dashboard.html" data-testid="topbar-dashboard">Dashboard</a><a href="/scenarios.html" aria-current="page" data-testid="topbar-scenarios">Scenarios</a></nav>
      <div className="environment"><span className="badge badge-blue">{mode?.hosted ? 'HOSTED DEMO' : 'LOCAL DEMO'}</span></div>
    </header>
    <main id="main" className="scenarios-main">
      <section className="scenarios-head">
        <div>
          <span className="meta-label">WORK ORDERS</span>
          <h1>Scenario work orders</h1>
          <p>Each card runs one scene of the demo against this console's own API with synthetic data. Owner steps are ticked by hand; ticking never calls PayPal or a model.</p>
          <p className="scenarios-mode" data-testid="scenario-mode"><Chip status={shownMode.tone} label={shownMode.label} /></p>
        </div>
        <div className="scenarios-actions">
          {/* Each work order opens its own session and the hosted demo shares one session-creation budget across every
              visitor (30 a minute), so Run all there could lock judges out of the console (red team r13 P1). Shown only once the
              page knows it is local: a failed mode read is not proof of local (r14). */}
          {mode?.hosted === false && <Button tone="blue" icon="play" data-testid="scenario-run-all" disabled={Boolean(busy) || !mode} onClick={() => run(WORK_ORDERS.map((order) => order.id))}>{busy === 'all' ? 'Running…' : 'Run all'}</Button>}
          <Button tone="ghost" icon="refresh" data-testid="scenario-reset" disabled={Boolean(busy)} onClick={reset}>Reset</Button>
        </div>
      </section>
      <div className="scenario-grid">
        {WORK_ORDERS.map((order) => {
          const orderSteps = steps[order.id];
          const status = cardStatus(order, orderSteps);
          const open = openOwnerSteps(order, orderSteps, ticked[order.id]);
          return <article key={order.id} className={`scenario-card scenario-${status}`} data-testid={`scenario-card-${order.id}`} aria-labelledby={`${order.id}-title`}>
            <header className="scenario-card-head">
              <div className="scenario-card-title"><span className="scenario-id">{order.id}</span><h2 id={`${order.id}-title`}>{order.title}</h2><small>{order.scene}</small></div>
              <span data-testid={`scenario-status-${order.id}`} aria-live="polite"><Chip status={status} /></span>
            </header>
            <ol className="scenario-steps">
              {order.steps.map((step) => {
                const state = orderSteps[step.n];
                const manual = step.kind === 'manual';
                const localOnly = manual && (mode?.hosted || state?.status === STATUS.LOCAL_ONLY);
                const isTicked = Boolean(ticked[order.id][step.n]);
                const stepStatus = manual ? (localOnly ? STATUS.LOCAL_ONLY : isTicked ? STATUS.PASSED : STATUS.NEEDS_OWNER) : (state?.status || STATUS.NOT_RUN);
                return <li key={step.n} className={`scenario-step${manual ? ' scenario-step-manual' : ''}`} data-testid={`scenario-step-${order.id}-${step.n}`} data-status={stepStatus}>
                  <span className="scenario-step-n" aria-hidden="true">{step.n}</span>
                  <div className="scenario-step-body">
                    {manual
                      ? <label className="scenario-owner"><input type="checkbox" checked={isTicked} disabled={localOnly} onChange={(event) => setTicked((all) => ({ ...all, [order.id]: { ...all[order.id], [step.n]: event.target.checked } }))} /><span><strong>Owner · {step.label}</strong></span></label>
                      : <strong>{step.label}</strong>}
                    <dl>
                      <div><dt>Expected</dt><dd>{step.expect}</dd></div>
                      <div><dt>Actual</dt><dd>{manual ? (localOnly ? `Needs ${step.needs === 'paypal' ? 'the PayPal Sandbox' : 'Gemini'}; run TradeGlot locally.` : isTicked ? 'Ticked by the owner' : 'Owner checks this on camera') : (state?.actual || '—')}</dd></div>
                    </dl>
                    {state?.note && !manual && <small className="scenario-note">{state.note}</small>}
                  </div>
                  <Chip status={stepStatus} label={manual && isTicked && !localOnly ? 'Owner ticked' : undefined} />
                </li>;
              })}
            </ol>
            {open > 0 && status !== STATUS.NOT_RUN && <p className="scenario-open">{open} owner step{open === 1 ? '' : 's'} open</p>}
            <footer className="scenario-card-foot">
              <Button tone="secondary" icon="play" data-testid={`scenario-run-${order.id}`} disabled={Boolean(busy) || !mode} onClick={() => run([order.id])}>{busy === order.id ? 'Running…' : 'Run auto steps'}</Button>
              <details className="scenario-receipt" data-testid={`scenario-receipt-${order.id}`}>
                <summary>Receipt (JSON) · {rows[order.id].length} row{rows[order.id].length === 1 ? '' : 's'}</summary>
                <pre>{rows[order.id].length ? receiptLines(rows[order.id]) : 'No rows yet. Run the auto steps.'}</pre>
                <Button tone="ghost" icon="copy" disabled={!rows[order.id].length} onClick={() => copy(order.id)}>{copied === order.id ? 'Copied' : 'Copy receipt'}</Button>
                <span className="scenario-copy-status" role="status" aria-live="polite" data-testid={`scenario-copy-status-${order.id}`}>{copied === order.id ? 'Copied to the clipboard' : copyFailed === order.id ? 'Copy was blocked by the browser; select the text above instead' : ''}</span>
              </details>
            </footer>
          </article>;
        })}
      </div>
      <footer><span><Icon name="shield" size={15} /> TradeGlot <span className="footer-divider">/</span> Scenario work orders</span><span className="footer-independent" data-testid="footer-independent">TradeGlot is an independent hackathon demo. Not affiliated with or endorsed by PayPal.</span><span>Synthetic data · nothing is sent to PayPal from this page</span></footer>
    </main>
  </div>;
}

createRoot(document.getElementById('root')).render(<ScenariosPage />);
