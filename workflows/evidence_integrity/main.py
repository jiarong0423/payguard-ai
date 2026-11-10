"""Render Workflows entry point for the TradeGlot evidence-integrity run (started on demand from the Render dashboard; no schedule, see docs/evidence/RENDER_WORKFLOW_RUN_20261109.md).

Pattern taken from the Render SDK (github.com/render-oss/sdk, python/example/task/main.py and
python/render/workflows/app.py; see docs/RENDER_WORKFLOWS_NOTES.md): one ``Workflows`` app, one
``@app.task`` per check, an orchestrator that runs each check as its own subtask with ``ctx.run``,
and ``app.start()`` to serve the tasks. Every task body is a plain function in tasks.py, so the unit
tests run the same code without the SDK, the network or any secret.

  Local (Render CLI):  render workflows dev -- python workflows/evidence_integrity/main.py
                       render workflows tasks start evidence_integrity --local
  Without Render:      python -m workflows.evidence_integrity.tasks
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from render import Retry, TaskContext, Workflows  # noqa: E402

from workflows.evidence_integrity import tasks  # noqa: E402

# No retries: a drift is a real finding, and re-running the same commit gives the same answer.
app = Workflows(default_retry=Retry(max_retries=0, wait_duration_ms=1000), default_timeout=600, default_plan="flex")


@app.task(timeout_seconds=1800)
def guide_benchmark(ctx: TaskContext) -> dict:
    """Task 1: tools/run_guide_benchmark.py --check against docs/evidence/guide_benchmark_current.json."""
    return tasks.check_guide_benchmark()


@app.task(timeout_seconds=600)
def dashboard_data(ctx: TaskContext) -> dict:
    """Task 2: tools/build_dashboard_data.py --check."""
    return tasks.check_dashboard_data()


@app.task(timeout_seconds=300)
def channel3_recordings(ctx: TaskContext) -> dict:
    """Task 3: recorded Channel3 replies load back through load_recorded and match their receipts."""
    return tasks.check_channel3_recordings()


SUBTASKS = {name: task for name, task in (("guide_benchmark", guide_benchmark), ("dashboard_data", dashboard_data),
                                          ("channel3_recordings", channel3_recordings)) if name in tasks.CHECK_NAMES}


@app.task(timeout_seconds=3600)
async def evidence_integrity(ctx: TaskContext) -> dict:
    """Run every check as its own subtask (a failed check does not stop the others), then write the receipt.

    The run fails (the task raises) when any check drifted or failed; the receipt is still printed first
    as a RECEIPT log line, because a failed task returns no value.
    """
    results = []
    for name, subtask in SUBTASKS.items():
        try:
            results.append(await ctx.run(subtask))
        except Exception as error:  # the SDK raises TaskRunError("Subtask failed: ...") for a failed subtask
            results.append({"task": name, "ok": False, "drift": tasks.drift_from_message(str(error)),
                            "exit_code": None, "seconds": None, "detail": str(error)[:300]})
    return tasks.write_receipt(results)


if __name__ == "__main__":
    app.start()
