"""Hosted demo with PAYGUARD_HOSTED_READONLY_SANDBOX=enabled: real READ-ONLY Sandbox calls, no writes, ever.

Every provider reply is a synthetic MockTransport answer that records (method, path). The adversarial checks:
every write route answers 503 on the hosted app, the wrapper has no write method that reaches the transport,
the only POST that ever leaves is the OAuth token request, the shared read budget answers 429 and recovers,
the flag does nothing without public mode, and with the flag off the hosted demo is exactly as before.
"""

import asyncio
import os
import unittest
from unittest import mock

from fastapi.testclient import TestClient
import httpx

from app import demo_mode
from app.demo_mode import (DISABLED_ROUTES, HOSTED_DEMO_CODE, HOSTED_READ_BUDGET_CODE, DemoModeConfigError,
                           HostedDemoPaypalStub, HostedReadOnlyPaypalAdapter, ReadBudget, hosted_readonly_enabled)
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import BoundaryError, SessionStore
from test_paypal_disputes import Clock, sandbox_detail_reply, sandbox_list_reply

ROOT = "/api/v1"
PUBLIC = "payguard-demo.onrender.com"
ORIGIN = "https://" + PUBLIC
PROXY = {"X-Forwarded-For": "198.51.100.7", "X-Forwarded-Proto": "https"}
PUBLIC_ENV = {"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": PUBLIC}
READONLY_ENV = dict(PUBLIC_ENV, PAYGUARD_HOSTED_READONLY_SANDBOX="enabled")
WRITE_ROUTES = ("/paypal/invoices/draft", "/paypal/disputes/provide-evidence", "/paypal/disputes/add-tracking",
                "/paypal/webhooks/verify", "/ai/evidence-brief", "/studio/agent-turn")


def env(**values):
    base = {key: value for key, value in os.environ.items() if not key.startswith(("PAYGUARD_DEMO", "PAYGUARD_PUBLIC", "PAYGUARD_HOSTED"))}
    base.update(values)
    return mock.patch.dict(os.environ, base, clear=True)


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class Recorder:
    """A MockTransport handler that records every request and answers only the OAuth token and two GETs."""

    def __init__(self):
        self.calls = []

    def __call__(self, request):
        request.read()
        self.calls.append((request.method, request.url.path))
        if request.url.path == "/v1/oauth2/token" and request.method == "POST":
            return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
        if request.method == "GET" and request.url.path == "/v1/customer/disputes":
            return httpx.Response(200, json=sandbox_list_reply())
        if request.method == "GET" and request.url.path.startswith("/v1/customer/disputes/PP-"):
            return httpx.Response(200, json=sandbox_detail_reply(request.url.path.rsplit("/", 1)[1]))
        return httpx.Response(500, json={})

    def posts(self):
        return [call for call in self.calls if call[0] != "GET"]


def make_inner(recorder, *, submit=True):
    return PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret", "", submit, submit,
                                                            merchant_id="SYNTHETICMERCHANT"),
                         transport=httpx.MockTransport(recorder), clock=Clock())


