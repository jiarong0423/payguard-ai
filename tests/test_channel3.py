"""Optional Channel3 category signal: sanitiser, closed contract, off-by-default, budget and timeout.

Every test uses a fake transport. No test opens a network connection or needs a real key.
"""

import json
import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app import channel3
from app.channel3 import (build_channel3_adapter, CallBudget, Channel3CategoryAdapter, Channel3Config, Channel3Error, ENDPOINT,
                          parse_categories_response, sanitize_product_name, validate_signal)
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore
from payguard.engines import check_aup


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"
FAKE_KEY = "c3-test-key-not-real-0000"


def categories_body(*entries):
    return json.dumps({"categories": [
        {"slug": slug, "title": title, "path": [{"slug": root, "title": root.title()}, {"slug": slug, "title": title}],
         "has_children": False} for slug, title, root in entries]}).encode()


class FakeTransport:
    def __init__(self, status=200, body=None, exc=None):
        self.status = status
        self.body = categories_body(("mugs", "Mugs", "kitchen")) if body is None else body
        self.exc = exc
        self.calls = []

    def __call__(self, url, params, headers, timeout):
        self.calls.append({"url": url, "params": dict(params), "headers": dict(headers), "timeout": timeout})
        if self.exc is not None:
            raise self.exc
        return self.status, self.body


def enabled_adapter(transport, budget=None, timeout=channel3.TIMEOUT_SECONDS):
    return Channel3CategoryAdapter(Channel3Config(enabled=True, api_key=FAKE_KEY), transport=transport,
                                   budget=budget or CallBudget(5), timeout=timeout)


class SanitiserTests(unittest.TestCase):
    def test_plain_product_name_is_kept(self):
        self.assertEqual(sanitize_product_name("Handcrafted ceramic coffee cup - set of two"),
                         "Handcrafted ceramic coffee cup - set of two")

    def test_non_ascii_is_folded_or_dropped(self):
        self.assertEqual(sanitize_product_name("Café crème brûlée kit — 🍮"), "Cafe creme brulee kit")
        self.assertTrue(sanitize_product_name("Cafe\u0000 mug‮").isascii())

    def test_emails_and_handles_are_removed(self):
        result = sanitize_product_name("Leather wallet contact jane.doe+shop@example.co.uk or @janeshop")
        self.assertEqual(result, "Leather wallet contact or")
        self.assertNotIn("@", result)

    def test_urls_are_removed(self):
        for text in ("Linen apron https://shop.example.com/p?id=9 sale", "Linen apron www.example.com sale",
                     "Linen apron example.store/item sale"):
            self.assertEqual(sanitize_product_name(text), "Linen apron sale", text)

    def test_digit_runs_longer_than_four_are_removed(self):
        self.assertEqual(sanitize_product_name("Order 1234567 desk lamp"), "Order desk lamp")
        self.assertEqual(sanitize_product_name("Desk lamp call (555) 123-4567"), "Desk lamp call")
        self.assertEqual(sanitize_product_name("Card 4111 1111 1111 1111 sleeve"), "Card sleeve")
        # Short numbers that describe the product stay.
        self.assertEqual(sanitize_product_name("Set of 2 mugs 12 oz"), "Set of 2 mugs 12 oz")
        self.assertEqual(sanitize_product_name("Model 2026 planner"), "Model 2026 planner")

    def test_names_after_for_and_to_are_removed(self):
        self.assertEqual(sanitize_product_name("Custom mug for John Smith"), "Custom mug")
        self.assertEqual(sanitize_product_name("Engraved pen to Mary O'Brien, gift wrapped"), "Engraved pen, gift wrapped")
        self.assertEqual(sanitize_product_name("Portrait for J. R. Tolkien fan"), "Portrait fan")
        self.assertEqual(sanitize_product_name("Mug for John and the kitchen"), "Mug and the kitchen")
        # Lowercase words after "for" are product context, not names.
        self.assertEqual(sanitize_product_name("Stand for kitchen tablets"), "Stand for kitchen tablets")

    def test_only_first_line_and_at_most_120_chars(self):
        result = sanitize_product_name("Bamboo cutting board\nShip to 12 Main Street, Springfield")
        self.assertEqual(result, "Bamboo cutting board")
        long = sanitize_product_name(" ".join(["walnut"] * 60))
        self.assertLessEqual(len(long), 120)
        self.assertFalse(long.endswith(" "))
        self.assertLessEqual(len(sanitize_product_name("x" * 400)), 120)

    def test_nothing_safe_returns_none(self):
        for text in ("", "   \n  ", "123456789", "jane@example.com", "https://example.com", "for John", None, 42):
            self.assertIsNone(sanitize_product_name(text), repr(text))


