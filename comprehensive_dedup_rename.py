#!/usr/bin/env python3
"""
Comprehensive Deduplication & Rename
Applies the upload script approach to ALL versioned files
"""

import difflib
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def are_duplicates(file1, file2, threshold=0.95):
    """Check if two files are duplicates (95%+ similar)"""
    try:
        lines1 = open(file1, errors="ignore").readlines()
        lines2 = open(file2, errors="ignore").readlines()
        ratio = difflib.SequenceMatcher(None, lines1, lines2).ratio()
        return ratio >= threshold, ratio
    except:
        return False, 0.0


def analyze_purpose(filepath):
    """Determine script purpose from code"""
    try:
        content = open(filepath, "r", errors="ignore").read().lower()

        # Check for specific purposes
        if "selenium" in content or "webdriver" in content:
            return "browser"
        if "pandas" in content and "read_csv" in content:
            return "csv-batch"
        if "chunksize" in content and "resumable" in content:
            return "api-chunked"
        if "oauth2client" in content:
            return "legacy"
        if "batch" in content or "bulk" in content:
            return "batch"
        if "simple" in content or len(content) < 5000:
            return "simple"
        if "api" in content or "googleapi" in content:
            return "api"

        return "main"
    except:
        return "unknown"


def main():
    root = Path(str(Path.home()) + "/documents/python")
    report_file = root / "VERSION_ANALYSIS_REPORT.json"

    if not report_file.exists():
        print("? Run analyze_versions.py first!")
        return

    with open(report_file) as f:
        version_data = json.load(f)

    print("?? COMPREHENSIVE DEDUPLICATION & RENAME")
    print("=" * 70)
    print(f"Analyzing {len(version_data)} script families...")

    # Analyze each family
    actions = {"keep_rename": [], "delete_duplicate": [], "stats": defaultdict(int)}

    for item in version_data:
        base_name = item["base_name"]
        category = item["category"]
        keep_path = Path(item["keep_path"])
        all_files = [keep_path] + [Path(a["path"]) for a in item["archive"]]

        # Find duplicates within this family
        seen = []
        for filepath in all_files:
            if not filepath.exists():
                continue

            is_dup = False
            for seen_file, seen_purpose in seen:
                is_duplicate, similarity = are_duplicates(filepath, seen_file)
                if is_duplicate:
                    actions["delete_duplicate"].append(
                        {
                            "file": str(filepath),
                            "duplicate_of": str(seen_file),
                            "similarity": similarity,
                            "category": category,
                        }
                    )
                    actions["stats"]["duplicates_deleted"] += 1
                    is_dup = True
                    break

            if not is_dup:
                # Not a duplicate - keep it
                purpose = analyze_purpose(filepath)
                new_name = f"{base_name}_{purpose}.py"

                # If multiple files with same purpose, add version number
                existing_purposes = [p for _, p in seen]
                if purpose in existing_purposes:
                    count = existing_purposes.count(purpose) + 1
                    new_name = f"{base_name}_{purpose}_v{count}.py"

                actions["keep_rename"].append(
                    {
                        "old_path": str(filepath),
                        "old_name": filepath.name,
                        "new_name": new_name,
                        "purpose": purpose,
                        "category": category,
                        "is_original_keeper": filepath == keep_path,
                    }
                )
                actions["stats"]["files_kept"] += 1
                seen.append((filepath, purpose))

    # Display results by category
    print(f"\n?? Analysis Complete:")
    print(f"  Files to keep & rename: {actions['stats']['files_kept']}")
    print(f"  Duplicates to delete: {actions['stats']['duplicates_deleted']}")

    by_category = defaultdict(lambda: {"keep": [], "delete": []})
    for item in actions["keep_rename"]:
        by_category[item["category"]]["keep"].append(item)
    for item in actions["delete_duplicate"]:
        by_category[item["category"]]["delete"].append(item)

    print("\n?? BY CATEGORY:")
    print("=" * 70)

    for category in sorted(by_category.keys()):
        cat_data = by_category[category]
        if not cat_data["keep"] and not cat_data["delete"]:
            continue

        print(f"\n{category}/")
        print(f"  Keep: {len(cat_data['keep'])}, Delete: {len(cat_data['delete'])}")

        # Show renames
        if cat_data["keep"]:
            for item in cat_data["keep"][:5]:  # First 5
                star = "?" if item["is_original_keeper"] else "  "
                print(f"  {star} {item['old_name']:40} ? {item['new_name']}")

            if len(cat_data["keep"]) > 5:
                print(f"     ... and {len(cat_data['keep']) - 5} more")

        # Show deletions
        if cat_data["delete"]:
            print(f"  ? Delete {len(cat_data['delete'])} duplicates")

    # Save execution plan
    output_file = root / "DEDUP_RENAME_PLAN.json"
    with open(output_file, "w") as f:
        json.dump(actions, f, indent=2)

    print(f"\n?? Full plan saved to: {output_file.name}")
    print("\n?? To execute:")
    print("  python3 execute_dedup_rename.py --dry-run   # Preview")
    print("  python3 execute_dedup_rename.py --execute   # Do it")


if __name__ == "__main__":
    main()
