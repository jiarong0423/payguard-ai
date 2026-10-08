import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  buildInternalReviewFiles,
  buildInternalReviewZip,
  validateInternalReviewZip,
} from '../frontend/src/reviewZip.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const clone = (value) => structuredClone(value);
const fixedNames = [
  'README.txt', 'manifest.json', 'requirements.json', 'timeline.json',
  'public-sources.json', 'pseudonymized-evidence.json',
];

const validDraft = {
  case_ref: 'case-ref-001',
  status: 'review_evidence',
  evidence: {
    reason: 'INR',
    opened_at: '2026-10-08T08:00:00Z',
    order_created_at: '2026-10-05T08:00:00Z',
    carrier_status: 'delivered',
    delivered_at: '2026-10-07T08:00:00Z',
    evidence_source: 'synthetic',
  },
  review_reasons: [],
  recommendation: 'Review the synthetic timeline and provider request before any external action.',
  limitations: ['Synthetic demo facts only.', 'Provider verification is not performed.'],
  policy_version: 'payguard.demo.v1',
  advisory_only: true,
  source: 'synthetic',
  routing: {
    schema_version: 1,
    snapshot_class: 'SYNTHETIC_PROVIDER_FIXTURE',
    reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED',
    status: 'WAITING_FOR_SELLER_RESPONSE',
    dispute_life_cycle_stage: 'INQUIRY',
    seller_response_due_date: '2026-10-10T08:00:00Z',
    due_state: 'OPEN',
    available_actions: ['PROVIDE_EVIDENCE'],
    requirements: [{
      request_id: 'requirement-001',
      provider_evidence_type: 'PROOF_OF_FULFILLMENT',
      evidence_type: 'FULFILLMENT',
      source: 'REQUESTED_FROM_SELLER',
      mandatory: true,
      action: 'PROVIDE_EVIDENCE',
      requirement_state: 'STRUCTURALLY_PRESENT',
      proof_count: 1,
      accepted_attachment_count: 1,
    }],
    overall_state: 'READY_FOR_LOCAL_REVIEW',
    human_review_required: true,
    provider_submission: 'NOT_PERFORMED',
  },
  restricted_original_summary: {
    schema_version: 1,
    profile: 'RESTRICTED_ORIGINAL_METADATA_V1',
    data_class: 'SYNTHETIC_RESTRICTED_EVIDENCE',
    custody: 'SESSION_MEMORY_ONLY',
    persistent_storage: 'NOT_IMPLEMENTED',
    production_pii_vault: 'NOT_IMPLEMENTED',
    proof_record_count: 1,
    attachment_count: 1,
    content_returned: false,
    provider_submission: 'NOT_PERFORMED',
  },
  scenario_match: {
    schema_version: 1,
    source: 'local_synthetic_scenario_matcher',
    status: 'synthetic_scenarios_found',
    intake_status: 'ready_for_local_rules',
    provenance: 'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES',
    evaluation_scope: 'AUTHORED_SYNTHETIC_DEMO_ONLY',
    required_human_review: true,
    operational_authority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
    engine_execution: 'NOT_RUN',
    current_policy_applicability: 'NOT_ESTABLISHED',
    real_case_evidence: 'NOT_PROVIDED',
    scenario: {
      scenario_id: 'US-DEMO-DISPUTE-EVIDENCE',
      title: 'INR or counterfeit evidence organization',
      theme: 'dispute_mediation',
      jurisdiction: 'US',
      evidence_class: 'SYNTHETIC_DEMO_SCENARIO',
      expected_route: 'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
      final_authority: 'PAYPAL_OR_EXTERNAL_ISSUER',
      limitations: ['No automatic submission', 'No outcome prediction', 'Photos only when relevant or requested'],
      citations: [{
        chunk_id: 'PP-DISPUTES-OVERVIEW-AUTHORITY',
        source_id: 'PP-DISPUTES-OVERVIEW',
        title: 'PayPal disputes overview',
        url: 'https://developer.paypal.com/disputes/overview',
        locator: 'Dispute lifecycle and external disputes',
        material_type: 'official_api_reference',
        jurisdiction: 'US',
        text_sha256: '18f6e233c45b96a1a8de1eda30987e234d5a6197c78829af5e5782f9832af91e',
      }],
    },
  },
  draft_digest: 'a'.repeat(64),
  identity_redaction: {
    method: 'HMAC-SHA256 pseudonymization',
    fields: ['name', 'address', 'email'],
    tokens: {
      name_token: 'PRIVATE_CASE_ID_DEMO_CASE_001',
      address_token: 'PRIVATE_ORDER_ID_DEMO_ORDER_001',
      email_token: 'PRIVATE_REQUEST_ID_REQUEST_FULFILLMENT_001',
    },
    synthetic: true,
  },
  document_redaction: {
    export_profile: 'INTERNAL_REVIEW_ONLY_V1',
    redacted_text: 'Order [MANUAL_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa] belongs to [NAME_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb].',
    replacement_count: 2,
    counts: { manual: 1, name: 1 },
    types: ['manual', 'name'],
    method: 'HMAC-SHA256 document pseudonymization v1',
    limited_detection: true,
    manual_review_required: true,
    source: 'synthetic',
    reversibility: false,
    limitations: ['Manual review is required.'],
  },
};