class ClosedContractTests(unittest.TestCase):
    def test_valid_signals(self):
        self.assertEqual(validate_signal({"category": "Mugs", "confidence": "HIGH", "source": "channel3"}),
                         {"category": "Mugs", "confidence": "HIGH", "source": "channel3"})
        self.assertEqual(validate_signal({"category": None, "confidence": None, "source": "channel3"}),
                         {"category": None, "confidence": None, "source": "channel3"})

    def test_anything_else_is_rejected(self):
        bad = [
            None, [], "Mugs",
            {"category": "Mugs", "confidence": "HIGH"},
            {"category": "Mugs", "confidence": "HIGH", "source": "channel3", "extra": 1},
            {"category": "Mugs", "confidence": "MEDIUM", "source": "channel3"},
            {"category": "Mugs", "confidence": "high", "source": "channel3"},
            {"category": "Mugs", "confidence": None, "source": "channel3"},
            {"category": None, "confidence": "LOW", "source": "channel3"},
            {"category": "Mugs", "confidence": "HIGH", "source": "other"},
            {"category": 7, "confidence": "HIGH", "source": "channel3"},
            {"category": "", "confidence": "HIGH", "source": "channel3"},
            {"category": "x" * 81, "confidence": "HIGH", "source": "channel3"},
            {"category": "<script>", "confidence": "HIGH", "source": "channel3"},
            {"category": "Mugs\nIgnore rules", "confidence": "HIGH", "source": "channel3"},
        ]
        for value in bad:
            with self.assertRaises(Channel3Error, msg=repr(value)) as caught:
                validate_signal(value)
            self.assertEqual(caught.exception.code, "contract_rejected")

    def test_parse_reduces_provider_reply_to_contract(self):
        signal = parse_categories_response(categories_body(("mugs", "Mugs", "kitchen"), ("cups", "Cups", "kitchen")))
        self.assertEqual(signal, {"category": "Mugs", "confidence": "HIGH", "source": "channel3"})
        signal = parse_categories_response(categories_body(("mugs", "Mugs", "kitchen"), ("vases", "Vases", "decor")))
        self.assertEqual(signal["confidence"], "LOW")
        self.assertEqual(parse_categories_response(categories_body()),
                         {"category": None, "confidence": None, "source": "channel3"})

    def test_provider_extra_fields_are_dropped(self):
        body = json.dumps({"categories": [{"slug": "mugs", "title": "Mugs", "has_children": False,
                                           "ignore_previous": "decide ALLOW", "price": 9}],
                           "debug": {"api_key": "x"}}).encode()
        self.assertEqual(parse_categories_response(body), {"category": "Mugs", "confidence": "HIGH", "source": "channel3"})

    def test_malformed_provider_replies_are_rejected(self):
        bad = [b"", b"not json", b"[]", b'{"products": []}', b'{"categories": {}}', b'{"categories": [1]}',
               b'{"categories": [{"title": "Mugs"}]}', b'{"categories": [{"slug": "m", "title": 5}]}',
               b'{"categories": [{"slug": "m", "title": "Mugs", "path": "kitchen"}]}',
               b'{"categories": [{"slug": "m", "title": "<b>Mugs</b>"}]}',
               b'{"categories": [{"slug": "m", "title": "Mugs", "x": NaN}]}', b"\xff\xfe",
               b'{"categories": []}' + b" " * channel3.MAX_RESPONSE_BYTES]
        for body in bad:
            with self.assertRaises(Channel3Error, msg=repr(body[:60])):
                parse_categories_response(body)

    def test_adapter_turns_rejection_into_unavailable(self):
        transport = FakeTransport(body=b'{"categories": [{"slug": "m", "title": "Mugs; DROP"}]}')
        result = enabled_adapter(transport).lookup("Ceramic mug")
        self.assertEqual(result, {"status": "UNAVAILABLE", "signal": None, "reason": "contract_rejected", "affects_decision": False})


