// Arrow keys for a role="tablist" (red team 2026-11-03 P2-8): Left/Right (and Up/Down) move to the next tab, Home and
// End jump to the ends, and the newly selected tab takes focus. Only the active tab sits in the Tab order
// (tabIndex 0); the others get -1, so Tab leaves the tablist in one press (roving tabindex).
export function tabKeyDown(event, keys, current, select, idFor) {
  const index = keys.indexOf(current);
  const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
  let next = null;
  if (step) next = keys[(index + step + keys.length) % keys.length];
  else if (event.key === 'Home') next = keys[0];
  else if (event.key === 'End') next = keys[keys.length - 1];
  if (next === null || next === undefined) return;
  event.preventDefault();
  select(next);
  window.requestAnimationFrame(() => document.getElementById(idFor(next))?.focus());
}
