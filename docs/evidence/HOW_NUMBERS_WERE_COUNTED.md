# How the public numbers were counted

Every figure on the Devpost page and in the README that is a count can be recomputed from this repository with one command, run from the repository root:

```
.venv/bin/python3 -B tools/verify_public_numbers.py
```

The script uses only the Python standard library, reads files only, makes no network call and starts no server. It prints the measured value, the way it was counted and the claimed value for each number, then PASS, DIFF or MANUAL. Exit code 1 means at least one DIFF. The Python test count needs the project environment (`.venv`, Python 3.13), because loading the tests imports FastAPI; every other line works with any Python 3.9+.

## Counting scope

The file set is the public candidate: every path in `public_export_manifest.json` (366 files) plus the manifest and `public_export_manifest.sha256`, which makes the 368 tracked files. A fresh copy also contains `.venv`, `node_modules`, `frontend/dist` and build logs; none of these is counted. The script also checks every file against the sha256 in the manifest and reports any that differ. A "line" is a physical line (a newline-terminated line, the same as `wc -l`), so blank lines and comments are included. A "word" is a whitespace-separated token (`str.split()`).

## The numbers

| Claim | Value | Command or rule |
|---|---|---|
| Tracked files | 368 | 366 manifest paths + `public_export_manifest.json` + `public_export_manifest.sha256` |
| Python source lines | 21,710 | all `*.py` outside `tests/` (backend, src, tools, integrations) |
| Python test lines | 17,893 | all `tests/**/*.py` |
| Front-end lines | 13,691 | `frontend/src/**/*.{jsx,js,css}`, 73 files; see below |
| JSX files / pages | 23 / 5 | `frontend/**/*.jsx`; `frontend/*.html` (index, dashboard, evidence, proof, scenarios; `public/offline.html` is the service-worker fallback, not a page) |
| API routes | 37 | see "Route count" |
| Node test files / lines | 49 / 6,912 | `tests/frontend_*.mjs` (the two other `.mjs` files are a token-writer and a recorder, not tests) |
| Python tests | 1,089 (9 skipped) | `unittest` discovery over `tests/`, loaded and counted, not run |
| Red-team requests | 1,727 | run-time only, see below |
| Words in documents | 74,377 (page says about 74,377; the script allows 1% either way) | see below |
| Evidence files | 24 | files directly in `docs/evidence/` (22 `.md`, 2 `.json`) |
| Diagrams and images | 22 | every `*.png` and `*.svg` in the file set: 16 under `docs/`, 6 application icons under `frontend/public/icons`; `.mmd` sources are not counted |
| PayPal clauses | 140 | `len(snippets)` in `data/country_rules/paypal_country_rules_v1.json` |
| Export / import rules | 313 / 368 = 681 | sum of `len(rules)` over `export_rules[country]` and `import_rules[country]`, ten countries |
| Evidence-guide benchmark | 268 cases | sum of `cases` over the seven corpora in `docs/evidence/guide_benchmark_v1.json`; the same 268 in each of the three flows |
| Scored guide replies | 601 | sum of `scored_replies` over the five rounds in `frontend/src/data/stress_test_v1.json`; this recounts the recorded table, the raw replies themselves are not published |
| PayPal-Debug-Ids | 3 | distinct values in `docs/evidence/RECEIPT_*.md` (`f908765a01293`, `f2088142a6218`, readback `ca5554cf42ef6`) |

### Python tests

`unittest.defaultTestLoader.discover("tests")` yields 1,089 test cases with no import failure. Nothing is executed. Skips are counted from `@unittest.skip*` markers visible at load time (9). A skip raised by `self.skipTest()` inside a test body would only appear when the test runs; the full run (`./tools/run.sh test`, final lines `Ran N tests` and `OK (skipped=N)`) is the authority for the skip count; the full suite was run on 2026-11-08 on this tree and printed `Ran 1058 tests` and `OK (skipped=9)`. Earlier documents quoting 1005, 1039, 1048 and 1055 are older counts from earlier states of the tree.

