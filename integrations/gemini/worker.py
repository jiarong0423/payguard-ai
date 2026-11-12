#!/usr/bin/env python3
"""Dedicated Python 3.12 Gemini worker for one fixed synthetic advisory call."""

from __future__ import annotations

import asyncio
import base64
import contextvars
from dataclasses import dataclass, field
from enum import Enum
import importlib
import os
from pathlib import Path
import re
import sys
from typing import Literal
import unicodedata


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import google.auth
from google import genai
from google.genai import types
from pydantic import ValidationError

from app.ai_brief import (
    API_VERSION,
    GENERATED_TEXT_INVENTORY,
    INSTRUCTIONS,
    LIMITATIONS,
    LOCATION,
    MAX_OUTPUT_TOKENS,
    MODEL,
    PROMPT_CONTRACT_DIGEST,
    PROMPT_CONTRACT_ID,
    PROVIDER_TIMEOUT_SECONDS,
    PROVIDER_BACKEND,
    WORKER_TIMEOUT_SECONDS,
    VERTEX_PROJECT_ENV,
    AiBriefError,
    AiBriefRequest,
    AiBriefResponse,
    GeneratedBrief,
    brief_limitations,
    build_fixed_context,
    build_logical_request,
    canonical_json,
    configured_vertex_project,
    fail,
    generated_text_matches_inventory,
    strict_json,
)


SDK_VERSION = "2.28.0"
MAX_STDIN_BYTES = 1024  # equals app.ai_brief.MAX_WORKER_BRIEF_BYTES
GUIDE_OPERATION = "map_guide_clauses"
MAX_GUIDE_REQUEST_BYTES = 2048  # equals app.guide_model.MAX_GUIDE_REQUEST_BYTES
STUDIO_OPERATION = "studio_agent_turn"
MAX_STUDIO_REQUEST_BYTES = 270336  # equals app.studio_agent.MAX_WORKER_REQUEST_BYTES
STUDIO_MAX_OUTPUT_TOKENS = 8192
STUDIO_TEMPERATURE = 0.2
# Gemini's documented thought signature for function calls the model did not make (injected history).
STUDIO_INJECTED_CALL_SIGNATURE = b"skip_thought_signature_validator"
# Parts a Studio reply may carry: text, function calls and their thought signatures. Thought parts are dropped.
_STUDIO_PART_FIELDS = frozenset({"text", "thought", "thought_signature", "function_call"})
_EXPECTED_PART_FIELDS = frozenset(
    {
        "audio_transcription",
        "code_execution_result",
        "executable_code",
        "file_data",
        "function_call",
        "function_response",
        "inline_data",
        "media_processing",
        "media_resolution",
        "part_metadata",
        "speech_metadata",
        "text",
        "thought",
        "thought_signature",
        "tool_call",
        "tool_response",
        "video_metadata",
    }
)
_FORBIDDEN_PART_FIELDS = (
    "function_call",
    "function_response",
    "executable_code",
    "code_execution_result",
    "inline_data",
    "file_data",
    "video_metadata",
    "media_resolution",
    "tool_call",
    "tool_response",
    "part_metadata",
    "audio_transcription",
    "media_processing",
    "speech_metadata",
)
_FORBIDDEN_ENVIRONMENT = frozenset(
    {
        "ALL_PROXY",
        "CLOUDSDK_CORE_PROJECT",
        "CURL_CA_BUNDLE",
        "GCLOUD_PROJECT",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_GENAI_USE_ENTERPRISE",
        "GOOGLE_GENAI_USE_VERTEXAI",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "OPENAI_API_KEY",
        "PAYGUARD_OPENAI_OUTBOUND",
        "PYTHONHOME",
        "PYTHONPATH",
        "REQUESTS_CA_BUNDLE",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "all_proxy",
        "curl_ca_bundle",
        "http_proxy",
        "https_proxy",
        "no_proxy",
        "requests_ca_bundle",
        "ssl_cert_dir",
        "ssl_cert_file",
    }
)
# (optimise r24) Token counts the SDK reported for this protocol run's provider call (usage_metadata), returned
# beside the result for the backend's per-session AI audit log. Counts only: never the prompt or the reply.
USAGE_FIELDS = ("prompt_token_count", "candidates_token_count", "total_token_count")
MAX_TOKEN_COUNT = 100_000_000  # equals app.ai_usage.MAX_TOKEN_COUNT
_CALL_USAGE: contextvars.ContextVar = contextvars.ContextVar("payguard_call_usage", default=None)
_UNSAFE_OUTPUT = (
    re.compile(r"(?i)\b(?:bearer\s+[A-Za-z0-9._~-]{12,}|(?:api|access|refresh)[_-]?key\s*[:=]\s*\S+)", re.ASCII),
    re.compile(r"(?<![A-Za-z0-9])(?:\+1[- .]?)?(?:\([2-9][0-9]{2}\)|[2-9][0-9]{2})[- .]?[0-9]{3}[- .]?[0-9]{4}(?![A-Za-z0-9])"),
    re.compile(r"(?<![0-9])[0-9]{3}-[0-9]{2}-[0-9]{4}(?![0-9])"),
    re.compile(r"(?i)\b\d{1,6}\s+[A-Za-z][A-Za-z .'-]{0,50}\s(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Boulevard|Blvd)\b"),
    re.compile(r"(?<![0-9])[0-9]{12,19}(?![0-9])"),
)


