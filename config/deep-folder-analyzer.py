#!/usr/bin/env python3
"""
Deep Folder Analyzer - Comprehensive directory analysis tool
Analyzes directory structure, file types, sizes, and patterns
"""

import os
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import mimetypes


class DeepFolderAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path).expanduser().resolve()
        self.stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "file_types": defaultdict(int),
            "file_extensions": Counter(),
            "size_by_extension": defaultdict(int),
            "largest_files": [],
            "largest_dirs": [],
            "deepest_paths": [],
            "hidden_files": 0,
            "hidden_dirs": 0,
            "empty_dirs": [],
            "symlinks": 0,
            "depth_distribution": defaultdict(int),
            "errors": [],
        }
        self.dir_sizes = {}

    def get_mime_type(self, filepath):
        """Get MIME type of file"""
        mime_type, _ = mimetypes.guess_type(str(filepath))
        return mime_type or "unknown"

    def get_file_category(self, filepath):
        """Categorize file by extension"""
        ext = filepath.suffix.lower()

        # Programming languages
        if ext in [
            ".py",
            ".js",
            ".java",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            ".cs",
            ".go",
            ".rs",
            ".rb",
            ".php",
            ".swift",
            ".kt",
        ]:
            return "code"
        # Web
        elif ext in [".html", ".css", ".scss", ".sass", ".jsx", ".tsx", ".vue"]:
            return "web"
        # Data/Config
        elif ext in [
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".xml",
            ".csv",
            ".tsv",
            ".ini",
            ".conf",
        ]:
            return "config"
        # Documents
        elif ext in [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"]:
            return "document"
        # Images
        elif ext in [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".svg",
            ".webp",
            ".ico",
            ".tiff",
            ".psd",
        ]:
            return "image"
        # Video
        elif ext in [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"]:
            return "video"
        # Audio
        elif ext in [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"]:
            return "audio"
        # Archives
        elif ext in [".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".xz", ".tgz"]:
            return "archive"
        # Executables
        elif ext in [".exe", ".dll", ".so", ".dylib", ".app", ".dmg"]:
            return "executable"
        # Database
        elif ext in [".db", ".sqlite", ".sqlite3", ".mdb"]:
            return "database"
        else:
            return "other"

    def calculate_dir_size(self, dirpath):
        """Calculate total size of directory"""
        if str(dirpath) in self.dir_sizes:
            return self.dir_sizes[str(dirpath)]

        total = 0
        try:
            for entry in os.scandir(dirpath):
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += self.calculate_dir_size(entry.path)
                except (PermissionError, OSError) as e:
                    self.stats["errors"].append(f"Error accessing {entry.path}: {e}")
        except (PermissionError, OSError) as e:
            self.stats["errors"].append(f"Error accessing directory {dirpath}: {e}")

        self.dir_sizes[str(dirpath)] = total
        return total

    def analyze(self, max_depth=None):
        """Perform deep analysis of directory"""
        print(f"🔍 Starting deep analysis of: {self.root_path}")
        print(
            f"📅 Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        # First pass: collect all information
        for root, dirs, files in os.walk(self.root_path):
            try:
                root_path = Path(root)
                depth = len(root_path.relative_to(self.root_path).parts)

                # Track depth distribution
                self.stats["depth_distribution"][depth] += 1

                # Skip if max depth exceeded
                if max_depth and depth >= max_depth:
                    dirs.clear()
                    continue

                # Analyze directories
                self.stats["total_dirs"] += len(dirs)
                for dirname in dirs:
                    dirpath = root_path / dirname
                    if dirname.startswith("."):
                        self.stats["hidden_dirs"] += 1

                    if dirpath.is_symlink():
                        self.stats["symlinks"] += 1

                # Check for empty directory
                if not dirs and not files:
                    self.stats["empty_dirs"].append(
                        str(root_path.relative_to(self.root_path))
                    )

                # Analyze files
                for filename in files:
                    filepath = root_path / filename

                    try:
                        # Skip symlinks
                        if filepath.is_symlink():
                            self.stats["symlinks"] += 1
                            continue

                        # Get file stats
                        stat = filepath.stat()
                        size = stat.st_size

                        self.stats["total_files"] += 1
                        self.stats["total_size"] += size

                        # Track hidden files
                        if filename.startswith("."):
                            self.stats["hidden_files"] += 1

                        # Track extensions and categories
                        ext = (
                            filepath.suffix.lower()
                            if filepath.suffix
                            else "(no extension)"
                        )
                        self.stats["file_extensions"][ext] += 1
                        self.stats["size_by_extension"][ext] += size

                        category = self.get_file_category(filepath)
                        self.stats["file_types"][category] += 1

                        # Track largest files
                        rel_path = filepath.relative_to(self.root_path)
                        self.stats["largest_files"].append(
                            {
                                "path": str(rel_path),
                                "size": size,
                                "size_mb": size / (1024 * 1024),
                            }
                        )

                        # Track deepest paths
                        self.stats["deepest_paths"].append(
                            {"path": str(rel_path), "depth": len(rel_path.parts)}
                        )

                    except (PermissionError, OSError) as e:
                        self.stats["errors"].append(
                            f"Error accessing file {filepath}: {e}"
                        )

            except (PermissionError, OSError) as e:
                self.stats["errors"].append(f"Error accessing directory {root}: {e}")

        # Sort and limit results
        self.stats["largest_files"].sort(key=lambda x: x["size"], reverse=True)
        self.stats["largest_files"] = self.stats["largest_files"][:50]

        self.stats["deepest_paths"].sort(key=lambda x: x["depth"], reverse=True)
        self.stats["deepest_paths"] = self.stats["deepest_paths"][:30]

        # Calculate largest directories (top-level only for performance)
        print("📊 Calculating directory sizes (this may take a moment)...")
        top_level_dirs = [
            d for d in self.root_path.iterdir() if d.is_dir() and not d.is_symlink()
        ]
        for dirpath in top_level_dirs:
            try:
                size = self.calculate_dir_size(dirpath)
                self.stats["largest_dirs"].append(
                    {
                        "path": dirpath.name,
                        "size": size,
                        "size_gb": size / (1024 * 1024 * 1024),
                    }
                )
            except Exception as e:
                self.stats["errors"].append(
                    f"Error calculating size for {dirpath}: {e}"
                )

        self.stats["largest_dirs"].sort(key=lambda x: x["size"], reverse=True)
        self.stats["largest_dirs"] = self.stats["largest_dirs"][:30]

    def format_size(self, size):
        """Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def print_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "=" * 80)
        print("📊 DEEP FOLDER ANALYSIS REPORT")
        print("=" * 80)

        print(f"\n📁 Root Directory: {self.root_path}")
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n" + "-" * 80)
        print("📈 OVERVIEW STATISTICS")
        print("-" * 80)
        print(f"Total Files:        {self.stats['total_files']:,}")
        print(f"Total Directories:  {self.stats['total_dirs']:,}")
        print(f"Total Size:         {self.format_size(self.stats['total_size'])}")
        print(f"Hidden Files:       {self.stats['hidden_files']:,}")
        print(f"Hidden Directories: {self.stats['hidden_dirs']:,}")
        print(f"Symlinks:           {self.stats['symlinks']:,}")
        print(f"Empty Directories:  {len(self.stats['empty_dirs']):,}")

        print("\n" + "-" * 80)
        print("📊 FILE TYPE DISTRIBUTION")
        print("-" * 80)
        for category, count in sorted(
            self.stats["file_types"].items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (
                (count / self.stats["total_files"] * 100)
                if self.stats["total_files"] > 0
                else 0
            )
            print(f"{category:15} {count:10,} files ({percentage:6.2f}%)")

        print("\n" + "-" * 80)
        print("📝 TOP 20 FILE EXTENSIONS")
        print("-" * 80)
        for ext, count in self.stats["file_extensions"].most_common(20):
            size = self.stats["size_by_extension"][ext]
            percentage = (
                (count / self.stats["total_files"] * 100)
                if self.stats["total_files"] > 0
                else 0
            )
            print(
                f"{ext:20} {count:10,} files ({percentage:5.2f}%) - {self.format_size(size):>12}"
            )

        print("\n" + "-" * 80)
        print("💾 TOP 30 LARGEST DIRECTORIES")
        print("-" * 80)
        for i, item in enumerate(self.stats["largest_dirs"][:30], 1):
            print(
                f"{i:2}. {item['path']:50} {self.format_size(item['size']):>12} ({item['size_gb']:.2f} GB)"
            )

        print("\n" + "-" * 80)
        print("📄 TOP 30 LARGEST FILES")
        print("-" * 80)
        for i, item in enumerate(self.stats["largest_files"][:30], 1):
            print(f"{i:2}. {item['path']:70} {self.format_size(item['size']):>12}")

        print("\n" + "-" * 80)
        print("🌲 DEPTH DISTRIBUTION")
        print("-" * 80)
        max_depth = (
            max(self.stats["depth_distribution"].keys())
            if self.stats["depth_distribution"]
            else 0
        )
        for depth in range(min(15, max_depth + 1)):
            count = self.stats["depth_distribution"].get(depth, 0)
            bar = "█" * min(50, count // 10)
            print(f"Level {depth:2}: {count:6,} dirs {bar}")

        print("\n" + "-" * 80)
        print("🔎 DEEPEST PATHS (Top 20)")
        print("-" * 80)
        for i, item in enumerate(self.stats["deepest_paths"][:20], 1):
            print(f"{i:2}. [Depth: {item['depth']:2}] {item['path']}")

        if self.stats["empty_dirs"]:
            print("\n" + "-" * 80)
            print(f"📭 EMPTY DIRECTORIES (First 20 of {len(self.stats['empty_dirs'])})")
            print("-" * 80)
            for empty_dir in self.stats["empty_dirs"][:20]:
                print(f"   {empty_dir}")

        if self.stats["errors"]:
            print("\n" + "-" * 80)
            print(f"⚠️  ERRORS ENCOUNTERED (First 20 of {len(self.stats['errors'])})")
            print("-" * 80)
            for error in self.stats["errors"][:20]:
                print(f"   {error}")

        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 80)

    def save_json_report(self, output_path):
        """Save detailed JSON report"""
        # Convert defaultdict to regular dict for JSON serialization
        report = {
            "metadata": {
                "root_path": str(self.root_path),
                "analysis_date": datetime.now().isoformat(),
            },
            "statistics": {
                "total_files": self.stats["total_files"],
                "total_dirs": self.stats["total_dirs"],
                "total_size": self.stats["total_size"],
                "total_size_formatted": self.format_size(self.stats["total_size"]),
                "hidden_files": self.stats["hidden_files"],
                "hidden_dirs": self.stats["hidden_dirs"],
                "symlinks": self.stats["symlinks"],
                "empty_dirs_count": len(self.stats["empty_dirs"]),
            },
            "file_types": dict(self.stats["file_types"]),
            "file_extensions": dict(self.stats["file_extensions"]),
            "size_by_extension": {
                k: v for k, v in self.stats["size_by_extension"].items()
            },
            "largest_files": self.stats["largest_files"],
            "largest_dirs": self.stats["largest_dirs"],
            "deepest_paths": self.stats["deepest_paths"],
            "depth_distribution": dict(self.stats["depth_distribution"]),
            "empty_dirs": self.stats["empty_dirs"],
            "errors": self.stats["errors"],
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 JSON report saved to: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Deep Folder Analyzer - Comprehensive directory analysis"
    )
    parser.add_argument(
        "path", nargs="?", default="~/", help="Path to analyze (default: ~/)"
    )
    parser.add_argument("--max-depth", type=int, help="Maximum depth to traverse")
    parser.add_argument("--json", help="Save JSON report to specified file")

    args = parser.parse_args()

    analyzer = DeepFolderAnalyzer(args.path)
    analyzer.analyze(max_depth=args.max_depth)
    analyzer.print_report()

    if args.json:
        analyzer.save_json_report(args.json)
    else:
        # Auto-save JSON report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f"deep_analysis_{timestamp}.json"
        analyzer.save_json_report(json_path)


if __name__ == "__main__":
    main()
