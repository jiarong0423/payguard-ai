# Checklist answer-key evaluation (v1 and v2, reported separately; v2 is held out by case, not by theme, and its author had seen the v1 results)

**Status: both answer keys were drafted by the project author together with an AI assistant from public PayPal sources; neither has been reviewed by any third party, by PayPal, or by a dispute professional, so every number below is a self-evaluation of a small hand-written set and says nothing about real dispute traffic.**

**Cost: 0 model calls, 0 network requests, deterministic.** Two consecutive runs of `--set all --json` are byte-identical (sha256 of the output `91b1615f...88d4c5`).

**Second rater (added 2026-11-09):** a separate AI rater that had not seen these keys labelled all 50 cases; see [SECOND_RATER_20261109.md](SECOND_RATER_20261109.md). It is not an expert review.

## What was frozen, and when

- v2 key: `data/eval/checklist_answer_key_v2_heldout.json`, sha256 `06992da608733341abc33b148b423c1dcc2df75282a09e860ec3af3a3c790cb8`, computed 2026-11-08T15:12:21Z, recorded in `data/eval/PREREGISTRATION_v2.md` before the program was run on any v2 case. This orders events inside this repo's files only; it is not a notarised timestamp.
- Program under test: git HEAD `d9cf900bad2d83bbaf0695a32cedb6266fbf69fd` (2026-11-05) **plus uncommitted changes**: the working tree has 33 modified or untracked paths, including `src/payguard/dispute_evidence.py` and `tests/test_dispute_evidence.py` (the three v1 fixes described below are uncommitted); this evaluation's own files are untracked. The scored program is therefore not reproducible from a commit alone.
- v1 results stay as first recorded: 22 / 30 on the first run, 25 / 30 after the fix. v1 and v2 are never pooled into one ratio.
- v2 showed failures; the program was not changed before the score was recorded, and they are listed as unfixed.

## Results per subset

Wilson 95% interval, z = 1.96. Baseline = a rule that answers INSUFFICIENT for every case (it agrees only where the key says INSUFFICIENT). Each rate is a self-evaluation on a hand-written set with the limits stated in this report, and the intervals are wide.

| Subset | n | Agree | Rate | Wilson 95% CI | Always-INSUFFICIENT baseline | Dangerous (case ids) |
| --- | --- | --- | --- | --- | --- | --- |
| v1 | 30 | 25 / 30 | 83.3% | 66.4% - 92.7% | 16 / 30 (53.3%) | 2 AK-29, AK-30 |
| v1_official_rule | 20 | 19 / 20 | 95.0% | 76.4% - 99.1% | 10 / 20 (50.0%) | 0  |
| v1_author_logic | 10 | 6 / 10 | 60.0% | 31.3% - 83.2% | 6 / 10 (60.0%) | 2 AK-29, AK-30 |
| v2 | 20 | 18 / 20 | 90.0% | 69.9% - 97.2% | 6 / 20 (30.0%) | 1 HK-20 |
| v2_official_rule | 14 | 13 / 14 | 92.9% | 68.5% - 98.7% | 4 / 14 (28.6%) | 0  |
| v2_author_logic | 6 | 5 / 6 | 83.3% | 43.6% - 97.0% | 2 / 6 (33.3%) | 1 HK-20 |

Reading the table with its limits: the program agrees with its own authors' key on 18 of 20 v2 cases (plausible range 70% to 97% at n = 20), against 6 of 20 for the always-INSUFFICIENT baseline on the same key, but the key was written by the same side that built the program, and 3 of the 18 agreements are fail-closed rejections not checked against the key's reason (Disclosure 7). v1's 25 / 30 is a post-fix number on the set that exposed the bugs.

## Dangerous errors (program says SUFFICIENT, key says otherwise), by case

