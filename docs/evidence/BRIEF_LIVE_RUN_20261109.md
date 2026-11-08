# The Gemini evidence brief: one live run (2026-11-09)

Until this run, the current evidence-brief contract had only been tested against fake models. This file records the first live run so the claim "it works" has something behind it, and says what it does not show.

- **What ran:** the **Generate AI brief** button of the dispute stage, on the owner's local console, with the Vertex AI Gemini profile (`PAYGUARD_GEMINI_OUTBOUND=enabled`, a Google Cloud project of the owner, Application Default Credentials). The hosted demo never makes this call.
- **Model shown by the console:** `gemini-3.8-flash`, labelled "Live model response". Synthetic case `case-ref-001` (item not received).
- **Outcome:** the backend accepted the reply (AI brief generated). The panel showed these points, all drawn from closed values the server computed:
  - Evidence points: the authored delivery timeline is synthetic; carrier and payment-provider events have not been verified; the local draft structurally includes proof of fulfillment; the seller response window is still open.
  - Missing evidence: verified carrier events; verified payment-provider events; "evidence sufficiency and program eligibility are not established".
  - Source references: `PP-REASONS-INR`, `PP-EVIDENCE-TRACKING`.
  - Closing line: the brief makes no compliance or dispute decision and authorizes no PayPal action; human review is required.
- **Inputs sent:** fixed synthetic facts, pinned citation IDs and closed values only. No description text, order, amount or identifier leaves the server.

**What this does not show.** One run is one run: it is not a benchmark, says nothing about other cases, and the backend allows at most three model attempts per process and one per stage, so repeating it means restarting the console. The reply text was read from the page; no separate raw response file was saved. The model's output is checked by code for shape and allowed values; the panel itself states that "semantic entailment" of the cited sources is not verified.