class ValidationSubcode(str, Enum):
    RESPONSE_ENVELOPE_INVALID = "response_envelope_invalid"
    RESPONSE_PROMPT_REJECTED = "response_prompt_rejected"
    RESPONSE_CANDIDATE_SHAPE_INVALID = "response_candidate_shape_invalid"
    RESPONSE_FINISH_STATE_INVALID = "response_finish_state_invalid"
    RESPONSE_EXTERNAL_METADATA_INVALID = "response_external_metadata_invalid"
    RESPONSE_CONTENT_SHAPE_INVALID = "response_content_shape_invalid"
    RESPONSE_TOOL_OR_THOUGHT_INVALID = "response_tool_or_thought_invalid"
    RESPONSE_JSON_INVALID = "response_json_invalid"
    RESPONSE_SCHEMA_INVALID = "response_schema_invalid"
    RESPONSE_TEXT_INVENTORY_INVALID = "response_text_inventory_invalid"
    RESPONSE_CITATIONS_INVALID = "response_citations_invalid"
    RESPONSE_OUTPUT_PRIVACY_INVALID = "response_output_privacy_invalid"
    RESPONSE_ID_INVALID = "response_id_invalid"
    RESPONSE_MODEL_IDENTITY_INVALID = "response_model_identity_invalid"


class ResponseValidationError(AiBriefError):
    """Non-content response branch identity used only inside the worker."""

    def __init__(self, subcode: ValidationSubcode):
        if type(subcode) is not ValidationSubcode:
            raise TypeError("validation_subcode_invalid")
        self.subcode = subcode
        super().__init__(502, "ai_response_invalid")


def response_fail(subcode: ValidationSubcode) -> None:
    raise ResponseValidationError(subcode) from None


@dataclass(frozen=True)
class GeminiConfig:
    enabled: bool = False
    credentials: object | None = field(default=None, repr=False)
    project: str = field(default="", repr=False)


@dataclass(frozen=True, slots=True)
class ProviderMetadata:
    response_id: str
    model_version: str
    generation_invocation_count: Literal[1] = 1
    sdk_version: Literal["2.28.0"] = SDK_VERSION


@dataclass(frozen=True, slots=True)
class _ConstructorProvenance:
    native: bool


def operator_gemini_config() -> GeminiConfig:
    if os.environ.get("PAYGUARD_GEMINI_OUTBOUND") != "enabled":
        return GeminiConfig()
    if any(name in os.environ for name in _FORBIDDEN_ENVIRONMENT):
        fail("ai_configuration_ambiguous", 503)
    configured_project = configured_vertex_project()
    if configured_project is None:
        fail("ai_not_configured", 503)
    try:
        credentials, discovered_project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    except Exception:
        fail("ai_not_configured", 503)
    if discovered_project not in (None, configured_project):
        fail("ai_configuration_ambiguous", 503)
    if credentials is None:
        fail("ai_not_configured", 503)
    return GeminiConfig(True, credentials, configured_project)


def assert_sdk_part_schema() -> None:
    fields = getattr(types.Part, "model_fields", None)
    if type(fields) is not dict or frozenset(fields) != _EXPECTED_PART_FIELDS:
        fail("ai_configuration_invalid", 503)


def _enum_value(value) -> str:
    if value is None:
        return ""
    raw = getattr(value, "value", value)
    return raw if type(raw) is str else str(raw)


def _safe_provider_scalar(value, pattern: str, subcode: ValidationSubcode) -> str:
    if type(value) is not str or not re.fullmatch(pattern, value):
        response_fail(subcode)
    return value


def _document_has_unsafe_output(document: object) -> bool:
    if type(document) is not dict:
        return False
    values = []
    summary = document.get("summary")
    if type(summary) is str:
        values.append(summary)
    for field_name in ("evidence_points", "missing_evidence"):
        field_value = document.get(field_name)
        if type(field_value) is list:
            values.extend(item for item in field_value if type(item) is str)
    for text in values:
        if any(unicodedata.category(char).startswith("C") for char in text):
            return True
        if re.search(r"https?://|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|<[^>]+>", text):
            return True
        if any(pattern.search(text) for pattern in _UNSAFE_OUTPUT):
            return True
    return False


