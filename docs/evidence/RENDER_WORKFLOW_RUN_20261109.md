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
- It does not show a recurring job: the run was started by hand once. Starting it nightly would need a separate caller (a cron job with an API key), which was not built.
- Compute is billed per second on the flex plan (Render's workflow pricing page); this run used a few seconds and was covered by the workspace's hackathon credit.
