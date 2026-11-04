"""Public hosted demo mode: refusing provider stubs, one exact public host, strict defaults when off."""

import asyncio
import os
from pathlib import Path
import socket
import subprocess
import sys
import unittest
from unittest import mock

from fastapi.testclient import TestClient
import httpx

from app import main
from app.demo_mode import (DISABLED_ROUTES, HOSTED_DEMO_CODE, DemoModeConfigError, HostedDemoBriefStub,
                           HostedDemoPaypalStub, public_demo_enabled, public_host,
                           require_public_host)
from app.main import ALLOWED_HOSTS, ALLOWED_ORIGINS, create_app, create_lmstudio_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore


ROOT = "/api/v1"
LOCAL_ORIGIN = "http://127.0.0.1:8000"
PUBLIC = "payguard-demo.onrender.com"
PUBLIC_ORIGIN = "https://" + PUBLIC
PROXY = {"X-Forwarded-For": "198.51.100.7", "X-Forwarded-Proto": "https"}
DEMO_ENV = {"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": PUBLIC}
# Provider switches an operator might leave set; demo mode must ignore all of them.
PROVIDER_ENV = {"PAYGUARD_PAYPAL_OUTBOUND": "enabled", "PAYPAL_CLIENT_ID": "synthetic-id",
                "PAYPAL_CLIENT_SECRET": "synthetic-secret", "PAYGUARD_PAYPAL_DISPUTE_SUBMIT": "enabled",
                "PAYGUARD_GEMINI_OUTBOUND": "enabled"}


def clean_env(**values):
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith(("PAYGUARD_DEMO", "PAYGUARD_PUBLIC"))}
    environment.update(values)
    return mock.patch.dict(os.environ, environment, clear=True)


class OutboundSpy:
    """Record and refuse every route out of the process: httpx transports, sockets, DNS, subprocesses."""

    def __init__(self):
        self.calls = []

    def _record(self, kind):
        def refuse(*_args, **_kwargs):
            self.calls.append(kind)
            raise AssertionError(f"outbound {kind} attempted in hosted demo mode")
        return refuse

    def _record_async(self, kind):
        async def refuse(*_args, **_kwargs):
            self.calls.append(kind)
            raise AssertionError(f"outbound {kind} attempted in hosted demo mode")
        return refuse

    def __enter__(self):
        self._patches = [
            mock.patch.object(httpx.HTTPTransport, "handle_request", self._record("httpx_sync")),
            mock.patch.object(httpx.AsyncHTTPTransport, "handle_async_request", self._record_async("httpx_async")),
            mock.patch.object(socket.socket, "connect", self._record("socket_connect")),
            mock.patch.object(socket.socket, "connect_ex", self._record("socket_connect_ex")),
            mock.patch.object(socket, "create_connection", self._record("create_connection")),
            mock.patch.object(socket, "getaddrinfo", self._record("getaddrinfo")),
            mock.patch.object(asyncio, "create_subprocess_exec", self._record_async("subprocess")),
            mock.patch.object(asyncio, "open_connection", self._record_async("open_connection")),
        ]
        for patch in self._patches:
            patch.start()
        return self

    def __exit__(self, *_exc):
        for patch in reversed(self._patches):
            patch.stop()


