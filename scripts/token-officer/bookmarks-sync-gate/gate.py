#!/usr/bin/env python3
"""Bookmarks 'x-bookmarks-sync' Mon/Thu 9:17 check -> gate.
Wakes Bookmarks (webhook routine folder x-bookmarks-gate) only when one of the newest 100 X
bookmarks isn't a 'Tweet ID' row in the X Bookmarks Notion data source. Payload carries
"new": <count> so the routine can skip mental-models-synthesis when it is 0. Read-only.
Secrets: X_USER_TOKEN, NOTION_TOKEN; with --wake also WAKE_URL_BOOKMARKS + WAKE_KEY_BOOKMARKS."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _wake import wake, log_run, now_ct, preflight, get_secret, http_json, fetch_failed

HERE = os.path.dirname(os.path.abspath(__file__))
GATE, STATE = "BOOKMARKS", "/home/box/agent-data/x-bookmarks/state.json"

def live_x(uid):
    try:
        d = http_json(f"https://api.x.com/2/users/{uid}/bookmarks?max_results=100", {"Authorization": f"Bearer {get_secret('X_USER_TOKEN')}"})
    except Exception as e:
        fetch_failed(HERE, "X bookmarks", e)
    return [p["id"] for p in d.get("data", [])]

def live_notion(ds):
    ids, cursor = set(), None
    h = {"Authorization": f"Bearer {get_secret('NOTION_TOKEN')}", "Notion-Version": "2025-09-03", "Content-Type": "application/json"}
    while True:
        body = json.dumps({"page_size": 100, **({"start_cursor": cursor} if cursor else {})}).encode()
        try:
            d = http_json(f"https://api.notion.com/v1/data_sources/{ds}/query", h, data=body)
        except Exception as e:
            fetch_failed(HERE, "Notion X Bookmarks", e)
        for r in d["results"]:
            rt = r["properties"].get("Tweet ID", {}).get("rich_text", [])
            if rt:
                ids.add("".join(t["plain_text"] for t in rt))
        if not d.get("has_more"):
            return ids
        cursor = d["next_cursor"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture"); ap.add_argument("--wake", action="store_true")
    a = ap.parse_args()
    preflight(a, HERE, GATE, ["X_USER_TOKEN", "NOTION_TOKEN"])
    st = json.load(open(STATE))
    if a.fixture:
        x_ids = [p["id"] for p in json.load(open(os.path.join(a.fixture, "x-bookmarks.json")))["data"]]
        n_ids = set(json.load(open(os.path.join(a.fixture, "notion-tweet-ids.json")))["tweet_ids"])
    else:
        x_ids, n_ids = live_x(st["x_user_id"]), live_notion(st["notion_data_source_id"])
    new = [i for i in x_ids if i not in n_ids]
    print(f"{now_ct()}  X bookmarks scanned: {len(x_ids)}  Notion rows: {len(n_ids)}  new: {len(new)}")
    if not x_ids:
        print("DECISION: WAKE (0 bookmarks returned - possible data problem)")
        res = wake(a, HERE, GATE, "Bookmarks", {"routine": "x-bookmarks-gate", "new": 0, "scanned": 0, "reason": "empty X pull, please check"})
    elif new:
        print(f"DECISION: WAKE Bookmarks ({len(new)} new)")
        res = wake(a, HERE, GATE, "Bookmarks", {"routine": "x-bookmarks-gate", "new": len(new), "scanned": len(x_ids), "new_post_ids": new})
    else:
        print("DECISION: SKIP (every bookmark already in Notion) - no wake"); res = "skipped"
    log_run(HERE, {"mode": ("fixture" if a.fixture else "live") + ("+wake" if a.wake else ""), "scanned": len(x_ids), "new": len(new), "result": res})

if __name__ == "__main__":
    main()
