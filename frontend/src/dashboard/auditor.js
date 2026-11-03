// The evidence auditor: a custom AG Studio agent with its own run loop.
//
// For a closed set of questions, one per part of the dashboard (deadlines, missing proof, time flags, time
// evidence, requested evidence, guide benchmark, Channel3 receipts), it computes the answer from the
// dashboard's rows with plain code, then builds the answer on the canvas with Studio's own tools
// (remove_widget, add_widget, configure_widget, add_widget_filter) and lists those steps in its reply. The canvas
// filter tests the same field as the code, so the grid shows exactly the rows named in the reply.
//
// Anything outside that set goes to Studio's lead agent when the console has a model configured (local live
// mode, through the governed backend route), to a recorded run of the lead agent when one exists (replayed with
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
export const BOUNDARY = 'Read only: this orders and shows synthetic records. It makes no dispute decision, predicts no outcome and submits nothing to PayPal.';
export const BUILT_IN_OFF = 'Studio\'s built-in agents (lead, data, page, planning, widget) are off: no model is configured, and the hosted demo makes no model calls.';
export const BUILT_IN_LIVE = 'Studio\'s built-in agents (lead, data, page, planning, widget) are on: they use Gemini through the console\'s governed route (local live mode, call caps, no key in the browser).';
export const DELEGATE_EXAMPLE = 'Make a widget comparing cases by days to due';

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
    say: (matched, all) => `${matched.length} of ${count(all.length, 'synthetic case')}: ${matched.map((row) => `${row.case_ref} in ${row.days_to_due} days`).join('; ') || 'none'}. Days run from the dashboard's as-of time to the seller response due date in the synthetic provider snapshot.`,
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
    match: /longest|biggest|largest|gap/iu,
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

function describeFilter(question, value) {
  const words = { equals: '=', lessThanOrEqual: '≤', greaterThan: '>', greaterThanOrEqual: '≥' };
  return `${question.table}.${question.field} ${words[question.operator]} ${JSON.stringify(value)}`;
}

// The answer as data: which rows, the reply text and the Studio tool calls that show it.
export function planAnswer(text, data, { slotExists = {} } = {}) {
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
  const calls = [
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
  const steps = [
    ...(slotExists[question.page] ? ['`remove_widget`: the previous answer'] : []),
    `\`add_widget\`: a grid in the answer slot under the headline tiles of the ${question.page === 'guide' ? 'Guide and Channel3 evidence' : 'Evidence readiness'} page`,
    `\`configure_widget\`: title and ${question.columns.length} columns from ${question.table}`,
    `\`add_widget_filter\`: ${describeFilter(question, value)}`,
  ];
  const reply = `${question.say(matched, rows)} How I built this: ${steps.map((step, index) => `${index + 1}. ${step}`).join(' ')}. ${BOUNDARY}`;
  const key = { cases: 'case_ref', time_events: 'event_id', requirements: 'requirement_id', benchmark: 'flow_id', receipts: 'receipt_id' }[question.table];
  return { intent: question.id, refs: matched.map((row) => row[key]), calls, page: question.page, reply, filter };
}

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
//   delegate   optional `tools.delegateTo(['lead'])`, only when the built-in agents are live
//   recording  optional validated recording (agentRecording.js), replayed when the agents are not live
//   recorder   optional recorder, in record mode only            onAnswer  called with the page that changed
export function createEvidenceAuditor({ studio, getState, data, delegate = null, recording = null, recorder = null, onAnswer = () => {} }) {
  let sequence = 0;
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
        const question = lastUserText(input.messages || []);
        const state = getState();
        const slotExists = Object.fromEntries(Object.entries(ANSWER_SLOTS)
          .map(([page, widgetId]) => [page, Boolean(state?.pages?.find((entry) => entry.id === page)?.widgets?.[widgetId])]));
        const plan = planAnswer(question, data, { slotExists });
        if (plan.intent === 'built_in') {
          const recorded = recording ? ` A run recorded on ${recording.recorded_at.slice(0, 10)} can be replayed here: ask "${recording.runs[0].question}".` : '';
          yield* say(messageId, `${mode === 'live' ? BUILT_IN_LIVE : `${BUILT_IN_OFF}${recorded}`} I am the evidence auditor: I answer my own questions with code. ${BOUNDARY}`);
          yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'built_in' } };
          return;
        }
        if (plan.intent === 'unknown') {
          if (mode === 'live') {
            // Hand the question to Studio's lead agent; it plans and delegates to the page and widget agents.
            recorder?.begin(question, state?.selectedPageId || ANSWER_PAGE_ID);
            const tool = delegate;
            const toolCallId = `${runId}-delegate`;
            const args = { type: { id: 'lead' }, instructions: question };
            yield { type: 'TOOL_CALL_START', toolCallId, toolCallName: tool.name };
            yield { type: 'TOOL_CALL_ARGS', toolCallId, delta: JSON.stringify(args) };
            yield { type: 'TOOL_CALL_END', toolCallId };
            const result = await tool.execute({ toolCallId, name: tool.name, args }, toolCtx);
            const summary = result.success ? result.response : result.issues.map((issue) => issue.message).join('; ');
            yield { type: 'TOOL_CALL_RESULT', messageId: `${toolCallId}-result`, toolCallId, role: 'tool', content: summary };
            recorder?.end(summary);
            yield* say(messageId, `That is outside my fixed questions, so I handed it to Studio's lead agent (Gemini, through the console's governed route). Its summary: ${summary} ${BOUNDARY}`);
            yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'delegated', ok: result.success } };
            return;
          }
          const recorded = mode === 'replay' ? findRecordedRun(recording, question) : null;
          if (recorded) {
            yield* replayRun(recorded, { studio, getState, toolContext: toolCtx, idPrefix: `${runId}-replay` });
            onAnswer(recorded.page_id);
            yield* say(messageId, `${recordingLabel(recording)} The lead agent's answer then: ${recorded.reply} ${BOUNDARY}`);
            yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'replayed' } };
            return;
          }
          const offer = mode === 'replay' ? ` A recorded run of Studio's lead agent can be replayed for: ${recording.runs.map((run) => `"${run.question}"`).join(', ')}.` : ` ${BUILT_IN_OFF}`;
          yield* say(messageId, `I answer fixed questions with code: ${QUESTIONS.map((entry) => entry.label).join(' ')}${offer} ${BOUNDARY}`);
          yield { type: 'RUN_FINISHED', threadId, runId, result: { intent: 'unknown' } };
          return;
        }
        for (const call of plan.calls) {
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
        if (plan.page) onAnswer(plan.page);
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
  else if (recording) starters.push({ label: `${recording.runs[0].question} (recorded)`, prompt: recording.runs[0].question });
  starters.push({ label: 'Are the built-in agents on?', prompt: 'Are the built-in agents on?' });
  return starters;
}
export const PROMPT_STARTERS = Object.freeze(promptStarters());
