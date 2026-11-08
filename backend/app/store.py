"""Bounded, expiring synthetic sessions and payload-bound local review."""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hmac
import hashlib
import json
import math
import secrets
import threading
from types import MappingProxyType

from payguard.evidence_pdf import EvidencePdfError, evidence_pdf_for_case
from payguard.engines import assess_velocity, check_aup, prepare_dispute
from payguard.case_cards import match_cases
from payguard.dispute_evidence import (
    DisputeEvidenceError,
    build_time_evidence,
    message_digest,
    internal_review_narrative,
    restricted_evidence_digest,
    resolve_dispute_requirements,
)
from payguard.policy import POLICY_VERSION
from payguard.privacy import redact_identity
from payguard.document_privacy import redact_dispute_document
from payguard.review import LocalReviewGate, payload_digest
from pydantic import ValidationError
from .ai_brief import AiBriefRequest
from .schemas import AupResponse, DisputeDraftResponse, InvoicePayload, ScenarioMatch

AI_FACT_EVIDENCE_TYPES = ("PROOF_OF_FULFILLMENT", "PROOF_OF_REFUND")  # equals app.ai_brief.FACT_EVIDENCE_TYPES
AI_FACT_REQUIREMENT_STATES = ("STRUCTURALLY_PRESENT", "MANDATORY_EVIDENCE_MISSING", "OPTIONAL_EVIDENCE_MISSING")


def safe_equal(left: object, right: object) -> bool:
    """Constant-time equality for values that may come from a request. hmac.compare_digest raises TypeError on
    str with non-ASCII characters (a case_ref of "case-ref-\u0661\u0662\u0663" was a 500); compare UTF-8 bytes instead
    and treat anything that is not a string as unequal."""
    if type(left) is not str or type(right) is not str:
        return False
    return hmac.compare_digest(left.encode("utf-8", "surrogatepass"), right.encode("utf-8", "surrogatepass"))


DEMO_VELOCITY_BASELINE = MappingProxyType({
    "amount_per_hour": "100.00",
    "provenance": "SYNTHETIC_BASELINE",
    "comparison_hours": 24,
    "observation_hours": 1,
})
DEMO_BURST_AMOUNTS = ("4.50", "12.00", "7.25", "18.00", "9.75", "6.50", "15.00", "11.25", "8.00", "7.75")
AI_ATTEMPT_LIMIT = 3
AI_BRIEF_STAGES = frozenset({"source_compliance", "velocity_guard", "dispute_mediation"})


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


_PLACEHOLDER_PDF_PREFIX = b"%PDF-1.7\nSynthetic delivery evidence"


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


# Synthetic dispute amounts in the PayPal Disputes `dispute_amount` shape. The values are reused from
# existing synthetic fixtures, not taken from any account: 48.00 and 125.50 from
# backend/app/paypal_disputes.py fixture_disputes(), 18.00 from DEMO_BURST_AMOUNTS above.
DEMO_DISPUTE_AMOUNTS = {
    "demo-case-001": {"currency_code": "USD", "value": "48.00"},
    "demo-case-002": {"currency_code": "USD", "value": "18.00"},
    "demo-case-003": {"currency_code": "USD", "value": "125.50"},
}


def _due_soon_demo_case(anchor: datetime) -> dict:
    """Synthetic physical-goods case due in one day with one requested item still missing.

    Proof of fulfilment (tracking, delivery scan, attachment) is on file, so the case can be drafted;
    the optional proof-of-refund request has no record yet. The board marks it "due soon, evidence missing".
    """
    ordered = anchor - timedelta(days=6)
    delivered = anchor - timedelta(days=4)
    opened = anchor - timedelta(days=3)
    return {
        "case_id": "demo-case-003", "order_id": "demo-dispute-order-003", "reason": "INR",
        "order_created_at": iso(ordered), "delivered_at": iso(delivered), "opened_at": iso(opened),
        "carrier_status": "delivered", "evidence_source": "synthetic",
        "dispute_amount": dict(DEMO_DISPUTE_AMOUNTS["demo-case-003"]),
        "provider_snapshot": {
            "schema_version": 1,
            "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
            "observed_at": iso(anchor - timedelta(hours=1)),
            "dispute_id": "demo-case-003",
            "order_id": "demo-dispute-order-003",
            "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
            "status": "WAITING_FOR_SELLER_RESPONSE",
            "dispute_life_cycle_stage": "INQUIRY",
            "seller_response_due_date": iso(anchor + timedelta(days=1)),
            "available_actions": ["PROVIDE_EVIDENCE"],
            "evidences": [
                {"request_id": "demo-request-fulfillment-003", "evidence_type": "PROOF_OF_FULFILLMENT",
                 "source": "REQUESTED_FROM_SELLER", "mandatory": True, "action": "PROVIDE_EVIDENCE"},
                {"request_id": "demo-request-refund-003", "evidence_type": "PROOF_OF_REFUND",
                 "source": "REQUESTED_FROM_SELLER", "mandatory": False, "action": "PROVIDE_EVIDENCE"},
            ],
        },
        "proof_records": [{
            "evidence_id": "demo-proof-fulfillment-003",
            "request_id": "demo-request-fulfillment-003",
            "evidence_type": "FULFILLMENT",
            "proof_fields": {
                "carrier_name": "SYNTHETIC_CARRIER",
                "tracking_number": "SYNTHETIC_TRACKING_003",
                "delivered_at": iso(delivered),
                "delivery_status": "DELIVERED",
                "destination_match_status": "MATCHED",
            },
            "observed_at": iso(delivered),
            "evidence_state": "SUPPLIED_UNVERIFIED",
            "attachment_ids": ["demo-attachment-003"],
        }],
        "attachment_candidates": [{
            "attachment_id": "demo-attachment-003",
            "evidence_id": "demo-proof-fulfillment-003",
            "filename": "synthetic-delivery-003.pdf",
            "declared_media_type": "application/pdf",
            "content": b"%PDF-1.7\nSynthetic delivery evidence 003\n%%EOF\n",
        }],
    }


