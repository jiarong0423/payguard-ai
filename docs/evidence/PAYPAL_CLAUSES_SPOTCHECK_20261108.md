# PayPal clause spot-check (24 of 140 rows), 2026-11-08

Scope: the `snippets` array (140 paraphrased PayPal clauses) of `paypal_country_rules_v1.json` (dataset `retrieved_at` 2026-11-02). Read-only. No data file or other project file was changed; this is the only file written. No PayPal API call, no login, no credentials read.

## 1. Method, seed, limits

- Draw: Python `random.Random(20261108)`; shuffle the 140 row indexes; take the first 2 rows seen for each of the 10 country files (US, GB, DE, JP, SG, AU, CA, CN, HK, TW = 20 rows); then add the next 4 rows of the shuffled order (any country). The single `ALL` row (developer.paypal.com disputes overview) was not drawn.
- Coverage: all 10 country files; 11 of the 12 dimensions (seller_protection, seller_protection_guest_checkout, seller_protection_proof, buyer_protection, buyer_protection_exclusions, holds_reserves, aup_prohibited, aup_preapproval, dispute_process, user_agreement, privacy); cross_border_currency was not drawn.
- Overlap with the earlier panel review (8 rows: US user agreement 1, US holds_reserves 1, US aup_preapproval 1, US aup_prohibited 1, US buyer_protection 1, US seller_protection 1, US seller_protection_proof 1, JP holds_reserves 1): 2 of the 24 were also in that set (rows 7 and 24 below). 22 rows are outside it (row 4 was only mentioned there as a side note, not one of the 8 sampled).
- Source pages: opened in the built-in browser as an ordinary reader, page text compared against the stored paraphrase with keyword extraction (not a full line-by-line read of the very long user agreements). Fetch date for every row: 2026-11-08. Tool-level 403 on automated fetch was not retried; the browser was used from the start.
- Requests: 20 distinct paypal.com URLs, 23 page loads in total. Three pages were loaded twice by mistake (DE acceptable use, AU seller protection, DE user agreement) because a first extraction did not capture the needed text. This breaks the "one fetch per URL" rule by 3 loads; total stayed under the 40 limit.
- Limits: only the clauses and keywords listed were compared. Pages were read in the language and variant served to this browser session (English for the `c2` pages, local language for DE, JP, TW). Whether a page text differs by visitor region was not tested. "Source fragment" is a short quote, not a full citation. Rows not located on the page are reported as such and are NOT counted as checked.
- Verdict labels: Consistent = 一致; Wording differs, meaning same = 措辭有差但意思一致; Page newer, content still consistent = 來源頁面日期較新（內容仍一致）; Incomplete = 不完整; Inconsistent = 不一致; Could not open = 無法開啟; Not located = 未核到 (extra label, not counted as checked).

## 2. Drawn rows (in draw order)

AU-holds_reserves-1, CA-buyer_protection-1, CN-buyer_protection_exclusions-1, US-dispute_process-2, CA-holds_reserves-1, JP-seller_protection_guest_checkout-1, US-seller_protection_proof-1, AU-seller_protection-1, GB-seller_protection_guest_checkout-1, HK-seller_protection_guest_checkout-1, CN-aup_prohibited-1, JP-seller_protection_proof-1, GB-buyer_protection-3, SG-aup_prohibited-1, DE-dispute_process-1, HK-seller_protection-1, DE-aup_preapproval-1, TW-holds_reserves-1, TW-aup_preapproval-1, SG-user_agreement-1, CN-privacy-1, US-seller_protection_guest_checkout-1, AU-seller_protection_guest_checkout-1, US-holds_reserves-1.

## 3. Results

Pinned = `effective_date` stored in the row. Page date = date the page itself showed on 2026-11-08.

