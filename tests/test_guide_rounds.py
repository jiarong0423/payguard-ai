"""Rounds of the guided gap filling: deterministic first, the model last.

Stages (API field "stage"): funnel = sanitise, keyword routes and fixed-label inputs, no model call;
echo = values mapped from the seller's words are read back from the field values for Confirm / Change,
nothing is subtracted until the seller confirms; fill = the remaining gaps, up to three per round.
A round is one guide message asking up to three items plus one seller action (one Save of those fixed
inputs, or one typed sentence). Every valid pick is subtracted at once by validate_form_value; the model
only maps the seller's own words for items that are still open.

Run `GUIDE_ROUNDS_REPORT=1 python -m unittest tests.test_guide_rounds` to print the measured table.
"""

from datetime import datetime, timezone
import json
import math
import os
import socket
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.guide_routes import GuideService
from app.main import create_app
from app.store import SessionStore
from payguard import evidence_guide as eg
from payguard.controlled_fallback import Governor


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1/guide"
NOW = datetime(2026, 10, 30, 9, 0, tzinfo=timezone.utc)  # a Friday
TODAY = NOW.date()
DATA = Path(__file__).resolve().parent / "data"
SITUATIONS = (("preflight", None), ("velocity", None), ("dispute", "physical"), ("dispute", "digital"))
GOOD_TEXT = {"product": "Ceramic coffee cups", "tracking_number": "1Z999AA10123456784"}


class Clock:
    def __call__(self):
        return 1000.0


class CountingModel:
    """A model chooser stand-in: answers from a reply function and records every request it receives."""

    def __init__(self, answer=lambda request: json.dumps({"v": 2, "u": []})):
        self.answer, self.requests = answer, []

    def __call__(self, request):
        self.requests.append(json.loads(json.dumps(request)))
        return self.answer(request)


def good_value(item, form, prefill):
    if item in prefill:
        return prefill[item]
    if form["kind"] == "choice":
        return next(option["value"] for option in form["options"] if option["value"] not in eg.DEFERRING_VALUES)
    if form["kind"] == "date":
        return TODAY.isoformat()
    return GOOD_TEXT[item]


class Guide:
    def __init__(self, test, model, scenario="dispute", goods="physical"):
        self.test, self.model = test, model
        store = SessionStore(clock=lambda: NOW)
        self.app = create_app(store=store)
        self.app.state.guide = GuideService(store, chooser_factory=lambda: model, governor=Governor(clock=Clock(), min_spacing=0), rule_confirm=False)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55020))
        session = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        self.view = self.post("/start", {"scenario": scenario, "goods_type": goods})

    def post(self, path, body):
        response = self.client.post(ROOT + path, json=body, headers=self.headers)
        self.test.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def say(self, text):
        self.post("/turn", {"text": text})
        self.app.state.guide.wait_for_analysis()
        self.view = self.client.get(ROOT + "/state", headers=self.headers).json()
        return self.view

    def save(self, answers):
        self.view = self.post("/form", {"fields": [{"item": item, "value": value} for item, value in answers]})
        return self.view

    def forms(self):
        return {item["id"]: item["form"] for item in self.view["items"]}

    def pick_round(self, override=None):
        """The seller fills every asked item with a valid fixed input (or an override) and presses Save once."""
        forms = self.forms()
        answers = [(item, (override or {}).get(item) or good_value(item, forms[item], self.view["prefill"])) for item in self.view["asked"]]
        return self.save(answers)

    def finish_by_picking(self, limit=10):
        while self.view["stage"] != "done" and limit:
            self.pick_round()
            limit -= 1
        return self.view

    @staticmethod
    def status(view, slot):
        return next(item["status"] for item in view["items"] if item["id"] == slot)


def applicable(scenario, goods):
    return len(eg.slots_for(scenario, goods)) if scenario == "dispute" else len(eg.SCENARIOS[scenario]["slots"])


