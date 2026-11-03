"""Case routing by fuzzy search: which dispute evidence items apply to what the seller sold.

The seller types what they sold, with typos and all ("wirless hedphones", "ebook pdf"). Code, not a
model, routes the case to a goods group, and the group decides which dispute items the guide asks for
(``evidence_guide.slots_for``):

1. The text is fuzzy-matched against the recorded Channel3 catalogue cards
   (``backend/app/data/channel3_recorded_v1.json``); a close match routes to ``physical`` and names
   the catalogue product it matched. A catalogue match wins over the word lists below.
2. Digital words (ebook, download, licence, course ...) route to ``digital``; service words route to
   ``service``, which the dispute items do not cover yet: the seller is told so. These words must be the
   thing itself (the head word, e.g. "online course"), or name it before a generic head ("software licence
   key"); a describing word does not count ("digital camera", "license plate frame", "cleaning cloth").
   They match exactly (plural and hyphen forms aside, plus a small list of common misspellings), not
   fuzzily, so "steam mop", "coarse sea salt" and "travel plug adapter" are not "stream", "course", "plugin".
3. Anything else is ``unknown``: the seller picks the group.

The route only pre-selects the goods group; the seller can change it, and it never decides a dispute.
Only the sanitised text (``channel3.sanitize_product_name``) is used. Matching runs in the process; only when it
finds no group and a live Channel3 product adapter is configured (switch and key set) does ``CaseRouter.route``
send that sanitised text in one live product search, from its own small budget.
"""

from __future__ import annotations

import re
import threading
from collections import OrderedDict
from difflib import SequenceMatcher
from typing import Iterable, Mapping

from payguard.evidence_guide import SCENARIOS, slots_for

from .channel3 import CallBudget, sanitize_product_name
from .channel3_products import RECORDED_PATH, load_recorded

# Live fallback allowance (operator key only), separate from the shared Channel3 budget of the listing check:
# routing may spend at most ROUTE_CALL_BUDGET calls per process and ROUTE_SESSION_CAP per session.
ROUTE_CALL_BUDGET = 8
ROUTE_SESSION_CAP = 2
MAX_ROUTE_SESSIONS = 256
MATCH_THRESHOLD = 0.55
MAX_MATCHES = 3
MAX_CANDIDATES = 10
UNITS = frozenset({"oz", "ml", "l", "cm", "mm", "in", "inch", "g", "kg", "lb", "gb", "tb", "mah", "w"})
ROUTES = ("physical", "digital", "service", "unknown")

DIGITAL_WORDS = ("ebook", "e-book", "pdf", "download", "downloadable", "digital", "licence", "license", "serial",
                 "subscription", "course", "template", "preset", "font", "software", "plugin", "app", "membership",
                 "printable", "mp3", "stream", "streaming", "voucher", "code")
SERVICE_WORDS = ("service", "consultation", "coaching", "lesson", "repair", "installation", "cleaning", "tutoring",
                 "commission", "session", "booking")
# File formats that make the whole phrase digital wherever they stand ("ebook pdf guide", "mp3 album").
FORMAT_WORDS = frozenset({"pdf", "mp3", "downloadable", "printable"})
# Generic head words: "software licence key", "font file", "course bundle" name the digital thing just before them.
GENERIC_HEADS = frozenset({"key", "file", "bundle", "access", "link", "version", "edition"})
# Misspellings the word lists accept (exact match otherwise; fuzzy matching sent "steam mop" to "stream").
MISSPELLINGS = {"ebok": "ebook", "e-bok": "ebook", "licens": "license", "lisence": "license", "subscripton": "subscription",
                "dowload": "download", "downlaod": "download", "softwear": "software", "consultaton": "consultation"}
_STOP = frozenset({"a", "an", "the", "of", "for", "and", "with", "to", "set", "my", "i", "sold", "two", "one", "pack"})


def _tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower()) if token not in _STOP and len(token) > 1]


def _trigrams(token: str) -> set[str]:
    padded = f"  {token} "
    return {padded[i:i + 3] for i in range(len(padded) - 2)}


def word_similarity(a: str, b: str) -> float:
    """Typo-tolerant similarity of two words in [0, 1]: the better of trigram overlap and edit ratio."""
    if a == b:
        return 1.0
    ta, tb = _trigrams(a), _trigrams(b)
    jaccard = len(ta & tb) / len(ta | tb)
    return max(jaccard, SequenceMatcher(None, a, b).ratio())


