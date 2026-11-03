"""PayPal API correctness checks from the r24 docs review (PayPal docs r24).

Every provider reply is a synthetic MockTransport answer; no test contacts the network or needs a credential.
Covered: fresh-GET gates before provide-evidence, carrier enum mapping, empty PROOF_OF_FULFILLMENT, file type and
size limits, PayPal-Request-Id length, PayPal-Debug-Id capture, the gated add-tracking action and zero-decimal
invoice amounts.
"""

from datetime import datetime, timezone
import json
import os
import socket
import unittest
from unittest import mock
from unittest.mock import patch

from fastapi.testclient import TestClient
import httpx
from pydantic import ValidationError

from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig, SANDBOX_BASE, allowed_request
from app.paypal_disputes import build_provide_evidence_request, fixture_disputes, map_carrier
from app.schemas import InvoicePayload
from app.store import BoundaryError, SessionStore


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
DEBUG_ID = "f00dbabe12345"


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 29, 8, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


FIX = fixture_disputes(Clock()())


def submittable(dispute_id="PP-D-SANDBOX01", **changes):
    return dict(FIX[0], dispute_id=dispute_id, links=[
        {"href": f"https://api-m.sandbox.paypal.com/v1/customer/disputes/{dispute_id}/provide-evidence",
         "rel": "provide_evidence", "method": "POST"}], **changes)


class LiveHarness(unittest.TestCase):
    """Connected Sandbox adapter on MockTransport with both submit flags on unless a test turns one off."""

    def setUp(self):
        for target in ("socket.socket.connect", "socket.create_connection"):
            guard = patch(target, side_effect=AssertionError("network forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        self.detail = submittable()
        self.tracking_reply = {"tracker_identifiers": [{"transaction_id": "SYNTHETICTXN0001",
                                                        "tracking_number": "SYNTHETIC_TRACKING_001"}], "errors": []}
        self.dispute_submit, self.tracking_submit = True, True

        def handler(request):
            request.read()
            self.calls.append(request)
            self.assertTrue(str(request.url).startswith(SANDBOX_BASE + "/"))
            headers = {"PayPal-Debug-Id": DEBUG_ID}
            if request.url.path == "/v1/oauth2/token":
                return httpx.Response(200, headers=headers,
                                      json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            if request.method == "GET" and request.url.path == "/v1/customer/disputes/PP-D-SANDBOX01":
                return httpx.Response(200, headers=headers, json=self.detail)
            if request.method == "POST" and request.url.path.endswith("/provide-evidence"):
                return httpx.Response(200, headers=headers, json={"links": []})
            if request.method == "POST" and request.url.path == "/v1/shipping/trackers-batch":
                return httpx.Response(200, headers=headers, json=self.tracking_reply)
            if request.url.path == "/v2/invoicing/invoices":
                self.invoice_body = json.loads(request.content)
                return httpx.Response(201, headers=headers, json={"id": "INV2-DEMO-1234-5678", "status": "DRAFT"})
            raise AssertionError("unexpected provider path " + request.url.path)

        self.provider = PaypalAdapter(
            config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "", self.dispute_submit,
                                               self.tracking_submit, "SYNTHETICMERCHANT"),
            transport=httpx.MockTransport(handler), clock=self.clock)
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55011),
                                 raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def headers(self):
        return {"Origin": ORIGIN, "X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]}

    def get(self, route):
        return self.client.get(ROOT + route, headers={"X-Demo-Session": self.session["session_id"]})

    def post(self, route, payload=None):
        return self.client.post(ROOT + route, json={} if payload is None else payload, headers=self.headers())

    def ready(self, approve=True):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.post("/demo/inject", {"scenario": "dispute"})
        self.assertEqual(self.get("/paypal/disputes/PP-D-SANDBOX01").status_code, 200)
        draft = self.post("/disputes/case-ref-001/draft").json()
        if approve:
            self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}).status_code, 200)

    def posts(self, suffix):
        return [row for row in self.calls if row.method == "POST" and row.url.path.endswith(suffix)]


