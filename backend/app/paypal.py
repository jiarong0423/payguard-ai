"""Fixed-host Sandbox transport; secrets and raw provider bodies stay private."""

import asyncio
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
import json
import math
import os
import re

import httpx
from pydantic import ValidationError

from .store import BoundaryError, iso, utc_now
from .schemas import (DISPUTE_ID_PATTERN, PAYPAL_DEBUG_ID_PATTERN, SandboxEvidenceReceipt, PaypalStatusResponse,
                      WebhookEnvelope)


SANDBOX_BASE = "https://api-m.sandbox.paypal.com"
HTTP_TIMEOUT = httpx.Timeout(8.0, connect=5.0)
PROVIDER_JSON_MAX_DEPTH = 32
PROVIDER_JSON_MAX_NODES = 4096
PROVIDER_JSON_MAX_INTEGER_DIGITS = 64
_DISPUTE_ID = re.compile(DISPUTE_ID_PATTERN)
_DISPUTE_PATH = re.compile(r"/v1/customer/disputes/(PP-[A-Z0-9][A-Z0-9-]{2,62})(/provide-evidence)?")
_POST_ALLOWLIST = frozenset({"/v1/oauth2/token", "/v2/invoicing/invoices", "/v1/notifications/verify-webhook-signature",
                             "/v1/shipping/trackers-batch"})
_DEBUG_ID = re.compile(PAYPAL_DEBUG_ID_PATTERN.strip("^$"))
# Sandbox webhook certificates are served from these hosts only (PayPal docs r24: cert_url <= 500 characters).
_CERT_URL = re.compile(r"https://api(?:-m)?\.sandbox\.paypal\.com/v1/notifications/certs/[A-Za-z0-9._-]{1,400}")
_SAFE_EVENT_VALUE = re.compile(r"[A-Za-z0-9_.:-]{1,128}")
_JSON_WS = " \t\n\r"
CALL_LOG_MAX = 64
# (evloop) PayPal error reasons the seller can read: the error `name` and up to 3 `details[].issue` codes, each a
# closed code shape. Free text (`message`, `description`, `field`, `value`, links) is never kept (PayPal docs: the
# error and error_details schemas of the Disputes, Tracking and Invoicing specs).
PAYPAL_CODE_PATTERN = r"^[A-Z0-9_]{1,64}$"
_PAYPAL_CODE = re.compile(PAYPAL_CODE_PATTERN.strip("^$"))
PAYPAL_ISSUE_MAX = 3


def _paypal_code(value):
    return value if type(value) is str and _PAYPAL_CODE.fullmatch(value) else None


def paypal_issue_from_body(content) -> dict | None:
    """Closed projection of a non-2xx PayPal body: {"name": code or None, "issues": [up to 3 codes]}, or None.

    Only values that fully match ^[A-Z0-9_]{1,64}$ survive; anything else (free text, lower case, too long, not a
    string) is dropped. Nothing else from the body is read.
    """
    try:
        body = json.loads(bytes(content), parse_constant=_reject_constant, parse_int=_provider_integer,
                          parse_float=_provider_float)
    except (ValueError, TypeError, UnicodeDecodeError, RecursionError):
        return None
    if not isinstance(body, dict):
        return None
    name = _paypal_code(body.get("name"))
    issues = []
    details = body.get("details")
    if type(details) is list:
        for row in details:
            code = _paypal_code(row.get("issue")) if type(row) is dict else None
            if code is not None and code not in issues:
                issues.append(code)
                if len(issues) == PAYPAL_ISSUE_MAX:
                    break
    if name is None and not issues:
        return None
    return {"name": name, "issues": issues}


class PaypalProviderError(BoundaryError):
    """A non-2xx PayPal answer: the same fixed code, plus the sanitised reason and the PayPal-Debug-Id."""

    def __init__(self, status: int, code: str, *, paypal_issue=None, paypal_debug_id=None):
        super().__init__(status, code)
        self.paypal_issue = paypal_issue
        self.paypal_debug_id = paypal_debug_id


