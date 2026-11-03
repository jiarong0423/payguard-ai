"""The API serves the built console from its own origin without changing any API answer."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient

from app.main import create_app

ORIGIN = "http://127.0.0.1:8000"


class ConsoleStaticTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "index.html").write_text("<!doctype html><title>console</title>", encoding="utf-8")
        (root / "assets").mkdir()
        (root / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
        (root / "manifest.webmanifest").write_text('{"name": "PayGuard", "start_url": "/"}', encoding="utf-8")
        (root / "sw.js").write_text("self.addEventListener('fetch', () => {});", encoding="utf-8")
        (root / "offline.html").write_text("<!doctype html><title>offline</title>", encoding="utf-8")
        self.env = mock.patch.dict(os.environ, {"PAYGUARD_STATIC_DIR": self.tmp.name})
        self.env.start()
        self.client = TestClient(create_app(), base_url=ORIGIN, client=("127.0.0.1", 55003), raise_server_exceptions=False)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_index_and_assets_are_served_for_get(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("<title>console</title>", page.text)
        self.assertEqual(page.headers.get("cache-control"), "no-store")
        self.assertEqual(self.client.get("/assets/app.js").status_code, 200)
        self.assertEqual(self.client.head("/").status_code, 200)

    def test_pages_cannot_be_framed(self):
        # Red team r20 D5: no other site may frame a console page; 'self' keeps the scenarios page's same-origin
        # licence frame of /dashboard.html working. The existing headers stay.
        (Path(self.tmp.name) / "dashboard.html").write_text("<!doctype html><title>dashboard</title>", encoding="utf-8")
        for path in ("/", "/index.html", "/dashboard.html", "/offline.html", "/sw.js", "/api/v1/health"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertEqual(response.headers.get("content-security-policy"), "frame-ancestors 'self'", path)
            self.assertEqual(response.headers.get("x-frame-options"), "SAMEORIGIN", path)
            self.assertEqual((response.headers.get("cache-control"), response.headers.get("x-content-type-options"),
                              response.headers.get("referrer-policy")), ("no-store", "nosniff", "no-referrer"), path)
        self.assertEqual(self.client.head("/").headers.get("x-frame-options"), "SAMEORIGIN")

    def test_hosted_demo_pages_cannot_be_framed(self):
        with mock.patch.dict(os.environ, {"PAYGUARD_DEMO_MODE": "public", "PAYGUARD_PUBLIC_HOST": "demo.example.com"}):
            client = TestClient(create_app(), base_url="https://demo.example.com", client=("10.0.0.5", 55005),
                                raise_server_exceptions=False)
        page = client.get("/", headers={"X-Forwarded-For": "203.0.113.9", "X-Forwarded-Proto": "https"})
        self.assertEqual(page.status_code, 200, page.text)
        self.assertEqual(page.headers.get("content-security-policy"), "frame-ancestors 'self'")
        self.assertEqual(page.headers.get("x-frame-options"), "SAMEORIGIN")

    def test_api_answers_do_not_change(self):
        self.assertEqual(self.client.get("/api/v1/health").status_code, 200)
        missing = self.client.get("/api/v1/does-not-exist")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing.json()["error"]["code"], "route_unavailable")
        self.assertEqual(self.client.get("/api/v1/paypal/connect").status_code, 405)
        self.assertEqual(self.client.post("/api/v1/paypal/payments", json={}, headers={"Origin": ORIGIN}).status_code, 404)

    def test_non_get_on_page_paths_is_not_served(self):
        self.assertEqual(self.client.post("/", json={}, headers={"Origin": ORIGIN}).status_code, 404)
        self.assertEqual(self.client.post("/index.html", json={}, headers={"Origin": ORIGIN}).status_code, 404)

    def test_pwa_files_have_correct_content_types(self):
        manifest = self.client.get("/manifest.webmanifest")
        self.assertEqual(manifest.status_code, 200)
        self.assertEqual(manifest.headers["content-type"], "application/manifest+json")
        self.assertEqual(manifest.json()["start_url"], "/")
        worker = self.client.get("/sw.js?v=index-abc123")
        self.assertEqual(worker.status_code, 200)
        self.assertEqual(worker.headers["content-type"], "text/javascript; charset=utf-8")
        self.assertEqual(worker.headers["x-content-type-options"], "nosniff")
        self.assertEqual(worker.headers["cache-control"], "no-store")
        self.assertEqual(self.client.head("/sw.js").headers["content-type"], "text/javascript; charset=utf-8")
        self.assertTrue(self.client.get("/offline.html").headers["content-type"].startswith("text/html"))

    def test_content_types_do_not_depend_on_host_mimetypes(self):
        # Some hosts (Windows registry) map .js to text/plain; nosniff would then block the worker.
        with mock.patch("starlette.responses.guess_type", return_value=("text/plain", None)):
            self.assertEqual(self.client.get("/sw.js").headers["content-type"], "text/javascript; charset=utf-8")
            self.assertEqual(self.client.get("/assets/app.js").headers["content-type"], "text/javascript; charset=utf-8")
            self.assertEqual(self.client.get("/manifest.webmanifest").headers["content-type"], "application/manifest+json")

    def test_missing_pwa_file_is_still_not_found(self):
        missing = self.client.get("/missing-worker.js")
        self.assertEqual(missing.status_code, 404)
        self.assertNotEqual(missing.headers.get("content-type"), "text/javascript; charset=utf-8")
        self.assertEqual(self.client.get("/api/v1/sw.js").status_code, 404)

    def test_missing_build_leaves_api_only(self):
        with mock.patch.dict(os.environ, {"PAYGUARD_STATIC_DIR": os.path.join(self.tmp.name, "absent")}):
            client = TestClient(create_app(), base_url=ORIGIN, client=("127.0.0.1", 55004), raise_server_exceptions=False)
        self.assertEqual(client.get("/").status_code, 404)
        self.assertEqual(client.get("/api/v1/health").status_code, 200)


if __name__ == "__main__":
    unittest.main()
