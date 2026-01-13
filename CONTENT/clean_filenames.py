#!/usr/bin/env python3
"""
Filename Cleaner for ai-ml-notes Repository
Removes numeric timestamp prefixes and hash suffixes from markdown files
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def clean_filename(filename: str) -> str:
    """
    Clean filename by removing:
    1. Timestamp prefixes (e.g., "12-53-7-", "20251024_")
    2. Hash suffixes (e.g., " 15336221d8b2819d83cbc377de524e32")
    3. Extra underscores and spaces

    Args:
        filename: Original filename (without extension)

    Returns:
        Cleaned filename
    """
    name = filename

    # Pattern 1: Remove timestamp prefixes like "12-53-7-" or "0-15-18-"
    name = re.sub(r'^\d{1,2}-\d{1,2}-\d{1,2}-', '', name)

    # Pattern 2: Remove date prefixes like "20251024_" or "20250909_"
    name = re.sub(r'^\d{8}_', '', name)

    # Pattern 3: Remove hash suffixes (32 hex characters) with optional leading space/underscore
    name = re.sub(r'[\s_][0-9a-f]{32}$', '', name)

    # Pattern 4: Remove "Untitled_" followed by hash
    name = re.sub(r'^Untitled_\d+[a-f0-9]+_', '', name)

    # Clean up extra underscores and spaces
    name = re.sub(r'_+', '_', name)  # Multiple underscores to single
    name = re.sub(r'\s+', ' ', name)  # Multiple spaces to single
    name = name.strip('_- ')  # Remove leading/trailing separators

    return name


def get_rename_operations(directory: Path) -> List[Tuple[Path, Path]]:
    """
    Scan directory and generate list of rename operations.

    Args:
        directory: Path to scan for markdown files

    Returns:
        List of (old_path, new_path) tuples
    """
    operations = []

    for md_file in directory.glob('*.md'):
        # Get filename without extension
        stem = md_file.stem

        # Clean the filename
        new_stem = clean_filename(stem)

        # Skip if no change needed
        if new_stem == stem:
            continue

        # Create new path
        new_path = md_file.parent / f"{new_stem}.md"

        # Handle potential conflicts
        if new_path.exists() and new_path != md_file:
            # Add suffix to avoid overwriting
            counter = 1
            while new_path.exists():
                new_path = md_file.parent / f"{new_stem}_{counter}.md"
                counter += 1

        operations.append((md_file, new_path))

    return operations


def preview_renames(operations: List[Tuple[Path, Path]]) -> None:
    """
    Display preview of rename operations.

    Args:
        operations: List of (old_path, new_path) tuples
    """
    if not operations:
        print("✓ No files need renaming!")
        return

    print(f"\n{'='*80}")
    print(f"RENAME PREVIEW - {len(operations)} files will be renamed:")
    print(f"{'='*80}\n")

    for old_path, new_path in operations:
        print(f"OLD: {old_path.name}")
        print(f"NEW: {new_path.name}")
        print("-" * 80)

    print(f"\nTotal files to rename: {len(operations)}")


def execute_renames(operations: List[Tuple[Path, Path]], dry_run: bool = True) -> None:
    """
    Execute the rename operations.

    Args:
        operations: List of (old_path, new_path) tuples
        dry_run: If True, only preview changes without executing
    """
    if dry_run:
        preview_renames(operations)
        print("\n⚠️  DRY RUN MODE - No files were actually renamed")
        print("Run with --execute flag to apply changes")
        return

    print(f"\n🔄 Renaming {len(operations)} files...\n")

    success_count = 0
    error_count = 0

    for old_path, new_path in operations:
        try:
            old_path.rename(new_path)
            print(f"✓ Renamed: {old_path.name} → {new_path.name}")
            success_count += 1
        except Exception as e:
            print(f"✗ Error renaming {old_path.name}: {e}")
            error_count += 1

    print(f"\n{'='*80}")
    print(f"✓ Successfully renamed: {success_count} files")
    if error_count > 0:
        print(f"✗ Errors: {error_count} files")
    print(f"{'='*80}")


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Clean numeric timestamps and hashes from markdown filenames'
    )
    parser.add_argument(
        '--directory',
        type=Path,
        default=Path('/Users/steven/Documents/markD/ai-ml-notes'),
        help='Directory containing markdown files (default: current directory)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually rename files (default is dry-run mode)'
    )

    args = parser.parse_args()

    # Validate directory
    if not args.directory.exists():
        print(f"❌ Directory not found: {args.directory}")
        return 1

    # Get rename operations
    operations = get_rename_operations(args.directory)

    # Execute or preview
    execute_renames(operations, dry_run=not args.execute)

    return 0


if __name__ == '__main__':
    exit(main())
