"""Governed Gemini turns for AG Studio's built-in agents: closed input, bounded output, caps, demo off.

Every test uses a fake worker (a callable returning a canned protocol envelope). No test starts a worker,
opens a network connection or needs a key.
"""

import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app import studio_agent as sa
from app.ai_brief import MODEL, canonical_json
from app.guide_model import ApiKeyProfileConfig
from app.main import MAX_BODY_BYTES, create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore
from payguard.controlled_fallback import Governor

ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
ADD_WIDGET = {"name": "add_widget", "description": "Add a widget to the grid.",
              "parameters": {"type": "object", "properties": {"widgetId": {"type": "string"}}, "required": ["widgetId"]}}


def turn(**overrides):
    body = {"instructions": "You arrange a synthetic dashboard with the tools given.",
            "items": [{"kind": "user", "text": "Make a widget comparing cases by days to due"}],
            "tools": [ADD_WIDGET], "tool_choice": "auto", "response_format": {"type": "text"}}
    body.update(overrides)
    return body


def envelope(*output, model=MODEL, status="ok"):
    result = {"output": list(output), "model": model}
    return canonical_json({"schema_version": "1.0", "status": status, "result": result if status == "ok" else {"code": "x", "status": 502}})


class FakeWorker:
    def __init__(self, *replies):
        self.replies, self.payloads = list(replies), []

    def __call__(self, payload: bytes) -> bytes:
        self.payloads.append(json.loads(payload))
        reply = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        if isinstance(reply, Exception):
            raise reply
        return reply


CALL = {"kind": "call", "name": "add_widget", "arguments": {"widgetId": "days"}, "signature": "c2lnLWJ5dGVz"}
TEXT = {"kind": "text", "text": "I added a widget comparing the two cases by days to due."}


