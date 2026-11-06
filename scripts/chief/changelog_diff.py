#!/usr/bin/env python3
"""changelog_diff.py: list Grok Bot changelog entries newer than the last-seen file. New entries only.

Fetches https://x.ai/changelog/bot (or reads --html FILE), parses each release (date, version, title,
"also includes"), compares with Chief's last-seen file, and prints only the newer entries as JSON.
Read-only unless --commit, which rewrites the last-seen file to the newest entry.

Usage:
  python3 changelog_diff.py                     # fetch live, compare, print JSON (read-only)
  python3 changelog_diff.py --html page.html    # parse a saved page instead of fetching
  python3 changelog_diff.py --commit            # same, then record the newest entry as last seen
  options: --no-items (leave out the New/Improved/Fixed bullet lists)  --last-seen PATH  --url URL  --today YYYY-MM-DD (date written by --commit)
Exit code: 0 nothing new, 1 new entries, 2 script error (fetch failed, 0 entries parsed,
unreadable last-seen file). An empty parse is an error, never "nothing new".
"""
import argparse, datetime as dt, html, json, re, subprocess, sys, urllib.request

URL = "https://x.ai/changelog/bot"
LAST_SEEN = "/home/box/agent-data/agents/ad6690d7-be33-4540-ac42-68eb3059c181/memory/changelog-last-seen.md"
UA = "Mozilla/5.0 (X11; Linux x86_64) chief-changelog-diff/1.0"

ARTICLE = re.compile(r"<article\b.*?</article>", re.S | re.I)
TIME = re.compile(r'<time[^>]*dateTime="(\d{4}-\d{2}-\d{2})"', re.I)
H2 = re.compile(r'<h2([^>]*)>(.*?)</h2>', re.S | re.I)
H2ID = re.compile(r'\bid="v?(\d+\.\d+\.\d+)"', re.I)
ALSO = re.compile(r"<p[^>]*>\s*Also includes\s*(.*?)</p>", re.S | re.I)
SECTION = re.compile(r"<section\b[^>]*>\s*<h3[^>]*>(.*?)</h3>(.*?)</section>", re.S | re.I)
LI = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S | re.I)
VER = re.compile(r"\bv?(\d+\.\d+\.\d+)\b")


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def vtuple(v):
    return tuple(int(x) for x in v.split(".")) if v else ()


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:  # some sites block urllib; curl is the documented fallback
        p = subprocess.run(["curl", "-sSL", "-m", "30", "-A", UA, url], capture_output=True, text=True)
        if p.returncode != 0 or not p.stdout:
            raise RuntimeError(f"fetch failed ({e}; curl exit {p.returncode})")
        return p.stdout


def parse(page):
    out = []
    for art in ARTICLE.findall(page):
        t, h = TIME.search(art), H2.search(art)
        if not t or not h:
            continue
        idm = H2ID.search(h.group(1))
        ver = idm.group(1) if idm else ""
        if not ver:
            m = VER.search(text(art[:art.find("<h2")]))
            ver = m.group(1) if m else ""
        also = ALSO.search(art)
        sections = {text(n): [text(li) for li in LI.findall(body)] for n, body in SECTION.findall(art)}
        out.append({"date": t.group(1), "version": ver, "title": text(h.group(2)),
                    "also_includes": text(also.group(1)) if also else "", "sections": sections})
    return out


def read_last_seen(path):
    raw = open(path, encoding="utf-8").read()
    f = dict(re.findall(r"^\s*-\s*(\w+):\s*(.*?)\s*$", raw, re.M))
    if "date" not in f or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["date"]):
        raise ValueError(f"last-seen file has no '- date: YYYY-MM-DD' line: {path}")
    m = VER.search(f.get("version", "") or f.get("title", ""))
    return {"date": f["date"], "version": m.group(1) if m else "", "title": f.get("title", ""),
            "previous": f.get("previous", "")}


def newer(e, seen):
    if e["date"] != seen["date"]:
        return e["date"] > seen["date"]
    if e["version"] and seen["version"]:
        return vtuple(e["version"]) > vtuple(seen["version"])
    return False


def commit(path, top, seen, today):
    body = (
        "# Grok Bot changelog last-seen\n\n"
        f"- date: {top['date']}\n"
        f"- version: v{top['version']}\n"
        f"- title: Latest v{top['version']} ({top['date']}): {top['title']}"
        + (f" (also includes {top['also_includes']})" if top["also_includes"] else "") + "\n"
        f"- recorded: {today} (changelog_diff.py --commit)\n"
        f"- previous: {seen['date']} v{seen['version']}\n"
        f"- source: {URL}\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--last-seen", default=LAST_SEEN)
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--no-items", action="store_true")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args(argv)
    page = open(a.html, encoding="utf-8", errors="replace").read() if a.html else fetch(a.url)
    entries = parse(page)
    if not entries:
        raise RuntimeError("0 changelog entries parsed (page layout changed or fetch blocked); not treating as 'nothing new'")
    seen = read_last_seen(a.last_seen)
    new = sorted([e for e in entries if newer(e, seen)], key=lambda e: (e["date"], vtuple(e["version"])), reverse=True)
    if a.no_items:
        new = [{k: v for k, v in e.items() if k != "sections"} for e in new]
    res = {"source": a.html or a.url, "entries_parsed": len(entries), "last_seen": seen,
           "latest": {k: v for k, v in entries[0].items() if k != "sections"}, "new_count": len(new), "new": new, "committed": False}
    if a.commit and new:
        commit(a.last_seen, new[0], seen, a.today)
        res["committed"] = True
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 1 if new else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"changelog_diff error: {e}", file=sys.stderr)
        sys.exit(2)