def _digital_demo_case(anchor: datetime) -> dict:
    """Synthetic digital-goods case: a payment, no order record yet, a later delivery and a claim inside the gap."""
    paid = anchor - timedelta(days=3, hours=12)
    order_recorded = anchor - timedelta(days=3)
    claim = anchor - timedelta(days=1)
    delivered = anchor - timedelta(hours=20)
    return {
        "case_id": "demo-case-002", "order_id": "demo-dispute-order-002", "reason": "INR",
        "order_created_at": iso(order_recorded), "delivered_at": iso(delivered), "opened_at": iso(claim),
        "carrier_status": "delivered", "evidence_source": "synthetic",
        "dispute_amount": dict(DEMO_DISPUTE_AMOUNTS["demo-case-002"]),
        "provider_snapshot": {
            "schema_version": 1,
            "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
            "observed_at": iso(anchor - timedelta(hours=1)),
            "dispute_id": "demo-case-002",
            "order_id": "demo-dispute-order-002",
            "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
            "status": "WAITING_FOR_SELLER_RESPONSE",
            "dispute_life_cycle_stage": "INQUIRY",
            "seller_response_due_date": iso(anchor + timedelta(days=2)),
            "available_actions": ["PROVIDE_EVIDENCE"],
            "evidences": [{
                "request_id": "demo-request-fulfillment-002",
                "evidence_type": "PROOF_OF_FULFILLMENT",
                "source": "REQUESTED_FROM_SELLER",
                "mandatory": True,
                "action": "PROVIDE_EVIDENCE",
            }],
        },
        "proof_records": [{
            "evidence_id": "demo-proof-fulfillment-002",
            "request_id": "demo-request-fulfillment-002",
            "evidence_type": "FULFILLMENT",
            "proof_fields": {"delivery_channel": "EMAIL_LINK", "delivered_at": iso(delivered)},
            "observed_at": iso(delivered),
            "evidence_state": "SUPPLIED_UNVERIFIED",
            "attachment_ids": [],
        }],
        "attachment_candidates": [],
        "time_evidence_input": {
            "times": {"payment_at": iso(paid), "order_record_at": iso(order_recorded),
                      "delivered_at": iso(delivered), "claim_at": iso(claim)},
            "messages": [
                {"channel": "EMAIL", "direction": "INBOUND", "sent_at": iso(paid + timedelta(minutes=30)),
                 "topic": "PAYMENT_NOTICE", "text": "Synthetic message: payment sent, no order confirmation yet."},
                {"channel": "EMAIL", "direction": "OUTBOUND", "sent_at": iso(paid + timedelta(hours=1)),
                 "topic": "ORDER_DETAILS_REQUEST", "text": "Synthetic message: no order found, please send the order details."},
                {"channel": "PRIVATE_MESSAGE", "direction": "INBOUND", "sent_at": iso(order_recorded - timedelta(hours=1)),
                 "topic": "ORDER_DETAILS_PROVIDED", "text": "Synthetic message: here are the order details."},
                {"channel": "EMAIL", "direction": "OUTBOUND", "sent_at": iso(delivered),
                 "topic": "DELIVERY_NOTICE", "text": "Synthetic message: the download link was sent."},
            ],
        },
    }


def _draft_response(public: dict) -> dict:
    """Validate a public draft; keep the response of cases without time evidence unchanged."""
    response = DisputeDraftResponse.model_validate(public).model_dump()
    if response.get("time_evidence") is None:
        response.pop("time_evidence", None)
    return response


def _legacy_dispute_case(case: dict) -> dict:
    fields = {
        "case_id", "order_id", "reason", "opened_at", "order_created_at",
        "carrier_status", "delivered_at", "evidence_source",
    }
    if type(case) is not dict:
        raise BoundaryError(422, "dispute_context_not_ready")
    return {field: case[field] for field in fields if field in case}


def _dispute_match_request(case: dict, routing: dict, as_of: datetime) -> str:
    required = {"case_id", "order_id", "opened_at", "order_created_at", "provider_snapshot", "proof_records"}
    if type(case) is not dict or not required.issubset(case) or type(routing) is not dict:
        raise BoundaryError(422, "dispute_context_not_ready")
    if any(type(case[field]) is not str or not case[field] for field in ("case_id", "order_id", "opened_at", "order_created_at")):
        raise BoundaryError(422, "dispute_context_not_ready")
    snapshot = case["provider_snapshot"]
    if type(snapshot) is not dict or routing.get("overall_state") != "READY_FOR_LOCAL_REVIEW":
        raise BoundaryError(422, "dispute_context_not_ready")
    payload = {
        "merchant_case_ref": case["case_id"],
        "order_id": case["order_id"],
        "reason_code": routing["reason"],
        "opened_at": case["opened_at"],
        "order_created_at": case["order_created_at"],
        "case_stage": routing["dispute_life_cycle_stage"],
        "case_status": routing["status"],
        "seller_response_due_date": routing["seller_response_due_date"],
        "available_actions": list(routing["available_actions"]),
        "evidences": deepcopy(snapshot["evidences"]),
    }
    if type(case.get("carrier_status")) is str:
        payload["carrier_status"] = case["carrier_status"]
    if type(case.get("delivered_at")) is str:
        payload["delivered_at"] = case["delivered_at"]
    evidence_items = []
    for proof in case["proof_records"]:
        if type(proof) is not dict:
            raise BoundaryError(422, "dispute_context_not_ready")
        evidence_items.append({
            "evidence_id": proof["evidence_id"],
            "evidence_type": proof["evidence_type"],
            "field_id": "payload.evidences",
            "provider_request_id": proof["request_id"],
            "origin_ref": {
                "source_id": "PP-DISPUTES-API",
                "chunk_id": "PP-EVIDENCE-TRACKING",
            },
            "observed_at": proof["observed_at"],
            "evidence_state": proof["evidence_state"],
        })
    request = {
        "schema_version": 1,
        "intake_id": case["case_id"],
        "requested_theme": "dispute_mediation",
        "request_kind": "prepare_dispute_draft",
        "jurisdiction": "US",
        "as_of": iso(as_of),
        "observation_max_age_days": 90,  # reference pack retrieved 2026-10-06; usable through 2027-01-04
        "source_class": "synthetic",
        "payload": payload,
        "evidence_items": evidence_items,
        "references": [],
    }
    return json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _project_dispute_match(result: dict) -> dict:
    if type(result) is not dict:
        raise BoundaryError(500, "response_contract_failure")
    status = result.get("status")
    if status in {"intake_blocked", "evidence_missing"}:
        raise BoundaryError(422, "dispute_context_not_ready")
    if status == "reference_unavailable":
        raise BoundaryError(503, "reference_unavailable")
    expected_keys = {
        "schema_version", "source", "status", "intake", "matches", "provenance",
        "evaluation_scope", "required_human_review", "operational_authority",
        "engine_execution", "semantic_confidence", "current_policy_applicability",
        "real_case_evidence",
    }
    intake = result.get("intake")
    matches = result.get("matches")
    if (set(result) != expected_keys or status != "synthetic_scenarios_found" or
            type(intake) is not dict or intake.get("status") not in {"ready_for_local_rules", "manual_review"} or
            type(matches) is not list or len(matches) != 1):
        raise BoundaryError(500, "response_contract_failure")
    match = matches[0]
    scenario_keys = {
        "scenario_id", "title", "theme", "jurisdiction", "evidence_class",
        "expected_route", "final_authority", "limitations", "citations",
        "real_case_evidence",
    }
    if type(match) is not dict or set(match) != scenario_keys or match.get("real_case_evidence") != "NOT_PROVIDED":
        raise BoundaryError(500, "response_contract_failure")
    projected = {
        "schema_version": result["schema_version"],
        "source": result["source"],
        "status": result["status"],
        "intake_status": intake["status"],
        "provenance": result["provenance"],
        "evaluation_scope": result["evaluation_scope"],
        "required_human_review": result["required_human_review"],
        "operational_authority": result["operational_authority"],
        "engine_execution": result["engine_execution"],
        "current_policy_applicability": result["current_policy_applicability"],
        "real_case_evidence": result["real_case_evidence"],
        "scenario": {key: match[key] for key in scenario_keys if key != "real_case_evidence"},
    }
    try:
        return ScenarioMatch.model_validate(projected).model_dump()
    except ValidationError:
        raise BoundaryError(500, "response_contract_failure") from None


