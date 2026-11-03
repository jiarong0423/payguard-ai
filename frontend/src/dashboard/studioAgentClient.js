// Studio's built-in agents through the console's governed Gemini route (local live mode only).
//
// AG Studio runs its agents in the browser and asks an AgLlmAdapter for one model turn at a time. This adapter
// sends the turn to POST /api/v1/studio/agent-turn in a closed wire shape; the backend holds the key, applies
// the call caps and checks the reply. The hosted demo answers 503 there, and the status probe says "off".
// Pure module (no Studio import): node tests drive it with a stand-in fetch.

export const STATUS_PATH = '/api/v1/studio/agent-status';
export const TURN_PATH = '/api/v1/studio/agent-turn';
export const SESSION_PATH = '/api/v1/demo/sessions';

const textOf = (content) => (Array.isArray(content) ? content : [])
  .map((part) => {
    if (part?.type === 'text' && typeof part.text === 'string') return part.text;
    if (part?.type === 'refusal' && typeof part.refusal === 'string') return part.refusal;
    throw new Error('studio_turn_unsupported_content');
  }).join('\n');

// AgLlmRequest -> the closed shape backend/app/studio_agent.validate_turn accepts. Images and files are refused
// here (the dashboard never sends them); reasoning items are dropped, they are not sent back to the model.
export function toWireTurn(request) {
  const items = [];
  for (const item of request.input || []) {
    if (item.type === 'message' && item.kind === 'input') {
      const text = textOf(item.content);
      if (text.trim()) items.push({ kind: item.role === 'system' ? 'context' : 'user', text });
    } else if (item.type === 'message' && item.role === 'assistant') {
      const text = textOf(item.content);
      if (text.trim()) items.push({ kind: 'assistant', text });
    } else if (item.type === 'function_call') {
      items.push({ kind: 'call', call_id: item.callId, name: item.name, arguments: item.arguments || '{}' });
    } else if (item.type === 'function_call_output') {
      items.push({ kind: 'result', call_id: item.callId, output: typeof item.output === 'string' ? item.output : JSON.stringify(item.output) });
    } else if (item.type !== 'reasoning') {
      throw new Error('studio_turn_unsupported_item');
    }
  }
  const tools = (request.tools || []).filter((tool) => (tool.kind || 'client') === 'client')
    .map((tool) => ({ name: tool.name, description: tool.description || tool.name, parameters: tool.parameters || { type: 'object' } }));
  const choice = request.toolChoice ?? 'auto';
  const format = request.responseFormat?.type === 'json'
    ? { type: 'json', name: request.responseFormat.name, schema: request.responseFormat.schema }
    : { type: 'text' };
  return {
    instructions: request.instructions || 'You help arrange a synthetic dashboard.',
    items,
    tools,
    tool_choice: typeof choice === 'string' ? choice : { name: choice.name },
    response_format: format,
  };
}

// The backend reply -> Studio output items plus the stream events Studio renders while a turn arrives.
export function toStudioResponse(reply, turnId) {
  const output = [];
  const events = [];
  (reply.output || []).forEach((item, index) => {
    if (item.type === 'text') {
      const id = `${turnId}-msg-${index}`;
      output.push({ id, kind: 'output', type: 'message', role: 'assistant', status: 'completed', content: [{ type: 'text', text: item.text, annotations: [] }] });
      events.push({ type: 'TEXT_MESSAGE_START', messageId: id, role: 'assistant' },
        { type: 'TEXT_MESSAGE_CONTENT', messageId: id, delta: item.text }, { type: 'TEXT_MESSAGE_END', messageId: id });
    } else if (item.type === 'call') {
      output.push({ id: `${turnId}-call-${index}`, kind: 'output', type: 'function_call', callId: item.call_id, name: item.name, arguments: item.arguments, status: 'completed' });
      events.push({ type: 'TOOL_CALL_START', toolCallId: item.call_id, toolCallName: item.name },
        { type: 'TOOL_CALL_ARGS', toolCallId: item.call_id, delta: item.arguments }, { type: 'TOOL_CALL_END', toolCallId: item.call_id });
    }
  });
  return { output, events };
}

// One demo session for the dashboard, created on first use: the console's session, CSRF and origin checks apply.
export function createSessionClient(fetchImpl = globalThis.fetch) {
  let session = null;
  const json = async (path, { method = 'GET', body, signal } = {}) => {
    if (!session && path !== SESSION_PATH) {
      session = await json(SESSION_PATH, { method: 'POST', body: {} });
    }
    const headers = { Accept: 'application/json' };
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (session && path !== SESSION_PATH) {
      headers['X-Demo-Session'] = session.session_id;
      if (method !== 'GET') headers['X-CSRF-Token'] = session.csrf_token;
    }
    const response = await fetchImpl(path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body), signal, credentials: 'same-origin' });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      const error = new Error(payload?.error?.message || 'The request failed.');
      error.code = payload?.error?.code || 'request_failed';
      error.status = response.status;
      throw error;
    }
    return payload;
  };
  return { json };
}

// "live" only when the backend says a model is configured; anything else (hosted demo, no backend) is "off".
export async function fetchAgentStatus(client) {
  try {
    const status = await client.json(STATUS_PATH);
    return status?.built_in_agents === 'live' ? 'live' : 'off';
  } catch {
    return 'off';
  }
}

export function createGeminiAdapter(client) {
  let turns = 0;
  return {
    executeTurn(request, options = {}) {
      turns += 1;
      const turnId = `turn-${turns}`;
      const pending = (async () => {
        try {
          const reply = await client.json(TURN_PATH, { method: 'POST', body: toWireTurn(request), signal: options.signal });
          return { ok: true, ...toStudioResponse(reply, turnId) };
        } catch (error) {
          return { ok: false, error: { code: error.code || 'studio_agent_failed', message: error.message || 'The agent turn failed.' } };
        }
      })();
      return {
        stream: (async function* stream() {
          const result = await pending;
          if (result.ok) yield* result.events;
        })(),
        complete: pending.then((result) => (result.ok
          ? { id: turnId, createdAt: Date.now(), output: result.output, status: 'completed', model: 'gemini' }
          : { id: turnId, createdAt: Date.now(), output: [], status: 'failed', error: result.error })),
      };
    },
  };
}
