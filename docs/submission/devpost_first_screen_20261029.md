# Devpost first-screen paragraph (draft, 2026-10-29)

Status: draft prepared on the `fix/judge-20261029` branch for the project owner to paste at the top of the Devpost "What it does" section. The Devpost page itself was not changed. Every number below comes from this repository or from a local run on 2026-10-29.

## Paragraph

**Built for small US PayPal sellers who first learn about a problem from a "respond by \<date\>" email.** In the demo, a merchant goes from the dispute notice to a pseudonymized, integrity-checked evidence ZIP in four clicks; a scripted timed local run on 2026-10-29 took 16 seconds from opening the dispute stage to the ZIP download, and the same deterministic rules that gate the optional Gemini brief also gate the real Sandbox invoice draft. The PayPal side is real where it matters: one authenticated Sandbox run on 2026-10-07 created an unsent USD 10.00 draft, id `INV2-2MTA-PRPQ-4CAJ-W5UW`, and the dispute stage reads `GET /v1/customer/disputes` from a connected Sandbox account (covered by mocked-transport tests; not yet run against a live Sandbox dispute) or, with no account connected, from a labelled fixture in the same JSON shape, and previews the multipart `provide-evidence` request, which is sent only after local approval with an explicit operator flag. `./tools/run.sh test` passes 436 tests (2 skipped).

## Facts behind each claim

| Claim | Where it comes from |
| --- | --- |
| Four clicks from dispute stage to ZIP | Next: dispute evidence (case auto-loads) → select case → Prepare evidence draft → Download review ZIP; `frontend/src/App.jsx` |
| 16 seconds | Local run on 2026-10-29, Vite dev server at 127.0.0.1:5173 with `./tools/run.sh api`; `performance.now()` from the stage-03 click to the "Internal review ZIP downloaded locally" notice, including the four clicks |
| 2026-10-07 Sandbox run, `INV2-2MTA-PRPQ-4CAJ-W5UW` | README "Verified once against the real Sandbox"; operator-attested, not replayable without the operator's Sandbox app |
| Disputes readback and provide-evidence preview | `backend/app/paypal_disputes.py`, `backend/app/paypal.py` allowlist, `tests/test_paypal_disputes.py` |
| 436 tests (2 skipped) | `./tools/run.sh test` on the public clone at this commit |
