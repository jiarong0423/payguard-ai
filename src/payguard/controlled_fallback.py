"""Controlled fallback for reference searches that find nothing.

The normal search runs first. Only when it returns evidence_missing may a chooser run.
The chooser sees a cleaned question plus closed context values and must answer exactly
{"route": <label>} with one label from a closed list: a topic route, or one of three
policy actions (professional advice, harmful request, off topic). The label maps to a
fixed theme and fixed query, or to a fixed message code. The user never sees chooser
text. A route that belongs to another flow is not searched; the user is told which flow
handles it. A wrong or unusable answer gets one retry, then the keyword chooser.
"""

import concurrent.futures
import ipaddress
import json
import re
import threading
import time
import unicodedata
from collections import OrderedDict

MAX_QUERY_CHARS = 200
MAX_INPUT_CHARS = MAX_QUERY_CHARS * 4
MAX_DIGITS = 4
MAX_TOKEN_CHARS = 15
MAX_NUMBER_WORDS = 3
MAX_PROVIDER_RESPONSE_BYTES = 256
MAX_SESSION_ID_CHARS = 64
MAX_CALLS_PER_SESSION = 3
MIN_SECONDS_BETWEEN_CALLS = 5.0
MAX_TRACKED_SESSIONS = 1000
SESSION_TTL_SECONDS = 3600.0
IDLE_EVICT_SECONDS = 300.0
MAX_ATTEMPTS = 2
CALLS_PER_CLIENT_PER_DAY = 20
GLOBAL_CALLS_PER_DAY = 500
DAY_SECONDS = 86400.0
GLOBAL_CALLS_PER_MINUTE = 30
BREAKER_FAILURES = 3
BREAKER_OPEN_SECONDS = 60.0
PROVIDER_TIMEOUT_SECONDS = 8.0
MAX_PROVIDER_IN_FLIGHT = 4

REDIRECT_PROFESSIONAL = "REDIRECT_PROFESSIONAL"
REFUSE_HARMFUL = "REFUSE_HARMFUL"
OFF_TOPIC = "OFF_TOPIC"
POLICY_ACTIONS = {
    REDIRECT_PROFESSIONAL: ("redirect_professional", "PROFESSIONAL_ADVICE_NOT_PROVIDED"),
    REFUSE_HARMFUL: ("refused", "REQUEST_REFUSED"),
    OFF_TOPIC: ("off_topic", "OUTSIDE_PAYGUARD_SCOPE"),
}

# label -> (theme, fixed query). Each pair was checked to return references in the pinned corpus.
ROUTES = {
    "ACCEPTABLE_USE": ("source_compliance", "AUP"),
    "HOLDS_AND_RESERVES": ("velocity_guard", "hold"),
    "SALES_GROWTH": ("velocity_guard", "rapid sales growth"),
    "DISPUTE_OVERVIEW": ("dispute_mediation", "dispute"),
    "ITEM_NOT_RECEIVED": ("dispute_mediation", "not received"),
    "DELIVERY_EVIDENCE": ("dispute_mediation", "tracking"),
    "SELLER_PROTECTION": ("dispute_mediation", "seller protection"),
    "REFUND_REASONS": ("dispute_mediation", "refund"),
    "INVOICING": ("source_compliance", "invoice"),
    "SANDBOX_TESTING": ("source_compliance", "sandbox"),
    "COURT_ORDERS": ("source_compliance", "court order"),
}

FLOWS = {"preflight": "source_compliance", "velocity": "velocity_guard", "dispute": "dispute_mediation"}
ANSWER_LABELS = tuple(sorted(ROUTES)) + tuple(sorted(POLICY_ACTIONS))

STATUSES = (
    "not_triggered", "disabled", "request_invalid", "query_not_sendable", "limit_reached",
    "provider_unavailable", "provider_failed", "provider_invalid", "redirect_professional",
    "refused", "off_topic", "other_flow", "related_found", "still_missing",
)

_NUMBER_WORDS = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
    r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|oh|nil)\b",
    re.IGNORECASE)
_SPOKEN_DOT = re.compile(r"\b(?:dot|arroba)\b", re.IGNORECASE)
_SPOKEN_AT = re.compile(r"\b(?:at|arroba)\b", re.IGNORECASE)
_SPOKEN_TLD = re.compile(r"\b(?:dot|period|point|com|net|org)\b", re.IGNORECASE)
_DOMAIN_LIKE = re.compile(r"[^\W\d_]\.[^\W\d_]")
_MIXED_TOKEN = re.compile(r"[^\W\d_]\d[^\W\d_]")
_ALLOWED_PUNCTUATION = set(" .,?!'-")


