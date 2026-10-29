"""Read-only PayPal Disputes readback plus a provide-evidence request preview.

Two data sources feed the same contract. When the Sandbox adapter is connected,
``GET /v1/customer/disputes`` and ``GET /v1/customer/disputes/{id}`` are called
through the reviewed gateway. Otherwise the console serves a synthetic fixture
that follows the public PayPal Disputes API JSON shape. Every response names its
source so the UI can label it as Sandbox or fixture.

``POST /v1/customer/disputes/{id}/provide-evidence`` is assembled as a multipart
request preview. It is sent only when the operator sets
``PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled`` and the request says ``submit: true``.
"""

from copy import deepcopy
import hashlib
import json
import re

from pydantic import ValidationError

from .schemas import (DisputeDetailResponse, DisputeListResponse, ProvideEvidenceResponse,
                      DISPUTE_ID_PATTERN)
from .store import BoundaryError, Session, SessionStore, iso


DISPUTE_REASONS = frozenset({
    "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
    "UNAUTHORISED", "CREDIT_NOT_PROCESSED", "DUPLICATE_TRANSACTION",
    "INCORRECT_AMOUNT", "PAYMENT_BY_OTHER_MEANS", "CANCELED_RECURRING_BILLING", "OTHER",
})
DISPUTE_STATUSES = frozenset({
    "OPEN", "WAITING_FOR_SELLER_RESPONSE", "WAITING_FOR_BUYER_RESPONSE",
    "UNDER_REVIEW", "RESOLVED", "CLOSED", "UNKNOWN",
})
DISPUTE_STAGES = frozenset({"INQUIRY", "CHARGEBACK", "PRE_ARBITRATION", "ARBITRATION", "UNKNOWN"})
EVIDENCE_SOURCES = frozenset({
    "REQUESTED_FROM_SELLER", "REQUESTED_FROM_BUYER", "SUBMITTED_BY_SELLER",
    "SUBMITTED_BY_BUYER", "SUBMITTED_BY_PARTNER",
})
MAX_LIST_ITEMS = 20
MAX_EVIDENCE_ROWS = 20
MAX_TRANSACTIONS = 10
MAX_NOTE_LENGTH = 2000
_DISPUTE_ID = re.compile(DISPUTE_ID_PATTERN)
_TOKEN = re.compile(r"[A-Z][A-Z0-9_]{0,63}")
_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z")
_MONEY_VALUE = re.compile(r"[0-9]{1,10}(?:\.[0-9]{1,2})?")
_CURRENCY = re.compile(r"[A-Z]{3}")
_TRANSACTION_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")
_TRACKING = re.compile(r"[A-Za-z0-9._-]{1,64}")


# Synthetic fixture in the public PayPal Disputes API JSON shape. Identifiers,
# amounts and dates are invented; they correspond to no PayPal account.
FIXTURE_DISPUTES = (
    {
        "dispute_id": "PP-D-00000001",
        "create_time": "2026-10-20T14:02:11.000Z",
        "update_time": "2026-10-21T09:15:40.000Z",
        "disputed_transactions": [{
            "seller_transaction_id": "SYNTHETIC-TXN-0001",
            "create_time": "2026-10-17T18:40:03.000Z",
            "transaction_status": "COMPLETED",
            "gross_amount": {"currency_code": "USD", "value": "48.00"},
            "seller": {"merchant_id": "SYNTHETICMERCHANT", "name": "Synthetic Demo Seller"},
            "buyer": {"name": "Synthetic Demo Person"},
            "items": [{"item_id": "SYN-CUP-001", "item_description": "Handcrafted ceramic coffee cup, set of two",
                       "item_quantity": "1", "partner_transaction_id": "SYNTHETIC-TXN-0001"}],
            "seller_protection_eligible": True,
        }],
        "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
        "status": "WAITING_FOR_SELLER_RESPONSE",
        "dispute_state": "REQUIRED_ACTION",
        "dispute_amount": {"currency_code": "USD", "value": "48.00"},
        "dispute_life_cycle_stage": "INQUIRY",
        "dispute_channel": "INTERNAL",
        "messages": [{"posted_by": "BUYER", "time_posted": "2026-10-20T14:02:11.000Z",
                      "content": "Synthetic buyer message: the package has not arrived."}],
        "evidences": [{
            "evidence_type": "PROOF_OF_FULFILLMENT",
            "source": "REQUESTED_FROM_SELLER",
            "action": "PROVIDE_EVIDENCE",
            "date": "2026-10-20T14:02:11.000Z",
            "notes": "Synthetic request: provide tracking information.",
        }],
        "seller_response_due_date": "2026-11-09T14:02:11.000Z",
        "links": [{"href": "https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-00000001",
                   "rel": "self", "method": "GET"}],
    },
    {
        "dispute_id": "PP-D-00000002",
        "create_time": "2026-10-12T08:30:00.000Z",
        "update_time": "2026-10-19T16:45:12.000Z",
        "disputed_transactions": [{
            "seller_transaction_id": "SYNTHETIC-TXN-0002",
            "create_time": "2026-10-05T11:12:45.000Z",
            "transaction_status": "COMPLETED",
            "gross_amount": {"currency_code": "USD", "value": "125.50"},
            "seller": {"merchant_id": "SYNTHETICMERCHANT", "name": "Synthetic Demo Seller"},
            "buyer": {"name": "Synthetic Demo Person"},
            "items": [{"item_id": "SYN-LAMP-002", "item_description": "Hand-blown glass table lamp",
                       "item_quantity": "1", "partner_transaction_id": "SYNTHETIC-TXN-0002"}],
            "seller_protection_eligible": False,
        }],
        "reason": "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
        "status": "UNDER_REVIEW",
        "dispute_state": "UNDER_PAYPAL_REVIEW",
        "dispute_amount": {"currency_code": "USD", "value": "125.50"},
        "dispute_life_cycle_stage": "CHARGEBACK",
        "dispute_channel": "EXTERNAL",
        "messages": [],
        "evidences": [{
            "evidence_type": "PROOF_OF_FULFILLMENT",
            "source": "SUBMITTED_BY_SELLER",
            "action": None,
            "date": "2026-10-14T10:00:00.000Z",
            "documents": [{"name": "synthetic-receipt.pdf", "url": "https://example.invalid/synthetic"}],
        }],
        "seller_response_due_date": "2026-10-22T08:30:00.000Z",
        "links": [{"href": "https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-00000002",
                   "rel": "self", "method": "GET"}],
    },
)


