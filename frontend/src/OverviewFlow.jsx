// (P2 2026-11-12) Overview first screen: the three steps as one seller flow, one real result per step, four figures and
// the recorded send replay. Display only: every value comes from a committed data file (overview_figures_v1.json,
// proof_facts_v1.json), each recounted from its source by tests/frontend_overview_figures.mjs; nothing is requested.
// Loaded on demand, so the console's first-load budget does not carry it.
// (C 2026-11-12) Site-wide containers: step cards and figures are .tg-clip (--step / --fact).
// (F 2026-11-12) Sources and the legend come from theme/sources.js (one copy in data/source_labels_v1.json).
// (R5 2026-11-12, P0 designer) Each step card shows a small piece of the product; one size and one surface for all three.
// (vteam 2026-11-12, ui_mock/vteam/CONSENSUS.md sections 1 and 8) Layout: one focus area per page. The 10 Nov hosted
// Sandbox send is the focus (.tg-focus.tg-focus--bleed, the page's one .tg-keyfig) in the right 5 of a 7/5 .tg-split;
// the three step cards sit below in .tg-cards3 (rows shared across cards); the four figures sit on .tg-grid-paper.
// Icons come from the sprite (theme/iconMap.js). (a11y 4a) The send ticket carries the page's one focus-size icon, a 56px key
// figure and a heavier ink rule on top, so it, not the headline, is the first thing a squinting eye finds.
// SendTicket is also exported so App.jsx can place it beside the hero (render <OverviewFlow ticket={false} /> then).
import { lazy, Suspense } from 'react';
import figures from './data/overview_figures_v1.json';
import facts from './data/proof_facts_v1.json';
import checkSale from './data/check_sale_examples_v1.json';
import { SourceLegend, SourceLine } from './theme/sources.js';
import { dateLabel, money } from './theme/format.js';
import { ACTION, FOCUS, ROLE, STATUS, SpriteIcon } from './theme/iconMap.js';
import './OverviewFlow.css';

const RecordedSendReplay = lazy(() => import('./RecordedSendReplay.jsx'));

const row = (id) => facts.rows.find((item) => item.id === id);
// Values quoted in the proof row itself: the send's Debug-Id and the read-back status.
const quoted = (item, pattern) => {
  for (const text of [...(item?.quotes || []), item?.how || '']) {
    const match = text.match(pattern);
    if (match) return match[1];
  }
  return null;
};

// The 10 Nov hosted Sandbox send, read from the proof row and the Overview figures: the page's focus.
export function SendTicket({ onOpen }) {
  const send = figures.step3_send;
  const sendRow = row(send.proof_row);
  const debugId = quoted(sendRow, /PayPal-Debug-Id of the send: (\w+)/u);
  const readBack = quoted(sendRow, /read-back right after showed the status ([A-Za-z ]+?) with/u);
  return <section className="tg-focus tg-focus--bleed ov-ticket tg-block tg-block--ov-ticket tg-lift" tabIndex={-1} aria-labelledby="ov-ticket-title" data-testid="overview-send-ticket">
    <p className="tg-eyebrow ov-ticket__head" data-testid="overview-send-stamp"><SpriteIcon name={FOCUS.overview} size="focus" />{dateLabel(sendRow?.date)} hosted send</p>
    <h2 className="tg-h3 ov-ticket__title" id="ov-ticket-title">Sandbox send · {send.case_ref}</h2>
    <span className="tg-keyfig tg-keyfig--xl">{money(send.amount.value, send.amount.currency)}</span>
    <p className="ov-ticket__row tg-box"><span className="tg-stamp tg-stamp--ok"><SpriteIcon name={STATUS.ok} size="sm" />Submitted</span>{readBack && <span className="ov-ticket__wait"><SpriteIcon name={STATUS.warn} size="sm" />Read-back: {readBack}</span>}</p>
    {debugId && <p className="ov-ticket__ref tg-box" title="PayPal-Debug-Id, the reference PayPal returned for the send">PayPal reference <span className="tg-mono">{debugId}</span></p>}
    <SourceLine kind="HOSTED DEMO" source={send.source_key} />
    {onOpen && <a className="tg-link ov-ticket__open" href="#proof" data-testid="overview-ticket-proof" onClick={(event) => { event.preventDefault(); onOpen('proof'); }}>See every send in Proof <SpriteIcon name={ACTION.open} size="sm" /></a>}
  </section>;
}

