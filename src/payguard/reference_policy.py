"""Pinned, metadata-only policy references. Import performs no I/O.

Authority labels are input assertions, not authenticated provider/merchant evidence.
This module resolves references only; it never opens, stats or evaluates rules.
"""

from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, timezone
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from types import MappingProxyType
import unicodedata


_MODULE_PROJECT_ROOT = Path(__file__).absolute().parents[2]
_PROJECT_ROOT = _MODULE_PROJECT_ROOT
_PACKAGE_PATH = "US/paypal_aup_reference_v1"
_PACKAGE_ID = "US_PAYPAL_AUP_REFERENCE_20261006_V1"
_SOURCE_ID = "PP-US-AUP-2022-10-29-OBSERVED-2026-10-06"
_POLICY_VERSION = "US_AUP_VISIBLE_UPDATE_2022_10_29_OBSERVED_2026_10_06"
_PINS = MappingProxyType({
    "registry.json": "488d25b40651118dcc5cfa3b603a05a57a52ff6b4217cfedbe18a4ff7e94e90b",
    "US/paypal_aup_reference_v1/manifest.json": "63177d0ce5de3e4c80101633b82d703219033c09287773fefc954289295b005a",
    "US/paypal_aup_reference_v1/source_index.json": "df46a8dbcdaadb71dd37d0d893c49ce0f084113ee12a84f0c34d7891b725fe92",
})
_MAX_BYTES = 65536
_OUTCOMES = frozenset({"INVALID_INPUT", "CONTEXT_CONFLICT", "PACKAGE_INTEGRITY_FAILURE", "PACKAGE_UNAVAILABLE", "UNSUPPORTED", "EVALUATE"})
_WARNING_LIMITATION = "PayGuard presents references and review signals before the ordinary PayPal flow; it does not decide compliance, block provider submission, submit an AUP review or replace PayPal's policy judgment."
_AUTHORITY_LIMITATION = "Context authority/provenance labels are unverified caller assertions; this runtime cannot authenticate provider accounts or merchant legal entities."
_FIELDS = frozenset({"policy_domain", "provider_account_region", "merchant_legal_region", "buyer_destination_region", "issuer_region_signal", "ip_country_signal", "event_time", "evaluated_at", "policy_as_of"})
_AUTHORITIES = frozenset({"PROVIDER_VERIFIED", "MERCHANT_VERIFIED", "USER_CLAIMED", "DERIVED_SIGNAL", "UNKNOWN"})
_PROVENANCE = frozenset({"PROVIDER_ACCOUNT_RECORD", "MERCHANT_ENTITY_RECORD", "USER_INPUT", "SIGNAL_SUMMARY", "SYSTEM_CLOCK", "EVENT_RECORD", "SNAPSHOT_REQUEST", "NOT_PROVIDED", "SYNTHETIC_TEST"})
_OPTIONAL_REGIONS = ("buyer_destination_region", "issuer_region_signal", "ip_country_signal")


class ReferencePolicyError(ValueError):
    """Fixed sanitized outcome/code; no caller values or paths in the exception."""
    def __init__(self, outcome, code):
        if outcome not in _OUTCOMES - {"EVALUATE"}:
            raise ValueError("INVALID_ERROR_OUTCOME")
        self.outcome = outcome
        self.code = code
        super().__init__(code)


def _fail(code, outcome="PACKAGE_INTEGRITY_FAILURE"):
    raise ReferencePolicyError(outcome, code)


def _exact(value, keys, code="SCHEMA_INVALID"):
    if type(value) is not dict or len(value) != len(keys) or set(value) != set(keys):
        _fail(code)


def _literal(value, expected):
    if type(value) is not type(expected) or value != expected:
        _fail("SCHEMA_INVALID")


def _text(value, cap=2000):
    if type(value) is not str or not value or len(value) > cap or any(unicodedata.category(c).startswith("C") for c in value):
        _fail("SCHEMA_INVALID")
    try:
        if len(value.encode("utf-8")) > cap * 4:
            _fail("SCHEMA_INVALID")
    except UnicodeError:
        _fail("SCHEMA_INVALID")


def _digest(value):
    if type(value) is not str or not re.fullmatch(r"[0-9a-f]{64}", value):
        _fail("SCHEMA_INVALID")