class BoundaryError(Exception):
    def __init__(self, status: int, code: str, *, retry_after: int | None = None):
        self.status = status
        self.code = code
        # (attack r21) Seconds until a capacity limit frees a slot, when the server knows it; None otherwise.
        self.retry_after = retry_after
        super().__init__(code)


class AiAttemptBudget:
    """Process-local, fail-closed model-attempt reservations.

    A reservation is permanent for the lifetime of this object. Provider
    failures, timeouts, cancellations, invalid responses, session reset and
    session expiry never return a slot.
    """

    def __init__(self, *, limit: int = AI_ATTEMPT_LIMIT):
        if type(limit) is not int or limit != AI_ATTEMPT_LIMIT:
            raise ValueError("ai_attempt_limit_invalid")
        self.limit = limit
        self._reservations: dict[str, str] = {}
        self._lock = threading.RLock()

    @property
    def used(self) -> int:
        with self._lock:
            return len(self._reservations)

    def snapshot(self):
        with self._lock:
            return MappingProxyType(dict(self._reservations))

    def reserve(self, stage: str, reserved_at: datetime) -> dict:
        with self._lock:
            if stage not in AI_BRIEF_STAGES:
                raise BoundaryError(422, "ai_request_invalid")
            if len(self._reservations) >= self.limit:
                raise BoundaryError(429, "ai_attempt_limit")
            if stage in self._reservations:
                raise BoundaryError(409, "ai_stage_attempt_exhausted")
            self._reservations[stage] = iso(reserved_at)
            used = len(self._reservations)
            return {"limit": self.limit, "used": used, "remaining": self.limit - used, "stage": stage}

    def can_reserve(self, stage: str) -> bool:
        with self._lock:
            return (
                stage in AI_BRIEF_STAGES
                and len(self._reservations) < self.limit
                and stage not in self._reservations
            )


@dataclass
class Session:
    session_id: str
    csrf_token: str
    created_at: datetime
    expires_at: datetime
    anchor: datetime
    token_key: bytes = field(default_factory=lambda: secrets.token_bytes(32), repr=False)
    transactions: list[dict] = field(default_factory=list)
    disputes: dict[str, dict] = field(default_factory=dict)
    drafts: dict[str, dict] = field(default_factory=dict)
    draft_expires: dict[str, datetime] = field(default_factory=dict)
    restricted_evidence: dict[str, dict] = field(default_factory=dict, repr=False)
    approved: set[str] = field(default_factory=set)
    # (optimise r24) Per approved case, the payload hashes the approval covers ({"provide_evidence", "add_tracking"}).
    approved_payloads: dict[str, dict] = field(default_factory=dict)
    # Cases whose approval a provide-evidence submit has already used: one approval, one send (red team r20 D4).
    submitted: set[str] = field(default_factory=set)
    aup_evaluations: dict[str, dict] = field(default_factory=dict)
    current_aup_evaluation_id: str | None = None
    # (attack r22) match_status of the latest /aup/review in this session; the guide refuses a self-declared
    # "no_signal" category answer while it is REVIEW_SIGNAL. Kept after the evaluation itself is used or expires.
    latest_aup_match_status: str | None = None
    aup_audit: deque = field(default_factory=lambda: deque(maxlen=30))
    invoice_reviews: dict[str, dict] = field(default_factory=dict)
    invoice_attempts: int = 0
    activity: list[dict] = field(default_factory=list)
    scenario: dict = field(default_factory=lambda: {"burst": False, "dispute": False})
    requests: deque = field(default_factory=deque)
    gate: LocalReviewGate = field(default_factory=LocalReviewGate, repr=False)
    # Who created it, so one visitor cannot hold the whole store (owner 2026-11-03: add per-visitor limits).
    client_key: str = "local"


# Per-visitor limits (owner 2026-11-03, attack r21 S01/S02): one visitor may create this many sessions a minute and
# hold this many at once; the store-wide creation limit stays as a backstop.
# r23: a real judge flow (console, dashboard, scenarios with its hidden frame, a reload, five work orders) opens about
# ten sessions in a minute, and 60 store-wide fitted only 7.5 visitors; the limits below leave room for both.
CLIENT_CREATIONS_PER_MINUTE = 20
CLIENT_MAX_LIVE_SESSIONS = 30
STORE_CREATIONS_PER_MINUTE = 600
HOSTED_MAX_SESSIONS = 1000
# Hosted demo: a judge reading a page for a few minutes keeps the session (r23: 60 s idle was evicted by others).
HOSTED_IDLE_EVICT_SECONDS = 600
# A full store may drop a session that has made no request for this long, to admit a new visitor.
IDLE_EVICT_SECONDS = 60


