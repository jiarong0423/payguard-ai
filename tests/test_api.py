"""Local HTTP/security tests; every provider interaction is MockTransport."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import httpx
from pydantic import ValidationError

from app.main import MAX_BODY_BYTES, create_app
from app.paypal import PaypalAdapter, PaypalConfig, SANDBOX_BASE
from app.schemas import ScenarioMatch, VelocityResponse
from app.store import AiAttemptBudget, BoundaryError, SessionStore, iso
from payguard.case_cards import match_cases as match_authored_cases
from payguard.engines import check_aup
from payguard.review import payload_digest


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


class AiAttemptBudgetTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 8, 8, 0, tzinfo=timezone.utc)

    def test_three_stage_reservations_are_permanent_and_fourth_fails(self):
        budget = AiAttemptBudget()
        for index, stage in enumerate(("source_compliance", "velocity_guard", "dispute_mediation"), start=1):
            receipt = budget.reserve(stage, self.now)
            self.assertEqual((receipt["used"], receipt["remaining"]), (index, 3 - index))
        with self.assertRaises(BoundaryError) as caught:
            budget.reserve("source_compliance", self.now)
        self.assertEqual((caught.exception.status, caught.exception.code), (429, "ai_attempt_limit"))
        self.assertEqual(budget.used, 3)
        snapshot = budget.snapshot()
        self.assertEqual(set(snapshot), {"source_compliance", "velocity_guard", "dispute_mediation"})
        with self.assertRaises(TypeError):
            snapshot["source_compliance"] = "restored"

    def test_same_stage_concurrency_allows_exactly_one_reservation(self):
        budget = AiAttemptBudget()
        def reserve_once():
            try:
                budget.reserve("source_compliance", self.now)
                return "reserved"
            except BoundaryError as exc:
                return exc.code
        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(pool.map(lambda _index: reserve_once(), range(10)))
        self.assertEqual(results.count("reserved"), 1)
        self.assertEqual(results.count("ai_stage_attempt_exhausted"), 9)
        self.assertEqual(budget.used, 1)

    def test_session_reset_and_new_session_do_not_restore_stage_attempt(self):
        clock = Clock()
        store = SessionStore(clock=clock, rate_limit=300)
        first = store.sessions[store.create()["session_id"]]
        store.review_aup(first, "Synthetic counterfeit goods")
        store.reserve_ai_brief_attempt(first, "source_compliance")
        store.inject(first, "reset")
        second = store.sessions[store.create()["session_id"]]
        store.review_aup(second, "Synthetic counterfeit goods")
        with self.assertRaises(BoundaryError) as caught:
            store.reserve_ai_brief_attempt(second, "source_compliance")
        self.assertEqual((caught.exception.status, caught.exception.code), (409, "ai_stage_attempt_exhausted"))
        self.assertEqual(store.ai_attempt_budget.used, 1)


class ClosedMockTransport(httpx.MockTransport):
    def __init__(self, handler):
        super().__init__(handler)
        self.close_count = 0

    async def aclose(self):
        self.close_count += 1
        await super().aclose()


def invoice_payload():
    return {"description": "Synthetic ceramic cup", "amount": "10.00", "currency": "USD"}


def bound_invoice_review(test, payload=None):
    payload = invoice_payload() if payload is None else payload
    evaluated = test.post("/aup/review", {"description": payload["description"]})
    test.assertEqual(evaluated.status_code, 200, evaluated.text)
    evaluation = evaluated.json()
    return dict(payload, confirm_sandbox_draft=True, evaluation_id=evaluation["evaluation_id"],
                description_digest=evaluation["description_digest"])


def webhook_payload():
    return {
        "transmission_id": "demo-transmission", "transmission_time": "2026-10-04T08:00:00Z",
        "cert_url": "https://api.sandbox.paypal.com/v1/notifications/certs/CERT-DEMO",
        "auth_algo": "SHA256withRSA", "transmission_sig": "synthetic-signature",
        "webhook_event": {"id": "WH-DEMO", "event_type": "INVOICING.INVOICE.CREATED", "resource_type": "invoice",
                          "create_time": "2026-10-04T08:00:00Z", "resource": {"id": "INV2-DEMO-0001", "status": "DRAFT"}},
    }


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        def handler(request):
            self.calls.append(request)
            raise AssertionError("Provider must not be contacted by synthetic/default routes")
        self.transport = ClosedMockTransport(handler)
        self.provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=self.transport, clock=self.clock)
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55001), raise_server_exceptions=False)
        self.client.__enter__()
        self.session = self.new_session()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider.open_clients, 0)

    def new_session(self):
        response = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN})
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def headers(self, session=None):
        session = session or self.session
        return {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}

    def post(self, route, payload=None, session=None):
        return self.client.post(ROOT + route, json={} if payload is None else payload, headers=self.headers(session))

    def state(self, session=None):
        response = self.client.get(ROOT + "/demo/state", headers=self.headers(session))
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_initial_health_empty_state_and_no_provider_effect(self):
        health = self.client.get(ROOT + "/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["mode"], "demo")
        state = self.state()
        self.assertEqual(state["transactions"], [])
        self.assertEqual(state["disputes"], [])
        self.assertEqual(state["velocity"]["status"], "normal")
        self.assertEqual(state["velocity"]["ratio"], "0")
        self.assertEqual(state["activity"], [])
        status = self.client.get(ROOT + "/paypal/status", headers=self.headers())
        self.assertEqual(status.json()["status"], "not_configured")
        self.assertEqual(self.calls, [])

    def test_velocity_response_requires_declared_comparison_window(self):
        payload = self.state()["velocity"]
        self.assertEqual(payload["baseline_provenance"], "SYNTHETIC_BASELINE")
        self.assertIsNotNone(payload["baseline_window_start"])
        self.assertIsNotNone(payload["baseline_window_end"])
        caller = dict(payload, baseline_provenance="CALLER_SUPPLIED_UNVERIFIED")
        self.assertEqual(VelocityResponse.model_validate(caller).baseline_provenance,
                         "CALLER_SUPPLIED_UNVERIFIED")
        for field in ("baseline_window_start", "baseline_window_end"):
            missing = dict(caller)
            missing.pop(field)
            with self.subTest(field=field), self.assertRaises(ValidationError):
                VelocityResponse.model_validate(missing)
        with self.assertRaises(ValidationError):
            VelocityResponse.model_validate(dict(caller, baseline_provenance="SUPPLIED_UNVERIFIED"))

    def test_independent_scenarios_idempotency_and_reset_identity(self):
        dispute = self.post("/demo/inject", {"scenario": "dispute"})
        self.assertEqual(dispute.status_code, 200, dispute.text)
        self.assertEqual(len(dispute.json()["disputes"]), 1)
        self.assertEqual(dispute.json()["transactions"], [])
        burst = self.post("/demo/inject", {"scenario": "burst"})
        self.assertEqual(burst.status_code, 200)
        state = burst.json()
        self.assertEqual(len(state["transactions"]), 50)
        self.assertEqual(state["velocity"]["status"], "review_velocity")
        self.assertEqual(state["velocity"]["ratio"], "5")
        repeat = self.post("/demo/inject", {"scenario": "burst"}).json()
        self.assertEqual(repeat, state)
        reset = self.post("/demo/inject", {"scenario": "reset"}).json()
        self.assertEqual(reset["transactions"], [])
        self.assertEqual(reset["disputes"], [])
        self.assertEqual(reset["activity"], [])
        self.assertEqual(reset["scenario"], {"burst": False, "dispute": False})
        self.assertEqual(reset["session_id"], self.session["session_id"])
        self.assertEqual(self.post("/demo/inject", {"scenario": "burst"}).status_code, 200)

    def test_session_isolation_and_expiry_purge(self):
        other = self.new_session()
        self.post("/demo/inject", {"scenario": "burst"})
        self.assertEqual(self.state(other)["transactions"], [])
        self.clock.advance(900)
        expired = self.client.get(ROOT + "/demo/state", headers=self.headers())
        self.assertEqual(expired.status_code, 401)
        self.assertEqual(self.store.sessions, {})

    def test_session_missing_csrf_and_cross_session_csrf_rejected(self):
        self.assertEqual(self.client.get(ROOT + "/demo/state").status_code, 401)
        headers = self.headers()
        del headers["X-CSRF-Token"]
        self.assertEqual(self.client.post(ROOT + "/demo/inject", json={"scenario": "burst"}, headers=headers).status_code, 403)
        other = self.new_session()
        headers["X-CSRF-Token"] = other["csrf_token"]
        self.assertEqual(self.client.post(ROOT + "/demo/inject", json={"scenario": "burst"}, headers=headers).status_code, 403)

    def test_exact_host_origin_loopback_and_preflight(self):
        self.assertEqual(self.client.get(ROOT + "/health", headers={"Host": "evil.invalid"}).status_code, 403)
        self.assertEqual(self.client.get(ROOT + "/health", headers={"Origin": "http://localhost:5173.evil.invalid"}).status_code, 403)
        self.assertEqual(self.client.post(ROOT + "/demo/sessions", json={}).status_code, 403)
        with TestClient(self.app, base_url="http://127.0.0.1:8000", client=("203.0.113.1", 1)) as remote:
            self.assertEqual(remote.get(ROOT + "/health").status_code, 403)
        response = self.client.options(ROOT + "/demo/inject", headers={"Origin": ORIGIN,
                    "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "X-Demo-Session,X-CSRF-Token,Content-Type"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], ORIGIN)
        self.assertNotIn("access-control-allow-credentials", response.headers)

    def test_security_headers_duplicate_headers_and_no_cache(self):
        self.assertIn("no-store", self.client.get(ROOT + "/health").headers["cache-control"])
        response = self.client.get(ROOT + "/health", headers=[("Origin", ORIGIN), ("Origin", "http://evil.invalid")])
        self.assertEqual(response.status_code, 403)

    def test_sanitized_schema_domain_json_body_and_content_type_failures(self):
        secret_marker = "synthetic-input-must-not-be-echoed"
        response = self.post("/aup/review", {"description": secret_marker, "unknown": secret_marker})
        self.assertEqual(response.status_code, 422)
        self.assertNotIn(secret_marker, response.text)
        self.assertEqual(set(response.json()), {"error"})
        domain = self.post("/aup/review", {"description": "\x00" + secret_marker})
        self.assertEqual(domain.status_code, 422)
        self.assertNotIn(secret_marker, domain.text)
        headers = dict(self.headers(), **{"Content-Type": "application/json"})
        for body in ('{"scenario":"burst","scenario":"dispute"}', '{"value":NaN}', '[]', '{'):
            with self.subTest(body=body):
                self.assertEqual(self.client.post(ROOT + "/demo/inject", content=body, headers=headers).status_code, 422)
        self.assertEqual(self.client.post(ROOT + "/demo/inject", content="x", headers=self.headers()).status_code, 415)
        self.assertEqual(self.client.post(ROOT + "/demo/inject", content="x" * (MAX_BODY_BYTES + 1), headers=headers).status_code, 413)
        def chunks():
            yield b"x" * 9000
            yield b"x" * 9000
        self.assertEqual(self.client.post(ROOT + "/demo/inject", content=chunks(), headers=headers).status_code, 413)

    def test_aup_advisory_only_no_raw_description(self):
        response = self.post("/aup/review", {"description": "Guaranteed 20% ROI"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["match_status"], "REVIEW_SIGNAL")
        self.assertTrue(response.json()["advisory_only"])
        self.assertNotIn("Guaranteed 20% ROI", response.text)

    def test_atomic_failed_injection_and_activity_bound(self):
        before = self.state()
        with patch("app.store.assess_velocity", side_effect=ValueError("do-not-echo")):
            response = self.post("/demo/inject", {"scenario": "burst"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.state(), before)
        session = self.store.sessions[self.session["session_id"]]
        for index in range(40):
            self.store._activity(session, "demo", f"Synthetic activity {index}")
        self.assertEqual(len(self.state()["activity"]), 30)
        session.transactions = [{"order_id": f"demo-existing-{i}", "amount": "1.00", "currency": "USD",
                                 "occurred_at": "2026-10-04T08:00:00Z"} for i in range(160)]
        response = self.post("/demo/inject", {"scenario": "burst"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(len(session.transactions), 160)
        self.assertFalse(session.scenario["burst"])

    def test_rate_and_capacity_limits(self):
        self.store.rate_limit = 2
        self.assertEqual(self.client.get(ROOT + "/demo/state", headers=self.headers()).status_code, 200)
        self.assertEqual(self.client.get(ROOT + "/demo/state", headers=self.headers()).status_code, 200)
        self.assertEqual(self.client.get(ROOT + "/demo/state", headers=self.headers()).status_code, 429)
        self.clock.advance(60)
        self.assertEqual(self.client.get(ROOT + "/demo/state", headers=self.headers()).status_code, 200)
        self.store.max_sessions = 1
        self.assertEqual(self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).status_code, 429)

    def test_dispute_draft_redaction_binding_replay_and_reset(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        matcher_requests = []
        def capture(raw_json):
            matcher_requests.append(json.loads(raw_json))
            return match_authored_cases(raw_json)
        with patch("app.store.match_cases", side_effect=capture):
            draft = self.post("/disputes/case-ref-001/draft")
        self.assertEqual(draft.status_code, 200, draft.text)
        data = draft.json()
        self.assertEqual(data["status"], "review_evidence")
        self.assertEqual(data["source"], "synthetic")
        self.assertEqual(len(matcher_requests), 1)
        request = matcher_requests[0]
        self.assertEqual(set(request), {
            "schema_version", "intake_id", "requested_theme", "request_kind", "jurisdiction",
            "as_of", "observation_max_age_days", "source_class", "payload", "evidence_items", "references",
        })
        self.assertEqual(request["jurisdiction"], "US")
        self.assertEqual(request["payload"]["reason_code"], "MERCHANDISE_OR_SERVICE_NOT_RECEIVED")
        self.assertEqual(request["payload"]["merchant_case_ref"], "demo-case-001")
        self.assertEqual(request["evidence_items"][0]["field_id"], "payload.evidences")
        self.assertEqual(request["evidence_items"][0]["provider_request_id"], "demo-request-fulfillment-001")
        scenario_match = data["scenario_match"]
        self.assertNotIn("intake", scenario_match)
        self.assertEqual(scenario_match["status"], "synthetic_scenarios_found")
        self.assertEqual(scenario_match["intake_status"], "ready_for_local_rules")
        self.assertTrue(scenario_match["required_human_review"])
        self.assertEqual(scenario_match["operational_authority"], "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION")
        self.assertEqual(
            [row["chunk_id"] for row in scenario_match["scenario"]["citations"]],
            [
                "PP-DISPUTES-OVERVIEW-AUTHORITY", "PP-US-PURCHASE-INR-SNAD",
                "PP-US-SELLER-ELIGIBILITY", "PP-US-SELLER-DELIVERY", "PP-REASONS-INR",
            ],
        )
        self.assertEqual(set(data["identity_redaction"]["tokens"]), {"name_token", "address_token", "email_token"})
        self.assertNotIn("demo@example.invalid", draft.text)
        session = self.store.sessions[self.session["session_id"]]
        stored = deepcopy(session.drafts["demo-case-001"])
        expected_digest = payload_digest({
            "session_id": session.session_id,
            "draft": stored,
            "restricted_sha256": session.restricted_evidence["demo-case-001"]["sha256"],
            "expires_at": iso(session.draft_expires["demo-case-001"]),
        })
        self.assertEqual(data["draft_digest"], expected_digest)
        changed = deepcopy(stored)
        changed["scenario_match"]["scenario"]["citations"].reverse()
        self.assertNotEqual(data["draft_digest"], payload_digest({
            "session_id": session.session_id,
            "draft": changed,
            "restricted_sha256": session.restricted_evidence["demo-case-001"]["sha256"],
            "expires_at": iso(session.draft_expires["demo-case-001"]),
        }))
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": "a" * 64}).status_code, 422)
        receipt = self.post("/disputes/case-ref-001/approve", {"draft_digest": data["draft_digest"]})
        self.assertEqual(receipt.status_code, 200, receipt.text)
        self.assertEqual(receipt.json()["status"], "local_draft_reviewed")
        self.assertEqual(receipt.json()["external_submission"], "FROZEN")
        self.assertFalse(receipt.json()["authenticated_actor"])
        self.assertEqual(receipt.json()["reviewer"], "DEMO_OPERATOR_UNAUTHENTICATED")
        self.assertEqual(receipt.json()["reviewed_at"], "2026-10-07T08:00:00Z")
        self.assertEqual(receipt.json()["retention"], "SESSION_MEMORY_ONLY")
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": data["draft_digest"]}).status_code, 422)
        self.post("/demo/inject", {"scenario": "reset"})
        self.assertEqual(self.post("/disputes/case-ref-001/draft").status_code, 404)
        self.post("/demo/inject", {"scenario": "dispute"})
        new_digest = self.post("/disputes/case-ref-001/draft").json()["draft_digest"]
        self.assertNotEqual(new_digest, data["draft_digest"])

    def test_dispute_matcher_failures_are_atomic_and_sanitized(self):
        cases = [
            ({"status": "intake_blocked"}, 422, "dispute_context_not_ready"),
            ({"status": "evidence_missing"}, 422, "dispute_context_not_ready"),
            ({"status": "reference_unavailable"}, 503, "reference_unavailable"),
            ({"status": "synthetic_scenarios_found"}, 500, "response_contract_failure"),
        ]
        for result, status, code in cases:
            with self.subTest(result=result):
                session_info = self.new_session()
                self.post("/demo/inject", {"scenario": "dispute"}, session_info)
                session = self.store.sessions[session_info["session_id"]]
                before_activity = deepcopy(session.activity)
                with patch("app.store.match_cases", return_value=result):
                    response = self.post("/disputes/case-ref-001/draft", session=session_info)
                self.assertEqual(response.status_code, status, response.text)
                self.assertEqual(response.json()["error"]["code"], code)
                self.assertEqual(session.drafts, {})
                self.assertEqual(session.draft_expires, {})
                self.assertEqual(session.activity, before_activity)
        session_info = self.new_session()
        self.post("/demo/inject", {"scenario": "dispute"}, session_info)
        session = self.store.sessions[session_info["session_id"]]
        before_activity = deepcopy(session.activity)
        with patch("app.store.match_cases", side_effect=RuntimeError("PRIVATE_PATH")):
            response = self.post("/disputes/case-ref-001/draft", session=session_info)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"]["code"], "response_contract_failure")
        self.assertNotIn("PRIVATE_PATH", response.text)
        self.assertEqual(session.drafts, {})
        self.assertEqual(session.draft_expires, {})
        self.assertEqual(session.activity, before_activity)
        self.assertEqual(self.calls, [])

    def test_scenario_match_schema_rejects_authority_and_citation_mutations(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        valid = self.post("/disputes/case-ref-001/draft").json()["scenario_match"]
        mutations = [
            lambda value: value.update(extra=True),
            lambda value: value.update(operational_authority="PAYGUARD_APPROVED"),
            lambda value: value.update(real_case_evidence="PROVIDED"),
            lambda value: value["scenario"].update(jurisdiction="CA"),
            lambda value: value["scenario"].update(final_authority="PAYGUARD"),
            lambda value: value["scenario"].update(evidence_class="REAL_CASE"),
            lambda value: value["scenario"]["citations"].append(deepcopy(value["scenario"]["citations"][0])),
            lambda value: value["scenario"]["citations"][0].update(url="https://example.com/private"),
            lambda value: value["scenario"]["citations"][0].update(text_sha256="0" * 64),
            lambda value: value["scenario"]["citations"][0].update(material_type="public_court_order_copy"),
        ]
        for mutate in mutations:
            candidate = deepcopy(valid)
            mutate(candidate)
            with self.subTest(mutation=mutations.index(mutate)), self.assertRaises(ValidationError):
                ScenarioMatch.model_validate(candidate)

    def test_wrong_session_or_missing_draft_cannot_approve(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": "a" * 64}).status_code, 422)
        digest = self.post("/disputes/case-ref-001/draft").json()["draft_digest"]
        other = self.new_session()
        self.post("/demo/inject", {"scenario": "dispute"}, other)
        self.post("/disputes/case-ref-001/draft", session=other)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": digest}, other).status_code, 422)

    def test_dispute_draft_expiry_requires_new_digest(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        digest = self.post("/disputes/case-ref-001/draft").json()["draft_digest"]
        self.clock.advance(300)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": digest}).status_code, 422)
        renewed = self.post("/disputes/case-ref-001/draft").json()["draft_digest"]
        self.assertNotEqual(renewed, digest)
        self.assertEqual(self.post("/disputes/case-ref-001/approve", {"draft_digest": renewed}).status_code, 200)

    def test_dispute_ai_gate_requires_live_reason_bound_inr_draft(self):
        self.post("/demo/inject", {"scenario": "dispute"})
        self.post("/disputes/case-ref-001/draft")
        session = self.store.sessions[self.session["session_id"]]
        self.assertTrue(self.store.ai_brief_allowed(session, "dispute_mediation"))

        session.disputes["demo-case-001"]["reason"] = "SNAD"
        self.assertFalse(self.store.ai_brief_allowed(session, "dispute_mediation"))

        session.disputes["demo-case-001"]["reason"] = "INR"
        session.drafts["demo-case-001"]["evidence"]["reason"] = "SNAD"
        self.assertFalse(self.store.ai_brief_allowed(session, "dispute_mediation"))

        session.drafts["demo-case-001"]["evidence"]["reason"] = "INR"
        self.clock.advance(300)
        self.assertFalse(self.store.ai_brief_allowed(session, "dispute_mediation"))

    def test_disabled_provider_and_frozen_actions(self):
        self.assertEqual(self.post("/paypal/connect").status_code, 503)
        review = self.post("/paypal/invoices/review", bound_invoice_review(self)).json()
        request = dict(invoice_payload(), review_token=review["review_token"], payload_digest=review["payload_digest"])
        self.assertEqual(self.post("/paypal/invoices/draft", request).status_code, 503)
        for route in ("/paypal/invoices/send", "/paypal/payments", "/paypal/refunds", "/paypal/disputes/provide-evidence"):
            self.assertEqual(self.post(route).status_code, 404)
        self.assertEqual(self.calls, [])


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock)
        self.calls = []
        self.invoice_status = "DRAFT"
        self.webhook_status = "SUCCESS"
        self.failure = None
        self.oauth_override = None
        def handler(request):
            self.calls.append(request)
            self.assertEqual(str(request.url).split(request.url.path)[0], SANDBOX_BASE)
            self.assertEqual(request.method, "POST")
            self.assertEqual(request.extensions["timeout"]["connect"], 5.0)
            self.assertEqual(request.extensions["timeout"]["read"], 8.0)
            if self.failure:
                return self.failure(request)
            if request.url.path == "/v1/oauth2/token":
                self.assertEqual(request.content, b"grant_type=client_credentials")
                self.assertTrue(request.headers["Authorization"].startswith("Basic "))
                return httpx.Response(200, json=self.oauth_override or {"access_token": "synthetic-access-token", "token_type": "Bearer", "expires_in": 300,
                                                                       "account_id": "synthetic-private-account"})
            if request.url.path == "/v2/invoicing/invoices":
                self.assertEqual(request.headers["Prefer"], "return=representation")
                self.assertLessEqual(len(request.headers["PayPal-Request-Id"]), 38)
                body = json.loads(request.content)
                self.assertEqual(set(body), {"detail", "items"})
                self.assertNotIn("primary_recipients", body)
                self.assertEqual(body["items"][0]["unit_amount"], {"currency_code": "USD", "value": "10.00"})
                return httpx.Response(201, json={"id": "INV2-DEMO-1234-5678", "status": self.invoice_status,
                                                "recipient_email": "synthetic@example.invalid"})
            if request.url.path == "/v1/notifications/verify-webhook-signature":
                self.assertEqual(json.loads(request.content)["webhook_id"], "synthetic-webhook-id")
                return httpx.Response(200, json={"verification_status": self.webhook_status})
            raise AssertionError("Unexpected provider path")
        self.transport = ClosedMockTransport(handler)
        self.config = PaypalConfig(True, "synthetic-client-id", "synthetic-client-secret", "synthetic-webhook-id")
        self.provider = PaypalAdapter(config_loader=lambda: self.config, transport=self.transport, clock=self.clock)
        self.client = TestClient(create_app(store=self.store, paypal=self.provider), base_url="http://127.0.0.1:8000",
                                 client=("127.0.0.1", 55002), raise_server_exceptions=False)
        self.client.__enter__()
        self.session = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider.open_clients, 0)
        self.assertEqual(self.transport.close_count, len(self.calls))

    def headers(self, session=None):
        session = session or self.session
        return {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}

    def post(self, route, payload=None, session=None):
        return self.client.post(ROOT + route, json={} if payload is None else payload, headers=self.headers(session))

    def connect(self):
        result = self.post("/paypal/connect")
        self.assertEqual(result.status_code, 200, result.text)
        return result

    def reviewed(self):
        review = self.post("/paypal/invoices/review", bound_invoice_review(self))
        self.assertEqual(review.status_code, 200, review.text)
        return dict(invoice_payload(), review_token=review.json()["review_token"], payload_digest=review.json()["payload_digest"])

    def test_get_status_no_network_connect_no_credentials_echo_expiry(self):
        self.assertEqual(self.client.get(ROOT + "/paypal/status", headers=self.headers()).json()["status"], "not_configured")
        self.assertEqual(self.calls, [])
        result = self.connect()
        self.assertEqual(result.json()["status"], "connected")
        for marker in ("synthetic-access-token", "synthetic-client-id", "synthetic-client-secret", "synthetic-private-account"):
            self.assertNotIn(marker, result.text)
        count = len(self.calls)
        self.clock.advance(300)
        status = self.client.get(ROOT + "/paypal/status", headers=self.headers()).json()
        self.assertEqual(status["status"], "disconnected")
        self.assertEqual(len(self.calls), count)
        self.assertIsNone(self.provider._access_token)

    def test_missing_credentials_never_sends(self):
        self.config = PaypalConfig(True)
        self.assertEqual(self.post("/paypal/connect").status_code, 503)
        self.assertEqual(self.calls, [])

    def test_actual_provider_draft_requires_binding_and_is_once_only(self):
        self.connect()
        request = self.reviewed()
        response = self.post("/paypal/invoices/draft", request)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "DRAFT")
        self.assertEqual(response.json()["source"], "paypal_sandbox")
        self.assertEqual(response.json()["external_send"], "FROZEN")
        self.assertNotIn("synthetic@example.invalid", response.text)
        self.assertEqual(self.post("/paypal/invoices/draft", request).status_code, 422)
        state = self.client.get(ROOT + "/demo/state", headers=self.headers()).json()
        self.assertEqual(state["transactions"], [])
        self.assertEqual(state["disputes"], [])
        self.assertEqual(len(self.calls), 2)

    def test_changed_payload_session_and_expired_review_rejected(self):
        self.connect()
        request = self.reviewed()
        self.assertEqual(self.post("/paypal/invoices/draft", dict(request, amount="11.00")).status_code, 422)
        other = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
        self.assertEqual(self.post("/paypal/invoices/draft", request, other).status_code, 422)
        self.clock.advance(120)
        self.assertEqual(self.post("/paypal/invoices/draft", request).status_code, 422)
        self.assertEqual(len(self.calls), 1)

    def test_reset_revokes_invoice_approval_and_restricted_description(self):
        self.connect()
        request = self.reviewed()
        self.post("/demo/inject", {"scenario": "reset"})
        self.assertEqual(self.post("/paypal/invoices/draft", request).status_code, 422)
        self.assertEqual(self.post("/paypal/invoices/review", dict(invoice_payload(), description="firearms", confirm_sandbox_draft=True)).status_code, 422)
        self.assertEqual(self.post("/paypal/invoices/review", dict(invoice_payload(), confirm_sandbox_draft=False)).status_code, 422)
        self.assertEqual(self.post("/paypal/invoices/review", dict(invoice_payload(), amount="0.00", confirm_sandbox_draft=True)).status_code, 422)
        self.assertEqual(len(self.calls), 1)

    def test_timeout_redirect_error_bodies_and_bad_oauth_sanitized(self):
        def timeout(request):
            raise httpx.ReadTimeout("synthetic-upstream-secret", request=request)
        failures = [timeout,
                    lambda _request: httpx.Response(302, headers={"Location": "https://evil.invalid/synthetic-secret"}),
                    lambda _request: httpx.Response(401, json={"secret": "synthetic-upstream-secret"}),
                    lambda _request: httpx.Response(200, content=b"not-json synthetic-upstream-secret"),
                    lambda _request: httpx.Response(200, content=b"x" * 65537)]
        for failure in failures:
            self.failure = failure
            with self.subTest(failure=failure):
                response = self.post("/paypal/connect")
                self.assertEqual(response.status_code, 502, response.text)
                self.assertNotIn("synthetic-upstream-secret", response.text)
                self.assertEqual(self.client.get(ROOT + "/paypal/status", headers=self.headers()).json()["status"], "error")
                self.assertEqual(self.provider.open_clients, 0)
        self.failure = None
        self.oauth_override = {"access_token": "synthetic-token", "token_type": 1, "expires_in": 300}
        self.assertEqual(self.post("/paypal/connect").status_code, 502)

    def test_provider_json_depth_duplicate_and_nonfinite_are_safe_failures(self):
        responses = [b'{"nested":' + b'[' * 15000 + b'0' + b']' * 15000 + b'}',
                     b'{"access_token":"synthetic-token","access_token":"synthetic-other","token_type":"Bearer","expires_in":300}',
                     b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":300,"unexpected":NaN}']
        for body in responses:
            with self.subTest(size=len(body)):
                self.failure = lambda _request, content=body: httpx.Response(200, content=content)
                result = self.post("/paypal/connect")
                self.assertEqual(result.status_code, 502)
                self.assertEqual(result.json()["error"]["code"], "provider_response_invalid")
                self.assertNotIn("synthetic-token", result.text)
                self.assertEqual(self.client.get(ROOT + "/paypal/status", headers=self.headers()).json()["status"], "error")
                self.assertEqual(self.provider.open_clients, 0)

    def test_provider_non_draft_status_is_not_promoted(self):
        self.connect()
        self.invoice_status = "SENT"
        response = self.post("/paypal/invoices/draft", self.reviewed())
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("invoice_id", response.json())

    def test_webhook_success_only_verify_no_demo_import_and_pii_rejected(self):
        self.connect()
        request = webhook_payload()
        verified = self.post("/paypal/webhooks/verify", request)
        self.assertEqual(verified.status_code, 200, verified.text)
        self.assertEqual(verified.json(), {"source": "paypal_sandbox", "verification_status": "SUCCESS", "imported_into_demo": False})
        self.webhook_status = "FAILURE"
        self.assertEqual(self.post("/paypal/webhooks/verify", request).status_code, 403)
        unsafe = deepcopy(request)
        unsafe["webhook_event"]["resource"]["email"] = "synthetic-private@example.invalid"
        calls = len(self.calls)
        response = self.post("/paypal/webhooks/verify", unsafe)
        self.assertEqual(response.status_code, 422)
        self.assertNotIn("synthetic-private@example.invalid", response.text)
        self.assertEqual(len(self.calls), calls)
        self.assertEqual(self.post("/paypal/webhooks/verify", dict(request, cert_url="https://evil.invalid/cert")).status_code, 422)


class AupReceiptTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.store = SessionStore(clock=self.clock, rate_limit=300)
        self.session = self.store.sessions[self.store.create()["session_id"]]
        self.description = "Synthetic ceramic cup"

    def evaluate(self, description=None, session=None):
        return self.store.review_aup(session or self.session, self.description if description is None else description)

    def acknowledge(self, evaluation, choice="ACKNOWLEDGE_AND_CONTINUE", session=None, **changes):
        request = dict(evaluation_id=evaluation["evaluation_id"], description_digest=evaluation["description_digest"], choice=choice)
        request.update(changes)
        return self.store.acknowledge_aup(session or self.session, request)

    def payload(self, evaluation, token=None, description=None, **changes):
        request = dict(description=self.description if description is None else description, amount="10.00", currency="USD",
                       confirm_sandbox_draft=True, evaluation_id=evaluation["evaluation_id"],
                       description_digest=evaluation["description_digest"], acknowledgement_token=token)
        request.update(changes)
        return request

    def assert_code(self, code, call):
        with self.assertRaises(BoundaryError) as captured:
            call()
        self.assertEqual(captured.exception.code, code)
        return captured.exception

    def test_clean_is_bound_single_use_and_draft_receipt_contains_aup(self):
        evaluation = self.evaluate()
        self.assertEqual(evaluation["match_status"], "NO_MATCH")
        self.assertEqual(evaluation["compliance_decision"], "NOT_MADE")
        receipt = self.store.review_invoice(self.session, self.payload(evaluation))
        stored = self.session.invoice_reviews[receipt["review_token"]]
        self.assertEqual(stored["aup_binding"]["evaluation_id"], evaluation["evaluation_id"])
        self.assertIsNone(stored["aup_binding"]["acknowledgement_digest"])
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(evaluation)))
        request = dict(invoice_payload(), review_token=receipt["review_token"], payload_digest=receipt["payload_digest"])
        self.store.consume_invoice(self.session, request)
        self.assert_code("review_binding_rejected", lambda: self.store.consume_invoice(self.session, request))

    def test_matched_warning_acknowledgement_then_review_and_draft(self):
        self.description = "Synthetic firearms description"
        evaluation = self.evaluate()
        self.assertEqual(evaluation["match_status"], "REVIEW_SIGNAL")
        self.assert_code("aup_acknowledgement_required", lambda: self.store.review_invoice(self.session, self.payload(evaluation)))
        ack = self.acknowledge(evaluation)
        self.assertFalse(ack["external_action_authorized"])
        self.assertEqual(ack["expires_at"], evaluation["expires_at"])
        self.assert_code("aup_acknowledgement_already_used", lambda: self.acknowledge(evaluation))
        receipt = self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"]))
        payload, _ = self.store.consume_invoice(self.session, dict(description=self.description, amount="10.00", currency="USD",
                                 review_token=receipt["review_token"], payload_digest=receipt["payload_digest"]))
        self.assertEqual(payload["description"], self.description)
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"])))

    def test_ai_gate_uses_commit_order_and_closes_after_current_evaluation_is_consumed(self):
        first = self.evaluate("Synthetic firearms")
        second = self.evaluate("Synthetic ceramic cup")
        self.assertEqual(self.session.current_aup_evaluation_id, second["evaluation_id"])
        self.assertFalse(self.store.ai_brief_allowed(self.session, "source_compliance"))

        third = self.evaluate("Synthetic counterfeit goods")
        self.assertEqual(self.session.current_aup_evaluation_id, third["evaluation_id"])
        self.assertTrue(self.store.ai_brief_allowed(self.session, "source_compliance"))

        self.acknowledge(first, "CANCEL")
        self.assertEqual(self.session.current_aup_evaluation_id, third["evaluation_id"])
        self.assertTrue(self.store.ai_brief_allowed(self.session, "source_compliance"))

        acknowledgement = self.acknowledge(third)
        self.store.review_invoice(
            self.session,
            self.payload(
                third,
                acknowledgement["acknowledgement_token"],
                "Synthetic counterfeit goods",
            ),
        )
        self.assertIsNone(self.session.current_aup_evaluation_id)
        self.assertFalse(self.store.ai_brief_allowed(self.session, "source_compliance"))

    def test_ai_gate_rejects_exact_expiry_and_reset_clears_current_identity(self):
        evaluation = self.evaluate("Synthetic firearms")
        self.assertTrue(self.store.ai_brief_allowed(self.session, "source_compliance"))
        self.clock.advance(120)
        self.assertFalse(self.store.ai_brief_allowed(self.session, "source_compliance"))

        replacement = self.evaluate("Synthetic counterfeit goods")
        self.assertEqual(self.session.current_aup_evaluation_id, replacement["evaluation_id"])
        self.store.inject(self.session, "reset")
        self.assertIsNone(self.session.current_aup_evaluation_id)
        self.assertFalse(self.store.ai_brief_allowed(self.session, "source_compliance"))

    def test_return_and_cancel_revoke_without_receipt(self):
        for choice in ("RETURN_TO_EDIT", "CANCEL"):
            evaluation = self.evaluate("Synthetic firearms")
            ack = self.acknowledge(evaluation, choice)
            self.assertIsNone(ack["acknowledgement_token"])
            self.assertIsNone(ack["expires_at"])
            self.assertNotIn(evaluation["evaluation_id"], self.session.aup_evaluations)
            self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation))
        self.assertEqual(self.session.invoice_reviews, {})

    def test_wrong_session_evaluation_and_digest_leave_valid_receipt(self):
        evaluation = self.evaluate("Synthetic firearms")
        other = self.store.sessions[self.store.create()["session_id"]]
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation, session=other))
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation, evaluation_id="x" * 43))
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation, description_digest="0" * 64))
        ack = self.acknowledge(evaluation)
        second = self.evaluate("Synthetic firearms")
        self.assert_code("aup_acknowledgement_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(second, ack["acknowledgement_token"], "Synthetic firearms")))
        self.assert_code("aup_acknowledgement_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(evaluation, "x" * 43, "Synthetic firearms")))
        self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"], "Synthetic firearms"))

    def test_exact_description_mutations_require_new_evaluation(self):
        evaluation = self.evaluate("ＦＩＲＥＡＲＭＳ")
        ack = self.acknowledge(evaluation)
        for changed in ("FIREARMS", "firearms", "ＦＩＲＥＡＲＭＳ ", "ＦＩＲＥＡＲＭＳx"):
            self.assert_code("aup_evaluation_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"], changed)))
        self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"], "ＦＩＲＥＡＲＭＳ"))

    def test_clean_ack_and_supplied_token_are_rejected(self):
        evaluation = self.evaluate()
        self.assert_code("aup_choice_rejected", lambda: self.acknowledge(evaluation))
        self.assert_code("aup_acknowledgement_binding_rejected", lambda: self.store.review_invoice(self.session, self.payload(evaluation, "x" * 43)))
        self.store.review_invoice(self.session, self.payload(evaluation))

    def test_exact_expiry_and_no_ttl_extension(self):
        evaluation = self.evaluate("Synthetic firearms")
        self.clock.advance(119)
        ack = self.acknowledge(evaluation)
        self.assertEqual(ack["expires_at"], evaluation["expires_at"])
        self.clock.advance(1)
        self.assert_code("aup_evaluation_expired", lambda: self.store.review_invoice(self.session, self.payload(evaluation, ack["acknowledgement_token"], "Synthetic firearms")))
        renewed = self.evaluate("Synthetic firearms")
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation))
        self.assertNotEqual(renewed["evaluation_id"], evaluation["evaluation_id"])

    def test_invoice_expiry_cannot_extend_aup_window(self):
        evaluation = self.evaluate()
        self.clock.advance(119)
        review = self.store.review_invoice(self.session, self.payload(evaluation))
        self.assertEqual(review["expires_at"], evaluation["expires_at"])
        self.clock.advance(1)
        self.assert_code("review_binding_rejected", lambda: self.store.consume_invoice(self.session, dict(invoice_payload(), review_token=review["review_token"], payload_digest=review["payload_digest"])))

    def test_session_liveness_reset_and_clock_rollback(self):
        evaluation = self.evaluate("Synthetic firearms")
        self.clock.advance(-1)
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation))
        self.clock.advance(1)
        self.acknowledge(evaluation)
        self.store.inject(self.session, "reset")
        self.assert_code("aup_evaluation_binding_rejected", lambda: self.acknowledge(evaluation))
        self.assertEqual(len(self.session.aup_audit), 0)
        stale = self.session
        del self.store.sessions[stale.session_id]
        self.assert_code("session_required", lambda: self.store.review_aup(stale, self.description))
        self.assert_code("session_required", lambda: self.store.acknowledge_aup(stale, dict(evaluation_id="x" * 43, description_digest="0" * 64, choice="CANCEL")))
        self.assert_code("session_required", lambda: self.store.review_invoice(stale, self.payload(evaluation)))

    def test_capacity_and_prune_do_not_evict_live_evaluations(self):
        evaluations = [self.evaluate() for _ in range(5)]
        before = deepcopy(self.session.aup_evaluations)
        self.assert_code("aup_capacity", self.evaluate)
        self.assertEqual(self.session.aup_evaluations, before)
        self.store.review_invoice(self.session, self.payload(evaluations[0]))
        self.evaluate()
        self.assertEqual(len(self.session.aup_evaluations), 5)
        self.clock.advance(120)
        self.evaluate()
        self.assertEqual(len(self.session.aup_evaluations), 1)

    def test_failure_preserves_evaluation_ack_and_review_capacity(self):
        for _ in range(5):
            evaluation = self.evaluate()
            self.store.review_invoice(self.session, self.payload(evaluation))
        evaluation = self.evaluate("Synthetic firearms")
        ack = self.acknowledge(evaluation)
        original = deepcopy(self.session.aup_evaluations)
        request = self.payload(evaluation, ack["acknowledgement_token"], "Synthetic firearms")
        for code, changes in (("sandbox_confirmation_required", {"confirm_sandbox_draft": False}), ("invalid_amount", {"amount": "0.00"}), ("review_capacity", {})):
            self.assert_code(code, lambda: self.store.review_invoice(self.session, dict(request, **changes)))
            self.assertEqual(self.session.aup_evaluations, original)
        self.assertEqual(len(self.session.invoice_reviews), 5)

    def test_parallel_ack_and_invoice_review_are_once(self):
        from concurrent.futures import ThreadPoolExecutor
        evaluation = self.evaluate("Synthetic firearms")
        def ack_call():
            try: return self.acknowledge(evaluation)
            except BoundaryError as error: return error.code
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(pool.map(lambda _: ack_call(), range(5)))
        acknowledgements = [value for value in results if type(value) is dict]
        self.assertEqual(len(acknowledgements), 1)
        self.assertEqual(results.count("aup_acknowledgement_already_used"), 4)
        request = self.payload(evaluation, acknowledgements[0]["acknowledgement_token"], "Synthetic firearms")
        def review_call():
            try: return self.store.review_invoice(self.session, request)
            except BoundaryError as error: return error.code
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(pool.map(lambda _: review_call(), range(5)))
        self.assertEqual(sum(type(value) is dict for value in results), 1)
        self.assertEqual(results.count("aup_evaluation_binding_rejected"), 4)
        self.assertEqual(len(self.session.invoice_reviews), 1)

    def test_forged_engine_categories_do_not_enter_audit_or_evaluations(self):
        for forged in ({"findings": [{"category": "RAW_SENTINEL", "code": "keyword_requires_policy_review"}], "match_status": "REVIEW_SIGNAL", "compliance_decision": "NOT_MADE", "advisory_only": True},
                       {"findings": [], "match_status": "REVIEW_SIGNAL", "compliance_decision": "NOT_MADE", "advisory_only": True},
                       {"findings": [], "match_status": "NO_MATCH", "compliance_decision": "APPROVED", "advisory_only": True}):
            with patch("app.store.check_aup", return_value=forged):
                self.assert_code("response_contract_failure", self.evaluate)
            self.assertEqual(self.session.aup_evaluations, {})
            self.assertEqual(len(self.session.aup_audit), 0)

    def test_store_payload_cannot_bypass_invoice_contract(self):
        evaluation = self.evaluate()
        for changes in ({"description": "x" * 201}, {"currency": "CAD"}, {"amount": "NaN"}):
            self.assert_code("schema_invalid", lambda: self.store.review_invoice(self.session, self.payload(evaluation, **changes)))
        self.assertIn(evaluation["evaluation_id"], self.session.aup_evaluations)

    def test_audit_bounded_without_raw_description_or_token(self):
        sentinel = "Synthetic firearms RAW_SENTINEL_NOT_IN_AUP_AUDIT"
        for _ in range(16):
            evaluation = self.evaluate(sentinel)
            ack = self.acknowledge(evaluation)
            self.assertNotIn(sentinel, repr(self.session.aup_evaluations))
            self.assertNotIn(ack["acknowledgement_token"], repr(self.session.aup_evaluations))
            self.acknowledge(evaluation, "CANCEL")
        self.assertEqual(len(self.session.aup_audit), 30)
        self.assertNotIn(sentinel, repr(self.session.aup_audit))
        self.assertNotIn(ack["acknowledgement_token"], repr(self.session.aup_audit))


class AupFunnelHttpTests(unittest.TestCase):
    setUp = ApiTests.setUp
    tearDown = ApiTests.tearDown
    new_session = ApiTests.new_session
    headers = ApiTests.headers
    post = ApiTests.post

    def test_full_engine_result_invalid_output_is_atomic_and_capacity_recovers(self):
        self.assertEqual(self.post("/aup/review", {"description": "existing valid evaluation"}).status_code, 200)
        live = self.store.sessions[self.session["session_id"]]
        before_evaluations = deepcopy(live.aup_evaluations)
        before_audit = deepcopy(live.aup_audit)
        baseline = check_aup("cup")
        mutations = [("recommendation", 12), ("recommendation", None), ("recommendation", []),
                     ("recommendation", ""), ("recommendation", "x" * 1001),
                     ("recommendation", "\ud800"), ("recommendation", "😀" * 501),
                     ("policy_version", None), ("policy_version", 12), ("policy_version", []),
                     ("policy_version", ""), ("policy_version", "x" * 129),
                     ("extra", "RAW_MARKER_NO_ECHO"), ("status", "manual_review")]
        for field, value in mutations:
            bad = dict(baseline, **{field: value})
            with self.subTest(field=field, value_type=type(value).__name__), patch("app.store.check_aup", return_value=bad):
                response = self.post("/aup/review", {"description": "cup"})
            self.assertEqual(response.status_code, 500, response.text)
            self.assertEqual(response.json()["error"]["code"], "response_contract_failure")
            self.assertNotIn("RAW_MARKER_NO_ECHO", response.text)
            self.assertEqual(live.aup_evaluations, before_evaluations)
            self.assertEqual(live.aup_audit, before_audit)
        for field in baseline:
            bad = dict(baseline)
            del bad[field]
            with self.subTest(missing=field), patch("app.store.check_aup", return_value=bad):
                response = self.post("/aup/review", {"description": "cup"})
            self.assertEqual(response.status_code, 500, response.text)
            self.assertEqual(live.aup_evaluations, before_evaluations)
            self.assertEqual(live.aup_audit, before_audit)
        response = self.post("/aup/review", {"description": "cup"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(len(live.aup_evaluations), 2)
        self.assertEqual(len(live.aup_audit), 2)

    def test_five_invalid_results_do_not_allocate_or_poison_capacity(self):
        live = self.store.sessions[self.session["session_id"]]
        bad = dict(check_aup("cup"), recommendation=12)
        with patch("app.store.check_aup", return_value=bad):
            for _ in range(5):
                response = self.post("/aup/review", {"description": "cup"})
                self.assertEqual(response.status_code, 500, response.text)
                self.assertEqual(live.aup_evaluations, {})
                self.assertEqual(len(live.aup_audit), 0)
        for _ in range(5):
            response = self.post("/aup/review", {"description": "cup"})
            self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.post("/aup/review", {"description": "cup"}).json()["error"]["code"], "aup_capacity")

    def test_complete_output_exact_text_limits_are_accepted(self):
        for recommendation in ("x", "x" * 1000, "😀" * 500):
            output = dict(check_aup("cup"), recommendation=recommendation, policy_version="v" * 128)
            with patch("app.store.check_aup", return_value=output):
                response = self.post("/aup/review", {"description": "cup"})
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()["recommendation"], recommendation)
            self.assertEqual(response.json()["policy_version"], "v" * 128)

    def test_direct_bypass_and_warning_choices(self):
        response = self.post("/paypal/invoices/review", dict(invoice_payload(), confirm_sandbox_draft=True))
        self.assertEqual(response.json()["error"]["code"], "aup_evaluation_required")
        for choice in ("RETURN_TO_EDIT", "CANCEL", "ACKNOWLEDGE_AND_CONTINUE"):
            evaluation = self.post("/aup/review", {"description": "Synthetic firearms"}).json()
            response = self.post("/aup/acknowledge", dict(evaluation_id=evaluation["evaluation_id"], description_digest=evaluation["description_digest"], choice=choice))
            self.assertEqual(response.status_code, 200, response.text)
            ack = response.json()
            payload = dict(invoice_payload(), description="Synthetic firearms", confirm_sandbox_draft=True,
                           evaluation_id=evaluation["evaluation_id"], description_digest=evaluation["description_digest"], acknowledgement_token=ack["acknowledgement_token"])
            review = self.post("/paypal/invoices/review", payload)
            self.assertEqual(review.status_code, 200 if choice == "ACKNOWLEDGE_AND_CONTINUE" else 422)
        self.assertEqual(self.calls, [])

    def test_new_routes_keep_csrf_schema_and_sanitized_errors(self):
        evaluation = self.post("/aup/review", {"description": "Synthetic firearms"}).json()
        payload = dict(evaluation_id=evaluation["evaluation_id"], description_digest=evaluation["description_digest"], choice="ACKNOWLEDGE_AND_CONTINUE")
        for headers, expected in (({"Origin": ORIGIN}, 401), (dict(self.headers(), **{"X-CSRF-Token": "bad"}), 403)):
            response = self.client.post(ROOT + "/aup/acknowledge", json=payload, headers=headers)
            self.assertEqual(response.status_code, expected)
        for changed in ({"choice": "APPROVE"}, {"description_digest": "private-sentinel"}, {"raw_description": "private-sentinel"}, {"evaluation_id": True}):
            response = self.post("/aup/acknowledge", dict(payload, **changed))
            self.assertEqual(response.status_code, 422)
            self.assertNotIn("private-sentinel", response.text)
        self.assertEqual(self.post("/aup/acknowledge", payload).status_code, 200)

    def test_scan_4000_invoice_200_and_mutation(self):
        self.assertEqual(self.post("/aup/review", {"description": "x" * 4000}).status_code, 200)
        self.assertEqual(self.post("/aup/review", {"description": "x" * 4001}).status_code, 422)
        request = bound_invoice_review(self, dict(invoice_payload(), description="x" * 200))
        self.assertEqual(self.post("/paypal/invoices/review", dict(request, description="x" * 201)).status_code, 422)
        self.assertEqual(self.post("/paypal/invoices/review", dict(request, description="y" * 200)).json()["error"]["code"], "aup_evaluation_binding_rejected")
        self.assertEqual(self.post("/paypal/invoices/review", request).status_code, 200)


if __name__ == "__main__":
    unittest.main()
