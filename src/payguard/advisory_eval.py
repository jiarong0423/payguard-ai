"""Offline structured-reference gates; no model generation or semantic proof.

Public bytes are untrusted data. Only the trusted outer request identifies the
region/theme/time/budget; source metadata always comes from the fixed loader.
The argument-free CLI runs authored synthetic fixtures, never candidate files.
"""

import json
import logging
import re
import sys
import unicodedata

from . import applicability
from .retrieval import AUTHORITY, CHUNKS_SHA256, CORPUS_ID, SOURCE_SHA256


VERSION = "payguard.advisory_eval.v1"
MAX_BYTES = 65536
MAX_DEPTH = 8
MAX_CLAIMS = 20
MAX_TEXT = 2000
CLAIM_TYPES = frozenset({"policy_reference", "current_policy", "procedural_reference", "api_reference", "financial_action", "assurance"})
_TYPE_REQUIREMENTS = {
    "policy_reference": {("official_policy", "not_applicable")},
    "current_policy": {("official_policy", "not_applicable")},
    "procedural_reference": {("public_court_order_copy", "procedural_order")},
    "api_reference": {("official_api_reference", "not_applicable")},
}
_ENVELOPE_FIELDS = {"schema_version", "jurisdiction", "theme", "as_of", "status", "advisory_only", "operational_authority", "claims"}
_CLAIM_FIELDS = {"claim_id", "claim_type", "text", "citation_chunk_ids"}
_ERROR_CODES = frozenset({"advisory_input_invalid", "advisory_json_invalid", "advisory_schema_invalid", "advisory_context_mismatch", "advisory_corpus_unavailable"})


class AdvisoryError(ValueError):
    """Fixed sanitized code; raw candidate fragments are never retained."""
    def __init__(self, code):
        self.code = code if type(code) is str and code in _ERROR_CODES else "advisory_input_invalid"
        super().__init__(self.code)


def _fail(code):
    raise AdvisoryError(code)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("advisory_json_invalid")
        result[key] = value
    return result


def _constant(_value):
    _fail("advisory_json_invalid")


def _scan_depth(raw):
    depth = 0
    quoted = False
    escaped = False
    for value in raw:
        if quoted:
            if escaped:
                escaped = False
            elif value == 92:
                escaped = True
            elif value == 34:
                quoted = False
        elif value == 34:
            quoted = True
        elif value in (91, 123):
            depth += 1
            if depth > MAX_DEPTH:
                _fail("advisory_json_invalid")
        elif value in (93, 125):
            depth -= 1
            if depth < 0:
                _fail("advisory_json_invalid")
    if depth != 0 or quoted:
        _fail("advisory_json_invalid")


