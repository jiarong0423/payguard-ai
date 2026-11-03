"""Governed Gemini turns for AG Studio's built-in agents (/dashboard.html, local live mode only).

AG Studio runs its agents in the browser; a built-in agent asks an ``AgLlmAdapter`` for one model turn at a
time (instructions, conversation, tool schemas). The dashboard's adapter sends that turn here, reduced to a
closed wire shape, and this module forwards it through the same governed path as the guided gap filling:

* Off unless ``PAYGUARD_STUDIO_AGENTS=gemini`` and one Gemini profile transport is configured (the same
  loaders as ``guide_model``: Vertex or ``PAYGUARD_GEMINI_TRANSPORT=api_key`` with ``GEMINI_API_KEY``). The
  hosted demo (``PAYGUARD_DEMO_MODE=public``) disables the route before any work: zero model calls there.
* The key never reaches the browser: it is read only when a worker starts and handed only to that worker's
  clean environment (``guide_model.clean_api_key_worker_environment``). This module imports no provider SDK.
* Closed input: the operator's question (no PII, bounded), Studio's own instructions, tool schemas, tool
  calls and tool results, each bounded; images, files, unknown fields and unknown roles are refused.
* Bounded output: at most ``MAX_OUTPUT_ITEMS`` items, text and tool arguments capped, every tool call must
  name a tool the request advertised, and a JSON response format must come back as JSON.
* Caps: a ``controlled_fallback.Governor`` (per-session calls, spacing, per-client and global day limits,
  global per-minute limit, failure breaker, in-flight cap) and the guide's timeout ladder.
* Gemini 3 function calling needs each call's thought signature on the next turn. Signatures are kept here,
  per session and call id in a bounded store, and re-attached; the browser never sees them.

The agents only arrange the dashboard with Studio's own tools. Nothing here reads or writes dispute data,
decides a dispute or submits anything.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import concurrent.futures
import json
import math
import os
import re
import secrets
import threading
import time
import unicodedata
from collections import OrderedDict

from payguard.controlled_fallback import MAX_PROVIDER_IN_FLIGHT, Governor

from .ai_usage import UsageInvalid, parse_usage
from .ai_brief import MODEL, AiBriefError, AiConfig, canonical_json, clean_worker_environment, operator_ai_config, \
    run_worker_subprocess
from .guide_model import (GUIDE_HTTP_TIMEOUT_SECONDS, GUIDE_PROVIDER_TIMEOUT_SECONDS, GUIDE_WORKER_TIMEOUT_SECONDS,
                          TRANSPORT_API_KEY, ApiKeyProfileConfig, api_key_profile_config, clean_api_key_worker_environment,
                          guide_transport)

STUDIO_AGENTS_ENV = "PAYGUARD_STUDIO_AGENTS"
STUDIO_OPERATION = "studio_agent_turn"
SCHEMA_VERSION = "1.0"

# Request bounds, measured on Studio 3.0.0's own agents (lead about 12 KB of instructions and 6 KB of tool
# schemas, page about 14 KB and 27 KB, planning about 17 KB and 10 KB, data about 5 KB and 28 KB, widget about
# 9 KB and 47 KB) with headroom.
MAX_TURN_BODY_BYTES = 262144
MAX_INSTRUCTIONS_CHARS = 32768
MAX_ITEMS = 64
MAX_QUESTION_CHARS = 600
MAX_CONTEXT_CHARS = 4000
MAX_ASSISTANT_TEXT_CHARS = 8000
MAX_TOOL_RESULT_CHARS = 32768
MAX_ARGUMENTS_CHARS = 16384
MAX_TOOLS = 16
# The data agent's create_expression and update_expression embed Studio's operator catalogue: about 4.5 KB each
# (measured 2026-11-04, Studio 3.0.0; 4000 refused every data-agent turn live). Other built-in tools stay under
# 400 characters. The total stays bounded by MAX_TOOLS_JSON_BYTES and the personal-data check is unchanged.
MAX_TOOL_DESCRIPTION_CHARS = 8192
MAX_TOOLS_JSON_BYTES = 98304
MAX_SCHEMA_DEPTH = 32
MAX_WORKER_REQUEST_BYTES = MAX_TURN_BODY_BYTES + 8192
# Output bounds.
MAX_OUTPUT_ITEMS = 8
MAX_OUTPUT_TEXT_CHARS = 6000
MAX_SIGNATURE_BYTES = 16384
MAX_ENVELOPE_BYTES = 65536
# Caps and timeouts: Governor limits plus the guide's ladder (SDK 25 s < worker call 26 s < subprocess 28 s
# < governed deadline 30 s). One Studio answer takes several turns, hence more calls than the guide.
STUDIO_CALLS_PER_SESSION = 20
STUDIO_MIN_SPACING_SECONDS = 0.5
STUDIO_DEADLINE_SECONDS = 30.0
SIGNATURES_PER_SESSION = 64
SIGNATURE_SESSIONS = 256

_TOOL_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_FORMAT_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
_CALL_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,80}$")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# The operator's own question: any run of 9+ digits (phone, card, account number) is refused outright.
_LONG_NUMBER = re.compile(r"(?:\d[\s().-]*){9,}")
# Everything else the model sees or returns (instructions, tool descriptions and schemas, tool results, assistant
# text, tool-call arguments) is machine-made and full of dates, ids and epoch timestamps, so it is checked with
# precise patterns instead: an email address, a phone number written with separators, or a card number (4-digit
# groups, or 15-16 plain digits) that passes the Luhn check.
_PHONE = re.compile(r"(?<!\d)(?:\+\d{1,3}[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)")
_CARD = re.compile(r"(?<![\d.])(?:\d{4}(?:[ -]\d{4}){3}(?:[ -]\d{1,3})?|\d{4}[ -]\d{6}[ -]\d{5}|\d{15,16})(?![\d.])")


def _luhn(digits: str) -> bool:
    total = 0
    for index, char in enumerate(reversed(digits)):
        value = int(char) * (2 if index % 2 else 1)
        total += value - 9 if value > 9 else value
    return total % 10 == 0


# (r25 R1 P2-3) Forms the patterns above missed. Each stays narrow so machine-made dashboard text (dates, counts,
# amounts, case ids, epoch seconds and milliseconds, which start with 1) keeps passing:
# - a spoken email, "jane.doe at example dot com" (an "at" word and at least one "dot" word);
#   The last label must be a common top-level domain, so "look at the dot plot" passes;
_SPOKEN_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+\s*[\[(]?\s*\bat\b\s*[\])]?\s*[A-Za-z0-9-]+"
                           r"(?:\s*(?:\.|[\[(]?\s*\bdot\b\s*[\])]?)\s*[A-Za-z0-9-]+)*"
                           r"\s*[\[(]?\s*\bdot\b\s*[\])]?\s*"
                           r"(?:com|net|org|edu|gov|io|co|me|info|biz|us|uk|tw|jp|de|fr|ca|au|cn|hk|sg|in)\b",
                           re.IGNORECASE)
# - a phone of 10-15 plain digits: "+" and 10-15 digits (E.164), or 10 digits whose area code starts 2-9 (optional
#   leading 1), except a run that starts like a date stamp (YYYYMM...), so 2026103100 passes;
_PLAIN_PHONE = re.compile(r"(?<![\d.])(?:\+\d{10,15}|1?(?!(?:19|20)\d{2}(?:0[1-9]|1[0-2]))[2-9]\d{9})(?![\d.])")
# - a card of 13-19 plain digits that starts like a card (22-27 Mastercard 2-series, 3 Amex/Diners/JCB, 4 Visa,
#   5 Mastercard/Maestro, 6 Discover/UnionPay; so 20xx date stamps and 1xxx epoch values pass) and passes the Luhn
#   check.
_PLAIN_CARD = re.compile(r"(?<![\d.])(?:2[2-7]\d{11,17}|[3-6]\d{12,18})(?![\d.])")
_INVISIBLE = re.compile(r"[\u00ad\u200b-\u200f\u2060-\u2064\ufeff]")


def fold(text: str) -> str:
    """NFKC folding (fullwidth @ and digits become ASCII) with invisible format characters removed."""
    return _INVISIBLE.sub("", unicodedata.normalize("NFKC", text))


def has_personal_data(text: str) -> bool:
    """Email address (also spoken or fullwidth), phone number (with separators, or 10+ plain digits shaped like a
    phone), or a Luhn-valid card number anywhere in the NFKC-folded text."""
    text = fold(text)
    if _EMAIL.search(text) or _PHONE.search(text) or _SPOKEN_EMAIL.search(text) or _PLAIN_PHONE.search(text):
        return True
    if any(_luhn(match.group(0)) for match in _PLAIN_CARD.finditer(text)):
        return True
    return any(_luhn(re.sub(r"[ -]", "", match.group(0))) for match in _CARD.finditer(text))


def _joined_personal_data(texts: list[str]) -> bool:
    """(r25 R1 P2-3) Personal data split across items: the texts joined with a space (all checks) and with nothing
    (an email cut at the @ or the dot)."""
    folded = [fold(text) for text in texts]
    return has_personal_data(" ".join(folded)) or _EMAIL.search("".join(folded)) is not None
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class StudioAgentError(Exception):
    """Fixed code only; never carries provider text or request content."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _text(value, limit: int, *, question: bool = False, allow_empty: bool = False) -> str:
    """Bounded text, checked for personal data: strictly for the operator's question, precisely for the rest."""
    if type(value) is not str or len(value) > limit or (not value.strip() and not allow_empty) or _CONTROL.search(value):
        raise StudioAgentError("studio_turn_invalid")
    if has_personal_data(value) or (question and _LONG_NUMBER.search(value)):
        raise StudioAgentError("studio_turn_personal_data")
    return value