class Flow:
    """Drive the console API the way the frontend does."""

    def __init__(self, test, client, origin, extra=None):
        self.test, self.client, self.origin, self.extra = test, client, origin, dict(extra or {})
        response = client.post(ROOT + "/demo/sessions", json={}, headers=self.base())
        test.assertEqual(response.status_code, 201, response.text)
        self.session = response.json()

    def base(self):
        return dict(self.extra, Origin=self.origin)

    def headers(self):
        return dict(self.base(), **{"X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]})

    def post(self, route, body=None):
        return self.client.post(ROOT + route, json={} if body is None else body, headers=self.headers())

    def get(self, route):
        return self.client.get(ROOT + route, headers=self.headers())

    def ok(self, response, status=200):
        self.test.assertEqual(response.status_code, status, response.text)
        return response.json()

    def disabled(self, response):
        self.test.assertEqual(response.status_code, 503, response.text)
        error = response.json()["error"]
        self.test.assertEqual(error["code"], HOSTED_DEMO_CODE)
        self.test.assertIn("disabled in the hosted demo", error["message"])
        self.test.assertNotIn("secret", response.text)


class HostedDemoFlowTests(unittest.TestCase):
    def make_app(self, **injected):
        with clean_env(**DEMO_ENV, **PROVIDER_ENV):
            return create_app(store=SessionStore(), **injected)

    def run_three_stages(self, app, *, client_addr, base_url, origin, extra=None):
        with OutboundSpy() as spy, TestClient(app, base_url=base_url, client=client_addr,
                                               raise_server_exceptions=False) as client:
            flow = Flow(self, client, origin, extra)
            self.assertEqual(flow.ok(client.get(ROOT + "/health", headers=flow.base()))["source"], "synthetic")
            # Sandbox status is local; connect and webhook verification are refused.
            status = flow.ok(flow.get("/paypal/status"))
            self.assertEqual((status["configured"], status["status"]), (False, "not_configured"))
            flow.disabled(flow.post("/paypal/connect"))
            flow.disabled(flow.post("/paypal/webhooks/verify", {"anything": "at all"}))

            # Stage 1: source compliance. Local AUP review, local invoice review, Sandbox draft refused.
            description = "Synthetic ceramic cup"
            evaluation = flow.ok(flow.post("/aup/review", {"description": description}))
            receipt = flow.ok(flow.post("/paypal/invoices/review", {
                "description": description, "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": evaluation["evaluation_id"], "description_digest": evaluation["description_digest"]}))
            flow.disabled(flow.post("/paypal/invoices/draft", {
                "description": description, "amount": "10.00", "currency": "USD",
                "review_token": receipt["review_token"], "payload_digest": receipt["payload_digest"]}))
            references = flow.ok(flow.post("/references/search",
                                           {"query": "prior approval", "theme": "source_compliance", "jurisdiction": "US"}))
            self.assertEqual(references["source"], "public_reference")
            flow.disabled(flow.post("/ai/evidence-brief", {"stage": "source_compliance"}))

            # Stage 2: velocity guard on the synthetic burst.
            state = flow.ok(flow.post("/demo/inject", {"scenario": "burst"}))
            self.assertEqual(state["velocity"]["status"], "review_velocity")
            flow.disabled(flow.post("/ai/evidence-brief", {"stage": "velocity_guard"}))

            # Stage 3: dispute mediation from synthetic cases and the Disputes fixture.
            flow.ok(flow.post("/demo/inject", {"scenario": "dispute"}))
            draft = flow.ok(flow.post("/disputes/case-ref-001/draft"))
            self.assertEqual(draft["source"], "synthetic")
            approval = flow.ok(flow.post("/disputes/case-ref-001/approve", {"draft_digest": draft["draft_digest"]}))
            self.assertEqual(approval["external_submission"], "FROZEN")
            listing = flow.ok(flow.get("/paypal/disputes"))
            self.assertEqual(listing["source"], "synthetic_fixture")
            detail = flow.ok(flow.get("/paypal/disputes/PP-D-00000001"))
            self.assertEqual(detail["evidence_class"], "SYNTHETIC_FIXTURE")
            for submit in (False, True):
                flow.disabled(flow.post("/paypal/disputes/provide-evidence",
                                        {"dispute_id": "PP-D-00000001", "case_ref": "case-ref-001", "submit": submit}))
            flow.disabled(flow.post("/ai/evidence-brief", {"stage": "dispute_mediation"}))
        self.assertEqual(spy.calls, [])

    def test_three_stage_flow_makes_zero_outbound_calls_from_loopback(self):
        self.run_three_stages(self.make_app(), client_addr=("127.0.0.1", 50001),
                              base_url="http://127.0.0.1:8000", origin=LOCAL_ORIGIN)

    def test_three_stage_flow_makes_zero_outbound_calls_behind_the_proxy(self):
        self.run_three_stages(self.make_app(), client_addr=("10.10.0.5", 50001), base_url=PUBLIC_ORIGIN,
                              origin=PUBLIC_ORIGIN, extra=PROXY)

    def test_injected_live_adapters_are_still_replaced(self):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(200, json={"access_token": "t", "token_type": "Bearer", "expires_in": 60})
        live = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "id", "secret"), transport=httpx.MockTransport(handler))
        app = self.make_app(paypal=live)
        self.assertIsInstance(app.state.paypal, HostedDemoPaypalStub)
        self.assertIsInstance(app.state.ai_brief, HostedDemoBriefStub)
        self.run_three_stages(app, client_addr=("127.0.0.1", 50001), base_url="http://127.0.0.1:8000", origin=LOCAL_ORIGIN)
        self.assertEqual(calls, [])
        with clean_env(**DEMO_ENV):
            self.assertIsInstance(create_lmstudio_app().state.ai_brief, HostedDemoBriefStub)

    def test_disabled_routes_answer_before_session_or_schema_checks(self):
        app = self.make_app()
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 50001)) as client:
            for method, path in sorted(DISABLED_ROUTES):
                response = client.request(method, path, json={"not": "valid"}, headers={"Origin": LOCAL_ORIGIN})
                self.assertEqual((response.status_code, response.json()["error"]["code"]), (503, HOSTED_DEMO_CODE), path)
            # The boundary still runs first: a foreign host never reaches the refusal.
            rejected = client.post(ROOT + "/paypal/connect", json={}, headers={"Origin": LOCAL_ORIGIN, "Host": "evil.invalid"})
            self.assertEqual(rejected.json()["error"]["code"], "host_rejected")


