#!/usr/bin/env python3
"""
Comprehensive file deduplication tool
Finds and removes duplicate files using hash-based comparison
"""

from pathlib import Path
import hashlib
from collections import defaultdict
from datetime import datetime
import json
import os

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folders to exclude from deduplication
EXCLUDE_PATTERNS = [
    "node_modules",
    ".git",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".venv",
    "venv",
    ".env",
    ".idea",
    ".vscode",
    "target",
    "bin",
    "obj",
    ".DS_Store",
    "Archives/repos",  # Archived repos
    "github/",  # Cloned repos
]


def should_exclude(path):
    """Check if path should be excluded"""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False


def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (IOError, OSError, PermissionError):
        return None


def find_duplicates():
    """Find all duplicate files"""
    print("=" * 100)
    print("🔍 SCANNING FOR DUPLICATE FILES")
    print("=" * 100)
    print()
    print("This may take several minutes...")
    print()

    file_hashes = defaultdict(list)
    total_files = 0
    processed = 0

    # Walk through all files
    for root, dirs, files in os.walk(documents_dir):
        # Skip excluded directories
        if any(pattern in root for pattern in EXCLUDE_PATTERNS):
            dirs[:] = []  # Don't recurse into excluded dirs
            continue

        for file in files:
            file_path = Path(root) / file
            total_files += 1

            # Skip excluded files
            if should_exclude(file_path):
                continue

            # Skip very small files (likely empty or system files)
            try:
                if file_path.stat().st_size == 0:
                    continue
            except:
                continue

            # Calculate hash
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                file_hashes[file_hash].append(file_path)
                processed += 1

            if processed % 1000 == 0:
                print(f"   Processed: {processed:,} files...")

    print()
    print(f"✅ Scanned {processed:,} files")
    print()

    # Find duplicates (groups with more than 1 file)
    duplicates = {
        hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1
    }

    return duplicates, file_hashes


def choose_keep_file(file_group):
    """Choose which file to keep from a duplicate group"""
    # Strategy: Keep the file with the shortest path (usually most organized)
    # If paths are same length, keep the one with better organization (fewer special chars)
    file_group = sorted(
        file_group,
        key=lambda p: (
            len(str(p)),  # Shorter path first
            str(p).count("_"),  # Fewer underscores (better naming)
            str(p).count(" "),  # Fewer spaces
            str(p),  # Alphabetical as tiebreaker
        ),
    )
    return file_group[0]


def analyze_duplicates(duplicates):
    """Analyze duplicate groups and generate statistics"""
    print("=" * 100)
    print("📊 DUPLICATE ANALYSIS")
    print("=" * 100)
    print()

    total_duplicate_groups = len(duplicates)
    total_duplicate_files = sum(len(files) for files in duplicates.values())
    total_duplicate_copies = (
        total_duplicate_files - total_duplicate_groups
    )  # Files to remove

    # Calculate total size
    total_size = 0
    size_by_group = []

    for file_hash, files in duplicates.items():
        try:
            file_size = files[0].stat().st_size
            group_size = file_size * (
                len(files) - 1
            )  # Size of duplicates (excluding keep)
            total_size += group_size
            size_by_group.append(
                {
                    "hash": file_hash,
                    "count": len(files),
                    "size": file_size,
                    "waste": group_size,
                    "files": [str(f.relative_to(documents_dir)) for f in files],
                }
            )
        except:
            pass

    # Sort by waste size
    size_by_group.sort(key=lambda x: x["waste"], reverse=True)

    print(f"Total duplicate groups: {total_duplicate_groups:,}")
    print(f"Total duplicate files: {total_duplicate_files:,}")
    print(f"Files to remove: {total_duplicate_copies:,}")
    print(f"Space to recover: {total_size / (1024 * 1024):.2f} MB")
    print()

    # Show top 20 largest duplicate groups
    print("Top 20 largest duplicate groups:")
    print("-" * 100)
    print(f"{'Count':<8} {'Size':<12} {'Waste':<12} {'Example File':<60}")
    print("-" * 100)

    for group in size_by_group[:20]:
        example = group["files"][0]
        if len(example) > 58:
            example = example[:55] + "..."
        print(
            f"{group['count']:<8} {group['size'] / (1024 * 1024):<12.2f} MB "
            f"{group['waste'] / (1024 * 1024):<12.2f} MB {example:<60}"
        )

    return {
        "total_groups": total_duplicate_groups,
        "total_files": total_duplicate_files,
        "files_to_remove": total_duplicate_copies,
        "space_to_recover_mb": round(total_size / (1024 * 1024), 2),
        "groups": size_by_group,
    }


def remove_duplicates(duplicates, dry_run=True):
    """Remove duplicate files, keeping the best copy"""
    print()
    print("=" * 100)
    if dry_run:
        print("🔍 DRY RUN: Duplicate Removal Plan")
    else:
        print("🗑️  REMOVING DUPLICATES")
    print("=" * 100)
    print()

    backup_log = documents_dir / f"DUPLICATE_REMOVAL_LOG_{timestamp}.csv"
    with open(backup_log, "w") as log:
        log.write("removed_file,kept_file,file_hash,size_bytes,removed_at\n")

    removed_count = 0
    removed_size = 0
    errors = 0

    for file_hash, files in duplicates.items():
        # Choose which file to keep
        keep_file = choose_keep_file(files)
        remove_files = [f for f in files if f != keep_file]

        for remove_file in remove_files:
            try:
                file_size = remove_file.stat().st_size

                if not dry_run:
                    # Remove file
                    remove_file.unlink()

                # Log
                with open(backup_log, "a") as log:
                    log.write(
                        f"{remove_file.relative_to(documents_dir)},"
                        f"{keep_file.relative_to(documents_dir)},"
                        f"{file_hash},{file_size},{datetime.now().isoformat()}\n"
                    )

                removed_count += 1
                removed_size += file_size

            except Exception as e:
                print(f"   ⚠️  Error removing {remove_file.name}: {e}")
                errors += 1

    print(
        f"{'Would remove' if dry_run else 'Removed'}: {removed_count:,} duplicate files"
    )
    print(
        f"Space {'to recover' if dry_run else 'recovered'}: {removed_size / (1024 * 1024):.2f} MB"
    )
    if errors > 0:
        print(f"Errors: {errors}")
    print()
    print(f"Backup log: {backup_log.name}")

    if dry_run:
        print()
        print("💡 This was a DRY RUN. No files were actually removed.")
        print("   Run with --remove to actually remove duplicates.")

    return removed_count, removed_size


def main():
    import sys

    dry_run = "--remove" not in sys.argv

    # Find duplicates
    duplicates, all_hashes = find_duplicates()

    if not duplicates:
        print("✅ No duplicates found!")
        return

    # Analyze
    analysis = analyze_duplicates(duplicates)

    # Save analysis report
    report_file = documents_dir / f"DUPLICATE_ANALYSIS_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(
            {
                "timestamp": timestamp,
                "summary": {
                    "total_groups": analysis["total_groups"],
                    "total_files": analysis["total_files"],
                    "files_to_remove": analysis["files_to_remove"],
                    "space_to_recover_mb": analysis["space_to_recover_mb"],
                },
                "top_groups": analysis["groups"][:50],  # Top 50
            },
            f,
            indent=2,
        )

    print(f"📄 Analysis report saved: {report_file.name}")
    print()

    # Remove duplicates
    removed_count, removed_size = remove_duplicates(duplicates, dry_run=dry_run)

    print()
    print("=" * 100)
    print("✅ DEDUPLICATION COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    main()
