# Render Workflows: notes for the TradeGlot evidence-integrity workflow

Written 2026-11-01 for round 5 (issue #6), updated 2026-11-02. It says what was read, what the workflow does, how
the owner would deploy it, and what is still unverified.

**Status (2026-11-09): a two-check variant ships in the public repository and ran once on Render by hand** (run `trn-0b94gdboi3thavh9s738mmujg`, succeeded in 4.2 s, receipt `ok:true`; see `docs/evidence/RENDER_WORKFLOW_RUN_20261109.md`). It is not scheduled. The public source package leaves out the benchmark tools, so a run from the public repository has two checks (`dashboard_data`, `channel3_recordings`); a run from the full project tree has three. The receipt lists exactly the checks that exist.

## Sources

### Read
| Source | What it gave |
|---|---|
| https://github.com/render-oss/sdk (README) | SDK status, as read on 2026-11-01: "Early Access ... subject to breaking changes" (recheck before relying on it); Python package `render`; `RENDER_API_KEY` for the client; Python 3.10 minimum |
| https://github.com/render-oss/sdk/blob/main/python/README.md | `from render import TaskContext, Workflows`; `app = Workflows(...)`; `@app.task`; subtasks with `await ctx.run(task, ...)`; `Retry(...)`; local development with `render workflows dev -- python main.py` and `render workflows tasks start <task name> --local`; client calls `Render().workflows.run_task(...)` / `start_task(...)` |
| https://raw.githubusercontent.com/render-oss/sdk/main/python/example/task/main.py | the entry-point layout used here: one `Workflows` app, `@app.task` functions taking `ctx: TaskContext` first, `app.start()` at the end; comment "Start via CLI: render-workflows example.task.main:app" |
| https://raw.githubusercontent.com/render-oss/sdk/main/python/pyproject.toml | `name = "render"`, `version = "1.6.0"` (main branch), `requires-python = ">=3.10,<4.0"`, console script `render-workflows` |
| https://raw.githubusercontent.com/render-oss/sdk/main/python/render/workflows/app.py | `task(..., name=None, retry=None, timeout_seconds=None, plan=None)` (the README's `timeout=` does not match the code; this repo uses `timeout_seconds`); `default_timeout` is in seconds; `start()` needs `RENDER_SDK_MODE` and `RENDER_SDK_SOCKET_PATH`, which the Render runtime or the CLI provides |
| https://raw.githubusercontent.com/render-oss/sdk/main/python/render/workflows/task.py | `timeout_seconds` range 30-86400; plans `starter`, `standard` (default), `pro` |
| https://render.com/docs/workflows-limits (read 2026-11-02) | the SDK docstring above is stale: starter and standard are discontinued for Workflows and run on `flex` (default, billed per second, at most $0.40/h); `main.py` now names `flex` |
| executor.py, client.py, runner.py in the same folder | a task that raises is reported as failed with `str(error)`; a failed subtask raises `TaskRunError("Subtask failed: ...")` in the caller; results are sent through `json.dumps` (so results must be JSON values); inputs arrive as JSON |

### UNREAD
On 2026-11-01 these pages could not be loaded from the build environment (the render.com DNS lookup failed then),
so nothing below is taken from them. Every point that depends on them is marked UNVERIFIED in this file. One render.com
page, `workflows-limits`, was read later (2026-11-02) and is listed under Read above; the rest stay unread.
- https://render.com/docs/workflows: UNREAD
- https://render.com/docs/workflows-tutorial: UNREAD
- https://render.com/docs/workflows-defining: UNREAD
- https://render.com/docs/workflows-local-development: UNREAD
- https://render.com/docs/workflows-running: UNREAD
- https://render.com/docs/blueprint-spec: UNREAD (so Blueprint support for workflows is unknown)
- https://render.com/workflows: UNREAD
- https://pypi.org/project/render/ and https://pypi.org/project/render-sdk/: UNREAD (a bot check page, not the listing)
- https://api-docs.render.com/reference/listworkflows: UNREAD

## What the workflow does

`workflows/evidence_integrity/` re-checks, on a schedule, that the evidence files TradeGlot shows to judges and
sellers still match the code that produces them. It needs no secret and makes no network call.

| Task | Runs | Fails when |
|---|---|---|
| `guide_benchmark` | `tools/run_guide_benchmark.py --check` (the real guide service, no model) | any wrong value appears, or the fresh numbers differ from `docs/evidence/guide_benchmark_current.json` (its `commit` stamp is ignored). The tool rewrites that file, so the task puts the committed bytes back. |
| `dashboard_data` | `tools/build_dashboard_data.py --check` | the committed dashboard data differs from a fresh build |
| `channel3_recordings` | `backend/app/channel3_products.load_recorded` on `backend/app/data/channel3_recorded_v1.json`, cross-checked with `docs/evidence/channel3_receipts_v1.json` | an entry does not load back, a receipt is missing or malformed, or a receipt disagrees with its recording (query, time, number of cards) |
| `evidence_integrity` | runs the three tasks above as subtasks (`ctx.run`), then writes the receipt | any subtask failed or drifted |

On drift or failure a task prints one line starting `ERROR DRIFT <task>:` or `ERROR FAILED <task>:` and raises. A
Render task run is then reported as failed; the command line exits 1.

**Receipt** (`payguard.evidence_integrity_receipt.v1`): commit, creation time, each task's result (ok, drift, exit
code, seconds, last output line), overall `drift` and `ok`, `secrets_used: false`, `network_used: false`, and
`content_sha256` over the canonical JSON. That digest shows the receipt was not edited after it was written. It is
not a cryptographic signature, because the workflow holds no key. The receipt is written to
`output/evidence_integrity/receipt_<commit>.json` (git-ignored) and printed as one `RECEIPT {...}` log line. A
failed Render task returns no value, so the log line is the copy that survives on Render. Whether Render keeps
files written by a task is UNVERIFIED; treat the log line and the returned value as the artifacts.

