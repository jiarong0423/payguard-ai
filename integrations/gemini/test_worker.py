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