### Red-team request matrix (1,727)

This number exists only while the program runs. `tools/redteam_input_matrix.py` reads the application's own schema (its OpenAPI document, built in memory by FastAPI), builds attack requests for every JSON route from that schema with a fixed seed (20261102), sends them in-process and prints one line: `round R1: 1827 requests; BROKEN 0, GAP 0, GUARDED 1810, OK 18`. There is no stored list of requests to count, so the script does not guess; it reports MANUAL. To reproduce, run `./tools/run.sh test` and read the line `round regression: 1827 requests; ...` (printed by `tests/test_redteam_input_matrix.py`), or run `PYTHONPATH=src:backend .venv/bin/python3 -B tools/redteam_input_matrix.py --out <empty dir>`. The count changes if a route or a field limit is added, because the requests follow the schema.

### Route count (37; one reviewer found 0)

The backend is FastAPI. Routes are registered inside the factory function `create_app()` in `backend/app/main.py` with decorators on a local variable named `application` (`@application.get(...)`, `@application.post(...)`), and two helper modules (`guide_routes.py`, `country_routes.py`) receive that object and decorate the same way: 29 + 5 + 3 = 37. Three things make a quick check return 0 or a different number:

1. `grep '@app\.'` or `'@router\.'` finds nothing, because the variable is `application`, not `app` or `router`. Matching the decorator on any receiver name finds 37.
2. The routes do not exist at import time. They are added when `create_app()` runs, so inspecting an un-called module (or `app.router.routes` before the factory is called) shows an empty router. Calling `create_app()` gives 37 `APIRoute` entries plus one `Mount` (the static console at `/`), 38 entries in all.
3. `openapi_url=None` and `docs_url=None`, so there is no `/openapi.json` to read the routes from over HTTP.

The script counts with the `ast` module (decorated functions whose decorator is `<name>.<get|post|put|delete|patch>(...)`), so it neither runs the app nor depends on the variable name. It also confirms there are no `add_api_route` or `include_router` calls. Each route has exactly one HTTP method, so routes and method-path pairs are both 37. This was cross-checked once by calling `create_app()` and counting `APIRoute` objects: 37.

### Front-end lines: 13,691

13,691 is the physical line count of the 73 files `frontend/src/**/*.jsx`, `*.js` and `*.css`. It excludes the JSON data files (adding them gives 15,407), `.mjs` files, the HTML pages and `frontend/public/` (adding HTML and public gives 13,733). JS and JSX without CSS is 10,729. The earlier public page said 13,463, the count of the published tree before 2026-11-08; the 15 more lines are the CSS added that day (`frontend/src/index.css` grew from 1,143 to 1,158 lines: the hint box before a draft and the toast placement rule). An independent reviewer's count of 13,553 uses the same scope.

### Document words: 74,377

74,377 is the whitespace-token count of all 42 Markdown files in the file set (README, the security and notices files, and everything under `docs/`), with code fences and tables included. Limited to `docs/**` it is 59,470; `docs/**` plus README is 71,596. Earlier pages quoted "about 48,700" (the tree before 2026-11-08, documents only); the count grew because evidence files and a README walkthrough were added that day. The page says "about 74,377"; the script accepts one percent either way because the documents are still being edited. `tools/verify_public_numbers.py` prints the current figure and the variants.

### Receipts with a Debug-Id

There are three receipt files in `docs/evidence/`. Three distinct PayPal-Debug-Ids appear in them, but only two files contain any: `RECEIPT_20261104_live.md` (one) and `RECEIPT_20261105_live.md` (two: the send and the fresh read). `RECEIPT_20261031_live.md` records Sandbox reads and an unsent invoice draft and has no Debug-Id. "Three Sandbox receipts" and "three Debug-Ids" are both true; "three receipts that each contain a Debug-Id" is not.

## Not in the repository

Git history is not public data. On 2026-11-09 the public repository had 46 commits (`git rev-list --count HEAD` in the public repository; the count grows with each push). The development history of 261 commits is the author's own statement and cannot be reproduced from the public repository.
