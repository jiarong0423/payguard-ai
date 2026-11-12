// (R5 S25, 2026-11-12) "Days left" must not change with a viewer clock a few seconds off the server: the demo sets each
// deadline as server time plus whole days, so a phone 1 s behind used to read case-ref-003 as "2 days".
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dueDays, DUE_GRACE_MS } from '../frontend/src/dueDays.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(root, path), 'utf8');
const anchor = Date.parse('2026-11-12T07:45:00Z');
const DAY = 86400000;

for (const days of [1, 2]) {
  const due = new Date(anchor + days * DAY).toISOString();
  for (const skew of [-5000, -1000, 0, 1000, 5000]) {
    assert.equal(dueDays(due, anchor + skew), days, `${days} day(s) with the viewer clock ${skew} ms off`);
    assert.equal(dueDays(due, anchor + 60000 + skew), days, `${days} day(s) one minute later, clock ${skew} ms off`);
  }
}
assert.equal(dueDays('', anchor), null, 'no date, no count');
assert.equal(dueDays('not a date', anchor), null, 'bad date, no count');
assert.equal(dueDays(new Date(anchor - DAY).toISOString(), anchor) < 0, true, 'overdue stays negative');
assert.equal(DUE_GRACE_MS, 300000, 'five-minute grace');

// One function for every surface: the console and the step 03 views import it and keep no local copy.
for (const path of ['frontend/src/App.jsx', 'frontend/src/steps/CaseViews.jsx']) {
  const source = read(path);
  assert.ok(/import \{ dueDays \} from '\.{1,2}\/(?:\.\.\/)?dueDays\.js';|import \{ dueDays \} from '\.\.\/dueDays\.js';/u.test(source), `${path} imports the shared dueDays`);
  assert.equal(source.includes('function dueDays('), false, `${path} has no local dueDays`);
  assert.equal(source.includes('Date.now()) / 86400000'), false, `${path} has no raw day rounding`);
}
console.log('frontend_due_days_clock: ok');
