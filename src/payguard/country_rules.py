"""Per-country rules: a deterministic pre-check for a seller-country / buyer-country pair, and a local vector search
over the official clauses it is built from.

The pack (data/country_rules/paypal_country_rules_v1.json) has two layers with different owners, and each row links to
its own source (review r13: do not call the whole pack PayPal's). PayPal layer: ten country profiles and 140 clauses
paraphrased from PayPal's legal hub pages with their URLs and retrieval date. Government and postal layer: 681 export
and import rules from official government pages and postal operators, each with its statute and article where one
exists, in the three tiers consolidation services use: general, restricted, prohibited. Export
and import are matched separately: allowed to leave one country is not allowed to enter the other. It is not legal advice. For a destination without import rules, goods PayPal does not name
(live animals, plants, food, cosmetics, batteries) are reported as depending on the law at both ends instead of a
guess. No network call, no model call.
"""

from __future__ import annotations

import collections
import hashlib
import json
import math
from pathlib import Path
import re

PACK_PATH = Path(__file__).resolve().parents[2] / "data" / "country_rules" / "paypal_country_rules_v1.json"
PACK_SHA256 = "c2c67640c11cd98413ef60d1429d60f816ef917635b06acf4278943fbece42cb"
SCHEMA = "payguard.country_rules.v1"
ACCOUNT_TYPES = ("personal", "business")
ACCOUNT_OPENED = ("unknown", "before_cutoff", "after_cutoff")
CHECKOUTS = ("paypal_account", "guest_card")
SEVERITY_ORDER = {"BLOCK": 0, "WARN": 1, "INFO": 2}
TIER_SEVERITY = {"prohibited": "BLOCK", "restricted": "WARN", "general": "INFO"}
# The policy names these more narrowly than the tag (review r10): say what it says.
AUP_WORDING = {"weapons": "firearms, ammunition and certain weapons or knives regulated by law"}
# Seller-facing names for tags, the same words as the panel's TAG_LABELS (red team 2026-11-03: "E cigarettes").
TAG_TEXT = {"e_cigarettes": "E-cigarettes", "tobacco_other": "Tobacco (not e-cigarettes)", "prescription": "Prescription items",
            "medical_devices": "Medical devices", "jewellery_precious_metals": "Jewellery or precious metals",
            "alcohol": "Alcohol"}
MAX_TAGS = 16  # every tag the panel offers (red team r2: the UI showed 16, the server took 12)
EU_MEMBERS = {"DE"}
# A rule that binds one channel only (the post, sea dangerous goods, air mail, travellers' luggage) never decides a
# whole tag: a seller can usually ship another way (review 2026-11-03: postal bans were holding courier sales).
CHANNEL_TEXT = {"post": "by post", "sea": "by sea", "air_mail": "by air mail", "traveller": "for travellers",
                "licensed_import": "via a licensed importer"}
# Goods PayPal approves first but whose shipment is still national law: a missing side is reported for them too.
PHYSICAL_APPROVAL_TAGS = {"alcohol", "e_cigarettes", "tobacco_other", "prescription", "medical_devices",
                          "jewellery_precious_metals"}


class CountryRulesError(ValueError):
    """Fixed code only."""


_CACHE: dict = {}


def load_pack(path: Path = PACK_PATH, expected_sha256: str = PACK_SHA256) -> dict:
    """The pack, checked against its pinned digest so an edited file is refused, not silently used."""
    key = (str(path), expected_sha256)
    if key in _CACHE:
        return _CACHE[key]
    try:
        raw = path.read_bytes()
    except OSError:
        raise CountryRulesError("country_rules_unavailable") from None
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise CountryRulesError("country_rules_digest_mismatch")
    pack = json.loads(raw.decode("utf-8"))
    if pack.get("schema_version") != SCHEMA or not isinstance(pack.get("countries"), dict):
        raise CountryRulesError("country_rules_invalid")
    _CACHE[key] = pack
    return pack