def _invalid():
    raise BoundaryError(502, "provider_response_invalid")


def _text(value, pattern, *, optional=False):
    if value is None and optional:
        return None
    if type(value) is not str or pattern.fullmatch(value) is None:
        _invalid()
    return value


def _enum(value, allowed, fallback):
    if value is None:
        return fallback
    if type(value) is not str or _TOKEN.fullmatch(value) is None:
        _invalid()
    return value if value in allowed else fallback


def _money(value):
    if type(value) is not dict:
        _invalid()
    return {"currency_code": _text(value.get("currency_code"), _CURRENCY),
            "value": _text(value.get("value"), _MONEY_VALUE)}


def sanitize_dispute_summary(raw: dict) -> dict:
    """Project one provider dispute row onto the closed summary contract.

    Names, messages, links, offers and documents are never copied.
    """
    if type(raw) is not dict:
        _invalid()
    return {
        "dispute_id": _text(raw.get("dispute_id"), _DISPUTE_ID),
        "reason": _enum(raw.get("reason"), DISPUTE_REASONS, "OTHER"),
        "status": _enum(raw.get("status"), DISPUTE_STATUSES, "UNKNOWN"),
        "dispute_life_cycle_stage": _enum(raw.get("dispute_life_cycle_stage"), DISPUTE_STAGES, "UNKNOWN"),
        "dispute_state": _text(raw.get("dispute_state"), _TOKEN, optional=True),
        "dispute_amount": _money(raw.get("dispute_amount")),
        "create_time": _text(raw.get("create_time"), _TIMESTAMP),
        "update_time": _text(raw.get("update_time"), _TIMESTAMP, optional=True),
        "seller_response_due_date": _text(raw.get("seller_response_due_date"), _TIMESTAMP, optional=True),
    }


def sanitize_dispute_detail(raw: dict) -> dict:
    summary = sanitize_dispute_summary(raw)
    transactions = raw.get("disputed_transactions") or []
    if type(transactions) is not list or len(transactions) > MAX_TRANSACTIONS:
        _invalid()
    projected_transactions = []
    for row in transactions:
        if type(row) is not dict:
            _invalid()
        eligible = row.get("seller_protection_eligible")
        if eligible is not None and type(eligible) is not bool:
            _invalid()
        projected_transactions.append({
            "seller_transaction_id": _text(row.get("seller_transaction_id"), _TRANSACTION_ID),
            "transaction_status": _text(row.get("transaction_status"), _TOKEN, optional=True),
            "gross_amount": _money(row.get("gross_amount")) if row.get("gross_amount") is not None else None,
            "seller_protection_eligible": eligible,
        })
    evidences = raw.get("evidences") or []
    if type(evidences) is not list or len(evidences) > MAX_EVIDENCE_ROWS:
        _invalid()
    projected_evidences = []
    for row in evidences:
        if type(row) is not dict:
            _invalid()
        source = row.get("source")
        projected_evidences.append({
            "evidence_type": _text(row.get("evidence_type"), _TOKEN),
            "source": _enum(source, EVIDENCE_SOURCES, "UNKNOWN") if source is not None else "UNKNOWN",
            "action": _text(row.get("action"), _TOKEN, optional=True),
            "date": _text(row.get("date"), _TIMESTAMP, optional=True),
        })
    return dict(summary, dispute_channel=_text(raw.get("dispute_channel"), _TOKEN, optional=True),
                disputed_transactions=projected_transactions, evidences=projected_evidences)


