import hashlib
import re
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from payguard.dispute_evidence import MAX_ATTACHMENT_BYTES, validate_attachment_bytes
from payguard.evidence_pdf import (EvidencePdfError, FOOTER, build_evidence_pdf, evidence_pdf_for_case,
                                   fields_from_case)

PDFTOTEXT = "/opt/homebrew/bin/pdftotext"

CASE = {
    "delivered_at": "2026-11-06T10:00:00Z", "order_created_at": "2026-11-04T10:00:00Z",
    "opened_at": "2026-11-07T10:00:00Z", "dispute_amount": {"currency_code": "USD", "value": "125.50"},
    "provider_snapshot": {
        "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "status": "WAITING_FOR_SELLER_RESPONSE",
        "seller_response_due_date": "2026-11-09T10:00:00Z",
        "evidences": [
            {"request_id": "r1", "evidence_type": "PROOF_OF_FULFILLMENT", "mandatory": True},
            {"request_id": "r2", "evidence_type": "PROOF_OF_REFUND", "mandatory": False}]},
    "proof_records": [{"request_id": "r1", "proof_fields": {
        "carrier_name": "SYNTHETIC_CARRIER", "tracking_number": "SYNTHETIC_TRACKING_003",
        "delivered_at": "2026-11-06T10:00:00Z", "delivery_status": "DELIVERED",
        "destination_match_status": "MATCHED"}}],
}


def text_of(content):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "e.pdf"
        path.write_bytes(content)
        return subprocess.run([PDFTOTEXT, "-layout", str(path), "-"], capture_output=True, text=True,
                              check=True).stdout


class EvidencePdfTests(unittest.TestCase):
    def setUp(self):
        self.pdf = evidence_pdf_for_case("case-ref-003", CASE)

    def test_deterministic(self):
        self.assertEqual(self.pdf, evidence_pdf_for_case("case-ref-003", CASE))
        self.assertNotEqual(self.pdf, evidence_pdf_for_case("case-ref-001", CASE))

    def test_structure(self):
        self.assertTrue(self.pdf.startswith(b"%PDF-"))
        self.assertTrue(self.pdf.endswith(b"%%EOF\n"))
        count = int(re.search(rb"/Size (\d+)", self.pdf).group(1))
        self.assertEqual(len(re.findall(rb"\n\d+ 0 obj\n", self.pdf)), count - 1)
        xref = int(re.search(rb"startxref\n(\d+)\n", self.pdf).group(1))
        self.assertTrue(self.pdf[xref:].startswith(b"xref\n0 %d\n" % count))
        entries = re.findall(rb"(\d{10}) 00000 n \n", self.pdf)
        self.assertEqual(len(entries), count - 1)
        for number, offset in enumerate(entries, start=1):
            self.assertTrue(self.pdf[int(offset):].startswith(b"%d 0 obj" % number))
        self.assertLessEqual(len(re.findall(rb"/Type /Page /", self.pdf)), 2)

    def test_text_has_required_fields(self):
        text = text_of(self.pdf)
        for needle in ("case-ref-003", "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "WAITING_FOR_SELLER_RESPONSE",
                       "USD 125.50", "2026-11-09T10:00:00Z", "PROOF_OF_FULFILLMENT (mandatory): provided",
                       "PROOF_OF_REFUND (optional): NOT provided", "SYNTHETIC_CARRIER", "SYNTHETIC_TRACKING_003",
                       "2026-11-06T10:00:00Z", "Dispute opened", "HUMAN REVIEW", "seller-supplied, unverified", "Gaps",
                       "PROOF_OF_REFUND: no record provided", FOOTER):
            self.assertIn(needle, text)

    def test_review_stamp_and_zip_hash(self):
        digest = "ab" * 32
        text = text_of(evidence_pdf_for_case("case-ref-003", CASE, "2026-11-08T01:02:03Z", digest))
        self.assertIn("HUMAN REVIEW COMPLETED - 2026-11-08T01:02:03Z", text)
        self.assertIn(digest, text)
        with self.assertRaises(EvidencePdfError):
            evidence_pdf_for_case("case-ref-003", CASE, None, "not-a-hash")

    def test_no_forbidden_strings(self):
        text = text_of(self.pdf)
        self.assertNotRegex(text, r"@")
        self.assertNotIn("/" + "Users/", text)
        self.assertNotRegex(text, r"PP-[A-Z0-9]")
        self.assertNotRegex(self.pdf.decode("latin-1"), "/" + "Users/" + r"|PP-[A-Z0-9]|@|(?i:api.?key)")

    def test_refuses_forbidden_input(self):
        for bad in ("buyer@example.com", "/" + "Users/x/file", "PP-R-ABC123456"):
            fields = fields_from_case("case-ref-003", CASE)
            fields["carrier"] = bad
            with self.subTest(bad=bad), self.assertRaises(EvidencePdfError):
                build_evidence_pdf(fields)

    def test_same_bytes_in_two_processes(self):
        code = ("import sys,hashlib;sys.path[:0]=['src'];import test_evidence_pdf as t;"
                "from payguard.evidence_pdf import evidence_pdf_for_case as f;"
                "print(hashlib.sha256(f('case-ref-003',t.CASE)).hexdigest())")
        runs = {subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, check=True,
                               env={"PATH": "/usr/bin", "PYTHONPATH": "src:tests", "PYTHONHASHSEED": str(seed)},
                               cwd=str(Path(__file__).resolve().parent.parent)).stdout.strip() for seed in (1, 2)}
        self.assertEqual(runs, {hashlib.sha256(self.pdf).hexdigest()})

    def test_accepted_as_attachment(self):
        meta = validate_attachment_bytes("synthetic-delivery-003.pdf", "application/pdf", self.pdf)
        self.assertEqual(meta["detected_media_type"], "application/pdf")
        self.assertLess(len(self.pdf), MAX_ATTACHMENT_BYTES)
        self.assertLess(len(self.pdf), 20_000)

    def test_page_overflow_refused(self):
        fields = fields_from_case("case-ref-003", CASE)
        fields["requested"] = [{"evidence_type": "PROOF_OF_FULFILLMENT", "mandatory": True, "provided": True}] * 120
        with self.assertRaises(EvidencePdfError):
            build_evidence_pdf(fields)


if __name__ == "__main__":
    unittest.main()
