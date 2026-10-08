"""Local authored review checklist, not a PayPal submission schema.

This module specifies intake shapes and review boundaries only. Import performs
no I/O. Accessors return defensive copies and never accept paths or callbacks.
Caller source/evidence labels cannot establish authenticity or action authority.
"""

from copy import deepcopy

from .dispute_evidence import (
    DISPUTE_REASONS,
    DISPUTE_STAGES,
    DISPUTE_STATUSES,
    EVIDENCE_STATES,
    LOCAL_EVIDENCE_TYPES,
    PROVIDER_EVIDENCE_TYPE_MAP,
    REASON_PROVIDER_EVIDENCE_TYPES,
)


CONTRACT_VERSION = "case-intake-us-v3"
SCHEMA_VERSION = 1
CORPUS_ID = "payguard-us-official-references-v2"
SOURCE_SHA256 = "72b7060a0f158f1102e813b8e62f9b6eeedbf5d61d3e91ed9dbfbd320427f77d"
CHUNKS_SHA256 = "802672744f1c824e662b16044f51f5c010e3ba78f2df50372d0aee833f5ac3b4"
OPERATIONAL_AUTHORITY = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"
THEMES = ("source_compliance", "velocity_guard", "dispute_mediation")
JURISDICTIONS = ("US",)
SOURCE_CLASSES = ("synthetic", "public_reference")
STATUSES = (
    "invalid_input", "needs_clarification", "needs_input",
    "manual_review", "ready_for_local_rules",
)
EVIDENCE_TYPES = LOCAL_EVIDENCE_TYPES
UNKNOWN = "UNKNOWN"


def _field(kind, *, required=False, allow_unknown=False, **limits):
    return dict(kind=kind, required=required, allow_unknown=allow_unknown,
                nullable=False, **limits)


def _identifier(*, required=False, allow_unknown=True):
    return _field("identifier", required=required, allow_unknown=allow_unknown,
                  max_chars=128, pattern=r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}")


def _time(*, required=False):
    return _field("aware_timestamp", required=required, allow_unknown=True,
                  max_chars=64, normalized_timezone="UTC",
                  pattern=r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})",
                  calendar_and_offset_validation="datetime.fromisoformat; aware offset required")


def _text(max_chars, *, required=False):
    return _field("text", required=required, allow_unknown=True,
                  min_chars=1, max_chars=max_chars, strip_for_blank_check=True)


def _enum(values, *, required=False, allow_unknown=True):
    return _field("enum", required=required, allow_unknown=allow_unknown,
                  values=list(values))


def _ref(*, required=False):
    return _field("evidence_id_ref", required=required, allow_unknown=True,
                  max_chars=128, pattern=r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}",
                  join="evidence_items.evidence_id")


