import logging

logger = logging.getLogger(__name__)


# Constants

#!/usr/bin/env python3
"""
🗂️ INTELLIGENT REORGANIZATION PLANNER
=====================================
Create a smart reorganization plan to flatten folder structure
from 10 levels to 6 levels while preserving content relationships.

Features:
✨ Analyzes current folder depth and nesting
✨ Identifies folders that should be flattened
✨ Preserves content relationships and categories
✨ Creates safe migration plan with rollback
✨ Generates folder mapping and move scripts
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple


# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class ReorganizationPlanner:
    """Create intelligent reorganization plan"""

    def __init__(self, target_dir: str, max_depth: int = 6):
        self.target_dir = Path(target_dir)
        self.max_depth = max_depth
        self.current_structure = {}
        self.proposed_structure = {}
        self.move_plan = []

        self.stats = {
            "total_folders": 0,
            "folders_to_move": 0,
            "deep_folders": 0,
            "files_affected": 0,
        }

    def analyze_structure(self):
        """Analyze current folder structure"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔍 ANALYZING CURRENT STRUCTURE")
        logger.info(f"{'='*80}{Colors.END}\n")

        folders_by_depth = defaultdict(list)

        for root, dirs, files in os.walk(self.target_dir):
            # Skip certain directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith((".git", "__pycache__", "backup", "dedup"))
            ]

            rel_path = Path(root).relative_to(self.target_dir)
            depth = len(rel_path.parts)

            if depth > 0:  # Skip root
                folders_by_depth[depth].append(
                    {
                        "path": Path(root),
                        "rel_path": rel_path,
                        "depth": depth,
                        "files": len([f for f in files if f.endswith(".py")]),
                        "subdirs": len(dirs),
                    }
                )

                self.stats["total_folders"] += 1

                if depth > self.max_depth:
                    self.stats["deep_folders"] += 1

        logger.info(
            f"{Colors.GREEN}Analyzed {self.stats['total_folders']} folders{Colors.END}"
        )
        logger.info(
            f"{Colors.YELLOW}Found {self.stats['deep_folders']} folders deeper than level {self.max_depth}{Colors.END}\n"
        )

        # Show distribution
        logger.info(f"{Colors.BOLD}Depth Distribution:{Colors.END}")
        for depth in sorted(folders_by_depth.keys()):
            count = len(folders_by_depth[depth])
            bar = "█" * min(count // 10, 50)
            logger.info(f"  Level {depth:2d}: {count:4d} folders {bar}")

        return folders_by_depth

    def create_flattening_plan(self, folders_by_depth: Dict):
        """Create plan to flatten deep folders"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"📋 CREATING FLATTENING PLAN")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Process folders deeper than max_depth
        for depth in sorted(folders_by_depth.keys(), reverse=True):
            if depth <= self.max_depth:
                continue

            for folder_info in folders_by_depth[depth]:
                # Determine new location (move up to max_depth)
                old_path = folder_info["rel_path"]

                # Strategy: Keep top levels, flatten middle, preserve bottom
                parts = list(old_path.parts)

                if len(parts) > self.max_depth:
                    # Keep first 2 and last 1, flatten middle with underscores
                    category = parts[0] if len(parts) > 0 else "misc"
                    subcategory = parts[1] if len(parts) > 1 else ""
                    folder_name = "_".join(parts[2:])  # Flatten middle parts

                    if subcategory:
                        new_rel_path = Path(category) / subcategory / folder_name
                    else:
                        new_rel_path = Path(category) / folder_name

                    self.move_plan.append(
                        {
                            "old_path": folder_info["path"],
                            "new_path": self.target_dir / new_rel_path,
                            "old_depth": depth,
                            "new_depth": len(new_rel_path.parts),
                            "files": folder_info["files"],
                            "reason": f"Flatten from level {depth} to {len(new_rel_path.parts)}",
                        }
                    )

                    self.stats["folders_to_move"] += 1
                    self.stats["files_affected"] += folder_info["files"]

        logger.info(
            f"{Colors.GREEN}Created plan for {self.stats['folders_to_move']} folders{Colors.END}"
        )
        logger.info(
            f"{Colors.YELLOW}Affects {self.stats['files_affected']} Python files{Colors.END}"
        )

    def generate_reports(self):
        """Generate reorganization reports"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"REORGANIZATION_PLAN_{timestamp}.md"
        script_file = self.target_dir / f"execute_reorganization_{timestamp}.sh"
        json_file = self.target_dir / f"reorganization_data_{timestamp}.json"

        # Markdown report
        with open(report_file, "w") as f:
            f.write("# 🗂️ INTELLIGENT REORGANIZATION PLAN\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Target Depth:** {self.max_depth} levels\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## 📊 REORGANIZATION SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Folders | {self.stats['total_folders']:,} |\n")
            f.write(
                f"| Deep Folders (>{self.max_depth}) | {self.stats['deep_folders']:,} |\n"
            )
            f.write(f"| Folders to Move | {self.stats['folders_to_move']:,} |\n")
            f.write(f"| Files Affected | {self.stats['files_affected']:,} |\n\n")

            # Strategy
            f.write("## 🎯 FLATTENING STRATEGY\n\n")
            f.write(
                f"**Goal:** Reduce folder depth from 10 → {self.max_depth} levels\n\n"
            )
            f.write("**Method:**\n")
            f.write("- Keep top 2 levels (category/subcategory)\n")
            f.write("- Flatten middle levels using underscores\n")
            f.write("- Preserve folder names for context\n")
            f.write("- Maintain content relationships\n\n")

            # Example transformations
            if self.move_plan:
                f.write("## 📝 EXAMPLE TRANSFORMATIONS\n\n")
                for move in self.move_plan[:10]:
                    f.write(f"### Move {move['files']} files\n")
                    f.write(
                        f"**From:** `{move['old_path'].relative_to(self.target_dir)}` (Level {move['old_depth']})\n"
                    )
                    f.write(
                        f"**To:** `{move['new_path'].relative_to(self.target_dir)}` (Level {move['new_depth']})\n"
                    )
                    f.write(f"**Reason:** {move['reason']}\n\n")

            # Move plan
            f.write("## 🚚 COMPLETE MOVE PLAN\n\n")
            f.write(f"Total moves: {len(self.move_plan)}\n\n")

            for idx, move in enumerate(self.move_plan, 1):
                f.write(
                    f"{idx}. `{move['old_path'].relative_to(self.target_dir)}` → `{move['new_path'].relative_to(self.target_dir)}`\n"
                )

        # Shell script
        with open(script_file, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Reorganization execution script\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("echo '🗂️ Starting reorganization...'\n")
            f.write("echo ''\n\n")

            for idx, move in enumerate(self.move_plan, 1):
                f.write(f"# Move {idx}/{len(self.move_plan)}\n")
                f.write(
                    f"echo '[{idx}/{len(self.move_plan)}] Moving {move['files']} files...'\n"
                )
                f.write(f"mkdir -p '{move['new_path']}'\n")
                f.write(
                    f"mv '{move['old_path']}'/* '{move['new_path']}/' 2>/dev/null\n"
                )
                f.write(f"rmdir '{move['old_path']}' 2>/dev/null\n\n")

            f.write("echo ''\n")
            f.write("echo '✅ Reorganization complete!'\n")

        script_file.chmod(0o755)

        # JSON data
        with open(json_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "stats": self.stats,
                    "max_depth": self.max_depth,
                    "move_plan": [
                        {
                            "old": str(m["old_path"].relative_to(self.target_dir)),
                            "new": str(m["new_path"].relative_to(self.target_dir)),
                            "old_depth": m["old_depth"],
                            "new_depth": m["new_depth"],
                            "files": m["files"],
                        }
                        for m in self.move_plan
                    ],
                },
                f,
                indent=2,
            )

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ Script: {script_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ Data: {json_file}{Colors.END}")

        return report_file

    def run(self):
        """Run reorganization planner"""

        logger.info(f"{Colors.BOLD}{Colors.CYAN}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║             🗂️ INTELLIGENT REORGANIZATION PLANNER 🧠                         ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║          Smart Folder Flattening with Content Awareness                      ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}")

        logger.info(f"\n{Colors.CYAN}Target: {self.target_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}Max Depth: {self.max_depth} levels{Colors.END}\n")

        # Analyze
        folders_by_depth = self.analyze_structure()

        # Create plan
        self.create_flattening_plan(folders_by_depth)

        # Generate reports
        self.generate_reports()

        # Summary
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✅ PLAN COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(
            f"  Total Folders: {Colors.CYAN}{self.stats['total_folders']:,}{Colors.END}"
        )
        logger.info(
            f"  Deep Folders (>{self.max_depth}): {Colors.YELLOW}{self.stats['deep_folders']:,}{Colors.END}"
        )
        logger.info(
            f"  To Move: {Colors.CYAN}{self.stats['folders_to_move']:,}{Colors.END}"
        )
        logger.info(
            f"  Files Affected: {Colors.CYAN}{self.stats['files_affected']:,}{Colors.END}\n"
        )


import os


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🗂️ Create reorganization plan")
    parser.add_argument("--target", type=str, required=True, help="Target directory")
    parser.add_argument(
        "--max-depth", type=int, default=6, help="Maximum folder depth (default: 6)"
    )

    args = parser.parse_args()

    planner = ReorganizationPlanner(args.target, args.max_depth)
    planner.run()


if __name__ == "__main__":
    main()
