"""Hosted demo with PAYGUARD_HOSTED_SANDBOX_SEND=enabled (owner decision 2026-11-10): real Sandbox evidence sends.

Every provider reply is a synthetic MockTransport answer that records each request. The checks: the switch fails
closed (unknown values and a send switch without the read-only switch stop startup), only provide-evidence opens,
every local send guard still applies, one send per dispute (server memory and PayPal's own state), one send per visitor
session, the shared window and daily caps answer 429, no visitor text reaches PayPal, ids stay masked, and the
console is told when nothing is left to send so it can offer the recorded replay.
"""

import asyncio
import json
import os
from pathlib import Path
import re
import unittest
from unittest import mock

from fastapi.testclient import TestClient
import httpx

from app import demo_mode
from app.demo_mode import (HOSTED_DEMO_CODE, HOSTED_SEND_BUDGET_CODE, HOSTED_SEND_SESSION, HOSTED_SEND_SESSION_CODE,
                           DemoModeConfigError, HostedReadOnlyPaypalAdapter, SendBudget, disabled_routes,
                           hosted_send_enabled)
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import BoundaryError, SessionStore
from test_paypal_disputes import FIX, Clock

ROOT = "/api/v1"
PUBLIC = "payguard-demo.onrender.com"
ORIGIN = "https://" + PUBLIC
PUBLIC_ENV = {"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": PUBLIC}
READONLY_ENV = dict(PUBLIC_ENV, PAYGUARD_HOSTED_READONLY_SANDBOX="enabled")
SEND_ENV = dict(READONLY_ENV, PAYGUARD_HOSTED_SANDBOX_SEND="enabled")
REAL_IDS = ("PP-D-SANDBOX01", "PP-D-SANDBOX02", "PP-D-SANDBOX03")
STILL_SHUT = ("/paypal/invoices/draft", "/paypal/disputes/add-tracking", "/paypal/webhooks/verify",
              "/ai/evidence-brief", "/studio/agent-turn")
FIXED_NOTE = "Shipment tracking for this order, provided by the seller."
DEBUG_ID = "f2088142a6218"


def env(**values):
    base = {key: value for key, value in os.environ.items()
            if not key.startswith(("PAYGUARD_DEMO", "PAYGUARD_PUBLIC", "PAYGUARD_HOSTED"))}
    base.update(values)
    return mock.patch.dict(os.environ, base, clear=True)


def submittable(dispute_id, **changes):
    """A dispute PayPal would accept evidence for: waiting for the seller, a provide_evidence link (PayPal docs r24)."""
    return dict(FIX[0], dispute_id=dispute_id, links=[
        {"href": f"https://api-m.sandbox.paypal.com/v1/customer/disputes/{dispute_id}/provide-evidence",
         "rel": "provide_evidence", "method": "POST"}], **changes)


class Provider:
    """Records every request; answers OAuth, the list, details and provide-evidence like the Sandbox would."""

    def __init__(self):
        self.calls = []
        self.answered = set()  # real ids PayPal already holds seller evidence for
        self.late = set()  # real ids still waiting for the seller but already listing seller evidence (red team P2-2)

    def __call__(self, request):
        request.read()
        self.calls.append(request)
        path = request.url.path
        if path == "/v1/oauth2/token" and request.method == "POST":
            return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
        if request.method == "GET" and path == "/v1/customer/disputes":
            return httpx.Response(200, json={"items": [
                dict(FIX[0], dispute_id=real, status="WAITING_FOR_BUYER_RESPONSE" if real in self.answered
                     else "WAITING_FOR_SELLER_RESPONSE") for real in REAL_IDS]})
        if request.method == "GET" and path.startswith("/v1/customer/disputes/PP-"):
            real = path.rsplit("/", 1)[1]
            if real in self.answered:
                return httpx.Response(200, json=dict(FIX[0], dispute_id=real, status="WAITING_FOR_BUYER_RESPONSE"))
            if real in self.late:
                evidences = FIX[0]["evidences"] + [{"evidence_type": "PROOF_OF_FULFILLMENT", "source": "SUBMITTED_BY_SELLER",
                                                    "date": FIX[0]["evidences"][0]["date"]}]
                return httpx.Response(200, json=submittable(real, evidences=evidences))
            return httpx.Response(200, json=submittable(real), headers={"PayPal-Debug-Id": "ca5554cf42ef6"})
        if request.method == "POST" and path.endswith("/provide-evidence"):
            self.answered.add(path.split("/")[-2])
            return httpx.Response(200, json={"links": []}, headers={"PayPal-Debug-Id": DEBUG_ID})
        return httpx.Response(500, json={})

    def sends(self):
        return [call for call in self.calls if call.method == "POST" and call.url.path.endswith("/provide-evidence")]