def _single_text_part(response) -> str:
    """Envelope checks shared by every operation: one STOP candidate, one plain text part, no tools or thoughts."""
    if response is None:
        response_fail(ValidationSubcode.RESPONSE_ENVELOPE_INVALID)
    if getattr(response, "automatic_function_calling_history", None) not in (None, []):
        response_fail(ValidationSubcode.RESPONSE_TOOL_OR_THOUGHT_INVALID)
    prompt_feedback = getattr(response, "prompt_feedback", None)
    block_reason = _enum_value(getattr(prompt_feedback, "block_reason", None))
    if block_reason not in ("", "BLOCK_REASON_UNSPECIFIED"):
        response_fail(ValidationSubcode.RESPONSE_PROMPT_REJECTED)
    candidates = getattr(response, "candidates", None)
    if type(candidates) is not list or len(candidates) != 1:
        response_fail(ValidationSubcode.RESPONSE_CANDIDATE_SHAPE_INVALID)
    candidate = candidates[0]
    if _enum_value(getattr(candidate, "finish_reason", None)) != "STOP":
        response_fail(ValidationSubcode.RESPONSE_FINISH_STATE_INVALID)
    for field_name in ("grounding_metadata", "url_context_metadata", "citation_metadata"):
        if getattr(candidate, field_name, None) is not None:
            response_fail(ValidationSubcode.RESPONSE_EXTERNAL_METADATA_INVALID)
    content = getattr(candidate, "content", None)
    if content is None or getattr(content, "role", None) != "model":
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    parts = getattr(content, "parts", None)
    if type(parts) is not list or len(parts) != 1:
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    part = parts[0]
    thought = getattr(part, "thought", None)
    if thought is not None and thought is not False:
        response_fail(ValidationSubcode.RESPONSE_TOOL_OR_THOUGHT_INVALID)
    for field_name in _FORBIDDEN_PART_FIELDS:
        if getattr(part, field_name, None) is not None:
            response_fail(ValidationSubcode.RESPONSE_TOOL_OR_THOUGHT_INVALID)
    text = getattr(part, "text", None)
    if type(text) is not str:
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    return text


def _response_metadata(response) -> ProviderMetadata:
    response_id = _safe_provider_scalar(
        getattr(response, "response_id", None),
        r"[A-Za-z0-9_.:-]{1,256}",
        ValidationSubcode.RESPONSE_ID_INVALID,
    )
    model_version = _safe_provider_scalar(
        getattr(response, "model_version", None),
        r"[A-Za-z0-9_.:/-]{1,256}",
        ValidationSubcode.RESPONSE_MODEL_IDENTITY_INVALID,
    )
    if model_version != MODEL:
        response_fail(ValidationSubcode.RESPONSE_MODEL_IDENTITY_INVALID)
    return ProviderMetadata(response_id=response_id, model_version=model_version)


def _extract_response(response, context) -> tuple[GeneratedBrief, ProviderMetadata]:
    text = _single_text_part(response)
    try:
        raw = text.encode("utf-8", errors="strict")
        document = strict_json(raw)
        if _document_has_unsafe_output(document):
            response_fail(ValidationSubcode.RESPONSE_OUTPUT_PRIVACY_INVALID)
        if type(document) is not dict or document.get("citation_ids") != context["citation_ids"]:
            response_fail(ValidationSubcode.RESPONSE_CITATIONS_INVALID)
        brief = GeneratedBrief.model_validate(document)
        if not generated_text_matches_inventory(context.get("stage"), brief, context.get("session_facts")):
            response_fail(ValidationSubcode.RESPONSE_TEXT_INVENTORY_INVALID)
    except ResponseValidationError:
        raise
    except AiBriefError:
        response_fail(ValidationSubcode.RESPONSE_JSON_INVALID)
    except (ValidationError, ValueError, TypeError, UnicodeError):
        response_fail(ValidationSubcode.RESPONSE_SCHEMA_INVALID)
    return brief, _response_metadata(response)


def _usage_metadata(response) -> dict | None:
    """(optimise r24) The SDK's usage_metadata counts when present; anything that is not a bounded int is dropped."""
    metadata = getattr(response, "usage_metadata", None)
    if metadata is None:
        return None
    counts = {}
    for name in USAGE_FIELDS:
        value = getattr(metadata, name, None)
        counts[name] = value if type(value) is int and 0 <= value <= MAX_TOKEN_COUNT else None
    return counts if any(value is not None for value in counts.values()) else None


def _ok_envelope(result) -> bytes:
    """The ok envelope; "usage" is added only when the provider reported counts (optimise r24)."""
    envelope = {"result": result, "schema_version": "1.0", "status": "ok"}
    usage = _CALL_USAGE.get()
    if usage is not None:
        envelope["usage"] = usage
    return canonical_json(envelope)


def _native_client(config: GeminiConfig):
    return genai.Client(
        enterprise=True,
        credentials=config.credentials,
        project=config.project,
        location=LOCATION,
        http_options=types.HttpOptions(
            api_version=API_VERSION,
            timeout=PROVIDER_TIMEOUT_SECONDS * 1000,
            retry_options=types.HttpRetryOptions(attempts=1),
            client_args={"trust_env": False, "follow_redirects": False},
            async_client_args={"trust_env": False, "follow_redirects": False},
        ),
    )


