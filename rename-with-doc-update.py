#!/usr/bin/env python3
"""
Rename with Documentation Update
Renames Python files AND updates all markdown documentation references
"""

import csv
import re
from pathlib import Path
from datetime import datetime
import shutil

class RenameWithDocUpdate:
    """Rename files and update all documentation"""
    
    def __init__(self, rename_csv):
        self.csv_path = Path(rename_csv)
        self.pythons_dir = Path.home() / 'pythons'
        self.renames = []
        self.md_files = []
        self.updates_made = []
        
    def load_rename_plan(self):
        """Load the final rename plan"""
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)
        
        # Only get RENAME actions where name actually changes
        self.renames = [
            r for r in all_rows 
            if r['action'] == 'RENAME' and r['current_name'] != r['suggested_name']
        ]
        
        print(f"✅ Loaded {len(self.renames)} files to rename")
        return len(self.renames)
    
    def find_all_markdown_files(self):
        """Find all markdown files in ~/pythons"""
        self.md_files = list(self.pythons_dir.rglob('*.md'))
        print(f"✅ Found {len(self.md_files)} markdown files to update")
    
    def update_markdown_file(self, md_file, old_name, new_name):
        """Update a single markdown file"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            updates = 0
            
            # Patterns to replace
            patterns = [
                # In backticks: `AI_ORCHESTRATOR_ULTIMATE.py`
                (f'`{old_name}`', f'`{new_name}`'),
                # Plain text: AI_ORCHESTRATOR_ULTIMATE.py
                (f' {old_name} ', f' {new_name} '),
                (f' {old_name}\n', f' {new_name}\n'),
                (f'\n{old_name} ', f'\n{new_name} '),
                # In paths: ~/pythons/AI_ORCHESTRATOR_ULTIMATE.py
                (f'pythons/{old_name}', f'pythons/{new_name}'),
                # Python imports: from AI_ORCHESTRATOR_ULTIMATE import
                (f'from {old_name.replace(".py", "")} import', f'from {new_name.replace(".py", "")} import'),
                # Python commands: python3 AI_ORCHESTRATOR_ULTIMATE.py
                (f'python3 {old_name}', f'python3 {new_name}'),
                (f'python {old_name}', f'python {new_name}'),
                # In parentheses: (AI_ORCHESTRATOR_ULTIMATE.py)
                (f'({old_name})', f'({new_name})'),
                # File references: **File**: `AI_ORCHESTRATOR_ULTIMATE.py`
                (f'File**: `{old_name}`', f'File**: `{new_name}`'),
                (f'File: `{old_name}`', f'File: `{new_name}`'),
            ]
            
            for old_pattern, new_pattern in patterns:
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    updates += 1
            
            # Save if changes were made
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True, updates
            
            return False, 0
            
        except Exception as e:
            print(f"   ⚠️ Error updating {md_file.name}: {e}")
            return False, 0
    
    def update_all_documentation(self):
        """Update all markdown files with new names"""
        print("\n📝 Updating documentation...")
        print("="*80)
        
        total_files_updated = 0
        total_replacements = 0
        
        for rename in self.renames:
            old_name = rename['current_name']
            new_name = rename['suggested_name']
            
            print(f"\n🔄 Updating references: {old_name} → {new_name}")
            
            files_updated = 0
            
            for md_file in self.md_files:
                was_updated, update_count = self.update_markdown_file(md_file, old_name, new_name)
                
                if was_updated:
                    files_updated += 1
                    total_replacements += update_count
                    print(f"   ✓ Updated {md_file.name} ({update_count} replacements)")
                    
                    self.updates_made.append({
                        'old_name': old_name,
                        'new_name': new_name,
                        'doc_file': str(md_file.relative_to(self.pythons_dir)),
                        'replacements': update_count
                    })
            
            if files_updated == 0:
                print(f"   No markdown references found")
            else:
                total_files_updated += files_updated
        
        print(f"\n{'='*80}")
        print(f"✅ Updated {total_files_updated} markdown files")
        print(f"✅ Made {total_replacements} total replacements")
    
    def rename_python_files(self):
        """Execute the actual file renames"""
        print("\n🏷️ Renaming Python files...")
        print("="*80)
        
        renamed_count = 0
        
        for rename in self.renames:
            old_path = self.pythons_dir / rename['current_name']
            new_path = self.pythons_dir / rename['suggested_name']
            
            if not old_path.exists():
                print(f"   ⚠️ Not found: {rename['current_name']}")
                continue
            
            if new_path.exists():
                print(f"   ⚠️ Target exists: {rename['suggested_name']}")
                continue
            
            try:
                old_path.rename(new_path)
                print(f"   ✓ {rename['current_name']} → {rename['suggested_name']}")
                renamed_count += 1
            except Exception as e:
                print(f"   ✗ Error renaming {rename['current_name']}: {e}")
        
        print(f"\n✅ Renamed {renamed_count} files")
        return renamed_count
    
    def create_backup(self):
        """Create backup before making changes"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.pythons_dir.parent / f'pythons_backup_{timestamp}'
        
        print(f"💾 Creating backup...")
        print(f"   {backup_dir}")
        
        # Only backup markdown files (Python files will be renamed, not deleted)
        backup_docs = backup_dir / 'docs'
        backup_docs.mkdir(parents=True, exist_ok=True)
        
        for md_file in self.md_files:
            rel_path = md_file.relative_to(self.pythons_dir)
            backup_file = backup_docs / rel_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_file, backup_file)
        
        print(f"✅ Backed up {len(self.md_files)} markdown files")
        return backup_dir
    
    def generate_update_report(self):
        """Generate report of all updates made"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.pythons_dir / f'_rename_update_report_{timestamp}.md'
        
        with open(report_path, 'w') as f:
            f.write("# 📝 Rename & Documentation Update Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write(f"## 📊 Summary\n\n")
            f.write(f"- **Python Files Renamed:** {len(self.renames)}\n")
            f.write(f"- **Documentation Files Updated:** {len(set(u['doc_file'] for u in self.updates_made))}\n")
            f.write(f"- **Total Replacements:** {sum(u['replacements'] for u in self.updates_made)}\n\n")
            
            f.write("---\n\n")
            f.write("## 🏷️ Files Renamed\n\n")
            
            for rename in self.renames:
                f.write(f"### {rename['current_name']} → {rename['suggested_name']}\n\n")
                f.write(f"**Reason:** {rename['reason']}\n\n")
                f.write(f"**Category:** {rename['category']}\n\n")
                
                # Show which docs were updated
                docs_updated = [u for u in self.updates_made if u['old_name'] == rename['current_name']]
                if docs_updated:
                    f.write("**Documentation Updated:**\n\n")
                    for doc in docs_updated:
                        f.write(f"- `{doc['doc_file']}` ({doc['replacements']} replacements)\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        return report_path
    
    def execute_full_rename(self):
        """Execute complete rename with documentation update"""
        print("\n🚀 COMPREHENSIVE RENAME WITH DOCUMENTATION UPDATE")
        print("="*80)
        
        # Step 1: Create backup
        backup_dir = self.create_backup()
        
        # Step 2: Update documentation first
        self.find_all_markdown_files()
        self.update_all_documentation()
        
        # Step 3: Rename Python files
        renamed_count = self.rename_python_files()
        
        # Step 4: Generate report
        report_path = self.generate_update_report()
        
        print(f"\n{'='*80}")
        print("✅ COMPLETE!")
        print("="*80)
        print(f"\n📊 Results:")
        print(f"   🏷️ Renamed: {renamed_count} Python files")
        print(f"   📝 Updated: {len(set(u['doc_file'] for u in self.updates_made))} markdown files")
        print(f"   💾 Backup: {backup_dir}")
        print(f"   📄 Report: {report_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Rename files and update documentation')
    parser.add_argument('--csv', default='FINAL_RENAME_PLAN_20251106_134344.csv',
                       help='CSV file with rename plan')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without executing')
    
    args = parser.parse_args()
    
    csv_path = Path.home() / 'pythons' / args.csv
    
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return
    
    renamer = RenameWithDocUpdate(csv_path)
    
    count = renamer.load_rename_plan()
    
    if count == 0:
        print("✅ No renames needed!")
        return
    
    if args.dry_run:
        print("\n🔍 DRY RUN - Showing what would be done:")
        print("="*80)
        for r in renamer.renames[:20]:
            print(f"   {r['current_name']}")
            print(f"   → {r['suggested_name']}")
            print()
        print(f"\n... and {len(renamer.renames) - 20} more")
        print("\n💡 Run without --dry-run to execute")
    else:
        confirm = input(f"\n⚠️  About to rename {count} files and update documentation. Continue? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            renamer.execute_full_rename()
        else:
            print("❌ Cancelled")


if __name__ == '__main__':
    main()
