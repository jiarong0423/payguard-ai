"""Per-country PayPal rules: the pinned pack, the pair check and the clause search (no network)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from fastapi.testclient import TestClient

from app.main import create_app
from payguard import country_rules as cr

ORIGIN = "http://localhost:5173"


class PackTests(unittest.TestCase):
    def test_pack_is_pinned_and_covers_ten_countries_with_official_sources(self):
        raw = cr.PACK_PATH.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), cr.PACK_SHA256)
        pack = cr.load_pack()
        self.assertEqual(set(pack["countries"]), {"US", "TW", "CN", "HK", "GB", "DE", "JP", "SG", "AU", "CA"})
        for code, row in pack["countries"].items():
            for url in row["sources"].values():
                self.assertTrue(url.startswith("https://www.paypal.com/"), (code, url))
        for snippet in pack["snippets"]:
            self.assertLessEqual(len(snippet["text"].split()), 60, snippet["id"])
            self.assertTrue(snippet["url"].startswith(("https://www.paypal.com/", "https://developer.paypal.com/")), snippet["id"])

    def test_an_edited_pack_is_refused(self):
        with self.assertRaises(cr.CountryRulesError):
            cr.load_pack(expected_sha256="0" * 64)


class CheckTests(unittest.TestCase):
    def codes(self, result):
        return {(row["severity"], row["code"]) for row in result["findings"]}

    def test_china_personal_account_after_cutoff_is_blocked_unknown_is_a_warning_before_is_clear(self):
        after = cr.check("CN", "US", account_type="personal", account_opened="after_cutoff")
        self.assertTrue(after["blocked"])
        self.assertIn(("BLOCK", "personal_account_goods_restricted"), self.codes(after))
        unknown = cr.check("CN", "US", account_type="personal")
        self.assertFalse(unknown["blocked"])
        self.assertIn(("WARN", "personal_account_goods_restricted"), self.codes(unknown))
        before = cr.check("CN", "US", account_type="personal", account_opened="before_cutoff")
        self.assertNotIn("personal_account_goods_restricted", {row["code"] for row in before["findings"]})
        self.assertFalse(cr.check("TW", "US", account_type="personal", account_opened="after_cutoff")["blocked"])

    def test_live_animals_cross_border_depends_on_both_laws_and_prohibited_goods_block_everywhere(self):
        # Neither side has rules (a pack without national rules): PayPal names no rule, so the law at both ends decides.
        bare = json.loads(json.dumps(cr.load_pack()))
        bare["export_rules"], bare["import_rules"] = {}, {}
        result = cr.check("US", "JP", goods_tags=["live_animals"], pack=bare)
        law = next(row for row in result["findings"] if row["code"] == "law_dependent")
        self.assertIn("both United States and Japan", law["text"])
        # Only one side has rules: the missing side is named, not read as allowed.
        one_side = json.loads(json.dumps(cr.load_pack()))
        one_side["import_rules"].pop("JP")
        self.assertIn(("WARN", "import_rules_not_in_pack"), self.codes(cr.check("CN", "JP", goods_tags=["live_animals"], pack=one_side)))
        self.assertEqual(law["severity"], "WARN")
        self.assertTrue(result["cross_border"])
        for seller in ("US", "TW", "DE"):
            self.assertTrue(cr.check(seller, "US", goods_tags=["weapons"])["blocked"], seller)
        self.assertIn(("WARN", "aup_preapproval"), self.codes(cr.check("US", "US", goods_tags=["alcohol"])))

    def test_guest_checkout_signature_and_buyer_rules_follow_the_matrix(self):
        self.assertIn(("WARN", "no_protection_guest_checkout"), self.codes(cr.check("HK", "US", checkout="guest_card")))
        self.assertNotIn(("WARN", "no_protection_guest_checkout"), self.codes(cr.check("TW", "US", checkout="guest_card")))
        self.assertIn(("WARN", "signature_required"), self.codes(cr.check("CN", "US", amount="750", currency="USD")))
        self.assertNotIn(("WARN", "signature_required"), self.codes(cr.check("CN", "US", amount="749.99", currency="USD")))
        self.assertIn(("INFO", "buyer_snad_window"), self.codes(cr.check("US", "DE")))
        self.assertIn(("INFO", "buyer_privacy_law"), self.codes(cr.check("US", "GB")))
        severities = [row["severity"] for row in cr.check("CN", "TW", account_type="personal", account_opened="after_cutoff",
                                                           checkout="guest_card", goods_tags=["weapons"])["findings"]]
        self.assertEqual(severities, sorted(severities, key=cr.SEVERITY_ORDER.get))

    def test_unknown_inputs_are_refused(self):
        for kwargs in ({"seller_country": "XX", "buyer_country": "US"}, {"seller_country": "US", "buyer_country": "US", "goods_tags": ["pets"]},
                       {"seller_country": "US", "buyer_country": "US", "checkout": "cash"}):
            with self.assertRaises(cr.CountryRulesError):
                cr.check(**kwargs)

    def test_post_bans_keep_the_lead_the_panel_turns_amber_on(self):
        # CountryRules.jsx POSTAL_LEAD reads this server wording (review r15 P2): if it changes, the amber verdict would
        # silently go green. CN to US e-cigarettes is a post-only ban.
        import re
        panel = (Path(__file__).resolve().parents[1] / "frontend" / "src" / "CountryRules.jsx").read_text(encoding="utf-8")
        lead = re.compile(re.search(r"const POSTAL_LEAD = /(.+)/;", panel).group(1))
        rows = [row for row in cr.check("CN", "US", goods_tags=["e_cigarettes"])["findings"] if row["code"].endswith("_prohibited")]
        self.assertTrue(any(row["severity"] == "WARN" and lead.search(row["text"]) for row in rows), rows)

    def test_taiwan_import_rules_use_three_tiers_and_only_ban_a_whole_tag_when_every_rule_bans(self):
        # Taiwan's live-animal ban binds the post only (review 2026-11-03); a courier import with quarantine papers warns.
        animals = cr.check("CN", "TW", goods_tags=["live_animals"])
        self.assertFalse(animals["blocked"])
        self.assertIn(("WARN", "import_prohibited"), self.codes(animals))
        food = cr.check("CN", "TW", goods_tags=["food"])
        self.assertFalse(food["blocked"], "some foods may enter: the meat and mainland bans warn as 'if your item is this kind'")
        self.assertIn(("WARN", "import_prohibited"), self.codes(food))
        self.assertIn(("WARN", "import_restricted"), self.codes(food))
        self.assertTrue(any("Pu'er" in row["text"] for row in food["findings"]), "mainland-only rule applies to CN->TW")
        self.assertFalse(any("Pu'er" in row["text"] for row in cr.check("US", "TW", goods_tags=["food"])["findings"]))
        self.assertFalse(any(row["code"].startswith("import") for row in cr.check("TW", "TW", goods_tags=["food"])["findings"]),
                         "a domestic sale has no import step")
        phones = cr.check("US", "TW", goods_tags=["radio_wireless"])
        self.assertIn(("WARN", "import_restricted"), self.codes(phones))
        self.assertFalse(any(row["code"] == "import_parcel_rule" for row in cr.check("US", "TW")["findings"]),
                         "parcel rules only when a ticked item has import rules")
        for row in cr.load_pack()["import_rules"]["TW"]["rules"]:
            self.assertRegex(row["url"], r"^https://([a-z0-9-]+\.)*(gov\.tw|law\.moj\.gov\.tw)/", row["id"])

    def test_approval_goods_still_reach_the_destination_import_rules(self):
        # review r10: alcohol, e-cigarettes, medicines and medical devices used to stop at the PayPal approval warning.
        ecig = cr.check("US", "TW", goods_tags=["e_cigarettes"])
        self.assertTrue(ecig["blocked"])
        self.assertIn(("WARN", "aup_preapproval"), self.codes(ecig))
        self.assertIn(("BLOCK", "import_prohibited"), self.codes(ecig))
        for tag in ("alcohol", "prescription", "medical_devices"):
            codes = self.codes(cr.check("US", "TW", goods_tags=[tag]))
            self.assertIn(("WARN", "aup_preapproval"), codes, tag)
            self.assertTrue(any(code.startswith("import_") for _sev, code in codes), tag)
        self.assertTrue(cr.check("US", "TW", goods_tags=["weapons"])["blocked"])

    def test_route_rules_and_wording_follow_the_sources(self):
        mainland = cr.check("CN", "TW")
        self.assertTrue(any(row["code"] == "import_parcel_rule" and row["severity"] == "WARN" for row in mainland["findings"]),
                        "the mainland permitted-goods list shows on CN->TW even with no item ticked")
        self.assertIn(("WARN", "local_account_required"), self.codes(cr.check("CN", "US", account_type="business")))
        restricted = next(row for row in cr.check("CN", "US", account_type="personal")["findings"] if row["code"] == "personal_account_goods_restricted")
        self.assertIn("or a later date PayPal announces", restricted["text"])
        hold = next(row for row in cr.check("US", "US")["findings"] if row["code"] == "risk_hold_days")
        self.assertIn("usually", hold["text"])
        weapons = next(row for row in cr.check("US", "US", goods_tags=["weapons"])["findings"] if row["code"] == "aup_prohibited")
        self.assertIn("firearms, ammunition", weapons["text"])

    def test_both_sides_are_matched_on_their_own_allowed_out_is_not_allowed_in(self):
        """Owner rule 2026-11-02: the export side and the import side are paired separately; either side banning the
        whole tag blocks, and one side's silence is reported, not read as allowed."""
        pack = json.loads(json.dumps(cr.load_pack()))
        url = "https://www.customs.gov.tw/"
        row = lambda **kw: {"id": kw.pop("id"), "url": url, "page_date": None, "retrieved_at": "2026-11-02",
                            "quantity_limit": None, "permit": None, "agency": "x", **kw}
        pack["export_rules"] = {
            "TW": {"rules": [row(id="tw-ex-1", route="TW->*", tag="cosmetics", tier="general", rule="Exports freely.",
                                 statute="Statute X", article="Art. 1")]},
            "JP": {"rules": [row(id="jp-ex-1", route="JP->TW", tag="cosmetics", tier="prohibited", rule="No export to TW.")]},
        }
        pack["import_rules"]["JP"] = {"rules": [row(id="jp-im-1", route="*->JP", tag="cosmetics", tier="prohibited",
                                                    rule="No cosmetics enter.")]}
        pack["import_rules"].pop("US", None)
        pack["export_rules"].pop("US", None)
        # Leaves TW freely, banned on entry to JP: blocked by the import side, the export row is still listed with its article.
        out_ok_in_banned = cr.check("TW", "JP", goods_tags=["cosmetics"], pack=pack)
        self.assertTrue(out_ok_in_banned["blocked"])
        self.assertIn(("INFO", "export_general"), self.codes(out_ok_in_banned))
        self.assertIn(("BLOCK", "import_prohibited"), self.codes(out_ok_in_banned))
        self.assertTrue(any("[Statute X Art. 1]" in f["text"] for f in out_ok_in_banned["findings"]))
        # Banned on leaving JP for TW: blocked by the export side whatever TW import says.
        self.assertIn(("BLOCK", "export_prohibited"), self.codes(cr.check("JP", "TW", goods_tags=["cosmetics"], pack=pack)))
        # The export rule is route-specific: JP to US does not match it, and JP has no import step on an outbound sale.
        self.assertFalse(cr.check("JP", "US", goods_tags=["cosmetics"], pack=pack)["blocked"])
        # TW export matched, US import absent from the pack: a warning names the missing side.
        silent = cr.check("TW", "US", goods_tags=["cosmetics"], pack=pack)
        self.assertIn(("WARN", "import_rules_not_in_pack"), self.codes(silent))
        self.assertFalse(silent["blocked"])
        # Domestic: no export or import step.
        self.assertFalse(any(f["code"].startswith(("export_", "import_")) for f in cr.check("JP", "JP", goods_tags=["cosmetics"], pack=pack)["findings"]))

    def test_statute_map_pairs_mainland_and_taiwan_export_and_import_with_articles(self):
        pack = cr.load_pack()
        self.assertEqual({c: len(v["rules"]) for c, v in pack["export_rules"].items()}, {"AU": 28, "CA": 33, "CN": 32, "DE": 23, "GB": 34, "HK": 35, "JP": 28, "SG": 23, "TW": 39, "US": 38})
        self.assertEqual({c: len(v["rules"]) for c, v in pack["import_rules"].items()}, {"AU": 32, "CA": 42, "CN": 33, "DE": 44, "GB": 30, "HK": 32, "JP": 34, "SG": 35, "TW": 49, "US": 37})
        for table in ("export_rules", "import_rules"):
            for block in pack[table].values():
                for rule in block["rules"]:
                    self.assertTrue(rule["statute"] and rule["url"].startswith(("https://", "http://www.npc.gov.cn/")), rule["id"])
                    # A postal operator or postal law binds the post only, so it never bans a whole tag.
                    if rule.get("channel") == "post":
                        self.assertFalse(rule["tier"] == "prohibited" and rule["scope"] == "all", rule["id"])
        # Taiwan bans e-cigarettes on the way out (Tobacco Hazards Prevention Act art. 15): blocked even to the US,
        # which has no import rules in the pack.
        ecig = cr.check("TW", "US", goods_tags=["e_cigarettes"])
        self.assertIn(("BLOCK", "export_prohibited"), self.codes(ecig))
        self.assertTrue(any("第15條" in row["text"] for row in ecig["findings"] if row["code"] == "export_prohibited"))
        # Plants: restricted from the mainland into Taiwan, banned from Taiwan into the mainland.
        self.assertFalse(cr.check("CN", "TW", goods_tags=["plants_seeds"])["blocked"])
        # Into the mainland, posting plants is banned and seeds need quarantine approval: a warning, not a whole-tag ban.
        plants_in = cr.check("TW", "CN", goods_tags=["plants_seeds"])
        self.assertFalse(plants_in["blocked"])
        self.assertIn(("WARN", "import_prohibited"), self.codes(plants_in))
        # A subset rule (endangered species, relics) never blocks the whole tag on its own.
        for side, rules in (("export", pack["export_rules"]["CN"]["rules"]),):
            subset = [r for r in rules if r.get("scope") == "subset" and r["tier"] == "prohibited"]
            self.assertTrue(subset)
            found = cr.check("CN", "TW", goods_tags=[subset[0]["tag"]])
            self.assertTrue(any(row["code"] == f"{side}_prohibited" and row["severity"] == "WARN" for row in found["findings"]))

    def test_search_finds_the_official_clause_and_filters_by_country(self):
        top = cr.search("china personal account goods payments", 1)[0]
        self.assertEqual((top["country"], top["dimension"]), ("CN", "cross_border_currency"))
        self.assertTrue(all(hit["country"] in ("JP", "ALL") for hit in cr.search("risk hold days japan", 5)))
        with self.assertRaises(cr.CountryRulesError):
            cr.search("", 3)


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app(), base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55120))
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        session = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}

    def test_routes_return_the_check_and_refuse_free_text(self):
        listed = self.client.get("/api/v1/country-rules/countries", headers=self.headers).json()
        self.assertEqual(len(listed["countries"]), 10)
        result = self.client.post("/api/v1/country-rules/check", json={"seller_country": "CN", "buyer_country": "TW",
            "account_type": "personal", "account_opened": "after_cutoff", "goods_tags": ["live_animals"]}, headers=self.headers)
        self.assertEqual(result.status_code, 200, result.text)
        self.assertTrue(result.json()["blocked"])
        for body in ({"seller_country": "Mars", "buyer_country": "TW"}, {"seller_country": "US", "buyer_country": "TW", "note": "x"},
                     {"seller_country": "US", "buyer_country": "TW", "goods_tags": ["kittens"]}):
            self.assertEqual(self.client.post("/api/v1/country-rules/check", json=body, headers=self.headers).status_code, 422, body)
        hits = self.client.post("/api/v1/country-rules/search", json={"query": "taiwan withdraw local bank"}, headers=self.headers).json()["hits"]
        self.assertEqual(hits[0]["country"], "TW")



