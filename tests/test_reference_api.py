"""Local public-reference HTTP boundaries; no provider or external transport."""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient
import httpx

from app.main import MAX_BODY_BYTES, create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.store import SessionStore
from payguard.retrieval import RetrievalError, load_corpus


ORIGIN = "http://localhost:5173"
ROUTE = "/api/v1/references/search"


def request_body(**changes):
    return dict({"query": "prior approval", "theme": "source_compliance", "jurisdiction": "US"}, **changes)


class ReferenceApiTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 6, 5, 0, tzinfo=timezone.utc)
        self.store = SessionStore(clock=lambda: self.now)
        self.provider_calls = []
        def reject_provider(request):
            self.provider_calls.append(request)
            raise AssertionError("Reference endpoint must not call provider")
        self.transport = httpx.MockTransport(reject_provider)
        self.provider = PaypalAdapter(config_loader=lambda: PaypalConfig(), transport=self.transport, clock=lambda: self.now)
        self.loader = Mock(side_effect=load_corpus)
        self.app = create_app(store=self.store, paypal=self.provider, reference_loader=self.loader)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 55101), raise_server_exceptions=False)
        self.client.__enter__()
        response = self.client.post("/api/v1/demo/sessions", json={}, headers={"Origin": ORIGIN})
        self.assertEqual(response.status_code, 201)
        self.session = response.json()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider_calls, [])
        self.assertEqual(self.provider.open_clients, 0)

    def headers(self, **changes):
        return dict({"Origin": ORIGIN, "X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]}, **changes)

    def search(self, body=None, headers=None):
        return self.client.post(ROUTE, json=request_body() if body is None else body, headers=self.headers() if headers is None else headers)

    def test_three_themes_citations_complete_and_reference_only(self):
        for theme, query in (("source_compliance", "prior approval"), ("velocity_guard", "rapid sales growth"), ("dispute_mediation", "INR")):
            with self.subTest(theme=theme):
                response = self.search(request_body(theme=theme, query=query, case_stage="not_applicable"))
                self.assertEqual(response.status_code, 200, response.text)
                body = response.json()
                self.assertEqual(body["status"], "references_found")
                self.assertEqual(body["source"], "public_reference")
                self.assertIs(body["advisory_only"], True)
                self.assertEqual(body["operational_authority"], "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION")
                self.assertEqual(body["filters_applied"]["limit"], 3)
                self.assertLessEqual(len(body["results"]), 3)
                for row in body["results"]:
                    self.assertEqual(row["jurisdiction"], "US")
                    self.assertEqual(row["case_stage"], "not_applicable")
                    for key in ("source_id", "chunk_id", "title", "source_title", "text", "url", "locator", "material_type", "jurisdiction_label", "case_outcome", "retrieved_at", "text_sha256", "relevance_score", "source_updated_date", "source_updated_date_status", "effective_date", "effective_date_status", "decision_date", "decision_date_status", "decision_acceptance_deadline"):
                        self.assertIn(key, row)

    def test_exact_region_theme_and_empty_without_fallback(self):
        response = self.search(request_body(query="zxqv12345totallyabsent"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "evidence_missing")
        self.assertEqual(response.json()["results"], [])
        self.assertNotIn("query", response.json())
        self.loader.reset_mock()
        for jurisdiction in ("CA", "GB", "GLOBAL"):
            with self.subTest(jurisdiction=jurisdiction):
                response = self.search(request_body(jurisdiction=jurisdiction))
                self.assertEqual(response.status_code, 422)
                self.assertEqual(response.json()["error"]["code"], "schema_invalid")
        self.loader.assert_not_called()

    def test_procedural_order_never_final_merits(self):
        expected = {
            "settlement hold reserve": "SETTLEMENT_APPROVAL_NOT_FINAL_MERITS",
            "arbitration AUP allegation": "ARBITRATION_COMPELLED_UNDERLYING_MERITS_NOT_DECIDED",
        }
        for query, outcome in expected.items():
            with self.subTest(query=query):
                body = request_body(query=query, theme="velocity_guard" if query.startswith("settlement") else "source_compliance", case_stage="procedural_order")
                response = self.search(body)
                self.assertEqual(response.status_code, 200)
                rows = response.json()["results"]
                self.assertTrue(rows)
                self.assertTrue(all(row["case_stage"] == "procedural_order" and row["case_outcome"] == outcome for row in rows))
                body["case_stage"] = "not_applicable"
                body["material_types"] = ["public_court_order_copy"]
                self.assertEqual(self.search(body).json()["results"], [])

    def test_date_unknown_preserved_and_known_filter(self):
        body = self.search(request_body(query="settlement", theme="velocity_guard", case_stage="procedural_order")).json()
        self.assertTrue(body["results"])
        self.assertTrue(all(row["source_updated_date"] is None and row["source_updated_date_status"] == "MISSING" for row in body["results"]))
        response = self.search(request_body(query="settlement", theme="velocity_guard", case_stage="procedural_order", require_known_source_date=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"], [])
        response = self.search(request_body(query="rapid sales growth", theme="velocity_guard", require_known_source_date=True, max_source_age_days=365, as_of="2026-10-06T12:00:00+08:00"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["filters_applied"]["as_of"], "2026-10-06T04:00:00+00:00")

    def test_material_types_sorted_exact_limit(self):
        response = self.search(request_body(query="AUP", material_types=["official_policy", "public_court_order_copy"], limit=1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["filters_applied"]["material_types"], ["official_policy", "public_court_order_copy"])
        self.assertLessEqual(len(response.json()["results"]), 1)

    def test_loader_after_auth_and_each_search(self):
        self.assertEqual(self.search(headers={"Origin": ORIGIN}).status_code, 401)
        self.assertEqual(self.search(headers=self.headers(**{"X-CSRF-Token": "invalid"})).status_code, 403)
        self.assertEqual(self.search(headers=self.headers(Origin="https://example.invalid")).status_code, 403)
        self.loader.assert_not_called()
        self.assertEqual(self.search().status_code, 200)
        self.assertEqual(self.search().status_code, 200)
        self.assertEqual(self.loader.call_count, 2)
        self.loader.side_effect = RetrievalError("corpus_digest_mismatch")
        self.assertEqual(self.search().status_code, 503)
        self.assertEqual(self.loader.call_count, 3)

    def test_expired_session_has_no_loader(self):
        self.now += timedelta(seconds=901)
        self.assertEqual(self.search().status_code, 401)
        self.loader.assert_not_called()

    def test_host_origin_csrf_and_anonymous_get_boundaries(self):
        for headers in (self.headers(Host="example.invalid:8000"), self.headers(Origin="null"), {"X-Demo-Session": self.session["session_id"], "X-CSRF-Token": self.session["csrf_token"]}):
            with self.subTest(headers=headers):
                self.assertEqual(self.search(headers=headers).status_code, 403)
        self.assertEqual(self.client.get(ROUTE, headers=self.headers()).status_code, 405)
        self.loader.assert_not_called()

    def test_strict_types_ranges_and_extra_keys(self):
        for changes in ({"limit": True}, {"limit": "3"}, {"limit": 3.0}, {"limit": 0}, {"limit": 11}, {"max_source_age_days": True}, {"max_source_age_days": -1}, {"max_source_age_days": 365001}, {"require_known_source_date": 1}, {"require_known_source_date": "false"}, {"query": 123}, {"query": "a" * 513}, {"theme": "unknown"}, {"jurisdiction": "CA"}, {"case_stage": "final"}, {"material_types": []}, {"material_types": ["unknown"]}, {"loader": "/private/path"}, {"expected_digest": "bad"}, {"as_of": 42}):
            with self.subTest(changes=changes):
                response = self.search(request_body(**changes))
                self.assertEqual(response.status_code, 422, response.text)
        self.loader.assert_not_called()

    def test_library_query_and_filter_errors_are_safe_422(self):
        for changes, expected in (({"query": "   "}, "query_invalid"), ({"query": "secret\x00query"}, "query_invalid"), ({"material_types": ["official_policy", "official_policy"]}, "filter_invalid"), ({"max_source_age_days": 1}, "filter_invalid"), ({"as_of": "2026-10-04T23:00:00XX"}, "filter_invalid")):
            with self.subTest(changes=changes):
                response = self.search(request_body(**changes))
                self.assertEqual(response.status_code, 422)
                self.assertEqual(response.json()["error"]["code"], expected)
                self.assertNotIn("secret", response.text)

    def test_duplicate_json_nonfinite_and_body_quota(self):
        headers = dict(self.headers(), **{"Content-Type": "application/json"})
        for raw in ('{"query":"AUP","query":"secret","theme":"source_compliance","jurisdiction":"US"}', '{"limit":NaN}', '[]'):
            self.assertEqual(self.client.post(ROUTE, content=raw, headers=headers).status_code, 422)
        self.assertEqual(self.client.post(ROUTE, content="x" * (MAX_BODY_BYTES + 1), headers=headers).status_code, 413)
        self.loader.assert_not_called()

    def test_rate_limit_precedes_loader(self):
        self.store.rate_limit = 1
        self.assertEqual(self.search().status_code, 200)
        self.assertEqual(self.search().status_code, 429)
        self.assertEqual(self.loader.call_count, 1)

    def test_corpus_failures_are_reference_unavailable_not_sandbox(self):
        for code in ("corpus_unavailable", "corpus_digest_mismatch", "corpus_invalid", "corpus_path_invalid", "trusted_digest_invalid"):
            with self.subTest(code=code):
                self.loader.side_effect = RetrievalError(code)
                response = self.search(request_body(query="private_secret_query"))
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json()["error"]["code"], "reference_unavailable")
                self.assertNotIn("Sandbox", response.text)
                self.assertNotIn("private_secret_query", response.text)
                self.assertNotIn(code, response.text)

    def test_unexpected_loader_failure_is_safe_500(self):
        for error in (RuntimeError("private_secret_query /private/unknown"), ValueError("private_secret_query /private/unknown")):
            with self.subTest(error=type(error).__name__):
                self.loader.side_effect = error
                response = self.search()
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response.json()["error"]["code"], "internal_error")
                self.assertNotIn("private", response.text)

    def test_no_query_retention_or_business_mutation(self):
        session = self.store.sessions[self.session["session_id"]]
        keys = ("transactions", "disputes", "drafts", "approved", "invoice_reviews", "activity", "scenario")
        before = {key: deepcopy(getattr(session, key)) for key in keys}
        marker = "private_secret_query_never_stored"
        response = self.search(request_body(query=marker))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(marker, response.text)
        self.assertEqual(before, {key: getattr(session, key) for key in keys})
        self.assertNotIn(marker, repr(vars(session)))
        self.assertEqual(response.headers["cache-control"].split(", ")[0], "no-store")

    def test_malformed_response_boundary_rejects_whole_payload(self):
        original = load_corpus().search(**request_body())
        mutations = (
            lambda p: p.update(schema_version=True),
            lambda p: p.update(advisory_only=1),
            lambda p: p.update(advisory_only=False),
            lambda p: p.update(operational_authority="FINANCIAL_ACTION"),
            lambda p: p.update(status="evidence_missing"),
            lambda p: p.update(private_query="private_secret_query"),
            lambda p: p.update(source="synthetic"),
            lambda p: p.update(source="paypal_sandbox"),
            lambda p: p["filters_applied"].update(jurisdiction="CA"),
            lambda p: p["filters_applied"].update(limit=2),
            lambda p: p["corpus_digests"].update(sources_sha256="0" * 64),
            lambda p: p["results"][0].update(url="javascript:alert(1)"),
            lambda p: p["results"][0].update(url="https://www.paypal.com.evil.invalid/us/legalhub/paypal/aup"),
            lambda p: p["results"][0].update(text_sha256="0" * 64),
            lambda p: p["results"][0].update(source_updated_date="2026-01-01"),
            lambda p: p["results"][0].update(case_stage="procedural_order"),
            lambda p: p["results"][0].update(jurisdiction="CA"),
            lambda p: p["results"][0].update(relevance_score=True),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                payload = deepcopy(original)
                mutate(payload)
                corpus = Mock()
                corpus.search.return_value = payload
                self.loader.side_effect = None
                self.loader.return_value = corpus
                response = self.search()
                self.assertEqual(response.status_code, 500, response.text)
                self.assertEqual(response.json()["error"]["code"], "response_contract_failure")
                self.assertNotIn("private_secret_query", response.text)


if __name__ == "__main__":
    unittest.main()
