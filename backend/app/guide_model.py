"""Optional Gemini chooser for guided gap filling (prompt v6, contract 2).

The chooser only maps up to three seller clauses to slot ids and tags who said each one
(SELLER / BUYER / THIRD_PARTY) and how it is known (STATED / INFERRED). evidence_guide
validates the reply, keeps only SELLER + STATED, computes the gap and picks a fixed template.

It is used only when PAYGUARD_GUIDE_MODEL=gemini AND one transport of the Gemini profile is configured:
- vertex (default): PAYGUARD_GEMINI_OUTBOUND=enabled, a Vertex project and the profile venv (see ai_brief);
- api_key: PAYGUARD_GEMINI_TRANSPORT=api_key plus GEMINI_API_KEY (an AI Studio key) and the profile venv,
  with no Vertex or outbound switch set. The two transports are never used together.
Otherwise no chooser is built and nothing here runs. The API key is read from the environment only when
a worker starts, handed only to that worker's clean environment, and never stored, logged or returned. A live call crosses the same bounded
subprocess boundary as the evidence brief; the worker rebuilds the prompt from this module, so
no prompt text crosses the boundary. This module imports no provider SDK and reads no credential.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import threading

from payguard import evidence_guide as eg

from .ai_brief import (
    MODEL,
    PROJECT_ROOT,
    DEFAULT_GEMINI_PYTHON,
    DEFAULT_GEMINI_WORKER,
    AiBriefError,
    AiConfig,
    canonical_json,
    clean_worker_environment,
    operator_ai_config,
    run_worker_subprocess,
    strict_json,
)
from .ai_usage import UsageInvalid, parse_usage

GUIDE_MODEL_ENV = "PAYGUARD_GUIDE_MODEL"
# (K10, 2026-11-13) The API-key guide worker may answer from this listed fallback when the primary call fails
# at the provider; the reply is validated exactly as before.
GUIDE_API_KEY_FALLBACK_MODEL = "gemini-3.5-flash-lite"
GUIDE_OPERATION = "map_guide_clauses"
GUIDE_PROMPT_ID = "payguard-guide-chooser-v6"
GUIDE_CONTRACT = 2
# Thinking tokens count against this ceiling. At 1024 a medium-thinking reply was cut off (finish reason not STOP)
# in about half of the live turns on 2026-11-01; the reply itself is still capped at 512 bytes by validation.
GUIDE_MAX_OUTPUT_TOKENS = 8192
# Timeout ladder, innermost first: SDK HTTP 25 s < worker call 26 s < host subprocess 28 s < governed deadline 30 s
# (guide_routes.GUIDE_MODEL_DEADLINE_SECONDS), so the subprocess is always terminated, never orphaned.
# Widened from 15/16/18/20 on 2026-11-01: live medium-thinking calls took 5-15 s and the 15 s HTTP limit cut
# about 1 in 5; the seller sees the keyword answer at once, so a longer wait for the model costs no time.
GUIDE_HTTP_TIMEOUT_SECONDS = 25
GUIDE_PROVIDER_TIMEOUT_SECONDS = 26
GUIDE_WORKER_TIMEOUT_SECONDS = 28
GUIDE_TEMPERATURE = 0.0
GUIDE_THINKING_LEVEL = "MEDIUM"
GUIDE_TRANSPORT_ENV = "PAYGUARD_GEMINI_TRANSPORT"
TRANSPORT_VERTEX = "vertex"
TRANSPORT_API_KEY = "api_key"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
# Token characters only (current AI Studio keys may contain "." and similar); never whitespace, quotes or "=".
API_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._~+/-]{20,256}$")
# Any of these next to the API-key transport would mix it with Vertex or another credential: refuse.
API_KEY_CONFLICTS = ("PAYGUARD_GEMINI_OUTBOUND", "PAYGUARD_VERTEX_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS",
                     "GOOGLE_API_KEY", "GOOGLE_GENAI_USE_VERTEXAI", "GOOGLE_GENAI_USE_ENTERPRISE",
                     "GOOGLE_CLOUD_PROJECT", "CLOUDSDK_CORE_PROJECT", "GCLOUD_PROJECT")
_WORKER_ENV_PASSTHROUGH = ("HOME", "LANG", "LC_ALL", "TMPDIR")
MAX_GUIDE_REQUEST_BYTES = 2048
MAX_GUIDE_ENVELOPE_BYTES = 2048


def _load_prompt_pack():
    """The per-situation prompts live in tools/make_prompt_pack.py; load that exact file, never a copy."""
    spec = importlib.util.spec_from_file_location("_payguard_guide_prompt_pack", PROJECT_ROOT / "tools" / "make_prompt_pack.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PROMPT_CACHE = {}


def guide_prompt(scenario):
    """The one prompt for this situation (v6): {"text", "sha256"}. Loaded only when a model request is actually built
    or checked: the hosted demo image carries no tools/ folder and never calls a model, so importing this module
    must not read tools/make_prompt_pack.py. Each situation has its own text and pin; none sees another's items."""
    if scenario not in eg.SCENARIOS:
        raise GuideModelError("guide_request_invalid")
    if not _PROMPT_CACHE:
        pack = _load_prompt_pack()
        for name in eg.SCENARIOS:
            text = pack.instructions_v6(name)
            _PROMPT_CACHE[name] = {"text": text, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    return _PROMPT_CACHE[scenario]


class GuideModelError(Exception):
    """Fixed code only; never carries provider text."""


def validate_guide_request(request):
    """The exact chooser request evidence_guide.chooser_request(..., contract=2) builds, nothing more."""
    if type(request) is not dict or set(request) != {"task", "scenario", "clauses", "slots", "contract"}:
        raise GuideModelError("guide_request_invalid")
    if request["task"] != "map_clauses" or request["contract"] != GUIDE_CONTRACT or type(request["contract"]) is not int:
        raise GuideModelError("guide_request_invalid")
    scenario = request["scenario"]
    if type(scenario) is not str or scenario not in eg.SCENARIOS:
        raise GuideModelError("guide_request_invalid")
    clauses = request["clauses"]
    if type(clauses) is not list or not 0 < len(clauses) <= eg.MAX_CLAUSES:
        raise GuideModelError("guide_request_invalid")
    for clause in clauses:
        if type(clause) is not str or not 0 < len(clause) <= eg.MAX_CLAUSE_CHARS or not clause.isascii():
            raise GuideModelError("guide_request_invalid")
        if any(not (char.isalnum() or char in " .,?!'-") for char in clause):
            raise GuideModelError("guide_request_invalid")
    slots = request["slots"]
    known = eg.SCENARIOS[scenario]["slots"]
    if type(slots) is not dict or not slots or set(slots) - set(known):
        raise GuideModelError("guide_request_invalid")
    if any(value not in eg.STATUSES or value == "NOT_APPLICABLE" for value in slots.values()):
        raise GuideModelError("guide_request_invalid")
    return {"task": "map_clauses", "scenario": scenario, "clauses": list(clauses), "slots": dict(slots), "contract": GUIDE_CONTRACT}


def _nullable_enum(values):
    return {"anyOf": [{"type": "string", "enum": list(values)}, {"type": "null"}]}


def guide_response_schema(request):
    """Contract 2, the same closed shape tools/gemini_api_trial.py enforced in the trial runs."""
    slots = sorted(slot for slot in request["slots"] if slot not in eg.SCENARIOS[request["scenario"]]["rule_only"])
    keys = ["c", "k", "s", "w", "r", "h", "b", "a"]
    entry = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "c": {"type": "string", "enum": slots},
            "k": {"type": "integer", "minimum": 0, "maximum": eg.MAX_CLAUSES - 1},
            "s": {"type": "string", "enum": ["P", "U"]},
            "w": _nullable_enum(eg.WEEKDAYS),
            "r": _nullable_enum(eg.RELATIVE_WEEKS),
            "h": {"type": "string", "enum": list(eg.HEDGES)},
            "b": {"type": "string", "enum": list(eg.BASES)},
            "a": {"type": "string", "enum": list(eg.ACTORS)},
        },
        "required": keys,
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "v": {"type": "integer", "minimum": GUIDE_CONTRACT, "maximum": GUIDE_CONTRACT},
            "u": {"type": "array", "maxItems": eg.MAX_INCREMENTS, "items": entry},
        },
        "required": ["v", "u"],
    }


