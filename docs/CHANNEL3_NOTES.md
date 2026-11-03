# Channel3 notes: optional category signal and product reference card (off by default)

Status (2026-11-01): the category signal is tested with a fake transport only. The product reference card made its
first real calls on 2026-11-01: 5 searches, all HTTP 200, the live reply matched the SDK-derived parser
(`docs/evidence/channel3_receipts_v1.json`; recordings in `backend/app/data/channel3_recorded_v1.json`).

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
- `channel3_sdk/client.py`: the SDK reads `CHANNEL3_API_KEY` by default (PayGuard uses the same name).
- `channel3_sdk/categories/raw_client.py`: `GET v1/categories/search` with query params `query`, `limit`; documented error statuses 401, 402, 422 and 500.
- `channel3_sdk/types/search_categories_response.py`, `category_summary.py`, `category_ref.py`: response shape.
- `channel3_sdk/products/raw_client.py`, `types/search_response.py`, `types/product.py`: product search, for reference.

## Endpoint PayGuard uses

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

PayGuard chose this endpoint over product search (`POST /v1/search`, body `{"query", "limit" (default 20, max 30), "filters", "config", "page_token"}`, response `{"products": [Product], "next_page_token"}` where `Product.category` is a `CategorySummary`). Category search sends the same single query string, but it returns only category labels: no merchants, prices, images or buy URLs to drop.

## PayGuard contract

The adapter is `backend/app/channel3.py`, and the route is `POST /api/v1/aup/category-signal`.

- **Construction**: `build_channel3_adapter(env=None, *, force_off=False)` is the single factory that `create_app` uses. `force_off=True` (for example, a demo mode) disables it whatever the environment says.
- **Enabled** only when `PAYGUARD_CHANNEL3=enabled` *and* `CHANNEL3_API_KEY` is non-empty. Anything else means off, and off makes zero outbound calls.
- **Outbound**: only the sanitised product name goes out. The adapter takes the first line of the description, folds it to ASCII and caps it at 120 characters. It strips emails, @handles, URLs, digit runs longer than four (separators included, so phone and card numbers go) and capitalised names after "for"/"to". If fewer than two letters remain, nothing is sent (`NOT_SENT`).
- **Key**: sent only in `x-api-key`. It is never logged, returned, put in an exception message or shown in `repr`.
- **Limits**: 4 s timeout, no redirects, no retry, response body capped at 64 KiB. A per-process budget allows 20 calls, and failed calls count against it.
- **Inbound**: the reply is reduced to the closed contract `{category: str|null, confidence: "HIGH"|"LOW"|null, source: "channel3"}`. Unknown provider fields are dropped. A malformed reply, an unexpected title character or any drift becomes `UNAVAILABLE / contract_rejected`.
- **Confidence** is PayGuard's own label, because Channel3 returns no score. It is `HIGH` when the top category is the only result or shares its root category with the runner-up, otherwise `LOW`.
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
