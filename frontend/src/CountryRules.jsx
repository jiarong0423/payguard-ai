import { lazy, Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { SpriteIcon, STATUS } from './theme/iconMap.js';
import { apiRequest, retrySecondsLeft } from './api.js';
import { tabKeyDown } from './tabKeys.js';
import { useWaitClock, waitFailureMessage, WaitLine } from './GuideLive.jsx';
import './CountryRules.css';

// Per-country rules for the seller (ships from) and the buyer (ships to). Both sides pick their own country;
// TradeGlot shows what PayPal's published rules and the official government and postal rules say for that pair, and
// blocks the sale before the invoice draft when a cited rule stops it. Where the pack has them, the seller country's export rules and the buyer country's import
// rules are matched separately (leaving one is not entering the other). Advisory only.
const TAG_LABELS = {
  live_animals: 'Live animals', plants_seeds: 'Plants or seeds', food: 'Food', cosmetics: 'Cosmetics',
  batteries_hazmat: 'Batteries or hazardous', alcohol: 'Alcohol', tobacco_other: 'Tobacco (not e-cigarettes)',
  prescription: 'Prescription items', crypto: 'Crypto', gambling: 'Gambling', medical_devices: 'Medical devices',
  jewellery_precious_metals: 'Jewellery or precious metals', weapons: 'Weapons', counterfeit: 'Possible counterfeit-goods signal',
  narcotics: 'Narcotics', cigarettes: 'Cigarettes', radio_wireless: 'Phones or wireless devices', e_cigarettes: 'E-cigarettes',
  currency: 'Cash or banknotes', cultural_relics: 'Antiques or cultural relics',
};
// Six common categories stay on screen; the rest sit under "More categories" (GLM red team #25). Ticked ones always show.
const COMMON_TAGS = ['e_cigarettes', 'food', 'cosmetics', 'batteries_hazmat', 'alcohol', 'radio_wireless'];
const SHOWN_TAGS = ['live_animals', 'plants_seeds', 'food', 'cosmetics', 'batteries_hazmat', 'radio_wireless', 'alcohol', 'tobacco_other', 'e_cigarettes',
  'prescription', 'medical_devices', 'jewellery_precious_metals', 'currency', 'cultural_relics', 'weapons', 'counterfeit'];
// "Rule match" and "paused", never "held": PayPal uses "hold" for payment holds.
const SEVERITY_TEXT = { BLOCK: 'Rule match', WARN: 'Check first', INFO: 'Note' };
// Review 2026-11-03: a long list buries the rule that matters; show the first few, keep the rest one click away.
const SUMMARY_ROWS = 2;
// Each link says whose rule it is (review r10: government import rules were labelled as PayPal's).
const CARRIER_HOSTS = /^https:\/\/([a-z0-9-]+\.)*(usps\.com|canadapost-postescanada\.ca|royalmail\.com|deutschepost\.de|dhl\.de|japanpost\.jp|singpost\.com|hongkongpost\.hk|auspost\.com\.au|post\.gov\.tw)\//;
const sourceLabel = (url) => (/^https:\/\/(www|developer)\.paypal\.com\//.test(url) ? 'PayPal source'
  : CARRIER_HOSTS.test(url) ? 'Postal operator rule' : 'Official government source');
const plural = (count, word) => `${count} ${word}${count === 1 ? '' : 's'}`;
// Plain-words help for the three terms sellers meet first in the rule sentences; each is explained once per result.
const GLOSSARY = [['EEI', 'the US customs export filing'], ['ENDS', 'e-cigarettes and similar vaping products'], ['nonmailable', 'the post will not carry it']];
function withGloss(sentence, seen) {
  let out = sentence;
  for (const [term, meaning] of GLOSSARY) {
    const match = seen.has(term) ? null : new RegExp(`\\b${term}\\b`).exec(out);
    if (match) { seen.add(term); out = `${out.slice(0, match.index + term.length)} (${meaning})${out.slice(match.index + term.length)}`; }
  }
  return out;
}
// (optimise r24) Clock time for the before/after card ("Paused at 10:02 → No listed rule matched at 10:04"), local 24-hour time.
const clockTime = (ms) => new Date(ms).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
// (vteam r6) The verdict is Check a sale's focus area: one 28px status icon by verdict (theme/iconMap.js STATUS); the
// shape carries the meaning as well as the colour (risk double frame + bar, warn dashed, ok double frame).
const VerdictIcon = ({ tone }) => <SpriteIcon name={STATUS[tone]} size="focus" className="country-verdict-icon" />;
const verdictState = (result) => (result.blocked ? 'is-blocked' : result.findings.some(isPostalBan) ? 'is-caution' : 'is-clear');
const verdictWord = (result) => (result.blocked ? 'Draft paused' : result.findings.some(isPostalBan) ? 'Draft allowed (other carrier)' : 'No listed rule matched');
// A rule row reads "{Country} {side} ({tier}): {rule}. [Statute Article]". The seller reads the plain sentence
// first; the scope and the statute move to a small second line and the source link (review r1 P0.4).
function splitRule(text) {
  let rest = text;
  let statute = '';
  const cite = rest.match(/\s\[([^[\]]+)\]$/);
  if (cite) {
    // English only on screen: words written in Chinese or Japanese (the statute name and article numbers) are dropped
    // here; the pack keeps them and the source link still opens the original page.
    statute = cite[1].split(/\s+/).filter((word) => !/[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]/u.test(word)).join(' ').trim();
    // After the Chinese or Japanese words are gone, a statute can be left as one bracketed English name: show it without the outer pair.
    const wrapped = statute.match(/^\((.*)\)$/u);
    if (wrapped && !/[()]/u.test(wrapped[1].replace(/\([^()]*\)/gu, ''))) statute = wrapped[1].trim();
    rest = rest.slice(0, cite.index);
  }
  // Only a "{Country} export|import|domestic sale|parcels ({tier}):" lead is a scope; a sentence such as "PayPal names GDPR
  // for Germany (EU): keep ..." stays whole (red team 2026-11-03 P2-5).
  const lead = rest.match(/^([^:]{3,120}(?:export|import|domestic sale|parcels) \([^)]*\)):\s+/);
  const scope = lead ? lead[1] : '';
  const sentence = lead ? rest.slice(lead[0].length) : rest;
  return { sentence: sentence.charAt(0).toUpperCase() + sentence.slice(1), scope, statute };
}