class HostedReadOnlyBase(unittest.TestCase):
    environment = READONLY_ENV

    def setUp(self):
        self.recorder = Recorder()
        patcher = env(**self.environment)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.app = create_app(store=SessionStore(), hosted_sandbox_inner=make_inner(self.recorder))
        self.client = TestClient(self.app, base_url=ORIGIN, client=("10.0.0.5", 40000), raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        session = self.client.post(ROOT + "/demo/sessions", json={}, headers=dict(PROXY, Origin=ORIGIN)).json()
        self.headers = dict(PROXY, Origin=ORIGIN, **{"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})

    def get(self, route):
        return self.client.get(ROOT + route, headers=self.headers)

    def post(self, route, body=None):
        return self.client.post(ROOT + route, json={} if body is None else body, headers=self.headers)


class WriteRoutesStayShut(HostedReadOnlyBase):
    def test_every_write_route_answers_503_and_nothing_leaves(self):
        for route in WRITE_ROUTES:
            for body in ({}, {"dispute_id": "PP-D-SANDBOX01"}, {"anything": "else"}):
                response = self.post(route, body)
                self.assertEqual(response.status_code, 503, (route, response.text))
                self.assertEqual(response.json()["error"]["code"], HOSTED_DEMO_CODE, route)
            self.assertEqual(self.post(route.rstrip("/") + "/").status_code, 503, route)
        self.assertEqual(self.recorder.calls, [])

    def test_only_connect_opens_and_only_the_oauth_post_leaves(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)
        code = self.get("/paypal/disputes").json()["items"][0]["dispute_id"]
        self.assertEqual(self.get("/paypal/disputes/" + code).status_code, 200)
        for route in WRITE_ROUTES:
            self.post(route, {"dispute_id": "PP-D-SANDBOX01"})
        self.assertEqual(self.recorder.posts(), [("POST", "/v1/oauth2/token")])
        self.assertEqual(self.recorder.calls[0], ("POST", "/v1/oauth2/token"))
        self.assertEqual({c for c in self.recorder.calls if c[0] == "GET"},
                         {("GET", "/v1/customer/disputes"), ("GET", "/v1/customer/disputes/PP-D-SANDBOX01")})


    def test_connections_reports_sandbox_reads_and_live_data_is_labelled(self):
        self.assertEqual(self.get("/connections").json(), {"mode": "hosted_demo", "sandbox_reads": True})
        self.post("/paypal/connect")
        body = self.get("/paypal/disputes").json()
        self.assertEqual((body["source"], body["readback"], body["provider_submission"]),
                         ("paypal_sandbox", "GET_LIST", "NOT_PERFORMED"))

    def test_submit_flags_in_the_inner_config_never_enable_a_send(self):
        self.post("/paypal/connect")
        self.assertIs(self.app.state.paypal.dispute_submit_enabled(), False)
        self.assertIs(self.app.state.paypal.tracking_submit_enabled(), False)
        self.assertEqual(self.recorder.posts(), [("POST", "/v1/oauth2/token")])


class PathVariantsStayShut(HostedReadOnlyBase):
    """Red team 2026-11-09 P2: a trailing newline or whitespace must never slip past the guard to a handler."""

    SUFFIXES = ("%0A", "%0a", "%0D", "%0d", "%09", "%20", "%0A%0A", "/%0A", "%0D%0A", "%00", "%0B", "%0C", "%C2%A0")

    def test_write_and_connect_paths_with_control_or_space_suffixes_answer_503(self):
        routes = tuple(r for r in WRITE_ROUTES) + ("/paypal/connect",)
        for route in routes:
            for suffix in self.SUFFIXES:
                response = self.client.post(ROOT + route + suffix, json={"dispute_id": "PP-D-SANDBOX01", "case_ref": "a"},
                                            headers=self.headers)
                self.assertEqual(response.status_code, 503, (route, suffix, response.status_code))
                self.assertEqual(response.json()["error"]["code"], HOSTED_DEMO_CODE, (route, suffix))
        self.assertEqual(self.recorder.calls, [], "none of these may reach PayPal")

    def test_reads_with_whitespace_are_refused_too_and_plain_reads_still_work(self):
        self.assertEqual(self.get("/paypal/disputes%0A").status_code, 503)
        self.assertEqual(self.get("/paypal/disputes%20").status_code, 503)
        self.post("/paypal/connect")
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)


class ConnectIsIdempotent(HostedReadOnlyBase):
    def test_second_connect_makes_no_call_and_spends_no_budget_until_the_token_runs_low(self):
        clock = FakeClock()
        inner = self.app.state.paypal._inner
        budget = ReadBudget(per_minute=3, per_day=50, clock=clock)
        self.app.state.paypal._budget = budget
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.assertEqual(len(self.recorder.calls), 1)
        for _ in range(10):
            self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.assertEqual(len(self.recorder.calls), 1, "a repeated Connect must not call PayPal")
        self.assertEqual(len(budget._stamps), 1, "a repeated Connect must not spend budget")
        self.assertEqual(self.get("/paypal/status").json()["status"], "connected")
        inner.clock.now += __import__("datetime").timedelta(seconds=3600 - 30)  # 30 s left: renew
        clock.now += 61
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.assertEqual(self.recorder.calls.count(("POST", "/v1/oauth2/token")), 2)
        self.assertEqual(self.recorder.posts(), [("POST", "/v1/oauth2/token")] * 2)

    def test_after_expiry_connect_reconnects(self):
        self.post("/paypal/connect")
        self.app.state.paypal._inner.clock.now += __import__("datetime").timedelta(seconds=4000)
        self.assertEqual(self.get("/paypal/status").json()["status"], "disconnected")
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        self.assertEqual(self.recorder.calls.count(("POST", "/v1/oauth2/token")), 2)


# TST marks a synthetic id for tools/validate_public_candidate.py (it rejects real-looking dispute numbers in public text).
REAL_IDS = ("PP-R-TST-010007173", "PP-R-TST-020007173", "PP-R-TST-030007172")  # the first two share prefix and last four: the same base code


class RealIdRecorder(Recorder):
    """Provider stub whose dispute ids are fake but realistic; two of them end in the same four characters."""

    def __call__(self, request):
        response = super().__call__(request)
        if request.method == "GET" and request.url.path == "/v1/customer/disputes":
            rows = sandbox_list_reply()["items"]
            items = [dict(rows[index % 2], dispute_id=real) for index, real in enumerate(REAL_IDS)]
            return httpx.Response(200, json={"items": items})
        return response


class MaskedDisputeIds(HostedReadOnlyBase):
    def setUp(self):
        super().setUp()
        self.recorder = RealIdRecorder()
        self.app.state.paypal._inner = make_inner(self.recorder)
        self.post("/paypal/connect")

    def listing(self):
        response = self.get("/paypal/disputes")
        self.assertEqual(response.status_code, 200, response.text)
        return response

    def test_list_response_never_holds_a_real_id_and_codes_are_valid_and_unique(self):
        response = self.listing()
        for real in REAL_IDS:
            self.assertNotIn(real, response.text)
            self.assertNotIn(real[-9:], response.text, "not even the long tail of the real number")
        codes = [row["dispute_id"] for row in response.json()["items"]]
        self.assertEqual(len(codes), 3)
        self.assertEqual(len(set(codes)), 3, "the two ids that share a tail must not collide")
        for code in codes:
            self.assertRegex(code, r"^PP-[A-Z0-9][A-Z0-9-]{2,62}$")
            self.assertNotIn(code, REAL_IDS)
        self.assertEqual([row["dispute_id"] for row in self.listing().json()["items"]], codes, "stable across reads")

    def test_detail_by_code_works_and_its_whole_response_has_no_real_id(self):
        code = self.listing().json()["items"][0]["dispute_id"]
        response = self.get("/paypal/disputes/" + code)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["dispute_id"], code)
        for real in REAL_IDS:
            self.assertNotIn(real, response.text)
        self.assertIn(("GET", "/v1/customer/disputes/" + REAL_IDS[0]), self.recorder.calls, "the server still asks PayPal by the real id")

    def test_a_real_id_or_an_unknown_code_is_refused_and_never_reaches_paypal(self):
        self.listing()
        before = list(self.recorder.calls)
        for real in REAL_IDS:
            self.assertEqual(self.get("/paypal/disputes/" + real).status_code, 404, real)
        self.assertEqual(self.get("/paypal/disputes/PP-R-TST-XXXX9999").status_code, 404)
        self.assertEqual(self.recorder.calls, before)

    def test_nothing_is_learned_before_a_list_and_the_code_table_is_bounded(self):
        self.assertEqual(self.get("/paypal/disputes/PP-R-TST-XXXX7173").status_code, 404)
        wrapper = self.app.state.paypal
        for index in range(demo_mode.HOSTED_ID_MAP_LIMIT * 3):
            wrapper._code_for(f"PP-R-TST-{index:09d}")
        self.assertLessEqual(len(wrapper._real_by_code), demo_mode.HOSTED_ID_MAP_LIMIT)
        self.assertEqual(len(wrapper._real_by_code), len(wrapper._code_by_real))

    def test_deep_masking_reaches_nested_fields_and_links(self):
        class Inner:
            def status(self):
                return {"status": "connected"}

            async def get_dispute(self, dispute_id):
                return {"dispute_id": dispute_id, "links": [{"href": "https://x/v1/customer/disputes/" + dispute_id}],
                        "nested": {"deep": [dispute_id, {"again": "ref " + dispute_id}]}, "paypal_debug_id": "abc"}

            async def list_disputes(self, page_size=10):
                return [{"dispute_id": REAL_IDS[0]}]
        wrapper = HostedReadOnlyPaypalAdapter(Inner())

        async def run():
            code = (await wrapper.list_disputes())[0]["dispute_id"]
            return code, await wrapper.get_dispute(code)
        code, detail = asyncio.run(run())
        self.assertNotIn(REAL_IDS[0], repr(detail))
        self.assertEqual(detail["dispute_id"], code)
        self.assertIn(code, detail["nested"]["deep"])

    def test_local_mode_does_not_mask(self):
        recorder = RealIdRecorder()
        with env():
            app = create_app(store=SessionStore(), paypal=make_inner(recorder))
            with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 9), raise_server_exceptions=False) as client:
                headers = {"Origin": "http://127.0.0.1:8000"}
                session = client.post(ROOT + "/demo/sessions", json={}, headers=headers).json()
                headers.update({"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})
                self.assertEqual(client.post(ROOT + "/paypal/connect", json={}, headers=headers).status_code, 200)
                listing = client.get(ROOT + "/paypal/disputes", headers=headers)
                self.assertEqual([row["dispute_id"] for row in listing.json()["items"]], list(REAL_IDS))
                self.assertEqual(client.get(ROOT + "/paypal/disputes/" + REAL_IDS[0], headers=headers).json()["dispute_id"], REAL_IDS[0])


class WrapperSurface(unittest.TestCase):
    def test_wrapper_has_no_passthrough_and_every_write_refuses_before_the_transport(self):
        recorder = Recorder()
        wrapper = HostedReadOnlyPaypalAdapter(make_inner(recorder))
        self.assertNotIn("__getattr__", vars(HostedReadOnlyPaypalAdapter))
        public = {name for name in dir(wrapper) if not name.startswith("_")}
        self.assertEqual(public, {"status", "require_connected", "connect", "list_disputes", "get_dispute",
                                  "dispute_submit_enabled", "tracking_submit_enabled", "account_merchant_id",
                                  "last_debug_id", "open_clients", "create_invoice_draft", "provide_evidence",
                                  "add_tracking", "verify_webhook"})
        for name in ("transport", "config_loader", "_request", "call_log", "clock"):
            self.assertFalse(hasattr(wrapper, name), name)

        async def attempt():
            await wrapper.connect()
            for call in (lambda: wrapper.create_invoice_draft({}, "r"), lambda: wrapper.provide_evidence("PP-D-SANDBOX01", {}),
                         lambda: wrapper.add_tracking({}), lambda: wrapper.verify_webhook(b"{}")):
                with self.assertRaises(BoundaryError) as caught:
                    await call()
                self.assertEqual((caught.exception.status, caught.exception.code), (503, HOSTED_DEMO_CODE))
        asyncio.run(attempt())
        self.assertEqual(recorder.calls, [("POST", "/v1/oauth2/token")])


class ReadBudgetTests(HostedReadOnlyBase):
    def setUp(self):
        super().setUp()
        self.clock = FakeClock()
        self.app.state.paypal._budget = ReadBudget(per_minute=3, per_day=5, clock=self.clock)
        self.post("/paypal/connect")  # uses 1

    def test_minute_cap_answers_429_then_recovers(self):
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)
        before = len(self.recorder.calls)
        over = self.get("/paypal/disputes")
        self.assertEqual(over.status_code, 429)
        self.assertEqual(over.json()["error"]["code"], HOSTED_READ_BUDGET_CODE)
        self.assertGreaterEqual(int(over.headers["Retry-After"]), 1)
        self.assertEqual(len(self.recorder.calls), before, "a refused read must not reach PayPal")
        self.clock.now += 61
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)

    def test_day_cap_answers_429_until_the_day_rolls(self):
        for _ in range(4):
            self.assertIn(self.get("/paypal/disputes").status_code, (200, 429))
            self.clock.now += 61
        self.assertEqual(self.get("/paypal/disputes").status_code, 429)
        self.clock.now += 86400
        self.assertEqual(self.get("/paypal/disputes").status_code, 200)