class InvoiceGateTests(RouteTests):
    def test_a_country_block_holds_the_invoice_review_on_the_server(self):
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body = {"description": "Handcrafted ceramic cup", "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": aup["evaluation_id"], "description_digest": aup["description_digest"]}
        blocked = self.client.post("/api/v1/country-rules/check", json={"seller_country": "CN", "buyer_country": "TW",
            "account_type": "personal", "account_opened": "after_cutoff"}, headers=self.headers)
        self.assertTrue(blocked.json()["blocked"])
        held = self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers)
        self.assertEqual((held.status_code, held.json()["error"]["code"]), (409, "country_rules_blocked"))
        self.client.post("/api/v1/country-rules/check", json={"seller_country": "US", "buyer_country": "US"}, headers=self.headers)
        self.assertEqual(self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers).status_code, 200)

    def test_a_review_token_minted_before_the_block_cannot_create_the_draft(self):
        """Red team 2026-11-03 F4: review, then a blocking check, then "Create draft" used to succeed."""
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body = {"description": "Handcrafted ceramic cup", "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": aup["evaluation_id"], "description_digest": aup["description_digest"]}
        review = self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers)
        self.assertEqual(review.status_code, 200, review.text)
        self.client.post("/api/v1/country-rules/check", json={"seller_country": "CN", "buyer_country": "TW",
            "account_type": "personal", "account_opened": "after_cutoff"}, headers=self.headers)
        draft = self.client.post("/api/v1/paypal/invoices/draft", json={"description": body["description"], "amount": "10.00",
            "currency": "USD", "review_token": review.json()["review_token"], "payload_digest": review.json()["payload_digest"]},
            headers=self.headers)
        self.assertEqual((draft.status_code, draft.json()["error"]["code"]), (409, "country_rules_blocked"))

    def _review_then_draft(self, before=None, after=None):
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body = {"description": "Handcrafted ceramic cup", "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": aup["evaluation_id"], "description_digest": aup["description_digest"]}
        if before:
            self.assertFalse(self.client.post("/api/v1/country-rules/check", json=before, headers=self.headers).json()["blocked"])
        review = self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers)
        self.assertEqual(review.status_code, 200, review.text)
        if after:
            self.assertFalse(self.client.post("/api/v1/country-rules/check", json=after, headers=self.headers).json()["blocked"])
        return self.client.post("/api/v1/paypal/invoices/draft", json={"description": body["description"], "amount": "10.00",
            "currency": "USD", "review_token": review.json()["review_token"], "payload_digest": review.json()["payload_digest"]},
            headers=self.headers)

    def test_a_route_change_after_review_holds_the_draft(self):
        """Red team 2026-11-03 F5: review A->B, then a non-blocking check C->D, kept the stale A->B draft note."""
        draft = self._review_then_draft(before={"seller_country": "US", "buyer_country": "US"},
                                        after={"seller_country": "GB", "buyer_country": "US"})
        self.assertEqual((draft.status_code, draft.json()["error"]["code"]), (409, "country_check_changed"))

    def test_the_same_route_checked_again_does_not_hold_the_draft(self):
        route = {"seller_country": "US", "buyer_country": "US"}
        draft = self._review_then_draft(before=route, after=route)
        code = (draft.json().get("error") or {}).get("code") if draft.status_code >= 400 else None
        self.assertNotIn(code, {"country_check_changed", "country_rules_blocked"}, draft.text)

    def test_reset_demo_forgets_the_country_stop_and_the_message_says_stop_not_hold(self):
        """Click-all 2026-11-03 #2 and PayPal-side F1: Reset clears the stop; the 409 text never says "holds"."""
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body = {"description": "Handcrafted ceramic cup", "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": aup["evaluation_id"], "description_digest": aup["description_digest"]}
        self.assertTrue(self.client.post("/api/v1/country-rules/check", json={"seller_country": "TW", "buyer_country": "US",
            "goods_tags": ["e_cigarettes"]}, headers=self.headers).json()["blocked"])
        held = self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers)
        self.assertEqual(held.status_code, 409)
        message = held.json()["error"]["message"]
        self.assertIn("won't create the draft: a listed country rule may apply to this sale", message)
        self.assertNotIn("hold", message.lower())
        self.assertEqual(self.client.post("/api/v1/demo/inject", json={"scenario": "reset"}, headers=self.headers).status_code, 200)
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body.update(evaluation_id=aup["evaluation_id"], description_digest=aup["description_digest"])
        self.assertEqual(self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers).status_code, 200)

    def test_a_review_with_no_country_check_is_not_held_by_the_country_gate(self):
        draft = self._review_then_draft()
        code = (draft.json().get("error") or {}).get("code") if draft.status_code >= 400 else None
        self.assertNotIn(code, {"country_check_changed", "country_rules_blocked"}, draft.text)


