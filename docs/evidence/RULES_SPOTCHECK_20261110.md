# TradeGlot country-rules and PayPal-clause spot-check, extension, 2026-11-10

**Date note.** The machine clock showed 2026-11-09 during the whole run. Wherever this file says 2026-11-10, that is the label chosen for the draw (it is also the random seed), not a separate calendar date, and no page was read after 2026-11-09 by that clock.

**What this is.** A second, larger sample drawn after judges flagged thin coverage. It extends `RULES_SPOTCHECK_20261108.md` (48 rules) and `PAYPAL_CLAUSES_SPOTCHECK_20261108.md` (24 clauses) with **64 more country rules** and **24 more PayPal clauses**, disjoint from the first draw. Dataset: `paypal_country_rules_v1.json` (rules retrieved 2026-11-02), read-only; nothing in it was modified. Fetch dates: 2026-11-09 and 2026-11-10 (the machine clock showed 2026-11-09 during the run). No PayPal API call, no login, no credential read.

**Who compared.** Every verdict below is **an AI reader's reading** of the located source passage (no human re-read). **Gemini was not run**: the project's Gemini worker needs the owner's Vertex project or API key and bills the owner. A ready-to-paste prompt for the owner was written instead (internal file, see section 6). When the owner returns Gemini's verdicts, they can be added as a second reader next to these rows. A human has not re-read these rows.

## 1. Method and seed

- **Seed `20261110`**, Python `random.Random`. Rules: the 633 rules not drawn on 2026-11-08; 3 export + 3 import per country (sample without replacement inside each country/direction stratum, 60 rules), then 4 more from the remaining pool without stratification = **64**. Clauses: the 116 `snippets` not drawn on 2026-11-08 (the single `ALL` row excluded) in a shuffled order; first 2 per country (20), then the next 4 = **24**. Draw script: `current_runs/20261110_spotcheck_internal/spotcheck_draw_20261110.py` (internal; the seed and method are also stored in the data file).
- **Data files:** `data/country_rules/spotcheck_sample_20261110.json` (the draw: ids, urls, seed, excluded ids) and `data/country_rules/spotcheck_results_20261110.json` (verdicts, depth, short fragments, notes).
- **Coverage of the draw:** rules per country: US 6, CA 6, JP 6, SG 6, HK 7, AU 6, GB 6, DE 7, CN 7, TW 7; both directions in every country. 53 distinct rule URLs and 23 distinct PayPal URLs (76 in total).
- **Fetching.** Each source URL was meant to be requested once, politely. Route: (1) a plain urllib script for 7 pages (4-5 s apart, TLS verification on); (2) an automated web fetcher for the other 46 non-PayPal pages, one request per URL, no retries; (3) PayPal legal pages return HTTP 403 to automated tools (23 of 23), so they were read in the built-in browser pane in a new tab of its own, a few seconds apart, and the tab was closed afterwards. Full page text, fetcher extracts and logs are kept only in an internal folder (not in the repository).
- **Request accounting (honest).** 76 distinct URLs. About 105 requests reached servers: 8 urllib (one URL, govinfo 18 U.S.C. 2320, was fetched twice because the first run went through before the network allow-list was fixed), 69 web-fetcher (23 of them PayPal 403s; Japan Post followed one 301), and 27 browser page loads for the 23 PayPal pages (US and AU buyer-protection, TW seller-protection and UK user agreement were each loaded twice because the first extraction missed the needed text). The first urllib attempt (75 requests) was blocked by the sandbox's network allow-list before leaving the machine; its log is kept as `fetch_log_sandbox_blocked_attempt1.jsonl`.
- **Depth labels.** `full` = the author read the operative text of the fetched page. `extract` = a web-fetcher extract (a small model returned partial quotes plus a summary; very long statutes were read only up to 100,000 characters). `headings` = table of contents only. `none` = nothing readable. Extract-depth rows are weaker evidence than full-depth rows and are counted as compared, as in the first spot-check, but see the limitations.
- **Verdict scale (rules, same as 2026-11-08).** Consistent = every substantive element located. Wording differs = core located, but wording differs or a sub-claim (figure, name, detail) is not on the fetched page. Could not open / verify = page unreadable, a JavaScript shell, image-only, truncated before the passage, or redirected away; not counted as checked. Not consistent = the source contradicts the rule (none found). Clause rows use the 2026-11-08 clause categories plus "Wording differs, meaning same".

## 2. Results for the 64 new rules

| Verdict | New (64) | Earlier (48) | Combined (112) |
|---|---|---|---|
| Consistent | 28 | 34 | 62 |
| Wording differs, meaning consistent | 20 | 10 | 30 |
| Could not open / verify | 16 | 4 | 20 |
| Not consistent | 0 | 0 | 0 |
| **Total sampled** | **64** | **48** | **112** |

