import {
  POLICY_COVERAGE,
  REFERENCE_CHUNKS as POLICY_CHUNKS,
  REFERENCE_CHUNK_DIGEST,
  REFERENCE_COMBINED_DIGEST,
  REFERENCE_CORPUS_ID,
  REFERENCE_OUTCOMES,
  REFERENCE_ROWS,
  REFERENCE_SOURCES as POLICY_SOURCES,
  REFERENCE_SOURCE_DIGEST,
  REFERENCE_STAGES,
  REFERENCE_TYPES,
} from './referenceContract.js';

export { REFERENCE_TYPES } from './referenceContract.js';

export class ApiError extends Error {
  constructor(message, status, code) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

const REFERENCE_SOURCE_IDS = new Set(Object.keys(POLICY_SOURCES));
const REFERENCE_CHUNK_IDS = new Set(Object.keys(REFERENCE_ROWS));
const REFERENCE_URLS = new Set(Object.values(POLICY_SOURCES).map((source) => source.url));

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
    return REFERENCE_URLS.has(value);
  } catch { return false; }
}

function referenceProvenance(row) {
  const source = POLICY_SOURCES[row.source_id];
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
    || payload.source !== 'public_reference' || payload.corpus_id !== REFERENCE_CORPUS_ID || payload.advisory_only !== true
    || payload.operational_authority !== 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION' || payload.corpus_digest !== REFERENCE_COMBINED_DIGEST
    || !keys(payload.corpus_digests, ['sources_sha256', 'chunks_sha256']) || payload.corpus_digests.sources_sha256 !== REFERENCE_SOURCE_DIGEST || payload.corpus_digests.chunks_sha256 !== REFERENCE_CHUNK_DIGEST
    || !keys(payload.filters_applied, filterKeys)) contractFailure();
  const filters = payload.filters_applied;
  const types = [...(request.material_types ?? REFERENCE_TYPES)].sort();
  if (!['source_compliance', 'velocity_guard', 'dispute_mediation'].includes(filters.theme) || filters.jurisdiction !== 'US'
    || request.jurisdiction !== 'US' || !REFERENCE_STAGES.includes(filters.case_stage)
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
    const expected = REFERENCE_ROWS[row?.chunk_id];
    if (!keys(row, citationKeys) || !text(row.chunk_id, 128) || !/^[A-Z0-9-]+$/.test(row.chunk_id) || ids.has(row.chunk_id)
      || !REFERENCE_CHUNK_IDS.has(row.chunk_id) || !REFERENCE_SOURCE_IDS.has(row.source_id) || !expected
      || !['title', 'source_title', 'text', 'locator'].every((key) => text(row[key])) || !text(row.jurisdiction_label, 2000)
      || !safeReferenceUrl(row.url) || !digest(row.text_sha256) || !Number.isInteger(row.relevance_score) || row.relevance_score < 1 || row.relevance_score > 128
      || row.jurisdiction !== filters.jurisdiction || !filters.material_types.includes(row.material_type) || !time(row.retrieved_at)
      || !REFERENCE_STAGES.slice(1).includes(row.case_stage) || (filters.case_stage !== 'any' && row.case_stage !== filters.case_stage)
      || !['source_updated_date', 'effective_date', 'decision_date', 'decision_acceptance_deadline'].every((key) => date(row[key]))) contractFailure();
    ids.add(row.chunk_id);
    if (!referenceProvenance(row) || !Object.keys(expected).every((key) => JSON.stringify(row[key]) === JSON.stringify(expected[key]))) contractFailure();
    for (const [key, statuses] of [['source_updated_date', ['DOCUMENT_STATED', 'MISSING']], ['effective_date', ['DOCUMENT_STATED', 'NOT_VERIFIED']], ['decision_date', ['DOCUMENT_STATED', 'NOT_STATED_IN_REVIEWED_DOCUMENT', 'NOT_APPLICABLE']]]) {
      if (!statuses.includes(row[`${key}_status`]) || (row[key] !== null) !== (row[`${key}_status`] === 'DOCUMENT_STATED')) contractFailure();
    }
    if ((filters.require_known_source_date || filters.max_source_age_days !== null) && row.source_updated_date === null) contractFailure();
    if (row.material_type === 'public_court_order_copy') {
      if (row.case_stage !== 'procedural_order' || row.jurisdiction !== 'US' || !REFERENCE_OUTCOMES.includes(row.case_outcome)) contractFailure();
    } else if (row.case_stage !== 'not_applicable' || row.case_outcome !== null) contractFailure();
  }
  return payload;
}


