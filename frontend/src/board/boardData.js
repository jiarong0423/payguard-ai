// Pure mapping for the evidence deadline board in step 03. Input is only what the console
// already holds: state.disputes (each case carries opened_at and seller_response_due_date), the
// dispute drafts it has fetched (routing.requirements, time_evidence, evidence) and the current time.
// The case data alone draws the response window, the due line, the now line and the plan bar; a
// draft only adds readiness and its evidence events. No Bryntum import here, so it runs in plain Node.
import { operatorLabel } from '../operatorLabels.js';
import { viewPresetFor } from '../optional/timelineModel.js';
import { displayDisputeId } from '../disputeDisplay.js';

export const DUE_SOON_DAYS = 3;
// (N1 B, D-C21/PF5, 2026-11-12) The board reads in the viewer's own time zone, like the rest of the console
// (dateTimeLabel, "GMT+8"): Bryntum lays out real Dates in local time, so the axis, the bars and the labels share one zone.
// It replaces the UTC wall clock (fields of a UTC time read as local), which put the board 8 hours off the case head.
export function boardWall(value) {
  const date = value instanceof Date ? new Date(value.getTime()) : new Date(value ?? '');
  return Number.isNaN(date.getTime()) ? null : date;
}
const HOUR = 3600 * 1000;
const DAY = 24 * HOUR;
const PRESENT = 'STRUCTURALLY_PRESENT';
const MISSING = new Set(['MANDATORY_EVIDENCE_MISSING', 'OPTIONAL_EVIDENCE_MISSING']);
const TIME_KINDS = new Set(['PAYMENT', 'ORDER_RECORD_CREATED', 'DELIVERY', 'MESSAGE', 'CLAIM_OPENED']);
const EVENT_COLORS = { PAYMENT: 'teal', ORDER_RECORD_CREATED: 'indigo', DELIVERY: 'green', MESSAGE: 'gray', CLAIM_OPENED: 'orange' };
const WINDOW_COLORS = { DUE_SOON_MISSING: 'red', DUE_SOON_NO_DRAFT: 'red', PAST_DUE: 'red', DUE_SOON: 'amber', OPEN: 'blue' };

// Highlighted on the board and counted in its summary (r20 UX-2).
export const URGENT = new Set(['DUE_SOON_MISSING', 'DUE_SOON_NO_DRAFT']);

export const BOARD_STATUS_LABELS = {
  NO_DUE_DATE: 'No response due date in the case data',
  PAST_DUE: 'Past the response due date',
  DUE_SOON_MISSING: `Due within ${DUE_SOON_DAYS} days · evidence missing`,
  DUE_SOON_NO_DRAFT: `Due within ${DUE_SOON_DAYS} days · no draft yet`,
  DUE_SOON: `Due within ${DUE_SOON_DAYS} days`,
  OPEN: 'Response window open',
  NOT_AWAITING_SELLER: 'PayPal is not waiting for the seller',
};

// Bryntum's own wording for this board (its hackathon idea list, quoted in the J4 sponsor review of 2026-11-10):
// "Dispute triage board (Scheduler)" with "disputed amount, response deadline, and evidence readiness".
// (N1 C06, 2026-11-12) Plain subtitle under the "Evidence deadline board" title (external review: subtitle, not a new title).
export const TRIAGE_CAPTION = 'Each case: amount, deadline, evidence';
export const UNSCHEDULED_LABEL = 'Deadline set · no evidence slot scheduled';

// (2026-11-10) Short text for the scheduler's narrow left grid, so a Sandbox row never wraps past its row height
// ("PayPal: Waiting for seller response" took four lines and was clipped). The cards keep the full wording.
const GRID_PAYPAL_STATUS = { WAITING_FOR_SELLER_RESPONSE: 'Waiting: seller', WAITING_FOR_BUYER_RESPONSE: 'Waiting: buyer', UNDER_REVIEW: 'Under review' };
export const GRID_TEXT_MAX = 16;
const GRID_REASON = { 'Item or service not received': 'Not received', 'Item or service not as described': 'Not as described' };
export const gridReasonLabel = (reason) => GRID_REASON[reason] || String(reason ?? '');
export function gridEvidenceLabel(row) {
  if (row?.source !== 'sandbox') return row?.readinessLabel ?? '';
  const status = String(row.readinessLabel || '').replace(/^PayPal: /u, '');
  const raw = Object.entries(GRID_PAYPAL_STATUS).find(([, label]) => operatorLabel(label) === status)?.[1];
  return GRID_PAYPAL_STATUS[row.providerStatus] || raw || status;
}

