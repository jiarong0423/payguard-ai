// Number and time formatting for every page (spec section 2 "Numbers"). Intl en-US, UTC for times.
// Every function returns DASH for missing or non-finite input instead of inventing a value.

export const DASH = '—';
export const MINUS = '−'; // U+2212 for signed deltas

const finite = (value) => {
  if (value === null || value === undefined || value === '') return null;
  const n = typeof value === 'number' ? value : Number(value);
  return Number.isFinite(n) ? n : null;
};

const fixed = (digits) => new Intl.NumberFormat('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
const MONEY = fixed(2);
const INTEGER = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });

// "500.00 USD". moneyParts() lets a view render the currency code smaller and muted.
export function moneyParts(value, currency = 'USD') {
  const n = finite(value);
  return n === null ? { amount: DASH, code: '' } : { amount: MONEY.format(n), code: String(currency || '').toUpperCase() };
}
export function money(value, currency = 'USD') {
  const { amount, code } = moneyParts(value, currency);
  return code ? `${amount} ${code}` : amount;
}

export function integer(value) {
  const n = finite(value);
  return n === null ? DASH : INTEGER.format(Math.round(n));
}

// "5.0×"
export function ratio(value, digits = 1) {
  const n = finite(value);
  return n === null ? DASH : `${fixed(digits).format(n)}×`;
}

// "19%" from 19 (already a percentage), or from 0.19 with { fraction: true }.
export function percent(value, { digits = 0, fraction = false } = {}) {
  const n = finite(value);
  return n === null ? DASH : `${fixed(digits).format(fraction ? n * 100 : n)}%`;
}

// Signed delta: "+36", "−36", "0". Optional unit suffix ("+2 d").
export function delta(value, { digits = 0, unit = '' } = {}) {
  const n = finite(value);
  if (n === null) return DASH;
  const body = fixed(digits).format(Math.abs(n));
  const sign = n > 0 ? '+' : n < 0 ? MINUS : '';
  return `${sign}${body}${unit ? ` ${unit}` : ''}`;
}

const toDate = (value) => {
  if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value;
  if (typeof value !== 'string' && typeof value !== 'number') return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d;
};
const DAY = new Intl.DateTimeFormat('en-US', { month: 'short', day: '2-digit', timeZone: 'UTC' });
const CLOCK = new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'UTC' });

// "Nov 01 · 15:42 UTC"
export function utcTime(value) {
  const d = toDate(value);
  return d === null ? DASH : `${DAY.format(d)} · ${CLOCK.format(d)} UTC`;
}
// "Nov 01"
export function utcDay(value) {
  const d = toDate(value);
  return d === null ? DASH : DAY.format(d);
}
// ISO 8601 for exports ("2026-11-01T12:00:00.000Z"); null when the input is not a date.
export function isoDate(value) {
  const d = toDate(value);
  return d === null ? null : d.toISOString();
}
