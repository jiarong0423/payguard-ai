// Data sources for the AG Studio dispute evidence readiness dashboard. Pure functions over files
// already in the repository (the caller passes them in); nothing here is invented, fetched or written back.
//   disputes   frontend/src/data/dashboard_disputes_v1.json  synthetic cases read back through the real API (tools/build_dashboard_data.py)
//   benchmark  frontend/src/data/guide_benchmark_v1.json     recorded guide benchmark
//   receipts   frontend/src/data/channel3_receipts_v1.json   copy of docs/evidence/channel3_receipts_v1.json (drift-tested)
import { operatorLabel } from '../operatorLabels.js';

const DAY_MS = 86400000;
export const DUE_SOON_DAYS = 3;

// Labels the console has no entry for yet; kept here so operatorLabels.js stays unchanged.
const LOCAL_LABELS = {
  delivery_not_before_dispute: 'Delivery recorded after the claim opened',
  FOUND: 'Found',
};

export function label(value) {
  if (value === null || value === undefined || value === '') return 'None';
  return LOCAL_LABELS[value] || operatorLabel(value, String(value));
}

export function daysBetween(fromIso, toIso) {
  return Math.round((Date.parse(toIso) - Date.parse(fromIso)) / DAY_MS * 10) / 10;
}

// The file is built at a fixed clock (tools/build_dashboard_data.py, as_of 2026-11-01 12:00 UTC). The console makes the
// same synthetic cases relative to its own clock, so the dashboard moves every case time by (now - as_of): due dates
// then match the console and its deadline board, and days to due stay exactly as built (r20 UX-1).
const shift = (iso, deltaMs) => (typeof iso === 'string' && Number.isFinite(Date.parse(iso)) ? new Date(Date.parse(iso) + deltaMs).toISOString() : iso);

export function rebaseDisputes(source, nowIso) {
  const deltaMs = Date.parse(nowIso) - Date.parse(source.as_of);
  if (!Number.isFinite(deltaMs)) return source;
  return {
    ...source,
    as_of: shift(source.as_of, deltaMs),
    built_as_of: source.as_of,
    cases: source.cases.map((item) => ({
      ...item,
      opened_at: shift(item.opened_at, deltaMs),
      seller_response_due_date: shift(item.seller_response_due_date, deltaMs),
      delivered_at: shift(item.delivered_at, deltaMs),
      time_evidence: item.time_evidence ? {
        ...item.time_evidence,
        events: item.time_evidence.events.map((event) => ({ ...event, at: shift(event.at, deltaMs) })),
      } : item.time_evidence,
    })),
  };
}

// "Proof of delivery on file" means an accepted attachment backs the fulfilment requirement.
// A seller-provided delivery time without an attachment is shown, but does not count as one.
export function hasDeliveryAttachment(caseRow) {
  return caseRow.requirements.some((row) => row.evidence_type === 'FULFILLMENT' && row.accepted_attachment_count > 0);
}

export function caseRows(source) {
  return source.cases.map((item) => {
    const daysToDue = daysBetween(source.as_of, item.seller_response_due_date);
    const flags = item.time_evidence?.flags || [];
    return {
      case_ref: item.case_ref,
      order_ref: item.order_ref,
      reason: label(item.reason),
      lifecycle_stage: label(item.lifecycle_stage),
      readiness: label(item.overall_state),
      due_date: item.seller_response_due_date,
      days_to_due: daysToDue,
      due_window: daysToDue <= DUE_SOON_DAYS ? `Due within ${DUE_SOON_DAYS} days` : `Due after ${DUE_SOON_DAYS} days`,
      delivery_proof: hasDeliveryAttachment(item) ? 'Attachment on file' : 'No attachment on file',
      carrier_status: label(item.carrier_status),
      delivered_at: item.delivered_at,
      time_flag_count: flags.length,
      review_flag: item.review_reasons.length ? item.review_reasons.map(label).join('; ') : 'None',
      submission: label(item.provider_submission),
    };
  });
}

export function requirementRows(source) {
  return source.cases.flatMap((item) => item.requirements.map((row, index) => ({
    requirement_id: `${item.case_ref}-req-${index + 1}`,
    case_ref: item.case_ref,
    evidence_type: label(row.provider_evidence_type),
    state: label(row.requirement_state),
    mandatory: row.mandatory ? 'Mandatory' : 'Optional',
    proof_count: row.proof_count,
    attachment_count: row.accepted_attachment_count,
  })));
}

export function timeEventRows(source) {
  return source.cases.flatMap((item) => (item.time_evidence?.events || []).map((event, index, list) => ({
    event_id: `${item.case_ref}-event-${index + 1}`,
    case_ref: item.case_ref,
    order: index + 1,
    event: event.kind === 'MESSAGE' ? `${label('MESSAGE')} · ${label(event.topic)}` : label(event.kind),
    at: event.at,
    source: label(event.source),
    gap_hours: index === 0 ? null : Math.round((Date.parse(event.at) - Date.parse(list[index - 1].at)) / 3600000 * 10) / 10,
  })));
}

