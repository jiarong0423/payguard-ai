"""Optional Channel3 product-category signal for the AUP preflight (off by default).

The signal sits next to the keyword AUP result and never changes it. The adapter is closed in both
directions:

* Outbound: only a sanitised product name leaves the process (ASCII, at most 120 characters, no
  email addresses, URLs, digit runs longer than four, or capitalised names after "for"/"to").
* Inbound: the provider reply is reduced to ``{"category", "confidence", "source"}``; any other
  shape is rejected and reported as unavailable.

It is enabled only when ``PAYGUARD_CHANNEL3=enabled`` and ``CHANNEL3_API_KEY`` is set. The key is
read from the environment, sent only in the ``x-api-key`` header, and never logged, returned or
included in an exception message. Each call has a fixed timeout and draws from a per-process call
budget. There is no retry.
"""

from __future__ import annotations

import json
import os
import re
import threading
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, Mapping

import httpx

ENDPOINT = "https://api.trychannel3.com/v1/categories/search"
RESULT_LIMIT = 3
TIMEOUT_SECONDS = 4.0
DEFAULT_CALL_BUDGET = 20
MAX_NAME_CHARS = 120
MAX_CATEGORY_CHARS = 80
MAX_RESPONSE_BYTES = 65536
SIGNAL_KEYS = frozenset({"category", "confidence", "source"})
CONFIDENCE_VALUES = frozenset({"HIGH", "LOW"})
STATUSES = frozenset({"OFF", "SIGNAL", "NOT_SENT", "UNAVAILABLE"})
REASONS = frozenset({"nothing_to_send", "budget_exhausted", "timeout", "upstream_error", "contract_rejected"})

_URL = re.compile(r"(?i)\b(?:[a-z][a-z0-9+.-]*://\S+|www\.\S+|[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|io|co|us|ai|app|dev|shop|store|biz|info|me|xyz)\b\S*)")
_EMAIL = re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")
_HANDLE = re.compile(r"(?<!\w)@\w+")
# A digit run joined by common separators (phone, card, order and account numbers).
_DIGIT_RUN = re.compile(r"\d(?:[\s().\-/]{0,2}\d)*")
# "for"/"to" followed by one or more capitalised words is treated as a person or business name.
_NAME_AFTER = re.compile(r"\b(?:[Ff]or|[Tt]o|FOR|TO)\s+[A-Z][A-Za-z'\-]*\.?(?:\s+[A-Z][A-Za-z'\-]*\.?)*")
_DISALLOWED = re.compile(r"[^A-Za-z0-9 &'\-,./+%]")
_CATEGORY_TEXT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 &'\-,./+()]*$")


class Channel3Error(Exception):
    """Closed failure with a code from ``REASONS``; never carries provider or key text."""

    def __init__(self, code: str):
        if code not in REASONS:
            code = "upstream_error"
        super().__init__(code)
        self.code = code


def sanitize_product_name(description: object) -> str | None:
    """Return the only text that may be sent to Channel3, or ``None`` when nothing safe remains."""
    if not isinstance(description, str):
        return None
    lines = [line.strip() for line in description.splitlines() if line.strip()]
    if not lines:
        return None
    text = unicodedata.normalize("NFKD", lines[0]).encode("ascii", "ignore").decode("ascii")
    text = _URL.sub(" ", _EMAIL.sub(" ", text))
    text = _HANDLE.sub(" ", text)
    text = _DIGIT_RUN.sub(lambda m: " " if sum(ch.isdigit() for ch in m.group(0)) > 4 else m.group(0), text)
    text = _NAME_AFTER.sub(" ", text)
    text = _DISALLOWED.sub(" ", text)
    text = re.sub(r"\s+([,.])", r"\1", re.sub(r"\s+", " ", text)).strip(" -,./&+")
    if len(text) > MAX_NAME_CHARS:
        cut = text[:MAX_NAME_CHARS]
        text = (cut.rsplit(" ", 1)[0] if " " in cut else cut).strip(" -,./&+")
    if sum(ch.isalpha() for ch in text) < 2:
        return None
    return text


def validate_signal(signal: object) -> dict:
    """Accept only the closed category-signal contract; raise ``Channel3Error`` otherwise."""
    if type(signal) is not dict or set(signal) != SIGNAL_KEYS:
        raise Channel3Error("contract_rejected")
    category, confidence = signal["category"], signal["confidence"]
    if signal["source"] != "channel3" or type(signal["source"]) is not str:
        raise Channel3Error("contract_rejected")
    if category is None:
        if confidence is not None:
            raise Channel3Error("contract_rejected")
    elif (type(category) is not str or not 1 <= len(category) <= MAX_CATEGORY_CHARS or
          not _CATEGORY_TEXT.fullmatch(category) or type(confidence) is not str or confidence not in CONFIDENCE_VALUES):
        raise Channel3Error("contract_rejected")
    return {"category": category, "confidence": confidence, "source": "channel3"}


