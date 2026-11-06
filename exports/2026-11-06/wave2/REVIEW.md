# Wave2 review

Archive gzip SHA256: `602f59184deca57b76eebe5590cb36caa5a97c50c7aa1f591ec25eb45b631641`.

Internal sums matched for COMPLETENESS.md, both bot JSON files, and scripts/brain_lint.py. INCLUDED.txt did not match. Recorded `c0c66b1b6c98545abe642ab908f5b98f156ceddfb088e2112d117fe12f9d702a`. Extracted file `98c983e7089b07762d6cc2e1b9e86f58557e597aabd5114ad9af927115695044`.

## Coverage

Read in full: Justin and Sage instructions, memories, user facts, and routines (Justin and Sage have no routines). Custom skill bodies on both bots were scanned in full for private names, health and family details, emails, phones, and account or calendar ids. Hits were removed. Public plugin skill text was left intact.

## Corrections

- Sage: 5 memories and 3 user facts removed (personal health, and family or pet grief).
- Shared custom skills present on these bots: one learned health bullet and private-name clauses removed from the writing-style skill; one example name removed from the program-from-eval skill; one private name and a calendar id removed from the morning-brief skill where those strings were present; one host name removed from a PRI skill line. The rest of each skill stayed.
- Justin memories and user facts: no entries removed.
- The lint script was not changed.

SHA256SUMS.txt lists the committed JSON checksums.

Sources: Personal wave2 archive 2026-11-06; review before commit.