def build_guide_logical_request(request):
    """Everything the worker sends to the provider, built from fixed code plus the validated request."""
    validated = validate_guide_request(request)
    return {
        "model": MODEL,
        "prompt_id": GUIDE_PROMPT_ID,
        "prompt_sha256": guide_prompt(validated["scenario"])["sha256"],
        "system_instruction": guide_prompt(validated["scenario"])["text"],
        "contents": canonical_json(validated).decode("utf-8"),
        "response_json_schema": guide_response_schema(validated),
        "max_output_tokens": GUIDE_MAX_OUTPUT_TOKENS,
        "scenario": validated["scenario"],
    }


def guide_worker_request(request) -> bytes:
    encoded = canonical_json({"operation": GUIDE_OPERATION, "schema_version": "1.0", "request": validate_guide_request(request)})
    if len(encoded) > MAX_GUIDE_REQUEST_BYTES:
        raise GuideModelError("guide_request_invalid")
    return encoded


def parse_guide_envelope(raw, scenario) -> bytes:
    """Return the chooser reply bytes; evidence_guide.validate_increments checks them again. The reply must carry the
    pin of this request's own situation prompt."""
    return parse_guide_envelope_with_usage(raw, scenario)[0]


def parse_guide_envelope_with_usage(raw, scenario):
    """The reply bytes plus the worker's token counts or None (optimise r24: counts only, for the AI audit log)."""
    try:
        envelope = strict_json(raw, maximum=MAX_GUIDE_ENVELOPE_BYTES)
    except AiBriefError:
        raise GuideModelError("guide_response_invalid") from None
    if type(envelope) is not dict or set(envelope) - {"usage"} != {"schema_version", "status", "result"} or envelope["schema_version"] != "1.0":
        raise GuideModelError("guide_response_invalid")
    if envelope["status"] == "error":
        raise GuideModelError("guide_provider_failure")
    try:
        usage = parse_usage(envelope.get("usage"))
    except UsageInvalid:
        raise GuideModelError("guide_response_invalid") from None
    result = envelope["result"]
    if envelope["status"] != "ok" or type(result) is not dict or set(result) != {"reply", "prompt_sha256", "model"}:
        raise GuideModelError("guide_response_invalid")
    if result["prompt_sha256"] != guide_prompt(scenario)["sha256"] or result["model"] not in (MODEL, GUIDE_API_KEY_FALLBACK_MODEL):
        raise GuideModelError("guide_response_invalid")
    reply = result["reply"]
    if type(reply) is not str or not reply.isascii() or not 0 < len(reply) <= eg.MAX_CHOOSER_BYTES:
        raise GuideModelError("guide_response_invalid")
    return reply.encode("ascii"), usage


