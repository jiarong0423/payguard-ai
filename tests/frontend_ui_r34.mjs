import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { hostedCopy, hostedGeminiMode } from '../frontend/src/hostedCopy.js';
import { SELLER_EVIDENCE_LOCK, SELLER_EVIDENCE_TEXT, sellerEvidenceOnFile, sendLockReason } from '../frontend/src/lockReasons.js';

// (r34 cross review) Console fixes: hosted Why? text from the guide's chooser status (#1), a dispute PayPal already
// has seller evidence for (#2), preview-only pairing wording (#3), case amount in the send dialog (#6), refused
// preview reason in place (#7), missing-record counts (#8), route summary after the review (#9), the per-turn model
// line first in the reply (#12), Technical details last (#13), wrapping instead of clipping (#14), local times (#15)
// and the country check lost with an expired session (#21).
const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const app = read('frontend/src/App.jsx');
const guide = read('frontend/src/GuideLive.jsx');
const guideCss = read('frontend/src/GuideLive.css');
const replay = read('frontend/src/GuideReplay.jsx');
const replayCss = read('frontend/src/GuideReplay.css');
const css = read('frontend/src/index.css');

// ---- #1: the Gemini line follows chooser_mode from the guide API, the value behind the guide's badge. ----
{
  assert.equal(hostedGeminiMode(null), 'unknown');
  assert.equal(hostedGeminiMode({ chooser_mode: 'keyword', model_requested: true }), 'off', 'requested but no chooser: off');
  assert.equal(hostedGeminiMode({ chooser_mode: 'gemini', model_requested: true }), 'gemini');
  const on = hostedCopy({ chooser_mode: 'gemini', model_requested: true });
  assert.equal(on.gemini, 'On for the guide only (5 a minute, 20 a day)');
  assert.equal(on.pill, 'Hosted demo · no PayPal calls');
  assert.equal(/never calls PayPal or Gemini|rules only|rules-only/u.test(`${on.intro} ${on.pill} ${on.guides}`), false, 'no "never Gemini" claim while the guide uses it');
  assert.equal(on.local, 'Gemini evidence brief', 'the guide is no longer listed as local only');
  const off = hostedCopy({ chooser_mode: 'keyword', model_requested: false });
  assert.equal(off.gemini, 'Off in hosted demo');
  const unknown = hostedCopy(null);
  assert.equal(/Off in hosted demo|never calls PayPal or Gemini/u.test(`${unknown.gemini} ${unknown.intro}`), false, 'no "Off" before any guide reported');
  // Wiring: every guide reports its chooser status; the badge receives it; the popover still calls no API.
  assert.ok(guide.includes("if (view?.chooser_mode) onChooser?.({ chooser_mode: view.chooser_mode, model_requested: view.model_requested === true });"), 'guide reports the chooser status');
  assert.ok(guide.includes("const modeBadge = view?.chooser_mode === 'gemini' ? <Badge tone=\"muted\">Rules + Gemini</Badge>"), 'badge reads the same field');
  assert.equal(app.split('onChooser={setGuideChooser}').length - 1, 3, 'all three guides report');
  assert.ok(app.includes('<HostedBadge guideChooser={guideChooser} sandboxReads={sandboxReads} sandboxSend={sandboxSend} />'), 'badge gets the status');
  assert.ok(app.includes("const HOSTED_DISABLED_NOTICE = 'This needs a local run: on the hosted demo, invoice drafts, tracking and the AI brief are off.';"), 'notice no longer says "no Gemini calls" or "cannot write to PayPal" (2026-11-10, intended)');
}

