// (F 2026-11-12) The one source line and the one legend for every console page (Overview, Check a sale, Proof, For judges).
// Definitions and source strings live in data/source_labels_v1.json; a page names a source by key, so one source reads
// the same on every page. The visible line wraps (never an ellipsis); the full path and cited lines sit in the title.
// Plain createElement (no JSX) so tests/frontend_source_labels.mjs can import this file in Node.
import { createElement as h } from 'react';
import table from '../data/source_labels_v1.json';
import { dateLabel } from './format.js';
import './sources.css';

export const SOURCE_KINDS = Object.freeze(table.labels.map((item) => item.kind));
// RECORDED, RECOUNTED, SYNTHETIC, HOSTED DEMO: one sentence each.
export const SOURCE_LABELS = Object.freeze(Object.fromEntries(table.labels.map((item) => [item.kind, item.meaning])));
export const SOURCES = table.sources;
export const CHANNEL3_READERS = Object.freeze({ ...table.channel3_readers, title: `${table.channel3_readers.path}:${table.channel3_readers.line}` });

// "Country rules file · line 3947", "Hosted send receipt · 10 Nov 2026"; title "path:3947, 9752 (detail)".
// An unknown key never breaks the page: it shows the key itself and logs an error (tests/frontend_source_labels.mjs
// checks every key used in frontend/src exists).
export function sourceCitation(key) {
  const entry = SOURCES[key];
  if (!entry) {
    console.error(`ERROR unknown source key: ${key}`);
    return { text: String(key), title: '', unknown: true };
  }
  const where = entry.show === 'line' ? `line ${entry.lines[0]}` : entry.show === 'date' ? dateLabel(entry.date) : '';
  const lines = entry.lines.length ? `:${entry.lines.join(', ')}` : '';
  return {
    text: where ? `${entry.text} · ${where}` : entry.text,
    title: `${entry.path}${lines}${entry.detail ? ` (${entry.detail})` : ''}`,
  };
}

// <SourceLine kind="RECOUNTED" source="country_rules_sg_ecig" />, or kind + text + title for a line that is not a file
// (for example a count with a link as children). Several keys join with "; " in one line.
export function SourceLine({ kind, source, text, title, children, as = 'p', className = '', testId }) {
  if (!SOURCE_LABELS[kind]) console.error(`ERROR unknown source label: ${kind}`);
  const cites = source ? [].concat(source).map(sourceCitation) : [];
  const shown = cites.length ? cites.map((cite) => cite.text).join('; ') : text;
  const full = cites.length ? cites.map((cite) => cite.title).join('; ') : title;
  return h(as, { className: `tg-source tg-source--wrap${className ? ` ${className}` : ''}`, title: full, 'data-testid': testId, 'data-source': source ? [].concat(source).join(' ') : undefined },
    h('span', { className: 'tg-source__label' }, kind),
    h('span', null, '· ', shown, children ? ' · ' : null, children || null));
}

// The four labels, in one list. Only this legend is used on the site.
export function SourceLegend({ testId, className = '' }) {
  return h('ul', { className: `tg-legend${className ? ` ${className}` : ''}`, 'data-testid': testId, 'aria-label': 'What the source labels mean' },
    table.labels.map((item) => h('li', { key: item.kind }, h('b', null, item.kind), h('span', null, item.meaning))));
}
