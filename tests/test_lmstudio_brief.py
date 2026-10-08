"""Offline contract tests for the default-off LM Studio adapter."""

import asyncio
from copy import deepcopy
import unittest

from pydantic import ValidationError

from app import ai_brief as ai
from app import lmstudio_brief as local


STAGES = ("source_compliance", "velocity_guard", "dispute_mediation")


def generated(stage):
    citations = {
        "source_compliance": ["PP-US-AUP-POLICY"],
        "velocity_guard": ["PP-US-UA-VELOCITY"],
        "dispute_mediation": ["PP-REASONS-INR", "PP-EVIDENCE-TRACKING"],
    }
    inventory = ai.GENERATED_TEXT_INVENTORY[stage]
    return {
        "summary": inventory["summary"][0],
        "evidence_points": [inventory["evidence_points"][0]],
        "missing_evidence": [inventory["missing_evidence"][0]],
        "citation_ids": citations[stage],
    }


def provider_response(stage, *, model=local.MODEL, message_extra=None, choice_extra=None):
    message = {"role": "assistant", "content": ai.canonical_json(generated(stage)).decode("utf-8")}
    message.update(message_extra or {})
    choice = {"index": 0, "message": message, "finish_reason": "stop"}
    choice.update(choice_extra or {})
    return ai.canonical_json({"id": "local-test", "model": model, "choices": [choice]})