export const POLICY_CLAIM_TYPES = ['policy_reference', 'current_policy', 'historical_case', 'procedural_reference', 'api_reference', 'guidance_reference', 'financial_action', 'assurance'];
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
  return policyContext(context,request) && p.schema_version === 1 && p.corpus_id === REFERENCE_CORPUS_ID && p.corpus_digest === REFERENCE_COMBINED_DIGEST && pk(p.corpus_digests,['sources_sha256','chunks_sha256']) && p.corpus_digests.sources_sha256 === REFERENCE_SOURCE_DIGEST && p.corpus_digests.chunks_sha256 === REFERENCE_CHUNK_DIGEST && p.advisory_only === true && p.operational_authority === POLICY_AUTHORITY && p.requires_human_review === true && p.current_policy_applicability === 'NOT_ESTABLISHED' && Array.isArray(p.limitations) && p.limitations.length > 0 && p.limitations.length <= 32 && p.limitations.every(pt) && pk(p.coverage,['complete','basis','regional_source_count','selected_source_count','selected_chunk_count','official_policy_source_ids','official_policy_chunk_count_by_theme','missing_official_policy_themes']) && pe(p.coverage,POLICY_COVERAGE[`${context.jurisdiction}|${context.theme}`]);
}
export function assertPolicyAssessment(p, request) {
  const fields=['schema_version','version','source','corpus_id','corpus_digest','corpus_digests','filters_applied','status','current_policy_applicability','advisory_only','operational_authority','requires_human_review','coverage','sources','chunks','reason_codes','limitations'];
  if (!pk(p,fields) || !policyCommon(p,request,p.filters_applied) || p.version !== 'payguard.applicability.v1' || p.source !== 'public_reference' || p.status !== 'INCOMPLETE_POLICY_EVIDENCE' || !pl(p.reason_codes,POLICY_REASONS,15,1) || !Array.isArray(p.sources) || p.sources.length !== p.coverage.selected_source_count || !Array.isArray(p.chunks) || p.chunks.length !== p.coverage.selected_chunk_count) contractFailure();
  const expectedChunks=Object.values(POLICY_CHUNKS).filter(c=>c.jurisdiction===request.jurisdiction && c.theme===request.theme).sort((a,b)=>a.chunk_id.localeCompare(b.chunk_id));
  if (!pe(p.chunks,expectedChunks)) contractFailure();
  const ids=[...new Set(expectedChunks.map(c=>c.source_id))].sort();
  if (!pe(p.sources.map(s=>s?.source_id),ids)) contractFailure();
  for (const s of p.sources) {
    const fixed=POLICY_SOURCES[s.source_id];
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
    const trusted=Array.isArray(c?.citation_chunk_ids) ? [...new Set(c.citation_chunk_ids.filter(id=>Object.hasOwn(POLICY_CHUNKS,id)))].sort() : null;
    if (!pk(g,['claim_index','claim_type','status','trusted_citation_chunk_ids','reason_codes']) || g.claim_index!==i || !POLICY_CLAIM_TYPES.includes(g.claim_type) || g.claim_type!==c?.claim_type || !statuses.includes(g.status) || !pe(g.trusted_citation_chunk_ids,trusted) || !pl(g.reason_codes,CLAIM_REASONS,10) || (g.status==='STRUCTURE_COMPATIBLE' && g.reason_codes.length!==0) || (g.status!=='STRUCTURE_COMPATIBLE' && !g.reason_codes.length)) contractFailure();
  }
  const overall=p.claim_gates.some(g=>g.status==='REJECTED')?'REJECTED':p.claim_gates.some(g=>g.status==='INCOMPLETE_EVIDENCE')?'INCOMPLETE_EVIDENCE':'STRUCTURE_COMPATIBLE';
  if(p.status!==overall) contractFailure();
  return p;
}

