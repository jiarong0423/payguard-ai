"""(r35) Send-flow guards from the r34 cross review (E1 P1-1, P2-2; summary #2, #5, #6).

#2  A live dispute whose session detail read rules out an evidence send (seller evidence already listed, not waiting for
    the seller, no provide_evidence link) still previews, but with a send_guard refusal, no confirmation and no pair.
#5  A confirmation is bound to the approval record it followed: a re-draft and re-review end it even without Reset.
#6  A live dispute's read amount must equal the case amount at preview; the 409 message names both amounts.
Every provider reply is a synthetic MockTransport answer; sockets are patched to fail.
"""

from datetime import timedelta
import unittest
from unittest.mock import patch

from test_paypal_r24 import FIX, LiveHarness, submittable

REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001"}
SELLER_PROOF = {"evidence_type": "PROOF_OF_FULFILLMENT", "source": "SUBMITTED_BY_SELLER",
                "date": "2026-10-28T08:00:00.000Z"}


class R35Harness(LiveHarness):
    def bindings(self):
        return self.app.state.paypal_disputes._bindings.get(self.session["session_id"], {})

    def evidence(self, submit=False, token=None):
        payload = dict(REQUEST, submit=submit)
        if token is not None:
            payload["confirm_token"] = token
        return self._post("/paypal/disputes/provide-evidence", payload)


class NotReadyPreviewTests(R35Harness):
    CASES = (
        # PP-R-WAH as read in r34: waiting for the buyer, PayPal already lists the seller's proof.
        ("seller_evidence_already_submitted",
         dict(status="WAITING_FOR_BUYER_RESPONSE", evidences=FIX[0]["evidences"] + [SELLER_PROOF])),
        ("seller_evidence_already_submitted", dict(evidences=FIX[0]["evidences"] + [SELLER_PROOF])),
        ("dispute_not_awaiting_seller", dict(status="UNDER_REVIEW")),
        ("dispute_evidence_not_offered", None),
    )

    def detail_for(self, changes):
        if changes is None:  # waiting for the seller, but only the self link
            return dict(FIX[0], dispute_id="PP-D-SANDBOX01", links=FIX[0]["links"][:1])
        return submittable(**changes)

    def test_a_not_ready_dispute_previews_without_confirmation_or_pair_and_never_sends(self):
        for code, changes in self.CASES:
            with self.subTest(code=code, changes=sorted(changes or {})):
                self.setUp()
                self.detail = self.detail_for(changes)
                self.ready()
                preview = self.evidence()
                self.assertEqual(preview.status_code, 200, preview.text)
                body = preview.json()
                self.assertIsNone(body["confirm_token"])
                self.assertEqual(body["send_guard"]["send_refusal"], code)
                self.assertEqual(body["external_send"], "FROZEN")
                self.assertEqual(self.bindings(), {})
                with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
                    refused = self.evidence(submit=True, token="A" * 32)
                self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, code))
                self.assertIn("Nothing was sent", refused.json()["error"]["message"])
                self.assertEqual(self.posts("/provide-evidence"), [])
                self.assertEqual(self.bindings(), {})

    def test_a_ready_preview_then_a_not_ready_read_ends_the_confirmation(self):
        self.ready()
        first = self.evidence()
        self.assertEqual(first.status_code, 200, first.text)
        token = first.json()["confirm_token"]
        self.assertIsNotNone(token)
        self.assertIsNone(first.json()["send_guard"]["send_refusal"])
        self.assertIn("PP-D-SANDBOX01", self.bindings())
        # PayPal now lists the seller's proof; the console reads the detail again and previews again.
        self.detail = submittable(status="WAITING_FOR_BUYER_RESPONSE", evidences=FIX[0]["evidences"] + [SELLER_PROOF])
        self.assertEqual(self.get("/paypal/disputes/PP-D-SANDBOX01").status_code, 200)
        again = self.evidence()
        self.assertEqual(again.status_code, 200, again.text)
        self.assertIsNone(again.json()["confirm_token"])
        self.assertEqual(again.json()["send_guard"]["send_refusal"], "seller_evidence_already_submitted")
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            refused = self.evidence(submit=True, token=token)
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "seller_evidence_already_submitted"))
        self.assertEqual(refused.json()["error"]["message"],
                         "PayPal already has seller evidence for this dispute, so PayGuard will not send more. "
                         "Nothing was sent.")
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_a_ready_live_dispute_still_issues_a_confirmation_and_sends(self):
        self.ready()
        preview = self.evidence()
        self.assertEqual(preview.status_code, 200, preview.text)
        self.assertIsNotNone(preview.json()["confirm_token"])
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            sent = self.evidence(submit=True, token=preview.json()["confirm_token"])
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(sent.json()["external_send"], "SUBMITTED")
        self.assertEqual(len(self.posts("/provide-evidence")), 1)


