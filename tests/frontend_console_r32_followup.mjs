import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// (r32 J4 P2-2, J5 P3-1 P3-2 P3-3, J1) Console follow-ups: a re-check that says "ready" but brings no send
// confirmation fails instead of counting down; both confirm dialogs are drawn on document.body; the send warning is
// the same orange as the draft warning; chart titles and subtitles wrap; the phone threshold label ends before the bars.
import { createSendConfirmTokens, MISSING_CONFIRM_NOTICE, readyWithoutToken } from '../frontend/src/sendConfirm.js';
import { monthlyChartOptions, velocityChartOptions } from '../frontend/src/charts/velocityChartData.js';

const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
const block = (name) => {
  const start = app.indexOf(`function ${name}(`);
  assert.ok(start > 0, `${name} present`);
  return app.slice(start, app.indexOf('\n}\n', start));
};

// ---- C7: readyWithoutToken, by behaviour over every combination of the four inputs. ----
const token = 'C'.repeat(32);
let combos = 0;
for (const submit_flag_enabled of [true, false, undefined]) {
  for (const source of ['paypal_sandbox', 'sample', undefined]) {
    for (const external_send of ['FROZEN', 'SUBMITTED', undefined]) {
      for (const confirm_token of [token, '', null, undefined, 42]) {
        const recheck = { payload_sha256: 'a'.repeat(64), submit_flag_enabled, source, external_send, confirm_token };
        const ready = submit_flag_enabled === true && source === 'paypal_sandbox' && external_send === 'FROZEN';
        const hasToken = typeof confirm_token === 'string' && confirm_token.length > 0;
        assert.equal(readyWithoutToken(recheck), ready && !hasToken, JSON.stringify(recheck));
        combos += 1;
      }
    }
  }
}
assert.equal(readyWithoutToken(null), false);
assert.equal(readyWithoutToken(undefined), false);
assert.equal(MISSING_CONFIRM_NOTICE, 'Could not get a send confirmation from the server; prepare the preview again. Nothing was sent.');

// The re-check the dialog runs, step by step with the real token store: a ready re-check without a token fails, keeps
// no token, and the send body would still carry null (which the server refuses), so nothing can go out.
const simulate = (before, fresh) => {
  const tokens = createSendConfirmTokens();
  tokens.remember('evidence', { confirm_token: 'OLD'.repeat(11) });
  const state = { dialog: 'evidence', notice: null };
  tokens.clear('evidence');
  if (!before?.payload_sha256 || fresh.payload_sha256 !== before.payload_sha256) { state.dialog = null; state.notice = 'changed'; return { ok: false, state, tokens }; }
  if (readyWithoutToken(fresh)) { state.dialog = null; state.notice = MISSING_CONFIRM_NOTICE; return { ok: false, state, tokens }; }
  tokens.remember('evidence', fresh);
  return { ok: true, state, tokens };
};
const before = { payload_sha256: 'a'.repeat(64) };
const readyFresh = { payload_sha256: 'a'.repeat(64), submit_flag_enabled: true, source: 'paypal_sandbox', external_send: 'FROZEN' };
const missing = simulate(before, readyFresh);
assert.equal(missing.ok, false, 'no countdown');
assert.deepEqual(missing.state, { dialog: null, notice: MISSING_CONFIRM_NOTICE }, 'dialog closed, plain notice');
assert.equal(missing.tokens.submitBody('evidence', {}).confirm_token, null, 'the old token is gone too');
const withToken = simulate(before, { ...readyFresh, confirm_token: token });
assert.equal(withToken.ok, true);
assert.equal(withToken.tokens.peek('evidence'), token);

// The wiring in App.jsx: after the payload/guard check, before the token is kept, and it closes the dialog.
const recheck = app.slice(app.indexOf('const recheckSend = async (kind) => {'), app.indexOf('const confirmSend = async (kind) => {'));
const at = recheck.indexOf('if (readyWithoutToken(fresh)) {');
assert.ok(at > recheck.indexOf('|| held) {'), 'after the payload and guard checks');
assert.ok(at < recheck.indexOf('sendConfirmTokens.current.remember(kind, fresh);'), 'before the token is kept');
assert.ok(recheck.slice(at, recheck.indexOf('return false;', at)).includes('setSendConfirm(null);\n        setNotice(MISSING_CONFIRM_NOTICE);'), 'closes and says why');
assert.ok(app.includes("import { createSendConfirmTokens, MISSING_CONFIRM_NOTICE, readyWithoutToken } from './sendConfirm.js';"));

// ---- C5: both confirm dialogs are portalled to document.body. ----
assert.ok(app.includes("import { createPortal } from 'react-dom';"));
for (const [name, testId] of [['SendConfirmDialog', 'send-confirm-backdrop'], ['DraftConfirmDialog', 'draft-confirm-backdrop']]) {
  const dialog = block(name);
  assert.ok(dialog.includes(`return createPortal(<div className="send-confirm-backdrop" data-testid="${testId}">`), `${name} portalled`);
  assert.ok(dialog.trimEnd().endsWith('</div>, document.body);'), `${name} on document.body`);
}

// ---- C2: one orange for both warnings, stronger than the Disputes body's muted paragraph rule. ----
assert.ok(block('SendConfirmDialog').includes('<p className="send-confirm-warning" data-testid="send-confirm-warning">'));
assert.ok(block('DraftConfirmDialog').includes('<p className="send-confirm-warning" data-testid="draft-confirm-warning">'));
// (P4 2026-11-12) Both warnings use the amber "check first" token instead of the off-palette orange #9a3412.
assert.match(css, /\.send-confirm \.send-confirm-warning \{[^}]*color: var\(--pg-color-warn\);/u);
assert.equal(/(^|\n)\.send-confirm-warning \{/u.test(css), false, 'no weaker single-class rule left');
assert.ok(css.includes('.provider-disputes-body > p, .provider-disputes-body p {'), 'the rule that greyed it (specificity 0,1,1 < 0,2,0)');

// ---- C5: chart captions wrap; the phone threshold label is short. ----
const rows = [{ label: '01:00', window: 'baseline', baseline: 100, spike: null }, { label: '09:00', window: 'spike', baseline: 100, spike: 500 }];
for (const options of [velocityChartOptions({ rows, reviewLine: 350, currency: 'USD' }, null), velocityChartOptions({ rows, reviewLine: 350, currency: 'USD' }, null, { compact: true }),
  monthlyChartOptions({ rows: [{ label: 'Oct', amount: 1000, ma3: null, change: null }], currency: 'USD' }, null)]) {
  for (const caption of [options.title, options.subtitle]) {
    assert.equal(caption.wrapping, 'on-space', `${caption.text} wraps`);
    assert.ok(caption.maxHeight >= 54, `${caption.text} has room for three lines`);
  }
}
assert.equal(velocityChartOptions({ rows, reviewLine: 350, currency: 'USD' }, null).axes.y.crossLines[0].label.text, 'Review threshold 350.00 USD/h');
assert.equal(velocityChartOptions({ rows, reviewLine: 350, currency: 'USD' }, null, { compact: true }).axes.y.crossLines[0].label.text, 'Review 350.00 USD/h');

console.log(JSON.stringify({ status: 'PASS', checks: [`readyWithoutToken ${combos} combos`, 'missing token fails the re-check', 'dialogs on document.body', 'one orange warning', 'chart captions wrap', 'phone threshold label'] }));
