// (P4 2026-11-12) Step 02 / 03 containers, loaded on demand so the console first load stays in budget
// (ui_mock/CONTAINER_SPEC.md). Layout only: every value is a field the page already had (/demo/state disputes and
// velocity, the draft, the local review receipt, the Sandbox send result) or a cited receipt line. The page passes its
// own Icon and DueText so the marks match the rest of the console.
import { dateLabel as fmtDay, dateTimeLabel as fmtDateTime, money as fmtMoney, zoneLabel } from '../theme/format.js';
import { SourceLine } from '../theme/sources.js';
import { operatorLabel } from '../operatorLabels.js';
import './caseViews.css';

const VIEWER_ZONE = zoneLabel(-new Date().getTimezoneOffset());
const dateLabel = (value) => (value ? fmtDateTime(value) : '—');
const dayLabel = (value) => (value ? fmtDay(value, VIEWER_ZONE) : '—');
const moneyLabel = (value, currency) => fmtMoney(value, currency);
function dueDays(value) {
  const due = Date.parse(value || '');
  return Number.isFinite(due) ? Math.ceil((due - Date.now()) / 86400000) : null;
}

// Step 02 source line (the SYNTHETIC demo generator), kept here so theme/sources.js loads with the step, not up front.
export function VelocitySource() {
  return <SourceLine kind="SYNTHETIC" source="demo_burst" testId="velocity-source" />;
}

const caseDue = (item) => dueDays(item?.seller_response_due_date);
const dueShort = (value) => {
  const days = dueDays(value);
  return days === null ? '—' : days < 0 ? 'Overdue' : days === 0 ? 'Today' : `${days} day${days === 1 ? '' : 's'}`;
};
const caseMoney = (item) => (item?.dispute_amount ? moneyLabel(item.dispute_amount.value, item.dispute_amount.currency_code) : '—');

// Case queue as a ledger: case | reason | amount | due, most urgent first (missing deadlines last), ink rule every 5 rows.
export function CaseQueue({ Icon, DueText, cases, selected, busy, onPick }) {
  const rows = (Array.isArray(cases) ? cases : []).slice().sort((a, b) => (caseDue(a) ?? Infinity) - (caseDue(b) ?? Infinity));
  const urgent = rows.filter((item) => caseDue(item) !== null && caseDue(item) <= 1).length;
  return <section className="tg-ledger ds-queue" aria-labelledby="ds-queue-title">
    <p className="ds-queue__cap" id="ds-queue-title"><b>Case queue</b><span>Demo cases in this session · most urgent first</span></p>
    {rows.length ? <>
      <p className="ds-queue__head" aria-hidden="true"><span>Case · Reason</span><span>Amount · Due</span></p>
      <ol className="ds-queue__list">{rows.map((item) => <li key={item.case_ref}>
        <button type="button" className={`ds-queue__row${selected === item.case_ref ? ' tg-is-sel' : ''}`} aria-pressed={selected === item.case_ref} disabled={busy} data-link={`case:${item.case_ref}`} onClick={() => onPick(item)}>
          <span className="ds-queue__ref">{item.case_ref}</span>
          <span className="ds-queue__amt tg-num">{caseMoney(item)}</span>
          <span className="ds-queue__reason">{operatorLabel(item.reason)}</span>
          <span className="ds-queue__due tg-num" data-testid={`case-due-${item.case_ref}`}><DueText value={item.seller_response_due_date} fallback="—" /></span>
        </button></li>)}</ol>
      <p className="ds-queue__total">{rows.length} case{rows.length === 1 ? '' : 's'} · {urgent} due within a day</p>
    </> : <div className="empty-state"><Icon name="file" size={32} /><strong>No dispute cases</strong><p>Use “Load dispute case” above to start.</p></div>}
  </section>;
}

