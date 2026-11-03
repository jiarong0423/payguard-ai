// Pure mapping from the backend time evidence block to rows and milestones for the
// optional Bryntum Scheduler timeline. No Bryntum import here, so it runs in plain Node.
import { operatorLabel } from '../operatorLabels.js';

// One row per kind of record, in the order a dispute usually unfolds.
export const TIMELINE_LANES = [
  ['PAYMENT', 'Payment'],
  ['ORDER_RECORD_CREATED', 'Order record'],
  ['DELIVERY', 'Delivery'],
  ['MESSAGE', 'Messages'],
  ['CLAIM_OPENED', 'Claim'],
];
const LANE_IDS = new Set(TIMELINE_LANES.map(([id]) => id));
const HOUR = 3600 * 1000;
const DAY = 24 * HOUR;

// Bryntum draws local wall-clock time. The evidence is UTC, so each instant becomes a
// Date whose local fields equal its UTC fields; the axis then reads in UTC.
export function utcWallClock(iso) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return null;
  return new Date(
    date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
    date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds(), date.getUTCMilliseconds(),
  );
}

// Preset and its tick length. The axis snaps to whole ticks, so the range is padded by
// at least one tick on each side and milestone labels near the ends stay visible.
const PRESETS = [
  [2 * DAY, 'hourAndDay', HOUR],
  [21 * DAY, 'dayAndWeek', DAY],
  [120 * DAY, 'weekAndMonth', 7 * DAY],
  [Infinity, 'monthAndYear', 31 * DAY],
];

export function viewPresetFor(spanMs) {
  return PRESETS.find(([limit]) => spanMs <= limit)[1];
}

function tickFor(spanMs) {
  return PRESETS.find(([limit]) => spanMs <= limit)[2];
}

function eventName(event) {
  if (event.kind === 'MESSAGE') return `${operatorLabel('MESSAGE')} · ${operatorLabel(event.topic)}`;
  return operatorLabel(event.kind);
}

// Returns null when there is nothing to draw. Every event becomes a zero-length
// milestone: the timeline places records in time, it does not measure or judge them.
export function buildTimelineModel(evidence) {
  if (!evidence || !Array.isArray(evidence.events)) return null;
  const events = [];
  evidence.events.forEach((event, index) => {
    if (!event || !LANE_IDS.has(event.kind)) return;
    const at = utcWallClock(event.at);
    if (!at) return;
    events.push({
      id: `evidence-${index}`,
      resourceId: event.kind,
      name: eventName(event),
      startDate: at,
      endDate: at,
      source: operatorLabel(event.source),
      at: event.at,
      cls: `payguard-milestone-${event.kind.toLowerCase()}`,
    });
  });
  if (events.length === 0) return null;
  const used = new Set(events.map((event) => event.resourceId));
  const resources = TIMELINE_LANES.filter(([id]) => used.has(id)).map(([id, name]) => ({ id, name }));
  const times = events.map((event) => event.startDate.getTime());
  const first = Math.min(...times);
  const last = Math.max(...times);
  const span = Math.max(last - first, HOUR);
  const pad = Math.max(span * 0.15, tickFor(span));
  return {
    resources,
    events,
    startDate: new Date(first - pad),
    endDate: new Date(last + pad),
    viewPreset: viewPresetFor(span),
  };
}