def provider_error_extra(exc) -> dict:
    """Optional error-body fields for a PaypalProviderError, re-checked here; {} for any other error."""
    if not isinstance(exc, PaypalProviderError):
        return {}
    extra = {}
    issue = exc.paypal_issue
    if type(issue) is dict and set(issue) == {"name", "issues"} and type(issue["issues"]) is list:
        name = issue["name"] if issue["name"] is None else _paypal_code(issue["name"])
        issues = [code for code in issue["issues"][:PAYPAL_ISSUE_MAX] if _paypal_code(code) is not None]
        if name is not None or issues:
            extra["paypal_issue"] = {"name": name, "issues": issues}
    debug_id = exc.paypal_debug_id
    if type(debug_id) is str and _DEBUG_ID.fullmatch(debug_id):
        extra["paypal_debug_id"] = debug_id
    return extra


def _keep_provider_error(exc: BoundaryError) -> BoundaryError:
    """Rebuild a boundary error with its fixed status and code; a provider answer keeps its sanitised reason."""
    if isinstance(exc, PaypalProviderError):
        return PaypalProviderError(exc.status, exc.code, paypal_issue=exc.paypal_issue,
                                   paypal_debug_id=exc.paypal_debug_id)
    return BoundaryError(exc.status, exc.code)


def _call_label(method: str, path: str) -> str:
    if path == "/v1/oauth2/token":
        return "OAUTH_TOKEN"
    if path == "/v2/invoicing/invoices":
        return "INVOICE_DRAFT"
    if path == "/v1/notifications/verify-webhook-signature":
        return "WEBHOOK_VERIFY"
    if path == "/v1/shipping/trackers-batch":
        return "ADD_TRACKING"
    if path == "/v1/customer/disputes":
        return "DISPUTES_LIST"
    return "PROVIDE_EVIDENCE" if path.endswith("/provide-evidence") else "DISPUTE_DETAIL"


def _reject_constant(_value):
    raise ValueError("nonfinite value")


def _top_level_raw_members(text: str) -> dict[str, str]:
    """Split one JSON object into {key: exact raw text of its value}, without re-serializing any value.

    PayPal docs r24 (webhooks): the webhook_event must be posted back exactly as it was received, with no deviations
    in formatting, so the event is kept as the original text slice, never parsed and re-stringified.
    """
    decoder = json.JSONDecoder(parse_constant=_reject_constant)
    def skip(index):
        while index < len(text) and text[index] in _JSON_WS:
            index += 1
        return index
    index = skip(0)
    if index >= len(text) or text[index] != "{":
        raise ValueError("object_required")
    members = {}
    index = skip(index + 1)
    if index < len(text) and text[index] == "}":
        index += 1
    else:
        while True:
            if index >= len(text) or text[index] != '"':
                raise ValueError("key_required")
            key, index = json.decoder.scanstring(text, index + 1)
            index = skip(index)
            if index >= len(text) or text[index] != ":":
                raise ValueError("colon_required")
            index = skip(index + 1)
            _value, end = decoder.raw_decode(text, index)
            if key in members:
                raise ValueError("duplicate")
            members[key] = text[index:end]
            index = skip(end)
            if index < len(text) and text[index] == ",":
                index = skip(index + 1)
                continue
            if index < len(text) and text[index] == "}":
                index += 1
                break
            raise ValueError("separator_required")
    if skip(index) != len(text):
        raise ValueError("trailing_data")
    return members


def allowed_request(method: str, path: str) -> bool:
    """Closed method/path allowlist; dispute paths carry a validated id only."""
    if method == "POST" and path in _POST_ALLOWLIST:
        return True
    if method == "GET" and path == "/v1/customer/disputes":
        return True
    match = _DISPUTE_PATH.fullmatch(path)
    if match is None:
        return False
    if match.group(2):
        return method == "POST"
    return method == "GET"


def _provider_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("nonfinite provider value")
    return parsed


def _provider_integer(value: str) -> int:
    digits = value[1:] if value.startswith("-") else value
    if len(digits) > PROVIDER_JSON_MAX_INTEGER_DIGITS:
        raise ValueError("provider integer too large")
    return int(value)


def _validate_provider_tree(root) -> None:
    stack = [(root, 0)]
    nodes = 0
    while stack:
        value, depth = stack.pop()
        nodes += 1
        if nodes > PROVIDER_JSON_MAX_NODES or depth > PROVIDER_JSON_MAX_DEPTH:
            raise ValueError("provider tree limit exceeded")
        if isinstance(value, dict):
            stack.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, list):
            stack.extend((child, depth + 1) for child in value)
        elif type(value) is float:
            if not math.isfinite(value):
                raise ValueError("nonfinite provider value")
        elif value is not None and type(value) not in (str, int, bool):
            raise ValueError("unsupported provider value")