// Case head (rebuttal_case layout): reason as a 28px serif title, amount and deadline as 40px figures side by side, then
// the linked tags. This session's demo case is labelled as such; the real 10 Nov hosted send is a separate record on Proof.
export function CaseHead({ Icon, item, draft, sent, onProof }) {
  const days = caseDue(item);
  const due = days !== null && days <= 1;
  return <header className="ds-head" data-testid="case-summary" data-link={`case:${item.case_ref}`}>
    <p className="ds-head__kicker"><span className="tg-pill" data-testid="case-demo-label">Demo case in this session</span><span className="tg-tag tg-tag--neutral" data-testid="case-reason">{operatorLabel(item.reason)}</span><span>{operatorLabel(item.status)}</span></p>
    <h3 className="ds-head__title">{item.case_ref} · order {item.order_ref}</h3>
    <div className="ds-head__figs">
      <div><span className="ds-head__label">Respond within</span><strong className={`ds-head__num tg-num${due ? ' is-due' : days !== null && days <= 2 ? ' is-soon' : ''}`} data-testid="case-deadline">{due && <Icon name="clock" size={28} />}{dueShort(item.seller_response_due_date)}</strong><span className="tg-small">{item.seller_response_due_date ? `Due ${dateLabel(item.seller_response_due_date)}` : 'Shown after the draft'}</span></div>
      <div><span className="ds-head__label">Amount</span><strong className="ds-head__num tg-num" data-testid="case-amount">{caseMoney(item)}</strong></div>
    </div>
    <p className="ds-head__tags">
      <span className="tg-tag" tabIndex={0} data-link={`case:${item.case_ref}`}><Icon name="file" size={14} />{item.case_ref}</span>
      <span className="tg-tag" tabIndex={0} data-link={`order:${item.order_ref}`}><Icon name="layers" size={14} />{item.order_ref}</span>
      {draft && <span className="tg-tag" tabIndex={0} data-link="file:review-zip"><Icon name="lock" size={14} />Review ZIP</span>}
      {sent && <span className="tg-tag" tabIndex={0} data-link="paypal:send"><Icon name="link" size={14} />PayPal-Debug-Id</span>}
      {sent?.readback && <span className="tg-tag" tabIndex={0} data-link="paypal:readback"><Icon name="check" size={14} />Read-back</span>}
    </p>
    <SourceLine kind="SYNTHETIC" text="Demo case made for this session; Seller Protection: PayPal decides if it applies" title="backend/app/store.py (demo dispute cases)" testId="case-source" />
    <SourceLine kind="HOSTED DEMO" source="hosted_receipt" testId="case-hosted-source"><a className="tg-link" href="#proof" data-testid="case-proof-link" onClick={(event) => { event.preventDefault(); onProof(); }}>The real 10 Nov 2026 send is on Proof</a></SourceLine>
  </header>;
}

// Case timeline as a day book: when | who (Buyer / You / PayPal) | what happened | next; the deadline closes it.
export function CaseLog({ Icon, item, draft, receipt, sent }) {
  const ev = draft?.evidence || {};
  const days = caseDue(item);
  const rows = [
    ev.order_created_at && { at: ev.order_created_at, who: 'Buyer', what: `Placed order ${item.order_ref}`, link: `order:${item.order_ref}`, state: 'is-done' },
    ev.delivered_at && { at: ev.delivered_at, who: 'You', what: `Delivery recorded: ${operatorLabel(ev.carrier_status)}`, state: 'is-done' },
    { at: item.opened_at, who: 'Buyer', what: `Opened a dispute: ${operatorLabel(item.reason)}`, next: draft ? '' : 'Next: prepare the evidence draft.', link: `case:${item.case_ref}` },
    draft && { who: 'You', what: 'Prepared the evidence draft and the review ZIP', next: receipt ? '' : 'Next: check it, then record your review.', link: 'file:review-zip', state: 'is-done' },
    receipt && { at: receipt.reviewed_at, who: 'You', what: 'Recorded your review (local, demo)', state: 'is-done' },
    sent && { who: 'PayPal', what: 'Received the evidence (Sandbox)', ref: `PayPal-Debug-Id ${sent.debug || 'not returned'}`, link: 'paypal:send', state: 'is-done' },
    item.seller_response_due_date && { at: item.seller_response_due_date, who: 'PayPal', what: 'Seller response due', next: 'PayPal decides the case.', state: days !== null && days <= 1 ? 'is-risk' : 'is-pending', due: days !== null && days <= 1 },
  ].filter(Boolean);
  return <ol className="tg-log ds-log" data-testid="case-log" aria-label="Case timeline">{rows.map((row, index) => <li key={index} className={`tg-log__entry ${row.state || ''}`} data-link={row.link}>
    <span className="tg-log__when">{row.at ? dayLabel(row.at).replace(/ \d{4}$/u, '') : 'Now'}</span>
    <div className="tg-log__body">
      <span className="tg-log__dateline">{row.at ? dateLabel(row.at) : 'This session'}</span>
      <p className="tg-log__title">{row.due && <Icon name="clock" size={16} />}<span className="tg-log__who">{row.who}</span>{row.what}</p>
      {row.next && <p className="tg-log__next">{row.next}</p>}
      {row.ref && <span className="tg-log__ref">{row.ref}</span>}
    </div>
  </li>)}</ol>;
}

