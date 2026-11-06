#!/usr/bin/env python3
"""Linus 'IronBlueprint bug triage' weekday 9am check -> gate.
Checks IB Slack #bugs (C0C8V38T082) top-level posts and open cards on the Basecamp Bugs board
(10037160132) against Linus's bug-triage-state.json + triage-locks/. Wakes Linus (webhook routine
folder ironblueprint-bug-triage) only for untracked items. Read-only.
Secrets: SLACK_BOT_TOKEN, BASECAMP_TOKEN; with --wake also WAKE_URL_LINUS_BUGS + WAKE_KEY_LINUS_BUGS."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _wake import wake, log_run, now_ct, preflight, get_secret, http_json, fetch_failed

HERE = os.path.dirname(os.path.abspath(__file__))
GATE, PREP, CHANNEL = "LINUS_BUGS", "/workspace/ironblueprint-agent-prep", "C0C8V38T082"
BC_ACCOUNT, BC_BUCKET, BC_TABLE = 6223040, 47608498, 10037160132
OPEN_COLS = {"Triage", "Ready", "In Progress", "QA"}

def as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])

def tracked(state_path, locks_dir):
    s = json.load(open(state_path)); ts, cards = set(), set()
    for t in s.get("triaged", []):
        ts.update(as_list(t.get("slack_ts"))); cards.update(str(c) for c in as_list(t.get("basecamp_card_id")))
    for t in s.get("skipped_non_bugs", []):
        ts.update(as_list(t.get("slack_ts")))
    for t in s.get("skipped_basecamp", []):
        cards.update(str(c) for c in as_list(t.get("basecamp_card_id")))
    if os.path.isdir(locks_dir):
        cards.update(os.listdir(locks_dir))
    return ts, cards

def live_slack(oldest):
    try:
        d = http_json(f"https://slack.com/api/conversations.history?channel={CHANNEL}&oldest={oldest}&limit=200",
                      {"Authorization": f"Bearer {get_secret('SLACK_BOT_TOKEN')}"})
    except Exception as e:
        fetch_failed(HERE, "Slack #bugs", e)
    if not d.get("ok"):
        fetch_failed(HERE, f"Slack #bugs ({d.get('error')})", Exception())
    return [{"ts": m["ts"], "text": m.get("text", "")[:200],
             "is_thread_reply": bool(m.get("thread_ts") and m.get("thread_ts") != m["ts"])}
            for m in d.get("messages", []) if m.get("subtype") not in ("channel_join", "message_deleted")]

def live_basecamp():
    h = {"Authorization": f"Bearer {get_secret('BASECAMP_TOKEN')}", "User-Agent": "token-officer-gate (ryne@ironblueprint.app)"}
    try:
        table = http_json(f"https://3.basecampapi.com/{BC_ACCOUNT}/buckets/{BC_BUCKET}/card_tables/{BC_TABLE}.json", h)
        out = []
        for col in table.get("lists", []):
            if col["title"] in OPEN_COLS:
                out += [{"id": c["id"], "column": col["title"], "title": c["title"]} for c in http_json(col["cards_url"], h)]
        return out
    except Exception as e:
        fetch_failed(HERE, "Basecamp Bugs board", e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture"); ap.add_argument("--state", default=f"{PREP}/bug-triage-state.json")
    ap.add_argument("--locks", default=f"{PREP}/triage-locks"); ap.add_argument("--wake", action="store_true")
    a = ap.parse_args()
    preflight(a, HERE, GATE, ["SLACK_BOT_TOKEN", "BASECAMP_TOKEN"])
    ts_seen, cards_seen = tracked(a.state, a.locks)
    oldest = min(ts_seen, key=float) if ts_seen else "0"
    if a.fixture:
        msgs = json.load(open(os.path.join(a.fixture, "slack-bugs.json")))["messages"]
        cards = json.load(open(os.path.join(a.fixture, "basecamp-bugs.json")))["cards"]
    else:
        msgs, cards = live_slack(oldest), live_basecamp()
    new_msgs = [m for m in msgs if not m.get("is_thread_reply") and float(m["ts"]) >= float(oldest) and m["ts"] not in ts_seen]
    open_cards = [c for c in cards if c["column"] in OPEN_COLS]
    new_cards = [c for c in open_cards if str(c["id"]) not in cards_seen]
    print(f"{now_ct()}  #bugs top-level: {len([m for m in msgs if not m.get('is_thread_reply')])} untracked: {len(new_msgs)} | "
          f"open cards: {len(open_cards)} untracked: {len(new_cards)}")
    if new_msgs or new_cards:
        print("DECISION: WAKE Linus")
        res = wake(a, HERE, GATE, "Linus", {"routine": "IronBlueprint bug triage", "new": len(new_msgs) + len(new_cards),
                   "slack_ts": [m["ts"] for m in new_msgs],
                   "basecamp_cards": [{"id": c["id"], "column": c["column"], "title": c["title"]} for c in new_cards]})
    else:
        print("DECISION: SKIP (nothing new in #bugs or on the Bugs board) - no wake"); res = "skipped"
    log_run(HERE, {"mode": ("fixture" if a.fixture else "live") + ("+wake" if a.wake else ""),
                   "new_slack": len(new_msgs), "new_cards": len(new_cards), "result": res})

if __name__ == "__main__":
    main()
