import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// (r30 J3 #1, J4 #6a/#6c) The hybrid funnel line under each guide reply, the country rule-audit note under the sources,
// and Technical details last in the guide panel.
const guide = readFileSync(new URL('../frontend/src/GuideLive.jsx', import.meta.url), 'utf8');
const guideCss = readFileSync(new URL('../frontend/src/GuideLive.css', import.meta.url), 'utf8');
const panel = readFileSync(new URL('../frontend/src/CountryRules.jsx', import.meta.url), 'utf8');
const panelCss = readFileSync(new URL('../frontend/src/CountryRules.css', import.meta.url), 'utf8');

// (a) The funnel helpers, run on their own source.
const grab = (name) => guide.match(new RegExp(`(?:const ${name} = \\{[\\s\\S]*?\\n\\};\\n|const ${name} = [^\\n]*\\n|function ${name}\\([\\s\\S]*?\\n\\}\\n)`, 'u'))[0];
const { changedLabels, whoBadge, funnelLine, autoLabels, modelMarks } = new Function(`${grab('changedLabels')}${grab('whoBadge')}${grab('MODEL_CALLS_TEXT')}${grab('funnelLine')}${grab('MARKED_TEXT')}${grab('modelMarks')}${grab('autoLabels')}return { changedLabels, whoBadge, funnelLine, autoLabels, modelMarks };`)();

const item = (id, label, status) => ({ id, label, status });
const before = [item('ship_date', 'Ship date', 'MISSING'), item('carrier', 'Carrier', 'MISSING'), item('delivery_record', 'Delivery record', 'MISSING')];

