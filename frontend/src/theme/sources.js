// (F 2026-11-12) The one source line and the one legend for every console page (Overview, Check a sale, Proof, For judges).
// Definitions and source strings live in data/source_labels_v1.json; a page names a source by key, so one source reads
// the same on every page. The visible line wraps (never an ellipsis); the full path and cited lines sit in the title.
// Plain createElement (no JSX) so tests/frontend_source_labels.mjs can import this file in Node.
// (R6 2026-11-12, S33) Softer source lines: the label shows in sentence case (Recorded, Recounted, Synthetic, Hosted demo),
// then the plain source and its date. File names and line numbers stay in the title; only the Proof page asks for the line
// number on the visible line (exact). The keys (RECORDED, ...) are unchanged.
import { createElement as h } from 'react';
import table from '../data/source_labels_v1.json';
import { dateLabel } from './format.js';
import './sources.css';

export const SOURCE_KINDS = Object.freeze(table.labels.map((item) => item.kind));
// RECORDED, RECOUNTED, SYNTHETIC, HOSTED DEMO: one sentence each.
export const SOURCE_LABELS = Object.freeze(Object.fromEntries(table.labels.map((item) => [item.kind, item.meaning])));
// RECORDED -> "Recorded": the shown name of each label.
export const SOURCE_NAMES = Object.freeze(Object.fromEntries(table.labels.map((item) => [item.kind, item.name])));
export const SOURCES = table.sources;
export const CHANNEL3_READERS = Object.freeze({ ...table.channel3_readers, title: `${table.channel3_readers.path}:${table.channel3_readers.line}` });

// "Country rules file" (exact: "Country rules file · line 3947"), "Hosted send receipt · 10 Nov 2026"; title "path:3947, 9752 (detail)".
// An unknown key never breaks the page: it shows the key itself and logs an error (tests/frontend_source_labels.mjs
// checks every key used in frontend/src exists).
export function sourceCitation(key, { exact = false } = {}) {
  const entry = SOURCES[key];
  if (!entry) {
    console.error(`ERROR unknown source key: ${key}`);
    return { text: String(key), title: '', unknown: true };
  }
  const where = entry.show === 'line' ? (exact ? `line ${entry.lines[0]}` : '') : entry.show === 'date' ? dateLabel(entry.date) : '';
  const lines = entry.lines.length ? `:${entry.lines.join(', ')}` : '';
  return {
    text: where ? `${entry.text} · ${where}` : entry.text,
    title: `${entry.path}${lines}${entry.detail ? ` (${entry.detail})` : ''}`,
  };
}

// <SourceLine kind="RECOUNTED" source="country_rules_sg_ecig" />, or kind + text + title for a line that is not a file
// (for example a count with a link as children). Several keys join with "; " in one line.
// (N1 C53) compact: the label alone, with `children` (an info button holding the source) after it; the title keeps the path.
export function SourceLine({ kind, source, text, title, children, as = 'p', className = '', testId, exact = false, compact = false }) {
  if (!SOURCE_LABELS[kind]) console.error(`ERROR unknown source label: ${kind}`);
  const cites = source ? [].concat(source).map((key) => sourceCitation(key, { exact })) : [];
  const shown = cites.length ? cites.map((cite) => cite.text).join('; ') : text;
  const full = cites.length ? cites.map((cite) => cite.title).join('; ') : title;
  return h(as, { className: `tg-source tg-source--wrap${className ? ` ${className}` : ''}`, title: full, 'data-testid': testId, 'data-source': source ? [].concat(source).join(' ') : undefined },
    h('span', { className: 'tg-source__label' }, SOURCE_NAMES[kind] || kind),
    compact ? h('span', null, ' ', children || null) : h('span', null, '· ', shown, children ? ' · ' : null, children || null));
}

// The four labels, in one list. Only this legend is used on the site.
// (N1 C13) A label's extra note sits behind a tap (ⓘ, a native fold). On a phone (below 768px when the page draws) the
// list is one fold; Node renders (no window) get the open list.
// (K1 G10c 2026-11-13) The fold title is plain words, one line at 393px; it no longer strings the label names
// ("Recorded · Recounted · Synthetic · Hosted demo"), which wrapped and read as jargon. Each name and its one-sentence
// meaning ("Counted again by a test from a saved data file.") stay in the list inside.
const phoneNow = () => typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia('(max-width: 767px)').matches;
export function SourceLegend({ testId, className = '' }) {
  const list = h('ul', { className: `tg-legend${className ? ` ${className}` : ''}`, 'data-testid': testId, 'aria-label': 'What the source labels mean' },
    table.labels.map((item) => h('li', { key: item.kind }, h('b', null, item.name), h('span', null, item.meaning,
      item.note ? h('details', { className: 'tg-legend__note' }, h('summary', { 'aria-label': `More about ${item.name}` }, 'ⓘ'), item.note) : null))));
  if (!phoneNow()) return list;
  return h('details', { className: 'tg-legend-fold' }, h('summary', null, 'What the source labels mean ▸'), list);
}
