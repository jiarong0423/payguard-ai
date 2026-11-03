"""Per-country rules routes: PayPal rules plus government and postal export/import rules (pack data/country_rules/paypal_country_rules_v1.json).

Deterministic and read-only: no outbound call and no model, so the hosted demo serves them too. Advisory only; they never
change the AUP result. A check that finds a BLOCK is kept per session and holds the invoice review and draft routes
(409 country_rules_blocked) until a later check for that session clears it. Mounted when present (the module is optional)
by app.main.register_optional_country_routes; the public build ships it since 66ba4f8 (red team r20).
"""

from __future__ import annotations

import re
from typing import Literal, Optional

from fastapi import Depends
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator

from payguard import country_rules

CountryCode = Literal["US", "TW", "CN", "HK", "GB", "DE", "JP", "SG", "AU", "CA"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class CountryRulesCheckRequest(_Strict):
    """Seller and buyer countries plus closed choices; no free text reaches the check."""
    seller_country: CountryCode
    buyer_country: CountryCode
    account_type: Literal["personal", "business"] = "business"
    account_opened: Literal["unknown", "before_cutoff", "after_cutoff"] = "unknown"
    checkout: Literal["paypal_account", "guest_card"] = "paypal_account"
    amount: Optional[StrictStr] = Field(default=None, pattern=r"^[0-9]{1,9}(\.[0-9]{1,2})?$")
    currency: Optional[StrictStr] = Field(default=None, pattern=r"^[A-Z]{3}$")
    goods_tags: list[StrictStr] = Field(default_factory=list, max_length=16)

    @model_validator(mode="after")
    def amount_matches_currency_decimals(self):
        # (r25 owner request) The invoice's currency rule (schemas.ZERO_DECIMAL_CURRENCIES, PayPal currency-codes):
        # TWD, JPY and HUF amounts are whole units; other currencies keep up to two decimals (the pattern above).
        if self.amount is not None and self.currency in ("TWD", "JPY", "HUF") and not re.fullmatch(r"[0-9]{1,9}", self.amount):
            raise ValueError("country_amount_whole_units")
        return self


class CountryRulesSearchRequest(_Strict):
    query: StrictStr = Field(min_length=1, max_length=200)
    limit: int = Field(default=5, ge=1, le=10)


def _error(error_response, error):
    code = str(error)
    return error_response(503 if code.startswith("country_rules_") else 422, code)


def register_country_routes(application, read_session, write_session, error_response):
    # The latest check per demo session. The invoice review route reads it, so a BLOCK holds the Sandbox invoice
    # draft on the server too, not only by a greyed-out button (review r10).
    application.state.country_blocks = {}

    def remember(session, result, goods_tags, amount=None, currency=None):
        blocks = application.state.country_blocks
        # Snapshot the keys (list() of a dict runs under the GIL) and pop with a default: a concurrent Reset demo pops
        # from the same dict, and iterating it live could raise mid-loop (red team r16).
        live = set(application.state.store.sessions)
        for stale in [key for key in list(blocks) if key not in live]:
            blocks.pop(stale, None)
        # The goods are part of what was checked (red team r2 R2-3: a held e-cigarette pair re-checked with no goods
        # ticked used to clear the draft for the same pair).
        # (attack r22) The checked amount and currency too: the invoice review must carry the same ones, or the
        # signature-confirmation warning could be checked at USD 1.00 and the invoice made at USD 9,999,999.99.
        blocks[session.session_id] = {"blocked": result["blocked"], "seller_country": result["seller_country"],
                                      "buyer_country": result["buyer_country"], "goods_tags": sorted(set(goods_tags)),
                                      "amount": amount, "currency": currency}

    @application.get("/api/v1/country-rules/countries")
    def country_rules_countries(_session=Depends(read_session)):
        try:
            pack = country_rules.load_pack()
        except country_rules.CountryRulesError as error:
            return _error(error_response, error)
        return {"schema_version": country_rules.SCHEMA, "retrieved_at": pack["retrieved_at"],
                "countries": country_rules.countries(pack), "goods_tags": {
                    "prohibited": pack["shared"]["aup_prohibited_tags"], "approval": pack["shared"]["aup_preapproval_tags"],
                    "law_dependent": pack["shared"]["law_dependent_tags"]}}

    @application.post("/api/v1/country-rules/check")
    def country_rules_check(body: CountryRulesCheckRequest, session=Depends(write_session)):
        try:
            result = country_rules.check(**body.model_dump())
            remember(session, result, body.goods_tags, body.amount, body.currency)
            return result
        except country_rules.CountryRulesError as error:
            return _error(error_response, error)

    @application.post("/api/v1/country-rules/search")
    def country_rules_search(body: CountryRulesSearchRequest, _session=Depends(write_session)):
        try:
            return {"schema_version": country_rules.SCHEMA, "hits": country_rules.search(body.query, body.limit)}
        except country_rules.CountryRulesError as error:
            return _error(error_response, error)
