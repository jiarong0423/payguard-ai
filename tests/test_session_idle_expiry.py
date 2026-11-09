"""Owner 2026-11-10: the demo session ends after ttl_seconds without a request (idle expiry), not at a fixed time.

A judge still clicking after 15 minutes kept losing every result. Each accepted request moves the end forward, an idle
session still ends, and no session lives past SESSION_MAX_AGE_SECONDS after creation.
"""
import unittest
from datetime import datetime, timedelta, timezone

from app.store import SESSION_MAX_AGE_SECONDS, BoundaryError, SessionStore


class Clock:
    def __init__(self):
        self.now = datetime(2026, 11, 10, 2, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


class SessionIdleExpiryTest(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock, ttl_seconds=900)
        self.session_id = self.store.create()["session_id"]

    def step(self, seconds):
        self.clock.now += timedelta(seconds=seconds)

    def test_activity_keeps_the_session_alive_past_the_first_ttl(self):
        for _ in range(4):  # 4 x 10 minutes = 40 minutes of use, longer than the 15-minute ttl
            self.step(600)
            session = self.store.require(self.session_id)
        self.assertEqual(session.expires_at, self.clock.now + timedelta(seconds=900))

    def test_an_idle_session_still_ends(self):
        self.step(600)
        self.store.require(self.session_id)
        self.step(901)
        with self.assertRaises(BoundaryError) as refused:
            self.store.require(self.session_id)
        self.assertEqual(refused.exception.status, 401)

    def test_no_session_outlives_the_maximum_age(self):
        created = self.clock.now
        while self.clock.now - created < timedelta(seconds=SESSION_MAX_AGE_SECONDS - 600):
            self.step(600)
            session = self.store.require(self.session_id)
        self.assertLessEqual(session.expires_at, created + timedelta(seconds=SESSION_MAX_AGE_SECONDS))
        self.clock.now = created + timedelta(seconds=SESSION_MAX_AGE_SECONDS + 1)
        with self.assertRaises(BoundaryError):
            self.store.require(self.session_id)

    def test_the_end_never_moves_earlier(self):
        before = self.store.require(self.session_id).expires_at
        self.store.require(self.session_id)
        self.assertGreaterEqual(self.store.require(self.session_id).expires_at, before)


if __name__ == "__main__":
    unittest.main()
