"""(P3 2026-11-12) Check a sale display data: every value the page shows is recomputed from its source.

frontend/src/data/check_sale_examples_v1.json: the three sample results (rerun through check_aup and
country_rules.check), the App.jsx label for a review signal, and the Step 01 guide's recorded Gemini round.
The Channel3 tree-vs-AUP reference block: counts from docs/CHANNEL3_NOTES.md and the published CSV, three CSV rows.
"""
import csv
import json
import re
import unittest
from pathlib import Path

from payguard import country_rules
from payguard.engines import check_aup

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = json.loads((ROOT / "frontend/src/data/check_sale_examples_v1.json").read_text(encoding="utf-8"))


def example(example_id):
    return next(item for item in EXAMPLES["examples"] if item["id"] == example_id)


class ThreeResultsTest(unittest.TestCase):
    def test_no_match_card_is_the_engine_output(self):
        card = example("no_match")
        result = check_aup(card["description"])
        self.assertEqual(result["match_status"], card["match_status"])
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["recommendation"], card["detail"])
        app = (ROOT / "frontend/src/App.jsx").read_text(encoding="utf-8")
        self.assertIn(f"<Badge tone=\"muted\">{card['result']}</Badge>", app)

    def test_review_signal_card_is_the_engine_output(self):
        card = example("review_signal")
        result = check_aup(card["description"])
        self.assertEqual(result["match_status"], "REVIEW_SIGNAL")
        self.assertEqual([finding["category"] for finding in result["findings"]], [card["category"]])
        self.assertEqual(result["recommendation"], card["detail"])
        app = (ROOT / "frontend/src/App.jsx").read_text(encoding="utf-8")
        self.assertIn(f"{card['category']}: '{card['result']}'", app)
        self.assertEqual(card["result"], "Return claim to double-check")

    def test_rule_match_card_is_the_country_check_output(self):
        card = example("rule_match")
        result = country_rules.check(card["seller_country"], card["buyer_country"], goods_tags=card["goods_tags"])
        self.assertTrue(result["blocked"])
        blocks = [row for row in result["findings"] if row["severity"] == "BLOCK"]
        self.assertEqual(len(blocks), 1)
        self.assertTrue(blocks[0]["text"].endswith(f"[{card['result']}]"))
        self.assertTrue(blocks[0]["text"].startswith("Singapore import (prohibited):"))
        self.assertEqual(card["detail"], "Singapore import, prohibited")
        post = [row for row in result["findings"] if row["severity"] == "WARN" and row["code"] == "export_prohibited"]
        self.assertEqual(len(post), 1)
        self.assertIn("(banned by post; other channels may differ)", post[0]["text"])
        self.assertIn(f"[{card['also']['statute']} ", post[0]["text"])
        self.assertEqual(card["also"]["label"], "Check first")
        pack_text = (ROOT / "data/country_rules/paypal_country_rules_v1.json").read_text(encoding="utf-8").split("\n")
        for cite in re.findall(r"paypal_country_rules_v1\.json:(\d+)", card["source"]):
            self.assertRegex(pack_text[int(cite) - 1].strip(), r'^"id": "(SG-IM-EC-01|US-EX-EC-01)",$')


class GuideAiTest(unittest.TestCase):
    def test_recorded_round_matches_the_evidence_page(self):
        ai = EXAMPLES["guide_ai"]
        lines = (ROOT / ai["source"]).read_text(encoding="utf-8").split("\n")
        row = [cell.strip() for cell in lines[ai["line"] - 1].strip("|").split("|")]
        self.assertTrue(row[0].startswith("Policy pre-check"))
        self.assertEqual([row[1], row[2], row[3], row[4], row[6], row[7]],
                         [ai["format_invalid"], ai["precision"], ai["recall"], ai["confident_wrong"], ai["attack_touched"], ai["latency"]])
        self.assertEqual(ai["sentences"], int(row[1].split("/")[1]))
        text = "\n".join(lines)
        self.assertIn(f"## API round: `{ai['model']}`", text)
        self.assertIn(f"Run {ai['date']} ", text)
        self.assertIn("(Gemini maps a seller sentence to a form item; fixed rules then validate it and code decides what counts)",
                      text.replace("\n", " "))
        self.assertIn("of the fields the model filled in, the share that were right", text.replace("\n", " "))
        extras = (ROOT / "frontend/src/CheckSaleExtras.jsx").read_text(encoding="utf-8")
        self.assertIn("Gemini maps a seller sentence to a form item; fixed rules then validate it and code decides what counts.", extras)


class Channel3TreeTest(unittest.TestCase):
    def test_reference_block_counts_and_rows(self):
        tree = EXAMPLES["channel3_tree"]
        notes = (ROOT / tree["notes"]).read_text(encoding="utf-8").split("\n")
        self.assertIn(f"{tree['categories_read']:,} categories, read once", notes[tree["notes_line"] - 1])
        rows = list(csv.DictReader((ROOT / tree["csv"]).open(encoding="utf-8")))
        self.assertEqual(tree["mapped"], len(rows))
        self.assertEqual(len(rows), 191)
        lines = (ROOT / tree["csv"]).read_text(encoding="utf-8").split("\n")
        for example in tree["examples"]:
            row = rows[example["line"] - 2]
            self.assertEqual((row["channel3_category_path"], row["paypal_aup_item"], row["agreement"]),
                             (example["path"], example["paypal_aup_item"], example["agreement"]))
            self.assertIn(example["path"], lines[example["line"] - 1])
        self.assertTrue(tree["csv_url"].endswith("/" + tree["csv"]))


if __name__ == "__main__":
    unittest.main()
