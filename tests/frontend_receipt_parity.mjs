// (red team A 2026-11-04 P2) Receipt parity: the console's Sandbox receipt check must accept exactly what the backend
// builds. The 653111a mismatch (paypal_debug_id added on the backend, missing in api.js) passed every suite because
// the frontend fixtures were hand-written; here the receipts come from backend/app/paypal.py itself.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { assertSandboxReceipt } from '../frontend/src/api.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const python = process.env.PAYGUARD_PYTHON_BIN || resolve(projectRoot, '.venv/bin/python3');
// Fail closed with a greppable reason when the backend runtime is missing (never a TypeError, never a pass).
if (!existsSync(python)) {
  console.error(`ERROR PAYGUARD_RUNTIME_MISSING: no Python runtime at ${python}; create .venv or set PAYGUARD_PYTHON_BIN`);
  process.exit(1);
}
const pythonProgram = String.raw`
import json
from datetime import datetime, timezone
from app.paypal import PaypalAdapter

now = datetime(2026, 11, 4, 4, 27, 19, 769443, tzinfo=timezone.utc)
build = PaypalAdapter._receipt
cases = []
for debug_id in (None, "ca550dd96ddb1"):
    for evidence_class in ("AUTHENTIC_SANDBOX_RESPONSE", "SYNTHETIC_TEST_RESPONSE"):
        cases.append({"action": "OAUTH_CONNECT", "invoice_id": None, "receipt": build(
            None, "OAUTH_CONNECT", "CONNECTED", now, evidence_class=evidence_class, debug_id=debug_id)})
        cases.append({"action": "CREATE_INVOICE_DRAFT", "invoice_id": "INV2-SYNT-AB12-CD34-TEST", "receipt": build(
            None, "CREATE_INVOICE_DRAFT", "DRAFT", now, "INV2-SYNT-AB12-CD34-TEST", evidence_class=evidence_class,
            debug_id=debug_id)})
print(json.dumps(cases, separators=(",", ":")))
`;
const generated = spawnSync(python, ['-c', pythonProgram], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${resolve(projectRoot, 'src')}:${resolve(projectRoot, 'backend')}` },
  encoding: 'utf8',
  maxBuffer: 1024 * 1024,
});
assert.equal(generated.status, 0, `ERROR receipt generator failed: ${generated.stderr || generated.stdout || String(generated.error)}`);
const cases = JSON.parse(generated.stdout.trim());
assert.equal(cases.length, 8);
for (const { action, invoice_id: invoiceId, receipt } of cases) {
  assert.deepEqual(assertSandboxReceipt(structuredClone(receipt), action, invoiceId), receipt, `${action} ${receipt.paypal_debug_id}`);
}
console.log(JSON.stringify({ status: 'PASS', receipts: cases.length, keys: Object.keys(cases[0].receipt).sort() }));
