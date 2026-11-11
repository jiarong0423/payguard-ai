import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { apiRequest } from '../frontend/src/api.js';

// Per-country rules panel: contract on the check payload, and the invoice draft stays closed on a BLOCK.
const app = readFileSync(new URL('../frontend/src/App.jsx', import.meta.url), 'utf8');
const panel = readFileSync(new URL('../frontend/src/CountryRules.jsx', import.meta.url), 'utf8');
assert.ok(app.includes('const countryBlocked = Boolean(countryCheck?.blocked);'), 'a BLOCK is tracked');
assert.ok(app.includes('const countryHeld = countryBlocked || countryStale;'), 'a cleared Stop still counts until a new check');
assert.ok(app.includes('disabled={disabled || countryHeld || !invoiceChecked'), 'draft context closed on a BLOCK or a stale Stop');
assert.ok(app.includes('disabled={disabled || countryHeld || !invoiceReview'), 'invoice creation closed on a BLOCK or a stale Stop');

// Cross-check 2026-11-03 A1-A3, A6: the redesigned panel and step 01 behaviour stay pinned.
// A1: editing a field after a Stop keeps the Stop (no open draft block, no green step).
assert.ok(app.includes('const sandboxReady = Boolean(aup || countryCheck) && !countryHeld;'), 'sandboxReady formula includes the stale Stop');
assert.ok(app.includes("countryHeld ? { label: 'Draft paused: a listed rule applies', tone: 'danger' }"), 'step status stays "No draft" while a Stop is pending');
assert.ok(app.includes('setCountryStale(!result && stale);'), 'stale only while no new result exists');
assert.ok(panel.includes('onResult?.(null, { stale: stopPendingRef.current })'), 'a field edit reports a pending Stop');
assert.ok(panel.includes('stopPendingRef.current = Boolean(payload.blocked);'), 'each new result resets the pending Stop');
assert.ok(app.includes("'Draft paused: the last country check found a listed rule for this sale. Check again after your change.'"), 'stale Stop explains itself');
// A2: a new result clears a country 409 banner.
assert.ok(app.includes("const COUNTRY_ERROR_CODES = ['country_rules_blocked', 'country_check_changed', 'country_amount_changed'];"), 'country error codes listed');
assert.ok(app.includes('if (result) setError((current) => (COUNTRY_ERROR_CODES.includes(current?.code) ? null : current));'), 'new result clears the country error');
// A3: Reset demo clears the country result and remounts the form.
assert.ok(app.includes('setCountryCheck(null); setCountryStale(false); setCountryResetCount((count) => count + 1);'), 'reset clears the country check');
assert.ok(app.includes('<CountryRules key={`country-${sessionRef.current?.session_id || \'no-session\'}-${countryResetCount}`}'), 'reset remounts the country form');
// Wording (A5, A8, A9) and severity labels.
assert.ok(panel.includes("const SEVERITY_TEXT = { BLOCK: 'Rule match', WARN: 'Check first', INFO: 'Note' };"), 'severity words');
assert.ok(panel.includes('A listed rule may apply to this sale.'), 'verdict is a likelihood, not an order');
// r20 UX-5: the act and article are on screen, not only in the link tooltip.
assert.ok(panel.includes('{statute && <small className="country-statute" data-testid={`country-statute-${row.code}`}>{statute}</small>}'), 'statute shown inline');
assert.ok(!panel.includes("Don't send this order"), 'old imperative verdict removed');
assert.ok(panel.includes('TradeGlot compares PayPal rules with official export and import rules.'), 'intro names TradeGlot and official rules');
assert.ok(!/customs rules|We check/.test(panel), 'no customs-check claim and no "we"');
assert.ok(panel.includes('`Notes (${groups.info.length})`'), 'Note rows and the Notes tab use one word');
// Panel controls keep their test ids.
for (const testId of ['country-continue-draft', 'country-edit-item', 'country-tags-summary', 'country-tags-change', 'country-tags-more',
  'country-no-goods', 'country-key-rules', 'country-more-rules', 'country-good-to-know']) {
  assert.ok(panel.includes(testId), `test id ${testId}`);
}
assert.ok(panel.includes("{accountStop ? 'Change account' : 'Edit item'}"), 'an account Stop points at the account field');
// r14: the phone bar uses the amber verdict's label.
assert.ok(app.includes("label: hasPostalBan(countryCheck) ? 'Continue with another carrier' : 'Continue to draft'"), 'phone bar label matches the verdict');
// Phone click-all r2: the section check has a gap between entering and leaving, hidden in-page buttons keep their
// space, a focused select keeps the action bar, and the guide's Send stays whole.
{ const css = readFileSync(new URL('../frontend/src/index.css', import.meta.url), 'utf8');
  const guideCss = readFileSync(new URL('../frontend/src/GuideLive.css', import.meta.url), 'utf8');
  assert.ok(app.includes("? rules.top < height * 0.7 && rules.bottom > height * 0.2") && app.includes(": rules.top < height * 0.6 && rules.bottom > height * 0.3"), 'section check hysteresis');
  assert.ok(css.includes('.app-shell.phone-action-approve [data-testid="dispute-approve"] { visibility: hidden; }'), 'hidden in-page action keeps its space');
  assert.ok(!/select:focus\)/.test(css), 'a focused select does not hide the action bar');
  assert.ok(guideCss.includes('.guide-live-input > input { flex: 1 1 auto; min-width: 0; }'), 'guide field shrinks, Send stays whole'); }
