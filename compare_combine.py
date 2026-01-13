#!/usr/bin/env python3
"""
Compare and combine TSV backup file entries.
Deduplicates by URL, keeping the most recent entry (highest timestamp) for each URL.
"""

import sys
from collections import defaultdict
from pathlib import Path


def parse_timestamp(ts_str):
    """Parse timestamp string like 'U1766973555632.994' to float."""
    try:
        return float(ts_str.lstrip('U'))
    except (ValueError, AttributeError):
        return 0.0


def compare_combine_tsv(input_file, output_file=None):
    """
    Compare and combine TSV entries by URL.
    
    Args:
        input_file: Path to input TSV file
        output_file: Path to output TSV file (default: adds '_combined' suffix)
    """
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return
    
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_combined{input_path.suffix}"
    output_path = Path(output_file)
    
    # Read all entries
    entries = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 4:
                print(f"Warning: Line {line_num} has {len(parts)} columns (expected 4), skipping")
                continue
            entries.append({
                'url': parts[0],
                'timestamp': parts[1],
                'value': parts[2],
                'title': parts[3],
                'line_num': line_num
            })
    
    print(f"Read {len(entries)} entries from {input_path.name}")
    
    # Group by URL
    url_groups = defaultdict(list)
    for entry in entries:
        url_groups[entry['url']].append(entry)
    
    print(f"Found {len(url_groups)} unique URLs")
    
    # Find duplicates
    duplicates = {url: items for url, items in url_groups.items() if len(items) > 1}
    if duplicates:
        total_duplicates = sum(len(items) - 1 for items in duplicates.values())
        print(f"Found {len(duplicates)} URLs with duplicates ({total_duplicates} duplicate entries)")
    
    # Combine: keep entry with highest timestamp for each URL
    combined_entries = []
    for url, items in url_groups.items():
        if len(items) == 1:
            # No duplicates, keep as is
            combined_entries.append(items[0])
        else:
            # Multiple entries, keep the one with highest timestamp
            best_entry = max(items, key=lambda e: parse_timestamp(e['timestamp']))
            combined_entries.append(best_entry)
            print(f"  Combined {len(items)} entries for: {url[:80]}...")
            print(f"    Kept entry with timestamp: {best_entry['timestamp']}")
    
    # Sort by timestamp (most recent first)
    combined_entries.sort(key=lambda e: parse_timestamp(e['timestamp']), reverse=True)
    
    # Write combined file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in combined_entries:
            f.write(f"{entry['url']}\t{entry['timestamp']}\t{entry['value']}\t{entry['title']}\n")
    
    print(f"\n✓ Combined file written: {output_path.name}")
    print(f"  Original entries: {len(entries)}")
    print(f"  Combined entries: {len(combined_entries)}")
    print(f"  Removed duplicates: {len(entries) - len(combined_entries)}")
    print(f"  Reduction: {((len(entries) - len(combined_entries)) / len(entries) * 100):.1f}%")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compare_combine.py <input.tsv> [output.tsv]")
        print("\nExample:")
        print("  python compare_combine.py htu_autobackup_20260103_incremental.tsv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    compare_combine_tsv(input_file, output_file)
