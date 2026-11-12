// (R5 S25, 2026-11-12) One "days left" count for the case queue, the case head, the timeline and the due text.
// The server sets each demo deadline as its own time plus whole days, so a viewer clock a few seconds behind the
// server read "1 day + 1 s" and rounded up to "2 days". A five-minute grace is taken off before rounding up, so any
// clock within five minutes of the server shows the same count. Display only: no deadline or rule uses this.
export const DUE_GRACE_MS = 5 * 60 * 1000;
const DAY_MS = 86400000;

export function dueDays(value, now = Date.now()) {
  const due = Date.parse(value || '');
  return Number.isFinite(due) ? Math.ceil((due - now - DUE_GRACE_MS) / DAY_MS) : null;
}
