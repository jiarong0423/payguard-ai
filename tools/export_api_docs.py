#!/usr/bin/env python3
"""Write the local console's API description: an OpenAPI 3.1 file and a Postman collection made from it.

Reads the FastAPI application in-process (no server, no network, no key). Output is deterministic: running it twice
gives the same bytes, and `--check` fails when the committed files are out of date.

Usage: PYTHONPATH=src:backend python3 -B tools/export_api_docs.py [--check]
Writes docs/api/openapi.json, docs/api/postman_collection.json and docs/api/postman_run_collection.json. Exit 0 ok, 1 stale with --check, 2 import failure.
"""
import copy
import json
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


SESSION_PATH = "/api/v1/demo/sessions"
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
