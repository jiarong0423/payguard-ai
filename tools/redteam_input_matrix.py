"""Reproducible input-guard attack matrix for every JSON endpoint (in-process, no network).

For each endpoint the request schema (FastAPI's OpenAPI) gives the fields and their limits. A valid baseline body is
built (with real ids from a set-up call where an endpoint needs them), then one field at a time is replaced by an
attack value: boundary lengths, overflow, negative and huge numbers, NaN/Infinity, wrong types, control and bidi
characters, injection strings, missing and extra fields. Whole-request attacks follow: huge and deeply nested bodies,
malformed JSON, wrong content type, missing or foreign session and CSRF headers, path traversal in path parameters.

Verdicts per request:
  BROKEN     server error (5xx), timeout-like slowness (> SLOW_SECONDS), or a stack trace / local path in the body
  GAP        an attack value the schema forbids was accepted (2xx)
  GUARDED    refused with 4xx
  OK         a valid value accepted
Exit code 1 when any BROKEN or GAP is found, so the same command is the regression check after a fix.

Usage (project root):
  PYTHONPATH=src:backend python3 tools/redteam_input_matrix.py --out <dir> [--round R1]
Writes <dir>/matrix_<round>.jsonl (one line per request) and <dir>/matrix_<round>.md (the impact matrix).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from unittest.mock import patch

SEED = 20261102
SLOW_SECONDS = 2.0
ROOT = "/api/v1"
ORIGIN = "http://127.0.0.1:8000"
# Split like tools/validate_public_candidate.py so this file itself carries no home-directory path.
LEAK_MARKERS = ("Traceback", "File \"/", "/" + "Users/", "/" + "home/", "site-packages", "OPENAI", "API_KEY", "SECRET")

# Values that satisfy the documented patterns, used for baselines.
PATTERN_SAMPLES = {
    "^[A-Za-z0-9_-]+$": "a" * 40,
    "^[a-f0-9]{64}$": "0" * 64,
    "^[0-9]{1,7}\\.[0-9]{2}$": "10.00",
    "^PP-[A-Z0-9][A-Z0-9-]{2,62}$": "PP-D-12345",
    "^case-ref-[0-9]{3}$": "case-ref-001",
}


def string_attacks(spec):
    lo, hi = spec.get("minLength", 0), spec.get("maxLength")
    attacks = [("empty", "", lo == 0 and "pattern" not in spec and "enum" not in spec),
               ("spaces_only", "   ", None),
               ("null_byte", "abc\x00def", None),
               ("control_chars", "a\x07\x1b[31mred\x08", None),
               ("bidi_override", "‮gnp.exe", None),
               ("emoji", "\U0001F600" * 8, None),
               ("script_tag", "<script>alert(1)</script>", None),
               ("sql_fragment", "' OR 1=1 --", None),
               ("path_traversal", "../../../etc/passwd", None),
               ("template_injection", "${jndi:ldap://x}{{7*7}}", None),
               ("huge_100k", "a" * 100_000, False if hi is not None else None),
               ("type_int", 12345, False), ("type_float", 1.5, False), ("type_bool", True, False),
               ("type_list", ["a"], False), ("type_object", {"a": 1}, False)]
    if hi is not None:
        attacks += [("at_max", "a" * hi, None if "pattern" in spec else True), ("max_plus_1", "a" * (hi + 1), False)]
    if lo > 1:
        attacks.append(("min_minus_1", "a" * (lo - 1), False))
    if "enum" in spec:
        attacks = [("enum_unknown", "NOT_A_CHOICE", False), ("enum_case", str(spec["enum"][0]).swapcase(), False),
                   ("enum_padded", f" {spec['enum'][0]} ", False)] + attacks
    if "pattern" in spec:
        attacks.append(("pattern_breaker", "ZZZ!!", False))
    return attacks


def number_attacks(spec):
    lo, hi = spec.get("minimum"), spec.get("maximum")
    attacks = [("negative", -1, False if lo is not None and lo >= 0 else None), ("zero", 0, None if lo is None else lo <= 0),
               ("int64_overflow", 2 ** 63, False if hi is not None else None), ("huge_float", 1e308, False),
               ("neg_huge", -(2 ** 63), False), ("fraction", 3.5, False), ("numeric_string", "5", None),
               ("nan_literal", "__NaN__", False), ("inf_literal", "__Infinity__", False),
               ("type_bool", True, None), ("type_list", [1], False), ("type_null", None, False)]
    if lo is not None:
        attacks.append(("below_min", int(lo) - 1, False))
    if hi is not None:
        attacks += [("at_max", int(hi), True), ("above_max", int(hi) + 1, False)]
    return attacks


def bool_attacks(_spec):
    return [("string_true", "true", None), ("int_one", 1, None), ("string_yes", "yes", False), ("type_null", None, False),
            ("type_list", [True], False)]


def array_attacks(spec):
    n = spec.get("maxItems", 64)
    return [("empty", [], None), ("over_max_items", ["a"] * (n + 1), False if "maxItems" in spec else None),
            ("huge_items", ["a"] * 10_000, False), ("nested", [[["x"]]], False), ("item_null", [None], None),
            ("item_huge", ["a" * 100_000], False), ("type_string", "abc", False)]


def resolve(spec, components):
    if "$ref" in spec:
        return components[spec["$ref"].split("/")[-1]]
    if "anyOf" in spec:
        concrete = [item for item in spec["anyOf"] if item.get("type") != "null"]
        merged = dict(resolve(concrete[0], components)) if concrete else {}
        merged["nullable"] = True
        return merged
    return spec


def attacks_for(spec, components):
    spec = resolve(spec, components)
    kind = spec.get("type")
    if kind == "string" or "enum" in spec:
        return string_attacks(spec)
    if kind in ("integer", "number"):
        return number_attacks(spec)
    if kind == "boolean":
        return bool_attacks(spec)
    if kind == "array":
        return array_attacks(spec)
    return [("type_string", "abc", False), ("type_list", [], False), ("type_null", None, None)]


def baseline_value(spec, components):
    spec = resolve(spec, components)
    if "enum" in spec:
        return spec["enum"][0]
    kind = spec.get("type")
    if kind == "string":
        if spec.get("pattern") in PATTERN_SAMPLES:
            return PATTERN_SAMPLES[spec["pattern"]]
        return "wireless headphones"[: spec.get("maxLength", 64)].ljust(spec.get("minLength", 1), "x")
    if kind in ("integer", "number"):
        return int(spec.get("minimum", 1)) if spec.get("minimum", 1) > 0 else 1
    if kind == "boolean":
        return False
    if kind == "array":
        return []
    if kind == "object":
        return {}
    return None


class Harness:
    def __init__(self, rate_limit=None):
        os.environ.pop("PAYGUARD_DEMO_MODE", None)
        import httpx
        from fastapi.testclient import TestClient
        from app.main import create_app
        from app.paypal import PaypalAdapter, PaypalConfig
        from app.store import SessionStore
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(
            lambda request: (_ for _ in ()).throw(AssertionError("no provider call"))))
        with patch.dict(os.environ, {}, clear=True):
            # Field attacks lift the per-session rate limit so every request reaches the field checks; the limit
            # itself is attacked separately with the default store (rate_limit_attacks).
            store = SessionStore(rate_limit=rate_limit) if rate_limit else SessionStore()
            self.app = create_app(store=store, paypal=provider)
        self.client = TestClient(self.app, base_url=ORIGIN, client=("127.0.0.1", 55011), raise_server_exceptions=False)
        self.client.__enter__()
        self.spec = self.app.openapi()
        self.components = self.spec.get("components", {}).get("schemas", {})
        self.session = self.new_session()

    def new_session(self):
        return self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def headers(self, session=None):
        session = session or self.session
        return {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}

    def send(self, method, path, body=None, headers=None, raw=None, content_type="application/json"):
        headers = dict(self.headers() if headers is None else headers)
        started = time.perf_counter()
        if raw is not None:
            headers["content-type"] = content_type
            response = self.client.request(method, path, content=raw, headers=headers)
        elif method == "GET":
            response = self.client.get(path, headers=headers)
        else:
            text = json.dumps(body).replace('"__NaN__"', "NaN").replace('"__Infinity__"', "Infinity")
            headers["content-type"] = content_type
            response = self.client.request(method, path, content=text.encode(), headers=headers)
        return response, time.perf_counter() - started

    # Real ids for endpoints that refuse made-up ones, so field attacks reach past the id check.
    def fixtures(self):
        review = self.client.post(ROOT + "/aup/review", json={"description": "wireless headphones"}, headers=self.headers()).json()
        self.client.post(ROOT + "/demo/inject", json={"scenario": "dispute"}, headers=self.headers())
        draft = self.client.post(ROOT + "/disputes/case-ref-001/draft", json={}, headers=self.headers()).json()
        return {"evaluation_id": review.get("evaluation_id"), "description_digest": review.get("description_digest"),
                "draft_digest": draft.get("draft_digest")}

    def endpoints(self):
        for path, ops in self.spec["paths"].items():
            for method, op in ops.items():
                schema = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
                model = self.components[schema["$ref"].split("/")[-1]] if schema and "$ref" in schema else None
                yield method.upper(), path, model, [p["name"] for p in op.get("parameters", []) if p.get("in") == "path"]


def verdict(status, elapsed, text, expected_valid):
    # A 5xx counts as broken unless it is the app's own closed error (e.g. 503 ai_disabled: the feature is off).
    closed_error = text.startswith('{"error":{"code":') and status in (502, 503)
    if (status >= 500 and not closed_error) or elapsed > SLOW_SECONDS or any(marker in text for marker in LEAK_MARKERS):
        return "BROKEN"
    if 200 <= status < 300:
        return "GAP" if expected_valid is False else "OK"
    return "GUARDED"


def rate_limit_attacks(record):
    """Default store: the 61st request in a minute from one session and the 31st session creation are refused."""
    harness = Harness()
    last = None
    for _ in range(61):
        last = harness.send("GET", ROOT + "/demo/state")
    record("GET /api/v1/demo/state", "(rate)", "61_requests_in_a_minute", False, *last)
    for _ in range(31):
        last = harness.send("POST", ROOT + "/demo/sessions", {}, headers={"Origin": ORIGIN})
    record("POST /api/v1/demo/sessions", "(rate)", "31_sessions_in_a_minute", False, *last)


def concrete(path, params):
    return path.replace("{case_ref}", "case-ref-001").replace("{dispute_id}", "PP-D-12345") if params else path


def run(out_dir: Path, round_name: str) -> int:
    random.seed(SEED)
    harness = Harness(rate_limit=10 ** 9)
    rows = []

    def record(endpoint, field, attack, expected, response, elapsed):
        text = response.text[:4000]
        rows.append({"endpoint": endpoint, "field": field, "attack": attack, "expected_valid": expected,
                     "status": response.status_code, "ms": round(elapsed * 1000, 1),
                     "verdict": verdict(response.status_code, elapsed, text, expected), "body": text[:300]})

    for method, path, model, params in harness.endpoints():
        if path.endswith("/demo/sessions") or path.endswith("/studio/agent-turn"):
            continue
        endpoint = f"{method} {path}"
        url = concrete(path, params)
        fixtures = harness.fixtures()  # fresh ids per endpoint: some calls consume them
        properties = (model or {}).get("properties", {})
        base = {name: fixtures.get(name) or baseline_value(spec, harness.components) for name, spec in properties.items()}
        if method != "GET":
            for name, spec in properties.items():
                for attack, value, expected in attacks_for(spec, harness.components):
                    body = dict(base)
                    body[name] = value
                    response, elapsed = harness.send(method, url, body)
                    record(endpoint, name, attack, expected, response, elapsed)
                missing = {key: value for key, value in base.items() if key != name}
                required = name in (model or {}).get("required", [])
                response, elapsed = harness.send(method, url, missing)
                record(endpoint, name, "missing", None if not required else False, response, elapsed)
            for attack, body, expected in (("extra_field", {**base, "zz_extra": "x"}, False),
                                           ("body_is_list", [base], False), ("body_is_null", None, False)):
                response, elapsed = harness.send(method, url, body)
                record(endpoint, "(body)", attack, expected, response, elapsed)
            for attack, raw, content_type in (("malformed_json", b'{"a": ', "application/json"),
                                              ("deep_nesting", b"[" * 50_000 + b"]" * 50_000, "application/json"),
                                              ("body_2mb", json.dumps({"x": "a" * 2_000_000}).encode(), "application/json"),
                                              ("form_encoded", b"a=1", "application/x-www-form-urlencoded"),
                                              ("utf16_body", json.dumps(base).encode("utf-16"), "application/json"),
                                              ("invalid_utf8", b'{"text": "\xff\xfe"}', "application/json")):
                response, elapsed = harness.send(method, url, raw=raw, content_type=content_type)
                record(endpoint, "(body)", attack, False, response, elapsed)
            other = harness.new_session()
            for attack, headers in (("no_session", {"Origin": ORIGIN}),
                                    ("foreign_csrf", {**harness.headers(), "X-CSRF-Token": other["csrf_token"]}),
                                    ("bad_origin", {**harness.headers(), "Origin": "http://evil.example"}),
                                    ("no_origin", {k: v for k, v in harness.headers().items() if k != "Origin"}),
                                    ("csrf_latin1", {**harness.headers(), "X-CSRF-Token": b"\xe9" * 43}),
                                    ("session_latin1", {**harness.headers(), "X-Demo-Session": b"\xe9" * 43})):
                response, elapsed = harness.send(method, url, base, headers=headers)
                record(endpoint, "(headers)", attack, False, response, elapsed)
        for param in params:
            for attack, value in (("traversal", "..%2F..%2Fetc%2Fpasswd"), ("dot_dot", ".."), ("long", "c" * 5000),
                                  ("unicode", "case-ref-١٢٣"), ("script", "%3Cscript%3E"),
                                  ("negative", "case-ref--01"), ("overflow_digits", "case-ref-" + "9" * 400)):
                response, elapsed = harness.send(method, path.replace("{" + param + "}", value), {} if method != "GET" else None)
                record(endpoint, param, attack, False, response, elapsed)

    rate_limit_attacks(record)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / f"matrix_{round_name}.jsonl").open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
    counts = Counter(row["verdict"] for row in rows)
    by_endpoint = defaultdict(Counter)
    for row in rows:
        by_endpoint[row["endpoint"]][row["verdict"]] += 1
    lines = [f"# Input-guard impact matrix, round {round_name}", "",
             f"Seed {SEED}; {len(rows)} requests; " + ", ".join(f"{key} {counts[key]}" for key in ("BROKEN", "GAP", "GUARDED", "OK")), "",
             "| Endpoint | BROKEN | GAP | GUARDED | OK |", "|---|---:|---:|---:|---:|"]
    for endpoint in sorted(by_endpoint):
        c = by_endpoint[endpoint]
        lines.append(f"| {endpoint} | {c['BROKEN']} | {c['GAP']} | {c['GUARDED']} | {c['OK']} |")
    lines += ["", "## BROKEN and GAP rows", "", "| Verdict | Endpoint | Field | Attack | Status | ms | Body (start) |", "|---|---|---|---|---:|---:|---|"]
    for row in rows:
        if row["verdict"] in ("BROKEN", "GAP"):
            body = row["body"][:90].replace("|", "/").replace("\n", " ")
            lines.append(f"| {row['verdict']} | {row['endpoint']} | {row['field']} | {row['attack']} | {row['status']} | {row['ms']} | {body} |")
    (out_dir / f"matrix_{round_name}.md").write_text("\n".join(lines) + "\n")
    print(f"round {round_name}: {len(rows)} requests; " + ", ".join(f"{key} {counts[key]}" for key in ("BROKEN", "GAP", "GUARDED", "OK")))
    return 1 if counts["BROKEN"] or counts["GAP"] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--round", default="R1")
    args = parser.parse_args()
    sys.exit(run(Path(args.out), args.round))
