// Motion helpers (spec section 2 "Motion rules"). Every JS reveal goes through prefersReducedMotion():
// with reduced motion it renders the final frame at once and count-ups jump to the final value.
import { useEffect, useRef, useState } from 'react';
import { motion } from './tokens.js';

export const DURATION = motion;
export const EASE_OUT = motion.easeOut;
export const EASE_IN = motion.easeIn;

export function prefersReducedMotion(win = globalThis.window) {
  try {
    return Boolean(win && typeof win.matchMedia === 'function' && win.matchMedia('(prefers-reduced-motion: reduce)').matches);
  } catch {
    return false;
  }
}

// cubic-bezier(.2,.8,.2,1) approximated by an ease-out cubic; pure, for count-ups and tests.
export const easeOut = (t) => 1 - (1 - Math.min(1, Math.max(0, t))) ** 3;

// Value of a count-up `elapsed` ms after start; reaches exactly `target` at `duration`.
export function countUpValue(target, elapsed, duration = motion.dataMax, { from = 0, digits = 0 } = {}) {
  if (!Number.isFinite(target)) return target;
  if (duration <= 0 || elapsed >= duration) return target;
  const raw = from + (target - from) * easeOut(elapsed / duration);
  const scale = 10 ** digits;
  return Math.round(raw * scale) / scale;
}

// React hook: counts from `from` to `target` once `start` is true; never longer than motion.max.
// Reduced motion (or no requestAnimationFrame) returns the final value immediately. Cancels on unmount.
export function useCountUp(target, { duration = motion.dataMax, start = true, from = 0, digits = 0 } = {}) {
  const reduced = prefersReducedMotion();
  const animate = start && !reduced && Number.isFinite(target) && typeof globalThis.requestAnimationFrame === 'function';
  const [value, setValue] = useState(animate ? from : target);
  const frame = useRef(0);
  useEffect(() => {
    if (!animate) { setValue(target); return undefined; }
    const length = Math.min(duration, motion.max);
    let startedAt = null;
    const tick = (now) => {
      if (startedAt === null) startedAt = now;
      const elapsed = now - startedAt;
      setValue(countUpValue(target, elapsed, length, { from, digits }));
      if (elapsed < length) frame.current = requestAnimationFrame(tick);
    };
    frame.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame.current);
  }, [animate, target, duration, from, digits]);
  return value;
}

// Runs `callback` once when `element` first enters the viewport; immediately under reduced motion or
// without IntersectionObserver. Returns a cleanup function (call it on unmount).
export function onceInView(element, callback, { threshold = 0.25, win = globalThis.window } = {}) {
  if (!element || prefersReducedMotion(win) || !win || typeof win.IntersectionObserver !== 'function') {
    callback();
    return () => {};
  }
  let done = false;
  const observer = new win.IntersectionObserver((entries) => {
    if (done || !entries.some((entry) => entry.isIntersecting)) return;
    done = true;
    observer.disconnect();
    callback();
  }, { threshold });
  observer.observe(element);
  return () => { done = true; observer.disconnect(); };
}
