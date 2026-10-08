"""Deterministic two-layer dispute-evidence routing for the synthetic MVP.

The resolver accepts a closed, synthetic provider-response snapshot and
synthetic proof records. It performs no I/O, stores no file bytes, submits
nothing to a provider, and never decides a dispute. Its restricted output is
for server-side session memory only; browser consumers receive only the safe
route and restricted-layer summary.
"""

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import json
from pathlib import PurePath
import re
import unicodedata


DISPUTE_REASONS = (
    "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
    "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
    "UNAUTHORISED",
    "CREDIT_NOT_PROCESSED",
    "DUPLICATE_TRANSACTION",
    "INCORRECT_AMOUNT",
    "PAYMENT_BY_OTHER_MEANS",
    "CANCELED_RECURRING_BILLING",
    "OTHER",
)
LOCAL_EVIDENCE_TYPES = (
    "ACTIVITY", "APPROVAL", "ORDER", "FULFILLMENT", "DELIVERY",
    "DESCRIPTION", "RETURN", "REFUND", "CREDIT_BASIS", "TRANSACTION",
    "PRICE_BASIS", "OTHER_PAYMENT", "SUBSCRIPTION", "CANCELLATION",
    "LIMITATION_NOTICE", "KYC_REQUEST", "KYC_RESPONSE", "BASELINE",
    "CASE_DETAILS", "OTHER",
)
EVIDENCE_STATES = (
    "SUPPLIED_UNVERIFIED", "DOCUMENT_STATED", "PARTY_ALLEGATION",
    "ADJUDICATOR_FINDING", "NOT_STATED_IN_REVIEWED_DOCUMENT",
    "NOT_ESTABLISHED", "UNKNOWN", "NOT_APPLICABLE", "CONFLICTING_SOURCES",
)
PROVIDER_EVIDENCE_TYPE_MAP = {
    "PROOF_OF_FULFILLMENT": "FULFILLMENT",
    "PROOF_OF_REFUND": "REFUND",
    "OTHER": "OTHER",
}
REASON_PROVIDER_EVIDENCE_TYPES = {
    "MERCHANDISE_OR_SERVICE_NOT_RECEIVED": ("PROOF_OF_FULFILLMENT", "PROOF_OF_REFUND"),
    "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED": ("OTHER", "PROOF_OF_REFUND"),
    "UNAUTHORISED": ("PROOF_OF_FULFILLMENT", "PROOF_OF_REFUND", "OTHER"),
    "CREDIT_NOT_PROCESSED": ("PROOF_OF_REFUND", "OTHER"),
    "DUPLICATE_TRANSACTION": ("PROOF_OF_REFUND", "OTHER"),
    "INCORRECT_AMOUNT": ("PROOF_OF_REFUND", "OTHER"),
    "PAYMENT_BY_OTHER_MEANS": ("PROOF_OF_REFUND", "OTHER"),
    "CANCELED_RECURRING_BILLING": ("PROOF_OF_REFUND", "OTHER"),
    "OTHER": ("PROOF_OF_REFUND", "OTHER"),
}
DISPUTE_STATUSES = (
    "OPEN", "WAITING_FOR_SELLER_RESPONSE", "WAITING_FOR_BUYER_RESPONSE",
    "UNDER_REVIEW", "RESOLVED", "CLOSED", "UNKNOWN",
)
DISPUTE_STAGES = (
    "INQUIRY", "CHARGEBACK", "PRE_ARBITRATION", "ARBITRATION", "UNKNOWN",
)
SUPPORTED_ATTACHMENT_EXTENSIONS = (".jpg", ".jpeg", ".gif", ".png", ".pdf")
MAX_ATTACHMENT_BYTES = 10_000_000
MAX_ATTACHMENT_SET_BYTES = 50_000_000
MAX_ATTACHMENTS = 20

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
_UPPER_TOKEN = re.compile(r"[A-Z][A-Z0-9_]{0,127}\Z")
_CURRENCY = re.compile(r"[A-Z]{3}\Z")
_DECIMAL = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})\Z"
)
_SAFE_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._ -]{0,127}\Z")
_SIGNATURES = (
    ("image/jpeg", (".jpg", ".jpeg"), lambda body: body.startswith(b"\xff\xd8\xff")),
    ("image/gif", (".gif",), lambda body: body.startswith((b"GIF87a", b"GIF89a"))),
    ("image/png", (".png",), lambda body: body.startswith(b"\x89PNG\r\n\x1a\n")),
    ("application/pdf", (".pdf",), lambda body: body.startswith(b"%PDF-")),
)


