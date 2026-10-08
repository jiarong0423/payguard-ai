import { buildPseudonymizedEvidenceExport } from './pseudonymizedExport.js';

const encoder = new TextEncoder();
const decoder = new TextDecoder('utf-8', { fatal: true });
const MAX_FILE_BYTES = 131072;
const MAX_ARCHIVE_BYTES = 262144;
const FIXED_FILES = Object.freeze([
  'README.txt',
  'manifest.json',
  'requirements.json',
  'timeline.json',
  'public-sources.json',
  'pseudonymized-evidence.json',
]);
const TOP_LEVEL_KEYS = [
  'status', 'evidence', 'review_reasons', 'recommendation', 'limitations',
  'policy_version', 'advisory_only', 'source', 'routing', 'restricted_original_summary',
  'scenario_match', 'draft_digest', 'identity_redaction', 'document_redaction',
];
const OPTIONAL_TOP_LEVEL_KEYS = ['case_ref'];
const ROUTING_KEYS = [
  'schema_version', 'snapshot_class', 'reason', 'status', 'dispute_life_cycle_stage',
  'seller_response_due_date', 'due_state', 'available_actions', 'requirements',
  'overall_state', 'human_review_required', 'provider_submission',
];
const REQUIREMENT_KEYS = [
  'request_id', 'provider_evidence_type', 'evidence_type', 'source', 'mandatory',
  'action', 'requirement_state', 'proof_count', 'accepted_attachment_count',
];
const CITATION_KEYS = [
  'chunk_id', 'source_id', 'title', 'url', 'locator', 'material_type',
  'jurisdiction', 'text_sha256',
];
const AUTHORITY = Object.freeze({
  advisory_only: true,
  export_profile: 'INTERNAL_REVIEW_ONLY_V1',
  provider_submission: 'NOT_PERFORMED',
  dispute_decision: 'NOT_MADE',
  human_review_required: true,
  paypal_supported_attachment: false,
  complete_official_evidence: false,
  external_action_authorized: false,
});
const MANIFEST_STATUS = 'INTERNAL_REVIEW_ONLY';
const MANIFEST_POLICY_VERSION = 'payguard.demo.v1';
const MANIFEST_LIMITATIONS = Object.freeze([
  'INTERNAL_REVIEW_ONLY',
  'SYNTHETIC_PSEUDONYMIZED_ADVISORY',
  'INCOMPLETE_OFFICIAL_EVIDENCE',
  'NO_RESTRICTED_ORIGINALS_OR_RAW_ATTACHMENTS',
  'NO_PAYPAL_SUBMISSION_OR_DISPUTE_VERDICT',
  'HUMAN_REVIEW_REQUIRED',
]);
const EXCLUDED_DATA_CLASSES = Object.freeze([
  'RAW_CASE_ORDER_REQUEST_IDENTIFIERS',
  'IDENTITY_SESSION_DRAFT_DIGESTS',
  'RESTRICTED_PROOF_VALUES',
  'ATTACHMENT_FILENAMES_AND_BYTES',
  'UNKNOWN_FIELDS',
]);
const MEDIA_TYPES = Object.freeze({
  'README.txt': 'text/plain; charset=utf-8',
  'requirements.json': 'application/json',
  'timeline.json': 'application/json',
  'public-sources.json': 'application/json',
  'pseudonymized-evidence.json': 'application/json',
});
const SHA256_CONSTANTS = Object.freeze([
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]);

function invalid() {
  throw new Error('internal_review_zip_invalid');
}

function plainObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) invalid();
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) invalid();
  return value;
}

function exactObject(value, keys) {
  plainObject(value);
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) invalid();
  return value;
}

function exactObjectWithOptional(value, requiredKeys, optionalKeys) {
  plainObject(value);
  const allowed = new Set([...requiredKeys, ...optionalKeys]);
  if (requiredKeys.some((key) => !Object.prototype.hasOwnProperty.call(value, key))) invalid();
  if (Object.keys(value).some((key) => !allowed.has(key))) invalid();
  return value;
}

function boundedText(value, maximum, pattern = null) {
  if (typeof value !== 'string' || value.length === 0 || encoder.encode(value).length > maximum) invalid();
  if (/[\x00-\x1f\x7f]/u.test(value) || (pattern && !pattern.test(value))) invalid();
  return value;
}

function exportText(value, maximum, knownForbidden = []) {
  const checked = boundedText(value, maximum);
  let normalized;
  try {
    normalized = checked.normalize('NFKC').toLowerCase();
  } catch {
    invalid();
  }
  for (const forbidden of knownForbidden) {
    if (typeof forbidden === 'string' && forbidden.length >= 8 && normalized.includes(forbidden.normalize('NFKC').toLowerCase())) invalid();
  }
  if (
    /\b[a-f0-9]{64}\b/iu.test(normalized)
    || /(?:^|[^a-z0-9])(?:sk|rk|pk|api)[_-][a-z0-9_-]{12,}/iu.test(normalized)
    || /(?:secret|token|password|credential)[_:= -]+[a-z0-9_-]{8,}/iu.test(normalized)
    || /\b(?:case|order|request|dispute|tracking|refund|attachment|file)[_ -]?id(?:\s*[:=]\s*|\s+)[a-z0-9][a-z0-9._-]{2,}\b/iu.test(normalized)
    || /\b(?:demo|raw|private)[_-](?:case|order|request|dispute|tracking|refund|attachment)[_-][a-z0-9_-]{3,}/iu.test(normalized)
    || /\b(?:case-ref|order-ref|requirement)-[0-9]{3,}\b/iu.test(normalized)
    || /\b[^\s/\\]{1,128}\.(?:pdf|png|jpe?g|gif|docx?|xlsx?|zip)\b/iu.test(normalized)
  ) invalid();
  return checked;
}

