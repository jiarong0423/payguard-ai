// AG Studio built-in agents through the governed Gemini route, with a fake model only (no network, no key).
//   1. Adapter contract: AgLlmRequest -> closed wire turn, reply -> Studio output items and stream events,
//      session and CSRF headers, failures surface as a failed turn, the status probe says "off" on any doubt.
//   2. Recording: schema, personal data and key-like strings refused, recorder output from telemetry events.
//   3. Replay: the recorded Studio tool calls run again with Studio's tools; read-only and failed steps do not.
//   4. Auditor: questions outside its set go to the data agent (after a yes) when live, to a recorded run when not.
//   5. Wiring in main.jsx: live agents only when the backend says live; record mode only when live.
//   6. Browser (skipped without Playwright): a fresh build, the real Studio agent loop driven by a fake model
//      behind route interception; the lead agent delegates, the page agent adds a widget, the recorder records it.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { createGeminiAdapter, createSessionClient, FORCE_FINISH_AFTER_TURNS, fetchAgentStatus, toStudioResponse, toWireTurn, TURN_PATH } from '../frontend/src/dashboard/studioAgentClient.js';
import { createRecorder, findRecordedRun, READ_ONLY_TOOLS, RECORDING_SCHEMA, recordingLabel, REPLAYED_TOOLS, replayRun, validateRecording } from '../frontend/src/dashboard/agentRecording.js';
import { createEvidenceAuditor, DELEGATE_CONFIRM_TEXT, DELEGATE_EXAMPLE, DELEGATE_INSTRUCTIONS_MAX, delegateInstructions, isDelegateConfirmation, NO_SUMMARY, NOT_FINISHED_TEXT, plainSummary, promptStarters, readableTimes, readsAsJudgement, WITHHELD_TEXT } from '../frontend/src/dashboard/auditor.js';
import { studioData } from '../frontend/src/dashboard/dashboardData.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const frontendRoot = join(projectRoot, 'frontend');
const read = (path) => readFileSync(resolve(projectRoot, path), 'utf8');
const json = (path) => JSON.parse(read(path));

