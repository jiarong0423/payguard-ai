"""One read-only run of PayPal's OFFICIAL MCP server (@paypal/mcp) against the PayPal Sandbox.

Credentials come from the environment variables PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET (type them hidden in your own terminal). The OAuth token is kept in memory and given only to
the child process; nothing secret is printed or written. Only the two read-only dispute tools are enabled (--tools=disputes.list,disputes.get).
Writes: receipt_official_mcp_<time>.json in the current folder (masked ids, counts, tool names, sha256 of each raw reply)."""
import asyncio, base64, hashlib, json, os, pathlib, re, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
import shutil
# Usage: PAYPAL_CLIENT_ID=... PAYPAL_CLIENT_SECRET=... python3 -B tools/official_paypal_mcp_readonly_run.py [path/to/node_modules/@paypal/mcp/dist/index.js]
# Needs the `mcp` Python package and `npm install @paypal/mcp` in some folder. Sandbox only; read-only tools only.
HERE = pathlib.Path.cwd()
SERVER = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "node_modules" / "@paypal" / "mcp" / "dist" / "index.js"
NODE = shutil.which("node") or "/usr/local/bin/node"

def mask(i):
    m = re.fullmatch(r"(PP-R-[A-Z]{3})-(\d+)", i)
    return f"{m.group(1)}-XXXX{m.group(2)[-4:]}" if m else "PP-R-XXX-XXXX"

def get_token():
    cid, sec = os.environ.get("PAYPAL_CLIENT_ID", ""), os.environ.get("PAYPAL_CLIENT_SECRET", "")
    if not cid or not sec:
        print("ERROR missing Sandbox client id or secret"); sys.exit(2)
    req = urllib.request.Request("https://api-m.sandbox.paypal.com/v1/oauth2/token", data=b"grant_type=client_credentials", method="POST",
        headers={"Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode(), "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]

async def main():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    token = get_token()
    params = StdioServerParameters(command=NODE, args=[str(SERVER), "--tools=disputes.list,disputes.get", "--paypal-environment=SANDBOX"],
        env={"PATH": os.pathsep.join([str(pathlib.Path(NODE).parent), "/usr/bin", "/bin"]), "PAYPAL_ACCESS_TOKEN": token, "PAYPAL_ENVIRONMENT": "SANDBOX"})
    rec = {"run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "server": "PayPal official MCP server @paypal/mcp (npm)",
           "enabled_tools_flag": "--tools=disputes.list,disputes.get (read-only)", "environment": "SANDBOX", "steps": []}
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            rec["server_info"] = {"name": init.serverInfo.name, "version": init.serverInfo.version}
            tools = (await s.list_tools()).tools
            rec["tools"] = [{"name": t.name, "required": (t.inputSchema or {}).get("required", [])} for t in tools]
            by = {t.name: t for t in tools}
            lname = next((n for n in by if "list" in n and "dispute" in n), None); gname = next((n for n in by if n.endswith("get_dispute") or ("get" in n and "dispute" in n)), None)
            rec["tool_names_used"] = [lname, gname]
            first = None
            if lname:
                res = await s.call_tool(lname, {})
                raw = "".join(getattr(c, "text", "") for c in res.content)
                ids = re.findall(r"PP-R-[A-Z]{3}-\d{4,}", raw)
                first = ids[0] if ids else None
                rec["steps"].append({"tool": lname, "is_error": bool(res.isError), "dispute_ids_in_reply": len(set(ids)), "masked_sample": sorted({mask(i) for i in ids})[:3],
                                     "reply_sha256": hashlib.sha256(raw.encode()).hexdigest(), "reply_chars": len(raw)})
            if gname and first:
                gschema = by[gname].inputSchema or {}
                key = next(iter(gschema.get("required", ["dispute_id"])), "dispute_id")
                res = await s.call_tool(gname, {key: first})
                raw = "".join(getattr(c, "text", "") for c in res.content)
                rec["steps"].append({"tool": gname, "argument_name": key, "is_error": bool(res.isError), "reply_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                                     "reply_chars": len(raw)})
    ok = all(not st["is_error"] for st in rec["steps"]) and len(rec["steps"]) >= 1
    rec["note"] = "Reply bodies are not kept: they hold Sandbox transaction and payer ids. Each reply is represented by its length and SHA-256. Dispute ids are masked."
    rec["result"] = "OK" if ok else "FAILED"
    out = HERE / f"receipt_official_mcp_{datetime.now().strftime('%H%M%S')}.json"
    out.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    print("result:", rec["result"], "| server:", rec["server_info"], "| tools:", [t["name"] for t in rec["tools"]], "| steps:", [(st["tool"], st["is_error"]) for st in rec["steps"]])
    print("wrote", out.name); return 0 if ok else 1

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception as e:
        print("ERROR", type(e).__name__, str(e)[:160]); sys.exit(1)