function optionalText(value, maximum, pattern = null) {
  return value === null ? null : boundedText(value, maximum, pattern);
}

function enumValue(value, values) {
  if (!values.includes(value)) invalid();
  return value;
}

function exactBoolean(value, expected) {
  if (typeof value !== 'boolean' || value !== expected) invalid();
  return value;
}

function booleanValue(value) {
  if (typeof value !== 'boolean') invalid();
  return value;
}

function boundedInteger(value, minimum, maximum) {
  if (!Number.isInteger(value) || value < minimum || value > maximum) invalid();
  return value;
}

function uniqueArray(value, minimum, maximum) {
  if (!Array.isArray(value) || value.length < minimum || value.length > maximum) invalid();
  return value;
}

function timestamp(value) {
  boundedText(value, 64, /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})$/u);
  if (Number.isNaN(Date.parse(value))) invalid();
  return value;
}

function officialUrl(value) {
  boundedText(value, 2048);
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    invalid();
  }
  if (parsed.protocol !== 'https:' || parsed.username || parsed.password || (parsed.port && parsed.port !== '443') || parsed.hash) invalid();
  const host = parsed.hostname;
  const path = parsed.pathname;
  const developerPath = host === 'developer.paypal.com' && ['/api/', '/sandbox-testing/', '/disputes/', '/platforms/disputes/'].some((prefix) => path.startsWith(prefix));
  const policyPath = host === 'www.paypal.com' && path.startsWith('/us/legalhub/paypal/');
  const courtPath = host === 'www.govinfo.gov' && path.startsWith('/content/pkg/USCOURTS-cand-') && path.endsWith('.pdf');
  if (!developerPath && !policyPath && !courtPath) invalid();
  if (/%2e|%2f|%5c/iu.test(path) || path.split('/').some((part) => part === '.' || part === '..')) invalid();
  if (policyPath) {
    if (parsed.search !== '?country.x=US&locale.x=en_US') invalid();
  } else if (parsed.search) invalid();
  return value;
}

function validateEvidence(value) {
  exactObject(value, ['reason', 'opened_at', 'order_created_at', 'carrier_status', 'delivered_at', 'evidence_source']);
  const reason = optionalText(value.reason, 128, /^[A-Z][A-Z0-9_]{0,127}$/u);
  const openedAt = value.opened_at === null ? null : timestamp(value.opened_at);
  const orderCreatedAt = value.order_created_at === null ? null : timestamp(value.order_created_at);
  const deliveredAt = value.delivered_at === null ? null : timestamp(value.delivered_at);
  const carrierStatus = value.carrier_status === null
    ? null
    : enumValue(value.carrier_status, ['delivered', 'in_transit', 'not_shipped', 'unknown']);
  enumValue(value.evidence_source, ['synthetic']);
  return {
    reason,
    order_created_at: orderCreatedAt,
    delivered_at: deliveredAt,
    dispute_opened_at: openedAt,
    carrier_status: carrierStatus,
    evidence_source: value.evidence_source,
  };
}

function validateRequirement(value) {
  exactObject(value, REQUIREMENT_KEYS);
  const requirementRef = boundedText(value.request_id, 32, /^requirement-[0-9]{3}$/u);
  const providerEvidenceType = boundedText(value.provider_evidence_type, 128, /^[A-Z][A-Z0-9_]{0,127}$/u);
  const evidenceType = optionalText(value.evidence_type, 128, /^[A-Z][A-Z0-9_]{0,127}$/u);
  const source = boundedText(value.source, 128, /^[A-Z][A-Z0-9_]{0,127}$/u);
  const mandatory = booleanValue(value.mandatory);
  const action = optionalText(value.action, 128, /^[A-Z][A-Z0-9_]{0,127}$/u);
  const requirementState = enumValue(value.requirement_state, [
    'CONTEXT_ONLY', 'UNMAPPED_EVIDENCE_TYPE', 'PROVIDER_REQUEST_OUTSIDE_LOCAL_MATRIX',
    'STRUCTURALLY_PRESENT', 'MANDATORY_EVIDENCE_MISSING', 'OPTIONAL_EVIDENCE_MISSING',
  ]);
  return {
    requirement_ref: requirementRef,
    provider_evidence_type: providerEvidenceType,
    evidence_type: evidenceType,
    source,
    mandatory,
    action,
    requirement_state: requirementState,
    proof_record_count: boundedInteger(value.proof_count, 0, 128),
    accepted_attachment_count: boundedInteger(value.accepted_attachment_count, 0, 20),
  };
}

