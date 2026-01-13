#!/usr/bin/env python3
"""
🧠 INTELLIGENT DEEPDIVE SCANNER
================================
Advanced content-aware scanner with parent folder awareness and multi-depth analysis

Features:
✨ Intelligent content analysis (not just file types)
✨ Parent folder context awareness
✨ Multi-depth hierarchical scanning
✨ Content pattern recognition
✨ Relationship mapping (parent-child, sibling analysis)
✨ Smart categorization based on folder context
✨ CSV export with comprehensive metadata
"""

import os
import csv
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple
import re


class Colors:
    """Terminal colors for output"""

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


class IntelligentDeepdiveScanner:
    """Intelligent scanner with parent folder awareness and multi-depth analysis"""

    def __init__(
        self,
        root_path: Path,
        max_depth: Optional[int] = None,
        output_dir: Optional[Path] = None,
    ):
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.root_path / f"deepdive_scan_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data structures
        self.all_files: List[Dict] = []
        self.folder_hierarchy: Dict[str, Dict] = {}
        self.content_patterns: defaultdict = defaultdict(list)
        self.parent_contexts: Dict[str, Dict] = {}
        self.depth_analysis: Dict[int, Dict] = defaultdict(
            lambda: {
                "files": [],
                "folders": [],
                "total_size": 0,
                "file_types": Counter(),
                "categories": Counter(),
            }
        )

        # Statistics
        self.stats = {
            "total_files": 0,
            "total_folders": 0,
            "max_depth_found": 0,
            "total_size_bytes": 0,
            "unique_extensions": set(),
            "content_categories": Counter(),
            "parent_folder_patterns": Counter(),
        }

        # Content analysis patterns
        self.content_keywords = {
            "code": [
                "function",
                "class",
                "import",
                "def ",
                "const ",
                "var ",
                "export",
                "module",
            ],
            "documentation": [
                "readme",
                "docs",
                "guide",
                "tutorial",
                "api",
                "reference",
            ],
            "config": [
                "config",
                "settings",
                "preferences",
                ".env",
                ".json",
                ".yaml",
                ".toml",
            ],
            "data": ["database", "csv", "json", "xml", "sqlite", "db"],
            "media": ["image", "video", "audio", "photo", "picture", "movie", "song"],
            "archive": ["zip", "tar", "gz", "rar", "7z", "archive"],
            "project": [
                "package.json",
                "requirements.txt",
                "setup.py",
                "pyproject.toml",
                "Cargo.toml",
            ],
        }

    def print_header(self, text: str, color=Colors.CYAN):
        """Print formatted header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")

    def analyze_file_content(self, file_path: Path) -> Dict:
        """Intelligently analyze file content (not just extension)"""
        analysis = {
            "content_type": "unknown",
            "category": "other",
            "keywords_found": [],
            "is_code": False,
            "is_documentation": False,
            "is_config": False,
            "is_data": False,
            "is_media": False,
            "is_archive": False,
            "is_project_file": False,
            "has_readable_content": False,
            "line_count": 0,
            "encoding": "unknown",
        }

        # Check extension first
        ext = file_path.suffix.lower()
        name_lower = file_path.name.lower()

        # Detect project files
        if name_lower in [
            "package.json",
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "build.gradle",
        ]:
            analysis["is_project_file"] = True
            analysis["category"] = "project"
            return analysis

        # Try to read and analyze content for text files
        text_extensions = {
            ".txt",
            ".md",
            ".py",
            ".js",
            ".ts",
            ".html",
            ".css",
            ".json",
            ".yaml",
            ".yml",
            ".xml",
            ".csv",
            ".sh",
            ".bat",
            ".ps1",
            ".rb",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".hpp",
            ".go",
            ".rs",
            ".php",
            ".swift",
            ".kt",
            ".scala",
            ".clj",
            ".lua",
            ".r",
            ".m",
            ".pl",
        }

        if ext in text_extensions or any(
            name_lower.endswith(ext) for ext in text_extensions
        ):
            try:
                # Try different encodings
                for encoding in ["utf-8", "latin-1", "cp1252"]:
                    try:
                        with open(
                            file_path, "r", encoding=encoding, errors="ignore"
                        ) as f:
                            content = f.read(8192)  # Read first 8KB
                            analysis["has_readable_content"] = True
                            analysis["encoding"] = encoding
                            analysis["line_count"] = content.count("\n")

                            content_lower = content.lower()

                            # Check for code patterns
                            for keyword in self.content_keywords["code"]:
                                if keyword in content_lower:
                                    analysis["keywords_found"].append(keyword)
                                    analysis["is_code"] = True
                                    analysis["category"] = "code"

                            # Check for documentation
                            for keyword in self.content_keywords["documentation"]:
                                if keyword in content_lower:
                                    analysis["keywords_found"].append(keyword)
                                    analysis["is_documentation"] = True
                                    if analysis["category"] == "other":
                                        analysis["category"] = "documentation"

                            # Check for config patterns
                            if any(
                                kw in content_lower or kw in name_lower
                                for kw in ["config", "settings", "preferences", ".env"]
                            ):
                                analysis["is_config"] = True
                                if analysis["category"] == "other":
                                    analysis["category"] = "config"

                            break
                    except (UnicodeDecodeError, PermissionError):
                        continue
            except (PermissionError, OSError):
                pass

        # Media detection
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            if mime_type.startswith("image/"):
                analysis["is_media"] = True
                analysis["category"] = "image"
            elif mime_type.startswith("video/"):
                analysis["is_media"] = True
                analysis["category"] = "video"
            elif mime_type.startswith("audio/"):
                analysis["is_media"] = True
                analysis["category"] = "audio"

        # Archive detection
        if ext in {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z", ".dmg", ".iso"}:
            analysis["is_archive"] = True
            analysis["category"] = "archive"

        # Data file detection
        if ext in {".csv", ".json", ".xml", ".sqlite", ".db", ".sql"}:
            analysis["is_data"] = True
            if analysis["category"] == "other":
                analysis["category"] = "data"

        return analysis

    def analyze_parent_context(self, file_path: Path) -> Dict:
        """Analyze parent folder context and hierarchy"""
        context = {
            "parent_path": str(file_path.parent),
            "parent_name": file_path.parent.name,
            "grandparent_name": (
                file_path.parent.parent.name
                if file_path.parent.parent != file_path.parent
                else ""
            ),
            "depth": len(file_path.relative_to(self.root_path).parts) - 1,
            "folder_chain": [],
            "sibling_files": [],
            "sibling_folders": [],
            "parent_category_hint": "unknown",
            "folder_pattern": "unknown",
        }

        # Build folder chain
        current = file_path.parent
        while current != self.root_path and current != current.parent:
            context["folder_chain"].append(current.name)
            current = current.parent

        context["folder_chain"].reverse()

        # Analyze siblings
        try:
            siblings = list(file_path.parent.iterdir())
            context["sibling_files"] = [s.name for s in siblings if s.is_file()]
            context["sibling_folders"] = [s.name for s in siblings if s.is_dir()]
        except (PermissionError, OSError):
            pass

        # Detect parent category from folder name
        parent_lower = file_path.parent.name.lower()
        if any(
            kw in parent_lower
            for kw in ["code", "src", "lib", "script", "python", "js", "ts"]
        ):
            context["parent_category_hint"] = "code"
        elif any(
            kw in parent_lower for kw in ["doc", "readme", "guide", "manual", "help"]
        ):
            context["parent_category_hint"] = "documentation"
        elif any(
            kw in parent_lower for kw in ["image", "photo", "pic", "img", "picture"]
        ):
            context["parent_category_hint"] = "image"
        elif any(kw in parent_lower for kw in ["video", "movie", "film", "vid"]):
            context["parent_category_hint"] = "video"
        elif any(kw in parent_lower for kw in ["audio", "music", "sound", "song"]):
            context["parent_category_hint"] = "audio"
        elif any(
            kw in parent_lower for kw in ["data", "database", "db", "csv", "json"]
        ):
            context["parent_category_hint"] = "data"
        elif any(kw in parent_lower for kw in ["config", "setting", "pref", "env"]):
            context["parent_category_hint"] = "config"
        elif any(kw in parent_lower for kw in ["test", "spec", "specs"]):
            context["parent_category_hint"] = "test"
        elif any(kw in parent_lower for kw in ["temp", "tmp", "cache", "log"]):
            context["parent_category_hint"] = "temporary"

        # Detect folder pattern
        if re.match(r"^\d{4}-\d{2}-\d{2}", parent_lower):
            context["folder_pattern"] = "date"
        elif re.match(r"^v?\d+\.\d+", parent_lower):
            context["folder_pattern"] = "version"
        elif "_" in parent_lower or "-" in parent_lower:
            context["folder_pattern"] = "snake_case"
        elif any(c.isupper() for c in parent_lower if c.isalpha()):
            context["folder_pattern"] = "mixed_case"
        else:
            context["folder_pattern"] = "simple"

        return context

    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate MD5 hash for duplicate detection"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (PermissionError, OSError, IOError):
            return None

    def scan_recursive(self, current_path: Path = None, current_depth: int = 0):
        """Recursively scan with depth awareness"""
        if current_path is None:
            current_path = self.root_path

        if self.max_depth and current_depth > self.max_depth:
            return

        try:
            items = list(current_path.iterdir())
        except (PermissionError, OSError) as e:
            print(f"⚠️  Cannot access {current_path}: {e}")
            return

        # Update max depth found
        if current_depth > self.stats["max_depth_found"]:
            self.stats["max_depth_found"] = current_depth

        # Process files
        for item in items:
            if item.is_file():
                try:
                    stat = item.stat()
                    file_size = stat.st_size
                    created = datetime.fromtimestamp(stat.st_ctime)
                    modified = datetime.fromtimestamp(stat.st_mtime)

                    # Content analysis
                    content_analysis = self.analyze_file_content(item)

                    # Parent context analysis
                    parent_context = self.analyze_parent_context(item)

                    # File hash for duplicate detection
                    file_hash = self.calculate_file_hash(item)

                    # Build comprehensive file record
                    file_record = {
                        "file_path": str(item),
                        "relative_path": str(item.relative_to(self.root_path)),
                        "filename": item.name,
                        "extension": item.suffix.lower(),
                        "stem": item.stem,
                        "size_bytes": file_size,
                        "size_mb": file_size / (1024 * 1024),
                        "created": created.isoformat(),
                        "modified": modified.isoformat(),
                        "depth": parent_context["depth"],
                        "parent_path": parent_context["parent_path"],
                        "parent_name": parent_context["parent_name"],
                        "grandparent_name": parent_context["grandparent_name"],
                        "folder_chain": " > ".join(parent_context["folder_chain"]),
                        "sibling_files_count": len(parent_context["sibling_files"]),
                        "sibling_folders_count": len(parent_context["sibling_folders"]),
                        "parent_category_hint": parent_context["parent_category_hint"],
                        "folder_pattern": parent_context["folder_pattern"],
                        "content_category": content_analysis["category"],
                        "is_code": content_analysis["is_code"],
                        "is_documentation": content_analysis["is_documentation"],
                        "is_config": content_analysis["is_config"],
                        "is_data": content_analysis["is_data"],
                        "is_media": content_analysis["is_media"],
                        "is_archive": content_analysis["is_archive"],
                        "is_project_file": content_analysis["is_project_file"],
                        "has_readable_content": content_analysis[
                            "has_readable_content"
                        ],
                        "line_count": content_analysis["line_count"],
                        "encoding": content_analysis["encoding"],
                        "keywords_found": ", ".join(content_analysis["keywords_found"]),
                        "file_hash": file_hash,
                        "mime_type": mimetypes.guess_type(str(item))[0] or "unknown",
                    }

                    self.all_files.append(file_record)

                    # Update statistics
                    self.stats["total_files"] += 1
                    self.stats["total_size_bytes"] += file_size
                    self.stats["unique_extensions"].add(item.suffix.lower())
                    self.stats["content_categories"][content_analysis["category"]] += 1
                    self.stats["parent_folder_patterns"][
                        parent_context["folder_pattern"]
                    ] += 1

                    # Update depth analysis
                    self.depth_analysis[current_depth]["files"].append(file_record)
                    self.depth_analysis[current_depth]["total_size"] += file_size
                    self.depth_analysis[current_depth]["file_types"][
                        item.suffix.lower()
                    ] += 1
                    self.depth_analysis[current_depth]["categories"][
                        content_analysis["category"]
                    ] += 1

                    # Store parent context
                    self.parent_contexts[str(item)] = parent_context

                except (OSError, PermissionError) as e:
                    print(f"⚠️  Error processing {item}: {e}")

            elif item.is_dir():
                # Skip system directories
                if item.name.startswith(".") and item.name not in [".git", ".github"]:
                    continue
                if item.name in [
                    "__pycache__",
                    "node_modules",
                    ".venv",
                    "venv",
                    "dist",
                    "build",
                ]:
                    continue

                self.stats["total_folders"] += 1
                self.depth_analysis[current_depth]["folders"].append(str(item))

                # Recursively scan subdirectories
                self.scan_recursive(item, current_depth + 1)

    def generate_reports(self):
        """Generate comprehensive CSV and JSON reports"""
        self.print_header("📊 GENERATING REPORTS", Colors.GREEN)

        # Main CSV report
        csv_path = self.output_dir / f"deepdive_scan_{self.timestamp}.csv"
        if self.all_files:
            fieldnames = list(self.all_files[0].keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.all_files)
            print(f"✅ Main CSV: {csv_path} ({len(self.all_files):,} files)")

        # Depth analysis CSV
        depth_csv_path = self.output_dir / f"depth_analysis_{self.timestamp}.csv"
        depth_rows = []
        for depth, data in sorted(self.depth_analysis.items()):
            depth_rows.append(
                {
                    "depth": depth,
                    "file_count": len(data["files"]),
                    "folder_count": len(data["folders"]),
                    "total_size_mb": data["total_size"] / (1024 * 1024),
                    "top_extensions": ", ".join(
                        [
                            f"{ext}({count})"
                            for ext, count in data["file_types"].most_common(5)
                        ]
                    ),
                    "top_categories": ", ".join(
                        [
                            f"{cat}({count})"
                            for cat, count in data["categories"].most_common(5)
                        ]
                    ),
                }
            )

        if depth_rows:
            with open(depth_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=depth_rows[0].keys())
                writer.writeheader()
                writer.writerows(depth_rows)
            print(f"✅ Depth Analysis CSV: {depth_csv_path}")

        # Summary JSON
        summary_path = self.output_dir / f"summary_{self.timestamp}.json"
        summary = {
            "scan_info": {
                "root_path": str(self.root_path),
                "timestamp": self.timestamp,
                "max_depth": self.max_depth,
                "max_depth_found": self.stats["max_depth_found"],
            },
            "statistics": {
                "total_files": self.stats["total_files"],
                "total_folders": self.stats["total_folders"],
                "total_size_gb": self.stats["total_size_bytes"] / (1024**3),
                "unique_extensions": len(self.stats["unique_extensions"]),
                "content_categories": dict(self.stats["content_categories"]),
                "folder_patterns": dict(self.stats["parent_folder_patterns"]),
            },
            "depth_summary": {
                str(depth): {
                    "files": len(data["files"]),
                    "folders": len(data["folders"]),
                    "size_mb": data["total_size"] / (1024 * 1024),
                }
                for depth, data in sorted(self.depth_analysis.items())
            },
        }

        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Summary JSON: {summary_path}")

        return csv_path, depth_csv_path, summary_path

    def print_summary(self):
        """Print scan summary"""
        self.print_header("📈 SCAN SUMMARY", Colors.CYAN)

        print(f"{Colors.BOLD}Root Path:{Colors.END} {self.root_path}")
        print(f"{Colors.BOLD}Total Files:{Colors.END} {self.stats['total_files']:,}")
        print(
            f"{Colors.BOLD}Total Folders:{Colors.END} {self.stats['total_folders']:,}"
        )
        print(
            f"{Colors.BOLD}Max Depth Found:{Colors.END} {self.stats['max_depth_found']}"
        )
        print(
            f"{Colors.BOLD}Total Size:{Colors.END} {self.stats['total_size_bytes'] / (1024**3):.2f} GB"
        )
        print(
            f"{Colors.BOLD}Unique Extensions:{Colors.END} {len(self.stats['unique_extensions'])}"
        )

        print(f"\n{Colors.BOLD}Content Categories:{Colors.END}")
        for cat, count in self.stats["content_categories"].most_common():
            print(f"  {cat}: {count:,}")

        print(f"\n{Colors.BOLD}Folder Patterns:{Colors.END}")
        for pattern, count in self.stats["parent_folder_patterns"].most_common():
            print(f"  {pattern}: {count:,}")

        print(f"\n{Colors.BOLD}Files by Depth:{Colors.END}")
        for depth in sorted(self.depth_analysis.keys()):
            data = self.depth_analysis[depth]
            print(
                f"  Depth {depth}: {len(data['files']):,} files, "
                f"{len(data['folders']):,} folders, "
                f"{data['total_size'] / (1024**2):.2f} MB"
            )

    def run(self):
        """Execute the full scan"""
        self.print_header("🧠 INTELLIGENT DEEPDIVE SCANNER", Colors.MAGENTA)
        print(f"Scanning: {self.root_path}")
        if self.max_depth:
            print(f"Max Depth: {self.max_depth}")
        print()

        # Perform scan
        self.print_header("🔍 SCANNING FILES", Colors.BLUE)
        self.scan_recursive()

        # Generate reports
        self.generate_reports()

        # Print summary
        self.print_summary()

        self.print_header("✅ SCAN COMPLETE", Colors.GREEN)
        print(f"Output directory: {self.output_dir}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Intelligent deepdive scanner with parent folder awareness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", type=Path, help="Root path to scan")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Maximum depth to scan (default: unlimited)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: <root>/deepdive_scan_<timestamp>)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"❌ Error: Path does not exist: {args.path}")
        return 1

    scanner = IntelligentDeepdiveScanner(
        root_path=args.path, max_depth=args.max_depth, output_dir=args.output
    )

    scanner.run()
    return 0


if __name__ == "__main__":
    exit(main())
