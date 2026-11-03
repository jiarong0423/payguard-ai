"""Channel3 product reference card: closed reduction, off by default, recorded replay, seller confirmation.

Every test uses a fake transport or a temporary recordings file. No test opens a network connection
or needs a real key. Reply bodies follow the ``SearchResponse`` / ``Product`` shape of the official
``channel3-sdk`` 4.6.0.
"""

import json
import os
import pathlib
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app import channel3_products
from app.channel3 import CallBudget, Channel3Config, Channel3Error
from app.channel3_products import (CARD_KEYS, ENDPOINT, Channel3ProductAdapter, build_channel3_product_adapter, card_digest,
                                   load_recorded, parse_search_response)
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore
from payguard.engines import check_aup


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
FAKE_KEY = "c3-test-key-not-real-0000"


def product(pid="prod_mug_1", title="Handmade Stoneware Coffee Mug, 12 oz", **extra):
    entry = {
        "id": pid, "title": title, "description": "Long merchant copy that is not kept.",
        "brands": [{"id": "b1", "name": "Clay Works"}],
        "images": [{"url": "http://cdn.example/plain.jpg", "is_main_image": False},
                   {"url": "https://cdn.example/main.jpg", "cleaned_url": "https://cdn.example/main-clean.png", "is_main_image": True}],
        "category": {"slug": "mugs", "title": "Mugs", "path": [{"slug": "kitchen", "title": "Kitchen"}], "has_children": False},
        "materials": ["Stoneware", "Glaze"], "key_features": ["Dishwasher safe", "12 oz capacity", "Hand thrown", "Lead free", "Fifth"],
        "offers": [{"url": "https://shop.example/buy?ref=1", "price": {"price": 24.0, "currency": "USD"}, "domain": "shop.example"}],
        "ratings": {"average": 4.7, "count": 120}, "gender": "unisex",
    }
    entry.update(extra)
    return entry


def search_body(*products):
    return json.dumps({"products": list(products), "next_page_token": None}).encode()


class FakeTransport:
    def __init__(self, status=200, body=None, exc=None):
        self.status, self.exc = status, exc
        self.body = search_body(product()) if body is None else body
        self.calls = []

    def __call__(self, url, body, headers, timeout):
        self.calls.append({"url": url, "body": dict(body), "headers": dict(headers), "timeout": timeout})
        if self.exc is not None:
            raise self.exc
        return self.status, self.body


def live_adapter(transport, budget=None):
    return Channel3ProductAdapter(Channel3Config(enabled=True, api_key=FAKE_KEY), transport=transport,
                                  budget=budget or CallBudget(5))


class ReductionTests(unittest.TestCase):
    def test_reply_is_reduced_to_closed_cards(self):
        cards = parse_search_response(search_body(product()))
        self.assertEqual(cards, [{
            "product_id": "prod_mug_1", "title": "Handmade Stoneware Coffee Mug, 12 oz", "brand": "Clay Works",
            "category": "Mugs", "key_features": ["Dishwasher safe", "12 oz capacity", "Hand thrown", "Lead free"],
            "materials": ["Stoneware", "Glaze"], "image_url": "https://cdn.example/main-clean.png"}])
        self.assertEqual(tuple(cards[0]), CARD_KEYS)

    def test_prices_offers_ratings_and_links_never_pass(self):
        text = json.dumps(parse_search_response(search_body(product())))
        for dropped in ("24.0", "shop.example", "ref=1", "4.7", "unisex", "merchant copy", "b1"):
            self.assertNotIn(dropped, text)

    def test_only_https_images_and_at_most_three_unique_products(self):
        plain = product("p2", images=[{"url": "http://cdn.example/x.jpg"}, {"url": "javascript:alert(1)"}])
        cards = parse_search_response(search_body(product("p1"), plain, product("p1"), product("p3"), product("p4")))
        self.assertEqual([card["product_id"] for card in cards], ["p1", "p2"])
        self.assertIsNone(cards[1]["image_url"])

    def test_optional_fields_may_be_absent(self):
        bare = {"id": "p9", "title": "Ceramic cup"}
        self.assertEqual(parse_search_response(search_body(bare)), [{
            "product_id": "p9", "title": "Ceramic cup", "brand": None, "category": None, "key_features": [],
            "materials": [], "image_url": None}])

    def test_text_is_folded_to_safe_ascii(self):
        card = parse_search_response(search_body(product(title="Café mug <script>x</script> ☕")))[0]
        self.assertEqual(card["title"], "Cafe mug script x /script")

    def test_malformed_replies_are_rejected(self):
        for body in (b"not json", b"[]", json.dumps({"items": []}).encode(), search_body({"title": "no id"}),
                     search_body(product(pid="bad id with spaces")), search_body(product(title="!!")),
                     b'{"products": [NaN]}', b"x" * (channel3_products.MAX_RESPONSE_BYTES + 1)):
            with self.assertRaises(Channel3Error):
                parse_search_response(body)

    def test_card_digest_is_stable_and_binds_every_field(self):
        card = parse_search_response(search_body(product()))[0]
        self.assertEqual(card_digest(card), card_digest(dict(reversed(list(card.items())))))
        self.assertNotEqual(card_digest(card), card_digest({**card, "title": card["title"] + " x"}))