function validateRouting(value) {
  exactObject(value, ROUTING_KEYS);
  if (value.schema_version !== 1) invalid();
  enumValue(value.snapshot_class, ['SYNTHETIC_PROVIDER_FIXTURE']);
  const reason = enumValue(value.reason, [
    'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', 'MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED',
    'UNAUTHORISED', 'CREDIT_NOT_PROCESSED', 'DUPLICATE_TRANSACTION', 'INCORRECT_AMOUNT',
    'PAYMENT_BY_OTHER_MEANS', 'CANCELED_RECURRING_BILLING', 'OTHER',
  ]);
  const status = enumValue(value.status, [
    'OPEN', 'WAITING_FOR_SELLER_RESPONSE', 'WAITING_FOR_BUYER_RESPONSE',
    'UNDER_REVIEW', 'RESOLVED', 'CLOSED', 'UNKNOWN',
  ]);
  const stage = enumValue(value.dispute_life_cycle_stage, ['INQUIRY', 'CHARGEBACK', 'PRE_ARBITRATION', 'ARBITRATION', 'UNKNOWN']);
  const dueAt = timestamp(value.seller_response_due_date);
  const dueState = enumValue(value.due_state, ['OPEN', 'EXPIRED']);
  const actions = uniqueArray(value.available_actions, 0, 20).map((action) => boundedText(action, 128, /^[A-Z][A-Z0-9_]{0,127}$/u));
  if (new Set(actions).size !== actions.length) invalid();
  const requirements = uniqueArray(value.requirements, 1, 20).map(validateRequirement);
  if (new Set(requirements.map((item) => item.requirement_ref)).size !== requirements.length) invalid();
  const overallState = enumValue(value.overall_state, [
    'CASE_NOT_ACTIONABLE', 'MANUAL_REVIEW', 'DUE_DATE_EXPIRED',
    'ACTION_NOT_AVAILABLE', 'NEEDS_INPUT', 'READY_FOR_LOCAL_REVIEW',
  ]);
  exactBoolean(value.human_review_required, true);
  enumValue(value.provider_submission, ['NOT_PERFORMED']);
  return {
    schema_version: 1,
    snapshot_class: value.snapshot_class,
    reason,
    status,
    dispute_life_cycle_stage: stage,
    seller_response_due_date: dueAt,
    due_state: dueState,
    available_actions: actions,
    requirements,
    overall_state: overallState,
    human_review_required: true,
    provider_submission: 'NOT_PERFORMED',
  };
}

function validateRestrictedSummary(value) {
  exactObject(value, [
    'schema_version', 'profile', 'data_class', 'custody', 'persistent_storage',
    'production_pii_vault', 'proof_record_count', 'attachment_count',
    'content_returned', 'provider_submission',
  ]);
  if (value.schema_version !== 1) invalid();
  enumValue(value.profile, ['RESTRICTED_ORIGINAL_METADATA_V1']);
  enumValue(value.data_class, ['SYNTHETIC_RESTRICTED_EVIDENCE']);
  enumValue(value.custody, ['SESSION_MEMORY_ONLY']);
  enumValue(value.persistent_storage, ['NOT_IMPLEMENTED']);
  enumValue(value.production_pii_vault, ['NOT_IMPLEMENTED']);
  const proofRecordCount = boundedInteger(value.proof_record_count, 0, 128);
  const attachmentCount = boundedInteger(value.attachment_count, 0, 20);
  exactBoolean(value.content_returned, false);
  enumValue(value.provider_submission, ['NOT_PERFORMED']);
  return {
    schema_version: 1,
    profile: value.profile,
    data_class: value.data_class,
    custody: value.custody,
    persistent_storage: value.persistent_storage,
    production_pii_vault: value.production_pii_vault,
    proof_record_count: proofRecordCount,
    attachment_count: attachmentCount,
    content_returned: false,
    provider_submission: 'NOT_PERFORMED',
  };
}

function validateIdentity(value) {
  exactObject(value, ['method', 'fields', 'tokens', 'synthetic']);
  enumValue(value.method, ['HMAC-SHA256 pseudonymization']);
  if (JSON.stringify(value.fields) !== JSON.stringify(['name', 'address', 'email'])) invalid();
  exactObject(value.tokens, ['name_token', 'address_token', 'email_token']);
  const tokens = Object.values(value.tokens).map((token) => boundedText(token, 256, /^[A-Za-z0-9_-]+$/u));
  exactBoolean(value.synthetic, true);
  return tokens;
}

function validateCitation(value, knownForbidden) {
  exactObject(value, CITATION_KEYS);
  return {
    chunk_id: boundedText(value.chunk_id, 128, /^[A-Z0-9-]+$/u),
    source_id: boundedText(value.source_id, 128, /^[A-Z0-9-]+$/u),
    title: exportText(value.title, 512, knownForbidden),
    url: officialUrl(value.url),
    locator: exportText(value.locator, 1000, knownForbidden),
    material_type: enumValue(value.material_type, ['official_api_reference', 'official_policy']),
    jurisdiction: enumValue(value.jurisdiction, ['US']),
    text_sha256: boundedText(value.text_sha256, 64, /^[a-f0-9]{64}$/u),
  };
}

