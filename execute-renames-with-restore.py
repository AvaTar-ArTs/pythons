#!/usr/bin/env python3
"""
Execute Renames with CSV Backup & Restore
Creates CSV mapping of old → new names for easy restoration
"""

import csv
import re
from pathlib import Path
from datetime import datetime
import argparse

class RenameExecutor:
    """Execute renames with CSV backup and restore capability"""
    
    def __init__(self, pythons_dir):
        self.pythons_dir = Path(pythons_dir)
        self.renames = []
        
    def load_rename_plan(self, csv_path):
        """Load rename plan CSV"""
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)
        
        # Only actual renames (where name changes)
        self.renames = [
            {
                'old_name': r['current_name'],
                'new_name': r['suggested_name'],
                'reason': r.get('reason', ''),
                'category': r.get('category', '')
            }
            for r in all_rows 
            if r['action'] == 'RENAME' and r['current_name'] != r['suggested_name']
        ]
        
        print(f"✅ Loaded {len(self.renames)} renames")
        return len(self.renames)
    
    def save_backup_csv(self):
        """Save old→new mapping as CSV backup"""
        timestamp = datetime.now().strftime('%Y%m%d')
        backup_path = self.pythons_dir / f'rename_backup_{timestamp}.csv'
        
        with open(backup_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['old_name', 'new_name', 'reason', 'category', 'status'])
            writer.writeheader()
            
            for rename in self.renames:
                writer.writerow({
                    'old_name': rename['old_name'],
                    'new_name': rename['new_name'],
                    'reason': rename['reason'],
                    'category': rename['category'],
                    'status': 'pending'
                })
        
        print(f"💾 Backup CSV created: {backup_path.name}")
        return backup_path
    
    def execute_renames(self, backup_csv):
        """Execute renames and update backup CSV status"""
        print("\n🏷️ Executing renames...")
        print("="*80)
        
        # Read backup CSV
        with open(backup_csv, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        renamed_count = 0
        errors = []
        
        for i, row in enumerate(rows):
            old_path = self.pythons_dir / row['old_name']
            new_path = self.pythons_dir / row['new_name']
            
            if not old_path.exists():
                rows[i]['status'] = 'error: not found'
                errors.append(f"{row['old_name']}: Not found")
                continue
            
            if new_path.exists() and new_path != old_path:
                rows[i]['status'] = 'error: target exists'
                errors.append(f"{row['new_name']}: Already exists")
                continue
            
            try:
                old_path.rename(new_path)
                rows[i]['status'] = 'completed'
                renamed_count += 1
                print(f"   ✓ {row['old_name']}")
                print(f"     → {row['new_name']}")
            except Exception as e:
                rows[i]['status'] = f'error: {str(e)}'
                errors.append(f"{row['old_name']}: {e}")
        
        # Update backup CSV with status
        with open(backup_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['old_name', 'new_name', 'reason', 'category', 'status'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\n✅ Renamed {renamed_count}/{len(rows)} files")
        
        if errors:
            print(f"\n⚠️ Errors ({len(errors)}):")
            for error in errors[:5]:
                print(f"   • {error}")
        
        return renamed_count
    
    def restore_from_backup(self, backup_csv):
        """Restore original names from backup CSV"""
        print("\n↩️  RESTORING FROM BACKUP...")
        print("="*80)
        
        with open(backup_csv, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Only restore completed renames
        to_restore = [r for r in rows if r['status'] == 'completed']
        
        if not to_restore:
            print("❌ No completed renames to restore")
            return 0
        
        restored_count = 0
        
        for row in to_restore:
            # Reverse: new_name → old_name
            current_path = self.pythons_dir / row['new_name']
            original_path = self.pythons_dir / row['old_name']
            
            if not current_path.exists():
                print(f"   ⚠️ Not found: {row['new_name']}")
                continue
            
            try:
                current_path.rename(original_path)
                print(f"   ✓ Restored: {row['new_name']} → {row['old_name']}")
                restored_count += 1
            except Exception as e:
                print(f"   ✗ Error restoring {row['new_name']}: {e}")
        
        print(f"\n✅ Restored {restored_count} files")
        return restored_count
    
    def update_markdown_docs(self, backup_csv):
        """Update all markdown documentation"""
        print("\n📝 Updating markdown documentation...")
        print("="*80)
        
        # Read completed renames
        with open(backup_csv, 'r') as f:
            reader = csv.DictReader(f)
            completed = [r for r in reader if r['status'] == 'completed']
        
        if not completed:
            print("❌ No completed renames to document")
            return
        
        # Find all markdown files
        md_files = list(self.pythons_dir.rglob('*.md'))
        
        total_files_updated = 0
        total_replacements = 0
        
        for rename in completed:
            old_name = rename['old_name']
            new_name = rename['new_name']
            
            files_updated = 0
            
            for md_file in md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Replace patterns
                    patterns = [
                        (f'`{old_name}`', f'`{new_name}`'),
                        (f' {old_name} ', f' {new_name} '),
                        (f'pythons/{old_name}', f'pythons/{new_name}'),
                        (f'from {old_name.replace(".py", "")} import', f'from {new_name.replace(".py", "")} import'),
                        (f'python3 {old_name}', f'python3 {new_name}'),
                        (f'({old_name})', f'({new_name})'),
                    ]
                    
                    for old_pattern, new_pattern in patterns:
                        content = content.replace(old_pattern, new_pattern)
                    
                    if content != original_content:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_updated += 1
                        
                except Exception as e:
                    continue
            
            if files_updated > 0:
                print(f"   ✓ Updated {files_updated} docs for: {old_name}")
                total_files_updated += files_updated
                total_replacements += files_updated
        
        print(f"\n✅ Updated {total_files_updated} total doc references")


def main():
    parser = argparse.ArgumentParser(description='Execute renames with backup/restore')
    parser.add_argument('--csv', default='FINAL_RENAME_PLAN_20251106_134344.csv',
                       help='Rename plan CSV')
    parser.add_argument('--restore', help='Restore from backup CSV')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without executing')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    pythons_dir = Path.home() / 'pythons'
    executor = RenameExecutor(pythons_dir)
    
    # RESTORE mode
    if args.restore:
        backup_csv = pythons_dir / args.restore
        if not backup_csv.exists():
            print(f"❌ Backup CSV not found: {backup_csv}")
            return
        
        confirm = input(f"⚠️  Restore from {args.restore}? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            executor.restore_from_backup(backup_csv)
        return
    
    # RENAME mode
    csv_path = pythons_dir / args.csv
    
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return
    
    count = executor.load_rename_plan(csv_path)
    
    if count == 0:
        print("✅ No renames needed!")
        return
    
    if args.dry_run:
        print("\n🔍 DRY RUN:")
        for r in executor.renames[:20]:
            print(f"   {r['old_name']:40} → {r['new_name']}")
        if len(executor.renames) > 20:
            print(f"\n   ... and {len(executor.renames) - 20} more")
        print(f"\n💡 Run without --dry-run to execute")
        return
    
    # Execute
    print(f"\n⚠️  About to:")
    print(f"   • Rename {count} Python files")
    print(f"   • Update ~20 markdown docs")
    print(f"   • Create CSV backup for restoration")
    
    if not args.yes:
        confirm = input(f"\nContinue? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("❌ Cancelled")
            return
    else:
        print("\n✅ Auto-confirmed with --yes flag")
    
    # Create backup CSV
    backup_csv = executor.save_backup_csv()
    
    # Execute renames
    renamed = executor.execute_renames(backup_csv)
    
    # Update docs
    if renamed > 0:
        executor.update_markdown_docs(backup_csv)
    
    print(f"\n{'='*80}")
    print("✅ COMPLETE!")
    print("="*80)
    print(f"\n💾 Backup CSV: {backup_csv.name}")
    print(f"\n💡 To restore:")
    print(f"   python3 execute-renames-with-restore.py --restore {backup_csv.name}")


if __name__ == '__main__':
    main()
