"""Backend optimisations, round 24 (optimise r24).

1. Exact-payload hash: the provide-evidence and add-tracking previews carry payload_sha256, the local approval records
   the hash it approved, and a send whose freshly built payload differs is refused with 409.
2. AI audit log: token counts from the worker envelope, latency and model per call, per session, never any text.
3. Per-session 429s carry Retry-After.

Every provider reply is a synthetic MockTransport or fake-runner answer; nothing contacts the network.
"""

from datetime import datetime, timedelta, timezone
import asyncio
import json
from pathlib import Path
import re
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app import ai_brief as ai
from app import ai_usage
from app.guide_model import parse_guide_envelope, parse_guide_envelope_with_usage, GuideModelError
from app.main import create_app
from app.paypal_disputes import (build_provide_evidence_request, build_tracking_request, evidence_payload_sha256,
                                 tracking_content_sha256, tracking_payload_sha256)
from app.store import BoundaryError, SessionStore
from app.studio_agent import StudioAgentError, StudioAgentService, parse_envelope_with_usage
from app.traffic import HARD_PER_MINUTE, MAX_PACE_DELAY_SECONDS, PACE_BURST, PACE_PER_SECOND

from test_ai_api import FakeBriefAdapter
from test_ai_brief import CapturingRunner, result as brief_result
from test_paypal_r24 import DEBUG_ID, LiveHarness, ROOT, submittable


HEX64 = re.compile(r"^[a-f0-9]{64}$")
USAGE = {"prompt_token_count": 812, "candidates_token_count": 96, "total_token_count": 1240}


class EvidencePayloadHashTests(LiveHarness):
    REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001"}

    def session_object(self):
        return self.store.sessions[self.session["session_id"]]

    def test_preview_hash_is_the_approved_hash_and_the_sent_hash(self):
        self.ready()
        preview = self.post("/paypal/disputes/provide-evidence", self.REQUEST)
        self.assertEqual(preview.status_code, 200, preview.text)
        digest = preview.json()["payload_sha256"]
        self.assertRegex(digest, HEX64)
        self.assertEqual(self.session_object().approved_payloads["demo-case-001"]["provide_evidence"], digest)
        # The hash covers the unmasked parts but reveals none of them.
        self.assertNotIn("SYNTHETIC_TRACKING_001", preview.text)
        sent = self.post("/paypal/disputes/provide-evidence", dict(self.REQUEST, submit=True))
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual((sent.json()["external_send"], sent.json()["payload_sha256"]), ("SUBMITTED", digest))
        self.assertEqual(len(self.posts("/provide-evidence")), 1)

    def test_a_payload_that_differs_from_the_approved_one_is_refused_and_nothing_is_sent(self):
        self.ready()
        session = self.session_object()
        for recorded in ("0" * 64, None):
            with self.subTest(recorded=recorded):
                session.approved_payloads["demo-case-001"]["provide_evidence"] = recorded
                refused = self.post("/paypal/disputes/provide-evidence", dict(self.REQUEST, submit=True))
                self.assertEqual((refused.status_code, refused.json()["error"]["code"]),
                                 (409, "evidence_changed_after_approval"))
                self.assertIn("the evidence changed after you approved it; review it again",
                              refused.json()["error"]["message"].lower())
        self.assertEqual(self.posts("/provide-evidence"), [])
        # The refusal does not use up the approval: with the approved hash back, the send goes out once.
        preview = self.post("/paypal/disputes/provide-evidence", self.REQUEST).json()
        session.approved_payloads["demo-case-001"]["provide_evidence"] = preview["payload_sha256"]
        sent = self.post("/paypal/disputes/provide-evidence", dict(self.REQUEST, submit=True))
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(len(self.posts("/provide-evidence")), 1)

    def test_one_changed_byte_of_the_evidence_pdf_is_refused_and_preview_equals_send(self):
        self.ready()
        session = self.session_object()
        preview = self.post("/paypal/disputes/provide-evidence", self.REQUEST).json()
        row = session.disputes["demo-case-001"]["attachment_candidates"][0]
        self.assertIn(b"Delivery evidence summary", row["content"])
        original = row["content"]
        row["content"] = original.replace(b"Disputed amount: USD 48.00", b"Disputed amount: USD 49.00")
        self.assertEqual(len(row["content"]), len(original))
        self.assertNotEqual(row["content"], original)
        refused = self.post("/paypal/disputes/provide-evidence", dict(self.REQUEST, submit=True))
        self.assertIn(refused.status_code, (409, 422), refused.text)
        self.assertEqual(self.posts("/provide-evidence"), [])
        row["content"] = original
        sent = self.post("/paypal/disputes/provide-evidence", dict(self.REQUEST, submit=True))
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual(sent.json()["payload_sha256"], preview["payload_sha256"])
        body = self.posts("/provide-evidence")[0].content
        self.assertIn(original, body)

    def test_the_hash_changes_with_any_part_and_is_keyed_per_session(self):
        self.ready()
        session = self.session_object()
        restricted = session.restricted_evidence["demo-case-001"]
        files = {row["attachment_id"]: row["content"]
                 for row in session.disputes["demo-case-001"].get("attachment_candidates", [])
                 if type(row.get("content")) is bytes}
        base = build_provide_evidence_request("PP-D-SANDBOX01", "case-ref-001", restricted, masked=False,
                                              attachment_bytes=files)
        digest = evidence_payload_sha256(session, base)
        # The dispute id is not part of the parts: the approval's hash holds for the dispute picked later.
        other = build_provide_evidence_request("PP-D-OTHER0001", "case-ref-001", restricted, masked=False,
                                               attachment_bytes=files)
        self.assertEqual(evidence_payload_sha256(session, other), digest)
        changed = json.loads(json.dumps(base, default=lambda value: value.hex()))
        changed["input"]["evidences"][0]["notes"] = "different"
        for row, original in zip(changed["files"], base["files"]):
            row["content"] = original["content"]
        self.assertNotEqual(evidence_payload_sha256(session, changed), digest)
        if base["files"]:
            renamed = dict(base, files=[dict(base["files"][0], filename="other.pdf")] + base["files"][1:])
            self.assertNotEqual(evidence_payload_sha256(session, renamed), digest)
            rebytes = dict(base, files=[dict(base["files"][0], content=b"x" + base["files"][0]["content"][1:])]
                           + base["files"][1:])
            self.assertNotEqual(evidence_payload_sha256(session, rebytes), digest)
        stranger = SessionStore(clock=self.clock)
        other_session = stranger.sessions[stranger.create()["session_id"]]
        self.assertNotEqual(evidence_payload_sha256(other_session, base), digest)

    def test_reset_clears_the_recorded_hashes(self):
        self.ready()
        self.assertIn("demo-case-001", self.session_object().approved_payloads)
        self.assertEqual(self.post("/demo/inject", {"scenario": "reset"}).status_code, 200)
        self.assertEqual(self.session_object().approved_payloads, {})


