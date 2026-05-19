#!/usr/bin/env python3
"""
🎯 SMART VERSION CONSOLIDATION
Automatically handle version differences based on intelligent analysis

ACTIONS:
1. Root Expanded (8 files) → Replace organized version with root
2. Organized Expanded (4 files) → Delete root version
3. Minor Edits (163 files) → Keep organized, archive root
4. Moderate Changes (72 files) → Manual review needed
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime


class SmartConsolidator:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.report_file = None

        # Find latest report
        reports = sorted(
            self.pythons_dir.glob("VERSION_ANALYSIS_REPORT_*.csv"), reverse=True
        )
        if reports:
            self.report_file = reports[0]

        self.actions = {
            "replace_with_root": [],
            "delete_root": [],
            "archive_root": [],
            "manual_review": [],
        }

    def load_and_categorize(self):
        """Load report and categorize actions"""
        if not self.report_file:
            print("❌ No analysis report found!")
            return False

        print(f"📄 Reading: {self.report_file.name}\n")

        with open(self.report_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                root_lines = int(row["Root Lines"])
                org_lines = int(row["Org Lines"])
                float(row["Root Complexity"])
                float(row["Org Complexity"])

                action = {
                    "filename": row["Filename"],
                    "root_path": self.pythons_dir / row["Filename"],
                    "org_path": None,  # Will be found
                    "parent_folder": row["Parent Folder"],
                    "root_lines": root_lines,
                    "org_lines": org_lines,
                    "reason": "",
                }

                # Find organized path
                org_candidates = list(self.pythons_dir.rglob(row["Filename"]))
                for candidate in org_candidates:
                    if candidate.parent != self.pythons_dir:
                        action["org_path"] = candidate
                        break

                if not action["org_path"]:
                    continue

                # Categorize based on analysis

                # 1. Root is significantly expanded (>1.5x AND >50 lines)
                if root_lines > org_lines * 1.5 and root_lines > 50:
                    action["reason"] = (
                        f"Root is expanded: {root_lines} lines vs {org_lines}"
                    )
                    self.actions["replace_with_root"].append(action)

                # 2. Organized is significantly expanded
                elif org_lines > root_lines * 1.5 and org_lines > 50:
                    action["reason"] = (
                        f"Organized is better: {org_lines} lines vs {root_lines}"
                    )
                    self.actions["delete_root"].append(action)

                # 3. Minor differences (< 10 lines diff)
                elif abs(root_lines - org_lines) < 10:
                    action["reason"] = (
                        f"Minor edit: {abs(root_lines - org_lines)} line difference"
                    )
                    self.actions["archive_root"].append(action)

                # 4. Moderate changes - need review
                else:
                    action["reason"] = (
                        f"Moderate change: Root {root_lines} vs Org {org_lines}"
                    )
                    self.actions["manual_review"].append(action)

        return True

    def print_plan(self):
        """Print consolidation plan"""
        print("=" * 70)
        print("🎯 SMART CONSOLIDATION PLAN")
        print("=" * 70 + "\n")

        total = sum(len(items) for items in self.actions.values())

        print(f"📊 Total files to process: {total}\n")

        for action_type, items in self.actions.items():
            if items:
                print(f"📌 {action_type.upper().replace('_', ' ')}: {len(items)} files")

                # Show examples
                for item in items[:5]:
                    print(f"   • {item['filename']}")
                    print(f"     {item['reason']}")

                if len(items) > 5:
                    print(f"   ... and {len(items) - 5} more")
                print()

    def execute_consolidation(self, dry_run=True):
        """Execute the consolidation"""
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made\n")
        else:
            print("⚠️  EXECUTING CONSOLIDATION\n")

            # Create archive directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dir = (
                self.pythons_dir / "_archive" / f"version-consolidation-{timestamp}"
            )
            archive_dir.mkdir(parents=True, exist_ok=True)
            print(f"📦 Archive directory: {archive_dir}\n")

        stats = {"replaced": 0, "deleted": 0, "archived": 0, "errors": []}

        # 1. Replace organized with root (root is better)
        print("=" * 70)
        print("🔄 REPLACING ORGANIZED VERSIONS WITH ROOT (Root is Expanded)")
        print("=" * 70 + "\n")

        for action in self.actions["replace_with_root"]:
            print(f"  📝 {action['filename']}")
            print(
                f"     Root: {action['root_lines']} lines → {action['parent_folder']}/"
            )
            print("     Replacing organized version...")

            try:
                if not dry_run:
                    # Backup organized version first
                    backup_path = archive_dir / f"org_{action['filename']}"
                    shutil.copy2(action["org_path"], backup_path)

                    # Replace with root version
                    shutil.copy2(action["root_path"], action["org_path"])

                    # Delete root (now copied to organized)
                    action["root_path"].unlink()

                stats["replaced"] += 1
                print("     ✅ Replaced\n")

            except Exception as e:
                stats["errors"].append(f"{action['filename']}: {e}")
                print(f"     ❌ Error: {e}\n")

        # 2. Delete root (organized is better)
        print("=" * 70)
        print("🗑️  DELETING ROOT VERSIONS (Organized is Better)")
        print("=" * 70 + "\n")

        for action in self.actions["delete_root"]:
            print(f"  🗑️  {action['filename']}")
            print(f"     Organized: {action['org_lines']} lines (keeping)")
            print(f"     Root: {action['root_lines']} lines (deleting)")

            try:
                if not dry_run:
                    # Archive root before deleting
                    backup_path = archive_dir / f"root_{action['filename']}"
                    shutil.copy2(action["root_path"], backup_path)

                    # Delete root
                    action["root_path"].unlink()

                stats["deleted"] += 1
                print("     ✅ Deleted\n")

            except Exception as e:
                stats["errors"].append(f"{action['filename']}: {e}")
                print(f"     ❌ Error: {e}\n")

        # 3. Archive root (minor edits)
        print("=" * 70)
        print("📦 ARCHIVING ROOT VERSIONS (Minor Edits)")
        print("=" * 70 + "\n")

        for action in self.actions["archive_root"]:
            print(f"  📦 {action['filename']}")
            print(
                f"     Minor difference: {abs(action['root_lines'] - action['org_lines'])} lines"
            )

            try:
                if not dry_run:
                    # Archive and delete root
                    backup_path = archive_dir / action["filename"]
                    shutil.move(str(action["root_path"]), str(backup_path))

                stats["archived"] += 1

                if stats["archived"] % 20 == 0:
                    print(f"     ... processed {stats['archived']} files")

            except Exception as e:
                stats["errors"].append(f"{action['filename']}: {e}")
                print(f"     ❌ Error: {e}")

        print(f"\n     ✅ Archived {stats['archived']} files\n")

        # Print summary
        print("=" * 70)
        print("📊 CONSOLIDATION SUMMARY")
        print("=" * 70)
        print(f"  🔄 Replaced (root → organized): {stats['replaced']}")
        print(f"  🗑️  Deleted (root removed):       {stats['deleted']}")
        print(f"  📦 Archived (minor edits):      {stats['archived']}")
        print(f"  📋 Manual review needed:        {len(self.actions['manual_review'])}")
        print(f"  ❌ Errors:                      {len(stats['errors'])}")
        print("=" * 70 + "\n")

        if not dry_run:
            print(f"📦 All backups saved to: {archive_dir}")

        return stats

    def save_manual_review_list(self):
        """Save list of files needing manual review"""
        if not self.actions["manual_review"]:
            return None

        review_file = self.pythons_dir / "MANUAL_REVIEW_NEEDED.txt"

        with open(review_file, "w") as f:
            f.write("=" * 70 + "\n")
            f.write("📋 FILES NEEDING MANUAL REVIEW\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total: {len(self.actions['manual_review'])} files\n\n")

            for action in self.actions["manual_review"]:
                f.write(f"• {action['filename']}\n")
                f.write(f"  Root:      {action['root_path']}\n")
                f.write(f"  Organized: {action['org_path']}\n")
                f.write(f"  Reason:    {action['reason']}\n\n")

        print(f"📋 Manual review list saved: {review_file.name}")
        return review_file


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🎯 SMART VERSION CONSOLIDATION                                ║
║     Automatically resolve version conflicts                       ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    consolidator = SmartConsolidator()

    # Load and categorize
    if not consolidator.load_and_categorize():
        return

    # Show plan
    consolidator.print_plan()

    # Execute based on args
    import sys

    if "--execute" in sys.argv:
        print("\n🚨 REAL EXECUTION MODE\n")
        confirm = input("Type 'CONSOLIDATE' to proceed: ")
        if confirm == "CONSOLIDATE":
            consolidator.execute_consolidation(dry_run=False)
            consolidator.save_manual_review_list()
            print("\n✅ Consolidation complete!")
        else:
            print("❌ Cancelled")

    elif "--dry-run" in sys.argv:
        consolidator.execute_consolidation(dry_run=True)
        consolidator.save_manual_review_list()

    else:
        consolidator.save_manual_review_list()
        print("\n🎯 To execute:")
        print("   python3 SMART_VERSION_CONSOLIDATION.py --dry-run      # Preview")
        print("   python3 SMART_VERSION_CONSOLIDATION.py --execute      # Real run")


if __name__ == "__main__":
    main()
