"""Pinned US demo scenarios and reference-only local matching.

The catalog contains authored synthetic scenarios. It is never a catalog of
real cases, merits decisions, training labels, or provider-approved outcomes.
Import performs no I/O and all returned values are defensive copies.
"""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from .case_contract import get_contract
from .case_intake import preflight_intake


SCENARIOS_SHA256 = "fcd71e4dd145fabb7f62221b565639afe93c0725fbdb6109ad65bcd9634fc836"
CATALOG_ID = "payguard.us_demo_scenarios.v1"
PROVENANCE = "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES"
MAX_CARD_BYTES = 131072
THEMES = frozenset({"source_compliance", "velocity_guard", "dispute_mediation"})
EVIDENCE_CLASS = "SYNTHETIC_DEMO_SCENARIO"
FINAL_AUTHORITIES = frozenset({"PAYPAL", "PAYPAL_OR_EXTERNAL_ISSUER"})
EXPECTED_ROUTES = frozenset({
    "EDIT_CANCEL_OR_ACKNOWLEDGE_AND_CONTINUE",
    "REVIEW_LOCAL_BASELINE_AND_MISSING_EVIDENCE",
    "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
})
_SPEC = get_contract()
_DISPUTE_COMMON_CITATIONS = {
    "MERCHANDISE_OR_SERVICE_NOT_RECEIVED": (
        "PP-DISPUTES-OVERVIEW-AUTHORITY",
        "PP-US-PURCHASE-INR-SNAD",
        "PP-US-SELLER-ELIGIBILITY",
        "PP-US-SELLER-DELIVERY",
    ),
    "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED": (
        "PP-DISPUTES-OVERVIEW-AUTHORITY",
        "PP-US-PURCHASE-INR-SNAD",
        "PP-US-PURCHASE-COUNTERFEIT",
        "PP-US-SELLER-ELIGIBILITY",
    ),
    "UNAUTHORISED": (
        "PP-DISPUTES-OVERVIEW-AUTHORITY",
        "PP-US-SELLER-ELIGIBILITY",
        "PP-US-SELLER-DELIVERY",
    ),
}
_DISPUTE_DEFAULT_CITATIONS = ("PP-DISPUTES-OVERVIEW-AUTHORITY",)


class CaseCardsError(ValueError):
    """Fixed safe error code without source text or filesystem paths."""

    def __init__(self, code="case_cards_invalid"):
        self.code = code if code in {"case_cards_invalid", "case_cards_unavailable"} else "case_cards_invalid"
        super().__init__(self.code)


def _require(condition):
    if not condition:
        raise CaseCardsError()


def _keys(value, fields):
    _require(type(value) is dict and set(value) == set(fields))


def _text(value, cap=2000):
    from .retrieval import _text as corpus_text

    try:
        return corpus_text(value, cap)
    except Exception:
        raise CaseCardsError() from None


def _validate_catalog(document, corpus):
    _keys(document, {
        "schema_version", "catalog_id", "provenance", "jurisdiction",
        "scenario_count", "scenarios", "case_evidence_gap",
    })
    _require(type(document["schema_version"]) is int and document["schema_version"] == 1)
    _require(document["catalog_id"] == CATALOG_ID)
    _require(document["provenance"] == PROVENANCE)
    _require(document["jurisdiction"] == "US")
    _require(type(document["scenario_count"]) is int and document["scenario_count"] == 3)
    _text(document["case_evidence_gap"], 1000)
    _require("No qualifying official US final-merits case" in document["case_evidence_gap"])
    _require("never be presented as real cases" in document["case_evidence_gap"])

    chunks = {row["chunk_id"]: row for row in corpus._chunks}
    sources = corpus._sources
    scenarios = document["scenarios"]
    _require(type(scenarios) is list and len(scenarios) == 3)
    seen_ids = set()
    seen_themes = set()
    for scenario in scenarios:
        _keys(scenario, {
            "scenario_id", "theme", "title", "evidence_class",
            "citation_chunk_ids", "expected_route", "final_authority", "limitations",
        })
        scenario_id = scenario["scenario_id"]
        _text(scenario_id, 128)
        _require(re.fullmatch(r"US-DEMO-[A-Z0-9-]{1,96}", scenario_id) is not None)
        _require(scenario_id not in seen_ids)
        seen_ids.add(scenario_id)
        theme = scenario["theme"]
        _require(theme in THEMES and theme not in seen_themes)
        seen_themes.add(theme)
        _text(scenario["title"], 256)
        _require(scenario["evidence_class"] == EVIDENCE_CLASS)
        _require(scenario["expected_route"] in EXPECTED_ROUTES)
        _require(scenario["final_authority"] in FINAL_AUTHORITIES)

        citations = scenario["citation_chunk_ids"]
        _require(type(citations) is list and 1 <= len(citations) <= 20)
        _require(len(citations) == len(set(citations)))
        for chunk_id in citations:
            _require(type(chunk_id) is str and chunk_id in chunks)
            chunk = chunks[chunk_id]
            _require(chunk["_theme"] == theme)
            _require(corpus._regions[chunk["source_id"]] == "US")
            _require(sources[chunk["source_id"]]["material_type"] in {
                "official_api_reference", "official_policy",
            })
        if theme == "dispute_mediation":
            required_reason_citations = {
                row["reference_chunk_id"]
                for row in _SPEC["routes"]["prepare_dispute_draft"]["reason_matrix"].values()
            }
            required_common_citations = {
                chunk_id
                for route_citations in _DISPUTE_COMMON_CITATIONS.values()
                for chunk_id in route_citations
            }
            required_common_citations.update(_DISPUTE_DEFAULT_CITATIONS)
            _require((required_reason_citations | required_common_citations) <= set(citations))
            _require("PP-DISPUTES-OVERVIEW-AUTHORITY" in citations)

        limitations = scenario["limitations"]
        _require(type(limitations) is list and 1 <= len(limitations) <= 8)
        _require(len(limitations) == len(set(limitations)))
        for limitation in limitations:
            _text(limitation, 256)

    _require(seen_themes == THEMES)
    return document


