// The reference corpus (about 50 kB of data) is loaded only when a reference or policy reply has to be checked, so it
// stays out of the console's first load. Until it is loaded the checks below fail closed (ref() raises a contract error).
export const REFERENCE_TYPES = Object.freeze(['official_api_reference', 'official_policy', 'public_court_order_copy']);
let loadedReference = null;
export async function loadReferenceContract() {
  if (loadedReference) return loadedReference;
  const loaded = await import('./referenceContract.js');
  loadedReference = {
    ...loaded, POLICY_CHUNKS: loaded.REFERENCE_CHUNKS, POLICY_SOURCES: loaded.REFERENCE_SOURCES,
    REFERENCE_SOURCE_IDS: new Set(Object.keys(loaded.REFERENCE_SOURCES)), REFERENCE_CHUNK_IDS: new Set(Object.keys(loaded.REFERENCE_ROWS)),
    REFERENCE_URLS: new Set(Object.values(loaded.REFERENCE_SOURCES).map((source) => source.url)),
  };
  return loadedReference;
}
const ref = () => { if (!loadedReference) contractFailure(); return loadedReference; };

// (r25 send guard) Plain sentences for the dispute send refusals, used when a reply carries the code without a message.
export const SEND_GUARD_MESSAGES = Object.freeze({
  dispute_case_bound: 'This dispute is already paired with another case, or this case with another dispute. Nothing was sent.',
  evidence_type_not_supported: 'PayPal asks for an evidence type TradeGlot cannot send yet. Respond to this dispute in PayPal directly. Nothing was sent.',
  dispute_not_this_account: 'This dispute belongs to a different PayPal account than the connected Sandbox account. Nothing was sent.',
  account_identity_unknown: 'TradeGlot cannot confirm which PayPal Sandbox account is connected, so it will not send. Nothing was sent.',
  input_characters_refused: 'The request contains characters or a number format TradeGlot does not accept. Remove them and try again.',
});

// (evloop) PayPal's own reason for a failed send, in words a seller can act on. The backend keeps only PayPal's error
// `name` and up to 3 `details[].issue` codes (each ^[A-Z0-9_]{1,64}$); every code here is one PayPal's Disputes,
// Tracking or Invoicing docs list. Any other code is shown as "PayPal said: CODE".
export const PAYPAL_ISSUE_TEXT = Object.freeze({
  INVALID_EVIDENCE_FILE: 'PayPal did not accept the evidence file. Use JPG, GIF, PNG or PDF, under 10 MB each and 50 MB per case.',
  MISSING_EVIDENCE_INFO: 'PayPal needs evidence details that were not in the request.',
  MISSING_EVIDENCE_TYPE: 'PayPal needs the evidence type for this evidence.',
  MISSING_TRACKING_INFO: 'PayPal needs a tracking number and carrier for proof of delivery.',
  MANDATORY_PARAMETER_MISSING: 'PayPal says a required field is missing.',
  ACTION_NOT_ALLOWED_IN_CURRENT_DISPUTE_STATE: 'PayPal does not allow this action in the dispute\'s current state. Check the dispute in PayPal.',
  INVALID_EVIDENCE_TYPE_PROOF_OF_FULFILLMENT: 'Proof of delivery is not a valid evidence type for this dispute\'s reason and status.',
  ITEM_ID_IS_MANDATORY_FOR_MULTIPLE_EVIDENCES: 'PayPal needs an item ID for each piece of evidence.',
  PERMISSION_DENIED: 'The connected PayPal account does not have permission for this request.',
  NOT_AUTHORIZED: 'The connected PayPal account is not allowed to make this request.',
  AUTHENTICATION_FAILURE: 'PayPal could not sign in the connected account. Connect again.',
  INPUT_VALIDATION_ERROR: 'PayPal did not accept the tracking details. Check the transaction ID and tracking number.',
  INVALID_PARAMETER_VALUE: 'PayPal did not accept the value of one field.',
  INVALID_PARAMETER_SYNTAX: 'PayPal did not accept the format of one field.',
  RESOURCE_NOT_FOUND: 'PayPal could not find this item.',
  RATE_LIMIT_REACHED: 'PayPal is limiting requests right now. Wait and try again.',
  INTERNAL_SERVER_ERROR: 'PayPal had an internal error. Try again later.',
  INVALID_REQUEST: 'PayPal did not accept the request format.',
  UNPROCESSABLE_ENTITY: 'PayPal could not process this request.',
});
const PAYPAL_CODE = /^[A-Z0-9_]{1,64}$/;
const PAYPAL_DEBUG_ID = /^[A-Za-z0-9]{6,64}$/;

// The optional paypal_issue of an error body: {name: code|null, issues: [up to 3 codes]}; anything else is dropped.
export function readPaypalIssue(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const keys = Object.keys(value).sort();
  if (keys.length !== 2 || keys[0] !== 'issues' || keys[1] !== 'name') return null;
  const { name, issues } = value;
  if (!(name === null || (typeof name === 'string' && PAYPAL_CODE.test(name)))) return null;
  if (!Array.isArray(issues) || issues.length > 3 || !issues.every((code) => typeof code === 'string' && PAYPAL_CODE.test(code))) return null;
  if (name === null && issues.length === 0) return null;
  return { name, issues: [...issues] };
}

// Plain-English lines for one paypal_issue: each issue code first (the most specific), then the name when no issue
// explains it. Unknown codes read "PayPal said: CODE".
export function paypalIssueLines(issue) {
  const checked = readPaypalIssue(issue);
  if (!checked) return [];
  const codes = checked.issues.length ? checked.issues : [checked.name];
  return [...new Set(codes)].map((code) => (Object.hasOwn(PAYPAL_ISSUE_TEXT, code) ? PAYPAL_ISSUE_TEXT[code] : `PayPal said: ${code}`));
}