class GeminiWorkerAdapter:
    __slots__ = (
        "_config_loader",
        "_client_factory",
        "_GeminiWorkerAdapter__constructor_provenance",
    )

    def __init__(self, *, config_loader=operator_gemini_config, client_factory=None):
        object.__setattr__(
            self,
            "_GeminiWorkerAdapter__constructor_provenance",
            _ConstructorProvenance(config_loader is operator_gemini_config and client_factory is None),
        )
        self._config_loader = config_loader
        self._client_factory = client_factory

    def __setattr__(self, name, value):
        if name == "_GeminiWorkerAdapter__constructor_provenance":
            raise AttributeError("constructor_provenance_immutable")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name == "_GeminiWorkerAdapter__constructor_provenance":
            raise AttributeError("constructor_provenance_immutable")
        object.__delattr__(self, name)

    async def generate(self, stage: str, session_facts: dict | None = None):
        try:
            request = AiBriefRequest.model_validate({"stage": stage, "session_facts": session_facts})
        except ValidationError:
            fail("ai_request_invalid", 422)
        native = (
            self.__constructor_provenance.native
            and self._config_loader is operator_gemini_config
            and self._client_factory is None
        )
        execution_evidence = "OPERATOR_LIVE_RESPONSE" if native else "SYNTHETIC_TEST_RESPONSE"
        context, context_digest, corpus_digest = build_fixed_context(request.stage, request.session_facts)
        logical, _logical_digest = build_logical_request(context)
        assert_sdk_part_schema()
        parent_client = None
        async_closed = False
        try:
            config = self._config_loader()
            if type(config) is not GeminiConfig or type(config.enabled) is not bool:
                fail("ai_configuration_invalid", 503)
            if not config.enabled:
                fail("ai_disabled", 503)
            if config.credentials is None or type(config.project) is not str or not config.project:
                fail("ai_not_configured", 503)
            factory = self._client_factory or _native_client
            parent_client = factory(config)
            if parent_client is None or not hasattr(parent_client, "aio"):
                fail("ai_configuration_invalid", 503)
            sdk_config = types.GenerateContentConfig(
                system_instruction=INSTRUCTIONS,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                response_mime_type="application/json",
                response_json_schema=logical["config"]["response_json_schema"],
                thinking_config=types.ThinkingConfig(
                    thinking_level="LOW", include_thoughts=False
                ),
                tools=[],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            )
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text=logical["contents"][0]["parts"][0]["text"])],
                )
            ]
            async with asyncio.timeout(WORKER_TIMEOUT_SECONDS):
                async with parent_client.aio as async_client:
                    response = await async_client.models.generate_content(
                        model=MODEL,
                        contents=contents,
                        config=sdk_config,
                    )
                async_closed = True
            _CALL_USAGE.set(_usage_metadata(response))
            brief, _metadata = _extract_response(response, context)
            result = {
                "schema_version": "1.0",
                "status": "completed",
                "stage": request.stage,
                "fixture_id": context["fixture_id"],
                "context_digest": context_digest,
                "corpus_digest": corpus_digest,
                "model": MODEL,
                "prompt_contract_id": PROMPT_CONTRACT_ID,
                "prompt_contract_digest": PROMPT_CONTRACT_DIGEST,
                "execution_evidence": execution_evidence,
                "brief": brief.model_dump(),
                "ai_generated": True,
                "advisory_only": True,
                "human_review_required": True,
                "compliance_decision": "NOT_MADE",
                "current_policy_applicability": "NOT_ESTABLISHED",
                "external_action_authorized": False,
                "workflow_transition_authorized": False,
                "semantic_entailment": "NOT_EVALUATED",
                "limitations": brief_limitations(context),
            }
            return AiBriefResponse.model_validate(result).model_dump()
        except AiBriefError:
            raise
        except (TimeoutError, asyncio.TimeoutError):
            fail("ai_timeout", 504)
        except asyncio.CancelledError:
            raise
        except Exception:
            fail("ai_provider_failure")
        finally:
            if parent_client is not None:
                try:
                    if not async_closed and hasattr(parent_client, "aio"):
                        await parent_client.aio.aclose()
                    parent_client.close()
                except Exception:
                    fail("ai_provider_failure")


@dataclass(frozen=True)
class GeminiApiKeyConfig:
    """Guide-only API-key transport (AI Studio). The key is excluded from repr and never written anywhere."""
    enabled: bool = False
    api_key: str = field(default="", repr=False)


