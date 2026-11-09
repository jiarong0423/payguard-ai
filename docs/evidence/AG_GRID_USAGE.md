# AG Grid and AG Charts usage in PayGuard AI

All views run on synthetic data in the local console. These views use the free Community packages
(`ag-grid-community` / `ag-grid-react` 36.2.0, `ag-charts-community` 14.2.0) and need no
licence key. The separate evidence dashboard (`/dashboard.html`) uses AG Studio 3.0.0, a commercial
package that runs in trial mode without a key; see `docs/AG_STUDIO_NOTES.md`. None of this code makes a network call. Line numbers were taken at commit `9d2c67e` (branch `feat/evidence-loop`) and can move with later edits; search for the named component or test id if a line no longer matches.

## Packages

| What | Where |
| --- | --- |
| `ag-charts-community` pinned at `14.2.0`. This matches the `ag-charts-types` 14.2.0 that `ag-grid-community` 36.2.0 depends on. | `frontend/package.json:16`, `frontend/package-lock.json` |
| AG Grid Community modules registered once for the console (the grid wrapper is lazy-loaded from `frontend/src/App.jsx:20`) | `frontend/src/grid/agGrid.jsx:35` |

## Stage 02 · Sales burst: hourly and monthly charts (AG Charts Community)

Step 02 has a **Sales view** tab pair, **Chart** and **Orders table** (`frontend/src/App.jsx:918`). The chart pane (`velocity-pane-chart`, `App.jsx:919`) holds `VelocityChart`; the orders pane (`velocity-pane-orders`, `App.jsx:920`) holds the AG Grid transaction table. One pane shows at a time.

| Feature | Where |
| --- | --- |
| Chart module lazy-loaded with `React.lazy`. It builds as its own chunk, so the main bundle gains no AG Charts code. | `frontend/src/App.jsx:17` |
| Mounted once, in the Chart tab, from existing `velocity` and `state.transactions` | `frontend/src/App.jsx:919` |
| Only the chart modules it needs are registered (cartesian, bar, line, category axis, number axis, cross lines, legend) | `frontend/src/charts/VelocityChart.jsx:17` |
| **Hourly** / **Monthly** period switch; both charts stay mounted and the hidden one keeps its test ids | `frontend/src/charts/VelocityChart.jsx:61`–`:63` |
| Hourly chart: `AgCharts.create`, then `chart.update` on new state | `frontend/src/charts/VelocityChart.jsx:33`–`:35` |
| Monthly chart: same create/update pattern on its own container | `frontend/src/charts/VelocityChart.jsx:41`–`:43` |
| Both charts `destroy` on unmount | `frontend/src/charts/VelocityChart.jsx:47`–`:52` |
| Text summary under each chart (spike total versus usual rate; monthly change, labelled as illustrative demo history) | `frontend/src/charts/VelocityChart.jsx:66`, `:72` |
| Hourly buckets: baseline-window hours carry the synthetic baseline rate the signal compares against; spike-window hours sum captured amounts in cents | `frontend/src/charts/velocityChartData.js:30` |
| Spike window is left-open, right-closed, the same boundary the backend uses. Other currencies are skipped. | `frontend/src/charts/velocityChartData.js:57`, `:62` |
| Hourly options: a dashed line for the baseline rate and a bar series for the spike window, each with its own tooltip | `frontend/src/charts/velocityChartData.js:105`, `:118`, `:124` |
| Dashed cross line at the review threshold (threshold × baseline rate) | `frontend/src/charts/velocityChartData.js:138` |
| Monthly history: twelve months derived from the synthetic baseline, with a three-month average and the change versus the previous month | `frontend/src/charts/velocityChartData.js:155`, `:179`, `:180` |
| Monthly options: month line plus dashed three-month-average line | `frontend/src/charts/velocityChartData.js:189`, `:205`, `:211` |

## Evidence page · guide benchmark charts (AG Charts Community)

`frontend/src/charts/BenchmarkCharts.jsx`, mounted by the evidence page (`frontend/src/evidence.jsx:15`), draws three charts from the committed guide benchmark data.

| Feature | Where |
| --- | --- |
| Registered modules (cartesian, bar, category axis, number axis, cross lines) | `frontend/src/charts/BenchmarkCharts.jsx:15` |
| One `Chart` wrapper: `AgCharts.create` on mount, `destroy` on unmount; taller charts at phone width for wrapped labels | `frontend/src/charts/BenchmarkCharts.jsx:19`–`:27` |
| Model calls per flow (horizontal bar) | `frontend/src/charts/benchmarkChartData.js:69` |
| Guide rounds versus a plain form (horizontal bar) | `frontend/src/charts/benchmarkChartData.js:87` |
| Rounds per design step on the clean blind set, with a dashed cross line at the plain-form value | `frontend/src/charts/benchmarkChartData.js:105`, `:122` |

