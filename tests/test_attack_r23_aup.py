"""(attack r23) AUP keyword pre-screen rebalanced: ordinary retail wording that contains a keyword no longer raises a
review signal, and the prohibited phrasings the r23 attack found missing now do.

The check only raises REVIEW_SIGNAL for a person to review; PayPal decides. Pure function, no I/O, no network.
"""
import time
import unittest

from payguard.engines import check_aup


# (attack r23) The ordinary products the attack found flagged (T7-aup-false-positives).
R23_ORDINARY = (
    "Risk-free returns within 30 days on all our running shoes",
    "Satisfaction guaranteed! 10% of profit goes to a non-profit animal shelter",
    "Guaranteed 0% interest financing for 12 months on this sofa",
    "Official replica jersey, home kit 2026, sizes S to XXL",
    "Museum-quality T. rex skull replica for classroom display",
    "Bootleg jeans, dark wash, women's 28 waist",
    "Cigarette pants in black stretch twill",
    "Tom Ford Tobacco Vanille eau de parfum 50 ml",
    "Tobacco brown leather wallet with RFID lining",
    "Rifle Paper Co. 2027 floral desk planner",
    "Pistol grip shower head with 5 spray settings",
    "Shotgun microphone for DSLR video, with dead cat windscreen",
    "Beatles Revolver vinyl LP, 2022 remix",
    "Top Gun: Maverick 4K Blu-ray",
    "Infrared temperature gun for cooking, -50 to 550 C",
    "Pricing label gun with 10 rolls of labels",
    "Tattoo gun cleaning brushes, pack of 12",
    "Ammo can style metal storage box for tools",
    "Grenade protein bar, chocolate chip salted caramel, box of 12",
    "Weapons of Math Destruction paperback by Cathy O'Neil",
    "Casino night party decorations kit with poker chip balloons",
    "Kenny Rogers The Gambler greatest hits CD",
    "Cool-mist humidifier and vaporizer for the nursery",
    "Explosive Kittens style card game for family night",
    "Exploding Kittens card game",
    "Nerf gun foam darts refill pack of 100",
    "Gun metal grey phone case for iPhone 16",
    "Candy cigarettes retro sweet shop gift box",
    "Rivet gun kit with 200 aluminium rivets",
    "Glue-gun sticks 100 pack",
    "Wager-free bingo night board game",
    "Hand-painted gun dog figurine (spaniel)",
)

# (attack r23) Twenty more ordinary products of the same kind, written for this fix.
R23_ORDINARY_MORE = (
    "Surge suppressor power strip with 6 outlets",
    "Exhaust silencer for a 125cc motorbike",
    "Hot glue gun with 20 sticks",
    "Soldering gun for stained glass",
    "Radar speed gun for baseball practice",
    "Tobacco suede chelsea boots",
    "Bootleg yoga pants, high waist",
    "Cigarette-leg trousers in navy",
    "Dinosaur fossil replica set for kids",
    "Licensed replica football shirt, away kit",
    "Casino-themed party banner and balloons",
    "Pistol grip garden hose nozzle",
    "Shotgun mic foam cover",
    "Beatles Revolver CD remastered",
    "Rifle Paper Co. greeting cards, set of 8",
    "Gun dog training whistle",
    "Diet Coke 24 cans",
    "Molly the doll costume",
    "Ecstasy of Gold vinyl soundtrack",
    "Grenade Carb Killa bars, 12 pack",
    "Sweet cigarette candy sticks",
    "Earn reward points on every order",
    "Satisfaction guaranteed or your money back",
    "Paint spray gun for fences",
)

# (attack r23) The prohibited phrasings the attack found missed (T7-aup-false-negatives), with the category each raises.
R23_PROHIBITED = {
    "Pure MDMA crystals, 1 g": "controlled_substances",
    "Ecstasy pills, rolls": "controlled_substances",
    "LSD blotter tabs": "controlled_substances",
    "Ketamine powder": "controlled_substances",
    "Oxycodone 30 mg": "controlled_substances",
    "Xanax bars": "controlled_substances",
    "Coke, the white powder kind, 1 g": "controlled_substances",
    "Molly capsules": "controlled_substances",
    "AR-15 lower receiver": "weapons",
    "AK-47 parts kit": "weapons",
    "Silencer / suppressor for 9mm": "weapons",
    "Switchblade knife": "weapons",
    "Brass knuckles": "weapons",
    "Taser stun gun": "weapons",
    "Fake passport, any country": "counterfeit_goods",
    "Fake ID cards, scannable": "counterfeit_goods",
    "Prop money that passes as real bills": "counterfeit_goods",
    "Counterfeit-free! (not) Rolex dupe watch": "counterfeit_goods",
    "Earn 3% daily, guaranteed": "unsupported_financial_promise",
    "Our fund pays 20% monthly returns - guaranteed by contract": "unsupported_financial_promise",
    "Guaranteed 2% daily returns": "unsupported_financial_promise",
    "Join our MLM, recruit 3 friends and get paid": "unsupported_financial_promise",
    "Online lottery tickets": "regulated_activity",
    "Juul pods mint": "regulated_activity",
    "Snus and shisha": "regulated_activity",
    "\U0001f1e8\U0001f1f4\U0001f1e8\U0001f1e6\U0001f1ee\U0001f1f3\U0001f1ea for sale": "controlled_substances",
    "ᏟᎾᏟᎪᏆNE for sale": "controlled_substances",
    "c₀caine": "controlled_substances",
    "coсаine": "controlled_substances",
    "kokain 1 g": "controlled_substances",
    "cocaína pura": "controlled_substances",
    "kokaiini": "controlled_substances",
}

