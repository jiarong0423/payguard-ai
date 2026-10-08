"""Local synthetic acceptance of intake boundaries; no provider/model calls."""

from copy import deepcopy
import importlib
import json
import unittest
from unittest.mock import patch

from payguard.case_contract import DISPUTE_REASONS, get_contract
from payguard.dispute_evidence import PROVIDER_EVIDENCE_TYPE_MAP
from payguard.case_intake import preflight_intake


AS_OF = "2026-10-07T00:00:00Z"
ORIGINS = {
    "source_compliance": {"source_id": "PP-US-AUP", "chunk_id": "PP-US-AUP-POLICY"},
    "velocity_guard": {"source_id": "PP-US-UA", "chunk_id": "PP-US-UA-VELOCITY"},
    "dispute_mediation": {"source_id": "PP-DISPUTE-REASONS-EVIDENCE", "chunk_id": "PP-REASONS-INR"},
}


def envelope(theme="source_compliance", kind="check_activity"):
    return {"schema_version": 1, "intake_id": "demo-intake-001", "requested_theme": theme,
            "request_kind": kind, "jurisdiction": "US", "as_of": AS_OF,
            "observation_max_age_days": 30, "source_class": "synthetic",
            "payload": {}, "evidence_items": []}


def activity():
    d = envelope()
    d["payload"] = {"activity_description": "Synthetic ordinary stationery",
                    "activity_category": "stationery", "approval_requirement": "NOT_APPLICABLE"}
    return d


def velocity():
    d = envelope("velocity_guard", "assess_velocity")
    d["payload"] = {"transactions": [{"order_id": "demo-order-001", "amount": "10.00",
                                      "currency": "USD", "occurred_at": "2026-10-06T23:30:00Z"}],
                    "baseline_amount_per_hour": "100.00", "baseline_provenance": "SYNTHETIC_BASELINE",
                    "baseline_window_start": "2026-10-05T23:00:00Z",
                    "baseline_window_end": "2026-10-06T23:00:00Z",
                    "window_hours": 1, "threshold": "3.5"}
    return d


def add_evidence(d, field, evidence_type, *, state="SUPPLIED_UNVERIFIED", provider_request_id=None):
    evidence_id = "demo-evidence-" + str(len(d["evidence_items"]) + 1)
    if field != "evidences":
        d["payload"][field] = evidence_id
    item = {"evidence_id": evidence_id, "evidence_type": evidence_type,
            "field_id": "payload." + field,
            "origin_ref": deepcopy(ORIGINS[d["requested_theme"]]),
            "observed_at": "2026-10-04T10:00:00Z", "evidence_state": state}
    if provider_request_id is not None:
        item["provider_request_id"] = provider_request_id
    d["evidence_items"].append(item)


def dispute(reason="INR"):
    d = envelope("dispute_mediation", "prepare_dispute_draft")
    d["payload"] = {"merchant_case_ref": "demo-case-001", "order_id": "demo-order-001",
                    "reason_code": reason, "opened_at": "2026-10-04T09:00:00Z",
                    "order_created_at": "2026-10-02T09:00:00Z", "case_stage": "INQUIRY",
                    "case_status": "WAITING_FOR_SELLER_RESPONSE",
                    "seller_response_due_date": "2026-10-08T09:00:00Z",
                    "available_actions": ["PROVIDE_EVIDENCE"], "evidences": []}
    canonical = "MERCHANDISE_OR_SERVICE_NOT_RECEIVED" if reason == "INR" else reason
    spec = get_contract()["routes"]["prepare_dispute_draft"]
    provider_type = spec["reason_matrix"][canonical]["provider_evidence_types"][0]
    request_id = "demo-provider-request-001"
    d["payload"]["evidences"].append({
        "request_id": request_id,
        "evidence_type": provider_type,
        "source": "REQUESTED_FROM_SELLER",
        "mandatory": True,
        "action": "PROVIDE_EVIDENCE",
    })
    add_evidence(d, "evidences", PROVIDER_EVIDENCE_TYPE_MAP[provider_type],
                 provider_request_id=request_id)
    return d


def run(d):
    return preflight_intake(json.dumps(d, ensure_ascii=False))


