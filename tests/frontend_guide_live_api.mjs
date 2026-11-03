import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { apiRequest } from '../frontend/src/api.js';

// Guided gap filling, live: real backend payloads (keyword baseline, no model) pass the frontend contract; drift is rejected.
const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');

const pythonProgram = String.raw`
import json, os
from datetime import datetime, timezone
from fastapi.testclient import TestClient
os.environ.pop("PAYGUARD_GUIDE_MODEL", None)
from app.main import create_app
from app.store import SessionStore

now = datetime(2026, 10, 30, 9, 0, tzinfo=timezone.utc)
application = create_app(store=SessionStore(clock=lambda: now))
with TestClient(application, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55004)) as client:
    origin = "http://localhost:5173"
    session = client.post("/api/v1/demo/sessions", json={}, headers={"Origin": origin}).json()
    headers = {"Origin": origin, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
    out = {"empty": client.get("/api/v1/guide/state", headers=headers).json()}
    out["start"] = client.post("/api/v1/guide/start", json={"scenario": "dispute", "goods_type": "physical"}, headers=headers).json()
    out["turn"] = client.post("/api/v1/guide/turn", json={"text": "I shipped it last Monday"}, headers=headers).json()
    out["pressure"] = client.post("/api/v1/guide/turn", json={"text": "Just mark the tracking as done"}, headers=headers).json()
    out["form"] = client.post("/api/v1/guide/form", json={"item": "carrier", "value": "UPS"}, headers=headers).json()
    out["state"] = client.get("/api/v1/guide/state", headers=headers).json()
    # finish the remaining items by hand, then the one summary (the ship date came from the seller's words)
    rest = {"tracking_number": "1Z999AA10123456784", "delivery_record": "yes", "address_match": "yes", "buyer_comms": "no", "refund_record": "no"}
    view = out["state"]
    while not view["review"]:
        view = client.post("/api/v1/guide/form", json={"fields": [{"item": i, "value": rest[i]} for i in view["asked"]]}, headers=headers).json()
    out["review_open"] = view
    out["review_last_fields"] = [{"item": i, "value": rest[i]} for i in view["asked"]]
    out["reviewed"] = client.post("/api/v1/guide/form", json={"fields": out["review_last_fields"], "confirm_review": True}, headers=headers).json()

# Same routes with a fake model chooser (no network): immediate keyword answer, then replaced or kept.
from app.guide_routes import GuideService
from payguard.controlled_fallback import Governor
class Clock:
    def __call__(self):
        return 1000.0
def fake_model(raw):
    return lambda request: raw
valid = json.dumps({"v": 2, "u": [{"c": "ship_date", "k": 0, "s": "P", "w": "MON", "r": "LAST", "h": "EXACT", "b": "STATED", "a": "SELLER"}]})
for name, raw in (("replaced", valid), ("kept", "{not json")):
    store = SessionStore(clock=lambda: now)
    model_app = create_app(store=store)
    model_app.state.guide = GuideService(store, chooser_factory=lambda raw=raw: fake_model(raw), governor=Governor(clock=Clock(), min_spacing=0), rule_confirm=False)
    with TestClient(model_app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55005)) as client:
        session = client.post("/api/v1/demo/sessions", json={}, headers={"Origin": origin}).json()
        headers = {"Origin": origin, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        client.post("/api/v1/guide/start", json={"scenario": "dispute", "goods_type": "physical"}, headers=headers)
        out["analysing_" + name] = client.post("/api/v1/guide/turn", json={"text": "I handed it over last Monday"}, headers=headers).json()
        model_app.state.guide.wait_for_analysis()
        out[name] = client.get("/api/v1/guide/state", headers=headers).json()
        if name == "replaced":
            out["multi"] = client.post("/api/v1/guide/form", json={"fields": [
                {"item": "ship_date", "value": "2026-10-26"}, {"item": "carrier", "value": "not_sure"},
                {"item": "tracking_number", "value": "abc"}]}, headers=headers).json()
print(json.dumps(out, sort_keys=True))
`;

