# AI and privacy note (2026-11-09)

PayGuard AI is the earlier name of TradeGlot. This note says what visitor text can reach an AI model, what is kept, and who wrote and checked what. Each statement names the file that backs it, so it can be checked with grep. Where a statement is not backed by code in this repository, it says so.

## 1. What can reach Gemini on the hosted demo

- **Only the evidence guide, and only if the operator opts in.** The hosted demo uses keyword rules unless the operator sets `PAYGUARD_HOSTED_GUIDE_MODEL=gemini`; otherwise the chooser is `None` and no worker can start (`backend/app/guide_routes.py`, `hosted_guide_service`). The shipped default, with no opt-in, therefore sends nothing to Gemini.
- **Everything else that would call a model answers 503 on the hosted demo:** `/api/v1/ai/evidence-brief` and `/api/v1/studio/agent-turn` are in `DISABLED_ROUTES` (`backend/app/demo_mode.py`). PayPal Sandbox writes are disabled there too; only the OAuth connect and read routes can open when the read-only switch is on (`READONLY_OPEN_ROUTES`, same file).
- **Caps when opted in:** 5 model calls a minute and 20 a day shared by all visitors, 10 per session, at least 2 seconds apart; past a cap the keyword chooser answers (`backend/app/guide_routes.py`: `HOSTED_GUIDE_CALLS_PER_MINUTE`, `HOSTED_GUIDE_CALLS_PER_DAY`, `GUIDE_MODEL_CALLS_PER_SESSION`, `GUIDE_MODEL_MIN_SPACING_SECONDS`).

## 2. What is sent when a model call happens

- The input is the text a visitor types in the guide (`POST /api/v1/guide/turn`, field `text`). Before anything is sent, `evidence_guide.sanitize_input` (`src/payguard/evidence_guide.py`) refuses text that is not English ASCII, is over 400 characters, contains a link, or has too many digits; refused text is never sent.
- Text that a keyword route marks as a policy matter is not sent (`route_policy`, same file; used in `model_request` in `backend/app/guide_routes.py`).
- At most 3 clauses of at most 80 characters each are kept (`split_clauses`, same file). Clauses spoken by a buyer or a third party, and clauses the rule layer already settled, are dropped (`model_request`, `model_clause_indices`).
- The request holds the clauses, the situation name and the status of each still-open form item. The code comment on `chooser_request` says it carries "no earlier text, no values", and `model_request` removes items already settled. Form values typed into fixed fields are not part of it.
- The request goes to a separate worker process, which calls Gemini (`backend/app/guide_model.py`, `integrations/gemini/worker.py`). The model only returns choices from a closed list, and the backend rejects anything outside the schema.
- Not backed by this repository: what Google does with a prompt after it arrives. The hosted guide uses a free-tier key (comment above `HOSTED_GUIDE_MODEL_ENV` in `backend/app/guide_routes.py`); Google's terms for that tier apply, and no code here controls them. Do not type real customer or personal data into the guide.

## 3. What is stored

- The module docstring of `backend/app/guide_routes.py` says neither seller text nor form values are stored or echoed; the server keeps statuses and weekday hints. The `GuideSession` dataclass in that file has no field for the typed text, and the model reply shown to the visitor is a fixed template text chosen by code (`model_text_shown` is always `False`, `values_stored` is always `False` in the response schema).
- Guide state lives in an in-memory dictionary keyed by demo session and is dropped with the session or on Reset demo (`GuideService._purge`, `GuideService.forget`).
- The per-session AI call log keeps timing, token counts, model name and outcome, never the prompt or the reply, in memory only (`backend/app/ai_usage.py`, module docstring).
- The container runs the server with `--no-access-log` (`Dockerfile`, last line), and the only logging in the traffic layer records the number of forwarding hops (`backend/app/traffic.py`, `LOGGER.warning`).
- Not backed by this repository: logs kept by Render or Google outside the application.

## 4. Who wrote and reviewed what

- The code was written and reviewed with AI coding agents, Claude and Codex, under the owner's direction and review. The repository files that record this for Claude are named below; the statement about Codex comes from the owner and is not recorded in a repository file.
- The review rounds named in the README ("independent reviewer agents (judge, PayPal developer relations, sponsor panel, security engineer, UI/UX)") are AI agents, not outside people (`README.md`, section on review and attack rounds; `docs/evidence/RED_TEAM_ROUNDS_20261104.md`).
- The second rater of the answer keys is "a separate Claude agent session, not a domain expert and not a person" (`docs/evidence/SECOND_RATER_20261109.md`).
- The country-rule and PayPal-clause spot-check verdicts are the reading of an AI ("the author's (Claude) reading"), with no human re-read; Gemini was not run for them (`docs/evidence/RULES_SPOTCHECK_20261110.md`, "Who compared"; `docs/evidence/RULES_SPOTCHECK_20261108.md`; `docs/evidence/PAYPAL_CLAUSES_SPOTCHECK_20261108.md`).
- No user study was run (`docs/submission/devpost_story.md`, "Limits and access").
