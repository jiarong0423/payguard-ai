// (P2 2026-11-12) Overview first screen: the three steps as one seller flow, one real result per step, four figures and
// the recorded send replay. Display only: every value comes from a committed data file (overview_figures_v1.json,
// proof_facts_v1.json), each recounted from its source by tests/frontend_overview_figures.mjs; nothing is requested.
// Loaded on demand, so the console's first-load budget does not carry it.
// (C 2026-11-12) Site-wide containers: step cards and figures are .tg-clip (--step / --fact), sources are one-line
// .tg-source with a plain-language origin (full path in the title), a .tg-legend explains the four source labels.
import { lazy, Suspense } from 'react';
import figures from './data/overview_figures_v1.json';
import facts from './data/proof_facts_v1.json';
import './OverviewFlow.css';

const RecordedSendReplay = lazy(() => import('./RecordedSendReplay.jsx'));

// Phosphor regular icons, path data copied from theme/icons/*.svg (MIT, theme/icons/LICENSE).
const icon = (d) => <svg className="tg-icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d={d} /></svg>;
const WARNING = icon('M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z');
const CHECK = icon('M173.66,98.34a8,8,0,0,1,0,11.32l-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35A8,8,0,0,1,173.66,98.34ZM232,128A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128Z');
const ARROW = icon('M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z');

// The four source labels, one plain sentence each (shown once, under the figures).
export const SOURCE_LEGEND = Object.freeze([
  ['Recorded', 'A real run, kept as a file in the repository.'],
  ['Recounted', 'Counted again from its file by a test on every build.'],
  ['Synthetic', 'Made-up demo data from the demo generator.'],
  ['Hosted demo', 'Done on the public hosted demo with a PayPal Sandbox test account.'],
]);

const NBSP = '\u00a0';
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const shortDate = (iso) => {
  const match = /^\d{4}-(\d{2})-(\d{2})/u.exec(iso || '');
  return match ? `${MONTHS[Number(match[1]) - 1]} ${Number(match[2])}` : '';
};

const row = (id) => facts.rows.find((item) => item.id === id);
// Values quoted in the proof row itself: the send's Debug-Id and the read-back status.
const quoted = (item, pattern) => {
  for (const text of [...(item?.quotes || []), item?.how || '']) {
    const match = text.match(pattern);
    if (match) return match[1];
  }
  return null;
};

