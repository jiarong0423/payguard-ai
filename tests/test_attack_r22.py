"""(attack r22) Backend findings pinned after their fix: AUP keyword evasions and synonyms, the guide's AUP and
rule-layer gaps, the per-session turn and form caps, and the country-check amount bound to the invoice.

Runs in process with TestClient and a fixed clock; any outbound connection fails the test.
"""
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.guide_routes import MAX_GUIDE_FORM_ROUNDS, GuideService
from app.main import create_app
from app.store import SessionStore
from payguard import country_rules
from payguard import evidence_guide as eg
from payguard.engines import check_aup

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "http://localhost:5173"


class Clock:
    def __init__(self, now=datetime(2026, 11, 3, 8, 0, tzinfo=timezone.utc)):
        self.now = now

    def __call__(self):
        return self.now


class R22AupKeywordTests(unittest.TestCase):
    ATTACKS = {
        "buy_cocaine_now": "controlled_substances", "PremiumCocaine 1g": "controlled_substances",
        "cocaine99 pure": "controlled_substances", "co/caine": "controlled_substances", "co'caine": "controlled_substances",
        "co,caine": "controlled_substances", "co+caine": "controlled_substances", "co|caine": "controlled_substances",
        "co·caine": "controlled_substances", "c  o  c  a  i  n  e": "controlled_substances",
        "c/o/c/a/i/n/e": "controlled_substances", "p!stol for sale": "weapons", "(ocaine": "controlled_substances",
        "9un parts": "weapons", "cօcaine": "controlled_substances", "ᴄocaine": "controlled_substances",
        "cⲟcaine": "controlled_substances", "counterfeiting handbags": "counterfeit_goods",
        "counterfeited sneakers": "counterfeit_goods", "ammunitions crate": "weapons", "online gamble tokens": "regulated_activity",
        "gambling chips": "regulated_activity", "vaporizer pens and juice": "regulated_activity", "meth crystals": "controlled_substances",
        "fentanyl patches": "controlled_substances", "Glock 19 with spare magazines": "weapons", "Glock19": "weapons",
        "AAA mirror quality Rolex": "counterfeit_goods", "1:1 copy Gucci bag": "counterfeit_goods", "grenades and detonators": "weapons",
        "sportsbook wager credits": "regulated_activity", "guaranteed returns of 200 percent": "unsupported_financial_promise",
        "risk-free double your money plan": "unsupported_financial_promise", "fire arm parts": "weapons",
        "Marlboro cigarettes carton": "regulated_activity",
    }
    # Intended matches, reviewed by a person: a split "fire arm" and "vaporizer" (also a humidifier).
    INTENDED = ("fire arms of a sofa", "cool mist vaporizer")
    ORDINARY = ("hand-crafted gin glasses", "Glockenspiel for kids", "methodology book", "gamer chair",
                "car cigarette lighter adapter", "heroine action figure", "guaranteed 100% cotton", "Guaranteed returns within 30 days",
                "AAA batteries 4 pack", "mirror grade polish", "1:10 scale model car", "iPhone case", "PayPal sticker",
                "gunmetal grey bottle", "Methodist hymn book", "stolen heart necklace", "Double your fun board game",
                "our secret weapon for clean floors", "T-shirt size S/M/L", "kids water gun", "c++ programming book",
                "Cocoa butter lotion", "pistachio nuts", "ammonite fossil")

    def test_each_evasion_and_synonym_gives_its_review_signal(self):
        for text, category in self.ATTACKS.items():
            result = check_aup(text)
            self.assertEqual(result["match_status"], "REVIEW_SIGNAL", repr(text))
            self.assertIn(category, [item["category"] for item in result["findings"]], repr(text))
            self.assertEqual(result["compliance_decision"], "NOT_MADE")

    def test_intended_matches_and_ordinary_text(self):
        for text in self.INTENDED:
            self.assertEqual(check_aup(text)["match_status"], "REVIEW_SIGNAL", text)
        for text in self.ORDINARY:
            self.assertEqual(check_aup(text)["match_status"], "NO_MATCH", text)

    def test_country_pack_prohibited_tags_the_table_can_name_are_flagged(self):
        pack = json.loads((ROOT / "data" / "country_rules" / "paypal_country_rules_v1.json").read_text())
        named = set(pack["shared"]["aup_prohibited_tags"]) - {"obscene"}  # no keyword category fits "obscene"
        for tag in sorted(named):
            self.assertEqual(check_aup(tag.replace("_", " "))["match_status"], "REVIEW_SIGNAL", tag)
        for tag in ("gambling", "e_cigarettes", "tobacco_other"):
            self.assertEqual(check_aup(tag.replace("_", " "))["match_status"], "REVIEW_SIGNAL", tag)

    def test_worst_case_text_stays_fast(self):
        import time
        for text in ("a " * 2000, "a_" * 2000, "aB" * 2000, "c/" * 2000, "1a" * 2000, "guaranteed " * 363):
            start = time.perf_counter()
            check_aup(text[:4000])
            self.assertLess(time.perf_counter() - start, 0.25, text[:8])