## Stage 03 · Dispute time evidence: event grid (AG Grid Community)

| Feature | Where |
| --- | --- |
| Dark Quartz theme to match the dispute panel | `frontend/src/TimeEvidenceView.jsx:10` |
| Rows built from the backend's ordered events; gap measured from the event above | `frontend/src/TimeEvidenceView.jsx:56` |
| Custom cell renderers: event (coloured kind dot + message detail), timestamp (`<time>`), source pill, gap to previous ("First event", "Same time", "+30 min") | `frontend/src/TimeEvidenceView.jsx:74`, `:81`, `:85`, `:89` |
| Number filter on order and gap columns, text filter on event, timestamp and source | `frontend/src/TimeEvidenceView.jsx:98`, `:99`, `:102`, `:104`, `:105` |
| Event column tooltip shows the full message detail when truncated | `frontend/src/TimeEvidenceView.jsx:101` |
| Timestamp filter and quick-filter text use the displayed UTC label | `frontend/src/TimeEvidenceView.jsx:103` |
| Table / Timeline toggle. The original timeline list and `data-testid="time-evidence"` are kept. | `frontend/src/TimeEvidenceView.jsx:110`, `:113`, `:114` |
| Grid mount | `frontend/src/TimeEvidenceView.jsx:118` |

## Guided gap filling: gap table (AG Grid Community)

| Feature | Where |
| --- | --- |
| `GapGrid`, a named export for reuse. `gapGridTheme`, `StatusChip` and `SourceChip` stay exported for `GuideLive.jsx`. | `frontend/src/GuideReplay.jsx:68`, `:6`, `:43`, `:48` |
| Status and source chips as cell renderers | `frontend/src/GuideReplay.jsx:60`, `:63` |
| Floating text filters on all three columns. Status and source filter on the shown English wording, not internal codes. | `frontend/src/GuideReplay.jsx:59`–`:65` |
| Quick filter box and a live "n of m items shown" count (`onModelUpdated`) | `frontend/src/GuideReplay.jsx:99` |
| CSV export of every item in the current step, with display wording via `processCellCallback`. File name: `payguard-replay-<scenario>-step-<n>.csv`. | `frontend/src/GuideReplay.jsx:77`, `:81`, `:163` |
| The raw model reply and its template sit in a closed `<details>` ("Show the model's closed reply") under "What the AI returned". It resets to closed on every step. | `frontend/src/GuideReplay.jsx:147` |

## Other AG Grid views

| Feature | Where |
| --- | --- |
| Stage 02 transaction grid (Orders table tab): cell renderer, value formatters, sortable/resizable/filterable columns, quick filter, row click to details, selected-row class, loading and no-rows overlays | `frontend/src/App.jsx:682`, `:923` |
| Optional analytics workspace grid with quick filter (desktop only: at 720 px and narrower the workspace shows a single-column summary instead of this grid) | `frontend/src/AnalyticsDashboard.jsx:217`, `:264`, `:272`; `frontend/src/AnalyticsDashboard.css:479` |
| Live guide gap grid, built from the exported replay theme and chips, lazy-loaded with the grid chunk | `frontend/src/GuideLive.jsx:19`, `:35`–`:37` |

## How this was checked

- `cd frontend && npm ci && npm run build` passes.
- `node tests/frontend_ag_charts_contract.mjs` checks:
  - the exact version pin and the lockfile;
  - that no enterprise package is a direct dependency, and that the enterprise packages in the lockfile are there only as AG Studio dependencies;
  - that the chart is lazy-loaded and mounted once, before the transaction grid in the source;
  - that there are no network calls in the changed files;
  - the time-grid renderers and the gap-table filter and CSV wiring;
  - hourly bucket boundaries on hand-built data, and the monthly history (twelve rows, three-month average, month-on-month change, no NaN on a zero baseline);
  - that the spike bars add up to the real backend's `total_amount` and `transaction_count` after the synthetic burst (needs `PAYGUARD_PYTHON_BIN`, Python 3.13 with `requirements.lock`).
- Checked by hand in headless Chromium against `./tools/run.sh console` on the earlier `cloud/c1-ag-grid` build (before the Chart / Orders table tabs and the monthly chart existed):
  - the chart draws, and its tooltip reads "500.00 USD, 50 captures";
  - the time grid shows 8 events with gaps;
  - the gap-table floating filter narrows 5 items to 2, and the quick filter to 4;
  - the CSV download has the step's 5 rows;
  - there were no console warnings, and the only requests went to `127.0.0.1:8000`;
  - the chart is present before and after "Load sales burst", with the PWA service worker controlling the page and with `PAYGUARD_DEMO_MODE=public`;
  - the replay reply disclosure starts closed, opens on click and is closed again on the next step.
