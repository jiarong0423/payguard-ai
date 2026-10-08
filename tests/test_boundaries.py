import copy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import secrets
import unittest

from payguard.ingest import collect_events
from payguard.policy import VelocityPolicy
from payguard.privacy import redact_identity
from payguard.reporting import compose_report
from payguard.review import LocalReviewGate


def event():
    return {"event_id": "demo-event-1", "source": "synthetic", "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"order_id": "demo-order-1", "amount": "10.00", "currency": "USD",
                         "occurred_at": "2026-10-04T07:00:00+00:00"}}


class IngestBoundaryTests(unittest.TestCase):
    def test_identical_replay_is_noop_without_input_mutation(self):
        data = event()
        original = copy.deepcopy(data)
        self.assertEqual(collect_events([data, data]), [data["resource"]])
        self.assertEqual(data, original)

    def test_collision_rejects_batch(self):
        first, second = event(), event()
        second["resource"]["amount"] = "99.00"
        with self.assertRaisesRegex(ValueError, "event_id_collision"):
            collect_events([first, second])

    def test_unverified_and_pii_inputs_rejected(self):
        real = event()
        real["source"] = "paypal"
        with self.assertRaisesRegex(ValueError, "unverified_event_source"):
            collect_events([real])
        real = event()
        real["resource"]["payer_email"] = "buyer@example.invalid"
        with self.assertRaisesRegex(ValueError, "invalid_resource_schema"):
            collect_events([real])


class PrivacyBoundaryTests(unittest.TestCase):
    def test_domain_separated_normalized_pseudonyms_no_raw_fields(self):
        key = secrets.token_bytes(32)
        tokens = redact_identity({"name": "Demo", "address": "Demo"}, key)
        equivalent = redact_identity({"name": "  DEMO "}, key)
        self.assertEqual(tokens["name_token"], equivalent["name_token"])
        self.assertNotEqual(tokens["name_token"], tokens["address_token"])
        self.assertNotIn("name", tokens)
        self.assertNotIn("Demo", str(tokens))
        self.assertNotEqual(tokens["name_token"], redact_identity({"name": "Demo"}, secrets.token_bytes(32))["name_token"])

    def test_card_fields_and_weak_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "identity_fields_not_allowlisted"):
            redact_identity({"card_number": "synthetic-only"}, secrets.token_bytes(32))
        with self.assertRaisesRegex(ValueError, "invalid_token_key"):
            redact_identity({"name": "Demo"}, b"short")


class PolicyBoundaryTests(unittest.TestCase):
    def test_invalid_measurement_definitions_fail_closed(self):
        for threshold in ("NaN", "Infinity", "-1", "0"):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                VelocityPolicy(threshold=threshold)
        for window in (0, 25, True, 1.5):
            with self.subTest(window=window), self.assertRaises(ValueError):
                VelocityPolicy(window_hours=window)


class ReviewBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 4, 7, tzinfo=timezone.utc)
        self.draft = {"case_id": "demo-case-1", "status": "review_evidence", "evidence": {"source": "synthetic"}}
        self.gate = LocalReviewGate()
        self.approval = self.gate.approve(self.draft, actor="demo-merchant", now=self.now)

    def test_approval_once_no_external_side_effect(self):
        result = self.gate.consume(self.approval, self.draft, actor="demo-merchant", now=self.now)
        self.assertEqual(result["external_submission"], "FROZEN")
        with self.assertRaisesRegex(ValueError, "approval_already_used"):
            self.gate.consume(self.approval, self.draft, actor="demo-merchant", now=self.now)

    def test_case_payload_actor_and_action_binding(self):
        for draft, actor, action in ((dict(self.draft, case_id="demo-case-2"), "demo-merchant", "review_draft"),
                                     (dict(self.draft, status="changed"), "demo-merchant", "review_draft"),
                                     (self.draft, "demo-other", "review_draft"),
                                     (self.draft, "demo-merchant", "submit_evidence")):
            with self.subTest(draft=draft, actor=actor, action=action), self.assertRaises(ValueError):
                self.gate.consume(self.approval, draft, actor=actor, now=self.now, action=action)

    def test_tampering_expiry_future_and_naive_clock(self):
        with self.assertRaisesRegex(ValueError, "approval_tampered"):
            self.gate.consume(replace(self.approval, actor="demo-other"), self.draft, actor="demo-other", now=self.now)
        for now in (self.now + timedelta(seconds=300), self.now - timedelta(seconds=1)):
            with self.assertRaisesRegex(ValueError, "approval_expired_or_future"):
                self.gate.consume(self.approval, self.draft, actor="demo-merchant", now=now)
        with self.assertRaisesRegex(ValueError, "timezone_required"):
            self.gate.approve(self.draft, actor="demo-merchant", now=self.now.replace(tzinfo=None))

    def test_approval_cannot_move_between_gate_instances(self):
        with self.assertRaisesRegex(ValueError, "approval_tampered"):
            LocalReviewGate().consume(self.approval, self.draft, actor="demo-merchant", now=self.now)


class ReportBoundaryTests(unittest.TestCase):
    def test_contract_failure_is_visible(self):
        with self.assertRaisesRegex(ValueError, "backend_contract_invalid_aup"):
            compose_report({}, {}, {}, {}, {})
        aup = {"match_status": "NO_MATCH", "compliance_decision": "NOT_MADE", "advisory_only": True}
        with self.assertRaisesRegex(ValueError, "backend_contract_missing_status"):
            compose_report(aup, {}, {}, {}, {})

    def test_aup_module_contract_rejects_legacy_ambiguous_and_assurance(self):
        aup = {"match_status": "NO_MATCH", "compliance_decision": "NOT_MADE", "advisory_only": True}
        other = {"status": "synthetic_test"}
        for changes in ({"status": "manual_review"}, {"match_status": "APPROVED"},
                        {"compliance_decision": "COMPLIANT"}, {"advisory_only": False}, {"advisory_only": 1}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, "backend_contract_invalid_aup"):
                compose_report(dict(aup, **changes), other, other, other, other)
        legacy = {"status": "manual_review", "compliance_decision": "NOT_MADE", "advisory_only": True}
        with self.assertRaisesRegex(ValueError, "backend_contract_invalid_aup"):
            compose_report(legacy, other, other, other, other)
        for match_status in ("NO_MATCH", "REVIEW_SIGNAL"):
            result = compose_report(dict(aup, match_status=match_status), other, other, other, other)
            self.assertEqual(result["aup"]["match_status"], match_status)

    def test_demo_three_paths_are_wired_and_policy_is_single_source(self):
        from payguard.cli import demo
        report = demo()
        self.assertTrue(report["aup"]["findings"])
        self.assertEqual(report["aup"]["match_status"], "REVIEW_SIGNAL")
        self.assertEqual(report["aup"]["compliance_decision"], "NOT_MADE")
        self.assertNotIn("status", report["aup"])
        self.assertEqual(report["velocity"]["status"], "review_velocity")
        self.assertEqual(report["dispute"]["status"], "review_evidence")
        self.assertEqual(report["external_submission"], "FROZEN")
        self.assertEqual(report["aup"]["policy_version"], VelocityPolicy().version)
        self.assertEqual(report["velocity"]["policy_version"], report["dispute"]["policy_version"])
        self.assertNotIn("Synthetic Buyer", str(report))


if __name__ == "__main__":
    unittest.main()