class AdapterTests(unittest.TestCase):
    def test_off_without_flag_and_key_makes_zero_calls(self):
        transport = FakeTransport()
        for env in ({}, {"PAYGUARD_CHANNEL3": "enabled"}, {"CHANNEL3_API_KEY": FAKE_KEY}):
            adapter = build_channel3_product_adapter(env, transport=transport)
            self.assertEqual(adapter.mode, "off")
            self.assertEqual(adapter.lookup("Ceramic mug")["status"], "OFF")
        self.assertEqual(transport.calls, [])

    def test_only_sanitised_name_limit_and_key_header_leave(self):
        transport = FakeTransport()
        result = live_adapter(transport).lookup("Mug for Jane Smith, call 555-123-4567 or jane@example.com\nsecond line")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["source"], "channel3_live")
        call = transport.calls[0]
        self.assertEqual(call["url"], ENDPOINT)
        self.assertEqual(call["body"], {"query": "Mug, call or", "limit": 3})
        self.assertEqual(call["headers"]["x-api-key"], FAKE_KEY)
        self.assertNotIn(FAKE_KEY, json.dumps(result))

    def test_empty_reply_is_not_found(self):
        result = live_adapter(FakeTransport(body=search_body())).lookup("Ceramic mug")
        self.assertEqual((result["status"], result["cards"], result["source"]), ("NOT_FOUND", [], "channel3_live"))

    def test_failures_are_closed_and_never_leak(self):
        for transport, reason in ((FakeTransport(status=401, body=b"bad key " + FAKE_KEY.encode()), "upstream_error"),
                                  (FakeTransport(body=b"{}"), "contract_rejected"),
                                  (FakeTransport(exc=RuntimeError(FAKE_KEY)), "upstream_error"),
                                  (FakeTransport(exc=TimeoutError()), "timeout")):
            result = live_adapter(transport).lookup("Ceramic mug")
            self.assertEqual((result["status"], result["reason"]), ("UNAVAILABLE", reason))
            self.assertNotIn(FAKE_KEY, json.dumps(result))

    def test_image_url_with_at_sign_is_skipped_not_fatal(self):
        # One image URL with "@" (user info or a retina suffix) passed _image but failed the response schema,
        # which voided every card. It is now skipped, and the next https image is used instead.
        images = [{"url": "https://cdn.example/main@2x.png", "is_main_image": True},
                  {"url": "https://user@cdn.example/x.png"},
                  {"url": "https://cdn.example/plain.png"}]
        cards = parse_search_response(search_body(product(images=images), product("prod_mug_2", "Speckled Clay Mug, 10 oz")))
        self.assertEqual([card["image_url"] for card in cards], ["https://cdn.example/plain.png", "https://cdn.example/main-clean.png"])
        only_at = parse_search_response(search_body(product(images=[{"url": "https://cdn.example/a@b.png", "is_main_image": True}])))
        self.assertIsNone(only_at[0]["image_url"])

    def test_cards_with_at_sign_images_pass_the_response_schema(self):
        from app.schemas import ProductReferenceResponse
        transport = FakeTransport(body=search_body(product(images=[{"url": "https://cdn.example/main@2x.png", "is_main_image": True}])))
        result = live_adapter(transport).lookup("Ceramic mug")
        validated = ProductReferenceResponse.model_validate(result)
        self.assertEqual((validated.status, len(validated.cards), validated.cards[0].image_url), ("FOUND", 1, None))

    def test_a_routing_budget_is_spent_instead_of_the_shared_one(self):
        transport, shared, routing = FakeTransport(), CallBudget(5), CallBudget(1)
        adapter = live_adapter(transport, shared)
        self.assertEqual(adapter.lookup("Ceramic mug", budget=routing)["status"], "FOUND")
        self.assertEqual((shared.remaining, routing.remaining), (5, 0))
        self.assertEqual(adapter.lookup("Ceramic mug", budget=routing)["reason"], "budget_exhausted")
        self.assertEqual(len(transport.calls), 1)

    def test_shown_cards_are_kept_per_session(self):
        adapter = live_adapter(FakeTransport())
        result = {"source": "channel3_live", "recorded_at": None, "cards": [parse_search_response(search_body(product()))[0]]}
        adapter.remember("session-a", "eval-a", result)
        # A flood from one session evicts only that session's oldest evaluations, never another session's cards.
        for index in range(channel3_products.MAX_REMEMBERED_SESSIONS * 2):
            adapter.remember("session-b", f"eval-{index}", result)
        self.assertIsNotNone(adapter.shown("session-a", "eval-a"))
        self.assertIsNone(adapter.shown("session-b", "eval-0"))
        self.assertIsNotNone(adapter.shown("session-b", f"eval-{channel3_products.MAX_REMEMBERED_SESSIONS * 2 - 1}"))
        self.assertIsNone(adapter.shown("session-b", "eval-a"), "an evaluation id is looked up in its own session only")
        self.assertEqual(len(adapter._shown["session-b"]), channel3_products.MAX_REMEMBERED_PER_SESSION)
        # The number of sessions is bounded too: the least recently used session goes first.
        for index in range(channel3_products.MAX_REMEMBERED_SESSIONS):
            adapter.remember(f"other-{index}", "eval", result)
        self.assertLessEqual(len(adapter._shown), channel3_products.MAX_REMEMBERED_SESSIONS)
        self.assertIsNone(adapter.shown("session-a", "eval-a"))

    def test_budget_caps_calls(self):
        transport = FakeTransport()
        adapter = live_adapter(transport, CallBudget(2))
        statuses = [adapter.lookup("Ceramic mug")["status"] for _ in range(3)]
        self.assertEqual(statuses, ["FOUND", "FOUND", "UNAVAILABLE"])
        self.assertEqual(len(transport.calls), 2)

    def test_nothing_to_send_makes_zero_calls(self):
        transport = FakeTransport()
        self.assertEqual(live_adapter(transport).lookup("555-123-4567")["reason"], "nothing_to_send")
        self.assertEqual(transport.calls, [])

    def test_httpx_post_transport_bounds_body_and_disables_redirects(self):
        seen = {}

        def handler(request):
            seen["method"], seen["body"] = request.method, json.loads(request.content)
            return httpx.Response(302, headers={"location": "https://elsewhere.example"})

        real_client = httpx.Client
        with patch.object(channel3_products.httpx, "Client",
                          lambda **kwargs: real_client(transport=httpx.MockTransport(handler), **kwargs)):
            status, _ = channel3_products.httpx_post_transport(ENDPOINT, {"query": "mug", "limit": 3}, {}, 1.0)
        self.assertEqual((status, seen["method"], seen["body"]), (302, "POST", {"query": "mug", "limit": 3}))


