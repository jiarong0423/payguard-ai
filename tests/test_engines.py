"""Meaningful boundary checks over entirely synthetic fixtures."""

from copy import deepcopy
from decimal import Inexact, localcontext
import unittest

from payguard.engines import assess_velocity, check_aup, prepare_dispute


AS_OF = "2026-10-04T12:00:00Z"


def transaction(order_id="demo-1", amount="350", occurred_at=AS_OF, currency="USD"):
    return {"order_id": order_id, "amount": amount, "currency": currency, "occurred_at": occurred_at}


def dispute():
    return {
        "case_id": "demo-case-1", "order_id": "demo-order-1", "reason": "INR",
        "order_created_at": "2026-10-01T08:00:00Z",
        "delivered_at": "2026-10-02T08:00:00Z",
        "opened_at": "2026-10-03T08:00:00Z",
        "carrier_status": "delivered", "evidence_source": "synthetic",
    }


def assess_declared_velocity(*args, **kwargs):
    kwargs.setdefault("baseline_provenance", "CALLER_SUPPLIED_UNVERIFIED")
    kwargs.setdefault("baseline_window_start", "2026-10-01T00:00:00Z")
    kwargs.setdefault("baseline_window_end", "2026-10-02T00:00:00Z")
    return assess_velocity(*args, **kwargs)


class AupTests(unittest.TestCase):
    def test_restricted_keywords_never_offer_rewriting(self):
        result = check_aup("Counterfeit luxury bags and firearms")
        self.assertEqual(result["match_status"], "REVIEW_SIGNAL")
        self.assertEqual({item["category"] for item in result["findings"]}, {"weapons", "counterfeit_goods"})
        self.assertIn("Do not disguise", result["recommendation"])
        self.assertTrue(result["advisory_only"])
        self.assertEqual(result["compliance_decision"], "NOT_MADE")

    def test_no_keyword_does_not_certify_compliance(self):
        result = check_aup("Synthetic handmade ceramic cup")
        self.assertEqual(result["match_status"], "NO_MATCH")
        self.assertEqual(result["findings"], [])
        self.assertIn("does not certify", result["recommendation"])

    def test_unicode_normalization_and_english_only_categories(self):
        self.assertEqual(check_aup("ＦＩＲＥＡＲＭＳ")["match_status"], "REVIEW_SIGNAL")
        self.assertEqual(check_aup("Synthetic counterfeit goods")["match_status"], "REVIEW_SIGNAL")
        self.assertEqual(check_aup("Synthetic café décor")["match_status"], "NO_MATCH")

    def test_text_boundaries(self):
        for value in (None, "", " ", "a" * 4001, "gun\x00", "g\u200bun"):
            with self.subTest(value=repr(value)[:50]), self.assertRaises(ValueError):
                check_aup(value)
        self.assertEqual(check_aup("a" * 4000)["match_status"], "NO_MATCH")

    def test_description_is_not_echoed(self):
        text = "SYNTHETIC-RAW-TEXT-NOT-OUTPUT"
        self.assertNotIn(text, str(check_aup(text)))


