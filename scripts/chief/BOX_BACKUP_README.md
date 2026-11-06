# Box backup (weekly, encrypted, to Achieve Drive "Bot Backups")

Approved by Ryne 2026-10-24. Backs up the files that exist only on this box:
`/home/box/agent-data` (a symlink to `/home/box/sand-data`) and `/workspace`.

Drive folder: "Bot Backups" in the Achieve Drive (private, owner only)
https://drive.google.com/drive/folders/11rLXkils0yPPl_8rStTqAG9CNXm2u01w
folderId `11rLXkils0yPPl_8rStTqAG9CNXm2u01w`, connection `user-Google-drive--achieve`.

## Weekly routine steps
1. `printenv BACKUP_PASSPHRASE >/dev/null || exit 2` (never print the value).
2. Run `python3 /home/box/agent-data/shared/scripts/chief/box_backup.py`
   (about 70 s, exit 0 ok / 1 warnings / 2 error). It prints JSON with `upload_files`.
3. Upload every path in `upload_files` plus the `checksums` file with cursor
   `UploadFile` (connection `user-Google-drive--achieve`, destination.folderId above).
   Run uploads 3 to 7 at a time. Parts are 95 MB because UploadFile caps at 100 MB.
   13 parts take about 2 to 2.5 min.
4. Drive `list_folder` on the folder (pageSize 200, write_to_file) and then run
   `python3 box_backup.py --prune-plan <that file>`. Run `trash_file` on each id under
   `trash`. It only touches files named `box-backup-YYYY-MM-DD.*` and keeps the newest 4 dates.
5. Report: parts, archive size, file count, warnings, and anything that was trashed.

## What is excluded
The script prints and logs paths only, never values.
- **Secrets and credentials:** box-secrets.json, host-secrets.json, chrome-cookie-seed.json,
  gateway.json, teach-queue-key.json, plus any `connector-secrets/`, `secrets/` or `plugin-data/` dir.
- **Key, token and env names:** `.env*`, `*.pem`, `*.key`, `*token*.json/txt`, `*api_key*` and similar.
- **Small text files that hold real-looking keys:** private keys, GitHub, Slack, OpenAI or Anthropic, AWS and Google tokens.
- **Two named files:** the Hawkin key `dbffeefc*.txt`, excluded anywhere it appears, and `/workspace/sc-csv-check/frc-raw.docx`.
- **Byte-identical copies** of any excluded secret file.
- **Rebuildable or bulky files:**
  - Lock files and live sqlite `-wal`/`-shm` files. Each `.db` file is copied with a consistent sqlite backup snapshot instead.
  - venvs, node_modules, caches, `.git` and plugins/cache.
  - Video files (.mov .mp4 .mkv .webm .avi .m4v), .b64 files, and anything over 200 MB.
- **Backup working folders:** `/workspace/box-backups` (the output) and `/workspace/restore-test*`.

The manifest lists each excluded group, with counts and example paths. It is saved
next to the archive (`/workspace/box-backups/box-backup-DATE.manifest.json`, kept
local only) and also inside the encrypted archive as `BACKUP_MANIFEST.json`.
The box keeps the last 2 dates locally.

## Encryption
gpg symmetric AES256, with the passphrase read from env `BACKUP_PASSPHRASE` through a pipe
(it is never on a command line). The plaintext tar.gz is never written to disk. If the
passphrase is lost, the backups cannot be restored.

## Restore
1. Download every `box-backup-DATE.tar.gz.gpg.NNN` part and the `.sha256` file from
   the Drive folder into a single folder under /workspace, using cursor `DownloadFile`
   one to four at a time.
2. Run:

       /home/box/agent-data/shared/scripts/chief/restore_box_backup.sh <that folder> /tmp/restore-test [DATE]

   This checks the part checksums, decrypts, extracts to the scratch dir and verifies
   every file's sha256 against the manifest. It never writes to live paths.
3. Copy back what you need by hand, for example
   `rsync -a /tmp/restore-test/agent-data/workflows/ /home/box/agent-data/workflows/`.

Manual equivalent:

    cat box-backup-DATE.tar.gz.gpg.0* | gpg --batch --pinentry-mode loopback \
      --passphrase-fd 3 --decrypt 3<<<"$BACKUP_PASSPHRASE" | tar -xz -C /tmp/restore-test

Tests: `chief/tests/test_box_backup.py` covers exclusion rules and the prune plan.
