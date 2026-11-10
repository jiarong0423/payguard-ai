// (2026-11-11) One display mapping for PayPal dispute ids. It decides only what the screen shows; the true value is never
// changed. Comparisons, storage keys, API payloads and the send lock keep using the raw id or App.jsx maskDisputeId,
// never this function (tests/frontend_dispute_display_map.mjs checks both), so changing the shown format cannot change
// pairing.
//
// Mapping:
// - a code the server already masked (hosted: PP-R-VAF-XXXX7877, or PP-R-VAF-XXXX7877-2 after a clash; backend/app/demo_mode.py
//   _code_for) is shown as is;
// - the short form (PP-D-…01, or "…"; backend/app/paypal_disputes.py mask_dispute_id) is shown as is, so the mapping is
//   idempotent;
// - a raw id (local Sandbox) is shown in that short form: the first 5 and the last 2 characters;
// - anything else (empty, not a string, too short) is shown as "…".
const HOSTED_CODE = /^[A-Z0-9][A-Z0-9-]{0,40}-XXXX[A-Z0-9]{1,4}(?:-[0-9]{1,6})?$/u;
const SHORT_FORM = /^(?:[^…]{5}…[^…]{2}|…)$/u;

export const DISPUTE_ID_HIDDEN = '…';

export function isShownDisputeId(value) {
  return typeof value === 'string' && (HOSTED_CODE.test(value) || SHORT_FORM.test(value));
}

export function displayDisputeId(value) {
  if (typeof value !== 'string') return DISPUTE_ID_HIDDEN;
  if (isShownDisputeId(value)) return value;
  return value.length > 8 ? `${value.slice(0, 5)}…${value.slice(-2)}` : DISPUTE_ID_HIDDEN;
}
