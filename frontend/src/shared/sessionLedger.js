// Session ledger: the seller's own local decisions (moved work blocks, checked to-do rows, filled gaps) that
// pages share within one browser session. sessionStorage only, never sent anywhere; every storage call is
// wrapped in try/catch (private mode, quota, disabled storage) and the ledger then works in memory.
// Same-tab listeners are notified directly; other tabs/pages hear the `storage` event.
//
//   const ledger = createSessionLedger();           // default key 'payguard.ledger.v1'
//   ledger.set('block:case-ref-002:tracking', { start: '2026-11-03T00:00:00Z' });
//   const stop = ledger.subscribe((entries) => render(entries));

export const LEDGER_KEY = 'payguard.ledger.v1';
const KEY_PATTERN = /^[a-z][a-z0-9_-]{0,31}(?::[A-Za-z0-9_.-]{1,64}){0,3}$/;
const MAX_ENTRIES = 200;
const MAX_BYTES = 64 * 1024;

const isPlainValue = (value) => {
  if (value === null || ['string', 'number', 'boolean'].includes(typeof value)) return typeof value !== 'number' || Number.isFinite(value);
  if (Array.isArray(value)) return value.every(isPlainValue);
  if (typeof value === 'object' && Object.getPrototypeOf(value) === Object.prototype) return Object.values(value).every(isPlainValue);
  return false;
};

function parse(raw) {
  if (typeof raw !== 'string' || !raw) return {};
  try {
    const data = JSON.parse(raw);
    if (!data || typeof data !== 'object' || Array.isArray(data) || data.version !== 1 || typeof data.entries !== 'object' || data.entries === null) return {};
    const entries = {};
    for (const [key, value] of Object.entries(data.entries)) if (KEY_PATTERN.test(key) && isPlainValue(value)) entries[key] = value;
    return entries;
  } catch {
    return {};
  }
}

export function createSessionLedger({ key = LEDGER_KEY, storage = globalThis.sessionStorage, win = globalThis.window } = {}) {
  const listeners = new Set();
  let memory = {};
  const read = () => {
    try { return storage ? parse(storage.getItem(key)) : { ...memory }; } catch { return { ...memory }; }
  };
  const write = (entries) => {
    memory = { ...entries };
    try { if (storage) storage.setItem(key, JSON.stringify({ version: 1, entries })); } catch { /* memory copy stays authoritative */ }
    const snapshot = Object.freeze({ ...entries });
    for (const listener of [...listeners]) { try { listener(snapshot); } catch { /* one listener must not break others */ } }
  };
  const onStorage = (event) => {
    if (event.key !== key && event.key !== null) return;
    const snapshot = Object.freeze(read());
    for (const listener of [...listeners]) { try { listener(snapshot); } catch { /* ignore */ } }
  };

  return {
    key,
    entries: () => Object.freeze(read()),
    get: (entryKey) => read()[entryKey],
    set(entryKey, value) {
      if (!KEY_PATTERN.test(entryKey)) throw new Error('LEDGER_KEY_INVALID');
      if (!isPlainValue(value)) throw new Error('LEDGER_VALUE_INVALID');
      const entries = { ...read(), [entryKey]: value };
      if (Object.keys(entries).length > MAX_ENTRIES) throw new Error('LEDGER_FULL');
      if (JSON.stringify(entries).length > MAX_BYTES) throw new Error('LEDGER_FULL');
      write(entries);
    },
    remove(entryKey) {
      const entries = read();
      if (!(entryKey in entries)) return;
      delete entries[entryKey];
      write(entries);
    },
    clear() {
      memory = {};
      try { if (storage) storage.removeItem(key); } catch { /* ignore */ }
      for (const listener of [...listeners]) { try { listener(Object.freeze({})); } catch { /* ignore */ } }
    },
    subscribe(listener) {
      if (listeners.size === 0 && win && typeof win.addEventListener === 'function') win.addEventListener('storage', onStorage);
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
        if (listeners.size === 0 && win && typeof win.removeEventListener === 'function') win.removeEventListener('storage', onStorage);
      };
    },
  };
}

let shared = null;
// The page-wide ledger (lazily created so importing this module has no side effects).
export function sessionLedger() {
  if (!shared) shared = createSessionLedger();
  return shared;
}