def make_inner(provider, *, submit=True, merchant_id="SYNTHETICMERCHANT"):
    return PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "", submit, False,
                                                            merchant_id=merchant_id),
                         transport=httpx.MockTransport(provider), clock=Clock())


class ConfigMatrix(unittest.TestCase):
    def test_switch_is_off_without_public_mode_whatever_its_value(self):
        for value in ("", "off", "enabled", "yes", "ENABLED"):
            self.assertIs(hosted_send_enabled({"PAYGUARD_HOSTED_SANDBOX_SEND": value}), False, value)
            self.assertIs(hosted_send_enabled({"PAYGUARD_DEMO_MODE": "off", "PAYGUARD_HOSTED_SANDBOX_SEND": value,
                                               "PAYGUARD_HOSTED_READONLY_SANDBOX": "enabled"}), False, value)

    def test_public_mode_values(self):
        self.assertIs(hosted_send_enabled(dict(READONLY_ENV)), False)
        self.assertIs(hosted_send_enabled(dict(READONLY_ENV, PAYGUARD_HOSTED_SANDBOX_SEND="off")), False)
        self.assertIs(hosted_send_enabled(dict(SEND_ENV)), True)
        for value in ("yes", "ENABLED", " enabled", "enabled ", "true", "1", "on"):
            with self.assertRaises(DemoModeConfigError, msg=value):
                hosted_send_enabled(dict(READONLY_ENV, PAYGUARD_HOSTED_SANDBOX_SEND=value))
        # The send switch without the read-only switch (unset or off) fails closed instead of being silently ignored.
        for readonly in ("", "off"):
            with self.assertRaises(DemoModeConfigError, msg=readonly):
                hosted_send_enabled(dict(PUBLIC_ENV, PAYGUARD_HOSTED_READONLY_SANDBOX=readonly,
                                         PAYGUARD_HOSTED_SANDBOX_SEND="enabled"))

    def test_create_app_refuses_to_start_on_a_bad_send_value(self):
        for extra in ({"PAYGUARD_HOSTED_SANDBOX_SEND": "maybe"},
                      {"PAYGUARD_HOSTED_SANDBOX_SEND": "enabled", "PAYGUARD_HOSTED_READONLY_SANDBOX": ""}):
            values = dict(READONLY_ENV)
            values.update(extra)
            with env(**values), self.assertRaises(DemoModeConfigError):
                create_app(store=SessionStore(), hosted_sandbox_inner=make_inner(Provider()))

    def test_local_mode_ignores_the_switch(self):
        with env(PAYGUARD_HOSTED_SANDBOX_SEND="enabled"):
            app = create_app(store=SessionStore(), paypal=make_inner(Provider()))
        self.assertIs(app.state.hosted_send, False)

    def test_all_hosted_opt_ins_start_together_and_the_guide_stays_open(self):
        values = dict(SEND_ENV, PAYGUARD_HOSTED_GUIDE_MODEL="gemini", PAYGUARD_GUIDE_MODEL="gemini",
                      PAYGUARD_GEMINI_TRANSPORT="api_key", GEMINI_API_KEY="synthetic-not-a-key")
        with env(**values), mock.patch("app.guide_routes.select_guide_chooser", return_value=object()):
            app = create_app(store=SessionStore(), hosted_sandbox_inner=make_inner(Provider()))
            self.assertIsNotNone(app.state.guide.chooser_factory(), "hosted Gemini guide still on with the send switch")
        self.assertEqual((app.state.hosted_readonly, app.state.hosted_send), (True, True))
        self.assertFalse(any("/guide/" in path for _method, path in disabled_routes(True, True)))

    def test_route_table(self):
        shut = {path for _method, path in disabled_routes(True, True)}
        self.assertNotIn("/api/v1/paypal/disputes/provide-evidence", shut)
        self.assertNotIn("/api/v1/paypal/connect", shut)
        for route in STILL_SHUT:
            self.assertIn("/api/v1" + route, shut)
        # The send flag alone never opens anything: without the read-only switch every route stays shut.
        self.assertEqual(disabled_routes(False, True), disabled_routes(False, False))
        self.assertIn(("POST", "/api/v1/paypal/disputes/provide-evidence"), disabled_routes(True, False))