def _load():
    try:
        from .retrieval import _json, _read_fixed, load_corpus

        root = Path(__file__).resolve(strict=True).parents[2]
        target = root / "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json"
        raw = _read_fixed(target, root)
        _require(0 < len(raw) <= MAX_CARD_BYTES)
        _require(hashlib.sha256(raw).hexdigest() == SCENARIOS_SHA256)
        document = _json(raw.decode("utf-8"))
        corpus = load_corpus()
        return _validate_catalog(document, corpus), corpus
    except CaseCardsError:
        raise
    except Exception:
        raise CaseCardsError("case_cards_unavailable") from None


def load_case_cards():
    """Return the pinned authored scenario catalog for local evaluation only."""

    return deepcopy(_load()[0])


def _selected_citation_ids(data, selected):
    if data["request_kind"] != "prepare_dispute_draft":
        return list(selected["citation_chunk_ids"])
    reason = data["payload"]["reason_code"]
    route = _SPEC["routes"]["prepare_dispute_draft"]
    canonical_reason = route["reason_aliases"].get(reason, reason)
    reason_citation = route["reason_matrix"][canonical_reason]["reference_chunk_id"]
    ordered = [
        *_DISPUTE_COMMON_CITATIONS.get(canonical_reason, _DISPUTE_DEFAULT_CITATIONS),
        reason_citation,
    ]
    allowed = set(selected["citation_chunk_ids"])
    _require(all(chunk_id in allowed for chunk_id in ordered))
    return list(dict.fromkeys(ordered))


def match_cases(raw_json):
    """Match a valid intake to authored US scenarios and official citations.

    The legacy function name is retained for API compatibility. Every output is
    explicitly labeled synthetic and cannot be used as evidence of a real case.
    """

    intake = preflight_intake(raw_json)
    result = {
        "schema_version": 1,
        "source": "local_synthetic_scenario_matcher",
        "status": "intake_blocked",
        "intake": intake,
        "matches": [],
        "provenance": PROVENANCE,
        "evaluation_scope": "AUTHORED_SYNTHETIC_DEMO_ONLY",
        "required_human_review": True,
        "operational_authority": _SPEC["review_gates"]["operational_authority"],
        "engine_execution": "NOT_RUN",
        "semantic_confidence": "NOT_EVALUATED",
        "current_policy_applicability": "NOT_ESTABLISHED",
        "real_case_evidence": "NOT_PROVIDED",
    }
    if intake["status"] not in {"ready_for_local_rules", "manual_review"}:
        return result

    try:
        catalog, corpus = _load()
        data = json.loads(raw_json)
        if data["jurisdiction"] != "US":
            return result
        theme = data["requested_theme"]
        selected = next(row for row in catalog["scenarios"] if row["theme"] == theme)
        chunk_map = {row["chunk_id"]: row for row in corpus._chunks}
        source_map = corpus._sources

        selected_citation_ids = _selected_citation_ids(data, selected)
        citations = []
        for chunk_id in selected_citation_ids:
            chunk = chunk_map[chunk_id]
            source = source_map[chunk["source_id"]]
            citations.append({
                "chunk_id": chunk_id,
                "source_id": chunk["source_id"],
                "title": source["title"],
                "url": chunk["source_url"],
                "locator": chunk["source_locator"],
                "material_type": chunk["material_type"],
                "jurisdiction": "US",
                "text_sha256": chunk["text_sha256"],
            })

        explicit = {(row["source_id"], row["chunk_id"]) for row in data.get("references", [])}
        citation_ids = {(row["source_id"], row["chunk_id"]) for row in citations}
        if explicit and not explicit.issubset(citation_ids):
            result["status"] = "evidence_missing"
            return result

        if data["request_kind"] == "reference_lookup":
            found = corpus.search(
                data["payload"]["query"],
                theme=theme,
                jurisdiction="US",
                limit=10,
                as_of=data["as_of"],
            )
            found_ids = {row["chunk_id"] for row in found["results"]}
            if not found_ids.intersection(selected_citation_ids):
                result["status"] = "evidence_missing"
                return result

        result["matches"] = [{
            "scenario_id": selected["scenario_id"],
            "title": selected["title"],
            "theme": theme,
            "jurisdiction": "US",
            "evidence_class": EVIDENCE_CLASS,
            "expected_route": selected["expected_route"],
            "final_authority": selected["final_authority"],
            "limitations": deepcopy(selected["limitations"]),
            "citations": citations,
            "real_case_evidence": "NOT_PROVIDED",
        }]
        result["status"] = "synthetic_scenarios_found"
    except Exception:
        result["status"] = "reference_unavailable"
        result["matches"] = []
    return result
