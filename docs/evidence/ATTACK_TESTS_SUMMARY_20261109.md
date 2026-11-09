# Attack tests in plain words (run 2026-11-09)

This page lists the kinds of attack the project was tested against, how many automated checks cover each kind, and what those checks do not prove. Every number below was printed by a test run on 2026-11-09 against the current development tree, or is read from `RED_TEAM_ROUNDS_20261104.md`. Nothing here is an outside audit.

## What was tested

| Attack class | In plain words | Checks that cover it (all passed on 2026-11-09) |
| --- | --- | --- |
| Hostile text in a dispute or seller sentence | Text that tries to give the AI orders ("ignore the rules"), or that quotes the buyer or PayPal as if it were the seller's own evidence | `tests/test_guide_routes.py` 45, `tests/test_advisory_eval.py` 17, `tests/test_dispute_evidence.py` 18 (PayPal and buyer text is kept as context, never counted as seller evidence) |
| Amount and refund mismatch | An invoice amount or currency that differs from the amount that was checked; a zero-value refund offered as proof | `tests/test_attack_r22.py` 16, plus the zero-value refund test in `tests/test_dispute_evidence.py` |
| Send without approval | Trying to send evidence to PayPal Sandbox without the local review, without the single-use confirmation, too early, twice, or from another session | `tests/test_send_confirmation.py` 14, `tests/test_r35_send_flow.py` 8, `tests/test_paypal_r24.py` 14 |
| Session, CSRF and origin | Requests with no session, a wrong token, a foreign website as origin, a wrong content type, oversized or malformed bodies | `tests/test_boundaries.py` 13, `tests/test_api.py` 74, and the input matrix below |
| Hosted write routes | Every route that would write to PayPal or call an AI model must answer 503 on the hosted demo | `tests/test_demo_mode.py` 23, `tests/test_demo_mode_integration.py` 9 (counts every way out of the process: network, subprocess, provider calls), `tests/test_hosted_readonly_sandbox.py` 21 |
| Masked dispute ids | The hosted list shows only generated codes; a real PayPal id, or an unknown code, is refused before any PayPal call | `tests/test_hosted_readonly_sandbox.py` (same 21 checks, the masking ones named `list_response_never_holds_a_real_id` and `a_real_id_or_an_unknown_code_is_refused`) |
| Read budget | The hosted demo's shared limit on PayPal reads: 429 when the minute cap or day cap is reached, recovery afterwards | `tests/test_hosted_readonly_sandbox.py` (minute-cap and day-cap checks) |
| Transport security header | The hosted app sends `Strict-Transport-Security: max-age=31536000`; local mode does not | `tests/test_hsts_header.py` 4 |
| Malformed input everywhere | One field at a time replaced by hostile values (huge, negative, NaN, control characters, injection strings), plus whole-request attacks, on every JSON route | `tools/redteam_input_matrix.py`: `round R1: 1727 requests; BROKEN 0, GAP 0, GUARDED 1710, OK 17`; also run as `tests/test_redteam_input_matrix.py` (9 checks) |

Earlier review and attack rounds (r13 to r35, 2026-11-03 to 2026-11-04) are listed in [RED_TEAM_ROUNDS_20261104.md](RED_TEAM_ROUNDS_20261104.md), each with what it found and how it was fixed. Two examples from that file: round r21 found that lookalike characters could slip past the policy pre-screen; round r22 found 44 more evasions and the backend count went from 44 to 0 after the fix.

## How to reproduce

From the project root, after the Run locally setup in the README:

```
PYTHONPATH=src:backend .venv/bin/python3 -B tools/redteam_input_matrix.py --out <an empty folder> --round R1
./tools/run.sh test
```

The first command prints the `round R1: ...` line quoted above and exits non-zero if any request is BROKEN or a GAP. The second runs the whole suite and prints the count.

## What this does NOT show

- It does not show the hosted site is safe against an attacker nobody thought of. The attacks were written by the author and by AI reviewer agents, not by an independent security firm.
- The tests run in-process with fake PayPal and fake model transports. They show our code refuses these requests, not how PayPal Sandbox or Gemini behave under attack.
- The input matrix only sends the attack values it was built with (a fixed list, seeded); a passing run is not a proof about other values.
- Prompt-injection checks cover the phrasings that were tried. The model only picks from closed options and code validates the result, but no test can show that no phrasing works.
- Rate limits and the read budget are counted inside one running server process. A restart, or more than one instance, gives a fresh count.
- The hosted demo sends no Content-Security-Policy that limits scripts, so a script-injection bug would not be blocked by the browser. The session id sits in the tab's sessionStorage, as `SECURITY.md` says.
- Nothing here covers real merchant accounts, real payments or PayPal production; none are supported.
