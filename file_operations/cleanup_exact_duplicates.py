#!/usr/bin/env python3
"""
Clean up exact duplicates intelligently - keep best versions, remove others.
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict


def calculate_hash(file_path):
    """Calculate MD5 hash of file."""
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception:
        return None


def score_file(file_path, rel_path):
    """Score file to determine which copy to keep (higher = better)."""
    score = 0

    # Prefer organized subdirectories
    if rel_path.startswith("pdf/") or "/pdf/" in rel_path:
        score += 100
    if rel_path.startswith("html/") or "/html/" in rel_path:
        score += 100
    if rel_path.startswith("IMAGES/") or "/IMAGES/" in rel_path:
        score += 100
    if rel_path.startswith("transcript/") or "/transcript/" in rel_path:
        score += 100
    if rel_path.startswith("analysis/") or "/analysis/" in rel_path:
        score += 100

    # Prefer project folders over root
    if "/" in rel_path and rel_path.count("/") > 0:
        score += 50

    # Penalize root directory
    if "/" not in rel_path or rel_path.count("/") == 0:
        score -= 50

    # Penalize archive folders (keep originals)
    if "archive" in rel_path.lower() or "Discorgraphy_archive" in rel_path:
        score -= 100

    # Penalize files with "copy", "(1)", "(2)" in name
    name_lower = Path(rel_path).name.lower()
    if "copy" in name_lower or "(1)" in name_lower or "(2)" in name_lower:
        score -= 30

    # Prefer files in v4/mp3/ subdirectories over root v4/
    if "v4/mp3/" in rel_path and rel_path.count("/") > 2:
        score += 20

    # Prefer newer files (by modification time)
    try:
        mtime = file_path.stat().st_mtime
        score += mtime / 10000000  # Small boost for newer files
    except:
        pass

    return score


def cleanup_exact_duplicates(root_path, dry_run=True):
    """Clean up exact duplicates."""
    print("=" * 80)
    print("EXACT DUPLICATES CLEANUP")
    print("=" * 80)

    root_path = Path(root_path)
    if not root_path.exists():
        print(f"❌ Error: Directory not found: {root_path}")
        return

    print(f"\n📂 Analyzing: {root_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")

    # Find all files and calculate hashes
    print("\n📋 Scanning files and calculating hashes...")
    hash_map = defaultdict(list)
    file_count = 0

    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            file_count += 1
            if file_count % 1000 == 0:
                print(f"     Processed {file_count} files...", end="\r")

            try:
                size = file_path.stat().st_size
                # Skip very large files for performance
                if size > 100 * 1024 * 1024:  # > 100MB
                    continue

                file_hash = calculate_hash(file_path)
                if file_hash:
                    rel_path = str(file_path.relative_to(root_path))
                    hash_map[file_hash].append(
                        {"path": file_path, "rel_path": rel_path, "size": size}
                    )
            except Exception:
                pass

    print(f"     Processed {file_count} files")

    # Find duplicates
    duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}

    print(f"\n🔍 Found {len(duplicates)} groups of exact duplicates")
    print(f"   Total duplicate files: {sum(len(v) for v in duplicates.values())}")

    # For each duplicate group, keep the best file, mark others for removal
    files_to_remove = []
    files_to_keep = []
    total_wasted = 0

    print("\n📊 Analyzing duplicate groups...")
    for file_hash, file_list in duplicates.items():
        if len(file_list) < 2:
            continue

        # Score each file
        scored_files = []
        for file_info in file_list:
            score = score_file(file_info["path"], file_info["rel_path"])
            scored_files.append((score, file_info))

        # Sort by score (highest first)
        scored_files.sort(key=lambda x: x[0], reverse=True)

        # Keep the best one
        best_file = scored_files[0][1]
        files_to_keep.append(best_file)

        # Mark others for removal
        for score, file_info in scored_files[1:]:
            files_to_remove.append(file_info)
            total_wasted += file_info["size"]

    print("\n📋 CLEANUP PLAN")
    print("=" * 80)
    print(f"\n   Files to keep: {len(files_to_keep)}")
    print(f"   Files to remove: {len(files_to_keep)}")
    print(f"   Space to recover: {total_wasted / 1024 / 1024 / 1024:.2f} GB")

    # Categorize removals
    by_location = defaultdict(list)
    for file_info in files_to_remove:
        rel_path = file_info["rel_path"]
        if "/" not in rel_path:
            by_location["Root Directory"].append(file_info)
        elif "archive" in rel_path.lower():
            by_location["Archive"].append(file_info)
        elif "v4" in rel_path:
            by_location["v4 Project"].append(file_info)
        elif "CoverAlbums" in rel_path or "TrashCaT" in rel_path:
            by_location["Project Folders"].append(file_info)
        else:
            by_location["Other"].append(file_info)

    print("\n   Removals by location:")
    for location, files in sorted(
        by_location.items(), key=lambda x: len(x[1]), reverse=True
    ):
        size = sum(f["size"] for f in files)
        print(
            f"     {location:20s} {len(files):4d} files ({size / 1024 / 1024 / 1024:.2f} GB)"
        )

    # Show sample removals
    print("\n   Sample files to remove:")
    for file_info in files_to_remove[:20]:
        print(
            f"     - {file_info['rel_path']} ({file_info['size'] / 1024 / 1024:.2f} MB)"
        )
    if len(files_to_remove) > 20:
        print(f"     ... and {len(files_to_remove) - 20} more")

    # Execute removal
    if not dry_run:
        print(f"\n🗑️  Removing {len(files_to_remove)} duplicate files...")
        removed_count = 0
        errors = []

        for file_info in files_to_remove:
            try:
                file_info["path"].unlink()
                removed_count += 1
                if removed_count % 100 == 0:
                    print(
                        f"     Removed {removed_count}/{len(files_to_remove)} files...",
                        end="\r",
                    )
            except Exception as e:
                errors.append(f"{file_info['rel_path']}: {e}")

        print(f"\n     ✓ Removed {removed_count} files")
        if errors:
            print(f"     ⚠️  Errors ({len(errors)}):")
            for error in errors[:5]:
                print(f"       - {error}")
    else:
        print("\n💡 Run with --execute to actually remove files")

    return {
        "to_remove": files_to_remove,
        "to_keep": files_to_keep,
        "wasted_space": total_wasted,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cleanup_exact_duplicates.py <directory> [--execute]")
        print("\nExample:")
        print("  python cleanup_exact_duplicates.py /path/to/dir          # Dry run")
        print(
            "  python cleanup_exact_duplicates.py /path/to/dir --execute # Actually remove"
        )
        sys.exit(1)

    root_path = sys.argv[1]
    dry_run = "--execute" not in sys.argv

    results = cleanup_exact_duplicates(root_path, dry_run)

    if not dry_run and results:
        print("\n✅ Cleanup complete!")
        print(f"   Recovered {results['wasted_space'] / 1024 / 1024 / 1024:.2f} GB")