def side_rules(pack: dict, side: str, seller_country: str, buyer_country: str, tag: str) -> list[dict]:
    """One side of a cross-border sale for a tag. side="export": the seller country's export rules (for any
    destination, or this destination only). side="import": the buyer country's import rules (from any origin, or this
    origin only). A domestic sale has neither step. Leaving one country says nothing about entering the other, so the
    two sides are always looked up separately. A domestic sale has no border step, but a sale or possession ban
    (rules marked applies_domestic) still binds the seller at home. EU rules written for the bloc ("EU->GB") match a
    seller or buyer in an EU member state."""
    if seller_country == buyer_country:
        if side != "export":
            return []
        block = (pack.get("export_rules") or {}).get(seller_country, {})
        return [rule for rule in block.get("rules", []) if rule["tag"] == tag and rule.get("applies_domestic")]
    origins = {seller_country} | ({"EU"} if seller_country in EU_MEMBERS else set())
    destinations = {buyer_country} | ({"EU"} if buyer_country in EU_MEMBERS else set())
    if side == "export":
        block = (pack.get("export_rules") or {}).get(seller_country, {})
        routes = {f"{seller_country}->*"} | {f"{seller_country}->{to}" for to in destinations}
    else:
        block = (pack.get("import_rules") or {}).get(buyer_country, {})
        routes = {f"*->{buyer_country}"} | {f"{origin}->{buyer_country}" for origin in origins}
    return [rule for rule in block.get("rules", []) if rule["tag"] == tag and rule["route"] in routes]


def import_rules_for(pack: dict, seller_country: str, buyer_country: str, tag: str) -> list[dict]:
    return side_rules(pack, "import", seller_country, buyer_country, tag)


_RELEVANCE = {"parcel_rule": 2}


def _known(value) -> bool:
    return bool(value) and "NOT_FOUND" not in str(value)


def _cite(rule: dict) -> str:
    """The statute and article a rule comes from, when the pack has them."""
    if not rule.get("statute"):
        return ""
    # A statute named in Chinese or Japanese also carries its English name (review 2026-11-03), so a reader can tell
    # which law it is without reading the original.
    english = f" ({rule['statute_en']})" if rule.get("statute_en") else ""
    return f" [{rule['statute']}{english}{' ' + rule['article'] if rule.get('article') else ''}]"


def countries(pack: dict | None = None) -> list[dict]:
    pack = pack or load_pack()
    return [{"code": code, "name": row["name"]} for code, row in sorted(pack["countries"].items())]


def _finding(severity: str, code: str, text: str, source: str) -> dict:
    return {"severity": severity, "code": code, "text": text, "source": source}


def accepted_currencies(pack: dict | None = None) -> frozenset:
    """(attack r22) Currency codes a country check accepts: every code in a pack threshold table, plus USD."""
    pack = pack or load_pack()
    codes = {"USD"}
    for country in pack["countries"].values():
        codes.update((country.get("signature_confirmation_thresholds") or {}).keys())
    return frozenset(codes)