// Fixed rule (start, policy refusal, summary): no model step, nothing filled.
assert.equal(funnelLine(null, []), 'Model calls this turn: 0 · Nothing filled');
// Rules match: the rule layer filled one item from the seller's words and the keyword match moved another.
const ruled = { auto_confirmed: ['ship_date'], items: [item('ship_date', 'Ship date', 'PRESENT'), item('carrier', 'Carrier', 'PARTIAL'), before[2]] };
const filled = autoLabels(ruled);
const marked = changedLabels(before, ruled.items).filter((label) => !filled.includes(label));
assert.deepEqual(filled, ['Ship date']);
assert.deepEqual(marked, ['Carrier']);
assert.equal(funnelLine(null, filled, marked), 'Model calls this turn: 0 · Rules filled: Ship date · Rules marked: Carrier');
// Gemini: a started step counts as 1 at once ("analysing"), and stays 1 whatever its outcome.
assert.equal(funnelLine('analysing', filled, marked), 'Model calls this turn: 1 (Gemini, running) · Rules filled: Ship date · Rules marked: Carrier');
assert.equal(funnelLine('replaced', filled), 'Model calls this turn: 1 (Gemini, checked by rules) · Rules filled: Ship date');
assert.equal(funnelLine('kept', [], marked), 'Model calls this turn: 1 (Gemini, answer not used) · Rules marked: Carrier');
// A budget refusal may come before the first call (Governor.admit) or before the resend, so it never claims exactly 1.
assert.equal(funnelLine('budget', []), 'Model calls this turn: at most 1 (model limit reached) · Nothing filled');
// (r32 J1) While the Gemini step runs, the bubble shows a neutral running state, not "No word matched": the quick
// word-match answer is held back and shown only when the model answer is not used.
{
  const { RUNNING_TEXT, RUNNING_NOTE, runningRow } = new Function(`${grab('RUNNING_TEXT')}${grab('RUNNING_NOTE')}${grab('runningRow')}return { RUNNING_TEXT, RUNNING_NOTE, runningRow };`)();
  assert.equal(RUNNING_TEXT, 'Checking with Gemini…');
  assert.equal(RUNNING_NOTE, 'Gemini is reading this sentence. If its answer is not used, the word-match answer is shown here.');
  const running = runningRow(funnelLine('analysing', [], []));
  assert.deepEqual(running, { text: 'Checking with Gemini…', template: undefined, meta: '', badge: '', dropped: '', analysing: true,
    funnel: 'Model calls this turn: 1 (Gemini, running) · Nothing filled' }, 'running row: no quick answer, no word-match label');
  const send = guide.slice(guide.indexOf('const send = async (event) => {'), guide.indexOf('const saveRound = async'));
  assert.ok(send.includes("push('payguard', analysing ? runningRow(funnelLine('analysing', filled, marked))"), 'an analysing turn opens with the running row');
  assert.ok(send.includes('pendingRef.current = analysing ? { turn: result.analysis.turn, rowId, before, filled, marked, quick } : null;'), 'the quick answer is held for the pending turn');
  const settle = guide.slice(guide.indexOf('const settle = (result) => {'), guide.indexOf('useEffect(() => {', guide.indexOf('const settle = (result) => {')));
  assert.ok(settle.includes('patchRow(pending.rowId, { text: result.reply.text,'), 'replaced: the model answer');
  assert.ok(settle.includes('patchRow(pending.rowId, { ...pending.quick, analysing: false, note: KEPT_TEXT[reason]'), 'kept, limit or superseded: the quick answer comes back');
  assert.ok(guide.includes("patchRow(rowId, { ...quick, analysing: false, note: KEPT_TEXT.late,"), 'late: the quick answer comes back');
  assert.ok(guide.includes('<span className="guide-live-dot" aria-hidden="true" />{RUNNING_NOTE}</small>'), 'the running note under the bubble');
  assert.equal(guide.includes('The quick answer above stays'), false, 'no note pointing at a quick answer that is not shown');
  assert.ok(guideCss.includes('.guide-live .guide-live-msg p.guide-live-running { color: var(--gl-muted); }'), 'running text muted');
}
// A form entry that passed the rule check names the form check, not the seller's words.
assert.equal(funnelLine(null, ['Carrier'], [], 'Form check filled'), 'Model calls this turn: 0 · Form check filled: Carrier');
// The Gemini badge never claims an item the rule layer settled in the same turn; a rules badge still names it.
const after = [item('ship_date', 'Ship date', 'PRESENT'), before[1], item('delivery_record', 'Delivery record', 'PARTIAL')];
assert.equal(whoBadge({ chooser: 'model' }, before, after, ['Ship date']), 'Gemini → Delivery record');
assert.equal(whoBadge({ chooser: 'keyword' }, before, after, ['Ship date']), 'Rules → Ship date, Delivery record');
assert.equal(whoBadge({ chooser: 'model' }, before, before, []), 'Gemini → nothing counted');
// (r31 J3) A Gemini turn names what the accepted answer marked, with its status, instead of "Nothing filled".
const thursday = [item('ship_date', 'ship date', 'PARTIAL'), before[1], before[2]];
const geminiMarked = modelMarks([item('ship_date', 'ship date', 'MISSING'), before[1], before[2]], thursday, []);
assert.deepEqual(geminiMarked, ['ship date (not confirmed)']);
assert.equal(funnelLine('replaced', [], [], 'Rules filled', geminiMarked), 'Model calls this turn: 1 (Gemini, checked by rules) · Gemini marked: ship date (not confirmed)');
assert.equal(whoBadge({ chooser: 'model' }, [item('ship_date', 'ship date', 'MISSING'), before[1], before[2]], thursday, []), 'Gemini → ship date', 'badge and funnel line name the same item');
// Same rule as the badge: an item the rule layer settled this turn is not claimed for Gemini; other statuses read plainly.
assert.deepEqual(modelMarks(before, after, ['Ship date']), ['Delivery record (not confirmed)']);
assert.deepEqual(modelMarks(before, [item('ship_date', 'Ship date', 'CONFLICTING'), item('carrier', 'Carrier', 'STRUCTURALLY_PRESENT'), before[2]], []),
  ['Ship date (two different answers)', 'Carrier (filled in, not checked)']);
assert.equal(funnelLine('replaced', filled, [], 'Rules filled', ['Carrier (not confirmed)']), 'Model calls this turn: 1 (Gemini, checked by rules) · Rules filled: Ship date · Gemini marked: Carrier (not confirmed)');
// "Nothing filled" stays only when nothing was filled or marked.
assert.deepEqual(modelMarks(before, before, []), []);
assert.equal(funnelLine('replaced', [], [], 'Rules filled', modelMarks(before, before, [])), 'Model calls this turn: 1 (Gemini, checked by rules) · Nothing filled');

