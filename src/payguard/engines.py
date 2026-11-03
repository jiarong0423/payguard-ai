"""Deterministic advisory engines for a local synthetic PayGuard prototype.

These functions perform no I/O and do not certify policy compliance, predict
account restrictions, or decide disputes. Their outputs are safe draft inputs
for a separate human review boundary.
"""

from datetime import datetime, timedelta, timezone
from decimal import Context, Decimal, InvalidOperation, localcontext
import re
import unicodedata
from payguard.policy import POLICY_VERSION, VelocityPolicy


_TRANSACTION_FIELDS = frozenset({"order_id", "amount", "currency", "occurred_at"})
_CASE_FIELDS = frozenset({
    "case_id", "order_id", "reason", "opened_at", "order_created_at",
    "carrier_status", "delivered_at", "evidence_source",
})
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
_CURRENCY = re.compile(r"[A-Z]{3}\Z")
_DECIMAL_TEXT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})\Z")
_BASELINE_PROVENANCE = frozenset({"SYNTHETIC_BASELINE", "CALLER_SUPPLIED_UNVERIFIED"})
# (attack r23) A promised percentage must be non-zero: "guaranteed 0% interest financing" is a store credit offer.
_PERCENT = r"(?<![0-9.])(?=[0-9.]*[1-9])[0-9]+(?:\.[0-9]+)?\s*(?:%|percent\b|per\s+cent\b)"
_GAIN = r"(?:roi|returns?|profits?|yields?|gains?|interest)"
# (attack r23) A rate per day/week/month ("earn 3% daily", "20% monthly returns") is how investment schemes are sold.
_PERIOD = r"(?:daily|weekly|monthly|(?:a|per|each|every)\s+(?:day|week|month))\b"
# (attack r22) The keyword table also carries the country pack's AUP-prohibited and pre-approval tags it can name
# (shared.aup_prohibited_tags: narcotics, drug_paraphernalia, cigarettes, stolen_goods, counterfeit, weapons,
# pyramid_schemes; shared.aup_preapproval_tags: gambling, e_cigarettes, tobacco_other), inflections ("counterfeiting",
# "gambled", "vaporizer") and the common synonyms ("meth", "Glock", "AAA mirror", "1:1 copy", "sportsbook"). The
# category names stay the five the API contract lists, so stolen goods sit with counterfeit goods (goods the seller has
# no right to sell) and pyramid schemes with unsupported financial promises. Intended matches a person then reviews:
# "fire arms of a sofa" (split "fire arm" is an evasion more often than furniture) and "vaporizer" (also a humidifier).
_AUP_CATEGORIES = (
    # (attack r23) "guaranteed ... profit" needs the profit promised ("guaranteed profits", "guaranteed monthly profit"), not
    # "satisfaction guaranteed! 10% of profit goes to a non-profit"; the rate may come before the guarantee ("earn 3% daily,
    # guaranteed"); "risk-free returns within 30 days" is a refund policy; MLM / recruit-and-get-paid is a pyramid pitch.
    ("unsupported_financial_promise", rf"\bguaranteed\b.{{0,80}}(?:{_PERCENT}\s*{_GAIN}\b|\b{_GAIN}\b.{{0,40}}{_PERCENT}|{_PERCENT}\s*{_PERIOD})"
                                      r"|\bguaranteed\s+(?:[a-z]+\s+){0,2}(?:profits?|roi)\b"
                                      rf"|{_PERCENT}\s*(?:{_GAIN}\s+)?{_PERIOD}.{{0,60}}\bguarantee[ds]?\b"
                                      rf"|{_PERCENT}\s*{_PERIOD}\s*{_GAIN}\b"
                                      rf"|\b(?:earn|earning|earns|make|making|get|receive|pays?|paying)\b.{{0,30}}{_PERCENT}\s*"
                                      r"(?:daily|weekly|(?:a|per|each|every)\s+(?:day|week))\b"
                                      r"|\b(?:double|triple)\s+your\s+(?:money|investment|cash|deposit|bitcoin|crypto)\b"
                                      r"|\brisk[- ]?free\s+(?:returns?\b(?!\s+(?:within|in\s+[0-9]|for\s+[0-9]|on\s+(?:all|any|every|your)|"
                                      r"policy|and\s+(?:exchanges?|refunds?)|&\s*(?:exchanges?|refunds?)|up\s+to))|profits?|investments?|income|trading)\b"
                                      r"|\b(?:pyramid|ponzi)\s+schemes?\b|\bponzi\b|\bmlm\b|\bmulti[- ]?level\s+marketing\b"
                                      r"|\brecruit(?:s|ed|ing)?\b.{0,40}\b(?:get|getting|earn|earning|be|are)\s+paid\b"),
    # Tools named "gun" (glue gun, nail gun, heat gun ...) are not weapons; more tool names are masked in _AUP_BENIGN.
    # (attack r23) AR-15 / AK-47, silencers and suppressors (not a surge or noise suppressor), switchblades, brass knuckles,
    # stun guns and tasers.
    ("weapons", r"\b(?:firearms?|fire\s+arms?|(?<!glue[ -])(?<!nail[ -])(?<!heat[ -])(?<!spray[ -])(?<!caulk[ -])(?<!staple[ -])(?<!massage[ -])(?<!bubble[ -])(?<!water[ -])"
                r"(?<!caulking[ -])(?<!grease[ -])guns?|handguns?|pistols?|rifles?|shotguns?|revolvers?|ammunitions?|ammo|explosives?|"
                r"glocks?|grenades?|detonators?|(?<!secret )weapons?|ar[- ]?15s?|ak[- ]?47s?|(?<!surge )(?<!noise )(?<!spark )(?<!exhaust )"
                r"(?<!echo )(?<!feedback )(?:silencers?|suppressors?)|switch[- ]?blades?|brass\s+knuckles?|knuckle[- ]?dusters?|"
                r"balisongs?|butterfly\s+kni(?:fe|ves)|tasers?)\b"),
    # (attack r23) Street and prescription names (MDMA, ecstasy pills, LSD, ketamine, oxycodone, Xanax, molly capsules,
    # "coke ... white powder") and common non-English spellings of cocaine (kokain, cocaína -> cocaina, kokaiini).
    # "Heroína" is left out: in Spanish it also means a heroine.
    ("controlled_substances", r"\b(?:cocaine|heroin|methamphetamines?|meth|crystal\s+meth|fentanyl|narcotics?|illegal\s+drugs?|"
                              r"drug\s+paraphernalia|mdma|lsd|ketamine|oxycodone|oxycontin|hydrocodone|percocet|xanax|alprazolam|"
                              r"psilocybin|cocaina|kokain[ae]?|kokaiini|metanfetamina|fentanilo|"
                              r"ecstasy\s+(?:pills?|tabs?|tablets?|rolls?|caps?|capsules?|powder|crystals?)|"
                              r"molly\s+(?:pills?|caps?|capsules?|crystals?|powder|rocks?)|blotter\s+(?:tabs?|acid|paper))\b"
                              r"|\bcoke\b.{0,40}\b(?:powder|[0-9]+\s*(?:g|grams?)|eight[- ]?ball|8[- ]?ball)\b"
                              r"|\bwhite\s+powder\b.{0,40}\bcoke\b"),
    # (attack r23) Fake identity documents and fake or prop money ("prop money that passes as real" stays a review item:
    # PayPal restricts play money that can pass as currency, so every "prop money" listing goes to a person).
    ("counterfeit_goods", r"\b(?:counterfeit(?:s|ed|ing|ers?)?|replicas?|knock-?offs?|bootlegs?|fake\s+(?:brands?|luxury|designer|"
                          r"rolex|gucci|chanel|prada|hermes|cartier|omega|nike|adidas|apple|louis\s+vuitton)|"
                          r"aaa\+*\s*(?:mirror|replicas?)|mirror\s+(?:copy|copies|replicas?)|"
                          r"fake\s+(?:passports?|ids?|id\s+cards?|identity\s+(?:cards?|documents?)|driver'?s?\s+licen[cs]es?|"
                          r"diplomas?|degrees?|money|bills|banknotes?|currency)|"
                          r"(?:novelty|scannable)\s+(?:ids?|id\s+cards?|driver'?s?\s+licen[cs]es?)|"
                          r"prop\s+(?:money|cash|bills|banknotes?|currency)|"
                          r"stolen\s+(?:goods|items|merchandise|property|products?))\b|(?<![0-9:])1\s*:\s*1\s+(?:copy|copies|replicas?|clones?)\b"),
    # (attack r23) Lottery tickets, Juul pods, snus, shisha and chewing tobacco need PayPal pre-approval.
    ("regulated_activity", r"\b(?:gambl(?:e|es|ed|er|ers|ing)|casinos?|betting|wagers?|sportsbooks?|e-?liquids?|vap(?:e|es|ed|er|ers|ing)|"
                           r"vapou?ri[sz]ers?|e-?cigarettes?|cigarettes?(?![ -]lighters?)|tobacco|nicotine|"
                           r"lottery\s+(?:tickets?|entries|entry|syndicates?)|online\s+lotter(?:y|ies)|juul|snus|shisha|"
                           r"(?:vape|nic|nicotine)\s+pods?)\b"),
)

