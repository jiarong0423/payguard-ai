"""Offline tests for Gemini worker generated-text inventory enforcement."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import socket
import sys
import tomllib
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch


CLAUDE_C1_PARAPHRASES = (
    "PayPal has cleared this activity.",
    "Seller Protection applies to this case.",
    "The seller is protected under Seller Protection.",
    "The listing is allowed under PayPal policy.",
    "This activity does not violate the AUP.",
    "The hold will be lifted soon.",
    "Your account is safe from limitation.",
    "Expect funds to be available within 21 days.",
    "The buyer will receive a full refund.",
    "The chargeback will be reversed in the seller's favor.",
    "The issuer will rule for the seller.",
    "The dispute outcome favors the merchant.",
    "We found no evidence of fraud.",
    "Fraud risk is low.",
    "AML screening passed.",
    "The merchant passed AML screening.",
)


def load_worker_module():
    google = ModuleType("google")
    google.__path__ = []
    google_auth = ModuleType("google.auth")
    google_auth.default = lambda **_kwargs: (None, None)
    google_genai = ModuleType("google.genai")
    google_genai.Client = object
    google_genai_types = ModuleType("google.genai.types")
    google_genai.types = google_genai_types
    google.auth = google_auth
    google.genai = google_genai
    modules = {
        "google": google,
        "google.auth": google_auth,
        "google.genai": google_genai,
        "google.genai.types": google_genai_types,
    }
    path = Path(__file__).resolve().parents[1] / "integrations/gemini/worker.py"
    spec = importlib.util.spec_from_file_location("_payguard_test_gemini_worker", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("worker_spec_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


worker = load_worker_module()


def load_runtime_guard():
    path = Path(__file__).resolve().parents[1] / "integrations/gemini/check_runtime.py"
    spec = importlib.util.spec_from_file_location("_payguard_test_gemini_runtime_guard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("runtime_guard_spec_unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime_guard = load_runtime_guard()


def generated(stage="dispute_mediation"):
    inventory = worker.GENERATED_TEXT_INVENTORY[stage]
    context, _context_digest, _corpus_digest = worker.build_fixed_context(stage)
    return {
        "summary": inventory["summary"][0],
        "evidence_points": [inventory["evidence_points"][0]],
        "missing_evidence": [inventory["missing_evidence"][0]],
        "citation_ids": list(context["citation_ids"]),
    }


def provider_response(document):
    part = SimpleNamespace(
        text=worker.canonical_json(document).decode("utf-8"),
        thought=None,
    )
    content = SimpleNamespace(role="model", parts=[part])
    candidate = SimpleNamespace(content=content, finish_reason="STOP")
    return SimpleNamespace(
        automatic_function_calling_history=None,
        candidates=[candidate],
        model_version=worker.MODEL,
        prompt_feedback=None,
        response_id="synthetic-response-1",
    )


class GeminiWorkerInventoryTests(unittest.TestCase):
    def setUp(self):
        for guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
            patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden")),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def assert_inventory_rejected(self, document, stage="dispute_mediation"):
        context, _context_digest, _corpus_digest = worker.build_fixed_context(stage)
        with self.assertRaises(worker.ResponseValidationError) as caught:
            worker._extract_response(provider_response(document), context)
        self.assertEqual(
            caught.exception.subcode,
            worker.ValidationSubcode.RESPONSE_TEXT_INVENTORY_INVALID,
        )
        self.assertEqual(caught.exception.code, "ai_response_invalid")

    def test_worker_accepts_exact_stage_bound_inventory(self):
        for stage, inventory in worker.GENERATED_TEXT_INVENTORY.items():
            document = generated(stage)
            document.update(
                summary=inventory["summary"][-1],
                evidence_points=list(inventory["evidence_points"]),
                missing_evidence=list(inventory["missing_evidence"]),
            )
            context, _context_digest, _corpus_digest = worker.build_fixed_context(stage)
            with self.subTest(stage=stage):
                brief, metadata = worker._extract_response(provider_response(document), context)
                self.assertEqual(brief.model_dump(), document)
                self.assertEqual(metadata.model_version, worker.MODEL)

    def test_worker_rejects_all_claude_c1_paraphrases(self):
        for claim in CLAUDE_C1_PARAPHRASES:
            document = generated()
            document["summary"] = claim
            with self.subTest(claim=claim):
                self.assert_inventory_rejected(document)

    def test_profile_manifest_and_source_markers_match_current_project(self):
        project_root = Path(__file__).resolve().parents[1]
        profile_root = project_root / "integrations/gemini"
        manifest = tomllib.loads((profile_root / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["tool"]["payguard-gemini"]["project-markers"],
            runtime_guard.PROJECT_MARKERS,
        )
        self.assertEqual(
            set(runtime_guard.PROJECT_MARKERS),
            {
                "backend/app/ai_brief.py",
                "backend/app/main.py",
                "backend/app/store.py",
                "integrations/gemini/run.sh",
                "integrations/gemini/worker.py",
            },
        )
        self.assertEqual(
            runtime_guard.validate_project(profile_root),
            project_root,
        )

    def test_worker_rejects_cross_stage_cross_field_and_mutated_text(self):
        dispute = worker.GENERATED_TEXT_INVENTORY["dispute_mediation"]
        source = worker.GENERATED_TEXT_INVENTORY["source_compliance"]
        cross_stage = generated()
        cross_stage["summary"] = source["summary"][0]
        cross_field = generated()
        cross_field["summary"] = dispute["evidence_points"][0]
        mutated = generated()
        mutated["summary"] = dispute["summary"][0] + " "
        for case, document in (
            ("cross_stage", cross_stage),
            ("cross_field", cross_field),
            ("mutated", mutated),
        ):
            with self.subTest(case=case):
                self.assert_inventory_rejected(document)


if __name__ == "__main__":
    unittest.main()
