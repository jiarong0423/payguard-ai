// The confirmation popup before a question goes to the AI model (local live mode only).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const dialog = read('frontend/src/dashboard/DelegateConfirm.jsx');
const main = read('frontend/src/dashboard/main.jsx');
const auditor = read('frontend/src/dashboard/auditor.js');

// Plain words for the seller: no vendor name on the buttons, the cost and the cap said once, a Cancel that is focused first.
assert.ok(dialog.includes('<h2 id="pg-confirm-title">Ask the AI helper?</h2>'), 'plain title');
assert.ok(dialog.includes('>Ask the AI</button>') && dialog.includes('>Cancel</button>'), 'plain buttons');
assert.ok(!/>[^<]*Gemini[^<]*<\/button>/u.test(dialog), 'no vendor name on a button');
assert.ok(dialog.includes('uses a few paid calls') && dialog.includes('20 a day'), 'cost and cap are stated');
assert.ok(dialog.includes('role="dialog"') && dialog.includes('aria-modal="true"') && dialog.includes("event.key === 'Escape'"), 'dialog semantics and Escape');
assert.ok(dialog.includes('cancel.current?.focus()'), 'Cancel takes focus first, so a stray Enter sends nothing');

// It only answers the auditor's own question: it types the confirmation word and presses Send, nothing else.
assert.ok(dialog.includes("set.call(box, 'yes')") && dialog.includes('button.click()'), 'answers yes through the message box');
for (const forbidden of ['fetch(', 'apiRequest', 'XMLHttpRequest', 'studio/agent-turn']) assert.ok(!dialog.includes(forbidden), `the dialog never calls ${forbidden}`);

// Wired once: the auditor reports the pending question only when it asks, and the dashboard shows the dialog.
assert.ok(auditor.includes('onConfirmNeeded = () => {}') && auditor.includes('onConfirmNeeded(question)'), 'auditor reports the pending question');
assert.ok(main.includes('onConfirmNeeded: setConfirmQuestion'), 'dashboard receives it');
assert.ok(main.includes('<DelegateConfirm question={confirmQuestion} onCancel={() => setConfirmQuestion(null)} onSend={() => { setConfirmQuestion(null); answerYes(); }} />'), 'dialog rendered once');

// A question about amounts must not be answered by the "longest gap between events" check just because it says "largest".
const gap = auditor.match(/id: 'longest_gap'[\s\S]*?match: (\/.*\/iu),/u);
assert.ok(gap, 'the longest-gap matcher is found');
const matcher = new Function(`return ${gap[1]};`)();
for (const q of ['Where is the longest gap between recorded events?', 'Which case has the biggest delay?', 'longest wait']) assert.ok(matcher.test(q), `still answers: ${q}`);
for (const q of ['What is the largest disputed amount among the three cases?', 'largest amount', 'Which case has the biggest dispute?']) assert.ok(!matcher.test(q), `no longer misrouted: ${q}`);
console.log(JSON.stringify({ status: 'PASS' }));
