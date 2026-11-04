"""Session-scoped guided gap filling routes (demo and live modes).

POST /api/v1/guide/start  {scenario, goods_type}  new guide for this demo session
POST /api/v1/guide/turn   {text}                  one seller message through evidence_guide.guide_turn
POST /api/v1/guide/review {confirm | change}      the summary confirmation: confirm, or reopen named items
POST /api/v1/guide/form   {item, value}           one form field through the rule layer
GET  /api/v1/guide/state                          current gap table and last fixed reply

The same session, CSRF, origin, host and body guards as every other route apply (LocalBoundaryMiddleware
plus read_session / write_session). The chooser is the keyword baseline unless guide_model builds a
Gemini chooser (PAYGUARD_GUIDE_MODEL=gemini and the Gemini profile configured). Every model call goes
through a controlled_fallback.Governor: per (session, situation), spacing, global, daily, in-flight and
breaker caps
plus a timeout. On a refusal, a timeout, a provider error or an invalid reply the keyword chooser answers
and the response says chooser "keyword_fallback".

Only code marks an item STRUCTURALLY_PRESENT, never the model: a form value (/guide/form, or the fixed fields
sent with /guide/turn) that passes the rule check below, or a closed value the rule layer reads from the
seller's words (evidence_guide.auto_confirm in /guide/turn, same validator) (r32 J3).
Neither seller text nor form values are stored or echoed; the server keeps statuses and weekday hints.
"""

from __future__ import annotations

import concurrent.futures
import copy
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import os
import re
import threading
import time
from typing import Annotated, Literal, Optional

from fastapi import Depends
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator

from payguard import evidence_guide as eg
from payguard.controlled_fallback import MAX_PROVIDER_IN_FLIGHT, Governor

from .guide_model import GUIDE_WORKER_TIMEOUT_SECONDS, configured_guide_chooser, guide_model_requested
from .store import BoundaryError

GUIDE_CONTRACT = 2
MAX_GUIDE_TURNS = 40
# (attack r22) /guide/form had no cap: one guide (demo session + situation) takes at most this many form saves. Nine
# items with three tries each is 27; the rest is room for Change and Not sure. Like the turn count, it survives a
# restart of the guide and Reset demo.
MAX_GUIDE_FORM_ROUNDS = 60
# (attack r22) Velocity dates checked against each other: the normal week must come before the spike.
PERIOD_ITEMS = ("baseline_period", "surge_period")
GUIDE_MODEL_CALLS_PER_SESSION = 10
GUIDE_MODEL_MIN_SPACING_SECONDS = 2.0
# (r32 hosted guide, owner decision 2026-11-04) The hosted demo may use Gemini for the guide only, on a free-tier key,
# when the operator sets this to "gemini" (plus the usual PAYGUARD_GUIDE_MODEL / transport / key). Unset, it stays on
# the keyword chooser and no worker can start. Its shared caps sit under the free tier, which owner checks on 2026-11-04
# put at about 5 to 15 requests a minute and about 20 a day for gemini-3.8-flash; past them the guide stays on keywords.
HOSTED_GUIDE_MODEL_ENV = "PAYGUARD_HOSTED_GUIDE_MODEL"
HOSTED_GUIDE_CALLS_PER_MINUTE = 5
HOSTED_GUIDE_CALLS_PER_DAY = 20
GUIDE_MODEL_DEADLINE_SECONDS = 30.0  # governed: the model result must arrive within this, or the keyword answer stays
MIN_RESEND_SECONDS = 1.0  # the one identical resend is skipped when less time than this is left
assert GUIDE_WORKER_TIMEOUT_SECONDS < GUIDE_MODEL_DEADLINE_SECONDS
MAX_FORM_VALUE_CHARS = eg.MAX_FIXED_VALUE_CHARS
DATE_LOOKBACK_DAYS = eg.DATE_LOOKBACK_DAYS

Scenario = Literal["preflight", "velocity", "dispute"]
GoodsType = Literal["physical", "digital"]
Status = Literal["STRUCTURALLY_PRESENT", "PARTIAL", "UNCLEAR", "CONFLICTING", "MISSING", "NOT_APPLICABLE"]
TemplateId = Literal[tuple(eg.TEMPLATES)]
ChooserUsed = Literal["none", "keyword", "model", "keyword_fallback", "form"]
FallbackReason = Literal["budget", "provider_error", "invalid_reply", "late", "no_items"]
AnalysisStatus = Literal["analysing", "replaced", "kept"]
AnalysisReason = Literal["budget", "provider_error", "invalid_reply", "late", "no_items", "superseded"]


# ---- form fields: the rule layer -------------------------------------------------------------
# Stage A fixed inputs are defined in evidence_guide next to SCENARIOS; this module only applies them.
FORM_FIELDS = eg.FIXED_INPUTS
ROUND_TEMPLATES = ("REQUEST", "ONE", "CONFIRM_DATE", "DONE", "PROGRESS", "OPEN")
MAX_FIELD_ATTEMPTS = 3  # invalid tries per fixed input before the item moves to "describe it in your own words"


def validate_form_value(scenario, item, value, today):
    """True only when the single field passes its rule (evidence_guide.validate_fixed_input).
    The value is never stored or returned. NOT_SURE and SKIP are never valid; they defer the item."""
    return eg.validate_fixed_input(scenario, item, value, today)


