// Round-1 review fixes (2026-11-10, buttons F1-F10 and UX U4/U6/U8/U9). Source and pure-logic checks; the browser
// probes that reproduce each finding are kept with the review evidence, not in this repository.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const app = read('frontend/src/App.jsx');
const css = read('frontend/src/index.css');

// F1: the receipt of a send made in this session is kept per dispute (page memory plus this tab's sessionStorage, tied
// to the session id) and shown again when that dispute is opened.
{
  assert.ok(app.includes("const SENT_STORE_KEY = 'payguard.console.sent.v1';"), 'own storage key');
  assert.ok(app.includes('if (!value || value.session_id !== sessionId || !value.items'), 'a stored receipt counts only for its own session');
  assert.ok(app.includes("row.result.external_send === 'SUBMITTED'\n  && row.result.dispute_id === id"), 'only a SUBMITTED result for that dispute is restored');
  // (round2 X, B 6a/6d) This page's own send first; a stored one only after the fresh read-back confirms it.
  assert.ok(app.includes('const mine = sentReceipts.current[disputeId] || null;\n    const stored = mine ? null : readStoredReceipts(session.session_id)[disputeId] || null;\n    const restored = restoredSendState(stored, result);\n    const kept = mine || (restored?.confirmed ? stored : null);'), 'looked up when a dispute is opened');
  assert.ok(app.includes('setProviderDisputeDetail(result); setEvidencePreview(kept ? kept.result : null); setTrackingPreview(null); setPreviewRefusal(null);'), 'receipt restored, nothing else kept');
  assert.ok(app.includes('    rememberSent(result);\n    rememberReceipt(session, result, null);\n    setEvidencePreview(result);'), 'remembered at the send');
  assert.equal((app.match(/sentReceipts\.current = \{\};/gu) || []).length, 2, 'memory cleared on a new session and on Reset demo');
  assert.equal(/writeStored\(SENT_STORE_KEY, [^)]*(csrf|token|description)/u.test(app), false, 'no token or seller input in the receipt store');
  assert.ok(app.includes('writeStored(RAN_STORE_KEY, null); writeStored(SENT_STORE_KEY, null);'), 'Reset demo clears the stored receipts');
  assert.ok(!/localStorage/u.test(app), 'still no localStorage');
}

// F2 / F2b: no new preview over a sent dispute; the open detail takes the read-back.
{
  assert.ok(app.includes("const evidenceSent = evidencePreview?.external_send === 'SUBMITTED';"));
  assert.ok(app.includes("    if (evidencePreview?.external_send === 'SUBMITTED') return;"), 'the handler refuses too');
  assert.ok(app.includes('disabled={disabled || !draft || !providerDisputeDetail || sellerEvidence || evidenceSent}'), 'preview button locked');
  assert.ok(app.includes('setProviderDisputeDetail((current) => (current?.dispute_id === fresh.dispute_id ? fresh : current));'), 'detail refreshed from the read-back, only for the same dispute');
}

// F3 / F4 / F5: the time column filters on the text it shows; one marked row.
{
  assert.ok(app.includes("{ field: 'occurred_at', headerName: 'TIME', minWidth: 180, flex: 1.2, cellDataType: 'text', filter: 'agTextColumnFilter', valueFormatter: ({ value }) => dateLabel(value),"), 'text column with a text filter');
  assert.ok(app.includes('filterValueGetter: ({ data }) => dateLabel(data?.occurred_at)'), 'column filter matches the displayed time');
  assert.ok(app.includes("getQuickFilterText: ({ value }) => `${dateLabel(value)} ${value || ''}`"), 'quick filter matches the displayed time and the raw value');
  assert.ok(read('frontend/src/grid/agGrid.jsx').includes('TextFilterModule'), 'text filter module registered');
  assert.ok(app.includes('useEffect(() => { try { velocityGridApi.current?.redrawRows(); } catch { /* grid already gone */ } }, [selectedOrderId]);'), 'rows redrawn on a new selection');
  assert.ok(app.includes('onGridReady={({ api }) => { velocityGridApi.current = api; }}'));
}