def recorded_reply(raw_v1, full_clauses):
    """A recorded contract-1 reply replayed through the live contract-2 path: tags default to SELLER / STATED
    (contract 1 had no tags) and clause indices follow the clauses that were actually sent."""
    def answer(request):
        rows = []
        for row in raw_v1["u"]:
            clause = full_clauses[row["k"]] if row["k"] < len(full_clauses) else None
            if clause in request["clauses"] and row["c"] in request["slots"]:
                rows.append(dict(row, k=request["clauses"].index(clause), b="STATED", a="SELLER"))
        return json.dumps({"v": 2, "u": rows})
    return answer


def gold_reply(item):
    """An oracle with the corpus' gold mapping, standing in for a model whose mapping is right."""
    def answer(request):
        rows = [{"c": slot, "k": 0, "s": "P", "w": item["gold_w"], "r": item["gold_r"], "h": item["gold_h"], "b": "STATED", "a": "SELLER"}
                for slot in item["gold_slots"] if slot in request["slots"]][:eg.MAX_INCREMENTS]
        return json.dumps({"v": 2, "u": rows})
    return answer


class StageATests(unittest.TestCase):
    def setUp(self):
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    def test_every_required_item_has_a_fixed_input_next_to_scenarios(self):
        for scenario, spec in eg.SCENARIOS.items():
            self.assertEqual(set(eg.FIXED_INPUTS[scenario]), set(spec["slots"]), scenario)
        dispute = eg.FIXED_INPUTS["dispute"]
        self.assertEqual([o["value"] for o in dispute["carrier"]["options"]], ["UPS", "USPS", "FedEx", "DHL", "other"])
        self.assertEqual(dispute["ship_date"]["kind"], "date")
        self.assertEqual(dispute["tracking_number"]["kind"], "text")
        for item in ("delivery_record", "refund_record", "buyer_comms"):
            self.assertEqual([o["value"] for o in dispute[item]["options"]], ["yes", "no", "not_sure"], item)
        self.assertEqual([o["value"] for o in dispute["address_match"]["options"]], ["yes", "no"])

    def test_picking_every_fixed_input_finishes_with_zero_model_calls(self):
        for scenario, goods in SITUATIONS:
            with self.subTest(scenario=scenario, goods=goods):
                model = CountingModel()
                guide = Guide(self, model, scenario, goods)
                needed = applicable(scenario, goods)
                self.assertEqual(guide.view["subtraction"]["text"], f"{needed} items needed · 0 taken from what you wrote · {needed} left")
                self.assertEqual(len(guide.view["asked"]), min(3, needed))
                view = guide.finish_by_picking()
                self.assertEqual(view["stage"], "done")
                self.assertEqual(view["reply"]["template"], "DONE")
                self.assertEqual(view["rounds_used"], math.ceil(needed / 3))
                self.assertEqual(view["subtraction"], {"needed": needed, "taken": needed, "left": 0,
                                                       "text": f"{needed} items needed · {needed} taken from what you wrote · 0 left"})
                self.assertEqual(model.requests, [])

    def test_the_nine_item_dispute_set_needs_at_most_three_rounds(self):
        # physical goods: 7 applicable items; digital: 4. Both are subsets of the 9 dispute items.
        for goods, rounds in (("physical", 3), ("digital", 2)):
            guide = Guide(self, CountingModel(), "dispute", goods)
            self.assertLessEqual(guide.finish_by_picking()["rounds_used"], rounds)

    def test_each_round_asks_up_to_three_items_in_priority_order_and_subtracts_at_once(self):
        guide = Guide(self, CountingModel())
        self.assertEqual(guide.view["asked"], ["ship_date", "carrier", "tracking_number"])
        self.assertEqual(guide.view["reply"]["template"], "REQUEST_MANY")
        self.assertIn("ship date, carrier and tracking number", guide.view["reply"]["text"])
        view = guide.save([("ship_date", TODAY.isoformat()), ("carrier", "UPS"), ("tracking_number", "abc")])
        self.assertEqual([r["valid"] for r in view["form_results"]], [True, True, False])
        self.assertEqual(view["subtraction"]["text"], "7 items needed · 2 taken from what you wrote · 5 left")
        self.assertEqual(view["asked"], ["tracking_number", "delivery_record", "address_match"])  # the invalid one is asked again

    def test_form_request_shapes(self):
        guide = Guide(self, CountingModel())
        bad = [{"fields": []}, {"fields": [{"item": "carrier", "value": "UPS"}] * 2},
               {"fields": [{"item": s, "value": "x"} for s in ("ship_date", "carrier", "tracking_number", "refund_record")]},
               {"item": "carrier"}, {"item": "carrier", "value": "UPS", "fields": [{"item": "carrier", "value": "UPS"}]},
               {"fields": [{"item": "carrier", "value": "UPS"}, {"item": "delivery_channel", "value": "email"}]}]
        for body in bad:
            with self.subTest(body=str(body)[:60]):
                self.assertEqual(guide.client.post(ROOT + "/form", json=body, headers=guide.headers).status_code, 422)
        self.assertEqual(guide.status(guide.client.get(ROOT + "/state", headers=guide.headers).json(), "carrier"), "MISSING")


