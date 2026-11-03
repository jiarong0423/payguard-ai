"""Fuzzy case routing: typo-tolerant matching to a goods group, closed result, no outbound call by default."""

import json
import os
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.case_routing import CaseRouter, route_case, word_similarity
from app.channel3 import CallBudget, Channel3Config
from app.channel3_products import Channel3ProductAdapter
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore

ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"


def card(pid, title, category, features=(), materials=()):
    return {"product_id": pid, "title": title, "brand": None, "category": category, "key_features": list(features),
            "materials": list(materials), "image_url": None}


RECORDED = {
    "headphones": {"cards": [card("p1", "Sony WH-1000XM6 Wireless Noise Canceling Headphones", "Over-Ear Headphones")]},
    "bag": {"cards": [card("p2", "Leather Crossbody Bag", "Cross Body Bags", ("Adjustable strap",), ("Leather",))]},
    "puzzle": {"cards": [card("p3", "Chunky Wooden Forest Puzzle", "Wooden & Pegged Puzzles")]},
}


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.router = CaseRouter(RECORDED)

    def test_typos_still_route_to_the_catalogue_product(self):
        for text, product in (("wirless hedphones", "p1"), ("leather cross body bag", "p2"), ("kids wooden puzzel", "p3"),
                              ("Sony WH-1000XM6", "p1")):
            result = self.router.route(text)
            self.assertEqual((result["route"], result["reason"]), ("physical", "catalogue_match"), text)
            self.assertEqual(result["matches"][0]["product_id"], product, text)
            self.assertIn("tracking number", result["items"])

    def test_a_shared_adjective_alone_does_not_route(self):
        for text in ("handmade soap", "leather wallet", "vintage lamp"):
            result = self.router.route(text)
            self.assertEqual((result["route"], result["matches"], result["items"]), ("unknown", [], []), text)

    def test_digital_and_service_words_win_and_are_named(self):
        digital = self.router.route("ebok pdf guide")
        self.assertEqual((digital["route"], digital["matched_word"]), ("digital", "ebook"))
        self.assertIn("delivery channel", digital["items"])
        self.assertNotIn("tracking number", digital["items"])
        service = self.router.route("logo design commission")
        self.assertEqual((service["route"], service["matched_word"], service["items"]), ("service", "commission", []))

    def test_a_describing_word_does_not_route_physical_goods(self):
        # Q3: fuzzy or adjective matches sent these to digital or service, and the guide then asked for digital items.
        for text in ("digital camera", "steam mop", "travel plug adapter", "coarse sea salt", "license plate frame",
                     "cleaning cloth", "phone repair kit", "course grinder burr", "app-controlled smart plug"):
            result = self.router.route(text)
            self.assertNotIn(result["route"], ("digital", "service"), text)

    def test_the_thing_itself_still_routes(self):
        for text, route, word in (("online course", "digital", "course"), ("software licence key", "digital", "licence"),
                                  ("photoshop presets", "digital", "preset"), ("mp3 album", "digital", "mp3"),
                                  ("guitar lessons", "service", "lesson"), ("phone repair", "service", "repair")):
            result = self.router.route(text)
            self.assertEqual((result["route"], result["matched_word"]), (route, word), text)

    def test_personal_details_are_removed_before_matching(self):
        result = self.router.route("headphones for Jane Smith 555-123-4567 jane@example.com")
        self.assertEqual(result["query"], "headphones")
        self.assertEqual(self.router.route("555-123-4567")["reason"], "nothing_to_match")

    def test_result_is_closed_and_advisory(self):
        result = self.router.route("wireless headphones")
        self.assertEqual(set(result), {"query", "route", "reason", "matched_word", "matches", "filtered_out", "items", "decided_by", "affects_decision"})
        self.assertEqual((result["decided_by"], result["affects_decision"]), ("code", False))
        self.assertLessEqual(len(result["matches"]), 3)

    def test_word_similarity_is_symmetric_and_bounded(self):
        for a, b in (("puzzel", "puzzle"), ("soap", "strap"), ("bag", "bag")):
            self.assertEqual(word_similarity(a, b), word_similarity(b, a))
            self.assertTrue(0 <= word_similarity(a, b) <= 1)

    def test_recorded_catalogue_file_loads(self):
        self.assertGreater(len(CaseRouter().catalogue), 0)


class PreciseFilterTests(unittest.TestCase):
    def setUp(self):
        self.router = CaseRouter({"bottles": {"cards": [
            card("b32", "BOXRAW 32oz Steel Water Bottle", "Water Bottles", materials=("Stainless steel",)),
            card("b24", "Sport Water Bottle 24 oz", "Water Bottles"),
            card("bplain", "Water Bottle", "Water Bottles")]},
            "phones": {"cards": [card("xm6", "Sony WH-1000XM6 Headphones", "Over-Ear Headphones"),
                                 card("xm4", "Sony WH-1000XM4C Headphones", "Over-Ear Headphones")]}})

    def test_a_contradicting_size_or_model_is_filtered_out(self):
        result = self.router.route("Sony WH-1000XM6")
        self.assertEqual([m["product_id"] for m in result["matches"]], ["xm6"])
        self.assertEqual((result["matches"][0]["match_type"], result["filtered_out"]), ("exact", 1))

    def test_number_and_unit_are_compared_as_one_size(self):
        result = self.router.route("water bottle 32 oz")
        self.assertEqual(result["matches"][0]["product_id"], "b32")
        self.assertIn("32oz", result["matches"][0]["exact_words"])
        self.assertNotIn("b24", [m["product_id"] for m in result["matches"]])

    def test_only_the_most_exact_candidates_survive(self):
        result = self.router.route("stainles steel water botle")
        self.assertEqual([m["product_id"] for m in result["matches"]], ["b32"])
        self.assertEqual(result["matches"][0]["match_type"], "close")

    def test_when_every_candidate_conflicts_the_seller_is_told(self):
        result = self.router.route("Sony WH-1000XM9")
        self.assertEqual((result["route"], result["reason"], result["matches"]), ("unknown", "filtered_conflict", []))
        self.assertEqual(result["filtered_out"], 2)