**Measured locally** (`docs/evidence/EVIDENCE_INTEGRITY_RECEIPT_20261101.json`, one run of
`python -m workflows.evidence_integrity.tasks` in the build environment at commit `47e775e`, not on Render):
`guide_benchmark` 111.333 s, `dashboard_data` 0.912 s, `channel3_recordings` 0.071 s (5 recordings, 5 receipts),
drift false. The timeouts in `main.py` (1800 s, 600 s, 300 s, 3600 s for the whole run) leave room above that.

Retries are off (`max_retries=0`): a drift is a finding, and re-running the same commit gives the same answer.

## Run it

Without Render (the same code the tasks run):

```bash
python -m workflows.evidence_integrity.tasks
```

With the Render CLI's local task server (SDK README; this repository has not run it, see below):

```bash
render workflows dev -- python workflows/evidence_integrity/main.py
```

```bash
render workflows tasks start evidence_integrity --local
```

Tests: `tests/test_evidence_integrity_workflow.py` runs every task as a plain function with no network.
`main.py` is checked against a stand-in `render` module built from the SDK signatures above. The real SDK was not
installed or run here: the build environment refused to install and run the external package. Run the
`render workflows dev` lines above once before the first deploy.

## Deploy (owner, dashboard). UNVERIFIED steps
`render.yaml` is unchanged: the Blueprint spec page is UNREAD, so it is not known whether a workflow can be
declared there. The steps below follow the SDK sources above. The service type, field names and scheduling are
UNVERIFIED until checked against the Render dashboard or the UNREAD pages.

1. In the Render dashboard, create a new **Workflow** (if offered), connected to this repository and branch.
2. Runtime Python 3.13 (the repository pins 3.13; the SDK supports 3.10 or later).
3. Build command:

   ```bash
   pip install --require-hashes -r requirements.lock && pip install -r workflows/evidence_integrity/requirements.txt
   ```

4. Start command: `python workflows/evidence_integrity/main.py`. The SDK also documents
   `render-workflows workflows.evidence_integrity.main:app`; use whichever the dashboard asks for.
5. No environment variables and no secrets. Do not add PayPal, Gemini, Google or Channel3 keys.
6. Run `evidence_integrity` once from the dashboard and check the `RECEIPT` log line says `"ok":true`.
7. Nightly: Workflows has no native scheduling (Render's documentation, re-read 2026-11-04); runs are started by a
   client call. A separate Render cron job therefore starts the task with the SDK client
   (`Render().workflows.start_task("<workflow slug>/evidence_integrity", [])`). That needs `RENDER_API_KEY` as a
   secret on the cron job only; the workflow itself stays secret-free. Workflow runs are billed per second of
   compute (see the limits row under "Sources"), and the cron job is billed separately. None of this is deployed.

## Public package
`workflows/evidence_integrity/` ships in the public repository. Task 1 (`guide_benchmark`) runs `tools/run_guide_benchmark.py` and `tools/simulate_guide_flow.py`, which the public package leaves out, so `tasks.py` and `main.py` register that task only when `tools/run_guide_benchmark.py` exists. From the public repository the workflow therefore has two checks. A local run of the public build on 2026-11-09 (`python -m workflows.evidence_integrity.tasks`) printed a receipt with `"ok":true` for `dashboard_data` ("no drift") and `channel3_recordings` ("5 recordings, 5 receipts"), `secrets_used:false`, `network_used:false`. `tests/test_evidence_integrity_workflow.py` stays out of the public package because it tests the three-check tree.