class StageBTests(unittest.TestCase):
    def setUp(self):
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    def test_not_sure_routes_the_item_to_fill_then_the_model_mapping_is_echoed_for_confirmation(self):
        ship = {"c": "ship_date", "k": 0, "s": "P", "w": "MON", "r": "LAST", "h": "EXACT", "b": "STATED", "a": "SELLER"}
        model = CountingModel(lambda request: json.dumps({"v": 2, "u": [ship] if "ship_date" in request["slots"] else []}))
        guide = Guide(self, model)
        view = guide.save([("ship_date", "not_sure"), ("carrier", "UPS"), ("tracking_number", "1Z999AA10123456784")])
        self.assertEqual(view["deferred"], ["ship_date"])
        self.assertEqual(view["form_results"][0], {"item": "ship_date", "valid": False, "deferred": True})
        self.assertEqual(guide.status(view, "ship_date"), "MISSING")
        self.assertEqual(view["stage"], "funnel")
        self.assertNotIn("ship_date", view["asked"])  # the funnel first; the deferred item waits for fill
        guide.pick_round()
        guide.pick_round()
        view = guide.view
        self.assertEqual((view["stage"], view["asked"], view["reply"]["template"]), ("fill", ["ship_date"], "DESCRIBE"))
        self.assertEqual(model.requests, [])  # no model call in the funnel
        view = guide.say("I handed it over last Monday")
        self.assertEqual(len(model.requests), 1)
        self.assertEqual(model.requests[0]["slots"], {"ship_date": "MISSING"})  # only still-open items
        self.assertEqual(view["prefill"], {"ship_date": "2026-10-19"})
        self.assertEqual(guide.status(view, "ship_date"), "PARTIAL")  # pre-filled, not present
        self.assertEqual((view["stage"], view["asked"], view["reply"]["template"]), ("echo", ["ship_date"], "ECHO"))
        self.assertEqual(view["reply"]["text"], "You said: ship date 2026-10-19. Is that right? Confirm, or change any of them.")
        view = guide.pick_round()  # Confirm: the seller saves the echoed value
        self.assertEqual(view["stage"], "done")
        self.assertEqual(view["gap"]["present"], ["ship_date", "carrier", "tracking_number", "delivery_record", "address_match",
                                                  "buyer_comms", "refund_record"])

    def test_an_unconfirmed_echo_never_marks_an_item_present(self):
        rows = [{"c": "ship_date", "k": 0, "s": "P", "w": "MON", "r": "LAST", "h": "EXACT", "b": "STATED", "a": "SELLER"},
                {"c": "carrier", "k": 0, "s": "P", "w": None, "r": None, "h": "EXACT", "b": "STATED", "a": "SELLER"}]
        guide = Guide(self, CountingModel(lambda request: json.dumps({"v": 2, "u": [r for r in rows if r["c"] in request["slots"]]})))
        view = guide.say("I handed it to UPS last Monday")
        # The two confirmations come first and the spare slot carries the next open item (no wasted slot).
        self.assertEqual((view["stage"], view["asked"]), ("echo", ["ship_date", "carrier", "tracking_number"]))
        self.assertEqual(view["reply"]["text"], "You said: ship date 2026-10-19, carrier UPS. Is that right? Confirm, or change any of them.")
        self.assertNotIn("handed", view["reply"]["text"])
        for action in ("say", "other_fields", "state", "not_sure_then_say"):
            if action == "say":
                view = guide.say("I handed it to UPS last Monday")
            elif action == "other_fields":
                view = guide.save([("delivery_record", "yes"), ("refund_record", "no")])
            elif action == "state":
                view = guide.client.get(ROOT + "/state", headers=guide.headers).json()
            else:
                guide.save([("carrier", "not_sure")])
                view = guide.say("I handed it to UPS last Monday")
            for slot in ("ship_date", "carrier"):
                self.assertNotEqual(guide.status(view, slot), "STRUCTURALLY_PRESENT", (action, slot))
            self.assertNotIn("ship_date", view["gap"]["present"])
        view = guide.save([("ship_date", "2026-10-21"), ("carrier", "UPS")])  # Change one value, confirm the other
        self.assertEqual([r["valid"] for r in view["form_results"]], [True, True])
        self.assertIn("ship_date", view["gap"]["present"])
        self.assertEqual(view["prefill"], {})

    def test_model_requests_never_contain_settled_items(self):
        model = CountingModel()
        guide = Guide(self, model)
        guide.pick_round()  # ship date, carrier and tracking number settled
        settled = set(guide.view["gap"]["present"])
        for text in ("I have the delivery confirmation", "I messaged them on PayPal last Tuesday", "I did not refund anything"):
            guide.say(text)
        self.assertTrue(model.requests)
        for request in model.requests:
            self.assertFalse(settled & set(request["slots"]), request["slots"])
            self.assertFalse(any(status == "STRUCTURALLY_PRESENT" for status in request["slots"].values()))

    def test_a_model_reply_naming_a_settled_item_is_refused(self):
        carrier = {"c": "carrier", "k": 0, "s": "P", "w": None, "r": None, "h": "EXACT", "b": "STATED", "a": "SELLER"}
        model = CountingModel(lambda request: json.dumps({"v": 2, "u": [carrier]}))
        guide = Guide(self, model)
        guide.pick_round()
        view = guide.say("I handed the parcel over at the counter")
        self.assertEqual(view["analysis"]["status"], "kept")
        self.assertEqual(view["analysis"]["reason"], "invalid_reply")
        self.assertEqual(guide.status(view, "carrier"), "STRUCTURALLY_PRESENT")

    def test_the_model_never_marks_present_and_a_carrier_name_prefills_the_pick_list(self):
        rows = [{"c": slot, "k": 0, "s": "P", "w": None, "r": None, "h": "EXACT", "b": "STATED", "a": "SELLER"} for slot in ("carrier",)]
        guide = Guide(self, CountingModel(lambda request: json.dumps({"v": 2, "u": rows})))
        view = guide.say("I handed it to fedex")
        self.assertEqual(view["prefill"], {"carrier": "FedEx"})
        self.assertEqual(view["gap"]["present"], [])
        self.assertEqual(view["subtraction"]["taken"], 0)


