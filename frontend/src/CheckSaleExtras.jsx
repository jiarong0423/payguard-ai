// (P3 2026-11-12) Check a sale, display only: three sample results side by side, the 10-country import / export rule
// grid, the rule chain shown on a result row, and the recorded summary of the Step 01 guide's AI step.
// Every value comes from frontend/src/data/check_sale_examples_v1.json (engines rerun by tests/test_check_sale_p3_data.py)
// or frontend/src/data/country_rules_index_v1.json (a display copy of the rule pack, recounted by
// tests/frontend_check_sale_p3.mjs). Nothing here sends a request or changes a result. Loaded on demand.
// (F 2026-11-12) Source lines from theme/sources.js (same key, same words as Overview, Proof and For judges); they wrap,
// never cut. Dates through theme/format.js. Card buttons sit on one baseline at the foot of each card.
import { useEffect, useRef, useState } from 'react';
import data from './data/check_sale_examples_v1.json';
import { CHANNEL3_READERS, SourceLine } from './theme/sources.js';
import { dateLabel } from './theme/format.js';
import xCircleSvg from './theme/icons/x-circle.svg?raw';
import arrowSvg from './theme/icons/arrow-right.svg?raw';
import fileSvg from './theme/icons/file-text.svg?raw';
import { SpriteIcon, STATUS } from './theme/iconMap.js';
import './ProductReference.css';
import './CheckSaleExtras.css';

// Phosphor icons from theme/icons, drawn at the .tg-icon size (18px).
function PhIcon({ svg }) {
  return <span className="tg-icon check-ph" aria-hidden="true" dangerouslySetInnerHTML={{ __html: svg }} />;
}
// (vteam r6) Status icons from theme/iconMap.js STATUS: risk x-circle on a rule row, check first / review the clock, note the info mark.
const STAMP_ICON = { risk: STATUS.riskNo, warn: STATUS.warn, neutral: STATUS.info };


// The rule pack copy is loaded once, on first use (a result row's chain or a grid cell).
let indexPromise = null;
export function loadRuleIndex() {
  if (!indexPromise) indexPromise = import('./data/country_rules_index_v1.json').then((module) => module.default);
  return indexPromise;
}
function useRuleIndex(wanted = true) {
  const [state, setState] = useState({ index: null, failed: false });
  useEffect(() => {
    if (!wanted) return undefined;
    let live = true;
    loadRuleIndex().then((index) => { if (live) setState({ index, failed: false }); })
      .catch(() => { indexPromise = null; if (live) setState({ index: null, failed: true }); });
    return () => { live = false; };
  }, [wanted]);
  return state;
}
const NAMES = Object.fromEntries(data.rule_grid.countries.map((row) => [row.code, row.name]));
const placeName = (code, names) => (code === '*' ? 'Any country' : names?.[code] || NAMES[code] || code);
const english = (text) => String(text || '').split(/\s+/).filter((word) => !/[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]/u.test(word)).join(' ').trim();
const hostOf = (url) => { try { return new URL(url).hostname.replace(/^www\./u, ''); } catch { return url; } };
const lawOf = (rule) => [english(rule.statute_en) || english(rule.statute), english(rule.article)].filter(Boolean).join(' ');
const TIER_WORD = { prohibited: 'Prohibited', restricted: 'Restricted', general: 'General' };
// What the screen shows for each tier when the server does not soften it (country_rules.TIER_SEVERITY).
const TIER_SHOWN = { prohibited: 'Rule match', restricted: 'Check first', general: 'Note' };
const CHANNEL_WORDS = { post: 'by post', air_mail: 'by air mail', sea: 'by sea', traveller: 'for travellers' };

// A result row matched back to its pack rule: same side (the server's row code starts with import_ or export_; a domestic
// row uses the export list), same source page, and the rule sentence appears in the row text.
const sideOf = (code) => (code.startsWith('import') ? 'import' : 'export');
export const matchRule = (index, row) => (index?.rules || []).filter((rule) => rule.side === sideOf(row.code) && rule.url === row.source && row.text.includes(rule.rule))
  .sort((a, b) => b.rule.length - a.rule.length)[0] || null;