def _depth(value, depth: int = 0) -> int:
    if depth > MAX_SCHEMA_DEPTH:
        raise StudioAgentError("studio_turn_invalid")
    if type(value) is dict:
        return max([_depth(item, depth + 1) for item in value.values()], default=depth)
    if type(value) is list:
        return max([_depth(item, depth + 1) for item in value], default=depth)
    if type(value) is float and not math.isfinite(value):
        raise StudioAgentError("studio_turn_invalid")  # (r25 R5 P2-1) 1e400 and NaN never reach canonical_json
    if value is None or type(value) in (str, int, float, bool):
        return depth
    raise StudioAgentError("studio_turn_invalid")


def _finite_float(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("nonfinite")
    return value


def _reject_constant(_value):
    raise ValueError("nonfinite")


def _json_object(raw, limit: int) -> dict:
    if type(raw) is not str or len(raw) > limit:
        raise StudioAgentError("studio_turn_invalid")
    try:
        value = json.loads(raw, parse_constant=_reject_constant, parse_float=_finite_float)
    except (ValueError, RecursionError):
        raise StudioAgentError("studio_turn_invalid") from None
    if type(value) is not dict:
        raise StudioAgentError("studio_turn_invalid")
    _depth(value)
    return value


def studio_json(raw, maximum: int, code: str = "studio_turn_invalid"):
    """Strict JSON for Studio turns: duplicate keys and NaN/Infinity refused, size and depth bounded.

    ai_brief.strict_json caps strings at 8 KB and depth at 10, which suits the fixed brief but not Studio's own
    instructions (12-17 KB) and tool schemas (deeper than 10); the closed checks below bound everything else.
    """
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate")
            result[key] = value
        return result

    def constant(_value):
        raise ValueError("nonfinite")
    if type(raw) is not bytes or not 0 < len(raw) <= maximum:
        raise StudioAgentError(code)
    try:
        document = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=pairs, parse_constant=constant,
                              parse_float=_finite_float)
        _depth(document, -4)
    except (ValueError, UnicodeError, RecursionError, StudioAgentError):
        raise StudioAgentError(code) from None
    return document


