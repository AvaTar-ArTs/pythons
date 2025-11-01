#!/usr/bin/env python3
"""
Script Version Analyzer
Finds all versioned scripts and identifies which version to keep
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

# Patterns to identify versions
VERSION_PATTERNS = [
    r"(.+)-v(\d+)\.py$",  # script-v1.py
    r"(.+)-v(\d+)-(\d+)\.py$",  # script-v1-2.py
    r"(.+)_v?(\d+)\.py$",  # script_v1.py or script_1.py
    r"(.+?)(\d+)\.py$",  # script1.py (if ends with number)
]


def find_versioned_scripts(root_dir):
    """Find all scripts that appear to be versions"""
    versioned_groups = defaultdict(list)

    for filepath in Path(root_dir).rglob("*.py"):
        # Skip archived/backup directories
        if any(
            x in str(filepath)
            for x in ["_ARCHIVED", "_backups", "10-archived-projects", ".git"]
        ):
            continue

        filename = filepath.name

        # Try each version pattern
        for pattern in VERSION_PATTERNS:
            match = re.match(pattern, filename)
            if match:
                base_name = match.group(1)
                version = match.group(2)

                # Get file stats
                stats = filepath.stat()

                versioned_groups[base_name].append(
                    {
                        "path": filepath,
                        "name": filename,
                        "version": version,
                        "size": stats.st_size,
                        "modified": datetime.fromtimestamp(stats.st_mtime),
                        "lines": sum(1 for _ in open(filepath, "r", errors="ignore")),
                    }
                )
                break

    return versioned_groups


def analyze_versions(versions):
    """Determine which version is likely the best"""
    if not versions:
        return None

    # Score each version
    for v in versions:
        score = 0

        # Prefer larger files (more features)
        score += v["size"] / 1000  # Convert to KB

        # Prefer more recent
        days_old = (datetime.now() - v["modified"]).days
        if days_old < 30:
            score += 100
        elif days_old < 90:
            score += 50

        # Prefer more lines of code (more complete)
        score += v["lines"] / 10

        # Prefer higher version numbers
        try:
            score += int(v["version"]) * 10
        except:
            pass

        v["score"] = score

    # Sort by score
    versions.sort(key=lambda x: x["score"], reverse=True)
    return versions[0]


def main():
    root = Path("/Users/steven/documents/python")

    print("?? Analyzing versioned scripts...")
    print("=" * 70)

    versioned_groups = find_versioned_scripts(root)

    # Filter to only groups with multiple versions
    multi_version_groups = {k: v for k, v in versioned_groups.items() if len(v) > 1}

    print(
        f"\n?? Found {len(multi_version_groups)} script families with multiple versions"
    )
    print(
        f"?? Total versioned files: {sum(len(v) for v in multi_version_groups.values())}"
    )

    # Prepare consolidation plan
    consolidation_plan = []

    for base_name in sorted(multi_version_groups.keys()):
        versions = multi_version_groups[base_name]
        best = analyze_versions(versions)

        category = str(versions[0]["path"].parent.name)

        consolidation_plan.append(
            {
                "base_name": base_name,
                "category": category,
                "versions": len(versions),
                "keep": best["name"],
                "keep_path": str(best["path"]),
                "keep_size": best["size"],
                "keep_lines": best["lines"],
                "keep_modified": best["modified"].strftime("%Y-%m-%d"),
                "archive": [
                    {
                        "name": v["name"],
                        "path": str(v["path"]),
                        "size": v["size"],
                        "lines": v["lines"],
                        "modified": v["modified"].strftime("%Y-%m-%d"),
                    }
                    for v in versions
                    if v != best
                ],
            }
        )

    # Display summary by category
    print("\n?? Versioned Scripts by Category:")
    print("-" * 70)

    by_category = defaultdict(list)
    for item in consolidation_plan:
        by_category[item["category"]].append(item)

    for category in sorted(by_category.keys()):
        items = by_category[category]
        total_versions = sum(item["versions"] for item in items)
        print(f"\n{category}/")
        print(f"  {len(items)} script families, {total_versions} total versions")

        # Show top 5 in this category
        for item in sorted(items, key=lambda x: x["versions"], reverse=True)[:5]:
            print(f"  ? {item['base_name']}: {item['versions']} versions")
            print(
                f"    ? Keep: {item['keep']} ({item['keep_lines']} lines, {item['keep_modified']})"
            )

    # Save detailed report
    output_file = root / "VERSION_ANALYSIS_REPORT.json"
    with open(output_file, "w") as f:
        json.dump(consolidation_plan, f, indent=2)

    print(f"\n?? Detailed report saved to: {output_file.name}")

    # Generate markdown summary
    md_file = root / "VERSION_CONSOLIDATION_PLAN.md"
    with open(md_file, "w") as f:
        f.write("# Script Version Consolidation Plan\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Script families with versions:** {len(multi_version_groups)}\n")
        f.write(
            f"- **Total versioned files:** {sum(len(v) for v in multi_version_groups.values())}\n"
        )
        f.write(
            f"- **Files to archive:** {sum(len(item['archive']) for item in consolidation_plan)}\n\n"
        )

        f.write("## Consolidation Plan by Category\n\n")

        for category in sorted(by_category.keys()):
            items = by_category[category]
            f.write(f"### {category}/\n\n")

            for item in sorted(items, key=lambda x: x["versions"], reverse=True):
                f.write(f"#### {item['base_name']} ({item['versions']} versions)\n\n")
                f.write(f"**? KEEP:** `{item['keep']}`\n")
                f.write(f"- Size: {item['keep_size']:,} bytes\n")
                f.write(f"- Lines: {item['keep_lines']}\n")
                f.write(f"- Modified: {item['keep_modified']}\n\n")

                if item["archive"]:
                    f.write(f"**?? ARCHIVE:** ({len(item['archive'])} files)\n")
                    for arch in item["archive"]:
                        f.write(
                            f"- `{arch['name']}` - {arch['lines']} lines, {arch['modified']}\n"
                        )
                    f.write("\n")

    print(f"?? Consolidation plan saved to: {md_file.name}")

    # Show top offenders
    print("\n?? Top 10 Scripts with Most Versions:")
    print("-" * 70)

    top_offenders = sorted(
        consolidation_plan, key=lambda x: x["versions"], reverse=True
    )[:10]
    for i, item in enumerate(top_offenders, 1):
        print(
            f"{i:2}. {item['base_name']:<30} ({item['category']:<15}) - {item['versions']} versions"
        )
        print(f"    Keep: {item['keep']}")

    print("\n" + "=" * 70)
    print("? Analysis complete!")
    print("\nNext steps:")
    print("1. Review: VERSION_CONSOLIDATION_PLAN.md")
    print("2. Run: python3 consolidate_versions.py (I'll create this next)")
    print("3. Test your key scripts still work")
    print("4. Commit the cleanup")


if __name__ == "__main__":
    main()