class ValidationTests(unittest.TestCase):
    def test_closed_turn_is_accepted_as_is(self):
        self.assertEqual(sa.validate_turn(turn())["items"], [{"kind": "user", "text": "Make a widget comparing cases by days to due"}])

    def test_anything_outside_the_contract_is_refused(self):
        bad = [
            turn(extra=1),
            turn(items=[{"kind": "user", "text": "hi", "image": "x"}]),
            turn(items=[{"kind": "image", "url": "https://example.com/a.png"}]),
            turn(items=[{"kind": "assistant", "text": "only the model spoke"}]),
            turn(items=[{"kind": "user", "text": "q"}, {"kind": "result", "call_id": "c1", "output": "orphan"}]),
            turn(items=[{"kind": "user", "text": "x" * (sa.MAX_QUESTION_CHARS + 1)}]),
            turn(instructions="x" * (sa.MAX_INSTRUCTIONS_CHARS + 1)),
            turn(tools=[ADD_WIDGET, ADD_WIDGET]),
            turn(tools=[dict(ADD_WIDGET, name=f"tool_{index}") for index in range(sa.MAX_TOOLS + 1)]),
            turn(tools=[dict(ADD_WIDGET, name="Bad-Name")]),
            turn(tool_choice={"name": "not_advertised"}),
            turn(tool_choice="sometimes"),
            turn(response_format={"type": "xml"}),
            turn(tools=[dict(ADD_WIDGET, parameters={"a": json.loads("[" * 40 + "]" * 40)})]),
            turn(items=[{"kind": "user", "text": "q"}, {"kind": "call", "call_id": "c1", "name": "add_widget", "arguments": "[1]"}]),
            turn(items=[{"kind": "user", "text": "bell\x07"}]),
        ]
        for body in bad:
            with self.subTest(body=json.dumps(body)[:80]), self.assertRaises(sa.StudioAgentError) as caught:
                sa.validate_turn(body)
            self.assertEqual(caught.exception.code, "studio_turn_invalid")

    def test_turns_the_real_studio_loop_sends_are_accepted(self):
        # Live 2026-11-04: every turn of the data agent was refused (422) because create_expression's description
        # (Studio's operator catalogue, 4485 characters) was over a 4000 cap. Shapes below are as the real Studio
        # 3.0.0 loop sent them in an offline browser harness: the data agent's tools, a delegate's seeded preflight
        # calls, and the lead's parallel calls replayed interleaved with their results.
        catalogue = "Add a calculated column.\n" + "".join(f"- op_{index}: (datetime, datetime) => number\n" for index in range(120))
        self.assertGreater(len(catalogue), 4485)
        deep = {"type": "object"}
        for _ in range(10):  # depth 20, as execute_query's schema
            deep = {"type": "object", "properties": {"next": deep}}
        data_tools = [{"name": "create_expression", "description": catalogue, "parameters": {"type": "object"}},
                      {"name": "execute_query", "description": "Run a query.", "parameters": deep},
                      {"name": "complete_task", "description": "Finish.", "parameters": {"type": "object"}}]
        self.assertEqual(len(sa.validate_turn(turn(tools=data_tools))["tools"]), 3)
        preflight = "run-9c047e3c-5075-4d0d-8d5c-4f95495c9e96-preflight-0"
        parallel = [{"kind": "user", "text": "Which reason code appears most often across the three cases?"},
                    {"kind": "call", "call_id": preflight, "name": "add_widget", "arguments": "{}"},
                    {"kind": "result", "call_id": preflight, "output": "{\"success\":true}"},
                    {"kind": "call", "call_id": "call_" + "a" * 24, "name": "add_widget", "arguments": "{\"widgetId\":\"a\"}"},
                    {"kind": "result", "call_id": "call_" + "a" * 24, "output": "{\"success\":true}"},
                    {"kind": "call", "call_id": "call_" + "b" * 24, "name": "add_widget", "arguments": "{\"widgetId\":\"b\"}"},
                    {"kind": "result", "call_id": "call_" + "b" * 24, "output": "{\"success\":true,\"response\":\"(the delegate finished without a summary)\"}"}]
        self.assertEqual([item["kind"] for item in sa.validate_turn(turn(items=parallel))["items"]],
                         ["user", "call", "result", "call", "result", "call", "result"])
        with self.assertRaises(sa.StudioAgentError) as caught:
            sa.validate_turn(turn(tools=[dict(ADD_WIDGET, description="x" * (sa.MAX_TOOL_DESCRIPTION_CHARS + 1))]))
        self.assertEqual(caught.exception.code, "studio_turn_invalid", "the description cap still holds")
        with self.assertRaises(sa.StudioAgentError) as caught:
            sa.validate_turn(turn(tools=[dict(ADD_WIDGET, description=catalogue + "Mail jane@example.com")]))
        self.assertEqual(caught.exception.code, "studio_turn_personal_data", "long descriptions are still checked")

    def test_personal_data_in_the_question_is_refused(self):
        for text in ("Email jane.doe@example.com about case 2", "Call the buyer on 415 555 0199", "Card 4111 1111 1111 1111"):
            with self.subTest(text=text), self.assertRaises(sa.StudioAgentError) as caught:
                sa.validate_turn(turn(items=[{"kind": "user", "text": text}]))
            self.assertEqual(caught.exception.code, "studio_turn_personal_data")

    def test_studio_json_bounds(self):
        self.assertEqual(sa.studio_json(b'{"a":1}', 100), {"a": 1})
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b"x" * 101, b"", ("[" * 60 + "]" * 60).encode()):
            with self.assertRaises(sa.StudioAgentError):
                sa.studio_json(raw, 100 if len(raw) > 100 else 1000)


