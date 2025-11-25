#!/usr/bin/env python3
"""
Complete Cleanup Orchestrator
Coordinates all cleanup operations for the Documents folder
"""

import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys


class CleanupOrchestrator:
    def __init__(self, root_path):
        """__init__ function."""

        self.root_path = Path(root_path)
        self.cleanup_log = []
        self.total_space_saved = 0
        self.total_files_removed = 0

    def run_analysis(self):
        """Run the initial analysis to understand the scope"""
        logger.info("🔍 Running comprehensive analysis...")

        try:
            result = subprocess.run(
                [sys.executable, "Documents_Analyzer_Robust.py"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info("✅ Analysis complete")
                return True
            else:
                logger.info(f"❌ Analysis failed: {result.stderr}")
                return False
        except Exception as e:
            logger.info(f"❌ Analysis error: {e}")
            return False

    def run_python_cleanup(self, dry_run=True):
        """Run Python-specific cleanup"""
        logger.info(
            f"\n🐍 Running Python cleanup ({'DRY RUN' if dry_run else 'LIVE'})..."
        )

        try:
            result = subprocess.run(
                [sys.executable, "Python_Duplicate_Cleaner.py"],
                cwd=self.root_path,
                input="YES" if not dry_run else "NO",
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                logger.info("✅ Python cleanup complete")
                return True
            else:
                logger.info(f"❌ Python cleanup failed: {result.stderr}")
                return False
        except Exception as e:
            logger.info(f"❌ Python cleanup error: {e}")
            return False

    def run_general_cleanup(self, dry_run=True):
        """Run general duplicate cleanup"""
        logger.info(
            f"\n🧹 Running general cleanup ({'DRY RUN' if dry_run else 'LIVE'})..."
        )

        try:
            result = subprocess.run(
                [sys.executable, "Smart_Duplicate_Cleaner.py"],
                cwd=self.root_path,
                input="YES" if not dry_run else "NO",
                text=True,
                capture_output=True,
            )

            if result.returncode == 0:
                logger.info("✅ General cleanup complete")
                return True
            else:
                logger.info(f"❌ General cleanup failed: {result.stderr}")
                return False
        except Exception as e:
            logger.info(f"❌ General cleanup error: {e}")
            return False

    def create_cleanup_summary(self):
        """Create a summary of all cleanup operations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Look for cleanup reports
        cleanup_reports = list(self.root_path.glob("*cleanup_report*.json"))
        python_reports = list(self.root_path.glob("*python_cleanup_report*.json"))

        summary = {
            "timestamp": timestamp,
            "total_operations": len(cleanup_reports) + len(python_reports),
            "reports_found": {
                "general_cleanup": len(cleanup_reports),
                "python_cleanup": len(python_reports),
            },
        }

        # Generate summary report
        report_content = f"""# Complete Cleanup Summary

## Overview
- **Cleanup Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Operations:** {summary['total_operations']}
- **General Cleanup Reports:** {len(cleanup_reports)}
- **Python Cleanup Reports:** {len(python_reports)}

## Available Reports
"""

        for report in cleanup_reports + python_reports:
            report_content += f"- `{report.name}`\n"

        report_content += "\n## Next Steps\n"
        report_content += "1. Review all cleanup reports\n"
        report_content += "2. Verify important files are preserved\n"
        report_content += "3. Check backup directories for safety\n"
        report_content += "4. Consider implementing regular cleanup schedule\n"

        # Save summary
        summary_file = self.root_path / f"cleanup_summary_{timestamp}.md"
        with open(summary_file, "w") as f:
            f.write(report_content)

        logger.info(f"📋 Cleanup summary saved: {summary_file.name}")
        return summary

    def run_complete_cleanup(self, dry_run=True):
        """Run the complete cleanup process"""
        logger.info("🚀 Starting Complete Documents Cleanup")
        logger.info("=" * 50)
        logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")

        # Step 1: Run analysis
        if not self.run_analysis():
            logger.info("❌ Analysis failed, stopping cleanup")
            return False

        # Step 2: Python cleanup
        if not self.run_python_cleanup(dry_run):
            logger.info("⚠️  Python cleanup failed, continuing with general cleanup")

        # Step 3: General cleanup
        if not self.run_general_cleanup(dry_run):
            logger.info("⚠️  General cleanup failed")

        # Step 4: Create summary
        self.create_cleanup_summary()

        logger.info(
            f"\n🎉 Complete cleanup {'simulation' if dry_run else 'execution'} finished!"
        )
        logger.info("📋 Check the generated reports for details")

        return True


def main():
    """main function."""

    logger.info("🧹 Complete Documents Cleanup Orchestrator")
    logger.info("=" * 50)

    orchestrator = CleanupOrchestrator(Path(str(Path.home()) + "/Documents"))

    # First run: Dry run
    logger.info("\n🔍 STEP 1: DRY RUN - Simulating complete cleanup...")
    orchestrator.run_complete_cleanup(dry_run=True)

    # Ask for confirmation
    logger.info(f"\n❓ Do you want to proceed with the actual cleanup?")
    logger.info("   This will remove duplicate files and create backups.")
    logger.info("   Type 'YES' to proceed, anything else to cancel:")

    response = input().strip().upper()

    if response == "YES":
        logger.info("\n🚀 STEP 2: LIVE CLEANUP - Removing duplicates...")
        orchestrator.run_complete_cleanup(dry_run=False)

        logger.info(f"\n🎉 COMPLETE CLEANUP FINISHED!")
        logger.info("📋 Check the generated reports for details")
    else:
        logger.info("\n❌ Cleanup cancelled. Dry run results saved for review.")


if __name__ == "__main__":
    main()
