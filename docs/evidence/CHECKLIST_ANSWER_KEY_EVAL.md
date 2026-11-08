# Checklist answer-key evaluation (v1)

**Status: the answer key was drafted by the project author together with an AI assistant from public PayPal sources. It has not been reviewed by any third party, by PayPal, or by a dispute professional.** Treat the numbers as a self-audit, not as an independent benchmark.

## Why this exists

The published 268-case benchmark (`GUIDE_BENCHMARK.md`) measures form-guidance rounds and wrong values. It does not measure whether the system's judgement of an evidence set is correct. This evaluation adds a small answer key for that judgement.

## What is tested

The function under test is `payguard.dispute_evidence.resolve_dispute_requirements(snapshot, proof_records, attachments, as_of)`, called in-process. It is the deterministic step that, given PayPal's evidence requests for a dispute and the seller's supplied items, reports `READY_FOR_LOCAL_REVIEW`, `NEEDS_INPUT` (with the missing mandatory requests), `MANUAL_REVIEW`, a not-actionable state, or rejects the input with a fixed error code. No server, network, PayPal call or model is used.

The repository states that PayPal's live request controls the checklist and that "completeness is not sufficiency" (`us_official_source_register.md`, `PP-DISPUTE-REASONS-EVIDENCE`). So the program's output is a structural verdict, not a claim that PayPal would accept the evidence. This evaluation asks the narrower question: does that structural verdict agree with what the public PayPal documentation implies?

## Method

