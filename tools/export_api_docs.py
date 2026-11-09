#!/usr/bin/env python3
"""Write the local console's API description: an OpenAPI 3.1 file and a Postman collection made from it.

Reads the FastAPI application in-process (no server, no network, no key). Output is deterministic: running it twice
gives the same bytes, and `--check` fails when the committed files are out of date.

Usage: PYTHONPATH=src:backend python3 -B tools/export_api_docs.py [--check]
Writes docs/api/openapi.json, docs/api/postman_collection.json and docs/api/postman_run_collection.json. Exit 0 ok, 1 stale with --check, 2 import failure.
"""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "backend")]
OUT = ROOT / "docs" / "api"


TAG_TEXT = {
    "aup": "Acceptable-use keyword check and the invoice review that follows it.",
    "country": "Ten-country import and export rules, clause search and the country check.",
    "demo": "Demo session, scenarios and local state.",
    "guide": "Evidence guide: gap filling over closed form items.",
    "paypal": "PayPal Sandbox connection, disputes and the gated evidence request (local console only).",
    "studio": "AG Studio agent route (local live mode only).",
    "ai": "Evidence brief (local console with a model profile only).",
    "references": "Pinned official references and search over them.",
    "health": "Liveness check.",
    "other": "Other console routes.",
}
ERROR_SCHEMA = {"type": "object", "description": "The error body every refusal uses.", "required": ["error"],
                "properties": {"error": {"type": "object", "description": "What was refused and why.", "required": ["code", "message"],
                                         "properties": {"code": {"type": "string", "description": "Stable machine-readable reason, for example session_required."},
                                                        "message": {"type": "string", "description": "A plain sentence for a person."}}}}}
ERROR_RESPONSES = {"401": "A valid demo session is required (session_required).", "429": "Too many requests; the body says when to retry."}


_DATA_KEYS = ("example", "examples", "default", "enum", "const")


def simplify_schemas(node, in_properties=False):
    """Drop the auto-generated schema titles (APIMatic rejects duplicates) and write integer exclusive bounds as inclusive ones."""
    if isinstance(node, list):
        for item in node:
            simplify_schemas(item)
        return
    if not isinstance(node, dict):
        return
    if not in_properties:
        if isinstance(node.get("title"), str):
            del node["title"]
        if node.get("type") == "integer":
            for key, inclusive, step in (("exclusiveMaximum", "maximum", -1), ("exclusiveMinimum", "minimum", 1)):
                value = node.get(key)
                if isinstance(value, (int, float)) and not isinstance(value, bool) and float(value).is_integer():
                    del node[key]
                    node[inclusive] = int(value) + step
    for key, value in node.items():
        if key in _DATA_KEYS:
            continue
        simplify_schemas(value, in_properties=(key == "properties" and not in_properties))


def humanize(name):
    words = str(name).replace("-", "_").split("_")
    text = " ".join(word for word in words if word)
    return (text[:1].upper() + text[1:] + ".") if text else "Value."