def _closed(value, keys: set) -> dict:
    if type(value) is not dict or set(value) != keys:
        raise StudioAgentError("studio_turn_invalid")
    return value


def validate_turn(body) -> dict:
    """The closed wire shape the dashboard's adapter sends; anything else is refused."""
    body = _closed(body, {"instructions", "items", "tools", "tool_choice", "response_format"})
    instructions = _text(body["instructions"], MAX_INSTRUCTIONS_CHARS)  # Studio's own prompt: checked like the rest
    items = body["items"]
    if type(items) is not list or not 0 < len(items) <= MAX_ITEMS:
        raise StudioAgentError("studio_turn_invalid")
    clean, called = [], set()
    for item in items:
        kind = item.get("kind") if type(item) is dict else None
        if kind == "user":
            _closed(item, {"kind", "text"})
            clean.append({"kind": "user", "text": _text(item["text"], MAX_QUESTION_CHARS, question=True)})
        elif kind == "context":
            _closed(item, {"kind", "text"})
            clean.append({"kind": "context", "text": _text(item["text"], MAX_CONTEXT_CHARS)})
        elif kind == "assistant":
            _closed(item, {"kind", "text"})
            clean.append({"kind": "assistant", "text": _text(item["text"], MAX_ASSISTANT_TEXT_CHARS)})
        elif kind == "call":
            _closed(item, {"kind", "call_id", "name", "arguments"})
            if type(item["call_id"]) is not str or not _CALL_ID.fullmatch(item["call_id"]) or type(item["name"]) is not str \
                    or not _TOOL_NAME.fullmatch(item["name"]):
                raise StudioAgentError("studio_turn_invalid")
            if has_personal_data(item["arguments"]) if type(item["arguments"]) is str else False:
                raise StudioAgentError("studio_turn_personal_data")
            arguments = _json_object(item["arguments"], MAX_ARGUMENTS_CHARS)
            called.add(item["call_id"])
            clean.append({"kind": "call", "call_id": item["call_id"], "name": item["name"], "arguments": arguments})
        elif kind == "result":
            _closed(item, {"kind", "call_id", "output"})
            # Type first: a list or object call_id is unhashable and made the set lookup a 500 (red team R3-STUDIO).
            if type(item["call_id"]) is not str or item["call_id"] not in called:
                raise StudioAgentError("studio_turn_invalid")
            output = _text(item["output"], MAX_TOOL_RESULT_CHARS, allow_empty=True)
            clean.append({"kind": "result", "call_id": item["call_id"], "output": output})
        else:
            raise StudioAgentError("studio_turn_invalid")
    if not any(entry["kind"] == "user" for entry in clean):
        raise StudioAgentError("studio_turn_invalid")
    # (r25 R1 P2-3) The free texts in order (question, context, assistant text, tool results), checked together.
    joined = [entry.get("text", entry.get("output")) for entry in clean if entry["kind"] != "call"]
    if _joined_personal_data([text for text in joined if type(text) is str]):
        raise StudioAgentError("studio_turn_personal_data")
    tools = body["tools"]
    if type(tools) is not list or len(tools) > MAX_TOOLS:
        raise StudioAgentError("studio_turn_invalid")
    clean_tools, names = [], set()
    for tool in tools:
        tool = _closed(tool, {"name", "description", "parameters"})
        if type(tool["name"]) is not str or not _TOOL_NAME.fullmatch(tool["name"]) or tool["name"] in names:
            raise StudioAgentError("studio_turn_invalid")
        if type(tool["parameters"]) is not dict:
            raise StudioAgentError("studio_turn_invalid")
        _depth(tool["parameters"])
        names.add(tool["name"])
        clean_tools.append({"name": tool["name"], "description": _text(tool["description"], MAX_TOOL_DESCRIPTION_CHARS),
                            "parameters": tool["parameters"]})
    encoded_tools = canonical_json(clean_tools)
    if len(encoded_tools) > MAX_TOOLS_JSON_BYTES:
        raise StudioAgentError("studio_turn_invalid")
    if has_personal_data(encoded_tools.decode("utf-8")):  # descriptions inside the parameter schemas too
        raise StudioAgentError("studio_turn_personal_data")
    choice = body["tool_choice"]
    if choice not in ("auto", "none", "required"):
        choice = _closed(choice, {"name"})
        if choice["name"] not in names:
            raise StudioAgentError("studio_turn_invalid")
        choice = {"name": choice["name"]}
    response_format = body["response_format"]
    if response_format == {"type": "text"}:
        response_format = {"type": "text"}
    else:
        response_format = _closed(response_format, {"type", "name", "schema"})
        if response_format["type"] != "json" or type(response_format["name"]) is not str \
                or not _FORMAT_NAME.fullmatch(response_format["name"]) or type(response_format["schema"]) is not dict:
            raise StudioAgentError("studio_turn_invalid")
        _depth(response_format["schema"])
        response_format = {"type": "json", "name": response_format["name"], "schema": response_format["schema"]}
    return {"instructions": instructions, "items": clean, "tools": clean_tools, "tool_choice": choice,
            "response_format": response_format}


