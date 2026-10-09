const EXPECTED_METHOD = 'HMAC-SHA256 document pseudonymization v1';
const ALLOWED_TYPES = new Set(['email', 'us_phone', 'id_like', 'name', 'address', 'manual', 'mixed']);

function invalid() {
  throw new Error('pseudonymized_export_invalid');
}

function strictDocument(documentRedaction) {
  if (!documentRedaction || typeof documentRedaction !== 'object' || Array.isArray(documentRedaction)) invalid();
  const {
    export_profile: exportProfile,
    redacted_text: redactedText,
    replacement_count: replacementCount,
    counts,
    types,
    method,
    limited_detection: limitedDetection,
    manual_review_required: manualReviewRequired,
    source,
    reversibility,
    limitations,
  } = documentRedaction;
  if (exportProfile !== 'INTERNAL_REVIEW_ONLY_V1') invalid();
  if (typeof redactedText !== 'string' || redactedText.length === 0 || redactedText.length > 32768) invalid();
  if (!Number.isInteger(replacementCount) || replacementCount < 0 || replacementCount > 128) invalid();
  if (!counts || typeof counts !== 'object' || Array.isArray(counts)) invalid();
  if (!Array.isArray(types) || types.length > ALLOWED_TYPES.size || !types.every((type) => ALLOWED_TYPES.has(type))) invalid();
  const countKeys = Object.keys(counts).sort();
  if (JSON.stringify(countKeys) !== JSON.stringify([...types].sort())) invalid();
  if (!countKeys.every((key) => Number.isInteger(counts[key]) && counts[key] > 0 && counts[key] <= 128)) invalid();
  if (countKeys.reduce((sum, key) => sum + counts[key], 0) !== replacementCount) invalid();
  if (method !== EXPECTED_METHOD || limitedDetection !== true || manualReviewRequired !== true || source !== 'synthetic' || reversibility !== false) invalid();
  if (!Array.isArray(limitations) || limitations.length === 0 || limitations.length > 8 || !limitations.every((item) => typeof item === 'string' && item.length > 0 && item.length <= 1000)) invalid();
  return { exportProfile, redactedText, replacementCount, counts, types, method, limitedDetection, manualReviewRequired, source, reversibility, limitations };
}

export function buildPseudonymizedEvidenceExport(documentRedaction) {
  const value = strictDocument(documentRedaction);
  return {
    schema_version: 'payguard.pseudonymized_evidence_export.v1',
    export_profile: value.exportProfile,
    evidence_class: 'SYNTHETIC_PSEUDONYMIZED_DOCUMENT',
    redacted_text: value.redactedText,
    redaction: {
      method: value.method,
      replacement_count: value.replacementCount,
      counts: { ...value.counts },
      types: [...value.types],
      limited_detection: value.limitedDetection,
      manual_review_required: value.manualReviewRequired,
      reversibility: value.reversibility,
      source: value.source,
    },
    limitations: [...value.limitations],
    authority: {
      advisory_only: true,
      provider_submission: 'NOT_PERFORMED',
      dispute_decision: 'NOT_MADE',
      human_review_required: true,
    },
  };
}

export function downloadPseudonymizedEvidence(documentRedaction) {
  if (typeof document === 'undefined' || typeof URL === 'undefined' || typeof Blob === 'undefined') invalid();
  const payload = buildPseudonymizedEvidenceExport(documentRedaction);
  const blob = new Blob([`${JSON.stringify(payload, null, 2)}\n`], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  let anchor;
  try {
    anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'payguard-pseudonymized-evidence.json';
    document.body.appendChild(anchor);
    anchor.click();
  } finally {
    try {
      anchor?.remove();
    } finally {
      URL.revokeObjectURL(url);
    }
  }
}
