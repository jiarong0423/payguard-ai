# TradeGlot country-rules spot-check, 2026-11-08

**Method.** Dataset: `paypal_country_rules_v1.json` (schema `payguard.country_rules.v1`, rules retrieved 2026-11-02), read-only. It holds 681 import/export rules (10 countries x export and import). From these, 48 rules were drawn with Python `random.Random(20261108)`, stratified: 2 export + 2 import rules per country (`sample` without replacement inside each country/direction stratum, 40 rules), then 8 more drawn from the remaining 641 rules without stratification. Every country therefore has at least 4 rules, with both directions present. For each rule, the rule's own `url` (an official government or postal-operator page) was fetched once, converted to plain text, and the rule text was compared with the matching passage. Fetch date for all rows: **2026-11-08**. Network: 42 distinct URLs, 51 HTTP requests in total (42 first attempts + 9 retries after a transient error; no URL needed more than one retry), 4-5 s between requests, plain urllib with TLS verification on. The comparison was done by the reviewing agent reading the located source passage, not by an automated matcher; a human has not re-read these rows. Nothing in the data file was modified.

**Verdict scale.** Consistent = every substantive element of the rule was located in the source. Wording differs = the core was located, but wording differs or a sub-claim (figure, name, detail) is not on the fetched page. Source changed/not found and Not consistent were available but no row received them. Could not open = the page could not be read or its body was not retrievable; these are not counted as checked.

**Sampled rule ids (48):** CN-EX-WP-01, G2-CN-EX-BH-01, CN-IM-AL-01, CN-IM-MD-01, TW-EX-CF-01, G2-TW-EX-RX-01, TW-IM-GEN-01, TW-IM-CR-02, US-EX-JW-01, US-EX-LA-01, US-IM-RX-02, US-IM-LA-02, CA-EX-GEN-01, CA-EX-MD-01, CA-IM-RW-01, CA-IM-EC-02, JP-EX-WE-03, JP-EX-AL-01, JP-IM-LA-02, JP-IM-BH-03, SG-EX-AL-02, GD-SG-EX-MD-02, SG-IM-CU-01, SG-IM-GEN-01, HK-EX-RX-04, HK-EX-TB-01, HK-IM-FD-02, HK-IM-JW-01, AU-EX-FD-03, AU-EX-BT-02, AU-IM-CO-01, AU-IM-GEN-01, GA-GB-EX-CO-02, GA-GB-EX-BH-02, GB-IM-JW-01, GB-IM-LA-01, DE-EX-CR-02, GD-DE-EX-PS-01, GD-DE-IM-FD-02, DE-IM-GEN-05, GB-IM-GEN-02, US-IM-EC-02, HK-IM-BT-02, US-EX-TB-01, US-EX-EC-01, G2-TW-IM-GEN-01, TW-EX-JW-03, DE-EX-JW-01

## Summary

| Verdict | Rules |
|---|---|
| Consistent (一致) | 34 |
| Wording differs, meaning consistent (措辭有差但意思一致) | 10 |
| Could not open / verify (無法開啟) | 4 |
| Source changed or not found (來源已變更或找不到) | 0 |
| Not consistent (不一致) | 0 |
| **Total sampled** | **48** |

Rules actually compared against source text: 44 of 48. Of these, 2 were compared against headings or a table of contents only (SG-IM-CU-01, AU-EX-FD-03), so full-text comparison covers 42.

| Country | Export | Import | Consistent | Wording differs | Could not open |
|---|---|---|---|---|---|
| US | 4 | 3 | 6 | 1 | 0 |
| CA | 2 | 2 | 4 | 0 | 0 |
| JP | 2 | 2 | 3 | 0 | 1 |
| SG | 2 | 2 | 1 | 3 | 0 |
| HK | 2 | 3 | 5 | 0 | 0 |
| AU | 2 | 2 | 1 | 2 | 1 |
| GB | 2 | 3 | 3 | 0 | 2 |
| DE | 3 | 2 | 4 | 1 | 0 |
| CN | 2 | 2 | 2 | 2 | 0 |
| TW | 3 | 3 | 5 | 1 | 0 |

## Per-rule record

Quotes are fragments of the source text (15 words / 15 characters or fewer) in the source language. Depth: full = operative text read; headings only = contents list only.