# ---- request / response contract -------------------------------------------------------------
class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class GuideStartRequest(_Strict):
    scenario: Scenario
    goods_type: Optional[GoodsType] = None


class GuideTurnRequest(_Strict):
    # Which situation's guide this is for. Each situation keeps its own guide; omitted = the one started last.
    scenario: Optional[Scenario] = None
    text: StrictStr = Field(min_length=1, max_length=eg.MAX_INPUT_CHARS * 4)
    # The first screen can send the sentence and the asked fixed inputs with one Save (one round, not two).
    fields: Optional[list["GuideField"]] = Field(default=None, min_length=1, max_length=eg.ITEMS_PER_ROUND)


ItemId = Annotated[StrictStr, Field(min_length=1, max_length=40, pattern=r"^[a-z_]+$")]
FieldValue = Annotated[StrictStr, Field(min_length=1, max_length=MAX_FORM_VALUE_CHARS)]


class GuideField(_Strict):
    item: ItemId
    value: FieldValue


class GuideFormRequest(_Strict):
    """One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both."""
    scenario: Optional[Scenario] = None
    item: Optional[ItemId] = None
    value: Optional[FieldValue] = None
    fields: Optional[list[GuideField]] = Field(default=None, min_length=1, max_length=eg.ITEMS_PER_ROUND)
    # The last round shows the summary of items taken from the seller's words; one Save can fill and confirm it.
    confirm_review: bool = False

    @model_validator(mode="after")
    def one_shape(self):
        single = self.item is not None or self.value is not None
        if single == (self.fields is not None) or (single and (self.item is None or self.value is None)):
            raise ValueError("guide_form_shape_invalid")
        if self.fields is not None and len({field.item for field in self.fields}) != len(self.fields):
            raise ValueError("guide_form_duplicate_item")
        return self

    def pairs(self):
        return [(self.item, self.value)] if self.fields is None else [(field.item, field.value) for field in self.fields]


class GuideOption(_Strict):
    value: StrictStr
    label: StrictStr


class GuideForm(_Strict):
    kind: Literal["date", "choice", "text"]
    options: list[GuideOption]
    placeholder: Optional[StrictStr]


class GuideItem(_Strict):
    id: StrictStr
    label: StrictStr
    status: Status
    source: Literal["OFFICIAL", "SUGGESTION"]
    chunk: Optional[StrictStr]
    form: Optional[GuideForm]


class GuideGap(_Strict):
    missing: list[StrictStr]
    partial: list[StrictStr]
    conflicting: list[StrictStr]
    present: list[StrictStr]


class GuideDropped(_Strict):
    item: StrictStr
    reason: Literal["other_party", "inferred"]


class GuideReply(_Strict):
    template: TemplateId
    text: StrictStr = Field(min_length=1, max_length=400)
    chooser: ChooserUsed
    state_changed: bool
    dropped: list[GuideDropped]
    fallback_reason: Optional[FallbackReason]


class GuideFormResult(_Strict):
    item: StrictStr
    valid: bool


class GuideFieldResult(_Strict):
    item: StrictStr
    valid: bool
    deferred: bool


class GuideSubtraction(_Strict):
    needed: int
    taken: int
    left: int
    text: StrictStr


class GuideAnalysis(_Strict):
    turn: int
    status: AnalysisStatus
    reason: Optional[AnalysisReason]


class GuideReviewRow(_Strict):
    item: StrictStr
    source: Literal["words", "words_pending"]
    value: StrictStr = Field(max_length=MAX_FORM_VALUE_CHARS)


class GuideReviewRequest(_Strict):
    scenario: Optional[Scenario] = None
    confirm: bool = False
    change: list[ItemId] = Field(default_factory=list, max_length=9)


class GuideStateResponse(_Strict):
    schema_version: Literal[1]
    started: bool
    scenario: Optional[Scenario]
    goods_type: Optional[GoodsType]
    flow_name: Optional[StrictStr]
    items: list[GuideItem]
    gap: GuideGap
    reply: Optional[GuideReply]
    form_result: Optional[GuideFormResult]
    form_results: list[GuideFieldResult]
    analysis: Optional[GuideAnalysis]
    asked: list[StrictStr] = Field(max_length=eg.ITEMS_PER_ROUND)
    stage: Optional[Literal["funnel", "echo", "fill", "review", "done"]]
    subtraction: Optional[GuideSubtraction]
    deferred: list[StrictStr]
    prefill: dict[StrictStr, StrictStr]
    auto_confirmed: list[StrictStr]  # settled by the rule layer from the last typed sentence, no click
    review: list["GuideReviewRow"]  # the one summary to confirm (only in the review stage)
    rounds_used: int
    turns_used: int
    turns_limit: int
    chooser_mode: Literal["keyword", "gemini"]
    model_requested: bool
    model_text_shown: Literal[False]
    values_stored: Literal[False]
    advisory_only: Literal[True]


# ---- governed model call ---------------------------------------------------------------------
class _Refused(Exception):
    pass


_MODEL_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROVIDER_IN_FLIGHT, thread_name_prefix="guide-model")


def _call_with_deadline(governor, provider, request, timeout):
    """Run one provider call on the guide pool under the Governor's in-flight cap; give up after timeout."""
    if timeout <= 0:
        raise TimeoutError()
    if not governor.begin_call():
        raise _Refused("busy")
    try:
        future = _MODEL_POOL.submit(provider, request)
    except Exception:
        governor.end_call()
        raise
    future.add_done_callback(governor.end_call)
    try:
        return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError:
        future.cancel()
        raise TimeoutError() from None