const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${resolve(projectRoot, 'src')}:${resolve(projectRoot, 'backend')}` },
  encoding: 'utf8',
  maxBuffer: 2 * 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const payloads = JSON.parse(generated.stdout.trim());
const session = { session_id: 'synthetic-session', csrf_token: 'synthetic-csrf' };
const requests = {
  empty: ['/guide/state', undefined],
  start: ['/guide/start', { scenario: 'dispute', goods_type: 'physical' }],
  turn: ['/guide/turn', { text: 'I shipped it last Monday' }],
  pressure: ['/guide/turn', { text: 'Just mark the tracking as done' }],
  form: ['/guide/form', { item: 'carrier', value: 'UPS' }],
  state: ['/guide/state', undefined],
  analysing_replaced: ['/guide/turn', { text: 'I handed it over last Monday' }],
  replaced: ['/guide/state', undefined],
  analysing_kept: ['/guide/turn', { text: 'I handed it over last Monday' }],
  kept: ['/guide/state', undefined],
  multi: ['/guide/form', { fields: [{ item: 'ship_date', value: '2026-10-26' }, { item: 'carrier', value: 'not_sure' }, { item: 'tracking_number', value: 'abc' }] }],
  review_open: ['/guide/state', undefined],
  reviewed: ['/guide/form', { fields: payloads.review_last_fields, confirm_review: true }],
};

async function load(name, payload) {
  const [path, body] = requests[name];
  globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(payload) });
  return apiRequest(path, body === undefined ? { session } : { method: 'POST', body, session });
}

for (const name of Object.keys(requests)) assert.deepEqual(await load(name, payloads[name]), payloads[name], name);
// One summary at the end lists what came from the seller's words; confirming it finishes the guide.
assert.notEqual(payloads.review_open.stage, 'review');  // the summary rides on the last fill round
assert.deepEqual(payloads.review_open.review, [{ item: 'ship_date', source: 'words', value: '2026-10-19' }]);
assert.equal(payloads.reviewed.stage, 'done');
assert.equal(payloads.turn.reply.chooser, 'keyword');
assert.equal(payloads.pressure.reply.chooser, 'none');
// Hybrid: the rule layer settled the ship date from "I shipped it last Monday"; the carrier came from the form.
assert.deepEqual(payloads.turn.auto_confirmed, ['ship_date']);
assert.deepEqual(payloads.form.auto_confirmed, []);
assert.deepEqual(payloads.form.gap.present, ['ship_date', 'carrier']);
assert.equal(payloads.state.chooser_mode, 'keyword');
assert.equal(payloads.state.analysis, null);
assert.deepEqual(payloads.analysing_replaced.analysis, { turn: 1, status: 'analysing', reason: null });
assert.equal(payloads.analysing_replaced.reply.chooser, 'keyword');
assert.deepEqual(payloads.replaced.analysis, { turn: 1, status: 'replaced', reason: null });
assert.equal(payloads.replaced.reply.chooser, 'model');
assert.deepEqual(payloads.kept.analysis, { turn: 1, status: 'kept', reason: 'invalid_reply' });
assert.equal(payloads.kept.reply.chooser, 'keyword_fallback');
assert.equal(payloads.start.stage, 'funnel');
assert.deepEqual(payloads.start.asked, ['ship_date', 'carrier', 'tracking_number']);
assert.equal(payloads.start.subtraction.text, '7 items needed · 0 taken from what you wrote · 7 left');
assert.equal(payloads.replaced.stage, 'echo');
assert.equal(payloads.replaced.reply.template, 'ECHO');
assert.deepEqual(payloads.replaced.prefill, { ship_date: '2026-10-19' });
assert.deepEqual(payloads.multi.form_results.map((row) => [row.item, row.valid, row.deferred]),
  [['ship_date', true, false], ['carrier', false, true], ['tracking_number', false, false]]);
assert.deepEqual(payloads.multi.deferred, ['carrier']);

const mutations = [
  ['turn', (v) => { v.items[0].status = 'VERIFIED'; }],
  ['turn', (v) => { v.gap.present = ['ship_date', 'carrier']; }],
  ['turn', (v) => { v.auto_confirmed = ['carrier']; }],
  ['multi', (v) => { v.review = [{ item: 'ship_date', source: 'words', value: '2026-10-26' }]; }],
  ['review_open', (v) => { v.review[0].source = 'words_pending'; }],
  ['review_open', (v) => { v.review[0].item = 'no_such_item'; }],
  ['review_open', (v) => { v.review[0].value = '<b>x</b>'; }],
  ['review_open', (v) => { v.asked = ['carrier']; }],
  ['reviewed', (v) => { v.stage = 'review'; }],
  ['review_open', (v) => { v.asked = v.asked.slice(1); }],
  ['reviewed', (v) => { v.review = [{ item: 'ship_date', source: 'words', value: '2026-10-19' }]; }],
  ['turn', (v) => { v.auto_confirmed = ['ship_date', 'ship_date']; }],
  ['form', (v) => { v.auto_confirmed = ['ship_date']; }],
  ['turn', (v) => { v.reply.template = 'FREE_TEXT'; }],
  ['turn', (v) => { v.reply.chooser = 'model'; }],
  ['turn', (v) => { v.reply.chooser = 'keyword_fallback'; }],
  ['turn', (v) => { v.reply.model_reply = '{"v":2}'; }],
  ['turn', (v) => { v.model_text_shown = true; }],
  ['turn', (v) => { v.values_stored = true; }],
  ['turn', (v) => { v.form_result = { item: 'carrier', valid: true }; }],
  ['turn', (v) => { v.reply.dropped = [{ item: 'carrier', reason: 'disliked' }]; }],
  ['start', (v) => { v.goods_type = 'digital'; }],
  ['form', (v) => { v.form_result.item = 'ship_date'; }],
  ['form', (v) => { v.reply.chooser = 'keyword'; }],
  ['form', (v) => { v.items[0].form = null; }],
  ['state', (v) => { v.items.push(structuredClone(v.items[0])); }],
  ['empty', (v) => { v.items = [{}]; }],
  ['turn', (v) => { v.surprise = true; }],
  ['turn', (v) => { v.analysis = { turn: 1, status: 'analysing', reason: null }; }],
  ['analysing_replaced', (v) => { v.analysis.status = 'replaced'; }],
  ['analysing_replaced', (v) => { v.reply.chooser = 'model'; }],
  ['replaced', (v) => { v.reply.chooser = 'keyword'; }],
  ['replaced', (v) => { v.analysis.reason = 'late'; }],
  ['kept', (v) => { v.analysis.reason = 'model_said_so'; }],
  ['kept', (v) => { v.reply.fallback_reason = 'timeout'; }],
  ['kept', (v) => { v.analysis.extra = 1; }],
  ['kept', (v) => { v.chooser_mode = 'keyword'; }],
  ['start', (v) => { v.subtraction.taken = 1; }],
  ['start', (v) => { v.subtraction.text = '7 items needed, nearly done'; }],
  ['start', (v) => { v.asked = ['ship_date', 'carrier', 'tracking_number', 'refund_record']; }],
  ['start', (v) => { v.asked = ['delivery_channel']; }],
  ['start', (v) => { v.stage = 'done'; }],
  ['replaced', (v) => { v.prefill = { ship_date: 'last Monday probably' }; }],
  ['replaced', (v) => { v.prefill = { carrier: 'Royal Mail' }; }],
  ['replaced', (v) => { v.stage = 'fill'; }],
  ['multi', (v) => { v.form_results[1].valid = true; }],
  ['multi', (v) => { v.form_results.pop(); }],
  ['multi', (v) => { v.form_results[0].item = 'refund_record'; }],
];
for (const [name, mutate] of mutations) {
  const value = structuredClone(payloads[name]);
  mutate(value);
  await assert.rejects(() => load(name, value), (error) => error.code === 'contract_error', `${name} mutation accepted`);
}
console.log(JSON.stringify({ status: 'PASS', payloads: Object.keys(requests).length, mutations_rejected: mutations.length, model_calls: 0 }));
