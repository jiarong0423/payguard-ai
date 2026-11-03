"""Per-session AI call audit log: model, token counts, latency and an estimated cost (optimise r24).

What is kept per call: when it ended, the stage, the model id, the token counts the provider SDK reported
(usage_metadata.prompt_token_count / candidates_token_count / total_token_count), the latency in milliseconds,
the outcome ("ok" or "error") and an estimated USD cost. Never kept: the prompt, the reply, the session facts or
any other content, so the log can be shown to the session that made the calls without new disclosure.

The log lives in memory only, per demo session, bounded per session and in the number of sessions; it is dropped
with the session. The hosted demo never makes a model call and its route answers an empty list.
"""

from __future__ import annotations

from collections import OrderedDict, deque
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import re
import threading
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr


USAGE_FIELDS = ("prompt_token_count", "candidates_token_count", "total_token_count")
MAX_TOKEN_COUNT = 100_000_000
MAX_ENTRIES_PER_SESSION = 50
MAX_SESSIONS = 1024
MAX_LATENCY_MS = 3_600_000
_MODEL_ID = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")
STAGES = ("source_compliance", "velocity_guard", "dispute_mediation", "guide", "studio_agent")

# USD per one million tokens, (input, output), by model id (optimise r24).
# Source to check before adding a row: https://ai.google.dev/gemini-api/docs/pricing (AI Studio) and
# https://cloud.google.com/vertex-ai/generative-ai/pricing (Vertex AI). The configured model (gemini-3.8-flash)
# could not be confirmed against those pages from this offline build, so the table is empty on purpose: the log
# stores token counts only and estimated_cost_usd stays null until the owner adds a checked row here.
PRICE_TABLE_USD_PER_MILLION: dict[str, tuple[Decimal, Decimal]] = {}
PRICE_TABLE_SOURCE = "https://ai.google.dev/gemini-api/docs/pricing"


class UsageInvalid(ValueError):
    """The usage counts in a worker envelope are not the closed shape."""


def parse_usage(value) -> dict | None:
    """The worker envelope's optional "usage": exactly the three SDK counts, each an int in range or null."""
    if value is None:
        return None
    if type(value) is not dict or set(value) != set(USAGE_FIELDS):
        raise UsageInvalid("usage_invalid")
    for name in USAGE_FIELDS:
        count = value[name]
        if count is not None and (type(count) is not int or not 0 <= count <= MAX_TOKEN_COUNT):
            raise UsageInvalid("usage_invalid")
    return {name: value[name] for name in USAGE_FIELDS}


def estimate_cost_usd(model: str | None, tokens_in: int | None, tokens_out: int | None) -> str | None:
    """Estimated USD as a decimal string, or None when the model has no checked price row or a count is missing."""
    prices = PRICE_TABLE_USD_PER_MILLION.get(model or "")
    if prices is None or tokens_in is None or tokens_out is None:
        return None
    cost = (Decimal(tokens_in) * prices[0] + Decimal(tokens_out) * prices[1]) / Decimal(1_000_000)
    return str(cost.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


class AiUsageEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    at: StrictStr
    stage: Literal["source_compliance", "velocity_guard", "dispute_mediation", "guide", "studio_agent"]
    model: StrictStr | None = Field(default=None, pattern=r"^[A-Za-z0-9_.:/-]{1,128}$")
    outcome: Literal["ok", "error"]
    tokens_in: StrictInt | None = Field(default=None, ge=0, le=MAX_TOKEN_COUNT)
    tokens_out: StrictInt | None = Field(default=None, ge=0, le=MAX_TOKEN_COUNT)
    tokens_total: StrictInt | None = Field(default=None, ge=0, le=MAX_TOKEN_COUNT)
    latency_ms: StrictInt = Field(ge=0, le=MAX_LATENCY_MS)
    estimated_cost_usd: StrictStr | None = Field(default=None, pattern=r"^[0-9]{1,9}\.[0-9]{6}$")


class AiUsageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    source: Literal["session_memory", "hosted_demo"]
    entries: list[AiUsageEntry] = Field(max_length=MAX_ENTRIES_PER_SESSION)
    price_table_source: StrictStr
    cost_note: StrictStr
    content_logged: Literal[False] = False


COST_NOTE = ("Estimated cost is null unless the model has a price row checked against the provider's published "
             "pricing; token counts are what the provider SDK reported.")


class AiUsageLog:
    """Thread-safe, bounded, per-session; holds counts and timings only."""

    def __init__(self, *, clock=None):
        self._lock = threading.Lock()
        self._entries: OrderedDict[str, deque] = OrderedDict()
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def record(self, session_id: str, *, stage: str, model: str | None, usage: dict | None, latency_ms, outcome: str) -> None:
        if type(session_id) is not str or not session_id or stage not in STAGES or outcome not in ("ok", "error"):
            return
        try:
            usage = parse_usage(usage)
        except UsageInvalid:
            usage = None
        usage = usage or {}
        tokens_in = usage.get("prompt_token_count")
        tokens_out = usage.get("candidates_token_count")
        model = model if type(model) is str and _MODEL_ID.fullmatch(model) is not None else None
        try:
            latency = max(0, min(MAX_LATENCY_MS, int(round(float(latency_ms)))))
        except (TypeError, ValueError, OverflowError):
            latency = 0
        entry = AiUsageEntry(
            at=self._clock().astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            stage=stage, model=model, outcome=outcome, tokens_in=tokens_in, tokens_out=tokens_out,
            tokens_total=usage.get("total_token_count"), latency_ms=latency,
            estimated_cost_usd=estimate_cost_usd(model, tokens_in, tokens_out) if outcome == "ok" else None,
        ).model_dump()
        with self._lock:
            rows = self._entries.pop(session_id, None)
            if rows is None:
                rows = deque(maxlen=MAX_ENTRIES_PER_SESSION)
            rows.append(entry)
            self._entries[session_id] = rows
            while len(self._entries) > MAX_SESSIONS:
                self._entries.popitem(last=False)

    def entries(self, session_id: str) -> list[dict]:
        with self._lock:
            return [dict(row) for row in self._entries.get(session_id, ())]

    def forget_missing(self, live_session_ids) -> None:
        """Drop the log of every session the store no longer holds."""
        live = set(live_session_ids)
        with self._lock:
            for stale in [key for key in self._entries if key not in live]:
                del self._entries[stale]