class ProvideEvidencePrecheckTests(LiveHarness):
    REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True}

    def test_a_live_dispute_in_another_currency_is_held_to_its_own_read_amount_not_the_case(self):
        # The owner's Sandbox test dispute is TWD 158.00 while the synthetic case is USD 48.00: the send must compare the
        # fresh read with the amount this session read before, not with the synthetic case (r24 review of the r24 fix).
        self.detail = submittable(dispute_amount={"currency_code": "TWD", "value": "158.00"})
        self.ready()
        sent = self.post("/paypal/disputes/provide-evidence", self.REQUEST)
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(sent.json()["external_send"], "SUBMITTED")

    def test_each_fresh_get_refusal_sends_nothing_and_keeps_the_approval(self):
        self.ready()
        refusals = (
            (submittable(status="UNDER_REVIEW"), "dispute_not_awaiting_seller", "not waiting for the seller"),
            (dict(FIX[0], dispute_id="PP-D-SANDBOX01", links=FIX[0]["links"][:1]), "dispute_evidence_not_offered",
             "does not offer evidence"),
            (submittable(dispute_amount={"currency_code": "USD", "value": "49.00"}), "dispute_amount_mismatch", "amount"),
            (submittable(dispute_amount={"currency_code": "EUR", "value": "48.00"}), "dispute_amount_mismatch", "amount"),
            (submittable(evidences=FIX[0]["evidences"] + [{"evidence_type": "PROOF_OF_REFUND", "source": "REQUESTED_FROM_SELLER",
                                                           "action": "PROVIDE_EVIDENCE"}]),
             # (r25 R3 P1-1) A requested refund cannot be shaped (no refund ids are invented): refused, not partial.
             "evidence_type_not_supported", "cannot send"),
            (submittable(reason="MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED"), "dispute_case_mismatch", "does not match"),
        )
        for detail, code, phrase in refusals:
            with self.subTest(code=code):
                self.detail = detail
                refused = self.post("/paypal/disputes/provide-evidence", self.REQUEST)
                self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, code))
                self.assertIn(phrase, refused.json()["error"]["message"])
                self.assertNotIn("does not match the accepted contract", refused.json()["error"]["message"])
        self.assertEqual(self.posts("/provide-evidence"), [])
        # "48.0" is the same amount as the case's "48.00"; the unconsumed approval now sends exactly once.
        self.detail = submittable(dispute_amount={"currency_code": "USD", "value": "48.0"})
        sent = self.post("/paypal/disputes/provide-evidence", self.REQUEST)
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual((sent.json()["external_send"], sent.json()["paypal_debug_id"]), ("SUBMITTED", DEBUG_ID))
        self.assertEqual(len(self.posts("/provide-evidence")), 1)
        request_id = self.posts("/provide-evidence")[0].headers["paypal-request-id"]
        self.assertRegex(request_id, r"^pg-[0-9a-f]{32}$")
        self.assertLessEqual(len(request_id.encode("ascii")), 38)
        content = self.posts("/provide-evidence")[0].content
        self.assertIn(b'"carrier_name":"OTHER"', content)
        self.assertIn(b'"carrier_name_other":"SYNTHETIC_CARRIER"', content)

    def test_debug_ids_are_captured_without_tokens(self):
        self.ready(approve=False)
        status = self.get("/paypal/status").json()
        self.assertEqual(status["evidence_receipt"]["paypal_debug_id"], DEBUG_ID)
        detail = self.get("/paypal/disputes/PP-D-SANDBOX01").json()
        self.assertEqual(detail["paypal_debug_id"], DEBUG_ID)
        self.assertNotIn("provide_evidence_link", detail)
        log = list(self.provider.call_log)
        self.assertEqual([row["call"] for row in log][:2], ["OAUTH_TOKEN", "DISPUTE_DETAIL"])
        self.assertTrue(all(set(row) == {"call", "http_status", "paypal_debug_id", "observed_at"} for row in log))
        self.assertTrue(all(row["paypal_debug_id"] == DEBUG_ID and row["http_status"] == 200 for row in log))
        self.assertNotIn("synthetic-token", json.dumps(log))
        self.assertNotIn("PP-D-SANDBOX01", json.dumps(log))

    def test_a_debug_id_that_is_not_plain_alphanumeric_is_dropped(self):
        adapter = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret"),
                                transport=httpx.MockTransport(lambda _request: httpx.Response(
                                    200, headers={"PayPal-Debug-Id": "abc<script>x"},
                                    json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 60})),
                                clock=self.clock)
        import asyncio
        connected = asyncio.run(adapter.connect())
        self.assertIsNone(connected["evidence_receipt"]["paypal_debug_id"])
        self.assertIsNone(adapter.call_log[-1]["paypal_debug_id"])


