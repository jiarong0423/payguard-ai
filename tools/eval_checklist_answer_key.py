#!/usr/bin/env python3
"""Run the checklist answer key against payguard.dispute_evidence.resolve_dispute_requirements.

In-process only: no network, no server, no PayPal or model call, no file writes unless --out is given.
Deterministic: fixed evaluation instant taken from the answer key, cases processed in key order.

Usage: .venv/bin/python3 -B tools/eval_checklist_answer_key.py [--key PATH] [--out PATH] [--json] [--fail-on-danger]
Exit codes: 0 ok, 2 answer key invalid or program import failed, 3 danger errors present with --fail-on-danger.
"""
import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
log = logging.getLogger("eval_checklist_answer_key")

try:
    from payguard.dispute_evidence import DisputeEvidenceError, resolve_dispute_requirements
except Exception as exc:  # fail loudly, never report a pass
    print("ERROR cannot import payguard.dispute_evidence: %s" % type(exc).__name__, file=sys.stderr)
    sys.exit(2)

TYPE_TO_LOCAL = {"PROOF_OF_FULFILLMENT": "FULFILLMENT", "PROOF_OF_REFUND": "REFUND", "OTHER": "OTHER"}
MAGIC = {"pdf": b"%PDF-1.4\n"}
OVERALL_TO_VERDICT = {
    "READY_FOR_LOCAL_REVIEW": "SUFFICIENT",
    "NEEDS_INPUT": "INSUFFICIENT",
    "MANUAL_REVIEW": "MANUAL_REVIEW",
    "CASE_NOT_ACTIONABLE": "NOT_ACTIONABLE",
    "DUE_DATE_EXPIRED": "NOT_ACTIONABLE",
    "ACTION_NOT_AVAILABLE": "NOT_ACTIONABLE",
}
VERDICTS = {"SUFFICIENT", "INSUFFICIENT", "MANUAL_REVIEW", "NOT_ACTIONABLE"}


