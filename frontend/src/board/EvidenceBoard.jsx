// Evidence deadline board for step 03: one row per dispute case, its evidence events and the
// seller response window on a Bryntum Scheduler (MIT Community tier), with a plain list
// that carries the same facts and stays readable on a phone. Loaded with React.lazy from App.jsx.
//
// (optimise r24) The case data stays read only. On top of it the seller gets one "Collect evidence" bar per case
// that can be dragged or resized inside the response window, in whole hours, from now to the due date. A drop
// that starts before now or ends after the due date snaps back with a short message. The plan is a planning aid:
// it stays in this page and this tab's sessionStorage and is never sent to the backend or PayPal. The check is
// the board's own client-side check against data it already holds (now and seller_response_due_date).
import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { BryntumScheduler, available } from 'virtual:payguard-optional-timeline';
import {
  DUE_SOON_DAYS, PLAN_MESSAGES, PLAN_NAME, buildEvidenceBoard, defaultPlan, planEvents, planWindowOf, readStoredPlans,
  restorePlans, shiftPlan, URGENCY_CHIPS, urgencyCounts, barClasses, plansToIcs, PLAN_ICS_NAME, PLAN_ICS_EMPTY_REASON, validatePlan, wallToUtcMs, writeStoredPlans,
  TRIAGE_CAPTION, UNSCHEDULED_LABEL, unscheduledRows, gridEvidenceLabel, gridReasonLabel, isTight,
} from './boardData.js';
import { utcWallClock } from '../optional/timelineModel.js';
import './board.css';

// (2026-11-10) Two lines in the Case cell (code, then reason) fit this height at the board's 14px text.
// (2026-11-10 redesign) Every row is the same height and holds two fixed lanes (board.css): case events and the response
// window on lane 1, the seller's Collect evidence plan on lane 2. Bryntum does not stack (eventLayout none), so a row with
// more bars is not taller than a row with one. The phone timeline keeps Bryntum's stacked rows (one narrow column).
const ROW_HEIGHT = 44;
// (2026-11-10 redesign) The board is one tool on the page, not the whole page: past this many rows the timeline keeps a fixed
// height and scrolls inside its own box (the header stays in view).
// On a short laptop screen (under 800px tall) four rows, so the whole board still fits one screen (red team R2 P0-2).
// (external review 2026-11-10 #7) Read on every resize, not once at import: a rotated tablet or a resized window updates it.
const visibleRowsNow = () => (typeof window !== 'undefined' && window.innerHeight < 800 ? 4 : 6);
function subscribeResize(onChange) {
  if (typeof window === 'undefined') return () => {};
  window.addEventListener('resize', onChange);
  return () => window.removeEventListener('resize', onChange);
}
const TIMELINE_HEADER = 58;