class EvidenceBuilderTests(unittest.TestCase):
    def setUp(self):
        self.store = SessionStore(clock=Clock(), rate_limit=50)
        self.session = self.store.sessions[self.store.create()["session_id"]]
        self.store.inject(self.session, "dispute")
        self.store.draft(self.session, "case-ref-001")
        self.restricted = self.session.restricted_evidence["demo-case-001"]

    def test_carrier_names_map_to_the_enum_or_other(self):
        self.assertEqual(map_carrier("ups"), {"carrier_name": "UPS"})
        self.assertEqual(map_carrier("FedEx"), {"carrier_name": "FEDEX"})
        self.assertEqual(map_carrier("Chunghwa Post"), {"carrier_name": "TW_CHUNGHWA_POST"})
        self.assertEqual(map_carrier("Japan Post"), {"carrier_name": "JP_JAPANPOST"})
        self.assertEqual(map_carrier("Acme Couriers"), {"carrier_name": "OTHER", "carrier_name_other": "Acme Couriers"})
        restricted = json.loads(json.dumps(self.restricted, default=str))
        restricted["proof_records"][0]["proof_fields"]["carrier_name"] = "usps"
        built = build_provide_evidence_request("PP-D-00000001", "case-ref-001", restricted, masked=True)
        self.assertEqual(built["input"]["evidences"][0]["evidence_info"]["tracking_info"][0]["carrier_name"], "USPS")
        self.assertNotIn("carrier_name_other", built["input"]["evidences"][0]["evidence_info"]["tracking_info"][0])

    def test_empty_proof_of_fulfillment_is_never_sent(self):
        restricted = dict(self.restricted, proof_records=[])
        with self.assertRaises(BoundaryError) as caught:
            build_provide_evidence_request("PP-D-00000001", "case-ref-001", restricted, masked=True)
        self.assertEqual((caught.exception.status, caught.exception.code), (422, "evidence_not_ready"))

    def test_file_types_and_sizes_follow_the_paypal_limits(self):
        base = self.restricted["attachments"][0]
        for attachment in (dict(base, filename="delivery.exe"), dict(base, detected_media_type="text/plain"),
                           dict(base, filename="delivery.png"), dict(base, size_bytes=10_000_000)):
            with self.subTest(attachment={k: attachment[k] for k in ("filename", "detected_media_type", "size_bytes")}):
                with self.assertRaises(BoundaryError) as caught:
                    build_provide_evidence_request("PP-D-00000001", "case-ref-001",
                                                   dict(self.restricted, attachments=[attachment]), masked=True)
                self.assertEqual(caught.exception.code, "evidence_file_rejected")
        six = [dict(base, attachment_id=f"a{i}", size_bytes=9_000_000) for i in range(6)]
        with self.assertRaises(BoundaryError) as caught:
            build_provide_evidence_request("PP-D-00000001", "case-ref-001", dict(self.restricted, attachments=six), masked=True)
        self.assertEqual(caught.exception.code, "evidence_file_rejected")
        five = six[:5]
        self.assertEqual(len(build_provide_evidence_request("PP-D-00000001", "case-ref-001",
                                                            dict(self.restricted, attachments=five), masked=True)["files"]), 5)


