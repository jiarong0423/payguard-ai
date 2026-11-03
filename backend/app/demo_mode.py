"""Optional public hosted demo: refusing provider stubs and one exact public host.

``PAYGUARD_DEMO_MODE=public`` is off by default. When it is on, the application
replaces every provider adapter (PayPal Sandbox, Gemini worker, LM Studio) with
a stub that owns no HTTP client, no subprocess and no credential, and the routes
that would reach a provider answer 503 ``hosted_demo_disabled`` before any body
parsing. Only the synthetic fixtures, the local engines and the committed replays
remain. The hosted demo therefore needs no keys and holds none.

``PAYGUARD_PUBLIC_HOST`` is read only in that mode, and that mode refuses to start
without it. It names one exact hostname
(no scheme, port, path or wildcard); the matching ``https://`` origin is the only
origin it adds. With demo mode off neither variable changes anything.
"""

import os
import re

from .ai_brief import AiBriefError
from .store import BoundaryError


DEMO_MODE_ENV = "PAYGUARD_DEMO_MODE"
PUBLIC_HOST_ENV = "PAYGUARD_PUBLIC_HOST"
HOSTED_DEMO_CODE = "hosted_demo_disabled"
HOSTED_DEMO_MESSAGE = ("This capability is disabled in the hosted demo, which makes no provider calls. "
                       "Run PayGuard locally to use it.")
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


class HostedDemoBriefStub:
    """Stands in for the Gemini and LM Studio brief adapters. Never starts a worker or a client."""

    def validate_attempt_configuration(self) -> None:
        raise AiBriefError(503, HOSTED_DEMO_CODE)

    async def generate(self, _request):
        raise AiBriefError(503, HOSTED_DEMO_CODE)


class HostedDemoGuardMiddleware:
    """Answer 503 for provider routes before routing, schema checks or session work."""

    def __init__(self, app, *, error_response):
        self.app = app
        self.error_response = error_response

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and (scope["method"], scope["path"].rstrip("/") or "/") in DISABLED_ROUTES:
            return await self.error_response(503, HOSTED_DEMO_CODE)(scope, receive, send)
        return await self.app(scope, receive, send)