// 1. Adapter contract ------------------------------------------------------------------------------------------
const studioRequest = {
  instructions: 'You are the Orchestrator.',
  input: [
    { id: 'u1', kind: 'input', type: 'message', role: 'user', status: 'completed', content: [{ type: 'text', text: DELEGATE_EXAMPLE }] },
    { id: 's1', kind: 'input', type: 'message', role: 'system', status: 'completed', content: [{ type: 'text', text: 'Page ids: readiness, guide.' }] },
    { id: 'r1', kind: 'output', type: 'reasoning', summary: [{ type: 'summary', text: 'private' }] },
    { id: 'c1', kind: 'output', type: 'function_call', callId: 'call_1', name: 'view_page', arguments: '{}' },
    { type: 'function_call_output', callId: 'call_1', output: '{"widgets":3}', status: 'completed' },
    { id: 'a1', kind: 'output', type: 'message', role: 'assistant', status: 'completed', content: [{ type: 'text', text: 'Looking at the page.', annotations: [] }] },
  ],
  tools: [{ name: 'delegate_to', description: 'Delegate.', parameters: { type: 'object' } }, { name: 'web_search', description: 'x', parameters: {}, kind: 'provided' }],
  toolChoice: { name: 'delegate_to' },
  responseFormat: { type: 'text' },
};
const wire = toWireTurn(studioRequest);
{
  // (red team r27 A) From turn FORCE_FINISH_AFTER_TURNS of one thread, a request offering complete_task must call it.
  const sentBodies = [];
  const fakeClient = { json: async (path, { body }) => { sentBodies.push(body); return { output: [{ type: 'text', text: 'ok' }], model: 'gemini', affects_decision: false }; } };
  const adapter = createGeminiAdapter(fakeClient);
  const finishing = { ...studioRequest, toolChoice: 'auto', tools: [...studioRequest.tools, { name: 'complete_task', description: 'Finish.', parameters: { type: 'object' } }] };
  for (let index = 0; index < 6; index += 1) await adapter.executeTurn(finishing, { trace: { threadId: 'child-1' } }).complete;
  await adapter.executeTurn(finishing, { trace: { threadId: 'child-2' } }).complete;
  await adapter.executeTurn({ ...studioRequest, toolChoice: 'auto' }, { trace: { threadId: 'child-1' } }).complete;
  assert.equal(FORCE_FINISH_AFTER_TURNS, 5);
  assert.deepEqual(sentBodies.slice(0, 4).map((body) => body.tool_choice), ['auto', 'auto', 'auto', 'auto']);
  assert.deepEqual(sentBodies.slice(4, 6).map((body) => body.tool_choice), [{ name: 'complete_task' }, { name: 'complete_task' }], 'forced from the fifth turn');
  assert.equal(sentBodies[6].tool_choice, 'auto', 'another thread counts on its own');
  assert.equal(sentBodies[7].tool_choice, 'auto', 'no forcing when complete_task is not offered');
}
assert.deepEqual(Object.keys(wire).sort(), ['instructions', 'items', 'response_format', 'tool_choice', 'tools']);
assert.deepEqual(wire.items, [
  { kind: 'user', text: DELEGATE_EXAMPLE },
  { kind: 'context', text: 'Page ids: readiness, guide.' },
  { kind: 'call', call_id: 'call_1', name: 'view_page', arguments: '{}' },
  { kind: 'result', call_id: 'call_1', output: '{"widgets":3}' },
  { kind: 'assistant', text: 'Looking at the page.' },
], 'reasoning dropped, roles mapped, nothing else added');
assert.deepEqual(wire.tools.map((tool) => tool.name), ['delegate_to'], 'only client tools are advertised');
assert.deepEqual(wire.tool_choice, { name: 'delegate_to' });
assert.throws(() => toWireTurn({ ...studioRequest, input: [{ kind: 'input', type: 'message', role: 'user', content: [{ type: 'image', imageUrl: 'https://x/y.png' }] }] }), /unsupported_content/u, 'images refused');
assert.throws(() => toWireTurn({ ...studioRequest, input: [{ type: 'mystery' }] }), /unsupported_item/u);
assert.deepEqual(toWireTurn({ ...studioRequest, responseFormat: { type: 'json', name: 'Plan', schema: { type: 'object' } } }).response_format, { type: 'json', name: 'Plan', schema: { type: 'object' } });

const reply = { output: [{ type: 'call', call_id: 'call_x', name: 'add_widget', arguments: '{"widgetId":"w"}' }, { type: 'text', text: 'Done.' }], model: 'gemini', affects_decision: false };
const converted = toStudioResponse(reply, 'turn-1');
assert.deepEqual(converted.output.map((item) => [item.type, item.callId || item.content?.[0]?.text]), [['function_call', 'call_x'], ['message', 'Done.']]);
assert.deepEqual(converted.events.map((event) => event.type), ['TOOL_CALL_START', 'TOOL_CALL_ARGS', 'TOOL_CALL_END', 'TEXT_MESSAGE_START', 'TEXT_MESSAGE_CONTENT', 'TEXT_MESSAGE_END']);

