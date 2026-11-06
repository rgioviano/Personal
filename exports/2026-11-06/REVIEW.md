# Export checkpoint placement (2026-11-06)

Archive file SHA256 (gzip): `11038997b4abd2a3a5bf54aacff8c46f7dffd51f1424334ab97abcd2d6c8ae72`.

`sha256sum -c` on `SHA256SUMS.txt` in the extracted archive exited 0 before any copy. Every listed file matched.

## Where files landed

Completeness and hash docs from the archive root are in this folder so they do not replace repo-root files. Their text is unchanged.

- `COMPLETENESS.md`, `INCLUDED.txt`, and `SHA256SUMS.txt` keep the checkpoint wording.
- Paths in `SHA256SUMS.txt` start with `Personal/`. That prefix is the archive folder and means the repo root.
- Paths in `INCLUDED.txt` and `COMPLETENESS.md` are repo-root paths for the export JSON and `scripts/brain_lint.py`.
- Export JSON is under `bots/<slug>/export/`.
- `scripts/brain_lint.py` is the included lint script. It is the same bytes as `scripts/chief/brain_lint.py`. The chief copy was not edited.

## Review before commit

Three export JSON files were edited after the hash check so obvious client or athlete names and personal health details are not in the commit. Archive hashes for those three files no longer match the committed bytes. Every other hashed file still matches `SHA256SUMS.txt`.

Redacted files and committed SHA256:

- `bots/chief/export/grok-bot-export-chief-part1.json` `d0710b8253e59e605135aff1a3862fdcbad8d062d6a48005aed7f679da48f8e1`
- `bots/scout/export/grok-bot-export-scout.json` `f6ed09b32f774c77b7d36105b5212b87fc636db5c1813eeeafd01882c3034b9c`
- `bots/doc/export/grok-bot-export-doc.json` `7dfc64b53abdc366d1565fe5dacd351ccd010b285d334d1c50b025d6faf9ebd0`

What was removed, without the original values:

- Client, athlete, student, and similar personal names in Chief memories, user facts, and one routine.
- Personal health statements, a treatment preference, and lab details in Scout memories and user facts.
- A personal health goal clause and stored lab values in one Doc memory and one Doc routine.
- A pet diagnosis word in Chief and Scout.

One allowed business address in a Scout skill was separated from a JSON `\n` so the lint scan reads that address instead of a glued prefix. The address itself was not removed.

`COMPLETENESS.md` is the checkpoint's own disclosure and was not rewritten.

Sources: attached Personal export archive 2026-11-06 (SHA256 above); `SHA256SUMS.txt` in this folder; review of memories, user facts, and routines before commit.
