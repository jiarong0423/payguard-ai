import json
import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src"), str(ROOT / "backend")]

import export_api_docs  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from app.main import create_app  # noqa: E402
from app.paypal import PaypalAdapter, PaypalConfig  # noqa: E402

API = ROOT / "docs" / "api"
BASE = "http://127.0.0.1:8000"
SESSION = "POST /api/v1/demo/sessions"
SECRET_WORDS = ("authorization", "bearer", "client_secret", "api_key", "apikey", "password", "private_key", "access_token", "begin rsa")
SECRET_SHAPES = (re.compile(r"AIza[0-9A-Za-z_-]{20,}"), re.compile(r"\bsk-[A-Za-z0-9]{16,}"), re.compile(r"\bEA[A-Za-z0-9_-]{30,}"),
                 re.compile(r"(?<![A-Za-z0-9/_.-])(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*[a-z])[A-Za-z0-9_-]{40,}(?![A-Za-z0-9/_.-])"))


def load(name):
    return json.loads((API / name).read_text(encoding="utf-8"))


def replay(collection, expectations):
    """Run a collection against the application in-process, the way Newman would: apply the collection-level
    pre-request rules (Origin, session headers), substitute variables, store captured values, return a result per item."""
    scrubbed = {key: value for key, value in os.environ.items() if key in ("PATH", "HOME", "TMPDIR", "LANG")}
    results = []
    with patch.dict(os.environ, scrubbed, clear=True):
        provider = PaypalAdapter(config_loader=lambda: PaypalConfig())
        client = TestClient(create_app(paypal=provider), base_url=BASE, client=("127.0.0.1", 55021), raise_server_exceptions=False)
        variables = {}
        with client:
            for item in collection["item"]:
                request = item["request"]
                path = request["url"]["raw"].replace("{{baseUrl}}", "")
                for entry in request["url"].get("variable", []):
                    path = path.replace(":" + entry["key"], entry["value"])
                headers = {"Content-Type": "application/json", "Origin": BASE}
                is_session = request["method"] == "POST" and path == "/api/v1/demo/sessions"
                if not is_session and variables.get("sessionId"):
                    headers["X-Demo-Session"] = variables["sessionId"]
                if not is_session and variables.get("csrfToken") and request["method"] != "GET":
                    headers["X-CSRF-Token"] = variables["csrfToken"]
                content = None
                if "body" in request:
                    content = request["body"]["raw"]
                    for key, value in variables.items():
                        content = content.replace("{{%s}}" % key, value)
                    assert "{{" not in content, (item["name"], "unresolved variable")
                response = client.request(request["method"], path, content=content, headers=headers)
                body = response.json()
                if is_session:
                    variables.update(sessionId=body["session_id"], csrfToken=body["csrf_token"])
                for var, key in expectations.get(item["name"], {}).get("captures", {}).items():
                    variables[var] = body[key]
                results.append((item, response.status_code, body))
        assert provider.open_clients == 0
    return results


