#!/usr/bin/env python3
"""
Execute Ultimate Reorganization
Uses the ultimate analysis to reorganize files intelligently
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict


class UltimateReorganizer:
    """Execute reorganization from ultimate analysis"""

    def __init__(self, analysis_file: Path, base_path: Path):
        self.analysis_file = Path(analysis_file)
        self.base_path = Path(base_path).expanduser()
        self.analysis = self._load_analysis()

    def _load_analysis(self) -> Dict:
        """Load analysis report"""
        with open(self.analysis_file, "r") as f:
            return json.load(f)

    def create_backup(self):
        """Create comprehensive backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = (
            self.base_path / "archive" / "backups" / f"before_ultimate_{timestamp}"
        )
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Save directory listing
        listing = backup_dir / "structure.txt"
        with open(listing, "w") as f:
            f.write("Directory structure before ultimate reorganization\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("=" * 70 + "\n\n")

            for item in sorted(self.base_path.iterdir()):
                if item.is_dir() and not item.name.startswith("."):
                    f.write(f"{item.name}/\n")
                elif item.is_file():
                    f.write(f"{item.name}\n")

        print(f"💾 Backup created: {backup_dir.name}")
        return backup_dir

    def execute_hierarchical(self, dry_run: bool = True):
        """Execute hierarchical reorganization"""
        mode = "🔍 DRY RUN" if dry_run else "✅ EXECUTING"
        print(f"\n{mode} - HIERARCHICAL REORGANIZATION")
        print("=" * 70)

        hierarchy = self.analysis["categories"]

        if not dry_run:
            backup = self.create_backup()
            print()

        moved_files = 0
        skipped_files = 0
        errors = 0

        for parent, data in sorted(
            hierarchy.items(), key=lambda x: x[1]["total_files"], reverse=True
        ):
            parent_dir = self.base_path / parent
            print(f"\n📁 {parent}/ ({data['total_files']} files)")

            if not dry_run:
                parent_dir.mkdir(exist_ok=True)

            # Handle files directly in parent
            if data.get("files"):
                for filename in data["files"]:
                    if self._move_file(filename, parent_dir, dry_run):
                        moved_files += 1
                    else:
                        skipped_files += 1

            # Handle subcategories
            for sub_name, sub_data in data.get("subcategories", {}).items():
                sub_dir = self.base_path / sub_name
                print(f"  └─ {sub_name}/ ({sub_data['count']} files)")

                if not dry_run:
                    sub_dir.mkdir(exist_ok=True)

                for filename in sub_data["files"]:
                    if self._move_file(filename, sub_dir, dry_run):
                        moved_files += 1
                    else:
                        skipped_files += 1

        # Results
        print("\n" + "=" * 70)
        print("📊 RESULTS")
        print("=" * 70)
        print(f"\nFiles moved: {moved_files}")
        print(f"Files skipped: {skipped_files}")
        print(f"Errors: {errors}")

        if dry_run:
            print("\n🔍 This was a DRY RUN - no files were moved")
            print("\nTo execute:")
            print("  python3 execute_ultimate_reorganization.py --execute")
        else:
            print("\n✅ Reorganization complete!")
            print(f"   Backup: {backup}")
            print("\n📁 New structure created:")
            print(f"   {len(hierarchy)} top-level categories")
            total_subs = sum(
                len(d.get("subcategories", {})) for d in hierarchy.values()
            )
            if total_subs:
                print(f"   {total_subs} subcategories")

        print()

    def execute_flat(self, dry_run: bool = True):
        """Execute flat reorganization (no hierarchy)"""
        mode = "🔍 DRY RUN" if dry_run else "✅ EXECUTING"
        print(f"\n{mode} - FLAT REORGANIZATION")
        print("=" * 70)

        hierarchy = self.analysis["categories"]

        if not dry_run:
            self.create_backup()
            print()

        moved_files = 0

        # Flatten all categories
        for parent, data in hierarchy.items():
            # Create parent directory
            parent_dir = self.base_path / parent

            if not dry_run:
                parent_dir.mkdir(exist_ok=True)

            # Move all files from subcategories into parent
            all_files = set(data.get("files", []))
            for sub_data in data.get("subcategories", {}).values():
                all_files.update(sub_data["files"])

            print(f"📁 {parent}/ ({len(all_files)} files)")

            for filename in all_files:
                if self._move_file(filename, parent_dir, dry_run):
                    moved_files += 1

        print(f"\n✅ Moved {moved_files} files")
        print()

    def _move_file(self, filename: str, dest_dir: Path, dry_run: bool) -> bool:
        """Move a single file"""
        # Find the file
        matches = list(self.base_path.rglob(filename))

        if not matches:
            return False

        source = matches[0]

        # Skip if already in destination
        if source.parent == dest_dir:
            return False

        dest = dest_dir / filename

        # Handle conflicts
        if dest.exists():
            return False

        if not dry_run:
            try:
                shutil.move(str(source), str(dest))
            except Exception as e:
                print(f"  ❌ Error moving {filename}: {e}")
                return False

        return True

    def show_summary(self):
        """Show analysis summary"""
        print("\n📊 ANALYSIS SUMMARY")
        print("=" * 70)

        stats = self.analysis["statistics"]
        print(f"\nTotal files: {stats['total_files']}")
        print(f"Total size: {stats.get('total_size_mb', 0):.2f} MB")

        hierarchy = self.analysis["categories"]
        print(f"\nCategories discovered: {len(hierarchy)}")

        print("\nTop 10 categories:")
        for i, (cat, data) in enumerate(
            sorted(hierarchy.items(), key=lambda x: x[1]["total_files"], reverse=True)[
                :10
            ],
            1,
        ):
            conf = data.get("confidence", 0)
            subs = len(data.get("subcategories", {}))
            sub_text = f" ({subs} subcategories)" if subs else ""
            print(
                f"  {i:2d}. {cat:30s} {data['total_files']:4d} files "
                f"[{conf:3.0f}% confidence]{sub_text}"
            )

        if self.analysis.get("duplicates"):
            print(f"\n⚠️  Duplicates: {len(self.analysis['duplicates'])} groups")

        quality = self.analysis.get("quality", {})
        if quality:
            print(f"\n💎 Quality: {quality.get('average', 0):.0f}/100 average")

        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute ultimate content reorganization"
    )
    parser.add_argument(
        "analysis_file",
        nargs="?",
        help="Analysis JSON file (will auto-detect latest if not specified)",
    )
    parser.add_argument(
        "--directory",
        help="Base directory (will use analysis directory if not specified)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute reorganization (default is dry-run)",
    )
    parser.add_argument(
        "--flat", action="store_true", help="Flat structure (no subcategories)"
    )

    args = parser.parse_args()

    # Find analysis file
    if args.analysis_file:
        analysis_file = Path(args.analysis_file)
    else:
        # Look in current directory
        candidates = sorted(Path.cwd().glob("ultimate_analysis_*.json"), reverse=True)
        if not candidates:
            print("❌ No analysis file found!")
            print("Run ultimate_content_organizer.py first")
            sys.exit(1)
        analysis_file = candidates[0]

    if not analysis_file.exists():
        print(f"❌ Analysis file not found: {analysis_file}")
        sys.exit(1)

    # Determine base directory
    if args.directory:
        base_dir = Path(args.directory)
    else:
        # Load analysis to get directory
        with open(analysis_file, "r") as f:
            data = json.load(f)
        base_dir = Path(data.get("directory", Path.cwd()))

    # Create reorganizer
    reorganizer = UltimateReorganizer(analysis_file, base_dir)

    # Show summary
    reorganizer.show_summary()

    # Execute
    if args.flat:
        reorganizer.execute_flat(dry_run=not args.execute)
    else:
        reorganizer.execute_hierarchical(dry_run=not args.execute)


if __name__ == "__main__":
    main()
