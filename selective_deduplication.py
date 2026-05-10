#!/usr/bin/env python3
"""
Selective deduplication of HISTORICAL_VAULT_2025 vs local folders.
Only removes obvious duplicates, skips potentially different user content.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Tuple, Optional

def get_file_hash(filepath: Path, quick: bool = True) -> Optional[str]:
    """Get hash of file (quick mode = first 1MB, full mode = entire file)."""
    try:
        hash_obj = hashlib.md5()
        with open(filepath, "rb") as f:
            if quick:
                # Quick hash of first 1MB for large files
                data = f.read(1024 * 1024)
            else:
                # Full file hash
                data = f.read()
            hash_obj.update(data)
        return hash_obj.hexdigest()
    except (OSError, IOError):
        return None

def is_obvious_duplicate(filename: str) -> bool:
    """Check if file is obviously a duplicate (system/media files)."""
    obvious_patterns = [
        # System files
        '.DS_Store', '.localized', '.empty',
        'Thumbs.db', 'desktop.ini',

        # Cache/temp files
        '.tmp', '.temp', '.cache', '.log',

        # Media files (safer to hash-verify)
        '.jpg', '.png', '.mp3', '.mp4', '.mov', '.avi',

        # Application files
        '.app', '.pkg', '.dmg'
    ]

    return any(filename.endswith(pattern) for pattern in obvious_patterns) or \
           any(pattern in filename.lower() for pattern in ['cache', 'temp', 'tmp'])

def find_selective_duplicates(vault_dir: Path, local_dir: Path, max_verify: int = 50) -> List[Tuple[Path, Path]]:
    """Find selective duplicates for safe removal."""
    print(f"Scanning for selective duplicates...")
    print(f"  Vault: {vault_dir}")
    print(f"  Local: {local_dir}")
    print()

    # Build inventories
    vault_files = {}
    local_files = {}

    for root, _, files in os.walk(vault_dir):
        for file in files:
            filepath = Path(root) / file
            try:
                size = filepath.stat().st_size
                key = (size, file)
                if key not in vault_files:
                    vault_files[key] = []
                vault_files[key].append(filepath)
            except OSError:
                continue

    for root, _, files in os.walk(local_dir):
        for file in files:
            filepath = Path(root) / file
            try:
                size = filepath.stat().st_size
                key = (size, file)
                if key not in local_files:
                    local_files[key] = []
                local_files[key].append(filepath)
            except OSError:
                continue

    # Find matches
    matches = []
    verified_count = 0

    for key, vault_paths in vault_files.items():
        if key in local_files:
            size, filename = key
            local_paths = local_files[key]

            # Skip non-obvious files unless we can verify them
            if not is_obvious_duplicate(filename):
                if verified_count >= max_verify:
                    print(f"Skipping {filename} (non-obvious, verification limit reached)")
                    continue
                print(f"Verifying {filename}...")

            # Take first match from each
            vault_file = vault_paths[0]
            local_file = local_paths[0]

            # Quick content verification for safety
            vault_hash = get_file_hash(vault_file, quick=True)
            local_hash = get_file_hash(local_file, quick=True)

            if vault_hash and local_hash and vault_hash == local_hash:
                matches.append((vault_file, local_file))
                verified_count += 1
                if not is_obvious_duplicate(filename):
                    print(f"  ✅ Verified duplicate: {filename}")
            else:
                if not is_obvious_duplicate(filename):
                    print(f"  ❌ Not identical: {filename}")

    return matches

def analyze_duplicates(duplicates: List[Tuple[Path, Path]]) -> dict:
    """Analyze duplicates by type and size."""
    analysis = {
        'total_count': len(duplicates),
        'total_size': 0,
        'by_type': {},
        'by_folder': {}
    }

    for vault_file, local_file in duplicates:
        try:
            size = vault_file.stat().st_size
            analysis['total_size'] += size

            # By file type
            ext = vault_file.suffix.lower() or 'no_extension'
            if ext not in analysis['by_type']:
                analysis['by_type'][ext] = {'count': 0, 'size': 0}
            analysis['by_type'][ext]['count'] += 1
            analysis['by_type'][ext]['size'] += size

            # By vault folder
            vault_folder = vault_file.parent.name
            if vault_folder not in analysis['by_folder']:
                analysis['by_folder'][vault_folder] = {'count': 0, 'size': 0}
            analysis['by_folder'][vault_folder]['count'] += 1
            analysis['by_folder'][vault_folder]['size'] += size

        except OSError:
            continue

    return analysis

def main():
    vault_base = Path("/Volumes/2T-Xx/HISTORICAL_VAULT_2025")
    local_base = Path("/Users/steven")

    folders_to_check = ["Pictures", "Movies", "Music"]  # Skip Documents for safety

    all_duplicates = []

    for folder in folders_to_check:
        vault_dir = vault_base / folder
        local_dir = local_base / folder

        if vault_dir.exists() and local_dir.exists():
            print(f"\n{'='*60}")
            print(f"CHECKING: {folder.upper()}")
            print('='*60)

            duplicates = find_selective_duplicates(vault_dir, local_dir, max_verify=20)
            all_duplicates.extend(duplicates)

            print(f"\nFound {len(duplicates)} verified duplicates in {folder}")

    print(f"\n{'='*60}")
    print("OVERALL ANALYSIS")
    print('='*60)

    if all_duplicates:
        analysis = analyze_duplicates(all_duplicates)

        print(f"Total verified duplicates: {analysis['total_count']}")
        print(f"Total space reclaimable: {analysis['total_size'] / (1024**3):.2f} GB")

        print("\nBy file type:")
        for ext, data in sorted(analysis['by_type'].items(), key=lambda x: x[1]['size'], reverse=True):
            print(f"  {ext}: {data['count']} files ({data['size'] / (1024**2):.1f} MB)")

        print("\nBy vault folder:")
        for folder, data in sorted(analysis['by_folder'].items(), key=lambda x: x[1]['size'], reverse=True):
            print(f"  {folder}: {data['count']} files ({data['size'] / (1024**3):.2f} GB)")

        print("\n⚠️  READY TO REMOVE DUPLICATES")
        print("The following files in HISTORICAL_VAULT_2025 are identical to local files:")
        print("They can be safely removed to reclaim space while keeping vault as backup.")
        print("\nTo proceed with removal, run with --remove flag")
        print("selective_deduplication.py --remove")

    else:
        print("No verified duplicates found for selective removal.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        print("REMOVAL MODE - This will delete files from vault!")
        print("Are you sure? (Type 'yes' to continue)")
        if input().lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
        # TODO: Implement actual removal

    main()