- v1: AK-29, AK-30 (author-logic cases; the function is never given the amounts or dispute currency, Disclosures 4 and 5). None on v1 official-rule cases.
- v2: HK-20 (author-logic case; a 0.00 refund passes the refund record check; a real gap, **unfixed**). None on v2 official-rule cases.

## Disclosures

1. **Author.** Both keys were written by the project author with an AI assistant; the same side built the program. No third-party, PayPal or dispute-professional review exists.
2. **v2 is held-out by case, not by theme.** The v2 author had seen the v1 results. HK-06, 09, 12, 18, 19 are new inputs on themes where v1 already showed program behaviour. Lines 1-200 of `src/payguard/dispute_evidence.py` (constants, helpers, snapshot validation) were read to learn the input vocabulary; the proof-record validation and routing code were not read before the key was frozen.
3. **v1 was tuned on after scoring.** After the first v1 run three program gaps were fixed (delivery before shipment, future dates, placeholder tracking numbers such as TBD) and the run repeated. The v1 key was not edited; the program was. So 25 / 30 is measured on the set that exposed those bugs. Only v2 has not been used to tune anything.
4. **AK-29's "amount owed" is not a PayPal data field.** The case compares a refund with "charged minus expected". PayPal's dispute record carries the disputed amount, not an expected correct price, so that difference cannot be derived from PayPal data; the program cannot honestly implement it and it was not faked.
5. **AK-29 and AK-30 scope.** They count as dangerous by definition, but `resolve_dispute_requirements` receives neither amount nor dispute currency. Amount mismatch is stopped by a different pre-send gate (`submit_refusal` and `dispute_amount_mismatch` in `backend/app/paypal_disputes.py`). That gate was not exercised here, so no claim is made about it beyond its existence.
6. **No third-party audit** of the program, the keys or this report.
7. **Rejection counts as agreement with INSUFFICIENT.** A fail-closed rejection (`DisputeEvidenceError`) with no missing-request list is scored as agreeing with a key of INSUFFICIENT, and the rejection code was not compared with the key's reason. Under a strict reading (require NEEDS_INPUT with the correct missing list) the v2 agreements for HK-06, HK-12, HK-19 would not count, leaving 15 / 20. Of the v2 INSUFFICIENT keys only HK-04 and HK-14 returned a missing list; both were correct. For v1 the first-run text said 7 rejections; after the fix the runner reports 10 (`rejected_without_missing_list`).
8. **Official table not re-fetched.** v2 reuses the reason-to-evidence table transcribed from the PayPal page in v1 (read 2026-11-08). The page lists evidence types per reason; it does not define mandatory status, field formats, date logic, amounts or sufficiency. Expectations for every author-logic case and for file types rest on the author or on the repo source register.
9. **Structural verdict only.** SUFFICIENT means the structure is complete for local review, never that PayPal will accept the evidence.

## v2 disagreements and who is wrong

| Case | Key | Program | Who is at fault |
| --- | --- | --- | --- |
| HK-09 UNAUTHORISED, notes + signed JPEG as proof of fulfillment | SUFFICIENT | rejected (`proof_record_invalid`) | Program, safe direction (over-conservative). Same cause as v1 AK-05: the fulfillment record needs carrier + tracking or a digital channel + time, while the PayPal page accepts notes or documents. Two of two such cases disagree, so this looks systematic. **Unfixed.** |
| HK-20 CREDIT_NOT_PROCESSED, refund of 0.00 | INSUFFICIENT | SUFFICIENT | **Program, dangerous, unfixed.** A zero-value refund passes the refund record check. The key basis is author logic ("0.00 is not a refund"), not a PayPal rule, but the data is inside the function's schema, so the gap is real. |

No v2 key was edited after scoring and no key error was found in v2. Boundary checks that held: due +1 s is open (HK-15), due -1 s is closed (HK-16), chargeback stage does not block (HK-17), unmapped request type goes to manual review (HK-18), a `TEST` tracking number is rejected (HK-19), a BMP attachment is rejected (HK-12, `attachment_signature_invalid`).

