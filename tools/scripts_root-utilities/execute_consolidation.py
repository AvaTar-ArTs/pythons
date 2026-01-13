#!/usr/bin/env python3
"""
Execute Consolidation Based on Deep Dive Analysis
Safely consolidates duplicates and scattered files with full backup and rollback capability.
"""

import csv
import shutil
import tarfile
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ConsolidationExecutor:
    """Execute consolidation with safety features."""
    
    def __init__(self, duplicates_csv: str, workspace_root: str = "/Users/steven/AVATARARTS"):
        """
        Initialize consolidation executor.
        
        Args:
            duplicates_csv: Path to duplicates CSV from deep dive analysis
            workspace_root: Root workspace directory
        """
        self.workspace_root = Path(workspace_root)
        self.duplicates_csv = Path(duplicates_csv)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.workspace_root / f"consolidation_backup_{self.timestamp}"
        self.log_file = self.workspace_root / f"consolidation_log_{self.timestamp}.txt"
        self.deleted_files = []
        self.errors = []
        
    def log(self, message: str):
        """Log message to file and console."""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")
    
    def load_duplicates(self) -> list:
        """Load duplicates from CSV."""
        duplicates = []
        
        if not self.duplicates_csv.exists():
            self.log(f"❌ Duplicates CSV not found: {self.duplicates_csv}")
            return duplicates
        
        with open(self.duplicates_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Action') == 'DELETE':
                    duplicates.append({
                        'filename': row['Filename'],
                        'keep_path': row['Keep Path'],
                        'duplicate_path': row['Duplicate Path'],
                        'size_mb': float(row.get('Size (MB)', 0)),
                        'waste_mb': float(row.get('Waste (MB)', 0))
                    })
        
        return duplicates
    
    def create_backup(self, files_to_backup: list) -> str:
        """Create compressed backup of files to be deleted."""
        if not files_to_backup:
            return None
        
        self.log(f"\n📦 Creating backup of {len(files_to_backup)} files...")
        self.backup_dir.mkdir(exist_ok=True)
        
        backed_up = 0
        for file_info in files_to_backup:
            filepath = self.workspace_root / file_info['duplicate_path']
            
            if not filepath.exists():
                continue
            
            try:
                # Preserve directory structure in backup
                rel_path = filepath.relative_to(self.workspace_root)
                backup_path = self.backup_dir / rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(filepath, backup_path)
                backed_up += 1
                
                if backed_up % 100 == 0:
                    self.log(f"   ... backed up {backed_up}/{len(files_to_backup)} files")
            
            except Exception as e:
                self.errors.append(f"Backup failed for {filepath}: {e}")
        
        # Compress backup
        backup_archive = f"{self.backup_dir}.tar.gz"
        self.log(f"   Compressing backup to {backup_archive}...")
        
        try:
            with tarfile.open(backup_archive, 'w:gz') as tar:
                tar.add(self.backup_dir, arcname=self.backup_dir.name)
            
            # Remove uncompressed backup
            shutil.rmtree(self.backup_dir)
            
            self.log(f"✅ Backup created: {backup_archive} ({backed_up} files)")
            return backup_archive
        
        except Exception as e:
            self.log(f"⚠️  Compression failed: {e}")
            self.log(f"   Backup directory kept at: {self.backup_dir}")
            return str(self.backup_dir)
    
    def execute_consolidation(self, duplicates: list, dry_run: bool = True, max_files: int = None):
        """
        Execute consolidation.
        
        Args:
            duplicates: List of duplicate file info
            dry_run: If True, only show what would be done
            max_files: Maximum number of files to process (for testing)
        """
        mode = "DRY RUN" if dry_run else "EXECUTING"
        self.log(f"\n{'='*70}")
        self.log(f"🗑️  {mode} CONSOLIDATION")
        self.log(f"{'='*70}\n")
        
        if max_files:
            duplicates = duplicates[:max_files]
            self.log(f"⚠️  Processing limited to first {max_files} files for testing\n")
        
        # Group by keep path to show summary
        keep_paths = defaultdict(list)
        for dup in duplicates:
            keep_paths[dup['keep_path']].append(dup)
        
        self.log(f"Files to consolidate: {len(duplicates)}")
        self.log(f"Unique files to keep: {len(keep_paths)}\n")
        
        # Calculate total waste
        total_waste_mb = sum(d['waste_mb'] for d in duplicates)
        total_waste_gb = total_waste_mb / 1024
        self.log(f"Potential space savings: {total_waste_gb:.2f} GB\n")
        
        if not dry_run:
            # Create backup first
            backup_file = self.create_backup(duplicates)
            if backup_file:
                self.log(f"\n✅ Backup secured: {backup_file}\n")
        
        # Delete duplicates
        deleted_count = 0
        skipped_count = 0
        
        for i, dup in enumerate(duplicates, 1):
            filepath = self.workspace_root / dup['duplicate_path']
            
            if not filepath.exists():
                skipped_count += 1
                continue
            
            if dry_run:
                if i <= 20:  # Show first 20
                    self.log(f"   Would delete: {dup['duplicate_path']} ({dup['size_mb']:.2f} MB)")
                elif i == 21:
                    self.log(f"   ... and {len(duplicates) - 20} more files")
            else:
                try:
                    filepath.unlink()
                    self.deleted_files.append(str(filepath))
                    deleted_count += 1
                    
                    if deleted_count % 100 == 0:
                        self.log(f"   Deleted {deleted_count}/{len(duplicates)}...")
                
                except Exception as e:
                    error_msg = f"Error deleting {filepath}: {e}"
                    self.errors.append(error_msg)
                    self.log(f"   ⚠️  {error_msg}")
        
        if not dry_run:
            self.log(f"\n✅ Deleted {deleted_count} duplicate files")
            if skipped_count > 0:
                self.log(f"   ⚠️  Skipped {skipped_count} files (not found)")
        
        return deleted_count
    
    def generate_rollback_script(self, backup_file: str):
        """Generate rollback script."""
        rollback_script = self.workspace_root / f"rollback_consolidation_{self.timestamp}.sh"
        
        with open(rollback_script, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Rollback script for consolidation {self.timestamp}\n\n")
            f.write(f"BACKUP_FILE=\"{backup_file}\"\n\n")
            f.write("if [ ! -f \"$BACKUP_FILE\" ] && [ ! -d \"$BACKUP_FILE\" ]; then\n")
            f.write("  echo \"Error: Backup file/directory not found!\"\n")
            f.write("  exit 1\n")
            f.write("fi\n\n")
            f.write("echo \"🔄 Rolling back consolidation...\"\n")
            
            if backup_file.endswith('.tar.gz'):
                f.write("tar -xzf \"$BACKUP_FILE\"\n")
                f.write(f"BACKUP_DIR=\"{self.backup_dir.name}\"\n")
                f.write("rsync -av \"$BACKUP_DIR/\" /\n")
                f.write("rm -rf \"$BACKUP_DIR\"\n")
            else:
                f.write("rsync -av \"$BACKUP_FILE/\" /\n")
            
            f.write("echo \"✅ Rollback complete!\"\n")
        
        rollback_script.chmod(0o755)
        self.log(f"\n✅ Rollback script created: {rollback_script}")
        return rollback_script
    
    def generate_report(self, duplicates: list, deleted_count: int, backup_file: str = None):
        """Generate consolidation report."""
        report_file = self.workspace_root / f"CONSOLIDATION_REPORT_{self.timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Consolidation Execution Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Files Processed:** {len(duplicates)}\n")
            f.write(f"- **Files Deleted:** {deleted_count}\n")
            f.write(f"- **Potential Space Savings:** {sum(d['waste_mb'] for d in duplicates) / 1024:.2f} GB\n")
            if backup_file:
                f.write(f"- **Backup:** {backup_file}\n")
            f.write(f"- **Log File:** {self.log_file.name}\n\n")
            
            if self.errors:
                f.write("## Errors\n\n")
                for error in self.errors[:20]:
                    f.write(f"- {error}\n")
                if len(self.errors) > 20:
                    f.write(f"- ... and {len(self.errors) - 20} more errors\n")
                f.write("\n")
            
            f.write("## Top Files Consolidated\n\n")
            # Group by filename
            filename_groups = defaultdict(list)
            for dup in duplicates:
                filename_groups[dup['filename']].append(dup)
            
            sorted_groups = sorted(
                filename_groups.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:30]
            
            for filename, group in sorted_groups:
                f.write(f"### {filename}\n\n")
                f.write(f"- **Duplicates removed:** {len(group)}\n")
                f.write(f"- **Space saved:** {sum(d['waste_mb'] for d in group):.2f} MB\n")
                f.write(f"- **Kept:** `{group[0]['keep_path']}`\n")
                f.write(f"- **Removed locations:**\n")
                for dup in group[:5]:
                    f.write(f"  - `{dup['duplicate_path']}`\n")
                if len(group) > 5:
                    f.write(f"  - ... and {len(group) - 5} more\n")
                f.write("\n")
        
        self.log(f"✅ Report generated: {report_file}")
        return report_file

def main():
    """Main execution."""
    print("\n" + "="*70)
    print("🧹 CONSOLIDATION EXECUTOR")
    print("="*70 + "\n")
    
    workspace_root = "/Users/steven/AVATARARTS"
    
    # Find latest duplicates CSV
    duplicates_files = sorted(
        Path(workspace_root).glob("MULTIFOLDER_DEEPDIVE_*_DUPLICATES.csv"),
        reverse=True
    )
    
    if not duplicates_files:
        print("❌ No duplicates CSV found!")
        print("Run: python3 multifolder_deepdive_consolidate.py first")
        return
    
    duplicates_csv = duplicates_files[0]
    print(f"📄 Using duplicates CSV: {duplicates_csv.name}\n")
    
    # Initialize executor
    executor = ConsolidationExecutor(str(duplicates_csv), workspace_root)
    
    # Load duplicates
    duplicates = executor.load_duplicates()
    
    if not duplicates:
        print("✅ No duplicates to consolidate!")
        return
    
    print(f"📊 Found {len(duplicates):,} duplicate files to remove")
    
    # Calculate summary
    total_waste_gb = sum(d['waste_mb'] for d in duplicates) / 1024
    print(f"💾 Potential space savings: {total_waste_gb:.2f} GB\n")
    
    # Dry run preview
    print("--- DRY RUN PREVIEW (first 100 files) ---")
    executor.execute_consolidation(duplicates, dry_run=True, max_files=100)
    
    # Confirm
    print(f"\n{'='*70}")
    response = input(f"\nProceed with consolidation? This will delete {len(duplicates):,} files. (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Consolidation cancelled")
        return
    
    # Execute (with limit for safety - can be removed)
    print("\n⚠️  Executing with 1000 file limit for safety. Remove limit in code for full consolidation.")
    deleted_count = executor.execute_consolidation(
        duplicates, 
        dry_run=False, 
        max_files=1000  # Safety limit - remove for full consolidation
    )
    
    # Generate rollback script
    backup_file = executor.backup_dir.parent / f"{executor.backup_dir.name}.tar.gz"
    if backup_file.exists():
        executor.generate_rollback_script(str(backup_file))
    
    # Generate report
    executor.generate_report(duplicates[:1000], deleted_count, str(backup_file) if backup_file.exists() else None)
    
    # Final summary
    print(f"\n{'='*70}")
    print("✅ CONSOLIDATION COMPLETE")
    print(f"{'='*70}\n")
    print(f"Deleted: {deleted_count} duplicate files")
    print(f"Log: {executor.log_file}")
    print(f"Report: CONSOLIDATION_REPORT_{executor.timestamp}.md")
    if backup_file.exists():
        print(f"Backup: {backup_file}")
    print()

if __name__ == "__main__":
    main()