def _decimal(*, required=False, allow_zero=False):
    return _field("decimal_string", required=required, allow_unknown=True,
                  max_chars=160, max_significant_digits=64,
                  max_absolute_exponent=100, finite=True,
                  minimum="0", minimum_inclusive=allow_zero,
                  pattern=r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


_REFERENCE = {
    "closed": True,
    "fields": {
        "source_id": _identifier(required=True, allow_unknown=False),
        "chunk_id": _field("chunk_id", required=True, max_chars=128,
                           pattern=r"[A-Z0-9-]{1,128}"),
    },
    "join": "fixed pinned corpus source_id/chunk_id pair",
}
_TRANSACTION = {
    "closed": True,
    "fields": {
        "order_id": _identifier(required=True, allow_unknown=False),
        "amount": _decimal(required=True),
        "currency": _field("currency", required=True, allow_unknown=True,
                           pattern=r"[A-Z]{3}", max_chars=3),
        "occurred_at": _time(required=True),
    },
    "unique_key": "order_id",
}
_EVIDENCE_ITEM = {
    "closed": True,
    "fields": {
        "evidence_id": _identifier(required=True, allow_unknown=False),
        "evidence_type": _enum(EVIDENCE_TYPES, required=True,
                               allow_unknown=False),
        "field_id": _field("field_id", required=True, max_chars=128,
                            vocabulary="exact field_ids for selected route"),
        "provider_request_id": _identifier(),
        "origin_ref": _field("reference_object", required=True,
                             allow_unknown=True, object_spec=_REFERENCE),
        "observed_at": _time(required=True),
        "evidence_state": _enum(EVIDENCE_STATES, required=True,
                                allow_unknown=False),
    },
    "unique_key": "evidence_id",
    "trust": "All caller labels unverified; source join proves identity only.",
}

_PROVIDER_EVIDENCE_REQUEST = {
    "closed": True,
    "fields": {
        "request_id": _identifier(required=True, allow_unknown=False),
        "evidence_type": _field("identifier", required=True, allow_unknown=False,
                                max_chars=128, pattern=r"[A-Z][A-Z0-9_]{0,127}"),
        "source": _field("identifier", required=True, allow_unknown=False,
                         max_chars=128, pattern=r"[A-Z][A-Z0-9_]{0,127}"),
        "mandatory": _field("strict_boolean", required=True),
        "action": _field("identifier", required=True, allow_unknown=False,
                         max_chars=128, pattern=r"[A-Z][A-Z0-9_]{0,127}"),
    },
    "unique_key": "request_id",
}
_COMMON = {
    "schema_version": _field("strict_integer", required=True, const=1),
    "intake_id": _identifier(required=True, allow_unknown=False),
    "requested_theme": _field("theme_selector", required=True, allow_unknown=True,
                              values=list(THEMES), max_chars=32, maximum_items=3,
                              accepted_shape="one known theme string only",
                              ambiguity_shapes="bounded unknown string or bounded list of theme strings",
                              unknown_or_multi_status="needs_clarification",
                              malformed_status="invalid_input",
                              dispatch_on_ambiguity=False),
    "request_kind": _enum(("reference_lookup", "check_activity",
                           "assess_velocity", "prepare_dispute_draft"),
                          required=True, allow_unknown=False),
    "jurisdiction": _enum(JURISDICTIONS, required=True),
    "as_of": _time(required=True),
    "observation_max_age_days": _field("strict_integer", required=True,
                                       minimum=0, maximum=365000),
    "source_class": _enum(SOURCE_CLASSES, required=True, allow_unknown=False),
    "payload": _field("route_payload_object", required=True),
    "evidence_items": _field("list", required=True, maximum_items=128,
                             item_spec=_EVIDENCE_ITEM),
    "references": _field("list", maximum_items=10, item_spec=_REFERENCE,
                         unique_key=("source_id", "chunk_id")),
}
_AUP = {
    "activity_description": _text(4000, required=True),
    "activity_category": _text(128, required=True),
    "approval_requirement": _enum(("REQUIRED", "NOT_APPLICABLE",
                                   "PROHIBITED", "UNKNOWN"), required=True),
    "approval_status": _enum(("NOT_OBTAINED", "CLAIMED_OBTAINED", "UNKNOWN")),
    "approval_evidence_ref": _ref(),
    "activity_evidence_ref": _ref(),
}
_VELOCITY = {
    "transactions": _field("list", required=True, maximum_items=10000,
                           item_spec=_TRANSACTION),
    "baseline_amount_per_hour": _decimal(required=True, allow_zero=True),
    "baseline_provenance": _enum(("SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED",
                                  "UNKNOWN"), required=True),
    "baseline_window_start": _time(),
    "baseline_window_end": _time(),
    "baseline_evidence_ref": _ref(),
    "window_hours": _field("strict_integer", required=True,
                           minimum=1, maximum=24),
    "threshold": _decimal(required=True),
    "limitation_review_requested": _field("strict_boolean"),
    "limitation_notice_ref": _ref(),
    "limitation_type": _enum(("FUNDS_HOLD", "ROLLING_RESERVE",
                              "ACCOUNT_LIMITATION", "PERMANENT_ACCOUNT_LIMITATION",
                              "UNKNOWN")),
    "limitation_status": _enum(("OBSERVED", "CLAIMED", "UNKNOWN")),
    "hold_started_at": _time(),
    "hold_expected_end_at": _time(),
    "kyc_request_status": _enum(("REQUESTED", "NOT_STATED", "UNKNOWN")),
    "kyc_response_status": _enum(("SUPPLIED", "NOT_SUPPLIED", "UNKNOWN")),
    "kyc_request_evidence_ref": _ref(),
    "fulfillment_review_requested": _field("strict_boolean"),
    "fulfillment_capacity_status": _enum(("SUPPLIED_UNVERIFIED", "UNKNOWN")),
    "fulfillment_evidence_ref": _ref(),
}
_DISPUTE = {
    "merchant_case_ref": _identifier(required=True),
    "order_id": _identifier(required=True),
    "reason_code": _enum(DISPUTE_REASONS + ("INR",), required=True,
                         allow_unknown=False),
    "opened_at": _time(required=True),
    "order_created_at": _time(required=True),
    "case_stage": _enum(DISPUTE_STAGES, required=True),
    "case_status": _enum(DISPUTE_STATUSES, required=True),
    "seller_response_due_date": _time(required=True),
    "available_actions": _field(
        "list", required=True, maximum_items=20, unique_items=True,
        item_spec=_field("identifier", allow_unknown=False, max_chars=128,
                         pattern=r"[A-Z][A-Z0-9_]{0,127}"),
    ),
    "evidences": _field("list", required=True, maximum_items=20,
                        item_spec=_PROVIDER_EVIDENCE_REQUEST,
                        unique_key="request_id"),
    "carrier_status": _enum(("delivered", "in_transit", "not_shipped",
                             "unknown", "UNKNOWN")),
    "delivered_at": _time(),
    "delivery_evidence_ref": _ref(),
    "fulfillment_evidence_ref": _ref(),
    "original_description_ref": _ref(),
    "claimed_mismatch_details": _text(2000),
    "return_claimed": _field("strict_boolean"),
    "return_status": _enum(("RETURNED", "NOT_RETURNED", "UNKNOWN")),
    "return_evidence_ref": _ref(),
    "refund_claimed": _field("strict_boolean"),
    "refund_status": _enum(("COMPLETED", "PENDING", "NOT_PROCESSED", "UNKNOWN")),
    "refund_evidence_ref": _ref(),
    "credit_owed_basis_ref": _ref(),
    "related_transaction_ref": _identifier(),
    "claimed_duplicate_details": _text(2000),
    "expected_amount": _decimal(allow_zero=True),
    "charged_amount": _decimal(allow_zero=True),
    "currency": _field("currency", allow_unknown=True,
                       pattern=r"[A-Z]{3}", max_chars=3),
    "price_basis_ref": _ref(),
    "other_payment_claim_details": _text(2000),
    "other_payment_status": _enum(("CLAIMED", "NOT_ESTABLISHED", "UNKNOWN")),
    "other_payment_evidence_ref": _ref(),
    "subscription_contract_ref": _ref(),
    "cancellation_status": _enum(("CLAIMED_CANCELED", "NOT_CANCELED", "UNKNOWN")),
    "canceled_at": _time(),
    "recurring_charge_at": _time(),
    "recurring_charge_ref": _identifier(),
    "other_reason_description": _text(2000),
    "case_details_ref": _ref(),
}


def _condition(field, equals, required):
    return {"when": {"field": field, "operator": "equals", "value": equals},
            "required": list(required), "unknown_handling": "needs_input"}


_REFUND_CONDITION = _condition("refund_claimed", True,
                               ("refund_status", "refund_evidence_ref"))
_RETURN_CONDITION = _condition("return_claimed", True,
                               ("return_status", "return_evidence_ref"))
_REASON_MATRIX = {
    "MERCHANDISE_OR_SERVICE_NOT_RECEIVED": {
        "required": [],
        "conditional": [],
        "evidence_types": ["DELIVERY", "FULFILLMENT"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["MERCHANDISE_OR_SERVICE_NOT_RECEIVED"]),
        "reference_chunk_id": "PP-REASONS-INR",
        "engine_support": "SYNTHETIC_INR_ONLY",
        "manual_if": {"carrier_status": ["in_transit", "not_shipped", "unknown"]},
        "boundary": "Undelivered does not require an invented delivered_at.",
    },
    "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED": {
        "required": [],
        "conditional": [],
        "evidence_types": ["DESCRIPTION", "RETURN", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED"]),
        "reference_chunk_id": "PP-REASONS-SNAD",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Mismatch allegations are not an established product defect.",
    },
    "UNAUTHORISED": {
        "required": [],
        "conditional": [],
        "evidence_types": ["FULFILLMENT", "DELIVERY", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["UNAUTHORISED"]),
        "reference_chunk_id": "PP-REASONS-UNAUTH",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Delivery cannot establish buyer authorization or intent.",
    },
    "CREDIT_NOT_PROCESSED": {
        "required": [],
        "conditional": [],
        "evidence_types": ["CREDIT_BASIS", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["CREDIT_NOT_PROCESSED"]),
        "reference_chunk_id": "PP-REASONS-CREDIT",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Claimed refund status is not verified provider settlement.",
    },
    "DUPLICATE_TRANSACTION": {
        "required": [],
        "conditional": [],
        "evidence_types": ["TRANSACTION", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["DUPLICATE_TRANSACTION"]),
        "reference_chunk_id": "PP-REASONS-DUPLICATE",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Related transaction linkage is an authored local checklist.",
    },
    "INCORRECT_AMOUNT": {
        "required": [],
        "conditional": [],
        "evidence_types": ["PRICE_BASIS", "TRANSACTION", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["INCORRECT_AMOUNT"]),
        "reference_chunk_id": "PP-REASONS-AMOUNT",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Compare finite Decimal values in one stated currency.",
    },
    "PAYMENT_BY_OTHER_MEANS": {
        "required": [],
        "conditional": [],
        "evidence_types": ["OTHER_PAYMENT", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["PAYMENT_BY_OTHER_MEANS"]),
        "reference_chunk_id": "PP-REASONS-OTHER-PAYMENT",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "An authored evidence checklist does not verify the other payment.",
    },
    "CANCELED_RECURRING_BILLING": {
        "required": [],
        "conditional": [],
        "evidence_types": ["SUBSCRIPTION", "CANCELLATION", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["CANCELED_RECURRING_BILLING"]),
        "reference_chunk_id": "PP-REASONS-SUBSCRIPTION",
        "engine_support": "REFERENCE_CHECKLIST_ONLY",
        "boundary": "Do not invent a cancellation date; check chronology when known.",
    },
    "OTHER": {
        "required": [],
        "conditional": [],
        "evidence_types": ["CASE_DETAILS", "OTHER", "REFUND"],
        "provider_evidence_types": list(REASON_PROVIDER_EVIDENCE_TYPES["OTHER"]),
        "reference_chunk_id": "PP-REASONS-OTHER",
        "engine_support": "MANUAL_REVIEW_ONLY",
        "boundary": "No automatic substitution to a different reason or INR.",
    },
}
_ROUTES = {
    "reference_lookup": {
        "themes": list(THEMES), "route": "reference_lookup",
        "payload": {"closed": True, "fields": {"query": _text(512, required=True)}},
        "conditional": [], "engine": None,
    },
    "check_activity": {
        "themes": ["source_compliance"], "route": "aup_checklist",
        "payload": {"closed": True, "fields": _AUP},
        "conditional": [_condition("approval_requirement", "REQUIRED",
                                   ("approval_status",)),
                        _condition("approval_status", "CLAIMED_OBTAINED",
                                   ("approval_evidence_ref",))],
        "manual_if": {"approval_requirement": ["PROHIBITED"],
                      "approval_status": ["NOT_OBTAINED"]},
        "engine": "check_aup advisory only; no keyword match is never compliant",
    },
    "assess_velocity": {
        "themes": ["velocity_guard"], "route": "velocity_checklist",
        "payload": {"closed": True, "fields": _VELOCITY},
        "conditional": [_condition("baseline_provenance", "SYNTHETIC_BASELINE",
                                   ("baseline_window_start", "baseline_window_end")),
                        _condition("baseline_provenance", "CALLER_SUPPLIED_UNVERIFIED",
                                   ("baseline_window_start", "baseline_window_end",
                                    "baseline_evidence_ref")),
                        _condition("limitation_review_requested", True,
                                   ("limitation_notice_ref", "limitation_type",
                                    "limitation_status")),
                        _condition("kyc_request_status", "REQUESTED",
                                   ("kyc_response_status", "kyc_request_evidence_ref")),
                        _condition("fulfillment_review_requested", True,
                                   ("fulfillment_capacity_status", "fulfillment_evidence_ref"))],
        "engine": "assess_velocity arithmetic only; no official freeze or AML prediction",
    },
    "prepare_dispute_draft": {
        "themes": ["dispute_mediation"], "route": "dispute_checklist",
        "payload": {"closed": True, "fields": _DISPUTE},
        "conditional": [], "reason_matrix": _REASON_MATRIX,
        "reason_aliases": {"INR": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"},
        "provider_evidence_type_map": dict(PROVIDER_EVIDENCE_TYPE_MAP),
        "engine": "prepare_dispute only after separately trusted synthetic INR boundary",
    },
}
for _route in _ROUTES.values():
    _route["field_ids"] = ["payload." + name for name in _route["payload"]["fields"]]
    if "transactions" in _route["payload"]["fields"]:
        _route["field_ids"] += ["payload.transactions[]." + name
                                 for name in _TRANSACTION["fields"]]

_ROUTES["reference_lookup"]["evidence_ref_types"] = {}
_ROUTES["check_activity"]["evidence_ref_types"] = {
    "approval_evidence_ref": ["APPROVAL"],
    "activity_evidence_ref": ["ACTIVITY"],
}
_ROUTES["assess_velocity"]["evidence_ref_types"] = {
    "baseline_evidence_ref": ["BASELINE"],
    "limitation_notice_ref": ["LIMITATION_NOTICE"],
    "kyc_request_evidence_ref": ["KYC_REQUEST"],
    "fulfillment_evidence_ref": ["FULFILLMENT"],
}
_ROUTES["prepare_dispute_draft"]["evidence_ref_types"] = {
    "delivery_evidence_ref": ["DELIVERY"],
    "fulfillment_evidence_ref": ["FULFILLMENT", "DELIVERY"],
    "original_description_ref": ["DESCRIPTION"],
    "return_evidence_ref": ["RETURN"],
    "refund_evidence_ref": ["REFUND"],
    "credit_owed_basis_ref": ["CREDIT_BASIS"],
    "price_basis_ref": ["PRICE_BASIS"],
    "other_payment_evidence_ref": ["OTHER_PAYMENT"],
    "subscription_contract_ref": ["SUBSCRIPTION"],
    "case_details_ref": ["CASE_DETAILS", "OTHER"],
}

_CONTRACT = {
    "version": CONTRACT_VERSION,
    "schema_version": SCHEMA_VERSION,
    "authored_requirement_basis": "LOCAL_REVIEW_CHECKLIST_NOT_PAYPAL_SUBMISSION_SCHEMA",
    "single_theme": True,
    "top_level_closed": True,
    "common_fields": _COMMON,
    "routes": _ROUTES,
    "statuses_in_precedence_order": list(STATUSES),
    "limits": {"utf8_bytes": 16384, "maximum_depth": 12,
               "maximum_total_nodes": 4096, "maximum_json_key_chars": 128,
               "reject_duplicate_keys": True, "reject_nonfinite": True,
               "reject_unknown_keys": True, "reject_controls_and_surrogates": True,
               "strict_integer_excludes_boolean": True,
               "pattern_semantics": "fullmatch", "field_paths": "closed vocabulary, never evaluated"},
    "diagnostics": {
        "field_locations": "Only fixed common field IDs, selected-route field_ids and fixed envelope/payload/evidence/reference container locations.",
        "unknown_key_handling": "Report the fixed known parent container with fixed unknown_field code; never echo caller key names or values.",
        "rejected_input_echo": False,
        "dynamic_field_access": False,
        "ambiguous_theme": "Unknown or multiple themes produce needs_clarification and no route, never a default theme. Malformed selector shape/type/bounds remains invalid_input.",
    },
    "unknown_semantics": {
        "sentinel": UNKNOWN, "nullable": False,
        "critical_unknown": "needs_input",
        "optional_unknown": "retain UNKNOWN; never coerce to false",
        "lowercase_carrier_unknown": "manual_review; delivery unconfirmed",
        "not_applicable": "Only explicit supported conditional states; never assume from omission.",
        "missing_conditional_trigger": "A missing optional trigger is not false and cannot assert that branch's evidence sufficiency.",
    },
    "status_semantics": {
        "invalid_input": "Malformed/unknown schema, duplicate key/ID, unjoined references, types, formats or bounds; no processing.",
        "needs_clarification": "Bounded unknown/multiple requested themes, contradictory facts, wrong theme-kind pair, region/source mismatch or temporal context conflict; no processing or default theme.",
        "needs_input": "Required field/conditional evidence missing or explicitly UNKNOWN; exact field IDs, no AI completion.",
        "manual_review": "Structurally complete but unsupported local engine, prohibited activity, insufficient baseline or scenario-specific unresolved evidence requires human review. Unknown authenticity alone does not prevent bounded reference or arithmetic checklist routing, and is never certified by ready status.",
        "ready_for_local_rules": "Shape/coherence sufficient only for an explicitly supported local checklist; human review remains mandatory.",
    },
    "coherence_rules": [
        {"id": "theme_kind", "check": "request_kind route themes contains requested_theme"},
        {"id": "reference_region", "check": "Each pinned reference matches explicit requested region/theme; no cross-region default."},
        {"id": "reference_dates", "check": "Saved retrieval/update dates not after as_of; unknown effective/decision dates retained, never invented."},
        {"id": "evidence_binding", "check": "Unique evidence_id and closed field_id belonging to selected route; every evidence_id_ref joins that field and required evidence type."},
        {"id": "velocity_currency", "check": "Validate all transaction rows, one currency; no conversion or omission of malformed out-of-window rows."},
        {"id": "velocity_baseline", "check": "Known baseline start < end <= observation start; synthetic and supplied baselines require complete windows; zero baseline manual_review/insufficient_baseline, no made-up ratio."},
        {"id": "velocity_window", "check": "Amount window is (as_of-window_hours,as_of]; count future/past exclusions explicitly if later arithmetic runs."},
        {"id": "dispute_chronology", "check": "order_created_at <= opened_at, seller_response_due_date is preserved, and delivered_at >= order_created_at if known; delivery after dispute possible but requires review, not impossible-event classification."},
        {"id": "provider_evidence_route", "check": "Only current payload.evidences entries whose source is REQUESTED_FROM_SELLER create seller evidence requirements; reason matrix entries absent from the response are never invented."},
        {"id": "carrier_time", "check": "Known delivered_at with not_shipped/in_transit contradicts carrier status; never correct automatically."},
        {"id": "cancellation_chronology", "check": "Known cancellation and recurring charge timestamps preserved; charge-before-cancellation does not prove unlawful recurring charge."},
        {"id": "amount_coherence", "check": "Finite nonnegative Decimal expected/charged amounts in one currency; equality does not establish complaint validity."},
    ],
    "review_gates": {
        "field_completeness": "COMPUTED_BY_LATER_PREFLIGHT_ONLY",
        "source_authenticity": "NOT_ESTABLISHED",
        "evidence_verification": "NOT_ESTABLISHED",
        "evidence_sufficiency": "NOT_ESTABLISHED",
        "current_policy_applicability": "NOT_ESTABLISHED",
        "actor_authorization": "NOT_ESTABLISHED",
        "external_action_authorization": "NOT_ESTABLISHED",
        "required_human_review": True,
        "operational_authority": OPERATIONAL_AUTHORITY,
    },
    "caller_trust": "source_class, approval and evidence states are untrusted claims. Filling them never establishes any review gate.",
    "engine_boundary": "This contract invokes no engine; reference_lookup is reference-only, public_reference never enters synthetic prepare_dispute, non-INR never maps to INR.",
    "corpus_binding": {"corpus_id": CORPUS_ID, "sources_sha256": SOURCE_SHA256,
                       "chunks_sha256": CHUNKS_SHA256},
    "limitations": [
        "This is an authored local review checklist, not complete official evidence requirements.",
        "Historical outcomes and court allegations do not establish present merchant facts or current jurisdiction-specific policy.",
        "Complete fields do not prove evidence authenticity, dispute victory, funds release or lack of money laundering.",
        "No model, DB, API/UI, actual PII, network, credentials, dependency changes or financial actions are authorized.",
    ],
}


def get_contract():
    """Return an independent JSON-serializable complete specification."""
    return deepcopy(_CONTRACT)


def get_route_spec(request_kind):
    """Return one defensive copy; reject dynamic keys without echoing input."""
    if type(request_kind) is not str or request_kind not in _ROUTES:
        raise ValueError("case_route_invalid")
    return deepcopy(_ROUTES[request_kind])


def get_reason_spec(reason_code):
    """Resolve only the fixed INR alias; never guess another reason."""
    if type(reason_code) is not str:
        raise ValueError("case_reason_invalid")
    canonical = ("MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
                 if reason_code == "INR" else reason_code)
    if canonical not in _REASON_MATRIX:
        raise ValueError("case_reason_invalid")
    return deepcopy(_REASON_MATRIX[canonical])
