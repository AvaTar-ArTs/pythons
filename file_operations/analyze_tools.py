#!/usr/bin/env python3
"""
Analyze tools directory structure and identify organization opportunities
"""

import os
from pathlib import Path
from collections import defaultdict, Counter
import json


def analyze_tools(root_dir):
    """Analyze tools directory structure"""
    tools_dir = Path(root_dir) / "tools"

    if not tools_dir.exists():
        print(f"❌ tools directory not found at {tools_dir}")
        return

    print("🔍 ANALYZING TOOLS DIRECTORY")
    print("=" * 70)
    print(f"Directory: {tools_dir}")
    print()

    # Collect data
    dir_data = []
    file_data = []
    depth_dist = Counter()
    subcategory_stats = defaultdict(lambda: {"dirs": 0, "files": 0, "size": 0})
    small_dirs = []
    deep_nesting = []
    duplicate_names = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(tools_dir):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(tools_dir)
        depth = len(rel_path.parts)

        if depth == 0:
            continue

        # Get subcategory (first level under tools)
        subcategory = rel_path.parts[0] if rel_path.parts else "root"

        # Count files
        file_count = len([f for f in filenames if not f.startswith(".")])

        dir_info = {
            "path": dir_path,
            "relative": str(rel_path),
            "depth": depth,
            "files": file_count,
            "subdirs": len(dirnames),
            "subcategory": subcategory,
            "name": dir_path.name,
        }

        dir_data.append(dir_info)
        depth_dist[depth] += 1
        subcategory_stats[subcategory]["dirs"] += 1

        # Track files
        for filename in filenames:
            if filename.startswith("."):
                continue
            file_path = dir_path / filename
            try:
                stat = file_path.stat()
                size = stat.st_size
                subcategory_stats[subcategory]["files"] += 1
                subcategory_stats[subcategory]["size"] += size

                file_data.append(
                    {
                        "name": filename,
                        "path": str(rel_path / filename),
                        "size": size,
                        "subcategory": subcategory,
                    }
                )
            except:
                pass

        # Identify small directories
        if file_count < 5 and depth > 1:
            small_dirs.append(dir_info)

        # Identify deep nesting
        if depth > 2:
            deep_nesting.append(dir_info)

        # Track duplicate names
        if dir_path.name:
            duplicate_names[dir_path.name.lower()].append(dir_info)

    # Find actual duplicates (same name, multiple locations)
    duplicates = {name: dirs for name, dirs in duplicate_names.items() if len(dirs) > 1}

    return {
        "tools_dir": tools_dir,
        "total_dirs": len(dir_data),
        "total_files": len(file_data),
        "dir_data": dir_data,
        "file_data": file_data,
        "depth_dist": dict(depth_dist),
        "subcategory_stats": dict(subcategory_stats),
        "small_dirs": small_dirs,
        "deep_nesting": deep_nesting,
        "duplicates": duplicates,
    }


