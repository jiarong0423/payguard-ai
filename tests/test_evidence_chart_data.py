"""Evidence-page chart data: extracted from the evidence records, never typed by hand.

The committed JSON files must equal a fresh extraction of the Markdown sources they name (by sha256),
and their totals must add up. In a public source candidate the Markdown sources are not shipped, so the
re-extraction tests skip there and the totals checks still run on the committed files.
"""

import hashlib
import json
import pathlib
import shutil
import tempfile
import unittest

from tools import extract_evidence_charts as extract

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES_PRESENT = all((ROOT / path).is_file() for path in (extract.BASELINE_MD, extract.STRESS_MD))


def committed(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


@unittest.skipUnless(SOURCES_PRESENT, "evidence Markdown sources are not part of this tree")
class ReExtraction(unittest.TestCase):
    def test_committed_json_equals_a_fresh_extraction(self):
        for path, text in extract.outputs(ROOT).items():
            with self.subTest(path=path):
                self.assertEqual((ROOT / path).read_text(encoding="utf-8"), text,
                                 "run python3 tools/extract_evidence_charts.py")

    def test_recorded_source_hash_is_the_current_file(self):
        for path, source in ((extract.BLIND_TREND_OUT, extract.BASELINE_MD), (extract.STRESS_TEST_OUT, extract.STRESS_MD)):
            with self.subTest(path=path):
                recorded = committed(path)["source"]
                self.assertEqual(recorded["path"], source)
                self.assertEqual(recorded["sha256"], hashlib.sha256((ROOT / source).read_bytes()).hexdigest())

    def test_every_extracted_row_points_at_its_source_line(self):
        baseline = (ROOT / extract.BASELINE_MD).read_text(encoding="utf-8").splitlines()
        for step in committed(extract.BLIND_TREND_OUT)["steps"]:
            line = baseline[step["source_line"] - 1]
            self.assertIn(f"{step['precision']:.2f}", line)
            self.assertIn(f"{step['recall']:.2f}", line)
            self.assertIn(str(step["confident_wrong"]), line)
        stress = (ROOT / extract.STRESS_MD).read_text(encoding="utf-8").splitlines()
        document = committed(extract.STRESS_TEST_OUT)
        for row in document["rounds"]:
            line = stress[row["source_line"] - 1]
            self.assertTrue(line.startswith(f"| {row['round']} | {row['corpus']} ({row['items']}"), line)
            self.assertTrue(line.rstrip().endswith(f"| {row['scored_replies']} |"), line)
        for row in document["drift"]:
            self.assertEqual(stress[row["source_line"] - 1], f"| {row['drift_type']} | {row['result']} |")


@unittest.skipUnless(SOURCES_PRESENT, "evidence Markdown sources are not part of this tree")
class FailsClosed(unittest.TestCase):
    """A changed source stops the extraction instead of producing a guessed number."""

    def copy_with(self, relative, old, new):
        temporary = pathlib.Path(tempfile.mkdtemp(prefix="payguard-evidence-extract-"))
        self.addCleanup(shutil.rmtree, temporary)
        for path in (extract.BASELINE_MD, extract.STRESS_MD):
            (temporary / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, temporary / path)
        text = (temporary / relative).read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, old)
        (temporary / relative).write_text(text.replace(old, new), encoding="utf-8")
        return temporary

    def test_total_row_must_equal_the_sum_of_rounds(self):
        root = self.copy_with(extract.STRESS_MD, "| Tag contract v3 | heldout_v3 (36) | 2 (Gemini API, two models) | 72 |",
                              "| Tag contract v3 | heldout_v3 (36) | 2 (Gemini API, two models) | 71 |")
        with self.assertRaisesRegex(extract.ExtractionError, "total scored_replies"):
            extract.extract_stress_test(root)

    def test_non_zero_format_failures_cannot_be_split_by_round(self):
        root = self.copy_with(extract.STRESS_MD, "| Reply outside the closed JSON format | 0 / 601 |",
                              "| Reply outside the closed JSON format | 2 / 601 |")
        with self.assertRaisesRegex(extract.ExtractionError, "per-round source"):
            extract.extract_stress_test(root)

    def test_trend_row_must_match_its_blind_set_table(self):
        root = self.copy_with(extract.BASELINE_MD, "| adb9a32 | v2 | 0.86 | 0.77 | 4 |", "| adb9a32 | v2 | 0.86 | 0.77 | 2 |")
        with self.assertRaisesRegex(extract.ExtractionError, "does not match the blind v2 table"):
            extract.extract_blind_trend(root)

    def test_missing_table_or_sentence_is_an_error(self):
        root = self.copy_with(extract.BASELINE_MD, "## Trend across the three blind sets", "## Trend (renamed)")
        with self.assertRaisesRegex(extract.ExtractionError, "heading not found"):
            extract.extract_blind_trend(root)
        root = self.copy_with(extract.BASELINE_MD, "Keyword chooser alone on blind v4:", "On blind v4 the chooser alone had:")
        with self.assertRaisesRegex(extract.ExtractionError, "blind v4 sentence not found"):
            extract.extract_blind_trend(root)
        root = self.copy_with(extract.STRESS_MD, "| Combined | all_v1 (60, 50 reach a model) |",
                              "| Combined | all_v1 |")
        with self.assertRaisesRegex(extract.ExtractionError, "volume row changed shape"):
            extract.extract_stress_test(root)