function browserRegion(codes) {
  // The browser's language tag carries a region (en-US, zh-TW); no location lookup and no network call.
  try {
    const region = new Intl.Locale(navigator.language || 'en-US').maximize().region;
    return codes.includes(region) ? region : 'US';
  } catch {
    return 'US';
  }
}

// Shape as well as colour tells the three apart (plan r2 E18): octagon = stopped, triangle = check first, circle = note.
const SEV_ICON = {
  BLOCK: <><path d="M8.2 3h7.6L21 8.2v7.6L15.8 21H8.2L3 15.8V8.2Z" /><path d="m9.5 9.5 5 5M14.5 9.5l-5 5" /></>,
  WARN: <><path d="M10.7 4.2a1.5 1.5 0 0 1 2.6 0l7.45 13.3a1.5 1.5 0 0 1-1.3 2.25H4.55a1.5 1.5 0 0 1-1.3-2.25Z" /><path d="M12 9.5v4M12 16.75h.01" /></>,
  INFO: <><circle cx="12" cy="12" r="8.5" /><path d="M12 11v5M12 7.75h.01" /></>,
};
function SevIcon({ severity }) {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{SEV_ICON[severity]}</svg>;
}

// (P3 2026-11-12) Rule chain: hovering or focusing a row's level label shows route, rule id, level, law and source
// (CheckSaleExtras.jsx, loaded on demand with its display copy of the rule pack).
const RuleChain = lazy(() => import('./CheckSaleExtras.jsx').then((module) => ({ default: module.RuleChain })));

// The link reads "Source" on one line; the statute or source kind sits in its tooltip and accessible name (plan r2 C11).
// The act and article also show as a small line of their own, so a viewer can read the act the video names (r20 UX-5).
function Finding({ row, retrievedAt, gloss, chain }) {
  const { sentence, scope, statute } = splitRule(row.text);
  const label = statute ? `Source: ${statute}` : sourceLabel(row.source);
  const tipId = `rule-chain-${chain.key}`;
  // Linked tags (theme/connect.js): the level label, the law and the source of one row share a key; rows citing the
  // same law, and the sample card naming it, share it too.
  const link = { 'data-link': statute ? `law:${statute}` : `row:${chain.key}`, 'data-link-risk': row.severity === 'BLOCK' ? '' : undefined };
  return <li className={`country-finding sev-${row.severity.toLowerCase()}`} data-testid={`country-finding-${row.code}`}>
    <span className="tg-tip country-chain"><button type="button" className="country-sev tg-tip__trigger" data-testid="rule-chain-trigger" aria-describedby={tipId} {...link}><SevIcon severity={row.severity} />{SEVERITY_TEXT[row.severity]}</button>
      <Suspense fallback={null}><RuleChain row={row} tipId={tipId} names={chain.names} result={chain.result} shownAs={SEVERITY_TEXT[row.severity]} sourceKind={sourceLabel(row.source)} /></Suspense></span>
    <span className="country-finding-body"><span>{gloss(sentence)}</span>
      {statute && <small className="country-statute" data-testid={`country-statute-${row.code}`} {...link}>{statute}</small>}
      <small className="country-source-line" title={`${scope ? `${scope} · ` : ''}${row.source}`}>{scope && <span>{scope} · </span>}<a href={row.source} target="_blank" rel="noopener noreferrer" title={label} {...link}
        aria-label={`${label}${scope ? ` (${scope})` : ''}, opens in a new tab`}>Source ↗</a>
        {retrievedAt && <span data-testid="country-row-source-date"> · source read {retrievedAt}</span>}
      </small></span>
  </li>;
}