class AddTrackingTests(LiveHarness):
    REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True}

    def test_allowlist_has_only_the_batch_tracker_post(self):
        self.assertTrue(allowed_request("POST", "/v1/shipping/trackers-batch"))
        for method, path in (("GET", "/v1/shipping/trackers-batch"), ("POST", "/v1/shipping/trackers"),
                             ("POST", "/v2/checkout/orders/X/track")):
            self.assertFalse(allowed_request(method, path))

    def test_fixture_preview_is_masked_and_never_contacts_paypal(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        self.assertEqual(self.post("/disputes/case-ref-001/draft").status_code, 200)
        preview = self.post("/paypal/disputes/add-tracking", {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001"})
        self.assertEqual(preview.status_code, 200, preview.text)
        body = preview.json()
        self.assertEqual((body["readback"], body["external_send"], body["source"], body["path"]),
                         ("ADD_TRACKING_PREVIEW", "FROZEN", "synthetic_fixture", "/v1/shipping/trackers-batch"))
        tracker = body["body"]["trackers"][0]
        self.assertEqual((tracker["status"], tracker["carrier"], tracker["carrier_name_other"]), ("SHIPPED", "OTHER", "SYNTHETIC_CARRIER"))
        self.assertTrue(tracker["transaction_id"].endswith("001") and tracker["transaction_id"].startswith("*"))
        self.assertNotIn("SYNTHETIC_TRACKING_001", preview.text)
        self.assertNotIn("SYNTHETICTXN0001", preview.text)
        other = self.post("/paypal/disputes/add-tracking", {"dispute_id": "PP-D-00000002", "case_ref": "case-ref-001"})
        self.assertEqual((other.status_code, other.json()["error"]["code"]), (409, "dispute_case_mismatch"))
        frozen = self.post("/paypal/disputes/add-tracking", {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001", "submit": True})
        self.assertEqual((frozen.status_code, frozen.json()["error"]["code"]), (422, "approval_required"))
        self.assertEqual(self.calls, [])

    def test_send_needs_approval_flag_and_fresh_transaction_then_sends_once(self):
        self.ready(approve=False)
        unapproved = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((unapproved.status_code, unapproved.json()["error"]["code"]), (422, "approval_required"))
        draft = self.post("/disputes/case-ref-001/draft").json()
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}).status_code, 200)
        self.tracking_submit = False
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        frozen = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((frozen.status_code, frozen.json()["error"]["code"]), (503, "provider_action_frozen"))
        self.tracking_submit = True
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.detail = submittable(disputed_transactions=[dict(FIX[0]["disputed_transactions"][0], seller_transaction_id="OTHER-TXN")])
        moved = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((moved.status_code, moved.json()["error"]["code"]), (409, "dispute_detail_required"))
        self.detail = submittable()
        self.tracking_reply = {"tracker_identifiers": [], "errors": [{"name": "INVALID_TRACKING", "message": "private-marker"}]}
        rejected = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((rejected.status_code, rejected.json()["error"]["code"]), (502, "provider_response_invalid"))
        self.assertNotIn("private-marker", rejected.text)
        # A failed send keeps that approval used for tracking: no automatic retry.
        again = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((again.status_code, again.json()["error"]["code"]), (409, "tracking_already_submitted"))
        self.assertEqual(len(self.posts("/v1/shipping/trackers-batch")), 1)
        self.assertEqual(json.loads(self.posts("/v1/shipping/trackers-batch")[0].content),
                         {"trackers": [{"transaction_id": "SYNTHETICTXN0001", "tracking_number": "SYNTHETIC_TRACKING_001",
                                        "status": "SHIPPED", "carrier": "OTHER", "carrier_name_other": "SYNTHETIC_CARRIER"}]})
        # Reset demo and a new review are a new approval: it sends once and reports the PayPal-Debug-Id.
        self.assertEqual(self.post("/demo/inject", {"scenario": "reset"}).status_code, 200)
        self.post("/demo/inject", {"scenario": "dispute"})
        draft = self.post("/disputes/case-ref-001/draft").json()
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}).status_code, 200)
        self.tracking_reply = {"tracker_identifiers": [{"transaction_id": "SYNTHETICTXN0001"}], "errors": []}
        sent = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual((sent.json()["external_send"], sent.json()["readback"], sent.json()["paypal_debug_id"]),
                         ("SUBMITTED", "ADD_TRACKING_SUBMITTED", DEBUG_ID))
        self.assertNotIn("SYNTHETIC_TRACKING_001", sent.text)
        repeat = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual((repeat.status_code, repeat.json()["error"]["code"]), (409, "tracking_already_submitted"))
        self.assertEqual(len(self.posts("/v1/shipping/trackers-batch")), 2)

    def test_hosted_demo_refuses_tracking(self):
        env = {key: value for key, value in os.environ.items() if not key.startswith(("PAYGUARD_", "PAYPAL_"))}
        env.update({"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": "payguard-demo.onrender.com"})
        with mock.patch.dict(os.environ, env, clear=True):
            app = create_app(store=SessionStore())
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55012),
                        raise_server_exceptions=False) as client:
            session = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
            refused = client.post(ROOT + "/paypal/disputes/add-tracking", json=dict(self.REQUEST, submit=False),
                                  headers={"Origin": ORIGIN, "X-Demo-Session": session["session_id"],
                                           "X-CSRF-Token": session["csrf_token"]})
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (503, "hosted_demo_disabled"))