function crc32(bytes) {
  let current = 0xffffffff;
  for (const byte of bytes) {
    current ^= byte;
    for (let bit = 0; bit < 8; bit += 1) current = (current & 1) ? (0xedb88320 ^ (current >>> 1)) : (current >>> 1);
  }
  return (current ^ 0xffffffff) >>> 0;
}

function parseZip(bytes) {
  assert.ok(bytes instanceof Uint8Array);
  assert.ok(bytes.length > 22 && bytes.length <= 262144);
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const endOffset = bytes.length - 22;
  assert.equal(view.getUint32(endOffset, true), 0x06054b50);
  assert.equal(view.getUint16(endOffset + 4, true), 0);
  assert.equal(view.getUint16(endOffset + 6, true), 0);
  const entries = view.getUint16(endOffset + 8, true);
  assert.equal(entries, view.getUint16(endOffset + 10, true));
  const centralSize = view.getUint32(endOffset + 12, true);
  const centralOffset = view.getUint32(endOffset + 16, true);
  assert.equal(centralOffset + centralSize, endOffset);
  assert.equal(view.getUint16(endOffset + 20, true), 0);
  const decoder = new TextDecoder();
  const files = new Map();
  let cursor = centralOffset;
  for (let index = 0; index < entries; index += 1) {
    assert.equal(view.getUint32(cursor, true), 0x02014b50);
    assert.equal(view.getUint16(cursor + 4, true), 0x0314);
    assert.equal(view.getUint16(cursor + 8, true), 0x0800);
    assert.equal(view.getUint16(cursor + 10, true), 0);
    assert.equal(view.getUint32(cursor + 38, true), 0x81a40000);
    const expectedCrc = view.getUint32(cursor + 16, true);
    const compressed = view.getUint32(cursor + 20, true);
    const uncompressed = view.getUint32(cursor + 24, true);
    assert.equal(compressed, uncompressed);
    const nameLength = view.getUint16(cursor + 28, true);
    const extraLength = view.getUint16(cursor + 30, true);
    const commentLength = view.getUint16(cursor + 32, true);
    const localOffset = view.getUint32(cursor + 42, true);
    const name = decoder.decode(bytes.subarray(cursor + 46, cursor + 46 + nameLength));
    assert.equal(view.getUint32(localOffset, true), 0x04034b50);
    assert.equal(view.getUint16(localOffset + 6, true), 0x0800);
    assert.equal(view.getUint16(localOffset + 8, true), 0);
    const localNameLength = view.getUint16(localOffset + 26, true);
    const localExtraLength = view.getUint16(localOffset + 28, true);
    const localName = decoder.decode(bytes.subarray(localOffset + 30, localOffset + 30 + localNameLength));
    assert.equal(localName, name);
    const dataStart = localOffset + 30 + localNameLength + localExtraLength;
    const content = bytes.slice(dataStart, dataStart + uncompressed);
    assert.equal(crc32(content), expectedCrc);
    assert.equal(view.getUint32(localOffset + 14, true), expectedCrc);
    assert.equal(view.getUint32(localOffset + 18, true), uncompressed);
    assert.equal(view.getUint32(localOffset + 22, true), uncompressed);
    files.set(name, content);
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  assert.equal(cursor, endOffset);
  return files;
}

function canonicalJson(value) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean' || typeof value === 'number') return value;
  if (Array.isArray(value)) return value.map(canonicalJson);
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalJson(value[key])]));
}

