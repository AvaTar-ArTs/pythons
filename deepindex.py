#!/usr/bin/env python3
"""
Deep Directory Indexer - Unlimited depth filesystem analysis and indexing
Analyzes directory structures recursively and generates comprehensive indexes
"""

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Optional dependency
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

class DirectoryIndexer:
    """Recursively indexes directories with comprehensive metadata collection"""

    def __init__(self,
                 root_path: str,
                 follow_symlinks: bool = False,
                 include_hidden: bool = False,
                 calculate_checksums: bool = False,
                 content_analysis: bool = False,
                 exclude_patterns: Optional[List[str]] = None):
        self.root_path = Path(root_path).resolve()
        self.follow_symlinks = follow_symlinks
        self.include_hidden = include_hidden
        self.calculate_checksums = calculate_checksums
        self.content_analysis = content_analysis
        self.exclude_patterns = exclude_patterns or []

        # Statistics
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'extensions': defaultdict(int),
            'depth_distribution': defaultdict(int),
            'largest_files': [],
            'errors': []
        }

        # Initialize file type detection
        if HAS_MAGIC:
            try:
                self.magic = magic.Magic(mime=True)
            except:
                self.magic = None
        else:
            self.magic = None

    def should_exclude(self, path: Path) -> bool:
        """Check if path matches exclusion patterns"""
        path_str = str(path)
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True
        return False

    def calculate_file_hash(self, filepath: Path, algorithm: str = 'sha256') -> Optional[str]:
        """Calculate file checksum"""
        try:
            hash_func = hashlib.new(algorithm)
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            return None

    def analyze_file(self, filepath: Path, depth: int) -> Dict:
        """Extract comprehensive metadata from a file"""
        try:
            stat_info = filepath.stat()

            # Basic metadata
            metadata = {
                'path': str(filepath),
                'name': filepath.name,
                'extension': filepath.suffix.lower(),
                'size': stat_info.st_size,
                'depth': depth,
                'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                'is_symlink': filepath.is_symlink(),
                'permissions': oct(stat_info.st_mode)[-3:],
            }

            # Mime type detection
            if self.magic:
                try:
                    metadata['mime_type'] = self.magic.from_file(str(filepath))
                except:
                    metadata['mime_type'] = mimetypes.guess_type(str(filepath))[0]
            else:
                metadata['mime_type'] = mimetypes.guess_type(str(filepath))[0]

            # Checksum calculation
            if self.calculate_checksums:
                metadata['sha256'] = self.calculate_file_hash(filepath)

            # Content analysis for text files
            if self.content_analysis and metadata.get('mime_type', '').startswith('text'):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        metadata['line_count'] = content.count('\n')
                        metadata['char_count'] = len(content)
                        metadata['word_count'] = len(content.split())
                except:
                    pass

            # Update statistics
            self.stats['total_files'] += 1
            self.stats['total_size'] += stat_info.st_size
            self.stats['extensions'][filepath.suffix.lower()] += 1
            self.stats['depth_distribution'][depth] += 1

            if metadata.get('mime_type'):
                self.stats['file_types'][metadata['mime_type']] += 1

            # Track largest files (top 100)
            self.stats['largest_files'].append((filepath, stat_info.st_size))
            self.stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
            self.stats['largest_files'] = self.stats['largest_files'][:100]

            return metadata

        except Exception as e:
            error_msg = f"Error analyzing {filepath}: {str(e)}"
            self.stats['errors'].append(error_msg)
            return None

    def index_directory(self, directory: Path, depth: int = 0) -> Dict:
        """Recursively index a directory and all its contents"""
        try:
            # Check exclusions
            if self.should_exclude(directory):
                return None

            # Skip hidden directories if configured
            if not self.include_hidden and directory.name.startswith('.'):
                return None

            dir_info = {
                'path': str(directory),
                'name': directory.name,
                'depth': depth,
                'type': 'directory',
                'children': []
            }

            self.stats['total_dirs'] += 1

            try:
                entries = list(directory.iterdir())
            except PermissionError:
                error_msg = f"Permission denied: {directory}"
                self.stats['errors'].append(error_msg)
                return dir_info

            for entry in sorted(entries, key=lambda x: (not x.is_dir(), x.name)):
                # Skip hidden files/dirs if configured
                if not self.include_hidden and entry.name.startswith('.'):
                    continue

                # Check exclusions
                if self.should_exclude(entry):
                    continue

                # Handle symlinks
                if entry.is_symlink() and not self.follow_symlinks:
                    continue

                try:
                    if entry.is_file():
                        file_info = self.analyze_file(entry, depth + 1)
                        if file_info:
                            dir_info['children'].append(file_info)

                    elif entry.is_dir():
                        subdir_info = self.index_directory(entry, depth + 1)
                        if subdir_info:
                            dir_info['children'].append(subdir_info)

                except Exception as e:
                    error_msg = f"Error processing {entry}: {str(e)}"
                    self.stats['errors'].append(error_msg)

            return dir_info

        except Exception as e:
            error_msg = f"Error indexing directory {directory}: {str(e)}"
            self.stats['errors'].append(error_msg)
            return None

    def generate_index(self) -> Dict:
        """Generate complete index starting from root path"""
        print(f"Indexing: {self.root_path}")
        print(f"Follow symlinks: {self.follow_symlinks}")
        print(f"Include hidden: {self.include_hidden}")
        print(f"Calculate checksums: {self.calculate_checksums}")
        print(f"Content analysis: {self.content_analysis}")
        print("-" * 60)

        start_time = datetime.now()

        index = self.index_directory(self.root_path)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        result = {
            'metadata': {
                'root_path': str(self.root_path),
                'indexed_at': datetime.now().isoformat(),
                'duration_seconds': duration,
                'indexer_version': '1.0.0'
            },
            'statistics': {
                'total_files': self.stats['total_files'],
                'total_directories': self.stats['total_dirs'],
                'total_size_bytes': self.stats['total_size'],
                'total_size_human': self._format_bytes(self.stats['total_size']),
                'file_types': dict(self.stats['file_types']),
                'extensions': dict(self.stats['extensions']),
                'depth_distribution': dict(self.stats['depth_distribution']),
                'max_depth': max(self.stats['depth_distribution'].keys()) if self.stats['depth_distribution'] else 0,
                'errors_count': len(self.stats['errors']),
                'largest_files': [
                    {'path': str(f[0]), 'size': f[1], 'size_human': self._format_bytes(f[1])}
                    for f in self.stats['largest_files'][:20]
                ]
            },
            'tree': index,
            'errors': self.stats['errors']
        }

        return result

    @staticmethod
    def _format_bytes(size: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


class IndexExporter:
    """Export indexes in multiple formats"""

    @staticmethod
    def export_json(index: Dict, output_path: Path, pretty: bool = True):
        """Export index as JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(index, f, indent=2, ensure_ascii=False)
            else:
                json.dump(index, f, ensure_ascii=False)
        print(f"✓ JSON index saved to: {output_path}")

    @staticmethod
    def export_csv(index: Dict, output_path: Path):
        """Export flat file list as CSV"""
        files = IndexExporter._flatten_files(index['tree'])

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if files:
                writer = csv.DictWriter(f, fieldnames=files[0].keys())
                writer.writeheader()
                writer.writerows(files)

        print(f"✓ CSV index saved to: {output_path}")

    @staticmethod
    def export_markdown(index: Dict, output_path: Path):
        """Export index as Markdown report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Directory Index Report\n\n")
            f.write(f"**Path:** `{index['metadata']['root_path']}`\n\n")
            f.write(f"**Generated:** {index['metadata']['indexed_at']}\n\n")
            f.write(f"**Duration:** {index['metadata']['duration_seconds']:.2f} seconds\n\n")

            f.write("## Statistics\n\n")
            stats = index['statistics']
            f.write(f"- **Total Files:** {stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {stats['total_directories']:,}\n")
            f.write(f"- **Total Size:** {stats['total_size_human']}\n")
            f.write(f"- **Max Depth:** {stats['max_depth']}\n")
            f.write(f"- **Errors:** {stats['errors_count']}\n\n")

            if stats['file_types']:
                f.write("## File Types Distribution\n\n")
                sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
                for mime_type, count in sorted_types[:20]:
                    f.write(f"- {mime_type}: {count:,}\n")
                f.write("\n")

            if stats['extensions']:
                f.write("## Top Extensions\n\n")
                sorted_ext = sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True)
                for ext, count in sorted_ext[:20]:
                    ext_display = ext if ext else "(no extension)"
                    f.write(f"- {ext_display}: {count:,}\n")
                f.write("\n")

            if stats['largest_files']:
                f.write("## Largest Files\n\n")
                for file_info in stats['largest_files'][:20]:
                    f.write(f"- `{file_info['path']}` - {file_info['size_human']}\n")
                f.write("\n")

            f.write("## Directory Tree\n\n")
            f.write("```\n")
            IndexExporter._write_tree(f, index['tree'], 0)
            f.write("```\n")

        print(f"✓ Markdown report saved to: {output_path}")

    @staticmethod
    def _flatten_files(node: Dict, files: Optional[List] = None) -> List[Dict]:
        """Flatten tree structure to list of files"""
        if files is None:
            files = []

        if node.get('type') == 'directory':
            for child in node.get('children', []):
                IndexExporter._flatten_files(child, files)
        else:
            files.append(node)

        return files

    @staticmethod
    def _write_tree(f, node: Dict, level: int, prefix: str = ""):
        """Write tree structure in ASCII format"""
        if node is None:
            return

        indent = "  " * level
        name = node['name']

        if node.get('type') == 'directory':
            f.write(f"{indent}{name}/\n")
            for child in node.get('children', []):
                IndexExporter._write_tree(f, child, level + 1)
        else:
            size = DirectoryIndexer._format_bytes(node.get('size', 0))
            f.write(f"{indent}{name} ({size})\n")