def _instant(value, outcome="PACKAGE_INTEGRITY_FAILURE"):
    if type(value) is not str or len(value) > 64:
        _fail("DATE_INVALID", outcome)
    match = re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-](?P<offset_hour>[0-9]{2}):(?P<offset_minute>[0-9]{2}))", value)
    if match is None:
        _fail("DATE_INVALID", outcome)
    if match.group("offset_hour") is not None:
        offset_hour = int(match.group("offset_hour"))
        offset_minute = int(match.group("offset_minute"))
        if offset_hour > 23 or offset_minute > 59 or offset_hour * 60 + offset_minute >= 24 * 60:
            _fail("DATE_INVALID", outcome)
    try:
        parsed = datetime.fromisoformat(value)
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        _fail("DATE_INVALID", outcome)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _nonfinite(_value):
    _fail("JSON_INVALID")


def _bounded_tree(value, depth=0, budget=None):
    if budget is None:
        budget = [1000]
    budget[0] -= 1
    if depth > 8 or budget[0] < 0:
        _fail("JSON_LIMIT_EXCEEDED")
    if type(value) is dict:
        if len(value) > 64:
            _fail("JSON_LIMIT_EXCEEDED")
        for key, child in value.items():
            _text(key, 128)
            _bounded_tree(child, depth + 1, budget)
    elif type(value) is list:
        if len(value) > 64:
            _fail("JSON_LIMIT_EXCEEDED")
        for child in value:
            _bounded_tree(child, depth + 1, budget)
    elif type(value) is str:
        _text(value)
    elif value is not None and type(value) not in (bool, int):
        _fail("SCHEMA_INVALID")


def _parse(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= _MAX_BYTES:
        _fail("FILE_SIZE_INVALID")
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_nonfinite)
        _bounded_tree(document)
        return document
    except ReferencePolicyError:
        raise
    except (ValueError, UnicodeError, RecursionError, TypeError):
        _fail("JSON_INVALID")


def _validate_registry(registry):
    _exact(registry, {"schema_version", "registry_status", "packages", "promotion_requires"})
    _literal(registry["schema_version"], "1.0")
    _literal(registry["registry_status"], "CURRENT_REFERENCE_PROFILE")
    if type(registry["packages"]) is not list or len(registry["packages"]) != 1:
        _fail("SCHEMA_INVALID")
    entry = registry["packages"][0]
    _exact(entry, {"package_id", "relative_path", "active_tier", "allowed_next_tier", "canonical_runtime_active", "manifest_sha256", "source_evidence_path", "source_evidence_sha256"})
    _text(entry["active_tier"], 128)
    if entry["active_tier"] != "REFERENCE_ONLY":
        _fail("TIER_UNSUPPORTED", "UNSUPPORTED")
    expected = {"package_id": _PACKAGE_ID, "relative_path": _PACKAGE_PATH, "active_tier": "REFERENCE_ONLY", "allowed_next_tier": "SHADOW", "canonical_runtime_active": True,
                "manifest_sha256": _PINS[_PACKAGE_PATH + "/manifest.json"], "source_evidence_path": "../../../docs/decisions/2026Q4/us_mainline_contract.md",
                "source_evidence_sha256": "305f1de611f7713c5c66f6e6ae20107156364414dbc4e7a248d831cbc6f22c18"}
    for key, value in expected.items():
        _literal(entry[key], value)
    _literal(registry["promotion_requires"], ["independent_verification_pass", "explicit_canonical_apply_scope", "same-version loader and interpreter validation", "negative and conflict vectors", "rollback and no-op evidence"])
    # source_evidence_path is historical metadata only, never followed as a path.


def _validate_manifest(manifest):
    expected = {"schema_version": "1.0", "package_id": _PACKAGE_ID, "jurisdiction": "US", "policy_domain": "AUP", "policy_version": _POLICY_VERSION,
                "effective_from": None, "effective_to": None, "effective_status": "NOT_VERIFIED", "execution_tier": "REFERENCE_ONLY",
                "maximum_tier_without_new_source_evidence": "SHADOW", "retroactive": False, "source_ids": [_SOURCE_ID],
                "rules_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "approval_ref": None,
                "current_policy_applicability": "NOT_ESTABLISHED", "workflow_transition_authorized": False, "external_action_authorized": False,
                "full_policy_text_included": False, "origin_bytes_archived": False, "status": "CURRENT_REFERENCE_PROFILE"}
    _exact(manifest, expected)
    _text(manifest["execution_tier"], 128)
    if manifest["execution_tier"] != "REFERENCE_ONLY":
        _fail("TIER_UNSUPPORTED", "UNSUPPORTED")
    for key, value in expected.items():
        _literal(manifest[key], value)
    _digest(manifest["rules_sha256"])


