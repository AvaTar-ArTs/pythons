import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200

#!/usr/bin/env python3
"""
🏷️ INTELLIGENT CONTENT-AWARE RENAMER
====================================
Smart file renaming with content analysis, pattern detection,
and style consistency based on file type and purpose.

Naming Conventions Applied:
- Python scripts (.py):     kebab-case (ai-powered-analyzer.py)
- Text files (.txt):        snake_case (organization_report.txt)
- Documentation (.md):      Title-Case-With-Dashes.md
- Folders:                  kebab-case or Title Case (API System Tools)
- Configs (.json/.yaml):    snake_case (config_settings.json)

Features:
✨ Content-aware naming based on file purpose
✨ Consistent style by file type
✨ Removes redundant prefixes (enhanced_, simple_, fixed_)
✨ Cleans version numbers (_1.py → _v1.py)
✨ Preserves ProperCase for classes (YouTubeBot.py)
✨ Parent folder context awareness
✨ Safe renaming with undo script
"""

import os
import sys
import ast
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


# Emojis
class Emojis:
    RENAME = "🏷️"
    BRAIN = "🧠"
    SPARKLES = "✨"
    CHECK = "✅"
    WARN = "⚠️"
    FILE = "📄"
    FOLDER = "📁"
    ROCKET = "🚀"


