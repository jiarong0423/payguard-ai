"""Complete synthetic demonstration; stdout only, no business artifact writes."""

import argparse
from datetime import datetime, timezone
import json
import logging
import secrets

from payguard.engines import check_aup, assess_velocity, prepare_dispute
from payguard.ingest import collect_events
from payguard.policy import VelocityPolicy
from payguard.privacy import redact_identity
from payguard.reporting import compose_report
from payguard.review import LocalReviewGate


def demo() -> dict:
    policy = VelocityPolicy()
    events = [{"event_id": "demo-event-" + str(index), "source": "synthetic",
               "event_type": "PAYMENT.CAPTURE.COMPLETED",
               "resource": {"order_id": "demo-order-" + str(index), "amount": "100.00", "currency": "USD",
                            "occurred_at": "2026-10-04T06:30:00+00:00"}} for index in range(4)]
    transactions = collect_events(events + [events[0]])
    aup = check_aup("Guaranteed 500% ROI on this investment")
    velocity = assess_velocity(transactions, "100.00", "2026-10-04T07:00:00+00:00",
                               window_hours=policy.window_hours, threshold=policy.threshold,
                               baseline_provenance="SYNTHETIC_BASELINE",
                               baseline_window_start="2026-10-03T06:00:00+00:00",
                               baseline_window_end="2026-10-04T06:00:00+00:00")
    dispute = prepare_dispute({"case_id": "demo-case-1", "order_id": "demo-order-0",
                               "reason": "INR", "opened_at": "2026-10-04T07:00:00+00:00",
                               "order_created_at": "2026-10-01T07:00:00+00:00",
                               "carrier_status": "delivered", "delivered_at": "2026-10-03T07:00:00+00:00",
                               "evidence_source": "synthetic"})
    gate = LocalReviewGate()
    now = datetime.now(timezone.utc)
    approval = gate.approve(dispute, actor="demo-merchant", now=now)
    review = gate.consume(approval, dispute, actor="demo-merchant", now=now)
    tokens = redact_identity({"name": "Synthetic Buyer", "address": "Demo Address", "email": "buyer@example.invalid"},
                             secrets.token_bytes(32))
    privacy = {"status": "pseudonymized", "tokens": tokens, "raw_identity_exported": False,
               "key_lifecycle": "ephemeral_demo_only", "anonymization_claim": False}
    return compose_report(aup, velocity, dispute, review, privacy)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        print(json.dumps(demo(), ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError):
        logging.error("PAYGUARD_DEMO_VALIDATION_FAILED")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
