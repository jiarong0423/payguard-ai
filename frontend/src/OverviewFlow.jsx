// (P2 2026-11-12) Overview first screen: the three steps as one seller flow, one real result per step, four figures and
// the recorded send replay. Display only: every value comes from a committed data file (overview_figures_v1.json,
// proof_facts_v1.json), each recounted from its source by tests/frontend_overview_figures.mjs; nothing is requested.
// Loaded on demand, so the console's first-load budget does not carry it.
// (C 2026-11-12) Site-wide containers: step cards and figures are .tg-clip (--step / --fact).
// (F 2026-11-12) Sources and the legend come from theme/sources.js (one copy in data/source_labels_v1.json); a source
// line wraps instead of being cut, the full path in its title. Dates and money through theme/format.js.
// (R5 2026-11-12, P0 designer) Each step card now shows a small piece of the product ("what you will see"): the rule
// result, the hour against a usual hour, the send ticket. All three cards share one size and one surface; the source line
// and the Open link sit together at the foot of every card. Review: ext_review/review_UI5.md section 1, review_FULL.md.
import { lazy, Suspense } from 'react';
import figures from './data/overview_figures_v1.json';
import facts from './data/proof_facts_v1.json';
import checkSale from './data/check_sale_examples_v1.json';
import { SourceLegend, SourceLine } from './theme/sources.js';
import { dateLabel, money } from './theme/format.js';
import './OverviewFlow.css';

const RecordedSendReplay = lazy(() => import('./RecordedSendReplay.jsx'));

// Phosphor regular icons, path data copied from theme/icons/*.svg (MIT, theme/icons/LICENSE).
const icon = (d) => <svg className="tg-icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d={d} /></svg>;
const WARNING = icon('M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z');
const CLOCK = icon('M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z');
const CHECK = icon('M173.66,98.34a8,8,0,0,1,0,11.32l-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35A8,8,0,0,1,173.66,98.34ZM232,128A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128Z');
const ARROW = icon('M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z');