class ServiceTests(unittest.TestCase):
    def service(self, worker, clock=None):
        governor = Governor(clock=clock or (lambda: 0.0), max_calls=sa.STUDIO_CALLS_PER_SESSION, min_spacing=0.0)
        return sa.StudioAgentService(worker, governor=governor)

    def test_off_without_a_model(self):
        with self.assertRaises(sa.StudioAgentError) as caught:
            sa.StudioAgentService(None).turn("s1", turn())
        self.assertEqual(caught.exception.code, "studio_agents_off")

    def test_tool_call_round_trip_keeps_signatures_server_side(self):
        worker = FakeWorker(envelope(CALL, TEXT), envelope(TEXT))
        service = self.service(worker)
        output = service.turn("s1", turn())
        self.assertEqual([item["type"] for item in output], ["call", "text"])
        call = output[0]
        self.assertEqual((call["name"], json.loads(call["arguments"])), ("add_widget", {"widgetId": "days"}))
        self.assertRegex(call["call_id"], r"^call_[0-9a-f]{24}$")
        self.assertNotIn("c2lnLWJ5dGVz", json.dumps(output), "the thought signature never reaches the browser")
        self.assertEqual(worker.payloads[0]["operation"], sa.STUDIO_OPERATION)
        # Next turn: the browser returns the call and its result; the stored signature is re-attached for the worker.
        follow = turn(items=[{"kind": "user", "text": "Make a widget comparing cases by days to due"},
                             {"kind": "call", "call_id": call["call_id"], "name": "add_widget", "arguments": call["arguments"]},
                             {"kind": "result", "call_id": call["call_id"], "output": "Added widget days (grid)."}])
        service.turn("s1", follow)
        sent_call = worker.payloads[1]["request"]["items"][1]
        self.assertEqual((sent_call["signature"], sent_call["arguments"]), ("c2lnLWJ5dGVz", {"widgetId": "days"}))
        self.assertEqual(sa.validate_worker_request(worker.payloads[1])["items"][1]["signature"], "c2lnLWJ5dGVz")
        # Another session cannot borrow it.
        service.turn("s2", follow)
        self.assertIsNone(worker.payloads[2]["request"]["items"][1]["signature"])

    def test_replies_are_bounded_and_closed(self):
        bad = [
            envelope({"kind": "call", "name": "delete_everything", "arguments": {}, "signature": None}),
            envelope({"kind": "text", "text": "x" * (sa.MAX_OUTPUT_TEXT_CHARS + 1)}),
            envelope(*([TEXT] * (sa.MAX_OUTPUT_ITEMS + 1))),
            envelope(),
            envelope(TEXT, model="another-model"),
            envelope({"kind": "call", "name": "add_widget", "arguments": {}, "signature": "not base64!"}),
            envelope({"kind": "image", "url": "https://example.com"}),
            b"not json",
        ]
        for raw in bad:
            with self.subTest(raw=raw[:60]), self.assertRaises(sa.StudioAgentError) as caught:
                self.service(FakeWorker(raw)).turn("s1", turn())
            self.assertEqual(caught.exception.code, "studio_agent_reply_invalid")
        with self.assertRaises(sa.StudioAgentError):
            self.service(FakeWorker(envelope(TEXT))).turn("s1", turn(response_format={"type": "json", "name": "Plan", "schema": {"type": "object"}}))
        with self.assertRaises(sa.StudioAgentError):
            self.service(FakeWorker(envelope(TEXT))).turn("s1", turn(tool_choice="required"))
        with self.assertRaises(sa.StudioAgentError) as caught:
            self.service(FakeWorker(envelope(TEXT, status="error"))).turn("s1", turn())
        self.assertEqual(caught.exception.code, "studio_agent_provider_failure")
        # (wo gemini run 2026-11-04) The worker's own reply checks are told apart from a provider failure.
        refused = canonical_json({"schema_version": "1.0", "status": "error", "result": {"code": "ai_response_invalid", "status": 502}})
        with self.assertRaises(sa.StudioAgentError) as caught:
            self.service(FakeWorker(refused)).turn("s1", turn())
        self.assertEqual(caught.exception.code, "studio_agent_reply_refused")

    def test_per_session_call_cap_and_breaker(self):
        service = self.service(FakeWorker(envelope(TEXT)))
        for _ in range(sa.STUDIO_CALLS_PER_SESSION):
            service.turn("busy", turn())
        with self.assertRaises(sa.StudioAgentError) as caught:
            service.turn("busy", turn())
        self.assertEqual(caught.exception.code, "studio_agent_limit")
        self.assertEqual(service.turn("calm", turn())[0]["type"], "text", "another session still gets turns")
        failing = self.service(FakeWorker(sa.StudioAgentError("studio_agent_provider_failure")))
        for _ in range(3):
            with self.assertRaises(sa.StudioAgentError):
                failing.turn("s1", turn())
        with self.assertRaises(sa.StudioAgentError) as caught:
            failing.turn("s1", turn())
        self.assertEqual(caught.exception.code, "studio_agent_unavailable", "breaker opens after repeated provider failures")

    def test_timeout_ladder_matches_the_guide(self):
        self.assertEqual(sa.TIMEOUT_LADDER, (25, 26, 28, 30.0))
        self.assertEqual(list(sa.TIMEOUT_LADDER), sorted(set(sa.TIMEOUT_LADDER)))


