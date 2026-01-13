#!/usr/bin/env python3
"""
Intelligent File Deduplication and Merger
Analyzes markdown files for duplicates based on:
- Exact filename matches (case-insensitive)
- Similar filenames (fuzzy matching)
- Content similarity (hash-based)
- Partial duplicates (same base name with suffixes like _1, _2, etc.)
"""

import os
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import difflib

def normalize_filename(filename: str) -> str:
    """Normalize filename for comparison."""
    name = filename.lower()
    # Remove common suffixes
    name = re.sub(r'[_\s]*\([0-9]+\)$', '', name)  # (1), (2), etc.
    name = re.sub(r'[_\s]*_[0-9]+$', '', name)     # _1, _2, etc.
    name = re.sub(r'[_\s]*copy$', '', name)         # copy
    name = re.sub(r'[_\s]*\d{4}-\d{2}-\d{2}$', '', name)  # dates
    return name.strip()


def get_file_hash(filepath: Path) -> str:
    """Get MD5 hash of file content."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return ""


def get_content_preview(filepath: Path, lines: int = 10) -> str:
    """Get first N lines of file for preview."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return ''.join(f.readlines()[:lines])
    except Exception:
        return ""


def find_duplicates(directory: Path) -> Dict[str, List[Path]]:
    """Find duplicate files based on multiple criteria."""

    # Group by normalized filename
    name_groups = defaultdict(list)
    # Group by content hash
    hash_groups = defaultdict(list)
    # Group by similar names (fuzzy)
    fuzzy_groups = defaultdict(list)

    md_files = list(directory.glob('*.md'))
    print(f"Analyzing {len(md_files)} markdown files...")

    # First pass: group by exact content hash
    for filepath in md_files:
        file_hash = get_file_hash(filepath)
        if file_hash:
            hash_groups[file_hash].append(filepath)

    # Second pass: group by normalized filename
    for filepath in md_files:
        normalized = normalize_filename(filepath.stem)
        name_groups[normalized].append(filepath)

    return {
        'exact_content': {k: v for k, v in hash_groups.items() if len(v) > 1},
        'similar_names': {k: v for k, v in name_groups.items() if len(v) > 1}
    }


def find_similar_filenames(files: List[Path], threshold: float = 0.85) -> List[Tuple[Path, Path, float]]:
    """Find files with similar names using fuzzy matching."""
    similar_pairs = []

    for i, file1 in enumerate(files):
        for file2 in files[i+1:]:
            ratio = difflib.SequenceMatcher(None, file1.stem.lower(), file2.stem.lower()).ratio()
            if ratio >= threshold:
                similar_pairs.append((file1, file2, ratio))

    return similar_pairs


def generate_dedup_report(directory: Path, output_file: Path):
    """Generate comprehensive deduplication report."""

    duplicates = find_duplicates(directory)

    from datetime import datetime

    report_lines = []
    report_lines.append("# File Deduplication Report\n")
    report_lines.append(f"Directory: {directory}\n")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # Section 1: Exact content duplicates
    report_lines.append("## 1. Exact Content Duplicates\n")
    report_lines.append("These files have identical content and can be safely merged:\n\n")

    exact_dupes = duplicates['exact_content']
    if exact_dupes:
        for hash_val, files in exact_dupes.items():
            report_lines.append(f"### Group (hash: {hash_val[:8]}...)\n")
            report_lines.append(f"**Files ({len(files)}):**\n")
            for f in files:
                size = f.stat().st_size
                report_lines.append(f"- `{f.name}` ({size:,} bytes)\n")

            # Recommend keeping the shortest name or most recent
            keeper = min(files, key=lambda x: len(x.name))
            report_lines.append(f"\n**Recommendation:** Keep `{keeper.name}`, delete others\n\n")
    else:
        report_lines.append("No exact content duplicates found.\n\n")

    # Section 2: Similar filenames
    report_lines.append("## 2. Similar Filenames\n")
    report_lines.append("These files have similar names and may be duplicates or versions:\n\n")

    similar_names = duplicates['similar_names']
    if similar_names:
        for normalized, files in list(similar_names.items())[:50]:  # Limit to first 50
            if len(files) > 1:
                report_lines.append(f"### Base: `{normalized}`\n")
                report_lines.append(f"**Variants ({len(files)}):**\n")
                for f in files:
                    size = f.stat().st_size
                    preview = get_content_preview(f, 3).replace('\n', ' ')[:100]
                    report_lines.append(f"- `{f.name}` ({size:,} bytes)\n")
                    report_lines.append(f"  Preview: {preview}...\n")
                report_lines.append("\n")
    else:
        report_lines.append("No similar filenames found.\n\n")

    # Section 3: Pattern-based duplicates
    report_lines.append("## 3. Pattern-Based Duplicates\n")

    # Find files with common patterns
    patterns = {
        'README variants': r'^README[_\s-]*\d*\.md$',
        'Analysis reports': r'.*analysis.*report.*\.md$',
        'Untitled files': r'^Untitled.*\.md$',
        'Numbered copies': r'.*[_\s]\(\d+\)\.md$',
        'Date suffixes': r'.*\d{4}-\d{2}-\d{2}.*\.md$',
    }

    for pattern_name, pattern in patterns.items():
        matches = [f for f in directory.glob('*.md') if re.match(pattern, f.name, re.IGNORECASE)]
        if matches:
            report_lines.append(f"\n### {pattern_name} ({len(matches)} files)\n")
            for f in matches[:20]:  # Limit display
                report_lines.append(f"- `{f.name}`\n")
            if len(matches) > 20:
                report_lines.append(f"... and {len(matches) - 20} more\n")

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(report_lines)

    print(f"\n✓ Report generated: {output_file}")
    return duplicates