class FlagSemantics(unittest.TestCase):
    def test_flag_without_public_mode_does_nothing(self):
        for environment in ({"PAYGUARD_HOSTED_READONLY_SANDBOX": "enabled"},
                            {"PAYGUARD_DEMO_MODE": "off", "PAYGUARD_HOSTED_READONLY_SANDBOX": "enabled"}):
            with env(**environment):
                self.assertFalse(hosted_readonly_enabled())
                app = create_app(store=SessionStore())
                self.assertFalse(app.state.hosted_readonly)
                self.assertNotIsInstance(app.state.paypal, HostedReadOnlyPaypalAdapter)
                with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 1)) as client:
                    session = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": "http://127.0.0.1:8000"}).json()
                    self.assertEqual(client.get(ROOT + "/connections", headers={"X-Demo-Session": session["session_id"]}).json(),
                                     {"mode": "local"})

    def test_flag_off_keeps_the_refusing_stub_and_connect_stays_503(self):
        for extra in ({}, {"PAYGUARD_HOSTED_READONLY_SANDBOX": "off"}):
            recorder = Recorder()
            with env(**dict(PUBLIC_ENV, **extra)):
                app = create_app(store=SessionStore(), hosted_sandbox_inner=make_inner(recorder))
                self.assertIsInstance(app.state.paypal, HostedDemoPaypalStub)
                with TestClient(app, base_url=ORIGIN, client=("10.0.0.5", 1), raise_server_exceptions=False) as client:
                    session = client.post(ROOT + "/demo/sessions", json={}, headers=dict(PROXY, Origin=ORIGIN)).json()
                    headers = dict(PROXY, Origin=ORIGIN, **{"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})
                    self.assertEqual(client.post(ROOT + "/paypal/connect", json={}, headers=headers).status_code, 503)
                    self.assertEqual(client.get(ROOT + "/connections", headers=headers).json(), {"mode": "hosted_demo"})
            self.assertEqual(recorder.calls, [])

    def test_unknown_flag_value_fails_startup_only_in_public_mode(self):
        with env(**dict(PUBLIC_ENV, PAYGUARD_HOSTED_READONLY_SANDBOX="yes")):
            with self.assertRaises(DemoModeConfigError):
                hosted_readonly_enabled()
        with env(PAYGUARD_HOSTED_READONLY_SANDBOX="yes"):
            self.assertFalse(hosted_readonly_enabled())

    def test_disabled_routes_constant_is_unchanged(self):
        self.assertIn(("POST", "/api/v1/paypal/connect"), DISABLED_ROUTES)
        self.assertEqual(len(DISABLED_ROUTES), 7)
        self.assertNotIn(("POST", "/api/v1/paypal/connect"), demo_mode.disabled_routes(True))
        self.assertEqual(len(demo_mode.disabled_routes(True)), 6)


if __name__ == "__main__":
    unittest.main()