class HostAllowlistTests(unittest.TestCase):
    def status(self, app, *, client=("10.10.0.5", 1), host=PUBLIC, origin=None, proxy=PROXY, method="GET", path="/health"):
        headers = dict(proxy or {})
        headers["Host"] = host
        if origin is not None:
            headers["Origin"] = origin
        with TestClient(app, base_url="http://" + PUBLIC, client=client) as test_client:
            response = test_client.request(method, ROOT + path, headers=headers, json={} if method == "POST" else None)
        return response.status_code, response.json().get("error", {}).get("code") if response.status_code >= 400 else None

    def demo_app(self, **env):
        with clean_env(**dict(DEMO_ENV, **env)):
            return create_app(store=SessionStore())

    def test_public_host_behind_proxy_is_admitted(self):
        app = self.demo_app()
        self.assertEqual(self.status(app), (200, None))
        self.assertEqual(self.status(app, host=PUBLIC.upper()), (200, None))
        self.assertEqual(self.status(app, origin=PUBLIC_ORIGIN, method="POST", path="/demo/sessions"), (201, None))

    def test_non_loopback_requires_the_proxy_headers(self):
        app = self.demo_app()
        self.assertEqual(self.status(app, proxy={}), (403, "host_rejected"))
        self.assertEqual(self.status(app, proxy={"X-Forwarded-For": "198.51.100.7"}), (403, "host_rejected"))
        self.assertEqual(self.status(app, proxy={"X-Forwarded-Proto": "https"}), (403, "host_rejected"))
        self.assertEqual(self.status(app, proxy={"X-Forwarded-For": " ", "X-Forwarded-Proto": "https"}), (403, "host_rejected"))
        self.assertEqual(self.status(app, proxy={"X-Forwarded-For": "198.51.100.7", "X-Forwarded-Proto": "http"}), (403, "host_rejected"))

    def test_only_the_exact_public_host_is_added(self):
        app = self.demo_app()
        for host in ("evil.invalid", "x." + PUBLIC, PUBLIC + ".evil.invalid", PUBLIC + ":443", "onrender.com",
                     "payguard-demo-2.onrender.com", "127.0.0.1:8000", "localhost:8000"):
            with self.subTest(host=host):
                self.assertEqual(self.status(app, host=host), (403, "host_rejected"))

    def test_only_the_https_public_origin_is_added(self):
        app = self.demo_app()
        for origin in ("http://" + PUBLIC, PUBLIC_ORIGIN + ":443", PUBLIC_ORIGIN + "/", "https://evil.invalid", "null"):
            with self.subTest(origin=origin):
                self.assertEqual(self.status(app, origin=origin), (403, "origin_rejected"))
        self.assertEqual(self.status(app, method="POST", path="/demo/sessions"), (403, "origin_required"))

    def test_duplicate_forwarding_headers_are_rejected(self):
        app = self.demo_app()
        with TestClient(app, base_url="http://" + PUBLIC, client=("10.10.0.5", 1)) as client:
            response = client.get(ROOT + "/health", headers=[("Host", PUBLIC), ("X-Forwarded-For", "198.51.100.7"),
                                                            ("X-Forwarded-Proto", "https"), ("X-Forwarded-Proto", "https")])
        self.assertEqual(response.json()["error"]["code"], "duplicate_security_header")

    def test_loopback_defaults_still_work_in_demo_mode(self):
        app = self.demo_app()
        self.assertEqual(self.status(app, client=("127.0.0.1", 1), host="127.0.0.1:8000", proxy={}), (200, None))
        self.assertEqual(self.status(app, client=("203.0.113.1", 1), host="127.0.0.1:8000"), (403, "host_rejected"))

    def test_demo_mode_without_public_host_refuses_to_build_the_app(self):
        for env in ({"PAYGUARD_DEMO_MODE": "public"}, {"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": ""}):
            with self.subTest(env=env), clean_env(**env):
                with self.assertRaises(DemoModeConfigError) as caught:
                    create_app(store=SessionStore())
                self.assertIn("requires PAYGUARD_PUBLIC_HOST", str(caught.exception))
            with self.subTest(env=env, factory="lmstudio"), clean_env(**env):
                with self.assertRaises(DemoModeConfigError):
                    create_lmstudio_app()

    def test_server_process_exits_non_zero_without_or_with_invalid_public_host(self):
        root = Path(__file__).resolve().parents[1]
        base = {key: value for key, value in os.environ.items() if not key.startswith("PAYGUARD_")}
        base.update(PYTHONPATH=f"{root / 'src'}{os.pathsep}{root / 'backend'}", PYTHONDONTWRITEBYTECODE="1",
                    PAYGUARD_DEMO_MODE="public")
        # Port 0 and loopback only; the process must stop while importing the app, before binding.
        command = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "0",
                   "--no-access-log", "--no-proxy-headers"]
        for host, message in ((None, "requires PAYGUARD_PUBLIC_HOST"), ("https://" + PUBLIC, "must be one lowercase hostname")):
            env = dict(base) if host is None else dict(base, PAYGUARD_PUBLIC_HOST=host)
            with self.subTest(host=host):
                result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=60)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("DemoModeConfigError", result.stderr)
                self.assertIn(message, result.stderr)
                self.assertNotIn("Uvicorn running", result.stderr)

    def test_invalid_configuration_fails_startup(self):
        for value in ("https://" + PUBLIC, PUBLIC + ":443", PUBLIC + "/", "*.onrender.com", PUBLIC + "," + "evil.invalid",
                      " " + PUBLIC, PUBLIC.upper(), PUBLIC + ".", "localhost", "203.0.113.1", "-bad.onrender.com"):
            with self.subTest(value=value), clean_env(PAYGUARD_DEMO_MODE="public", PAYGUARD_PUBLIC_HOST=value):
                with self.assertRaises(DemoModeConfigError):
                    create_app(store=SessionStore())
        for mode in ("Public", "on", "1", "true"):
            with self.subTest(mode=mode), clean_env(PAYGUARD_DEMO_MODE=mode):
                with self.assertRaises(DemoModeConfigError):
                    create_app(store=SessionStore())

    def test_config_readers(self):
        self.assertFalse(public_demo_enabled({}))
        self.assertFalse(public_demo_enabled({"PAYGUARD_DEMO_MODE": "off"}))
        self.assertTrue(public_demo_enabled({"PAYGUARD_DEMO_MODE": "public"}))
        self.assertIsNone(public_host({}))
        with self.assertRaises(DemoModeConfigError):
            require_public_host({})
        self.assertEqual(require_public_host({"PAYGUARD_PUBLIC_HOST": PUBLIC}), PUBLIC)
        self.assertEqual(public_host({"PAYGUARD_PUBLIC_HOST": PUBLIC}), PUBLIC)