class VelocityTests(unittest.TestCase):
    def test_strict_threshold(self):
        exact = assess_declared_velocity([transaction()], "100", AS_OF)
        above = assess_declared_velocity([transaction(amount="350.000000000000000000000000001")], "100", AS_OF)
        below = assess_declared_velocity([transaction(amount="349.999999999999999999999999999")], "100", AS_OF)
        self.assertEqual(exact["status"], "normal")
        self.assertFalse(exact["alert"])
        self.assertEqual(above["status"], "review_velocity")
        self.assertTrue(above["alert"])
        self.assertFalse(below["alert"])

    def test_window_and_timezone_equivalence(self):
        rows = [
            transaction("left", "9", "2026-10-04T11:00:00Z"),
            transaction("inside", "10", "2026-10-04T19:00:00.000001+08:00"),
            transaction("right", "20", "2026-10-04T20:00:00+08:00"),
            transaction("future", "900", "2026-10-04T12:00:00.000001Z"),
        ]
        result = assess_declared_velocity(rows, "100", AS_OF)
        self.assertEqual(result["total_amount"], "30")
        self.assertEqual(result["transaction_count"], 2)
        self.assertEqual(result["excluded_future_count"], 1)
        self.assertEqual(result["excluded_past_count"], 1)
        self.assertEqual(result["window_start"], "2026-10-04T11:00:00Z")

    def test_multi_hour_rate_uses_duration(self):
        result = assess_declared_velocity([transaction(amount="600")], "100", AS_OF, window_hours=2)
        self.assertEqual(result["current_amount_per_hour"], "300")
        self.assertEqual(result["ratio"], "3")
        self.assertFalse(result["alert"])

    def test_declared_synthetic_baseline_has_non_overlapping_window(self):
        result = assess_declared_velocity(
            [transaction()],
            "100",
            AS_OF,
            baseline_provenance="SYNTHETIC_BASELINE",
            baseline_window_start="2026-10-03T11:00:00Z",
            baseline_window_end="2026-10-04T11:00:00Z",
        )
        self.assertEqual(result["baseline_provenance"], "SYNTHETIC_BASELINE")
        self.assertEqual(result["baseline_window_start"], "2026-10-03T11:00:00Z")
        self.assertEqual(result["baseline_window_end"], result["window_start"])

    def test_every_supported_baseline_requires_complete_preceding_window(self):
        cases = (
            {},
            {"baseline_window_start": "2026-10-03T11:00:00Z"},
            {"baseline_window_end": "2026-10-04T11:00:00Z"},
            {
                "baseline_window_start": "2026-10-04T10:00:00Z",
                "baseline_window_end": "2026-10-04T11:30:00Z",
            },
        )
        for provenance in ("SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED"):
            for extra in cases:
                with self.subTest(provenance=provenance, extra=extra), self.assertRaises(ValueError):
                    assess_velocity(
                        [transaction()],
                        "100",
                        AS_OF,
                        baseline_provenance=provenance,
                        **extra,
                    )

    def test_provenance_vocabulary_is_exact(self):
        for provenance in ("SUPPLIED_UNVERIFIED", "UNKNOWN", "PAYPAL_THRESHOLD"):
            with self.subTest(provenance=provenance), self.assertRaises(ValueError):
                assess_velocity(
                    [transaction()],
                    "100",
                    AS_OF,
                    baseline_provenance=provenance,
                    baseline_window_start="2026-10-01T00:00:00Z",
                    baseline_window_end="2026-10-02T00:00:00Z",
                )

    def test_zero_baseline_and_empty_input(self):
        result = assess_declared_velocity([transaction()], "0", AS_OF)
        self.assertEqual(result["status"], "insufficient_baseline")
        self.assertIsNone(result["ratio"])
        self.assertFalse(result["alert"])
        empty = assess_declared_velocity([], "100", AS_OF)
        self.assertEqual(empty["status"], "normal")
        self.assertEqual(empty["total_amount"], "0")
        self.assertIsNone(empty["currency"])

    def test_duplicate_ids_including_outside_window_rejected(self):
        rows = [transaction(), transaction(occurred_at="2026-10-01T12:00:00Z")]
        with self.assertRaises(ValueError):
            assess_declared_velocity(rows, "100", AS_OF)

    def test_mixed_currency_including_future_rejected(self):
        rows = [transaction(), transaction("future", occurred_at="2026-10-05T12:00:00Z", currency="EUR")]
        with self.assertRaises(ValueError):
            assess_declared_velocity(rows, "100", AS_OF)

    def test_invalid_amounts_are_rejected_before_calculation(self):
        for amount in ("NaN", "Infinity", "-Infinity", "0", "-1", 1, 1.2, True, " 1", "1_000", "1e101", "9" * 65):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                assess_declared_velocity([transaction(amount=amount)], "100", AS_OF)

    def test_invalid_baseline_threshold_window_and_time(self):
        for baseline in ("NaN", "Infinity", "-1", 100, "1e101"):
            with self.subTest(baseline=baseline), self.assertRaises(ValueError):
                assess_declared_velocity([], baseline, AS_OF)
        for threshold in ("0", "-1", "NaN", "Infinity", 3.5):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                assess_declared_velocity([], "100", AS_OF, threshold=threshold)
        for hours in (0, -1, 1.5, True, "1", 10**30):
            with self.subTest(hours=hours), self.assertRaises(ValueError):
                assess_declared_velocity([], "100", AS_OF, window_hours=hours)
        for date in ("2026-10-04T12:00:00", "invalid", "2026-10-04", None):
            with self.subTest(date=date), self.assertRaises(ValueError):
                assess_declared_velocity([], "100", date)

    def test_schema_identifier_currency_and_out_of_window_time_validation(self):
        for row in ({}, dict(transaction(), extra="x"), dict(transaction(), order_id="../x"), dict(transaction(), currency="usd"), dict(transaction(), occurred_at="2026-10-01T12:00:00")):
            with self.subTest(row=row), self.assertRaises(ValueError):
                assess_declared_velocity([row], "100", AS_OF)
        with self.assertRaises(ValueError):
            assess_declared_velocity(tuple(), "100", AS_OF)

    def test_decimal_arithmetic_and_no_mutation(self):
        rows = [transaction("first", "0.1"), transaction("second", "0.2")]
        original = deepcopy(rows)
        self.assertEqual(assess_declared_velocity(rows, "1", AS_OF)["total_amount"], "0.3")
        self.assertEqual(rows, original)

    def test_ambient_decimal_context_does_not_change_results(self):
        with localcontext() as context:
            context.prec = 2
            context.traps[Inexact] = True
            result = assess_declared_velocity([transaction(amount="123.45")], "7", AS_OF, window_hours=3)
        self.assertEqual(result["current_amount_per_hour"], "41.15")
        self.assertTrue(result["alert"])

    def test_submicrosecond_timestamp_is_rejected_without_truncation(self):
        with self.assertRaises(ValueError):
            assess_declared_velocity([transaction(occurred_at="2026-10-04T12:00:00.0000001Z")], "100", AS_OF)


