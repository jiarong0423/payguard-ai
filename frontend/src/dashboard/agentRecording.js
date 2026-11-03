// A recorded run of Studio's built-in agents, for the hosted dashboard that never calls a model.
//
// The owner records one real run locally (tools/record_studio_agent_run.mjs, live Gemini through the governed
// backend route): the question, every Studio tool call the agents made, the final reply, timings and the final
// layout of the page. No key and no personal data: the key never reaches the browser, the question is checked,
// and the file is validated below. The hosted dashboard then replays the recorded Studio tool calls with the real
// Studio tools, labelled as a recording; no model is called. Pure module: node tests drive it.

export const RECORDING_SCHEMA = 'payguard.studio_agent_run.v1';
export const MAX_RUNS = 5;
export const MAX_STEPS = 80;
export const MAX_ARGS_CHARS = 16384;
export const MAX_REPLY_CHARS = 4000;

// Studio tools that change the canvas, as Studio's tool names and the AgAiStudioTools method that builds each.
export const REPLAYED_TOOLS = Object.freeze({
  add_widget: 'addWidget', position_widget: 'positionWidget', remove_widget: 'removeWidget', configure_widget: 'configureWidget',
  add_page_filter: 'addPageFilter', remove_page_filter: 'removePageFilter', add_widget_filter: 'addWidgetFilter',
  remove_widget_filter: 'removeWidgetFilter', create_expression: 'createExpression', update_expression: 'updateExpression',
  delete_expression: 'deleteExpression',
});
// Read-only or conversation tools: recorded for the "how it was built" list, not executed again.
export const READ_ONLY_TOOLS = Object.freeze(['view_schema', 'view_report', 'view_page', 'view_widget', 'execute_query',
  'view_plan', 'create_plan', 'update_plan', 'clear_plan', 'rename_thread', 'delegate_to', 'complete_task']);
const AGENTS = ['evidence-auditor', 'lead', 'data', 'page', 'planning', 'widget'];

const EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/u;
const LONG_NUMBER = /(?:\d[\s().-]*){9,}/u;
const KEY_LIKE = /AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{20,}|ya29\.[0-9A-Za-z_-]+|-----BEGIN/u;

function fail(reason) {
  throw new Error(`studio_recording_invalid: ${reason}`);
}

function exact(value, keys, where) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(`${where} is not an object`);
  const actual = Object.keys(value).sort();
  if (JSON.stringify(actual) !== JSON.stringify([...keys].sort())) fail(`${where} keys ${actual.join(',')}`);
}

function cleanStrings(value, where) {
  if (typeof value === 'string') {
    if (EMAIL.test(value) || KEY_LIKE.test(value)) fail(`${where} holds personal data or a key`);
    return;
  }
  if (Array.isArray(value)) value.forEach((item, index) => cleanStrings(item, `${where}[${index}]`));
  else if (value && typeof value === 'object') Object.entries(value).forEach(([key, item]) => cleanStrings(item, `${where}.${key}`));
}

export function validateRecording(doc) {
  exact(doc, ['schema_version', 'recorded_at', 'model', 'source', 'affects_decision', 'runs', 'final_layout'], 'recording');
  if (doc.schema_version !== RECORDING_SCHEMA || doc.source !== 'gemini_live_local' || doc.affects_decision !== false) fail('header');
  if (typeof doc.recorded_at !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/u.test(doc.recorded_at)) fail('recorded_at');
  if (typeof doc.model !== 'string' || !/^gemini[A-Za-z0-9.-]{0,40}$/u.test(doc.model)) fail('model');
  if (!Array.isArray(doc.runs) || doc.runs.length < 1 || doc.runs.length > MAX_RUNS) fail('runs');
  doc.runs.forEach((run, index) => {
    const where = `runs[${index}]`;
    exact(run, ['question', 'page_id', 'steps', 'reply', 'turns', 'duration_ms'], where);
    if (typeof run.question !== 'string' || !run.question.trim() || run.question.length > 600 || LONG_NUMBER.test(run.question)) fail(`${where}.question`);
    if (typeof run.page_id !== 'string' || !/^[A-Za-z0-9_-]{1,40}$/u.test(run.page_id)) fail(`${where}.page_id`);
    if (typeof run.reply !== 'string' || run.reply.length > MAX_REPLY_CHARS) fail(`${where}.reply`);
    if (!Number.isInteger(run.turns) || run.turns < 0 || run.turns > 200) fail(`${where}.turns`);
    if (!Number.isInteger(run.duration_ms) || run.duration_ms < 0 || run.duration_ms > 3600000) fail(`${where}.duration_ms`);
    if (!Array.isArray(run.steps) || run.steps.length > MAX_STEPS) fail(`${where}.steps`);
    run.steps.forEach((step, stepIndex) => {
      const at = `${where}.steps[${stepIndex}]`;
      exact(step, ['agent', 'tool', 'args', 'ok', 'ms'], at);
      if (!AGENTS.includes(step.agent)) fail(`${at}.agent`);
      if (!(step.tool in REPLAYED_TOOLS) && !READ_ONLY_TOOLS.includes(step.tool)) fail(`${at}.tool ${step.tool}`);
      if (!step.args || typeof step.args !== 'object' || Array.isArray(step.args) || JSON.stringify(step.args).length > MAX_ARGS_CHARS) fail(`${at}.args`);
      if (typeof step.ok !== 'boolean' || !Number.isInteger(step.ms) || step.ms < 0) fail(`${at}.ok/ms`);
    });
  });
  exact(doc.final_layout, ['page_id', 'widgets', 'widget_layout'], 'final_layout');
  if (JSON.stringify(doc.final_layout).length > 65536) fail('final_layout size');
  cleanStrings(doc, 'recording');
  return doc;
}

