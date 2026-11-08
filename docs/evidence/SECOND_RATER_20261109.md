# A blind second rater for the answer keys (2026-11-09)

The answer keys (30 cases in v1, 20 in v2) were written by one person, who also built the program under test. This file records a second, independent labelling of all 50 cases, and says what it does and does not show.

**Who the second rater is.** A separate Claude agent session, not a domain expert and not a person. It was given only: the definitions of the four verdicts and the method (the "What is tested" and "Method" sections of [CHECKLIST_ANSWER_KEY_EVAL.md](CHECKLIST_ANSWER_KEY_EVAL.md), without the per-case tables), the 50 case inputs with every answer field removed, and one read of PayPal's [dispute reasons and evidence](https://developer.paypal.com/disputes/reasons-evidence/) page. It did not read the answer keys, the evaluation tables or the program's source. It saved its labels first and only then ran the comparison. (An earlier attempt on the same day is not used: that rater had read the per-case table first, so its 50 of 50 agreement could not be told apart from copying.)

**Result.** Verdict agreement 47 of 50 (94.0%, Wilson 95% interval 83.8% to 97.9%); full agreement (verdict and the list of missing request ids) 43 of 50; Cohen's kappa over the four verdicts 0.903. Two cases were marked ambiguous by the rater (AK-12, HK-17). Reproduce with `python3 -B tools/compare_second_rater.py`; the labels are in `data/eval/second_rater_labels_v1_v2.json`.

| Case | Author | Second rater | What differs |
| --- | --- | --- | --- |
| AK-12 | SUFFICIENT | INSUFFICIENT | A duplicate evidence id: the author reads the duplicate as harmless, the rater as a rejected input |
| AK-20 | SUFFICIENT | INSUFFICIENT (missing r1) | An e-mail link as delivery record for a digital item: the author counts it as notes, the rater wants a carrier number, notes or a document |
| HK-09 | SUFFICIENT | INSUFFICIENT (missing r1) | Unauthorised-transaction reason: the rater reads PayPal's page as accepting carrier plus tracking only, not notes with a picture |
| AK-14, AK-15, AK-16, HK-12 | INSUFFICIENT, missing r1 | INSUFFICIENT, no ids listed | Same verdict; the rater did not list a missing id when the program rejects an input, and the definitions do not fix that convention |

**What this shows.** For 47 of 50 synthetic cases an agent that did not see the keys reached the same verdict from the written definitions and PayPal's public page. The three differences are places where the author's key and a careful reading of the page can reasonably differ (HK-09 is also the case the program disagreed with the key on in the first v2 run). The key was not edited after this comparison.

**What this does not show.** It is one AI rater, not an expert panel and not a person; the definitions it worked from were written by the same author as the key; 50 cases are a small sample of synthetic situations. It is not inter-rater reliability in the sense of a study, and it says nothing about real disputes or about PayPal's decisions.
