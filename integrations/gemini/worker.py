#!/usr/bin/env python3
"""Dedicated Python 3.12 Gemini worker for one fixed synthetic advisory call."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
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
    build_fixed_context,
    build_logical_request,
    canonical_json,
    configured_vertex_project,
    fail,
    generated_text_matches_inventory,
    strict_json,
)


SDK_VERSION = "2.28.0"
MAX_STDIN_BYTES = 512
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


def _extract_response(response, context) -> tuple[GeneratedBrief, ProviderMetadata]:
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
    try:
        raw = text.encode("utf-8", errors="strict")
        document = strict_json(raw)
        if _document_has_unsafe_output(document):
            response_fail(ValidationSubcode.RESPONSE_OUTPUT_PRIVACY_INVALID)
        if type(document) is not dict or document.get("citation_ids") != context["citation_ids"]:
            response_fail(ValidationSubcode.RESPONSE_CITATIONS_INVALID)
        brief = GeneratedBrief.model_validate(document)
        if not generated_text_matches_inventory(context.get("stage"), brief):
            response_fail(ValidationSubcode.RESPONSE_TEXT_INVENTORY_INVALID)
    except ResponseValidationError:
        raise
    except AiBriefError:
        response_fail(ValidationSubcode.RESPONSE_JSON_INVALID)
    except (ValidationError, ValueError, TypeError, UnicodeError):
        response_fail(ValidationSubcode.RESPONSE_SCHEMA_INVALID)
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
    return brief, ProviderMetadata(response_id=response_id, model_version=model_version)


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

    async def generate(self, stage: str):
        try:
            request = AiBriefRequest.model_validate({"stage": stage})
        except ValidationError:
            fail("ai_request_invalid", 422)
        native = (
            self.__constructor_provenance.native
            and self._config_loader is operator_gemini_config
            and self._client_factory is None
        )
        execution_evidence = "OPERATOR_LIVE_RESPONSE" if native else "SYNTHETIC_TEST_RESPONSE"
        context, context_digest, corpus_digest = build_fixed_context(request.stage)
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
                "limitations": list(LIMITATIONS),
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


async def run_protocol(raw: bytes, adapter: GeminiWorkerAdapter | None = None) -> bytes:
    try:
        document = strict_json(raw, maximum=MAX_STDIN_BYTES)
        if type(document) is not dict or set(document) != {"operation", "schema_version", "stage"}:
            fail("ai_response_invalid")
        if document["schema_version"] != "1.0" or document["operation"] != "generate_fixed_brief":
            fail("ai_response_invalid")
        request = AiBriefRequest.model_validate({"stage": document["stage"]})
        result = await (adapter or GeminiWorkerAdapter()).generate(request.stage)
        return canonical_json({"result": result, "schema_version": "1.0", "status": "ok"})
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
    raw = sys.stdin.buffer.read(MAX_STDIN_BYTES + 1)
    output = asyncio.run(run_protocol(raw))
    sys.stdout.buffer.write(output + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