# Same token-character rule as backend/app/guide_model.API_KEY_PATTERN.
_API_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._~+/-]{20,256}$")
# The API-key transport refuses every Vertex, ADC, proxy and other-credential switch: never both transports.
_API_KEY_FORBIDDEN_ENVIRONMENT = (_FORBIDDEN_ENVIRONMENT - {"GEMINI_API_KEY"}) | {"PAYGUARD_GEMINI_OUTBOUND", "PAYGUARD_VERTEX_PROJECT"}


def operator_guide_config():
    """Guide transport: PAYGUARD_GEMINI_TRANSPORT=api_key reads GEMINI_API_KEY; anything else is the Vertex path."""
    transport = os.environ.get("PAYGUARD_GEMINI_TRANSPORT", "")
    if transport in ("", "vertex"):
        return operator_gemini_config()
    if transport != "api_key":
        fail("ai_configuration_invalid", 503)
    if any(name in os.environ for name in _API_KEY_FORBIDDEN_ENVIRONMENT):
        fail("ai_configuration_ambiguous", 503)
    key = os.environ.get("GEMINI_API_KEY")
    if type(key) is not str or _API_KEY_PATTERN.fullmatch(key) is None:
        fail("ai_not_configured", 503)
    return GeminiApiKeyConfig(True, key)


def _native_api_key_client(config: GeminiApiKeyConfig):
    return genai.Client(
        api_key=config.api_key,
        http_options=types.HttpOptions(
            timeout=_guide_timeouts()[0] * 1000,
            retry_options=types.HttpRetryOptions(attempts=1),
            client_args={"trust_env": False, "follow_redirects": False},
            async_client_args={"trust_env": False, "follow_redirects": False},
        ),
    )


def _guide_timeouts():
    guide_model = importlib.import_module("app.guide_model")
    return guide_model.GUIDE_HTTP_TIMEOUT_SECONDS, guide_model.GUIDE_PROVIDER_TIMEOUT_SECONDS


# (K10, 2026-11-13) Guide on the API-key transport only: when the primary model call fails at the provider (for
# example a free-tier key that may not call it), the same turn tries one listed fallback model. Nothing else changes:
# same prompt, schema, validation and deadline; a timeout is never retried.


def _api_key_response_metadata(response, expected_model=MODEL) -> None:
    """AI Studio may report a versioned model name and may omit the response id; identity is still checked."""
    model_version = _safe_provider_scalar(
        getattr(response, "model_version", None),
        r"[A-Za-z0-9_.:/-]{1,256}",
        ValidationSubcode.RESPONSE_MODEL_IDENTITY_INVALID,
    )
    if model_version != expected_model and not model_version.startswith(expected_model + "-"):
        response_fail(ValidationSubcode.RESPONSE_MODEL_IDENTITY_INVALID)
    response_id = getattr(response, "response_id", None)
    if response_id is not None:
        _safe_provider_scalar(response_id, r"[A-Za-z0-9_.:-]{1,256}", ValidationSubcode.RESPONSE_ID_INVALID)


