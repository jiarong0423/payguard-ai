"""Strict HTTP input and allowlisted response contracts."""

from typing import Annotated, Literal, Optional, Union
from datetime import date, datetime, timezone
import hashlib
import re
import unicodedata
from urllib.parse import urlsplit
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator, model_validator, ValidationInfo
from payguard.retrieval import CHUNKS_SHA256, MATERIAL_TYPES, SOURCE_SHA256, load_corpus


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class EmptyRequest(Contract):
    pass


class InjectRequest(Contract):
    scenario: Literal["burst", "dispute", "reset"]


class AupRequest(Contract):
    description: StrictStr = Field(min_length=1, max_length=4000)


class AupCategorySignalRequest(Contract):
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description: StrictStr = Field(min_length=1, max_length=4000)


class AupAcknowledgeRequest(Contract):
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    choice: Literal["RETURN_TO_EDIT", "CANCEL", "ACKNOWLEDGE_AND_CONTINUE"]


class ApproveRequest(Contract):
    draft_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")


# PayPal docs r24 (https://developer.paypal.com/api/rest/reference/currency-codes/): TWD, JPY and HUF do not support
# decimals, so their invoice amounts are whole numbers; USD keeps exactly two decimals.
ZERO_DECIMAL_CURRENCIES = frozenset({"TWD", "JPY", "HUF"})
INVOICE_WHOLE_UNITS_ERROR = "invoice_amount_whole_units"


class InvoicePayload(Contract):
    description: StrictStr = Field(min_length=1, max_length=200)
    amount: StrictStr = Field(pattern=r"^[0-9]{1,9}(?:\.[0-9]{1,2})?$")
    currency: Literal["USD", "TWD", "JPY", "HUF"]

    @model_validator(mode="after")
    def amount_matches_currency_decimals(self):
        if self.currency in ZERO_DECIMAL_CURRENCIES:
            if not re.fullmatch(r"[0-9]{1,9}", self.amount):
                raise ValueError(INVOICE_WHOLE_UNITS_ERROR)
        elif not re.fullmatch(r"[0-9]{1,7}\.[0-9]{2}", self.amount):
            raise ValueError("invoice_amount_two_decimals")
        return self


