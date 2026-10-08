"""One reviewed Sandbox operation; optional SDK catalog, never its executor."""

import hmac
import importlib.metadata
import json
import math
import re

from pydantic import ValidationError

from .schemas import InvoiceDraftRequest, InvoiceDraftResponse, InvoicePayload, PaypalStatusResponse
from .store import BoundaryError, Session, SessionStore


MAX_ARGUMENT_BYTES = 8192
MAX_ARGUMENT_DEPTH = 8
MAX_ARGUMENT_NODES = 128
_SAFE_ERRORS = {
    (401, "session_required"), (405, "tool_action_frozen"),
    (413, "body_limit"), (422, "schema_invalid"),
    (422, "invalid_amount"), (422, "description_requires_policy_review"),
    (422, "review_binding_rejected"), (429, "invoice_attempt_limit"),
    (502, "provider_response_invalid"), (502, "provider_upstream_failure"),
    (503, "provider_disabled"), (503, "provider_not_configured"),
    (503, "provider_not_connected"), (503, "provider_environment_rejected"),
    (503, "clock_unavailable"), (503, "tool_runtime_unavailable"),
}


def _safe_error(error):
    if (type(error) is BoundaryError and type(error.status) is int and type(error.code) is str and
            (error.status, error.code) in _SAFE_ERRORS):
        return BoundaryError(error.status, error.code)
    return BoundaryError(502, "provider_upstream_failure")


def _bounded_object(arguments):
    """Bound before parsing, reject JSON ambiguity and Python object hooks."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate")
            result[key] = value
        return result

    def nonfinite(_value):
        raise ValueError("nonfinite")

    try:
        if type(arguments) is str:
            if len(arguments) > MAX_ARGUMENT_BYTES or len(arguments.encode("utf-8")) > MAX_ARGUMENT_BYTES:
                raise BoundaryError(413, "body_limit")
            arguments = json.loads(arguments, object_pairs_hook=unique, parse_constant=nonfinite)
        if type(arguments) is not dict:
            raise ValueError("object_required")
        stack = [(arguments, 0)]
        seen = set()
        nodes = size = 0
        while stack:
            value, depth = stack.pop()
            nodes += 1
            if depth > MAX_ARGUMENT_DEPTH or nodes > MAX_ARGUMENT_NODES:
                raise ValueError("complexity")
            kind = type(value)
            if kind in (dict, list):
                if id(value) in seen or len(value) > MAX_ARGUMENT_NODES:
                    raise ValueError("complexity")
                seen.add(id(value))
                if kind is dict:
                    for key, child in value.items():
                        if type(key) is not str:
                            raise ValueError("key")
                        stack.append((key, depth + 1))
                        stack.append((child, depth + 1))
                else:
                    stack.extend((child, depth + 1) for child in value)
            elif kind is str:
                if len(value) > MAX_ARGUMENT_BYTES:
                    raise BoundaryError(413, "body_limit")
                size += len(value.encode("utf-8"))
            elif kind is float:
                if not math.isfinite(value):
                    raise ValueError("nonfinite")
                size += 32
            elif kind is int:
                if value.bit_length() > 128:
                    raise ValueError("integer")
                size += 40
            elif kind in (bool, type(None)):
                size += 5
            else:
                raise ValueError("type")
            if size > MAX_ARGUMENT_BYTES:
                raise BoundaryError(413, "body_limit")
        return arguments
    except BoundaryError:
        raise
    except (ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise BoundaryError(422, "schema_invalid") from None


def _request(arguments, schema=InvoiceDraftRequest):
    try:
        return schema.model_validate(_bounded_object(arguments)).model_dump()
    except ValidationError:
        raise BoundaryError(422, "schema_invalid") from None


class SafePaypalToolGateway:
    """Trusted caller supplies session; arguments cannot select authority/transport."""

    def __init__(self, store: SessionStore, adapter):
        self._store = store
        self._adapter = adapter

    def _live_session(self, session):
        if (type(session) is not Session or
                self._store.sessions.get(session.session_id) is not session or
                session.expires_at <= self._store._now()):
            raise BoundaryError(401, "session_required")

    async def invoke(self, method, arguments, *, session):
        if type(method) is not str or method != "create_invoice":
            raise BoundaryError(405, "tool_action_frozen")
        request = _request(arguments)
        try:
            with self._store.lock:
                self._live_session(session)
                status = PaypalStatusResponse.model_validate(self._adapter.status())
                if status.environment != "sandbox":
                    raise BoundaryError(503, "provider_environment_rejected")
                self._adapter.require_connected()
                if status.status != "connected":
                    raise BoundaryError(503, "provider_not_connected")
                payload, request_id = self._store.consume_invoice(session, request)
            result = await self._adapter.create_invoice_draft(payload, request_id)
            try:
                response = InvoiceDraftResponse.model_validate(_bounded_object(result))
            except (BoundaryError, ValidationError):
                raise BoundaryError(502, "provider_response_invalid") from None
            if (response.evidence_receipt.evidence_class != status.evidence_receipt.evidence_class or
                    not re.fullmatch(r"INV2-[A-Z0-9-]{8,64}", response.invoice_id)):
                raise BoundaryError(502, "provider_response_invalid")
            return response.model_dump()
        except ValidationError:
            raise BoundaryError(502, "provider_response_invalid") from None
        except BoundaryError as error:
            raise _safe_error(error) from None
        except Exception:
            raise BoundaryError(502, "provider_upstream_failure") from None


def create_official_invoice_tool(gateway, *, session, reviewed_request):
    """Explicit optional factory, using a narrowed local schema, not upstream schema.

    The upstream catalog proves tool identity only. Its execute function, API,
    requests client and context are never used. A trusted operator binds one
    existing review; SDK run context carries no authority.
    """
    request = _request(reviewed_request)
    try:
        with gateway._store.lock:
            gateway._live_session(session)
            review = session.invoice_reviews.get(request["review_token"])
            payload = {key: request[key] for key in ("description", "amount", "currency")}
            if (review is None or review["expires_at"] <= gateway._store._now() or
                    review["payload"] != payload or
                    not hmac.compare_digest(review["digest"], request["payload_digest"])):
                raise BoundaryError(422, "review_binding_rejected")
        for package, expected in (("paypal-agent-toolkit", "1.11.0"),
                                  ("openai-agents", "0.0.2"), ("openai", "1.66.0")):
            if importlib.metadata.version(package) != expected:
                raise BoundaryError(503, "tool_runtime_unavailable")
        from paypal_agent_toolkit.shared.tools import tools
        from agents import FunctionTool
        matches = [row for row in tools if row.get("method") == "create_invoice"]
        if (len(matches) != 1 or matches[0].get("name") != "Create PayPal Invoice" or
                matches[0].get("actions") != {"invoices": {"create": True}}):
            raise BoundaryError(503, "tool_runtime_unavailable")
    except BoundaryError as error:
        raise _safe_error(error) from None
    except Exception:
        raise BoundaryError(503, "tool_runtime_unavailable") from None

    async def callback(_context, arguments):
        supplied = _request(arguments, InvoicePayload)
        if supplied != payload:
            raise BoundaryError(422, "review_binding_rejected")
        result = await gateway.invoke("create_invoice", dict(request), session=session)
        return json.dumps(result, separators=(",", ":"), allow_nan=False)

    return FunctionTool(
        name="create_invoice",
        description="Create exactly one operator-reviewed Sandbox invoice draft. Sending remains frozen.",
        params_json_schema=InvoicePayload.model_json_schema(),
        on_invoke_tool=callback,
        strict_json_schema=True,
    )
