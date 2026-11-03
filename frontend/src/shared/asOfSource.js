// The app-side as-of: reads only `as_of` from the dashboard data file (named JSON import, tree-shaken) and
// applies the public-demo `?asof=` rule from shared/asOf.js. Use AS_OF wherever a page would otherwise read the wall clock.
import { as_of as fileAsOf } from '../data/dashboard_disputes_v1.json';
import { asOfMs, resolveAsOf } from './asOf.js';

const env = import.meta.env || {};
export const PUBLIC_DEMO = env.VITE_PAYGUARD_PUBLIC_DEMO === '1';

export const AS_OF = resolveAsOf({
  fileAsOf,
  search: typeof window === 'undefined' ? '' : window.location.search,
  publicDemo: PUBLIC_DEMO,
});
export const AS_OF_MS = asOfMs(AS_OF);