# (attack r23) Ordinary retail wording that contains a keyword: compound nouns ("glue gun", "pistol grip shower head",
# "shotgun microphone"), colour words ("gun metal", "tobacco brown"), garment cuts ("bootleg jeans", "cigarette pants"),
# brand / media titles ("Rifle Paper Co.", "Top Gun", "Revolver" LP, "Weapons of Math Destruction", "The Gambler",
# "Grenade" protein bars, "Exploding Kittens", "Tobacco Vanille"), museum and fan replicas ("skull replica", "official
# replica jersey"), sweets ("candy cigarettes"), party props ("casino night ... decorations") and negations ("wager-free").
# Only the phrase itself is blanked before the keyword table runs, so any other keyword in the same text is still seen
# ("Top Gun poster and a Glock" is still flagged). A bare "replica", "vaporizer" or "casino" stays a review signal.
_AUP_BENIGN = re.compile(
    r"\b(?:temperature|thermometer|label(?:l?ing|ler)?|pricing|price|tattoo|rivet|nerf|foam\s+dart|squirt|paint|soldering|"
    r"tape|grout|sealant|silicone|radar|speed|hot\s+glue|glue|nail|heat|spray|caulk(?:ing)?|staple|massage|bubble|water|grease)"
    r"[ -]?guns?\b"
    r"|\bgun[ -]?(?:metal|dogs?)\b|\btop\s+gun\b"
    r"|\brifle\s+paper\b"
    r"|\bpistol[ -]grip\s+(?:shower\w*|hose|garden|spray\w*|nozzles?|drills?|saws?|watering|trigger\s+sprayers?)"
    r"|\bshotgun\s+(?:mics?|microphones?|condenser)\b"
    r"|\b(?:beatles(?:'s?)?\s+)?revolver\s+(?:vinyl|lp|album|cd|record|remix|remaster\w*|deluxe|box\s+set)\b|\bbeatles(?:'s?)?\s+revolver\b"
    r"|\bammo[ -]cans?(?=[ -](?:style|type|storage|organi[sz]ers?|tool\s*box))"
    r"|\bgrenade\s+(?:carb\s+killa\s+)?(?:protein|bars?|carb|shakes?)\b"
    r"|\bweapons\s+of\s+math\s+destruction\b"
    r"|\bexplo(?:ding|sive)\s+kittens\b"
    r"|\bcasino[ -](?:night|party|themed?)(?=.{0,40}\b(?:decorations?|decor|kit|balloons?|banners?|props?|costumes?|"
    r"invitations?|supplies|tablecloths?)\b)"
    r"|\bthe\s+gambler\b"
    r"|\bhumidifiers?\s+(?:and|&|/|or)\s+vapou?ri[sz]ers?\b|\bvapou?ri[sz]ers?\s+(?:and|&|/|or)\s+humidifiers?\b"
    r"|\b(?:candy|chocolate|bubble\s*gum|sweet|gum)\s+cigarettes?\b"
    r"|\bcigarette[ -](?:pants|trousers|jeans|leg|legs|skirts?|fit|cut)\b"
    r"|\btobacco\s+(?:vanill?e|oud|honey)\b|\btobacco[ -](?:brown|colou?r(?:ed)?|suede|tan|hue|shade)\b"
    r"|\bbootleg[ -](?:jeans|pants|trousers|denim|leggings|cut|fit|yoga\s+pants|flares?)\b"
    r"|\b(?:official|licensed)\s+replica\s+(?:jerseys?|shirts?|kits?|football\s+shirts?)\b"
    r"|\b(?:skull|fossil|skeleton|dinosaur|museum|tooth|teeth|claw|meteorite)\s+replicas?\b"
    r"|\breplicas?\s+(?:of\s+(?:a|an|the)\s+)?(?:fossils?|skulls?|skeletons?|dinosaurs?|teeth|tooth|claws?)\b"
    r"|\bwager[ -]?free\b"
)
_AUP_PATTERNS = tuple((category, re.compile(pattern)) for category, pattern in _AUP_CATEGORIES)


