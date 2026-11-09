"""Strict-Transport-Security: sent on the hosted public app only; never on local mode or a non-proxied request."""

import os
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app.main import create_app

PUBLIC = "payguard-demo.onrender.com"
PROXY = {"X-Forwarded-For": "198.51.100.7", "X-Forwarded-Proto": "https"}
HSTS = "max-age=31536000"


def env(**values):
    base = {key: value for key, value in os.environ.items() if not key.startswith(("PAYGUARD_DEMO", "PAYGUARD_PUBLIC", "PAYGUARD_HOSTED"))}
    base.update(values)
    return mock.patch.dict(os.environ, base, clear=True)


class HstsHeaderTests(unittest.TestCase):
    def hosted_get(self, path="/api/v1/paypal/status"):
        with env(PAYGUARD_DEMO_MODE="public", PAYGUARD_PUBLIC_HOST=PUBLIC):
            client = TestClient(create_app(), base_url="https://" + PUBLIC)
            return client.get(path, headers=PROXY)

    def test_hosted_response_carries_exact_hsts_value(self):
        response = self.hosted_get()
        self.assertEqual(response.headers.get("strict-transport-security"), HSTS)
        value = response.headers["strict-transport-security"].lower()
        self.assertNotIn("includesubdomains", value)
        self.assertNotIn("preload", value)

    def test_hosted_error_response_also_carries_it(self):
        # A 401 (no session) and a 404 both pass the same send wrapper.
        self.assertEqual(self.hosted_get("/api/v1/paypal/status").headers.get("strict-transport-security"), HSTS)
        self.assertEqual(self.hosted_get("/nope").headers.get("strict-transport-security"), HSTS)

    def test_local_mode_has_no_hsts(self):
        with env():
            client = TestClient(create_app(), base_url="http://127.0.0.1:8000")
            response = client.get("/api/v1/paypal/status")
        self.assertIsNone(response.headers.get("strict-transport-security"))
        self.assertEqual(response.headers.get("x-content-type-options"), "nosniff")

    def test_hosted_app_without_proxy_headers_is_refused_and_has_no_hsts(self):
        with env(PAYGUARD_DEMO_MODE="public", PAYGUARD_PUBLIC_HOST=PUBLIC):
            client = TestClient(create_app(), base_url="https://" + PUBLIC)
            response = client.get("/api/v1/paypal/status")
        self.assertGreaterEqual(response.status_code, 400)
        self.assertIsNone(response.headers.get("strict-transport-security"))


if __name__ == "__main__":
    unittest.main()
