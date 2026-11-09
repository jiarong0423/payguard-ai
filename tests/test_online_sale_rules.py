"""Shape checks for the online-sale rules file (a separate, unpinned file next to the pinned import/export rules)."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "country_rules" / "online_sale_rules_20261109.json"
PINNED = ROOT / "data" / "country_rules" / "paypal_country_rules_v1.json"


class OnlineSaleRulesTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_every_rule_has_source_and_dates(self):
        self.assertEqual(self.data["schema_version"], "payguard.online_sale_rules.v1")
        for rule in self.data["rules"]:
            for key in ("id", "country", "kind", "tag", "tier", "rule", "url", "agency", "read"):
                self.assertTrue(rule.get(key), (rule.get("id"), key))
            self.assertTrue(rule["url"].startswith("https://"), rule["id"])
            self.assertEqual(rule["kind"], "online_sale")
        ids = [r["id"] for r in self.data["rules"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_annex_has_nineteen_items(self):
        taiwan = next(r for r in self.data["rules"] if r["id"] == "TW-OS-MD-01")
        self.assertEqual(len(taiwan["annex_items"]), 19)
        self.assertEqual([i["no"] for i in taiwan["annex_items"]], list(range(1, 20)))

    def test_marketplace_policies_are_labelled_and_sourced(self):
        for item in self.data["marketplace_policies"]:
            self.assertTrue(item["url"].startswith("https://"), item["id"])
            self.assertTrue(item["rule"], item["id"])

    def test_no_id_overlaps_the_pinned_import_export_rules(self):
        pinned = json.loads(PINNED.read_text(encoding="utf-8"))
        pinned_ids = {r["id"] for side in ("import_rules", "export_rules") for v in pinned[side].values() for r in v["rules"]}
        self.assertFalse(pinned_ids & {r["id"] for r in self.data["rules"]})


if __name__ == "__main__":
    unittest.main()
