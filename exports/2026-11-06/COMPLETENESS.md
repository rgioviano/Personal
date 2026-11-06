# Personal export checkpoint completeness

privacy_ready: true
semantic_review: full re-scan of memories, user_facts, instructions, routine instructions;
known client/athlete identifiers and personal-health clinical content removed when present;
brain_lint secrets/pii/emdash exit 0; scan.py empty.
skills: non-Chief incomplete/unverified; only full-text skills after Chief fill kept.

The lines above are the archive checkpoint's own disclosure. The byte sizes in that disclosure were the archive sizes.

## Committed copy after the 2026-11-06 review

A second read covered custom and private skill bodies plus personal fields (memories, user facts, routines, bot instructions), including bytes past the 5MB lint read. Where a section held a private name, personal health detail, nonpublic email or account id, or a private calendar id, that whole entry was dropped. `scripts/brain_lint.py` was not changed and was not weakened.

Committed byte sizes:

Wave3 replaced the Maverick export. The Maverick size below is that later committed file. The other wave1 exports were left as they were.

- `bots/chief/export/grok-bot-export-chief-part1.json` bytes=5994973
- `bots/chief/export/grok-bot-export-chief-part2.json` bytes=4441710
- `bots/doc/export/grok-bot-export-doc.json` bytes=110087
- `bots/forge/export/grok-bot-export-forge.json` bytes=88041
- `bots/jetson/export/grok-bot-export-jetson.json` bytes=167744
- `bots/maverick/export/grok-bot-export-maverick.json` bytes=9525699
- `bots/midori/export/grok-bot-export-midori.json` bytes=91972
- `bots/nsca/export/grok-bot-export-nsca.json` bytes=48855
- `bots/scout/export/grok-bot-export-scout.json` bytes=9669045
- `bots/splice/export/grok-bot-export-splice.json` bytes=3911
- `bots/spot/export/grok-bot-export-spot.json` bytes=9459259
- `bots/token-officer/export/grok-bot-export-token-officer.json` bytes=68276
- `scripts/brain_lint.py` bytes=9117

SHA256SUMS.txt in this folder matches these committed bytes. Paths are repo-root paths.
The gzip archive SHA256 was `11038997b4abd2a3a5bf54aacff8c46f7dffd51f1424334ab97abcd2d6c8ae72`, and the archive's own sums checked out before this review.

Sources: attached Personal export archive 2026-11-06; second review of custom skill bodies and personal fields before commit.
