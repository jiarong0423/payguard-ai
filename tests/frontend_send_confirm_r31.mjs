import assert from 'node:assert/strict';

// (r31 J5 A6) The console side of the server's single-use send confirmation, by behaviour: the module App.jsx uses
// (frontend/src/sendConfirm.js) is driven the way the send dialog drives it (re-check, then send, then clear). The
// wiring inside App.jsx is pinned in frontend_foolproof_20261104.mjs.
import { createSendConfirmTokens, SEND_KINDS } from '../frontend/src/sendConfirm.js';

const fields = { dispute_id: 'PP-R-TST-00000001', case_ref: 'case-ref-001' };
const tokenA = 'A'.repeat(32);
const tokenB = 'B'.repeat(32);
const tokenT = 'T'.repeat(32);

assert.deepEqual(SEND_KINDS, ['evidence', 'tracking']);

// Nothing remembered yet: the body still says submit and carries null, which the server refuses (409).
const fresh = createSendConfirmTokens();
assert.deepEqual(fresh.submitBody('evidence', fields), { ...fields, submit: true, confirm_token: null });
assert.deepEqual(fresh.submitBody('tracking', fields), { ...fields, submit: true, confirm_token: null });

// The token from the latest re-check is the one sent.
const tokens = createSendConfirmTokens();
tokens.remember('evidence', { payload_sha256: 'a'.repeat(64), confirm_token: tokenA });
assert.equal(tokens.submitBody('evidence', fields).confirm_token, tokenA);
tokens.remember('evidence', { payload_sha256: 'a'.repeat(64), confirm_token: tokenB });
assert.equal(tokens.submitBody('evidence', fields).confirm_token, tokenB, 'a second re-check replaces the first token');
assert.deepEqual(tokens.submitBody('evidence', fields), { dispute_id: fields.dispute_id, case_ref: fields.case_ref, submit: true, confirm_token: tokenB });
assert.deepEqual(fields, { dispute_id: 'PP-R-TST-00000001', case_ref: 'case-ref-001' }, 'the request fields are not changed');

// Evidence and tracking tokens never cross.
assert.equal(tokens.submitBody('tracking', fields).confirm_token, null, 'an evidence re-check gives tracking nothing');
tokens.remember('tracking', { confirm_token: tokenT });
assert.equal(tokens.submitBody('tracking', fields).confirm_token, tokenT);
assert.equal(tokens.submitBody('evidence', fields).confirm_token, tokenB, 'a tracking re-check leaves the evidence token');
assert.equal(tokens.peek('evidence'), tokenB);
assert.equal(tokens.peek('tracking'), tokenT);

// Cleared after a send: the next send of that kind carries null; the other kind keeps its own.
tokens.clear('evidence');
assert.equal(tokens.submitBody('evidence', fields).confirm_token, null, 'used once');
assert.equal(tokens.submitBody('tracking', fields).confirm_token, tokenT, 'clearing evidence leaves tracking');
tokens.clear('tracking');
assert.equal(tokens.submitBody('tracking', fields).confirm_token, null);

// A re-check without a token leaves null (it never keeps the older one).
tokens.remember('evidence', { confirm_token: tokenA });
for (const recheck of [{}, { confirm_token: null }, { confirm_token: '' }, { confirm_token: 42 }, null, undefined]) {
  tokens.remember('evidence', recheck);
  assert.equal(tokens.submitBody('evidence', fields).confirm_token, null, `no token from ${JSON.stringify(recheck)}`);
  tokens.remember('evidence', { confirm_token: tokenA });
}

// Reset demo or a new session drops both.
tokens.remember('tracking', { confirm_token: tokenT });
tokens.clearAll();
assert.equal(tokens.peek('evidence'), null);
assert.equal(tokens.peek('tracking'), null);

// Two consoles (two stores) share nothing.
const one = createSendConfirmTokens();
const two = createSendConfirmTokens();
one.remember('evidence', { confirm_token: tokenA });
assert.equal(two.peek('evidence'), null);

console.log(JSON.stringify({ status: 'PASS', checks: ['latest re-check token is sent', 'evidence and tracking never cross', 'cleared after a send', 'null without a token', 'clearAll on reset'] }));