class DisputeEvidenceError(ValueError):
    """Fixed-code validation failure that never includes caller data."""


def _error(code):
    raise DisputeEvidenceError(code)


def _closed(value, fields, code):
    if type(value) is not dict or set(value) != set(fields):
        _error(code)


def _identifier(value, code):
    if type(value) is not str or _IDENTIFIER.fullmatch(value) is None:
        _error(code)
    return value


def _upper(value, code, *, nullable=False):
    if nullable and value is None:
        return None
    if type(value) is not str or _UPPER_TOKEN.fullmatch(value) is None:
        _error(code)
    return value


def _text(value, code, maximum=4000):
    if (type(value) is not str or not value.strip() or len(value) > maximum or
            any(unicodedata.category(char).startswith("C") for char in value)):
        _error(code)
    return value


def _time(value, code):
    if type(value) is not str or _TIMESTAMP.fullmatch(value) is None:
        _error(code)
    try:
        parsed = datetime.fromisoformat(value)
    except (ValueError, OverflowError):
        _error(code)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _error(code)
    return parsed.astimezone(timezone.utc)


def _iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _decimal(value, code):
    if type(value) is not str or len(value) > 160 or _DECIMAL.fullmatch(value) is None:
        _error(code)
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        _error(code)
    if not parsed.is_finite() or parsed < 0 or len(parsed.as_tuple().digits) > 64:
        _error(code)
    return format(parsed, "f")


def _normalize_reason(value):
    if value == "INR":
        return "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
    if value not in DISPUTE_REASONS:
        _error("dispute_reason_invalid")
    return value


def _validate_snapshot(snapshot):
    fields = {
        "schema_version", "snapshot_class", "observed_at", "dispute_id",
        "order_id", "reason", "status", "dispute_life_cycle_stage",
        "seller_response_due_date", "available_actions", "evidences",
    }
    _closed(snapshot, fields, "dispute_snapshot_invalid")
    if type(snapshot["schema_version"]) is not int or snapshot["schema_version"] != 1:
        _error("dispute_snapshot_invalid")
    if snapshot["snapshot_class"] != "SYNTHETIC_PROVIDER_FIXTURE":
        _error("dispute_snapshot_invalid")
    observed = _time(snapshot["observed_at"], "dispute_snapshot_invalid")
    due = _time(snapshot["seller_response_due_date"], "dispute_due_date_invalid")
    dispute_id = _identifier(snapshot["dispute_id"], "dispute_snapshot_invalid")
    order_id = _identifier(snapshot["order_id"], "dispute_snapshot_invalid")
    reason = _normalize_reason(snapshot["reason"])
    if snapshot["status"] not in DISPUTE_STATUSES or snapshot["dispute_life_cycle_stage"] not in DISPUTE_STAGES:
        _error("dispute_snapshot_invalid")
    actions = snapshot["available_actions"]
    if type(actions) is not list or len(actions) > 20:
        _error("dispute_snapshot_invalid")
    normalized_actions = [_upper(value, "dispute_snapshot_invalid") for value in actions]
    if len(normalized_actions) != len(set(normalized_actions)):
        _error("dispute_snapshot_invalid")
    rows = snapshot["evidences"]
    if type(rows) is not list or not 1 <= len(rows) <= 20:
        _error("dispute_snapshot_invalid")
    requests = []
    request_ids = set()
    for row in rows:
        _closed(row, {"request_id", "evidence_type", "source", "mandatory", "action"},
                "dispute_snapshot_invalid")
        request_id = _identifier(row["request_id"], "dispute_snapshot_invalid")
        if request_id in request_ids:
            _error("dispute_snapshot_invalid")
        request_ids.add(request_id)
        evidence_type = _upper(row["evidence_type"], "dispute_snapshot_invalid")
        source = _upper(row["source"], "dispute_snapshot_invalid")
        action = _upper(row["action"], "dispute_snapshot_invalid", nullable=True)
        if type(row["mandatory"]) is not bool:
            _error("dispute_snapshot_invalid")
        requests.append({
            "request_id": request_id,
            "evidence_type": evidence_type,
            "source": source,
            "mandatory": row["mandatory"],
            "action": action,
        })
    return {
        "schema_version": 1,
        "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
        "observed_at": _iso(observed),
        "dispute_id": dispute_id,
        "order_id": order_id,
        "reason": reason,
        "status": snapshot["status"],
        "dispute_life_cycle_stage": snapshot["dispute_life_cycle_stage"],
        "seller_response_due_date": _iso(due),
        "available_actions": normalized_actions,
        "evidences": requests,
    }