def main():
    parser = argparse.ArgumentParser(
        description='Deep Directory Indexer - Analyze and index directories with unlimited depth',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/directory
  %(prog)s ~/Documents --include-hidden --checksums
  %(prog)s /data --format json,csv,markdown --output ./index
  %(prog)s . --exclude node_modules,venv,.git --content-analysis
        """
    )

    parser.add_argument('path', help='Directory path to index')
    parser.add_argument('-o', '--output', default='./directory_index',
                       help='Output path prefix (default: ./directory_index)')
    parser.add_argument('-f', '--format', default='json,markdown',
                       help='Output formats: json,csv,markdown (default: json,markdown)')
    parser.add_argument('--follow-symlinks', action='store_true',
                       help='Follow symbolic links')
    parser.add_argument('--include-hidden', action='store_true',
                       help='Include hidden files and directories')
    parser.add_argument('--checksums', action='store_true',
                       help='Calculate SHA256 checksums (slower)')
    parser.add_argument('--content-analysis', action='store_true',
                       help='Analyze text file contents (line/word counts)')
    parser.add_argument('--exclude', default='',
                       help='Comma-separated patterns to exclude (e.g., node_modules,.git)')
    parser.add_argument('--pretty', action='store_true', default=True,
                       help='Pretty print JSON output (default: True)')

    args = parser.parse_args()

    # Validate path
    path = Path(args.path).resolve()
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if not path.is_dir():
        print(f"Error: Path is not a directory: {path}", file=sys.stderr)
        sys.exit(1)

    # Parse exclusion patterns
    exclude_patterns = [p.strip() for p in args.exclude.split(',') if p.strip()]

    # Create indexer
    indexer = DirectoryIndexer(
        root_path=str(path),
        follow_symlinks=args.follow_symlinks,
        include_hidden=args.include_hidden,
        calculate_checksums=args.checksums,
        content_analysis=args.content_analysis,
        exclude_patterns=exclude_patterns
    )

    # Generate index
    try:
        index = indexer.generate_index()
    except KeyboardInterrupt:
        print("\n\nIndexing interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError during indexing: {e}", file=sys.stderr)
        sys.exit(1)

    # Print summary
    print("\n" + "=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)
    print(f"Files: {index['statistics']['total_files']:,}")
    print(f"Directories: {index['statistics']['total_directories']:,}")
    print(f"Total Size: {index['statistics']['total_size_human']}")
    print(f"Max Depth: {index['statistics']['max_depth']}")
    print(f"Duration: {index['metadata']['duration_seconds']:.2f}s")
    if index['statistics']['errors_count'] > 0:
        print(f"Errors: {index['statistics']['errors_count']}")
    print("=" * 60)

    # Export in requested formats
    output_base = Path(args.output)
    formats = [f.strip().lower() for f in args.format.split(',')]

    exporter = IndexExporter()

    if 'json' in formats:
        exporter.export_json(index, output_base.with_suffix('.json'), args.pretty)

    if 'csv' in formats:
        exporter.export_csv(index, output_base.with_suffix('.csv'))

    if 'markdown' in formats or 'md' in formats:
        exporter.export_markdown(index, output_base.with_suffix('.md'))

    print(f"\n✓ All exports complete!")


if __name__ == "__main__":
    main()