# Wording tricks the keyword check also sees through (red team R5): look-alike letters NFKC keeps (U+0261 "ɡun",
# Cyrillic/Greek vowels), digits for letters ("c0unterfeit"), separators inside a word ("counter-feit") and words
# spelled out letter by letter ("c o u n t e r f e i t"). The signal only asks a person to review; it decides nothing.
_LOOKALIKE = str.maketrans({"\u0261": "g", "\u0131": "i", "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
                            "\u0441": "c", "\u0443": "y", "\u0445": "x", "\u0456": "i", "\u03bf": "o", "\u03b1": "a"})
# (attack r22) "!" for i ("p!stol"), "(" for c ("(ocaine") and "9" for g ("9un").
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "9": "g", "@": "a", "$": "s",
                       "!": "i", "(": "c"})
# (attack r21) Marks and look-alikes NFKC keeps: combining marks ("co\u0336caine", "coca\u0308ine", "p\u00edstol"),
# more Greek/Cyrillic letters ("\u03f2ocaine") and filler / zero-width characters inside a word ("fire\u3164arm").
# Used only in an extra folded variant, so the text as typed is still checked unchanged.
_FOLD_LOOKALIKE = str.maketrans({
    "\u0261": "g", "\u0131": "i", "\u0251": "a", "\u025b": "e", "\u0269": "i", "\u0283": "s",
    # Cyrillic
    "\u0430": "a", "\u0432": "b", "\u0435": "e", "\u043a": "k", "\u043c": "m", "\u043d": "h", "\u043e": "o",
    "\u0440": "p", "\u0441": "c", "\u0442": "t", "\u0443": "y", "\u0445": "x", "\u0455": "s", "\u0456": "i",
    "\u0458": "j", "\u04bb": "h", "\u0501": "d", "\u051b": "q", "\u051d": "w", "\u0457": "i", "\u0491": "r",
    # Greek
    "\u03b1": "a", "\u03b2": "b", "\u03b5": "e", "\u03b9": "i", "\u03ba": "k", "\u03bd": "v", "\u03bf": "o",
    "\u03c1": "p", "\u03c4": "t", "\u03c5": "u", "\u03c7": "x", "\u03f2": "c", "\u03f3": "j", "\u03b7": "n",
    "\u03c9": "w", "\u03c3": "o", "\u03c2": "c",
    # (attack r22) Armenian, Coptic and Latin small capitals that NFKC keeps ("c\u0585caine", "\u1d04ocaine", "c\u2c9fcaine")
    "\u0585": "o", "\u0578": "n", "\u057d": "u", "\u0570": "h", "\u0581": "g", "\u0566": "q",
    "\u2c81": "a", "\u2c85": "r", "\u2c89": "e", "\u2c93": "i", "\u2c95": "k", "\u2c99": "m", "\u2c9b": "n",
    "\u2c9f": "o", "\u2ca1": "p", "\u2ca3": "p", "\u2ca5": "c", "\u2ca7": "t", "\u2ca9": "y", "\u2cad": "x",
    "\u1d00": "a", "\u0299": "b", "\u1d04": "c", "\u1d05": "d", "\u1d07": "e", "\ua730": "f", "\u0262": "g",
    "\u029c": "h", "\u026a": "i", "\u1d0a": "j", "\u1d0b": "k", "\u029f": "l", "\u1d0d": "m", "\u0274": "n",
    "\u1d0f": "o", "\u1d18": "p", "\u0280": "r", "\ua731": "s", "\u1d1b": "t", "\u1d1c": "u", "\u1d20": "v",
    "\u1d21": "w", "\u028f": "y", "\u1d22": "z",
    # (attack r23) Cherokee capitals that look like Latin letters ("\u13df\u13be\u13df\u13aa\u13c6NE"); casefold maps the small
    # Cherokee letters (U+AB70..) back to these capitals, and the table runs again after casefold.
    "\u13aa": "a", "\u13f4": "b", "\u13df": "c", "\u13a0": "d", "\u13ac": "e", "\u13c0": "g", "\u13bb": "h", "\u13a5": "i",
    "\u13c6": "i", "\u13ab": "j", "\u13e6": "k", "\u13de": "l", "\u13b7": "m", "\u13be": "o", "\u13eb": "o", "\u13e2": "p",
    "\u13a1": "r", "\u13da": "s", "\u13a2": "t", "\u13d9": "v", "\u13b3": "w", "\u13c3": "z",
    # (attack r23) Regional-indicator symbols (flag letters, U+1F1E6..U+1F1FF) read as a..z.
    **{chr(0x1F1E6 + offset): chr(ord("a") + offset) for offset in range(26)},
})
# Filler and invisible characters (Hangul fillers, zero-width, word joiner, BOM, ...) are dropped from the folded variant.
_FOLD_INVISIBLE = re.compile("[\u115f\u1160\u3164\uffa0\u17b4\u17b5\u180e\u200b-\u200f\u2060-\u2064\u206a-\u206f\ufeff\u034f\u00ad]")