| # | Row | Pinned / page date | Verdict | Source fragment (page) | Note |
|---|---|---|---|---|---|
| 1 | AU-holds_reserves-1 | 2026-10-05 / 5 Oct 2026 | Consistent | "usually held for up to 21 days" | 180-day retention on account closure also on page. |
| 2 | CA-buyer_protection-1 | 2026-01-26 / Jan 26, 2026 | Consistent | "whichever is sooner" (30 days from delivery vs 180) | 180-day INR and 20-day escalation also on page. |
| 3 | CN-buyer_protection_exclusions-1 | 2026-01-26 / Jan 26, 2026 | Incomplete | "Payments that you have not sent using your PayPal account" | Row omits this ineligible item; the other 17 listed items match the page. |
| 4 | US-dispute_process-2 | 2026-09-14 / Nov 4, 2026 | Incomplete (and page date newer) | "ratio of all Item Not Received and Significantly Not as Described claims" | Page also says total claims include chargebacks/reversals and exclude Unauthorized claims; High Volume tier at 1.5% and more than 100 sales; row omits these. Page text itself words the ratio two ways. See section 5. |
| 5 | CA-holds_reserves-1 | 2026-06-10 / Jun 10, 2026 | Consistent | "generally remain in place for up to 21 days" | Rolling and minimum reserves both on page. |
| 6 | JP-seller_protection_guest_checkout-1 | 2026-01-26 / 2026年1月26日 | Consistent | 米国、英国、ドイツ、カナダ、ブラジル、またはメキシコで登録 | Japan is not in the list, so the row's inference holds. |
| 7 | US-seller_protection_proof-1 | 2026-01-26 / Jan 26, 2026 | Consistent | "no later than two days after PayPal notified you" | Tracking, dates, address match, INR needs delivery, 7-day recommendation all on page. (Also in the earlier review.) |
| 8 | AU-seller_protection-1 | 2025-01-13 / 13 Jan 2025 | Inconsistent (minor) | "You receive payment via PayPal from a buyer's PayPal account" | "Redirected parcels lose coverage" is not on the AU page (searched redirect/different address: no hit). Card-issuer INR exclusion and PayPal-hosted-environment limit are also not in the row. Unauthorized + INR covered, SNAD excluded, no primary-address clause: match. |
| 9 | GB-seller_protection_guest_checkout-1 | 2026-10-12 / 12 Oct 2026 | Consistent | "ineligible ... registered in the following countries" | UK is not on the page's list. |
| 10 | HK-seller_protection_guest_checkout-1 | 2026-01-26 / 26 Jan 2026 | Consistent | "Singapore, China, Hong Kong, Australia, Italy" | Hong Kong is on the exclusion list. |
| 11 | CN-aup_prohibited-1 | 2022-11-02 / Nov 2, 2022 | Incomplete | "Last updated on November 2, 2022" | Listed items match the page, but the row reads as complete and omits: third-party personal information, annuities/lottery contracts, currency exchange/check cashing, credit repair/insurance, bribery, high-fraud-risk products, activity needing pre-approval without it. |
| 12 | JP-seller_protection_proof-1 | 2026-01-26 / 2026年1月26日 | Inconsistent (minor) | 「取引の詳細」ページに記載されている配送先住所と一致する | The row says the address needs "at least city/state or postcode"; the JP page has no such line (the US page does). Other elements (online tracking, ship/delivery date, 2 days, 7 days) match. Row text is identical to the US row. |
| 13 | GB-buyer_protection-3 | 2026-10-12 / 12 Oct 2026 | Consistent | "The seller has provided proof of delivery." | Applies to Item Not Received. The row's comparison to the US page ("proof of shipment or delivery") was not checked in this run. |
| 14 | SG-aup_prohibited-1 | 2022-11-02 / 2 Nov 2022 | Incomplete | "Last updated on 2 November 2022" | Same omissions as row 11 (page text identical to the c2 page). |
| 15 | DE-dispute_process-1 | 2026-09-07 / 4. November 2026 | Not located (page date newer) | "Letzte Aktualisierung 4. November 2026" | Page opened and searched in German for seller liability for reversals, PayPal response timeframe and card-issuer decision; the specific wording was not found by keyword search. Not counted as checked. |
| 16 | HK-seller_protection-1 | 2026-01-26 / 26 Jan 2026 | Incomplete | "primary address for your PayPal account must be in Hong Kong" | Core claims match. Omits: Unauthorized cover only in a PayPal-hosted environment; INR filed directly with the card issuer is not eligible. |
| 17 | DE-aup_preapproval-1 | 2023-07-17 / 17. Juli 2023 | Consistent | "(nicht abschließende Aufzählung)" | All 18 categories present; the row does not carry the "not exhaustive" caveat. |
| 18 | TW-holds_reserves-1 | 2026-05-28 / 2026年5月28日 | Consistent | 最多持續 30 天 | Tracking-upload early release and longer hold during a dispute also on page. |
| 19 | TW-aup_preapproval-1 | 2022-11-02 / 2022年11月2日 | Consistent | （清單並非詳盡無遺） | All 18 categories present; the row does not carry the "not exhaustive" caveat. |
| 20 | SG-user_agreement-1 | 2026-05-28 / 28 May 2026 | Consistent | "contract between you and PayPal Pte. Ltd." | "Same agreement as other Pte. Ltd. markets" is only partly corroborated (the TW page names the same entity); identical text was not compared. |
| 21 | CN-privacy-1 | 2026-10-12 / Oct 12, 2026 | Inconsistent (minor) | "Last updated on October 12, 2026" | No mainland-China entry in the contact table and no PIPL mention (keyword search): match. But the row says the statement is "in Chinese"; the c2 page was served in English here. Korea-only claim not exhaustively tested. |
| 22 | US-seller_protection_guest_checkout-1 | 2026-01-26 / Jan 26, 2026 | Consistent | "accounts registered in all other countries are otherwise eligible" | US is not on the exclusion list. |
| 23 | AU-seller_protection_guest_checkout-1 | 2025-01-13 / 13 Jan 2025 | Consistent | "Singapore, China, Hong Kong, Australia, Italy" | Australia is on the exclusion list. |
| 24 | US-holds_reserves-1 | 2026-09-14 / Nov 4, 2026 | Page newer, content still consistent | "generally remain in place for up to 21 days" | 10% / 90-day rolling reserve example and "up to 180 days" hold both found. Only the holds/reserves text was compared, not the whole revision. (Also in the earlier review.) |

