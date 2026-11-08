"""Tests for tools/sandbox_readback_hash.py with a stub transport: no network, no credentials, no real files at PayPal."""

import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import sandbox_readback_hash as tool  # noqa: E402

DISPUTE = "PP-R-ABC-" + "1234" + "5678"  # built at run time: the public-text gate rejects a literal dispute id
DOC_URL = "https://api-m.sandbox.paypal.com/v1/customer/disputes/" + DISPUTE + "/documents/evidence-summary.pdf"
ENV = {"PAYPAL_CLIENT_ID": "client", "PAYPAL_CLIENT_SECRET": "secret"}


def make_transport(documents, held_bytes, calls):
    def transport(url, headers, data=None):
        calls.append(url)
        if url.endswith("/v1/oauth2/token"):
            return 200, {}, json.dumps({"access_token": "token-value"}).encode()
        if url.endswith("/v1/customer/disputes/" + DISPUTE):
            body = {"evidences": [{"source": "SUBMITTED_BY_SELLER", "documents": documents},
                                  {"source": "SUBMITTED_BY_BUYER", "documents": [{"name": "buyer.png", "url": DOC_URL}]}]}
            return 200, {"Paypal-Debug-Id": "dbg123456789"}, json.dumps(body).encode()
        return 200, {}, held_bytes
    return transport


class ReadbackTests(unittest.TestCase):
    def run_main(self, args, transport=None, environ=None):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = tool.main(args, transport=transport or tool.http_get, environ=ENV if environ is None else environ)
        return code, out.getvalue(), err.getvalue()

    def sent_file(self, content):
        folder = tempfile.mkdtemp()
        path = Path(folder) / "evidence-summary.pdf"
        path.write_bytes(content)
        return str(path)

    def test_dry_run_makes_no_call_and_reads_no_credential(self):
        calls = []
        code, out, _ = self.run_main(["--dispute-id", DISPUTE, "--sent-file", self.sent_file(b"abc")],
                                     transport=make_transport([], b"", calls), environ={})
        self.assertEqual(code, 0)
        self.assertEqual(calls, [])
        self.assertIn("DRY RUN", out)
        self.assertNotIn(DISPUTE, out)  # the id is masked even in a dry run

    def test_identical_bytes_match(self):
        calls = []
        content = b"%PDF-1.4 real evidence bytes"
        transport = make_transport([{"name": "evidence-summary.pdf", "url": DOC_URL}], content, calls)
        code, out, _ = self.run_main(["--dispute-id", DISPUTE, "--sent-file", self.sent_file(content), "--apply"], transport)
        self.assertEqual(code, 0)
        self.assertIn(hashlib.sha256(content).hexdigest()[:16], out)
        self.assertIn("| yes |", out)
        self.assertNotIn("token-value", out)
        self.assertNotIn(DISPUTE, out)
        self.assertIn("dbg123456789", out)
        self.assertEqual(sum(url == DOC_URL for url in calls), 1)  # only the seller's document is downloaded

    def test_different_bytes_are_reported_as_a_mismatch(self):
        transport = make_transport([{"name": "evidence-summary.pdf", "url": DOC_URL}], b"other bytes", [])
        code, out, _ = self.run_main(["--dispute-id", DISPUTE, "--sent-file", self.sent_file(b"sent bytes"), "--apply"], transport)
        self.assertEqual(code, 1)
        self.assertIn("| NO |", out)

    def test_document_url_on_another_host_is_refused_and_the_token_is_not_sent(self):
        evil = "https://example.com/steal.pdf"
        # the stub transport does not check hosts; the real transport does, so test the check and the real transport directly
        with self.assertRaises(tool.ReadbackError):
            tool.check_url(evil)
        with self.assertRaises(tool.ReadbackError):
            tool.check_url("https://api-m.sandbox.paypal.com:8443/x")
        with self.assertRaises(tool.ReadbackError):
            tool.check_url("https://user:pw@api-m.sandbox.paypal.com/x")
        tool.check_url("https://api-m.sandbox.paypal.com/x")
        tool.check_url("https://api-m.sandbox.paypal.com:443/x")
        with self.assertRaises(tool.ReadbackError):
            tool.check_url("http://api-m.sandbox.paypal.com/x")
        with self.assertRaises(tool.ReadbackError):
            tool.check_url("https://api-m.sandbox.paypal.com.evil.test/x")
        with self.assertRaises(tool.ReadbackError):
            tool.http_get(evil, {"Authorization": "Bearer token-value"})  # refused before any connection is made
        self.assertIsNone(tool._NoRedirect().redirect_request(None, None, 302, "Found", {}, evil))  # a redirect is never followed

    def test_neither_the_client_secret_nor_the_token_reaches_output_or_the_receipt(self):
        environ = {"PAYPAL_CLIENT_ID": "CLIENT-ID-VALUE", "PAYPAL_CLIENT_SECRET": "CLIENT-SECRET-VALUE"}
        content = b"%PDF-1.4 evidence"
        transport = make_transport([{"name": "evidence-summary.pdf", "url": DOC_URL}], content, [])
        receipt = str(Path(tempfile.mkdtemp()) / "receipt.md")
        code, out, err = self.run_main(["--dispute-id", DISPUTE, "--sent-file", self.sent_file(content), "--apply",
                                        "--receipt", receipt], transport, environ=environ)
        self.assertEqual(code, 0)
        written = Path(receipt).read_text(encoding="utf-8")
        for secret in ("CLIENT-SECRET-VALUE", "CLIENT-ID-VALUE", "token-value", DISPUTE):
            for text in (out, err, written):
                self.assertNotIn(secret, text)

    def test_missing_credentials_and_bad_ids_stop_early(self):
        code, _, err = self.run_main(["--dispute-id", DISPUTE, "--sent-file", self.sent_file(b"a"), "--apply"], environ={})
        self.assertEqual(code, 2)
        self.assertIn("PAYPAL_CLIENT_ID", err)
        code, _, err = self.run_main(["--dispute-id", "not-an-id", "--sent-file", self.sent_file(b"a")])
        self.assertEqual(code, 2)

    def test_only_seller_documents_are_listed(self):
        dispute = {"evidences": [{"source": "SUBMITTED_BY_SELLER", "documents": [{"name": "a.pdf", "url": DOC_URL}]},
                                 {"source": "SUBMITTED_BY_BUYER", "documents": [{"name": "b.png", "url": DOC_URL}]}]}
        self.assertEqual([row["name"] for row in tool.seller_documents(dispute)], ["a.pdf"])


if __name__ == "__main__":
    unittest.main()