function stubFetch(routes) {
  const calls = [];
  const impl = async (path, init) => {
    calls.push({ path, method: init.method, headers: init.headers, body: init.body ? JSON.parse(init.body) : undefined });
    const [status, payload] = routes[path] ? routes[path](init) : [404, { error: { code: 'not_found' } }];
    return { ok: status < 400, status, json: async () => payload };
  };
  return { impl, calls };
}
const session = { session_id: 'S'.repeat(43), csrf_token: 'C'.repeat(43) };
const live = stubFetch({
  '/api/v1/demo/sessions': () => [201, session],
  '/api/v1/studio/agent-status': () => [200, { built_in_agents: 'live', reason: null, affects_decision: false }],
  [TURN_PATH]: () => [200, reply],
});
const client = createSessionClient(live.impl);
assert.equal(await fetchAgentStatus(client), 'live');
const handler = createGeminiAdapter(client).executeTurn(studioRequest);
const streamed = [];
for await (const event of handler.stream) streamed.push(event.type);
const completed = await handler.complete;
assert.equal(completed.status, 'completed');
assert.equal(completed.output.length, 2);
assert.equal(streamed.length, 6);
assert.deepEqual(live.calls.map((call) => `${call.method} ${call.path}`), ['POST /api/v1/demo/sessions', 'GET /api/v1/studio/agent-status', `POST ${TURN_PATH}`], 'one session, created first');
assert.equal(live.calls[2].headers['X-CSRF-Token'], session.csrf_token, 'turns carry the CSRF token');
assert.equal(live.calls[1].headers['X-CSRF-Token'], undefined, 'reads do not');
assert.deepEqual(live.calls[2].body, wire, 'the closed wire turn is what is sent');
const refused = stubFetch({ '/api/v1/demo/sessions': () => [201, session], [TURN_PATH]: () => [503, { error: { code: 'hosted_demo_disabled', message: 'disabled' } }] });
const failedTurn = await createGeminiAdapter(createSessionClient(refused.impl)).executeTurn(studioRequest).complete;
assert.deepEqual([failedTurn.status, failedTurn.error.code, failedTurn.output], ['failed', 'hosted_demo_disabled', []]);
for (const routes of [{ '/api/v1/demo/sessions': () => [201, session], '/api/v1/studio/agent-status': () => [200, { built_in_agents: 'off', reason: 'hosted_demo' }] }, {}]) {
  assert.equal(await fetchAgentStatus(createSessionClient(stubFetch(routes).impl)), 'off', 'off on the hosted demo or with no backend');
}

// 2. Recording --------------------------------------------------------------------------------------------------
const run = {
  question: DELEGATE_EXAMPLE, page_id: 'readiness', reply: 'I added a column chart comparing cases by days to due.', turns: 6, duration_ms: 9100,
  steps: [
    { agent: 'page', tool: 'view_page', args: {}, ok: true, ms: 3 },
    { agent: 'page', tool: 'add_widget', args: { widgetId: 'days-chart', type: 'column-chart-grouped', xTrack: 0, yTrack: 99, xSpan: 12, ySpan: 14 }, ok: true, ms: 12 },
    { agent: 'widget', tool: 'configure_widget', args: { widgetId: 'days-chart', op: 'patch', value: { dataMapping: { categoryKey: [{ id: 'cases.case_ref' }], valueKey: [{ id: 'cases.days_to_due', aggregation: 'sum' }] } } }, ok: true, ms: 20 },
    { agent: 'widget', tool: 'add_widget_filter', args: { widgetId: 'days-chart', op: 'append', value: {} }, ok: false, ms: 5 },
  ],
};
const recording = { schema_version: RECORDING_SCHEMA, recorded_at: '2026-11-02T10:00:00Z', model: 'gemini', source: 'gemini_live_local', affects_decision: false, runs: [run],
  final_layout: { page_id: 'readiness', widgets: { 'days-chart': { type: 'column-chart-grouped' } }, widget_layout: { 'days-chart': { xTrack: 0, yTrack: 99, xSpan: 12, ySpan: 14 } } } };
