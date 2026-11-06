#!/usr/bin/env python3
"""Weekly encrypted backup of box-only files (agent-data + /workspace).

Builds box-backup-YYYY-MM-DD.tar.gz.gpg (AES256, passphrase from env
BACKUP_PASSPHRASE) plus a manifest, in /workspace/box-backups.
The plaintext tar.gz never touches disk: tar is streamed into gpg.

Upload + Drive retention are done by the calling agent (Python cannot call
the Drive connector). Archives over --split-mb (95 MB, the UploadFile cap) are split into
.001, .002 ... parts. Use `--prune-plan LISTING.json` to get the Drive file
ids to trash (every part of backups older than the newest --keep dates).

Exit codes: 0 ok, 1 warnings (backup made, see manifest), 2 error.
Secret values are never printed or logged; only paths are reported.
"""
import argparse, datetime as dt, fnmatch, hashlib, io, json, os, re, shutil
import sqlite3, stat, subprocess, sys, tarfile, tempfile, time

AGENT_DATA_LINK = "/home/box/agent-data"
WORKSPACE = "/workspace"
OUT_DIR = "/workspace/box-backups"
MAX_BYTES = 200 * 1024 * 1024
NAME_RE = re.compile(r"^box-backup-(\d{4}-\d{2}-\d{2})\.tar\.gz\.gpg(?:\.(\d{3}))?$")
DRIVE_RE = re.compile(r"^box-backup-(\d{4}-\d{2}-\d{2})\.(?:tar\.gz\.gpg(?:\.\d{3})?|sha256|manifest\.json)$")
SPLIT_MB = 95  # UploadFile accepts at most 100 MB per file

# --- exclusion rules -------------------------------------------------------
EXACT_NAMES = {  # secrets / credentials anywhere
    "box-secrets.json", "host-secrets.json", "chrome-cookie-seed.json",
    "gateway.json", "teach-queue-key.json", ".netrc", ".git-credentials",
    ".npmrc", ".pypirc", ".hawkin_access",
}
EXCL_DIRS = {  # directory names pruned anywhere
    "connector-secrets", "secrets", "plugin-data", ".ssh", ".gnupg",
    "node_modules", "__pycache__", ".cache", "site-packages", ".git",
    ".playwright-mcp", ".ytvenv", ".overlay-venv", ".pytest_cache",
    ".mypy_cache", ".npm", ".pnpm-store", "venv",
}
EXCL_DIR_GLOBS = [".venv*", "*.venv"]
EXCL_BASENAME_GLOBS = ["dbffeefc*.txt"]  # Hawkin key; agent attachments keep copies under the same hash name
EXCL_PATHS = [  # absolute (real) path globs
    "/workspace/box-backups", "/workspace/box-backups/*",
    "/workspace/uploads/dbffeefc*.txt",       # plaintext Hawkin key
    "/workspace/sc-csv-check/frc-raw.docx",   # contains a login
    "/home/box/sand-data/plugins/cache",      # re-downloadable plugin cache
    "/workspace/restore-test*",
]
SECRET_NAME_RE = re.compile(
    r"(^\.env$|^\.env\.|\.env$|\.pem$|\.key$|\.p12$|\.pfx$|\.keystore$|^id_rsa|^id_ed25519|^id_ecdsa"
    r"|access[_-]?token|refresh[_-]?token|api[_-]?key|apikey|credential|oauth"
    r"|secrets?\.(json|txt|ya?ml|env|toml)$|(^|[_.-])tokens?\.(json|txt)$"
    r"|[_-]key\.(json|txt)$|cookies?\.(json|txt|sqlite)$|hawkin_access)", re.I)
MEDIA_EXT = {".mov", ".mp4", ".m4v", ".mkv", ".webm", ".avi", ".b64"}
JUNK_RE = re.compile(r"(\.lock$|-wal$|-shm$|-journal$|\.pyc$|\.swp$)")
# High-confidence secret content patterns (values are never printed).
SECRET_CONTENT_RE = re.compile(
    rb"-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}"
    rb"|gh[ousr]_[A-Za-z0-9]{36}|xox[abposr]-[0-9]{6,}-[A-Za-z0-9-]{10,}"
    rb"|sk-(?:ant-|proj-)[A-Za-z0-9_-]{32,}|AKIA[0-9A-Z]{16}|ya29\.[A-Za-z0-9_-]{20,}"
    rb"|1//0[A-Za-z0-9_-]{30,}")
