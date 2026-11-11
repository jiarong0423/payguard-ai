"""Optional public hosted demo: refusing provider stubs and one exact public host.

``PAYGUARD_DEMO_MODE=public`` is off by default. When it is on, the application
replaces every provider adapter (PayPal Sandbox, Gemini worker) with
a stub that owns no HTTP client, no subprocess and no credential, and the routes
that would reach a provider answer 503 ``hosted_demo_disabled`` before any body
parsing (requests that fail the earlier host, origin or content-type checks are
refused there first). Only the synthetic fixtures, the local engines and the committed replays
remain. The hosted demo therefore needs no keys and holds none.

``PAYGUARD_PUBLIC_HOST`` is read only in that mode, and that mode refuses to start
without it. It names one exact hostname
(no scheme, port, path or wildcard); the matching ``https://`` origin is the only
origin it adds. With demo mode off neither variable changes anything.

Two opt-in switches widen the hosted demo, each fail-closed (an unrecognised value stops startup):
``PAYGUARD_HOSTED_READONLY_SANDBOX=enabled`` opens read-only Sandbox calls (OAuth, dispute list and detail) with
masked dispute ids; ``PAYGUARD_HOSTED_SANDBOX_SEND=enabled`` (owner decision 2026-11-10, Sandbox test account only)
additionally opens one write, ``POST /api/v1/paypal/disputes/provide-evidence``, behind every local send guard plus
hosted-only caps: one send per dispute, one per visitor session, and a process-wide window and daily limit.
"""

import asyncio
import collections
import contextvars
import os
import re
import threading
import time

from .ai_brief import AiBriefError
from .store import BoundaryError


DEMO_MODE_ENV = "PAYGUARD_DEMO_MODE"
PUBLIC_HOST_ENV = "PAYGUARD_PUBLIC_HOST"
# Opt-in, honoured only together with PAYGUARD_DEMO_MODE=public: the hosted page may make READ-ONLY Sandbox calls.
HOSTED_READONLY_ENV = "PAYGUARD_HOSTED_READONLY_SANDBOX"
HOSTED_READ_BUDGET_CODE = "hosted_read_budget_exceeded"
# Process-wide cap on every call the hosted demo sends to PayPal (OAuth connect, list, detail), all visitors together.
HOSTED_READS_PER_MINUTE = 20
HOSTED_READS_PER_DAY = 500
# The hosted page never shows a real dispute number: it shows a code (for example PP-R-BNP-XXXX7173). The code -> real
# number table lives only in server memory and keeps at most this many entries (oldest dropped first).
HOSTED_ID_MAP_LIMIT = 200
HOSTED_DEMO_CODE = "hosted_demo_disabled"
HOSTED_DEMO_MESSAGE = ("This capability is disabled in the hosted demo, which cannot send or change anything at a provider. "
                       "Run TradeGlot locally to use it.")
