"""(evloop) PayPal error reasons the seller can read: a closed, sanitised `paypal_issue` on provider failures.

Every provider reply is a synthetic MockTransport answer; no test opens a network connection or reads a credential.
Only the error `name` and up to 3 `details[].issue` codes matching ^[A-Z0-9_]{1,64}$ may reach a response; free
text, `message`, `description`, `field` and `value` never do.
"""

import json
import unittest

import httpx

from app.paypal import (PAYPAL_ISSUE_MAX, PaypalAdapter, PaypalConfig, PaypalProviderError, paypal_issue_from_body,
                        provider_error_extra)
from app.paypal_tools import _safe_error
from app.store import BoundaryError
from test_r25_backend import Clock, TwoDisputeHarness, no_network

DEBUG = "f00dbabe12345"
FREE_TEXT = "Synthetic private reason buyer@example.invalid"


def error_body(name="UNPROCESSABLE_ENTITY", issues=("INVALID_EVIDENCE_FILE",), **extra):
    """A PayPal-shaped error (Disputes error_422 schema) with free text in every place a leak could hide."""
    return {"name": name, "message": FREE_TEXT, "debug_id": DEBUG,
            "details": [{"issue": issue, "description": FREE_TEXT, "field": "/evidences/0", "value": FREE_TEXT,
                         "location": "body"} for issue in issues],
            "links": [{"href": "https://developer.paypal.com/private-link", "rel": "information_link"}], **extra}


class SanitiserTests(unittest.TestCase):
    def test_name_and_issue_codes_only(self):
        self.assertEqual(paypal_issue_from_body(json.dumps(error_body()).encode()),
                         {"name": "UNPROCESSABLE_ENTITY", "issues": ["INVALID_EVIDENCE_FILE"]})

    def test_free_text_lower_case_and_oversize_values_are_dropped(self):
        for bad in ("The requested action could not be performed", "invalid_evidence_file", "A" * 65, "",
                    "INVALID-EVIDENCE", "INVALID_EVIDENCE_FILE\n", " INVALID_EVIDENCE_FILE", 42, None, ["X"], {"X": 1}):
            body = json.dumps({"name": bad, "details": [{"issue": bad}, {"description": "MISSING_EVIDENCE_INFO"}]}).encode()
            self.assertIsNone(paypal_issue_from_body(body), repr(bad))
        mixed = error_body(name="Unprocessable entity.", issues=("free text issue", "A" * 65, "MISSING_EVIDENCE_INFO"))
        self.assertEqual(paypal_issue_from_body(json.dumps(mixed).encode()), {"name": None, "issues": ["MISSING_EVIDENCE_INFO"]})
        self.assertEqual(paypal_issue_from_body(json.dumps({"name": "A" * 64}).encode()), {"name": "A" * 64, "issues": []})

    def test_at_most_three_distinct_issues(self):
        issues = ("MISSING_EVIDENCE_INFO", "MISSING_EVIDENCE_INFO", "INVALID_EVIDENCE_FILE", "PERMISSION_DENIED",
                  "MISSING_TRACKING_INFO")
        projected = paypal_issue_from_body(json.dumps(error_body(issues=issues)).encode())
        self.assertEqual(PAYPAL_ISSUE_MAX, 3)
        self.assertEqual(projected["issues"], ["MISSING_EVIDENCE_INFO", "INVALID_EVIDENCE_FILE", "PERMISSION_DENIED"])

    def test_non_json_and_non_object_bodies_give_nothing(self):
        for body in (b"", b"not json", b"[]", b'"INVALID_REQUEST"', b'{"name": NaN}', b"\xff\xfe", b'{"details": "X"}',
                     b'{"details": [1, "X", null]}'):
            self.assertIsNone(paypal_issue_from_body(body), body)

    def test_extra_rechecks_and_only_for_provider_errors(self):
        self.assertEqual(provider_error_extra(BoundaryError(502, "provider_upstream_failure")), {})
        forged = PaypalProviderError(502, "provider_upstream_failure",
                                     paypal_issue={"name": FREE_TEXT, "issues": ["OK_CODE", FREE_TEXT, "B", "C", "D"]},
                                     paypal_debug_id="not a debug id!")
        self.assertEqual(provider_error_extra(forged), {"paypal_issue": {"name": None, "issues": ["OK_CODE", "B"]}})
        self.assertEqual(provider_error_extra(PaypalProviderError(502, "provider_upstream_failure",
                                                                  paypal_issue={"name": "X", "issues": [], "message": "x"})), {})

    def test_invoice_gateway_keeps_the_sanitised_reason(self):
        issue = {"name": "INVALID_REQUEST", "issues": ["INVALID_PARAMETER_VALUE"]}
        kept = _safe_error(PaypalProviderError(502, "provider_upstream_failure", paypal_issue=issue, paypal_debug_id=DEBUG))
        self.assertEqual((kept.status, kept.code, provider_error_extra(kept)),
                         (502, "provider_upstream_failure", {"paypal_issue": issue, "paypal_debug_id": DEBUG}))
        # Any other code on a provider error is still reduced to the generic failure with nothing attached.
        other = _safe_error(PaypalProviderError(502, FREE_TEXT, paypal_issue=issue))
        self.assertEqual((other.code, provider_error_extra(other)), ("provider_upstream_failure", {}))


class InvoiceAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_a_400_invoice_answer_raises_the_sanitised_reason(self):
        no_network(self)

        def handler(request):
            request.read()
            if request.url.path == "/v1/oauth2/token":
                return httpx.Response(200, json={"access_token": "synthetic-token", "token_type": "Bearer", "expires_in": 3600})
            return httpx.Response(400, headers={"PayPal-Debug-Id": DEBUG},
                                  json=error_body(name="INVALID_REQUEST", issues=("INVALID_PARAMETER_VALUE", "lower case")))

        adapter = PaypalAdapter(config_loader=lambda: PaypalConfig(True, "synthetic-id", "synthetic-secret"),
                                transport=httpx.MockTransport(handler), clock=Clock())
        await adapter.connect()
        with self.assertRaises(PaypalProviderError) as caught:
            await adapter.create_invoice_draft({"description": "Synthetic item", "amount": "10.00", "currency": "USD"},
                                               "synthetic-request-0001")
        self.assertEqual((caught.exception.status, caught.exception.code), (502, "provider_upstream_failure"))
        self.assertEqual(provider_error_extra(caught.exception),
                         {"paypal_issue": {"name": "INVALID_REQUEST", "issues": ["INVALID_PARAMETER_VALUE"]},
                          "paypal_debug_id": DEBUG})
        self.assertEqual(adapter.open_clients, 0)


class RouteTests(TwoDisputeHarness):
    """A mocked 422 on provide-evidence and on add-tracking reaches the route's error response sanitised."""

    def setUp(self):
        super().setUp()
        self.reply = None
        provider = self.app.state.paypal
        original = provider.transport.handler

        def handler(request):
            if request.method == "POST" and self.reply is not None and (
                    request.url.path.endswith("/provide-evidence") or request.url.path == "/v1/shipping/trackers-batch"):
                request.read()
                self.calls.append(request)
                return httpx.Response(422, headers={"PayPal-Debug-Id": DEBUG}, content=self.reply)
            return original(request)

        provider.transport = httpx.MockTransport(handler)

    def send(self, route):
        return self.post(route, {"dispute_id": "PP-D-SANDBOX01", "case_ref": "case-ref-001", "submit": True})

    def assert_clean(self, response):
        for marker in (FREE_TEXT, "Synthetic private", "example.invalid", "private-link", "description"):
            self.assertNotIn(marker, response.text)

    def test_provide_evidence_422_carries_name_and_issue(self):
        self.ready("case-ref-001")
        self.reply = json.dumps(error_body(issues=("INVALID_EVIDENCE_FILE", "free text", "B" * 65))).encode()
        failed = self.send("/paypal/disputes/provide-evidence")
        self.assertEqual(self.code(failed), (502, "provider_upstream_failure"))
        error = failed.json()["error"]
        self.assertEqual(set(error), {"code", "message", "paypal_issue", "paypal_debug_id"})
        self.assertEqual(error["paypal_issue"], {"name": "UNPROCESSABLE_ENTITY", "issues": ["INVALID_EVIDENCE_FILE"]})
        self.assertEqual(error["paypal_debug_id"], DEBUG)
        self.assert_clean(failed)
        self.assertEqual(len(self.posts("/provide-evidence")), 1)

    def test_add_tracking_422_carries_name_and_issue(self):
        self.ready("case-ref-001")
        self.reply = json.dumps(error_body(issues=("INPUT_VALIDATION_ERROR",))).encode()
        failed = self.send("/paypal/disputes/add-tracking")
        self.assertEqual(self.code(failed), (502, "provider_upstream_failure"))
        self.assertEqual(failed.json()["error"]["paypal_issue"], {"name": "UNPROCESSABLE_ENTITY", "issues": ["INPUT_VALIDATION_ERROR"]})
        self.assert_clean(failed)

    def test_free_text_or_oversize_values_leave_no_paypal_issue(self):
        self.ready("case-ref-001")
        self.reply = json.dumps({"name": "Unprocessable: " + FREE_TEXT, "message": FREE_TEXT,
                                 "details": [{"issue": "C" * 65, "description": FREE_TEXT},
                                             {"issue": "not a code", "description": FREE_TEXT}]}).encode()
        failed = self.send("/paypal/disputes/provide-evidence")
        self.assertEqual(self.code(failed), (502, "provider_upstream_failure"))
        self.assertNotIn("paypal_issue", failed.json()["error"])
        self.assertEqual(failed.json()["error"]["paypal_debug_id"], DEBUG)
        self.assert_clean(failed)
        self.assertNotIn("C" * 65, failed.text)

    def test_a_non_json_failure_keeps_the_fixed_code_only(self):
        self.ready("case-ref-001")
        self.reply = ("<html>" + FREE_TEXT + "</html>").encode()
        failed = self.send("/paypal/disputes/add-tracking")
        self.assertEqual(self.code(failed), (502, "provider_upstream_failure"))
        self.assertEqual(set(failed.json()["error"]), {"code", "message", "paypal_debug_id"})
        self.assert_clean(failed)


if __name__ == "__main__":
    unittest.main()
