"""Strict synthetic inbox; no real webhook verification is implied."""

import hashlib
import json


def collect_events(events: list[dict]) -> list[dict]:
    if not isinstance(events, list) or len(events) > 1000:
        raise ValueError("invalid_event_batch")
    seen: dict[str, str] = {}
    accepted = []
    for event in events:
        if not isinstance(event, dict) or set(event) != {"event_id", "source", "event_type", "resource"}:
            raise ValueError("invalid_event_schema")
        if event["source"] != "synthetic":
            raise ValueError("unverified_event_source")
        identifier = event["event_id"]
        if not isinstance(identifier, str) or not identifier.startswith("demo-") or len(identifier) > 100:
            raise ValueError("invalid_event_id")
        if event["event_type"] != "PAYMENT.CAPTURE.COMPLETED":
            raise ValueError("unsupported_event_type")
        resource = event["resource"]
        if not isinstance(resource, dict) or set(resource) != {"order_id", "amount", "currency", "occurred_at"}:
            raise ValueError("invalid_resource_schema")
        if any(not isinstance(value, str) or not value or len(value) > 100 for value in resource.values()):
            raise ValueError("invalid_resource_field")
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), allow_nan=False)
        digest = hashlib.sha256(canonical.encode()).hexdigest()
        if identifier in seen:
            if seen[identifier] != digest:
                raise ValueError("event_id_collision")
            continue
        seen[identifier] = digest
        accepted.append(dict(resource))
    return accepted
