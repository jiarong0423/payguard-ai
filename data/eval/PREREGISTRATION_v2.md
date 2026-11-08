# Pre-registration: checklist answer key v2 (held-out)

Written before the program was run on any v2 case.

| Item | Value |
| --- | --- |
| File | `data/eval/checklist_answer_key_v2_heldout.json` |
| SHA-256 | `06992da608733341abc33b148b423c1dcc2df75282a09e860ec3af3a3c790cb8` |
| Bytes | 29563 |
| Hash computed (UTC) | 2026-11-08T15:12:21Z (system clock at the moment the file was finalised; not back-dated) |
| Cases | 20 (`HK-01` to `HK-20`); 14 `OFFICIAL_RULE`, 6 `AUTHOR_CONSISTENCY_CHECK` |
| Reasons covered | 9 of 9 in the official table (not received, not as described, unauthorised, credit not processed, duplicate transaction, incorrect amount, payment by other means, canceled recurring billing, other) |
| Boundary / adversarial | due date +1 s and -1 s around the evaluation instant, chargeback stage, unmapped request type, `TEST` tracking number, zero-value refund, unsupported BMP attachment, wrong-type proof |

## Rules followed

1. Expected verdicts were written from the PayPal reason-to-evidence table (transcribed in v1 from the public page; not re-fetched, 0 network requests in this task) and the logic stated in `docs/decisions/2026Q4/policy_engine_v1.md` (structural verdict only; unknown stays unknown).
2. The program was not run on any v2 case before this hash. Lines 1-200 of `src/payguard/dispute_evidence.py` (constants, helpers, snapshot validation) were read to learn the input vocabulary; the proof-record validation and routing code were not read. v1 results, however, were known to the author, so cases HK-06, HK-09, HK-12, HK-18 and HK-19 are variants of themes where v1 already showed behaviour (wrong type, notes/document proof, bad file, unmapped type, placeholder tracking). They are new inputs, not new themes.
3. The key will not be edited after scoring. A key error found later is reported as a key error, not fixed in place. If the file is changed, the hash above stops matching and the report must say so.
4. Verify: `shasum -a 256 data/eval/checklist_answer_key_v2_heldout.json` must equal the value above.