def governed_model_rows(governor, key, provider, request, scenario, deadline, clock=time.monotonic, client_id=None):
    """The single model step of a turn: Governor.admit, one call, one identical resend when the reply
    fails the closed check (Governor.extra_attempt), all before the deadline.

    Returns (rows, reason): validated rows and None, or None and budget / late / provider_error / invalid_reply.
    ``client_id`` keys the per-client daily cap (r25 R5 P2-3); the per-session count stays keyed by ``key``.
    """
    refused, _previous = governor.admit(key, uses_model=True, client_id=client_id)
    if refused is not None:
        return None, "budget"
    failed = False
    reason = "invalid_reply"
    try:
        for attempt in range(2):
            remaining = deadline - clock()
            if attempt:
                if remaining < MIN_RESEND_SECONDS:
                    break
                if not governor.extra_attempt():
                    reason = "budget"
                    break
            try:
                raw = _call_with_deadline(governor, provider, request, remaining)
            except _Refused:
                reason = "budget"
                break
            except TimeoutError:
                failed, reason = True, "late"
                break
            except Exception:
                failed, reason = True, "provider_error"
                break
            rows = eg.validate_increments(raw, scenario, GUIDE_CONTRACT)
            if rows is not None and all(row["k"] < len(request["clauses"]) and row["c"] in request["slots"] for row in rows):
                return rows, None
    finally:
        governor.finish(key, failed)
    return None, reason


def model_request(snapshot, text, skip_clauses=()):
    """What the model may see for this turn: only clauses whose grammatical subject is not a buyer or a
    third party (reported speech never reaches the model), minus clauses the rule layer already settled
    in full (skip_clauses). Returns (request, original clause indices) or (None, None)."""
    cleaned, _reason = eg.sanitize_input(text)
    if cleaned is None or eg.route_policy(cleaned) is not None:
        return None, None
    clauses = eg.split_clauses(cleaned)
    kept = eg.model_clause_indices(clauses, skip_clauses)
    if not kept:
        return None, None
    request = eg.chooser_request([clauses[index] for index in kept], snapshot["scenario"], snapshot, GUIDE_CONTRACT)
    # Stage B: the model sees only items that are still open; settled items are never listed.
    request["slots"] = {slot: status for slot, status in request["slots"].items() if status != "STRUCTURALLY_PRESENT"}
    if not request["slots"]:
        return None, None
    return request, kept


# ---- per-session guide state -----------------------------------------------------------------
@dataclass
class GuideSession:
    state: dict
    turns: int = 0
    reply: Optional[dict] = None
    form_result: Optional[dict] = None
    conflicts: dict = field(default_factory=dict)
    analysis: Optional[dict] = None
    form_results: list = field(default_factory=list)
    deferred: set = field(default_factory=set)  # items the seller marked Not sure or skipped: stage B
    prefill: dict = field(default_factory=dict)  # echo: closed values (a date, a carrier option) the seller must confirm
    auto_confirmed: list = field(default_factory=list)  # items the rule layer settled from the last typed sentence
    word_values: dict = field(default_factory=dict)  # closed values taken from the seller's words (for the summary only)
    review_done: bool = False  # the final summary was confirmed once
    attempts: dict = field(default_factory=dict)  # invalid fixed-input attempts per item (three, then describe it instead)
    round: Optional[dict] = None
    rounds: int = 0
    form_rounds: int = 0  # (attack r22) form saves, capped by MAX_GUIDE_FORM_ROUNDS
    # (attack r22) The two velocity dates, only to check their order; never returned, dropped with the guide.
    period_dates: dict = field(default_factory=dict, repr=False)
    sequence: int = 0  # every turn and form entry; a pending model result applies only if nothing came after it
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)


_UNSET = object()


def select_guide_chooser():
    """The one place the chooser is chosen: a Gemini chooser or None (keyword baseline).
    Demo mode can replace this function (or pass chooser_factory) to force the keyword chooser."""
    return configured_guide_chooser()


def _new_governor():
    return Governor(max_calls=GUIDE_MODEL_CALLS_PER_SESSION, min_spacing=GUIDE_MODEL_MIN_SPACING_SECONDS)


def hosted_guide_service(store, environ=None):
    """(r32) The hosted demo's guide: the keyword chooser, unless the operator opted in with HOSTED_GUIDE_MODEL_ENV.
    Opted in, it takes the default factory (so PAYGUARD_GUIDE_MODEL and the transport still decide) under lower caps."""
    environ = os.environ if environ is None else environ
    if environ.get(HOSTED_GUIDE_MODEL_ENV) != "gemini":
        return GuideService(store, chooser_factory=lambda: None)
    governor = Governor(max_calls=GUIDE_MODEL_CALLS_PER_SESSION, min_spacing=GUIDE_MODEL_MIN_SPACING_SECONDS,
                        global_per_minute=HOSTED_GUIDE_CALLS_PER_MINUTE, global_per_day=HOSTED_GUIDE_CALLS_PER_DAY)
    return GuideService(store, governor=governor)