@dataclass(frozen=True, slots=True)
class ApiKeyProfileConfig:
    """Paths of the Gemini profile for the API-key transport. Deliberately holds no key."""
    python_bin: Path
    worker_path: Path


def guide_transport():
    """vertex (default), api_key, or None for any other value (no chooser)."""
    value = os.environ.get(GUIDE_TRANSPORT_ENV, "")
    if value in ("", TRANSPORT_VERTEX):
        return TRANSPORT_VERTEX
    if value == TRANSPORT_API_KEY:
        return TRANSPORT_API_KEY
    return None


def _api_key_from_env():
    key = os.environ.get(GEMINI_API_KEY_ENV)
    if type(key) is not str or API_KEY_PATTERN.fullmatch(key) is None:
        return None
    return key


def api_key_profile_config():
    """The API-key transport's profile paths, or None. Checks the key's shape only; never returns it."""
    if guide_transport() != TRANSPORT_API_KEY or _api_key_from_env() is None:
        return None
    if any(name in os.environ for name in API_KEY_CONFLICTS):
        return None
    python_bin, worker_path = DEFAULT_GEMINI_PYTHON, DEFAULT_GEMINI_WORKER
    if not python_bin.is_file() or not os.access(python_bin, os.X_OK) or worker_path.is_symlink() or not worker_path.is_file():
        return None
    try:
        return ApiKeyProfileConfig(python_bin, worker_path.resolve(strict=True))
    except OSError:
        return None