| # | Rule id | Country | Dir | Source URL | Verdict | Depth | Source fragment | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | CN-EX-WP-01 | CN | export | https://www.gov.cn/zhengce/1993-02/26/content_5723395.htm | Consistent | full | "列入禁止进境范围的所有物品" | Export-ban list item 1 points back to the import-ban list, whose item 1 is weapons, imitation weapons, ammunition, explosives. |
| 2 | G2-CN-EX-BH-01 | CN | export | https://www.caac.gov.cn/PHONE/XWZX/MHYW/201406/t20140613_13807.html | Consistent | full | "仍然不允许航空邮寄任何锂电池" | Wh and lithium-content limits and the "China Post had no procedure" statement all located (CAAC news item, 2014-06-13). |
| 3 | CN-IM-AL-01 | CN | import | https://www.gov.cn/zhengce/1993-02/26/content_5723395.htm | Wording differs, meaning consistent | full | "烟、酒" | Alcohol listed as a restricted import (item 2). The "1,500 ml traveller allowance" in the rule text is not on this page, so it is unverified here. |
| 4 | CN-IM-MD-01 | CN | import | https://www.mfa.gov.cn/web/wjb_673085/zzjg_673183/bjhysws_674671/bhflfg/ldbjglxgfl/202303/P020230313589081879122.pdf | Wording differs, meaning consistent | full | "合理数量为限" | Customs Law art. 46 (own use, reasonable quantity) located. The "RMB 2,000 parcel limit" and the "no device-specific restriction" negative claim are not in this PDF and cannot be verified from it. |
| 5 | TW-EX-CF-01 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070001 | Consistent | full | "販賣或意圖販賣而持有" | Art. 97 (sale, possession for sale, export/import; online included) and art. 75 (customs notify on suspected infringement) located. |
| 6 | G2-TW-EX-RX-01 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0050021 | Consistent | full | "鴉片、嗎啡及其他麻醉物品" | Art. 37 item 6 with the permit / court-evidence / abroad-medical exceptions. |
| 7 | TW-IM-GEN-01 | TW | import | https://www.etax.nat.gov.tw/etwmain/tax-info/network-transaction-taxtation-area/consumer/oversea-online-shopping-notice | Consistent | full | "2,000元以內者，免徵關稅" | Source is the Ministry of Finance e-tax guidance page, not the statute text; the NT$2,000 exemption and tobacco/alcohol/quota exclusions match. |
| 8 | TW-IM-CR-02 | TW | import | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0170001 | Consistent | full | "應事先向主管機關提出申請" | Cultural Heritage Preservation Act art. 74. |
| 9 | US-EX-JW-01 | US | export | https://www.ecfr.gov/current/title-31/section-592.201 | Consistent | full | "controlled through the Kimberley Process Certification Scheme" | 31 CFR 592.201(a). |
| 10 | US-EX-LA-01 | US | export | https://pe.usps.com/cpim/ftp/pubs/pub52/pub52.pdf | Consistent | full | "Most live or dead animals are nonmailable in international mail" | Pub. 52 s. 641 (Aug 2026 edition) lists bees, leeches, silkworms, Drosophila flies, dried insects/reptiles, beneficial insects. 2.9 MB PDF; section found by text search. |
| 11 | US-IM-RX-02 | US | import | https://www.ecfr.gov/current/title-21/section-1312.11 | Consistent | full | "A separate permit or declaration is required for each shipment" | 21 CFR 1312.11(a)-(c): permit for Schedule I-II/narcotics, import declaration for others. |
| 12 | US-IM-LA-02 | US | import | https://www.ecfr.gov/current/title-42/section-71.51 | Wording differs, meaning consistent | full | "CDC dog import permit means a document issued by CDC" | Rule ties the permit to "dog-rabies high-risk countries". The regulation requires a foreign rabies vaccination/microchip form and designated airports for high-risk countries, and defines the permit for "DMRVV-restricted" countries. Wording conflates the two tiers. |
| 13 | CA-EX-GEN-01 | CA | export | https://laws-lois.justice.gc.ca/eng/regulations/SOR-2005-23/FullText.html | Consistent | full | "commercial goods having a value of less than $2,000 Canadian" | s. 6(b), "if the goods are not restricted goods", subject to s. 8. |
| 14 | CA-EX-MD-01 | CA | export | https://laws-lois.justice.gc.ca/eng/acts/F-27/section-37.html | Consistent | full | "Conditions under which exports exempt" | s. 37(1): export-only products exempt with a certificate of compliance with destination law. |
| 15 | CA-IM-RW-01 | CA | import | https://laws-lois.justice.gc.ca/eng/acts/R-2/section-4.html | Consistent | full | "for which a technical acceptance certificate is required" | s. 4(2) located; s. 4(3) standards clause read in the same fetch. |
| 16 | CA-IM-EC-02 | CA | import | https://laws-lois.justice.gc.ca/eng/regulations/SOR-2021-123/FullText.html | Consistent | full | "must not contain nicotine in a concentration that exceeds 20 mg/mL" | s. 4(1); s. 5 packaging prohibition also located. |
| 17 | JP-EX-WE-03 | JP | export | https://www.post.japanpost.jp/service/send/oversea/attention/restriction/index.html | Consistent | full | "花火、クラッカー、弾薬" | Japan Post list of items that cannot be sent by international mail (explosives class). |
| 18 | JP-EX-AL-01 | JP | export | https://www.post.japanpost.jp/service/send/oversea/attention/restriction/index.html | Consistent | full | "アルコール濃度24％を超えるもの" | Alcoholic beverages above 24% listed as unmailable. |
| 19 | JP-IM-LA-02 | JP | import | https://laws.e-gov.go.jp/law/326AC1000000166 | Could not open / verify | none | - | Page returned HTTP 200 but only an 800-byte JavaScript shell (e-Gov law search); article text is rendered client-side and was not retrievable without a browser. Not verified. |
| 20 | JP-IM-BH-03 | JP | import | https://www.customs.go.jp/tetsuzuki/c-answer/imtsukan/1801_jr.htm | Consistent | full | "高圧ガス保安法 高圧ガス" | Customs page cites Customs Law art. 70 and lists the other-law approvals (High Pressure Gas Safety Act, Poisonous and Deleterious Substances Act, Agricultural Chemicals Regulation Act). Page is Shift_JIS. |
| 21 | SG-EX-AL-02 | SG | export | https://www.customs.gov.sg/doing-business/export-operations/export-procedures/permit-exemptions/ | Wording differs, meaning consistent | full | "unless they are dutiable or controlled" | Page says parcel post is exempt from an export permit unless dutiable or controlled. It does not name liquor; "liquor is dutiable" is inference from outside this page. |
| 22 | GD-SG-EX-MD-02 | SG | export | https://www.hsa.gov.sg/medical-devices/manufacturing-import-and-supply/dealers-licence/ | Wording differs, meaning consistent | full | "You need a dealer's licence if you manufacture, import or wholesale" | Licence requirement matches (HSA page, updated 2026-03-13). The "applications go through SHARE" detail is not in the static page text. |
| 23 | SG-IM-CU-01 | SG | import | https://sso.agc.gov.sg/Act/CDTOSCCBA1992 | Wording differs, meaning consistent | headings only | "CROSS BORDER MOVEMENTS OF PHYSICAL CURRENCY AND BEARER NEGOTIABLE INSTRUMENTS" | Only the Act table of contents (Part 6A; s. 60 reports about cross border movements; s. 62 reports about receipts of cash from outside Singapore) was visible in the fetched HTML. Section bodies were not retrieved, so the duty to report is consistent with the headings but not read in full. |
| 24 | SG-IM-GEN-01 | SG | import | https://www.customs.gov.sg/doing-business/import-operations/import-procedures/importing-by-postal-or-courier-service/ | Consistent | full | "value not exceeding S$400" | GST relief only for post/air, CIF up to S$400, excluding liquor and tobacco; none for sea/land. Page updated 2026-02-17. |
| 25 | HK-EX-RX-04 | HK | export | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-exports/index.html | Consistent | full | "36 types Chinese herbal medicines" | Export of proprietary Chinese medicines and 36 listed herbal medicines needs a Department of Health licence. |
| 26 | HK-EX-TB-01 | HK | export | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-exports/index.html | Consistent | full | "Export of these commodities requires a licence from the Customs and Excise Department" | Removal permits also required. |
| 27 | HK-IM-FD-02 | HK | import | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-imports/index.html | Consistent | full | "in an amount not exceeding 15 kg" | Import licence per consignment from FEHD; 15 kg personal-baggage exemption. |
| 28 | HK-IM-JW-01 | HK | import | https://www.customs.gov.hk/en/service-enforcement-information/trade-controls/kimberley/index.html | Consistent | full | "a registration system for rough diamond traders" | Page confirms registration + certification system administered by TID. Short page; certificate name not spelled out beyond "certification system". |
| 29 | AU-EX-FD-03 | AU | export | https://www.legislation.gov.au/F1996B03403/latest/text | Wording differs, meaning consistent | headings only | "Exportation of goods specified in Schedule 4 (toothfish)" | Only the regulation table of contents was visible; reg. 6 operative text was not read. Consistent with the heading, not verified in full. |
| 30 | AU-EX-BT-02 | AU | export | https://auspost.com.au/personal/sending/sending-guidelines/dangerous-prohibited-items | Wording differs, meaning consistent | full | "You cannot send lithium batteries to Bhutan, Germany, Italy, Laos, Macao or Thailand" | Courier prohibition and recalled/damaged battery prohibition also located. The "loose batteries" phrase in the rule was not matched verbatim (page allows installed batteries only, max two batteries or four cells). |
| 31 | AU-IM-CO-01 | AU | import | https://www.abf.gov.au/importing-exporting-and-manufacturing/prohibited-goods/list-of-items | Could not open / verify | none | - | ABF list-of-items page returned HTTP 200 but the list body is not in the static HTML (no mention of cosmetics or lead). Not verified. |
| 32 | AU-IM-GEN-01 | AU | import | https://www.abf.gov.au/buying-online/buying-online | Consistent | full | "over AUD1000, you will need to fill out an Import Declaration" | Content found embedded in page JSON (page updated 2026-10-20). Tobacco/alcohol excluded from the low-value rule. |
| 33 | GA-GB-EX-CO-02 | GB | export | https://help.royalmail.com/personal/s/article/Prohibited-and-restricted-items-personal-customer-guidelines | Could not open / verify | none | - | TLS certificate verification failed for help.royalmail.com in this environment (one retry, same error). Verification was not disabled. Not verified. |
| 34 | GA-GB-EX-BH-02 | GB | export | https://help.royalmail.com/personal/s/article/Prohibited-and-restricted-items-personal-customer-guidelines | Could not open / verify | none | - | Same URL and same TLS failure as GA-GB-EX-CO-02. Not verified. |
| 35 | GB-IM-JW-01 | GB | import | https://www.legislation.gov.uk/ukpga/1973/43/section/1 | Consistent | full | "applies to an unhallmarked article a description" | Hallmarking Act 1973 s. 1(1)(a)-(b). |
| 36 | GB-IM-LA-01 | GB | import | https://www.gov.uk/bringing-pet-animals-to-great-britain/print | Consistent | full | "You can bring up to 5 pets to Great Britain" | Extra rules for sale/rehoming, more than 5 animals, wild/exotic/endangered; invasive species barred. |
| 37 | DE-EX-CR-02 | DE | export | https://www.zoll.de/DE/Fachthemen/Verbote-Beschraenkungen/Schutz-des-Kulturgutes/Nationales-Kulturgut/nationales-kulturgut_node.html | Consistent | full | "bedarf einer Genehmigung (§§ 22, 23" | Zoll page also states export is barred while listing is pending (s. 21 no. 1 KGSG). |
| 38 | GD-DE-EX-PS-01 | DE | export | https://www.gesetze-im-internet.de/pflbeschv/__17.html | Wording differs, meaning consistent | full | "§ 17 Pflanzengesundheitszeugnisse nach Artikel 100 Absatz 1" | Para. 1 located; para. 4 (inspection) not separately checked. |
| 39 | GD-DE-IM-FD-02 | DE | import | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-aus-einem-Nicht-EU-Staat/Einschraenkungen/Waren/Lebensmittel-und-Futtermittel/lebensmittel-und-futtermittel_node.html | Consistent | full | "Kleinmengen von bis zu 5 kg frischer Erzeugnisse oder 2 kg sonstiger Erzeugnisse" | Small-quantity exemption wording matches (Zoll page). |
| 40 | DE-IM-GEN-05 | DE | import | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-aus-einem-Nicht-EU-Staat/Einschraenkungen/Waren/Produktsicherheit-und-konformitaet/produktsicherheit-und-konformitaet_node.html | Consistent | full | "Ausschließlich diese entscheidet, ob ein Produkt eingeführt werden darf" | Customs refers to market surveillance, which decides release/return/destruction. |
| 41 | GB-IM-GEN-02 | GB | import | https://www.gov.uk/goods-sent-from-abroad/print | Consistent | full | "Non-excise goods worth £135 or less No charge" | Customs Duty above GBP 135 and on excise goods; duty base includes postage, packaging, insurance. |
| 42 | US-IM-EC-02 | US | import | https://www.govinfo.gov/link/uscode/21/387j?type=usc&year=mostrecent&link-type=html | Consistent | full | "Premarket review required" | 21 U.S.C. 387j(a): new tobacco product (not marketed by 2007-02-15) needs a premarket order. |
| 43 | HK-IM-BT-02 | HK | import | https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/prohibited-articles/controlled-imports/index.html | Consistent | full | "import of any waste requires a permit issued by the Department" | Waste batteries named as an example of hazardous waste (Waste Disposal Ordinance s. 20A, EPD). |
| 44 | US-EX-TB-01 | US | export | https://www.govinfo.gov/link/uscode/18/1716E?type=usc&year=mostrecent&link-type=html | Consistent | full | "Tobacco products as nonmailable" | 18 U.S.C. 1716E(a)(1) located; Pub. 52 s. 473.1(d) excludes international mail from the exceptions (checked in the Pub. 52 PDF from the US-EX-EC-01 fetch). |
| 45 | US-EX-EC-01 | US | export | https://pe.usps.com/cpim/ftp/pubs/pub52/pub52.pdf | Consistent | full | "International mail as defined in DMM 608.2.3" | Pub. 52 s. 47 covers ENDS; s. 473.1(d) means exceptions do not apply to international mail. Same PDF as US-EX-LA-01, fetched once. |
| 46 | G2-TW-IM-GEN-01 | TW | import | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0350064 | Consistent | full | "毛重七十公斤以下之貨物" | Art. 6 para. 1 items 1-2 and para. 2. |
| 47 | TW-EX-JW-03 | TW | export | https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0350072 | Wording differs, meaning consistent | full | "據實申報物品名稱、數量、價值" | Art. 16 says parcels that need no customs declaration (art. 15: FOB over USD 5,000 or other triggers) are declared by name/quantity/value on the mailing documents. "Normal export declaration" in the rule is looser than that; suggest rewording. |
| 48 | DE-EX-JW-01 | DE | export | https://www.zoll.de/DE/Privatpersonen/Postsendungen-Internetbestellungen/Sendungen-in-einen-Nicht-EU-Staat/Einschraenkungen/Waren/Rohdiamanten/rohdiamanten_node.html | Consistent | full | "existieren keine Wertgrenzen bzw. Freimengen für Rohdiamanten" | Kimberley certificate required; no value or quantity exemption. |

