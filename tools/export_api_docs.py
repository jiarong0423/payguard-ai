#!/usr/bin/env python3
"""Write the local console's API description: an OpenAPI 3.1 file and a Postman collection made from it.

Reads the FastAPI application in-process (no server, no network, no key). Output is deterministic: running it twice
gives the same bytes, and `--check` fails when the committed files are out of date.

Usage: PYTHONPATH=src:backend python3 -B tools/export_api_docs.py [--check]
Writes docs/api/openapi.json and docs/api/postman_collection.json. Exit 0 ok, 1 stale with --check, 2 import failure.
"""
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


def build():
    try:
        from app.main import app
    except Exception as exc:  # fail loudly, never write a partial file
        print("ERROR cannot import the application: %s" % type(exc).__name__, file=sys.stderr)
        sys.exit(2)
    spec = app.openapi()
    spec["info"]["description"] = ("API of the local TradeGlot console (127.0.0.1:8000). It uses synthetic data, expects the demo "
                                   "session headers the console sets, and the hosted demo answers 503 on every route that would reach PayPal.")
    describe(spec)
    items = []
    for path in sorted(spec["paths"]):
        for method, operation in sorted(spec["paths"][path].items()):
            name = operation.get("summary") or ("%s %s" % (method.upper(), path))
            request = {"method": method.upper(), "header": [{"key": "Content-Type", "value": "application/json"}],
                       "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": [part for part in path.split("/") if part]},
                       "description": operation.get("description") or ""}
            if method.lower() in ("post", "put", "patch"):
                request["body"] = {"mode": "raw", "raw": "{}", "options": {"raw": {"language": "json"}}}
            items.append({"name": "%s %s" % (method.upper(), path), "request": request, "_summary": name})
    for item in items:
        item.pop("_summary")
    collection = {"info": {"name": "TradeGlot local console API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                           "description": "Generated from docs/api/openapi.json by tools/export_api_docs.py. Local console only; bodies are empty skeletons."},
                  "variable": [{"key": "baseUrl", "value": "http://127.0.0.1:8000"}], "item": items}
    return {"openapi.json": spec, "postman_collection.json": collection}


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