function validateScenarioMatch(value, knownForbidden) {
  exactObject(value, [
    'schema_version', 'source', 'status', 'intake_status', 'provenance', 'evaluation_scope',
    'required_human_review', 'operational_authority', 'engine_execution',
    'current_policy_applicability', 'real_case_evidence', 'scenario',
  ]);
  if (value.schema_version !== 1) invalid();
  enumValue(value.source, ['local_synthetic_scenario_matcher']);
  enumValue(value.status, ['synthetic_scenarios_found']);
  enumValue(value.intake_status, ['ready_for_local_rules', 'manual_review']);
  enumValue(value.provenance, ['AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES']);
  enumValue(value.evaluation_scope, ['AUTHORED_SYNTHETIC_DEMO_ONLY']);
  exactBoolean(value.required_human_review, true);
  enumValue(value.operational_authority, ['REFERENCE_ONLY_NO_ACTION_AUTHORIZATION']);
  enumValue(value.engine_execution, ['NOT_RUN']);
  enumValue(value.current_policy_applicability, ['NOT_ESTABLISHED']);
  enumValue(value.real_case_evidence, ['NOT_PROVIDED']);
  const scenario = exactObject(value.scenario, [
    'scenario_id', 'title', 'theme', 'jurisdiction', 'evidence_class', 'expected_route',
    'final_authority', 'limitations', 'citations',
  ]);
  enumValue(scenario.scenario_id, ['US-DEMO-DISPUTE-EVIDENCE']);
  enumValue(scenario.title, ['INR or counterfeit evidence organization']);
  enumValue(scenario.theme, ['dispute_mediation']);
  enumValue(scenario.jurisdiction, ['US']);
  enumValue(scenario.evidence_class, ['SYNTHETIC_DEMO_SCENARIO']);
  enumValue(scenario.expected_route, ['PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW']);
  enumValue(scenario.final_authority, ['PAYPAL_OR_EXTERNAL_ISSUER']);
  const limitations = uniqueArray(scenario.limitations, 3, 3).map((item) => exportText(item, 256, knownForbidden));
  if (JSON.stringify(limitations) !== JSON.stringify([
    'No automatic submission', 'No outcome prediction', 'Photos only when relevant or requested',
  ])) invalid();
  const citations = uniqueArray(scenario.citations, 1, 20).map((citation) => validateCitation(citation, knownForbidden));
  if (new Set(citations.map((item) => item.chunk_id)).size !== citations.length) invalid();
  return {
    schema_version: 1,
    source: value.source,
    provenance: value.provenance,
    evaluation_scope: value.evaluation_scope,
    current_policy_applicability: value.current_policy_applicability,
    real_case_evidence: value.real_case_evidence,
    scenario: {
      scenario_id: scenario.scenario_id,
      title: scenario.title,
      jurisdiction: scenario.jurisdiction,
      evidence_class: scenario.evidence_class,
      expected_route: scenario.expected_route,
      final_authority: scenario.final_authority,
      limitations,
      citations,
    },
  };
}

function validateDocument(value, knownForbidden) {
  exactObject(value, [
    'export_profile', 'redacted_text', 'replacement_count', 'counts', 'types', 'method',
    'limited_detection', 'manual_review_required', 'source', 'reversibility', 'limitations',
  ]);
  try {
    const exported = buildPseudonymizedEvidenceExport(value);
    const withoutPseudonyms = exported.redacted_text.replace(/\[[A-Z][A-Z0-9_]{0,31}_[a-f0-9]{64}\]/gu, '[PSEUDONYM]');
    exportText(withoutPseudonyms, 32768, knownForbidden);
    for (const limitation of exported.limitations) exportText(limitation, 1000, knownForbidden);
    return exported;
  } catch {
    invalid();
  }
}

function validateDraft(draft) {
  exactObjectWithOptional(draft, TOP_LEVEL_KEYS, OPTIONAL_TOP_LEVEL_KEYS);
  const draftDigest = boundedText(draft.draft_digest, 64, /^[a-f0-9]{64}$/u);
  const identityTokens = validateIdentity(draft.identity_redaction);
  const knownForbidden = [draftDigest, ...identityTokens];
  const status = enumValue(draft.status, ['manual_review', 'review_evidence']);
  const evidence = validateEvidence(draft.evidence);
  const reviewReasons = uniqueArray(draft.review_reasons, 0, 20).map((item) => {
    const reason = boundedText(item, 128, /^[a-z][a-z0-9_]{0,127}$/u);
    return exportText(reason, 128, knownForbidden);
  });
  if (new Set(reviewReasons).size !== reviewReasons.length) invalid();
  const recommendation = exportText(draft.recommendation, 2000, knownForbidden);
  const limitations = uniqueArray(draft.limitations, 1, 20).map((item) => exportText(item, 1000, knownForbidden));
  const policyVersion = exportText(
    boundedText(draft.policy_version, 128, /^[A-Za-z0-9._:-]+$/u),
    128,
    knownForbidden,
  );
  if (policyVersion !== MANIFEST_POLICY_VERSION) invalid();
  exactBoolean(draft.advisory_only, true);
  enumValue(draft.source, ['synthetic']);
  const routing = validateRouting(draft.routing);
  const restrictedOriginalSummary = validateRestrictedSummary(draft.restricted_original_summary);
  const scenario = validateScenarioMatch(draft.scenario_match, knownForbidden);
  const pseudonymizedEvidence = validateDocument(draft.document_redaction, knownForbidden);
  return {
    status,
    evidence,
    reviewReasons,
    recommendation,
    limitations,
    policyVersion,
    routing,
    restrictedOriginalSummary,
    scenario,
    pseudonymizedEvidence,
  };
}