class InvoiceReviewRequest(InvoicePayload):
    confirm_sandbox_draft: StrictBool
    evaluation_id: StrictStr | None = Field(default=None, min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description_digest: StrictStr | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    acknowledgement_token: StrictStr | None = Field(default=None, min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class InvoiceDraftRequest(InvoicePayload):
    review_token: StrictStr = Field(min_length=32, max_length=128)
    payload_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")


class HealthResponse(Contract):
    status: Literal["ok"]
    mode: Literal["demo"]
    version: str
    source: Literal["synthetic"]


class ConnectionsResponse(Contract):
    """Deployment mode only. Never a key, a key's presence, a value or a variable name."""
    mode: Literal["local", "hosted_demo"]
    # Present (true) only on the hosted demo with PAYGUARD_HOSTED_READONLY_SANDBOX=enabled: real read-only Sandbox calls.
    sandbox_reads: bool | None = None


class SessionResponse(Contract):
    session_id: str
    csrf_token: str
    source: Literal["synthetic"]
    expires_at: str


class Transaction(Contract):
    order_id: str
    amount: str
    currency: str
    occurred_at: str


class Finding(Contract):
    category: Literal["unsupported_financial_promise", "weapons", "controlled_substances", "counterfeit_goods", "regulated_activity"]
    code: Literal["keyword_requires_policy_review"]


class AupResponse(Contract):
    match_status: Literal["NO_MATCH", "REVIEW_SIGNAL"]
    compliance_decision: Literal["NOT_MADE"]
    current_policy_applicability: Literal["NOT_ESTABLISHED"]
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    evaluated_at: str
    expires_at: str
    warning_copy_version: Literal["aup-warning-v1"]
    policy_url: Literal["https://www.paypal.com/us/legalhub/paypal/acceptableuse-full"]
    findings: list[Finding]
    recommendation: StrictStr = Field(min_length=1, max_length=1000)
    policy_version: StrictStr = Field(min_length=1, max_length=128)
    advisory_only: Literal[True]
    source: Literal["synthetic"]


    @field_validator("recommendation", "policy_version")
    @classmethod
    def aup_output_text(cls, value: str, info: ValidationInfo) -> str:
        try:
            value.encode("utf-8")
            units = len(value.encode("utf-16-le")) // 2
        except UnicodeError:
            raise ValueError("aup_output_text_encoding_invalid") from None
        limit = 1000 if info.field_name == "recommendation" else 128
        if units > limit:
            raise ValueError("aup_output_text_limit")
        return value


class CategorySignal(Contract):
    category: StrictStr | None = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9][A-Za-z0-9 &'\-,./+()]*$")
    confidence: Literal["HIGH", "LOW"] | None
    source: Literal["channel3"]

    @model_validator(mode="after")
    def category_and_confidence_together(self):
        if (self.category is None) != (self.confidence is None):
            raise ValueError("category_signal_incomplete")
        return self


class AupCategorySignalResponse(Contract):
    """Optional Channel3 signal shown next to the AUP result; it never changes the rule decision."""
    status: Literal["OFF", "SIGNAL", "NOT_SENT", "UNAVAILABLE"]
    signal: CategorySignal | None
    reason: Literal["nothing_to_send", "budget_exhausted", "timeout", "upstream_error", "contract_rejected"] | None
    affects_decision: Literal[False]

    @model_validator(mode="after")
    def status_shape(self):
        if (self.status == "SIGNAL") != (self.signal is not None):
            raise ValueError("category_signal_status_mismatch")
        if (self.status in ("NOT_SENT", "UNAVAILABLE")) != (self.reason is not None):
            raise ValueError("category_signal_reason_mismatch")
        return self


_CARD_TEXT = r"^[A-Za-z0-9 &'\-,./+()%\"]+$"


class ProductCard(Contract):
    """A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links."""
    product_id: StrictStr = Field(pattern=r"^[A-Za-z0-9_.:-]{1,64}$")
    title: StrictStr = Field(min_length=2, max_length=120, pattern=_CARD_TEXT)
    brand: StrictStr | None = Field(min_length=2, max_length=60, pattern=_CARD_TEXT)
    category: StrictStr | None = Field(min_length=2, max_length=80, pattern=_CARD_TEXT)
    key_features: list[Annotated[StrictStr, Field(min_length=2, max_length=100, pattern=_CARD_TEXT)]] = Field(max_length=4)
    materials: list[Annotated[StrictStr, Field(min_length=2, max_length=40, pattern=_CARD_TEXT)]] = Field(max_length=4)
    image_url: StrictStr | None = Field(max_length=500, pattern=r"^https://[^\s@]+$")


class ProductReferenceRequest(Contract):
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description: StrictStr = Field(min_length=1, max_length=4000)


class ProductReferenceResponse(Contract):
    """Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision."""
    status: Literal["OFF", "FOUND", "NOT_FOUND", "NOT_SENT", "UNAVAILABLE"]
    source: Literal["channel3_live", "channel3_recorded"] | None
    cards: list[ProductCard] = Field(max_length=3)
    reason: Literal["nothing_to_send", "not_recorded", "budget_exhausted", "timeout", "upstream_error",
                    "contract_rejected"] | None
    recorded_at: StrictStr | None = Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    affects_decision: Literal[False]

    @model_validator(mode="after")
    def status_shape(self):
        if (self.status == "FOUND") != bool(self.cards):
            raise ValueError("product_reference_cards_mismatch")
        if (self.status in ("FOUND", "NOT_FOUND")) != (self.source is not None):
            raise ValueError("product_reference_source_mismatch")
        if (self.status in ("NOT_SENT", "UNAVAILABLE")) != (self.reason is not None):
            raise ValueError("product_reference_reason_mismatch")
        if (self.source == "channel3_recorded") != (self.recorded_at is not None):
            raise ValueError("product_reference_recorded_mismatch")
        if len({card.product_id for card in self.cards}) != len(self.cards):
            raise ValueError("product_reference_duplicate")
        return self


class ProductConfirmRequest(Contract):
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description: StrictStr = Field(min_length=1, max_length=4000)
    product_id: StrictStr | None = Field(pattern=r"^[A-Za-z0-9_.:-]{1,64}$")


class ProductConfirmResponse(Contract):
    """The seller's own choice: one of the cards they were shown, or none of them."""
    choice: Literal["CONFIRMED", "NONE_MATCH"]
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    source: Literal["channel3_live", "channel3_recorded"]
    recorded_at: StrictStr | None = Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    card: ProductCard | None
    card_digest: StrictStr | None = Field(pattern=r"^[a-f0-9]{64}$")
    confirmed_by: Literal["seller"]
    affects_decision: Literal[False]

    @model_validator(mode="after")
    def choice_shape(self):
        if (self.choice == "CONFIRMED") != (self.card is not None) or (self.card is None) != (self.card_digest is None):
            raise ValueError("product_confirm_shape")
        return self


class CaseRouteRequest(Contract):
    text: StrictStr = Field(min_length=1, max_length=200)


class CaseRouteMatch(Contract):
    product_id: StrictStr = Field(pattern=r"^[A-Za-z0-9_.:-]{1,64}$")
    title: StrictStr = Field(min_length=2, max_length=120, pattern=_CARD_TEXT)
    category: StrictStr | None = Field(min_length=2, max_length=80, pattern=_CARD_TEXT)
    score: float = Field(ge=0, le=1)
    exact_words: list[Annotated[StrictStr, Field(min_length=1, max_length=40, pattern=r"^[a-z0-9]+$")]] = Field(max_length=8)
    match_type: Literal["exact", "close"]


class CaseRouteResponse(Contract):
    """Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only."""
    query: StrictStr | None = Field(max_length=120)
    route: Literal["physical", "digital", "service", "unknown"]
    reason: Literal["catalogue_match", "live_catalogue_match", "digital_word", "service_word", "filtered_conflict",
                    "no_close_match", "nothing_to_match"]
    matched_word: StrictStr | None = Field(max_length=40)
    matches: list[CaseRouteMatch] = Field(max_length=3)
    filtered_out: StrictInt = Field(ge=0, le=1000)
    items: list[StrictStr] = Field(max_length=12)
    decided_by: Literal["code"]
    affects_decision: Literal[False]

    @model_validator(mode="after")
    def route_shape(self):
        if (self.route == "physical") != bool(self.matches):
            raise ValueError("case_route_matches_mismatch")
        if (self.route in ("digital", "service")) != (self.matched_word is not None):
            raise ValueError("case_route_word_mismatch")
        if (self.route in ("physical", "digital")) != bool(self.items):
            raise ValueError("case_route_items_mismatch")
        return self


class AupAcknowledgeResponse(Contract):
    source: Literal["synthetic"]
    evaluation_id: StrictStr = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    description_digest: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")
    choice: Literal["RETURN_TO_EDIT", "CANCEL", "ACKNOWLEDGE_AND_CONTINUE"]
    acknowledgement_token: StrictStr | None = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    expires_at: str | None
    warning_copy_version: Literal["aup-warning-v1"]
    compliance_decision: Literal["NOT_MADE"]
    external_action_authorized: Literal[False]


class VelocityResponse(Contract):
    status: Literal["normal", "review_velocity", "insufficient_baseline"]
    window_start: str
    window_end: str
    window_hours: int
    window_boundary: Literal["left_open_right_closed"]
    transaction_count: int
    excluded_future_count: int
    excluded_past_count: int
    currency: str | None
    total_amount: str
    current_amount_per_hour: str
    baseline_amount_per_hour: str
    baseline_provenance: Literal["SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED"]
    baseline_window_start: str
    baseline_window_end: str
    ratio: str | None
    threshold: str
    alert: bool
    policy_version: str
    advisory_only: Literal[True]
    limitations: list[str]

class SyntheticMoney(Contract):
    """Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic."""
    currency_code: StrictStr = Field(pattern=r"^[A-Z]{3}$")
    value: StrictStr = Field(pattern=r"^[0-9]{1,10}(?:\.[0-9]{1,2})?$")


class DisputeSummary(Contract):
    case_ref: str
    order_ref: str
    reason: str
    opened_at: str
    # The synthetic case's own response deadline, so each card can say how many days are left (UI/UX r16 P1).
    seller_response_due_date: str
    dispute_amount: SyntheticMoney
    status: Literal["needs_review", "draft_ready", "local_draft_reviewed"]


class Activity(Contract):
    id: str
    at: str
    kind: str
    label: str
    source: Literal["synthetic"]


class Scenario(Contract):
    burst: bool
    dispute: bool


class StateResponse(Contract):
    session_id: str
    source: Literal["synthetic"]
    policy_version: str
    transactions: list[Transaction]
    velocity: VelocityResponse
    disputes: list[DisputeSummary]
    activity: list[Activity]
    scenario: Scenario
    expires_at: str


class Evidence(Contract):
    reason: str | None = None
    opened_at: str | None = None
    order_created_at: str | None = None
    carrier_status: str | None = None
    delivered_at: str | None = None
    evidence_source: Literal["synthetic"]


class IdentityTokens(Contract):
    name_token: str
    address_token: str
    email_token: str


class IdentityRedaction(Contract):
    method: Literal["HMAC-SHA256 pseudonymization"]
    fields: list[Literal["name", "address", "email"]]
    tokens: IdentityTokens
    synthetic: Literal[True]


DocumentRedactionType = Literal["email", "us_phone", "id_like", "name", "address", "manual", "mixed"]


class DocumentRedaction(Contract):
    export_profile: Literal["INTERNAL_REVIEW_ONLY_V1"]
    redacted_text: StrictStr = Field(max_length=32768)
    replacement_count: StrictInt = Field(ge=0, le=128)
    counts: dict[DocumentRedactionType, Annotated[StrictInt, Field(ge=1, le=128)]]
    types: list[DocumentRedactionType] = Field(max_length=7)
    method: Literal["HMAC-SHA256 document pseudonymization v1"]
    limited_detection: Literal[True]
    manual_review_required: Literal[True]
    source: Literal["synthetic"]
    reversibility: Literal[False]
    limitations: list[Annotated[StrictStr, Field(min_length=1, max_length=1000)]] = Field(min_length=1, max_length=8)

    @model_validator(mode="before")
    @classmethod
    def exact_flags(cls, value):
        if type(value) is not dict:
            raise ValueError("document_redaction_invalid")
        for field, expected in (("limited_detection", True), ("manual_review_required", True), ("reversibility", False)):
            if type(value.get(field)) is not bool or value[field] is not expected:
                raise ValueError("document_redaction_invalid")
        return value

    @model_validator(mode="after")
    def coherent(self):
        if (self.types != sorted(self.counts) or sum(self.counts.values()) != self.replacement_count or
                type(self.limited_detection) is not bool or type(self.manual_review_required) is not bool or
                type(self.reversibility) is not bool):
            raise ValueError("document_redaction_invalid")
        try:
            if len(self.redacted_text.encode("utf-8")) > 32768:
                raise ValueError("document_redaction_invalid")
        except UnicodeError:
            raise ValueError("document_redaction_invalid") from None
        return self


class DisputeApprovalResponse(Contract):
    case_ref: str
    action: Literal["review_draft"]
    status: Literal["local_draft_reviewed"]
    external_submission: Literal["FROZEN"]
    authenticated_actor: Literal[False]
    durable_approval: Literal[False]
    reviewer: Literal["DEMO_OPERATOR_UNAUTHENTICATED"]
    reviewed_at: datetime
    retention: Literal["SESSION_MEMORY_ONLY"]
    source: Literal["synthetic"]


# PayPal-Debug-Id response header (PayPal docs r24): a plain alphanumeric correlation id, never a token.
PAYPAL_DEBUG_ID_PATTERN = r"^[A-Za-z0-9]{6,64}$"


class SandboxEvidenceReceipt(Contract):
    schema_version: Literal[1]
    paypal_debug_id: StrictStr | None = Field(pattern=PAYPAL_DEBUG_ID_PATTERN)
    environment: Literal["sandbox"]
    action: Literal["OAUTH_CONNECT", "CREATE_INVOICE_DRAFT"]
    status: Literal["CONNECTED", "DRAFT"]
    observed_at: StrictStr = Field(min_length=20, max_length=27)
    invoice_id: StrictStr | None = Field(min_length=13, max_length=69, pattern=r"^INV2-[A-Z0-9-]{8,64}$")
    evidence_class: Literal["AUTHENTIC_SANDBOX_RESPONSE", "SYNTHETIC_TEST_RESPONSE"]
    proof_kind: Literal["POST_RESPONSE_ONLY"]
    separate_get_readback: Literal[False]
    external_send: Literal["FROZEN"]

    @model_validator(mode="before")
    @classmethod
    def exact_primitives(cls, value):
        if type(value) is not dict or type(value.get("schema_version")) is not int or value.get("schema_version") != 1:
            raise ValueError("sandbox_receipt_invalid")
        if type(value.get("separate_get_readback")) is not bool or value.get("separate_get_readback") is not False:
            raise ValueError("sandbox_receipt_invalid")
        return value

    @field_validator("observed_at")
    @classmethod
    def utc_timestamp(cls, value):
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z", value):
            raise ValueError("sandbox_receipt_invalid")
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, OverflowError):
            raise ValueError("sandbox_receipt_invalid") from None
        return value

    @model_validator(mode="after")
    def action_binding(self):
        if self.action == "OAUTH_CONNECT":
            if self.status != "CONNECTED" or self.invoice_id is not None:
                raise ValueError("sandbox_receipt_invalid")
        elif self.status != "DRAFT" or self.invoice_id is None:
            raise ValueError("sandbox_receipt_invalid")
        return self


class PaypalStatusResponse(Contract):
    configured: bool
    status: Literal["not_configured", "disconnected", "connected", "error"]
    environment: Literal["sandbox"]
    last_verified_at: str | None
    source: Literal["paypal_sandbox"]
    evidence_receipt: SandboxEvidenceReceipt | None

    @model_validator(mode="after")
    def connection_receipt_binding(self):
        if self.status == "connected":
            if (not self.configured or self.evidence_receipt is None or
                    self.evidence_receipt.action != "OAUTH_CONNECT" or
                    self.evidence_receipt.observed_at != self.last_verified_at):
                raise ValueError("sandbox_receipt_invalid")
        elif self.evidence_receipt is not None:
            raise ValueError("sandbox_receipt_invalid")
        return self


class InvoiceReviewResponse(Contract):
    source: Literal["synthetic"]
    review_token: str
    payload_digest: str
    expires_at: str
    action: Literal["create_sandbox_invoice_draft"]
    authenticated_actor: Literal[False]
    policy_status: Literal["manual_review"]
    advisory_only: Literal[True]
    limitations: list[str]


class InvoiceDraftResponse(Contract):
    source: Literal["paypal_sandbox"]
    invoice_id: StrictStr = Field(min_length=13, max_length=69, pattern=r"^INV2-[A-Z0-9-]{8,64}$")
    status: Literal["DRAFT"]
    environment: Literal["sandbox"]
    external_send: Literal["FROZEN"]
    evidence_receipt: SandboxEvidenceReceipt

    @model_validator(mode="after")
    def creation_receipt_binding(self):
        if self.evidence_receipt.action != "CREATE_INVOICE_DRAFT" or self.evidence_receipt.invoice_id != self.invoice_id:
            raise ValueError("sandbox_receipt_invalid")
        return self


class WebhookEnvelope(Contract):
    """The verify request envelope (PayPal docs r24: transmission_id <= 50, cert_url <= 500 characters).

    webhook_event is checked to be an object only; the adapter forwards its original raw text, never this parse.
    """
    transmission_id: StrictStr = Field(pattern=r"^[A-Za-z0-9_.:-]{1,50}$")
    transmission_time: StrictStr = Field(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})$")
    cert_url: StrictStr = Field(max_length=500, pattern=r"^https://api(?:-m)?\.sandbox\.paypal\.com/v1/notifications/certs/[A-Za-z0-9._-]{1,400}$")
    auth_algo: Literal["SHA256withRSA"]
    transmission_sig: StrictStr = Field(pattern=r"^[A-Za-z0-9+/=_-]{1,4096}$")
    webhook_event: dict


