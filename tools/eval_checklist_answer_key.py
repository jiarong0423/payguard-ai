#!/usr/bin/env python3
"""Run the checklist answer key against payguard.dispute_evidence.resolve_dispute_requirements.

In-process only: no network, no server, no PayPal or model call, no file writes unless --out is given.
Deterministic: fixed evaluation instant taken from the answer key, cases processed in key order.

Usage: .venv/bin/python3 -B tools/eval_checklist_answer_key.py [--set v1|v2|all] [--key PATH] [--out PATH] [--json] [--md] [--fail-on-danger]
Without --set and --key the behaviour and output are those of the original v1 runner. --set v2 / all adds
subset statistics (Wilson 95% intervals); --md prints the per-case Markdown tables used in the evidence report.
Exit codes: 0 ok, 2 answer key invalid or program import failed, 3 danger errors present with --fail-on-danger.
"""
import argparse
import json
import logging
import math
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
MAGIC = {"pdf": b"%PDF-1.4\n", "png": b"\x89PNG\r\n\x1a\n", "jpeg": b"\xff\xd8\xff\xe0",
         "gif": b"GIF89a", "bmp": b"BM"}
KEY_FILES = {"v1": "data/eval/checklist_answer_key_v1.json", "v2": "data/eval/checklist_answer_key_v2_heldout.json"}
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


def wilson(k, n, z=1.959964):
    """Wilson score interval for a binomial proportion; returns (low, high) rounded to 4 places."""
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def subset_stats(rows):
    n = len(rows)
    k = sum(r["class"] == "AGREE" for r in rows)
    return {"n": n, "agree": k, "rate": round(k / n, 4) if n else None, "wilson95": wilson(k, n),
            "dangerous": sum(r["class"] == "DANGEROUS" for r in rows),
            "dangerous_case_ids": [r["case_id"] for r in rows if r["class"] == "DANGEROUS"],
            "baseline_always_insufficient_agree": sum(r["expected"] == "INSUFFICIENT" for r in rows),
            "dangerous_excluding_input_gap": sum(r["class"] == "DANGEROUS" and not r["input_gap"] for r in rows)}


def subsets(rows):
    """Subsets are reported per key set; v1 and v2 are never pooled into one ratio."""
    out = {}
    for name in ("v1", "v2"):
        sub = [r for r in rows if r["set"] == name]
        if not sub:
            continue
        out[name] = subset_stats(sub)
        for basis, label in (("OFFICIAL_RULE", "official_rule"), ("AUTHOR_CONSISTENCY_CHECK", "author_logic")):
            part = [r for r in sub if r["basis"] == basis]
            if part:
                out[name + "_" + label] = subset_stats(part)
    return out


def fault(r):
    """Mechanical attribution label for a non-agreeing row; the written judgement lives in the report."""
    if r["class"] == "AGREE":
        return ""
    return "scope" if r["input_gap"] else "program-or-key"


def markdown(rows, subs):
    lines = ["| Subset | n | Agree | Rate | Wilson 95% CI | Always-INSUFFICIENT baseline | Dangerous (case ids) |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, s in subs.items():
        lines.append("| %s | %d | %d / %d | %.1f%% | %.1f%% - %.1f%% | %d / %d (%.1f%%) | %d %s |" % (
            k, s["n"], s["agree"], s["n"], 100 * s["rate"], 100 * s["wilson95"][0], 100 * s["wilson95"][1],
            s["baseline_always_insufficient_agree"], s["n"], 100 * s["baseline_always_insufficient_agree"] / s["n"],
            s["dangerous"], ", ".join(s["dangerous_case_ids"])))
    for name in ("v1", "v2"):
        sub = [r for r in rows if r["set"] == name]
        if not sub:
            continue
        lines += ["", "Per-case, %s:" % name, "", "| Case | Reason | Basis | Key | Program | Class |", "| --- | --- | --- | --- | --- | --- |"]
        for r in sub:
            prog = r["program"] + (" (%s)" % (r["program_code"] or r["program_overall"]) if (r["program_code"] or r["program_overall"]) else "")
            lines.append("| %s %s | %s | %s | %s | %s | %s%s |" % (r["case_id"], r["title"], r["reason"], r["basis"], r["expected"],
                         prog, r["class"], " [input-gap]" if r["input_gap"] else ""))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["v1", "v2", "all"])
    ap.add_argument("--key", default=None)
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--fail-on-danger", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.key and args.set:
        print("ERROR --key and --set are mutually exclusive", file=sys.stderr)
        return 2
    legacy = args.set is None
    if args.key:
        paths = [("custom", args.key)]
    elif legacy:
        paths = [("v1", str(ROOT / KEY_FILES["v1"]))]
    elif args.set == "all":
        paths = [(n, str(ROOT / KEY_FILES[n])) for n in ("v1", "v2")]
    else:
        paths = [(args.set, str(ROOT / KEY_FILES[args.set]))]
    rows, versions, statuses = [], [], []
    for name, path in paths:
        try:
            key = load_key(path)
        except Exception as exc:
            print("ERROR answer key invalid: %s" % type(exc).__name__, file=sys.stderr)
            return 2
        part = evaluate(key)
        for r in part:
            r["set"] = name
        rows += part
        versions.append(key["version"])
        statuses.append(key["status"])
    ids = [r["case_id"] for r in rows]
    if len(ids) != len(set(ids)):
        print("ERROR duplicate case_id across sets", file=sys.stderr)
        return 2
    summary = summarize(rows)
    if legacy or args.key:
        for r in rows:
            del r["set"]
        result = {"key_version": versions[0], "key_status": statuses[0], "summary": summary, "rows": rows}
        subs = None
    else:
        subs = subsets(rows)
        result = {"key_versions": versions, "key_status": statuses[0], "summary": summary, "subsets": subs, "rows": rows}
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=1, sort_keys=True))
    elif args.md:
        print(markdown(rows, subs if subs else subsets([dict(r, set="v1") for r in rows])))
    else:
        for r in rows:
            print("%-6s %-9s exp=%-14s got=%-14s %s %s" % (r["case_id"], r["class"], r["expected"], r["program"],
                  r["program_code"] or r["program_overall"] or "", "[input-gap]" if r["input_gap"] else ""))
        print(json.dumps(summary, sort_keys=True))
        if subs:
            print(json.dumps(subs, sort_keys=True))
    return 3 if (args.fail_on_danger and summary["dangerous"]) else 0


if __name__ == "__main__":
    sys.exit(main())