class SignatureStore:
    """Thought signatures of the model's tool calls, per session and call id; bounded, never sent to the browser."""

    def __init__(self, per_session: int = SIGNATURES_PER_SESSION, sessions: int = SIGNATURE_SESSIONS):
        self._per_session, self._sessions = per_session, sessions
        self._lock = threading.Lock()
        self._store: OrderedDict[str, OrderedDict[str, str]] = OrderedDict()

    def keep(self, session_id: str, call_id: str, signature: str | None) -> None:
        if signature is None:
            return
        with self._lock:
            entries = self._store.setdefault(session_id, OrderedDict())
            entries[call_id] = signature
            entries.move_to_end(call_id)
            while len(entries) > self._per_session:
                entries.popitem(last=False)
            self._store.move_to_end(session_id)
            while len(self._store) > self._sessions:
                self._store.popitem(last=False)

    def get(self, session_id: str, call_id: str) -> str | None:
        with self._lock:
            return self._store.get(session_id, {}).get(call_id)


def worker_request(turn: dict, session_id: str, signatures: SignatureStore) -> bytes:
    """What crosses the subprocess boundary: the validated turn plus the stored signatures, nothing else."""
    items = []
    for item in turn["items"]:
        if item["kind"] == "call":
            items.append({**item, "signature": signatures.get(session_id, item["call_id"])})
        else:
            items.append(item)
    encoded = canonical_json({"operation": STUDIO_OPERATION, "schema_version": SCHEMA_VERSION,
                              "request": {**turn, "items": items}})
    if len(encoded) > MAX_WORKER_REQUEST_BYTES:
        raise StudioAgentError("studio_turn_invalid")
    return encoded