_WEBHOOK_VALUE = r"^[A-Za-z0-9_.:-]{1,128}$"


class WebhookEventProjection(Contract):
    """All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary."""
    id: StrictStr | None = Field(pattern=_WEBHOOK_VALUE)
    event_type: StrictStr | None = Field(pattern=_WEBHOOK_VALUE)
    resource_type: StrictStr | None = Field(pattern=_WEBHOOK_VALUE)
    resource_id: StrictStr | None = Field(pattern=_WEBHOOK_VALUE)
    resource_status: StrictStr | None = Field(pattern=_WEBHOOK_VALUE)


class WebhookVerifyResponse(Contract):
    source: Literal["paypal_sandbox"]
    verification_status: Literal["SUCCESS"]
    imported_into_demo: Literal[False]
    event: WebhookEventProjection
    paypal_debug_id: StrictStr | None = Field(pattern=PAYPAL_DEBUG_ID_PATTERN)


DISPUTE_ID_PATTERN = r"^PP-[A-Z0-9][A-Z0-9-]{2,62}$"
_UPPER_TOKEN = r"^[A-Z][A-Z0-9_]{0,63}$"
_PROVIDER_TIME = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$"
DisputeSource = Literal["paypal_sandbox", "synthetic_fixture"]
DisputeEvidenceClass = Literal["AUTHENTIC_SANDBOX_RESPONSE", "SYNTHETIC_TEST_RESPONSE", "SYNTHETIC_FIXTURE"]


class ProviderMoney(Contract):
    currency_code: StrictStr = Field(pattern=r"^[A-Z]{3}$")
    value: StrictStr = Field(pattern=r"^[0-9]{1,10}(?:\.[0-9]{1,2})?$")


class DisputeRecord(Contract):
    dispute_id: StrictStr = Field(pattern=DISPUTE_ID_PATTERN)
    reason: Literal[
        "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
        "UNAUTHORISED", "CREDIT_NOT_PROCESSED", "DUPLICATE_TRANSACTION",
        "INCORRECT_AMOUNT", "PAYMENT_BY_OTHER_MEANS", "CANCELED_RECURRING_BILLING", "OTHER",
    ]
    status: Literal[
        "OPEN", "WAITING_FOR_SELLER_RESPONSE", "WAITING_FOR_BUYER_RESPONSE",
        "UNDER_REVIEW", "RESOLVED", "CLOSED", "UNKNOWN",
    ]
    dispute_life_cycle_stage: Literal["INQUIRY", "CHARGEBACK", "PRE_ARBITRATION", "ARBITRATION", "UNKNOWN"]
    dispute_state: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    dispute_amount: ProviderMoney
    create_time: StrictStr = Field(pattern=_PROVIDER_TIME)
    update_time: StrictStr | None = Field(default=None, pattern=_PROVIDER_TIME)
    seller_response_due_date: StrictStr | None = Field(default=None, pattern=_PROVIDER_TIME)


class DisputeEnvelope(Contract):
    source: DisputeSource
    data_source_label: Literal["Sandbox", "Fixture"]
    environment: Literal["sandbox"]
    evidence_class: DisputeEvidenceClass
    observed_at: StrictStr = Field(min_length=20, max_length=27)
    provider_submission: Literal["NOT_PERFORMED", "PERFORMED"]
    # PayPal-Debug-Id of the Sandbox call behind this answer (PayPal docs r24); always null for the fixture.
    paypal_debug_id: StrictStr | None = Field(default=None, pattern=PAYPAL_DEBUG_ID_PATTERN)

    @model_validator(mode="after")
    def source_binding(self):
        if (self.source == "synthetic_fixture") != (self.evidence_class == "SYNTHETIC_FIXTURE"):
            raise ValueError("dispute_source_invalid")
        if self.source == "synthetic_fixture" and self.paypal_debug_id is not None:
            raise ValueError("dispute_source_invalid")
        if (self.source == "synthetic_fixture") != (self.data_source_label == "Fixture"):
            raise ValueError("dispute_source_invalid")
        return self


class DisputeListResponse(DisputeEnvelope):
    readback: Literal["GET_LIST"]
    items: list[DisputeRecord] = Field(max_length=20)

    @model_validator(mode="after")
    def unique_and_frozen(self):
        if self.provider_submission != "NOT_PERFORMED":
            raise ValueError("dispute_source_invalid")
        if len({row.dispute_id for row in self.items}) != len(self.items):
            raise ValueError("dispute_source_invalid")
        return self


class DisputedTransaction(Contract):
    seller_transaction_id: StrictStr = Field(pattern=r"^[A-Za-z0-9._-]{1,64}$")
    transaction_status: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    gross_amount: ProviderMoney | None = None
    seller_protection_eligible: StrictBool | None = None


class DisputeEvidenceRow(Contract):
    evidence_type: StrictStr = Field(pattern=_UPPER_TOKEN)
    source: Literal[
        "REQUESTED_FROM_SELLER", "REQUESTED_FROM_BUYER", "SUBMITTED_BY_SELLER",
        "SUBMITTED_BY_BUYER", "SUBMITTED_BY_PARTNER", "UNKNOWN",
    ]
    action: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    date: StrictStr | None = Field(default=None, pattern=_PROVIDER_TIME)


