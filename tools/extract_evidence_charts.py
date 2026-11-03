"""Extract the evidence-page chart data from the evidence records (no hand-typed numbers).

Two outputs, each recording the sha256 of the Markdown file it was read from:
  frontend/src/data/blind_trend_v1.json
      docs/evidence/KEYWORD_CHOOSER_BASELINE.md: the keyword chooser on each blind set, measured once
      after the rules were frozen (the "Trend across the three blind sets" table, plus the blind v4
      sentence of the hybrid section), cross-checked against each blind set's own table.
  frontend/src/data/stress_test_v1.json
      docs/evidence/GUIDE_STRESS_TEST.md: the volume table (rounds, corpora, conditions, scored model
      replies) and the drift table. The total row is parsed too and must equal the sum of the rows.

Every number is parsed from the Markdown; if a table or sentence is missing or changes shape the
extraction fails rather than guessing.

  python3 tools/extract_evidence_charts.py            write both files
  python3 tools/extract_evidence_charts.py --check    compare the committed files with a fresh extraction (exit 1 on drift)
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE_MD = "docs/evidence/KEYWORD_CHOOSER_BASELINE.md"
STRESS_MD = "docs/evidence/GUIDE_STRESS_TEST.md"
BLIND_TREND_OUT = "frontend/src/data/blind_trend_v1.json"
STRESS_TEST_OUT = "frontend/src/data/stress_test_v1.json"
EXTRACTOR = "tools/extract_evidence_charts.py"


class ExtractionError(ValueError):
    """The source Markdown no longer has the expected structure."""


def _source(relative: str, root: pathlib.Path) -> tuple[str, dict]:
    payload = (root / relative).read_bytes()
    return payload.decode("utf-8"), {"path": relative, "sha256": hashlib.sha256(payload).hexdigest()}


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_after(lines: list[str], heading_pattern: str, header: list[str]) -> list[tuple[int, list[str]]]:
    """Rows (1-based line number, cells) of the first table whose header matches, after the heading."""
    start = next((index for index, line in enumerate(lines) if re.search(heading_pattern, line)), None)
    if start is None:
        raise ExtractionError(f"heading not found: {heading_pattern}")
    for index in range(start, len(lines)):
        if lines[index].startswith("|") and _cells(lines[index]) == header:
            if index + 1 >= len(lines) or not re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lines[index + 1].strip()):
                raise ExtractionError(f"table separator missing after: {heading_pattern}")
            rows = []
            for row_index in range(index + 2, len(lines)):
                if not lines[row_index].startswith("|"):
                    break
                cells = _cells(lines[row_index])
                if len(cells) != len(header):
                    raise ExtractionError(f"row width changed at line {row_index + 1}")
                rows.append((row_index + 1, cells))
            if not rows:
                raise ExtractionError(f"empty table after: {heading_pattern}")
            return rows
        if index > start and lines[index].startswith("## "):
            break
    raise ExtractionError(f"table {header} not found after: {heading_pattern}")


def _ratio(text: str) -> float:
    if not re.fullmatch(r"[01]\.\d{2}", text):
        raise ExtractionError(f"not a two-decimal ratio: {text!r}")
    return float(text)


def _count(text: str) -> int:
    cleaned = text.replace("*", "").strip()
    if not re.fullmatch(r"\d+", cleaned):
        raise ExtractionError(f"not a count: {text!r}")
    return int(cleaned)


def extract_blind_trend(root: pathlib.Path = ROOT) -> dict:
    text, source = _source(BASELINE_MD, root)
    lines = text.splitlines()
    steps = []
    for line_number, (rules, blind_set, precision, recall, wrong) in _table_after(
            lines, r"^## Trend across the three blind sets", ["rules", "blind set", "precision", "recall", "confident wrong"]):
        if not re.fullmatch(r"v\d+", blind_set):
            raise ExtractionError(f"blind set label changed at line {line_number}")
        steps.append({"rules": rules, "blind_set": blind_set, "precision": _ratio(precision), "recall": _ratio(recall),
                      "confident_wrong": _count(wrong), "source_line": line_number,
                      "source_section": "Trend across the three blind sets"})

    # Cross-check: each trend row equals the row of its own blind-set table.
    per_set = {}
    for version in sorted({step["blind_set"] for step in steps}):
        for line_number, (label, precision, recall, wrong, attack) in _table_after(
                lines, rf"^## Blind set {version}\b", ["", "precision", "recall", "confident wrong", "attack touched"]):
            per_set.setdefault(version, []).append((_ratio(precision), _ratio(recall), _count(wrong), _count(attack)))
    for step in steps:
        rows = per_set.get(step["blind_set"], [])
        match = [row for row in rows if row[:3] == (step["precision"], step["recall"], step["confident_wrong"])]
        if len(match) != 1:
            raise ExtractionError(f"trend row at line {step['source_line']} does not match the blind {step['blind_set']} table")
        step["attack_touched"] = match[0][3]

    # Blind v4 is reported in one sentence of the hybrid section, measured with the rules named there.
    v4_rules = None
    for index, line in enumerate(lines):
        named = re.search(r"Blind set v4 \(.*measured once with ([0-9a-f]{7})\)", line)
        if named:
            v4_rules = named.group(1)
        found = re.fullmatch(r"Keyword chooser alone on blind v4: precision (\d\.\d{2}), recall (\d\.\d{2}), "
                             r"confident wrong (\d+) \(all stopped before the form\)\..*", line.strip())
        if found:
            if v4_rules is None:
                raise ExtractionError("blind v4 rules commit not stated before the v4 sentence")
            steps.append({"rules": v4_rules, "blind_set": "v4", "precision": _ratio(found.group(1)),
                          "recall": _ratio(found.group(2)), "confident_wrong": _count(found.group(3)),
                          "attack_touched": None, "source_line": index + 1,
                          "source_section": "Hybrid confirmation (sentence on blind set v4)"})
            break
    else:
        raise ExtractionError("blind v4 sentence not found")

    red_line = re.search(r"does not reach the red line of (\d+) on unseen wording", text)
    if red_line is None:
        raise ExtractionError("red-line sentence not found")
    return {
        "schema_version": "payguard.blind_trend.v1",
        "source": source,
        "extracted_by": EXTRACTOR,
        "description": ("Keyword chooser alone on blind sets written by separate writers, each measured once after "
                        "the rules were frozen. Rows in the order of the source."),
        "red_line_confident_wrong": int(red_line.group(1)),
        "steps": steps,
    }


def _volume_row(line_number: int, cells: list[str]) -> dict:
    round_name, corpus_cell, conditions_cell, replies = cells
    corpus = re.fullmatch(r"(\w+) \((\d+)(?:(?::| ,|,) (.+))?\)", corpus_cell)
    conditions = re.fullmatch(r"(\d+) \((.+)\)", conditions_cell)
    if corpus is None or conditions is None:
        raise ExtractionError(f"volume row changed shape at line {line_number}")
    row = {"round": round_name, "corpus": corpus.group(1), "items": int(corpus.group(2)),
           "corpus_note": corpus.group(3), "conditions": int(conditions.group(1)),
           "conditions_note": conditions.group(2), "scored_replies": _count(replies), "source_line": line_number}
    reach = re.fullmatch(r"(\d+) reach a model", row["corpus_note"] or "")
    row["items_reaching_model"] = int(reach.group(1)) if reach else None
    return row


def extract_stress_test(root: pathlib.Path = ROOT) -> dict:
    text, source = _source(STRESS_MD, root)
    lines = text.splitlines()
    table = _table_after(lines, r"^## Volume$", ["Round", "Corpus (items)", "Conditions", "Scored model replies"])
    *body, (total_line, total_cells) = table
    if not total_cells[0].strip("*").strip() == "Total":
        raise ExtractionError("the volume table no longer ends with its Total row")
    rounds = [_volume_row(line_number, cells) for line_number, cells in body]
    corpora = re.fullmatch(r"\*\*(\d+) frozen corpora, (\d+) items\*\*", total_cells[1])
    runs = re.fullmatch(r"\*\*(\d+) runs\*\*", total_cells[2])
    if corpora is None or runs is None:
        raise ExtractionError(f"total row changed shape at line {total_line}")
    total = {"corpora": int(corpora.group(1)), "items": int(corpora.group(2)), "runs": int(runs.group(1)),
             "scored_replies": _count(total_cells[3]), "source_line": total_line}
    sums = {"corpora": len(rounds), "items": sum(row["items"] for row in rounds),
            "runs": sum(row["conditions"] for row in rounds), "scored_replies": sum(row["scored_replies"] for row in rounds)}
    for key, value in sums.items():
        if total[key] != value:
            raise ExtractionError(f"total {key} {total[key]} != sum of rows {value}")

    drift = []
    for line_number, (kind, result) in _table_after(lines, r"^## Drift across the \d+ replies$", ["Drift type", "Result"]):
        fraction = re.fullmatch(r"(\d+) / (\d+)", result)
        every_run = re.fullmatch(r"(\d+) in every run", result)
        drift.append({
            "drift_type": kind, "result": result, "source_line": line_number,
            "count": int(fraction.group(1)) if fraction else int(every_run.group(1)) if every_run else None,
            "of_replies": int(fraction.group(2)) if fraction else None,
            "scope": "all replies" if fraction else "every run" if every_run else "see result text",
        })
    outside = [row for row in drift if row["drift_type"] == "Reply outside the closed JSON format"]
    if len(outside) != 1 or outside[0]["of_replies"] != total["scored_replies"]:
        raise ExtractionError("format row missing or not stated over all scored replies")
    # The format count is stated over all replies; a total of 0 makes every round 0, so the per-round
    # split is derived, not read. A non-zero total cannot be split without a per-round source.
    if outside[0]["count"] != 0:
        raise ExtractionError("non-zero outside-format total has no per-round source; extend the extractor")
    for row in rounds:
        row["outside_format"] = 0
        row["within_format"] = row["scored_replies"]

    api = re.search(r"(\d+) of the (\d+) replies came from scripted Gemini API calls", text)
    if api is None or int(api.group(2)) != total["scored_replies"]:
        raise ExtractionError("API share sentence not found or not over all replies")
    return {
        "schema_version": "payguard.stress_test.v1",
        "source": source,
        "extracted_by": EXTRACTOR,
        "description": ("Model replies scored against frozen corpora per round, and drift across all of them. "
                        "outside_format per round is derived from the all-reply total of 0."),
        "rounds": rounds,
        "total": total,
        "drift": drift,
        "gemini_api_replies": int(api.group(1)),
    }


def render(document: dict) -> str:
    return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def outputs(root: pathlib.Path = ROOT) -> dict[str, str]:
    return {BLIND_TREND_OUT: render(extract_blind_trend(root)), STRESS_TEST_OUT: render(extract_stress_test(root))}


def main(argv: list[str]) -> int:
    try:
        fresh = outputs()
    except (ExtractionError, OSError, UnicodeError) as error:
        print(f"FAILED: {error}")
        return 2
    if "--check" in argv:
        drift = [path for path, text in fresh.items()
                 if not (ROOT / path).is_file() or (ROOT / path).read_text(encoding="utf-8") != text]
        if drift:
            print("DRIFT: " + ", ".join(drift) + " (run python3 tools/extract_evidence_charts.py)")
            return 1
        print("evidence chart data: no drift")
        return 0
    for path, text in fresh.items():
        (ROOT / path).write_text(text, encoding="utf-8")
    print("wrote " + " and ".join(fresh))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