Rules actually compared against source text: **48 of 64** new, **92 of 112** combined (44 of 48 earlier). Of the new compared rows, 6 were read at full depth, 40 from web-fetcher extracts and 2 from headings only. **0 rules were found not consistent**, in the new or the combined sample. Coverage: 112 of 681 rules = 16.4 percent.

| Country | New sampled | Consistent | Wording differs | Could not open | Combined sampled (old + new) |
|---|---|---|---|---|---|
| US | 6 | 2 | 0 | 4 | 13 |
| CA | 6 | 6 | 0 | 0 | 10 |
| JP | 6 | 1 | 1 | 4 | 10 |
| SG | 6 | 3 | 3 | 0 | 10 |
| HK | 7 | 1 | 2 | 4 | 12 |
| AU | 6 | 2 | 2 | 2 | 10 |
| GB | 6 | 2 | 4 | 0 | 11 |
| DE | 7 | 4 | 2 | 1 | 12 |
| CN | 7 | 4 | 2 | 1 | 11 |
| TW | 7 | 3 | 4 | 0 | 13 |

### Per-rule record (verdict source: author)

Fragments are short quotes (under 15 words) in the source language.

| # | Rule id | Country | Dir | Source URL | Verdict | Depth | Source fragment | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | AU-EX-GEN-01 | AU | export | https://www.abf.gov.au/importing-exporting-and-manufacturing/exporting/how-to-export/export-requirements | Wording differs, meaning consistent | full | "value of more than AUD2,000" | Declaration trigger and the under-AUD2,000 exemption match (ABF page). "Australia charges no export duty" is not on this page. |
| 2 | AU-EX-PS-02 | AU | export | https://www.abf.gov.au/importing-exporting-and-manufacturing/prohibited-goods/list-of-items | Could not open / verify | none | - | ABF list-of-items page: only 1.6 kB of page chrome in static HTML; the list is not there (same gap as AU-IM-CO-01 on 2026-11-08). |
| 3 | AU-EX-CR-01 | AU | export | https://www.legislation.gov.au/C2004A03252/latest/text | Wording differs, meaning consistent | headings | "9 Unlawful exports" | Federal Register page showed only the Act table of contents (ss. 7, 9, 10: movable cultural heritage, unlawful exports, grant of permits). Body of s. 9-10 not read. |
| 4 | AU-IM-MD-02 | AU | import | https://www.tga.gov.au/products/unapproved-therapeutic-goods/access-pathways/personal-importation-scheme | Consistent | full | "prohibited from being imported under any circumstances" | TGA Personal Importation Scheme page: counterfeit medicines and medical devices. |
| 5 | AU-IM-TB-01 | AU | import | https://www.abf.gov.au/importing-exporting-and-manufacturing/prohibited-goods/list-of-items | Could not open / verify | none | - | Same ABF list-of-items page as AU-EX-PS-02; list body not in static HTML. |
| 6 | AU-IM-RW-02 | AU | import | https://www.acma.gov.au/buying-or-selling-electrical-products | Consistent | full | "the same laws apply to you" | ACMA page: online/post/in-person radio device sellers treated like larger retailers; penalties apply. |
| 7 | CA-EX-PS-01 | CA | export | https://www.canadapost-postescanada.ca/cpc/doc/en/support/non-mailable-matter.pdf | Consistent | full | "The Plant Protection Act and the Convention on International Trade" | Canada Post non-mailable-matter PDF s. 4.10 lists plants, seeds, fruits, bark, plant parts, soil; CFIA Plant Health permit office named. |
| 8 | CA-EX-GEN-03 | CA | export | https://laws-lois.justice.gc.ca/eng/acts/E-19/section-13.html | Consistent | extract | "No person shall export or transfer, or attempt to export" | Export and Import Permits Act s. 13 (web-fetcher extract): Export Control List goods/technology, and goods to Area Control List countries, need a permit. |
| 9 | CA-EX-LA-02 | CA | export | https://laws-lois.justice.gc.ca/eng/regulations/C.R.C.,_c._296/FullText.html | Consistent | extract | (web-fetcher summary of s. 69(1)) | Evidence of importing-country sanitary compliance plus a certificate from a veterinary inspector or endorsed accredited veterinarian. Only 100,000 of 313,611 chars were read; summary, not verbatim. |
| 10 | CA-IM-LA-02 | CA | import | https://laws-lois.justice.gc.ca/eng/acts/W-8.5/section-6.html | Consistent | extract | "No person shall import into Canada any animal or plant that was taken" | WAPPRIITA s. 6(1); parts/derivatives wording from web-fetcher summary. |
| 11 | CA-IM-JW-01 | CA | import | https://laws-lois.justice.gc.ca/eng/acts/E-18.5/FullText.html | Consistent | extract | "was issued by a participant" | s. 14(1): compliant container, Kimberley Process Certificate issued by a participant, not invalidated, accurate. |
| 12 | CA-IM-FD-02 | CA | import | https://laws-lois.justice.gc.ca/eng/regulations/SOR-2018-108/FullText.html | Consistent | extract | "Any food that is imported must have been manufactured" | SFCR s. 11(1) equivalence and s. 13(1)(a) importer name and licence number. |
| 13 | CN-EX-LA-02 | CN | export | https://www.moa.gov.cn/ztzl/gjzwbhgy/flfg/201205/t20120525_2635872.htm | Wording differs, meaning consistent | extract | "向口岸动植物检疫机关报检" | Animal and Plant Quarantine Law art. 20 (declare before export) located. The "isolation at designated sites" part is not in the passages retrieved. |
| 14 | CN-EX-FD-01 | CN | export | https://www.moa.gov.cn/ztzl/gjzwbhgy/flfg/201205/t20120525_2635872.htm | Wording differs, meaning consistent | extract | "向口岸动植物检疫机关报检" | Art. 20 located; the examples "meat products, animal-based pet food" are not named in art. 20. |
| 15 | CN-EX-CU-02 | CN | export | https://www.pbc.gov.cn/tiaofasi/144941/3581332/3582861/2018072309595152720.pdf | Could not open / verify | none | - | PBC regulation PDF is image-only (no text layer); not verified (needs OCR). |
| 16 | CN-IM-WP-01 | CN | import | https://www.gov.cn/zhengce/1993-02/26/content_5723395.htm | Consistent | full | "各种武器、仿真武器、弹药及爆炸物品" | Item 1 of the import-ban list on the gov.cn page. |
| 17 | CN-IM-FD-03 | CN | import | https://www.moa.gov.cn/ztzl/gjzwbhgy/flfg/201205/t20120525_2635872.htm | Consistent | extract | "邮寄进境的动植物" | Arts. 31-32: mail quarantine at the international mail exchange, released if passed, otherwise returned or destroyed. Examples "tea, dried goods" not named. |
| 18 | CN-IM-LA-02 | CN | import | https://www.moa.gov.cn/ztzl/gjzwbhgy/flfg/201205/t20120525_2635872.htm | Consistent | extract | "作退回或者销毁处理" | Art. 29 para. 2: listed items carried or posted in are returned or destroyed. |
| 19 | GD-DE-EX-EC-01 | DE | export | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-in-einen-Nicht-EU-Staat/Einschraenkungen/Waren/waren_node.html | Consistent | extract | "Artenschutz" | Zoll postal-export page lists species protection, dual-use, torture goods, rough diamonds, cultural goods, weapons. The negative claim (no e-cigarette restriction) cannot be proven from a list. |
| 20 | DE-EX-RW-01 | DE | export | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-in-einen-Nicht-EU-Staat/Einschraenkungen/Waren/Dual-Use-Gueter/dual-use-gueter_node.html | Wording differs, meaning consistent | extract | "Solche Güter können beim Versand" | Dual-use page names electronics/telecom/IT, software, and BAFA. The words "Ausfuhrgenehmigung" and Regulation 2021/821 art. 3 are not on the page text retrieved. |
| 21 | GD-DE-EX-TO-01 | DE | export | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-in-einen-Nicht-EU-Staat/Einschraenkungen/Waren/waren_node.html | Consistent | extract | "Artenschutz" | Same Zoll page as GD-DE-EX-EC-01; negative claim not provable from a list. |
| 22 | DE-IM-CU-01 | DE | import | https://www.gesetze-im-internet.de/zollvg/__12a.html | Wording differs, meaning consistent | extract | "binnen einer Frist von 30 Tagen" | ZollVG s. 12a(2): EUR 10,000 and 30-day disclosure located. The page does not mention post or courier; it speaks of unaccompanied cash. |
| 23 | DE-IM-RW-01 | DE | import | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-aus-einem-Nicht-EU-Staat/Einschraenkungen/Waren/Produktsicherheit-und-konformitaet/produktsicherheit-und-konformitaet_node.html | Consistent | extract | "Laserpointer mit einer Leistung von mehr als einem Milliwatt" | Zoll product-safety page: jammers and laser pointers over 1 mW banned; toys and electrical devices must meet safety requirements. |
| 24 | GD-DE-IM-FD-04 | DE | import | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-aus-einem-Nicht-EU-Staat/Einschraenkungen/Waren/Lebensmittel-und-Futtermittel/lebensmittel-und-futtermittel_node.html | Consistent | extract | "im Postversand nicht" | Zoll food page: caviar needs CITES documents; no exemption for small personal quantities by post. |
| 25 | GB-EX-RX-01 | GB | export | https://www.legislation.gov.uk/ukpga/1971/38/section/3 | Consistent | extract | "the exportation of a controlled drug" | Misuse of Drugs Act 1971 s. 3(1)(b) and s. 3(2)(b) (licence of the Secretary of State). Rule says Home Office licence. |
| 26 | GB-EX-LA-02 | GB | export | https://www.gov.uk/guidance/cites-imports-and-exports | Wording differs, meaning consistent | extract | "You must apply for a permit" | GOV.UK CITES page: permit needed to move a specimen into or out of GB; APHA issues permits. It does not say "certificate" or "re-export" in those words in the passages retrieved. |
| 27 | GB-EX-CU-01 | GB | export | https://www.gov.uk/guidance/taking-cash-in-and-out-of-great-britain | Wording differs, meaning consistent | extract | "You must declare cash of £10,000 or more" | Located. Page says "customs authorities", not Border Force. |
| 28 | GB-IM-CO-02 | GB | import | https://www.gov.uk/guidance/import-vat-and-customs-duty-on-gifts | Consistent | extract | "Perfumes with a flashpoint of less than 60°C" | GOV.UK gifts page (updated 2024-10-18): banned from international mail. |
| 29 | GB-IM-LA-03 | GB | import | https://www.gov.uk/bringing-plants-and-wood-into-great-britain/print | Wording differs, meaning consistent | extract | "You’ll need to apply for a permit or certificate" | Plants and wood page: CITES permit, CN22/CN23, Border Force seizure located. The page covers plants; animals are not covered there. |
| 30 | GB-IM-RW-01 | GB | import | https://www.legislation.gov.uk/uksi/2017/1206/contents | Wording differs, meaning consistent | headings | "21. Requirements which must be satisfied before an importer places" | legislation.gov.uk contents list only; reg. 21 body not read. |
| 31 | HK-EX-WP-01 | HK | export | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-exports/index.html | Wording differs, meaning consistent | extract | "air guns and air rifles with muzzle energy greater than 2 joules" | Air guns, stun guns, crossbows over 6 kg, Police licence and TID licence for the Munitions List located. Pepper sprays are not named; page mentions noxious-gas aerosols (dog repellents). |
| 32 | HK-EX-GEN-01 | HK | export | https://www.elegislation.gov.hk/hk/cap60E!en | Could not open / verify | none | - | elegislation.gov.hk Cap. 60E page is a JavaScript shell ("Loading required resource"). |
| 33 | HK-EX-EC-01 | HK | export | https://www.elegislation.gov.hk/hk/cap371!en | Could not open / verify | none | - | elegislation.gov.hk Cap. 371 page is a JavaScript shell. |
| 34 | HK-IM-CU-01 | HK | import | https://www.customs.gov.hk/en/faqs/currency-and-bearer-negotiable-instruments/index.html | Consistent | extract | "an advance electronic declaration must be made" | Customs FAQ: HKD 120,000 per batch as cargo; postal packets excluded. |
| 35 | HK-IM-EC-01 | HK | import | https://www.elegislation.gov.hk/hk/cap60!en | Could not open / verify | none | - | elegislation.gov.hk Cap. 60 page is a JavaScript shell. |
| 36 | HK-IM-FD-03 | HK | import | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-imports/index.html | Wording differs, meaning consistent | extract | "specific legal requirements or administrative arrangements" | Customs page is a link list naming milk, frozen confections, colouring, sweeteners, preservatives, metals; the legal detail is not on the page. |
| 37 | JP-EX-TO-01 | JP | export | https://www.post.japanpost.jp/service/send/oversea/attention/restriction/index.html | Wording differs, meaning consistent | extract | "国別に輸入を禁止している品物がございます" | Japan Post lists tobacco among items often prohibited by destination countries. "Japan does not bar tobacco exports" is not stated on the page. |
| 38 | JP-EX-BH-01 | JP | export | https://www.post.japanpost.jp/service/send/oversea/attention/restriction/index.html | Consistent | extract | "国際航空運送協会（IATA）の「危険物に関する規則」" | Japan Post: IATA dangerous goods cannot be mailed by any service; fireworks, lighter fuel, gas cylinders, matches, bleach, pesticides, mercury, wet batteries listed. Dry ice not seen in the extract (cut off). |
| 39 | JP-EX-CU-02 | JP | export | https://laws.e-gov.go.jp/law/355CO0000000260 | Could not open / verify | none | - | e-Gov law page is a JavaScript shell. |
| 40 | JP-IM-WE-01 | JP | import | https://laws.e-gov.go.jp/law/329AC0000000061 | Could not open / verify | none | - | e-Gov law page is a JavaScript shell. |
| 41 | JP-IM-BH-01 | JP | import | https://laws.e-gov.go.jp/law/336AC0000000234 | Could not open / verify | none | - | e-Gov law page is a JavaScript shell. |
| 42 | JP-IM-CF-01 | JP | import | https://laws.e-gov.go.jp/law/329AC0000000061 | Could not open / verify | none | - | e-Gov law page is a JavaScript shell. |
| 43 | SG-EX-BH-01 | SG | export | https://www.singpost.com/support/sending-an-item/general-prohibition-dangerous-goods | Consistent | extract | "Explosives" | SingPost dangerous-goods page: classes 1-9 with ammunition, aerosols, alcohol/perfume, matches, bleach, pesticides, wet and sealed lead-acid batteries, magnets, dry ice. |
| 44 | SG-EX-GEN-01 | SG | export | https://www.customs.gov.sg/doing-business/export-operations/export-procedures/permit-exemptions/ | Consistent | extract | "unless they are dutiable or controlled" | Singapore Customs permit-exemptions page (updated 2026-02-11): parcel post and air exports up to S$1,000. |
| 45 | SG-EX-CF-01 | SG | export | https://www.customs.gov.sg/doing-business/compliance/border-enforcement-of-intellectual-property-rights/ | Wording differs, meaning consistent | extract | "Are suspected to infringe the registered trade mark, copyright" | Rights-holder notice covers trade mark, copyright, GI and registered design; the ex-officio list names trade mark, copyright and GI only. The rule gives all four for both routes. |
| 46 | SG-IM-TO-01 | SG | import | https://www.hsa.gov.sg/tobacco-regulation/overview/ | Wording differs, meaning consistent | extract | "A valid tobacco licence is required" | HSA page (updated 2026-10-20): SP specification for parcel post, return of non-compliant products, licence. "Dutiable at any value" is not on this page. |
| 47 | SG-IM-FD-01 | SG | import | https://www.sfa.gov.sg/food-import-export/commercial-imports/what-you-need-to-know-for-import-of-food | Consistent | extract | "you must apply for an import permit using TradeNet" | SFA page (updated 2026-09-07): licence or registration, TradeNet permit per consignment, parcel-post receipts counted as commercial import. |
| 48 | SG-IM-BH-01 | SG | import | https://www.singpost.com/support/sending-an-item/general-prohibition-dangerous-goods | Wording differs, meaning consistent | extract | "Explosives" | Same SingPost page as SG-EX-BH-01. The page lists the classes under general "must not be shipped" and does not restate them for inbound mail. |
| 49 | TW-EX-CU-01 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0380131 | Consistent | extract | "以貨物運送、快遞、郵寄或其他相類之方法運送前項各款物品出入境者，亦同" | Anti-Money Laundering Act art. 14 para. 2 (courier or post covered). Thresholds per item are summarised only. |
| 50 | TW-EX-TB-01 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0350072 | Wording differs, meaning consistent | extract | "據實申報物品名稱、數量、價值" | Art. 16 (export parcels declared on mailing documents) contains nothing about tobacco; the negative claim "no restriction found" cannot be verified from this page. |
| 51 | TW-EX-PL-01 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=M0140001 | Consistent | extract | "輸入國要求提出檢疫證明者，輸出人得申請" | Plant Protection and Quarantine Act art. 20. |
| 52 | TW-IM-FD-05 | TW | import | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0350072 | Consistent | extract | "進口六公斤以下之寵物食品，免申請「飼料輸入登記證」" | Art. 14 para. 1 item 1. |
| 53 | G3-TW-IM-BH-03 | TW | import | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0070004 | Wording differs, meaning consistent | extract | "載運危險品之船舶，應符合下列條件" | Ship Act art. 34 has three alternative conditions (older ships, newer ships, ships under 500 GT); the rule states only the classification-society one. |
| 54 | TW-IM-RF-01 | TW | import | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0060146 | Wording differs, meaning consistent | extract | "申請第二級電信管制射頻器材進口者" | Art. 9 located; the extract gives hand-carried 6-10 units, mailed 3-10 units, max 10 a year. The rule's "2 units per shipment without permit" figure was not confirmed in the extract. |
| 55 | US-EX-CF-01 | US | export | https://www.govinfo.gov/link/uscode/18/2320?type=usc&year=mostrecent&link-type=html | Consistent | full | "make, import, export, obtain control of" | 18 U.S.C. 2320(f)(5) definition of traffic; (a)(1) knowing use of a counterfeit mark. 2320 also bars export of prohibited goods. |
| 56 | GA-US-EX-JW-02 | US | export | https://pe.usps.com/text/imm/immc1_013.htm | Consistent | extract | "controlled through the Kimberley Process Certification Scheme" | USPS IMM 134.3 (immc1_013). |
| 57 | US-EX-BH-01 | US | export | https://pe.usps.com/cpim/ftp/pubs/pub52/pub52.pdf | Could not open / verify | none | - | USPS Pub. 52 PDF returned as raw compressed bytes through the fetch tool; not parsed. |
| 58 | US-IM-GEN-05 | US | import | https://www.ecfr.gov/current/title-19/section-134.11 | Could not open / verify | none | - | eCFR returned a 302 to unblock.federalregister.gov; not followed. |
| 59 | US-IM-MD-01 | US | import | https://www.ecfr.gov/current/title-21/section-807.40 | Could not open / verify | none | - | eCFR returned a 302 to unblock.federalregister.gov; not followed. |
| 60 | US-IM-EC-01 | US | import | https://pe.usps.com/cpim/ftp/pubs/pub52/pub52.pdf | Could not open / verify | none | - | Same Pub. 52 PDF; unreadable. |
| 61 | GA-DE-IM-BH-02 | DE | import | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R1542 | Could not open / verify | none | - | EUR-Lex page is 478,636 chars; the fetch read the first 100,000 (recitals only), so arts. 3(1)(47) and 55(2) were not reached. |
| 62 | TW-IM-RX-02 | TW | import | https://www.fda.gov.tw/Tc/newsContent.aspx?cid=4&id=t623657 | Wording differs, meaning consistent | extract | "管制藥品不得郵寄或快遞" | TFDA page states the rule; the cited art. 16 of the Controlled Drugs Act is not named on the page. |
| 63 | HK-EX-CO-01 | HK | export | https://www.elegislation.gov.hk/hk/cap640!en | Could not open / verify | none | - | elegislation.gov.hk Cap. 640 page is a JavaScript shell. |
| 64 | CN-IM-CU-01 | CN | import | https://www.gov.cn/zhengce/1993-02/26/content_5723395.htm | Consistent | extract | "国家货币" | Restricted import item 4 on the gov.cn page (it says 国家货币, not 人民币). |

