"""Synthetic-only text, overlap, isolation and strict API-contract challenges."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
import logging
import re
import socket
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import create_app
from app.schemas import DocumentRedaction, DisputeDraftResponse
from app.store import BoundaryError, SessionStore
from payguard.document_privacy import DocumentPrivacyError, MAX_TEXT_BYTES, redact_dispute_document
from payguard.dispute_evidence import DisputeEvidenceError
from payguard.privacy import redact_identity
from payguard.review import payload_digest


KEY = bytes(range(32))


def redact(text, *, key=KEY, document_id="synthetic-document-001", literals=None):
    return redact_dispute_document(text, key, document_id=document_id, literals=literals)


class DocumentTests(unittest.TestCase):
    def test_output_is_labeled_for_internal_review_export_only(self):
        self.assertEqual(redact("ordinary evidence")["export_profile"], "INTERNAL_REVIEW_ONLY_V1")

    def assert_error(self, code, operation):
        with self.assertRaises(DocumentPrivacyError) as result:
            operation()
        self.assertEqual(str(result.exception), code)
        self.assertEqual(repr(result.exception), "DocumentPrivacyError('" + code + "')")
        self.assertIsNone(result.exception.__cause__)

    def test_all_fixed_us_patterns_with_ascii_boundaries(self):
        text = "Customer demo@example.invalid, phones (415) 555-0123 and +1 646 555 0199, synthetic SSN 123-45-6789."
        result = redact(text)
        for raw in ("demo@example.invalid", "(415) 555-0123", "+1 646 555 0199", "123-45-6789"):
            self.assertNotIn(raw, json.dumps(result))
        self.assertEqual(result["counts"], {"email": 1, "id_like": 1, "us_phone": 2})
        self.assertEqual(result["replacement_count"], 4)
        DocumentRedaction.model_validate(result)

    def test_ascii_identifier_substrings_and_financial_dates_preserved(self):
        text = "XDEMO123456Z xSAMPLE987654x REF109123456789 2026-10-04T08:00:00Z order demo-order-001 amount 100.00 USD"
        result = redact(text)
        self.assertEqual(result["redacted_text"], text)
        self.assertEqual(result["replacement_count"], 0)
        self.assertTrue(result["manual_review_required"])

    def test_exact_host_literals_repeat_and_manual_miss(self):
        literals = [{"type": "name", "text": "Synthetic José"}, {"type": "address", "text": "742 Café Lane"},
                    {"type": "manual", "text": "Ｆｕｌｌ－ｗｉｄｔｈ ｄｅｍｏ＠ｅｘａｍｐｌｅ.invalid"}]
        text = "Synthetic José lives at 742 Café Lane; Synthetic José uses Ｆｕｌｌ－ｗｉｄｔｈ ｄｅｍｏ＠ｅｘａｍｐｌｅ.invalid."
        result = redact(text, literals=literals)
        names = re.findall(r"\[NAME_[a-f0-9]{64}\]", result["redacted_text"])
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], names[1])
        for literal in literals:
            self.assertNotIn(literal["text"], json.dumps(result, ensure_ascii=False))
        self.assertEqual(result["counts"], {"address": 1, "manual": 1, "name": 2})

    def test_union_entire_email_id_and_literal_overlap(self):
        text = "prefix-DEMO123456@example.invalid-suffix"
        result = redact(text, literals=[{"type": "manual", "text": "prefix-DEMO123456"},
                                       {"type": "name", "text": "example.invalid-suffix"}])
        self.assertEqual(result["replacement_count"], 1)
        self.assertEqual(result["types"], ["mixed"])
        self.assertRegex(result["redacted_text"], r"^\[MIXED_[a-f0-9]{64}\]$")
        self.assertNotIn("prefix", result["redacted_text"])
        self.assertNotIn("suffix", result["redacted_text"])

    def test_chain_and_contained_overlaps_not_partial_replacements(self):
        result = redact("abcdefghij", literals=[{"type": "name", "text": "abcde"},
                                                {"type": "address", "text": "defgh"},
                                                {"type": "manual", "text": "hij"},
                                                {"type": "manual", "text": "bc"}])
        self.assertEqual(result["replacement_count"], 1)
        self.assertRegex(result["redacted_text"], r"^\[MIXED_[a-f0-9]{64}\]$")
        overlap = redact("AAAA", literals=[{"type": "manual", "text": "AAA"}])
        self.assertEqual(overlap["replacement_count"], 1)
        self.assertNotIn("AAAA", overlap["redacted_text"])

    def test_touching_intervals_distinct_and_input_order_irrelevant(self):
        literals = [{"type": "name", "text": "abc"}, {"type": "address", "text": "def"}]
        result = redact("abcdef", literals=literals)
        self.assertEqual(result["replacement_count"], 2)
        self.assertEqual(result, redact("abcdef", literals=list(reversed(literals))))

    def test_document_and_session_domain_separation_and_no_normalization(self):
        text = "demo@example.invalid demo@example.invalid"
        first = redact(text)
        self.assertEqual(first, redact(text))
        self.assertNotEqual(first["redacted_text"], redact(text, document_id="synthetic-document-002")["redacted_text"])
        self.assertNotEqual(first["redacted_text"], redact(text, key=bytes(range(1, 33)))["redacted_text"])
        self.assertNotEqual(first["redacted_text"], redact(text + " changed")["redacted_text"])
        literals = [{"type": "manual", "text": "ＡＢＣ"}]
        result = redact("ＡＢＣ ABC", literals=literals)
        self.assertTrue(result["redacted_text"].endswith(" ABC"))

    def test_full_width_risk_not_silently_certified(self):
        text = "ｄｅｍｏ＠ｅｘａｍｐｌｅ.invalid ＋１ ４１５ ５５５ ０１３２"
        result = redact(text)
        self.assertEqual(result["redacted_text"], text)
        self.assertTrue(result["limited_detection"])
        self.assertTrue(result["manual_review_required"])
        self.assertFalse(result["reversibility"])
        self.assertIn("Full-width", " ".join(result["limitations"]))

    def test_text_byte_and_span_limits(self):
        self.assertEqual(redact("x" * MAX_TEXT_BYTES)["replacement_count"], 0)
        self.assert_error("document_limit", lambda: redact("x" * (MAX_TEXT_BYTES + 1)))
        self.assert_error("document_limit", lambda: redact("★" * 6000))
        self.assert_error("document_span_limit", lambda: redact("demo@example.invalid " * 129))
        self.assertEqual(redact("demo@example.invalid " * 128)["replacement_count"], 128)

    def test_invalid_text_surrogate_and_controls_fixed_errors(self):
        for text in (None, 1, True, b"synthetic"):
            self.assert_error("document_invalid", lambda text=text: redact(text))
        self.assert_error("document_limit", lambda: redact("synthetic\ud800"))
        for text in ("synthetic\x00", "synthetic\u202e", "synthetic\u200b"):
            self.assert_error("document_invalid", lambda text=text: redact(text))
        self.assertEqual(redact("\n\t\r")["redacted_text"], "\n\t\r")

    def test_weak_key_and_bad_scope_fixed_errors(self):
        for key in (None, True, "key", b"a" * 31, b"a" * 32, bytes(range(256))):
            self.assert_error("document_key_invalid", lambda key=key: redact("synthetic", key=key))
        for scope in (None, True, "", "private/raw", "\ud800", "x" * 129):
            self.assert_error("document_scope_invalid", lambda scope=scope: redact("synthetic", document_id=scope))

    def test_literal_count_length_type_and_extra_fields(self):
        invalid = [True, {}, (), [None], [{"type": "name", "text": ""}], [{"type": "name", "text": " "}],
                   [{"type": "unknown", "text": "synthetic"}], [{"type": True, "text": "synthetic"}],
                   [{"type": "manual", "text": True}], [{"type": "name", "text": "x" * 501}],
                   [{"type": "name", "text": "synthetic", "url": "untrusted"}],
                   [{"type": "name", "text": "\ud800"}], [{"type": "manual", "text": "x"}] * 33]
        for literals in invalid:
            self.assert_error("document_literals_invalid", lambda literals=literals: redact("synthetic", literals=literals))

    def test_no_raw_state_mapping_logging_or_network(self):
        text = "Synthetic Demo Person demo@example.invalid"
        literals = [{"type": "name", "text": "Synthetic Demo Person"}]
        saved = deepcopy(literals)
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(logging.Logger, "_log", side_effect=AssertionError("log forbidden")), \
                patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
                patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")):
            result = redact(text, literals=literals)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(literals, saved)
        serialized = json.dumps(result)
        self.assertNotIn("Synthetic Demo Person", serialized)
        self.assertNotIn("demo@example.invalid", serialized)
        self.assertFalse(set(result) & {"mapping", "reverse_map", "spans", "key", "document_id", "raw_text", "raw_literals"})

    def test_strict_contract_false_booleans_counts_and_extras(self):
        result = redact("demo@example.invalid")
        for changes in ({"limited_detection": False}, {"limited_detection": 1}, {"manual_review_required": False},
                        {"manual_review_required": 1}, {"reversibility": True}, {"reversibility": 0},
                        {"source": "real"}, {"replacement_count": True}, {"counts": {"email": True}},
                        {"counts": {"unknown": 1}}, {"counts": {"email": 2}}, {"types": ["email", "email"]},
                        {"reverse_map": {}}, {"redacted_text": "\ud800"}):
            with self.assertRaises(ValidationError):
                DocumentRedaction.model_validate(dict(result, **changes))

    def test_existing_identity_tokens_contract_untouched(self):
        identity = {"name": "Synthetic Demo Person", "address": "Synthetic Demo Address", "email": "demo@example.invalid"}
        self.assertEqual(set(redact_identity(identity, KEY)), {"name_token", "address_token", "email_token"})
        self.assertEqual(redact_identity(identity, KEY), redact_identity(identity, KEY))


class DocumentApiTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 7, 8, tzinfo=timezone.utc)
        self.store = SessionStore(clock=lambda: self.now, rate_limit=200)
        self.created = self.store.create()
        self.session = self.store.sessions[self.created["session_id"]]
        self.app = create_app(store=self.store)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001))
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def post(self, path, body=None, session=None):
        selected = self.session if session is None else session
        return self.client.post("/api/v1" + path, json={} if body is None else body,
                                headers={"Origin": "http://localhost:5173", "X-Demo-Session": selected.session_id,
                                         "X-CSRF-Token": selected.csrf_token})

    def draft(self, session=None):
        self.assertEqual(self.post("/demo/inject", {"scenario": "dispute"}, session).status_code, 200)
        response = self.post("/disputes/case-ref-001/draft", session=session)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_real_consumer_strict_response_no_raw_pii_chronology_digest(self):
        draft = self.draft()
        DisputeDraftResponse.model_validate(draft)
        document = draft["document_redaction"]
        self.assertEqual(document["export_profile"], "INTERNAL_REVIEW_ONLY_V1")
        self.assertEqual(document["replacement_count"], 6)
        for raw in ("Synthetic Demo Person", "Synthetic Demo Address", "demo@example.invalid", "(415) 555-0132", "123-45-6789"):
            self.assertNotIn(raw, json.dumps(draft))
        case = self.session.disputes["demo-case-001"]
        self.assertNotIn(case["order_id"], document["redacted_text"])
        self.assertNotIn(case["case_id"], json.dumps(draft))
        self.assertNotIn(case["order_id"], json.dumps(draft))
        self.assertEqual(draft["case_ref"], "case-ref-001")
        state = self.client.get("/api/v1/demo/state", headers={
            "Origin": "http://localhost:5173", "X-Demo-Session": self.session.session_id,
        }).json()
        self.assertEqual(state["disputes"][0]["case_ref"], "case-ref-001")
        self.assertEqual(state["disputes"][0]["order_ref"], "order-ref-001")
        self.assertNotIn(case["case_id"], json.dumps(state["disputes"]))
        self.assertNotIn(case["order_id"], json.dumps(state["disputes"]))
        self.assertRegex(document["redacted_text"], r"Order \[MANUAL_[a-f0-9]{64}\]")
        for field in ("order_created_at", "delivered_at", "opened_at"):
            self.assertIn(case[field], document["redacted_text"])
        expected = payload_digest({"session_id": self.session.session_id, "draft": self.session.drafts["demo-case-001"],
                                   "restricted_sha256": self.session.restricted_evidence["demo-case-001"]["sha256"],
                                   "expires_at": self.session.draft_expires["demo-case-001"].isoformat().replace("+00:00", "Z")})
        self.assertEqual(draft["draft_digest"], expected)
        self.assertIn("does not establish fraud", document["redacted_text"])
        self.assertEqual(draft["routing"]["overall_state"], "READY_FOR_LOCAL_REVIEW")
        self.assertEqual(draft["routing"]["due_state"], "OPEN")
        self.assertEqual(draft["routing"]["requirements"][0]["requirement_state"], "STRUCTURALLY_PRESENT")
        self.assertEqual(draft["restricted_original_summary"]["custody"], "SESSION_MEMORY_ONLY")
        self.assertFalse(draft["restricted_original_summary"]["content_returned"])
        serialized = json.dumps(draft)
        for restricted_value in ("SYNTHETIC_TRACKING_001", "SYNTHETIC_CARRIER", "synthetic-delivery.pdf"):
            self.assertNotIn(restricted_value, serialized)

    def test_session_isolation_reset_and_single_review_still_bound(self):
        first = self.draft()
        other = self.store.sessions[self.store.create()["session_id"]]
        second = self.draft(other)
        self.assertNotEqual(first["document_redaction"]["redacted_text"], second["document_redaction"]["redacted_text"])
        self.assertNotEqual(first["draft_digest"], second["draft_digest"])
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]}, other).status_code, 422)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]}).status_code, 200)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]}).status_code, 422)
        self.assertEqual(self.post("/demo/inject", {"scenario": "reset"}).status_code, 200)
        self.assertEqual(self.session.restricted_evidence, {})
        third = self.draft()
        self.assertNotEqual(first["document_redaction"]["redacted_text"], third["document_redaction"]["redacted_text"])
        self.assertNotEqual(first["identity_redaction"]["tokens"], third["identity_redaction"]["tokens"])

    def test_document_change_invalidates_old_digest_and_expiry_preserved(self):
        first = self.draft()
        self.session.drafts["demo-case-001"]["document_redaction"]["redacted_text"] += " synthetic review annotation"
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]}).status_code, 422)
        updated = self.post("/disputes/case-ref-001/draft").json()
        self.assertNotEqual(first["draft_digest"], updated["draft_digest"])
        self.now += timedelta(seconds=300)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": updated["draft_digest"]}).status_code, 422)
        self.assertEqual(self.session.restricted_evidence, {})

    def test_restricted_layer_change_invalidates_bound_review_digest(self):
        first = self.draft()
        self.session.restricted_evidence["demo-case-001"]["sha256"] = "0" * 64
        response = self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "review_binding_rejected")

    def test_nested_restricted_payload_tamper_invalidates_review_digest(self):
        first = self.draft()
        restricted = self.session.restricted_evidence["demo-case-001"]
        restricted["proof_records"][0]["proof_fields"]["tracking_number"] = "TAMPERED"
        response = self.post("/disputes/case-ref-001/approve", {"draft_digest": first["draft_digest"]})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "review_binding_rejected")
        self.assertFalse(self.store.ai_brief_allowed(self.session, "dispute_mediation"))

    def test_resolver_failure_commits_neither_evidence_layer(self):
        self.store.inject(self.session, "dispute")
        before = deepcopy(self.session.activity)
        with patch("app.store.resolve_dispute_requirements",
                   side_effect=DisputeEvidenceError("proof_record_invalid")):
            response = self.post("/disputes/case-ref-001/draft")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "dispute_context_not_ready")
        self.assertEqual(self.session.drafts, {})
        self.assertEqual(self.session.restricted_evidence, {})
        self.assertEqual(self.session.draft_expires, {})
        self.assertEqual(self.session.activity, before)

    def test_partial_timeline_absent_none_empty_fails_before_draft(self):
        for missing in ("absent", None, ""):
            self.store.inject(self.session, "reset")
            self.store.inject(self.session, "dispute")
            case = self.session.disputes["demo-case-001"]
            for field in ("order_id", "order_created_at", "delivered_at", "opened_at"):
                if missing == "absent":
                    del case[field]
                else:
                    case[field] = missing
            before = deepcopy(self.session.activity)
            response = self.post("/disputes/case-ref-001/draft")
            self.assertEqual(response.status_code, 422, response.text)
            self.assertEqual(response.json()["error"]["code"], "dispute_context_not_ready")
            self.assertEqual(self.session.drafts, {})
            self.assertEqual(self.session.draft_expires, {})
            self.assertEqual(self.session.activity, before)

    def test_pipeline_failure_atomic_no_raw_http_error(self):
        self.store.inject(self.session, "dispute")
        self.session.token_key = b"synthetic-weak-key".ljust(32, b"x")[:32]
        self.session.token_key = b"a" * 32
        before = deepcopy(self.session.activity)
        response = self.post("/disputes/case-ref-001/draft")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "domain_invalid")
        self.assertEqual(self.session.activity, before)
        self.assertEqual(self.session.drafts, {})
        for raw in ("Synthetic Demo Person", "Synthetic Demo Address", "demo@example.invalid", "(415) 555-0132", "123-45-6789"):
            self.assertNotIn(raw, response.text)


if __name__ == "__main__":
    unittest.main()