_PROOF_FIELDS = {
    "FULFILLMENT": {
        "allowed": {"carrier_name", "tracking_number", "shipped_at", "delivered_at",
                    "delivery_status", "destination_match_status"},
        "required": {"carrier_name", "tracking_number"},
    },
    "REFUND": {
        "allowed": {"refund_id", "amount", "currency", "refunded_at"},
        "required": {"refund_id"},
    },
    "OTHER": {
        "allowed": {"notes", "product_description", "return_policy_text"},
        "required_any": {"notes", "product_description", "return_policy_text"},
    },
}


def _validate_proof_fields(evidence_type, fields):
    spec = _PROOF_FIELDS.get(evidence_type)
    if spec is None or type(fields) is not dict or not set(fields).issubset(spec["allowed"]):
        _error("proof_record_invalid")
    if not spec.get("required", set()).issubset(fields):
        _error("proof_record_invalid")
    if spec.get("required_any") and not set(fields).intersection(spec["required_any"]):
        _error("proof_record_invalid")
    result = {}
    for name, value in fields.items():
        if name in {"shipped_at", "delivered_at", "refunded_at"}:
            result[name] = _iso(_time(value, "proof_record_invalid"))
        elif name in {"amount"}:
            result[name] = _decimal(value, "proof_record_invalid")
        elif name == "currency":
            if type(value) is not str or _CURRENCY.fullmatch(value) is None:
                _error("proof_record_invalid")
            result[name] = value
        elif name in {"delivery_status", "destination_match_status"}:
            result[name] = _upper(value, "proof_record_invalid")
        elif name in {"carrier_name", "tracking_number", "refund_id"}:
            result[name] = _identifier(value, "proof_record_invalid")
        else:
            result[name] = _text(value, "proof_record_invalid")
    return result


