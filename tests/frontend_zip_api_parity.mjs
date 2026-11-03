import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { buildInternalReviewZip, canonicalCardJson, productCardDigest, validateInternalReviewZip } from '../frontend/src/reviewZip.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
assert.ok(existsSync(python), 'PAYGUARD_RUNTIME_MISSING');

const pythonProgram = String.raw`
import json
from datetime import datetime, timezone
from fastapi.testclient import TestClient
import httpx
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore

now = datetime(2026, 10, 8, 8, 0, tzinfo=timezone.utc)
provider_calls = []

def reject_provider_call(request):
    provider_calls.append(str(request.url))
    raise AssertionError("provider call forbidden")

store = SessionStore(clock=lambda: now)
provider = PaypalAdapter(
    config_loader=lambda: PaypalConfig(),
    transport=httpx.MockTransport(reject_provider_call),
    clock=lambda: now,
)
application = create_app(store=store, paypal=provider)
with TestClient(
    application,
    base_url="http://127.0.0.1:8000",
    client=("127.0.0.1", 55001),
    raise_server_exceptions=False,
) as client:
    origin = "http://localhost:5173"
    root = "/api/v1"
    session_response = client.post(root + "/demo/sessions", json={}, headers={"Origin": origin})
    assert session_response.status_code == 201, session_response.text
    session = session_response.json()
    headers = {
        "Origin": origin,
        "X-Demo-Session": session["session_id"],
        "X-CSRF-Token": session["csrf_token"],
    }
    injected = client.post(root + "/demo/inject", json={"scenario": "dispute"}, headers=headers)
    assert injected.status_code == 200, injected.text
    draft_response = client.post(root + "/disputes/case-ref-001/draft", json={}, headers=headers)
    assert draft_response.status_code == 200, draft_response.text
    assert provider_calls == []
    print(json.dumps(draft_response.json(), sort_keys=True, separators=(",", ":")))
assert provider.open_clients == 0
`;

const environment = {
  ...process.env,
  PYTHONDONTWRITEBYTECODE: '1',
  PYTHONPATH: `${resolve(projectRoot, 'src')}:${resolve(projectRoot, 'backend')}`,
};
const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: environment,
  encoding: 'utf8',
  maxBuffer: 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const draft = JSON.parse(generated.stdout.trim());

assert.equal(draft.source, 'synthetic');
assert.equal(draft.policy_version, 'payguard.demo.v1');
assert.equal(draft.status, 'review_evidence');
assert.equal(draft.evidence.carrier_status, 'delivered');
assert.equal(draft.scenario_match.scenario.citations.length, 5);
assert.deepEqual(draft.document_redaction.types, ['address', 'email', 'id_like', 'manual', 'name', 'us_phone']);

const archive = buildInternalReviewZip(draft);
assert.equal(validateInternalReviewZip(archive), true);
assert.ok(archive.length > 0 && archive.length <= 262144);

for (const unsupportedStatus of ['DELIVERED', 'pending', 'delivered ']) {
  const invalid = structuredClone(draft);
  invalid.evidence.carrier_status = unsupportedStatus;
  assert.throws(() => buildInternalReviewZip(invalid), /internal_review_zip_invalid/u);
}

console.log(JSON.stringify({
  status: 'PASS',
  api_carrier_status: draft.evidence.carrier_status,
  citation_count: draft.scenario_match.scenario.citations.length,
  document_redaction_type_count: draft.document_redaction.types.length,
  archive_bytes: archive.length,
  provider_calls: 0,
}));

// Card digest parity: the ZIP recomputes card_digest exactly as backend/app/channel3_products.card_digest does.
// Every recorded Channel3 card, plus cards with quotes, a backslash, a slash, null fields, non-ASCII and an astral
// character (the backend's own reduction keeps cards ASCII; the canonical form must still agree on anything).
const digestProgram = String.raw`
import json, sys
from app.channel3_products import CARD_KEYS, RECORDED_PATH, card_digest
recorded = json.loads(RECORDED_PATH.read_text(encoding="utf-8"))
cards = [card for entry in recorded["entries"] for card in entry["cards"]]
cards += [
    {"product_id": "p.1", "title": 'Mug "Classic" 12 oz / blue', "brand": None, "category": None, "key_features": [], "materials": [], "image_url": None},
    {"product_id": "p:2", "title": "Café cup \\ saucer — set", "brand": "Brüder", "category": "Cups", "key_features": ["\U0001F375 tea", "line\nbreak"], "materials": ["Porzellan ä"], "image_url": "https://cdn.example/x.png"},
]
print(json.dumps([{"card": card, "canonical": json.dumps({key: card[key] for key in CARD_KEYS}, sort_keys=True, separators=(",", ":"), ensure_ascii=True), "digest": card_digest(card)} for card in cards]))
`;
const digests = spawnSync(python, ['-c', digestProgram], { cwd: projectRoot, env: environment, encoding: 'utf8' });
assert.equal(digests.status, 0, digests.stderr || digests.stdout);
const digestCases = JSON.parse(digests.stdout.trim());
assert.ok(digestCases.length >= 7, 'recorded cards and edge cases');
for (const { card, canonical, digest } of digestCases) {
  assert.equal(canonicalCardJson(card), canonical, `canonical JSON matches Python for ${card.product_id}`);
  assert.equal(productCardDigest(card), digest, `card_digest matches Python for ${card.product_id}`);
}
console.log(JSON.stringify({ status: 'PASS', card_digest_parity: digestCases.length }));

