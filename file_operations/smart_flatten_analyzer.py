import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Smart Directory Flattening Analyzer
Analyzes structure and suggests intelligent improvements
"""

import os
from pathlib import Path
from collections import defaultdict, Counter
import json


def analyze_structure(root_dir):
    """Analyze directory structure intelligently"""
    root = Path(root_dir)

    print("🔍 SMART STRUCTURE ANALYSIS")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print()

    # Collect data
    dir_data = []
    depth_dist = Counter()
    category_dirs = defaultdict(list)
    small_dirs_by_category = defaultdict(list)
    deep_nesting = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "__pycache__", ".vscode")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth == 0:
            continue

        # Count files
        file_count = len([f for f in filenames if not f.startswith(".")])

        # Get category (top-level)
        category = rel_path.parts[0] if rel_path.parts else "root"

        dir_info = {
            "path": dir_path,
            "relative": str(rel_path),
            "depth": depth,
            "files": file_count,
            "subdirs": len(dirnames),
            "category": category,
            "name": dir_path.name,
        }

        dir_data.append(dir_info)
        depth_dist[depth] += 1
        category_dirs[category].append(dir_info)

        # Identify small directories
        if file_count < 5 and depth > 2:
            small_dirs_by_category[category].append(dir_info)

        # Identify deep nesting
        if depth > 3:
            deep_nesting.append(dir_info)

    return {
        "dirs": dir_data,
        "depth_dist": dict(depth_dist),
        "categories": dict(category_dirs),
        "small_dirs": dict(small_dirs_by_category),
        "deep_nesting": deep_nesting,
    }


def analyze_patterns(analysis):
    """Identify patterns and opportunities"""

    print("📊 STRUCTURE ANALYSIS")
    print("-" * 70)

    # Depth distribution
    depth_dist = analysis["depth_dist"]
    print("\n📏 Depth Distribution:")
    for depth in sorted(depth_dist.keys()):
        count = depth_dist[depth]
        bar = "█" * (count // 10)
        print(f"   Depth {depth:2}: {count:4,} dirs {bar}")

    # Category analysis
    categories = analysis["categories"]
    print("\n📁 Directories by Category (Top 15):")
    cat_sizes = [(cat, len(dirs)) for cat, dirs in categories.items()]
    cat_sizes.sort(key=lambda x: -x[1])

    for cat, count in cat_sizes[:15]:
        small_count = len(analysis["small_dirs"].get(cat, []))
        deep_count = len([d for d in categories[cat] if d["depth"] > 3])
        print(
            f"   {cat:30} {count:4,} dirs | {small_count:3} small | {deep_count:3} deep"
        )

    # Small directories
    all_small = []
    for dirs in analysis["small_dirs"].values():
        all_small.extend(dirs)

    print("\n📦 Small Directories Analysis:")
    print(f"   Total small dirs (< 5 files, depth > 2): {len(all_small):,}")

    # Group small dirs by parent
    small_by_parent = defaultdict(list)
    for dir_info in all_small:
        parent = str(Path(dir_info["relative"]).parent)
        small_by_parent[parent].append(dir_info)

    merge_opportunities = [
        (parent, dirs) for parent, dirs in small_by_parent.items() if len(dirs) >= 2
    ]

    print(
        f"   Merge opportunities (≥2 small dirs per parent): {len(merge_opportunities):,}"
    )

    # Deep nesting
    deep_nesting = analysis["deep_nesting"]
    print("\n📂 Deep Nesting Analysis:")
    print(f"   Directories at depth > 3: {len(deep_nesting):,}")

    # Group by category
    deep_by_category = defaultdict(list)
    for dir_info in deep_nesting:
        deep_by_category[dir_info["category"]].append(dir_info)

    print("   Deep nesting by category:")
    for cat, dirs in sorted(deep_by_category.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"      {cat:30} {len(dirs):4,} deep dirs")

    return {
        "merge_opportunities": merge_opportunities,
        "deep_by_category": dict(deep_by_category),
        "cat_sizes": cat_sizes,
    }


def suggest_improvements(analysis, patterns):
    """Suggest intelligent improvements"""

    print("\n💡 INTELLIGENT SUGGESTIONS")
    print("=" * 70)

    suggestions = []

    # 1. Category-specific strategies
    cat_sizes = patterns["cat_sizes"]
    deep_by_category = patterns["deep_by_category"]

    print("\n🎯 Category-Specific Strategies:")

    for cat, count in cat_sizes[:10]:
        deep_count = len(deep_by_category.get(cat, []))
        small_count = len(analysis["small_dirs"].get(cat, []))

        strategy = []
        potential_reduction = 0

        # Strategy based on characteristics
        if count > 200:
            strategy.append(f"🔹 Major consolidation target ({count} dirs)")
            if deep_count > 50:
                strategy.append(
                    f"   → Flatten deep structures (could reduce ~{deep_count // 2} dirs)"
                )
                potential_reduction += deep_count // 2
            if small_count > 30:
                strategy.append(
                    f"   → Merge small dirs (could reduce ~{small_count * 0.7:.0f} dirs)"
                )
                potential_reduction += int(small_count * 0.7)

        elif count > 50:
            strategy.append(f"🔸 Moderate consolidation ({count} dirs)")
            if deep_count > 20:
                strategy.append(
                    f"   → Flatten depth > 3 (could reduce ~{deep_count // 2} dirs)"
                )
                potential_reduction += deep_count // 2
            if small_count > 10:
                strategy.append(
                    f"   → Merge small dirs (could reduce ~{small_count * 0.6:.0f} dirs)"
                )
                potential_reduction += int(small_count * 0.6)

        if strategy:
            print(f"\n   {cat}:")
            for s in strategy:
                print(f"      {s}")
            if potential_reduction > 0:
                print(
                    f"      💰 Potential reduction: ~{potential_reduction} directories"
                )

            suggestions.append(
                {
                    "category": cat,
                    "current_count": count,
                    "potential_reduction": potential_reduction,
                    "strategies": strategy,
                }
            )

    # 2. Global strategies
    print("\n🌐 Global Strategies:")

    total_dirs = len(analysis["dirs"])
    deep_count = len(analysis["deep_nesting"])
    small_count = len(
        [d for d in analysis["dirs"] if d["files"] < 5 and d["depth"] > 2]
    )

    print("\n   1. Aggressive Depth Flattening:")
    print(f"      Current: {deep_count:,} directories at depth > 3")
    print("      Strategy: Flatten all depth > 3 to depth 3")
    print(f"      Potential reduction: ~{deep_count // 3 * 2:,} directories")

    print("\n   2. Small Directory Merging:")
    print(f"      Current: {small_count:,} small directories (< 5 files, depth > 2)")
    print("      Strategy: Merge into parents or combine similar")
    print(f"      Potential reduction: ~{int(small_count * 0.65):,} directories")

    print("\n   3. Duplicate Name Consolidation:")
    merge_ops = patterns["merge_opportunities"]
    print(f"      Current: {len(merge_ops):,} parents with multiple small dirs")
    print("      Strategy: Merge directories with same/similar names")
    print(f"      Potential reduction: ~{len(merge_ops) * 2:,} directories")

    # Calculate total potential
    total_potential = (
        (deep_count // 3 * 2) + int(small_count * 0.65) + (len(merge_ops) * 2)
    )

    print(f"\n   💰 TOTAL POTENTIAL REDUCTION: ~{total_potential:,} directories")
    print(f"      Target: {total_dirs - total_potential:,} directories")
    print(f"      Reduction percentage: ~{(total_potential / total_dirs * 100):.1f}%")

    return suggestions, total_potential


def generate_improved_strategy(analysis, patterns):
    """Generate improved flattening strategy"""

    print("\n🚀 IMPROVED FLATTENING STRATEGY")
    print("=" * 70)

    strategy_steps = []

    # Step 1: Smart category-based flattening
    deep_by_category = patterns["deep_by_category"]

    print("\n📋 Step 1: Category-Priority Flattening")
    print("   Focus on high-impact categories first:")

    priority_cats = sorted(deep_by_category.items(), key=lambda x: -len(x[1]))[:5]

    for cat, dirs in priority_cats:
        count = len(dirs)
        print(f"   • {cat}: {count} deep directories → flatten to depth 3")
        strategy_steps.append(
            {
                "step": 1,
                "category": cat,
                "action": "flatten_deep",
                "count": count,
                "expected_reduction": count // 2,
            }
        )

    # Step 2: Intelligent small dir merging
    print("\n📋 Step 2: Intelligent Small Directory Merging")
    small_dirs = analysis["small_dirs"]

    total_small = sum(len(dirs) for dirs in small_dirs.values())
    print(f"   • Merge {total_small} small directories intelligently")
    print("   • Group by parent and merge when beneficial")
    print(f"   • Expected reduction: ~{int(total_small * 0.65)} directories")

    strategy_steps.append(
        {
            "step": 2,
            "action": "merge_small",
            "count": total_small,
            "expected_reduction": int(total_small * 0.65),
        }
    )

    # Step 3: Duplicate consolidation
    print("\n📋 Step 3: Duplicate Name Consolidation")
    merge_ops = patterns["merge_opportunities"]
    print(f"   • Consolidate {len(merge_ops)} duplicate/similar directory names")
    print(f"   • Expected reduction: ~{len(merge_ops) * 2} directories")

    strategy_steps.append(
        {
            "step": 3,
            "action": "consolidate_duplicates",
            "count": len(merge_ops),
            "expected_reduction": len(merge_ops) * 2,
        }
    )

    # Step 4: Empty directory cleanup
    print("\n📋 Step 4: Empty Directory Cleanup")
    print("   • Remove all empty directories")
    print("   • Clean up after merges")

    strategy_steps.append(
        {"step": 4, "action": "cleanup_empty", "expected_reduction": "variable"}
    )

    return strategy_steps


def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"

    # Analyze
    analysis = analyze_structure(root_dir)

    # Find patterns
    patterns = analyze_patterns(analysis)

    # Suggest improvements
    suggestions, potential = suggest_improvements(analysis, patterns)

    # Generate strategy
    strategy = generate_improved_strategy(analysis, patterns)

    # Save report
    report = {
        "current_state": {
            "total_directories": len(analysis["dirs"]),
            "depth_distribution": analysis["depth_dist"],
            "categories": {
                cat: len(dirs) for cat, dirs in analysis["categories"].items()
            },
        },
        "opportunities": {
            "deep_nesting_count": len(analysis["deep_nesting"]),
            "small_dirs_count": sum(
                len(dirs) for dirs in analysis["small_dirs"].values()
            ),
            "merge_opportunities": len(patterns["merge_opportunities"]),
        },
        "suggestions": suggestions,
        "potential_reduction": potential,
        "strategy": strategy,
    }

    report_file = Path.home() / "smart_flatten_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n💾 Report saved to: {report_file}")
    print("\n✅ Analysis complete!")
    print("\n💡 Next: Run improved flattening script with these strategies")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)