# Routes that would contact PayPal, Gemini or another provider. They answer 503 in public demo mode.
DISABLED_ROUTES = frozenset({
    ("POST", "/api/v1/paypal/connect"),
    ("POST", "/api/v1/paypal/invoices/draft"),
    ("POST", "/api/v1/paypal/disputes/provide-evidence"),
    ("POST", "/api/v1/paypal/disputes/add-tracking"),
    ("POST", "/api/v1/paypal/webhooks/verify"),
    ("POST", "/api/v1/ai/evidence-brief"),
    # AG Studio built-in agents: the hosted demo replays a recorded run and never calls a model.
    ("POST", "/api/v1/studio/agent-turn"),
})
# With the read-only Sandbox switch on, only the OAuth connect route opens; the other six stay disabled.
READONLY_OPEN_ROUTES = frozenset({("POST", "/api/v1/paypal/connect")})
# Opt-in on top of the read-only switch (owner decision 2026-11-10): the hosted page may send dispute evidence to the
# owner's own Sandbox test disputes. Only this one route opens; invoices, tracking, webhooks, AI brief and Studio stay 503.
HOSTED_SEND_ENV = "PAYGUARD_HOSTED_SANDBOX_SEND"
SEND_OPEN_ROUTES = frozenset({("POST", "/api/v1/paypal/disputes/provide-evidence")})
HOSTED_SEND_BUDGET_CODE = "hosted_send_budget_exceeded"
HOSTED_SEND_SESSION_CODE = "hosted_send_session_used"
# Process-wide caps on hosted evidence sends, all visitors together, plus one send per visitor session and per dispute.
HOSTED_SENDS_PER_WINDOW = 3
HOSTED_SEND_WINDOW_SECONDS = 600
HOSTED_SENDS_PER_DAY = 15
# (red team 2026-11-10 A1) One send per session alone let one address open new sessions and use up the whole Sandbox
# dispute stock (3 per window, 15 a day) in minutes. Each client key (the TrafficGate address, an IPv6 /64 counted once)
# may send at most this many in any 24 hours; the shared caps above still apply.
HOSTED_SENDS_PER_CLIENT_PER_DAY = 2
HOSTED_SEND_CLIENT_CODE = "hosted_send_client_used"
# The visitor session making the current send; set by the provide-evidence route only around a submit.
HOSTED_SEND_SESSION = contextvars.ContextVar("payguard_hosted_send_session", default=None)
# The client key of that visitor (TrafficGate's address key); set together with HOSTED_SEND_SESSION.
HOSTED_SEND_CLIENT = contextvars.ContextVar("payguard_hosted_send_client", default=None)
_LABEL = r"(?!-)[a-z0-9-]{1,63}(?<!-)"
_PUBLIC_HOST = re.compile(rf"(?=.{{1,253}}\Z){_LABEL}(?:\.{_LABEL})*\.[a-z](?:[a-z0-9-]{{0,61}}[a-z0-9])?\Z")


class DemoModeConfigError(RuntimeError):
    """Raised at startup for an unrecognised demo mode or public host value."""


def public_demo_enabled(environ=None) -> bool:
    value = (os.environ if environ is None else environ).get(DEMO_MODE_ENV, "")
    if value in ("", "off"):
        return False
    if value == "public":
        return True
    raise DemoModeConfigError("PAYGUARD_DEMO_MODE must be unset, 'off' or 'public'")


def hosted_readonly_enabled(environ=None) -> bool:
    """True only for HOSTED_READONLY=enabled while PAYGUARD_DEMO_MODE=public. Anything else is off.
    An unrecognised value with public mode on fails startup (fail closed)."""
    source = os.environ if environ is None else environ
    if not public_demo_enabled(source):
        return False
    value = source.get(HOSTED_READONLY_ENV, "")
    if value in ("", "off"):
        return False
    if value == "enabled":
        return True
    raise DemoModeConfigError("PAYGUARD_HOSTED_READONLY_SANDBOX must be unset, 'off' or 'enabled'")


def hosted_send_enabled(environ=None) -> bool:
    """True only for PAYGUARD_HOSTED_SANDBOX_SEND=enabled while public mode AND the read-only switch are on.
    Off without public mode. With public mode on, an unrecognised value, or 'enabled' without the read-only switch,
    fails startup (fail closed): the send is never on by accident or half-configured."""
    source = os.environ if environ is None else environ
    if not public_demo_enabled(source):
        return False
    value = source.get(HOSTED_SEND_ENV, "")
    if value in ("", "off"):
        return False
    if value != "enabled":
        raise DemoModeConfigError("PAYGUARD_HOSTED_SANDBOX_SEND must be unset, 'off' or 'enabled'")
    if not hosted_readonly_enabled(source):
        raise DemoModeConfigError("PAYGUARD_HOSTED_SANDBOX_SEND=enabled requires PAYGUARD_HOSTED_READONLY_SANDBOX=enabled")
    return True


def disabled_routes(readonly: bool = False, send: bool = False) -> frozenset:
    if not readonly:
        return DISABLED_ROUTES
    routes = DISABLED_ROUTES - READONLY_OPEN_ROUTES
    return routes - SEND_OPEN_ROUTES if send else routes


def public_host(environ=None) -> str | None:
    """The single exact public hostname, or None when unset. Invalid values fail startup."""
    value = (os.environ if environ is None else environ).get(PUBLIC_HOST_ENV, "")
    if value == "":
        return None
    if _PUBLIC_HOST.fullmatch(value) is None:
        raise DemoModeConfigError("PAYGUARD_PUBLIC_HOST must be one lowercase hostname without scheme, port or path")
    return value