class DisputeDetailResponse(DisputeEnvelope, DisputeRecord):
    readback: Literal["GET_DETAIL"]
    dispute_channel: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    disputed_transactions: list[DisputedTransaction] = Field(max_length=10)
    evidences: list[DisputeEvidenceRow] = Field(max_length=20)

    @model_validator(mode="after")
    def frozen_readback(self):
        if self.provider_submission != "NOT_PERFORMED":
            raise ValueError("dispute_source_invalid")
        return self


# (r30 J2 P2-1) Single-use send confirmation the preview issues; a send must carry the latest one.
CONFIRM_TOKEN_PATTERN = r"^[A-Za-z0-9_-]{32}$"


class ProvideEvidenceRequest(Contract):
    dispute_id: StrictStr = Field(pattern=DISPUTE_ID_PATTERN)
    case_ref: StrictStr = Field(pattern=r"^case-ref-[0-9]{3}$")
    submit: StrictBool = False
    confirm_token: StrictStr | None = Field(default=None, pattern=CONFIRM_TOKEN_PATTERN)


# A subset of the PayPal carrier enum (PayPal docs r24, customer-disputes/v1 schema.json); any other carrier is sent as
# OTHER with carrier_name_other.
PAYPAL_CARRIERS = ("USPS", "UPS", "FEDEX", "DHL", "TW_CHUNGHWA_POST", "JP_JAPANPOST")
# PayPal docs r24 (supported-file-types-sizes): JPG, JPEG, GIF, PNG and PDF; each under 10 MB, 50 MB per call.
EVIDENCE_MEDIA_TYPES = ("image/jpeg", "image/gif", "image/png", "application/pdf")
EVIDENCE_FILE_MAX_BYTES = 10_000_000
EVIDENCE_TOTAL_MAX_BYTES = 50_000_000


class TrackingInfo(Contract):
    carrier_name: Literal["USPS", "UPS", "FEDEX", "DHL", "TW_CHUNGHWA_POST", "JP_JAPANPOST", "OTHER"]
    carrier_name_other: StrictStr | None = Field(default=None, min_length=1, max_length=64)
    tracking_number: StrictStr = Field(min_length=1, max_length=64)

    @model_validator(mode="after")
    def other_needs_name(self):
        # PayPal docs r24: carrier_name OTHER requires carrier_name_other; a named carrier carries none.
        if (self.carrier_name == "OTHER") != (self.carrier_name_other is not None):
            raise ValueError("carrier_invalid")
        return self


class EvidenceInfo(Contract):
    tracking_info: list[TrackingInfo] = Field(max_length=10)


class EvidenceInputItem(Contract):
    evidence_type: StrictStr = Field(pattern=_UPPER_TOKEN)
    evidence_info: EvidenceInfo
    notes: StrictStr = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def fulfillment_has_tracking(self):
        # PayPal docs r24: PROOF_OF_FULFILLMENT carries 1-10 tracking_info items.
        if self.evidence_type == "PROOF_OF_FULFILLMENT" and not 1 <= len(self.evidence_info.tracking_info) <= 10:
            raise ValueError("tracking_info_required")
        return self


class EvidenceInput(Contract):
    evidences: list[EvidenceInputItem] = Field(min_length=1, max_length=20)


class MultipartFilePart(Contract):
    name: StrictStr = Field(pattern=r"^file[0-9]{1,3}$")
    filename: StrictStr = Field(max_length=255)
    content_type: Literal["image/jpeg", "image/gif", "image/png", "application/pdf"]
    byte_length: StrictInt = Field(ge=0, lt=10_000_000)


class SentFileFingerprint(Contract):
    """Plain SHA-256 of one file's exact bytes, recorded at the moment of a send so a later read-back can be compared.

    The keyed ``payload_sha256`` cannot be checked outside the session; this one can. Never present on a preview."""
    filename: StrictStr = Field(max_length=255)
    content_type: Literal["image/jpeg", "image/gif", "image/png", "application/pdf"]
    byte_length: StrictInt = Field(ge=0, lt=10_000_000)
    sha256: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")


class SendGuard(Contract):
    """(r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4)."""
    case_ref: StrictStr = Field(pattern=r"^case-ref-[0-9]{3}$")
    case_reason: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    dispute_masked: StrictStr = Field(pattern=r"^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}|\u2026)$")
    dispute_reason: StrictStr | None = Field(default=None, pattern=_UPPER_TOKEN)
    dispute_amount: ProviderMoney | None = None
    bound_dispute_masked: StrictStr | None = Field(default=None, pattern=r"^(?:PP-[A-Z0-9-]{2}\u2026[A-Z0-9-]{2}|\u2026)$")
    sending_account_masked: StrictStr | None = Field(default=None, pattern=r"^(?:[0-9A-Za-z]{2}\u2026[0-9A-Za-z]{4}|\u2026)$")
    dispute_seller_masked: StrictStr | None = Field(default=None, pattern=r"^(?:[0-9A-Za-z]{2}\u2026[0-9A-Za-z]{4}|\u2026)$")
    account_status: Literal["MATCH", "MISMATCH", "UNKNOWN"]
    # (r35 #2) Also why the session's last detail read rules out an evidence send (no confirmation, no pair).
    send_refusal: Literal["account_identity_unknown", "dispute_not_this_account", "dispute_detail_required",
                          "seller_evidence_already_submitted", "dispute_not_awaiting_seller",
                          "dispute_evidence_not_offered"] | None = None


class ProvideEvidenceResponse(DisputeEnvelope):
    readback: Literal["PROVIDE_EVIDENCE_PREVIEW", "PROVIDE_EVIDENCE_SUBMITTED"]
    dispute_id: StrictStr = Field(pattern=DISPUTE_ID_PATTERN)
    case_ref: StrictStr = Field(pattern=r"^case-ref-[0-9]{3}$")
    method: Literal["POST"]
    path: StrictStr = Field(pattern=r"^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$")
    content_type: Literal["multipart/form-data"]
    input: EvidenceInput
    files: list[MultipartFilePart] = Field(max_length=20)
    external_send: Literal["FROZEN", "SUBMITTED"]
    submit_flag_enabled: StrictBool
    human_review_required: Literal[True]
    # (optimise r24) Keyed SHA-256 of the exact multipart parts a send carries; null while the files cannot be built.
    payload_sha256: StrictStr | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    send_guard: SendGuard
    # (r30 J2 P2-1) Issued by a preview whose payload can be sent; null on a send and while nothing can be sent.
    confirm_token: StrictStr | None = Field(default=None, pattern=CONFIRM_TOKEN_PATTERN)
    # (2026-11-09) Plain SHA-256 of each file's bytes, set only on a send; null on a preview.
    sent_files: list[SentFileFingerprint] | None = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def total_size(self):
        if sum(row.byte_length for row in self.files) > 50_000_000:
            raise ValueError("dispute_submit_invalid")
        return self

    @model_validator(mode="after")
    def sent_files_binding(self):
        if self.external_send != "SUBMITTED":
            if self.sent_files is not None:
                raise ValueError("dispute_submit_invalid")
            return self
        if self.sent_files is None or len(self.sent_files) != len(self.files):
            raise ValueError("dispute_submit_invalid")
        for sent, part in zip(self.sent_files, self.files):
            if (sent.filename, sent.content_type, sent.byte_length) != (part.filename, part.content_type, part.byte_length):
                raise ValueError("dispute_submit_invalid")
        return self

    @model_validator(mode="after")
    def submit_binding(self):
        submitted = self.external_send == "SUBMITTED"
        if submitted != (self.provider_submission == "PERFORMED"):
            raise ValueError("dispute_submit_invalid")
        if submitted != (self.readback == "PROVIDE_EVIDENCE_SUBMITTED"):
            raise ValueError("dispute_submit_invalid")
        if submitted and (self.source != "paypal_sandbox" or not self.submit_flag_enabled):
            raise ValueError("dispute_submit_invalid")
        if self.path != f"/v1/customer/disputes/{self.dispute_id}/provide-evidence":
            raise ValueError("dispute_submit_invalid")
        return self


class AddTrackingRequest(Contract):
    dispute_id: StrictStr = Field(pattern=DISPUTE_ID_PATTERN)
    case_ref: StrictStr = Field(pattern=r"^case-ref-[0-9]{3}$")
    submit: StrictBool = False
    confirm_token: StrictStr | None = Field(default=None, pattern=CONFIRM_TOKEN_PATTERN)


