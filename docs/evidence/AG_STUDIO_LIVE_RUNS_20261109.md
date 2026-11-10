# AG Studio built-in agents: three more live runs (2026-11-09)

Three questions were asked through the dashboard's AI panel on the author's local console, with the evidence auditor handing each to AG Studio's data agent (Gemini, the author's own AI Studio key typed hidden; the key never reaches the browser and is not in the file). Each question went through the "Reply yes to send it" confirmation. The recorder is the same code path as `tools/record_studio_agent_run.mjs` (here driven from Python); the data is the three synthetic cases.

| Question | Studio tool calls | Turns | Time | What the agent answered |
| --- | --- | --- | --- | --- |
| Which case is due first? | 3 (`view_schema`, `execute_query`, `complete_task`) | 3 | 15.8 s | `case-ref-003`, from the cases table |
| What is the total disputed amount across the three cases? | 4 | 4 | 24.7 s | It said the dataset has no disputed-amount field, so it gave no total (an honest "not in the data" answer, not a number) |
| Which case has the most missing evidence? | 4 | 4 | 22.1 s | `case-ref-003`, with one missing evidence requirement, from the requirements table |

Total: 3 runs, 11 Studio tool calls, all finished. The recording file is `docs/evidence/studio_agent_live_runs_20261109.json` (closed schema, passes the project's own `validateRecording`; no key, no personal data, no PayPal identifiers).

## What this does and does not show
- It shows the built-in agents answer real questions about the dashboard data with Studio's own tools, live, and say so when the data cannot answer.
- The three runs were added to the dashboard's recording, `frontend/src/data/studio_agent_run_v1.json`, next to the run recorded on 2026-11-08. AG Studio's built-in agents ran live on the local console on 2026-11-04 (several runs, none saved), on 2026-11-08 (one run, recorded) and on 2026-11-09 (three runs, 11 tool calls, recorded); the hosted dashboard replays the recording dated 2026-11-09, with its four questions, and calls no model.
- Three questions on synthetic data are a demonstration, not a benchmark. The answers were not scored against an answer key; the first and third match the table rows.