class ApiDocsTests(unittest.TestCase):
    def test_committed_files_match_the_application(self):
        self.assertEqual(export_api_docs.main(["--check"]), 0, "run tools/export_api_docs.py and commit docs/api")

    def test_openapi_and_collection_are_consistent(self):
        spec = json.loads((ROOT / "docs" / "api" / "openapi.json").read_text(encoding="utf-8"))
        collection = json.loads((ROOT / "docs" / "api" / "postman_collection.json").read_text(encoding="utf-8"))
        self.assertTrue(spec["openapi"].startswith("3."))
        operations = sum(len(methods) for methods in spec["paths"].values())
        self.assertEqual(len(collection["item"]), operations)
        self.assertEqual(collection["variable"], [{"key": "baseUrl", "value": "http://127.0.0.1:8000"}])
        text = json.dumps(spec) + json.dumps(collection)
        self.assertNotIn("/" + "Users/", text)

    def test_security_schemes_match_the_sessions_the_application_requires(self):
        spec = load("openapi.json")
        schemes = spec["components"]["securitySchemes"]
        self.assertEqual({k: (v["type"], v["in"], v["name"]) for k, v in schemes.items()},
                         {"DemoSession": ("apiKey", "header", "X-Demo-Session"), "DemoCsrf": ("apiKey", "header", "X-CSRF-Token")})
        for path, methods in spec["paths"].items():
            for method, operation in methods.items():
                if path in ("/api/v1/health", "/api/v1/demo/sessions"):
                    self.assertEqual(operation["security"], [], (method, path))
                elif method == "post":
                    self.assertEqual(operation["security"], [{"DemoSession": [], "DemoCsrf": []}], (method, path))
                else:
                    self.assertEqual(operation["security"], [{"DemoSession": []}], (method, path))
        pre = "\n".join(next(e for e in load("postman_collection.json")["event"] if e["listen"] == "prerequest")["script"]["exec"])
        for scheme in schemes.values():
            self.assertIn(scheme["name"], pre)

    def test_every_example_is_valid_for_its_schema_and_privacy_safe(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed")
        spec = load("openapi.json")

        def resolve(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    return resolve(spec["components"]["schemas"][node["$ref"].rsplit("/", 1)[-1]])
                return {k: resolve(v) for k, v in node.items()}
            return [resolve(v) for v in node] if isinstance(node, list) else node
        checked = 0
        for path, methods in spec["paths"].items():
            for method, operation in methods.items():
                self.assertTrue(operation.get("requestBody", {"description": "x"}).get("description"), (method, path))
                for parameter in operation.get("parameters", []):
                    self.assertIn("example", parameter, (method, path, parameter["name"]))
                    jsonschema.validate(parameter["example"], resolve(parameter["schema"]))
                media = list(operation.get("requestBody", {}).get("content", {}).values())
                media += [m for r in operation["responses"].values() for m in r.get("content", {}).values()]
                for item in media:
                    if "example" in item and item.get("schema"):
                        jsonschema.Draft202012Validator(resolve(item["schema"])).validate(item["example"])
                        text = json.dumps(item["example"])
                        self.assertNotRegex(text, r"[0-9a-fA-F]{32,}")
                        self.assertNotIn("@", text)
                        checked += 1
        self.assertGreater(checked, 150)

    def test_the_collection_carries_no_credentials(self):
        collection = (ROOT / "docs" / "api" / "postman_collection.json").read_text(encoding="utf-8").lower()
        for word in ("authorization", "bearer", "client_secret", "api_key"):
            self.assertNotIn(word, collection)

    def test_every_request_has_a_test_script_and_the_session_comes_first(self):
        for name in ("postman_collection.json", "postman_run_collection.json"):
            collection = load(name)
            self.assertEqual(collection["variable"], [{"key": "baseUrl", "value": BASE}], name)
            first = collection["item"][0]["request"]
            self.assertEqual(first["method"] + " " + first["url"]["raw"].replace("{{baseUrl}}", ""), SESSION, name)
            self.assertEqual(len({item["name"] for item in collection["item"]}), len(collection["item"]), name)
            pre = [event for event in collection["event"] if event["listen"] == "prerequest"]
            self.assertEqual(len(pre), 1, name)
            script = "\n".join(pre[0]["script"]["exec"])
            for needle in ("'Origin'", "X-Demo-Session", "X-CSRF-Token", "sessionId", "csrfToken", "baseUrl"):
                self.assertIn(needle, script, name)
            session_test = "\n".join(collection["item"][0]["event"][0]["script"]["exec"])
            self.assertIn("collectionVariables.set('sessionId'", session_test)
            self.assertIn("collectionVariables.set('csrfToken'", session_test)
            for item in collection["item"]:
                tests = [event for event in item["event"] if event["listen"] == "test"]
                self.assertEqual(len(tests), 1, item["name"])
                self.assertIn("pm.test(", "\n".join(tests[0]["script"]["exec"]), item["name"])

    def test_collections_carry_no_secret_looking_strings(self):
        for name in ("postman_collection.json", "postman_run_collection.json"):
            # The advisory candidate legitimately carries the closed value REFERENCE_ONLY_NO_ACTION_AUTHORIZATION; nothing else may match.
            text = (API / name).read_text(encoding="utf-8").replace("REFERENCE_ONLY_NO_ACTION_AUTHORIZATION", "REFERENCE_ONLY")
            lowered = text.lower()
            for word in SECRET_WORDS:
                self.assertNotIn(word, lowered, (name, word))
            for shape in SECRET_SHAPES:
                self.assertIsNone(shape.search(text), (name, shape.pattern))
            self.assertNotIn("/" + "Users/", text)

    def test_the_full_collection_keeps_path_variables_and_marks_provider_routes(self):
        collection = load("postman_collection.json")
        by_name = {item["name"]: item for item in collection["item"]}
        approve = by_name["POST /api/v1/disputes/{case_ref}/approve"]["request"]
        self.assertEqual(approve["url"]["raw"], "{{baseUrl}}/api/v1/disputes/:case_ref/approve")
        self.assertEqual(approve["url"]["variable"], [{"key": "case_ref", "value": "case-ref-001"}])
        for name in ("POST /api/v1/paypal/connect", "POST /api/v1/ai/evidence-brief", "POST /api/v1/studio/agent-turn"):
            self.assertIn("not in postman_run_collection.json", by_name[name]["request"]["description"], name)

    def test_the_run_collection_is_safe_and_the_right_size(self):
        collection = load("postman_run_collection.json")
        items = collection["item"]
        self.assertTrue(20 <= len(items) <= 25, len(items))
        self.assertEqual(len(items), len(export_api_docs.RUN_REQUESTS))
        for item in items:
            path = item["request"]["url"]["raw"].replace("{{baseUrl}}", "")
            self.assertFalse(path.startswith(export_api_docs.PROVIDER_PATHS), "provider route in the run collection: " + path)
        negatives = [item for item in items if "(negative case)" in item["name"]]
        self.assertEqual(len(negatives), sum(1 for spec in export_api_docs.RUN_REQUESTS if spec.get("negative")))
        self.assertGreaterEqual(len(negatives), 3)
        for item in negatives:
            self.assertIn("Negative case:", item["request"]["description"])
        assertions = sum("pm.test(" in line for item in items for event in item["event"] for line in event["script"]["exec"])
        self.assertGreaterEqual(assertions, 2 * len(items) - 2)

    def test_run_collection_bodies_match_the_application(self):
        """Replay every request in-process (default demo mode, keys scrubbed): each answers the status the collection
        documents, the Newman assertions hold, and the status written into the collection's own script agrees."""
        collection = load("postman_run_collection.json")
        specs = {spec["name"]: spec for spec in export_api_docs.RUN_REQUESTS}
        results = replay(collection, specs)
        self.assertEqual(len(results), len(collection["item"]))
        for item, status, body in results:
            spec = specs[item["name"]]
            self.assertEqual(status, spec["expect"], (item["name"], body))
            script = "\n".join(item["event"][0]["script"]["exec"])
            self.assertIn("have.status(%d)" % spec["expect"], script, item["name"])
            if spec.get("negative"):
                self.assertGreaterEqual(status, 400, item["name"])
                self.assertIn("error", body)
            else:
                self.assertLess(status, 400, item["name"])
            for path, expected in spec.get("checks", []):
                node = body
                for part in path.split("."):
                    node = node[part]
                self.assertEqual(node, expected, (item["name"], path))
        self.assertEqual(results[0][0]["name"], "01 Create demo session")

    def test_full_collection_skeletons_answer_a_documented_status(self):
        """Every request of the generated collection, sent with its empty skeleton and no key, ends in a documented
        status with a JSON body and no server error. No provider is called: the adapter is unconfigured."""
        collection = load("postman_collection.json")
        results = replay(collection, {})
        self.assertEqual(len(results), len(collection["item"]))
        for item, status, body in results:
            self.assertIn(status, export_api_docs.ALLOWED_CODES, (item["name"], status, body))
        statuses = {item["name"]: status for item, status, _body in results}
        self.assertEqual(statuses[SESSION], 201)
        self.assertEqual(statuses["GET /api/v1/health"], 200)

    def test_generated_files_are_deterministic(self):
        first = {name: json.dumps(value, sort_keys=True) for name, value in export_api_docs.build().items()}
        second = {name: json.dumps(value, sort_keys=True) for name, value in export_api_docs.build().items()}
        self.assertEqual(first, second)
        self.assertEqual(set(first), {"openapi.json", "postman_collection.json", "postman_run_collection.json"})


if __name__ == "__main__":
    unittest.main()
