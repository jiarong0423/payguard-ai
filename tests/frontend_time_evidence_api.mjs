import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { apiRequest } from '../frontend/src/api.js';
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
    first = client.post(root + "/disputes/case-ref-001/draft", json={}, headers=headers)
    second = client.post(root + "/disputes/case-ref-002/draft", json={}, headers=headers)
    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert provider_calls == []
    print(json.dumps({"first": first.json(), "second": second.json()}, sort_keys=True, separators=(",", ":")))
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
  maxBuffer: 2 * 1024 * 1024,
});
assert.equal(generated.status, 0, generated.stderr || generated.stdout);
const { first, second } = JSON.parse(generated.stdout.trim());
const session = { session_id: 'synthetic-session', csrf_token: 'synthetic-csrf' };

function stubFetch(payload) {
  globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => structuredClone(payload) });
}
async function loadDraft(caseRef, payload) {
  stubFetch(payload);
  return apiRequest(`/disputes/${caseRef}/draft`, { method: 'POST', body: {}, session });
}

// Case one carries no time evidence and is accepted unchanged.
assert.equal('time_evidence' in first, false);
const acceptedFirst = await loadDraft('case-ref-001', first);
assert.equal('time_evidence' in acceptedFirst, false);

// Case two carries the ordered time evidence and is accepted.
const evidence = second.time_evidence;
assert.equal(evidence.schema_version, 'payguard.time_evidence.v1');
assert.deepEqual(evidence.flags, ['DELIVERY_AFTER_CLAIM']);
assert.equal(evidence.judgement, 'NOT_MADE');
assert.equal(evidence.events.filter((row) => row.kind === 'MESSAGE').length, 4);
const acceptedSecond = await loadDraft('case-ref-002', second);
assert.deepEqual(acceptedSecond.time_evidence, evidence);
assert.equal(validateInternalReviewZip(buildInternalReviewZip(acceptedSecond)), true, 'real API draft builds a valid ZIP');
assert.equal(JSON.stringify(evidence).includes('Synthetic message'), false, 'no message text in the API response');

// The validator rejects every drift of the time evidence block.
const mutations = [
  (value) => { value.time_evidence.unknown = true; },
  (value) => { value.time_evidence.judgement = 'LIKELY_FRAUD'; },
  (value) => { value.time_evidence.advisory_only = false; },
  (value) => { value.time_evidence.events[1].body = 'text'; },
  (value) => { value.time_evidence.events[1].message_digest = 'F'.repeat(64); },
  (value) => { value.time_evidence.events[0].source = 'PROVIDER_VERIFIED'; },
  (value) => { value.time_evidence.events[0].at = 'yesterday'; },
  (value) => { value.time_evidence.events = [value.time_evidence.events[0]]; },
  (value) => { value.time_evidence.gaps_seconds.payment_to_claim = 1.5; },
  (value) => { value.time_evidence.gaps_seconds.extra = 1; },
  (value) => { value.time_evidence.flags = ['BUYER_ACTED_IN_BAD_FAITH']; },
  (value) => { value.time_evidence.flags = ['DELIVERY_AFTER_CLAIM', 'DELIVERY_AFTER_CLAIM']; },
  (value) => { value.time_evidence = null; },
  (value) => { value.surprise = true; },
];
for (const mutate of mutations) {
  const value = structuredClone(second);
  mutate(value);
  await assert.rejects(() => loadDraft('case-ref-002', value), (error) => error.code === 'contract_error');
}

console.log(JSON.stringify({ status: 'PASS', time_evidence_events: evidence.events.length, mutations_rejected: mutations.length, provider_calls: 0 }));
