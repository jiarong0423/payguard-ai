"""Deterministic tests for the two-layer synthetic dispute-evidence contract."""

from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from payguard.dispute_evidence import (
    DISPUTE_REASONS,
    DisputeEvidenceError,
    internal_review_narrative,
    restricted_evidence_digest,
    resolve_dispute_requirements,
    validate_attachment_bytes,
    validate_attachment_set,
)


AS_OF = "2026-10-08T09:00:00Z"


def snapshot(reason="INR"):
    return {
        "schema_version": 1,
        "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
        "observed_at": "2026-10-08T08:00:00Z",
        "dispute_id": "demo-case-001",
        "order_id": "demo-order-001",
        "reason": reason,
        "status": "WAITING_FOR_SELLER_RESPONSE",
        "dispute_life_cycle_stage": "INQUIRY",
        "seller_response_due_date": "2026-10-10T08:00:00Z",
        "available_actions": ["PROVIDE_EVIDENCE"],
        "evidences": [{
            "request_id": "request-fulfillment-001",
            "evidence_type": "PROOF_OF_FULFILLMENT",
            "source": "REQUESTED_FROM_SELLER",
            "mandatory": True,
            "action": "PROVIDE_EVIDENCE",
        }],
    }


def proof():
    return {
        "evidence_id": "proof-fulfillment-001",
        "request_id": "request-fulfillment-001",
        "evidence_type": "FULFILLMENT",
        "proof_fields": {
            "carrier_name": "USPS",
            "tracking_number": "SYNTHETICTRACK001",
            "shipped_at": "2026-10-05T10:00:00Z",
            "delivered_at": "2026-10-07T10:00:00Z",
            "delivery_status": "DELIVERED",
            "destination_match_status": "MATCHED_TRANSACTION_DETAILS",
        },
        "observed_at": "2026-10-08T08:30:00Z",
        "evidence_state": "SUPPLIED_UNVERIFIED",
        "attachment_ids": ["attachment-receipt-001"],
    }


def attachment(content=b"%PDF-1.4\nsynthetic receipt"):
    return {
        "attachment_id": "attachment-receipt-001",
        "evidence_id": "proof-fulfillment-001",
        "filename": "synthetic-receipt.pdf",
        "declared_media_type": "application/pdf",
        "content": content,
    }


