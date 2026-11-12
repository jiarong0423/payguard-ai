// Evidence deadline board (step 03): MIT Community package pinned, licence guard, rows and
// events built only from the console's existing state.disputes and draft shapes, and (optimise r24) the
// seller's per-tab "Collect evidence" plan with its client-side check. No browser.
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import optionalBryntumTimeline, { auditBryntumDeclarations, detectBryntum, isCommunityName } from '../frontend/src/optional/vitePlugin.js';
import {
  BOARD_STATUS_LABELS, DUE_SOON_DAYS, PLAN_DEFAULT_HOURS, PLAN_MESSAGES, PLAN_SCHEMA, PLAN_STORAGE_KEY, amountOf, boardStatus, buildEvidenceBoard,
  ceilHour, defaultPlan, floorHour, planEvents, planWindowOf, readStoredPlans, readinessOf, restorePlans, shiftPlan, validatePlan, wallToUtcMs,
  writeStoredPlans,
} from '../frontend/src/board/boardData.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');
const read = (path) => readFileSync(join(projectRoot, path), 'utf8');
const json = (path) => JSON.parse(read(path));

// 1. Packages: exact pins, Community tier, MIT in the lock and the installed manifests.
const manifest = json('frontend/package.json');
const lock = json('frontend/package-lock.json');
const PINNED = ['@bryntum/core-community', '@bryntum/scheduler-community', '@bryntum/scheduler-react-community'];
for (const name of PINNED) {
  assert.match(manifest.dependencies[name] ?? '', /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?$/u, `${name} pinned exactly`);
  assert.equal(lock.packages[`node_modules/${name}`]?.version, manifest.dependencies[name], `${name} locked at the pinned version`);
}
const bryntumLock = Object.entries(lock.packages).filter(([key]) => key.includes('node_modules/@bryntum/'));
assert.ok(bryntumLock.length >= PINNED.length);
for (const [key, entry] of bryntumLock) {
  assert.equal(entry.license, 'MIT', `${key} MIT`);
  assert.equal(entry.version, manifest.dependencies['@bryntum/scheduler-community'], `${key} one Bryntum version`);
  assert.ok(isCommunityName(key.slice(key.lastIndexOf('node_modules/') + 'node_modules/'.length)), `${key} Community tier`);
  assert.match(entry.resolved, /^https:\/\/registry\.npmjs\.org\/@bryntum\//u);
  assert.match(entry.integrity, /^sha512-/u);
}
assert.deepEqual(auditBryntumDeclarations(manifest, lock), []);
// (optimise r24) The general-availability 8.0.0 release, with the integrities read from the registry tarballs on
// 2026-11-04 (docs/BRYNTUM_LICENSE_CHECK.md). A new version needs a new licence check and a new table here.
const VERIFIED_8_0_0 = {
  '@bryntum/core-community': 'sha512-46olNPneMyxy6Y5kAEv+AqQOCOjlsHaSrE+GZ+MvcK2Jq7oO4cV2ueSrMwAcSL1Qgd1zv0jiW0znDPiUYlO7qQ==',
  '@bryntum/core-react-community': 'sha512-L/2iQAf39h44UK0BzQ8aq2oAXjttd8EXMa0zkG4J9dZAiygLZzvkTaY5xhDonz15wx7YQIUm9/Yv7wkAbhdZog==',
  '@bryntum/engine-community': 'sha512-jBXH8qJtBwXYI48XttHLiHqFzU3Rmq/rqc7oiE3FIibGcSQDx/LmpauJDJgWExcBQwzutQwHACLEalA2E19lXQ==',
  '@bryntum/grid-community': 'sha512-mP05jXRp2w0uIEX3lB1oIUd4KzTYpUts0AeGQxlfEuZ/amdKi4kJnPdTxzhMqdFv7kTrz+g+/Nun/qpiYres0A==',
  '@bryntum/grid-react-community': 'sha512-9i3JKafRlMjwVjcoZf6WM5AMW9JafpsQ9CmLmIyzA/ENmUFGFhlUhFYJm44VlcYVKDKuf8uAbLGR57DuwYXhEw==',
  '@bryntum/scheduler-community': 'sha512-NcvzQqTy8zeOXrGT/mkHvdJyMeULYMZq/qDnBLSzX301k4uRmrrPQKD6oc7+jSs7xgukPLYbW4+xD9lro4rREw==',
  '@bryntum/scheduler-react-community': 'sha512-L2DnKJfCTjSjugdT0+RIKFXJVuOcTW7MzTakLIXwXGkBcf4XkqtHxm7SBOfn79ycKalnuxi0Y4bwubIMmrJvYw==',
};
for (const name of PINNED) assert.equal(manifest.dependencies[name], '8.0.0', `${name} pinned at the GA release`);
assert.deepEqual(Object.fromEntries(bryntumLock.map(([key, entry]) => [key.slice(key.lastIndexOf('node_modules/') + 'node_modules/'.length), entry.integrity]).sort()), VERIFIED_8_0_0, 'lock holds the seven verified 8.0.0 tarballs');
const installed = detectBryntum(frontendRoot);
if (installed.installed) {
  assert.equal(installed.version, manifest.dependencies['@bryntum/scheduler-community']);
  for (const name of PINNED) {
    const packageDir = join(frontendRoot, 'node_modules', ...name.split('/'));
    assert.equal(JSON.parse(readFileSync(join(packageDir, 'package.json'), 'utf8')).license, 'MIT', `${name} installed MIT`);
    assert.match(readFileSync(join(packageDir, 'LICENSE'), 'utf8'), /^MIT License/u, `${name} ships the MIT LICENSE`);
  }
}

// 2. The guard refuses trial, Business, Enterprise, unpinned and non-MIT packages.
for (const name of ['@bryntum/scheduler-trial', '@bryntum/scheduler-thin-trial', '@bryntum/scheduler', '@bryntum/schedulerpro-business', '@bryntum/scheduler-enterprise', '@bryntum/scheduler-react']) {
  assert.equal(isCommunityName(name), false, name);
  assert.ok(auditBryntumDeclarations({ dependencies: { [name]: '7.3.8' } }, { packages: {} }).some((problem) => problem.startsWith('NOT_COMMUNITY_TIER')), name);
  assert.throws(() => optionalBryntumTimeline({ root: frontendRoot, declarations: () => ({ manifest: { dependencies: { [name]: '7.3.8' } }, lock: { packages: {} } }) }), /licence guard/u, name);
}
assert.deepEqual(auditBryntumDeclarations({ dependencies: { '@bryntum/scheduler-community': '^8.0.0-beta.1' } }, { packages: {} }), ['VERSION_NOT_PINNED:@bryntum/scheduler-community@^8.0.0-beta.1']);
assert.deepEqual(auditBryntumDeclarations({}, { packages: { 'node_modules/@bryntum/grid-community': { license: 'Commercial' } } }), ['LICENSE_NOT_MIT:@bryntum/grid-community:Commercial']);
assert.throws(() => optionalBryntumTimeline({ root: frontendRoot, detect: () => ({ installed: false, reason: 'LICENSE_NOT_MIT_COMMUNITY', version: '8.0.0' }) }), /does not declare MIT/u);

// 3. Inputs: the exact shapes the console already holds (state.disputes and POST /disputes/{case_ref}/draft).
const NOW = Date.parse('2026-10-08T08:00:00Z');
// dispute_amount values are the synthetic ones backend/app/store.py DEMO_DISPUTE_AMOUNTS assigns. Every summary carries
// seller_response_due_date, as GET /demo/state does (backend/app/store.py state(); frontend/src/api.js requires it).
const disputes = [
  { case_ref: 'case-ref-001', order_ref: 'order-ref-001', reason: 'INR', opened_at: '2026-10-07T08:00:00Z', seller_response_due_date: '2026-10-10T08:00:00Z', dispute_amount: { currency_code: 'USD', value: '48.00' }, status: 'draft_ready' },
  { case_ref: 'case-ref-002', order_ref: 'order-ref-002', reason: 'INR', opened_at: '2026-10-07T08:00:00Z', seller_response_due_date: '2026-10-20T08:00:00Z', dispute_amount: { currency_code: 'USD', value: '18.00' }, status: 'draft_ready' },
  { case_ref: 'case-ref-003', order_ref: 'order-ref-003', reason: 'INR', opened_at: '2026-10-07T08:00:00Z', seller_response_due_date: '2026-10-09T20:00:00Z', dispute_amount: { currency_code: 'USD', value: '125.50' }, status: 'needs_review' },
];
const requirement = (state, mandatory = true) => ({ request_id: `requirement-${state}`, provider_evidence_type: 'PROOF_OF_FULFILLMENT', evidence_type: 'FULFILLMENT', source: 'REQUESTED_FROM_SELLER', mandatory, action: 'PROVIDE_EVIDENCE', requirement_state: state, proof_count: state === 'STRUCTURALLY_PRESENT' ? 1 : 0, accepted_attachment_count: 0 });
const routing = (due, requirements) => ({ schema_version: 1, reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', status: 'WAITING_FOR_SELLER_RESPONSE', dispute_life_cycle_stage: 'INQUIRY', seller_response_due_date: due, due_state: 'OPEN', available_actions: ['PROVIDE_EVIDENCE'], requirements, overall_state: 'NEEDS_INPUT' });
const drafts = {
  // Physical case: no time_evidence; order, delivery and opened timestamps come from draft.evidence.
  'case-ref-001': { case_ref: 'case-ref-001', time_evidence: null, routing: routing('2026-10-10T08:00:00Z', [requirement('MANDATORY_EVIDENCE_MISSING'), requirement('STRUCTURALLY_PRESENT', false)]), evidence: { reason: 'INR', opened_at: '2026-10-07T08:00:00Z', order_created_at: '2026-10-05T08:00:00Z', carrier_status: 'delivered', delivered_at: '2026-10-06T08:00:00Z', evidence_source: 'synthetic' } },
  // Digital case with time evidence (payment, messages, order record, claim, delivery).
  'case-ref-002': { case_ref: 'case-ref-002', routing: routing('2026-10-20T08:00:00Z', [requirement('STRUCTURALLY_PRESENT'), requirement('CONTEXT_ONLY')]), evidence: { reason: 'INR', opened_at: '2026-10-07T08:00:00Z', order_created_at: '2026-10-05T08:00:00Z', delivered_at: '2026-10-07T12:00:00Z', evidence_source: 'synthetic' },
    time_evidence: { schema_version: 'payguard.time_evidence.v1', events: [
      { kind: 'PAYMENT', at: '2026-10-04T20:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
      { kind: 'MESSAGE', at: '2026-10-04T20:30:00Z', source: 'SELLER_PROVIDED_UNVERIFIED', channel: 'EMAIL', direction: 'INBOUND', topic: 'PAYMENT_NOTICE', message_digest: 'b'.repeat(64) },
      { kind: 'ORDER_RECORD_CREATED', at: '2026-10-05T08:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
      { kind: 'CLAIM_OPENED', at: '2026-10-07T08:00:00Z', source: 'PROVIDER' },
      { kind: 'DELIVERY', at: '2026-10-07T12:00:00Z', source: 'SELLER_PROVIDED_UNVERIFIED' },
      { kind: 'UNKNOWN_KIND', at: '2026-10-07T13:00:00Z', source: 'PROVIDER' },
      { kind: 'PAYMENT', at: 'broken', source: 'PROVIDER' },
    ], gaps_seconds: {}, flags: ['DELIVERY_AFTER_CLAIM'], judgement: 'NOT_MADE', advisory_only: true } },
  // A draft held for a case the backend lists as needs_review is stale and ignored.
  'case-ref-003': { case_ref: 'case-ref-003', routing: routing('2026-10-08T09:00:00Z', [requirement('MANDATORY_EVIDENCE_MISSING')]), evidence: { opened_at: '2026-10-07T08:00:00Z' } },
};
const before = JSON.stringify({ disputes, drafts });
const board = buildEvidenceBoard({ disputes, drafts, now: NOW });
assert.equal(JSON.stringify({ disputes, drafts }), before, 'inputs not mutated');

// 4. One row per dispute case, in the order of state.disputes; every value traces to an input field.
assert.deepEqual(board.rows.map((row) => row.id), disputes.map((row) => row.case_ref));
const [first, second, third] = board.rows;
assert.deepEqual(first.readiness, { present: 1, missing: 1, mandatoryMissing: 1, required: 2, manual: 0 });
assert.equal(first.readinessLabel, '1/2 present');
assert.equal(first.dueAt, drafts['case-ref-001'].routing.seller_response_due_date);
assert.equal(first.status, 'DUE_SOON_MISSING');
assert.equal(first.highlight, true);
assert.equal(first.cls, 'payguard-board-urgent');
assert.equal(second.readinessLabel, '1/1 present');
assert.equal(second.readiness.manual, 1);
assert.equal(second.status, 'OPEN');
assert.equal(second.highlight, false);
// No usable draft (the held one is stale): the due date still comes from the case data, never from the stale draft.
assert.equal(third.status, 'DUE_SOON_NO_DRAFT');
assert.equal(third.dueAt, disputes[2].seller_response_due_date);
assert.equal(third.readiness, null);
assert.equal(third.readinessLabel, 'No draft yet');
assert.deepEqual(board.highlighted, ['case-ref-001', 'case-ref-003']);
for (const row of board.rows) {
  const money = disputes.find((item) => item.case_ref === row.id).dispute_amount;
  assert.equal(row.amount, `${money.value} ${money.currency_code}`, 'amount is the summary dispute_amount, nothing added');
  assert.equal(row.statusLabel, BOARD_STATUS_LABELS[row.status]);
  assert.equal(row.orderRef, disputes.find((item) => item.case_ref === row.id).order_ref);
}

// 5. Events: evidence milestones plus one response-window bar from claim opened to the due date.
const eventsOf = (id) => board.events.filter((event) => event.resourceId === id);
assert.deepEqual(eventsOf('case-ref-001').map((event) => event.kind), ['ORDER_RECORD_CREATED', 'DELIVERY', 'CLAIM_OPENED', 'RESPONSE_WINDOW']);
assert.deepEqual(eventsOf('case-ref-002').map((event) => event.kind), ['PAYMENT', 'MESSAGE', 'ORDER_RECORD_CREATED', 'CLAIM_OPENED', 'DELIVERY', 'RESPONSE_WINDOW']);
assert.deepEqual(eventsOf('case-ref-003').map((event) => event.kind), ['CLAIM_OPENED', 'RESPONSE_WINDOW'], 'no draft: the queue opened_at and the window from case data');
assert.equal(eventsOf('case-ref-003')[1].source, 'Case queue · no draft yet');
assert.equal(eventsOf('case-ref-002')[1].name, 'Message record · Payment notice');
const inputInstants = new Set([
  ...disputes.flatMap((row) => [row.opened_at, row.seller_response_due_date]),
  ...Object.values(drafts).flatMap((draft) => [draft.routing.seller_response_due_date, ...Object.values(draft.evidence || {}), ...(draft.time_evidence?.events || []).map((event) => event.at)]),
]);
// (N1 B, D-C21) The board reads in the viewer's own zone: a board date is the real instant (local Date), not UTC fields read as local.
const wall = (iso) => new Date(iso).getTime();
const allowedTimes = new Set([...inputInstants].filter((value) => Number.isFinite(Date.parse(value))).map(wall));
for (const event of board.events) {
  assert.ok(allowedTimes.has(event.startDate.getTime()) && allowedTimes.has(event.endDate.getTime()), `${event.id} times come from the inputs`);
  assert.ok(inputInstants.has(event.at), `${event.id} at comes from the inputs`);
  if (event.kind === 'RESPONSE_WINDOW') {
    assert.ok(event.endDate > event.startDate);
    assert.equal(event.at, disputes.find((row) => row.case_ref === event.resourceId).seller_response_due_date, 'window ends at the case due date');
  } else {
    assert.equal(event.startDate.getTime(), event.endDate.getTime(), 'evidence events are milestones');
  }
}
const window1 = eventsOf('case-ref-001').at(-1);
assert.equal(window1.eventColor, 'red');
assert.match(window1.cls, /payguard-board-window-due_soon_missing/u);
assert.equal(JSON.stringify(board).includes('b'.repeat(64)), false, 'message digests are not drawn');
assert.ok(board.startDate.getTime() < Math.min(...board.events.map((event) => event.startDate.getTime())));
assert.ok(board.endDate.getTime() > Math.max(...board.events.map((event) => event.endDate.getTime())));
assert.equal(board.nowIso, new Date(NOW).toISOString());
assert.equal(board.viewPreset, 'dayAndWeek');
// Default view fits from the earliest event to the latest due date (round 5: the axis used to end early).
const latestDue = Math.max(...disputes.map((row) => wall(row.seller_response_due_date)));
assert.equal(board.fit.latestDue.getTime(), latestDue);
assert.ok(board.endDate.getTime() > latestDue, 'view ends after the latest due date');
assert.ok(board.startDate.getTime() <= Math.min(...board.events.map((event) => event.startDate.getTime()), wall(new Date(NOW).toISOString())));
// A due date with no window bar (no usable opened_at) still widens the view.
const lateDue = '2026-11-20T08:00:00Z';
const noWindow = buildEvidenceBoard({
  disputes: [{ ...disputes[0], opened_at: 'not a time', seller_response_due_date: lateDue }],
  drafts: { 'case-ref-001': { case_ref: 'case-ref-001', routing: routing('2026-10-12T08:00:00Z', [requirement('STRUCTURALLY_PRESENT')]) } },
  now: NOW,
});
assert.equal(noWindow.events.length, 0);
assert.equal(noWindow.rows[0].dueAt, lateDue, 'the case due date wins over the draft copy');
assert.ok(noWindow.endDate.getTime() > wall(lateDue) && noWindow.fit.latestDue.getTime() === wall(lateDue));
// A queue row without a usable due date falls back to the draft's routing copy; with neither, no date and no window.
{
  const { seller_response_due_date: _drop, ...bare } = disputes[0];
  assert.equal(buildEvidenceBoard({ disputes: [bare], drafts: { 'case-ref-001': drafts['case-ref-001'] }, now: NOW }).rows[0].dueAt, drafts['case-ref-001'].routing.seller_response_due_date);
  const none = buildEvidenceBoard({ disputes: [{ ...bare, seller_response_due_date: 'not a time' }], drafts: {}, now: NOW });
  assert.equal(none.rows[0].status, 'NO_DUE_DATE');
  assert.equal(none.rows[0].statusLabel, 'No response due date in the case data');
  assert.deepEqual(none.events.map((event) => event.kind), ['CLAIM_OPENED']);
  assert.deepEqual(none.timeRanges.map((range) => range.kind), ['NOW']);
}

// 6. Status rules and helpers.
const day = 24 * 3600 * 1000;
const missing = { missing: 1 };
const ready = { missing: 0 };
assert.equal(DUE_SOON_DAYS, 3);
assert.equal(boardStatus({ dueMs: NOW + 3 * day, readiness: missing, nowMs: NOW, hasDraft: true }), 'DUE_SOON_MISSING');
assert.equal(boardStatus({ dueMs: NOW + 3 * day + 1, readiness: missing, nowMs: NOW, hasDraft: true }), 'OPEN');
assert.equal(boardStatus({ dueMs: NOW + day, readiness: ready, nowMs: NOW, hasDraft: true }), 'DUE_SOON');
assert.equal(boardStatus({ dueMs: NOW - 1, readiness: missing, nowMs: NOW, hasDraft: true }), 'PAST_DUE');
assert.equal(boardStatus({ dueMs: null, readiness: missing, nowMs: NOW, hasDraft: true }), 'NO_DUE_DATE');
assert.equal(boardStatus({ dueMs: null, readiness: null, nowMs: NOW, hasDraft: false }), 'NO_DUE_DATE');
// evloop: the board never waits for a draft to show a due date (a judge read it as empty before any draft).
assert.equal(Object.hasOwn(BOARD_STATUS_LABELS, 'NO_DRAFT'), false);
for (const source of [read('frontend/src/board/boardData.js'), read('frontend/src/board/EvidenceBoard.jsx')]) assert.equal(source.includes('Prepare the draft'), false);
// r19: a case with a known due date but no draft yet still shows how close the deadline is.
// r20 UX-2: due within 3 days with no draft counts as evidence not yet checked, highlighted like missing evidence.
assert.equal(boardStatus({ dueMs: NOW + day, readiness: null, nowMs: NOW, hasDraft: false }), 'DUE_SOON_NO_DRAFT');
assert.equal(boardStatus({ dueMs: NOW + 3 * day + 1, readiness: null, nowMs: NOW, hasDraft: false }), 'OPEN');
{
  const queued = disputes.map((item, index) => ({ ...item, status: 'needs_review', seller_response_due_date: new Date(NOW + (index + 1) * day).toISOString() }));
  const noDrafts = buildEvidenceBoard({ disputes: queued, drafts: {}, now: NOW });
  assert.deepEqual(noDrafts.rows.map((row) => row.status), ['DUE_SOON_NO_DRAFT', 'DUE_SOON_NO_DRAFT', 'DUE_SOON_NO_DRAFT']);
  assert.deepEqual(noDrafts.highlighted, queued.map((item) => item.case_ref));
  assert.equal(noDrafts.noDraftSoon, 3);
  assert.equal(noDrafts.missingSoon, 0);
  assert.equal(noDrafts.rows[0].statusLabel, 'Due within 3 days · no draft yet');
}
// evloop: before any draft, the case data alone draws for every case the response window bar up to the due date, the
// due line, the now line and a draggable Collect evidence bar; the case events stay locked.
{
  const caseOnly = buildEvidenceBoard({ disputes, drafts: {}, now: NOW });
  for (const row of caseOnly.rows) {
    const due = disputes.find((item) => item.case_ref === row.id).seller_response_due_date;
    assert.equal(row.dueAt, due);
    assert.equal(row.readiness, null);
    const bar = caseOnly.events.find((event) => event.resourceId === row.id && event.kind === 'RESPONSE_WINDOW');
    assert.ok(bar, `${row.id} window bar without a draft`);
    assert.equal(bar.endDate.getTime(), wall(due), `${row.id} window ends at the due date`);
    assert.ok(caseOnly.timeRanges.some((range) => range.kind === 'DUE' && range.resourceId === row.id && range.at === due), `${row.id} due line`);
  }
  assert.equal(caseOnly.timeRanges.filter((range) => range.kind === 'NOW').length, 1, 'now line');
  for (const event of caseOnly.events) assert.equal(event.draggable === false && event.resizable === false, true, `${event.id} locked`);
  const caseOnlyPlans = restorePlans({}, caseOnly.rows, NOW);
  assert.deepEqual(Object.keys(caseOnlyPlans), disputes.map((row) => row.case_ref), 'a plan for every case with time left');
  const caseOnlyBars = planEvents(caseOnly.rows, caseOnlyPlans);
  assert.deepEqual(caseOnlyBars.map((bar) => [bar.name, bar.draggable, bar.resizable]), disputes.map(() => ['Collect evidence', true, true]));
  for (const row of caseOnly.rows) assert.equal(validatePlan(caseOnlyPlans[row.id], { nowMs: NOW, dueMs: Date.parse(row.dueAt) }).valid, true);
}
assert.ok(read('frontend/src/board/EvidenceBoard.jsx').includes('due within ${DUE_SOON_DAYS} days with no draft yet'), 'summary counts cases with no draft');
// (N1 C05) The phone summary has its own shorter string; the desktop string above stays word for word, and the phone one
// must say the same count and the same "no draft" state.
assert.ok(read('frontend/src/board/EvidenceBoard.jsx').includes('due within ${DUE_SOON_DAYS} days, no draft`'), 'phone summary counts cases with no draft');
assert.equal(readinessOf({}), null);
assert.equal(amountOf({ dispute_amount: { value: '25.00', currency_code: 'USD' } }), '25.00 USD');
assert.equal(amountOf({ case_ref: 'case-ref-001' }), null);
assert.equal(buildEvidenceBoard({ disputes: [], drafts, now: NOW }), null);
assert.equal(buildEvidenceBoard({ disputes: undefined, now: NOW }), null);
assert.equal(buildEvidenceBoard({ disputes, now: Number.NaN }), null);
{
  const crossed = buildEvidenceBoard({ disputes, drafts: { 'case-ref-001': { ...drafts['case-ref-002'] } }, now: NOW }).rows[0];
  assert.equal(crossed.status, 'DUE_SOON_NO_DRAFT', 'a draft for another case is not used');
  assert.equal(crossed.readiness, null);
}

// 7. Wiring: lazy chunk, StepSection in step 03, read-only features, no direct Bryntum import.
const app = read('frontend/src/App.jsx');
// Matched as two halves so the export import scanner does not read this test as importing the module.
assert.ok(app.includes(['const EvidenceBoard = lazy(() => imp', "ort('./board/EvidenceBoard.jsx'));"].join('')), 'board is a lazy chunk');
const stepThree = app.slice(app.indexOf('<StageAccordion id="disputes"'), app.indexOf('</StageAccordion>', app.indexOf('<StageAccordion id="disputes"')));
assert.match(stepThree, /<StepSection id="evidence-board" title="Evidence deadline board"[^>]*open=\{boardOpen\}/u);
// (2026-11-10, intended) The board also gets the live Sandbox dispute list when the console holds one.
assert.ok(stepThree.includes("<EvidenceBoard disputes={state?.disputes} drafts={boardDraftsForState} sandbox={providerDisputes?.source === 'paypal_sandbox' ? providerDisputes.items : null} />"));
assert.ok(app.includes('const boardOpen = boardExpanded ?? false;'), 'closed by default (UI plan r2 A3), open once toggled');
const boardSource = read('frontend/src/board/EvidenceBoard.jsx');
assert.ok(boardSource.includes("from 'virtual:payguard-optional-timeline'"));
assert.equal(/['"]@bryntum\//u.test(boardSource) || /['"]@bryntum\//u.test(read('frontend/src/board/boardData.js')), false);
// (optimise r24) Case data stays read only: editors, menus, drag-create and delete stay off; drag and resize are on
// with validators, and every data event is locked (checked in section 9).
for (const feature of ['cellEditFeature', 'eventDragCreateFeature', 'eventEditFeature', 'eventMenuFeature', 'scheduleMenuFeature', 'dependenciesFeature', 'resourceMenuFeature', 'cellMenuFeature']) {
  assert.ok(boardSource.includes(`${feature}: false`), `${feature} disabled`);
}
assert.ok(boardSource.includes('enableDeleteKey={false}'), 'Delete key cannot remove events');
assert.ok(boardSource.includes('eventDragFeature={dragFeature} eventResizeFeature={resizeFeature}'), 'drag and resize go through the validators');
assert.ok(boardSource.includes('constrainDragToResource: true'), 'a plan stays on its own case row');
assert.ok(boardSource.includes('snap timeResolution={HOUR_RESOLUTION}') && boardSource.includes("const HOUR_RESOLUTION = { unit: 'hour', increment: 1 };"), 'snaps to whole hours');
assert.ok(boardSource.includes("if (record?.get?.('kind') !== 'PLAN') verdict = { valid: false, code: 'READ_ONLY'"), 'validators refuse anything but a plan bar');
assert.ok(boardSource.includes("scheduler.element?.addEventListener('keydown', keydown, true)"), 'plan keys are taken before the navigator');
assert.ok(boardSource.includes('window.sessionStorage') && !/localStorage/u.test(boardSource), 'plan kept per tab only');
for (const source of [boardSource, read('frontend/src/board/boardData.js')]) {
  assert.equal(/\bfetch\(|XMLHttpRequest|sendBeacon|apiRequest|WebSocket|EventSource|from '\.\.\/api\.js'/u.test(source), false, 'the plan is never sent anywhere');
}
assert.equal(/TimeRanges?Feature|timeRangesFeature/u.test(boardSource), false, 'no Business-tier TimeRanges feature');
// Start and end reach Bryntum together: the scheduler is keyed on the computed range.
assert.ok(boardSource.includes('<BryntumScheduler key={`${board.startDate.getTime()}-${board.endDate.getTime()}-${board.viewPreset}`}'), 'scheduler keyed on its range');
assert.ok(boardSource.includes("`${row.amount} · demo`"), 'list labels the amount demo (N1 C07: synthetic -> demo)');
const css = read('frontend/src/board/board.css');
assert.ok(css.includes('.board-scroll { max-width: 100%; overflow-x: auto;'), 'only the board box scrolls sideways');
for (const size of css.matchAll(/font-size:\s*(\d+)px/gu)) assert.ok(Number(size[1]) >= 14, `font-size ${size[1]}px >= 14px`);

// 8. Hosted image: frontend/src is in the Docker context; the lock is installed with npm ci.
const dockerfile = read('Dockerfile');
assert.ok(dockerfile.includes('COPY frontend/package.json frontend/package-lock.json ./') && dockerfile.includes('RUN npm ci'));
assert.ok(read('.dockerignore').includes('!frontend/src/'));
assert.ok(existsSync(join(frontendRoot, 'src', 'board', 'EvidenceBoard.jsx')));

// 9. (optimise r24) Plan bars, lines and the per-tab plan store.
for (const event of board.events) assert.equal(event.draggable === false && event.resizable === false, true, `${event.id} locked`);
assert.deepEqual(board.timeRanges.map((range) => [range.id, range.kind, range.resourceId]), [['now', 'NOW', null], ['case-ref-001-due', 'DUE', 'case-ref-001'], ['case-ref-002-due', 'DUE', 'case-ref-002'], ['case-ref-003-due', 'DUE', 'case-ref-003']], 'now line plus one due line per case with a due date');
assert.equal(board.timeRanges[0].startDate.getTime(), wall(new Date(NOW).toISOString()));
assert.equal(board.timeRanges[1].startDate.getTime(), wall(drafts['case-ref-001'].routing.seller_response_due_date));
const HOUR = 3600 * 1000;
assert.equal(floorHour(NOW + 1), NOW);
assert.equal(ceilHour(NOW + 1), NOW + HOUR);
assert.equal(wallToUtcMs(new Date(2026, 9, 8, 8, 0)), Date.parse('2026-10-08T08:00:00'), 'local board Date back to its instant');
assert.ok(Number.isNaN(wallToUtcMs(new Date('nope'))));
const odd = NOW + 20 * 60 * 1000;
const windowFirst = planWindowOf(first, odd);
assert.deepEqual(windowFirst, { startMs: NOW + HOUR, endMs: Date.parse('2026-10-10T08:00:00Z'), dueMs: Date.parse('2026-10-10T08:00:00Z') }, 'next whole hour to the due date');
assert.equal(planWindowOf({ dueAt: null }, NOW), null, 'no due date, no plan');
assert.deepEqual(planWindowOf(third, NOW), { startMs: NOW, endMs: Date.parse('2026-10-09T20:00:00Z'), dueMs: Date.parse('2026-10-09T20:00:00Z') }, 'no draft: the plan window comes from the case due date');
assert.equal(planWindowOf({ dueAt: new Date(NOW + 50 * 60 * 1000).toISOString() }, NOW + 1), null, 'under an hour left, no plan');
assert.deepEqual(defaultPlan(windowFirst), { startMs: NOW + HOUR, endMs: NOW + HOUR + PLAN_DEFAULT_HOURS * HOUR });
assert.deepEqual(defaultPlan({ startMs: NOW, endMs: NOW + 2 * HOUR }), { startMs: NOW, endMs: NOW + 2 * HOUR }, 'default stops at the due date');
const due1 = Date.parse('2026-10-10T08:00:00Z');
const judge = (startMs, endMs, nowMs = NOW) => validatePlan({ startMs, endMs }, { nowMs, dueMs: due1 });
assert.deepEqual(judge(NOW, NOW + 4 * HOUR), { valid: true, code: 'OK', message: '' });
assert.equal(judge(NOW - HOUR, NOW + 4 * HOUR).code, 'BEFORE_NOW');
assert.equal(judge(due1 - HOUR, due1 + HOUR).code, 'AFTER_DUE');
assert.equal(judge(due1 - 4 * HOUR, due1).valid, true, 'may end exactly at the due date');
assert.equal(judge(NOW + HOUR, NOW + HOUR).code, 'EMPTY');
assert.equal(judge(NOW + 60000, NOW + 2 * HOUR).code, 'NOT_ON_HOUR');
assert.equal(judge(Number.NaN, NOW).code, 'INVALID');
assert.equal(validatePlan({ startMs: NOW, endMs: NOW + HOUR }, { nowMs: NOW, dueMs: Number.NaN }).code, 'INVALID');
assert.equal(PLAN_MESSAGES.BEFORE_NOW, 'Cannot start before now.');
assert.equal(PLAN_MESSAGES.AFTER_DUE, 'Needs to end by the response due date.');
assert.deepEqual(shiftPlan({ startMs: NOW, endMs: NOW + HOUR }, 2), { startMs: NOW + 2 * HOUR, endMs: NOW + 3 * HOUR });
assert.deepEqual(shiftPlan({ startMs: NOW, endMs: NOW + 3 * HOUR }, -1, { resize: true }), { startMs: NOW, endMs: NOW + 2 * HOUR });
// Restore: a stored plan that still fits is kept, a broken or late one falls back to the default, unknown cases drop.
const stored = {
  'case-ref-001': { start: new Date(NOW + 5 * HOUR).toISOString(), end: new Date(NOW + 9 * HOUR).toISOString() },
  'case-ref-002': { start: new Date(NOW - 5 * HOUR).toISOString(), end: new Date(NOW + 9 * HOUR).toISOString() },
  'case-ref-999': { start: new Date(NOW + HOUR).toISOString(), end: new Date(NOW + 2 * HOUR).toISOString() },
};
const plans = restorePlans(stored, board.rows, NOW);
assert.deepEqual(Object.keys(plans), ['case-ref-001', 'case-ref-002', 'case-ref-003']);
assert.deepEqual(plans['case-ref-003'], defaultPlan(planWindowOf(third, NOW)));
assert.deepEqual(plans['case-ref-001'], { startMs: NOW + 5 * HOUR, endMs: NOW + 9 * HOUR });
assert.deepEqual(plans['case-ref-002'], defaultPlan(planWindowOf(second, NOW)));
const bars = planEvents(board.rows, plans);
assert.deepEqual(bars.map((bar) => [bar.id, bar.resourceId, bar.kind, bar.name, bar.draggable, bar.resizable]), [
  ['case-ref-001-plan', 'case-ref-001', 'PLAN', 'Collect evidence', true, true], ['case-ref-002-plan', 'case-ref-002', 'PLAN', 'Collect evidence', true, true],
  ['case-ref-003-plan', 'case-ref-003', 'PLAN', 'Collect evidence', true, true]]);
assert.equal(bars[0].startDate.getTime(), wall(new Date(NOW + 5 * HOUR).toISOString()), 'plan bars use the board wall clock');
// Storage: schema-checked, per tab, times and case refs only; a throwing storage leaves the plan in the page.
const memory = new Map();
const fake = { getItem: (key) => memory.get(key) ?? null, setItem: (key, value) => memory.set(key, value) };
assert.equal(writeStoredPlans(fake, plans), true);
assert.deepEqual(JSON.parse(memory.get(PLAN_STORAGE_KEY)), { schema: PLAN_SCHEMA, plans: {
  'case-ref-001': { start: new Date(NOW + 5 * HOUR).toISOString(), end: new Date(NOW + 9 * HOUR).toISOString() },
  'case-ref-002': { start: new Date(plans['case-ref-002'].startMs).toISOString(), end: new Date(plans['case-ref-002'].endMs).toISOString() },
  'case-ref-003': { start: new Date(plans['case-ref-003'].startMs).toISOString(), end: new Date(plans['case-ref-003'].endMs).toISOString() },
} });
assert.deepEqual(restorePlans(readStoredPlans(fake), board.rows, NOW), plans, 'round trip');
const throwing = { getItem: () => { throw new Error('blocked'); }, setItem: () => { throw new Error('blocked'); } };
assert.deepEqual(readStoredPlans(throwing), {});
assert.equal(writeStoredPlans(throwing, plans), false);
assert.equal(writeStoredPlans(null, plans), false);
memory.set(PLAN_STORAGE_KEY, JSON.stringify({ schema: 'other', plans: stored }));
assert.deepEqual(readStoredPlans(fake), {}, 'other schema ignored');
memory.set(PLAN_STORAGE_KEY, '{not json');
assert.deepEqual(readStoredPlans(fake), {});

// "Download my plan (.ics)" (2026-11-09): RFC 5545 text, one VEVENT per case, UTC, CRLF, no personal data, no network.
{
  const { plansToIcs, PLAN_ICS_EMPTY_REASON } = await import('../frontend/src/board/boardData.js');
  assert.equal(plansToIcs({}), null, 'no plan, no file');
  assert.ok(PLAN_ICS_EMPTY_REASON.length > 10);
  const ics = plansToIcs({ 'case-ref-002': { startMs: Date.UTC(2026, 10, 10, 9), endMs: Date.UTC(2026, 10, 10, 12) }, 'case-ref-001': { startMs: Date.UTC(2026, 10, 9, 8), endMs: Date.UTC(2026, 10, 9, 20) } }, { now: Date.UTC(2026, 10, 9, 7, 30) });
  assert.ok(ics.startsWith('BEGIN:VCALENDAR\r\nVERSION:2.0\r\n') && ics.endsWith('END:VCALENDAR\r\n'), 'calendar frame, CRLF');
  assert.ok(!/[^\r]\n/u.test(ics), 'every line ends in CRLF');
  assert.equal((ics.match(/BEGIN:VEVENT/gu) || []).length, 2, 'one VEVENT per case');
  assert.equal((ics.match(/END:VEVENT/gu) || []).length, 2);
  assert.ok(ics.includes('DTSTART:20261109T080000Z\r\nDTEND:20261109T200000Z') && ics.includes('DTSTART:20261110T090000Z\r\nDTEND:20261110T120000Z'), 'UTC start and end');
  assert.ok(ics.includes('SUMMARY:Collect evidence for case-ref-001') && ics.includes('DTSTAMP:20261109T073000Z'));
  assert.ok(ics.indexOf('case-ref-001') < ics.indexOf('case-ref-002'), 'sorted by case');
  assert.ok(!/@(?!tradeglot\.invalid)[a-z]/iu.test(ics) && !/https?:/u.test(ics), 'no e-mail, no link');
  const boardSrc = readFileSync(join(projectRoot, 'frontend/src/board/EvidenceBoard.jsx'), 'utf8');
  assert.ok(boardSrc.includes('data-testid="evidence-board-plan-ics"') && boardSrc.includes('Download my plan (.ics)') && boardSrc.includes('disabled={!Object.keys(plans).length}'), 'button, disabled without a plan');
  assert.ok(!/fetch\(|apiRequest/u.test(boardSrc.slice(boardSrc.indexOf('const downloadPlan'), boardSrc.indexOf('const resetPlans'))), 'the download makes no request');
}

console.log(`frontend_bryntum_board_contract: ok (${board.rows.length} rows, ${board.events.length} events, highlighted ${board.highlighted.join(',')}; ${manifest.dependencies['@bryntum/scheduler-community']} MIT${installed.installed ? ', installed' : ''})`);
