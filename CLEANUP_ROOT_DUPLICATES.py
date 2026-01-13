#!/usr/bin/env python3
"""
🗑️ CLEANUP ROOT DUPLICATES
Remove duplicate files from root that already exist in organized folders
"""

import hashlib
from pathlib import Path
import shutil
from datetime import datetime

class DuplicateRemover:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.duplicates = []
        self.unique = []

    def get_file_hash(self, filepath):
        """Calculate MD5 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def find_duplicates(self):
        """Find root files that exist in subdirectories"""
        print("🔍 Scanning for duplicates...\n")

        # Get all root .py files
        root_files = [f for f in self.pythons_dir.glob('*.py') if f.is_file()]

        # Get all subdirectory .py files
        subdir_files = {}
        for f in self.pythons_dir.rglob('*.py'):
            if f.parent != self.pythons_dir:  # Not in root
                subdir_files[f.name] = f

        print(f"📂 Root files: {len(root_files)}")
        print(f"📁 Organized files: {len(subdir_files)}\n")

        # Check each root file
        for root_file in root_files:
            if root_file.name in subdir_files:
                # Same name exists - check if same content
                organized_file = subdir_files[root_file.name]

                root_hash = self.get_file_hash(root_file)
                org_hash = self.get_file_hash(organized_file)

                if root_hash == org_hash:
                    # Exact duplicate
                    self.duplicates.append({
                        'root': root_file,
                        'organized': organized_file,
                        'hash': root_hash,
                        'size': root_file.stat().st_size
                    })
                else:
                    # Same name, different content
                    print(f"⚠️  DIFFERENT CONTENT: {root_file.name}")
                    print(f"   Root: {root_file}")
                    print(f"   Organized: {organized_file}\n")
                    self.unique.append(root_file)
            else:
                # Unique to root
                self.unique.append(root_file)

        return len(self.duplicates), len(self.unique)

    def print_summary(self):
        """Print summary of findings"""
        print("=" * 70)
        print("📊 DUPLICATE ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"  🗑️  Exact duplicates (can delete): {len(self.duplicates)}")
        print(f"  📌 Unique files (keep in root):    {len(self.unique)}")

        total_size = sum(d['size'] for d in self.duplicates)
        print(f"  💾 Space to recover:               {total_size / (1024*1024):.2f} MB")
        print("=" * 70 + "\n")

    def show_sample_duplicates(self, limit=10):
        """Show sample of duplicates"""
        print(f"📋 Sample duplicates (showing {min(limit, len(self.duplicates))}):\n")

        for dup in self.duplicates[:limit]:
            size_kb = dup['size'] / 1024
            print(f"  🗑️  {dup['root'].name} ({size_kb:.1f} KB)")
            print(f"     Root:      {dup['root']}")
            print(f"     Organized: {dup['organized']}")
            print()

    def delete_duplicates(self, dry_run=True):
        """Delete duplicate files from root"""
        if dry_run:
            print("🔍 DRY RUN - No files will be deleted\n")
        else:
            print("⚠️  DELETING FILES\n")

        deleted = 0
        errors = []

        for dup in self.duplicates:
            try:
                if not dry_run:
                    dup['root'].unlink()
                deleted += 1

                if deleted % 50 == 0:
                    print(f"   ... processed {deleted} files")

            except Exception as e:
                errors.append(f"{dup['root'].name}: {e}")

        print(f"\n✅ {'Would delete' if dry_run else 'Deleted'}: {deleted} files")
        if errors:
            print(f"❌ Errors: {len(errors)}")
            for err in errors[:5]:
                print(f"   - {err}")

        return deleted, errors

    def archive_before_delete(self):
        """Archive root files before deletion"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'root-duplicates-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print(f"📦 Archiving to: {archive_dir.name}\n")

        for dup in self.duplicates:
            try:
                shutil.copy2(dup['root'], archive_dir / dup['root'].name)
            except Exception as e:
                print(f"❌ Failed to archive {dup['root'].name}: {e}")

        print(f"✅ Archived {len(self.duplicates)} files\n")
        return archive_dir


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        🗑️  CLEANUP ROOT DUPLICATES                               ║
║        Remove files that exist in organized folders               ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    remover = DuplicateRemover()

    # Find duplicates
    dup_count, unique_count = remover.find_duplicates()

    # Show summary
    remover.print_summary()
    remover.show_sample_duplicates(15)

    # Execute based on command line
    import sys

    if '--execute' in sys.argv:
        print("🚨 REAL DELETION MODE\n")

        # Archive first
        print("📦 Creating archive first for safety...")
        archive_dir = remover.archive_before_delete()
        print(f"✅ Archive created: {archive_dir}\n")

        confirm = input("Type 'DELETE' to remove duplicates from root: ")
        if confirm == 'DELETE':
            deleted, errors = remover.delete_duplicates(dry_run=False)
            print(f"\n✅ Cleanup complete! Deleted {deleted} duplicate files.")
            print(f"📦 Archive safe at: {archive_dir}")
        else:
            print("❌ Cancelled")

    elif '--dry-run' in sys.argv:
        remover.delete_duplicates(dry_run=True)

    else:
        print("🎯 To execute:")
        print("   python3 CLEANUP_ROOT_DUPLICATES.py --dry-run    # Preview")
        print("   python3 CLEANUP_ROOT_DUPLICATES.py --execute    # Delete (with archive)")


if __name__ == "__main__":
    main()