function canonicalJsonText(value) {
  return `${JSON.stringify(canonicalJson(value), null, 2)}\n`;
}

function findCentralEntry(bytes, wantedName) {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const endOffset = bytes.length - 22;
  let cursor = view.getUint32(endOffset + 16, true);
  const count = view.getUint16(endOffset + 8, true);
  const textDecoder = new TextDecoder('utf-8', { fatal: true });
  for (let index = 0; index < count; index += 1) {
    const nameLength = view.getUint16(cursor + 28, true);
    const extraLength = view.getUint16(cursor + 30, true);
    const commentLength = view.getUint16(cursor + 32, true);
    const name = textDecoder.decode(bytes.subarray(cursor + 46, cursor + 46 + nameLength));
    if (name === wantedName) return {
      centralOffset: cursor,
      localOffset: view.getUint32(cursor + 42, true),
      size: view.getUint32(cursor + 24, true),
    };
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  throw new Error(`entry not found: ${wantedName}`);
}

function mutateCanonicalJsonEntryAndRecomputeZipCrc(bytes, name, mutate) {
  const result = bytes.slice();
  const view = new DataView(result.buffer, result.byteOffset, result.byteLength);
  const entry = findCentralEntry(result, name);
  const localNameLength = view.getUint16(entry.localOffset + 26, true);
  const localExtraLength = view.getUint16(entry.localOffset + 28, true);
  const dataStart = entry.localOffset + 30 + localNameLength + localExtraLength;
  const currentBytes = result.slice(dataStart, dataStart + entry.size);
  const parsedValue = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(currentBytes));
  mutate(parsedValue);
  const replacement = new TextEncoder().encode(canonicalJsonText(parsedValue));
  assert.equal(replacement.length, currentBytes.length, `${name} semantic mutation must remain equal length`);
  result.set(replacement, dataStart);
  const checksum = crc32(replacement);
  view.setUint32(entry.localOffset + 14, checksum, true);
  view.setUint32(entry.centralOffset + 16, checksum, true);
  return result;
}

const first = buildInternalReviewZip(clone(validDraft));
const second = buildInternalReviewZip(clone(validDraft));
assert.deepEqual(first, second, 'ZIP bytes must be deterministic');
assert.equal(validateInternalReviewZip(first), true, 'completed archive must pass runtime validation');
const parsed = parseZip(first);
assert.deepEqual([...parsed.keys()], fixedNames);

const directFiles = buildInternalReviewFiles(clone(validDraft));
assert.deepEqual(directFiles.map((file) => file.name), fixedNames);
for (const file of directFiles) assert.deepEqual(file.bytes, parsed.get(file.name));

