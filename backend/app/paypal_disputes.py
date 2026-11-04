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
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import json
import re
import secrets
from urllib.parse import urlsplit

from pydantic import ValidationError

from .schemas import (AddTrackingResponse, DisputeDetailResponse, DisputeListResponse, ProvideEvidenceResponse,
                      DISPUTE_ID_PATTERN, EVIDENCE_FILE_MAX_BYTES, EVIDENCE_MEDIA_TYPES, EVIDENCE_TOTAL_MAX_BYTES,
                      PAYPAL_CARRIERS)
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
# (r25 R3 P2) PayPal tracking schema: tracker.transaction_id is ^[a-zA-Z0-9]*$, 1-50 characters.
_TRACKER_TRANSACTION_ID = re.compile(r"[A-Za-z0-9]{1,50}")
_TRACKING = re.compile(r"[A-Za-z0-9._-]{1,64}")
MAX_TRACKING_INFO = 10
_SANDBOX_API_HOSTS = frozenset({"api-m.sandbox.paypal.com", "api.sandbox.paypal.com"})
# Free-text carrier names that mean one PayPal carrier enum value (PayPal docs r24, customer-disputes/v1 schema.json).
_CARRIER_ALIASES = {"FED_EX": "FEDEX", "FEDERAL_EXPRESS": "FEDEX", "DHL_EXPRESS": "DHL",
                    "CHUNGHWA_POST": "TW_CHUNGHWA_POST",
                    "JAPAN_POST": "JP_JAPANPOST", "JAPANPOST": "JP_JAPANPOST"}
_EXTENSIONS = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".png": "image/png",
               ".pdf": "application/pdf"}
TRACKING_PATH = "/v1/shipping/trackers-batch"
# (r30 J2 P2-1) The send dialog holds "Send to PayPal" for 3 seconds (App.jsx SEND_HOLD_SECONDS); the server holds the
# confirmation it issued for the same time, so a script that skips the dialog cannot send straight after a preview.
CONFIRM_HOLD_SECONDS = 3
# (r25 R3 P1-1) Evidence types this console can shape for provide-evidence. PayPal (customer-disputes/v1 schema.json)
# expects evidence_info for PROOF_OF_FULFILLMENT (tracking_info, minItems 1), PROOF_OF_REFUND (refund_ids) and
# PROOF_OF_RETURN; refund ids are never invented, so only PROOF_OF_FULFILLMENT with real tracking is sent. A dispute
# or case that asks for any other type is refused before any send (409 evidence_type_not_supported).
SUPPORTED_EVIDENCE_TYPES = frozenset({"PROOF_OF_FULFILLMENT"})


def unsupported_requested_types(rows) -> list[str]:
    """Evidence types requested from the seller that this console cannot shape, sorted."""
    # A case requirement carries the PayPal type as provider_evidence_type (its evidence_type is the local class).
    def kind(row):
        return row.get("provider_evidence_type") or row.get("evidence_type")
    return sorted({str(kind(row)) for row in rows or [] if type(row) is dict and
                   row.get("source") == "REQUESTED_FROM_SELLER" and kind(row) not in SUPPORTED_EVIDENCE_TYPES})
_PROVIDE_EVIDENCE_PATH = re.compile(r"/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence")


def map_carrier(name: str) -> dict:
    """Map a free-text carrier to the PayPal enum, else OTHER with carrier_name_other (PayPal docs r24)."""
    token = re.sub(r"[^A-Z0-9]+", "_", name.strip().upper()).strip("_")
    token = _CARRIER_ALIASES.get(token, token)
    if token in PAYPAL_CARRIERS:
        return {"carrier_name": token}
    return {"carrier_name": "OTHER", "carrier_name_other": name.strip()[:64] or "OTHER"}


# (r25 send guard) Disputes v1 disputed_transactions[].seller.merchant_id: ^[0-9A-Za-z]+$ ("The PayPal account ID for
# the merchant"). Kept server-side only; a response or log carries it masked (first 2 and last 4 characters).
_MERCHANT_ID = re.compile(r"[0-9A-Za-z]{1,64}")


def mask_account(value) -> str | None:
    """First 2 and last 4 characters; an id too short to mask safely shows nothing of itself."""
    if type(value) is not str or not value:
        return None
    return value[:2] + "\u2026" + value[-4:] if len(value) >= 8 else "\u2026"


def mask_dispute_id(value: str) -> str:
    """PP-D-…01: the id's type prefix and last 2 characters, enough to tell two disputes apart on screen."""
    return value[:5] + "\u2026" + value[-2:] if type(value) is str and len(value) > 8 else "\u2026"


def dispute_sellers(detail: dict) -> set:
    """The seller merchant ids of a sanitized detail's disputed transactions (an unreadable one counts as None)."""
    return {row.get("seller_merchant_id") for row in detail.get("disputed_transactions") or []}


def account_refusal(account_id, sellers: set) -> str | None:
    """(r25 send guard) Why a real send must not happen from this account to this dispute; None when it may."""
    if account_id is None:
        return "account_identity_unknown"
    if not sellers or sellers != {account_id}:
        return "dispute_not_this_account"
    return None


FIXTURE_DISPUTE_IDS = frozenset({"PP-D-00000001", "PP-D-00000002"})