## 3. Results for the 24 new PayPal clauses

Pinned date = `effective_date` stored in the row; page date = date shown on the page when read (verdict source: author).

| # | Clause id | Page date | Verdict | Source fragment | Notes |
|---|---|---|---|---|---|
| 1 | GB-buyer_protection_exclusions-1 | 12 Oct 2026 | Incomplete | "Payments made using PayPal Payouts" | Every item of the row is on the page; the page also lists "payments that you have not sent using your PayPal account", which the row omits. |
| 2 | DE-cross_border_currency-1 | 4. November 2026 | Page newer, content still consistent | "Sofortzahlung auf Ihr Bankkonto" | Standard bank transfer and instant payment to a linked bank account on the page. Page date newer than the pinned 2026-09-07; only the withdrawal passage compared. |
| 3 | JP-aup_prohibited-2 | 2022年11月2日 | Consistent | (none of the searched terms appear) | Page is ~3 kB; no entry for animals, plants, seeds, food, cosmetics, batteries or hazardous goods; general-law duty present. |
| 4 | TW-seller_protection_proof-1 | Jan 26, 2026 | Wording differs, meaning same | "two days after PayPal notified you" | All proof elements located (2 days, 7 days, tracking, ship/delivery date). Page asks for city, country or postal code; the row says city/state or postcode. Page date newer than pinned 2025-12-11. |
| 5 | CA-seller_protection_proof-1 | January 26, 2026 | Consistent | "no later than two days after PayPal notified you" | All elements located, including "city/province, city/country, or postal/zip code". |
| 6 | CA-aup_prohibited-1 | November 2, 2022 | Wording differs, meaning same | "narcotics, steroids, certain controlled substances" | Items (a)-(k) match. "Selling items not yet owned" was not found by keyword search on this page. |
| 7 | SG-seller_protection_proof-1 | 26 January 2026 | Wording differs, meaning same | "two days after PayPal notified you" | Same as TW row: city, country or postal code wording differs slightly from the row. |
| 8 | DE-seller_protection-1 | 17. Juli 2025 | Wording differs, meaning same | "an eine andere Adresse weitergeleitet" | Redirected-parcel loss of coverage located and the date matches. The Germany-address condition and the claim types were not checked (keyword search missed them). |
| 9 | TW-seller_protection_guest_checkout-1 | Jan 26, 2026 | Page newer, content still consistent | "registered in the following countries" | Taiwan is not on the exclusion list, so the row holds. Page date newer than pinned 2025-12-11. |
| 10 | GB-dispute_process-1 | 12 October 2026 | Not located (not counted as checked) | - | User agreement page opened (148,756 chars, date matches); keyword searches for the liability, response-time and chargeback passages found nothing. Not counted as checked. |
| 11 | US-buyer_protection_exclusions-1 | January 26, 2026 | Incomplete | "Real estate, including residential property." | Row items located; the page adds payments initiated through a third-party platform with the account/routing number, and PayPal World QR payments. The list was read to its 17th item only. |
| 12 | CN-seller_protection_proof-1 | January 26, 2026 | Wording differs, meaning same | "no later than two days after PayPal notified you" | Same wording difference as TW row (city, country or postal code). |
| 13 | AU-buyer_protection_exclusions-1 | 1 July 2024 | Incomplete | "Payments that you have not sent using your PayPal account" | AU page also excludes in-person pickup for Significantly Not as Described claims, which the row attributes to INR only. |
| 14 | SG-dispute_process-1 | 28 May 2026 | Wording differs, meaning same | "the card issuer, not PayPal, will determine who wins" | Card-issuer decision and reversal/chargeback hold language located. Seller liability and the "answer within the timeframe PayPal communicates" wording were not located on this page. |
| 15 | HK-aup_prohibited-1 | 2 November 2022 | Wording differs, meaning same | "narcotics, steroids, certain controlled substances" | Same text as the CA page: items (a)-(k) match; "not yet owned" not found by keyword search. |
| 16 | JP-dispute_process-1 | 2026年5月28日 | Consistent | "PayPalではなく、カード発行会社が" | Seller liable for the full reversed amount plus fees; must answer PayPal within the notified period; card issuer decides chargebacks. |
| 17 | AU-cross_border_currency-1 | 5 October 2026 | Consistent | "Any PayPal balance in US Dollars may be withdrawn to a US bank account" | Convert to AUD for withdrawal; USD to a linked US bank with a fee. |
| 18 | US-seller_protection-1 | January 26, 2026 | Incomplete | "The primary address for your PayPal account must be in the United States" | Unauthorized and INR cover, US address and redirect rule located. The page limits Unauthorized cover to PayPal-hosted environments and excludes INR chargebacks filed with the card issuer; the row omits both. |
| 19 | HK-holds_reserves-1 | 28 May 2026 | Not located (not counted as checked) | "PayPal may limit the payment methods available" | Payment review and holds are described, but no "up to 30 days" hold period was found in the passages searched (the 30 days that appear concern unclaimed payments and pending orders). Candidate inconsistency; needs a full read. |
| 20 | CN-aup_prohibited-2 | 2022年11月2日 | Consistent | (none of the searched terms appear) | c2 page was served in Chinese here; no entry for animals, plants, seeds, food, cosmetics, batteries or hazardous goods. |
| 21 | DE-aup_prohibited-1 | 17. Juli 2023 | Consistent | "Zigaretten" | Items (a)-(k) and "noch nicht verfügt" located. |
| 22 | CA-privacy-1 | October 12, 2026 | Consistent | "PayPal Canada Co. MaRS Centre West Tower" | Contact table lists PayPal Canada Co., Toronto; PIPEDA is not named on the page. |
| 23 | GB-seller_protection-1 | 12 October 2026 | Wording differs, meaning same | "one of the countries to which this user agreement applies" | Redirect rule and Unauthorized/INR located. The named list (UK, Guernsey, Isle of Man, Jersey) is not on the page text read. |
| 24 | DE-buyer_protection-1 | 15. April 2025 | Consistent | "innerhalb von 180 Tagen" | 180 days to open, 20 days to escalate; no 30-day limit found; 15 April 2025 change notice present. |