const decoder = new TextDecoder();
const texts = Object.fromEntries([...parsed].map(([name, bytes]) => [name, decoder.decode(bytes)]));
const manifest = JSON.parse(texts['manifest.json']);
const requirements = JSON.parse(texts['requirements.json']);
const timeline = JSON.parse(texts['timeline.json']);
const sources = JSON.parse(texts['public-sources.json']);
const pseudonymized = JSON.parse(texts['pseudonymized-evidence.json']);
for (const name of fixedNames.filter((item) => item.endsWith('.json'))) {
  assert.equal(texts[name], canonicalJsonText(JSON.parse(texts[name])), `${name} must use recursive lexicographic canonical JSON`);
}
assert.equal(manifest.export_profile, 'INTERNAL_REVIEW_ZIP_V1');
assert.equal(manifest.schema_version, 'payguard.internal_review_zip_manifest.v1');
assert.equal(manifest.evidence_class, 'SYNTHETIC_INTERNAL_REVIEW_PACKAGE');
assert.equal(manifest.status, 'INTERNAL_REVIEW_ONLY');
assert.equal(manifest.policy_version, 'payguard.demo.v1');
assert.equal(manifest.source, 'synthetic');
assert.equal(manifest.authority.provider_submission, 'NOT_PERFORMED');
assert.equal(manifest.authority.dispute_decision, 'NOT_MADE');
assert.equal(manifest.authority.human_review_required, true);
assert.equal(manifest.authority.paypal_supported_attachment, false);
assert.equal(manifest.authority.complete_official_evidence, false);
assert.equal(manifest.authority.external_action_authorized, false);
assert.deepEqual(manifest.integrity, {
  digital_signature: 'NOT_PROVIDED',
  entry_crc32: true,
  manifest_self_hash: 'NOT_EMBEDDED',
  payload_sha256: true,
  zip_method: 'STORE',
});
assert.deepEqual(manifest.limitations, [
  'INTERNAL_REVIEW_ONLY',
  'SYNTHETIC_PSEUDONYMIZED_ADVISORY',
  'INCOMPLETE_OFFICIAL_EVIDENCE',
  'NO_RESTRICTED_ORIGINALS_OR_RAW_ATTACHMENTS',
  'NO_PAYPAL_SUBMISSION_OR_DISPUTE_VERDICT',
  'HUMAN_REVIEW_REQUIRED',
]);
assert.deepEqual(manifest.excluded_data_classes, [
  'RAW_CASE_ORDER_REQUEST_IDENTIFIERS',
  'IDENTITY_SESSION_DRAFT_DIGESTS',
  'RESTRICTED_PROOF_VALUES',
  'ATTACHMENT_FILENAMES_AND_BYTES',
  'UNKNOWN_FIELDS',
]);
const payloadNames = fixedNames.filter((name) => name !== 'manifest.json');
assert.deepEqual(manifest.entries.map((entry) => entry.path), payloadNames);
for (const entry of manifest.entries) {
  const bytes = parsed.get(entry.path);
  assert.equal(entry.byte_length, bytes.length);
  assert.equal(entry.crc32, crc32(bytes).toString(16).padStart(8, '0'));
  assert.equal(entry.sha256, createHash('sha256').update(bytes).digest('hex'));
  assert.equal(entry.media_type, entry.path === 'README.txt' ? 'text/plain; charset=utf-8' : 'application/json');
}
assert.equal(requirements.routing.requirements[0].requirement_ref, 'requirement-001');
assert.equal('request_id' in requirements.routing.requirements[0], false);
assert.deepEqual(requirements.restricted_original_summary, validDraft.restricted_original_summary);
assert.equal(timeline.timeline.evidence_source, 'synthetic');
assert.equal(sources.scenario.citations[0].jurisdiction, 'US');
assert.equal(pseudonymized.export_profile, 'INTERNAL_REVIEW_ONLY_V1');
assert.match(texts['README.txt'], /not a PayPal-supported attachment/u);
assert.match(texts['README.txt'], /not complete official evidence/u);
assert.ok(texts['README.txt'].includes('Internal review package — synthetic, pseudonymized, and advisory only. This archive contains a local projection of a synthetic provider-response requirement, public-reference citations, and a pseudonymized review document. It does not contain original PayPal case data or original evidence attachment bytes. `STRUCTURALLY_PRESENT` means only that required fields and references exist in the local synthetic record; it does not establish authenticity, evidentiary sufficiency, PayPal eligibility, official completeness, or a likely outcome. PayPal or the external issuer remains the final authority. No evidence was submitted to PayPal.'));
assert.match(texts['README.txt'], /no restricted originals, raw attachments/u);
assert.match(texts['README.txt'], /No provider submission was performed and no dispute verdict was made\. Human review is required\./u);