def _validate_sources(document):
    _exact(document, {"schema_version", "sources", "limitations"})
    _literal(document["schema_version"], "1.0")
    if type(document["sources"]) is not list or len(document["sources"]) != 1:
        _fail("SCHEMA_INVALID")
    source = document["sources"][0]
    constants = {"source_id": _SOURCE_ID, "authority": "PayPal", "jurisdiction": "US", "locale": "en_US", "title": "PayPal Acceptable Use Policy",
                 "url": "https://www.paypal.com/us/legalhub/paypal/acceptableuse-full?country.x=US&locale.x=en_US", "observed_at": "2026-10-06T12:00:00+08:00",
                 "visible_updated_date": "2022-10-29", "visible_updated_date_status": "DOCUMENT_STATED", "effective_from": None,
                 "effective_to": None, "effective_status": "NOT_VERIFIED", "current_policy_applicability": "NOT_ESTABLISHED",
                 "representation": "STRUCTURED_PARAPHRASE_AND_CONTROLLED_LABELS_NOT_FULL_SOURCE", "origin_bytes_archived": False,
                 "origin_bytes_sha256": None, "rights": "Source rights retained by PayPal; no redistribution license inferred."}
    _exact(source, set(constants) | {"locators"})
    for key, value in constants.items():
        _literal(source[key], value)
    _instant(source["observed_at"])
    try:
        date.fromisoformat(source["visible_updated_date"])
    except ValueError:
        _fail("DATE_INVALID")
    expected_locators = ["AUP_PROHIBITED_ACTIVITIES", "AUP_PRIOR_APPROVAL_ACTIVITIES", "AUP_CATEGORY_DISTINCTION"]
    locators = source["locators"]
    if type(locators) is not list or len(locators) != len(expected_locators):
        _fail("SCHEMA_INVALID")
    for locator, identifier in zip(locators, expected_locators):
        _exact(locator, {"locator_id", "heading", "semantic_use"})
        _literal(locator["locator_id"], identifier)
        _text(locator["heading"], 256)
        _text(locator["semantic_use"], 512)
    limitations = document["limitations"]
    if type(limitations) is not list or len(limitations) != 6 or any(type(value) is not str for value in limitations):
        _fail("SCHEMA_INVALID")
    if len(set(limitations)) != 6:
        _fail("SCHEMA_INVALID")
    for limitation in limitations:
        _text(limitation, 1000)


