# PayPal's official MCP server, one read-only Sandbox run, 2026-11-09

One run of PayPal's own MCP server (npm package `@paypal/mcp`, server name "PayPal", version 1.11.0) against the author's PayPal Sandbox, with only the two read-only dispute tools switched on (`--tools=disputes.list,disputes.get`). It was started on the author's computer by a small script that gets a Sandbox OAuth token, passes it only to the server process, and calls the tools through the official MCP Python client. The Sandbox keys were typed hidden by the author; they and the token are not printed or stored.

## Result
| Step | Result |
| --- | --- |
| tools offered by the server (with only the two read-only tools enabled) | `list_disputes`, `get_dispute` |
| `list_disputes` | no error; 8 author-created Sandbox test disputes in the reply |
| `get_dispute` for one of them | no error; the detail reply came back |

The receipt is `docs/evidence/official_paypal_mcp_receipt_20261109.json`: tool names, error flags, how many disputes the list held, masked dispute ids and the length and SHA-256 of each reply. The reply bodies are not kept because they contain Sandbox transaction and payer ids.

## What this does and does not show
- It shows TradeGlot's author could connect PayPal's official MCP server to the Sandbox and read disputes through it, read-only.
- It does not put PayPal's MCP server into the product path: the console still reads disputes through its own PayPal Sandbox adapter. TradeGlot's own MCP server (rules checks for AI agents) is a separate, read-only server.
- No write tool (create, send, accept) was enabled or called. One run is one run; nothing here is a benchmark.
- How to repeat it: `npm install @paypal/mcp`, then `PAYPAL_CLIENT_ID=... PAYPAL_CLIENT_SECRET=... python3 -B tools/official_paypal_mcp_readonly_run.py` (needs your own Sandbox keys and the `mcp` Python package); it writes a receipt next to where you run it.