## After a post-hoc fix to the v2 failure (not held-out)

The pre-registered v2 result above, 18 of 20, is the held-out number. It found one real gap inside the function's schema: HK-20, a refund of 0.00 passed the refund check. After the run, `_validate_proof_fields` was changed to reject a refund proof whose amount is zero (same closed code `proof_record_invalid`; a unit test covers 0.00, 0 and a positive amount). The v2 key was not edited. Re-running the same key gives **19 of 20 (Wilson 95% interval 76.4 to 99.1), 0 dangerous errors**. Because the program was changed after the key was scored, **19 of 20 is not a held-out figure**; it only shows the gap is closed. HK-09 (a signed JPEG offered with notes as proof of fulfilment is refused) is the same over-cautious behaviour as v1 AK-05 and is left unfixed.

## Per-case tables

Reproduce: `PYTHONPATH=src:backend .venv/bin/python3 -B tools/eval_checklist_answer_key.py --set v1|v2|all` (also `--json`, `--md`, `--out FILE`, `--fail-on-danger`). With no `--set` the original v1 output is unchanged (verified byte-identical before and after the script edit).

v2 held-out:

| Case | Reason | Basis | Key | Program | Class |
| --- | --- | --- | --- | --- | --- |
| HK-01 PAYMENT_BY_OTHER_MEANS notes + refund both mandatory and supplied | PAYMENT_BY_OTHER_MEANS | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-02 PAYMENT_BY_OTHER_MEANS only OTHER requested, notes supplied | PAYMENT_BY_OTHER_MEANS | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-03 CANCELED_RECURRING_BILLING notes with small PNG | CANCELED_RECURRING_BILLING | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-04 CANCELED_RECURRING_BILLING nothing supplied | CANCELED_RECURRING_BILLING | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| HK-05 DUPLICATE_TRANSACTION refund only, refund ID complete | DUPLICATE_TRANSACTION | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-06 DUPLICATE_TRANSACTION refund proof offered for an OTHER request | DUPLICATE_TRANSACTION | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| HK-07 INCORRECT_AMOUNT refund equals the stated difference | INCORRECT_AMOUNT | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-08 UNAUTHORISED fulfillment complete, refund and OTHER optional unanswered | UNAUTHORISED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-09 UNAUTHORISED fulfillment proven by notes + signed JPEG document | UNAUTHORISED | OFFICIAL_RULE | SUFFICIENT | REJECTED (proof_record_invalid) | OVER_CONSERVATIVE |
| HK-10 SNAD product description supplied | MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-11 SNAD OTHER answered, optional refund unanswered | MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-12 SNAD notes with a BMP attachment | MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (attachment_signature_invalid) | AGREE |
| HK-13 Reason OTHER, OTHER request answered with notes | OTHER | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-14 CREDIT_NOT_PROCESSED refund answered, mandatory OTHER unanswered | CREDIT_NOT_PROCESSED | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| HK-15 Response due one second after evaluation instant | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-16 Response due one second before evaluation instant | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | NOT_ACTIONABLE | NOT_ACTIONABLE (DUE_DATE_EXPIRED) | AGREE |
| HK-17 CHARGEBACK stage, complete fulfillment evidence | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| HK-18 CANCELED_RECURRING_BILLING asks for fulfillment (not in table), nothing supplied | CANCELED_RECURRING_BILLING | AUTHOR_CONSISTENCY_CHECK | MANUAL_REVIEW | MANUAL_REVIEW (MANUAL_REVIEW) | AGREE |
| HK-19 Tracking number is the placeholder TEST | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| HK-20 Zero-value refund offered as proof | CREDIT_NOT_PROCESSED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | DANGEROUS |


v1:

