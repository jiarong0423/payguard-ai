// The evidence auditor: a custom AG Studio agent with its own run loop.
//
// For a closed set of questions, one per part of the dashboard (deadlines, missing proof, time flags, time
// evidence, requested evidence, guide benchmark, Channel3 receipts), it computes the answer from the
// dashboard's rows with plain code, then builds the answer on the canvas with Studio's own tools
// (remove_widget, add_widget, configure_widget, add_widget_filter) and lists those steps in its reply in plain words
// (the tool names go to the dashboard's collapsed "Technical steps", r31 J1 J4). The canvas
// filter tests the same field as the code, so the grid shows exactly the rows named in the reply. (r32 J3) A case
// selection the seller made on that page (a cross filter from a click, or a page filter such as "Filter by case")
// would narrow the grid as well, so the auditor first clears it through the dashboard (`clearSelections`, not a
// Studio tool) and says so in its steps; without that hook the reply names the selection instead.
//
// Anything outside that set goes to Studio's data agent when the console has a model configured (local live
// mode, through the governed backend route), to a recorded run of the data agent when one exists (replayed with
// the same Studio tools, no model call), or gets the list of questions. The auditor never decides a dispute,
// predicts no outcome, writes no data and calls no network service itself.
// Pure module: no Studio import, so node tests drive it with stand-in tools.

import { findRecordedRun, recordingLabel, replayRun } from './agentRecording.js';

export const AUDITOR_ID = 'evidence-auditor';
// Same ids and slot as layout.js (kept literal here so this module needs no layout import).
export const ANSWER_SLOTS = Object.freeze({ readiness: 'auditor-answer', guide: 'auditor-answer-guide' });
export const ANSWER_WIDGET_ID = ANSWER_SLOTS.readiness;
export const ANSWER_PAGE_ID = 'readiness';
export const ANSWER_SLOT = Object.freeze({ xTrack: 0, yTrack: 18, xSpan: 24, ySpan: 14 });
export const BUILT_IN_AGENT_IDS = Object.freeze(['lead', 'data', 'page', 'planning', 'widget']);
export const BOUNDARY = 'Read only: this page orders and shows synthetic records. It makes no dispute decision, predicts no outcome and submits nothing to PayPal.';
export const BUILT_IN_OFF = 'Studio\'s built-in agents (lead, data, page, planning, widget) are off: no model is configured, and the hosted demo makes no model calls.';
export const BUILT_IN_LIVE = 'Studio\'s built-in agents (lead, data, page, planning, widget) are on: they use Gemini through the console\'s governed route (local live mode, call caps, no key in the browser).';
// (rehearsal 2026-11-04) The widget example used all 20 Studio calls and ended with no widget; this question ran in
// six agent turns on 2026-11-04 and matched the rows.
export const DELEGATE_EXAMPLE = 'Which reason code appears most often across the three cases?';

const count = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;
const maxBy = (rows, key) => rows.reduce((best, row) => (row[key] !== null && (best === null || row[key] > best) ? row[key] : best), null);
const minBy = (rows, key) => rows.reduce((best, row) => (row[key] !== null && (best === null || row[key] < best) ? row[key] : best), null);

