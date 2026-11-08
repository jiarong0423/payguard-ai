import ast
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from payguard import mcp_server  # noqa: E402

SOURCE = (ROOT / "src" / "payguard" / "mcp_server.py").read_text(encoding="utf-8")
EXPECTED_TOOLS = ["check_acceptable_use", "list_countries", "check_country_rules", "search_rule_clauses", "check_sales_spike"]
FORBIDDEN_WORDS = ("send", "submit", "connect", "approve", "write", "delete", "create", "update", "token", "paypal", "evidence_request")


def call(name, arguments=None, request_id=7):
    return mcp_server.handle_message({"jsonrpc": "2.0", "id": request_id, "method": "tools/call",
                                      "params": {"name": name, "arguments": arguments if arguments is not None else {}}})


class ProtocolTests(unittest.TestCase):
    def test_initialize_negotiates_a_supported_version(self):
        for asked in mcp_server.SUPPORTED_PROTOCOLS:
            reply = mcp_server.handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": asked}})
            self.assertEqual(reply["result"]["protocolVersion"], asked)
        reply = mcp_server.handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "1999-01-01"}})
        self.assertEqual(reply["result"]["protocolVersion"], mcp_server.SUPPORTED_PROTOCOLS[0])
        self.assertEqual(reply["result"]["capabilities"], {"tools": {"listChanged": False}})
        self.assertEqual(reply["result"]["serverInfo"]["name"], "tradeglot")
        self.assertIn("read-only", reply["result"]["instructions"])

    def test_notifications_get_no_answer(self):
        self.assertIsNone(mcp_server.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        self.assertIsNone(mcp_server.handle_message({"jsonrpc": "2.0", "method": "notifications/cancelled", "params": {}}))

    def test_ping_unknown_method_and_bad_requests(self):
        self.assertEqual(mcp_server.handle_message({"jsonrpc": "2.0", "id": 3, "method": "ping"})["result"], {})
        self.assertEqual(mcp_server.handle_message({"jsonrpc": "2.0", "id": 4, "method": "resources/list"})["error"]["code"], -32601)
        self.assertEqual(mcp_server.handle_message({"id": 5, "method": "ping"})["error"]["code"], -32600)
        self.assertEqual(mcp_server.handle_message("nope")["error"]["code"], -32600)

    def test_stdio_framing_parse_errors_and_batches(self):
        lines = io.StringIO('not json\n[{"jsonrpc":"2.0","id":1,"method":"ping"}]\n\n{"jsonrpc":"2.0","id":2,"method":"ping"}\n')
        out = io.StringIO()
        mcp_server.serve(lines, out)
        replies = [json.loads(line) for line in out.getvalue().splitlines()]
        self.assertEqual([r.get("error", {}).get("code") for r in replies[:2]], [-32700, -32600])
        self.assertEqual(replies[2], {"jsonrpc": "2.0", "id": 2, "result": {}})

    def test_oversize_line_is_refused(self):
        out = io.StringIO()
        mcp_server.serve(io.StringIO("x" * (mcp_server.MAX_LINE_BYTES + 10) + "\n"), out)
        self.assertEqual(json.loads(out.getvalue())["error"]["code"], -32600)

    def test_real_process_over_a_pipe(self):
        requests = "\n".join(json.dumps(m) for m in (
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})) + "\n"
        run = subprocess.run([sys.executable, "-B", "-m", "payguard.mcp_server"], input=requests, capture_output=True, text=True,
                             cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"}, timeout=60, check=False)
        self.assertEqual(run.returncode, 0, run.stderr[-300:])
        replies = [json.loads(line) for line in run.stdout.splitlines()]
        self.assertEqual([r["id"] for r in replies], [1, 2])
        self.assertEqual([t["name"] for t in replies[1]["result"]["tools"]], EXPECTED_TOOLS)


class ToolSetTests(unittest.TestCase):
    def test_exactly_the_five_read_only_tools(self):
        reply = mcp_server.handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        tools = reply["result"]["tools"]
        self.assertEqual([t["name"] for t in tools], EXPECTED_TOOLS)
        for tool in tools:
            self.assertEqual(tool["annotations"], {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False})
            self.assertEqual(tool["inputSchema"]["type"], "object")
            self.assertIs(tool["inputSchema"]["additionalProperties"], False)
            haystack = (tool["name"] + " " + tool["description"]).lower()
            for word in FORBIDDEN_WORDS:
                self.assertNotIn(word, tool["name"].lower(), f"{tool['name']} must not suggest {word}")
            self.assertNotIn("sends ", haystack)

    def test_the_module_cannot_reach_out(self):
        tree = ast.parse(SOURCE)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                imported.add((node.module or "").split(".")[0])
        self.assertTrue(imported <= {"__future__", "json", "sys"}, imported)
        for banned in ("open(", "os.environ", "getenv", "socket", "urllib", "requests", "httpx", "subprocess", "eval(", "exec("):
            self.assertNotIn(banned, SOURCE)


class ToolCallTests(unittest.TestCase):
    def payload(self, reply):
        self.assertFalse(reply["result"]["isError"], reply)
        self.assertEqual(json.loads(reply["result"]["content"][0]["text"]), reply["result"]["structuredContent"])
        return reply["result"]["structuredContent"]

    def test_acceptable_use_is_a_signal_not_a_decision(self):
        flagged = self.payload(call("check_acceptable_use", {"description": "Disposable vape e-cigarette liquid"}))
        self.assertEqual((flagged["match_status"], flagged["compliance_decision"], flagged["advisory_only"]), ("REVIEW_SIGNAL", "NOT_MADE", True))
        clear = self.payload(call("check_acceptable_use", {"description": "Ceramic coffee cup"}))
        self.assertEqual(clear["match_status"], "NO_MATCH")
        self.assertEqual(clear["compliance_decision"], "NOT_MADE")

    def test_countries_and_rules(self):
        countries = self.payload(call("list_countries"))["countries"]
        self.assertEqual(len(countries), 10)
        result = self.payload(call("check_country_rules", {"seller_country": "US", "buyer_country": "SG", "goods_tags": ["e_cigarettes"]}))
        self.assertTrue(result["blocked"])
        self.assertIs(result["advisory_only"], True)
        self.assertIs(result["legal_advice"], False)
        self.assertEqual(result["findings"][0]["severity"], "BLOCK")
        self.assertTrue(all("text" in f for f in result["findings"]))

    def test_clause_search(self):
        found = self.payload(call("search_rule_clauses", {"query": "seller protection address", "limit": 3}))["results"]
        self.assertTrue(1 <= len(found) <= 3)

    def test_sales_spike_uses_the_callers_declared_baseline(self):
        arguments = {"transactions": [{"order_id": "o1", "amount": "400.00", "currency": "USD", "occurred_at": "2026-11-08T10:30:00Z"}],
                     "baseline_amount_per_hour": "100.00", "as_of": "2026-11-08T11:00:00Z",
                     "baseline_window_start": "2026-11-07T09:00:00Z", "baseline_window_end": "2026-11-08T09:00:00Z"}
        result = self.payload(call("check_sales_spike", arguments))
        self.assertEqual(result["status"], "review_velocity")
        self.assertEqual(result["baseline_provenance"], "CALLER_SUPPLIED_UNVERIFIED")
        quiet = dict(arguments, transactions=[{"order_id": "o1", "amount": "50.00", "currency": "USD", "occurred_at": "2026-11-08T10:30:00Z"}])
        self.assertEqual(self.payload(call("check_sales_spike", quiet))["status"], "normal")

    def test_bad_input_is_a_tool_error_not_a_crash(self):
        for name, arguments in (("check_acceptable_use", {"description": ""}), ("check_acceptable_use", {}),
                                ("check_acceptable_use", {"description": "x", "extra": 1}),
                                ("check_country_rules", {"seller_country": "US", "buyer_country": "ZZ"}),
                                ("check_country_rules", {"seller_country": "US", "buyer_country": "SG", "goods_tags": ["not_a_tag"]}),
                                ("search_rule_clauses", {"query": "x" * 500}), ("list_countries", {"unexpected": True}),
                                ("check_sales_spike", {"transactions": "no"})):
            reply = call(name, arguments)
            self.assertTrue(reply["result"]["isError"], (name, arguments))
            self.assertNotIn("Traceback", reply["result"]["content"][0]["text"])

    def test_unknown_and_send_style_tools_do_not_exist(self):
        for name in ("send_evidence", "provide_evidence", "connect_paypal", "approve", "submit", "create_invoice"):
            self.assertEqual(call(name)["error"]["code"], -32602, name)


if __name__ == "__main__":
    unittest.main()