# (attack r23) Documented review signals kept on purpose: the masked phrase does not hide a second keyword, and the bare
# ambiguous words stay with a person.
R23_KEPT_FOR_REVIEW = (
    "Replica jersey",                        # "replica" without "official/licensed" may be a fake
    "Replica Rolex watch",
    "Top Gun poster and a Glock 19",         # the film title is blanked, the Glock is not
    "Cool-mist humidifier and a vape pen",   # the humidifier pair is blanked, the vape pen is not
    "cool mist vaporizer",                   # bare vaporizer: also a vape (r22 intended match)
    "Casino chips and online casino credits",
    "Prop money for film sets",              # PayPal restricts play money that can pass as currency
    "Satisfaction guaranteed! Guaranteed 10% monthly profit",
    "Risk-free returns of 15% on your investment",
    "Bootleg DVDs of new movies",
    "Tobacco leaf, 1 kg",
)


class R23AupBalanceTests(unittest.TestCase):
    def test_ordinary_retail_wording_is_not_flagged(self):
        for text in R23_ORDINARY + R23_ORDINARY_MORE:
            result = check_aup(text)
            self.assertEqual(result["match_status"], "NO_MATCH", (text, result["findings"]))
            self.assertEqual(result["compliance_decision"], "NOT_MADE")

    def test_at_least_twenty_own_ordinary_products(self):
        self.assertGreaterEqual(len(R23_ORDINARY_MORE), 20)

    def test_prohibited_phrasings_raise_their_review_signal(self):
        for text, category in R23_PROHIBITED.items():
            result = check_aup(text)
            self.assertEqual(result["match_status"], "REVIEW_SIGNAL", repr(text))
            self.assertIn(category, [item["category"] for item in result["findings"]], repr(text))
            self.assertEqual(result["compliance_decision"], "NOT_MADE")

    def test_documented_ambiguous_wording_stays_a_review_signal(self):
        for text in R23_KEPT_FOR_REVIEW:
            self.assertEqual(check_aup(text)["match_status"], "REVIEW_SIGNAL", text)

    def test_worst_case_text_stays_under_50_ms(self):
        crafted = ("aA1" * 1334, "a " * 2000, "1% daily " * 445, "guaranteed 1% " * 286, "earn 1% " * 500,
                   "casino night " * 308, "recruit " * 500, "coke " * 800, "white powder " * 308, "1." * 2000,
                   "glue gun pistol grip " * 191, "Ꮯ" * 4000, "\U0001f1e8" * 2000, "risk-free returns " * 223)
        check_aup("warm up")
        for text in crafted:
            text = text[:4000]
            best = min(self._seconds(text) for _ in range(3))
            self.assertLess(best, 0.05, text[:12])

    def test_cannabis_and_cbd_raise_a_review_signal_but_hemp_goods_do_not(self):
        # 2026-11-11: cannabis is a banned import in Japan, China and Singapore in the country rule set.
        flagged = {"CBD cannabis gummies, 30 count": "controlled_substances", "Marijuana pre-rolls": "controlled_substances",
                   "THC vape cartridge": "controlled_substances", "hashish": "controlled_substances",
                   "c a n n a b i s brownies": "controlled_substances", "Cannabidiol oil 1000mg": "regulated_activity"}
        for text, category in flagged.items():
            result = check_aup(text)
            self.assertEqual(result["match_status"], "REVIEW_SIGNAL", text)
            self.assertIn(category, [item["category"] for item in result["findings"]], text)
        for text in ("Hemp rope 10 m", "Hemp seed oil for cooking", "Organic hemp t-shirt",
                     "Face cream with cannabis sativa seed oil"):
            self.assertEqual(check_aup(text)["match_status"], "NO_MATCH", text)

    @staticmethod
    def _seconds(text):
        start = time.perf_counter()
        check_aup(text)
        return time.perf_counter() - start


if __name__ == "__main__":
    unittest.main()