def print_analysis(analysis):
    """Print analysis results"""

    print("📊 ANALYSIS RESULTS")
    print("-" * 70)

    # Summary
    print("\n📈 Summary:")
    print(f"   Total directories: {analysis['total_dirs']:,}")
    print(f"   Total files: {analysis['total_files']:,}")

    # Depth distribution
    depth_dist = analysis["depth_dist"]
    print("\n📏 Depth Distribution:")
    for depth in sorted(depth_dist.keys()):
        count = depth_dist[depth]
        percentage = (
            (count / analysis["total_dirs"] * 100) if analysis["total_dirs"] > 0 else 0
        )
        bar = "█" * (count // 5)
        print(f"   Depth {depth:2}: {count:4,} dirs ({percentage:5.1f}%) {bar}")

    # Subcategory statistics
    subcat_stats = analysis["subcategory_stats"]
    print("\n📁 Subcategories (Top 20):")
    sorted_subs = sorted(subcat_stats.items(), key=lambda x: x[1]["dirs"], reverse=True)

    for subcat, stats in sorted_subs[:20]:
        print(
            f"   {subcat:50} {stats['dirs']:4,} dirs | {stats['files']:5,} files | {stats['size'] / (1024 * 1024):6.2f} MB"
        )

    # Small directories
    small_dirs = analysis["small_dirs"]
    print("\n📦 Small Directories (< 5 files, depth > 1):")
    print(f"   Total: {len(small_dirs):,}")

    # Group by subcategory
    small_by_subcat = defaultdict(list)
    for dir_info in small_dirs:
        small_by_subcat[dir_info["subcategory"]].append(dir_info)

    print("   By subcategory:")
    for subcat, dirs in sorted(small_by_subcat.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"      {subcat:45} {len(dirs):4,} small dirs")

    # Deep nesting
    deep_nesting = analysis["deep_nesting"]
    print("\n📂 Deep Nesting (depth > 2):")
    print(f"   Total: {len(deep_nesting):,}")

    deep_by_subcat = defaultdict(list)
    for dir_info in deep_nesting:
        deep_by_subcat[dir_info["subcategory"]].append(dir_info)

    print("   By subcategory:")
    for subcat, dirs in sorted(deep_by_subcat.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"      {subcat:45} {len(dirs):4,} deep dirs")

    # Duplicates
    duplicates = analysis["duplicates"]
    print("\n🔄 Duplicate Directory Names:")
    print(f"   Total duplicate names: {len(duplicates)}")

    if duplicates:
        print("   Top duplicates:")
        for name, dirs in sorted(duplicates.items(), key=lambda x: -len(x[1]))[:10]:
            print(f"      '{name}': {len(dirs)} occurrences")
            for d in dirs[:3]:
                print(f"         - {d['relative']}")
            if len(dirs) > 3:
                print(f"         ... and {len(dirs) - 3} more")


def suggest_fixes(analysis):
    """Suggest fixes and improvements"""

    print("\n💡 SUGGESTED FIXES")
    print("=" * 70)

    suggestions = []

    # 1. Flatten deep nesting
    deep_nesting = analysis["deep_nesting"]
    if deep_nesting:
        print("\n1️⃣  Flatten Deep Nesting:")
        print(f"   • {len(deep_nesting):,} directories at depth > 2")
        print("   • Flatten to depth 2 (merge intermediate levels)")
        print(f"   • Expected reduction: ~{len(deep_nesting) // 2:,} directories")
        suggestions.append(
            {
                "fix": "flatten_deep",
                "count": len(deep_nesting),
                "expected_reduction": len(deep_nesting) // 2,
            }
        )

    # 2. Merge small directories
    small_dirs = analysis["small_dirs"]
    if small_dirs:
        print("\n2️⃣  Merge Small Directories:")
        print(f"   • {len(small_dirs):,} small directories (< 5 files)")
        print("   • Merge into parent directories")
        print(f"   • Expected reduction: ~{int(len(small_dirs) * 0.7):,} directories")
        suggestions.append(
            {
                "fix": "merge_small",
                "count": len(small_dirs),
                "expected_reduction": int(len(small_dirs) * 0.7),
            }
        )

    # 3. Consolidate duplicates
    duplicates = analysis["duplicates"]
    if duplicates:
        total_dup_dirs = sum(len(dirs) - 1 for dirs in duplicates.values())
        print("\n3️⃣  Consolidate Duplicate Names:")
        print(f"   • {len(duplicates)} duplicate directory names")
        print(f"   • {total_dup_dirs} directories that could be merged")
        print(f"   • Expected reduction: ~{total_dup_dirs:,} directories")
        suggestions.append(
            {
                "fix": "consolidate_duplicates",
                "count": len(duplicates),
                "expected_reduction": total_dup_dirs,
            }
        )

    # 4. Organize by subcategory
    subcat_stats = analysis["subcategory_stats"]
    large_subs = [
        (cat, stats) for cat, stats in subcat_stats.items() if stats["dirs"] > 10
    ]

    if large_subs:
        print("\n4️⃣  Organize Large Subcategories:")
        for cat, stats in sorted(large_subs, key=lambda x: -x[1]["dirs"])[:5]:
            print(
                f"   • {cat}: {stats['dirs']} directories → consider further organization"
            )

    # Total potential reduction
    total_reduction = sum(s["expected_reduction"] for s in suggestions)
    current_count = analysis["total_dirs"]

    print("\n💰 TOTAL POTENTIAL REDUCTION:")
    print(f"   Current: {current_count:,} directories")
    print(f"   Potential reduction: ~{total_reduction:,} directories")
    print(f"   Target: ~{current_count - total_reduction:,} directories")
    print(f"   Reduction percentage: ~{(total_reduction / current_count * 100):.1f}%")

    return suggestions


def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"

    # Analyze
    analysis = analyze_tools(root_dir)

    # Print results
    print_analysis(analysis)

    # Suggest fixes
    suggestions = suggest_fixes(analysis)

    # Save report
    report = {
        "summary": {
            "total_directories": analysis["total_dirs"],
            "total_files": analysis["total_files"],
        },
        "depth_distribution": analysis["depth_dist"],
        "subcategory_statistics": {
            cat: {
                "directories": stats["dirs"],
                "files": stats["files"],
                "size_mb": stats["size"] / (1024 * 1024),
            }
            for cat, stats in analysis["subcategory_stats"].items()
        },
        "issues": {
            "small_directories": len(analysis["small_dirs"]),
            "deep_nesting": len(analysis["deep_nesting"]),
            "duplicate_names": len(analysis["duplicates"]),
        },
        "suggestions": suggestions,
    }

    report_file = Path.home() / "tools_analysis_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n💾 Report saved to: {report_file}")
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
