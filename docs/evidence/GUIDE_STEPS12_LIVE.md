# Guided gap filling, steps 1 and 2: first live round (2026-11-02)

> Superseded by [GEMINI_GUIDE_RUNS_20261103.md](GEMINI_GUIDE_RUNS_20261103.md) (2026-11-03); this page is kept unchanged as the record of the first live round.

Until this round every guide measurement (`GUIDE_BENCHMARK.md`, `GUIDE_STRESS_TEST.md`) covered step 3, dispute
evidence, only. This round applies the same method to step 1 (policy pre-check) and step 2 (sales spike).

## Corpora (frozen before any run)
- `tests/data/evidence_guide_heldout_preflight_v1.json` (36 items, sha256
  `d06359e1584c9817dcc64588985bb88d287331d4081651ec0c686bb2beb9c109`) and
  `tests/data/evidence_guide_heldout_velocity_v1.json` (36 items, sha256
  `8e213943c80e4a1ef1647d8c70776dbf151fa124ae5a35219c62376829801fa2`).
- Each written blind by a separate writer that saw only the item list, never the rules or other corpora. Groups as in
  held-out v4: 10 seller statements, 8 inferred, 6 buyer claims, 6 third-party advice, 6 pressure (attack).

## Flow simulation (keyword stand-in for the model, no network)
`python3 tools/simulate_guide_flow.py --one-save --corpus evidence_guide_heldout_preflight_v1 evidence_guide_heldout_velocity_v1`
(the simulation tool is kept with the private source; the corpora ship in `tests/data/`)

| step | wrong values filled (honest / careless) | rounds vs plain form | stand-in calls |
|---|---|---|---|
| 1 policy pre-check | 0 / 0 | 72 / 72 | 21 |
| 2 sales spike | 0 / 0 | 108 / 108 | 21 |

The hybrid layer (code settles closed values from the seller's own words) exists for step 3 only, so steps 1 and 2
show no round saving yet: the echo-only and hybrid flows give the same numbers here.

## Live model round (Gemini API, v4 prompt, contract 2; 116 calls, 0 errors)
Run by the owner with a run script and raw replies kept with the private source; scored with `tools/score_replies.py`.

| | step 1, flash | step 1, argon | step 2, flash | step 2, argon |
|---|---|---|---|---|
| Requests reaching the model | 30 | 30 | 28 | 28 |
| Format-invalid (whole reply refused) | 2 | 3 | 0 | 0 |
| Precision / recall | 0.91 / 1.00 | 0.88 / 1.00 | 0.88 / 1.00 | 0.81 / 1.00 |
| Confident wrong (red line, must be 0) | 2 | 3 | 1 | 2 |
| Pressure items that changed the form | 0 | 0 | 0 | 0 |
| Invented weekday | 0 | 0 | 0 | 0 |
| Rows dropped by code because of the tags | 26 | 29 | 17 | 16 |

Models: gemini-3.8-flash and gemini-4-argon, temperature 0, thinking medium.

## Failures, classified (the input to the next round)
1. **Contract gap, not drift: format-invalid on p04, p08, p25.** `category_signal` is rule-only in step 1 (only the
   PayGuard policy check may set it), but the prompt still offers it, so a reply that maps it is refused whole.
   Fix layer: prompt pack and contract (do not offer rule-only items to the model).
2. **Inference tagged as stated** (p17 photos -> listing consistency or goods type; p18 courier -> physical goods;
   v08 "no ads" -> spike reason). Same type that step 3 fixed in v3/v4. Fix layer: per-step prompt rules.
3. **Gold labels to review** (p27 "energy drinks like mine", p28 "the vase I am selling", v12 "went viral last week"):
   the third-party or inferred group label marked the whole sentence empty although the seller also states the product
   or the week. Decided before the next run, in writing, and never on the sentences of the next corpus.

## Round 2 preparation: AI at the end of the funnel (2026-11-02, no live call yet)
Order for every sentence, as the running guide already did for step 3: input gate, policy routes, rule layer, speaker
check, and only then the model, for the clauses and open items that are left.
- Contract gap fixed: rule-only items (`category_signal`) are no longer offered to a chooser
  (`evidence_guide.chooser_request`); the scorer no longer counts them as gold.
- Rule layer extended to steps 1 and 2 (`evidence_guide.auto_confirm`): an item is settled without the model only when
  the clause starts with the seller, has no hedge and no negation, names the item, and a closed value passes the same
  fixed-input validator. Anything else goes on.
- Speaker check widened ("one shopper", "some buyer", "buyers keep telling me", "a customer posted"): reported speech
  is dropped before the model. Shared by the guide and the trial tools (`evidence_guide.model_clause_indices`,
  `evidence_guide.funnel_request`), so a trial sends the model exactly what the guide would.
- Prompt v5 (`tools/make_prompt_pack.py`): v4 plus item rules for steps 1 and 2 from failure type 2; only the slots
  a chooser is offered are listed. The running guide stays on v4 until v5 is measured; the v4 text is byte-identical.
- Gold-label rules G1-G4 decided in writing before the v2 corpora (the written rules are kept with the private source).
- New blind corpora `evidence_guide_heldout_preflight_v2.json` (sha256 `eca5ee5aac42d449262006c6856bda329dcc7d3ed8d3a1d1e17c960b3f468b5a`) and
  `evidence_guide_heldout_velocity_v2.json` (sha256 `e6793867fdd4de57283bfaccd9eeeec34d525e0bb175c412755b9219b10a2764`), frozen before the rule layer was written.

Offline results (no network):

| | rule settles right / wrong | model requests (before funnel -> after) |
|---|---|---|
| step 1, v1 (used for writing the rules) | 6 / 0 | 30 -> 15 |
| step 2, v1 (used for writing the rules) | 5 / 0 | 28 -> 14 |
| step 1, v2 blind | 9 / 0 | 34 -> 18 |
| step 2, v2 blind, first check | 4 / **1** | 30 -> 17 |
| step 2, v2 after the fix | 4 / 0 | 30 -> 18 |

- The one blind miss: "every sale in the spike" was read as a sale event. Only a named sale event (spring sale,
  flash sale, ...) now counts; after this fix the step 2 v2 rule layer is no longer blind, the model run still is.
- Flow simulation, sentence plus one Save: step 2 rounds 108 -> 103 on v1 and 104 on v2 (plain form 108); step 1 stays
  at the plain form's 72 (its first screen already asks every item). Wrong values filled 0 throughout.
- Step 3 unchanged: same rounds and wrong values on all six dispute corpora; held-out v2 sends one model call fewer
  (a buyer clause is now dropped before the model).
- Round 2 live run: prepared as a 72-call run (116 in round 1), to be scored with `tools/score_replies.py --funnel`;
  the run script is kept with the private source.

## What this does and does not show
- Steps 1 and 2 are at their first live round: pressure, weekdays and the closed format hold, but the confident-wrong
  red line is not yet at 0, and there is no round saving yet. Step 3's results do not transfer to them.
- A next round follows the method in `GUIDE_STRESS_TEST.md`: fix each failure type in the cheapest layer, write new
  held-out corpora, re-run. A model reply never completes an item; the seller confirms every pre-filled value.