def describe(spec):
    """Fill in what the generated description lacks: servers, contact, tags, readable operation ids, descriptions and the error body."""
    from app.demo_mode import DISABLED_ROUTES
    info = spec["info"]
    info["summary"] = "Read-only rule checks and a gated evidence workflow for small PayPal sellers, on synthetic data."
    info["contact"] = {"name": "TradeGlot", "url": "https://github.com/jiarong0423/payguard-ai"}
    info["license"] = {"name": "MIT", "identifier": "MIT"}
    spec["servers"] = [{"url": "http://127.0.0.1:8000", "description": "Local console (synthetic data)"}]
    used_tags, seen_ids = set(), set()
    for path in sorted(spec["paths"]):
        parts = [part for part in path.split("/") if part and part not in ("api", "v1")]
        tag = parts[0] if parts and parts[0] in TAG_TEXT else ("other" if parts else "health")
        for method, operation in sorted(spec["paths"][path].items()):
            used_tags.add(tag)
            operation["tags"] = [tag]
            base = "_".join([method.lower()] + [part.strip("{}").replace("-", "_") for part in parts]) or method.lower()
            operation_id, n = base, 2
            while operation_id in seen_ids:
                operation_id, n = "%s_%d" % (base, n), n + 1
            seen_ids.add(operation_id)
            operation["operationId"] = operation_id
            summary = operation.get("summary") or ("%s %s" % (method.upper(), path))
            operation["summary"] = summary
            text = operation.get("description") or ("%s. Local console route %s %s on synthetic data; advisory only." % (summary.rstrip("."), method.upper(), path))
            if (method.upper(), path) in DISABLED_ROUTES:
                text += " The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls."
            operation["description"] = text
            for parameter in operation.get("parameters", []):
                parameter.setdefault("description", humanize(parameter.get("name", "")))
            for code, message in ERROR_RESPONSES.items():
                operation.setdefault("responses", {}).setdefault(code, {"description": message, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorBody"}}}})
    spec["tags"] = [{"name": name, "description": TAG_TEXT[name]} for name in sorted(used_tags)]
    schemas = spec.setdefault("components", {}).setdefault("schemas", {})
    schemas["ErrorBody"] = ERROR_SCHEMA
    for name, schema in sorted(schemas.items()):
        schema.setdefault("description", humanize(name))
        for key, prop in (schema.get("properties") or {}).items():
            if isinstance(prop, dict) and "$ref" not in prop:
                prop.setdefault("description", humanize(key))
    simplify_schemas(spec["paths"])
    simplify_schemas(spec["components"])


def add_security(spec, app):
    """Declare the two demo-session headers as apiKey schemes and apply them per operation, read from the app's own dependencies."""
    def called(dependant):
        names = set()
        for sub in dependant.dependencies:
            names.add(getattr(sub.call, "__name__", ""))
            names |= called(sub)
        return names
    needs = {}
    for route in app.routes:
        if hasattr(route, "dependant"):
            for method in route.methods:
                needs[(method, route.path)] = called(route.dependant)
    spec["components"]["securitySchemes"] = {
        "DemoSession": {"type": "apiKey", "in": "header", "name": "X-Demo-Session",
                        "description": "Demo session id. Get it from the session_id field of the response to POST /api/v1/demo/sessions "
                                       "(that request needs no header). Without it the API answers 401 session_required."},
        "DemoCsrf": {"type": "apiKey", "in": "header", "name": "X-CSRF-Token",
                     "description": "CSRF token for the same session. Get it from the csrf_token field of the response to POST /api/v1/demo/sessions. "
                                    "Every POST also needs it; without it the API answers 403 csrf_rejected."}}
    spec["info"]["description"] += (" Authentication: create a session with POST /api/v1/demo/sessions, then send X-Demo-Session on every other "
                                    "call and X-CSRF-Token on every POST. POST calls also need an Origin header equal to the console's own origin "
                                    "(browsers add it; scripts must set it), otherwise the API answers 403 origin_required.")
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            deps = needs.get((method.upper(), path), set())
            if "write_session" in deps:
                operation["security"] = [{"DemoSession": [], "DemoCsrf": []}]
                codes = {"403": "Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected)."}
            elif "read_session" in deps:
                operation["security"] = [{"DemoSession": []}]
                codes = {}
            else:
                operation["security"] = []
                codes = {}
            for code, message in codes.items():
                operation["responses"].setdefault(code, {"description": message, "content": {JSON: {"schema": {"$ref": "#/components/schemas/ErrorBody"}}}})


# ---- Generated examples: filled only where no hand-written example exists, built from each schema's own constraints. ----
_STRING_CANDIDATES = ("example", "case-ref-001", "PP-R-BNP-XXXX7173", "EXAMPLE", "example-0001", "2026-10-07T09:30:00Z", "2026-10-07", "42.50", "1", "USD", "US",
                      "A", "AB1234", "Example-1", "example one", "ABC123")
_UNBUILDABLE = []  # (schema path) entries where no valid example could be built; read by the test and the report


def _resolve(schemas, node):
    while isinstance(node, dict) and "$ref" in node:
        node = schemas[node["$ref"].rsplit("/", 1)[-1]]
    return node


def _string_example(node):
    if "enum" in node:
        return node["enum"][0]
    if "const" in node:
        return node["const"]
    formats = {"date-time": "2026-10-07T09:30:00Z", "date": "2026-10-07", "uri": "https://example.com/", "uuid": "00000000-0000-4000-8000-000000000001"}
    if "format" in node:
        if node["format"] not in formats:
            raise ValueError("unsupported format")
        return formats[node["format"]]
    low, high = node.get("minLength", 0), node.get("maxLength")
    pattern = re.compile(node["pattern"]) if "pattern" in node else None
    for candidate in _STRING_CANDIDATES:
        text = candidate
        if len(text) < low:
            text = (text + "x" * low)[:max(low, 1)]
        if high is not None and len(text) > high:
            text = text[:high]
        if len(text) < low or (pattern is not None and pattern.search(text) is None):
            continue
        if re.search(r"[0-9a-fA-F]{32,}", text):
            continue
        return text
    raise ValueError("no string example")


def build_example(schemas, node, depth=0):
    """A minimal valid value for a JSON schema: required fields only, first enum value, no emails, no long hex. Raises ValueError if none can be built."""
    if depth > 6:
        raise ValueError("too deep")
    node = _resolve(schemas, node)
    if not isinstance(node, dict) or not node:
        raise ValueError("no schema")
    if "const" in node:
        return node["const"]
    if "enum" in node:
        return node["enum"][0]
    for key in ("allOf", "oneOf", "anyOf"):
        if key in node:
            options = [_resolve(schemas, option) for option in node[key]]
            for option in options:
                if option.get("type") != "null":
                    try:
                        return build_example(schemas, option, depth + 1)
                    except ValueError:
                        if not any(o.get("type") == "null" for o in options):
                            raise
            if any(o.get("type") == "null" for o in options):
                return None
    kind = node.get("type")
    if isinstance(kind, list):
        kind = next((k for k in kind if k != "null"), None)
    if kind == "string":
        return _string_example(node)
    if kind == "boolean":
        return False
    if kind in ("integer", "number"):
        value = node.get("minimum", 1 if kind == "integer" else 0.5)
        if "maximum" in node and value > node["maximum"]:
            value = node["maximum"]
        return int(value) if kind == "integer" else value
    if kind == "array":
        count = max(node.get("minItems", 0), 1) if "items" in node else node.get("minItems", 0)
        count = min(count, node.get("maxItems", count))
        return [build_example(schemas, node["items"], depth + 1) for _ in range(count)]
    if kind == "object" or "properties" in node:
        return {name: build_example(schemas, node["properties"][name], depth + 1) for name in node.get("required", [])}
    raise ValueError("unsupported schema")


def _structured_errors(spec):
    from app.main import _MESSAGES
    return {"401": {"error": {"code": "session_required", "message": _MESSAGES[401]}},
            "403": {"error": {"code": "csrf_rejected", "message": _MESSAGES[403]}},
            "429": {"error": {"code": "rate_limited", "message": _MESSAGES[429]}}}


def fill_details(spec):
    """Request-body descriptions, parameter examples and media-type examples for everything the hand-written EXAMPLES left open."""
    schemas = spec["components"]["schemas"]
    errors = _structured_errors(spec)
    del _UNBUILDABLE[:]
    for path, methods in sorted(spec["paths"].items()):
        for method, operation in sorted(methods.items()):
            label = "%s %s" % (method.upper(), path)
            body = operation.get("requestBody")
            if body is not None:
                body.setdefault("description", "JSON body for: %s." % operation["summary"].rstrip("."))
                body.setdefault("required", True)
                for media in body["content"].values():
                    if "example" not in media and "examples" not in media:
                        try:
                            media["example"] = build_example(schemas, media.get("schema", {}))
                        except ValueError:
                            _UNBUILDABLE.append(label + " request")
            for parameter in operation.get("parameters", []):
                if "example" not in parameter:
                    if parameter.get("name") == "case_ref":
                        parameter["example"] = "case-ref-001"
                    else:
                        try:
                            parameter["example"] = build_example(schemas, parameter.get("schema", {}))
                        except ValueError:
                            _UNBUILDABLE.append(label + " parameter " + str(parameter.get("name")))
            for code, response in sorted(operation.get("responses", {}).items()):
                for media in response.get("content", {}).values():
                    if "example" in media or "examples" in media:
                        continue
                    if code in errors:
                        media["example"] = copy.deepcopy(errors[code])
                        continue
                    try:
                        media["example"] = build_example(schemas, media.get("schema", {}))
                    except ValueError:
                        _UNBUILDABLE.append("%s response %s" % (label, code))


SESSION_PATH = "/api/v1/demo/sessions"

# Synthetic, privacy-safe examples for the developer portal. Every value is made up: masked codes, no real ids, no emails, no hashes.
# They are written into the media types after describe(), so regeneration is deterministic. Runtime behaviour is untouched.
_MONEY = {"currency_code": "USD", "value": "42.50"}
_DISPUTE_META = {"source": "synthetic_fixture", "data_source_label": "Fixture", "environment": "sandbox", "evidence_class": "SYNTHETIC_FIXTURE",
                 "observed_at": "2026-10-07T09:30:00Z", "provider_submission": "NOT_PERFORMED", "readback": "GET_LIST", "paypal_debug_id": None}
_DISPUTE_RECORD = {"dispute_id": "PP-R-BNP-XXXX7173", "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "status": "WAITING_FOR_SELLER_RESPONSE",
                   "dispute_life_cycle_stage": "INQUIRY", "dispute_amount": _MONEY, "create_time": "2026-10-01T08:00:00Z",
                   "update_time": "2026-10-02T08:00:00Z", "seller_response_due_date": "2026-10-15T08:00:00Z", "dispute_state": "OPEN_INQUIRIES"}
JSON = "application/json"
EXAMPLES = {
    ("GET", "/api/v1/health"): {"200": {"status": "ok", "mode": "demo", "version": "0.0.0-example", "source": "synthetic"}},
    ("GET", "/api/v1/connections"): {"200": {"mode": "hosted_demo", "sandbox_reads": True}},
    ("POST", SESSION_PATH): {"201": {"session_id": "sess-example-0001", "csrf_token": "csrf-example-0001", "source": "synthetic",
                                     "expires_at": "2026-10-07T10:30:00Z"}},
    ("POST", "/api/v1/demo/inject"): {"request": {"scenario": "burst"}},
    ("GET", "/api/v1/paypal/status"): {"200": {"configured": False, "status": "not_configured", "environment": "sandbox",
                                              "last_verified_at": None, "source": "paypal_sandbox", "evidence_receipt": None}},
    ("GET", "/api/v1/paypal/disputes"): {"200": dict(_DISPUTE_META, items=[_DISPUTE_RECORD])},
    ("GET", "/api/v1/paypal/disputes/{dispute_id}"): {"path": {"dispute_id": "PP-R-BNP-XXXX7173"}, "200": dict(
        _DISPUTE_RECORD, source="synthetic_fixture", data_source_label="Fixture", environment="sandbox", evidence_class="SYNTHETIC_FIXTURE",
        observed_at="2026-10-07T09:30:00Z", provider_submission="NOT_PERFORMED", readback="GET_DETAIL", paypal_debug_id=None,
        disputed_transactions=[{"seller_transaction_id": "TXN-EXAMPLE-0001", "gross_amount": _MONEY, "seller_protection_eligible": True,
                                "transaction_status": "COMPLETED"}],
        evidences=[{"evidence_type": "PROOF_OF_FULFILLMENT", "source": "REQUESTED_FROM_SELLER", "action": None, "date": "2026-10-01T08:00:00Z"}])},
    ("POST", "/api/v1/cases/route"): {"request": {"text": "handmade ceramic coffee mug"}},
    ("POST", "/api/v1/country-rules/check"): {"request": {"seller_country": "TW", "buyer_country": "US", "account_type": "business",
                                                          "checkout": "paypal_account", "amount": "120.00", "currency": "USD", "goods_tags": []}},
    ("POST", "/api/v1/policy/assess"): {"request": {"jurisdiction": "US", "theme": "source_compliance", "as_of": "2026-10-07T00:00:00Z",
                                                    "observation_max_age_days": 30}},
    ("POST", "/api/v1/aup/review"): {"request": {"description": "Handmade ceramic coffee mug, shipped in a padded box"}},
    ("POST", "/api/v1/paypal/disputes/provide-evidence"): {"request": {"dispute_id": "PP-R-BNP-XXXX7173", "case_ref": "case-ref-001", "submit": False}},
}


def add_examples(spec):
    """Write the EXAMPLES into the media types, add the hosted 503 refusal, and describe the 422 body the application really returns."""
    from app.demo_mode import DISABLED_ROUTES, HOSTED_DEMO_MESSAGE
    invalid = {"error": {"code": "schema_invalid", "message": "The request does not match the accepted contract."}}
    refused = {"error": {"code": "hosted_demo_disabled", "message": HOSTED_DEMO_MESSAGE}}
    ref = {"$ref": "#/components/schemas/ErrorBody"}
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            key = (method.upper(), path)
            responses = operation.setdefault("responses", {})
            if "422" in responses:  # the application answers its own error body, not FastAPI's default list
                responses["422"] = {"description": "The request does not match the accepted contract (schema_invalid).",
                                    "content": {JSON: {"schema": copy.deepcopy(ref), "example": copy.deepcopy(invalid)}}}
            if key in DISABLED_ROUTES:
                responses["503"] = {"description": "Hosted demo only: this route makes no provider call (hosted_demo_disabled).",
                                    "content": {JSON: {"schema": copy.deepcopy(ref), "example": copy.deepcopy(refused)}}}
            sample = EXAMPLES.get(key, {})
            if "request" in sample:
                operation["requestBody"]["content"][JSON]["example"] = copy.deepcopy(sample["request"])
            for code in ("200", "201"):
                if code in sample:
                    responses[code].setdefault("content", {}).setdefault(JSON, {})["example"] = copy.deepcopy(sample[code])
            for parameter in operation.get("parameters", []):
                if parameter.get("in") == "path" and parameter.get("name") in sample.get("path", {}):
                    parameter["example"] = sample["path"][parameter["name"]]

PATH_SAMPLES = {"case_ref": "case-ref-001", "dispute_id": "PP-D-00000001"}
# Routes that reach PayPal Sandbox or a model when the operator has configured one; the run collection leaves them out.
PROVIDER_PATHS = ("/api/v1/ai/evidence-brief", "/api/v1/studio/agent-turn", "/api/v1/guide/turn", "/api/v1/guide/review",
                  "/api/v1/paypal/connect", "/api/v1/paypal/disputes", "/api/v1/paypal/invoices", "/api/v1/paypal/webhooks")
ALLOWED_CODES = (200, 201, 401, 404, 409, 422, 429, 503)

# One shared pre-request script. It is the only place the two headers the local security boundary needs are added:
# Origin (the base URL's own origin, required on every POST) and the demo session pair that the session request returns.
PRE_REQUEST = [
    "var base = pm.variables.get('baseUrl') || 'http://127.0.0.1:8000';",
    "var origin = (base.match(/^[a-z]+:\\/\\/[^\\/]+/i) || [base])[0];",
    "var isSession = pm.request.method === 'POST' && /\\/api\\/v1\\/demo\\/sessions$/.test(pm.request.url.getPath());",
    "pm.request.headers.upsert({key: 'Origin', value: origin});",
    "var sid = pm.collectionVariables.get('sessionId');",
    "var csrf = pm.collectionVariables.get('csrfToken');",
    "if (!isSession && sid) { pm.request.headers.upsert({key: 'X-Demo-Session', value: sid}); }",
    "if (!isSession && csrf && pm.request.method !== 'GET') { pm.request.headers.upsert({key: 'X-CSRF-Token', value: csrf}); }",
]
SCHEMA_URL = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"


def js(value):
    return json.dumps(value, ensure_ascii=False)


def session_test():
    return ["pm.test('session created (201, synthetic)', function () {",
            "  pm.response.to.have.status(201);",
            "  var j = pm.response.json();",
            "  pm.expect(j.source).to.eql('synthetic');",
            "  pm.expect(j.session_id).to.be.a('string').and.not.empty;",
            "  pm.expect(j.csrf_token).to.be.a('string').and.not.empty;",
            "  pm.collectionVariables.set('sessionId', j.session_id);",
            "  pm.collectionVariables.set('csrfToken', j.csrf_token);",
            "});"]


def status_test(code, label=None):
    lines = ["pm.test(%s, function () { pm.response.to.have.status(%d); });" % (js(label or "status is %d" % code), code),
             "pm.test('body is JSON', function () { pm.response.json(); });"]
    return lines


def value_tests(checks):
    """checks: list of (dotted path, expected value); each becomes one assertion on the parsed JSON body."""
    lines = []
    for path, expected in checks:
        access = "".join("[%s]" % js(part) for part in path.split("."))
        lines.append("pm.test(%s, function () { pm.expect(pm.response.json()%s).to.eql(%s); });" % (js("%s is %s" % (path, js(expected))), access, js(expected)))
    return lines


def capture_lines(captures):
    return ["pm.collectionVariables.set(%s, pm.response.json()[%s]);" % (js(var), js(key)) for var, key in sorted(captures.items())]


def event(kind, lines):
    return {"listen": kind, "script": {"type": "text/javascript", "exec": list(lines)}}


def url_for(path, variables=None):
    parts = [part for part in path.split("/") if part]
    segments = [":" + part[1:-1] if part.startswith("{") else part for part in parts]
    url = {"raw": "{{baseUrl}}/" + "/".join(segments), "host": ["{{baseUrl}}"], "path": segments}
    names = [part[1:-1] for part in parts if part.startswith("{")]
    if names:
        url["variable"] = [{"key": name, "value": (variables or PATH_SAMPLES).get(name, "sample")} for name in names]
    return url


def request_for(method, path, description, body=None):
    request = {"method": method.upper(), "header": [{"key": "Content-Type", "value": "application/json"}],
               "url": url_for(path), "description": description}
    if body is not None:
        request["body"] = {"mode": "raw", "raw": body if isinstance(body, str) else json.dumps(body, indent=2, ensure_ascii=False),
                           "options": {"raw": {"language": "json"}}}
    return request


# The run collection: every request is safe in the default local demo mode (no PayPal key, no model key, no network
# beyond loopback). `expect` is the status the app answers; `negative` marks a deliberate refusal; `captures` stores a
# response field in a collection variable for later bodies; `checks` are (dotted path, value) assertions on the JSON.
_POLICY = {"jurisdiction": "US", "theme": "source_compliance", "as_of": "2026-10-07T00:00:00Z", "observation_max_age_days": 30}
_CANDIDATE = {"schema_version": 1, "jurisdiction": "US", "theme": "source_compliance", "as_of": "2026-10-07T00:00:00Z",
              "status": "manual_review", "advisory_only": True, "operational_authority": "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
              "claims": [{"claim_id": "CLAIM_1", "claim_type": "policy_reference", "text": "The seller cites the pinned acceptable-use page.",
                          "citation_chunk_ids": ["PP-US-AUP-POLICY"]}]}
_MUG = "Handmade ceramic coffee mug, shipped in a padded box"
RUN_REQUESTS = [
    {"name": "01 Create demo session", "method": "POST", "path": SESSION_PATH, "body": {}, "expect": 201, "session": True,
     "note": "Starts a synthetic demo session; its id and CSRF token are stored in collection variables for every later request."},
    {"name": "02 Health", "method": "GET", "path": "/api/v1/health", "expect": 200,
     "checks": [("status", "ok"), ("source", "synthetic")], "note": "Liveness check; the only route that needs no session."},
    {"name": "03 Connections", "method": "GET", "path": "/api/v1/connections", "expect": 200, "checks": [("mode", "local")],
     "note": "Deployment mode only; no key, no key presence."},
    {"name": "04 Demo state", "method": "GET", "path": "/api/v1/demo/state", "expect": 200, "checks": [("source", "synthetic")],
     "note": "The session's synthetic transactions and velocity result."},
    {"name": "05 Inject burst scenario", "method": "POST", "path": "/api/v1/demo/inject", "body": {"scenario": "burst"}, "expect": 200,
     "checks": [("source", "synthetic")], "note": "Loads the synthetic burst of small payments into this session."},
    {"name": "06 Inject unknown scenario (negative case)", "method": "POST", "path": "/api/v1/demo/inject", "body": {"scenario": "bogus"},
     "expect": 422, "negative": True, "checks": [("error.code", "schema_invalid")],
     "note": "Negative case: a scenario outside burst, dispute, reset is refused with 422 schema_invalid."},
    {"name": "07 Country rules: countries", "method": "GET", "path": "/api/v1/country-rules/countries", "expect": 200,
     "checks": [("schema_version", "payguard.country_rules.v1")], "note": "The ten supported countries and the goods tags."},
    {"name": "08 Country rules: check TW seller to US buyer", "method": "POST", "path": "/api/v1/country-rules/check",
     "body": {"seller_country": "TW", "buyer_country": "US", "account_type": "business", "checkout": "paypal_account",
              "amount": "120.00", "currency": "USD", "goods_tags": []},
     "expect": 200, "checks": [("blocked", False), ("cross_border", True)], "note": "A passing cross-border check with no restricted goods."},
    {"name": "09 Country rules: unknown country (negative case)", "method": "POST", "path": "/api/v1/country-rules/check",
     "body": {"seller_country": "XX", "buyer_country": "US"}, "expect": 422, "negative": True, "checks": [("error.code", "schema_invalid")],
     "note": "Negative case: a country code outside the ten is refused with 422."},
    {"name": "10 Country rules: search", "method": "POST", "path": "/api/v1/country-rules/search", "body": {"query": "hold", "limit": 3},
     "expect": 200, "checks": [("schema_version", "payguard.country_rules.v1")], "note": "Clause search over the country rules pack."},
    {"name": "11 Acceptable-use review", "method": "POST", "path": "/api/v1/aup/review", "body": {"description": _MUG}, "expect": 200,
     "captures": {"evaluationId": "evaluation_id", "descriptionDigest": "description_digest"},
     "checks": [("match_status", "NO_MATCH"), ("compliance_decision", "NOT_MADE")],
     "note": "Keyword check of a synthetic product description; stores evaluation_id and description_digest for the next two requests."},
    {"name": "12 Acceptable-use category signal", "method": "POST", "path": "/api/v1/aup/category-signal",
     "body": {"evaluation_id": "{{evaluationId}}", "description": _MUG}, "expect": 200,
     "checks": [("status", "OFF"), ("affects_decision", False)], "note": "The optional category lookup is off in the default mode."},
    {"name": "13 Acceptable-use acknowledge", "method": "POST", "path": "/api/v1/aup/acknowledge",
     "body": {"evaluation_id": "{{evaluationId}}", "description_digest": "{{descriptionDigest}}", "choice": "RETURN_TO_EDIT"},
     "expect": 200, "checks": [("choice", "RETURN_TO_EDIT"), ("external_action_authorized", False)],
     "note": "Records the seller's choice for the review above."},
    {"name": "14 Acceptable-use empty description (negative case)", "method": "POST", "path": "/api/v1/aup/review",
     "body": {"description": ""}, "expect": 422, "negative": True, "checks": [("error.code", "schema_invalid")],
     "note": "Negative case: an empty description is refused with 422."},
    {"name": "15 Case route: digital goods", "method": "POST", "path": "/api/v1/cases/route", "body": {"text": "online course"},
     "expect": 200, "checks": [("route", "digital"), ("decided_by", "code")], "note": "Which evidence list applies to this kind of goods."},
    {"name": "16 Policy assess", "method": "POST", "path": "/api/v1/policy/assess", "body": _POLICY, "expect": 200,
     "checks": [("current_policy_applicability", "NOT_ESTABLISHED"), ("advisory_only", True)],
     "note": "Offline applicability summary over the pinned references; no model."},
    {"name": "17 Advisory evaluate", "method": "POST", "path": "/api/v1/advisory/evaluate",
     "body": dict(_POLICY, candidate_json=json.dumps(_CANDIDATE)), "expect": 200,
     "checks": [("model_generation", "NOT_RUN"), ("semantic_entailment", "NOT_EVALUATED")],
     "note": "Offline structural gate over a candidate advisory; candidate_json is a JSON string."},
    {"name": "18 References search", "method": "POST", "path": "/api/v1/references/search",
     "body": {"query": "proof of delivery tracking", "theme": "dispute_mediation", "jurisdiction": "US"}, "expect": 200,
     "checks": [("status", "references_found")], "note": "Search over the pinned official references."},
    {"name": "19 Guide state", "method": "GET", "path": "/api/v1/guide/state", "expect": 200, "checks": [("started", False)],
     "note": "The evidence guide before it is started."},
    {"name": "20 Guide start", "method": "POST", "path": "/api/v1/guide/start", "body": {"scenario": "dispute", "goods_type": "physical"},
     "expect": 200, "checks": [("started", True), ("scenario", "dispute")], "note": "Starts the dispute evidence guide for physical goods."},
    {"name": "21 Guide form: ship date", "method": "POST", "path": "/api/v1/guide/form",
     "body": {"scenario": "dispute", "item": "ship_date", "value": "2026-10-01"}, "expect": 200, "checks": [("started", True)],
     "note": "Fills one closed form item; no model."},
    {"name": "22 PayPal status", "method": "GET", "path": "/api/v1/paypal/status", "expect": 200, "checks": [("configured", False)],
     "note": "Reads the adapter state only; with no Sandbox keys it answers not_configured and makes no PayPal call."},
    {"name": "23 AI usage", "method": "GET", "path": "/api/v1/ai/usage", "expect": 200, "checks": [("content_logged", False)],
     "note": "This session's AI audit log; empty because no model call was made."},
    {"name": "24 Studio agent status", "method": "GET", "path": "/api/v1/studio/agent-status", "expect": 200,
     "checks": [("built_in_agents", "off")], "note": "Built-in agents are off unless a model is configured."},
    {"name": "25 Reset demo", "method": "POST", "path": "/api/v1/demo/inject", "body": {"scenario": "reset"}, "expect": 200,
     "checks": [("source", "synthetic")], "note": "Clears this session's demo state and guide answers."},
]


def run_item(spec):
    description = spec["note"] + (" Expected status %d." % spec["expect"])
    request = request_for(spec["method"], spec["path"], description, spec.get("body"))
    if spec.get("session"):
        test = session_test()
    else:
        label = "negative case: status is %d" % spec["expect"] if spec.get("negative") else None
        test = status_test(spec["expect"], label) + value_tests(spec.get("checks", [])) + capture_lines(spec.get("captures", {}))
    return {"name": spec["name"], "request": request, "event": [event("test", test)]}


def full_item(path, method, operation):
    description = operation.get("description") or ""
    if path.startswith(PROVIDER_PATHS):
        description += " This route can reach PayPal Sandbox or a model when the operator has configured one; it is not in postman_run_collection.json."
    body = "{}" if method.lower() in ("post", "put", "patch") else None
    code_list = ", ".join(str(code) for code in ALLOWED_CODES)
    test = ["var allowed = [%s];" % code_list,
            "pm.test('status is a documented answer (200, 201, 401, 404, 409, 422, 429 or 503)', function () { pm.expect(pm.response.code).to.be.oneOf(allowed); });",
            "pm.test('body is JSON', function () { pm.response.json(); });"]
    if path == SESSION_PATH:
        test = session_test()
    return {"name": "%s %s" % (method.upper(), path), "request": request_for(method, path, description, body), "event": [event("test", test)]}


def collection(name, description, items):
    return {"info": {"name": name, "schema": SCHEMA_URL, "description": description},
            "event": [event("prerequest", PRE_REQUEST)],
            "variable": [{"key": "baseUrl", "value": "http://127.0.0.1:8000"}], "item": items}


def build():
    try:
        from app.main import app
    except Exception as exc:  # fail loudly, never write a partial file
        print("ERROR cannot import the application: %s" % type(exc).__name__, file=sys.stderr)
        sys.exit(2)
    spec = copy.deepcopy(app.openapi())  # the application caches its schema; never edit the cached one
    spec["info"]["description"] = ("API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo "
                                   "session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal.")
    describe(spec)
    add_examples(spec)
    add_security(spec, app)
    fill_details(spec)
    items = [full_item(path, method, operation) for path in sorted(spec["paths"]) for method, operation in sorted(spec["paths"][path].items())]
    items.sort(key=lambda item: item["name"] != "POST " + SESSION_PATH)  # stable: the session request first, the rest in path order
    usage = ("A collection-level pre-request script adds the Origin header and the X-Demo-Session / X-CSRF-Token headers; the first "
             "request creates the session and stores both values. Run it in order. ")
    full = collection("TradeGlot local console API", "Generated from docs/api/openapi.json by tools/export_api_docs.py. Local console only. " + usage +
                      "Bodies are empty skeletons, so most write routes answer a documented 422; for requests with real bodies use postman_run_collection.json.", items)
    run = collection("TradeGlot local console API - run collection",
                     "25 requests that are safe in the default local demo mode (no PayPal key, no model key, no outside network). " + usage +
                     "Requests marked negative case are deliberate refusals and are expected to answer 4xx. "
                     "Run: newman run postman_run_collection.json --env-var baseUrl=http://127.0.0.1:8000",
                     [run_item(spec_item) for spec_item in RUN_REQUESTS])
    return {"openapi.json": spec, "postman_collection.json": full, "postman_run_collection.json": run}


def main(argv):
    files = {name: json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False) + "\n" for name, value in build().items()}
    if "--check" in argv:
        stale = [name for name, text in files.items() if not (OUT / name).is_file() or (OUT / name).read_text(encoding="utf-8") != text]
        print("STALE " + ", ".join(stale) if stale else "OK docs/api is up to date")
        return 1 if stale else 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote docs/api/%s (%d bytes)" % (name, len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
