# Render Workflows run, 2026-11-09

One manual run of the `evidence_integrity` task on a Render Workflow service created from this public repository (commit `e0da94b`). No schedule exists, so nothing here supports a "nightly" claim.

## What was set up
- Service: Render Workflow `tradeglot-evidence-integrity`, Python 3, flex compute plan, region Oregon, branch `main`, Auto-Deploy off.
- Build: `pip install --require-hashes -r requirements.lock && pip install -r workflows/evidence_integrity/requirements.txt`. Start: `python workflows/evidence_integrity/main.py`. One environment variable, `PYTHON_VERSION=3.13.5`; no secrets.
- Four tasks were registered (`evidence_integrity`, `dashboard_data`, `channel3_recordings`, `guide_benchmark`). In the public repository only the first three run, because the benchmark tools are not shipped (see `docs/RENDER_WORKFLOWS_NOTES.md`).

## The run
| Field | Value |
| --- | --- |
| run | `trn-0b94gdboi3thavh9s738mmujg`, task `evidence_integrity`, started 2026-11-09 09:29 (UTC+8) |
| result | Succeeded, 4.2 s (queued 0.5 s, ran 3.7 s) |
| subtasks | `dashboard_data` 1.7 s, `channel3_recordings` 0.8 s, both succeeded |
| receipt commit | `e0da94baa90c4c68012978d0a5bcee9f506ee1bb` |
| receipt digest | `content_sha256` `6a694b4e81688160944de6bc5f3c9546ce00cdb47b8d611ccd605621c9f6549c` |
| receipt body | `ok: true`, `drift: false`, `secrets_used: false`, `network_used: false`; `dashboard_data`: "dashboard data: no drift"; `channel3_recordings`: "5 recordings, 5 receipts" |

The receipt digest covers the receipt content; it is not a signature, because the workflow holds no key.

## What this does and does not show
- It shows the workflow code in this repository starts on Render, runs its checks, and returns a receipt whose commit matches the deployed commit.
- It does not show a recurring job: the run was started on demand once. Starting it nightly would need a separate caller (a cron job with an API key), which was not built.
- Compute is billed per second on the flex plan (Render's workflow pricing page); this run used a few seconds and was covered by the workspace's hackathon credit.

## Update, later on 2026-11-09: two more manual runs
The same task was started on demand two more times from the dashboard on the same deployed version (`e0da94b`): run `trn-0b94gdbokgp1avh9s738mmuq0` (succeeded, 4.2 s) and run `trn-0b94gdbokh7jat3og00ck053g` (succeeded, 4 s). The dashboard lists the three runs as Succeeded. The receipt body is recorded above for the first run only. There is still no schedule, so nothing here supports a nightly claim; the three runs show the task starts and finishes repeatably, not that it runs on its own.

## How the runs were started (checked 2026-11-11)
- All three runs were started on demand with the dashboard's **Run Task** button on the owner's signed-in dashboard; at least two were pressed through a browser tool the owner ran. Nothing calls the workflow on a schedule.
- GitHub supplies the code, not the runs: the Workflow service is connected to `jiarong0423/payguard-ai` (branch `main`), and its Events page shows the first deploy of `e0da94b` started 2026-11-09 09:27 and ready at 09:28 (UTC+8).
- The dashboard on 2026-11-11 lists 3 total runs, Succeeded (3), Failed (0), Canceled (0), all on version `e0da94b`: [render_workflow_runs_20261111.png](render_workflow_runs_20261111.png) (the account e-mail line is cropped out).
- Separate from the workflow: a keep-awake job on the owner's computer requests the hosted `start.html` every 10 minutes so judges do not wait for a cold start. It does not start the workflow.

