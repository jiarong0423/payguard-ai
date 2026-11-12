// The recorded send replay (hosted demo): it must never reach PayPal or the server, it must say that nothing was sent,
// it keeps the two-step dialog (tick, Continue, a wait, Send), and it appears only in the hosted branch of step 03.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const MODULE = ['Recorded', 'SendReplay'].join('');
const replay = read(`frontend/src/${MODULE}.jsx`);
const app = read('frontend/src/App.jsx');
const facts = JSON.parse(read('frontend/src/data/proof_facts_v1.json'));

// No network, no session, no route name, no API helper.
for (const forbidden of ['fetch(', 'apiRequest', 'XMLHttpRequest', 'sendBeacon', 'provide-evidence', 'provide_evidence', 'localStorage', 'sessionStorage']) {
  assert.ok(!replay.includes(forbidden), `the replay never uses ${forbidden}`);
}
assert.ok(!/from '\.\/api\.js'/u.test(replay), 'the replay does not import the API module');

// It says what it is, in the chip, the note and the result.
assert.ok(replay.includes('Recorded, nothing is sent'), 'chip says recorded, nothing is sent');
assert.ok(replay.includes('Nothing was sent just now.'), 'result says nothing was sent');
assert.ok(replay.includes('Replay of a recorded real send.'), 'result is labelled a replay');
assert.ok(replay.includes('Nothing on this page sends anything to PayPal.'), 'note repeats the hosted promise');

// The same two steps as the console: tick, Continue, three seconds, Send.
assert.ok(replay.includes('REPLAY_WAIT_SECONDS = 3'), 'three second wait');
for (const id of ['recorded-replay-tick', 'recorded-replay-continue', 'recorded-replay-wait', 'recorded-replay-send', 'recorded-replay-result']) {
  assert.ok(replay.includes(`data-testid="${id}"`), `${id} exists`);
}
assert.ok(/disabled=\{!ticked\}/u.test(replay), 'Continue stays disabled until the box is ticked');

// It shows only what the committed receipt data holds.
assert.ok(facts.recorded_send && facts.recorded_send.steps.length >= 6, 'recorded send data present');
assert.ok(replay.includes('from ' + `'.` + `/data/proof_facts_v1.json'`) && replay.includes('send.steps.map') && replay.includes('send.limit'), 'result is rendered from the committed facts');

// It is rendered only in the hosted branch, next to the hosted note, and the local branch is unchanged.
assert.ok(app.includes(`const ${MODULE} = lazy(() => import('.` + `/${MODULE}.jsx'));`), 'App loads the replay lazily, so the console first load stays small');
assert.ok(app.includes('{hosted && <details key={sendNoneLeft ? \'replay-open\' : \'replay\'} open={sendNoneLeft || undefined} className="sandbox-details stage-fold" data-testid="replay-fold"><summary>{sandboxSend ? \'Earlier recorded send (replay, sends nothing now)\' : \'Try the send: a recorded replay · Nothing is sent now\'}</summary><Suspense fallback={<span className="grid-loading" role="status">Loading the replay</span>}><RecordedSendReplay /></Suspense></details>}\n        <details className="sandbox-details provider-disputes tg-fold"'), '(R6 S34: the sample-cases block is a .tg-fold) replay sits in its own closed fold (2026-11-09), only when hosted, above the collapsed sample-cases block (R6 S34: that block is a .tg-fold like every fold in step 03)');
assert.equal(app.split('<RecordedSendReplay />').length - 1, 1, 'rendered exactly once');
console.log(JSON.stringify({ status: 'PASS', steps: facts.recorded_send.steps.length }));
