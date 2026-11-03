# Gemini guide runs, 2026-11-03 (summary)

What was measured: the live guide's model step (Gemini maps a seller sentence to a form item; fixed rules then
validate it and code decides what counts). Each situation used the first 12 funnel requests of its held-out corpus,
scored with `tools/score_replies.py --funnel`. Requests not sent (beyond the 12) count as missed, not as wrong.

Precision here means: of the fields the model filled in, the share that were right. It is not accuracy.

## API round: `gemini-3.8-flash`, 36 calls, 0 errors

Run 2026-11-03 02:30-02:36 (local time), 12 calls per situation (`--limit 12 --max-calls 12`).

| Situation | Format-invalid | Precision | Recall | Confident wrong | Weekday wrong | Attack touched | Latency median / max |
|---|---|---|---|---|---|---|---|
| Policy pre-check (`preflight_v2`) | 0/12 | 1.00 | 0.76 | 0 | 0 | 0 | 5.2 s / 26.2 s |
| Sales spike (`velocity_v2`, prompt 7e49835) | 0/12 | 1.00 | 0.95 | 0 | 0 | 0 | 6.1 s / 65.4 s |
| Dispute evidence (`heldout_v4`) | 0/12 | 1.00 | 0.83 | 0 | 0 (7/8 right) | 0 | 5.1 s / 25.2 s |

## Desktop round (same packets pasted into a Gemini 4 chat; no API call)

| Situation | Format-invalid | Precision | Confident wrong | Weekday wrong | Attack touched |
|---|---|---|---|---|---|
| Policy pre-check | 0/12 | 1.00 | 0 | 0 | 0 |
| Sales spike, round 1 | 0/12 | 0.90 | 2 | 0 | 0 |
| Sales spike, round 2 after fix 7e49835 | 0/12 | 1.00 | 0 | 0 | 0 |
| Dispute evidence | 0/12 | 1.00 | 0 | 0 (8/8 right) | 0 |

Fix 7e49835: in the sales-spike prompt a spike reason counts only when the same clause says sales or orders went up;
an event on its own is dropped by code. Inferred tags dropped by code as designed (desktop round): pre-check 2, sales
spike 4, dispute 6. One hedge was not flagged in pre-check.

## Limits

- 36 API calls in total (12 per situation); a small sample, not a guarantee.
- Recall below 1.00 means some stated facts were not filled in; the guide asks the seller again instead of guessing.
- The model never decides a dispute, a policy question or a PayPal action.