const allText = Object.values(texts).join('\n');
for (const forbidden of [
  '"case_ref"', '"draft_digest"', '"identity_redaction"', '"session_id"', '"order_id"', '"request_id"',
  'PRIVATE_CASE_ID_DEMO_CASE_001', 'PRIVATE_ORDER_ID_DEMO_ORDER_001',
  'PRIVATE_REQUEST_ID_REQUEST_FULFILLMENT_001', '"attachment_id"', '"filename"', '"content"',
]) assert.equal(allText.includes(forbidden), false, forbidden);

const withoutCaseRef = clone(validDraft);
delete withoutCaseRef.case_ref;
assert.deepEqual(buildInternalReviewZip(withoutCaseRef), first, 'case_ref must not be required');
const changedCaseRef = clone(validDraft);
changedCaseRef.case_ref = 'RAW-PRIVATE-CASE-IDENTIFIER';
assert.deepEqual(buildInternalReviewZip(changedCaseRef), first, 'case_ref must not affect archive bytes');

const rejectedCredentialShape = ['s', 'k', '_', 'te', 'st', '_', 'secret', 'value', '123456'].join('');
const invalidMutations = [
  (value) => { value.unknown = true; },
  (value) => { value.evidence.unknown = true; },
  (value) => { value.routing.unknown = true; },
  (value) => { value.routing.requirements[0].request_id = 'request-fulfillment-001'; },
  (value) => { value.routing.requirements[0].filename = 'private.pdf'; },
  (value) => { value.scenario_match.scenario.citations[0].url = 'https://example.com/private'; },
  (value) => { value.scenario_match.scenario.citations[0].raw_text = 'unknown'; },
  (value) => { value.document_redaction.unknown = true; },
  (value) => { value.document_redaction.export_profile = 'PAYPAL_SUBMISSION'; },
  (value) => { value.document_redaction.redacted_text = 'x'.repeat(32769); },
  (value) => { value.identity_redaction.tokens.secret = 'hidden'; },
  (value) => { value.draft_digest = 'not-a-digest'; },
  (value) => { value.recommendation = 'MARKER_PRIVATE_CASE_ID_DEMO_CASE_001'; },
  (value) => { value.recommendation = 'MARKER_sk-test-secret-like-value-1234567890'; },
  (value) => { value.limitations = [`Digest ${'c'.repeat(64)}`]; },
  (value) => { value.limitations = ['Review private-evidence.pdf before use.']; },
  (value) => { value.scenario_match.scenario.citations[0].title = 'PRIVATE_ORDER_ID_DEMO_ORDER_001'; },
  (value) => { value.scenario_match.scenario.citations[0].locator = 'credential=secretvalue123456'; },
  (value) => { value.document_redaction.limitations = ['Attachment private-evidence.png']; },
  (value) => { value.document_redaction.redacted_text += ' PRIVATE_REQUEST_ID_REQUEST_001'; },
];
for (const family of ['attachment', 'file']) {
  for (const joiner of ['-', '_', ' ']) {
    for (const delimiter of [':', '=', ' ']) {
      invalidMutations.push((value) => { value.limitations = [`${family}${joiner}id${delimiter}PRIVATE123`]; });
    }
  }
}
invalidMutations.push(
  (value) => { value.scenario_match.scenario.citations[0].title = 'attachment-id=PRIVATE123'; },
  (value) => { value.scenario_match.scenario.citations[0].locator = 'file_id:PRIVATE123'; },
  (value) => { value.document_redaction.limitations = ['attachment id PRIVATE123']; },
  (value) => { value.document_redaction.redacted_text += ' file-id=PRIVATE123'; },
  (value) => { value.review_reasons = ['private_attachment_id_secret123']; },
  (value) => { value.policy_version = rejectedCredentialShape; },
  (value) => { value.policy_version = 'payguard.demo.v2'; },
);
for (const mutate of invalidMutations) {
  const value = clone(validDraft);
  mutate(value);
  assert.throws(() => buildInternalReviewZip(value), /internal_review_zip_invalid/u);
}