def _stamp(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def fixture_disputes(now: datetime) -> tuple[dict, ...]:
    """Synthetic disputes in the public PayPal Disputes API JSON shape.

    Dates are offsets from ``now`` (the request time), so the response windows
    never expire as the calendar moves. Identifiers, amounts and names are
    invented; they correspond to no PayPal account.
    """
    return (
        {
            "dispute_id": "PP-D-00000001",
            "create_time": _stamp(now - timedelta(days=2)),
            "update_time": _stamp(now - timedelta(hours=6)),
            "disputed_transactions": [{
                "seller_transaction_id": "SYNTHETICTXN0001",
                "create_time": _stamp(now - timedelta(days=6)),
                "transaction_status": "COMPLETED",
                "gross_amount": {"currency_code": "USD", "value": "48.00"},
                "seller": {"merchant_id": "SYNTHETICMERCHANT", "name": "Synthetic Demo Seller"},
                "buyer": {"name": "Synthetic Demo Person"},
                "items": [{"item_id": "SYN-CUP-001", "item_description": "Handcrafted ceramic coffee cup, set of two",
                           "item_quantity": "1", "partner_transaction_id": "SYNTHETICTXN0001"}],
                "seller_protection_eligible": True,
            }],
            "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
            "status": "WAITING_FOR_SELLER_RESPONSE",
            "dispute_state": "REQUIRED_ACTION",
            "dispute_amount": {"currency_code": "USD", "value": "48.00"},
            "dispute_life_cycle_stage": "INQUIRY",
            "dispute_channel": "INTERNAL",
            "messages": [{"posted_by": "BUYER", "time_posted": _stamp(now - timedelta(days=2)),
                          "content": "Synthetic buyer message: the package has not arrived."}],
            "evidences": [{
                "evidence_type": "PROOF_OF_FULFILLMENT",
                "source": "REQUESTED_FROM_SELLER",
                "action": "PROVIDE_EVIDENCE",
                "date": _stamp(now - timedelta(days=2)),
                "notes": "Synthetic request: provide tracking information.",
            }],
            "seller_response_due_date": _stamp(now + timedelta(days=7)),
            "links": [{"href": "https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-00000001",
                       "rel": "self", "method": "GET"},
                      {"href": "https://api-m.sandbox.paypal.com/v1/customer/disputes/PP-D-00000001/provide-evidence",
                       "rel": "provide_evidence", "method": "POST"}],
        },
        {
            "dispute_id": "PP-D-00000002",
            "create_time": _stamp(now - timedelta(days=9)),
            "update_time": _stamp(now - timedelta(days=1)),
            "disputed_transactions": [{
                "seller_transaction_id": "SYNTHETICTXN0002",
                "create_time": _stamp(now - timedelta(days=16)),
                "transaction_status": "COMPLETED",
                "gross_amount": {"currency_code": "USD", "value": "125.50"},
                "seller": {"merchant_id": "SYNTHETICMERCHANT", "name": "Synthetic Demo Seller"},
                "buyer": {"name": "Synthetic Demo Person"},
                "items": [{"item_id": "SYN-LAMP-002", "item_description": "Hand-blown glass table lamp",
                           "item_quantity": "1", "partner_transaction_id": "SYNTHETICTXN0002"}],
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
                "date": _stamp(now - timedelta(days=7)),
                "documents": [{"name": "synthetic-receipt.pdf", "url": "https://example.invalid/synthetic"}],
            }],
            "seller_response_due_date": _stamp(now + timedelta(days=5)),
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


def _offers_provide_evidence(raw: dict, dispute_id: str) -> bool:
    """True when the detail carries PayPal's provide_evidence link for this dispute.

    PayPal docs r24 (customer-disputes/v1 schema.json): "In case the link is not present in the response, you can't
    provide evidence". Only this boolean is kept; the link itself is never copied.
    """
    links = raw.get("links")
    if type(links) is not list:
        return False
    for link in links[:32]:
        if type(link) is not dict or link.get("rel") != "provide_evidence" or type(link.get("href")) is not str:
            continue
        try:
            parts = urlsplit(link["href"])
        except ValueError:
            continue
        # The detail was read by its id (and that id is checked), so the link's own id is not compared again.
        if (parts.scheme == "https" and parts.hostname in _SANDBOX_API_HOSTS and
                _PROVIDE_EVIDENCE_PATH.fullmatch(parts.path)):
            return True
    return False


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
        seller = row.get("seller")
        merchant_id = seller.get("merchant_id") if type(seller) is dict else None
        projected_transactions.append({
            "seller_transaction_id": _text(row.get("seller_transaction_id"), _TRANSACTION_ID),
            # Server-side only (stripped before any response): the send guard compares it with the connected account.
            "seller_merchant_id": merchant_id if type(merchant_id) is str and _MERCHANT_ID.fullmatch(merchant_id) else None,
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
                disputed_transactions=projected_transactions, evidences=projected_evidences,
                provide_evidence_link=_offers_provide_evidence(raw, summary["dispute_id"]))


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
    # (r25 R3 P1-1) A requested type this console cannot shape stops the whole request: sending only part of what
    # PayPal asks for would be refused (submit_refusal), and an empty or invented evidence_info is never sent.
    if unsupported_requested_types([row for row in requirements if type(row) is dict and
                                    row.get("action") == "PROVIDE_EVIDENCE"]):
        raise BoundaryError(409, "evidence_type_not_supported")
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
            tracking_info.append(dict(map_carrier(carrier), tracking_number=_mask(tracking) if masked else tracking))
        # PayPal docs r24: PROOF_OF_FULFILLMENT needs 1-10 tracking_info items; an empty one is not sent at all.
        if requirement["provider_evidence_type"] not in SUPPORTED_EVIDENCE_TYPES:
            raise BoundaryError(409, "evidence_type_not_supported")
        if not tracking_info:
            continue
        if len(tracking_info) > MAX_TRACKING_INFO:
            raise BoundaryError(422, "dispute_context_not_ready")
        evidences.append({
            "evidence_type": requirement["provider_evidence_type"],
            "evidence_info": {"tracking_info": tracking_info},
            # In the seller's voice and without the tool's name or the local case_ref: this note reaches PayPal (Q29).
            "notes": "Shipment tracking for this order, provided by the seller."[:MAX_NOTE_LENGTH],
        })
    if not evidences:
        raise BoundaryError(422, "evidence_not_ready")
    files = []
    total = 0
    for index, attachment in enumerate(attachments, start=1):
        size = attachment.get("size_bytes")
        if type(size) is not int or size < 0:
            raise BoundaryError(422, "dispute_context_not_ready")
        filename = str(attachment.get("filename", ""))[:255]
        media_type = str(attachment.get("detected_media_type", "application/octet-stream"))[:128]
        extension = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""
        total += size
        # PayPal docs r24 (supported-file-types-sizes): JPG/JPEG/GIF/PNG/PDF only, each under 10 MB, 50 MB per call.
        if (media_type not in EVIDENCE_MEDIA_TYPES or _EXTENSIONS.get(extension) != media_type or
                size >= EVIDENCE_FILE_MAX_BYTES or total > EVIDENCE_TOTAL_MAX_BYTES):
            raise BoundaryError(422, "evidence_file_rejected")
        part = {
            "name": f"file{index}",
            "filename": filename,
            "content_type": media_type,
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


def _same_money(left, right) -> bool:
    if type(left) is not dict or type(right) is not dict:
        return False
    try:
        return (left.get("currency_code") == right.get("currency_code") and
                Decimal(str(left.get("value"))) == Decimal(str(right.get("value"))))
    except (InvalidOperation, TypeError, ValueError):
        return False


_MONEY_TEXT = re.compile(r"^[A-Z]{3} [0-9]{1,15}(?:\.[0-9]{1,6})?$")


def _money_text(amount) -> str:
    """(r35 #6) "158.00 TWD"-style text for a refusal message; anything off-pattern reads "unknown"."""
    if type(amount) is not dict:
        return "unknown"
    code, value = amount.get("currency_code"), amount.get("value")
    if type(code) is not str or type(value) is not str or _MONEY_TEXT.fullmatch(f"{code} {value}") is None:
        return "unknown"
    return f"{value} {code}"


class DisputeAmountMismatch(BoundaryError):
    """(r35 #6) 409 dispute_amount_mismatch with both amounts in its message (main.py boundary_handler reads
    public_message only from this class; both parts are pattern-checked by _money_text)."""

    def __init__(self, dispute_amount, case_amount):
        super().__init__(409, "dispute_amount_mismatch")
        self.public_message = (f"The dispute amount in PayPal ({_money_text(dispute_amount)}) differs from the selected "
                               f"case's amount ({_money_text(case_amount)}). Select the case it belongs to. "
                               "Nothing was sent.")


def evidence_readiness(detail: dict) -> dict:
    """(r35 #2, E1 P1-1) What a detail read says about sending evidence now; kept per session and dispute."""
    return {
        "status": detail.get("status"),
        "offered": detail.get("provide_evidence_link") is True,
        "seller_submitted": any(type(row) is dict and row.get("source") == "SUBMITTED_BY_SELLER"
                                for row in detail.get("evidences") or []),
    }


def readiness_refusal(readiness) -> str | None:
    """(r35 #2) Why the session's last detail read already rules out an evidence send; None when it does not.
    PayPal docs r24 (customer-disputes/v1): evidence only while WAITING_FOR_SELLER_RESPONSE with a provide_evidence
    link. Seller evidence PayPal already lists is named first, so the console can say so instead of offering a send."""
    if type(readiness) is not dict:
        return "dispute_detail_required"
    if readiness.get("seller_submitted"):
        return "seller_evidence_already_submitted"
    if readiness.get("status") != "WAITING_FOR_SELLER_RESPONSE":
        return "dispute_not_awaiting_seller"
    if readiness.get("offered") is not True:
        return "dispute_evidence_not_offered"
    return None


def submit_refusal(fresh: dict, case_reason, case_amount, evidence_input: dict) -> str | None:
    """Why a provide-evidence send must not happen, read from a fresh GET of the dispute; None when it may.

    PayPal docs r24 (customer-disputes/v1 schema.json): evidence is accepted only while the dispute is
    WAITING_FOR_SELLER_RESPONSE and only when the detail carries a provide_evidence link.
    """
    if fresh.get("status") != "WAITING_FOR_SELLER_RESPONSE":
        return "dispute_not_awaiting_seller"
    if fresh.get("provide_evidence_link") is not True:
        return "dispute_evidence_not_offered"
    if fresh.get("reason") != case_reason:
        return "dispute_case_mismatch"
    if not _same_money(fresh.get("dispute_amount"), case_amount):
        return "dispute_amount_mismatch"
    if unsupported_requested_types(fresh.get("evidences")):
        return "evidence_type_not_supported"
    requested = {row["evidence_type"] for row in fresh.get("evidences") or [] if row.get("source") == "REQUESTED_FROM_SELLER"}
    sent = {row["evidence_type"] for row in evidence_input.get("evidences") or []}
    # Never an empty or non-fulfillment evidence_info (PayPal tracking_info minItems 1).
    if any(row.get("evidence_type") not in SUPPORTED_EVIDENCE_TYPES or
           not (row.get("evidence_info") or {}).get("tracking_info") for row in evidence_input.get("evidences") or []):
        return "evidence_type_not_supported"
    if requested - sent:
        return "dispute_evidence_incomplete"
    return None


def build_tracking_request(transaction_id: str, restricted: dict, *, masked: bool) -> dict:
    """One tracker for /v1/shipping/trackers-batch from the case's first valid tracking proof (PayPal docs r24)."""
    if type(transaction_id) is not str or _TRACKER_TRANSACTION_ID.fullmatch(transaction_id) is None:
        raise BoundaryError(409, "dispute_detail_required")
    for proof in (restricted.get("proof_records") or []) if type(restricted) is dict else []:
        fields = proof.get("proof_fields") or {}
        tracking, carrier = fields.get("tracking_number"), fields.get("carrier_name")
        if type(tracking) is not str or _TRACKING.fullmatch(tracking) is None or type(carrier) is not str:
            continue
        mapped = map_carrier(carrier)
        tracker = {"transaction_id": _mask(transaction_id) if masked else transaction_id,
                   "tracking_number": _mask(tracking) if masked else tracking,
                   "status": "SHIPPED", "carrier": mapped["carrier_name"]}
        if "carrier_name_other" in mapped:
            tracker["carrier_name_other"] = mapped["carrier_name_other"]
        return {"method": "POST", "path": TRACKING_PATH, "content_type": "application/json",
                "body": {"trackers": [tracker]}}
    raise BoundaryError(422, "dispute_context_not_ready")


# (optimise r24) Exact-payload hash. A placeholder id stands in for the dispute and the transaction when the approval
# records its hash: the hashed parts (evidence input and files; tracker without its transaction id) do not depend on
# them, and the fresh read before a send still checks the real dispute and transaction.
_HASH_DISPUTE_ID = "PP-PAYLOAD-HASH"
_HASH_TRANSACTION_ID = "PAYLOADHASH"


def _payload_key(session: Session) -> bytes:
    # Keyed per session, so the hash shown in the preview cannot be used to guess a masked tracking number offline.
    return hmac.new(session.token_key, b"payguard-payload-sha256-v1", hashlib.sha256).digest()


def _keyed_sha256(session: Session, document) -> str:
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hmac.new(_payload_key(session), canonical.encode("ascii"), hashlib.sha256).hexdigest()


def evidence_payload_sha256(session: Session, unmasked: dict) -> str:
    """(optimise r24) HMAC-SHA256 (session key) over the exact multipart parts a send would carry: the input part's
    JSON text exactly as sent, and each file's part name, filename, media type, byte length and SHA-256 of its bytes."""
    parts = multipart_parts(unmasked)
    files = [{"part": name, "filename": value[0], "content_type": value[2], "byte_length": len(value[1]),
              "sha256": hashlib.sha256(value[1]).hexdigest()}
             for name, value in parts.items() if name != "input"]
    return _keyed_sha256(session, {"kind": "provide_evidence", "input": parts["input"][1], "files": files})


def tracking_payload_sha256(session: Session, unmasked: dict) -> str:
    """(optimise r24) HMAC-SHA256 (session key) over the exact trackers-batch JSON body a send would carry."""
    return _keyed_sha256(session, {"kind": "add_tracking", "body": unmasked["body"]})


def tracking_content_sha256(session: Session, unmasked: dict) -> str:
    """The same body without the transaction id: what the seller approved for this case before any dispute was read.
    The transaction id itself is held to the fresh read of the dispute before a send."""
    trackers = [{key: value for key, value in tracker.items() if key != "transaction_id"}
                for tracker in unmasked["body"]["trackers"]]
    return _keyed_sha256(session, {"kind": "add_tracking_content", "trackers": trackers})


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
        # Dispute ids this session has read, per data source. A preview or submit
        # may only name an id the console itself returned for the current source.
        self._seen: dict[str, dict[str, set]] = {}
        # Provider reason and amount of each Sandbox dispute this session read; evidence may only go to a dispute whose
        # reason matches the local case it was prepared for (review r7).
        self._reasons: dict[str, dict[str, str]] = {}
        self._amounts: dict[str, dict[str, dict | None]] = {}
        # One dispute <-> one case per session (review r7b): the first preview pairs them and the pair is kept, so one
        # case's evidence never reaches two disputes and one dispute never receives two cases' evidence.
        self._bindings: dict[str, dict[str, str]] = {}
        # Seller transaction id of each dispute this session read in detail (the tracking target), and the
        # (review gate, case) pairs whose tracking was already sent: one approval, one tracking send. "Reset demo"
        # replaces the session's review gate, so only a new review after a reset can send tracking again.
        self._transactions: dict[str, dict[str, str | None]] = {}
        self._tracking_sent: dict[str, list] = {}
        # (r25 R3 P1-1) Requested evidence types each read dispute asks for that this console cannot shape.
        self._unsupported: dict[str, dict[str, list]] = {}
        # (r25 send guard) Seller merchant ids of each read dispute (server-side only; masked in responses).
        self._sellers: dict[str, dict[str, set]] = {}
        # (r30 J2 P2-1) The latest send confirmation per (kind, dispute): (token, case id, payload hash, issued at,
        # review gate). A preview replaces it, a send consumes it under the store lock; a send without the latest one is
        # refused. (r31 J2 J5) "Reset demo" replaces the gate, so it also ends every confirmation issued before it.
        # (r35 #5, E1 P2-2) The tuple also holds the approval record itself (session.approved_payloads[case_id], a new
        # object per review), so a re-draft and re-review ends older confirmations even without "Reset demo".
        self._confirmations: dict[str, dict[tuple, tuple]] = {}
        # (r35 #2, E1 P1-1) Status, provide_evidence link and seller-submitted flag of each dispute's latest detail read.
        self._readiness: dict[str, dict[str, dict]] = {}
        # (optimise r24) The local approval records the payload hashes it approved; a send is held to them.
        hooks = getattr(store, "approval_hooks", None)
        if isinstance(hooks, dict):
            hooks["paypal_payloads"] = self._approval_payloads

    @staticmethod
    def _attachment_bytes(session: Session, case_id: str) -> dict:
        return {row["attachment_id"]: row["content"]
                for row in (session.disputes.get(case_id) or {}).get("attachment_candidates", [])
                if type(row.get("attachment_id")) is str and type(row.get("content")) is bytes}

    def _approval_payloads(self, session: Session, case_id: str) -> dict:
        """(optimise r24) Called by SessionStore.approve under the store lock: the hashes of what this approval covers.
        None for a payload the case cannot build yet; a send then answers 409 and needs a new review."""
        restricted = deepcopy(session.restricted_evidence.get(case_id))
        approved = {"provide_evidence": None, "add_tracking": None}
        try:
            approved["provide_evidence"] = evidence_payload_sha256(session, build_provide_evidence_request(
                _HASH_DISPUTE_ID, "", restricted, masked=False, attachment_bytes=self._attachment_bytes(session, case_id)))
        except BoundaryError:
            pass
        try:
            approved["add_tracking"] = tracking_content_sha256(
                session, build_tracking_request(_HASH_TRANSACTION_ID, restricted, masked=False))
        except BoundaryError:
            pass
        return approved

    @staticmethod
    def _approved_hash(session: Session, case_id: str, kind: str):
        return (getattr(session, "approved_payloads", None) or {}).get(case_id, {}).get(kind)

    def _remember(self, session: Session, source: str, ids, reasons: dict[str, str] | None = None,
                  amounts: dict[str, dict | None] | None = None) -> None:
        for table in (self._seen, self._reasons, self._amounts, self._bindings, self._transactions, self._tracking_sent,
                      self._unsupported, self._sellers, self._readiness):
            for stale in [key for key in table if key not in self._store.sessions]:
                del table[stale]
        if reasons:
            self._reasons.setdefault(session.session_id, {}).update(reasons)
        if amounts:
            self._amounts.setdefault(session.session_id, {}).update(amounts)
        self._seen.setdefault(session.session_id, {}).setdefault(source, set()).update(ids)

    def _known(self, session: Session, live: bool, dispute_id: str) -> bool:
        if not live:
            return dispute_id in FIXTURE_DISPUTE_IDS
        return dispute_id in self._seen.get(session.session_id, {}).get("paypal_sandbox", set())

    def _provider_amount(self, session: Session, live: bool, dispute_id: str) -> dict | None:
        if not live:
            match = [row for row in fixture_disputes(self._store._now()) if row["dispute_id"] == dispute_id]
            return match[0].get("dispute_amount") if match else None
        return self._amounts.get(session.session_id, {}).get(dispute_id)

    def _provider_reason(self, session: Session, live: bool, dispute_id: str) -> str | None:
        if not live:
            match = [row for row in fixture_disputes(self._store._now()) if row["dispute_id"] == dispute_id]
            return match[0]["reason"] if match else None
        return self._reasons.get(session.session_id, {}).get(dispute_id)

    def _unsupported_types(self, session: Session, live: bool, dispute_id: str) -> list:
        if not live:
            match = [row for row in fixture_disputes(self._store._now()) if row["dispute_id"] == dispute_id]
            return unsupported_requested_types(match[0].get("evidences")) if match else []
        return self._unsupported.get(session.session_id, {}).get(dispute_id) or []

    def _account_id(self, live: bool):
        if not live:
            return None
        reader = getattr(self._adapter, "account_merchant_id", None)
        try:
            value = reader() if callable(reader) else None
        except BoundaryError:
            return None
        return value if type(value) is str and _MERCHANT_ID.fullmatch(value) else None

    def _send_guard(self, session: Session, live: bool, dispute_id: str, case_id: str, case_ref: str,
                    case_reason, dispute_amount, sellers=None) -> dict:
        """(r25 send guard) What a send would carry and to whom, all masked, for the console's side-by-side check."""
        if sellers is None:
            if live:
                sellers = self._sellers.get(session.session_id, {}).get(dispute_id) or set()
            else:
                match = [row for row in fixture_disputes(self._store._now()) if row["dispute_id"] == dispute_id]
                sellers = dispute_sellers(sanitize_dispute_detail(deepcopy(match[0]))) if match else set()
        account_id = self._account_id(live)
        refusal = account_refusal(account_id, sellers)
        if account_id is not None and not sellers:
            refusal = "dispute_detail_required"  # the seller is read with the dispute's details
        bound = [other for other, pair in self._bindings.get(session.session_id, {}).items() if pair[0] == case_id]
        single = next(iter(sellers)) if len(sellers) == 1 else None
        return {
            "case_ref": case_ref,
            "case_reason": case_reason,
            "dispute_masked": mask_dispute_id(dispute_id),
            "dispute_reason": self._provider_reason(session, live, dispute_id),
            "dispute_amount": deepcopy(dispute_amount),
            "bound_dispute_masked": mask_dispute_id(bound[0]) if bound else None,
            "sending_account_masked": mask_account(account_id),
            "dispute_seller_masked": mask_account(single),
            "account_status": ("UNKNOWN" if account_id is None or not sellers else
                               "MATCH" if refusal is None else "MISMATCH"),
            "send_refusal": refusal,
        }

    def _issue_confirmation(self, session: Session, kind: str, dispute_id: str, case_id: str, payload_sha256, now,
                            sendable: bool):
        """(r30 J2 P2-1) Called under the store lock by a preview. (r31 J2 J5) Issued only when this send could go out
        now (Sandbox connected, send switch on, case reviewed, payload built); otherwise the old one is dropped too."""
        # Sessions the store expired or evicted take their confirmations with them.
        for gone in [key for key in self._confirmations if key not in self._store.sessions]:
            del self._confirmations[gone]
        if payload_sha256 is None or not sendable:
            self._confirmations.get(session.session_id, {}).pop((kind, dispute_id), None)
            return None
        token = secrets.token_urlsafe(24)
        self._confirmations.setdefault(session.session_id, {})[(kind, dispute_id)] = (
            token, case_id, payload_sha256, now, session.gate, self._approval_record(session, case_id))
        return token

    @staticmethod
    def _approval_record(session: Session, case_id: str):
        return (getattr(session, "approved_payloads", None) or {}).get(case_id)

    def _confirmation_refusal(self, session: Session, kind: str, dispute_id: str, case_id: str, payload_sha256,
                              token, now) -> str | None:
        """(r30 J2 P2-1) Called under the store lock; the send consumes the confirmation only after every check passed."""
        if not token:
            return "confirmation_required"
        held = self._confirmations.get(session.session_id, {}).get((kind, dispute_id))
        if (held is None or not hmac.compare_digest(held[0], token) or held[1] != case_id or payload_sha256 is None
                or not hmac.compare_digest(held[2], payload_sha256) or held[4] is not session.gate
                or held[5] is None or held[5] is not self._approval_record(session, case_id)):
            return "confirmation_invalid"
        if now - held[3] < timedelta(seconds=CONFIRM_HOLD_SECONDS):
            return "confirmation_too_early"
        return None

    def _check_binding(self, session: Session, dispute_id: str, case_id: str) -> dict:
        """(review r7b, r25 R5 P1-1) One dispute <-> one case per session, for evidence and tracking alike.

        Refuses (409 dispute_case_bound) a dispute paired with another current case, and a case paired with another
        dispute. Stale pairs (the bound case was reset or re-drafted) do not block. Called under the store lock;
        returns the session's binding table so the caller records the pair once every other check passed."""
        bindings = self._bindings.setdefault(session.session_id, {})

        def current(bound):
            bound_case, bound_digest = bound
            try:
                return self._store._verified_restricted_digest(session, bound_case) == bound_digest
            except BoundaryError:
                return False

        bound = bindings.get(dispute_id)
        if bound is not None and bound[0] != case_id and current(bound):
            raise BoundaryError(409, "dispute_case_bound")
        if any(other != dispute_id and pair[0] == case_id and current(pair) for other, pair in bindings.items()):
            raise BoundaryError(409, "dispute_case_bound")
        for other in [other for other, pair in bindings.items() if pair[0] == case_id and other != dispute_id]:
            del bindings[other]  # a stale pair of this case
        return bindings

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

    def _envelope(self, live: bool, readback: str, debug_id=None) -> dict:
        return {
            "paypal_debug_id": debug_id if live else None,
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
        debug_id = None
        if live:
            items = await self._adapter.list_disputes()
            debug_id = getattr(self._adapter, "last_debug_id", None)
        else:
            items = [sanitize_dispute_summary(row) for row in fixture_disputes(self._store._now())]
        if live:
            self._remember(session, "paypal_sandbox", [row["dispute_id"] for row in items],
                           {row["dispute_id"]: row["reason"] for row in items},
                           {row["dispute_id"]: row.get("dispute_amount") for row in items})
        try:
            return DisputeListResponse.model_validate(dict(self._envelope(live, "GET_LIST", debug_id), items=items)).model_dump()
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
            match = [row for row in fixture_disputes(self._store._now()) if row["dispute_id"] == dispute_id]
            if not match:
                raise BoundaryError(404, "dispute_not_found")
            detail = sanitize_dispute_detail(deepcopy(match[0]))
        detail = dict(detail)
        debug_id = detail.pop("paypal_debug_id", None)
        readiness = evidence_readiness(detail)  # (r35 #2) read before the link flag is dropped from the response
        detail.pop("provide_evidence_link", None)
        sellers = dispute_sellers(detail)
        detail["disputed_transactions"] = [{key: value for key, value in row.items() if key != "seller_merchant_id"}
                                           for row in detail.get("disputed_transactions") or []]
        if live:
            self._remember(session, "paypal_sandbox", [dispute_id], {dispute_id: detail["reason"]},
                           {dispute_id: detail.get("dispute_amount")})
            transactions = detail.get("disputed_transactions") or []
            self._transactions.setdefault(session.session_id, {})[dispute_id] = (
                transactions[0]["seller_transaction_id"] if len(transactions) == 1 else None)
            self._unsupported.setdefault(session.session_id, {})[dispute_id] = unsupported_requested_types(
                detail.get("evidences"))
            self._sellers.setdefault(session.session_id, {})[dispute_id] = sellers
            self._readiness.setdefault(session.session_id, {})[dispute_id] = readiness
        try:
            return DisputeDetailResponse.model_validate(dict(self._envelope(live, "GET_DETAIL", debug_id), **detail)).model_dump()
        except ValidationError:
            raise BoundaryError(502, "provider_response_invalid") from None

    async def provide_evidence(self, session: Session, body: dict) -> dict:
        dispute_id = body["dispute_id"]
        case_ref = body["case_ref"]
        submit = body["submit"] is True
        confirm_token = body.get("confirm_token")
        live = self._connected()
        if not self._known(session, live, dispute_id):
            raise BoundaryError(404, "dispute_not_found")
        submit_enabled = bool(self._adapter.dispute_submit_enabled())
        with self._store.lock:
            now = self._store._now()
            self._store._require_live_session(session, now)
            self._store._expire_dispute_layers(session, now)
            case_id, _case = self._store._resolve_case_ref(session, case_ref)
            if case_id not in session.drafts or case_id not in session.restricted_evidence:
                raise BoundaryError(422, "draft_required")
            if self._provider_reason(session, live, dispute_id) != session.drafts[case_id].get("routing", {}).get("reason"):
                raise BoundaryError(409, "dispute_case_mismatch")
            # Fixture disputes carry the same amount as the synthetic case they stand for, so the amount must match too.
            if not live and self._provider_amount(session, live, dispute_id) != _case.get("dispute_amount"):
                raise BoundaryError(409, "dispute_case_mismatch")
            digest = self._store._verified_restricted_digest(session, case_id)
            # The pair is written only after every check above passed (review r8), and it remembers the case's evidence
            # digest: a pair whose case was reset or re-drafted no longer blocks, so a mistaken first pick can be undone
            # with "Reset demo" instead of locking the right pair out for the session.
            bindings = self._check_binding(session, dispute_id, case_id)
            # (r25 R3 P1-1) The preview shows the same refusal a send would get from the dispute's requested types.
            if self._unsupported_types(session, live, dispute_id):
                raise BoundaryError(409, "evidence_type_not_supported")
            restricted = deepcopy(session.restricted_evidence[case_id])
            attachment_bytes = self._attachment_bytes(session, case_id)
            # Built before the pair is written, so a case with nothing PayPal would accept does not take the dispute.
            preview = build_provide_evidence_request(dispute_id, case_ref, restricted, masked=True)
            # (r35 #6) A live Sandbox dispute is held to the case amount at preview too (the amount this session read),
            # so a 158 TWD dispute never pairs with a 48 USD case; the message names both amounts. After the pair, type and
            # evidence-shape checks, so a dispute taken by another case or a case with nothing to send still says so first.
            if live and not _same_money(self._provider_amount(session, live, dispute_id), _case.get("dispute_amount")):
                raise DisputeAmountMismatch(self._provider_amount(session, live, dispute_id), _case.get("dispute_amount"))
            # (optimise r24) The hash of the exact parts a send would carry (None while the files cannot be assembled).
            try:
                payload_sha256 = evidence_payload_sha256(session, build_provide_evidence_request(
                    dispute_id, case_ref, restricted, masked=False, attachment_bytes=attachment_bytes))
            except BoundaryError:
                payload_sha256 = None
            # (r35 #2, E1 P1-1) A live dispute whose last detail read rules out a send (seller evidence already listed,
            # not waiting for the seller, no provide_evidence link, or no detail read) keeps the preview but gets no
            # confirmation and no pair, so the console never offers a send PayPal would refuse.
            not_ready = readiness_refusal(self._readiness.get(session.session_id, {}).get(dispute_id)) if live else None
            if not_ready is None:
                bindings[dispute_id] = (case_id, digest)
            guard = self._send_guard(session, live, dispute_id, case_id, case_ref,
                                     session.drafts[case_id].get("routing", {}).get("reason"),
                                     self._provider_amount(session, live, dispute_id))
            if not_ready is not None:
                guard["send_refusal"] = not_ready
            if submit:
                if case_id not in session.approved:
                    raise BoundaryError(422, "approval_required")
                if not live or not submit_enabled:
                    raise BoundaryError(503, "provider_action_frozen")
                if not_ready is not None:
                    raise BoundaryError(409, not_ready)
                # Built before the approval is consumed, so a request that cannot be assembled does not use it up.
                unmasked = build_provide_evidence_request(dispute_id, case_ref, restricted, masked=False,
                                                          attachment_bytes=attachment_bytes)
                if case_id in session.submitted:
                    raise BoundaryError(409, "evidence_already_submitted")
                # (optimise r24) The freshly built payload must be the one the approval recorded.
                payload_sha256 = evidence_payload_sha256(session, unmasked)
                approved_sha256 = self._approved_hash(session, case_id, "provide_evidence")
                if approved_sha256 is None or not hmac.compare_digest(approved_sha256, payload_sha256):
                    raise BoundaryError(409, "evidence_changed_after_approval")
                case_reason = session.drafts[case_id].get("routing", {}).get("reason")
                # (r35 #6) Live and fixture alike: the fresh read must still carry the case amount (which the amount
                # this session read already matched above), so the send stops if the dispute changed since the preview.
                case_amount = deepcopy(_case.get("dispute_amount"))
                # Checked before the fresh read, so a send without the dialog's confirmation never reaches PayPal.
                refusal = self._confirmation_refusal(session, "provide_evidence", dispute_id, case_id, payload_sha256,
                                                     confirm_token, now)
                if refusal is not None:
                    raise BoundaryError(409, refusal)
                issued = None
            else:
                issued = self._issue_confirmation(session, "provide_evidence", dispute_id, case_id, payload_sha256, now,
                                                  live and submit_enabled and case_id in session.approved
                                                  and case_id not in session.submitted and not_ready is None)
        envelope = self._envelope(live, "PROVIDE_EVIDENCE_PREVIEW")
        result = dict(envelope, dispute_id=dispute_id, case_ref=case_ref, external_send="FROZEN",
                      submit_flag_enabled=submit_enabled, human_review_required=True, payload_sha256=payload_sha256,
                      send_guard=guard, confirm_token=issued, **preview)
        if submit:
            # PayPal docs r24: read the dispute again right before sending; PayPal accepts evidence only while it waits
            # for the seller and offers the provide_evidence link, and the amount and requested types must still fit.
            fresh = await self._adapter.get_dispute(dispute_id)
            refusal = submit_refusal(fresh, case_reason, case_amount, unmasked["input"])
            if refusal == "dispute_amount_mismatch":
                raise DisputeAmountMismatch(fresh.get("dispute_amount"), case_amount)
            if refusal is not None:
                raise BoundaryError(409, refusal)
            # (r25 send guard) The fresh read's seller must be the connected account.
            refusal = account_refusal(self._account_id(live), dispute_sellers(fresh))
            if refusal is not None:
                raise BoundaryError(409, refusal)
            with self._store.lock:
                now = self._store._now()
                self._store._require_live_session(session, now)
                # One approval, one send (red team r20 D4): the approval is consumed here, under the store lock and
                # before the provider call, so a repeated or concurrent submit answers 409 and never reaches PayPal a
                # second time. A failed send keeps it consumed (no automatic retry); a new draft and a new review, or
                # "Reset demo", are needed to send again.
                if case_id not in session.approved:
                    raise BoundaryError(422, "approval_required")
                if (self._store._verified_restricted_digest(session, case_id) != digest or
                        self._bindings.get(session.session_id, {}).get(dispute_id) != (case_id, digest)):
                    raise BoundaryError(409, "dispute_case_bound")
                if case_id in session.submitted:
                    raise BoundaryError(409, "evidence_already_submitted")
                approved_sha256 = self._approved_hash(session, case_id, "provide_evidence")
                if approved_sha256 is None or not hmac.compare_digest(approved_sha256, payload_sha256):
                    raise BoundaryError(409, "evidence_changed_after_approval")
                refusal = self._confirmation_refusal(session, "provide_evidence", dispute_id, case_id, payload_sha256,
                                                     confirm_token, self._store._now())
                if refusal is not None:
                    raise BoundaryError(409, refusal)
                self._confirmations[session.session_id].pop(("provide_evidence", dispute_id))
                session.submitted.add(case_id)
            try:
                sent = await self._adapter.provide_evidence(dispute_id, multipart_parts(unmasked))
            except BaseException:
                with self._store.lock:
                    self._store._activity(session, "provide_evidence",
                                          "Dispute evidence send did not complete; the approval stays used")
                raise
            with self._store.lock:
                self._store._activity(session, "provide_evidence", "Dispute evidence submitted to PayPal Sandbox")
            result.update(external_send="SUBMITTED", provider_submission="PERFORMED",
                          readback="PROVIDE_EVIDENCE_SUBMITTED",
                          paypal_debug_id=(sent or {}).get("paypal_debug_id") if type(sent) is dict else None)
        try:
            return ProvideEvidenceResponse.model_validate(result).model_dump()
        except ValidationError:
            raise BoundaryError(500, "response_contract_failure") from None

    def _tracking_used(self, session: Session, case_id: str) -> bool:
        return any(gate is session.gate and used == case_id for gate, used in self._tracking_sent.get(session.session_id, []))

    async def add_tracking(self, session: Session, body: dict) -> dict:
        """Preview, or with every gate open send, one tracker for the disputed transaction (item not received).

        Gates for a send: a local review approval of the case, PAYGUARD_PAYPAL_TRACKING_SUBMIT=enabled, submit:true,
        a connected Sandbox adapter, and a fresh GET whose transaction, reason and amount still fit the case.
        """
        dispute_id, case_ref, submit = body["dispute_id"], body["case_ref"], body["submit"] is True
        confirm_token = body.get("confirm_token")
        live = self._connected()
        if not self._known(session, live, dispute_id):
            raise BoundaryError(404, "dispute_not_found")
        submit_enabled = bool(getattr(self._adapter, "tracking_submit_enabled", lambda: False)())
        with self._store.lock:
            now = self._store._now()
            self._store._require_live_session(session, now)
            self._store._expire_dispute_layers(session, now)
            case_id, _case = self._store._resolve_case_ref(session, case_ref)
            if case_id not in session.drafts or case_id not in session.restricted_evidence:
                raise BoundaryError(422, "draft_required")
            case_reason = session.drafts[case_id].get("routing", {}).get("reason")
            if self._provider_reason(session, live, dispute_id) != case_reason:
                raise BoundaryError(409, "dispute_case_mismatch")
            if case_reason != "MERCHANDISE_OR_SERVICE_NOT_RECEIVED":
                raise BoundaryError(409, "tracking_not_applicable")
            # (r35 #6) Same rule as provide-evidence: live or fixture, the amount this session read must be the case's.
            case_amount = deepcopy(_case.get("dispute_amount"))
            digest = self._store._verified_restricted_digest(session, case_id)
            # (r25 R5 P1-1) The same two-way binding as provide-evidence.
            bindings = self._check_binding(session, dispute_id, case_id)
            if not _same_money(self._provider_amount(session, live, dispute_id), case_amount):
                raise DisputeAmountMismatch(self._provider_amount(session, live, dispute_id), case_amount)
            if live:
                transaction_id = self._transactions.get(session.session_id, {}).get(dispute_id)
            else:
                match = [row for row in fixture_disputes(now) if row["dispute_id"] == dispute_id]
                rows = match[0]["disputed_transactions"] if match else []
                transaction_id = rows[0]["seller_transaction_id"] if len(rows) == 1 else None
            restricted = deepcopy(session.restricted_evidence[case_id])
            preview = build_tracking_request(transaction_id, restricted, masked=True)
            # (optimise r24) The hash of the exact JSON body a send to this transaction would carry.
            payload_sha256 = tracking_payload_sha256(session, build_tracking_request(transaction_id, restricted, masked=False))
            # Written once the tracker can be built and before any send, so evidence for this case can no longer go to
            # another dispute, and another case can no longer use this dispute.
            bindings[dispute_id] = (case_id, digest)
            guard = self._send_guard(session, live, dispute_id, case_id, case_ref, case_reason,
                                     self._provider_amount(session, live, dispute_id))
            if submit:
                if case_id not in session.approved:
                    raise BoundaryError(422, "approval_required")
                if not live or not submit_enabled:
                    raise BoundaryError(503, "provider_action_frozen")
                if self._tracking_used(session, case_id):
                    raise BoundaryError(409, "tracking_already_submitted")
                refusal = self._confirmation_refusal(session, "add_tracking", dispute_id, case_id, payload_sha256,
                                                     confirm_token, now)
                if refusal is not None:
                    raise BoundaryError(409, refusal)
                issued = None
            else:
                issued = self._issue_confirmation(session, "add_tracking", dispute_id, case_id, payload_sha256, now,
                                                  live and submit_enabled and case_id in session.approved
                                                  and not self._tracking_used(session, case_id))
        result = dict(self._envelope(live, "ADD_TRACKING_PREVIEW"), readback="ADD_TRACKING_PREVIEW",
                      dispute_id=dispute_id, case_ref=case_ref, external_send="FROZEN",
                      submit_flag_enabled=submit_enabled, human_review_required=True, payload_sha256=payload_sha256,
                      send_guard=guard, confirm_token=issued, **preview)
        if submit:
            fresh = await self._adapter.get_dispute(dispute_id)
            rows = fresh.get("disputed_transactions") or []
            fresh_transaction = rows[0]["seller_transaction_id"] if len(rows) == 1 else None
            if fresh_transaction is None or fresh_transaction != transaction_id:
                raise BoundaryError(409, "dispute_detail_required")
            if fresh.get("reason") != case_reason:
                raise BoundaryError(409, "dispute_case_mismatch")
            if not _same_money(fresh.get("dispute_amount"), case_amount):
                raise DisputeAmountMismatch(fresh.get("dispute_amount"), case_amount)
            refusal = account_refusal(self._account_id(live), dispute_sellers(fresh))  # (r25 send guard)
            if refusal is not None:
                raise BoundaryError(409, refusal)
            unmasked = build_tracking_request(fresh_transaction, restricted, masked=False)
            with self._store.lock:
                self._store._require_live_session(session, self._store._now())
                if case_id not in session.approved:
                    raise BoundaryError(422, "approval_required")
                if self._tracking_used(session, case_id):
                    raise BoundaryError(409, "tracking_already_submitted")
                if self._bindings.get(session.session_id, {}).get(dispute_id) != (case_id, digest):
                    raise BoundaryError(409, "dispute_case_bound")
                # (optimise r24) The tracker the approval recorded (transaction id aside, checked on the fresh read
                # above) must be the one about to be sent; the case's current evidence must still build it.
                approved_sha256 = self._approved_hash(session, case_id, "add_tracking")
                try:
                    current = build_tracking_request(fresh_transaction, deepcopy(session.restricted_evidence[case_id]),
                                                     masked=False)
                except (BoundaryError, KeyError):
                    raise BoundaryError(409, "evidence_changed_after_approval") from None
                sent_sha256 = tracking_content_sha256(session, unmasked)
                if (approved_sha256 is None or not hmac.compare_digest(approved_sha256, sent_sha256) or
                        tracking_content_sha256(session, current) != sent_sha256):
                    raise BoundaryError(409, "evidence_changed_after_approval")
                result["payload_sha256"] = tracking_payload_sha256(session, unmasked)
                refusal = self._confirmation_refusal(session, "add_tracking", dispute_id, case_id, result["payload_sha256"],
                                                     confirm_token, self._store._now())
                if refusal is not None:
                    raise BoundaryError(409, refusal)
                self._confirmations[session.session_id].pop(("add_tracking", dispute_id))
                # Consumed before the provider call; a failed send stays consumed (no automatic retry).
                self._tracking_sent.setdefault(session.session_id, []).append((session.gate, case_id))
            try:
                sent = await self._adapter.add_tracking(unmasked["body"]["trackers"][0])
            except BaseException:
                with self._store.lock:
                    self._store._activity(session, "add_tracking",
                                          "Tracking send did not complete; the approval stays used for tracking")
                raise
            with self._store.lock:
                self._store._activity(session, "add_tracking", "Tracking added to the PayPal Sandbox transaction")
            result.update(external_send="SUBMITTED", provider_submission="PERFORMED", readback="ADD_TRACKING_SUBMITTED",
                          paypal_debug_id=sent.get("paypal_debug_id") if type(sent) is dict else None)
        try:
            return AddTrackingResponse.model_validate(result).model_dump()
        except ValidationError:
            raise BoundaryError(500, "response_contract_failure") from None
