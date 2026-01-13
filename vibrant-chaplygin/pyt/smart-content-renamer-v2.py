#!/usr/bin/env python3
"""
🏷️ SMART CONTENT-AWARE RENAMER V2
==================================
Intelligent file renaming that preserves meaning while applying
consistent style conventions based on file type.

Style Guide (Based on User Preferences):
- .py files:       kebab-case (ai-powered-analyzer.py, youtube-downloader.py)
- .txt files:      snake_case (file_organization_report.txt)
- .md files:       Title-Case-Dashes (API-System-Guide.md)
- ProperCase:      Preserved for class files (YouTubeBot.py, WhisperTranscriber.py)
- Folders:         kebab-case or spaces (api-tools, API System GUIDES)

Improvements:
✨ Preserves meaningful parts of original names
✨ Removes only truly redundant prefixes
✨ Cleans version numbers properly
✨ Handles special cases intelligently
✨ Parent folder context awareness
"""

import os
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import csv


# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class SmartRenamer:
    """Intelligent content-aware renaming"""

    # Only remove TRULY redundant prefixes
    REDUNDANT_WORDS = {
        "enhanced_",
        "simple_",
        "basic_",
        "new_",
        "old_",
        "fixed_",
        "temp_",
        "tmp_",
        "test_",
        "demo_",
    }

    def __init__(self, target_dir: str, dry_run: bool = True):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.undo_script = self.target_dir / f"UNDO_SMART_RENAME_{timestamp}.sh"

        self.stats = {
            "analyzed": 0,
            "renamed": 0,
            "skipped": 0,
        }

        self.rename_plan = []
        self.undo_commands = []

    def extract_meaningful_parts(self, filename: str) -> List[str]:
        """Extract meaningful parts from filename"""

        # Remove extension
        name = Path(filename).stem

        # Split by underscores, dashes, camelCase
        # First handle camelCase
        name = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)

        # Split by separators
        parts = re.split(r"[_\-\s]+", name.lower())

        # Remove redundant words
        meaningful = []
        for part in parts:
            # Skip if it's a pure redundant prefix
            if part + "_" in self.REDUNDANT_WORDS:
                continue
            # Skip pure numbers (timestamps)
            if part.isdigit() and len(part) >= 8:
                continue
            # Skip very short parts (unless important)
            if len(part) < 2 and part not in ["ai", "ml", "ui", "ux", "db"]:
                continue
            # Skip copy/version markers
            if part in ["copy", "bak", "tmp", "temp"]:
                continue

            meaningful.append(part)

        return meaningful

    def generate_python_name(self, filepath: Path, original_stem: str) -> str:
        """Generate kebab-case Python filename"""

        # Check for ProperCase (class-based files like YouTubeBot, WhisperTranscriber)
        if re.search(r"^[A-Z][a-z]+[A-Z]", original_stem):
            # Keep ProperCase, just clean up
            clean = re.sub(r"[_\s-]+", "", original_stem)
            # Handle version numbers
            clean = re.sub(r"(\d+)$", r"_v\1", clean)
            return f"{clean}.py"

        # Extract meaningful parts
        parts = self.extract_meaningful_parts(filepath.name)

        # If we have good parts, use them
        if parts:
            name_base = "-".join(parts[:4])  # Max 4 parts for readability
        else:
            # Fall back to cleaned original
            name_base = original_stem.lower()

        # Clean up
        name_base = re.sub(r"[^\w\-]", "-", name_base)
        name_base = re.sub(r"-+", "-", name_base)
        name_base = name_base.strip("-")

        # Handle version numbers at end
        name_base = re.sub(r"-(\d{8,})$", "", name_base)  # Remove timestamps
        name_base = re.sub(r"-v?(\d+)$", r"-v\1", name_base)  # Standardize versions

        return f"{name_base}.py"

    def generate_text_name(self, filepath: Path, original_stem: str) -> str:
        """Generate snake_case text filename"""

        parts = self.extract_meaningful_parts(filepath.name)

        if parts:
            name_base = "_".join(parts[:4])
        else:
            name_base = original_stem.lower()

        # Clean up
        name_base = re.sub(r"[^\w_]", "_", name_base)
        name_base = re.sub(r"_+", "_", name_base)
        name_base = name_base.strip("_")

        return f"{name_base}.txt"

    def generate_markdown_name(self, filepath: Path, original_stem: str) -> str:
        """Generate Title-Case-Dashes markdown filename"""

        parts = self.extract_meaningful_parts(filepath.name)

        if parts:
            # Title case each part
            title_parts = [p.capitalize() for p in parts[:4]]
            name_base = "-".join(title_parts)
        else:
            # Clean original
            name_base = original_stem.replace("_", "-").replace(" ", "-")
            words = name_base.split("-")
            name_base = "-".join([w.capitalize() for w in words if w])

        return f"{name_base}.md"

    def generate_smart_name(self, filepath: Path) -> Optional[str]:
        """Generate smart name based on file type and content"""

        original_stem = filepath.stem
        extension = filepath.suffix

        # Skip if already well-named (no weird characters, reasonable length)
        if (
            len(original_stem) < 50
            and not re.search(r"[\(\)\[\]]", original_stem)
            and not re.search(r"\s\d+$", original_stem)
            and "copy" not in original_stem.lower()
            and original_stem.count("_") < 5
            and not original_stem.endswith(("--", "__"))
        ):
            return None

        # Generate based on type
        if extension == ".py":
            new_name = self.generate_python_name(filepath, original_stem)
        elif extension == ".txt":
            new_name = self.generate_text_name(filepath, original_stem)
        elif extension == ".md":
            new_name = self.generate_markdown_name(filepath, original_stem)
        else:
            # Default: snake_case
            parts = self.extract_meaningful_parts(filepath.name)
            if parts:
                new_name = f"{'_'.join(parts[:4])}{extension}"
            else:
                return None

        # Don't rename if it's the same
        if new_name == filepath.name:
            return None

        return new_name

    def scan_files(self):
        """Scan and create rename plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔍 SCANNING FILES")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Find Python and text files
        files_to_check = []
        files_to_check.extend(self.target_dir.rglob("*.py"))
        files_to_check.extend(self.target_dir.rglob("*.txt"))
        files_to_check.extend(self.target_dir.rglob("*.md"))

        # Skip backups
        skip_patterns = [
            "backup",
            ".git",
            "__pycache__",
            "dedup_backup",
            "rename_backup",
            "merge_backup",
            "bare_except_backup",
        ]
        files_to_check = [
            f
            for f in files_to_check
            if not any(skip in str(f) for skip in skip_patterns)
        ]

        logger.info(
            f"{Colors.GREEN}Checking {len(files_to_check)} files...{Colors.END}\n"
        )

        for idx, filepath in enumerate(files_to_check, 1):
            if idx % CONSTANT_200 == 0:
                logger.info(
                    f"{Colors.YELLOW}Progress: {idx}/{len(files_to_check)}...{Colors.END}",
                    end="\r",
                )

            self.stats["analyzed"] += 1

            new_name = self.generate_smart_name(filepath)

            if new_name:
                self.rename_plan.append(
                    {
                        "old_path": filepath,
                        "old_name": filepath.name,
                        "new_name": new_name,
                        "parent": filepath.parent.name,
                        "ext": filepath.suffix,
                    }
                )

        logger.info(
            f"\n{Colors.GREEN}✅ Found {len(self.rename_plan)} files to rename{Colors.END}"
        )

    def execute_renames(self):
        """Execute rename plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🏷️ EXECUTING RENAMES")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.YELLOW}Total: {len(self.rename_plan)}{Colors.END}")
        logger.info(
            f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n"
        )

        # Group by extension
        by_ext = defaultdict(list)
        for item in self.rename_plan:
            by_ext[item["ext"]].append(item)

        for ext in sorted(by_ext.keys()):
            items = by_ext[ext]
            logger.info(
                f"\n{Colors.BOLD}{ext} files ({len(items)} renames){Colors.END}"
            )

            for item in items[:10]:  # Show first 10 per type
                logger.info(f"  {Colors.RED}{item['old_name']}{Colors.END}")
                logger.info(f"  → {Colors.GREEN}{item['new_name']}{Colors.END}")

                if not self.dry_run:
                    try:
                        new_path = item["old_path"].parent / item["new_name"]

                        # Handle collision
                        if new_path.exists() and new_path != item["old_path"]:
                            counter = 2
                            base = Path(item["new_name"]).stem
                            ext_name = Path(item["new_name"]).suffix
                            while (
                                item["old_path"].parent / f"{base}-v{counter}{ext_name}"
                            ).exists():
                                counter += 1
                            new_path = (
                                item["old_path"].parent / f"{base}-v{counter}{ext_name}"
                            )

                        item["old_path"].rename(new_path)

                        self.undo_commands.append(
                            f"mv '{new_path}' '{item['old_path']}'"
                        )
                        self.stats["renamed"] += 1
                    except Exception as e:
                        logger.info(f"  {Colors.RED}Error: {e}{Colors.END}")
                        self.stats["skipped"] += 1

            if len(items) > 10:
                logger.info(f"  ... and {len(items) - 10} more")

    def generate_report(self):
        """Generate renaming report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"SMART_RENAME_REPORT_{timestamp}.md"
        csv_file = self.target_dir / f"rename_mapping_{timestamp}.csv"

        # Markdown
        with open(report_file, "w") as f:
            f.write("# 🏷️ SMART RENAME REPORT\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Analyzed | {self.stats['analyzed']:,} |\n")
            f.write(f"| Renamed | {self.stats['renamed']:,} |\n")
            f.write(f"| Skipped | {self.stats['skipped']:,} |\n\n")

            # Style guide
            f.write("## 🎨 NAMING CONVENTIONS\n\n")
            f.write("- Python (.py): kebab-case\n")
            f.write("- Text (.txt): snake_case\n")
            f.write("- Markdown (.md): Title-Case-Dashes\n")
            f.write("- ProperCase: Preserved for class files\n\n")

            # Examples
            f.write("## 📝 EXAMPLES\n\n")
            by_ext = defaultdict(list)
            for item in self.rename_plan[:CONSTANT_100]:
                by_ext[item["ext"]].append(item)

            for ext, items in sorted(by_ext.items()):
                f.write(f"### {ext} Files\n\n")
                for item in items[:15]:
                    f.write(f"- `{item['old_name']}` → `{item['new_name']}`\n")
                f.write(Path("\n"))

        # CSV
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Old Name", "New Name", "Extension", "Parent Folder", "Path"]
            )

            for item in self.rename_plan:
                writer.writerow(
                    [
                        item["old_name"],
                        item["new_name"],
                        item["ext"],
                        item["parent"],
                        str(item["old_path"].relative_to(self.target_dir)),
                    ]
                )

        # Undo script
        if self.undo_commands and not self.dry_run:
            with open(self.undo_script, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo smart renaming\n\n")
                for cmd in reversed(self.undo_commands):
                    f.write(f"{cmd}\n")
            self.undo_script.chmod(0o755)

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")

    def run(self):
        """Run smart renamer"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║              🏷️ SMART CONTENT-AWARE RENAMER V2 🧠                           ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║         Intelligent Naming with Style Consistency                            ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")
        logger.info(
            f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n"
        )

        self.scan_files()
        self.execute_renames()
        self.generate_report()

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✅ COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(f"  Analyzed: {Colors.CYAN}{self.stats['analyzed']:,}{Colors.END}")
        logger.info(f"  Renamed: {Colors.CYAN}{self.stats['renamed']:,}{Colors.END}")
        logger.info(f"  Skipped: {Colors.CYAN}{self.stats['skipped']:,}{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🏷️ Smart Content-Aware Renamer")
    parser.add_argument("--target", type=str, required=True, help="Target directory")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run")
    parser.add_argument("--live", action="store_true", help="Apply renames")

    args = parser.parse_args()

    renamer = SmartRenamer(args.target, dry_run=not args.live)
    renamer.run()


if __name__ == "__main__":
    main()