def require_public_host(environ=None) -> str:
    """Public demo mode needs its exact host; unset or invalid stops startup (fail closed)."""
    host = public_host(environ)
    if host is None:
        raise DemoModeConfigError("PAYGUARD_DEMO_MODE=public requires PAYGUARD_PUBLIC_HOST (one exact lowercase hostname)")
    return host


def _refuse():
    raise BoundaryError(503, HOSTED_DEMO_CODE)


def _replace_everywhere(value, old: str, new: str):
    """Copy of a provider answer with every string that holds ``old`` rewritten, whatever the nesting."""
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, dict):
        return {_replace_everywhere(key, old, new): _replace_everywhere(item, old, new) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_replace_everywhere(item, old, new) for item in value]
    return value


class HostedDemoPaypalStub:
    """Stands in for PaypalAdapter. No transport, no config loader, no credentials.

    ``status`` reports ``not_configured`` so the Disputes readback serves the
    synthetic fixture; every provider operation refuses.
    """

    open_clients = 0

    def status(self) -> dict:
        return {"configured": False, "status": "not_configured", "environment": "sandbox",
                "source": "paypal_sandbox", "last_verified_at": None, "evidence_receipt": None}

    def dispute_submit_enabled(self) -> bool:
        return False

    def require_connected(self):
        _refuse()

    async def connect(self) -> dict:
        _refuse()

    async def create_invoice_draft(self, _payload: dict, _request_id: str) -> dict:
        _refuse()

    async def list_disputes(self, page_size: int = 10) -> list[dict]:
        _refuse()

    async def get_dispute(self, _dispute_id: str) -> dict:
        _refuse()

    async def provide_evidence(self, _dispute_id: str, _parts: dict) -> dict:
        _refuse()

    async def verify_webhook(self, _payload: dict) -> dict:
        _refuse()


class ReadBudget:
    """Rolling per-minute and per-day cap on provider reads, shared by every visitor of the process."""

    def __init__(self, per_minute: int = HOSTED_READS_PER_MINUTE, per_day: int = HOSTED_READS_PER_DAY, clock=time.monotonic):
        self.per_minute, self.per_day, self.clock = per_minute, per_day, clock
        self._stamps = collections.deque()
        self._lock = threading.Lock()

    def take(self) -> None:
        """Reserve one read before the call is made; answers 429 when either window is full."""
        with self._lock:
            now = self.clock()
            while self._stamps and now - self._stamps[0] >= 86400:
                self._stamps.popleft()
            if len(self._stamps) >= self.per_day:
                raise BoundaryError(429, HOSTED_READ_BUDGET_CODE,
                                    retry_after=max(1, int(86400 - (now - self._stamps[0])) + 1))
            recent = [stamp for stamp in self._stamps if now - stamp < 60]
            if len(recent) >= self.per_minute:
                raise BoundaryError(429, HOSTED_READ_BUDGET_CODE, retry_after=max(1, int(60 - (now - recent[0])) + 1))
            self._stamps.append(now)


class SendBudget:
    """Process-wide cap on hosted evidence sends: at most ``per_window`` in any ``window`` seconds and ``per_day`` in
    any 24 hours, all visitors together. A reserved send stays counted whatever the provider answers."""

    def __init__(self, per_window: int = HOSTED_SENDS_PER_WINDOW, window: int = HOSTED_SEND_WINDOW_SECONDS,
                 per_day: int = HOSTED_SENDS_PER_DAY, clock=time.monotonic):
        self.per_window, self.window, self.per_day, self.clock = per_window, window, per_day, clock
        self._stamps = collections.deque()

    def _prune(self, now):
        while self._stamps and now - self._stamps[0] >= 86400:
            self._stamps.popleft()

    def refusal(self):
        """None when one more send fits now, else the seconds until it would (the caller holds the adapter lock)."""
        now = self.clock()
        self._prune(now)
        if len(self._stamps) >= self.per_day:
            return max(1, int(86400 - (now - self._stamps[0])) + 1)
        recent = [stamp for stamp in self._stamps if now - stamp < self.window]
        if len(recent) >= self.per_window:
            return max(1, int(self.window - (now - recent[0])) + 1)
        return None

    def take(self) -> None:
        wait = self.refusal()
        if wait is not None:
            raise BoundaryError(429, HOSTED_SEND_BUDGET_CODE, retry_after=wait)
        self._stamps.append(self.clock())

    def left(self) -> dict:
        now = self.clock()
        self._prune(now)
        recent = sum(1 for stamp in self._stamps if now - stamp < self.window)
        return {"window": max(0, self.per_window - recent), "day": max(0, self.per_day - len(self._stamps))}


