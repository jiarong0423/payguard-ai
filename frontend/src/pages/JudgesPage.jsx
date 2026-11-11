// (P5 2026-11-12) Console For judges page: a 90-second route through four console pages. Each step is a .tg-clip--step
// with a large number, the title, what to look for, a time budget and a deep link to that page's hash. No new facts:
// the route and seconds come from judges_route_v1.json; every value to look for is read from overview_figures_v1.json,
// proof_facts_v1.json or proof_ledger_v1.json (each checked against its source by the existing tests and by
// tests/frontend_proof_page.mjs). tests/frontend_judges_page.mjs checks each target page exists in App.jsx.
import route from '../data/judges_route_v1.json';
import figures from '../data/overview_figures_v1.json';
import facts from '../data/proof_facts_v1.json';
import ledger from '../data/proof_ledger_v1.json';
import arrowSvg from '../theme/icons/arrow-right.svg?raw';
import clockSvg from '../theme/icons/clock.svg?raw';
import checkSvg from '../theme/icons/check-circle.svg?raw';
import warningSvg from '../theme/icons/warning.svg?raw';
import './JudgesPage.css';

const ICONS = { arrow: arrowSvg, clock: clockSvg, check: checkSvg, warning: warningSvg };
function Icon({ name }) {
  return <span className="tg-icon jp-icon" aria-hidden="true" dangerouslySetInnerHTML={{ __html: ICONS[name] }} />;
}
function Source({ label, text, path }) {
  return <span className="tg-source" title={path}><span className="tg-source__label">{label}</span>· {text}</span>;
}
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const plainDate = (iso) => { const [, month, day] = iso.split('-').map(Number); return `${day} ${MONTHS[month - 1]}`; };

// What each step asks judges to look for, built from the committed data files.
function lookFor(page) {
  if (page === 'compliance') {
    const rule = figures.step1_example;
    return {
      marks: [{ stamp: 'risk', text: 'Rule match' }, { mono: rule.rule_id }],
      see: `${rule.route}, ${rule.goods}: ${rule.statute} ${rule.article}, ${rule.tier}.`,
      source: { label: 'RECOUNTED', text: `Country rules file · line ${rule.line}`, path: `${rule.source}:${rule.line}` },
    };
  }
  if (page === 'velocity') {
    const spike = figures.step2_example;
    return {
      marks: [{ figure: `×${spike.ratio}` }],
      see: `${spike.orders} orders in ${spike.window_hours} h: ${spike.currency} ${spike.total} against a usual ${spike.currency} ${spike.baseline_per_hour} an hour.`,
      source: { label: 'SYNTHETIC', text: `Demo order generator · line ${spike.lines.burst_rows}`, path: `${spike.source}:${spike.lines.burst_rows}` },
    };
  }
  if (page === 'disputes') {
    const send = ledger.sends.find((item) => item.basis === 'HOSTED DEMO');
    const row = facts.rows.find((item) => item.id === figures.step3_send.proof_row);
    return {
      marks: [{ label: 'PayPal-Debug-Id' }, { mono: send.debug_id.value }],
      see: `${figures.step3_send.case_ref}, ${figures.step3_send.amount.currency} ${figures.step3_send.amount.value}, sent from the hosted demo on ${plainDate(row.date)}; read back as ${send.readback.value}.`,
      source: { label: 'HOSTED DEMO', text: `${send.label} · line ${send.debug_id.line}`, path: `${send.file}:${send.debug_id.line}` },
    };
  }
  const verify = ledger.verify;
  const send = ledger.sends.find((item) => item.id === verify.send_id);
  return {
    marks: [{ stamp: 'ok', text: 'Match' }],
    see: `Your browser hashes the ${verify.served_bytes.value} PayPal served back and compares it with ${verify.recorded_sha256.value.slice(0, 8)}…, recorded at send time. Then change one byte.`,
    source: { label: send.basis, text: `${send.label} · line ${verify.recorded_sha256.line}`, path: `${verify.file}:${verify.recorded_sha256.line}` },
  };
}

function Mark({ mark }) {
  if (mark.stamp) return <span className={`tg-stamp tg-stamp--${mark.stamp}`}><Icon name={mark.stamp === 'ok' ? 'check' : 'warning'} />{mark.text}</span>;
  if (mark.figure) return <span className="jp-figure">{mark.figure}</span>;
  if (mark.mono) return <span className="tg-mono jp-mono">{mark.mono}</span>;
  return <span className="tg-eyebrow">{mark.label}</span>;
}

export default function JudgesPage({ onOpen }) {
  const total = route.steps.reduce((sum, step) => sum + step.seconds, 0);
  const open = (page) => (event) => {
    if (!onOpen) return;
    event.preventDefault();
    onOpen(page);
  };
  return <div className="jp" data-testid="judges-page">
    <p className="jp-total"><Icon name="clock" /><span>About {total} seconds, {route.steps.length} stops. Each stop opens the page, says what to press and what to look for.</span></p>
    <ol className="jp-route" aria-label="The route for judges">
      {route.steps.map((step, index) => {
        const look = lookFor(step.page);
        return <li key={step.page}>
          <figure className="tg-clip tg-clip--step jp-step" data-testid={`judges-step-${step.page}`}>
            <span className="tg-clip__num jp-step__n" aria-hidden="true">{step.n}</span>
            <div className="jp-step__body">
              <figcaption className="jp-step__head"><h3 className="tg-h3">{step.title}</h3><span className="jp-step__time"><Icon name="clock" />≈ {step.seconds} s</span></figcaption>
              <p className="jp-step__do">{step.action}</p>
              <p className="tg-clip__kicker jp-step__kicker">Look for</p>
              <blockquote className="tg-clip__quote jp-step__look">
                <span className="jp-look__marks">{look.marks.map((mark, markIndex) => <Mark key={markIndex} mark={mark} />)}</span>
                <span className="jp-look__see">{look.see}</span>
              </blockquote>
              <div className="tg-clip__source jp-step__foot">
                <Source {...look.source} />
                <a className={`tg-btn ${index === 0 ? 'tg-btn--primary' : 'tg-btn--secondary'}`} href={`#${step.page}`} data-testid={`judges-link-${step.page}`} onClick={open(step.page)}>Open {step.title}<Icon name="arrow" /></a>
              </div>
            </div>
          </figure>
        </li>;
      })}
    </ol>
    <ul className="tg-legend" data-testid="judges-basis-legend" aria-label="What the source labels mean">{ledger.basis.map((item) => <li key={item.label}><b>{item.label}</b><span>{item.meaning}</span></li>)}</ul>
  </div>;
}