// (2026-11-10) Live PayPal Sandbox disputes as board rows: the list read the console already made (GET /paypal/disputes,
// source paypal_sandbox; hosted ids are masked codes). Only the projected summary fields are used. Sandbox rows get no
// automatic plan: a deadline without a scheduled evidence slot is shown as such until the seller adds one.
export function sandboxCases(items) {
  if (!Array.isArray(items)) return [];
  return items.filter((row) => row && typeof row.dispute_id === 'string').map((row) => ({
    case_ref: row.dispute_id, reason: row.reason, status: row.status, providerStatus: row.status,
    dispute_amount: row.dispute_amount, seller_response_due_date: row.seller_response_due_date ?? null,
    opened_at: row.create_time, source: 'sandbox',
  }));
}

function instant(value) {
  if (typeof value !== 'string') return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : null;
}

// present / required count only requirements the local matrix can judge; the rest need manual review.
export function readinessOf(draft) {
  const rows = Array.isArray(draft?.routing?.requirements) ? draft.routing.requirements : null;
  if (!rows) return null;
  const present = rows.filter((row) => row?.requirement_state === PRESENT).length;
  const missing = rows.filter((row) => MISSING.has(row?.requirement_state)).length;
  const mandatoryMissing = rows.filter((row) => row?.requirement_state === 'MANDATORY_EVIDENCE_MISSING').length;
  return { present, missing, mandatoryMissing, required: present + missing, manual: rows.length - present - missing };
}

// The synthetic case summaries carry dispute_amount in the PayPal Disputes shape (synthetic values).
export function amountOf(dispute) {
  const money = dispute?.dispute_amount;
  if (money && typeof money.value === 'string' && typeof money.currency_code === 'string') return `${money.value} ${money.currency_code}`;
  if (typeof dispute?.amount === 'string' && typeof dispute?.currency === 'string') return `${dispute.amount} ${dispute.currency}`;
  return null;
}

export function boardStatus({ dueMs, readiness, nowMs, hasDraft }) {
  // The due date comes from the case queue (r16), so no case waits for a draft to show how close it is (evloop: a
  // judge read the board as empty before any draft). Only a case with no usable date has no window.
  if (dueMs === null) return 'NO_DUE_DATE';
  const left = dueMs - nowMs;
  if (left < 0) return 'PAST_DUE';
  // A case with no draft has no evidence checked yet: it is flagged like missing evidence, not "Due within 3 days"
  // alone (r20 UX-2: the summary said nothing was missing while two cards read "No draft yet").
  if (left <= DUE_SOON_DAYS * DAY) {
    if (!hasDraft) return 'DUE_SOON_NO_DRAFT';
    return readiness && readiness.missing > 0 ? 'DUE_SOON_MISSING' : 'DUE_SOON';
  }
  return 'OPEN';
}

function timeEvidenceName(event) {
  if (event.kind === 'MESSAGE') return `${operatorLabel('MESSAGE')} · ${operatorLabel(event.topic)}`;
  return operatorLabel(event.kind);
}

// Evidence events for one case: the draft's time evidence when present, otherwise the
// draft's order / delivery / opened timestamps, otherwise the case's opened_at alone.
function evidenceEvents(dispute, draft) {
  if (Array.isArray(draft?.time_evidence?.events)) {
    return draft.time_evidence.events
      .filter((event) => event && TIME_KINDS.has(event.kind) && instant(event.at) !== null)
      .map((event) => ({ kind: event.kind, at: event.at, name: timeEvidenceName(event), source: operatorLabel(event.source) }));
  }
  if (draft?.evidence) {
    const source = operatorLabel(draft.evidence.evidence_source, 'Synthetic');
    return [
      ['ORDER_RECORD_CREATED', draft.evidence.order_created_at, 'Order created'],
      ['DELIVERY', draft.evidence.delivered_at, 'Delivery event'],
      ['CLAIM_OPENED', draft.evidence.opened_at, operatorLabel('CLAIM_OPENED')],
    ].filter(([, at]) => instant(at) !== null).map(([kind, at, name]) => ({ kind, at, name, source }));
  }
  return instant(dispute.opened_at) === null ? [] : [{ kind: 'CLAIM_OPENED', at: dispute.opened_at, name: operatorLabel('CLAIM_OPENED'), source: 'Case queue' }];
}