const row = (id) => facts.rows.find((item) => item.id === id);
// Values quoted in the proof row itself: the send's Debug-Id and the read-back status.
const quoted = (item, pattern) => {
  for (const text of [...(item?.quotes || []), item?.how || '']) {
    const match = text.match(pattern);
    if (match) return match[1];
  }
  return null;
};

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
  // The spike card draws the usual hour against this hour, both from the data file (baseline per hour, total / hours).
  const perHour = Number(spike.total) / spike.window_hours;
  const usualWidth = `${Math.max(4, Math.round((Number(spike.baseline_per_hour) / perHour) * 100))}%`;
  const replay = figures.replay;
  const guide = checkSale.guide_ai;
  const open = (page) => (event) => { event.preventDefault(); onOpen(page); };

  return <div className="ov" data-testid="overview-flow">

    <ol className="ov-flow" aria-label="The seller flow, step by step">
      <li className="ov-step">
        <a className="ov-step__link" href="#compliance" data-testid="overview-step-compliance" onClick={open('compliance')}>
          <figure className="tg-clip tg-clip--step tg-pad">
            <figcaption className="tg-clip__kicker">Before you ship<span className="tg-clip__num">01</span></figcaption>
            <p className="ov-step__name">Check a sale</p>
            <p className="ov-step__what">See whether a sale can ship before you take the money.</p>
            <div className="ov-screen" aria-label="What step 1 shows">
              <p className="ov-screen__row"><span>{example.route}</span><span className="ov-nowrap">{example.goods}</span></p>
              <span className="tg-stamp tg-stamp--risk ov-step__stamp">{WARNING}Rule match</span>
              <blockquote className="tg-clip__quote">{example.statute} {example.article} · {example.tier}</blockquote>
            </div>
            <div className="ov-step__foot">
              <SourceLine kind="RECOUNTED" source={example.source_key} />
              <span className="ov-step__open">Open step {ARROW}</span>
            </div>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#velocity" data-testid="overview-step-velocity" onClick={open('velocity')}>
          <figure className="tg-clip tg-clip--step tg-pad">
            <figcaption className="tg-clip__kicker">When orders jump<span className="tg-clip__num">02</span></figcaption>
            <p className="ov-step__name">Sales spike</p>
            <p className="ov-step__what">Spot the hour that needs proof of delivery.</p>
            <div className="ov-screen" aria-label="What step 2 shows">
              <p className="ov-screen__row"><span>{spike.orders} orders in {spike.window_hours} h</span><span className="ov-step__figure">×{spike.ratio}</span></p>
              <div className="ov-bars" role="img" aria-label={`Usual hour ${money(spike.baseline_per_hour, spike.currency)}, this hour ${money(spike.total, spike.currency)}`}>
                <span className="ov-bar ov-bar--usual" style={{ '--ov-w': usualWidth }}><span className="ov-nowrap">Usual hour · {money(spike.baseline_per_hour, spike.currency)}</span></span>
                <span className="ov-bar ov-bar--now"><span className="ov-nowrap">This hour · {money(spike.total, spike.currency)}</span></span>
              </div>
            </div>
            <div className="ov-step__foot">
              <SourceLine kind="SYNTHETIC" source={spike.source_key} />
              <span className="ov-step__open">Open step {ARROW}</span>
            </div>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#disputes" data-testid="overview-step-disputes" onClick={open('disputes')}>
          <figure className="tg-clip tg-clip--step tg-pad">
            <figcaption className="tg-clip__kicker">When a buyer disputes<span className="tg-clip__num">03</span></figcaption>
            <p className="ov-step__name">Disputes</p>
            <p className="ov-step__what">Evidence, a person's review, then the send.</p>
            <div className="ov-screen ov-ticket" aria-label="What step 3 shows">
              <p className="ov-ticket__head" data-testid="overview-send-stamp">{dateLabel(sendRow?.date)} hosted send</p>
              <p className="ov-screen__row"><span>Sandbox send · {send.case_ref}</span><span className="ov-nowrap">{money(send.amount.value, send.amount.currency)}</span></p>
              {debugId && <p className="ov-step__line" title="PayPal-Debug-Id, the reference PayPal returned for the send">PayPal reference <span className="tg-mono">{debugId}</span></p>}
              <p className="ov-screen__row ov-screen__row--stamp"><span className="tg-stamp tg-stamp--ok">{CHECK}Submitted</span>{readBack && <span className="ov-step__line ov-step__wait">{CLOCK}Read-back: {readBack}</span>}</p>
            </div>
            <div className="ov-step__foot">
              <SourceLine kind="HOSTED DEMO" source={send.source_key} />
              <span className="ov-step__open">Open step {ARROW}</span>
            </div>
          </figure>
        </a>
      </li>
    </ol>

    <div className="ov-facts" role="list" aria-label="Figures, each with its source">
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Rules check<span className="tg-clip__num">{rules.import_rules + rules.export_rules}</span></figcaption>
        <blockquote className="tg-clip__quote">official import and export rules ({rules.import_rules} import, {rules.export_rules} export)</blockquote>
        <SourceLine kind="RECOUNTED" source={rules.source_key} />
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Coverage<span className="tg-clip__num">{rules.countries}</span></figcaption>
        <blockquote className="tg-clip__quote">countries in the rules check</blockquote>
        <SourceLine kind="RECOUNTED" source={rules.source_key} />
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Sandbox sends<span className="tg-clip__num">{sends.length}</span></figcaption>
        <blockquote className="tg-clip__quote">real evidence sends on file</blockquote>
        <SourceLine kind="RECORDED" text={`${sendsWithId} receipts`} title={sendPaths}><a className="tg-link" href="#proof" data-testid="overview-sends-proof" onClick={open('proof')}>see Proof</a></SourceLine>
      </figure>
      <figure className="tg-clip tg-clip--fact" role="listitem">
        <figcaption className="tg-clip__kicker">Proof rows<span className="tg-clip__num">{facts.rows.length}</span></figcaption>
        <blockquote className="tg-clip__quote">rows, each naming its source file</blockquote>
        <SourceLine kind="RECOUNTED" source="proof_table" />
      </figure>
    </div>

    <SourceLegend testId="overview-legend" />

    {/* Where AI works (4th look, under the figures). Numbers from check_sale_examples_v1.json guide_ai, recomputed from
        docs/evidence/GEMINI_GUIDE_RUNS_20261103.md:15 (policy pre-check row) by tests/test_check_sale_p3_data.py; the
        boundary clause is README.md:131 and :46, docs/SPONSOR_TECH_MAP.md:19. */}
    <figure className="tg-clip ov-ai" data-testid="overview-ai">
      <figcaption className="tg-clip__kicker">Where AI works</figcaption>
      <blockquote className="tg-clip__quote tg-clip__quote--ruled ov-ai__text">Gemini guide, {guide.sentences} seller sentences: {guide.format_invalid} format-invalid replies, precision {guide.precision}, recall {guide.recall}. Code checks every item it fills; PayPal decides the outcome.</blockquote>
      <SourceLine kind="RECORDED" source="gemini_guide_runs" />
    </figure>

    <section className="tg-card ov-replay" aria-label="Recorded replay of an earlier send" data-testid="overview-replay">
      <p className="tg-eyebrow">{dateLabel(replay.date)} local send: recorded replay (nothing is sent now)</p>
      <Suspense fallback={<p className="tg-small" role="status">Loading the recorded replay</p>}><RecordedSendReplay /></Suspense>
    </section>
  </div>;
}
