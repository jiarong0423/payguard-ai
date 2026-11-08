import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src"), str(ROOT / "backend")]

import export_api_docs  # noqa: E402


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

    def test_the_collection_carries_no_credentials(self):
        collection = (ROOT / "docs" / "api" / "postman_collection.json").read_text(encoding="utf-8").lower()
        for word in ("authorization", "bearer", "client_secret", "api_key"):
            self.assertNotIn(word, collection)


if __name__ == "__main__":
    unittest.main()
