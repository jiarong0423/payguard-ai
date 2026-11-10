// (2026-11-10, video frame MAIN 168 s) After a Sandbox send (local or hosted) the step 03 review receipt must not keep
// saying "Not submitted" while the request Status row says "Submitted to Sandbox". Pure-module and source checks.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { restoredReviewText, reviewSubmissionLabel } from '../frontend/src/operatorLabels.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const app = readFileSync(resolve(root, 'frontend/src/App.jsx'), 'utf8');

// Before a send: the server's value, FROZEN -> "Not submitted" (unchanged).
assert.equal(reviewSubmissionLabel({ external_submission: 'FROZEN' }, null), 'Not submitted');
assert.equal(reviewSubmissionLabel({}, null), 'Not submitted');
assert.equal(restoredReviewText(null), 'Review recorded earlier in this session. Nothing was sent to PayPal.');
// After a send: the same words as the Status row, with the masked id the send went to.
assert.equal(reviewSubmissionLabel({ external_submission: 'FROZEN' }, 'PP-D-XXXX7173'), 'Submitted to Sandbox (PP-D-XXXX7173)');
assert.ok(!reviewSubmissionLabel({ external_submission: 'FROZEN' }, 'PP-D-XXXX7173').includes('Not submitted'));
assert.ok(restoredReviewText('PP-D-XXXX7173').includes('sent to the PayPal Sandbox'));
assert.ok(!restoredReviewText('PP-D-XXXX7173').includes('Nothing was sent'));

// The receipt and the restored line read the per-case sent record (set only by an external_send SUBMITTED reply).
// (round2 X) sentTo is the full dispute id; the label gets its displayed form.
assert.ok(app.includes('const sentToShown = sentTo ? displayDisputeId(sentTo) : null;'), 'shown form of the sent id');
assert.ok(app.includes('reviewSubmissionLabel(receipt, sentToShown)'), 'receipt uses the sent state');
assert.ok(app.includes('restoredReviewText(sentToShown)'), 'restored line uses the sent state');
assert.ok(!app.includes("operatorLabel(receipt.external_submission || 'FROZEN')"), 'no fixed "Not submitted" left on the receipt');
assert.ok(/const rememberSent = \(result\) => \{\s*if \(result\?\.external_send === 'SUBMITTED' && typeof result\.dispute_id === 'string'\) sentByCaseRef\.current\[result\.case_ref\] = result\.dispute_id;/u.test(app));
console.log('frontend_send_receipt_label: ok');