class TrackerItem(Contract):
    # The preview masks the transaction id and the tracking number ("*"); the server-side send carries the originals.
    transaction_id: StrictStr = Field(pattern=r"^[A-Za-z0-9*._-]{1,64}$")
    tracking_number: StrictStr = Field(min_length=1, max_length=64)
    status: Literal["SHIPPED"]
    carrier: Literal["USPS", "UPS", "FEDEX", "DHL", "TW_CHUNGHWA_POST", "JP_JAPANPOST", "OTHER"]
    carrier_name_other: StrictStr | None = Field(default=None, min_length=1, max_length=64)

    @model_validator(mode="after")
    def other_needs_name(self):
        if (self.carrier == "OTHER") != (self.carrier_name_other is not None):
            raise ValueError("carrier_invalid")
        return self


class TrackerBatch(Contract):
    trackers: list[TrackerItem] = Field(min_length=1, max_length=1)


class AddTrackingResponse(DisputeEnvelope):
    readback: Literal["ADD_TRACKING_PREVIEW", "ADD_TRACKING_SUBMITTED"]
    dispute_id: StrictStr = Field(pattern=DISPUTE_ID_PATTERN)
    case_ref: StrictStr = Field(pattern=r"^case-ref-[0-9]{3}$")
    method: Literal["POST"]
    path: Literal["/v1/shipping/trackers-batch"]
    content_type: Literal["application/json"]
    body: TrackerBatch
    external_send: Literal["FROZEN", "SUBMITTED"]
    submit_flag_enabled: StrictBool
    human_review_required: Literal[True]
    # (optimise r24) Keyed SHA-256 of the exact trackers-batch JSON body a send carries.
    payload_sha256: StrictStr | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    send_guard: SendGuard
    # (r30 J2 P2-1) Issued by a preview whose payload can be sent; null on a send and while nothing can be sent.
    confirm_token: StrictStr | None = Field(default=None, pattern=CONFIRM_TOKEN_PATTERN)

    @model_validator(mode="after")
    def submit_binding(self):
        submitted = self.external_send == "SUBMITTED"
        if submitted != (self.provider_submission == "PERFORMED"):
            raise ValueError("tracking_submit_invalid")
        if submitted != (self.readback == "ADD_TRACKING_SUBMITTED"):
            raise ValueError("tracking_submit_invalid")
        if submitted and (self.source != "paypal_sandbox" or not self.submit_flag_enabled):
            raise ValueError("tracking_submit_invalid")
        return self


ReferenceTheme = Literal["source_compliance", "velocity_guard", "dispute_mediation"]
ReferenceRegion = Literal["US"]
ReferenceStage = Literal["any", "procedural_order", "not_applicable"]
ReferenceMaterial = Literal["official_api_reference", "official_policy", "public_court_order_copy"]
ReferenceText = Annotated[StrictStr, Field(min_length=1, max_length=8000)]
ReferenceDigest = Annotated[StrictStr, Field(pattern=r"^[a-f0-9]{64}$")]
ReferenceDate = Annotated[StrictStr, Field(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")]
ReferenceTime = Annotated[StrictStr, Field(min_length=20, max_length=64)]


def reference_instant(value):
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})", value):
        raise ValueError("reference_time_invalid")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("reference_time_invalid")
        # Year 9999 minus an offset (or year 1 plus one) leaves datetime's range: OverflowError, not ValueError,
        # which surfaced as a 500 (red team R1-DATE).
        return parsed.astimezone(timezone.utc)
    except OverflowError:
        raise ValueError("reference_time_invalid") from None


def reference_url(value):
    if any(c.isspace() or unicodedata.category(c).startswith("C") for c in value) or "\\" in value:
        raise ValueError("reference_url_invalid")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.username is not None or parsed.password is not None or parsed.port not in (None, 443) or parsed.fragment:
        raise ValueError("reference_url_invalid")
    host, path = parsed.hostname, parsed.path
    if re.search(r"%2e|%2f|%5c", path, re.I) or any(part in (".", "..") for part in path.split("/")):
        raise ValueError("reference_url_invalid")
    allowed = ((host == "developer.paypal.com" and path.startswith(("/api/", "/sandbox-testing/", "/disputes/", "/platforms/disputes/"))) or
               (host == "www.paypal.com" and path.startswith("/us/legalhub/paypal/")) or
               (host == "www.govinfo.gov" and path.startswith("/content/pkg/USCOURTS-cand-") and path.endswith(".pdf")))
    if not allowed:
        raise ValueError("reference_url_invalid")
    if host == "www.paypal.com":
        if parsed.query != "country.x=US&locale.x=en_US":
            raise ValueError("reference_url_invalid")
    elif parsed.query:
        raise ValueError("reference_url_invalid")
    return value


class ScenarioCitation(Contract):
    chunk_id: StrictStr = Field(pattern=r"^[A-Z0-9-]{1,128}$")
    source_id: StrictStr = Field(pattern=r"^[A-Z0-9-]{1,128}$")
    title: StrictStr = Field(min_length=1, max_length=512)
    url: StrictStr = Field(min_length=1, max_length=2048)
    locator: StrictStr = Field(min_length=1, max_length=1000)
    material_type: Literal["official_api_reference", "official_policy"]
    jurisdiction: Literal["US"]
    text_sha256: StrictStr = Field(pattern=r"^[a-f0-9]{64}$")

    @field_validator("title", "locator")
    @classmethod
    def bounded_text(cls, value):
        if any(unicodedata.category(char).startswith("C") for char in value):
            raise ValueError("scenario_match_invalid")
        return value

    @field_validator("url")
    @classmethod
    def official_url(cls, value):
        return reference_url(value)

    @model_validator(mode="after")
    def pinned_identity(self):
        try:
            corpus = load_corpus()
            chunks = {row["chunk_id"]: row for row in corpus._chunks}
            sources = corpus._sources
            chunk = chunks[self.chunk_id]
            source = sources[chunk["source_id"]]
        except Exception:
            raise ValueError("scenario_match_invalid") from None
        expected = {
            "chunk_id": self.chunk_id,
            "source_id": chunk["source_id"],
            "title": source["title"],
            "url": chunk["source_url"],
            "locator": chunk["source_locator"],
            "material_type": chunk["material_type"],
            "jurisdiction": "US",
            "text_sha256": chunk["text_sha256"],
        }
        if self.model_dump() != expected:
            raise ValueError("scenario_match_invalid")
        return self


class DisputeScenario(Contract):
    scenario_id: Literal["US-DEMO-DISPUTE-EVIDENCE"]
    title: Literal["INR or counterfeit evidence organization"]
    theme: Literal["dispute_mediation"]
    jurisdiction: Literal["US"]
    evidence_class: Literal["SYNTHETIC_DEMO_SCENARIO"]
    expected_route: Literal["PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW"]
    final_authority: Literal["PAYPAL_OR_EXTERNAL_ISSUER"]
    limitations: list[StrictStr] = Field(min_length=1, max_length=8)
    citations: list[ScenarioCitation] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def bounded_unique_values(self):
        expected_limitations = [
            "No automatic submission",
            "No outcome prediction",
            "Photos only when relevant or requested",
        ]
        if self.limitations != expected_limitations:
            raise ValueError("scenario_match_invalid")
        if len(self.limitations) != len(set(self.limitations)):
            raise ValueError("scenario_match_invalid")
        if any(len(value) > 256 or any(unicodedata.category(char).startswith("C") for char in value)
               for value in [self.title, *self.limitations]):
            raise ValueError("scenario_match_invalid")
        ids = [row.chunk_id for row in self.citations]
        if len(ids) != len(set(ids)):
            raise ValueError("scenario_match_invalid")
        return self


class ScenarioMatch(Contract):
    schema_version: Literal[1]
    source: Literal["local_synthetic_scenario_matcher"]
    status: Literal["synthetic_scenarios_found"]
    intake_status: Literal["ready_for_local_rules", "manual_review"]
    provenance: Literal["AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES"]
    evaluation_scope: Literal["AUTHORED_SYNTHETIC_DEMO_ONLY"]
    required_human_review: Literal[True]
    operational_authority: Literal["REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"]
    engine_execution: Literal["NOT_RUN"]
    current_policy_applicability: Literal["NOT_ESTABLISHED"]
    real_case_evidence: Literal["NOT_PROVIDED"]
    scenario: DisputeScenario


