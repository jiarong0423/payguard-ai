"""Offline boundary challenges, including the actual optional SDK callback."""

import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.metadata
import json
import socket
import sys
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig, SANDBOX_BASE
from app.paypal_tools import SafePaypalToolGateway, create_official_invoice_tool
from app.store import BoundaryError, SessionStore


def sdk_available():
    try:
        return all(importlib.metadata.version(package) == version for package, version in
                   (("paypal-agent-toolkit", "1.11.0"), ("openai-agents", "0.0.2"), ("openai", "1.66.0")))
    except importlib.metadata.PackageNotFoundError:
        return False


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 4, 8, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


class ToolTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.network_guards = [patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
                               patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))]
        for guard in self.network_guards:
            guard.start()
            self.addCleanup(guard.stop)
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock, rate_limit=200)
        created = self.store.create()
        self.session = self.store.sessions[created["session_id"]]
        self.calls = []
        self.reply = {"id": "INV2-SYNTHETIC-0001", "status": "DRAFT"}
        self.failure = None

        def handler(request):
            self.assertTrue(str(request.url).startswith(SANDBOX_BASE + "/"))
            self.calls.append(request)
            if request.url.path == "/v1/oauth2/token":
                return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            self.assertEqual(request.url.path, "/v2/invoicing/invoices")
            if self.failure is not None:
                raise self.failure
            if type(self.reply) is bytes:
                return httpx.Response(200, content=self.reply)
            return httpx.Response(200, json=self.reply)

        self.adapter = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret"),
                                     transport=httpx.MockTransport(handler), clock=self.clock)
        self.gateway = SafePaypalToolGateway(self.store, self.adapter)
        await self.adapter.connect()
        self.payload = {"description": "Synthetic ceramic cup", "amount": "10.00", "currency": "USD"}
        self.request = self.review(self.session)

    async def asyncTearDown(self):
        self.assertEqual(self.adapter.open_clients, 0)

    def review(self, session):
        evaluation = self.store.review_aup(session, self.payload["description"])
        receipt = self.store.review_invoice(session, dict(self.payload, confirm_sandbox_draft=True,
                    evaluation_id=evaluation["evaluation_id"], description_digest=evaluation["description_digest"]))
        return dict(self.payload, review_token=receipt["review_token"], payload_digest=receipt["payload_digest"])

    async def assert_boundary(self, arguments=None, *, session=None, method="create_invoice", code=None, gateway=None):
        with self.assertRaises(BoundaryError) as captured:
            await (gateway or self.gateway).invoke(method, self.request if arguments is None else arguments,
                                                  session=self.session if session is None else session)
        if code:
            self.assertEqual(captured.exception.code, code)
        self.assertNotIn("synthetic-secret", str(captured.exception))
        self.assertIsNone(captured.exception.__cause__)
        return captured.exception

    async def test_only_create_invoice_and_no_authority_input(self):
        count = len(self.calls)
        for method in ("send_invoice", "create_order", "get_invoice", "list_transactions", "accept_dispute_claim", None, {}, "CREATE_INVOICE"):
            await self.assert_boundary(method=method, code="tool_action_frozen")
        for key in ("method", "session", "environment", "url", "context", "recipients"):
            await self.assert_boundary(dict(self.request, **{key: "untrusted"}), code="schema_invalid")
        self.assertEqual(len(self.calls), count)
        self.assertIn(self.request["review_token"], self.session.invoice_reviews)

    async def test_success_exact_response_then_replay(self):
        result = await self.gateway.invoke("create_invoice", json.dumps(self.request), session=self.session)
        self.assertEqual({key: value for key, value in result.items() if key != "evidence_receipt"},
                         {"source": "paypal_sandbox", "invoice_id": "INV2-SYNTHETIC-0001", "status": "DRAFT",
                          "environment": "sandbox", "external_send": "FROZEN"})
        self.assertEqual(result["evidence_receipt"]["evidence_class"], "SYNTHETIC_TEST_RESPONSE")
        self.assertFalse(result["evidence_receipt"]["separate_get_readback"])
        await self.assert_boundary(code="review_binding_rejected")
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.session.invoice_attempts, 1)

    async def test_duplicate_nonfinite_depth_cycles_and_types(self):
        valid = json.dumps(self.request)
        values = [valid[:-1] + ',"amount":"20.00"}', '{"amount":NaN}', '{"x":Infinity}',
                  '{"x":1e999}', "[]", "null", 3, b"{}", {"amount": 10}, dict(self.request, amount=10.0)]
        deep = {}; cursor = deep
        for _index in range(12):
            cursor["x"] = {}; cursor = cursor["x"]
        values.append(deep)
        cycle = {}; cycle["self"] = cycle; values.append(cycle)
        values.append({"x": list(range(200))})
        values.append({"x": 2 ** 500})
        values.append({"x": object()})
        for value in values:
            await self.assert_boundary(value, code="schema_invalid")
        self.assertEqual(len(self.calls), 1)

    async def test_size_and_unicode_limits(self):
        for value in (" " * 8193, {"x": "a" * 8193}, {"x": "★" * 4000}):
            error = await self.assert_boundary(value, code="body_limit")
            self.assertEqual(error.status, 413)
        await self.assert_boundary('{"x":"\ud800"}', code="schema_invalid")

    async def test_forged_removed_and_expired_sessions(self):
        forged = deepcopy(self.session)
        await self.assert_boundary(session=forged, code="session_required")
        del self.store.sessions[self.session.session_id]
        await self.assert_boundary(code="session_required")
        self.store.sessions[self.session.session_id] = self.session
        self.clock.now = self.session.expires_at
        await self.assert_boundary(code="session_required")
        self.assertEqual(len(self.calls), 1)

    async def test_review_cross_session_change_expiry_reset(self):
        other = self.store.sessions[self.store.create()["session_id"]]
        await self.assert_boundary(session=other, code="review_binding_rejected")
        await self.assert_boundary(dict(self.request, amount="11.00"), code="review_binding_rejected")
        self.clock.now += timedelta(seconds=120)
        await self.assert_boundary(code="review_binding_rejected")
        self.request = self.review(self.session)
        self.store.inject(self.session, "reset")
        await self.assert_boundary(code="review_binding_rejected")
        self.assertEqual(len(self.calls), 1)

    async def test_parallel_consume_is_once(self):
        results = await asyncio.gather(*(self.gateway.invoke("create_invoice", self.request, session=self.session)
                                         for _index in range(5)), return_exceptions=True)
        self.assertEqual(sum(type(result) is dict for result in results), 1)
        self.assertEqual(sum(type(result) is BoundaryError for result in results), 4)
        self.assertEqual(len(self.calls), 2)

    async def test_disconnected_disabled_no_consume(self):
        self.adapter._access_token = None
        self.adapter._status = "disconnected"
        await self.assert_boundary(code="provider_not_connected")
        self.assertIn(self.request["review_token"], self.session.invoice_reviews)
        self.adapter._config = PaypalConfig()
        await self.assert_boundary(code="provider_disabled")
        self.assertEqual(len(self.calls), 1)

    async def test_clock_failure_safe(self):
        self.store.clock = lambda: datetime(2026, 10, 4)
        await self.assert_boundary(code="clock_unavailable")

    async def test_provider_timeout_consumed_not_false_success(self):
        self.failure = httpx.ReadTimeout("private provider buyer@example.invalid synthetic-secret")
        await self.assert_boundary(code="provider_upstream_failure")
        await self.assert_boundary(code="review_binding_rejected")
        self.assertEqual(len(self.calls), 2)

    async def test_provider_cap_duplicate_nonfinite_non_draft(self):
        for reply in (b"x" * 65537, b'{"id":"INV2-SYNTHETIC-0001","id":"duplicate","status":"DRAFT"}',
                      b'{"id":NaN,"status":"DRAFT"}', {"id": "INV2-SYNTHETIC-0001", "status": "SENT"}):
            self.reply = reply
            self.request = self.review(self.session)
            await self.assert_boundary(code="provider_response_invalid")

    async def test_sanitized_adapter_boundary_and_exception(self):
        for error in (BoundaryError(502, "buyer@example.invalid"), BoundaryError(502, {"private": "buyer@example.invalid"}),
                      RuntimeError("synthetic-secret buyer@example.invalid")):
            async def broken(_payload, _request_id):
                raise error
            self.request = self.review(self.session)
            with patch.object(self.adapter, "create_invoice_draft", broken):
                await self.assert_boundary(code="provider_upstream_failure")

    async def test_environment_rejection_and_credential_loader_never_called(self):
        with patch.object(self.adapter, "config_loader", side_effect=AssertionError("credential read forbidden")):
            status = self.adapter.status()
            status["environment"] = "production"
            with patch.object(self.adapter, "status", return_value=status):
                await self.assert_boundary(code="provider_response_invalid")
            self.assertIn(self.request["review_token"], self.session.invoice_reviews)
            result = await self.gateway.invoke("create_invoice", self.request, session=self.session)
            self.assertEqual(result["environment"], "sandbox")

    async def test_result_contract_rejects_raw_extra_bad_id_and_success_flags(self):
        safe = {"source": "paypal_sandbox", "invoice_id": "INV2-SYNTHETIC-0001", "status": "DRAFT",
                "environment": "sandbox", "external_send": "FROZEN"}
        for result in (dict(safe, payer="buyer@example.invalid"), dict(safe, invoice_id="buyer@example.invalid"),
                       dict(safe, external_send="SENT"), dict(safe, environment="production"), None):
            async def faulty(_payload, _request_id):
                return result
            self.request = self.review(self.session)
            with patch.object(self.adapter, "create_invoice_draft", faulty):
                await self.assert_boundary(code="provider_response_invalid")

    async def test_attempt_limit_unchanged(self):
        self.session.invoice_attempts = 5
        await self.assert_boundary(code="invoice_attempt_limit")
        self.assertIn(self.request["review_token"], self.session.invoice_reviews)

    async def test_http_existing_route_calls_gateway(self):
        app = create_app(store=self.store, paypal=self.adapter)
        calls = []
        original = app.state.paypal_tools.invoke
        async def spy(method, arguments, *, session):
            calls.append((method, session is self.session))
            return await original(method, arguments, session=session)
        app.state.paypal_tools.invoke = spy
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001)) as client:
            response = client.post("/api/v1/paypal/invoices/draft", json=self.request,
                                   headers={"Origin": "http://localhost:5173", "X-Demo-Session": self.session.session_id,
                                            "X-CSRF-Token": self.session.csrf_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(calls, [("create_invoice", True)])

    async def test_optional_missing_or_mismatched_runtime_typed(self):
        with patch("app.paypal_tools.importlib.metadata.version", return_value="wrong"):
            with self.assertRaises(BoundaryError) as captured:
                create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
        self.assertEqual((captured.exception.status, captured.exception.code), (503, "tool_runtime_unavailable"))
        with patch("app.paypal_tools.importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError):
            with self.assertRaises(BoundaryError) as captured:
                create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
        self.assertEqual(captured.exception.code, "tool_runtime_unavailable")

    @unittest.skipUnless(sdk_available(), "optional pinned SDK absent in formal runtime")
    async def test_actual_sdk_callback_schema_and_context_no_authority(self):
        import requests
        from agents import FunctionTool
        with patch.object(requests.sessions.Session, "request", side_effect=AssertionError("SDK transport forbidden")):
            tool = create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
            self.assertIsInstance(tool, FunctionTool)
            self.assertEqual(tool.name, "create_invoice")
            self.assertEqual(set(tool.params_json_schema["properties"]), {"description", "amount", "currency"})
            self.assertFalse(tool.params_json_schema["additionalProperties"])
            self.assertTrue(tool.strict_json_schema)
            for key in ("review_token", "payload_digest", "method", "session", "environment", "url", "context"):
                with self.assertRaises(BoundaryError):
                    await tool.on_invoke_tool(object(), json.dumps(dict(self.payload, **{key: "untrusted"})))
            with self.assertRaises(BoundaryError):
                await tool.on_invoke_tool({"session": self.session}, json.dumps(dict(self.payload, amount="11.00")))
            result = json.loads(await tool.on_invoke_tool({"environment": "production", "session": "forged"}, json.dumps(self.payload)))
            self.assertEqual(result["status"], "DRAFT")
            with self.assertRaises(BoundaryError):
                await tool.on_invoke_tool(None, json.dumps(self.payload))
        self.assertEqual(len(self.calls), 2)

    @unittest.skipUnless(sdk_available(), "optional pinned SDK absent in formal runtime")
    async def test_actual_sdk_reset_expiry_parallel_and_captured_copy(self):
        tool = create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
        self.request["amount"] = "999.00"
        outcomes = await asyncio.gather(*(tool.on_invoke_tool(None, json.dumps(self.payload)) for _index in range(4)), return_exceptions=True)
        self.assertEqual(sum(type(result) is str for result in outcomes), 1)
        self.request = self.review(self.session)
        tool = create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
        self.store.inject(self.session, "reset")
        with self.assertRaises(BoundaryError):
            await tool.on_invoke_tool(None, json.dumps(self.payload))
        self.request = self.review(self.session)
        tool = create_official_invoice_tool(self.gateway, session=self.session, reviewed_request=self.request)
        self.clock.now += timedelta(seconds=120)
        with self.assertRaises(BoundaryError):
            await tool.on_invoke_tool(None, json.dumps(self.payload))


if __name__ == "__main__":
    unittest.main()