def _validate_proofs(proof_records, requests, as_of):
    if type(proof_records) is not list or len(proof_records) > 128:
        _error("proof_record_invalid")
    request_by_id = {row["request_id"]: row for row in requests}
    result = []
    evidence_ids = set()
    for record in proof_records:
        _closed(record, {"evidence_id", "request_id", "evidence_type", "proof_fields",
                         "observed_at", "evidence_state", "attachment_ids"},
                "proof_record_invalid")
        evidence_id = _identifier(record["evidence_id"], "proof_record_invalid")
        request_id = _identifier(record["request_id"], "proof_record_invalid")
        if evidence_id in evidence_ids or request_id not in request_by_id:
            _error("proof_record_invalid")
        evidence_ids.add(evidence_id)
        evidence_type = record["evidence_type"]
        mapped = PROVIDER_EVIDENCE_TYPE_MAP.get(request_by_id[request_id]["evidence_type"])
        if evidence_type not in _PROOF_FIELDS or mapped != evidence_type:
            _error("proof_record_invalid")
        observed = _time(record["observed_at"], "proof_record_invalid")
        if observed > as_of:
            _error("proof_record_invalid")
        if record["evidence_state"] not in EVIDENCE_STATES:
            _error("proof_record_invalid")
        attachment_ids = record["attachment_ids"]
        if type(attachment_ids) is not list or len(attachment_ids) > MAX_ATTACHMENTS:
            _error("proof_record_invalid")
        normalized_attachment_ids = [_identifier(value, "proof_record_invalid") for value in attachment_ids]
        if len(normalized_attachment_ids) != len(set(normalized_attachment_ids)):
            _error("proof_record_invalid")
        result.append({
            "evidence_id": evidence_id,
            "request_id": request_id,
            "evidence_type": evidence_type,
            "proof_fields": _validate_proof_fields(evidence_type, record["proof_fields"]),
            "observed_at": _iso(observed),
            "evidence_state": record["evidence_state"],
            "attachment_ids": normalized_attachment_ids,
        })
    return result