def text_similarity(query_tokens: list[str], target_tokens: Iterable[str]) -> float:
    """Share of query words that find a close word in the target (each word's best similarity, averaged).

    The last word is usually the thing itself ("handmade soap" -> soap), so it must find a close word too;
    otherwise a shared adjective alone would route a soap to a leather bag.
    """
    target = list(dict.fromkeys(target_tokens))
    if not query_tokens or not target:
        return 0.0
    best = [max(word_similarity(word, other) for other in target) for word in query_tokens]
    # The head word is the last plain word; sizes and units after it ("bottle 32 oz") are not the thing itself.
    head = max((i for i, word in enumerate(query_tokens) if word.isalpha() and word not in UNITS), default=len(best) - 1)
    if best[head] < 0.75:
        return 0.0
    return sum(score if score >= 0.75 else 0.0 for score in best) / len(best)


def _exact_form(token: str) -> str:
    """Form used by the precise filter: no hyphen, no plural s ("cross-body" = "crossbody", "cups" = "cup")."""
    token = token.replace("-", "")
    return token[:-1] if len(token) > 3 and token.endswith("s") and not token.endswith("ss") else token


def _exact_set(tokens: list[str]) -> list[str]:
    """Exact forms, with a number and the unit after it joined ("32 oz" = "32oz")."""
    out, i = [], 0
    while i < len(tokens):
        token = tokens[i]
        if token.isdigit() and i + 1 < len(tokens) and tokens[i + 1] in UNITS:
            out.append(token + tokens[i + 1])
            i += 2
            continue
        out.append(_exact_form(token))
        i += 1
    return out


def _coded(tokens: Iterable[str]) -> set[str]:
    """Words that carry a number: sizes and model codes (32oz, wh1000xm6)."""
    return {token for token in tokens if any(ch.isdigit() for ch in token)}


def rank(tokens: list[str], entries: list[dict]) -> tuple[list[dict], int]:
    """Fuzzy search, then a precise filter.

    1. Fuzzy recall: every entry whose fuzzy score reaches MATCH_THRESHOLD is a candidate (typos allowed).
    2. Filter: a candidate whose sizes or model codes contradict the query's is dropped (XM6 asked, XM4C listed).
    3. Filter: only candidates with the most exactly matching words stay.
    Survivors are labelled exact (every query word matched exactly, no code missing) or close.
    Returns (at most MAX_MATCHES survivors, number of candidates the filter removed).
    """
    query_exact = _exact_set(tokens)
    query_codes = _coded(query_exact)
    candidates = []
    for entry in entries:
        entry_exact_list = _exact_set(entry["tokens"])
        # Codes are judged by the filter below, not by fuzzy recall, so "32 oz" does not lower the recall score.
        fuzzy = text_similarity([word for word in query_exact if word not in query_codes] or query_exact, entry_exact_list)
        if fuzzy < MATCH_THRESHOLD:
            continue
        entry_exact = set(entry_exact_list)
        entry_codes = _coded(entry_exact)
        if query_codes and entry_codes and not query_codes <= entry_codes:
            candidates.append(None)
            continue
        exact_words = [word for word in query_exact if word in entry_exact]
        candidates.append({"product_id": entry["product_id"], "title": entry["title"], "category": entry["category"],
                           "score": round(fuzzy, 2), "exact_words": exact_words[:8],
                           "match_type": "exact" if len(exact_words) == len(query_exact) else "close"})
    kept = [row for row in candidates if row is not None]
    best = max((len(row["exact_words"]) for row in kept), default=0)
    survivors = sorted((row for row in kept if len(row["exact_words"]) == best),
                       key=lambda row: (row["match_type"] != "exact", -row["score"], row["title"]))
    return survivors[:MAX_MATCHES], len(candidates) - len(survivors)


def _hit(tokens: list[str], vocabulary: tuple[str, ...]) -> str | None:
    """The vocabulary word the seller's thing is, or None: only the head word counts (or the word before a generic
    head such as "key"), matched exactly in its plain form, so a describing word ("digital camera") never routes."""
    words = [MISSPELLINGS.get(token, token) for token in tokens if any(ch.isalpha() for ch in token)]
    words = [word for word in words if word not in UNITS]
    if not words:
        return None
    candidates = [words[-1]]
    if words[-1] in GENERIC_HEADS and len(words) > 1:
        candidates.append(words[-2])
    forms = {}
    for word in vocabulary:
        forms.setdefault(_exact_form(word), word)  # first listed spelling wins ("ebook" over "e-book")
    if any(word in FORMAT_WORDS for word in words):
        # Name the first listed word in the phrase ("ebok pdf guide" -> ebook), not just the format.
        candidates = words
    for candidate in candidates:
        hit = forms.get(_exact_form(MISSPELLINGS.get(candidate, candidate)))
        if hit:
            return hit
    return None