export default function OverviewFlow({ onOpen, ticket = true }) {
  const rules = figures.country_rules;
  const example = figures.step1_example;
  const send = figures.step3_send;
  const sends = [...figures.receipt_sends, ...figures.readback_sends];
  const sendsWithId = sends.filter((item) => item.debug_id).length;
  const sendPaths = sends.map((item) => `${item.file}:${item.line}`).join(', ');
  const spike = figures.step2_example;
  // The spike card draws the usual hour against this hour, both from the data file (baseline per hour, total / hours).
  const perHour = Number(spike.total) / spike.window_hours;
  const usualWidth = `${Math.max(4, Math.round((Number(spike.baseline_per_hour) / perHour) * 100))}%`;
  const replay = figures.replay;
  const guide = checkSale.guide_ai;
  // (R6 S35) Card 01 also shows the export side of the same example (check first, by post only), from the Check a sale data.
  const also = checkSale.examples.find((item) => item.rule_id === example.rule_id)?.also;
  // Keep the statute's last word with its article ("Act s. 16") on one line.
  const statuteWords = example.statute.split(' ');
  const statuteEnd = statuteWords.pop();
  const open = (page) => (event) => { event.preventDefault(); onOpen(page); };

  const factsRow = <>
    <div className="ov-facts tg-grid-paper tg-block tg-block--ov-facts" role="list" aria-label="Figures, each with its source">
      <figure className="tg-clip tg-clip--fact tg-box" role="listitem">
        <figcaption className="tg-clip__kicker">Rules check<span className="tg-clip__num">{rules.import_rules + rules.export_rules}</span></figcaption>
        <blockquote className="tg-clip__quote">official import and export rules ({rules.import_rules} import, {rules.export_rules} export)</blockquote>
        <SourceLine kind="RECOUNTED" source={rules.source_key} />
      </figure>
      <figure className="tg-clip tg-clip--fact tg-box" role="listitem">
        <figcaption className="tg-clip__kicker">Coverage<span className="tg-clip__num">{rules.countries}</span></figcaption>
        <blockquote className="tg-clip__quote">countries in the rules check</blockquote>
        <SourceLine kind="RECOUNTED" source={rules.source_key} />
      </figure>
      <figure className="tg-clip tg-clip--fact tg-box" role="listitem">
        <figcaption className="tg-clip__kicker">Sandbox sends<span className="tg-clip__num">{sends.length}</span></figcaption>
        <blockquote className="tg-clip__quote">real evidence sends on file</blockquote>
        <SourceLine kind="RECORDED" text={`${sendsWithId} receipts`} title={sendPaths}><a className="tg-link" href="#proof" data-testid="overview-sends-proof" onClick={open('proof')}>see Proof</a></SourceLine>
      </figure>
      <figure className="tg-clip tg-clip--fact tg-box" role="listitem">
        <figcaption className="tg-clip__kicker">Proof rows<span className="tg-clip__num">{facts.rows.length}</span></figcaption>
        <blockquote className="tg-clip__quote">rows, each naming its source file</blockquote>
        <SourceLine kind="RECOUNTED" source="proof_table" />
      </figure>
    </div>

    <SourceLegend testId="overview-legend" />
  </>;
  return <div className="ov" data-testid="overview-flow">
    {ticket
      ? <div className="tg-split ov-top"><div className="ov-top__facts">{factsRow}</div><SendTicket onOpen={onOpen} /></div>
      : null}

    <ol className="ov-flow tg-cards3 tg-mod tg-mod--ov-flow" aria-label="The seller flow, step by step">
      <li className="ov-step">
        <a className="ov-step__link" href="#compliance" data-testid="overview-step-compliance" onClick={open('compliance')}>
          <figure className="tg-clip tg-clip--step tg-pad tg-block">
            <figcaption className="tg-clip__kicker">Before you ship<span className="tg-clip__num">01</span></figcaption>
            <p className="ov-step__name">Check a sale</p>
            <p className="ov-step__what">See whether a sale can ship before you take the money.</p>
            <div className="ov-screen tg-box" aria-label="What step 1 shows">
              <p className="ov-screen__row"><span>{example.route}</span><span className="ov-nowrap">{example.goods}</span></p>
              <p className="tg-risk ov-result"><SpriteIcon name={STATUS.risk} size="lg" />Rule match</p>
              <blockquote className="tg-clip__quote">{statuteWords.join(' ')} <span className="ov-nowrap">{statuteEnd} {example.article}</span> · {example.tier}</blockquote>
              {also && <p className="ov-screen__row ov-screen__row--stamp"><span className="tg-pill tg-pill--warn"><SpriteIcon name={STATUS.warn} size="sm" />{also.label}</span><span className="ov-step__line">{also.detail}</span></p>}
            </div>
            <div className="ov-step__foot tg-box">
              <SourceLine kind="RECOUNTED" source={example.source_key} />
              <span className="ov-step__open">Open step <SpriteIcon name={ACTION.open} size="sm" /></span>
            </div>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#velocity" data-testid="overview-step-velocity" onClick={open('velocity')}>
          <figure className="tg-clip tg-clip--step tg-pad tg-block">
            <figcaption className="tg-clip__kicker">When orders jump<span className="tg-clip__num">02</span></figcaption>
            <p className="ov-step__name">Sales spike</p>
            <p className="ov-step__what">Spot the hour that needs proof of delivery.</p>
            <div className="ov-screen tg-box" aria-label="What step 2 shows">
              <p className="ov-screen__row"><span>{spike.orders} orders in {spike.window_hours} h</span><span className="ov-step__figure">×{spike.ratio}</span></p>
              <div className="ov-bars" role="img" aria-label={`Usual hour ${money(spike.baseline_per_hour, spike.currency)}, this hour ${money(spike.total, spike.currency)}`}>
                <span className="ov-bar ov-bar--usual" style={{ '--ov-w': usualWidth }}><span className="ov-nowrap">Usual hour · {money(spike.baseline_per_hour, spike.currency)}</span></span>
                <span className="ov-bar ov-bar--now"><span className="ov-nowrap">This hour · {money(spike.total, spike.currency)}</span></span>
              </div>
            </div>
            <div className="ov-step__foot tg-box">
              <SourceLine kind="SYNTHETIC" source={spike.source_key} />
              <span className="ov-step__open">Open step <SpriteIcon name={ACTION.open} size="sm" /></span>
            </div>
          </figure>
        </a>
      </li>
      <li className="ov-step">
        <a className="ov-step__link" href="#disputes" data-testid="overview-step-disputes" onClick={open('disputes')}>
          <figure className="tg-clip tg-clip--step tg-pad tg-block">
            <figcaption className="tg-clip__kicker">When a buyer disputes<span className="tg-clip__num">03</span></figcaption>
            <p className="ov-step__name">Disputes</p>
            <p className="ov-step__what">Evidence, a person's review, then the send.</p>
            <ol className="ov-screen ov-steps3 tg-box" aria-label="What step 3 shows">
              <li><SpriteIcon name={ACTION.draft} size="sm" />Evidence drafted from your records</li>
              <li><SpriteIcon name={ROLE.reviewer} size="sm" />You review it, then confirm</li>
              <li><SpriteIcon name={ACTION.send} size="sm" />Sent to PayPal Sandbox, read back</li>
            </ol>
            <div className="ov-step__foot tg-box">
              <SourceLine kind="HOSTED DEMO" source={send.source_key} />
              <span className="ov-step__open">Open step <SpriteIcon name={ACTION.open} size="sm" /></span>
            </div>
          </figure>
        </a>
      </li>
    </ol>
    {!ticket && <div className="ov-facts-row tg-mod tg-mod--ov-facts">{factsRow}</div>}


    {/* Where AI works (4th look, under the figures). Numbers from check_sale_examples_v1.json guide_ai, recomputed from
        docs/evidence/GEMINI_GUIDE_RUNS_20261103.md:15 (policy pre-check row) by tests/test_check_sale_p3_data.py; the
        boundary clause is README.md:131 and :46, docs/SPONSOR_TECH_MAP.md:19. */}
    <figure className="tg-clip ov-ai tg-mod tg-block" data-testid="overview-ai">
      <figcaption className="tg-clip__kicker">Where AI works</figcaption>
      <blockquote className="tg-clip__quote tg-clip__quote--ruled ov-ai__text">Gemini guide, {guide.sentences} seller sentences: {guide.format_invalid} format-invalid replies, precision {guide.precision}, recall {guide.recall}. Code checks every item it fills; PayPal decides the outcome.</blockquote>
      <SourceLine kind="RECORDED" source="gemini_guide_runs" />
    </figure>

    <section className="tg-card ov-replay tg-mod" aria-label="Recorded replay of an earlier send" data-testid="overview-replay">
      <p className="tg-eyebrow">{dateLabel(replay.date)} local send: recorded replay (nothing is sent now)</p>
      <Suspense fallback={<p className="tg-small" role="status">Loading the recorded replay</p>}><RecordedSendReplay /></Suspense>
    </section>
  </div>;
}