class ResolverTests(unittest.TestCase):
    def resolve(self, current_snapshot=None, proofs=None, attachments=None, as_of=AS_OF):
        return resolve_dispute_requirements(
            snapshot() if current_snapshot is None else current_snapshot,
            [proof()] if proofs is None else proofs,
            [attachment()] if attachments is None else attachments,
            as_of,
        )

    def assert_code(self, code, operation):
        with self.assertRaises(DisputeEvidenceError) as result:
            operation()
        self.assertEqual(str(result.exception), code)
        self.assertIsNone(result.exception.__cause__)

    def test_ready_result_has_two_layers_and_no_bytes_in_metadata(self):
        result = self.resolve()
        self.assertEqual(result["routing"]["reason"], "MERCHANDISE_OR_SERVICE_NOT_RECEIVED")
        self.assertEqual(result["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")
        self.assertEqual(result["routing"]["requirements"][0]["source"], "REQUESTED_FROM_SELLER")
        self.assertEqual(result["routing"]["requirements"][0]["provider_evidence_type"], "PROOF_OF_FULFILLMENT")
        self.assertEqual(result["routing"]["requirements"][0]["request_id"], "requirement-001")
        self.assertEqual(result["restricted"]["requirements"][0]["request_id"], "request-fulfillment-001")
        self.assertEqual(result["routing"]["requirements"][0]["accepted_attachment_count"], 1)
        self.assertEqual(result["restricted"]["profile"], "RESTRICTED_ORIGINAL_METADATA_V1")
        self.assertEqual(result["restricted_original_summary"]["content_returned"], False)
        serialized = json.dumps(result)
        self.assertNotIn("%PDF", serialized)
        self.assertNotIn("content", result["restricted"]["attachments"][0])

    def test_actual_requested_type_controls_and_static_reason_type_is_not_added(self):
        current = snapshot("MERCHANDISE_OR_SERVICE_NOT_RECEIVED")
        current["evidences"] = [{
            "request_id": "request-refund-001",
            "evidence_type": "PROOF_OF_REFUND",
            "source": "REQUESTED_FROM_SELLER",
            "mandatory": True,
            "action": "PROVIDE_EVIDENCE",
        }]
        refund = {
            "evidence_id": "proof-refund-001",
            "request_id": "request-refund-001",
            "evidence_type": "REFUND",
            "proof_fields": {"refund_id": "synthetic-refund-001", "amount": "10.00", "currency": "USD",
                             "refunded_at": "2026-10-08T07:00:00Z"},
            "observed_at": "2026-10-08T08:30:00Z",
            "evidence_state": "SUPPLIED_UNVERIFIED",
            "attachment_ids": [],
        }
        result = self.resolve(current, [refund], [])
        self.assertEqual([row["provider_evidence_type"] for row in result["routing"]["requirements"]],
                         ["PROOF_OF_REFUND"])
        self.assertNotIn("PROOF_OF_FULFILLMENT", json.dumps(result["routing"]))
        self.assertEqual(result["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")

    def test_non_seller_source_is_context_only(self):
        current = snapshot()
        current["evidences"][0]["source"] = "SUBMITTED_BY_BUYER"
        result = self.resolve(current, [], [])
        self.assertEqual(result["routing"]["requirements"][0]["requirement_state"], "CONTEXT_ONLY")
        self.assertEqual(result["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")

    def test_unknown_provider_type_is_preserved_and_never_coerced(self):
        current = snapshot()
        current["evidences"][0]["evidence_type"] = "PROOF_OF_NEW_PROVIDER_RECORD"
        result = self.resolve(current, [], [])
        row = result["routing"]["requirements"][0]
        self.assertEqual(row["provider_evidence_type"], "PROOF_OF_NEW_PROVIDER_RECORD")
        self.assertIsNone(row["evidence_type"])
        self.assertEqual(row["requirement_state"], "UNMAPPED_EVIDENCE_TYPE")
        self.assertEqual(result["routing"]["overall_state"], "MANUAL_REVIEW")

    def test_missing_mandatory_optional_and_action_states(self):
        result = self.resolve(proofs=[], attachments=[])
        self.assertEqual(result["routing"]["overall_state"], "NEEDS_INPUT")
        self.assertEqual(result["routing"]["requirements"][0]["requirement_state"], "MANDATORY_EVIDENCE_MISSING")
        current = snapshot()
        current["evidences"][0]["mandatory"] = False
        optional = self.resolve(current, [], [])
        self.assertEqual(optional["routing"]["requirements"][0]["requirement_state"], "OPTIONAL_EVIDENCE_MISSING")
        self.assertEqual(optional["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")
        current = snapshot()
        current["available_actions"] = []
        self.assertEqual(self.resolve(current)["routing"]["overall_state"], "ACTION_NOT_AVAILABLE")

    def test_only_exact_provide_evidence_action_creates_seller_requirement(self):
        for action in (None, "ACKNOWLEDGE", "ACCEPT_CLAIM"):
            with self.subTest(action=action):
                current = snapshot()
                current["evidences"][0]["action"] = action
                result = self.resolve(current, [], [])
                self.assertEqual(result["routing"]["requirements"][0]["requirement_state"], "CONTEXT_ONLY")
                self.assertEqual(result["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")

    def test_due_date_case_status_and_stage_precedence(self):
        current = snapshot()
        current["seller_response_due_date"] = AS_OF
        self.assertEqual(self.resolve(current)["routing"]["overall_state"], "DUE_DATE_EXPIRED")
        current = snapshot()
        current["status"] = "RESOLVED"
        self.assertEqual(self.resolve(current)["routing"]["overall_state"], "CASE_NOT_ACTIONABLE")
        current = snapshot()
        current["dispute_life_cycle_stage"] = "UNKNOWN"
        self.assertEqual(self.resolve(current)["routing"]["overall_state"], "MANUAL_REVIEW")
        current["seller_response_due_date"] = AS_OF
        self.assertEqual(self.resolve(current)["routing"]["overall_state"], "DUE_DATE_EXPIRED")

    def test_all_reasons_and_only_inr_alias(self):
        for reason in DISPUTE_REASONS:
            current = snapshot(reason)
            if "PROOF_OF_FULFILLMENT" not in {
                row for row in (
                    "PROOF_OF_FULFILLMENT" if reason in {
                        "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "UNAUTHORISED"
                    } else "OTHER",
                )
            }:
                current["evidences"][0]["evidence_type"] = "OTHER"
                current["evidences"][0]["request_id"] = "request-other-001"
                current["evidences"][0]["mandatory"] = False
                current["evidences"][0]["source"] = "SUBMITTED_BY_BUYER"
                result = self.resolve(current, [], [])
            else:
                result = self.resolve(current)
            self.assertEqual(result["restricted"]["case_snapshot"]["reason"], reason)
        bad = snapshot("NOT_A_REASON")
        self.assert_code("dispute_reason_invalid", lambda: self.resolve(bad))

    def test_snapshot_proof_and_join_fail_closed(self):
        for mutation, code in (
            (lambda value: value.pop("seller_response_due_date"), "dispute_snapshot_invalid"),
            (lambda value: value.__setitem__("seller_response_due_date", "2026-10-10T08:00:00"),
             "dispute_due_date_invalid"),
            (lambda value: value["evidences"].append(deepcopy(value["evidences"][0])),
             "dispute_snapshot_invalid"),
        ):
            current = snapshot()
            mutation(current)
            self.assert_code(code, lambda current=current: self.resolve(current))
        broken = proof()
        broken["request_id"] = "missing-request"
        self.assert_code("proof_record_invalid", lambda: self.resolve(proofs=[broken]))
        broken = proof()
        broken["evidence_type"] = "REFUND"
        self.assert_code("proof_record_invalid", lambda: self.resolve(proofs=[broken]))

    def test_restricted_digest_stable_and_proof_sensitive(self):
        first = self.resolve()
        reordered = {key: snapshot()[key] for key in reversed(list(snapshot()))}
        second = self.resolve(reordered)
        self.assertEqual(first["restricted"]["sha256"], second["restricted"]["sha256"])
        changed = proof()
        changed["proof_fields"]["tracking_number"] = "SYNTHETICTRACK002"
        third = self.resolve(proofs=[changed])
        self.assertNotEqual(first["restricted"]["sha256"], third["restricted"]["sha256"])
        self.assertEqual(restricted_evidence_digest(first["restricted"]), first["restricted"]["sha256"])
        tampered = deepcopy(first["restricted"])
        tampered["proof_records"][0]["proof_fields"]["tracking_number"] = "TAMPERED"
        self.assert_code("restricted_evidence_invalid", lambda: restricted_evidence_digest(tampered))

    def test_internal_narrative_is_safe_and_bounded(self):
        result = self.resolve()
        text = internal_review_narrative(result["routing"])
        self.assertIn("not a PayPal attachment", text)
        self.assertIn("REQUESTED_FROM_SELLER", text)
        for restricted in ("demo-case-001", "demo-order-001", "SYNTHETICTRACK001", "synthetic-refund-001"):
            self.assertNotIn(restricted, text)


class AttachmentTests(unittest.TestCase):
    def assert_code(self, code, operation):
        with self.assertRaises(DisputeEvidenceError) as result:
            operation()
        self.assertEqual(str(result.exception), code)

    def test_supported_signatures_extensions_and_media_types(self):
        samples = (
            ("sample.jpg", "image/jpeg", b"\xff\xd8\xffsynthetic"),
            ("sample.jpeg", "image/jpeg", b"\xff\xd8\xffsynthetic"),
            ("sample.gif", "image/gif", b"GIF87asynthetic"),
            ("sample.gif", "image/gif", b"GIF89asynthetic"),
            ("sample.png", "image/png", b"\x89PNG\r\n\x1a\nsynthetic"),
            ("sample.pdf", "application/pdf", b"%PDF-synthetic"),
        )
        for filename, media_type, body in samples:
            with self.subTest(filename=filename, body=body[:6]):
                result = validate_attachment_bytes(filename, media_type, body)
                self.assertNotIn("content", result)
                self.assertEqual(result["size_bytes"], len(body))

    def test_attachment_mismatch_path_empty_and_unknown_rejected(self):
        cases = (
            ("../sample.pdf", "application/pdf", b"%PDF-x", "attachment_name_invalid"),
            ("sample.pdf.exe", "application/pdf", b"%PDF-x", "attachment_extension_invalid"),
            ("sample.png", "image/png", b"not png", "attachment_signature_invalid"),
            ("sample.pdf", "image/png", b"%PDF-x", "attachment_media_type_invalid"),
            ("sample.pdf", "application/pdf", b"", "attachment_size_invalid"),
        )
        for filename, media_type, body, code in cases:
            with self.subTest(code=code):
                self.assert_code(code, lambda filename=filename, media_type=media_type, body=body:
                                 validate_attachment_bytes(filename, media_type, body))

    def test_individual_and_total_boundaries_without_retaining_bytes(self):
        with patch("payguard.dispute_evidence.MAX_ATTACHMENT_BYTES", 10):
            accepted = validate_attachment_bytes("a.pdf", "application/pdf", b"%PDF-1234")
            self.assertEqual(accepted["size_bytes"], 9)
            self.assert_code("attachment_size_invalid",
                             lambda: validate_attachment_bytes("a.pdf", "application/pdf", b"%PDF-12345"))
        candidates = []
        sizes = [9, 9, 9, 9, 9, 5]
        for index, size in enumerate(sizes):
            candidates.append({
                "attachment_id": f"a-{index}",
                "evidence_id": "proof-1",
                "filename": f"a-{index}.pdf",
                "declared_media_type": "application/pdf",
                "content": b"%PDF-" + b"x" * (size - 5),
            })
        with patch("payguard.dispute_evidence.MAX_ATTACHMENT_BYTES", 10), \
                patch("payguard.dispute_evidence.MAX_ATTACHMENT_SET_BYTES", 50):
            accepted = validate_attachment_set(candidates, ["proof-1"])
            self.assertEqual(sum(row["size_bytes"] for row in accepted), 50)
            larger = deepcopy(candidates)
            larger[-1]["content"] += b"x"
            self.assert_code("attachment_total_size_invalid",
                             lambda: validate_attachment_set(larger, ["proof-1"]))


if __name__ == "__main__":
    unittest.main()
