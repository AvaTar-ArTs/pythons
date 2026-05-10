import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Auto-run General Cleanup
Automatically runs the general duplicate cleanup without user input
"""

import sys
from pathlib import Path

# Import the SmartDuplicateCleaner
sys.path.append(str(Path(__file__).parent))
from Smart_Duplicate_Cleaner import SmartDuplicateCleaner


def main():
    print("🧹 Auto-running General Duplicate Cleanup")
    print("=" * 50)

    # Run dry run first
    print("\n🔍 STEP 1: DRY RUN...")
    cleaner_dry = SmartDuplicateCleaner("/Users/steven/Documents", dry_run=True)
    dry_results = cleaner_dry.run_cleanup(dry_run=True)

    print("\n📋 DRY RUN RESULTS:")
    print(f"   - {dry_results['files_removed']:,} files would be removed")
    print(f"   - {dry_results['space_saved_gb']:.2f} GB would be saved")

    # Run actual cleanup
    print("\n🚀 STEP 2: LIVE CLEANUP...")
    cleaner_live = SmartDuplicateCleaner("/Users/steven/Documents", dry_run=False)
    live_results = cleaner_live.run_cleanup(dry_run=False)

    print("\n🎉 GENERAL CLEANUP COMPLETE!")
    print(f"   - {live_results['files_removed']:,} files removed")
    print(f"   - {live_results['space_saved_gb']:.2f} GB saved")
    print("   - Backup created in: 00_CLEANUP_BACKUP/")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)