export function RuleChain({ row, tipId, names, result, shownAs, sourceKind }) {
  const { index, failed } = useRuleIndex();
  const rule = matchRule(index, row);
  const [from, to] = rule ? rule.route.split('->') : [result.seller_country, result.buyer_country];
  const tier = rule && TIER_WORD[rule.tier];
  // A channel rule (post only) never decides the whole item, so it shows as Check first by design.
  const level = !rule ? shownAs
    : rule.channel ? `${tier} ${CHANNEL_WORDS[rule.channel] || rule.channel.replace(/_/gu, ' ')} only, other channels may differ`
      : rule.tier === 'prohibited' && shownAs !== TIER_SHOWN.prohibited ? `${tier} for some items of this kind` : tier;
  const items = [
    ['Route', `${placeName(from, names)} → ${placeName(to, names)}${rule ? ` · ${placeName(rule.country, names)} ${rule.side}` : ''}`],
    ['Rule id', rule ? rule.id : failed ? 'Rule details could not be loaded' : index ? `${row.code} (PayPal or account rule, not in the country pack)` : 'Loading…'],
    ['Level', `${level}${rule && shownAs !== TIER_SHOWN[rule.tier] ? ` · shown as ${shownAs}` : ''}`],
    ['Law', rule ? lawOf(rule) || 'Not named on the source page' : sourceKind],
    ['Source', `${rule?.agency ? `${rule.agency} · ` : ''}${hostOf(row.source)} · read ${dateLabel(rule?.retrieved_at || result.retrieved_at)}`],
  ];
  return <span className="tg-tip__body rule-chain" role="tooltip" id={tipId} data-testid="rule-chain" data-rule-id={rule?.id || ''}>
    <b className="rule-chain__title">Why this row</b>
    <dl>{items.map(([term, value]) => <div key={term}><dt>{term}</dt><dd className={term === 'Rule id' && rule ? 'tg-mono' : undefined}>{value}</dd></div>)}</dl>
  </span>;
}

// B. Three sample items, three results; a card's button puts that example in the form through the page's own controls
// (the Quick tests buttons, whose texts are the two descriptions, and "Fill from example"), so no new path is added.
const PICK = { no_match: '.description-presets button:nth-of-type(1)', review_signal: '.description-presets button:nth-of-type(2)', rule_match: '[data-testid="country-try-example"]' };
// (R5 seller 2026-11-12) A short, calm confirmation after a card is used: what happened and the one next press.
const PICKED = {
  description: 'Example added. Press Run Policy Check when you are ready.',
  route: 'Example filled in: United States to Singapore, e-cigarettes. The country check is under way.',
};
function pick(example) {
  const target = document.querySelector(`#compliance ${PICK[example.id]}`);
  target?.click();
  if (example.kind === 'description') window.requestAnimationFrame(() => document.getElementById('description')?.focus());
  return Boolean(target);
}
// (R5 seller) The NO MATCH card leads with plain words; the engine's own sentence stays in the detail line under it.
const PLAIN_RESULT = { no_match: 'Nothing flagged for this item' };
// The detail line never repeats the result line word for word (the NO MATCH card's first sentence).
const restOf = (detail, result) => (detail.startsWith(result) ? detail.slice(result.length).replace(/^[.\s]+/u, '') : detail);
const detailOf = (example) => (PLAIN_RESULT[example.id] ? `${example.result}. ${restOf(example.detail, example.result)}` : restOf(example.detail, example.result));
export function ThreeResults() {
  const [picked, setPicked] = useState(null);
  useEffect(() => {
    if (!picked) return undefined;
    const timer = window.setTimeout(() => setPicked(null), 6000);
    return () => window.clearTimeout(timer);
  }, [picked]);
  // Without a connection the country form is not on the page yet: say so plainly instead of "not ready".
  const offline = () => Boolean(document.querySelector('#compliance [data-testid="country-rules-empty"]'));
  const use = (example) => setPicked(pick(example) ? { kind: example.kind, at: Date.now() }
    : { kind: example.kind === 'route' && offline() ? 'offline' : 'missing', at: Date.now() });
  return <section className="check-three tg-section" data-testid="three-results" aria-labelledby="three-results-title">
    <div className="check-head"><h3 id="three-results-title" className="tg-h3">Three sample sales, three answers</h3>
      <p className="tg-small">The same checks on three sample items. Pick one to try it in the form below.</p></div>
    <div className="check-three__row tg-cards3">
      {data.examples.map((example) => <figure key={example.id} className={`tg-clip tg-clip--fact tg-card--cta check-three__card is-${example.tone}`} data-testid={`three-results-${example.id}`}>
        <figcaption className="tg-clip__kicker"><span className={`tg-stamp tg-stamp--${example.tone}`}><SpriteIcon name={STAMP_ICON[example.tone]} size="sm" />{example.stamp}</span></figcaption>
        <blockquote className="tg-clip__quote">{example.description}</blockquote>
        <p className={example.tone === 'risk' ? 'tg-risk check-three__result' : 'check-three__result'} data-link={example.kind === 'route' ? `law:${example.result}` : undefined} data-link-risk={example.tone === 'risk' ? '' : undefined}>{example.tone === 'risk' && <PhIcon svg={xCircleSvg} />}<span>{PLAIN_RESULT[example.id] || example.result}</span></p>
        <p className="check-three__detail">{detailOf(example)}</p>
        {/* tg-cards3 rows line up across cards: a card without a second rule keeps an empty row. */}
        {example.also ? <p className="check-three__also"><span className="tg-deadline--soon check-three__also-word"><SpriteIcon name={STATUS.warn} size="sm" />{example.also.label}</span> {example.also.statute} · {example.also.detail}</p> : <span className="check-three__also" aria-hidden="true" />}
        <div className="tg-cta check-three__foot"><SourceLine kind="RECOUNTED" source={example.kind === 'route' ? 'country_rules_sg_ecig' : 'policy_check'} />
        <button type="button" className="tg-btn tg-btn--secondary check-three__use" data-testid={`three-results-card-${example.id}`} onClick={() => use(example)}>
          {example.kind === 'route' ? 'Try this route' : 'Try this item'}<PhIcon svg={arrowSvg} /></button></div>
      </figure>)}
    </div>
    <p className="check-three__picked" data-testid="three-results-picked" role="status" aria-live="polite">{picked && <span key={picked.at} className="tg-note check-three__picked-note">
      {picked.kind === 'offline' ? 'The country check opens once the demo connects. Nothing was sent; the result on this card stands meanwhile.'
        : picked.kind === 'missing' ? 'The form is not quite ready. Please try again in a moment.' : PICKED[picked.kind]}</span>}</p>
  </section>;
}