// Red team r13 P2: a new session starts with no country check.
{ const boot = app.slice(app.indexOf('const bootstrap = useCallback('), app.indexOf("apiRequest('/demo/sessions'", app.indexOf('const bootstrap = useCallback(')));
  assert.ok(boot.includes('setCountryCheck(null); setCountryStale(false);'), 'session restart clears the country check'); }
// Review r13 P0: a postal ban (WARN *_prohibited) turns the verdict amber and sorts above other WARN rows.
assert.ok(panel.includes("const isPostalBan = (row) => row.severity === 'WARN' && /_prohibited$/.test(row.code) && POSTAL_LEAD.test(row.text);"), 'postal bans recognised');
{ // r14 P0: only the post-channel lead turns the verdict amber.
  const lead = new RegExp(panel.match(/const POSTAL_LEAD = \/(.+)\/;/)[1]);
  assert.ok(lead.test('United States import (banned by post; other channels may differ): ENDS devices'), 'post ban');
  assert.ok(!lead.test('Canada import (banned if your item is this kind): Cosmetics that may injure users'), 'subset ban is not postal');
  assert.ok(!lead.test('Japan import (banned for travellers; other channels may differ): x'), 'traveller ban is not postal'); }
assert.ok(panel.includes('The post will not carry this item.') && panel.includes("'is-caution'"), 'amber verdict on a postal ban');
assert.ok(panel.includes("row.severity === 'BLOCK' ? 0 : isPostalBan(row) ? 1"), 'postal bans sort right after stops');
assert.ok(panel.includes('(?:export|import|domestic sale|parcels) \\([^)]*\\)):'), 'scope split only on a country side lead');
// Tablists: arrow keys and roving tabindex.
const tabKeys = readFileSync(new URL('../frontend/src/tabKeys.js', import.meta.url), 'utf8');
assert.ok(tabKeys.includes('ArrowRight: 1') && tabKeys.includes("event.key === 'Home'"), 'tab key handler covers arrows and Home/End');
assert.ok(panel.includes('tabIndex={shown === key ? 0 : -1}'), 'country views use a roving tabindex');
assert.ok(app.includes('tabIndex={velocityView === key ? 0 : -1}'), 'sales views use a roving tabindex');
assert.ok(panel.includes("new Intl.Locale(navigator.language || 'en-US').maximize().region"), 'country preset from the browser language, no location lookup');
assert.ok(!/fetch\(|geoip|ipapi|XMLHttpRequest/i.test(panel), 'no IP or network lookup in the panel');
assert.ok(panel.includes('Not legal advice'), 'panel states the limit');

const session = { session_id: 's', csrf_token: 'c' };
const good = { schema_version: 'payguard.country_rules.v1', seller_country: 'CN', buyer_country: 'TW', cross_border: true, blocked: true,
  findings: [{ severity: 'BLOCK', code: 'personal_account_goods_restricted', text: 'Personal accounts ...', source: 'https://www.paypal.com/c2/legalhub/paypal/useragreement-full' }],
  retrieved_at: '2026-11-02', advisory_only: true, legal_advice: false };
const reply = (payload) => async () => ({ ok: true, status: 200, json: async () => payload });
globalThis.fetch = reply(good);
assert.deepEqual(await apiRequest('/country-rules/check', { method: 'POST', body: {}, session }), good);
const officialImport = { ...good, findings: [...good.findings, { severity: 'WARN', code: 'import_restricted', text: 'Import (restricted): ...', source: 'https://www.fda.gov.tw/Tc/newsContent.aspx?cid=4&id=t623657' }] };
globalThis.fetch = reply(officialImport);
assert.deepEqual(await apiRequest('/country-rules/check', { method: 'POST', body: {}, session }), officialImport, 'official .gov.tw import sources are accepted');
const bad = [
  { ...good, blocked: false },
  { ...good, findings: [{ ...good.findings[0], source: 'https://evil.example/' }] },
  { ...good, findings: [{ ...good.findings[0], source: 'https://gov.tw.evil.example/' }] },
  { ...good, findings: [{ ...good.findings[0], severity: 'DECIDED' }] },
  { ...good, legal_advice: true },
  { ...good, extra: 1 },
];
for (const payload of bad) {
  globalThis.fetch = reply(payload);
  await assert.rejects(apiRequest('/country-rules/check', { method: 'POST', body: {}, session }), (error) => error.code === 'contract_error');
}
// Owner 2026-11-03: country check and shipping country are soft reminders, never a block on the draft.
assert.ok(app.includes('data-testid="invoice-country-reminder"') && app.includes('This does not block the draft.'), 'unchecked route is a reminder');
assert.ok(app.includes('data-testid="invoice-shipping-reminder"') && app.includes("Add the buyer's country in PayPal before you send the invoice."), 'shipping country is a reminder');
console.log(`frontend_country_rules: ok (${bad.length} mutations rejected)`);
