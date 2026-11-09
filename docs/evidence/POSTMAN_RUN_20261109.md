# Postman collection run, 2026-11-09

The collection generated from the OpenAPI file (`docs/api/postman_collection.json`, 37 requests) was imported into Postman by the author earlier the same day. This note records a **run of a read-only subset of it with Newman** (Postman's command-line runner, version 6) against the local console on `127.0.0.1:8000`, started in its default demo mode: no PayPal Sandbox keys, no Gemini key, no network beyond loopback.

## What ran
- `docs/api/postman_readonly_subset.json`: 10 of the 37 requests: the session request and the 9 read-only `GET` requests that need no path parameter. A collection-level pre-request script adds the `Origin` header the local security boundary requires and the demo session header returned by the session request.
- Command: `newman run docs/api/postman_readonly_subset.json --reporters cli,json` against a local `uvicorn` of this file set. The server was stopped afterwards and no listener remained on port 8000.

## Result
| Request | Status |
| --- | --- |
| `POST /api/v1/demo/sessions` | 201 (21 ms) |
| `GET /api/v1/ai/usage` | 200 (12 ms) |
| `GET /api/v1/connections` | 200 (2 ms) |
| `GET /api/v1/country-rules/countries` | 200 (5 ms) |
| `GET /api/v1/demo/state` | 200 (3 ms) |
| `GET /api/v1/guide/state` | 200 (3 ms) |
| `GET /api/v1/health` | 200 (2 ms) |
| `GET /api/v1/paypal/disputes` | 200 (3 ms) |
| `GET /api/v1/paypal/status` | 200 (2 ms) |
| `GET /api/v1/studio/agent-status` | 200 (2 ms) |

**10 requests, 19 assertions (status and JSON body), 0 failed.**

## What went wrong first
The first run of the unmodified skeleton collection got HTTP 403 `origin_required` on the session request and 401 on every later request: the generated collection sends no `Origin` header and no session header, so the local boundary refused it. That is the boundary working, and it is why the subset adds a pre-request script. The 27 requests that were not run need a path parameter, a request body or a write path (PayPal Sandbox calls, evidence sends, AI calls); the collection still carries empty body skeletons for them, so they were **not run**.

## What this does and does not show
- It shows the generated collection can be driven from a Postman-compatible runner against the real local API once the two headers are added, and that the read-only endpoints answer 200 with JSON.
- It does not show the write paths, the hosted site, or the PayPal Sandbox calls through Postman. It is a local demo-mode run, not a run of Postman's cloud monitors.
