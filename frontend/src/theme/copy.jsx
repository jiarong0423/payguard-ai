// (N1 B, 2026-11-12, ui_mock/COPY_FINAL_v4_1.md) One place for the copy's phone variants and its one-tap extras.
// "new" is the text for wide screens; "phone" is the text below 768px; what a phone line leaves out sits one tap away,
// in an info button (ⓘ, a real button: phones have no hover) or a fold (<details>). Display only: no value is computed here.
// A server render and Node tests (no window) get the wide text, so a test that reads the desktop string keeps reading it.
import { useState, useSyncExternalStore } from 'react';

export const PHONE_QUERY = '(max-width: 767px)';
const media = () => (typeof window !== 'undefined' && typeof window.matchMedia === 'function' ? window.matchMedia(PHONE_QUERY) : null);
function subscribe(onChange) {
  const list = media();
  if (!list) return () => {};
  list.addEventListener('change', onChange);
  return () => list.removeEventListener('change', onChange);
}
const isPhone = () => Boolean(media()?.matches);

// True below 768px (the copy's phone width); false without a window.
export function usePhoneCopy() {
  return useSyncExternalStore(subscribe, isPhone, () => false);
}

// An info button you can tap: the extra detail opens under it and closes on a second tap. `label` names it for screen
// readers ("More about …"); the visible mark is ⓘ.
export function Info({ label = 'More detail', children, testId }) {
  const [open, setOpen] = useState(false);
  return <span className="copy-info tg-box tg-box--info" data-testid={testId}>
    <button type="button" className="copy-info__btn" aria-expanded={open} aria-label={label} title={label} onClick={() => setOpen((on) => !on)}>ⓘ</button>
    {open && <span className="copy-info__body" role="note">{children}</span>}
  </span>;
}

// A fold that starts closed: its summary is the one line shown, the body is one tap away.
export function Fold({ summary, children, testId, open }) {
  return <details className="copy-fold tg-box tg-box--fold" data-testid={testId} open={open}>
    <summary className="copy-fold__sum">{summary}</summary>
    <div className="copy-fold__body">{children}</div>
  </details>;
}

// Wide text, or on a phone the short text plus (when `more` is given) an info button holding what it leaves out.
export function Short({ wide, phone, more, label }) {
  const narrow = usePhoneCopy();
  if (!narrow || phone === undefined || phone === null) return wide;
  return <>{phone}{more ? <> <Info label={label || 'Full text'}>{more}</Info></> : null}</>;
}