def sanitize_query(query):
    """Return a text that is safe to hand to the chooser, or None when it must not be sent."""
    if not isinstance(query, str) or not query or len(query) > MAX_INPUT_CHARS:
        return None
    text = " ".join(unicodedata.normalize("NFKC", query).split())
    if not text or len(text) > MAX_QUERY_CHARS:
        return None
    digits = 0
    for char in text:
        category = unicodedata.category(char)
        if category == "Nd":
            digits += 1
        elif not (category.startswith("L") or char in _ALLOWED_PUNCTUATION):
            return None
    if digits > MAX_DIGITS or any(len(token) > MAX_TOKEN_CHARS for token in text.split()):
        return None
    if len(_NUMBER_WORDS.findall(text)) > MAX_NUMBER_WORDS or _SPOKEN_DOT.search(text):
        return None
    if _SPOKEN_AT.search(text) and _SPOKEN_TLD.search(text) or _DOMAIN_LIKE.search(text):
        return None
    for token in text.split():
        uppers = sum(1 for char in token if char.isupper())
        if _MIXED_TOKEN.search(token) or (len(token) >= 8 and uppers >= 3 and not token.isupper()):
            return None
    return text


def client_key(address):
    """Server-observed client address as the identity: IPv4 as is, IPv6 reduced to its /64."""
    if type(address) is not str or len(address) > 64:
        return None
    try:
        parsed = ipaddress.ip_address(address.strip())
    except ValueError:
        return None
    if parsed.version == 6:
        if parsed.ipv4_mapped is not None:
            return str(parsed.ipv4_mapped)
        return str(ipaddress.ip_network(f"{parsed}/64", strict=False))
    return str(parsed)


def _no_duplicates(pairs):
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key")
    return dict(pairs)


def validate_choice(raw):
    """Accept only a JSON object with the single key route and a known answer label."""
    if type(raw) is str:
        raw = raw.encode("utf-8", "strict")
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_PROVIDER_RESPONSE_BYTES:
        return None
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicates)
    except (ValueError, UnicodeError, RecursionError):
        return None
    if type(value) is not dict or set(value) != {"route"} or type(value["route"]) is not str:
        return None
    return value["route"] if value["route"] in ANSWER_LABELS else None


def chooser_request(query, flow, previous_route, attempt):
    """Everything the chooser may see: cleaned text plus closed context values."""
    allowed = sorted(label for label, (theme, _) in ROUTES.items() if theme == FLOWS[flow])
    return {
        "task": "choose_route",
        "query": query,
        "flow": flow,
        "previous_route": previous_route,
        "attempt": attempt,
        "routes": list(ANSWER_LABELS),
        "routes_for_flow": allowed,
    }


