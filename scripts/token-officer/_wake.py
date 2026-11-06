"""Shared helpers for Token Officer gate scripts: secrets, wake, heartbeat log.

Secrets (never printed or logged; only their NAMES ever appear in output):
  - looked up first in the process environment (agent shells get Grok Bot saved
    secrets injected as env vars), then in the box secret store
    /home/box/agent-data/box-secrets.json -> "card" -> NAME, which is where Grok Bot
    saved secrets live. A detached scheduler started earlier will not see env vars added
    later, so the file is re-read on every run.

Wake (only with --wake): POST JSON to WAKE_URL_<GATE> with the routine's sender key in
both `Authorization: Bearer <key>` and `X-Automation-Key: <key>` (Grok Bot webhook
routine convention, per workflows/make-bot-ui/SKILL.md). 8 s timeout, one try, no retry.
On failure the payload (no secrets) goes to pending-wakes.jsonl.
"""
import json, os, sys, datetime, urllib.request, urllib.error

SECRET_STORE = "/home/box/agent-data/box-secrets.json"
CT = None
try:
    from zoneinfo import ZoneInfo
    CT = ZoneInfo("America/Chicago")
except Exception:
    pass

def now_ct():
    return datetime.datetime.now(CT).strftime("%Y-%m-%d %H:%M %Z") if CT else datetime.datetime.now().isoformat()

def get_secret(name):
    v = os.environ.get(name)
    if v:
        return v
    try:
        with open(SECRET_STORE) as f:
            v = (json.load(f).get("card") or {}).get(name)
        return v or None
    except Exception:
        return None

def missing(names):
    return [n for n in names if not get_secret(n)]

def log_run(script_dir, record):
    record = {"at": datetime.datetime.now(datetime.timezone.utc).isoformat(), **record}
    with open(os.path.join(script_dir, "run-log.jsonl"), "a") as f:
        f.write(json.dumps(record) + "\n")

def preflight(args, script_dir, gate, token_names):
    """In --wake mode, refuse to do anything unless every secret is present.
    In dry-run live mode, the tokens are still required (to read the sources)."""
    need = list(token_names)
    if args.wake:
        need += [f"WAKE_URL_{gate}", f"WAKE_KEY_{gate}"]
    if args.fixture:
        need = [n for n in need if n.startswith("WAKE_")]  # fixture mode reads no APIs
    miss = missing(need)
    if miss:
        print(f"{now_ct()}  missing secrets, no wake (missing: {', '.join(miss)})")
        log_run(script_dir, {"result": "missing secrets, no wake", "missing": miss,
                             "mode": "wake" if args.wake else "dry-run"})
        sys.exit(0)

def wake(args, script_dir, gate, bot, payload):
    body = json.dumps({"bot": bot, **payload})
    if not args.wake:
        print(f"[DRY RUN] would POST to WAKE_URL_{gate} (sender key from WAKE_KEY_{gate}) with:\n"
              + json.dumps(json.loads(body), indent=1))
        return "dry-run"
    url, key = get_secret(f"WAKE_URL_{gate}"), get_secret(f"WAKE_KEY_{gate}")
    req = urllib.request.Request(url, data=body.encode(), method="POST", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {key}", "X-Automation-Key": key,
        "User-Agent": "token-officer-gate/1"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            print(f"woke {bot}: HTTP {r.status}")
            return f"woke HTTP {r.status}"
    except urllib.error.HTTPError as e:
        err = f"HTTP {e.code}"
    except Exception as e:
        err = type(e).__name__  # no message: it could echo the URL
    print(f"wake FAILED for {bot}: {err} (payload saved to pending-wakes.jsonl)")
    with open(os.path.join(script_dir, "pending-wakes.jsonl"), "a") as f:
        f.write(json.dumps({"at": now_ct(), "error": err, "payload": json.loads(body)}) + "\n")
    return f"wake failed {err}"

def http_json(url, headers, data=None, timeout=30):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def fetch_failed(script_dir, source, e):
    code = getattr(e, "code", None)
    msg = f"HTTP {code}" if code else type(e).__name__
    print(f"{now_ct()}  read error from {source}: {msg}; no wake")
    log_run(script_dir, {"result": "read error, no wake", "source": source, "error": msg})
    sys.exit(2)