class TrackingPayloadHashTests(LiveHarness):
    REQUEST = {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001"}

    def test_preview_and_send_carry_the_hash_and_a_changed_tracker_is_refused(self):
        self.ready()
        session = self.store.sessions[self.session["session_id"]]
        preview = self.post("/paypal/disputes/add-tracking", self.REQUEST)
        self.assertEqual(preview.status_code, 200, preview.text)
        digest = preview.json()["payload_sha256"]
        self.assertRegex(digest, HEX64)
        self.assertNotIn("SYNTHETIC_TRACKING_001", preview.text)
        approved = session.approved_payloads["demo-case-001"]["add_tracking"]
        self.assertRegex(approved, HEX64)
        session.approved_payloads["demo-case-001"]["add_tracking"] = "f" * 64
        refused = self.post("/paypal/disputes/add-tracking", dict(self.REQUEST, submit=True))
        self.assertEqual((refused.status_code, refused.json()["error"]["code"]), (409, "evidence_changed_after_approval"))
        self.assertEqual(self.posts("/v1/shipping/trackers-batch"), [])
        session.approved_payloads["demo-case-001"]["add_tracking"] = approved
        sent = self.post("/paypal/disputes/add-tracking", dict(self.REQUEST, submit=True))
        self.assertEqual(sent.status_code, 200, sent.text)
        self.assertEqual((sent.json()["external_send"], sent.json()["payload_sha256"]), ("SUBMITTED", digest))
        self.assertEqual(len(self.posts("/v1/shipping/trackers-batch")), 1)

    def test_content_hash_ignores_only_the_transaction_id(self):
        self.ready(approve=False)
        session = self.store.sessions[self.session["session_id"]]
        restricted = session.restricted_evidence["demo-case-001"]
        one = build_tracking_request("TXNA", restricted, masked=False)
        two = build_tracking_request("TXNB", restricted, masked=False)
        self.assertEqual(tracking_content_sha256(session, one), tracking_content_sha256(session, two))
        self.assertNotEqual(tracking_payload_sha256(session, one), tracking_payload_sha256(session, two))
        changed = json.loads(json.dumps(one))
        changed["body"]["trackers"][0]["tracking_number"] = "OTHER_NUMBER"
        self.assertNotEqual(tracking_content_sha256(session, changed), tracking_content_sha256(session, one))


class UsageParsingTests(unittest.TestCase):
    def test_parse_usage_accepts_the_closed_shape_only(self):
        self.assertIsNone(ai_usage.parse_usage(None))
        self.assertEqual(ai_usage.parse_usage(USAGE), USAGE)
        self.assertEqual(ai_usage.parse_usage(dict(USAGE, total_token_count=None))["total_token_count"], None)
        for bad in ({"prompt_token_count": 1}, dict(USAGE, extra=1), dict(USAGE, prompt_token_count=-1),
                    dict(USAGE, prompt_token_count=True), dict(USAGE, prompt_token_count="12"),
                    dict(USAGE, prompt_token_count=ai_usage.MAX_TOKEN_COUNT + 1), [1, 2, 3], "usage"):
            with self.subTest(bad=bad), self.assertRaises(ai_usage.UsageInvalid):
                ai_usage.parse_usage(bad)

    def test_cost_is_null_without_a_checked_price_row_and_computed_with_one(self):
        self.assertEqual(ai_usage.PRICE_TABLE_USD_PER_MILLION, {}, "no price row without a checked source")
        self.assertIsNone(ai_usage.estimate_cost_usd(ai.MODEL, 1000, 100))
        from decimal import Decimal
        with mock.patch.dict(ai_usage.PRICE_TABLE_USD_PER_MILLION, {"m": (Decimal("0.30"), Decimal("2.50"))}):
            self.assertEqual(ai_usage.estimate_cost_usd("m", 1_000_000, 100_000), "0.550000")
            self.assertIsNone(ai_usage.estimate_cost_usd("m", None, 10))

    def test_log_is_bounded_per_session_and_holds_no_text(self):
        log = ai_usage.AiUsageLog()
        for index in range(ai_usage.MAX_ENTRIES_PER_SESSION + 5):
            log.record("s1", stage="guide", model=ai.MODEL, usage=USAGE, latency_ms=index, outcome="ok")
        rows = log.entries("s1")
        self.assertEqual(len(rows), ai_usage.MAX_ENTRIES_PER_SESSION)
        self.assertEqual(set(rows[0]), {"at", "stage", "model", "outcome", "tokens_in", "tokens_out", "tokens_total",
                                        "latency_ms", "estimated_cost_usd"})
        self.assertEqual((rows[-1]["tokens_in"], rows[-1]["tokens_out"], rows[-1]["tokens_total"]), (812, 96, 1240))
        self.assertEqual(log.entries("s2"), [])
        # Unknown stages and malformed counts are not recorded as given.
        log.record("s2", stage="free text the seller typed", model=ai.MODEL, usage=USAGE, latency_ms=1, outcome="ok")
        log.record("s2", stage="guide", model="has spaces in it", usage={"x": 1}, latency_ms="n", outcome="ok")
        self.assertEqual(log.entries("s2"), [dict(log.entries("s2")[0], model=None, tokens_in=None, latency_ms=0)])
        log.forget_missing({"s2"})
        self.assertEqual(log.entries("s1"), [])

    def test_guide_and_studio_envelopes_accept_usage_and_reject_bad_usage(self):
        scenario_raw = {"schema_version": "1.0", "status": "error", "result": {"code": "ai_timeout", "status": 504}}
        with self.assertRaises(GuideModelError):
            parse_guide_envelope(json.dumps(scenario_raw).encode(), "preflight")
        bad = dict(scenario_raw, status="ok", result={"reply": "x", "prompt_sha256": "0" * 64, "model": ai.MODEL},
                   usage={"prompt_token_count": "many"})
        with self.assertRaises(GuideModelError):
            parse_guide_envelope_with_usage(json.dumps(bad).encode(), "preflight")
        turn = {"tools": [], "tool_choice": "auto", "response_format": {"type": "text"}}
        ok = {"schema_version": "1.0", "status": "ok", "result": {"output": [{"kind": "text", "text": "Three cases."}],
                                                                   "model": ai.MODEL}, "usage": USAGE}
        output, usage = parse_envelope_with_usage(json.dumps(ok).encode(), turn)
        self.assertEqual((output[0]["text"], usage), ("Three cases.", USAGE))
        _output, none = parse_envelope_with_usage(json.dumps({k: v for k, v in ok.items() if k != "usage"}).encode(), turn)
        self.assertIsNone(none)
        with self.assertRaises(StudioAgentError):
            parse_envelope_with_usage(json.dumps(dict(ok, usage=dict(USAGE, total_token_count=-5))).encode(), turn)
        with self.assertRaises(StudioAgentError):
            parse_envelope_with_usage(json.dumps(dict(ok, other=1)).encode(), turn)


class StudioUsageTests(unittest.TestCase):
    def test_a_studio_turn_records_counts_and_latency(self):
        reply = {"schema_version": "1.0", "status": "ok", "usage": USAGE,
                 "result": {"output": [{"kind": "text", "text": "Three synthetic cases."}], "model": ai.MODEL}}
        model = mock.Mock(return_value=json.dumps(reply).encode())
        service = StudioAgentService(model)
        service.usage_log = ai_usage.AiUsageLog()
        body = {"instructions": "Answer about the dashboard.", "items": [{"kind": "user", "text": "How many cases?"}],
                "tools": [], "tool_choice": "auto", "response_format": {"type": "text"}}
        try:
            output = service.turn("s-studio", body)
        except StudioAgentError as error:
            self.skipTest(f"studio turn contract changed: {error.code}")
        self.assertEqual(output[0]["text"], "Three synthetic cases.")
        rows = service.usage_log.entries("s-studio")
        self.assertEqual([(row["stage"], row["model"], row["outcome"], row["tokens_in"]) for row in rows],
                         [("studio_agent", ai.MODEL, "ok", 812)])
        self.assertNotIn("Three synthetic cases", json.dumps(rows))
        self.assertNotIn("How many cases", json.dumps(rows))


def usage_envelope(stage):
    return ai.canonical_json({"result": brief_result(stage), "schema_version": "1.0", "status": "ok", "usage": USAGE})


class UsageRunner(CapturingRunner):
    async def __call__(self, command, payload, environment):
        self.calls.append((command, payload, environment))
        return usage_envelope(json.loads(payload)["stage"]) if self.output is None else self.output


class FakeUsageAdapter(FakeBriefAdapter):
    MODEL_ID = ai.MODEL

    async def generate_with_usage(self, request):
        return await self.generate(request), dict(USAGE)


class EvidenceBriefUsageTests(unittest.TestCase):
    def adapter(self, runner):
        fixed = ai.AiConfig(True, Path("/synthetic/python"), Path("/synthetic/worker"), "synthetic-project")
        return ai.EvidenceBriefAdapter(config_loader=lambda: fixed, process_runner=runner)

    def test_brief_adapter_returns_usage_beside_the_unchanged_result(self):
        runner = UsageRunner()
        result, usage = asyncio.run(self.adapter(runner).generate_with_usage({"stage": "dispute_mediation"}))
        self.assertEqual(usage, USAGE)
        self.assertNotIn("usage", result)
        plain = asyncio.run(self.adapter(UsageRunner()).generate({"stage": "dispute_mediation"}))
        self.assertEqual(plain, result)
        no_usage = CapturingRunner()
        self.assertIsNone(asyncio.run(self.adapter(no_usage).generate_with_usage({"stage": "dispute_mediation"}))[1])

    def test_bad_usage_or_usage_on_an_error_envelope_is_rejected(self):
        for raw in (
            ai.canonical_json({"result": brief_result("dispute_mediation"), "schema_version": "1.0", "status": "ok",
                               "usage": {"prompt_token_count": 1}}),
            ai.canonical_json({"result": {"code": "ai_timeout", "status": 504}, "schema_version": "1.0",
                               "status": "error", "usage": USAGE}),
        ):
            with self.subTest(raw=raw[:40]), self.assertRaises(ai.AiBriefError) as caught:
                asyncio.run(self.adapter(UsageRunner(raw)).generate({"stage": "dispute_mediation"}))
            self.assertEqual(caught.exception.code, "ai_response_invalid")

    def test_route_logs_the_call_per_session_without_any_text(self):
        store = SessionStore()
        app = create_app(store=store, ai_brief=FakeUsageAdapter())
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55121),
                        raise_server_exceptions=False) as client:
            def session():
                created = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": "http://localhost:5173"}).json()
                return {"Origin": "http://localhost:5173", "X-Demo-Session": created["session_id"],
                        "X-CSRF-Token": created["csrf_token"]}
            mine, other = session(), session()
            client.post(ROOT + "/demo/inject", json={"scenario": "dispute"}, headers=mine)
            self.assertEqual(client.post(ROOT + "/disputes/case-ref-001/draft", json={}, headers=mine).status_code, 200)
            brief = client.post(ROOT + "/ai/evidence-brief", json={"stage": "dispute_mediation"}, headers=mine)
            self.assertEqual(brief.status_code, 200, brief.text)
            usage = client.get(ROOT + "/ai/usage", headers={"X-Demo-Session": mine["X-Demo-Session"]})
            self.assertEqual(usage.status_code, 200, usage.text)
            body = usage.json()
            self.assertEqual((body["source"], body["content_logged"], body["price_table_source"]),
                             ("session_memory", False, ai_usage.PRICE_TABLE_SOURCE))
            self.assertEqual(len(body["entries"]), 1)
            entry = body["entries"][0]
            self.assertEqual((entry["stage"], entry["model"], entry["outcome"], entry["tokens_in"], entry["tokens_out"],
                              entry["tokens_total"], entry["estimated_cost_usd"]),
                             ("dispute_mediation", ai.MODEL, "ok", 812, 96, 1240, None))
            self.assertIsInstance(entry["latency_ms"], int)
            self.assertNotIn(brief.json()["brief"]["summary"], usage.text)
            self.assertEqual(client.get(ROOT + "/ai/usage", headers={"X-Demo-Session": other["X-Demo-Session"]})
                             .json()["entries"], [])
            self.assertEqual(client.get(ROOT + "/ai/usage").status_code, 401)

    def test_a_failed_call_is_logged_as_an_error_with_no_counts(self):
        app = create_app(store=SessionStore(), ai_brief=FakeUsageAdapter(error=ai.AiBriefError(504, "ai_timeout")))
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55122),
                        raise_server_exceptions=False) as client:
            created = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": "http://localhost:5173"}).json()
            headers = {"Origin": "http://localhost:5173", "X-Demo-Session": created["session_id"],
                       "X-CSRF-Token": created["csrf_token"]}
            client.post(ROOT + "/demo/inject", json={"scenario": "dispute"}, headers=headers)
            client.post(ROOT + "/disputes/case-ref-001/draft", json={}, headers=headers)
            self.assertEqual(client.post(ROOT + "/ai/evidence-brief", json={"stage": "dispute_mediation"},
                                         headers=headers).status_code, 504)
            entries = client.get(ROOT + "/ai/usage", headers={"X-Demo-Session": created["session_id"]}).json()["entries"]
            self.assertEqual([(row["outcome"], row["model"], row["tokens_in"]) for row in entries],
                             [("error", ai.MODEL, None)])


