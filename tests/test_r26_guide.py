"""Red team r26 #2 (2026-11-04): reported speech behind a seller subject, and dates from another verb."""
import datetime
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from payguard import evidence_guide as eg  # noqa: E402

TODAY = datetime.date(2026, 11, 4)


class ReportedSpeechBehindSellerSubject(unittest.TestCase):
    REPORTED = (
        "I heard from the buyer that it arrived last Monday",
        "We got a message from the customer saying it came on Tuesday",
        "I was told it arrived Monday",
        "I shipped it on Monday, the buyer says it never came",
        "I was told by the buyer it was delivered",
        "I was told the buyer was refunded",
        "The guy who bought it confirms it came",
    )
    OWN = (
        "I wrote to the buyer and they replied",
        "I shipped it last Friday",
        "I handed the parcel over at the counter on Thursday",
        "UPS says delivered",
    )

    def test_reported_speech_never_reaches_the_model(self):
        for clause in self.REPORTED:
            with self.subTest(clause=clause):
                self.assertIn(eg.reported_speaker(clause), ("BUYER", "THIRD_PARTY"))
                self.assertEqual(eg.model_clause_indices([clause]), [])

    def test_the_sellers_own_words_still_reach_the_model(self):
        for clause in self.OWN:
            with self.subTest(clause=clause):
                self.assertEqual(eg.model_clause_indices([clause]), [0])


class DatesFromOneVerbOnly(unittest.TestCase):
    def test_two_time_verbs_fix_no_date(self):
        self.assertIsNone(eg._clause_date("i shipped it last week and it arrived this friday", TODAY))

    def test_the_week_word_must_sit_next_to_the_weekday(self):
        self.assertEqual(eg._clause_date("i shipped it last friday", TODAY), "2026-10-30")
        self.assertEqual(eg._clause_date("i shipped it friday last week", TODAY), "2026-10-30")
        self.assertIsNone(eg._clause_date("last week i shipped it, maybe friday", TODAY))

    def test_a_model_week_hint_far_from_the_weekday_is_dropped(self):
        rows = eg.ground_hints([{"c": "ship_date", "k": 0, "s": "P", "w": "FRI", "r": "LAST"}],
                               ["I probably shipped it last week and the buyer got it this Friday"])
        self.assertIsNone(rows[0]["r"])


if __name__ == "__main__":
    unittest.main()