// (b) Wiring: the line is set when a turn is shown, then on every settle path (replaced, kept, poll limit).
// (r32 J1) The running row and the quick answer carry their own funnel line; the rules part and the quick answer are
// kept for the settle.
assert.ok(guide.includes("analysing ? runningRow(funnelLine('analysing', filled, marked))") && guide.includes('{ ...quick, analysing: false, funnel: funnelLine(null, filled, marked) });'), 'a started model step reads 1 at once');
assert.ok(guide.includes('pendingRef.current = analysing ? { turn: result.analysis.turn, rowId, before, filled, marked, quick } : null;'), 'the rules part is kept for the settle');
assert.ok(guide.includes("funnel: funnelLine('replaced', pending.filled, [], 'Rules filled', modelMarks(pending.before, result.items, pending.filled)) });"), 'replaced keeps 1 call and names what Gemini marked');
// (r31 J4) Plain suffix on the replaced answer, no "replaced the quick answer" jargon.
assert.ok(guide.includes('meta: `${chooserText(result.reply)} · used instead of the quick answer`'), 'plain replaced suffix');
assert.equal(guide.includes('replaced the quick answer'), false, 'old jargon gone');
assert.ok(guide.includes("funnel: funnelLine(reason === 'budget' ? 'budget' : 'kept', pending.filled, pending.marked) });"), 'kept keeps 1 call');
assert.ok(guide.includes("patchRow(rowId, { ...quick, analysing: false, note: KEPT_TEXT.late, funnel: funnelLine('kept', filled, marked) });"), 'poll limit keeps 1 call');
assert.ok(guide.includes('{row.funnel && <small className="guide-live-funnel" data-testid="guide-live-funnel">{row.funnel}</small>}'), 'one muted line per reply');
assert.ok(/\.guide-live \.guide-live-funnel \{[^}]*color: var\(--gl-muted\);[^}]*overflow-wrap: anywhere;/u.test(guideCss), 'muted and wraps on a phone');

// (c) Technical details: kept with its text, collapsed (no open attribute), after the guide layout, last in the panel.
const section = guide.slice(guide.indexOf('<section className="guide-live"'), guide.indexOf('</section>'));
const details = section.indexOf('<details className="technical-details guide-live-technical" data-testid="guide-live-technical"><summary>Technical details</summary>');
assert.ok(details > section.indexOf('{started && <div className="guide-live-layout">'), 'after the chat and the gap table');
assert.equal(section.split('<details').length - 1, 1, 'one Technical details in the guide');
assert.ok(section.slice(details).includes('Only code marks an item filled in: a form value that passes the rule check, or a closed value the rule layer reads from your own words, which you confirm in the summary. Your text and form values are not stored.</p></details>\n    '), 'text kept, closes the panel');
assert.equal(/<details[^>]*\sopen/u.test(section), false, 'collapsed by default');
assert.equal(section.includes('Only a form field that passes the rule check counts as filled in'), false, 'old form-only claim gone (r32 J3: the rule layer also fills items)');

// (d) Country rule audit (r48): a 36-rule TW and CN sample, muted under the sources, not in the verdict.
assert.ok(panel.includes("export const ruleAuditText = (names = {}) => `an earlier sample of 36 ${names.TW || 'TW'} and ${names.CN || 'CN'} rules was compared with their sources on 2026-11-02, and a recorded spot-check on 2026-11-08 sampled 48 of the 681 rules and compared 44 (34 consistent, 10 wording differs; 4 could not be opened); the other rules are not checked line by line`;"), 'audit wording states the sample, not whole countries');
assert.ok(panel.includes('Rule audit: {ruleAuditText(names)}.'), 'footnote shows the sample wording');
assert.equal(panel.includes('rules checked line by line against their sources'), false, 'no whole-country line-check claim');
const verdict = panel.slice(panel.indexOf('function Verdict('), panel.indexOf('// Optional amount'));
assert.equal(verdict.includes('lineCheck'), false, 'no audit line under the verdict');
const footnote = panel.indexOf('Paraphrased from official sources, {result.retrieved_at}. Not legal advice.</small>');
assert.ok(footnote > 0 && panel.indexOf('<LineCheckNote names={names} />') > footnote, 'audit note sits under the source lines');
assert.ok(panel.includes('<small className="country-footnote country-line-check-note" data-testid="country-verdict-line-check">'), 'muted footnote style');
assert.equal(panelCss.includes('.country-verdict-check'), false, 'no bold audit style left');

console.log('frontend guide funnel r30: ok');
