"""Bounded, expiring synthetic sessions and payload-bound local review."""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hmac
import hashlib
import json
import secrets
import threading
from types import MappingProxyType

from payguard.engines import assess_velocity, check_aup, prepare_dispute
from payguard.case_cards import match_cases
from payguard.dispute_evidence import (
    DisputeEvidenceError,
    internal_review_narrative,
    restricted_evidence_digest,
    resolve_dispute_requirements,
)
from payguard.policy import POLICY_VERSION
from payguard.privacy import redact_identity
from payguard.document_privacy import redact_dispute_document
from payguard.review import LocalReviewGate, payload_digest
from pydantic import ValidationError
from .schemas import AupResponse, DisputeDraftResponse, InvoicePayload, ScenarioMatch


DEMO_VELOCITY_BASELINE = MappingProxyType({
    "amount_per_hour": "100.00",
    "provenance": "SYNTHETIC_BASELINE",
    "comparison_hours": 24,
    "observation_hours": 1,
})
AI_ATTEMPT_LIMIT = 3
AI_BRIEF_STAGES = frozenset({"source_compliance", "velocity_guard", "dispute_mediation"})


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


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
        "observation_max_age_days": 30,
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
    def __init__(self, status: int, code: str):
        self.status = status
        self.code = code
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
    aup_evaluations: dict[str, dict] = field(default_factory=dict)
    current_aup_evaluation_id: str | None = None
    aup_audit: deque = field(default_factory=lambda: deque(maxlen=30))
    invoice_reviews: dict[str, dict] = field(default_factory=dict)
    invoice_attempts: int = 0
    activity: list[dict] = field(default_factory=list)
    scenario: dict = field(default_factory=lambda: {"burst": False, "dispute": False})
    requests: deque = field(default_factory=deque)
    gate: LocalReviewGate = field(default_factory=LocalReviewGate, repr=False)