const corruptions = [];
const localFlagMutation = first.slice();
localFlagMutation[6] ^= 0x01;
corruptions.push(localFlagMutation);
const badEocd = first.slice();
badEocd[badEocd.length - 22] ^= 0x01;
corruptions.push(badEocd);
const badCentralFlag = first.slice();
const badCentralFlagView = new DataView(badCentralFlag.buffer, badCentralFlag.byteOffset, badCentralFlag.byteLength);
const firstCentralOffset = badCentralFlagView.getUint32(badCentralFlag.length - 6, true);
badCentralFlag[firstCentralOffset + 8] ^= 0x01;
corruptions.push(badCentralFlag);
const badMethod = first.slice();
new DataView(badMethod.buffer, badMethod.byteOffset, badMethod.byteLength).setUint16(firstCentralOffset + 10, 8, true);
corruptions.push(badMethod);
const badSize = first.slice();
const badSizeView = new DataView(badSize.buffer, badSize.byteOffset, badSize.byteLength);
badSizeView.setUint32(firstCentralOffset + 24, badSizeView.getUint32(firstCentralOffset + 24, true) + 1, true);
corruptions.push(badSize);
const badLocalOffset = first.slice();
new DataView(badLocalOffset.buffer, badLocalOffset.byteOffset, badLocalOffset.byteLength).setUint32(firstCentralOffset + 42, 1, true);
corruptions.push(badLocalOffset);
const badName = first.slice();
badName[firstCentralOffset + 46] ^= 0x01;
corruptions.push(badName);
const badExternalAttributes = first.slice();
const badExternalView = new DataView(badExternalAttributes.buffer, badExternalAttributes.byteOffset, badExternalAttributes.byteLength);
badExternalView.setUint32(firstCentralOffset + 38, 0, true);
corruptions.push(badExternalAttributes);
const payloadMutation = first.slice();
const payloadView = new DataView(payloadMutation.buffer, payloadMutation.byteOffset, payloadMutation.byteLength);
const requirementEntry = findCentralEntry(payloadMutation, 'requirements.json');
const localNameLength = payloadView.getUint16(requirementEntry.localOffset + 26, true);
const localExtraLength = payloadView.getUint16(requirementEntry.localOffset + 28, true);
const requirementStart = requirementEntry.localOffset + 30 + localNameLength + localExtraLength;
const recommendationNeedle = new TextEncoder().encode('Review the synthetic timeline');
let recommendationOffset = -1;
for (let index = 0; index <= requirementEntry.size - recommendationNeedle.length; index += 1) {
  if (recommendationNeedle.every((byte, needleIndex) => payloadMutation[requirementStart + index + needleIndex] === byte)) {
    recommendationOffset = index;
    break;
  }
}
assert.notEqual(recommendationOffset, -1);
payloadMutation[requirementStart + recommendationOffset] = 0x58;
const mutatedPayload = payloadMutation.subarray(requirementStart, requirementStart + requirementEntry.size);
const mutatedCrc = crc32(mutatedPayload);
payloadView.setUint32(requirementEntry.localOffset + 14, mutatedCrc, true);
payloadView.setUint32(requirementEntry.centralOffset + 16, mutatedCrc, true);
corruptions.push(payloadMutation);
for (const bytes of corruptions) {
  assert.throws(() => validateInternalReviewZip(bytes), /internal_review_zip_invalid/u, 'mutated completed archive must fail before download');
}