class LmStudioBriefTests(unittest.IsolatedAsyncioTestCase):
    async def test_default_is_disabled(self):
        adapter = local.LmStudioEvidenceBriefAdapter()
        with self.assertRaises(ai.AiBriefError) as caught:
            await adapter.generate({"stage": "source_compliance"})
        self.assertEqual((caught.exception.status, caught.exception.code), (503, "ai_disabled"))

    async def test_three_fixed_stages_return_local_evidence(self):
        calls = []

        async def transport(request):
            calls.append(deepcopy(request))
            context = ai.strict_json(request["messages"][1]["content"].encode("utf-8"))
            return provider_response(context["stage"])

        adapter = local.LmStudioEvidenceBriefAdapter(
            config=local.LmStudioConfig(enabled=True),
            transport=transport,
        )
        for stage in STAGES:
            result = await adapter.generate({"stage": stage})
            self.assertEqual(result["stage"], stage)
            self.assertEqual(result["model"], local.MODEL)
            self.assertEqual(result["execution_evidence"], "LOCAL_RUNTIME_RESPONSE")
            self.assertEqual(result["compliance_decision"], "NOT_MADE")
            self.assertFalse(result["external_action_authorized"])
        self.assertEqual(len(calls), 3)
        for request in calls:
            self.assertEqual(request["model"], local.MODEL)
            self.assertEqual(request["temperature"], 0)
            self.assertEqual(request["reasoning_effort"], "none")
            self.assertEqual(request["tools"], [])
            self.assertEqual(request["tool_choice"], "none")
            self.assertFalse(request["stream"])
            self.assertEqual(request["messages"][0], {"role": "system", "content": ai.INSTRUCTIONS})
            self.assertEqual(
                request["response_format"]["json_schema"]["schema"]["additionalProperties"],
                False,
            )
            for field_name in ("evidence_points", "missing_evidence"):
                self.assertEqual(
                    request["response_format"]["json_schema"]["schema"]["properties"][field_name]["maxItems"],
                    1,
                )

    async def test_model_reasoning_tool_and_contract_drift_fail_closed(self):
        cases = (
            provider_response("source_compliance", model="gemini-3.8-flash"),
            provider_response("source_compliance", message_extra={"reasoning_content": "hidden"}),
            provider_response("source_compliance", message_extra={"tool_calls": [{"type": "function"}]}),
            provider_response("source_compliance", choice_extra={"finish_reason": "length"}),
            ai.canonical_json({"model": local.MODEL, "choices": []}),
        )
        for raw in cases:
            with self.subTest(raw=raw[:80]):
                async def transport(_request, value=raw):
                    return value

                adapter = local.LmStudioEvidenceBriefAdapter(
                    config=local.LmStudioConfig(enabled=True),
                    transport=transport,
                )
                with self.assertRaises(ai.AiBriefError) as caught:
                    await adapter.generate({"stage": "source_compliance"})
                self.assertEqual(caught.exception.code, "ai_response_invalid")

    async def test_inactive_provider_reasoning_and_tool_placeholders_are_allowed(self):
        async def transport(_request):
            return provider_response(
                "source_compliance",
                message_extra={"reasoning_content": None, "tool_calls": []},
            )

        adapter = local.LmStudioEvidenceBriefAdapter(
            config=local.LmStudioConfig(enabled=True),
            transport=transport,
        )
        result = await adapter.generate({"stage": "source_compliance"})
        self.assertEqual(result["model"], local.MODEL)

    async def test_generated_text_and_citation_order_are_closed(self):
        wrong_text = generated("source_compliance")
        wrong_text["summary"] = "A plausible but unapproved sentence."
        wrong_citations = generated("dispute_mediation")
        wrong_citations["citation_ids"] = list(reversed(wrong_citations["citation_ids"]))
        documents = (wrong_text, wrong_citations)
        stages = ("source_compliance", "dispute_mediation")
        for stage, document in zip(stages, documents, strict=True):
            async def transport(_request, value=document):
                return ai.canonical_json({
                    "model": local.MODEL,
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": ai.canonical_json(value).decode("utf-8")},
                        "finish_reason": "stop",
                    }],
                })

            adapter = local.LmStudioEvidenceBriefAdapter(
                config=local.LmStudioConfig(enabled=True),
                transport=transport,
            )
            with self.assertRaises(ai.AiBriefError):
                await adapter.generate({"stage": stage})

    async def test_local_model_gate_serializes_concurrent_stages(self):
        in_flight = 0
        maximum = 0
        calls = 0

        async def transport(request):
            nonlocal in_flight, maximum, calls
            calls += 1
            in_flight += 1
            maximum = max(maximum, in_flight)
            try:
                await asyncio.sleep(0.01)
                context = ai.strict_json(request["messages"][1]["content"].encode("utf-8"))
                return provider_response(context["stage"])
            finally:
                in_flight -= 1

        adapter = local.LmStudioEvidenceBriefAdapter(
            config=local.LmStudioConfig(enabled=True),
            transport=transport,
        )
        results = await asyncio.gather(*(adapter.generate({"stage": stage}) for stage in STAGES))
        self.assertEqual([result["stage"] for result in results], list(STAGES))
        self.assertEqual(calls, 3)
        self.assertEqual(maximum, 1)

    def test_model_and_evidence_pairs_are_not_interchangeable(self):
        context, context_digest, corpus_digest = ai.build_fixed_context("source_compliance")
        base = {
            "schema_version": "1.0",
            "status": "completed",
            "stage": "source_compliance",
            "fixture_id": "payguard-fixed-synthetic-brief-v1",
            "context_digest": context_digest,
            "corpus_digest": corpus_digest,
            "model": local.MODEL,
            "prompt_contract_id": ai.PROMPT_CONTRACT_ID,
            "prompt_contract_digest": ai.PROMPT_CONTRACT_DIGEST,
            "execution_evidence": "LOCAL_RUNTIME_RESPONSE",
            "brief": generated("source_compliance"),
            "ai_generated": True,
            "advisory_only": True,
            "human_review_required": True,
            "compliance_decision": "NOT_MADE",
            "current_policy_applicability": "NOT_ESTABLISHED",
            "external_action_authorized": False,
            "workflow_transition_authorized": False,
            "semantic_entailment": "NOT_EVALUATED",
            "limitations": list(ai.LIMITATIONS),
        }
        ai.AiBriefResponse.model_validate(base)
        for model, evidence in (
            ("gemini-3.8-flash", "LOCAL_RUNTIME_RESPONSE"),
            (local.MODEL, "OPERATOR_LIVE_RESPONSE"),
            (local.MODEL, "SYNTHETIC_TEST_RESPONSE"),
        ):
            with self.subTest(model=model, evidence=evidence):
                with self.assertRaises(ValidationError):
                    ai.AiBriefResponse.model_validate({**base, "model": model, "execution_evidence": evidence})

    def test_repeated_generated_points_fail_closed(self):
        repeated = generated("velocity_guard")
        repeated["evidence_points"] = [
            repeated["evidence_points"][0],
            repeated["evidence_points"][0],
        ]
        with self.assertRaises(ValidationError):
            ai.GeneratedBrief.model_validate(repeated)


if __name__ == "__main__":
    unittest.main()
