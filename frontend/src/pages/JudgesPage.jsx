// (P5 2026-11-12) Console For judges page: a 90-second route through four console pages. Each step is a .tg-clip--step
// with a large number, the title, what to look for, a time budget and a deep link to that page's hash. No new facts:
// the route and seconds come from judges_route_v1.json; every value to look for is read from overview_figures_v1.json,
// proof_facts_v1.json or proof_ledger_v1.json (each checked against its source by the existing tests and by
// tests/frontend_proof_page.mjs). tests/frontend_judges_page.mjs checks each target page exists in App.jsx.
// (F 2026-11-12) Each stop is one row (number | title and action | look for | seconds | button) so all four fit the
// 1440x900 first screen; the route length is said once, in the page lede. Sources and the legend from theme/sources.js.
// (R5 2026-11-12, P0 designer) One look-for vocabulary: every stop shows one framed mark of the same height (a stamp for
// an outcome, a neutral tag with an icon for a value), buttons share one width, rows are split by a single fine rule, and
// a closing line says where to reset. Review: ext_review/review_UI5.md section 4.
import route from '../data/judges_route_v1.json';
import figures from '../data/overview_figures_v1.json';
import facts from '../data/proof_facts_v1.json';
import ledger from '../data/proof_ledger_v1.json';
import arrowSvg from '../theme/icons/arrow-right.svg?raw';
import clockSvg from '../theme/icons/clock.svg?raw';
import checkSvg from '../theme/icons/check-circle.svg?raw';
import warningSvg from '../theme/icons/warning.svg?raw';
import chartSvg from '../theme/icons/chart-line-up.svg?raw';
import fingerprintSvg from '../theme/icons/fingerprint.svg?raw';
import { SourceLegend, SourceLine } from '../theme/sources.js';
import { dateLabel, money } from '../theme/format.js';
import './JudgesPage.css';

const ICONS = { arrow: arrowSvg, clock: clockSvg, check: checkSvg, warning: warningSvg, chart: chartSvg, fingerprint: fingerprintSvg };
function Icon({ name }) {
  return <span className="tg-icon jp-icon" aria-hidden="true" dangerouslySetInnerHTML={{ __html: ICONS[name] }} />;
}

// What each step asks judges to look for, built from the committed data files.
function lookFor(page) {
  if (page === 'compliance') {
    const rule = figures.step1_example;
    return {
      marks: [{ stamp: 'risk', text: 'Rule match' }, { mono: rule.rule_id }],
      see: `${rule.route}, ${rule.goods}: ${rule.statute} ${rule.article}, ${rule.tier}.`,
      source: { kind: 'RECOUNTED', source: rule.source_key },
    };
  }
  if (page === 'velocity') {
    const spike = figures.step2_example;
    return {
      marks: [{ tag: `×${spike.ratio} the usual hour`, icon: 'chart' }],
      see: `${spike.orders} orders in ${spike.window_hours} h: ${money(spike.total, spike.currency)} against a usual ${money(spike.baseline_per_hour, spike.currency)} an hour.`,
      source: { kind: 'SYNTHETIC', source: spike.source_key },
    };
  }
  if (page === 'disputes') {
    const send = ledger.sends.find((item) => item.basis === 'HOSTED DEMO');
    const row = facts.rows.find((item) => item.id === figures.step3_send.proof_row);
    return {
      marks: [{ tag: 'PayPal reference', mono: send.debug_id.value, icon: 'fingerprint', title: 'PayPal-Debug-Id, the reference PayPal returned for the send' }],
      see: `Recorded hosted send · ${dateLabel(row.date)}: ${figures.step3_send.case_ref}, ${money(figures.step3_send.amount.value, figures.step3_send.amount.currency)}, read back as ${send.readback.value}.`,
      source: { kind: 'HOSTED DEMO', source: send.source_key },
    };
  }
  const verify = ledger.verify;
  const send = ledger.sends.find((item) => item.id === verify.send_id);
  return {
    marks: [{ stamp: 'ok', text: 'Match' }],
    see: `Your browser hashes the ${verify.served_bytes.value} PayPal served back; it must equal ${verify.recorded_sha256.value.slice(0, 8)}…, recorded at send time.`,
    source: { kind: send.basis, source: send.source_key },
  };
}

function Mark({ mark }) {
  if (mark.stamp) return <span className={`tg-stamp tg-stamp--${mark.stamp}`}><Icon name={{ ok: 'check', risk: 'warning', warn: 'clock' }[mark.stamp] || 'clock'} />{mark.text}</span>;
  if (mark.tag) return <span className="tg-tag tg-tag--neutral jp-tag" title={mark.title}><Icon name={mark.icon} />{mark.tag}{mark.mono && <span className="tg-mono jp-mono">{mark.mono}</span>}</span>;
  if (mark.mono) return <span className="tg-mono jp-mono">{mark.mono}</span>;
  return <span className="tg-eyebrow">{mark.label}</span>;
}

export default function JudgesPage({ onOpen }) {
  // A stop with an anchor (Proof: #verify) scrolls to it once the lazily loaded page has drawn it.
  const open = (page, anchor) => (event) => {
    if (!onOpen) return;
    event.preventDefault();
    onOpen(page);
    if (!anchor) return;
    const until = Date.now() + 3e3; // give the lazy page up to three seconds
    // (phone r5) Wait until the target is on screen (its page is shown, not just in the DOM), then scroll once more
    // after the lazy parts above it have drawn, so it does not land short of the anchor.
    const seek = () => {
      const target = document.getElementById(anchor);
      if (target && target.offsetParent !== null) {
        target.scrollIntoView({ block: 'start' });
        window.setTimeout(() => target.scrollIntoView({ block: 'start' }), 7e2);
      } else if (Date.now() < until) window.requestAnimationFrame(seek);
    };
    window.requestAnimationFrame(seek);
  };
  return <div className="jp" data-testid="judges-page">
    <ol className="jp-route" aria-label="The route for judges">
      {route.steps.map((step, index) => {
        const look = lookFor(step.page);
        return <li key={step.page}>
          <figure className="tg-clip tg-clip--step jp-step" data-testid={`judges-step-${step.page}`}>
            <span className="tg-clip__num jp-step__n" aria-hidden="true">{step.n}</span>
            <figcaption className="jp-step__head"><h3 className="tg-h3">{step.title}</h3><p className="jp-step__do">{step.action}</p></figcaption>
            <div className="jp-step__look">
              <blockquote className="tg-clip__quote jp-step__quote">
                <span className="jp-look__marks"><span className="tg-clip__kicker jp-step__kicker">Look for</span>{look.marks.map((mark, markIndex) => <Mark key={markIndex} mark={mark} />)}</span>
                <span className="jp-look__see">{look.see}</span>
              </blockquote>
              <div className="tg-clip__source"><SourceLine {...look.source} /></div>
            </div>
            <span className="jp-step__time"><Icon name="clock" />≈ {step.seconds} s</span>
            <a className={`tg-btn ${index === 0 ? 'tg-btn--primary' : 'tg-btn--secondary'} jp-step__open`} href={`#${step.page}`} data-testid={`judges-link-${step.page}`} onClick={open(step.page, step.anchor)}>Open {step.title}<Icon name="arrow" /></a>
          </figure>
        </li>;
      })}
    </ol>
    <p className="jp-reset" data-testid="judges-reset-note">Stuck? Every step has a Reset demo button. Nothing you press on this page is sent anywhere.</p>
    <SourceLegend testId="judges-basis-legend" />
  </div>;
}
