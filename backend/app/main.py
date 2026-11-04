"""Loopback-only FastAPI application with explicit synthetic session boundaries."""

import asyncio
from decimal import Decimal, InvalidOperation
import hashlib
import importlib
import ipaddress
import json
import math
import os
import re
from pathlib import Path, PurePosixPath
import time

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.routing import Match, Mount
from pydantic import ValidationError

from payguard.engines import check_aup
from payguard.retrieval import RetrievalError, load_corpus
from payguard import applicability, advisory_eval
from payguard.applicability import ApplicabilityError, assess_applicability
from payguard.advisory_eval import AdvisoryError, evaluate_advisory

from .paypal import PaypalAdapter, provider_error_extra
from .paypal_tools import SafePaypalToolGateway
from .paypal_disputes import DisputeAmountMismatch, DisputeReadbackService
from .ai_brief import AiBriefError, AiBriefHttpRequest, AiBriefResponse, EvidenceBriefAdapter
from .ai_usage import COST_NOTE, PRICE_TABLE_SOURCE, AiUsageLog, AiUsageResponse
from .lmstudio_brief import LmStudioConfig, LmStudioEvidenceBriefAdapter
from .demo_mode import (HOSTED_DEMO_CODE, HOSTED_DEMO_MESSAGE, HostedDemoBriefStub, HostedDemoGuardMiddleware,
                        HostedDemoPaypalStub, public_demo_enabled, require_public_host)
from .channel3 import build_channel3_adapter
from .channel3_products import build_channel3_product_adapter, card_digest
from .case_routing import CaseRouter
from .studio_agent import MAX_TURN_BODY_BYTES, StudioAgentError, StudioAgentService, configured_studio_model
from .schemas import (CaseRouteRequest, CaseRouteResponse, ProductConfirmRequest, ProductConfirmResponse, ProductReferenceRequest, ProductReferenceResponse,
                      ApproveRequest, AupRequest, AupResponse, AupAcknowledgeRequest, AupAcknowledgeResponse, DisputeApprovalResponse,
                      AupCategorySignalRequest, AupCategorySignalResponse,
                      DisputeDraftResponse, EmptyRequest, HealthResponse, ConnectionsResponse, InjectRequest,
                      InvoiceDraftRequest, InvoiceDraftResponse, InvoiceReviewRequest,
                      InvoiceReviewResponse, PaypalStatusResponse, SessionResponse,
                      DisputeDetailResponse, DisputeListResponse, ProvideEvidenceRequest, ProvideEvidenceResponse,
                      AddTrackingRequest, AddTrackingResponse, INVOICE_WHOLE_UNITS_ERROR,
                      StateResponse, WebhookVerifyResponse,
                      ReferenceRequest, ReferenceResponse, PolicyRequest,
                      AdvisoryRequest, PolicyAssessmentResponse, AdvisoryEvaluationResponse)
from .store import AiAttemptBudget, BoundaryError, SessionStore
from .traffic import TrafficGate
PROCESS_AI_ATTEMPT_BUDGET = AiAttemptBudget()

ALLOWED_HOSTS = frozenset({"localhost:8000", "127.0.0.1:8000", "[::1]:8000"})
ALLOWED_ORIGINS = frozenset({"http://localhost:5173", "http://127.0.0.1:5173",
                             "http://localhost:8000", "http://127.0.0.1:8000"})
MAX_BODY_BYTES = 16384
STUDIO_TURN_PATH = "/api/v1/studio/agent-turn"
# One route may carry more: an AG Studio agent turn holds Studio's own instructions and tool schemas (about
# 20-45 KB measured). It is session, CSRF and Governor bound, local live mode only, and disabled in the hosted demo.
ROUTE_BODY_LIMITS = {STUDIO_TURN_PATH: MAX_TURN_BODY_BYTES}
SENSITIVE_HEADERS = frozenset({b"host", b"origin", b"x-demo-session", b"x-csrf-token", b"content-length", b"content-type"})
# A new-session request waits at most this long in the queue before it is refused with Retry-After.
SESSION_QUEUE_SECONDS = 8

_MESSAGES = {
    401: "A valid demo session is required.",
    403: "The request failed a local security boundary.",
    404: "The requested demo resource was not found.",
    405: "This operation is unavailable.",
    413: "The request exceeds the allowed body size.",
    415: "JSON content is required.",
    422: "The request does not match the accepted contract.",
    429: "The local request or sample limit was reached.",
    500: "The local service could not complete the request.",
    502: "The Sandbox provider response could not be verified.",
    503: "The requested Sandbox capability is unavailable.",
}


# (r25 owner request) Input characters and numbers are locked in the shared JSON parse, for every route, before any
# handler runs. Numbers: plain digits with an optional decimal point only, at most 15 integer and 6 fraction digits
# (no exponent, leading +, NaN or Infinity; so no value can overflow to inf). Strings and object keys: no control
# characters other than tab, newline and carriage return, no bidi override or isolate, no zero-width characters and
# no lone surrogates.
INPUT_REFUSED_CODE = "input_characters_refused"
INPUT_REFUSED_MESSAGE = ("The request contains characters or a number format PayGuard does not accept (control, "
                         "invisible or direction-changing characters, or numbers written in exponent form). Remove them and "
                         "try again.")
_PLAIN_NUMBER = re.compile(r"-?(?:0|[1-9][0-9]{0,14})(?:\.[0-9]{1,6})?")
_REFUSED_CHARACTERS = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069"
                                 "\u200b-\u200d\u2060\ufeff\ud800-\udfff]")


class InputRefused(ValueError):
    """A JSON body value outside the locked character and number rules."""


def _plain_number(text: str):
    if _PLAIN_NUMBER.fullmatch(text) is None:
        raise InputRefused("number")
    return float(text) if "." in text else int(text)


