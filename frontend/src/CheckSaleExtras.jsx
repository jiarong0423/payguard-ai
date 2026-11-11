// (P3 2026-11-12) Check a sale, display only: three sample results side by side, the 10-country import / export rule
// grid, the rule chain shown on a result row, and the recorded summary of the Step 01 guide's AI step.
// Every value comes from frontend/src/data/check_sale_examples_v1.json (engines rerun by tests/test_check_sale_p3_data.py)
// or frontend/src/data/country_rules_index_v1.json (a display copy of the rule pack, recounted by
// tests/frontend_check_sale_p3.mjs). Nothing here sends a request or changes a result. Loaded on demand.
import { useEffect, useState } from 'react';
import data from './data/check_sale_examples_v1.json';
import warningSvg from './theme/icons/warning.svg?raw';
import xCircleSvg from './theme/icons/x-circle.svg?raw';
import infoSvg from './theme/icons/info.svg?raw';
import arrowSvg from './theme/icons/arrow-right.svg?raw';
import './ProductReference.css';
import './CheckSaleExtras.css';

// Phosphor icons from theme/icons, drawn at the .tg-icon size (18px).
function PhIcon({ svg }) {
  return <span className="tg-icon check-ph" aria-hidden="true" dangerouslySetInnerHTML={{ __html: svg }} />;
}
const STAMP_ICON = { risk: xCircleSvg, warn: warningSvg, neutral: infoSvg };

// One source line everywhere: LABEL · plain words; the full path sits in the title.
function Source({ label, title, children, testId }) {
  return <p className="tg-source check-source" title={title} data-testid={testId}><span className="tg-source__label">{label}</span><span>· {children}</span></p>;
}

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
    ['Source', `${rule?.agency ? `${rule.agency} · ` : ''}${hostOf(row.source)} · read ${rule?.retrieved_at || result.retrieved_at}`],
  ];
  return <span className="tg-tip__body rule-chain" role="tooltip" id={tipId} data-testid="rule-chain" data-rule-id={rule?.id || ''}>
    <b className="rule-chain__title">Why this row</b>
    <dl>{items.map(([term, value]) => <div key={term}><dt>{term}</dt><dd className={term === 'Rule id' && rule ? 'tg-mono' : undefined}>{value}</dd></div>)}</dl>
  </span>;
}

// B. Three sample items, three results; a card's button puts that example in the form through the page's own controls
// (the Quick tests buttons, whose texts are the two descriptions, and "Fill from example"), so no new path is added.
const PICK = { no_match: '.description-presets button:nth-of-type(1)', review_signal: '.description-presets button:nth-of-type(2)', rule_match: '[data-testid="country-try-example"]' };
function pick(example) {
  document.querySelector(`#compliance ${PICK[example.id]}`)?.click();
  if (example.kind === 'description') window.requestAnimationFrame(() => document.getElementById('description')?.focus());
}
export function ThreeResults() {
  return <section className="check-three tg-section" data-testid="three-results" aria-labelledby="three-results-title">
    <div className="check-head"><h3 id="three-results-title" className="tg-h3">Three items, three results</h3>
      <p className="tg-small">The same checks on three sample items. Use a card to put its example in the form below.</p></div>
    <div className="check-three__row">
      {data.examples.map((example) => <figure key={example.id} className={`tg-clip tg-clip--fact check-three__card is-${example.tone}`} data-testid={`three-results-${example.id}`}>
        <figcaption className="tg-clip__kicker"><span className={`tg-stamp tg-stamp--${example.tone}`}><PhIcon svg={STAMP_ICON[example.tone]} />{example.stamp}</span></figcaption>
        <blockquote className="tg-clip__quote">{example.description}</blockquote>
        <p className={example.tone === 'risk' ? 'tg-risk check-three__result' : 'check-three__result'} data-link={example.kind === 'route' ? `law:${example.result}` : undefined} data-link-risk={example.tone === 'risk' ? '' : undefined}>{example.tone === 'risk' && <PhIcon svg={xCircleSvg} />}<span>{example.result}</span></p>
        <p className="check-three__detail">{example.detail}</p>
        {example.also && <p className="check-three__also"><span className="tg-deadline--soon check-three__also-word"><PhIcon svg={warningSvg} />{example.also.label}</span> {example.also.statute} · {example.also.detail}</p>}
        <Source label="RECOUNTED" title={example.source}>{example.kind === 'route' ? 'country rules check, rerun in tests' : 'policy check, rerun in tests'}</Source>
        <button type="button" className="tg-btn tg-btn--secondary tg-btn--sm check-three__use" data-testid={`three-results-card-${example.id}`} onClick={() => pick(example)}>
          {example.kind === 'route' ? 'Fill the country form' : 'Put in the description'}<PhIcon svg={arrowSvg} /></button>
      </figure>)}
    </div>
  </section>;
}