def sanitize_dispute_list(raw: dict) -> list[dict]:
    if type(raw) is not dict:
        _invalid()
    items = raw.get("items")
    if items is None:
        items = []
    if type(items) is not list or len(items) > 50:
        _invalid()
    projected = [sanitize_dispute_summary(row) for row in items[:MAX_LIST_ITEMS]]
    if len({row["dispute_id"] for row in projected}) != len(projected):
        _invalid()
    return projected


def _mask(value: str) -> str:
    """Keep the browser preview free of restricted originals."""
    return "*" * max(len(value) - 3, 0) + value[-3:]


def build_provide_evidence_request(dispute_id: str, case_ref: str, restricted: dict, *, masked: bool,
                                   attachment_bytes: dict | None = None) -> dict:
    """Assemble the multipart ``provide-evidence`` request from the session draft.

    ``masked=True`` produces the browser preview: tracking numbers are masked and
    attachments are described by name, media type and byte length only.
    ``masked=False`` is used only by the server-side submit path and requires the
    original bytes, keyed by attachment id, whose SHA-256 must match the
    restricted metadata.
    """
    if type(dispute_id) is not str or _DISPUTE_ID.fullmatch(dispute_id) is None:
        raise BoundaryError(422, "schema_invalid")
    if type(restricted) is not dict:
        raise BoundaryError(422, "draft_required")
    requirements = restricted.get("requirements") or []
    proofs = restricted.get("proof_records") or []
    attachments = restricted.get("attachments") or []
    proof_by_request = {}
    for proof in proofs:
        proof_by_request.setdefault(proof["request_id"], []).append(proof)
    evidences = []
    for requirement in requirements:
        if (requirement.get("source") != "REQUESTED_FROM_SELLER" or requirement.get("action") != "PROVIDE_EVIDENCE" or
                requirement.get("requirement_state") != "STRUCTURALLY_PRESENT"):
            continue
        tracking_info = []
        for proof in proof_by_request.get(requirement["request_id"], []):
            fields = proof.get("proof_fields") or {}
            tracking = fields.get("tracking_number")
            carrier = fields.get("carrier_name")
            if type(tracking) is not str or _TRACKING.fullmatch(tracking) is None or type(carrier) is not str:
                continue
            tracking_info.append({
                "carrier_name": "OTHER",
                "carrier_name_other": carrier[:64],
                "tracking_number": _mask(tracking) if masked else tracking,
            })
        evidences.append({
            "evidence_type": requirement["provider_evidence_type"],
            "evidence_info": {"tracking_info": tracking_info},
            "notes": ("Prepared locally by PayGuard for case " + case_ref +
                      ". Human review required before any submission.")[:MAX_NOTE_LENGTH],
        })
    if not evidences:
        raise BoundaryError(422, "dispute_context_not_ready")
    files = []
    for index, attachment in enumerate(attachments, start=1):
        size = attachment.get("size_bytes")
        if type(size) is not int or size < 0:
            raise BoundaryError(422, "dispute_context_not_ready")
        part = {
            "name": f"file{index}",
            "filename": str(attachment.get("filename", ""))[:255],
            "content_type": str(attachment.get("detected_media_type", "application/octet-stream"))[:128],
            "byte_length": size,
        }
        if not masked:
            content = (attachment_bytes or {}).get(attachment.get("attachment_id"))
            if (type(content) is not bytes or len(content) != size or
                    hashlib.sha256(content).hexdigest() != attachment.get("sha256")):
                raise BoundaryError(422, "dispute_context_not_ready")
            part["content"] = content
        files.append(part)
    return {
        "method": "POST",
        "path": f"/v1/customer/disputes/{dispute_id}/provide-evidence",
        "content_type": "multipart/form-data",
        "input": {"evidences": evidences},
        "files": files,
    }


def multipart_parts(request: dict) -> dict:
    """Translate the unmasked request into httpx ``files`` parts."""
    parts = {"input": (None, json.dumps(request["input"], separators=(",", ":"), allow_nan=False), "application/json")}
    for row in request["files"]:
        parts[row["name"]] = (row["filename"], row["content"], row["content_type"])
    return parts