// One row per dispute case in state.disputes. `drafts` maps case_ref to a draft the console fetched.
export function buildEvidenceBoard({ disputes, drafts = {}, now, sandbox = null }) {
  const live = sandboxCases(sandbox);
  const cases = [...live, ...(Array.isArray(disputes) ? disputes : [])];
  if (cases.length === 0) return null;
  const nowMs = now instanceof Date ? now.getTime() : Number(now);
  if (!Number.isFinite(nowMs)) return null;
  const rows = [];
  const events = [];
  cases.forEach((dispute) => {
    if (!dispute || typeof dispute.case_ref !== 'string') return;
    const fromSandbox = dispute.source === 'sandbox';
    // A draft held for a case the backend lists as not drafted is stale (for example after a reset).
    const candidate = fromSandbox ? null : drafts[dispute.case_ref];
    const draft = candidate && candidate.case_ref === dispute.case_ref && dispute.status !== 'needs_review' ? candidate : null;
    const readiness = draft ? readinessOf(draft) : null;
    // Case data first: the queue's seller_response_due_date; a draft's routing copy only when the queue has none.
    const dueAt = instant(dispute.seller_response_due_date) !== null ? dispute.seller_response_due_date : (draft?.routing?.seller_response_due_date ?? null);
    const dueMs = instant(dueAt);
    // A Sandbox dispute has no local draft; its readiness is PayPal's own status (evidence goes only while it waits).
    const status = fromSandbox && dispute.providerStatus !== 'WAITING_FOR_SELLER_RESPONSE' && dueMs !== null ? 'NOT_AWAITING_SELLER'
      : boardStatus({ dueMs, readiness, nowMs, hasDraft: fromSandbox || Boolean(draft) });
    const id = dispute.case_ref;
    const caseEvents = evidenceEvents(dispute, draft);
    caseEvents.forEach((event, index) => {
      const at = boardWall(event.at);
        // Case data stays read only on the board: only the seller's own plan bar can move (optimise r24).
      events.push({
        id: `${id}-evidence-${index}`, resourceId: id, name: event.name, startDate: at, endDate: at,
        kind: event.kind, at: event.at, source: event.source, eventColor: EVENT_COLORS[event.kind], cls: 'payguard-board-milestone',
        draggable: false, resizable: false,
      });
    });
    const openedAt = draft?.evidence?.opened_at ?? dispute.opened_at;
    const openedMs = instant(openedAt);
    if (dueMs !== null && openedMs !== null && dueMs > openedMs) {
      events.push({
        id: `${id}-window`, resourceId: id, name: 'Response window', startDate: boardWall(openedAt), endDate: boardWall(dueAt),
        kind: 'RESPONSE_WINDOW', at: dueAt, source: fromSandbox ? 'PayPal Sandbox · seller response due date' : draft ? operatorLabel(draft.routing?.due_state) : 'Case queue · no draft yet', eventColor: WINDOW_COLORS[status] || 'blue', cls: `payguard-board-window payguard-board-window-${status.toLowerCase()}`,
        draggable: false, resizable: false,
      });
    }
    rows.push({
      id,
      name: id,
      caseRef: id,
      // (2026-11-11) Display only: a Sandbox row's id is a dispute id and goes through the one display mapping; the row id,
      // the plan keys and every lookup keep the true value.
      caseRefShown: fromSandbox ? displayDisputeId(id) : id,
      orderRef: typeof dispute.order_ref === 'string' ? dispute.order_ref : null,
      reason: operatorLabel(dispute.reason),
      caseStatus: operatorLabel(dispute.status),
      amount: amountOf(dispute),
      dueAt,
      dueState: draft?.routing?.due_state ?? null,
      readiness,
      readinessLabel: fromSandbox ? `PayPal: ${operatorLabel(dispute.providerStatus)}` : readiness ? (readiness.required ? `${readiness.present}/${readiness.required} present` : 'No tracked items') : 'No draft yet',
      source: fromSandbox ? 'sandbox' : 'synthetic',
      providerStatus: fromSandbox ? dispute.providerStatus : null,
      autoPlan: !fromSandbox,
      status,
      statusLabel: BOARD_STATUS_LABELS[status],
      highlight: URGENT.has(status),
      eventCount: caseEvents.length,
      cls: URGENT.has(status) ? 'payguard-board-urgent' : '',
    });
  });
  if (rows.length === 0) return null;
  // Default view: from the earliest evidence event to the latest due date (every row's due date, even
  // one without a window bar), with "now" included so the remaining window is visible. Local time
  // like the events.
  const nowWall = boardWall(new Date(nowMs).toISOString()).getTime();
  const dueTimes = rows.filter((row) => instant(row.dueAt) !== null).map((row) => boardWall(row.dueAt).getTime());
  // Lines in the TimeRanges shape (zero-length range = a line): "now" across every row and each case's response
  // due date on its own row. Bryntum's TimeRanges feature is not in the Community tier (8.0.0 README, features per
  // tier), so EvidenceBoard draws these with the Community coordinate API (optimise r24).
  const timeRanges = [
    { id: 'now', kind: 'NOW', name: 'Now', resourceId: null, at: new Date(nowMs).toISOString(), startDate: new Date(nowWall) },
    ...rows.filter((row) => instant(row.dueAt) !== null).map((row) => ({
      id: `${row.id}-due`, kind: 'DUE', name: `${row.caseRefShown} response due`, resourceId: row.id, at: row.dueAt, startDate: boardWall(row.dueAt),
    })),
  ];
  const times = [nowWall, ...dueTimes, ...events.flatMap((event) => [event.startDate.getTime(), event.endDate.getTime()])];
  const first = Math.min(...times);
  const last = Math.max(...times);
  const span = Math.max(last - first, HOUR);
  const pad = Math.max(span * 0.08, HOUR);
  return {
    rows,
    events,
    timeRanges,
    nowMs,
    nowIso: new Date(nowMs).toISOString(),
    startDate: new Date(first - pad),
    endDate: new Date(last + pad),
    // The unpadded span the view must contain, for checks: earliest event or now, latest due date or event.
    fit: { first: new Date(first), last: new Date(last), latestDue: dueTimes.length ? new Date(Math.max(...dueTimes)) : null },
    // A deadline board reads in days: hour ticks squeezed into one box overlap, so short spans still show days.
    viewPreset: span <= 21 * 24 * 3600 * 1000 ? 'dayAndWeek' : viewPresetFor(span),
    highlighted: rows.filter((row) => row.highlight).map((row) => row.id),
    missingSoon: rows.filter((row) => row.status === 'DUE_SOON_MISSING').length,
    noDraftSoon: rows.filter((row) => row.status === 'DUE_SOON_NO_DRAFT').length,
  };
}

