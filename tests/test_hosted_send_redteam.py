"""Red team 2026-11-10 (hosted live send) regressions: one address cannot use up the Sandbox dispute stock by opening new
sessions (A1), a send without a known client key never reaches the transport, and racing sends from several sessions
to one dispute send once (A4). Synthetic MockTransport only; no network."""

import asyncio
import unittest

from app import demo_mode
from app.demo_mode import (HOSTED_SEND_CLIENT, HOSTED_SEND_CLIENT_CODE, HOSTED_SEND_SESSION, HostedReadOnlyPaypalAdapter,
                           SendBudget)
from app.store import BoundaryError
from test_hosted_sandbox_send import REAL_IDS, HostedSendBase


class SlowInner:
    def __init__(self):
        self.sent = []

    async def provide_evidence(self, real, _parts):
        await asyncio.sleep(0.02)
        self.sent.append(real)
        return {"status_code": 200, "dispute_id": real, "paypal_debug_id": "abc123def4567"}


def run_send(adapter, code, session_id, client):
    async def one():
        HOSTED_SEND_SESSION.set(session_id)
        HOSTED_SEND_CLIENT.set(client)
        return await adapter.provide_evidence(code, {"input": (None, "{}", "application/json")})
    return asyncio.run(one())


class OneAddressCannotUseUpTheStock(HostedSendBase):
    def test_new_sessions_from_one_address_stop_at_the_per_client_cap(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 200)
        results = []
        for code in self.codes():
            headers = self.new_session()
            headers["X-Forwarded-For"] = "198.51.100.200"
            self.prepare(code, headers)
            response = self.send(code, headers)
            results.append((response.status_code, response.json().get("error", {}).get("code")))
        self.assertEqual(results[:2], [(200, None), (200, None)])
        self.assertEqual(results[2], (409, HOSTED_SEND_CLIENT_CODE))
        self.assertEqual(len(self.provider.sends()), demo_mode.HOSTED_SENDS_PER_CLIENT_PER_DAY)
        # Another address still has its own share (the shared window cap of 3 is the next limit).
        other = self.new_session()
        self.assertEqual(self.get("/connections", other).json()["send_state"]["sends_left_window"], 1)


class WrapperClientKey(unittest.TestCase):
    def test_send_without_a_client_key_is_refused_before_the_transport(self):
        inner = SlowInner()
        adapter = HostedReadOnlyPaypalAdapter(inner, send_enabled=True)
        code = adapter._code_for(REAL_IDS[0])
        for client in (None, ""):
            with self.assertRaises(BoundaryError) as caught:
                run_send(adapter, code, "s1", client)
            self.assertEqual(caught.exception.code, demo_mode.HOSTED_DEMO_CODE)
        self.assertEqual(inner.sent, [])

    def test_per_client_cap_frees_after_24_hours(self):
        clock = [1000.0]
        inner = SlowInner()
        adapter = HostedReadOnlyPaypalAdapter(inner, send_enabled=True,
                                              send_budget=SendBudget(per_window=10, per_day=10, clock=lambda: clock[0]))
        codes = [adapter._code_for(real) for real in REAL_IDS]
        run_send(adapter, codes[0], "s1", "203.0.113.1")
        run_send(adapter, codes[1], "s2", "203.0.113.1")
        with self.assertRaises(BoundaryError) as caught:
            run_send(adapter, codes[2], "s3", "203.0.113.1")
        self.assertEqual(caught.exception.code, HOSTED_SEND_CLIENT_CODE)
        clock[0] += 86400
        self.assertEqual(run_send(adapter, codes[2], "s4", "203.0.113.1")["dispute_id"], codes[2])
        self.assertEqual(inner.sent, list(REAL_IDS))

    def test_racing_sessions_on_one_dispute_send_once(self):
        inner = SlowInner()
        adapter = HostedReadOnlyPaypalAdapter(inner, send_enabled=True, send_budget=SendBudget(per_window=10, per_day=10))
        code = adapter._code_for(REAL_IDS[0])

        async def one(index):
            HOSTED_SEND_SESSION.set(f"s{index}")
            HOSTED_SEND_CLIENT.set(f"203.0.113.{index}")
            try:
                return await adapter.provide_evidence(code, {"input": (None, "{}", "application/json")})
            except BoundaryError as error:
                return error.code

        async def race():
            return await asyncio.gather(*(asyncio.create_task(one(index)) for index in range(5)))

        results = asyncio.run(race())
        self.assertEqual(inner.sent, [REAL_IDS[0]])
        self.assertEqual(sorted(item for item in results if isinstance(item, str)), ["evidence_already_submitted"] * 4)
        self.assertNotIn(REAL_IDS[0], repr(results))


if __name__ == "__main__":
    unittest.main()