// F6: the filter popup's text starts after AG Grid's search icon.
assert.match(css, /\.ag-filter-body input\.ag-input-field-input\[type="text"\][^{]*\{ padding-left: 30px; \}/u, 'filter box leaves room for the icon');

// F7: a "Proof rows" link always lands on at least one row; tools without rows link to where they run.
{
  const { SPONSOR_MAP, sponsorHref } = await import('../frontend/src/sponsorMap.js');
  const facts = JSON.parse(read('frontend/src/data/proof_facts_v1.json'));
  for (const entry of SPONSOR_MAP) {
    if (entry.proof) assert.ok(facts.rows.some((row) => row.sponsors?.includes(entry.proof)), `${entry.name}: "Proof rows" has a row to show`);
    else assert.ok(entry.href.startsWith('/'), `${entry.name}: links to where it runs`);
  }
  assert.equal(sponsorHref(SPONSOR_MAP.find((entry) => entry.name === 'AG Grid')), '/#analytics');
  assert.equal(sponsorHref(SPONSOR_MAP.find((entry) => entry.name === 'Bryntum')), '/#evidence-board');
  assert.ok(app.includes("if (target === 'evidence-board') { setActiveStage('disputes'); setBoardExpanded(true); }"), 'the board link opens step 03 on the board tab');
  assert.ok(app.includes("setAnalyticsExpanded(target === 'analytics');"), 'the all-orders link opens that panel');
}

// F8: proof filters. A chip with rows of its own never lands on an empty list; a linked empty pair names the real reason.
{
  const { resolveProofFilter, emptyProofNote, rowMatches } = await import('../frontend/src/proof/proofData.js');
  const facts = JSON.parse(read('frontend/src/data/proof_facts_v1.json'));
  const count = (state) => facts.rows.filter((row) => rowMatches(row, state)).length;
  const paypalRows = count({ sponsor: 'PayPal' });
  assert.ok(paypalRows > 0 && count({ method: 'RECORDED', sponsor: 'PayPal' }) === 0, 'fixture: PayPal has rows, none Recorded');
  assert.deepEqual(resolveProofFilter(facts.rows, { method: 'RECORDED', sponsor: '' }, { sponsor: 'PayPal' }), { method: 'ALL', sponsor: 'PayPal' }, 'Recorded then PayPal: method resets');
  assert.deepEqual(resolveProofFilter(facts.rows, { method: 'ALL', sponsor: 'PayPal' }, { method: 'RECORDED' }), { method: 'RECORDED', sponsor: '' }, 'PayPal then Recorded: sponsor resets');
  assert.deepEqual(resolveProofFilter(facts.rows, { method: 'ALL', sponsor: 'PayPal' }, { method: 'REAL_SANDBOX' }), { method: 'REAL_SANDBOX', sponsor: 'PayPal' }, 'a pair with rows is kept');
  assert.deepEqual(resolveProofFilter(facts.rows, { method: 'RECORDED', sponsor: '' }, { sponsor: 'Bryntum' }), { method: 'RECORDED', sponsor: 'Bryntum' }, 'a tool with no row at all changes nothing else');
  assert.equal(emptyProofNote(facts.rows, { method: 'REAL_SANDBOX', sponsor: 'PayPal' }), '', 'no note when rows show');
  const pair = emptyProofNote(facts.rows, { method: 'RECORDED', sponsor: 'PayPal' });
  assert.ok(pair && !pair.includes('No proof row names PayPal'), 'an empty pair does not claim PayPal has no rows');
  assert.ok(emptyProofNote(facts.rows, { sponsor: 'Bryntum' }).startsWith('No proof row names Bryntum'), 'a tool without rows still says so');
  const page = read('frontend/src/proof/main.jsx');
  assert.ok(page.includes('onClick={() => setFilter(pick({ method: value }))}') && page.includes(": pick({ sponsor: name }))}"), 'both chip groups use the rule');
  assert.ok(page.includes('{countFor(pick({ method: value }))}') && page.includes('{countFor(pick({ sponsor: name }))}'), 'a chip count is what pressing it shows');
}

// F9: a replayed data-agent answer is also shown outside the Studio panel, and a phone goes to that line.
{
  const auditor = read('frontend/src/dashboard/auditor.js');
  const replay = auditor.slice(auditor.indexOf('if (recorded) {'), auditor.indexOf("result: { intent: 'replayed' }"));
  assert.ok(replay.indexOf('onDelegated({ question, summary: recorded.reply, ok: true, recorded: true });') > 0
    && replay.indexOf('onAnswer(recorded.page_id, null, { textOnly: true });') > replay.indexOf('onDelegated('), 'answer reported, then the page told it is text only');
  const dashboard = read('frontend/src/dashboard/main.jsx');
  assert.ok(dashboard.includes('setTimeout(() => (textOnly ? showAnswerLine() : focusAnswer()), 300);'), 'phone: answer line instead of a widget search');
  assert.ok(dashboard.includes('data-testid="dashboard-delegated" ref={delegatedLineRef} tabIndex={-1}'), 'the line can take focus');
  assert.ok(dashboard.includes("{delegated.recorded ? 'Recorded data-agent answer (no model call here):' : 'Data agent:'}"), 'a replay is labelled as recorded');
  assert.match(read('frontend/src/dashboard/dashboard.css'), /\.pg-delegated \{ scroll-margin-top: 136px;/u, 'not hidden under the sticky top bar');
}

// F10: a toggle chip keeps its width. The check mark's slot (left padding) exists in both states and the pressed label is not bolder.
for (const [path, selector] of [
  ['frontend/src/charts/charts.css', '.velocity-mark-chips button'],
  ['frontend/src/board/board.css', '.board-chips button'],
  ['frontend/src/AnalyticsDashboard.css', '.analytics-grid-chips button'],
  ['frontend/src/proof/proof.css', '.proof-filter-chip'],
  ['frontend/src/dashboard/dashboard.css', '.pg-replay-buttons button'],
]) {
  const sheet = read(path);
  assert.ok(sheet.includes(`${selector}[aria-pressed] { position: relative; padding-left: 30px; }`), `${path}: slot reserved in both states`);
  assert.ok(sheet.includes(`${selector}[aria-pressed]::before { content: "\\2713"; position: absolute; left: 10px; top: 50%; transform: translateY(-50%); visibility: hidden; }`), `${path}: the mark takes no room in the text flow`);
  assert.ok(sheet.includes(`${selector}[aria-pressed="true"]::before { visibility: visible; }`), `${path}: mark shown when pressed`);
  const pressed = sheet.split('\n').find((line) => line.startsWith(`${selector}[aria-pressed="true"] {`));
  assert.ok(pressed && !/font-weight|padding|letter-spacing|font-size/u.test(pressed), `${path}: pressed state changes no width-bearing property`);
  assert.equal(sheet.includes(`${selector}[aria-pressed="true"]::before { content:`), false, `${path}: no content added on press`);
}

// U4: after a send one Debug-Id line (the SUBMITTED card), no preview-only sentence, and fingerprints labelled for
// what they cover. The label's claim is checked against the backend: the preview value is a session-keyed HMAC of the
// whole request, the sent value a plain SHA-256 of one file's bytes.
{
  assert.ok(app.includes('{!evidenceSent && evidencePreview.paypal_debug_id && <p className="evidence-debug-id" data-testid="evidence-debug-id">'), 'Debug-Id line under the preview only before the send');
  assert.ok(app.includes("{evidenceSent ? (evidencePreview.sent_files?.length > 0 && <p className=\"text-dim\" data-testid=\"evidence-fingerprint-note\">{FINGERPRINT_NOTE}</p>) : <p className=\"text-dim\">Tracking numbers are masked in this preview."), 'preview sentence gone after the send');
  assert.ok(app.includes('data-testid="evidence-sent-sha256">Sent file SHA-256 (plain hash of the file\'s bytes): {file.sha256}</p>'), 'sent value labelled');
  assert.ok(app.includes('<dt title={FINGERPRINT_NOTE}>Request fingerprint (session-keyed SHA-256)</dt><dd data-testid="approval-payload-sha256"'), 'preview value labelled');
  assert.ok(/const FINGERPRINT_NOTE = '[^']*differ by design\.';/u.test(app), 'the note says the two values differ by design');
  const backend = read('backend/app/paypal_disputes.py');
  const keyed = backend.slice(backend.indexOf('def evidence_payload_sha256('), backend.indexOf('def tracking_payload_sha256('));
  assert.ok(keyed.includes('return _keyed_sha256(session, {"kind": "provide_evidence", "input": parts["input"][1], "files": files})'), 'preview fingerprint: keyed, whole request');
  assert.ok(backend.includes('return hmac.new(_payload_key(session), canonical.encode("ascii"), hashlib.sha256).hexdigest()'), 'keyed means HMAC under the session key');
  assert.ok(backend.includes('"byte_length": len(row["content"]), "sha256": hashlib.sha256(row["content"]).hexdigest()}'), 'sent fingerprint: plain hash of the file bytes');
}

// U6: one cue above the list; the send buttons and the pairing card right under the list; the PayPal read of the
// picked dispute last, inside the collapsed Technical details.
{
  const order = [
    'data-testid="provider-dispute-hint">Pick a dispute that is waiting for the seller.</p>}',
    '<div className="provider-dispute-list">',
    '<div className="provider-dispute-actions">',
    '&& <SendGuardSummary guard={',
    '<div className="send-receipt-big" data-testid="send-receipt"',
    '<details className="technical-details" data-testid="evidence-technical-details"><summary>Technical details</summary>',
    '<dl className="provider-dispute-detail" data-testid="provider-dispute-detail">',
  ].map((text) => { const at = app.indexOf(text); assert.ok(at > 0, text); return at; });
  assert.deepEqual(order, [...order].sort((a, b) => a - b), 'hint, list, buttons, pairing card, receipt, technical details with the detail');
  const technical = app.slice(order[5], app.indexOf('</details>', order[6]));
  assert.ok(technical.includes('data-testid="provider-dispute-detail"') && !/<details[^>]*\sopen/u.test(technical.slice(0, 120)), 'detail inside the fold, closed by default');
}

// U8: the phone bar never shows a dead "Local review recorded"; it offers the next step or steps aside, at one height.
{
  const bar = app.slice(app.indexOf("activeStage === 'disputes'\n"), app.indexOf("// The bar's action changed under the finger"));
  for (const text of [
    ': boardOpen || (reviewDone && (evidencePreview || (hosted && !sandboxSend))) ? null',
    "? { key: 'connect-disputes', label: 'Connect US Sandbox'",
    "? { key: 'pick-dispute', label: providerDisputeDetail ? 'Pick another PayPal dispute' : 'Pick a PayPal dispute'",
    ': reviewDone ? null',
  ]) assert.ok(bar.includes(text), text);
  assert.ok(bar.indexOf(': reviewDone ? null') < bar.indexOf("{ key: 'approve'"), 'the approve entry is reached only before the review is recorded');
  assert.ok(app.includes("<div className={`phone-action-bar${phoneReason ? ' has-reason' : ''}`}"), 'reason state marked on the bar');
  assert.match(css, /\.phone-action-bar\.has-reason \.button \{ min-height: 24px; height: 24px;/u, 'compact button when a reason shows');
  assert.match(css, /\.phone-action-bar\.has-reason \.phone-action-reason \{ line-height: 18px; white-space: nowrap;/u, 'one-line reason: 24 + 2 + 18 = the 44px row');
}

// U9: each repeated statement once. The disclosures themselves stay (checked where they are kept).
{
  assert.equal(app.includes('(it is there now)'), false);
  assert.ok(app.includes("setNotice('Local draft review recorded.');"), 'toast without the repeat');
  assert.ok(read('frontend/src/operatorLabels.js').includes("FROZEN: 'Not submitted'"), 'the receipt line still says Not submitted');
  const rules = read('frontend/src/CountryRules.jsx');
  assert.equal((rules.match(/araphrased from official pages/gu) || []).length, 1, 'paraphrase disclosure once');
  assert.ok(rules.includes('Paraphrased from official pages, {result.retrieved_at}. Not legal advice.</small>') && rules.includes('See <a href="/proof.html">Proof</a> for how the rules were checked.'), 'date, "not legal advice" and the Proof link kept');
  const board = read('frontend/src/board/EvidenceBoard.jsx');
  assert.equal(board.includes('The plan stays in this tab and is not sent anywhere.') || board.includes('made in this page, not sent.'), false, 'the standing help line and the download note no longer repeat it');
  assert.ok(board.includes("${stored ? 'Kept in this tab only' : 'Kept in this page only'}, not sent.`"), 'in the plan message, which every screen size shows');
}

console.log('frontend_fix_r1: ok');