| Case | Reason | Basis | Key | Program | Class |
| --- | --- | --- | --- | --- | --- |
| AK-01 INR complete carrier + tracking | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-02 INR carrier without tracking number | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-03 INR tracking without carrier | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-04 INR no evidence supplied | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| AK-05 INR proof via delivery-signature document, no tracking | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | SUFFICIENT | REJECTED (proof_record_invalid) | OVER_CONSERVATIVE |
| AK-06 INR delivered_at earlier than shipped_at | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-07 INR delivered_at in the future | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-08 INR placeholder tracking number TBD | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-09 INR refund proof attached to a fulfillment request | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-10 INR optional refund request unanswered | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-11 INR mandatory refund request unanswered | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| AK-12 INR same evidence submitted twice (same id) | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | SUFFICIENT | REJECTED (proof_record_invalid) | OVER_CONSERVATIVE |
| AK-13 INR request type not in the reason table | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | MANUAL_REVIEW | REJECTED (proof_record_invalid) | WRONG_CLASS |
| AK-14 INR notes proof with a .docx attachment | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-15 INR 12 MB PDF attachment | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (attachment_size_invalid) | AGREE |
| AK-16 INR evidence observed after evaluation time | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-17 INR complete evidence but due date passed | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | NOT_ACTIONABLE | NOT_ACTIONABLE (DUE_DATE_EXPIRED) | AGREE |
| AK-18 INR provide-evidence not an available action | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | NOT_ACTIONABLE | NOT_ACTIONABLE (ACTION_NOT_AVAILABLE) | AGREE |
| AK-19 INR dispute already RESOLVED | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | OFFICIAL_RULE | NOT_ACTIONABLE | NOT_ACTIONABLE (CASE_NOT_ACTIONABLE) | AGREE |
| AK-20 INR digital goods: email link + delivery time | MERCHANDISE_OR_SERVICE_NOT_RECEIVED | AUTHOR_CONSISTENCY_CHECK | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-21 UNAUTHORISED fulfillment complete, optional OTHER unanswered | UNAUTHORISED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-22 UNAUTHORISED notes supplied, mandatory fulfillment missing | UNAUTHORISED | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| AK-23 SNAD product description supplied | MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-24 SNAD description but mandatory refund missing | MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED | OFFICIAL_RULE | INSUFFICIENT | INSUFFICIENT (NEEDS_INPUT) | AGREE |
| AK-25 CREDIT_NOT_PROCESSED refund ID supplied | CREDIT_NOT_PROCESSED | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-26 CREDIT_NOT_PROCESSED refund proof without refund ID | CREDIT_NOT_PROCESSED | OFFICIAL_RULE | INSUFFICIENT | REJECTED (proof_record_invalid) | AGREE |
| AK-27 DUPLICATE_TRANSACTION notes + refund ID | DUPLICATE_TRANSACTION | OFFICIAL_RULE | SUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | AGREE |
| AK-28 CREDIT_NOT_PROCESSED asks for fulfillment (not in table) | CREDIT_NOT_PROCESSED | AUTHOR_CONSISTENCY_CHECK | MANUAL_REVIEW | MANUAL_REVIEW (MANUAL_REVIEW) | AGREE |
| AK-29 INCORRECT_AMOUNT refund covers only part of the difference | INCORRECT_AMOUNT | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | DANGEROUS [input-gap] |
| AK-30 INCORRECT_AMOUNT refund in a different currency | INCORRECT_AMOUNT | AUTHOR_CONSISTENCY_CHECK | INSUFFICIENT | SUFFICIENT (READY_FOR_LOCAL_REVIEW) | DANGEROUS [input-gap] |

---

# Original v1 report (kept as written; its first sections show the first-run and post-fix figures at that time)

# (v1 text follows)

**Status: the answer key was drafted by the project author together with an AI assistant from public PayPal sources. It has not been reviewed by any third party, by PayPal, or by a dispute professional.** Treat the numbers as a self-audit, not as a third-party benchmark.

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

- **Not a third-party review.** Author and AI wrote the key; the same people know the program. Source reading was kept separate from program output, but this is not a blind third-party review.
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

