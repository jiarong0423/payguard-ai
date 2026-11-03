"""The replayable examples must match a fresh build, label their source honestly, and never overstate."""

import hashlib
import json
import pathlib
import sys
import unittest

from payguard import evidence_guide as eg

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPLAYS = ROOT / "frontend" / "src" / "data" / "guide_replays_v1.json"
RECORDED_SHA256 = "1592c1088e38c12c8beabf17df3f1e7d56336f32d4c062ee5ce595c80c7bbdec"
sys.path.insert(0, str(ROOT / "tools"))
import build_replays  # noqa: E402


class Replays(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(REPLAYS.read_text(encoding="utf-8"))
        self.steps = [(s, step) for s in self.document["scenarios"] for step in s["steps"]]

    def test_committed_file_matches_a_fresh_build(self):
        self.assertEqual(REPLAYS.read_text(encoding="utf-8"), build_replays.render(build_replays.build()))

    def test_label_says_never_a_live_call(self):
        self.assertIn("Never a live model call", self.document["label"])

    def test_all_three_situations_are_covered(self):
        self.assertEqual({s["situation"] for s in self.document["scenarios"]}, {"preflight", "velocity", "dispute"})

    def test_every_model_step_names_its_kind_and_source(self):
        for scenario, step in self.steps:
            if step["model_called"]:
                self.assertIn(step["reply_kind"], ("recorded", "authored"))
                self.assertIsNotNone(step["reply"])
                self.assertIn("model", step["reply_from"])
            else:
                self.assertIsNone(step["reply_kind"])
                self.assertIsNone(step["reply"])
                self.assertIsNone(step["reply_from"])

    def test_authored_replies_are_labelled_as_not_a_model_run(self):
        authored = json.loads((ROOT / "tests" / "data" / "authored_replies_v1.json").read_text())
        self.assertIn("NOT a model run", authored["source"]["path"])
        for step in (st for _, st in self.steps if st["reply_kind"] == "authored"):
            self.assertIn("NOT a model run", step["reply_from"]["path"])

    def test_every_reply_passes_the_same_strict_validator_under_its_own_contract(self):
        for scenario, step in self.steps:
            if step["model_called"]:
                self.assertEqual(step["reply_contract"], step["reply"]["v"], scenario["id"])
                self.assertIsNotNone(eg.validate_increments(json.dumps(step["reply"]), scenario["situation"], step["reply_contract"]),
                                     scenario["id"])
            else:
                self.assertIsNone(step["reply_contract"])
                self.assertIsNone(step["reply_note"])

    def test_every_authored_reply_file_entry_is_contract_2(self):
        authored = json.loads((ROOT / "tests" / "data" / "authored_replies_v1.json").read_text())
        scenarios = {"p-": "preflight", "v-": "velocity"}
        self.assertTrue(authored["replies"])
        for key, reply in authored["replies"].items():
            situation = scenarios[key[:2]]
            raw = json.dumps(reply, separators=(",", ":"))
            self.assertEqual(reply["v"], 2, key)
            self.assertLessEqual(len(reply["u"]), eg.MAX_INCREMENTS, key)
            self.assertLessEqual(len(raw.encode("ascii")), eg.MAX_CHOOSER_BYTES, key)
            self.assertTrue(all(set(row) == set("cksawrhb") for row in reply["u"]), key)
            self.assertIsNotNone(eg.validate_increments(raw, situation, 2), key)
            self.assertIsNone(eg.validate_increments(raw, situation, 1), key)  # really contract 2, not contract 1
        for step in (st for _, st in self.steps if st["reply_kind"] == "authored"):
            self.assertEqual((step["reply_contract"], step["reply_note"]), (2, None))

    def test_recorded_replies_are_never_edited_and_old_format_ones_say_so(self):
        recorded_file = ROOT / "tests" / "data" / "recorded_replies_v1.json"
        # Pinned to the file as captured from the real model run; any edit must fail here.
        self.assertEqual(hashlib.sha256(recorded_file.read_bytes()).hexdigest(), RECORDED_SHA256)
        recorded = json.loads(recorded_file.read_text())
        for step in (st for _, st in self.steps if st["reply_kind"] == "recorded"):
            self.assertIn(step["reply"], recorded["replies"].values())
            self.assertEqual(step["reply_contract"], step["reply"]["v"])
            if step["reply_contract"] == 1:
                self.assertEqual(step["reply_note"], build_replays.RECORDED_V1_NOTE)
                self.assertTrue(all("b" not in row and "a" not in row for row in step["reply"]["u"]))
            else:
                self.assertIsNone(step["reply_note"])

    def test_assistant_text_comes_from_the_fixed_templates_and_is_clean(self):
        for scenario, step in self.steps:
            lowered = (step["assistant_text"] or "").casefold().replace("can't guarantee", "cannot promise")
            for word in eg.FORBIDDEN_WORDS:
                self.assertNotIn(word, lowered, scenario["id"])
            self.assertIn(step["template"], eg.TEMPLATES)

    def test_routes_and_gates_never_call_the_model(self):
        by_id = {s["id"]: s for s in self.document["scenarios"]}
        self.assertFalse(by_id["english-only-gate"]["steps"][0]["model_called"])
        self.assertFalse(by_id["pressure-gets-no-shortcut"]["steps"][1]["model_called"])
        self.assertFalse(by_id["spike-pressure"]["steps"][0]["model_called"])
        self.assertEqual(by_id["spike-pressure"]["steps"][0]["template"], "REFUSE")

    def test_no_replay_step_names_another_situation_in_a_refusal(self):
        for scenario, step in self.steps:
            if step["template"] == "REFUSE":
                self.assertNotIn("dispute", step["assistant_text"].casefold())

    def test_nothing_is_ever_reported_present_by_a_replay(self):
        for scenario, step in self.steps:
            self.assertEqual(step["gap"]["present"], [], scenario["id"])

    def test_done_is_never_shown_while_required_items_are_only_partial(self):
        for scenario, step in self.steps:
            self.assertNotEqual(step["template"], "DONE", scenario["id"])

    def test_every_item_row_names_its_source_and_official_rows_name_a_chunk(self):
        for scenario, step in self.steps:
            self.assertEqual([i["id"] for i in step["items"]], scenario["required_items"], scenario["id"])
            for item in step["items"]:
                self.assertIn(item["source"], (eg.OFFICIAL, eg.SUGGESTION))
                self.assertEqual(item["source"] == eg.OFFICIAL, item["chunk"] is not None, item["id"])
                self.assertIn(item["status"], eg.STATUSES)
                self.assertNotEqual(item["status"], "STRUCTURALLY_PRESENT", scenario["id"])

    def test_conflicting_days_become_a_question(self):
        scenario = [s for s in self.document["scenarios"] if s["id"] == "two-different-days"][0]
        self.assertEqual(scenario["steps"][-1]["template"], "CONFLICT")

    def test_preflight_never_asks_the_model_for_the_rule_only_signal(self):
        for scenario in (s for s in self.document["scenarios"] if s["situation"] == "preflight"):
            self.assertNotIn("category_signal", scenario["required_items"])


class EmptyRequiredSet(unittest.TestCase):
    def test_an_empty_required_set_is_an_error_not_done(self):
        state = eg.new_state("dispute", "digital")
        eg.choose_goods_type(state, "digital")
        with self.assertRaises(ValueError):
            eg.next_message(state, required=("carrier", "tracking_number"))

    def test_done_needs_every_required_item_present(self):
        state = eg.new_state("dispute", "digital")
        eg.choose_goods_type(state, "digital")
        required = ("delivery_channel", "delivered_at")
        self.assertNotEqual(eg.next_message(state, required)[0], "DONE")
        for slot in required:
            eg.apply_form(state, slot, True)
        self.assertEqual(eg.next_message(state, required)[0], "DONE")


if __name__ == "__main__":
    unittest.main()