class GeminiGuideWorkerAdapter:
    """One guided-gap-filling chooser call: prompt v6, contract 2, reply checked before it leaves.

    Both transports send the identical request (instruction, contents, closed schema, temperature 0,
    thinking medium) and the reply passes the identical checks; only the client differs.
    """

    __slots__ = ("_config_loader", "_client_factory")

    def __init__(self, *, config_loader=operator_guide_config, client_factory=None):
        self._config_loader = config_loader
        self._client_factory = client_factory

    async def map_clauses(self, request) -> dict:
        # Load the guide modules only for this operation (the brief and Studio paths never need them).
        try:
            guide_model = importlib.import_module("app.guide_model")
            guide_rules = importlib.import_module("payguard.evidence_guide")
        except ModuleNotFoundError:
            fail("ai_not_configured", 503)
        try:
            logical = guide_model.build_guide_logical_request(request)
        except guide_model.GuideModelError:
            fail("ai_response_invalid")
        assert_sdk_part_schema()
        parent_client = None
        async_closed = False
        try:
            config = self._config_loader()
            if type(config) not in (GeminiConfig, GeminiApiKeyConfig) or type(config.enabled) is not bool:
                fail("ai_configuration_invalid", 503)
            if not config.enabled:
                fail("ai_disabled", 503)
            api_key_transport = type(config) is GeminiApiKeyConfig
            if api_key_transport:
                if type(config.api_key) is not str or _API_KEY_PATTERN.fullmatch(config.api_key) is None:
                    fail("ai_not_configured", 503)
            elif config.credentials is None or type(config.project) is not str or not config.project:
                fail("ai_not_configured", 503)
            native = _native_api_key_client if api_key_transport else _native_client
            parent_client = (self._client_factory or native)(config)
            if parent_client is None or not hasattr(parent_client, "aio"):
                fail("ai_configuration_invalid", 503)
            sdk_config = types.GenerateContentConfig(
                system_instruction=logical["system_instruction"],
                max_output_tokens=logical["max_output_tokens"],
                response_mime_type="application/json",
                response_json_schema=logical["response_json_schema"],
                temperature=guide_model.GUIDE_TEMPERATURE,
                thinking_config=types.ThinkingConfig(thinking_level=guide_model.GUIDE_THINKING_LEVEL, include_thoughts=False),
                tools=[],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            )
            contents = [types.Content(role="user", parts=[types.Part(text=logical["contents"])])]
            used_model = MODEL
            async with asyncio.timeout(guide_model.GUIDE_PROVIDER_TIMEOUT_SECONDS):
                async with parent_client.aio as async_client:
                    try:
                        response = await async_client.models.generate_content(
                            model=MODEL,
                            contents=contents,
                            config=sdk_config,
                        )
                    except (TimeoutError, asyncio.TimeoutError, asyncio.CancelledError):
                        raise
                    except Exception:
                        if not api_key_transport:
                            raise
                        used_model = guide_model.GUIDE_API_KEY_FALLBACK_MODEL
                        fallback_config = types.GenerateContentConfig(
                            system_instruction=logical["system_instruction"],
                            max_output_tokens=logical["max_output_tokens"],
                            response_mime_type="application/json",
                            response_json_schema=logical["response_json_schema"],
                            temperature=guide_model.GUIDE_TEMPERATURE,
                            tools=[],
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                        )
                        response = await async_client.models.generate_content(
                            model=used_model,
                            contents=contents,
                            config=fallback_config,
                        )
                async_closed = True
            _CALL_USAGE.set(_usage_metadata(response))
            text = _single_text_part(response)
            if guide_rules.validate_increments(text, logical["scenario"], 2) is None:
                response_fail(ValidationSubcode.RESPONSE_SCHEMA_INVALID)
            if api_key_transport:
                _api_key_response_metadata(response, used_model)
            else:
                _response_metadata(response)
            return {"reply": text, "prompt_sha256": logical["prompt_sha256"], "model": used_model}
        except AiBriefError:
            raise
        except (TimeoutError, asyncio.TimeoutError):
            fail("ai_timeout", 504)
        except asyncio.CancelledError:
            raise
        except Exception:
            fail("ai_provider_failure")
        finally:
            if parent_client is not None:
                try:
                    if not async_closed and hasattr(parent_client, "aio"):
                        await parent_client.aio.aclose()
                    parent_client.close()
                except Exception:
                    fail("ai_provider_failure")


def _studio_reply(response) -> list:
    """Envelope checks for a Studio agent turn: one STOP candidate, text and function-call parts only."""
    if response is None:
        response_fail(ValidationSubcode.RESPONSE_ENVELOPE_INVALID)
    if getattr(response, "automatic_function_calling_history", None) not in (None, []):
        response_fail(ValidationSubcode.RESPONSE_TOOL_OR_THOUGHT_INVALID)
    block_reason = _enum_value(getattr(getattr(response, "prompt_feedback", None), "block_reason", None))
    if block_reason not in ("", "BLOCK_REASON_UNSPECIFIED"):
        response_fail(ValidationSubcode.RESPONSE_PROMPT_REJECTED)
    candidates = getattr(response, "candidates", None)
    if type(candidates) is not list or len(candidates) != 1:
        response_fail(ValidationSubcode.RESPONSE_CANDIDATE_SHAPE_INVALID)
    candidate = candidates[0]
    if _enum_value(getattr(candidate, "finish_reason", None)) != "STOP":
        response_fail(ValidationSubcode.RESPONSE_FINISH_STATE_INVALID)
    for field_name in ("grounding_metadata", "url_context_metadata", "citation_metadata"):
        if getattr(candidate, field_name, None) is not None:
            response_fail(ValidationSubcode.RESPONSE_EXTERNAL_METADATA_INVALID)
    content = getattr(candidate, "content", None)
    if content is None or getattr(content, "role", None) != "model":
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    parts = getattr(content, "parts", None)
    if type(parts) is not list or not parts:
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    output = []
    for part in parts:
        for field_name in _EXPECTED_PART_FIELDS - _STUDIO_PART_FIELDS:
            if getattr(part, field_name, None) is not None:
                response_fail(ValidationSubcode.RESPONSE_TOOL_OR_THOUGHT_INVALID)
        if getattr(part, "thought", None) is True:
            continue  # reasoning stays inside the worker
        signature = getattr(part, "thought_signature", None)
        if signature is not None and type(signature) is not bytes:
            response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
        call = getattr(part, "function_call", None)
        if call is not None:
            name, args = getattr(call, "name", None), getattr(call, "args", None)
            if type(name) is not str or not (args is None or type(args) is dict):
                response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
            output.append({"kind": "call", "name": name, "arguments": dict(args or {}),
                           "signature": base64.b64encode(signature).decode("ascii") if signature else None})
            continue
        text = getattr(part, "text", None)
        if type(text) is not str:
            response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
        if text:
            output.append({"kind": "text", "text": text})
    if not output:
        response_fail(ValidationSubcode.RESPONSE_CONTENT_SHAPE_INVALID)
    return output