class ConfigurationTests(unittest.TestCase):
    def test_flag_off_inspects_nothing(self):
        def explode():
            raise AssertionError("no configuration may be read with the flag off")
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(sa.configured_studio_model(config_loader=explode, api_key_loader=explode))
        with patch.dict(os.environ, {"PAYGUARD_STUDIO_AGENTS": "gemini"}, clear=True):
            self.assertIsNone(sa.configured_studio_model(public_demo=True, config_loader=explode, api_key_loader=explode))

    def test_api_key_transport_builds_a_model_without_holding_the_key(self):
        config = ApiKeyProfileConfig(Path("/usr/bin/python3"), Path("/tmp/worker.py"))
        with patch.dict(os.environ, {"PAYGUARD_STUDIO_AGENTS": "gemini", "PAYGUARD_GEMINI_TRANSPORT": "api_key"}, clear=True):
            model = sa.configured_studio_model(api_key_loader=lambda: config)
        self.assertIsInstance(model, sa.StudioAgentModel)
        self.assertEqual(model.transport, "api_key")
        self.assertNotIn("key", repr(model).replace("api_key", ""))


class RouteTests(unittest.TestCase):
    def make(self, worker=None, env=None):
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(
            lambda request: (_ for _ in ()).throw(AssertionError("no provider call"))))
        with patch.dict(os.environ, env or {}, clear=True):
            app = create_app(store=SessionStore(), paypal=provider, studio_model=worker)
        client = TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55020), raise_server_exceptions=False)
        client.__enter__()
        self.addCleanup(client.__exit__, None, None, None)
        session = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        return app, client, headers

    def test_off_by_default(self):
        _app, client, headers = self.make()
        self.assertEqual(client.get(ROOT + "/studio/agent-status", headers=headers).json(),
                         {"built_in_agents": "off", "reason": "not_configured", "affects_decision": False})
        response = client.post(ROOT + "/studio/agent-turn", json=turn(), headers=headers)
        self.assertEqual((response.status_code, response.json()["error"]["code"]), (503, "studio_agents_off"))

    def test_live_turn_through_the_route(self):
        worker = FakeWorker(envelope(CALL, TEXT))
        _app, client, headers = self.make(worker)
        self.assertEqual(client.get(ROOT + "/studio/agent-status", headers=headers).json()["built_in_agents"], "live")
        big = turn(instructions="x" * 30000)  # larger than every other route's 16 KB body limit
        self.assertGreater(len(json.dumps(big)), MAX_BODY_BYTES)
        response = client.post(ROOT + "/studio/agent-turn", json=big, headers=headers)
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual((body["affects_decision"], [item["type"] for item in body["output"]]), (False, ["call", "text"]))
        self.assertNotIn("signature", response.text)
        self.assertEqual(client.post(ROOT + "/studio/agent-turn", json=turn(items=[{"kind": "user", "text": "mail a@b.com"}]),
                                     headers=headers).json()["error"]["code"], "studio_turn_personal_data")
        # The larger limit belongs to this route only.
        self.assertEqual(client.post(ROOT + "/aup/review", json={"description": "x" * 20000}, headers=headers).status_code, 413)
        self.assertEqual(client.post(ROOT + "/studio/agent-turn", json=turn(instructions="x" * 300000), headers=headers).status_code, 413)
        self.assertIn(client.post(ROOT + "/studio/agent-turn", json=turn(), headers={"Origin": ORIGIN}).status_code, (401, 403))

    def test_hosted_demo_refuses_before_any_model_call(self):
        worker = FakeWorker(envelope(TEXT))
        _app, client, headers = self.make(worker, env={"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": "payguard-demo.example.com"})
        response = client.post(ROOT + "/studio/agent-turn", json=turn(), headers=headers)
        self.assertEqual((response.status_code, response.json()["error"]["code"]), (503, "hosted_demo_disabled"))
        self.assertEqual(client.get(ROOT + "/studio/agent-status", headers=headers).json()["reason"], "hosted_demo")
        self.assertEqual(worker.payloads, [], "zero model calls on the hosted demo")


if __name__ == "__main__":
    unittest.main()
