"""Optional public hosted demo: refusing provider stubs and one exact public host.

``PAYGUARD_DEMO_MODE=public`` is off by default. When it is on, the application
replaces every provider adapter (PayPal Sandbox, Gemini worker, LM Studio) with
a stub that owns no HTTP client, no subprocess and no credential, and the routes
that would reach a provider answer 503 ``hosted_demo_disabled`` before any body
parsing (requests that fail the earlier host, origin or content-type checks are
refused there first). Only the synthetic fixtures, the local engines and the committed replays
remain. The hosted demo therefore needs no keys and holds none.

``PAYGUARD_PUBLIC_HOST`` is read only in that mode, and that mode refuses to start
without it. It names one exact hostname
(no scheme, port, path or wildcard); the matching ``https://`` origin is the only
origin it adds. With demo mode off neither variable changes anything.
"""

import asyncio
import collections
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
# No daily cap. PayPal does not publish exact rate limits (developer.paypal.com/api/rate-limiting); a 429 from PayPal can
# follow traffic spikes, so a modest per-minute guard remains so that a burst of visitors cannot flood the Sandbox.
HOSTED_READS_PER_MINUTE = 40
HOSTED_READS_PER_DAY = None
# The hosted page never shows a real dispute number: it shows a code (for example PP-R-BNP-XXXX7173). The code -> real
# number table lives only in server memory and keeps at most this many entries (oldest dropped first).
HOSTED_ID_MAP_LIMIT = 200
HOSTED_DEMO_CODE = "hosted_demo_disabled"
HOSTED_DEMO_MESSAGE = ("This capability is disabled in the hosted demo, which cannot send or change anything at a provider. "
                       "Run TradeGlot locally to use it.")
# Routes that would contact PayPal, Gemini or a local model. They answer 503 in public demo mode.
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


def disabled_routes(readonly: bool = False) -> frozenset:
    return DISABLED_ROUTES - READONLY_OPEN_ROUTES if readonly else DISABLED_ROUTES


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

    def __init__(self, per_minute: int = HOSTED_READS_PER_MINUTE, per_day: int | None = HOSTED_READS_PER_DAY, clock=time.monotonic):
        self.per_minute, self.per_day, self.clock = per_minute, per_day, clock
        self._stamps = collections.deque()
        self._lock = threading.Lock()

    def take(self) -> None:
        """Reserve one read before the call is made; answers 429 when either window is full."""
        with self._lock:
            now = self.clock()
            keep = 86400 if self.per_day is not None else 60
            while self._stamps and now - self._stamps[0] >= keep:
                self._stamps.popleft()
            if self.per_day is not None and len(self._stamps) >= self.per_day:
                raise BoundaryError(429, HOSTED_READ_BUDGET_CODE,
                                    retry_after=max(1, int(86400 - (now - self._stamps[0])) + 1))
            recent = [stamp for stamp in self._stamps if now - stamp < 60]
            if len(recent) >= self.per_minute:
                raise BoundaryError(429, HOSTED_READ_BUDGET_CODE, retry_after=max(1, int(60 - (now - recent[0])) + 1))
            self._stamps.append(now)


class HostedReadOnlyPaypalAdapter:
    """Hosted demo with real READ-ONLY Sandbox calls. Wraps a real PaypalAdapter but exposes only
    status, require_connected, connect (OAuth token), list_disputes and get_dispute (GET). Every other
    provider action refuses before any transport is reached. There is deliberately no ``__getattr__``."""

    def __init__(self, inner, budget: ReadBudget | None = None):
        self._inner = inner
        self._budget = budget if budget is not None else ReadBudget()
        self._connect_lock = asyncio.Lock()
        self._real_by_code = collections.OrderedDict()
        self._code_by_real = {}

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
        return False

    def tracking_submit_enabled(self) -> bool:
        return False

    def account_merchant_id(self):
        return None

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

    async def provide_evidence(self, _dispute_id: str, _parts: dict) -> dict:
        _refuse()

    async def add_tracking(self, _tracker: dict) -> dict:
        _refuse()

    async def verify_webhook(self, _payload) -> dict:
        _refuse()


class HostedDemoBriefStub:
    """Stands in for the Gemini and LM Studio brief adapters. Never starts a worker or a client."""

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
