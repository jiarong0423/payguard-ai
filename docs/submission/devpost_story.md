# PayGuard AI — Submitted Devpost Story

Status: the Devpost project is submitted. This is the current public story, read back after saving the evidence-gap wording.

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
3. **After a dispute — evidence preparation.** A case-specific checklist identifies requested seller items. PayGuard builds a pseudonymized, integrity-checked **Internal Review ZIP** and can request an optional bounded Gemini evidence brief. A person reviews the package; it is not a PayPal submission attachment and nothing is sent automatically.

## How I built it

The working stack is PayPal Sandbox REST APIs and OAuth, FastAPI, deterministic US policy-reference rules, React, Tailwind, AG Grid Community, and optional bounded Gemini on Vertex AI. Rules run before AI. The AI path receives fixed synthetic facts and pinned citation identities, produces advisory text, and has no tool authority to change a rule, send an invoice, submit evidence, or decide a dispute. The public repository includes an MIT license, a runnable local setup path, tests, a visual architecture map, and the source for all three stages.

## Challenge and learning

The hardest design choice was joining three moments in a merchant's workflow without implying that an AI system can replace provider review. I separated deterministic signals, evidence inspection, optional semantic summarization, and human action. The result is a coherent merchant-side workflow rather than an automated verdict engine.

## Scope and access

This is a **US-only, synthetic-data Sandbox demo**. PayPal decides applicable internal policy and dispute matters; a bank or card issuer decides an external dispute. PayGuard does not approve compliance, prevent an account restriction, handle real customer records, or claim production readiness. Judges can run the build using the [public repository and quickstart](https://github.com/jiarong0423/payguard-ai); no hosted demo is claimed. The [2:02 demonstration](https://youtu.be/K28N9QhRp1E) shows the merchant workflow.
