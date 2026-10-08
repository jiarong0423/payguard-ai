"""Bounded local intake preflight; never executes a finance engine or action.

Input and evidence labels are untrusted. Outputs contain only fixed diagnostics
and an optional local checklist route, not the raw payload or verification.
Import performs no I/O; fixed corpus loading occurs only for explicit citations.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import json
import math
import re
import unicodedata

from .case_contract import get_contract


_SPEC = get_contract()
_UNKNOWN = "UNKNOWN"
_MAX_BYTES = _SPEC["limits"]["utf8_bytes"]


class _InputError(ValueError):
    pass


class _Issues:
    def __init__(self):
        self.invalid = set()
        self.clarify = set()
        self.missing = set()
        self.manual = set()
        self.gaps = set()

    def add(self, bucket, field, code):
        getattr(self, bucket).add((field, code))

    def result(self, data=None, route=None):
        buckets = (self.invalid, self.clarify, self.missing, self.manual)
        status = next((s for s, b in zip(_SPEC["statuses_in_precedence_order"], buckets)
                       if b), "ready_for_local_rules")
        theme = data.get("requested_theme") if type(data) is dict else None
        if type(theme) is not str or theme not in _SPEC["common_fields"]["requested_theme"]["values"]:
            theme = None
        intake_id = data.get("intake_id") if type(data) is dict else None
        if not _valid_identifier(intake_id) or intake_id == _UNKNOWN:
            intake_id = None
        gates = dict(_SPEC["review_gates"])
        gates["field_completeness"] = ("INVALID" if self.invalid else
                                       "INCOMPLETE" if self.missing else "COMPLETE")
        diagnostics = sorted(set().union(*buckets, self.gaps))
        return {
            "schema_version": 1,
            "contract_version": _SPEC["version"],
            "source": "local_intake_preflight",
            "intake_id": intake_id,
            "requested_theme": theme,
            "status": status,
            "route": route if status in ("ready_for_local_rules", "manual_review") else None,
            "missing_fields": sorted({f for f, _ in self.missing}),
            "invalid_fields": sorted({f for f, _ in self.invalid}),
            "conflicts": sorted({f for f, _ in self.clarify}),
            "evidence_gaps": sorted({f for f, _ in self.gaps}),
            "diagnostics": [{"field": f, "code": c} for f, c in diagnostics],
            "required_human_review": True,
            "advisory_only": True,
            "operational_authority": _SPEC["review_gates"]["operational_authority"],
            "review_gates": gates,
            "engine_execution": "NOT_RUN",
            "caller_provenance": "UNVERIFIED",
            "corpus_binding": dict(_SPEC["corpus_binding"]),
        }


def _valid_identifier(value):
    return (type(value) is str and len(value) <= 128 and
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", value) is not None)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _InputError("duplicate_key")
        result[key] = value
    return result


def _constant(_value):
    raise _InputError("nonfinite")


def _bounded_tree(value):
    pending = [(value, 1)]
    nodes = 0
    while pending:
        item, depth = pending.pop()
        nodes += 1
        if depth > _SPEC["limits"]["maximum_depth"] or nodes > _SPEC["limits"]["maximum_total_nodes"]:
            raise _InputError("structure_limit")
        if type(item) is str:
            if any(unicodedata.category(c).startswith("C") for c in item):
                raise _InputError("invalid_unicode")
        elif type(item) is dict:
            for key, child in item.items():
                if len(key) > _SPEC["limits"]["maximum_json_key_chars"]:
                    raise _InputError("key_limit")
                pending.extend(((key, depth + 1), (child, depth + 1)))
        elif type(item) is list:
            pending.extend((child, depth + 1) for child in item)
        elif type(item) is float and not math.isfinite(item):
            raise _InputError("nonfinite")


def _known(value):
    return value is not None and value != _UNKNOWN


def _parse_time(value):
    instant = datetime.fromisoformat(value)
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("time_invalid")
    return instant.astimezone(timezone.utc)


def _check_object(value, fields, location, issues):
    if type(value) is not dict:
        issues.add("invalid", location, "object_required")
        return
    if set(value) - set(fields):
        issues.add("invalid", location, "unknown_field")
    for name, spec in fields.items():
        field = name if location == "envelope" else location + "." + name
        if name not in value:
            if spec.get("required"):
                issues.add("missing", field, "required_field_missing")
        else:
            _check_value(value[name], spec, field, issues)


def _check_value(value, spec, field, issues):
    kind = spec["kind"]
    if kind == "theme_selector":
        if type(value) is str and 0 < len(value) <= spec["max_chars"]:
            if value not in spec["values"]:
                issues.add("clarify", field, "theme_selection_required")
        elif (type(value) is list and 0 < len(value) <= spec["maximum_items"] and
              all(type(v) is str and 0 < len(v) <= spec["max_chars"] for v in value)):
            issues.add("clarify", field, "single_theme_required")
        else:
            issues.add("invalid", field, "theme_selector_invalid")
        return
    if value == _UNKNOWN and spec.get("allow_unknown"):
        if spec.get("required"):
            issues.add("missing", field, "required_field_unknown")
        return
    if value is None:
        issues.add("invalid", field, "null_not_allowed")
        return
    valid = True
    if kind == "strict_integer":
        valid = type(value) is int
        if valid:
            valid = (("const" not in spec or value == spec["const"]) and
                     ("minimum" not in spec or value >= spec["minimum"]) and
                     ("maximum" not in spec or value <= spec["maximum"]))
    elif kind == "strict_boolean":
        valid = type(value) is bool
    elif kind == "enum":
        valid = type(value) is str and value in spec["values"]
    elif kind in ("identifier", "chunk_id", "evidence_id_ref", "currency"):
        valid = (type(value) is str and len(value) <= spec["max_chars"] and
                 re.fullmatch(spec["pattern"], value) is not None)
    elif kind in ("text", "field_id"):
        valid = (type(value) is str and len(value) <= spec["max_chars"] and
                 bool(value.strip()))
    elif kind == "aware_timestamp":
        valid = (type(value) is str and len(value) <= spec["max_chars"] and
                 re.fullmatch(spec["pattern"], value) is not None)
        if valid:
            try:
                _parse_time(value)
            except (ValueError, OverflowError):
                valid = False
    elif kind == "decimal_string":
        valid = (type(value) is str and len(value) <= spec["max_chars"] and
                 re.fullmatch(spec["pattern"], value) is not None)
        if valid:
            try:
                number = Decimal(value)
                valid = (number.is_finite() and len(number.as_tuple().digits) <= spec["max_significant_digits"] and
                         abs(number.as_tuple().exponent) <= spec["max_absolute_exponent"] and
                         (number >= 0 if spec["minimum_inclusive"] else number > 0))
            except (ValueError, InvalidOperation):
                valid = False
    elif kind == "route_payload_object":
        valid = type(value) is dict
    elif kind == "reference_object":
        _check_object(value, spec["object_spec"]["fields"], field, issues)
        return
    elif kind == "list":
        if type(value) is not list or len(value) > spec["maximum_items"]:
            valid = False
        else:
            item_spec = spec["item_spec"]
            for item in value:
                if "fields" in item_spec:
                    _check_object(item, item_spec["fields"], field + "[]", issues)
                else:
                    _check_value(item, item_spec, field + "[]", issues)
            if spec.get("unique_items"):
                fingerprints = [json.dumps(v, sort_keys=True, separators=(",", ":")) for v in value]
                if len(fingerprints) != len(set(fingerprints)):
                    issues.add("invalid", field, "duplicate_item")
            unique_key = spec.get("unique_key", item_spec.get("unique_key"))
            if unique_key:
                names = (unique_key,) if type(unique_key) is str else unique_key
                keys = [tuple(item.get(k) for k in names) for item in value
                        if type(item) is dict and all(type(item.get(k)) is str for k in names)]
                if len(keys) != len(set(keys)):
                    issues.add("invalid", field, "duplicate_id")
    else:
        valid = False
    if not valid:
        issues.add("invalid", field, "field_format_invalid")


def _required(payload, names, issues):
    for name in names:
        if name not in payload or not _known(payload[name]):
            issues.add("missing", "payload." + name, "conditional_field_missing")


def _conditions(payload, conditions, issues):
    for condition in conditions:
        trigger = condition["when"]
        name = trigger["field"]
        if name in payload and type(payload[name]) is type(trigger["value"]) and payload[name] == trigger["value"]:
            _required(payload, condition["required"], issues)


def _reference_checks(data, items, issues):
    citations = [v for v in data.get("references", [])
                 if type(v) is dict and all(type(v.get(k)) is str for k in ("source_id", "chunk_id"))]
    citations.extend(v["origin_ref"] for v in items
                     if type(v.get("origin_ref")) is dict and
                     all(type(v["origin_ref"].get(k)) is str for k in ("source_id", "chunk_id")))
    if not citations:
        return
    try:
        from .retrieval import load_corpus
        corpus = load_corpus()
        chunks = {c["chunk_id"]: c for c in corpus._chunks}
        end = _parse_time(data["as_of"]) if _known(data.get("as_of")) else None
        for citation in citations:
            row = chunks.get(citation["chunk_id"])
            if row is None or row["source_id"] != citation["source_id"]:
                issues.add("invalid", "references", "reference_join_invalid")
                continue
            source = corpus._sources[row["source_id"]]
            if _known(data.get("jurisdiction")) and corpus._regions[row["source_id"]] != data["jurisdiction"]:
                issues.add("clarify", "references", "reference_region_mismatch")
            if type(data.get("requested_theme")) is str and data["requested_theme"] in _SPEC["common_fields"]["requested_theme"]["values"] and row["_theme"] != data["requested_theme"]:
                issues.add("clarify", "references", "reference_theme_mismatch")
            if end is not None:
                observed = _parse_time(source["retrieved_at"])
                updated = source["source_updated_date"]
                if observed > end or (updated is not None and updated > end.date().isoformat()):
                    issues.add("clarify", "references", "reference_after_as_of")
                elif (type(data.get("observation_max_age_days")) is int and
                      (end - observed).total_seconds() > data["observation_max_age_days"] * 86400):
                    issues.add("clarify", "references", "reference_observation_stale")
            if source["effective_date"] is None:
                issues.add("gaps", "references", "policy_effective_date_not_verified")
    except Exception:
        issues.add("invalid", "references", "reference_unavailable")


def _evidence_checks(data, route, issues):
    payload = data["payload"]
    items = data["evidence_items"]
    evidence = {item["evidence_id"]: item for item in items if _valid_identifier(item.get("evidence_id"))}
    allowed_fields = set(route["field_ids"])
    for item in items:
        if "field_id" in item and item["field_id"] not in allowed_fields:
            issues.add("invalid", "evidence_items[].field_id", "evidence_field_invalid")
        if item.get("evidence_state") in ("UNKNOWN", "NOT_STATED_IN_REVIEWED_DOCUMENT", "NOT_ESTABLISHED"):
            issues.add("gaps", "evidence_items[].evidence_state", "evidence_not_established")
        if item.get("evidence_state") == "CONFLICTING_SOURCES":
            issues.add("clarify", "evidence_items[].evidence_state", "evidence_conflict")
        field_name = item.get("field_id", "").removeprefix("payload.")
        if field_name in route["evidence_ref_types"] and item.get("evidence_type") is not None and item["evidence_type"] not in route["evidence_ref_types"][field_name]:
            issues.add("invalid", "evidence_items[].evidence_type", "evidence_type_mismatch")
        if _known(item.get("observed_at")) and _known(data.get("as_of")) and _parse_time(item["observed_at"]) > _parse_time(data["as_of"]):
            issues.add("clarify", "evidence_items[].observed_at", "evidence_after_as_of")
    for name, types in route["evidence_ref_types"].items():
        value = payload.get(name)
        if not _known(value):
            continue
        item = evidence.get(value)
        if item is None:
            if any("evidence_id" not in candidate for candidate in items):
                issues.add("missing", "payload." + name, "evidence_binding_incomplete")
            else:
                issues.add("invalid", "payload." + name, "evidence_join_invalid")
        elif "field_id" not in item or "evidence_type" not in item:
            issues.add("missing", "evidence_items", "evidence_binding_missing")
        elif item["field_id"] != "payload." + name or item["evidence_type"] not in types:
            issues.add("invalid", "payload." + name, "evidence_binding_invalid")
        elif item.get("evidence_state") in ("UNKNOWN", "NOT_ESTABLISHED", "NOT_STATED_IN_REVIEWED_DOCUMENT", "NOT_APPLICABLE"):
            issues.add("manual", "payload." + name, "evidence_unresolved")
            issues.add("gaps", "payload." + name, "evidence_unresolved")
    if data.get("request_kind") == "prepare_dispute_draft":
        requests = payload.get("evidences")
        if type(requests) is list:
            for request in requests:
                if type(request) is not dict or request.get("source") != "REQUESTED_FROM_SELLER":
                    continue
                provider_type = request.get("evidence_type")
                mapped_type = route["provider_evidence_type_map"].get(provider_type)
                request_id = request.get("request_id")
                if mapped_type is None:
                    issues.add("manual", "payload.evidences", "provider_evidence_type_unmapped")
                    issues.add("gaps", "payload.evidences", "provider_evidence_type_unmapped")
                    continue
                matching = [
                    item for item in items
                    if item.get("provider_request_id") == request_id
                    and item.get("evidence_type") == mapped_type
                    and item.get("field_id") == "payload.evidences"
                ]
                if not matching and request.get("mandatory") is True:
                    issues.add("missing", "payload.evidences", "seller_requested_evidence_missing")
                    issues.add("gaps", "payload.evidences", "seller_requested_evidence_missing")
                elif matching and all(
                    item.get("evidence_state") in (
                        "UNKNOWN", "NOT_ESTABLISHED", "NOT_STATED_IN_REVIEWED_DOCUMENT", "NOT_APPLICABLE"
                    ) for item in matching
                ):
                    issues.add("manual", "payload.evidences", "seller_requested_evidence_unresolved")
                    issues.add("gaps", "payload.evidences", "seller_requested_evidence_unresolved")


def _coherence(data, route, issues):
    payload = data["payload"]
    end = _parse_time(data["as_of"]) if _known(data.get("as_of")) else None
    for name in ("order_created_at", "opened_at", "delivered_at", "canceled_at",
                 "recurring_charge_at", "baseline_window_start", "baseline_window_end", "hold_started_at"):
        if end is not None and _known(payload.get(name)) and _parse_time(payload[name]) > end:
            issues.add("clarify", "payload." + name, "event_after_as_of")
    def compare(first, second, *, strict=False):
        if _known(payload.get(first)) and _known(payload.get(second)):
            a, b = _parse_time(payload[first]), _parse_time(payload[second])
            if a > b or (strict and a == b):
                issues.add("clarify", "payload." + first, "chronology_conflict")
    compare("baseline_window_start", "baseline_window_end", strict=True)
    compare("order_created_at", "opened_at")
    compare("order_created_at", "delivered_at")
    compare("hold_started_at", "hold_expected_end_at")
    if _known(payload.get("delivered_at")) and payload.get("carrier_status") in ("not_shipped", "in_transit"):
        issues.add("clarify", "payload.carrier_status", "carrier_timestamp_conflict")
    if _known(payload.get("delivered_at")) and _known(payload.get("opened_at")) and _parse_time(payload["delivered_at"]) >= _parse_time(payload["opened_at"]):
        issues.add("manual", "payload.delivered_at", "delivery_not_before_dispute")
    if data["request_kind"] == "assess_velocity":
        transactions = payload.get("transactions", [])
        currencies = {r["currency"] for r in transactions if _known(r.get("currency"))}
        if len(currencies) > 1:
            issues.add("clarify", "payload.transactions[].currency", "mixed_currency")
        window_hours = payload.get("window_hours")
        if end is not None and type(window_hours) is int:
            observation_start = end - timedelta(hours=window_hours)
            transaction_times = []
            for row in transactions:
                if _known(row.get("occurred_at")):
                    occurred_at = _parse_time(row["occurred_at"])
                    transaction_times.append(occurred_at)
                    if occurred_at > end:
                        issues.add("clarify", "payload.transactions[].occurred_at",
                                   "transaction_after_as_of")
            if (len(transaction_times) == len(transactions) and
                    not any(observation_start < occurred_at <= end
                            for occurred_at in transaction_times)):
                issues.add("clarify", "payload.transactions",
                           "no_transactions_in_observation_window")
            if (_known(payload.get("baseline_window_end")) and
                    _parse_time(payload["baseline_window_end"]) > observation_start):
                issues.add("clarify", "payload.baseline_window_end",
                           "baseline_overlaps_observation_window")
        if _known(payload.get("baseline_amount_per_hour")) and Decimal(payload["baseline_amount_per_hour"]) == 0:
            issues.add("manual", "payload.baseline_amount_per_hour", "insufficient_baseline")
    if data["request_kind"] == "prepare_dispute_draft":
        reason = payload.get("reason_code")
        if reason is None:
            return
        reason = route["reason_aliases"].get(reason, reason)
        matrix = route["reason_matrix"][reason]
        _required(payload, matrix["required"], issues)
        _conditions(payload, matrix["conditional"], issues)
        if matrix["engine_support"] != "SYNTHETIC_INR_ONLY":
            issues.add("manual", "payload.reason_code", "local_engine_unsupported")
        if data["source_class"] != "synthetic":
            issues.add("manual", "source_class", "public_reference_not_synthetic_evidence")
        seller_requests = [
            request for request in payload.get("evidences", [])
            if type(request) is dict and request.get("source") == "REQUESTED_FROM_SELLER"
        ]
        if (payload.get("case_status") == "WAITING_FOR_SELLER_RESPONSE" and
                not seller_requests):
            issues.add("manual", "payload.evidences", "seller_request_not_present")
            issues.add("gaps", "payload.evidences", "seller_request_not_present")
        if seller_requests and "PROVIDE_EVIDENCE" not in payload.get("available_actions", []):
            issues.add("manual", "payload.available_actions", "provide_evidence_action_unavailable")
        for request in seller_requests:
            provider_type = request.get("evidence_type")
            if provider_type not in matrix.get("provider_evidence_types", []):
                issues.add("manual", "payload.evidences", "provider_request_outside_local_matrix")
                issues.add("gaps", "payload.evidences", "provider_request_outside_local_matrix")
        if end is not None and _known(payload.get("seller_response_due_date")):
            if _parse_time(payload["seller_response_due_date"]) <= end:
                issues.add("manual", "payload.seller_response_due_date", "seller_response_due_date_expired")
        if payload.get("case_status") in ("CLOSED", "RESOLVED"):
            issues.add("manual", "payload.case_status", "case_not_open_for_review")
        for name, values in matrix.get("manual_if", {}).items():
            if payload.get(name) in values:
                issues.add("manual", "payload." + name, "scenario_requires_review")
    for name, values in route.get("manual_if", {}).items():
        if payload.get(name) in values:
            issues.add("manual", "payload." + name, "scenario_requires_review")


def preflight_intake(raw_json):
    """Validate bounded JSON to a safe route plan; no action or engine execution."""
    issues = _Issues()
    if type(raw_json) is not str:
        issues.add("invalid", "envelope", "json_text_required")
        return issues.result()
    try:
        if not raw_json or len(raw_json) > _MAX_BYTES or len(raw_json.encode("utf-8")) > _MAX_BYTES:
            raise _InputError("byte_limit")
        data = json.loads(raw_json, object_pairs_hook=_pairs, parse_constant=_constant)
        _bounded_tree(data)
    except (ValueError, UnicodeError, RecursionError):
        issues.add("invalid", "envelope", "json_invalid_or_unbounded")
        return issues.result()
    _check_object(data, _SPEC["common_fields"], "envelope", issues)
    if type(data) is not dict:
        return issues.result()
    kind = data.get("request_kind")
    route = _SPEC["routes"].get(kind) if type(kind) is str else None
    if route is not None and type(data.get("payload")) is dict:
        _check_object(data["payload"], route["payload"]["fields"], "payload", issues)
        _conditions(data["payload"], route["conditional"], issues)
        theme = data.get("requested_theme")
        if type(theme) is str and theme in _SPEC["common_fields"]["requested_theme"]["values"] and theme not in route["themes"]:
            issues.add("clarify", "requested_theme", "theme_kind_mismatch")
    if issues.invalid or route is None:
        return issues.result(data)
    _reference_checks(data, data.get("evidence_items", []), issues)
    # Missing values have already been diagnosed; never dereference incomplete
    # structures or infer optional branch values to continue local processing.
    if all(name in data for name in ("payload", "evidence_items", "source_class")):
        _evidence_checks(data, route, issues)
        _coherence(data, route, issues)
    return issues.result(data, route["route"])
