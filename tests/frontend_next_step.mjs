// (K9) nextStepFor: fixed next step after a PayPal read-back. Rules only, no promise about the outcome.
import assert from 'node:assert/strict';
import { nextStepFor } from '../frontend/src/operatorLabels.js';

assert.equal(nextStepFor('WAITING_FOR_SELLER_RESPONSE'), 'PayPal is waiting for you. Review the draft, then send it.');
assert.equal(nextStepFor('WAITING_FOR_BUYER_RESPONSE'), 'PayPal is waiting for the buyer. Nothing to send now.');
assert.equal(nextStepFor('UNDER_REVIEW'), 'PayPal is reviewing your case. Keep your records ready; PayPal decides.');
assert.equal(nextStepFor('Under review'), nextStepFor('UNDER_REVIEW'), 'labels normalise to the status key');
assert.equal(nextStepFor('under-review'), nextStepFor('UNDER_REVIEW'));
assert.equal(nextStepFor('RESOLVED'), 'PayPal closed this case. Check the outcome in your PayPal account.');
assert.equal(nextStepFor('APPEALABLE'), 'Check this case in your PayPal account before you act.', 'unknown status falls back');
assert.equal(nextStepFor(null), 'Check this case in your PayPal account before you act.');
// After a send, a stale "seller's turn" read must not ask the seller to send again.
assert.equal(nextStepFor('WAITING_FOR_SELLER_RESPONSE', { afterSend: true }), 'PayPal may still be updating. Check again soon; do not send twice.');
assert.equal(nextStepFor('WAITING_FOR_BUYER_RESPONSE', { afterSend: true }), nextStepFor('WAITING_FOR_BUYER_RESPONSE'));
for (const status of ['WAITING_FOR_SELLER_RESPONSE', 'WAITING_FOR_BUYER_RESPONSE', 'UNDER_REVIEW', 'RESOLVED', 'X']) {
  for (const afterSend of [false, true]) {
    const line = nextStepFor(status, { afterSend });
    assert.ok(!/\b(win|won|guarantee|refund approved|days?)\b/i.test(line), `no promise or deadline: ${line}`);
    assert.ok(line.split(/\s+/).length <= 14, `short: ${line}`);
  }
}
console.log('frontend_next_step: ok');
