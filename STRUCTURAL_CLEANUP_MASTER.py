#!/usr/bin/env python3
"""
🔧 STRUCTURAL CLEANUP MASTER
Fix all structural issues: nesting, empty folders, legacy, duplicates
"""

import shutil
from pathlib import Path
from datetime import datetime
import csv

class StructuralCleanup:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.scan_file = None

        # Find latest scan
        scans = sorted(self.pythons_dir.glob('RECURSIVE_FOLDER_SCAN_*.csv'), reverse=True)
        if scans:
            self.scan_file = scans[0]

        self.actions = {
            'flatten': [],
            'delete_empty': [],
            'consolidate_legacy': [],
            'deduplicate': []
        }

    def load_issues(self):
        """Load and categorize issues from scan"""
        if not self.scan_file:
            print("❌ No scan file found!")
            return False

        print(f"📄 Reading: {self.scan_file.name}\n")

        with open(self.scan_file, 'r') as f:
            folders = list(csv.DictReader(f))

        # Process each folder
        for folder in folders:
            depth = int(folder['Depth'])
            path = folder['Folder Path']
            py_files = int(folder['Python Files (Total)'])
            total_files = int(folder['Total Files'])

            # Skip root and depth 1
            if depth <= 1:
                continue

            # Skip _archive (leave it alone)
            if path.startswith('_archive'):
                continue

            # 1. Empty or nearly empty folders (depth 3+)
            if depth >= 3 and total_files <= 2:
                self.actions['delete_empty'].append({
                    'path': path,
                    'depth': depth,
                    'files': total_files,
                    'reason': 'Empty or nearly empty'
                })

            # 2. Deep nesting (depth 6+) with few files
            elif depth >= 6 and py_files < 10:
                self.actions['flatten'].append({
                    'path': path,
                    'depth': depth,
                    'files': py_files,
                    'reason': f'Too deep (depth {depth}) with few files'
                })

            # 3. Legacy folders
            elif any(kw in path.lower() for kw in ['legacy', 'archived', 'backup', 'old']):
                self.actions['consolidate_legacy'].append({
                    'path': path,
                    'depth': depth,
                    'files': py_files,
                    'reason': 'Legacy/archived content'
                })

        return True

    def print_action_plan(self):
        """Print what will be done"""
        print("=" * 70)
        print("🎯 STRUCTURAL CLEANUP ACTION PLAN")
        print("=" * 70 + "\n")

        total = sum(len(items) for items in self.actions.values())
        print(f"Total actions: {total}\n")

        # Empty folders
        if self.actions['delete_empty']:
            print(f"🗑️  DELETE EMPTY/NEARLY EMPTY: {len(self.actions['delete_empty'])} folders")
            for item in self.actions['delete_empty'][:10]:
                print(f"   • {item['path']} (depth {item['depth']}, {item['files']} files)")
            if len(self.actions['delete_empty']) > 10:
                print(f"   ... and {len(self.actions['delete_empty']) - 10} more")
            print()

        # Deep nesting
        if self.actions['flatten']:
            print(f"📂 FLATTEN DEEP NESTING: {len(self.actions['flatten'])} folders")
            for item in self.actions['flatten'][:10]:
                print(f"   • {item['path']} (depth {item['depth']})")
            if len(self.actions['flatten']) > 10:
                print(f"   ... and {len(self.actions['flatten']) - 10} more")
            print()

        # Legacy
        if self.actions['consolidate_legacy']:
            print(f"📦 CONSOLIDATE LEGACY: {len(self.actions['consolidate_legacy'])} folders")
            for item in self.actions['consolidate_legacy'][:10]:
                print(f"   • {item['path']} ({item['files']} files)")
            if len(self.actions['consolidate_legacy']) > 10:
                print(f"   ... and {len(self.actions['consolidate_legacy']) - 10} more")
            print()

    def execute_cleanup(self):
        """Execute the structural cleanup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'structural-cleanup-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("=" * 70)
        print("🔧 EXECUTING STRUCTURAL CLEANUP")
        print("=" * 70)
        print(f"📦 Archive: {archive_dir}\n")

        stats = {'deleted': 0, 'flattened': 0, 'errors': []}

        # 1. Delete empty folders (bottom-up)
        print("🗑️  PHASE 1: Removing empty/nearly empty folders\n")

        empty_sorted = sorted(self.actions['delete_empty'],
                            key=lambda x: x['depth'], reverse=True)

        for item in empty_sorted:
            folder_path = self.pythons_dir / item['path']

            if not folder_path.exists():
                continue

            try:
                # Archive if has any content
                if item['files'] > 0:
                    archive_path = archive_dir / item['path']
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(folder_path), str(archive_path))
                else:
                    # Just delete if truly empty
                    folder_path.rmdir()

                stats['deleted'] += 1

                if stats['deleted'] % 50 == 0:
                    print(f"   ... removed {stats['deleted']} folders")

            except Exception as e:
                stats['errors'].append(f"{item['path']}: {e}")

        print(f"✅ Removed {stats['deleted']} empty/nearly empty folders\n")

        # 2. Flatten deep nesting
        print("📂 PHASE 2: Flattening deep nesting\n")

        for item in self.actions['flatten']:
            folder_path = self.pythons_dir / item['path']

            if not folder_path.exists():
                continue

            try:
                # Move contents up to depth 3 or 4
                parent_parts = folder_path.relative_to(self.pythons_dir).parts
                if len(parent_parts) > 4:
                    # Move to depth 3
                    target_parent = self.pythons_dir / '/'.join(parent_parts[:3])
                    target_parent.mkdir(parents=True, exist_ok=True)

                    # Move all files from deep folder to shallower location
                    for file in folder_path.rglob('*.py'):
                        target_file = target_parent / file.name
                        if not target_file.exists():
                            shutil.move(str(file), str(target_file))
                            stats['flattened'] += 1

            except Exception as e:
                stats['errors'].append(f"{item['path']}: {e}")

        if stats['flattened'] > 0:
            print(f"✅ Flattened {stats['flattened']} files from deep nesting\n")

        # SUMMARY
        print("=" * 70)
        print("📊 STRUCTURAL CLEANUP SUMMARY")
        print("=" * 70)
        print(f"Empty folders removed:  {stats['deleted']}")
        print(f"Files flattened:        {stats['flattened']}")
        print(f"Errors:                 {len(stats['errors'])}")
        print("=" * 70)

        if stats['errors']:
            print("\n⚠️  Errors (first 10):")
            for err in stats['errors'][:10]:
                print(f"  - {err}")

        print(f"\n📦 Archive: {archive_dir}")

        # Final count
        remaining_folders = sum(1 for _ in self.pythons_dir.rglob('*') if _.is_dir())
        print(f"\n🎯 Folders remaining: {remaining_folders}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        🔧 STRUCTURAL CLEANUP MASTER                               ║
║        Fix nesting, empty folders, and structure                 ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    cleanup = StructuralCleanup()

    if not cleanup.load_issues():
        return

    cleanup.print_action_plan()

    confirm = input("\nType 'CLEANUP' to execute: ")

    if confirm == 'CLEANUP':
        cleanup.execute_cleanup()
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