// ---- #2: PayPal already has seller evidence (SUBMITTED_BY_SELLER row or not waiting for the seller). ----
{
  const live = { source: 'paypal_sandbox', status: 'WAITING_FOR_SELLER_RESPONSE', evidences: [{ evidence_type: 'PROOF_OF_FULFILLMENT', source: 'REQUESTED_FROM_SELLER' }] };
  assert.equal(sellerEvidenceOnFile(live), false, 'waiting, only requested: can send');
  assert.equal(sellerEvidenceOnFile({ ...live, evidences: [...live.evidences, { evidence_type: 'PROOF_OF_FULFILLMENT', source: 'SUBMITTED_BY_SELLER' }] }), true, 'seller evidence on file');
  assert.equal(sellerEvidenceOnFile({ ...live, status: 'WAITING_FOR_BUYER_RESPONSE' }), true, 'no longer waiting for the seller');
  assert.equal(sellerEvidenceOnFile({ ...live, source: 'synthetic_fixture', status: 'UNDER_REVIEW' }), false, 'sample cases never send anyway');
  assert.equal(sellerEvidenceOnFile(null), false);
  assert.equal(SELLER_EVIDENCE_LOCK, 'Locked: PayPal already has seller evidence for this dispute.');
  assert.equal(SELLER_EVIDENCE_TEXT, 'PayPal already has seller evidence');
  const ready = { external_send: 'FROZEN', source: 'paypal_sandbox', submit_flag_enabled: true };
  assert.equal(sendLockReason({ draft: {}, receipt: {}, preview: ready }), null, 'ready without seller evidence');
  assert.equal(sendLockReason({ draft: {}, receipt: {}, preview: ready, sellerEvidence: true }), SELLER_EVIDENCE_LOCK, 'locked with it');
  assert.equal(sendLockReason({ draft: {}, receipt: null, preview: null, sellerEvidence: true }), SELLER_EVIDENCE_LOCK, 'said before any other step');
  assert.equal(sendLockReason({ draft: {}, receipt: {}, preview: { ...ready, external_send: 'SUBMITTED' }, sellerEvidence: true }), 'Sent: this evidence already went to PayPal Sandbox.', 'our own send still reads Sent');
  assert.equal(sendLockReason({ kind: 'tracking', draft: {}, receipt: {}, preview: ready, sellerEvidence: true }), null, 'tracking is not the evidence send');
  assert.ok(app.includes("['Provider submission', sellerEvidence ? SELLER_EVIDENCE_TEXT : operatorLabel(providerDisputeDetail.provider_submission)],"), 'detail row derived from the evidences');
  assert.ok(app.includes("&& !evidenceBlock && !sellerEvidence;"), 'Submit stays locked');
  assert.ok(app.includes("{sendConfirm && !(sendConfirm === 'evidence' && sellerEvidence) && <SendConfirmDialog"), 'the send dialog never opens for it');
  // (fix r1 F2) Also locked once this session's own send for the open dispute is on screen.
  assert.ok(app.includes('<Button data-testid="evidence-preview" icon="file" disabled={disabled || !draft || !providerDisputeDetail || sellerEvidence || evidenceSent}'), 'no preview (and so no pairing) for it');
  assert.ok(app.includes('if (sellerEvidenceOnFile(providerDisputeDetail)) return;'), 'previewEvidence refuses it too');
}

