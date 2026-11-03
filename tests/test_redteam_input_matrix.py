"""Regression for the input-guard attack matrix (tools/redteam_input_matrix.py): every attack round must stay clean.

Round R1 on 2026-11-02 found a 500 on a non-ASCII case_ref (hmac.compare_digest raises on non-ASCII str) and UTF-16
request bodies accepted past the UTF-8 boundary; both are pinned here as well as through the full matrix.
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from app.store import safe_equal

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("redteam_input_matrix", ROOT / "tools" / "redteam_input_matrix.py")
matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix)


class SafeEqual(unittest.TestCase):
    def test_non_ascii_and_non_strings_compare_unequal_instead_of_raising(self):
        self.assertFalse(safe_equal("case-ref-١٢٣", "case-ref-001"))
        self.assertFalse(safe_equal("é" * 4, "abcd"))
        self.assertFalse(safe_equal(None, "abc"))
        self.assertFalse(safe_equal(b"abc", "abc"))
        self.assertTrue(safe_equal("case-ref-001", "case-ref-001"))


class AttackMatrix(unittest.TestCase):
    def test_pinned_attacks(self):
        harness = matrix.Harness(rate_limit=10 ** 9)
        harness.fixtures()
        response, _ = harness.send("POST", matrix.ROOT + "/disputes/case-ref-١٢٣/draft", {})
        self.assertEqual(response.status_code, 404)
        response, _ = harness.send("POST", matrix.ROOT + "/cases/route", raw=json.dumps({"text": "mug"}).encode("utf-16"))
        self.assertEqual((response.status_code, response.json()["error"]["code"]), (422, "invalid_json"))

    def test_every_round_is_clean(self):
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(matrix.run(Path(out), "regression"), 0, (Path(out) / "matrix_regression.md").read_text())


class RoundTwoRedTeam(unittest.TestCase):
    """Red-team round 2 (2026-11-02, redteam/REDTEAM_CODE_REPORT.md): each finding pinned after its fix."""

    def setUp(self):
        self.harness = matrix.Harness(rate_limit=10 ** 9)

    def test_out_of_range_offset_dates_are_422_not_500(self):
        for as_of in ("9999-12-31T23:59:59-23:59", "0001-01-01T00:00:00+23:59"):
            for path, extra in (("/policy/assess", {}), ("/advisory/evaluate", {"candidate_json": "{}"})):
                body = {"jurisdiction": "US", "theme": "dispute_mediation", "as_of": as_of, "observation_max_age_days": 30, **extra}
                response, _ = self.harness.send("POST", matrix.ROOT + path, body)
                self.assertEqual(response.status_code, 422, (path, as_of, response.text[:120]))

    def test_studio_result_with_a_non_string_call_id_is_refused(self):
        from app.studio_agent import StudioAgentError, validate_turn
        for call_id in (["x"], {"a": 1}, 7, None):
            body = {"instructions": "x", "tools": [], "tool_choice": "auto", "response_format": {"type": "text"},
                    "items": [{"kind": "user", "text": "What is on the board?"}, {"kind": "result", "call_id": call_id, "output": "x"}]}
            with self.assertRaises(StudioAgentError):
                validate_turn(body)

    def test_a_full_store_admits_a_new_visitor_by_dropping_an_idle_session(self):
        from datetime import datetime, timedelta, timezone
        from app.store import BoundaryError, SessionStore
        now = [datetime(2026, 11, 2, tzinfo=timezone.utc)]
        store = SessionStore(clock=lambda: now[0], max_sessions=3, rate_limit=1000)
        hoarded = [store.create()["session_id"] for _ in range(3)]
        active = store.create  # the store is full; nobody has been idle long enough yet
        with self.assertRaises(BoundaryError):
            active()
        now[0] += timedelta(seconds=61)
        store.require(hoarded[2])  # one session is in use and must survive
        visitor = store.create()["session_id"]
        self.assertIn(visitor, store.sessions)
        self.assertIn(hoarded[2], store.sessions)
        self.assertEqual(len(store.sessions), 3)

    def test_policy_check_sees_through_wording_tricks_without_flagging_tools(self):
        from payguard.engines import check_aup
        for text in ("c0unterfeit rolex", "counter-feit rolex", "c o u n t e r f e i t rolex", "replica rolex", "knockoff rolex",
                     "fake rolex", "g u n", "9mm pistol", "\u0261un"):
            self.assertEqual(check_aup(text)["match_status"], "REVIEW_SIGNAL", text)
        for text in ("glue gun for crafts", "nail-gun", "massage gun", "fake plant for decor", "a b c toy blocks",
                     "wireless headphones", "top 10 tips ebook"):
            self.assertEqual(check_aup(text)["match_status"], "NO_MATCH", text)

    def test_tracking_number_needs_plain_ascii_and_a_full_match(self):
        import datetime
        from payguard import evidence_guide as eg
        today = datetime.date(2026, 11, 2)
        for value in ("\u00df" * 8, "\ufb00" * 5, "ABCD1234EF\n", "\u0661" * 10):
            self.assertFalse(eg.validate_fixed_input("dispute", "tracking_number", value, today), repr(value))
        self.assertTrue(eg.validate_fixed_input("dispute", "tracking_number", "1Z999AA10123456784", today))

    def test_a_lapsed_review_is_logged(self):
        from datetime import datetime, timedelta, timezone
        from app.store import SessionStore
        now = [datetime(2026, 11, 2, tzinfo=timezone.utc)]
        store = SessionStore(clock=lambda: now[0], rate_limit=1000)
        session = store.sessions[store.create()["session_id"]]
        store.inject(session, "dispute")
        draft = store.draft(session, "case-ref-001")
        store.approve(session, "case-ref-001", draft["draft_digest"])
        now[0] += timedelta(seconds=301)
        store.state(session)
        self.assertTrue(any("lapsed" in entry["label"] for entry in session.activity))


if __name__ == "__main__":
    unittest.main()