// ---------------------------------------------------------------------------------------------------------------
// Evidence collection plan (optimise r24). One "Collect evidence" bar per case that the seller may move or resize
// inside the case's response window, from now to the due date, in whole hours. It is a planning aid only: it lives
// in the page and in this tab's sessionStorage, is never sent to the backend or PayPal, and never changes case data.
// The check below is the board's own client-side check against data it already holds (now, seller_response_due_date).

export const PLAN_STORAGE_KEY = 'payguard.board.plan.v1';
export const PLAN_SCHEMA = 'payguard.board_plan.v1';
export const PLAN_DEFAULT_HOURS = 24;
export const PLAN_NAME = 'Collect evidence';
export const PLAN_MESSAGES = {
  INVALID: 'Not a valid time.',
  NOT_ON_HOUR: 'Plans snap to whole hours.',
  EMPTY: 'Keep at least one hour.',
  BEFORE_NOW: 'Cannot start before now.',
  AFTER_DUE: 'Needs to end by the response due date.',
  NO_WINDOW: 'No time left before the due date.',
};

export const floorHour = (ms) => Math.floor(ms / HOUR) * HOUR;
export const ceilHour = (ms) => Math.ceil(ms / HOUR) * HOUR;

// Inverse of boardWall: Bryntum hands back real local Dates, so the instant is the Date's own time.
export function wallToUtcMs(date) {
  if (!(date instanceof Date) || Number.isNaN(date.getTime())) return Number.NaN;
  return date.getTime();
}
const wallOfMs = (ms) => boardWall(new Date(ms).toISOString());

