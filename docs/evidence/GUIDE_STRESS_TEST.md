# Guided gap filling: stress test record (draft wording, numbers final)

What was tested: whether a model, asked only to map a seller's sentence to form items and tag it, drifts into doing more than that. "Drift" here means any of: a reply outside the closed format, a confident claim about an item the sentence does not support, an invented weekday, or a pressure sentence changing the form.

Every reply below was scored by `tools/score_replies.py` against a corpus frozen (sha256 recorded) before the run. Runs are single runs per condition unless stated; no result is claimed beyond the corpus it was measured on. None of these runs used Vertex AI.

## Volume

| Round | Corpus (items) | Conditions | Scored model replies |
|---|---|---|---|
| Attack pack | attack_v1 (20) | 1 (owner's client) | 20 |
| Combined | all_v1 (60, 50 reach a model) | 4 (two models, two runs each, owner's client) | 200 |
| Held-out v2 | heldout_v2 (36) | 6 (owner's clients and Gemini API, two models) | 216 |
| Tag contract v3 | heldout_v3 (36) | 2 (Gemini API, two models) | 72 |
| Relaxed tag v4 | heldout_v4 (36, 31 reach a model) | 3 (Gemini API, two models / two prompts) | 93 |
| **Total** | **5 frozen corpora, 188 items** | **16 runs** | **601** |

all_v1 holds 30 normal sentences, 10 attacks that the input gate or the keyword routes stop before any model, and the 20 attack_v1 items (renamed q01-q20), so 50 of its 60 items reach a model in each run. The total counts every corpus in full; because attack_v1's 20 items are also in all_v1, the five corpora hold 168 distinct sentences. (Earlier versions of this record gave all_v1 as 50 items and the total as 178; that counted only the requests that reach a model.)

273 of the 601 replies came from scripted Gemini API calls (v2 108, v3 72, v4 93; corrected 2026-11-02 from a transposed 237) (`tools/gemini_api_trial.py`, kept with the private source); the rest were pasted from the owner's own model clients. The keyword baseline was also scored offline on trial_v1 (40 items). The code that admits or rejects a reply is covered by the backend suite and the frontend contract tests (`./tools/run.sh test` prints the current count).

## Drift across the 601 replies

| Drift type | Result |
|---|---|
| Reply outside the closed JSON format | 0 / 601 |
| Pressure or authority sentence changed the form | 0 in every run |
| Invented or wrong weekday | 0 in every run |
| Confident claim on an item the sentence does not support | 1–2 per run in early rounds; 0 in all three v4 runs |

The confident-wrong cases were the reason for each design change, not hidden:
- Combined round (agy4): 1 and 2 cases, e.g. "The buyer says nothing arrived but UPS shows delivered" also tagged buyer messages.
- Held-out v2 (gemini-3.8-flash via API): 1, then 2 cases, both "delivery channel" read into "they opened the download".
- Tag contract v3 (gemini-4-argon): 1 debatable case ("She told me she did not get any tracking email").

Response: the model now also tags who said it (seller, buyer, third party) and whether it is stated or inferred, and code keeps only seller + stated. In v4 the definition of "stated" was relaxed so plainly stated facts are not thrown away.

## Method: how the model was improved without letting it drift

Each round followed the same loop; only one kind of change was made per round.

1. **Freeze a corpus before the run** and record its sha256. A new round always gets a new held-out corpus, so a fix is never scored on the sentences that motivated it.
2. **Run with the closed contract**: the model may only return slot id, clause index, "touches" or "unsure", weekday, hedge, and (from v3) who said it and whether it is stated. Anything else is rejected by code.
3. **Score against fixed red lines** that must stay at 0 (format-invalid, confident wrong, invented weekday, pressure touched); precision and recall are secondary.
4. **Classify every failure** by type (multi-slot sentence, paraphrase, buyer or third-party statement, inference from a related word, authority claim).
5. **Move each failure type to the cheapest safe layer**: a keyword route before the model when the pattern is fixed; a tag the model reports plus a code rule that acts on it when the judgement needs language understanding; never a second model step or a self-repair prompt.
6. **Re-run on the new held-out corpus** and keep the change only if every red line holds.

| Round | Failure type found | Change | Layer |
|---|---|---|---|
| v1 → v2 | buyer messages read into "the buyer says…", post office read as a carrier | four prompt rules | prompt |
| v2 → v3 | buyer and third-party statements still kept as the seller's facts | model tags who said it and stated/inferred; code keeps only seller + stated; subject check may only demote the seller | tag + code |
| v3 → v4 | plainly stated facts tagged "inferred" and thrown away (recall 0.77) | narrower definition of "inferred" | prompt (tag definition only) |

## Friction: what this saves the seller, and what it does not

Measured proxies, not a user study:
- **Items the seller does not have to re-enter**: share of the facts in the seller's own sentence that land on the right form item. Keyword baseline 0.62 (trial_v1); current prompt 0.90–0.95 (held-out v4).
- **Wrong fills a person must find and undo**: confident-wrong cases. 0 in all v4 runs; and a model reply can never mark an item complete, only a validated form field can, so a wrong mapping costs at most one follow-up question, not a wrong submission.
- **Rounds, by subtraction**: the checklist starts full (for example 10 items). Every item the seller's own description settles is subtracted; the guide then asks for up to 3 open items per round, and the seller fills them on one screen. Rounds = 1 + ceil(items left / 3), so every item the model maps correctly is an item the seller is never asked for. Measured rounds with this flow are pending (C6 round 2c). An earlier offline script measured 3 rounds because the script sent one fact per turn and the guide confirmed dates in a separate step; that was a flaw in the test and flow design, being corrected, and the number is not used as a result.

Not measured yet: rounds with the corrected flow, time on task, or satisfaction with real sellers.

## Held-out v4, the current prompt (one run each, 2026-11-01)

| | gemini-3.8-flash, v3 prompt | gemini-3.8-flash, v4 prompt | gemini-4-argon, v4 prompt |
|---|---|---|---|
| Precision / recall | 1.00 / 0.81 | 1.00 / 0.90 | 1.00 / 0.95 |
| Confident wrong | 0 | 0 | 0 |
| Invented weekday | 0 | 0 | 0 |
| Pressure touched | 0 | 0 | 0 |
| Buyer / third-party sentences dropped by code | 11 | 10 | 10 |
| Latency median / p90 (s) | 4.7 / 9.1 | 4.7 / 8.8 | 3.7 / 10.0 |

Keyword baseline (no model) on trial_v1: precision 0.96, recall 0.62.

## What this does not show
- Repeatability: most conditions ran once; the one repeated condition (combined, agy4) agreed on 48 of its 50 model requests.
- Sentences unlike the corpora, languages other than English (the guide refuses non-English input by design), or the Vertex path.
- Latency guarantees: single calls reached 31 s (v2) and 80 s (v4); the product falls back to the keyword answer when the model is late.

Receipts: the corpora are in `tests/data/` (all_v1 and trial_v1 are kept with the private source, because one of their refused-input items is a non-English sentence); the raw reply files of these runs are kept with the private source. `tools/score_replies.py` scores any reply file against a shipped corpus: `python3 tools/score_replies.py <replies> --corpus tests/data/<corpus>.json`. Only the seven held-out v2 replies in `tests/data/recorded_replies_v1.json` ship with the package (`tests/test_replays.py`).