class DefaultsUnchangedTests(unittest.TestCase):
    def test_allowlist_constants_are_the_strict_loopback_values(self):
        self.assertEqual(ALLOWED_HOSTS, frozenset({"localhost:8000", "127.0.0.1:8000", "[::1]:8000"}))
        self.assertEqual(ALLOWED_ORIGINS, frozenset({"http://localhost:5173", "http://127.0.0.1:5173",
                                                     "http://localhost:8000", "http://127.0.0.1:8000"}))

    def test_default_app_keeps_real_adapters_and_strict_boundary(self):
        with clean_env():
            app = create_app(store=SessionStore())
        self.assertEqual(app.state.demo_mode, "off")
        self.assertIsInstance(app.state.paypal, PaypalAdapter)
        self.assertNotIsInstance(app.state.ai_brief, HostedDemoBriefStub)
        boundary = [entry for entry in app.user_middleware if entry.cls is main.LocalBoundaryMiddleware]
        self.assertEqual(len(boundary), 1)
        self.assertEqual(boundary[0].kwargs, {})
        self.assertEqual([entry.cls for entry in app.user_middleware], [main.LocalBoundaryMiddleware])

    def requests(self):
        """Requests whose answers must not depend on the public-host variables when demo mode is off."""
        local = {"Origin": LOCAL_ORIGIN}
        return [
            (("127.0.0.1", 1), "GET", "/health", {}),
            (("127.0.0.1", 1), "GET", "/health", {"Host": PUBLIC}),
            (("127.0.0.1", 1), "GET", "/health", {"Origin": PUBLIC_ORIGIN}),
            (("127.0.0.1", 1), "GET", "/health", dict(PROXY, Host=PUBLIC)),
            (("10.10.0.5", 1), "GET", "/health", dict(PROXY, Host=PUBLIC)),
            (("10.10.0.5", 1), "GET", "/health", dict(PROXY)),
            (("203.0.113.1", 1), "GET", "/health", {}),
            (("127.0.0.1", 1), "POST", "/paypal/connect", dict(local)),
            (("127.0.0.1", 1), "POST", "/ai/evidence-brief", dict(local)),
            (("127.0.0.1", 1), "POST", "/demo/sessions", {"Origin": PUBLIC_ORIGIN}),
            (("127.0.0.1", 1), "OPTIONS", "/demo/inject", {"Origin": PUBLIC_ORIGIN, "Access-Control-Request-Method": "POST"}),
            (("127.0.0.1", 1), "OPTIONS", "/demo/inject", {"Origin": LOCAL_ORIGIN, "Access-Control-Request-Method": "POST"}),
        ]

    def answers(self, env):
        with clean_env(**env):
            app = create_app(store=SessionStore(), paypal=PaypalAdapter(config_loader=PaypalConfig,
                                                                         transport=httpx.MockTransport(lambda _r: httpx.Response(599))))
        results = []
        for client_addr, method, path, headers in self.requests():
            with TestClient(app, base_url="http://127.0.0.1:8000", client=client_addr, raise_server_exceptions=False) as client:
                response = client.request(method, ROOT + path, headers=headers, json={} if method == "POST" else None)
            results.append((response.status_code, sorted(response.headers.items()), response.content))
        return results

    def test_public_host_without_demo_mode_changes_no_response_byte(self):
        baseline = self.answers({})
        self.assertEqual(baseline[0][0], 200)
        self.assertEqual([row[0] for row in baseline[1:7]], [403] * 6)
        self.assertEqual(self.answers({"PAYGUARD_PUBLIC_HOST": PUBLIC}), baseline)
        self.assertEqual(self.answers({"PAYGUARD_DEMO_MODE": "off", "PAYGUARD_PUBLIC_HOST": PUBLIC}), baseline)