def _aup_fold(raw: str) -> str:
    """(attack r21) NFKD, drop combining marks, map look-alikes to Latin and remove filler/invisible characters.

    Starts from the text as typed: NFKC would turn the lunate sigma U+03F2 ("\u03f2ocaine") into a plain sigma first."""
    text = _FOLD_INVISIBLE.sub("", raw).replace("\u03f9", "c").translate(_FOLD_LOOKALIKE)
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(char for char in decomposed if unicodedata.category(char) not in ("Mn", "Me", "Mc"))
    return unicodedata.normalize("NFKC", stripped).casefold().translate(_FOLD_LOOKALIKE)


# (attack r22) Punctuation that splits a word ("co/caine", "co'caine", "co,caine", "co+caine", "co|caine", "co·caine").
_AUP_SPLIT = "-._*/'‘’`,+|·•‧・"
_AUP_JOIN = re.compile(rf"(?<=[a-z0-9@$!(])[{re.escape(_AUP_SPLIT)}]+(?=[a-z0-9@$!(])")
# Runs of three or more single letters split by spaces or that punctuation, single or doubled ("c  o  c  a  i  n  e").
_AUP_SPELLED = re.compile(rf"\b(?:[a-z][\s{re.escape(_AUP_SPLIT)}]+){{2,}}[a-z]\b")


