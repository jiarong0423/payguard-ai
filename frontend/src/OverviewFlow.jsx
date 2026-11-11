// (P2 2026-11-12) Overview first screen: the three steps as one seller flow, one real result per step, four figures and
// the recorded send replay. Display only: every value comes from a committed data file (overview_figures_v1.json,
// proof_facts_v1.json), each recounted from its source by tests/frontend_overview_figures.mjs; nothing is requested.
// Loaded on demand, so the console's first-load budget does not carry it.
import { lazy, Suspense } from 'react';
import figures from './data/overview_figures_v1.json';
import facts from './data/proof_facts_v1.json';
import './OverviewFlow.css';

const RecordedSendReplay = lazy(() => import('./RecordedSendReplay.jsx'));

const svg = (paths) => <svg className="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths}</svg>;
const WARNING = svg(<><path d="M10.7 4.2a1.5 1.5 0 0 1 2.6 0l7.45 13.3a1.5 1.5 0 0 1-1.3 2.25H4.55a1.5 1.5 0 0 1-1.3-2.25L10.7 4.2Z" /><path d="M12 9.25v4.25M12 16.75h.01" /></>);
const CHECK = svg(<><circle cx="12" cy="12" r="8.5" /><path d="m8.5 12.25 2.4 2.4 4.6-4.9" /></>);
const ARROW = svg(<><path d="M4.75 12h14.5" /><path d="m13.5 6.25 5.75 5.75-5.75 5.75" /></>);

const row = (id) => facts.rows.find((item) => item.id === id);
// Values quoted in the proof row itself: the send's Debug-Id and the read-back status.
const quoted = (item, pattern) => {
  for (const text of [...(item?.quotes || []), item?.how || '']) {
    const match = text.match(pattern);
    if (match) return match[1];
  }
  return null;
};

function Source({ mark, children }) {
  return <span className="ov-source"><b>{mark}</b><span>{children}</span></span>;
}

export default function OverviewFlow({ onOpen }) {
  const rules = figures.country_rules;
  const example = figures.step1_example;
  const send = figures.step3_send;
  const sendRow = row(send.proof_row);
  const debugId = quoted(sendRow, /PayPal-Debug-Id of the send: (\w+)/u);
  const readBack = quoted(sendRow, /read-back right after showed the status ([A-Za-z ]+?) with/u);
  const sends = [...figures.receipt_sends, ...figures.readback_sends];
  const sendsWithId = sends.filter((item) => item.debug_id).length;
  const sendSources = Object.entries(sends.reduce((files, item) => ({ ...files, [item.file.replace('docs/evidence/', '')]: [...(files[item.file.replace('docs/evidence/', '')] || []), item.line] }), {})).map(([file, lines]) => `${file}:${lines.join('/')}`).join(', ');
  const spike = figures.step2_example;
  const open = (page) => (event) => { event.preventDefault(); onOpen(page); };

  return <div className="ov" data-testid="overview-flow">
    <ol className="ov-flow" aria-label="The seller flow, step by step">
      <li className="ov-step">
        <a className="ov-step__link" href="#compliance" data-testid="overview-step-compliance" onClick={open('compliance')}>
          <span className="ov-step__n">01</span><span className="ov-step__name">Check a sale</span>
          <span className="ov-step__what">Before you ship: {example.route}, {example.goods}</span>
          <span className="tg-stamp tg-stamp--risk ov-step__stamp">{WARNING}Rule match</span>
          <span className="ov-step__result">{example.statute} {example.article} · {example.tier}</span>
          <Source mark="Recounted">{example.source}:{example.line} ({example.rule_id})</Source>
          <span className="ov-step__open">Open step {ARROW}</span>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#velocity" data-testid="overview-step-velocity" onClick={open('velocity')}>
          <span className="ov-step__n">02</span><span className="ov-step__name">Sales spike</span>
          <span className="ov-step__what">When orders jump: which ones need proof of delivery</span>
          <span className="ov-step__figure">×{spike.ratio}</span>
          <span className="ov-step__result">{spike.orders} orders in {spike.window_hours} h · {spike.currency} {spike.total} vs usual {spike.currency} {spike.baseline_per_hour}/h</span>
          <Source mark="Synthetic">{spike.source}:{spike.lines.baseline}, {spike.lines.amounts}, {spike.lines.burst_rows} (the burst this step loads)</Source>
          <span className="ov-step__open">Open step {ARROW}</span>
        </a>
      </li>
      <li className="ov-step ov-step--send">
        <a className="ov-step__link" href="#disputes" data-testid="overview-step-disputes" onClick={open('disputes')}>
          <span className="ov-step__n">03</span><span className="ov-step__name">Disputes</span>
          <span className="ov-step__what">When a buyer disputes: evidence, a person's review, then the send</span>
          <span className="ov-step__badge">Real Sandbox send</span>
          <span className="ov-step__result">{send.case_ref} · {send.amount.currency} {send.amount.value} · {sendRow?.date}</span>
          {debugId && <span className="ov-step__result">PayPal-Debug-Id <span className="tg-mono">{debugId}</span></span>}
          {readBack && <span className="tg-done ov-step__result">{CHECK}Read-back: {readBack}</span>}
          <Source mark="Hosted demo">{send.source}:{send.line} · proof row {send.proof_row}</Source>
          <span className="ov-step__open">Open step {ARROW}</span>
        </a>
      </li>
    </ol>

    <div className="tg-figures ov-figures" role="list" aria-label="Figures, each with its source">
      <div className="tg-figure" role="listitem"><span className="tg-figure__value">{rules.import_rules + rules.export_rules}</span><span className="tg-figure__label">official export and import rules</span>
        <span className="tg-figure__source"><b>Recounted</b><span>{rules.source} ({rules.import_rules} import + {rules.export_rules} export)</span></span></div>
      <div className="tg-figure" role="listitem"><span className="tg-figure__value">{rules.countries}</span><span className="tg-figure__label">countries in the rules check</span>
        <span className="tg-figure__source"><b>Recounted</b><span>{rules.source}</span></span></div>
      <div className="tg-figure" role="listitem"><span className="tg-figure__value">{sends.length}</span><span className="tg-figure__label">real Sandbox evidence sends on file; {sendsWithId} with a PayPal-Debug-Id</span>
        <span className="tg-figure__source"><b>Recorded</b><span>{sendSources}</span></span></div>
      <div className="tg-figure" role="listitem"><span className="tg-figure__value">{facts.rows.length}</span><span className="tg-figure__label">proof rows, each naming its source file</span>
        <span className="tg-figure__source"><b>Recounted</b><span>frontend/src/data/proof_facts_v1.json</span></span></div>
    </div>

    <section className="tg-card tg-card--feature ov-replay" aria-label="Recorded send replay">
      <p className="tg-eyebrow">Step 03 evidence · recorded</p>
      <Suspense fallback={<p className="tg-small" role="status">Loading the recorded replay</p>}><RecordedSendReplay /></Suspense>
    </section>
  </div>;
}
