"""HTTP integration for the bounded synthetic AI evidence brief."""

from copy import deepcopy
from datetime import datetime, timezone
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import httpx

from app.ai_brief import (AiBriefError, GENERATED_TEXT_INVENTORY, LIMITATIONS,
                          PROMPT_CONTRACT_DIGEST, PROMPT_CONTRACT_ID)
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore


ORIGIN = "http://localhost:5173"
ROOT = "/api/v1"


def valid_brief(stage="source_compliance"):
    citations = {
        "source_compliance": ["PP-US-AUP-POLICY"],
        "velocity_guard": ["PP-US-UA-VELOCITY"],
        "dispute_mediation": ["PP-REASONS-INR", "PP-EVIDENCE-TRACKING"],
    }
    inventory = GENERATED_TEXT_INVENTORY[stage]
    return {
        "schema_version": "1.0",
        "status": "completed",
        "stage": stage,
        "fixture_id": "payguard-fixed-synthetic-brief-v1",
        "context_digest": "a" * 64,
        "corpus_digest": "b" * 64,
        "model": "gemini-3.8-flash",
        "prompt_contract_id": PROMPT_CONTRACT_ID,
        "prompt_contract_digest": PROMPT_CONTRACT_DIGEST,
        "execution_evidence": "SYNTHETIC_TEST_RESPONSE",
        "brief": {
            "summary": inventory["summary"][0],
            "evidence_points": [inventory["evidence_points"][0]],
            "missing_evidence": [inventory["missing_evidence"][0]],
            "citation_ids": citations[stage],
        },
        "ai_generated": True,
        "advisory_only": True,
        "human_review_required": True,
        "compliance_decision": "NOT_MADE",
        "current_policy_applicability": "NOT_ESTABLISHED",
        "external_action_authorized": False,
        "workflow_transition_authorized": False,
        "semantic_entailment": "NOT_EVALUATED",
        "limitations": list(LIMITATIONS),
    }


class FakeBriefAdapter:
    def __init__(self, result=None, error=None):
        self.result = valid_brief() if result is None else result
        self.error = error
        self.calls = []

    def validate_attempt_configuration(self):
        return None

    async def generate(self, request):
        self.calls.append(deepcopy(request))
        if self.error is not None:
            raise self.error
        result = deepcopy(self.result)
        if result.get("stage") != request["stage"]:
            result = valid_brief(request["stage"])
        return result


class FixedClock:
    def __call__(self):
        return datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)