class RedTeamRegressionTests(unittest.TestCase):
    """Red team and gap review 2026-11-03: wrong BLOCK, wrong ALLOW and contract findings stay fixed."""

    def test_channel_rules_never_ban_a_whole_tag_and_cannot_cancel_a_statutory_ban(self):
        self.assertFalse(cr.check("TW", "CN", goods_tags=["food"])["blocked"])  # tea, pineapple cake
        self.assertFalse(cr.check("TW", "CN", goods_tags=["batteries_hazmat"])["blocked"])  # postal ban only
        pack = json.loads(json.dumps(cr.load_pack()))
        for block in (pack["export_rules"], pack["import_rules"]):
            for rules in block.values():
                for rule in rules["rules"]:
                    if rule.get("channel"):
                        self.assertFalse(rule["tier"] == "prohibited" and rule["scope"] == "all", rule["id"])
        # A postal restricted row next to a statutory ban must not turn the ban into a warning (F7).
        pack["import_rules"]["SG"]["rules"].append({"id": "X", "tag": "e_cigarettes", "tier": "restricted", "scope": "all",
            "channel": "post", "route": "*->SG", "rule": "r", "url": "https://www.singpost.com/x", "statute": "s",
            "article": None, "quantity_limit": None, "permit": None})
        self.assertTrue(cr.check("US", "SG", goods_tags=["e_cigarettes"], pack=pack)["blocked"])

    def test_sale_bans_hold_a_domestic_sale_and_eu_rules_reach_member_states(self):
        for code in ("SG", "HK", "TW"):
            self.assertTrue(cr.check(code, code, goods_tags=["e_cigarettes"])["blocked"], code)
        self.assertFalse(cr.check("US", "US", goods_tags=["e_cigarettes"])["blocked"])
        eu_rows = [rule for rule in cr.side_rules(cr.load_pack(), "import", "DE", "GB", "food") if rule["route"] == "EU->GB"]
        self.assertTrue(eu_rows)
        self.assertFalse([rule for rule in cr.side_rules(cr.load_pack(), "import", "US", "GB", "food") if rule["route"] == "EU->GB"])

    def test_approval_warnings_name_the_goods_like_the_panel(self):
        """Red team 2026-11-03 P2-4: "E cigarettes needs ..." lost its hyphen."""
        texts = [row["text"] for row in cr.check("US", "US", goods_tags=["e_cigarettes"])["findings"] if row["code"] == "aup_preapproval"]
        self.assertEqual(texts, ["E-cigarettes needs PayPal's approval before you accept payments for it."])

    def test_a_missing_side_is_named_for_approval_goods_too(self):
        codes = {row["code"] for row in cr.check("AU", "JP", goods_tags=["e_cigarettes"])["findings"]}
        self.assertTrue({"law_dependent", "export_rules_not_in_pack", "import_rules_not_in_pack"} & codes, codes)

    def test_every_finding_fits_the_frontend_contract(self):
        pack = cr.load_pack()
        tags = ["live_animals", "plants_seeds", "food", "cosmetics", "batteries_hazmat", "radio_wireless", "alcohol",
                "tobacco_other", "e_cigarettes", "prescription", "medical_devices", "jewellery_precious_metals", "currency",
                "cultural_relics", "weapons", "counterfeit"]
        for seller in pack["countries"]:
            for buyer in pack["countries"]:
                for tag in tags:
                    for row in cr.check(seller, buyer, goods_tags=[tag])["findings"]:
                        self.assertLessEqual(len(row["text"]), 1200, (seller, buyer, tag, row["code"]))