def merge_files(files: List[Path], output_path: Path, strategy: str = 'newest'):
    """Merge multiple files into one."""

    if strategy == 'newest':
        # Use the most recently modified file as base
        source = max(files, key=lambda x: x.stat().st_mtime)
    elif strategy == 'largest':
        # Use the largest file as base
        source = max(files, key=lambda x: x.stat().st_size)
    elif strategy == 'shortest_name':
        # Use file with shortest name
        source = min(files, key=lambda x: len(x.name))
    else:
        source = files[0]

    # Copy source to output
    output_path.write_bytes(source.read_bytes())

    return source


def create_merge_plan(duplicates: Dict, directory: Path) -> List[Dict]:
    """Create a merge plan from duplicates."""

    merge_plan = []

    # Plan for exact duplicates
    for hash_val, files in duplicates['exact_content'].items():
        keeper = min(files, key=lambda x: len(x.name))
        to_delete = [f for f in files if f != keeper]

        merge_plan.append({
            'type': 'exact_duplicate',
            'keeper': keeper,
            'delete': to_delete,
            'reason': 'Identical content'
        })

    return merge_plan


def execute_merge_plan(plan: List[Dict], dry_run: bool = True):
    """Execute the merge plan."""

    if dry_run:
        print("\n🔍 DRY RUN - No files will be modified\n")
    else:
        print("\n🔄 Executing merge plan...\n")

    for i, action in enumerate(plan, 1):
        print(f"\n[{i}/{len(plan)}] {action['type']}")
        print(f"  Keep: {action['keeper'].name}")
        print(f"  Delete ({len(action['delete'])} files):")
        for f in action['delete']:
            print(f"    - {f.name}")

        if not dry_run:
            for f in action['delete']:
                try:
                    f.unlink()
                    print(f"      ✓ Deleted {f.name}")
                except Exception as e:
                    print(f"      ✗ Error: {e}")

    if dry_run:
        print("\n⚠️  DRY RUN COMPLETE - Run with --execute to apply changes")
    else:
        print(f"\n✓ Merge complete - Deleted {sum(len(a['delete']) for a in plan)} files")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Deduplicate and merge markdown files')
    parser.add_argument('--directory', type=Path,
                       default=Path('/Users/steven/Documents/markD/ai-ml-notes'),
                       help='Directory to analyze')
    parser.add_argument('--execute', action='store_true',
                       help='Execute deletions (default is dry-run)')
    parser.add_argument('--report-only', action='store_true',
                       help='Only generate report, no merging')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"❌ Directory not found: {args.directory}")
        return 1

    # Generate report
    report_file = args.directory / 'DEDUPLICATION_REPORT.md'
    duplicates = generate_dedup_report(args.directory, report_file)

    if args.report_only:
        print("\n✓ Report-only mode complete")
        return 0

    # Create and execute merge plan
    plan = create_merge_plan(duplicates, args.directory)

    if not plan:
        print("\n✓ No duplicates found to merge!")
        return 0

    execute_merge_plan(plan, dry_run=not args.execute)

    return 0


if __name__ == '__main__':
    exit(main())
