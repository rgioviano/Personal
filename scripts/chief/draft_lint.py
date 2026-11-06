#!/usr/bin/env python3
"""draft_lint.py: check a draft message against Ryne's draft rules. Exceptions only.

Checks: em dashes, $ prices (drafts to leads), "Aurora", and the banned phrases
"thanks for checking in", "thank you for checking in", "reach out anytime".

Usage:
  python3 draft_lint.py draft.txt
  echo "text" | python3 draft_lint.py
  options: --not-lead (skip the price rule, for drafts that are not to a lead)
           --price-ok (skip the price rule, price was read live today)
           --json
Exit code: 0 clean ("0 exceptions"), 1 exceptions found, 2 script error.
"""
import argparse, json, re, sys

RULES = [
    ("em-dash", re.compile("\u2014"), "em dash; use a comma, period or parentheses"),
    ("price", re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?(?:\s?(?:k|/mo|/month|a month|per month|/session))?", re.I),
     "price in a draft to a lead; omit unless read live today"),
    ("aurora", re.compile(r"\bAurora\b", re.I), "mentions Aurora"),
    ("thanks-for-checking-in", re.compile(r"\bthanks?(?:\s+(?:you|so much|a lot))*\s+for\s+checking\s+in\b", re.I),
     "thanks the reader for checking in (do not invite more check-ins)"),
    ("thank-you-for-checking-in", re.compile(r"\bthank\s+you(?:\s+so\s+much)?\s+for\s+checking\s+in\b", re.I),
     "thanks the reader for checking in (do not invite more check-ins)"),
    ("reach-out-anytime", re.compile(r"\breach\s+out\s+any\s?time\b", re.I), "invites more messages"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--not-lead", action="store_true")
    ap.add_argument("--price-ok", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8", errors="replace").read() if a.file and a.file != "-" else sys.stdin.read()
    skip = {"price"} if (a.not_lead or a.price_ok) else set()
    hits, spans = [], set()
    for ln, line in enumerate(text.splitlines(), 1):
        for rid, rx, why in RULES:
            if rid in skip:
                continue
            for m in rx.finditer(line):
                key = (ln, m.start(), "thank")
                if rid.startswith("thank"):
                    if key in spans:
                        continue
                    spans.add(key)
                shown = "(em dash)" if rid == "em-dash" else m.group(0)
                hits.append({"line": ln, "col": m.start() + 1, "rule": rid, "match": shown, "why": why})
    if a.json:
        print(json.dumps({"exception_count": len(hits), "exceptions": hits}, indent=2))
    elif not hits:
        print("0 exceptions")
    else:
        for h in hits:
            print(f"line {h['line']}:{h['col']}  {h['rule']}  \"{h['match']}\"  ({h['why']})")
        print(f"{len(hits)} exceptions")
    return 1 if hits else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"draft_lint error: {e}", file=sys.stderr)
        sys.exit(2)
