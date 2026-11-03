"""Channel3 product reference card: the seller's own product, enriched and confirmed by the seller.

A seller describes what they sell; Channel3 product search (``POST /v1/search``) returns up to three
catalogue products. PayGuard reduces each to a closed reference card (title, brand, category, key
features, materials, one https image) and the seller picks the one that is their product, or says
none is. Only a card the seller confirmed can be exported; it records what the item is, which is the
evidence a seller needs when a buyer later claims the item was not as described.

Same boundaries as the category signal in ``channel3.py``:

* Outbound: only the sanitised product name (``sanitize_product_name``) and ``limit`` leave the process.
* Inbound: offers, prices, merchant and buy URLs, ratings and every unknown field are dropped; any
  other shape is rejected and reported as unavailable. The card never changes the AUP decision.
* Off unless ``PAYGUARD_CHANNEL3=enabled`` and ``CHANNEL3_API_KEY`` are set. The key is sent only in
  ``x-api-key`` and never logged, returned or put in an exception message. Fixed timeout, call
  budget, no retry, no redirects, bounded body.
* Recorded mode (the public demo): replies recorded from real calls by ``tools/record_channel3.py``
  are replayed for the exact preset names and labelled as recorded; the server makes no Channel3 call (the
  visitor's browser still loads the recorded cards' images from Channel3's image host).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import threading
import unicodedata
from collections import OrderedDict
from typing import Callable, Mapping
from urllib.parse import urlsplit

import httpx

from .channel3 import CallBudget, Channel3Config, Channel3Error, sanitize_product_name

ENDPOINT = "https://api.trychannel3.com/v1/search"
RESULT_LIMIT = 3
TIMEOUT_SECONDS = 6.0
MAX_RESPONSE_BYTES = 524288
MAX_TITLE = 120
MAX_BRAND = 60
MAX_CATEGORY = 80
MAX_FEATURES = 4
MAX_FEATURE = 100
MAX_MATERIALS = 4
MAX_MATERIAL = 40
MAX_IMAGE_URL = 500
# Shown cards are kept per session: each session keeps its own last few evaluations, so one busy session can
# never push out another session's cards. The session count is bounded above the store's session cap.
MAX_REMEMBERED_PER_SESSION = 8
MAX_REMEMBERED_SESSIONS = 256
STATUSES = frozenset({"OFF", "FOUND", "NOT_FOUND", "NOT_SENT", "UNAVAILABLE"})
SOURCES = frozenset({"channel3_live", "channel3_recorded"})
RECORDED_PATH = pathlib.Path(__file__).resolve().parent / "data" / "channel3_recorded_v1.json"

_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")
_TEXT = re.compile(r"[^A-Za-z0-9 &'\-,./+()%\"]")
CARD_KEYS = ("product_id", "title", "brand", "category", "key_features", "materials", "image_url")


def _text(value: object, limit: int) -> str | None:
    """ASCII-folded, single-line, allowlisted text cut at a word boundary; ``None`` when nothing is left."""
    if type(value) is not str:
        return None
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", _TEXT.sub(" ", text)).strip(" -,./&+")
    if len(text) > limit:
        cut = text[:limit]
        text = (cut.rsplit(" ", 1)[0] if " " in cut else cut).strip(" -,./&+")
    return text if sum(ch.isalpha() for ch in text) >= 2 else None


def _image(images: object) -> str | None:
    """The main (else first) https image; anything else is dropped.

    A URL with ``@`` anywhere is skipped: the response schema and the frontend reject ``@`` in an image URL
    (it can carry user info or a lookalike host), and one such URL must not void every card in the reply.
    """
    if type(images) is not list:
        return None
    ordered = sorted((item for item in images if type(item) is dict), key=lambda item: item.get("is_main_image") is not True)
    for item in ordered:
        for key in ("cleaned_url", "url"):
            url = item.get(key)
            if (type(url) is str and len(url) <= MAX_IMAGE_URL and url.isascii() and "@" not in url
                    and not any(ch.isspace() for ch in url)):
                parts = urlsplit(url)
                if parts.scheme == "https" and parts.hostname and not parts.username and not parts.password:
                    return url
    return None


def _card(entry: object) -> dict:
    if type(entry) is not dict:
        raise Channel3Error("contract_rejected")
    product_id, title = entry.get("id"), _text(entry.get("title"), MAX_TITLE)
    if type(product_id) is not str or not _ID.fullmatch(product_id) or title is None:
        raise Channel3Error("contract_rejected")
    brands = entry.get("brands")
    brand = None
    if type(brands) is list and brands and type(brands[0]) is dict:
        brand = _text(brands[0].get("name"), MAX_BRAND)
    category = entry.get("category")
    category = _text(category.get("title"), MAX_CATEGORY) if type(category) is dict else None

    def listed(values, count, limit):
        if type(values) is not list:
            return []
        kept = [_text(value, limit) for value in values]
        return [value for value in kept if value is not None][:count]

    return {"product_id": product_id, "title": title, "brand": brand, "category": category,
            "key_features": listed(entry.get("key_features"), MAX_FEATURES, MAX_FEATURE),
            "materials": listed(entry.get("materials"), MAX_MATERIALS, MAX_MATERIAL),
            "image_url": _image(entry.get("images"))}


def _reject_constant(_value):
    raise ValueError("nonfinite")


def parse_search_response(body: bytes) -> list[dict]:
    """Reduce a ``POST /v1/search`` reply to at most three closed reference cards."""
    if type(body) is not bytes or len(body) > MAX_RESPONSE_BYTES:
        raise Channel3Error("contract_rejected")
    try:
        payload = json.loads(body.decode("utf-8"), parse_constant=_reject_constant)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise Channel3Error("contract_rejected") from None
    if type(payload) is not dict or type(payload.get("products")) is not list:
        raise Channel3Error("contract_rejected")
    cards, seen = [], set()
    for entry in payload["products"][:RESULT_LIMIT]:
        card = _card(entry)
        if card["product_id"] not in seen:
            seen.add(card["product_id"])
            cards.append(card)
    return cards


def card_digest(card: Mapping[str, object]) -> str:
    """sha256 of the card in canonical JSON; binds a confirmation to exactly what the seller saw."""
    canonical = json.dumps({key: card[key] for key in CARD_KEYS}, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


PostTransport = Callable[[str, Mapping[str, object], Mapping[str, str], float], tuple[int, bytes]]


def httpx_post_transport(url: str, body: Mapping[str, object], headers: Mapping[str, str], timeout: float) -> tuple[int, bytes]:
    """Single POST with a hard timeout, no redirects, no retry and a bounded body."""
    try:
        with httpx.Client(timeout=httpx.Timeout(timeout), follow_redirects=False, trust_env=False) as client:
            with client.stream("POST", url, json=dict(body), headers=headers) as response:
                data = bytearray()
                for chunk in response.iter_bytes():
                    data.extend(chunk)
                    if len(data) > MAX_RESPONSE_BYTES:
                        raise Channel3Error("contract_rejected")
                return response.status_code, bytes(data)
    except httpx.TimeoutException:
        raise Channel3Error("timeout") from None
    except httpx.HTTPError:
        raise Channel3Error("upstream_error") from None


def load_recorded(path: pathlib.Path = RECORDED_PATH) -> dict[str, dict]:
    """Recorded replies keyed by sanitised name; a missing or malformed file means no recordings."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if type(payload) is not dict or payload.get("schema_version") != "payguard.channel3_recorded.v1":
        return {}
    recorded = {}
    for item in payload.get("entries", []) if type(payload.get("entries")) is list else []:
        try:
            name = item["query"]
            cards = [_card_from_record(card) for card in item["cards"]]
            if sanitize_product_name(name) != name or not cards or len(cards) > RESULT_LIMIT:
                continue
            recorded[name] = {"cards": cards, "recorded_at": item["recorded_at"]}
        except (KeyError, TypeError, Channel3Error):
            continue
    return recorded