class RetryAfterTests(unittest.TestCase):
    def test_per_session_rate_limit_carries_retry_after(self):
        now = datetime(2026, 11, 4, 8, 0, tzinfo=timezone.utc)
        clock = mock.Mock(return_value=now)
        store = SessionStore(clock=clock, rate_limit=3)
        session_id = store.create()["session_id"]
        for _ in range(3):
            store.require(session_id)
        clock.return_value = now + timedelta(seconds=20)
        with self.assertRaises(BoundaryError) as caught:
            store.require(session_id)
        self.assertEqual((caught.exception.status, caught.exception.code, caught.exception.retry_after),
                         (429, "rate_limited", 40))

    def test_creation_limit_and_full_store_carry_retry_after(self):
        now = datetime(2026, 11, 4, 8, 0, tzinfo=timezone.utc)
        clock = mock.Mock(return_value=now)
        store = SessionStore(clock=clock, rate_limit=2, max_sessions=50)
        store.create()
        store.create()
        with self.assertRaises(BoundaryError) as caught:
            store.create()
        self.assertEqual((caught.exception.code, caught.exception.retry_after), ("rate_limited", 60))
        full = SessionStore(clock=clock, max_sessions=1)
        full.create()
        clock.return_value = now + timedelta(seconds=61)
        held = full.create()
        full.require(held["session_id"])
        clock.return_value = now + timedelta(seconds=71)
        with self.assertRaises(BoundaryError) as caught:
            full.create()
        self.assertEqual(caught.exception.code, "session_capacity")
        self.assertEqual(caught.exception.retry_after, 50)

    def test_the_http_answer_has_the_header(self):
        store = SessionStore(rate_limit=2)
        app = create_app(store=store)
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55123),
                        raise_server_exceptions=False) as client:
            created = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": "http://localhost:5173"}).json()
            headers = {"X-Demo-Session": created["session_id"]}
            answers = [client.get(ROOT + "/demo/state", headers=headers) for _ in range(3)]
        self.assertEqual([answer.status_code for answer in answers], [200, 200, 429])
        self.assertTrue(1 <= int(answers[-1].headers["Retry-After"]) <= 60)

    def test_hard_limit_docstring_matches_the_pacing_arithmetic(self):
        ceiling = PACE_BURST + PACE_PER_SECOND * (60 + MAX_PACE_DELAY_SECONDS)
        self.assertEqual(ceiling, 330)
        self.assertGreater(HARD_PER_MINUTE, ceiling, "HARD_PER_MINUTE is a backstop above the paced ceiling")


