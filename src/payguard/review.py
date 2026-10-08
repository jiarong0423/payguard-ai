"""Local demo approval bound to exact payload; no external execution."""

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import hmac
import json
import secrets


def payload_digest(payload: dict) -> str:
    if not isinstance(payload, dict):
        raise ValueError("invalid_draft")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def aware_time(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timezone_required")
    return value


@dataclass(frozen=True)
class Approval:
    case_id: str
    action: str
    actor: str
    digest: str
    issued_at: str
    expires_at: str
    nonce: str
    signature: str


class LocalReviewGate:
    def __init__(self):
        self._key = secrets.token_bytes(32)
        self._used: set[str] = set()

    def _signature(self, fields: dict) -> str:
        canonical = json.dumps(fields, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        return hmac.new(self._key, canonical, hashlib.sha256).hexdigest()

    def approve(self, draft: dict, *, actor: str, now: datetime, ttl_seconds: int = 300) -> Approval:
        aware_time(now)
        if not isinstance(actor, str) or not actor.startswith("demo-") or len(actor) > 100:
            raise ValueError("synthetic_actor_required")
        if type(ttl_seconds) is not int or not 1 <= ttl_seconds <= 300:
            raise ValueError("invalid_approval_ttl")
        case_id = draft.get("case_id") if isinstance(draft, dict) else None
        if not isinstance(case_id, str) or not case_id.startswith("demo-") or len(case_id) > 100:
            raise ValueError("synthetic_case_required")
        fields = {"case_id": case_id, "action": "review_draft", "actor": actor,
                  "digest": payload_digest(draft), "issued_at": now.isoformat(),
                  "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat(),
                  "nonce": secrets.token_hex(16)}
        return Approval(**fields, signature=self._signature(fields))

    def consume(self, approval: Approval, draft: dict, *, actor: str, now: datetime, action: str = "review_draft") -> dict:
        aware_time(now)
        if not isinstance(approval, Approval):
            raise ValueError("invalid_approval")
        fields = asdict(approval)
        signature = fields.pop("signature")
        if not hmac.compare_digest(signature, self._signature(fields)):
            raise ValueError("approval_tampered")
        if action != "review_draft" or action != approval.action:
            raise ValueError("external_execution_frozen")
        if actor != approval.actor or draft.get("case_id") != approval.case_id or payload_digest(draft) != approval.digest:
            raise ValueError("approval_scope_mismatch")
        if not datetime.fromisoformat(approval.issued_at) <= now < datetime.fromisoformat(approval.expires_at):
            raise ValueError("approval_expired_or_future")
        if approval.nonce in self._used:
            raise ValueError("approval_already_used")
        self._used.add(approval.nonce)
        return {"case_id": approval.case_id, "action": action, "status": "local_draft_reviewed",
                "external_submission": "FROZEN", "authenticated_actor": False,
                "durable_approval": False}
