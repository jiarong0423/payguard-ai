"""Contract tests using frozen public references and explicit trusted byte fixtures."""

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import payguard.retrieval as retrieval
from payguard.retrieval import ReferenceCorpus, RetrievalError, load_corpus


ROOT = Path(__file__).absolute().parents[1]
CORPUS_DIR = ROOT / "data/knowledge/payguard_us_official_v2"
SOURCE = (CORPUS_DIR / "sources.json").read_bytes()
CHUNKS = (CORPUS_DIR / "chunks.jsonl").read_bytes()


def parse(source=SOURCE, chunks=CHUNKS):
    return ReferenceCorpus.from_bytes(source, chunks, hashlib.sha256(source).hexdigest(), hashlib.sha256(chunks).hexdigest())


def changed(source_change=None, chunk_change=None):
    sources = json.loads(SOURCE)
    chunks = [json.loads(line) for line in CHUNKS.splitlines()]
    if source_change:
        source_change(sources)
    if chunk_change:
        chunk_change(chunks)
    return json.dumps(sources, ensure_ascii=False).encode(), b"\n".join(json.dumps(row, ensure_ascii=False).encode() for row in chunks) + b"\n"


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = load_corpus()

    def ids(self, result):
        return {x["source_id"] for x in result["results"]}

    def test_us_v2_exact_identity_counts_ids_types_and_outcomes(self):
        expected_source_ids = {
            "PP-DEV-REST-GET-STARTED", "PP-DEV-SANDBOX-OVERVIEW", "PP-DEV-SANDBOX-ACCOUNTS",
            "PP-DEV-INVOICING", "PP-US-AUP", "PP-US-UA", "PP-US-PURCHASE-PROTECTION",
            "PP-US-SELLER-PROTECTION", "PP-DISPUTES-OVERVIEW", "PP-DISPUTES-API",
            "PP-DISPUTE-REASONS-EVIDENCE", "PP-DISPUTE-FILES", "PP-DISPUTES-SETUP",
            "PP-DISPUTES-TEST-GO-LIVE", "US-COURT-ZEPEDA-2017-DOC357", "US-COURT-EVANS-2022-DOC37",
        }
        self.assertEqual(retrieval.CORPUS_ID, "payguard-us-official-references-v2")
        self.assertEqual(hashlib.sha256(SOURCE).hexdigest(), retrieval.SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(CHUNKS).hexdigest(), retrieval.CHUNKS_SHA256)
        self.assertEqual(len(self.corpus._sources), 16)
        self.assertEqual(len(self.corpus._chunks), 29)
        self.assertEqual(set(self.corpus._sources), expected_source_ids)
        self.assertEqual(set(self.corpus._regions.values()), {"US"})
        self.assertEqual({row["material_type"] for row in self.corpus._sources.values()}, {
            "official_api_reference", "official_policy", "public_court_order_copy",
        })
        court_outcomes = {
            row["source_id"]: row["case_outcome"]
            for row in self.corpus._chunks
            if row["material_type"] == "public_court_order_copy"
        }
        self.assertEqual(court_outcomes, {
            "US-COURT-ZEPEDA-2017-DOC357": "SETTLEMENT_APPROVAL_NOT_FINAL_MERITS",
            "US-COURT-EVANS-2022-DOC37": "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED",
        })

    def test_us_aup_and_foreign_jurisdictions_fail_closed(self):
        result = self.corpus.search("AUP prior approval", "source_compliance", "US", material_types=["official_policy"])
        self.assertEqual(self.ids(result), {"PP-US-AUP"})
        self.assertTrue(all(x["jurisdiction"] == "US" for x in result["results"]))
        self.assertTrue(all(x["case_stage"] == "not_applicable" and x["case_outcome"] is None for x in result["results"]))
        for foreign in ("CA", "GB", "GLOBAL"):
            with self.subTest(jurisdiction=foreign), self.assertRaises(RetrievalError) as error:
                self.corpus.search("AUP", "source_compliance", foreign)
            self.assertEqual(error.exception.code, "filter_invalid")

    def test_velocity_policy_and_procedural_case_are_distinct(self):
        policy = self.corpus.search("rapid sales growth", "velocity_guard", "US", material_types=["official_policy"])
        self.assertEqual(self.ids(policy), {"PP-US-UA"})
        self.assertTrue(all(row["case_stage"] == "not_applicable" for row in policy["results"]))
        procedure = self.corpus.search("settlement hold reserve", "velocity_guard", "US", case_stage="procedural_order")
        self.assertEqual(self.ids(procedure), {"US-COURT-ZEPEDA-2017-DOC357"})
        self.assertEqual(procedure["results"][0]["case_outcome"], "SETTLEMENT_APPROVAL_NOT_FINAL_MERITS")

    def test_english_reason_and_inr_short_code(self):
        for query in ("INR", "MERCHANDISE_OR_SERVICE_NOT_RECEIVED", "Item not received"):
            with self.subTest(query=query):
                result = self.corpus.search(query, "dispute_mediation", "US")
                self.assertIn("PP-REASONS-INR", {x["chunk_id"] for x in result["results"]})
                self.assertTrue(all(x["jurisdiction"] == "US" for x in result["results"]))

    def test_seller_eligibility_metadata_owns_snad_boundary(self):
        row = next(item for item in self.corpus._chunks if item["chunk_id"] == "PP-US-SELLER-ELIGIBILITY")
        self.assertEqual(row["reason_codes"], [
            "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
            "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED",
            "UNAUTHORISED",
        ])
        self.assertIn("Significantly Not as Described claims are ineligible", row["text"])
        self.assertEqual(
            hashlib.sha256(row["text"].encode("utf-8")).hexdigest(),
            row["text_sha256"],
        )

    def test_court_stage_and_official_not_applicable(self):
        expected = {
            "US-COURT-ZEPEDA-2017-DOC357": "SETTLEMENT_APPROVAL_NOT_FINAL_MERITS",
            "US-COURT-EVANS-2022-DOC37": "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED",
        }
        rows = []
        rows.extend(self.corpus.search("settlement hold reserve", "velocity_guard", "US", case_stage="procedural_order")["results"])
        rows.extend(self.corpus.search("arbitration AUP allegation", "source_compliance", "US", case_stage="procedural_order")["results"])
        self.assertEqual({row["source_id"]: row["case_outcome"] for row in rows}, expected)
        self.assertTrue(all(row["case_stage"] == "procedural_order" for row in rows))
        with self.assertRaises(RetrievalError) as error:
            self.corpus.search("settlement arbitration", "velocity_guard", "US", case_stage="final_decision")
        self.assertEqual(error.exception.code, "filter_invalid")

    def test_missing_source_date_known_filter_and_no_date_fabrication(self):
        self.assertEqual(self.corpus.search("settlement", "velocity_guard", "US", require_known_source_date=True)["results"], [])
        result = self.corpus.search("AUP", "source_compliance", "US", require_known_source_date=True)
        self.assertEqual(result["results"][0]["source_updated_date"], "2022-10-29")
        self.assertIsNone(result["results"][0]["effective_date"])
        self.assertEqual(result["results"][0]["effective_date_status"], "NOT_VERIFIED")

    def test_source_age_uses_document_date_not_recent_retrieval(self):
        result = self.corpus.search("AUP", "source_compliance", "US", max_source_age_days=365, as_of="2026-10-06T12:00:00+08:00")
        self.assertEqual(result["results"], [])
        fresh = self.corpus.search("rapid sales growth", "velocity_guard", "US", max_source_age_days=365, as_of=datetime(2026, 10, 6, 4, tzinfo=timezone.utc))
        self.assertEqual(self.ids(fresh), {"PP-US-UA"})
        past = self.corpus.search("rapid sales growth", "velocity_guard", "US", as_of="2026-07-01T00:00:00Z")
        self.assertEqual(past["results"], [])

    def test_empty_invalid_but_nonempty_no_match_is_evidence_missing(self):
        for query in ("", "  ", None, True, "a\x00b", "a\u200bb", "a" * 513):
            with self.subTest(query=repr(query)), self.assertRaises(RetrievalError) as error:
                self.corpus.search(query, "source_compliance", "US")
            self.assertEqual(error.exception.code, "query_invalid")
        result = self.corpus.search("zxqv12345totallyabsent", "source_compliance", "US")
        self.assertEqual(result["status"], "evidence_missing")
        self.assertEqual(result["results"], [])
        self.assertNotIn("zxqv12345totallyabsent", json.dumps(result))
        one_letter = self.corpus.search("a", "velocity_guard", "US")
        self.assertEqual(one_letter["status"], "evidence_missing")
        self.assertEqual(one_letter["results"], [])

    def test_filter_and_limit_types_fail_closed(self):
        cases = [{"theme": "unknown"}, {"jurisdiction": "ZZ"}, {"case_stage": "won"}, {"limit": True}, {"limit": 0}, {"limit": 11},
                 {"material_types": []}, {"material_types": ["unknown"]}, {"material_types": ["official_policy", "official_policy"]},
                 {"material_types": "official_policy"}, {"require_known_source_date": 1}, {"max_source_age_days": True, "as_of": "2026-10-04T15:00:00Z"},
                 {"max_source_age_days": 1}, {"max_source_age_days": -1, "as_of": "2026-10-04T15:00:00Z"}, {"as_of": "2026-10-04T15:00:00"}]
        for change in cases:
            kwargs = {"query": "AUP", "theme": "source_compliance", "jurisdiction": "US"}
            kwargs.update(change)
            with self.subTest(change=change), self.assertRaises(RetrievalError):
                self.corpus.search(**kwargs)

    def test_material_filter_limit_citation_schema(self):
        result = self.corpus.search("AUP", "source_compliance", "US", material_types=["official_policy"], limit=1)
        self.assertEqual(self.ids(result), {"PP-US-AUP"})
        self.assertTrue(result["advisory_only"])
        self.assertEqual(result["operational_authority"], "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION")
        row = result["results"][0]
        self.assertTrue({"title", "source_title", "url", "locator", "source_updated_date_status", "decision_date_status", "text_sha256", "relevance_score"} <= set(row))
        self.assertNotIn("confidence", row)

    def test_stable_repeat_parallel_and_defensive_copy(self):
        first = self.corpus.search("AUP", "source_compliance", "US", limit=10)
        expected = deepcopy(first)
        first["results"][0]["text"] = "changed"
        first["corpus_digests"].clear()
        first["limitations"].clear()
        with ThreadPoolExecutor(max_workers=3) as pool:
            actual = list(pool.map(lambda _: self.corpus.search("AUP", "source_compliance", "US", limit=10), range(6)))
        self.assertTrue(all(row == expected for row in actual))
        ties = expected["results"]
        self.assertEqual(ties, sorted(ties, key=lambda x: (-x["relevance_score"], x["chunk_id"])))
        self.assertEqual((CORPUS_DIR / "sources.json").read_bytes(), SOURCE)
        self.assertEqual((CORPUS_DIR / "chunks.jsonl").read_bytes(), CHUNKS)

    def test_default_digest_tamper_and_unvalidated_constructor(self):
        with self.assertRaises(RetrievalError) as error:
            ReferenceCorpus.from_bytes(SOURCE + b" ", CHUNKS, retrieval.SOURCE_SHA256, retrieval.CHUNKS_SHA256)
        self.assertEqual(error.exception.code, "corpus_digest_mismatch")
        with self.assertRaises(RetrievalError):
            ReferenceCorpus()
        with self.assertRaises(RetrievalError):
            ReferenceCorpus.from_bytes(SOURCE, CHUNKS, "bad", retrieval.CHUNKS_SHA256)

    def test_malformed_duplicate_json_keys_nonfinite_and_blank_line(self):
        for source, chunks in ((b"{", CHUNKS), (SOURCE, CHUNKS + b"\n"), (SOURCE, b"{\"a\":NaN}"),
                               (b'{"schema_version":1,"schema_version":1}', CHUNKS), (SOURCE, b'{} trailing'), (b'\xff', CHUNKS)):
            with self.subTest(source=source[:20]), self.assertRaises(RetrievalError):
                parse(source, chunks)

    def test_duplicate_source_chunk_ids_missing_join_metadata_hash(self):
        mutations = [
            (lambda s: s["sources"][1].update(source_id=s["sources"][0]["source_id"]), None),
            (None, lambda c: c[1].update(chunk_id=c[0]["chunk_id"])),
            (None, lambda c: c[0].update(source_id="UNKNOWN")),
            (None, lambda c: c[0].update(jurisdiction="CA")),
            (None, lambda c: c[0].update(text="Changed summary")),
            (None, lambda c: c[0].update(reason_codes=["UNKNOWN"])),
            (lambda s: s["sources"][0].update(jurisdiction="unknown"), None),
            (lambda s: s["sources"][0].update(source_updated_date_status=[]), None),
            (None, lambda c: c[0].update(case_outcome={"untrusted": "won"})),
            (lambda s: s["theme_case_map"]["source_compliance"].append("US-COURT-ZEPEDA-2017-DOC357"), None),
            (lambda s: s["sources"][0].update(source_updated_date=None), None),
            (lambda s: s.update(source_count=True), None),
        ]
        for source_change, chunk_change in mutations:
            with self.subTest(mutation=mutations.index((source_change, chunk_change))), self.assertRaises(RetrievalError):
                parse(*changed(source_change, chunk_change))

    def test_unsafe_urls_and_bad_date_rejected_without_echo(self):
        for url in ("http://www.paypal.com/us/legalhub/paypal/x", "https://www.paypal.com.evil.invalid/x", "https://user:secret@www.paypal.com/us/legalhub/paypal/x", "https://www.paypal.com:444/us/legalhub/paypal/x", "https://www.paypal.com/us/legalhub/paypal/%2e%2e/x", "https://www.paypal.com\\evil.invalid/x"):
            def change(s):
                s["sources"][0]["url"] = url
            with self.subTest(url=url), self.assertRaises(RetrievalError) as error:
                parse(*changed(change))
            self.assertNotIn(url, str(error.exception))
        with self.assertRaises(RetrievalError):
            parse(*changed(lambda s: s["sources"][0].update(retrieved_at="2026-10-04T15:00:00")))

    def test_size_and_record_text_caps(self):
        with self.assertRaises(RetrievalError):
            parse(b" " * (retrieval.MAX_FILE_BYTES + 1), CHUNKS)
        def huge(c):
            c[0]["text"] = "x" * 8001
            c[0]["text_sha256"] = hashlib.sha256(c[0]["text"].encode()).hexdigest()
        with self.assertRaises(RetrievalError):
            parse(*changed(chunk_change=huge))
        with self.assertRaises(RetrievalError):
            parse(bytearray(SOURCE), CHUNKS)

    def test_fixed_loader_symlink_final_and_ancestor(self):
        with tempfile.TemporaryDirectory(prefix="payguard-retrieval-tests-") as temporary:
            root = Path(temporary)
            data = root / "data/knowledge/payguard_us_official_v2"
            data.mkdir(parents=True)
            (root / "outside.json").write_bytes(SOURCE)
            (data / "sources.json").symlink_to(root / "outside.json")
            (data / "chunks.jsonl").write_bytes(CHUNKS)
            fake_module = root / "src/payguard/retrieval.py"
            fake_module.parent.mkdir(parents=True)
            fake_module.write_text("# test module identity\n", encoding="utf-8")
            with patch.object(retrieval, "__file__", str(fake_module)), self.assertRaises(RetrievalError) as error:
                load_corpus()
            self.assertEqual(error.exception.code, "corpus_path_invalid")
            (data / "sources.json").unlink()
            (data / "sources.json").write_bytes(SOURCE)
            actual = root / "actual"
            data.rename(actual)
            data.symlink_to(actual, target_is_directory=True)
            with patch.object(retrieval, "__file__", str(fake_module)), self.assertRaises(RetrievalError):
                load_corpus()

    def test_module_root_alias_loads_without_weakening_fixed_reader(self):
        with tempfile.TemporaryDirectory(prefix="payguard-retrieval-alias-") as temporary:
            alias = Path(temporary) / "project-alias"
            alias.symlink_to(ROOT, target_is_directory=True)
            module_path = alias / "src/payguard/retrieval.py"
            self.assertNotEqual(module_path.absolute(), module_path.resolve(strict=True))
            with patch.object(retrieval, "__file__", str(module_path)):
                corpus = load_corpus()
            self.assertEqual(corpus._digests["sources_sha256"], retrieval.SOURCE_SHA256)
            self.assertEqual(corpus._digests["chunks_sha256"], retrieval.CHUNKS_SHA256)

    def test_fixed_reader_hash_type_missing_and_root_escape_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix="payguard-retrieval-boundary-") as temporary:
            workspace = Path(temporary)
            root = workspace / "project"
            data = root / "data/knowledge/payguard_us_official_v2"
            data.mkdir(parents=True)
            source_path = data / "sources.json"
            chunk_path = data / "chunks.jsonl"
            source_path.write_bytes(SOURCE + b" ")
            chunk_path.write_bytes(CHUNKS)
            fake_module = root / "src/payguard/retrieval.py"
            fake_module.parent.mkdir(parents=True)
            fake_module.write_text("# test module identity\n", encoding="utf-8")
            with patch.object(retrieval, "__file__", str(fake_module)), self.assertRaises(RetrievalError) as error:
                load_corpus()
            self.assertEqual(error.exception.code, "corpus_digest_mismatch")

            source_path.unlink()
            with patch.object(retrieval, "__file__", str(fake_module)), self.assertRaises(RetrievalError) as error:
                load_corpus()
            self.assertEqual(error.exception.code, "corpus_unavailable")

            source_path.mkdir()
            with patch.object(retrieval, "__file__", str(fake_module)), self.assertRaises(RetrievalError) as error:
                load_corpus()
            self.assertEqual(error.exception.code, "corpus_path_invalid")

            outside = workspace / "outside.json"
            outside.write_bytes(SOURCE)
            with self.assertRaises(RetrievalError) as error:
                retrieval._read_fixed(outside, root)
            self.assertEqual(error.exception.code, "corpus_path_invalid")

    def test_import_does_not_read_corpus_or_open_connections(self):
        code = "from pathlib import Path\nfrom unittest.mock import patch\nwith patch.object(Path,'read_bytes',side_effect=RuntimeError('read')), patch('os.open',side_effect=RuntimeError('open')), patch('socket.create_connection',side_effect=RuntimeError('network')):\n import payguard.retrieval\n"
        process = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 0, process.stderr)


if __name__ == "__main__":
    unittest.main()