def _card_from_record(card: object) -> dict:
    """A recorded card must already be in the closed shape; re-reduce it to be sure."""
    if type(card) is not dict or set(card) != set(CARD_KEYS):
        raise Channel3Error("contract_rejected")
    rebuilt = _card({"id": card["product_id"], "title": card["title"],
                     "brands": [{"name": card["brand"]}] if card["brand"] is not None else None,
                     "category": {"title": card["category"]} if card["category"] is not None else None,
                     "key_features": card["key_features"], "materials": card["materials"],
                     "images": [{"url": card["image_url"], "is_main_image": True}] if card["image_url"] else None})
    if rebuilt != card:
        raise Channel3Error("contract_rejected")
    return rebuilt


def _result(status: str, source: str | None = None, cards: list | None = None, reason: str | None = None,
            recorded_at: str | None = None) -> dict:
    return {"status": status, "source": source, "cards": cards or [], "reason": reason, "recorded_at": recorded_at,
            "affects_decision": False}


class Channel3ProductAdapter:
    """Look up reference cards for a product name; returns a closed result and never raises."""

    def __init__(self, config: Channel3Config | None = None, *, transport: PostTransport | None = None,
                 budget: CallBudget | None = None, timeout: float = TIMEOUT_SECONDS,
                 recorded: Mapping[str, dict] | None = None):
        self.config = config if config is not None else Channel3Config.from_env()
        self._transport = transport or httpx_post_transport
        self.budget = budget if budget is not None else CallBudget()
        self.timeout = timeout
        self.recorded = dict(recorded or {})
        self._lock = threading.Lock()
        self._shown: OrderedDict[str, OrderedDict[str, dict]] = OrderedDict()

    @property
    def mode(self) -> str:
        return "live" if self.config.enabled else ("recorded" if self.recorded else "off")

    def lookup(self, description: object, *, budget: CallBudget | None = None) -> dict:
        """``budget`` lets a caller with its own allowance (case routing) spend that instead of the shared one."""
        if self.mode == "off":
            return _result("OFF")
        name = sanitize_product_name(description)
        if name is None:
            return _result("NOT_SENT", reason="nothing_to_send")
        if self.mode == "recorded":
            entry = self.recorded.get(name)
            if entry is None:
                return _result("NOT_SENT", reason="not_recorded")
            return _result("FOUND", "channel3_recorded", [dict(card) for card in entry["cards"]],
                           recorded_at=entry["recorded_at"])
        try:
            (budget if budget is not None else self.budget).reserve()
            status, body = self._transport(ENDPOINT, {"query": name, "limit": RESULT_LIMIT},
                                           {"x-api-key": self.config.api_key, "accept": "application/json",
                                            "content-type": "application/json"}, self.timeout)
            if type(status) is not int or status != 200:
                raise Channel3Error("upstream_error")
            cards = parse_search_response(body)
            return _result("FOUND" if cards else "NOT_FOUND", "channel3_live", cards)
        except Channel3Error as exc:
            return _result("UNAVAILABLE", reason=exc.code)
        except TimeoutError:
            return _result("UNAVAILABLE", reason="timeout")
        except Exception:
            return _result("UNAVAILABLE", reason="upstream_error")

    def remember(self, session_id: str, evaluation_id: str, result: Mapping[str, object]) -> None:
        """Keep the cards the seller was shown, so only one of them can be confirmed."""
        with self._lock:
            per_session = self._shown.setdefault(session_id, OrderedDict())
            per_session[evaluation_id] = {"source": result["source"], "recorded_at": result["recorded_at"],
                                          "cards": {card["product_id"]: dict(card) for card in result["cards"]}}
            per_session.move_to_end(evaluation_id)
            while len(per_session) > MAX_REMEMBERED_PER_SESSION:
                per_session.popitem(last=False)
            self._shown.move_to_end(session_id)
            while len(self._shown) > MAX_REMEMBERED_SESSIONS:
                self._shown.popitem(last=False)

    def shown(self, session_id: str, evaluation_id: str) -> dict | None:
        with self._lock:
            entry = self._shown.get(session_id, {}).get(evaluation_id)
            return None if entry is None else {"source": entry["source"], "recorded_at": entry["recorded_at"],
                                               "cards": dict(entry["cards"])}


def build_channel3_product_adapter(env: Mapping[str, str] | None = None, *, public_demo: bool = False,
                                   transport: PostTransport | None = None, budget: CallBudget | None = None,
                                   recorded_path: pathlib.Path = RECORDED_PATH) -> Channel3ProductAdapter:
    """Single construction point. The public demo never calls out; it replays recorded replies only."""
    if public_demo:
        return Channel3ProductAdapter(Channel3Config(enabled=False), transport=transport, budget=budget,
                                      recorded=load_recorded(recorded_path))
    return Channel3ProductAdapter(Channel3Config.from_env(env), transport=transport, budget=budget)