| Clause verdict | New (24) | Earlier (24) | Combined (48) |
|---|---|---|---|
| Consistent | 8 | 14 | 22 |
| Page newer, content still consistent | 2 | 1 | 3 |
| Wording differs, meaning same | 8 | 0 | 8 |
| Incomplete | 4 | 5 | 9 |
| Inconsistent | 0 | 3 | 3 |
| Could not open | 0 | 0 | 0 |
| Not located (not counted as checked) | 2 | 1 | 3 |
| **Total sampled** | **24** | **24** | **48** |

Clauses compared: **22 of 24** new, **45 of 48** combined (earlier: 23 of 24). No clause was found inconsistent in the new sample. Coverage: 48 of 140 clauses = 34.3 percent. All ten countries are in the new draw; `cross_border_currency` is now covered (it was not drawn on 2026-11-08), `aup_preapproval` was not drawn this time, so all 12 dimensions are covered across the two drawings.

## 4. Inconsistencies and proposed fixes (rules pack not edited)

No rule or clause was found to contradict its source. Proposed wording or citation fixes, by id:

**Rules** (trim the claim, or add a citation to the page that supports it):
- HK-EX-WP-01: "pepper sprays" is not named on the cited Customs page (it names noxious-gas aerosols such as dog repellents); cite the Cap. 238 text or drop the word.
- SG-EX-CF-01: registered designs appear only on the rights-holder-notice route; the ex-officio route names trade mark, copyright and geographical indication.
- GB-IM-LA-03: the cited GOV.UK page covers plants and wood; add the animal-side source or narrow the sentence.
- AU-EX-GEN-01: "Australia charges no export duty" is not on the cited ABF page.
- SG-IM-TO-01: "dutiable at any value" is not on the cited HSA page; cite Singapore Customs for the duty point.
- SG-IM-BH-01: the SingPost page does not restate the dangerous-goods classes for inbound mail; cite the page for importing goods.
- G3-TW-IM-BH-03: Ship Act art. 34 has three alternative conditions; the rule gives only the classification-society one.
- JP-EX-TO-01 and TW-EX-TB-01: both are negative claims ("does not bar", "no restriction found") that the cited page neither states nor tests; word them as "no restriction was found on the cited page".
- CN-EX-LA-02 and CN-EX-FD-01: art. 20 only requires declaration before export; the isolation-site sentence and the meat/pet-food examples come from other articles or are the author's examples.
- DE-EX-RW-01, DE-IM-CU-01, GB-EX-LA-02, GB-EX-CU-01, TW-IM-RX-02, TW-IM-RF-01: minor, cited page does not carry one word or figure of the rule ("Ausfuhrgenehmigung"; post/courier; "certificate"; "Border Force"; art. 16 of the Controlled Drugs Act; the 2-unit figure was not visible in the extract).

