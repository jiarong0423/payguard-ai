# Channel3 notes: optional category signal and product reference card (off by default)

Status (2026-11-01): the category signal is tested with a fake transport only. The product reference card made its
first real calls on 2026-11-01: 5 searches, all HTTP 200, the live reply matched the SDK-derived parser
(`docs/evidence/channel3_receipts_v1.json`; recordings in `backend/app/data/channel3_recorded_v1.json`).

Second run (2026-11-09): 5 more real searches with a new key (bamboo cutting board, cotton bath towel set, portable Bluetooth speaker, ceramic plant pot, women's running shoes), all HTTP 200 with 3 cards each, 1.1 to 2.1 seconds. Receipts (time, status, latency, card count, SHA-256 of the raw reply; no key, no raw reply): `docs/evidence/channel3_receipts_20261109.json`. These calls were not added to the hosted demo's recorded replies, so the hosted demo still replays only the 2026-11-01 recordings. Ten real searches in total.

Update (2026-11-04): Channel3's documentation is now at https://channel3.ai/docs and was read there. Its pricing
page (https://channel3.ai/docs/pricing) lists 1000 free credits every month, `/search` at 1 credit per call and
`/categories` free. The contract
below was not re-derived from the new pages; recheck it against them before relying on it.

## Where the facts come from

The documentation hosts (`docs.trychannel3.com`, `trychannel3.com`) were not reachable from the
build environment on 2026-11-01. The proxy refused the connection, so no page was read. The
contract below comes from the **official Python SDK, `channel3-sdk` 4.0.0**, downloaded from
PyPI. Fern generates that SDK from Channel3's API definition. Recheck it against the live docs
before you rely on it.

| Source | URL | What it gave |
| --- | --- | --- |
| PyPI package page | https://pypi.org/project/channel3-sdk/4.0.0/ | SDK version, README (auth header) |
| SDK repository (linked from PyPI) | https://github.com/channel3-ai/channel3-python-sdk | generated client and types |
| Docs site named in the SDK README | https://channel3.docs.buildwithfern.com | not read (unreachable) |
| Docs guides (found by web search) | https://docs.trychannel3.com/guides/search.md, https://docs.trychannel3.com/guides/product.md | not read on 2026-11-01 (unreachable); search snippets mention `x-api-key` and `POST /v1/search`. The docs now live at https://channel3.ai/docs |

The SDK files each fact came from:

- `channel3_sdk/environment.py`: base URL `https://api.trychannel3.com`.
- `channel3_sdk/core/client_wrapper.py`: `headers["x-api-key"] = api_key`.
- `channel3_sdk/client.py`: the SDK reads `CHANNEL3_API_KEY` by default (TradeGlot uses the same name).
- `channel3_sdk/categories/raw_client.py`: `GET v1/categories/search` with query params `query`, `limit`; documented error statuses 401, 402, 422 and 500.
- `channel3_sdk/types/search_categories_response.py`, `category_summary.py`, `category_ref.py`: response shape.
- `channel3_sdk/products/raw_client.py`, `types/search_response.py`, `types/product.py`: product search, for reference.

## Endpoint TradeGlot uses

```
GET https://api.trychannel3.com/v1/categories/search?query=<sanitised name>&limit=3
x-api-key: <CHANNEL3_API_KEY>
accept: application/json
```

Response (`SearchCategoriesResponse`), with categories ordered by relevance:

```json
{
  "categories": [
    {
      "slug": "mugs",
      "title": "Mugs",
      "path": [{"slug": "kitchen", "title": "Kitchen"}, {"slug": "mugs", "title": "Mugs"}],
      "has_children": false
    }
  ]
}
```

- `slug: str`, `title: str`, `has_children: bool`, `path: list[{slug, title}] | null` (root first; the last entry is the category itself).
- **There is no score or confidence field.**

TradeGlot chose this endpoint over product search (`POST /v1/search`, body `{"query", "limit" (default 20, max 30), "filters", "config", "page_token"}`, response `{"products": [Product], "next_page_token"}` where `Product.category` is a `CategorySummary`). Category search sends the same single query string, but it returns only category labels: no merchants, prices, images or buy URLs to drop.

## TradeGlot contract

The adapter is `backend/app/channel3.py`, and the route is `POST /api/v1/aup/category-signal`.

- **Construction**: `build_channel3_adapter(env=None, *, force_off=False)` is the single factory that `create_app` uses. `force_off=True` (for example, a demo mode) disables it whatever the environment says.
- **Enabled** only when `PAYGUARD_CHANNEL3=enabled` *and* `CHANNEL3_API_KEY` is non-empty. Anything else means off, and off makes zero outbound calls.
- **Outbound**: only the sanitised product name goes out. The adapter takes the first line of the description, folds it to ASCII and caps it at 120 characters. It strips emails, @handles, URLs, digit runs longer than four (separators included, so phone and card numbers go) and capitalised names after "for"/"to". If fewer than two letters remain, nothing is sent (`NOT_SENT`).
- **Key**: sent only in `x-api-key`. It is never logged, returned, put in an exception message or shown in `repr`.
- **Limits**: 4 s timeout, no redirects, no retry, response body capped at 64 KiB. A per-process budget allows 20 calls, and failed calls count against it.
- **Inbound**: the reply is reduced to the closed contract `{category: str|null, confidence: "HIGH"|"LOW"|null, source: "channel3"}`. Unknown provider fields are dropped. A malformed reply, an unexpected title character or any drift becomes `UNAVAILABLE / contract_rejected`.
- **Confidence** is TradeGlot's own label, because Channel3 returns no score. It is `HIGH` when the top category is the only result or shares its root category with the runner-up, otherwise `LOW`.
- **Decision isolation**: the route needs a live AUP evaluation of the same description (`evaluation_id` plus a description digest check). It reads that evaluation but never modifies it. Every response carries `affects_decision: false`. The AUP response, its findings and the acknowledgement flow are unchanged.
- **UI**: under the AUP result, "Category signal (Channel3): <category> · <high|low> confidence", or "Category lookup off" when disabled.

Route response:

```json
{"status": "OFF" | "SIGNAL" | "NOT_SENT" | "UNAVAILABLE",
 "signal": {"category": "...", "confidence": "HIGH", "source": "channel3"} | null,
 "reason": null | "nothing_to_send" | "budget_exhausted" | "timeout" | "upstream_error" | "contract_rejected",
 "affects_decision": false}
```

## Making one real call later

From the repository root, after creating a key in the Channel3 dashboard. `read -rs` keeps the key
out of shell history and off the screen:

```sh
read -rs CHANNEL3_API_KEY && export CHANNEL3_API_KEY && PAYGUARD_CHANNEL3=enabled PYTHONPATH=src:backend .venv/bin/python3 -c "from app.channel3 import Channel3CategoryAdapter as A; print(A().lookup('Handcrafted ceramic coffee cup'))"; unset CHANNEL3_API_KEY
```

Expected output is one line like
`{'status': 'SIGNAL', 'signal': {'category': 'Mugs', 'confidence': 'HIGH', 'source': 'channel3'}, 'reason': None, 'affects_decision': False}`.
`UNAVAILABLE / upstream_error` usually means the key was rejected (401) or the plan needs payment (402).
`contract_rejected` means the live reply differs from the SDK-derived shape above; update this note
and the parser together.

To see it in the console instead, export the key the same way and start the app with
`PAYGUARD_CHANNEL3=enabled ./tools/run.sh console`.

## Product reference card (seller-confirmed, goes into the review ZIP)

Added 2026-11-01. Contract from the official SDK `channel3-sdk` 4.6.0 (`products/raw_client.py`
`search`, `types/search_response.py`, `types/product.py`). The first real calls (2026-11-01, see the
status at the top) matched it.

```
POST https://api.trychannel3.com/v1/search
x-api-key: <CHANNEL3_API_KEY>
{"query": "<sanitised name>", "limit": 3}
```

- Adapter `backend/app/channel3_products.py`; routes `POST /api/v1/aup/product-reference` and
  `POST /api/v1/aup/product-reference/confirm`, both bound to a live AUP evaluation of the same text.
- Each product is reduced to a closed card: `product_id`, `title`, `brand`, `category`, up to 4
  `key_features`, up to 4 `materials`, one https `image_url`. Offers, prices, shops, buy URLs,
  ratings and unknown fields are dropped.
- The seller picks "This is my product" or "None of these". Only a card the server showed this
  session for this evaluation can be confirmed; the client cannot supply a card.
- A confirmation becomes `product-reference.json`, the seventh fixed file of the review ZIP
  (`NOT_CONFIRMED` when there is none). It records what the item is, for an item-not-as-described reply.
- Same flag, key handling, timeout (6 s), per-process budget (20), no retry and no redirects as the
  category signal. It never changes the AUP decision (`affects_decision: false`).
- Hosted demo: no outbound call. It replays `backend/app/data/channel3_recorded_v1.json`, written by
  `tools/record_channel3.py` from real calls, and labels the cards as recorded with the recording time.
  The file holds the five recordings made on 2026-11-01; with an empty file the demo would show the lookup as off.
- Receipts of the real calls (time, HTTP status, latency, card count, sha256 of the raw reply; no key,
  no raw reply) go to `docs/evidence/channel3_receipts_v1.json`.

## Category call attempt (2026-11-09)

Four real calls to `GET /v1/categories/search` (the optional category signal) were made with the project's own adapter, using the same API key that had worked for product search earlier that day. All four came back **HTTP 403** (about 0.6 s each), which the adapter reports as UNAVAILABLE / `upstream_error`. The documented error statuses for this endpoint are 401, 402, 422 and 500, so a 403 is not explained by the documentation we read; we did not find out why and did not retry (the receipts are in `docs/evidence/channel3_category_receipts_20261109.json`: query, time, status, latency, reply hash; no key and no reply body). The category signal therefore has no successful live call to show. The Channel3 product card (product search) does: see `channel3_receipts_20261109.json`.

## Category tree check against PayPal's AUP (local experiment, 2026-11-09; the 191 matching categories are published, the rest is not)

What was done: the Channel3 category tree (`GET /v1/categories`, 11,861 categories, read once) was compared with the items on PayPal's US Acceptable Use Policy page ("Last updated on November 4, 2026"). Each category got a category-level hint: it matches an AUP item (for example "medical devices", "prescription items", "dealers in jewels and precious metals"), it depends on the actual product, or it is not on the page's lists. A hint is PayPal's rule for taking payment on its service. It is not a legal judgement: cigarettes, for example, are legal to sell in many countries while PayPal's policy still lists them as prohibited on its service, and the page says its approval list is not exhaustive.

How: a Python word filter picked candidate categories, three Claude reviewers who did not see each other's answers and two other-vendor models (DeepSeek, Qwen) voted on 2,203 of them, a narrow 3-of-5 majority that would overturn our own label was not forced and went to a "needs human" area, and the doubtful ones were checked against official lists (US FDA device classification, a government list of class-2 devices allowed for online sale, US tariff schedule, marketplace policy pages). About 190 categories (under 2%) matched an AUP item or depend on the product. 9,658 categories were never reviewed by a model; a 700-category sample of the filtered-out part found 3 that were actually listed (0.43%, 95% upper bound 1.25%), so a few may be missed.

What is published: [channel3_category_aup_hints_20261109.csv](evidence/channel3_category_aup_hints_20261109.csv), 191 category paths (1.6% of the 11,861) with the AUP item each one matched or, for 17, the question to ask the seller, plus how many of the five readers agreed. Category names are Channel3's; Channel3 is credited as their source. The author decided to publish this small part on 2026-11-09 before Channel3 had answered the email asking about it (Section 7 of the Publisher Terms, effective November 2, 2026, prohibits caching or redistributing a significant portion of the catalog or Customer Output and does not mention the taxonomy). It will be removed if Channel3 asks. What is not published: the full category tree, the table of the other 11,670 categories and the per-reader votes. No Channel3 data was used to train or fine-tune any model; category names were only sent to models for classification at inference time.

How it is used: as a reviewer reference table, read next to the AUP page; the console's AUP check runs on its own rules.

How to read the CSV: a row is a hint for a person to check, not a ruling. `agreement` shows how many of five readers (three Claude reviewers plus DeepSeek and Qwen) chose the item; "3 of 5 readers (weakest)" rows are the least certain, and "2+ independent sources agree" rows were matched against official lists instead of a vote. Whether a real product falls under the item depends on what it does, so ask the seller when unsure.

Limits: the reviewers read names only, not products; all three of those reviewers are Claude models; and the AUP reference pinned in this repository is older than the page (see the README limits).