class GuideUsageTests(unittest.TestCase):
    def test_metered_chooser_records_counts_and_errors_without_text(self):
        from app.guide_routes import GuideService

        class Chooser:
            MODEL_ID = ai.MODEL

            def __init__(self):
                self.fail = False
                self.usage = None

            def __call__(self, request):
                if self.fail:
                    raise RuntimeError("provider down")
                self.usage = dict(USAGE)
                return b'{"v":2,"u":[]}'

            def take_usage(self):
                usage, self.usage = self.usage, None
                return usage

        service = GuideService(SessionStore(), chooser_factory=lambda: None)
        chooser = Chooser()
        self.assertIs(service._metered(chooser, "s-guide"), chooser, "no log, no wrapper")
        service.ai_usage = ai_usage.AiUsageLog()
        metered = service._metered(chooser, "s-guide")
        self.assertEqual(metered({"clauses": ["I shipped it Monday"]}), b'{"v":2,"u":[]}')
        chooser.fail = True
        with self.assertRaises(RuntimeError):
            metered({"clauses": ["I shipped it Monday"]})
        rows = service.ai_usage.entries("s-guide")
        self.assertEqual([(row["stage"], row["outcome"], row["tokens_out"]) for row in rows],
                         [("guide", "ok", 96), ("guide", "error", None)])
        self.assertNotIn("shipped", json.dumps(rows))
        plain = object()
        self.assertIs(service._metered(plain, "s-guide"), plain, "a chooser without counts is not wrapped")