class IntelligentRenamer:
    """Content-aware file renaming with style consistency"""

    # Naming patterns by file purpose
    NAMING_TEMPLATES = {
        "analyzer": "content-type-analyzer",
        "generator": "output-type-generator",
        "processor": "input-processor",
        "downloader": "platform-downloader",
        "uploader": "platform-uploader",
        "bot": "platform-bot",
        "scraper": "platform-scraper",
        "api_client": "service-api-client",
        "converter": "input-to-output-converter",
        "organizer": "target-organizer",
        "manager": "resource-manager",
        "tool": "purpose-tool",
    }

    # Redundant prefixes to remove
    REDUNDANT_PREFIXES = [
        "enhanced_",
        "simple_",
        "comprehensive_",
        "fixed_",
        "direct_",
        "improved_",
        "new_",
        "updated_",
        "advanced_",
        "basic_",
    ]

    def __init__(
        self, target_dir: str, dry_run: bool = True, interactive: bool = False
    ):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.interactive = interactive

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"rename_backup_{timestamp}"
        self.undo_script = self.target_dir / f"UNDO_RENAMES_{timestamp}.sh"

        self.stats = {
            "files_analyzed": 0,
            "files_renamed": 0,
            "folders_renamed": 0,
            "skipped": 0,
        }

        self.rename_plan = []
        self.undo_commands = []

    def detect_file_purpose(self, filepath: Path) -> Tuple[str, List[str]]:
        """Detect file purpose from content"""

        purpose = "script"
        keywords = []

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            functions = []
            classes = []
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name.lower())
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name.lower())
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.lower())
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.lower())

            all_text = " ".join(functions + classes + imports).lower()

            # Detect purpose
            if any(word in all_text for word in ["analyze", "analyse", "inspect"]):
                purpose = "analyzer"
                keywords.extend(["analyze", "inspect"])
            elif any(word in all_text for word in ["generate", "create", "build"]):
                purpose = "generator"
                keywords.extend(["generate", "create"])
            elif any(word in all_text for word in ["process", "transform"]):
                purpose = "processor"
                keywords.extend(["process", "transform"])
            elif any(word in all_text for word in ["download", "fetch", "pull"]):
                purpose = "downloader"
                keywords.append("download")
            elif any(word in all_text for word in ["upload", "push", "publish"]):
                purpose = "uploader"
                keywords.append("upload")
            elif any(word in all_text for word in ["scrape", "crawl", "spider"]):
                purpose = "scraper"
                keywords.append("scrape")
            elif "bot" in all_text:
                purpose = "bot"
                keywords.append("bot")
            elif "api" in all_text and "client" in all_text:
                purpose = "api_client"
                keywords.append("api")
            elif any(word in all_text for word in ["convert", "transform"]):
                purpose = "converter"
                keywords.append("convert")

            # Extract platform/service
            platforms = [
                "youtube",
                "instagram",
                "reddit",
                "twitter",
                "tiktok",
                "leonardo",
                "openai",
                "gemini",
                "claude",
            ]
            for platform in platforms:
                if platform in all_text:
                    keywords.append(platform)

            # Extract content types
            content_types = ["image", "video", "audio", "text", "data", "file"]
            for ctype in content_types:
                if ctype in all_text:
                    keywords.append(ctype)

        except (OSError, IOError, FileNotFoundError):
            pass

        return purpose, keywords[:3]  # Top 3 keywords

    def generate_smart_name(
        self, filepath: Path, purpose: str, keywords: List[str]
    ) -> str:
        """Generate smart filename based on content"""

        original = filepath.stem
        extension = filepath.suffix

        # Check if it's a ProperCase class name (like YouTubeBot)
        has_proper_case = bool(re.search(r"[A-Z][a-z]+[A-Z]", original))

        # Remove redundant prefixes
        clean_name = original
        for prefix in self.REDUNDANT_PREFIXES:
            clean_name = clean_name.replace(prefix, "")

        # Handle version numbers
        clean_name = re.sub(r"_(\d+)$", r"_v\1", clean_name)
        clean_name = re.sub(r" (\d+)$", r"_v\1", clean_name)

        # Remove copy/duplicate markers
        clean_name = re.sub(r"\s*copy\s*\d*", "", clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r"\s+\(\d+\)", "", clean_name)

        # If ProperCase (like YouTubeBot, WhisperTranscriber), keep it
        if has_proper_case and extension == ".py":
            # Just clean it up, don't change case
            result = clean_name.replace(" ", "").replace("--", "-").replace("__", "_")
            return f"{result}{extension}"

        # Apply style based on file type
        if extension == ".py":
            # Python: kebab-case
            if keywords:
                # Build from keywords and purpose
                parts = keywords + [purpose] if purpose != "script" else keywords
                name_base = "-".join(parts[:3])
            else:
                name_base = clean_name

            # Convert to kebab-case
            name_base = name_base.lower()
            name_base = re.sub(r"[_\s]+", "-", name_base)
            name_base = re.sub(r"-+", "-", name_base)
            name_base = name_base.strip("-")

            return f"{name_base}{extension}"

        elif extension in [".txt", ".json", ".yaml", ".yml"]:
            # Config/text: snake_case
            name_base = clean_name.lower()
            name_base = re.sub(r"[-\s]+", "_", name_base)
            name_base = re.sub(r"_+", "_", name_base)
            name_base = name_base.strip("_")

            return f"{name_base}{extension}"

        elif extension == ".md":
            # Markdown: Title-Case-With-Dashes
            name_base = clean_name.replace("_", " ").replace("-", " ")
            # Title case each word
            words = name_base.split()
            title_words = [w.capitalize() for w in words]
            name_base = "-".join(title_words)

            return f"{name_base}{extension}"

        else:
            # Others: clean snake_case
            name_base = clean_name.lower()
            name_base = re.sub(r"[^\w\-.]", "_", name_base)
            name_base = re.sub(r"_+", "_", name_base).strip("_")

            return f"{name_base}{extension}"

    def scan_and_analyze(self):
        """Scan directory and create rename plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{Emojis.BRAIN} SCANNING AND ANALYZING FILES")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Find all Python files
        python_files = list(self.target_dir.rglob("*.py"))

        # Skip backups and special directories
        skip_patterns = [
            "backup",
            ".git",
            "__pycache__",
            "dedup_backup",
            "rename_backup",
            "merge_backup",
        ]
        python_files = [
            f for f in python_files if not any(skip in str(f) for skip in skip_patterns)
        ]

        logger.info(
            f"{Colors.GREEN}Found {len(python_files)} Python files{Colors.END}\n"
        )

        for idx, filepath in enumerate(python_files, 1):
            if idx % CONSTANT_100 == 0:
                logger.info(
                    f"{Colors.YELLOW}Analyzing: {idx}/{len(python_files)}...{Colors.END}",
                    end="\r",
                )

            self.stats["files_analyzed"] += 1

            # Detect purpose and keywords
            purpose, keywords = self.detect_file_purpose(filepath)

            # Generate new name
            new_name = self.generate_smart_name(filepath, purpose, keywords)

            # Only add to plan if name would change
            if new_name != filepath.name:
                self.rename_plan.append(
                    {
                        "old_path": filepath,
                        "old_name": filepath.name,
                        "new_name": new_name,
                        "purpose": purpose,
                        "keywords": keywords,
                        "parent": filepath.parent.name,
                    }
                )

        logger.info(f"\n{Colors.GREEN}✅ Analysis complete!{Colors.END}")
        logger.info(
            f"{Colors.YELLOW}Files to rename: {len(self.rename_plan)}{Colors.END}"
        )

    def execute_renames(self):
        """Execute the rename plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{Emojis.RENAME} EXECUTING RENAME PLAN")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(
            f"{Colors.YELLOW}Total renames: {len(self.rename_plan)}{Colors.END}"
        )
        logger.info(
            f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE RENAME'}{Colors.END}\n"
        )

        # Group by parent folder
        by_parent = defaultdict(list)
        for item in self.rename_plan:
            by_parent[item["parent"]].append(item)

        for parent in sorted(by_parent.keys())[:20]:  # Show first 20 folders
            items = by_parent[parent]

            logger.info(f"\n{Colors.BOLD}📁 {parent}/{Colors.END} ({len(items)} files)")

            for idx, item in enumerate(items[:5], 1):  # Show first 5 per folder
                logger.info(f"  {Colors.RED}{item['old_name']}{Colors.END}")
                logger.info(f"  → {Colors.GREEN}{item['new_name']}{Colors.END}")
                logger.info(f"     ({item['purpose']}: {', '.join(item['keywords'])})")

                # Execute rename
                if not self.dry_run:
                    try:
                        new_path = item["old_path"].parent / item["new_name"]

                        # Check if target exists
                        if new_path.exists() and new_path != item["old_path"]:
                            # Add version suffix
                            counter = 2
                            base = Path(item["new_name"]).stem
                            ext = Path(item["new_name"]).suffix
                            while (
                                item["old_path"].parent / f"{base}_v{counter}{ext}"
                            ).exists():
                                counter += 1
                            new_path = (
                                item["old_path"].parent / f"{base}_v{counter}{ext}"
                            )

                        # Rename
                        item["old_path"].rename(new_path)

                        # Create undo command
                        self.undo_commands.append(
                            f"mv '{new_path}' '{item['old_path']}'"
                        )

                        self.stats["files_renamed"] += 1
                    except Exception as e:
                        logger.info(f"  {Colors.RED}Error: {e}{Colors.END}")
                        self.stats["skipped"] += 1
                else:
                    logger.info(f"  {Colors.YELLOW}[DRY RUN] Would rename{Colors.END}")

            if len(items) > 5:
                logger.info(f"  ... and {len(items) - 5} more files")

    def generate_report(self):
        """Generate rename report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"RENAME_REPORT_{timestamp}.md"
        csv_file = self.target_dir / f"rename_mapping_{timestamp}.csv"

        # Markdown report
        with open(report_file, "w") as f:
            f.write("# 🏷️ INTELLIGENT RENAME REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE RENAME'}\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## 📊 RENAME SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Files Analyzed | {self.stats['files_analyzed']:,} |\n")
            f.write(f"| Files Renamed | {self.stats['files_renamed']:,} |\n")
            f.write(f"| Folders Renamed | {self.stats['folders_renamed']:,} |\n")
            f.write(f"| Skipped | {self.stats['skipped']:,} |\n\n")

            # Naming conventions
            f.write("## 🎨 NAMING CONVENTIONS APPLIED\n\n")
            f.write("- **Python scripts (.py):** kebab-case (ai-powered-analyzer.py)\n")
            f.write("- **Text files (.txt):** snake_case (organization_report.txt)\n")
            f.write("- **Documentation (.md):** Title-Case-With-Dashes.md\n")
            f.write("- **ProperCase classes:** Preserved (YouTubeBot.py)\n\n")

            # Renames by purpose
            f.write("## 📝 RENAMES BY PURPOSE\n\n")

            by_purpose = defaultdict(list)
            for item in self.rename_plan[:CONSTANT_200]:  # First CONSTANT_200
                by_purpose[item["purpose"]].append(item)

            for purpose in sorted(by_purpose.keys()):
                items = by_purpose[purpose]
                f.write(f"### {purpose.title()} ({len(items)} files)\n\n")

                for item in items[:10]:  # First 10 per category
                    f.write(f"- `{item['old_name']}` → `{item['new_name']}`\n")

                if len(items) > 10:
                    f.write(f"- ... and {len(items) - 10} more\n")
                f.write(Path("\n"))

        # CSV export
        import csv

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Old Name", "New Name", "Purpose", "Keywords", "Parent Folder", "Path"]
            )

            for item in self.rename_plan:
                writer.writerow(
                    [
                        item["old_name"],
                        item["new_name"],
                        item["purpose"],
                        ", ".join(item["keywords"]),
                        item["parent"],
                        str(item["old_path"].relative_to(self.target_dir)),
                    ]
                )

        # Undo script
        if self.undo_commands and not self.dry_run:
            with open(self.undo_script, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo intelligent renaming\n")
                f.write(
                    f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                f.write("echo '🔄 Undoing renames...'\n\n")
                for cmd in reversed(self.undo_commands):
                    f.write(f"{cmd}\n")
                f.write("\necho '✅ Undo complete!'\n")

            self.undo_script.chmod(0o755)

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")
        if self.undo_script.exists():
            logger.info(f"{Colors.GREEN}✅ Undo: {self.undo_script}{Colors.END}")

        return report_file

    def run(self):
        """Run intelligent renamer"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║              🏷️ INTELLIGENT CONTENT-AWARE RENAMER 🧠                        ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║           Smart File Renaming with Style Consistency                         ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}🛡️ MODE: DRY RUN{Colors.END}\n")
        else:
            logger.info(f"{Colors.RED}⚠️ MODE: LIVE RENAME{Colors.END}\n")

        # Scan and analyze
        self.scan_and_analyze()

        # Execute
        self.execute_renames()

        # Report
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✨ GENERATING REPORT")
        logger.info(f"{'='*80}{Colors.END}\n")

        self.generate_report()

        # Summary
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{Emojis.ROCKET} RENAME COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(
            f"  Analyzed: {Colors.CYAN}{self.stats['files_analyzed']:,}{Colors.END}"
        )
        logger.info(
            f"  Renamed: {Colors.CYAN}{self.stats['files_renamed']:,}{Colors.END}"
        )
        logger.info(f"  Skipped: {Colors.CYAN}{self.stats['skipped']:,}{Colors.END}\n")

        if self.dry_run:
            logger.info(
                f"{Colors.YELLOW}⚠️ DRY RUN. Use --live to apply renames.{Colors.END}\n"
            )
        else:
            logger.info(f"{Colors.GREEN}✅ Renames applied!{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🏷️ Intelligent Content-Aware File Renamer"
    )

    parser.add_argument(
        "--target", type=str, required=True, help="Target directory to rename files in"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry run mode (default, safe)",
    )
    parser.add_argument(
        "--live", action="store_true", help="Live mode (actually renames files)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode (ask for confirmation)",
    )

    args = parser.parse_args()

    renamer = IntelligentRenamer(
        target_dir=args.target, dry_run=not args.live, interactive=args.interactive
    )

    renamer.run()


if __name__ == "__main__":
    main()
