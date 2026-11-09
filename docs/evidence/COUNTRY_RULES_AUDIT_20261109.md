# Country rules pack: audit notes (2026-11-09)

Scope: `data/country_rules/paypal_country_rules_v1.json`, 681 government and postal rules (import and export) for 10 countries. Rule count, ids and rule text are unchanged. This note records what the audit found and what was done; it makes no claim beyond that.

## What changed in the data file

Two optional fields were added. Nothing reads them yet, and the loader does not validate rule keys, so behaviour is unchanged. The pinned digest in `src/payguard/country_rules.py` was updated in the same change.

- `evidence_kind: "absence_only"` on the 14 rules whose text only says nothing was found. Absence of a found rule is not evidence that the goods are allowed.
- `page_date_status: "not_shown"` on the 265 rules that show no page date.

## 1. Rules that only say nothing was found (14)

Match: `no .* (restriction|rule)s? found | none found | not found`.

| Side | Country | Id | Tag |
|---|---|---|---|
| import | CN | CN-IM-CO-01 | cosmetics |
| import | CN | CN-IM-MD-01 | medical_devices |
| export | CN | CN-EX-CO-01 | cosmetics |
| export | CN | CN-EX-AL-01 | alcohol |
| export | CN | CN-EX-RX-03 | prescription |
| export | CN | CN-EX-MD-01 | medical_devices |
| export | TW | TW-EX-FD-02 | food |
| export | TW | TW-EX-CO-01 | cosmetics |
| export | TW | TW-EX-RF-01 | radio_wireless |
| export | TW | TW-EX-AL-01 | alcohol |
| export | TW | TW-EX-TB-01 | tobacco_other |
| export | TW | TW-EX-RX-03 | prescription |
| export | TW | TW-EX-MD-01 | medical_devices |
| export | SG | GD-SG-EX-RW-01 | radio_wireless |

Three are medical devices (CN import, CN export, TW export). The checker still shows these rules as general-tier information; the new field lets a reader or later code tell them apart from a real rule.

## 2. Hong Kong has no medical_devices rule

HK has import and export rules for other tags but none tagged `medical_devices`. This is a gap in the pack, not a finding that Hong Kong has no such rule. No rule was added.

## 3. Rules without a page date (265)

By country: JP 62, HK 62, DE 59, AU 44, GB 20, SG 15, US 3. CA, CN and TW have none. The field was empty (`null`) in the source rows; the rule text and its URL are unchanged.

## 4. Identical text across import and export (4 groups)

Each group is one import rule and one export rule with the same text, URL and country, for a law that covers both directions. These are not errors and were kept, because export and import are matched separately.

- CN batteries_hazmat: G2-CN-IM-BH-01 / G2-CN-EX-BH-01
- TW currency: G2-TW-IM-CU-01 / G2-TW-EX-CU-01
- TW currency: G2-TW-IM-CU-02 / G2-TW-EX-CU-02
- TW general: G2-TW-IM-GEN-01 / G2-TW-EX-GEN-01

## 5. Scope limit: customs and post, not online sale

The pack covers import and export rules (customs, post, carrier). Only 10 rules mention online or internet sale. Whether a particular online sale is allowed can depend on law the pack does not hold.