def check(seller_country: str, buyer_country: str, *, account_type: str = "business", checkout: str = "paypal_account",
          account_opened: str = "unknown",
          amount: str | None = None, currency: str | None = None, goods_tags: list[str] | tuple = (),
          pack: dict | None = None) -> dict:
    """Findings for one seller/buyer pair, most severe first. BLOCK = a cited PayPal or government rule stops this sale as set up;
    WARN = it can go ahead but Seller Protection or approval is at risk; INFO = a rule worth knowing."""
    pack = pack or load_pack()
    table = pack["countries"]
    if seller_country not in table or buyer_country not in table:
        raise CountryRulesError("country_unknown")
    if account_type not in ACCOUNT_TYPES or checkout not in CHECKOUTS or account_opened not in ACCOUNT_OPENED:
        raise CountryRulesError("country_check_invalid")
    # (attack r21) An amount is a price: negative, NaN or infinite values are refused here too, not only by the API
    # schema, so a direct caller gets the same 422 country_check_invalid instead of a normal check.
    if amount is not None:
        try:
            parsed_amount = float(amount)
        except (TypeError, ValueError):
            raise CountryRulesError("country_check_invalid") from None
        if not math.isfinite(parsed_amount) or parsed_amount < 0:
            raise CountryRulesError("country_check_invalid")
    # (attack r22) Only ISO 4217 codes the pack prices in (its signature-confirmation thresholds) plus USD, the invoice
    # currency. An unknown code such as "ZZZ" was accepted and its threshold silently skipped.
    if currency is not None and currency not in accepted_currencies(pack):
        raise CountryRulesError("country_check_invalid")
    shared = pack["shared"]
    known_tags = set(shared["aup_prohibited_tags"]) | set(shared["aup_preapproval_tags"]) | set(shared["law_dependent_tags"])
    tags = list(dict.fromkeys(goods_tags))
    if len(tags) > MAX_TAGS or any(tag not in known_tags for tag in tags):
        raise CountryRulesError("country_check_invalid")
    seller, buyer = table[seller_country], table[buyer_country]
    sources = seller["sources"]
    findings = []

    restricted = seller.get("personal_goods_payments_restricted")
    # The rule binds only accounts opened after the cut-off: blocked when the seller says so, a warning when unknown.
    if restricted and account_type == "personal" and account_opened != "before_cutoff":
        findings.append(_finding("BLOCK" if account_opened == "after_cutoff" else "WARN", "personal_account_goods_restricted",
            f"{seller['name']}: personal accounts registered after {restricted['registered_after']} (or a later date PayPal "
            "announces) are restricted from requesting and accepting payments other than friends and family, including "
            "goods and services, and cannot become business accounts. Sell from a business account.",
            sources["user_agreement"]))
    if restricted and account_type == "business":
        findings.append(_finding("WARN", "local_account_required",
            f"{seller['name']}: business accounts must also open an account with {restricted['also_required'].split(' account')[0]}; "
            "without it PayPal may suspend the PayPal account after the cut-off.", sources["user_agreement"]))
    if seller.get("goods_and_services_only") and account_type == "personal":
        findings.append(_finding("INFO", "goods_and_services_only",
            f"{seller['name']}: accounts are for goods and services; personal fund transfers are not offered.",
            sources["user_agreement"]))

    for tag in tags:
        # An AUP ban ends the item: PayPal will not take the payment whatever the import rules say.
        if tag in shared["aup_prohibited_tags"]:
            findings.append(_finding("BLOCK", "aup_prohibited",
                f"PayPal's Acceptable Use Policy prohibits {AUP_WORDING.get(tag, tag.replace('_', ' '))} in every country in this pack.",
                sources["acceptable_use"]))
            continue
        # Approval goods still face the destination's import rules (review r10: alcohol, e-cigarettes, medicines,
        # medical devices and jewellery used to stop at the approval warning).
        if tag in shared["aup_preapproval_tags"]:
            findings.append(_finding("WARN", "aup_preapproval",
                f"{TAG_TEXT.get(tag, tag.replace('_', ' ').capitalize())} needs PayPal's approval before you accept payments for it.",
                sources["acceptable_use"]))
        sides = {side: side_rules(pack, side, seller_country, buyer_country, tag) for side in ("export", "import")}
        # Both sides are matched on their own (owner rule 2026-11-02: allowed to leave is not allowed to enter). A broad
        # tag (food, plants, medicines) mixes banned kinds with allowed ones: a side blocks only when every rule it has
        # for the tag on this route is a ban; otherwise each ban reads "banned if your item is this kind" and warns.
        domestic = seller_country == buyer_country
        for side, rules in sides.items():
            country = seller if side == "export" else buyer
            label = "domestic sale" if domestic else side
            # A rule with scope "subset" covers only some items under the tag (endangered species, narcotics, relics),
            # and a channel rule binds one way of shipping only: neither decides the whole tag, so their bans warn.
            whole = [rule for rule in rules if rule.get("scope", "all") == "all" and not rule.get("channel")]
            whole_tag_banned = bool(whole) and all(rule["tier"] == "prohibited" for rule in whole)
            for rule in rules:
                # A research gap marker (NOT_FOUND) is not a limit a seller can act on: leave it out of the text.
                limit = f" Limit: {rule['quantity_limit']}." if _known(rule.get("quantity_limit")) else ""
                permit = f" Needs: {rule['permit']}." if _known(rule.get("permit")) else ""
                severity = TIER_SEVERITY[rule["tier"]]
                channel = CHANNEL_TEXT.get(rule.get("channel"), "")
                lead = f"{country['name']} {label} ({rule['tier']}{', ' + channel + ' only' if channel else ''})"
                if rule["tier"] == "prohibited" and channel:
                    severity, lead = "WARN", f"{country['name']} {label} (banned {channel}; other channels may differ)"
                elif rule["tier"] == "prohibited" and (not whole_tag_banned or rule.get("scope", "all") != "all"):
                    severity, lead = "WARN", f"{country['name']} {label} (banned if your item is this kind)"
                findings.append(_finding(severity, f"{'domestic' if domestic else side}_{rule['tier']}",
                                         f"{lead}: {rule['rule']}{limit}{permit}{_cite(rule)}", rule["url"]))
        if any(sides.values()):
            # One side matched and the other has no rules in the pack: say so instead of reading silence as allowed.
            for side, rules in sides.items():
                if not rules and not domestic and (tag in shared["law_dependent_tags"] or tag in PHYSICAL_APPROVAL_TAGS):
                    country = seller if side == "export" else buyer
                    findings.append(_finding("WARN", f"{side}_rules_not_in_pack",
                        f"The pack has no {country['name']} {side} rules for {tag.replace('_', ' ')}; the other side's rules "
                        f"above do not mean {country['name']} allows it. Check its official {side} rules.",
                        sources["acceptable_use"]))
        elif tag in shared["law_dependent_tags"] or (tag in PHYSICAL_APPROVAL_TAGS and seller_country != buyer_country):
            where = (f"both {seller['name']} and {buyer['name']}" if seller_country != buyer_country
                     else seller["name"])
            findings.append(_finding("WARN", "law_dependent",
                f"PayPal names no rule for {tag.replace('_', ' ')}; whether you can ship it depends on the law in {where} "
                "(import, quarantine or carrier rules). Check the official rules before you ship"
                + (" across the border." if seller_country != buyer_country else "."),
                sources["acceptable_use"]))

    if seller_country != buyer_country:
        # Parcel-wide rules keep their tier (a conditional ban warns). Route-only rules (e.g. the mainland permitted-goods
        # list on CN->TW) always show; rules for every route show once an item with rules on that side is ticked.
        for side, country, wildcard in (("export", seller, "->*"), ("import", buyer, "*->")):
            item_rules = any(side_rules(pack, side, seller_country, buyer_country, tag) for tag in tags)
            for rule in side_rules(pack, side, seller_country, buyer_country, "general"):
                if wildcard in rule["route"] and not item_rules:
                    continue
                severity = "INFO" if rule["tier"] == "general" else "WARN"
                findings.append(_finding(severity, f"{side}_parcel_rule",
                    f"{country['name']} {side} parcels ({rule['tier']}): {rule['rule']}{_cite(rule)}", rule["url"]))

    if checkout == "guest_card" and seller["seller_protection_guest_checkout"] == "not_eligible":
        findings.append(_finding("WARN", "no_protection_guest_checkout",
            f"Sellers registered in {seller['name']} get no Seller Protection on guest or card checkout that does not "
            "go through the buyer's PayPal account.", sources["seller_protection"]))

    thresholds = seller.get("signature_confirmation_thresholds") or {}
    if amount is not None and currency in thresholds:
        try:
            value = float(amount)
        except (TypeError, ValueError):
            raise CountryRulesError("country_check_invalid") from None
        if value >= thresholds[currency]:
            findings.append(_finding("WARN", "signature_required",
                f"At {currency} {thresholds[currency]:,} or more, Seller Protection needs signature confirmation of delivery.",
                sources["seller_protection"]))

    if seller["seller_protection_address_in_country_required"]:
        findings.append(_finding("INFO", "address_in_country",
            f"Seller Protection in {seller['name']} expects the account's primary address there.", sources["seller_protection"]))
    if seller["risk_hold_max_days"]:
        findings.append(_finding("INFO", "risk_hold_days",
            f"Payments to a {seller['name']} account are usually held for up to {seller['risk_hold_max_days']} days on risk "
            "review, and longer while a dispute is open.", sources["user_agreement"]))
    findings.append(_finding("INFO", "seller_protection_scope",
        "Seller Protection covers unauthorised payments and items not received, never 'not as described' claims.",
        sources["seller_protection"]))
    if not buyer["snad_30_days_after_delivery_cap"]:
        findings.append(_finding("INFO", "buyer_snad_window",
            f"Buyers in {buyer['name']} can claim 'not as described' up to {shared['buyer_dispute_window_days']} days "
            "from payment, without the 30-day-after-delivery limit.", buyer["sources"]["buyer_protection"]))
    if buyer["privacy_laws_named"]:
        findings.append(_finding("INFO", "buyer_privacy_law",
            f"PayPal names {', '.join(buyer['privacy_laws_named'])} for {buyer['name']}: keep buyer data in the review "
            "file to what the case needs.", buyer["sources"]["privacy"]))

    # Most severe first; within a severity, rules about the ticked goods come before parcel-wide lists and PayPal
    # account notes (seller review 2026-11-03: food buyers saw strategic high-tech and postal lists first).
    findings.sort(key=lambda row: (SEVERITY_ORDER[row["severity"]], _RELEVANCE.get(row["code"].split("_", 1)[-1], 1)
                                   if row["code"].endswith("_parcel_rule") else 0))
    return {
        "schema_version": SCHEMA,
        "seller_country": seller_country,
        "buyer_country": buyer_country,
        "cross_border": seller_country != buyer_country,
        "blocked": any(row["severity"] == "BLOCK" for row in findings),
        "findings": findings,
        "retrieved_at": pack["retrieved_at"],
        "advisory_only": True,
        "legal_advice": False,
    }