CONTENT_SCAN_MAX = 2 * 1024 * 1024  # small files: excluded on a hit
CONTENT_SCAN_EXT = {".json", ".txt", ".md", ".env", ".yaml", ".yml", ".toml", ".ini",
                    ".cfg", ".conf", ".sh", ".py", ".js", ".ts", ".csv", ""}


def log(msg):
    print(f"[box_backup] {msg}", file=sys.stderr, flush=True)


def classify(real, name, is_dir):
    """Return exclusion reason or None."""
    for g in EXCL_PATHS:
        if fnmatch.fnmatch(real, g):
            return "excluded-path"
    if is_dir:
        if name in EXCL_DIRS or any(fnmatch.fnmatch(name, g) for g in EXCL_DIR_GLOBS):
            return "excluded-dir"
        return None
    if name in EXACT_NAMES or any(fnmatch.fnmatch(name, g) for g in EXCL_BASENAME_GLOBS):
        return "secret-name"
    if name.endswith(".example") or name.endswith(".sample"):
        pass
    elif SECRET_NAME_RE.search(name):
        return "secret-name"
    if JUNK_RE.search(name):
        return "lock-or-live-db-sidecar"
    if os.path.splitext(name)[1].lower() in MEDIA_EXT:
        return "media"
    return None


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def collect(sources):
    """Return (items, excluded, warnings). items: (real_path, arcname, kind, size)."""
    items, excluded, warnings = [], {}, []
    secret_sigs = {}  # size -> {sha256} of excluded secret files, to catch copies elsewhere
    def excl(reason, path, size=0):
        e = excluded.setdefault(reason, {"count": 0, "bytes": 0, "examples": []})
        e["count"] += 1; e["bytes"] += size
        if len(e["examples"]) < 40:
            e["examples"].append(path)
    for root, prefix in sources:
        for dp, dn, fn in os.walk(root, followlinks=False):
            keep = []
            for d in sorted(dn):
                full = os.path.join(dp, d)
                r = classify(full, d, True)
                if r:
                    excl(r, full)
                elif os.path.islink(full):
                    fn.append(d)  # store symlink itself, do not follow
                else:
                    keep.append(d)
            dn[:] = keep
            for f in sorted(fn):
                full = os.path.join(dp, f)
                arc = prefix + "/" + os.path.relpath(full, root)
                try:
                    st = os.lstat(full)
                except OSError as e:
                    warnings.append(f"stat failed: {full}: {e.strerror}"); continue
                if stat.S_ISLNK(st.st_mode):
                    items.append((full, arc, "link", 0)); continue
                if not stat.S_ISREG(st.st_mode):
                    excl("not-regular-file", full); continue
                r = classify(full, f, False)
                if r in ("secret-name", "excluded-path") and 0 < st.st_size <= CONTENT_SCAN_MAX * 10:
                    try:
                        secret_sigs.setdefault(st.st_size, set()).add(sha256_file(full))
                    except OSError:
                        pass
                if r:
                    excl(r, full, st.st_size); continue
                if st.st_size > MAX_BYTES:
                    excl("over-200MB", full, st.st_size); continue
                if (st.st_size <= CONTENT_SCAN_MAX and
                        os.path.splitext(f)[1].lower() in CONTENT_SCAN_EXT):
                    try:
                        with open(full, "rb") as fh:
                            if SECRET_CONTENT_RE.search(fh.read()):
                                excl("secret-content", full, st.st_size); continue
                    except OSError as e:
                        warnings.append(f"read failed: {full}: {e.strerror}"); continue
                kind = "sqlite" if f.endswith((".db", ".sqlite", ".sqlite3")) and st.st_size > 0 else "file"
                items.append((full, arc, kind, st.st_size))
    # second pass: drop byte-identical copies of excluded secret files
    kept = []
    for it in items:
        real, arc, kind, size = it
        if kind != "link" and size in secret_sigs:
            try:
                if sha256_file(real) in secret_sigs[size]:
                    excl("copy-of-secret-file", real, size); continue
            except OSError:
                pass
        kept.append(it)
    return kept, excluded, warnings


def split_file(path, chunk):
    """Split into path.001, path.002 ... when larger than chunk; remove whole file.
    Returns list of part paths ([] if no split was needed)."""
    if os.path.getsize(path) <= chunk:
        return []
    parts, i = [], 1
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            pp = f"{path}.{i:03d}"
            with open(pp, "wb") as o:
                o.write(b)
            parts.append(pp); i += 1
    os.remove(path)
    return parts


