# PayGuard AI — Submitted Devpost Story

Project: PayGuard AI

Tagline: A merchant defense buffer for policy warnings, sales spikes, and dispute evidence.

Devpost: https://devpost.com/software/payguard-ai-zbsp9l

Repository: https://github.com/jiarong0423/payguard-ai

Video: https://youtu.be/K28N9QhRp1E (public, 2:02)

---

## Why I built PayGuard AI

A merchant may notice a policy warning, a sudden sales spike, or a dispute only after the records have become difficult to assemble. PayGuard AI is a **merchant defense buffer layer**: it helps the merchant identify evidence gaps early and prepare evidence, while keeping every decision with the merchant and the relevant payment provider.

**Why these three situations:** the stages follow published decisions of the UK Financial Ombudsman Service about PayPal accounts, checked against the published PDFs on 2026-10-31. [DRN-3621543](https://www.financial-ombudsman.org.uk/decision/DRN-3621543.pdf): an e-liquid seller could no longer receive payments because the goods needed PayPal's pre-approval under its Acceptable Use Policy (complaint not upheld). [DRN-5706769](https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf): a new business account with a sharp rise in sales had part of its funds held and a 15% rolling reserve applied (the reserve was found reasonable; GBP 150 was awarded for an unexplained delay in releasing funds). [DRN-3526295](https://www.financial-ombudsman.org.uk/decision/DRN-3526295.pdf): a buyer's Buyer Protection claim over a watch that did not match its description (upheld; this is the buyer's side, which PayGuard does not act for). These are UK decisions about PayPal's UK and European entities, not US cases, and three cases show a pattern, not an incidence rate. The author collected further public sources for the project; they are not included in this repository.

## What it does

1. **Before an invoice draft — AUP preflight.** Deterministic checks compare a synthetic product description with pinned public PayPal US AUP references. The merchant can edit, cancel, or acknowledge the warning. Only after that review does the PayPal Sandbox path create one **unsent** invoice draft.
2. **During fulfillment — sales-velocity readiness.** A backend comparison flags a synthetic increase against a declared local baseline. **AG Grid Community** makes the transaction stream sortable and filterable, so a reviewer can select an order and inspect missing fulfillment records. This is a local preparation signal, not a PayPal risk score or account-hold prediction.
3. **After a dispute — evidence preparation.** The stage lists disputes through `GET /v1/customer/disputes` and `GET /v1/customer/disputes/{id}` (Sandbox when connected, otherwise a labelled fixture), a case-specific checklist identifies requested seller items, and PayGuard builds a pseudonymized, integrity-checked **Internal Review ZIP**, previews the multipart `provide-evidence` request and can request a Gemini evidence brief (Gemini selects each sentence from a closed, pre-approved inventory and fixed code validates the choice). A person reviews the package; the request is sent only after the local approval, with `PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled` and a Sandbox connection.

## How I built it

The working stack is PayPal Sandbox REST APIs and OAuth, FastAPI, deterministic US policy-reference rules, React, Tailwind, AG Grid Community, and bounded Gemini on Vertex AI. Rules run before AI. The AI path receives fixed synthetic facts and pinned citation identities, produces advisory text, and has no tool authority to change a rule, send an invoice, submit evidence, or decide a dispute. The public repository includes an MIT license, a runnable local setup path, tests, a visual architecture map, and the source for all three stages.

## Challenge and learning

The hardest design choice was joining three moments in a merchant's workflow without implying that an AI system can replace provider review. I separated deterministic signals, evidence inspection, bounded semantic summarization, and human action. The result is a coherent merchant-side workflow rather than an automated verdict engine.

## Scope and access

This is a **US-only, synthetic-data Sandbox demo**. Scope: a fictitious US Business Sandbox seller with synthetic data. PayPal and card issuers make every decision; PayGuard prepares the merchant side. Judges run it locally in about five minutes (quickstart in the [public repository](https://github.com/jiarong0423/payguard-ai)). An optional hosted demo at https://payguard-demo-j2b3.onrender.com shows the synthetic stages in demo mode; its server makes no PayPal or live Channel3 call, and only its evidence guide can use Gemini when the operator opts in (free-tier key held as a Render secret, at most 5 calls a minute and 20 a day, guide only). The Sandbox steps, the AI brief and the Studio agents need the local run. Measured scope: `./tools/run.sh test` runs the automated Python tests and prints the count, and the frontend scripts (`node tests/frontend_*.mjs`) pass; the Sandbox path has receipts for an unsent invoice draft (2026-10-06 17:44 UTC, 2026-10-07 in UTC+8; draft `INV2-2MTA-PRPQ-4CAJ-W5UW`, and a second one on 2026-10-31), and on 2026-10-31 PayGuard listed one Sandbox test dispute that the author filed between two Sandbox test accounts (labelled Sandbox data; an earlier read 2.4 minutes after filing was empty, a read 12.7 minutes after filing listed it; it is not a real merchant case); on 2026-11-04 PayGuard sent evidence to one more author-created Sandbox test dispute and PayPal Sandbox accepted the request (masked receipt `docs/evidence/RECEIPT_20261104_live.md`), and on 2026-11-05 (UTC+8) a second send to a newly filed test dispute was accepted the same way (`docs/evidence/RECEIPT_20261105_live.md`); other dispute rows are covered by mocked-transport tests. A synthetic digital-goods case shows the time evidence: payment, order record, message digests, delivery and claim, with the gaps between them, preserved and ordered but never judged. The first commit of the repository is dated 2026-10-08, inside the submission period. The [2:02 demonstration](https://youtu.be/K28N9QhRp1E) shows the merchant workflow. PayGuard works alongside PayPal's Resolution Center and seller protection. The problem framing comes from the published ombudsman decisions cited above.
