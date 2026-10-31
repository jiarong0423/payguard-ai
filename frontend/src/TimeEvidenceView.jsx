import { operatorLabel } from './operatorLabels.js';

const GAP_NAMES = [
  ['payment_to_order_record', 'Payment to order record'],
  ['payment_to_delivery', 'Payment to delivery'],
  ['delivery_to_claim', 'Delivery to claim'],
  ['payment_to_claim', 'Payment to claim'],
];

function whenLabel(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return `${date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}

function gapLabel(seconds) {
  if (seconds === null || seconds === undefined) return 'Not recorded';
  const sign = seconds < 0 ? '−' : '';
  const total = Math.abs(seconds);
  const days = Math.floor(total / 86400);
  const hours = Math.floor((total % 86400) / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  if (days > 0) return `${sign}${days} d ${hours} h`;
  if (hours > 0) return `${sign}${hours} h ${minutes} min`;
  return `${sign}${minutes} min`;
}

export default function TimeEvidenceView({ evidence }) {
  if (!evidence || !Array.isArray(evidence.events)) return null;
  return (
    <section className="time-evidence" data-testid="time-evidence" aria-label="Time evidence">
      <div className="mini-heading"><span>Time evidence · ordered, not judged</span><span className="badge badge-amber">SYNTHETIC</span></div>
      <ol className="time-events">
        {evidence.events.map((event, index) => (
          <li key={`${event.kind}-${event.at}-${index}`} className={`time-event time-event-${event.kind.toLowerCase()}`}>
            <time dateTime={event.at}>{whenLabel(event.at)}</time>
            <strong>{operatorLabel(event.kind)}</strong>
            {event.kind === 'MESSAGE' && <span>{operatorLabel(event.channel)} · {operatorLabel(event.direction)} · {operatorLabel(event.topic)}</span>}
            <em>{operatorLabel(event.source)}</em>
          </li>
        ))}
      </ol>
      <div className="time-gaps">
        {GAP_NAMES.map(([key, label]) => (
          <div key={key}><span>{label}</span><strong>{gapLabel(evidence.gaps_seconds?.[key])}</strong></div>
        ))}
      </div>
      {evidence.flags?.length > 0 && (
        <p className="time-flags">{evidence.flags.map((flag) => <span key={flag} className="badge badge-muted">{operatorLabel(flag)}</span>)}</p>
      )}
      <p className="time-note">PayGuard orders and preserves times. It states no intent, predicts no outcome and gives no legal advice. Messages are kept as a topic and a keyed digest, never as text. A negative gap means the second event is earlier than the first.</p>
    </section>
  );
}
