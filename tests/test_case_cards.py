"""Synthetic US scenario-card acceptance; no real-case or merits claims."""

from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import payguard.case_cards as cards
from payguard.case_contract import get_contract
from payguard.retrieval import load_corpus
from test_case_intake import ORIGINS, activity, dispute, envelope, velocity


def match(data):
    return cards.match_cases(json.dumps(data))


class CaseCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = load_corpus()
        cls.document = cards.load_case_cards()

    def assert_invalid(self, change):
        data = deepcopy(self.document)
        change(data)
        with self.assertRaises(cards.CaseCardsError):
            cards._validate_catalog(data, self.corpus)

    def test_three_exact_authored_scenarios_cover_each_theme_once(self):
        self.assertEqual(self.document["catalog_id"], "payguard.us_demo_scenarios.v1")
        self.assertEqual(self.document["provenance"], "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES")
        self.assertEqual(self.document["jurisdiction"], "US")
        self.assertEqual(self.document["scenario_count"], 3)
        rows = self.document["scenarios"]
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["theme"] for row in rows}, {"source_compliance", "velocity_guard", "dispute_mediation"})
        self.assertEqual({row["scenario_id"] for row in rows}, {
            "US-DEMO-AUP-WARNING", "US-DEMO-VELOCITY-READINESS", "US-DEMO-DISPUTE-EVIDENCE",
        })
        self.assertTrue(all(row["evidence_class"] == "SYNTHETIC_DEMO_SCENARIO" for row in rows))
        self.assertIn("never be presented as real cases", self.document["case_evidence_gap"])

    def test_fixed_file_and_raw_hash(self):
        path = Path(cards.__file__).absolute().parents[2] / "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), cards.SCENARIOS_SHA256)

    def test_module_root_alias_loads_exact_pinned_catalog(self):
        project_root = Path(cards.__file__).absolute().parents[2]
        with tempfile.TemporaryDirectory(prefix="payguard-case-card-alias-") as temporary:
            alias = Path(temporary) / "project-alias"
            alias.symlink_to(project_root, target_is_directory=True)
            module_path = alias / "src/payguard/case_cards.py"
            self.assertNotEqual(module_path.absolute(), module_path.resolve(strict=True))
            with patch.object(cards, "__file__", str(module_path)):
                document = cards.load_case_cards()
            self.assertEqual(document["catalog_id"], cards.CATALOG_ID)
            self.assertEqual(document["scenario_count"], 3)

    def test_case_card_descendant_hash_type_missing_and_symlink_fail_closed(self):
        canonical = Path(cards.__file__).absolute().parents[2] / "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json"
        original = canonical.read_bytes()
        for mode, expected in (
            ("hash", "case_cards_invalid"),
            ("missing", "case_cards_unavailable"),
            ("type", "case_cards_unavailable"),
            ("final_symlink", "case_cards_unavailable"),
            ("intermediate_symlink", "case_cards_unavailable"),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix="payguard-case-card-boundary-") as temporary:
                root = Path(temporary)
                module_path = root / "src/payguard/case_cards.py"
                module_path.parent.mkdir(parents=True)
                module_path.write_text("# test module identity\n", encoding="utf-8")
                target = root / "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json"
                if mode == "intermediate_symlink":
                    actual = root / "actual-corpus"
                    actual.mkdir()
                    (actual / "scenario_cards.v1.json").write_bytes(original)
                    target.parent.parent.mkdir(parents=True)
                    target.parent.symlink_to(actual, target_is_directory=True)
                else:
                    target.parent.mkdir(parents=True)
                    if mode == "hash":
                        target.write_bytes(original + b" ")
                    elif mode == "type":
                        target.mkdir()
                    elif mode == "final_symlink":
                        outside = root / "outside.json"
                        outside.write_bytes(original)
                        target.symlink_to(outside)
                with patch.object(cards, "__file__", str(module_path)), self.assertRaises(cards.CaseCardsError) as error:
                    cards.load_case_cards()
                self.assertEqual(error.exception.code, expected)
        with self.assertRaises(TypeError):
            cards.load_case_cards(Path(cards.__file__).absolute().parents[2])

    def test_scenario_citations_are_official_references_never_court_records(self):
        chunks = {row["chunk_id"]: row for row in self.corpus._chunks}
        for scenario in self.document["scenarios"]:
            for chunk_id in scenario["citation_chunk_ids"]:
                chunk = chunks[chunk_id]
                source = self.corpus._sources[chunk["source_id"]]
                self.assertEqual(chunk["_theme"], scenario["theme"])
                self.assertIn(source["material_type"], {"official_api_reference", "official_policy"})
                self.assertNotEqual(source["material_type"], "public_court_order_copy")
                self.assertEqual(self.corpus._regions[chunk["source_id"]], "US")

    def test_both_court_records_are_procedural_never_final_merits(self):
        expected = {
            "US-COURT-ZEPEDA-2017-DOC357": "SETTLEMENT_APPROVAL_NOT_FINAL_MERITS",
            "US-COURT-EVANS-2022-DOC37": "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED",
        }
        rows = [row for row in self.corpus._chunks if row["source_id"] in expected]
        self.assertEqual({row["source_id"] for row in rows}, set(expected))
        for row in rows:
            self.assertEqual(row["_stage"], "procedural_order")
            self.assertEqual(row["case_outcome"], expected[row["source_id"]])
        scenario_citations = {chunk_id for scenario in self.document["scenarios"] for chunk_id in scenario["citation_chunk_ids"]}
        self.assertTrue(all(row["chunk_id"] not in scenario_citations for row in rows))

    def test_top_schema_identity_provenance_and_count_rejected(self):
        changes = [
            lambda d: d.update(extra=True),
            lambda d: d.update(schema_version=True),
            lambda d: d.update(catalog_id="other"),
            lambda d: d.update(provenance="REAL_CASES"),
            lambda d: d.update(jurisdiction="CA"),
            lambda d: d.update(scenario_count=True),
            lambda d: d["scenarios"].pop(),
            lambda d: d["scenarios"].__setitem__(1, deepcopy(d["scenarios"][0])),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assert_invalid(change)

    def test_scenario_fields_and_safe_text_rejected(self):
        changes = [
            lambda d: d["scenarios"][0].update(extra=True),
            lambda d: d["scenarios"][0].update(scenario_id="CASE-001"),
            lambda d: d["scenarios"][0].update(theme="velocity_guard"),
            lambda d: d["scenarios"][0].update(title="bad\u200btext"),
            lambda d: d["scenarios"][0].update(evidence_class="PUBLIC_CASE_DECISION"),
            lambda d: d["scenarios"][0].update(expected_route="AUTOMATIC_SUBMISSION"),
            lambda d: d["scenarios"][0].update(final_authority="PAYGUARD"),
            lambda d: d["scenarios"][0].update(citation_chunk_ids=[]),
            lambda d: d["scenarios"][0]["citation_chunk_ids"].append(d["scenarios"][0]["citation_chunk_ids"][0]),
            lambda d: d["scenarios"][0].update(limitations=[]),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assert_invalid(change)

    def test_unknown_cross_theme_and_court_citations_rejected(self):
        for chunk_id in ("MADE-UP", "PP-US-UA-VELOCITY", "US-COURT-EVANS-2022-DOC37-ORDER"):
            with self.subTest(chunk_id=chunk_id):
                self.assert_invalid(lambda d, chunk_id=chunk_id: d["scenarios"][0].update(citation_chunk_ids=[chunk_id]))

    def test_loader_digest_duplicate_nonfinite_oversize_and_missing_safe(self):
        from payguard import retrieval

        raw_values = (b"{}", b"{" * 300000, b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff")
        for raw in raw_values:
            with self.subTest(raw=raw[:20]), patch.object(retrieval, "_read_fixed", return_value=raw):
                with self.assertRaises(cards.CaseCardsError) as error:
                    cards.load_case_cards()
                self.assertNotIn("/", str(error.exception))
        with patch.object(retrieval, "_read_fixed", side_effect=ValueError("PRIVATE_PATH")):
            with self.assertRaises(cards.CaseCardsError) as error:
                cards.load_case_cards()
        self.assertEqual(str(error.exception), "case_cards_unavailable")

    def test_catalog_returns_defensive_copies_and_import_no_io(self):
        data = cards.load_case_cards()
        data["scenarios"][0]["evidence_class"] = "FORGED"
        self.assertEqual(cards.load_case_cards()["scenarios"][0]["evidence_class"], "SYNTHETIC_DEMO_SCENARIO")
        with patch("builtins.open", side_effect=AssertionError("no import I/O")):
            importlib.reload(cards)

    def test_blocked_intake_never_loads_catalog(self):
        invalid = activity()
        invalid["payload"]["x"] = "private"
        missing = activity()
        del missing["payload"]["activity_description"]
        conflict = activity()
        conflict["requested_theme"] = ["source_compliance", "velocity_guard"]
        foreign = activity()
        foreign["jurisdiction"] = "CA"
        for data in (invalid, missing, conflict, foreign):
            with patch.object(cards, "_load", side_effect=AssertionError("must not load")):
                result = match(data)
            self.assertEqual(result["status"], "intake_blocked")
            self.assertEqual(result["matches"], [])

    def test_each_valid_theme_returns_one_synthetic_scenario_only(self):
        expected = {
            "source_compliance": "US-DEMO-AUP-WARNING",
            "velocity_guard": "US-DEMO-VELOCITY-READINESS",
            "dispute_mediation": "US-DEMO-DISPUTE-EVIDENCE",
        }
        for data in (activity(), velocity(), dispute()):
            result = match(data)
            self.assertEqual(result["status"], "synthetic_scenarios_found")
            self.assertEqual([row["scenario_id"] for row in result["matches"]], [expected[data["requested_theme"]]])
            self.assertEqual(result["provenance"], cards.PROVENANCE)
            self.assertEqual(result["real_case_evidence"], "NOT_PROVIDED")
            self.assertTrue(all(row["evidence_class"] == "SYNTHETIC_DEMO_SCENARIO" for row in result["matches"]))

    def test_manual_dispute_still_returns_synthetic_scenario_without_outcome_prediction(self):
        contract = get_contract()["routes"]["prepare_dispute_draft"]["reason_matrix"]
        authority = "PP-DISPUTES-OVERVIEW-AUTHORITY"
        expected = {
            "MERCHANDISE_OR_SERVICE_NOT_RECEIVED": [
                authority, "PP-US-PURCHASE-INR-SNAD", "PP-US-SELLER-ELIGIBILITY",
                "PP-US-SELLER-DELIVERY", "PP-REASONS-INR",
            ],
            "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED": [
                authority, "PP-US-PURCHASE-INR-SNAD", "PP-US-PURCHASE-COUNTERFEIT",
                "PP-US-SELLER-ELIGIBILITY", "PP-REASONS-SNAD",
            ],
            "UNAUTHORISED": [
                authority, "PP-US-SELLER-ELIGIBILITY", "PP-US-SELLER-DELIVERY",
                "PP-REASONS-UNAUTH",
            ],
            "CREDIT_NOT_PROCESSED": [authority, "PP-REASONS-CREDIT"],
            "DUPLICATE_TRANSACTION": [authority, "PP-REASONS-DUPLICATE"],
            "INCORRECT_AMOUNT": [authority, "PP-REASONS-AMOUNT"],
            "PAYMENT_BY_OTHER_MEANS": [authority, "PP-REASONS-OTHER-PAYMENT"],
            "CANCELED_RECURRING_BILLING": [authority, "PP-REASONS-SUBSCRIPTION"],
            "OTHER": [authority, "PP-REASONS-OTHER"],
        }
        chunks = {row["chunk_id"]: row for row in self.corpus._chunks}
        for reason in contract:
            with self.subTest(reason=reason):
                result = match(dispute(reason))
                expected_intake = (
                    "ready_for_local_rules"
                    if reason == "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
                    else "manual_review"
                )
                self.assertEqual(result["intake"]["status"], expected_intake)
                self.assertEqual(result["status"], "synthetic_scenarios_found")
                self.assertEqual(len(result["matches"]), 1)
                self.assertIn("No outcome prediction", result["matches"][0]["limitations"])
                citations = [row["chunk_id"] for row in result["matches"][0]["citations"]]
                self.assertEqual(citations, expected[reason])
                other_reason_citations = {
                    row["reference_chunk_id"] for key, row in contract.items() if key != reason
                }
                self.assertFalse(set(citations) & other_reason_citations)
                for chunk_id in citations:
                    if chunk_id != authority:
                        self.assertIn(reason, chunks[chunk_id]["reason_codes"])
        alias = [row["chunk_id"] for row in match(dispute("INR"))["matches"][0]["citations"]]
        self.assertEqual(alias, expected["MERCHANDISE_OR_SERVICE_NOT_RECEIVED"])

    def test_unsupported_reason_values_fail_before_catalog_load(self):
        for value in ("SNAD", "UNKNOWN", "MADE_UP", "", None, True):
            data = dispute()
            data["payload"]["reason_code"] = value
            with self.subTest(value=value), patch.object(cards, "_load", side_effect=AssertionError("must not load")):
                result = match(data)
            self.assertEqual(result["status"], "intake_blocked")
            self.assertEqual(result["matches"], [])

    def test_dispute_catalog_requires_every_reason_owned_common_chunk(self):
        for chunk_id in ("PP-US-PURCHASE-COUNTERFEIT", "PP-US-SELLER-ELIGIBILITY"):
            def remove(document, selected=chunk_id):
                scenario = next(row for row in document["scenarios"] if row["theme"] == "dispute_mediation")
                scenario["citation_chunk_ids"].remove(selected)
            with self.subTest(chunk_id=chunk_id):
                self.assert_invalid(remove)

    def test_explicit_reference_must_intersect_scenario_citations(self):
        data = activity()
        data["references"] = [deepcopy(ORIGINS["source_compliance"])]
        self.assertEqual(match(data)["status"], "synthetic_scenarios_found")
        data["references"] = [{"source_id": "US-COURT-EVANS-2022-DOC37", "chunk_id": "US-COURT-EVANS-2022-DOC37-ORDER"}]
        self.assertEqual(match(data)["status"], "evidence_missing")
        self.assertEqual(match(data)["matches"], [])

        data = dispute("CREDIT_NOT_PROCESSED")
        data["references"] = [
            {"source_id": "PP-DISPUTE-REASONS-EVIDENCE", "chunk_id": "PP-REASONS-CREDIT"},
            {"source_id": "PP-DISPUTE-REASONS-EVIDENCE", "chunk_id": "PP-REASONS-INR"},
        ]
        self.assertEqual(match(data)["status"], "evidence_missing")
        self.assertEqual(match(data)["matches"], [])

    def test_lexical_reference_lookup_uses_official_citations(self):
        data = envelope("source_compliance", "reference_lookup")
        data["payload"] = {"query": "AUP prior approval"}
        self.assertEqual(match(data)["status"], "synthetic_scenarios_found")
        data["payload"]["query"] = "zxqv12345totallyabsent"
        self.assertEqual(match(data)["status"], "evidence_missing")

    def test_result_excludes_case_proof_gold_and_source_text(self):
        forbidden = {
            "case_id", "case_stage", "case_outcome", "expected_answer", "facts", "solutions",
            "required_fact_ids", "adjudicator_finding", "source_text", "confidence",
        }

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertNotIn(key, forbidden)
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        for data in (activity(), velocity(), dispute(), dispute("MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED")):
            result = match(data)
            walk(result)
            self.assertEqual(result["semantic_confidence"], "NOT_EVALUATED")
            self.assertEqual(result["current_policy_applicability"], "NOT_ESTABLISHED")
            self.assertEqual(result["evaluation_scope"], "AUTHORED_SYNTHETIC_DEMO_ONLY")

    def test_match_unavailable_is_sanitized_and_engines_never_run(self):
        with patch.object(cards, "_load", side_effect=ValueError("PRIVATE_PATH")):
            result = match(activity())
        self.assertEqual(result["status"], "reference_unavailable")
        self.assertNotIn("PRIVATE_PATH", json.dumps(result))
        with patch("payguard.engines.prepare_dispute", side_effect=AssertionError("forbidden")), \
             patch("payguard.engines.assess_velocity", side_effect=AssertionError("forbidden")), \
             patch("payguard.engines.check_aup", side_effect=AssertionError("forbidden")):
            for data in (activity(), velocity(), dispute()):
                self.assertEqual(match(data)["status"], "synthetic_scenarios_found")


if __name__ == "__main__":
    unittest.main()