// One line: LABEL · plain origin. The full path stays in the title (hover) and on the Proof page.
function Source({ label, title, children }) {
  return <p className="tg-source" title={title}><span className="tg-source__label">{label}</span><span>· {children}</span></p>;
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
  const sendPaths = sends.map((item) => `${item.file}:${item.line}`).join(', ');
  const spike = figures.step2_example;
  const replay = figures.replay;
  const ai = figures.ai;
  const open = (page) => (event) => { event.preventDefault(); onOpen(page); };

  return <div className="ov" data-testid="overview-flow">
    {/* Where AI works. Every clause is in the repository: README.md:131 and :46, docs/SPONSOR_TECH_MAP.md:19 (guide),
        README.md:42 (AG Studio replay of the recording dated 2026-11-09, four questions). */}
    <figure className="tg-clip ov-ai" data-testid="overview-ai">
      <figcaption className="tg-clip__kicker">Where AI works</figcaption>
      <blockquote className="tg-clip__quote">In step 03 the evidence guide can use Gemini to turn the seller's own sentence into closed evidence items. Code checks every item; the model cannot mark one present, and PayPal decides the outcome.</blockquote>
      <Source label="Recorded" title={`${ai.guide_source}; ${ai.studio_source} (AG Studio agents, ${ai.studio_questions} questions, replayed on the dashboard)`}>Gemini guide runs, {shortDate(ai.guide_date)}; AG Studio agent run, {shortDate(ai.studio_date)}</Source>
    </figure>

    <ol className="ov-flow" aria-label="The seller flow, step by step">
      <li className="ov-step">
        <a className="ov-step__link" href="#compliance" data-testid="overview-step-compliance" onClick={open('compliance')}>
          <figure className="tg-clip tg-clip--step">
            <figcaption className="tg-clip__kicker">Before you ship<span className="tg-clip__num">01</span></figcaption>
            <p className="ov-step__name">Check a sale</p>
            <p className="ov-step__what">{example.route}, {example.goods}</p>
            <span className="tg-stamp tg-stamp--risk ov-step__stamp">{WARNING}Rule match</span>
            <blockquote className="tg-clip__quote">{example.statute} {example.article} · {example.tier}</blockquote>
            <Source label="Recounted" title={`${example.source}:${example.line} (${example.rule_id})`}>{example.source_plain} · row {example.line}</Source>
            <span className="ov-step__open">Open step {ARROW}</span>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#velocity" data-testid="overview-step-velocity" onClick={open('velocity')}>
          <figure className="tg-clip tg-clip--step">
            <figcaption className="tg-clip__kicker">When orders jump<span className="tg-clip__num">02</span></figcaption>
            <p className="ov-step__name">Sales spike</p>
            <p className="ov-step__what">Which orders need proof of delivery</p>
            <span className="ov-step__figure">×{spike.ratio}</span>
            <blockquote className="tg-clip__quote">{spike.orders} orders in {spike.window_hours} h · {spike.currency}{NBSP}{spike.total} vs usual {spike.currency}{NBSP}{spike.baseline_per_hour}/h</blockquote>
            <Source label="Synthetic" title={`${spike.source}:${spike.lines.baseline}, ${spike.lines.amounts}, ${spike.lines.burst_rows} (the burst this step loads)`}>{spike.source_plain}</Source>
            <span className="ov-step__open">Open step {ARROW}</span>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#disputes" data-testid="overview-step-disputes" onClick={open('disputes')}>
          <figure className="tg-clip tg-clip--step">
            <figcaption className="tg-clip__kicker">When a buyer disputes<span className="tg-clip__num">03</span></figcaption>
            <p className="ov-step__name">Disputes</p>
            <p className="ov-step__what">Evidence, a person's review, then the send</p>
            <span className="tg-stamp ov-step__stamp" data-testid="overview-send-stamp">{shortDate(sendRow?.date)} hosted send</span>
            <blockquote className="tg-clip__quote">Real Sandbox send · {send.case_ref} · {send.amount.currency}{NBSP}{send.amount.value}</blockquote>
            {debugId && <p className="ov-step__line">PayPal reference (Debug-Id) <span className="tg-mono">{debugId}</span></p>}
            {readBack && <p className="tg-done ov-step__line">{CHECK}Read-back: {readBack}</p>}
            <Source label="Hosted demo" title={`${send.source}:${send.line} · proof row ${send.proof_row}`}>{send.source_plain}, {shortDate(sendRow?.date)}</Source>
            <span className="ov-step__open">Open step {ARROW}</span>
          </figure>
        </a>
      </li>
    </ol>

    <div className="ov-facts" role="list" aria-label="Figures, each with its source">
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Rules check<span className="tg-clip__num">{rules.import_rules + rules.export_rules}</span></figcaption>
        <blockquote className="tg-clip__quote">official import and export rules ({rules.import_rules} import, {rules.export_rules} export)</blockquote>
        <Source label="Recounted" title={rules.source}>{rules.source_plain}</Source>
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Coverage<span className="tg-clip__num">{rules.countries}</span></figcaption>
        <blockquote className="tg-clip__quote">countries in the rules check</blockquote>
        <Source label="Recounted" title={rules.source}>{rules.source_plain}</Source>
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Sandbox sends<span className="tg-clip__num">{sends.length}</span></figcaption>
        <blockquote className="tg-clip__quote">real evidence sends on file</blockquote>
        <p className="tg-source" title={sendPaths}><span className="tg-source__label">Recorded</span><span>· {sendsWithId} receipts · <a className="tg-link" href="#proof" data-testid="overview-sends-proof" onClick={open('proof')}>see Proof</a></span></p>
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Proof rows<span className="tg-clip__num">{facts.rows.length}</span></figcaption>
        <blockquote className="tg-clip__quote">rows, each naming its source file</blockquote>
        <Source label="Recounted" title="frontend/src/data/proof_facts_v1.json">Proof table</Source>
      </figure>
    </div>

    <ul className="tg-legend" aria-label="What the source labels mean" data-testid="overview-legend">
      {SOURCE_LEGEND.map(([label, text]) => <li key={label}><b>{label}</b><span>{text}</span></li>)}
    </ul>

    <section className="tg-card ov-replay" aria-label="Recorded replay of an earlier send" data-testid="overview-replay">
      <p className="tg-eyebrow">{shortDate(replay.date)} local send: recorded replay (nothing is sent now)</p>
      <Suspense fallback={<p className="tg-small" role="status">Loading the recorded replay</p>}><RecordedSendReplay /></Suspense>
    </section>
  </div>;
}