@dataclass(frozen=True)
class PaypalConfig:
    enabled: bool = False
    client_id: str = field(default="", repr=False)
    client_secret: str = field(default="", repr=False)
    webhook_id: str = field(default="", repr=False)
    dispute_submit: bool = False
    tracking_submit: bool = False
    # (r25 send guard) The connected Sandbox account's PayPal account ID (Disputes v1 field
    # disputed_transactions[].seller.merchant_id, "The PayPal account ID for the merchant"), declared by the operator:
    # the client-credentials token response carries no account id, and no allow-listed endpoint returns one without a
    # new scope. Empty means unknown, and every real dispute send is then refused (409 account_identity_unknown).
    merchant_id: str = field(default="", repr=False)


def operator_config() -> PaypalConfig:
    """Only an explicit connect operation calls this credential boundary.

    Never load dotenv files or print environment values. The agent's tests use
    injected synthetic config and MockTransport; this accessor is not invoked.
    """
    if os.environ.get("PAYGUARD_PAYPAL_OUTBOUND") != "enabled":
        return PaypalConfig()
    return PaypalConfig(True, os.environ.get("PAYPAL_CLIENT_ID", ""),
                        os.environ.get("PAYPAL_CLIENT_SECRET", ""),
                        os.environ.get("PAYPAL_WEBHOOK_ID", ""),
                        os.environ.get("PAYGUARD_PAYPAL_DISPUTE_SUBMIT") == "enabled",
                        os.environ.get("PAYGUARD_PAYPAL_TRACKING_SUBMIT") == "enabled",
                        os.environ.get("PAYGUARD_PAYPAL_SANDBOX_MERCHANT_ID", ""))


