import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Restore files from a 'restore later' CSV (selective restore manifest).

Reads restore_later.csv written by advanced_consolidation Phase 1.
Restores chosen rows: copy from backup_path back to original_path.
Use --dry-run to print what would be restored without moving files.

Usage:
  python3 restore_consolidation_from_csv.py <restore_later.csv> [--dry-run]
  python3 restore_consolidation_from_csv.py /path/to/consolidation_backup_*/restore_later.csv [--dry-run]
"""

import argparse
import csv
import os
import shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Restore files from restore_later CSV (selective restore)")
    ap.add_argument("csv_path", help="Path to restore_later.csv")
    ap.add_argument("--dry-run", action="store_true", help="Only print what would be restored")
    args = ap.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.is_file():
        print("Error: CSV file not found:", csv_path)
        raise SystemExit(1)

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No rows in CSV. Nothing to restore.")
        return

    for row in rows:
        orig = row.get("original_path", "").strip()
        backup = row.get("backup_path", "").strip()
        if not orig or not backup:
            continue
        if not os.path.exists(backup):
            print("Skip (backup missing):", backup)
            continue
        if args.dry_run:
            print("Would restore:", orig, "<--", backup)
            continue
        parent = Path(orig).parent
        parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, orig)
        print("Restored:", orig)

    if args.dry_run:
        print("Dry run: no files were restored.")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)