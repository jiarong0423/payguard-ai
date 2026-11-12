const labels = {
  NOT_MADE: 'No decision made',
  NOT_ESTABLISHED: 'Not established',
  NOT_EVALUATED: 'Requires human review',
  NOT_RUN: 'No model used',
  NOT_PERFORMED: 'Not submitted',
  NOT_PROVIDED: 'Not provided',
  REFERENCE_ONLY_NO_ACTION_AUTHORIZATION: 'Reference only · no action authorized',
  READY_FOR_LOCAL_REVIEW: 'Ready for human review',
  CASE_NOT_ACTIONABLE: 'Case is not actionable',
  MANUAL_REVIEW: 'Needs manual review',
  DUE_DATE_EXPIRED: 'Response window expired',
  ACTION_NOT_AVAILABLE: 'Required action is unavailable',
  NEEDS_INPUT: 'More information needed',
  OPEN: 'Response window open',
  EXPIRED: 'Response window expired',
  WAITING_FOR_SELLER_RESPONSE: 'Waiting for seller response',
  WAITING_FOR_BUYER_RESPONSE: 'Waiting for buyer response',
  UNDER_REVIEW: 'Under review',
  RESOLVED: 'Resolved',
  CLOSED: 'Closed',
  UNKNOWN: 'Needs review',
  INQUIRY: 'Buyer asked a question',
  CHARGEBACK: 'Chargeback',
  PRE_ARBITRATION: 'Pre-arbitration',
  ARBITRATION: 'Arbitration',
  MERCHANDISE_OR_SERVICE_NOT_RECEIVED: 'Item or service not received',
  MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED: 'Item or service not as described',
  UNAUTHORISED: 'Reported as unauthorized',
  CREDIT_NOT_PROCESSED: 'Credit not processed',
  DUPLICATE_TRANSACTION: 'Duplicate transaction',
  INCORRECT_AMOUNT: 'Incorrect amount',
  PAYMENT_BY_OTHER_MEANS: 'Paid by another method',
  CANCELED_RECURRING_BILLING: 'Canceled recurring billing',
  OTHER: 'Other evidence',
  PAYMENT: 'Payment',
  ORDER_RECORD_CREATED: 'Order record created',
  DELIVERY: 'Digital item delivered',
  CLAIM_OPENED: 'Claim opened',
  MESSAGE: 'Message record',
  PROVIDER: 'From the dispute record',
  SELLER_PROVIDED_UNVERIFIED: 'Seller-provided, not verified',
  EMAIL: 'Email',
  PRIVATE_MESSAGE: 'Private message',
  INBOUND: 'Buyer to seller',
  OUTBOUND: 'Seller to buyer',
  PAYMENT_NOTICE: 'Payment notice',
  ORDER_DETAILS_REQUEST: 'Order details requested',
  ORDER_DETAILS_PROVIDED: 'Order details provided',
  DELIVERY_NOTICE: 'Delivery notice',
  REFUND_REQUEST: 'Refund request',
  ORDER_RECORD_ABSENT: 'No order record',
  DELIVERY_NOT_RECORDED: 'No delivery time recorded',
  DELIVERY_AFTER_CLAIM: 'Delivery time is later than the claim time',
  CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME: 'Claim time is earlier than the payment time',
  REQUESTED_FROM_SELLER: 'Requested from seller',
  PROVIDE_EVIDENCE: 'Prepare evidence',
  PROOF_OF_FULFILLMENT: 'Proof of fulfillment',
  PROOF_OF_REFUND: 'Proof of refund',
  FULFILLMENT: 'Fulfillment record',
  CONTEXT_ONLY: 'Context only',
  UNMAPPED_EVIDENCE_TYPE: 'Evidence type needs review',
  PROVIDER_REQUEST_OUTSIDE_LOCAL_MATRIX: 'Provider request needs manual review',
  STRUCTURALLY_PRESENT: 'Required fields present',
  MANDATORY_EVIDENCE_MISSING: 'Required evidence missing',
  OPTIONAL_EVIDENCE_MISSING: 'Optional evidence missing',
  INCOMPLETE_POLICY_EVIDENCE: 'Policy evidence incomplete',
  STRUCTURE_COMPATIBLE: 'Structure check passed',
  INCOMPLETE_EVIDENCE: 'Evidence incomplete',
  REJECTED: 'Needs review',
  SUMMARY_COVERAGE_INCOMPLETE: 'Source coverage is incomplete',
  CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED: 'Current policy applicability is not established',
  CURRENT_POLICY_NOT_ESTABLISHED: 'Current policy is not established',
  FUTURE_OBSERVATION: 'Source timestamp is after the comparison time',
  STALE_OBSERVATION: 'Source is outside the selected age limit',
  WITHIN_OBSERVATION_BUDGET: 'Source is within the selected age limit',
  DOCUMENT_UPDATE_DATE_MISSING: 'Document update date is missing',
  DOCUMENT_UPDATE_IN_FUTURE: 'Document update date is after the comparison time',
  UNKNOWN_EFFECTIVE_DATE: 'Effective date is not verified',
  EFFECTIVE_DATE_IN_FUTURE: 'Effective date is after the comparison time',
  API_REFERENCE_NOT_POLICY: 'PayPal developer docs do not decide whether a policy applies',
  GUIDANCE_NOT_APPLICABLE_POLICY: 'Guidance does not establish current policy applicability',
  HISTORICAL_CASE_NOT_APPLICABLE_POLICY: 'Historical case does not establish current policy applicability',
  PROCEDURE_NOT_APPLICABLE_POLICY: 'Procedural record does not establish current policy applicability',
  NO_OFFICIAL_POLICY_COVERAGE: 'No official policy source covers this theme',
  NO_REFERENCE_COVERAGE: 'No matching reference coverage',
  ACTION_CLAIM_FORBIDDEN: 'This review does not cover action claims',
  ASSURANCE_CLAIM_FORBIDDEN: 'This review does not cover assurance claims',
  CITATION_UNKNOWN: 'Citation is not recognized',
  CITATION_REGION_MISMATCH: 'Citation region does not match',
  CITATION_THEME_MISMATCH: 'Citation theme does not match',
  CLAIM_REFERENCE_TYPE_MISMATCH: 'Citation type does not support this claim',
  DOCUMENT_STATED: 'Document stated',
  MISSING: 'Date missing',
  NOT_VERIFIED: 'Not verified',
  NOT_STATED_IN_REVIEWED_DOCUMENT: 'Not stated in the reviewed document',
  NOT_APPLICABLE: 'Not applicable',
  AUTHENTIC_SANDBOX_RESPONSE: 'Live Sandbox response',
  SYNTHETIC_TEST_RESPONSE: 'Synthetic test run',
  OPERATOR_LIVE_RESPONSE: 'Live model response',
  POST_RESPONSE_ONLY: 'Verified from the response',
  CONNECTED: 'Connected',
  DRAFT: 'Draft · not sent',
  FROZEN: 'Not submitted',
  SUBMITTED: 'Submitted to Sandbox',
  PERFORMED: 'Submitted',
  connected: 'Connected',
  disconnected: 'Disconnected',
  not_configured: 'Not configured',
  error: 'Connection error',
  needs_review: 'Needs review',
  draft_ready: 'Draft ready',
  local_draft_reviewed: 'Local review recorded',
  INR: 'Item not received',
  delivered: 'Delivered',
  synthetic: 'Demo record',
  unsupported_reason: 'Unsupported case reason',
  AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES: 'Authored demo scenario',
  SYNTHETIC_PROVIDER_FIXTURE: 'Demo provider record',
  SYNTHETIC_BASELINE: 'Demo baseline',
  CALLER_SUPPLIED_UNVERIFIED: 'Unverified supplied baseline',
  // The corpus holds author paraphrases of PayPal pages (with links), not the pages themselves (Q11).
  official_api_reference: 'PayPal developer reference (paraphrased)',
  official_policy: 'PayPal US policy (paraphrased)',
  official_api_schema: 'PayPal developer field list (paraphrased)',
  official_policy_guidance: 'PayPal policy guidance (paraphrased)',
  public_case_decision: 'Public case record',
  public_court_order_copy: 'Official US court procedural record',
  any: 'All source stages',
  procedural_order: 'Procedural order · not final merits',
  not_applicable: 'Policy or developer document · not a case decision',
  SETTLEMENT_APPROVAL_NOT_FINAL_MERITS: 'Settlement approval · not a final merits finding',
  ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED: 'Arbitration compelled · underlying merits not decided',
  saved_retrieved_at_exact_elapsed_time: 'Saved retrieval time compared with the evaluation time',
  policy_reference: 'Policy reference',
  current_policy: 'Current-policy claim',
  historical_case: 'Historical case',
  procedural_reference: 'Procedural reference',
  api_reference: 'Developer reference',
  guidance_reference: 'Policy guidance reference',
  financial_action: 'Financial action',
  assurance: 'Assurance claim',
  'payguard-bounded-advisory-v3': 'Fixed advisory contract',
  PAYLOAD_DIGEST_BOUND: 'Draft details locked for this review',
  SEPARATE_READBACK_TRUE: 'Verified by a separate status check',
  SEPARATE_READBACK_FALSE: 'Verified from the creation response only',
  EXTERNAL_ACTION_FALSE: 'No external action authorized',
  DEMO_OPERATOR_UNAUTHENTICATED: 'Demo operator · identity not authenticated',
  SESSION_MEMORY_ONLY: 'Stored in this session',
};

