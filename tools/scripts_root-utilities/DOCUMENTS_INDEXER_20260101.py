#!/usr/bin/env python3
"""
Comprehensive Documents Directory Indexer
Generates detailed inventories, summaries, and analysis reports.

Usage:
    python3 DOCUMENTS_INDEXER_20260101.py [directory]

Features:
    - Full file inventory with metadata
    - File type distribution analysis
    - Directory size summaries
    - Duplicate file detection (by size and name)
    - Large file identification
    - Hidden file detection
    - Timestamped output files

Follows AVATARARTS inventory pattern.
"""
import argparse
import csv
import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class DocumentsIndexer:
    """Comprehensive directory indexing and analysis."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.files_data = []
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'file_type_sizes': defaultdict(int),
            'directories': defaultdict(int),
            'directory_sizes': defaultdict(int),
        }

    def get_file_hash(self, file_path: Path, quick: bool = True) -> str:
        """Generate file hash. Use quick mode for large files (first 1MB)."""
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                if quick and file_path.stat().st_size > 1024 * 1024:
                    # For files > 1MB, hash first 1MB only
                    md5.update(f.read(1024 * 1024))
                else:
                    while chunk := f.read(8192):
                        md5.update(chunk)
            return md5.hexdigest()
        except (PermissionError, OSError):
            return ''

    def get_file_info(self, file_path: Path) -> Dict:
        """Extract comprehensive file information."""
        try:
            stat = file_path.stat()
            relative_path = file_path.relative_to(self.root_dir)

            info = {
                'path': str(file_path),
                'relative_path': str(relative_path),
                'name': file_path.name,
                'stem': file_path.stem,
                'extension': file_path.suffix.lower(),
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'size_gb': round(stat.st_size / (1024 ** 3), 4),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'directory': str(file_path.parent),
                'relative_directory': str(file_path.parent.relative_to(self.root_dir)),
                'depth': len(relative_path.parts) - 1,
                'is_hidden': file_path.name.startswith('.'),
            }

            # Update stats
            self.stats['total_files'] += 1
            self.stats['total_size'] += stat.st_size
            self.stats['file_types'][info['extension']] += 1
            self.stats['file_type_sizes'][info['extension']] += stat.st_size
            self.stats['directories'][info['relative_directory']] += 1
            self.stats['directory_sizes'][info['relative_directory']] += stat.st_size

            return info
        except (PermissionError, OSError) as e:
            return None

    def scan_directory(self) -> None:
        """Scan directory and collect file information."""
        print(f"Scanning {self.root_dir}...")
        print("This may take a few minutes for large directories...")

        file_count = 0
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file():
                info = self.get_file_info(file_path)
                if info:
                    self.files_data.append(info)
                    file_count += 1

                    if file_count % 100 == 0:
                        print(f"  Processed {file_count} files...", end='\r')

        print(f"\nScan complete! Found {len(self.files_data):,} files")

    def generate_inventory_csv(self) -> str:
        """Generate main inventory CSV file."""
        output_file = self.root_dir / f'DOCUMENTS_INVENTORY_{self.timestamp}.csv'

        # Sort by size (largest first)
        sorted_data = sorted(self.files_data, key=lambda x: x['size_bytes'], reverse=True)

        print(f"\nWriting inventory to {output_file.name}...")

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['relative_path', 'name', 'extension', 'size_mb', 'size_gb',
                          'modified', 'created', 'relative_directory', 'depth', 'is_hidden']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for row in sorted_data:
                writer.writerow({k: row.get(k) for k in fieldnames})

        return str(output_file)

    def generate_file_types_csv(self) -> str:
        """Generate file type distribution CSV."""
        output_file = self.root_dir / f'DOCUMENTS_FILE_TYPES_{self.timestamp}.csv'

        print(f"Writing file types analysis to {output_file.name}...")

        # Sort by count (descending)
        sorted_types = sorted(
            self.stats['file_types'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Extension', 'Count', 'Total Size (MB)', 'Total Size (GB)', 'Avg Size (MB)'])

            for ext, count in sorted_types:
                total_size = self.stats['file_type_sizes'][ext]
                avg_size = total_size / count if count > 0 else 0
                writer.writerow([
                    ext or '(no extension)',
                    count,
                    round(total_size / (1024 * 1024), 2),
                    round(total_size / (1024 ** 3), 4),
                    round(avg_size / (1024 * 1024), 2)
                ])

        return str(output_file)

    def generate_directory_summary_csv(self) -> str:
        """Generate directory size summary CSV."""
        output_file = self.root_dir / f'DOCUMENTS_DIRECTORIES_{self.timestamp}.csv'

        print(f"Writing directory summary to {output_file.name}...")

        # Sort by size (descending)
        sorted_dirs = sorted(
            self.stats['directory_sizes'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Directory', 'File Count', 'Total Size (MB)', 'Total Size (GB)'])

            for dir_path, total_size in sorted_dirs:
                file_count = self.stats['directories'][dir_path]
                writer.writerow([
                    dir_path or '(root)',
                    file_count,
                    round(total_size / (1024 * 1024), 2),
                    round(total_size / (1024 ** 3), 4)
                ])

        return str(output_file)

    def find_duplicates(self) -> str:
        """Find potential duplicate files by size and name."""
        output_file = self.root_dir / f'DOCUMENTS_DUPLICATES_{self.timestamp}.csv'

        print(f"Analyzing for duplicates...")

        # Group by size and name
        size_name_groups = defaultdict(list)
        for file_info in self.files_data:
            key = (file_info['size_bytes'], file_info['name'])
            size_name_groups[key].append(file_info)

        # Filter to only groups with duplicates
        duplicates = {k: v for k, v in size_name_groups.items() if len(v) > 1}

        print(f"Writing duplicates analysis to {output_file.name}...")
        print(f"Found {len(duplicates)} sets of potential duplicates")

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Size (MB)', 'Count', 'Paths'])

            for (size, name), files in sorted(duplicates.items(), key=lambda x: x[0][0], reverse=True):
                paths = ' | '.join([f['relative_path'] for f in files])
                writer.writerow([
                    name,
                    round(size / (1024 * 1024), 2),
                    len(files),
                    paths
                ])

        return str(output_file)

    def generate_summary_report(self) -> str:
        """Generate text summary report."""
        output_file = self.root_dir / f'DOCUMENTS_SUMMARY_{self.timestamp}.txt'

        print(f"Writing summary report to {output_file.name}...")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Documents Directory Analysis Summary\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Directory: {self.root_dir}\n\n")

            f.write(f"Overview\n")
            f.write(f"-" * 60 + "\n")
            f.write(f"Total Files: {self.stats['total_files']:,}\n")
            f.write(f"Total Size: {self.stats['total_size'] / (1024 ** 3):.2f} GB\n")
            f.write(f"Unique Directories: {len(self.stats['directories'])}\n\n")

            f.write(f"Top 10 File Types by Count\n")
            f.write(f"-" * 60 + "\n")
            sorted_types = sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True)
            for i, (ext, count) in enumerate(sorted_types[:10], 1):
                size_mb = self.stats['file_type_sizes'][ext] / (1024 * 1024)
                f.write(f"{i:2}. {ext or '(no ext)':15} - {count:6,} files ({size_mb:10.2f} MB)\n")

            f.write(f"\nTop 10 Largest Files\n")
            f.write(f"-" * 60 + "\n")
            sorted_files = sorted(self.files_data, key=lambda x: x['size_bytes'], reverse=True)
            for i, file_info in enumerate(sorted_files[:10], 1):
                f.write(f"{i:2}. {file_info['name']:40} - {file_info['size_mb']:10.2f} MB\n")
                f.write(f"    {file_info['relative_path']}\n")

            f.write(f"\nTop 10 Largest Directories\n")
            f.write(f"-" * 60 + "\n")
            sorted_dirs = sorted(self.stats['directory_sizes'].items(), key=lambda x: x[1], reverse=True)
            for i, (dir_path, size) in enumerate(sorted_dirs[:10], 1):
                count = self.stats['directories'][dir_path]
                size_mb = size / (1024 * 1024)
                f.write(f"{i:2}. {dir_path or '(root)':40}\n")
                f.write(f"    {count:6,} files - {size_mb:10.2f} MB\n")

        return str(output_file)

    def run_full_analysis(self) -> Dict[str, str]:
        """Run complete analysis and generate all reports."""
        print(f"\n{'=' * 60}")
        print(f"Documents Directory Indexer")
        print(f"{'=' * 60}\n")

        # Scan directory
        self.scan_directory()

        # Generate all reports
        reports = {
            'inventory': self.generate_inventory_csv(),
            'file_types': self.generate_file_types_csv(),
            'directories': self.generate_directory_summary_csv(),
            'duplicates': self.find_duplicates(),
            'summary': self.generate_summary_report(),
        }

        print(f"\n{'=' * 60}")
        print(f"Analysis Complete!")
        print(f"{'=' * 60}\n")
        print(f"Generated files:")
        for report_type, file_path in reports.items():
            print(f"  - {Path(file_path).name}")

        print(f"\nTotal files analyzed: {self.stats['total_files']:,}")
        print(f"Total size: {self.stats['total_size'] / (1024 ** 3):.2f} GB")

        return reports


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Comprehensive Documents Directory Indexer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Index current directory
    python3 DOCUMENTS_INDEXER_20260101.py

    # Index specific directory
    python3 DOCUMENTS_INDEXER_20260101.py /path/to/directory

Outputs:
    - DOCUMENTS_INVENTORY_YYYYMMDD_HHMMSS.csv - Full file inventory
    - DOCUMENTS_FILE_TYPES_YYYYMMDD_HHMMSS.csv - File type analysis
    - DOCUMENTS_DIRECTORIES_YYYYMMDD_HHMMSS.csv - Directory summaries
    - DOCUMENTS_DUPLICATES_YYYYMMDD_HHMMSS.csv - Duplicate file analysis
    - DOCUMENTS_SUMMARY_YYYYMMDD_HHMMSS.txt - Text summary report
        """
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='/Users/steven/Documents',
        help='Directory to index (default: /Users/steven/Documents)'
    )

    args = parser.parse_args()

    # Run analysis
    indexer = DocumentsIndexer(args.directory)
    reports = indexer.run_full_analysis()


if __name__ == '__main__':
    main()