def sqlite_snapshot(src, tmpdir):
    dst = os.path.join(tmpdir, hashlib.sha1(src.encode()).hexdigest() + ".db")
    s = sqlite3.connect(f"file:{src}?mode=ro", uri=True, timeout=30)
    d = sqlite3.connect(dst)
    with d:
        s.backup(d)
    s.close(); d.close()
    return dst


def build(args):
    passphrase = os.environ.get(args.passphrase_env)
    if not passphrase:
        log(f"env var {args.passphrase_env} is not set; refusing to build"); return 2
    if not shutil.which("gpg"):
        log("gpg not found"); return 2
    real_ad = os.path.realpath(AGENT_DATA_LINK)
    sources = [(real_ad, "agent-data"), (os.path.realpath(WORKSPACE), "workspace")]
    os.makedirs(args.out_dir, mode=0o700, exist_ok=True)
    date = dt.date.today().isoformat()
    base = f"box-backup-{date}"
    out = os.path.join(args.out_dir, base + ".tar.gz.gpg")
    man_path = os.path.join(args.out_dir, base + ".manifest.json")
    t0 = time.time()
    log(f"collecting from {real_ad} (via {AGENT_DATA_LINK}) and {WORKSPACE}")
    items, excluded, warnings = collect(sources)
    log(f"{len(items)} entries to archive; encrypting to {out}.part")
    tmpdir = tempfile.mkdtemp(prefix="box-backup-", dir="/tmp")
    os.chmod(tmpdir, 0o700)
    files = []
    r_fd, w_fd = os.pipe()
    part = out + ".part"
    old_umask = os.umask(0o077)
    try:
        gpg = subprocess.Popen(
            ["gpg", "--batch", "--yes", "--quiet", "--pinentry-mode", "loopback",
             "--passphrase-fd", str(r_fd), "--symmetric", "--cipher-algo", "AES256",
             "--s2k-digest-algo", "SHA512", "--compress-algo", "none", "-o", part],
            stdin=subprocess.PIPE, pass_fds=(r_fd,), stderr=subprocess.PIPE)
        os.close(r_fd)
        os.write(w_fd, passphrase.encode() + b"\n"); os.close(w_fd)
        with tarfile.open(fileobj=gpg.stdin, mode="w|gz", compresslevel=6) as tar:
            for real, arc, kind, _ in items:
                try:
                    if kind == "link":
                        ti = tar.gettarinfo(real, arcname=arc); tar.addfile(ti)
                        files.append({"path": arc, "type": "symlink", "target": ti.linkname}); continue
                    src = sqlite_snapshot(real, tmpdir) if kind == "sqlite" else real
                    ti = tar.gettarinfo(src, arcname=arc)
                    st = os.stat(real); ti.mtime, ti.mode = st.st_mtime, st.st_mode & 0o7777
                    with open(src, "rb") as fh:  # read once so size can't change mid-tar
                        data = fh.read()
                    ti.size = len(data)
                    tar.addfile(ti, io.BytesIO(data))
                    if kind == "sqlite":
                        os.remove(src)
                    files.append({"path": arc, "size": ti.size, "sha256": hashlib.sha256(data).hexdigest(),
                                  **({"note": "sqlite .backup snapshot"} if kind == "sqlite" else {})})
                except Exception as e:  # file vanished / changed size mid-read
                    warnings.append(f"skipped {arc}: {type(e).__name__}")
            summary = {
                "name": os.path.basename(out), "created": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "host_paths": {"agent-data": f"{AGENT_DATA_LINK} -> {real_ad}", "workspace": WORKSPACE},
                "file_count": sum(1 for f in files if "sha256" in f),
                "symlink_count": sum(1 for f in files if f.get("type") == "symlink"),
                "total_bytes": sum(f.get("size", 0) for f in files),
                "excluded": excluded, "warnings": warnings,
                "encryption": "gpg symmetric AES256, passphrase from env " + args.passphrase_env,
            }
            mbytes = json.dumps({**summary, "files": files}, indent=1).encode()
            ti = tarfile.TarInfo("BACKUP_MANIFEST.json"); ti.size = len(mbytes); ti.mtime = time.time(); ti.mode = 0o600
            tar.addfile(ti, io.BytesIO(mbytes))
        gpg.stdin.close()
        err = gpg.stderr.read().decode(errors="replace"); rc = gpg.wait()
        if rc != 0:
            log(f"gpg failed rc={rc}: {err.strip()[:300]}"); return 2
        os.replace(part, out)
        with open(man_path, "wb") as f:
            f.write(mbytes)
        whole_sha = sha256_file(out)
        whole_bytes = os.path.getsize(out)
        for old in os.listdir(args.out_dir):  # same-day rerun: drop stale parts
            if old.startswith(os.path.basename(out) + ".") and old[-3:].isdigit():
                os.remove(os.path.join(args.out_dir, old))
        parts = split_file(out, args.split_mb * 1024 * 1024)
        sums_path = os.path.join(args.out_dir, base + ".sha256")
        with open(sums_path, "w") as f:  # sha256sum -c format, whole archive + parts
            f.write(f"{whole_sha}  {os.path.basename(out)}\n")
            for pp in parts:
                f.write(f"{sha256_file(pp)}  {os.path.basename(pp)}\n")
    finally:
        os.umask(old_umask)
        shutil.rmtree(tmpdir, ignore_errors=True)
        if os.path.exists(part):
            os.remove(part)
    # local retention: keep the newest --keep-local dates
    dates = sorted({NAME_RE.match(p).group(1) for p in os.listdir(args.out_dir) if NAME_RE.match(p)})
    for old in os.listdir(args.out_dir):
        m = NAME_RE.match(old) or re.match(r"^box-backup-(\d{4}-\d{2}-\d{2})\.(manifest\.json|sha256)$", old)
        if m and m.group(1) in dates[:-args.keep_local]:
            os.remove(os.path.join(args.out_dir, old))
    result = {
        "archive": out if not parts else None, "manifest": man_path,
        "upload_files": parts or [out], "checksums": sums_path,
        "parts": len(parts), "archive_bytes": whole_bytes, "archive_sha256": whole_sha,
        "file_count": summary["file_count"], "total_bytes": summary["total_bytes"],
        "excluded_counts": {k: v["count"] for k, v in excluded.items()},
        "warnings": len(warnings), "seconds": round(time.time() - t0, 1),
        "drive_folder": args.drive_folder, "keep_on_drive": args.keep,
    }
    print(json.dumps(result, indent=1))
    return 1 if warnings else 0


