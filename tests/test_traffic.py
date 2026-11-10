"""Traffic control (owner 2026-11-03): per-visitor session limits, pacing of high-frequency addresses, queued bursts."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import unittest

from app.store import CLIENT_CREATIONS_PER_MINUTE, CLIENT_MAX_LIVE_SESSIONS, BoundaryError, SessionStore
from app.traffic import TrafficGate, client_key


class Clock:
    def __init__(self):
        self.now = datetime(2026, 11, 3, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


def scope(path="/api/v1/demo/state", forwarded=None, client="127.0.0.1"):
    headers = [(b"host", b"example.invalid")]
    if forwarded is not None:
        headers.append((b"x-forwarded-for", forwarded.encode()))
    return {"type": "http", "path": path, "method": "GET", "headers": headers, "client": (client, 5000)}


async def run(gate, item):
    sent = []

    async def receive():
        return {"type": "http.request", "body": b""}

    async def send(message):
        sent.append(message)

    await gate(item, receive, send)
    start = next(message for message in sent if message["type"] == "http.response.start")
    return start["status"], dict(start.get("headers", []))


async def ok_app(scope, receive, send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"{}"})


class ClientKeyTests(unittest.TestCase):
    def test_behind_the_proxy_the_right_most_hop_wins_and_left_entries_cannot_spoof_it(self):
        self.assertEqual(client_key(scope(forwarded="203.0.113.7"), proxied=True), "203.0.113.7")
        self.assertEqual(client_key(scope(forwarded="1.2.3.4, 203.0.113.7"), proxied=True), "203.0.113.7")
        self.assertEqual(client_key(scope(forwarded="not-an-ip"), proxied=True), "invalid-forwarded")
        self.assertEqual(client_key(scope(forwarded="1.2.3.4"), proxied=False), "127.0.0.1")

    def test_the_trusted_hop_is_configurable_and_a_bad_value_falls_back_to_the_right_most(self):
        # r24: Render's hop count is undocumented; the owner sets PAYGUARD_CLIENT_IP_HOP after reading the hop log.
        from unittest import mock
        from app.traffic import configured_hop
        item = scope(forwarded="198.51.100.9, 10.0.0.2")
        self.assertEqual(client_key(item, proxied=True, hop=1), "10.0.0.2")
        self.assertEqual(client_key(item, proxied=True, hop=2), "198.51.100.9")
        # (red team 2026-11-10 P2-1, intended change) A header shorter than the trusted hop has no trusted entry: every
        # such request shares one bucket instead of using the visitor-written left-most entry.
        self.assertEqual(client_key(item, proxied=True, hop=5), "short-forwarded", "a short header fails closed")
        self.assertEqual(client_key(scope(forwarded="203.0.113.50, 10.0.0.2"), proxied=True, hop=3), "short-forwarded")
        self.assertEqual(client_key(scope(forwarded="203.0.113.51"), proxied=True, hop=3), "short-forwarded",
                         "two forged short headers land in the same bucket")
        self.assertEqual(client_key(scope(forwarded="203.0.113.7, 10.0.0.2, 10.0.0.3"), proxied=True, hop=3), "203.0.113.7")
        for raw, expected in (("2", 2), ("0", 1), ("9", 1), ("x", 1)):
            with mock.patch.dict("os.environ", {"PAYGUARD_CLIENT_IP_HOP": raw}):
                self.assertEqual(configured_hop(), expected, raw)

    def test_one_ipv6_slash_64_is_one_visitor_and_a_mapped_ipv4_is_its_ipv4(self):
        # attack r23: 1000 addresses inside one /64 got 1000 separate limits.
        first = client_key(scope(forwarded="2001:db8:1:2::1"), proxied=True)
        self.assertEqual(first, client_key(scope(forwarded="2001:db8:1:2:ffff::9"), proxied=True))
        self.assertNotEqual(first, client_key(scope(forwarded="2001:db8:1:3::1"), proxied=True))
        self.assertEqual(client_key(scope(forwarded="::ffff:203.0.113.7"), proxied=True), "203.0.113.7")


class PacingTests(unittest.TestCase):
    def make(self, **overrides):
        self.time = [1000.0]
        self.slept = []

        async def fake_sleep(seconds):
            self.slept.append(seconds)

        return TrafficGate(ok_app, proxied=True, clock=lambda: self.time[0], sleep=fake_sleep, **overrides)

    def test_a_burst_runs_at_once_then_requests_are_slowed_not_refused(self):
        gate = self.make(pace_per_second=5, burst=20)
        statuses = [asyncio.run(run(gate, scope(forwarded="198.51.100.1")))[0] for _ in range(22)]
        self.assertEqual(statuses, [200] * 22)
        self.assertEqual(len(self.slept), 2, "only the two requests past the burst wait")
        self.assertAlmostEqual(self.slept[0], 0.2, places=3)

    def test_the_hard_limit_answers_429_with_retry_after_and_other_visitors_are_unaffected(self):
        gate = self.make(pace_per_second=1000, burst=1000, hard_per_minute=5)
        for _ in range(5):
            self.assertEqual(asyncio.run(run(gate, scope(forwarded="198.51.100.2")))[0], 200)
        status, headers = asyncio.run(run(gate, scope(forwarded="198.51.100.2")))
        self.assertEqual(status, 429)
        self.assertIn(b"retry-after", headers)
        self.assertEqual(asyncio.run(run(gate, scope(forwarded="198.51.100.3")))[0], 200)

    def test_a_too_long_pace_delay_is_refused_instead_of_held(self):
        gate = self.make(pace_per_second=0.1, burst=1)
        self.assertEqual(asyncio.run(run(gate, scope(forwarded="198.51.100.4")))[0], 200)
        status, headers = asyncio.run(run(gate, scope(forwarded="198.51.100.4")))
        self.assertEqual(status, 429)
        self.assertEqual(int(headers[b"retry-after"]), 10)

    def test_a_refused_request_takes_no_token_so_honouring_retry_after_works(self):
        # attack r23: refusals used to use up tokens, so waiting Retry-After seconds still got 429.
        gate = self.make(pace_per_second=1, burst=1)
        self.assertEqual(asyncio.run(run(gate, scope(forwarded="198.51.100.6")))[0], 200)
        for _ in range(5):
            asyncio.run(run(gate, scope(forwarded="198.51.100.6")))
        refused = [status for status in (asyncio.run(run(gate, scope(forwarded="198.51.100.6")))[0] for _ in range(3))]
        self.time[0] += 1.0
        self.assertEqual(asyncio.run(run(gate, scope(forwarded="198.51.100.6")))[0], 200, refused)

    def test_static_pages_are_not_paced(self):
        gate = self.make(hard_per_minute=1)
        for _ in range(5):
            self.assertEqual(asyncio.run(run(gate, scope(path="/index.html", forwarded="198.51.100.5")))[0], 200)


class QueueTests(unittest.TestCase):
    def test_requests_past_the_in_flight_limit_wait_in_line_and_a_full_line_answers_503(self):
        release = None

        async def slow_app(scope, receive, send):
            await release.wait()
            await ok_app(scope, receive, send)

        async def scenario():
            nonlocal release
            release = asyncio.Event()
            gate = TrafficGate(slow_app, proxied=True, max_in_flight=1, max_queue=1, queue_wait=5,
                               pace_per_second=1000, burst=1000)
            first = asyncio.create_task(run(gate, scope(forwarded="192.0.2.1")))
            await asyncio.sleep(0)
            second = asyncio.create_task(run(gate, scope(forwarded="192.0.2.2")))
            await asyncio.sleep(0)
            third = await run(gate, scope(forwarded="192.0.2.3"))
            release.set()
            return (await first)[0], (await second)[0], third

        first, second, (third, headers) = asyncio.run(scenario())
        self.assertEqual((first, second), (200, 200), "the second request waited for the first, then ran")
        self.assertEqual(third, 503)
        self.assertIn(b"retry-after", headers)


class HopLogTests(unittest.TestCase):
    def test_the_hosted_gate_logs_hop_counts_only_never_addresses(self):
        gate = TrafficGate(ok_app, proxied=True, pace_per_second=1000, burst=1000)
        with self.assertLogs("payguard.traffic", level="WARNING") as logs:
            asyncio.run(run(gate, scope(forwarded="203.0.113.50, 10.0.0.9")))
        self.assertEqual(logs.output, ["WARNING:payguard.traffic:payguard traffic: x-forwarded-for hops=2 using_hop=1"])
        self.assertNotIn("203.0.113.50", "".join(logs.output))


class QueueExemptTests(unittest.TestCase):
    def test_new_session_requests_never_hold_a_shared_in_flight_slot(self):
        # attack r23 P1-1: eight waiting session requests from one address stalled every other visitor.
        release = None

        async def slow_app(scope, receive, send):
            if scope["path"] == "/api/v1/demo/sessions":
                await release.wait()
            await ok_app(scope, receive, send)

        async def scenario():
            nonlocal release
            release = asyncio.Event()
            gate = TrafficGate(slow_app, proxied=True, max_in_flight=1, max_queue=4, queue_wait=1,
                               pace_per_second=1000, burst=1000)
            waiting = [asyncio.create_task(run(gate, scope(path="/api/v1/demo/sessions", forwarded="192.0.2.9")))
                       for _ in range(3)]
            await asyncio.sleep(0)
            other = await run(gate, scope(forwarded="192.0.2.10"))
            release.set()
            await asyncio.gather(*waiting)
            return other[0]

        self.assertEqual(asyncio.run(scenario()), 200)


class PerVisitorSessionTests(unittest.TestCase):
    def store(self):
        self.clock = Clock()
        store = SessionStore(clock=self.clock)
        store.per_client_limits = True
        return store

    def test_one_visitor_cannot_use_up_session_creation_for_everyone(self):
        store = self.store()
        for _ in range(CLIENT_CREATIONS_PER_MINUTE):
            store.create("203.0.113.10")
        self.assertGreater(store.creation_wait("203.0.113.10"), 0)
        with self.assertRaises(BoundaryError):
            store.create("203.0.113.10")
        self.assertEqual(store.creation_wait("203.0.113.11"), 0)
        store.create("203.0.113.11")
        self.clock.now += timedelta(seconds=61)
        self.assertEqual(store.creation_wait("203.0.113.10"), 0)

    def test_one_visitor_holds_at_most_the_live_cap_and_only_its_own_sessions_make_room(self):
        store = self.store()
        other = store.create("203.0.113.20")["session_id"]
        for wave in range(3):
            for _ in range(CLIENT_CREATIONS_PER_MINUTE):
                store.create("203.0.113.21")
            self.clock.now += timedelta(seconds=61)
        mine = [session for session in store.sessions.values() if session.client_key == "203.0.113.21"]
        self.assertEqual(len(mine), CLIENT_MAX_LIVE_SESSIONS)
        self.assertIn(other, store.sessions, "another visitor's session is never dropped")

    def test_the_local_console_keeps_its_single_operator_limit(self):
        store = SessionStore(clock=Clock())
        for _ in range(12):
            store.create("anything")
        self.assertTrue(all(session.client_key == "local" for session in store.sessions.values()))


if __name__ == "__main__":
    unittest.main()
