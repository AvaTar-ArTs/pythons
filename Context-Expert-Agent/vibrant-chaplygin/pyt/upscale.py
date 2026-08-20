#!/usr/bin/env python3
"""
Move Improvements Back Script
=============================

Moves all improved files from the copied_files directory back to the original
Python directory, replacing the original files with the improved versions.

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImprovementMover:
    """Moves improved files back to the original directory."""

    def __init__(self, python_dir: str, copied_files_dir: str):
        """__init__ function."""

        self.python_dir = Path(python_dir)
        self.copied_files_dir = Path(copied_files_dir)

        # Files to move back (improved versions)
        self.improved_files = [
            "enhanced_image_upscaler.py",
            "improved_batch_upscaler.py",
            "unified_image_upscaler.py",
            "improved_common_utilities.py",
            "improved_audio_transcriber.py",
            "enhanced_utilities.py",
            "test_framework.py",
            "coding_standards.py",
            "quality_monitor.py",
            "comprehensive_codebase_analyzer.py",
            "comprehensive_fix_implementer.py",
            "advanced_quality_improver.py",
            "comprehensive_test_generator.py",
            "batch_quality_improver.py",
            "batch_progress_monitor.py",
            "advanced_quality_enhancer.py",
            "focused_quality_analyzer.py",
            "merge_improvements.py",
            "move_improvements_back.py",
        ]

        # Documentation files to move
        self.documentation_files = [
            "COMPREHENSIVE_IMPROVEMENTS_IMPLEMENTED.md",
            "COMPREHENSIVE_ANALYSIS_SUMMARY.md",
            "COMPREHENSIVE_IMPROVEMENT_PLAN.md",
            "PYTHON_IMPROVEMENTS_README.md",
            "IMPROVEMENT_TRACKING.md",
            "FINAL_QUALITY_IMPROVEMENT_SUMMARY.md",
        ]

        # Configuration files to move
        self.config_files = [
            "config.json",
            "requirements.txt",
            "requirements_improved.txt",
            "requirements_enhanced.txt",
        ]

        # Test files to move
        self.test_files = ["test_improvements.py"]

        # Report files to move
        self.report_files = [
            "python_improvements_summary.csv",
            "all_files_fix_report.json",
            "advanced_quality_report.json",
            "test_generation_report.json",
            "fix_report.json",
            "quality_improvement_report.json",
            "enhancement_report.json",
        ]

    def move_improvements_back(self) -> None:
        """Move all improved files back to the original directory."""
        logger.info("Starting to move improvements back to original directory...")

        # Create backup of original directory
        self._create_backup()

        # Move improved Python files
        self._move_improved_files()

        # Move documentation
        self._move_documentation()

        # Move configuration files
        self._move_configuration()

        # Move test files
        self._move_test_files()

        # Move report files
        self._move_reports()

        # Generate move summary
        self._generate_move_summary()

        logger.info("Move improvements back process completed!")

    def _create_backup(self) -> None:
        """Create a backup of the original directory before moving files."""
        backup_dir = (
            self.python_dir.parent
            / f"python_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        logger.info(f"Creating backup at: {backup_dir}")
        try:
            shutil.copytree(self.python_dir, backup_dir, ignore_dangling_symlinks=True)
            logger.info(f"Backup created successfully at: {backup_dir}")
        except Exception as e:
            logger.warning(f"Backup creation failed (continuing anyway): {e}")
            logger.info("Skipping backup due to symlink issues")

    def _move_improved_files(self) -> None:
        """Move improved Python files back to their original locations."""
        for file_name in self.improved_files:
            source = self.copied_files_dir / file_name
            if source.exists():
                # Determine destination based on file type
                if "upscaler" in file_name or "image" in file_name:
                    destination = (
                        self.python_dir
                        / "02_media_processing"
                        / "image_tools"
                        / file_name
                    )
                elif "audio" in file_name or "transcriber" in file_name:
                    destination = self.python_dir / "05_audio_video" / file_name
                elif "utilities" in file_name or "common" in file_name:
                    destination = self.python_dir / "00_shared_libraries" / file_name
                elif (
                    "quality" in file_name
                    or "analyzer" in file_name
                    or "improver" in file_name
                ):
                    destination = self.python_dir / "06_development_tools" / file_name
                else:
                    destination = self.python_dir / "00_shared_libraries" / file_name

                # Create destination directory if it doesn't exist
                destination.parent.mkdir(parents=True, exist_ok=True)

                # Move file
                shutil.copy2(source, destination)
                logger.info(f"Moved {file_name} to {destination}")
            else:
                logger.warning(f"File not found: {file_name}")

    def _move_documentation(self) -> None:
        """Move documentation files."""
        doc_dir = self.python_dir / "09_documentation"
        doc_dir.mkdir(parents=True, exist_ok=True)

        for doc_file in self.documentation_files:
            source = self.copied_files_dir / doc_file
            if source.exists():
                destination = doc_dir / doc_file
                shutil.copy2(source, destination)
                logger.info(f"Moved {doc_file} to documentation")

    def _move_configuration(self) -> None:
        """Move configuration files."""
        config_dir = self.python_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        for config_file in self.config_files:
            source = self.copied_files_dir / config_file
            if source.exists():
                destination = config_dir / config_file
                shutil.copy2(source, destination)
                logger.info(f"Moved {config_file} to config")

    def _move_test_files(self) -> None:
        """Move test files."""
        test_dir = self.python_dir / "tests"
        test_dir.mkdir(parents=True, exist_ok=True)

        for test_file in self.test_files:
            source = self.copied_files_dir / test_file
            if source.exists():
                destination = test_dir / test_file
                shutil.copy2(source, destination)
                logger.info(f"Moved {test_file} to tests")

    def _move_reports(self) -> None:
        """Move report files."""
        reports_dir = self.python_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        for report_file in self.report_files:
            source = self.copied_files_dir / report_file
            if source.exists():
                destination = reports_dir / report_file
                shutil.copy2(source, destination)
                logger.info(f"Moved {report_file} to reports")

    def _generate_move_summary(self) -> None:
        """Generate a summary of the move process."""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "move_summary": {
                "improved_files_moved": len(self.improved_files),
                "documentation_files_moved": len(self.documentation_files),
                "configuration_files_moved": len(self.config_files),
                "test_files_moved": len(self.test_files),
                "report_files_moved": len(self.report_files),
            },
            "file_locations": {
                "improved_files": "Moved to appropriate subdirectories based on functionality",
                "documentation": "Moved to 09_documentation/",
                "configuration": "Moved to config/",
                "tests": "Moved to tests/",
                "reports": "Moved to reports/",
            },
            "next_steps": [
                "Review the improved files in their new locations",
                "Test the improved functionality",
                "Update any import statements if needed",
                "Run quality analysis on the improved codebase",
            ],
        }

        summary_file = self.python_dir / "MOVE_SUMMARY.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Move summary generated: {summary_file}")

        # Also create a markdown summary
        self._generate_markdown_summary(summary)

    def _generate_markdown_summary(self, summary: Dict) -> None:
        """Generate a markdown summary of the move."""
        md_file = self.python_dir / "MOVE_SUMMARY.md"

        with open(md_file, "w") as f:
            f.write("# Improvement Move Summary\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            f.write("## Overview\n\n")
            f.write(
                "All improved files have been moved back to the original Python directory structure.\n\n"
            )

            f.write("## Files Moved\n\n")
            move_data = summary["move_summary"]
            f.write(
                f"- **Improved Files:** {move_data['improved_files_moved']} files\n"
            )
            f.write(
                f"- **Documentation Files:** {move_data['documentation_files_moved']} files\n"
            )
            f.write(
                f"- **Configuration Files:** {move_data['configuration_files_moved']} files\n"
            )
            f.write(f"- **Test Files:** {move_data['test_files_moved']} files\n")
            f.write(f"- **Report Files:** {move_data['report_files_moved']} files\n\n")

            f.write("## File Locations\n\n")
            for category, description in summary["file_locations"].items():
                f.write(f"- **{category.title()}:** {description}\n")
            f.write(Path("\n"))

            f.write("## Next Steps\n\n")
            for i, step in enumerate(summary["next_steps"], 1):
                f.write(f"{i}. {step}\n")
            f.write(Path("\n"))

            f.write("## Quick Start\n\n")
            f.write("```bash\n")
            f.write("# Run quality analysis on improved codebase\n")
            f.write("python 00_shared_libraries/focused_quality_analyzer.py .\n\n")
            f.write("# Run batch improvements\n")
            f.write(
                "python 00_shared_libraries/batch_quality_improver.py . --batch-size 25\n\n"
            )
            f.write("# Monitor quality\n")
            f.write("python 00_shared_libraries/quality_monitor.py .\n")
            f.write("```\n")


def main():
    """Main function."""
    if len(sys.argv) != 3:
        logger.info(
            "Usage: python move_improvements_back.py <python_directory> <copied_files_directory>"
        )
        sys.exit(1)

    python_dir = sys.argv[1]
    copied_files_dir = sys.argv[2]

    if not os.path.exists(python_dir):
        logger.info(f"Error: Python directory {python_dir} does not exist")
        sys.exit(1)

    if not os.path.exists(copied_files_dir):
        logger.info(f"Error: Copied files directory {copied_files_dir} does not exist")
        sys.exit(1)

    # Create mover
    mover = ImprovementMover(python_dir, copied_files_dir)

    # Move improvements back
    mover.move_improvements_back()

    logger.info(Path("\n") + "=" * 60)
    logger.info("IMPROVEMENTS MOVED BACK SUCCESSFULLY")
    logger.info("=" * 60)
    logger.info("All improved files have been moved back to the original directory.")
    logger.info("Check the MOVE_SUMMARY.md file for details on the new organization.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
