#!/usr/bin/env python3
"""
Merge multiple directories into ~/pythons, identifying and handling duplicates by content hash.
"""

import os
import hashlib
import shutil
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Directories to merge
SOURCE_DIRS = [
    "/Users/steven/.claude-worktrees/pythons",
    "/Users/steven/pythons-merged-backup",
    "/Users/steven/pythons-sort",
]

TARGET_DIR = "/Users/steven/pythons"

# Exclude patterns
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".git",
    ".DS_Store",
    ".history",
    ".vscode",
    "*.pyc",
    ".ipynb_checkpoints",
]


def get_file_hash(filepath):
    """Calculate SHA256 hash of file content."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (IOError, OSError) as e:
        print(f"Error reading {filepath}: {e}")
        return None


def should_exclude(path):
    """Check if path should be excluded."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False


def scan_directory(directory):
    """Scan directory and return dict mapping relative paths to full paths and hashes."""
    files = {}
    directory = Path(directory).resolve()

    if not directory.exists():
        print(f"Directory does not exist: {directory}")
        return files

    for root, dirs, filenames in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]

        for filename in filenames:
            full_path = Path(root) / filename
            if should_exclude(full_path):
                continue

            try:
                if full_path.is_file():
                    rel_path = full_path.relative_to(directory)
                    file_hash = get_file_hash(full_path)
                    if file_hash:
                        files[str(rel_path)] = {
                            "full_path": str(full_path),
                            "hash": file_hash,
                            "size": full_path.stat().st_size,
                            "source_dir": str(directory),
                        }
            except Exception as e:
                print(f"Error processing {full_path}: {e}")

    return files


def merge_directories():
    """Main function to merge directories."""
    print("🔍 Starting directory merge and deduplication process...")
    print(f"📁 Target directory: {TARGET_DIR}")
    print(f"📂 Source directories: {', '.join(SOURCE_DIRS)}\n")

    # Step 1: Scan all source directories
    all_files = {}
    hash_to_files = defaultdict(list)  # Maps hash to list of file info

    for source_dir in SOURCE_DIRS:
        print(f"📊 Scanning {source_dir}...")
        files = scan_directory(source_dir)
        print(f"   Found {len(files)} files")
        all_files.update(files)

        # Build hash mapping
        for rel_path, file_info in files.items():
            hash_to_files[file_info["hash"]].append(
                {"relative_path": rel_path, "source_dir": source_dir, **file_info}
            )

    print(f"\n📈 Total files found: {len(all_files)}")

    # Step 2: Scan target directory
    print(f"\n📊 Scanning target directory {TARGET_DIR}...")
    target_files = scan_directory(TARGET_DIR)
    target_hashes = {info["hash"] for info in target_files.values()}
    print(f"   Found {len(target_files)} existing files")

    # Step 3: Identify duplicates
    print("\n🔎 Identifying duplicates...")
    duplicates_by_hash = {
        h: files for h, files in hash_to_files.items() if len(files) > 1
    }
    print(
        f"   Found {len(duplicates_by_hash)} duplicate groups (same content, different paths)"
    )

    # Step 4: Identify files to copy
    files_to_copy = []
    conflicts = []

    for source_dir in SOURCE_DIRS:
        source_files = {
            k: v for k, v in all_files.items() if v["source_dir"] == source_dir
        }

        for rel_path, file_info in source_files.items():
            file_hash = file_info["hash"]
            target_path = Path(TARGET_DIR) / rel_path

            # Skip if file already exists in target with same hash
            if file_hash in target_hashes:
                # Check if target has a file with this hash
                target_file_exists = False
                for t_rel_path, t_info in target_files.items():
                    if t_info["hash"] == file_hash:
                        target_file_exists = True
                        break

                if target_file_exists:
                    continue  # Already exists, skip

            # Check if target path exists (potential conflict)
            if target_path.exists():
                target_hash = get_file_hash(target_path)
                if target_hash != file_hash:
                    # Different content, same filename - conflict!
                    conflicts.append(
                        {
                            "source": file_info["full_path"],
                            "target": str(target_path),
                            "source_hash": file_hash,
                            "target_hash": target_hash,
                            "relative_path": rel_path,
                        }
                    )
                    continue

            files_to_copy.append(
                {
                    "source": file_info["full_path"],
                    "target": str(target_path),
                    "hash": file_hash,
                    "relative_path": rel_path,
                    "source_dir": source_dir,
                }
            )

    # Step 5: Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_files_scanned": len(all_files),
        "target_files_existing": len(target_files),
        "duplicate_groups": len(duplicates_by_hash),
        "files_to_copy": len(files_to_copy),
        "conflicts": len(conflicts),
        "duplicates": {},
        "conflict_details": conflicts,
        "files_to_copy_details": files_to_copy,
    }

    # Add duplicate details
    for file_hash, files in list(duplicates_by_hash.items())[:20]:  # Limit to first 20
        report["duplicates"][file_hash] = [
            {"relative_path": f["relative_path"], "source_dir": f["source_dir"]}
            for f in files
        ]

    # Step 6: Save report
    report_path = (
        Path(TARGET_DIR)
        / f"merge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved to: {report_path}")
    print("\n📊 Summary:")
    print(f"   Total files scanned: {len(all_files)}")
    print(
        f"   Files already in target: {len(all_files) - len(files_to_copy) - len(conflicts)}"
    )
    print(f"   Files to copy: {len(files_to_copy)}")
    print(f"   Conflicts (same name, different content): {len(conflicts)}")
    print(f"   Duplicate groups: {len(duplicates_by_hash)}")

    # Step 7: Handle conflicts
    if conflicts:
        print(
            f"\n⚠️  Found {len(conflicts)} conflicts (same filename, different content):"
        )
        for conflict in conflicts[:10]:  # Show first 10
            print(f"   {conflict['relative_path']}")
            print(f"      Source: {conflict['source']}")
            print(f"      Target: {conflict['target']}")

        conflict_report_path = (
            Path(TARGET_DIR)
            / f"conflicts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(conflict_report_path, "w") as f:
            f.write("CONFLICTS: Same filename, different content\n")
            f.write("=" * 80 + "\n\n")
            for conflict in conflicts:
                f.write(f"Relative Path: {conflict['relative_path']}\n")
                f.write(f"Source: {conflict['source']}\n")
                f.write(f"Target: {conflict['target']}\n")
                f.write(f"Source Hash: {conflict['source_hash']}\n")
                f.write(f"Target Hash: {conflict['target_hash']}\n")
                f.write("-" * 80 + "\n")
        print(f"   Full conflict report: {conflict_report_path}")

    # Step 8: Copy files
    if files_to_copy:
        print(f"\n📋 Ready to copy {len(files_to_copy)} files.")
        response = input("Proceed with copying? (yes/no): ").strip().lower()

        if response == "yes":
            copied = 0
            errors = 0

            for file_info in files_to_copy:
                source = Path(file_info["source"])
                target = Path(file_info["target"])

                try:
                    # Create parent directory if needed
                    target.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(source, target)
                    copied += 1

                    if copied % 100 == 0:
                        print(f"   Copied {copied}/{len(files_to_copy)} files...")

                except Exception as e:
                    print(f"   Error copying {source} to {target}: {e}")
                    errors += 1

            print("\n✅ Copy complete!")
            print(f"   Copied: {copied}")
            print(f"   Errors: {errors}")
        else:
            print("❌ Copy cancelled by user.")

    return report


if __name__ == "__main__":
    try:
        merge_directories()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
