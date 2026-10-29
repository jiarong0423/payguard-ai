"""Offline Disputes readback and provide-evidence preview tests.

Every provider response here is a synthetic MockTransport reply or the built-in
fixture. No test contacts the network or needs a credential.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
import socket
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import httpx
from pydantic import ValidationError

from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig, SANDBOX_BASE, allowed_request
from app.paypal_disputes import (FIXTURE_DISPUTES, build_provide_evidence_request, multipart_parts,
                                 sanitize_dispute_detail, sanitize_dispute_list, sanitize_dispute_summary)
from app.schemas import DisputeDetailResponse, DisputeListResponse, ProvideEvidenceResponse
from app.store import BoundaryError, DEMO_BURST_AMOUNTS, SessionStore


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
PRIVATE_MARKERS = ("Synthetic Demo Person", "Synthetic Demo Seller", "SYNTHETICMERCHANT", "private-", "example.invalid",
                   "synthetic-token", "synthetic-secret", "links", "messages", "documents")


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 29, 8, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


def sandbox_list_reply():
    return {"items": [dict(FIXTURE_DISPUTES[0], dispute_id="PP-D-SANDBOX01",
                           messages=[{"content": "private-message-marker"}]),
                      dict(FIXTURE_DISPUTES[1], dispute_id="PP-D-SANDBOX02")],
            "links": [{"href": "https://api-m.sandbox.paypal.com/private-link-marker", "rel": "self"}]}


def sandbox_detail_reply(dispute_id="PP-D-SANDBOX01"):
    return dict(FIXTURE_DISPUTES[0], dispute_id=dispute_id, status="OTHER", dispute_life_cycle_stage="UNEXPECTED",
                extensions={"merchant_contacted": True}, offer={"buyer_requested_amount": {"value": "1.00"}})


class AllowlistTests(unittest.TestCase):
    def test_method_path_matrix(self):
        allowed = [("POST", "/v1/oauth2/token"), ("POST", "/v2/invoicing/invoices"),
                   ("POST", "/v1/notifications/verify-webhook-signature"), ("GET", "/v1/customer/disputes"),
                   ("GET", "/v1/customer/disputes/PP-D-00000001"),
                   ("POST", "/v1/customer/disputes/PP-D-00000001/provide-evidence")]
        rejected = [("GET", "/v1/oauth2/token"), ("POST", "/v1/customer/disputes"),
                    ("POST", "/v1/customer/disputes/PP-D-00000001"), ("GET", "/v1/customer/disputes/PP-D-00000001/provide-evidence"),
                    ("POST", "/v1/customer/disputes/PP-D-00000001/accept-claim"),
                    ("POST", "/v1/customer/disputes/PP-D-00000001/acknowledge-return-item"),
                    ("GET", "/v1/customer/disputes/../../v2/invoicing/invoices"), ("GET", "/v1/customer/disputes/pp-d-1"),
                    ("DELETE", "/v1/customer/disputes/PP-D-00000001"), ("GET", "/v1/customer/disputes/PP-D-00000001/"),
                    ("GET", "/v1/reporting/transactions"), ("POST", "/v2/checkout/orders")]
        for method, path in allowed:
            with self.subTest(method=method, path=path):
                self.assertTrue(allowed_request(method, path))
        for method, path in rejected:
            with self.subTest(method=method, path=path):
                self.assertFalse(allowed_request(method, path))


class SanitizerTests(unittest.TestCase):
    def test_summary_and_detail_drop_private_fields(self):
        summary = sanitize_dispute_summary(FIXTURE_DISPUTES[0])
        self.assertEqual(set(summary), {"dispute_id", "reason", "status", "dispute_life_cycle_stage", "dispute_state",
                                        "dispute_amount", "create_time", "update_time", "seller_response_due_date"})
        detail = sanitize_dispute_detail(sandbox_detail_reply())
        self.assertEqual(detail["status"], "UNKNOWN")
        self.assertEqual(detail["dispute_life_cycle_stage"], "UNKNOWN")
        self.assertEqual(detail["disputed_transactions"], [{"seller_transaction_id": "SYNTHETIC-TXN-0001",
                                                            "transaction_status": "COMPLETED",
                                                            "gross_amount": {"currency_code": "USD", "value": "48.00"},
                                                            "seller_protection_eligible": True}])
        self.assertEqual(detail["evidences"], [{"evidence_type": "PROOF_OF_FULFILLMENT", "source": "REQUESTED_FROM_SELLER",
                                                "action": "PROVIDE_EVIDENCE", "date": "2026-10-20T14:02:11.000Z"}])
        encoded = json.dumps(detail)
        for marker in PRIVATE_MARKERS:
            self.assertNotIn(marker, encoded)
        DisputeDetailResponse.model_validate(dict(detail, source="synthetic_fixture", data_source_label="Fixture",
                                                  environment="sandbox", evidence_class="SYNTHETIC_FIXTURE",
                                                  observed_at="2026-10-29T08:00:00Z", provider_submission="NOT_PERFORMED",
                                                  readback="GET_DETAIL"))

    def test_invalid_provider_shapes_fail_closed(self):
        for broken in ({"items": "rows"}, {"items": [{"dispute_id": "../x"}]},
                       {"items": [FIXTURE_DISPUTES[0], FIXTURE_DISPUTES[0]]},
                       {"items": [dict(FIXTURE_DISPUTES[0], dispute_amount={"currency_code": "usd", "value": "1"})]},
                       {"items": [dict(FIXTURE_DISPUTES[0], create_time="2026-10-20 14:02")]},
                       {"items": [dict(FIXTURE_DISPUTES[0], reason=["MERCHANDISE_OR_SERVICE_NOT_RECEIVED"])]}):
            with self.subTest(broken=str(broken)[:60]), self.assertRaises(BoundaryError) as caught:
                sanitize_dispute_list(broken)
            self.assertEqual(caught.exception.code, "provider_response_invalid")
        self.assertEqual(sanitize_dispute_list({}), [])
        with self.assertRaises(BoundaryError):
            sanitize_dispute_detail(dict(FIXTURE_DISPUTES[0], disputed_transactions=[{"seller_transaction_id": "a b"}]))
        with self.assertRaises(BoundaryError):
            sanitize_dispute_detail(dict(FIXTURE_DISPUTES[0], evidences=[{"evidence_type": "proof"}]))

    def test_schema_bindings_reject_inconsistent_envelopes(self):
        base = dict(source="synthetic_fixture", data_source_label="Fixture", environment="sandbox",
                    evidence_class="SYNTHETIC_FIXTURE", observed_at="2026-10-29T08:00:00Z",
                    provider_submission="NOT_PERFORMED", readback="GET_LIST", items=[])
        DisputeListResponse.model_validate(base)
        for change in ({"source": "paypal_sandbox"}, {"data_source_label": "Sandbox"}, {"provider_submission": "PERFORMED"},
                       {"evidence_class": "AUTHENTIC_SANDBOX_RESPONSE"}, {"extra": 1}):
            with self.subTest(change=change), self.assertRaises(ValidationError):
                DisputeListResponse.model_validate(dict(base, **change))
        preview = dict(source="paypal_sandbox", data_source_label="Sandbox", environment="sandbox",
                       evidence_class="SYNTHETIC_TEST_RESPONSE", observed_at="2026-10-29T08:00:00Z",
                       provider_submission="NOT_PERFORMED", readback="PROVIDE_EVIDENCE_PREVIEW",
                       dispute_id="PP-D-00000001", case_ref="case-ref-001", method="POST",
                       path="/v1/customer/disputes/PP-D-00000001/provide-evidence", content_type="multipart/form-data",
                       input={"evidences": [{"evidence_type": "PROOF_OF_FULFILLMENT", "evidence_info": {"tracking_info": []},
                                             "notes": "n"}]},
                       files=[], external_send="FROZEN", submit_flag_enabled=False, human_review_required=True)
        ProvideEvidenceResponse.model_validate(preview)
        for change in ({"external_send": "SUBMITTED"}, {"provider_submission": "PERFORMED"},
                       {"readback": "PROVIDE_EVIDENCE_SUBMITTED"}, {"path": "/v1/customer/disputes/PP-D-00000002/provide-evidence"},
                       {"external_send": "SUBMITTED", "provider_submission": "PERFORMED",
                        "readback": "PROVIDE_EVIDENCE_SUBMITTED"},
                       {"source": "synthetic_fixture", "data_source_label": "Fixture", "evidence_class": "SYNTHETIC_FIXTURE",
                        "external_send": "SUBMITTED", "provider_submission": "PERFORMED",
                        "readback": "PROVIDE_EVIDENCE_SUBMITTED", "submit_flag_enabled": True}):
            with self.subTest(change=change), self.assertRaises(ValidationError):
                ProvideEvidenceResponse.model_validate(dict(preview, **change))


class BurstFixtureTests(unittest.TestCase):
    def test_burst_amounts_vary_and_keep_ratio_five(self):
        store = SessionStore(clock=Clock(), rate_limit=50)
        session = store.sessions[store.create()["session_id"]]
        state = store.inject(session, "burst")
        amounts = [row["amount"] for row in state["transactions"]]
        self.assertEqual(len(amounts), 50)
        self.assertEqual(len(set(amounts)), len(DEMO_BURST_AMOUNTS))
        self.assertEqual(sum(Decimal(value) for value in amounts), Decimal("500.00"))
        self.assertEqual(state["velocity"]["ratio"], "5")
        self.assertEqual(state["velocity"]["status"], "review_velocity")
        self.assertEqual(sum(Decimal(value) for value in DEMO_BURST_AMOUNTS), Decimal("100.00"))


class FixtureRouteTests(unittest.TestCase):
    """Provider disabled: every dispute route answers from the fixture, never the network."""

    def setUp(self):
        for target in ("socket.socket.connect", "socket.create_connection"):
            guard = patch(target, side_effect=AssertionError("network forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        def handler(request):
            self.calls.append(request)
            raise AssertionError("Provider must not be contacted in fixture mode")
        self.provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(handler),
                                      clock=self.clock)
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001),
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

    def test_fixture_list_and_detail_are_labelled_and_sanitized(self):
        response = self.get("/paypal/disputes")
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual((body["source"], body["data_source_label"], body["evidence_class"], body["readback"]),
                         ("synthetic_fixture", "Fixture", "SYNTHETIC_FIXTURE", "GET_LIST"))
        self.assertEqual([row["dispute_id"] for row in body["items"]], ["PP-D-00000001", "PP-D-00000002"])
        self.assertEqual(body["items"][0]["dispute_amount"], {"currency_code": "USD", "value": "48.00"})
        detail = self.get("/paypal/disputes/PP-D-00000001")
        self.assertEqual(detail.status_code, 200, detail.text)
        self.assertEqual(detail.json()["readback"], "GET_DETAIL")
        self.assertEqual(detail.json()["data_source_label"], "Fixture")
        self.assertEqual(detail.json()["evidences"][0]["source"], "REQUESTED_FROM_SELLER")
        for marker in PRIVATE_MARKERS:
            self.assertNotIn(marker, response.text)
            self.assertNotIn(marker, detail.text)
        self.assertEqual(self.get("/paypal/disputes/PP-D-99999999").json()["error"]["code"], "dispute_not_found")
        self.assertEqual(self.get("/paypal/disputes/pp-d-1").status_code, 422)
        self.assertEqual(self.client.get(ROOT + "/paypal/disputes").status_code, 401)
        self.assertEqual(self.calls, [])

    def test_preview_requires_draft_and_masks_restricted_values(self):
        missing = self.post("/paypal/disputes/provide-evidence", {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001"})
        self.assertEqual(missing.json()["error"]["code"], "case_not_found")
        self.post("/demo/inject", {"scenario": "dispute"})
        no_draft = self.post("/paypal/disputes/provide-evidence", {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001"})
        self.assertEqual(no_draft.json()["error"]["code"], "draft_required")
        self.assertEqual(self.post("/disputes/case-ref-001/draft").status_code, 200)
        preview = self.post("/paypal/disputes/provide-evidence", {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001"})
        self.assertEqual(preview.status_code, 200, preview.text)
        body = preview.json()
        self.assertEqual((body["method"], body["path"], body["content_type"]),
                         ("POST", "/v1/customer/disputes/PP-D-00000001/provide-evidence", "multipart/form-data"))
        self.assertEqual((body["external_send"], body["provider_submission"], body["submit_flag_enabled"], body["source"]),
                         ("FROZEN", "NOT_PERFORMED", False, "synthetic_fixture"))
        evidence = body["input"]["evidences"]
        self.assertEqual(len(evidence), 1)
        self.assertEqual(evidence[0]["evidence_type"], "PROOF_OF_FULFILLMENT")
        self.assertEqual(evidence[0]["evidence_info"]["tracking_info"][0]["tracking_number"], "*" * 19 + "001")
        self.assertEqual(evidence[0]["evidence_info"]["tracking_info"][0]["carrier_name_other"], "SYNTHETIC_CARRIER")
        self.assertEqual(body["files"], [{"name": "file1", "filename": "synthetic-delivery.pdf",
                                          "content_type": "application/pdf", "byte_length": 43}])
        self.assertNotIn("SYNTHETIC_TRACKING_001", preview.text)
        self.assertNotIn("%PDF", preview.text)
        for change in ({"submit": "yes"}, {"dispute_id": "PP-D-0000 1"}, {"case_ref": "demo-case-001"}, {"extra": 1}):
            self.assertEqual(self.post("/paypal/disputes/provide-evidence",
                                       dict({"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001"}, **change)).status_code, 422)
        frozen = self.post("/paypal/disputes/provide-evidence",
                           {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001", "submit": True})
        self.assertEqual((frozen.status_code, frozen.json()["error"]["code"]), (503, "provider_action_frozen"))
        self.assertEqual(self.calls, [])
        self.assertNotIn("provide_evidence", [row["kind"] for row in self.client.get(
            ROOT + "/demo/state", headers={"X-Demo-Session": self.session["session_id"]}).json()["activity"]])


class SandboxRouteTests(unittest.TestCase):
    """Provider enabled with MockTransport: GET readback and the gated submit path."""

    def setUp(self):
        for target in ("socket.socket.connect", "socket.create_connection"):
            guard = patch(target, side_effect=AssertionError("network forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        self.list_reply = sandbox_list_reply()
        self.detail_reply = sandbox_detail_reply()
        self.submit_status = 200
        self.submit_enabled = False
        def handler(request):
            request.read()
            self.calls.append(request)
            self.assertTrue(str(request.url).startswith(SANDBOX_BASE + "/"))
            if request.url.path == "/v1/oauth2/token":
                return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            self.assertEqual(request.headers["authorization"], "Bearer synthetic-token")
            if request.method == "GET" and request.url.path == "/v1/customer/disputes":
                self.assertEqual(request.url.params["page_size"], "10")
                return httpx.Response(200, json=self.list_reply)
            if request.method == "GET" and request.url.path == "/v1/customer/disputes/PP-D-SANDBOX01":
                return httpx.Response(200, json=self.detail_reply)
            if request.method == "POST" and request.url.path.endswith("/provide-evidence"):
                return httpx.Response(self.submit_status, json={"links": [{"href": "https://api-m.sandbox.paypal.com/private", "rel": "self"}]})
            raise AssertionError("unexpected provider path " + request.url.path)
        self.provider = PaypalAdapter(
            config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "", self.submit_enabled),
            transport=httpx.MockTransport(handler), clock=self.clock)
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001),
                                 raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def tearDown(self):
        self.assertEqual(self.provider.open_clients, 0)

    def headers(self):
        return {"Origin": ORIGIN, "X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]}

    def get(self, route):
        return self.client.get(ROOT + route, headers={"X-Demo-Session": self.session["session_id"]})

    def post(self, route, payload=None):
        return self.client.post(ROOT + route, json={} if payload is None else payload, headers=self.headers())

    def connect(self):
        response = self.post("/paypal/connect")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "connected")

    def test_fixture_until_connected_then_sandbox_readback(self):
        before = self.get("/paypal/disputes").json()
        self.assertEqual(before["source"], "synthetic_fixture")
        self.assertEqual(self.calls, [])
        self.connect()
        listed = self.get("/paypal/disputes")
        self.assertEqual(listed.status_code, 200, listed.text)
        body = listed.json()
        self.assertEqual((body["source"], body["data_source_label"], body["evidence_class"]),
                         ("paypal_sandbox", "Sandbox", "SYNTHETIC_TEST_RESPONSE"))
        self.assertEqual([row["dispute_id"] for row in body["items"]], ["PP-D-SANDBOX01", "PP-D-SANDBOX02"])
        detail = self.get("/paypal/disputes/PP-D-SANDBOX01")
        self.assertEqual(detail.status_code, 200, detail.text)
        self.assertEqual(detail.json()["status"], "UNKNOWN")
        self.assertEqual(detail.json()["data_source_label"], "Sandbox")
        for marker in PRIVATE_MARKERS + ("private-message-marker", "private-link-marker", "merchant_contacted"):
            self.assertNotIn(marker, listed.text)
            self.assertNotIn(marker, detail.text)
        self.assertEqual([(row.method, row.url.path) for row in self.calls],
                         [("POST", "/v1/oauth2/token"), ("GET", "/v1/customer/disputes"),
                          ("GET", "/v1/customer/disputes/PP-D-SANDBOX01")])
        self.detail_reply = sandbox_detail_reply("PP-D-SANDBOX02")
        mismatch = self.get("/paypal/disputes/PP-D-SANDBOX01")
        self.assertEqual((mismatch.status_code, mismatch.json()["error"]["code"]), (502, "provider_response_invalid"))
        self.list_reply = {"items": [{"dispute_id": "PP-D-SANDBOX01", "reason": "OTHER"}]}
        self.assertEqual(self.get("/paypal/disputes").json()["error"]["code"], "provider_response_invalid")

    def test_submit_requires_explicit_flag_and_posts_multipart(self):
        self.connect()
        self.post("/demo/inject", {"scenario": "dispute"})
        self.assertEqual(self.post("/disputes/case-ref-001/draft").status_code, 200)
        request = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True}
        frozen = self.post("/paypal/disputes/provide-evidence", request)
        self.assertEqual((frozen.status_code, frozen.json()["error"]["code"]), (503, "provider_action_frozen"))
        self.assertFalse(any(row.url.path.endswith("/provide-evidence") for row in self.calls))
        preview = self.post("/paypal/disputes/provide-evidence", dict(request, submit=False)).json()
        self.assertEqual((preview["source"], preview["external_send"], preview["submit_flag_enabled"]),
                         ("paypal_sandbox", "FROZEN", False))
        self.submit_enabled = True
        self.connect()
        submitted = self.post("/paypal/disputes/provide-evidence", request)
        self.assertEqual(submitted.status_code, 200, submitted.text)
        body = submitted.json()
        self.assertEqual((body["external_send"], body["provider_submission"], body["readback"], body["submit_flag_enabled"]),
                         ("SUBMITTED", "PERFORMED", "PROVIDE_EVIDENCE_SUBMITTED", True))
        self.assertEqual(body["input"]["evidences"][0]["evidence_info"]["tracking_info"][0]["tracking_number"], "*" * 19 + "001")
        self.assertNotIn("SYNTHETIC_TRACKING_001", submitted.text)
        posted = [row for row in self.calls if row.url.path == "/v1/customer/disputes/PP-D-SANDBOX01/provide-evidence"]
        self.assertEqual(len(posted), 1)
        self.assertTrue(posted[0].headers["content-type"].startswith("multipart/form-data; boundary="))
        content = posted[0].content
        self.assertIn(b'name="input"', content)
        self.assertIn(b'"evidence_type":"PROOF_OF_FULFILLMENT"', content)
        self.assertIn(b'"tracking_number":"SYNTHETIC_TRACKING_001"', content)
        self.assertIn(b'name="file1"; filename="synthetic-delivery.pdf"', content)
        self.assertIn(b"%PDF-1.7", content)
        self.assertNotIn(("*" * 19 + "001").encode(), content)
        activity = self.client.get(ROOT + "/demo/state", headers={"X-Demo-Session": self.session["session_id"]}).json()["activity"]
        self.assertIn("provide_evidence", [row["kind"] for row in activity])
        self.submit_status = 400
        failed = self.post("/paypal/disputes/provide-evidence", request)
        self.assertEqual((failed.status_code, failed.json()["error"]["code"]), (502, "provider_upstream_failure"))
        self.assertNotIn("private", failed.text)


class RequestBuilderTests(unittest.TestCase):
    def setUp(self):
        self.store = SessionStore(clock=Clock(), rate_limit=50)
        self.session = self.store.sessions[self.store.create()["session_id"]]
        self.store.inject(self.session, "dispute")
        self.store.draft(self.session, "case-ref-001")
        self.restricted = self.session.restricted_evidence["demo-case-001"]
        self.attachment_bytes = {row["attachment_id"]: row["content"]
                                 for row in self.session.disputes["demo-case-001"]["attachment_candidates"]}

    def test_masked_and_unmasked_requests_share_structure(self):
        masked = build_provide_evidence_request("PP-D-00000001", "case-ref-001", self.restricted, masked=True)
        raw = build_provide_evidence_request("PP-D-00000001", "case-ref-001", self.restricted, masked=False,
                                             attachment_bytes=self.attachment_bytes)
        self.assertEqual(masked["files"][0]["byte_length"], len(raw["files"][0]["content"]))
        for broken in ({}, {"demo-attachment-001": b"%PDF-1.7\ntampered\n%%EOF\n"}):
            with self.subTest(broken=str(broken)[:30]), self.assertRaises(BoundaryError) as caught:
                build_provide_evidence_request("PP-D-00000001", "case-ref-001", self.restricted, masked=False,
                                               attachment_bytes=broken)
            self.assertEqual(caught.exception.code, "dispute_context_not_ready")
        self.assertEqual(masked["input"]["evidences"][0]["evidence_type"], raw["input"]["evidences"][0]["evidence_type"])
        self.assertEqual(raw["input"]["evidences"][0]["evidence_info"]["tracking_info"][0]["tracking_number"], "SYNTHETIC_TRACKING_001")
        self.assertNotIn("content", masked["files"][0])
        self.assertEqual(raw["files"][0]["content"], b"%PDF-1.7\nSynthetic delivery evidence\n%%EOF\n")
        parts = multipart_parts(raw)
        self.assertEqual(set(parts), {"input", "file1"})
        self.assertEqual(parts["input"][2], "application/json")
        self.assertEqual(json.loads(parts["input"][1]), raw["input"])
        self.assertEqual(parts["file1"], ("synthetic-delivery.pdf", raw["files"][0]["content"], "application/pdf"))
        with self.assertRaises(BoundaryError):
            build_provide_evidence_request("bad id", "case-ref-001", self.restricted, masked=True)
        with self.assertRaises(BoundaryError) as caught:
            build_provide_evidence_request("PP-D-00000001", "case-ref-001", dict(self.restricted, requirements=[]), masked=True)
        self.assertEqual(caught.exception.code, "dispute_context_not_ready")


class AdapterGuardTests(unittest.IsolatedAsyncioTestCase):
    async def test_disputes_require_connection_and_frozen_paths_never_reach_transport(self):
        calls = []
        def handler(request):
            calls.append(request)
            if request.url.path == "/v1/oauth2/token":
                return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            return httpx.Response(200, json={})
        adapter = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret"),
                                transport=httpx.MockTransport(handler), clock=Clock())
        for coroutine in (adapter.list_disputes(), adapter.get_dispute("PP-D-00000001"),
                          adapter.provide_evidence("PP-D-00000001", {"input": (None, "{}", "application/json")})):
            with self.assertRaises(BoundaryError) as caught:
                await coroutine
            self.assertEqual(caught.exception.code, "provider_disabled")
        await adapter.connect()
        self.assertFalse(adapter.dispute_submit_enabled())
        with self.assertRaises(BoundaryError) as caught:
            await adapter.provide_evidence("PP-D-00000001", {"input": (None, "{}", "application/json")})
        self.assertEqual(caught.exception.code, "provider_action_frozen")
        with self.assertRaises(BoundaryError) as caught:
            await adapter._request("/v1/customer/disputes/PP-D-00000001/accept-claim", method="POST", headers={})
        self.assertEqual(caught.exception.code, "provider_action_frozen")
        with self.assertRaises(BoundaryError):
            await adapter.get_dispute("PP-D-0000 1")
        with self.assertRaises(BoundaryError):
            await adapter.list_disputes(page_size=50)
        self.assertEqual([row.url.path for row in calls], ["/v1/oauth2/token"])
        self.assertEqual(adapter.open_clients, 0)


if __name__ == "__main__":
    unittest.main()
