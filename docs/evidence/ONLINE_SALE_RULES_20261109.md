# Online-sale rules for medical devices (2026-11-09)

## What this adds and why it is a separate file
The ten-country rules in `data/country_rules/paypal_country_rules_v1.json` (681 rules, pinned by a SHA-256 in the code) answer one question: what may an individual **import or post** between two countries. They do not say what may be **sold online** to the public, which is what a marketplace seller needs to know. The new file `data/country_rules/online_sale_rules_20261109.json` holds that second kind of rule. It is a separate file so the pinned dataset, its hash and its counted numbers stay unchanged.

## What is in it
- **Two rules, each read from the official page or document itself on 2026-11-09:**
  - Taiwan: medical devices may be sold through distance-selling channels only by registered medical device dealers or pharmacies, and only class 1 devices plus 19 listed class 2 item groups (Ministry of Health and Welfare announcement 衛授食字第1101601942號, 2021-04-29; the annex was read as an image of the official PDF and its 19 items are copied into the file). Contact lenses themselves are not on the annex, only lens care products.
  - Malaysia: a registered device may be sold online, but professional-use devices must not be sold to the general public (Medical Device Authority FAQ, page dated 2026-11-06; an FAQ answer, not a statute).
- **Three marketplace policies** (not law): Yahoo Taiwan bans all medical devices, Yahoo! Japan Auctions bans highly controlled devices including contact lenses, eBay bans prescription-required devices and allows over-the-counter ones with conditions. Platforms can be stricter than the law.

## What is not in it: reported but not verified
A web AI reported online-sale rules for nine more countries (Australia, Canada, China, Germany, Great Britain, Hong Kong, Japan, Singapore, United States). Its source numbers for US device classes matched the FDA classification data we downloaded, but its quoted wording for these country rules was not checked against the pages, and for China, Japan, Germany and Singapore it was a translation. They are not in the data file. Examples: Hong Kong's device listing system is voluntary, Japan requires a prefectural licence to sell highly controlled devices, Germany limits prescription-only devices, Singapore is reported to forbid selling contact lenses online. Treat each as a lead to check against the official page, not as a finding.

## Limits
- Official pages for several countries (Australia, California, Korea, Hong Kong, Germany, Great Britain) could not be read from the author's computer (blocked, timed out or JavaScript-only), so their cells are empty, not "no rule".
- Rules change; each entry carries the page date where the page showed one.
- This is not legal advice and TradeGlot does not use these rules in any decision: they are reference data, and the category hints elsewhere in the project do not depend on them.
