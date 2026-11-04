"""Regression tests for the r25 backend review (R1 AI drift, R3 PayPal technical, R5 red team).

Every provider reply is a synthetic MockTransport answer and every model is a fake callable; no test opens a
network connection, reads a credential or starts a worker.
"""

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
import socket
import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import httpx

from app import studio_agent as sa
from app.ai_brief import AiBriefError
from app.guide_routes import GuideService, governed_model_rows
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.paypal_disputes import (FIXTURE_DISPUTE_IDS, SUPPORTED_EVIDENCE_TYPES, build_provide_evidence_request,
                                 build_tracking_request, fixture_disputes, submit_refusal)
from app.store import BoundaryError, SessionStore
from send_confirmation import with_confirmation
from payguard import controlled_fallback as cf
from payguard.controlled_fallback import Governor

ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
PUBLIC = "payguard-demo.onrender.com"


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 29, 8, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


def no_network(test):
    for target in ("socket.socket.connect", "socket.create_connection"):
        guard = patch(target, side_effect=AssertionError("network forbidden"))
        guard.start()
        test.addCleanup(guard.stop)


def clean_env(**values):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("PAYGUARD_", "PAYPAL_", "GEMINI", "CHANNEL3", "GOOGLE"))}
    env.update(values)
    return patch.dict(os.environ, env, clear=True)


FIX = fixture_disputes(Clock()())


def live_detail(dispute_id, transaction_id, **changes):
    detail = deepcopy(FIX[0])
    detail["dispute_id"] = dispute_id
    detail["disputed_transactions"][0]["seller_transaction_id"] = transaction_id
    detail["links"] = [{"href": f"https://api-m.sandbox.paypal.com/v1/customer/disputes/{dispute_id}/provide-evidence",
                        "rel": "provide_evidence", "method": "POST"}]
    detail.update(changes)
    return detail


class TwoDisputeHarness(unittest.TestCase):
    """Connected Sandbox adapter on MockTransport with two item-not-received disputes and both submit flags on."""

    def setUp(self):
        no_network(self)
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        self.merchant_id = getattr(self, "MERCHANT_ID", "SYNTHETICMERCHANT")
        self.details = {"PP-D-SANDBOX01": live_detail("PP-D-SANDBOX01", "TXNAAAA0001"),
                        "PP-D-SANDBOX02": live_detail("PP-D-SANDBOX02", "TXNBBBB0002")}

        def handler(request):
            request.read()
            self.calls.append(request)
            path = request.url.path
            headers = {"PayPal-Debug-Id": "f00dbabe12345"}
            if path == "/v1/oauth2/token":
                return httpx.Response(200, headers=headers,
                                      json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            if request.method == "GET" and path.startswith("/v1/customer/disputes/"):
                return httpx.Response(200, headers=headers, json=self.details[path.rsplit("/", 1)[1]])
            if request.method == "POST" and path.endswith("/provide-evidence"):
                return httpx.Response(200, headers=headers, json={"links": []})
            if request.method == "POST" and path == "/v1/shipping/trackers-batch":
                tracker = json.loads(request.content)["trackers"][0]
                return httpx.Response(200, headers=headers, json={"tracker_identifiers": [
                    {"transaction_id": tracker["transaction_id"], "tracking_number": tracker["tracking_number"]}], "errors": []})
            raise AssertionError("unexpected provider path " + path)

        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "", True, True,
                                                                    self.merchant_id),
                                 transport=httpx.MockTransport(handler), clock=self.clock)
        with clean_env():
            self.app = create_app(store=self.store, paypal=provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55061),
                                 raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        self.session_id = session["session_id"]

    def post(self, route, payload=None):
        return with_confirmation(self._post, route, payload)

    def _post(self, route, payload=None):
        return self.client.post(ROOT + route, json={} if payload is None else payload, headers=self.headers)

    def get(self, route):
        return self.client.get(ROOT + route, headers={"X-Demo-Session": self.session_id})

    def ready(self, *case_refs):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.post("/demo/inject", {"scenario": "dispute"})
        for dispute_id in self.details:
            self.assertEqual(self.get("/paypal/disputes/" + dispute_id).status_code, 200)
        for case_ref in case_refs:
            draft = self.post(f"/disputes/{case_ref}/draft")
            self.assertEqual(draft.status_code, 200, draft.text)
            approved = self.post(f"/disputes/{case_ref}/approve", {"draft_digest": draft.json()["draft_digest"]})
            self.assertEqual(approved.status_code, 200, approved.text)

    def posts(self, suffix):
        return [row for row in self.calls if row.method == "POST" and row.url.path.endswith(suffix)]

    @staticmethod
    def code(response):
        return response.status_code, response.json().get("error", {}).get("code")