function canonicalJsonValue(value) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number') {
    if (!Number.isFinite(value) || !Number.isInteger(value) || value < 0 || Object.is(value, -0)) invalid();
    return value;
  }
  if (Array.isArray(value)) return value.map((item) => canonicalJsonValue(item));
  plainObject(value);
  const result = {};
  for (const key of Object.keys(value).sort()) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') invalid();
    result[key] = canonicalJsonValue(value[key]);
  }
  return result;
}

function jsonBytes(value) {
  return encoder.encode(`${JSON.stringify(canonicalJsonValue(value), null, 2)}\n`);
}

function verifyPayloadDeclarations(files) {
  const byName = new Map(files.map((file) => [file.name, file.bytes]));
  let manifest;
  try {
    manifest = JSON.parse(decoder.decode(byName.get('manifest.json')));
  } catch {
    invalid();
  }
  const expectedNames = FIXED_FILES.filter((name) => name !== 'manifest.json');
  if (!Array.isArray(manifest.entries) || manifest.entries.length !== expectedNames.length) invalid();
  for (let index = 0; index < expectedNames.length; index += 1) {
    const name = expectedNames[index];
    const bytes = byName.get(name);
    const declaration = manifest.entries[index];
    exactObject(declaration, ['path', 'media_type', 'byte_length', 'crc32', 'sha256']);
    if (
      declaration.path !== name
      || declaration.media_type !== MEDIA_TYPES[name]
      || declaration.byte_length !== bytes.length
      || declaration.crc32 !== crc32(bytes).toString(16).padStart(8, '0')
      || declaration.sha256 !== sha256Hex(bytes)
    ) invalid();
  }
}

function buildFiles(draft) {
  const value = validateDraft(draft);
  const readme = [
    'PayGuard AI — Internal Review ZIP',
    '',
    'Classification: INTERNAL_REVIEW_ONLY',
    'Authority: Advisory only. Human review is required.',
    'Provider submission: NOT_PERFORMED',
    'Dispute decision: NOT_MADE',
    '',
    'Internal review package — synthetic, pseudonymized, and advisory only. This archive contains a local projection of a synthetic provider-response requirement, public-reference citations, and a pseudonymized review document. It does not contain original PayPal case data or original evidence attachment bytes. `STRUCTURALLY_PRESENT` means only that required fields and references exist in the local synthetic record; it does not establish authenticity, evidentiary sufficiency, PayPal eligibility, official completeness, or a likely outcome. PayPal or the external issuer remains the final authority. No evidence was submitted to PayPal.',
    '',
    'This archive is not a PayPal-supported attachment and is not complete official evidence.',
    'It contains no restricted originals, raw attachments, raw identifiers, restricted proof values, or attachment bytes.',
    'No provider submission was performed and no dispute verdict was made. Human review is required.',
    '',
    'Review every file before using it outside this local synthetic demo.',
  ].join('\n') + '\n';
  const requirements = {
    schema_version: 'payguard.internal_review_requirements.v1',
    status: value.status,
    policy_version: value.policyVersion,
    recommendation: value.recommendation,
    review_flags: value.reviewReasons,
    routing: value.routing,
    restricted_original_summary: value.restrictedOriginalSummary,
    limitations: value.limitations,
    authority: { ...AUTHORITY },
  };
  const timeline = {
    schema_version: 'payguard.internal_review_timeline.v1',
    timeline: value.evidence,
    authority: { ...AUTHORITY },
  };
  const publicSources = {
    schema_version: 'payguard.internal_review_public_sources.v1',
    ...value.scenario,
    authority: { ...AUTHORITY },
  };
  const payloads = new Map([
    ['README.txt', encoder.encode(readme)],
    ['requirements.json', jsonBytes(requirements)],
    ['timeline.json', jsonBytes(timeline)],
    ['public-sources.json', jsonBytes(publicSources)],
    ['pseudonymized-evidence.json', jsonBytes(value.pseudonymizedEvidence)],
  ]);
  const entries = [...payloads].map(([path, bytes]) => ({
    path,
    media_type: MEDIA_TYPES[path],
    byte_length: bytes.length,
    crc32: crc32(bytes).toString(16).padStart(8, '0'),
    sha256: sha256Hex(bytes),
  }));
  const manifest = {
    schema_version: 'payguard.internal_review_zip_manifest.v1',
    export_profile: 'INTERNAL_REVIEW_ZIP_V1',
    evidence_class: 'SYNTHETIC_INTERNAL_REVIEW_PACKAGE',
    status: MANIFEST_STATUS,
    policy_version: MANIFEST_POLICY_VERSION,
    source: 'synthetic',
    entries,
    integrity: {
      zip_method: 'STORE',
      entry_crc32: true,
      payload_sha256: true,
      manifest_self_hash: 'NOT_EMBEDDED',
      digital_signature: 'NOT_PROVIDED',
    },
    limitations: [...MANIFEST_LIMITATIONS],
    excluded_data_classes: [...EXCLUDED_DATA_CLASSES],
    authority: { ...AUTHORITY },
  };
  const contents = new Map([...payloads, ['manifest.json', jsonBytes(manifest)]]);
  if (contents.size !== FIXED_FILES.length || FIXED_FILES.some((name) => !contents.has(name))) invalid();
  let total = 0;
  const files = FIXED_FILES.map((name) => {
    const bytes = contents.get(name);
    if (!(bytes instanceof Uint8Array) || bytes.length === 0 || bytes.length > MAX_FILE_BYTES) invalid();
    total += bytes.length;
    return { name, bytes };
  });
  if (total > MAX_ARCHIVE_BYTES - 4096) invalid();
  verifyPayloadDeclarations(files);
  return files;
}

