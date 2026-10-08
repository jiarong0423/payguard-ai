"""Loopback-only FastAPI application with explicit synthetic session boundaries."""

import ipaddress
import json

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from pydantic import ValidationError

from payguard.engines import check_aup
from payguard.retrieval import RetrievalError, load_corpus
from payguard import applicability, advisory_eval
from payguard.applicability import ApplicabilityError, assess_applicability
from payguard.advisory_eval import AdvisoryError, evaluate_advisory

from .paypal import PaypalAdapter
from .paypal_tools import SafePaypalToolGateway
from .ai_brief import AiBriefError, AiBriefRequest, AiBriefResponse, EvidenceBriefAdapter
from .lmstudio_brief import LmStudioConfig, LmStudioEvidenceBriefAdapter
from .schemas import (ApproveRequest, AupRequest, AupResponse, AupAcknowledgeRequest, AupAcknowledgeResponse, DisputeApprovalResponse,
                      DisputeDraftResponse, EmptyRequest, HealthResponse, InjectRequest,
                      InvoiceDraftRequest, InvoiceDraftResponse, InvoiceReviewRequest,
                      InvoiceReviewResponse, PaypalStatusResponse, SessionResponse,
                      StateResponse, WebhookVerifyRequest, WebhookVerifyResponse,
                      ReferenceRequest, ReferenceResponse, PolicyRequest,
                      AdvisoryRequest, PolicyAssessmentResponse, AdvisoryEvaluationResponse)
from .store import AiAttemptBudget, BoundaryError, SessionStore
PROCESS_AI_ATTEMPT_BUDGET = AiAttemptBudget()

ALLOWED_HOSTS = frozenset({"localhost:8000", "127.0.0.1:8000", "[::1]:8000"})
ALLOWED_ORIGINS = frozenset({"http://localhost:5173", "http://127.0.0.1:5173",
                             "http://localhost:8000", "http://127.0.0.1:8000"})
MAX_BODY_BYTES = 16384
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


def error_response(status: int, code: str):
    if code.startswith("ai_"):
        message = "The AI evidence brief is unavailable or could not be verified."
    elif code == "reference_unavailable":
        message = "The local public reference corpus is unavailable."
    else:
        message = _MESSAGES.get(status, "The request could not be completed.")
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}},
                        headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})