class LiveFallbackTests(unittest.TestCase):
    def live(self, body):
        calls = []

        def transport(url, payload, headers, timeout):
            calls.append(payload)
            return 200, json.dumps(body).encode()
        return Channel3ProductAdapter(Channel3Config(enabled=True, api_key="c3-test-key-not-real"), transport=transport,
                                      budget=CallBudget(3)), calls

    def test_unknown_text_is_searched_live_only_when_a_key_is_configured(self):
        adapter, calls = self.live({"products": [{"id": "lamp1", "title": "Vintage Brass Table Lamp", "category": {"title": "Lamps"}}]})
        result = CaseRouter(RECORDED, products=adapter).route("vintage lamp")
        self.assertEqual((result["route"], result["reason"], result["matches"][0]["product_id"]), ("physical", "live_catalogue_match", "lamp1"))
        self.assertEqual(calls, [{"query": "vintage lamp", "limit": 3}])

    def lamp_adapter(self, shared=None):
        calls = []

        def transport(url, payload, headers, timeout):
            calls.append(payload)
            return 200, json.dumps({"products": [{"id": "lamp1", "title": "Vintage Brass Table Lamp"}]}).encode()
        return Channel3ProductAdapter(Channel3Config(enabled=True, api_key="c3-test-key-not-real"), transport=transport,
                                      budget=shared or CallBudget(20)), calls

    def test_routing_spends_its_own_budget_not_the_shared_one(self):
        shared = CallBudget(20)
        adapter, calls = self.lamp_adapter(shared)
        router = CaseRouter(RECORDED, products=adapter, budget=CallBudget(3), session_cap=10)
        routes = [router.route("vintage lamp", f"session-{index}")["reason"] for index in range(5)]
        self.assertEqual(routes, ["live_catalogue_match"] * 3 + ["no_close_match"] * 2)
        self.assertEqual((len(calls), router.budget.remaining, shared.remaining), (3, 0, 20),
                         "the listing check's shared budget is untouched")

    def test_one_session_cannot_exhaust_routing(self):
        adapter, calls = self.lamp_adapter()
        router = CaseRouter(RECORDED, products=adapter, budget=CallBudget(8), session_cap=2)
        greedy = [router.route("vintage lamp", "greedy")["reason"] for _ in range(6)]
        self.assertEqual(greedy, ["live_catalogue_match"] * 2 + ["no_close_match"] * 4)
        self.assertEqual(router.route("vintage lamp", "polite")["reason"], "live_catalogue_match", "another session still gets a search")
        self.assertEqual((len(calls), router.budget.remaining), (3, 5))

    def test_defaults_are_small_and_separate(self):
        from app import case_routing
        router = CaseRouter(RECORDED)
        self.assertEqual((router.budget.limit, router.session_cap), (case_routing.ROUTE_CALL_BUDGET, case_routing.ROUTE_SESSION_CAP))
        self.assertLess(case_routing.ROUTE_CALL_BUDGET, 20)
        with self.assertRaises(ValueError):
            CaseRouter(RECORDED, session_cap=-1)

    def test_known_text_never_calls_out(self):
        adapter, calls = self.live({"products": []})
        CaseRouter(RECORDED, products=adapter).route("wireless headphones")
        self.assertEqual(calls, [])

    def test_recorded_or_off_adapters_never_call_out(self):
        off = Channel3ProductAdapter(Channel3Config(enabled=False), transport=lambda *_: (_ for _ in ()).throw(AssertionError("called")))
        self.assertEqual(CaseRouter(RECORDED, products=off).route("vintage lamp")["route"], "unknown")


class RouteApiTests(unittest.TestCase):
    def setUp(self):
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(
            lambda request: (_ for _ in ()).throw(AssertionError("no provider call"))))
        with patch.dict(os.environ, {}, clear=True):
            self.app = create_app(store=SessionStore(), paypal=provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55003), raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def post(self, payload, session=True):
        headers = {"Origin": ORIGIN}
        if session:
            headers.update({"X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]})
        return self.client.post(ROOT + "/cases/route", json=payload, headers=headers)

    def test_route_endpoint_returns_the_closed_result(self):
        response = self.post({"text": "wirless hedphones"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["route"], "physical")

    def test_route_endpoint_validates_input_and_session(self):
        self.assertEqual(self.post({"text": ""}).status_code, 422)
        self.assertEqual(self.post({"text": "x" * 201}).status_code, 422)
        self.assertEqual(self.post({"text": "bag", "extra": 1}).status_code, 422)
        self.assertIn(self.post({"text": "bag"}, session=False).status_code, (401, 403))

    def test_drifting_router_is_replaced_by_an_error(self):
        class Drifting:
            def route(self, _text, _session_id=None):
                return {"route": "physical", "decision": "WIN"}
        self.app.state.case_router = Drifting()
        self.assertEqual(self.post({"text": "bag"}).status_code, 502)

    def test_route_endpoint_charges_live_searches_to_the_calling_session(self):
        seen = []
        real = self.app.state.case_router

        class Recording:
            def route(self, text, session_id=None):
                seen.append(session_id)
                return real.route(text, session_id)
        self.app.state.case_router = Recording()
        self.assertEqual(self.post({"text": "wirless hedphones"}).status_code, 200)
        self.assertEqual(seen, [self.session["session_id"]])


if __name__ == "__main__":
    unittest.main()