def validate_worker_request(document) -> dict:
    """The worker's own check of the same shape (signatures included), before anything reaches the provider."""
    document = _closed(document, {"operation", "schema_version", "request"})
    if document["operation"] != STUDIO_OPERATION or document["schema_version"] != SCHEMA_VERSION:
        raise StudioAgentError("studio_turn_invalid")
    request = document["request"]
    if type(request) is not dict or type(request.get("items")) is not list:
        raise StudioAgentError("studio_turn_invalid")
    signatures, items = {}, []
    for item in request["items"]:
        if type(item) is dict and item.get("kind") == "call":
            item = _closed(item, {"kind", "call_id", "name", "arguments", "signature"})
            signature = item["signature"]
            if signature is not None and (type(signature) is not str or len(signature) > MAX_SIGNATURE_BYTES * 2):
                raise StudioAgentError("studio_turn_invalid")
            signatures[item["call_id"]] = signature
            items.append({key: item[key] for key in ("kind", "call_id", "name")} | {"arguments": json.dumps(item["arguments"])})
        else:
            items.append(item)
    turn = validate_turn({**request, "items": items})
    for item in turn["items"]:
        if item["kind"] == "call":
            item["signature"] = signatures.get(item["call_id"])
    return turn


def validate_output(result, turn: dict) -> list[dict]:
    """The worker's reply: bounded items, advertised tools only, JSON when JSON was asked for."""
    result = _closed(result, {"output", "model"}) if type(result) is dict else None
    if result is None or result["model"] != MODEL or type(result["output"]) is not list:
        raise StudioAgentError("studio_agent_reply_invalid")
    output = result["output"]
    if not 0 < len(output) <= MAX_OUTPUT_ITEMS:
        raise StudioAgentError("studio_agent_reply_invalid")
    names = {tool["name"] for tool in turn["tools"]}
    clean, text_total = [], 0
    for item in output:
        kind = item.get("kind") if type(item) is dict else None
        if kind == "text":
            item = _closed(item, {"kind", "text"})
            if type(item["text"]) is not str or _CONTROL.search(item["text"]) or has_personal_data(item["text"]):
                raise StudioAgentError("studio_agent_reply_invalid")
            text_total += len(item["text"])
            if text_total > MAX_OUTPUT_TEXT_CHARS:
                raise StudioAgentError("studio_agent_reply_invalid")
            if turn["response_format"]["type"] == "json":
                try:
                    json.loads(item["text"])
                except ValueError:
                    raise StudioAgentError("studio_agent_reply_invalid") from None
            clean.append({"kind": "text", "text": item["text"]})
        elif kind == "call":
            item = _closed(item, {"kind", "name", "arguments", "signature"})
            if item["name"] not in names or turn["tool_choice"] == "none" or type(item["arguments"]) is not dict:
                raise StudioAgentError("studio_agent_reply_invalid")
            arguments = json.dumps(item["arguments"], separators=(",", ":"))
            if len(arguments) > MAX_ARGUMENTS_CHARS or has_personal_data(arguments):
                raise StudioAgentError("studio_agent_reply_invalid")
            signature = item["signature"]
            if signature is not None:
                try:
                    raw = base64.b64decode(signature, validate=True)
                except (binascii.Error, ValueError, TypeError):
                    raise StudioAgentError("studio_agent_reply_invalid") from None
                if not 0 < len(raw) <= MAX_SIGNATURE_BYTES:
                    raise StudioAgentError("studio_agent_reply_invalid")
            clean.append({"kind": "call", "name": item["name"], "arguments": arguments, "signature": signature})
        else:
            raise StudioAgentError("studio_agent_reply_invalid")
    if turn["tool_choice"] == "required" and not any(item["kind"] == "call" for item in clean):
        raise StudioAgentError("studio_agent_reply_invalid")
    return clean