def measure_sentence_first(item, model):
    """Seller describes the case first, then fills each asked round with valid picks (pre-filled values kept)."""
    class Probe(unittest.TestCase):
        def runTest(self):
            pass
    probe = Probe()
    guide = Guide(probe, model, item["scenario"], item["goods"])
    needed = guide.view["subtraction"]["needed"]
    guide.say(item["text"])
    view = guide.view
    prefilled = len(view["prefill"])
    mentioned = len(view["gap"]["partial"]) + len(view["gap"]["conflicting"])
    left = view["subtraction"]["left"]
    after_sentence = view["rounds_used"]
    guide.finish_by_picking()
    return {"id": item["id"], "group": item.get("group", "recorded held-out v2 sentence"), "needed": needed, "mentioned": mentioned, "prefilled": prefilled,
            "subtracted_by_sentence": needed - left, "left_after_sentence": left,
            "rounds": guide.view["rounds_used"], "formula": after_sentence + eg.expected_rounds(left),
            "model_calls": len(model.requests) if model is not None else 0, "done": guide.view["stage"] == "done"}


def corpus(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))["items"]


class SentenceFirstMeasurementTests(unittest.TestCase):
    """Held-out v4 sentences with the keyword chooser and with a gold-mapping oracle, and the seven recorded
    model replies; the formula rounds = 1 + ceil(left / 3) holds on every case."""

    def setUp(self):
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    def rows(self):
        rows = []
        for item in corpus("evidence_guide_heldout_v4.json"):
            rows.append(dict(measure_sentence_first(item, None), chooser="keyword"))
            rows.append(dict(measure_sentence_first(item, CountingModel(gold_reply(item))), chooser="gold oracle"))
        recorded = json.loads((DATA / "recorded_replies_v1.json").read_text(encoding="utf-8"))["replies"]
        v2 = {item["id"]: item for item in corpus("evidence_guide_heldout_v2.json")}
        for item_id, raw in sorted(recorded.items()):
            item = v2[item_id]
            cleaned, _ = eg.sanitize_input(item["text"])
            clauses = eg.split_clauses(cleaned) if cleaned else []
            rows.append(dict(measure_sentence_first(item, CountingModel(recorded_reply(raw, clauses))), chooser="recorded v1 reply"))
        return rows

    def test_formula_and_completion_on_every_case(self):
        rows = self.rows()
        self.assertEqual(len(rows), 36 * 2 + 7)
        for row in rows:
            self.assertTrue(row["done"], row)
            self.assertEqual(row["rounds"], row["formula"], row)
            self.assertEqual(row["subtracted_by_sentence"], 0, row)  # text never settles an item; it pre-fills
        for row in rows:
            if row["chooser"] == "keyword":
                self.assertEqual(row["model_calls"], 0)
        # Pressure and other-party sentences: whether or not a phrasing slips past the routes and the grammar filter,
        # nothing from them is ever echoed (pre-filled) or present. A few unusual phrasings ("A customer wrote ...",
        # "My bookkeeper advised ...") are still marked "mentioned" by the keyword baseline; that count is reported.
        pressure_or_other = [row for row in rows if row["group"].startswith(("pressure", "buyer", "third-party"))]
        self.assertEqual(len(pressure_or_other), 18 * 2)
        for row in pressure_or_other:
            self.assertEqual(row["prefilled"], 0, row)
        if os.environ.get("GUIDE_ROUNDS_REPORT") == "1":
            print_report(rows)


