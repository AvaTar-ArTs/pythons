#!/usr/bin/env python3
"""
Advanced Sort and Deduplication Tool

This script comprehensively sorts, deduplicates, and organizes the Python music processing directory.
It removes duplicates, consolidates similar files, and creates a clean, organized structure.
"""

import os
import sys
import logging
import shutil
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import re
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("sort_and_dedupe.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AdvancedSortAndDedupe:
    def __init__(self, base_dir: str):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.clean_dir = self.base_dir / "CLEAN_ORGANIZED"
        self.duplicates_dir = self.base_dir / "DUPLICATES_ARCHIVE"
        self.reports_dir = self.base_dir / "REPORTS"

        # File hash cache for duplicate detection
        self.file_hashes = {}
        self.duplicate_groups = defaultdict(list)

        # Content similarity patterns
        self.similarity_patterns = {
            "analyze_variants": [r"analyze.*\.py$", r"analyzer.*\.py$", r".*analysis.*\.py$"],
            "transcribe_variants": [r"trans.*\.py$", r"transcript.*\.py$", r".*transcribe.*\.py$"],
            "generate_variants": [r"generate.*\.py$", r"gen.*\.py$", r".*create.*\.py$"],
            "process_variants": [r"process.*\.py$", r"mp3.*\.py$", r"mp4.*\.py$", r"convert.*\.py$"],
            "suno_variants": [r"suno.*\.py$", r".*scrape.*\.py$", r".*extract.*\.py$"],
        }

        # File categories for organization
        self.categories = {
            "core_analysis": "Core Analysis Scripts",
            "transcription": "Transcription & Speech Processing",
            "generation": "Content Generation",
            "processing": "File Processing & Conversion",
            "web_scraping": "Web Scraping & Data Extraction",
            "organization": "File Organization & Management",
            "utilities": "Utility Scripts",
            "experimental": "Experimental & Test Scripts",
            "archived": "Archived Scripts",
        }

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def find_exact_duplicates(self) -> Dict[str, List[Path]]:
        """Find files with identical content."""
        logger.info("Scanning for exact duplicates...")

        for file_path in self.base_dir.rglob("*.py"):
            if file_path.is_file():
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    self.file_hashes[file_hash] = file_path
                    self.duplicate_groups[file_hash].append(file_path)

        # Return only groups with duplicates
        duplicates = {h: files for h, files in self.duplicate_groups.items() if len(files) > 1}
        logger.info(f"Found {len(duplicates)} groups of exact duplicates")
        return duplicates

    def find_similar_files(self) -> Dict[str, List[Path]]:
        """Find files with similar names and purposes."""
        logger.info("Scanning for similar files...")

        similar_groups = defaultdict(list)

        for file_path in self.base_dir.rglob("*.py"):
            if file_path.is_file():
                filename = file_path.name.lower()

                for pattern_name, patterns in self.similarity_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, filename):
                            similar_groups[pattern_name].append(file_path)
                            break

        # Filter out single-file groups
        similar_groups = {k: v for k, v in similar_groups.items() if len(v) > 1}
        logger.info(f"Found {len(similar_groups)} groups of similar files")
        return similar_groups

    def analyze_file_content(self, file_path: Path) -> Dict:
        """Analyze file content to determine category and quality."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic content analysis
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]

            # Quality indicators
            has_docstring = '"""' in content or "'''" in content
            has_logging = "logging" in content.lower()
            has_error_handling = "try:" in content and "except" in content
            has_main_function = 'if __name__ == "__main__":' in content
            has_imports = len(
                [line for line in lines if line.strip().startswith("import") or line.strip().startswith("from")]
            )

            # Determine category based on content
            category = self._determine_category(content, file_path.name)

            # Calculate quality score
            quality_score = 0
            if has_docstring:
                quality_score += 2
            if has_logging:
                quality_score += 1
            if has_error_handling:
                quality_score += 2
            if has_main_function:
                quality_score += 1
            if has_imports > 5:
                quality_score += 1

            return {
                "file_path": file_path,
                "category": category,
                "quality_score": quality_score,
                "lines": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "has_docstring": has_docstring,
                "has_logging": has_logging,
                "has_error_handling": has_error_handling,
                "has_main_function": has_main_function,
                "imports_count": has_imports,
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
            }

        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
            return {
                "file_path": file_path,
                "category": "utilities",
                "quality_score": 0,
                "lines": 0,
                "non_empty_lines": 0,
                "has_docstring": False,
                "has_logging": False,
                "has_error_handling": False,
                "has_main_function": False,
                "imports_count": 0,
                "size": 0,
                "modified": 0,
            }

    def _determine_category(self, content: str, filename: str) -> str:
        """Determine file category based on content and filename."""
        content_lower = content.lower()
        filename_lower = filename.lower()

        # Analysis scripts
        if any(keyword in content_lower for keyword in ["analyze", "analysis", "analyzer"]):
            return "core_analysis"

        # Transcription scripts
        if any(keyword in content_lower for keyword in ["transcribe", "transcript", "whisper", "speech"]):
            return "transcription"

        # Generation scripts
        if any(keyword in content_lower for keyword in ["generate", "create", "build", "html", "csv"]):
            return "generation"

        # Processing scripts
        if any(keyword in content_lower for keyword in ["process", "convert", "mp3", "mp4", "ffmpeg"]):
            return "processing"

        # Web scraping scripts
        if any(keyword in content_lower for keyword in ["scrape", "suno", "beautifulsoup", "requests"]):
            return "web_scraping"

        # Organization scripts
        if any(keyword in content_lower for keyword in ["organize", "sort", "manage", "file"]):
            return "organization"

        # Experimental/test scripts
        if any(keyword in filename_lower for keyword in ["test", "experimental", "untitled", "copy"]):
            return "experimental"

        return "utilities"

    def create_clean_structure(self):
        """Create clean directory structure."""
        logger.info("Creating clean directory structure...")

        # Create main directories
        self.clean_dir.mkdir(exist_ok=True)
        self.duplicates_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        # Create category directories
        for category, description in self.categories.items():
            category_dir = self.clean_dir / category
            category_dir.mkdir(exist_ok=True)

            # Create README for each category
            readme_path = category_dir / "README.md"
            with open(readme_path, "w") as f:
                f.write(f"# {description}\n\n")
                f.write(f"This directory contains {description.lower()}.\n\n")
                f.write("## Files in this category:\n")

        logger.info("Clean directory structure created")

    def process_duplicates(self, duplicates: Dict[str, List[Path]]):
        """Process and archive duplicate files."""
        logger.info("Processing duplicate files...")

        total_duplicates = 0

        for file_hash, files in duplicates.items():
            if len(files) > 1:
                # Sort by quality score and file size
                file_analyses = [self.analyze_file_content(f) for f in files]
                file_analyses.sort(key=lambda x: (x["quality_score"], x["size"]), reverse=True)

                # Keep the best file
                keep_file = file_analyses[0]["file_path"]
                duplicate_files = [f["file_path"] for f in file_analyses[1:]]

                logger.info(f"Keeping: {keep_file}")
                logger.info(f"Archiving {len(duplicate_files)} duplicates")

                # Archive duplicates
                for duplicate in duplicate_files:
                    archive_path = self.duplicates_dir / duplicate.name
                    counter = 1
                    while archive_path.exists():
                        archive_path = self.duplicates_dir / f"{duplicate.stem}_{counter}{duplicate.suffix}"
                        counter += 1

                    shutil.move(str(duplicate), str(archive_path))
                    total_duplicates += 1

        logger.info(f"Archived {total_duplicates} duplicate files")

    def process_similar_files(self, similar_groups: Dict[str, List[Path]]):
        """Process similar files and consolidate them."""
        logger.info("Processing similar files...")

        for group_name, files in similar_groups.items():
            logger.info(f"Processing {group_name} group with {len(files)} files")

            # Analyze all files in the group
            file_analyses = [self.analyze_file_content(f) for f in files]
            file_analyses.sort(key=lambda x: (x["quality_score"], x["size"]), reverse=True)

            # Keep the best file and archive others
            keep_file = file_analyses[0]["file_path"]
            similar_files = [f["file_path"] for f in file_analyses[1:]]

            logger.info(f"Keeping best: {keep_file}")
            logger.info(f"Archiving {len(similar_files)} similar files")

            # Archive similar files
            for similar in similar_files:
                archive_path = self.duplicates_dir / f"{group_name}_{similar.name}"
                counter = 1
                while archive_path.exists():
                    archive_path = self.duplicates_dir / f"{group_name}_{similar.stem}_{counter}{similar.suffix}"
                    counter += 1

                shutil.move(str(similar), str(archive_path))

    def organize_remaining_files(self):
        """Organize remaining files into clean structure."""
        logger.info("Organizing remaining files...")

        # Find all remaining Python files
        remaining_files = []
        for file_path in self.base_dir.rglob("*.py"):
            if (
                file_path.is_file()
                and self.clean_dir not in file_path.parents
                and self.duplicates_dir not in file_path.parents
            ):
                remaining_files.append(file_path)

        logger.info(f"Organizing {len(remaining_files)} remaining files")

        for file_path in remaining_files:
            try:
                # Analyze file
                analysis = self.analyze_file_content(file_path)
                category = analysis["category"]

                # Determine target directory
                target_dir = self.clean_dir / category

                # Create new filename
                new_filename = self._create_clean_filename(file_path.name, analysis)
                target_path = target_dir / new_filename

                # Handle duplicates
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                # Move file
                shutil.move(str(file_path), str(target_path))
                logger.info(f"Moved {file_path.name} to {category}/{target_path.name}")

            except Exception as e:
                logger.error(f"Error organizing {file_path}: {e}")

    def _create_clean_filename(self, filename: str, analysis: Dict) -> str:
        """Create a clean filename based on analysis."""
        # Remove common suffixes and clean up
        clean_name = filename

        # Remove common patterns
        patterns_to_remove = [
            r"\(\d+\)",  # (1), (2), etc.
            r"_\d+$",  # _1, _2, etc.
            r"\s+\d+$",  # space + number
            r"copy",  # copy
            r"backup",  # backup
        ]

        for pattern in patterns_to_remove:
            clean_name = re.sub(pattern, "", clean_name, flags=re.IGNORECASE)

        # Clean up extra spaces and underscores
        clean_name = re.sub(r"[_\s]+", "_", clean_name)
        clean_name = clean_name.strip("_")

        # Ensure .py extension
        if not clean_name.endswith(".py"):
            clean_name += ".py"

        return clean_name

    def generate_reports(self, duplicates: Dict[str, List[Path]], similar_groups: Dict[str, List[Path]]):
        """Generate comprehensive reports."""
        logger.info("Generating reports...")

        # Summary report
        summary_report = self.reports_dir / "SORTING_SUMMARY.md"
        with open(summary_report, "w") as f:
            f.write("# Python Directory Sorting and Deduplication Summary\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Overview\n\n")
            f.write(f"- **Total Python files processed:** {len(list(self.base_dir.rglob('*.py')))}\n")
            f.write(f"- **Exact duplicates found:** {sum(len(files) - 1 for files in duplicates.values())}\n")
            f.write(f"- **Similar file groups:** {len(similar_groups)}\n")
            f.write(f"- **Files archived:** {len(list(self.duplicates_dir.rglob('*.py')))}\n")
            f.write(f"- **Files organized:** {len(list(self.clean_dir.rglob('*.py')))}\n\n")

            f.write("## Duplicate Groups\n\n")
            for file_hash, files in duplicates.items():
                f.write(f"### Group {file_hash[:8]}...\n")
                f.write(f"Files: {len(files)}\n")
                for file_path in files:
                    f.write(f"- {file_path}\n")
                f.write(Path("\n"))

            f.write("## Similar File Groups\n\n")
            for group_name, files in similar_groups.items():
                f.write(f"### {group_name.replace('_', ' ').title()}\n")
                f.write(f"Files: {len(files)}\n")
                for file_path in files:
                    f.write(f"- {file_path}\n")
                f.write(Path("\n"))

            f.write("## Clean Directory Structure\n\n")
            f.write("```\n")
            f.write("CLEAN_ORGANIZED/\n")
            for category in self.categories.keys():
                f.write(f"├── {category}/\n")
                f.write(f"│   ├── README.md\n")
                category_files = list((self.clean_dir / category).glob("*.py"))
                for i, file_path in enumerate(category_files[:5]):  # Show first 5 files
                    f.write(f"│   ├── {file_path.name}\n")
                if len(category_files) > 5:
                    f.write(f"│   └── ... ({len(category_files) - 5} more files)\n")
                else:
                    f.write(f"│   └── (empty)\n")
            f.write("└── DUPLICATES_ARCHIVE/\n")
            f.write("    └── (archived files)\n")
            f.write("```\n")

        # Detailed analysis report
        analysis_report = self.reports_dir / "DETAILED_ANALYSIS.json"
        analysis_data = {
            "duplicates": {h: [str(f) for f in files] for h, files in duplicates.items()},
            "similar_groups": {k: [str(f) for f in files] for k, files in similar_groups.items()},
            "categories": {cat: len(list((self.clean_dir / cat).glob("*.py"))) for cat in self.categories.keys()},
            "total_files_processed": len(list(self.base_dir.rglob("*.py"))),
            "files_archived": len(list(self.duplicates_dir.rglob("*.py"))),
            "files_organized": len(list(self.clean_dir.rglob("*.py"))),
        }

        with open(analysis_report, "w") as f:
            json.dump(analysis_data, f, indent=2)

        logger.info(f"Reports generated in {self.reports_dir}")

    def run_complete_sort_and_dedupe(self):
        """Run the complete sorting and deduplication process."""
        logger.info("Starting complete sort and deduplication process...")

        # Step 1: Find exact duplicates
        duplicates = self.find_exact_duplicates()

        # Step 2: Find similar files
        similar_groups = self.find_similar_files()

        # Step 3: Create clean structure
        self.create_clean_structure()

        # Step 4: Process duplicates
        self.process_duplicates(duplicates)

        # Step 5: Process similar files
        self.process_similar_files(similar_groups)

        # Step 6: Organize remaining files
        self.organize_remaining_files()

        # Step 7: Generate reports
        self.generate_reports(duplicates, similar_groups)

        logger.info("Complete sort and deduplication process finished!")

        # Print summary
        total_original = len(list(self.base_dir.rglob("*.py")))
        total_archived = len(list(self.duplicates_dir.rglob("*.py")))
        total_organized = len(list(self.clean_dir.rglob("*.py")))

        logger.info(f"\n✅ Sorting and Deduplication Complete!")
        logger.info(f"📊 Original files: {total_original}")
        logger.info(f"🗂️  Files organized: {total_organized}")
        logger.info(f"📦 Files archived: {total_archived}")
        logger.info(f"📁 Clean directory: {self.clean_dir}")
        logger.info(f"📋 Reports: {self.reports_dir}")


def main():
    """Main function."""
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/python")

    if not os.path.exists(base_dir):
        logger.error(f"Base directory not found: {base_dir}")
        return

    sorter = AdvancedSortAndDedupe(base_dir)
    sorter.run_complete_sort_and_dedupe()


if __name__ == "__main__":
    main()