const semanticManifestMutations = [
  (value) => { value.source = 'malicious'; },
  (value) => { value.export_profile = 'EXTERNAL_REVIEW_ZIP_V1'; },
  (value) => { value.authority.provider_submission = 'DID_SUBMITTED'; },
  (value) => { value.authority.human_review_required = null; },
  (value) => { value.authority.advisory_onlx = value.authority.advisory_only; delete value.authority.advisory_only; },
  (value) => { value.statuz = value.status; delete value.status; },
  (value) => { value.excluded_data_classes[4] = 'UNKNOWN_CLASSX'; },
  (value) => { value.limitations[0] = 'EXTERNAL_REVIEW_ONLY'; },
  (value) => { value.policy_version = 'payguard.demo.v2'; },
  (value) => { value.schema_version = 'payguard.internal_review_zip_manifest.v2'; },
  (value) => { value.integrity.zip_method = 'DEFL8'; },
  (value) => { value.integrity.entry_crc33 = value.integrity.entry_crc32; delete value.integrity.entry_crc32; },
  (value) => { [value.entries[0], value.entries[1]] = [value.entries[1], value.entries[0]]; },
  (value) => { value.entries[0].path = 'READMX.txt'; },
  (value) => { value.entries[1].media_type = 'application/js0n'; },
  (value) => { value.entries[2].path = 'manifest.json'; },
];
for (const mutate of semanticManifestMutations) {
  const mutatedArchive = mutateCanonicalJsonEntryAndRecomputeZipCrc(first, 'manifest.json', mutate);
  assert.throws(() => validateInternalReviewZip(mutatedArchive), /internal_review_zip_invalid/u,
    'canonical manifest semantic mutation with recomputed ZIP CRC must fail before download');
}

const appSource = readFileSync(resolve(projectRoot, 'frontend/src/App.jsx'), 'utf8');
const reviewZipSource = readFileSync(resolve(projectRoot, 'frontend/src/reviewZip.js'), 'utf8');
const downloadFunctionOffset = reviewZipSource.indexOf('export function downloadInternalReviewZip');
const downloadValidatorOffset = reviewZipSource.indexOf('validateInternalReviewZip(bytes);', downloadFunctionOffset);
const downloadBlobOffset = reviewZipSource.indexOf('new Blob([bytes]', downloadFunctionOffset);
assert.ok(downloadFunctionOffset >= 0 && downloadValidatorOffset > downloadFunctionOffset && downloadBlobOffset > downloadValidatorOffset,
  'completed ZIP validation must run after build and before Blob creation');
for (const required of [
  "import { downloadInternalReviewZip } from './reviewZip.js';",
  'data-testid="download-internal-review-zip"',
  'data-testid="internal-review-zip-boundary"',
  'Download Internal Review ZIP',
  '<strong>INTERNAL REVIEW ONLY</strong>',
  'This synthetic, pseudonymized preparation package is not a PayPal-supported attachment.',
  'Required fields present does not prove authenticity, sufficiency, eligibility, completeness, or outcome.',
  'PayPal or the external issuer keeps final authority, and nothing was submitted.',
  'Internal review ZIP downloaded locally. It is not a PayPal evidence attachment, is not complete official evidence, and was not submitted.',
  'Internal Review ZIP creation failed. No file was downloaded or submitted to PayPal.',
  "code: 'internal_review_zip_invalid'",
]) assert.ok(appSource.includes(required), required);

console.log('frontend ZIP contract: 6 fixed entries, deterministic bytes, valid CRC32 and central directory PASS');
console.log(`frontend ZIP sample: ${first.length} bytes, sha256=${createHash('sha256').update(first).digest('hex')}`);
console.log(`frontend ZIP privacy: ${invalidMutations.length} fail-closed mutations and forbidden-field exclusion PASS`);
console.log(`frontend ZIP completed-archive gate: ${corruptions.length} binary mutations rejected before download PASS`);
console.log(`frontend ZIP manifest semantics: ${semanticManifestMutations.length} canonical CRC-recomputed mutations rejected PASS`);
console.log('frontend ZIP UI contract PASS');
