"""Record real Channel3 product-search replies for the hosted demo, plus a receipt of each call.

Runs the same adapter the console uses (``backend/app/channel3_products.py``) against the live API
for the console's quick-test product names, then writes:

* ``backend/app/data/channel3_recorded_v1.json``: the closed reference cards per sanitised name; the
  public demo replays these and never calls out.
* ``docs/evidence/channel3_receipts_v1.json``: one receipt per call (time, HTTP status, latency,
  number of cards, sha256 of the raw reply). No key, no raw reply.

The key is read from ``CHANNEL3_API_KEY`` only and is never printed or written. Usage, from the
repository root (``read -rs`` keeps the key off the screen and out of history):

  read -rs CHANNEL3_API_KEY && export CHANNEL3_API_KEY && .venv/bin/python3 tools/record_channel3.py; unset CHANNEL3_API_KEY
  .venv/bin/python3 tools/record_channel3.py --dry-run     # show what would be sent, no call

Exit code 0 when every name was recorded, 1 when any call failed, 2 when the key is missing.
"""

import argparse
import hashlib
import json
import os
import pathlib
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "backend"), str(ROOT / "src")]

from app.channel3 import CallBudget, Channel3Config, sanitize_product_name  # noqa: E402
from app.channel3_products import (RECORDED_PATH, Channel3ProductAdapter, httpx_post_transport,  # noqa: E402
                                   load_recorded)

# The console's quick-test names (frontend/src/App.jsx) plus everyday seller items.
NAMES = (
    "Handcrafted ceramic coffee cup — set of two",
    "Wireless noise cancelling headphones",
    "Leather crossbody bag",
    "Stainless steel water bottle 32 oz",
    "Kids wooden puzzle set",
)
RECEIPTS_PATH = ROOT / "docs" / "evidence" / "channel3_receipts_v1.json"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    queries = [sanitize_product_name(name) for name in NAMES]
    if args.dry_run:
        for name, query in zip(NAMES, queries):
            print(f"would send query={query!r} limit=3  (from {name!r})")
        return 0
    key = (os.environ.get("CHANNEL3_API_KEY") or "").strip()
    if not key:
        print("ERROR: CHANNEL3_API_KEY is not set; nothing was called", file=sys.stderr)
        return 2
    raw = {}

    def recording_transport(url, body, headers, timeout):
        status, data = httpx_post_transport(url, body, headers, timeout)
        raw["status"], raw["sha256"] = status, hashlib.sha256(data).hexdigest()
        return status, data

    adapter = Channel3ProductAdapter(Channel3Config(enabled=True, api_key=key), transport=recording_transport,
                                     budget=CallBudget(len(NAMES)))
    entries, receipts, failed = [], [], 0
    for query in queries:
        raw.clear()
        started = time.monotonic()
        result = adapter.lookup(query)
        latency = round(time.monotonic() - started, 3)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        receipts.append({"query": query, "called_at": stamp, "http_status": raw.get("status"), "latency_seconds": latency,
                         "result_status": result["status"], "reason": result["reason"], "cards": len(result["cards"]),
                         "reply_sha256": raw.get("sha256")})
        if result["status"] == "FOUND":
            entries.append({"query": query, "recorded_at": stamp, "cards": result["cards"]})
        else:
            failed += result["status"] == "UNAVAILABLE"
        print(f"{result['status']:<11} {len(result['cards'])} card(s) {latency:.2f}s  {query}")
    recorded = {"schema_version": "payguard.channel3_recorded.v1", "endpoint": "POST https://api.trychannel3.com/v1/search",
                "entries": entries}
    RECORDED_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECORDED_PATH.write_text(json.dumps(recorded, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    RECEIPTS_PATH.write_text(json.dumps({"schema_version": "payguard.channel3_receipts.v1", "receipts": receipts},
                                        indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if len(load_recorded()) != len(entries):
        print("ERROR: the written recordings do not load back in full", file=sys.stderr)
        return 1
    print(f"wrote {RECORDED_PATH.relative_to(ROOT)} ({len(entries)} names) and {RECEIPTS_PATH.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