def clean_api_key_worker_environment():
    """The only place the key leaves this process: the worker's clean environment, nothing else inherited."""
    key = _api_key_from_env()
    if key is None:
        raise GuideModelError("guide_not_configured")
    environment = {"PATH": "/usr/bin:/bin", "PYTHONNOUSERSITE": "1", GUIDE_TRANSPORT_ENV: TRANSPORT_API_KEY, GEMINI_API_KEY_ENV: key}
    for name in _WORKER_ENV_PASSTHROUGH:
        value = os.environ.get(name)
        if value and "\x00" not in value and not any(char in value for char in "\r\n"):
            environment[name] = value
    return environment


class GeminiGuideChooser:
    """Synchronous chooser callable; guide_routes runs it on its pool under the governed deadline."""

    __slots__ = ("_config", "_runner", "_usage")

    def __init__(self, config, runner=None):
        if type(config) is AiConfig:
            if not config.enabled or config.python_bin is None or config.worker_path is None:
                raise GuideModelError("guide_not_configured")
        elif type(config) is not ApiKeyProfileConfig:
            raise GuideModelError("guide_not_configured")
        self._config = config
        self._runner = runner
        # (optimise r24) Token counts of the last call made on this thread; read once by the AI audit log.
        self._usage = threading.local()

    @property
    def transport(self):
        return TRANSPORT_API_KEY if type(self._config) is ApiKeyProfileConfig else TRANSPORT_VERTEX

    def __repr__(self):
        return f"GeminiGuideChooser(transport={self.transport!r})"

    async def _run(self, payload: bytes) -> bytes:
        command = (str(self._config.python_bin), "-I", "-B", str(self._config.worker_path), "generate")
        if type(self._config) is ApiKeyProfileConfig:
            environment = clean_api_key_worker_environment()
        else:
            environment = clean_worker_environment(self._config.vertex_project)
        async with asyncio.timeout(GUIDE_WORKER_TIMEOUT_SECONDS):
            return await (self._runner or run_worker_subprocess)(command, payload, environment)

    # (optimise r24) The model id the per-session AI audit log records for this chooser.
    MODEL_ID = MODEL

    def take_usage(self):
        """(optimise r24) The token counts of this thread's last call (or None), then forgotten."""
        usage = getattr(self._usage, "value", None)
        self._usage.value = None
        return usage

    def __call__(self, request) -> bytes:
        self._usage.value = None
        payload = guide_worker_request(request)
        try:
            raw = asyncio.run(self._run(payload))
        except (TimeoutError, asyncio.TimeoutError):
            raise GuideModelError("guide_timeout") from None
        except AiBriefError:
            raise GuideModelError("guide_provider_failure") from None
        except GuideModelError:
            raise
        except Exception:
            raise GuideModelError("guide_provider_failure") from None
        reply, usage = parse_guide_envelope_with_usage(raw, request["scenario"])
        self._usage.value = usage
        return reply


def guide_model_requested() -> bool:
    return os.environ.get(GUIDE_MODEL_ENV) == "gemini"


def configured_guide_chooser(*, config_loader=operator_ai_config, api_key_loader=api_key_profile_config, runner=None):
    """A Gemini chooser, or None for the keyword baseline. The env flag is read first, so with the
    flag off no configuration is inspected and no worker can start. PAYGUARD_GEMINI_TRANSPORT picks
    exactly one transport; the other one's loader is never called."""
    if not guide_model_requested():
        return None
    transport = guide_transport()
    if transport is None:
        return None
    if transport == TRANSPORT_API_KEY:
        config = api_key_loader()
        if type(config) is not ApiKeyProfileConfig:
            return None
        try:
            return GeminiGuideChooser(config, runner)
        except GuideModelError:
            return None
    try:
        config = config_loader()
    except AiBriefError:
        return None
    if type(config) is not AiConfig or not config.enabled or config.python_bin is None or config.worker_path is None:
        return None
    try:
        return GeminiGuideChooser(config, runner)
    except GuideModelError:
        return None