// (optimise r24) After a Stop, a later check of changed goods or countries that no longer stops the sale shows both
// results with their times, so the unlock is visible (Preflight-style before/after).
function BeforeAfter({ record, names }) {
  const { before, after } = record;
  const route = (entry) => `${names[entry.seller] || entry.seller} → ${names[entry.buyer] || entry.buyer}`;
  const goods = (entry) => (entry.tags.length ? entry.tags.map((tag) => TAG_LABELS[tag] || tag).join(', ') : 'nothing ticked');
  const changes = [];
  if (before.seller !== after.seller || before.buyer !== after.buyer) changes.push(`route ${route(before)} to ${route(after)}`);
  if (before.tags.join() !== after.tags.join()) changes.push(`goods ${goods(before)} to ${goods(after)}`);
  if (before.account !== after.account) changes.push(`account ${before.account} to ${after.account}`);
  return <div className="country-before-after" data-testid="country-before-after">
    <strong data-testid="country-before-after-line">Paused at {clockTime(before.at)} → {after.word} at {clockTime(after.at)}</strong>
    <span className="country-before-after-note" data-testid="country-before-after-note">This compares your declaration only. Changing a declaration does not change what PayPal or a carrier will do.</span>
    <span>{changes.length ? `Changed: ${changes.join('; ')}.` : 'Same details checked again.'} The draft is no longer paused by a country rule.</span>
  </div>;
}

// A postal ban is a WARN (another carrier may take the item), but it must never sit below the fold of a green verdict
// (review r13 P0: China mainland to US with e-cigarettes and alcohol read "No cited rule stops this sale").
// Only a ban on the post itself counts (r14 P0: "banned if your item is this kind" and traveller bans are *_prohibited
// too, so the code alone turned AU to CA cosmetics amber); the server writes this lead for channel bans only.
const POSTAL_LEAD = /\(banned by (post|air mail); other channels may differ\):/;
const isPostalBan = (row) => row.severity === 'WARN' && /_prohibited$/.test(row.code) && POSTAL_LEAD.test(row.text);
// The phone bar repeats the verdict's button, so it needs the same label (r14).
export const hasPostalBan = (result) => Boolean(result && !result.blocked && result.findings?.some(isPostalBan));
const rank = (row) => (row.severity === 'BLOCK' ? 0 : isPostalBan(row) ? 1 : row.severity === 'WARN' ? 2 : row.severity === 'INFO' ? 3 : 4);
function findingsBySeverity(unordered) {
  // Stopping rules first, then postal bans, so the summary rows always show why (GLM red team #11; review r13 P0).
  const findings = [...unordered].sort((a, b) => rank(a) - rank(b));
  return { block: findings.filter((row) => row.severity === 'BLOCK'), warn: findings.filter((row) => row.severity === 'WARN'),
    ban: findings.filter(isPostalBan),
    info: findings.filter((row) => row.severity === 'INFO'), action: findings.filter((row) => row.severity !== 'INFO') };
}

// A muted line under the source lines (not in the verdict, where it read as "the check was not done"): how the rules were checked
// is on the Proof page, so no audit numbers sit on this screen.
function LineCheckNote() {
  return <small className="country-footnote country-line-check-note" data-testid="country-verdict-line-check">
    See <a href="/proof.html">Proof</a> for how the rules were checked.</small>;
}

