import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
import csv
import os
import shutil


def restore_from_mapping(mapping_file):
    """Restore files from mapping CSV"""
    if not os.path.exists(mapping_file):
        print(f"Mapping file not found: {mapping_file}")
        return

    restored = 0
    with open(mapping_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            original = row.get("original_location", "")
            consolidated = row.get("consolidated_location", "") or row.get(
                "active_location", ""
            )

            if not original or not consolidated:
                continue

            # Create directory if needed
            os.makedirs(os.path.dirname(consolidated), exist_ok=True)

            # Copy original to consolidated location
            if os.path.exists(original):
                shutil.copy2(original, consolidated)
                print(f"Restored: {consolidated}")
                restored += 1
            else:
                print(f"Warning: Original not found: {original}")

    print(f"\nRestored {restored} files from {mapping_file}")


try:
        import sys
        if len(sys.argv) > 1:
            restore_from_mapping(sys.argv[1])
        else:
            print("Usage: python restore_files.py <mapping_file.csv>")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)