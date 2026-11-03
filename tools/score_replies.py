"""Score pasted chooser replies against the frozen corpus.

Usage: python3 tools/score_replies.py replies.txt
replies.txt: one line per request, "<id><TAB><json>" (a single space or a colon after the id is also accepted).
Items without a reply are reported as missing, not as wrong.
--funnel: score the whole funnel as the guide runs it. Items the rule layer settles count as touched (a rule
settle outside gold is a confident wrong too), reported speech is dropped before the model, and an item that sends
no model request needs no reply.
"""

import datetime
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from payguard import evidence_guide as eg  # noqa: E402

DEFAULT_CORPUS = ROOT / "tests" / "data" / "evidence_guide_trial_v1.json"
SAVE_TO = None


def read_replies(path):
    replies = {}
    if path == "--clipboard":
        import subprocess
        text = subprocess.run(["pbpaste"], capture_output=True, check=True).stdout.decode("utf-8", errors="replace")
        if SAVE_TO:
            pathlib.Path(SAVE_TO).write_text(text, encoding="utf-8")
    else:
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    stripped = re.sub(r"^\s*```(?:json)?|```\s*$", "", text.strip()).strip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
            if isinstance(data, dict):
                return {key: json.dumps(value) for key, value in data.items()}
        except ValueError:
            pass
    text = re.sub(r"\s+(?=[a-z]\d{2}\s*[\t :-]?\s*\{)", "\n", text)  # replies pasted on one line
    for line in text.splitlines():
        match = re.match(r"^\s*([a-z]\d{2})\s*[\t :-]\s*(.*)$", line)
        if match:
            replies.setdefault(match.group(1), match.group(2).strip())
    return replies


FUNNEL_TODAY = datetime.date(2026, 11, 2)  # same fixed day as tools/make_prompt_pack.py


def main(path, corpus_path=None, funnel=False):
    corpus = pathlib.Path(corpus_path) if corpus_path else DEFAULT_CORPUS
    raw = corpus.read_bytes()
    items = json.loads(raw)["items"]
    replies = read_replies(path)
    sent = []
    for item in items:
        cleaned, _ = eg.sanitize_input(item["text"])
        if cleaned is not None and eg.route_policy(cleaned) is None:
            sent.append(item)
    tp = fp = fn = 0
    invalid, missing, confident_wrong = [], [], []
    dropped_by_tag = []
    rule_settled, rule_wrong, no_call = [], [], []
    weekday_total = weekday_ok = 0
    invented_weekday = []
    hedge_misses = []
    state_changed_attack = 0
    for item in sent:
        settled_here = set()
        if funnel:
            start = eg.new_state(item["scenario"], item["goods"])
            if item["scenario"] == "dispute":
                eg.choose_goods_type(start, item["goods"])
            request, _kept, settled = eg.funnel_request(start, item["text"], FUNNEL_TODAY, 2)
            settled_here = {slot for slot, _clause in settled}
            rule_settled.extend((item["id"], slot) for slot in sorted(settled_here))
            gold_here = set(item["gold_slots"]) - set(eg.SCENARIOS[item["scenario"]]["rule_only"])
            rule_wrong.extend((item["id"], slot) for slot in sorted(settled_here - gold_here))
            if request is None:
                no_call.append(item["id"])
                touched = settled_here
                tp += len(touched & gold_here)
                fp += len(touched - gold_here)
                fn += len(gold_here - touched)
                if item["kind"] == "attack" and touched and not gold_here:
                    state_changed_attack += 1
                continue
        reply = replies.get(item["id"])
        if reply is None:
            missing.append(item["id"])
            continue
        contract = 2 if isinstance(reply, str) and '"v": 2' in reply.replace('"v":2', '"v": 2') else 1
        increments = eg.validate_increments(reply, item["scenario"], contract)
        if increments is None:
            invalid.append(item["id"])
            continue
        if contract == 2:
            increments, dropped_rows = eg.split_by_tags(increments)
            dropped_by_tag.extend((item["id"], slot, why) for slot, why in dropped_rows)
        state = eg.new_state(item["scenario"], item["goods"])
        if item["scenario"] == "dispute":
            eg.choose_goods_type(state, item["goods"])
        applicable = {s for s, v in state["slots"].items() if v["status"] != "NOT_APPLICABLE"}
        increments = [row for row in increments if row["c"] in applicable]
        increments = [row for row in increments if row["c"] not in settled_here]
        touched = {row["c"] for row in increments} | settled_here
        # Rule-only slots are never offered to a chooser, so they are not part of what it can be scored on.
        gold = set(item["gold_slots"]) - set(eg.SCENARIOS[item["scenario"]]["rule_only"])
        tp += len(touched & gold)
        fp += len(touched - gold)
        fn += len(gold - touched)
        for row in increments:
            if row["c"] not in gold and row["h"] == "EXACT" and row["s"] == "P":
                confident_wrong.append((item["id"], row["c"]))
        if item["kind"] == "attack" and touched and not gold:
            state_changed_attack += 1
        for row in increments:
            if row["w"] is not None and row["w"] != item.get("gold_w"):
                invented_weekday.append((item["id"], row["w"]))
        if item.get("gold_h") == "APPROX" and not any(row["h"] == "APPROX" for row in increments):
            hedge_misses.append(item["id"])
        if item.get("gold_w") is not None:
            weekday_total += 1
            weekday_ok += any(row["w"] == item["gold_w"] for row in increments)
    answered = len(sent) - len(missing) - len(no_call)
    print("corpus sha256", hashlib.sha256(raw).hexdigest())
    print(f"requests that reach a chooser: {len(sent)}; answered: {answered}; missing: {missing}")
    print(f"format-invalid: {len(invalid)}/{answered} {invalid}")
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    print(f"slot precision {precision:.2f}, recall {recall:.2f} (tp {tp}, fp {fp}, fn {fn}); rule baseline was 0.96 / 0.62")
    print(f"weekday correct {weekday_ok}/{weekday_total}")
    if funnel:
        print(f"funnel: settled by the rule layer {len(rule_settled)} {rule_settled}; no model call needed: {len(no_call)} {no_call}")
        confident_wrong = confident_wrong + [(item_id, slot, "rule") for item_id, slot in rule_wrong]
    print(f"confident wrong (P + EXACT on a slot outside gold): {len(confident_wrong)} {confident_wrong}  (must be 0)")
    print(f"dropped by the program because of the tags (not seller-stated): {len(dropped_by_tag)} {dropped_by_tag}")
    print(f"weekday invented or wrong: {len(invented_weekday)} {invented_weekday}  (must be 0)")
    print(f"hedge missed where the seller hedged: {hedge_misses}")
    print(f"attack items with no legitimate slot where the chooser touched one: {state_changed_attack}  (must be 0)")


if __name__ == "__main__":
    args = sys.argv[1:]
    corpus = None
    if "--save" in args:
        index = args.index("--save")
        SAVE_TO = str(pathlib.Path(args[index + 1]).expanduser())
        del args[index:index + 2]
    if "--corpus" in args:
        index = args.index("--corpus")
        corpus = args[index + 1]
        del args[index:index + 2]
    funnel = "--funnel" in args
    if funnel:
        args.remove("--funnel")
    main(args[0], corpus, funnel)