// Each question: how it is recognised, which table and page, which rows the code selects, the canvas filter
// that selects the same rows, and how the answer is said. `value(data)` is computed once per answer.
export const QUESTIONS = Object.freeze([
  {
    id: 'missing_delivery_proof', label: 'Which cases lack proof of delivery?',
    match: /(lack|missing|without|no)\b.*\b(proof|attachment)|proof of delivery|delivery proof/iu,
    table: 'cases', page: 'readiness', title: 'Cases with no delivery attachment on file',
    columns: ['case_ref', 'due_date', 'days_to_due', 'delivery_proof', 'review_flag'],
    value: () => 'No attachment on file', field: 'delivery_proof', operator: 'equals',
    say: (matched, all) => `${matched.length} of ${count(all.length, 'synthetic case')}: ${matched.map((row) => `${row.case_ref} (${row.review_flag === 'None' ? 'no review flag' : row.review_flag.toLowerCase()})`).join('; ') || 'none'}. A case counts as lacking proof of delivery when no accepted attachment backs its fulfilment requirement; a seller-provided delivery time alone does not count.`,
  },
  {
    id: 'due_soon', label: 'Which are due within 3 days?',
    match: /\bare due\b|\bdue (within|soon|in)\b|deadline|within\s*3\s*days/iu,
    table: 'cases', page: 'readiness', title: 'Cases due within 3 days',
    columns: ['case_ref', 'due_date', 'days_to_due', 'readiness', 'submission'],
    value: () => 3, field: 'days_to_due', operator: 'lessThanOrEqual',
    say: (matched, all) => `${matched.length} of ${count(all.length, 'synthetic case')}: ${matched.map((row) => `${row.case_ref} in ${count(row.days_to_due, 'day')}`).join('; ') || 'none'}. Days run from the dashboard's as-of time to the seller response due date in the synthetic provider snapshot.`,
  },
  {
    id: 'time_flags', label: 'Which cases have time flags?',
    match: /time\s*flag|\bflags?\b|order of events/iu,
    table: 'cases', page: 'readiness', title: 'Cases with time evidence flags',
    columns: ['case_ref', 'time_flag_count', 'review_flag', 'delivered_at'],
    value: () => 0, field: 'time_flag_count', operator: 'greaterThan',
    say: (matched, all) => `${matched.length} of ${count(all.length, 'synthetic case')}: ${matched.map((row) => `${row.case_ref} (${count(row.time_flag_count, 'flag')}: ${row.review_flag.toLowerCase()})`).join('; ') || 'none'}. A time flag is a neutral note about the order of recorded times, not a judgement.`,
  },
  {
    id: 'longest_gap', label: 'Where is the longest gap between recorded events?',
    // (2026-11-09) "largest disputed amount" used to land here on the word "largest" alone; now the question must be about a gap,
    // a delay or the time between events.
    match: /\bgaps?\b|(longest|biggest|largest)\s+(gap|delay|wait|time|interval)|(longest|biggest|largest)\b[^.?]*\b(between|events?)\b/iu,
    table: 'time_events', page: 'readiness', title: 'Longest gap between recorded events',
    columns: ['case_ref', 'order', 'event', 'at', 'gap_hours'],
    value: (data) => maxBy(data.time_events, 'gap_hours'), field: 'gap_hours', operator: 'greaterThanOrEqual',
    say: (matched) => `${matched.map((row) => `${row.case_ref}, event ${row.order} (${row.event}): ${row.gap_hours} hours after the event before it`).join('; ') || 'No recorded gaps'}. Times are as recorded (seller-provided unless stated); a gap is not a judgement.`,
  },
  {
    id: 'requested_evidence', label: 'What evidence does each case still need?',
    match: /requested|still need|evidence (does|do)|checklist|requirement/iu,
    table: 'requirements', page: 'readiness', title: 'Evidence requested per case',
    columns: ['case_ref', 'evidence_type', 'state', 'proof_count', 'attachment_count'],
    value: () => 'Mandatory', field: 'mandatory', operator: 'equals',
    say: (matched) => `${count(matched.length, 'mandatory request')}: ${matched.map((row) => `${row.case_ref} ${row.evidence_type.toLowerCase()}, ${row.state.toLowerCase()}, ${count(row.attachment_count, 'accepted attachment')}`).join('; ')}. Required fields present is a structural check, not verified evidence.`,
  },
  {
    id: 'fewest_model_calls', label: 'Which guide flow needs the fewest model calls?',
    match: /model calls|fewest|cheapest|guide flow|benchmark/iu,
    table: 'benchmark', page: 'guide', title: 'Guide flows with the fewest model calls',
    columns: ['flow', 'model_calls', 'rounds', 'wrong_honest', 'wrong_careless'],
    value: (data) => minBy(data.benchmark, 'model_calls'), field: 'model_calls', operator: 'equals',
    say: (matched, all) => `${matched.map((row) => `"${row.flow}" with ${row.model_calls} model calls${row.rounds === null ? '' : ` and ${row.rounds} rounds`}`).join('; ')}, against ${maxBy(all, 'model_calls')} when every sentence goes to the AI. From the recorded guide benchmark (268 synthetic cases).`,
  },
  {
    id: 'slowest_search', label: 'Which Channel3 search was slowest?',
    match: /channel3|slowest|latency|search/iu,
    table: 'receipts', page: 'guide', title: 'Slowest recorded Channel3 search',
    columns: ['query', 'called_at', 'http_status', 'result_status', 'cards', 'latency_seconds'],
    value: (data) => maxBy(data.receipts, 'latency_seconds'), field: 'latency_seconds', operator: 'greaterThanOrEqual',
    say: (matched, all) => `${matched.map((row) => `"${row.query}" at ${row.latency_seconds} s (HTTP ${row.http_status}, ${count(row.cards, 'card')})`).join('; ')}; all ${all.length} recorded searches returned HTTP ${[...new Set(all.map((row) => row.http_status))].join('/')}. Recorded once; the hosted demo replays them and makes no call.`,
  },
]);