class GeminiStudioWorkerAdapter:
    """One AG Studio agent turn with function calling, for the dashboard's built-in agents (local live only).

    Same transports, clients and identity checks as the guide; the request is the closed turn
    ``app.studio_agent.validate_worker_request`` accepts and the reply passes ``validate_output`` before it leaves.
    """

    __slots__ = ("_config_loader", "_client_factory")

    def __init__(self, *, config_loader=operator_guide_config, client_factory=None):
        self._config_loader = config_loader
        self._client_factory = client_factory

    @staticmethod
    def contents(turn) -> tuple[list, str]:
        """Studio's conversation as Gemini contents; context lines join the system instruction.

        Gemini 3 checks the thought signature of the first function call of every step in the current turn, and
        expects a step's calls in one model content followed by their responses in one user content. Studio's
        history interleaves a step's parallel calls with their results (call, result, call, result) and Gemini
        signs only a step's first call, so each step is regrouped here: a signed call starts a new step, an
        unsigned one joins the open step. Calls Studio seeds itself (view_page, view_plan, view_widget before a
        delegate's first turn) were never model output: the first call of such a step carries Gemini's documented
        placeholder for injected calls (live 2026-11-04: an unsigned second step failed as a provider error).
        """
        contents, context, names = [], [], {}
        step_calls, step_responses, step_ids = [], [], set()

        def add(role, part):
            if contents and contents[-1].role == role:
                contents[-1].parts.append(part)
            else:
                contents.append(types.Content(role=role, parts=[part]))

        def close_step():
            for part in step_calls:
                add("model", part)
            for part in step_responses:
                add("user", part)
            step_calls.clear()
            step_responses.clear()
            step_ids.clear()
        for item in turn["items"]:
            if item["kind"] == "context":
                context.append(item["text"])
            elif item["kind"] == "call":
                names[item["call_id"]] = item["name"]
                signature = base64.b64decode(item["signature"], validate=True) if item["signature"] else None
                if signature is not None:
                    close_step()
                elif not step_calls:
                    signature = STUDIO_INJECTED_CALL_SIGNATURE
                step_calls.append(types.Part(function_call=types.FunctionCall(name=item["name"], args=item["arguments"]),
                                             thought_signature=signature))
                step_ids.add(item["call_id"])
            elif item["kind"] == "result":
                part = types.Part(function_response=types.FunctionResponse(
                    name=names[item["call_id"]], response={"output": item["output"]}))
                if item["call_id"] in step_ids:
                    step_responses.append(part)
                else:
                    close_step()
                    add("user", part)
            else:
                close_step()
                add("user" if item["kind"] == "user" else "model", types.Part(text=item["text"]))
        close_step()
        system = turn["instructions"] + ("\n\n" + "\n\n".join(context) if context else "")
        return contents, system

    @staticmethod
    def generation_config(turn, system):
        tools, tool_config = [], None
        if turn["tools"]:
            tools = [types.Tool(function_declarations=[
                types.FunctionDeclaration(name=tool["name"], description=tool["description"], parameters_json_schema=tool["parameters"])
                for tool in turn["tools"]])]
            choice = turn["tool_choice"]
            mode = {"auto": "AUTO", "none": "NONE", "required": "ANY"}.get(choice if type(choice) is str else "", "ANY")
            allowed = [choice["name"]] if type(choice) is dict else None
            tool_config = types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode=mode, allowed_function_names=allowed))
        json_format = turn["response_format"]["type"] == "json"
        return types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=STUDIO_MAX_OUTPUT_TOKENS,
            temperature=STUDIO_TEMPERATURE,
            thinking_config=types.ThinkingConfig(thinking_level="MEDIUM", include_thoughts=False),
            tools=tools,
            tool_config=tool_config,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            response_mime_type="application/json" if json_format else None,
            response_json_schema=turn["response_format"]["schema"] if json_format else None,
        )

    async def turn(self, document) -> dict:
        try:
            studio = importlib.import_module("app.studio_agent")
            guide_model = importlib.import_module("app.guide_model")
        except ModuleNotFoundError:
            fail("ai_not_configured", 503)
        try:
            turn = studio.validate_worker_request(document)
        except studio.StudioAgentError:
            fail("ai_response_invalid")
        assert_sdk_part_schema()
        parent_client = None
        async_closed = False
        try:
            config = self._config_loader()
            if type(config) not in (GeminiConfig, GeminiApiKeyConfig) or type(config.enabled) is not bool:
                fail("ai_configuration_invalid", 503)
            if not config.enabled:
                fail("ai_disabled", 503)
            api_key_transport = type(config) is GeminiApiKeyConfig
            if api_key_transport:
                if type(config.api_key) is not str or _API_KEY_PATTERN.fullmatch(config.api_key) is None:
                    fail("ai_not_configured", 503)
            elif config.credentials is None or type(config.project) is not str or not config.project:
                fail("ai_not_configured", 503)
            contents, system = self.contents(turn)
            sdk_config = self.generation_config(turn, system)
            native = _native_api_key_client if api_key_transport else _native_client
            parent_client = (self._client_factory or native)(config)
            if parent_client is None or not hasattr(parent_client, "aio"):
                fail("ai_configuration_invalid", 503)
            async with asyncio.timeout(guide_model.GUIDE_PROVIDER_TIMEOUT_SECONDS):
                async with parent_client.aio as async_client:
                    response = await async_client.models.generate_content(model=MODEL, contents=contents, config=sdk_config)
                async_closed = True
            _CALL_USAGE.set(_usage_metadata(response))
            output = _studio_reply(response)
            if api_key_transport:
                _api_key_response_metadata(response)
            else:
                _response_metadata(response)
            result = {"output": output, "model": MODEL}
            try:
                studio.validate_output(result, turn)
            except studio.StudioAgentError:
                response_fail(ValidationSubcode.RESPONSE_SCHEMA_INVALID)
            return result
        except AiBriefError:
            raise
        except (TimeoutError, asyncio.TimeoutError):
            fail("ai_timeout", 504)
        except asyncio.CancelledError:
            raise
        except Exception:
            fail("ai_provider_failure")
        finally:
            if parent_client is not None:
                try:
                    if not async_closed and hasattr(parent_client, "aio"):
                        await parent_client.aio.aclose()
                    parent_client.close()
                except Exception:
                    fail("ai_provider_failure")