// One big line, then the count line (review r1 P0.3; wording per the PayPal-side red teams: the block may come from a
// government, postal or PayPal rule, so the big line names no country).
function Verdict({ result, names, tags, onEdit, onContinue }) {
  // An account rule (not the goods) can be what stops the sale; the button then opens the account field instead.
  const accountStop = result.findings.some((row) => row.severity === 'BLOCK' && row.code === 'personal_account_goods_restricted');
  const { block, warn, ban } = findingsBySeverity(result.findings);
  const seller = names[result.seller_country];
  const buyer = names[result.buyer_country];
  const noGoods = tags.length === 0 && <span className="country-verdict-line" data-testid="country-no-goods">No goods ticked: account and shipping rules only.</span>;
  // One next step under the verdict (plan r2 E19): change the goods after a Stop, or go on to the draft.
  if (result.blocked) {
    return <><strong className="country-verdict-big"><VerdictIcon tone="risk" />A listed rule may apply to this sale.</strong>
      <span className="country-verdict-line">Draft paused: {plural(block.length, 'listed rule')} {block.length === 1 ? 'applies' : 'apply'} to {seller} → {buyer}.</span>{noGoods}
      <span className="country-verdict-next"><button type="button" className="button button-secondary" data-testid="country-edit-item" onClick={() => onEdit(accountStop)}>{accountStop ? 'Change account' : 'Edit item'}</button></span></>;
  }
  if (ban.length) {
    return <><strong className="country-verdict-big"><VerdictIcon tone="warn" />The post will not carry this item.</strong>
      <span className="country-verdict-line">{plural(ban.length, 'postal rule')} ban{ban.length === 1 ? 's' : ''} it {seller} → {buyer}; another carrier may differ{warn.length > ban.length ? ` · ${warn.length - ban.length} more to check` : ''}. Not a legal clearance.</span>{noGoods}
      <span className="country-verdict-next"><button type="button" className="button button-secondary" data-testid="country-continue-draft" onClick={onContinue}>Continue with another carrier</button></span></>;
  }
  return <><strong className="country-verdict-big"><VerdictIcon tone="ok" />No cited rule applies to this sale.</strong>
    <span className="country-verdict-notclear" data-testid="country-not-clearance">This is not clearance. Only the listed country and PayPal rules were checked; payment type, address match and carrier limits are not covered.</span>
    <span className="country-verdict-line">{result.cross_border ? 'Cross-border' : 'Domestic'}, {seller} → {buyer}{warn.length ? ` · ${warn.length} to check first` : ''}. Not a legal clearance; PayPal's Acceptable Use Policy still applies.</span>{noGoods}
    <span className="country-verdict-next"><button type="button" className="button button-secondary" data-testid="country-continue-draft" onClick={onContinue}>Continue to draft</button></span></>;
}

// Optional amount: empty, or above 0 with at most two decimals (the backend pattern is 1-9 digits, two decimals). Checked
// before sending, so -5, abc, 1e309, 10.001 and 45.6.7 get a field message, not a generic 422 (attack r21 phone #5).
const AMOUNT = /^[0-9]{1,9}(\.[0-9]{1,2})?$/;
export const countryAmountProblem = (value) => {
  const text = String(value || '').trim();
  if (!text) return '';
  return AMOUNT.test(text) && Number(text) > 0 ? '' : 'Enter an amount above 0 like 120 or 120.50 (at most two decimals), or leave it empty.';
};
const SESSION_EXPIRED_TEXT = 'The demo session has ended. Nothing was sent. Select Reconnect at the top of the page to begin a fresh one.';

// "Try the example" (judge self-test): ships from the United States to Singapore with E-cigarettes ticked, then runs the
// same local rules check as the Check country rules button. No other request kind, no PayPal call, no model call.
export const EXAMPLE_ROUTE = Object.freeze({ seller_country: 'US', buyer_country: 'SG', goods_tags: Object.freeze(['e_cigarettes']) });

// (P3 2026-11-12, judges' consensus) The page opens on the example's RULE MATCH, like Overview card 01: the first time
// the Check a sale page is shown in a page load, the existing "Fill from example" runs once (same request, same rules).
let autoExampleDone = false;

