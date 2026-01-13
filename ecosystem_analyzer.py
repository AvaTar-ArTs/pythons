#!/usr/bin/env python3
"""
Complete Ecosystem Analyzer
Scans all content repositories and generates comprehensive analysis

Usage:
    python ecosystem_analyzer.py --scan-all
    python ecosystem_analyzer.py --compare-repos
    python ecosystem_analyzer.py --find-duplicates
    python ecosystem_analyzer.py --generate-report
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple
import argparse

class EcosystemAnalyzer:
    """Analyze complete content ecosystem"""

    def __init__(self, base_dir: Path = Path.home()):
        self.base_dir = base_dir
        self.repositories = {
            'pythons': base_dir / 'pythons',
            'pythons-sort': base_dir / 'pythons-sort',
            'pydocs': base_dir / 'pydocs',
            'scripts': base_dir / 'scripts',
            'markd-programming': base_dir / 'Documents' / 'markD' / 'programming',
            'markd-general': base_dir / 'Documents' / 'markD' / 'general-notes',
            'paste-export': base_dir / 'Documents' / 'PasTe-Export'
        }

        self.analysis_dir = base_dir / 'analysis'
        self.analysis_dir.mkdir(exist_ok=True)

        self.results = {}

    def scan_repository(self, name: str, path: Path) -> Dict:
        """Scan a single repository"""
        print(f"📂 Scanning {name}: {path}")

        if not path.exists():
            print(f"  ⚠️  Path does not exist: {path}")
            return {'error': 'Path not found'}

        stats = {
            'name': name,
            'path': str(path),
            'files': [],
            'total_files': 0,
            'total_size': 0,
            'by_extension': defaultdict(int),
            'by_size': {
                'small': 0,    # <10KB
                'medium': 0,   # 10KB-1MB
                'large': 0     # >1MB
            }
        }

        for root, dirs, files in os.walk(path):
            # Skip hidden and cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and
                      d not in ['__pycache__', 'node_modules', 'venv', '.venv']]

            for file in files:
                if file.startswith('.'):
                    continue

                file_path = Path(root) / file
                try:
                    file_stat = file_path.stat()
                    file_size = file_stat.st_size

                    # Get extension
                    ext = file_path.suffix.lower() if file_path.suffix else 'no_ext'

                    # Compute hash for duplicate detection
                    file_hash = self._compute_file_hash(file_path)

                    file_info = {
                        'path': str(file_path),
                        'name': file,
                        'size': file_size,
                        'extension': ext,
                        'hash': file_hash,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    }

                    stats['files'].append(file_info)
                    stats['total_files'] += 1
                    stats['total_size'] += file_size
                    stats['by_extension'][ext] += 1

                    # Size category
                    if file_size < 10 * 1024:
                        stats['by_size']['small'] += 1
                    elif file_size < 1024 * 1024:
                        stats['by_size']['medium'] += 1
                    else:
                        stats['by_size']['large'] += 1

                except (PermissionError, OSError) as e:
                    print(f"  ⚠️  Error accessing {file_path}: {e}")

        print(f"  ✓ Found {stats['total_files']} files ({self._format_size(stats['total_size'])})")
        return stats

    def _compute_file_hash(self, file_path: Path, sample_size: int = 8192) -> str:
        """Compute file hash (first 8KB for speed)"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                hasher.update(f.read(sample_size))
            return hasher.hexdigest()
        except:
            return 'error'

    def _format_size(self, size: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def scan_all_repositories(self) -> Dict:
        """Scan all configured repositories"""
        print("🔍 Scanning all repositories...\n")

        for name, path in self.repositories.items():
            self.results[name] = self.scan_repository(name, path)

        # Save results
        output_file = self.analysis_dir / f'ecosystem_scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Scan complete! Results saved to: {output_file}")
        return self.results

    def find_duplicates(self) -> Dict[str, List[str]]:
        """Find duplicate files across repositories"""
        print("\n🔎 Finding duplicates across repositories...\n")

        hash_map = defaultdict(list)

        # Group files by hash
        for repo_name, repo_data in self.results.items():
            if 'error' in repo_data:
                continue

            for file_info in repo_data['files']:
                if file_info['hash'] != 'error':
                    hash_map[file_info['hash']].append({
                        'repository': repo_name,
                        'path': file_info['path'],
                        'name': file_info['name'],
                        'size': file_info['size']
                    })

        # Filter to only duplicates
        duplicates = {
            hash_val: files
            for hash_val, files in hash_map.items()
            if len(files) > 1
        }

        print(f"Found {len(duplicates)} sets of duplicate files:\n")

        for i, (hash_val, files) in enumerate(list(duplicates.items())[:10], 1):
            print(f"{i}. {files[0]['name']} ({self._format_size(files[0]['size'])})")
            for file in files:
                print(f"   - {file['repository']}: {file['path']}")
            print()

        if len(duplicates) > 10:
            print(f"... and {len(duplicates) - 10} more duplicate sets\n")

        # Save duplicates report
        output_file = self.analysis_dir / 'duplicates_report.json'
        with open(output_file, 'w') as f:
            json.dump(duplicates, f, indent=2)

        print(f"✅ Duplicates report saved to: {output_file}")
        return duplicates

    def compare_repositories(self, repo1: str, repo2: str) -> Dict:
        """Compare two repositories"""
        print(f"\n⚖️  Comparing {repo1} vs {repo2}...\n")

        if repo1 not in self.results or repo2 not in self.results:
            print("❌ One or both repositories not found in scan results")
            return {}

        r1_data = self.results[repo1]
        r2_data = self.results[repo2]

        # Get file sets by hash
        r1_hashes = {f['hash']: f for f in r1_data['files'] if f['hash'] != 'error'}
        r2_hashes = {f['hash']: f for f in r2_data['files'] if f['hash'] != 'error'}

        # Calculate overlaps
        common = set(r1_hashes.keys()) & set(r2_hashes.keys())
        only_r1 = set(r1_hashes.keys()) - set(r2_hashes.keys())
        only_r2 = set(r2_hashes.keys()) - set(r1_hashes.keys())

        comparison = {
            'repo1': {
                'name': repo1,
                'total_files': r1_data['total_files'],
                'unique_files': len(only_r1),
                'unique_file_list': [r1_hashes[h]['name'] for h in list(only_r1)[:20]]
            },
            'repo2': {
                'name': repo2,
                'total_files': r2_data['total_files'],
                'unique_files': len(only_r2),
                'unique_file_list': [r2_hashes[h]['name'] for h in list(only_r2)[:20]]
            },
            'common': {
                'count': len(common),
                'files': [r1_hashes[h]['name'] for h in list(common)[:20]]
            }
        }

        print(f"Repository 1 ({repo1}):")
        print(f"  Total files: {comparison['repo1']['total_files']}")
        print(f"  Unique to r1: {comparison['repo1']['unique_files']}")

        print(f"\nRepository 2 ({repo2}):")
        print(f"  Total files: {comparison['repo2']['total_files']}")
        print(f"  Unique to r2: {comparison['repo2']['unique_files']}")

        print(f"\nCommon files: {comparison['common']['count']}")

        # Save comparison
        output_file = self.analysis_dir / f'comparison_{repo1}_vs_{repo2}.json'
        with open(output_file, 'w') as f:
            json.dump(comparison, f, indent=2)

        print(f"\n✅ Comparison saved to: {output_file}")
        return comparison

    def generate_summary_report(self) -> str:
        """Generate markdown summary report"""
        print("\n📊 Generating summary report...\n")

        report_lines = [
            "# Complete Ecosystem Analysis Report",
            f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n---\n",
            "## Repository Overview\n"
        ]

        total_files = 0
        total_size = 0

        # Repository table
        report_lines.append("| Repository | Files | Size | Top Extensions |")
        report_lines.append("|------------|-------|------|----------------|")

        for repo_name, repo_data in sorted(self.results.items()):
            if 'error' in repo_data:
                report_lines.append(f"| {repo_name} | ERROR | - | - |")
                continue

            files = repo_data['total_files']
            size = repo_data['total_size']
            total_files += files
            total_size += size

            # Top 3 extensions
            top_exts = sorted(
                repo_data['by_extension'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            ext_str = ', '.join([f"{ext} ({count})" for ext, count in top_exts])

            report_lines.append(
                f"| {repo_name} | {files:,} | {self._format_size(size)} | {ext_str} |"
            )

        report_lines.append(f"| **TOTAL** | **{total_files:,}** | **{self._format_size(total_size)}** | - |")

        # Summary statistics
        report_lines.extend([
            "\n## Summary Statistics\n",
            f"- **Total Repositories Scanned**: {len(self.results)}",
            f"- **Total Files**: {total_files:,}",
            f"- **Total Size**: {self._format_size(total_size)}",
            f"- **Analysis Directory**: `{self.analysis_dir}`"
        ])

        # Extension distribution
        report_lines.append("\n## File Type Distribution\n")

        all_exts = defaultdict(int)
        for repo_data in self.results.values():
            if 'error' in repo_data:
                continue
            for ext, count in repo_data['by_extension'].items():
                all_exts[ext] += count

        report_lines.append("| Extension | Count | Percentage |")
        report_lines.append("|-----------|-------|------------|")

        for ext, count in sorted(all_exts.items(), key=lambda x: x[1], reverse=True)[:15]:
            pct = (count / total_files * 100) if total_files > 0 else 0
            report_lines.append(f"| {ext} | {count:,} | {pct:.1f}% |")

        # Size distribution
        report_lines.append("\n## File Size Distribution\n")

        total_small = sum(r.get('by_size', {}).get('small', 0) for r in self.results.values() if 'error' not in r)
        total_medium = sum(r.get('by_size', {}).get('medium', 0) for r in self.results.values() if 'error' not in r)
        total_large = sum(r.get('by_size', {}).get('large', 0) for r in self.results.values() if 'error' not in r)

        report_lines.append("| Size Category | Count | Percentage |")
        report_lines.append("|---------------|-------|------------|")
        report_lines.append(f"| Small (<10KB) | {total_small:,} | {total_small/total_files*100:.1f}% |")
        report_lines.append(f"| Medium (10KB-1MB) | {total_medium:,} | {total_medium/total_files*100:.1f}% |")
        report_lines.append(f"| Large (>1MB) | {total_large:,} | {total_large/total_files*100:.1f}% |")

        # Recommendations
        report_lines.extend([
            "\n## Recommendations\n",
            "1. **Consolidate Repositories**: Consider merging `pythons` and `pythons-sort`",
            "2. **Documentation**: Auto-generate docs for undocumented scripts",
            "3. **Deduplication**: Remove duplicate files (see duplicates_report.json)",
            "4. **Organization**: Implement project-based structure",
            "5. **Metadata**: Convert text files to structured databases"
        ])

        report_content = '\n'.join(report_lines)

        # Save report
        report_file = self.analysis_dir / f'ECOSYSTEM_REPORT_{datetime.now().strftime("%Y%m%d")}.md'
        with open(report_file, 'w') as f:
            f.write(report_content)

        print(f"✅ Summary report saved to: {report_file}\n")
        return report_content


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Analyze complete content ecosystem')
    parser.add_argument('--scan-all', action='store_true', help='Scan all repositories')
    parser.add_argument('--compare-repos', nargs=2, metavar=('REPO1', 'REPO2'),
                       help='Compare two repositories')
    parser.add_argument('--find-duplicates', action='store_true', help='Find duplicate files')
    parser.add_argument('--generate-report', action='store_true', help='Generate summary report')
    parser.add_argument('--base-dir', type=Path, default=Path.home(),
                       help='Base directory (default: ~)')

    args = parser.parse_args()

    analyzer = EcosystemAnalyzer(base_dir=args.base_dir)

    if args.scan_all:
        analyzer.scan_all_repositories()

    if args.find_duplicates:
        if not analyzer.results:
            print("⚠️  No scan results found. Run --scan-all first.")
        else:
            analyzer.find_duplicates()

    if args.compare_repos:
        if not analyzer.results:
            print("⚠️  No scan results found. Run --scan-all first.")
        else:
            analyzer.compare_repositories(args.compare_repos[0], args.compare_repos[1])

    if args.generate_report:
        if not analyzer.results:
            print("⚠️  No scan results found. Run --scan-all first.")
        else:
            report = analyzer.generate_summary_report()
            print(report)

    # If no arguments, run everything
    if not any([args.scan_all, args.find_duplicates, args.compare_repos, args.generate_report]):
        print("🚀 Running complete ecosystem analysis...\n")
        analyzer.scan_all_repositories()
        analyzer.find_duplicates()
        analyzer.compare_repositories('pythons', 'pythons-sort')
        analyzer.generate_summary_report()
        print("\n✅ Complete analysis finished!")
        print(f"📁 Results saved to: {analyzer.analysis_dir}")


if __name__ == "__main__":
    main()