class Governor:
    """In-memory limits: per session, global rate, failure breaker and in-flight cap."""

    def __init__(self, clock=time.monotonic, max_calls=None, min_spacing=None, global_per_minute=None,
                 global_per_day=None):
        self._clock = clock
        self._max_calls = MAX_CALLS_PER_SESSION if max_calls is None else max_calls
        self._min_spacing = MIN_SECONDS_BETWEEN_CALLS if min_spacing is None else min_spacing
        # (r32 hosted guide) The hosted demo runs on a free-tier key, so it may only lower the shared caps, never raise
        # them above the module defaults.
        self._global_per_minute = GLOBAL_CALLS_PER_MINUTE if global_per_minute is None else min(global_per_minute,
                                                                                                GLOBAL_CALLS_PER_MINUTE)
        self._global_per_day = GLOBAL_CALLS_PER_DAY if global_per_day is None else min(global_per_day, GLOBAL_CALLS_PER_DAY)
        self._lock = threading.Lock()
        self._sessions = OrderedDict()
        self._global = []
        self._daily = OrderedDict()
        self._global_day = []
        self._failures = 0
        self._open_until = 0.0
        self._probing = False
        self._in_flight = 0

    def _take_global(self, now):
        self._global = [stamp for stamp in self._global if now - stamp < 60.0]
        if len(self._global) >= self._global_per_minute:
            return False
        self._global.append(now)
        return True

    def _breaker(self, now):
        if now < self._open_until:
            return "provider_unavailable"
        if self._open_until and not self._probing:
            self._probing = True
            return None
        if self._open_until and self._probing:
            return "provider_unavailable"
        return None

    def admit(self, session_id, uses_model=True, client_id=None):
        """``client_id`` (optional) keys the per-client daily cap; without it the session id does, as before."""
        if type(session_id) is not str or not 0 < len(session_id) <= MAX_SESSION_ID_CHARS:
            return "limit_reached", None
        if client_id is not None and (type(client_id) is not str or not 0 < len(client_id) <= MAX_SESSION_ID_CHARS):
            return "limit_reached", None
        daily_key = session_id if client_id is None else f"client:{client_id}"
        now = self._clock()
        with self._lock:
            refused = self._breaker(now) if uses_model else None
            if refused:
                return refused, None
            expired = [key for key, (_, last, _) in self._sessions.items() if now - last >= SESSION_TTL_SECONDS]
            for key in expired:
                del self._sessions[key]
            count, last, previous = self._sessions.get(session_id, (0, None, None))
            if session_id not in self._sessions and len(self._sessions) >= MAX_TRACKED_SESSIONS:
                oldest = next(iter(self._sessions))
                if now - self._sessions[oldest][1] < IDLE_EVICT_SECONDS:
                    self._release_probe()
                    return "limit_reached", None
                del self._sessions[oldest]
            if count >= self._max_calls or (last is not None and now - last < self._min_spacing):
                self._release_probe()
                return "limit_reached", None
            stamps = [stamp for stamp in self._daily.get(daily_key, ()) if now - stamp < DAY_SECONDS]
            self._global_day = [stamp for stamp in self._global_day if now - stamp < DAY_SECONDS]
            if len(stamps) >= CALLS_PER_CLIENT_PER_DAY or len(self._global_day) >= self._global_per_day:
                self._release_probe()
                return "limit_reached", None
            if not self._take_global(now):
                self._release_probe()
                return "limit_reached", None
            stamps.append(now)
            self._daily[daily_key] = stamps
            self._daily.move_to_end(daily_key)
            while len(self._daily) > MAX_TRACKED_SESSIONS:
                self._daily.popitem(last=False)
            self._global_day.append(now)
            self._sessions[session_id] = (count + 1, now, previous)
            self._sessions.move_to_end(session_id)
            return None, previous

    def _release_probe(self):
        if self._open_until and self._probing and self._clock() >= self._open_until:
            self._probing = False

    def begin_call(self):
        """Reserve a worker slot; it is released only when the worker really finishes."""
        with self._lock:
            if self._in_flight >= MAX_PROVIDER_IN_FLIGHT:
                return False
            self._in_flight += 1
            return True

    def end_call(self, _future=None):
        with self._lock:
            self._in_flight = max(0, self._in_flight - 1)

    def extra_attempt(self):
        """The one identical resend: counted against the per-minute and the global daily caps (r25 R1 P2-4)."""
        with self._lock:
            now = self._clock()
            self._global_day = [stamp for stamp in self._global_day if now - stamp < DAY_SECONDS]
            if len(self._global_day) >= self._global_per_day or not self._take_global(now):
                return False
            self._global_day.append(now)
            return True

    def finish(self, session_id, failed, route=None):
        """Release the in-flight slot. Only provider exceptions and timeouts feed the breaker."""
        with self._lock:
            if failed:
                self._failures += 1
                if self._failures >= BREAKER_FAILURES or self._probing:
                    self._open_until = self._clock() + BREAKER_OPEN_SECONDS
                    self._failures = 0
                self._probing = False
                return
            self._failures = 0
            if self._probing:
                self._open_until = 0.0
                self._probing = False
            if route is not None and session_id in self._sessions:
                count, last, _ = self._sessions[session_id]
                self._sessions[session_id] = (count, last, route)


_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROVIDER_IN_FLIGHT, thread_name_prefix="fallback")


class _Busy(Exception):
    pass


def _call_provider(governor, provider, request):
    if not governor.begin_call():
        raise _Busy()
    try:
        future = _POOL.submit(provider, request)
    except Exception:
        governor.end_call()
        raise
    future.add_done_callback(governor.end_call)
    try:
        return future.result(timeout=PROVIDER_TIMEOUT_SECONDS)
    except concurrent.futures.TimeoutError:
        future.cancel()
        raise


def _outcome(status, route=None, result=None, message_code=None, handled_by=None, chooser=None):
    return {
        "status": status,
        "route": route,
        "result": result,
        "message_code": message_code,
        "handled_by_flow": handled_by,
        "chooser": chooser,
        "model_text_shown": False,
        "advisory_only": True,
    }


def _flow_of(theme):
    return next(name for name, value in FLOWS.items() if value == theme)


def _settle(label, flow, search, chooser):
    if label in POLICY_ACTIONS:
        status, code = POLICY_ACTIONS[label]
        return _outcome(status, message_code=code, chooser=chooser)
    theme, fixed_query = ROUTES[label]
    if theme != FLOWS[flow]:
        return _outcome("other_flow", route=label, message_code="HANDLED_IN_OTHER_FLOW",
                        handled_by=_flow_of(theme), chooser=chooser)
    try:
        result = search(theme, fixed_query)
    except Exception:
        return _outcome("still_missing", route=label, chooser=chooser)
    filters = result.get("filters_applied") if isinstance(result, dict) else None
    belongs = isinstance(filters, dict) and filters.get("theme") == theme
    found = isinstance(result, dict) and result.get("status") == "references_found" and belongs
    return _outcome("related_found" if found else "still_missing", route=label,
                    result=result if found else None, chooser=chooser)


