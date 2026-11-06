# Wave3 review

Archive gzip SHA256: `0e23e4dbcfc011cdd94faf887a1c2295af562268f1c53f32506f4e94ba935e31`.

Internal sums matched for COMPLETENESS.md, the four bot JSON files, and scripts/brain_lint.py. INCLUDED.txt did not match. Recorded `68376ed5c2c46fab5ed8ededf1fcfbfeb8f28c11a2e6b7294a65e9c8df8cb8e7`. Extracted file `4d18eebe768aa6a6716852ab069ca3c22315f8160116b0f5342a6b5497dc822d`.

Maverick replaces the shorter wave1 export on purpose. The other wave1 bot exports were not changed.

## Coverage

Read in full: Bookmarks, Dr. Eggbot, Maverick, and Plaid instructions, memories, user facts, and routines. Custom skill bodies were scanned in full for private names, health and family details, emails, phones, and account or calendar ids. Hits were removed. Public plugin skill text was left intact.

## Corrections

- Plaid: 1 memory removed (a private contact name). An order id, page ids, and that same name were removed from the remaining facts and the routine.
- Bookmarks: Notion page and data-source ids removed from facts and one routine. The X user id was already a redaction marker in the archive.
- Dr. Eggbot: bot account ids removed from memories. No memories or facts were dropped.
- Maverick: no memories or facts dropped. The same shared skill strips as wave2 were applied where those private fragments were present.
- The lint script was not changed.

The parent `exports/2026-11-06/SHA256SUMS.txt` Maverick line is updated to this committed file so that check still matches.

SHA256SUMS.txt in this folder lists the committed JSON checksums.

Sources: Personal wave3 archive 2026-11-06; review before commit.
