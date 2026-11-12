// (vteam icon 2026-11-12) One icon vocabulary for the whole site: Phosphor Regular (MIT, theme/icons/LICENSE).
// Every icon a page draws is named here by what it stands for (a step, a status, a person, an action, a data source),
// and drawn from one external sprite (theme/icons/sprite.svg, built by theme/icons/build-sprite.mjs from the single
// files beside it). The sprite is a separate hashed asset, so the first-load JS carries names, not path data.
// Size steps: one 28px icon for the page's focus area, then 20 / 18 / 16. Colour is always currentColor: status
// icons take the status colour from their parent (.tg-risk, .tg-done, .tg-deadline--soon); everything else is muted
// or ink. The accent colour is only for the focus icon when the focus is not a status, and for the AI mark.
import { createElement } from 'react';
import spriteUrl from './icons/sprite.svg?no-inline';

// The sprite holds exactly these files from theme/icons (build-sprite.mjs reads this list).
export const SPRITE_NAMES = [
  'arrow-right', 'arrow-u-down-left', 'arrows-clockwise', 'buildings', 'chart-line-up', 'check', 'check-circle',
  'clock', 'cloud-check', 'copy', 'database', 'dot-outline', 'file-text', 'files', 'fingerprint', 'flask', 'gavel',
  'globe', 'house', 'info', 'lightning', 'link-simple', 'lock-simple', 'note-pencil', 'paper-plane-tilt', 'play',
  'plugs-connected', 'scales', 'seal-check', 'shield-check', 'sparkle', 'stack', 'storefront', 'test-tube', 'user',
  'user-check', 'warning', 'warning-octagon', 'x', 'x-circle',
];

export const ICON_SIZE = { focus: 28, lg: 20, md: 18, sm: 16 };

// The focus area of each page gets one icon at ICON_SIZE.focus and nothing else on the page is drawn at 28.
// Check a sale has no fixed focus icon: its result card uses STATUS by verdict (risk / ok / warn).
export const FOCUS = {
  overview: 'paper-plane-tilt', // the 10 Nov send receipt (P0 2026-11-12): not a status, may take the accent colour
  compliance: null,
  velocity: 'chart-line-up', // the x5.0 figure: not a status, may take the accent colour
  disputes: 'clock', // the "1 day" deadline: amber
  proof: 'fingerprint', // the SHA-256 MATCH result
  judges: 'seal-check', // the first stop on the route
};

// Step heads and the page tabs (ICON_SIZE.md).
export const STEP = {
  overview: 'house', compliance: 'globe', velocity: 'chart-line-up', disputes: 'scales', proof: 'fingerprint', judges: 'seal-check',
};

// Status: never colour alone (consensus section 3, a11y P0). Risk is the octagon (x-circle where a row says "no").
export const STATUS = { risk: 'warning-octagon', riskNo: 'x-circle', ok: 'check-circle', warn: 'clock', info: 'info', notRun: 'dot-outline' };

// People and roles (ICON_SIZE.sm, muted): timeline nodes and the ledger "who" column only, not every line.
export const ROLE = { buyer: 'user', seller: 'storefront', paypal: 'buildings', reviewer: 'user-check', ai: 'sparkle' };

// Actions (ICON_SIZE.sm inside meta lines, ICON_SIZE.md inside buttons; one icon per button).
export const ACTION = {
  send: 'paper-plane-tilt', readBack: 'arrow-u-down-left', draft: 'note-pencil', connect: 'plugs-connected',
  run: 'play', copy: 'copy', refresh: 'arrows-clockwise', open: 'arrow-right', close: 'x',
};

// Data roles: where a figure or a file comes from (the source labels and the proof method chips).
export const SOURCE = {
  RECORDED: 'files', RECOUNTED: 'database', SYNTHETIC: 'flask', 'HOSTED DEMO': 'cloud-check',
  REAL_SANDBOX: 'shield-check', TEST: 'test-tube', LAW: 'gavel', EVIDENCE: 'file-text', HASH: 'fingerprint',
};

// The hand-drawn names in App.jsx, scenarios/main.jsx and proof/main.jsx, mapped to Phosphor, so each page can swap
// its local path table for <SpriteIcon name={LEGACY[name]} /> without touching the call sites.
export const LEGACY = {
  shield: 'shield-check', arrow: 'arrow-right', bolt: 'lightning', chart: 'chart-line-up', check: 'check',
  clock: 'clock', layers: 'stack', file: 'file-text', refresh: 'arrows-clockwise', link: 'link-simple',
  alert: 'warning-octagon', lock: 'lock-simple', close: 'x', info: 'info', play: 'play', copy: 'copy',
  cross: 'x', user: 'user', dot: 'dot-outline',
  sandbox: 'shield-check', recorded: 'files', test: 'test-tube', synthetic: 'flask',
};

// Name checks: build-sprite.mjs --check fails when any value in the maps above is not in SPRITE_NAMES; in dev a
// missing name is also logged (grep-able ERROR). The production build leaves the list out (first-load budget), and a
// missing name draws nothing, never a shield or a check that could read as a result.
export function iconHref(name) {
  if (import.meta.env.DEV && !SPRITE_NAMES.includes(name)) console.error(`ERROR iconMap: no sprite icon "${name}"`);
  return `${spriteUrl}#ph-${name}`;
}

// <SpriteIcon name="paper-plane-tilt" size="sm" /> or size={14} for an exact pixel size. No class by default, so the
// width/height attributes hold (.tg-icon fixes 18px in components.css); container rules such as `.tg-risk > svg`
// still size it. Baseline: sits on the text line like a lower-case letter.
const BASELINE = { verticalAlign: '-0.125em', flex: 'none' };
export function SpriteIcon({ name, size = 'md', className, style, ...props }) {
  const px = typeof size === 'number' ? size : ICON_SIZE[size] || ICON_SIZE.md;
  return createElement('svg', {
    width: px, height: px, viewBox: '0 0 256 256', fill: 'currentColor', 'aria-hidden': 'true', focusable: 'false',
    className, style: style ? { ...BASELINE, ...style } : BASELINE, 'data-icon': name, ...props,
  }, createElement('use', { href: iconHref(name) }));
}