def _protocol_error(error: AiBriefError) -> bytes:
    status = error.status if error.status in {502, 503, 504} else 502
    code = error.code if error.code in {
        "ai_configuration_ambiguous",
        "ai_configuration_invalid",
        "ai_not_configured",
        "ai_provider_failure",
        "ai_response_invalid",
        "ai_timeout",
    } else "ai_provider_failure"
    return canonical_json(
        {
            "result": {"code": code, "status": status},
            "schema_version": "1.0",
            "status": "error",
        }
    )


async def run_protocol(raw: bytes, adapter: GeminiWorkerAdapter | None = None,
                       guide_adapter: GeminiGuideWorkerAdapter | None = None,
                       studio_adapter: GeminiStudioWorkerAdapter | None = None) -> bytes:
    _CALL_USAGE.set(None)
    try:
        if b'"operation":"%s"' % STUDIO_OPERATION.encode() in raw[:64]:
            # The Studio agent turn (canonical JSON, operation first) has its own strict parser and bounds:
            # Studio's instructions and schemas exceed strict_json's 8 KB strings and depth 10.
            try:
                studio = importlib.import_module("app.studio_agent")
            except ModuleNotFoundError:
                fail("ai_not_configured", 503)
            try:
                document = studio.studio_json(raw, MAX_STUDIO_REQUEST_BYTES)
            except studio.StudioAgentError:
                fail("ai_response_invalid")
            result = await (studio_adapter or GeminiStudioWorkerAdapter()).turn(document)
            return _ok_envelope(result)
        document = strict_json(raw, maximum=MAX_GUIDE_REQUEST_BYTES)
        if type(document) is dict and document.get("operation") == GUIDE_OPERATION:
            if set(document) != {"operation", "schema_version", "request"} or document["schema_version"] != "1.0":
                fail("ai_response_invalid")
            result = await (guide_adapter or GeminiGuideWorkerAdapter()).map_clauses(document["request"])
            return _ok_envelope(result)
        if len(raw) > MAX_STDIN_BYTES:
            fail("ai_response_invalid")
        if type(document) is not dict or set(document) not in ({"operation", "schema_version", "stage"},
                                                             {"operation", "schema_version", "stage", "session_facts"}):
            fail("ai_response_invalid")
        if document["schema_version"] != "1.0" or document["operation"] != "generate_fixed_brief":
            fail("ai_response_invalid")
        request = AiBriefRequest.model_validate({"stage": document["stage"], "session_facts": document.get("session_facts")})
        if request.session_facts is None:
            result = await (adapter or GeminiWorkerAdapter()).generate(request.stage)
        else:
            result = await (adapter or GeminiWorkerAdapter()).generate(request.stage, request.session_facts)
        return _ok_envelope(result)
    except AiBriefError as error:
        return _protocol_error(error)
    except (ValidationError, ValueError, TypeError, UnicodeError, RecursionError):
        return _protocol_error(AiBriefError(502, "ai_response_invalid"))
    except Exception:
        return _protocol_error(AiBriefError(502, "ai_provider_failure"))


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments != ["generate"]:
        return 64
    raw = sys.stdin.buffer.read(MAX_STUDIO_REQUEST_BYTES + 1)
    output = asyncio.run(run_protocol(raw))
    sys.stdout.buffer.write(output + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