class PaypalAdapter:
    def __init__(self, *, config_loader=operator_config, transport=None, clock=utc_now):
        # Immutable provenance ceiling: injected instances can never be authentic.
        self.__constructor_evidence_class = (
            "AUTHENTIC_SANDBOX_RESPONSE" if config_loader is operator_config and
            transport is None and clock is utc_now else "SYNTHETIC_TEST_RESPONSE")
        self.config_loader = config_loader
        self.transport = transport
        self.clock = clock
        self._revoke_connection("not_configured")
        self._lock = asyncio.Lock()
        self.open_clients = 0
        # PayPal-Debug-Id of the most recent provider call, and a bounded per-call log (label, HTTP status, debug id,
        # time). No token, header value other than the debug id, id or body is ever recorded here.
        self.last_debug_id = None
        self.call_log = deque(maxlen=CALL_LOG_MAX)

    @property
    def _evidence_class(self):
        # Current seams may downgrade the private constructor ceiling, never upgrade it.
        return ("AUTHENTIC_SANDBOX_RESPONSE" if self.__constructor_evidence_class == "AUTHENTIC_SANDBOX_RESPONSE" and self.transport is None and
                self.config_loader is operator_config and self.clock is utc_now
                else "SYNTHETIC_TEST_RESPONSE")

    def _now(self):
        try:
            now = self.clock()
            if type(now) is not datetime or now.tzinfo is None or now.utcoffset() is None:
                raise ValueError("clock_invalid")
            return now
        except Exception:
            raise BoundaryError(503, "clock_unavailable") from None

    def _receipt(self, action, status, now, invoice_id=None, *, evidence_class, debug_id=None):
        # Values are server-authored after validated POST success, never copied raw.
        return SandboxEvidenceReceipt.model_validate({
            "paypal_debug_id": debug_id,
            "schema_version": 1, "environment": "sandbox", "action": action,
            "status": status, "observed_at": iso(now), "invoice_id": invoice_id,
            "evidence_class": evidence_class, "proof_kind": "POST_RESPONSE_ONLY",
            "separate_get_readback": False, "external_send": "FROZEN",
        }).model_dump()

    def _revoke_connection(self, status):
        if status not in {"not_configured", "disconnected", "error"}:
            raise ValueError("revocation_status_invalid")
        self._config = PaypalConfig()
        self._access_token = None
        self._token_expiry = None
        self._last_verified_at = None
        self._connection_receipt = None
        self._status = status

    def account_merchant_id(self) -> str | None:
        """(r25 send guard) The connected account's merchant id, or None when not connected or not declared.
        Callers mask it (first 2 and last 4 characters) before it reaches a log or a response."""
        merchant_id = getattr(self._config, "merchant_id", "")
        if self._status != "connected" or not self._access_token or type(merchant_id) is not str:
            return None
        return merchant_id if re.fullmatch(r"[0-9A-Za-z]{8,64}", merchant_id) else None

    def status(self) -> dict:
        expired = False
        if self._access_token:
            try:
                expired = self._token_expiry <= self._now()
            except Exception:
                self._revoke_connection("not_configured")
                raise BoundaryError(503, "clock_unavailable") from None
        if expired:
            self._access_token = None
            self._status = "disconnected"
            self._connection_receipt = None
        if self._status != "connected":
            self._connection_receipt = None
        return {"configured": bool(self._config.enabled and self._config.client_id and self._config.client_secret),
                "status": self._status, "environment": "sandbox", "source": "paypal_sandbox",
                "last_verified_at": self._last_verified_at,
                "evidence_receipt": dict(self._connection_receipt) if self._connection_receipt else None}

    def _enabled(self):
        if not self._config.enabled:
            raise BoundaryError(503, "provider_disabled")
        if not self._config.client_id or not self._config.client_secret:
            raise BoundaryError(503, "provider_not_configured")

    def require_connected(self):
        self._enabled()
        if self.status()["status"] != "connected":
            raise BoundaryError(503, "provider_not_connected")

    def _log_call(self, method, path, status_code, debug_id):
        # Wall-clock time for the log only, never the injected receipt clock (whose call order is part of the contract).
        try:
            observed = iso(utc_now())
        except Exception:
            observed = None
        self.call_log.append({"call": _call_label(method, path), "http_status": status_code,
                              "paypal_debug_id": debug_id, "observed_at": observed})

    async def _request(self, path: str, *, method="POST", headers=None, data=None, body=None, auth=None,
                       params=None, files=None, content=None) -> tuple[int, dict]:
        if method not in ("GET", "POST") or not allowed_request(method, path):
            raise BoundaryError(503, "provider_action_frozen")
        self.last_debug_id = None
        logged = False
        self.open_clients += 1
        try:
            async with asyncio.timeout(15), httpx.AsyncClient(base_url=SANDBOX_BASE, transport=self.transport,
                                         timeout=HTTP_TIMEOUT, follow_redirects=False, trust_env=False) as client:
                async with client.stream(method, path, headers=headers, params=params, data=data, json=body,
                                         files=files, auth=auth, content=content) as response:
                    # PayPal-Debug-Id identifies the call for PayPal support; it is kept only when it has the plain
                    # alphanumeric shape (PayPal docs r24), on success and on failure alike.
                    raw_debug = response.headers.get("paypal-debug-id")
                    debug_id = raw_debug if type(raw_debug) is str and _DEBUG_ID.fullmatch(raw_debug) else None
                    self.last_debug_id = debug_id
                    self._log_call(method, path, response.status_code, debug_id)
                    logged = True
                    content = bytearray()
                    async for chunk in response.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > 65536:
                            raise BoundaryError(502, "provider_response_invalid")
                    if not 200 <= response.status_code < 300:
                        # (evloop) Same fixed 502 code; the seller also gets PayPal's sanitised name and issue codes.
                        raise PaypalProviderError(502, "provider_upstream_failure",
                                                  paypal_issue=paypal_issue_from_body(content), paypal_debug_id=debug_id)
                    def unique_object(pairs):
                        parsed = {}
                        for key, value in pairs:
                            if key in parsed:
                                raise ValueError("duplicate provider key")
                            parsed[key] = value
                        return parsed
                    def reject_constant(_value):
                        raise ValueError("nonfinite provider value")
                    try:
                        result = json.loads(
                            content,
                            object_pairs_hook=unique_object,
                            parse_constant=reject_constant,
                            parse_float=_provider_float,
                            parse_int=_provider_integer,
                        )
                        _validate_provider_tree(result)
                    except (ValueError, UnicodeDecodeError, RecursionError):
                        raise BoundaryError(502, "provider_response_invalid") from None
                    if not isinstance(result, dict):
                        raise BoundaryError(502, "provider_response_invalid")
                    return response.status_code, result
        except (httpx.HTTPError, OSError, TimeoutError):
            if not logged:
                self._log_call(method, path, None, None)
            raise BoundaryError(502, "provider_upstream_failure") from None
        finally:
            self.open_clients -= 1

    async def connect(self) -> dict:
        async with self._lock:
            # Reconnect is fail-closed: revoke every prior success artifact before
            # invoking any injected or otherwise fallible boundary.
            self._revoke_connection("not_configured")
            try:
                evidence_class = self._evidence_class
                try:
                    config = self.config_loader()
                except Exception:
                    raise BoundaryError(503, "provider_not_configured") from None
                if type(config) is not PaypalConfig:
                    raise BoundaryError(503, "provider_not_configured")
                if not config.enabled:
                    raise BoundaryError(503, "provider_disabled")
                if not config.client_id or not config.client_secret:
                    raise BoundaryError(503, "provider_not_configured")
                self._now()
                if self._evidence_class != evidence_class:
                    evidence_class = "SYNTHETIC_TEST_RESPONSE"
                _, data = await self._request("/v1/oauth2/token", data={"grant_type": "client_credentials"},
                                              auth=httpx.BasicAuth(config.client_id, config.client_secret),
                                              headers={"Accept": "application/json"})
                token = data.get("access_token")
                expires = data.get("expires_in")
                token_type = data.get("token_type")
                if (not isinstance(token, str) or not 1 <= len(token) <= 4096 or
                        not re.fullmatch(r"[A-Za-z0-9._~-]+", token) or
                        not isinstance(token_type, str) or token_type.casefold() != "bearer" or
                        type(expires) is not int or not 1 <= expires <= 86400):
                    raise BoundaryError(502, "provider_response_invalid")
                debug_id = self.last_debug_id
                now = self._now()
                receipt = self._receipt("OAUTH_CONNECT", "CONNECTED", now, evidence_class=evidence_class,
                                        debug_id=debug_id)
                try:
                    expiry = now + timedelta(seconds=expires)
                except OverflowError:
                    raise BoundaryError(503, "clock_unavailable") from None
                verified_at = iso(now)
                response = PaypalStatusResponse.model_validate({
                    "configured": True, "status": "connected", "environment": "sandbox",
                    "source": "paypal_sandbox", "last_verified_at": verified_at,
                    "evidence_receipt": receipt,
                }).model_dump()
                # No await, clock/status read or injectable callback after commit.
                (self._config, self._access_token, self._token_expiry,
                 self._last_verified_at, self._connection_receipt, self._status) = (
                    config, token, expiry, verified_at, receipt, "connected")
                return response
            except BoundaryError as exc:
                self._revoke_connection("error" if exc.status == 502 else "not_configured")
                raise BoundaryError(exc.status, exc.code) from None
            except Exception:
                self._revoke_connection("error")
                raise BoundaryError(502, "provider_upstream_failure") from None

    async def create_invoice_draft(self, payload: dict, request_id: str) -> dict:
        async with self._lock:
            try:
                evidence_class = self._evidence_class
                self.require_connected()
                self._now()
                if self._evidence_class != evidence_class or self._connection_receipt["evidence_class"] != evidence_class:
                    evidence_class = "SYNTHETIC_TEST_RESPONSE"
                # No recipients, account IDs, invoice send, payment or refund actions.
                detail = {"currency_code": payload["currency"]}
                route = payload.get("country_route")
                if route:
                    # The seller's private memo, never the buyer-facing note (buyer review 2026-11-03: a note reads as a
                    # clearance to the buyer). Country codes only: no recipient, address or account data on the draft.
                    goods = ", ".join(route.get("goods_tags") or []) or "none ticked"
                    detail["memo"] = (f"PayGuard country check: ships from {route['seller_country']} to "
                                      f"{route['buyer_country']}; goods checked: {goods}. Not a customs or legal clearance.")
                body = {"detail": detail,
                        "items": [{"name": payload["description"], "quantity": "1",
                                   "unit_amount": {"currency_code": payload["currency"], "value": payload["amount"]}}]}
                _, result = await self._request("/v2/invoicing/invoices", body=body,
                                                headers={"Authorization": "Bearer " + self._access_token,
                                                         "Content-Type": "application/json", "Prefer": "return=representation",
                                                         "PayPal-Request-Id": request_id})
                debug_id = self.last_debug_id
                invoice_id = result.get("id")
                if (not isinstance(invoice_id, str) or not re.fullmatch(r"INV2-[A-Z0-9-]{8,64}", invoice_id) or
                        result.get("status") != "DRAFT"):
                    raise BoundaryError(502, "provider_response_invalid")
                # A clock failure here cannot undo the completed provider POST. The
                # adapter revokes local connection evidence and never retries it.
                receipt_now = self._now()
                return {"source": "paypal_sandbox", "invoice_id": invoice_id, "status": "DRAFT",
                        "environment": "sandbox", "external_send": "FROZEN",
                        "evidence_receipt": self._receipt("CREATE_INVOICE_DRAFT", "DRAFT", receipt_now, invoice_id,
                                                          evidence_class=evidence_class, debug_id=debug_id)}
            except BoundaryError as exc:
                if exc.code == "clock_unavailable":
                    self._revoke_connection("not_configured")
                raise _keep_provider_error(exc) from None

    def dispute_submit_enabled(self) -> bool:
        """True only while connected with the explicit submit flag in the loaded config."""
        return bool(self._config.enabled and self._config.dispute_submit and self._status == "connected")

    def tracking_submit_enabled(self) -> bool:
        """True only while connected with PAYGUARD_PAYPAL_TRACKING_SUBMIT=enabled in the loaded config."""
        return bool(self._config.enabled and self._config.tracking_submit and self._status == "connected")

    def _bearer_headers(self) -> dict:
        return {"Authorization": "Bearer " + self._access_token, "Accept": "application/json"}

    async def list_disputes(self, page_size: int = 10) -> list[dict]:
        """GET /v1/customer/disputes; the provider rows are projected before return."""
        from .paypal_disputes import sanitize_dispute_list
        if type(page_size) is not int or not 1 <= page_size <= 20:
            raise BoundaryError(422, "schema_invalid")
        async with self._lock:
            self.require_connected()
            _, result = await self._request("/v1/customer/disputes", method="GET", headers=self._bearer_headers(),
                                            params={"page_size": str(page_size)})
            return sanitize_dispute_list(result)

    async def get_dispute(self, dispute_id: str) -> dict:
        """GET /v1/customer/disputes/{id}; names, messages and links are never copied."""
        from .paypal_disputes import sanitize_dispute_detail
        if type(dispute_id) is not str or _DISPUTE_ID.fullmatch(dispute_id) is None:
            raise BoundaryError(422, "schema_invalid")
        async with self._lock:
            self.require_connected()
            _, result = await self._request(f"/v1/customer/disputes/{dispute_id}", method="GET",
                                            headers=self._bearer_headers())
            debug_id = self.last_debug_id
            detail = sanitize_dispute_detail(result)
            if detail["dispute_id"] != dispute_id:
                raise BoundaryError(502, "provider_response_invalid")
            return dict(detail, paypal_debug_id=debug_id)

    async def provide_evidence(self, dispute_id: str, parts: dict) -> dict:
        """POST multipart provide-evidence; requires the explicit submit flag."""
        if type(dispute_id) is not str or _DISPUTE_ID.fullmatch(dispute_id) is None:
            raise BoundaryError(422, "schema_invalid")
        async with self._lock:
            self.require_connected()
            if not self._config.dispute_submit:
                raise BoundaryError(503, "provider_action_frozen")
            if type(parts) is not dict or "input" not in parts:
                raise BoundaryError(422, "schema_invalid")
            # A correlation id only: PayPal-Request-Id is limited to 38 single-byte characters, and the Disputes spec
            # does not declare the header, so no PayPal-side idempotency is assumed (PayPal docs r24). The real guard
            # against a second send is the local one-approval-one-send lock in DisputeReadbackService.
            digest = hashlib.sha256(repr(sorted(parts.items())).encode("utf-8")).hexdigest()
            headers = {**self._bearer_headers(), "PayPal-Request-Id": "pg-" + hashlib.sha256(
                f"{dispute_id}|{digest}".encode("utf-8")).hexdigest()[:32]}
            status, _result = await self._request(f"/v1/customer/disputes/{dispute_id}/provide-evidence",
                                                  method="POST", headers=headers, files=parts)
            return {"status_code": status, "dispute_id": dispute_id, "paypal_debug_id": self.last_debug_id}

    async def add_tracking(self, tracker: dict) -> dict:
        """POST /v1/shipping/trackers-batch with one tracker; requires PAYGUARD_PAYPAL_TRACKING_SUBMIT=enabled.

        PayPal docs r24 (https://developer.paypal.com/docs/tracking/): the legacy batch call takes transaction_id,
        tracking_number, status and carrier. The response is reduced to a count; identifiers are not copied.
        """
        if type(tracker) is not dict or set(tracker) - {"transaction_id", "tracking_number", "status", "carrier",
                                                        "carrier_name_other"}:
            raise BoundaryError(422, "schema_invalid")
        async with self._lock:
            self.require_connected()
            if not self._config.tracking_submit:
                raise BoundaryError(503, "provider_action_frozen")
            status, result = await self._request("/v1/shipping/trackers-batch", method="POST",
                                                 headers={**self._bearer_headers(), "Content-Type": "application/json"},
                                                 body={"trackers": [dict(tracker)]})
            debug_id = self.last_debug_id
            identifiers = result.get("tracker_identifiers")
            errors = result.get("errors") or []
            if type(identifiers) is not list or not identifiers or type(errors) is not list or errors:
                raise BoundaryError(502, "provider_response_invalid")
            return {"status_code": status, "tracker_count": len(identifiers), "paypal_debug_id": debug_id}

    async def verify_webhook(self, raw_body: bytes) -> dict:
        """Verify one Sandbox webhook by posting the event back verbatim; keep only id, type and status afterwards.

        PayPal docs r24 (https://developer.paypal.com/api/rest/webhooks/rest/): the webhook_event must be posted back
        exactly as it was received, so the event is forwarded as its original raw JSON text inside a hand-built body.
        Nothing from the event is stored or logged; after SUCCESS only a closed projection is returned.
        """
        # The envelope is checked before any connection state, so a malformed request answers 422 whatever the state.
        try:
            if type(raw_body) is not bytes:
                raise ValueError("bytes_required")
            text = raw_body.decode("utf-8")
            members = _top_level_raw_members(text)
            parsed = {key: json.loads(value, parse_constant=_reject_constant) for key, value in members.items()}
        except (ValueError, UnicodeDecodeError, RecursionError):
            raise BoundaryError(422, "webhook_schema_invalid") from None
        cert_url = parsed.get("cert_url")
        if type(cert_url) is not str or len(cert_url) > 500 or _CERT_URL.fullmatch(cert_url) is None:
            raise BoundaryError(422, "webhook_certificate_rejected")
        try:
            envelope = WebhookEnvelope.model_validate(parsed)
        except ValidationError:
            raise BoundaryError(422, "webhook_schema_invalid") from None
        event = envelope.webhook_event
        if any(type(event.get(key)) is not str or not 1 <= len(event[key]) <= 128 for key in ("id", "event_type")):
            raise BoundaryError(422, "webhook_schema_invalid")
        async with self._lock:
            self.require_connected()
            if not self._config.webhook_id:
                raise BoundaryError(503, "webhook_not_configured")
            fields = {"auth_algo": envelope.auth_algo, "cert_url": envelope.cert_url,
                      "transmission_id": envelope.transmission_id, "transmission_sig": envelope.transmission_sig,
                      "transmission_time": envelope.transmission_time, "webhook_id": self._config.webhook_id}
            forwarded = ("{" + ",".join(json.dumps(key) + ":" + json.dumps(value) for key, value in fields.items()) +
                         ',"webhook_event":' + members["webhook_event"] + "}").encode("utf-8")
            _, result = await self._request("/v1/notifications/verify-webhook-signature", content=forwarded,
                                            headers={"Authorization": "Bearer " + self._access_token,
                                                     "Content-Type": "application/json"})
            debug_id = self.last_debug_id
            if result.get("verification_status") != "SUCCESS":
                raise BoundaryError(403, "webhook_verification_failed")
            resource = event.get("resource") if type(event.get("resource")) is dict else {}
            def safe(value):
                return value if type(value) is str and _SAFE_EVENT_VALUE.fullmatch(value) else None
            projection = {"id": safe(event.get("id")), "event_type": safe(event.get("event_type")),
                          "resource_type": safe(event.get("resource_type")), "resource_id": safe(resource.get("id")),
                          "resource_status": safe(resource.get("status"))}
            return {"source": "paypal_sandbox", "verification_status": "SUCCESS", "imported_into_demo": False,
                    "event": projection, "paypal_debug_id": debug_id}