export class ApiError extends Error {
  constructor(message, status, code, retryAfter = null, { paypalIssue = null, paypalDebugId = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    // (evloop) Optional, checked again here: PayPal's sanitised reason and the PayPal-Debug-Id of the failed call.
    this.paypalIssue = readPaypalIssue(paypalIssue);
    this.paypalDebugId = typeof paypalDebugId === 'string' && PAYPAL_DEBUG_ID.test(paypalDebugId) ? paypalDebugId : null;
    // (attack r23) A 429 or 503 with Retry-After: seconds to wait and the instant the wait ends, so the page can count
    // down and hold the button that hit the limit instead of letting the seller retry into it.
    this.retryAfter = retryAfter;
    this.retryAt = retryAfter ? Date.now() + retryAfter * 1000 : null;
  }
}

// (attack r23) Retry-After is delay-seconds or an HTTP date; anything else, or a wait over ten minutes, is ignored.
export function parseRetryAfter(value, now = Date.now()) {
  if (typeof value !== 'string' || !value.trim()) return null;
  const text = value.trim();
  const seconds = /^\d{1,6}$/.test(text) ? Number(text) : Math.ceil((Date.parse(text) - now) / 1000);
  return Number.isFinite(seconds) && seconds >= 1 && seconds <= 600 ? seconds : null;
}

// Whole seconds left on a failure's Retry-After (0 when there is none or it has passed).
export const retrySecondsLeft = (failure, now = Date.now()) => (failure?.retryAt ? Math.max(0, Math.ceil((failure.retryAt - now) / 1000)) : 0);
export const waitText = (seconds) => `Try again in ${seconds} second${seconds === 1 ? '' : 's'}.`;
// The server's own fixed wait sentence ("try again in 37 seconds", "try again in a few seconds") gives way to the live
// countdown, so the page never shows two different numbers (attack r23).
export const withoutFixedWait = (message) => String(message || '')
  .replace(/[\s;,.]*(?:and )?try again(?: in (?:\d+ seconds?|a few seconds|about two minutes))?\.?\s*$/i, '.').replace(/^\.$/, '');


function contractFailure() {
  throw new ApiError('API contract mismatch. Unverified content is hidden; check the backend version.', 502, 'contract_error');
}

function safeReferenceUrl(value) {
  if (typeof value !== 'string' || value.length > 2000 || /[\s\\\p{C}]/u.test(value)) return false;
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.port || url.hash) return false;
    const rawPath = value.replace(/^https:\/\/[^/]+/, '').split(/[?#]/, 1)[0];
    if (/%2e|%2f|%5c/i.test(rawPath) || rawPath.split('/').some((part) => part === '.' || part === '..')) return false;
    return ref().REFERENCE_URLS.has(value);
  } catch { return false; }
}

function referenceProvenance(row) {
  const source = ref().POLICY_SOURCES[row.source_id];
  return Boolean(source) && row.jurisdiction === 'US' && row.jurisdiction_label === source.jurisdiction
    && row.material_type === source.material_type && row.url === source.url && safeReferenceUrl(row.url);
}

export function assertReferences(payload, request) {
  const object = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
  const keys = (value, allowed) => object(value) && Object.keys(value).length === allowed.length && Object.keys(value).every((key) => allowed.includes(key));
  const text = (value, cap = 8000) => typeof value === 'string' && value.length > 0 && value.length <= cap && !/\p{C}/u.test(value);
  const digest = (value) => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
  const time = (value) => typeof value === 'string' && value.length <= 64 && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/.test(value) && Number.isFinite(Date.parse(value)) && new Date(`${value.slice(0, 10)}T00:00:00Z`).toISOString().slice(0, 10) === value.slice(0, 10);
  const microsecondTail = (value) => ((value.match(/\.(\d{1,6})(?:Z|[+-]\d{2}:\d{2})$/)?.[1] ?? '').padEnd(6, '0')).slice(3);
  const date = (value) => value === null || (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && Number.isFinite(Date.parse(`${value}T00:00:00Z`)) && new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) === value);
  const listSame = (left, right) => Array.isArray(left) && JSON.stringify(left) === JSON.stringify(right);
  const citationKeys = ['chunk_id', 'source_id', 'title', 'source_title', 'text', 'url', 'locator', 'material_type', 'jurisdiction', 'jurisdiction_label', 'case_stage', 'case_outcome', 'retrieved_at', 'text_sha256', 'relevance_score', 'source_updated_date', 'source_updated_date_status', 'effective_date', 'effective_date_status', 'decision_date', 'decision_date_status', 'decision_acceptance_deadline'];
  const envelopeKeys = ['schema_version', 'status', 'corpus_id', 'corpus_digest', 'corpus_digests', 'filters_applied', 'results', 'limitations', 'advisory_only', 'operational_authority', 'source'];
  const filterKeys = ['theme', 'jurisdiction', 'case_stage', 'material_types', 'limit', 'require_known_source_date', 'max_source_age_days', 'age_basis', 'as_of'];
  if (!keys(payload, envelopeKeys) || !object(request) || payload.schema_version !== 1 || !['references_found', 'evidence_missing'].includes(payload.status)
    || payload.source !== 'public_reference' || payload.corpus_id !== ref().REFERENCE_CORPUS_ID || payload.advisory_only !== true
    || payload.operational_authority !== 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION' || payload.corpus_digest !== ref().REFERENCE_COMBINED_DIGEST
    || !keys(payload.corpus_digests, ['sources_sha256', 'chunks_sha256']) || payload.corpus_digests.sources_sha256 !== ref().REFERENCE_SOURCE_DIGEST || payload.corpus_digests.chunks_sha256 !== ref().REFERENCE_CHUNK_DIGEST
    || !keys(payload.filters_applied, filterKeys)) contractFailure();
  const filters = payload.filters_applied;
  const types = [...(request.material_types ?? REFERENCE_TYPES)].sort();
  if (!['source_compliance', 'velocity_guard', 'dispute_mediation'].includes(filters.theme) || filters.jurisdiction !== 'US'
    || request.jurisdiction !== 'US' || !ref().REFERENCE_STAGES.includes(filters.case_stage)
    || filters.theme !== request.theme || filters.jurisdiction !== request.jurisdiction || filters.case_stage !== (request.case_stage ?? 'any')
    || !Number.isInteger(filters.limit) || filters.limit < 1 || filters.limit > 10 || filters.limit !== (request.limit ?? 3)
    || typeof filters.require_known_source_date !== 'boolean' || filters.require_known_source_date !== (request.require_known_source_date ?? false)
    || filters.max_source_age_days !== (request.max_source_age_days ?? null) || (filters.max_source_age_days !== null && (!Number.isInteger(filters.max_source_age_days) || filters.max_source_age_days < 0 || filters.max_source_age_days > 365000))
    || !types.length || new Set(types).size !== types.length || types.some((type) => !REFERENCE_TYPES.includes(type)) || !listSame(filters.material_types, types)
    || filters.age_basis !== 'source_updated_date_utc_calendar' || ((request.as_of ?? null) === null ? filters.as_of !== null : (!time(filters.as_of) || !time(request.as_of) || Date.parse(filters.as_of) !== Date.parse(request.as_of) || microsecondTail(filters.as_of) !== microsecondTail(request.as_of)))
    || (filters.max_source_age_days !== null && filters.as_of === null)
    || !Array.isArray(payload.results) || payload.results.length > filters.limit || (payload.status === 'references_found') !== (payload.results.length > 0)
    || !Array.isArray(payload.limitations) || !payload.limitations.length || payload.limitations.length > 32 || !payload.limitations.every((value) => text(value, 2000))) contractFailure();
  const ids = new Set();
  for (const row of payload.results) {
    const expected = ref().REFERENCE_ROWS[row?.chunk_id];
    if (!keys(row, citationKeys) || !text(row.chunk_id, 128) || !/^[A-Z0-9-]+$/.test(row.chunk_id) || ids.has(row.chunk_id)
      || !ref().REFERENCE_CHUNK_IDS.has(row.chunk_id) || !ref().REFERENCE_SOURCE_IDS.has(row.source_id) || !expected
      || !['title', 'source_title', 'text', 'locator'].every((key) => text(row[key])) || !text(row.jurisdiction_label, 2000)
      || !safeReferenceUrl(row.url) || !digest(row.text_sha256) || !Number.isInteger(row.relevance_score) || row.relevance_score < 1 || row.relevance_score > 128
      || row.jurisdiction !== filters.jurisdiction || !filters.material_types.includes(row.material_type) || !time(row.retrieved_at)
      || !ref().REFERENCE_STAGES.slice(1).includes(row.case_stage) || (filters.case_stage !== 'any' && row.case_stage !== filters.case_stage)
      || !['source_updated_date', 'effective_date', 'decision_date', 'decision_acceptance_deadline'].every((key) => date(row[key]))) contractFailure();
    ids.add(row.chunk_id);
    if (!referenceProvenance(row) || !Object.keys(expected).every((key) => JSON.stringify(row[key]) === JSON.stringify(expected[key]))) contractFailure();
    for (const [key, statuses] of [['source_updated_date', ['DOCUMENT_STATED', 'MISSING']], ['effective_date', ['DOCUMENT_STATED', 'NOT_VERIFIED']], ['decision_date', ['DOCUMENT_STATED', 'NOT_STATED_IN_REVIEWED_DOCUMENT', 'NOT_APPLICABLE']]]) {
      if (!statuses.includes(row[`${key}_status`]) || (row[key] !== null) !== (row[`${key}_status`] === 'DOCUMENT_STATED')) contractFailure();
    }
    if ((filters.require_known_source_date || filters.max_source_age_days !== null) && row.source_updated_date === null) contractFailure();
    if (row.material_type === 'public_court_order_copy') {
      if (row.case_stage !== 'procedural_order' || row.jurisdiction !== 'US' || !ref().REFERENCE_OUTCOMES.includes(row.case_outcome)) contractFailure();
    } else if (row.case_stage !== 'not_applicable' || row.case_outcome !== null) contractFailure();
  }
  return payload;
}


const GUIDE_PATHS = ['/guide/start', '/guide/turn', '/guide/form', '/guide/review', '/guide/state'];
const GUIDE_STATUSES = ['STRUCTURALLY_PRESENT', 'PARTIAL', 'UNCLEAR', 'CONFLICTING', 'MISSING', 'NOT_APPLICABLE'];
export const GUIDE_TEMPLATES = ['OPEN', 'CONFIRM_DATE', 'REQUEST', 'ONE', 'COMMS', 'PROGRESS', 'UNCLEAR', 'CONFLICT', 'DONE', 'PROFESSIONAL', 'REFUSE', 'OFF_TOPIC', 'OTHER_FLOW', 'OTHER_PARTY', 'SKIP', 'NO_GUARANTEE', 'NOT_ENOUGH', 'ENGLISH_ONLY', 'PII', 'NOT_SENDABLE', 'DEADLINE', 'UPLOAD', 'BUYER_ANGER', 'BUDGET', 'REQUEST_MANY', 'ECHO', 'DESCRIBE', 'SUBTRACTION', 'REVIEW'];
export const GUIDE_STAGES = ['funnel', 'echo', 'fill', 'review', 'done'];
const GUIDE_CHOOSERS = ['none', 'keyword', 'model', 'keyword_fallback', 'form'];