export const OPERATOR_LABELS = Object.freeze(labels);

// (N2 C63, COPY_FINAL_v4_1) Phone text (below 768px) for the two developer-docs labels; read at render time.
// Node tests and wide screens get OPERATOR_LABELS. The field-list label keeps its one wording on every width.
export const OPERATOR_LABELS_PHONE = Object.freeze({
  API_REFERENCE_NOT_POLICY: 'PayPal developer docs do not decide policy',
  official_api_reference: 'Developer reference (paraphrased)',
});
const phoneWidth = () => typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia('(max-width: 767px)').matches;

export function operatorLabel(value, fallback = 'Needs review') {
  if (typeof value !== 'string' || value.length === 0) return fallback;
  if (Object.hasOwn(OPERATOR_LABELS_PHONE, value) && phoneWidth()) return OPERATOR_LABELS_PHONE[value];
  return Object.hasOwn(OPERATOR_LABELS, value) ? OPERATOR_LABELS[value] : fallback;
}

export function operatorLabels(values, fallback = 'Needs review') {
  if (!Array.isArray(values) || values.length === 0) return [];
  return values.map((value) => operatorLabel(value, fallback));
}

export function sandboxReadbackLabel(separateReadback) {
  return operatorLabel(separateReadback === true ? 'SEPARATE_READBACK_TRUE' : 'SEPARATE_READBACK_FALSE');
}

