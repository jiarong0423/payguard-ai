// (r31 J2 J4 J5 A4) One seller-readable line under a locked primary action, from the same conditions that disable
// the button (App.jsx passes them in). Never an environment-variable name: the operator detail stays in the
// button's title and in Technical details. null means "not locked for a reason the seller can act on": the button is
// usable, done, held by a line already shown next to it (a country Stop, the hosted-demo note), or only waiting for
// a request that is running.
export const SESSION_LOCK = 'Locked: the demo session expired. Select Reconnect first.';
// (r31 A3c) The policy result lasts 120 s on the server (store.py, evaluation expires_at); the console only says so.
export const POLICY_EXPIRED_LOCK = 'Locked: the description check expired after 2 minutes. Run Policy Check again.';

// Confirm Draft Context, then Create Sandbox draft: one line for the pair, for whichever is the next step.
export function draftLockReason({ sessionExpired = false, hosted = false, countryHeld = false, aup = null, aupExpired = false, aupConsumed = false,
  descriptionTooLong = false, invoiceChecked = false, invoiceReview = null, invoice = null, connected = false } = {}) {
  if (sessionExpired) return SESSION_LOCK;
  if (countryHeld) return null;
  if (!aupConsumed) {
    if (!aup) return aupExpired ? POLICY_EXPIRED_LOCK : 'Locked: run Policy Check on the description first.';
    if (descriptionTooLong) return 'Locked: shorten the description to 200 characters first.';
    if (!invoiceChecked) return 'Locked: tick the box above to confirm the draft context.';
    return hosted ? null : 'Locked: confirm the draft context first, then create the draft.';
  }
  if (hosted || invoice) return null;
  if (!invoiceReview) return 'Locked: confirm the draft context first.';
  if (!invoiceChecked) return 'Locked: tick the box above first.';
  if (!connected) return 'Locked: connect the US Sandbox first.';
  return null;
}

// Submit to PayPal Sandbox (test) / Send tracking to PayPal Sandbox (test). Returns null exactly when the console's
// evidenceSubmitReady / trackingSubmitReady is true: receipt, Sandbox source, preview still FROZEN, submit flag on and
// no send-guard block.
// (r32 J2 #6) `disputeSelected`: whether a PayPal Sandbox dispute row is open. The preview button is disabled without
// one, so "prepare the preview first" sent the seller in a loop; before a dispute is picked the line names that step.
export const SELECT_DISPUTE_LOCK = 'Locked: select a PayPal Sandbox dispute first.';
// (r34 #2) PayPal's own detail already shows seller evidence (an evidences row SUBMITTED_BY_SELLER) or the dispute no
// longer waits for the seller: PayPal would refuse another provide-evidence, so the evidence send stays locked and its
// dialog never opens. Derived from the GET detail the console already holds; no new backend field.
export const SELLER_EVIDENCE_LOCK = 'Locked: PayPal already has seller evidence for this dispute.';
export const SELLER_EVIDENCE_TEXT = 'PayPal already has seller evidence';
export function sellerEvidenceOnFile(detail) {
  if (!detail || detail.source !== 'paypal_sandbox') return false;
  return detail.status !== 'WAITING_FOR_SELLER_RESPONSE'
    || (Array.isArray(detail.evidences) ? detail.evidences : []).some((row) => row?.source === 'SUBMITTED_BY_SELLER');
}
// (r34 #7) `refusal`: the server's own sentence for a refused preview of this dispute and case (409), so the line
// under Submit names why instead of asking for the preview the seller just tried.
export function sendLockReason({ kind = 'evidence', sessionExpired = false, draft = null, receipt = null, preview = null, block = null, disputeSelected = true,
  sellerEvidence = false, refusal = null } = {}) {
  const tracking = kind === 'tracking';
  if (sessionExpired) return SESSION_LOCK;
  if (preview?.external_send === 'SUBMITTED') return tracking ? 'Sent: this tracking already went to PayPal Sandbox.' : 'Sent: this evidence already went to PayPal Sandbox.';
  if (sellerEvidence && !tracking) return SELLER_EVIDENCE_LOCK;
  if (!receipt) return draft ? 'Locked: confirm the local review first.' : 'Locked: prepare the evidence draft first.';
  if (!preview && !disputeSelected) return SELECT_DISPUTE_LOCK;
  if (!preview && refusal) return `Locked: ${refusal}`;
  if (!preview) return tracking ? 'Locked: preview the tracking for PayPal first.' : 'Locked: prepare the evidence request preview first.';
  if (preview.source !== 'paypal_sandbox') return 'Locked: this is a sample case; connect the US Sandbox and pick a Sandbox dispute to send.';
  if (block) return 'Locked: the dispute check above does not pass yet.';
  if (preview.submit_flag_enabled !== true) return 'Locked: sending is turned off on this console.';
  if (preview.external_send !== 'FROZEN') return 'Locked: prepare the preview again.';
  return null;
}

// Confirm local draft review. Nothing once the review is recorded (the button says so).
export function approveLockReason({ sessionExpired = false, draft = null, receipt = null, reviewedOnServer = false, reviewChecked = false } = {}) {
  if (!draft || receipt || reviewedOnServer) return null;
  if (sessionExpired) return SESSION_LOCK;
  if (!draft.draft_digest || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW') return 'Locked: this draft is not ready for a local review.';
  if (!reviewChecked) return 'Locked: first tick "I have read the evidence".';
  return null;
}