class SessionStore:
    def __init__(self, *, clock=utc_now, ttl_seconds=900, max_sessions=100, rate_limit=60,
                 ai_attempt_budget: AiAttemptBudget | None = None):
        self.clock = clock
        self.ttl_seconds = ttl_seconds
        self.max_sessions = max_sessions
        self.rate_limit = rate_limit
        self.sessions: dict[str, Session] = {}
        self.creation_requests: deque = deque()
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

    def create(self) -> dict:
        with self.lock:
            now = self._now()
            self._purge(now)
            self._rate(self.creation_requests, now, min(self.rate_limit, 30))
            if len(self.sessions) >= self.max_sessions:
                raise BoundaryError(429, "session_capacity")
            session = Session(secrets.token_urlsafe(32), secrets.token_urlsafe(32), now,
                              now + timedelta(seconds=self.ttl_seconds), now)
            self.sessions[session.session_id] = session
            return {"session_id": session.session_id, "csrf_token": session.csrf_token,
                    "source": "synthetic", "expires_at": iso(session.expires_at)}

    def _rate(self, requests: deque, now: datetime, limit: int):
        cutoff = now - timedelta(seconds=60)
        while requests and requests[0] <= cutoff:
            requests.popleft()
        if len(requests) >= limit:
            raise BoundaryError(429, "rate_limited")
        requests.append(now)

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
                           not hmac.compare_digest(csrf_token, session.csrf_token)):
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
                 "opened_at": case["opened_at"],
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
            return any(
                type(session.drafts.get(case_id, {}).get("routing")) is dict and
                session.drafts[case_id]["routing"].get("overall_state") == "READY_FOR_LOCAL_REVIEW" and
                session.disputes[case_id].get("reason") == "INR" and
                session.drafts[case_id].get("evidence", {}).get("reason") == "INR" and
                session.drafts[case_id]["routing"].get("reason") == "MERCHANDISE_OR_SERVICE_NOT_RECEIVED" and
                self._restricted_is_current(session, case_id) and
                session.draft_expires.get(case_id, now) > now
                for case_id in session.disputes
            )
        return False

    def ai_brief_allowed(self, session: Session, stage: str) -> bool:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            return self._ai_context_ready_locked(session, stage, now) and self.ai_attempt_budget.can_reserve(stage)

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
                session.invoice_reviews.clear()
                session.aup_evaluations.clear()
                session.current_aup_evaluation_id = None
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
                rows.extend({"order_id": f"demo-burst-{index:03d}", "amount": "10.00", "currency": "USD",
                             "occurred_at": iso(session.anchor - timedelta(minutes=index % 40))}
                            for index in range(1, 51))
            else:
                case = {"case_id": "demo-case-001", "order_id": "demo-dispute-order-001", "reason": "INR",
                        "order_created_at": iso(session.anchor - timedelta(days=3)),
                        "delivered_at": iso(session.anchor - timedelta(days=2)),
                        "opened_at": iso(session.anchor - timedelta(days=1)),
                        "carrier_status": "delivered", "evidence_source": "synthetic",
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
            if hmac.compare_digest(case_ref, expected):
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
                    response = DisputeDraftResponse.model_validate(
                        self._public_dispute_draft(draft, case_ref, digest)
                    ).model_dump()
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
                return DisputeDraftResponse.model_validate(
                    self._public_dispute_draft(draft, case_ref, digest)
                ).model_dump()
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
            if not hmac.compare_digest(current["draft_digest"], digest):
                raise BoundaryError(422, "review_binding_rejected")
            draft = session.drafts[case_id]
            approval = session.gate.approve(draft, actor="demo-reviewer", now=now)
            receipt = session.gate.consume(approval, draft, actor="demo-reviewer", now=now)
            session.approved.add(case_id)
            self._activity(session, "review", "Local synthetic draft reviewed; external submission frozen")
            receipt.pop("case_id", None)
            return dict(receipt, case_ref=case_ref, source="synthetic")

    def _expire_dispute_layers(self, session: Session, now: datetime):
        expired = [case_id for case_id, expires_at in session.draft_expires.items()
                   if expires_at <= now]
        for case_id in expired:
            session.drafts.pop(case_id, None)
            session.draft_expires.pop(case_id, None)
            session.restricted_evidence.pop(case_id, None)
            session.approved.discard(case_id)

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
                raise BoundaryError(429, "aup_capacity")
            evaluation = {"description_digest": digest, "match_status": result["match_status"],
                          "categories": tuple(item["category"] for item in result["findings"]),
                          "evaluated_at": now, "expires_at": expires, "acknowledgement_digest": None,
                          "acknowledged_at": None}
            live[evaluation_id] = evaluation
            session.aup_evaluations = live
            session.current_aup_evaluation_id = evaluation_id
            self._aup_event(session, evaluation_id, evaluation, "EVALUATED", now)
            return response

    def _require_aup_evaluation(self, session: Session, evaluation_id: str | None,
                                description_digest: str | None, now: datetime) -> dict:
        if evaluation_id is None or description_digest is None:
            raise BoundaryError(422, "aup_evaluation_required")
        evaluation = session.aup_evaluations.get(evaluation_id)
        if evaluation is None or not hmac.compare_digest(evaluation["description_digest"], description_digest):
            raise BoundaryError(422, "aup_evaluation_binding_rejected")
        if evaluation["expires_at"] <= now:
            raise BoundaryError(422, "aup_evaluation_expired")
        if now < evaluation["evaluated_at"]:
            raise BoundaryError(422, "aup_evaluation_binding_rejected")
        return evaluation

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

    def review_invoice(self, session: Session, payload: dict) -> dict:
        with self.lock:
            now = self._now()
            self._require_live_session(session, now)
            if not payload["confirm_sandbox_draft"]:
                raise BoundaryError(422, "sandbox_confirmation_required")
            safe_payload = self.invoice_payload(payload)
            evaluation_id = payload.get("evaluation_id")
            evaluation = self._require_aup_evaluation(session, evaluation_id, payload.get("description_digest"), now)
            actual = hashlib.sha256(safe_payload["description"].encode("utf-8")).hexdigest()
            if not hmac.compare_digest(evaluation["description_digest"], actual):
                raise BoundaryError(422, "aup_evaluation_binding_rejected")
            supplied = payload.get("acknowledgement_token")
            if evaluation["match_status"] == "REVIEW_SIGNAL":
                if supplied is None:
                    raise BoundaryError(422, "aup_acknowledgement_required")
                received = hashlib.sha256(supplied.encode("ascii")).hexdigest()
                if (evaluation["acknowledgement_digest"] is None or
                        not hmac.compare_digest(received, evaluation["acknowledgement_digest"])):
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
            if not hmac.compare_digest(review["digest"], request["payload_digest"]) or not hmac.compare_digest(expected, review["digest"]):
                raise BoundaryError(422, "review_binding_rejected")
            if session.invoice_attempts >= 5:
                raise BoundaryError(429, "invoice_attempt_limit")
            del session.invoice_reviews[token]
            session.invoice_attempts += 1
            return payload, "pg-" + hashlib.sha256(token.encode()).hexdigest()[:32]