1. **Key written first.** The 30 cases and expected verdicts in `data/eval/checklist_answer_key_v1.json` were written before the program was run on them. Expected values were never taken from program output and were not changed afterwards.
2. **Sources.** The PayPal reason-to-evidence page (https://developer.paypal.com/disputes/reasons-evidence/, read 2026-11-08), the repo's official source register (file types and sizes, dispute response fields), and logical consistency checks. Three web requests were made (the second and third returned only an index of the API reference, no request-body detail).
3. **Coverage.** Six dispute reasons (not received, not as described, unauthorised, credit not processed, duplicate transaction, incorrect amount); edge cases include missing tracking, missing carrier, wrong dates, amount and currency mismatch, duplicate evidence, evidence unrelated to the requested type, bad attachments, expired or closed cases.
4. **Basis tag per case.** `OFFICIAL_RULE` (20 cases): follows the PayPal page or register. `AUTHOR_CONSISTENCY_CHECK` (10 cases): a logical check the author considers necessary (for example delivery before shipment) that PayPal's page does not state. Results are reported separately.
5. **Verdicts.** `SUFFICIENT`, `INSUFFICIENT` (with missing request ids), `MANUAL_REVIEW`, `NOT_ACTIONABLE`. A fail-closed rejection by the program (`DisputeEvidenceError`) counts as agreement with a key verdict of `INSUFFICIENT`, and as a mismatch with any other.
6. **Dangerous error** = program says `SUFFICIENT` while the key says anything else.

Re-run: `.venv/bin/python3 -B tools/eval_checklist_answer_key.py` (add `--json`, `--out FILE`, `--fail-on-danger`). Output is byte-identical across runs (checked by hash).

## Results

| Measure | Value |
| --- | --- |
| Cases | 30 |
| Agreement | 22 / 30 (73.3%) |
| Agreement, OFFICIAL_RULE cases | 19 / 20 |
| Agreement, AUTHOR_CONSISTENCY_CHECK cases | 3 / 10 |
| Dangerous errors (program sufficient, key not) | 5 |
| ...of which the decisive data is not an input to this function | 2 (AK-29, AK-30) |
| Over-conservative (program refuses, key sufficient) | 2 |
| Other class mismatch | 1 |
| Missing-request list correct, when program returns `NEEDS_INPUT` | 4 / 4 |
| Key `INSUFFICIENT` answered by rejection (no missing list given) | 7 |

## Disagreements

| Case | Key | Program | Who is at fault, and why |
| --- | --- | --- | --- |
| AK-05 proof of delivery by signed document, no tracking | SUFFICIENT | rejected (`proof_record_invalid`) | Program, but safe: the PayPal page accepts notes or documents for proof of fulfillment; the program's fulfillment record demands carrier plus tracking (or a digital channel plus time). Stricter than the source. |
| AK-06 delivered before shipped | INSUFFICIENT | SUFFICIENT | **Dangerous.** Program has no cross-field date check. Key basis is author logic, not a PayPal rule. |
| AK-07 delivery date in the future | INSUFFICIENT | SUFFICIENT | **Dangerous.** Program checks only that `observed_at` is not in the future, not `delivered_at`. Author logic. |
| AK-08 tracking number "TBD" | INSUFFICIENT | SUFFICIENT | **Dangerous.** Any alphanumeric token passes the identifier pattern. Author logic. |
| AK-12 same evidence id submitted twice | SUFFICIENT | rejected | Arguably the key: rejecting a duplicated id is a defensible fail-closed choice; the key's "dedupe and accept" is an author preference. Counted as a program mismatch, not hidden. |
| AK-13 request type outside the reason table, with a proof attached | MANUAL_REVIEW | rejected | Arguably both. The program does route an unmapped request to manual review when no proof is attached (see AK-28), but rejects when a proof is attached to it. Non-dangerous. |
| AK-29 refund 5.00 against a 20.00 difference | INSUFFICIENT | SUFFICIENT | **Dangerous by definition, but out of scope for this function.** It receives no disputed amount, so it cannot compare. Amount reconciliation is not exercised here (a separate send-time amount guard exists in `backend/app/paypal_disputes.py`; it was not tested). |
| AK-30 EUR refund on a USD dispute | INSUFFICIENT | SUFFICIENT | Same as AK-29. |

Counting only dangerous errors where the program had the data (AK-06, AK-07, AK-08): 3. All five are on `AUTHOR_CONSISTENCY_CHECK` cases; none contradicts a rule stated by PayPal.

## Limitations

- **Not independent.** Author and AI wrote the key; the same people know the program. Source reading was kept separate from program output, but this is not a blind third-party review.
- **Small and synthetic.** 30 hand-written cases; agreement rates carry wide uncertainty and are not a prevalence estimate. Several cases were written to expose gaps, so the rate is not representative of real traffic.
- **Thin official basis.** The PayPal page gives evidence types per reason but no stated rules on dates, amounts, mandatory status, formats or sufficiency. The API reference pages fetched held no request-body detail. Every date, placeholder, amount and duplicate expectation is an author inference.
- **Structural verdict only.** "Sufficient" here means the structure is complete for local review. It is never a prediction that PayPal accepts the evidence or the seller wins.
- **Adapter.** The runner translates PayPal evidence names to the program's schema and passes content through unchanged. An unsolicited item with no matching request cannot be expressed in the program's input, so "irrelevant evidence" is tested as a wrong-type item attached to a request.
- **Scope.** Only the dispute-requirement resolver was evaluated, not the guided form flow, the intake contract preflight, or any AI brief.
- Nothing in the program or tests was modified.

## Re-run after the fix (2026-11-08, same answer key, unchanged)

The first run (above) found three real logic gaps on author-logic cases: AK-06 (delivery before shipment), AK-07 (delivery in the future) and AK-08 (placeholder tracking number "TBD"). The program passed all three. They were fixed in `src/payguard/dispute_evidence.py` (`_validate_proof_fields`): a delivery earlier than its shipment, a shipment or delivery after the evaluation instant, and a placeholder tracking number (TBD, N/A, none, pending, unknown, a value of one repeated character, and similar) are now rejected with the existing closed code `proof_record_invalid`, so no API or screen contract changes. Unit tests for both directions were added in `tests/test_dispute_evidence.py` (real-looking tracking numbers and same-day delivery still pass). The answer key was not edited after the first run.

| | First run | After the fix |
|---|---|---|
| Agreement | 22 / 30 (73.3%) | 25 / 30 (83.3%) |
| Official-rule cases | 19 / 20 | 19 / 20 |
| Author-logic cases | 3 / 10 | 6 / 10 |
| Dangerous errors (program says sufficient, key says not) | 5 | 2 |

The two remaining dangerous errors are AK-29 and AK-30 (amount mismatch and currency mismatch). They are marked `[input-gap]` in the output: the disputed amount and currency are not inputs of `resolve_dispute_requirements`, so the function cannot see them. They are not fixed here; fixing them needs the amount to be passed into this function, which is a larger interface change. The other three mismatches (AK-05, AK-12, AK-13) are unchanged.

Reproduce: `PYTHONPATH=src:backend .venv/bin/python3 -B tools/eval_checklist_answer_key.py` (no network, no model, byte-identical output across runs).