assert.equal(validateRecording(structuredClone(recording)).runs.length, 1);
assert.equal(recordingLabel(recording), 'Recorded live run (Gemini, 2026-11-02), no model call here.');
const clone = () => structuredClone(recording);
for (const [label, mutate] of [
  ['extra field', (doc) => { doc.extra = 1; }],
  ['wrong schema', (doc) => { doc.schema_version = 'v0'; }],
  ['decision flag', (doc) => { doc.affects_decision = true; }],
  ['email in a reply', (doc) => { doc.runs[0].reply = 'Mail jane@example.com'; }],
  ['key-like string', (doc) => { doc.runs[0].steps[1].args.note = `AIza${'x'.repeat(30)}`; }],
  ['phone in the question', (doc) => { doc.runs[0].question = 'call 415 555 0199'; }],
  ['unknown tool', (doc) => { doc.runs[0].steps[0].tool = 'send_email'; }],
  ['unknown agent', (doc) => { doc.runs[0].steps[0].agent = 'stranger'; }],
  ['too many runs', (doc) => { doc.runs = Array(6).fill(doc.runs[0]); }],
]) {
  const doc = clone();
  mutate(doc);
  assert.throws(() => validateRecording(doc), /studio_recording_invalid/u, label);
}
for (const tool of Object.keys(REPLAYED_TOOLS)) assert.ok(!READ_ONLY_TOOLS.includes(tool));
assert.equal(findRecordedRun(recording, '  which REASON code appears most often across the three cases!! ')?.question, DELEGATE_EXAMPLE, 'question match ignores case and punctuation');
assert.equal(findRecordedRun(recording, 'something else'), null);
assert.equal(existsSync(resolve(projectRoot, 'frontend/src/data/studio_agent_run_v1.json'))
  ? validateRecording(json('frontend/src/data/studio_agent_run_v1.json')).source : 'none', existsSync(resolve(projectRoot, 'frontend/src/data/studio_agent_run_v1.json')) ? 'gemini_live_local' : 'none',
'a committed recording, if any, passes the schema');

let clock = 1000;
const recorder = createRecorder({ now: () => clock, getState: () => ({ selectedPageId: 'readiness', pages: [{ id: 'readiness', widgets: { w: { type: 'grid' } }, widgetLayout: { w: { xTrack: 0, yTrack: 0, xSpan: 24, ySpan: 9 } } }] }) });
recorder.observer.onEvent({ type: 'tool_execution_started', toolCallId: 'ignored', name: 'add_widget', args: {} });
recorder.begin(DELEGATE_EXAMPLE, 'readiness');
recorder.observer.onEvent({ type: 'turn_started', trace: { agentId: 'lead' } });
recorder.observer.onEvent({ type: 'tool_execution_started', trace: { agentId: 'page' }, toolCallId: 't1', name: 'add_widget', args: { widgetId: 'w' }, timestamp: 2000 });
recorder.observer.onEvent({ type: 'tool_execution_finished', trace: { agentId: 'page' }, toolCallId: 't1', name: 'add_widget', ok: true, timestamp: 2045 });
clock = 4000;
recorder.end('Done.');
const recorded = recorder.finish({ recordedAt: '2026-11-02T10:00:00.123Z' });
assert.deepEqual(recorded.runs, [{ question: DELEGATE_EXAMPLE, page_id: 'readiness', steps: [{ agent: 'page', tool: 'add_widget', args: { widgetId: 'w' }, ok: true, ms: 45 }], reply: 'Done.', turns: 1, duration_ms: 3000 }], 'only events between begin and end');
assert.equal(recorded.recorded_at, '2026-11-02T10:00:00Z');
assert.deepEqual(Object.keys(recorded.final_layout.widgets), ['w']);

// 3. Replay ----------------------------------------------------------------------------------------------------
function standInStudio() {
  const calls = [];
  const make = (name, toolName) => (...bind) => ({
    name: toolName, kind: 'client', schema: () => ({}),
    async execute(invocation, ctx) { calls.push({ toolName, bind, args: invocation.args }); return ctx.success(`${toolName} ok`); },
  });
  return { calls, studio: Object.fromEntries(Object.entries(REPLAYED_TOOLS).map(([tool, method]) => [method, make(method, tool)])) };
}
const ctx = { signal: new AbortController().signal, run: { threadId: 't', runId: 'r' }, success: (response) => ({ success: true, response }), error: (message) => ({ success: false, issues: [{ message }] }) };
const replayed = standInStudio();
const replayEvents = [];
for await (const event of replayRun(run, { studio: replayed.studio, getState: () => ({ pages: [] }), toolContext: ctx })) replayEvents.push(event);
assert.deepEqual(replayed.calls.map((call) => call.toolName), ['add_widget', 'configure_widget'], 'read-only and failed steps are not replayed');
assert.deepEqual(replayed.calls[1].bind, [{ widgetType: 'column-chart-grouped', widgetId: 'days-chart' }, { pageId: 'readiness' }], 'configure_widget bound to the widget type the recording added');
assert.deepEqual(replayed.calls[0].bind, [{ pageId: 'readiness' }]);
assert.equal(replayEvents.filter((event) => event.type === 'TOOL_CALL_RESULT').length, 2);

