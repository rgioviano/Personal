# Export checkpoint review (2026-11-06)

Archive gzip SHA256: `11038997b4abd2a3a5bf54aacff8c46f7dffd51f1424334ab97abcd2d6c8ae72`.

The archive's own `SHA256SUMS.txt` checked out with `sha256sum -c` before copy. That record used a `Personal/` prefix. That prefix meant the repo root.

## Placement

Completeness, inclusion, hash, and this review live in `exports/2026-11-06/` so they do not replace repo-root files. Export JSON is under `bots/<slug>/export/`. `scripts/brain_lint.py` matches `scripts/chief/brain_lint.py` byte for byte.

## Second review

Custom and private skill bodies and personal fields were read again, including file bytes past the 5MB lint cap. Whole entries were dropped when they held a private name, personal health detail, nonpublic email or account id, or a private calendar id. The same name and calendar id were removed from `skills/morning-brief/SKILL.md`. `scripts/chief/promise_scan.py` no longer stores personal names or mailbox addresses that `brain_lint.py` rejects. Lint rules were not changed.

`SHA256SUMS.txt` is the hash of the committed files, not the pre-review archive bytes.

Sources: attached Personal export archive 2026-11-06; second review before commit.