def _refuse_number_constant(_text):
    raise InputRefused("nonfinite")


def _checked_text(value: str) -> str:
    if _REFUSED_CHARACTERS.search(value):
        raise InputRefused("characters")
    return value


def _number_syntax_refused(text: str, position: int) -> bool:
    """True when a JSON syntax error sits on a number form outside the plain rule (+5, 0x10, .5, 1., 012)."""
    current, previous = text[position:position + 1], text[position - 1:position] if position else ""
    return (current in ("+", ".") or text.startswith(("NaN", "Infinity"), position) or
            (previous.isdigit() and current.isalnum()) or (previous == "." and not current.isdigit()))


def parse_locked_json(text: str):
    """json.loads with duplicate keys refused (ValueError) and the r25 input lock (InputRefused)."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            _checked_text(key)
            if type(value) is str:
                _checked_text(value)
            if key in result:
                raise ValueError("duplicate")
            result[key] = value
        return result

    try:
        parsed = json.loads(text, object_pairs_hook=unique_object, parse_constant=_refuse_number_constant,
                            parse_float=_plain_number, parse_int=_plain_number)
    except json.JSONDecodeError as error:
        if _number_syntax_refused(error.doc, error.pos):
            raise InputRefused("number") from None
        raise
    # Strings inside arrays (object values and keys were checked above).
    pending = [parsed]
    while pending:
        value = pending.pop()
        if type(value) is list:
            for item in value:
                if type(item) is str:
                    _checked_text(item)
                elif type(item) in (list, dict):
                    pending.append(item)
        elif type(value) is dict:
            pending.extend(item for item in value.values() if type(item) in (list, dict))
        elif type(value) is str:
            _checked_text(value)
    return parsed


# Evidence pairing (review r7b): say why, so the seller can pick the right case instead of retrying.
DISPUTE_PAIRING_MESSAGES = {
    "dispute_case_mismatch": "This dispute does not match the selected case (reason or amount differ). Select the case it belongs to.",
    "dispute_case_bound": "This dispute is already paired with another case in this session. Evidence is never mixed between cases.",
    "country_rules_blocked": "PayGuard won't create the draft: a country rule stops this sale. Change the goods, account or countries and check again.",
    "country_check_changed": "The country check changed after this draft was reviewed; review the draft again.",
    # The seller needs the cause, not a generic "changed" (r22: a TWD check then a USD invoice looked unexplained).
    "country_amount_changed": "The country check used a different amount or currency than this invoice. Check country rules again with the invoice amount in USD, or leave the amount empty.",
    # (attack r22) The guide's form saves are capped per demo session.
    "guide_form_limit": "This guide reached its limit of form saves for this demo session. Start a new demo session to continue.",
    # One submit per approval (red team r20); the seller needs a plain sentence, not the generic contract error.
    "evidence_already_submitted": "This evidence was already sent for this approval. Reset the demo and review the case again to send a new version.",
    # PayPal docs r24 (customer-disputes/v1): checked on a fresh read of the dispute right before any send.
    "dispute_not_awaiting_seller": "PayPal is not waiting for the seller's response on this dispute, so evidence cannot be sent now. Nothing was sent.",
    "dispute_evidence_not_offered": "PayPal does not offer evidence submission on this dispute right now. Nothing was sent.",
    "dispute_amount_mismatch": "The dispute amount in PayPal differs from the selected case's amount. Nothing was sent.",
    # (r35 #2, E1 P1-1) Read at preview from the session's last detail read: no confirmation, no pair.
    "seller_evidence_already_submitted": "PayPal already has seller evidence for this dispute, so PayGuard will not send more. Nothing was sent.",
    # (r25 R3 P1-1) Only proof of fulfillment with tracking is shaped; refund ids are never invented.
    "evidence_type_not_supported": "PayPal asks for an evidence type PayGuard cannot send yet (only proof of fulfillment with tracking is supported). Respond to this dispute in PayPal directly. Nothing was sent.",
    # (r25 send guard) The fresh read's disputed_transactions[].seller.merchant_id must be the connected account.
    "dispute_not_this_account": "This dispute belongs to a different PayPal account than the connected Sandbox account. Nothing was sent.",
    "account_identity_unknown": "PayGuard cannot confirm which PayPal Sandbox account is connected (set PAYGUARD_PAYPAL_SANDBOX_MERCHANT_ID), so it will not send. Nothing was sent.",
    "dispute_evidence_incomplete": "PayPal asks for evidence this draft does not cover. Add the missing evidence and review the case again. Nothing was sent.",
    "evidence_not_ready": "This case has no evidence PayPal would accept yet (proof of fulfillment needs a tracking number). Nothing was sent.",
    "evidence_file_rejected": "An attachment is not accepted by PayPal: use JPG, GIF, PNG or PDF files under 10 MB each and 50 MB in total.",
    "tracking_not_applicable": "Tracking is added only for an item-not-received case. Nothing was sent.",
    "dispute_detail_required": "Open this dispute's details first; PayPal must show exactly one disputed transaction to add tracking to. Nothing was sent.",
    # (optimise r24) The payload built for the send must be the one the local approval recorded.
    "evidence_changed_after_approval": "The evidence changed after you approved it; review it again. Nothing was sent.",
    "tracking_already_submitted": "Tracking was already sent for this approval. Reset the demo and review the case again to send it again.",
    # (r30 J2 P2-1) The server-side send confirmation issued by the latest preview.
    "confirmation_required": "Open the send dialog and confirm there; a send needs the confirmation from the latest preview. Nothing was sent.",
    "confirmation_invalid": "This confirmation is used, replaced by a newer preview, or does not match what would be sent. Prepare the preview again. Nothing was sent.",
    "confirmation_too_early": "Wait for the send button to unlock, then send. Nothing was sent.",
    # PayPal docs r24 (currency-codes): these currencies have no decimals.
    INVOICE_WHOLE_UNITS_ERROR: "TWD, JPY and HUF invoices take whole amounts only, for example 1500 rather than 1500.00.",
}
STUDIO_MESSAGES = {
    "studio_agents_off": "Studio's built-in agents are off: no model is configured for this console.",
    "studio_turn_invalid": "The agent turn does not match the accepted contract.",
    "studio_turn_personal_data": "The agent turn looks like it contains personal data (an email address, phone or card number); ask about the dashboard only.",
    "studio_agent_limit": "The agent call limit for this session was reached.",
    "studio_agent_unavailable": "The model is paused after repeated failures; try again later.",
    "studio_agent_timeout": "The model did not answer in time.",
    "studio_agent_reply_refused": "The model answered, but the reply failed the console's checks and was not shown.",
}


def _country_amount_matches(latest: dict, amount, currency) -> bool:
    """(attack r22) True when the latest country check carried no amount, or the same amount and currency as the invoice."""
    checked_amount, checked_currency = latest.get("amount"), latest.get("currency")
    if checked_amount is None and checked_currency is None:
        return True
    if checked_currency is not None and checked_currency != currency:
        return False
    if checked_amount is None:
        return True
    try:
        return amount is not None and Decimal(checked_amount) == Decimal(amount)
    except (InvalidOperation, TypeError, ValueError):
        return False


def error_response(status: int, code: str, retry_after: int | None = None, *, extra: dict | None = None):
    if code == "aup_capacity":
        # (attack r21) The page showed only "try again"; say when (the limit is unchanged).
        message = ("Five policy checks are already open in the last two minutes. "
                   + (f"Try again in {retry_after} second{'' if retry_after == 1 else 's'}."
                      if retry_after else "Try again in about two minutes."))
    elif code == HOSTED_DEMO_CODE:
        message = HOSTED_DEMO_MESSAGE
    elif code == INPUT_REFUSED_CODE:
        message = INPUT_REFUSED_MESSAGE
    elif code.startswith("ai_"):
        message = "The AI evidence brief is unavailable or could not be verified."
    elif code == "reference_unavailable":
        message = "The local public reference corpus is unavailable."
    elif code in DISPUTE_PAIRING_MESSAGES:
        message = DISPUTE_PAIRING_MESSAGES[code]
    elif code.startswith("studio_"):
        message = STUDIO_MESSAGES.get(code, "The dashboard agents are unavailable or their reply could not be verified.")
    else:
        message = _MESSAGES.get(status, "The request could not be completed.")
    headers = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}
    if retry_after:
        headers["Retry-After"] = str(retry_after)
    # (evloop) extra: only paypal.provider_error_extra's closed fields (paypal_issue, paypal_debug_id).
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message, **(extra or {})}},
                        headers=headers)


class LocalBoundaryMiddleware:
    """Validate transport identity and bounded bodies before HTTP parsing.

    With no ``public_host`` (the default, and always when demo mode is off) only loopback
    clients with the loopback Host/Origin values pass. A ``public_host`` adds exactly one
    Host and its https Origin, and admits a non-loopback client only when the request names
    that Host and carries the forwarding headers the hosting proxy sets.
    """
    def __init__(self, app, *, public_host=None):
        self.app = app
        self.public_host = public_host
        if public_host is None:
            self.allowed_hosts = ALLOWED_HOSTS
            self.allowed_origins = ALLOWED_ORIGINS
            self.sensitive = SENSITIVE_HEADERS
        else:
            self.allowed_hosts = ALLOWED_HOSTS | {public_host}
            self.allowed_origins = ALLOWED_ORIGINS | {"https://" + public_host}
            # (r25 R5 P2-2) A request that names the public Host (the hosted proxied mode) accepts only its https
            # Origin, never the loopback origins; a loopback client naming a loopback Host keeps the local origins.
            self.public_origins = frozenset({"https://" + public_host})
            self.sensitive = SENSITIVE_HEADERS | {b"x-forwarded-proto", b"x-forwarded-for"}

    def _proxied_public_request(self, header) -> bool:
        return (self.public_host is not None and header.get(b"host", "").lower() == self.public_host and
                header.get(b"x-forwarded-proto") == "https" and bool(header.get(b"x-forwarded-for", "").strip()))

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = scope.get("headers", [])
        for name in self.sensitive:
            if sum(key.lower() == name for key, _ in headers) > 1:
                return await error_response(403, "duplicate_security_header")(scope, receive, send)
        header = {key.lower(): value.decode("latin-1") for key, value in headers}
        try:
            loopback = ipaddress.ip_address(scope.get("client", ("", 0))[0]).is_loopback
        except (ValueError, TypeError, IndexError):
            loopback = False
        if not loopback:
            loopback = self._proxied_public_request(header)
        if not loopback or header.get(b"host", "").lower() not in self.allowed_hosts:
            return await error_response(403, "host_rejected")(scope, receive, send)
        origin = header.get(b"origin")
        allowed_origins = self.allowed_origins
        if self.public_host is not None:
            allowed_origins = (self.public_origins if header.get(b"host", "").lower() == self.public_host
                               else ALLOWED_ORIGINS)
        if origin is not None and origin not in allowed_origins:
            return await error_response(403, "origin_rejected")(scope, receive, send)
        method = scope["method"]
        if method in ("POST", "PUT", "PATCH", "DELETE") and origin not in allowed_origins:
            return await error_response(403, "origin_required")(scope, receive, send)
        if method == "OPTIONS":
            requested_method = header.get(b"access-control-request-method", "")
            requested_headers = {item.strip().lower() for item in header.get(b"access-control-request-headers", "").split(",") if item.strip()}
            if (origin not in allowed_origins or requested_method not in ("GET", "POST") or
                    requested_headers - {"content-type", "x-demo-session", "x-csrf-token"}):
                return await error_response(403, "cors_rejected")(scope, receive, send)
            response = JSONResponse(content={}, headers={"Access-Control-Allow-Origin": origin,
                                    "Access-Control-Allow-Methods": "GET, POST",
                                    "Access-Control-Allow-Headers": "Content-Type, X-Demo-Session, X-CSRF-Token",
                                    "Vary": "Origin", "Cache-Control": "no-store"})
            return await response(scope, receive, send)
        try:
            declared = int(header.get(b"content-length", "0"))
        except ValueError:
            return await error_response(422, "invalid_body")(scope, receive, send)
        body_limit = ROUTE_BODY_LIMITS.get(scope["path"], MAX_BODY_BYTES) if method == "POST" else MAX_BODY_BYTES
        if declared < 0 or declared > body_limit:
            return await error_response(413, "body_limit")(scope, receive, send)
        chunks = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            if message["type"] != "http.request":
                continue
            chunks.extend(message.get("body", b""))
            if len(chunks) > body_limit:
                return await error_response(413, "body_limit")(scope, receive, send)
            if not message.get("more_body", False):
                break
        if method == "POST":
            if header.get(b"content-type", "").split(";", 1)[0].strip().lower() != "application/json":
                return await error_response(415, "json_required")(scope, receive, send)
            # Reject duplicate keys, refused characters and every number outside the plain rule (r25: 1e400 overflowed
            # to inf without passing through parse_constant) before Pydantic can normalize them.
            try:
                # Strict UTF-8: json.loads on bytes would also accept UTF-16/32 bodies (RFC 8259 section 8.1).
                parsed = parse_locked_json(bytes(chunks).decode("utf-8"))
                if not isinstance(parsed, dict):
                    raise ValueError("object_required")
            except InputRefused:
                return await error_response(422, INPUT_REFUSED_CODE)(scope, receive, send)
            except (ValueError, UnicodeDecodeError, RecursionError):
                # (r25 R5 P2-1) The Studio turn keeps its own closed error code for a body it cannot accept.
                code = "studio_turn_invalid" if scope["path"] == STUDIO_TURN_PATH else "invalid_json"
                return await error_response(422, code)(scope, receive, send)
        delivered = False
        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(chunks), "more_body": False}
            return await receive()
        async def safe_send(message):
            if message["type"] == "http.response.start":
                response_headers = list(message.get("headers", []))
                response_headers.extend([(b"cache-control", b"no-store"), (b"x-content-type-options", b"nosniff"),
                                         (b"referrer-policy", b"no-referrer")])
                # No other site may frame these pages, so the gated Connect and Submit buttons cannot be overlaid
                # (red team r20 D5). 'self', not 'none': the scenarios page reads the licence line from a hidden
                # same-origin frame of /dashboard.html (frontend/src/scenarios/main.jsx readLicence), which 'none' would
                # break. Only frame-ancestors is set, so the console's own scripts, styles and fetches are unchanged.
                # X-Frame-Options covers browsers without CSP level 2.
                response_headers.extend([(b"content-security-policy", b"frame-ancestors 'self'"),
                                         (b"x-frame-options", b"SAMEORIGIN")])
                if origin in allowed_origins:
                    response_headers.extend([(b"access-control-allow-origin", origin.encode()), (b"vary", b"Origin")])
                message["headers"] = response_headers
            await send(message)
        await self.app(scope, replay, safe_send)


# Explicit types for the console's own files, so the answer does not depend on the host's mimetypes
# table (Windows can map .js to text/plain). Every response carries nosniff, so a wrong type would
# block the scripts, the web manifest and the service worker.
CONSOLE_CONTENT_TYPES = {
    ".js": b"text/javascript; charset=utf-8",
    ".css": b"text/css; charset=utf-8",
    ".webmanifest": b"application/manifest+json",
    ".png": b"image/png",
    ".svg": b"image/svg+xml",
}


class ConsoleStatic:
    """Serve the built console for GET/HEAD page requests only.

    API paths and non-GET methods keep the answers the API gave before the mount existed: 405 when a
    route exists for the path with another method, otherwise the JSON 404. Successful file answers for
    the suffixes in CONSOLE_CONTENT_TYPES carry that fixed content type.
    """

    def __init__(self, directory: str, routes):
        self.files = StaticFiles(directory=directory, html=True)
        self.routes = routes

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and (scope["method"] not in ("GET", "HEAD") or scope["path"].startswith("/api/")):
            partial = any(not isinstance(route, Mount) and route.matches(scope)[0] is Match.PARTIAL for route in self.routes)
            return await error_response(405 if partial else 404, "route_unavailable")(scope, receive, send)
        content_type = CONSOLE_CONTENT_TYPES.get(PurePosixPath(scope.get("path", "")).suffix.lower()) if scope["type"] == "http" else None
        if content_type is None:
            return await self.files(scope, receive, send)

        async def typed_send(message):
            if message["type"] == "http.response.start" and message["status"] == 200:
                headers = [(key, value) for key, value in message.get("headers", []) if key.lower() != b"content-type"]
                message = {**message, "headers": [*headers, (b"content-type", content_type)]}
            await send(message)
        return await self.files(scope, receive, typed_send)


def register_optional_guide_routes(application, read_session, write_session):
    """Guided gap filling: mounted when present (the module is optional). The public build ships it (red team r20)."""
    try:
        module = importlib.import_module(".guide_routes", __package__)
    except ModuleNotFoundError as exc:
        if exc.name not in (f"{__package__}.guide_routes", "payguard.evidence_guide", "payguard.controlled_fallback"):
            raise
        return
    if getattr(application.state, "demo_mode", "off") == "public":
        # Hosted demo: the keyword chooser, unless the operator opted in to the guide's Gemini chooser (r32, free-tier
        # key, lower caps). The evidence brief and the Studio agents stay disabled there either way.
        application.state.guide = module.hosted_guide_service(application.state.store)
    module.register_guide_routes(application, read_session, write_session)


def register_optional_country_routes(application, read_session, write_session):
    """Per-country PayPal rules: mounted when present (the module is optional). The public build ships them since 66ba4f8
    (red team r20)."""
    try:
        module = importlib.import_module(".country_routes", __package__)
    except ModuleNotFoundError as exc:
        if exc.name not in (f"{__package__}.country_routes", "payguard.country_rules"):
            raise
        return
    module.register_country_routes(application, read_session, write_session, error_response)


def create_app(*, store=None, paypal=None, reference_loader=None, ai_brief=None, channel3=None,
               channel3_products=None, studio_model=None) -> FastAPI:
    # PAYGUARD_DEMO_MODE=public (hosted demo): every provider adapter, injected or default, is
    # replaced by a refusing stub. Off by default; then nothing below differs from the local console.
    demo_public = public_demo_enabled()
    hosted_host = require_public_host() if demo_public else None
    if demo_public:
        paypal, ai_brief = HostedDemoPaypalStub(), HostedDemoBriefStub()
    application = FastAPI(title="PayGuard Local Console", version="0.2.0", docs_url=None, redoc_url=None, openapi_url=None)
    application.state.demo_mode = "public" if demo_public else "off"
    application.state.store = store or SessionStore(ai_attempt_budget=PROCESS_AI_ATTEMPT_BUDGET)
    application.state.paypal = paypal or PaypalAdapter()
    application.state.paypal_tools = SafePaypalToolGateway(application.state.store, application.state.paypal)
    application.state.paypal_disputes = DisputeReadbackService(application.state.store, application.state.paypal)
    application.state.reference_loader = load_corpus if reference_loader is None else reference_loader
    application.state.ai_brief = ai_brief if ai_brief is not None else EvidenceBriefAdapter()
    # AG Studio built-in agents: off unless configured; never in the hosted demo (an injected model is ignored there too).
    application.state.studio_agents = StudioAgentService(
        None if demo_public else (studio_model if studio_model is not None else configured_studio_model()))
    # (optimise r24) Per-session AI audit log: model, token counts, latency, estimated cost; never prompt or reply text.
    application.state.ai_usage = AiUsageLog()
    application.state.studio_agents.usage_log = None if demo_public else application.state.ai_usage
    # Off unless PAYGUARD_CHANNEL3=enabled and CHANNEL3_API_KEY are both set; never alters the AUP decision.
    # The hosted demo forces it off whatever the environment says.
    application.state.channel3 = build_channel3_adapter(force_off=True) if demo_public else (
        channel3 if channel3 is not None else build_channel3_adapter())
    # Product reference cards: live only with the same flag and key; the hosted demo replays recorded replies.
    application.state.channel3_products = (channel3_products if channel3_products is not None and not demo_public
                                           else build_channel3_product_adapter(public_demo=demo_public))
    # Fuzzy case routing over the recorded catalogue; a live Channel3 search only when the operator configured a key.
    application.state.case_router = CaseRouter(products=application.state.channel3_products)
    if demo_public:
        # Added first so it runs inside the boundary: Host, Origin and body checks still run before it.
        application.add_middleware(HostedDemoGuardMiddleware, error_response=error_response)
        # Per-visitor pacing and a bounded in-flight queue, hosted demo only (owner 2026-11-03).
        application.add_middleware(TrafficGate, proxied=True)
        application.state.store.per_client_limits = True
        application.add_middleware(LocalBoundaryMiddleware, public_host=hosted_host)
    else:
        application.add_middleware(LocalBoundaryMiddleware)

    @application.exception_handler(BoundaryError)
    async def boundary_handler(_request, exc):
        if isinstance(exc, DisputeAmountMismatch):  # (r35 #6) the message names both amounts (pattern-checked)
            return JSONResponse(status_code=exc.status, headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"},
                                content={"error": {"code": exc.code, "message": exc.public_message}})
        return error_response(exc.status, exc.code, getattr(exc, "retry_after", None), extra=provider_error_extra(exc))

    @application.exception_handler(RequestValidationError)
    async def validation_handler(_request, exc):
        # A plain sentence for the one invoice rule a seller can fix directly (PayPal docs r24 currency-codes).
        if any(INVOICE_WHOLE_UNITS_ERROR in str(error.get("msg", "")) for error in exc.errors()):
            return error_response(422, INVOICE_WHOLE_UNITS_ERROR)
        return error_response(422, "schema_invalid")

    @application.exception_handler(ValueError)
    async def domain_handler(_request, _exc):
        return error_response(422, "domain_invalid")

    @application.exception_handler(ResponseValidationError)
    async def response_handler(_request, _exc):
        return error_response(500, "response_contract_failure")

    @application.exception_handler(HTTPException)
    async def http_handler(_request, exc):
        return error_response(exc.status_code, "route_unavailable")

    @application.exception_handler(Exception)
    async def unexpected_handler(_request, _exc):
        return error_response(500, "internal_error")

    def _record_ai_call(session, stage, model, usage, started, outcome):
        if application.state.demo_mode == "public":
            return
        log = application.state.ai_usage
        log.forget_missing(application.state.store.sessions)
        log.record(session.session_id, stage=stage, model=model, usage=usage,
                   latency_ms=(time.monotonic() - started) * 1000, outcome=outcome)

    def read_session(request: Request):
        return application.state.store.require(request.headers.get("X-Demo-Session"))

    def write_session(request: Request):
        return application.state.store.require(request.headers.get("X-Demo-Session"), request.headers.get("X-CSRF-Token"), mutate=True)

    @application.get("/api/v1/ai/usage", response_model=AiUsageResponse)
    def ai_usage(session=Depends(read_session)):
        """(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
        text is ever stored; the hosted demo makes no model call and answers an empty list."""
        hosted = application.state.demo_mode == "public"
        entries = [] if hosted else application.state.ai_usage.entries(session.session_id)
        return {"source": "hosted_demo" if hosted else "session_memory", "entries": entries,
                "price_table_source": PRICE_TABLE_SOURCE, "cost_note": COST_NOTE, "content_logged": False}

    @application.post("/api/v1/ai/evidence-brief", response_model=AiBriefResponse)
    async def evidence_brief(body: AiBriefHttpRequest, session=Depends(write_session)):
        try:
            application.state.ai_brief.validate_attempt_configuration()
        except AiBriefError as exc:
            return error_response(exc.status, exc.code)
        # Local runs send the closed facts of this session; the hosted demo's stub answers before this point.
        facts = application.state.store.reserve_ai_brief(session, body.stage, body.case_ref)
        adapter = application.state.ai_brief
        started = time.monotonic()
        usage = None
        try:
            # (optimise r24) Adapters that report token counts return them beside the result.
            if callable(getattr(adapter, "generate_with_usage", None)):
                result, usage = await adapter.generate_with_usage({"stage": body.stage, "session_facts": facts})
            else:
                result = await adapter.generate({"stage": body.stage, "session_facts": facts})
        except AiBriefError as exc:
            _record_ai_call(session, body.stage, getattr(adapter, "MODEL_ID", None), None, started, "error")
            return error_response(exc.status, exc.code)
        _record_ai_call(session, body.stage, result.get("model") if type(result) is dict else None, usage, started, "ok")
        try:
            return AiBriefResponse.model_validate(result)
        except ValidationError:
            raise ResponseValidationError(errors=[{"type": "ai_contract_invalid"}]) from None

    @application.get("/api/v1/health", response_model=HealthResponse)
    def health():
        return {"status": "ok", "mode": "demo", "version": "0.2.0", "source": "synthetic"}

    @application.post("/api/v1/demo/sessions", response_model=SessionResponse, status_code=201)
    async def new_session(request: Request, _body: EmptyRequest):
        # A burst queues for a short wait instead of a refusal; a long wait answers 429 with Retry-After
        # (owner 2026-11-03: turn bursts into a queue).
        store = application.state.store
        key = request.scope.get("state", {}).get("client_key", "local")
        for _ in range(3):
            wait = store.creation_wait(key)
            if wait <= 0:
                break
            if wait > SESSION_QUEUE_SECONDS:
                return JSONResponse(status_code=429, headers={"Retry-After": str(max(1, math.ceil(wait)))},
                                    content={"error": {"code": "rate_limited",
                                                       "message": f"Too many new sessions; try again in {math.ceil(wait)} seconds."}})
            await asyncio.sleep(wait)
        return store.create(key)

    @application.get("/api/v1/demo/state", response_model=StateResponse)
    def state(session=Depends(read_session)):
        return application.state.store.state(session)

    @application.post("/api/v1/demo/inject", response_model=StateResponse)
    def inject(body: InjectRequest, session=Depends(write_session)):
        # Reset demo also forgets the session's country check, so a past Stop no longer blocks the draft after the
        # console shows "Not started" again (click-all 2026-11-03 #2).
        if body.scenario == "reset":
            (getattr(application.state, "country_blocks", None) or {}).pop(session.session_id, None)
            # (attack r21) ... and the evidence guide's answers for this session (the guide module is optional).
            guide = getattr(application.state, "guide", None)
            if guide is not None and hasattr(guide, "forget"):
                guide.forget(session.session_id)
        return application.state.store.inject(session, body.scenario)

    @application.post("/api/v1/aup/review", response_model=AupResponse)
    def aup(body: AupRequest, session=Depends(write_session)):
        return application.state.store.review_aup(session, body.description)

    @application.post("/api/v1/aup/category-signal", response_model=AupCategorySignalResponse)
    def aup_category_signal(body: AupCategorySignalRequest, session=Depends(write_session)):
        # Bound to a live AUP evaluation of the same text; the evaluation itself is not modified.
        application.state.store.require_aup_category_binding(session, body.evaluation_id, body.description)
        result = application.state.channel3.lookup(body.description)
        try:
            return AupCategorySignalResponse.model_validate(result)
        except ValidationError:
            return AupCategorySignalResponse.model_validate(
                {"status": "UNAVAILABLE", "signal": None, "reason": "contract_rejected", "affects_decision": False})

    @application.post("/api/v1/aup/product-reference", response_model=ProductReferenceResponse)
    def aup_product_reference(body: ProductReferenceRequest, session=Depends(write_session)):
        # Same binding as the category signal: a live AUP evaluation of the same text, read-only.
        application.state.store.require_aup_category_binding(session, body.evaluation_id, body.description)
        adapter = application.state.channel3_products
        try:
            result = ProductReferenceResponse.model_validate(adapter.lookup(body.description))
        except ValidationError:
            return ProductReferenceResponse.model_validate(
                {"status": "UNAVAILABLE", "source": None, "cards": [], "reason": "contract_rejected", "recorded_at": None,
                 "affects_decision": False})
        if result.status == "FOUND":
            adapter.remember(session.session_id, body.evaluation_id, result.model_dump())
        return result

    @application.post("/api/v1/aup/product-reference/confirm", response_model=ProductConfirmResponse)
    def aup_product_confirm(body: ProductConfirmRequest, session=Depends(write_session)):
        # Only a card this session was shown for this evaluation can be confirmed; the client cannot supply one.
        application.state.store.require_aup_category_binding(session, body.evaluation_id, body.description)
        shown = application.state.channel3_products.shown(session.session_id, body.evaluation_id)
        if shown is None:
            return error_response(422, "product_reference_not_shown")
        card = None
        if body.product_id is not None:
            card = shown["cards"].get(body.product_id)
            if card is None:
                return error_response(422, "product_reference_unknown")
        return ProductConfirmResponse.model_validate({
            "choice": "CONFIRMED" if card else "NONE_MATCH", "evaluation_id": body.evaluation_id,
            "description_digest": hashlib.sha256(body.description.encode("utf-8")).hexdigest(),
            "source": shown["source"], "recorded_at": shown["recorded_at"], "card": card,
            "card_digest": card_digest(card) if card else None, "confirmed_by": "seller", "affects_decision": False})

    @application.get("/api/v1/studio/agent-status")
    def studio_agent_status(_session=Depends(read_session)):
        live = application.state.studio_agents.live
        reason = None if live else ("hosted_demo" if application.state.demo_mode == "public" else "not_configured")
        return {"built_in_agents": "live" if live else "off", "reason": reason, "affects_decision": False}

    @application.post(STUDIO_TURN_PATH)
    def studio_agent_turn(body: dict, request: Request, session=Depends(write_session)):
        # A plain dict body: studio_agent.validate_turn is the closed contract (Pydantic would coerce first).
        try:
            output = application.state.studio_agents.turn(session.session_id, body,
                                                          client_id=request.client.host if request.client else None)
        except StudioAgentError as error:
            status = {"studio_agents_off": 503, "studio_turn_invalid": 422, "studio_turn_personal_data": 422,
                      "studio_agent_limit": 429, "studio_agent_unavailable": 503, "studio_agent_timeout": 504}.get(error.code, 502)
            return error_response(status, error.code)
        return {"output": output, "model": "gemini", "affects_decision": False}

    @application.post("/api/v1/cases/route", response_model=CaseRouteResponse)
    def case_route(body: CaseRouteRequest, session=Depends(write_session)):
        try:
            return CaseRouteResponse.model_validate(application.state.case_router.route(body.text, session.session_id))
        except ValidationError:
            return error_response(502, "case_route_contract_rejected")

    @application.post("/api/v1/aup/acknowledge", response_model=AupAcknowledgeResponse)
    def acknowledge_aup(body: AupAcknowledgeRequest, session=Depends(write_session)):
        return application.state.store.acknowledge_aup(session, body.model_dump())

    @application.post("/api/v1/references/search", response_model=ReferenceResponse)
    def references(body: ReferenceRequest, _session=Depends(write_session)):
        try:
            corpus = application.state.reference_loader()
            result = corpus.search(**body.model_dump())
        except RetrievalError as exc:
            if exc.code in {"query_invalid", "filter_invalid"}:
                return error_response(422, exc.code)
            return error_response(503, "reference_unavailable")
        except Exception:
            return error_response(500, "internal_error")
        if not isinstance(result, dict) or "source" in result:
            return error_response(500, "response_contract_failure")
        try:
            return ReferenceResponse.model_validate(dict(result, source="public_reference"), context={"request": body})
        except ValidationError:
            raise ResponseValidationError(errors=[{"type": "reference_contract_invalid"}]) from None

    @application.post("/api/v1/policy/assess", response_model=PolicyAssessmentResponse)
    def policy_assess(body: PolicyRequest, _session=Depends(write_session)):
        try:
            result = assess_applicability(**body.model_dump())
            # Same-process deterministic re-evaluation binds every nested metadata field.
            trusted = applicability.assess_applicability(**body.model_dump())
        except ApplicabilityError as exc:
            if exc.code == "applicability_corpus_unavailable":
                return error_response(503, "reference_unavailable")
            return error_response(422, exc.code)
        except Exception:
            return error_response(500, "internal_error")
        try:
            return PolicyAssessmentResponse.model_validate(result, context={"trusted": trusted})
        except (ValidationError, TypeError, ValueError):
            raise ResponseValidationError(errors=[{"type": "policy_contract_invalid"}]) from None

    @application.post("/api/v1/advisory/evaluate", response_model=AdvisoryEvaluationResponse)
    def advisory_evaluate(body: AdvisoryRequest, _session=Depends(write_session)):
        try:
            raw = body.candidate_json.encode("utf-8")
        except UnicodeError:
            return error_response(422, "advisory_input_invalid")
        context = body.model_dump(exclude={"candidate_json"})
        try:
            result = evaluate_advisory(raw, **context)
            trusted = advisory_eval.evaluate_advisory(raw, **context)
        except AdvisoryError as exc:
            if exc.code == "advisory_corpus_unavailable":
                return error_response(503, "reference_unavailable")
            return error_response(422, exc.code)
        except Exception:
            return error_response(500, "internal_error")
        try:
            return AdvisoryEvaluationResponse.model_validate(result, context={"trusted": trusted})
        except (ValidationError, TypeError, ValueError):
            raise ResponseValidationError(errors=[{"type": "advisory_contract_invalid"}]) from None

    @application.post("/api/v1/disputes/{case_ref}/draft", response_model=DisputeDraftResponse,
                      response_model_exclude_unset=True)
    def draft(case_ref: str, _body: EmptyRequest, session=Depends(write_session)):
        return application.state.store.draft(session, case_ref)

    @application.post("/api/v1/disputes/{case_ref}/approve", response_model=DisputeApprovalResponse)
    def approve(case_ref: str, body: ApproveRequest, session=Depends(write_session)):
        return application.state.store.approve(session, case_ref, body.draft_digest)

    @application.get("/api/v1/connections", response_model=ConnectionsResponse)
    def connections(_session=Depends(read_session)):
        # Read-only deployment mode for the console. It reads the mode fixed at startup, never the environment,
        # so the hosted demo cannot reveal whether any key is present.
        return {"mode": "hosted_demo" if application.state.demo_mode == "public" else "local"}

    @application.get("/api/v1/paypal/status", response_model=PaypalStatusResponse)
    def paypal_status(_session=Depends(read_session)):
        return application.state.paypal.status()

    @application.post("/api/v1/paypal/connect", response_model=PaypalStatusResponse)
    async def connect(_body: EmptyRequest, _session=Depends(write_session)):
        return await application.state.paypal.connect()

    @application.post("/api/v1/paypal/invoices/review", response_model=InvoiceReviewResponse)
    def invoice_review(body: InvoiceReviewRequest, session=Depends(write_session)):
        # When the optional country-rules check ran for this session and found a BLOCK, no draft is prepared.
        latest = (getattr(application.state, "country_blocks", None) or {}).get(session.session_id) or {}
        if latest.get("blocked"):
            return error_response(409, "country_rules_blocked")
        # The checked seller/buyer pair is bound into the review and written on the Sandbox draft (review 2026-11-03:
        # the country check should touch the PayPal object, not only the page).
        route = ({"seller_country": latest["seller_country"], "buyer_country": latest["buyer_country"],
                  "goods_tags": list(latest.get("goods_tags") or [])} if latest.get("seller_country") else None)
        # (attack r22) A check that carried an amount binds the invoice to that amount and currency.
        if route is not None and not _country_amount_matches(latest, body.amount, body.currency):
            return error_response(409, "country_amount_changed")
        return application.state.store.review_invoice(session, body.model_dump(), country_route=route)

    @application.post("/api/v1/paypal/invoices/draft", response_model=InvoiceDraftResponse)
    async def invoice_draft(body: InvoiceDraftRequest, session=Depends(write_session)):
        # The stop also binds a review token minted before the block (red team 2026-11-03: review, then a blocking
        # country check, then "Create draft" still succeeded).
        latest = (getattr(application.state, "country_blocks", None) or {}).get(session.session_id) or {}
        if latest.get("blocked"):
            return error_response(409, "country_rules_blocked")
        # The route bound at review must still be the session's latest check (red team 2026-11-03 F5: review A->B,
        # then a non-blocking check C->D, used to create the draft with the stale A->B note). A review made with no
        # check stays allowed while no check exists: the country module is optional. Once a check exists, a review made
        # before it no longer fits (red team r16: review, then a passing check, then a draft with no route memo).
        review = session.invoice_reviews.get(body.review_token) or {}
        bound = (review.get("aup_binding") or {}).get("country_route")
        if bound is None and latest.get("seller_country"):
            return error_response(409, "country_check_changed")
        if bound is not None:
            current = ({"seller_country": latest["seller_country"], "buyer_country": latest["buyer_country"],
                        "goods_tags": list(latest.get("goods_tags") or [])} if latest.get("seller_country") else None)
            if current != bound:
                return error_response(409, "country_check_changed")
            # (attack r22) A later check with another amount or currency than the reviewed invoice also no longer fits.
            reviewed = review.get("payload") or {}
            if not _country_amount_matches(latest, reviewed.get("amount"), reviewed.get("currency")):
                return error_response(409, "country_amount_changed")
        return await application.state.paypal_tools.invoke("create_invoice", body.model_dump(), session=session)

    @application.get("/api/v1/paypal/disputes", response_model=DisputeListResponse)
    async def list_disputes(session=Depends(read_session)):
        return await application.state.paypal_disputes.list_disputes(session)

    @application.get("/api/v1/paypal/disputes/{dispute_id}", response_model=DisputeDetailResponse)
    async def get_dispute(dispute_id: str, session=Depends(read_session)):
        return await application.state.paypal_disputes.get_dispute(session, dispute_id)

    @application.post("/api/v1/paypal/disputes/provide-evidence", response_model=ProvideEvidenceResponse)
    async def provide_evidence(body: ProvideEvidenceRequest, session=Depends(write_session)):
        return await application.state.paypal_disputes.provide_evidence(session, body.model_dump())

    @application.post("/api/v1/paypal/disputes/add-tracking", response_model=AddTrackingResponse)
    async def add_tracking(body: AddTrackingRequest, session=Depends(write_session)):
        # Hosted demo: no provider calls (the stub adapter has no tracking action).
        if application.state.demo_mode == "public":
            return error_response(503, HOSTED_DEMO_CODE)
        return await application.state.paypal_disputes.add_tracking(session, body.model_dump())

    @application.post("/api/v1/paypal/webhooks/verify", response_model=WebhookVerifyResponse)
    async def verify_webhook(request: Request, _session=Depends(write_session)):
        # The raw body, not a parsed model: PayPal docs r24 require the event to be posted back exactly as received.
        return await application.state.paypal.verify_webhook(await request.body())

    register_optional_guide_routes(application, read_session, write_session)
    if not demo_public and getattr(application.state, "guide", None) is not None:
        application.state.guide.ai_usage = application.state.ai_usage
    register_optional_country_routes(application, read_session, write_session)

    # Single-port console: when the frontend has been built, serve it from this same loopback origin
    # (http://127.0.0.1:8000), so a judge runs one process and opens one address. API routes above win;
    # the mount only answers paths no route claimed. Nothing changes when the build is absent.
    static_dir = Path(os.environ.get("PAYGUARD_STATIC_DIR") or Path(__file__).resolve().parents[2] / "frontend" / "dist")
    if (static_dir / "index.html").is_file():
        application.state.static_dir = str(static_dir)
        application.mount("/", ConsoleStatic(str(static_dir), application.router.routes), name="console")
    return application


def create_lmstudio_app() -> FastAPI:
    """Create the explicit local-model API; the default application stays Gemini-bound."""
    return create_app(ai_brief=LmStudioEvidenceBriefAdapter(config=LmStudioConfig(enabled=True)))


app = create_app()
