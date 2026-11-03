"""Build the data files behind the AG Studio dispute evidence readiness dashboard (/dashboard.html).

Nothing here is invented and nothing calls the network. Two outputs:
  frontend/src/data/dashboard_disputes_v1.json
      The synthetic dispute cases the console's "Load dispute case" button creates (three since round 5), read back
      through the real backend (FastAPI app, in-process test client, no socket) at a fixed clock:
      the dispute summaries, each case's draft routing (due date, readiness, requirement states,
      proof and attachment counts), review reasons and, where present, the ordered time evidence.
  frontend/src/data/channel3_receipts_v1.json
      A byte-for-byte copy of docs/evidence/channel3_receipts_v1.json.

  python3 tools/build_dashboard_data.py            write both files
  python3 tools/build_dashboard_data.py --check    compare the committed files with a fresh build (exit 1 on drift)
"""

import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "backend"))

DISPUTES_OUT = ROOT / "frontend" / "src" / "data" / "dashboard_disputes_v1.json"
RECEIPTS_IN = ROOT / "docs" / "evidence" / "channel3_receipts_v1.json"
RECEIPTS_OUT = ROOT / "frontend" / "src" / "data" / "channel3_receipts_v1.json"
# The dashboard's "today". Every due date and gap below is relative to this fixed instant.
AS_OF = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)
ORIGIN = "http://localhost:5173"


def build_disputes() -> dict:
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.store import SessionStore

    application = create_app(store=SessionStore(clock=lambda: AS_OF))
    with TestClient(application, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55010)) as client:
        session = client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        state = client.post("/api/v1/demo/inject", json={"scenario": "dispute"}, headers=headers)
        state.raise_for_status()
        cases = []
        for summary in state.json()["disputes"]:
            response = client.post(f"/api/v1/disputes/{summary['case_ref']}/draft", json={}, headers=headers)
            response.raise_for_status()
            draft = response.json()
            routing = draft["routing"]
            time_evidence = draft.get("time_evidence")
            cases.append({
                "case_ref": summary["case_ref"],
                "order_ref": summary["order_ref"],
                "reason": summary["reason"],
                "opened_at": summary["opened_at"],
                "provider_reason": routing["reason"],
                "provider_status": routing["status"],
                "lifecycle_stage": routing["dispute_life_cycle_stage"],
                "seller_response_due_date": routing["seller_response_due_date"],
                "due_state": routing["due_state"],
                "overall_state": routing["overall_state"],
                "human_review_required": routing["human_review_required"],
                "provider_submission": routing["provider_submission"],
                "carrier_status": draft["evidence"]["carrier_status"],
                "delivered_at": draft["evidence"]["delivered_at"],
                "requirements": [{
                    "provider_evidence_type": row["provider_evidence_type"],
                    "evidence_type": row["evidence_type"],
                    "mandatory": row["mandatory"],
                    "requirement_state": row["requirement_state"],
                    "proof_count": row["proof_count"],
                    "accepted_attachment_count": row["accepted_attachment_count"],
                } for row in routing["requirements"]],
                "review_reasons": draft["review_reasons"],
                "time_evidence": None if time_evidence is None else {
                    # message_digest is keyed per session with a random key, so it is left out: it would
                    # change on every build and the dashboard never shows it.
                    "events": [{key: value for key, value in event.items() if key != "message_digest"}
                               for event in time_evidence["events"]],
                    "gaps_seconds": time_evidence["gaps_seconds"],
                    "flags": time_evidence["flags"],
                    "judgement": time_evidence["judgement"],
                },
            })
    return {
        "schema_version": "payguard.dashboard_disputes.v1",
        "source": ("Synthetic dispute cases from backend/app/store.py, read back through the real API "
                   "(POST /api/v1/demo/inject, POST /api/v1/disputes/{case_ref}/draft) by tools/build_dashboard_data.py."),
        "as_of": AS_OF.isoformat().replace("+00:00", "Z"),
        "synthetic": True,
        "affects_decision": False,
        "cases": cases,
    }


def render(document: dict) -> str:
    return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv) -> int:
    disputes = render(build_disputes())
    receipts = RECEIPTS_IN.read_bytes()
    if "--check" in argv:
        drift = []
        if not DISPUTES_OUT.is_file() or DISPUTES_OUT.read_text(encoding="utf-8") != disputes:
            drift.append(str(DISPUTES_OUT.relative_to(ROOT)))
        if not RECEIPTS_OUT.is_file() or RECEIPTS_OUT.read_bytes() != receipts:
            drift.append(str(RECEIPTS_OUT.relative_to(ROOT)))
        if drift:
            print("DRIFT: " + ", ".join(drift) + " (run python3 tools/build_dashboard_data.py)")
            return 1
        print("dashboard data: no drift")
        return 0
    DISPUTES_OUT.write_text(disputes, encoding="utf-8")
    RECEIPTS_OUT.write_bytes(receipts)
    print(f"wrote {DISPUTES_OUT.relative_to(ROOT)} and {RECEIPTS_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
