#!/usr/bin/env python3
"""Compare the blind second rater's labels with the author's answer keys (v1 and v2).

Reads data/eval/second_rater_labels_v1_v2.json and the two answer keys; prints verdict agreement,
full agreement (verdict and missing request ids), Cohen's kappa over the four verdicts, and every
disagreement. No network, no model, no file writes. Exit 0 on success, 2 when an input file is invalid.

Usage: python3 -B tools/compare_second_rater.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = ("SUFFICIENT", "INSUFFICIENT", "MANUAL_REVIEW", "NOT_ACTIONABLE")


def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("ERROR cannot read %s: %s" % (path, type(exc).__name__), file=sys.stderr)
        sys.exit(2)


def kappa(pairs):
    n = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / n
    left, right = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    expected = sum(left[v] * right[v] for v in VERDICTS) / (n * n)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def main():
    labels = load("data/eval/second_rater_labels_v1_v2.json")
    keys = {"v1": load("data/eval/checklist_answer_key_v1.json")["cases"],
            "v2": load("data/eval/checklist_answer_key_v2_heldout.json")["cases"]}
    pairs, verdict_same, full_same, rows = [], 0, 0, []
    for subset in ("v1", "v2"):
        rater = {item["case_id"]: item for item in labels[subset]}
        if set(rater) != {case["case_id"] for case in keys[subset]}:
            print("ERROR case ids differ in %s" % subset, file=sys.stderr)
            sys.exit(2)
        for case in keys[subset]:
            mine, theirs = rater[case["case_id"]]["expected"], case["expected"]
            pairs.append((theirs["verdict"], mine["verdict"]))
            same_verdict = theirs["verdict"] == mine["verdict"]
            same_missing = sorted(theirs.get("missing_request_ids") or []) == sorted(mine.get("missing_request_ids") or [])
            verdict_same += same_verdict
            full_same += same_verdict and same_missing
            if not (same_verdict and same_missing):
                rows.append((case["case_id"], theirs["verdict"], theirs.get("missing_request_ids"),
                             mine["verdict"], mine.get("missing_request_ids"), rater[case["case_id"]].get("reason", "")))
    total = len(pairs)
    print("cases %d; verdict agreement %d/%d; full agreement %d/%d; kappa (4 verdicts) %.3f"
          % (total, verdict_same, total, full_same, total, kappa(pairs)))
    for row in rows:
        print("DIFF %s author=%s%s rater2=%s%s | %s" % (row[0], row[1], row[2], row[3], row[4], row[5]))


if __name__ == "__main__":
    main()