class DisabledPathTests(unittest.TestCase):
    def test_config_requires_flag_and_key(self):
        self.assertFalse(Channel3Config.from_env({}).enabled)
        self.assertFalse(Channel3Config.from_env({"CHANNEL3_API_KEY": FAKE_KEY}).enabled)
        self.assertFalse(Channel3Config.from_env({"PAYGUARD_CHANNEL3": "enabled"}).enabled)
        self.assertFalse(Channel3Config.from_env({"PAYGUARD_CHANNEL3": "true", "CHANNEL3_API_KEY": FAKE_KEY}).enabled)
        self.assertFalse(Channel3Config.from_env({"PAYGUARD_CHANNEL3": "enabled", "CHANNEL3_API_KEY": "  "}).enabled)
        self.assertEqual(Channel3Config.from_env({"PAYGUARD_CHANNEL3": "true", "CHANNEL3_API_KEY": FAKE_KEY}).api_key, "")
        config = Channel3Config.from_env({"PAYGUARD_CHANNEL3": "enabled", "CHANNEL3_API_KEY": FAKE_KEY})
        self.assertTrue(config.enabled)
        self.assertNotIn(FAKE_KEY, repr(config))

    def test_disabled_adapter_makes_zero_calls(self):
        transport = FakeTransport()
        budget = CallBudget(5)
        adapter = Channel3CategoryAdapter(Channel3Config.from_env({}), transport=transport, budget=budget)
        for text in ("Ceramic mug", "Guaranteed 30% ROI investment package", "", None):
            self.assertEqual(adapter.lookup(text), {"status": "OFF", "signal": None, "reason": None, "affects_decision": False})
        self.assertEqual(transport.calls, [])
        self.assertEqual(budget.remaining, 5)

    def test_default_adapter_is_off_without_env(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(Channel3CategoryAdapter().enabled)

    def test_factory_force_off_overrides_env(self):
        env = {"PAYGUARD_CHANNEL3": "enabled", "CHANNEL3_API_KEY": FAKE_KEY}
        self.assertTrue(build_channel3_adapter(env).enabled)
        transport = FakeTransport()
        adapter = build_channel3_adapter(env, force_off=True, transport=transport)
        self.assertFalse(adapter.enabled)
        self.assertEqual(adapter.lookup("Ceramic mug")["status"], "OFF")
        self.assertEqual(transport.calls, [])
        self.assertEqual(adapter.config.api_key, "")

    def test_nothing_to_send_makes_zero_calls(self):
        transport = FakeTransport()
        result = enabled_adapter(transport).lookup("jane@example.com 5551234567")
        self.assertEqual(result, {"status": "NOT_SENT", "signal": None, "reason": "nothing_to_send", "affects_decision": False})
        self.assertEqual(transport.calls, [])


class EnabledCallTests(unittest.TestCase):
    def test_only_sanitised_name_and_key_header_are_sent(self):
        transport = FakeTransport()
        result = enabled_adapter(transport).lookup("Custom mug for John Smith jane@example.com 5551234567\nsecond line")
        self.assertEqual(result, {"status": "SIGNAL", "signal": {"category": "Mugs", "confidence": "HIGH", "source": "channel3"},
                                  "reason": None, "affects_decision": False})
        self.assertEqual(len(transport.calls), 1)
        call = transport.calls[0]
        self.assertEqual(call["url"], ENDPOINT)
        self.assertEqual(call["params"], {"query": "Custom mug", "limit": "3"})
        self.assertEqual(call["headers"], {"x-api-key": FAKE_KEY, "accept": "application/json"})
        self.assertEqual(call["timeout"], channel3.TIMEOUT_SECONDS)

    def test_non_200_is_unavailable_and_key_never_in_result(self):
        for status in (401, 402, 422, 429, 500):
            result = enabled_adapter(FakeTransport(status=status, body=FAKE_KEY.encode())).lookup("Ceramic mug")
            self.assertEqual(result["status"], "UNAVAILABLE")
            self.assertEqual(result["reason"], "upstream_error")
            self.assertNotIn(FAKE_KEY, json.dumps(result))

    def test_transport_exception_text_never_leaks(self):
        result = enabled_adapter(FakeTransport(exc=RuntimeError("boom " + FAKE_KEY))).lookup("Ceramic mug")
        self.assertEqual(result, {"status": "UNAVAILABLE", "signal": None, "reason": "upstream_error", "affects_decision": False})


class BudgetTests(unittest.TestCase):
    def test_budget_caps_outbound_calls_per_process(self):
        transport = FakeTransport()
        budget = CallBudget(2)
        adapter = enabled_adapter(transport, budget=budget)
        self.assertEqual(adapter.lookup("Ceramic mug")["status"], "SIGNAL")
        self.assertEqual(adapter.lookup("Ceramic mug")["status"], "SIGNAL")
        self.assertEqual(adapter.lookup("Ceramic mug"),
                         {"status": "UNAVAILABLE", "signal": None, "reason": "budget_exhausted", "affects_decision": False})
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(budget.remaining, 0)

    def test_failed_calls_still_spend_budget(self):
        transport = FakeTransport(status=500)
        adapter = enabled_adapter(transport, budget=CallBudget(1))
        adapter.lookup("Ceramic mug")
        self.assertEqual(adapter.lookup("Ceramic mug")["reason"], "budget_exhausted")
        self.assertEqual(len(transport.calls), 1)

    def test_budget_rejects_invalid_limits(self):
        for limit in (-1, 1.5, "3", True):
            with self.assertRaises(ValueError):
                CallBudget(limit)


class TimeoutTests(unittest.TestCase):
    def test_transport_timeout_is_reported(self):
        for exc in (Channel3Error("timeout"), TimeoutError()):
            result = enabled_adapter(FakeTransport(exc=exc)).lookup("Ceramic mug")
            self.assertEqual(result, {"status": "UNAVAILABLE", "signal": None, "reason": "timeout", "affects_decision": False})

    def test_httpx_transport_maps_timeout_and_passes_timeout_value(self):
        seen = {}
        def handler(request):
            seen["key"] = request.headers.get("x-api-key")
            seen["query"] = dict(request.url.params)
            seen["timeout"] = request.extensions.get("timeout")
            raise httpx.ReadTimeout("slow", request=request)
        real_client = httpx.Client
        def fake_client(**kwargs):
            return real_client(transport=httpx.MockTransport(handler), **kwargs)
        with patch.object(channel3.httpx, "Client", side_effect=fake_client):
            with self.assertRaises(Channel3Error) as caught:
                channel3.httpx_transport(ENDPOINT, {"query": "Ceramic mug", "limit": "3"}, {"x-api-key": FAKE_KEY}, 1.5)
        self.assertEqual(caught.exception.code, "timeout")
        self.assertEqual(seen["key"], FAKE_KEY)
        self.assertEqual(seen["query"], {"query": "Ceramic mug", "limit": "3"})
        self.assertEqual(seen["timeout"], {"connect": 1.5, "read": 1.5, "write": 1.5, "pool": 1.5})

    def test_httpx_transport_bounds_body_and_disables_redirects(self):
        def handler(request):
            return httpx.Response(302, headers={"location": "https://evil.example/"}, content=b"{}")
        real_client = httpx.Client
        with patch.object(channel3.httpx, "Client", side_effect=lambda **kw: real_client(transport=httpx.MockTransport(handler), **kw)):
            status, _body = channel3.httpx_transport(ENDPOINT, {"query": "Mug"}, {}, 1.0)
        self.assertEqual(status, 302)
        big = lambda request: httpx.Response(200, content=b"x" * (channel3.MAX_RESPONSE_BYTES + 1))
        with patch.object(channel3.httpx, "Client", side_effect=lambda **kw: real_client(transport=httpx.MockTransport(big), **kw)):
            with self.assertRaises(Channel3Error) as caught:
                channel3.httpx_transport(ENDPOINT, {"query": "Mug"}, {}, 1.0)
        self.assertEqual(caught.exception.code, "contract_rejected")


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


class CategorySignalApiTests(unittest.TestCase):
    def build(self, adapter=None):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=httpx.MockTransport(
            lambda request: (_ for _ in ()).throw(AssertionError("no provider call"))), clock=self.clock)
        with patch.dict(os.environ, {}, clear=True):
            self.app = create_app(store=self.store, paypal=provider, channel3=adapter)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001),
                                 raise_server_exceptions=False)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        response = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN})
        self.session = response.json()

    def post(self, route, payload):
        return self.client.post(ROOT + route, json=payload, headers={
            "Origin": ORIGIN, "X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]})

    def review(self, description):
        response = self.post("/aup/review", {"description": description})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_default_app_is_off_and_aup_result_unchanged(self):
        self.build()
        description = "Guaranteed 30% ROI investment package"
        result = self.review(description)
        self.assertEqual(result["match_status"], "REVIEW_SIGNAL")
        self.assertEqual({key: result[key] for key in ("match_status", "findings", "recommendation", "policy_version")},
                         {key: value for key, value in check_aup(description).items()
                          if key in ("match_status", "findings", "recommendation", "policy_version")})
        self.assertNotIn("category_signal", result)
        signal = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": description})
        self.assertEqual(signal.status_code, 200, signal.text)
        self.assertEqual(signal.json(), {"status": "OFF", "signal": None, "reason": None, "affects_decision": False})

    def test_enabled_signal_never_changes_rule_decision(self):
        transport = FakeTransport(body=categories_body(("investing", "Financial Services", "services")))
        self.build(enabled_adapter(transport))
        for description, expected in (("Guaranteed 30% ROI investment package", "REVIEW_SIGNAL"),
                                      ("Handcrafted ceramic coffee cup", "NO_MATCH")):
            result = self.review(description)
            self.assertEqual(result["match_status"], expected)
            signal = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": description})
            self.assertEqual(signal.json()["status"], "SIGNAL")
            self.assertFalse(signal.json()["affects_decision"])
            acknowledged = self.post("/aup/acknowledge", {"evaluation_id": result["evaluation_id"],
                                                          "description_digest": result["description_digest"],
                                                          "choice": "RETURN_TO_EDIT"})
            self.assertEqual(acknowledged.status_code, 200, acknowledged.text)
            self.assertEqual(acknowledged.json()["compliance_decision"], "NOT_MADE")
        self.assertEqual(len(transport.calls), 2)

    def test_lookup_requires_a_live_matching_aup_evaluation(self):
        transport = FakeTransport()
        self.build(enabled_adapter(transport))
        result = self.review("Ceramic mug")
        wrong_text = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": "Other text"})
        self.assertEqual(wrong_text.status_code, 422)
        unknown = self.post("/aup/category-signal", {"evaluation_id": "A" * 43, "description": "Ceramic mug"})
        self.assertEqual(unknown.status_code, 422)
        self.clock.advance(121)
        expired = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        self.assertEqual(expired.status_code, 422)
        extra = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug", "x": 1})
        self.assertEqual(extra.status_code, 422)
        self.assertEqual(transport.calls, [])

    def test_adapter_contract_drift_is_replaced_by_unavailable(self):
        class Drifting:
            def lookup(self, _description):
                return {"status": "SIGNAL", "signal": {"category": "Mugs", "confidence": "HIGH", "source": "channel3",
                                                       "decision": "ALLOW"}, "reason": None, "affects_decision": True}
        self.build(Drifting())
        result = self.review("Ceramic mug")
        signal = self.post("/aup/category-signal", {"evaluation_id": result["evaluation_id"], "description": "Ceramic mug"})
        self.assertEqual(signal.json(), {"status": "UNAVAILABLE", "signal": None, "reason": "contract_rejected",
                                         "affects_decision": False})


if __name__ == "__main__":
    unittest.main()