def parse_envelope(raw: bytes, turn: dict) -> list[dict]:
    return parse_envelope_with_usage(raw, turn)[0]


def parse_envelope_with_usage(raw: bytes, turn: dict):
    """The checked output plus the worker's token counts or None (optimise r24: counts only, for the AI audit log)."""
    envelope = studio_json(raw, MAX_ENVELOPE_BYTES, "studio_agent_reply_invalid")
    if type(envelope) is not dict or set(envelope) - {"usage"} != {"schema_version", "status", "result"} or envelope["schema_version"] != SCHEMA_VERSION:
        raise StudioAgentError("studio_agent_reply_invalid")
    if envelope["status"] == "error":
        # The worker reports provider failures, rate limits and timeouts as an exit-0 envelope. These count as
        # failed calls for the breaker (see StudioAgentService.turn); a worker timeout is a timeout (504).
        result = envelope["result"]
        code = result.get("code") if type(result) is dict else None
        # (wo gemini run 2026-11-04) A reply the worker's own checks refused is a reply failure, not a provider failure,
        # so a live 502 says which side failed. Both still count for the breaker.
        if code == "ai_timeout":
            raise StudioAgentError("studio_agent_timeout")
        raise StudioAgentError("studio_agent_reply_refused" if code == "ai_response_invalid" else "studio_agent_provider_failure")
    if envelope["status"] != "ok":
        raise StudioAgentError("studio_agent_reply_invalid")
    try:
        usage = parse_usage(envelope.get("usage"))
    except UsageInvalid:
        raise StudioAgentError("studio_agent_reply_invalid") from None
    return validate_output(envelope["result"], turn), usage


def browser_output(output: list[dict], session_id: str, signatures: SignatureStore) -> list[dict]:
    """What the dashboard receives: text and tool calls with fresh call ids; signatures stay here."""
    clean = []
    for item in output:
        if item["kind"] == "text":
            clean.append({"type": "text", "text": item["text"]})
        else:
            call_id = "call_" + secrets.token_hex(12)
            signatures.keep(session_id, call_id, item["signature"])
            clean.append({"type": "call", "call_id": call_id, "name": item["name"], "arguments": item["arguments"]})
    return clean


class StudioAgentModel:
    """One governed worker call per turn; synchronous, run on this module's pool under the deadline."""

    __slots__ = ("_config", "_runner")

    def __init__(self, config, runner=None):
        if type(config) is AiConfig:
            if not config.enabled or config.python_bin is None or config.worker_path is None:
                raise StudioAgentError("studio_agents_off")
        elif type(config) is not ApiKeyProfileConfig:
            raise StudioAgentError("studio_agents_off")
        self._config, self._runner = config, runner

    @property
    def transport(self) -> str:
        return TRANSPORT_API_KEY if type(self._config) is ApiKeyProfileConfig else "vertex"

    def __repr__(self):
        return f"StudioAgentModel(transport={self.transport!r})"

    async def _run(self, payload: bytes) -> bytes:
        command = (str(self._config.python_bin), "-I", "-B", str(self._config.worker_path), "generate")
        environment = clean_api_key_worker_environment() if type(self._config) is ApiKeyProfileConfig \
            else clean_worker_environment(self._config.vertex_project)
        async with asyncio.timeout(GUIDE_WORKER_TIMEOUT_SECONDS):
            return await (self._runner or run_worker_subprocess)(command, payload, environment)

    def __call__(self, payload: bytes) -> bytes:
        try:
            return asyncio.run(self._run(payload))
        except (TimeoutError, asyncio.TimeoutError):
            raise StudioAgentError("studio_agent_timeout") from None
        except StudioAgentError:
            raise
        except Exception:
            raise StudioAgentError("studio_agent_provider_failure") from None


def studio_agents_requested() -> bool:
    return os.environ.get(STUDIO_AGENTS_ENV) == "gemini"