def catalogue_entries(recorded: Mapping[str, dict]) -> list[dict]:
    entries, seen = [], set()
    for entry in recorded.values():
        for card in entry["cards"]:
            if card["product_id"] in seen:
                continue
            seen.add(card["product_id"])
            words = [card["title"], card["category"] or "", card["brand"] or "", *card["key_features"], *card["materials"]]
            entries.append({"product_id": card["product_id"], "title": card["title"], "category": card["category"],
                            "tokens": _tokens(" ".join(words))})
    return entries


def _items(route: str) -> list[str]:
    if route not in ("physical", "digital"):
        return []
    spec = SCENARIOS["dispute"]["slots"]
    return [spec[slot_id][0] for slot_id in slots_for("dispute", route)]


def route_case(text: object, catalogue: list[dict]) -> dict:
    """Closed routing result; never raises on seller input."""
    name = sanitize_product_name(text)
    base = {"query": name, "matches": [], "filtered_out": 0, "matched_word": None, "decided_by": "code", "affects_decision": False}
    if name is None:
        return {**base, "route": "unknown", "reason": "nothing_to_match", "items": []}
    tokens = _tokens(name)
    matches, filtered_out = rank(tokens, catalogue)
    if matches:
        return {**base, "route": "physical", "reason": "catalogue_match", "matches": matches, "filtered_out": filtered_out,
                "items": _items("physical")}
    digital = _hit(tokens, DIGITAL_WORDS)
    if digital:
        return {**base, "route": "digital", "reason": "digital_word", "matched_word": digital, "matches": [],
                "items": _items("digital")}
    service = _hit(tokens, SERVICE_WORDS)
    if service:
        return {**base, "route": "service", "reason": "service_word", "matched_word": service, "items": []}
    if filtered_out:
        # Close names were found, but every one contradicts a size or model code the seller gave.
        return {**base, "route": "unknown", "reason": "filtered_conflict", "filtered_out": filtered_out, "items": []}
    return {**base, "route": "unknown", "reason": "no_close_match", "items": []}


class CaseRouter:
    """Holds the catalogue index built once from the recorded Channel3 replies.

    With a live Channel3 product adapter (operator key configured), text that matches nothing in the recorded
    catalogue is searched once on Channel3; a close live product routes to ``physical``. The hosted demo has no
    live adapter, so it never calls out.

    Live searches spend the router's own small budget, never the listing check's shared Channel3 budget, and each
    session may spend at most ``session_cap`` of them, so one session cannot exhaust routing for everyone.
    """

    def __init__(self, recorded: Mapping[str, dict] | None = None, products=None, *, budget: CallBudget | None = None,
                 session_cap: int = ROUTE_SESSION_CAP):
        if type(session_cap) is not int or session_cap < 0:
            raise ValueError("session_cap_invalid")
        self.catalogue = catalogue_entries(load_recorded(RECORDED_PATH) if recorded is None else recorded)
        self.products = products
        self.budget = budget if budget is not None else CallBudget(ROUTE_CALL_BUDGET)
        self.session_cap = session_cap
        self._lock = threading.Lock()
        self._session_calls: OrderedDict[str, int] = OrderedDict()

    def _take_session_call(self, session_id: str | None) -> bool:
        """Count one live search against the session; ``False`` once its cap is reached."""
        if session_id is None:
            return True
        with self._lock:
            used = self._session_calls.get(session_id, 0)
            if used >= self.session_cap:
                return False
            self._session_calls[session_id] = used + 1
            self._session_calls.move_to_end(session_id)
            while len(self._session_calls) > MAX_ROUTE_SESSIONS:
                self._session_calls.popitem(last=False)
            return True

    def route(self, text: object, session_id: str | None = None) -> dict:
        result = route_case(text, self.catalogue)
        if result["route"] != "unknown" or result["query"] is None or getattr(self.products, "mode", "off") != "live":
            return result
        if self.budget.remaining <= 0 or not self._take_session_call(session_id):
            return result
        live = self.products.lookup(result["query"], budget=self.budget)
        if live["status"] != "FOUND":
            return result
        live_catalogue = catalogue_entries({"live": {"cards": live["cards"]}})
        matches, filtered_out = rank(_tokens(result["query"]), live_catalogue)
        if not matches:
            return result
        return {**result, "route": "physical", "reason": "live_catalogue_match", "matches": matches, "filtered_out": filtered_out,
                "items": _items("physical")}