class AiApiTests(unittest.TestCase):
    def setUp(self):
        self.provider_calls = []

        def provider_handler(request):
            self.provider_calls.append((request.method, request.url.path))
            raise AssertionError("AI route must not invoke PayPal")

        self.provider = PaypalAdapter(
            config_loader=lambda: PaypalConfig(),
            transport=httpx.MockTransport(provider_handler),
            clock=FixedClock(),
        )
        self.adapter = FakeBriefAdapter()
        self.app = create_app(store=SessionStore(clock=FixedClock()), paypal=self.provider, ai_brief=self.adapter)
        self.client = TestClient(
            self.app,
            base_url="http://127.0.0.1:8000",
            client=("127.0.0.1", 55101),
            raise_server_exceptions=False,
        )
        self.client.__enter__()
        response = self.client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN})
        self.assertEqual(response.status_code, 201, response.text)
        self.session = response.json()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider.open_clients, 0)
        self.assertEqual(self.provider_calls, [])

    def headers(self):
        return {
            "Origin": ORIGIN,
            "X-Demo-Session": self.session["session_id"],
            "X-CSRF-Token": self.session["csrf_token"],
        }

    def state(self):
        response = self.client.get(ROOT + "/demo/state", headers=self.headers())
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def post(self, payload, headers=None):
        return self.client.post(ROOT + "/ai/evidence-brief", json=payload, headers=self.headers() if headers is None else headers)

    def prepare_stage(self, stage):
        if stage == "source_compliance":
            response = self.client.post(
                ROOT + "/aup/review",
                json={"description": "Synthetic counterfeit luxury goods"},
                headers=self.headers(),
            )
        elif stage == "velocity_guard":
            response = self.client.post(
                ROOT + "/demo/inject",
                json={"scenario": "burst"},
                headers=self.headers(),
            )
        else:
            injected = self.client.post(
                ROOT + "/demo/inject",
                json={"scenario": "dispute"},
                headers=self.headers(),
            )
            self.assertEqual(injected.status_code, 200, injected.text)
            response = self.client.post(
                ROOT + "/disputes/case-ref-001/draft",
                json={},
                headers=self.headers(),
            )
        self.assertEqual(response.status_code, 200, response.text)

    def test_success_is_stage_only_and_does_not_mutate_business_state(self):
        for stage in ("source_compliance", "velocity_guard", "dispute_mediation"):
            self.prepare_stage(stage)
            before = self.state()
            response = self.post({"stage": stage})
            self.assertEqual(response.status_code, 200, response.text)
            body = response.json()
            self.assertEqual(body["stage"], stage)
            self.assertEqual(body["execution_evidence"], "SYNTHETIC_TEST_RESPONSE")
            self.assertEqual(body["compliance_decision"], "NOT_MADE")
            self.assertIs(body["external_action_authorized"], False)
            self.assertIs(body["workflow_transition_authorized"], False)
            self.assertEqual(self.state(), before)
        self.assertEqual(self.adapter.calls, [
            {"stage": "source_compliance"},
            {"stage": "velocity_guard"},
            {"stage": "dispute_mediation"},
        ])
        fourth = self.post({"stage": "source_compliance"})
        self.assertEqual(fourth.status_code, 429, fourth.text)
        self.assertEqual(fourth.json()["error"]["code"], "ai_attempt_limit")
        self.assertEqual(len(self.adapter.calls), 3)

    def test_stage_context_is_required_before_adapter_call(self):
        for stage in ("source_compliance", "velocity_guard", "dispute_mediation"):
            with self.subTest(stage=stage):
                response = self.post({"stage": stage})
                self.assertEqual(response.status_code, 409, response.text)
                self.assertEqual(response.json()["error"]["code"], "ai_context_not_ready")
        self.assertEqual(self.adapter.calls, [])

    def test_source_compliance_uses_latest_review_and_closes_after_invoice_binding(self):
        warning_description = "Synthetic firearms description"
        warning = self.client.post(
            ROOT + "/aup/review",
            json={"description": warning_description},
            headers=self.headers(),
        )
        self.assertEqual(warning.status_code, 200, warning.text)
        warning = warning.json()
        self.assertEqual(warning["match_status"], "REVIEW_SIGNAL")

        clean = self.client.post(
            ROOT + "/aup/review",
            json={"description": "Synthetic ceramic cup"},
            headers=self.headers(),
        )
        self.assertEqual(clean.status_code, 200, clean.text)
        self.assertEqual(clean.json()["match_status"], "NO_MATCH")
        blocked = self.post({"stage": "source_compliance"})
        self.assertEqual(blocked.status_code, 409, blocked.text)
        self.assertEqual(self.adapter.calls, [])

        latest = self.client.post(
            ROOT + "/aup/review",
            json={"description": warning_description},
            headers=self.headers(),
        )
        self.assertEqual(latest.status_code, 200, latest.text)
        latest = latest.json()
        allowed = self.post({"stage": "source_compliance"})
        self.assertEqual(allowed.status_code, 200, allowed.text)
        self.assertEqual(self.adapter.calls, [{"stage": "source_compliance"}])

        acknowledgement = self.client.post(
            ROOT + "/aup/acknowledge",
            json={
                "evaluation_id": latest["evaluation_id"],
                "description_digest": latest["description_digest"],
                "choice": "ACKNOWLEDGE_AND_CONTINUE",
            },
            headers=self.headers(),
        )
        self.assertEqual(acknowledgement.status_code, 200, acknowledgement.text)
        review = self.client.post(
            ROOT + "/paypal/invoices/review",
            json={
                "description": warning_description,
                "amount": "10.00",
                "currency": "USD",
                "confirm_sandbox_draft": True,
                "evaluation_id": latest["evaluation_id"],
                "description_digest": latest["description_digest"],
                "acknowledgement_token": acknowledgement.json()["acknowledgement_token"],
            },
            headers=self.headers(),
        )
        self.assertEqual(review.status_code, 200, review.text)
        blocked_after_binding = self.post({"stage": "source_compliance"})
        self.assertEqual(blocked_after_binding.status_code, 409, blocked_after_binding.text)
        self.assertEqual(self.adapter.calls, [{"stage": "source_compliance"}])

    def test_dispute_mediation_rejects_non_inr_before_draft_and_adapter_call(self):
        injected = self.client.post(
            ROOT + "/demo/inject",
            json={"scenario": "dispute"},
            headers=self.headers(),
        )
        self.assertEqual(injected.status_code, 200, injected.text)
        session = self.app.state.store.sessions[self.session["session_id"]]
        session.disputes["demo-case-001"]["reason"] = "SNAD"
        draft = self.client.post(
            ROOT + "/disputes/case-ref-001/draft",
            json={},
            headers=self.headers(),
        )
        self.assertEqual(draft.status_code, 422, draft.text)
        self.assertEqual(draft.json()["error"]["code"], "dispute_context_not_ready")
        self.assertEqual(session.drafts, {})
        self.assertEqual(session.draft_expires, {})
        blocked = self.post({"stage": "dispute_mediation"})
        self.assertEqual(blocked.status_code, 409, blocked.text)
        self.assertEqual(self.adapter.calls, [])

    def test_session_origin_csrf_and_schema_fail_before_adapter(self):
        cases = [
            ({"stage": "source_compliance"}, {"Origin": ORIGIN}, 401),
            ({"stage": "source_compliance"}, {"Origin": ORIGIN, "X-Demo-Session": self.session["session_id"]}, 403),
            ({"stage": "source_compliance"}, {**self.headers(), "Origin": "https://attacker.invalid"}, 403),
            ({"stage": "unknown"}, self.headers(), 422),
            ({"stage": "source_compliance", "prompt": "private"}, self.headers(), 422),
        ]
        for payload, headers, expected in cases:
            with self.subTest(expected=expected, payload=payload):
                response = self.post(payload, headers)
                self.assertEqual(response.status_code, expected, response.text)
        self.assertEqual(self.adapter.calls, [])

    def test_ai_error_is_fixed_and_sanitized(self):
        self.prepare_stage("source_compliance")
        self.adapter.error = AiBriefError(502, "ai_provider_failure")
        response = self.post({"stage": "source_compliance"})
        self.assertEqual(response.status_code, 502, response.text)
        self.assertEqual(response.json(), {"error": {"code": "ai_provider_failure", "message": "The AI evidence brief is unavailable or could not be verified."}})
        self.assertNotIn("provider", response.text.lower().replace("ai_provider_failure", ""))
        retry = self.post({"stage": "source_compliance"})
        self.assertEqual(retry.status_code, 409, retry.text)
        self.assertEqual(retry.json()["error"]["code"], "ai_stage_attempt_exhausted")
        self.assertEqual(len(self.adapter.calls), 1)

    def test_malformed_adapter_result_fails_response_contract(self):
        self.prepare_stage("source_compliance")
        malformed = valid_brief()
        malformed["external_action_authorized"] = True
        self.adapter.result = malformed
        response = self.post({"stage": "source_compliance"})
        self.assertEqual(response.status_code, 500, response.text)
        self.assertEqual(response.json()["error"]["code"], "response_contract_failure")

    def test_default_adapter_is_disabled_without_outbound_opt_in_and_does_not_reserve_attempt(self):
        store = SessionStore(clock=FixedClock())
        app = create_app(store=store, paypal=self.provider)
        with TestClient(app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55102), raise_server_exceptions=False) as client:
            session = client.post(ROOT + "/demo/sessions", json={}, headers={"Origin": ORIGIN}).json()
            headers = {"Origin": ORIGIN, "X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]}
            prepared = client.post(ROOT + "/aup/review", json={"description": "Synthetic counterfeit goods"}, headers=headers)
            self.assertEqual(prepared.status_code, 200, prepared.text)
            with patch.dict("os.environ", {}, clear=True):
                response = client.post(ROOT + "/ai/evidence-brief", json={"stage": "source_compliance"}, headers=headers)
            self.assertEqual(store.ai_attempt_budget.used, 0)
            app.state.ai_brief = FakeBriefAdapter()
            retry = client.post(ROOT + "/ai/evidence-brief", json={"stage": "source_compliance"}, headers=headers)
        self.assertEqual(response.status_code, 503, response.text)
        self.assertEqual(response.json()["error"]["code"], "ai_disabled")
        self.assertEqual(response.json()["error"]["message"], "The AI evidence brief is unavailable or could not be verified.")
        self.assertEqual(retry.status_code, 200, retry.text)
        self.assertEqual(store.ai_attempt_budget.used, 1)


if __name__ == "__main__":
    unittest.main()