function utcLabel(iso) {
  const date = new Date(iso ?? '');
  if (Number.isNaN(date.getTime())) return '—';
  return `${date.toLocaleString('en-US', { month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}
const msLabel = (ms) => utcLabel(new Date(ms).toISOString());
const wallLabel = (date) => msLabel(wallToUtcMs(date));
const wallOf = (ms) => utcWallClock(new Date(ms).toISOString());
const planLabel = (plan) => (plan ? `${msLabel(plan.startMs)} → ${msLabel(plan.endMs)}` : '—');

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}

// sessionStorage may throw (blocked site data); the plan then lives in the page only.
function tabStorage() {
  try { return typeof window === 'undefined' ? null : window.sessionStorage; } catch { return null; }
}

// Everything that could change case data or open an editor stays off. Drag and resize are on, but only the plan
// bars are draggable/resizable (the data events carry draggable: false, resizable: false) and the validators refuse
// anything else (optimise r24).
const LOCKED_FEATURES = {
  cellEditFeature: false, cellMenuFeature: false, columnReorderFeature: false, dependenciesFeature: false,
  eventDragCreateFeature: false, eventEditFeature: false, eventMenuFeature: false,
  headerMenuFeature: false, resourceMenuFeature: false, scheduleMenuFeature: false,
  scheduleTooltipFeature: false, timeAxisHeaderMenuFeature: false,
};
const HOUR_RESOLUTION = { unit: 'hour', increment: 1 };

const COLUMNS = [
  // Case code on line 1 and the reason on line 2, both escaped here (htmlEncode is off only for this cell's two spans).
  // (2026-11-10 redesign) Compact one-line rows, like the order table: the case code alone (the reason is its title), and
  // columns wide enough that no cell wraps to a second line.
  { text: 'Case', field: 'name', width: 200, htmlEncode: false, renderer: ({ record }) => `<span class="board-grid-case" title="${escapeHtml(String(record.get('reasonFull') ?? ''))}"><strong>${escapeHtml(String(record.get('caseRef') ?? ''))}</strong></span>` },
  { text: 'Due', field: 'dueText', width: 180, htmlEncode: true },
  { text: 'Evidence', field: 'gridEvidence', width: 140, htmlEncode: true },
  { text: 'Amount', field: 'amountText', width: 128, htmlEncode: true },
];
// (external review 2026-11-10 #1) Tablet widths (641-1100px): four locked columns (650px) left the time axis about 40px
// wide, so no bar showed. Case and Due only; the cards above carry evidence and amount.
const MID_COLUMNS = [{ ...COLUMNS[0], width: 200 }, { ...COLUMNS[1], width: 172 }];
const MID_QUERY = '(min-width: 641px) and (max-width: 1100px)';
const midMedia = () => (typeof window !== 'undefined' && typeof window.matchMedia === 'function' ? window.matchMedia(MID_QUERY) : null);
function subscribeMid(onChange) {
  const media = midMedia();
  if (!media) return () => {};
  media.addEventListener('change', onChange);
  return () => media.removeEventListener('change', onChange);
}
const isMid = () => Boolean(midMedia()?.matches);
// (fix F3 D-C5) Narrowest board box that still takes the four desktop columns (648px) plus a readable time axis.
const DESKTOP_MIN_BOX = 1100;

// Phones (phone r3 P2 #9): the list above already carries due, evidence and amount, so the timeline keeps one narrow
// Case column. Bryntum scrolls only the time axis sideways and the locked Case column stays in view, instead of the
// whole board sliding away with the case names.
// (2026-11-10) Wide enough for a masked Sandbox code (PP-R-XXX-XXXX1234) at the board's 14px text.
// (phone fix 2026-11-10) The shared "PP-R-" prefix is dropped on the phone so the code fits one line at larger system
// text sizes; the full code is the cell's title.
// (2026-11-11) caseRef here is the shown code (displayDisputeId for a Sandbox row); the prefix is kept when only "…" would remain.
const PHONE_COLUMNS = [{ text: 'Case', field: 'caseRef', width: 160, htmlEncode: false, renderer: ({ record }) => { const ref = String(record.get('caseRef') ?? ''); return `<span title="${escapeHtml(ref)}">${escapeHtml(ref.replace(/^PP-R-(?!…)/u, ''))}</span>`; } }];
const PHONE_QUERY = '(max-width: 640px)';
const phoneMedia = () => (typeof window !== 'undefined' && typeof window.matchMedia === 'function' ? window.matchMedia(PHONE_QUERY) : null);
function subscribePhone(onChange) {
  const media = phoneMedia();
  if (!media) return () => {};
  media.addEventListener('change', onChange);
  return () => media.removeEventListener('change', onChange);
}
const isPhone = () => Boolean(phoneMedia()?.matches);

// Spread before the fixed props; switching between the two remounts the scheduler (board-canvas key).
// A bar whose width encodes a short time span cannot show a long name: the label is a block that ends in an ellipsis (the
// full name stays in the tooltip). The bar width itself is never changed.
// The full name is also the label's title, so a short bar that ends in "…" still shows it on hover.
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// (2026-11-10) A plan bar names its day ("Collect evidence · Nov 10"): a few-hour slot at week scale is narrow, so the bar
// has a minimum width in board.css and never shows as an empty box. The dates are wall-clock UTC fields (utcWallClock).
// Milestones carry a short label inside their diamond (the full name is the title and the tooltip).
const MILESTONE_SHORT = { CLAIM_OPENED: 'Claim', ORDER_RECORD_CREATED: 'Order', DELIVERY: 'Delivered', PAYMENT: 'Paid', MESSAGE: 'Message' };
const eventLabel = (eventRecord) => {
  const name = String(eventRecord.name ?? '');
  const short = MILESTONE_SHORT[eventRecord.get('kind')];
  if (short) return short;
  const start = eventRecord.startDate;
  return eventRecord.get('kind') === 'PLAN' && start instanceof Date && !Number.isNaN(start.getTime())
    ? `${name} · ${MONTHS[start.getMonth()]} ${start.getDate()}` : name;
};
// (external review 2026-11-10 #2) On the one-line desktop rows a milestone is its diamond only: several milestones close
// together ("C", "Del", "Claim") overlapped each other and the window label. The name is the diamond's tooltip and title.
const desktopEventRenderer = ({ eventRecord }) => {
  // (external review 2026-11-10 #2) A short response window at month scale cannot hold its name, and the name running on
  // past the bar crossed the due line: the bar is named in the legend above and in its tooltip instead.
  if (eventRecord.get('kind') === 'RESPONSE_WINDOW') return `<span class="ev-label ev-label-window" title="${escapeHtml(String(eventRecord.name ?? ''))}"></span>`;
  if (MILESTONE_SHORT[eventRecord.get('kind')]) return `<span class="ev-label ev-label-milestone" title="${escapeHtml(String(eventRecord.name ?? ''))}"></span>`;
  const label = escapeHtml(eventLabel(eventRecord));
  const full = eventRecord.get('kind') === 'PLAN' ? label : escapeHtml(String(eventRecord.name ?? ''));
  return `<span class="ev-label" title="${full}">${label}</span>`;
};
const DESKTOP_SCHEDULER = { columns: COLUMNS, forceFit: true, eventRenderer: desktopEventRenderer };
const MID_SCHEDULER = { columns: MID_COLUMNS, forceFit: true, eventRenderer: desktopEventRenderer };
// (phone fix 2026-11-10) Same bar labels as the desktop: stacked phone rows were uneven (64 to 229px) and cut every label.
const PHONE_SCHEDULER = { columns: PHONE_COLUMNS, forceFit: false, tickSize: 72, eventRenderer: desktopEventRenderer };
// (fix F3, coordinator ruling 2026-11-12) A phone box under PHONE_NARROW_BOX: the Case column is 112px and the code wraps at
// its hyphens on two lines (board.css .board-case-wrap), never cut with an ellipsis, so the time axis gets 160px or more.
const PHONE_NARROW_BOX = 480;
const PHONE_NARROW_SCHEDULER = { ...PHONE_SCHEDULER, columns: [{ ...PHONE_COLUMNS[0], width: 112, cellCls: 'board-case-wrap' }] };

// Tooltips name the case, its due date and, for the plan bar, the planned window (optimise r24).
function tooltipHtml(eventRecord, dueAtOf, shownOf) {
  const kind = eventRecord.get('kind');
  const caseRef = String(eventRecord.resourceId ?? '');
  const due = dueAtOf(caseRef);
  const lines = [`<strong>${escapeHtml(eventRecord.name)} · ${escapeHtml(shownOf(caseRef))}</strong>`];
  if (kind === 'PLAN') {
    lines.push(`Due ${escapeHtml(utcLabel(due))}`, `Planned ${escapeHtml(wallLabel(eventRecord.startDate))} → ${escapeHtml(wallLabel(eventRecord.endDate))}`, 'Your plan · this tab only, not sent');
  } else if (kind === 'RESPONSE_WINDOW') {
    lines.push(`Due ${escapeHtml(utcLabel(eventRecord.get('at')))}`, escapeHtml(eventRecord.get('source') || ''));
  } else {
    lines.push(escapeHtml(utcLabel(eventRecord.get('at'))), `Due ${escapeHtml(utcLabel(due))}`, escapeHtml(eventRecord.get('source') || ''));
  }
  return lines.join('<br>');
}

// "Now" and due-date lines in the TimeRanges shape, drawn with the Community coordinate API because the TimeRanges
// feature is Business tier (optimise r24). The layer sits under the bars and ignores the pointer; the caption legend
// names the two line styles and the list carries the same times as text.
function drawTimeRanges(scheduler, ranges) {
  const host = scheduler?.timeAxisSubGridElement;
  if (!host || scheduler.isDestroyed) return;
  let layer = host.querySelector(':scope > .payguard-board-lines');
  if (!layer) {
    layer = document.createElement('div');
    layer.className = 'payguard-board-lines';
    layer.setAttribute('aria-hidden', 'true');
    host.appendChild(layer);
  }
  const lines = [];
  for (const range of ranges) {
    const x = scheduler.getCoordinateFromDate(range.startDate, true);
    if (!Number.isFinite(x) || x < 0) continue;
    const line = document.createElement('div');
    line.className = `payguard-board-line payguard-board-line-${range.kind.toLowerCase()}`;
    line.dataset.lineId = range.id;
    line.style.left = `${Math.round(x)}px`;
    if (range.resourceId) {
      const resource = scheduler.resourceStore.getById(range.resourceId);
      const row = resource && scheduler.getRowFor(resource);
      if (!row) continue;
      line.style.top = `${row.top}px`;
      line.style.height = `${row.height}px`;
    }
    lines.push(line);
  }
  layer.replaceChildren(...lines);
  // (external review 2026-11-10, "Dec 202") A header label cut by the axis end is hidden instead of showing "Dec 202".
  // Only visibility changes: Bryntum reuses header cells while scrolling, so the text itself is never rewritten.
  const edge = scheduler.timeAxisSubGridElement?.getBoundingClientRect().right ?? Infinity;
  scheduler.element?.querySelectorAll('.b-sch-header-time-axis-cell > .b-sch-header-text').forEach((text) => {
    text.style.visibility = '';
    const box = text.getBoundingClientRect();
    if (box.width && box.right > Math.min(edge, text.parentElement.getBoundingClientRect().right) - 2) text.style.visibility = 'hidden';
  });
}

// (external review 2026-11-10 #4) Short card status, so a card never ends a line in "…"; the full wording is the title.
const CARD_STATUS_SHORT = {
  NO_DUE_DATE: 'No due date', PAST_DUE: 'Past due', DUE_SOON_MISSING: `Due in ${DUE_SOON_DAYS} days · evidence missing`,
  DUE_SOON_NO_DRAFT: `Due in ${DUE_SOON_DAYS} days · no draft`, DUE_SOON: `Due within ${DUE_SOON_DAYS} days`, OPEN: 'Window open',
  NOT_AWAITING_SELLER: 'Not waiting for seller',
};
// (external review 2026-11-10 #8) One order for the cards and the timeline: a chip filters both, and the highlight puts
// the tight cases first, soonest due first.
function orderedRows(rows, focus, glow) {
  const list = focus === 'tight' ? rows.filter(isTight) : focus === 'open' ? rows.filter((row) => !isTight(row)) : rows;
  if (!glow) return list;
  const due = (row) => { const ms = Date.parse(row.dueAt ?? ''); return Number.isNaN(ms) ? Infinity : ms; };
  return [...list.filter(isTight).sort((a, b) => due(a) - due(b)), ...list.filter((row) => !isTight(row))];
}

function BoardList({ rows, plans, unscheduled, onSchedule, listRef }) {
  return <ul ref={listRef} className="board-list" data-testid="evidence-board-list">{rows.map((row) => <li key={row.id} className={`board-row board-row-${row.status.toLowerCase()}${row.highlight ? ' board-row-urgent' : ''}${unscheduled.has(row.id) ? ' board-row-unscheduled' : ''}${!plans[row.id] && !unscheduled.has(row.id) ? ' board-row-noplan' : ''}`} data-testid="evidence-board-row" data-status={row.status} data-source={row.source}>
    <div className="board-row-head"><strong>{row.caseRefShown}</strong>{row.source === 'sandbox' && <span className="board-row-source" data-testid="evidence-board-sandbox-tag">PayPal Sandbox</span>}<span className="board-row-status" title={row.statusLabel}>{CARD_STATUS_SHORT[row.status] || row.statusLabel}</span></div>
    <dl><div title={row.reason}><dt>Reason</dt><dd>{gridReasonLabel(row.reason)}</dd></div><div><dt>Due</dt><dd>{row.dueAt ? utcLabel(row.dueAt) : '—'}</dd></div><div title={row.readinessLabel}><dt>Evidence</dt><dd>{gridEvidenceLabel(row)}{row.readiness?.manual ? ` · ${row.readiness.manual} need manual review` : ''}</dd></div><div><dt>Amount</dt><dd>{row.amount ? (row.source === 'sandbox' ? `${row.amount} · Sandbox` : `${row.amount} · synthetic`) : 'Not in case data'}</dd></div>
      <div><dt>Plan</dt><dd data-testid="evidence-board-plan">{plans[row.id] ? `${PLAN_NAME} ${planLabel(plans[row.id])}` : unscheduled.has(row.id) ? <><strong className="board-unscheduled" data-testid="evidence-board-unscheduled" title={UNSCHEDULED_LABEL}>No evidence slot yet</strong> <button type="button" className="board-plan-reset" data-testid="evidence-board-schedule" onClick={() => onSchedule(row)}>Schedule a slot</button></> : row.source === 'sandbox' && row.providerStatus && row.providerStatus !== 'WAITING_FOR_SELLER_RESPONSE' ? 'Not waiting for the seller.' : row.dueAt ? PLAN_MESSAGES.NO_WINDOW : '—'}</dd></div></dl>
  </li>)}</ul>;
}

export default function EvidenceBoard({ disputes, drafts, sandbox = null }) {
  // "Now" is taken when the inputs change; the board does not tick on its own. The plan check uses the live clock.
  // `sandbox`: the console's live PayPal Sandbox dispute list (null when it holds sample data only).
  const board = useMemo(() => buildEvidenceBoard({ disputes, drafts, sandbox, now: Date.now() }), [disputes, drafts, sandbox]);
  const phone = useSyncExternalStore(subscribePhone, isPhone, () => false);
  const midViewport = useSyncExternalStore(subscribeMid, isMid, () => false);
  // (fix F3 D-C5) The board's own box, not the viewport, picks the desktop layout: inside the step's fold a 1440 window gives
  // the board about 660px, and the four desktop columns (648px) on an 880px canvas left the time axis 228px behind a
  // sideways scroll. Below DESKTOP_MIN_BOX the two-column fitted layout is used, so the axis is in view.
  const boxRef = useRef(null);
  const [boxWidth, setBoxWidth] = useState(0);
  const mid = midViewport || (boxWidth > 0 && boxWidth < DESKTOP_MIN_BOX);
  const phoneNarrow = phone && boxWidth > 0 && boxWidth < PHONE_NARROW_BOX;
  const VISIBLE_ROWS = useSyncExternalStore(subscribeResize, visibleRowsNow, () => 6);
  const schedulerRef = useRef(null);
  // Plans restored for this board: a stored plan that still fits, otherwise the default (optimise r24).
  const restored = useMemo(() => (board ? restorePlans(readStoredPlans(tabStorage()), board.rows, board.nowMs) : {}), [board]);
  const [plans, setPlans] = useState(restored);
  const plansRef = useRef(restored);
  const verdictRef = useRef(null);
  const [message, setMessage] = useState('');
  const lastCls = useRef({});
  const [focus, setFocus] = useState('all');
  const [glow, setGlow] = useState(false);
  useEffect(() => {
    plansRef.current = restored;
    setPlans(restored);
    if (board) writeStoredPlans(tabStorage(), restored);
  }, [board, restored]);

  const dueAtById = useMemo(() => Object.fromEntries((board?.rows || []).map((row) => [row.id, row.dueAt])), [board]);
  const dueRef = useRef(dueAtById);
  dueRef.current = dueAtById;
  const dueAtOf = useCallback((ref) => dueRef.current[ref] ?? null, []);
  // (2026-11-11) What a message or tooltip shows for a row id (the shown code); the id itself stays the key.
  const shownById = useMemo(() => Object.fromEntries((board?.rows || []).map((row) => [row.id, row.caseRefShown])), [board]);
  const shownRef = useRef(shownById);
  shownRef.current = shownById;
  const shownOf = useCallback((ref) => shownRef.current[ref] ?? String(ref), []);

  const resources = useMemo(() => (board?.rows || []).map((row) => ({
    id: row.id, name: `${row.caseRefShown} · ${row.reason}`, caseRef: row.caseRefShown, reasonText: gridReasonLabel(row.reason), reasonFull: row.reason, cls: row.cls,
    dueText: row.dueAt ? utcLabel(row.dueAt) : 'No due date', readinessLabel: row.readinessLabel, gridEvidence: gridEvidenceLabel(row), amountText: row.amount ?? '—',
  })), [board]);
  // The events reach Bryntum once per board; later moves live in Bryntum's own store and in `plans`.
  const events = useMemo(() => (board ? [...board.events, ...planEvents(board.rows, restored)] : []), [board, restored]);

  // One check for drag, resize and keys: only a plan bar, in its own row, from now to its due date, whole hours.
  const judge = useCallback((record, startDate, endDate, newResource) => {
    let verdict;
    if (record?.get?.('kind') !== 'PLAN') verdict = { valid: false, code: 'READ_ONLY', message: 'Case data is read only.' };
    else if (newResource && newResource.id !== record.resourceId) verdict = { valid: false, code: 'OTHER_CASE', message: 'A plan stays on its own case.' };
    else verdict = validatePlan({ startMs: wallToUtcMs(startDate), endMs: wallToUtcMs(endDate) }, { nowMs: Date.now(), dueMs: Date.parse(dueRef.current[record.resourceId] ?? '') });
    verdictRef.current = verdict;
    return verdict;
  }, []);

  const keep = useCallback((ref, plan, note) => {
    const next = { ...plansRef.current, [ref]: plan };
    plansRef.current = next;
    setPlans(next);
    const stored = writeStoredPlans(tabStorage(), next);
    setMessage(`${shownOf(ref)}: ${PLAN_NAME.toLowerCase()} ${planLabel(plan)}${note ? ` ${note}` : ''}. ${stored ? 'Kept in this tab only' : 'Kept in this page only'}, not sent.`);
  }, [shownOf]);

  // Applies Bryntum's result once more through the same check; anything that slipped through is put back.
  const commit = useCallback((record) => {
    if (!record || record.get('kind') !== 'PLAN') return;
    const ref = String(record.resourceId);
    const previous = plansRef.current[ref];
    const verdict = judge(record, record.startDate, record.endDate, null);
    if (!verdict.valid) {
      if (previous) record.setStartEndDate(wallOf(previous.startMs), wallOf(previous.endMs));
      setMessage(`${shownOf(ref)}: moved back. ${verdict.message}`);
      return;
    }
    const plan = { startMs: wallToUtcMs(record.startDate), endMs: wallToUtcMs(record.endDate) };
    if (previous && previous.startMs === plan.startMs && previous.endMs === plan.endMs) return;
    keep(ref, plan);
  }, [judge, keep, shownOf]);

  // A refused drop snaps back with the reason from this gesture's last check. The verdict is cleared when a gesture
  // starts, so a click on a handle that changes nothing shows no stale reason.
  const refused = useCallback((record) => {
    if (!record || record.get?.('kind') !== 'PLAN') return;
    const verdict = verdictRef.current;
    if (verdict && !verdict.valid) setMessage(`${shownOf(String(record.resourceId))}: moved back. ${verdict.message}`);
  }, [shownOf]);
  const gestureStart = useCallback(() => { verdictRef.current = null; }, []);

  const dragFeature = useMemo(() => ({
    constrainDragToResource: true,
    validatorFn: ({ eventRecords, startDate, endDate, newResource }) => {
      const verdict = (eventRecords || []).length === 1 ? judge(eventRecords[0], startDate, endDate, newResource) : { valid: false, message: 'Move one plan at a time.' };
      return verdict.valid ? true : { valid: false, message: verdict.message };
    },
  }), [judge]);
  const resizeFeature = useMemo(() => ({
    // The 8.0.0 resize context names the bar eventRecord (the typings say record); both are accepted.
    validatorFn: ({ eventRecord, record, startDate, endDate }) => {
      const verdict = judge(eventRecord ?? record, startDate, endDate, null);
      return verdict.valid ? true : { valid: false, message: verdict.message };
    },
  }), [judge]);
  const tooltipFeature = useMemo(() => ({ template: ({ eventRecord }) => tooltipHtml(eventRecord, dueAtOf, shownOf) }), [dueAtOf, shownOf]);

  const onAfterEventDrop = useCallback(({ valid, eventRecords }) => {
    if (valid) (eventRecords || []).forEach(commit);
    else refused(eventRecords?.[0]);
  }, [commit, refused]);
  const onEventResizeEnd = useCallback(({ changed, eventRecord }) => {
    if (changed) commit(eventRecord);
    else refused(eventRecord);
  }, [commit, refused]);

  // Keyboard: Tab and the arrow keys reach the bars through Bryntum's own event navigation. On a focused plan bar
  // Shift+Left/Right moves it one hour and Alt+Left/Right moves its end one hour, through the same check. The keys are
  // taken in the capture phase, before the navigator would also move focus to the neighbouring event (optimise r24).
  const onPlanKey = useCallback((scheduler, event) => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key) || !(event.shiftKey || event.altKey) || event.ctrlKey || event.metaKey) return;
    const record = event.target?.closest?.('.b-sch-event-wrap') ? scheduler.resolveEventRecord(event.target) : null;
    if (!record || record.get('kind') !== 'PLAN') return;
    event.preventDefault();
    event.stopPropagation();
    const ref = String(record.resourceId);
    const current = plansRef.current[ref];
    if (!current) return;
    const proposal = shiftPlan(current, event.key === 'ArrowRight' ? 1 : -1, { resize: event.altKey && !event.shiftKey });
    const verdict = judge(record, wallOf(proposal.startMs), wallOf(proposal.endMs), null);
    if (!verdict.valid) {
      setMessage(`${shownOf(ref)}: not moved. ${verdict.message}`);
      return;
    }
    record.setStartEndDate(wallOf(proposal.startMs), wallOf(proposal.endMs));
    keep(ref, proposal);
  }, [judge, keep, shownOf]);

  // "Download my plan (.ics)": built here from the plans in this tab; no request, no personal data.
  const downloadPlan = useCallback(() => {
    const text = plansToIcs(plansRef.current);
    if (!text || typeof document === 'undefined') return;
    const url = URL.createObjectURL(new Blob([text], { type: 'text/calendar;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url; link.download = PLAN_ICS_NAME;
    document.body.appendChild(link); link.click(); link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    setMessage('Plan downloaded as a calendar file. It was made in this page and not sent anywhere.');
  }, []);
  // A Sandbox row's first evidence slot: the default plan, added to Bryntum's store as a movable bar.
  const schedule = useCallback((row) => {
    const plan = defaultPlan(planWindowOf(row, Date.now()));
    if (!plan) { setMessage(`${row.caseRefShown ?? row.id}: ${PLAN_MESSAGES.NO_WINDOW}`); return; }
    const store = schedulerRef.current?.instance?.eventStore;
    if (store && !store.getById(`${row.id}-plan`)) store.add(planEvents([row], { [row.id]: plan }));
    keep(row.id, plan, 'scheduled');
  }, [keep]);
  const resetPlans = useCallback(() => {
    if (!board) return;
    const next = {};
    const store = schedulerRef.current?.instance?.eventStore;
    for (const row of board.rows) {
      // Sandbox rows go back to "no evidence slot scheduled"; the sample cases get the default plan again.
      if (row.autoPlan === false) { const bar = store?.getById(`${row.id}-plan`); if (bar) store.remove(bar); continue; }
      const plan = defaultPlan(planWindowOf(row, Date.now()));
      if (plan) next[row.id] = plan;
    }
    for (const [ref, plan] of Object.entries(next)) store?.getById(`${ref}-plan`)?.setStartEndDate(wallOf(plan.startMs), wallOf(plan.endMs));
    plansRef.current = next;
    setPlans(next);
    writeStoredPlans(tabStorage(), next);
    setMessage('Plans reset to the next 24 hours (or up to the due date).');
  }, [board]);

  // Draw "now" and due lines whenever the scheduler lays out its rows or time axis; take the plan keys.
  const schedulerKey = board ? `${board.startDate.getTime()}-${board.endDate.getTime()}-${board.viewPreset}` : 'none';
  useEffect(() => {
    const scheduler = schedulerRef.current?.instance;
    if (!scheduler || !board) return undefined;
    let frame = 0;
    const redraw = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => drawTimeRanges(scheduler, board.timeRanges));
    };
    const detachScheduler = scheduler.on({ paint: redraw, renderRows: redraw, timelineViewportResize: redraw, timeAxisChange: redraw, horizontalScroll: redraw });
    const detachStore = scheduler.eventStore.on({ change: redraw });
    const keydown = (event) => onPlanKey(scheduler, event);
    scheduler.element?.addEventListener('keydown', keydown, true);
    redraw();
    return () => {
      cancelAnimationFrame(frame);
      scheduler.element?.removeEventListener('keydown', keydown, true);
      if (typeof detachScheduler === 'function') detachScheduler();
      if (typeof detachStore === 'function') detachStore();
    };
  }, [board, phone, mid, phoneNarrow, schedulerKey, onPlanKey]);

  // (defect D2) On a phone the axis starts at the oldest event, so the Collect evidence bars sat off-screen: bring the
  // earliest plan bar into view once the scheduler is laid out. Display only; nothing in the data or the plan changes.
  useEffect(() => {
    const scheduler = schedulerRef.current?.instance;
    // (click-through 2026-11-10) Tablets too: the two-column timeline opened at the axis start with the bars off to the right.
    if (!scheduler || !board || !(phone || mid)) return undefined;
    const first = events.filter((event) => event.kind === 'PLAN' && event.startDate).map((event) => event.startDate).sort((x, y) => x - y)[0];
    if (!first) return undefined;
    let frame = 0;
    const timer = setTimeout(() => {
      frame = requestAnimationFrame(() => {
        try { if (!scheduler.isDestroyed) scheduler.scrollToDate(first, { block: 'start', edgeOffset: 8, animate: false }); } catch { /* scroll position is cosmetic */ }
      });
    }, 0);
    return () => { clearTimeout(timer); cancelAnimationFrame(frame); };
  }, [board, events, phone, mid, phoneNarrow, schedulerKey]);

  // Quick classify and highlight: Bryntum's own event styling (a record's cls); case data and the plan are not touched.
  useEffect(() => {
    const scheduler = schedulerRef.current?.instance;
    if (!scheduler || !board) return undefined;
    const rowById = Object.fromEntries(board.rows.map((row) => [row.id, row]));
    if (lastCls.current.scheduler !== scheduler) lastCls.current = { scheduler };
    const baseCls = Object.fromEntries(events.map((event) => [event.id, event.cls || '']));
    {
      scheduler.eventStore.forEach((record) => {
        // The class names the event was created with, plus the classes this chip state asks for (assigned as one string).
        // A plan bar added after the board was built (Schedule a slot) is not in `events`: it keeps its own class, so a chip
        // never strips the lane and the label from it (red team 2026-11-10 P0).
        // (recording 2026-11-10) The timeline now shows only the chip's cases, so nothing is dimmed (a dimmed class stayed
        // on after Reset); the highlight glow still applies. The class string is assigned every time.
        const next = `${baseCls[record.id] ?? (record.get('kind') === 'PLAN' ? 'payguard-board-plan' : '')} ${barClasses(rowById[record.resourceId], { focus: 'all', glow })}`.trim();
        lastCls.current[record.id] = next; record.cls = next;
      });
    }
    return undefined;
  }, [board, events, focus, glow, schedulerKey, phone, mid, phoneNarrow]);

  // (final red team C P1) A quick filter shows only its cases on the timeline, and the highlight puts the tight cases on top,
  // so the matching rows are always in the six visible rows instead of greyed out below the fold. Case data is unchanged.
  const listRows = useMemo(() => orderedRows(board?.rows || [], focus, glow), [board, focus, glow]);
  const timelineResources = useMemo(() => {
    const byId = Object.fromEntries(resources.map((resource) => [resource.id, resource]));
    return listRows.map((row) => byId[row.id]).filter(Boolean);
  }, [resources, listRows]);
  // (recording 2026-11-10) The timeline keeps one resource store: a chip filters and sorts it with Bryntum's own store
  // filter and sorter. Swapping the resources prop on every chip left a blank timeline (no bars, rows drawn on top of each
  // other) after Reset.
  useEffect(() => {
    const store = schedulerRef.current?.instance?.resourceStore;
    if (!store || store.isDestroyed) return;
    const index = Object.fromEntries(listRows.map((row, i) => [row.id, i]));
    try {
      store.clearFilters();
      if (focus !== 'all') store.filter({ id: 'payguard-focus', filterBy: (record) => record.id in index });
      store.sort({ fn: (a, b) => (index[a.id] ?? 1e6) - (index[b.id] ?? 1e6) });
    } catch { /* order is cosmetic; the cards above carry the same filter */ }
  }, [listRows, focus, schedulerKey, phone, mid, phoneNarrow]);
  // The card strip starts at its first card whenever the filter or the order changes (it kept an old scroll offset and
  // showed the end of the list after Reset).
  const listRef = useRef(null);
  useEffect(() => { const list = listRef.current; if (list) list.scrollLeft = 0; }, [focus, glow]);
  // (fix F3 D-C5, OFFICIAL_FIX_GUIDE s5) Watch the board's box: it is measured once the fold opens and again when the fold or
  // the page column changes width. A change of layout remounts the scheduler (board-canvas key); a width change inside one
  // layout calls refresh() so the fitted time axis (forceFit) is laid out again at the new width.
  const hasBoard = Boolean(board);
  useEffect(() => {
    const box = boxRef.current;
    if (!box || typeof ResizeObserver === 'undefined') return undefined;
    const observer = new ResizeObserver((entries) => {
      const width = Math.round(entries[0]?.contentRect?.width || 0);
      setBoxWidth((previous) => (Math.abs(previous - width) > 1 ? width : previous));
    });
    observer.observe(box);
    return () => observer.disconnect();
  }, [hasBoard]);
  useEffect(() => {
    const scheduler = schedulerRef.current?.instance;
    if (!scheduler || !boxWidth) return undefined;
    const frame = requestAnimationFrame(() => {
      try { if (!scheduler.isDestroyed) scheduler.refresh(); } catch { /* layout refresh is cosmetic */ }
    });
    return () => cancelAnimationFrame(frame);
  }, [boxWidth]);
  if (!board) return <p className="board-empty" data-testid="evidence-board-empty">Load the dispute case to see its evidence and response window.</p>;
  // Missing evidence and "no draft yet" are counted apart, so the summary never says none while a card reads "No draft yet" (r20 UX-2).
  const soon = [board.missingSoon && `${board.missingSoon} due within ${DUE_SOON_DAYS} days with evidence missing`, board.noDraftSoon && `${board.noDraftSoon} due within ${DUE_SOON_DAYS} days with no draft yet`].filter(Boolean);
  const timeline = available && BryntumScheduler;
  const unscheduled = new Set(unscheduledRows(board.rows, plans, Date.now()).map((row) => row.id));
  const liveRows = board.rows.filter((row) => row.source === 'sandbox').length;
  return <div ref={boxRef} className="evidence-board" data-testid="evidence-board">
    <p className="board-triage" data-testid="evidence-board-triage">{TRIAGE_CAPTION}{liveRows ? ` · ${liveRows} from the PayPal Sandbox dispute list` : ' · sample cases'}</p>
    <p className="board-summary" data-testid="evidence-board-summary">{board.rows.length} case{board.rows.length === 1 ? '' : 's'} · {soon.length ? soon.join(' · ') : `none due within ${DUE_SOON_DAYS} days with evidence missing or no draft`}{unscheduled.size ? ` · ${unscheduled.size} with a deadline but no evidence slot scheduled` : ''} · now {utcLabel(board.nowIso)}{board.rows.length > 2 ? ' · scroll the cards sideways for more →' : ''}</p>
    <BoardList listRef={listRef} rows={listRows} plans={plans} unscheduled={unscheduled} onSchedule={schedule} />
    {timeline ? <figure className={`board-timeline${phone ? ' board-timeline-phone' : mid ? ' board-timeline-fit' : ''}`} data-testid="evidence-board-timeline">
      <figcaption title="Bars are the seller response window up to the due date. Bryntum Scheduler Community (MIT).">
        Times in UTC · case data read only · bars: response window and your Collect evidence plan · <span className="board-legend-now">now</span> and <span className="board-legend-due">due</span> lines{phone && <span className="board-swipe-hint" data-testid="evidence-board-swipe-hint"> · swipe the timeline sideways →</span>}
      </figcaption>
      <p className="board-plan-help" id="evidence-board-plan-help" data-testid="evidence-board-plan-help">
        Drag or resize each <strong>{PLAN_NAME}</strong> bar to plan when you will gather the proof, in whole hours, between now and the due date.
        With a bar focused (Tab, then the arrow keys), Shift+←/→ moves it one hour and Alt+←/→ moves its end.
      </p>
      <div className="board-chips" role="group" aria-label="Quick classify cases by urgency" data-testid="evidence-board-urgency">
        {URGENCY_CHIPS.map(([key, label]) => <button key={key} type="button" aria-pressed={focus === key} data-testid={`evidence-board-urgency-${key}`} onClick={() => setFocus(key)}>{label} <span>{urgencyCounts(board.rows)[key]}</span></button>)}
        <button type="button" aria-pressed={glow} data-testid="evidence-board-glow" onClick={() => setGlow((on) => !on)}>Highlight tight deadlines</button>
        <button type="button" data-testid="evidence-board-urgency-reset" disabled={focus === 'all' && !glow} onClick={() => { setFocus('all'); setGlow(false); }}>Reset</button>
      </div>
      <div className="board-plan-bar">
        <p className="board-plan-message" role="status" aria-live="polite" data-testid="evidence-board-plan-message" title={message}>{message}</p>
        <button type="button" className="board-plan-reset" data-testid="evidence-board-plan-reset" onClick={resetPlans}>Reset plans</button>
        <button type="button" className="board-plan-reset board-plan-download" data-testid="evidence-board-plan-ics" disabled={!Object.keys(plans).length} aria-describedby="evidence-board-plan-ics-note" onClick={downloadPlan}>Download my plan (.ics)</button>
        <small id="evidence-board-plan-ics-note" className="board-plan-ics-note" data-testid="evidence-board-plan-ics-note">{Object.keys(plans).length ? 'A calendar file of your Collect evidence bars.' : PLAN_ICS_EMPTY_REASON}</small>
      </div>
      <div className="board-scroll" tabIndex={0} role="region" aria-label="Evidence deadline timeline, scrolls sideways" aria-describedby="evidence-board-plan-help">
        {/* Keyed on the layout too: a phone and a desktop scheduler differ in columns and fit, so a fresh one is made. */}
        <div className="board-canvas" key={phone ? (phoneNarrow ? 'phone-narrow' : 'phone') : mid ? 'mid' : 'desktop'}>
          {/* Keyed on the range: when a newly prepared draft widens it, a fresh scheduler takes start and end
              together. Updating the two props one by one let Bryntum keep the old span, so the axis ended
              before the latest response-window bar. */}
          <BryntumScheduler key={`${board.startDate.getTime()}-${board.endDate.getTime()}-${board.viewPreset}`} ref={schedulerRef} {...(phone ? (phoneNarrow ? PHONE_NARROW_SCHEDULER : PHONE_SCHEDULER) : mid ? MID_SCHEDULER : DESKTOP_SCHEDULER)} autoHeight={timelineResources.length <= VISIBLE_ROWS} height={timelineResources.length > VISIBLE_ROWS ? VISIBLE_ROWS * ROW_HEIGHT + TIMELINE_HEADER : undefined} rowHeight={ROW_HEIGHT} barMargin={3} eventLayout="none" startDate={board.startDate} endDate={board.endDate} viewPreset={board.viewPreset}
            snap timeResolution={HOUR_RESOLUTION} enableDeleteKey={false}
            detectCSSCompatibilityIssues={false} useInitialAnimation={false} zoomOnMouseWheel={false} zoomOnTimeAxisDoubleClick={false}
            milestoneLayoutMode="estimate" milestoneTextPosition="outside" resources={resources} events={events}
            eventDragFeature={dragFeature} eventResizeFeature={resizeFeature} eventTooltipFeature={tooltipFeature} {...LOCKED_FEATURES}
            onEventDragStart={gestureStart} onEventResizeStart={gestureStart} onAfterEventDrop={onAfterEventDrop} onEventResizeEnd={onEventResizeEnd} />
        </div>
      </div>
    </figure> : null}
  </div>;
}