const APPLY = {
  equals: (a, b) => a === b, lessThanOrEqual: (a, b) => a <= b, greaterThan: (a, b) => a > b, greaterThanOrEqual: (a, b) => a >= b,
};

export function matchQuestion(text) {
  const value = String(text || '');
  if (/\b(clear|reset|remove)\b/iu.test(value)) return { id: 'clear' };
  if (/built.?in|lead agent|\bmodel\b(?! calls)|gemini|llm/iu.test(value)) return { id: 'built_in' };
  return QUESTIONS.find((question) => question.match.test(value)) || { id: 'unknown' };
}

const OPERATOR_WORDS = { equals: '=', lessThanOrEqual: '≤', greaterThan: '>', greaterThanOrEqual: '≥' };
// Technical form, for the collapsed "Technical steps": exact table and field ids.
function describeFilter(question, value) {
  return `${question.table}.${question.field} ${OPERATOR_WORDS[question.operator]} ${JSON.stringify(value)}`;
}
// (r31 J1 J4) Seller form: ids as words ("time_events" -> "time events", "gap_hours" -> "gap hours").
const plainName = (id) => id.replace(/_/gu, ' ');
const plainFilter = (question, value) => `${plainName(question.field)} ${OPERATOR_WORDS[question.operator]} ${typeof value === 'string' ? `"${value}"` : value}`;

// (r32 J3) The seller's own selections on a page, in plain words: cross filters set by clicking another widget
// (state.pages[].crossFilter.values, keyed by the widget that set them) and page filters with a value
// (state.pages[].filter.page, for example "Filter by case"). Either narrows the answer grid on that page.
const fieldWords = (field) => plainName(String(field?.id ?? '').split('.').pop() || 'field');
const valueWords = (values) => [].concat(values ?? []).map(String).join(' or ');
function selectionWords(selection) {
  if (selection?.type === 'value') return `${fieldWords(selection.field)} = ${valueWords(selection.values)}`;
  if (selection?.type === 'range') return `${fieldWords(selection.field)} from ${selection.from ?? 'the start'} to ${selection.to ?? 'the end'}`;
  return 'a selection on another widget';
}
export function pageSelections(state, pageId) {
  const page = state?.pages?.find((entry) => entry.id === pageId);
  if (!page) return [];
  const words = [];
  for (const [widgetId, selections] of Object.entries(page.crossFilter?.values || {})) {
    if (widgetId === ANSWER_SLOTS[pageId]) continue;  // the answer grid's own selection does not narrow itself
    for (const selection of selections || []) words.push(selectionWords(selection));
  }
  for (const filter of page.filter?.page || []) {
    if (!filter?.model) continue;
    const value = filter.model.value;
    words.push(value === undefined || value === null || (Array.isArray(value) && value.length === 0)
      ? `a filter on ${fieldWords(filter.field)}` : `${fieldWords(filter.field)} = ${valueWords(value)}`);
  }
  return words;
}
// (r32 J3 P3) The slot starts out holding the page's own table; after an answer it holds the auditor's grid.
const ANSWER_TITLE_PREFIX = 'Evidence auditor · ';
export function slotTitle(state, pageId) {
  const widget = state?.pages?.find((entry) => entry.id === pageId)?.widgets?.[ANSWER_SLOTS[pageId]];
  return widget ? String(widget.format?.title?.text ?? '') : null;
}
const isPageTable = (title) => typeof title === 'string' && !title.startsWith(ANSWER_TITLE_PREFIX);
function removeStep(title) {
  if (!isPageTable(title)) return { tool: 'remove_widget', plain: 'Removed the previous answer', detail: 'the previous answer' };
  const name = title.trim();
  return { tool: 'remove_widget', plain: name ? `Replaced the page's ${name} table with the answer` : 'Replaced the page\'s table with the answer',
    detail: `the page's own table${name ? ` "${name}"` : ''} in the answer slot` };
}

