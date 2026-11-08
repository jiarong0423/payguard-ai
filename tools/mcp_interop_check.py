#!/usr/bin/env python3
"""Check the TradeGlot MCP server with the official MCP Python SDK client over stdio.

Needs the `mcp` package (not in requirements.lock; install it in any separate Python, for example
`python3 -m pip install mcp`). It starts the server as a child process, initialises, lists the tools and calls each one.
No network, no key, nothing is written. Exit 0 when every check passes, 1 on a failed check, 2 when `mcp` is missing.

Usage: python3 -B tools/mcp_interop_check.py
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("SKIP the `mcp` package is not installed in this Python (pip install mcp)", file=sys.stderr)
    sys.exit(2)

EXPECTED = ["check_acceptable_use", "list_countries", "check_country_rules", "search_rule_clauses", "check_sales_spike"]
FAILED = []


def check(label, condition):
    print(("PASS  " if condition else "FAIL  ") + label)
    if not condition:
        FAILED.append(label)


async def main():
    server = StdioServerParameters(command=sys.executable, args=["-B", "-m", "payguard.mcp_server"],
                                   env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"}, cwd=str(ROOT))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            check("initialize: server tradeglot", init.serverInfo.name == "tradeglot")
            tools = (await session.list_tools()).tools
            check("tools/list: the five tools", [t.name for t in tools] == EXPECTED)
            check("every tool is annotated read-only", all(t.annotations and t.annotations.readOnlyHint for t in tools))
            result = await session.call_tool("check_country_rules", {"seller_country": "US", "buyer_country": "SG", "goods_tags": ["e_cigarettes"]})
            check("check_country_rules: US to SG e-cigarettes is blocked, with findings", not result.isError and result.structuredContent["blocked"] and result.structuredContent["findings"])
            result = await session.call_tool("check_acceptable_use", {"description": "Disposable vape e-cigarette liquid"})
            check("check_acceptable_use: a review signal, decision not made", result.structuredContent["match_status"] == "REVIEW_SIGNAL" and result.structuredContent["compliance_decision"] == "NOT_MADE")
            result = await session.call_tool("list_countries", {})
            check("list_countries: ten countries", len(result.structuredContent["countries"]) == 10)
            result = await session.call_tool("search_rule_clauses", {"query": "seller protection address", "limit": 2})
            check("search_rule_clauses: results", 1 <= len(result.structuredContent["results"]) <= 2)
            spike = {"transactions": [{"order_id": "o1", "amount": "400.00", "currency": "USD", "occurred_at": "2026-11-08T10:30:00Z"}],
                     "baseline_amount_per_hour": "100.00", "as_of": "2026-11-08T11:00:00Z",
                     "baseline_window_start": "2026-11-07T09:00:00Z", "baseline_window_end": "2026-11-08T09:00:00Z"}
            result = await session.call_tool("check_sales_spike", spike)
            check("check_sales_spike: review_velocity against the declared baseline", result.structuredContent["status"] == "review_velocity")
            result = await session.call_tool("check_acceptable_use", {"description": ""})
            check("bad input comes back as a tool error", result.isError)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