class TrackingBindingTests(TwoDisputeHarness):
    """(r25 R5 P1-1) add-tracking uses the same two-way case <-> dispute binding as provide-evidence."""

    def evidence(self, dispute_id, case_ref="case-ref-001"):
        return self.post("/paypal/disputes/provide-evidence", {"dispute_id": dispute_id, "case_ref": case_ref, "submit": True})

    def tracking(self, dispute_id, case_ref="case-ref-001", submit=True):
        return self.post("/paypal/disputes/add-tracking", {"dispute_id": dispute_id, "case_ref": case_ref, "submit": submit})

    def test_evidence_first_then_tracking_to_another_dispute_is_refused(self):
        self.ready("case-ref-001")
        sent = self.evidence("PP-D-SANDBOX01")
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(sent.json()["external_send"], "SUBMITTED")
        refused = self.tracking("PP-D-SANDBOX02")
        self.assertEqual(self.code(refused), (409, "dispute_case_bound"))
        self.assertEqual(self.posts("/v1/shipping/trackers-batch"), [])
        # The bound dispute still takes this case's tracking.
        same = self.tracking("PP-D-SANDBOX01")
        self.assertEqual(same.status_code, 200, same.text)
        self.assertEqual(json.loads(self.posts("/v1/shipping/trackers-batch")[0].content)["trackers"][0]["transaction_id"],
                         "TXNAAAA0001")

    def test_tracking_first_then_evidence_to_another_dispute_is_refused(self):
        self.ready("case-ref-001")
        sent = self.tracking("PP-D-SANDBOX02")
        self.assertEqual(sent.status_code, 200, sent.text)
        refused = self.evidence("PP-D-SANDBOX01")
        self.assertEqual(self.code(refused), (409, "dispute_case_bound"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_tracking_preview_records_the_binding_before_any_send(self):
        self.ready("case-ref-001")
        preview = self.tracking("PP-D-SANDBOX02", submit=False)
        self.assertEqual(preview.status_code, 200, preview.text)
        self.assertEqual(self.code(self.evidence("PP-D-SANDBOX01")), (409, "dispute_case_bound"))
        self.assertEqual(self.code(self.tracking("PP-D-SANDBOX01", submit=False)), (409, "dispute_case_bound"))
        self.assertEqual(self.posts("/provide-evidence") + self.posts("/v1/shipping/trackers-batch"), [])

    def test_a_dispute_bound_to_another_case_refuses_that_cases_tracking(self):
        self.ready("case-ref-001")
        self.assertEqual(self.evidence("PP-D-SANDBOX01").status_code, 200)
        draft = self.post("/disputes/case-ref-003/draft")
        self.assertEqual(draft.status_code, 200, draft.text)
        refused = self.tracking("PP-D-SANDBOX01", case_ref="case-ref-003", submit=False)
        self.assertEqual(self.code(refused), (409, "dispute_case_bound"))
        self.assertEqual(self.posts("/v1/shipping/trackers-batch"), [])


class AccountIdentityTests(TwoDisputeHarness):
    """(r25 send guard) A real send needs the fresh read's seller.merchant_id to equal the connected account's id."""

    def send_both(self):
        evidence = self.post("/paypal/disputes/provide-evidence",
                             {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True})
        tracking = self.post("/paypal/disputes/add-tracking",
                             {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True})
        return evidence, tracking

    def test_matching_ids_send_and_responses_carry_masks_only(self):
        self.ready("case-ref-001")
        detail = self.get("/paypal/disputes/PP-D-SANDBOX01")
        self.assertNotIn("SYNTHETICMERCHANT", detail.text)
        preview = self.post("/paypal/disputes/provide-evidence",
                            {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": False}).json()
        self.assertEqual(preview["send_guard"], {
            "case_ref": "case-ref-001", "case_reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "dispute_masked": "PP-D-\u202601",
            "dispute_reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "dispute_amount": {"currency_code": "USD", "value": "48.00"},
            "bound_dispute_masked": "PP-D-\u202601", "sending_account_masked": "SY\u2026HANT",
            "dispute_seller_masked": "SY\u2026HANT", "account_status": "MATCH", "send_refusal": None})
        evidence, tracking = self.send_both()
        self.assertEqual((evidence.status_code, tracking.status_code), (200, 200), evidence.text + tracking.text)
        self.assertEqual((len(self.posts("/provide-evidence")), len(self.posts("/v1/shipping/trackers-batch"))), (1, 1))
        for response in (preview, evidence.json(), tracking.json()):
            self.assertNotIn("SYNTHETICMERCHANT", json.dumps(response))

    def test_a_dispute_of_another_account_is_refused_with_no_provider_post(self):
        for dispute in self.details.values():
            dispute["disputed_transactions"][0]["seller"] = {"merchant_id": "OTHERACCOUNT9876", "name": "Synthetic Other"}
        self.ready("case-ref-001")
        preview = self.post("/paypal/disputes/add-tracking",
                            {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": False}).json()
        self.assertEqual((preview["send_guard"]["account_status"], preview["send_guard"]["send_refusal"],
                          preview["send_guard"]["dispute_seller_masked"]), ("MISMATCH", "dispute_not_this_account", "OT\u20269876"))
        for response in self.send_both():
            self.assertEqual(self.code(response), (409, "dispute_not_this_account"))
            self.assertIn("different PayPal account", response.json()["error"]["message"])
        self.assertEqual(self.posts("/provide-evidence") + self.posts("/v1/shipping/trackers-batch"), [])

    def test_the_seller_changing_after_the_preview_stops_the_send(self):
        self.ready("case-ref-001")
        self.details["PP-D-SANDBOX01"]["disputed_transactions"][0]["seller"] = {"merchant_id": "OTHERACCOUNT9876"}
        for response in self.send_both():
            self.assertEqual(self.code(response), (409, "dispute_not_this_account"))
        self.assertEqual(self.posts("/provide-evidence") + self.posts("/v1/shipping/trackers-batch"), [])


class UnknownAccountTests(TwoDisputeHarness):
    MERCHANT_ID = ""

    def test_an_unknown_account_id_is_refused_and_previews_say_why(self):
        self.ready("case-ref-001")
        preview = self.post("/paypal/disputes/provide-evidence",
                            {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": False})
        self.assertEqual(preview.status_code, 200, preview.text)
        self.assertEqual((preview.json()["send_guard"]["account_status"], preview.json()["send_guard"]["send_refusal"],
                          preview.json()["send_guard"]["sending_account_masked"]), ("UNKNOWN", "account_identity_unknown", None))
        for route in ("provide-evidence", "add-tracking"):
            refused = self.post("/paypal/disputes/" + route,
                                {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True})
            self.assertEqual(self.code(refused), (409, "account_identity_unknown"))
        self.assertEqual(self.posts("/provide-evidence") + self.posts("/v1/shipping/trackers-batch"), [])

    def test_masks_show_only_the_first_two_and_last_four_characters(self):
        from app.paypal_disputes import mask_account, mask_dispute_id
        self.assertEqual(mask_account("ABCDEFGHIJ1234"), "AB\u20261234")
        self.assertEqual(mask_account("SHORT12"), "\u2026")
        self.assertIsNone(mask_account(None))
        self.assertEqual(mask_dispute_id("PP-D-SANDBOX02"), "PP-D-\u202602")


class EvidenceTypeTests(TwoDisputeHarness):
    """(r25 R3 P1-1) Only types the console can shape are sent; any other requested type is refused up front."""

    REFUND_REQUEST = {"evidence_type": "PROOF_OF_REFUND", "source": "REQUESTED_FROM_SELLER", "action": "PROVIDE_EVIDENCE"}

    def test_only_proof_of_fulfillment_is_supported(self):
        self.assertEqual(SUPPORTED_EVIDENCE_TYPES, frozenset({"PROOF_OF_FULFILLMENT"}))

    def test_a_dispute_asking_for_a_refund_is_refused_in_the_preview_and_the_send(self):
        self.details["PP-D-SANDBOX01"] = live_detail("PP-D-SANDBOX01", "TXNAAAA0001",
                                                     evidences=FIX[0]["evidences"] + [self.REFUND_REQUEST])
        self.ready("case-ref-001")
        for submit in (False, True):
            with self.subTest(submit=submit):
                refused = self.post("/paypal/disputes/provide-evidence",
                                    {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": submit})
                self.assertEqual(self.code(refused), (409, "evidence_type_not_supported"))
                self.assertIn("cannot send", refused.json()["error"]["message"])
                self.assertIn("Nothing was sent", refused.json()["error"]["message"])
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_the_dispute_changing_to_ask_for_a_refund_after_the_preview_stops_the_send(self):
        self.ready("case-ref-001")
        preview = self.post("/paypal/disputes/provide-evidence",
                            {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": False})
        self.assertEqual(preview.status_code, 200, preview.text)
        self.details["PP-D-SANDBOX01"]["evidences"] = FIX[0]["evidences"] + [self.REFUND_REQUEST]
        refused = self.post("/paypal/disputes/provide-evidence",
                            {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True})
        self.assertEqual(self.code(refused), (409, "evidence_type_not_supported"))
        self.assertEqual(self.posts("/provide-evidence"), [])

    def test_case_ref_003_asks_for_a_refund_and_is_refused_before_any_send(self):
        self.ready("case-ref-003")
        for submit in (False, True):
            with self.subTest(submit=submit):
                refused = self.post("/paypal/disputes/provide-evidence",
                                    {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-003", "submit": submit})
                self.assertEqual(self.code(refused), (409, "evidence_type_not_supported"))
        self.assertEqual(self.posts("/provide-evidence"), [])
        restricted = self.store.sessions[self.session_id].restricted_evidence["demo-case-003"]
        with self.assertRaises(BoundaryError) as raised:
            build_provide_evidence_request("PP-D-SANDBOX01", "case-ref-003", restricted, masked=True)
        self.assertEqual((raised.exception.status, raised.exception.code), (409, "evidence_type_not_supported"))

    def test_no_request_ever_carries_an_empty_or_non_fulfillment_evidence_info(self):
        restricted = {"requirements": [
            {"request_id": "r1", "provider_evidence_type": "PROOF_OF_FULFILLMENT", "evidence_type": "FULFILLMENT",
             "source": "REQUESTED_FROM_SELLER", "action": "PROVIDE_EVIDENCE", "requirement_state": "STRUCTURALLY_PRESENT"}],
            "proof_records": [{"request_id": "r1", "proof_fields": {"tracking_number": "SYNTHETIC_1", "carrier_name": "UPS"}}],
            "attachments": []}
        built = build_provide_evidence_request("PP-D-SANDBOX01", "case-ref-001", restricted, masked=True)
        self.assertEqual([row["evidence_type"] for row in built["input"]["evidences"]], ["PROOF_OF_FULFILLMENT"])
        self.assertTrue(all(row["evidence_info"]["tracking_info"] for row in built["input"]["evidences"]))
        other = deepcopy(restricted)
        other["requirements"].append({"request_id": "r2", "provider_evidence_type": "OTHER", "evidence_type": "OTHER",
                                      "source": "REQUESTED_FROM_SELLER", "action": "PROVIDE_EVIDENCE",
                                      "requirement_state": "STRUCTURALLY_PRESENT"})
        other["proof_records"].append({"request_id": "r2", "proof_fields": {"note": "synthetic"}})
        with self.assertRaises(BoundaryError) as raised:
            build_provide_evidence_request("PP-D-SANDBOX01", "case-ref-001", other, masked=True)
        self.assertEqual(raised.exception.code, "evidence_type_not_supported")
        fresh = {"status": "WAITING_FOR_SELLER_RESPONSE", "provide_evidence_link": True, "reason": "R",
                 "dispute_amount": {"currency_code": "USD", "value": "1.00"},
                 "evidences": [{"evidence_type": "PROOF_OF_FULFILLMENT", "source": "REQUESTED_FROM_SELLER"}]}
        empty = {"evidences": [{"evidence_type": "PROOF_OF_FULFILLMENT", "evidence_info": {"tracking_info": []}}]}
        self.assertEqual(submit_refusal(fresh, "R", {"currency_code": "USD", "value": "1.00"}, empty),
                         "evidence_type_not_supported")


class TrackerTransactionIdTests(unittest.TestCase):
    """(r25 R3 P2) tracker.transaction_id follows PayPal: ^[a-zA-Z0-9]*$, 1-50 characters."""

    RESTRICTED = {"proof_records": [{"proof_fields": {"tracking_number": "SYNTHETIC_1", "carrier_name": "UPS"}}]}

    def test_the_pattern_matches_paypal(self):
        self.assertEqual(build_tracking_request("A" * 50, self.RESTRICTED, masked=False)["body"]["trackers"][0]["transaction_id"],
                         "A" * 50)
        for bad in ("TXN-A", "TXN.A", "TXN_A", "A" * 51, "", "TXN A"):
            with self.subTest(transaction_id=bad):
                with self.assertRaises(BoundaryError) as raised:
                    build_tracking_request(bad, self.RESTRICTED, masked=False)
                self.assertEqual(raised.exception.code, "dispute_detail_required")

    def test_fixture_transaction_ids_fit_the_tracker_pattern(self):
        for dispute in fixture_disputes(Clock()()):
            self.assertIn(dispute["dispute_id"], FIXTURE_DISPUTE_IDS)
            for row in dispute["disputed_transactions"]:
                build_tracking_request(row["seller_transaction_id"], self.RESTRICTED, masked=True)


class StudioNonFiniteTests(unittest.TestCase):
    """(r25 R5 P2-1) Non-finite numbers in a Studio turn answer 422 studio_turn_invalid, never 500."""

    class NoModel:
        def __call__(self, payload):
            raise AssertionError("the model must not be called")

    def setUp(self):
        no_network(self)
        with clean_env():
            app = create_app(store=SessionStore(), studio_model=self.NoModel())
        self.client = TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55062),
                                 raise_server_exceptions=False)
        session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"],
                        "content-type": "application/json"}
        self.base = {"instructions": "Answer about the dashboard.", "items": [{"kind": "user", "text": "What is on the chart?"}],
                     "tools": [], "tool_choice": "auto", "response_format": {"type": "text"}}

    def send(self, body, raw_number=None):
        raw = json.dumps(body)
        if raw_number is not None:
            raw = raw.replace('"__NUMBER__"', raw_number)
        response = self.client.post(ROOT + "/studio/agent-turn", content=raw.encode(), headers=self.headers)
        return response.status_code, response.json()["error"]["code"]

    def test_overflowing_floats_and_nan_never_reach_the_route(self):
        # The shared parse refuses them first (r25 owner request: input_characters_refused on every route); a NaN
        # inside a call's arguments string reaches the Studio contract and is studio_turn_invalid.
        tool = deepcopy(self.base)
        tool["tools"] = [{"name": "t", "description": "d", "parameters": {"x": "__NUMBER__"}}]
        schema = deepcopy(self.base)
        schema["response_format"] = {"type": "json", "name": "f", "schema": {"x": "__NUMBER__"}}
        for number in ("1e400", "-1e400", "NaN", "Infinity"):
            with self.subTest(number=number):
                self.assertEqual(self.send(tool, number), (422, "input_characters_refused"))
                self.assertEqual(self.send(schema, number), (422, "input_characters_refused"))
        for arguments in ('{"a": NaN}', '{"a": 1e400}', '{"a": -Infinity}'):
            with self.subTest(arguments=arguments):
                call = deepcopy(self.base)
                call["items"] = [{"kind": "user", "text": "q?"},
                                 {"kind": "call", "call_id": "c1", "name": "t", "arguments": arguments}]
                self.assertEqual(self.send(call), (422, "studio_turn_invalid"))

    def test_the_validators_refuse_non_finite_values(self):
        for value in (float("inf"), float("-inf"), float("nan")):
            with self.assertRaises(sa.StudioAgentError):
                sa._depth({"x": [value]})
        with self.assertRaises(sa.StudioAgentError):
            sa._json_object('{"a": 1e400}', 1000)
        self.assertEqual(sa._json_object('{"a": 1.5}', 1000), {"a": 1.5})

    def test_a_canonical_json_failure_in_the_turn_is_studio_turn_invalid(self):
        service = sa.StudioAgentService(self.NoModel(), Governor(min_spacing=0))
        with patch.object(sa, "worker_request", side_effect=AiBriefError("ai_context_unavailable", 503)):
            with self.assertRaises(sa.StudioAgentError) as raised:
                service.turn("s" * 32, self.base)
        self.assertEqual(raised.exception.code, "studio_turn_invalid")


class HostedOriginTests(unittest.TestCase):
    """(r25 R5 P2-2) The hosted proxied mode accepts only https://<public host> as Origin; local mode is unchanged."""

    def setUp(self):
        no_network(self)
        with clean_env(PAYGUARD_DEMO_MODE="public", PAYGUARD_PUBLIC_HOST=PUBLIC):
            self.app = create_app()
        self.client = TestClient(self.app, base_url="https://" + PUBLIC, client=("10.20.0.5", 4000),
                                 raise_server_exceptions=False)

    @staticmethod
    def proxied(origin):
        return {"host": PUBLIC, "x-forwarded-proto": "https", "x-forwarded-for": "203.0.113.9", "origin": origin}

    def test_loopback_origins_are_refused_through_the_proxy(self):
        for origin in ("http://localhost:5173", "http://127.0.0.1:8000", "http://127.0.0.1:5173"):
            with self.subTest(origin=origin):
                preflight = self.client.options(ROOT + "/demo/sessions", headers=dict(
                    self.proxied(origin), **{"access-control-request-method": "POST"}))
                self.assertEqual(preflight.status_code, 403)
                self.assertNotIn("access-control-allow-origin", preflight.headers)
                created = self.client.post(ROOT + "/demo/sessions", json={}, headers=self.proxied(origin))
                self.assertEqual((created.status_code, created.json()["error"]["code"]), (403, "origin_rejected"))

    def test_the_public_origin_still_works(self):
        created = self.client.post(ROOT + "/demo/sessions", json={}, headers=self.proxied("https://" + PUBLIC))
        self.assertEqual(created.status_code, 201, created.text)
        self.assertEqual(created.headers.get("access-control-allow-origin"), "https://" + PUBLIC)

    def test_local_mode_keeps_the_loopback_origins(self):
        with clean_env():
            app = create_app()
        local = TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 1), raise_server_exceptions=False)
        created = local.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN})
        self.assertEqual(created.status_code, 201, created.text)
        self.assertEqual(created.headers.get("access-control-allow-origin"), ORIGIN)


class GuideGovernorTests(unittest.TestCase):
    """(r25 R5 P2-3, R1 P2-4) The guide passes a client id to the governor; the resend counts against the daily cap."""

    def test_governed_rows_apply_the_per_client_daily_cap_across_sessions(self):
        ticks = iter(range(0, 10 ** 6, 61))  # past the per-minute cap, well inside one day
        governor = Governor(clock=lambda: float(next(ticks)), min_spacing=0)
        calls = []

        def provider(request):
            calls.append(request)
            return json.dumps({"v": 2, "u": []})
        request = {"clauses": ["x"], "slots": ["ship_date"]}
        reasons = [governed_model_rows(governor, f"key-{index}", provider, request, "dispute", time.monotonic() + 30,
                                       client_id="local")[1]
                   for index in range(cf.CALLS_PER_CLIENT_PER_DAY + 3)]
        self.assertNotIn("budget", reasons[:cf.CALLS_PER_CLIENT_PER_DAY])
        self.assertEqual(reasons[cf.CALLS_PER_CLIENT_PER_DAY:], ["budget"] * 3)
        self.assertLessEqual(len(calls), 2 * cf.CALLS_PER_CLIENT_PER_DAY)
        other = governed_model_rows(governor, "key-other", provider, request, "dispute", time.monotonic() + 30,
                                    client_id="203.0.113.9")[1]
        self.assertNotEqual(other, "budget")

    def test_the_service_sends_the_session_client_key_or_local(self):
        seen = []

        class Recording(Governor):
            def admit(self, session_id, uses_model=True, client_id=None):
                seen.append(client_id)
                return super().admit(session_id, uses_model=uses_model, client_id=client_id)

        class Model:
            def __call__(self, request):
                return json.dumps({"v": 2, "u": []})

        store = SessionStore(clock=lambda: datetime(2026, 10, 30, 9, 0, tzinfo=timezone.utc))
        with clean_env():
            app = create_app(store=store)
        app.state.guide = GuideService(store, chooser_factory=lambda: Model(), governor=Recording(clock=lambda: 1000.0, min_spacing=0))
        client = TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55063))
        session = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        self.assertEqual(client.post(ROOT + "/guide/start", json={"scenario": "dispute", "goods_type": "physical"},
                                     headers=headers).status_code, 200)
        self.assertEqual(client.post(ROOT + "/guide/turn", json={"text": "the tracking number is saved somewhere"},
                                     headers=headers).status_code, 200)
        app.state.guide.wait_for_analysis()
        expected = store.sessions[session["session_id"]].client_key
        self.assertEqual(seen, [expected])
        self.assertTrue(expected)
        self.assertEqual(GuideService._client_id(object()), "local")

    def test_the_identical_resend_counts_against_the_global_daily_cap(self):
        governor = Governor(clock=lambda: 1000.0, min_spacing=0)
        governor._global_day = [1000.0] * (cf.GLOBAL_CALLS_PER_DAY - 1)
        self.assertTrue(governor.extra_attempt())
        self.assertEqual(len(governor._global_day), cf.GLOBAL_CALLS_PER_DAY)
        governor._global = []
        self.assertFalse(governor.extra_attempt())


class StudioPersonalDataTests(unittest.TestCase):
    """(r25 R1 P2-3) NFKC folding, spoken emails, plain phones and cards, and text split across items."""

    def turn(self, *results, question="Which cases are item not received?"):
        items = [{"kind": "user", "text": question}]
        for index, text in enumerate(results):
            items += [{"kind": "call", "call_id": f"c{index}", "name": "view_page", "arguments": "{}"},
                      {"kind": "result", "call_id": f"c{index}", "output": text}]
        return {"instructions": "You arrange a synthetic dashboard.", "items": items, "tools": [],
                "tool_choice": "auto", "response_format": {"type": "text"}}

    def refused(self, *results):
        with self.assertRaises(sa.StudioAgentError) as raised:
            sa.validate_turn(self.turn(*results))
        self.assertEqual(raised.exception.code, "studio_turn_personal_data")

    def test_hidden_personal_data_is_refused(self):
        for text in ("buyer jane.doe at example dot com", "jane (at) mail (dot) co (dot) uk", "buyer jane.doe＠example.com",
                     "jane.doe@exam​ple.com", "phone 5551234567", "call 15551234567", "call +886912345678",
                     "card 4222222222222", "card 4111111111111111", "card 6011000990139424", "card 378282246310005",
                     "card ４１１１１１１１１１１１１１１１"):
            with self.subTest(text=text):
                self.refused(text)

    def test_personal_data_split_across_items_is_refused(self):
        self.refused("jane.doe@", "example.com")
        self.refused("card 4111 1111", "1111 1111")
        self.refused("jane.doe at example", "dot com")

    def test_dashboard_questions_and_machine_text_still_pass(self):
        passing = ("How many cases are open?", "Total 125.50 USD across 3 cases; 48.00 is due on 2026-11-05",
                   "Look at the dot plot of days to due", "created 1730000000 and updated 1730000000123",
                   "order 2026103100 has 48.00", "id 20261031123456", "case-ref-001 has 2 of 3 items",
                   "tracking 1Z999AA10123456784 delivered", "Sum is 1234 and count 56", "Meet at noon, see the dot",
                   "amount 125.50 at 3 cases", "cases at risk: 2")
        for text in passing:
            with self.subTest(text=text):
                sa.validate_turn(self.turn(text))
        sa.validate_turn(self.turn("count 12", "345 cases", "1730000000", "123"))
        for question in ("How many disputes are due this week?", "What is the total amount in USD for open cases?",
                         "Show cases with amount over 100"):
            with self.subTest(question=question):
                sa.validate_turn(self.turn(question=question))



class InputLockTests(unittest.TestCase):
    """(r25 owner request) The shared JSON parse refuses special characters and non-plain numbers on every route."""

    def setUp(self):
        no_network(self)
        with clean_env():
            self.app = create_app(store=SessionStore())
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55064),
                                 raise_server_exceptions=False)
        session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"],
                        "content-type": "application/json"}

    def raw(self, route, text):
        return self.client.post(ROOT + route, content=text.encode("utf-8"), headers=self.headers)

    def refused(self, route, text):
        response = self.raw(route, text)
        self.assertEqual((response.status_code, response.json()["error"]["code"]), (422, "input_characters_refused"), text)
        self.assertIn("does not accept", response.json()["error"]["message"])

    def test_every_refused_character_class(self):
        samples = {"NUL": "\\u0000", "bell": "\\u0007", "vertical tab": "\\u000b", "escape": "\\u001b", "DEL": "\\u007f",
                   "C1": "\\u0085", "C1 end": "\\u009f", "LRE": "\\u202a", "RLO": "\\u202e", "LRI": "\\u2066",
                   "PDI": "\\u2069", "ZWSP": "\\u200b", "ZWNJ": "\\u200c", "ZWJ": "\\u200d", "word joiner": "\\u2060",
                   "BOM": "\\ufeff", "lone high surrogate": "\\ud800", "lone low surrogate": "\\udfff"}
        for label, escape in samples.items():
            with self.subTest(label=label):
                self.refused("/aup/review", '{"description": "Ceramic cup' + escape + ' set"}')
                self.refused("/aup/review", '{"description": ["a' + escape + '"]}')  # inside an array
                self.refused("/aup/review", '{"descr' + escape + 'iption": "Ceramic cup"}')  # in a key
                self.refused("/studio/agent-turn", '{"instructions": "x' + escape + '"}')
        # A raw (unescaped) bidi override and zero-width space too.
        self.refused("/aup/review", json.dumps({"description": "cup \u202e set"}, ensure_ascii=False))
        self.refused("/aup/review", json.dumps({"description": "cup\u200bset"}, ensure_ascii=False))

    def test_numbers_are_plain_digits_with_an_optional_decimal_point(self):
        for number in ("1e3", "1E400", "-1e400", "2E-5", "1.5e2", "+5", "NaN", "Infinity", "-Infinity", "0x10",
                       "1234567890123456", "1.1234567", ".5", "1.", "012"):
            with self.subTest(number=number):
                self.refused("/demo/inject", '{"scenario": "dispute", "x": ' + number + '}')
                self.refused("/demo/inject", '{"scenario": "dispute", "x": [' + number + ']}')
        for number in ("12.50", "1500", "0", "-3", "123456789012345", "0.123456"):
            with self.subTest(number=number):
                response = self.raw("/demo/inject", '{"scenario": "dispute", "x": ' + number + '}')
                self.assertEqual((response.status_code, response.json()["error"]["code"]), (422, "schema_invalid"))

    def test_normal_text_still_passes(self):
        for text in ("Caf\u00e9 cr\u00e8me br\u00fbl\u00e9e cups, na\u00efve design", "Price \u20ac12.50, \u00a31500, \u00a5300, NT$1,500, $48.00",
                     "Tom's \"best\" mugs - 2/pack & gift box (blue)",
                     "C\u00f4te d'Ivoire, S\u00e3o Tom\u00e9, \u00c5land, M\u00fcnchen", "\u65e5\u672c\u306e\u6e6f\u98f2\u307f"):
            with self.subTest(text=text):
                response = self.client.post(ROOT + "/aup/review", json={"description": text}, headers=self.headers)
                self.assertEqual(response.status_code, 200, response.text)
        # Studio's own instructions carry newlines and are accepted by the parse.
        from app.main import parse_locked_json
        self.assertEqual(parse_locked_json('{"instructions": "## Role\\nYou are the Orchestrator.\\n", "n": 12.50}'),
                         {"instructions": "## Role\nYou are the Orchestrator.\n", "n": 12.5})
        # Tab, newline and carriage return are kept by the parse (a route may still apply its own text rule).
        self.assertEqual(parse_locked_json('{"t": "Line one\\nTwo\\tTabbed\\r\\nEnd"}'), {"t": "Line one\nTwo\tTabbed\r\nEnd"})
        self.assertEqual(parse_locked_json('{"limit": 1500, "list": [1, -2, 0.5]}'), {"limit": 1500, "list": [1, -2, 0.5]})

    def test_country_amounts_follow_the_currency_decimal_rule(self):
        from app.country_routes import CountryRulesCheckRequest
        base = {"seller_country": "US", "buyer_country": "TW"}
        for amount, currency in (("1500", "TWD"), ("12.50", "USD"), ("48", "USD"), ("300", "JPY")):
            CountryRulesCheckRequest(**base, amount=amount, currency=currency)
        for amount, currency in (("12.50", "TWD"), ("1500.00", "JPY"), ("1.5", "HUF"), ("1e3", "USD"), ("+5", "USD"),
                                 ("12.505", "USD")):
            with self.subTest(amount=amount, currency=currency):
                with self.assertRaises(ValueError):
                    CountryRulesCheckRequest(**base, amount=amount, currency=currency)


if __name__ == "__main__":
    unittest.main()
