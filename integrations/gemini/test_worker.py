"""Offline fake-client tests for the dedicated Python 3.12 Gemini worker."""

from __future__ import annotations

import asyncio
from copy import deepcopy
import json
import os
from pathlib import Path
import socket
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch


PROFILE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PROFILE_ROOT.parents[1]
sys.path.insert(0, str(PROFILE_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import worker
from app import ai_brief as host


VALID_BRIEF = {
    "summary": "A synthetic item-not-received dispute has an authored timeline that requires human review.",
    "evidence_points": ["Carrier and payment-provider events have not been verified."],
    "missing_evidence": ["Verified carrier events are missing."],
    "citation_ids": ["PP-REASONS-INR", "PP-EVIDENCE-TRACKING"],
}


class FakePart:
    text = json.dumps(VALID_BRIEF)
    thought = False
    function_call = None
    function_response = None
    executable_code = None
    code_execution_result = None
    inline_data = None
    file_data = None
    video_metadata = None
    media_resolution = None
    tool_call = None
    tool_response = None
    part_metadata = None
    audio_transcription = None
    media_processing = None
    speech_metadata = None

    @property
    def thought_signature(self):
        raise AssertionError("opaque thought signature must not be accessed")


def provider_response(brief=None, *, finish="STOP", model="gemini-3.8-flash", response_id="resp-test-1", part=None):
    selected = part or FakePart()
    if brief is not None:
        selected = deepcopy(selected)
        selected.text = json.dumps(brief)
    candidate = SimpleNamespace(
        finish_reason=finish,
        content=SimpleNamespace(role="model", parts=[selected]),
        grounding_metadata=None,
        url_context_metadata=None,
        citation_metadata=None,
    )
    return SimpleNamespace(
        candidates=[candidate],
        model_version=model,
        response_id=response_id,
        prompt_feedback=None,
        automatic_function_calling_history=None,
        sdk_http_response=SimpleNamespace(private="must-not-persist"),
    )


class FakeModels:
    def __init__(self, response=None, error=None):
        self.response = response or provider_response()
        self.error = error
        self.calls = []

    async def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.response


class FakeAsyncClient:
    def __init__(self, models, close_error=None):
        self.models = models
        self.closed = False
        self.close_error = close_error

    async def __aenter__(self):
        return self

    async def __aexit__(self, _kind, _value, _traceback):
        await self.aclose()

    async def aclose(self):
        self.closed = True
        if self.close_error is not None:
            raise self.close_error


class FakeParentClient:
    def __init__(self, response=None, error=None, close_error=None):
        self.models = FakeModels(response=response, error=error)
        self.aio = FakeAsyncClient(self.models, close_error=close_error)
        self.closed = False

    def close(self):
        self.closed = True


def adapter_for(parent):
    return worker.GeminiWorkerAdapter(
        config_loader=lambda: worker.GeminiConfig(True, object(), "synthetic-project"),
        client_factory=lambda _config: parent,
    )


class GeminiWorkerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def test_sdk_schema_and_fixed_identity(self):
        worker.assert_sdk_part_schema()
        self.assertEqual(worker.SDK_VERSION, "2.28.0")
        self.assertEqual(host.MODEL, "gemini-3.8-flash")
        self.assertEqual(host.PROVIDER_BACKEND, "GEMINI_VERTEX_AI")
        self.assertEqual(host.API_VERSION, "v1")
        self.assertEqual(host.LOCATION, "global")

    async def test_injected_client_is_called_once_and_never_reads_signature(self):
        parent = FakeParentClient()
        result = await adapter_for(parent).generate("dispute_mediation")
        self.assertEqual(result["execution_evidence"], "SYNTHETIC_TEST_RESPONSE")
        self.assertEqual(result["prompt_contract_id"], host.PROMPT_CONTRACT_ID)
        self.assertEqual(result["prompt_contract_digest"], host.PROMPT_CONTRACT_DIGEST)
        self.assertEqual(result["brief"], VALID_BRIEF)
        self.assertEqual(len(parent.models.calls), 1)
        self.assertTrue(parent.aio.closed)
        self.assertTrue(parent.closed)
        call = parent.models.calls[0]
        self.assertEqual(call["model"], "gemini-3.8-flash")
        self.assertEqual(call["config"].tools, [])
        self.assertTrue(call["config"].automatic_function_calling.disable)
        self.assertFalse(call["config"].thinking_config.include_thoughts)
        self.assertEqual(str(call["config"].thinking_config.thinking_level), "ThinkingLevel.LOW")

    def test_operator_config_disabled_never_reads_adc(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
            worker.google.auth, "default", side_effect=AssertionError("ADC must not run")
        ):
            self.assertEqual(worker.operator_gemini_config(), worker.GeminiConfig())

    def test_operator_config_rejects_each_ambiguous_environment_before_adc(self):
        for name in worker._FORBIDDEN_ENVIRONMENT:
            with self.subTest(name=name), patch.dict(
                os.environ,
                {
                    "PAYGUARD_GEMINI_OUTBOUND": "enabled",
                    "PAYGUARD_VERTEX_PROJECT": "synthetic-project",
                    name: "present",
                },
                clear=True,
            ), patch.object(
                worker.google.auth, "default", side_effect=AssertionError("ADC must not run")
            ), self.assertRaises(host.AiBriefError) as caught:
                worker.operator_gemini_config()
            self.assertEqual(caught.exception.code, "ai_configuration_ambiguous")

    def test_operator_config_uses_adc_without_exposing_values(self):
        credentials = object()
        with patch.dict(
            os.environ,
            {
                "PAYGUARD_GEMINI_OUTBOUND": "enabled",
                "PAYGUARD_VERTEX_PROJECT": "synthetic-project",
            },
            clear=True,
        ), patch.object(
            worker.google.auth, "default", return_value=(credentials, None)
        ) as default:
            config = worker.operator_gemini_config()
        self.assertTrue(config.enabled)
        self.assertIs(config.credentials, credentials)
        self.assertEqual(config.project, "synthetic-project")
        self.assertNotIn("synthetic-project", repr(config))
        default.assert_called_once_with(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    def test_operator_config_requires_valid_project_before_adc(self):
        for environment, code in (
            ({"PAYGUARD_GEMINI_OUTBOUND": "enabled"}, "ai_not_configured"),
            (
                {
                    "PAYGUARD_GEMINI_OUTBOUND": "enabled",
                    "PAYGUARD_VERTEX_PROJECT": "INVALID_PROJECT",
                },
                "ai_configuration_invalid",
            ),
        ):
            with self.subTest(code=code), patch.dict(
                os.environ, environment, clear=True
            ), patch.object(
                worker.google.auth, "default", side_effect=AssertionError("ADC must not run")
            ), self.assertRaises(host.AiBriefError) as caught:
                worker.operator_gemini_config()
            self.assertEqual(caught.exception.code, code)

    def test_operator_config_rejects_discovered_project_conflict(self):
        with patch.dict(
            os.environ,
            {
                "PAYGUARD_GEMINI_OUTBOUND": "enabled",
                "PAYGUARD_VERTEX_PROJECT": "synthetic-project",
            },
            clear=True,
        ), patch.object(
            worker.google.auth, "default", return_value=(object(), "different-project")
        ), self.assertRaises(host.AiBriefError) as caught:
            worker.operator_gemini_config()
        self.assertEqual(caught.exception.code, "ai_configuration_ambiguous")

    def test_native_client_disables_retry_and_environment_routing(self):
        captured = {}

        def constructor(**kwargs):
            captured.update(kwargs)
            return object()

        with patch.object(worker.genai, "Client", side_effect=constructor):
            worker._native_client(worker.GeminiConfig(True, object(), "synthetic-project"))
        self.assertTrue(captured["enterprise"])
        self.assertEqual(captured["location"], "global")
        options = captured["http_options"]
        self.assertEqual(options.api_version, "v1")
        self.assertEqual(options.timeout, 45_000)
        self.assertEqual(options.retry_options.attempts, 1)
        self.assertFalse(options.client_args["trust_env"])
        self.assertFalse(options.client_args["follow_redirects"])
        self.assertFalse(options.async_client_args["trust_env"])
        self.assertFalse(options.async_client_args["follow_redirects"])

    async def test_response_shape_finish_metadata_tools_and_thoughts_fail_closed(self):
        variants = []
        variants.append(SimpleNamespace(candidates=[], prompt_feedback=None, automatic_function_calling_history=None))
        variants.append(provider_response(finish="MAX_TOKENS"))
        metadata = provider_response()
        metadata.candidates[0].grounding_metadata = object()
        variants.append(metadata)
        history = provider_response()
        history.automatic_function_calling_history = [object()]
        variants.append(history)
        thought = provider_response()
        thought.candidates[0].content.parts[0] = SimpleNamespace(
            text=json.dumps(VALID_BRIEF), thought=True, **{name: None for name in worker._FORBIDDEN_PART_FIELDS}
        )
        variants.append(thought)
        tool = provider_response()
        tool.candidates[0].content.parts[0] = SimpleNamespace(
            text=json.dumps(VALID_BRIEF), thought=False,
            **{name: (object() if name == "function_call" else None) for name in worker._FORBIDDEN_PART_FIELDS},
        )
        variants.append(tool)
        for response in variants:
            with self.subTest(response=response), self.assertRaises(host.AiBriefError) as caught:
                await adapter_for(FakeParentClient(response=response)).generate("dispute_mediation")
            self.assertEqual(caught.exception.code, "ai_response_invalid")

    async def test_model_citations_schema_and_privacy_fail_closed(self):
        variants = []
        variants.append(provider_response(model="other-model"))
        wrong = deepcopy(VALID_BRIEF)
        wrong["citation_ids"] = ["PP-REASONS-INR"]
        variants.append(provider_response(wrong))
        unsafe = deepcopy(VALID_BRIEF)
        unsafe["summary"] = "buyer@example.invalid"
        variants.append(provider_response(unsafe))
        empty = deepcopy(VALID_BRIEF)
        empty["missing_evidence"] = []
        variants.append(provider_response(empty))
        for response in variants:
            with self.subTest(response=response), self.assertRaises(host.AiBriefError) as caught:
                await adapter_for(FakeParentClient(response=response)).generate("dispute_mediation")
            self.assertEqual(caught.exception.code, "ai_response_invalid")

    async def test_provider_and_close_failures_are_sanitized(self):
        for parent in (
            FakeParentClient(error=RuntimeError("private provider message")),
            FakeParentClient(close_error=RuntimeError("private close message")),
        ):
            with self.subTest(parent=parent), self.assertRaises(host.AiBriefError) as caught:
                await adapter_for(parent).generate("dispute_mediation")
            self.assertEqual(caught.exception.code, "ai_provider_failure")
            self.assertNotIn("private", str(caught.exception))

    async def test_protocol_is_strict_bounded_and_sanitized(self):
        parent = FakeParentClient()
        adapter = adapter_for(parent)
        request = host.worker_request("dispute_mediation")
        raw = await worker.run_protocol(request, adapter)
        envelope = host.strict_json(raw)
        self.assertEqual(envelope["status"], "ok")
        self.assertEqual(envelope["result"]["execution_evidence"], "SYNTHETIC_TEST_RESPONSE")
        self.assertNotIn("response_id", json.dumps(envelope))
        self.assertNotIn("synthetic-project", json.dumps(envelope))
        for invalid in (
            b"not-json",
            b'{"stage":"dispute_mediation","stage":"dispute_mediation"}',
            b'{"stage":NaN}',
            b"x" * (worker.MAX_STDIN_BYTES + 1),
            host.canonical_json({"operation": "generate_fixed_brief", "schema_version": "1.0", "stage": "unknown"}),
            host.canonical_json({"operation": "other", "schema_version": "1.0", "stage": "dispute_mediation"}),
        ):
            with self.subTest(length=len(invalid)):
                error = host.strict_json(await worker.run_protocol(invalid, adapter))
                self.assertEqual(error["status"], "error")
                self.assertEqual(error["result"]["code"], "ai_response_invalid")

    async def test_protocol_carries_closed_session_facts(self):
        facts = {"reason": "INR", "due_state": "OPEN",
                 "requirements": [{"evidence_type": "PROOF_OF_FULFILLMENT", "state": "STRUCTURALLY_PRESENT"}]}
        envelope = host.strict_json(await worker.run_protocol(host.worker_request("dispute_mediation", facts), adapter_for(FakeParentClient())))
        self.assertEqual(envelope["status"], "ok")
        context, digest, _ = host.build_fixed_context("dispute_mediation", facts)
        self.assertEqual(envelope["result"]["fixture_id"], host.SESSION_FIXTURE_ID)
        self.assertEqual(envelope["result"]["context_digest"], digest)
        self.assertEqual(envelope["result"]["limitations"], list(host.SESSION_LIMITATIONS))
        for invalid in (dict(facts, note="free text"), dict(facts, reason="SNAD"), {"transaction_count": 50, "ratio": "5.00", "threshold": "3.50"}):
            with self.subTest(facts=invalid):
                raw = host.canonical_json({"operation": "generate_fixed_brief", "schema_version": "1.0",
                                           "stage": "dispute_mediation", "session_facts": invalid})
                error = host.strict_json(await worker.run_protocol(raw, adapter_for(FakeParentClient())))
                self.assertEqual(error["status"], "error")
                self.assertEqual(error["result"]["code"], "ai_response_invalid")

    async def test_cancellation_propagates_and_closes_client(self):
        gate = asyncio.Event()

        class PendingModels(FakeModels):
            async def generate_content(self, **kwargs):
                self.calls.append(kwargs)
                await gate.wait()

        parent = FakeParentClient()
        parent.models = PendingModels()
        parent.aio.models = parent.models
        task = asyncio.create_task(adapter_for(parent).generate("dispute_mediation"))
        await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(parent.aio.closed)
        self.assertTrue(parent.closed)

    def test_constructor_provenance_is_immutable(self):
        adapter = worker.GeminiWorkerAdapter()
        with self.assertRaises(AttributeError):
            adapter._GeminiWorkerAdapter__constructor_provenance = object()
        with self.assertRaises(AttributeError):
            del adapter._GeminiWorkerAdapter__constructor_provenance


if __name__ == "__main__":
    unittest.main()


GUIDE_REQUEST = {
    "task": "map_clauses",
    "contract": 2,
    "scenario": "dispute",
    "clauses": ["I shipped it last Monday"],
    "slots": {"ship_date": "MISSING", "carrier": "MISSING", "buyer_comms": "MISSING"},
}
GUIDE_REPLY = '{"v":2,"u":[{"c":"ship_date","k":0,"s":"P","w":"MON","r":"LAST","h":"EXACT","b":"STATED","a":"SELLER"}]}'


def guide_adapter_for(parent):
    return worker.GeminiGuideWorkerAdapter(
        config_loader=lambda: worker.GeminiConfig(True, object(), "synthetic-project"),
        client_factory=lambda _config: parent,
    )


def guide_response(text):
    part = deepcopy(FakePart())
    part.text = text
    return provider_response(part=part)


class GeminiGuideWorkerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    async def test_guide_call_uses_its_situation_prompt_and_contract_2_schema(self):
        from app import guide_model
        parent = FakeParentClient(response=guide_response(GUIDE_REPLY))
        result = await guide_adapter_for(parent).map_clauses(deepcopy(GUIDE_REQUEST))
        self.assertEqual(result, {"reply": GUIDE_REPLY, "prompt_sha256": guide_model.guide_prompt("dispute")["sha256"], "model": host.MODEL})
        self.assertEqual(len(parent.models.calls), 1)
        call = parent.models.calls[0]
        self.assertEqual(call["config"].system_instruction, guide_model.guide_prompt("dispute")["text"])
        self.assertEqual(call["config"].tools, [])
        self.assertTrue(call["config"].automatic_function_calling.disable)
        schema = call["config"].response_json_schema
        self.assertEqual(schema["properties"]["u"]["items"]["required"], ["c", "k", "s", "w", "r", "h", "b", "a"])
        self.assertEqual(json.loads(call["contents"][0].parts[0].text), GUIDE_REQUEST)
        self.assertTrue(parent.aio.closed and parent.closed)

    async def test_guide_reply_failing_the_closed_contract_is_rejected(self):
        for text in ('{"v":2,"u":[{"c":"ship_date","k":0,"s":"DONE","b":"STATED","a":"SELLER"}]}', "not json",
                     '{"v":2,"u":[]}' + " " * 600):
            with self.subTest(text=text[:30]), self.assertRaises(host.AiBriefError) as caught:
                await guide_adapter_for(FakeParentClient(response=guide_response(text))).map_clauses(deepcopy(GUIDE_REQUEST))
            self.assertEqual(caught.exception.code, "ai_response_invalid")

    async def test_guide_request_with_extra_text_never_reaches_the_client(self):
        parent = FakeParentClient(response=guide_response(GUIDE_REPLY))
        request = dict(deepcopy(GUIDE_REQUEST), history=["earlier seller text"])
        with self.assertRaises(host.AiBriefError):
            await guide_adapter_for(parent).map_clauses(request)
        self.assertEqual(parent.models.calls, [])

    async def test_protocol_dispatches_guide_operation_and_keeps_brief_limit(self):
        parent = FakeParentClient(response=guide_response(GUIDE_REPLY))
        raw = host.canonical_json({"operation": "map_guide_clauses", "schema_version": "1.0", "request": GUIDE_REQUEST})
        envelope = json.loads(await worker.run_protocol(raw, guide_adapter=guide_adapter_for(parent)))
        self.assertEqual(envelope["status"], "ok")
        self.assertEqual(envelope["result"]["reply"], GUIDE_REPLY)
        oversized_brief = host.canonical_json({"operation": "generate_fixed_brief", "schema_version": "1.0", "stage": "dispute_mediation" + " " * 600})
        self.assertEqual(json.loads(await worker.run_protocol(oversized_brief))["status"], "error")


class GeminiGuideConstantTests(unittest.TestCase):
    def test_worker_guide_constants_match_the_host(self):
        from app import guide_model
        self.assertEqual(worker.GUIDE_OPERATION, guide_model.GUIDE_OPERATION)
        self.assertEqual(worker.MAX_GUIDE_REQUEST_BYTES, guide_model.MAX_GUIDE_REQUEST_BYTES)


SYNTHETIC_KEY = "AIzaSyntheticTestKey0123456789abcdefXYZ"  # shape of an AI Studio key; not a real key


def api_key_adapter_for(parent):
    return worker.GeminiGuideWorkerAdapter(
        config_loader=lambda: worker.GeminiApiKeyConfig(True, SYNTHETIC_KEY),
        client_factory=lambda _config: parent,
    )


class GeminiGuideApiKeyTransportTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def environment(self, **extra):
        return patch.dict(os.environ, {"PAYGUARD_GEMINI_TRANSPORT": "api_key", "GEMINI_API_KEY": SYNTHETIC_KEY, **extra}, clear=True)

    def test_transport_is_explicit_and_never_mixed_with_vertex(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": SYNTHETIC_KEY}, clear=True):
            self.assertEqual(worker.operator_guide_config(), worker.GeminiConfig())  # no transport flag: Vertex path, disabled
        with self.environment():
            config = worker.operator_guide_config()
        self.assertEqual((type(config), config.enabled, config.api_key), (worker.GeminiApiKeyConfig, True, SYNTHETIC_KEY))
        self.assertNotIn(SYNTHETIC_KEY, repr(config))
        for name in ("PAYGUARD_GEMINI_OUTBOUND", "PAYGUARD_VERTEX_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_API_KEY", "HTTPS_PROXY"):
            with self.subTest(name=name), self.environment(**{name: "present"}), self.assertRaises(host.AiBriefError) as caught:
                worker.operator_guide_config()
            self.assertEqual(caught.exception.code, "ai_configuration_ambiguous")
        for key in (None, "short", "has space in it 0123456789"):
            values = {"PAYGUARD_GEMINI_TRANSPORT": "api_key", **({} if key is None else {"GEMINI_API_KEY": key})}
            with self.subTest(key=key), patch.dict(os.environ, values, clear=True), self.assertRaises(host.AiBriefError) as caught:
                worker.operator_guide_config()
            self.assertEqual(caught.exception.code, "ai_not_configured")
        with patch.dict(os.environ, {"PAYGUARD_GEMINI_TRANSPORT": "both"}, clear=True), self.assertRaises(host.AiBriefError):
            worker.operator_guide_config()

    async def test_request_and_validation_are_identical_to_the_vertex_path(self):
        from app import guide_model
        vertex_parent = FakeParentClient(response=guide_response(GUIDE_REPLY))
        key_parent = FakeParentClient(response=guide_response(GUIDE_REPLY))
        vertex = await guide_adapter_for(vertex_parent).map_clauses(deepcopy(GUIDE_REQUEST))
        keyed = await api_key_adapter_for(key_parent).map_clauses(deepcopy(GUIDE_REQUEST))
        self.assertEqual(vertex, keyed)
        first, second = vertex_parent.models.calls[0], key_parent.models.calls[0]
        self.assertEqual(first["model"], second["model"])
        self.assertEqual(first["contents"][0].parts[0].text, second["contents"][0].parts[0].text)
        self.assertEqual(first["config"].model_dump(), second["config"].model_dump())
        self.assertEqual(second["config"].temperature, 0.0)
        self.assertEqual(str(second["config"].thinking_config.thinking_level), "ThinkingLevel.MEDIUM")
        self.assertEqual(second["config"].system_instruction, guide_model.guide_prompt(GUIDE_REQUEST["scenario"])["text"])
        for text in ('{"v":2,"u":[{"c":"ship_date","k":0,"s":"DONE","b":"STATED","a":"SELLER"}]}', "not json"):
            with self.subTest(text=text), self.assertRaises(host.AiBriefError) as caught:
                await api_key_adapter_for(FakeParentClient(response=guide_response(text))).map_clauses(deepcopy(GUIDE_REQUEST))
            self.assertEqual(caught.exception.code, "ai_response_invalid")

    async def test_model_identity_is_checked_and_a_versioned_name_is_accepted(self):
        for model, accepted in (("gemini-3.8-flash", True), ("gemini-3.8-flash-001", True), ("gemini-3.8-pro", False), ("other", False)):
            response = guide_response(GUIDE_REPLY)
            response.model_version = model
            with self.subTest(model=model):
                if accepted:
                    await api_key_adapter_for(FakeParentClient(response=response)).map_clauses(deepcopy(GUIDE_REQUEST))
                else:
                    with self.assertRaises(host.AiBriefError):
                        await api_key_adapter_for(FakeParentClient(response=response)).map_clauses(deepcopy(GUIDE_REQUEST))
        response = guide_response(GUIDE_REPLY)
        response.response_id = None
        await api_key_adapter_for(FakeParentClient(response=response)).map_clauses(deepcopy(GUIDE_REQUEST))

    async def test_key_never_appears_in_errors_responses_or_logs(self):
        import logging
        records = []
        handler = logging.Handler(level=logging.DEBUG)
        handler.emit = lambda record: records.append(record.getMessage() + " ".join(map(str, record.args or ())))
        root = logging.getLogger()
        previous = root.level
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        self.addCleanup(root.removeHandler, handler)
        self.addCleanup(root.setLevel, previous)
        raw = host.canonical_json({"operation": "map_guide_clauses", "schema_version": "1.0", "request": GUIDE_REQUEST})
        leaking = [
            FakeParentClient(error=RuntimeError(f"401 invalid key {SYNTHETIC_KEY}")),
            FakeParentClient(error=TimeoutError(SYNTHETIC_KEY)),
            FakeParentClient(response=guide_response(GUIDE_REPLY), close_error=RuntimeError(SYNTHETIC_KEY)),
            FakeParentClient(response=guide_response('{"v":2,"u":[],"k":"' + SYNTHETIC_KEY + '"}')),
        ]
        for parent in leaking:
            output = await worker.run_protocol(raw, guide_adapter=api_key_adapter_for(parent))
            self.assertNotIn(SYNTHETIC_KEY.encode(), output)
            self.assertEqual(json.loads(output)["status"], "error")
        ok = await worker.run_protocol(raw, guide_adapter=api_key_adapter_for(FakeParentClient(response=guide_response(GUIDE_REPLY))))
        self.assertNotIn(SYNTHETIC_KEY.encode(), ok)
        self.assertFalse([record for record in records if SYNTHETIC_KEY in record])

    def test_native_client_receives_the_key_and_ignores_proxy_settings(self):
        captured = {}

        def fake_client(**kwargs):
            captured.update(kwargs)
            return SimpleNamespace(aio=None, close=lambda: None)
        with patch.object(worker.genai, "Client", side_effect=fake_client):
            worker._native_api_key_client(worker.GeminiApiKeyConfig(True, SYNTHETIC_KEY))
        self.assertEqual(captured["api_key"], SYNTHETIC_KEY)
        self.assertNotIn("vertexai", captured)
        self.assertNotIn("project", captured)
        options = captured["http_options"]
        self.assertFalse(options.client_args["trust_env"])
        self.assertFalse(options.async_client_args["follow_redirects"])
        self.assertEqual(options.retry_options.attempts, 1)
        from app import guide_model
        self.assertEqual(options.timeout, guide_model.GUIDE_HTTP_TIMEOUT_SECONDS * 1000)

    def test_timeout_ladder_stays_below_the_governed_deadline(self):
        from app import guide_model
        self.assertLess(guide_model.GUIDE_HTTP_TIMEOUT_SECONDS, guide_model.GUIDE_PROVIDER_TIMEOUT_SECONDS)
        self.assertLess(guide_model.GUIDE_PROVIDER_TIMEOUT_SECONDS, guide_model.GUIDE_WORKER_TIMEOUT_SECONDS)
        # guide_routes.GUIDE_MODEL_DEADLINE_SECONDS is 30 (pinned in tests/test_guide_live_contract.py); this profile
        # venv has no FastAPI, so the route module is not imported here.
        self.assertLess(guide_model.GUIDE_WORKER_TIMEOUT_SECONDS, 30)


# ---- AG Studio agent turn (dashboard built-in agents, local live mode only) ----------------------------------
def studio_turn_document(tools=None, items=None, tool_choice="auto", response_format=None, signature=None):
    from app import studio_agent
    turn = {
        "instructions": "You arrange a synthetic dashboard with the tools given.",
        "items": items or [{"kind": "user", "text": "Make a widget comparing cases by days to due"}],
        "tools": tools if tools is not None else [{"name": "add_widget", "description": "Add a widget.",
                                                   "parameters": {"type": "object", "properties": {"widgetId": {"type": "string"}}}}],
        "tool_choice": tool_choice,
        "response_format": response_format or {"type": "text"},
    }
    store = studio_agent.SignatureStore()
    for item in turn["items"]:
        if item["kind"] == "call" and signature:
            store.keep("session-1", item["call_id"], signature)
    return json.loads(studio_agent.worker_request(studio_agent.validate_turn(turn), "session-1", store))


def studio_part(**fields):
    part = SimpleNamespace(**{name: None for name in worker._EXPECTED_PART_FIELDS})
    for name, value in fields.items():
        setattr(part, name, value)
    return part


def studio_response(*parts, finish="STOP"):
    response = provider_response(part=parts[0], finish=finish)
    response.candidates[0].content.parts = list(parts)
    return response


def studio_adapter_for(parent):
    return worker.GeminiStudioWorkerAdapter(
        config_loader=lambda: worker.GeminiApiKeyConfig(True, SYNTHETIC_KEY),
        client_factory=lambda _config: parent,
    )


class GeminiStudioWorkerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    async def test_function_call_turn_round_trips_tools_and_signatures(self):
        call = SimpleNamespace(name="add_widget", args={"widgetId": "days"}, id=None, partial_args=None, will_continue=None)
        parent = FakeParentClient(response=studio_response(
            studio_part(thought=True, text="private reasoning"),
            studio_part(function_call=call, thought_signature=b"sig-bytes"),
            studio_part(text="Placing the widget now.")))
        items = [{"kind": "user", "text": "Make a widget comparing cases by days to due"},
                 {"kind": "call", "call_id": "call_1", "name": "add_widget", "arguments": "{\"widgetId\": \"a\"}"},
                 {"kind": "result", "call_id": "call_1", "output": "Added widget a."},
                 {"kind": "context", "text": "The page is called readiness."}]
        document = studio_turn_document(items=items, signature="b2xkLXNpZw==")
        result = await studio_adapter_for(parent).turn(document)
        self.assertEqual(result["model"], host.MODEL)
        self.assertEqual(result["output"], [
            {"kind": "call", "name": "add_widget", "arguments": {"widgetId": "days"}, "signature": "c2lnLWJ5dGVz"},
            {"kind": "text", "text": "Placing the widget now."}])
        self.assertNotIn("private reasoning", json.dumps(result), "thought parts never leave the worker")
        sent = parent.models.calls[0]
        self.assertEqual(sent["model"], host.MODEL)
        config = sent["config"]
        self.assertEqual(config.tools[0].function_declarations[0].name, "add_widget")
        self.assertEqual(config.tool_config.function_calling_config.mode.value, "AUTO")
        self.assertTrue(config.automatic_function_calling.disable)
        self.assertIn("The page is called readiness.", config.system_instruction)
        roles = [content.role for content in sent["contents"]]
        self.assertEqual(roles, ["user", "model", "user"])
        model_part = sent["contents"][1].parts[0]
        self.assertEqual((model_part.function_call.name, model_part.thought_signature), ("add_widget", b"old-sig"))
        self.assertEqual(sent["contents"][2].parts[0].function_response.name, "add_widget")

    def test_studio_history_is_regrouped_into_signed_gemini_steps(self):
        # Live 2026-11-04 (502): the lead made two parallel calls; Gemini signed only the first. Studio replays a
        # step as call, result, call, result, which sent Gemini a second model step whose first call had no
        # signature. Delegates also start with calls Studio seeds itself (view_page, view_plan), never signed.
        from app import studio_agent
        tools = [{"name": name, "description": name, "parameters": {"type": "object"}}
                 for name in ("view_page", "view_plan", "rename_thread", "delegate_to", "add_widget")]
        seeded = "run-9c047e3c-5075-4d0d-8d5c-4f95495c9e96-preflight-"
        items = [{"kind": "user", "text": "Which reason code appears most often across the three cases?"}]
        for call_id, name in ((seeded + "0", "view_page"), (seeded + "1", "view_plan"), ("call_a", "rename_thread"),
                              ("call_b", "delegate_to"), ("call_c", "add_widget")):
            items += [{"kind": "call", "call_id": call_id, "name": name, "arguments": "{}"},
                      {"kind": "result", "call_id": call_id, "output": f"{name} done"}]
        items.insert(-2, {"kind": "assistant", "text": "Adding the widget."})
        store = studio_agent.SignatureStore()
        store.keep("session-1", "call_a", "c2lnLWE=")  # a step's first call: signed (sig-a)
        store.keep("session-1", "call_c", "c2lnLWM=")  # the next step, signed again (sig-c)
        turn = studio_agent.validate_turn({"instructions": "Arrange the dashboard.", "items": items, "tools": tools,
                                           "tool_choice": "auto", "response_format": {"type": "text"}})
        document = json.loads(studio_agent.worker_request(turn, "session-1", store))
        contents, _system = worker.GeminiStudioWorkerAdapter.contents(studio_agent.validate_worker_request(document))

        def shape(content):
            return [("call", part.function_call.name, part.thought_signature) if part.function_call
                    else ("result", part.function_response.name) if part.function_response else ("text", part.text)
                    for part in content.parts]
        self.assertEqual([(content.role, shape(content)) for content in contents], [
            ("user", [("text", "Which reason code appears most often across the three cases?")]),
            ("model", [("call", "view_page", worker.STUDIO_INJECTED_CALL_SIGNATURE), ("call", "view_plan", None)]),
            ("user", [("result", "view_page"), ("result", "view_plan")]),
            ("model", [("call", "rename_thread", b"sig-a"), ("call", "delegate_to", None)]),
            ("user", [("result", "rename_thread"), ("result", "delegate_to")]),
            ("model", [("text", "Adding the widget."), ("call", "add_widget", b"sig-c")]),
            ("user", [("result", "add_widget")]),
        ], "one model content per step, its first call signed, then one user content with every response")
        for index, content in enumerate(contents):
            calls = [part for part in content.parts if part.function_call]
            if content.role == "model" and calls:
                self.assertIsNotNone(calls[0].thought_signature)
                self.assertEqual(len(calls), len([part for part in contents[index + 1].parts if part.function_response]))

    async def test_tool_choice_maps_to_gemini_modes(self):
        for choice, mode, allowed in (("none", "NONE", None), ("required", "ANY", None), ({"name": "add_widget"}, "ANY", ["add_widget"])):
            parent = FakeParentClient(response=studio_response(studio_part(function_call=SimpleNamespace(name="add_widget", args={}))
                                                               if choice != "none" else studio_part(text="ok")))
            await studio_adapter_for(parent).turn(studio_turn_document(tool_choice=choice))
            config = parent.models.calls[0]["config"].tool_config.function_calling_config
            self.assertEqual((config.mode.value, config.allowed_function_names), (mode, allowed))

    async def test_unsafe_or_unexpected_replies_are_refused(self):
        bad_replies = (
            studio_response(studio_part(function_call=SimpleNamespace(name="delete_everything", args={}))),  # not advertised
            studio_response(studio_part(executable_code=SimpleNamespace(code="print(1)"))),
            studio_response(studio_part(text="cut off"), finish="MAX_TOKENS"),
            studio_response(studio_part(thought=True, text="only thoughts")),
            studio_response(studio_part(text="x" * 7000)),
        )
        for response in bad_replies:
            with self.assertRaises(host.AiBriefError):
                await studio_adapter_for(FakeParentClient(response=response)).turn(studio_turn_document())

    async def test_json_format_and_protocol_size_routing(self):
        parent = FakeParentClient(response=studio_response(studio_part(text='{"steps": []}')))
        document = studio_turn_document(response_format={"type": "json", "name": "Plan", "schema": {"type": "object"}}, tools=[])
        result = await studio_adapter_for(parent).turn(document)
        self.assertEqual(result["output"], [{"kind": "text", "text": '{"steps": []}'}])
        self.assertEqual(parent.models.calls[0]["config"].response_mime_type, "application/json")
        large = deepcopy(studio_turn_document())
        large["request"]["instructions"] = "x" * 20000
        raw = json.dumps(large, sort_keys=True, separators=(",", ":")).encode()
        self.assertGreater(len(raw), worker.MAX_GUIDE_REQUEST_BYTES)
        ok = json.loads(await worker.run_protocol(raw, studio_adapter=studio_adapter_for(FakeParentClient(response=studio_response(studio_part(text="ok"))))))
        self.assertEqual(ok["status"], "ok")
        other = json.dumps({"operation": "generate_fixed_brief", "schema_version": "1.0", "stage": "x" * 5000}).encode()
        self.assertEqual(json.loads(await worker.run_protocol(other))["status"], "error", "only the Studio turn may be large")


class WorkerUsageTests(unittest.IsolatedAsyncioTestCase):
    """(optimise r24) usage_metadata counts travel beside the result; never any text."""

    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def test_usage_metadata_keeps_bounded_ints_only(self):
        self.assertIsNone(worker._usage_metadata(SimpleNamespace()))
        response = SimpleNamespace(usage_metadata=SimpleNamespace(prompt_token_count=812, candidates_token_count=96,
                                                                  total_token_count=1240, cached_content_token_count=5))
        self.assertEqual(worker._usage_metadata(response),
                         {"prompt_token_count": 812, "candidates_token_count": 96, "total_token_count": 1240})
        odd = SimpleNamespace(usage_metadata=SimpleNamespace(prompt_token_count=True, candidates_token_count="9",
                                                             total_token_count=-1))
        self.assertIsNone(worker._usage_metadata(odd))

    async def test_studio_protocol_envelope_carries_usage_when_reported(self):
        response = studio_response(studio_part(text="ok"))
        response.usage_metadata = SimpleNamespace(prompt_token_count=10, candidates_token_count=2, total_token_count=12)
        raw = json.dumps(studio_turn_document(), sort_keys=True, separators=(",", ":")).encode()
        envelope = json.loads(await worker.run_protocol(raw, studio_adapter=studio_adapter_for(FakeParentClient(response=response))))
        self.assertEqual(envelope["status"], "ok")
        self.assertEqual(envelope["usage"], {"prompt_token_count": 10, "candidates_token_count": 2, "total_token_count": 12})
        plain = json.loads(await worker.run_protocol(raw, studio_adapter=studio_adapter_for(
            FakeParentClient(response=studio_response(studio_part(text="ok"))))))
        self.assertNotIn("usage", plain)
