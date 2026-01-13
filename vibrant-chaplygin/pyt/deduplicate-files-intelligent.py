import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_256 = 256
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_65536 = 65536

#!/usr/bin/env python3
"""
🧹 INTELLIGENT DUPLICATE REMOVER
================================
Content-aware duplicate detection and removal with parent folder intelligence.

Features:
✨ SHA-CONSTANT_256 hash-based exact duplicate detection
✨ Semantic similarity detection (AST-based)
✨ Parent folder context awareness
✨ Smart decision making (keep newest, most complete, best location)
✨ Safe removal with comprehensive backups
✨ Detailed removal report with undo script
"""

import os
import sys
import ast
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any, Set


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
    TRASH = "🗑️"
    SHIELD = "🛡️"
    BRAIN = "🧠"
    CHECK = "✅"
    WARN = "⚠️"
    FOLDER = "📁"
    FILE = "📄"
    ROCKET = "🚀"
    SPARKLES = "✨"
    TARGET = "🎯"


class IntelligentDeduplicator:
    """Smart duplicate detection and removal"""

    def __init__(self, target_dir: str, dry_run: bool = True, interactive: bool = True):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.interactive = interactive

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"dedup_backup_{timestamp}"
        self.report_dir = self.target_dir / f"dedup_reports_{timestamp}"

        self.file_inventory: Dict[str, Dict] = {}
        self.hash_to_files: Dict[str, List[Path]] = defaultdict(list)
        self.semantic_groups: Dict[str, List[Path]] = defaultdict(list)

        self.stats = {
            "total_files": 0,
            "exact_duplicates": 0,
            "semantic_duplicates": 0,
            "files_removed": 0,
            "space_saved": 0,
            "groups_processed": 0,
        }

        self.removal_plan: List[Dict] = []
        self.kept_files: List[Path] = []
        self.undo_commands: List[str] = []

    def print_header(self, text: str, emoji=""):
        """Print fancy header"""
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA-CONSTANT_256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def analyze_python_file(self, filepath: Path) -> Dict[str, Any]:
        """Deep file analysis"""
        analysis = {
            "path": str(filepath),
            "size": 0,
            "modified": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "loc": 0,
            "has_docstring": False,
            "complexity": 0,
            "parent_folder": str(filepath.parent.name),
            "depth": len(filepath.relative_to(self.target_dir).parts) - 1,
        }

        try:
            stat = filepath.stat()
            analysis["size"] = stat.st_size
            analysis["modified"] = stat.st_mtime

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                analysis["loc"] = len(content.splitlines())

            # AST analysis
            tree = ast.parse(content)
            analysis["has_docstring"] = bool(ast.get_docstring(tree))

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

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def get_semantic_signature(self, analysis: Dict) -> str:
        """Create semantic signature for similarity detection"""
        functions = sorted(analysis.get("functions", []))
        classes = sorted(analysis.get("classes", []))
        imports = sorted(analysis.get("imports", []))

        return f"F:{','.join(functions[:15])}|C:{','.join(classes[:10])}|I:{','.join(imports[:15])}"

    def scan_codebase(self):
        """Scan codebase and build inventory"""

        self.print_header("SCANNING FOR DUPLICATES", Emojis.FOLDER)

        python_files = list(self.target_dir.rglob("*.py"))

        # Skip certain directories
        skip_patterns = [
            "dedup_backup_",
            "dedup_reports_",
            "merge_backup_",
            "merge_analysis_",
            ".git",
            "__pycache__",
        ]

        python_files = [
            f for f in python_files if not any(skip in str(f) for skip in skip_patterns)
        ]

        self.stats["total_files"] = len(python_files)
        logger.info(
            f"{Colors.GREEN}Found {len(python_files)} Python files{Colors.END}\n"
        )

        # Analyze each file
        for idx, filepath in enumerate(python_files, 1):
            if idx % 50 == 0:
                logger.info(
                    f"{Colors.YELLOW}Analyzing: {idx}/{len(python_files)}...{Colors.END}",
                    end="\r",
                )

            try:
                # Calculate hash
                file_hash = self.calculate_hash(filepath)
                self.hash_to_files[file_hash].append(filepath)

                # Deep analysis
                analysis = self.analyze_python_file(filepath)
                self.file_inventory[str(filepath)] = analysis

                # Semantic grouping
                if not file_hash.startswith("ERROR"):
                    semantic_sig = self.get_semantic_signature(analysis)
                    if semantic_sig:
                        self.semantic_groups[semantic_sig].append(filepath)

            except Exception as e:
                logger.info(f"{Colors.RED}Error analyzing {filepath}: {e}{Colors.END}")

        logger.info(f"\n{Colors.GREEN}{Emojis.CHECK} Scan complete!{Colors.END}")

    def choose_best_file(self, files: List[Path]) -> Tuple[Path, List[Path]]:
        """Choose which file to keep from duplicates"""

        # Score each file
        scored_files = []

        for filepath in files:
            analysis = self.file_inventory.get(str(filepath), {})

            score = 0
            reasons = []

            # Prefer more recent files
            if analysis.get("modified", 0) > 0:
                score += 10

            # Prefer files with docstrings
            if analysis.get("has_docstring"):
                score += 5
                reasons.append("has docstring")

            # Prefer more complex (feature-rich) files
            complexity = analysis.get("complexity", 0)
            if complexity > 0:
                score += min(complexity, 20)
                if complexity > 10:
                    reasons.append(f"complex ({complexity} nodes)")

            # Prefer larger files (usually more complete)
            size = analysis.get("size", 0)
            if size > 0:
                score += min(size / CONSTANT_1000, 10)

            # Prefer files in better locations (not in archived, test, or temp folders)
            path_lower = str(filepath).lower()
            if "archive" in path_lower or "old" in path_lower:
                score -= 20
                reasons.append("in archive folder")
            elif "test" in path_lower:
                score -= 5
            elif "backup" in path_lower:
                score -= 15
                reasons.append("in backup folder")

            # Prefer shallow depth
            depth = analysis.get("depth", 0)
            score -= depth

            # Bonus for being in core, automation, or media folders
            if any(
                folder in path_lower for folder in ["core/", "automation/", "media/"]
            ):
                score += 10
                reasons.append("in primary folder")

            scored_files.append(
                {
                    "path": filepath,
                    "score": score,
                    "analysis": analysis,
                    "reasons": reasons,
                }
            )

        # Sort by score (highest first)
        scored_files.sort(
            key=lambda x: (x["score"], x["analysis"].get("modified", 0)), reverse=True
        )

        best = scored_files[0]["path"]
        to_remove = [item["path"] for item in scored_files[1:]]

        return best, to_remove

    def create_removal_plan(self):
        """Create intelligent removal plan"""

        self.print_header("CREATING REMOVAL PLAN", Emojis.BRAIN)

        # Process exact duplicates
        exact_dupes = {
            h: files
            for h, files in self.hash_to_files.items()
            if len(files) > 1 and not h.startswith("ERROR")
        }

        self.stats["exact_duplicates"] = len(exact_dupes)

        logger.info(
            f"{Colors.CYAN}Exact duplicate groups: {len(exact_dupes)}{Colors.END}"
        )

        for file_hash, files in exact_dupes.items():
            self.stats["groups_processed"] += 1

            # Choose best file
            keep_file, remove_files = self.choose_best_file(files)

            for remove_file in remove_files:
                remove_analysis = self.file_inventory.get(str(remove_file), {})
                keep_analysis = self.file_inventory.get(str(keep_file), {})

                self.removal_plan.append(
                    {
                        "type": "exact_duplicate",
                        "remove": remove_file,
                        "keep": keep_file,
                        "hash": file_hash[:16],
                        "size": remove_analysis.get("size", 0),
                        "remove_parent": remove_analysis.get(
                            "parent_folder", "unknown"
                        ),
                        "keep_parent": keep_analysis.get("parent_folder", "unknown"),
                        "reason": f"Exact duplicate of {keep_file.name}",
                    }
                )

                self.stats["files_removed"] += 1
                self.stats["space_saved"] += remove_analysis.get("size", 0)

            self.kept_files.append(keep_file)

        # Process semantic duplicates (same structure/function but different content)
        semantic_dupes = {
            sig: files for sig, files in self.semantic_groups.items() if len(files) > 1
        }

        self.stats["semantic_duplicates"] = len(semantic_dupes)

        logger.info(
            f"{Colors.CYAN}Semantic duplicate groups: {len(semantic_dupes)}{Colors.END}"
        )
        logger.info(
            f"{Colors.YELLOW}Total files to remove: {self.stats['files_removed']}{Colors.END}"
        )
        logger.info(
            f"{Colors.GREEN}Space to save: {self.stats['space_saved'] / CONSTANT_1024 / CONSTANT_1024:.2f} MB{Colors.END}"
        )

    def execute_removal(self):
        """Execute the removal plan"""

        self.print_header("EXECUTING REMOVAL PLAN", Emojis.TRASH)

        logger.info(
            f"{Colors.YELLOW}Total files to remove: {len(self.removal_plan)}{Colors.END}"
        )
        logger.info(
            f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE REMOVAL'}{Colors.END}\n"
        )

        # Create backup directory
        if not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        for idx, item in enumerate(self.removal_plan, 1):
            remove_file = item["remove"]
            keep_file = item["keep"]

            logger.info(f"\n{Colors.BOLD}[{idx}/{len(self.removal_plan)}]{Colors.END}")
            logger.info(
                f"{Colors.RED}Remove: {remove_file.relative_to(self.target_dir)}{Colors.END}"
            )
            logger.info(f"  Parent: {Colors.CYAN}{item['remove_parent']}{Colors.END}")
            logger.info(
                f"{Colors.GREEN}Keep:   {keep_file.relative_to(self.target_dir)}{Colors.END}"
            )
            logger.info(f"  Parent: {Colors.CYAN}{item['keep_parent']}{Colors.END}")
            logger.info(f"  Reason: {item['reason']}")
            logger.info(f"  Size: {item['size']:,} bytes")

            # Interactive confirmation for uncertain cases
            if self.interactive:
                # Auto-approve obvious cases
                if (
                    "backup" in str(remove_file).lower()
                    or "archive" in str(remove_file).lower()
                ):
                    proceed = True
                else:
                    logger.info(f"\n{Colors.CYAN}Proceed? [y/n/q]{Colors.END} ", end="")
                    choice = input().lower().strip()

                    if choice == "q":
                        logger.info(f"{Colors.YELLOW}Removal aborted{Colors.END}")
                        return
                    proceed = choice == "y"

                if not proceed:
                    logger.info(f"{Colors.YELLOW}Skipped{Colors.END}")
                    continue

            # Execute removal
            try:
                if not self.dry_run:
                    # Backup before removal
                    backup_path = self.backup_dir / remove_file.relative_to(
                        self.target_dir
                    )
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(remove_file, backup_path)

                    # Create undo command
                    self.undo_commands.append(f"cp '{backup_path}' '{remove_file}'")

                    # Remove file
                    remove_file.unlink()
                    logger.info(f"{Colors.GREEN}{Emojis.CHECK} Removed{Colors.END}")
                else:
                    logger.info(f"{Colors.YELLOW}[DRY RUN] Would remove{Colors.END}")

            except Exception as e:
                logger.info(f"{Colors.RED}{Emojis.WARN} Error: {e}{Colors.END}")

    def generate_report(self):
        """Generate comprehensive deduplication report"""

        self.print_header("GENERATING REPORT", Emojis.SPARKLES)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"DEDUP_REPORT_{timestamp}.md"
        json_file = self.target_dir / f"DEDUP_DATA_{timestamp}.json"
        undo_script = self.target_dir / f"UNDO_DEDUP_{timestamp}.sh"

        # Markdown report
        with open(report_file, "w") as f:
            f.write("# 🧹 INTELLIGENT DEDUPLICATION REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE REMOVAL'}\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## 📊 DEDUPLICATION SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Files Scanned | {self.stats['total_files']:,} |\n")
            f.write(
                f"| Exact Duplicate Groups | {self.stats['exact_duplicates']:,} |\n"
            )
            f.write(
                f"| Semantic Duplicate Groups | {self.stats['semantic_duplicates']:,} |\n"
            )
            f.write(f"| Files Removed | {self.stats['files_removed']:,} |\n")
            f.write(
                f"| Space Saved | {self.stats['space_saved'] / CONSTANT_1024 / CONSTANT_1024:.2f} MB |\n"
            )
            f.write(f"| Backup Location | `{self.backup_dir}` |\n\n")

            # Removal details grouped by parent folder
            f.write("## 🗑️ REMOVED FILES (By Parent Folder)\n\n")

            by_parent = defaultdict(list)
            for item in self.removal_plan:
                parent = item["remove_parent"]
                by_parent[parent].append(item)

            for parent in sorted(by_parent.keys()):
                items = by_parent[parent]
                total_size = sum(item["size"] for item in items)

                f.write(f"### 📁 {parent}\n")
                f.write(
                    f"**Removed:** {len(items)} files ({total_size / CONSTANT_1024:.1f} KB)\n\n"
                )

                for item in items:
                    f.write(f"- `{item['remove'].name}`\n")
                    f.write(
                        f"  - **Kept:** `{item['keep'].relative_to(self.target_dir)}`\n"
                    )
                    f.write(f"  - **Reason:** {item['reason']}\n")
                    f.write(f"  - **Size:** {item['size']:,} bytes\n\n")

            # Rollback instructions
            f.write("## 🔄 ROLLBACK INSTRUCTIONS\n\n")
            f.write("### Option 1: Restore All Files\n")
            f.write("```bash\n")
            f.write(f"cp -R {self.backup_dir}/* {self.target_dir}/\n")
            f.write("```\n\n")

            f.write("### Option 2: Use Undo Script\n")
            f.write("```bash\n")
            f.write(f"bash {undo_script}\n")
            f.write("```\n\n")

        # JSON data
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "removed_files": [
                {
                    "removed": str(item["remove"].relative_to(self.target_dir)),
                    "kept": str(item["keep"].relative_to(self.target_dir)),
                    "type": item["type"],
                    "size": item["size"],
                    "reason": item["reason"],
                }
                for item in self.removal_plan
            ],
        }

        with open(json_file, "w") as f:
            json.dump(json_data, f, indent=2)

        # Undo script
        if self.undo_commands and not self.dry_run:
            with open(undo_script, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo deduplication\n")
                f.write(
                    f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                f.write("echo '🔄 Restoring removed files...'\n\n")
                for cmd in self.undo_commands:
                    f.write(f"{cmd}\n")
                f.write("\necho '✅ Restore complete!'\n")

            undo_script.chmod(0o755)

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Data: {json_file}{Colors.END}")
        if undo_script.exists():
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} Undo: {undo_script}{Colors.END}")

        return report_file

    def run(self):
        """Run deduplication process"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║              🧹 INTELLIGENT DUPLICATE REMOVER 🧠                             ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║        Content-Aware Deduplication with Parent Folder Intelligence           ║"
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
            logger.info(
                f"{Colors.YELLOW}{Emojis.SHIELD} MODE: DRY RUN (no files will be removed){Colors.END}"
            )
        else:
            logger.info(
                f"{Colors.RED}{Emojis.WARN} MODE: LIVE REMOVAL (files will be deleted!){Colors.END}"
            )

        logger.info(
            f"{Colors.CYAN}Interactive: {'Yes' if self.interactive else 'No'}{Colors.END}\n"
        )

        # Scan
        self.scan_codebase()

        # Create plan
        self.create_removal_plan()

        # Execute
        self.execute_removal()

        # Report
        report = self.generate_report()

        # Summary
        self.print_header("DEDUPLICATION COMPLETE!", Emojis.ROCKET)

        logger.info(f"{Colors.BOLD}📊 FINAL STATS:{Colors.END}\n")
        logger.info(
            f"  {Emojis.FILE} Scanned: {Colors.CYAN}{self.stats['total_files']:,}{Colors.END}"
        )
        logger.info(
            f"  {Emojis.TARGET} Exact Dupes: {Colors.CYAN}{self.stats['exact_duplicates']:,} groups{Colors.END}"
        )
        logger.info(
            f"  {Emojis.BRAIN} Semantic Dupes: {Colors.CYAN}{self.stats['semantic_duplicates']:,} groups{Colors.END}"
        )
        logger.info(
            f"  {Emojis.TRASH} Removed: {Colors.CYAN}{self.stats['files_removed']:,} files{Colors.END}"
        )
        logger.info(
            f"  💾 Space Saved: {Colors.CYAN}{self.stats['space_saved'] / CONSTANT_1024 / CONSTANT_1024:.2f} MB{Colors.END}\n"
        )

        if self.dry_run:
            logger.info(
                f"{Colors.YELLOW}{Emojis.WARN} This was a DRY RUN. Use --live to actually remove files.{Colors.END}\n"
            )
        else:
            logger.info(
                f"{Colors.GREEN}{Emojis.CHECK} Deduplication complete!{Colors.END}\n"
            )
            logger.info(
                f"{Colors.CYAN}Backups saved to: {self.backup_dir}{Colors.END}\n"
            )


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🧹 Intelligent Duplicate Remover - Content-Aware Deduplication"
    )

    parser.add_argument(
        "--target",
        type=str,
        default=Path(str(Path.home()) + "/GitHub/AvaTarArTs-Suite"),
        help="Target directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry run mode (default, safe)",
    )
    parser.add_argument(
        "--live", action="store_true", help="Live mode (actually removes files)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        default=True,
        help="Interactive mode (asks for confirmation)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch mode (no confirmation, auto-approve safe removals)",
    )

    args = parser.parse_args()

    deduplicator = IntelligentDeduplicator(
        target_dir=args.target, dry_run=not args.live, interactive=not args.batch
    )

    deduplicator.run()


if __name__ == "__main__":
    main()