class HostedSendBase(unittest.TestCase):
    environment = SEND_ENV

    def setUp(self):
        for target in ("socket.socket.connect", "socket.create_connection"):
            guard = mock.patch(target, side_effect=AssertionError("network forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        self.provider = Provider()
        patcher = env(**self.environment)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.app = create_app(store=SessionStore(), hosted_sandbox_inner=make_inner(self.provider))
        self.client = TestClient(self.app, base_url=ORIGIN, client=("10.0.0.5", 40000), raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.visitors = 0
        self.headers = self.new_session()
        hold = mock.patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0)
        hold.start()
        self.addCleanup(hold.stop)

    def new_session(self):
        self.visitors += 1
        proxy = {"X-Forwarded-For": f"198.51.100.{self.visitors}", "X-Forwarded-Proto": "https"}
        session = self.client.post(ROOT + "/demo/sessions", json={}, headers=dict(proxy, Origin=ORIGIN)).json()
        return dict(proxy, Origin=ORIGIN, **{"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})

    def get(self, route, headers=None):
        return self.client.get(ROOT + route, headers=headers or self.headers)

    def post(self, route, body=None, headers=None):
        return self.client.post(ROOT + route, json={} if body is None else body, headers=headers or self.headers)

    def codes(self, headers=None):
        listing = self.get("/paypal/disputes", headers)
        self.assertEqual(listing.status_code, 200, listing.text)
        return [row["dispute_id"] for row in listing.json()["items"]]

    def prepare(self, code, headers=None):
        """Connect, load the synthetic case, read the dispute, draft and record the local review (human step one)."""
        headers = headers or self.headers
        self.assertEqual(self.post("/paypal/connect", headers=headers).status_code, 200)
        self.post("/demo/inject", {"scenario": "dispute"}, headers)
        self.assertEqual(self.get("/paypal/disputes/" + code, headers).status_code, 200)
        draft = self.post("/disputes/case-ref-001/draft", headers=headers).json()
        approval = self.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}, headers)
        self.assertEqual(approval.status_code, 200, approval.text)

    def send(self, code, headers=None):
        """Preview (issues the dialog's confirmation), then the confirmed send (human step two)."""
        headers = headers or self.headers
        body = {"dispute_id": code, "case_ref": "case-ref-001"}
        preview = self.post("/paypal/disputes/provide-evidence", dict(body, submit=False), headers)
        token = preview.json().get("confirm_token") if preview.status_code == 200 else None
        payload = dict(body, submit=True)
        if token:
            payload["confirm_token"] = token
        return self.post("/paypal/disputes/provide-evidence", payload, headers)


class RouteOpensOnlyWithBothSwitches(HostedSendBase):
    def test_provide_evidence_reaches_the_service_and_the_rest_stay_503(self):
        refused = self.post("/paypal/disputes/provide-evidence", {"dispute_id": "PP-D-XXXXOX01", "case_ref": "case-ref-001"})
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (404, "dispute_not_found"))
        for route in STILL_SHUT:
            response = self.post(route, {"dispute_id": "PP-D-SANDBOX01"})
            self.assertEqual((response.status_code, response.json()["error"]["code"]), (503, HOSTED_DEMO_CODE), route)
        self.assertEqual(self.provider.calls, [])

    def test_connections_reports_send_and_counts_only(self):
        body = self.get("/connections").json()
        self.assertEqual(body, {"mode": "hosted_demo", "sandbox_reads": True, "sandbox_send": True,
                                "send_state": {"sends_left_window": 3, "sends_left_day": 15, "window_minutes": 10,
                                               "disputes_sent": 0}})


class ReadOnlyKeepsSendShut(HostedSendBase):
    environment = READONLY_ENV

    def test_read_only_switch_alone_keeps_provide_evidence_503(self):
        response = self.post("/paypal/disputes/provide-evidence", {"dispute_id": "PP-D-XXXXOX01", "case_ref": "case-ref-001",
                                                                   "submit": True})
        self.assertEqual((response.status_code, response.json()["error"]["code"]), (503, HOSTED_DEMO_CODE))
        self.assertEqual(self.get("/connections").json(), {"mode": "hosted_demo", "sandbox_reads": True})
        self.assertIs(self.app.state.paypal.dispute_submit_enabled(), False)


class FullSend(HostedSendBase):
    def test_send_after_two_human_steps_shows_submitted_and_debug_id_with_masked_ids(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.assertNotIn(code, REAL_IDS)
        self.prepare(code)
        sent = self.send(code)
        self.assertEqual(sent.status_code, 200, sent.text)
        body = sent.json()
        self.assertEqual((body["external_send"], body["readback"], body["provider_submission"]),
                         ("SUBMITTED", "PROVIDE_EVIDENCE_SUBMITTED", "PERFORMED"))
        self.assertEqual(body["paypal_debug_id"], DEBUG_ID)
        self.assertEqual(body["dispute_id"], code)
        self.assertEqual(body["path"], f"/v1/customer/disputes/{code}/provide-evidence")
        self.assertEqual([call.url.path for call in self.provider.sends()], ["/v1/customer/disputes/PP-D-SANDBOX01/provide-evidence"])
        for real in REAL_IDS:
            self.assertNotIn(real, sent.text)
        # Read-back after the send: PayPal now waits for the buyer, the code still opens the case, still masked.
        readback = self.get("/paypal/disputes/" + code)
        self.assertEqual((readback.status_code, readback.json()["status"]), (200, "WAITING_FOR_BUYER_RESPONSE"))
        self.assertNotIn("PP-D-SANDBOX01", readback.text)
        self.assertEqual(self.get("/connections").json()["send_state"]["disputes_sent"], 1)

    def test_no_send_without_the_local_review_or_the_confirmation(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.post("/demo/inject", {"scenario": "dispute"})
        self.get("/paypal/disputes/" + code)
        self.post("/disputes/case-ref-001/draft")
        unreviewed = self.send(code)
        self.assertEqual((unreviewed.status_code, unreviewed.json()["error"]["code"]), (422, "approval_required"))
        draft = self.post("/disputes/case-ref-001/draft").json()
        self.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]})
        unconfirmed = self.post("/paypal/disputes/provide-evidence",
                                {"dispute_id": code, "case_ref": "case-ref-001", "submit": True})
        self.assertEqual((unconfirmed.status_code, unconfirmed.json()["error"]["code"]), (409, "confirmation_required"))
        self.assertEqual(self.provider.sends(), [])

    def test_account_check_still_applies(self):
        self.app.state.paypal._inner.config_loader = lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "",
                                                                          True, False, merchant_id="OTHERMERCHANT01")
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.prepare(code)
        refused = self.send(code)
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "dispute_not_this_account"))
        self.assertEqual(self.provider.sends(), [])

    def test_inner_submit_flag_off_keeps_the_send_frozen(self):
        self.app.state.paypal._inner.config_loader = lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "",
                                                                          False, False, merchant_id="SYNTHETICMERCHANT")
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.prepare(code)
        refused = self.send(code)
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (503, "provider_action_frozen"))
        self.assertEqual(self.provider.sends(), [])