const crcTable = (() => {
  const table = new Uint32Array(256);
  for (let index = 0; index < table.length; index += 1) {
    let current = index;
    for (let bit = 0; bit < 8; bit += 1) current = (current & 1) ? (0xedb88320 ^ (current >>> 1)) : (current >>> 1);
    table[index] = current >>> 0;
  }
  return table;
})();

function crc32(bytes) {
  let current = 0xffffffff;
  for (const byte of bytes) current = crcTable[(current ^ byte) & 0xff] ^ (current >>> 8);
  return (current ^ 0xffffffff) >>> 0;
}

function rotateRight(value, count) {
  return (value >>> count) | (value << (32 - count));
}

function sha256Hex(bytes) {
  if (!(bytes instanceof Uint8Array)) invalid();
  const paddedLength = Math.ceil((bytes.length + 9) / 64) * 64;
  const padded = new Uint8Array(paddedLength);
  padded.set(bytes);
  padded[bytes.length] = 0x80;
  const bitLength = bytes.length * 8;
  const paddedView = new DataView(padded.buffer);
  paddedView.setUint32(paddedLength - 8, Math.floor(bitLength / 0x100000000), false);
  paddedView.setUint32(paddedLength - 4, bitLength >>> 0, false);
  const hash = new Uint32Array([
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
  ]);
  const words = new Uint32Array(64);
  for (let offset = 0; offset < paddedLength; offset += 64) {
    for (let index = 0; index < 16; index += 1) words[index] = paddedView.getUint32(offset + index * 4, false);
    for (let index = 16; index < 64; index += 1) {
      const previous = words[index - 15];
      const secondPrevious = words[index - 2];
      const sigma0 = rotateRight(previous, 7) ^ rotateRight(previous, 18) ^ (previous >>> 3);
      const sigma1 = rotateRight(secondPrevious, 17) ^ rotateRight(secondPrevious, 19) ^ (secondPrevious >>> 10);
      words[index] = (words[index - 16] + sigma0 + words[index - 7] + sigma1) >>> 0;
    }
    let [a, b, c, d, e, f, g, h] = hash;
    for (let index = 0; index < 64; index += 1) {
      const upperSigma1 = rotateRight(e, 6) ^ rotateRight(e, 11) ^ rotateRight(e, 25);
      const choice = (e & f) ^ (~e & g);
      const temporary1 = (h + upperSigma1 + choice + SHA256_CONSTANTS[index] + words[index]) >>> 0;
      const upperSigma0 = rotateRight(a, 2) ^ rotateRight(a, 13) ^ rotateRight(a, 22);
      const majority = (a & b) ^ (a & c) ^ (b & c);
      const temporary2 = (upperSigma0 + majority) >>> 0;
      h = g;
      g = f;
      f = e;
      e = (d + temporary1) >>> 0;
      d = c;
      c = b;
      b = a;
      a = (temporary1 + temporary2) >>> 0;
    }
    hash[0] = (hash[0] + a) >>> 0;
    hash[1] = (hash[1] + b) >>> 0;
    hash[2] = (hash[2] + c) >>> 0;
    hash[3] = (hash[3] + d) >>> 0;
    hash[4] = (hash[4] + e) >>> 0;
    hash[5] = (hash[5] + f) >>> 0;
    hash[6] = (hash[6] + g) >>> 0;
    hash[7] = (hash[7] + h) >>> 0;
  }
  return [...hash].map((word) => word.toString(16).padStart(8, '0')).join('');
}

function littleEndian(size, writes) {
  const bytes = new Uint8Array(size);
  const view = new DataView(bytes.buffer);
  for (const [width, offset, value] of writes) {
    if (width === 2) view.setUint16(offset, value, true);
    else view.setUint32(offset, value, true);
  }
  return bytes;
}

function concat(parts) {
  const length = parts.reduce((sum, part) => sum + part.length, 0);
  if (length > MAX_ARCHIVE_BYTES) invalid();
  const result = new Uint8Array(length);
  let offset = 0;
  for (const part of parts) {
    result.set(part, offset);
    offset += part.length;
  }
  return result;
}

export function buildInternalReviewFiles(draft) {
  return buildFiles(draft).map(({ name, bytes }) => ({ name, bytes: bytes.slice() }));
}

