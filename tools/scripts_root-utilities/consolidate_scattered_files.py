#!/usr/bin/env python3
"""
Scattered Files Consolidation
Consolidates exact duplicate files scattered across multiple locations
Keeps one canonical copy, removes others with full backup capability
"""

import csv
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class ScatteredFilesConsolidator:
    """Consolidate scattered files with backup and rollback."""

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(f"scattered_backup_{self.timestamp}")
        self.log_file = f"scattered_consolidation_log_{self.timestamp}.txt"
        self.deleted_files = []

    def log(self, message):
        """Log message to file and console."""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")

    def load_scattered_report(self, report_file):
        """Load scattered files report."""
        scattered_groups = defaultdict(list)

        with open(report_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['category'] == 'exact_duplicates':
                    paths = row['paths'].split(' | ')
                    scattered_groups[row['filename']] = paths

        return scattered_groups

    def determine_canonical_location(self, filename, paths):
        """Determine which copy to keep as canonical."""
        # Priority order for canonical locations:
        # 1. AVATARARTS root (main workspace)
        # 2. GitHub/AvaTarArTs-Suite (production code)
        # 3. pythons/AI_CONTENT (organized content)
        # 4. scripts (utility scripts)
        # 5. Others

        priorities = {
            '/Users/steven/AVATARARTS/': 100,
            '/Users/steven/scripts/': 90,
            '/Users/steven/GitHub/AvaTarArTs-Suite/': 80,
            '/Users/steven/pythons/AI_CONTENT/': 70,
            '/Users/steven/pythons/': 50,
            '/Users/steven/pythons-sort/': 40,
        }

        # Special cases for specific files
        if 'csv_analyzer' in filename or 'batch_csv_analyzer' in filename:
            # CSV tools should be in AVATARARTS root
            for path in paths:
                if path.startswith('/Users/steven/AVATARARTS/') and 'SEO_CONTENT_STRATEGY' not in path:
                    return path

        if 'heavenly_hands' in filename:
            # Production deployment files
            for path in paths:
                if 'avatararts-deployment' in path:
                    return path

        # Default: highest priority location
        scored_paths = []
        for path in paths:
            score = 0
            for prefix, priority in priorities.items():
                if path.startswith(prefix):
                    score = priority
                    # Penalize if in subdirectories (prefer root)
                    depth = len(Path(path).relative_to(prefix).parts)
                    score -= depth * 2
                    break
            scored_paths.append((score, path))

        # Return highest scored path
        return max(scored_paths, key=lambda x: x[0])[1]

    def analyze_consolidation(self, scattered_groups):
        """Analyze what will be consolidated."""
        self.log(f"\n{'='*70}")
        self.log("📊 SCATTERED FILES CONSOLIDATION ANALYSIS")
        self.log(f"{'='*70}\n")

        consolidation_plan = {}

        for filename, paths in scattered_groups.items():
            canonical = self.determine_canonical_location(filename, paths)
            to_delete = [p for p in paths if p != canonical]

            if to_delete:
                consolidation_plan[filename] = {
                    'keep': canonical,
                    'delete': to_delete,
                    'count': len(to_delete)
                }

        # Report
        total_to_delete = sum(plan['count'] for plan in consolidation_plan.values())

        self.log(f"Files to consolidate: {len(consolidation_plan)}")
        self.log(f"Total files to delete: {total_to_delete}\n")

        # Show top items
        self.log("Top consolidation opportunities:\n")
        sorted_items = sorted(consolidation_plan.items(),
                            key=lambda x: x[1]['count'], reverse=True)

        for i, (filename, plan) in enumerate(sorted_items[:15], 1):
            self.log(f"{i:2d}. {filename} - {plan['count']} duplicates")
            self.log(f"    Keep: {Path(plan['keep']).parent.name}/{filename}")
            for path in plan['delete'][:3]:
                self.log(f"    Delete: {Path(path).parent.name}/{filename}")
            if len(plan['delete']) > 3:
                self.log(f"    ... and {len(plan['delete']) - 3} more")
            self.log("")

        return consolidation_plan

    def create_backup(self, files_to_delete):
        """Create compressed backup of files to be deleted."""
        if not files_to_delete:
            return None

        self.log(f"\n📦 Creating backup: {self.backup_dir}.tar.gz")
        self.backup_dir.mkdir(exist_ok=True)

        # Copy files to backup directory
        for filepath in files_to_delete:
            src = Path(filepath)
            if not src.exists():
                continue

            # Preserve directory structure
            rel_path = src.relative_to(src.anchor) if src.is_absolute() else src
            dst = self.backup_dir / rel_path

            dst.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(src, dst)
            except Exception as e:
                self.log(f"   ⚠️  Backup failed for {src}: {e}")

        # Compress backup
        backup_archive = f"{self.backup_dir}.tar.gz"
        with tarfile.open(backup_archive, 'w:gz') as tar:
            tar.add(self.backup_dir, arcname=self.backup_dir.name)

        # Remove uncompressed backup
        shutil.rmtree(self.backup_dir)

        self.log(f"✓ Backup created: {backup_archive}")
        return backup_archive

    def execute_consolidation(self, consolidation_plan, dry_run=False):
        """Execute file consolidation."""
        mode = "DRY RUN" if dry_run else "EXECUTING"
        self.log(f"\n{'='*70}")
        self.log(f"🗑️  {mode} CONSOLIDATION")
        self.log(f"{'='*70}\n")

        all_files_to_delete = []
        for filename, plan in consolidation_plan.items():
            all_files_to_delete.extend(plan['delete'])

        if not dry_run:
            # Create backup first
            backup_file = self.create_backup(all_files_to_delete)
            self.log(f"\n✓ Backup secured: {backup_file}\n")

        # Delete files
        deleted_count = 0
        for i, filepath in enumerate(all_files_to_delete, 1):
            path = Path(filepath)

            if dry_run:
                if i <= 10:  # Show first 10
                    self.log(f"   Would delete: {path}")
                elif i == 11:
                    self.log(f"   ... and {len(all_files_to_delete) - 10} more files")
            else:
                try:
                    if path.exists():
                        path.unlink()
                        self.deleted_files.append(str(path))
                        deleted_count += 1

                        if deleted_count % 20 == 0:
                            self.log(f"   Deleted {deleted_count}/{len(all_files_to_delete)}...")
                except Exception as e:
                    self.log(f"   ⚠️  Error deleting {path}: {e}")

        if not dry_run:
            self.log(f"\n✓ Deleted {deleted_count} duplicate files")

        return deleted_count

    def generate_rollback_script(self):
        """Generate rollback script."""
        rollback_script = f"rollback_scattered_{self.timestamp}.sh"

        with open(rollback_script, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Rollback script for scattered files consolidation {self.timestamp}\n\n")
            f.write(f"BACKUP_FILE=\"{self.backup_dir}.tar.gz\"\n\n")
            f.write("if [ ! -f \"$BACKUP_FILE\" ]; then\n")
            f.write("  echo \"Error: Backup file not found!\"\n")
            f.write("  exit 1\n")
            f.write("fi\n\n")
            f.write("echo \"🔄 Rolling back scattered files consolidation...\"\n")
            f.write("tar -xzf \"$BACKUP_FILE\"\n")
            f.write(f"rsync -av {self.backup_dir}/ /\n")
            f.write(f"rm -rf {self.backup_dir}\n")
            f.write("echo \"✓ Rollback complete!\"\n")

        Path(rollback_script).chmod(0o755)
        self.log(f"\n✓ Rollback script created: {rollback_script}")

    def generate_report(self, consolidation_plan, deleted_count):
        """Generate consolidation report."""
        report_file = f"SCATTERED_CONSOLIDATION_REPORT_{self.timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Scattered Files Consolidation Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Files Consolidated:** {len(consolidation_plan)}\n")
            f.write(f"- **Duplicates Removed:** {deleted_count}\n")
            f.write(f"- **Backup:** {self.backup_dir}.tar.gz\n")
            f.write(f"- **Rollback Script:** rollback_scattered_{self.timestamp}.sh\n\n")

            f.write("## Consolidation Strategy\n\n")
            f.write("**Canonical Location Priority:**\n")
            f.write("1. AVATARARTS root (main workspace)\n")
            f.write("2. scripts/ (utility scripts)\n")
            f.write("3. GitHub/AvaTarArTs-Suite/ (production code)\n")
            f.write("4. pythons/AI_CONTENT/ (organized content)\n")
            f.write("5. Other locations\n\n")

            f.write("## What Was Consolidated\n\n")
            sorted_items = sorted(consolidation_plan.items(),
                                key=lambda x: x[1]['count'], reverse=True)

            for i, (filename, plan) in enumerate(sorted_items[:30], 1):
                f.write(f"### {i}. {filename}\n\n")
                f.write(f"**Canonical location:** `{plan['keep']}`\n\n")
                f.write(f"**Removed {len(plan['delete'])} duplicate(s):**\n")
                for path in plan['delete']:
                    f.write(f"- `{path}`\n")
                f.write("\n---\n\n")

            f.write("## Rollback Instructions\n\n")
            f.write("If you need to undo these changes:\n\n")
            f.write(f"```bash\n./rollback_scattered_{self.timestamp}.sh\n```\n")

        self.log(f"✓ Report generated: {report_file}")
        return report_file


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("🧹 SCATTERED FILES CONSOLIDATION")
    print("="*70 + "\n")

    consolidator = ScatteredFilesConsolidator()

    # Find latest scattered files report
    report_files = sorted(Path('.').glob('SCATTERED_FILES_REPORT_*.csv'), reverse=True)
    if not report_files:
        print("❌ No scattered files report found!")
        print("Run: python3 analyze_scattered_files_detailed.py first")
        return

    report_file = report_files[0]

    # Load report
    scattered_groups = consolidator.load_scattered_report(str(report_file))

    if not scattered_groups:
        print("✅ No scattered files to consolidate!")
        return

    # Analyze
    consolidation_plan = consolidator.analyze_consolidation(scattered_groups)

    if not consolidation_plan:
        print("✅ No files need consolidation!")
        return

    # Dry run preview
    print("\n--- DRY RUN PREVIEW ---")
    consolidator.execute_consolidation(consolidation_plan, dry_run=True)

    # Confirm
    print(f"\n{'='*70}")
    total_to_delete = sum(plan['count'] for plan in consolidation_plan.values())
    response = input(f"\nConsolidate {len(consolidation_plan)} files (delete {total_to_delete} duplicates)? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\n❌ Consolidation cancelled")
        return

    # Execute
    deleted_count = consolidator.execute_consolidation(consolidation_plan, dry_run=False)

    # Generate rollback script
    consolidator.generate_rollback_script()

    # Generate report
    report_file = consolidator.generate_report(consolidation_plan, deleted_count)

    # Final summary
    print(f"\n{'='*70}")
    print("✅ CONSOLIDATION COMPLETE")
    print(f"{'='*70}\n")
    print(f"Consolidated: {len(consolidation_plan)} files")
    print(f"Deleted: {deleted_count} duplicates")
    print(f"\nBackup: {consolidator.backup_dir}.tar.gz")
    print(f"Report: {report_file}")
    print(f"Log: {consolidator.log_file}\n")


if __name__ == "__main__":
    main()