// C. Ten countries x import / export: each cell is a filter for that country's rules on that side.
const TIERS = ['prohibited', 'restricted', 'general'];
const SHOW_FIRST = 6;
function RuleGridBody() {
  const grid = data.rule_grid;
  const [cell, setCell] = useState(null);
  const [tier, setTier] = useState('all');
  const [all, setAll] = useState(false);
  const { index, failed } = useRuleIndex(Boolean(cell));
  const pick = (code, side) => { setCell((current) => (current?.code === code && current?.side === side ? null : { code, side })); setTier('all'); setAll(false); };
  const rows = cell && index ? index.rules.filter((rule) => rule.country === cell.code && rule.side === cell.side) : [];
  const shown = tier === 'all' ? rows : rows.filter((rule) => rule.tier === tier);
  const visible = all ? shown : shown.slice(0, SHOW_FIRST);
  return <section className="check-grid tg-section" data-testid="rule-grid" aria-labelledby="rule-grid-title">
    <div className="check-head"><h3 id="rule-grid-title" className="tg-h3">Rules in the pack: 10 countries, import and export</h3>
      <p className="tg-small">Select a number to list that country's rules for that side.</p></div>
    <div className="tg-ledger check-grid__ledger">
      <table className="tg-ledger__table">
        <thead><tr><th scope="col" className="tg-ledger__ref">Country</th><th scope="col" className="tg-ledger__amt">Import rules</th><th scope="col" className="tg-ledger__amt">Export rules</th></tr></thead>
        <tbody>{grid.countries.map(({ code, name }) => <tr key={code} className={cell?.code === code ? 'is-selected' : undefined}>
          <th scope="row" className="tg-ledger__ref">{name}</th>
          {['import', 'export'].map((side) => <td key={side} className="tg-ledger__amt">
            <button type="button" className="tg-filter check-grid__cell" data-testid={`rule-grid-cell-${code}-${side}`} aria-pressed={cell?.code === code && cell?.side === side}
              aria-label={`${name} ${side}: ${grid.counts[side][code]} rules`} onClick={() => pick(code, side)}>{grid.counts[side][code]}</button></td>)}
        </tr>)}</tbody>
        <tfoot><tr className="tg-ledger__total"><th scope="row" className="tg-ledger__ref">All 10 countries</th>
          <td className="tg-ledger__amt" data-testid="rule-grid-total-import">{grid.totals.import}</td><td className="tg-ledger__amt" data-testid="rule-grid-total-export">{grid.totals.export}</td></tr></tfoot>
      </table>
      <SourceLine kind="RECOUNTED" source="country_rules" testId="rule-grid-source">official pages read {dateLabel(grid.retrieved_at)}</SourceLine>
    </div>
    {cell && <div className="check-grid__list" data-testid="rule-grid-list" aria-live="polite">
      <div className="check-grid__list-head"><strong>{NAMES[cell.code]} {cell.side} · {grid.counts[cell.side][cell.code]} rules</strong>
        <button type="button" className="tg-btn tg-btn--text" data-testid="rule-grid-clear" onClick={() => setCell(null)}>Clear</button></div>
      {failed ? <p className="tg-small" role="alert">The rule list did not load. The counts above still come from the pack; please try again shortly.</p> : !index ? <p className="tg-small">Loading the rules…</p> : <>
        <div className="tg-filters" role="group" aria-label="Filter by level">
          {['all', ...TIERS].map((key) => <button key={key} type="button" className="tg-filter" aria-pressed={tier === key} data-testid={`rule-grid-tier-${key}`}
            onClick={() => { setTier(key); setAll(false); }}>{key === 'all' ? 'All' : TIER_WORD[key]}<span className="tg-filter__n">{key === 'all' ? rows.length : rows.filter((rule) => rule.tier === key).length}</span></button>)}
        </div>
        <ul className="check-grid__rules">{visible.map((rule) => <li key={rule.id}><figure className="tg-clip check-grid__rule">
          <figcaption className="tg-clip__kicker"><span className="tg-mono">{rule.id}</span> · {TIER_WORD[rule.tier]}{rule.channel ? ` ${CHANNEL_WORDS[rule.channel] || rule.channel.replace(/_/gu, ' ')} only` : ''} · {placeName(rule.route.split('->')[0])} → {placeName(rule.route.split('->')[1])}</figcaption>
          <blockquote className="tg-clip__quote tg-clip__quote--ruled">{rule.rule}</blockquote>
          <p className="tg-clip__source" title={`${rule.url} · ${grid.source}:${rule.line}`} data-link={lawOf(rule) ? `law:${lawOf(rule)}` : undefined}>{lawOf(rule) ? `${lawOf(rule)} · ` : ''}<a className="tg-link" href={rule.url} target="_blank" rel="noopener noreferrer">{rule.agency || hostOf(rule.url)}</a> · read {dateLabel(rule.retrieved_at)}</p>
        </figure></li>)}</ul>
        {shown.length > SHOW_FIRST && <button type="button" className="tg-btn tg-btn--secondary tg-btn--sm" data-testid="rule-grid-more" aria-expanded={all} onClick={() => setAll((open) => !open)}>{all ? `Show the first ${SHOW_FIRST}` : `Show all ${shown.length}`}</button>}
      </>}
    </div>}
  </section>;
}

