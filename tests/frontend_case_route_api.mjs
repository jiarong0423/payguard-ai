// Fuzzy case routing: the browser accepts only the closed routing shape (code decides, advisory only).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { apiRequest } from '../frontend/src/api.js';

const session = { session_id: 's'.repeat(43), csrf_token: 'c'.repeat(43) };
let reply = null;
globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(reply) });
const body = { text: 'wirless hedphones' };
const physical = { query: 'wirless hedphones', route: 'physical', reason: 'catalogue_match', matched_word: null,
  matches: [{ product_id: 'p1', title: 'Sony WH-1000XM6 Wireless Headphones', category: 'Over-Ear Headphones', score: 0.97,
    exact_words: ['sony', 'wh1000xm6'], match_type: 'exact' }],
  filtered_out: 1, items: ['ship date', 'carrier', 'tracking number'], decided_by: 'code', affects_decision: false };

async function check(payload, ok, label) {
  reply = payload;
  const run = apiRequest('/cases/route', { method: 'POST', body, session });
  if (ok) assert.deepEqual(await run, payload, label);
  else await assert.rejects(run, (error) => error.code === 'contract_error', label);
}

await check(physical, true, 'physical');
await check({ ...physical, route: 'digital', reason: 'digital_word', matched_word: 'ebook', matches: [], items: ['delivery channel'] }, true, 'digital');
await check({ ...physical, route: 'service', reason: 'service_word', matched_word: 'repair', matches: [], items: [] }, true, 'service');
await check({ ...physical, route: 'unknown', reason: 'no_close_match', matches: [], items: [] }, true, 'unknown');
await check({ ...physical, route: 'unknown', reason: 'filtered_conflict', matches: [], items: [], filtered_out: 3 }, true, 'filtered');
const mutations = [
  ['decision leak', { ...physical, affects_decision: true }],
  ['model decided', { ...physical, decided_by: 'model' }],
  ['physical without a match', { ...physical, matches: [] }],
  ['unknown with items', { ...physical, route: 'unknown', reason: 'no_close_match', matches: [] }],
  ['score above one', { ...physical, matches: [{ ...physical.matches[0], score: 1.5 }] }],
  ['price in a match', { ...physical, matches: [{ ...physical.matches[0], price: 24 }] }],
  ['unknown reason', { ...physical, reason: 'ai_guess' }],
  ['extra key', { ...physical, outcome: 'win' }],
  ['unknown match type', { ...physical, matches: [{ ...physical.matches[0], match_type: 'perfect' }] }],
  ['negative filter count', { ...physical, filtered_out: -1 }],
  ['markup in exact words', { ...physical, matches: [{ ...physical.matches[0], exact_words: ['<b>'] }] }],
];
for (const [label, payload] of mutations) await check(payload, false, label);
// Q24: the route result belongs to the text it was found for; editing the text clears it (GuideLive.jsx).
const guideLive = readFileSync(new URL('../frontend/src/GuideLive.jsx', import.meta.url), 'utf8');
assert.ok(guideLive.includes('const editRouteText = (value) => { setRouteText(value); setRoute(null); };'), 'an edit clears the route');
assert.ok(guideLive.includes('data-testid="guide-route-input"') && guideLive.includes('onChange={(event) => editRouteText(event.target.value)}'), 'the route input uses it');
assert.equal((guideLive.match(/setRouteText\(/gu) || []).length, 1, 'no other path changes the text without clearing the route');
console.log(`case route contract: ${mutations.length} mutations rejected; edit clears the route`);