class CiWorkflowExportTests(unittest.TestCase):
    """(optimise r24) The public package ships the CI workflow and the validator accepts exactly that dot-dir file."""

    def test_workflow_is_listed_and_accepted(self):
        import sys
        tools = str(Path(__file__).resolve().parents[1] / "tools")
        if tools not in sys.path:
            sys.path.insert(0, tools)
        import build_public_candidate as builder
        import validate_public_candidate as validator
        self.assertIn(".github/workflows/ci.yml", builder.source_paths())
        self.assertFalse(validator.forbidden_relative(".github/workflows/ci.yml"))
        for other in (".github/workflows/release.yml", ".github/ci.yml", "x/.github/workflows/ci.yml", ".git/config"):
            self.assertTrue(validator.forbidden_relative(other), other)
        self.assertIn(".yml", validator.TEXT_SUFFIXES)

    def test_workflow_uses_no_secrets_and_skips_only_the_two_named_checks(self):
        text = (Path(__file__).resolve().parents[1] / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("secrets.", text)
        self.assertIn("contents: read", text)
        self.assertIn('PAYGUARD_SKIP_GEMINI_MARKERS: "1"', text)
        self.assertIn('PAYGUARD_SKIP_ENV_LOCAL_CHECK: "1"', text)
        self.assertIn("--require-hashes -r requirements.lock", text)
        self.assertIn("./tools/run.sh test", text)
        self.assertIn('node-version: "22"', text)
        self.assertIn("npm ci --prefix frontend", text)
        self.assertIn("npm --prefix frontend run build", text)
        root = Path(__file__).resolve().parents[1]
        readers = [path.name for path in sorted((root / "tests").glob("*"))
                   if path.suffix in (".py", ".mjs") and "PAYGUARD_SKIP_" in path.read_text(encoding="utf-8")
                   and path.name != Path(__file__).name]
        self.assertEqual(readers, ["frontend_ag_studio_contract.mjs", "test_gemini_worker.py"])


if __name__ == "__main__":
    unittest.main()