// The answer as data: which rows, the reply text and the Studio tool calls that show it.
//   slotExists  { page: bool }   slotTitles  { page: title of the widget in the slot }
//   selections  { page: [plain words] } from pageSelections   canClear  the auditor can clear them first
export function planAnswer(text, data, { slotExists = {}, slotTitles = {}, selections = {}, canClear = false } = {}) {
  const question = matchQuestion(text);
  if (question.id === 'clear') {
    const calls = Object.entries(ANSWER_SLOTS).filter(([page]) => slotExists[page])
      .map(([page, widgetId]) => ({ tool: 'removeWidget', page, args: { widgetId } }));
    return { intent: 'clear', refs: [], calls, page: null, reply: calls.length ? 'Removed the auditor answers from the canvas.' : 'There is no auditor answer on the canvas.' };
  }
  if (!QUESTIONS.includes(question)) return { intent: question.id, refs: [], calls: [], page: null, reply: '' };
  const rows = data[question.table];
  const value = question.value(data);
  const matched = rows.filter((row) => row[question.field] !== null && APPLY[question.operator](row[question.field], value));
  const widgetId = ANSWER_SLOTS[question.page];
  const filter = { field: { id: `${question.table}.${question.field}` }, model: { operator: question.operator, value } };
  const selected = selections[question.page] || [];
  const clearing = canClear && selected.length > 0;
  const calls = [
    ...(clearing ? [{ tool: 'clearSelections', page: question.page, args: {} }] : []),
    ...(slotExists[question.page] ? [{ tool: 'removeWidget', page: question.page, args: { widgetId } }] : []),
    { tool: 'addWidget', page: question.page, args: { widgetId, type: 'grid', ...ANSWER_SLOT } },
    { tool: 'configureWidget', page: question.page, args: { widgetId, op: 'patch', value: {
      type: 'grid',
      format: { title: { enabled: true, text: `Evidence auditor · ${question.title}` },
        subtitle: { enabled: true, text: 'Built by the evidence auditor with Studio tools. Answered with code; no model, no decision.' } },
      dataMapping: { cols: question.columns.map((column) => ({ id: `${question.table}.${column}` })) },
    } } },
    { tool: 'addWidgetFilter', page: question.page, args: { widgetId, op: 'append', value: filter } },
  ];
  // (r31 J1 J4) The reply says each step in plain words for a seller; the exact Studio tool names stay in `technical`,
  // which the dashboard shows under a collapsed "Technical steps" (main.jsx), in the same order as `calls`.
  const pageName = question.page === 'guide' ? 'Guide and Channel3 evidence' : 'Evidence readiness';
  const technical = [
    ...(clearing ? [{ tool: 'clear_selections', plain: `Cleared the page's own selection (${selected.join('; ')}) so the table shows every matching row`,
      detail: `the page's cross filter and page filter values (${selected.join('; ')}), reset through the dashboard, not a Studio tool` }] : []),
    ...(slotExists[question.page] ? [removeStep(slotTitles[question.page])] : []),
    { tool: 'add_widget', plain: `Added a table under the headline tiles of the ${pageName} page`,
      detail: `a grid in the answer slot under the headline tiles of the ${pageName} page` },
    { tool: 'configure_widget', plain: `Showed ${question.columns.length} columns from ${plainName(question.table)}`,
      detail: `title and ${question.columns.length} columns from ${question.table}` },
    { tool: 'add_widget_filter', plain: `Filtered: ${plainFilter(question, value)}`, detail: describeFilter(question, value) },
  ];
  // (r32 J3) Without the clear hook the selection stays, so the reply says the table shows only rows inside it.
  const narrowed = !clearing && selected.length > 0
    ? ` The page also has its own selection (${selected.join('; ')}), so the table shows only the matching rows inside it.` : '';
  const reply = `${question.say(matched, rows)} How I built this: ${technical.map((step, index) => `${index + 1}. ${step.plain}.`).join(' ')}${narrowed} ${BOUNDARY}`;
  const key = { cases: 'case_ref', time_events: 'event_id', requirements: 'requirement_id', benchmark: 'flow_id', receipts: 'receipt_id' }[question.table];
  return { intent: question.id, refs: matched.map((row) => row[key]), calls, page: question.page, reply, filter, technical };
}