def load_key(path):
    key = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = key["cases"]
    ids = [c["case_id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id")
    for c in cases:
        if c["expected"]["verdict"] not in VERDICTS:
            raise ValueError("bad verdict in " + c["case_id"])
    return key


def adapt(key, c):
    """Translate one key case into the program's closed input schema. No coercion of content."""
    snapshot = {
        "schema_version": 1, "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
        "observed_at": key["snapshot_observed_at"], "dispute_id": "ak-" + c["case_id"], "order_id": "ak-order",
        "reason": c["reason"], "status": c["status"], "dispute_life_cycle_stage": c["stage"],
        "seller_response_due_date": c["seller_response_due_date"],
        "available_actions": list(c["available_actions"]), "evidences": [dict(r) for r in c["requests"]],
    }
    proofs, attachments = [], []
    for item in c["provided_evidence"]:
        att_ids = []
        for a in item["attachments"]:
            size = a["size_bytes"]
            body = MAGIC[a["magic"]]
            body = body + b"x" * max(0, size - len(body))
            attachments.append({"attachment_id": a["attachment_id"], "evidence_id": item["evidence_id"],
                                "filename": a["filename"], "declared_media_type": a["media_type"], "content": body})
            att_ids.append(a["attachment_id"])
        proofs.append({
            "evidence_id": item["evidence_id"], "request_id": item["for_request"],
            "evidence_type": TYPE_TO_LOCAL.get(item["provided_type"], item["provided_type"]),
            "proof_fields": dict(item["fields"]), "observed_at": item["observed_at"],
            "evidence_state": item["evidence_state"], "attachment_ids": att_ids,
        })
    return snapshot, proofs, attachments


def run_case(key, c):
    try:
        snapshot, proofs, attachments = adapt(key, c)
        out = resolve_dispute_requirements(snapshot, proofs, attachments, key["as_of"])
    except DisputeEvidenceError as exc:
        return {"verdict": "REJECTED", "overall": None, "code": str(exc), "missing": None}
    except Exception as exc:
        log.error("%s unexpected %s", c["case_id"], type(exc).__name__)
        return {"verdict": "ERROR", "overall": None, "code": type(exc).__name__, "missing": None}
    overall = out["routing"]["overall_state"]
    missing = sorted(r["request_id"] for r in out["restricted"]["requirements"]
                     if r["requirement_state"] == "MANDATORY_EVIDENCE_MISSING")
    return {"verdict": OVERALL_TO_VERDICT[overall], "overall": overall, "code": None, "missing": missing}


def classify(expected, got):
    ev, gv = expected["verdict"], got["verdict"]
    if gv == "SUFFICIENT" and ev != "SUFFICIENT":
        return "DANGEROUS"
    if gv == ev:
        agree = True
    elif gv == "REJECTED" and ev == "INSUFFICIENT":
        agree = True  # fail-closed rejection of the supplied item is a non-sufficient verdict
    else:
        agree = False
    if agree:
        return "AGREE"
    if ev == "SUFFICIENT":
        return "OVER_CONSERVATIVE"
    return "WRONG_CLASS"


def evaluate(key):
    rows = []
    for c in key["cases"]:
        got = run_case(key, c)
        cls = classify(c["expected"], got)
        missing_ok = None
        if c["expected"]["verdict"] == "INSUFFICIENT" and got["verdict"] == "INSUFFICIENT":
            missing_ok = got["missing"] == sorted(c["expected"]["missing_request_ids"])
        rows.append({"case_id": c["case_id"], "title": c["title"], "reason": c["reason"], "basis": c["basis"],
                     "expected": c["expected"]["verdict"], "expected_missing": c["expected"]["missing_request_ids"],
                     "program": got["verdict"], "program_overall": got["overall"], "program_code": got["code"],
                     "program_missing": got["missing"], "missing_list_match": missing_ok,
                     "input_gap": c["decisive_input_outside_program_schema"], "class": cls})
    return rows


def summarize(rows):
    n = len(rows)
    counts = Counter(r["class"] for r in rows)
    by_basis = {}
    for b in sorted({r["basis"] for r in rows}):
        sub = [r for r in rows if r["basis"] == b]
        by_basis[b] = {"n": len(sub), "agree": sum(r["class"] == "AGREE" for r in sub)}
    danger = [r for r in rows if r["class"] == "DANGEROUS"]
    return {
        "cases": n, "agree": counts["AGREE"], "agreement_rate": round(counts["AGREE"] / n, 4) if n else None,
        "dangerous": counts["DANGEROUS"], "dangerous_excluding_input_gap": sum(not r["input_gap"] for r in danger),
        "over_conservative": counts["OVER_CONSERVATIVE"], "wrong_class": counts["WRONG_CLASS"],
        "by_basis": by_basis,
        "missing_list_checked": sum(r["missing_list_match"] is not None for r in rows),
        "missing_list_match": sum(r["missing_list_match"] is True for r in rows),
        "rejected_without_missing_list": sum(r["program"] == "REJECTED" and r["expected"] == "INSUFFICIENT" for r in rows),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", default=str(ROOT / "data/eval/checklist_answer_key_v1.json"))
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on-danger", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        key = load_key(args.key)
    except Exception as exc:
        print("ERROR answer key invalid: %s" % type(exc).__name__, file=sys.stderr)
        return 2
    rows = evaluate(key)
    summary = summarize(rows)
    result = {"key_version": key["version"], "key_status": key["status"], "summary": summary, "rows": rows}
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=1, sort_keys=True))
    else:
        for r in rows:
            print("%-6s %-9s exp=%-14s got=%-14s %s %s" % (r["case_id"], r["class"], r["expected"], r["program"],
                  r["program_code"] or r["program_overall"] or "", "[input-gap]" if r["input_gap"] else ""))
        print(json.dumps(summary, sort_keys=True))
    return 3 if (args.fail_on_danger and summary["dangerous"]) else 0


if __name__ == "__main__":
    sys.exit(main())
