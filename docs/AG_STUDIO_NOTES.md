# AG Studio dispute evidence readiness dashboard

`/dashboard.html` is a separate page built with AG Studio 3.0.0. It shows the synthetic dispute cases, the evidence their provider snapshot requests, their time evidence, the recorded guide benchmark and the recorded Channel3 searches. The console links to it from the top bar ("Dashboard") and from step 03 next to the case review; the evidence page links to it too, and the dashboard links back to the console.

The dashboard only shows and orders synthetic records. It makes no dispute decision, predicts no outcome, writes no data and submits nothing to PayPal. The hosted demo (`PAYGUARD_DEMO_MODE=public`) serves it like any other static page and makes no model call.

## What is custom, what is Studio's own, what is not used

| Part | Custom (this repository) | Studio built-in |
| --- | --- | --- |
| Theme | `frontend/src/dashboard/theme.js`: `studioTheme.withParams(...)` with the console's indigo accent (`#4f46e5`, `#4338ca` hover, `#eef2ff` tint, as in `frontend/src/index.css`), Inter 14 px, widget, grid and chart parameters; a phone variant (`compactTheme`) widens the AI panel to the screen | The Studio theming engine and parameters |
| Widgets | `frontend/src/dashboard/widgets.jsx`: a **deadline tile** and an **evidence checklist** (React). Both read through `widgetApi.getData`, so page filters, the case button filter and cross-filters apply; clicking a case in the checklist calls `widgetApi.toggleCrossFilter` (with `crossFilter: 'highlight'` it keeps every case visible and dims the rest) | Value tiles (one with a widget-level filter), button filter, bar and column charts, grids |
| Layout | `frontend/src/dashboard/layout.js`: two pages on the 24-column canvas, an "Evidence auditor" answer slot at the top of each, a full-width time-evidence chart so the event names are not cut off, a stacked phone layout (≤ 720 px, KPI tiles two per row); header page switcher and "Ask the auditor · edit layout" | Canvas, drag, resize, edit and view modes, filters panel |
| Agent | `frontend/src/dashboard/auditor.js`: the **evidence auditor**, an agent with its own `run` loop (below) | The agent framework (`createAiHarness`, `delegateTo`, telemetry) and the five built-in agents |
| Model access | `frontend/src/dashboard/studioAgentClient.js` (an `AgLlmAdapter`), `backend/app/studio_agent.py` and the `studio_agent_turn` operation in `integrations/gemini/worker.py` | `directLlmRunner` drives the built-in agents' turns |
| Recording | `frontend/src/dashboard/agentRecording.js` and `tools/record_studio_agent_run.mjs` | Telemetry observers |

Not used: Studio's compose and data panels in edit mode (collapsing them through the panel state did not take effect and they squeezed the canvas; moving and resizing widgets on the canvas still works), saving layouts (edits stay in the browser tab), and any model on the hosted demo.

## Sources

Every number on the page comes from one of these files; nothing is typed in by hand.

| Table in Studio | File | How the file is made |
| --- | --- | --- |
| `cases`, `requirements`, `time_events` | `frontend/src/data/dashboard_disputes_v1.json` | `python3 tools/build_dashboard_data.py`. It reads back the three synthetic cases that "Load dispute case" creates (`backend/app/store.py`), using the real API in process (`POST /api/v1/demo/inject`, `POST /api/v1/disputes/{case_ref}/draft`) at a fixed clock of 2026-11-01 12:00 UTC. It keeps the due date, readiness, requirement states, proof and attachment counts, review reasons and the ordered time evidence. Message digests are left out because they are keyed per session and change on every run. `--check` reports drift. |
| `benchmark` | `frontend/src/data/guide_benchmark_v1.json` | Already in the repository; its `source` field names `docs/evidence/guide_benchmark_v1.json` (commit 7091011). |
| `receipts` | `frontend/src/data/channel3_receipts_v1.json` | A byte-for-byte copy of `docs/evidence/channel3_receipts_v1.json`, written by the same tool and drift-tested. |
| (agent replay) | `frontend/src/data/studio_agent_run_v1.json` | One question recorded on 2026-11-08 (see below); `node tools/record_studio_agent_run.mjs` records more, run by the owner with a Gemini profile. |