**Clauses:**
- HK-holds_reserves-1: the page read does not show an "up to 30 days" risk-hold period (searched hold/30 days; found payment-review language and unrelated 30-day items). Candidate inconsistency; needs a full read of the Hong Kong user agreement before it is cited.
- GB-buyer_protection_exclusions-1, US-buyer_protection_exclusions-1, AU-buyer_protection_exclusions-1: the shared exclusion sentence reads as complete but the pages add items (payments not sent from the PayPal account; US third-party-platform and PayPal World QR payments); AU also excludes picked-up items for Significantly Not as Described. Add "and other items listed on the page" or the missing items.
- US-seller_protection-1: add that Unauthorized cover applies only in a PayPal-hosted environment and that Item Not Received claims filed directly with the card issuer are not covered (same finding as AU-seller_protection-1 on 2026-11-08).
- GB-dispute_process-1: not located on the page read; re-check with a full read.

Fixes already listed on 2026-11-08 (US-IM-LA-02, TW-EX-JW-03, AU-EX-BT-02, GD-DE-EX-PS-01 and the CN/SG source-citation items) are not repeated.

## 5. Combined totals for README / numbers

- Rules sampled: **112 of 681** (48 + 64); compared **92** (44 + 48); **0 not consistent**; wording-level differences **30**; could not open **20**.
- Clauses sampled: **48 of 140** (24 + 24); compared **45**; inconsistent **3** (all minor, from 2026-11-08; none new); incomplete **9**; wording differs **8**; not located **3**.
- All ten countries appear in both samples; the combined rule sample covers every country with at least 10 rules.

