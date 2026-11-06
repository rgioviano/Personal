#!/usr/bin/env bash
# Restore a box backup made by box_backup.py into a SCRATCH directory.
# Usage: restore_box_backup.sh <dir-with-archive-or-parts> <dest-dir> [YYYY-MM-DD]
#   Passphrase comes from env BACKUP_PASSPHRASE (never typed on the command line).
#   Verifies part checksums (.sha256), decrypts, extracts, then checks every
#   extracted file's sha256 against BACKUP_MANIFEST.json.
#   It never writes to live paths. Copy what you need back by hand, e.g.
#   rsync -a <dest>/agent-data/workflows/ /home/box/agent-data/workflows/
# Exit codes: 0 restore verified, 1 verify mismatches, 2 error.
set -euo pipefail
SRC=${1:?source dir}; DEST=${2:?dest dir}; DATE=${3:-}
[ -n "${BACKUP_PASSPHRASE:-}" ] || { echo "BACKUP_PASSPHRASE not set" >&2; exit 2; }
cd "$SRC"
if [ -z "$DATE" ]; then
  DATE=$(ls box-backup-*.tar.gz.gpg* 2>/dev/null | sed -E 's/^box-backup-([0-9-]{10}).*/\1/' | sort -u | tail -1)
fi
[ -n "$DATE" ] || { echo "no box-backup-*.tar.gz.gpg[.NNN] in $SRC" >&2; exit 2; }
BASE="box-backup-$DATE.tar.gz.gpg"
if ls "$BASE".[0-9][0-9][0-9] >/dev/null 2>&1; then PARTS=$(ls "$BASE".[0-9][0-9][0-9] | sort); else PARTS="$BASE"; fi
if [ -f "box-backup-$DATE.sha256" ]; then
  # check the parts that are present (whole-archive line is skipped when split)
  grep -F -f <(printf '%s\n' $PARTS) "box-backup-$DATE.sha256" | sha256sum -c --quiet - \
    || { echo "checksum mismatch on downloaded parts" >&2; exit 2; }
  echo "part checksums OK ($(echo $PARTS | wc -w) file(s))"
fi
mkdir -p "$DEST"; chmod 700 "$DEST"
cat $PARTS | gpg --batch --quiet --pinentry-mode loopback --passphrase-fd 3 --decrypt 3<<<"$BACKUP_PASSPHRASE" \
  | tar -xz -C "$DEST"
echo "extracted to $DEST"
python3 - "$DEST" <<'PY'
import hashlib, json, os, sys
d = sys.argv[1]; m = json.load(open(os.path.join(d, "BACKUP_MANIFEST.json")))
bad = missing = ok = 0
for f in m["files"]:
    if "sha256" not in f: continue
    p = os.path.join(d, f["path"])
    if not os.path.isfile(p): missing += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == f["sha256"]: ok += 1
    else: bad += 1
print(json.dumps({"manifest_files": m["file_count"], "verified": ok, "mismatch": bad, "missing": missing}))
sys.exit(0 if bad == missing == 0 and ok == m["file_count"] else 1)
PY
