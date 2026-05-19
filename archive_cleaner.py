#!/usr/bin/env python3
"""
archive_cleaner.py — General-purpose archive cleanup tool  (v1.0.0)
=====================================================================

Removes junk artifacts from ZIP, TAR, TAR.GZ, TAR.BZ2, and TAR.XZ archives,
then re-packs them clean.  Great for cleaning repo exports, backups, and
bundles before sharing or long-term storage.

QUICK START (Command Line)
--------------------------
    python archive_cleaner.py archive.zip
    python archive_cleaner.py backup.tar.gz -o clean_backup.tar.gz
    python archive_cleaner.py ~/Downloads/ --recursive
    python archive_cleaner.py archive.zip --dry-run

QUICK START (Python Module)
---------------------------
    from archive_cleaner import clean_archive
    clean_archive("archive.zip")                          # auto-named output
    clean_archive("backup.tar.gz", "clean_backup.tar.gz")  # custom name
    clean_archive("archive.zip", dry_run=True)             # preview only
    clean_archive("archive.zip", verbose=False)            # silent

WHAT GETS REMOVED
-----------------
Junk DIRECTORIES:
    .git, .svn, .hg          — Version control histories
    node_modules, vendor     — Dependency trees
    __pycache__, .pytest_cache, .mypy_cache, .ruff_cache
    .venv, venv, env, virtualenv
    dist, build, target, .tox
    __MACOSX                 — macOS resource fork metadata
    .idea, .vscode, .fleet, .zed
    .sass-cache, .next, .nuxt, .parcel-cache, .cache
    *.egg-info

Junk FILES:
    .DS_Store, Thumbs.db, desktop.ini
    .env, .env.local, .env.development, .env.production
    .coverage, .nvmrc, .python-version, .ruby-version, .node-version
    *~ (backup files ending with tilde)

Junk EXTENSIONS:
    .pyc, .pyo, .pyd        — Compiled Python
    .log, .tmp, .temp
    .swp, .swo              — Vim swap files
    .bak, .orig, .rej       — Patch/merge artifacts
    .class, .o, .obj, .so, .dylib, .dll, .exe
    .min.js, .min.css       — Minified assets

SUPPORTED FORMATS
-----------------
    .zip, .tar, .tar.gz (.tgz), .tar.bz2 (.tbz2), .tar.xz (.txz)

HOW IT WORKS
------------
1. EXTRACT  → Unpack archive to a temp directory
2. CLEAN    → Walk tree top-down, remove junk dirs/files
3. REPACK   → Re-create archive with clean content only
4. OUTPUT   → Write <stem>-cleaned.<ext> next to original

The original archive is NEVER modified.  All work happens in a temp
directory that is automatically deleted when done.

OUTPUT NAMING
-------------
Default: <stem>-cleaned.<ext>
    archive.zip        →  archive-cleaned.zip
    backup.tar.gz      →  backup-cleaned.tar.gz
Override with -o / --output:
    python archive_cleaner.py archive.zip -o release.zip

EXAMPLES
--------
# Single archive, default output
    python archive_cleaner.py project-export.zip

# Custom output name
    python archive_cleaner.py backup.tar.gz -o clean_backup.tar.gz

# Preview what would be removed (no changes)
    python archive_cleaner.py archive.zip --dry-run

# Process every archive in a folder
    python archive_cleaner.py ~/Downloads/old-archives/ --recursive

# Silent mode
    python archive_cleaner.py huge-archive.zip --quiet

SAFETY NOTES
------------
• Original archive is never touched — only read.
• All operations happen in a temporary directory.
• Use --dry-run first on unfamiliar archives to preview removals.
• .env files are removed by default (often contain secrets).

EXIT CODES
----------
    0  — Success
    1  — Error (not found, unsupported format, I/O failure)
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Default junk patterns
# ---------------------------------------------------------------------------

DEFAULT_JUNK_DIRS: set[str] = {
    ".git", ".svn", ".hg",
    "node_modules", "vendor",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", "virtualenv",
    "dist", "build", "target", ".tox", "__MACOSX",
    ".idea", ".vscode", ".fleet", ".zed",
    ".sass-cache", ".next", ".nuxt", ".parcel-cache", ".cache",
}

DEFAULT_JUNK_FILES: set[str] = {
    ".DS_Store", "Thumbs.db", "desktop.ini",
    ".env", ".env.local", ".env.development", ".env.production",
    ".coverage", ".nvmrc", ".python-version", ".ruby-version", ".node-version",
}

DEFAULT_JUNK_EXTENSIONS: tuple[str, ...] = (
    ".pyc", ".pyo", ".pyd", ".log", ".tmp", ".temp",
    ".swp", ".swo", ".bak", ".orig", ".rej",
    ".class", ".o", ".obj", ".so", ".dylib", ".dll", ".exe",
    ".min.js", ".min.css",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_junk_dir(name: str) -> bool:
    if name in DEFAULT_JUNK_DIRS:
        return True
    if name.endswith(".egg-info"):
        return True
    return False

def is_junk_file(name: str) -> bool:
    if name in DEFAULT_JUNK_FILES:
        return True
    if name.endswith("~"):
        return True
    if name.endswith(DEFAULT_JUNK_EXTENSIONS):
        return True
    return False

def _archive_format(path: Path) -> str | None:
    suffixes = [s.lower() for s in path.suffixes]
    name_lower = path.name.lower()
    if ".tar.gz" in name_lower or ".tgz" in name_lower:
        return "tar.gz"
    if ".tar.bz2" in name_lower or ".tbz2" in name_lower:
        return "tar.bz2"
    if ".tar.xz" in name_lower or ".txz" in name_lower:
        return "tar.xz"
    if ".tar" in suffixes:
        return "tar"
    if ".zip" in suffixes:
        return "zip"
    return None

def _default_output(path: Path) -> Path:
    stem = path.stem
    if path.suffixes and path.suffixes[-1].lower() in {".gz", ".bz2", ".xz"}:
        stem = Path(path.name[: -len("".join(path.suffixes[-2:]))]).stem
    suffix = "".join(path.suffixes)
    return path.parent / f"{stem}-cleaned{suffix}"

# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_archive(archive_path: Path, extract_dir: Path) -> None:
    fmt = _archive_format(archive_path)
    if fmt is None:
        raise ValueError(f"Unsupported archive format: {archive_path}")
    if fmt == "zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extract_dir)
    else:
        mode = "r:" + fmt.replace("tar.", "") if fmt != "tar" else "r"
        with tarfile.open(archive_path, mode) as tf:
            for member in tf.getmembers():
                member_path = extract_dir / member.name
                try:
                    member_path.resolve().relative_to(extract_dir.resolve())
                except ValueError:
                    continue
                tf.extract(member, extract_dir)

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def clean_directory(root: Path, *, dry_run: bool = False) -> tuple[int, int]:
    dirs_removed = 0
    files_removed = 0
    for dirpath, dirnames, filenames in os.walk(str(root), topdown=True):
        for d in list(dirnames):
            if is_junk_dir(d):
                full = Path(dirpath) / d
                if not dry_run:
                    shutil.rmtree(full, ignore_errors=True)
                dirnames.remove(d)
                dirs_removed += 1
                if dry_run:
                    print(f"  [dry-run] would remove dir:  {full.relative_to(root)}")
        for f in filenames:
            if is_junk_file(f):
                full = Path(dirpath) / f
                if not dry_run:
                    full.unlink(missing_ok=True)
                files_removed += 1
                if dry_run:
                    print(f"  [dry-run] would remove file: {full.relative_to(root)}")
    return dirs_removed, files_removed

# ---------------------------------------------------------------------------
# Repacking
# ---------------------------------------------------------------------------

def repack_zip(source_dir: Path, output_path: Path) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _, filenames in os.walk(str(source_dir)):
            for f in filenames:
                full = Path(dirpath) / f
                rel = full.relative_to(source_dir)
                zf.write(full, rel)

def repack_tar(source_dir: Path, output_path: Path, fmt: str) -> None:
    mode_map = {"tar": "w", "tar.gz": "w:gz", "tar.bz2": "w:bz2", "tar.xz": "w:xz"}
    mode = mode_map.get(fmt, "w")
    with tarfile.open(output_path, mode) as tf:
        for dirpath, _, filenames in os.walk(str(source_dir)):
            for f in filenames:
                full = Path(dirpath) / f
                rel = full.relative_to(source_dir)
                tf.add(full, arcname=str(rel))

def repack(source_dir: Path, output_path: Path) -> None:
    fmt = _archive_format(output_path)
    if fmt is None:
        raise ValueError(f"Cannot determine archive format for: {output_path}")
    if fmt == "zip":
        repack_zip(source_dir, output_path)
    else:
        repack_tar(source_dir, output_path, fmt)

# ---------------------------------------------------------------------------
# Main API
# ---------------------------------------------------------------------------

def clean_archive(
    input_path: str | Path,
    output_path: str | Path | None = None,
    *,
    dry_run: bool = False,
    verbose: bool = True,
) -> Path:
    input_path = Path(input_path).resolve()
    if output_path is None:
        output_path = _default_output(input_path)
    else:
        output_path = Path(output_path).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Archive not found: {input_path}")

    fmt = _archive_format(input_path)
    if fmt is None:
        raise ValueError(f"Unsupported archive format: {input_path}")

    if verbose:
        print(f"{'=' * 60}")
        print(f"Archive: {input_path.name}")
        print(f"Format:  {fmt}")
        print(f"Output:  {output_path.name}")
        print(f"Mode:    {'dry-run' if dry_run else 'live'}")

    with tempfile.TemporaryDirectory(prefix="archive_cleaner_") as tmp:
        extract_dir = Path(tmp) / "extracted"
        extract_dir.mkdir()

        if verbose:
            print("  Extracting...")
        extract_archive(input_path, extract_dir)

        entries = [e for e in extract_dir.iterdir() if not e.name.startswith(".")]
        if len(entries) == 1 and entries[0].is_dir():
            project_root = entries[0]
        else:
            project_root = extract_dir

        if verbose:
            print("  Cleaning...")
        dirs_removed, files_removed = clean_directory(project_root, dry_run=dry_run)

        if verbose:
            print(f"  Removed {dirs_removed} junk dirs, {files_removed} junk files")

        if dry_run:
            if verbose:
                print("  (dry-run: no output archive created)")
            return output_path

        remaining = sum(1 for _ in project_root.rglob("*") if _.is_file())
        if verbose:
            print(f"  Remaining files: {remaining}")

        if verbose:
            print("  Repacking...")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        repack(extract_dir, output_path)

        size_mb = output_path.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  Done: {size_mb:.1f} MB")

    return output_path

def clean_archives(
    paths: Iterable[str | Path],
    *,
    recursive: bool = False,
    dry_run: bool = False,
    verbose: bool = True,
) -> list[Path]:
    results: list[Path] = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            if recursive:
                for child in sorted(p.iterdir()):
                    if _archive_format(child):
                        try:
                            out = clean_archive(child, dry_run=dry_run, verbose=verbose)
                            results.append(out)
                        except Exception as exc:
                            print(f"ERROR: {child.name}: {exc}", file=sys.stderr)
            else:
                print(f"Skipping directory (use --recursive): {p}", file=sys.stderr)
        elif p.is_file():
            try:
                out = clean_archive(p, dry_run=dry_run, verbose=verbose)
                results.append(out)
            except Exception as exc:
                print(f"ERROR: {p.name}: {exc}", file=sys.stderr)
        else:
            print(f"Not found: {p}", file=sys.stderr)
    return results

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Clean junk artifacts from ZIP and TAR archives.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s archive.zip
  %(prog)s backup.tar.gz -o clean_backup.tar.gz
  %(prog)s folder/ --recursive
  %(prog)s archive.zip --dry-run
""",
    )
    parser.add_argument("paths", nargs="+", help="Archive file(s) or directory(s) to clean")
    parser.add_argument("-o", "--output", dest="output", help="Output path (default: *-cleaned.*)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process all archives in directories")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show what would be removed without doing it")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args(argv)

    if args.output and len(args.paths) == 1 and Path(args.paths[0]).is_file():
        try:
            clean_archive(
                args.paths[0], args.output,
                dry_run=args.dry_run, verbose=not args.quiet,
            )
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    else:
        clean_archives(
            args.paths,
            recursive=args.recursive,
            dry_run=args.dry_run,
            verbose=not args.quiet,
        )
    return 0

if __name__ == "__main__":
    sys.exit(main())