// C. Ten countries x import / export: each cell is a filter for that country's rules on that side.
const TIERS = ['prohibited', 'restricted', 'general'];
const SHOW_FIRST = 6;
export function RuleGrid() {
  const grid = data.rule_grid;
  const [cell, setCell] = useState(null);
  const [tier, setTier] = useState('all');
  const [all, setAll] = useState(false);
  const { index, failed } = useRuleIndex(Boolean(cell));
  const pick = (code, side) => { setCell((current) => (current?.code === code && current?.side === side ? null : { code, side })); setTier('all'); setAll(false); };
  const rows = cell && index ? index.rules.filter((rule) => rule.country === cell.code && rule.side === cell.side) : [];
  const shown = tier === 'all' ? rows : rows.filter((rule) => rule.tier === tier);
  const visible = all ? shown : shown.slice(0, SHOW_FIRST);
  const file = grid.source.split('/').pop();
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
      <Source label="RECOUNTED" title={`${grid.source} (recounted by tests/frontend_check_sale_p3.mjs)`} testId="rule-grid-source">{file}, official pages read {grid.retrieved_at}</Source>
    </div>
    {cell && <div className="check-grid__list" data-testid="rule-grid-list" aria-live="polite">
      <div className="check-grid__list-head"><strong>{NAMES[cell.code]} {cell.side} · {grid.counts[cell.side][cell.code]} rules</strong>
        <button type="button" className="tg-btn tg-btn--text" data-testid="rule-grid-clear" onClick={() => setCell(null)}>Clear</button></div>
      {failed ? <p className="tg-small" role="alert">The rule list could not be loaded. The counts above still come from the pack.</p> : !index ? <p className="tg-small">Loading the rules…</p> : <>
        <div className="tg-filters" role="group" aria-label="Filter by level">
          {['all', ...TIERS].map((key) => <button key={key} type="button" className="tg-filter" aria-pressed={tier === key} data-testid={`rule-grid-tier-${key}`}
            onClick={() => { setTier(key); setAll(false); }}>{key === 'all' ? 'All' : TIER_WORD[key]}<span className="tg-filter__n">{key === 'all' ? rows.length : rows.filter((rule) => rule.tier === key).length}</span></button>)}
        </div>
        <ul className="check-grid__rules">{visible.map((rule) => <li key={rule.id}><figure className="tg-clip check-grid__rule">
          <figcaption className="tg-clip__kicker"><span className="tg-mono">{rule.id}</span> · {TIER_WORD[rule.tier]}{rule.channel ? ` ${CHANNEL_WORDS[rule.channel] || rule.channel.replace(/_/gu, ' ')} only` : ''} · {placeName(rule.route.split('->')[0])} → {placeName(rule.route.split('->')[1])}</figcaption>
          <blockquote className="tg-clip__quote">{rule.rule}</blockquote>
          <p className="tg-clip__source" title={`${rule.url} · ${grid.source}:${rule.line}`} data-link={lawOf(rule) ? `law:${lawOf(rule)}` : undefined}>{lawOf(rule) ? `${lawOf(rule)} · ` : ''}<a className="tg-link" href={rule.url} target="_blank" rel="noopener noreferrer">{rule.agency || hostOf(rule.url)}</a> · read {rule.retrieved_at}</p>
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
  return <section className="check-ai tg-section" data-testid="guide-ai-card" aria-labelledby="guide-ai-title">
    <p className="tg-eyebrow">Step 01 guide · AI step</p>
    <h3 id="guide-ai-title" className="tg-h3">Gemini maps a seller sentence to a form item; fixed rules then validate it and code decides what counts.</h3>
    <dl className="check-ai__figures">
      <div><dt>Seller sentences sent</dt><dd className="tg-num">{ai.sentences}</dd></div>
      <div><dt>Replies refused for format</dt><dd className="tg-num">{ai.format_invalid}</dd></div>
      <div><dt>Filled fields that were right</dt><dd className="tg-num">{ai.precision}</dd></div>
      <div><dt>Recall</dt><dd className="tg-num">{ai.recall}</dd></div>
      <div><dt>Confident wrong</dt><dd className="tg-num">{ai.confident_wrong}</dd></div>
    </dl>
    <Source label="RECORDED" title={`${ai.source}:${ai.line}`} testId="guide-ai-source">Gemini API run {ai.date}, {ai.model}, policy pre-check</Source>
    <button type="button" className="tg-btn tg-btn--text" data-testid="guide-ai-open" onClick={openGuide}>Open the Step 01 guide</button>
  </section>;
}

// (P3 2026-11-12, owner decision) A product card names its Channel3 category only; the comparison of Channel3's
// category tree with PayPal's AUP is one reference block on the page (Channel3Reference), never part of the result.
export function CategoryReference({ category }) {
  if (!category) return null;
  return <p className="product-card-ref" data-testid="product-card-category-ref">Channel3 category: <strong>{category}</strong></p>;
}

// Channel3 category tree vs PayPal AUP: counts from docs/CHANNEL3_NOTES.md and the published CSV, three CSV rows verbatim.
export function Channel3Reference() {
  const tree = data.channel3_tree;
  const file = tree.csv.split('/').pop();
  return <section className="check-c3 tg-section" data-testid="channel3-reference" aria-labelledby="channel3-reference-title">
    <figure className="tg-clip check-c3__clip">
      <figcaption className="tg-clip__kicker">Reference, does not change the result</figcaption>
      <h3 id="channel3-reference-title" className="tg-h3">Channel3 category tree vs PayPal AUP</h3>
      <p className="check-c3__count" data-testid="channel3-reference-count"><span className="tg-num">{tree.categories_read.toLocaleString('en-US')}</span> Channel3 categories read once; <span className="tg-num">{tree.mapped}</span> mapped to a PayPal AUP item or a question for the seller.</p>
      <ul className="check-c3__rows">{tree.examples.map((row) => <li key={row.line} data-testid="channel3-reference-row">
        <blockquote className="tg-clip__quote">{row.path}</blockquote>
        <p className="tg-small">{row.paypal_aup_item} · {row.agreement.replace(/^(\d) of 5 readers$/u, '$1 of 5 readers agreed')} · <span title={`${tree.csv}:${row.line}`}>CSV line {row.line}</span></p>
      </li>)}</ul>
      <Source label="RECORDED" title={`${tree.notes}:${tree.notes_line}; ${tree.csv}`} testId="channel3-reference-source">Channel3 category tree, read once; mapping in {file}</Source>
      <p className="tg-clip__source"><a className="tg-link" href={tree.csv_url} target="_blank" rel="noopener noreferrer" data-testid="channel3-reference-csv">Open the {tree.mapped}-row table (CSV)</a></p>
    </figure>
  </section>;
}