/** Guided gap filling: closed shape, statuses from the rule layer, fixed template ids, no model text and no stored values. */
export function assertGuideState(payload, path, body) {
  const fail = () => { throw new ApiError('API contract mismatch. Unverified content is hidden; check the backend version.', 502, 'contract_error'); };
  const keys = ['schema_version', 'started', 'scenario', 'goods_type', 'flow_name', 'items', 'gap', 'reply', 'form_result', 'form_results', 'analysis',
    'asked', 'stage', 'subtraction', 'deferred', 'prefill', 'auto_confirmed', 'review', 'rounds_used', 'turns_used', 'turns_limit', 'chooser_mode', 'model_requested', 'model_text_shown', 'values_stored', 'advisory_only'];
  const id = (v) => typeof v === 'string' && /^[a-z_]{1,40}$/.test(v);
  const short = (v, cap = 160) => typeof v === 'string' && v.length > 0 && v.length <= cap && !/[\p{C}<>]/u.test(v);
  const count = (v, cap) => Number.isInteger(v) && v >= 0 && v <= cap;
  if (!pk(payload, keys) || payload.schema_version !== 1 || typeof payload.started !== 'boolean' || payload.model_text_shown !== false
    || payload.values_stored !== false || payload.advisory_only !== true || !['keyword', 'gemini'].includes(payload.chooser_mode)
    || typeof payload.model_requested !== 'boolean' || !count(payload.turns_limit, 1000) || !count(payload.turns_used, payload.turns_limit)
    || !Array.isArray(payload.items) || payload.items.length > 12 || !pk(payload.gap, ['missing', 'partial', 'conflicting', 'present'])
    || !Array.isArray(payload.form_results) || payload.form_results.length > 3 || !Array.isArray(payload.asked) || payload.asked.length > 3
    || !Array.isArray(payload.deferred) || !po(payload.prefill) || !Array.isArray(payload.auto_confirmed) || payload.auto_confirmed.length > 12 || !Array.isArray(payload.review) || payload.review.length > 12
    || !count(payload.rounds_used, 10000)) fail();
  if (!payload.started) {
    if (path !== '/guide/state' || payload.scenario !== null || payload.items.length || payload.reply !== null || payload.form_result !== null || payload.analysis !== null
      || payload.form_results.length || payload.asked.length || payload.stage !== null || payload.subtraction !== null || payload.deferred.length
      || Object.keys(payload.prefill).length || payload.auto_confirmed.length || payload.review.length || payload.rounds_used !== 0
      || Object.values(payload.gap).some((list) => !Array.isArray(list) || list.length)) fail();
    return payload;
  }
  if (!['preflight', 'velocity', 'dispute'].includes(payload.scenario) || !short(payload.flow_name, 40)
    || (payload.scenario === 'dispute' ? !['physical', 'digital'].includes(payload.goods_type) : payload.goods_type !== null)) fail();
  if (path === '/guide/start' && (body?.scenario !== payload.scenario || (body?.goods_type ?? null) !== payload.goods_type)) fail();
  // One guide per situation: an answer for another situation's guide is never shown in this one.
  if (body?.scenario !== undefined && payload.scenario !== body.scenario) fail();
  const ids = new Set();
  for (const item of payload.items) {
    if (!pk(item, ['id', 'label', 'status', 'source', 'chunk', 'form']) || !id(item.id) || ids.has(item.id) || !short(item.label, 60)
      || !GUIDE_STATUSES.includes(item.status) || !['OFFICIAL', 'SUGGESTION'].includes(item.source)
      || (item.source === 'OFFICIAL' ? !(typeof item.chunk === 'string' && /^[A-Z0-9-]{3,64}$/.test(item.chunk)) : item.chunk !== null)
      || ((item.status === 'NOT_APPLICABLE') !== (item.form === null))) fail();
    if (item.form !== null) {
      const form = item.form;
      if (!pk(form, ['kind', 'options', 'placeholder']) || !['date', 'choice', 'text'].includes(form.kind) || !Array.isArray(form.options)
        || (form.kind === 'choice') !== (form.options.length > 0) || form.options.length > 8
        || !form.options.every((option) => pk(option, ['value', 'label']) && short(option.value, 40) && short(option.label, 80))
        || (form.kind === 'choice' ? form.placeholder !== null : !short(form.placeholder, 80))) fail();
    }
    ids.add(item.id);
  }
  const byStatus = (wanted) => payload.items.filter((item) => wanted.includes(item.status)).map((item) => item.id);
  const same = (list, expected) => Array.isArray(list) && list.length === expected.length && list.every((value, index) => value === expected[index]);
  if (!same(payload.gap.missing, byStatus(['MISSING'])) || !same(payload.gap.partial, byStatus(['PARTIAL', 'UNCLEAR']))
    || !same(payload.gap.conflicting, byStatus(['CONFLICTING'])) || !same(payload.gap.present, byStatus(['STRUCTURALLY_PRESENT']))) fail();
  const reply = payload.reply;
  if (!pk(reply, ['template', 'text', 'chooser', 'state_changed', 'dropped', 'fallback_reason']) || !GUIDE_TEMPLATES.includes(reply.template)
    || !short(reply.text, 400) || !GUIDE_CHOOSERS.includes(reply.chooser) || typeof reply.state_changed !== 'boolean'
    || !Array.isArray(reply.dropped) || reply.dropped.length > 3
    || !reply.dropped.every((row) => pk(row, ['item', 'reason']) && ids.has(row.item) && ['other_party', 'inferred'].includes(row.reason))
    || (reply.chooser === 'keyword_fallback' ? !['budget', 'provider_error', 'invalid_reply', 'late', 'no_items'].includes(reply.fallback_reason) : reply.fallback_reason !== null)
    || (reply.chooser === 'model' && payload.chooser_mode !== 'gemini')) fail();
  // A turn may carry the first round's fixed inputs in the same Save; then its results match what was sent.
  const sentWithTurn = path === '/guide/turn' && Array.isArray(body?.fields) ? body.fields.map((field) => field.item) : [];
  if (path === '/guide/turn' && (reply.chooser === 'form' || payload.form_results.length > sentWithTurn.length
    || !payload.form_results.every((row) => sentWithTurn.includes(row.item)) || (payload.form_result !== null) !== (payload.form_results.length > 0))) fail();
  // Rounds: subtraction is rule arithmetic; asked holds up to three open ids; echo values are closed field values.
  const open = new Set([...payload.gap.missing, ...payload.gap.partial, ...payload.gap.conflicting]);
  const sub = payload.subtraction;
  const itemCount = payload.items.filter((item) => item.status !== 'NOT_APPLICABLE').length;
  if (!GUIDE_STAGES.includes(payload.stage) || !pk(sub, ['needed', 'taken', 'left', 'text']) || sub.needed !== itemCount
    || sub.taken !== payload.gap.present.length || sub.left !== sub.needed - sub.taken
    || sub.text !== `${sub.needed} items needed · ${sub.taken} taken from what you wrote · ${sub.left} left`
    // done needs every item present; review is the one summary: nothing asked, only values from the seller's words open
    || (payload.stage === 'done' && open.size !== 0) || (open.size === 0 && !['done', 'review'].includes(payload.stage))
    || (['done', 'review'].includes(payload.stage)) !== (payload.asked.length === 0)
    // The summary of items taken from the seller's words: its own round only when nothing is left to fill,
    // otherwise on the same screen as the last round (the asked items are every open item).
    || (payload.stage === 'review' && (!payload.review.length || open.size !== 0))
    || (payload.review.length && payload.stage !== 'review' && !(open.size > 0 && [...open].every((item) => payload.asked.includes(item))))
    || !payload.review.every((row) => pk(row, ['item', 'source', 'value']) && ids.has(row.item) && row.source === 'words'
      && short(row.value, 40) && payload.gap.present.includes(row.item))
    || new Set(payload.asked).size !== payload.asked.length || !payload.asked.every((item) => open.has(item))
    || !payload.deferred.every((item) => open.has(item))
    // Settled by the rule layer from the last typed sentence: present items, only on a typed turn, never twice.
    || !payload.auto_confirmed.every((item) => payload.gap.present.includes(item)) || new Set(payload.auto_confirmed).size !== payload.auto_confirmed.length
    || (path !== '/guide/turn' && path !== '/guide/state' && payload.auto_confirmed.length)
    || !Object.entries(payload.prefill).every(([item, value]) => {
      const row = payload.items.find((entry) => entry.id === item);
      if (!row || !open.has(item) || row.form === null || typeof value !== 'string') return false;
      return row.form.kind === 'choice' ? row.form.options.some((option) => option.value === value) : row.form.kind === 'date' && /^\d{4}-\d{2}-\d{2}$/.test(value);
    })
    // Echo: the confirmations come first; spare slots may carry the next open items.
    || (payload.stage === 'echo' && (!payload.asked.length || !(payload.asked[0] in payload.prefill)
      || payload.asked.some((item, index) => index > 0 && item in payload.prefill && !(payload.asked[index - 1] in payload.prefill))))
    || (payload.stage === 'fill' && !payload.asked.every((item) => payload.deferred.includes(item)))) fail();
  const analysis = payload.analysis;
  if (analysis !== null) {
    // One governed model step per turn: analysing, then replaced (model reply) or kept (keyword answer and a reason).
    if (!pk(analysis, ['turn', 'status', 'reason']) || !Number.isInteger(analysis.turn) || analysis.turn < 1 || analysis.turn > 10000
      || !['analysing', 'replaced', 'kept'].includes(analysis.status) || payload.chooser_mode !== 'gemini'
      || (analysis.status === 'kept' ? !['budget', 'provider_error', 'invalid_reply', 'late', 'no_items', 'superseded'].includes(analysis.reason) : analysis.reason !== null)
      || (path === '/guide/turn' && analysis.status !== 'analysing')
      || !({ analysing: ['keyword'], replaced: ['model', 'form'], kept: ['keyword_fallback', 'form'] }[analysis.status] || []).includes(reply.chooser)) fail();
  }
  if (path === '/guide/review' && (reply.chooser !== 'form' || payload.form_results.length || payload.form_result !== null)) fail();
  if (path === '/guide/form') {
    const sent = Array.isArray(body?.fields) ? body.fields.map((field) => field.item) : [body?.item];
    if (!pk(payload.form_result, ['item', 'valid']) || payload.form_result.item !== sent[sent.length - 1] || typeof payload.form_result.valid !== 'boolean'
      || reply.chooser !== 'form' || payload.form_results.length !== sent.length
      || !payload.form_results.every((row, index) => pk(row, ['item', 'valid', 'deferred']) && row.item === sent[index]
        && typeof row.valid === 'boolean' && typeof row.deferred === 'boolean' && !(row.valid && row.deferred)
        && (!row.valid || payload.gap.present.includes(row.item)))) fail();
  } else if (payload.form_result !== null && !((path === '/guide/state' || sentWithTurn.length) && pk(payload.form_result, ['item', 'valid'])
    && ids.has(payload.form_result.item))) fail();
  return payload;
}

