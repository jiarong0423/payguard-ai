import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { apiRequest, SEND_GUARD_MESSAGES } from '../frontend/src/api.js';

// (r25 send guard) Safeguards against sending to the wrong dispute: (a) case and dispute side by side, (b) a held send
// with one plain line, (c) a two-step confirm before a real send, (d) plain messages for the backend's refusal codes,
// plus the account identity line, the 3-second hold and the colours' contrast.
const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const section = app.slice(app.indexOf('// (r25 send guard) Safeguards'), app.indexOf('// (optimise r24) Next to "Confirm local draft review"'));
assert.ok(section.length > 2000, 'send guard section present');
assert.equal(/[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]/u.test(section), false, 'English only, no CJK');

// (b) The hold rule, run on its own source with a stub label function.
const grab = (name) => section.match(new RegExp(`(?:const ${name} = [^\\n]*\\n|function ${name}\\([\\s\\S]*?\\n\\}\\n)`, 'u'))[0];
const factory = new Function('operatorLabel', `${grab('maskDisputeId')}${grab('ACCOUNT_LINES').length ? section.match(/const ACCOUNT_LINES = \{[\s\S]*?\n\};\n/u)[0] : ''}${grab('sameMoney')}${grab('sendGuardBlock')}${grab('sendItemText')}return { maskDisputeId, sendGuardBlock, sendItemText };`);
const { maskDisputeId, sendGuardBlock, sendItemText } = factory((value, fallback = 'Needs review') => value || fallback);
assert.equal(maskDisputeId('PP-D-SANDBOX01'), 'PP-D-…01');
const detail = { dispute_id: 'PP-D-SANDBOX02', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', source: 'paypal_sandbox', dispute_amount: { currency_code: 'USD', value: '48.00' } };
const guard = { case_ref: 'case-ref-001', case_reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', dispute_masked: 'PP-D-…02', dispute_reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED',
  dispute_amount: { currency_code: 'USD', value: '48.00' }, bound_dispute_masked: 'PP-D-…02', sending_account_masked: 'SY…HANT', dispute_seller_masked: 'SY…HANT',
  account_status: 'MATCH', send_refusal: null };
const caseItem = { case_ref: 'case-ref-001', reason: 'INR', dispute_amount: { currency_code: 'USD', value: '48.00' } };
assert.equal(sendGuardBlock(guard, detail, caseItem, null), null, 'matching case and dispute: no hold');
assert.equal(sendGuardBlock(guard, detail, caseItem, 'PP-D-…01'), 'This case was already sent to PP-D-…01; it cannot also go to PP-D-…02.');
assert.match(sendGuardBlock({ ...guard, case_reason: 'MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED' }, detail, caseItem, null), /^The case reason .* does not match this dispute/);
assert.match(sendGuardBlock(guard, { ...detail, dispute_amount: { currency_code: 'USD', value: '49.00' } }, caseItem, null), /^The amount does not match/);
assert.match(sendGuardBlock(guard, { ...detail, dispute_amount: { currency_code: 'TWD', value: '48.00' } }, caseItem, null), /^The currency does not match/);
assert.match(sendGuardBlock(guard, { ...detail, source: 'synthetic_fixture' }, { ...caseItem, dispute_amount: { currency_code: 'USD', value: '18.00' } }, null), /amount does not match/, 'a fixture is held to its case amount');
assert.match(sendGuardBlock({ ...guard, account_status: 'MISMATCH', send_refusal: 'dispute_not_this_account' }, detail, caseItem, null), /different PayPal account/);
assert.match(sendGuardBlock({ ...guard, account_status: 'UNKNOWN', send_refusal: 'account_identity_unknown' }, detail, caseItem, null), /cannot confirm which PayPal Sandbox account/);
assert.match(sendGuardBlock(null, detail, caseItem, null), /Prepare the preview/);
assert.equal(sendItemText('tracking', { body: { trackers: [{ carrier: 'UPS', tracking_number: '****123' }] } }), 'Tracking: UPS ****123');
assert.match(sendItemText('evidence', { input: { evidences: [{ evidence_type: 'PROOF_OF_FULFILLMENT', evidence_info: { tracking_info: [{}] } }] }, files: [{ filename: 'synthetic-delivery.pdf' }] }),
  /files: synthetic-delivery\.pdf; 1 tracking row \(masked\)/);

// (a) Side by side, with the binding line and the account line; both send buttons are held by the guard.
for (const id of ['send-guard-case', 'send-guard-dispute', 'send-guard-bound', 'send-guard-account', 'send-guard-block']) assert.ok(section.includes(`data-testid="${id}"`), id);
assert.ok(section.includes('<span className="send-guard-label">From case</span>') && section.includes('<span className="send-guard-label">To PayPal dispute</span>'));
assert.ok(app.includes("trackingPreview?.external_send === 'FROZEN' && !trackingBlock;") && app.includes("evidencePreview?.external_send === 'FROZEN' && !evidenceBlock;"), 'sends held by the guard');
assert.ok(app.includes("onClick={() => setSendConfirm('evidence')}") && app.includes("onClick={() => setSendConfirm('tracking')}"), 'real sends open the dialog');
assert.ok(app.includes('onClick={previewEvidence}') && app.includes('onClick={previewTracking}'), 'previews stay one click');

// (c) Two steps: summary + tick + Continue; then the warning, a 3-second visible countdown and Send to PayPal.
assert.ok(section.includes('const SEND_HOLD_SECONDS = 3;'));
assert.ok(section.includes('role="dialog" aria-modal="true" aria-labelledby="send-confirm-title"') && section.includes('<h3 id="send-confirm-title">'), 'labelled modal dialog');
assert.ok(section.includes('I checked this is the right dispute'));
assert.ok(section.includes("disabled={!checked || checking || guard?.account_status !== 'MATCH'}") && section.includes('>Continue</Button>'), 'Continue needs the tick and a matching account');
assert.ok(section.includes('Sending as: Sandbox account {guard?.sending_account_masked') && section.includes('dispute seller: {guard?.dispute_seller_masked'), 'account identity, masked');
assert.ok(section.includes('This sends to PayPal and cannot be undone here.'));
assert.ok(section.includes('aria-live="polite" data-testid="send-confirm-countdown"') && section.includes('Send is available in ${left} second'), 'visible countdown');
assert.ok(section.includes('disabled={left > 0 || sending}') && section.includes("const send = async () => { if (sending) return; setSending(true); await onSend(); };"), 'held 3 s, then one click; disabled on the first click');
assert.ok(section.includes("if (event.key === 'Escape') { event.preventDefault(); onCancel(); return; }"), 'Escape cancels');
assert.ok(section.includes("if (event.key !== 'Tab') return;") && section.includes('last.focus()') && section.includes('first.focus()'), 'focus trapped');
assert.ok(section.includes('return () => { if (trigger && typeof trigger.focus === \'function\') trigger.focus(); };'), 'focus returns to the trigger');
assert.ok(section.includes('data-testid="send-confirm-back" tone="ghost" onClick={onCancel}>Back</Button>'), 'Back cancels');
assert.ok(app.includes("if (!before?.payload_sha256 || fresh.payload_sha256 !== before.payload_sha256 || held) {"), 'step 2 re-checks the fresh preview hash');
assert.ok(app.includes("setNotice(held || 'What would be sent changed since the preview; nothing was sent. Prepare the preview again.');"), 'plain message on a changed preview');

// (d) Plain messages for the refusal codes, from the server or the console's own fallback.
const session = { session_id: 's', csrf_token: 'c' };
for (const code of ['dispute_case_bound', 'evidence_type_not_supported', 'dispute_not_this_account', 'account_identity_unknown', 'input_characters_refused']) {
  assert.ok(SEND_GUARD_MESSAGES[code] && !/contract|error/i.test(SEND_GUARD_MESSAGES[code]), code);
  globalThis.fetch = async () => ({ ok: false, status: code === 'input_characters_refused' ? 422 : 409, headers: { get: () => null }, json: async () => ({ error: { code } }) });
  await assert.rejects(apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: { dispute_id: 'PP-D-SANDBOX01', case_ref: 'case-ref-001', submit: false }, session }),
    (failure) => failure.code === code && failure.message === SEND_GUARD_MESSAGES[code]);
}
const serverText = 'PayPal asks for an evidence type PayGuard cannot send yet (only proof of fulfillment with tracking is supported). Respond to this dispute in PayPal directly. Nothing was sent.';
globalThis.fetch = async () => ({ ok: false, status: 409, headers: { get: () => null }, json: async () => ({ error: { code: 'evidence_type_not_supported', message: serverText } }) });
await assert.rejects(apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: { dispute_id: 'PP-D-SANDBOX01', case_ref: 'case-ref-001', submit: false }, session }),
  (failure) => failure.message === serverText, 'the server sentence wins');

