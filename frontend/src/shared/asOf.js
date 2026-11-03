// One "as of" time for every page (spec D16): the `as_of` of frontend/src/data/dashboard_disputes_v1.json.
// `?asof=<ISO 8601 UTC>` overrides it only in a build made with VITE_PAYGUARD_PUBLIC_DEMO=1. No build in this
// repository sets that variable (not the Dockerfile, render.yaml or tools/run.sh), so the parameter is ignored
// in every build, the hosted one included. Pure functions here; the file value
// is read in shared/asOfSource.js so that this module stays importable from Node tests.

const ISO_UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,3})?)?Z$/;

export function parseAsOf(value) {
  if (typeof value !== 'string' || !ISO_UTC.test(value)) return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? new Date(ms).toISOString() : null;
}

// Returns the as-of instant as an ISO string. Throws when the file value is not a valid UTC time:
// a missing as-of must stop the page, never fall back to the wall clock.
export function resolveAsOf({ fileAsOf, search = '', publicDemo = false }) {
  const base = parseAsOf(fileAsOf);
  if (base === null) throw new Error('AS_OF_SOURCE_INVALID');
  if (!publicDemo) return base;
  let requested = null;
  try { requested = new URLSearchParams(search).get('asof'); } catch { requested = null; }
  return parseAsOf(requested) ?? base;
}

export const asOfMs = (iso) => Date.parse(iso);

// Whole days from `asOf` to `due` (negative when overdue), on UTC calendar days.
export function daysUntil(due, asOf) {
  const a = parseAsOf(asOf); const d = typeof due === 'string' ? Date.parse(due) : NaN;
  if (a === null || !Number.isFinite(d)) return null;
  const day = 86400000;
  return Math.floor(d / day) - Math.floor(Date.parse(a) / day);
}
