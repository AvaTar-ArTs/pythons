#!/usr/bin/env python3
"""
Smart Version Renaming
Keeps version numbers but adds descriptive context
Format: original-v{N}-{purpose}.py
"""

import json
from pathlib import Path
import re


def analyze_script_purpose(filepath):
    """Analyze script to determine its purpose"""
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
    except:
        return "unknown"

    # Check imports to determine approach
    imports = content.lower()

    # Selenium = browser automation
    if "selenium" in imports:
        return "browser"

    # CSV batch processing
    if "pandas" in imports and "read_csv" in content:
        return "csv-batch"

    # Chunked upload with resume
    if "chunksize" in content and "resumable" in content.lower():
        return "chunked"

    # Simple API
    if "googleapiclient" in imports and len(lines) < 100:
        return "simple"

    # Legacy oauth2client
    if "oauth2client" in imports:
        return "legacy"

    # Check for specific features
    if "thumbnail" in content.lower() and "playlist" in content.lower():
        return "full"

    if "batch" in content.lower():
        return "batch"

    return "api"


def create_rename_plan():
    """Create smart rename plan for versioned scripts"""

    root = Path(str(Path.home()) + "/documents/python")
    report_file = root / "VERSION_ANALYSIS_REPORT.json"

    if not report_file.exists():
        print("? Please run analyze_versions.py first!")
        return

    with open(report_file) as f:
        plan = json.load(f)

    rename_plan = []

    for item in plan:
        base_name = item["base_name"]
        category = item["category"]
        keep_path = Path(item["keep_path"])
        all_versions = [{"name": item["keep"], "path": keep_path}]
        all_versions.extend(
            [{"name": a["name"], "path": Path(a["path"])} for a in item["archive"]]
        )

        # Analyze purpose of each version
        for version in all_versions:
            purpose = analyze_script_purpose(version["path"])

            # Extract version number
            version_match = re.search(r"[-_]?v?(\d+)", version["name"])
            version_num = version_match.group(1) if version_match else "1"

            # Create new name: base-v{N}-{purpose}.py
            new_name = f"{base_name}-v{version_num}-{purpose}.py"

            rename_plan.append(
                {
                    "category": category,
                    "old_name": version["name"],
                    "new_name": new_name,
                    "old_path": str(version["path"]),
                    "new_path": str(version["path"].parent / new_name),
                    "purpose": purpose,
                    "is_keeper": version["path"] == keep_path,
                }
            )

    return rename_plan


def display_rename_plan(rename_plan):
    """Display the rename plan grouped by category"""

    from collections import defaultdict

    by_category = defaultdict(list)

    for item in rename_plan:
        by_category[item["category"]].append(item)

    print("???  SMART RENAME PLAN")
    print("=" * 70)
    print("\nFormat: {base}-v{N}-{purpose}.py")
    print("  where purpose = browser|api|chunked|csv-batch|simple|legacy|etc.\n")

    for category in sorted(by_category.keys()):
        items = by_category[category]
        keepers = [i for i in items if i["is_keeper"]]

        if not items:
            continue

        print(f"\n?? {category}/")
        print("-" * 70)

        # Group by base name
        by_base = defaultdict(list)
        for item in items:
            base = item["new_name"].split("-v")[0]
            by_base[base].append(item)

        for base_name, versions in sorted(by_base.items()):
            print(f"\n  {base_name}:")

            for v in sorted(versions, key=lambda x: x["new_name"]):
                status = "? KEEP" if v["is_keeper"] else "?? ARCHIVE"
                print(f"    {status:12} {v['old_name']:40} ? {v['new_name']}")

    # Save to file
    output_file = Path(str(Path.home()) + "/documents/python/SMART_RENAME_PLAN.json")
    with open(output_file, "w") as f:
        json.dump(rename_plan, f, indent=2)

    print(f"\n?? Full plan saved to: {output_file.name}")

    # Create summary
    total = len(rename_plan)
    keepers = sum(1 for r in rename_plan if r["is_keeper"])

    print(f"\n?? Summary:")
    print(f"  Total files: {total}")
    print(f"  Keepers: {keepers}")
    print(f"  Archive: {total - keepers}")


def main():
    import sys

    print("?? Analyzing script purposes...")
    rename_plan = create_rename_plan()

    if not rename_plan:
        return

    display_rename_plan(rename_plan)

    print("\n" + "=" * 70)
    print("? Rename plan generated!")
    print("\nNext: Review SMART_RENAME_PLAN.json")
    print("Then run: python3 execute_smart_rename.py (I'll create this)")


if __name__ == "__main__":
    main()