# ---- local vector search over the official clauses (TF-IDF + cosine, as in tools/example_retrieval.py) ----------
_STOP = set("a an the of to in on for and or is are be by with as at from that this it its any no not can may".split())
COUNTRY_WORDS = {"us": "US", "usa": "US", "taiwan": "TW", "china": "CN", "mainland": "CN", "hong": "HK", "kong": "HK",
                 "uk": "GB", "britain": "GB", "germany": "DE", "eu": "DE", "japan": "JP", "singapore": "SG",
                 "australia": "AU", "canada": "CA"}


def _stem(word: str) -> str:
    for suffix in ("ing", "ies", "es", "ed", "s"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[: -len(suffix)] + ("y" if suffix == "ies" else "")
    return word


def _tokens(text: str) -> list[str]:
    return [_stem(word) for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in _STOP]


class ClauseIndex:
    def __init__(self, snippets: list[dict]):
        self.rows = snippets
        docs = [collections.Counter(_tokens(" ".join(filter(None, (row["text"], row["dimension"].replace("_", " "),
                                                                   row.get("category") or ""))))) for row in snippets]
        df = collections.Counter(term for doc in docs for term in doc)
        self.idf = {term: math.log((1 + len(docs)) / (1 + freq)) + 1.0 for term, freq in df.items()}
        self.vectors = [self._vector(doc) for doc in docs]

    def _vector(self, doc):
        weights = {term: (1 + math.log(freq)) * self.idf.get(term, 0.0) for term, freq in doc.items()}
        norm = math.sqrt(sum(value * value for value in weights.values())) or 1.0
        return {term: value / norm for term, value in weights.items()}

    def search(self, query: str, limit: int = 5) -> list[dict]:
        words = re.findall(r"[a-z]+", query.lower())
        wanted = {COUNTRY_WORDS[word] for word in words if word in COUNTRY_WORDS}
        # A country named in the query filters; it does not score, or it would match every row of that country.
        country_terms = {_stem(word) for word in COUNTRY_WORDS}
        query_vector = self._vector(collections.Counter(term for term in _tokens(query) if term not in country_terms))
        hits = []
        for row, vector in zip(self.rows, self.vectors):
            if wanted and row["country"] not in wanted and row["country"] != "ALL":
                continue
            score = sum(weight * vector.get(term, 0.0) for term, weight in query_vector.items())
            if score > 0:
                hits.append({"score": round(score, 3), "country": row["country"], "dimension": row["dimension"],
                             "text": row["text"], "url": row["url"], "effective_date": row.get("effective_date")})
        hits.sort(key=lambda hit: (-hit["score"], hit["country"], hit["dimension"]))
        return hits[:limit]


def search(query: str, limit: int = 5, pack: dict | None = None) -> list[dict]:
    if type(query) is not str or not 0 < len(query.strip()) <= 200 or not 1 <= limit <= 10:
        raise CountryRulesError("country_search_invalid")
    pack = pack or load_pack()
    index = _CACHE.get(("index", id(pack)))
    if index is None:
        index = _CACHE[("index", id(pack))] = ClauseIndex(pack["snippets"])
    return index.search(query, limit)