class GuideService:
    def __init__(self, store, *, chooser_factory=None, governor=None, clock=None, max_turns=MAX_GUIDE_TURNS,
                 model_deadline_seconds=GUIDE_MODEL_DEADLINE_SECONDS, rule_confirm=True, review_flow=None,
                 max_form_rounds=MAX_GUIDE_FORM_ROUNDS):
        self.store = store
        # Review flow (owner decision 2026-11-01, follows Lex / Alexa practice): values taken from the seller's words
        # are not confirmed one by one; they wait, and one summary at the end is confirmed before the guide is done.
        self.review_flow = rule_confirm if review_flow is None else review_flow
        # Hybrid (owner decision 2026-11-01): the rule layer settles closed values it reads for certain from the
        # seller's own unhedged words; only the rest goes to echo, the form and the model. False = echo-only flow.
        self.rule_confirm = rule_confirm
        self.chooser_factory = chooser_factory if chooser_factory is not None else (lambda: select_guide_chooser())
        # Only the default factory reads PAYGUARD_GUIDE_MODEL; an injected factory (the hosted demo passes
        # lambda: None) is the whole truth, so a leftover env flag can never report a model as requested.
        self._factory_reads_env = chooser_factory is None
        self.governor = governor if governor is not None else _new_governor()
        self.clock = clock
        self.max_turns = max_turns
        self.max_form_rounds = max_form_rounds
        # (attack r22) Turns and form saves used per (demo session, situation). /guide/start and Reset demo used to
        # hand out a fresh 40-turn count; the count now lives as long as the demo session does.
        self._spent: dict[tuple[str, str], tuple[int, int]] = {}
        self.model_deadline_seconds = model_deadline_seconds
        # (optimise r24) The app's per-session AI audit log (counts and timings only); None records nothing.
        self.ai_usage = None
        # One guide per (demo session, situation): the three situations never share state, answers or budget.
        self._sessions: dict[tuple[str, str], GuideSession] = {}
        self._latest: dict[str, str] = {}  # situation started last, for callers that name none
        self._lock = threading.Lock()
        self._jobs = concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="guide-analysis")
        self._pending: set = set()

    # session bookkeeping
    def _purge(self):
        with self.store.lock:
            live = set(self.store.sessions)
        for key in [key for key in self._sessions if key[0] not in live]:
            del self._sessions[key]
        for key in [key for key in self._latest if key not in live]:
            del self._latest[key]
        for key in [key for key in self._spent if key[0] not in live]:
            del self._spent[key]

    def forget(self, session_id):
        """(attack r21) Reset demo: drop every guide of this demo session, like the store and the country check.

        Model-call budgets (the Governor) are left alone on purpose: a reset never refills them. A background analysis
        still running writes into the dropped guide object only, which nothing reads any more."""
        with self._lock:
            for key in [key for key in self._sessions if key[0] == session_id]:
                self._keep_spent(key, self._sessions[key])
                del self._sessions[key]
            self._latest.pop(session_id, None)

    def _keep_spent(self, key, guide):
        """(attack r22) Remember the turns and form saves a guide used before it is replaced or dropped."""
        turns, forms = self._spent.get(key, (0, 0))
        self._spent[key] = (max(turns, guide.turns), max(forms, guide.form_rounds))

    def _get(self, session, scenario=None):
        with self._lock:
            self._purge()
            scenario = scenario or self._latest.get(session.session_id)
            return self._sessions.get((session.session_id, scenario)) if scenario else None

    def _require(self, session, scenario=None):
        guide = self._get(session, scenario)
        if guide is None:
            raise BoundaryError(409, "guide_not_started")
        return guide

    @staticmethod
    def _governor_key(session, scenario):
        # Per situation: model calls used by one situation's guide never block another's.
        return hashlib.sha256(("guide:" + scenario + ":" + session.session_id).encode("ascii")).hexdigest()[:32]

    @staticmethod
    def _client_id(session):
        """(r25 R5 P2-3) The session's client key (server-observed address) for the per-client daily cap, else "local"."""
        key = getattr(session, "client_key", None)
        return key if type(key) is str and 0 < len(key) <= 64 else "local"

    def _today(self):
        now = (self.clock or self.store.clock)()
        return now.astimezone(timezone.utc).date()

    def _chooser_status(self, provider=_UNSET):
        """(chooser_mode, model_requested), both derived from the real chooser_factory.

        chooser_mode is "gemini" only when the factory returns a chooser. model_requested is true when it
        does, or when the default factory saw PAYGUARD_GUIDE_MODEL=gemini but the profile is not configured.
        Building a chooser makes no model call.
        """
        if provider is _UNSET:
            provider = self.chooser_factory()
        if provider is not None:
            return "gemini", True
        return "keyword", self._factory_reads_env and guide_model_requested()

    def _chooser_mode(self):
        return self._chooser_status()[0]

    # rendering
    def _review_rows(self, guide):
        """Items the rule layer settled from the seller's words, with their closed values (the summary rows)."""
        if not self.review_flow or guide.review_done:
            return []
        return [{"item": slot, "source": "words", "value": guide.word_values[slot]}
                for slot in eg.SCENARIOS[guide.state["scenario"]]["slots"]
                if slot in guide.word_values and guide.state["slots"][slot]["status"] == "STRUCTURALLY_PRESENT"]

    def _is_last_round(self, guide, round_):
        open_ids = set(eg.open_items(guide.state))
        return bool(open_ids) and open_ids <= set(round_["asked"])

    def _compute_round(self, guide):
        """Up to three open items (echo confirmations first). Items settled from the seller's words are listed once:
        on the same screen as the last round (one Save fills it and confirms the summary), or, when nothing is left
        to fill, in one REVIEW round. Nothing extra when no item came from the seller's words."""
        if eg.open_items(guide.state):
            return eg.next_round(guide.state, guide.deferred, guide.prefill)
        rows = self._review_rows(guide)
        if rows:
            labels = eg.gap(guide.state)["labels"]
            lines = ", ".join(f"{labels[row['item']]} {row['value']}" for row in rows)
            if len(lines) > 120:  # template variables are capped; the full list is in the review field
                lines = f"{len(rows)} items taken from what you wrote, listed below"
            return {"template": "REVIEW", "text": eg.render("REVIEW", lines=lines), "asked": [], "stage": "review"}
        return eg.next_round(guide.state, guide.deferred, guide.prefill)

    def _round_message(self, guide):
        """The round message: CONFLICT first when two weekdays clash, otherwise the computed round (up to three items)."""
        guide.round = self._compute_round(guide)
        conflicting = eg.gap(guide.state)["conflicting"]
        if conflicting and guide.conflicts.get(conflicting[0]):
            pair = guide.conflicts[conflicting[0]]
            return "CONFLICT", eg.render("CONFLICT", weekday_a=eg.WEEKDAY_NAMES[pair[0]], weekday_b=eg.WEEKDAY_NAMES[pair[1]])
        return guide.round["template"], guide.round["text"]

    def _refresh_prefill(self, guide, before=None, text=None):
        """Closed suggestions only: a date computed from the weekday hint, a carrier option named in the text.
        Mapped items leave stage B (the seller now confirms them with the fixed input)."""
        today = self._today()
        for slot_id, slot in guide.state["slots"].items():
            if slot["status"] in ("STRUCTURALLY_PRESENT", "NOT_APPLICABLE"):
                guide.prefill.pop(slot_id, None)
                guide.deferred.discard(slot_id)
                continue
            touched = before is not None and before["slots"][slot_id] != slot
            if touched:
                guide.deferred.discard(slot_id)
            if slot_id in guide.deferred:
                continue  # the seller said Not sure: no echo until they describe it again
            if slot_id in eg.DATE_SLOTS:
                date_value = eg.prefill_date(slot["hint"], today)
                if date_value and eg.validate_fixed_input(guide.state["scenario"], slot_id, date_value, today):
                    if guide.prefill.get(slot_id) != date_value:
                        guide.review_done = False
                    guide.prefill[slot_id] = date_value
            if slot_id == "carrier" and touched and text is not None:
                carrier = eg.prefill_carrier(text)
                if carrier:
                    if guide.prefill.get(slot_id) != carrier:
                        guide.review_done = False
                    guide.prefill[slot_id] = carrier

    def _reply_for(self, guide, result):
        """Policy, other-party, unclear and conflict answers stand; a state change gets the round message."""
        if result["template"] in ROUND_TEMPLATES:
            template, text = self._round_message(guide)
            result = dict(result, template=template, text=text)
        else:
            guide.round = self._compute_round(guide)
        return result

    def _view(self, guide, provider=_UNSET):
        mode, requested = self._chooser_status(provider)
        base = {"schema_version": 1, "turns_limit": self.max_turns, "chooser_mode": mode, "model_requested": requested,
                "model_text_shown": False, "values_stored": False, "advisory_only": True}
        if guide is None:
            return dict(base, started=False, scenario=None, goods_type=None, flow_name=None, items=[],
                        gap={"missing": [], "partial": [], "conflicting": [], "present": []}, reply=None, form_result=None,
                        form_results=[], analysis=None, asked=[], stage=None, subtraction=None, deferred=[], prefill={}, auto_confirmed=[], review=[],
                        rounds_used=0, turns_used=0)
        state = guide.state
        scenario = state["scenario"]
        spec = eg.SCENARIOS[scenario]["slots"]
        items = []
        for slot_id, row in spec.items():
            status = state["slots"][slot_id]["status"]
            items.append({"id": slot_id, "label": row[0], "status": status, "source": row[1], "chunk": row[2],
                          "form": None if status == "NOT_APPLICABLE" else FORM_FIELDS[scenario][slot_id]})
        g = eg.gap(state)
        current = guide.round or self._compute_round(guide)
        return dict(base, started=True, scenario=scenario, goods_type=state["goods_type"], flow_name=eg.SCENARIOS[scenario]["flow_name"],
                    items=items, gap={key: g[key] for key in ("missing", "partial", "conflicting", "present")},
                    reply=guide.reply, form_result=guide.form_result, form_results=list(guide.form_results), analysis=guide.analysis,
                    asked=list(current["asked"]), stage=current["stage"], subtraction=eg.subtraction(state),
                    deferred=[slot for slot in spec if slot in guide.deferred],
                    prefill={slot: guide.prefill[slot] for slot in spec if slot in guide.prefill},
                    auto_confirmed=[slot for slot in spec if slot in guide.auto_confirmed],
                    review=self._review_rows(guide) if current["stage"] == "review" or self._is_last_round(guide, current) else [],
                    rounds_used=guide.rounds, turns_used=guide.turns)

    # operations
    def state(self, session, scenario=None):
        return self._view(self._get(session, scenario))

    def start(self, session, scenario, goods_type):
        if (scenario == "dispute") != (goods_type is not None):
            raise BoundaryError(422, "guide_goods_type_invalid")
        state = eg.new_state(scenario, goods_type)
        if scenario == "dispute":
            eg.choose_goods_type(state, goods_type)
        guide = GuideSession(state=state)
        template, text = self._round_message(guide)
        guide.reply = {"template": template, "text": text, "chooser": "none", "state_changed": False, "dropped": [], "fallback_reason": None}
        key = (session.session_id, scenario)
        with self._lock:
            self._purge()
            previous = self._sessions.get(key)
            if previous is not None:
                self._keep_spent(key, previous)
            guide.turns, guide.form_rounds = self._spent.get(key, (0, 0))
            self._sessions[key] = guide
            self._latest[session.session_id] = scenario
        return self._view(guide)

    def _record(self, guide, result, fallback_reason=None):
        if result["template"] == "CONFLICT":
            for slot_id, slot in guide.state["slots"].items():
                if slot["status"] == "CONFLICTING" and slot["hint"] and guide.conflicts.get(slot_id) is None:
                    guide.conflicts[slot_id] = self._conflict_pair(result["text"])
        guide.reply = {
            "template": result["template"],
            "text": result["text"],
            "chooser": result["chooser"],
            "state_changed": result["state_changed"],
            "dropped": [{"item": item, "reason": reason} for item, reason in result.get("dropped", [])],
            "fallback_reason": fallback_reason,
        }

    def turn(self, session, text, fields=None, scenario=None):
        """Answer at once with the keyword chooser; if a model chooser is configured and some clause may be
        sent, run the single governed model step in the background. A valid reply within the deadline
        replaces this turn's keyword mapping (same step, not a second one); otherwise the keyword answer stays."""
        guide = self._require(session, scenario)
        job = None
        with guide.lock:
            if fields:
                self._check_fields(guide, fields)
            provider = self.chooser_factory()
            budget_ok = guide.turns < self.max_turns
            guide.turns = min(guide.turns + 1, self.max_turns)
            guide.sequence += 1
            snapshot, conflicts = copy.deepcopy(guide.state), copy.deepcopy(guide.conflicts)
            side = {"prefill": dict(guide.prefill), "deferred": set(guide.deferred)}
            guide.rounds += 1
            result = eg.guide_turn(guide.state, text, chooser=None, budget_ok=budget_ok, contract=GUIDE_CONTRACT)
            # Hybrid: the rule layer settles what it reads for certain (closed value + validator), at once and
            # without a model; the same items are settled in the snapshot the model step starts from.
            settled, resolved = ([], set())
            if self.rule_confirm and result["chooser"] == "keyword":
                settled, resolved = eg.auto_confirm(guide.state, text, self._today())
                for item, clause_index in settled:
                    clauses = eg.split_clauses(eg.sanitize_input(text)[0])
                    value = eg.rule_value(item, clauses[clause_index].casefold(), self._today(), guide.state["scenario"])
                    if value is not None:
                        guide.word_values[item] = value
                        if item in PERIOD_ITEMS:  # (attack r22) a later form date is checked against this one
                            guide.period_dates[item] = date.fromisoformat(value)
                    guide.review_done = False
                    eg.apply_form(snapshot, item, True)
                    guide.prefill.pop(item, None)
                    guide.deferred.discard(item)
            guide.auto_confirmed = [item for item, _clause in settled]
            # Fixed inputs sent with the sentence in the same Save: same validator, same round.
            results = (self._apply_fields(guide, fields, self._today(), skip_present=True,
                                          aup_review_signal=self._aup_review_signal(session)) if fields else [])
            for entry in results:
                if entry["valid"]:
                    eg.apply_form(snapshot, entry["item"], True)
            self._refresh_prefill(guide, snapshot, text)
            self._record(guide, self._reply_for(guide, result))
            guide.form_result = {"item": results[-1]["item"], "valid": results[-1]["valid"]} if results else None
            guide.form_results = results
            guide.analysis = None
            if provider is not None and result["chooser"] == "keyword":
                request, kept = model_request(snapshot, text, skip_clauses=resolved)
                if request is not None:
                    guide.analysis = {"turn": guide.sequence, "status": "analysing", "reason": None}
                    job = (guide, guide.sequence, snapshot, conflicts, side, text, request, kept,
                           self._metered(provider, session.session_id), self._governor_key(session, guide.state["scenario"]),
                           self._client_id(session))
            view = self._view(guide, provider)
        if job is not None:
            future = self._jobs.submit(self._analyse, *job)
            self._pending.add(future)
            future.add_done_callback(self._pending.discard)
        return view

    def _metered(self, provider, session_id):
        """(optimise r24) The chooser, recording each call's model, token counts and latency in the AI audit log.
        Only a chooser that reports counts (take_usage) is wrapped; the seller text is never recorded."""
        log = self.ai_usage
        if log is None or not callable(getattr(provider, "take_usage", None)):
            return provider

        def call(request):
            started = time.monotonic()
            model = getattr(provider, "MODEL_ID", None)
            try:
                raw = provider(request)
                usage = provider.take_usage()
            except BaseException:
                log.record(session_id, stage="guide", model=model, usage=None,
                           latency_ms=(time.monotonic() - started) * 1000, outcome="error")
                raise
            log.record(session_id, stage="guide", model=model, usage=usage,
                       latency_ms=(time.monotonic() - started) * 1000, outcome="ok")
            return raw
        return call

    def _analyse(self, guide, sequence, snapshot, conflicts, side, text, request, kept, provider, key, client_id="local"):
        """Background: the governed model step for one turn. The seller text lives only in this call."""
        deadline = time.monotonic() + self.model_deadline_seconds
        before = copy.deepcopy(snapshot)
        try:
            rows, reason = governed_model_rows(self.governor, key, provider, request, snapshot["scenario"], deadline,
                                               client_id=client_id)
        except Exception:
            rows, reason = None, "provider_error"
        with guide.lock:
            if guide.sequence != sequence or guide.analysis is None or guide.analysis.get("turn") != sequence:
                return  # a later turn or form entry came first; its own answer stands
            if rows is not None:
                remapped = json.dumps({"v": GUIDE_CONTRACT, "u": [dict(row, k=kept[row["k"]]) for row in rows]}, separators=(",", ":"))
                result = eg.guide_turn(snapshot, text, chooser=lambda _request: remapped, budget_ok=True, contract=GUIDE_CONTRACT)
                # (wo gemini run 2026-11-04) A valid model reply that maps no item would swap a specific keyword
                # answer ("fill in baseline, spike period, reason") for the vaguer UNCLEAR; 2 of 12 live runs did.
                # The keyword answer stays, labelled, unless it was UNCLEAR itself.
                no_items = result["chooser"] == "model" and result["template"] == "UNCLEAR" and guide.reply.get("template") != "UNCLEAR"
                if result["chooser"] == "model" and not no_items:
                    guide.state, guide.conflicts = snapshot, conflicts
                    guide.prefill, guide.deferred = dict(side["prefill"]), set(side["deferred"])
                    self._refresh_prefill(guide, before, text)
                    self._record(guide, self._reply_for(guide, result))
                    guide.analysis = {"turn": sequence, "status": "replaced", "reason": None}
                    return
                reason = "no_items" if no_items else "invalid_reply"
            guide.reply = dict(guide.reply, chooser="keyword_fallback", fallback_reason=reason)
            guide.analysis = {"turn": sequence, "status": "kept", "reason": reason}

    def wait_for_analysis(self, timeout=30.0):
        """Block until every pending model step has settled (tests and the one-turn tool use this)."""
        concurrent.futures.wait(list(self._pending), timeout=timeout)

    @staticmethod
    def _conflict_pair(text):
        names = {name: code for code, name in eg.WEEKDAY_NAMES.items()}
        found = [names[word] for word in re.findall(r"[A-Z][a-z]+day", text) if word in names]
        return tuple(found[:2]) if len(found) >= 2 else None

    def _check_fields(self, guide, fields):
        scenario = guide.state["scenario"]
        for item, _value in fields:
            slot = guide.state["slots"].get(item)
            if slot is None or slot["status"] == "NOT_APPLICABLE" or item not in FORM_FIELDS[scenario]:
                raise BoundaryError(422, "guide_item_invalid")

    @staticmethod
    def _aup_review_signal(session):
        """(attack r22) True when the latest /aup/review result in this demo session was REVIEW_SIGNAL."""
        return getattr(session, "latest_aup_match_status", None) == "REVIEW_SIGNAL"

    @staticmethod
    def _period_date(item, value, scenario, today):
        if scenario != "velocity" or item not in PERIOD_ITEMS or not validate_form_value(scenario, item, value, today):
            return None
        return date.fromisoformat(value)

    def _apply_fields(self, guide, fields, today, skip_present=False, aup_review_signal=False):
        """Each field on its own through validate_form_value; only a valid field becomes STRUCTURALLY_PRESENT.

        (attack r22) Two cross-checks: category_signal "no_signal" is refused while the session's latest policy check
        said REVIEW_SIGNAL, and a baseline week that starts after the spike day is refused (both dates in one Save are
        refused together, since either may be the wrong one)."""
        scenario = guide.state["scenario"]
        results = []
        entered = {item: self._period_date(item, value, scenario, today) for item, value in fields if item in PERIOD_ITEMS}
        known = dict(guide.period_dates)
        known.update({item: day for item, day in entered.items() if day is not None})
        periods_clash = (scenario == "velocity" and all(known.get(item) for item in PERIOD_ITEMS)
                         and known["baseline_period"] > known["surge_period"])
        for item, value in fields:
            if skip_present and guide.state["slots"][item]["status"] == "STRUCTURALLY_PRESENT":
                continue  # already settled from the sentence in the same Save
            if value in eg.DEFERRING_VALUES:
                guide.deferred.add(item)
                guide.prefill.pop(item, None)  # "Change" to Not sure drops the echo for that item
                results.append({"item": item, "valid": False, "deferred": True})
                continue
            valid = validate_form_value(scenario, item, value, today)
            if valid and item == "category_signal" and value == "no_signal" and aup_review_signal:
                valid = False
            if valid and item in PERIOD_ITEMS and scenario == "velocity":
                if periods_clash:
                    valid = False
                    guide.period_dates.pop(item, None)
                else:
                    guide.period_dates[item] = entered[item]
            elif item in PERIOD_ITEMS:
                guide.period_dates.pop(item, None)
            eg.apply_form(guide.state, item, valid)
            deferred = False
            if valid:
                guide.conflicts.pop(item, None)
                guide.deferred.discard(item)
                guide.prefill.pop(item, None)
                guide.attempts.pop(item, None)
                guide.word_values.pop(item, None)  # the seller's own entry replaces a value taken from words
            else:
                guide.attempts[item] = guide.attempts.get(item, 0) + 1
                if guide.attempts[item] >= MAX_FIELD_ATTEMPTS:
                    # Three invalid tries: stop asking for this format; the seller can describe it in their own words.
                    guide.deferred.add(item)
                    guide.attempts.pop(item, None)
                    deferred = True
            results.append({"item": item, "valid": valid, "deferred": deferred})
        return results

    def review(self, session, confirm, change, scenario=None):
        """The one summary confirmation. confirm: values waiting from the seller's words go through the validator and
        the guide may finish. change: those items are reopened and asked again. Never calls a model."""
        guide = self._require(session, scenario)
        with guide.lock:
            if any(slot not in guide.state["slots"] for slot in change):
                raise BoundaryError(422, "guide_item_invalid")
            current = self._compute_round(guide)
            if not self._review_rows(guide) or not (current["stage"] == "review" or self._is_last_round(guide, current)):
                raise BoundaryError(409, "guide_review_not_open")
            reviewable = {row["item"] for row in self._review_rows(guide)}
            if not set(change) <= reviewable:
                raise BoundaryError(422, "guide_item_invalid")
            guide.sequence += 1
            guide.rounds += 1
            guide.auto_confirmed = []
            today = self._today()
            if confirm:
                guide.review_done = True
            for slot in change:
                guide.state["slots"][slot]["status"] = "MISSING"
                guide.state["slots"][slot]["hint"] = None
                guide.prefill.pop(slot, None)
                guide.word_values.pop(slot, None)
                guide.review_done = False
            template, text = self._round_message(guide)
            guide.reply = {"template": template, "text": text, "chooser": "form", "state_changed": True, "dropped": [], "fallback_reason": None}
            guide.form_results = []
            guide.form_result = None
            return self._view(guide)

    def form(self, session, fields, confirm_review=False, scenario=None):
        """One round of fixed inputs (1 to 3 fields). Each field is checked by validate_form_value on its own;
        only a valid field becomes STRUCTURALLY_PRESENT. Not sure / skip settles nothing and sends the item to
        stage B. Nothing here calls a model. The whole request is refused if any item is unknown."""
        guide = self._require(session, scenario)
        with guide.lock:
            self._check_fields(guide, fields)
            if confirm_review:
                current = self._compute_round(guide)
                if not self._review_rows(guide) or not self._is_last_round(guide, current):
                    raise BoundaryError(409, "guide_review_not_open")
            if guide.form_rounds >= self.max_form_rounds:
                raise BoundaryError(429, "guide_form_limit")
            guide.form_rounds += 1
            today = self._today()
            guide.sequence += 1
            guide.rounds += 1
            guide.auto_confirmed = []
            if confirm_review:
                guide.review_done = True
            if guide.analysis is not None and guide.analysis["status"] == "analysing":
                guide.analysis = {"turn": guide.analysis["turn"], "status": "kept", "reason": "superseded"}
            results = self._apply_fields(guide, fields, today, aup_review_signal=self._aup_review_signal(session))
            self._refresh_prefill(guide)
            template, text = self._round_message(guide)
            guide.reply = {"template": template, "text": text, "chooser": "form", "state_changed": True, "dropped": [], "fallback_reason": None}
            guide.form_results = results
            guide.form_result = {"item": results[-1]["item"], "valid": results[-1]["valid"]}
            return self._view(guide)


