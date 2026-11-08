# TradeGlot as a read-only MCP server

An AI agent can call the same rule checks the console uses, through the Model Context Protocol. It is an addition: the web console, the hosted demo and every check stay as they were.

**What it is.** `src/payguard/mcp_server.py`, a standard-library Python module that speaks MCP over stdio (newline-delimited JSON-RPC 2.0; protocol versions 2025-06-18, 2025-03-26 and 2024-11-05). It runs on your computer. It has no network access, no key, and writes nothing.

**What it can do: five tools, all read-only.** Every tool carries the annotations `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false`.

| Tool | What it returns |
| --- | --- |
| `check_acceptable_use` | A review signal for a product description (`REVIEW_SIGNAL` or `NO_MATCH`) and the categories matched. `compliance_decision` is always `NOT_MADE`. |
| `list_countries` | The ten countries in the rules pack. |
| `check_country_rules` | For a seller country and a buyer country (and optional goods tags, account type, checkout): findings most severe first (BLOCK, WARN, INFO), each with its official source. Advisory only; `legal_advice` is false. |
| `search_rule_clauses` | The best matches among the 140 paraphrased PayPal clauses, with their source pages. |
| `check_sales_spike` | Compares recent captured amounts with a baseline *you declare*; the answer says the baseline is unverified. A review signal, never a verdict. |

**What it deliberately does not do.** There is no tool that sends evidence, connects to PayPal, approves, creates or changes anything. `tests/test_mcp_server.py` asserts that the module imports nothing that could reach out (no sockets, HTTP, subprocess, environment or file opening), that no tool name suggests a send or write, and that calls to `send_evidence`, `provide_evidence`, `connect_paypal`, `approve`, `submit` and `create_invoice` answer "Unknown tool". Real PayPal Sandbox sends stay in the local console behind the human approval, as described in the README. This server does not use PayPal's own MCP server or Agent Toolkit.

## Run it

```bash
PYTHONPATH=src python3 -B -m payguard.mcp_server
```

Claude Desktop (`claude_desktop_config.json`) or any client that takes a command and arguments:

```json
{
  "mcpServers": {
    "tradeglot": {
      "command": "python3",
      "args": ["-B", "-m", "payguard.mcp_server"],
      "env": { "PYTHONPATH": "/path/to/tradeglot/src" }
    }
  }
}
```

Claude Code: `claude mcp add tradeglot --env PYTHONPATH=/path/to/tradeglot/src -- python3 -B -m payguard.mcp_server`.

## How it was checked

- **Unit tests:** `tests/test_mcp_server.py`, 14 tests: protocol (version negotiation, notifications, ping, errors, framing, oversize line), the exact five tools and their annotations, the no-reach-out check, each tool's answer, bad input returning a tool error instead of a crash, and a run of the real process over a pipe.
- **With the official client:** `python3 -B tools/mcp_interop_check.py` starts the server as a child process and drives it with the official MCP Python SDK client (`mcp` 1.27.0 on 2026-11-09; the package is not part of `requirements.lock`, install it in a separate Python). It initialises, lists the five tools, calls each one and checks a refused input. All nine checks passed on 2026-11-09.

**Limits.** This is one small server checked with one client library on one machine. It has not been tried with a hosted agent product, and it has no authentication because it never leaves your computer over stdio. The rules pack and its limits are the ones described in the README (681 rules, 44 compared with their sources in the spot-check).