class ZeroDecimalInvoiceTests(LiveHarness):
    def test_schema_takes_whole_amounts_for_twd_jpy_huf_only(self):
        for currency in ("TWD", "JPY", "HUF"):
            InvoicePayload.model_validate({"description": "Synthetic cup", "amount": "1500", "currency": currency})
            for amount in ("1500.00", "1500.5", "15.0"):
                with self.subTest(currency=currency, amount=amount), self.assertRaises(ValidationError) as caught:
                    InvoicePayload.model_validate({"description": "Synthetic cup", "amount": amount, "currency": currency})
                self.assertIn("invoice_amount_whole_units", str(caught.exception))
        InvoicePayload.model_validate({"description": "Synthetic cup", "amount": "10.00", "currency": "USD"})
        for amount in ("10", "10.5"):
            with self.assertRaises(ValidationError):
                InvoicePayload.model_validate({"description": "Synthetic cup", "amount": amount, "currency": "USD"})

    def test_route_explains_whole_amounts_and_drafts_a_twd_invoice(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        refused = self.post("/paypal/invoices/review", {"description": "Synthetic ceramic cup", "amount": "1500.00",
                                                        "currency": "TWD", "confirm_sandbox_draft": True})
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (422, "invoice_amount_whole_units"))
        self.assertIn("whole amounts", refused.json()["error"]["message"])
        evaluated = self.post("/aup/review", {"description": "Synthetic ceramic cup"}).json()
        payload = {"description": "Synthetic ceramic cup", "amount": "1500", "currency": "TWD"}
        review = self.post("/paypal/invoices/review", dict(payload, confirm_sandbox_draft=True,
                                                           evaluation_id=evaluated["evaluation_id"],
                                                           description_digest=evaluated["description_digest"]))
        self.assertEqual(review.status_code, 200, review.text)
        draft = self.post("/paypal/invoices/draft", dict(payload, review_token=review.json()["review_token"],
                                                         payload_digest=review.json()["payload_digest"]))
        self.assertEqual(draft.status_code, 200, draft.text)
        self.assertEqual(self.invoice_body["items"][0]["unit_amount"], {"currency_code": "TWD", "value": "1500"})
        self.assertEqual(draft.json()["evidence_receipt"]["paypal_debug_id"], DEBUG_ID)
        self.assertLessEqual(len(self.posts("/v2/invoicing/invoices")[0].headers["paypal-request-id"]), 38)


if __name__ == "__main__":
    unittest.main()
