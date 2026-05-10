import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
AVATARARTS Space Management Plan

Analyzes and provides recommendations for managing the 22GB AVATARARTS directory.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class SpaceManager:
    def __init__(self, avatararts_dir="/Users/steven/AVATARARTS"):
        self.avatararts_dir = Path(avatararts_dir)

    def analyze_space_usage(self):
        """Analyze current space usage."""
        print("🔍 Analyzing AVATARARTS space usage...\n")

        # Get total size
        total_size = sum(f.stat().st_size for f in self.avatararts_dir.rglob('*') if f.is_file())

        # Analyze large items
        large_items = []
        for item in self.avatararts_dir.iterdir():
            if item.is_dir():
                size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                large_items.append((item.name, size, 'directory'))
            elif item.is_file():
                size = item.stat().st_size
                large_items.append((item.name, size, 'file'))

        # Sort by size
        large_items.sort(key=lambda x: x[1], reverse=True)

        return total_size, large_items

    def format_size(self, size_bytes):
        """Format size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def generate_recommendations(self):
        """Generate space management recommendations."""
        total_size, large_items = self.analyze_space_usage()

        print("📊 AVATARARTS Space Analysis")
        print("=" * 50)
        print(f"Total Size: {self.format_size(total_size)}")
        print(f"Location: {self.avatararts_dir}")
        print()

        print("🏆 Top Space Consumers:")
        for name, size, item_type in large_items[:10]:
            print("10s")
        print()

        print("🎯 RECOMMENDED ACTIONS:")
        print()

        # Check for consolidation backup
        consolidation_backup = self.avatararts_dir / "consolidation/scattered/AVATARARTS_BACKUP_PRE_CONSOLIDATION_20260125_143000"
        if consolidation_backup.exists():
            backup_size = sum(f.stat().st_size for f in consolidation_backup.rglob('*') if f.is_file())
            print("1️⃣  REMOVE PRE-CONSOLIDATION BACKUP (SAFE)")
            print("   File: consolidation/scattered/AVATARARTS_BACKUP_PRE_CONSOLIDATION_20260125_143000/")
            print(f"   Size: {self.format_size(backup_size)}")
            print("   Reason: Pre-consolidation backup, consolidation is complete")
            print("   Command: rm -rf consolidation/scattered/AVATARARTS_BACKUP_PRE_CONSOLIDATION_20260125_143000")
            print()

        # Check for tar.gz backup
        tar_backup = self.avatararts_dir / "archives/AVATARARTS.backup.2026-02-03.tar.gz"
        if tar_backup.exists():
            print("2️⃣  REMOVE TAR.GZ BACKUP (OPTIONAL)")
            print(f"   File: archives/AVATARARTS.backup.2026-02-03.tar.gz")
            print(f"   Size: {self.format_size(tar_backup.stat().st_size)}")
            print("   Reason: Compressed backup, keep if you want rollback capability")
            print("   Command: rm archives/AVATARARTS.backup.2026-02-03.tar.gz")
            print()

        # Check for super-flat directory
        super_flat = self.avatararts_dir / "super-flat"
        if super_flat.exists():
            sf_size = sum(f.stat().st_size for f in super_flat.rglob('*') if f.is_file())
            print("3️⃣  EVALUATE SUPER-FLAT DIRECTORY")
            print(f"   Directory: super-flat/")
            print(f"   Size: {self.format_size(sf_size)}")
            print("   Action: Review contents, may be redundant with consolidated structure")
            print()

        # General recommendations
        print("4️⃣  GENERAL SPACE OPTIMIZATION")
        print("   • Consider compressing old project archives")
        print("   • Remove unused development artifacts")
        print("   • Archive completed projects to external storage")
        print("   • Use git for version control instead of multiple backups")
        print()

        print("💾 TARGET SIZE OPTIONS:")
        print(f"   Current: {self.format_size(total_size)}")
        tar_size = tar_backup.stat().st_size if tar_backup.exists() else 0
        reduced_size = total_size - backup_size - tar_size
        print(f"   After removing backups: ~{self.format_size(reduced_size)}")
        print("   Minimal active size: ~2-3GB (core functionality only)")
        print()

        print("⚠️  SAFETY NOTES:")
        print("   • Keep at least one backup until you verify everything works")
        print("   • Test critical scripts after cleanup")
        print("   • Consider external backup for archives before deletion")
        print()

    def execute_safe_cleanup(self):
        """Execute safe cleanup (remove pre-consolidation backup)."""
        print("🧹 Executing safe cleanup...")

        consolidation_backup = self.avatararts_dir / "consolidation/scattered/AVATARARTS_BACKUP_PRE_CONSOLIDATION_20260125_143000"

        if consolidation_backup.exists():
            backup_size = sum(f.stat().st_size for f in consolidation_backup.rglob('*') if f.is_file())
            print(f"Removing: {consolidation_backup}")
            print(f"Size: {self.format_size(backup_size)}")

            response = input("Continue? (y/N): ")
            if response.lower() == 'y':
                shutil.rmtree(consolidation_backup)
                print("✅ Pre-consolidation backup removed successfully!")
                return True
            else:
                print("❌ Operation cancelled")
                return False
        else:
            print("❌ Pre-consolidation backup not found")
            return False

def main():
    manager = SpaceManager()

    print("AVATARARTS Space Management Plan")
    print("Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()

    manager.generate_recommendations()

    print("🚀 EXECUTE SAFE CLEANUP?")
    response = input("Remove pre-consolidation backup? (y/N): ")
    if response.lower() == 'y':
        manager.execute_safe_cleanup()

try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)