class RecordedTests(unittest.TestCase):
    def write(self, payload):
        folder = tempfile.mkdtemp()
        self.addCleanup(lambda: [p.unlink() for p in pathlib.Path(folder).iterdir()] and None)
        path = pathlib.Path(folder) / "recorded.json"
        path.write_text(json.dumps(payload))
        return path

    def recording(self, **entry):
        card = parse_search_response(search_body(product()))[0]
        base = {"query": "Handcrafted ceramic coffee cup set of two", "recorded_at": "2026-11-02T01:00:00Z", "cards": [card]}
        base.update(entry)
        return {"schema_version": "payguard.channel3_recorded.v1", "entries": [base]}

    def test_public_demo_replays_recordings_and_never_calls_out(self):
        transport = FakeTransport()
        adapter = build_channel3_product_adapter({"PAYGUARD_CHANNEL3": "enabled", "CHANNEL3_API_KEY": FAKE_KEY},
                                                 public_demo=True, transport=transport, recorded_path=self.write(self.recording()))
        self.assertEqual(adapter.mode, "recorded")
        result = adapter.lookup("Handcrafted ceramic coffee cup — set of two")
        self.assertEqual((result["status"], result["source"], result["recorded_at"]),
                         ("FOUND", "channel3_recorded", "2026-11-02T01:00:00Z"))
        self.assertEqual(adapter.lookup("Something else entirely")["reason"], "not_recorded")
        self.assertEqual(transport.calls, [])

    def test_public_demo_without_recordings_is_off(self):
        adapter = build_channel3_product_adapter({}, public_demo=True, recorded_path=pathlib.Path("/nonexistent/x.json"))
        self.assertEqual(adapter.lookup("Ceramic mug")["status"], "OFF")

    def test_recordings_outside_the_closed_shape_are_skipped(self):
        card = parse_search_response(search_body(product()))[0]
        for bad in (self.recording(cards=[{**card, "price": 24}]), self.recording(cards=[{**card, "image_url": "http://x/y.jpg"}]),
                    self.recording(cards=[]), self.recording(query="Mug for Jane Smith"),
                    {"schema_version": "other", "entries": []}):
            self.assertEqual(load_recorded(self.write(bad)), {})