def configured_studio_model(*, public_demo: bool = False, config_loader=operator_ai_config,
                            api_key_loader=api_key_profile_config, runner=None) -> StudioAgentModel | None:
    """A model for Studio's built-in agents, or None (agents off). The hosted demo never builds one; with the
    flag off no configuration is inspected. One transport only, chosen like the guide's."""
    if public_demo or not studio_agents_requested():
        return None
    transport = guide_transport()
    try:
        if transport == TRANSPORT_API_KEY:
            config = api_key_loader()
            return StudioAgentModel(config, runner) if type(config) is ApiKeyProfileConfig else None
        if transport is None:
            return None
        config = config_loader()
        return StudioAgentModel(config, runner) if type(config) is AiConfig and config.enabled else None
    except (AiBriefError, StudioAgentError):
        return None


_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROVIDER_IN_FLIGHT, thread_name_prefix="studio-agent")


class StudioAgentService:
    """Governor + model + signature store, held by the app. ``model`` None means the agents are off."""

    def __init__(self, model: StudioAgentModel | None, governor: Governor | None = None,
                 signatures: SignatureStore | None = None, deadline: float = STUDIO_DEADLINE_SECONDS):
        self.model = model
        self.governor = governor or Governor(max_calls=STUDIO_CALLS_PER_SESSION, min_spacing=STUDIO_MIN_SPACING_SECONDS)
        self.signatures = signatures or SignatureStore()
        self.deadline = deadline
        # (optimise r24) The app's per-session AI audit log (counts and timings only); None records nothing.
        self.usage_log = None

    def _record_usage(self, session_id: str, started: float, usage, outcome: str) -> None:
        if self.usage_log is not None:
            self.usage_log.record(session_id, stage="studio_agent", model=MODEL, usage=usage,
                                  latency_ms=(time.monotonic() - started) * 1000, outcome=outcome)

    @property
    def live(self) -> bool:
        return self.model is not None

    def turn(self, session_id: str, body, client_id: str | None = None) -> list[dict]:
        """One governed turn. ``client_id`` (the caller's address) keys the per-client daily cap; the per-session
        count and spacing stay keyed by the session."""
        if self.model is None:
            raise StudioAgentError("studio_agents_off")
        try:
            turn = validate_turn(body)
            payload = worker_request(turn, session_id, self.signatures)
        except (AiBriefError, ValueError, TypeError, RecursionError):
            # (r25 R5 P2-1) canonical_json refusing a value is a contract failure of the turn, not a server error.
            raise StudioAgentError("studio_turn_invalid") from None
        refused, _previous = self.governor.admit(session_id, uses_model=True, client_id=client_id)
        if refused is not None:
            raise StudioAgentError("studio_agent_unavailable" if refused == "provider_unavailable" else "studio_agent_limit")
        failed = False
        try:
            if not self.governor.begin_call():
                raise StudioAgentError("studio_agent_limit")
            try:
                future = _POOL.submit(self.model, payload)
            except Exception:
                self.governor.end_call()
                raise
            future.add_done_callback(self.governor.end_call)
            started = time.monotonic()
            try:
                raw = future.result(timeout=self.deadline)
            except concurrent.futures.TimeoutError:
                future.cancel()
                failed = True
                self._record_usage(session_id, started, None, "error")
                raise StudioAgentError("studio_agent_timeout") from None
            except StudioAgentError as error:
                failed = error.code in ("studio_agent_timeout", "studio_agent_provider_failure", "studio_agent_reply_refused")
                self._record_usage(session_id, started, None, "error")
                raise
            try:
                output, usage = parse_envelope_with_usage(raw, turn)
            except StudioAgentError as error:
                # Error envelopes (provider failure, rate limit, timeout) feed the breaker like a raised failure.
                failed = error.code in ("studio_agent_timeout", "studio_agent_provider_failure", "studio_agent_reply_refused")
                self._record_usage(session_id, started, None, "error")
                raise
            self._record_usage(session_id, started, usage, "ok")
            return browser_output(output, session_id, self.signatures)
        finally:
            self.governor.finish(session_id, failed)


# The timeout ladder this route shares with the guide; asserted in the tests.
TIMEOUT_LADDER = (GUIDE_HTTP_TIMEOUT_SECONDS, GUIDE_PROVIDER_TIMEOUT_SECONDS, GUIDE_WORKER_TIMEOUT_SECONDS, STUDIO_DEADLINE_SECONDS)