class ConfirmationBoundToApprovalTests(R35Harness):
    def redraft_and_review(self):
        self.clock.now += timedelta(seconds=301)  # the 300 s draft lapses with its review; the gate is unchanged
        draft = self._post("/disputes/case-ref-001/draft")
        self.assertEqual(draft.status_code, 200, draft.text)
        approved = self._post("/disputes/case-ref-001/approve", {"draft_digest": draft.json()["draft_digest"]})
        self.assertEqual(approved.status_code, 200, approved.text)

    def test_a_confirmation_from_before_a_redraft_and_rereview_is_refused_without_reset(self):
        self.ready()
        gate = self.store.sessions[self.session["session_id"]].gate
        token = self.evidence().json()["confirm_token"]
        self.assertIsNotNone(token)
        self.redraft_and_review()
        self.assertIs(self.store.sessions[self.session["session_id"]].gate, gate)
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            refused = self.evidence(submit=True, token=token)
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "confirmation_invalid"))
        self.assertEqual(self.posts("/provide-evidence"), [])
        # A new preview after the new review sends.
        fresh = self.evidence().json()["confirm_token"]
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            sent = self.evidence(submit=True, token=fresh)
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(len(self.posts("/provide-evidence")), 1)

    def test_a_tracking_confirmation_from_before_a_rereview_is_refused(self):
        self.ready()
        preview = self._post("/paypal/disputes/add-tracking", dict(REQUEST, submit=False))
        self.assertEqual(preview.status_code, 200, preview.text)
        token = preview.json()["confirm_token"]
        self.assertIsNotNone(token)
        self.redraft_and_review()
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            refused = self._post("/paypal/disputes/add-tracking", dict(REQUEST, submit=True, confirm_token=token))
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "confirmation_invalid"))
        self.assertEqual(self.posts("/v1/shipping/trackers-batch"), [])


class LiveAmountTests(R35Harness):
    MESSAGE = ("The dispute amount in PayPal ({}) differs from the selected case's amount (48.00 USD). "
               "Select the case it belongs to. Nothing was sent.")

    def test_tracking_preview_refuses_a_live_dispute_in_another_amount(self):
        self.detail = submittable(dispute_amount={"currency_code": "TWD", "value": "158.00"})
        self.ready()
        for submit in (False, True):
            refused = self._post("/paypal/disputes/add-tracking", dict(REQUEST, submit=submit))
            self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "dispute_amount_mismatch"))
            self.assertEqual(refused.json()["error"]["message"], self.MESSAGE.format("158.00 TWD"))
        self.assertEqual(self.bindings(), {})
        self.assertEqual(self.posts("/v1/shipping/trackers-batch"), [])

    def test_the_fresh_read_amount_change_names_both_amounts(self):
        self.ready()
        token = self.evidence().json()["confirm_token"]
        self.detail = submittable(dispute_amount={"currency_code": "USD", "value": "49.00"})
        with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
            refused = self.evidence(submit=True, token=token)
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "dispute_amount_mismatch"))
        self.assertEqual(refused.json()["error"]["message"], self.MESSAGE.format("49.00 USD"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_an_off_pattern_amount_reads_unknown_in_the_message(self):
        from app.paypal_disputes import DisputeAmountMismatch
        error = DisputeAmountMismatch({"currency_code": "usd<script>", "value": "1"}, None)
        self.assertEqual(error.public_message, self.MESSAGE.replace("48.00 USD", "unknown").format("unknown"))


if __name__ == "__main__":
    unittest.main()
