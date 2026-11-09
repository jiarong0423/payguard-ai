"""Evidence-integrity checks as plain functions: no Render SDK import, no network, no secrets.

Each check rebuilds or reloads a committed evidence file and compares it with what is committed:

  guide_benchmark       tools/run_guide_benchmark.py --check   (wrong values must stay 0; the fresh numbers
                        must equal docs/evidence/guide_benchmark_current.json, ignoring its "commit" field)
  dashboard_data        tools/build_dashboard_data.py --check  (exit 1 on drift)
  channel3_recordings   backend/app/channel3_products.load_recorded must load every recorded entry back, and
                        docs/evidence/channel3_receipts_v1.json must match those entries one to one
  receipt               a JSON receipt (commit, task results, drift yes/no) with a sha256 over its content

On drift or failure a check prints one line starting with "ERROR" to stderr and raises IntegrityError, so a
Render task run fails and the command line (python -m workflows.evidence_integrity.tasks) exits non-zero.
Every check leaves the working tree exactly as it found it.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECEIPT_SCHEMA = "payguard.evidence_integrity_receipt.v1"
WORKFLOW_NAME = "payguard-evidence-integrity"
BENCHMARK_FILE = ROOT / "docs" / "evidence" / "guide_benchmark_current.json"
RECORDED_FILE = ROOT / "backend" / "app" / "data" / "channel3_recorded_v1.json"
RECEIPTS_FILE = ROOT / "docs" / "evidence" / "channel3_receipts_v1.json"
DEFAULT_RECEIPT_DIR = ROOT / "output" / "evidence_integrity"  # git-ignored
TOOL_TIMEOUT_SECONDS = {"guide_benchmark": 1500, "dashboard_data": 300}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
# The public source package leaves out tools/run_guide_benchmark.py, so a run from the public repository has
# two checks; a run from the full project tree has three. The receipt lists exactly the checks that exist.
_ALL_CHECK_NAMES = ("guide_benchmark", "dashboard_data", "channel3_recordings")
CHECK_NAMES = tuple(name for name in _ALL_CHECK_NAMES
                    if name != "guide_benchmark" or (ROOT / "tools" / "run_guide_benchmark.py").exists())


class IntegrityError(Exception):
    """A check found drift or could not complete. The message is one line, no file contents, and starts with
    DRIFT or FAILED so a caller that only sees the text (a Render subtask error) can tell the two apart."""

    def __init__(self, task: str, reason: str, result: dict | None = None, drift: bool = False):
        self.task, self.reason, self.result, self.drift = task, reason, result, drift
        super().__init__(f"{'DRIFT' if drift else 'FAILED'} {task}: {reason}")


def _fail(task: str, reason: str, result: dict) -> None:
    error = IntegrityError(task, reason, result, drift=bool(result.get("drift")))
    print(f"ERROR {error}", file=sys.stderr, flush=True)
    raise error


def drift_from_message(message: str) -> bool:
    """True when an error text (for example a Render TaskRunError) carries the DRIFT marker."""
    return re.search(r"(?:^|\W)DRIFT \w", message) is not None


def _environment() -> dict:
    env = {key: value for key, value in os.environ.items() if key in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": f"{ROOT / 'src'}{os.pathsep}{ROOT / 'backend'}"})
    return env


def _run_tool(task: str, arguments: list[str], runner=subprocess.run) -> tuple[int, str, float]:
    started = time.monotonic()
    try:
        completed = runner([sys.executable, *arguments], cwd=ROOT, env=_environment(), capture_output=True, text=True,
                           timeout=TOOL_TIMEOUT_SECONDS[task], check=False)
    except subprocess.TimeoutExpired:
        return -1, "timed out", round(time.monotonic() - started, 3)
    last = (completed.stdout.strip().splitlines() or completed.stderr.strip().splitlines() or [""])[-1]
    return completed.returncode, last[:300], round(time.monotonic() - started, 3)


def _numbers(document: dict) -> dict:
    """The benchmark minus its commit stamp: the part that must not drift."""
    return {key: value for key, value in document.items() if key != "commit"}


def check_guide_benchmark(runner=subprocess.run) -> dict:
    """Task 1: rebuild the guide benchmark; zero wrong values and no change against the committed numbers."""
    task = "guide_benchmark"
    committed = BENCHMARK_FILE.read_bytes() if BENCHMARK_FILE.is_file() else None
    try:
        code, last, seconds = _run_tool(task, [str(ROOT / "tools" / "run_guide_benchmark.py"), "--check"], runner)
        fresh = json.loads(BENCHMARK_FILE.read_text(encoding="utf-8")) if BENCHMARK_FILE.is_file() else None
    finally:
        if committed is not None:
            BENCHMARK_FILE.write_bytes(committed)  # the tool rewrites the file; a check must not change the tree
    result = {"task": task, "exit_code": code, "seconds": seconds, "detail": last, "drift": False, "ok": False}
    if committed is None or fresh is None:
        result["drift"] = True
        _fail(task, "docs/evidence/guide_benchmark_current.json is missing", result)
    if code != 0:
        result["drift"] = code == 1
        _fail(task, f"run_guide_benchmark.py --check exited {code}: {last}", result)
    if _numbers(fresh) != _numbers(json.loads(committed)):
        result["drift"] = True
        _fail(task, "fresh benchmark numbers differ from docs/evidence/guide_benchmark_current.json", result)
    result["ok"] = True
    return result


def check_dashboard_data(runner=subprocess.run) -> dict:
    """Task 2: rebuild the dashboard data and compare it with the committed files."""
    task = "dashboard_data"
    code, last, seconds = _run_tool(task, [str(ROOT / "tools" / "build_dashboard_data.py"), "--check"], runner)
    result = {"task": task, "exit_code": code, "seconds": seconds, "detail": last, "drift": code == 1, "ok": code == 0}
    if code != 0:
        _fail(task, f"build_dashboard_data.py --check exited {code}: {last}", result)
    return result


def check_channel3_recordings(recorded_file: pathlib.Path = RECORDED_FILE, receipts_file: pathlib.Path = RECEIPTS_FILE) -> dict:
    """Task 3: every recorded Channel3 entry loads back through load_recorded, and the receipts match them."""
    task = "channel3_recordings"
    started = time.monotonic()
    for path in (str(ROOT / "src"), str(ROOT / "backend")):
        if path not in sys.path:
            sys.path.insert(0, path)
    from app.channel3_products import RESULT_LIMIT, load_recorded

    problems = []
    try:
        raw_entries = json.loads(recorded_file.read_text(encoding="utf-8")).get("entries", [])
        raw_receipts = json.loads(receipts_file.read_text(encoding="utf-8"))
    except (OSError, ValueError, AttributeError) as error:
        raw_entries, raw_receipts = [], {}
        problems.append(f"cannot read the recorded or receipt file ({type(error).__name__})")
    loaded = load_recorded(recorded_file)
    if len(loaded) != len(raw_entries) or not loaded:
        problems.append(f"load_recorded returned {len(loaded)} of {len(raw_entries)} recorded entries")
    if raw_receipts.get("schema_version") != "payguard.channel3_receipts.v1":
        problems.append("receipt schema_version is not payguard.channel3_receipts.v1")
    receipts = raw_receipts.get("receipts") if type(raw_receipts.get("receipts")) is list else []
    found = {}
    for receipt in receipts:
        query = receipt.get("query") if type(receipt) is dict else None
        if type(query) is not str or not _SHA256.match(str(receipt.get("reply_sha256"))):
            problems.append("a receipt has no query or no sha256 of its reply")
            continue
        if receipt.get("result_status") == "FOUND":
            found[query] = receipt
    for query, entry in loaded.items():
        receipt = found.get(query)
        if receipt is None:
            problems.append(f"recorded entry without a FOUND receipt: {query}")
        elif receipt.get("cards") != len(entry["cards"]) or receipt.get("called_at") != entry["recorded_at"]:
            problems.append(f"receipt and recording disagree: {query}")
        if not 0 < len(entry["cards"]) <= RESULT_LIMIT:
            problems.append(f"recorded entry has {len(entry['cards'])} cards: {query}")
    for query in found:
        if query not in loaded:
            problems.append(f"FOUND receipt without a loadable recording: {query}")
    result = {"task": task, "exit_code": 0 if not problems else 1, "seconds": round(time.monotonic() - started, 3),
              "detail": f"{len(loaded)} recordings, {len(receipts)} receipts" if not problems else problems[0],
              "drift": bool(problems), "ok": not problems, "recordings": len(loaded), "receipts": len(receipts)}
    if problems:
        _fail(task, f"{len(problems)} problem(s); first: {problems[0]}", result)
    return result


def current_commit() -> str:
    """The checked-out commit: git first, then RENDER_GIT_COMMIT (see the notes; that name is UNREAD), else unknown."""
    try:
        commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True,
                                timeout=10, check=False).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = ""
    if re.fullmatch(r"[0-9a-f]{40}", commit):
        return commit
    env = os.environ.get("RENDER_GIT_COMMIT", "")
    return env if re.fullmatch(r"[0-9a-f]{7,40}", env) else "unknown"


def build_receipt(results: list[dict], commit: str | None = None, now: datetime | None = None) -> dict:
    """Task 4 body: the receipt document. A digest over the canonical content, not a cryptographic signature."""
    by_name = {row["task"]: row for row in results}
    tasks = [by_name.get(name, {"task": name, "ok": False, "drift": False, "exit_code": None, "seconds": None,
                                "detail": "did not run"}) for name in CHECK_NAMES]
    body = {
        "schema_version": RECEIPT_SCHEMA,
        "workflow": WORKFLOW_NAME,
        "commit": commit or current_commit(),
        "created_at": (now or datetime.now(timezone.utc)).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "tasks": tasks,
        "drift": any(task["drift"] for task in tasks),
        "ok": all(task["ok"] for task in tasks),
        "secrets_used": False,
        "network_used": False,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return dict(body, content_sha256=hashlib.sha256(canonical).hexdigest())


def verify_receipt(receipt: dict) -> bool:
    body = {key: value for key, value in receipt.items() if key != "content_sha256"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return receipt.get("content_sha256") == hashlib.sha256(canonical).hexdigest()


def write_receipt(results: list[dict], out_dir: pathlib.Path = DEFAULT_RECEIPT_DIR, commit: str | None = None,
                  now: datetime | None = None) -> dict:
    """Task 4: write the receipt as an artifact file, print it as one RECEIPT log line, and fail on drift."""
    receipt = build_receipt(results, commit, now)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"receipt_{receipt['commit'][:12]}.json"
    path.write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("RECEIPT " + json.dumps(receipt, sort_keys=True, separators=(",", ":")), flush=True)
    if not receipt["ok"]:
        failed = [task["task"] for task in receipt["tasks"] if not task["ok"]]
        _fail("receipt", f"{'drift' if receipt['drift'] else 'failure'} in {', '.join(failed)}; receipt {path.name}", receipt)
    return dict(receipt, path=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path))


CHECKS = {name: check for name, check in (("guide_benchmark", check_guide_benchmark), ("dashboard_data", check_dashboard_data),
                                          ("channel3_recordings", check_channel3_recordings)) if name in CHECK_NAMES}


def run_all(checks: dict | None = None, out_dir: pathlib.Path = DEFAULT_RECEIPT_DIR) -> dict:
    """The whole workflow in one process: every check runs (a failure does not stop the others), then the receipt."""
    results = []
    for name, check in (checks or CHECKS).items():
        try:
            results.append(check())
        except IntegrityError as error:
            results.append(error.result or {"task": name, "ok": False, "drift": False, "exit_code": None,
                                            "seconds": None, "detail": error.reason})
    return write_receipt(results, out_dir)


def main(argv: list[str] | None = None) -> int:
    try:
        receipt = run_all()
    except IntegrityError:
        return 1
    print(f"evidence integrity OK: {receipt['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
