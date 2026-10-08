"""Offline applicability evidence boundaries, no eligibility assurance."""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import inspect
import subprocess
import sys
import unittest
from unittest.mock import patch

import payguard.applicability as applicability
from payguard.applicability import ApplicabilityError, assess_applicability
from payguard.retrieval import AUTHORITY, CHUNKS_SHA256, SOURCE_SHA256, RetrievalError, load_corpus


AS_OF = "2026-10-07T01:00:00+08:00"


class ApplicabilityTests(unittest.TestCase):
    def test_exact_region_coverage_does_not_fallback(self):
        result = assess_applicability("US", AS_OF, 30)
        self.assertEqual(result["coverage"]["regional_source_count"], 16)
        self.assertEqual(result["coverage"]["selected_source_count"], 16)
        self.assertEqual(result["coverage"]["selected_chunk_count"], 29)
        self.assertTrue(all(row["jurisdiction_normalized"] == "US" for row in result["sources"]))
        self.assertTrue(all(row["jurisdiction"] == "US" for row in result["chunks"]))
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["current_policy_applicability"], "NOT_ESTABLISHED")
        with patch.object(applicability, "load_corpus", side_effect=AssertionError("foreign request must fail before corpus load")) as loader:
            for region in ("CA", "GB", "GLOBAL"):
                with self.subTest(region=region), self.assertRaises(ApplicabilityError) as caught:
                    assess_applicability(region, AS_OF, 30)
                self.assertEqual(caught.exception.code, "applicability_filter_invalid")
            loader.assert_not_called()

    def test_all_effective_dates_unknown_separate_update_observation_decision(self):
        all_sources = assess_applicability("US", AS_OF, 30)["sources"]
        self.assertEqual(len(all_sources), 16)
        self.assertTrue(all(row["effective_date"] is None and row["effective_date_status"] == "NOT_VERIFIED" for row in all_sources))
        for row in all_sources:
            self.assertIn("UNKNOWN_EFFECTIVE_DATE", row["reason_codes"])
            for key in ("source_updated_date", "source_updated_date_status", "retrieved_at", "decision_date", "decision_date_status", "decision_acceptance_deadline"):
                self.assertIn(key, row)
        us_aup = next(row for row in all_sources if row["source_id"] == "PP-US-AUP")
        self.assertEqual(us_aup["source_updated_date"], "2022-10-29")
        self.assertTrue(us_aup["retrieved_at"].startswith("2026-10-06"))
        self.assertEqual(us_aup["observation_status"], "WITHIN_OBSERVATION_BUDGET")
        self.assertNotIn("STALE_OBSERVATION", us_aup["reason_codes"])

    def test_nonpolicy_sources_cannot_establish_applicability(self):
        expected = {"official_api_reference": "API_REFERENCE_NOT_POLICY", "official_api_schema": "API_REFERENCE_NOT_POLICY", "official_policy_guidance": "GUIDANCE_NOT_APPLICABLE_POLICY", "public_case_decision": "HISTORICAL_CASE_NOT_APPLICABLE_POLICY", "public_court_order_copy": "PROCEDURE_NOT_APPLICABLE_POLICY"}
        rows = assess_applicability("US", AS_OF, 30)["sources"]
        for row in rows:
            if row["material_type"] in expected:
                self.assertIn(expected[row["material_type"]], row["reason_codes"])
            self.assertEqual(row["current_policy_applicability"], "NOT_ESTABLISHED")
        us = assess_applicability("US", AS_OF, 30)
        self.assertEqual(us["coverage"]["official_policy_source_ids"], ["PP-US-AUP", "PP-US-PURCHASE-PROTECTION", "PP-US-SELLER-PROTECTION", "PP-US-UA"])
        procedures = [row for row in us["sources"] if row["material_type"] == "public_court_order_copy"]
        self.assertEqual({row["source_id"] for row in procedures}, {"US-COURT-ZEPEDA-2017-DOC357", "US-COURT-EVANS-2022-DOC37"})
        self.assertTrue(all("PROCEDURE_NOT_APPLICABLE_POLICY" in row["reason_codes"] for row in procedures))

    def test_theme_filters_are_exact_not_full_coverage_claims(self):
        for theme in ("source_compliance", "velocity_guard", "dispute_mediation"):
            result = assess_applicability("US", AS_OF, 30, theme=theme)
            self.assertTrue(result["chunks"])
            self.assertTrue(all(row["theme"] == theme for row in result["chunks"]))
            self.assertEqual(result["filters_applied"]["theme"], theme)
            self.assertFalse(result["coverage"]["complete"])
        regional = assess_applicability("US", AS_OF, 30)
        self.assertIsNone(regional["filters_applied"]["theme"])
        self.assertEqual(regional["coverage"]["missing_official_policy_themes"], [])

    def test_timezones_normalize_without_losing_microseconds(self):
        left = assess_applicability("US", "2026-10-06T09:00:00.123456Z", 1)
        right = assess_applicability("US", "2026-10-06T17:00:00.123456+08:00", 1)
        self.assertEqual(left, right)
        self.assertEqual(left["filters_applied"]["as_of"], "2026-10-06T09:00:00.123456+00:00")

    def test_observation_budget_exact_elapsed_boundary(self):
        source_time = datetime.fromisoformat(load_corpus()._sources["PP-US-AUP"]["retrieved_at"])
        exact = assess_applicability("US", source_time + timedelta(days=1), 1)
        later = assess_applicability("US", source_time + timedelta(days=1, microseconds=1), 1)
        at_observation = assess_applicability("US", source_time, 0)
        pick = lambda result: next(row for row in result["sources"] if row["source_id"] == "PP-US-AUP")
        self.assertEqual(pick(exact)["observation_status"], "WITHIN_OBSERVATION_BUDGET")
        self.assertEqual(pick(later)["observation_status"], "STALE_OBSERVATION")
        self.assertEqual(pick(at_observation)["observation_status"], "WITHIN_OBSERVATION_BUDGET")

    def test_future_and_stale_observation_keep_unknown_effective_reason(self):
        future = assess_applicability("US", "2026-10-03T00:00:00Z", 30)
        stale = assess_applicability("US", "2026-11-07T00:00:00Z", 1)
        for result, reason in ((future, "FUTURE_OBSERVATION"), (stale, "STALE_OBSERVATION")):
            self.assertIn(reason, result["reason_codes"])
            self.assertIn("UNKNOWN_EFFECTIVE_DATE", result["reason_codes"])
            self.assertEqual(result["status"], "INCOMPLETE_POLICY_EVIDENCE")
            self.assertTrue(all(reason in row["reason_codes"] for row in result["sources"]))

    def test_document_future_date_is_not_silent_effective_date(self):
        result = assess_applicability("US", "2026-07-01T00:00:00Z", 30)
        self.assertIn("DOCUMENT_UPDATE_IN_FUTURE", result["reason_codes"])
        self.assertIn("FUTURE_OBSERVATION", result["reason_codes"])
        self.assertIn("UNKNOWN_EFFECTIVE_DATE", result["reason_codes"])

    def test_invalid_region_theme_budget_time_before_loader(self):
        invalid = [("CA", AS_OF, 1, None), ("GB", AS_OF, 1, None), ("MX", AS_OF, 1, None), ("GLOBAL", AS_OF, 1, None), (True, AS_OF, 1, None), ("us", AS_OF, 1, None), ("US", AS_OF, -1, None), ("US", AS_OF, True, None), ("US", AS_OF, "1", None), ("US", AS_OF, 1.0, None), ("US", AS_OF, 365001, None), ("US", AS_OF, 1, "unknown"), ("US", AS_OF, 1, []), ("US", "2026-10-05T00:00:00", 1, None), ("US", "2026-02-30T00:00:00Z", 1, None), ("US", datetime(2026, 10, 5), 1, None), ("US", "private_marker" * 100, 1, None), ("US", None, 1, None)]
        with patch.object(applicability, "load_corpus", side_effect=AssertionError("must not load")) as loader:
            for region, instant, budget, theme in invalid:
                with self.subTest(region=region, budget=budget, theme=theme):
                    with self.assertRaises(ApplicabilityError) as caught:
                        assess_applicability(region, instant, budget, theme=theme)
                    self.assertEqual(caught.exception.code, "applicability_filter_invalid")
                    self.assertNotIn("private_marker", str(caught.exception))
            loader.assert_not_called()

    def test_each_call_loads_fixed_corpus_and_drift_does_not_fallback(self):
        with patch.object(applicability, "load_corpus", wraps=load_corpus) as loader:
            assess_applicability("US", AS_OF, 30)
            assess_applicability("US", AS_OF, 30)
            self.assertEqual(loader.call_count, 2)
        with patch.object(applicability, "load_corpus", side_effect=RetrievalError("corpus_digest_mismatch")):
            with self.assertRaises(ApplicabilityError) as caught:
                assess_applicability("US", AS_OF, 30)
            self.assertEqual(str(caught.exception), "applicability_corpus_unavailable")

    def test_safe_loader_failures_do_not_retain_path_or_input(self):
        for error in (OSError("/private/secret"), ValueError("private_marker"), RuntimeError("provider URL")):
            with self.subTest(error=type(error).__name__), patch.object(applicability, "load_corpus", side_effect=error):
                with self.assertRaises(ApplicabilityError) as caught:
                    assess_applicability("US", AS_OF, 30)
                self.assertEqual(str(caught.exception), "applicability_corpus_unavailable")
                self.assertTrue(caught.exception.__suppress_context__)

    def test_private_snapshot_type_pins_and_bounds_fail_closed(self):
        fake = deepcopy(load_corpus())
        fake._digests["sources_sha256"] = "0" * 64
        short = deepcopy(load_corpus())
        short._chunks.pop()
        for value in (object(), fake, short):
            with self.subTest(value=type(value).__name__), patch.object(applicability, "load_corpus", return_value=value):
                with self.assertRaises(ApplicabilityError) as caught:
                    assess_applicability("US", AS_OF, 30)
                self.assertEqual(caught.exception.code, "applicability_corpus_unavailable")

    def test_snapshot_is_nested_immutable_and_detached(self):
        corpus = load_corpus()
        original = deepcopy((corpus._sources, corpus._chunks, corpus._regions))
        with patch.object(applicability, "load_corpus", return_value=corpus):
            snapshot = applicability._load_snapshot()
            with self.assertRaises(TypeError):
                snapshot.sources["PP-US-AUP"]["effective_date"] = "2026-01-01"
            with self.assertRaises(TypeError):
                snapshot.regions["PP-US-AUP"] = "UK"
            with self.assertRaises(TypeError):
                snapshot.chunks[next(iter(snapshot.chunks))]["theme"] = "unknown"
            self.assertEqual(original, (corpus._sources, corpus._chunks, corpus._regions))

    def test_response_detached_pins_authority_and_no_original_text(self):
        first = assess_applicability("US", AS_OF, 30)
        original = deepcopy(first)
        first["sources"][0]["effective_date"] = "2026-01-01"
        first["sources"].clear()
        self.assertEqual(assess_applicability("US", AS_OF, 30), original)
        self.assertEqual(original["corpus_digests"], {"sources_sha256": SOURCE_SHA256, "chunks_sha256": CHUNKS_SHA256})
        self.assertTrue(original["advisory_only"])
        self.assertTrue(original["requires_human_review"])
        self.assertEqual(original["operational_authority"], AUTHORITY)
        self.assertTrue(all("text" not in row for row in original["chunks"]))
        self.assertTrue(all("eligible" not in row for row in original["sources"]))

    def test_public_api_has_no_caller_corpus_authority_paths(self):
        self.assertEqual(list(inspect.signature(assess_applicability).parameters), ["jurisdiction", "as_of", "observation_max_age_days", "theme"])
        for extra in ("corpus", "metadata", "loader", "path", "expected_source_sha256"):
            with self.subTest(extra=extra), self.assertRaises(TypeError):
                assess_applicability("US", AS_OF, 30, **{extra: "private_marker"})

    def test_import_reload_has_no_corpus_io(self):
        code = "from unittest.mock import patch\nwith patch('payguard.retrieval.load_corpus', side_effect=AssertionError('import must not load')) as loader:\n    import payguard.applicability\n    loader.assert_not_called()\n"
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