// The six claim types src/payguard/advisory_eval.py CLAIM_TYPES accepts; the backend has no source rule for historical
// cases or guidance claims, so offering them only ever produced a 422 (click-all 2026-11-03 #1).
export const POLICY_CLAIM_TYPES = ['policy_reference', 'current_policy', 'procedural_reference', 'api_reference', 'financial_action', 'assurance'];
const POLICY_THEMES = ['source_compliance', 'velocity_guard', 'dispute_mediation'];
const POLICY_REASONS = ['SUMMARY_COVERAGE_INCOMPLETE','CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED','FUTURE_OBSERVATION','STALE_OBSERVATION','DOCUMENT_UPDATE_DATE_MISSING','DOCUMENT_UPDATE_IN_FUTURE','UNKNOWN_EFFECTIVE_DATE','EFFECTIVE_DATE_IN_FUTURE','API_REFERENCE_NOT_POLICY','GUIDANCE_NOT_APPLICABLE_POLICY','HISTORICAL_CASE_NOT_APPLICABLE_POLICY','PROCEDURE_NOT_APPLICABLE_POLICY','NO_OFFICIAL_POLICY_COVERAGE','NO_REFERENCE_COVERAGE'];
const CLAIM_REASONS = ['ACTION_CLAIM_FORBIDDEN','ASSURANCE_CLAIM_FORBIDDEN','CITATION_UNKNOWN','CITATION_REGION_MISMATCH','CITATION_THEME_MISMATCH','CLAIM_REFERENCE_TYPE_MISMATCH','FUTURE_OBSERVATION','STALE_OBSERVATION','DOCUMENT_UPDATE_IN_FUTURE','CURRENT_POLICY_NOT_ESTABLISHED'];
const POLICY_AUTHORITY = 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION';
const po = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const pk = (v, fields) => po(v) && Object.keys(v).length === fields.length && Object.keys(v).every((k) => fields.includes(k));
const canonical = v => Array.isArray(v) ? v.map(canonical) : po(v) ? Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])) : v;
const pe = (a,b) => JSON.stringify(canonical(a)) === JSON.stringify(canonical(b));
const pt = (v) => typeof v === 'string' && v.length > 0 && v.length <= 2000 && !/\p{C}/u.test(v);
const pl = (v, allowed, cap, minimum = 0) => Array.isArray(v) && v.length >= minimum && v.length <= cap && v.every((x) => allowed.includes(x)) && pe(v,[...new Set(v)].sort());
export function policyInstant(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/.test(value) || !Number.isFinite(Date.parse(value))) return null;
  const day = new Date(`${value.slice(0,10)}T00:00:00Z`);
  if (!Number.isFinite(day.getTime()) || day.toISOString().slice(0,10) !== value.slice(0,10) || +value.slice(11,13)>23 || +value.slice(14,16)>59 || +value.slice(17,19)>59) return null;
  return `${Date.parse(value)}|${((value.match(/\.(\d{1,6})(?:Z|[+-]\d{2}:\d{2})$/)?.[1] ?? '').padEnd(6,'0')).slice(3)}`;
}
function policyContext(actual, request) {
  return pk(actual,['jurisdiction','theme','as_of','observation_max_age_days']) && actual.jurisdiction === 'US' && request?.jurisdiction === 'US' && POLICY_THEMES.includes(actual.theme) && actual.theme === request?.theme && Number.isInteger(actual.observation_max_age_days) && actual.observation_max_age_days >= 0 && actual.observation_max_age_days <= 365000 && actual.observation_max_age_days === request.observation_max_age_days && policyInstant(actual.as_of) !== null && policyInstant(actual.as_of) === policyInstant(request.as_of);
}
function policyCommon(p, request, context) {
  return policyContext(context,request) && p.schema_version === 1 && p.corpus_id === ref().REFERENCE_CORPUS_ID && p.corpus_digest === ref().REFERENCE_COMBINED_DIGEST && pk(p.corpus_digests,['sources_sha256','chunks_sha256']) && p.corpus_digests.sources_sha256 === ref().REFERENCE_SOURCE_DIGEST && p.corpus_digests.chunks_sha256 === ref().REFERENCE_CHUNK_DIGEST && p.advisory_only === true && p.operational_authority === POLICY_AUTHORITY && p.requires_human_review === true && p.current_policy_applicability === 'NOT_ESTABLISHED' && Array.isArray(p.limitations) && p.limitations.length > 0 && p.limitations.length <= 32 && p.limitations.every(pt) && pk(p.coverage,['complete','basis','regional_source_count','selected_source_count','selected_chunk_count','official_policy_source_ids','official_policy_chunk_count_by_theme','missing_official_policy_themes']) && pe(p.coverage,ref().POLICY_COVERAGE[`${context.jurisdiction}|${context.theme}`]);
}
export function assertPolicyAssessment(p, request) {
  const fields=['schema_version','version','source','corpus_id','corpus_digest','corpus_digests','filters_applied','status','current_policy_applicability','advisory_only','operational_authority','requires_human_review','coverage','sources','chunks','reason_codes','limitations'];
  if (!pk(p,fields) || !policyCommon(p,request,p.filters_applied) || p.version !== 'payguard.applicability.v1' || p.source !== 'public_reference' || p.status !== 'INCOMPLETE_POLICY_EVIDENCE' || !pl(p.reason_codes,POLICY_REASONS,15,1) || !Array.isArray(p.sources) || p.sources.length !== p.coverage.selected_source_count || !Array.isArray(p.chunks) || p.chunks.length !== p.coverage.selected_chunk_count) contractFailure();
  const expectedChunks=Object.values(ref().POLICY_CHUNKS).filter(c=>c.jurisdiction===request.jurisdiction && c.theme===request.theme).sort((a,b)=>a.chunk_id.localeCompare(b.chunk_id));
  if (!pe(p.chunks,expectedChunks)) contractFailure();
  const ids=[...new Set(expectedChunks.map(c=>c.source_id))].sort();
  if (!pe(p.sources.map(s=>s?.source_id),ids)) contractFailure();
  for (const s of p.sources) {
    const fixed=ref().POLICY_SOURCES[s.source_id];
    const extra=['jurisdiction_normalized','observation_status','observation_age_basis','current_policy_applicability','reason_codes','citation_chunk_ids'];
    if (!fixed || !pk(s,[...Object.keys(fixed),...extra]) || !Object.keys(fixed).every(k=>pe(s[k],fixed[k])) || !safeReferenceUrl(s.url) || s.jurisdiction_normalized!==request.jurisdiction || !['FUTURE_OBSERVATION','STALE_OBSERVATION','WITHIN_OBSERVATION_BUDGET'].includes(s.observation_status) || s.observation_age_basis!=='saved_retrieved_at_exact_elapsed_time' || s.current_policy_applicability!=='NOT_ESTABLISHED' || !pl(s.reason_codes,POLICY_REASONS,15,1) || !pe(s.citation_chunk_ids,expectedChunks.filter(c=>c.source_id===s.source_id).map(c=>c.chunk_id))) contractFailure();
  }
  return p;
}
export function assertAdvisoryEvaluation(p, request) {
  const fields=['schema_version','version','source','status','requested_context','corpus_id','corpus_digest','corpus_digests','advisory_only','operational_authority','requires_human_review','semantic_entailment','PII_quality','prompt_injection_quality','natural_language_action_assurance_quality','model_generation','claim_count','claim_gates','current_policy_applicability','coverage','limitations'];
  let candidate;
  try { candidate=JSON.parse(request.candidate_json); } catch { contractFailure(); }
  const statuses=['STRUCTURE_COMPATIBLE','INCOMPLETE_EVIDENCE','REJECTED'];
  if (!pk(p,fields) || !policyCommon(p,request,p.requested_context) || p.version!=='payguard.advisory_eval.v1' || p.source!=='offline_structured_gate' || !statuses.includes(p.status) || !['semantic_entailment','PII_quality','prompt_injection_quality','natural_language_action_assurance_quality'].every(k=>p[k]==='NOT_EVALUATED') || p.model_generation!=='NOT_RUN' || !Array.isArray(candidate?.claims) || !Number.isInteger(p.claim_count) || p.claim_count<1 || p.claim_count>20 || p.claim_count!==candidate.claims.length || !Array.isArray(p.claim_gates) || p.claim_gates.length!==p.claim_count) contractFailure();
  for (const [i,g] of p.claim_gates.entries()) {
    const c=candidate.claims[i];
    const trusted=Array.isArray(c?.citation_chunk_ids) ? [...new Set(c.citation_chunk_ids.filter(id=>Object.hasOwn(ref().POLICY_CHUNKS,id)))].sort() : null;
    if (!pk(g,['claim_index','claim_type','status','trusted_citation_chunk_ids','reason_codes']) || g.claim_index!==i || !POLICY_CLAIM_TYPES.includes(g.claim_type) || g.claim_type!==c?.claim_type || !statuses.includes(g.status) || !pe(g.trusted_citation_chunk_ids,trusted) || !pl(g.reason_codes,CLAIM_REASONS,10) || (g.status==='STRUCTURE_COMPATIBLE' && g.reason_codes.length!==0) || (g.status!=='STRUCTURE_COMPATIBLE' && !g.reason_codes.length)) contractFailure();
  }
  const overall=p.claim_gates.some(g=>g.status==='REJECTED')?'REJECTED':p.claim_gates.some(g=>g.status==='INCOMPLETE_EVIDENCE')?'INCOMPLETE_EVIDENCE':'STRUCTURE_COMPATIBLE';
  if(p.status!==overall) contractFailure();
  return p;
}

export const PAYPAL_WRITE_PATHS = ['/paypal/invoices/draft', '/paypal/disputes/provide-evidence', '/paypal/disputes/add-tracking'];
export const PAYPAL_WRITE_TIMEOUT_MESSAGE = 'No answer within 45 seconds. It may still have reached PayPal Sandbox: check the dispute or the Sandbox invoices before you try again.';

export function assertSandboxReceipt(receipt, action, invoiceId = null) {
  // (rehearsal 2026-11-04) The backend receipt has carried paypal_debug_id since 653111a: always present, null or the
  // call's PayPal-Debug-Id (schemas.SandboxEvidenceReceipt, no default). Missing it here made every real Sandbox
  // connect and draft fail as a contract mismatch; tests/frontend_receipt_parity.mjs now feeds the backend's own
  // receipts through this check.
  const fields = ['schema_version','paypal_debug_id','environment','action','status','observed_at','invoice_id','evidence_class','proof_kind','separate_get_readback','external_send'];
  const debugId = receipt?.paypal_debug_id;
  if (debugId !== null && !(typeof debugId === 'string' && /^[A-Za-z0-9]{6,64}$/.test(debugId))) contractFailure();
  const time = receipt?.observed_at;
  const utc = typeof time === 'string' && time.length >= 20 && time.length <= 27
    && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(time)
    && Number.isFinite(Date.parse(time)) && +time.slice(11,13) <= 23 && +time.slice(14,16) <= 59 && +time.slice(17,19) <= 59
    && new Date(`${time.slice(0,10)}T00:00:00Z`).toISOString().slice(0,10) === time.slice(0,10);
  const draft = action === 'CREATE_INVOICE_DRAFT';
  if (!pk(receipt, fields) || receipt.schema_version !== 1 || receipt.environment !== 'sandbox'
      || !['OAUTH_CONNECT','CREATE_INVOICE_DRAFT'].includes(action) || receipt.action !== action
      || receipt.status !== (draft ? 'DRAFT' : 'CONNECTED') || !utc
      || !['AUTHENTIC_SANDBOX_RESPONSE','SYNTHETIC_TEST_RESPONSE'].includes(receipt.evidence_class)
      || receipt.proof_kind !== 'POST_RESPONSE_ONLY' || receipt.separate_get_readback !== false || receipt.external_send !== 'FROZEN'
      || receipt.invoice_id !== invoiceId || (draft && (typeof invoiceId !== 'string' || !/^INV2-[A-Z0-9-]{8,64}$/.test(invoiceId)))
      || (!draft && invoiceId !== null)) contractFailure();
  return receipt;
}

const AI_CITATIONS = {
  source_compliance: new Set(['PP-US-AUP-POLICY']),
  velocity_guard: new Set(['PP-US-UA-VELOCITY']),
  dispute_mediation: new Set(['PP-REASONS-INR', 'PP-EVIDENCE-TRACKING']),
};
const AI_PROMPT_CONTRACT_ID = 'payguard-bounded-advisory-v3';
const AI_PROMPT_CONTRACT_DIGEST = '98cd0bc33670027ff728ea571bc05debd5e1aa756d493521b2ea810f1bc8e5c0';
// Local runs answer from this session's closed facts; the fixed fixture remains for tests and replays.
// Each variant carries its own first limitation, so a session brief cannot be shown with the fixed wording or back.
const AI_FIRST_LIMITATION = {
  'payguard-session-brief-v1': 'Built from closed values the server computed for this demo session; the demo data is synthetic and this brief does not describe a real merchant.',
  'payguard-fixed-synthetic-brief-v1': 'Fixed synthetic fixture only; this brief does not describe the current session or a real merchant.',
};
const AI_MODEL_EVIDENCE = {
  'gemini-3.8-flash': new Set(['SYNTHETIC_TEST_RESPONSE', 'OPERATOR_LIVE_RESPONSE']),
  'nvidia-nemotron-3-nano-4b': new Set(['LOCAL_RUNTIME_RESPONSE']),
};

