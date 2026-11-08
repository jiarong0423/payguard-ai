"""TradeGlot as a read-only MCP server over stdio.

An AI agent can call the rule checks that the console uses: the acceptable-use keyword check, the ten-country rules
check, the clause search and the sales-spike comparison. Every tool only reads and computes. None of them sends,
connects, approves, writes a file or reaches the network; there is no PayPal tool here at all. The answers carry the
same advisory flags as the console (`advisory_only`, `compliance_decision: NOT_MADE`, `legal_advice: false`): the agent
gets rule findings with their sources, never a verdict.

Transport: newline-delimited JSON-RPC 2.0 on stdin and stdout (the MCP stdio transport). Logs go to stderr only.
Run:  PYTHONPATH=src python3 -B -m payguard.mcp_server
This module uses only the standard library and the project's own pure functions.
"""
from __future__ import annotations

import json
import sys

from . import country_rules, engines

SERVER_NAME = "tradeglot"
SERVER_VERSION = "0.1.0"
SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")
MAX_LINE_BYTES = 1_000_000

INSTRUCTIONS = (
    "TradeGlot gives advisory rule findings for small PayPal sellers: acceptable-use keywords, ten-country import and "
    "export rules with their official sources, and a sales-spike comparison against a baseline the caller declares. "
    "Every tool is read-only and computes locally; nothing is sent to PayPal or anywhere else. Results are review "
    "signals, not compliance decisions and not legal advice: a person decides, and PayPal decides every real case."
)

_READ_ONLY = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
_GOODS_TAGS = ["alcohol", "batteries_hazmat", "cosmetics", "counterfeit", "cultural_relics", "currency", "e_cigarettes",
               "food", "general", "jewellery_precious_metals", "live_animals", "medical_devices", "plants_seeds",
               "prescription", "radio_wireless", "tobacco_other", "weapons"]
_COUNTRY = {"type": "string", "pattern": "^[A-Z]{2}$", "description": "Two-letter country code from list_countries."}

TOOLS = [
    {
        "name": "check_acceptable_use",
        "title": "Check a product description against acceptable-use keywords",
        "description": "Flags a seller's product or service description for policy review using TradeGlot's keyword rules. "
                       "Returns a review signal and the categories matched, never a compliance decision.",
        "inputSchema": {"type": "object", "additionalProperties": False, "required": ["description"],
                        "properties": {"description": {"type": "string", "minLength": 1, "maxLength": 4000}}},
    },
    {
        "name": "list_countries",
        "title": "List the countries the rules pack covers",
        "description": "Returns the two-letter codes and names of the ten countries covered by the local rules pack.",
        "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
    },
    {
        "name": "check_country_rules",
        "title": "Check a sale between two countries against the rules pack",
        "description": "Findings for one seller country and buyer country, most severe first: BLOCK (a cited rule stops the "
                       "sale as set up), WARN, INFO. Each finding names its source. Advisory only; not legal advice.",
        "inputSchema": {"type": "object", "additionalProperties": False, "required": ["seller_country", "buyer_country"],
                        "properties": {
                            "seller_country": _COUNTRY,
                            "buyer_country": _COUNTRY,
                            "goods_tags": {"type": "array", "maxItems": 17, "uniqueItems": True,
                                           "items": {"type": "string", "enum": _GOODS_TAGS}},
                            "account_type": {"type": "string", "enum": list(country_rules.ACCOUNT_TYPES)},
                            "checkout": {"type": "string", "enum": list(country_rules.CHECKOUTS)},
                        }},
    },
    {
        "name": "search_rule_clauses",
        "title": "Search the paraphrased PayPal clauses",
        "description": "Searches the 140 paraphrased PayPal legal-hub clauses held in the local rules pack and returns the best "
                       "matches with their source pages.",
        "inputSchema": {"type": "object", "additionalProperties": False, "required": ["query"],
                        "properties": {"query": {"type": "string", "minLength": 1, "maxLength": 200},
                                       "limit": {"type": "integer", "minimum": 1, "maximum": 10}}},
    },
    {
        "name": "check_sales_spike",
        "title": "Compare recent sales with a declared baseline",
        "description": "Compares the captured amount per hour in the last window with a baseline the caller declares and "
                       "returns a review signal when it exceeds the threshold. The baseline is the caller's own unverified "
                       "number; the result says so. Review signal only.",
        "inputSchema": {"type": "object", "additionalProperties": False,
                        "required": ["transactions", "baseline_amount_per_hour", "as_of", "baseline_window_start",
                                     "baseline_window_end"],
                        "properties": {
                            "transactions": {"type": "array", "maxItems": 10000, "items": {
                                "type": "object", "additionalProperties": False,
                                "required": ["order_id", "amount", "currency", "occurred_at"],
                                "properties": {"order_id": {"type": "string"}, "amount": {"type": "string"},
                                               "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
                                               "occurred_at": {"type": "string", "description": "ISO 8601 UTC time"}}}},
                            "baseline_amount_per_hour": {"type": "string"},
                            "as_of": {"type": "string", "description": "ISO 8601 UTC end of the window"},
                            "baseline_window_start": {"type": "string"},
                            "baseline_window_end": {"type": "string"},
                            "window_hours": {"type": "integer", "minimum": 1, "maximum": 168},
                            "threshold": {"type": "string", "description": "Multiple of the baseline, default 3.5"},
                        }},
    },
]
for _tool in TOOLS:
    _tool["annotations"] = dict(_READ_ONLY)


