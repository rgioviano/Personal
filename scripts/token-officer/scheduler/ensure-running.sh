#!/usr/bin/env bash
# Start the Token Officer gate scheduler if it isn't running. Safe to call any number of times.
D="$(cd "$(dirname "$0")" && pwd)"
PIDF="$D/scheduler.pid"
if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null && grep -q scheduler.py "/proc/$(cat "$PIDF")/cmdline" 2>/dev/null; then
  echo "scheduler running (pid $(cat "$PIDF"))"; exit 0
fi
# env -i: start from a clean env so no agent-shell secrets are inherited; gates read secrets
# fresh from the box secret store on each run.
setsid env -i HOME=/home/box PATH=/usr/local/bin:/usr/bin:/bin TZ=America/Chicago \
  nohup /usr/bin/python3 "$D/scheduler.py" >>"$D/logs/scheduler.out" 2>&1 < /dev/null &
echo $! > "$PIDF"; sleep 1
kill -0 "$(cat "$PIDF")" 2>/dev/null && echo "scheduler started (pid $(cat "$PIDF"))" || { echo "FAILED to start; see $D/logs/scheduler.out"; exit 1; }
