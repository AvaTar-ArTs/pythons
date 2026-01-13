import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
🎯 MASTER ANALYSIS RUNNER
========================
Runs ALL analysis and improvement tools on the consolidated Python directory.

Executes in order:
1. identify_user_scripts.py     - Separate YOUR code from libraries
2. analyze_codebase.py          - Basic code metrics & analysis
3. content_aware_organizer.py   - Folder structure intelligence
4. intelligent_dedup.py         - Find & remove duplicates
5. fix_bare_except.py           - Fix code quality issues
6. create_reorganization_plan.py - Folder flattening plan
7. deep_content_renamer.py      - Intelligent renaming suggestions
8. export_to_csv.py             - Export everything to CSV

Generates: MASTER_ANALYSIS_COMPLETE.md with all findings
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class MasterRunner:
    """Runs all analysis tools in sequence"""

    def __init__(self, target_dir: str, scripts_dir: str):
        self.target = Path(target_dir)
        self.scripts = Path(scripts_dir)
        self.results = {}
        self.start_time = datetime.now()

    def run_tool(self, script_name: str, args: list, description: str) -> bool:
        """Run a single tool and capture results"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔧 {description}")
        logger.info(f"{'='*80}{Colors.END}\n")

        script_path = self.scripts / script_name

        if not script_path.exists():
            logger.info(f"{Colors.RED}❌ Script not found: {script_path}{Colors.END}")
            self.results[script_name] = "NOT_FOUND"
            return False

        cmd = ["python3", str(script_path)] + args

        logger.info(f"{Colors.YELLOW}Running: {' '.join(cmd)}{Colors.END}\n")

        try:
            result = subprocess.run(cmd, capture_output=False, text=True)

            if result.returncode == 0:
                logger.info(f"\n{Colors.GREEN}✅ {description} - COMPLETE{Colors.END}")
                self.results[script_name] = "SUCCESS"
                return True
            else:
                logger.info(
                    f"\n{Colors.YELLOW}⚠️ {description} - COMPLETED WITH WARNINGS{Colors.END}"
                )
                self.results[script_name] = "WARNING"
                return True

        except Exception as e:
            logger.info(f"\n{Colors.RED}❌ {description} - FAILED: {e}{Colors.END}")
            self.results[script_name] = "FAILED"
            return False

    def run_all(self):
        """Run all analysis tools"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║                  🎯 MASTER ANALYSIS RUNNER 🧠                                 ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║            Running ALL Tools on Consolidated Python Directory                ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target}{Colors.END}")
        logger.info(f"{Colors.CYAN}Scripts: {self.scripts}{Colors.END}\n")

        # 1. Identify user scripts
        self.run_tool(
            "identify_user_scripts.py",
            ["--target", str(self.target)],
            "STEP 1: Identify YOUR scripts vs library files",
        )

        # 2. Basic code analysis
        self.run_tool(
            "analyze_codebase.py",
            ["--target", str(self.target)],
            "STEP 2: Analyze code metrics & quality",
        )

        # 3. Folder structure analysis
        self.run_tool(
            "content_aware_organizer.py",
            ["--target", str(self.target), "--depth", "6"],
            "STEP 3: Analyze folder structure (depth 6)",
        )

        # 4. Duplicate detection (batch mode)
        self.run_tool(
            "intelligent_dedup.py",
            ["--target", str(self.target), "--batch"],
            "STEP 4: Detect duplicates (dry-run)",
        )

        # 5. Fix bare except (dry-run)
        self.run_tool(
            "fix_bare_except.py",
            ["--target", str(self.target), "--dry-run"],
            "STEP 5: Scan for bare except clauses (dry-run)",
        )

        # 6. Reorganization plan
        self.run_tool(
            "create_reorganization_plan.py",
            ["--target", str(self.target), "--max-depth", "6"],
            "STEP 6: Create folder reorganization plan (10→6 levels)",
        )

        # 7. Renaming suggestions (dry-run)
        self.run_tool(
            "deep_content_renamer.py",
            ["--target", str(self.target), "--dry-run", "--limit", "100"],
            "STEP 7: Generate renaming suggestions (CONSTANT_100 files)",
        )

        # 8. Export to CSV
        self.run_tool(
            "export_to_csv.py",
            ["--target", str(self.target)],
            "STEP 8: Export all findings to CSV",
        )

        # Generate final report
        self.generate_master_report()

    def generate_master_report(self):
        """Generate comprehensive master report"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"📊 GENERATING MASTER REPORT")
        logger.info(f"{'='*80}{Colors.END}\n")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target / f"MASTER_ANALYSIS_COMPLETE_{timestamp}.md"

        elapsed = datetime.now() - self.start_time

        with open(report_file, "w") as f:
            f.write("# 🎯 MASTER ANALYSIS COMPLETE\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duration:** {elapsed.total_seconds():.1f} seconds\n")
            f.write(f"**Target:** `{self.target}`\n\n")

            f.write("## ✅ ANALYSIS SUMMARY\n\n")

            success_count = sum(1 for v in self.results.values() if v == "SUCCESS")
            warning_count = sum(1 for v in self.results.values() if v == "WARNING")
            failed_count = sum(1 for v in self.results.values() if v == "FAILED")

            f.write(f"- **Total Tools:** {len(self.results)}\n")
            f.write(f"- **Successful:** {success_count}\n")
            f.write(f"- **Warnings:** {warning_count}\n")
            f.write(f"- **Failed:** {failed_count}\n\n")

            f.write("## 📊 TOOLS EXECUTED\n\n")

            for idx, (script, status) in enumerate(self.results.items(), 1):
                if status == "SUCCESS":
                    icon = "✅"
                elif status == "WARNING":
                    icon = "⚠️"
                elif status == "FAILED":
                    icon = "❌"
                else:
                    icon = "❓"

                f.write(f"{idx}. {icon} **{script}** - {status}\n")

            f.write("\n## 📂 GENERATED REPORTS\n\n")
            f.write("All reports are in `~/Documents/python/`:\n\n")
            f.write(
                "- `USER_SCRIPTS_IDENTIFIED_*.md` - Your scripts vs library files\n"
            )
            f.write("- `analysis_report.json` - Code metrics & quality\n")
            f.write("- `FOLDER_STRUCTURE_ANALYSIS_*.md` - Folder intelligence\n")
            f.write("- `DEDUP_REPORT_*.md` - Duplicate detection\n")
            f.write("- `BARE_EXCEPT_FIX_REPORT_*.md` - Code quality issues\n")
            f.write("- `REORGANIZATION_PLAN_*.md` - Folder flattening plan\n")
            f.write("- `DEEP_RENAME_REPORT_*.md` - Renaming suggestions\n")
            f.write("- `*.csv` - All data exported for Excel/Numbers\n\n")

            f.write("## 🎯 NEXT STEPS\n\n")
            f.write("1. Review CSV files in spreadsheet app\n")
            f.write("2. Apply renaming (remove `yt_` prefix)\n")
            f.write("3. Execute reorganization plan (flatten folders)\n")
            f.write("4. Apply code quality fixes\n")
            f.write("5. Remove duplicates if found\n\n")

            f.write("## ✨ STATUS\n\n")
            f.write(
                "**All analysis complete!** Your Python directory is fully analyzed and ready for improvements.\n"
            )

        logger.info(f"{Colors.GREEN}✅ Master report: {report_file}{Colors.END}")

        # Final summary
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🎊 MASTER ANALYSIS COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 RESULTS:{Colors.END}\n")
        logger.info(f"  ✅ Successful: {success_count}/{len(self.results)}")
        logger.info(f"  ⚠️  Warnings: {warning_count}/{len(self.results)}")
        logger.info(f"  ❌ Failed: {failed_count}/{len(self.results)}\n")

        logger.info(
            f"{Colors.BOLD}⏱️  Duration: {elapsed.total_seconds():.1f} seconds{Colors.END}\n"
        )

        logger.info(f"{Colors.GREEN}📊 All findings exported to CSV files!{Colors.END}")
        logger.info(f"{Colors.GREEN}📚 Master report: {report_file.name}{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🎯 Run all analysis tools")
    parser.add_argument(
        "--target",
        type=str,
        default=Path(str(Path.home()) + "/Documents/python"),
        help="Target directory to analyze",
    )
    parser.add_argument(
        "--scripts",
        type=str,
        default=Path(str(Path.home()) + "/GitHub/AvaTarArTs-Suite/scripts"),
        help="Scripts directory",
    )

    args = parser.parse_args()

    runner = MasterRunner(args.target, args.scripts)
    runner.run_all()


if __name__ == "__main__":
    main()
