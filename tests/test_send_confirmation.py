"""(r30 J2 P2-1) Server-side send confirmation for provide-evidence and add-tracking.

Before r30 the tick, the orange Continue, the 3-second hold and the green Send lived only in the browser, so a script
holding the session id and CSRF token could send with two API calls. Now each preview whose payload can be sent issues
a single-use confirmation; a send must carry the latest one, at least CONFIRM_HOLD_SECONDS after it was issued, for the
same dispute, case and payload. It is consumed under the store lock with the approval. These tests post without the
harness helper, so nothing adds the confirmation for them.
"""

from datetime import timedelta
from pathlib import Path
import unittest

from app.paypal_disputes import CONFIRM_HOLD_SECONDS
from test_paypal_r24 import LiveHarness

EVIDENCE = "/paypal/disputes/provide-evidence"
TRACKING = "/paypal/disputes/add-tracking"
REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001"}


class SendConfirmationTests(LiveHarness):
    def preview(self, route):
        response = self._post(route, dict(REQUEST, submit=False))
        self.assertEqual(response.status_code, 200, response.text)
        token = response.json()["confirm_token"]
        self.assertRegex(token, r"^[A-Za-z0-9_-]{32}$")
        return token

    def send(self, route, token):
        body = dict(REQUEST, submit=True) if token is None else dict(REQUEST, submit=True, confirm_token=token)
        return self._post(route, body)

    def wait(self, seconds=CONFIRM_HOLD_SECONDS):
        self.clock.now += timedelta(seconds=seconds)

    def code(self, response):
        return response.status_code, response.json()["error"]["code"]

    def test_hold_matches_the_dialog(self):
        source = (Path(__file__).resolve().parents[1] / "frontend/src/App.jsx").read_text(encoding="utf-8")
        self.assertIn(f"const SEND_HOLD_SECONDS = {CONFIRM_HOLD_SECONDS};", source)

    def test_a_send_without_the_confirmation_is_refused_before_any_provider_call(self):
        for route, suffix in ((EVIDENCE, "/provide-evidence"), (TRACKING, "/trackers-batch")):
            with self.subTest(route=route):
                self.ready() if route == EVIDENCE else None
                gets = len([row for row in self.calls if row.method == "GET"])
                refused = self.send(route, None)
                self.assertEqual(self.code(refused), (409, "confirmation_required"))
                self.assertIn("nothing was sent", refused.json()["error"]["message"].lower())
                self.assertEqual(self.posts(suffix), [])
                # Refused before the fresh read, so PayPal is not even asked.
                self.assertEqual(len([row for row in self.calls if row.method == "GET"]), gets)

    def test_a_send_straight_after_the_preview_is_refused_and_keeps_the_confirmation(self):
        self.ready()
        token = self.preview(EVIDENCE)
        self.wait(CONFIRM_HOLD_SECONDS - 1)
        self.assertEqual(self.code(self.send(EVIDENCE, token)), (409, "confirmation_too_early"))
        self.assertEqual(self.posts("/provide-evidence"), [])
        self.wait(1)
        sent = self.send(EVIDENCE, token)
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(sent.json()["external_send"], "SUBMITTED")
        self.assertIsNone(sent.json()["confirm_token"])
        self.assertEqual(len(self.posts("/provide-evidence")), 1)

    def test_a_newer_preview_replaces_the_confirmation(self):
        self.ready()
        older = self.preview(EVIDENCE)
        newer = self.preview(EVIDENCE)
        self.assertNotEqual(older, newer)
        self.wait()
        self.assertEqual(self.code(self.send(EVIDENCE, older)), (409, "confirmation_invalid"))
        self.assertEqual(self.send(EVIDENCE, newer).status_code, 200)

    def test_a_confirmation_works_once_and_only_for_its_own_action(self):
        self.ready()
        evidence = self.preview(EVIDENCE)
        tracking = self.preview(TRACKING)
        self.wait()
        # The evidence confirmation does not open the tracking send, nor the other way round.
        self.assertEqual(self.code(self.send(TRACKING, evidence)), (409, "confirmation_invalid"))
        self.assertEqual(self.code(self.send(EVIDENCE, tracking)), (409, "confirmation_invalid"))
        self.assertEqual(self.send(EVIDENCE, evidence).status_code, 200)
        self.assertEqual(self.send(TRACKING, tracking).status_code, 200)
        self.assertEqual(len(self.posts("/provide-evidence")), 1)
        self.assertEqual(len(self.posts("/trackers-batch")), 1)

    def test_a_used_confirmation_cannot_send_again_after_a_new_review(self):
        self.ready()
        token = self.preview(TRACKING)
        self.wait()
        self.assertEqual(self.send(TRACKING, token).status_code, 200)
        self.assertEqual(self.code(self.send(TRACKING, token)), (409, "tracking_already_submitted"))
        self.assertEqual(len(self.posts("/trackers-batch")), 1)

    def test_a_confirmation_from_another_session_is_refused(self):
        self.ready()
        token = self.preview(EVIDENCE)
        self.wait()
        other = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": "http://localhost:5173"}).json()
        self.session = other
        self.ready()
        self.assertEqual(self.code(self.send(EVIDENCE, token)), (409, "confirmation_invalid"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_reset_demo_ends_the_confirmation(self):
        # (r31 J2 J5) Reset replaces the review gate; a confirmation issued before it cannot send after a new review.
        self.ready()
        token = self.preview(EVIDENCE)
        self.assertEqual(self._post("/demo/inject", {"scenario": "reset"}).status_code, 200)
        self.ready()
        self.wait()
        self.assertEqual(self.code(self.send(EVIDENCE, token)), (409, "confirmation_invalid"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_a_new_review_gate_alone_ends_the_confirmation(self):
        # (r32 J5) Same payload, only the review gate replaced: the gate check by itself refuses the old confirmation.
        from app.store import LocalReviewGate
        self.ready()
        token = self.preview(EVIDENCE)
        session = self.store.sessions[self.session["session_id"]]
        session.gate = LocalReviewGate()
        self.wait()
        self.assertEqual(self.code(self.send(EVIDENCE, token)), (409, "confirmation_invalid"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_no_confirmation_while_the_send_could_not_go_out(self):
        # (r31 J2) Not reviewed yet: the preview issues none; once reviewed it does.
        self.ready(approve=False)
        preview = self._post(EVIDENCE, dict(REQUEST, submit=False))
        self.assertEqual(preview.status_code, 200, preview.text)
        self.assertIsNone(preview.json()["confirm_token"])
        draft = self._post("/disputes/case-ref-001/draft").json()
        self.assertEqual(self._post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}).status_code, 200)
        self.preview(EVIDENCE)

    def test_no_confirmation_while_the_send_switch_is_off(self):
        # The switch is read when the adapter connects, so it is set before ready().
        self.dispute_submit = False
        self.ready()
        preview = self._post(EVIDENCE, dict(REQUEST, submit=False))
        self.assertEqual(preview.status_code, 200, preview.text)
        self.assertIsNone(preview.json()["confirm_token"])

    def test_the_confirmation_check_comes_after_the_review_and_switch_checks(self):
        # (r31 J5) A send without a confirmation meets the same refusal its preview would: review first, then switch.
        self.dispute_submit = False
        self.ready(approve=False)
        self.assertEqual(self.code(self.send(EVIDENCE, None)), (422, "approval_required"))
        draft = self._post("/disputes/case-ref-001/draft").json()
        self.assertEqual(self._post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}).status_code, 200)
        self.assertEqual(self.code(self.send(EVIDENCE, None)), (503, "provider_action_frozen"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_expired_sessions_take_their_confirmations_with_them(self):
        self.ready()
        self.preview(EVIDENCE)
        service = self.app.state.paypal_disputes
        first = self.session["session_id"]
        self.assertIn(first, service._confirmations)
        self.clock.now += timedelta(seconds=self.store.ttl_seconds + 1)
        self.session = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": "http://localhost:5173"}).json()
        self.ready()
        self.preview(EVIDENCE)
        self.assertNotIn(first, service._confirmations)

    def test_a_malformed_confirmation_is_rejected_by_the_schema(self):
        self.ready()
        refused = self.send(EVIDENCE, "not-a-token")
        self.assertEqual(refused.status_code, 422)
        self.assertEqual(self.posts("/provide-evidence"), [])


if __name__ == "__main__":
    unittest.main()
