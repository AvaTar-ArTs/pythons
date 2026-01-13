#!/usr/bin/env python3
"""
Phase 1 Consolidation - Quick Wins
Safely removes low-risk duplicate files with backup and rollback capability
"""

import csv
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SafeConsolidator:
    """Safe file consolidation with backup and rollback"""

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(f"consolidation_backup_{self.timestamp}")
        self.log_file = f"consolidation_log_{self.timestamp}.txt"
        self.deleted_files = []
        self.stats = defaultdict(int)

    def log(self, message):
        """Log message to file and console"""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")

    def create_backup(self, files_to_delete):
        """Create compressed backup of files to be deleted"""
        if not files_to_delete:
            return None

        self.log(f"\n📦 Creating backup: {self.backup_dir}.tar.gz")
        self.backup_dir.mkdir(exist_ok=True)

        # Copy files to backup directory maintaining structure
        for filepath in files_to_delete:
            src = Path(filepath)
            if not src.exists():
                continue

            # Preserve directory structure
            rel_path = src.relative_to(src.anchor) if src.is_absolute() else src
            dst = self.backup_dir / rel_path

            dst.parent.mkdir(parents=True, exist_ok=True)

            try:
                if src.is_file():
                    shutil.copy2(src, dst)
                elif src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
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

    def analyze_deletions(self, inventory_file):
        """Analyze what will be deleted"""
        self.log(f"\n{'='*70}")
        self.log("📊 PHASE 1 CONSOLIDATION ANALYSIS")
        self.log(f"{'='*70}\n")

        # Load inventory
        files = []
        with open(inventory_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            files = list(reader)

        # Categorize files for deletion
        categories = {
            'venv_files': [],
            'archived_backups': [],
            'timestamped_configs': [],
            'consolidated_dirs': []
        }

        for row in files:
            filepath = Path(row['full_path'])

            # Virtual environment files
            if '/.venv/' in str(filepath) or '/venv/' in str(filepath):
                categories['venv_files'].append(row)

            # Archived backup directories
            elif '/dedup_backup_' in str(filepath) or '08_archived/consolidated' in str(filepath):
                categories['archived_backups'].append(row)

            # Timestamped config files
            elif ('config_202' in row['filename'] or
                  '_202' in row['filename'] and row['filename'].endswith('.py')):
                if 'config' in row['filename'].lower():
                    categories['timestamped_configs'].append(row)

        # Report analysis
        self.log("Files identified for deletion:\n")
        total_files = 0
        total_size_mb = 0

        for category, files_list in categories.items():
            if not files_list:
                continue

            count = len(files_list)
            size_mb = sum(float(f['size_kb']) for f in files_list) / 1024
            total_files += count
            total_size_mb += size_mb

            category_name = category.replace('_', ' ').title()
            self.log(f"  {category_name}:")
            self.log(f"    Files: {count:,}")
            self.log(f"    Size: {size_mb:.2f} MB\n")

        self.log(f"{'─'*70}")
        self.log(f"Total Files: {total_files:,}")
        self.log(f"Total Size: {total_size_mb:.2f} MB")
        self.log(f"{'─'*70}\n")

        return categories, total_files, total_size_mb

    def execute_deletions(self, categories, dry_run=False):
        """Execute file deletions with safety checks"""
        mode = "DRY RUN" if dry_run else "EXECUTING"
        self.log(f"\n{'='*70}")
        self.log(f"🗑️  {mode} DELETIONS")
        self.log(f"{'='*70}\n")

        all_files_to_delete = []
        all_dirs_to_delete = set()

        # Collect all files
        for category, files_list in categories.items():
            for row in files_list:
                filepath = Path(row['full_path'])
                if filepath.exists():
                    all_files_to_delete.append(str(filepath))

                    # Track parent directories for cleanup
                    if 'dedup_backup_' in str(filepath) or 'consolidated' in str(filepath):
                        # Mark entire directory for deletion
                        parent = filepath
                        while parent.parent != parent:
                            if 'dedup_backup_' in parent.name or 'consolidated' in parent.name:
                                all_dirs_to_delete.add(str(parent))
                                break
                            parent = parent.parent

        if not dry_run:
            # Create backup first
            backup_file = self.create_backup(all_files_to_delete + list(all_dirs_to_delete))
            self.log(f"\n✓ Backup secured: {backup_file}\n")

        # Delete files
        deleted_count = 0
        for filepath in all_files_to_delete:
            path = Path(filepath)

            if dry_run:
                if deleted_count < 10:  # Show first 10
                    self.log(f"   Would delete: {path.name}")
                elif deleted_count == 10:
                    self.log(f"   ... and {len(all_files_to_delete) - 10} more files")
            else:
                try:
                    if path.exists() and path.is_file():
                        path.unlink()
                        self.deleted_files.append(str(path))
                        deleted_count += 1

                        if deleted_count % 100 == 0:
                            self.log(f"   Deleted {deleted_count}/{len(all_files_to_delete)}...")
                except Exception as e:
                    self.log(f"   ⚠️  Error deleting {path}: {e}")

        # Delete empty directories
        if not dry_run and all_dirs_to_delete:
            self.log("\n🗂️  Cleaning up directories...")
            for dir_path in sorted(all_dirs_to_delete, key=len, reverse=True):
                path = Path(dir_path)
                try:
                    if path.exists() and path.is_dir():
                        # Only delete if empty or contains only our deleted files
                        if not any(path.rglob('*')):
                            shutil.rmtree(path)
                            self.log(f"   Removed empty directory: {path.name}")
                except Exception as e:
                    self.log(f"   ⚠️  Could not remove {path}: {e}")

        return deleted_count

    def generate_rollback_script(self):
        """Generate rollback script"""
        rollback_script = f"rollback_{self.timestamp}.sh"

        with open(rollback_script, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Rollback script for consolidation {self.timestamp}\n\n")
            f.write(f"BACKUP_FILE=\"{self.backup_dir}.tar.gz\"\n\n")
            f.write("if [ ! -f \"$BACKUP_FILE\" ]; then\n")
            f.write("  echo \"Error: Backup file not found!\"\n")
            f.write("  exit 1\n")
            f.write("fi\n\n")
            f.write("echo \"🔄 Rolling back consolidation...\"\n")
            f.write("tar -xzf \"$BACKUP_FILE\"\n")
            f.write(f"rsync -av {self.backup_dir}/ /\n")
            f.write(f"rm -rf {self.backup_dir}\n")
            f.write("echo \"✓ Rollback complete!\"\n")

        Path(rollback_script).chmod(0o755)
        self.log(f"\n✓ Rollback script created: {rollback_script}")

    def generate_report(self, total_deleted, total_size_mb):
        """Generate final consolidation report"""
        report_file = f"CONSOLIDATION_REPORT_{self.timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Phase 1 Consolidation Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Files Deleted:** {total_deleted:,}\n")
            f.write(f"- **Space Freed:** {total_size_mb:.2f} MB\n")
            f.write(f"- **Backup:** {self.backup_dir}.tar.gz\n")
            f.write(f"- **Rollback Script:** rollback_{self.timestamp}.sh\n\n")
            f.write("## What Was Removed\n\n")
            f.write("1. **Virtual Environment Files** - Regenerable Python packages\n")
            f.write("2. **Archived Backups** - Old dedup_backup_* directories\n")
            f.write("3. **Timestamped Configs** - Duplicate config files with timestamps\n")
            f.write("4. **Consolidated Directories** - Old consolidation attempts\n\n")
            f.write("## Safety\n\n")
            f.write("- ✅ Full backup created before deletion\n")
            f.write("- ✅ Rollback script generated\n")
            f.write("- ✅ Detailed log of all changes\n\n")
            f.write("## Rollback Instructions\n\n")
            f.write("If you need to undo these changes:\n\n")
            f.write(f"```bash\n./rollback_{self.timestamp}.sh\n```\n")

        self.log(f"✓ Report generated: {report_file}")
        return report_file


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("🧹 PHASE 1 CONSOLIDATION - QUICK WINS")
    print("="*70 + "\n")

    consolidator = SafeConsolidator()

    # Find latest inventory
    inventory_files = sorted(Path('.').glob('PYTHON_INVENTORY_*.csv'), reverse=True)
    if not inventory_files:
        print("❌ No inventory file found!")
        return

    inventory_file = inventory_files[0]

    # Analyze
    categories, total_files, total_size_mb = consolidator.analyze_deletions(str(inventory_file))

    if total_files == 0:
        print("✅ No files to delete - workspace is already clean!")
        return

    # Dry run preview
    print("\n--- DRY RUN PREVIEW ---")
    consolidator.execute_deletions(categories, dry_run=True)

    # Confirm
    print(f"\n{'='*70}")
    response = input(f"\nDelete {total_files:,} files ({total_size_mb:.2f} MB)? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\n❌ Consolidation cancelled")
        return

    # Execute
    deleted_count = consolidator.execute_deletions(categories, dry_run=False)

    # Generate rollback script
    consolidator.generate_rollback_script()

    # Generate report
    report_file = consolidator.generate_report(deleted_count, total_size_mb)

    # Final summary
    print(f"\n{'='*70}")
    print("✅ CONSOLIDATION COMPLETE")
    print(f"{'='*70}\n")
    print(f"Deleted: {deleted_count:,} files")
    print(f"Freed: {total_size_mb:.2f} MB")
    print(f"\nBackup: {consolidator.backup_dir}.tar.gz")
    print(f"Report: {report_file}")
    print(f"Log: {consolidator.log_file}\n")


if __name__ == "__main__":
    main()