export function assertAiBrief(payload, request) {
  const envelope = ['schema_version','status','stage','fixture_id','context_digest','corpus_digest','model','prompt_contract_id','prompt_contract_digest','execution_evidence','brief','ai_generated','advisory_only','human_review_required','compliance_decision','current_policy_applicability','external_action_authorized','workflow_transition_authorized','semantic_entailment','limitations'];
  const briefFields = ['summary','evidence_points','missing_evidence','citation_ids'];
  const digest = (value) => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
  const boundedText = (value, limit) => typeof value === 'string' && value.trim().length > 0
    && [...value].length <= limit && !/\p{C}/u.test(value);
  const requestKeys = request && Object.hasOwn(request, 'case_ref') ? ['stage', 'case_ref'] : ['stage'];
  if (!pk(payload, envelope) || !pk(request, requestKeys) || !Object.hasOwn(AI_CITATIONS, request.stage)
      || (Object.hasOwn(request, 'case_ref') && (request.stage !== 'dispute_mediation' || typeof request.case_ref !== 'string' || !/^case-ref-[0-9]{3}$/.test(request.case_ref)))
      || payload.schema_version !== '1.0' || payload.status !== 'completed' || payload.stage !== request.stage
      || !Object.hasOwn(AI_FIRST_LIMITATION, payload.fixture_id) || !digest(payload.context_digest) || !digest(payload.corpus_digest)
      || !Object.hasOwn(AI_MODEL_EVIDENCE, payload.model)
      || payload.prompt_contract_id !== AI_PROMPT_CONTRACT_ID || payload.prompt_contract_digest !== AI_PROMPT_CONTRACT_DIGEST
      || !AI_MODEL_EVIDENCE[payload.model].has(payload.execution_evidence)
      || payload.ai_generated !== true || payload.advisory_only !== true || payload.human_review_required !== true
      || payload.compliance_decision !== 'NOT_MADE' || payload.current_policy_applicability !== 'NOT_ESTABLISHED'
      || payload.external_action_authorized !== false || payload.workflow_transition_authorized !== false
      || payload.semantic_entailment !== 'NOT_EVALUATED' || !pk(payload.brief, briefFields)) contractFailure();
  const brief = payload.brief;
  if (!boundedText(brief.summary, 1200)
      || !Array.isArray(brief.evidence_points) || brief.evidence_points.length < 1 || brief.evidence_points.length > 5
      || !brief.evidence_points.every((value) => boundedText(value, 300))
      || !Array.isArray(brief.missing_evidence) || brief.missing_evidence.length < 1 || brief.missing_evidence.length > 5
      || !brief.missing_evidence.every((value) => boundedText(value, 300))
      || !Array.isArray(brief.citation_ids) || brief.citation_ids.length < 1 || brief.citation_ids.length > 3
      || new Set(brief.citation_ids).size !== brief.citation_ids.length
      || !brief.citation_ids.every((value) => typeof value === 'string' && /^[A-Z0-9-]{1,128}$/.test(value) && AI_CITATIONS[request.stage].has(value))
      || !Array.isArray(payload.limitations) || payload.limitations.length !== 3
      || !payload.limitations.every((value) => boundedText(value, 1200))
      || payload.limitations[0] !== AI_FIRST_LIMITATION[payload.fixture_id]) contractFailure();
  return payload;
}

