// Channel3 product reference: the browser accepts only the closed card shape the backend promises.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { apiRequest } from '../frontend/src/api.js';

const session = { session_id: 's'.repeat(43), csrf_token: 'c'.repeat(43) };
let reply = null;
globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(reply) });

const card = { product_id: 'prod_mug_1', title: 'Handmade Stoneware Coffee Mug, 12 oz', brand: 'Clay Works', category: 'Mugs',
  key_features: ['Dishwasher safe', '12 oz capacity'], materials: ['Stoneware'], image_url: 'https://cdn.example/main.png' };
const found = { status: 'FOUND', source: 'channel3_live', cards: [card, { ...card, product_id: 'p2', image_url: null, brand: null }],
  reason: null, recorded_at: null, affects_decision: false };
const lookupBody = { evaluation_id: 'E'.repeat(43), description: 'Ceramic mug' };
const confirmBody = { ...lookupBody, product_id: 'prod_mug_1' };
const confirmed = { choice: 'CONFIRMED', evaluation_id: 'E'.repeat(43), description_digest: 'a'.repeat(64), source: 'channel3_live',
  recorded_at: null, card, card_digest: 'b'.repeat(64), confirmed_by: 'seller', affects_decision: false };

async function accepts(path, body, payload) {
  reply = payload;
  return apiRequest(path, { method: 'POST', body, session });
}
async function rejects(path, body, payload, label) {
  reply = payload;
  await assert.rejects(apiRequest(path, { method: 'POST', body, session }), (error) => error.code === 'contract_error', label);
}

assert.deepEqual(await accepts('/aup/product-reference', lookupBody, found), found);
for (const payload of [
  { status: 'OFF', source: null, cards: [], reason: null, recorded_at: null, affects_decision: false },
  { status: 'NOT_FOUND', source: 'channel3_live', cards: [], reason: null, recorded_at: null, affects_decision: false },
  { status: 'NOT_SENT', source: null, cards: [], reason: 'not_recorded', recorded_at: null, affects_decision: false },
  { ...found, source: 'channel3_recorded', recorded_at: '2026-11-02T01:00:00Z' },
]) await accepts('/aup/product-reference', lookupBody, payload);

const mutations = [
  ['price leaks into a card', { ...found, cards: [{ ...card, price: 24 }] }],
  ['buy link replaces the image', { ...found, cards: [{ ...card, image_url: 'http://shop.example/buy' }] }],
  ['decision flag', { ...found, affects_decision: true }],
  ['four cards', { ...found, cards: [card, { ...card, product_id: 'a' }, { ...card, product_id: 'b' }, { ...card, product_id: 'c' }] }],
  ['duplicate card', { ...found, cards: [card, card] }],
  ['FOUND without cards', { ...found, cards: [] }],
  ['recorded without a time', { ...found, source: 'channel3_recorded' }],
  ['live with a recorded time', { ...found, recorded_at: '2026-11-02T01:00:00Z' }],
  ['unknown status', { ...found, status: 'MATCHED' }],
  ['markup in a title', { ...found, cards: [{ ...card, title: '<b>Mug</b>' }] }],
  ['extra key', { ...found, note: 'x' }],
];
for (const [label, payload] of mutations) await rejects('/aup/product-reference', lookupBody, payload, label);

assert.deepEqual(await accepts('/aup/product-reference/confirm', confirmBody, confirmed), confirmed);
await accepts('/aup/product-reference/confirm', { ...lookupBody, product_id: null },
  { ...confirmed, choice: 'NONE_MATCH', card: null, card_digest: null });
for (const [label, payload, body] of [
  ['a different card than asked', { ...confirmed, card: { ...card, product_id: 'p2' } }, confirmBody],
  ['confirmed by the model', { ...confirmed, confirmed_by: 'model' }, confirmBody],
  ['another evaluation', { ...confirmed, evaluation_id: 'F'.repeat(43) }, confirmBody],
  ['none match with a card', { ...confirmed, choice: 'NONE_MATCH' }, { ...lookupBody, product_id: null }],
  ['confirmed without a digest', { ...confirmed, card_digest: null }, confirmBody],
]) await rejects('/aup/product-reference/confirm', body, payload, label);

// Q8: a recorded-mode miss says the demo only replays the recorded searches (and names them), not the
// "removing personal details" text that belongs to nothing_to_send.
const view = readFileSync(new URL('../frontend/src/ProductReference.jsx', import.meta.url), 'utf8');
assert.match(view, /status === 'NOT_SENT' && result\.reason === 'not_recorded' \? NOT_RECORDED_TEXT/u);
const receipts = JSON.parse(readFileSync(new URL('../frontend/src/data/channel3_receipts_v1.json', import.meta.url), 'utf8'));
const recorded = JSON.parse(readFileSync(new URL('../backend/app/data/channel3_recorded_v1.json', import.meta.url), 'utf8'));
const recordedQueries = (recorded.entries || Object.values(recorded).find(Array.isArray) || []).map((entry) => entry.query).sort();
assert.deepEqual(receipts.receipts.map((receipt) => receipt.query).sort(), recordedQueries, 'the names shown are exactly the recorded searches');

// A failed catalogue image falls back to the plain tile instead of a broken image (sponsor review S3).
const cardSource = readFileSync(new URL('../frontend/src/ProductReference.jsx', import.meta.url), 'utf8');
assert.ok(cardSource.includes('onError={() => setImageFailed(true)}') && cardSource.includes('data-testid="product-card-noimg"'), 'image fallback');

console.log(`product reference contract: ${mutations.length + 5} mutations rejected`);