class RedTeamRound2Tests(unittest.TestCase):
    """Red team r2 2026-11-03: whole-tag bans are statutory, and the checked goods are bound to the draft."""

    def test_no_whole_tag_ban_carries_a_permit_or_a_channel_and_no_research_marker_reaches_text(self):
        pack = cr.load_pack()
        for table in ("export_rules", "import_rules"):
            for block in pack[table].values():
                for rule in block["rules"]:
                    if rule["tier"] == "prohibited" and rule.get("scope", "all") == "all":
                        self.assertFalse(rule.get("permit") or rule.get("channel"), rule["id"])
                    self.assertNotIn("NOT_FOUND", rule["rule"], rule["id"])
        self.assertFalse(cr.check("US", "CN", goods_tags=["live_animals"])["blocked"])  # carried or posted only
        self.assertTrue(cr.check("US", "SG", goods_tags=["e_cigarettes"])["blocked"])

    def test_sixteen_tags_fit_the_server_and_the_frontend_cap(self):
        tags = ["live_animals", "plants_seeds", "food", "cosmetics", "batteries_hazmat", "radio_wireless", "alcohol",
                "tobacco_other", "e_cigarettes", "prescription", "medical_devices", "jewellery_precious_metals", "currency",
                "cultural_relics", "weapons", "counterfeit"]
        pack = cr.load_pack()
        for seller in pack["countries"]:
            for buyer in pack["countries"]:
                self.assertLessEqual(len(cr.check(seller, buyer, goods_tags=tags)["findings"]), 120, (seller, buyer))


