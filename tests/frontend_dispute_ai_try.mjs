// (R7 T6 + red team r7) The Disputes "Try it" box: local guide endpoints only, Rules only, and it says that the
// sentence joins the Step 03 guide, what it confirmed or marked there, why a refused turn was refused, and links to the guide.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const views = readFileSync(resolve(root, 'frontend/src/steps/CaseViews.jsx'), 'utf8');
const start = views.indexOf('function AiTry(');
const body = views.slice(start, views.indexOf('export function DisputeAiClip(', start));
assert.ok(start > 0 && body.length > 0, 'AiTry exists');
for (const path of ["'/guide/state?scenario=dispute'", "'/guide/start'", "'/guide/turn'"]) assert.ok(body.includes(path), `uses ${path}`);
assert.equal(/https?:\/\//u.test(body), false, 'no outside address');
assert.ok(body.includes("view.chooser_mode === 'gemini'") && body.includes('use the Step 03 guide below instead'), 'never sends while the guide is on Gemini');
assert.ok(body.includes('Rules only · no AI call · adds to the Step 03 guide'), 'says it joins the guide');
assert.ok(body.includes('Confirmed in the guide:') && body.includes('data-testid="dispute-ai-confirmed"'), 'lists items confirmed outright');
assert.ok(body.includes('Marked in the guide:') && body.includes('data-testid="dispute-ai-marked"'), 'lists items marked');
assert.ok(body.includes('Not added to the guide: ${failure.message}'), 'a refused turn shows the reason');
assert.ok(body.includes('data-testid="dispute-ai-open-result"') && body.includes('onClick={onOpenGuide}'), 'links to the same guide');
assert.ok(views.includes('<AiTry session={session} onOpenGuide={onOpenGuide} />'), 'clip passes the guide opener');
console.log('frontend_dispute_ai_try: ok');