class NoVisitorText(HostedSendBase):
    def test_extra_fields_are_refused_and_only_the_apps_own_records_reach_paypal(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.prepare(code)
        for extra in ({"note": "visitor text"}, {"notes": "x"}, {"evidences": []}, {"tracking_number": "1Z999"}):
            refused = self.post("/paypal/disputes/provide-evidence",
                                dict({"dispute_id": code, "case_ref": "case-ref-001", "submit": True}, **extra))
            self.assertEqual(refused.status_code, 422, extra)
        self.assertEqual(self.provider.sends(), [])
        self.assertEqual(self.send(code).status_code, 200)
        posted = self.provider.sends()[0]
        content = posted.content.decode("latin-1")
        start = content.index('{"evidences"')
        document = json.loads(content[start:content.index("\r\n", start)])
        self.assertEqual(document, {"evidences": [{
            "evidence_type": "PROOF_OF_FULFILLMENT",
            "evidence_info": {"tracking_info": [{"carrier_name": "OTHER", "carrier_name_other": "SYNTHETIC_CARRIER",
                                                 "tracking_number": "SYNTHETIC_TRACKING_001"}]},
            "notes": FIXED_NOTE}]})


class OncePerDispute(HostedSendBase):
    def test_server_memory_refuses_a_second_send_even_when_paypal_still_waits(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.prepare(code)
        self.assertEqual(self.send(code).status_code, 200)
        # PayPal state reverted (simulated lag): only server memory stands between a second visitor and a second send.
        self.provider.answered.clear()
        other = self.new_session()
        self.prepare(code, other)
        again = self.send(code, other)
        self.assertEqual((again.status_code, again.json()["error"]["code"]), (409, "evidence_already_submitted"))
        self.assertEqual(len(self.provider.sends()), 1)

    def test_paypal_state_refuses_a_dispute_no_longer_waiting_for_the_seller(self):
        self.provider.answered.add("PP-D-SANDBOX02")
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[1]
        self.prepare(code)
        refused = self.send(code)
        self.assertEqual(refused.status_code, 409, refused.text)
        self.assertIn(refused.json()["error"]["code"], {"dispute_not_awaiting_seller", "confirmation_required"})
        self.assertEqual(self.provider.sends(), [])
        listing = self.get("/paypal/disputes").json()["items"]
        self.assertEqual([row["status"] for row in listing].count("WAITING_FOR_SELLER_RESPONSE"), 2)


class SellerEvidenceAtTheFreshRead(HostedSendBase):
    """(red team 2026-11-10 P2-2) Seller evidence that appears after the preview stops the send at the fresh read."""

    def test_seller_evidence_listed_after_the_preview_refuses_with_409_and_nothing_is_sent(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        code = self.codes()[0]
        self.prepare(code)
        preview = self.post("/paypal/disputes/provide-evidence", {"dispute_id": code, "case_ref": "case-ref-001", "submit": False})
        self.assertEqual(preview.status_code, 200, preview.text)
        self.provider.late.add("PP-D-SANDBOX01")  # still WAITING_FOR_SELLER_RESPONSE, upload still offered
        refused = self.post("/paypal/disputes/provide-evidence", {"dispute_id": code, "case_ref": "case-ref-001", "submit": True,
                                                                  "confirm_token": preview.json()["confirm_token"]})
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "seller_evidence_already_submitted"))
        self.assertEqual(self.provider.sends(), [])

    def test_submit_refusal_names_seller_evidence(self):
        from app.paypal_disputes import submit_refusal
        fresh = {"status": "WAITING_FOR_SELLER_RESPONSE", "provide_evidence_link": True,
                 "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "dispute_amount": {"currency_code": "USD", "value": "48.00"},
                 "evidences": [{"evidence_type": "PROOF_OF_FULFILLMENT", "source": "SUBMITTED_BY_SELLER"}]}
        self.assertEqual(submit_refusal(fresh, "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", {"currency_code": "USD", "value": "48.00"},
                                        {"evidences": []}), "seller_evidence_already_submitted")


class OncePerSession(HostedSendBase):
    def test_reset_demo_does_not_give_a_visit_a_second_send(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        first, second = self.codes()[:2]
        self.prepare(first)
        self.assertEqual(self.send(first).status_code, 200)
        self.post("/demo/inject", {"scenario": "reset"})
        self.prepare(second)
        again = self.send(second)
        self.assertEqual((again.status_code, again.json()["error"]["code"]), (409, HOSTED_SEND_SESSION_CODE))
        self.assertIn("recorded replay", again.json()["error"]["message"])
        self.assertEqual(len(self.provider.sends()), 1)


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class Caps(HostedSendBase):
    def test_window_and_day_caps_answer_429_and_recover(self):
        clock = FakeClock()
        self.app.state.paypal._send_budget = SendBudget(per_window=1, window=600, per_day=2, clock=clock)
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        first, second, third = self.codes()
        self.prepare(first)
        self.assertEqual(self.send(first).status_code, 200)
        visitor_b = self.new_session()
        self.prepare(second, visitor_b)
        capped = self.send(second, visitor_b)
        self.assertEqual((capped.status_code, capped.json()["error"]["code"]), (429, HOSTED_SEND_BUDGET_CODE))
        self.assertIn("Retry-After", capped.headers)
        self.assertEqual(self.get("/connections", visitor_b).json()["send_state"]["sends_left_window"], 0)
        clock.now += 601
        visitor_c = self.new_session()
        self.prepare(second, visitor_c)
        self.assertEqual(self.send(second, visitor_c).status_code, 200)
        clock.now += 601
        visitor_d = self.new_session()
        self.prepare(third, visitor_d)
        day = self.send(third, visitor_d)
        self.assertEqual((day.status_code, day.json()["error"]["code"]), (429, HOSTED_SEND_BUDGET_CODE))
        state = self.get("/connections", visitor_d).json()["send_state"]
        self.assertEqual((state["sends_left_day"], state["disputes_sent"]), (0, 2))
        self.assertEqual(len(self.provider.sends()), 2)


class WrapperRefusals(unittest.TestCase):
    def test_send_outside_a_visitor_request_or_with_the_switch_off_never_reaches_the_transport(self):
        provider = Provider()

        async def attempt(wrapper):
            await wrapper.connect()
            code = (await wrapper.list_disputes())[0]["dispute_id"]
            with self.assertRaises(BoundaryError) as caught:
                await wrapper.provide_evidence(code, {"input": (None, "{}", "application/json")})
            self.assertEqual((caught.exception.status, caught.exception.code), (503, HOSTED_DEMO_CODE))
            marker = HOSTED_SEND_SESSION.set("visitor-session")
            # (red team A1) A visitor send also carries its client key; without one it is refused like no session.
            client_marker = demo_mode.HOSTED_SEND_CLIENT.set("203.0.113.1")
            try:
                with self.assertRaises(BoundaryError) as caught:
                    await wrapper.provide_evidence("PP-D-SANDBOX01", {"input": (None, "{}", "application/json")})
            finally:
                demo_mode.HOSTED_SEND_CLIENT.reset(client_marker)
                HOSTED_SEND_SESSION.reset(marker)
            return caught.exception

        asyncio.run(attempt(HostedReadOnlyPaypalAdapter(make_inner(provider))))  # switch off: 503 both times
        refused = asyncio.run(attempt(HostedReadOnlyPaypalAdapter(make_inner(provider), send_enabled=True)))
        # Switch on but no visitor session: 503; a real id instead of a handed-out code: 404, never sent.
        self.assertEqual((refused.status, refused.code), (404, "dispute_not_found"))
        self.assertEqual(provider.sends(), [])


class DocsAgreeWithCode(unittest.TestCase):
    """README, SECURITY and render.yaml state the send opt-in, its caps and no longer say the hosted demo never sends."""

    ROOT = Path(__file__).resolve().parents[1]
    STALE = ("only reads and never sends", "its only paypal calls are read-only", "do not add paypal or google cloud",
             "the hosted demo refuses all writes", "it makes no paypal write", "the hosted page can only read the sandbox",
             "still sends nothing to paypal: its only paypal calls are reads")

    def text(self, name):
        return re.sub(r"\s+", " ", (self.ROOT / name).read_text(encoding="utf-8")).casefold()

    def test_caps_in_code_match_the_docs(self):
        self.assertEqual((demo_mode.HOSTED_SENDS_PER_WINDOW, demo_mode.HOSTED_SEND_WINDOW_SECONDS, demo_mode.HOSTED_SENDS_PER_DAY),
                         (3, 600, 15), "change README, SECURITY and render.yaml with the caps")
        for name in ("README.md", "SECURITY.md", "render.yaml"):
            text = self.text(name)
            with self.subTest(name=name):
                self.assertIn("payguard_hosted_sandbox_send=enabled", text)
                self.assertIn("3 per 10 minutes", text)
                self.assertIn("15 a day", text)
                for phrase in self.STALE:
                    self.assertNotIn(phrase, text)

    def test_start_page_quickstart_and_llms_txt_match_the_send_opt_in(self):
        # (cross-check v3 C2/C3, red team P2-4) The judge start page and quickstart no longer say every write is refused.
        stale = self.STALE + ("every write is refused", "the hosted site is read-only", "its only paypal calls are",
                              "two human steps", "nothing is sent to paypal from the hosted site")
        from app.main import LLMS_TXT
        texts = {name: self.text(name) for name in ("frontend/public/start.html", "docs/submission/quickstart.md",
                                                    "README.md", "SECURITY.md")}
        texts["llms.txt"] = re.sub(r"\s+", " ", LLMS_TXT).casefold()
        texts["hostedCopy.js"] = self.text("frontend/src/hostedCopy.js")
        for name, text in texts.items():
            with self.subTest(name=name):
                self.assertIn("at most 2 sends per address per day", text)
                for phrase in stale:
                    self.assertNotIn(phrase, text)
        self.assertEqual(demo_mode.HOSTED_SENDS_PER_CLIENT_PER_DAY, 2, "change the docs with the address cap")

    def test_render_declares_the_sandbox_keys_without_values(self):
        blueprint = (self.ROOT / "render.yaml").read_text(encoding="utf-8")
        for key in ("PAYGUARD_PAYPAL_OUTBOUND", "PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET", "PAYGUARD_PAYPAL_SANDBOX_MERCHANT_ID",
                    "PAYGUARD_PAYPAL_DISPUTE_SUBMIT", "PAYGUARD_HOSTED_READONLY_SANDBOX", "PAYGUARD_HOSTED_SANDBOX_SEND"):
            with self.subTest(key=key):
                block = re.search(rf"^      - key: {key}\n((?:        .*\n)+)", blueprint, re.MULTILINE)
                self.assertIsNotNone(block, f"{key} declared")
                self.assertEqual(block.group(1).strip(), "sync: false")
        self.assertIn("never put live (production) paypal credentials", blueprint.casefold())


if __name__ == "__main__":
    unittest.main()