class R22RuleLayerTests(unittest.TestCase):
    TODAY = date(2026, 11, 3)

    def settled(self, scenario, goods, text):
        state = eg.new_state(scenario, goods)
        if goods:
            eg.choose_goods_type(state, goods)
        return [item for item, _clause in eg.auto_confirm(state, text, self.TODAY)[0]]

    def test_over_reading_is_left_to_the_seller(self):
        self.assertNotIn("shipping_tracking", self.settled("velocity", None, "We have tracking on every order except a few"))
        self.assertNotIn("ship_date", self.settled("dispute", "physical", "I shipped it last Tuesday or Monday"))
        self.assertNotIn("ship_date", self.settled("dispute", "physical", "I only shipped half the order last Monday"))
        self.assertIn("ship_date", self.settled("dispute", "physical", "I shipped it last Monday"))
        self.assertIn("shipping_tracking", self.settled("velocity", None, "We have tracking on every order"))

    def test_product_name_goes_through_the_aup_check(self):
        self.assertNotIn("product", self.settled("preflight", None, "I sell cocaine"))
        self.assertFalse(eg.validate_fixed_input("preflight", "product", "Handgun ammunition", self.TODAY))
        self.assertTrue(eg.validate_fixed_input("preflight", "product", "Handmade ceramic mugs", self.TODAY))

    def test_seller_local_today_is_one_day_of_slack(self):
        for offset, valid in ((-1, True), (0, True), (1, True), (2, False)):
            value = (self.TODAY + timedelta(days=offset)).isoformat()
            self.assertEqual(eg.validate_fixed_input("dispute", "ship_date", value, self.TODAY), valid, value)


class R22ApiBase(unittest.TestCase):
    def setUp(self, now=None):
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)
        self.clock = Clock(now or datetime(2026, 11, 3, 8, 0, tzinfo=timezone.utc))
        self.store = SessionStore(clock=self.clock, rate_limit=100000)
        self.app = create_app(store=self.store)
        self.app.state.guide = GuideService(self.store, chooser_factory=lambda: None)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55322))
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        session = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}

    def post(self, path, body):
        return self.client.post("/api/v1" + path, json=body, headers=self.headers)


class R22GuideApiTests(R22ApiBase):
    def test_restarting_the_guide_keeps_the_turn_count(self):
        self.post("/guide/start", {"scenario": "dispute", "goods_type": "physical"})
        for _ in range(40):
            view = self.post("/guide/turn", {"text": "I shipped the parcel"}).json()
        self.assertEqual(view["turns_used"], 40)
        self.assertEqual(self.post("/guide/start", {"scenario": "dispute", "goods_type": "physical"}).json()["turns_used"], 40)
        after = self.post("/guide/turn", {"text": "I shipped the parcel"}).json()
        self.assertEqual((after["turns_used"], after["reply"]["template"]), (40, "BUDGET"))

    def test_form_saves_are_capped_per_guide(self):
        self.post("/guide/start", {"scenario": "dispute", "goods_type": "physical"})
        codes = [self.post("/guide/form", {"item": "carrier", "value": "bogus"}).status_code for _ in range(MAX_GUIDE_FORM_ROUNDS)]
        self.assertEqual(set(codes), {200})
        refused = self.post("/guide/form", {"item": "carrier", "value": "UPS"})
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (429, "guide_form_limit"))
        self.post("/guide/start", {"scenario": "dispute", "goods_type": "physical"})
        self.assertEqual(self.post("/guide/form", {"item": "carrier", "value": "UPS"}).status_code, 429)

    def test_no_signal_is_refused_after_a_review_signal(self):
        self.post("/guide/start", {"scenario": "preflight"})
        self.post("/aup/review", {"description": "counterfeit handbags"})
        refused = self.post("/guide/form", {"item": "category_signal", "value": "no_signal"}).json()
        self.assertFalse(refused["form_result"]["valid"])
        self.assertTrue(self.post("/guide/form", {"item": "category_signal", "value": "review_signal"}).json()["form_result"]["valid"])
        self.post("/aup/review", {"description": "ceramic mug"})
        self.assertTrue(self.post("/guide/form", {"item": "category_signal", "value": "no_signal"}).json()["form_result"]["valid"])

    def test_baseline_after_spike_is_refused(self):
        self.post("/guide/start", {"scenario": "velocity"})
        both = self.post("/guide/form", {"fields": [{"item": "baseline_period", "value": "2026-10-30"},
                                                    {"item": "surge_period", "value": "2025-11-10"}]}).json()
        self.assertEqual([row["valid"] for row in both["form_results"]], [False, False])
        self.assertTrue(self.post("/guide/form", {"item": "surge_period", "value": "2026-10-20"}).json()["form_result"]["valid"])
        self.assertFalse(self.post("/guide/form", {"item": "baseline_period", "value": "2026-10-30"}).json()["form_result"]["valid"])
        self.assertTrue(self.post("/guide/form", {"item": "baseline_period", "value": "2026-10-01"}).json()["form_result"]["valid"])


