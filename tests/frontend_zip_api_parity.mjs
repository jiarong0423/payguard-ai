import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { buildInternalReviewZip, validateInternalReviewZip } from '../frontend/src/reviewZip.js';

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
