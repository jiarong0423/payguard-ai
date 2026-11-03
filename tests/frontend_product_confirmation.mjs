// Q2: the seller's product confirmation survives the two-minute AUP expiry and reaches the review ZIP.
// It is cleared only by a description edit, a new policy check or a session change, and a confirmation reply
// that arrives after one of those (or for another session) is dropped. Simulated with the reducer the console uses.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { CLEAR_REASONS, initialProductConfirmation, productConfirmationReducer as reduce } from '../frontend/src/productConfirmation.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const appSource = readFileSync(resolve(projectRoot, 'frontend/src/App.jsx'), 'utf8');

const record = { choice: 'CONFIRMED', card: { title: 'Handmade Stoneware Coffee Mug, 12 oz' } };
const other = { choice: 'NONE_MATCH', card: null };
assert.deepEqual(CLEAR_REASONS, ['description_edited', 'policy_check', 'session_changed']);

// A session starts, the seller runs a check and confirms a card.
let state = reduce(initialProductConfirmation, { type: 'clear', reason: 'session_changed', session: 's1' });
state = reduce(state, { type: 'clear', reason: 'policy_check' });
const requested = { revision: state.revision, session: 's1' };
state = reduce(state, { type: 'confirmed', record, ...requested });
assert.equal(state.record, record, 'confirmation recorded');

// Two minutes later the AUP evaluation expires. Expiry is not a clear reason: nothing it dispatches changes the record.
for (const action of [{ type: 'clear', reason: 'aup_expired' }, { type: 'expired' }, { type: 'clear' }, undefined]) {
  assert.equal(reduce(state, action), state, `ignored: ${JSON.stringify(action)}`);
}
assert.equal(state.record, record, 'still there after expiry, so the review ZIP records SELLER_CONFIRMED');

// Each real clear reason empties it and bumps the revision.
for (const reason of CLEAR_REASONS) {
  const cleared = reduce(state, { type: 'clear', reason, session: reason === 'session_changed' ? 's2' : undefined });
  assert.equal(cleared.record, null, `${reason} clears it`);
  assert.equal(cleared.revision, state.revision + 1);
  assert.equal(cleared.session, reason === 'session_changed' ? 's2' : 's1', 'only a session change moves the session');
}

// Revision guard: a reply requested before an edit is dropped after it.
let racing = reduce(state, { type: 'clear', reason: 'policy_check' });
const inFlight = { revision: racing.revision, session: 's1' };
racing = reduce(racing, { type: 'clear', reason: 'description_edited' });
assert.equal(reduce(racing, { type: 'confirmed', record: other, ...inFlight }), racing, 'stale reply after an edit is dropped');
assert.equal(reduce(racing, { type: 'confirmed', record: other, revision: racing.revision, session: 's9' }), racing, 'reply for another session is dropped');
assert.equal(reduce(racing, { type: 'confirmed', record: null, revision: racing.revision, session: 's1' }), racing, 'an empty reply is not a confirmation');
assert.equal(reduce(racing, { type: 'confirmed', record: other, revision: racing.revision, session: 's1' }).record, other);

// The console uses it that way.
const invalidateAup = appSource.slice(appSource.indexOf('const invalidateAup = useCallback('), appSource.indexOf('const editDescription'));
assert.ok(invalidateAup.length > 0 && !invalidateAup.includes('dispatchProductConfirmation') && !invalidateAup.includes('setProductConfirm'),
  'clearing the AUP result (which expiry does) leaves the confirmation alone');
const expiry = appSource.slice(appSource.indexOf("The description check expired") - 200, appSource.indexOf("The description check expired") + 200);
assert.ok(expiry.includes('invalidateAup()') && !expiry.includes('dispatchProductConfirmation'), 'expiry dispatches no clear');
assert.ok(appSource.includes("const editDescription = (value) => { invalidateAup(); dispatchProductConfirmation({ type: 'clear', reason: 'description_edited' });"));
assert.match(appSource, /const scan = \(\) => action\('aup', async \(session\) => \{\s*invalidateAup\(\);\s*dispatchProductConfirmation\(\{ type: 'clear', reason: 'policy_check' \}\);/u);
assert.equal((appSource.match(/reason: 'session_changed'/gu) || []).length, 4, 'session created, expired, re-bootstrapped and demo reset');
assert.ok(appSource.includes("dispatchProductConfirmation({ type: 'confirmed', record: result, ...requested });"));
assert.ok(appSource.includes('current.revision !== requested.revision || current.session !== requested.session'), 'setter guarded before dispatch');
assert.ok(appSource.includes('downloadInternalReviewZip(draft, productConfirm);'));
assert.equal(/setProductConfirm\b/u.test(appSource), false, 'no other writer');
assert.ok(appSource.includes('data-testid="product-confirmation-kept"'), 'a kept confirmation stays visible after expiry');
console.log(JSON.stringify({ status: 'PASS', clear_reasons: CLEAR_REASONS.length }));
