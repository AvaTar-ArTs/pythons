#!/usr/bin/env python3
"""
Smart Archive Deduplicator
Intelligently archives backup directories, removing exact duplicates while preserving different versions
"""

import hashlib
import json
import shutil
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def calculate_file_hash(filepath):
    """Calculate SHA256 hash of file content"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.warning(f"Could not hash {filepath}: {e}")
        return None


def scan_directories(base_dirs):
    """
    Scan all directories and catalog files by content hash
    Returns: dict mapping hash -> list of file paths with that hash
    """
    file_hashes = defaultdict(list)
    total_files = 0
    total_size = 0

    for base_dir in base_dirs:
        if not base_dir.exists():
            logger.warning(f"Directory not found: {base_dir}")
            continue

        logger.info(f"Scanning {base_dir}...")
        for filepath in base_dir.rglob("*"):
            if filepath.is_file():
                total_files += 1
                file_size = filepath.stat().st_size
                total_size += file_size

                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    file_hashes[file_hash].append(
                        {
                            "path": filepath,
                            "size": file_size,
                            "relative_path": str(
                                filepath.relative_to(
                                    filepath.parents[
                                        len(filepath.parents)
                                        - len(base_dir.parents)
                                        - 1
                                    ]
                                )
                            ),
                        }
                    )

                if total_files % 100 == 0:
                    logger.info(f"  Processed {total_files} files...")

    logger.info(f"Scanned {total_files} files ({total_size / 1024 / 1024:.2f} MB)")
    return file_hashes, total_files, total_size


def create_deduplicated_archive(file_hashes, output_path, manifest_path):
    """
    Create a ZIP archive with deduplicated files
    """
    unique_files = 0
    duplicate_files = 0
    saved_space = 0
    archive_mapping = {}

    logger.info(f"Creating archive: {output_path}")

    with zipfile.ZipFile(
        output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zipf:
        for file_hash, file_list in file_hashes.items():
            if len(file_list) == 1:
                # Unique file
                file_info = file_list[0]
                arcname = f"unique/{file_info['relative_path']}"
                try:
                    zipf.write(file_info["path"], arcname)
                    unique_files += 1
                    archive_mapping[file_hash] = {
                        "archive_path": arcname,
                        "original_paths": [str(file_info["path"])],
                        "size": file_info["size"],
                        "status": "unique",
                    }
                except Exception as e:
                    logger.warning(f"Could not archive {file_info['path']}: {e}")
            else:
                # Duplicate files - keep one copy and record all locations
                file_info = file_list[0]  # Keep the first one
                arcname = f"deduplicated/{file_hash[:8]}/{file_info['path'].name}"

                try:
                    zipf.write(file_info["path"], arcname)
                    duplicate_files += len(file_list) - 1
                    saved_space += sum(f["size"] for f in file_list[1:])

                    archive_mapping[file_hash] = {
                        "archive_path": arcname,
                        "original_paths": [str(f["path"]) for f in file_list],
                        "size": file_info["size"],
                        "duplicate_count": len(file_list),
                        "status": "deduplicated",
                        "saved_bytes": sum(f["size"] for f in file_list[1:]),
                    }
                    unique_files += 1
                except Exception as e:
                    logger.warning(f"Could not archive {file_info['path']}: {e}")

    # Create manifest
    manifest = {
        "created": datetime.now().isoformat(),
        "statistics": {
            "unique_files": unique_files,
            "duplicate_files": duplicate_files,
            "total_original_files": unique_files + duplicate_files,
            "saved_space_bytes": saved_space,
            "saved_space_mb": saved_space / 1024 / 1024,
        },
        "file_mapping": archive_mapping,
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def main():
    """Main archival process"""
    root = Path(str(Path.home()) + "/documents/python")

    # Directories to archive
    backup_dirs = [root / "_ARCHIVED_BACKUPS_20251101_044505", root / "_backups"]

    # Output paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_archive = root / f"CONSOLIDATED_BACKUPS_{timestamp}.zip"
    manifest_file = root / f"ARCHIVE_MANIFEST_{timestamp}.json"
    summary_file = root / f"ARCHIVE_SUMMARY_{timestamp}.md"

    logger.info("=" * 70)
    logger.info("SMART BACKUP ARCHIVER - DEDUPLICATION MODE")
    logger.info("=" * 70)

    # Step 1: Scan all files
    file_hashes, total_files, total_size = scan_directories(backup_dirs)

    # Step 2: Analyze duplicates
    unique_hashes = sum(1 for files in file_hashes.values() if len(files) == 1)
    duplicate_groups = sum(1 for files in file_hashes.values() if len(files) > 1)
    duplicate_count = sum(
        len(files) - 1 for files in file_hashes.values() if len(files) > 1
    )

    logger.info(f"\nAnalysis:")
    logger.info(f"  Total files: {total_files}")
    logger.info(f"  Unique files: {unique_hashes}")
    logger.info(f"  Duplicate groups: {duplicate_groups}")
    logger.info(f"  Duplicate files: {duplicate_count}")
    logger.info(
        f"  Space savings potential: {sum(sum(f['size'] for f in files[1:]) for files in file_hashes.values() if len(files) > 1) / 1024 / 1024:.2f} MB"
    )

    # Step 3: Create archive
    logger.info("\nCreating deduplicated archive...")
    manifest = create_deduplicated_archive(file_hashes, output_archive, manifest_file)

    # Step 4: Create summary report
    archive_size = output_archive.stat().st_size
    compression_ratio = (1 - archive_size / total_size) * 100 if total_size > 0 else 0

    summary = f"""# Archive Summary Report