class DisputeRequirement(Contract):
    request_id: StrictStr = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
    provider_evidence_type: StrictStr = Field(min_length=1, max_length=128, pattern=r"^[A-Z][A-Z0-9_]{0,127}$")
    evidence_type: StrictStr | None = Field(default=None, min_length=1, max_length=128, pattern=r"^[A-Z][A-Z0-9_]{0,127}$")
    source: StrictStr = Field(min_length=1, max_length=128, pattern=r"^[A-Z][A-Z0-9_]{0,127}$")
    mandatory: StrictBool
    action: StrictStr | None = Field(default=None, min_length=1, max_length=128, pattern=r"^[A-Z][A-Z0-9_]{0,127}$")
    requirement_state: Literal[
        "CONTEXT_ONLY", "UNMAPPED_EVIDENCE_TYPE", "PROVIDER_REQUEST_OUTSIDE_LOCAL_MATRIX",
        "STRUCTURALLY_PRESENT", "MANDATORY_EVIDENCE_MISSING", "OPTIONAL_EVIDENCE_MISSING",
    ]
    proof_count: StrictInt = Field(ge=0, le=128)
    accepted_attachment_count: StrictInt = Field(ge=0, le=20)


class DisputeRouting(Contract):
    schema_version: Literal[1]
    snapshot_class: Literal["SYNTHETIC_PROVIDER_FIXTURE"]
    reason: Literal[
        "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
        "UNAUTHORISED", "CREDIT_NOT_PROCESSED", "DUPLICATE_TRANSACTION",
        "INCORRECT_AMOUNT", "PAYMENT_BY_OTHER_MEANS", "CANCELED_RECURRING_BILLING", "OTHER",
    ]
    status: Literal[
        "OPEN", "WAITING_FOR_SELLER_RESPONSE", "WAITING_FOR_BUYER_RESPONSE",
        "UNDER_REVIEW", "RESOLVED", "CLOSED", "UNKNOWN",
    ]
    dispute_life_cycle_stage: Literal[
        "INQUIRY", "CHARGEBACK", "PRE_ARBITRATION", "ARBITRATION", "UNKNOWN",
    ]
    seller_response_due_date: StrictStr = Field(min_length=20, max_length=64)
    due_state: Literal["OPEN", "EXPIRED"]
    available_actions: list[StrictStr] = Field(max_length=20)
    requirements: list[DisputeRequirement] = Field(min_length=1, max_length=20)
    overall_state: Literal[
        "CASE_NOT_ACTIONABLE", "MANUAL_REVIEW", "DUE_DATE_EXPIRED",
        "ACTION_NOT_AVAILABLE", "NEEDS_INPUT", "READY_FOR_LOCAL_REVIEW",
    ]
    human_review_required: Literal[True]
    provider_submission: Literal["NOT_PERFORMED"]

    @model_validator(mode="after")
    def bounded_actions_and_requests(self):
        if (len(self.available_actions) != len(set(self.available_actions)) or
                any(re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", action) is None
                    for action in self.available_actions)):
            raise ValueError("dispute_routing_invalid")
        request_ids = [row.request_id for row in self.requirements]
        if len(request_ids) != len(set(request_ids)):
            raise ValueError("dispute_routing_invalid")
        return self


class RestrictedOriginalSummary(Contract):
    schema_version: Literal[1]
    profile: Literal["RESTRICTED_ORIGINAL_METADATA_V1"]
    data_class: Literal["SYNTHETIC_RESTRICTED_EVIDENCE"]
    custody: Literal["SESSION_MEMORY_ONLY"]
    persistent_storage: Literal["NOT_IMPLEMENTED"]
    production_pii_vault: Literal["NOT_IMPLEMENTED"]
    proof_record_count: StrictInt = Field(ge=0, le=128)
    attachment_count: StrictInt = Field(ge=0, le=20)
    content_returned: Literal[False]
    provider_submission: Literal["NOT_PERFORMED"]


class TimeEvent(Contract):
    kind: Literal["PAYMENT", "ORDER_RECORD_CREATED", "DELIVERY", "CLAIM_OPENED"]
    at: StrictStr = Field(min_length=20, max_length=40)
    source: Literal["PROVIDER", "SELLER_PROVIDED_UNVERIFIED"]


class MessageTimeEvent(Contract):
    kind: Literal["MESSAGE"]
    at: StrictStr = Field(min_length=20, max_length=40)
    source: Literal["SELLER_PROVIDED_UNVERIFIED"]
    channel: Literal["EMAIL", "PRIVATE_MESSAGE"]
    direction: Literal["INBOUND", "OUTBOUND"]
    topic: Literal["PAYMENT_NOTICE", "ORDER_DETAILS_REQUEST", "ORDER_DETAILS_PROVIDED",
                   "DELIVERY_NOTICE", "REFUND_REQUEST", "OTHER"]
    message_digest: StrictStr = Field(pattern=r"^[0-9a-f]{64}$")


class TimeGaps(Contract):
    payment_to_order_record: Optional[StrictInt]
    payment_to_delivery: Optional[StrictInt]
    delivery_to_claim: Optional[StrictInt]
    payment_to_claim: Optional[StrictInt]


class TimeEvidence(Contract):
    schema_version: Literal["payguard.time_evidence.v1"]
    events: list[Union[MessageTimeEvent, TimeEvent]] = Field(min_length=2, max_length=30)
    gaps_seconds: TimeGaps
    flags: list[Literal["ORDER_RECORD_ABSENT", "DELIVERY_NOT_RECORDED", "DELIVERY_AFTER_CLAIM",
                        "CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME"]] = Field(max_length=4)
    judgement: Literal["NOT_MADE"]
    advisory_only: Literal[True]


class DisputeDraftResponse(Contract):
    case_ref: str
    status: Literal["manual_review", "review_evidence"]
    evidence: Evidence
    review_reasons: list[str]
    recommendation: str
    limitations: list[str]
    policy_version: str
    advisory_only: Literal[True]
    source: Literal["synthetic"]
    routing: DisputeRouting
    restricted_original_summary: RestrictedOriginalSummary
    scenario_match: ScenarioMatch
    draft_digest: str
    identity_redaction: IdentityRedaction
    document_redaction: DocumentRedaction
    time_evidence: Optional[TimeEvidence] = None


class ReferenceRequest(Contract):
    query: StrictStr = Field(min_length=1, max_length=512)
    theme: ReferenceTheme
    jurisdiction: ReferenceRegion
    case_stage: ReferenceStage = "any"
    material_types: list[ReferenceMaterial] | None = Field(default=None, min_length=1, max_length=3)
    limit: StrictInt = Field(default=3, ge=1, le=10)
    require_known_source_date: StrictBool = False
    max_source_age_days: StrictInt | None = Field(default=None, ge=0, le=365000)
    as_of: StrictStr | None = Field(default=None, min_length=20, max_length=64)


class ReferenceDigests(Contract):
    sources_sha256: ReferenceDigest
    chunks_sha256: ReferenceDigest

    @model_validator(mode="after")
    def pinned(self):
        if self.sources_sha256 != SOURCE_SHA256 or self.chunks_sha256 != CHUNKS_SHA256:
            raise ValueError("reference_digest_invalid")
        return self


class ReferenceFilters(Contract):
    theme: ReferenceTheme
    jurisdiction: ReferenceRegion
    case_stage: ReferenceStage
    material_types: list[ReferenceMaterial] = Field(min_length=1, max_length=3)
    limit: StrictInt = Field(ge=1, le=10)
    require_known_source_date: StrictBool
    max_source_age_days: StrictInt | None = Field(ge=0, le=365000)
    age_basis: Literal["source_updated_date_utc_calendar"]
    as_of: ReferenceTime | None

    @model_validator(mode="after")
    def coherent(self):
        if self.material_types != sorted(set(self.material_types)):
            raise ValueError("reference_filters_invalid")
        if self.max_source_age_days is not None and self.as_of is None:
            raise ValueError("reference_filters_invalid")
        if self.as_of is not None:
            reference_instant(self.as_of)
        return self