class HostedReadOnlyPaypalAdapter:
    """Hosted demo with real READ-ONLY Sandbox calls. Wraps a real PaypalAdapter but exposes only
    status, require_connected, connect (OAuth token), list_disputes and get_dispute (GET). Every other
    provider action refuses before any transport is reached. There is deliberately no ``__getattr__``.

    With ``send_enabled`` (PAYGUARD_HOSTED_SANDBOX_SEND=enabled, owner decision 2026-11-10) one write is added:
    provide_evidence, to a dispute this process listed under a masked code, at most once per dispute and once per
    visitor session, within the SendBudget, and only while the inner adapter's own submit flag
    (PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled) and merchant id are set. Every local guard in DisputeReadbackService
    (two human steps, account check, fresh PayPal read) still runs before this method is reached."""

    def __init__(self, inner, budget: ReadBudget | None = None, *, send_enabled: bool = False,
                 send_budget: SendBudget | None = None):
        self._inner = inner
        self._budget = budget if budget is not None else ReadBudget()
        self._connect_lock = asyncio.Lock()
        self._real_by_code = collections.OrderedDict()
        self._code_by_real = {}
        self._send_enabled = send_enabled is True
        self._send_budget = send_budget if send_budget is not None else SendBudget()
        self._send_lock = threading.Lock()
        # Real dispute numbers that already received a hosted send, and visitor sessions that already sent one.
        # Server memory only; kept for the life of the process (never trimmed, so a dispute is never sent to twice).
        self._sent_disputes = set()
        self._sent_sessions = set()
        # Send times per client key (24-hour window, send budget clock); bounded by the shared daily cap.
        self._sent_clients = {}

    def _code_for(self, real: str) -> str:
        """The public code of a real dispute number: same prefix, the number masked except its last four characters.
        Stable for one number, unique across numbers (a counter is added on a clash), never equal to a real number."""
        code = self._code_by_real.get(real)
        if code is not None:
            self._real_by_code.move_to_end(code)
            return code
        head, separator, tail = real.rpartition("-")
        base = f"{head}{separator}XXXX{tail[-4:]}"
        code, counter = base, 1
        while code in self._real_by_code or code == real:
            counter += 1
            code = f"{base}-{counter}"
        self._real_by_code[code] = real
        self._code_by_real[real] = code
        while len(self._real_by_code) > HOSTED_ID_MAP_LIMIT:
            _old_code, old_real = self._real_by_code.popitem(last=False)
            del self._code_by_real[old_real]
        return code

    def _token_seconds_left(self) -> float:
        try:
            return (self._inner._token_expiry - self._inner._now()).total_seconds()
        except Exception:
            return 0.0

    def _still_connected(self):
        """The current status when the shared connection holds a token with more than 60 s left, else None."""
        try:
            current = self._inner.status()
        except BoundaryError:
            return None
        return current if current.get("status") == "connected" and self._token_seconds_left() > 60 else None

    @property
    def last_debug_id(self):
        return getattr(self._inner, "last_debug_id", None)

    @property
    def open_clients(self):
        return getattr(self._inner, "open_clients", 0)

    def status(self) -> dict:
        return self._inner.status()

    def require_connected(self):
        return self._inner.require_connected()

    def dispute_submit_enabled(self) -> bool:
        return self._send_enabled and self._inner.dispute_submit_enabled() is True

    def tracking_submit_enabled(self) -> bool:
        return False

    def account_merchant_id(self):
        # Without the send switch no account id is known, so the local account check refuses every send.
        return self._inner.account_merchant_id() if self._send_enabled else None

    def send_state(self) -> dict | None:
        """Hosted send status for the console: None with the send switch off; else what is left of the process caps.
        Counts only, never an id."""
        if not self._send_enabled:
            return None
        with self._send_lock:
            left = self._send_budget.left()
            return {"sends_left_window": left["window"], "sends_left_day": left["day"],
                    "window_minutes": self._send_budget.window // 60, "disputes_sent": len(self._sent_disputes)}

    async def connect(self) -> dict:
        # A repeated Connect neither revokes the shared connection nor spends budget while its token is still good.
        # A reconnect that fails (token nearly expired) leaves the inner adapter in its fail-closed state for everyone
        # until the next successful Connect; that is the existing adapter behaviour and is documented here, not hidden.
        async with self._connect_lock:
            current = self._still_connected()
            if current is not None:
                return current
            self._budget.take()
            return await self._inner.connect()

    async def list_disputes(self, page_size: int = 10) -> list[dict]:
        self._budget.take()
        rows = await self._inner.list_disputes(page_size)
        return [dict(row, dispute_id=self._code_for(row["dispute_id"])) for row in rows]

    async def get_dispute(self, dispute_id: str) -> dict:
        # Only a code this process handed out is accepted; a real number (or any other string) is "not found" and
        # never reaches PayPal or the read budget.
        real = self._real_by_code.get(dispute_id)
        if real is None:
            raise BoundaryError(404, "dispute_not_found")
        self._budget.take()
        detail = await self._inner.get_dispute(real)
        masked = _replace_everywhere(detail, real, self._code_for(real))
        masked["dispute_id"] = self._code_for(real)
        return masked

    async def create_invoice_draft(self, _payload: dict, _request_id: str) -> dict:
        _refuse()

    async def provide_evidence(self, dispute_id: str, parts: dict) -> dict:
        """One hosted evidence send. Refuses (before any transport) with the switch off, outside a visitor send, for a
        code this process did not hand out, a dispute already sent to, a session that already sent, or a full cap.
        The dispute and the session are marked used and the cap is spent before the provider call: a failed send
        is never retried automatically."""
        session_id = HOSTED_SEND_SESSION.get()
        client = HOSTED_SEND_CLIENT.get()
        if (not self._send_enabled or not isinstance(session_id, str) or not session_id
                or not isinstance(client, str) or not client):
            _refuse()
        real = self._real_by_code.get(dispute_id)
        if real is None:
            raise BoundaryError(404, "dispute_not_found")
        with self._send_lock:
            if real in self._sent_disputes:
                raise BoundaryError(409, "evidence_already_submitted")
            if session_id in self._sent_sessions:
                raise BoundaryError(409, HOSTED_SEND_SESSION_CODE)
            now = self._send_budget.clock()
            for key in [key for key, stamps in self._sent_clients.items() if all(now - stamp >= 86400 for stamp in stamps)]:
                del self._sent_clients[key]
            mine = [stamp for stamp in self._sent_clients.get(client, []) if now - stamp < 86400]
            if len(mine) >= HOSTED_SENDS_PER_CLIENT_PER_DAY:
                raise BoundaryError(409, HOSTED_SEND_CLIENT_CODE)
            self._send_budget.take()
            self._sent_disputes.add(real)
            self._sent_sessions.add(session_id)
            self._sent_clients[client] = mine + [now]
        sent = await self._inner.provide_evidence(real, parts)
        sent = _replace_everywhere(sent if type(sent) is dict else {}, real, self._code_for(real))
        sent["dispute_id"] = self._code_for(real)
        return sent

    async def add_tracking(self, _tracker: dict) -> dict:
        _refuse()

    async def verify_webhook(self, _payload) -> dict:
        _refuse()


class HostedDemoBriefStub:
    """Stands in for the Gemini brief adapter. Never starts a worker or a client."""

    def validate_attempt_configuration(self) -> None:
        raise AiBriefError(503, HOSTED_DEMO_CODE)

    async def generate(self, _request):
        raise AiBriefError(503, HOSTED_DEMO_CODE)


class HostedDemoGuardMiddleware:
    """Answer 503 for provider routes before routing, schema checks or session work."""

    def __init__(self, app, *, error_response, routes=DISABLED_ROUTES):
        self.app = app
        self.error_response = error_response
        self.routes = frozenset(routes)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            # Starlette's route regex also matches before a trailing newline, so a path with a control character or
            # whitespace (%0A, %0D, %09, %20, ...) is refused outright instead of being compared to the table.
            if (any(ord(char) < 32 or ord(char) == 127 or char.isspace() for char in path)
                    or (scope["method"], path.rstrip("/\r\n") or "/") in self.routes):
                return await self.error_response(503, HOSTED_DEMO_CODE)(scope, receive, send)
        return await self.app(scope, receive, send)
