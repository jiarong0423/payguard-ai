# mcp-server

Source: http://localhost:3000/#/ruby/x-redirect/cGFnZSUzQWd1aWRlcyUyRm1jcC1zZXJ2ZXI

The repository ships a small read-only MCP server, `src/payguard/mcp_server.py`, built on the Python standard library. It speaks newline-delimited JSON-RPC 2.0 over stdio.


# Five tools, all read-only

| Tool | Returns |
| --- | --- |
| `check_acceptable_use` | A review signal for a product description. |
| `list_countries` | The ten countries in the rules pack. |
| `check_country_rules` | Findings for a seller and buyer country, most severe first, each with its source. |
| `search_rule_clauses` | The best matches among 140 paraphrased PayPal clauses. |
| `check_sales_spike` | A comparison with a baseline you declare; the answer says the baseline is unverified. |

There is no tool that sends evidence, connects to PayPal, approves or changes anything.


# Run it

```bash
PYTHONPATH=src python3 -B -m payguard.mcp_server
```



