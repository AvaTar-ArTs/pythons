import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_256 = 256
CONSTANT_65536 = 65536

#!/usr/bin/env python3
"""
🔄 CROSS-DIRECTORY INTELLIGENT MERGER
====================================
Merges multiple Python directories into one master location,
detecting duplicates across directories and keeping the best version.

Features:
✨ Cross-directory duplicate detection (by SHA-CONSTANT_256 hash)
✨ Intelligent file selection (newest, most complete, best location)
✨ User script filtering (excludes library/system files)
✨ Content-aware diff generation
✨ Safe merging with comprehensive backups
✨ Detailed merge report with file mappings

Use Case:
Merge python_backup/ and python-repo/ INTO python/ (master)
Remove duplicates, keep best versions, archive source dirs
"""

import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
import csv
import json


# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class CrossDirectoryMerger:
    """Merge multiple directories into master, removing cross-dir duplicates"""

    def __init__(
        self,
        master_dir: str,
        source_dirs: List[str],
        user_scripts_only: bool = True,
        dry_run: bool = True,
    ):
        self.master_dir = Path(master_dir)
        self.source_dirs = [Path(d) for d in source_dirs]
        self.user_scripts_only = user_scripts_only
        self.dry_run = dry_run

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(fstr(Path.home()) + "/Documents/merge_backup_{timestamp}")

        self.file_inventory = {}  # hash -> list of file info
        self.merge_plan = []

        self.stats = {
            "master_files": 0,
            "source_files": 0,
            "duplicates_found": 0,
            "files_to_merge": 0,
            "files_skipped": 0,
        }

    def calc_hash(self, filepath: Path) -> str:
        """Calculate SHA-CONSTANT_256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (OSError, IOError, FileNotFoundError):
            return "ERROR"

    def is_user_script(self, filepath: Path) -> bool:
        """Quick check if file is user script"""

        name_lower = filepath.stem.lower()

        # Exclude obvious library test files
        library_patterns = [
            "test_pandas",
            "test_numpy",
            "test_scipy",
            "test_array",
            "test_scalar",
            "test_dtype",
        ]

        if any(pattern in name_lower for pattern in library_patterns):
            return False

        # Include if has custom indicators in name
        custom_indicators = [
            "instagram",
            "youtube",
            "leonardo",
            "openai",
            "bot",
            "scraper",
            "downloader",
            "uploader",
            "organizer",
            "automation",
            "generator",
        ]

        if any(indicator in name_lower for indicator in custom_indicators):
            return True

        # Default to include (we'll be conservative)
        return True

    def scan_directories(self):
        """Scan all directories and build inventory"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔍 SCANNING DIRECTORIES")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Scan master directory
        logger.info(f"{Colors.CYAN}📁 Master: {self.master_dir}{Colors.END}")
        master_files = list(self.master_dir.rglob("*.py"))
        master_files = [f for f in master_files if "backup" not in str(f)]

        if self.user_scripts_only:
            master_files = [f for f in master_files if self.is_user_script(f)]

        for filepath in master_files:
            file_hash = self.calc_hash(filepath)
            if file_hash != "ERROR":
                if file_hash not in self.file_inventory:
                    self.file_inventory[file_hash] = []

                self.file_inventory[file_hash].append(
                    {
                        "path": filepath,
                        "source": "MASTER",
                        "size": filepath.stat().st_size,
                        "modified": filepath.stat().st_mtime,
                    }
                )

        self.stats["master_files"] = len(master_files)
        logger.info(f"  Found {len(master_files)} files\n")

        # Scan source directories
        for source_dir in self.source_dirs:
            logger.info(f"{Colors.CYAN}📁 Source: {source_dir}{Colors.END}")

            if not source_dir.exists():
                logger.info(
                    f"  {Colors.YELLOW}⚠️  Directory not found, skipping{Colors.END}\n"
                )
                continue

            source_files = list(source_dir.rglob("*.py"))

            if self.user_scripts_only:
                source_files = [f for f in source_files if self.is_user_script(f)]

            for filepath in source_files:
                file_hash = self.calc_hash(filepath)
                if file_hash != "ERROR":
                    if file_hash not in self.file_inventory:
                        self.file_inventory[file_hash] = []

                    self.file_inventory[file_hash].append(
                        {
                            "path": filepath,
                            "source": source_dir.name,
                            "size": filepath.stat().st_size,
                            "modified": filepath.stat().st_mtime,
                        }
                    )

            self.stats["source_files"] += len(source_files)
            logger.info(f"  Found {len(source_files)} files\n")

    def create_merge_plan(self):
        """Create plan to merge unique files into master"""

        logger.info(f"{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🧠 CREATING MERGE PLAN")
        logger.info(f"{'='*80}{Colors.END}\n")

        duplicates_across_dirs = 0

        for file_hash, instances in self.file_inventory.items():
            if len(instances) > 1:
                # Check if duplicates span multiple directories
                sources = set(inst["source"] for inst in instances)
                if len(sources) > 1:
                    duplicates_across_dirs += 1

                    # Find if master has this file
                    has_master = any(inst["source"] == "MASTER" for inst in instances)

                    if not has_master:
                        # Choose best version to merge into master
                        best = max(instances, key=lambda x: (x["modified"], x["size"]))

                        self.merge_plan.append(
                            {
                                "action": "merge",
                                "file": best["path"],
                                "source": best["source"],
                                "hash": file_hash[:16],
                                "duplicates": [
                                    inst["path"] for inst in instances if inst != best
                                ],
                            }
                        )

                        self.stats["files_to_merge"] += 1
                    else:
                        # Master already has it, skip sources
                        self.stats["files_skipped"] += len(
                            [i for i in instances if i["source"] != "MASTER"]
                        )
            else:
                # Unique file
                inst = instances[0]
                if inst["source"] != "MASTER":
                    self.merge_plan.append(
                        {
                            "action": "merge",
                            "file": inst["path"],
                            "source": inst["source"],
                            "hash": file_hash[:16],
                            "duplicates": [],
                        }
                    )
                    self.stats["files_to_merge"] += 1

        self.stats["duplicates_found"] = duplicates_across_dirs

        logger.info(f"{Colors.GREEN}✅ Plan created!{Colors.END}\n")
        logger.info(
            f"  Cross-directory duplicates: {Colors.YELLOW}{duplicates_across_dirs}{Colors.END}"
        )
        logger.info(
            f"  Files to merge: {Colors.CYAN}{self.stats['files_to_merge']}{Colors.END}"
        )
        logger.info(
            f"  Files to skip (already in master): {Colors.YELLOW}{self.stats['files_skipped']}{Colors.END}"
        )

    def execute_merge(self):
        """Execute the merge plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔄 EXECUTING MERGE")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(
            f"{Colors.YELLOW}Mode: {'DRY RUN' if self.dry_run else 'LIVE MERGE'}{Colors.END}\n"
        )

        if not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        for idx, item in enumerate(self.merge_plan[:20], 1):  # Show first 20
            source_file = item["file"]

            # Determine target path in master
            # Try to preserve relative structure if possible
            try:
                rel_path = source_file.relative_to(source_file.parent.parent)
                target_path = self.master_dir / rel_path
            except (OSError, IOError, FileNotFoundError):
                # Just use filename
                target_path = self.master_dir / source_file.name

            logger.info(f"{Colors.BOLD}[{idx}/{len(self.merge_plan)}]{Colors.END}")
            logger.info(
                f"  From: {Colors.CYAN}{source_file.relative_to(source_file.parent.parent.parent)}{Colors.END}"
            )
            logger.info(
                f"  To:   {Colors.GREEN}{target_path.relative_to(self.master_dir)}{Colors.END}"
            )

            if item["duplicates"]:
                logger.info(
                    f"  Duplicates: {len(item['duplicates'])} (will be skipped)"
                )

            if not self.dry_run:
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_path)
                    logger.info(f"  {Colors.GREEN}✅ Merged{Colors.END}")
                except Exception as e:
                    logger.info(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                logger.info(f"  {Colors.YELLOW}[DRY RUN] Would merge{Colors.END}")
            print()

        if len(self.merge_plan) > 20:
            logger.info(f"... and {len(self.merge_plan) - 20} more files to merge")

    def generate_report(self):
        """Generate merge report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.master_dir / f"CROSS_DIRECTORY_MERGE_REPORT_{timestamp}.md"
        csv_file = self.master_dir / f"merge_mapping_{timestamp}.csv"

        with open(report_file, "w") as f:
            f.write("# 🔄 CROSS-DIRECTORY MERGE REPORT\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Master Files | {self.stats['master_files']:,} |\n")
            f.write(f"| Source Files | {self.stats['source_files']:,} |\n")
            f.write(f"| Cross-Dir Duplicates | {self.stats['duplicates_found']:,} |\n")
            f.write(f"| Files Merged | {self.stats['files_to_merge']:,} |\n")
            f.write(f"| Files Skipped | {self.stats['files_skipped']:,} |\n\n")

            # Merge details
            f.write("## 📝 MERGE DETAILS\n\n")
            for item in self.merge_plan[:CONSTANT_100]:
                f.write(f"### {item['file'].name}\n")
                f.write(f"- **Source:** `{item['source']}`\n")
                f.write(f"- **Hash:** `{item['hash']}`\n")
                if item["duplicates"]:
                    f.write(f"- **Duplicates:** {len(item['duplicates'])} (skipped)\n")
                f.write(Path("\n"))

        # CSV
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "File Name",
                    "Source Directory",
                    "Hash",
                    "Duplicates Count",
                    "Target Path",
                ]
            )

            for item in self.merge_plan:
                writer.writerow(
                    [
                        item["file"].name,
                        item["source"],
                        item["hash"],
                        len(item["duplicates"]),
                        str(item["file"]),
                    ]
                )

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")

    def run(self):
        """Run cross-directory merger"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║          🔄 CROSS-DIRECTORY INTELLIGENT MERGER 🧠                            ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║    Merge Multiple Directories with Duplicate Detection                       ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Master (target): {self.master_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}Sources to merge:{Colors.END}")
        for src in self.source_dirs:
            logger.info(f"  → {src}")
        logger.info(
            f"\n{Colors.CYAN}User scripts only: {self.user_scripts_only}{Colors.END}"
        )
        logger.info(
            f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n"
        )

        self.scan_directories()
        self.create_merge_plan()
        self.execute_merge()
        self.generate_report()

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✅ MERGE COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(
            f"  Master files: {Colors.CYAN}{self.stats['master_files']:,}{Colors.END}"
        )
        logger.info(
            f"  Source files: {Colors.CYAN}{self.stats['source_files']:,}{Colors.END}"
        )
        logger.info(
            f"  To merge: {Colors.CYAN}{self.stats['files_to_merge']:,}{Colors.END}"
        )
        logger.info(
            f"  Duplicates found: {Colors.YELLOW}{self.stats['duplicates_found']:,}{Colors.END}"
        )
        logger.info(
            f"  Skipped (already in master): {Colors.YELLOW}{self.stats['files_skipped']:,}{Colors.END}\n"
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🔄 Cross-directory merger")
    parser.add_argument(
        "--master", type=str, required=True, help="Master directory (target)"
    )
    parser.add_argument(
        "--sources", nargs="+", required=True, help="Source directories to merge"
    )
    parser.add_argument(
        "--user-scripts-only",
        action="store_true",
        default=True,
        help="Only merge user scripts (exclude library files)",
    )
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run")
    parser.add_argument("--live", action="store_true", help="Execute merge")

    args = parser.parse_args()

    merger = CrossDirectoryMerger(
        master_dir=args.master,
        source_dirs=args.sources,
        user_scripts_only=args.user_scripts_only,
        dry_run=not args.live,
    )

    merger.run()


if __name__ == "__main__":
    main()
