#!/usr/bin/env python3
"""Owner-run check: are the files PayPal holds for a Sandbox dispute byte-identical to the files TradeGlot sent?

Method (the same idea another entrant published): hash the exact bytes that were sent, then read the dispute back from
PayPal, download each document PayPal lists under the seller's submitted evidence, hash those bytes and compare.

Safety rules, all enforced in code:
  * Sandbox only: the host is fixed to api-m.sandbox.paypal.com, and a document URL on any other host is refused, so the
    bearer token can never be sent elsewhere. Redirects are refused.
  * Dry run by default: without --apply nothing is sent and no credential is read.
  * Credentials come from PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in the environment only; they are never printed or
    written. The receipt masks the dispute id and keeps only short hash prefixes.
  * Read-only against PayPal: one token request, one dispute GET, one GET per document. Nothing is submitted.

It does not prove PayPal accepted the evidence; it only compares bytes.

Usage:
  python3 tools/sandbox_readback_hash.py --dispute-id <dispute id> --sent-file path/to/file.pdf            # dry run
  python3 tools/sandbox_readback_hash.py --dispute-id <dispute id> --sent-file path/to/file.pdf --apply \\
      --receipt docs/evidence/RECEIPT_READBACK_<date>.md
Exit code: 0 all sent files matched, 1 a mismatch or a sent file not found at PayPal, 2 input or transport error.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SANDBOX_HOST = "api-m.sandbox.paypal.com"
BASE = "https://" + SANDBOX_HOST
DISPUTE_ID = re.compile(r"PP-[A-Z0-9][A-Z0-9-]{2,62}")
MAX_BYTES = 5_000_000
TIMEOUT = 30


class ReadbackError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # a redirect could carry the token to another host
        return None


def mask_dispute_id(value: str) -> str:
    return value[:7] + "..." if DISPUTE_ID.fullmatch(value) else "(invalid)"


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def check_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    try:
        port = parsed.port
    except ValueError as error:
        raise ReadbackError("document_url_refused") from error
    if (parsed.scheme != "https" or parsed.hostname != SANDBOX_HOST or parsed.username or parsed.password
            or port not in (None, 443)):
        raise ReadbackError("document_url_refused")
    return url


def http_get(url: str, headers: dict, data: bytes | None = None):
    """Real transport. Tests replace it with a stub that has the same signature."""
    request = urllib.request.Request(check_url(url), data=data, headers=headers)
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ReadbackError("response_too_large")
            return response.status, dict(response.headers), body
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers or {}), b""
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise ReadbackError("transport_error") from error


def get_token(client_id: str, client_secret: str, transport=http_get) -> str:
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    status, _, body = transport(BASE + "/v1/oauth2/token",
                                {"Authorization": "Basic " + basic, "Content-Type": "application/x-www-form-urlencoded"},
                                b"grant_type=client_credentials")
    if status != 200:
        raise ReadbackError("token_request_failed")
    token = json.loads(body.decode("utf-8")).get("access_token")
    if type(token) is not str or not token:
        raise ReadbackError("token_missing")
    return token


def seller_documents(dispute: dict) -> list[dict]:
    """Documents PayPal lists as submitted by the seller (name and url only)."""
    found = []
    for evidence in dispute.get("evidences", []) or []:
        if evidence.get("source") != "SUBMITTED_BY_SELLER":
            continue
        for document in evidence.get("documents", []) or []:
            url, name = document.get("url"), document.get("name")
            if type(url) is str and type(name) is str:
                found.append({"name": name, "url": url})
    return found


def read_back(dispute_id: str, token: str, transport=http_get) -> tuple[list[dict], str]:
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    status, response_headers, body = transport(f"{BASE}/v1/customer/disputes/{dispute_id}", headers)
    if status != 200:
        raise ReadbackError(f"dispute_read_failed_http_{status}")
    debug_id = response_headers.get("Paypal-Debug-Id") or response_headers.get("PayPal-Debug-Id") or ""
    rows = []
    for document in seller_documents(json.loads(body.decode("utf-8"))):
        # PayPal's content service answers 404 to "Accept: application/json" (seen on 2026-11-09 for two disputes) and serves
        # the file to "Accept: application/pdf". Ask for the PDF first, then for anything, before reporting a failure.
        doc_status, content = 0, b""
        for accept in ("application/pdf", "*/*"):
            doc_status, _, content = transport(document["url"], {**headers, "Accept": accept})
            if doc_status == 200:
                break
        if doc_status != 200:
            rows.append({"name": document["name"], "error": f"download_http_{doc_status}"})
            continue
        rows.append({"name": document["name"], "bytes": len(content), "sha256": sha256_hex(content)})
    return rows, debug_id


def compare(sent: list[dict], held: list[dict]) -> list[dict]:
    held_hashes = {row["sha256"] for row in held if "sha256" in row}
    return [{**row, "found_at_paypal": row["sha256"] in held_hashes} for row in sent]


def receipt_text(dispute_id: str, debug_id: str, sent: list[dict], held: list[dict], matched: list[dict]) -> str:
    lines = [
        "# TradeGlot Sandbox read-back hash check (masked)",
        "",
        "Sandbox test data created by the author. The check reads the dispute back from PayPal and compares the bytes of the files "
        "PayPal holds with the bytes that were sent. It does not mean PayPal accepted the evidence.",
        "",
        f"- dispute: {mask_dispute_id(dispute_id)} (masked)",
        f"- PayPal-Debug-Id of the dispute read: {debug_id or '(not returned)'}",
        f"- files sent (local hash): {len(sent)}; documents PayPal lists as submitted by the seller: {len(held)}",
        "",
        "| file sent | bytes | sha256 (first 16) | found at PayPal with the same bytes |",
        "|---|---|---|---|",
    ]
    for row in matched:
        lines.append(f"| {row['name']} | {row['bytes']} | {row['sha256'][:16]} | {'yes' if row['found_at_paypal'] else 'NO'} |")
    lines += ["", "| document PayPal holds | bytes | sha256 (first 16) |", "|---|---|---|"]
    for row in held:
        lines.append(f"| {row['name']} | {row.get('bytes', '-')} | {row.get('sha256', row.get('error', '-'))[:16]} |")
    return "\n".join(lines) + "\n"


def main(argv=None, transport=http_get, environ=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dispute-id", required=True)
    parser.add_argument("--sent-file", action="append", required=True, help="the exact file that was sent; repeatable")
    parser.add_argument("--apply", action="store_true", help="make the read-only Sandbox calls (default is a dry run)")
    parser.add_argument("--receipt", help="write a masked receipt (markdown) to this path")
    args = parser.parse_args(argv)
    environ = os.environ if environ is None else environ
    if DISPUTE_ID.fullmatch(args.dispute_id) is None:
        print("ERROR dispute id has the wrong shape", file=sys.stderr)
        return 2
    sent = []
    for name in args.sent_file:
        path = Path(name)
        if not path.is_file() or path.stat().st_size > MAX_BYTES:
            print(f"ERROR sent file not readable or too large: {path.name}", file=sys.stderr)
            return 2
        content = path.read_bytes()
        sent.append({"name": path.name, "bytes": len(content), "sha256": sha256_hex(content)})
    if not args.apply:
        print(f"DRY RUN: would read {mask_dispute_id(args.dispute_id)} from {SANDBOX_HOST} and compare {len(sent)} file(s).")
        for row in sent:
            print(f"  local {row['name']}: {row['bytes']} bytes, sha256 {row['sha256'][:16]}...")
        print("Nothing was sent; no credential was read. Add --apply to make the read-only calls.")
        return 0
    client_id, client_secret = environ.get("PAYPAL_CLIENT_ID", ""), environ.get("PAYPAL_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        print("ERROR PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET must be set in the environment", file=sys.stderr)
        return 2
    try:
        token = get_token(client_id, client_secret, transport)
        held, debug_id = read_back(args.dispute_id, token, transport)
    except (ReadbackError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    matched = compare(sent, held)
    text = receipt_text(args.dispute_id, debug_id, sent, held, matched)
    print(text)
    if args.receipt:
        Path(args.receipt).write_text(text, encoding="utf-8")
    return 0 if all(row["found_at_paypal"] for row in matched) else 1


if __name__ == "__main__":
    sys.exit(main())
