"""Default-off LM Studio adapter for fixed synthetic PayGuard evidence briefs.

This module has one network destination: the loopback LM Studio OpenAI-compatible
chat-completions endpoint. It accepts no caller prompt, model, URL, credential,
tool definition, retry count, or business record.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

import httpx
from pydantic import ValidationError

from .ai_brief import (
    AiBriefError,
    AiBriefRequest,
    AiBriefResponse,
    GeneratedBrief,
    INSTRUCTIONS,
    LIMITATIONS,
    MAX_PROTOCOL_BYTES,
    MAX_REQUEST_BYTES,
    PROMPT_CONTRACT_DIGEST,
    PROMPT_CONTRACT_ID,
    build_fixed_context,
    canonical_json,
    fail,
    response_schema,
    strict_json,
)


MODEL = "nvidia-nemotron-3-nano-4b"
ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"
MAX_OUTPUT_TOKENS = 900
TOTAL_TIMEOUT_SECONDS = 90
CONNECT_TIMEOUT_SECONDS = 3
READ_TIMEOUT_SECONDS = 80
_MODEL_GATE = asyncio.Semaphore(1)


@dataclass(frozen=True, slots=True)
class LmStudioConfig:
    enabled: bool = False


def build_lmstudio_request(context: dict[str, object]) -> dict[str, object]:
    """Build the only request shape allowed to reach the local model."""
    schema = response_schema(context["stage"], context["citation_ids"])
    for field_name in ("evidence_points", "missing_evidence"):
        schema["properties"][field_name]["maxItems"] = 1
    request = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": canonical_json(context).decode("utf-8")},
        ],
        "temperature": 0,
        "reasoning_effort": "none",
        "max_tokens": MAX_OUTPUT_TOKENS,
        "stream": False,
        "tools": [],
        "tool_choice": "none",
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "payguard_evidence_brief",
                "strict": True,
                "schema": schema,
            },
        },
    }
    if len(canonical_json(request)) > MAX_REQUEST_BYTES:
        fail("ai_context_unavailable", 503)
    return request


async def call_lmstudio(request: dict[str, object]) -> bytes:
    """Call a fixed loopback endpoint once and return a bounded response body."""
    timeout = httpx.Timeout(
        connect=CONNECT_TIMEOUT_SECONDS,
        read=READ_TIMEOUT_SECONDS,
        write=CONNECT_TIMEOUT_SECONDS,
        pool=CONNECT_TIMEOUT_SECONDS,
    )
    limits = httpx.Limits(max_connections=1, max_keepalive_connections=0)
    try:
        async with httpx.AsyncClient(
            trust_env=False,
            follow_redirects=False,
            timeout=timeout,
            limits=limits,
        ) as client:
            async with client.stream(
                "POST",
                ENDPOINT,
                json=request,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
            ) as response:
                if response.status_code != 200:
                    fail("ai_provider_failure")
                content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
                if content_type != "application/json":
                    fail()
                declared = response.headers.get("content-length")
                if declared is not None:
                    try:
                        if int(declared) > MAX_PROTOCOL_BYTES:
                            fail()
                    except ValueError:
                        fail()
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_PROTOCOL_BYTES:
                        fail()
                if not body:
                    fail()
                return bytes(body)
    except AiBriefError:
        raise
    except (httpx.TimeoutException, TimeoutError, asyncio.TimeoutError):
        fail("ai_timeout", 504)
    except asyncio.CancelledError:
        raise
    except Exception:
        fail("ai_provider_failure")


LocalTransport = Callable[[dict[str, object]], Awaitable[bytes]]


def validate_lmstudio_response(raw: bytes, *, stage: str, context: dict[str, object]) -> dict[str, object]:
    """Reduce an OpenAI-compatible envelope to the closed PayGuard response."""
    envelope = strict_json(raw)
    if type(envelope) is not dict or envelope.get("model") != MODEL:
        fail()
    choices = envelope.get("choices")
    if type(choices) is not list or len(choices) != 1 or type(choices[0]) is not dict:
        fail()
    choice = choices[0]
    if choice.get("finish_reason") != "stop" or choice.get("index") not in (0, None):
        fail()
    message = choice.get("message")
    allowed_message_fields = {"role", "content", "reasoning_content", "tool_calls"}
    if type(message) is not dict or not {"role", "content"} <= set(message) <= allowed_message_fields:
        fail()
    if message.get("role") != "assistant" or type(message.get("content")) is not str:
        fail()
    if message.get("reasoning_content") not in (None, ""):
        fail()
    if message.get("tool_calls") not in (None, []):
        fail()
    content = message["content"].encode("utf-8", errors="strict")
    document = strict_json(content, maximum=MAX_PROTOCOL_BYTES)
    if type(document) is not dict:
        fail()
    try:
        brief = GeneratedBrief.model_validate(document).model_dump()
    except ValidationError:
        fail()
    if brief["citation_ids"] != context["citation_ids"]:
        fail()
    return brief


class LmStudioEvidenceBriefAdapter:
    """Explicitly enabled, serialized local model adapter with no retries."""

    __slots__ = ("_config", "_transport")

    def __init__(self, *, config: LmStudioConfig | None = None, transport: LocalTransport | None = None):
        self._config = LmStudioConfig() if config is None else config
        self._transport = call_lmstudio if transport is None else transport

    def validate_attempt_configuration(self) -> None:
        """Fail before a process-wide attempt is reserved when local AI is unavailable."""
        if type(self._config) is not LmStudioConfig or type(self._config.enabled) is not bool:
            fail("ai_configuration_invalid", 503)
        if not self._config.enabled:
            fail("ai_disabled", 503)

    async def generate(self, request):
        try:
            validated = AiBriefRequest.model_validate(request)
        except ValidationError:
            fail("ai_request_invalid", 422)
        self.validate_attempt_configuration()

        context, context_digest, corpus_digest = build_fixed_context(validated.stage)
        logical_request = build_lmstudio_request(context)
        try:
            async with asyncio.timeout(TOTAL_TIMEOUT_SECONDS):
                async with _MODEL_GATE:
                    raw = await self._transport(logical_request)
            brief = validate_lmstudio_response(raw, stage=validated.stage, context=context)
            result = AiBriefResponse.model_validate(
                {
                    "schema_version": "1.0",
                    "status": "completed",
                    "stage": validated.stage,
                    "fixture_id": "payguard-fixed-synthetic-brief-v1",
                    "context_digest": context_digest,
                    "corpus_digest": corpus_digest,
                    "model": MODEL,
                    "prompt_contract_id": PROMPT_CONTRACT_ID,
                    "prompt_contract_digest": PROMPT_CONTRACT_DIGEST,
                    "execution_evidence": "LOCAL_RUNTIME_RESPONSE",
                    "brief": brief,
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
            ).model_dump()
        except AiBriefError:
            raise
        except (TimeoutError, asyncio.TimeoutError):
            fail("ai_timeout", 504)
        except asyncio.CancelledError:
            raise
        except (ValidationError, ValueError, TypeError, UnicodeError):
            fail()
        return result