// The hours a plan may use: from the next whole hour after now to the last whole hour at or before the due date.
export function planWindowOf(row, nowMs) {
  const dueMs = instant(row?.dueAt);
  if (dueMs === null || !Number.isFinite(nowMs)) return null;
  const startMs = ceilHour(nowMs);
  const endMs = floorHour(dueMs);
  return endMs - startMs >= HOUR ? { startMs, endMs, dueMs } : null;
}

// { valid, code, message }. Refuses a plan that starts before now or ends after the due date.
export function validatePlan(plan, { nowMs, dueMs }) {
  const startMs = Number(plan?.startMs);
  const endMs = Number(plan?.endMs);
  const refuse = (code) => ({ valid: false, code, message: PLAN_MESSAGES[code] });
  if (!Number.isFinite(startMs) || !Number.isFinite(endMs) || !Number.isFinite(dueMs)) return refuse('INVALID');
  if (startMs % HOUR !== 0 || endMs % HOUR !== 0) return refuse('NOT_ON_HOUR');
  if (endMs - startMs < HOUR) return refuse('EMPTY');
  if (Number.isFinite(nowMs) && startMs < nowMs) return refuse('BEFORE_NOW');
  if (endMs > dueMs) return refuse('AFTER_DUE');
  return { valid: true, code: 'OK', message: '' };
}

export function defaultPlan(window) {
  if (!window) return null;
  return { startMs: window.startMs, endMs: Math.min(window.startMs + PLAN_DEFAULT_HOURS * HOUR, window.endMs) };
}

// Moves (or, with resize, stretches the end of) a plan by whole hours; returns the proposal, not yet checked.
export function shiftPlan(plan, hours, { resize = false } = {}) {
  const delta = Math.trunc(hours) * HOUR;
  return resize ? { startMs: plan.startMs, endMs: plan.endMs + delta } : { startMs: plan.startMs + delta, endMs: plan.endMs + delta };
}

// One plan per case with time left: a stored plan that still passes the check, otherwise the default.
export function restorePlans(stored, rows, nowMs) {
  const plans = {};
  for (const row of rows || []) {
    const window = planWindowOf(row, nowMs);
    if (!window) continue;
    const kept = stored?.[row.id];
    const candidate = kept && { startMs: Date.parse(kept.start), endMs: Date.parse(kept.end) };
    if (candidate && validatePlan(candidate, { nowMs, dueMs: window.dueMs }).valid) plans[row.id] = candidate;
    else if (row.autoPlan !== false) plans[row.id] = defaultPlan(window);
  }
  return plans;
}

// Rows with a response deadline and time left but no evidence slot scheduled (Sandbox rows until the seller adds one).
export function unscheduledRows(rows, plans, nowMs) {
  return (rows || []).filter((row) => row.status !== 'NOT_AWAITING_SELLER' && !plans?.[row.id] && planWindowOf(row, nowMs));
}

// The Bryntum events for the plan bars, in the same wall-clock frame as the read-only events.
export function planEvents(rows, plans) {
  return (rows || []).filter((row) => plans?.[row.id]).map((row) => ({
    id: `${row.id}-plan`, resourceId: row.id, name: PLAN_NAME, kind: 'PLAN', at: row.dueAt, source: 'Your plan · this tab only',
    startDate: wallOfMs(plans[row.id].startMs), endDate: wallOfMs(plans[row.id].endMs),
    draggable: true, resizable: true, eventColor: 'indigo', cls: 'payguard-board-plan',
  }));
}

