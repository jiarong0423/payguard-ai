"""Bounded synthetic-document pseudonymization; limited detection, no reverse map.

Clean-room design: detect spans, union every overlap, then replace typed spans.
This module contains no upstream pii-guard implementation or model dependency.
Exact input indices and text are used without Unicode normalization.
"""

import hashlib
import hmac
import re
import unicodedata


MAX_TEXT_BYTES = 16384
MAX_OUTPUT_BYTES = 32768
MAX_LITERALS = 32
MAX_LITERAL_LENGTH = 500
MAX_SPANS = 128
METHOD = "HMAC-SHA256 document pseudonymization v1"
EXPORT_PROFILE = "INTERNAL_REVIEW_ONLY_V1"
TYPES = frozenset({"email", "us_phone", "id_like", "name", "address", "manual", "mixed"})
LIMITATIONS = (
    "Detection covers fixed ASCII email, US phone and SSN-like patterns plus exact host-supplied literals only.",
    "Full-width variants, other phone formats, names, addresses and contextual identifiers may remain undetected.",
    "Manual review is required; pseudonymization is not legal anonymization or proof of privacy compliance.",
)
_PATTERNS = (
    ("email", re.compile(r"(?<![A-Za-z0-9.!#$%&'*+/=?^_`{|}~-])[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]{1,64}@"
                         r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
                         r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+(?![A-Za-z0-9-])")),
    ("us_phone", re.compile(r"(?<![A-Za-z0-9])(?:\+1[- .]?)?(?:\([2-9][0-9]{2}\)|[2-9][0-9]{2})[- .]?[0-9]{3}[- .]?[0-9]{4}(?![A-Za-z0-9])")),
    ("id_like", re.compile(r"(?<![0-9])[0-9]{3}-[0-9]{2}-[0-9]{4}(?![0-9])")),
)


class DocumentPrivacyError(ValueError):
    """Fixed-code exception; never retain or render raw document/literal values."""
    def __init__(self, code):
        allowed = {"document_invalid", "document_limit", "document_scope_invalid", "document_key_invalid",
                   "document_literals_invalid", "document_span_limit", "document_output_limit"}
        self.code = code if type(code) is str and code in allowed else "document_invalid"
        super().__init__(self.code)


def _text_bytes(value, *, limit, code):
    if type(value) is not str or len(value) > limit:
        raise DocumentPrivacyError(code)
    try:
        encoded = value.encode("utf-8", errors="strict")
    except UnicodeError:
        raise DocumentPrivacyError(code) from None
    if len(encoded) > limit:
        raise DocumentPrivacyError(code)
    if any(unicodedata.category(character).startswith("C") and character not in "\n\r\t" for character in value):
        raise DocumentPrivacyError("document_invalid")
    return encoded


def redact_dispute_document(text, key, *, document_id, literals=None):
    """Return metadata and substituted text only, for a synthetic host-owned document.

    ``literals`` is a list of exact ``{"type": "name|address|manual", "text": str}``
    entries supplied by the host, never model-selected authority. Stable tokens
    apply only within one exact document and key. No input, spans or map survive
    in the returned value; no file, network, logging or model operations occur.
    """
    if type(text) is not str:
        raise DocumentPrivacyError("document_invalid")
    encoded = _text_bytes(text, limit=MAX_TEXT_BYTES, code="document_limit")
    if type(key) is not bytes or not 32 <= len(key) <= 128 or len(set(key)) < 8:
        raise DocumentPrivacyError("document_key_invalid")
    if (type(document_id) is not str or not 1 <= len(document_id) <= 128 or
            not re.fullmatch(r"[A-Za-z0-9_.:-]+", document_id)):
        raise DocumentPrivacyError("document_scope_invalid")
    if literals is None:
        literals = []
    if type(literals) is not list or len(literals) > MAX_LITERALS:
        raise DocumentPrivacyError("document_literals_invalid")
    approved = []
    for literal in literals:
        if (type(literal) is not dict or set(literal) != {"type", "text"} or
                type(literal["type"]) is not str or literal["type"] not in {"name", "address", "manual"} or
                type(literal["text"]) is not str or not literal["text"].strip() or
                len(literal["text"]) > MAX_LITERAL_LENGTH):
            raise DocumentPrivacyError("document_literals_invalid")
        _text_bytes(literal["text"], limit=MAX_LITERAL_LENGTH * 4, code="document_literals_invalid")
        approved.append((literal["type"], literal["text"]))

    spans = []
    def add(start, end, kind):
        if len(spans) >= MAX_SPANS:
            raise DocumentPrivacyError("document_span_limit")
        spans.append((start, end, {kind}))

    for kind, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            add(match.start(), match.end(), kind)
    for kind, literal in approved:
        cursor = 0
        while True:
            start = text.find(literal, cursor)
            if start < 0:
                break
            add(start, start + len(literal), kind)
            cursor = start + 1

    unions = []
    for start, end, kinds in sorted(spans, key=lambda span: (span[0], span[1])):
        if unions and start < unions[-1][1]:
            previous_start, previous_end, previous_kinds = unions[-1]
            unions[-1] = (previous_start, max(previous_end, end), previous_kinds | kinds)
        else:
            unions.append((start, end, kinds))

    scope = hmac.new(key, b"payguard.document.scope.v1\x00" + document_id.encode("ascii") + b"\x00" + encoded,
                     hashlib.sha256).digest()
    parts = []
    counts = {}
    cursor = 0
    for start, end, kinds in unions:
        kind = next(iter(kinds)) if len(kinds) == 1 else "mixed"
        raw = text[start:end].encode("utf-8")
        token = hmac.new(key, b"payguard.document.token.v1\x00" + scope + b"\x00" + kind.encode("ascii") + b"\x00" + raw,
                         hashlib.sha256).hexdigest()
        parts.extend((text[cursor:start], "[" + kind.upper() + "_" + token + "]"))
        cursor = end
        counts[kind] = counts.get(kind, 0) + 1
    parts.append(text[cursor:])
    redacted = "".join(parts)
    if len(redacted.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise DocumentPrivacyError("document_output_limit")
    return {"export_profile": EXPORT_PROFILE, "redacted_text": redacted,
            "replacement_count": len(unions), "counts": dict(sorted(counts.items())),
            "types": sorted(counts), "method": METHOD, "limited_detection": True, "manual_review_required": True,
            "source": "synthetic", "reversibility": False, "limitations": list(LIMITATIONS)}