function assertContract(path, payload, session, body) {
  if (path === '/policy/assess') return assertPolicyAssessment(payload, body);
  if (path === '/advisory/evaluate') return assertAdvisoryEvaluation(payload, body);
  if (path === '/ai/evidence-brief') return assertAiBrief(payload, body);
  if (GUIDE_PATHS.includes(path)) return assertGuideState(payload, path, body);
  const object = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
  const text = (value) => typeof value === 'string' && value.length > 0;
  const digest = (value) => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
  let valid = object(payload);
  if (path === '/references/search') {
    return assertReferences(payload, body);
  } else if (path === '/demo/sessions') {
    valid = valid && text(payload.session_id) && text(payload.csrf_token) && text(payload.expires_at) && payload.source === 'synthetic';
  } else if (path === '/demo/state' || path === '/demo/inject') {
    valid = valid && payload.source === 'synthetic' && payload.session_id === session?.session_id
      && text(payload.policy_version) && text(payload.expires_at)
      && Array.isArray(payload.transactions) && payload.transactions.length <= 200
      && payload.transactions.every((row) => object(row) && ['order_id', 'amount', 'currency', 'occurred_at'].every((key) => text(row[key])))
      && Array.isArray(payload.disputes) && payload.disputes.length <= 5
      && payload.disputes.every((row) => object(row) && pk(row,['case_ref','order_ref','reason','opened_at','seller_response_due_date','dispute_amount','status'])
        && ['case_ref', 'order_ref', 'reason', 'opened_at', 'seller_response_due_date', 'status'].every((key) => text(row[key]))
        && Number.isFinite(Date.parse(row.seller_response_due_date))
        // Synthetic amount in the PayPal Disputes dispute_amount shape.
        && pk(row.dispute_amount, ['currency_code', 'value']) && typeof row.dispute_amount.currency_code === 'string'
        && /^[A-Z]{3}$/.test(row.dispute_amount.currency_code) && typeof row.dispute_amount.value === 'string'
        && /^[0-9]{1,10}(\.[0-9]{1,2})?$/.test(row.dispute_amount.value))
      && Array.isArray(payload.activity) && payload.activity.length <= 30
      && payload.activity.every((row) => object(row) && ['id', 'at', 'label', 'source'].every((key) => text(row[key])) && row.source === 'synthetic')
      && object(payload.velocity) && ['normal','review_velocity','insufficient_baseline'].includes(payload.velocity.status)
      && payload.velocity.baseline_provenance === 'SYNTHETIC_BASELINE'
      && text(payload.velocity.baseline_amount_per_hour)
      && text(payload.velocity.baseline_window_start) && text(payload.velocity.baseline_window_end)
      && Number.isFinite(Date.parse(payload.velocity.baseline_window_start))
      && Number.isFinite(Date.parse(payload.velocity.baseline_window_end))
      && Date.parse(payload.velocity.baseline_window_start) < Date.parse(payload.velocity.baseline_window_end)
      && Date.parse(payload.velocity.baseline_window_end) <= Date.parse(payload.velocity.window_start)
      && object(payload.scenario);
  } else if (path === '/aup/review') {
    const categories = ['unsupported_financial_promise','weapons','controlled_substances','counterfeit_goods','regulated_activity'];
    valid = valid && pk(payload,['match_status','compliance_decision','current_policy_applicability','evaluation_id','description_digest','evaluated_at','expires_at','warning_copy_version','policy_url','findings','recommendation','policy_version','advisory_only','source'])
      && ['NO_MATCH','REVIEW_SIGNAL'].includes(payload.match_status) && payload.compliance_decision === 'NOT_MADE'
      && payload.current_policy_applicability === 'NOT_ESTABLISHED'
      && typeof payload.evaluation_id === 'string' && /^[A-Za-z0-9_-]{32,128}$/.test(payload.evaluation_id)
      && digest(payload.description_digest) && Number.isFinite(Date.parse(payload.evaluated_at)) && Number.isFinite(Date.parse(payload.expires_at))
      && Date.parse(payload.expires_at) > Date.parse(payload.evaluated_at)
      && Date.parse(payload.expires_at) <= Date.parse(payload.evaluated_at) + 120000
      && Date.parse(payload.expires_at) <= Date.parse(session?.expires_at)
      && payload.warning_copy_version === 'aup-warning-v1' && payload.policy_url === 'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full'
      && Array.isArray(payload.findings) && payload.findings.length <= 5
      && payload.findings.every((finding) => pk(finding,['category','code']) && categories.includes(finding.category) && finding.code === 'keyword_requires_policy_review')
      && new Set(payload.findings.map(f=>f.category)).size === payload.findings.length
      && (payload.match_status === 'REVIEW_SIGNAL') === (payload.findings.length > 0)
      && text(payload.recommendation) && payload.recommendation.length <= 1000 && text(payload.policy_version)
      && payload.advisory_only === true && payload.source === 'synthetic';
  } else if (path === '/aup/category-signal') {
    // Optional Channel3 signal: a closed shape that never carries or changes the AUP decision.
    const statusOk = ['OFF','SIGNAL','NOT_SENT','UNAVAILABLE'].includes(payload.status);
    const reasonOk = payload.reason === null || ['nothing_to_send','budget_exhausted','timeout','upstream_error','contract_rejected'].includes(payload.reason);
    const signal = payload.signal;
    const signalOk = signal === null || (pk(signal,['category','confidence','source']) && signal.source === 'channel3'
      && ((signal.category === null && signal.confidence === null)
        || (typeof signal.category === 'string' && /^[A-Za-z0-9][A-Za-z0-9 &'\-,./+()]{0,79}$/.test(signal.category) && ['HIGH','LOW'].includes(signal.confidence))));
    valid = valid && pk(payload,['status','signal','reason','affects_decision']) && statusOk && reasonOk && signalOk
      && payload.affects_decision === false
      && (payload.status === 'SIGNAL') === (signal !== null)
      && ['NOT_SENT','UNAVAILABLE'].includes(payload.status) === (payload.reason !== null);
  } else if (path === '/aup/product-reference' || path === '/aup/product-reference/confirm') {
    // Channel3 reference cards: closed shape, no prices, offers or buy links; never changes the AUP decision.
    const cardText = (v, max) => typeof v === 'string' && v.length >= 2 && v.length <= max && /^[A-Za-z0-9 &'\-,./+()%"]+$/.test(v);
    const card = (c) => pk(c,['product_id','title','brand','category','key_features','materials','image_url'])
      && typeof c.product_id === 'string' && /^[A-Za-z0-9_.:-]{1,64}$/.test(c.product_id) && cardText(c.title, 120)
      && (c.brand === null || cardText(c.brand, 60)) && (c.category === null || cardText(c.category, 80))
      && Array.isArray(c.key_features) && c.key_features.length <= 4 && c.key_features.every((f) => cardText(f, 100))
      && Array.isArray(c.materials) && c.materials.length <= 4 && c.materials.every((m) => cardText(m, 40))
      && (c.image_url === null || (typeof c.image_url === 'string' && c.image_url.length <= 500 && /^https:\/\/[^\s@]+$/.test(c.image_url)));
    const sources = ['channel3_live','channel3_recorded'];
    const stamp = (v) => v === null || (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(v));
    if (path === '/aup/product-reference') {
      const cards = payload.cards;
      valid = valid && pk(payload,['status','source','cards','reason','recorded_at','affects_decision'])
        && ['OFF','FOUND','NOT_FOUND','NOT_SENT','UNAVAILABLE'].includes(payload.status)
        && Array.isArray(cards) && cards.length <= 3 && cards.every(card)
        && new Set(cards.map((c) => c.product_id)).size === cards.length
        && (payload.status === 'FOUND') === (cards.length > 0)
        && (['FOUND','NOT_FOUND'].includes(payload.status) ? sources.includes(payload.source) : payload.source === null)
        && (payload.reason === null || ['nothing_to_send','not_recorded','budget_exhausted','timeout','upstream_error','contract_rejected'].includes(payload.reason))
        && ['NOT_SENT','UNAVAILABLE'].includes(payload.status) === (payload.reason !== null)
        && stamp(payload.recorded_at) && (payload.source === 'channel3_recorded') === (payload.recorded_at !== null)
        && payload.affects_decision === false;
    } else {
      valid = valid && pk(payload,['choice','evaluation_id','description_digest','source','recorded_at','card','card_digest','confirmed_by','affects_decision'])
        && ['CONFIRMED','NONE_MATCH'].includes(payload.choice) && payload.evaluation_id === body?.evaluation_id
        && typeof payload.description_digest === 'string' && /^[a-f0-9]{64}$/.test(payload.description_digest)
        && sources.includes(payload.source) && stamp(payload.recorded_at)
        && (payload.choice === 'CONFIRMED' ? card(payload.card) && payload.card.product_id === body?.product_id
          && typeof payload.card_digest === 'string' && /^[a-f0-9]{64}$/.test(payload.card_digest)
          : payload.card === null && payload.card_digest === null && body?.product_id === null)
        && payload.confirmed_by === 'seller' && payload.affects_decision === false;
    }
  } else if (path === '/cases/route') {
    // Fuzzy case routing: closed shape; code decides the goods group, never a dispute outcome.
    const routeText = (v, max) => typeof v === 'string' && v.length >= 2 && v.length <= max && /^[A-Za-z0-9 &'\-,./+()%"]+$/.test(v);
    const match = (m) => pk(m,['product_id','title','category','score','exact_words','match_type']) && typeof m.product_id === 'string' && /^[A-Za-z0-9_.:-]{1,64}$/.test(m.product_id)
      && routeText(m.title, 120) && (m.category === null || routeText(m.category, 80)) && typeof m.score === 'number' && m.score >= 0 && m.score <= 1
      && Array.isArray(m.exact_words) && m.exact_words.length <= 8 && m.exact_words.every((w) => typeof w === 'string' && /^[a-z0-9]{1,40}$/.test(w))
      && ['exact','close'].includes(m.match_type);
    valid = valid && pk(payload,['query','route','reason','matched_word','matches','filtered_out','items','decided_by','affects_decision'])
      && Number.isInteger(payload.filtered_out) && payload.filtered_out >= 0 && payload.filtered_out <= 1000
      && (payload.query === null || (typeof payload.query === 'string' && payload.query.length <= 120))
      && ['physical','digital','service','unknown'].includes(payload.route)
      && ['catalogue_match','live_catalogue_match','digital_word','service_word','filtered_conflict','no_close_match','nothing_to_match'].includes(payload.reason)
      && (payload.matched_word === null || (typeof payload.matched_word === 'string' && payload.matched_word.length <= 40))
      && Array.isArray(payload.matches) && payload.matches.length <= 3 && payload.matches.every(match)
      && Array.isArray(payload.items) && payload.items.length <= 12 && payload.items.every((item) => typeof item === 'string' && item.length > 0 && item.length <= 60)
      && (payload.route === 'physical') === (payload.matches.length > 0)
      && ['digital','service'].includes(payload.route) === (payload.matched_word !== null)
      && ['physical','digital'].includes(payload.route) === (payload.items.length > 0)
      && payload.decided_by === 'code' && payload.affects_decision === false;
  } else if (path === '/aup/acknowledge') {
    valid = valid && pk(payload,['source','evaluation_id','description_digest','choice','acknowledgement_token','expires_at','warning_copy_version','compliance_decision','external_action_authorized'])
      && payload.source === 'synthetic' && payload.evaluation_id === body?.evaluation_id
      && payload.description_digest === body?.description_digest && payload.choice === body?.choice
      && ['RETURN_TO_EDIT','CANCEL','ACKNOWLEDGE_AND_CONTINUE'].includes(payload.choice)
      && payload.warning_copy_version === 'aup-warning-v1' && payload.compliance_decision === 'NOT_MADE' && payload.external_action_authorized === false;
    if (valid && payload.choice === 'ACKNOWLEDGE_AND_CONTINUE') {
      valid = typeof payload.acknowledgement_token === 'string' && /^[A-Za-z0-9_-]{32,128}$/.test(payload.acknowledgement_token)
        && Number.isFinite(Date.parse(payload.expires_at)) && Date.parse(payload.expires_at) <= Date.parse(session?.expires_at);
    } else if (valid) valid = payload.acknowledgement_token === null && payload.expires_at === null;
  } else if (path === '/connections') {
    // Deployment mode only: the console never learns whether a key is present.
    // sandbox_reads: true appears only on the hosted demo with read-only Sandbox reads switched on (never a key or a name).
    valid = valid && (pk(payload, ['mode']) ? ['local', 'hosted_demo'].includes(payload.mode)
      : pk(payload, ['mode', 'sandbox_reads']) && payload.mode === 'hosted_demo' && payload.sandbox_reads === true);
  } else if (path === '/paypal/status' || path === '/paypal/connect') {
    valid = valid && pk(payload,['configured','status','environment','last_verified_at','source','evidence_receipt'])
      && payload.source === 'paypal_sandbox' && payload.environment === 'sandbox' && typeof payload.configured === 'boolean'
      && ['not_configured', 'disconnected', 'connected', 'error'].includes(payload.status);
    if (valid && payload.status === 'connected') {
      assertSandboxReceipt(payload.evidence_receipt,'OAUTH_CONNECT');
      valid = payload.configured && payload.last_verified_at === payload.evidence_receipt.observed_at;
    } else if (valid) valid = payload.evidence_receipt === null;
  } else if (path === '/paypal/disputes' || /^\/paypal\/disputes\/PP-[A-Z0-9][A-Z0-9-]{2,62}$/.test(path) || path === '/paypal/disputes/provide-evidence' || path === '/paypal/disputes/add-tracking') {
    const disputeId = (value) => typeof value === 'string' && /^PP-[A-Z0-9][A-Z0-9-]{2,62}$/.test(value);
    const money = (value) => object(value) && pk(value, ['currency_code', 'value']) && /^[A-Z]{3}$/.test(value.currency_code) && /^[0-9]{1,10}(\.[0-9]{1,2})?$/.test(value.value);
    // (optimise r24) Optional fields the backend now returns: paypal_debug_id on every dispute envelope (null, or the
    // Sandbox call's PayPal-Debug-Id; always null for the fixture) and payload_sha256 on the provide-evidence and
    // add-tracking previews.
    // Each is read only when present and must match its pattern; every other key stays exact.
    const has = (key) => Object.prototype.hasOwnProperty.call(payload, key);
    const optional = (...keys) => keys.filter(has);
    const debugIdValid = !has('paypal_debug_id') || payload.paypal_debug_id === null
      || (payload.source === 'paypal_sandbox' && typeof payload.paypal_debug_id === 'string' && /^[A-Za-z0-9]{6,64}$/.test(payload.paypal_debug_id));
    // (r25 send guard) What a send carries and to whom, side by side; account ids arrive masked (first 2, last 4).
    const maskedDispute = (value) => typeof value === 'string' && /^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}|\u2026)$/.test(value);
    const maskedAccount = (value) => value === null || (typeof value === 'string' && /^(?:[0-9A-Za-z]{2}\u2026[0-9A-Za-z]{4}|\u2026)$/.test(value));
    const token = (value) => value === null || (typeof value === 'string' && /^[A-Z][A-Z0-9_]{0,63}$/.test(value));
    const ACCOUNT_REFUSALS = ['account_identity_unknown', 'dispute_not_this_account', 'dispute_detail_required'];
    const READINESS_REFUSALS = ['seller_evidence_already_submitted', 'dispute_not_awaiting_seller', 'dispute_evidence_not_offered'];
    const sendGuardValid = !has('send_guard') || (object(payload.send_guard)
      && pk(payload.send_guard, ['case_ref', 'case_reason', 'dispute_masked', 'dispute_reason', 'dispute_amount', 'bound_dispute_masked', 'sending_account_masked', 'dispute_seller_masked', 'account_status', 'send_refusal'])
      && payload.send_guard.case_ref === body?.case_ref && token(payload.send_guard.case_reason) && maskedDispute(payload.send_guard.dispute_masked)
      && token(payload.send_guard.dispute_reason) && (payload.send_guard.dispute_amount === null || money(payload.send_guard.dispute_amount))
      && (payload.send_guard.bound_dispute_masked === null || maskedDispute(payload.send_guard.bound_dispute_masked))
      && maskedAccount(payload.send_guard.sending_account_masked) && maskedAccount(payload.send_guard.dispute_seller_masked)
      && ['MATCH', 'MISMATCH', 'UNKNOWN'].includes(payload.send_guard.account_status)
      && [null, ...ACCOUNT_REFUSALS, ...READINESS_REFUSALS].includes(payload.send_guard.send_refusal)
      // (r34 E1 P1-1) A matched account can still be refused for the dispute's state; an account refusal never matches.
      && (payload.send_guard.account_status === 'MATCH') === !ACCOUNT_REFUSALS.includes(payload.send_guard.send_refusal)
      && (payload.send_guard.account_status === 'MATCH' || payload.send_guard.send_refusal !== null));
    // (r30 J2 P2-1) The single-use send confirmation a preview issues: null, or 32 URL-safe characters.
    const confirmTokenValid = !has('confirm_token') || payload.confirm_token === null
      || (typeof payload.confirm_token === 'string' && /^[A-Za-z0-9_-]{32}$/.test(payload.confirm_token));
    // (2026-11-10) `note` is part of the dispute envelope (schemas.DisputeEnvelope: null or up to 300 characters). The
    // write routes serialise it as null, which the exact-key check refused ("API contract mismatch" on a live preview).
    const noteValid = !has('note') || payload.note === null || (typeof payload.note === 'string' && payload.note.length <= 300);
    const envelopeKeys = ['source', 'data_source_label', 'environment', 'evidence_class', 'observed_at', 'provider_submission', ...optional('paypal_debug_id', 'note')];
    const recordKeys = ['dispute_id', 'reason', 'status', 'dispute_life_cycle_stage', 'dispute_state', 'dispute_amount', 'create_time', 'update_time', 'seller_response_due_date'];
    const record = (row) => object(row) && disputeId(row.dispute_id) && text(row.reason) && text(row.status) && text(row.dispute_life_cycle_stage)
      && (row.dispute_state === null || text(row.dispute_state)) && money(row.dispute_amount) && text(row.create_time)
      && (row.update_time === null || text(row.update_time)) && (row.seller_response_due_date === null || text(row.seller_response_due_date));
    const fixture = payload.source === 'synthetic_fixture';
    valid = valid && ['paypal_sandbox', 'synthetic_fixture'].includes(payload.source) && payload.environment === 'sandbox'
      && payload.data_source_label === (fixture ? 'Fixture' : 'Sandbox')
      && (fixture ? payload.evidence_class === 'SYNTHETIC_FIXTURE' : ['AUTHENTIC_SANDBOX_RESPONSE', 'SYNTHETIC_TEST_RESPONSE'].includes(payload.evidence_class))
      && text(payload.observed_at) && ['NOT_PERFORMED', 'PERFORMED'].includes(payload.provider_submission) && debugIdValid && noteValid;
    if (valid && path === '/paypal/disputes') {
      valid = pk(payload, [...envelopeKeys, 'readback', 'items']) && payload.readback === 'GET_LIST' && payload.provider_submission === 'NOT_PERFORMED'
        && Array.isArray(payload.items) && payload.items.length <= 20 && payload.items.every((row) => pk(row, recordKeys) && record(row))
        && new Set(payload.items.map((row) => row.dispute_id)).size === payload.items.length;
    } else if (valid && path === '/paypal/disputes/provide-evidence') {
      const submitted = payload.external_send === 'SUBMITTED';
      // (2026-11-09) A send carries the plain SHA-256 of each file it posted, in the same order as `files`; a preview never does.
      const sha256 = (v) => typeof v === 'string' && /^[a-f0-9]{64}$/.test(v);
      const sentFilesValid = (!has('sent_files') || payload.sent_files === null) ? !submitted
        : submitted && Array.isArray(payload.sent_files) && Array.isArray(payload.files) && payload.sent_files.length === payload.files.length
          && payload.sent_files.every((row, index) => pk(row, ['filename', 'content_type', 'byte_length', 'sha256']) && payload.files[index]
            && row.filename === payload.files[index].filename && row.content_type === payload.files[index].content_type
            && row.byte_length === payload.files[index].byte_length && sha256(row.sha256));
      valid = pk(payload, [...envelopeKeys, 'readback', 'dispute_id', 'case_ref', 'method', 'path', 'content_type', 'input', 'files', 'external_send', 'submit_flag_enabled', 'human_review_required', ...optional('payload_sha256', 'send_guard', 'confirm_token', 'sent_files')]) && sendGuardValid && confirmTokenValid && sentFilesValid
        && (!has('payload_sha256') || payload.payload_sha256 === null || digest(payload.payload_sha256))
        && ['PROVIDE_EVIDENCE_PREVIEW', 'PROVIDE_EVIDENCE_SUBMITTED'].includes(payload.readback) && disputeId(payload.dispute_id)
        && payload.dispute_id === body?.dispute_id && payload.case_ref === body?.case_ref && payload.method === 'POST'
        && payload.path === `/v1/customer/disputes/${payload.dispute_id}/provide-evidence` && payload.content_type === 'multipart/form-data'
        && object(payload.input) && pk(payload.input, ['evidences']) && Array.isArray(payload.input.evidences) && payload.input.evidences.length >= 1 && payload.input.evidences.length <= 20
        && payload.input.evidences.every((row) => pk(row, ['evidence_type', 'evidence_info', 'notes']) && text(row.evidence_type) && text(row.notes) && object(row.evidence_info) && Array.isArray(row.evidence_info.tracking_info))
        && Array.isArray(payload.files) && payload.files.length <= 20
        && payload.files.every((row) => pk(row, ['name', 'filename', 'content_type', 'byte_length']) && text(row.name) && Number.isInteger(row.byte_length) && row.byte_length >= 0)
        && ['FROZEN', 'SUBMITTED'].includes(payload.external_send) && typeof payload.submit_flag_enabled === 'boolean' && payload.human_review_required === true
        && submitted === (payload.provider_submission === 'PERFORMED') && submitted === (payload.readback === 'PROVIDE_EVIDENCE_SUBMITTED')
        && (!submitted || (!fixture && payload.submit_flag_enabled));
    } else if (valid && path === '/paypal/disputes/add-tracking') {
      // (optimise r24) POST /v1/shipping/trackers-batch preview (masked) or, with every server gate open, the send.
      const submitted = payload.external_send === 'SUBMITTED';
      const carriers = ['USPS', 'UPS', 'FEDEX', 'DHL', 'TW_CHUNGHWA_POST', 'JP_JAPANPOST', 'OTHER'];
      const tracker = (row) => object(row) && pk(row, ['transaction_id', 'tracking_number', 'status', 'carrier', 'carrier_name_other'])
        && typeof row.transaction_id === 'string' && /^[A-Za-z0-9*._-]{1,64}$/.test(row.transaction_id)
        && text(row.tracking_number) && row.tracking_number.length <= 64 && row.status === 'SHIPPED' && carriers.includes(row.carrier)
        && ((row.carrier === 'OTHER') === (typeof row.carrier_name_other === 'string' && row.carrier_name_other.length > 0))
        && (row.carrier === 'OTHER' || row.carrier_name_other === null);
      valid = pk(payload, [...envelopeKeys, 'readback', 'dispute_id', 'case_ref', 'method', 'path', 'content_type', 'body', 'external_send', 'submit_flag_enabled', 'human_review_required', ...optional('payload_sha256', 'send_guard', 'confirm_token')]) && sendGuardValid && confirmTokenValid
        && (!has('payload_sha256') || payload.payload_sha256 === null || digest(payload.payload_sha256))
        && ['ADD_TRACKING_PREVIEW', 'ADD_TRACKING_SUBMITTED'].includes(payload.readback) && disputeId(payload.dispute_id)
        && payload.dispute_id === body?.dispute_id && payload.case_ref === body?.case_ref && payload.method === 'POST'
        && payload.path === '/v1/shipping/trackers-batch' && payload.content_type === 'application/json'
        && object(payload.body) && pk(payload.body, ['trackers']) && Array.isArray(payload.body.trackers) && payload.body.trackers.length === 1
        && payload.body.trackers.every(tracker)
        && ['FROZEN', 'SUBMITTED'].includes(payload.external_send) && typeof payload.submit_flag_enabled === 'boolean' && payload.human_review_required === true
        && submitted === (payload.provider_submission === 'PERFORMED') && submitted === (payload.readback === 'ADD_TRACKING_SUBMITTED')
        && (!submitted || (!fixture && payload.submit_flag_enabled));
    } else if (valid) {
      valid = pk(payload, [...envelopeKeys, 'readback', ...recordKeys, 'dispute_channel', 'disputed_transactions', 'evidences']) && payload.readback === 'GET_DETAIL'
        && payload.provider_submission === 'NOT_PERFORMED' && record(payload) && payload.dispute_id === path.slice('/paypal/disputes/'.length)
        && (payload.dispute_channel === null || text(payload.dispute_channel))
        && Array.isArray(payload.disputed_transactions) && payload.disputed_transactions.length <= 10
        && payload.disputed_transactions.every((row) => pk(row, ['seller_transaction_id', 'transaction_status', 'gross_amount', 'seller_protection_eligible']) && text(row.seller_transaction_id) && (row.gross_amount === null || money(row.gross_amount)))
        && Array.isArray(payload.evidences) && payload.evidences.length <= 20
        && payload.evidences.every((row) => pk(row, ['evidence_type', 'source', 'action', 'date']) && text(row.evidence_type) && text(row.source));
    }
  } else if (path.startsWith('/disputes/') && path.endsWith('/draft')) {
    const routing = payload.routing;
    const summary = payload.restricted_original_summary;
    const requirementStates = ['CONTEXT_ONLY','UNMAPPED_EVIDENCE_TYPE','PROVIDER_REQUEST_OUTSIDE_LOCAL_MATRIX','STRUCTURALLY_PRESENT','MANDATORY_EVIDENCE_MISSING','OPTIONAL_EVIDENCE_MISSING'];
    const overallStates = ['CASE_NOT_ACTIONABLE','MANUAL_REVIEW','DUE_DATE_EXPIRED','ACTION_NOT_AVAILABLE','NEEDS_INPUT','READY_FOR_LOCAL_REVIEW'];
    const requirementValid = (row) => pk(row,['request_id','provider_evidence_type','evidence_type','source','mandatory','action','requirement_state','proof_count','accepted_attachment_count'])
      && text(row.request_id) && text(row.provider_evidence_type) && (row.evidence_type === null || text(row.evidence_type))
      && text(row.source) && typeof row.mandatory === 'boolean' && (row.action === null || text(row.action))
      && requirementStates.includes(row.requirement_state) && Number.isInteger(row.proof_count) && row.proof_count >= 0 && row.proof_count <= 128
      && Number.isInteger(row.accepted_attachment_count) && row.accepted_attachment_count >= 0 && row.accepted_attachment_count <= 20;
    const draftKeys = ['case_ref','status','evidence','review_reasons','recommendation','limitations','policy_version','advisory_only','source','routing','restricted_original_summary','scenario_match','draft_digest','identity_redaction','document_redaction'];
    const hasTimeEvidence = Object.prototype.hasOwnProperty.call(payload, 'time_evidence');
    const timeFlags = ['ORDER_RECORD_ABSENT','DELIVERY_NOT_RECORDED','DELIVERY_AFTER_CLAIM','CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME'];
    const timeEventValid = (row) => po(row) && (row.kind === 'MESSAGE'
      ? pk(row,['kind','at','source','channel','direction','topic','message_digest'])
        && row.source === 'SELLER_PROVIDED_UNVERIFIED' && ['EMAIL','PRIVATE_MESSAGE'].includes(row.channel)
        && ['INBOUND','OUTBOUND'].includes(row.direction)
        && ['PAYMENT_NOTICE','ORDER_DETAILS_REQUEST','ORDER_DETAILS_PROVIDED','DELIVERY_NOTICE','REFUND_REQUEST','OTHER'].includes(row.topic)
        && typeof row.message_digest === 'string' && /^[a-f0-9]{64}$/u.test(row.message_digest)
      : pk(row,['kind','at','source']) && ['PAYMENT','ORDER_RECORD_CREATED','DELIVERY','CLAIM_OPENED'].includes(row.kind)
        && ['PROVIDER','SELLER_PROVIDED_UNVERIFIED'].includes(row.source))
      && policyInstant(row.at) !== null;
    const timeEvidenceValid = (value) => pk(value,['schema_version','events','gaps_seconds','flags','judgement','advisory_only'])
      && value.schema_version === 'payguard.time_evidence.v1' && value.judgement === 'NOT_MADE' && value.advisory_only === true
      && Array.isArray(value.events) && value.events.length >= 2 && value.events.length <= 30 && value.events.every(timeEventValid)
      && pk(value.gaps_seconds,['payment_to_order_record','payment_to_delivery','delivery_to_claim','payment_to_claim'])
      && Object.values(value.gaps_seconds).every((gap) => gap === null || (Number.isInteger(gap) && Math.abs(gap) <= 31536000))
      && pl(value.flags, timeFlags, 4);
    valid = valid && pk(payload, hasTimeEvidence ? [...draftKeys, 'time_evidence'] : draftKeys)
      && (!hasTimeEvidence || timeEvidenceValid(payload.time_evidence))
      && payload.source === 'synthetic' && text(payload.case_ref) && digest(payload.draft_digest)
      && object(payload.evidence) && pk(payload.evidence,['reason','opened_at','order_created_at','carrier_status','delivered_at','evidence_source'])
      && payload.evidence.evidence_source === 'synthetic'
      && Array.isArray(payload.review_reasons) && payload.review_reasons.every(text)
      && object(routing) && pk(routing,['schema_version','snapshot_class','reason','status','dispute_life_cycle_stage','seller_response_due_date','due_state','available_actions','requirements','overall_state','human_review_required','provider_submission'])
      && routing.schema_version === 1 && routing.snapshot_class === 'SYNTHETIC_PROVIDER_FIXTURE'
      && text(routing.reason) && text(routing.status) && text(routing.dispute_life_cycle_stage)
      && text(routing.seller_response_due_date) && Number.isFinite(Date.parse(routing.seller_response_due_date))
      && ['OPEN','EXPIRED'].includes(routing.due_state) && Array.isArray(routing.available_actions) && routing.available_actions.length <= 20
      && new Set(routing.available_actions).size === routing.available_actions.length && routing.available_actions.every(text)
      && Array.isArray(routing.requirements) && routing.requirements.length >= 1 && routing.requirements.length <= 20
      && routing.requirements.every(requirementValid) && new Set(routing.requirements.map((row) => row.request_id)).size === routing.requirements.length
      && overallStates.includes(routing.overall_state) && routing.human_review_required === true && routing.provider_submission === 'NOT_PERFORMED'
      && object(summary) && pk(summary,['schema_version','profile','data_class','custody','persistent_storage','production_pii_vault','proof_record_count','attachment_count','content_returned','provider_submission'])
      && summary.schema_version === 1 && summary.profile === 'RESTRICTED_ORIGINAL_METADATA_V1'
      && summary.data_class === 'SYNTHETIC_RESTRICTED_EVIDENCE' && summary.custody === 'SESSION_MEMORY_ONLY'
      && summary.persistent_storage === 'NOT_IMPLEMENTED' && summary.production_pii_vault === 'NOT_IMPLEMENTED'
      && Number.isInteger(summary.proof_record_count) && summary.proof_record_count >= 0 && summary.proof_record_count <= 128
      && Number.isInteger(summary.attachment_count) && summary.attachment_count >= 0 && summary.attachment_count <= 20
      && summary.content_returned === false && summary.provider_submission === 'NOT_PERFORMED'
      && object(payload.identity_redaction) && text(payload.identity_redaction.method)
      && Array.isArray(payload.identity_redaction.fields) && payload.identity_redaction.fields.every(text)
      && object(payload.document_redaction)
      && payload.document_redaction.export_profile === 'INTERNAL_REVIEW_ONLY_V1'
      && text(payload.document_redaction.redacted_text)
      && payload.document_redaction.manual_review_required === true
      && payload.document_redaction.reversibility === false;
  } else if (path.startsWith('/disputes/') && path.endsWith('/approve')) {
    valid = valid && pk(payload,['case_ref','action','status','external_submission','authenticated_actor','durable_approval','reviewer','reviewed_at','retention','source'])
      && text(payload.case_ref) && payload.action === 'review_draft' && payload.status === 'local_draft_reviewed'
      && payload.source === 'synthetic' && payload.external_submission === 'FROZEN'
      && payload.authenticated_actor === false && payload.durable_approval === false
      && payload.reviewer === 'DEMO_OPERATOR_UNAUTHENTICATED'
      && text(payload.reviewed_at) && Number.isFinite(Date.parse(payload.reviewed_at))
      && payload.retention === 'SESSION_MEMORY_ONLY';
  } else if (path === '/country-rules/check') {
    // Per-country PayPal rules: closed severities and codes, official PayPal source links only, never a decision.
    const severities = ['BLOCK', 'WARN', 'INFO'];
    valid = valid && pk(payload, ['schema_version','seller_country','buyer_country','cross_border','blocked','findings','retrieved_at','advisory_only','legal_advice'])
      && payload.schema_version === 'payguard.country_rules.v1' && payload.advisory_only === true && payload.legal_advice === false
      && typeof payload.cross_border === 'boolean' && typeof payload.blocked === 'boolean'
      && Array.isArray(payload.findings) && payload.findings.length <= 120
      && payload.findings.every((row) => pk(row, ['severity','code','text','source']) && severities.includes(row.severity)
        && /^[a-z_]{3,48}$/.test(row.code) && text(row.text) && row.text.length <= 1200
        && /^(https:\/\/((www|developer)\.paypal\.com|([a-z0-9-]+\.)*(gov|gov\.(tw|cn|uk|au|sg|hk)|go\.jp|gc\.ca|canada\.ca|europa\.eu|gesetze-im-internet\.de|zoll\.de|dhl\.de|royalmail\.com|usps\.com|canadapost-postescanada\.ca|japanpost\.jp|singpost\.com|hongkongpost\.hk|auspost\.com\.au))|http:\/\/www\.npc\.gov\.cn)\//.test(row.source))
      && payload.blocked === payload.findings.some((row) => row.severity === 'BLOCK');
  } else if (path === '/country-rules/countries') {
    valid = valid && payload.schema_version === 'payguard.country_rules.v1' && Array.isArray(payload.countries)
      && payload.countries.length > 0 && payload.countries.length <= 20
      && payload.countries.every((row) => pk(row, ['code','name']) && /^[A-Z]{2}$/.test(row.code) && text(row.name))
      && object(payload.goods_tags) && ['prohibited','approval','law_dependent'].every((key) => Array.isArray(payload.goods_tags[key]));
  } else if (path === '/paypal/invoices/review') {
    valid = valid && payload.source === 'synthetic' && text(payload.review_token) && digest(payload.payload_digest)
      && text(payload.expires_at) && payload.action === 'create_sandbox_invoice_draft';
  } else if (path === '/paypal/invoices/draft') {
    valid = valid && pk(payload,['source','invoice_id','status','environment','external_send','evidence_receipt'])
      && payload.source === 'paypal_sandbox' && text(payload.invoice_id)
      && payload.status === 'DRAFT' && payload.environment === 'sandbox' && payload.external_send === 'FROZEN';
    if (valid) assertSandboxReceipt(payload.evidence_receipt,'CREATE_INVOICE_DRAFT',payload.invoice_id);
  }
  if (!valid) throw new ApiError('API contract mismatch. Unverified content is hidden; check the backend version.', 502, 'contract_error');
  return payload;
}

export async function apiRequest(path, { method = 'GET', body, session, signal } = {}) {
  const controller = new AbortController();
  // (red team r26 #1 P1) A PayPal write can take two provider calls of up to 15 s each behind the adapter lock, so
  // the browser waits 45 s for them, and a timeout says the write may have happened instead of "try again".
  const paypalWrite = PAYPAL_WRITE_PATHS.includes(path);
  const timeout = setTimeout(() => controller.abort(), path === '/ai/evidence-brief' ? 65000 : paypalWrite ? 45000 : 15000);
  const abort = () => controller.abort();
  signal?.addEventListener('abort', abort, { once: true });
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (session) {
    headers['X-Demo-Session'] = session.session_id;
    if (method !== 'GET') headers['X-CSRF-Token'] = session.csrf_token;
  }
  try {
    if (signal?.aborted) {
      controller.abort();
      throw new ApiError('Request canceled.', 0, 'request_cancelled');
    }
    // The only query the console sends: which situation's guide state to read.
    const [basePath, query] = path.split('?');
    if (query !== undefined && !(basePath === '/guide/state' && /^scenario=(?:preflight|velocity|dispute)$/.test(query))) {
      throw new ApiError('Request path is not allowed.', 0, 'request_invalid');
    }
    const response = await fetch(`/api/v1${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
      credentials: 'omit',
      cache: 'no-store',
      redirect: 'error',
    });
    // (attack r23) Only a 429 or 503 carries a wait the page honours.
    const retryAfter = [429, 503].includes(response.status) ? parseRetryAfter(response.headers.get('Retry-After')) : null;
    let payload;
    try {
      payload = await response.json();
    } catch {
      if (retryAfter) throw new ApiError(response.status === 429 ? 'Too many requests; slow down.' : 'TradeGlot is busy right now.', response.status, response.status === 429 ? 'rate_limited' : 'server_busy', retryAfter);
      throw new ApiError('The API returned invalid content; check the backend service.', response.status, 'invalid_response');
    }
    if (!response.ok) {
      const code = payload?.error?.code || 'request_failed';
      throw new ApiError(payload?.error?.message || SEND_GUARD_MESSAGES[code] || 'Request failed; try again.', response.status, code, retryAfter,
        { paypalIssue: payload?.error?.paypal_issue ?? null, paypalDebugId: payload?.error?.paypal_debug_id ?? null });
    }
    if (signal?.aborted) throw new ApiError('Request canceled.', 0, 'request_cancelled');
    if (['/references/search', '/policy/assess', '/advisory/evaluate'].includes(basePath)) await loadReferenceContract().catch(contractFailure);
    return assertContract(basePath, payload, session, query === undefined ? body : { scenario: query.slice('scenario='.length) });
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (signal?.aborted) throw new ApiError('Request canceled.', 0, 'request_cancelled');
    if (error.name === 'AbortError' && paypalWrite) throw new ApiError(PAYPAL_WRITE_TIMEOUT_MESSAGE, 0, 'request_timeout');
    throw new ApiError(error.name === 'AbortError' ? 'Request timed out; try again.' : 'Cannot connect to the backend service; confirm that the API is running.', 0, error.name === 'AbortError' ? 'request_timeout' : 'backend_unavailable');
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener('abort', abort);
  }
}