def register_guide_routes(application, read_session, write_session):
    """Attach the five guide routes to an existing app; guards are the app's own dependencies."""
    if not hasattr(application.state, "guide") or application.state.guide is None:
        application.state.guide = GuideService(application.state.store)

    @application.post("/api/v1/guide/start", response_model=GuideStateResponse)
    def guide_start(body: GuideStartRequest, session=Depends(write_session)):
        return application.state.guide.start(session, body.scenario, body.goods_type)

    @application.post("/api/v1/guide/turn", response_model=GuideStateResponse)
    def guide_turn(body: GuideTurnRequest, session=Depends(write_session)):
        fields = [(field.item, field.value) for field in body.fields] if body.fields else None
        if fields and len({item for item, _value in fields}) != len(fields):
            raise BoundaryError(422, "guide_fields_duplicate")
        return application.state.guide.turn(session, body.text, fields, body.scenario)

    @application.post("/api/v1/guide/review", response_model=GuideStateResponse)
    def guide_review(body: GuideReviewRequest, session=Depends(write_session)):
        if body.confirm == bool(body.change) or len(set(body.change)) != len(body.change):
            raise BoundaryError(422, "guide_review_invalid")  # exactly one of: confirm, or a list of items to change
        return application.state.guide.review(session, body.confirm, body.change, body.scenario)

    @application.post("/api/v1/guide/form", response_model=GuideStateResponse)
    def guide_form(body: GuideFormRequest, session=Depends(write_session)):
        return application.state.guide.form(session, body.pairs(), body.confirm_review, body.scenario)

    @application.get("/api/v1/guide/state", response_model=GuideStateResponse)
    def guide_state(scenario: Optional[Scenario] = None, session=Depends(read_session)):
        return application.state.guide.state(session, scenario)