**Created:** {manifest['created']}
**Archive:** {output_archive.name}

## Statistics

### Files
- **Total Original Files:** {manifest['statistics']['total_original_files']:,}
- **Unique Files Stored:** {manifest['statistics']['unique_files']:,}
- **Duplicates Removed:** {manifest['statistics']['duplicate_files']:,}

### Space Savings
- **Original Size:** {total_size / 1024 / 1024:.2f} MB
- **Archive Size:** {archive_size / 1024 / 1024:.2f} MB
- **Deduplication Savings:** {manifest['statistics']['saved_space_mb']:.2f} MB
- **Compression Ratio:** {compression_ratio:.1f}%
- **Total Savings:** {(1 - archive_size / (total_size)) * 100:.1f}%

## Archive Structure

```
CONSOLIDATED_BACKUPS_{timestamp}.zip
??? unique/                  # Files with no duplicates
?   ??? [original paths preserved]
??? deduplicated/            # Deduplicated files
    ??? [hash-based organization]
```

## Files Included

**Source Directories:**
- `_ARCHIVED_BACKUPS_20251101_044505/` (~31 MB)
- `_backups/` (~276 KB)

## Top Duplicate Files

"""

    # Find top duplicates
    duplicate_files = [(h, files) for h, files in file_hashes.items() if len(files) > 1]
    duplicate_files.sort(key=lambda x: len(x[1]) * x[1][0]["size"], reverse=True)

    for i, (file_hash, files) in enumerate(duplicate_files[:10], 1):
        saved_mb = (len(files) - 1) * files[0]["size"] / 1024 / 1024
        summary += f"{i}. **{files[0]['path'].name}**\n"
        summary += f"   - Copies: {len(files)}\n"
        summary += f"   - Size each: {files[0]['size'] / 1024:.1f} KB\n"
        summary += f"   - Saved: {saved_mb:.2f} MB\n\n"

    summary += f"""
## Manifest File

Detailed file mapping saved to: `{manifest_file.name}`

This JSON file contains:
- Complete hash-to-file mapping
- All original file locations
- Deduplication statistics

## Restoration

To restore files from this archive:
```bash
# Extract entire archive
unzip {output_archive.name} -d restored_backups/

# Find specific file
cat {manifest_file.name} | jq '.file_mapping[] | select(.original_paths[] | contains("filename"))'
```

## Cleanup Recommendation

Once you've verified the archive:
```bash
# Remove original backup directories
rm -rf _ARCHIVED_BACKUPS_20251101_044505/
rm -rf _backups/
```

**Estimated disk space freed:** {total_size / 1024 / 1024:.2f} MB
"""

    with open(summary_file, "w") as f:
        f.write(summary)

    logger.info("\n" + "=" * 70)
    logger.info("? ARCHIVAL COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Archive created: {output_archive.name}")
    logger.info(f"  Size: {archive_size / 1024 / 1024:.2f} MB")
    logger.info(f"  Files: {manifest['statistics']['unique_files']:,}")
    logger.info(f"  Duplicates removed: {manifest['statistics']['duplicate_files']:,}")
    logger.info(f"  Space saved: {manifest['statistics']['saved_space_mb']:.2f} MB")
    logger.info(f"\nManifest: {manifest_file.name}")
    logger.info(f"Summary: {summary_file.name}")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