export function recordingLabel(doc) {
  return `Recorded on ${doc.recorded_at.slice(0, 10)} with Gemini; replayed here, no model call.`;
}

const normal = (text) => String(text || '').toLowerCase().replace(/[^a-z0-9 ]+/gu, ' ').replace(/\s+/gu, ' ').trim();

export function findRecordedRun(doc, question) {
  if (!doc) return null;
  const wanted = normal(question);
  return doc.runs.find((run) => normal(run.question) === wanted) || null;
}

// Collects one run from Studio's telemetry stream. The auditor calls begin() when it hands a question to the
// lead agent and end() with the final reply; every tool execution in between, by any agent, is a step.
export function createRecorder({ now = () => Date.now(), getState } = {}) {
  let current = null;
  const runs = [];
  const open = new Map();
  return {
    observer: {
      onEvent(event) {
        if (!current) return;
        if (event.type === 'turn_started') current.turns += 1;
        if (event.type === 'tool_execution_started') {
          open.set(event.toolCallId, current.steps.length);
          current.steps.push({ agent: event.trace?.agentId || 'lead', tool: event.name, args: event.args && typeof event.args === 'object' ? event.args : {}, ok: false, ms: event.timestamp || now() });
        }
        if (event.type === 'tool_execution_finished' && open.has(event.toolCallId)) {
          const step = current.steps[open.get(event.toolCallId)];
          step.ok = event.ok === true;
          step.ms = Math.max(0, Math.round((event.timestamp || now()) - step.ms));
          open.delete(event.toolCallId);
        }
      },
    },
    begin(question, pageId) {
      current = { question, page_id: pageId, steps: [], reply: '', turns: 0, started: now() };
    },
    end(reply) {
      if (!current) return;
      const { started, ...run } = current;
      run.steps = run.steps.map((step) => ({ ...step, ms: step.ms > 1e11 ? 0 : step.ms }));
      runs.push({ ...run, reply: String(reply || '').slice(0, MAX_REPLY_CHARS), duration_ms: Math.max(0, Math.round(now() - started)) });
      current = null;
    },
    finish({ recordedAt = new Date().toISOString(), model = 'gemini' } = {}) {
      const state = getState?.();
      const pageId = runs.at(-1)?.page_id || state?.selectedPageId;
      const page = state?.pages?.find((entry) => entry.id === pageId) || { widgets: {}, widgetLayout: {} };
      return validateRecording({
        schema_version: RECORDING_SCHEMA, recorded_at: recordedAt.replace(/\.\d{3}Z$/u, 'Z'), model, source: 'gemini_live_local',
        affects_decision: false, runs: runs.slice(0, MAX_RUNS),
        final_layout: { page_id: pageId, widgets: page.widgets || {}, widget_layout: page.widgetLayout || {} },
      });
    },
  };
}

// Re-run one recorded run with Studio's tools: the canvas changes exactly as it did when recorded.
export async function* replayRun(run, { studio, getState, toolContext, idPrefix = 'replay' }) {
  const widgetTypes = new Map();
  let index = 0;
  for (const step of run.steps) {
    index += 1;
    if (step.tool === 'add_widget' && step.args.widgetId) widgetTypes.set(step.args.widgetId, step.args.type);
    const method = REPLAYED_TOOLS[step.tool];
    if (!method || !step.ok) continue;
    let tool;
    if (method === 'configureWidget') {
      const widgetId = step.args.widgetId;
      const page = getState()?.pages?.find((entry) => entry.id === run.page_id);
      const widgetType = step.args.value?.type || widgetTypes.get(widgetId) || page?.widgets?.[widgetId]?.type;
      if (!widgetId || !widgetType) continue;
      tool = studio.configureWidget({ widgetType, widgetId }, { pageId: run.page_id });
    } else {
      tool = studio[method]({ pageId: run.page_id });
    }
    const toolCallId = `${idPrefix}-${index}`;
    yield { type: 'TOOL_CALL_START', toolCallId, toolCallName: tool.name };
    yield { type: 'TOOL_CALL_ARGS', toolCallId, delta: JSON.stringify(step.args) };
    yield { type: 'TOOL_CALL_END', toolCallId };
    const result = await tool.execute({ toolCallId, name: tool.name, args: step.args }, toolContext);
    yield { type: 'TOOL_CALL_RESULT', messageId: `${toolCallId}-result`, toolCallId, role: 'tool',
      content: result.success ? result.response : result.issues.map((issue) => issue.message).join('; ') };
  }
}