class SessionStore:
    def __init__(self, *, clock=utc_now, ttl_seconds=900, max_sessions=100, rate_limit=60,
                 ai_attempt_budget: AiAttemptBudget | None = None):
        self.clock = clock
        self.ttl_seconds = ttl_seconds
        self.max_sessions = max_sessions
        self.rate_limit = rate_limit
        self.sessions: dict[str, Session] = {}
        self.creation_requests: deque = deque()
        self.client_creations: dict[str, deque] = {}
        # On only for the hosted demo (create_app); the local console has one operator and keeps the old limit.
        self.per_client_limits = False
        # (optimise r24) Callables (session, case_id) -> {payload kind: hash} that approve() records; see paypal_disputes.
        self.approval_hooks: dict = {}
        self.ai_attempt_budget = ai_attempt_budget if ai_attempt_budget is not None else AiAttemptBudget()
        if type(self.ai_attempt_budget) is not AiAttemptBudget:
            raise TypeError("ai_attempt_budget_invalid")
        self.lock = threading.RLock()

    def _now(self) -> datetime:
        value = self.clock()
        if value.tzinfo is None or value.utcoffset() is None:
            raise BoundaryError(503, "clock_unavailable")
        return value.astimezone(timezone.utc)

    def _purge(self, now: datetime):
        expired = [key for key, session in self.sessions.items() if session.expires_at <= now]
        for key in expired:
            del self.sessions[key]

    def creation_wait(self, client_key: str = "local") -> float:
        """Seconds until this visitor may create a session (0 = now). Read-only, so the route can queue a request for a
        short wait instead of refusing it (owner 2026-11-03: turn bursts into a queue)."""
        with self.lock:
            now = self._now()
            self._purge(now)
            waits = [0.0]
            # The store-wide creation limit is its own number, not capped by the per-session request rate (attack r23).
            store_limit = STORE_CREATIONS_PER_MINUTE if self.per_client_limits else min(self.rate_limit, 30)
            checks = [(self.creation_requests, store_limit)]
            if self.per_client_limits:
                checks.append((self.client_creations.get(client_key, deque()), CLIENT_CREATIONS_PER_MINUTE))
            for requests, limit in checks:
                live = [at for at in requests if at > now - timedelta(seconds=60)]
                if len(live) >= limit:
                    waits.append((live[len(live) - limit] + timedelta(seconds=60) - now).total_seconds())
            return max(waits)

    def create(self, client_key: str = "local") -> dict:
        with self.lock:
            now = self._now()
            self._purge(now)
            if not self.per_client_limits:
                client_key = "local"
                self._rate(self.creation_requests, now, min(self.rate_limit, 30))
            else:
                # The visitor's own limit first, so a refused visitor does not use up the store-wide count.
                self._rate(self.client_creations.setdefault(client_key, deque()), now, CLIENT_CREATIONS_PER_MINUTE)
                self._rate(self.creation_requests, now, STORE_CREATIONS_PER_MINUTE)
            mine = [session for session in self.sessions.values() if session.client_key == client_key]
            if self.per_client_limits and len(mine) >= CLIENT_MAX_LIVE_SESSIONS:
                # This visitor's own least recently used session makes room; another visitor's never does.
                oldest = min(mine, key=lambda session: session.requests[-1] if session.requests else session.created_at)
                del self.sessions[oldest.session_id]
            if len(self.client_creations) > 4096:
                for key in [key for key, requests in self.client_creations.items() if not requests or requests[-1] <= now - timedelta(seconds=60)]:
                    del self.client_creations[key]
            capacity = max(self.max_sessions, HOSTED_MAX_SESSIONS) if self.per_client_limits else self.max_sessions
            if len(self.sessions) >= capacity and not self._evict_idle(now):
                raise BoundaryError(429, "session_capacity", retry_after=self._capacity_wait(now))
            session = Session(secrets.token_urlsafe(32), secrets.token_urlsafe(32), now,
                              now + timedelta(seconds=self.ttl_seconds), now, client_key=client_key)
            self.sessions[session.session_id] = session
            return {"session_id": session.session_id, "csrf_token": session.csrf_token,
                    "source": "synthetic", "expires_at": iso(session.expires_at)}

    def _evict_idle(self, now: datetime) -> bool:
        """Free one slot when the store is full: drop the session idle longest, if it has been idle at least
        IDLE_EVICT_SECONDS. Without this, one client creating max_sessions sessions locked every new visitor out until
        the TTL ran out (red team R4); a session in active use is never dropped."""
        # One switch: the hosted limits all follow per_client_limits, so no store is half configured (attack r23).
        cutoff = now - timedelta(seconds=HOSTED_IDLE_EVICT_SECONDS if self.per_client_limits else IDLE_EVICT_SECONDS)
        idle = [(session.requests[-1] if session.requests else session.created_at, key) for key, session in self.sessions.items()]
        idle = [entry for entry in idle if entry[0] <= cutoff]
        if not idle:
            return False
        del self.sessions[min(idle)[1]]
        return True

    def _rate(self, requests: deque, now: datetime, limit: int):
        cutoff = now - timedelta(seconds=60)
        while requests and requests[0] <= cutoff:
            requests.popleft()
        if len(requests) >= limit:
            # (optimise r24) Say when: the refusal carries Retry-After (the console's countdown reads it), the
            # seconds until the oldest request that still counts leaves the one-minute window.
            wait = (requests[len(requests) - limit] + timedelta(seconds=60) - now).total_seconds()
            raise BoundaryError(429, "rate_limited", retry_after=max(1, min(60, math.ceil(wait))))
        requests.append(now)

    def _capacity_wait(self, now: datetime) -> int:
        """(optimise r24) Seconds until a full store frees a slot: the first session to expire or to become idle long
        enough to be dropped for a new visitor."""
        idle = timedelta(seconds=HOSTED_IDLE_EVICT_SECONDS if self.per_client_limits else IDLE_EVICT_SECONDS)
        moments = [min(session.expires_at, (session.requests[-1] if session.requests else session.created_at) + idle)
                   for session in self.sessions.values()]
        wait = (min(moments) - now).total_seconds() if moments else 1
        return max(1, min(self.ttl_seconds, math.ceil(wait)))

    def require(self, session_id: str | None, csrf_token: str | None = None, *, mutate=False) -> Session:
        with self.lock:
            now = self._now()
            self._purge(now)
            if not isinstance(session_id, str) or not session_id.isascii() or len(session_id) > 128:
                raise BoundaryError(401, "session_required")
            session = self.sessions.get(session_id)
            if session is None:
                raise BoundaryError(401, "session_required")
            if mutate and (not isinstance(csrf_token, str) or not csrf_token.isascii() or len(csrf_token) > 128 or
                           not safe_equal(csrf_token, session.csrf_token)):
                raise BoundaryError(403, "csrf_rejected")
            self._rate(session.requests, now, self.rate_limit)
            return session

    def state(self, session: Session) -> dict:
        with self.lock:
            now = self._now()
            self._expire_dispute_layers(session, now)
            velocity = self._velocity(session.transactions, now)
            summaries = [
                {"case_ref": f"case-ref-{index:03d}", "order_ref": f"order-ref-{index:03d}", "reason": case["reason"],
                 "opened_at": case["opened_at"], "seller_response_due_date": case["provider_snapshot"]["seller_response_due_date"],
                 "dispute_amount": deepcopy(case["dispute_amount"]),
                 "status": "local_draft_reviewed" if case_id in session.approved else
                           ("draft_ready" if case_id in session.drafts else "needs_review")}
                for index, (case_id, case) in enumerate(session.disputes.items(), start=1)
            ]
            return deepcopy({"session_id": session.session_id, "source": "synthetic", "policy_version": POLICY_VERSION,
                             "transactions": session.transactions, "velocity": velocity, "disputes": summaries,
                             "activity": session.activity, "scenario": session.scenario,
                             "expires_at": iso(session.expires_at)})

    def _velocity(self, transactions: list[dict], as_of: datetime) -> dict:
        observation_start = as_of - timedelta(hours=DEMO_VELOCITY_BASELINE["observation_hours"])
        baseline_end = observation_start
        baseline_start = baseline_end - timedelta(hours=DEMO_VELOCITY_BASELINE["comparison_hours"])
        return assess_velocity(
            transactions,
            DEMO_VELOCITY_BASELINE["amount_per_hour"],
            iso(as_of),
            window_hours=DEMO_VELOCITY_BASELINE["observation_hours"],
            baseline_provenance=DEMO_VELOCITY_BASELINE["provenance"],
            baseline_window_start=iso(baseline_start),
            baseline_window_end=iso(baseline_end),
        )

    def _ai_context_ready_locked(self, session: Session, stage: str, now: datetime) -> bool:
        self._expire_dispute_layers(session, now)
        if stage == "source_compliance":
            evaluation = session.aup_evaluations.get(session.current_aup_evaluation_id)
            return bool(
                evaluation is not None and
                evaluation["expires_at"] > now and
                evaluation["match_status"] == "REVIEW_SIGNAL"
            )
        if stage == "velocity_guard":
            return self._velocity(session.transactions, now)["status"] == "review_velocity"
        if stage == "dispute_mediation":
            return any(self._case_ai_ready(session, case_id, now) for case_id in session.disputes)
        return False

    def _case_ai_ready(self, session: Session, case_id: str, now: datetime) -> bool:
        return bool(
            type(session.drafts.get(case_id, {}).get("routing")) is dict and
            session.drafts[case_id]["routing"].get("overall_state") == "READY_FOR_LOCAL_REVIEW" and
            session.disputes[case_id].get("reason") == "INR" and
            session.drafts[case_id].get("evidence", {}).get("reason") == "INR" and
            session.drafts[case_id]["routing"].get("reason") == "MERCHANDISE_OR_SERVICE_NOT_RECEIVED" and
            self._restricted_is_current(session, case_id) and
            session.draft_expires.get(case_id, now) > now
        )

    def _ai_session_facts_locked(self, session: Session, stage: str, case_ref: str | None, now: datetime) -> dict:
        """Closed values for the AI brief, computed here from session state: no description text, order, amount
        detail or identifier leaves this method. The AI brief contract validates them again."""
        if stage == "source_compliance":
            evaluation = session.aup_evaluations[session.current_aup_evaluation_id]
            return {"review_categories": sorted(set(evaluation["categories"]))}
        if stage == "velocity_guard":
            velocity = self._velocity(session.transactions, now)
            two_places = lambda value: str(Decimal(str(value)).quantize(Decimal("0.01"), rounding="ROUND_DOWN"))
            return {"transaction_count": velocity["transaction_count"], "ratio": two_places(velocity["ratio"]),
                    "threshold": two_places(velocity["threshold"])}
        if case_ref is None:
            case_id = next(case_id for case_id in session.disputes if self._case_ai_ready(session, case_id, now))
        else:
            case_id, _case = self._resolve_case_ref(session, case_ref)
            if not self._case_ai_ready(session, case_id, now):
                raise BoundaryError(409, "ai_context_not_ready")
        routing = session.drafts[case_id]["routing"]
        # One row per evidence type; when the provider asks for a type twice, the least complete state wins.
        rank = {"MANDATORY_EVIDENCE_MISSING": 0, "OPTIONAL_EVIDENCE_MISSING": 1, "STRUCTURALLY_PRESENT": 2}
        rows = {}
        for row in routing["requirements"]:
            kind, state = row.get("provider_evidence_type"), row.get("requirement_state")
            if row.get("source") != "REQUESTED_FROM_SELLER" or kind not in AI_FACT_EVIDENCE_TYPES or state not in rank:
                continue
            if kind not in rows or rank[state] < rank[rows[kind]]:
                rows[kind] = state
        if not rows:
            raise BoundaryError(409, "ai_context_not_ready")
        return {"reason": "INR", "due_state": routing["due_state"],
                "requirements": [{"evidence_type": key, "state": rows[key]} for key in sorted(rows)]}

    def ai_brief_allowed(self, session: Session, stage: str) -> bool:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            return self._ai_context_ready_locked(session, stage, now) and self.ai_attempt_budget.can_reserve(stage)

    def reserve_ai_brief(self, session: Session, stage: str, case_ref: str | None = None) -> dict:
        """Atomically validate context, compute the closed session facts and reserve a model attempt; returns the facts."""
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            if not self._ai_context_ready_locked(session, stage, now):
                raise BoundaryError(409, "ai_context_not_ready")
            facts = self._ai_session_facts_locked(session, stage, case_ref, now)
            try:  # the facts pass the brief's own closed contract before an attempt is spent
                AiBriefRequest.model_validate({"stage": stage, "session_facts": facts})
            except ValidationError:
                raise BoundaryError(409, "ai_context_not_ready") from None
            self.ai_attempt_budget.reserve(stage, now)
            return facts

    def reserve_ai_brief_attempt(self, session: Session, stage: str) -> dict:
        """Atomically validate context and permanently reserve a model attempt."""
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            if not self._ai_context_ready_locked(session, stage, now):
                raise BoundaryError(409, "ai_context_not_ready")
            return self.ai_attempt_budget.reserve(stage, now)

    def _activity(self, session: Session, kind: str, label: str):
        session.activity.append({"id": "demo-activity-" + secrets.token_hex(8), "at": iso(self._now()),
                                 "kind": kind, "label": label, "source": "synthetic"})
        session.activity[:] = session.activity[-30:]

    def inject(self, session: Session, scenario: str) -> dict:
        with self.lock:
            self._require_live_session(session, self._now())
            if scenario == "reset":
                session.transactions.clear()
                session.disputes.clear()
                session.drafts.clear()
                session.draft_expires.clear()
                session.restricted_evidence.clear()
                session.approved.clear()
                session.approved_payloads.clear()
                session.submitted.clear()
                session.invoice_reviews.clear()
                session.aup_evaluations.clear()
                session.current_aup_evaluation_id = None
                session.latest_aup_match_status = None
                session.aup_audit.clear()
                session.activity.clear()
                session.scenario = {"burst": False, "dispute": False}
                session.anchor = self._now()
                session.token_key = secrets.token_bytes(32)
                session.gate = LocalReviewGate()
                return self.state(session)
            if session.scenario[scenario]:
                return self.state(session)
            rows = deepcopy(session.transactions)
            cases = deepcopy(session.disputes)
            if scenario == "burst":
                # Fifty synthetic captures with varied amounts; every ten rows sum to
                # 100.00 so the window total stays 500.00 against the 100.00/h baseline.
                rows.extend({"order_id": f"demo-burst-{index:03d}",
                             "amount": DEMO_BURST_AMOUNTS[(index - 1) % len(DEMO_BURST_AMOUNTS)], "currency": "USD",
                             "occurred_at": iso(session.anchor - timedelta(minutes=index % 40))}
                            for index in range(1, 51))
            else:
                case = {"case_id": "demo-case-001", "order_id": "demo-dispute-order-001", "reason": "INR",
                        "order_created_at": iso(session.anchor - timedelta(days=3)),
                        "delivered_at": iso(session.anchor - timedelta(days=2)),
                        "opened_at": iso(session.anchor - timedelta(days=1)),
                        "carrier_status": "delivered", "evidence_source": "synthetic",
                        "dispute_amount": dict(DEMO_DISPUTE_AMOUNTS["demo-case-001"]),
                        "provider_snapshot": {
                            "schema_version": 1,
                            "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
                            "observed_at": iso(session.anchor - timedelta(hours=1)),
                            "dispute_id": "demo-case-001",
                            "order_id": "demo-dispute-order-001",
                            "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
                            "status": "WAITING_FOR_SELLER_RESPONSE",
                            "dispute_life_cycle_stage": "INQUIRY",
                            "seller_response_due_date": iso(session.anchor + timedelta(days=2)),
                            "available_actions": ["PROVIDE_EVIDENCE"],
                            "evidences": [{
                                "request_id": "demo-request-fulfillment-001",
                                "evidence_type": "PROOF_OF_FULFILLMENT",
                                "source": "REQUESTED_FROM_SELLER",
                                "mandatory": True,
                                "action": "PROVIDE_EVIDENCE",
                            }],
                        },
                        "proof_records": [{
                            "evidence_id": "demo-proof-fulfillment-001",
                            "request_id": "demo-request-fulfillment-001",
                            "evidence_type": "FULFILLMENT",
                            "proof_fields": {
                                "carrier_name": "SYNTHETIC_CARRIER",
                                "tracking_number": "SYNTHETIC_TRACKING_001",
                                "delivered_at": iso(session.anchor - timedelta(days=2)),
                                "delivery_status": "DELIVERED",
                                "destination_match_status": "MATCHED",
                            },
                            "observed_at": iso(session.anchor - timedelta(days=2)),
                            "evidence_state": "SUPPLIED_UNVERIFIED",
                            "attachment_ids": ["demo-attachment-001"],
                        }],
                        "attachment_candidates": [{
                            "attachment_id": "demo-attachment-001",
                            "evidence_id": "demo-proof-fulfillment-001",
                            "filename": "synthetic-delivery.pdf",
                            "declared_media_type": "application/pdf",
                            "content": b"%PDF-1.7\nSynthetic delivery evidence\n%%EOF\n",
                        }]}
                prepare_dispute(_legacy_dispute_case(case))
                cases[case["case_id"]] = case
                digital = _digital_demo_case(session.anchor)
                prepare_dispute(_legacy_dispute_case(digital))
                cases[digital["case_id"]] = digital
                due_soon = _due_soon_demo_case(session.anchor)
                prepare_dispute(_legacy_dispute_case(due_soon))
                cases[due_soon["case_id"]] = due_soon
            if len(rows) > 200 or len(cases) > 5:
                raise BoundaryError(422, "sample_limit")
            self._velocity(rows, self._now())
            # All domain validation precedes the single in-memory commit.
            session.transactions = rows
            session.disputes = cases
            session.scenario[scenario] = True
            self._activity(session, scenario, "Synthetic burst injected" if scenario == "burst" else "Synthetic INR dispute injected")
            return self.state(session)

    def _resolve_case_ref(self, session: Session, case_ref: str) -> tuple[str, dict]:
        if type(case_ref) is not str:
            raise BoundaryError(404, "case_not_found")
        for index, (case_id, case) in enumerate(session.disputes.items(), start=1):
            expected = f"case-ref-{index:03d}"
            if safe_equal(case_ref, expected):
                return case_id, case
        raise BoundaryError(404, "case_not_found")

    def _public_dispute_draft(self, draft: dict, case_ref: str, digest: str) -> dict:
        public = deepcopy(draft)
        public.pop("case_id", None)
        evidence = public.get("evidence")
        if type(evidence) is not dict:
            raise BoundaryError(500, "response_contract_failure")
        evidence.pop("case_id", None)
        evidence.pop("order_id", None)
        public["case_ref"] = case_ref
        public["draft_digest"] = digest
        return public

    def _verified_restricted_digest(self, session: Session, case_id: str) -> str:
        try:
            return restricted_evidence_digest(session.restricted_evidence.get(case_id))
        except DisputeEvidenceError:
            raise BoundaryError(422, "review_binding_rejected") from None

    def _restricted_is_current(self, session: Session, case_id: str) -> bool:
        try:
            restricted_evidence_digest(session.restricted_evidence.get(case_id))
            return True
        except DisputeEvidenceError:
            return False

    def draft(self, session: Session, case_ref: str) -> dict:
        with self.lock:
            case_id, case = self._resolve_case_ref(session, case_ref)
            now = self._now()
            self._expire_dispute_layers(session, now)
            if case_id not in session.drafts:
                legacy_reason = case.get("reason")
                snapshot_reason = case.get("provider_snapshot", {}).get("reason")
                if (legacy_reason == "INR" and snapshot_reason != "MERCHANDISE_OR_SERVICE_NOT_RECEIVED") or \
                        (legacy_reason != "INR" and legacy_reason != snapshot_reason):
                    raise BoundaryError(422, "dispute_context_not_ready")
                draft = prepare_dispute(_legacy_dispute_case(case))
                draft["source"] = "synthetic"
                try:
                    # Real content for the synthetic delivery PDF, built from this case's own fields; the bytes then
                    # flow into the restricted sha256, the draft digest and the approval's payload hash as before.
                    case["attachment_candidates"] = [
                        dict(row, content=evidence_pdf_for_case(case_ref, case))
                        if type(row.get("content")) is bytes and row["content"].startswith(_PLACEHOLDER_PDF_PREFIX) else row
                        for row in case["attachment_candidates"]]
                except EvidencePdfError:
                    raise BoundaryError(422, "dispute_context_not_ready") from None
                try:
                    layers = resolve_dispute_requirements(
                        case["provider_snapshot"], case["proof_records"],
                        case["attachment_candidates"], now,
                    )
                    matched = match_cases(_dispute_match_request(case, layers["routing"], now))
                except BoundaryError:
                    raise
                except DisputeEvidenceError:
                    raise BoundaryError(422, "dispute_context_not_ready") from None
                except Exception:
                    raise BoundaryError(500, "response_contract_failure") from None
                draft["routing"] = layers["routing"]
                time_input = case.get("time_evidence_input")
                if time_input is not None:
                    try:
                        records = [{"channel": row["channel"], "direction": row["direction"],
                                    "sent_at": row["sent_at"], "topic": row["topic"],
                                    "message_digest": message_digest(session.token_key, row["text"])}
                                   for row in time_input["messages"]]
                        draft["time_evidence"] = build_time_evidence(time_input["times"], records)
                    except (DisputeEvidenceError, KeyError, TypeError):
                        raise BoundaryError(422, "dispute_context_not_ready") from None
                draft["restricted_original_summary"] = layers["restricted_original_summary"]
                draft["scenario_match"] = _project_dispute_match(matched)
                tokens = redact_identity({"name": "Synthetic Demo Person", "address": "Synthetic Demo Address",
                                          "email": "demo@example.invalid"}, session.token_key)
                draft["identity_redaction"] = {"method": "HMAC-SHA256 pseudonymization",
                                                "fields": ["name", "address", "email"], "tokens": tokens,
                                                "synthetic": True}
                narrative_fields = {field: draft["evidence"].get(field) or "MISSING[" + field + "]"
                                    for field in ("order_id", "order_created_at", "delivered_at", "opened_at")}
                narrative = ("Synthetic Demo Person at Synthetic Demo Address; email demo@example.invalid; "
                             "synthetic phone (415) 555-0132; synthetic SSN-like 123-45-6789. "
                             "Order " + narrative_fields["order_id"] + " created " + narrative_fields["order_created_at"] +
                             "; delivery observed " + narrative_fields["delivered_at"] + "; dispute opened " + narrative_fields["opened_at"] +
                             ". Delivery evidence does not establish fraud or release of funds. " +
                             internal_review_narrative(layers["routing"]))
                draft["document_redaction"] = redact_dispute_document(
                    narrative, session.token_key, document_id=case_id,
                    literals=[{"type": "name", "text": "Synthetic Demo Person"},
                              {"type": "address", "text": "Synthetic Demo Address"},
                              {"type": "manual", "text": narrative_fields["order_id"]}])
                expires_at = min(session.expires_at, now + timedelta(seconds=300))
                digest = payload_digest({"session_id": session.session_id, "draft": draft,
                                         "restricted_sha256": layers["restricted"]["sha256"],
                                         "expires_at": iso(expires_at)})
                try:
                    response = _draft_response(self._public_dispute_draft(draft, case_ref, digest))
                except ValidationError:
                    raise BoundaryError(500, "response_contract_failure") from None
                session.drafts[case_id] = draft
                session.restricted_evidence[case_id] = layers["restricted"]
                session.draft_expires[case_id] = expires_at
                self._activity(session, "draft", "Synthetic dispute evidence draft prepared")
                return response
            draft = deepcopy(session.drafts[case_id])
            restricted_digest = self._verified_restricted_digest(session, case_id)
            digest = payload_digest({"session_id": session.session_id, "draft": draft,
                                     "restricted_sha256": restricted_digest,
                                     "expires_at": iso(session.draft_expires[case_id])})
            try:
                return _draft_response(self._public_dispute_draft(draft, case_ref, digest))
            except ValidationError:
                raise BoundaryError(500, "response_contract_failure") from None

    def approve(self, session: Session, case_ref: str, digest: str) -> dict:
        with self.lock:
            now = self._now()
            self._expire_dispute_layers(session, now)
            case_id, _case = self._resolve_case_ref(session, case_ref)
            if case_id not in session.drafts:
                raise BoundaryError(422, "draft_required")
            if case_id in session.approved:
                raise BoundaryError(422, "review_already_used")
            current = self.draft(session, case_ref)
            if not safe_equal(current["draft_digest"], digest):
                raise BoundaryError(422, "review_binding_rejected")
            draft = session.drafts[case_id]
            approval = session.gate.approve(draft, actor="demo-reviewer", now=now)
            receipt = session.gate.consume(approval, draft, actor="demo-reviewer", now=now)
            session.approved.add(case_id)
            # (optimise r24) Record the hashes of the payloads this approval covers; a send whose freshly built
            # payload differs is refused (409 evidence_changed_after_approval).
            recorded = {}
            for hook in list(self.approval_hooks.values()):
                recorded.update(hook(session, case_id))
            session.approved_payloads[case_id] = recorded
            self._activity(session, "review", "Local synthetic draft reviewed; external submission frozen")
            receipt.pop("case_id", None)
            return dict(
                receipt,
                case_ref=case_ref,
                reviewer="DEMO_OPERATOR_UNAUTHENTICATED",
                reviewed_at=now,
                retention="SESSION_MEMORY_ONLY",
                source="synthetic",
            )

    def _expire_dispute_layers(self, session: Session, now: datetime):
        expired = [case_id for case_id, expires_at in session.draft_expires.items()
                   if expires_at <= now]
        for case_id in expired:
            session.drafts.pop(case_id, None)
            session.draft_expires.pop(case_id, None)
            session.restricted_evidence.pop(case_id, None)
            session.approved_payloads.pop(case_id, None)
            # The used approval lapses with its draft; a new draft needs a new review before it can be sent (red team r20).
            session.submitted.discard(case_id)
            if case_id in session.approved:
                # The review was bound to this draft; say so in the activity log instead of dropping it silently
                # (red team R3). A new draft needs a new review.
                session.approved.discard(case_id)
                self._activity(session, "review", "Earlier local review lapsed with its expired draft; a new review is needed")

    def _require_live_session(self, session: Session, now: datetime):
        if (type(session) is not Session or self.sessions.get(session.session_id) is not session or
                session.expires_at <= now):
            raise BoundaryError(401, "session_required")

    def _aup_event(self, session: Session, evaluation_id: str, evaluation: dict, choice: str, now: datetime):
        session.aup_audit.append({
            "evaluation_id": evaluation_id, "description_digest": evaluation["description_digest"],
            "categories": list(evaluation["categories"]), "match_status": evaluation["match_status"],
            "evaluated_at": iso(evaluation["evaluated_at"]), "event_time": iso(now), "choice": choice,
            "warning_copy_version": "aup-warning-v1", "compliance_decision": "NOT_MADE",
            "external_action_authorized": False,
        })

    def review_aup(self, session: Session, description: str) -> dict:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            result = check_aup(description)
            expected_fields = {"match_status", "compliance_decision", "findings", "recommendation", "policy_version", "advisory_only"}
            if type(result) is not dict or set(result) != expected_fields:
                raise BoundaryError(500, "response_contract_failure")
            allowed_categories = {"unsupported_financial_promise", "weapons", "controlled_substances", "counterfeit_goods", "regulated_activity"}
            findings = result.get("findings") if type(result) is dict else None
            if (type(findings) is not list or len(findings) > 5 or
                    any(type(item) is not dict or set(item) != {"category", "code"} or
                        type(item.get("category")) is not str or item.get("category") not in allowed_categories or item.get("code") != "keyword_requires_policy_review" for item in findings) or
                    len({item["category"] for item in findings}) != len(findings) or
                    result.get("match_status") != ("REVIEW_SIGNAL" if findings else "NO_MATCH") or
                    result.get("compliance_decision") != "NOT_MADE" or result.get("advisory_only") is not True):
                raise BoundaryError(500, "response_contract_failure")
            digest = hashlib.sha256(description.encode("utf-8")).hexdigest()
            evaluation_id = secrets.token_urlsafe(32)
            expires = min(session.expires_at, now + timedelta(seconds=120))
            try:
                response = AupResponse.model_validate(dict(result, source="synthetic", evaluation_id=evaluation_id,
                    description_digest=digest, evaluated_at=iso(now), expires_at=iso(expires),
                    warning_copy_version="aup-warning-v1", policy_url="https://www.paypal.com/us/legalhub/paypal/acceptableuse-full",
                    current_policy_applicability="NOT_ESTABLISHED")).model_dump()
            except ValidationError:
                raise BoundaryError(500, "response_contract_failure") from None
            live = {key: value for key, value in session.aup_evaluations.items() if value["expires_at"] > now}
            if len(live) >= 5:
                # (attack r21) Say how long to wait: the oldest of the five live checks leaves the window first.
                # The limit itself (5 live checks, each live for up to 120 s) is unchanged.
                wait = math.ceil((min(value["expires_at"] for value in live.values()) - now).total_seconds())
                raise BoundaryError(429, "aup_capacity", retry_after=max(1, min(120, wait)))
            evaluation = {"description_digest": digest, "match_status": result["match_status"],
                          "categories": tuple(item["category"] for item in result["findings"]),
                          "evaluated_at": now, "expires_at": expires, "acknowledgement_digest": None,
                          "acknowledged_at": None}
            live[evaluation_id] = evaluation
            session.aup_evaluations = live
            session.current_aup_evaluation_id = evaluation_id
            session.latest_aup_match_status = result["match_status"]
            self._aup_event(session, evaluation_id, evaluation, "EVALUATED", now)
            return response

    def _require_aup_evaluation(self, session: Session, evaluation_id: str | None,
                                description_digest: str | None, now: datetime) -> dict:
        if evaluation_id is None or description_digest is None:
            raise BoundaryError(422, "aup_evaluation_required")
        evaluation = session.aup_evaluations.get(evaluation_id)
        if evaluation is None or not safe_equal(evaluation["description_digest"], description_digest):
            raise BoundaryError(422, "aup_evaluation_binding_rejected")
        if evaluation["expires_at"] <= now:
            raise BoundaryError(422, "aup_evaluation_expired")
        if now < evaluation["evaluated_at"]:
            raise BoundaryError(422, "aup_evaluation_binding_rejected")
        return evaluation

    def require_aup_category_binding(self, session: Session, evaluation_id: str, description: str) -> None:
        """Bind an optional category lookup to a live AUP evaluation of the same description.

        Read-only: the evaluation, its findings and its acknowledgement state are not touched.
        """
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            digest = hashlib.sha256(description.encode("utf-8")).hexdigest()
            self._require_aup_evaluation(session, evaluation_id, digest, now)

    def acknowledge_aup(self, session: Session, request: dict) -> dict:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            evaluation_id = request["evaluation_id"]
            evaluation = self._require_aup_evaluation(session, evaluation_id, request["description_digest"], now)
            choice = request["choice"]
            if choice not in ("RETURN_TO_EDIT", "CANCEL", "ACKNOWLEDGE_AND_CONTINUE"):
                raise BoundaryError(422, "aup_choice_rejected")
            token = None
            if choice == "ACKNOWLEDGE_AND_CONTINUE":
                if evaluation["match_status"] != "REVIEW_SIGNAL":
                    raise BoundaryError(422, "aup_choice_rejected")
                if evaluation["acknowledgement_digest"] is not None:
                    raise BoundaryError(422, "aup_acknowledgement_already_used")
                token = secrets.token_urlsafe(32)
                evaluation["acknowledgement_digest"] = hashlib.sha256(token.encode("ascii")).hexdigest()
                evaluation["acknowledged_at"] = now
            else:
                del session.aup_evaluations[evaluation_id]
                if session.current_aup_evaluation_id == evaluation_id:
                    session.current_aup_evaluation_id = None
            self._aup_event(session, evaluation_id, evaluation, choice, now)
            return {"source": "synthetic", "evaluation_id": evaluation_id,
                    "description_digest": evaluation["description_digest"], "choice": choice,
                    "acknowledgement_token": token, "expires_at": iso(evaluation["expires_at"]) if token else None,
                    "warning_copy_version": "aup-warning-v1", "compliance_decision": "NOT_MADE",
                    "external_action_authorized": False}

    def invoice_payload(self, payload: dict) -> dict:
        try:
            safe = InvoicePayload.model_validate({key: payload[key] for key in ("description", "amount", "currency")}).model_dump()
        except (ValidationError, KeyError, TypeError):
            raise BoundaryError(422, "schema_invalid") from None
        if Decimal(safe["amount"]) <= 0:
            raise BoundaryError(422, "invalid_amount")
        check_aup(safe["description"])
        return safe

    def review_invoice(self, session: Session, payload: dict, country_route: dict | None = None) -> dict:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            if not payload["confirm_sandbox_draft"]:
                raise BoundaryError(422, "sandbox_confirmation_required")
            safe_payload = self.invoice_payload(payload)
            evaluation_id = payload.get("evaluation_id")
            evaluation = self._require_aup_evaluation(session, evaluation_id, payload.get("description_digest"), now)
            actual = hashlib.sha256(safe_payload["description"].encode("utf-8")).hexdigest()
            if not safe_equal(evaluation["description_digest"], actual):
                raise BoundaryError(422, "aup_evaluation_binding_rejected")
            supplied = payload.get("acknowledgement_token")
            if evaluation["match_status"] == "REVIEW_SIGNAL":
                if supplied is None:
                    raise BoundaryError(422, "aup_acknowledgement_required")
                received = hashlib.sha256(supplied.encode("ascii")).hexdigest()
                if (evaluation["acknowledgement_digest"] is None or
                        not safe_equal(received, evaluation["acknowledgement_digest"])):
                    raise BoundaryError(422, "aup_acknowledgement_binding_rejected")
            elif supplied is not None:
                raise BoundaryError(422, "aup_acknowledgement_binding_rejected")
            live_reviews = {key: value for key, value in session.invoice_reviews.items() if value["expires_at"] > now}
            if len(live_reviews) >= 5:
                raise BoundaryError(429, "review_capacity")
            binding = {"evaluation_id": evaluation_id, "description_digest": evaluation["description_digest"],
                       "match_status": evaluation["match_status"], "warning_copy_version": "aup-warning-v1",
                       "acknowledgement_digest": evaluation["acknowledgement_digest"],
                       "acknowledged_at": iso(evaluation["acknowledged_at"]) if evaluation["acknowledged_at"] else None}
            if country_route is not None:
                binding["country_route"] = {"seller_country": country_route["seller_country"],
                                            "buyer_country": country_route["buyer_country"],
                                            "goods_tags": list(country_route.get("goods_tags") or [])}
            token = secrets.token_urlsafe(32)
            digest = payload_digest({"session_id": session.session_id, "action": "create_sandbox_invoice_draft",
                                     "payload": safe_payload, "aup_binding": binding})
            expires = min(session.expires_at, evaluation["expires_at"], now + timedelta(seconds=120))
            live_reviews[token] = {"digest": digest, "payload": safe_payload, "aup_binding": binding, "expires_at": expires}
            session.invoice_reviews = live_reviews
            del session.aup_evaluations[evaluation_id]
            if session.current_aup_evaluation_id == evaluation_id:
                session.current_aup_evaluation_id = None
            self._aup_event(session, evaluation_id, evaluation, "INVOICE_REVIEW_BOUND", now)
            return {"source": "synthetic", "review_token": token, "payload_digest": digest,
                    "expires_at": iso(expires), "action": "create_sandbox_invoice_draft", "authenticated_actor": False,
                    "policy_status": "manual_review", "advisory_only": True,
                    "limitations": ["Warning acknowledgement does not certify policy compliance or constitute PayPal review.",
                                    "Confirmation authorizes only one Sandbox draft creation, never invoice send."]}

    def consume_invoice(self, session: Session, request: dict) -> tuple[dict, str]:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            token = request["review_token"]
            review = session.invoice_reviews.get(token)
            if review is None or review["expires_at"] <= now:
                raise BoundaryError(422, "review_binding_rejected")
            payload = self.invoice_payload(request)
            expected = payload_digest({"session_id": session.session_id, "action": "create_sandbox_invoice_draft",
                                       "payload": payload, "aup_binding": review["aup_binding"]})
            if not safe_equal(review["digest"], request["payload_digest"]) or not safe_equal(expected, review["digest"]):
                raise BoundaryError(422, "review_binding_rejected")
            if session.invoice_attempts >= 5:
                raise BoundaryError(429, "invoice_attempt_limit")
            del session.invoice_reviews[token]
            session.invoice_attempts += 1
            if review["aup_binding"].get("country_route"):
                payload = dict(payload, country_route=review["aup_binding"]["country_route"])
            return payload, "pg-" + hashlib.sha256(token.encode()).hexdigest()[:32]
