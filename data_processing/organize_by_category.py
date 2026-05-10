#!/usr/bin/env python3
"""
Smart File Organization Script
Organizes Python files based on functional category analysis results.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List


def load_analysis_results(analysis_file: str) -> Dict:
    """Load the functional analysis JSON results."""
    with open(analysis_file, "r") as f:
        return json.load(f)


def get_latest_analysis() -> Path:
    """Find the latest analysis JSON file."""
    analysis_dir = Path("functional_analysis")
    if not analysis_dir.exists():
        raise FileNotFoundError(
            "No functional_analysis directory found. Run functional_category_analyzer.py first."
        )

    json_files = list(analysis_dir.glob("functional_analysis_*.json"))
    if not json_files:
        raise FileNotFoundError("No analysis files found.")

    # Get the most recent file
    return max(json_files, key=lambda p: p.stat().st_mtime)


def create_category_structure(base_dir: Path, categories: List[str]):
    """Create directory structure for categories."""
    for category in categories:
        category_dir = base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # Create a simple README for each category
        readme = category_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                f"# {category.replace('-', ' ').title()}\n\n"
                f"Scripts related to {category} functionality.\n"
            )


def organize_files(analysis_data: Dict, dry_run: bool = True):
    """
    Organize files based on analysis results.

    Args:
        analysis_data: Analysis results from functional_category_analyzer
        dry_run: If True, only print what would be done without moving files
    """
    base_dir = Path()
    organized_dir = base_dir / "organized_by_function"

    print(f"\n{'🔍 DRY RUN MODE' if dry_run else '📦 ORGANIZING FILES'}")
    print("=" * 60)

    # Count files per category
    category_counts = {}
    for file_path, file_data in analysis_data["file_categories"].items():
        category = file_data.get("primary_category", "uncategorized")
        category_counts[category] = category_counts.get(category, 0) + 1

    # Create directory structure
    if not dry_run:
        organized_dir.mkdir(exist_ok=True)
        create_category_structure(organized_dir, category_counts.keys())

    # Organize files
    moved_count = 0
    for file_path, file_data in analysis_data["file_categories"].items():
        source = Path(file_path)

        # Skip if file doesn't exist
        if not source.exists():
            continue

        # Get category
        category = file_data.get("primary_category", "uncategorized")
        confidence = file_data.get("confidence", 0)

        # Determine destination
        dest_dir = organized_dir / category
        dest = dest_dir / source.name

        # Handle name conflicts
        if dest.exists() and dest != source:
            base_name = source.stem
            ext = source.suffix
            counter = 1
            while dest.exists():
                dest = dest_dir / f"{base_name}_{counter}{ext}"
                counter += 1

        # Move or print action
        if dry_run:
            print(f"📄 {source.name:50} → {category:30} (confidence: {confidence:.2f})")
        else:
            try:
                shutil.move(str(source), str(dest))
                moved_count += 1
                print(f"✅ Moved: {source.name} → {category}/")
            except Exception as e:
                print(f"❌ Error moving {source.name}: {e}")

    # Print summary
    print("\n" + "=" * 60)
    if dry_run:
        print("✅ Dry run complete. No files were moved.")
        print(
            f"📊 Would organize {len(analysis_data['file_categories'])} files into {len(category_counts)} categories"
        )
        print(
            "\n💡 To actually move files, run: python3 organize_by_category.py --execute"
        )
    else:
        print(
            f"✅ Organized {moved_count} files into {len(category_counts)} categories"
        )
        print(f"📁 Files organized in: {organized_dir}")

    # Show top categories
    print("\n🏆 TOP CATEGORIES:")
    sorted_categories = sorted(
        category_counts.items(), key=lambda x: x[1], reverse=True
    )
    for i, (cat, count) in enumerate(sorted_categories[:10], 1):
        print(f"   {i:2d}. {cat:30} - {count:4d} files")


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Organize Python files by functional category",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (see what would happen)
  python3 organize_by_category.py

  # Actually move files
  python3 organize_by_category.py --execute

  # Use specific analysis file
  python3 organize_by_category.py --execute --analysis my_analysis.json
        """,
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually move files (default is dry run)",
    )

    parser.add_argument(
        "--analysis", type=str, help="Path to analysis JSON file (default: uses latest)"
    )

    args = parser.parse_args()

    # Load analysis
    try:
        if args.analysis:
            analysis_file = Path(args.analysis)
        else:
            analysis_file = get_latest_analysis()

        print(f"📊 Loading analysis from: {analysis_file}")
        analysis_data = load_analysis_results(str(analysis_file))

        # Organize files
        organize_files(analysis_data, dry_run=not args.execute)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
