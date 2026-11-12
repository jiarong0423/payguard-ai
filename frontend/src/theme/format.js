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

// "USD 48.00": currency code first, one space, two decimals (components.css rule 5, FIELD_INVENTORY section 2).
// moneyParts() returns the same two parts in display order, so a view can render the code smaller and muted.
export function moneyParts(value, currency = 'USD') {
  const n = finite(value);
  return n === null ? { code: '', amount: DASH } : { code: String(currency || '').toUpperCase(), amount: MONEY.format(n) };
}
export function money(value, currency = 'USD') {
  const { code, amount } = moneyParts(value, currency);
  return code ? `${code} ${amount}` : amount;
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
// Site-wide dates (review_INTEG.md section 4 item 5): "9 Nov 2026" and "9 Nov 2026, 06:24 GMT+8".
// A zone label is "UTC", "GMT" or "GMT+8" / "GMT-5" / "GMT+5:30"; the clock is shifted by that offset, so the output
// does not depend on the machine. Without a label, dateTimeLabel uses the viewer's own offset and names it.
const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const DATE_ONLY = /^(\d{4})-(\d{2})-(\d{2})$/u;
const pad2 = (n) => String(n).padStart(2, '0');
export function zoneOffsetMinutes(label) {
  const match = /^(?:UTC|GMT)(?:([+\-\u2212])(\d{1,2})(?::?(\d{2}))?)?$/u.exec(String(label || '').trim());
  if (!match) return null;
  if (!match[1]) return 0;
  const minutes = Number(match[2]) * 60 + Number(match[3] || 0);
  return minutes > 14 * 60 ? null : (match[1] === '+' ? minutes : -minutes);
}
export function zoneLabel(offsetMinutes) {
  if (!Number.isFinite(offsetMinutes)) return '';
  if (offsetMinutes === 0) return 'UTC'; // (vteam viz r7) one name for offset 0 everywhere: facts and chart both say UTC
  const abs = Math.abs(offsetMinutes);
  return `GMT${offsetMinutes > 0 ? '+' : '-'}${Math.floor(abs / 60)}${abs % 60 ? `:${pad2(abs % 60)}` : ''}`;
}
const dayText = (d) => `${d.getUTCDate()} ${MONTH_NAMES[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
// "9 Nov 2026". A date-only string ("2026-11-09") is a calendar day and is never shifted; a timestamp is read in the
// given zone label (UTC when none is given).
export function dateLabel(value, timeZoneLabel = 'UTC') {
  if (typeof value === 'string') {
    const day = DATE_ONLY.exec(value);
    if (day) {
      const d = new Date(Date.UTC(Number(day[1]), Number(day[2]) - 1, Number(day[3])));
      return d.getUTCMonth() === Number(day[2]) - 1 ? dayText(d) : DASH;
    }
  }
  const d = toDate(value);
  const offset = zoneOffsetMinutes(timeZoneLabel);
  if (d === null || offset === null) return DASH;
  return dayText(new Date(d.getTime() + offset * 60000));
}
// "9 Nov 2026, 06:24 GMT+8"
export function dateTimeLabel(value, timeZoneLabel) {
  const d = toDate(value);
  if (d === null || (typeof value === 'string' && DATE_ONLY.test(value))) return DASH;
  const offset = timeZoneLabel === undefined ? -d.getTimezoneOffset() : zoneOffsetMinutes(timeZoneLabel);
  if (offset === null) return DASH;
  const shifted = new Date(d.getTime() + offset * 60000);
  const label = timeZoneLabel === undefined ? zoneLabel(offset) : String(timeZoneLabel).trim().replace('\u2212', '-');
  return `${dayText(shifted)}, ${pad2(shifted.getUTCHours())}:${pad2(shifted.getUTCMinutes())} ${label}`;
}

// ISO 8601 for exports ("2026-11-01T12:00:00.000Z"); null when the input is not a date.
export function isoDate(value) {
  const d = toDate(value);
  return d === null ? null : d.toISOString();
}
