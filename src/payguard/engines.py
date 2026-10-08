"""Deterministic advisory engines for a local synthetic PayGuard prototype.

These functions perform no I/O and do not certify policy compliance, predict
account restrictions, or decide disputes. Their outputs are safe draft inputs
for a separate human review boundary.
"""

from datetime import datetime, timedelta, timezone
from decimal import Context, Decimal, InvalidOperation, localcontext
import re
import unicodedata
from payguard.policy import POLICY_VERSION, VelocityPolicy


_TRANSACTION_FIELDS = frozenset({"order_id", "amount", "currency", "occurred_at"})
_CASE_FIELDS = frozenset({
    "case_id", "order_id", "reason", "opened_at", "order_created_at",
    "carrier_status", "delivered_at", "evidence_source",
})
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
_CURRENCY = re.compile(r"[A-Z]{3}\Z")
_DECIMAL_TEXT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})\Z")
_BASELINE_PROVENANCE = frozenset({"SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED"})
_AUP_CATEGORIES = (
    ("unsupported_financial_promise", r"\bguaranteed\b.{0,80}(?:[0-9]+(?:\.[0-9]+)?%\s*(?:roi|returns?)\b|\b(?:profit|roi)\b)"),
    ("weapons", r"\b(?:firearms?|guns?|ammunition|explosives?)\b"),
    ("controlled_substances", r"\b(?:cocaine|heroin|methamphetamine|illegal\s+drugs?)\b"),
    ("counterfeit_goods", r"\b(?:counterfeit|fake\s+(?:brands?|luxury|designer))\b"),
    ("regulated_activity", r"\b(?:gambling|casino|betting)\b"),
)


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{field} must be a bounded identifier")
    return value


def _decimal(value: object, field: str, *, allow_zero: bool = False) -> Decimal:
    if not isinstance(value, str) or len(value) > 160 or not _DECIMAL_TEXT.fullmatch(value):
        raise ValueError(f"{field} must be a finite decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a finite decimal string") from exc
    if not result.is_finite() or result < 0 or (result == 0 and not allow_zero):
        raise ValueError(f"{field} must be {'nonnegative' if allow_zero else 'positive'} and finite")
    if len(result.as_tuple().digits) > 64 or abs(result.as_tuple().exponent) > 100:
        raise ValueError(f"{field} exceeds supported decimal precision")
    return result


