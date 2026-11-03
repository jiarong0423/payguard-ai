# Guide benchmark: the optimisation baseline (2026-11-01)

Every change to the guided gap filling is measured the same way and compared with this page. A change counts as an improvement only if **wrong values stay 0** and rounds or model calls fall. Regenerate with `python3 tools/run_guide_benchmark.py --check` (writes `guide_benchmark_current.json`). The benchmark tools, the blind corpora and the result JSON are kept with the private source; the frozen totals the evidence page shows ship as `frontend/src/data/guide_benchmark_v1.json`.

**How it is measured.** `tools/simulate_guide_flow.py` sends each test sentence once to the real guide service (same routes and code as the console; no network). A simulated seller then finishes the form: the honest seller confirms only what their own sentence settled and corrects anything else; the careless seller confirms everything shown without reading. 268 cases from seven corpora, four of them blind (written by separate writers who never saw the rules, each measured once after the rules were frozen). A plain fixed-input form needs 721 rounds for the same cases.

**Scope.** These 268 cases are all step 3 (dispute evidence). Steps 1 and 2 are measured separately in `GUIDE_STEPS12_LIVE.md`; their first live round was not at 0 confident-wrong replies, so "0 wrong values" here is a step 3 result only.

## Current code (1834d2e, re-run 2026-11-02): totals over 268 cases

| flow | rounds | vs plain form (721) | model calls | wrong values filled (honest / careless) | items settled by code (wrong) |
|---|---|---|---|---|---|
| echo only (every value confirmed by a click) | 989 | +37% | 184 | 0 / 0 | 0 (0) |
| hybrid (code settles certain closed values) | 941 | +31% | 148 | 0 / 0 | 63 (0) |
| **hybrid + one Save + summary on the last round** | **697** | **-3%** | **148** | **0 / 0** | **63 (0)** |

Against 7091011 only the model calls moved (185 -> 184, 149 -> 148): the wider speaker check (cc683ed) drops one more buyer clause in held-out v2 before the model. Rounds and wrong values are unchanged. The evidence page charts still show the frozen 7091011 baseline (`guide_benchmark_v1.json`).

## History: every variant tried, in order

| step | commit | what changed | blind v4 rounds (form only 104) | wrong values | kept? |
|---|---|---|---|---|---|
| 1 | 957c885 | echo only: model / keywords map, seller confirms each value | 144 | 0 | baseline |
| 2 | a568d9a | hybrid: code settles closed values from the seller's own unhedged words; settled clauses skip the model | 135 | 0 (first version without the positive-seller rule settled 4 wrongly on blind v2/v3; fixed before v4) | yes |
| 3 | e60d3d9 | topology order + one Save (sentence and first three inputs together) | 101 | 0 | yes |
| 4 | fd51e9e | one summary at the end as its own round, values from words wait for it | 110 | 0 | no: +9 rounds |
| 5 | 7091011 | summary shown on the last fill round; one Save fills and confirms | 102 | 0 | yes |
| 6 | 1834d2e | AI at the end of the funnel for every step, wider speaker check, scoped negation, one guide per situation | same as step 5 (only held-out v2 model calls -1) | 0 | **yes (current)** |
| — | ca64f05 | example retrieval (TF-IDF nearest sentences) as an extra mapper | not used: blind v4 precision 0.87 -> 0.74, wrong kept 4 -> 9 | — | no |

Model calls on blind v4: echo only 30, hybrid 23 (-23%).

## What these numbers do and do not show
- They show the flow on one-sentence test cases, measured with a simulated seller; every case was run once.
- They do not show real sellers' time or satisfaction, multi-sentence conversations, or live model behaviour (the simulation uses the keyword mapper as the model stand-in; live Gemini runs are in `GUIDE_STRESS_TEST.md`).
- The rule wording was improved while reading blind v1-v3 failures, so only blind v4 is a clean held-out result for the current rules (the keyword-chooser baseline record is kept with the private source).