### Counts (24 rows)

| Verdict | Rows |
|---|---|
| Consistent | 14 |
| Wording differs, meaning same | 0 |
| Page newer, content still consistent | 1 (row 24) |
| Incomplete | 5 (rows 3, 4, 11, 14, 16) |
| Inconsistent (all minor) | 3 (rows 8, 12, 21) |
| Could not open | 0 |
| Not located (not counted as checked) | 1 (row 15) |

Also flagged as "page date newer" on top of the main verdict: rows 4 and 15. Rows genuinely checked: 23 of 24. This is a 24-row sample of 140; it does not support a claim about the other 116 rows.

## 4. Pinned-date disclosure

Page date = what the page showed on 2026-11-08. Pinned = `effective_date` stored for that URL in all rows (single value per URL in the file).

| Page (URL path under paypal.com) | TradeGlot pin | Page shows | Status |
|---|---|---|---|
| /us/legalhub/paypal/acceptableuse-full | 2022-10-29 | Last updated on November 4, 2026 | STALE (newer page) |
| /us/legalhub/paypal/useragreement-full | 2026-09-14 | Last updated on November 4, 2026 | STALE (newer page) |
| /de/legalhub/paypal/useragreement-full | 2026-09-07 | Letzte Aktualisierung 4. November 2026 | STALE (newer page) |
| /us/legalhub/paypal/seller-protection | 2026-01-26 | January 26, 2026 | Match |
| /jp/legalhub/paypal/seller-protection | 2026-01-26 | 2026年1月26日 | Match |
| /au/legalhub/paypal/seller-protection | 2025-01-13 | 13 January 2025 | Match |
| /hk/legalhub/paypal/seller-protection | 2026-01-26 | 26 January 2026 | Match |
| /uk/legalhub/paypal/seller-protection | 2026-10-12 | 12 October 2026 | Match |
| /uk/legalhub/paypal/buyer-protection | 2026-10-12 | 12 October 2026 | Match |
| /ca/legalhub/paypal/buyer-protection | 2026-01-26 | January 26, 2026 | Match |
| /c2/legalhub/paypal/buyer-protection | 2026-01-26 | January 26, 2026 | Match |
| /au/legalhub/paypal/useragreement-full | 2026-10-05 | 5 October 2026 | Match |
| /ca/legalhub/paypal/useragreement-full | 2026-06-10 | June 10, 2026 | Match |
| /tw/legalhub/paypal/useragreement-full | 2026-05-28 | 2026年5月28日 | Match |
| /sg/legalhub/paypal/useragreement-full | 2026-05-28 | 28 May 2026 | Match |
| /c2/legalhub/paypal/acceptableuse-full | 2022-11-02 | November 2, 2022 | Match |
| /sg/legalhub/paypal/acceptableuse-full | 2022-11-02 | 2 November 2022 | Match |
| /tw/legalhub/paypal/acceptableuse-full | 2022-11-02 | 2022年11月2日 | Match |
| /de/legalhub/paypal/acceptableuse-full | 2023-07-17 | 17. Juli 2023 | Match |
| /c2/legalhub/paypal/privacy-full | 2026-10-12 | October 12, 2026 | Match |