def _aup_forms(text: str) -> tuple[str, ...]:
    plain = text.translate(_LOOKALIKE)
    joined = _AUP_JOIN.sub("", plain)
    leet = re.sub(r"[a-z0-9@$!(]+", lambda m: m.group().translate(_LEET) if re.search(r"[a-z]", m.group()) else m.group(), joined)
    # "c o u n t e r f e i t" -> "counterfeit": runs of three or more single letters become one word.
    spelled = _AUP_SPELLED.sub(lambda m: re.sub(rf"[\s{re.escape(_AUP_SPLIT)}]+", "", m.group()), leet)
    return (text, plain, joined, leet, spelled)


def _aup_unglue(cased: str) -> tuple[str, str]:
    """(attack r22) Words glued so that \\b cannot see them: "buy_cocaine_now", "PremiumCocaine", "cocaine99".

    First form: underscores and camelCase boundaries become spaces (digits kept, so leet still reads "c0caine_now").
    Second form: a letter next to a digit is split as well ("cocaine99" -> "cocaine 99", "glock19" -> "glock 19")."""
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", cased).replace("_", " ").casefold()
    digits = re.sub(r"(?<=[^\W\d_])(?=\d)|(?<=\d)(?=[^\W\d_])", " ", spaced)
    return spaced, digits


