#!/usr/bin/env python3
"""
Deep Index Comparator - Compare two directory indexes
Analyzes differences between directory snapshots
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class IndexComparator:
    """Compare two directory indexes and identify differences"""

    def __init__(self, before_index: Dict, after_index: Dict):
        self.before = before_index
        self.after = after_index
        self.before_files = self._extract_files(self.before['tree'])
        self.after_files = self._extract_files(self.after['tree'])

    def _extract_files(self, node: Dict, files: Dict[str, Dict] = None) -> Dict[str, Dict]:
        """Extract all files from tree structure into flat dictionary"""
        if files is None:
            files = {}

        if node.get('type') != 'directory':
            files[node['path']] = node
        else:
            for child in node.get('children', []):
                self._extract_files(child, files)

        return files

    def find_added_files(self) -> List[Dict]:
        """Find files that exist in after but not in before"""
        added = []
        for path, file_info in self.after_files.items():
            if path not in self.before_files:
                added.append(file_info)
        return sorted(added, key=lambda x: x['path'])

    def find_deleted_files(self) -> List[Dict]:
        """Find files that exist in before but not in after"""
        deleted = []
        for path, file_info in self.before_files.items():
            if path not in self.after_files:
                deleted.append(file_info)
        return sorted(deleted, key=lambda x: x['path'])

    def find_modified_files(self) -> List[Tuple[Dict, Dict]]:
        """Find files that changed between before and after"""
        modified = []
        for path in self.before_files:
            if path in self.after_files:
                before_file = self.before_files[path]
                after_file = self.after_files[path]

                # Check for modifications (size or timestamp changes)
                if (before_file.get('size') != after_file.get('size') or
                    before_file.get('modified') != after_file.get('modified')):
                    modified.append((before_file, after_file))

        return sorted(modified, key=lambda x: x[0]['path'])

    def find_renamed_files(self) -> List[Tuple[Dict, Dict]]:
        """Find files that may have been renamed (same size, different path)"""
        renamed = []
        deleted = self.find_deleted_files()
        added = self.find_added_files()

        # Group by size for potential matches
        deleted_by_size = {}
        for file in deleted:
            size = file['size']
            if size not in deleted_by_size:
                deleted_by_size[size] = []
            deleted_by_size[size].append(file)

        for added_file in added:
            size = added_file['size']
            if size in deleted_by_size:
                for deleted_file in deleted_by_size[size]:
                    # If same size and extension, likely a rename/move
                    if added_file.get('extension') == deleted_file.get('extension'):
                        renamed.append((deleted_file, added_file))

        return renamed

    def compare_statistics(self) -> Dict:
        """Compare high-level statistics"""
        before_stats = self.before['statistics']
        after_stats = self.after['statistics']

        return {
            'files': {
                'before': before_stats['total_files'],
                'after': after_stats['total_files'],
                'change': after_stats['total_files'] - before_stats['total_files']
            },
            'directories': {
                'before': before_stats['total_directories'],
                'after': after_stats['total_directories'],
                'change': after_stats['total_directories'] - before_stats['total_directories']
            },
            'size': {
                'before': before_stats['total_size_bytes'],
                'after': after_stats['total_size_bytes'],
                'change': after_stats['total_size_bytes'] - before_stats['total_size_bytes'],
                'before_human': before_stats['total_size_human'],
                'after_human': after_stats['total_size_human'],
                'change_human': self._format_bytes(
                    after_stats['total_size_bytes'] - before_stats['total_size_bytes']
                )
            }
        }

    def generate_report(self) -> Dict:
        """Generate comprehensive comparison report"""
        added = self.find_added_files()
        deleted = self.find_deleted_files()
        modified = self.find_modified_files()
        renamed = self.find_renamed_files()
        stats_comparison = self.compare_statistics()

        # Calculate size changes
        added_size = sum(f['size'] for f in added)
        deleted_size = sum(f['size'] for f in deleted)
        modified_size_change = sum(
            after['size'] - before['size']
            for before, after in modified
        )

        report = {
            'metadata': {
                'compared_at': datetime.now().isoformat(),
                'before_indexed_at': self.before['metadata']['indexed_at'],
                'after_indexed_at': self.after['metadata']['indexed_at'],
                'before_root': self.before['metadata']['root_path'],
                'after_root': self.after['metadata']['root_path']
            },
            'summary': {
                'files_added': len(added),
                'files_deleted': len(deleted),
                'files_modified': len(modified),
                'files_possibly_renamed': len(renamed),
                'size_added': added_size,
                'size_deleted': deleted_size,
                'size_modified_delta': modified_size_change,
                'size_added_human': self._format_bytes(added_size),
                'size_deleted_human': self._format_bytes(deleted_size),
                'size_modified_delta_human': self._format_bytes(modified_size_change),
                'net_change': len(added) - len(deleted),
                'net_size_change': stats_comparison['size']['change'],
                'net_size_change_human': stats_comparison['size']['change_human']
            },
            'statistics_comparison': stats_comparison,
            'changes': {
                'added': added,
                'deleted': deleted,
                'modified': [
                    {
                        'path': before['path'],
                        'before_size': before['size'],
                        'after_size': after['size'],
                        'size_delta': after['size'] - before['size'],
                        'before_modified': before['modified'],
                        'after_modified': after['modified']
                    }
                    for before, after in modified
                ],
                'possibly_renamed': [
                    {
                        'old_path': before['path'],
                        'new_path': after['path'],
                        'size': before['size']
                    }
                    for before, after in renamed
                ]
            }
        }

        return report

    @staticmethod
    def _format_bytes(size: int) -> str:
        """Convert bytes to human readable format"""
        if size < 0:
            return "-" + IndexComparator._format_bytes(-size)

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


def print_comparison_report(report: Dict):
    """Print human-readable comparison report"""
    print("\n" + "=" * 70)
    print("DIRECTORY INDEX COMPARISON REPORT")
    print("=" * 70)

    print(f"\nBefore: {report['metadata']['before_root']}")
    print(f"  Indexed: {report['metadata']['before_indexed_at']}")
    print(f"\nAfter:  {report['metadata']['after_root']}")
    print(f"  Indexed: {report['metadata']['after_indexed_at']}")

    print("\n" + "-" * 70)
    print("SUMMARY")
    print("-" * 70)

    summary = report['summary']
    stats = report['statistics_comparison']

    print(f"\nFile Changes:")
    print(f"  Added:        {summary['files_added']:>6} files  (+{summary['size_added_human']})")
    print(f"  Deleted:      {summary['files_deleted']:>6} files  (-{summary['size_deleted_human']})")
    print(f"  Modified:     {summary['files_modified']:>6} files  ({summary['size_modified_delta_human']})")
    print(f"  Renamed:      {summary['files_possibly_renamed']:>6} files  (estimated)")

    print(f"\nNet Changes:")
    print(f"  Files:        {summary['net_change']:>+7} files")
    print(f"  Size:         {summary['net_size_change_human']:>10}")

    print(f"\nTotal Statistics:")
    print(f"  Files:        {stats['files']['before']:>6} → {stats['files']['after']:>6}")
    print(f"  Directories:  {stats['directories']['before']:>6} → {stats['directories']['after']:>6}")
    print(f"  Size:         {stats['size']['before_human']:>10} → {stats['size']['after_human']:>10}")

    # Show details if not too many changes
    if summary['files_added'] > 0 and summary['files_added'] <= 20:
        print("\n" + "-" * 70)
        print(f"ADDED FILES ({summary['files_added']})")
        print("-" * 70)
        for file in report['changes']['added'][:20]:
            size = IndexComparator._format_bytes(file['size'])
            print(f"  + {file['path']}")
            print(f"    Size: {size}")

    if summary['files_deleted'] > 0 and summary['files_deleted'] <= 20:
        print("\n" + "-" * 70)
        print(f"DELETED FILES ({summary['files_deleted']})")
        print("-" * 70)
        for file in report['changes']['deleted'][:20]:
            size = IndexComparator._format_bytes(file['size'])
            print(f"  - {file['path']}")
            print(f"    Size: {size}")

    if summary['files_modified'] > 0 and summary['files_modified'] <= 20:
        print("\n" + "-" * 70)
        print(f"MODIFIED FILES ({summary['files_modified']})")
        print("-" * 70)
        for mod in report['changes']['modified'][:20]:
            delta = IndexComparator._format_bytes(mod['size_delta'])
            print(f"  ~ {mod['path']}")
            print(f"    Size: {mod['before_size']:,} → {mod['after_size']:,} ({delta})")

    if summary['files_possibly_renamed'] > 0 and summary['files_possibly_renamed'] <= 20:
        print("\n" + "-" * 70)
        print(f"POSSIBLY RENAMED ({summary['files_possibly_renamed']})")
        print("-" * 70)
        for rename in report['changes']['possibly_renamed'][:20]:
            print(f"  {rename['old_path']}")
            print(f"  → {rename['new_path']}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Compare two directory indexes and identify differences',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('before', help='Path to first (before) index JSON file')
    parser.add_argument('after', help='Path to second (after) index JSON file')
    parser.add_argument('-o', '--output', help='Save comparison report as JSON')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Only output JSON, no console report')

    args = parser.parse_args()

    # Load indexes
    try:
        with open(args.before) as f:
            before_index = json.load(f)
    except Exception as e:
        print(f"Error loading before index: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.after) as f:
            after_index = json.load(f)
    except Exception as e:
        print(f"Error loading after index: {e}", file=sys.stderr)
        sys.exit(1)

    # Compare
    comparator = IndexComparator(before_index, after_index)
    report = comparator.generate_report()

    # Output
    if not args.quiet:
        print_comparison_report(report)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Comparison report saved to: {args.output}")


if __name__ == "__main__":
    main()