def print_report(rows):
    print()
    print(f"{'chooser':<18} {'group':<44} {'n':>3} {'needed':>6} {'mentioned':>9} {'prefilled':>9} {'rounds':>6} {'model calls':>11}")
    groups = {}
    for row in rows:
        groups.setdefault((row["chooser"], row["group"]), []).append(row)
    for (chooser, group), items in sorted(groups.items()):
        n = len(items)
        mean = lambda key: sum(row[key] for row in items) / n  # noqa: E731
        print(f"{chooser:<18} {group:<44} {n:>3} {mean('needed'):>6.2f} {mean('mentioned'):>9.2f} {mean('prefilled'):>9.2f} "
              f"{mean('rounds'):>6.2f} {mean('model_calls'):>11.2f}")
    for chooser in sorted({row["chooser"] for row in rows}):
        items = [row for row in rows if row["chooser"] == chooser]
        n = len(items)
        print(f"{chooser:<18} {'ALL':<44} {n:>3} {sum(r['needed'] for r in items) / n:>6.2f} "
              f"{sum(r['mentioned'] for r in items) / n:>9.2f} {sum(r['prefilled'] for r in items) / n:>9.2f} "
              f"{sum(r['rounds'] for r in items) / n:>6.2f} {sum(r['model_calls'] for r in items) / n:>11.2f}")


if __name__ == "__main__":
    unittest.main()