def _category_entry(entry: object) -> tuple[str, str]:
    if type(entry) is not dict:
        raise Channel3Error("contract_rejected")
    title, path = entry.get("title"), entry.get("path")
    if type(title) is not str or type(entry.get("slug")) is not str:
        raise Channel3Error("contract_rejected")
    root = entry["slug"]
    if path is not None:
        if type(path) is not list or any(type(item) is not dict or type(item.get("slug")) is not str for item in path):
            raise Channel3Error("contract_rejected")
        if path:
            root = path[0]["slug"]
    title = re.sub(r"\s+", " ", unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")).strip()
    return title, root


def _reject_constant(_value):
    raise ValueError("nonfinite")


def parse_categories_response(body: bytes) -> dict:
    """Reduce a ``GET /v1/categories/search`` reply to the closed signal contract.

    Channel3 returns categories ordered by relevance but no score, so confidence is PayGuard's own
    label: HIGH when the top result is the only one or shares its root category with the runner-up,
    LOW otherwise. Unknown provider fields are dropped, never passed through.
    """
    if type(body) is not bytes or len(body) > MAX_RESPONSE_BYTES:
        raise Channel3Error("contract_rejected")
    try:
        payload = json.loads(body.decode("utf-8"), parse_constant=_reject_constant)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise Channel3Error("contract_rejected") from None
    if type(payload) is not dict or type(payload.get("categories")) is not list:
        raise Channel3Error("contract_rejected")
    entries = [_category_entry(entry) for entry in payload["categories"][:RESULT_LIMIT]]
    if not entries:
        return validate_signal({"category": None, "confidence": None, "source": "channel3"})
    title, root = entries[0]
    confidence = "HIGH" if len(entries) == 1 or entries[1][1] == root else "LOW"
    return validate_signal({"category": title, "confidence": confidence, "source": "channel3"})


class CallBudget:
    """Process-local, thread-safe ceiling on outbound Channel3 calls."""

    def __init__(self, limit: int = DEFAULT_CALL_BUDGET):
        if type(limit) is not int or limit < 0:
            raise ValueError("budget_invalid")
        self.limit = limit
        self.used = 0
        self._lock = threading.Lock()

    def reserve(self) -> None:
        with self._lock:
            if self.used >= self.limit:
                raise Channel3Error("budget_exhausted")
            self.used += 1

    @property
    def remaining(self) -> int:
        with self._lock:
            return self.limit - self.used


Transport = Callable[[str, Mapping[str, str], Mapping[str, str], float], tuple[int, bytes]]


def httpx_transport(url: str, params: Mapping[str, str], headers: Mapping[str, str], timeout: float) -> tuple[int, bytes]:
    """Single GET with a hard timeout, no redirects, no retry and a bounded body."""
    try:
        with httpx.Client(timeout=httpx.Timeout(timeout), follow_redirects=False, trust_env=False) as client:
            with client.stream("GET", url, params=params, headers=headers) as response:
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise Channel3Error("contract_rejected")
                return response.status_code, bytes(body)
    except httpx.TimeoutException:
        raise Channel3Error("timeout") from None
    except httpx.HTTPError:
        raise Channel3Error("upstream_error") from None


@dataclass(frozen=True)
class Channel3Config:
    enabled: bool
    api_key: str = field(default="", repr=False)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "Channel3Config":
        source = os.environ if env is None else env
        key = (source.get("CHANNEL3_API_KEY") or "").strip()
        enabled = source.get("PAYGUARD_CHANNEL3") == "enabled" and bool(key)
        return cls(enabled=enabled, api_key=key if enabled else "")


def _result(status: str, signal: dict | None = None, reason: str | None = None) -> dict:
    return {"status": status, "signal": signal, "reason": reason, "affects_decision": False}


class Channel3CategoryAdapter:
    """Look up an optional category signal; returns a closed result and never raises."""

    def __init__(self, config: Channel3Config | None = None, *, transport: Transport | None = None,
                 budget: CallBudget | None = None, timeout: float = TIMEOUT_SECONDS):
        self.config = config if config is not None else Channel3Config.from_env()
        self._transport = transport or httpx_transport
        self.budget = budget if budget is not None else CallBudget()
        self.timeout = timeout

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    def lookup(self, description: object) -> dict:
        if not self.config.enabled:
            return _result("OFF")
        name = sanitize_product_name(description)
        if name is None:
            return _result("NOT_SENT", reason="nothing_to_send")
        try:
            self.budget.reserve()
            status, body = self._transport(ENDPOINT, {"query": name, "limit": str(RESULT_LIMIT)},
                                           {"x-api-key": self.config.api_key, "accept": "application/json"},
                                           self.timeout)
            if type(status) is not int or status != 200:
                raise Channel3Error("upstream_error")
            return _result("SIGNAL", signal=parse_categories_response(body))
        except Channel3Error as exc:
            return _result("UNAVAILABLE", reason=exc.code)
        except TimeoutError:
            return _result("UNAVAILABLE", reason="timeout")
        except Exception:
            return _result("UNAVAILABLE", reason="upstream_error")


def build_channel3_adapter(env: Mapping[str, str] | None = None, *, force_off: bool = False,
                           transport: Transport | None = None, budget: CallBudget | None = None) -> Channel3CategoryAdapter:
    """Single construction point. ``force_off=True`` (e.g. a demo mode) disables it whatever the env says."""
    config = Channel3Config(enabled=False) if force_off else Channel3Config.from_env(env)
    return Channel3CategoryAdapter(config, transport=transport, budget=budget)