class DisputeReadbackService:
    """Session-bound readback and preview; the adapter owns credentials."""

    def __init__(self, store: SessionStore, adapter):
        self._store = store
        self._adapter = adapter

    def _connected(self) -> bool:
        try:
            status = self._adapter.status()
        except BoundaryError:
            return False
        return status.get("status") == "connected"

    def _evidence_class(self, live: bool) -> str:
        if not live:
            return "SYNTHETIC_FIXTURE"
        receipt = self._adapter.status().get("evidence_receipt") or {}
        return "AUTHENTIC_SANDBOX_RESPONSE" if receipt.get("evidence_class") == "AUTHENTIC_SANDBOX_RESPONSE" else "SYNTHETIC_TEST_RESPONSE"

    def _envelope(self, live: bool, readback: str) -> dict:
        return {
            "source": "paypal_sandbox" if live else "synthetic_fixture",
            "data_source_label": "Sandbox" if live else "Fixture",
            "environment": "sandbox",
            "evidence_class": self._evidence_class(live),
            "observed_at": iso(self._store._now()),
            "readback": readback,
            "provider_submission": "NOT_PERFORMED",
        }

    async def list_disputes(self, session: Session) -> dict:
        with self._store.lock:
            self._store._require_live_session(session, self._store._now())
        live = self._connected()
        if live:
            items = await self._adapter.list_disputes()
        else:
            items = [sanitize_dispute_summary(row) for row in FIXTURE_DISPUTES]
        try:
            return DisputeListResponse.model_validate(dict(self._envelope(live, "GET_LIST"), items=items)).model_dump()
        except ValidationError:
            raise BoundaryError(502, "provider_response_invalid") from None

    async def get_dispute(self, session: Session, dispute_id: str) -> dict:
        with self._store.lock:
            self._store._require_live_session(session, self._store._now())
        if type(dispute_id) is not str or _DISPUTE_ID.fullmatch(dispute_id) is None:
            raise BoundaryError(422, "schema_invalid")
        live = self._connected()
        if live:
            detail = await self._adapter.get_dispute(dispute_id)
        else:
            match = [row for row in FIXTURE_DISPUTES if row["dispute_id"] == dispute_id]
            if not match:
                raise BoundaryError(404, "dispute_not_found")
            detail = sanitize_dispute_detail(deepcopy(match[0]))
        try:
            return DisputeDetailResponse.model_validate(dict(self._envelope(live, "GET_DETAIL"), **detail)).model_dump()
        except ValidationError:
            raise BoundaryError(502, "provider_response_invalid") from None

    async def provide_evidence(self, session: Session, body: dict) -> dict:
        dispute_id = body["dispute_id"]
        case_ref = body["case_ref"]
        submit = body["submit"] is True
        with self._store.lock:
            now = self._store._now()
            self._store._require_live_session(session, now)
            self._store._expire_dispute_layers(session, now)
            case_id, _case = self._store._resolve_case_ref(session, case_ref)
            if case_id not in session.drafts or case_id not in session.restricted_evidence:
                raise BoundaryError(422, "draft_required")
            self._store._verified_restricted_digest(session, case_id)
            restricted = deepcopy(session.restricted_evidence[case_id])
            attachment_bytes = {row["attachment_id"]: row["content"]
                                for row in session.disputes[case_id].get("attachment_candidates", [])
                                if type(row.get("attachment_id")) is str and type(row.get("content")) is bytes}
        preview = build_provide_evidence_request(dispute_id, case_ref, restricted, masked=True)
        live = self._connected()
        submit_enabled = bool(self._adapter.dispute_submit_enabled())
        envelope = self._envelope(live, "PROVIDE_EVIDENCE_PREVIEW")
        result = dict(envelope, dispute_id=dispute_id, case_ref=case_ref, external_send="FROZEN",
                      submit_flag_enabled=submit_enabled, human_review_required=True, **preview)
        if submit:
            if not live or not submit_enabled:
                raise BoundaryError(503, "provider_action_frozen")
            unmasked = build_provide_evidence_request(dispute_id, case_ref, restricted, masked=False,
                                                      attachment_bytes=attachment_bytes)
            await self._adapter.provide_evidence(dispute_id, multipart_parts(unmasked))
            with self._store.lock:
                self._store._activity(session, "provide_evidence", "Dispute evidence submitted to PayPal Sandbox")
            result.update(external_send="SUBMITTED", provider_submission="PERFORMED",
                          readback="PROVIDE_EVIDENCE_SUBMITTED")
        try:
            return ProvideEvidenceResponse.model_validate(result).model_dump()
        except ValidationError:
            raise BoundaryError(500, "response_contract_failure") from None