// ---- #3 and #7: preview-only pairing wording; a refused preview names its reason in place. ----
const section = app.slice(app.indexOf('const SEND_HOLD_SECONDS'), app.indexOf('function LockReason'));
const grab = (name) => { const match = section.match(new RegExp(`(?:const ${name} = [^\\n]*\\n|function ${name}\\([\\s\\S]*?\\n\\}\\n)`, 'u')); return match ? match[0] : ''; };
{
  const factory = new Function('operatorLabel', `${grab('maskDisputeId')}${section.match(/const ACCOUNT_LINES = \{[\s\S]*?\n\};\n/u)[0]}${grab('sameMoney')}${grab('sendGuardBlock')}return { sendGuardBlock };`);
  const { sendGuardBlock } = factory((value, fallback = 'Needs review') => value || fallback);
  const detail = { dispute_id: 'PP-D-0000000002', reason: 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED', dispute_amount: { currency_code: 'USD', value: '48.00' }, source: 'paypal_sandbox' };
  assert.equal(sendGuardBlock(null, detail, {}, 'PP-D-…81'), 'Paired with PP-D-…81 (preview only). Reset demo to pair it with another dispute.');
  assert.equal(sendGuardBlock(null, detail, {}, 'PP-D-…81', 'PP-D-…81'), 'This case was already sent to PP-D-…81; it cannot also go to PP-D-…02.');
  assert.ok(app.includes("if (result?.external_send === 'SUBMITTED') sentByCaseRef.current[result.case_ref] = maskDisputeId(result.dispute_id);"), 'sent only after a real send');
  assert.equal(app.split('boundByCaseRef.current = {}; sentByCaseRef.current = {}; setPreviewRefusal(null);').length - 1, 2, 'Reset demo and a new session forget the pairings');
  assert.equal(sendLockReason({ draft: {}, receipt: {}, refusal: 'This dispute does not match the selected case (reason or amount differ).' }),
    'Locked: This dispute does not match the selected case (reason or amount differ).', 'refusal reason, not "prepare the preview first"');
  assert.ok(app.includes("if (failure?.status !== 409) throw failure;"), 'only a 409 refusal is kept in place; other failures keep the banner');
  assert.ok(app.includes("setPreviewRefusal({ kind, ...request, message: failure.message || 'The server refused this preview. Nothing was sent.' });"), 'refusal kept with its dispute and case');
  assert.ok(/@media \(max-width: 640px\) \{\n  \/\* \(r34 #7\)[^\n]*\n  \.feedback-region \.message-error \{ max-height: 40vh; max-height: 40dvh; overflow-y: auto; \}/u.test(css), 'phone error never grows over the bar');
  assert.ok(css.includes('.app-shell.has-phone-action .feedback-region .message-error { bottom: calc(56px + 12px + env(safe-area-inset-bottom)); }'), 'and sits above it');
}

// ---- #6: Case amount beside the dispute amount in the send dialog. ----
{
  const dialog = app.slice(app.indexOf('function SendConfirmDialog('), app.indexOf('function LockReason'));
  const caseRow = dialog.indexOf('<dt>Case amount</dt><dd data-testid="send-confirm-case-amount">{caseAmount ? `${caseAmount.value} ${caseAmount.currency_code}` : \'—\'}</dd>');
  assert.ok(caseRow > 0 && caseRow < dialog.indexOf('<dt>Dispute amount</dt>'), 'case amount, then dispute amount');
  assert.ok(app.includes('caseAmount={caseItem?.dispute_amount}'), 'the selected case supplies it');
}

// ---- #8: "Missing in 50 of 50 orders". ----
{
  assert.ok(app.includes('<li key={label}>{label}: missing in {count - present} of {count} orders</li>'), 'missing count, not present count');
  const present = 0; const count = 50;
  assert.equal(`Tracking numbers: missing in ${count - present} of ${count} orders`, 'Tracking numbers: missing in 50 of 50 orders');
}

// ---- #9: after the local review the summary says what is next; server values stay in Technical details. ----
{
  assert.ok(app.includes("<strong data-testid=\"dispute-readiness\">{receipt || reviewedOnServer ? 'Reviewed · next: preview and send' : operatorLabel(draft.routing?.overall_state)}</strong>"));
  assert.ok(app.includes('{!(receipt || reviewedOnServer) && <small data-testid="dispute-actions">Draft ready: review it below. PayPal action for this case:'), 'Next options hidden after the review');
  assert.ok(app.includes('<p data-testid="dispute-route-server">Server routing: {operatorLabel(draft.routing.overall_state)} · next options:'), 'server values in Technical details');
}

// ---- #12: the per-turn model line is the first line inside the reply bubble. ----
{
  const bubble = guide.slice(guide.indexOf('{log.map((row) => <li key={row.id}'), guide.indexOf('</ol>'));
  const funnel = bubble.indexOf('{row.funnel && <small className="guide-live-funnel" data-testid="guide-live-funnel">{row.funnel}</small>}');
  assert.ok(funnel > bubble.indexOf('<span className="guide-live-tag">') && funnel < bubble.indexOf('{row.badge &&') && funnel < bubble.indexOf('<p className={row.analysing'), 'right under the speaker tag');
  assert.equal(bubble.split('guide-live-funnel').length - 1, 2, 'rendered once (class + test id)');
}

// ---- #13: Technical details last in the evidence area and set apart. ----
{
  const body = app.slice(app.indexOf('<div className="provider-disputes-body">'), app.indexOf('</details>\n        <StepSection id="evidence-board"'));
  const tech = body.indexOf('<details className="technical-details" data-testid="evidence-technical-details">');
  assert.ok(tech > body.indexOf('{trackingPreview && <div className="evidence-preview tracking-preview"') && tech > body.indexOf('data-testid="evidence-debug-id"'), 'below the previews and the Debug-Id line');
  assert.equal(body.slice(body.indexOf('</details>', tech) + '</details>'.length).trim(), '</div>', 'nothing after it in the send area');
  assert.ok(css.includes('.provider-disputes-body > .technical-details:last-child { margin-top: 32px; padding-top: 16px; border-top: 1px dashed var(--pg-color-rule); }'), 'set apart');
}

// ---- #14: wrap instead of clipping. ----
{
  assert.ok(css.includes('.case-card .badge { white-space: normal; max-width: 100%; overflow-wrap: anywhere; text-align: left; }'), 'dispute card badge wraps');
  assert.ok(/@media \(max-width: 900px\) \{\n  \.journey-step strong \{ white-space: normal; overflow: visible; text-overflow: clip;/u.test(css), 'step labels wrap at 768');
  assert.ok(css.includes('.feedback-region .message { overflow-wrap: anywhere; }'), 'toast text wraps');
  assert.ok(/\.guide-live-who \{[^}]*white-space: normal;[^}]*overflow-wrap: anywhere;/u.test(guideCss) && !/\.guide-live-who \{[^}]*text-overflow: ellipsis/u.test(guideCss), 'phone badge wraps');
  for (const field of ['label', 'status', 'source']) assert.ok(new RegExp(`field: '${field}'[^\\n]*wrapText: true, autoHeight: true`, 'u').test(replay), `gap table ${field} wraps`);
  assert.ok(replayCss.includes('.guide-replay-grid .ag-cell-wrap-text .gap-chip { white-space: normal; max-width: 100%; }'), 'chips wrap inside a wrapped cell');
}

// ---- #15: visible times in the viewer's clock; UTC only in Technical details. ----
{
  const dateLabel = app.slice(app.indexOf('function dateLabel(value) {'), app.indexOf('function utcLabel(value) {'));
  assert.equal(/timeZone:|UTC/u.test(dateLabel), false, 'dateLabel is local');
  assert.ok(dateLabel.includes("timeZoneName: 'short'"), 'local time names its zone (external review 2026-11-10: list vs UTC board)');
  assert.ok(app.includes('<ValidFor expiresAt={invoiceReview.expires_at} testId="invoice-valid-for" />'), 'draft context: "valid for m:ss"');
  assert.equal(app.includes('valid until {dateLabel('), false, 'no visible "valid until" UTC time');
  assert.ok(app.includes('· valid until {utcLabel(aup.expires_at)}</p>}'), 'UTC kept in Technical details');
  assert.ok(app.includes("{left > 0 ? `valid for ${Math.floor(left / 60)}:${String(left % 60).padStart(2, '0')}` : 'expired'}"), 'relative form');
  assert.ok(app.includes("dateLabel(detail.create_time) : '—'"), 'send dialog Opened is local');
  const local = new Date('2026-11-04T14:09:51Z').toLocaleString('en-US', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
  assert.equal(/UTC/u.test(local), false, local);
}

// ---- #21: after Reconnect, the lost country check says to run it again. ----
{
  assert.ok(app.includes('const countryLost = Boolean(state && lastCountryCheck && lastCountryCheck.session !== state.session_id && !countryCheck);'), 'lost = from another session');
  assert.ok(app.includes('data-testid="country-check-lost" role="status">Run the country check again: the {lastCountryCheck.seller_country} → {lastCountryCheck.buyer_country} result ended with the expired session.</p>}'), 'step 01 line');
  assert.ok(app.includes("lostCheck ? `Run the country check again in step 01: the ${lostCheck.seller_country} → ${lostCheck.buyer_country} result ended with the expired session.`"), 'step 03 line');
  assert.ok(app.includes('lostCheck={countryLost ? lastCountryCheck : null}'), 'passed to the step 03 summary');
}

console.log('frontend ui r34: ok');