def _aup_variants(normalized: str, raw: str | None = None, cased: str | None = None) -> tuple[str, ...]:
    forms = _aup_forms(normalized) + _aup_forms(_aup_fold(normalized if raw is None else raw))
    if cased is not None:
        for unglued in _aup_unglue(cased) + _aup_unglue(_aup_fold_cased(raw if raw is not None else cased)):
            forms += _aup_forms(unglued)
    return tuple(dict.fromkeys(forms))


def _aup_fold_cased(raw: str) -> str:
    """_aup_fold without the casefold, so camelCase is still visible after look-alikes are mapped."""
    text = _FOLD_INVISIBLE.sub("", raw).replace("Ϲ", "c")
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(char for char in decomposed if unicodedata.category(char) not in ("Mn", "Me", "Mc"))
    return unicodedata.normalize("NFKC", stripped)


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{field} must be a bounded identifier")
    return value


def _decimal(value: object, field: str, *, allow_zero: bool = False) -> Decimal:
    if not isinstance(value, str) or len(value) > 160 or not _DECIMAL_TEXT.fullmatch(value):
        raise ValueError(f"{field} must be a finite decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a finite decimal string") from exc
    if not result.is_finite() or result < 0 or (result == 0 and not allow_zero):
        raise ValueError(f"{field} must be {'nonnegative' if allow_zero else 'positive'} and finite")
    if len(result.as_tuple().digits) > 64 or abs(result.as_tuple().exponent) > 100:
        raise ValueError(f"{field} exceeds supported decimal precision")
    return result


