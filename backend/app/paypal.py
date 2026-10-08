"""Fixed-host Sandbox transport; secrets and raw provider bodies stay private."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import math
import os
import re

import httpx

from .store import BoundaryError, iso, utc_now
from .schemas import SandboxEvidenceReceipt, PaypalStatusResponse


SANDBOX_BASE = "https://api-m.sandbox.paypal.com"
HTTP_TIMEOUT = httpx.Timeout(8.0, connect=5.0)
PROVIDER_JSON_MAX_DEPTH = 32
PROVIDER_JSON_MAX_NODES = 4096
PROVIDER_JSON_MAX_INTEGER_DIGITS = 64


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


def operator_config() -> PaypalConfig:
    """Only an explicit connect operation calls this credential boundary.

    Never load dotenv files or print environment values. The agent's tests use
    injected synthetic config and MockTransport; this accessor is not invoked.
    """
    if os.environ.get("PAYGUARD_PAYPAL_OUTBOUND") != "enabled":
        return PaypalConfig()
    return PaypalConfig(True, os.environ.get("PAYPAL_CLIENT_ID", ""),
                        os.environ.get("PAYPAL_CLIENT_SECRET", ""),
                        os.environ.get("PAYPAL_WEBHOOK_ID", ""))


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

    def _receipt(self, action, status, now, invoice_id=None, *, evidence_class):
        # Values are server-authored after validated POST success, never copied raw.
        return SandboxEvidenceReceipt.model_validate({
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

    async def _request(self, path: str, *, headers=None, data=None, body=None, auth=None) -> tuple[int, dict]:
        if path not in ("/v1/oauth2/token", "/v2/invoicing/invoices", "/v1/notifications/verify-webhook-signature"):
            raise BoundaryError(503, "provider_action_frozen")
        self.open_clients += 1
        try:
            async with asyncio.timeout(15), httpx.AsyncClient(base_url=SANDBOX_BASE, transport=self.transport,
                                         timeout=HTTP_TIMEOUT, follow_redirects=False, trust_env=False) as client:
                async with client.stream("POST", path, headers=headers, data=data, json=body, auth=auth) as response:
                    content = bytearray()
                    async for chunk in response.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > 65536:
                            raise BoundaryError(502, "provider_response_invalid")
                    if not 200 <= response.status_code < 300:
                        raise BoundaryError(502, "provider_upstream_failure")
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
                now = self._now()
                receipt = self._receipt("OAUTH_CONNECT", "CONNECTED", now, evidence_class=evidence_class)
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
                body = {"detail": {"currency_code": payload["currency"]},
                        "items": [{"name": payload["description"], "quantity": "1",
                                   "unit_amount": {"currency_code": payload["currency"], "value": payload["amount"]}}]}
                _, result = await self._request("/v2/invoicing/invoices", body=body,
                                                headers={"Authorization": "Bearer " + self._access_token,
                                                         "Content-Type": "application/json", "Prefer": "return=representation",
                                                         "PayPal-Request-Id": request_id})
                invoice_id = result.get("id")
                if (not isinstance(invoice_id, str) or not re.fullmatch(r"INV2-[A-Z0-9-]{8,64}", invoice_id) or
                        result.get("status") != "DRAFT"):
                    raise BoundaryError(502, "provider_response_invalid")
                # A clock failure here cannot undo the completed provider POST. The
                # adapter revokes local connection evidence and never retries it.
                receipt_now = self._now()
                return {"source": "paypal_sandbox", "invoice_id": invoice_id, "status": "DRAFT",
                        "environment": "sandbox", "external_send": "FROZEN",
                        "evidence_receipt": self._receipt("CREATE_INVOICE_DRAFT", "DRAFT", receipt_now, invoice_id, evidence_class=evidence_class)}
            except BoundaryError as exc:
                if exc.code == "clock_unavailable":
                    self._revoke_connection("not_configured")
                raise BoundaryError(exc.status, exc.code) from None

    async def verify_webhook(self, payload: dict) -> dict:
        """Verify only an allowlisted event; never import a real resource into demo."""
        async with self._lock:
            self.require_connected()
            if not self._config.webhook_id:
                raise BoundaryError(503, "webhook_not_configured")
            expected = {"transmission_id", "transmission_time", "cert_url", "auth_algo", "transmission_sig", "webhook_event"}
            if not isinstance(payload, dict) or set(payload) != expected:
                raise BoundaryError(422, "webhook_schema_invalid")
            for key in expected - {"webhook_event"}:
                if not isinstance(payload[key], str) or not 1 <= len(payload[key]) <= 4096:
                    raise BoundaryError(422, "webhook_schema_invalid")
            if not re.fullmatch(r"https://api\.sandbox\.paypal\.com/v1/notifications/certs/[A-Za-z0-9-]+", payload["cert_url"]):
                raise BoundaryError(422, "webhook_certificate_rejected")
            event = payload["webhook_event"]
            if not isinstance(event, dict) or set(event) != {"id", "event_type", "resource_type", "create_time", "resource"}:
                raise BoundaryError(422, "webhook_schema_invalid")
            if any(not isinstance(event[key], str) or not 1 <= len(event[key]) <= 128
                   for key in ("id", "event_type", "resource_type", "create_time")):
                raise BoundaryError(422, "webhook_schema_invalid")
            if not isinstance(event["resource"], dict) or set(event["resource"]) != {"id", "status"}:
                raise BoundaryError(422, "webhook_sensitive_resource_rejected")
            if any(not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", value) for value in event["resource"].values()):
                raise BoundaryError(422, "webhook_sensitive_resource_rejected")
            _, result = await self._request("/v1/notifications/verify-webhook-signature", body=dict(payload, webhook_id=self._config.webhook_id),
                                            headers={"Authorization": "Bearer " + self._access_token,
                                                     "Content-Type": "application/json"})
            if result.get("verification_status") != "SUCCESS":
                raise BoundaryError(403, "webhook_verification_failed")
            return {"source": "paypal_sandbox", "verification_status": "SUCCESS", "imported_into_demo": False}
