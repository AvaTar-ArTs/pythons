#!/usr/bin/env python3
"""
Batch Rename Processor
Reads batch analysis CSVs and executes approved renames

Usage:
    python PROCESS_BATCH_RENAMES.py <batch_number>
    python PROCESS_BATCH_RENAMES.py 1    # Process batch 1
    python PROCESS_BATCH_RENAMES.py all  # Process all batches
"""

import sys
import csv
import shutil
from pathlib import Path
from datetime import datetime

pythons_dir = Path.home() / "Documents" / "pythons"
analysis_dir = pythons_dir / "_analysis"
library_dir = pythons_dir / "_library"

def process_batch(batch_num):
    """Process a single batch CSV"""

    # Find the batch CSV
    batch_files = list(analysis_dir.glob(f"BATCH_{batch_num:02d}_ANALYSIS_*.csv"))
    if not batch_files:
        print(f"❌ No batch file found for batch {batch_num}")
        return False

    batch_csv = batch_files[0]
    print(f"\n{'='*90}")
    print(f"📊 PROCESSING BATCH {batch_num}: {batch_csv.name}")
    print(f"{'='*90}\n")

    # Read the batch CSV
    with open(batch_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Count actions
    renames = []
    libraries = []
    deletes = []
    keeps = []

    for row in rows:
        action = row['action'].strip().upper()
        filename = row['filename'].strip()
        suggested_name = row['suggested_name'].strip()

        if action == 'RENAME' and suggested_name:
            renames.append((filename, suggested_name))
        elif action == 'LIBRARY':
            libraries.append(filename)
        elif action == 'DELETE':
            deletes.append(filename)
        elif action == 'KEEP':
            keeps.append(filename)

    if not (renames or libraries or deletes):
        print("⚠️  No actions specified in this batch. Skipping.")
        return False

    # Show summary
    print(f"📝 Summary:")
    print(f"   ✏️  Rename: {len(renames)} files")
    print(f"   📦 Library: {len(libraries)} files")
    print(f"   🗑️  Delete: {len(deletes)} files")
    print(f"   ✅ Keep: {len(keeps)} files")
    print()

    # Ask for confirmation
    response = input("Continue with these changes? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled.")
        return False

    print()

    # Execute renames
    if renames:
        print("🔄 RENAMING FILES:")
        print("-" * 90)
        for old, new in renames:
            old_path = pythons_dir / old
            new_path = pythons_dir / new

            if old_path.exists():
                if new_path.exists():
                    print(f"⚠️  {old:45s} → {new} (target exists)")
                else:
                    shutil.move(str(old_path), str(new_path))
                    print(f"✅ {old:45s} → {new}")
            else:
                print(f"⚠️  {old:45s} (not found)")
        print()

    # Move to library
    if libraries:
        print("📦 MOVING TO LIBRARY:")
        print("-" * 90)
        for filename in libraries:
            src = pythons_dir / filename
            dst = library_dir / filename

            if src.exists():
                if dst.exists():
                    print(f"⚠️  {filename:45s} (already in library)")
                else:
                    shutil.move(str(src), str(dst))
                    print(f"✅ {filename:45s} → _library/")
            else:
                print(f"⚠️  {filename:45s} (not found)")
        print()

    # Delete files
    if deletes:
        print("🗑️  DELETING FILES:")
        print("-" * 90)
        for filename in deletes:
            file_path = pythons_dir / filename

            if file_path.exists():
                file_path.unlink()
                print(f"✅ Deleted: {filename}")
            else:
                print(f"⚠️  {filename:45s} (not found)")
        print()

    # Create backup log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_csv = analysis_dir / f"EXECUTED_BATCH_{batch_num:02d}_{timestamp}.csv"

    with open(backup_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['action', 'original', 'new', 'status'])
        writer.writeheader()

        for old, new in renames:
            writer.writerow({'action': 'RENAME', 'original': old, 'new': new, 'status': 'completed'})
        for lib in libraries:
            writer.writerow({'action': 'LIBRARY', 'original': lib, 'new': f'_library/{lib}', 'status': 'completed'})
        for del_file in deletes:
            writer.writerow({'action': 'DELETE', 'original': del_file, 'new': '', 'status': 'completed'})

    print(f"💾 Execution log saved: {backup_csv.name}")
    print()

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python PROCESS_BATCH_RENAMES.py <batch_number|all>")
        print("Example: python PROCESS_BATCH_RENAMES.py 1")
        print("         python PROCESS_BATCH_RENAMES.py all")
        sys.exit(1)

    batch_arg = sys.argv[1].lower()

    if batch_arg == 'all':
        # Process all batches
        batch_files = sorted(analysis_dir.glob("BATCH_*_ANALYSIS_*.csv"))
        batch_nums = set()
        for bf in batch_files:
            try:
                num = int(bf.name.split('_')[1])
                batch_nums.add(num)
            except:
                continue

        for batch_num in sorted(batch_nums):
            process_batch(batch_num)
    else:
        try:
            batch_num = int(batch_arg)
            process_batch(batch_num)
        except ValueError:
            print(f"❌ Invalid batch number: {batch_arg}")
            sys.exit(1)

    print("=" * 90)
    print("✅ PROCESSING COMPLETE!")
    print("=" * 90)

if __name__ == "__main__":
    main()