class Totals(unittest.TestCase):
    """Runs everywhere, including a public candidate: the committed numbers add up."""

    def test_stress_test_rounds_add_up_to_the_stated_totals(self):
        document = committed(extract.STRESS_TEST_OUT)
        rounds, total = document["rounds"], document["total"]
        self.assertEqual(sum(row["scored_replies"] for row in rounds), total["scored_replies"])
        self.assertEqual(sum(row["items"] for row in rounds), total["items"])
        self.assertEqual(sum(row["conditions"] for row in rounds), total["runs"])
        self.assertEqual(len(rounds), total["corpora"])
        self.assertEqual(len({row["corpus"] for row in rounds}), total["corpora"])
        for row in rounds:
            self.assertEqual(row["within_format"] + row["outside_format"], row["scored_replies"])
        outside = [row for row in document["drift"] if row["drift_type"] == "Reply outside the closed JSON format"]
        self.assertEqual(len(outside), 1)
        self.assertEqual(outside[0]["of_replies"], total["scored_replies"])
        self.assertEqual(outside[0]["count"], sum(row["outside_format"] for row in rounds))
        self.assertLessEqual(document["gemini_api_replies"], total["scored_replies"])
        self.assertEqual(document["schema_version"], "payguard.stress_test.v1")
        self.assertRegex(document["source"]["sha256"], r"^[0-9a-f]{64}$")

    def test_blind_trend_steps_are_complete_and_in_range(self):
        document = committed(extract.BLIND_TREND_OUT)
        steps = document["steps"]
        self.assertEqual(document["schema_version"], "payguard.blind_trend.v1")
        self.assertRegex(document["source"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertGreaterEqual(len(steps), 2)
        self.assertEqual(steps[-1]["blind_set"], "v4")
        for step in steps:
            self.assertEqual(set(step), {"rules", "blind_set", "precision", "recall", "confident_wrong", "attack_touched",
                                         "source_line", "source_section"})
            self.assertTrue(0 <= step["precision"] <= 1 and 0 <= step["recall"] <= 1)
            self.assertGreaterEqual(step["confident_wrong"], document["red_line_confident_wrong"])
        versions = [int(step["blind_set"][1:]) for step in steps]
        self.assertEqual(versions, sorted(versions), "one blind set per step, in order")


if __name__ == "__main__":
    unittest.main()