## Findings worth acting on

- US-IM-LA-02: permit is attached to "high-risk" countries in the rule, but the regulation attaches the permit to "DMRVV-restricted" countries; high-risk countries need a foreign rabies vaccination/microchip form and designated airports.
- TW-EX-JW-03: "normal export declaration" is looser than art. 16 (declaration on mailing documents below the art. 15 triggers).
- AU-EX-BT-02: rule mentions "loose" batteries; page only allows installed batteries (max two batteries / four cells) and does not use that word. GD-DE-EX-PS-01: para. 4 (inspection/blocking) not checked.
- CN-IM-AL-01, CN-IM-MD-01, SG-EX-AL-02, GD-SG-EX-MD-02: parts of the rule text come from sources other than the cited URL (1,500 ml allowance, RMB 2,000 limit, liquor being dutiable, SHARE). Cite the supporting page or trim the claim.
- No outright contradiction was found in this sample.

## Limitations

- **Sample size.** 48 of 681 rules (7.0%). With 0 contradictions and 10 wording-level issues among 44 comparable rows, no population error rate can be stated with confidence; the sample says nothing certain about the remaining 633 rules. Even together with the earlier 2026-11-02 check of 36 rules (two countries), most of the 681 rules remain individually unverified.
- **Four rules (4 of 48) were not verified**: JP-IM-LA-02 (e-Gov law page is a JavaScript shell), AU-IM-CO-01 (ABF list body not in static HTML), GA-GB-EX-CO-02 and GA-GB-EX-BH-02 (Royal Mail TLS certificate verification failed; verification was deliberately left on). Dynamic or client-rendered pages are the largest systematic gap: a static fetch cannot see them.
- **Headings only** for SG-IM-CU-01 and AU-EX-FD-03 (long statute pages whose body was not in the fetched HTML).
- **One-page comparison.** Each rule was checked only against its cited URL. When a rule bundles several claims, claims supported by other sources were marked "wording differs", not confirmed. Negative claims ("no restriction found") cannot be verified from one page.
- **Currency.** Pages are as fetched on 2026-11-08 and several are living pages (eCFR, legislation sites, HMRC/ABF/Zoll guidance); a change since the 2026-11-02 retrieval would show up as a difference, none was identified, but page revision dates are not available on every page.
- **Languages.** Chinese, Japanese and German sources were read in the original; translation nuance in the paraphrased English rule text may hide small differences.
- **Method.** Single reviewer pass, text extraction by regex/pdftotext; PDFs (USPS Pub. 52, MFA customs law) were located by text search, not page-by-page reading. Statutory interpretation and legal sufficiency were not assessed; this checks transcription fidelity only, not legal advice.
- **Scope.** The 681-rule file only; PayPal policy snippets (140) and shared tables were not sampled.