class ReferenceCitation(Contract):
    chunk_id: StrictStr = Field(pattern=r"^[A-Z0-9-]{1,128}$")
    source_id: StrictStr = Field(min_length=1, max_length=128)
    title: ReferenceText
    source_title: ReferenceText
    text: ReferenceText
    url: StrictStr = Field(min_length=1, max_length=2000)
    locator: ReferenceText
    material_type: ReferenceMaterial
    jurisdiction: ReferenceRegion
    jurisdiction_label: StrictStr = Field(min_length=1, max_length=2000)
    case_stage: Literal["procedural_order", "not_applicable"]
    case_outcome: Literal["SETTLEMENT_APPROVAL_NOT_FINAL_MERITS", "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED"] | None
    retrieved_at: ReferenceTime
    text_sha256: ReferenceDigest
    relevance_score: StrictInt = Field(ge=1, le=128)
    source_updated_date: ReferenceDate | None
    source_updated_date_status: Literal["DOCUMENT_STATED", "MISSING"]
    effective_date: ReferenceDate | None
    effective_date_status: Literal["DOCUMENT_STATED", "NOT_VERIFIED"]
    decision_date: ReferenceDate | None
    decision_date_status: Literal["DOCUMENT_STATED", "NOT_STATED_IN_REVIEWED_DOCUMENT", "NOT_APPLICABLE"]
    decision_acceptance_deadline: ReferenceDate | None

    @field_validator("url")
    @classmethod
    def safe_url(cls, value):
        return reference_url(value)

    @field_validator("title", "source_title", "text", "locator", "source_id", "jurisdiction_label")
    @classmethod
    def safe_text(cls, value):
        if any(unicodedata.category(c).startswith("C") for c in value):
            raise ValueError("reference_text_invalid")
        return value

    @model_validator(mode="after")
    def coherent(self):
        reference_instant(self.retrieved_at)
        for key in ("source_updated_date", "effective_date", "decision_date", "decision_acceptance_deadline"):
            value = getattr(self, key)
            if value is not None:
                date.fromisoformat(value)
            if key != "decision_acceptance_deadline" and (value is not None) != (getattr(self, key + "_status") == "DOCUMENT_STATED"):
                raise ValueError("reference_date_invalid")
        if hashlib.sha256(self.text.encode("utf-8")).hexdigest() != self.text_sha256:
            raise ValueError("reference_text_digest_invalid")
        if self.material_type == "public_court_order_copy":
            if self.case_stage != "procedural_order" or self.case_outcome not in {"SETTLEMENT_APPROVAL_NOT_FINAL_MERITS", "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED"} or self.jurisdiction != "US":
                raise ValueError("reference_case_invalid")
        elif self.case_stage != "not_applicable" or self.case_outcome is not None:
            raise ValueError("reference_case_invalid")
        return self


class ReferenceResponse(Contract):
    schema_version: StrictInt = Field(ge=1, le=1)
    status: Literal["references_found", "evidence_missing"]
    corpus_id: Literal["payguard-us-official-references-v2"]
    corpus_digest: ReferenceDigest
    corpus_digests: ReferenceDigests
    filters_applied: ReferenceFilters
    results: list[ReferenceCitation] = Field(max_length=10)
    limitations: list[Annotated[StrictStr, Field(min_length=1, max_length=2000)]] = Field(min_length=1, max_length=32)
    advisory_only: StrictBool
    operational_authority: Literal["REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"]
    source: Literal["public_reference"]

    @model_validator(mode="after")
    def coherent(self, info: ValidationInfo):
        combined = hashlib.sha256((SOURCE_SHA256 + "\n" + CHUNKS_SHA256).encode("ascii")).hexdigest()
        if self.corpus_digest != combined or self.advisory_only is not True:
            raise ValueError("reference_authority_invalid")
        filters = self.filters_applied
        if (self.status == "references_found") != bool(self.results) or len(self.results) > filters.limit:
            raise ValueError("reference_results_invalid")
        ids = [row.chunk_id for row in self.results]
        if len(ids) != len(set(ids)):
            raise ValueError("reference_results_invalid")
        if self.results != sorted(self.results, key=lambda row: (-row.relevance_score, row.chunk_id)):
            raise ValueError("reference_results_invalid")
        for row in self.results:
            if row.jurisdiction != filters.jurisdiction or row.material_type not in filters.material_types or (filters.case_stage != "any" and row.case_stage != filters.case_stage):
                raise ValueError("reference_filters_invalid")
            if (filters.require_known_source_date or filters.max_source_age_days is not None) and row.source_updated_date is None:
                raise ValueError("reference_date_invalid")
            if filters.as_of is not None:
                instant = reference_instant(filters.as_of)
                updated = None if row.source_updated_date is None else date.fromisoformat(row.source_updated_date)
                if reference_instant(row.retrieved_at) > instant or (updated is not None and updated > instant.date()):
                    raise ValueError("reference_date_invalid")
                if filters.max_source_age_days is not None and (instant.date() - updated).days > filters.max_source_age_days:
                    raise ValueError("reference_date_invalid")
        request = (info.context or {}).get("request")
        if request is not None:
            expected = request.model_dump(exclude={"query", "as_of"})
            expected["material_types"] = sorted(MATERIAL_TYPES if request.material_types is None else request.material_types)
            expected["as_of"] = None if request.as_of is None else reference_instant(request.as_of).isoformat()
            expected["age_basis"] = "source_updated_date_utc_calendar"
            if filters.model_dump() != expected:
                raise ValueError("reference_filters_invalid")
        return self


PolicyReason = Literal["SUMMARY_COVERAGE_INCOMPLETE", "CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED", "FUTURE_OBSERVATION", "STALE_OBSERVATION", "DOCUMENT_UPDATE_DATE_MISSING", "DOCUMENT_UPDATE_IN_FUTURE", "UNKNOWN_EFFECTIVE_DATE", "EFFECTIVE_DATE_IN_FUTURE", "API_REFERENCE_NOT_POLICY", "PROCEDURE_NOT_APPLICABLE_POLICY", "NO_OFFICIAL_POLICY_COVERAGE", "NO_REFERENCE_COVERAGE"]
ClaimReason = Literal["ACTION_CLAIM_FORBIDDEN", "ASSURANCE_CLAIM_FORBIDDEN", "CITATION_UNKNOWN", "CITATION_REGION_MISMATCH", "CITATION_THEME_MISMATCH", "CLAIM_REFERENCE_TYPE_MISMATCH", "FUTURE_OBSERVATION", "STALE_OBSERVATION", "DOCUMENT_UPDATE_IN_FUTURE", "CURRENT_POLICY_NOT_ESTABLISHED"]
ClaimType = Literal["policy_reference", "current_policy", "procedural_reference", "api_reference", "financial_action", "assurance"]
ClaimGateStatus = Literal["STRUCTURE_COMPATIBLE", "INCOMPLETE_EVIDENCE", "REJECTED"]
PolicyIdentity = Annotated[StrictStr, Field(pattern=r"^[A-Z0-9-]{1,128}$")]
PolicyCount = Annotated[StrictInt, Field(ge=0, le=29)]
PolicyLabel = Annotated[StrictStr, Field(min_length=1, max_length=2000)]


class PolicyRequest(Contract):
    jurisdiction: ReferenceRegion
    theme: ReferenceTheme
    as_of: ReferenceTime
    observation_max_age_days: StrictInt = Field(ge=0, le=365000)

    @field_validator("as_of")
    @classmethod
    def aware_as_of(cls, value):
        reference_instant(value)
        return value


class AdvisoryRequest(PolicyRequest):
    candidate_json: StrictStr = Field(min_length=1, max_length=8192)


class PolicyContext(PolicyRequest):
    pass


class PolicyThemeCounts(Contract):
    source_compliance: PolicyCount
    velocity_guard: PolicyCount
    dispute_mediation: PolicyCount


class PolicyCoverage(Contract):
    complete: StrictBool
    basis: Literal["pinned_authored_summaries_only"]
    regional_source_count: StrictInt = Field(ge=0, le=16)
    selected_source_count: StrictInt = Field(ge=0, le=16)
    selected_chunk_count: PolicyCount
    official_policy_source_ids: list[PolicyIdentity] = Field(max_length=16)
    official_policy_chunk_count_by_theme: PolicyThemeCounts
    missing_official_policy_themes: list[ReferenceTheme] = Field(max_length=3)

    @model_validator(mode="after")
    def coherent(self):
        if self.complete is not False or self.selected_source_count > self.regional_source_count:
            raise ValueError("policy_coverage_invalid")
        if self.official_policy_source_ids != sorted(set(self.official_policy_source_ids)):
            raise ValueError("policy_coverage_invalid")
        expected_missing = sorted(key for key, count in self.official_policy_chunk_count_by_theme.model_dump().items() if count == 0)
        if self.missing_official_policy_themes != expected_missing:
            raise ValueError("policy_coverage_invalid")
        return self