// The send_guard contract: accepted with masks, refused with a full id or an inconsistent status.
const reply = (payload) => async () => ({ ok: true, status: 200, json: async () => payload });
const envelope = { source: 'paypal_sandbox', data_source_label: 'Sandbox', environment: 'sandbox', evidence_class: 'SYNTHETIC_TEST_RESPONSE',
  observed_at: '2026-11-04T08:00:00Z', provider_submission: 'NOT_PERFORMED', paypal_debug_id: null };
const tracking = { ...envelope, readback: 'ADD_TRACKING_PREVIEW', dispute_id: 'PP-D-SANDBOX02', case_ref: 'case-ref-001', method: 'POST', path: '/v1/shipping/trackers-batch',
  content_type: 'application/json', body: { trackers: [{ transaction_id: '********0002', tracking_number: '****001', status: 'SHIPPED', carrier: 'UPS', carrier_name_other: null }] },
  external_send: 'FROZEN', submit_flag_enabled: true, human_review_required: true, payload_sha256: 'a'.repeat(64), send_guard: guard };
const trackingBody = { dispute_id: 'PP-D-SANDBOX02', case_ref: 'case-ref-001', submit: false };
globalThis.fetch = reply(tracking);
assert.deepEqual(await apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: trackingBody, session }), tracking, 'send_guard accepted');
for (const broken of [{ sending_account_masked: 'SYNTHETICMERCHANT' }, { account_status: 'MATCH', send_refusal: 'dispute_not_this_account' },
  { case_ref: 'case-ref-002' }, { dispute_masked: 'PP-D-SANDBOX02' }, { surprise: 1 }]) {
  globalThis.fetch = reply({ ...tracking, send_guard: { ...guard, ...broken } });
  await assert.rejects(apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: trackingBody, session }), /contract mismatch/, JSON.stringify(broken));
}