export default function CountryRules({ session, onResult, onContinue, onSessionExpired, onBusy, onExample, autoExample = false, verdictTarget = null }) {
  const [catalog, setCatalog] = useState(null);
  const [unavailable, setUnavailable] = useState(false);
  const [form, setForm] = useState(null);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [moreTags, setMoreTags] = useState(false);
  // After a result the goods collapse to one line; "Change" opens them again (plan r2 B6).
  const [tagsOpen, setTagsOpen] = useState(false);
  // Result rows: one view at a time instead of stacked disclosures (plan r2 B7).
  const [view, setView] = useState('key');
  const tagsRef = useRef(null);
  const resultRef = useRef(null);
  const formRef = useRef(null);
  // Set while the last result was a Stop and no new check has run since (red team 2026-11-03 P1-1): editing a field
  // clears the result, but the server still holds the Stop, so the console must not read that as "clear".
  const stopPendingRef = useRef(false);
  // A check still in flight when this panel unmounts (Reset demo remounts it) or when a newer check starts must not
  // write its old result back (attack r21 desktop #1: a late Stop locked the draft after Reset).
  const liveRef = useRef(true);
  const runTokenRef = useRef(0);
  // True when the result being shown came from "Try the example": the page then scrolls the result to the top of the screen.
  const exampleRef = useRef(false);
  // The automatic example on page entry does not scroll the page; autoRef holds the current tryExample.
  const quietRef = useRef(false);
  const autoRef = useRef(null);
  const [amountNote, setAmountNote] = useState('');
  // (optimise r24) The last Stop (route, goods, time) and, once a later check no longer stops the sale, that result:
  // { before, after } drives the before/after card. A new Stop replaces it.
  const [unlock, setUnlock] = useState(null);
  // (attack r23) A 429/503 with Retry-After holds Check country rules until then (epoch ms; 0 = no wait) and the
  // message counts down; the phone bar's Check country rules clicks this same button, so it is held too.
  const [waitUntil, setWaitUntil] = useState(0);
  const now = useWaitClock(waitUntil);
  const waiting = waitUntil > now;
  // The country list itself got a 429/503: load it again once, after the wait.
  const [catalogTry, setCatalogTry] = useState(0);
  useEffect(() => { liveRef.current = true; return () => { liveRef.current = false; runTokenRef.current += 1; }; }, []);
  // The console's phone bar repeats Check country rules, so it shows the same loading state (attack r22 phone #5).
  useEffect(() => { onBusy?.(busy); }, [busy]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => onBusy?.(false), []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!session) return undefined;
    let live = true;
    let retryTimer = 0;
    apiRequest('/country-rules/countries', { session }).then((payload) => {
      if (!live) return;
      setCatalog(payload);
      const codes = payload.countries.map((row) => row.code);
      const home = browserRegion(codes);
      // (optimise r24) Ships to starts on another country than Ships from: the United States, or Canada when the
      // browser region is already the United States (first other country if neither is in the list).
      const away = [home === 'US' ? 'CA' : 'US', ...codes].find((code) => code !== home && codes.includes(code)) || home;
      setForm({ seller_country: home, buyer_country: away, account_type: 'business', account_opened: 'unknown',
        checkout: 'paypal_account', amount: '', currency: 'USD', goods_tags: [] });
    }).catch((failure) => {
      if (!live) return;
      // Only a missing route means this build has no country rules; anything else is a real error to show.
      if (failure.status === 404) setUnavailable(true);
      else if (failure.status === 401) { setError(SESSION_EXPIRED_TEXT); onSessionExpired?.(failure, session); }
      else {
        setError(waitFailureMessage(failure, 'The country list did not load. Nothing was sent; please try again shortly.'));
        if (retrySecondsLeft(failure) && catalogTry === 0) {
          setWaitUntil(failure.retryAt);
          retryTimer = window.setTimeout(() => { if (live) { setError(''); setCatalogTry(1); } }, failure.retryAt - Date.now());
        }
      }
    });
    return () => { live = false; window.clearTimeout(retryTimer); onResult?.(null); };
  }, [session, catalogTry]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!autoExample || !catalog || !form || autoExampleDone) return;
    autoExampleDone = true;
    quietRef.current = true;
    autoRef.current?.();
  }, [autoExample, catalog, form]);
  // Bring the verdict on screen (above the phone action bar) once it arrives (review r1 P0.3).
  useEffect(() => {
    if (!result) return;
    if (quietRef.current) { quietRef.current = false; exampleRef.current = false; return; }
    window.requestAnimationFrame(() => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const fromExample = exampleRef.current;
      exampleRef.current = false;
      resultRef.current?.scrollIntoView({ block: fromExample ? 'start' : 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
    });
  }, [result]);

  const names = useMemo(() => Object.fromEntries((catalog?.countries || []).map((row) => [row.code, row.name])), [catalog]);
  if (unavailable) return <p className="text-dim" data-testid="country-rules-unavailable">Country rules are not part of this build.</p>;
  // (R5 seller 2026-11-12, review_UI5 s3 #1) Never an empty column: until the country list arrives, the card keeps its
  // title and says what happens next (or shows the error with its wait line).
  if (!catalog || !form) {
    return <section className="country-rules country-rules--empty" data-testid="country-rules-empty" aria-labelledby="country-rules-title" aria-busy={Boolean(session && !error) || undefined}>
      <div className="country-rules-head">
        <h3 id="country-rules-title">Where are you shipping from and to?</h3>
        <p>TradeGlot compares PayPal rules with official export and import rules.</p>
      </div>
      {error ? <p className="guide-live-error" role="alert">{error}<WaitLine until={waitUntil} now={now} testId="country-wait" /></p>
        : <p className="country-empty-note" data-testid="country-rules-empty-note">{session ? 'One moment: fetching the country list.'
          : 'Not connected yet. The country check opens as soon as the demo connects; until then, the e-cigarettes card above shows what it finds for United States to Singapore.'}</p>}
    </section>;
  }

  const set = (key, value) => { setForm((current) => ({ ...current, [key]: value })); setResult(null); onResult?.(null, { stale: stopPendingRef.current });
    if (key === 'amount' && !countryAmountProblem(value)) setAmountNote(''); };
  const toggleTag = (tag) => set('goods_tags', form.goods_tags.includes(tag) ? form.goods_tags.filter((item) => item !== tag) : [...form.goods_tags, tag]);
  const run = () => runCheck(form);
  const tryExample = () => {
    if (busy || Date.now() < waitUntil) return;
    const codes = catalog.countries.map((row) => row.code);
    if (!codes.includes(EXAMPLE_ROUTE.seller_country) || !codes.includes(EXAMPLE_ROUTE.buyer_country)) {
      setError('The example needs the United States and Singapore, which this build does not list. Pick the countries yourself.');
      return;
    }
    const next = { ...form, ...EXAMPLE_ROUTE, goods_tags: [...EXAMPLE_ROUTE.goods_tags] };
    setForm(next);
    setAmountNote('');
    exampleRef.current = true;
    onExample?.();
    runCheck(next);
  };
  autoRef.current = tryExample;
  async function runCheck(values) {
    // aria-disabled while running: the button keeps keyboard focus (review r1 P0.7). Also while a Retry-After runs.
    if (busy || Date.now() < waitUntil) return;
    const amountProblem = countryAmountProblem(values.amount);
    if (amountProblem) {
      setAmountNote(amountProblem);
      const details = formRef.current?.querySelector('details.country-optional');
      if (details) details.open = true;
      // attack r22 phone #6: bring the message into view; on a touch screen the field is not focused, because the
      // keyboard it opens covered half of the message. The next frame or 50 ms, whichever comes first.
      let done = false;
      const show = () => {
        if (done) return;
        done = true;
        if (!window.matchMedia('(pointer: coarse)').matches) document.getElementById('country-amount-input')?.focus({ preventScroll: true });
        document.getElementById('country-amount-note')?.scrollIntoView({ block: 'center' });
      };
      window.requestAnimationFrame(show);
      window.setTimeout(show, 50);
      return;
    }
    const token = ++runTokenRef.current;
    const current = () => liveRef.current && token === runTokenRef.current;
    setBusy(true);
    setError('');
    setWaitUntil(0);
    try {
      const body = { ...values, amount: values.amount.trim() || null, currency: values.amount.trim() ? values.currency : null };
      const payload = await apiRequest('/country-rules/check', { method: 'POST', body, session });
      if (!current()) return;
      stopPendingRef.current = Boolean(payload.blocked);
      // (optimise r24) Record the Stop, or pair a later non-stop result with the last Stop.
      const entry = { at: Date.now(), seller: payload.seller_country, buyer: payload.buyer_country, tags: [...values.goods_tags].sort(),
        account: values.account_type, word: verdictWord(payload) };
      setUnlock((current) => (payload.blocked ? { before: entry, after: null } : current ? { before: current.before, after: entry } : null));
      setResult({ ...payload, checked_tags: [...values.goods_tags] });
      setTagsOpen(false);
      setView('key');
      onResult?.(payload);
    } catch (failure) {
      if (!current()) return;
      if (failure.status === 401) { setError(SESSION_EXPIRED_TEXT); onSessionExpired?.(failure, session); return; }
      if (retrySecondsLeft(failure)) setWaitUntil(failure.retryAt);
      setError(waitFailureMessage(failure, 'That check did not go through. Nothing was sent; please try again.'));
    } finally {
      if (liveRef.current && token === runTokenRef.current) setBusy(false);
    }
  }

  const select = (key, label, options, className = '') => <label className={`country-field ${className}`}>{label}
    <select data-testid={`country-${key}`} value={form[key]} disabled={busy} onChange={(event) => set(key, event.target.value)}>
      {options.map(([value, text]) => <option key={value} value={value}>{text}</option>)}
    </select></label>;
  const countryOptions = catalog.countries.map((row) => [row.code, row.name]);
  const groups = result ? findingsBySeverity(result.findings) : null;
  const views = groups ? [
    ['key', 'Key rules', 'country-key-tab'],
    ...(groups.action.length > SUMMARY_ROWS ? [['all', `All rules (${groups.action.length})`, 'country-more-rules']] : []),
    // Same word as the row label "Note" (red team 2026-11-03 P2-3).
    ...(groups.info.length > 0 ? [['info', `Notes (${groups.info.length})`, 'country-good-to-know']] : []),
  ] : [];
  // Key rules always show; the rest (all rules, notes) sit in one closed "See all rules and notes" fold.
  const foldViews = views.filter(([key]) => key !== 'key');
  const shown = foldViews.some(([key]) => key === view) ? view : foldViews[0]?.[0];
  const keyRows = !groups ? [] : groups.action.slice(0, SUMMARY_ROWS);
  const foldRows = !groups ? [] : shown === 'info' ? groups.info : groups.action;
  const editItem = (account = false) => {
    if (account) {
      const details = formRef.current?.querySelector('details.country-optional');
      if (details) details.open = true;
      window.requestAnimationFrame(() => formRef.current?.querySelector('[data-testid="country-account_type"]')?.focus());
      return;
    }
    setTagsOpen(true);
    window.requestAnimationFrame(() => tagsRef.current?.querySelector('input')?.focus());
  };
  // "Change" unmounts itself; focus moves to the first goods box instead of dropping to the page (click-all #5).
  const changeTags = () => editItem(false);
  const tagChip = (tag) => <label key={tag} className={`country-tag ${form.goods_tags.includes(tag) ? 'is-on' : ''}`}>
    <input type="checkbox" data-testid={`country-tag-${tag}`} checked={form.goods_tags.includes(tag)} disabled={busy} onChange={() => toggleTag(tag)} />
    {TAG_LABELS[tag]}
  </label>;
  const extraTags = SHOWN_TAGS.filter((tag) => !COMMON_TAGS.includes(tag));
  const visibleExtra = moreTags ? extraTags : extraTags.filter((tag) => form.goods_tags.includes(tag));

  return <section className="country-rules" data-testid="country-rules" aria-labelledby="country-rules-title">
    <div className="country-rules-head">
      <h3 id="country-rules-title">Where are you shipping from and to?</h3>
      <p>TradeGlot compares PayPal rules with official export and import rules.</p>
      <button type="button" className="button button-secondary country-try-example" data-testid="country-try-example" aria-disabled={busy || waiting || undefined}
        title="Fills United States to Singapore with E-cigarettes ticked and runs the same check" onClick={tryExample}>Fill from example</button>
      <small className="country-try-note" data-testid="country-try-note">United States to Singapore, e-cigarettes. Synthetic data, no PayPal calls; fills the form and runs the check.</small>
    </div>
    <div className="country-form" ref={formRef}>
      <div className="country-places">
        <div className="country-grid">
          {select('seller_country', 'Ships from', countryOptions, 'country-field-place')}
          {select('buyer_country', 'Ships to', countryOptions, 'country-field-place')}
        </div>
        <details className="country-optional" data-testid="country-more-details">
          <summary><span>More details (optional)</span></summary>
          <div className="country-grid">
            {select('account_type', 'Seller account', [['business', 'Business'], ['personal', 'Personal']])}
            {form.account_type === 'personal' && form.seller_country === 'CN' && select('account_opened', 'Account opened', [['unknown', 'Not sure'], ['before_cutoff', 'Before 30 Jun 2026'], ['after_cutoff', 'After 30 Jun 2026']])}
            {select('checkout', 'How the buyer pays', [['paypal_account', 'PayPal account'], ['guest_card', 'Guest or card']])}
            <div className="country-field">
              <label htmlFor="country-amount-input">Amount</label>
              <span className="country-amount">
                {/* Typed text is kept as typed (stripping "-" turned -1 into 1 silently) and checked on Check (attack r21). */}
                <input id="country-amount-input" data-testid="country-amount" inputMode="decimal" maxLength={12} value={form.amount} disabled={busy}
                  aria-invalid={amountNote ? true : undefined} aria-describedby={amountNote ? 'country-amount-note' : undefined}
                  onChange={(event) => set('amount', event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter') { event.preventDefault(); run(); } }} placeholder="e.g. 120" />
                <select data-testid="country-currency" aria-label="Currency" value={form.currency} disabled={busy} onChange={(event) => set('currency', event.target.value)}>
                  {['USD', 'TWD', 'HKD', 'GBP', 'EUR', 'JPY', 'SGD', 'AUD', 'CAD'].map((code) => <option key={code} value={code}>{code}</option>)}
                </select>
              </span>
              {amountNote && <small id="country-amount-note" className="country-field-note" role="alert" data-testid="country-amount-note">{amountNote}</small>}
            </div>
          </div>
        </details>
      </div>
      {result && !tagsOpen ? <p className="country-tags-summary" data-testid="country-tags-summary"><span className="country-tags-picked">Selling: <strong>{result.checked_tags.length ? result.checked_tags.map((tag) => TAG_LABELS[tag]).join(', ') : 'nothing ticked'}</strong></span>
        <button type="button" className="country-link-button" data-testid="country-tags-change" onClick={changeTags}>Change</button></p>
      : <fieldset className="country-tags" ref={tagsRef}>
        <legend>What are you selling? (tick any)</legend>
        {COMMON_TAGS.map(tagChip)}
        {visibleExtra.map(tagChip)}
        <button type="button" className="country-link-button" data-testid="country-tags-more" aria-expanded={moreTags} onClick={() => setMoreTags((open) => !open)}>
          {moreTags ? 'Fewer categories' : `More categories (${extraTags.length})`}</button>
      </fieldset>}
    </div>
    <button type="button" className={`button button-secondary${waiting ? ' is-blocked' : ''}`} data-testid="country-check" aria-disabled={busy || waiting || undefined} aria-busy={busy} onClick={run}>{busy ? 'Checking…' : 'Check country rules'}</button>
    {error && <p className="guide-live-error" role="alert">{error}<WaitLine until={waitUntil} now={now} testId="country-wait" /></p>}
    <div className="country-live" aria-live="polite">
    {result && <div ref={resultRef} tabIndex={-1} className={`country-result ${verdictState(result)}`} data-testid="country-result">
      {(() => {
        // (R5 2026-11-12) With a slot from the page (under the three sample cards) the verdict is drawn there; the
        // wrapper repeats the state class so the same .country-result.is-* colours apply. Same Verdict, same test ids.
        const verdict = <div className="country-verdict" data-testid="country-verdict"><Verdict result={result} names={names} tags={result.checked_tags} onEdit={editItem} onContinue={onContinue} /></div>;
        return verdictTarget ? createPortal(<div className={`country-result country-result--portal tg-focus ${verdictState(result)}`} data-testid="country-verdict-focus">{verdict}</div>, verdictTarget) : verdict;
      })()}
      {!result.blocked && unlock?.after && <BeforeAfter record={unlock} names={names} />}
      {(() => {
        const seen = new Set();
        const list = (items, where) => <ul>{items.map((row, at) => <Finding key={`${row.code}-${row.text}`} row={row} retrievedAt={result.retrieved_at} gloss={(text) => withGloss(text, seen)}
          chain={{ key: `${where}-${at}`, names, result }} />)}</ul>;
        return <>
          <div id="country-view-rows" data-testid="country-key-rules">
            {keyRows.length > 0 ? list(keyRows, 'key') : <p className="country-footnote">No rule to check first.</p>}
          </div>
          {foldViews.length > 0 && <details className="sandbox-details country-all-rules" data-testid="country-all-rules"><summary>See all rules and notes</summary>
            <div className="segmented" role="tablist" aria-label="Which rules to show"
              onKeyDown={(event) => tabKeyDown(event, foldViews.map(([key]) => key), shown, setView, (key) => `country-view-${key}`)}>
              {foldViews.map(([key, label, testId]) => <button key={key} type="button" role="tab" id={`country-view-${key}`} data-testid={testId} aria-selected={shown === key} tabIndex={shown === key ? 0 : -1} aria-controls="country-view-fold" className={shown === key ? 'is-active' : ''} onClick={() => setView(key)}>{label}</button>)}
            </div>
            <div id="country-view-fold" role="tabpanel" aria-labelledby={`country-view-${shown}`}>{list(foldRows, shown)}</div>
          </details>}
        </>;
      })()}
      <small className="country-footnote">Paraphrased from official pages, {result.retrieved_at}. Not legal advice.</small>
      <LineCheckNote />
    </div>}
    </div>
  </section>;
}