## 6. Gemini status

Not run (it needs the owner's Vertex project or key and costs the owner money; no other model was substituted). An internal prompt file (not published, about 80 kB) lists all 88 items: Part A carries the page text the author fetched, Part B lists the items whose page text is unavailable (the PayPal pages, whose text was read in the browser but not saved, and the unreadable pages); the owner pastes it into Gemini himself and can paste the replies back to be recorded as a second reader.

## 7. Limitations

- **Sample size.** 112 of 681 rules (16.4 percent) and 48 of 140 clauses (34.3 percent). With no contradiction in the compared rules, an error rate for the population still cannot be stated confidently; most rules remain individually unverified.
- **Single reader, no Gemini.** All verdicts are one agent's reading; no second reader and no human re-read.
- **Extract-depth evidence.** 42 of the 48 compared new rules rest on web-fetcher extracts (partial quotes and summaries by a small model) or headings, not on a full read of the page. Treat those as located rather than proven.
- **Not verified: 16 of 64 new rules** (JS-rendered e-Gov and elegislation pages, image-only PBC PDF, USPS Pub. 52 PDF, eCFR redirect, ABF list page, EUR-Lex truncated before the articles). Dynamic or client-rendered pages remain the largest systematic gap.
- **One-page comparison.** Each item was checked only against its cited URL; a sub-claim supported elsewhere is marked "wording differs", not confirmed. Negative claims cannot be proven from one page.
- **PayPal pages.** Read in the browser as served to the reader (language and variant by locale: the Taiwan seller-protection page and the C2 acceptable-use page were served in English/Chinese respectively); regional variants were not compared. Keyword windows were read, not the full agreements, so passages missing from a window are reported "not located", never "inconsistent".
- **Currency.** Pages as read on 2026-11-09/10; several are living pages and newer than the dates pinned in the dataset (TW seller protection, DE user agreement).
- **Scope.** Transcription fidelity only, not legal advice or legal sufficiency.

