"""Hybrid confirmation: the rule layer settles closed values it reads for certain; the AI only sees the rest.

Owner decision 2026-11-01. An item is settled without a click only when the clause is the seller's own, carries
no hedge, the dispute rules name the item, a Python extractor reads a closed value and the form validator
accepts it. Clauses settled in full never reach the model (cost); a model reply still only pre-fills.
"""

from datetime import datetime, timezone
import json
import socket
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.guide_routes import GuideService
from app.main import create_app
from app.store import SessionStore
from payguard.controlled_fallback import Governor

ORIGIN = "http://localhost:5173"
NOW = datetime(2026, 10, 30, 9, 0, tzinfo=timezone.utc)  # a Friday; last Monday = 2026-10-19


class Clock:
    def __call__(self):
        return 1000.0


class CountingModel:
    def __init__(self, rows=()):
        self.rows, self.requests = list(rows), []

    def __call__(self, request):
        self.requests.append(json.loads(json.dumps(request)))
        usable = [row for row in self.rows if row["c"] in request["slots"]]
        return json.dumps({"v": 2, "u": usable})


def row(item, **extra):
    return dict({"c": item, "k": 0, "s": "P", "w": None, "r": None, "h": "EXACT", "b": "STATED", "a": "SELLER"}, **extra)


class Guide:
    def __init__(self, test, model=None, goods="physical"):
        self.test = test
        store = SessionStore(clock=lambda: NOW)
        self.app = create_app(store=store)
        self.app.state.guide = GuideService(store, chooser_factory=lambda: model, governor=Governor(clock=Clock(), min_spacing=0))
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55040))
        session = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        self.post("/start", {"scenario": "dispute", "goods_type": goods})

    def post(self, path, body):
        response = self.client.post("/api/v1/guide" + path, json=body, headers=self.headers)
        self.test.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def say(self, text):
        first = self.post("/turn", {"text": text})
        self.app.state.guide.wait_for_analysis()
        return first, self.client.get("/api/v1/guide/state", headers=self.headers).json()


