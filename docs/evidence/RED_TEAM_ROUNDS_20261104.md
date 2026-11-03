# Red-team and stress-test rounds (2026-11-03 to 2026-11-04)

This file records the review and attack rounds run against the development branch before the public sync. Each round was run by independent reviewer agents with fixed roles (judge, PayPal developer relations, sponsor panel, security engineer, UI/UX) or by attack agents (backend matrix, desktop browser, real Android phone). Every finding was re-checked by the author before it was counted, and every fix was followed by the full test suite. Earlier review rounds of individual branches are not summarised here.

Nothing in these rounds called PayPal Live, a paid model, or a real payment. Backend attacks ran in-process against a clean checkout with a mocked PayPal transport; browser and phone attacks ran against an isolated rules-only copy of the console with PayPal not configured.

## What each round found and what happened to it

| Round | Kind | Scope | Found | Outcome |
| --- | --- | --- | --- | --- |
| r13 | Five-role review | First public-sync candidate | Country verdict shown green for a postal ban; rule pack described as PayPal's own; hosted demo session budget exhaustible | Fixed (amber postal-ban verdict, honest pack labels, no Run all on the hosted demo) |
| r14 | Verification | r13 fixes | Over-broad postal-ban match; public test run missing two corpora | Fixed |
| r15 | Verification | r14 fixes | No P0 or P1 left in the developer's scope | Closed |
| r16 | Five-role review | Whole build | Review before the first country check could still draft; four injection phrasings passed; case deadlines hidden | Fixed |
| r17 | Re-review | r16 fixes | The new injection patterns refused 6 of 12 ordinary seller sentences | Fixed (patterns anchored to the addressed form; ordinary sentences kept as must-pass tests) |
| r18 | Judge reading the private repo | README after the first doc update | Country rules below the fold; stale test count | Fixed |
| r19 | Line-by-line, five roles | About 427 sentences in README, quickstart and notes | 43 wrong and 44 stale sentences, counted per reviewer | 66 fix entries and 15 items left unchanged with a reason (owner wording, UI code outside the doc pass, or not visible on the local build). Several fix entries cover one sentence flagged by two or three roles; the record does not reconcile 87 with 66 + 15 item by item, so that split is unverified |
| r20 | Fresh reviewers with no memory + phone click-through | Same build, new eyes | A country stop could be cleared by a re-check with no goods ticked (documented as advisory); phone layout and dashboard issues | UI and doc fixes; country-check binding recorded as an open owner decision |
| r21 | Attack: backend matrix (143 cases), desktop (38 sequences), phone (28 sequences) | Multi-round request sequences, adversarial UI use | Policy pre-screen evaded by combining marks and lookalikes; reported PayPal speech counted as the seller's evidence; stale country result after Reset; Back reloading the page on phones | Fixed; 13 backend findings to 2, both the then-accepted shared session budget |
| r22 | Attack: backend (119 cases), desktop (33), phone (36) | New angles and verification of r21 | 44 pre-screen evasions (glued, split, leet, synonyms); guide over-reading; country amount not bound to the invoice; dashboard focus and keyboard trap | Fixed; backend 44 to 0; phone 15 of 15 previous fixes confirmed on the device |
| r23 | Attack: backend (traffic layer focus), desktop (23), phone (22) | The new hosted traffic limits | One address could stall every visitor through queued session requests; store-wide limit too small; wait time not shown on 429/503; pre-screen false positives on ordinary retail wording | Fixed; traffic findings to 0, pre-screen false positives 30 to 0 and misses 27 to 0 on the attack lists |
| r24 | Five-role review with external evidence + competitor scan | Private branch, owner decisions | Webhook verification must forward the event unchanged; provide-evidence needs a status and link check; hop count of the hosting proxy undocumented; stale wording | Fixed in commit 653111a (webhook event forwarded unchanged, provide-evidence status and link check, proxy hop count configurable and logged without addresses), pinned in `tests/test_paypal_r24.py`, `tests/test_api.py` (`test_webhook_event_is_forwarded_byte_for_byte`) and `tests/test_traffic.py` (hop tests); owner decisions listed separately |

## Reproduce it yourself

The fixes from these rounds are pinned as tests that run with `./tools/run.sh test`:

| Test | What it holds |
| --- | --- |
| `tests/test_redteam_input_matrix.py` | Malformed and hostile requests across every route: 0 broken, 0 gaps (the run prints the request count) |
| `tests/test_attack_r22.py` | Pre-screen evasions, guide over-reading, country amount and currency binding |
| `tests/test_attack_r23_aup.py` | Ordinary retail wording passes; prohibited items and evasions raise a review signal; worst-case input under 50 ms |
| `tests/test_traffic.py` | Per-visitor pacing, bounded queue, session limits, configurable proxy hop, hop log without addresses |
| `tests/test_api.py` (classes `R21*`) | Accent and lookalike folding, PayPal-reported speech, reset isolation, wait-time messages |
| `tests/frontend_attack_r21_console.mjs`, `frontend_attack_r22_console.mjs`, `frontend_attack_r23_console.mjs`, `frontend_attack_r23_secondary.mjs` | Console, dashboard and evidence-page fixes from the browser and phone rounds |

## Known limits after these rounds

- The policy pre-screen is a keyword screen that asks a person to review; it is not a classifier and it does not decide anything. Some ambiguous words (for example a bare "replica" or "casino") still raise a review signal on purpose.
- The country check is advisory and the seller declares the goods; the server holds the draft only while a stop is on record for that session.
- The hosting proxy's X-Forwarded-For hop count is not documented by the host; the hosted demo logs hop counts (never addresses) so the setting can be confirmed after deploy.
- No evidence has been submitted to a live PayPal Sandbox dispute; the provide-evidence path is built and gated but only previewed.