export function assertSandboxReceipt(receipt, action, invoiceId = null) {
  const fields = ['schema_version','environment','action','status','observed_at','invoice_id','evidence_class','proof_kind','separate_get_readback','external_send'];
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
const AI_PROMPT_CONTRACT_ID = 'payguard-bounded-advisory-v2';
const AI_PROMPT_CONTRACT_DIGEST = '2f870a865397a3e41a00bd51f85d96be5cce9ba77ad517d86d779dd3e15f2941';
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
  if (!pk(payload, envelope) || !pk(request, ['stage']) || !Object.hasOwn(AI_CITATIONS, request.stage)
      || payload.schema_version !== '1.0' || payload.status !== 'completed' || payload.stage !== request.stage
      || payload.fixture_id !== 'payguard-fixed-synthetic-brief-v1' || !digest(payload.context_digest) || !digest(payload.corpus_digest)
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
      || !payload.limitations.every((value) => boundedText(value, 1200))) contractFailure();
  return payload;
}

function assertContract(path, payload, session, body) {
  if (path === '/policy/assess') return assertPolicyAssessment(payload, body);
  if (path === '/advisory/evaluate') return assertAdvisoryEvaluation(payload, body);
  if (path === '/ai/evidence-brief') return assertAiBrief(payload, body);
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
      && payload.disputes.every((row) => object(row) && pk(row,['case_ref','order_ref','reason','opened_at','status'])
        && ['case_ref', 'order_ref', 'reason', 'opened_at', 'status'].every((key) => text(row[key])))
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
  } else if (path === '/paypal/status' || path === '/paypal/connect') {
    valid = valid && pk(payload,['configured','status','environment','last_verified_at','source','evidence_receipt'])
      && payload.source === 'paypal_sandbox' && payload.environment === 'sandbox' && typeof payload.configured === 'boolean'
      && ['not_configured', 'disconnected', 'connected', 'error'].includes(payload.status);
    if (valid && payload.status === 'connected') {
      assertSandboxReceipt(payload.evidence_receipt,'OAUTH_CONNECT');
      valid = payload.configured && payload.last_verified_at === payload.evidence_receipt.observed_at;
    } else if (valid) valid = payload.evidence_receipt === null;
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
    valid = valid && pk(payload,['case_ref','status','evidence','review_reasons','recommendation','limitations','policy_version','advisory_only','source','routing','restricted_original_summary','scenario_match','draft_digest','identity_redaction','document_redaction'])
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
  const timeout = setTimeout(() => controller.abort(), path === '/ai/evidence-brief' ? 25000 : 15000);
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
    const response = await fetch(`/api/v1${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
      credentials: 'omit',
      cache: 'no-store',
      redirect: 'error',
    });
    let payload;
    try {
      payload = await response.json();
    } catch {
      throw new ApiError('The API returned invalid content; check the backend service.', response.status, 'invalid_response');
    }
    if (!response.ok) {
      throw new ApiError(payload?.error?.message || 'Request failed; try again.', response.status, payload?.error?.code || 'request_failed');
    }
    if (signal?.aborted) throw new ApiError('Request canceled.', 0, 'request_cancelled');
    return assertContract(path, payload, session, body);
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (signal?.aborted) throw new ApiError('Request canceled.', 0, 'request_cancelled');
    throw new ApiError(error.name === 'AbortError' ? 'Request timed out; try again.' : 'Cannot connect to the backend service; confirm that the API is running.', 0, error.name === 'AbortError' ? 'request_timeout' : 'backend_unavailable');
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener('abort', abort);
  }
}