Findings:
- Three of 20 opened pages are newer than the pin: US acceptable use, US user agreement, DE user agreement. The US acceptable use pin is 2022-10-29 while the page shows a 2026-11-04 date; the US acceptable use 18-category pre-approval list still matched the stored list when I read it, but the prohibited list on the page is longer than the row paraphrase (rows 11 and 14 show the same pattern in other countries).
- The dataset `retrieved_at` (2026-11-02) is before the 2026-11-04 revision, so rows pinned to those three pages are not re-read against the new text. What changed on 2026-11-04 is unknown (old text not kept).
- Pages not opened in this run (no claim made): GB user agreement and acceptable use, DE seller and buyer protection, JP/HK/AU/CA/TW user agreement variants other than those listed, all other privacy pages, c2 user agreement (pinned 2026-06-30), US buyer protection and seller protection beyond what is listed above, and the TW seller-protection page (pinned 2025-12-11).

## 5. Known incomplete or imprecise rows (flagged only; data file not changed)

Source for items A and B: the earlier panel review. I re-read the relevant page text myself where noted.

A. Seller Protection summary rows omit exclusion conditions.
- Re-read on US, JP, AU and HK pages (all four show it): Unauthorized Transaction cover applies only to transactions "in an environment hosted by PayPal"; Item Not Received claims that buyers file with their card issuer are not eligible; the item must be a physical, tangible good (intangible goods and QR payments carry extra conditions); for Unauthorized claims the payment must be flagged "eligible" or "partially eligible" on the transaction page; PayPal decides eligibility "in its sole discretion"; the US/JP ineligible-transaction list also covers items sent after PayPal advised not to release, personal (friends-and-family) payments, Payouts, and others.
- Reported by the panel review, not re-verified here: seller can be suspended from the program.
- Affected rows from this sample: row 8 (AU), row 16 (HK); the same pattern is expected in the other `seller_protection` rows (US, JP, others) but those were not individually checked in this run.

B. Dispute-fee sentence (row 4, US-dispute_process-2).
- Row says "fee tier depends on the INR/SNAD claim ratio". The user agreement page words it two ways: one sentence says the ratio of Item Not Received and Significantly Not as Described claims to sales over the previous three calendar months; a later sentence says total claims are all claims except Unauthorized Transaction claims, plus chargebacks and reversals. High Volume tier applies at a dispute ratio of 1.5% or more with more than 100 sales in the prior three full months. The row leaves out the thresholds and the chargeback/reversal inclusion. Page date is newer (2026-11-04) than the row pin (2026-09-14).

C. Rows where the stored text states something the opened page does not show (minor):
- Row 8 (AU): "redirected parcels lose coverage" not on AU page.
- Row 12 (JP): "at least city/state or postcode" not on JP page.
- Row 21 (CN privacy): "in Chinese" not what the c2 page showed in this session.

D. Lists that read as complete but are not: rows 3 (one ineligible item missing), 11 and 14 (several prohibited categories missing). The acceptable-use pre-approval lists (rows 17, 19) are complete on categories but the "not exhaustive" caveat is not carried in the row text.

E. Not located: row 15 (DE-dispute_process-1). Needs a manual read of the German user agreement section on buyer protection and chargebacks.
