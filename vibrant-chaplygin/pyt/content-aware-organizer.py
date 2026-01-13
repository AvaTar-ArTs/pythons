import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
🌳 CONTENT-AWARE PARENT FOLDER STRUCTURE ANALYZER
=================================================
Deep understanding of folder hierarchy, content relationships,
and intelligent organization with full context awareness.

Features:
✨ Deep parent folder structure analysis
✨ Content-aware categorization
✨ Relationship mapping between files
✨ Hierarchical context understanding
✨ Smart folder recommendations
✨ Directory-aware duplicate detection
✨ Parent-child relationship tracking
"""

import ast
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# Colors
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    END = "\033[0m"
    BOLD = "\033[1m"


# Emojis
class Emojis:
    TREE = "🌳"
    FOLDER = "📁"
    FILE = "📄"
    LINK = "🔗"
    BRAIN = "🧠"
    SPARKLES = "✨"
    TARGET = "🎯"
    CHART = "📊"
    MICROSCOPE = "🔬"
    CHECK = "✅"
    WARN = "⚠️"
    ROCKET = "🚀"


class FolderNode:
    """Represents a folder in the hierarchy with full context"""

    def __init__(self, path: Path, parent: Optional["FolderNode"] = None):
        self.path = path
        self.name = path.name
        self.parent = parent
        self.depth = 0 if parent is None else parent.depth + 1
        self.children: List["FolderNode"] = []
        self.files: List[Path] = []

        # Content analysis
        self.categories: Set[str] = set()
        self.technologies: Set[str] = set()
        self.patterns: Set[str] = set()
        self.purpose: Optional[str] = None

        # Statistics
        self.total_files = 0
        self.total_size = 0
        self.python_files = 0
        self.avg_complexity = 0.0

    def add_child(self, child: "FolderNode"):
        """Add child folder"""
        self.children.append(child)

    def add_file(self, file_path: Path):
        """Add file to this folder"""
        self.files.append(file_path)
        self.total_files += 1
        try:
            self.total_size += file_path.stat().st_size
        except (OSError, IOError, FileNotFoundError):
            pass
        if file_path.suffix == ".py":
            self.python_files += 1

    def get_ancestry(self) -> List[str]:
        """Get full path ancestry"""
        ancestry = []
        current = self
        while current:
            ancestry.append(current.name)
            current = current.parent
        return list(reversed(ancestry))

    def get_context_signature(self) -> str:
        """Generate signature based on folder context"""
        return f"{'/'.join(self.get_ancestry())}|{self.name}|{len(self.files)}"

    def __repr__(self):
        return f"FolderNode({self.name}, depth={self.depth}, files={len(self.files)})"


class ContentAwareAnalyzer:
    """Deep content and structure analysis"""

    # Enhanced category detection based on folder names and content
    CATEGORY_PATTERNS = {
        "ai_tools": [
            "ai",
            "ml",
            "model",
            "neural",
            "gpt",
            "claude",
            "gemini",
            "openai",
        ],
        "automation": ["bot", "automation", "scheduler", "cron", "workflow"],
        "api_integrations": ["api", "client", "sdk", "integration", "service"],
        "media_processing": ["image", "video", "audio", "media", "ffmpeg"],
        "web_scraping": ["scraper", "crawler", "spider", "selenium", "beautifulsoup"],
        "data_analysis": ["data", "analysis", "pandas", "numpy", "analytics"],
        "utilities": ["util", "helper", "tool", "common", "shared"],
        "testing": ["test", "pytest", "unittest", "spec"],
        "documentation": ["doc", "guide", "readme", "wiki"],
        "configuration": ["config", "settings", "env", "setup"],
        "social_media": ["instagram", "twitter", "facebook", "reddit", "tiktok"],
        "content_creation": ["generator", "creator", "builder", "maker"],
        "file_management": ["organizer", "sorter", "manager", "cleaner"],
    }

    def __init__(self):
        self.root_nodes: Dict[str, FolderNode] = {}
        self.all_nodes: List[FolderNode] = []
        self.file_to_node: Dict[Path, FolderNode] = {}

    def detect_category(self, folder_name: str, parent_names: List[str], file_content: str = "") -> Set[str]:
        """Detect categories based on folder name, ancestry, and content"""
        categories = set()
        all_text = f"{folder_name} {' '.join(parent_names)} {file_content}".lower()

        for category, patterns in self.CATEGORY_PATTERNS.items():
            if any(pattern in all_text for pattern in patterns):
                categories.add(category)

        return categories

    def analyze_file_content(self, filepath: Path) -> Dict[str, Any]:
        """Analyze file content for categorization"""
        analysis = {
            "imports": [],
            "functions": [],
            "classes": [],
            "keywords": set(),
            "complexity": 0,
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # AST analysis
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(node.name)
                    analysis["complexity"] += 1
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(node.name)
                    analysis["complexity"] += 2
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis["imports"].append(node.module)

            # Extract keywords from function/class names
            for name in analysis["functions"] + analysis["classes"]:
                # Split camelCase and snake_case
                import re

                words = re.findall(r"[a-z]+", name.lower())
                analysis["keywords"].update(words)

        except Exception as e:
            analysis["error"] = str(e)

        return analysis


class ParentFolderStructureAnalyzer:
    """Main analyzer with deep folder structure awareness"""

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.content_analyzer = ContentAwareAnalyzer()
        self.root_node = FolderNode(self.target_dir, parent=None)

        self.stats = {
            "total_folders": 0,
            "total_files": 0,
            "max_depth": 0,
            "categories_found": defaultdict(int),
            "folder_purposes": {},
        }

        self.folder_map: Dict[Path, FolderNode] = {}
        self.category_folders: Dict[str, List[FolderNode]] = defaultdict(list)

    def print_header(self, text: str, emoji=""):
        """Print fancy header"""
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def build_folder_tree(self, current_path: Path, parent_node: FolderNode, current_depth: int = 0):
        """Recursively build folder tree with full context"""

        # Skip certain directories
        skip_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            "merge_backup_",
            "merge_analysis_",
            "dedup_backup",
            "ai_diff_reports_",
        }

        try:
            for item in current_path.iterdir():
                # Skip hidden and special directories
                if any(item.name.startswith(skip) for skip in skip_dirs):
                    continue

                if item.is_dir():
                    # Create folder node
                    folder_node = FolderNode(item, parent=parent_node)
                    parent_node.add_child(folder_node)
                    self.folder_map[item] = folder_node
                    self.content_analyzer.all_nodes.append(folder_node)

                    self.stats["total_folders"] += 1
                    self.stats["max_depth"] = max(self.stats["max_depth"], folder_node.depth)

                    # Recursively process subdirectories
                    self.build_folder_tree(item, folder_node, current_depth + 1)

                elif item.is_file() and item.suffix == ".py":
                    # Add file to parent folder
                    parent_node.add_file(item)
                    self.content_analyzer.file_to_node[item] = parent_node
                    self.stats["total_files"] += 1

        except PermissionError:
            pass

    def analyze_folder_content(self, folder_node: FolderNode):
        """Deep analysis of folder content and purpose"""

        # Analyze all Python files in this folder
        for filepath in folder_node.files:
            if filepath.suffix == ".py":
                analysis = self.content_analyzer.analyze_file_content(filepath)

                # Aggregate technologies and patterns
                folder_node.technologies.update(analysis["imports"][:10])

                # Detect categories from content
                categories = self.content_analyzer.detect_category(
                    folder_node.name,
                    folder_node.get_ancestry(),
                    " ".join(analysis["keywords"]),
                )
                folder_node.categories.update(categories)

                # Track complexity
                if analysis["complexity"] > 0:
                    folder_node.avg_complexity = (
                        folder_node.avg_complexity * (len(folder_node.files) - 1) + analysis["complexity"]
                    ) / len(folder_node.files)

        # Determine folder purpose based on aggregated data
        if folder_node.categories:
            primary_category = list(folder_node.categories)[0]
            folder_node.purpose = self.infer_purpose(folder_node, primary_category)

            # Track for statistics
            for category in folder_node.categories:
                self.stats["categories_found"][category] += 1
                self.category_folders[category].append(folder_node)

    def infer_purpose(self, folder_node: FolderNode, category: str) -> str:
        """Infer folder purpose from category and context"""

        ancestry = folder_node.get_ancestry()

        purposes = {
            "ai_tools": f"AI/ML tools and integrations ({folder_node.python_files} scripts)",
            "automation": f"Automation scripts and bots ({folder_node.python_files} scripts)",
            "api_integrations": f"API clients and integrations ({folder_node.python_files} scripts)",
            "media_processing": f"Media processing tools ({folder_node.python_files} scripts)",
            "web_scraping": f"Web scraping and data extraction ({folder_node.python_files} scripts)",
            "utilities": f"Utility scripts and helpers ({folder_node.python_files} scripts)",
            "testing": f"Test suites and testing utilities ({folder_node.python_files} tests)",
        }

        return purposes.get(category, f"{category} ({folder_node.python_files} files)")

    def analyze_relationships(self):
        """Analyze relationships between folders"""

        self.print_header("ANALYZING FOLDER RELATIONSHIPS", Emojis.LINK)

        # Find related folders (similar categories, technologies)
        relationships = defaultdict(list)

        for i, node1 in enumerate(self.content_analyzer.all_nodes):
            for node2 in self.content_analyzer.all_nodes[i + 1 :]:
                # Check for category overlap
                common_categories = node1.categories & node2.categories
                if common_categories:
                    relationships[node1.path].append(
                        {
                            "related_to": node2.path,
                            "reason": f"Shared categories: {', '.join(common_categories)}",
                            "strength": len(common_categories) / max(len(node1.categories), len(node2.categories)),
                        }
                    )

                # Check for technology overlap
                common_tech = node1.technologies & node2.technologies
                if len(common_tech) >= 3:
                    relationships[node1.path].append(
                        {
                            "related_to": node2.path,
                            "reason": f"Shared technologies: {', '.join(list(common_tech)[:5])}",
                            "strength": len(common_tech) / max(len(node1.technologies), len(node2.technologies)),
                        }
                    )

        return relationships

    def generate_folder_structure_report(self):
        """Generate comprehensive folder structure report"""

        self.print_header("GENERATING STRUCTURE REPORT", Emojis.CHART)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"FOLDER_STRUCTURE_ANALYSIS_{timestamp}.md"
        json_file = self.target_dir / f"FOLDER_STRUCTURE_DATA_{timestamp}.json"

        with open(report_file, "w") as f:
            f.write("# 🌳 CONTENT-AWARE FOLDER STRUCTURE ANALYSIS\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 EXECUTIVE SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Folders | {self.stats['total_folders']:,} |\n")
            f.write(f"| Total Python Files | {self.stats['total_files']:,} |\n")
            f.write(f"| Maximum Depth | {self.stats['max_depth']} levels |\n")
            f.write(f"| Categories Found | {len(self.stats['categories_found'])} |\n\n")

            # Category Distribution
            f.write("## 🎯 CATEGORY DISTRIBUTION\n\n")
            for category, count in sorted(self.stats["categories_found"].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{category}**: {count} folders\n")
            f.write(Path("\n"))

            # Folder Hierarchy
            f.write("## 🌳 FOLDER HIERARCHY\n\n")
            self.write_tree_recursive(f, self.root_node, prefix="")

            # Detailed Folder Analysis
            f.write("\n## 📁 DETAILED FOLDER ANALYSIS\n\n")

            # Group by category
            for category, folders in sorted(self.category_folders.items()):
                if folders:
                    f.write(f"### {category.replace('_', ' ').title()}\n\n")

                    for folder in sorted(folders, key=lambda x: len(x.files), reverse=True)[:10]:
                        ancestry = " > ".join(folder.get_ancestry())
                        f.write(f"#### `{ancestry}`\n")
                        f.write(f"- **Purpose:** {folder.purpose or 'Unknown'}\n")
                        f.write(f"- **Files:** {len(folder.files)} ({folder.python_files} Python)\n")
                        f.write(f"- **Depth:** {folder.depth} levels\n")
                        f.write(f"- **Size:** {folder.total_size / CONSTANT_1024:.1f} KB\n")

                        if folder.technologies:
                            top_tech = list(folder.technologies)[:5]
                            f.write(f"- **Technologies:** {', '.join(top_tech)}\n")

                        if folder.avg_complexity > 0:
                            f.write(f"- **Avg Complexity:** {folder.avg_complexity:.1f}\n")

                        f.write(Path("\n"))

            # Recommendations
            f.write("## 💡 RECOMMENDATIONS\n\n")
            f.write("### Organization Suggestions\n\n")

            # Find folders that might need reorganization
            for category, folders in self.category_folders.items():
                if len(folders) > 5:
                    f.write(f"- Consider consolidating {len(folders)} `{category}` folders\n")

            f.write("\n### Folder Structure Improvements\n\n")

            # Find deeply nested folders
            deep_folders = [n for n in self.content_analyzer.all_nodes if n.depth > 4]
            if deep_folders:
                f.write(f"- {len(deep_folders)} folders are deeply nested (>4 levels)\n")
                f.write("  - Consider flattening the structure for better organization\n\n")

            # Find folders with many files
            large_folders = [n for n in self.content_analyzer.all_nodes if len(n.files) > 20]
            if large_folders:
                f.write(f"- {len(large_folders)} folders contain >20 files\n")
                f.write("  - Consider splitting into subcategories\n\n")

        # Save JSON data
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": dict(self.stats),
            "folders": [
                {
                    "path": str(node.path.relative_to(self.target_dir)),
                    "name": node.name,
                    "depth": node.depth,
                    "files": len(node.files),
                    "python_files": node.python_files,
                    "categories": list(node.categories),
                    "technologies": list(node.technologies)[:10],
                    "purpose": node.purpose,
                    "ancestry": node.get_ancestry(),
                }
                for node in self.content_analyzer.all_nodes
            ],
        }

        with open(json_file, "w") as f:
            json.dump(json_data, f, indent=2)

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Data: {json_file}{Colors.END}")

        return report_file, json_file

    def write_tree_recursive(self, f, node: FolderNode, prefix: str, is_last: bool = True):
        """Write tree structure recursively"""

        if node.parent:  # Skip root
            # Tree characters
            connector = "└── " if is_last else "├── "

            # Colorize based on content
            icon = Emojis.FOLDER
            info = f"({node.python_files} .py)" if node.python_files > 0 else ""

            categories = f" [{', '.join(list(node.categories)[:2])}]" if node.categories else ""

            f.write(f"{prefix}{connector}{icon} **{node.name}** {info}{categories}\n")

            # Update prefix for children
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension
        else:
            new_prefix = ""

        # Process children
        for i, child in enumerate(node.children):
            self.write_tree_recursive(f, child, new_prefix, i == len(node.children) - 1)

    def run(self):
        """Run complete analysis"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║         🌳 CONTENT-AWARE FOLDER STRUCTURE ANALYZER 🧠                        ║")
        print("║                                                                               ║")
        print("║     Deep Understanding of Parent Hierarchy and Content Relationships         ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}\n")

        # Build folder tree
        self.print_header("BUILDING FOLDER TREE", Emojis.TREE)
        self.build_folder_tree(self.target_dir, self.root_node)
        print(
            f"{Colors.GREEN}Built tree with {self.stats['total_folders']} folders, "
            f"{self.stats['max_depth']} levels deep{Colors.END}"
        )

        # Analyze folder content
        self.print_header("ANALYZING FOLDER CONTENT", Emojis.MICROSCOPE)
        for node in self.content_analyzer.all_nodes:
            self.analyze_folder_content(node)
        print(f"{Colors.GREEN}Analyzed {len(self.content_analyzer.all_nodes)} folders{Colors.END}")

        # Analyze relationships
        relationships = self.analyze_relationships()
        print(f"{Colors.GREEN}Found {len(relationships)} folder relationships{Colors.END}")

        # Generate report
        report_file, json_file = self.generate_folder_structure_report()

        # Final summary
        self.print_header("ANALYSIS COMPLETE!", Emojis.ROCKET)

        logger.info(f"{Colors.BOLD}📊 FINAL STATS:{Colors.END}\n")
        print(f"  {Emojis.FOLDER} Folders: {Colors.CYAN}{self.stats['total_folders']:,}{Colors.END}")
        print(f"  {Emojis.FILE} Python Files: {Colors.CYAN}{self.stats['total_files']:,}{Colors.END}")
        print(f"  {Emojis.TREE} Max Depth: {Colors.CYAN}{self.stats['max_depth']}{Colors.END}")
        print(f"  {Emojis.TARGET} Categories: {Colors.CYAN}{len(self.stats['categories_found'])}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}🎯 TOP CATEGORIES:{Colors.END}\n")
        for category, count in sorted(self.stats["categories_found"].items(), key=lambda x: x[1], reverse=True)[:5]:
            logger.info(f"  {Colors.CYAN}{category}{Colors.END}: {count} folders")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Content-aware folder structure analysis")
    parser.add_argument(
        "--target",
        type=str,
        default=Path(str(Path.home()) + "/GitHub/AvaTarArTs-Suite"),
        help="Target directory to analyze",
    )
    parser.add_argument("--depth", type=int, default=6, help="Maximum folder depth to scan (default: 6)")
    args = parser.parse_args()

    analyzer = ParentFolderStructureAnalyzer(args.target)
    analyzer.max_depth = args.depth
    analyzer.run()


if __name__ == "__main__":
    main()
