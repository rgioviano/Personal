#!/usr/bin/env python3
"""Linus 'IronBlueprint PR review' weekday 9am check -> gate.
Wakes Linus (webhook routine folder ironblueprint-pr-review) only when an open, non-draft PR
in the 3 IronBlueprint repos has a (repo#n, head_sha) not in Linus's pr-review-state.json.
Read-only. Secrets: GITHUB_TOKEN; with --wake also WAKE_URL_LINUS_PR + WAKE_KEY_LINUS_PR."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _wake import wake, log_run, now_ct, preflight, get_secret, http_json, fetch_failed

HERE = os.path.dirname(os.path.abspath(__file__))
GATE, OWNER = "LINUS_PR", "IronBluePrint"
REPOS = ["frontend-website", "nodejs-backend", "nexus-ai-agent"]
STATE = "/workspace/ironblueprint-agent-prep/pr-review-state.json"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture"); ap.add_argument("--state", default=STATE); ap.add_argument("--wake", action="store_true")
    a = ap.parse_args()
    preflight(a, HERE, GATE, ["GITHUB_TOKEN"])
    reviewed = json.load(open(a.state)).get("reviewed", {}) if os.path.exists(a.state) else {}
    pending, counts = [], {}
    for repo in REPOS:
        if a.fixture:
            prs = json.load(open(os.path.join(a.fixture, f"pulls-{repo}.json")))
        else:
            try:
                prs = http_json(f"https://api.github.com/repos/{OWNER}/{repo}/pulls?state=open&per_page=100",
                                {"Authorization": f"Bearer {get_secret('GITHUB_TOKEN')}", "Accept": "application/vnd.github+json",
                                 "User-Agent": "token-officer-gate"})
            except Exception as e:
                fetch_failed(HERE, f"GitHub {repo}", e)
        counts[repo] = len(prs)
        for p in prs:
            if p.get("draft"):
                continue
            key, sha = f"{OWNER}/{repo}#{p['number']}", p["head"]["sha"]
            prev = reviewed.get(key, {})
            if prev.get("head_sha") != sha:
                pending.append({"pr": key, "title": p["title"], "head_sha": sha,
                                "why": "new PR" if not prev else "new commits since last review", "url": p.get("html_url")})
    print(f"{now_ct()}  open PRs: {counts}  reviewed keys in state: {len(reviewed)}")
    if pending:
        print(f"DECISION: WAKE Linus ({len(pending)} PR(s) need review)")
        res = wake(a, HERE, GATE, "Linus", {"routine": "IronBlueprint PR review", "new": len(pending), "prs": pending})
    else:
        print("DECISION: SKIP (every open PR's head SHA is already reviewed) - no wake"); res = "skipped"
    log_run(HERE, {"mode": ("fixture" if a.fixture else "live") + ("+wake" if a.wake else ""), "open": counts, "new": len(pending), "result": res})

if __name__ == "__main__":
    main()