class R22SellerLocalTodayTests(R22ApiBase):
    def setUp(self):
        super().setUp(now=datetime(2026, 11, 3, 17, 0, tzinfo=timezone.utc))  # 2026-11-04 01:00 at UTC+8

    def test_local_today_is_accepted(self):
        self.post("/guide/start", {"scenario": "dispute", "goods_type": "physical"})
        self.assertTrue(self.post("/guide/form", {"item": "ship_date", "value": "2026-11-04"}).json()["form_result"]["valid"])


class R22CountryAmountTests(R22ApiBase):
    def invoice(self, amount):
        aup = self.post("/aup/review", {"description": "ceramic mug"}).json()
        return self.post("/paypal/invoices/review", {"description": "ceramic mug", "amount": amount, "currency": "USD",
                                                     "confirm_sandbox_draft": True, "evaluation_id": aup["evaluation_id"],
                                                     "description_digest": aup["description_digest"]})

    def check(self, **extra):
        return self.post("/country-rules/check", dict({"seller_country": "CN", "buyer_country": "US"}, **extra))

    def test_invoice_amount_must_match_the_checked_amount(self):
        self.assertEqual(self.check(amount="1.00", currency="USD").status_code, 200)
        refused = self.invoice("9999999.99")
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "country_amount_changed"))
        self.assertEqual(self.invoice("1.00").status_code, 200)
        self.assertEqual(self.check(amount="10", currency="USD").status_code, 200)
        self.assertEqual(self.invoice("10.00").status_code, 200)

    def test_currency_must_match_and_a_check_without_amount_binds_none(self):
        self.assertEqual(self.check(amount="10", currency="TWD").status_code, 200)
        self.assertEqual(self.invoice("10.00").status_code, 409)
        self.assertEqual(self.check().status_code, 200)
        self.assertEqual(self.invoice("9999999.99").status_code, 200)

    def test_a_later_check_with_another_amount_stops_the_draft(self):
        self.assertEqual(self.check(amount="10", currency="USD").status_code, 200)
        review = self.invoice("10.00").json()
        self.assertEqual(self.check(amount="20", currency="USD").status_code, 200)
        draft = self.post("/paypal/invoices/draft", {"description": "ceramic mug", "amount": "10.00", "currency": "USD",
                                                     "review_token": review["review_token"], "payload_digest": review["payload_digest"]})
        self.assertEqual((draft.status_code, draft.json()["error"]["code"]), (409, "country_amount_changed"))

    def test_unknown_currency_is_422(self):
        for currency in ("ZZZ", "XXX", "ABC"):
            response = self.check(amount="100000", currency=currency)
            self.assertEqual((response.status_code, response.json()["error"]["code"]), (422, "country_check_invalid"), currency)
        for currency in sorted(country_rules.accepted_currencies()):
            self.assertEqual(self.check(amount="10", currency=currency).status_code, 200, currency)
        with self.assertRaises(country_rules.CountryRulesError):
            country_rules.check("CN", "US", amount="10", currency="ZZZ")


if __name__ == "__main__":
    unittest.main()