// 4. Auditor: delegation when live, replay when recorded ----------------------------------------------------------
const tables = Object.fromEntries(studioData({ disputes: json('frontend/src/data/dashboard_disputes_v1.json'), benchmark: json('frontend/src/data/guide_benchmark_v1.json'), receipts: json('frontend/src/data/channel3_receipts_v1.json') })
  .sources.map((source) => [source.id, source.data]));
async function runTurns(options, texts) {
  const agent = createEvidenceAuditor({ studio: standInStudio().studio, getState: () => ({ selectedPageId: 'readiness', pages: [] }), data: tables, ...options });
  const turns = [];
  for (const text of texts) {
    const events = [];
    for await (const event of agent.run({ threadId: 't', runId: 'r', messages: [{ id: 'u', role: 'user', content: text }] })) events.push(event);
    turns.push({ events, reply: events.filter((event) => event.type === 'TEXT_MESSAGE_CONTENT').map((event) => event.delta).join('') });
  }
  return turns;
}
const runAuditor = async (options, text) => (await runTurns(options, [text]))[0];
const delegated = [];
const delegate = { name: 'delegate_to', kind: 'client', schema: () => ({}), async execute(invocation, toolCtx) { delegated.push(invocation.args); return toolCtx.success('Added a column chart days-chart.'); } };
const begun = [];
// (foolproofing 2026-11-04) The first turn only asks; nothing is delegated until a plain yes.
const [askFirst, liveRun] = await runTurns({ delegate, recorder: { begin: (...args) => begun.push(['begin', ...args]), end: (summary) => begun.push(['end', summary]) } }, [DELEGATE_EXAMPLE, 'yes']);
assert.ok(askFirst.reply.includes(DELEGATE_CONFIRM_TEXT), 'the auditor asks before spending Studio calls');
assert.equal(askFirst.events.at(-1).result.intent, 'confirm_delegation');
assert.deepEqual(delegated, [{ type: { id: 'data' }, instructions: delegateInstructions(DELEGATE_EXAMPLE) }], 'handed to the data agent with the scope prefix and the question');
assert.deepEqual(begun, [['begin', DELEGATE_EXAMPLE, 'readiness'], ['end', 'Added a column chart days-chart.']]);
assert.match(liveRun.reply, /handed it to Studio's data agent.*Its answer: Added a column chart days-chart\./u);
// (red team r27 A) Scope, length, unfinished runs and judgement wording.
assert.ok(delegateInstructions(DELEGATE_EXAMPLE).endsWith(`Question: ${DELEGATE_EXAMPLE}`));
assert.ok(delegateInstructions('x'.repeat(2000)).length <= DELEGATE_INSTRUCTIONS_MAX, 'prefix plus question fits the 600-character user item');
assert.equal(/\d/u.test(delegateInstructions('')), false, 'the prefix carries no digits (the 9-digit check)');
for (const [reply, success, shown, ok] of [
  [NO_SUMMARY, true, NOT_FINISHED_TEXT, false],
  ['', true, NOT_FINISHED_TEXT, false],
  ['agent turn failed', false, NOT_FINISHED_TEXT, false],
  ['The buyer is likely to win this one.', true, WITHHELD_TEXT, false],
  ['Item not received appears in all 3 cases.', true, 'Item not received appears in all 3 cases.', true],
]) {
  const told = [];
  const fake = { name: 'delegate_to', kind: 'client', schema: () => ({}), async execute(invocation, toolCtx) { return success ? toolCtx.success(reply) : toolCtx.error(reply); } };
  const [, run] = await runTurns({ delegate: fake, onDelegated: (value) => told.push(value) }, [DELEGATE_EXAMPLE, 'yes']);
  assert.ok(run.reply.includes(`Its answer: ${shown}`), `${reply} -> ${shown}`);
  assert.deepEqual(told, [{ question: DELEGATE_EXAMPLE, summary: shown, ok }], 'the answer is also reported outside the Studio thread');
}
assert.equal(plainSummary('In @table[cases], the reason is "Item not received". Breakdown by @field[cases.case_ref]: - @field[cases.case_ref] `case-ref-001`: @field[cases.reason] = `Item not received`'),
  'In cases, the reason is "Item not received". Breakdown by case_ref · case_ref case-ref-001: reason = Item not received', 'status line shows plain text');
// (judge rerun 2026-11-12 S1) Recorded replies show readable UTC dates, not raw ISO stamps; invalid dates stay as written.
assert.equal(plainSummary('@field[cases.due_date]: 2026-11-10T04:04:52.527Z'), 'due_date: Nov 10, 2026, 04:04 UTC', 'ISO stamp becomes a readable UTC date');
assert.equal(readableTimes('due 2026-02-30T04:04:52Z'), 'due 2026-02-30T04:04:52Z', 'an impossible date is left as written');
assert.ok(!/\d{4}-\d{2}-\d{2}T/u.test(plainSummary(json('frontend/src/data/studio_agent_run_v1.json').runs.map((run) => run.reply).join(' '))), 'no recorded reply shows a raw ISO stamp');
for (const text of ['in the seller\'s favour', 'the merchant is at fault', 'a strong case', 'the buyer won']) assert.ok(readsAsJudgement(text), text);
for (const text of ['Item not received appears 3 times.', 'Two cases have no delivery attachment.', 'refund record missing']) assert.equal(readsAsJudgement(text), false, text);
assert.equal(liveRun.events.at(-1).result.intent, 'delegated');
const [, notYes] = await runTurns({ delegate }, [DELEGATE_EXAMPLE, 'no, which cases are due soon?']);
assert.equal(delegated.length, 1, 'anything but a plain yes cancels the pending delegation');
assert.equal(notYes.events.at(-1).result.intent === 'delegated', false);
const yesAlone = await runAuditor({ delegate }, 'yes');
assert.equal(delegated.length, 1, 'a yes with nothing pending delegates nothing');
assert.equal(yesAlone.events.at(-1).result.intent, 'confirm_delegation');
await runTurns({ delegate }, ['yes', 'yes']);
assert.equal(delegated.length, 1, 'two bare yeses never delegate the word "yes"');
{
  // Two Studio threads share one auditor object: a yes in thread B never confirms thread A's question.
  const handed = [];
  const own = { ...delegate, async execute(invocation, toolCtx) { handed.push(invocation.args); return toolCtx.success('done'); } };
  const agent = createEvidenceAuditor({ studio: standInStudio().studio, getState: () => ({ selectedPageId: 'readiness', pages: [] }), data: tables, delegate: own });
  const turn = async (threadId, text) => { for await (const event of agent.run({ threadId, runId: `${threadId}-r`, messages: [{ id: 'u', role: 'user', content: text }] })) void event; };
  await turn('A', DELEGATE_EXAMPLE);
  await turn('B', 'yes');
  assert.equal(handed.length, 0, 'a yes in another thread does not delegate');
  await turn('A', 'yes');
  assert.deepEqual(handed, [{ type: { id: 'data' }, instructions: delegateInstructions(DELEGATE_EXAMPLE) }], 'the yes in the same thread delegates its own question');
}
for (const word of ['yes', 'Yes.', ' ok ', 'send it', 'continue!']) assert.ok(isDelegateConfirmation(word), word);
for (const word of ['yes please do the widget', 'yesterday', 'no', '', null]) assert.equal(isDelegateConfirmation(word), false, String(word));
const ownQuestion = await runAuditor({ delegate }, 'Which cases lack proof of delivery?');
assert.equal(delegated.length, 1, 'fixed questions are never delegated');
assert.match(ownQuestion.reply, /How I built this/u);
const replayRunResult = await runAuditor({ recording }, DELEGATE_EXAMPLE);
assert.match(replayRunResult.reply, /Recorded live run \(Gemini, 2026-11-02\), no model call here\. The data agent's answer then: I added a column chart/u);
assert.equal(replayRunResult.events.filter((event) => event.type === 'TOOL_CALL_START').length, 2);
const offer = await runAuditor({ recording }, 'Something else entirely');
assert.match(offer.reply, /can be replayed for: "Which reason code appears most often across the three cases\?"/u);
assert.deepEqual(promptStarters({ mode: 'live' }).map((entry) => entry.prompt).slice(-2), [DELEGATE_EXAMPLE, 'Are the built-in agents on?']);
assert.equal(promptStarters({ mode: 'replay', recording }).at(-2).label, `${DELEGATE_EXAMPLE} (recorded live run)`);

// 5. Wiring -----------------------------------------------------------------------------------------------------
const mainSource = read('frontend/src/dashboard/main.jsx');
for (const text of [
  "mode: status === 'live' ? 'live' : RECORDING ? 'replay' : 'off'",
  "BUILT_IN_AGENT_IDS.map((id) => directLlmRunner({ ...builtIn[id], adapter, maxTurns: STUDIO_MAX_TURNS }))",
  "const STUDIO_MAX_TURNS = 8;",
  "delegate: live ? tools.delegateTo(['data']) : null, recording: live ? null : RECORDING,",
  'data-testid="dashboard-delegated"',
  "import.meta.glob('../data/studio_agent_run_v1.json', { eager: true, import: 'default' })",
  "RECORD_MODE && setup.mode === 'live' ? createRecorder(",
  "observers: recorder ? [recorder.observer] : [],",
]) assert.ok(mainSource.includes(text), `main.jsx: ${text}`);
assert.equal(/<AgStudioProvider[^>]*\bkey=/u.test(mainSource), false, 'no remount key on the Studio provider (red team r27 B)');
assert.ok(read('backend/app/demo_mode.py').includes('("POST", "/api/v1/studio/agent-turn")'), 'the hosted demo refuses the turn route');
assert.ok(read('tools/record_studio_agent_run.mjs').includes("if (mode !== 'live') throw new Error"), 'the recorder refuses to run unless live');

// 6. Browser: the real Studio loop with a fake model (optional) -------------------------------------------------
let browserStage = 'UNVERIFIABLE (playwright is not available; browser stage not run; substitute evidence: module_health.mjs (CDP) + screenshots; set PAYGUARD_REQUIRE_RENDER=1 to make this a failure)';
let chromium;
try { ({ chromium } = createRequire(import.meta.url)('playwright')); } catch { chromium = null; }
if (chromium && existsSync(join(frontendRoot, 'node_modules', '.bin', 'vite'))) {
  const outDir = mkdtempSync(join(tmpdir(), 'payguard-studio-agent-'));
  const built = spawnSync(join(frontendRoot, 'node_modules', '.bin', 'vite'), ['build', '--outDir', outDir, '--emptyOutDir', '--logLevel', 'error'],
    { cwd: frontendRoot, encoding: 'utf8', env: { ...process.env, VITE_AG_STUDIO_LICENSE: '' } });
  assert.equal(built.status, 0, built.stderr || built.stdout);
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json', '.png': 'image/png' };
  const server = createServer((request, response) => {
    const path = normalize(join(outDir, decodeURIComponent(new URL(request.url, 'http://x').pathname)));
    if (!path.startsWith(outDir + sep) || !existsSync(path)) { response.writeHead(404); response.end(); return; }
    response.writeHead(200, { 'content-type': types[extname(path)] || 'application/octet-stream' });
    response.end(readFileSync(path));
  });
  await new Promise((done) => server.listen(0, '127.0.0.1', done));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
    const errors = [];
    const hosts = new Set();
    const turns = [];
    page.on('pageerror', (error) => errors.push(error.message));
    page.on('request', (request) => hosts.add(new URL(request.url()).origin));
    await page.route('**/api/v1/demo/sessions', (route) => route.fulfill({ status: 201, json: session }));
    await page.route('**/api/v1/studio/agent-status', (route) => route.fulfill({ json: { built_in_agents: 'live', reason: null, affects_decision: false } }));
    // The fake model plays the data agent: it never finishes on its own, so the adapter must force complete_task.
    await page.route(`**${TURN_PATH}`, (route) => {
      const body = route.request().postDataJSON();
      assert.equal(route.request().headers()['x-csrf-token'], session.csrf_token);
      turns.push(body.tool_choice);
      const output = typeof body.tool_choice === 'object' && body.tool_choice?.name === 'complete_task'
        ? [{ type: 'call', call_id: `call_finish_${turns.length}`, name: 'complete_task', arguments: JSON.stringify({ summary: 'Item not received appears in all 3 cases.' }) }]
        : [{ type: 'text', text: 'Looking at the rows.' }];
      route.fulfill({ json: { output, model: 'gemini', affects_decision: false } });
    });
    await page.goto(`${origin}/dashboard.html?record=1`);
    await page.getByTestId('widget-deadline').waitFor({ timeout: 30000 });
    assert.equal(await page.getByTestId('dashboard-built-in').getAttribute('data-mode'), 'live');
    await page.getByTestId('dashboard-mode').click();
    const box = page.getByPlaceholder('Ask the AI Assistant...');
    await box.fill(DELEGATE_EXAMPLE);
    await box.press('Enter');
    await page.getByText(/Reply "yes" to send it/).first().waitFor({ timeout: 30000 });
    await box.fill('yes');
    await box.press('Enter');
    await page.getByText(/handed it to Studio's data agent/).first().waitFor({ timeout: 30000 });
    assert.match(await page.getByTestId('dashboard-delegated').innerText(), /Item not received appears in all 3 cases\./u);
    assert.ok(turns.length <= 8, `at most 8 model turns (${turns.length})`);
    assert.ok(turns.some((choice) => choice?.name === 'complete_task'), 'the adapter forced complete_task');
    assert.deepEqual([...hosts], [origin], 'nothing leaves the page origin');
    assert.deepEqual(errors, []);
    browserStage = `PASS (${turns.length} fake model turns)`;
  } finally {
    await browser.close();
    server.close();
    rmSync(outDir, { recursive: true, force: true });
  }
}

// The static contract above passed; when the browser stage could not run the status says so instead of a bare PASS.
const browserUnverifiable = browserStage.startsWith('UNVERIFIABLE');
console.log(JSON.stringify({ status: browserUnverifiable ? 'PASS_STATIC_BROWSER_UNVERIFIABLE' : 'PASS', adapter: 'closed', recording_schema: RECORDING_SCHEMA, browser: browserStage }));
if (browserUnverifiable && process.env.PAYGUARD_REQUIRE_RENDER === '1') process.exit(1);

// Four recorded live runs (2026-11-09): the committed recording holds all four questions and replay finds each one.
{
  const committed = validateRecording(json('frontend/src/data/studio_agent_run_v1.json'));
  const questions = ['Which reason code appears most often across the three cases?', 'Which case is due first?', 'What is the total disputed amount across the three cases?', 'Which case has the most missing evidence?'];
  assert.deepEqual(committed.runs.map((entry) => entry.question), questions, 'four recorded questions, in order');
  assert.equal(committed.recorded_at.slice(0, 10), '2026-11-09', 'recorded_at is the latest run date');
  for (const question of questions) assert.ok(findRecordedRun(committed, question), `replay finds: ${question}`);
  assert.deepEqual(promptStarters({ mode: 'replay', recording: committed }).filter((entry) => entry.label.endsWith('(recorded live run)')).map((entry) => entry.prompt), questions, 'each recorded question is a clickable starter');
  assert.equal(recordingLabel(committed), 'Recorded live run (Gemini, 2026-11-09), no model call here.');
}