def _parse(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_BYTES:
        _fail("advisory_input_invalid")
    _scan_depth(raw)
    try:
        parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise AdvisoryError("advisory_json_invalid") from None
    stack = [(parsed, 0)]
    while stack:
        value, depth = stack.pop()
        if depth > MAX_DEPTH:
            _fail("advisory_json_invalid")
        if type(value) is str:
            if len(value) > MAX_TEXT or any(unicodedata.category(char).startswith("C") for char in value):
                _fail("advisory_schema_invalid")
        elif type(value) is dict:
            if len(value) > 20:
                _fail("advisory_schema_invalid")
            stack.extend((key, depth + 1) for key in value)
            stack.extend((item, depth + 1) for item in value.values())
        elif type(value) is list:
            if len(value) > MAX_CLAIMS:
                _fail("advisory_schema_invalid")
            stack.extend((item, depth + 1) for item in value)
        elif value is not None and type(value) not in (int, bool):
            _fail("advisory_schema_invalid")
    return parsed


def _validate_envelope(payload, jurisdiction, theme, instant):
    if type(payload) is not dict or set(payload) != _ENVELOPE_FIELDS or type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        _fail("advisory_schema_invalid")
    if payload["status"] != "manual_review" or payload["advisory_only"] is not True or payload["operational_authority"] != AUTHORITY:
        _fail("advisory_schema_invalid")
    try:
        inner_instant = applicability._validate_filters(payload["jurisdiction"], payload["as_of"], 0, payload["theme"])
    except applicability.ApplicabilityError:
        raise AdvisoryError("advisory_schema_invalid") from None
    if payload["jurisdiction"] != jurisdiction or payload["theme"] != theme or inner_instant != instant:
        _fail("advisory_context_mismatch")
    claims = payload["claims"]
    if type(claims) is not list or not 1 <= len(claims) <= MAX_CLAIMS:
        _fail("advisory_schema_invalid")
    claim_ids = set()
    citation_ids = set()
    for claim in claims:
        if type(claim) is not dict or set(claim) != _CLAIM_FIELDS:
            _fail("advisory_schema_invalid")
        cid, kind, text, citations = (claim[key] for key in ("claim_id", "claim_type", "text", "citation_chunk_ids"))
        if type(cid) is not str or not re.fullmatch(r"[A-Z0-9_-]{1,64}", cid) or cid in claim_ids or type(kind) is not str or kind not in CLAIM_TYPES or type(text) is not str or not text.strip():
            _fail("advisory_schema_invalid")
        claim_ids.add(cid)
        if type(citations) is not list or not 1 <= len(citations) <= 10:
            _fail("advisory_schema_invalid")
        for reference in citations:
            if type(reference) is not str or not re.fullmatch(r"[A-Z0-9-]{1,128}", reference) or reference in citation_ids:
                _fail("advisory_schema_invalid")
            citation_ids.add(reference)
    return claims


def evaluate_advisory(candidate_bytes, *, jurisdiction, theme, as_of, observation_max_age_days):
    """Gate bounded structure only. Valid prose remains NOT_EVALUATED.

    Outer request fields are mandatory and must match the untrusted envelope;
    public callers cannot provide source metadata, a corpus, path or loader.
    Citation IDs are unique throughout the envelope, including across claims.
    """
    if theme is None:
        _fail("advisory_input_invalid")
    try:
        instant = applicability._validate_filters(jurisdiction, as_of, observation_max_age_days, theme)
    except applicability.ApplicabilityError:
        raise AdvisoryError("advisory_input_invalid") from None
    payload = _parse(candidate_bytes)
    claims = _validate_envelope(payload, jurisdiction, theme, instant)
    try:
        snapshot = applicability._load_snapshot()
        evidence = applicability._assess_snapshot(snapshot, jurisdiction, instant, observation_max_age_days, theme)
    except Exception:
        raise AdvisoryError("advisory_corpus_unavailable") from None
    source_reports = {row["source_id"]: row for row in evidence["sources"]}
    gates = []
    for index, claim in enumerate(claims):
        reasons = set()
        known_ids = []
        if claim["claim_type"] == "financial_action":
            reasons.add("ACTION_CLAIM_FORBIDDEN")
        elif claim["claim_type"] == "assurance":
            reasons.add("ASSURANCE_CLAIM_FORBIDDEN")
        for reference in claim["citation_chunk_ids"]:
            row = snapshot.chunks.get(reference)
            if row is None:
                reasons.add("CITATION_UNKNOWN")
                continue
            known_ids.append(row["chunk_id"])
            if snapshot.regions[row["source_id"]] != jurisdiction:
                reasons.add("CITATION_REGION_MISMATCH")
            if row["theme"] != theme:
                reasons.add("CITATION_THEME_MISMATCH")
            if claim["claim_type"] in _TYPE_REQUIREMENTS and (row["material_type"], row["case_stage"]) not in _TYPE_REQUIREMENTS[claim["claim_type"]]:
                reasons.add("CLAIM_REFERENCE_TYPE_MISMATCH")
            source_report = source_reports.get(row["source_id"])
            if source_report is not None:
                for reason in ("FUTURE_OBSERVATION", "STALE_OBSERVATION", "DOCUMENT_UPDATE_IN_FUTURE"):
                    if reason in source_report["reason_codes"]:
                        reasons.add(reason)
        if claim["claim_type"] == "current_policy":
            reasons.add("CURRENT_POLICY_NOT_ESTABLISHED")
        rejected = bool(reasons & {"ACTION_CLAIM_FORBIDDEN", "ASSURANCE_CLAIM_FORBIDDEN", "CITATION_UNKNOWN", "CITATION_REGION_MISMATCH", "CITATION_THEME_MISMATCH", "CLAIM_REFERENCE_TYPE_MISMATCH"})
        status = "REJECTED" if rejected else "INCOMPLETE_EVIDENCE" if reasons else "STRUCTURE_COMPATIBLE"
        gates.append({"claim_index": index, "claim_type": claim["claim_type"], "status": status,
                      "trusted_citation_chunk_ids": sorted(known_ids), "reason_codes": sorted(reasons)})
    statuses = {row["status"] for row in gates}
    overall = "REJECTED" if "REJECTED" in statuses else "INCOMPLETE_EVIDENCE" if "INCOMPLETE_EVIDENCE" in statuses else "STRUCTURE_COMPATIBLE"
    return {"schema_version": 1, "version": VERSION, "source": "offline_structured_gate", "status": overall,
            "requested_context": evidence["filters_applied"], "corpus_id": CORPUS_ID, "corpus_digest": evidence["corpus_digest"],
            "corpus_digests": dict(evidence["corpus_digests"]), "advisory_only": True, "operational_authority": AUTHORITY,
            "requires_human_review": True, "semantic_entailment": "NOT_EVALUATED", "PII_quality": "NOT_EVALUATED",
            "prompt_injection_quality": "NOT_EVALUATED", "natural_language_action_assurance_quality": "NOT_EVALUATED", "model_generation": "NOT_RUN",
            "claim_count": len(gates), "claim_gates": gates,
            "current_policy_applicability": evidence["current_policy_applicability"], "coverage": dict(evidence["coverage"]),
            "limitations": ["Only finite claim/citation/authority/context structure is checked; free prose entailment and safety remain unassessed.",
                            "Compatible structure does not establish factual grounding, policy effect, account eligibility or financial authority.",
                            "Candidate text and candidate claim IDs are not returned, stored or logged."] + list(evidence["limitations"])}


def _synthetic_bytes(region, theme, claim_type, citation, *, as_of="2026-10-05T00:00:00Z"):
    return json.dumps({"schema_version": 1, "jurisdiction": region, "theme": theme, "as_of": as_of,
                       "status": "manual_review", "advisory_only": True, "operational_authority": AUTHORITY,
                       "claims": [{"claim_id": "SYNTHETIC_CLAIM", "claim_type": claim_type,
                                   "text": "Authored synthetic reference statement requiring human review.", "citation_chunk_ids": [citation]}]},
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def benchmark():
    """Fixed US-only authored fixtures; reports no candidate prose or model accuracy."""
    snapshot = applicability._load_snapshot()
    def select(theme, kind):
        identifiers = sorted(row["chunk_id"] for row in snapshot.chunks.values()
                             if snapshot.regions[row["source_id"]] == "US" and row["theme"] == theme
                             and row["material_type"] == kind)
        if not identifiers:
            raise AdvisoryError("advisory_corpus_unavailable")
        return identifiers[0]
    policy = select("source_compliance", "official_policy")
    procedure = select("source_compliance", "public_court_order_copy")
    api_reference = select("dispute_mediation", "official_api_reference")
    specs = [
        ("POLICY_REFERENCE", "source_compliance", "policy_reference", policy, "STRUCTURE_COMPATIBLE", "2026-10-06T04:00:00Z", 30),
        ("CURRENT_POLICY_UNKNOWN_EFFECT", "source_compliance", "current_policy", policy, "INCOMPLETE_EVIDENCE", "2026-10-06T04:00:00Z", 30),
        ("PROCEDURE_AS_POLICY", "source_compliance", "current_policy", procedure, "REJECTED", "2026-10-06T04:00:00Z", 30),
        ("PROCEDURE_REFERENCE", "source_compliance", "procedural_reference", procedure, "STRUCTURE_COMPATIBLE", "2026-10-06T04:00:00Z", 30),
        ("API_REFERENCE", "dispute_mediation", "api_reference", api_reference, "STRUCTURE_COMPATIBLE", "2026-10-06T04:00:00Z", 30),
        ("MISMATCH_THEME", "velocity_guard", "policy_reference", policy, "REJECTED", "2026-10-06T04:00:00Z", 30),
        ("UNKNOWN_CITATION", "source_compliance", "policy_reference", "SYNTHETIC-NONEXISTENT", "REJECTED", "2026-10-06T04:00:00Z", 30),
        ("ACTION_FORBIDDEN", "source_compliance", "financial_action", policy, "REJECTED", "2026-10-06T04:00:00Z", 30),
        ("ASSURANCE_FORBIDDEN", "source_compliance", "assurance", policy, "REJECTED", "2026-10-06T04:00:00Z", 30),
        ("STALE_OBSERVATION", "source_compliance", "policy_reference", policy, "INCOMPLETE_EVIDENCE", "2026-11-06T04:00:00Z", 1),
        ("FUTURE_OBSERVATION", "source_compliance", "policy_reference", policy, "INCOMPLETE_EVIDENCE", "2026-10-05T04:00:00Z", 30),
    ]
    cases = []
    for case_id, theme, kind, reference, expected, instant, budget in specs:
        result = evaluate_advisory(_synthetic_bytes("US", theme, kind, reference, as_of=instant), jurisdiction="US", theme=theme, as_of=instant, observation_max_age_days=budget)
        cases.append({"case_id": case_id, "expected_gate": expected, "observed_gate": result["status"], "matched": result["status"] == expected})
    document = json.loads(_synthetic_bytes(
        "US", "source_compliance", "policy_reference", policy,
        as_of="2026-10-06T04:00:00Z",
    ))
    duplicate_document = json.loads(json.dumps(document))
    duplicate_document["claims"][0]["citation_chunk_ids"].append(policy)
    forged_document = json.loads(json.dumps(document))
    forged_document["claims"][0]["source_id"] = "SYNTHETIC-FORGED-SOURCE"
    parse_specs = [
        ("DUPLICATE_JSON", b'{"x":1,"x":2}', "advisory_json_invalid"),
        ("NONFINITE_JSON", b'{"x":NaN}', "advisory_json_invalid"),
        ("BAD_ENVELOPE", b'{}', "advisory_schema_invalid"),
        ("DUPLICATE_CITATIONS", json.dumps(duplicate_document).encode("utf-8"), "advisory_schema_invalid"),
        ("FORGED_SOURCE_METADATA", json.dumps(forged_document).encode("utf-8"), "advisory_schema_invalid"),
        ("CONTEXT_MISMATCH", _synthetic_bytes("US", "velocity_guard", "policy_reference", policy), "advisory_context_mismatch"),
        ("DEPTH_LIMIT", b'[' * 9 + b'0' + b']' * 9, "advisory_json_invalid"),
    ]
    for case_id, raw, expected in parse_specs:
        try:
            evaluate_advisory(raw, jurisdiction="US", theme="source_compliance", as_of="2026-10-06T04:00:00Z", observation_max_age_days=30)
            observed = "UNEXPECTED_ACCEPT"
        except AdvisoryError as exc:
            observed = exc.code
        cases.append({"case_id": case_id, "expected_gate": expected, "observed_gate": observed, "matched": observed == expected})
    return {"schema_version": 1, "benchmark_id": "payguard.us_synthetic_structured_gates.v2", "fixture_source": "authored_synthetic_candidates",
            "status": "PASS" if all(case["matched"] for case in cases) else "FAIL", "case_count": len(cases),
            "matched_count": sum(case["matched"] for case in cases), "cases": cases,
            "corpus_id": CORPUS_ID, "corpus_digests": {"sources_sha256": SOURCE_SHA256, "chunks_sha256": CHUNKS_SHA256},
            "model_generation": "NOT_RUN", "semantic_entailment": "NOT_EVALUATED", "requires_human_review": True,
            "advisory_only": True, "operational_authority": AUTHORITY,
            "limitations": ["PASS concerns expected structured gate outcomes, not actual model accuracy or semantic safety.", "No candidate prose is returned; current policy applicability and account eligibility are not established."]}


def main():
    if len(sys.argv) != 1:
        logging.error("PAYGUARD_EVALUATION_ARGUMENTS_REJECTED")
        return 64
    try:
        report = benchmark()
        print(json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False))
        return 0 if report["status"] == "PASS" else 2
    except Exception:
        logging.error("PAYGUARD_EVALUATION_FAILED")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