export function readStoredPlans(storage) {
  try {
    const parsed = JSON.parse(storage?.getItem(PLAN_STORAGE_KEY) ?? 'null');
    if (!parsed || parsed.schema !== PLAN_SCHEMA || typeof parsed.plans !== 'object' || parsed.plans === null) return {};
    const plans = {};
    for (const [ref, value] of Object.entries(parsed.plans)) {
      if (typeof ref === 'string' && typeof value?.start === 'string' && typeof value?.end === 'string') plans[ref] = { start: value.start, end: value.end };
    }
    return plans;
  } catch {
    return {};
  }
}

// Holds only case refs and two times per case; returns false when the tab refuses storage (private mode, quota).
export function writeStoredPlans(storage, plans) {
  try {
    const out = {};
    for (const [ref, plan] of Object.entries(plans || {})) out[ref] = { start: new Date(plan.startMs).toISOString(), end: new Date(plan.endMs).toISOString() };
    storage?.setItem(PLAN_STORAGE_KEY, JSON.stringify({ schema: PLAN_SCHEMA, plans: out }));
    return Boolean(storage);
  } catch {
    return false;
  }
}

// "Download my plan (.ics)": the seller's own "Collect evidence" bars as a calendar file (RFC 5545), built in the page.
// One VEVENT per case, UTC times, CRLF line ends. Only the case reference and the planned hours: no name, e-mail or
// amount, and nothing is sent anywhere.
export const PLAN_ICS_NAME = 'tradeglot-evidence-plan.ics';
export const PLAN_ICS_EMPTY_REASON = 'No plan yet: a case with time left gets a Collect evidence bar to download.';
const icsTime = (ms) => new Date(ms).toISOString().replace(/[-:]/gu, '').replace(/\.\d{3}Z$/u, 'Z');
const icsText = (text) => String(text).replace(/\\/gu, '\\\\').replace(/;/gu, '\;').replace(/,/gu, '\\,').replace(/\r?\n/gu, '\\n');
export function plansToIcs(plans, { now = Date.now() } = {}) {
  const entries = Object.entries(plans || {}).filter(([, plan]) => Number.isFinite(plan?.startMs) && Number.isFinite(plan?.endMs) && plan.endMs > plan.startMs);
  if (!entries.length) return null;
  const stamp = icsTime(now instanceof Date ? now.getTime() : Number(now));
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//TradeGlot demo//Evidence plan//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
  for (const [ref, plan] of entries.sort(([a], [b]) => (a < b ? -1 : 1))) {
    lines.push('BEGIN:VEVENT', `UID:${icsText(ref)}-plan@tradeglot.invalid`, `DTSTAMP:${stamp}`, `DTSTART:${icsTime(plan.startMs)}`, `DTEND:${icsTime(plan.endMs)}`,
      `SUMMARY:${icsText(`Collect evidence for ${ref}`)}`, 'DESCRIPTION:Planning aid from the TradeGlot demo. Not sent to PayPal.', 'END:VEVENT');
  }
  lines.push('END:VCALENDAR');
  return `${lines.join('\r\n')}\r\n`;
}

// Quick classify and highlight on the deadline board (2026-11-09): "tight" is a response window that is past due or due within
// DUE_SOON_DAYS days, whatever the evidence state; the rest are open. Pure helpers; Bryntum only restyles the bars.
export const TIGHT_STATUSES = new Set(['PAST_DUE', 'DUE_SOON', 'DUE_SOON_MISSING', 'DUE_SOON_NO_DRAFT']);
export const isTight = (row) => TIGHT_STATUSES.has(row?.status);
export const URGENCY_CHIPS = Object.freeze([['all', 'All cases'], ['tight', `Due within ${DUE_SOON_DAYS} days or past due`], ['open', 'Open window']]);
export function urgencyCounts(rows) {
  const list = Array.isArray(rows) ? rows : [];
  const tight = list.filter(isTight).length;
  return { all: list.length, tight, open: list.length - tight };
}
// Extra class names for one bar: it glows when "Highlight tight deadlines" is on and its case is tight, and it is dimmed
// when a chip other than All is chosen and its case is not in that group.
export function barClasses(row, { focus = 'all', glow = false } = {}) {
  const out = [];
  if (glow && isTight(row)) out.push('payguard-board-glow');
  if (focus === 'tight' && !isTight(row)) out.push('payguard-board-dim');
  if (focus === 'open' && isTight(row)) out.push('payguard-board-dim');
  return out.join(' ');
}
