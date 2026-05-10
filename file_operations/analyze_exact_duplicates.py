#!/usr/bin/env python3
"""
Detailed analysis of exact duplicates - compare contents and categorize.
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


def categorize_file(file_path):
    """Categorize file by location and type."""
    rel_path = str(file_path)

    # System files
    if ".DS_Store" in rel_path:
        return "System Files"
    if ".pyc" in rel_path or "__pycache__" in rel_path:
        return "Python Cache"

    # Archive/backup locations
    if "archive" in rel_path.lower() or "backup" in rel_path.lower():
        return "Archive"
    if "Discorgraphy_archive" in rel_path:
        return "Archive"

    # Organized subdirectories
    if rel_path.startswith("pdf/") or "/pdf/" in rel_path:
        return "Organized (pdf/)"
    if rel_path.startswith("html/") or "/html/" in rel_path:
        return "Organized (html/)"
    if rel_path.startswith("IMAGES/") or "/IMAGES/" in rel_path:
        return "Organized (IMAGES/)"
    if rel_path.startswith("transcript/") or "/transcript/" in rel_path:
        return "Organized (transcript/)"
    if rel_path.startswith("analysis/") or "/analysis/" in rel_path:
        return "Organized (analysis/)"

    # Root directory
    if "/" not in rel_path or rel_path.count("/") == 0:
        return "Root Directory"

    # Project subdirectories
    if "CoverAlbums" in rel_path:
        return "Project (CoverAlbums)"
    if "TrashCaTs" in rel_path or "TrashCaT" in rel_path:
        return "Project (TrashCaT)"
    if "mp3-analyze-transcribe" in rel_path:
        return "Project (mp3-analyze)"
    if "v4" in rel_path:
        return "Project (v4)"

    return "Other"


def analyze_exact_duplicates(root_path):
    """Analyze exact duplicates in detail."""
    print("=" * 80)
    print("EXACT DUPLICATES CONTENT ANALYSIS")
    print("=" * 80)

    root_path = Path(root_path)
    if not root_path.exists():
        print(f"❌ Error: Directory not found: {root_path}")
        return

    print(f"\n📂 Analyzing: {root_path}")

    # Find all files and calculate hashes
    print("\n📋 Scanning files and calculating hashes...")
    hash_map = defaultdict(list)
    file_count = 0

    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            file_count += 1
            if file_count % 500 == 0:
                print(f"     Processed {file_count} files...", end="\r")

            # Skip very large files for performance
            try:
                size = file_path.stat().st_size
                if size > 100 * 1024 * 1024:  # Skip files > 100MB
                    continue

                file_hash = calculate_hash(file_path)
                if file_hash:
                    rel_path = str(file_path.relative_to(root_path))
                    hash_map[file_hash].append(
                        {
                            "path": file_path,
                            "rel_path": rel_path,
                            "size": size,
                            "category": categorize_file(rel_path),
                        }
                    )
            except Exception:
                pass

    print(f"     Processed {file_count} files")

    # Find duplicates
    duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}

    print(f"\n🔍 Found {len(duplicates)} groups of exact duplicates")
    print(f"   Total duplicate files: {sum(len(v) for v in duplicates.values())}")

    # Categorize duplicates
    print("\n📊 CATEGORIZING DUPLICATES")
    print("=" * 80)

    by_category = defaultdict(lambda: {"groups": 0, "files": 0, "size": 0})
    by_file_type = defaultdict(lambda: {"groups": 0, "files": 0})

    for file_hash, file_list in duplicates.items():
        if not file_list:
            continue

        # Get file info from first file
        first_file = file_list[0]
        ext = Path(first_file["rel_path"]).suffix.lower() or "(no extension)"
        size = first_file["size"]

        # Count by category
        categories = [f["category"] for f in file_list]
        primary_category = max(set(categories), key=categories.count)

        by_category[primary_category]["groups"] += 1
        by_category[primary_category]["files"] += len(file_list)
        by_category[primary_category]["size"] += size * (
            len(file_list) - 1
        )  # Wasted space

        by_file_type[ext]["groups"] += 1
        by_file_type[ext]["files"] += len(file_list)

    print("\n📁 BY LOCATION CATEGORY:")
    for category, data in sorted(
        by_category.items(), key=lambda x: x[1]["files"], reverse=True
    ):
        wasted_gb = data["size"] / 1024 / 1024 / 1024
        print(
            f"   {category:30s} {data['groups']:4d} groups, {data['files']:5d} files, {wasted_gb:6.2f} GB wasted"
        )

    print("\n📄 BY FILE TYPE:")
    for ext, data in sorted(
        by_file_type.items(), key=lambda x: x[1]["files"], reverse=True
    )[:15]:
        print(f"   {ext:20s} {data['groups']:4d} groups, {data['files']:5d} files")

    # Analyze patterns
    print("\n🔍 DUPLICATE PATTERNS")
    print("=" * 80)

    # Pattern 1: Root vs Organized subdirectories
    root_vs_organized = []
    archive_duplicates = []
    project_duplicates = []

    for file_hash, file_list in duplicates.items():
        if len(file_list) < 2:
            continue

        categories = [f["category"] for f in file_list]
        [f["rel_path"] for f in file_list]

        # Check for root vs organized
        has_root = "Root Directory" in categories
        has_organized = any("Organized" in c for c in categories)

        if has_root and has_organized:
            root_vs_organized.append({"files": file_list, "hash": file_hash})

        # Check for archive duplicates
        if "Archive" in categories:
            archive_duplicates.append({"files": file_list, "hash": file_hash})

        # Check for project duplicates
        if any("Project" in c for c in categories):
            project_duplicates.append({"files": file_list, "hash": file_hash})

    print(f"\n📋 Root vs Organized Subdirectories: {len(root_vs_organized)} groups")
    if root_vs_organized:
        print("   (Files in root that also exist in organized subdirectories)")
        for group in root_vs_organized[:10]:
            files = group["files"]
            root_files = [f for f in files if f["category"] == "Root Directory"]
            org_files = [f for f in files if "Organized" in f["category"]]
            if root_files and org_files:
                print(f"     - {root_files[0]['rel_path']}")
                print(f"       Also in: {org_files[0]['rel_path']}")
        if len(root_vs_organized) > 10:
            print(f"     ... and {len(root_vs_organized) - 10} more")

    print(f"\n📦 Archive Duplicates: {len(archive_duplicates)} groups")
    if archive_duplicates:
        print("   (Files duplicated in archive folders)")
        for group in archive_duplicates[:10]:
            files = group["files"]
            print(f"     - {files[0]['rel_path']} ({len(files)} copies)")
            for f in files[1:3]:
                print(f"       Also: {f['rel_path']}")
        if len(archive_duplicates) > 10:
            print(f"     ... and {len(archive_duplicates) - 10} more")

    print(f"\n📁 Project Duplicates: {len(project_duplicates)} groups")
    if project_duplicates:
        print("   (Files duplicated across project folders)")
        for group in project_duplicates[:10]:
            files = group["files"]
            print(f"     - {files[0]['rel_path']} ({len(files)} copies)")
            for f in files[1:3]:
                print(f"       Also: {f['rel_path']}")
        if len(project_duplicates) > 10:
            print(f"     ... and {len(project_duplicates) - 10} more")

    # Recommendations
    print("\n" + "=" * 80)
    print("CLEANUP RECOMMENDATIONS")
    print("=" * 80)

    total_wasted = sum(
        size * (len(files) - 1)
        for hash_key, files in duplicates.items()
        for size in [files[0]["size"]]
        if files
    )
    total_wasted_gb = total_wasted / 1024 / 1024 / 1024

    print(f"\n💾 Total wasted space: {total_wasted_gb:.2f} GB")

    # Calculate potential savings by category
    root_removable = sum(
        f["size"]
        for group in root_vs_organized
        for f in group["files"]
        if f["category"] == "Root Directory"
    )
    archive_removable = sum(
        f["size"]
        for group in archive_duplicates
        for f in group["files"][1:]
        if "Archive" in f["category"]
    )

    print("\n📋 Recommended cleanup:")
    print(
        f"   1. Remove root duplicates (keep organized versions): {root_removable / 1024 / 1024 / 1024:.2f} GB"
    )
    print(
        f"   2. Remove archive duplicates (keep originals): {archive_removable / 1024 / 1024 / 1024:.2f} GB"
    )
    print("   3. System files (.DS_Store, .pyc): Can be regenerated/removed")

    # Show top duplicate groups by size
    print("\n📦 TOP DUPLICATE GROUPS BY SIZE:")
    size_sorted = sorted(
        duplicates.items(),
        key=lambda x: x[1][0]["size"] * (len(x[1]) - 1) if x[1] else 0,
        reverse=True,
    )

    for hash_key, file_list in size_sorted[:15]:
        if file_list:
            size = file_list[0]["size"]
            wasted = size * (len(file_list) - 1)
            if wasted > 1024 * 1024:  # > 1MB wasted
                print(f"   {file_list[0]['rel_path']}")
                print(
                    f"     Size: {size / 1024 / 1024:.2f} MB, Copies: {len(file_list)}, Wasted: {wasted / 1024 / 1024:.2f} MB"
                )
                for f in file_list[1:3]:
                    print(f"       - {f['rel_path']} ({f['category']})")
                if len(file_list) > 3:
                    print(f"       ... and {len(file_list) - 3} more")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    return {
        "duplicates": duplicates,
        "root_vs_organized": root_vs_organized,
        "archive_duplicates": archive_duplicates,
        "project_duplicates": project_duplicates,
        "total_wasted": total_wasted,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_exact_duplicates.py <directory>")
        sys.exit(1)

    root_path = sys.argv[1]
    analyze_exact_duplicates(root_path)
