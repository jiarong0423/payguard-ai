"""Offline policy-evidence inventory; never certifies current applicability.

The public entry always calls the accepted fixed pinned retrieval loader. This
module deliberately couples to ReferenceCorpus's private snapshot fields at the
accepted corpus version. The bounded detached snapshot is internal only, never
a caller-provided authority or metadata argument. Import performs no I/O.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import hashlib
import re
from types import MappingProxyType

from .retrieval import AUTHORITY, CHUNKS_SHA256, CORPUS_ID, SOURCE_SHA256, ReferenceCorpus, load_corpus


REGIONS = frozenset({"US"})
THEMES = frozenset({"source_compliance", "velocity_guard", "dispute_mediation"})
VERSION = "payguard.applicability.v1"
_DIGESTS = MappingProxyType({"sources_sha256": SOURCE_SHA256, "chunks_sha256": CHUNKS_SHA256})
_COMBINED = hashlib.sha256((SOURCE_SHA256 + "\n" + CHUNKS_SHA256).encode("ascii")).hexdigest()
_SOURCE_KEYS = ("source_id", "title", "url", "material_type", "jurisdiction", "retrieved_at", "source_updated_date", "source_updated_date_status", "effective_date", "effective_date_status", "decision_date", "decision_date_status", "decision_acceptance_deadline", "content_class", "representation")
_NON_POLICY = {
    "official_api_reference": "API_REFERENCE_NOT_POLICY",
    "public_court_order_copy": "PROCEDURE_NOT_APPLICABLE_POLICY",
}
LIMITATIONS = (
    "Saved authored summaries are incomplete evidence, not complete policy documents.",
    "Document update, policy effective, saved observation and decision dates are distinct.",
    "All saved effective dates are unverified; current policy applicability is not established.",
    "Observation freshness does not establish policy effect, account eligibility or semantic truth.",
    "Procedural court orders and API documents cannot establish applicable policy.",
    "No cross-region fallback or eligibility inference is performed; human review is required.",
    "Reference evidence authorizes no payment, refund, submission or other financial action.",
)


class ApplicabilityError(ValueError):
    """Fixed sanitized code, without input text, corpus details or local paths."""
    def __init__(self, code):
        if type(code) is not str or code not in {"applicability_filter_invalid", "applicability_corpus_unavailable"}:
            code = "applicability_corpus_unavailable"
        self.code = code
        super().__init__(code)


def _invalid():
    raise ApplicabilityError("applicability_filter_invalid")


def _instant(value):
    try:
        if type(value) is datetime:
            parsed = value
        elif type(value) is str and len(value) <= 64 and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})", value):
            parsed = datetime.fromisoformat(value)
        else:
            _invalid()
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            _invalid()
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError, TypeError):
        _invalid()


def _validate_filters(jurisdiction, as_of, observation_max_age_days, theme):
    if type(jurisdiction) is not str or len(jurisdiction) > 6 or jurisdiction not in REGIONS or (theme is not None and (type(theme) is not str or len(theme) > 32 or theme not in THEMES)):
        _invalid()
    if type(observation_max_age_days) is not int or not 0 <= observation_max_age_days <= 365000:
        _invalid()
    return _instant(as_of)


@dataclass(frozen=True)
class _EvidenceSnapshot:
    """Internal detached scalar metadata, immutable mappings; no corpus text."""
    sources: MappingProxyType
    chunks: MappingProxyType
    regions: MappingProxyType


def _load_snapshot():
    """Only trusted fixed loader; private-field coupling is version/count bound."""
    try:
        corpus = load_corpus()
        if type(corpus) is not ReferenceCorpus or corpus._digests != _DIGESTS or corpus._combined != _COMBINED:
            raise ValueError("snapshot_identity")
        if len(corpus._sources) != 16 or len(corpus._chunks) != 29 or set(corpus._regions) != set(corpus._sources):
            raise ValueError("snapshot_bounds")
        sources = {}
        for sid, source in corpus._sources.items():
            if sid != source["source_id"] or corpus._regions[sid] not in REGIONS or source["content_class"] != "public_reference_summary" or source["representation"] != "authored_paraphrase_not_full_source":
                raise ValueError("snapshot_source")
            sources[sid] = MappingProxyType({key: source[key] for key in _SOURCE_KEYS})
        chunks = {}
        for row in corpus._chunks:
            cid, sid = row["chunk_id"], row["source_id"]
            if cid in chunks or sid not in sources or row["_theme"] not in THEMES or row["operational_authority"] != AUTHORITY:
                raise ValueError("snapshot_chunk")
            chunks[cid] = MappingProxyType({"chunk_id": cid, "source_id": sid, "theme": row["_theme"], "case_stage": row["_stage"], "material_type": row["material_type"], "case_outcome": row["case_outcome"], "text_sha256": row["text_sha256"]})
        return _EvidenceSnapshot(MappingProxyType(sources), MappingProxyType(chunks), MappingProxyType(dict(corpus._regions)))
    except Exception:
        raise ApplicabilityError("applicability_corpus_unavailable") from None


def _source_state(source, instant, budget):
    observation = _instant(source["retrieved_at"])
    age = instant - observation
    if age < timedelta(0):
        observation_status = "FUTURE_OBSERVATION"
    elif age > timedelta(days=budget):
        observation_status = "STALE_OBSERVATION"
    else:
        observation_status = "WITHIN_OBSERVATION_BUDGET"
    reasons = ["SUMMARY_COVERAGE_INCOMPLETE"]
    if observation_status != "WITHIN_OBSERVATION_BUDGET":
        reasons.append(observation_status)
    if source["source_updated_date"] is None:
        reasons.append("DOCUMENT_UPDATE_DATE_MISSING")
    elif date.fromisoformat(source["source_updated_date"]) > instant.date():
        reasons.append("DOCUMENT_UPDATE_IN_FUTURE")
    if source["effective_date"] is None:
        reasons.append("UNKNOWN_EFFECTIVE_DATE")
    elif date.fromisoformat(source["effective_date"]) > instant.date():
        reasons.append("EFFECTIVE_DATE_IN_FUTURE")
    if source["material_type"] != "official_policy":
        reasons.append(_NON_POLICY[source["material_type"]])
    return observation_status, sorted(reasons)


def _assess_snapshot(snapshot, jurisdiction, instant, budget, theme):
    """Trusted internal helper for evaluator; never an external metadata API."""
    regional_sources = {sid for sid, region in snapshot.regions.items() if region == jurisdiction}
    selected_chunks = sorted((row for row in snapshot.chunks.values() if row["source_id"] in regional_sources and (theme is None or row["theme"] == theme)), key=lambda row: row["chunk_id"])
    selected_sources = sorted({row["source_id"] for row in selected_chunks})
    source_reports = []
    combined_reasons = {"SUMMARY_COVERAGE_INCOMPLETE", "CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED"}
    for sid in selected_sources:
        source = snapshot.sources[sid]
        status, reasons = _source_state(source, instant, budget)
        combined_reasons.update(reasons)
        source_reports.append(dict(source, jurisdiction_normalized=jurisdiction,
                                   observation_status=status, observation_age_basis="saved_retrieved_at_exact_elapsed_time",
                                   current_policy_applicability="NOT_ESTABLISHED", reason_codes=reasons,
                                   citation_chunk_ids=[row["chunk_id"] for row in selected_chunks if row["source_id"] == sid]))
    official_sources = [sid for sid in selected_sources if snapshot.sources[sid]["material_type"] == "official_policy"]
    if not official_sources:
        combined_reasons.add("NO_OFFICIAL_POLICY_COVERAGE")
    if not selected_chunks:
        combined_reasons.add("NO_REFERENCE_COVERAGE")
    thematic_counts = {topic: sum(1 for row in snapshot.chunks.values() if row["source_id"] in regional_sources and row["theme"] == topic and row["material_type"] == "official_policy") for topic in sorted(THEMES)}
    return {"schema_version": 1, "version": VERSION, "source": "public_reference", "corpus_id": CORPUS_ID,
            "corpus_digest": _COMBINED, "corpus_digests": dict(_DIGESTS),
            "filters_applied": {"jurisdiction": jurisdiction, "theme": theme, "as_of": instant.isoformat(), "observation_max_age_days": budget},
            "status": "INCOMPLETE_POLICY_EVIDENCE", "current_policy_applicability": "NOT_ESTABLISHED",
            "advisory_only": True, "operational_authority": AUTHORITY, "requires_human_review": True,
            "coverage": {"complete": False, "basis": "pinned_authored_summaries_only", "regional_source_count": len(regional_sources),
                         "selected_source_count": len(selected_sources), "selected_chunk_count": len(selected_chunks),
                         "official_policy_source_ids": official_sources, "official_policy_chunk_count_by_theme": thematic_counts,
                         "missing_official_policy_themes": [topic for topic, count in thematic_counts.items() if not count]},
            "sources": source_reports, "chunks": [dict(row, jurisdiction=jurisdiction) for row in selected_chunks],
            "reason_codes": sorted(combined_reasons), "limitations": list(LIMITATIONS)}


def assess_applicability(jurisdiction, as_of, observation_max_age_days, *, theme=None):
    """Assess reference evidence, never current policy or merchant eligibility.

    Exact region/theme; aware as_of; strict explicit 0..365000-day observation
    budget. No caller corpus, metadata, path or loader arguments are accepted.
    Freshness uses saved retrieved_at, never update/effective/decision dates.
    """
    instant = _validate_filters(jurisdiction, as_of, observation_max_age_days, theme)
    snapshot = _load_snapshot()
    try:
        return _assess_snapshot(snapshot, jurisdiction, instant, observation_max_age_days, theme)
    except Exception:
        raise ApplicabilityError("applicability_corpus_unavailable") from None