def _read_pinned(relative_path):
    """Descriptor-relative no-follow read, including every root ancestor."""
    if relative_path not in _PINS:
        _fail("PATH_NOT_ALLOWLISTED")
    parent_fd = file_fd = None
    try:
        if any(not hasattr(os, name) for name in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")) or os.open not in os.supports_dir_fd:
            _fail("SAFE_READER_UNAVAILABLE")
        if _PROJECT_ROOT == _MODULE_PROJECT_ROOT:
            try:
                root = Path(__file__).resolve(strict=True).parents[2]
            except (OSError, RuntimeError, IndexError):
                _fail("METADATA_UNAVAILABLE", "PACKAGE_UNAVAILABLE")
        else:
            root = _PROJECT_ROOT.absolute()
        components = root.parts[1:] + ("policies",) + tuple(relative_path.split("/"))
        if any(part in ("", ".", "..") for part in components):
            _fail("PATH_NOT_ALLOWLISTED")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        parent_fd = os.open(root.anchor, flags)
        for component in components[:-1]:
            next_fd = os.open(component, flags, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = next_fd
        file_fd = os.open(components[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
        info = os.fstat(file_fd)
        if not stat.S_ISREG(info.st_mode):
            _fail("FILE_TYPE_INVALID")
        if not 0 < info.st_size <= _MAX_BYTES:
            _fail("FILE_SIZE_INVALID")
        with os.fdopen(file_fd, "rb") as stream:
            file_fd = None
            raw = stream.read(_MAX_BYTES + 1)
        if not 0 < len(raw) <= _MAX_BYTES:
            _fail("FILE_SIZE_INVALID")
        if hashlib.sha256(raw).hexdigest() != _PINS[relative_path]:
            _fail("HASH_MISMATCH")
        return raw
    except ReferencePolicyError:
        raise
    except (ValueError, NotImplementedError):
        _fail("PATH_NOT_ALLOWLISTED")
    except OSError as exc:
        if exc.errno in (errno.ELOOP, errno.ENOTDIR):
            _fail("PATH_BOUNDARY_VIOLATION")
        _fail("METADATA_UNAVAILABLE", "PACKAGE_UNAVAILABLE")
    finally:
        if file_fd is not None:
            os.close(file_fd)
        if parent_fd is not None:
            os.close(parent_fd)


@dataclass(frozen=True, init=False)
class ReferencePackage:
    """Validated immutable serialized snapshot; outputs are detached copies."""
    _metadata_bytes: bytes

    def __init__(self, *args, **kwargs):
        _fail("VALIDATED_LOAD_REQUIRED")

    def metadata(self):
        return json.loads(self._metadata_bytes)


def load_reference_package():
    """Load exactly three pinned metadata files; callers supply no paths/pins."""
    documents = {}
    errors = []
    validators = (("registry.json", _validate_registry), (_PACKAGE_PATH + "/manifest.json", _validate_manifest), (_PACKAGE_PATH + "/source_index.json", _validate_sources))
    for relative, validator in validators:
        try:
            document = _parse(_read_pinned(relative))
            validator(document)
            documents[relative] = document
        except ReferencePolicyError as exc:
            errors.append(exc)
    if errors:
        precedence = {"PACKAGE_INTEGRITY_FAILURE": 0, "PACKAGE_UNAVAILABLE": 1, "UNSUPPORTED": 2}
        raise min(errors, key=lambda exc: precedence[exc.outcome])
    manifest = documents[_PACKAGE_PATH + "/manifest.json"]
    sources = documents[_PACKAGE_PATH + "/source_index.json"]
    selected = {key: manifest[key] for key in ("package_id", "jurisdiction", "policy_domain", "policy_version", "effective_from", "effective_to", "effective_status", "execution_tier", "source_ids", "current_policy_applicability", "origin_bytes_archived")}
    selected.update({"sources": sources["sources"], "limitations": sources["limitations"] + [_WARNING_LIMITATION, _AUTHORITY_LIMITATION], "metadata_sha256": dict(_PINS),
                     "metadata_snapshot_sha256": hashlib.sha256(json.dumps(dict(_PINS), sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                     "integrity_scope": "PINNED_METADATA_ONLY", "rules_integrity_verified": False,
                     "rules_loaded": False, "rules_evaluated": False, "canonical_runtime_active": True,
                     "evaluation_mode": "REFERENCE_METADATA_ONLY", "compliance_decision": "NOT_MADE",
                     "workflow_transition_authorized": False, "external_action_authorized": False, "advisory_only": True})
    package = object.__new__(ReferencePackage)
    object.__setattr__(package, "_metadata_bytes", json.dumps(selected, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return package


def _context(context):
    if type(context) is not dict or len(context) != len(_FIELDS) + 1 or set(context) != _FIELDS | {"authority"}:
        _fail("CONTEXT_SCHEMA_INVALID", "INVALID_INPUT")
    authority = context["authority"]
    if type(authority) is not dict or len(authority) != len(_FIELDS) or set(authority) != _FIELDS:
        _fail("CONTEXT_AUTHORITY_INVALID", "INVALID_INPUT")
    for field in sorted(_FIELDS):
        descriptor = authority[field]
        if type(descriptor) is not dict or len(descriptor) != 2 or set(descriptor) != {"authority_class", "provenance"}:
            _fail("CONTEXT_AUTHORITY_INVALID", "INVALID_INPUT")
        if type(descriptor["authority_class"]) is not str or len(descriptor["authority_class"]) > 64 or descriptor["authority_class"] not in _AUTHORITIES or type(descriptor["provenance"]) is not str or len(descriptor["provenance"]) > 64 or descriptor["provenance"] not in _PROVENANCE:
            _fail("CONTEXT_AUTHORITY_INVALID", "INVALID_INPUT")
    domain = context["policy_domain"]
    if type(domain) is not str or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,31}", domain):
        _fail("CONTEXT_SCHEMA_INVALID", "INVALID_INPUT")
    for field in ("provider_account_region", "merchant_legal_region", *_OPTIONAL_REGIONS):
        value = context[field]
        if value is not None and (type(value) is not str or not re.fullmatch(r"[A-Z]{2}|UNKNOWN", value)):
            _fail("CONTEXT_SCHEMA_INVALID", "INVALID_INPUT")
        label = authority[field]["authority_class"]
        if (value in (None, "UNKNOWN")) != (label == "UNKNOWN"):
            _fail("CONTEXT_AUTHORITY_INVALID", "INVALID_INPUT")
        if field in ("issuer_region_signal", "ip_country_signal") and label not in {"DERIVED_SIGNAL", "UNKNOWN"}:
            _fail("SIGNAL_AUTHORITY_INVALID", "INVALID_INPUT")
    times = {key: _instant(context[key], "INVALID_INPUT") for key in ("event_time", "evaluated_at", "policy_as_of")}
    if times["event_time"] > times["evaluated_at"] or times["policy_as_of"] > times["evaluated_at"]:
        _fail("TIME_ORDER_INVALID", "INVALID_INPUT")
    return deepcopy(context)


def _result(outcome, code, context=None, metadata=None, diagnostics=None):
    return {"schema_version": "1.0", "outcome": outcome, "reason_code": code,
            "evaluation_mode": "REFERENCE_METADATA_ONLY", "compliance_decision": "NOT_MADE",
            "workflow_transition_authorized": False, "external_action_authorized": False,
            "advisory_only": True, "rules_loaded": False, "rules_evaluated": False,
            "current_policy_applicability": "NOT_ESTABLISHED", "context": context,
            "reference_metadata": metadata, "diagnostics": diagnostics or [],
            "limitations": [_WARNING_LIMITATION, _AUTHORITY_LIMITATION]}


def resolve_reference_context(context):
    """Resolve the one accepted AUP reference without policy/rule evaluation.

    Invalid input precedes primary conflict, integrity, availability, unsupported.
    Auxiliary signals remain diagnostics and cannot change AUP package selection.
    """
    try:
        snapshot = _context(context)
    except ReferencePolicyError as exc:
        return _result(exc.outcome, exc.code)
    domain = snapshot["policy_domain"]
    provider = snapshot["provider_account_region"]
    merchant = snapshot["merchant_legal_region"]
    authority = snapshot["authority"]
    primary_authority = authority["provider_account_region"]["authority_class"] == "PROVIDER_VERIFIED" and authority["merchant_legal_region"]["authority_class"] == "MERCHANT_VERIFIED"
    if primary_authority and provider not in (None, "UNKNOWN") and merchant not in (None, "UNKNOWN") and provider != merchant:
        return _result("CONTEXT_CONFLICT", "AUTHORITATIVE_REGION_CONFLICT", snapshot)
    diagnostics = []
    for field in _OPTIONAL_REGIONS:
        if snapshot[field] not in (None, "UNKNOWN", provider):
            diagnostics.append({"code": "GEO_SIGNAL_CONFLICT", "dimension": field, "routing_effect": "NONE_REFERENCE_ONLY_AUP"})
    if domain != "AUP":
        return _result("UNSUPPORTED", "DOMAIN_UNSUPPORTED", snapshot, diagnostics=diagnostics)
    if provider in (None, "UNKNOWN") or merchant in (None, "UNKNOWN") or not primary_authority:
        return _result("UNSUPPORTED", "AUTHORITATIVE_REGION_REQUIRED", snapshot, diagnostics=diagnostics)
    if provider != "US" or merchant != "US":
        return _result("UNSUPPORTED", "REGION_UNSUPPORTED", snapshot, diagnostics=diagnostics)
    try:
        metadata = load_reference_package().metadata()
    except ReferencePolicyError as exc:
        return _result(exc.outcome, exc.code, snapshot, diagnostics=diagnostics)
    return _result("EVALUATE", "REFERENCE_METADATA_RESOLVED", snapshot, metadata, diagnostics)