class PolicySource(Contract):
    source_id: PolicyIdentity
    title: PolicyLabel
    url: StrictStr = Field(min_length=1, max_length=2000)
    material_type: ReferenceMaterial
    jurisdiction: PolicyLabel
    retrieved_at: ReferenceTime
    source_updated_date: ReferenceDate | None
    source_updated_date_status: Literal["DOCUMENT_STATED", "MISSING"]
    effective_date: ReferenceDate | None
    effective_date_status: Literal["DOCUMENT_STATED", "NOT_VERIFIED"]
    decision_date: ReferenceDate | None
    decision_date_status: Literal["DOCUMENT_STATED", "NOT_STATED_IN_REVIEWED_DOCUMENT", "NOT_APPLICABLE"]
    decision_acceptance_deadline: ReferenceDate | None
    content_class: Literal["public_reference_summary"]
    representation: Literal["authored_paraphrase_not_full_source"]
    jurisdiction_normalized: ReferenceRegion
    observation_status: Literal["FUTURE_OBSERVATION", "STALE_OBSERVATION", "WITHIN_OBSERVATION_BUDGET"]
    observation_age_basis: Literal["saved_retrieved_at_exact_elapsed_time"]
    current_policy_applicability: Literal["NOT_ESTABLISHED"]
    reason_codes: list[PolicyReason] = Field(min_length=1, max_length=15)
    citation_chunk_ids: list[PolicyIdentity] = Field(min_length=1, max_length=29)

    @field_validator("url")
    @classmethod
    def safe_url(cls, value):
        return reference_url(value)

    @field_validator("title", "jurisdiction")
    @classmethod
    def safe_label(cls, value):
        if any(unicodedata.category(c).startswith("C") for c in value):
            raise ValueError("policy_label_invalid")
        return value

    @model_validator(mode="after")
    def coherent(self):
        reference_instant(self.retrieved_at)
        for key in ("source_updated_date", "effective_date", "decision_date", "decision_acceptance_deadline"):
            value = getattr(self, key)
            if value is not None:
                date.fromisoformat(value)
            if key != "decision_acceptance_deadline" and (value is not None) != (getattr(self, key + "_status") == "DOCUMENT_STATED"):
                raise ValueError("policy_date_invalid")
        if self.reason_codes != sorted(set(self.reason_codes)) or self.citation_chunk_ids != sorted(set(self.citation_chunk_ids)):
            raise ValueError("policy_source_invalid")
        return self


class PolicyChunk(Contract):
    chunk_id: PolicyIdentity
    source_id: PolicyIdentity
    theme: ReferenceTheme
    case_stage: Literal["procedural_order", "not_applicable"]
    material_type: ReferenceMaterial
    case_outcome: Literal["SETTLEMENT_APPROVAL_NOT_FINAL_MERITS", "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED"] | None
    text_sha256: ReferenceDigest
    jurisdiction: ReferenceRegion


class TrustedPolicyResponse(Contract):
    @model_validator(mode="after")
    def trusted_readback(self, info: ValidationInfo):
        trusted = (info.context or {}).get("trusted")
        if trusted is not None and (type(trusted) is not dict or self.model_dump() != trusted):
            raise ValueError("policy_trusted_readback_invalid")
        return self


class PolicyAssessmentResponse(TrustedPolicyResponse):
    schema_version: StrictInt = Field(ge=1, le=1)
    version: Literal["payguard.applicability.v1"]
    source: Literal["public_reference"]
    corpus_id: Literal["payguard-us-official-references-v2"]
    corpus_digest: ReferenceDigest
    corpus_digests: ReferenceDigests
    filters_applied: PolicyContext
    status: Literal["INCOMPLETE_POLICY_EVIDENCE"]
    current_policy_applicability: Literal["NOT_ESTABLISHED"]
    advisory_only: StrictBool
    operational_authority: Literal["REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"]
    requires_human_review: StrictBool
    coverage: PolicyCoverage
    sources: list[PolicySource] = Field(max_length=16)
    chunks: list[PolicyChunk] = Field(max_length=29)
    reason_codes: list[PolicyReason] = Field(min_length=1, max_length=15)
    limitations: list[PolicyLabel] = Field(min_length=1, max_length=32)

    @model_validator(mode="after")
    def coherent(self):
        combined = hashlib.sha256((SOURCE_SHA256 + "\n" + CHUNKS_SHA256).encode("ascii")).hexdigest()
        if self.advisory_only is not True or self.requires_human_review is not True or self.corpus_digest != combined:
            raise ValueError("policy_authority_invalid")
        source_ids = [s.source_id for s in self.sources]
        chunk_ids = [c.chunk_id for c in self.chunks]
        if source_ids != sorted(set(source_ids)) or chunk_ids != sorted(set(chunk_ids)):
            raise ValueError("policy_identity_invalid")
        if len(self.sources) != self.coverage.selected_source_count or len(self.chunks) != self.coverage.selected_chunk_count:
            raise ValueError("policy_count_invalid")
        sources = {s.source_id: s for s in self.sources}
        for chunk in self.chunks:
            if chunk.source_id not in sources or chunk.theme != self.filters_applied.theme or chunk.jurisdiction != self.filters_applied.jurisdiction or chunk.material_type != sources[chunk.source_id].material_type:
                raise ValueError("policy_chunk_invalid")
        for source in self.sources:
            joined = [c.chunk_id for c in self.chunks if c.source_id == source.source_id]
            if source.jurisdiction_normalized != self.filters_applied.jurisdiction or source.citation_chunk_ids != joined:
                raise ValueError("policy_source_invalid")
        official = sorted(s.source_id for s in self.sources if s.material_type == "official_policy")
        if self.coverage.official_policy_source_ids != official or self.reason_codes != sorted(set(self.reason_codes)):
            raise ValueError("policy_coverage_invalid")
        return self


class AdvisoryClaimGate(Contract):
    claim_index: StrictInt = Field(ge=0, le=19)
    claim_type: ClaimType
    status: ClaimGateStatus
    trusted_citation_chunk_ids: list[PolicyIdentity] = Field(max_length=10)
    reason_codes: list[ClaimReason] = Field(max_length=10)

    @model_validator(mode="after")
    def coherent(self):
        if self.trusted_citation_chunk_ids != sorted(set(self.trusted_citation_chunk_ids)) or self.reason_codes != sorted(set(self.reason_codes)):
            raise ValueError("advisory_gate_invalid")
        return self


class AdvisoryEvaluationResponse(TrustedPolicyResponse):
    schema_version: StrictInt = Field(ge=1, le=1)
    version: Literal["payguard.advisory_eval.v1"]
    source: Literal["offline_structured_gate"]
    status: ClaimGateStatus
    requested_context: PolicyContext
    corpus_id: Literal["payguard-us-official-references-v2"]
    corpus_digest: ReferenceDigest
    corpus_digests: ReferenceDigests
    advisory_only: StrictBool
    operational_authority: Literal["REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"]
    requires_human_review: StrictBool
    semantic_entailment: Literal["NOT_EVALUATED"]
    PII_quality: Literal["NOT_EVALUATED"]
    prompt_injection_quality: Literal["NOT_EVALUATED"]
    natural_language_action_assurance_quality: Literal["NOT_EVALUATED"]
    model_generation: Literal["NOT_RUN"]
    claim_count: StrictInt = Field(ge=1, le=20)
    claim_gates: list[AdvisoryClaimGate] = Field(min_length=1, max_length=20)
    current_policy_applicability: Literal["NOT_ESTABLISHED"]
    coverage: PolicyCoverage
    limitations: list[PolicyLabel] = Field(min_length=1, max_length=32)

    @model_validator(mode="after")
    def coherent(self):
        combined = hashlib.sha256((SOURCE_SHA256 + "\n" + CHUNKS_SHA256).encode("ascii")).hexdigest()
        if self.advisory_only is not True or self.requires_human_review is not True or self.corpus_digest != combined or len(self.claim_gates) != self.claim_count:
            raise ValueError("advisory_authority_invalid")
        if [g.claim_index for g in self.claim_gates] != list(range(self.claim_count)):
            raise ValueError("advisory_index_invalid")
        statuses = {g.status for g in self.claim_gates}
        expected = "REJECTED" if "REJECTED" in statuses else "INCOMPLETE_EVIDENCE" if "INCOMPLETE_EVIDENCE" in statuses else "STRUCTURE_COMPATIBLE"
        if self.status != expected:
            raise ValueError("advisory_status_invalid")
        return self