// Colours: orange Continue and sage-green Send, both at least 4.5:1 with white text (pinned ratios).
const luminance = (hex) => {
  const [r, g, b] = [1, 3, 5].map((index) => parseInt(hex.slice(index, index + 2), 16) / 255).map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (hex) => 1.05 / (luminance(hex) + 0.05);
const background = (selector) => css.match(new RegExp(`${selector.replace(/\./g, '\\.')} \\{ background: (#[0-9a-f]{6});[^}]*color: #fff;`, 'u'))[1];
const orange = background('.button.button-confirm-continue');
const green = background('.button.button-confirm-send');
assert.equal(orange, '#c2410c', 'orange token darkened from #e06c1e for AA');
assert.equal(green, '#4a6a4e', 'sage green');
assert.equal(Number(contrast(orange).toFixed(2)), 5.18);
assert.equal(Number(contrast(green).toFixed(2)), 6.06);
assert.ok(contrast('#e06c1e') < 4.5, 'the original orange would fail AA, hence the darker shade');
assert.ok(css.includes('.button.button-confirm-send.is-holding, .button.button-confirm-send:disabled { background: #cbd5d0;'), 'muted during the hold');
assert.ok(section.includes('icon="arrow"') && section.includes('icon="lock"'), 'colour always with a label and an icon');

console.log('frontend send guard r25: ok');