export function buildInternalReviewZip(draft) {
  const files = buildFiles(draft);
  const localParts = [];
  const centralParts = [];
  let localOffset = 0;
  for (const file of files) {
    const name = encoder.encode(file.name);
    const checksum = crc32(file.bytes);
    const localHeader = littleEndian(30, [
      [4, 0, 0x04034b50], [2, 4, 20], [2, 6, 0x0800], [2, 8, 0], [2, 10, 0], [2, 12, 0x21],
      [4, 14, checksum], [4, 18, file.bytes.length], [4, 22, file.bytes.length],
      [2, 26, name.length], [2, 28, 0],
    ]);
    localParts.push(localHeader, name, file.bytes);
    const centralHeader = littleEndian(46, [
      [4, 0, 0x02014b50], [2, 4, 0x0314], [2, 6, 20], [2, 8, 0x0800], [2, 10, 0],
      [2, 12, 0], [2, 14, 0x21], [4, 16, checksum], [4, 20, file.bytes.length],
      [4, 24, file.bytes.length], [2, 28, name.length], [2, 30, 0], [2, 32, 0],
      [2, 34, 0], [2, 36, 0], [4, 38, 0x81a40000], [4, 42, localOffset],
    ]);
    centralParts.push(centralHeader, name);
    localOffset += localHeader.length + name.length + file.bytes.length;
  }
  const central = concat(centralParts);
  const end = littleEndian(22, [
    [4, 0, 0x06054b50], [2, 4, 0], [2, 6, 0], [2, 8, files.length],
    [2, 10, files.length], [4, 12, central.length], [4, 16, localOffset], [2, 20, 0],
  ]);
  const archive = concat([...localParts, central, end]);
  validateInternalReviewZip(archive);
  return archive;
}

function equalBytes(left, right) {
  if (!(left instanceof Uint8Array) || !(right instanceof Uint8Array) || left.length !== right.length) return false;
  for (let index = 0; index < left.length; index += 1) if (left[index] !== right[index]) return false;
  return true;
}