export function benchmarkRows(source) {
  return source.flows.map((flow) => ({
    flow_id: flow.id,
    flow: flow.label,
    model_calls: flow.model_calls,
    rounds: flow.rounds,
    wrong_honest: flow.wrong_honest,
    wrong_careless: flow.wrong_careless,
  }));
}

export function receiptRows(source) {
  return source.receipts.map((row, index) => ({
    receipt_id: `channel3-${index + 1}`,
    query: row.query,
    called_at: row.called_at,
    http_status: row.http_status,
    result_status: label(row.result_status),
    cards: row.cards,
    latency_seconds: row.latency_seconds,
  }));
}

const text = (id, name, extra = {}) => ({ id, name, format: 'textFormat', ...extra });
const integer = (id, name) => ({ id, name, format: 'integerFormat' });
// Times in UTC like the deadline tile ("Nov 3, 12:00 UTC"), not the viewer's local zone; decimals to one place.
const UTC_TIME = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC', timeZoneName: 'short' });
const ONE_PLACE = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 });
const decimal = (id, name) => ({ id, name, format: 'decimalFormat', formatOptions: { format: ONE_PLACE } });
const dateTime = (id, name) => ({ id, name, format: 'dateTimeFormat', formatOptions: { format: UTC_TIME } });

// AG Studio data definition: five tables, two of them related to cases so a click on a case
// in one widget cross-filters the requirement and time-event widgets.
export function studioData({ disputes, benchmark, receipts }) {
  return {
    description: 'PayGuard AI synthetic dispute evidence readiness. Read only: nothing here decides a dispute or submits to PayPal.',
    sources: [
      {
        id: 'cases', name: 'Dispute cases', description: `Synthetic dispute cases as of ${disputes.as_of}.`, data: caseRows(disputes),
        fields: [text('case_ref', 'Case'), text('order_ref', 'Order'), text('reason', 'Reason'), text('lifecycle_stage', 'Stage'),
          text('readiness', 'Readiness'), dateTime('due_date', 'Seller response due'), decimal('days_to_due', 'Days to due'),
          text('due_window', 'Due window'), text('delivery_proof', 'Delivery proof'), text('carrier_status', 'Carrier status'),
          dateTime('delivered_at', 'Delivered at'), integer('time_flag_count', 'Time flags'), text('review_flag', 'Review flag'),
          text('submission', 'Submission')],
      },
      {
        id: 'requirements', name: 'Requested evidence', description: 'Evidence the synthetic provider snapshot requests per case.', data: requirementRows(disputes),
        fields: [text('requirement_id', 'Requirement', { hide: true }), text('case_ref', 'Case'), text('evidence_type', 'Evidence type'),
          text('state', 'State'), text('mandatory', 'Mandatory'), integer('proof_count', 'Proof records'), integer('attachment_count', 'Accepted attachments')],
      },
      {
        id: 'time_events', name: 'Time evidence', description: 'Ordered time events (synthetic, seller-provided unless stated).', data: timeEventRows(disputes),
        fields: [text('event_id', 'Event id', { hide: true }), text('case_ref', 'Case'), integer('order', 'Order'), text('event', 'Event'),
          dateTime('at', 'Time'), text('source', 'Source'), decimal('gap_hours', 'Hours since previous')],
      },
      {
        id: 'benchmark', name: 'Guide benchmark', description: benchmark.source, data: benchmarkRows(benchmark),
        fields: [text('flow_id', 'Flow id', { hide: true }), text('flow', 'Flow'), integer('model_calls', 'Model calls'), integer('rounds', 'Rounds'),
          integer('wrong_honest', 'Wrong (honest seller)'), integer('wrong_careless', 'Wrong (careless seller)')],
      },
      {
        id: 'receipts', name: 'Channel3 receipts', description: 'Recorded Channel3 product searches (docs/evidence/channel3_receipts_v1.json).', data: receiptRows(receipts),
        fields: [text('receipt_id', 'Receipt', { hide: true }), text('query', 'Query'), dateTime('called_at', 'Called at'), integer('http_status', 'HTTP status'),
          text('result_status', 'Result'), integer('cards', 'Cards'), decimal('latency_seconds', 'Latency (s)')],
      },
    ],
    relationships: [
      { id: 'requirements-case', source: { tableId: 'requirements', fieldId: 'case_ref' }, target: { tableId: 'cases', fieldId: 'case_ref' }, type: 'many-to-one' },
      { id: 'time-events-case', source: { tableId: 'time_events', fieldId: 'case_ref' }, target: { tableId: 'cases', fieldId: 'case_ref' }, type: 'many-to-one' },
    ],
  };
}

export const DATA_FILES = Object.freeze([
  'frontend/src/data/dashboard_disputes_v1.json',
  'frontend/src/data/guide_benchmark_v1.json',
  'frontend/src/data/channel3_receipts_v1.json',
]);