// (2026-11-10, video frame MAIN 168 s) The local review receipt said "Not submitted" next to a Status row reading
// "Submitted to Sandbox". Once this case's evidence was sent (local or hosted), the receipt says so; before, the
// server's own value (FROZEN -> "Not submitted").
export function reviewSubmissionLabel(receipt, sentTo) {
  return sentTo ? `${labels.SUBMITTED} (${sentTo})` : operatorLabel(receipt?.external_submission || 'FROZEN');
}
export function restoredReviewText(sentTo) {
  return sentTo ? `Review recorded earlier in this session. Evidence was sent to the PayPal Sandbox (${sentTo}).`
    : 'Review recorded earlier in this session. Nothing was sent to PayPal.';
}

// (K8, three-way arbitration 2026-11-13) After a PayPal read-back, one fixed next step per dispute status. Rules only,
// no AI call, no promise about the outcome: PayPal decides the case.
const NEXT_STEPS = Object.freeze({
  WAITING_FOR_SELLER_RESPONSE: 'PayPal is waiting for you. Review the draft, then send it.',
  WAITING_FOR_BUYER_RESPONSE: 'PayPal is waiting for the buyer. Nothing to send now.',
  UNDER_REVIEW: 'PayPal is reviewing your case. Keep your records ready; PayPal decides.',
  RESOLVED: 'PayPal closed this case. Check the outcome in your PayPal account.',
});
// Right after a send PayPal may still show the seller's turn for a moment: never tell the seller to send again then.
export function nextStepFor(status, { afterSend = false } = {}) {
  const key = String(status ?? '').trim().toUpperCase().replace(/[\s-]+/g, '_');
  if (afterSend && key === 'WAITING_FOR_SELLER_RESPONSE') return 'PayPal may still be updating. Check again soon; do not send twice.';
  return NEXT_STEPS[key] || 'Check this case in your PayPal account before you act.';
}
