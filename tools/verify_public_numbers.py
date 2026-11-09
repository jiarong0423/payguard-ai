#!/usr/bin/env python3
"""Recompute, from the files in this repository, every number the public pages claim.

Standard library only. It writes no file, makes no network call and starts no server. To count the Python tests it imports
the test modules (unittest discovery), which runs their top-level code but none of the tests.
Run from the repository root (any Python 3.9+; step 4 needs the project's own Python 3.13 environment):

    .venv/bin/python3 -B tools/verify_public_numbers.py

For each number it prints the measured value, how it was counted, the value the docs claim, and PASS, DIFF or
MANUAL. MANUAL means the number only exists while a program runs (see docs/evidence/HOW_NUMBERS_WERE_COUNTED.md).
Exit code: 0 when no line is DIFF, 1 when at least one is, 2 when the repository cannot be read.

File set: every path in public_export_manifest.json plus the manifest and its .sha256 file. Anything else on disk
(.venv, node_modules, frontend/dist, build logs) is never counted.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = "public_export_manifest.json"
MANIFEST_SHA = "public_export_manifest.sha256"

# Values claimed on the public pages (README.md, docs/submission/devpost_story.md).
CLAIMS = {
    "tracked_files": 381,
    "python_source_lines": 21878,
    "python_test_lines": 18169,
    "frontend_lines": 13730,
    "jsx_files": 23,
    "frontend_pages": 5,
    "api_routes": 37,
    "node_test_files": 50,
    "node_test_lines": 6973,
    "python_tests": 1104,
    "python_tests_skipped": 9,
    "redteam_requests": 1727,
    "doc_words": 80672,
    "evidence_files": 25,
    "images": 22,
    "paypal_clauses": 140,
    "rules_total": 681,
    "rules_export": 313,
    "rules_import": 368,
    "countries": 10,
    "benchmark_cases": 268,
    "scored_replies": 601,
    "debug_ids": 3,
}

RESULTS = []  # (status, key, measured, claimed, method)


def record(key, measured, method, claimed=None, tolerance_words=False):
    claimed = CLAIMS.get(key) if claimed is None else claimed
    if measured is None:
        status = "MANUAL"
    elif claimed is None:
        status = "INFO"
    else:
        # The word count is quoted as "about"; the documents are still edited, so allow one percent either way.
        close = abs(measured - claimed) <= claimed * 0.01 if key == "doc_words" else measured == claimed
        status = "PASS" if close else "DIFF"
    RESULTS.append((status, key, measured, claimed, method))


def fail(message):
    print("ERROR " + message, file=sys.stderr)
    sys.exit(2)


def read_bytes(rel):
    return (ROOT / rel).read_bytes()


def line_count(rel):
    data = read_bytes(rel)
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def total_lines(paths):
    return sum(line_count(p) for p in paths)


def ext(path):
    return os.path.splitext(path)[1]


def load_file_set():
    try:
        manifest = json.loads(read_bytes(MANIFEST).decode("utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"cannot read {MANIFEST} (run from the repository root): {exc}")
    paths = [entry["path"] for entry in manifest["files"]]
    extra = [p for p in (MANIFEST, MANIFEST_SHA) if (ROOT / p).is_file()]
    missing = [p for p in paths if not (ROOT / p).is_file()]
    if missing:
        fail("files listed in the manifest are missing: " + ", ".join(missing[:5]))
    changed = [entry["path"] for entry in manifest["files"]
               if hashlib.sha256(read_bytes(entry["path"])).hexdigest() != entry["sha256"]]
    return manifest, sorted(set(paths + extra)), changed


def count_routes(paths):
    """Count FastAPI route decorators with the ast module: @<receiver>.<get|post|put|delete|patch>(...)."""
    verbs = {"get", "post", "put", "delete", "patch", "options", "head"}
    per_file, receivers, other_registration = {}, set(), []
    for rel in paths:
        if not rel.startswith("backend/") or ext(rel) != ".py":
            continue
        tree = ast.parse(read_bytes(rel).decode("utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for deco in node.decorator_list:
                    if (isinstance(deco, ast.Call) and isinstance(deco.func, ast.Attribute)
                            and deco.func.attr in verbs and isinstance(deco.func.value, ast.Name)):
                        per_file[rel] = per_file.get(rel, 0) + 1
                        receivers.add(deco.func.value.id)
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr in ("add_api_route", "include_router", "api_route")):
                other_registration.append(rel)
    return per_file, receivers, other_registration


def load_python_tests(paths):
    """Load (never run) the unittest suite the way `unittest discover -s tests` does and count it."""
    sys.dont_write_bytecode = True
    for sub in ("", "src", "backend"):
        sys.path.insert(0, str(ROOT / sub))
    previous = os.getcwd()
    os.chdir(ROOT)
    try:
        suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    finally:
        os.chdir(previous)

    def flatten(item):
        for child in item:
            if isinstance(child, unittest.TestSuite):
                yield from flatten(child)
            else:
                yield child

    tests = list(flatten(suite))
    failed = [t for t in tests if type(t).__name__ == "_FailedTest"]
    skipped = 0
    for test in tests:
        method = getattr(test, getattr(test, "_testMethodName", ""), None)
        if getattr(type(test), "__unittest_skip__", False) or getattr(method, "__unittest_skip__", False):
            skipped += 1
    return len(tests), skipped, len(failed)


def main():
    manifest, paths, changed = load_file_set()
    pathset = set(paths)
    print(f"File set: {len(manifest['files'])} manifest files + {len(paths) - len(manifest['files'])} manifest "
          f"records = {len(paths)}; files whose sha256 differs from the manifest: {len(changed)}")

    # 1. Tracked files
    record("tracked_files", len(paths), "paths in public_export_manifest.json + the manifest and its .sha256")

    # 2. Python lines (newline-terminated lines; blank lines and comments included)
    py = [p for p in paths if ext(p) == ".py"]
    test_py = [p for p in py if p.startswith("tests/")]
    src_py = [p for p in py if not p.startswith("tests/")]
    record("python_source_lines", total_lines(src_py),
           "*.py outside tests/ (backend, src, tools, integrations), physical lines")
    record("python_test_lines", total_lines(test_py), "tests/**/*.py, physical lines")

    # 3. Front end
    fe_src = [p for p in paths if p.startswith("frontend/src/") and ext(p) in (".jsx", ".js", ".css")]
    record("frontend_lines", total_lines(fe_src),
           "frontend/src/**/*.{jsx,js,css}, physical lines (no .json data, no .mjs, no HTML, no public/)")
    record("jsx_files", len([p for p in paths if p.startswith("frontend/") and ext(p) == ".jsx"]),
           "frontend/**/*.jsx")
    record("frontend_pages", len([p for p in paths if re.fullmatch(r"frontend/[^/]+\.html", p)]),
           "frontend/*.html (Vite entry pages; public/offline.html is not a page)")
    RESULTS.append(("INFO", "frontend_lines_variants", None, None,
                    "js+jsx only {}; +css {}; +json data {}; +html+public {}".format(
                        total_lines([p for p in fe_src if ext(p) != ".css"]),
                        total_lines(fe_src),
                        total_lines(fe_src + [p for p in paths if p.startswith("frontend/src/") and ext(p) == ".json"]),
                        total_lines([p for p in paths if p.startswith("frontend/") and ext(p) in (".jsx", ".js", ".css", ".html")]))))

    # 4. Routes
    per_file, receivers, other = count_routes(paths)
    record("api_routes", sum(per_file.values()),
           "ast: decorated functions @<name>.<get|post|...>(...) in backend/**/*.py; receivers={}; per file {}; "
           "add_api_route/include_router calls: {}".format(sorted(receivers), per_file, len(other)))

    # 5. Node tests
    node = [p for p in paths if re.fullmatch(r"tests/frontend_[^/]+\.mjs", p)]
    record("node_test_files", len(node), "tests/frontend_*.mjs")
    record("node_test_lines", total_lines(node), "tests/frontend_*.mjs, physical lines")

    # 6. Python tests (loaded, not run)
    try:
        loaded, skipped, failed = load_python_tests(paths)
        if failed:
            # A count taken while some test modules cannot be imported would be wrong, so do not report one.
            note = (f"{failed} test module(s) could not be imported with this Python (the project packages are missing); "
                    "run it with the project environment: .venv/bin/python3 -B tools/verify_public_numbers.py, "
                    "or run ./tools/run.sh test and read the final 'Ran N tests' line")
            record("python_tests", None, note)
            record("python_tests_skipped", None, "as above: final line 'OK (skipped=N)'")
        else:
            record("python_tests", loaded,
                   "unittest discover loader on tests/ (load only, nothing executed); every test module imported")
            record("python_tests_skipped", skipped,
                   "tests/methods carrying a @unittest.skip* marker at load time; a skipTest() call inside a test body "
                   "is only visible when it runs, so this is a lower bound")
    except Exception as exc:  # missing third-party packages: say so, do not guess
        record("python_tests", None, f"could not load tests ({type(exc).__name__}: {str(exc)[:80]}); use the "
               "project .venv python, or run ./tools/run.sh test and read the final 'Ran N tests' line")
        record("python_tests_skipped", None, "as above: final line 'OK (skipped=N)'")

    # 7. Red-team request matrix
    record("redteam_requests", None,
           "exists only at run time: tools/redteam_input_matrix.py builds requests from the app's OpenAPI schema. "
           "Run ./tools/run.sh test (prints 'round regression: N requests; BROKEN 0, GAP 0 ...') or "
           "PYTHONPATH=src:backend python3 tools/redteam_input_matrix.py --out <dir>")

    # 8. Words in markdown
    md = [p for p in paths if ext(p) == ".md"]
    words = sum(len(read_bytes(p).decode("utf-8").split()) for p in md)
    record("doc_words", words, f"all {len(md)} *.md in the file set (README, SECURITY, notices, docs/**), "
           "whitespace-separated tokens; code fences and tables included")
    RESULTS.append(("INFO", "doc_words_variants", None, None,
                    "docs/**/*.md only {}; docs + README.md {}".format(
                        sum(len(read_bytes(p).decode('utf-8').split()) for p in md if p.startswith("docs/")),
                        sum(len(read_bytes(p).decode('utf-8').split()) for p in md if p.startswith("docs/") or p == "README.md"))))

    # 9. Evidence files and images
    record("evidence_files", len([p for p in paths if re.fullmatch(r"docs/evidence/[^/]+", p)]),
           "files directly in docs/evidence/ in the file set (Markdown, JSON and receipts)")
    images = [p for p in paths if ext(p) in (".png", ".svg")]
    docs_images = [p for p in images if p.startswith("docs/")]
    record("images", len(images),
           f"*.png and *.svg anywhere in the file set ({len(docs_images)} under docs/, "
           f"{len(images) - len(docs_images)} app icons under frontend/); .mmd sources not counted")

    # 10. Country rules
    rules = json.loads(read_bytes("data/country_rules/paypal_country_rules_v1.json").decode("utf-8"))
    export = sum(len(v["rules"]) for v in rules["export_rules"].values())
    imported = sum(len(v["rules"]) for v in rules["import_rules"].values())
    record("paypal_clauses", len(rules["snippets"]), "len(snippets) in data/country_rules/paypal_country_rules_v1.json")
    record("rules_export", export, "sum of len(rules) over export_rules[country]")
    record("rules_import", imported, "sum of len(rules) over import_rules[country]")
    record("rules_total", export + imported, "export + import")
    record("countries", len(rules["countries"]), "keys of countries")

    # 11. Benchmark and stress test
    bench = json.loads(read_bytes("docs/evidence/guide_benchmark_v1.json").decode("utf-8"))
    cases = {}
    for flow, corpora in bench["flows"].items():
        cases[flow] = sum((v["cases"] if "cases" in v else v["honest"]["cases"]) for v in corpora.values())
    record("benchmark_cases", cases.get("hybrid"),
           f"sum of cases over the {len(bench['corpora'])} corpora of flow 'hybrid' in guide_benchmark_v1.json "
           f"(per flow: {cases})")
    stress = json.loads(read_bytes("frontend/src/data/stress_test_v1.json").decode("utf-8"))
    rounds_total = sum(r["scored_replies"] for r in stress["rounds"])
    record("scored_replies", rounds_total,
           f"sum of scored_replies over {len(stress['rounds'])} rounds in stress_test_v1.json "
           f"(its own 'total' field: {stress['total']['scored_replies']}). The raw replies are not published, "
           "so this is a recount of the recorded table, not of the replies")

    # 12. Debug-Ids in receipts
    ids, with_id = set(), 0
    receipts = [p for p in paths if re.fullmatch(r"docs/evidence/RECEIPT_[^/]+\.md", p)]
    for rel in receipts:
        found = set(re.findall(r"Debug-Id[^\n]{0,30}?\b([0-9a-f]{12,14})\b", read_bytes(rel).decode("utf-8")))
        with_id += 1 if found else 0
        ids |= found
    record("debug_ids", len(ids),
           f"distinct 'PayPal-Debug-Id <hex>' values in {len(receipts)} docs/evidence/RECEIPT_*.md "
           f"({with_id} of the {len(receipts)} files contain one; the 2026-10-31 receipt is reads and an unsent draft only)")

    # Report
    width = max(len(r[1]) for r in RESULTS)
    for status, key, measured, claimed, method in RESULTS:
        if status == "INFO":
            print(f"[INFO]   {key:<{width}}  {method}")
            continue
        shown = "n/a (run-time)" if measured is None else f"{measured:,}"
        claim = "-" if claimed is None else f"{claimed:,}"
        print(f"[{status:<6}] {key:<{width}}  measured={shown}  claimed={claim}\n         how: {method}")
    counts = {s: sum(1 for r in RESULTS if r[0] == s) for s in ("PASS", "DIFF", "MANUAL")}
    print("SUMMARY PASS={PASS} DIFF={DIFF} MANUAL={MANUAL}".format(**counts))
    if changed:
        print("NOTE files differ from manifest sha256: " + ", ".join(changed[:10]))
    return 1 if counts["DIFF"] else 0


if __name__ == "__main__":
    sys.exit(main())
