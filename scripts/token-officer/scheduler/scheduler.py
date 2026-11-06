#!/usr/bin/env python3
"""Token Officer gate scheduler: a supervised loop (no cron on this box: no cron package,
PID 1 is tini, no systemd). Times are America/Chicago. Each job fires at most once per
local day; if the box was down at fire time it catches up within CATCHUP minutes.
State: scheduler-state.json (last fire date per job). Heartbeat: heartbeat.json every loop.
Gates run with --wake; they exit with 'missing secrets, no wake' until Ryne adds the secrets."""
import datetime, json, os, subprocess, sys, time
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TZ = ZoneInfo("America/Chicago")
CATCHUP = 120  # minutes
JOBS = [  # name, gate dir, weekdays (Mon=0), HH, MM
    ("linus-pr", "linus-pr-review-gate", {0, 1, 2, 3, 4}, 9, 0),
    ("linus-bugs", "linus-bug-triage-gate", {0, 1, 2, 3, 4}, 9, 0),
    ("bookmarks", "bookmarks-sync-gate", {0, 3}, 9, 17),
]
STATE, BEAT = os.path.join(HERE, "scheduler-state.json"), os.path.join(HERE, "heartbeat.json")

def load():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}

def save(path, obj):
    tmp = path + ".tmp"; json.dump(obj, open(tmp, "w"), indent=1); os.replace(tmp, path)

def run(name, gate):
    log = os.path.join(HERE, "logs", f"{name}.log")
    with open(log, "a") as f:
        f.write(f"\n=== {datetime.datetime.now(TZ):%Y-%m-%d %H:%M %Z} run {gate} --wake\n"); f.flush()
        try:
            r = subprocess.run([sys.executable, os.path.join(ROOT, gate, "gate.py"), "--wake"],
                               stdout=f, stderr=subprocess.STDOUT, timeout=600, cwd=ROOT)
            f.write(f"=== exit {r.returncode}\n")
        except subprocess.TimeoutExpired:
            f.write("=== TIMEOUT after 600s\n")

def main():
    once = "--once-check" in sys.argv
    while True:
        now = datetime.datetime.now(TZ); st = load(); today = now.date().isoformat()
        for name, gate, days, hh, mm in JOBS:
            due = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            if now.weekday() in days and due <= now < due + datetime.timedelta(minutes=CATCHUP) and st.get(name) != today:
                st[name] = today; save(STATE, st)  # mark first: never double-fire
                run(name, gate)
        nxt = {}
        for name, gate, days, hh, mm in JOBS:
            d = now
            for i in range(8):
                c = (now + datetime.timedelta(days=i)).replace(hour=hh, minute=mm, second=0, microsecond=0)
                if c.weekday() in days and (c > now or (i == 0 and st.get(name) != today and c <= now < c + datetime.timedelta(minutes=CATCHUP))):
                    nxt[name] = c.strftime("%a %Y-%m-%d %H:%M %Z"); break
        save(BEAT, {"pid": os.getpid(), "alive_at": now.strftime("%Y-%m-%d %H:%M:%S %Z"), "next": nxt, "last_fired": st})
        if once:
            print(json.dumps(json.load(open(BEAT)), indent=1)); return
        time.sleep(30)

if __name__ == "__main__":
    main()