if __name__ == "__main__":
    unittest.main()


class HostedGuideModelTests(unittest.TestCase):
    """(r32 hosted guide) Gemini for the hosted guide is an explicit opt-in on a free-tier key, under lower caps."""

    GUIDE_ENV = {"PAYGUARD_GUIDE_MODEL": "gemini", "PAYGUARD_GEMINI_TRANSPORT": "api_key"}

    def build(self, **values):
        with clean_env(**DEMO_ENV, **values):
            return create_app(store=SessionStore()).state.guide

    def test_without_the_switch_the_hosted_guide_never_builds_a_chooser(self):
        # Even with every guide model variable set, the hosted guide stays on the keyword chooser.
        guide = self.build(**self.GUIDE_ENV)
        with mock.patch("app.guide_routes.select_guide_chooser", side_effect=AssertionError("no chooser")):
            self.assertIsNone(guide.chooser_factory())
        self.assertEqual(guide._chooser_status(), ("keyword", False))

    def test_any_other_switch_value_is_off(self):
        for value in ("", "on", "true", "Gemini", "gemini "):
            with self.subTest(value=value):
                guide = self.build(**self.GUIDE_ENV, PAYGUARD_HOSTED_GUIDE_MODEL=value)
                self.assertIsNone(guide.chooser_factory())

    def test_with_the_switch_the_default_factory_decides_under_lower_caps(self):
        from app import guide_routes
        guide = self.build(**self.GUIDE_ENV, PAYGUARD_HOSTED_GUIDE_MODEL="gemini")
        sentinel = object()
        with mock.patch("app.guide_routes.select_guide_chooser", return_value=sentinel):
            self.assertIs(guide.chooser_factory(), sentinel)
        self.assertEqual(guide.governor._global_per_minute, guide_routes.HOSTED_GUIDE_CALLS_PER_MINUTE)
        self.assertEqual(guide.governor._global_per_day, guide_routes.HOSTED_GUIDE_CALLS_PER_DAY)
        self.assertLessEqual(guide_routes.HOSTED_GUIDE_CALLS_PER_MINUTE, 5)
        self.assertLessEqual(guide_routes.HOSTED_GUIDE_CALLS_PER_DAY, 20)

    def test_switch_on_without_a_key_stays_on_keywords(self):
        # No GEMINI_API_KEY in the environment: the api-key profile is not configured, so no worker can start.
        with clean_env(**DEMO_ENV, **self.GUIDE_ENV, PAYGUARD_HOSTED_GUIDE_MODEL="gemini"):
            os.environ.pop("GEMINI_API_KEY", None)
            guide = create_app(store=SessionStore()).state.guide
            self.assertIsNone(guide.chooser_factory())

    def test_the_other_ai_routes_stay_disabled_with_the_switch_on(self):
        self.assertIn(("POST", "/api/v1/ai/evidence-brief"), DISABLED_ROUTES)
        self.assertIn(("POST", "/api/v1/studio/agent-turn"), DISABLED_ROUTES)

    def test_lower_caps_can_never_raise_the_shared_ones(self):
        from payguard import controlled_fallback as cf
        governor = cf.Governor(global_per_minute=cf.GLOBAL_CALLS_PER_MINUTE * 10, global_per_day=cf.GLOBAL_CALLS_PER_DAY * 10)
        self.assertEqual((governor._global_per_minute, governor._global_per_day),
                         (cf.GLOBAL_CALLS_PER_MINUTE, cf.GLOBAL_CALLS_PER_DAY))
        small = cf.Governor(clock=lambda: 1000.0, min_spacing=0, global_per_minute=2)
        admitted = [small.admit(f"s{n}", client_id=f"c{n}")[0] is None for n in range(4)]
        self.assertEqual(admitted, [True, True, False, False])