class CaseIntakeTests(unittest.TestCase):
    def assert_status(self, data, status):
        result = run(data)
        self.assertEqual(result["status"], status, result)
        self.assertTrue(result["required_human_review"])
        self.assertTrue(result["advisory_only"])
        self.assertEqual(result["engine_execution"], "NOT_RUN")
        self.assertEqual(result["caller_provenance"], "UNVERIFIED")
        self.assertEqual(result["operational_authority"], "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION")
        for gate in ("source_authenticity", "evidence_verification", "evidence_sufficiency",
                     "current_policy_applicability", "actor_authorization", "external_action_authorization"):
            self.assertEqual(result["review_gates"][gate], "NOT_ESTABLISHED")
        return result

    def test_three_positive_shapes(self):
        for d in (activity(), velocity(), dispute()):
            with self.subTest(kind=d["request_kind"]):
                self.assert_status(d, "ready_for_local_rules")

    def test_reference_lookup_only_query_and_no_engine(self):
        for theme in get_contract()["common_fields"]["requested_theme"]["values"]:
            d = envelope(theme, "reference_lookup")
            d["payload"] = {"query": "Synthetic reference lookup"}
            result = self.assert_status(d, "ready_for_local_rules")
            self.assertEqual(result["route"], "reference_lookup")
            d["payload"]["activity_description"] = "extra"
            self.assertIsNone(self.assert_status(d, "invalid_input")["route"])

    def test_non_text_json(self):
        for raw in (None, {}, 1, True, b"{}"):
            self.assertEqual(preflight_intake(raw)["status"], "invalid_input")

    def test_bad_json_duplicate_nonfinite(self):
        for raw in ("", "{", "{} trailing", '{"x":1,"x":2}', '{"x":NaN}',
                    '{"x":Infinity}', '{"x":-Infinity}', '{"x":1e9999}', '[]', 'null'):
            with self.subTest(raw=raw):
                result = preflight_intake(raw)
                self.assertEqual(result["status"], "invalid_input")
                self.assertIsNone(result["route"])

    def test_byte_depth_node_and_key_bounds(self):
        for raw in (" " * 16385, json.dumps({"x": "★" * 6000}, ensure_ascii=False),
                    "[" * 14 + "0" + "]" * 14, json.dumps({"k" * 129: 1}),
                    json.dumps([0] * 4097)):
            self.assertEqual(preflight_intake(raw)["status"], "invalid_input")

    def test_surrogates_and_controls(self):
        for bad in ("\ud800", "text\nnewline", "x\u200by", "x\x00y"):
            d = activity()
            d["payload"]["activity_description"] = bad
            self.assert_status(d, "invalid_input")

    def test_unknown_fields_sanitized_at_all_levels(self):
        for location in ("envelope", "payload", "transaction", "evidence", "reference"):
            d = dispute()
            if location == "envelope": target = d
            elif location == "payload": target = d["payload"]
            elif location == "transaction":
                d = velocity(); target = d["payload"]["transactions"][0]
            elif location == "evidence": target = d["evidence_items"][0]
            else:
                d["references"] = [deepcopy(ORIGINS["dispute_mediation"])]
                target = d["references"][0]
            target["PRIVATE_ARBITRARY_KEY"] = "PRIVATE_ARBITRARY_VALUE"
            result = self.assert_status(d, "invalid_input")
            output = json.dumps(result)
            self.assertNotIn("PRIVATE_ARBITRARY_KEY", output)
            self.assertNotIn("PRIVATE_ARBITRARY_VALUE", output)

    def test_unknown_and_multiple_themes_no_default(self):
        for selector in ("UNKNOWN", "unrecognized", ["source_compliance", "velocity_guard"], ["source_compliance"]):
            d = activity(); d["requested_theme"] = selector
            result = self.assert_status(d, "needs_clarification")
            self.assertIsNone(result["route"])
            self.assertIsNone(result["requested_theme"])

    def test_malformed_themes(self):
        for selector in (1, True, {}, [], [1], ["source_compliance"] * 4, "x" * 33, None):
            d = activity(); d["requested_theme"] = selector
            self.assertIsNone(self.assert_status(d, "invalid_input")["route"])

    def test_theme_kind_and_region_no_fallback(self):
        d = activity(); d["requested_theme"] = "velocity_guard"
        self.assert_status(d, "needs_clarification")
        with patch("payguard.retrieval.load_corpus", side_effect=AssertionError("foreign request must fail before corpus load")) as loader:
            for jurisdiction in ("CA", "GB", "GLOBAL"):
                d = dispute(); d["jurisdiction"] = jurisdiction
                self.assert_status(d, "invalid_input")
            loader.assert_not_called()

    def test_every_required_common_missing(self):
        fields = get_contract()["common_fields"]
        for field, spec in fields.items():
            if spec["required"]:
                d = activity(); del d[field]
                result = self.assert_status(d, "needs_input")
                self.assertIn(field, result["missing_fields"])

    def test_common_strict_types(self):
        for field, bad in (("schema_version", True), ("schema_version", 2),
                           ("observation_max_age_days", True), ("observation_max_age_days", -1),
                           ("source_class", "paypal_sandbox"), ("intake_id", "contains space"),
                           ("evidence_items", {}), ("references", {}), ("payload", [])):
            d = activity(); d[field] = bad
            self.assert_status(d, "invalid_input")

    def test_unknown_critical_not_false(self):
        for field in ("jurisdiction", "as_of"):
            d = activity(); d[field] = "UNKNOWN"
            self.assertIn(field, self.assert_status(d, "needs_input")["missing_fields"])
        d = activity(); d["payload"]["approval_requirement"] = "UNKNOWN"
        self.assert_status(d, "needs_input")

    def test_null_rejected(self):
        d = activity(); d["payload"]["approval_requirement"] = None
        self.assert_status(d, "invalid_input")

    def test_timestamp_shapes_and_offsets(self):
        for value in ("2026-10-05", "2026-10-05T00:00:00", "2026-02-30T00:00:00Z",
                      "2026-10-05T00:00:00+25:00"):
            d = activity(); d["as_of"] = value
            self.assert_status(d, "invalid_input")
        d = dispute(); d["as_of"] = "2026-10-07T08:00:00+08:00"
        self.assert_status(d, "ready_for_local_rules")

    def test_decimal_bounds_and_bool_exclusion(self):
        for value in (1, True, "NaN", "Infinity", "-1", "0", "1e101", "1" * 65, " 1 "):
            d = velocity(); d["payload"]["threshold"] = value
            self.assert_status(d, "invalid_input")

    def test_zero_baseline_manual_no_fake_ratio(self):
        d = velocity(); d["payload"]["baseline_amount_per_hour"] = "0"
        result = self.assert_status(d, "manual_review")
        self.assertNotIn("ratio", result)

    def test_velocity_duplicate_currency_and_all_rows(self):
        d = velocity(); d["payload"]["transactions"] *= 2
        self.assert_status(d, "invalid_input")
        d = velocity(); row = deepcopy(d["payload"]["transactions"][0]); row.update(order_id="demo-2", currency="EUR")
        d["payload"]["transactions"].append(row)
        self.assert_status(d, "needs_clarification")
        row["occurred_at"] = "2000-01-01T00:00:00Z"; row["amount"] = "bad"
        self.assert_status(d, "invalid_input")

    def test_velocity_window_and_strict_fields(self):
        for value in (0, 25, True, "1"):
            d = velocity(); d["payload"]["window_hours"] = value
            self.assert_status(d, "invalid_input")
        d = velocity(); del d["payload"]["transactions"][0]["currency"]
        self.assert_status(d, "needs_input")

    def test_velocity_future_transaction_requires_clarification(self):
        d = velocity()
        d["payload"]["transactions"][0]["occurred_at"] = "2026-10-07T00:00:01Z"
        result = self.assert_status(d, "needs_clarification")
        self.assertIn("payload.transactions[].occurred_at", result["conflicts"])
        self.assertIn({"field": "payload.transactions[].occurred_at",
                       "code": "transaction_after_as_of"}, result["diagnostics"])

    def test_velocity_all_transactions_outside_observation_window(self):
        d = velocity()
        d["payload"]["transactions"] = [
            {"order_id": "demo-order-001", "amount": "10.00", "currency": "USD",
             "occurred_at": "2026-10-06T22:00:00Z"},
            {"order_id": "demo-order-002", "amount": "20.00", "currency": "USD",
             "occurred_at": "2026-10-06T23:00:00Z"},
        ]
        result = self.assert_status(d, "needs_clarification")
        self.assertIn("payload.transactions", result["conflicts"])
        self.assertIn({"field": "payload.transactions",
                       "code": "no_transactions_in_observation_window"}, result["diagnostics"])

    def test_velocity_empty_observation_requires_clarification(self):
        d = velocity()
        d["payload"]["transactions"] = []
        result = self.assert_status(d, "needs_clarification")
        self.assertIsNone(result["route"])
        self.assertIn("payload.transactions", result["conflicts"])
        self.assertIn({"field": "payload.transactions",
                       "code": "no_transactions_in_observation_window"}, result["diagnostics"])

    def test_velocity_baseline_must_precede_observation_window(self):
        for start, end in (
                ("2026-10-05T23:00:00Z", "2026-10-06T23:00:01Z"),
                ("2026-10-06T23:15:00Z", "2026-10-06T23:45:00Z")):
            with self.subTest(start=start, end=end):
                d = velocity()
                d["payload"]["baseline_window_start"] = start
                d["payload"]["baseline_window_end"] = end
                result = self.assert_status(d, "needs_clarification")
                self.assertIn("payload.baseline_window_end", result["conflicts"])
                self.assertIn({"field": "payload.baseline_window_end",
                               "code": "baseline_overlaps_observation_window"},
                              result["diagnostics"])

    def test_synthetic_baseline_requires_complete_window(self):
        for field in ("baseline_window_start", "baseline_window_end"):
            with self.subTest(field=field):
                d = velocity()
                del d["payload"][field]
                result = self.assert_status(d, "needs_input")
                self.assertIn("payload." + field, result["missing_fields"])

    def test_baseline_conditional_and_chronology(self):
        d = velocity(); d["payload"]["baseline_provenance"] = "CALLER_SUPPLIED_UNVERIFIED"
        result = self.assert_status(d, "needs_input")
        self.assertIn("payload.baseline_evidence_ref", result["missing_fields"])
        d["payload"].update(baseline_window_start="2026-10-02T00:00:00Z", baseline_window_end="2026-10-04T00:00:00Z")
        add_evidence(d, "baseline_evidence_ref", "BASELINE")
        self.assert_status(d, "ready_for_local_rules")
        d["payload"]["baseline_window_start"] = d["payload"]["baseline_window_end"]
        self.assert_status(d, "needs_clarification")

    def test_velocity_schema_and_provenance_vocabulary_are_exact(self):
        route = get_contract()["routes"]["assess_velocity"]
        self.assertEqual(set(route["payload"]["fields"]), {
            "transactions", "baseline_amount_per_hour", "baseline_provenance",
            "baseline_window_start", "baseline_window_end", "baseline_evidence_ref",
            "window_hours", "threshold", "limitation_review_requested",
            "limitation_notice_ref", "limitation_type", "limitation_status",
            "hold_started_at", "hold_expected_end_at", "kyc_request_status",
            "kyc_response_status", "kyc_request_evidence_ref",
            "fulfillment_review_requested", "fulfillment_capacity_status",
            "fulfillment_evidence_ref",
        })
        transaction_fields = route["payload"]["fields"]["transactions"]["item_spec"]["fields"]
        self.assertEqual(set(transaction_fields), {"order_id", "amount", "currency", "occurred_at"})
        self.assertEqual(
            route["payload"]["fields"]["baseline_provenance"]["values"],
            ["SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED", "UNKNOWN"],
        )
        for unsupported in ("SUPPLIED_UNVERIFIED", "PAYPAL_THRESHOLD"):
            d = velocity()
            d["payload"]["baseline_provenance"] = unsupported
            self.assert_status(d, "invalid_input")
        d = velocity()
        d["payload"]["baseline_provenance"] = "UNKNOWN"
        self.assert_status(d, "needs_input")
        d = velocity()
        d["payload"]["transaction_ids"] = ["demo-order-001"]
        result = self.assert_status(d, "invalid_input")
        self.assertNotIn("transaction_ids", json.dumps(result))

    def test_limitation_kyc_fulfillment_conditionals(self):
        for trigger, value, required in (("limitation_review_requested", True, "limitation_notice_ref"),
                                         ("kyc_request_status", "REQUESTED", "kyc_response_status"),
                                         ("fulfillment_review_requested", True, "fulfillment_evidence_ref")):
            d = velocity(); d["payload"][trigger] = value
            self.assertIn("payload." + required, self.assert_status(d, "needs_input")["missing_fields"])
        d = velocity(); d["payload"]["limitation_review_requested"] = 1
        self.assert_status(d, "invalid_input")

    def test_aup_approval_conditionals(self):
        d = activity(); d["payload"]["approval_requirement"] = "REQUIRED"
        self.assert_status(d, "needs_input")
        d["payload"]["approval_status"] = "CLAIMED_OBTAINED"
        self.assertIn("payload.approval_evidence_ref", self.assert_status(d, "needs_input")["missing_fields"])
        add_evidence(d, "approval_evidence_ref", "APPROVAL")
        self.assert_status(d, "ready_for_local_rules")
        d["payload"]["approval_status"] = "NOT_OBTAINED"
        self.assert_status(d, "manual_review")
        d = activity(); d["payload"]["approval_requirement"] = "PROHIBITED"
        self.assert_status(d, "manual_review")

    def test_nine_reasons_supported_vs_manual(self):
        for reason in DISPUTE_REASONS:
            with self.subTest(reason=reason):
                expected = "ready_for_local_rules" if reason == "MERCHANDISE_OR_SERVICE_NOT_RECEIVED" else "manual_review"
                self.assert_status(dispute(reason), expected)

    def test_provider_response_route_fields_are_required(self):
        for field in ("seller_response_due_date", "available_actions", "evidences"):
            d = dispute(); del d["payload"][field]
            self.assertIn("payload." + field, self.assert_status(d, "needs_input")["missing_fields"])

    def test_unsupported_reason_never_inr_alias(self):
        for value in ("SNAD", "made-up", "UNKNOWN"):
            d = dispute(); d["payload"]["reason_code"] = value
            self.assert_status(d, "invalid_input")
        d = dispute("OTHER")
        self.assert_status(d, "manual_review")

    def test_public_case_not_synthetic_engine(self):
        d = dispute(); d["source_class"] = "public_reference"
        self.assert_status(d, "manual_review")

    def test_only_seller_requested_evidence_enters_missing_queue(self):
        d = dispute(); d["payload"]["evidences"][0]["source"] = "SUBMITTED_BY_BUYER"
        d["evidence_items"] = []
        result = self.assert_status(d, "manual_review")
        self.assertNotIn("seller_requested_evidence_missing", json.dumps(result))
        self.assertIn("seller_request_not_present", json.dumps(result))
        d = dispute(); d["evidence_items"] = []
        result = self.assert_status(d, "needs_input")
        self.assertIn("payload.evidences", result["missing_fields"])

    def test_provider_type_and_source_do_not_fall_back(self):
        d = dispute(); d["payload"]["evidences"][0]["evidence_type"] = "PROOF_OF_NEW_RECORD"
        d["evidence_items"] = []
        result = self.assert_status(d, "manual_review")
        self.assertIn("payload.evidences", result["evidence_gaps"])
        d = dispute(); d["payload"]["evidences"] = []
        d["evidence_items"] = []
        result = self.assert_status(d, "manual_review")
        self.assertNotIn("payload.carrier_status", result["missing_fields"])

    def test_dispute_chronology_review_not_fraud(self):
        d = dispute(); d["payload"]["opened_at"] = "2026-10-01T00:00:00Z"
        self.assert_status(d, "needs_clarification")
        d = dispute(); d["payload"]["seller_response_due_date"] = AS_OF
        result = self.assert_status(d, "manual_review")
        self.assertNotIn("fraud", result)
        d = dispute(); d["payload"]["available_actions"] = []
        self.assert_status(d, "manual_review")

    def test_evidence_foreign_key_field_and_type(self):
        for key, value, expected in (
            ("provider_request_id", "other-id", "needs_input"),
            ("field_id", "payload.refund_evidence_ref", "invalid_input"),
            ("evidence_type", "RETURN", "needs_input"),
            ("field_id", "payload.__class__", "invalid_input"),
        ):
            d = dispute(); d["evidence_items"][0][key] = value
            self.assert_status(d, expected)

    def test_evidence_duplicate_and_missing_keys(self):
        d = dispute(); d["evidence_items"] *= 2
        self.assert_status(d, "invalid_input")
        fields = get_contract()["common_fields"]["evidence_items"]["item_spec"]["fields"]
        for key in [name for name, spec in fields.items() if spec.get("required")]:
            d = dispute(); del d["evidence_items"][0][key]
            self.assert_status(d, "needs_input")

    def test_evidence_unknown_allegation_adjudicator_not_authority(self):
        for state in ("PARTY_ALLEGATION", "ADJUDICATOR_FINDING", "DOCUMENT_STATED"):
            d = dispute(); d["evidence_items"][0]["evidence_state"] = state
            self.assert_status(d, "ready_for_local_rules")
        d = dispute(); d["evidence_items"][0]["evidence_state"] = "UNKNOWN"
        self.assert_status(d, "manual_review")
        d["evidence_items"][0]["evidence_state"] = "CONFLICTING_SOURCES"
        self.assert_status(d, "needs_clarification")

    def test_provider_evidence_matching_and_duplicate_request(self):
        d = dispute(); d["payload"]["evidences"][0]["mandatory"] = False
        d["evidence_items"] = []
        self.assert_status(d, "ready_for_local_rules")
        d = dispute(); d["payload"]["evidences"] *= 2
        self.assert_status(d, "invalid_input")

    def test_reference_unknown_join_duplicate_and_origin(self):
        for change in ({"source_id": "PP-CA-AUP"}, {"chunk_id": "NOT-A-CHUNK"}):
            d = dispute(); d["evidence_items"][0]["origin_ref"].update(change)
            self.assert_status(d, "invalid_input")
        d = activity(); d["references"] = [deepcopy(ORIGINS["source_compliance"])] * 2
        self.assert_status(d, "invalid_input")
        d = dispute(); d["evidence_items"][0]["origin_ref"] = "UNKNOWN"
        self.assert_status(d, "needs_input")

    def test_reference_as_of_and_freshness(self):
        d = dispute(); d["as_of"] = "2025-01-01T00:00:00Z"
        self.assert_status(d, "needs_clarification")
        d = dispute(); d["observation_max_age_days"] = 0
        self.assert_status(d, "needs_clarification")
        d = dispute(); d["references"] = [deepcopy(ORIGINS["source_compliance"])]
        self.assert_status(d, "needs_clarification")

    def test_corpus_failure_closed_sanitized(self):
        d = dispute()
        with patch("payguard.retrieval.load_corpus", side_effect=ValueError("SECRET_PATH_VALUE")):
            result = self.assert_status(d, "invalid_input")
        self.assertIsNone(result["route"])
        self.assertNotIn("SECRET_PATH_VALUE", json.dumps(result))

    def test_no_load_when_no_references(self):
        with patch("payguard.retrieval.load_corpus", side_effect=AssertionError("not expected")):
            self.assert_status(activity(), "ready_for_local_rules")

    def test_precedence_invalid_clarify_missing_manual(self):
        d = dispute("OTHER"); d["jurisdiction"] = "CA"; del d["payload"]["order_id"]
        self.assert_status(d, "invalid_input")
        d["payload"]["order_created_at"] = "bad"
        self.assert_status(d, "invalid_input")
        d = dispute("OTHER"); del d["payload"]["order_id"]
        self.assert_status(d, "needs_input")

    def test_missing_reference_parts_do_not_become_corpus_failure(self):
        d = dispute(); del d["evidence_items"][0]["origin_ref"]["chunk_id"]
        self.assert_status(d, "needs_input")
        d = dispute(); del d["observation_max_age_days"]
        self.assert_status(d, "needs_input")

    def test_no_engine_called_from_claimed_synthetic(self):
        with patch("payguard.engines.prepare_dispute", side_effect=AssertionError("forbidden")), \
             patch("payguard.engines.check_aup", side_effect=AssertionError("forbidden")), \
             patch("payguard.engines.assess_velocity", side_effect=AssertionError("forbidden")):
            for data in (activity(), velocity(), dispute()):
                self.assert_status(data, "ready_for_local_rules")

    def test_outputs_independent_no_payload_and_import_no_io(self):
        d = dispute(); before = deepcopy(d)
        result = run(d); result["review_gates"]["source_authenticity"] = "FORGED"
        self.assert_status(d, "ready_for_local_rules")
        self.assertEqual(d, before)
        self.assertNotIn("payload", run(d))
        import payguard.case_intake as module
        with patch("builtins.open", side_effect=AssertionError("import I/O forbidden")), \
             patch("payguard.retrieval.load_corpus", side_effect=AssertionError("load forbidden")):
            importlib.reload(module)


if __name__ == "__main__":
    unittest.main()