class DisputeTests(unittest.TestCase):
    def test_complete_inr_produces_objective_review_draft(self):
        case = dispute()
        original = deepcopy(case)
        result = prepare_dispute(case)
        self.assertEqual(result["status"], "review_evidence")
        self.assertEqual(result["case_id"], case["case_id"])
        self.assertEqual(result["evidence"], case)
        self.assertEqual(result["review_reasons"], [])
        self.assertTrue(result["advisory_only"])
        self.assertEqual(case, original)
        self.assertFalse({"buyer_malicious", "won", "resolved"} & set(result))
        self.assertIn("does not establish buyer intent", " ".join(result["limitations"]))

    def test_non_inr_is_always_manual_review(self):
        for reason in ("unauthorized", "SNAD", "UNSUPPORTED_REASON"):
            with self.subTest(reason=reason):
                result = prepare_dispute(dict(dispute(), reason=reason))
                self.assertEqual(result["status"], "manual_review")
                self.assertIn("unsupported_reason", result["review_reasons"])

    def test_missing_evidence_is_manual_review(self):
        for field in set(dispute()) - {"evidence_source"}:
            case = dispute()
            del case[field]
            with self.subTest(field=field):
                result = prepare_dispute(case)
                self.assertEqual(result["status"], "manual_review")
                if field == "delivered_at":
                    self.assertIn("missing_delivered_at", result["review_reasons"])
                else:
                    self.assertIn(f"missing_{field}", result["review_reasons"])
                self.assertIn("case_id", result)

    def test_not_shipped_does_not_invent_or_require_delivery_timestamp(self):
        case = dispute()
        case["carrier_status"] = "not_shipped"
        del case["delivered_at"]
        result = prepare_dispute(case)
        self.assertEqual(result["status"], "manual_review")
        self.assertIn("delivery_not_confirmed", result["review_reasons"])
        self.assertNotIn("missing_delivered_at", result["review_reasons"])
        self.assertNotIn("delivered_at", result["evidence"])

    def test_chronology_conflicts_and_equal_delivery_are_manual_review(self):
        changes = (
            {"delivered_at": "2026-09-30T08:00:00Z"},
            {"order_created_at": "2026-10-04T08:00:00Z"},
            {"delivered_at": "2026-10-03T08:00:00Z"},
            {"delivered_at": "2026-10-04T08:00:00Z"},
        )
        for change in changes:
            with self.subTest(change=change):
                self.assertEqual(prepare_dispute(dict(dispute(), **change))["status"], "manual_review")

    def test_carrier_contradiction_is_manual_review(self):
        result = prepare_dispute(dict(dispute(), carrier_status="in_transit"))
        self.assertEqual(result["status"], "manual_review")
        self.assertIn("carrier_timestamp_conflict", result["review_reasons"])

    def test_timezone_offsets_are_normalized_for_comparison(self):
        case = dict(dispute(), delivered_at="2026-10-02T16:00:00+08:00")
        result = prepare_dispute(case)
        self.assertEqual(result["status"], "review_evidence")
        self.assertEqual(result["evidence"]["delivered_at"], "2026-10-02T08:00:00Z")

    def test_unknown_fields_private_text_and_real_source_rejected(self):
        cases = (
            dict(dispute(), customer_email="synthetic@example.invalid"),
            dict(dispute(), raw_text="synthetic unrestricted text"),
            dict(dispute(), evidence_source="paypal"),
            dict(dispute(), evidence_source=None),
            dict(dispute(), case_id="bad identifier"),
            dict(dispute(), carrier_status="unknown-status"),
            dict(dispute(), opened_at="2026-10-03T08:00:00"),
        )
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                prepare_dispute(case)


if __name__ == "__main__":
    unittest.main()