// The AI step, open by default in the main column beside the evidence list (review_INTEG #1, review_FULL s4): sentence ->
// evidence item -> program check. Live values are the guide's own (chooser state from the guide API it calls when opened,
// open items it reports to the page); the recorded runs are cited. Adds no request.
export function DisputeAiClip({ chooser, openItems = 0 }) {
  const live = chooser ? (chooser.chooser_mode === 'gemini' ? 'Rules + Gemini' : 'Rules only') : 'Not started';
  return <figure className="tg-clip ds-ai" data-testid="dispute-ai-clip" data-link="ai:guide">
    <p className="tg-clip__kicker">AI step · Gemini evidence guide · <span data-testid="dispute-ai-state">{live}</span></p>
    <ol className="ds-ai__flow">
      <li><b>Your sentence</b><span>Tell the guide what happened, in your own words.</span></li>
      <li><b>Evidence item</b><span>Gemini points the sentence at one missing item{openItems > 0 ? ` · ${openItems} still open` : ''}.</span></li>
      <li><b>Program check</b><span>Fixed rules decide what counts; the model cannot mark evidence by itself.</span></li>
    </ol>
    <p className="ds-ai__state"><a className="tg-link" href="#guide-dispute">Open the guide</a></p>
    <SourceLine kind="RECORDED" source="gemini_guide_runs" />
    <SourceLine kind="RECORDED" source="ag_studio_runs"><a className="tg-link" href="/dashboard.html">AG Studio questions</a></SourceLine>
  </figure>;
}

// The real hosted Sandbox send of 10 Nov 2026, as PayPal answered it (For judges stop 03 points here). A record from
// docs/evidence/RECEIPT_20261110_hosted_live.md, not this session's demo case, which is never marked as sent here.
const HOSTED_SEND = [
  ['13:46', 'You', 'POST provide-evidence: evidence for case-ref-001 (item not received, USD 48.00) to Sandbox dispute PP-R-…7877', 'f869050ae2a63', 14],
  ['13:46', 'PayPal', 'GET dispute read-back right after the send: Under review', 'f2530346edb95', 16],
  ['Result', 'PayPal', 'SUBMITTED to PayPal Sandbox; PayPal, not TradeGlot, decides the case', '', 13],
];
export function HostedSendLog() {
  return <section id="hosted-send" className="ds-hosted" data-testid="hosted-send-log" aria-labelledby="hosted-send-title">
    <p className="tg-wire__head" id="hosted-send-title">Recorded hosted send · 10 Nov 2026</p>
    <p className="tg-small">The one real send made from the public hosted demo on 10 Nov 2026. It is a separate record, not the demo case in this session. Times as written in the receipt.</p>
    <ol className="tg-log">{HOSTED_SEND.map(([when, who, what, debug, line]) => <li key={line} className="tg-log__entry is-done" data-link={debug ? `paypal:${debug}` : undefined}>
      <span className="tg-log__when">{when}</span>
      <div className="tg-log__body"><p className="tg-log__title"><span className="tg-log__who">{who}</span>{what}</p>{debug && <span className="tg-log__ref">PayPal-Debug-Id {debug}</span>}</div>
    </li>)}</ol>
    <SourceLine kind="HOSTED DEMO" source="hosted_receipt" testId="hosted-send-source" />
  </section>;
}