class LocalBoundaryMiddleware:
    """Validate transport identity and bounded bodies before HTTP parsing."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = scope.get("headers", [])
        sensitive = {b"host", b"origin", b"x-demo-session", b"x-csrf-token", b"content-length", b"content-type"}
        for name in sensitive:
            if sum(key.lower() == name for key, _ in headers) > 1:
                return await error_response(403, "duplicate_security_header")(scope, receive, send)
        header = {key.lower(): value.decode("latin-1") for key, value in headers}
        try:
            loopback = ipaddress.ip_address(scope.get("client", ("", 0))[0]).is_loopback
        except (ValueError, TypeError, IndexError):
            loopback = False
        if not loopback or header.get(b"host", "").lower() not in ALLOWED_HOSTS:
            return await error_response(403, "host_rejected")(scope, receive, send)
        origin = header.get(b"origin")
        if origin is not None and origin not in ALLOWED_ORIGINS:
            return await error_response(403, "origin_rejected")(scope, receive, send)
        method = scope["method"]
        if method in ("POST", "PUT", "PATCH", "DELETE") and origin not in ALLOWED_ORIGINS:
            return await error_response(403, "origin_required")(scope, receive, send)
        if method == "OPTIONS":
            requested_method = header.get(b"access-control-request-method", "")
            requested_headers = {item.strip().lower() for item in header.get(b"access-control-request-headers", "").split(",") if item.strip()}
            if (origin not in ALLOWED_ORIGINS or requested_method not in ("GET", "POST") or
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
        if declared < 0 or declared > MAX_BODY_BYTES:
            return await error_response(413, "body_limit")(scope, receive, send)
        chunks = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            if message["type"] != "http.request":
                continue
            chunks.extend(message.get("body", b""))
            if len(chunks) > MAX_BODY_BYTES:
                return await error_response(413, "body_limit")(scope, receive, send)
            if not message.get("more_body", False):
                break
        if method == "POST":
            if header.get(b"content-type", "").split(";", 1)[0].strip().lower() != "application/json":
                return await error_response(415, "json_required")(scope, receive, send)
            # Reject duplicate keys and nonfinite values before Pydantic can normalize them.
            def unique_object(pairs):
                result = {}
                for key, value in pairs:
                    if key in result:
                        raise ValueError("duplicate")
                    result[key] = value
                return result
            def reject_constant(_value):
                raise ValueError("nonfinite")
            try:
                parsed = json.loads(chunks, object_pairs_hook=unique_object, parse_constant=reject_constant)
                if not isinstance(parsed, dict):
                    raise ValueError("object_required")
            except (ValueError, UnicodeDecodeError, RecursionError):
                return await error_response(422, "invalid_json")(scope, receive, send)
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
                if origin in ALLOWED_ORIGINS:
                    response_headers.extend([(b"access-control-allow-origin", origin.encode()), (b"vary", b"Origin")])
                message["headers"] = response_headers
            await send(message)
        await self.app(scope, replay, safe_send)


def create_app(*, store=None, paypal=None, reference_loader=None, ai_brief=None) -> FastAPI:
    application = FastAPI(title="PayGuard Local Console", version="0.2.0", docs_url=None, redoc_url=None, openapi_url=None)
    application.state.store = store or SessionStore(ai_attempt_budget=PROCESS_AI_ATTEMPT_BUDGET)
    application.state.paypal = paypal or PaypalAdapter()
    application.state.paypal_tools = SafePaypalToolGateway(application.state.store, application.state.paypal)
    application.state.reference_loader = load_corpus if reference_loader is None else reference_loader
    application.state.ai_brief = ai_brief if ai_brief is not None else EvidenceBriefAdapter()
    application.add_middleware(LocalBoundaryMiddleware)

    @application.exception_handler(BoundaryError)
    async def boundary_handler(_request, exc):
        return error_response(exc.status, exc.code)

    @application.exception_handler(RequestValidationError)
    async def validation_handler(_request, _exc):
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

    def read_session(request: Request):
        return application.state.store.require(request.headers.get("X-Demo-Session"))

    def write_session(request: Request):
        return application.state.store.require(request.headers.get("X-Demo-Session"), request.headers.get("X-CSRF-Token"), mutate=True)

    @application.post("/api/v1/ai/evidence-brief", response_model=AiBriefResponse)
    async def evidence_brief(body: AiBriefRequest, session=Depends(write_session)):
        application.state.store.reserve_ai_brief_attempt(session, body.stage)
        try:
            result = await application.state.ai_brief.generate(body.model_dump())
        except AiBriefError as exc:
            return error_response(exc.status, exc.code)
        try:
            return AiBriefResponse.model_validate(result)
        except ValidationError:
            raise ResponseValidationError(errors=[{"type": "ai_contract_invalid"}]) from None

    @application.get("/api/v1/health", response_model=HealthResponse)
    def health():
        return {"status": "ok", "mode": "demo", "version": "0.2.0", "source": "synthetic"}

    @application.post("/api/v1/demo/sessions", response_model=SessionResponse, status_code=201)
    def new_session(_body: EmptyRequest):
        return application.state.store.create()

    @application.get("/api/v1/demo/state", response_model=StateResponse)
    def state(session=Depends(read_session)):
        return application.state.store.state(session)

    @application.post("/api/v1/demo/inject", response_model=StateResponse)
    def inject(body: InjectRequest, session=Depends(write_session)):
        return application.state.store.inject(session, body.scenario)

    @application.post("/api/v1/aup/review", response_model=AupResponse)
    def aup(body: AupRequest, session=Depends(write_session)):
        return application.state.store.review_aup(session, body.description)

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

    @application.post("/api/v1/disputes/{case_ref}/draft", response_model=DisputeDraftResponse)
    def draft(case_ref: str, _body: EmptyRequest, session=Depends(write_session)):
        return application.state.store.draft(session, case_ref)

    @application.post("/api/v1/disputes/{case_ref}/approve", response_model=DisputeApprovalResponse)
    def approve(case_ref: str, body: ApproveRequest, session=Depends(write_session)):
        return application.state.store.approve(session, case_ref, body.draft_digest)

    @application.get("/api/v1/paypal/status", response_model=PaypalStatusResponse)
    def paypal_status(_session=Depends(read_session)):
        return application.state.paypal.status()

    @application.post("/api/v1/paypal/connect", response_model=PaypalStatusResponse)
    async def connect(_body: EmptyRequest, _session=Depends(write_session)):
        return await application.state.paypal.connect()

    @application.post("/api/v1/paypal/invoices/review", response_model=InvoiceReviewResponse)
    def invoice_review(body: InvoiceReviewRequest, session=Depends(write_session)):
        return application.state.store.review_invoice(session, body.model_dump())

    @application.post("/api/v1/paypal/invoices/draft", response_model=InvoiceDraftResponse)
    async def invoice_draft(body: InvoiceDraftRequest, session=Depends(write_session)):
        return await application.state.paypal_tools.invoke("create_invoice", body.model_dump(), session=session)

    @application.post("/api/v1/paypal/webhooks/verify", response_model=WebhookVerifyResponse)
    async def verify_webhook(body: WebhookVerifyRequest, _session=Depends(write_session)):
        return await application.state.paypal.verify_webhook(body.model_dump())

    return application


def create_lmstudio_app() -> FastAPI:
    """Create the explicit local-model API; the default application stays Gemini-bound."""
    return create_app(ai_brief=LmStudioEvidenceBriefAdapter(config=LmStudioConfig(enabled=True)))


app = create_app()