def prune_plan(args):
    """Read a Drive list_folder JSON and print ids of archives to trash."""
    try:
        raw = open(args.prune_plan).read()  # tolerate tool wrapper lines around the JSON
        data = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except Exception as e:
        log(f"cannot read listing: {e}"); return 2
    entries = data.get("files", data) if isinstance(data, dict) else data
    arch = [f for f in entries if isinstance(f, dict) and DRIVE_RE.match(f.get("name", ""))
            and f.get("mimeType", "") != "application/vnd.google-apps.folder"]
    dates = sorted({DRIVE_RE.match(f["name"]).group(1) for f in arch}, reverse=True)
    keep_dates = set(dates[:args.keep])
    keep = [f for f in arch if DRIVE_RE.match(f["name"]).group(1) in keep_dates]
    trash = [f for f in arch if DRIVE_RE.match(f["name"]).group(1) not in keep_dates]
    keep.sort(key=lambda f: f["name"]); trash.sort(key=lambda f: f["name"])
    print(json.dumps({"keep_dates": sorted(keep_dates, reverse=True),
                      "keep": [{"id": f["id"], "name": f["name"]} for f in keep],
                      "trash": [{"id": f["id"], "name": f["name"]} for f in trash]}, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--passphrase-env", default="BACKUP_PASSPHRASE")
    ap.add_argument("--keep-local", type=int, default=2, help="local archives to keep (default 2)")
    ap.add_argument("--keep", type=int, default=4, help="Drive archives to keep (default 4)")
    ap.add_argument("--drive-folder", default="Bot Backups")
    ap.add_argument("--split-mb", type=int, default=SPLIT_MB, help="part size in MB (default 95)")
    ap.add_argument("--prune-plan", metavar="LISTING_JSON")
    a = ap.parse_args()
    try:
        return prune_plan(a) if a.prune_plan else build(a)
    except Exception as e:
        log(f"error: {type(e).__name__}: {e}"); return 2


if __name__ == "__main__":
    sys.exit(main())
