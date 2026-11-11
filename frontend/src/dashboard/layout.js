// The shipped report: two pages on Studio's 24-column canvas. Pure data, so a node test can check
// that every field it maps exists in the data sources and that nothing overlaps.
// (P1 2026-11-12) Colours from the design tokens; no hex values written here.
import { color } from '../theme/tokens.js';

export const DEADLINE_WIDGET = 'payguard-deadline';
export const CHECKLIST_WIDGET = 'payguard-checklist';

const at = (xTrack, yTrack, xSpan, ySpan) => ({ xTrack, yTrack, xSpan, ySpan });
const title = (text, subtitle) => ({
  title: { enabled: true, text },
  ...(subtitle ? { subtitle: { enabled: true, text: subtitle } } : {}),
});
const field = (id, aggregation) => (aggregation ? { id, aggregation } : { id });
// KPI tile: number top-left at 28 px bold ink; `emphasis` makes it the one number that stands out (40 px, watch amber).
const value = (id, aggregation, heading, subtitle, emphasis = false) => ({
  type: 'value',
  dataMapping: { value: [field(id, aggregation)] },
  format: { ...title(heading, subtitle), style: { verticalAlign: 'top', textAlign: 'left',
    typography: { fontSize: emphasis ? 40 : 28, fontWeight: 'bold' }, color: emphasis ? color.watch : color.ink } },
});
const grid = (cols, heading, subtitle) => ({ type: 'grid', dataMapping: { cols: cols.map((id) => field(id)) }, format: { ...title(heading, subtitle), crossFilter: 'filter' } });
const columns = (type, category, measure, aggregation, heading, subtitle) => ({
  type,
  dataMapping: { categoryKey: [field(category)], valueKey: [field(measure, aggregation)] },
  format: { ...title(heading, subtitle), crossFilter: 'filter' },
});

export const NO_ATTACHMENT = 'No attachment on file';

// The evidence auditor's answer slot: full width under the headline tiles. It starts out holding the page's main
// table (Cases / Channel3 receipts); the auditor replaces it with its answer grid in the same place.
export const ANSWER_SLOT_ID = 'auditor-answer';
export const ANSWER_SLOT = Object.freeze(at(0, 18, 24, 14));
export const READINESS_PAGE_ID = 'readiness';
export const GUIDE_ANSWER_SLOT_ID = 'auditor-answer-guide';


const readiness = {
  id: READINESS_PAGE_ID,
  widgets: {
    [ANSWER_SLOT_ID]: grid(['cases.case_ref', 'cases.due_date', 'cases.delivery_proof', 'cases.review_flag'],
      'Cases', 'Ask the auditor to filter'),
    deadline: {
      type: DEADLINE_WIDGET,
      dataMapping: { fields: [field('cases.case_ref'), field('cases.due_date'), field('cases.days_to_due'), field('cases.readiness')] },
      format: title('Response deadlines', 'Demo · read only'),
    },
    'kpi-cases': value('cases.case_ref', 'countd', 'Cases', 'Demo'),
    'kpi-no-attachment': value('cases.case_ref', 'countd', 'No attachment', 'Delivery proof', true),
    'kpi-flags': value('cases.time_flag_count', 'sum', 'Time flags', 'Neutral notes'),
    'kpi-proofs': value('requirements.proof_count', 'sum', 'Proofs on file', 'Records'),
    'case-filter': { type: 'button-filter', dataMapping: { value: [field('cases.case_ref')] }, format: { ...title('Filter by case'),
      style: { dimensions: { height: 44, minWidth: 112 },
        defaultItem: { typography: { fontSize: 14 }, color: color.ink, backgroundColor: color.panel, borderEnabled: true, borderWidth: 1, borderColor: color.controlLine, borderRadius: 8 },
        activeItem: { color: color.ink, backgroundColor: color.accentSelected, borderColor: color.ink } } } },
    checklist: {
      type: CHECKLIST_WIDGET,
      dataMapping: { fields: [field('requirements.case_ref'), field('requirements.evidence_type'), field('requirements.state'),
        field('requirements.proof_count'), field('requirements.attachment_count'), field('cases.review_flag'), field('cases.delivery_proof')] },
      format: title('Evidence checklist', 'One case per card · select to cross-filter (separate from Filter by case)'),
    },
    'gap-chart': columns('bar-chart-grouped', 'time_events.event', 'time_events.gap_hours', 'sum',
      'Hours since the previous event', 'Ordered time evidence · seller-provided unless stated'),
    'events-grid': grid(['time_events.case_ref', 'time_events.order', 'time_events.event', 'time_events.at', 'time_events.source', 'time_events.gap_hours'],
      'Time evidence', 'Only cases with recorded time events · ordered, not judged'),
  },
  widgetLayout: {
    deadline: at(0, 0, 10, 18),
    'kpi-cases': at(10, 0, 7, 9),
    'kpi-no-attachment': at(17, 0, 7, 9),
    'kpi-flags': at(10, 9, 7, 9),
    'kpi-proofs': at(17, 9, 7, 9),
    [ANSWER_SLOT_ID]: { ...ANSWER_SLOT },
    'case-filter': at(0, 32, 24, 9),
    checklist: at(0, 41, 10, 22),
    'gap-chart': at(10, 41, 14, 22),
    'events-grid': at(0, 63, 24, 20),
  },
  filter: {
    widget: { 'kpi-no-attachment': [{ field: field('cases.delivery_proof'), model: { operator: 'equals', value: NO_ATTACHMENT } }] },
  },
};