// Step 01 guide: the AI step, made visible with the recorded API round (aggregate scores only; no call is made here).
function openGuide() {
  const trigger = document.querySelector('#guide-live-preflight .optional-trigger');
  if (trigger?.getAttribute('aria-expanded') === 'false') trigger.click();
  trigger?.focus();
}
export function GuideAiCard() {
  const ai = data.guide_ai;
  // (R5 seller 2026-11-12, review_UI5 s3) Test figures are for judges, not part of the seller's form: closed by default,
  // short labels on one baseline. Same values, same source line.
  return <details className="check-ai tg-fold" data-testid="guide-ai-card">
    <summary><span className="check-ai__summary">How the AI step was tested<small className="tg-small">Step 01 guide · recorded run, aggregate scores only</small></span></summary>
    <div className="tg-fold__body check-ai__body">
      <p id="guide-ai-title" className="check-ai__lede">Gemini maps a seller sentence to a form item; fixed rules then validate it and code decides what counts.</p>
      <dl className="check-ai__figures">
        <div><dt>Sentences</dt><dd className="tg-num">{ai.sentences}</dd></div>
        <div><dt>Invalid replies</dt><dd className="tg-num">{ai.format_invalid}</dd></div>
        <div><dt>Fields right</dt><dd className="tg-num">{ai.precision}</dd></div>
        <div><dt>Recall</dt><dd className="tg-num">{ai.recall}</dd></div>
        <div><dt>Confident errors</dt><dd className="tg-num">{ai.confident_wrong}</dd></div>
      </dl>
      <SourceLine kind="RECORDED" source="gemini_guide_runs" testId="guide-ai-source">{ai.model}, policy pre-check</SourceLine>
      <button type="button" className="tg-btn tg-btn--text" data-testid="guide-ai-open" onClick={openGuide}>Try the guide yourself</button>
    </div>
  </details>;
}