def validate_attachment_bytes(filename, declared_media_type, content):
    """Return content-free metadata for one supported synthetic attachment."""
    if (type(filename) is not str or not filename.isascii() or
            _SAFE_FILENAME.fullmatch(filename) is None or
            filename in {".", ".."} or PurePath(filename).name != filename or ".." in filename):
        _error("attachment_name_invalid")
    if type(declared_media_type) is not str:
        _error("attachment_media_type_invalid")
    if type(content) is not bytes:
        _error("attachment_content_invalid")
    size = len(content)
    if size <= 0 or size >= MAX_ATTACHMENT_BYTES:
        _error("attachment_size_invalid")
    detected = next(((media_type, extensions) for media_type, extensions, test in _SIGNATURES
                     if test(content)), None)
    if detected is None:
        _error("attachment_signature_invalid")
    media_type, extensions = detected
    extension = PurePath(filename).suffix.casefold()
    if extension not in extensions:
        _error("attachment_extension_invalid")
    if declared_media_type != media_type:
        _error("attachment_media_type_invalid")
    return {
        "filename": filename,
        "extension": extension,
        "detected_media_type": media_type,
        "size_bytes": size,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def validate_attachment_set(candidates, evidence_ids):
    """Validate an attachment set and discard all file bytes from the result."""
    if type(candidates) is not list or len(candidates) > MAX_ATTACHMENTS:
        _error("attachment_set_invalid")
    allowed_evidence_ids = set(evidence_ids)
    result = []
    attachment_ids = set()
    total = 0
    for candidate in candidates:
        _closed(candidate, {"attachment_id", "evidence_id", "filename",
                            "declared_media_type", "content"}, "attachment_set_invalid")
        attachment_id = _identifier(candidate["attachment_id"], "attachment_set_invalid")
        evidence_id = _identifier(candidate["evidence_id"], "attachment_set_invalid")
        if attachment_id in attachment_ids or evidence_id not in allowed_evidence_ids:
            _error("attachment_set_invalid")
        attachment_ids.add(attachment_id)
        metadata = validate_attachment_bytes(candidate["filename"], candidate["declared_media_type"],
                                             candidate["content"])
        total += metadata["size_bytes"]
        if total > MAX_ATTACHMENT_SET_BYTES:
            _error("attachment_total_size_invalid")
        result.append({"attachment_id": attachment_id, "evidence_id": evidence_id, **metadata})
    return result


def _canonical_digest(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except (TypeError, ValueError, OverflowError):
        _error("restricted_evidence_invalid")
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def restricted_evidence_digest(restricted):
    """Verify and return the digest of a closed restricted evidence object."""
    if type(restricted) is not dict or type(restricted.get("sha256")) is not str:
        _error("restricted_evidence_invalid")
    stored = restricted["sha256"]
    if re.fullmatch(r"[a-f0-9]{64}", stored) is None:
        _error("restricted_evidence_invalid")
    current = _canonical_digest({key: value for key, value in restricted.items() if key != "sha256"})
    if not hmac.compare_digest(stored, current):
        _error("restricted_evidence_invalid")
    return current


def resolve_dispute_requirements(snapshot, proof_records, attachment_candidates, as_of):
    """Build restricted session metadata and a safe browser projection."""
    instant = _time(as_of, "dispute_as_of_invalid") if type(as_of) is str else as_of
    if type(instant) is not datetime or instant.tzinfo is None or instant.utcoffset() is None:
        _error("dispute_as_of_invalid")
    instant = instant.astimezone(timezone.utc)
    normalized_snapshot = _validate_snapshot(snapshot)
    if _time(normalized_snapshot["observed_at"], "dispute_snapshot_invalid") > instant:
        _error("dispute_snapshot_invalid")
    proofs = _validate_proofs(proof_records, normalized_snapshot["evidences"], instant)
    attachments = validate_attachment_set(attachment_candidates, [row["evidence_id"] for row in proofs])
    attachment_by_id = {row["attachment_id"]: row for row in attachments}
    for proof in proofs:
        if any(attachment_id not in attachment_by_id or
               attachment_by_id[attachment_id]["evidence_id"] != proof["evidence_id"]
               for attachment_id in proof["attachment_ids"]):
            _error("attachment_join_invalid")
    proof_by_request = {}
    for proof in proofs:
        proof_by_request.setdefault(proof["request_id"], []).append(proof)
    due = _time(normalized_snapshot["seller_response_due_date"], "dispute_due_date_invalid")
    due_state = "EXPIRED" if due <= instant else "OPEN"
    allowed_types = set(REASON_PROVIDER_EVIDENCE_TYPES[normalized_snapshot["reason"]])
    requirements = []
    has_manual = False
    has_missing = False
    for request in normalized_snapshot["evidences"]:
        mapped = PROVIDER_EVIDENCE_TYPE_MAP.get(request["evidence_type"])
        joined = proof_by_request.get(request["request_id"], [])
        accepted_attachment_count = sum(len(row["attachment_ids"]) for row in joined)
        if request["source"] != "REQUESTED_FROM_SELLER":
            state = "CONTEXT_ONLY"
        elif request["action"] != "PROVIDE_EVIDENCE":
            state = "CONTEXT_ONLY"
        elif mapped is None:
            state = "UNMAPPED_EVIDENCE_TYPE"
            has_manual = True
        elif request["evidence_type"] not in allowed_types:
            state = "PROVIDER_REQUEST_OUTSIDE_LOCAL_MATRIX"
            has_manual = True
        elif joined:
            state = "STRUCTURALLY_PRESENT"
        elif request["mandatory"]:
            state = "MANDATORY_EVIDENCE_MISSING"
            has_missing = True
        else:
            state = "OPTIONAL_EVIDENCE_MISSING"
        requirements.append({
            "request_id": request["request_id"],
            "provider_evidence_type": request["evidence_type"],
            "evidence_type": mapped,
            "source": request["source"],
            "mandatory": request["mandatory"],
            "action": request["action"],
            "requirement_state": state,
            "proof_count": len(joined),
            "accepted_attachment_count": accepted_attachment_count,
        })
    if normalized_snapshot["status"] in {"RESOLVED", "CLOSED"}:
        overall = "CASE_NOT_ACTIONABLE"
    elif due_state == "EXPIRED":
        overall = "DUE_DATE_EXPIRED"
    elif normalized_snapshot["status"] == "UNKNOWN" or normalized_snapshot["dispute_life_cycle_stage"] == "UNKNOWN":
        overall = "MANUAL_REVIEW"
    elif "PROVIDE_EVIDENCE" not in normalized_snapshot["available_actions"]:
        overall = "ACTION_NOT_AVAILABLE"
    elif has_manual:
        overall = "MANUAL_REVIEW"
    elif has_missing:
        overall = "NEEDS_INPUT"
    else:
        overall = "READY_FOR_LOCAL_REVIEW"
    restricted_without_digest = {
        "schema_version": 1,
        "profile": "RESTRICTED_ORIGINAL_METADATA_V1",
        "data_class": "SYNTHETIC_RESTRICTED_EVIDENCE",
        "custody": "SESSION_MEMORY_ONLY",
        "persistent_storage": "NOT_IMPLEMENTED",
        "production_pii_vault": "NOT_IMPLEMENTED",
        "provider_submission": "NOT_PERFORMED",
        "case_snapshot": normalized_snapshot,
        "requirements": requirements,
        "proof_records": proofs,
        "attachments": attachments,
        "created_at": _iso(instant),
    }
    restricted = {**restricted_without_digest, "sha256": _canonical_digest(restricted_without_digest)}
    public_requirements = [
        {**requirement, "request_id": f"requirement-{index:03d}"}
        for index, requirement in enumerate(requirements, start=1)
    ]
    routing = {
        "schema_version": 1,
        "snapshot_class": normalized_snapshot["snapshot_class"],
        "reason": normalized_snapshot["reason"],
        "status": normalized_snapshot["status"],
        "dispute_life_cycle_stage": normalized_snapshot["dispute_life_cycle_stage"],
        "seller_response_due_date": normalized_snapshot["seller_response_due_date"],
        "due_state": due_state,
        "available_actions": normalized_snapshot["available_actions"],
        "requirements": public_requirements,
        "overall_state": overall,
        "human_review_required": True,
        "provider_submission": "NOT_PERFORMED",
    }
    summary = {
        "schema_version": 1,
        "profile": "RESTRICTED_ORIGINAL_METADATA_V1",
        "data_class": "SYNTHETIC_RESTRICTED_EVIDENCE",
        "custody": "SESSION_MEMORY_ONLY",
        "persistent_storage": "NOT_IMPLEMENTED",
        "production_pii_vault": "NOT_IMPLEMENTED",
        "proof_record_count": len(proofs),
        "attachment_count": len(attachments),
        "content_returned": False,
        "provider_submission": "NOT_PERFORMED",
    }
    return {"restricted": restricted, "routing": routing, "restricted_original_summary": summary}


def internal_review_narrative(routing):
    """Create a bounded review-safe narrative without restricted identifiers."""
    _closed(routing, {"schema_version", "snapshot_class", "reason", "status",
                      "dispute_life_cycle_stage", "seller_response_due_date", "due_state",
                      "available_actions", "requirements", "overall_state",
                      "human_review_required", "provider_submission"}, "routing_invalid")
    rows = []
    for requirement in routing["requirements"]:
        rows.append(
            "type=" + str(requirement["provider_evidence_type"]) +
            ", source=" + str(requirement["source"]) +
            ", mandatory=" + str(requirement["mandatory"]).lower() +
            ", state=" + str(requirement["requirement_state"]) +
            ", attachments=" + str(requirement["accepted_attachment_count"])
        )
    return (
        "Internal pseudonymized review copy. Reason=" + routing["reason"] +
        "; lifecycle=" + routing["dispute_life_cycle_stage"] +
        "; status=" + routing["status"] +
        "; seller response due=" + routing["seller_response_due_date"] +
        "; due state=" + routing["due_state"] +
        "; overall state=" + routing["overall_state"] +
        ". Requested evidence: " + " | ".join(rows) +
        ". This JSON is not a PayPal attachment and was not submitted."
    )


def defensive_copy(value):
    """Return a deep copy for tests and bounded adapters."""
    return deepcopy(value)