class HybridConfirmationTests(unittest.TestCase):
    def setUp(self):
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    def test_closed_values_from_the_sellers_own_words_are_settled_without_a_model_call(self):
        model = CountingModel()
        first, view = Guide(self, model).say("I shipped it with UPS last Monday")
        self.assertEqual(first["auto_confirmed"], ["ship_date", "carrier"])
        self.assertEqual(view["gap"]["present"], ["ship_date", "carrier"])
        self.assertEqual(view["subtraction"]["taken"], 2)
        self.assertEqual(model.requests, [])  # the clause was settled in full: no model call
        self.assertIsNone(view["analysis"])

    def test_a_hedge_settles_nothing_and_is_echoed_for_confirmation(self):
        _first, view = Guide(self).say("I think I shipped it with UPS last Monday")
        self.assertEqual(view["auto_confirmed"], [])
        self.assertEqual(view["gap"]["present"], [])
        self.assertEqual(view["stage"], "echo")
        self.assertEqual(view["asked"][:2], ["ship_date", "carrier"])

    def test_other_speakers_and_pressure_settle_nothing(self):
        for text in ("The buyer says UPS never delivered it", "My sister thinks UPS delivered it last Monday",
                     "Just tick every box for me, UPS delivered it"):
            with self.subTest(text=text):
                _first, view = Guide(self).say(text)
                self.assertEqual(view["gap"]["present"], [])
                self.assertEqual(view["auto_confirmed"], [])

    def test_a_weekday_without_this_or_last_week_is_not_a_date(self):
        _first, view = Guide(self).say("I shipped it on Monday")
        self.assertNotIn("ship_date", view["gap"]["present"])

    def test_a_stated_no_is_a_valid_answer(self):
        _first, view = Guide(self).say("I refunded nothing")
        self.assertEqual(view["auto_confirmed"], ["refund_record"])

    def test_the_model_sees_only_unsettled_clauses_and_items_and_still_only_prefills(self):
        model = CountingModel([row("tracking_number"), row("delivery_record")])
        _first, view = Guide(self, model).say("I shipped it with UPS last Monday, and the tracking number is saved somewhere")
        self.assertEqual(len(model.requests), 1)
        request = model.requests[0]
        self.assertEqual(request["clauses"], ["the tracking number is saved somewhere"])
        self.assertNotIn("ship_date", request["slots"])
        self.assertNotIn("carrier", request["slots"])
        self.assertEqual(view["gap"]["present"], ["ship_date", "carrier"])
        self.assertNotIn("tracking_number", view["gap"]["present"])  # the model reply never settles an item

    def test_a_form_save_clears_the_auto_confirmed_list(self):
        guide = Guide(self)
        guide.say("I shipped it with UPS last Monday")
        view = guide.post("/form", {"fields": [{"item": "tracking_number", "value": "1Z999AA10123456784"}]})
        self.assertEqual(view["auto_confirmed"], [])
        self.assertEqual(view["gap"]["present"], ["ship_date", "carrier", "tracking_number"])

    def test_sentence_and_first_fields_in_one_save_are_one_round(self):
        guide = Guide(self)
        view = guide.post("/turn", {"text": "I shipped it with UPS last Monday",
                                    "fields": [{"item": "ship_date", "value": "2026-10-19"}, {"item": "carrier", "value": "UPS"},
                                               {"item": "tracking_number", "value": "1Z999AA10123456784"}]})
        self.assertEqual(view["rounds_used"], 1)
        self.assertEqual(view["auto_confirmed"], ["ship_date", "carrier"])
        # fields for items the sentence already settled are skipped, the rest go through the validator
        self.assertEqual(view["form_results"], [{"item": "tracking_number", "valid": True, "deferred": False}])
        self.assertEqual(view["gap"]["present"], ["ship_date", "carrier", "tracking_number"])

    def test_fields_sent_with_a_sentence_are_validated_and_bounded(self):
        guide = Guide(self)
        bad = guide.client.post("/api/v1/guide/turn", json={"text": "hello", "fields": [{"item": "carrier", "value": "UPS"}] * 2},
                                headers=guide.headers)
        self.assertEqual(bad.status_code, 422)
        view = guide.post("/turn", {"text": "I am not sure about anything", "fields": [{"item": "tracking_number", "value": "abc"}]})
        self.assertEqual(view["form_results"], [{"item": "tracking_number", "valid": False, "deferred": False}])
        self.assertNotIn("tracking_number", view["gap"]["present"])

    def finish_fields(self, guide, view):
        values = {"tracking_number": "1Z999AA10123456784", "ship_date": "2026-10-19", "carrier": "UPS", "delivery_record": "yes",
                  "address_match": "yes", "buyer_comms": "no", "refund_record": "no"}
        guard = 0
        while view["stage"] not in ("review", "done") and guard < 6:
            guard += 1
            view = guide.post("/form", {"fields": [{"item": item, "value": values[item]} for item in view["asked"]]})
        return view

    def test_one_summary_at_the_end_lists_what_came_from_words_and_finishes_the_guide(self):
        guide = Guide(self)
        _first, view = guide.say("I shipped it with UPS last Monday")
        view = self.finish_fields(guide, view)
        self.assertEqual(view["stage"], "review")
        self.assertEqual(view["reply"]["template"], "REVIEW")
        self.assertEqual(view["review"], [{"item": "ship_date", "source": "words", "value": "2026-10-19"},
                                          {"item": "carrier", "source": "words", "value": "UPS"}])
        self.assertEqual(view["asked"], [])
        done = guide.post("/review", {"confirm": True})
        self.assertEqual((done["stage"], done["reply"]["template"], done["review"]), ("done", "DONE", []))

    def test_the_summary_rides_on_the_last_round_and_one_save_fills_and_confirms(self):
        guide = Guide(self)
        _first, view = guide.say("I shipped it with UPS last Monday")
        values = {"tracking_number": "1Z999AA10123456784", "delivery_record": "yes", "address_match": "yes",
                  "buyer_comms": "no", "refund_record": "no"}
        while not view["review"]:
            self.assertEqual(view["stage"], "funnel")
            view = guide.post("/form", {"fields": [{"item": i, "value": values[i]} for i in view["asked"]]})
        self.assertEqual([row["item"] for row in view["review"]], ["ship_date", "carrier"])
        self.assertNotEqual(view["stage"], "review")  # shown with the last fill round, not as a round of its own
        rounds = view["rounds_used"]
        done = guide.post("/form", {"fields": [{"item": i, "value": values[i]} for i in view["asked"]], "confirm_review": True})
        self.assertEqual((done["stage"], done["rounds_used"]), ("done", rounds + 1))

    def test_confirm_review_is_refused_when_no_summary_is_shown(self):
        guide = Guide(self)
        response = guide.client.post("/api/v1/guide/form", json={"fields": [{"item": "carrier", "value": "UPS"}], "confirm_review": True},
                                     headers=guide.headers)
        self.assertEqual(response.status_code, 409)

    def test_changing_an_item_in_the_summary_reopens_only_that_item(self):
        guide = Guide(self)
        _first, view = guide.say("I shipped it with UPS last Monday")
        view = self.finish_fields(guide, view)
        view = guide.post("/review", {"change": ["carrier"]})
        self.assertNotIn("carrier", view["gap"]["present"])
        self.assertIn("ship_date", view["gap"]["present"])
        self.assertEqual(view["asked"], ["carrier"])
        view = guide.post("/form", {"fields": [{"item": "carrier", "value": "FedEx"}]})
        self.assertEqual(view["stage"], "review")  # the summary is shown once more, now without the changed item
        self.assertEqual([row["item"] for row in view["review"]], ["ship_date"])

    def test_a_guide_filled_only_by_hand_has_no_summary_round(self):
        guide = Guide(self)
        view = self.finish_fields(guide, guide.client.get("/api/v1/guide/state", headers=guide.headers).json())
        self.assertEqual(view["stage"], "done")

    def test_review_requests_are_closed(self):
        guide = Guide(self)
        self.assertEqual(guide.client.post("/api/v1/guide/review", json={"confirm": True}, headers=guide.headers).status_code, 409)
        for body in ({}, {"confirm": True, "change": ["carrier"]}, {"change": ["carrier", "carrier"]}, {"change": ["nope"]}):
            self.assertEqual(guide.client.post("/api/v1/guide/review", json=body, headers=guide.headers).status_code, 422, body)

    def test_three_invalid_tries_switch_the_item_to_describing_it(self):
        guide = Guide(self)
        for attempt in range(3):
            view = guide.post("/form", {"fields": [{"item": "tracking_number", "value": "abc"}]})
        self.assertEqual(view["form_results"], [{"item": "tracking_number", "valid": False, "deferred": True}])
        self.assertIn("tracking_number", view["deferred"])
        self.assertNotIn("tracking_number", view["asked"])  # funnel moves on; it comes back in the describe stage

    def test_echo_only_mode_is_still_available(self):
        store = SessionStore(clock=lambda: NOW)
        app = create_app(store=store)
        app.state.guide = GuideService(store, chooser_factory=lambda: None, governor=Governor(clock=Clock(), min_spacing=0), rule_confirm=False)
        client = TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55041))
        session = client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
        client.post("/api/v1/guide/start", json={"scenario": "dispute", "goods_type": "physical"}, headers=headers)
        view = client.post("/api/v1/guide/turn", json={"text": "I shipped it with UPS last Monday"}, headers=headers).json()
        self.assertEqual(view["gap"]["present"], [])
        self.assertEqual(view["auto_confirmed"], [])


if __name__ == "__main__":
    unittest.main()