def run_fallback(session_id, flow, query, first_result, search, provider, governor, enabled):
    """Run the controlled loop once. search(theme, query) is the ordinary reference search.

    provider is the model chooser; when it is None the keyword chooser is used. The
    provider is only called after the ordinary search found nothing, the query passed
    cleaning, and the governor admitted the run.
    """
    if not isinstance(first_result, dict) or first_result.get("status") != "evidence_missing":
        return _outcome("not_triggered")
    if enabled is not True:
        return _outcome("disabled")
    if type(flow) is not str or flow not in FLOWS:
        return _outcome("request_invalid")
    text = sanitize_query(query)
    if text is None:
        return _outcome("query_not_sendable")
    refused, previous = governor.admit(session_id, uses_model=provider is not None)
    if refused is not None:
        return _outcome(refused)
    chooser = "model" if provider is not None else "keyword"
    label = None
    failed = False
    busy = False
    try:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            if attempt > 1 and not governor.extra_attempt():
                break
            request = chooser_request(text, flow, previous, attempt)
            try:
                raw = keyword_provider(request) if provider is None else _call_provider(governor, provider, request)
            except _Busy:
                busy = True
                break
            except Exception:
                failed = True
                break
            label = validate_choice(raw)
            if label is not None:
                break
        if label is None and not failed and not busy:
            label = validate_choice(keyword_provider(chooser_request(text, flow, previous, MAX_ATTEMPTS)))
            chooser = "keyword_fallback"
    finally:
        governor.finish(session_id, failed, label if label in ROUTES else None)
    if busy:
        return _outcome("provider_unavailable")
    if failed:
        return _outcome("provider_failed")
    if label is None:
        return _outcome("provider_invalid")
    return _settle(label, flow, search, chooser)


_KEYWORDS = (
    (REFUSE_HARMFUL, (r"\bignore (?:all|the|your|previous|these|any)\b", r"\bpretend\b", r"\bsystem prompt\b",
                      r"\bprevious instructions\b", r"\b(?:show|reveal|tell|give|read|print)\b.{0,20}\b(?:instructions|rules|prompt)\b",
                      r"\bhidden rules\b", r"\bdeveloper mode\b", r"\bas the developer\b", r"\bkill", r"\bhurt\b", r"\bweapon", r"\bhack")),
    (REDIRECT_PROFESSIONAL, (r"\blawyer", r"\battorney", r"\bsue\b", r"\blegal advice\b", r"\btax advice\b",
                             r"\binvestment advice\b", r"\bdiagnos")),
    ("HOLDS_AND_RESERVES", (r"\bhold", r"\breserve", r"\bfrozen\b", r"\bfreez", r"\bwithheld\b")),
    ("SALES_GROWTH", (r"\bspike", r"\bsudden", r"\bsurge", r"\bsales volume\b", r"\bgrowth\b")),
    ("ITEM_NOT_RECEIVED", (r"\bnot arrive", r"\bnever arrived\b", r"\bnot received\b", r"\bmissing package\b")),
    ("DELIVERY_EVIDENCE", (r"\btracking\b", r"\bdelivery proof\b", r"\bshipped\b", r"\bcarrier\b")),
    ("SELLER_PROTECTION", (r"\bseller protection\b", r"\bprotected\b", r"\beligib")),
    ("REFUND_REASONS", (r"\brefund", r"\bmoney back\b", r"\bcredit not\b")),
    ("DISPUTE_OVERVIEW", (r"\bdispute", r"\bchargeback", r"\bclaim")),
    ("INVOICING", (r"\binvoice", r"\bbill(?:s|ing)?\b")),
    ("SANDBOX_TESTING", (r"\bsandbox\b", r"\btest account")),
    ("COURT_ORDERS", (r"\bcourt\b", r"\blawsuit", r"\barbitration\b")),
    ("ACCEPTABLE_USE", (r"\ballowed\b", r"\bprohibited\b", r"\bbanned item", r"\bpolicy\b", r"\bacceptable\b")),
)
_COMPILED = tuple((label, tuple(re.compile(pattern) for pattern in patterns)) for label, patterns in _KEYWORDS)


def keyword_provider(request):
    """Deterministic chooser with no model: same contract as a model-backed chooser."""
    lowered = request["query"].casefold()
    for label, patterns in _COMPILED:
        if any(pattern.search(lowered) for pattern in patterns):
            return json.dumps({"route": label})
    return json.dumps({"route": OFF_TOPIC})