// (P3 2026-11-12, owner decision) A product card names its Channel3 category only; the comparison of Channel3's
// category tree with PayPal's AUP is one reference block on the page (Channel3Reference), never part of the result.
export function CategoryReference({ category }) {
  if (!category) return null;
  return <p className="product-card-ref" data-testid="product-card-category-ref">Channel3 category: <strong>{category}</strong></p>;
}

// Channel3 category tree vs PayPal AUP: counts from docs/CHANNEL3_NOTES.md and the published CSV, three CSV rows verbatim.
function Channel3Body() {
  const tree = data.channel3_tree;
  return <section className="check-c3 tg-section" data-testid="channel3-reference" aria-labelledby="channel3-reference-title">
    <figure className="tg-clip check-c3__clip">
      <figcaption className="tg-clip__kicker">Reference, does not change the result</figcaption>
      <h3 id="channel3-reference-title" className="tg-h3">Channel3 category tree vs PayPal AUP</h3>
      <p className="check-c3__count" data-testid="channel3-reference-count"><span className="tg-num">{tree.categories_read.toLocaleString('en-US')}</span> Channel3 categories read once; <span className="tg-num">{tree.mapped}</span> mapped to a PayPal AUP item or a question for the seller.</p>
      <ul className="check-c3__rows">{tree.examples.map((row) => <li key={row.line} data-testid="channel3-reference-row">
        <blockquote className="tg-clip__quote tg-clip__quote--ruled">{row.path}</blockquote>
        <p className="tg-small">{row.paypal_aup_item} · {row.agreement.replace(/^(\d) of 5 readers$/u, '$1 of 5 readers agreed')} · <span title={`${tree.csv}:${row.line}`}>CSV line {row.line}</span></p>
      </li>)}</ul>
      <p className="check-c3__readers" title={CHANNEL3_READERS.title} data-testid="channel3-readers">{CHANNEL3_READERS.text}</p>
      <SourceLine kind="RECORDED" source="channel3_table" testId="channel3-reference-source" />
      <p className="tg-clip__source check-c3__csv"><a className="tg-btn tg-btn--secondary tg-btn--sm" href={tree.csv_url} target="_blank" rel="noopener noreferrer" data-testid="channel3-reference-csv"><PhIcon svg={fileSvg} />Open the {tree.mapped}-row table (CSV)<PhIcon svg={arrowSvg} /></a></p>
    </figure>
  </section>;
}

// (S31 round 6, 2026-11-12) The rule pack table and the Channel3 reference are judge material, not part of the seller's
// form: one fold, closed by default, under the form. It opens itself when the address names it (#rule-pack), so a
// For judges stop or a shared link can point at it. App.jsx still mounts <Channel3Reference />; that slot now draws
// nothing because the reference lives inside this fold (same test ids, same values).
const REF_HASH = '#rule-pack';
export function RuleGrid() {
  const ref = useRef(null);
  useEffect(() => {
    const openIfNamed = () => {
      if (window.location.hash.split('?')[0] !== REF_HASH || !ref.current) return;
      ref.current.open = true;
      ref.current.scrollIntoView({ block: 'start', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    };
    openIfNamed();
    window.addEventListener('hashchange', openIfNamed);
    return () => window.removeEventListener('hashchange', openIfNamed);
  }, []);
  return <details ref={ref} id="rule-pack" className="check-ref tg-fold" data-testid="rule-pack-fold">
    <summary><span className="check-ai__summary">Behind the check: the rule pack and the Channel3 reference<small className="tg-small">{data.rule_grid.totals.import + data.rule_grid.totals.export} official rules by country and side, and how Channel3 categories map to PayPal's policy</small></span></summary>
    <div className="tg-fold__body check-ref__body"><RuleGridBody /><Channel3Body /></div>
  </details>;
}
export function Channel3Reference() {
  return null;
}
