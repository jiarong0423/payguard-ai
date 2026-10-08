"""Allowlisted identity tokens; pseudonymization, not anonymization."""

import hashlib
import hmac
import unicodedata


def redact_identity(identity: dict[str, str], key: bytes) -> dict[str, str]:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("invalid_token_key")
    if not isinstance(identity, dict) or not identity or set(identity) - {"name", "address", "email"}:
        raise ValueError("identity_fields_not_allowlisted")
    tokens = {}
    for field, raw in identity.items():
        if not isinstance(raw, str) or not raw.strip() or len(raw) > 500:
            raise ValueError("invalid_identity_field")
        normalized = unicodedata.normalize("NFKC", raw).strip().casefold()
        message = ("payguard.identity.v1\x00" + field + "\x00" + normalized).encode()
        tokens[field + "_token"] = hmac.new(key, message, hashlib.sha256).hexdigest()
    return tokens
