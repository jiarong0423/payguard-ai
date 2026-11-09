# APIMatic run, 2026-11-09

What was done with APIMatic's own CLI (version 1.5.0) and an APIMatic account, on the generated description of the local console API (`docs/api/openapi.json`: OpenAPI 3.1, 37 operations). No payment was requested. Nothing was published: every output below is a local folder and none of it is in this repository.

| Step | Command | Result |
| --- | --- | --- |
| Validate, first run | `apimatic api validate --file=openapi.json` | Failed: 345 errors (344 duplicate schema titles, 1 `exclusiveMaximum` type), 331 warnings, 1,291 information notes |
| Fix | `tools/export_api_docs.py` now drops the auto-generated schema titles and writes integer exclusive bounds as inclusive ones | export tests pass |
| Validate, second run | same command | Succeeded: 0 errors, 556 warnings, 1,291 information notes |
| Documentation portal | `apimatic portal generate` | Succeeded: two guides (what TradeGlot is and is not; the read-only MCP server), `llms.txt` and `llms-full.txt`, a `code-sample-api` folder, seven language tabs |
| SDKs | `apimatic sdk generate -l <language>` | Succeeded for python, typescript, java, csharp, php, ruby and go (650 to 805 files each) |
| API Copilot | `apimatic portal copilot --force` | Configured, with a welcome message in TradeGlot wording. The portal showed its "Ask AI" panel, but the panel said it was still being prepared. No Copilot answer has been checked, so none is claimed. |

What this does not show:
- The validator reports errors, warnings and information notes. It gives no score, and none is claimed.
- The warnings and information notes were not worked down; they are mostly missing examples and descriptions.
- No SDK was published, no context plugin was generated (it needs a published SDK), and the generated SDKs were not run against the API.
- The first validation run failed. The description in the repository is the fixed version.

## Update, later on 2026-11-09: the portal is now published
The generated portal (with `llms.txt`) was published as static pages on GitHub Pages: https://jiarong0423.github.io/payguard-ai/portal/ (the files live on the `gh-pages` branch, not in `main`). The first version of the page pointed its assets at the local preview address and rendered blank; that was fixed by rewriting those links to the published address, then the live page was opened in a browser and showed the navigation, the API endpoints and the language tabs. The portal is documentation only: the API it describes runs on the author's computer (the hosted demo answers 503 on write routes). The SDKs were published nowhere, the portal's request and response examples are still empty, and no Copilot answer has been checked.
