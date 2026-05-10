#!/usr/bin/env python3
"""
Verify that vault duplicates are actually identical files (not just same size/name).
"""

import os
import hashlib
from pathlib import Path

def get_file_hash(filepath):
    """Get MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (OSError, IOError):
        return None

def verify_duplicates(vault_dir, local_dir, sample_size=10):
    """Verify that size+name matches are actually identical files."""
    print(f"Verifying duplicate files between:")
    print(f"  Vault: {vault_dir}")
    print(f"  Local: {local_dir}")
    print()

    # Get files from both directories
    vault_files = {}
    local_files = {}

    # Build inventory (size, name) -> path
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
    for key in vault_files:
        if key in local_files:
            # Take first match from each
            vault_file = vault_files[key][0]
            local_file = local_files[key][0]
            matches.append((vault_file, local_file))

    print(f"Found {len(matches)} size+name matches")

    if not matches:
        print("No matches to verify")
        return

    # Verify content of first N matches
    verified_duplicates = 0
    verified_different = 0
    errors = 0

    sample = matches[:sample_size] if len(matches) > sample_size else matches

    print(f"\nVerifying content of {len(sample)} sample files:")
    print("-" * 60)

    for vault_file, local_file in sample:
        print(f"\nChecking: {vault_file.name}")

        vault_hash = get_file_hash(vault_file)
        local_hash = get_file_hash(local_file)

        if vault_hash is None or local_hash is None:
            print("  ❌ Error reading file(s)")
            errors += 1
            continue

        if vault_hash == local_hash:
            print("  ✅ IDENTICAL - True duplicate")
            verified_duplicates += 1
        else:
            print("  ❌ DIFFERENT - Same size/name but different content")
            print(f"     Vault hash: {vault_hash}")
            print(f"     Local hash: {local_hash}")
            verified_different += 1

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print(f"  Sample size: {len(sample)}")
    print(f"  True duplicates: {verified_duplicates}")
    print(f"  False duplicates: {verified_different}")
    print(f"  Read errors: {errors}")

    if verified_duplicates > 0 and verified_different == 0:
        print("  ✅ All samples are true duplicates!")
        print(f"  Safe to assume all {len(matches)} matches are duplicates")
    elif verified_different > 0:
        print("  ⚠️  Found false duplicates - need individual verification")
    else:
        print("  ❓ Mixed results - may need more verification")

def main():
    # Check Pictures folder as sample
    vault_pictures = "/Volumes/2T-Xx/HISTORICAL_VAULT_2025/Pictures"
    local_pictures = "/Users/steven/Pictures"

    if os.path.exists(vault_pictures) and os.path.exists(local_pictures):
        verify_duplicates(vault_pictures, local_pictures, sample_size=5)
    else:
        print("Pictures folders not found")

if __name__ == "__main__":
    main()