class SourceHostContractTests(unittest.TestCase):
    def test_every_pack_source_passes_the_frontend_host_allowlist(self):
        """Red team r2: the frontend contract rejects a result whose source host it does not know, and the panel then
        shows nothing. Node runs the regex from frontend/src/api.js against every URL in the pack."""
        import re
        import subprocess
        api = (cr.PACK_PATH.parents[2] / "frontend" / "src" / "api.js").read_text(encoding="utf-8")
        pattern = re.search(r"(/\^\(https:\S*?npc\\\.gov\\\.cn\)\\//)\.test\(row\.source\)", api)
        self.assertIsNotNone(pattern, "host regex not found in api.js")
        urls = [rule["url"] for table in ("export_rules", "import_rules")
                for block in cr.load_pack()[table].values() for rule in block["rules"]]
        script = f"const re={pattern.group(1)};const urls=JSON.parse(require('fs').readFileSync(0,'utf8'));" \
                 "process.stdout.write(JSON.stringify(urls.filter(u=>!re.test(u))))"
        result = subprocess.run(["node", "-e", script], input=json.dumps(urls), capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])


class GoodsBindingTests(RouteTests):
    def test_changing_the_ticked_goods_after_review_holds_the_draft(self):
        self.client.post("/api/v1/country-rules/check", json={"seller_country": "US", "buyer_country": "GB",
                                                               "goods_tags": ["cosmetics"]}, headers=self.headers)
        aup = self.client.post("/api/v1/aup/review", json={"description": "Handcrafted ceramic cup"}, headers=self.headers).json()
        body = {"description": "Handcrafted ceramic cup", "amount": "10.00", "currency": "USD", "confirm_sandbox_draft": True,
                "evaluation_id": aup["evaluation_id"], "description_digest": aup["description_digest"]}
        review = self.client.post("/api/v1/paypal/invoices/review", json=body, headers=self.headers).json()
        self.client.post("/api/v1/country-rules/check", json={"seller_country": "US", "buyer_country": "GB"}, headers=self.headers)
        draft = self.client.post("/api/v1/paypal/invoices/draft", json={"description": body["description"], "amount": "10.00",
            "currency": "USD", "review_token": review["review_token"], "payload_digest": review["payload_digest"]}, headers=self.headers)
        self.assertEqual((draft.status_code, draft.json()["error"]["code"]), (409, "country_check_changed"))


if __name__ == "__main__":
    unittest.main()