class Clock:
    def __init__(self):
        self.value = datetime(2026, 11, 2, 1, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


class ProductReferenceApiTests(unittest.TestCase):
    def build(self, adapter=None):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(
            lambda request: (_ for _ in ()).throw(AssertionError("no provider call"))), clock=self.clock)
        with patch.dict(os.environ, {}, clear=True):
            self.app = create_app(store=self.store, paypal=provider, channel3_products=adapter)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55002),
                                 raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def post(self, route, payload):
        return self.client.post(ROOT + route, json=payload, headers={
            "Origin": ORIGIN, "X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]})

    def review(self, description):
        response = self.post("/aup/review", {"description": description})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_default_app_is_off(self):
        self.build()
        result = self.review("Ceramic mug")
        response = self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        self.assertEqual(response.json(), {"status": "OFF", "source": None, "cards": [], "reason": None, "recorded_at": None,
                                           "affects_decision": False})

    def test_seller_confirms_one_shown_card_and_rule_result_is_unchanged(self):
        transport = FakeTransport(body=search_body(product("p1"), product("p2", title="Porcelain Tea Cup")))
        self.build(live_adapter(transport))
        description = "Guaranteed 30% ROI investment package"
        result = self.review(description)
        cards = self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": description}).json()
        self.assertEqual([card["product_id"] for card in cards["cards"]], ["p1", "p2"])
        confirm = self.post("/aup/product-reference/confirm", {"evaluation_id": result["evaluation_id"], "description": description,
                                                               "product_id": "p2"})
        self.assertEqual(confirm.status_code, 200, confirm.text)
        body = confirm.json()
        self.assertEqual((body["choice"], body["card"]["title"], body["confirmed_by"], body["source"]),
                         ("CONFIRMED", "Porcelain Tea Cup", "seller", "channel3_live"))
        self.assertEqual(body["card_digest"], card_digest(cards["cards"][1]))
        self.assertEqual(body["description_digest"], result["description_digest"])
        self.assertEqual({key: result[key] for key in ("match_status", "findings")},
                         {key: check_aup(description)[key] for key in ("match_status", "findings")})
        self.assertEqual(len(transport.calls), 1)

    def test_none_match_is_recorded_without_a_card(self):
        self.build(live_adapter(FakeTransport()))
        result = self.review("Ceramic mug")
        self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        body = self.post("/aup/product-reference/confirm", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug",
                                                            "product_id": None}).json()
        self.assertEqual((body["choice"], body["card"], body["card_digest"]), ("NONE_MATCH", None, None))

    def test_only_cards_shown_to_this_session_can_be_confirmed(self):
        self.build(live_adapter(FakeTransport()))
        result = self.review("Ceramic mug")
        never_shown = self.post("/aup/product-reference/confirm", {"evaluation_id": result["evaluation_id"],
                                                                   "description": "Ceramic mug", "product_id": "prod_mug_1"})
        self.assertEqual((never_shown.status_code, never_shown.json()["error"]["code"]), (422, "product_reference_not_shown"))
        self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        forged = self.post("/aup/product-reference/confirm", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug",
                                                              "product_id": "prod_forged"})
        self.assertEqual((forged.status_code, forged.json()["error"]["code"]), (422, "product_reference_unknown"))
        client_card = self.post("/aup/product-reference/confirm", {"evaluation_id": result["evaluation_id"],
                                                                   "description": "Ceramic mug", "product_id": "prod_mug_1",
                                                                   "card": {"title": "Anything"}})
        self.assertEqual(client_card.status_code, 422)

    def test_lookup_requires_a_live_matching_evaluation(self):
        transport = FakeTransport()
        self.build(live_adapter(transport))
        result = self.review("Ceramic mug")
        wrong = self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Other"})
        self.assertEqual(wrong.status_code, 422)
        self.clock.advance(121)
        expired = self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        self.assertEqual(expired.status_code, 422)
        self.assertEqual(transport.calls, [])

    def test_adapter_drift_becomes_unavailable(self):
        class Drifting:
            def lookup(self, _description):
                return {"status": "FOUND", "source": "channel3_live", "cards": [{"product_id": "p1", "title": "Mug",
                        "price": 24}], "reason": None, "recorded_at": None, "affects_decision": True}

        self.build(Drifting())
        result = self.review("Ceramic mug")
        body = self.post("/aup/product-reference", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"}).json()
        self.assertEqual((body["status"], body["reason"], body["cards"]), ("UNAVAILABLE", "contract_rejected", []))


if __name__ == "__main__":
    unittest.main()