Derived values, all computed in `frontend/src/dashboard/dashboardData.js`: days to due (due date minus the as-of time); due within 3 days (days to due ≤ 3); delivery proof ("Attachment on file" when an accepted attachment backs the fulfilment requirement; a seller-provided delivery time alone does not count); time flags (number of time-evidence flags); hours since previous (gap between consecutive events in backend order). Labels come from `frontend/src/operatorLabels.js`; the two codes it has no label for (`delivery_not_before_dispute`, `FOUND`) are labelled in `dashboardData.js`.

There are three synthetic cases. `case-ref-001` and `case-ref-002` are due on 2026-11-03 12:00 UTC; `case-ref-003` is due on 2026-11-02 12:00 UTC and its optional proof-of-refund request has no record yet. That is the data the app has.

## Evidence auditor

A custom agent in Studio's framework with its own `run` loop. For a closed set of seven questions, one per part of the dashboard, it computes the answer from the rows with plain code and builds it on the canvas with Studio's tools:

| Question | Table | Page | Canvas filter |
| --- | --- | --- | --- |
| Which cases lack proof of delivery? | cases | Evidence readiness | `delivery_proof = "No attachment on file"` |
| Which are due within 3 days? | cases | Evidence readiness | `days_to_due ≤ 3` |
| Which cases have time flags? | cases | Evidence readiness | `time_flag_count > 0` |
| Where is the longest gap between recorded events? | time_events | Evidence readiness | `gap_hours ≥ max` |
| What evidence does each case still need? | requirements | Evidence readiness | `mandatory = "Mandatory"` |
| Which guide flow needs the fewest model calls? | benchmark | Guide and Channel3 evidence | `model_calls = min` |
| Which Channel3 search was slowest? | receipts | Guide and Channel3 evidence | `latency_seconds ≥ max` |

Each answer is four Studio tool calls bound to that page: `remove_widget` (the answer slot), `add_widget` (a grid in exactly that slot), `configure_widget` (title and columns) and `add_widget_filter`. The filter tests the same field as the code, so the grid shows exactly the rows named in the reply. The reply ends with "How I built this: 1. … 4. …", and the AI panel lists each tool call. The dashboard then shows the page that changed. It also answers whether the built-in agents are on, and "clear". `tests/frontend_ag_studio_contract.mjs` records the Studio tool calls of every question.

Anything outside the set:

- **Live** (local console with a model configured; the header chip reads "Built-in agents: live"): the auditor first asks for confirmation ("This question goes to Studio's data agent (Gemini, paid). One question usually uses 3 to 6 Gemini calls (hard stop at 8) of the 20 allowed per day on this console."). Only after a plain "yes" does it call Studio's `delegate_to` tool and hand the question to Studio's **data** agent; a confirmation word on its own is never stored as a question. The data agent is told to answer only from the rows in at most two queries (`execute_query`), with no opinion about any party or result and no widgets; it is asked to finish by its fifth turn and has a hard cap of 8 turns. Before its answer is shown, it is checked for judgement wording (who wins, at fault, in someone's favour); a match is withheld with "The answer was withheld: it read as a judgement about the dispute, which this dashboard does not make.", and an agent that does not finish inside the limit gets a plain "did not finish" message instead of an answer. The final answer also appears in a status line at the top of the dashboard. Usually 3 to 6 Gemini calls per question, hard stop at 8; the console's Studio budget is 20 calls per client per day. The live starter question is "Which reason code appears most often across the three cases?".

  History (before the data-agent change the question went to the **lead** agent, which planned and delegated to the page and widget agents): The earlier starter, "Make a widget comparing cases by days to due", used all 20 calls in a 2026-11-04 rehearsal and ended with no widget, so it was replaced. On 2026-11-04 one question outside the auditor's set ("Which reason code appears most often across the three cases?") ran on the owner's local console with `gemini-3.8-flash`: six agent turns, all HTTP 200; the lead delegated and returned "Item not received" for all three synthetic cases, which matches the rows. The first live attempts that day failed (a data-agent tool description over the 4,000-character cap, and Gemini 3 signed-step ordering in the worker); both were fixed and pinned by tests. 2026-11-04 afternoon: the reason-code question twice used all 20 calls without a summary before the data-agent change. On 2026-11-08 one question ("Which reason code appears most often across the three cases?") ran live on the owner's local console through the Vertex route; the data agent made three Studio tool calls (view_schema, execute_query, complete_task) in 17.9 s, and the answer, "Item not received" for all three cases, matches the rows. That run is saved as `frontend/src/data/studio_agent_run_v1.json`.
- **Recorded** (hosted demo; one recording exists, see below): if the question matches a recorded run, the auditor replays that run's Studio tool calls with the real Studio tools and labels the answer "Recorded on <date> with Gemini; replayed here, no model call".
- **Off**: it lists its questions and says the built-in agents are off.

## Built-in agents and the governed Gemini route (owner decision 2026-11-01, local live mode only)

When the local console runs with `PAYGUARD_STUDIO_AGENTS=gemini` and a Gemini profile transport (the same one the guide uses: Vertex, or `PAYGUARD_GEMINI_TRANSPORT=api_key` with `GEMINI_API_KEY`), the dashboard creates its harness with the auditor plus Studio's five agents (`lead`, `data`, `page`, `planning`, `widget`), each run by `directLlmRunner` with the dashboard's adapter. The dashboard asks `GET /api/v1/studio/agent-status` before Studio is created; anything but `live` (hosted demo, no backend) means off.

Each model turn goes to `POST /api/v1/studio/agent-turn`:

- **Key:** never in the browser. The backend starts the Gemini worker with the key in the worker's clean environment only (`guide_model.clean_api_key_worker_environment`); `studio_agent.py` imports no provider SDK.
- **Closed input** (`studio_agent.validate_turn`): Studio's instructions (≤ 32 KB), up to 64 conversation items (the operator's question ≤ 600 characters, refused if it looks like an email address or a phone or card number; Studio's system context; assistant text; tool calls and tool results, each bounded), up to 16 tool schemas (≤ 96 KB, depth ≤ 32), tool choice and response format. Images, files, unknown fields and unknown roles are refused. The bounds come from measuring Studio 3.0.0's own agents (lead about 12 KB of instructions and 6 KB of schemas, page about 14 KB and 27 KB, planning about 17 KB and 10 KB). This route alone accepts bodies up to 256 KB; every other route keeps 16 KB.
- **Bounded output** (`studio_agent.validate_output`, applied in the worker and again in the backend): at most 8 items, 6,000 characters of text, tool calls only to advertised tools with arguments ≤ 16 KB, JSON when JSON was asked for. Thought parts never leave the worker.
- **Thought signatures:** Gemini 3 needs each tool call's signature on the next turn. They are kept server-side per session and call id (bounded) and never sent to the browser.
- **Confirmation and turn limits:** a delegated question reaches this route only after the operator's plain "yes"; the data agent is asked to finish by its fifth turn and stops at 8 turns, so one question usually uses 3 to 6 Gemini calls, hard stop at 8. The yes gate, the turn limits and the judgement check run in the browser; the server enforces the turn shape and the call caps.
- **Caps:** a `controlled_fallback.Governor` (20 calls per session, 0.5 s spacing, per-client and global day limits, 30 calls per minute across all sessions, failure breaker, in-flight cap). These counters belong to the Studio route's own Governor instance in this process; the guide has a separate Governor with its own limits, so the two do not share the per-minute or daily counts and the guide's timeout ladder (SDK 25 s < worker 26 s < subprocess 28 s < deadline 30 s).
- **Hosted demo:** the route is in `demo_mode.DISABLED_ROUTES` and answers 503 `hosted_demo_disabled` before any work; the app does not even build a model there.

### Recording and replay

The owner records one real run locally:

```sh
PAYGUARD_STUDIO_AGENTS=gemini PAYGUARD_GEMINI_TRANSPORT=api_key GEMINI_API_KEY=... ./tools/run.sh console
node tools/record_studio_agent_run.mjs --question "Which reason code appears most often across the three cases?"
```

The script opens `/dashboard.html?record=1` in headless Chromium, refuses to run unless the console reports the agents as live, asks each question through the AI panel and writes `frontend/src/data/studio_agent_run_v1.json`: the questions, every Studio tool call with its arguments, the final replies, turn counts and timings, and the final page layout. A Studio telemetry observer collects the run; it exists only in record mode on a live console. The file is validated (`agentRecording.validateRecording`: closed schema, no email addresses or phone numbers, no key-like strings) before it is written; the key never reaches the browser, so it cannot be in the file. After a rebuild the hosted dashboard replays it. Until then it says the built-in agents are off. The one recording that exists was made on 2026-11-08 by driving the same recorder steps (open record mode, ask, answer yes, read `finish()`) in the built-in browser; the file passed `validateRecording` before it was written. It holds one question only, so any other question is not replayed.

## Licence

AG Studio, AG Grid Enterprise and AG Charts Enterprise are commercial software from AG Grid Ltd (lock-declared licence `Commercial`; see `THIRD_PARTY_NOTICES.md`). The repository does not vendor them, and `npm ci` fetches them.

- The key is read only at build time, from `import.meta.env.VITE_AG_STUDIO_LICENSE`, and passed to `AgStudioProvider` (for example `VITE_AG_STUDIO_LICENSE=... npm run build`, or a `frontend/.env.local` file, which `.gitignore` excludes). Never commit a key; `tests/frontend_ag_studio_contract.mjs` fails on a key-like literal or a filled-in `.env` file.
- A Vite variable is compiled into the page's JavaScript, so a key in a public build is readable, as with any browser-side AG licence key.
- Without a key, AG Studio logs a "License Key Not Found" notice and runs in trial mode. Served locally on `127.0.0.1` no watermark was seen (the watermark element was present but hidden). A build, including the hosted one, may be given a key through the `VITE_AG_STUDIO_LICENSE` build argument (`Dockerfile`); without one, AG's trial watermark and console warnings show on a public host. The hosted demo's build is given a trial or development key by the owner; it is not a purchased production licence.

## How it was checked

- `tests/test_studio_agent.py` (fake worker only): closed input and personal-data refusals, the signature round trip that never reaches the browser, bounded and closed replies, the per-session cap and the breaker, 503 when off and `hosted_demo_disabled` on the hosted demo with zero model calls, the 256 KB limit on this route only, configuration gating, the timeout ladder.
- `integrations/gemini/test_worker.py` (fake Gemini client, real `google-genai` 2.28 types, network blocked): the turn becomes Gemini contents with function declarations, the tool-choice modes, signatures re-attached, thoughts dropped, unadvertised tools, code execution, cut-off and over-long replies refused, the large-request path open to this operation only.
- `tests/frontend_studio_agent.mjs`: the adapter contract, the recording schema, the recorder and replay, delegation and replay in the auditor, the wiring in `main.jsx`; with Playwright, a fresh build in headless Chromium where a fake model behind route interception drives the real Studio agent loop (the lead agent delegates, the page agent adds a widget, the recorder records it, nothing leaves the page origin).
- `tests/frontend_ag_studio_contract.mjs`: pins, links (console, evidence page, back link), licence, data drift and traceability, layout without overlaps on desktop and phone, the seven questions with the Studio tool calls each makes, and with Playwright the rendered page with cross-filtering and an auditor answer.
- Checked by hand in Chromium at 1280 px and 375 px: titles and chart axis labels are not cut off, the phone AI panel is fully readable and the dashboard returns to the canvas after an answer, and the evidence page's charts wrap their labels at phone width.

## Known limits

- Three synthetic cases at a fixed as-of time; the dashboard is a view of the demo data, not of real disputes.
- The built-in agents have run live on the local console (2026-11-04, several runs none saved; then on a freshly started console four questions went through the popup and one finished, which is the recorded one); the hosted dashboard replays that recorded run and calls no model.
- On a phone the AI panel takes the screen while it is open; the dashboard goes back to the canvas after an auditor answer.
- The dashboard bundle is about 870 kB gzip. It loads only on `/dashboard.html`; the console and evidence page load no AG Studio code.

## Confirmation popup and a live check on 2026-11-09

A question outside the auditor's own set now brings up a small popup ("Ask the AI helper?", with the question, the cost and the 20-calls-a-day cap, Cancel focused first) before it goes to the model; pressing "Ask the AI" does what typing "yes" did (`frontend/src/dashboard/DelegateConfirm.jsx`, test `tests/frontend_delegate_confirm.mjs`, screenshot `docs/submission/screens/delegate_confirm_popup.jpg`). The popup only exists in local live mode.

The same day, on a freshly started local console, four questions went to the data agent through the popup. One finished: "Which reason code appears most often across the three cases?" (the answer, "Item not received" for all three, matches the rows; this is the question that is recorded). Three did not finish within the call limit and showed the standard "no answer to show" text: a per-case count of time events, "which carrier status appears most often" (every case has a different value, so there is no clear winner), and "the largest disputed amount" (the data has no amount column). Failed runs are not recorded. The data agent is reliable on questions the rows answer directly and can fail on others, so the hosted replay holds one recorded question, not four.

