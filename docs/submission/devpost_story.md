# PayGuard AI — Submitted Devpost Story

Status: the Devpost project is submitted. Story text updated 2026-10-29 to match the repository (Disputes readback, stage auto-load, varied transaction amounts, 436 tests).

Project: PayGuard AI

Tagline: A merchant defense buffer for policy warnings, sales spikes, and dispute evidence.

Devpost: https://devpost.com/software/payguard-ai-zbsp9l

Repository: https://github.com/jiarong0423/payguard-ai

Video: https://youtu.be/K28N9QhRp1E (public, 2:02)

---

## Why I built PayGuard AI

A merchant may notice a policy warning, a sudden sales spike, or a dispute only after the records have become difficult to assemble. PayGuard AI is a **merchant defense buffer layer**: it helps the merchant identify evidence gaps early and prepare evidence, while keeping every decision with the merchant and the relevant payment provider.

## What it does

1. **Before an invoice draft — AUP preflight.** Deterministic checks compare a synthetic product description with pinned public PayPal US AUP references. The merchant can edit, cancel, or acknowledge the warning. Only after that review does the PayPal Sandbox path create one **unsent** invoice draft.
2. **During fulfillment — sales-velocity readiness.** A backend comparison flags a synthetic increase against a declared local baseline. **AG Grid Community** makes the transaction stream sortable and filterable, so a reviewer can select an order and inspect missing fulfillment records. This is a local preparation signal, not a PayPal risk score or account-hold prediction.
3. **After a dispute — evidence preparation.** The stage lists disputes through `GET /v1/customer/disputes` and `GET /v1/customer/disputes/{id}` (Sandbox when connected, otherwise a labelled fixture), a case-specific checklist identifies requested seller items, and PayGuard builds a pseudonymized, integrity-checked **Internal Review ZIP**, previews the multipart `provide-evidence` request and can request a Gemini evidence brief (Gemini selects each sentence from a closed, pre-approved inventory and fixed code validates the choice). A person reviews the package; the request is sent only after the local approval, with `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled` and a Sandbox connection.

## How I built it

The working stack is PayPal Sandbox REST APIs and OAuth, FastAPI, deterministic US policy-reference rules, React, Tailwind, AG Grid Community, and bounded Gemini on Vertex AI. Rules run before AI. The AI path receives fixed synthetic facts and pinned citation identities, produces advisory text, and has no tool authority to change a rule, send an invoice, submit evidence, or decide a dispute. The public repository includes an MIT license, a runnable local setup path, tests, a visual architecture map, and the source for all three stages.

## Challenge and learning

The hardest design choice was joining three moments in a merchant's workflow without implying that an AI system can replace provider review. I separated deterministic signals, evidence inspection, bounded semantic summarization, and human action. The result is a coherent merchant-side workflow rather than an automated verdict engine.

## Scope and access

This is a **US-only, synthetic-data Sandbox demo**. PayPal decides applicable internal policy and dispute matters; a bank or card issuer decides an external dispute. Scope: a fictitious US Business Sandbox seller with synthetic data; PayPal and card issuers keep the decisions. Judges run it locally in about five minutes (quickstart in the [public repository](https://github.com/jiarong0423/payguard-ai)); hosting was not part of this entry. Measured scope: `./tools/run.sh test` runs 436 tests (2 skipped); the Sandbox path has one operator-run receipt (2026-10-07, unsent USD 10.00 draft `INV2-2MTA-PRPQ-4CAJ-W5UW`) and the Disputes calls are covered by mocked-transport tests, not yet by a live Sandbox dispute. The [2:02 demonstration](https://youtu.be/K28N9QhRp1E) shows the merchant workflow.
