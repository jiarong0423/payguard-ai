"""Session-bound policy/advisory routes and nested trusted-output guards."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore
from payguard.applicability import ApplicabilityError, assess_applicability
from payguard.advisory_eval import AdvisoryError, evaluate_advisory
from payguard.retrieval import load_corpus

ORIGIN = {"Origin": "http://localhost:5173"}
ASSESS = "/api/v1/policy/assess"
EVALUATE = "/api/v1/advisory/evaluate"
AS_OF = "2026-10-07T00:00:00Z"
CONTEXT = {"jurisdiction": "US", "theme": "source_compliance", "as_of": AS_OF, "observation_max_age_days": 30}
SENTINEL = "RAW_CANDIDATE_NO_ECHO_8F15"


def candidate(region="US", theme="source_compliance", kind="policy_reference", reference="PP-US-AUP-POLICY", instant=AS_OF):
    corpus = load_corpus()
    return json.dumps({"schema_version": 1, "jurisdiction": region, "theme": theme, "as_of": instant,
                       "status": "manual_review", "advisory_only": True, "operational_authority": "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
                       "claims": [{"claim_id": "RAW_CLAIM_ID_8F15", "claim_type": kind, "text": SENTINEL, "citation_chunk_ids": [reference]}]})


class PolicyApiTests(unittest.TestCase):
    def setUp(self):
        self.clock = lambda: datetime(2026, 10, 7, tzinfo=timezone.utc)
        self.store = SessionStore(clock=self.clock)
        self.provider = PaypalAdapter(config_loader=lambda: PaypalConfig())
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55021), raise_server_exceptions=False)
        self.client.__enter__()
        session = self.client.post("/api/v1/demo/sessions", json={}, headers=ORIGIN).json()
        self.headers = dict(ORIGIN, **{"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider.open_clients, 0)

    def assess(self, **changes):
        return self.client.post(ASSESS, json=dict(CONTEXT, **changes), headers=self.headers)

    def evaluate(self, raw=None, **changes):
        return self.client.post(EVALUATE, json=dict(CONTEXT, candidate_json=candidate() if raw is None else raw, **changes), headers=self.headers)

    def assert_safe(self, response, status, code=None):
        self.assertEqual(response.status_code, status, response.text)
        self.assertEqual(set(response.json()), {"error"})
        if code is not None:
            self.assertEqual(response.json()["error"]["code"], code)
        self.assertNotIn(SENTINEL, response.text)
        self.assertNotIn("/private/", response.text)

    def test_real_assessment_exact_regions_and_themes(self):
        for theme in ("source_compliance", "velocity_guard", "dispute_mediation"):
            with self.subTest(theme=theme):
                response = self.assess(theme=theme)
                self.assertEqual(response.status_code, 200, response.text)
                result = response.json()
                self.assertEqual(result["status"], "INCOMPLETE_POLICY_EVIDENCE")
                self.assertEqual(result["current_policy_applicability"], "NOT_ESTABLISHED")
                self.assertFalse(result["coverage"]["complete"])
                self.assertTrue(all(s["jurisdiction_normalized"] == "US" and s["effective_date"] is None for s in result["sources"]))
                self.assertTrue(all(c["theme"] == theme and c["jurisdiction"] == "US" for c in result["chunks"]))
        for region in ("CA", "GB", "GLOBAL"):
            with self.subTest(region=region):
                self.assert_safe(self.assess(jurisdiction=region), 422, "schema_invalid")

    def test_assessment_date_budget_and_offset(self):
        future = self.assess(as_of="2026-10-03T00:00:00Z").json()
        stale = self.assess(as_of="2026-11-05T00:00:00Z", observation_max_age_days=1).json()
        self.assertIn("FUTURE_OBSERVATION", future["reason_codes"])
        self.assertIn("STALE_OBSERVATION", stale["reason_codes"])
        self.assertEqual(self.assess(as_of="2026-10-07T08:00:00+08:00").json(), self.assess().json())

    def test_eval_three_themes_and_claim_categories(self):
        cases = (
            ("source_compliance", "policy_reference", "PP-US-AUP-POLICY"),
            ("velocity_guard", "procedural_reference", "US-COURT-ZEPEDA-2017-DOC357-ORDER"),
            ("dispute_mediation", "api_reference", "PP-REASONS-INR"),
        )
        for theme, kind, reference in cases:
            body = dict(CONTEXT, theme=theme, candidate_json=candidate("US", theme, kind, reference))
            response = self.client.post(EVALUATE, json=body, headers=self.headers)
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()["status"], "STRUCTURE_COMPATIBLE")
            self.assertEqual(response.json()["semantic_entailment"], "NOT_EVALUATED")
        for kind, expected in (("current_policy", "INCOMPLETE_EVIDENCE"), ("financial_action", "REJECTED"), ("assurance", "REJECTED")):
            response = self.evaluate(candidate(kind=kind))
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()["status"], expected)
            self.assertEqual(response.json()["model_generation"], "NOT_RUN")

    def test_invalid_input_contracts(self):
        for changes in ({"jurisdiction": "CA"}, {"jurisdiction": "GB"}, {"jurisdiction": "GLOBAL"}, {"jurisdiction": "EU"}, {"theme": "other"}, {"as_of": "2026-10-05T00:00:00"}, {"observation_max_age_days": True}, {"observation_max_age_days": "30"}, {"observation_max_age_days": -1}, {"observation_max_age_days": 365001}, {"path": "/private/forged"}, {"metadata": {"effective": True}}):
            with self.subTest(changes=changes):
                self.assert_safe(self.assess(**changes), 422)
        for key in CONTEXT:
            body = dict(CONTEXT)
            del body[key]
            self.assert_safe(self.client.post(ASSESS, json=body, headers=self.headers), 422)
        for raw in ("", "x" * 8193, {"bad": True}, 5):
            self.assert_safe(self.evaluate(raw), 422)

    def test_inner_json_duplicate_nonfinite_depth_controls_and_context(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '[' * 9 + '0' + ']' * 9, json.dumps({"text": "\n" + SENTINEL}), candidate(region="UK")):
            with self.subTest(raw_kind=len(raw)):
                self.assert_safe(self.evaluate(raw), 422)
        malformed = json.loads(candidate())
        malformed["claims"][0]["source_id"] = "FORGED"
        self.assert_safe(self.evaluate(json.dumps(malformed)), 422)
        malformed = json.loads(candidate())
        malformed["claims"][0]["citation_chunk_ids"] *= 2
        self.assert_safe(self.evaluate(json.dumps(malformed)), 422)

    def test_surrogate_encoding_and_outer_json_body_gates(self):
        body = dict(CONTEXT, candidate_json="\ud800")
        self.assert_safe(self.client.post(EVALUATE, content=json.dumps(body).encode(), headers=dict(self.headers, **{"Content-Type": "application/json"})), 422)
        self.assert_safe(self.client.post(EVALUATE, content=b'{' + b' ' * 16384 + b'}', headers=dict(self.headers, **{"Content-Type": "application/json"})), 413)
        for raw in (b'{"jurisdiction":"US","jurisdiction":"UK"}', b'{"budget":NaN}'):
            self.assert_safe(self.client.post(ASSESS, content=raw, headers=dict(self.headers, **{"Content-Type": "application/json"})), 422)

    def test_exact_candidate_character_cap_and_UTF8_transport_cap(self):
        raw = candidate()
        raw += " " * (8192 - len(raw))
        self.assertEqual(len(raw), 8192)
        self.assertEqual(self.evaluate(raw).status_code, 200)
        oversized_transport = dict(CONTEXT, candidate_json="😀" * 8192)
        self.assert_safe(self.client.post(EVALUATE, content=json.dumps(oversized_transport, ensure_ascii=False).encode("utf-8"), headers=dict(self.headers, **{"Content-Type": "application/json"})), 413)

    def test_auth_origin_csrf_denials_never_call_core(self):
        with patch("app.main.assess_applicability") as assess_call, patch("app.main.evaluate_advisory") as eval_call, patch("app.main.applicability.assess_applicability") as assess_guard, patch("app.main.advisory_eval.evaluate_advisory") as eval_guard:
            for path, body in ((ASSESS, CONTEXT), (EVALUATE, dict(CONTEXT, candidate_json=candidate()))):
                self.assert_safe(self.client.post(path, json=body, headers=ORIGIN), 401)
                self.assert_safe(self.client.post(path, json=body, headers=dict(self.headers, **{"X-CSRF-Token": "bad"})), 403)
                self.assert_safe(self.client.post(path, json=body, headers=dict(self.headers, Origin="https://wrong.example")), 403)
            for call in (assess_call, eval_call, assess_guard, eval_guard):
                call.assert_not_called()

    def test_expired_session_and_quota(self):
        token = self.headers["X-Demo-Session"]
        self.store.clock = lambda: datetime(2026, 10, 8, tzinfo=timezone.utc)
        self.assert_safe(self.assess(), 401)
        self.store.clock = self.clock
        session = self.client.post("/api/v1/demo/sessions", json={}, headers=ORIGIN).json()
        self.store.rate_limit = 1
        self.headers.update({"X-Demo-Session": session["session_id"], "X-CSRF-Token": session["csrf_token"]})
        self.assertEqual(self.assess().status_code, 200)
        self.assert_safe(self.evaluate(), 429)
        self.assertNotEqual(token, session["session_id"])

    def test_library_and_second_read_fail_closed_safe_errors(self):
        for symbol, error, path, body in (("app.main.assess_applicability", ApplicabilityError("applicability_corpus_unavailable"), ASSESS, CONTEXT), ("app.main.evaluate_advisory", AdvisoryError("advisory_corpus_unavailable"), EVALUATE, dict(CONTEXT, candidate_json=candidate())), ("app.main.applicability.assess_applicability", ApplicabilityError("applicability_corpus_unavailable"), ASSESS, CONTEXT), ("app.main.advisory_eval.evaluate_advisory", AdvisoryError("advisory_corpus_unavailable"), EVALUATE, dict(CONTEXT, candidate_json=candidate()))):
            with self.subTest(symbol=symbol), patch(symbol, side_effect=error):
                response = self.client.post(path, json=body, headers=self.headers)
                self.assert_safe(response, 503, "reference_unavailable")
                self.assertNotIn("Sandbox", response.text)
        with patch("app.main.assess_applicability", side_effect=RuntimeError(SENTINEL + "/private/path")):
            self.assert_safe(self.assess(), 500, "internal_error")

    def test_assessment_forged_nested_response_guards(self):
        baseline = assess_applicability(**CONTEXT)
        mutations = [
            lambda d: d.update(raw_candidate=SENTINEL),
            lambda d: d.update(corpus_digest="0" * 64),
            lambda d: d["filters_applied"].update(jurisdiction="UK"),
            lambda d: d["coverage"].update(regional_source_count=1),
            lambda d: d["coverage"]["official_policy_chunk_count_by_theme"].update(dispute_mediation=30),
            lambda d: d["sources"][0].update(url="javascript:alert(1)"),
            lambda d: d["sources"][0].update(jurisdiction="forged provenance"),
            lambda d: d["sources"][0].update(retrieved_at="2026-10-01T00:00:00Z"),
            lambda d: d["sources"][0].update(effective_date="2000-01-01", effective_date_status="DOCUMENT_STATED"),
            lambda d: d["chunks"][0].update(text_sha256="0" * 64),
            lambda d: d["sources"][0].update(citation_chunk_ids=[]),
            lambda d: d.update(status="APPLICABLE", advisory_only=False),
        ]
        for mutate in mutations:
            forged = deepcopy(baseline)
            mutate(forged)
            with patch("app.main.assess_applicability", return_value=forged):
                self.assert_safe(self.assess(), 500, "response_contract_failure")

    def test_evaluation_forged_nested_response_guards(self):
        raw = candidate()
        baseline = evaluate_advisory(raw.encode(), **CONTEXT)
        mutations = [
            lambda d: d.update(candidate_json=SENTINEL),
            lambda d: d.update(semantic_entailment="PASS"),
            lambda d: d.update(PII_quality="PASS"),
            lambda d: d["requested_context"].update(theme="velocity_guard"),
            lambda d: d["coverage"].update(regional_source_count=1),
            lambda d: d["claim_gates"][0].update(trusted_citation_chunk_ids=["FORGED-ID"]),
            lambda d: d["claim_gates"][0].update(claim_type="assurance"),
            lambda d: d["claim_gates"][0].update(reason_codes=["CURRENT_POLICY_NOT_ESTABLISHED"]),
            lambda d: d.update(claim_count=2),
            lambda d: d["claim_gates"][0].update(claim_index=1),
            lambda d: d.update(model_generation="RUN", operational_authority="FINANCIAL_ACTION_ALLOWED"),
        ]
        for mutate in mutations:
            forged = deepcopy(baseline)
            mutate(forged)
            with patch("app.main.evaluate_advisory", return_value=forged):
                self.assert_safe(self.evaluate(raw), 500, "response_contract_failure")

    def test_no_candidate_echo_or_merchant_state_mutation(self):
        self.client.post("/api/v1/demo/inject", json={"scenario": "burst"}, headers=self.headers)
        self.client.post("/api/v1/demo/inject", json={"scenario": "dispute"}, headers=self.headers)
        before = self.client.get("/api/v1/demo/state", headers=self.headers).json()
        for response in (self.assess(), self.evaluate(), self.evaluate(candidate(kind="financial_action"))):
            self.assertEqual(response.status_code, 200, response.text)
            self.assertNotIn(SENTINEL, response.text)
            self.assertNotIn("RAW_CLAIM_ID_8F15", response.text)
        self.assertEqual(before, self.client.get("/api/v1/demo/state", headers=self.headers).json())
        self.assertNotIn(SENTINEL, repr(self.store.__dict__))


if __name__ == "__main__":
    unittest.main()
