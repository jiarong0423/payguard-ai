# What is inside the Internal Review ZIP

Step 03 can download one ZIP for the human reviewer ("Internal Review ZIP"). It is built in the browser from the reviewed draft by `frontend/src/reviewZip.js`, checked again before download, and never sent anywhere. It is for the person who approves the case; it is not the file PayPal receives.

**Seven entries, always in this set** (`INTERNAL_REVIEW_ZIP_CONTENTS`):

| Entry | What it holds | Size in the fixture run |
| --- | --- | --- |
| `README.txt` | Classification (internal review only), "advisory only", "provider submission: not performed", "dispute decision: not made" | 1,442 bytes |
| `manifest.json` | Name, size and SHA-256 of every other entry, so a change is visible | 2,629 bytes |
| `requirements.json` | What PayPal asked the seller to provide, and whether each item is present | 2,053 bytes |
| `timeline.json` | Dated events (order, shipping, delivery, claim opened) in order, with the gaps between them | 652 bytes |
| `public-sources.json` | The official PayPal references the checks cite | 1,559 bytes |
| `pseudonymized-evidence.json` | The evidence summary with identifiers replaced; no raw identifiers or attachment bytes | 915 bytes |
| `product-reference.json` | The product the seller confirmed from the Channel3 catalogue (or "not confirmed"); never prices, shops or links | 360 bytes |

**How this list was made.** `buildInternalReviewFiles` was run on the synthetic draft in `tests/frontend_zip_contract.mjs` (`validDraft`), and the names, byte sizes and hashes were read from its output. Sizes change with the case. `node tests/frontend_zip_contract.mjs` asserts that the entry names are exactly these seven, that the manifest matches the files, and that a changed or extra entry is refused.

**What the ZIP deliberately does not hold:** restricted originals, raw attachments, raw identifiers, restricted proof values and attachment bytes. The README inside says so in its own words.