def _time(value: object, field: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise ValueError(f"{field} must be an ISO timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError(f"{field} must include timezone")
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be an ISO timestamp with timezone") from exc


def _utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _number(value: Decimal) -> str:
    return format(value, "f")


def check_aup(description: str) -> dict:
    """Flag bounded text for review without offering policy evasion or certification."""
    if not isinstance(description, str) or not description.strip() or len(description) > 4000:
        raise ValueError("description must contain between 1 and 4000 characters")
    if any(unicodedata.category(char).startswith("C") for char in description):
        raise ValueError("description must not contain control or invisible characters")
    normalized = unicodedata.normalize("NFKC", description).casefold()
    findings = [
        {"category": category, "code": "keyword_requires_policy_review"}
        for category, pattern in _AUP_CATEGORIES
        if re.search(pattern, normalized)
    ]
    return {
        "match_status": "REVIEW_SIGNAL" if findings else "NO_MATCH",
        "compliance_decision": "NOT_MADE",
        "findings": findings,
        "recommendation": (
            "Review the actual goods or activity against applicable policy. "
            "Do not disguise restricted activity through wording changes."
            if findings else
            "No configured demo keyword matched. Review the actual goods or activity "
            "against applicable policy; this result does not certify compliance."
        ),
        "policy_version": POLICY_VERSION,
        "advisory_only": True,
    }


def assess_velocity(
    transactions: list[dict],
    baseline_amount_per_hour: str,
    as_of: str,
    window_hours: int = 1,
    threshold: str = "3.5",
    *,
    baseline_provenance: str = "CALLER_SUPPLIED_UNVERIFIED",
    baseline_window_start: str | None = None,
    baseline_window_end: str | None = None,
) -> dict:
    """Compare a validated current amount/hour to a declared local baseline.

    Every row is validated, including rows outside the window. The window is
    (as_of - window_hours, as_of], and duplicate IDs are rejected across all
    rows. Decimal bounds are computational limits, not merchant policy limits.
    """
    if not isinstance(transactions, list) or len(transactions) > 10000:
        raise ValueError("transactions must be a list with at most 10000 rows")
    if type(window_hours) is not int or window_hours <= 0:
        raise ValueError("window_hours must be a positive integer")
    VelocityPolicy(threshold=threshold, window_hours=window_hours)
    baseline = _decimal(baseline_amount_per_hour, "baseline_amount_per_hour", allow_zero=True)
    limit = _decimal(threshold, "threshold")
    end = _time(as_of, "as_of")
    try:
        start = end - timedelta(hours=window_hours)
    except (OverflowError, TypeError) as exc:
        raise ValueError("window_hours exceeds supported timestamp range") from exc
    if not isinstance(baseline_provenance, str) or baseline_provenance not in _BASELINE_PROVENANCE:
        raise ValueError("baseline_provenance is outside the supported vocabulary")
    if baseline_window_start is None or baseline_window_end is None:
        raise ValueError("baseline provenance requires a complete comparison window")
    baseline_start = _time(baseline_window_start, "baseline_window_start")
    baseline_end = _time(baseline_window_end, "baseline_window_end")
    if not baseline_start < baseline_end <= start:
        raise ValueError("baseline window must precede and not overlap the observation window")
    normalized_baseline_start = _utc(baseline_start)
    normalized_baseline_end = _utc(baseline_end)
    ids = set()
    currencies = set()
    included = []
    excluded_future = 0
    excluded_past = 0
    for row in transactions:
        if not isinstance(row, dict) or set(row) != _TRANSACTION_FIELDS:
            raise ValueError("transaction fields must exactly match the transaction contract")
        order_id = _identifier(row["order_id"], "order_id")
        if order_id in ids:
            raise ValueError("duplicate order_id")
        ids.add(order_id)
        amount = _decimal(row["amount"], "amount")
        currency = row["currency"]
        if not isinstance(currency, str) or not _CURRENCY.fullmatch(currency):
            raise ValueError("currency must be an uppercase three-letter code")
        currencies.add(currency)
        if len(currencies) > 1:
            raise ValueError("transactions must use one currency")
        occurred = _time(row["occurred_at"], "occurred_at")
        if occurred > end:
            excluded_future += 1
        elif occurred <= start:
            excluded_past += 1
        else:
            included.append(amount)
    with localcontext(Context(prec=512)):
        total = sum(included, Decimal("0"))
        rate = total / Decimal(window_hours)
        ratio = None if baseline == 0 else rate / baseline
        # Compare the exact products, avoiding a rounded quotient at the boundary.
        alert = baseline != 0 and total > baseline * Decimal(window_hours) * limit
        result = {
            "status": "insufficient_baseline" if baseline == 0 else ("review_velocity" if alert else "normal"),
            "window_start": _utc(start),
            "window_end": _utc(end),
            "window_hours": window_hours,
            "window_boundary": "left_open_right_closed",
            "transaction_count": len(included),
            "excluded_future_count": excluded_future,
            "excluded_past_count": excluded_past,
            "currency": next(iter(currencies), None),
            "total_amount": _number(total),
            "current_amount_per_hour": _number(rate),
            "baseline_amount_per_hour": _number(baseline),
            "baseline_provenance": baseline_provenance,
            "baseline_window_start": normalized_baseline_start,
            "baseline_window_end": normalized_baseline_end,
            "ratio": None if ratio is None else _number(ratio),
            "threshold": _number(limit),
            "alert": bool(alert),
            "policy_version": POLICY_VERSION,
            "advisory_only": True,
            "limitations": [
                "The baseline is synthetic or caller-supplied and is not a PayPal risk threshold.",
                "A velocity alert is a review signal and does not predict account restrictions.",
            ],
        }
    return result


def prepare_dispute(case: dict) -> dict:
    """Build objective synthetic evidence for human review; never decide a case."""
    if not isinstance(case, dict) or not set(case).issubset(_CASE_FIELDS):
        raise ValueError("case contains fields outside the evidence allowlist")
    if case.get("evidence_source") != "synthetic":
        raise ValueError("only explicitly synthetic evidence is accepted")
    evidence = {"evidence_source": "synthetic"}
    review_reasons = []
    for field in ("case_id", "order_id"):
        value = case.get(field)
        if value is None or value == "":
            review_reasons.append(f"missing_{field}")
        else:
            evidence[field] = _identifier(value, field)
    reason = case.get("reason")
    if reason is None or reason == "":
        review_reasons.append("missing_reason")
    else:
        evidence["reason"] = _identifier(reason, "reason")
        if reason != "INR":
            review_reasons.append("unsupported_reason")
    timestamps = {}
    for field in ("opened_at", "order_created_at"):
        value = case.get(field)
        if value is None or value == "":
            review_reasons.append(f"missing_{field}")
        else:
            timestamps[field] = _time(value, field)
            evidence[field] = _utc(timestamps[field])
    carrier_status = case.get("carrier_status")
    if carrier_status is None or carrier_status == "":
        review_reasons.append("missing_carrier_status")
    else:
        if carrier_status not in ("delivered", "in_transit", "not_shipped", "unknown"):
            raise ValueError("carrier_status is outside the allowed status vocabulary")
        evidence["carrier_status"] = carrier_status
        if carrier_status != "delivered":
            review_reasons.append("delivery_not_confirmed")
    delivered_value = case.get("delivered_at")
    if delivered_value is None or delivered_value == "":
        if carrier_status == "delivered":
            review_reasons.append("missing_delivered_at")
    else:
        timestamps["delivered_at"] = _time(delivered_value, "delivered_at")
        evidence["delivered_at"] = _utc(timestamps["delivered_at"])
    created = timestamps.get("order_created_at")
    opened = timestamps.get("opened_at")
    delivered = timestamps.get("delivered_at")
    if created is not None and opened is not None and created > opened:
        review_reasons.append("order_created_after_dispute")
    if created is not None and delivered is not None and delivered < created:
        review_reasons.append("delivery_before_order")
    if delivered is not None and opened is not None and delivered >= opened:
        review_reasons.append("delivery_not_before_dispute")
    if delivered is not None and carrier_status not in (None, "", "delivered"):
        review_reasons.append("carrier_timestamp_conflict")
    return {
        "case_id": evidence.get("case_id"),
        "status": "manual_review" if review_reasons else "review_evidence",
        "evidence": evidence,
        "review_reasons": review_reasons,
        "recommendation": "A human reviewer must verify the evidence and applicable case requirements before taking any action.",
        "limitations": [
            "All evidence is synthetic and has not been verified against a carrier or payment provider.",
            "A delivery event does not establish buyer intent or determine a dispute outcome.",
            "This draft does not submit evidence or authorize any financial action.",
        ],
        "policy_version": POLICY_VERSION,
        "advisory_only": True,
    }