function validateInternalReviewZipCore(bytes) {
  if (!(bytes instanceof Uint8Array) || bytes.length < 22 || bytes.length > MAX_ARCHIVE_BYTES) invalid();
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const endOffset = bytes.length - 22;
  if (
    view.getUint32(endOffset, true) !== 0x06054b50
    || view.getUint16(endOffset + 4, true) !== 0
    || view.getUint16(endOffset + 6, true) !== 0
    || view.getUint16(endOffset + 8, true) !== FIXED_FILES.length
    || view.getUint16(endOffset + 10, true) !== FIXED_FILES.length
    || view.getUint16(endOffset + 20, true) !== 0
  ) invalid();
  const centralSize = view.getUint32(endOffset + 12, true);
  const centralOffset = view.getUint32(endOffset + 16, true);
  if (centralOffset < 1 || centralSize < 1 || centralOffset + centralSize !== endOffset) invalid();

  const extracted = new Map();
  let centralCursor = centralOffset;
  let expectedLocalOffset = 0;
  for (let index = 0; index < FIXED_FILES.length; index += 1) {
    if (centralCursor + 46 > endOffset || view.getUint32(centralCursor, true) !== 0x02014b50) invalid();
    const creatorVersion = view.getUint16(centralCursor + 4, true);
    const extractVersion = view.getUint16(centralCursor + 6, true);
    const flags = view.getUint16(centralCursor + 8, true);
    const method = view.getUint16(centralCursor + 10, true);
    const time = view.getUint16(centralCursor + 12, true);
    const date = view.getUint16(centralCursor + 14, true);
    const checksum = view.getUint32(centralCursor + 16, true);
    const compressedSize = view.getUint32(centralCursor + 20, true);
    const uncompressedSize = view.getUint32(centralCursor + 24, true);
    const nameLength = view.getUint16(centralCursor + 28, true);
    const extraLength = view.getUint16(centralCursor + 30, true);
    const commentLength = view.getUint16(centralCursor + 32, true);
    const diskStart = view.getUint16(centralCursor + 34, true);
    const internalAttributes = view.getUint16(centralCursor + 36, true);
    const externalAttributes = view.getUint32(centralCursor + 38, true);
    const localOffset = view.getUint32(centralCursor + 42, true);
    const centralEnd = centralCursor + 46 + nameLength + extraLength + commentLength;
    if (
      creatorVersion !== 0x0314 || extractVersion !== 20 || flags !== 0x0800 || method !== 0
      || time !== 0 || date !== 0x21 || compressedSize !== uncompressedSize
      || nameLength === 0 || extraLength !== 0 || commentLength !== 0 || diskStart !== 0
      || internalAttributes !== 0 || externalAttributes !== 0x81a40000
      || localOffset !== expectedLocalOffset || centralEnd > endOffset || uncompressedSize > MAX_FILE_BYTES
    ) invalid();
    const centralNameBytes = bytes.subarray(centralCursor + 46, centralCursor + 46 + nameLength);
    const expectedName = FIXED_FILES[index];
    if (decoder.decode(centralNameBytes) !== expectedName || !equalBytes(centralNameBytes, encoder.encode(expectedName))) invalid();

    if (localOffset + 30 > centralOffset || view.getUint32(localOffset, true) !== 0x04034b50) invalid();
    const localNameLength = view.getUint16(localOffset + 26, true);
    const localExtraLength = view.getUint16(localOffset + 28, true);
    if (
      view.getUint16(localOffset + 4, true) !== 20
      || view.getUint16(localOffset + 6, true) !== flags
      || view.getUint16(localOffset + 8, true) !== method
      || view.getUint16(localOffset + 10, true) !== time
      || view.getUint16(localOffset + 12, true) !== date
      || view.getUint32(localOffset + 14, true) !== checksum
      || view.getUint32(localOffset + 18, true) !== compressedSize
      || view.getUint32(localOffset + 22, true) !== uncompressedSize
      || localNameLength !== nameLength || localExtraLength !== 0
    ) invalid();
    const localNameStart = localOffset + 30;
    const dataStart = localNameStart + localNameLength;
    const dataEnd = dataStart + uncompressedSize;
    if (dataEnd > centralOffset) invalid();
    const localNameBytes = bytes.subarray(localNameStart, dataStart);
    if (!equalBytes(localNameBytes, centralNameBytes)) invalid();
    const content = bytes.slice(dataStart, dataEnd);
    if (crc32(content) !== checksum) invalid();
    extracted.set(expectedName, content);
    expectedLocalOffset = dataEnd;
    centralCursor = centralEnd;
  }
  if (centralCursor !== endOffset || expectedLocalOffset !== centralOffset || extracted.size !== FIXED_FILES.length) invalid();

  for (const name of FIXED_FILES.filter((item) => item.endsWith('.json'))) {
    const raw = extracted.get(name);
    let parsed;
    try {
      parsed = JSON.parse(decoder.decode(raw));
    } catch {
      invalid();
    }
    if (!equalBytes(raw, jsonBytes(parsed))) invalid();
  }

  let manifest;
  try {
    manifest = JSON.parse(decoder.decode(extracted.get('manifest.json')));
  } catch {
    invalid();
  }
  exactObject(manifest, [
    'schema_version', 'export_profile', 'evidence_class', 'status', 'policy_version',
    'source', 'entries', 'integrity', 'limitations', 'excluded_data_classes', 'authority',
  ]);
  if (
    manifest.schema_version !== 'payguard.internal_review_zip_manifest.v1'
    || manifest.export_profile !== 'INTERNAL_REVIEW_ZIP_V1'
    || manifest.evidence_class !== 'SYNTHETIC_INTERNAL_REVIEW_PACKAGE'
    || manifest.status !== MANIFEST_STATUS
    || manifest.policy_version !== MANIFEST_POLICY_VERSION
    || manifest.source !== 'synthetic'
  ) invalid();
  exactObject(manifest.integrity, [
    'zip_method', 'entry_crc32', 'payload_sha256', 'manifest_self_hash', 'digital_signature',
  ]);
  if (
    manifest.integrity.zip_method !== 'STORE'
    || manifest.integrity.entry_crc32 !== true
    || manifest.integrity.payload_sha256 !== true
    || manifest.integrity.manifest_self_hash !== 'NOT_EMBEDDED'
    || manifest.integrity.digital_signature !== 'NOT_PROVIDED'
  ) invalid();
  exactObject(manifest.authority, Object.keys(AUTHORITY));
  for (const [key, expected] of Object.entries(AUTHORITY)) {
    if (manifest.authority[key] !== expected) invalid();
  }
  if (
    JSON.stringify(manifest.limitations) !== JSON.stringify(MANIFEST_LIMITATIONS)
    || JSON.stringify(manifest.excluded_data_classes) !== JSON.stringify(EXCLUDED_DATA_CLASSES)
  ) invalid();
  const payloadNames = FIXED_FILES.filter((name) => name !== 'manifest.json');
  if (!Array.isArray(manifest.entries) || manifest.entries.length !== payloadNames.length) invalid();
  if (new Set(manifest.entries.map((entry) => plainObject(entry).path)).size !== payloadNames.length) invalid();
  for (let index = 0; index < payloadNames.length; index += 1) {
    const name = payloadNames[index];
    const content = extracted.get(name);
    const declaration = manifest.entries[index];
    exactObject(declaration, ['path', 'media_type', 'byte_length', 'crc32', 'sha256']);
    if (
      declaration.path !== name
      || declaration.media_type !== MEDIA_TYPES[name]
      || declaration.byte_length !== content.length
      || declaration.crc32 !== crc32(content).toString(16).padStart(8, '0')
      || declaration.sha256 !== sha256Hex(content)
    ) invalid();
  }
  return true;
}

export function validateInternalReviewZip(bytes) {
  try {
    return validateInternalReviewZipCore(bytes);
  } catch {
    invalid();
  }
}

export function downloadInternalReviewZip(draft) {
  if (typeof document === 'undefined' || typeof URL === 'undefined' || typeof Blob === 'undefined') invalid();
  const bytes = buildInternalReviewZip(draft);
  validateInternalReviewZip(bytes);
  const blob = new Blob([bytes], { type: 'application/zip' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  try {
    anchor.href = url;
    anchor.download = 'payguard-internal-review.zip';
    document.body.appendChild(anchor);
    anchor.click();
  } finally {
    anchor.remove();
    URL.revokeObjectURL(url);
  }
}