def _time(value: object, field: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise ValueError(f"{field} must be an ISO timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError(f"{field} must include timezone")
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be an ISO timestamp with timezone") from exc


def _utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _number(value: Decimal) -> str:
    return format(value, "f")


def check_aup(description: str) -> dict:
    """Flag bounded text for review without offering policy evasion or certification."""
    if not isinstance(description, str) or not description.strip() or len(description) > 4000:
        raise ValueError("description must contain between 1 and 4000 characters")
    if any(unicodedata.category(char).startswith("C") for char in description):
        raise ValueError("description must not contain control or invisible characters")
    cased = unicodedata.normalize("NFKC", description)
    normalized = cased.casefold()
    # (attack r23) Known ordinary phrases are blanked in every variant before the keyword table runs.
    variants = tuple(dict.fromkeys(_AUP_BENIGN.sub(" ", variant) for variant in _aup_variants(normalized, description, cased)))
    findings = [
        {"category": category, "code": "keyword_requires_policy_review"}
        for category, pattern in _AUP_PATTERNS
        if any(pattern.search(variant) for variant in variants)
    ]
    return {
        "match_status": "REVIEW_SIGNAL" if findings else "NO_MATCH",
        "compliance_decision": "NOT_MADE",
        "findings": findings,
        "recommendation": (
            "Review the actual goods or activity against applicable policy. "
            "Do not disguise restricted activity through wording changes."
            if findings else
            "No configured demo keyword matched. Review the actual goods or activity "
            "against applicable policy; this result does not certify compliance."
        ),
        "policy_version": POLICY_VERSION,
        "advisory_only": True,
    }


def assess_velocity(
    transactions: list[dict],
    baseline_amount_per_hour: str,
    as_of: str,
    window_hours: int = 1,
    threshold: str = "3.5",
    *,
    baseline_provenance: str = "CALLER_SUPPLIED_UNVERIFIED",
    baseline_window_start: str | None = None,
    baseline_window_end: str | None = None,
) -> dict:
    """Compare a validated current amount/hour to a declared local baseline.

    Every row is validated, including rows outside the window. The window is
    (as_of - window_hours, as_of], and duplicate IDs are rejected across all
    rows. Decimal bounds are computational limits, not merchant policy limits.
    """
    if not isinstance(transactions, list) or len(transactions) > 10000:
        raise ValueError("transactions must be a list with at most 10000 rows")
    if type(window_hours) is not int or window_hours <= 0:
        raise ValueError("window_hours must be a positive integer")
    VelocityPolicy(threshold=threshold, window_hours=window_hours)
    baseline = _decimal(baseline_amount_per_hour, "baseline_amount_per_hour", allow_zero=True)
    limit = _decimal(threshold, "threshold")
    end = _time(as_of, "as_of")
    try:
        start = end - timedelta(hours=window_hours)
    except (OverflowError, TypeError) as exc:
        raise ValueError("window_hours exceeds supported timestamp range") from exc
    if not isinstance(baseline_provenance, str) or baseline_provenance not in _BASELINE_PROVENANCE:
        raise ValueError("baseline_provenance is outside the supported vocabulary")
    if baseline_window_start is None or baseline_window_end is None:
        raise ValueError("baseline provenance requires a complete comparison window")
    baseline_start = _time(baseline_window_start, "baseline_window_start")
    baseline_end = _time(baseline_window_end, "baseline_window_end")
    if not baseline_start < baseline_end <= start:
        raise ValueError("baseline window must precede and not overlap the observation window")
    normalized_baseline_start = _utc(baseline_start)
    normalized_baseline_end = _utc(baseline_end)
    ids = set()
    currencies = set()
    included = []
    excluded_future = 0
    excluded_past = 0
    for row in transactions:
        if not isinstance(row, dict) or set(row) != _TRANSACTION_FIELDS:
            raise ValueError("transaction fields must exactly match the transaction contract")
        order_id = _identifier(row["order_id"], "order_id")
        if order_id in ids:
            raise ValueError("duplicate order_id")
        ids.add(order_id)
        amount = _decimal(row["amount"], "amount")
        currency = row["currency"]
        if not isinstance(currency, str) or not _CURRENCY.fullmatch(currency):
            raise ValueError("currency must be an uppercase three-letter code")
        currencies.add(currency)
        if len(currencies) > 1:
            raise ValueError("transactions must use one currency")
        occurred = _time(row["occurred_at"], "occurred_at")
        if occurred > end:
            excluded_future += 1
        elif occurred <= start:
            excluded_past += 1
        else:
            included.append(amount)
    with localcontext(Context(prec=512)):
        total = sum(included, Decimal("0"))
        rate = total / Decimal(window_hours)
        ratio = None if baseline == 0 else rate / baseline
        # Compare the exact products, avoiding a rounded quotient at the boundary.
        alert = baseline != 0 and total > baseline * Decimal(window_hours) * limit
        result = {
            "status": "insufficient_baseline" if baseline == 0 else ("review_velocity" if alert else "normal"),
            "window_start": _utc(start),
            "window_end": _utc(end),
            "window_hours": window_hours,
            "window_boundary": "left_open_right_closed",
            "transaction_count": len(included),
            "excluded_future_count": excluded_future,
            "excluded_past_count": excluded_past,
            "currency": next(iter(currencies), None),
            "total_amount": _number(total),
            "current_amount_per_hour": _number(rate),
            "baseline_amount_per_hour": _number(baseline),
            "baseline_provenance": baseline_provenance,
            "baseline_window_start": normalized_baseline_start,
            "baseline_window_end": normalized_baseline_end,
            "ratio": None if ratio is None else _number(ratio),
            "threshold": _number(limit),
            "alert": bool(alert),
            "policy_version": POLICY_VERSION,
            "advisory_only": True,
            "limitations": [
                "The baseline is synthetic or caller-supplied and is not a PayPal risk threshold.",
                "A velocity alert is a review signal and does not predict account restrictions.",
            ],
        }
    return result


def prepare_dispute(case: dict) -> dict:
    """Build objective synthetic evidence for human review; never decide a case."""
    if not isinstance(case, dict) or not set(case).issubset(_CASE_FIELDS):
        raise ValueError("case contains fields outside the evidence allowlist")
    if case.get("evidence_source") != "synthetic":
        raise ValueError("only explicitly synthetic evidence is accepted")
    evidence = {"evidence_source": "synthetic"}
    review_reasons = []
    for field in ("case_id", "order_id"):
        value = case.get(field)
        if value is None or value == "":
            review_reasons.append(f"missing_{field}")
        else:
            evidence[field] = _identifier(value, field)
    reason = case.get("reason")
    if reason is None or reason == "":
        review_reasons.append("missing_reason")
    else:
        evidence["reason"] = _identifier(reason, "reason")
        if reason != "INR":
            review_reasons.append("unsupported_reason")
    timestamps = {}
    for field in ("opened_at", "order_created_at"):
        value = case.get(field)
        if value is None or value == "":
            review_reasons.append(f"missing_{field}")
        else:
            timestamps[field] = _time(value, field)
            evidence[field] = _utc(timestamps[field])
    carrier_status = case.get("carrier_status")
    if carrier_status is None or carrier_status == "":
        review_reasons.append("missing_carrier_status")
    else:
        if carrier_status not in ("delivered", "in_transit", "not_shipped", "unknown"):
            raise ValueError("carrier_status is outside the allowed status vocabulary")
        evidence["carrier_status"] = carrier_status
        if carrier_status != "delivered":
            review_reasons.append("delivery_not_confirmed")
    delivered_value = case.get("delivered_at")
    if delivered_value is None or delivered_value == "":
        if carrier_status == "delivered":
            review_reasons.append("missing_delivered_at")
    else:
        timestamps["delivered_at"] = _time(delivered_value, "delivered_at")
        evidence["delivered_at"] = _utc(timestamps["delivered_at"])
    created = timestamps.get("order_created_at")
    opened = timestamps.get("opened_at")
    delivered = timestamps.get("delivered_at")
    if created is not None and opened is not None and created > opened:
        review_reasons.append("order_created_after_dispute")
    if created is not None and delivered is not None and delivered < created:
        review_reasons.append("delivery_before_order")
    if delivered is not None and opened is not None and delivered >= opened:
        review_reasons.append("delivery_not_before_dispute")
    if delivered is not None and carrier_status not in (None, "", "delivered"):
        review_reasons.append("carrier_timestamp_conflict")
    return {
        "case_id": evidence.get("case_id"),
        "status": "manual_review" if review_reasons else "review_evidence",
        "evidence": evidence,
        "review_reasons": review_reasons,
        "recommendation": "A human reviewer must verify the evidence and applicable case requirements before taking any action.",
        "limitations": [
            "All evidence is synthetic and has not been verified against a carrier or payment provider.",
            "A delivery event does not establish buyer intent or determine a dispute outcome.",
            "This draft does not submit evidence or authorize any financial action.",
        ],
        "policy_version": POLICY_VERSION,
        "advisory_only": True,
    }