const guide = {
  id: 'guide',
  widgets: {
    [GUIDE_ANSWER_SLOT_ID]: grid(['receipts.query', 'receipts.called_at', 'receipts.http_status', 'receipts.result_status', 'receipts.cards', 'receipts.latency_seconds'],
      'Channel3 receipts', 'Recorded once; the hosted demo replays them and makes no call'),
    'calls-chart': columns('bar-chart-grouped', 'benchmark.flow', 'benchmark.model_calls', 'sum',
      'Model calls per flow', 'Recorded guide benchmark, 268 cases · lower is cheaper'),
    'rounds-chart': columns('bar-chart-grouped', 'benchmark.flow', 'benchmark.rounds', 'sum',
      'Rounds per flow', 'The first flow records no rounds'),
    'kpi-receipts': value('receipts.receipt_id', 'countd', 'Searches', 'Channel3, recorded'),
    'kpi-cards': value('receipts.cards', 'sum', 'Product cards', 'Returned'),
    'kpi-latency': value('receipts.latency_seconds', 'avg', 'Avg latency (s)', 'Per search'),
    'latency-chart': columns('column-chart-grouped', 'receipts.query', 'receipts.latency_seconds', 'sum',
      'Latency per recorded search (s)', 'docs/evidence/channel3_receipts_v1.json'),
  },
  widgetLayout: {
    'calls-chart': at(0, 0, 12, 18),
    'rounds-chart': at(12, 0, 12, 18),
    [GUIDE_ANSWER_SLOT_ID]: { ...ANSWER_SLOT },
    'kpi-receipts': at(0, 32, 8, 8),
    'kpi-cards': at(8, 32, 8, 8),
    'kpi-latency': at(16, 32, 8, 8),
    'latency-chart': at(0, 40, 24, 16),
  },
};

export const PAGE_TITLES = Object.freeze({ readiness: 'Evidence readiness', guide: 'Guide & Channel3' });

// Phone layouts, written out so the answer slot keeps the full width (the generic stacking below would treat a
// short widget as a half-width tile). Reading order: headline, answer slot, KPI pairs, then detail.
const PHONE = {
  readiness: {
    deadline: at(0, 0, 24, 18), [ANSWER_SLOT_ID]: { ...ANSWER_SLOT },
    'kpi-cases': at(0, 32, 12, 8), 'kpi-no-attachment': at(12, 32, 12, 8), 'kpi-flags': at(0, 40, 12, 8), 'kpi-proofs': at(12, 40, 12, 8),
    'case-filter': at(0, 48, 24, 12), checklist: at(0, 60, 24, 22), 'gap-chart': at(0, 82, 24, 18), 'events-grid': at(0, 100, 24, 18),
  },
  guide: {
    'calls-chart': at(0, 0, 24, 18), [GUIDE_ANSWER_SLOT_ID]: { ...ANSWER_SLOT }, 'rounds-chart': at(0, 32, 24, 14),
    'kpi-receipts': at(0, 46, 12, 8), 'kpi-cards': at(12, 46, 12, 8), 'kpi-latency': at(0, 54, 24, 8), 'latency-chart': at(0, 62, 24, 16),
  },
};

// Generic phone stacking: the same widgets in reading order, full width, KPI tiles two per row.
export function compactLayout(widgetLayout) {
  const ordered = Object.entries(widgetLayout).sort(([, a], [, b]) => a.yTrack - b.yTrack || a.xTrack - b.xTrack);
  const out = {};
  let y = 0;
  let halfOpen = null;
  for (const [id, layout] of ordered) {
    const small = layout.ySpan <= 9;
    if (small && halfOpen) { out[id] = at(12, halfOpen.y, 12, halfOpen.h); halfOpen = null; continue; }
    if (small) { out[id] = at(0, y, 12, layout.ySpan); halfOpen = { y, h: layout.ySpan }; y += layout.ySpan; continue; }
    halfOpen = null;
    out[id] = at(0, y, 24, Math.max(layout.ySpan, 12));
    y += out[id].ySpan;
  }
  return out;
}

// Canvas tracks a page needs, so the page shell can give a stacked phone layout its full height.
export function pageTracks(page) {
  return Object.values(page.widgetLayout).reduce((max, layout) => Math.max(max, layout.yTrack + layout.ySpan), 0);
}

export function initialReport({ compact = false } = {}) {
  const pages = [structuredClone(readiness), structuredClone(guide)];
  if (compact) for (const page of pages) page.widgetLayout = PHONE[page.id] ? structuredClone(PHONE[page.id]) : compactLayout(page.widgetLayout);
  return { selectedPageId: readiness.id, pages, panels: { ai: { width: compact ? 268 : 380 }, filters: { collapsed: true } } };
}