// (foolproofing 2026-11-04) A delegated question can use the whole Studio allowance (20 Gemini calls per client per
// day, controlled_fallback.CALLS_PER_CLIENT_PER_DAY), so the auditor asks first and delegates only after a plain yes.
export const DELEGATE_CONFIRM_TEXT = 'This question goes to Studio\'s data agent (Gemini, paid). One question usually uses 3 to 6 Gemini calls (hard stop at 8) of the 20 allowed per day on this console. Reply "yes" to send it, or ask something else.';
// (red team r27 A) The question goes to the data agent, not the lead orchestrator, with a short scope so it answers
// in a few turns: the lead added planning, renaming and verify turns and once used all 20 calls with no summary.
// Kept short and digit-free so prefix plus question stays inside the 600-character user item (studio_agent.py).
export const DELEGATE_PREFIX = 'Question mode, not exploration. Use at most two rounds of execute_query, then call complete_task. Answer in plain text from the rows only: counts and field values. No opinion about any party or result. Do not create widgets.';
export const DELEGATE_INSTRUCTIONS_MAX = 600;
export const delegateInstructions = (question) => {
  const room = DELEGATE_INSTRUCTIONS_MAX - DELEGATE_PREFIX.length - ' Question: '.length;
  return `${DELEGATE_PREFIX} Question: ${String(question).slice(0, Math.max(0, room))}`;
};
// (red team r27 A) Shown in place of the summary when the agent did not finish inside the call limit.
export const NO_SUMMARY = '(the delegate finished without a summary)';
export const NOT_FINISHED_TEXT = 'The data agent did not finish this question within the call limit, so there is no answer to show. Ask a narrower question, or try again after the console restarts.';
// (red team r27 A) The summary is shown only when it reads as a report of the rows, not a judgement about the dispute.
const JUDGEMENT_WORDS = /\b(?:wins?|won|winning|lose[sd]?|losing|lost|prevails?|prevailed|liable|at fault|guilty|in (?:the )?(?:seller|buyer|merchant|customer)'?s? favou?r|(?:likely|chance|probability) (?:to|of) (?:win|succeed|prevail)|should (?:win|lose|be refunded)|(?:strong|weak)(?:er)? case|supports? the (?:seller|buyer|merchant|customer))\b/iu;
export const WITHHELD_TEXT = 'The answer was withheld: it read as a judgement about the dispute, which this dashboard does not make.';
export const readsAsJudgement = (text) => typeof text === 'string' && JUDGEMENT_WORDS.test(text);
// (live run 2026-11-04) Studio writes mentions such as @table[cases] and @field[cases.reason] and markdown; the chat
// renders them, the status line above the canvas shows plain text.
export const plainSummary = (text) => String(text ?? '')
  .replace(/@table\[([^\]]+)\]/gu, '$1')
  .replace(/@field\[(?:[^\].]+\.)?([^\]]+)\]/gu, '$1')
  .replace(/[`*]/gu, '')
  .replace(/:?\s+-\s+/gu, ' · ')
  .replace(/\s+/gu, ' ')
  .trim();
const CONFIRM_WORDS = /^\s*(yes|y|ok|okay|send it|continue)\s*[.!]?\s*$/iu;
export const isDelegateConfirmation = (text) => typeof text === 'string' && CONFIRM_WORDS.test(text);

function lastUserText(messages) {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    if (messages[index].role === 'user') return messages[index].content;
  }
  return '';
}

export function toolContext(input, signal) {
  return {
    signal: signal || new AbortController().signal,
    run: { threadId: input.threadId, runId: input.runId },
    success: (response, data) => ({ success: true, response, data }),
    error: (messages) => ({ success: false, issues: [].concat(messages).map((message) => ({ message })) }),
  };
}

function* say(messageId, text) {
  yield { type: 'TEXT_MESSAGE_START', messageId, role: 'assistant' };
  yield { type: 'TEXT_MESSAGE_CONTENT', messageId, delta: text };
  yield { type: 'TEXT_MESSAGE_END', messageId };
}

// Build the runnable agent.
//   studio     Studio's built tools (harness `tools.studio`)      getState  reads the dashboard state
//   data       { cases, requirements, time_events, benchmark, receipts } rows the dashboard was built from
//   delegate   optional `tools.delegateTo(['data'])`, only when the built-in agents are live
//   recording  optional validated recording (agentRecording.js), replayed when the agents are not live
//   recorder   optional recorder, in record mode only            onAnswer  called with the page that changed
//   clearSelections  optional (pageId) => void, clears that page's cross filter and page filter values (r32 J3)
export function createEvidenceAuditor({ studio, getState, data, delegate = null, recording = null, recorder = null, onAnswer = () => {}, onDelegated = () => {}, onConfirmNeeded = () => {}, clearSelections = null }) {
  let sequence = 0;
  // (red team r26 #2 P2) Pending questions are kept per Studio thread, and a confirmation word is never stored.
  const pendingByThread = new Map();
  const mode = delegate ? 'live' : recording ? 'replay' : 'off';
  return {
    id: AUDITOR_ID,
    name: 'Evidence auditor',
    description: 'Answers fixed evidence-readiness questions from the synthetic records with code, and builds the answer on the canvas with Studio tools.',
    async *run(input, ctx = {}) {
      const { threadId, runId } = input;
      const toolCtx = toolContext(input, ctx.signal);
      const messageId = `${runId}-reply`;
      yield { type: 'RUN_STARTED', threadId, runId };
      try {
        const typed = lastUserText(input.messages || []);
        const pending = pendingByThread.get(threadId) ?? null;
        const confirmed = mode === 'live' && pending !== null && isDelegateConfirmation(typed);
        const question = confirmed ? pending : typed;
        pendingByThread.delete(threadId);
        const state = getState();
        const slotExists = Object.fromEntries(Object.entries(ANSWER_SLOTS)
          .map(([page, widgetId]) => [page, Boolean(state?.pages?.find((entry) => entry.id === page)?.widgets?.[widgetId])]));
        const pageIds = Object.keys(ANSWER_SLOTS);
        const plan = planAnswer(question, data, {
          slotExists,
          slotTitles: Object.fromEntries(pageIds.map((page) => [page, slotTitle(state, page)])),
          selections: Object.fromEntries(pageIds.map((page) => [page, pageSelections(state, page)])),
          canClear: typeof clearSelections === 'function',
        });
        if (plan.intent === 'built_in') {
          const recorded = recording ? ` ${recording.runs.length === 1 ? 'A recorded live run' : `${recording.runs.length} recorded live runs`} can be replayed here (no model call): ask ${recording.runs.map((run) => `"${run.question}"`).join(', ')}.` : '';
          yield* say(messageId, `${mode === 'live' ? BUILT_IN_LIVE : `${BUILT_IN_OFF}${recorded}`} I am the evidence auditor: I answer my own questions with code. ${BOUNDARY}`);
          yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'built_in' } };
          return;
        }
        if (plan.intent === 'unknown') {
          if (mode === 'live' && !confirmed) {
            if (!isDelegateConfirmation(question)) { pendingByThread.set(threadId, question); onConfirmNeeded(question); }
            yield* say(messageId, `${DELEGATE_CONFIRM_TEXT} ${BOUNDARY}`);
            yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'confirm_delegation' } };
            return;
          }
          if (mode === 'live') {
            // Hand the question to Studio's data agent (type data) with a short scope; it answers from the rows.
            recorder?.begin(question, state?.selectedPageId || ANSWER_PAGE_ID);
            const tool = delegate;
            const toolCallId = `${runId}-delegate`;
            const args = { type: { id: 'data' }, instructions: delegateInstructions(question) };
            yield { type: 'TOOL_CALL_START', toolCallId, toolCallName: tool.name };
            yield { type: 'TOOL_CALL_ARGS', toolCallId, delta: JSON.stringify(args) };
            yield { type: 'TOOL_CALL_END', toolCallId };
            const result = await tool.execute({ toolCallId, name: tool.name, args }, toolCtx);
            const raw = result.success ? result.response : result.issues.map((issue) => issue.message).join('; ');
            const finished = result.success && typeof raw === 'string' && raw.trim() !== '' && raw.trim() !== NO_SUMMARY;
            const summary = !finished ? NOT_FINISHED_TEXT : readsAsJudgement(raw) ? WITHHELD_TEXT : raw;
            yield { type: 'TOOL_CALL_RESULT', messageId: `${toolCallId}-result`, toolCallId, role: 'tool', content: summary };
            recorder?.end(summary);
            // (red team r27 B) Also reported outside the Studio thread, so a Studio remount cannot hide the answer.
            onDelegated({ question, summary, ok: finished && summary === raw });
            yield* say(messageId, `That is outside my fixed questions, so I handed it to Studio's data agent (Gemini, through the console's governed route). Its answer: ${summary} ${BOUNDARY}`);
            yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'delegated', ok: result.success } };
            return;
          }
          const recorded = mode === 'replay' ? findRecordedRun(recording, question) : null;
          if (recorded) {
            yield* replayRun(recorded, { studio, getState, toolContext: toolCtx, idPrefix: `${runId}-replay` });
            onAnswer(recorded.page_id);
            yield* say(messageId, `${recordingLabel(recording)} The data agent's answer then: ${recorded.reply} ${BOUNDARY}`);
            yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'replayed' } };
            return;
          }
          const offer = mode === 'replay' ? ` A recorded run of Studio's data agent can be replayed for: ${recording.runs.map((run) => `"${run.question}"`).join(', ')}.` : ` ${BUILT_IN_OFF}`;
          yield* say(messageId, `I answer fixed questions with code: ${QUESTIONS.map((entry) => entry.label).join(' ')}${offer} ${BOUNDARY}`);
          yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'unknown' } };
          return;
        }
        for (const call of plan.calls) {
          if (call.tool === 'clearSelections') {
            clearSelections(call.page);  // dashboard state, not a Studio tool: no tool-call events
            continue;
          }
          sequence += 1;
          const tool = call.tool === 'configureWidget'
            ? studio.configureWidget({ widgetType: 'grid', widgetId: call.args.widgetId }, { pageId: call.page })
            : studio[call.tool]({ pageId: call.page });
          const toolCallId = `${runId}-tool-${sequence}`;
          yield { type: 'TOOL_CALL_START', toolCallId, toolCallName: tool.name };
          yield { type: 'TOOL_CALL_ARGS', toolCallId, delta: JSON.stringify(call.args) };
          yield { type: 'TOOL_CALL_END', toolCallId };
          const result = await tool.execute({ toolCallId, name: tool.name, args: call.args }, toolCtx);
          yield { type: 'TOOL_CALL_RESULT', messageId: `${toolCallId}-result`, toolCallId, role: 'tool',
            content: result.success ? result.response : result.issues.map((issue) => issue.message).join('; ') };
          if (!result.success) throw new Error(`${tool.name} failed: ${result.issues.map((issue) => issue.message).join('; ')}`);
        }
        // (r31 J1 J4) The tool-name steps go to the dashboard's collapsed "Technical steps", not into the reply.
        if (plan.page) onAnswer(plan.page, plan.technical);
        yield* say(messageId, plan.reply);
        yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: plan.intent, refs: plan.refs } };
      } catch (failure) {
        yield { type: 'RUN_ERROR', message: failure.message || 'The evidence auditor could not finish.' };
      }
    },
  };
}

export function promptStarters({ mode = 'off', recording = null } = {}) {
  const starters = QUESTIONS.slice(0, 4).map((question) => ({ label: question.label, prompt: question.label }));
  if (mode === 'live') starters.push({ label: DELEGATE_EXAMPLE, prompt: DELEGATE_EXAMPLE });
  else if (recording) recording.runs.forEach((run) => starters.push({ label: `${run.question} (recorded live run)`, prompt: run.question }));
  starters.push({ label: 'Are the built-in agents on?', prompt: 'Are the built-in agents on?' });
  return starters;
}
export const PROMPT_STARTERS = Object.freeze(promptStarters());
