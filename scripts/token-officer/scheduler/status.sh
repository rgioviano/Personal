#!/usr/bin/env bash
D="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$D/scheduler.pid" ] && kill -0 "$(cat "$D/scheduler.pid")" 2>/dev/null; then echo "RUNNING pid $(cat "$D/scheduler.pid")"; else echo "NOT RUNNING (run $D/ensure-running.sh)"; fi
cat "$D/heartbeat.json" 2>/dev/null
python3 - <<'PY'
import json
names=["GITHUB_TOKEN","SLACK_BOT_TOKEN","BASECAMP_TOKEN","X_USER_TOKEN","NOTION_TOKEN","WAKE_URL_LINUS_PR","WAKE_KEY_LINUS_PR","WAKE_URL_LINUS_BUGS","WAKE_KEY_LINUS_BUGS","WAKE_URL_BOOKMARKS","WAKE_KEY_BOOKMARKS"]
try: card=(json.load(open("/home/box/agent-data/box-secrets.json")).get("card") or {})
except Exception: card={}
print("secrets present in box store (names only):", {n: bool(card.get(n)) for n in names})
PY