class ToolError(Exception):
    """A tool refused its input; the message is safe to show the caller."""


def _only(arguments, allowed, required=()):
    if not isinstance(arguments, dict):
        raise ToolError("arguments must be an object")
    extra = sorted(set(arguments) - set(allowed))
    if extra:
        raise ToolError("unknown argument: " + ", ".join(extra))
    missing = [key for key in required if key not in arguments]
    if missing:
        raise ToolError("missing argument: " + ", ".join(missing))


def _run(name, arguments):
    try:
        if name == "check_acceptable_use":
            _only(arguments, ("description",), ("description",))
            return engines.check_aup(arguments["description"])
        if name == "list_countries":
            _only(arguments, ())
            return {"countries": country_rules.countries()}
        if name == "check_country_rules":
            _only(arguments, ("seller_country", "buyer_country", "goods_tags", "account_type", "checkout"),
                  ("seller_country", "buyer_country"))
            tags = arguments.get("goods_tags", [])
            if not isinstance(tags, list) or any(tag not in _GOODS_TAGS for tag in tags):
                raise ToolError("goods_tags must be a list of known tags")
            options = {key: arguments[key] for key in ("account_type", "checkout") if key in arguments}
            return country_rules.check(arguments["seller_country"], arguments["buyer_country"],
                                       goods_tags=tuple(tags), **options)
        if name == "search_rule_clauses":
            _only(arguments, ("query", "limit"), ("query",))
            return {"results": country_rules.search(arguments["query"], arguments.get("limit", 5))}
        if name == "check_sales_spike":
            _only(arguments, ("transactions", "baseline_amount_per_hour", "as_of", "baseline_window_start",
                              "baseline_window_end", "window_hours", "threshold"),
                  ("transactions", "baseline_amount_per_hour", "as_of", "baseline_window_start", "baseline_window_end"))
            options = {key: arguments[key] for key in ("window_hours", "threshold") if key in arguments}
            return engines.assess_velocity(arguments["transactions"], arguments["baseline_amount_per_hour"],
                                           arguments["as_of"], baseline_window_start=arguments["baseline_window_start"],
                                           baseline_window_end=arguments["baseline_window_end"], **options)
    except ToolError:
        raise
    except (ValueError, TypeError, KeyError, country_rules.CountryRulesError) as exc:
        raise ToolError("the input was refused: " + (str(exc) or type(exc).__name__)[:300]) from None
    raise KeyError(name)


def _error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle_message(message):
    """One decoded JSON-RPC message in, one response dict out, or None for a notification."""
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
        return _error(None, -32600, "Invalid Request")
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}
    if not isinstance(method, str):
        return None if "result" in message or "error" in message else _error(request_id, -32600, "Invalid Request")
    if "id" not in message:
        return None  # notifications (initialized, cancelled, ...) get no answer
    if method == "initialize":
        asked = params.get("protocolVersion") if isinstance(params, dict) else None
        version = asked if asked in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
        return {"jsonrpc": "2.0", "id": request_id, "result": {
            "protocolVersion": version, "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "title": "TradeGlot rule checks (read-only)", "version": SERVER_VERSION},
            "instructions": INSTRUCTIONS}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name") if isinstance(params, dict) else None
        if name not in {tool["name"] for tool in TOOLS}:
            return _error(request_id, -32602, "Unknown tool")
        try:
            result = _run(name, params.get("arguments") or {})
        except ToolError as exc:
            return {"jsonrpc": "2.0", "id": request_id, "result": {
                "content": [{"type": "text", "text": str(exc)}], "isError": True}}
        text = json.dumps(result, ensure_ascii=False, sort_keys=True)
        return {"jsonrpc": "2.0", "id": request_id, "result": {
            "content": [{"type": "text", "text": text}], "structuredContent": result, "isError": False}}
    return _error(request_id, -32601, "Method not found")


def serve(stdin=None, stdout=None):
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        if len(line.encode("utf-8", "replace")) > MAX_LINE_BYTES:
            response = _error(None, -32600, "Request too large")
        else:
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                response = _error(None, -32700, "Parse error")
            else:
                response = handle_message(message) if not isinstance(message, list) else _error(None, -32600, "Batches are not supported")
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            stdout.flush()
    return 0


def main():
    sys.stderr.write("tradeglot MCP server (read-only) ready on stdio\n")
    return serve()


if __name__ == "__main__":
    raise SystemExit(main())
