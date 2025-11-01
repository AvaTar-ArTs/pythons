"""
Downloads

This module provides functionality for downloads.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024
CONSTANT_2025 = 2025
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
Downloads Directory Organizer & Consolidator
Comprehensive analysis and organization tool for Downloads directory

Author: Steven Chaplinski
Date: October CONSTANT_2025
Purpose: Deep analysis, duplicate detection, and intelligent organization
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import csv
import re
from typing import Dict, List, Tuple, Set


class DownloadsOrganizer:
    def __init__(self, downloads_path: str = Path("/Users/steven/Downloads")):
        """__init__ function."""

        self.downloads_path = Path(downloads_path)
        self.analysis_data = {}
        self.duplicates = defaultdict(list)
        self.file_hashes = {}
        self.organization_plan = {}
        self.backup_path = None

    def create_backup(self) -> str:
        """Create a timestamped backup of the Downloads directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"/Users/steven/Downloads_BACKUP_{timestamp}"

        logger.info(f"Creating backup at: {backup_path}")
        shutil.copytree(self.downloads_path, backup_path)
        self.backup_path = backup_path
        return backup_path

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (IOError, OSError):
            return None

    def analyze_directory_structure(self) -> Dict:
        """Analyze the directory structure and categorize files"""
        analysis = {
            "total_files": 0,
            "total_directories": 0,
            "total_size": 0,
            "file_types": Counter(),
            "directories": {},
            "large_files": [],
            "empty_directories": [],
            "duplicate_files": [],
            "similar_names": defaultdict(list),
        }

        logger.info("Analyzing directory structure...")

        for root, dirs, files in os.walk(self.downloads_path):
            rel_root = os.path.relpath(root, self.downloads_path)
            analysis["directories"][rel_root] = {
                "file_count": len(files),
                "subdir_count": len(dirs),
                "files": files,
            }

            for file in files:
                file_path = Path(root) / file
                analysis["total_files"] += 1

                try:
                    file_size = file_path.stat().st_size
                    analysis["total_size"] += file_size

                    # Track large files (>10MB)
                    if file_size > 10 * CONSTANT_1024 * CONSTANT_1024:
                        analysis["large_files"].append(
                            {
                                "path": str(file_path),
                                "size": file_size,
                                "size_mb": round(
                                    file_size / (CONSTANT_1024 * CONSTANT_1024), 2
                                ),
                            }
                        )

                    # Track file types
                    file_ext = file_path.suffix.lower()
                    analysis["file_types"][file_ext] += 1

                    # Calculate hash for duplicate detection
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        self.file_hashes[file_hash] = str(file_path)
                        if file_hash in self.duplicates:
                            self.duplicates[file_hash].append(str(file_path))
                        else:
                            self.duplicates[file_hash] = [str(file_path)]

                    # Track similar filenames
                    base_name = file_path.stem.lower()
                    analysis["similar_names"][base_name].append(str(file_path))

                except (OSError, IOError) as e:
                    logger.info(f"Error processing {file_path}: {e}")

        # Find empty directories
        for root, dirs, files in os.walk(self.downloads_path):
            if not dirs and not files:
                rel_root = os.path.relpath(root, self.downloads_path)
                analysis["empty_directories"].append(rel_root)

        # Find duplicates
        for file_hash, file_list in self.duplicates.items():
            if len(file_list) > 1:
                analysis["duplicate_files"].append(
                    {"hash": file_hash, "files": file_list, "count": len(file_list)}
                )

        analysis["total_directories"] = len(analysis["directories"])
        self.analysis_data = analysis
        return analysis

    def detect_duplicates(self) -> List[Dict]:
        """Detect and categorize duplicate files"""
        duplicates = []

        for file_hash, file_list in self.duplicates.items():
            if len(file_list) > 1:
                # Sort by modification time (keep newest)
                file_info = []
                for file_path in file_list:
                    try:
                        stat = Path(file_path).stat()
                        file_info.append(
                            {
                                "path": file_path,
                                "size": stat.st_size,
                                "mtime": stat.st_mtime,
                                "mtime_str": datetime.fromtimestamp(
                                    stat.st_mtime
                                ).strftime("%Y-%m-%d %H:%M:%S"),
                            }
                        )
                    except OSError:
                        continue

                file_info.sort(key=lambda x: x["mtime"], reverse=True)

                duplicates.append(
                    {
                        "hash": file_hash,
                        "files": file_info,
                        "count": len(file_info),
                        "total_size": sum(f["size"] for f in file_info),
                        "keep_file": file_info[0]["path"],  # Keep newest
                        "remove_files": [
                            f["path"] for f in file_info[1:]
                        ],  # Remove older
                    }
                )

        return duplicates

    def categorize_content(self) -> Dict[str, List[str]]:
        """Categorize content based on file types and names"""
        categories = {
            "ai_content": [],
            "technical_resources": [],
            "creative_projects": [],
            "data_analytics": [],
            "web_business": [],
            "documentation": [],
            "media_files": [],
            "archives": [],
            "configurations": [],
            "unclassified": [],
        }

        # File type mappings
        ai_extensions = {".md", ".txt", ".json", ".csv"}
        ai_keywords = [
            "ai",
            "gpt",
            "chatgpt",
            "claude",
            "perplexity",
            "suno",
            "dalle",
            "midjourney",
            "leonardo",
            "ideogram",
        ]

        tech_extensions = {
            ".py",
            ".js",
            ".html",
            ".css",
            ".sh",
            ".yml",
            ".yaml",
            ".json",
            ".xml",
        }
        tech_keywords = [
            "script",
            "code",
            "technical",
            "development",
            "programming",
            "automation",
        ]

        creative_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".pdf",
            ".psd",
            ".ai",
            ".mp4",
            ".mp3",
            ".wav",
        }
        creative_keywords = [
            "creative",
            "design",
            "art",
            "image",
            "video",
            "audio",
            "story",
            "narrative",
        ]

        data_extensions = {".csv", ".xlsx", ".json", ".xml", ".sql", ".db"}
        data_keywords = ["data", "export", "analytics", "dataset", "analysis", "report"]

        web_extensions = {".html", ".css", ".js", ".php", ".asp", ".jsp"}
        web_keywords = [
            "web",
            "website",
            "business",
            "shop",
            "notion",
            "quantumforge",
            "avatararts",
        ]

        doc_extensions = {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"}
        doc_keywords = ["document", "conversation", "chat", "export", "backup"]

        media_extensions = {
            ".mp4",
            ".avi",
            ".mov",
            ".mp3",
            ".wav",
            ".flac",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
        }

        archive_extensions = {".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"}

        config_extensions = {".json", ".yml", ".yaml", ".conf", ".config", ".ini"}
        config_keywords = ["config", "settings", "carbon", "notion", "shop"]

        for file_path in self.file_hashes.values():
            path_obj = Path(file_path)
            file_name = path_obj.name.lower()
            file_ext = path_obj.suffix.lower()

            # Check file extensions and keywords
            if (
                any(keyword in file_name for keyword in ai_keywords)
                or file_ext in ai_extensions
            ):
                categories["ai_content"].append(file_path)
            elif (
                any(keyword in file_name for keyword in tech_keywords)
                or file_ext in tech_extensions
            ):
                categories["technical_resources"].append(file_path)
            elif (
                any(keyword in file_name for keyword in creative_keywords)
                or file_ext in creative_extensions
            ):
                categories["creative_projects"].append(file_path)
            elif (
                any(keyword in file_name for keyword in data_keywords)
                or file_ext in data_extensions
            ):
                categories["data_analytics"].append(file_path)
            elif (
                any(keyword in file_name for keyword in web_keywords)
                or file_ext in web_extensions
            ):
                categories["web_business"].append(file_path)
            elif (
                any(keyword in file_name for keyword in doc_keywords)
                or file_ext in doc_extensions
            ):
                categories["documentation"].append(file_path)
            elif file_ext in media_extensions:
                categories["media_files"].append(file_path)
            elif file_ext in archive_extensions:
                categories["archives"].append(file_path)
            elif (
                any(keyword in file_name for keyword in config_keywords)
                or file_ext in config_extensions
            ):
                categories["configurations"].append(file_path)
            else:
                categories["unclassified"].append(file_path)

        return categories

    def generate_organization_plan(self) -> Dict:
        """Generate a comprehensive organization plan"""
        categories = self.categorize_content()
        duplicates = self.detect_duplicates()

        plan = {
            "new_structure": {
                "00_ARCHIVES": [],
                "01_AI_CONTENT": [],
                "02_TECHNICAL_RESOURCES": [],
                "03_CREATIVE_PROJECTS": [],
                "04_DATA_ANALYTICS": [],
                "05_WEB_BUSINESS": [],
                "06_DOCUMENTATION": [],
                "07_MEDIA_FILES": [],
                "08_CONFIGURATIONS": [],
                "09_CONSOLIDATED": [],
            },
            "duplicate_actions": [],
            "consolidation_opportunities": [],
            "file_movements": [],
            "cleanup_actions": [],
        }

        # Map categories to new structure
        category_mapping = {
            "ai_content": "01_AI_CONTENT",
            "technical_resources": "02_TECHNICAL_RESOURCES",
            "creative_projects": "03_CREATIVE_PROJECTS",
            "data_analytics": "04_DATA_ANALYTICS",
            "web_business": "05_WEB_BUSINESS",
            "documentation": "06_DOCUMENTATION",
            "media_files": "07_MEDIA_FILES",
            "archives": "00_ARCHIVES",
            "configurations": "08_CONFIGURATIONS",
            "unclassified": "09_CONSOLIDATED",
        }

        for category, files in categories.items():
            target_dir = category_mapping.get(category, "09_CONSOLIDATED")
            for file_path in files:
                plan["file_movements"].append(
                    {
                        "source": file_path,
                        "destination": f"{target_dir}/{Path(file_path).name}",
                        "category": category,
                    }
                )

        # Add duplicate actions
        for dup in duplicates:
            plan["duplicate_actions"].append(
                {
                    "action": "keep_newest",
                    "keep": dup["keep_file"],
                    "remove": dup["remove_files"],
                    "savings_mb": round(
                        dup["total_size"] / (CONSTANT_1024 * CONSTANT_1024), 2
                    ),
                }
            )

        # Add consolidation opportunities
        consolidation_opportunities = [
            {
                "type": "chatgpt_conversations",
                "files": [
                    f
                    for f in self.analysis_data.get("similar_names", {}).get(
                        "chatgpt_conversation", []
                    )
                ],
                "action": "merge_into_single_archive",
            },
            {
                "type": "ideogram_pdfs",
                "files": [
                    f
                    for f in self.analysis_data.get("similar_names", {}).get(
                        "ideogram_copy", []
                    )
                ],
                "action": "organize_by_date",
            },
            {
                "type": "python_scripts",
                "files": [
                    f
                    for f in self.analysis_data.get("similar_names", {}).get(
                        "scripty", []
                    )
                ],
                "action": "consolidate_versions",
            },
        ]

        plan["consolidation_opportunities"] = consolidation_opportunities

        self.organization_plan = plan
        return plan

    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        report = []
        report.append("# Downloads Directory Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary statistics
        report.append("## Summary Statistics")
        report.append(f"- Total Files: {self.analysis_data.get('total_files', 0):,}")
        report.append(
            f"- Total Directories: {self.analysis_data.get('total_directories', 0):,}"
        )
        report.append(
            f"- Total Size: {self.analysis_data.get('total_size', 0) / (CONSTANT_1024*CONSTANT_1024*CONSTANT_1024):.2f} GB"
        )
        report.append(
            f"- Duplicate Files: {len(self.analysis_data.get('duplicate_files', []))}"
        )
        report.append(
            f"- Empty Directories: {len(self.analysis_data.get('empty_directories', []))}"
        )
        report.append("")

        # File type breakdown
        report.append("## File Type Breakdown")
        for ext, count in self.analysis_data.get("file_types", {}).most_common(10):
            report.append(f"- {ext or 'no extension'}: {count:,} files")
        report.append("")

        # Duplicate analysis
        report.append("## Duplicate File Analysis")
        duplicates = self.detect_duplicates()
        total_duplicate_size = sum(dup["total_size"] for dup in duplicates)
        report.append(f"- Duplicate Groups: {len(duplicates)}")
        report.append(
            f"- Potential Space Savings: {total_duplicate_size / (CONSTANT_1024*CONSTANT_1024):.2f} MB"
        )
        report.append("")

        for i, dup in enumerate(duplicates[:5], 1):  # Show top 5
            report.append(f"### Duplicate Group {i}")
            report.append(f"- Files: {dup['count']}")
            report.append(
                f"- Total Size: {dup['total_size'] / (CONSTANT_1024*CONSTANT_1024):.2f} MB"
            )
            report.append(f"- Keep: {Path(dup['keep_file']).name}")
            report.append(f"- Remove: {len(dup['remove_files'])} files")
            report.append("")

        # Organization plan
        report.append("## Organization Plan")
        categories = self.categorize_content()
        for category, files in categories.items():
            if files:
                report.append(
                    f"- {category.replace('_', ' ').title()}: {len(files)} files"
                )
        report.append("")

        # Recommendations
        report.append("## Recommendations")
        report.append("1. Create backup before proceeding with reorganization")
        report.append("2. Remove duplicate files to save space")
        report.append("3. Consolidate similar content into organized categories")
        report.append("4. Implement automated organization for future downloads")
        report.append("5. Regular cleanup schedule to prevent accumulation")

        return Path("\n").join(report)

    def save_analysis(self, output_path: str = None):
        """Save analysis data to JSON file"""
        if output_path is None:
            output_path = f"/Users/steven/Downloads_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "directory_path": str(self.downloads_path),
            "backup_path": self.backup_path,
            "analysis": self.analysis_data,
            "duplicates": self.detect_duplicates(),
            "categories": self.categorize_content(),
            "organization_plan": self.organization_plan,
        }

        with open(output_path, "w") as f:
            json.dump(analysis_data, f, indent=2, default=str)

        logger.info(f"Analysis saved to: {output_path}")
        return output_path

    def run_full_analysis(self):
        """Run complete analysis and generate reports"""
        logger.info("Starting Downloads Directory Analysis...")
        logger.info("=" * 50)

        # Create backup
        backup_path = self.create_backup()
        logger.info(f"Backup created: {backup_path}")

        # Analyze directory structure
        logger.info("\nAnalyzing directory structure...")
        self.analyze_directory_structure()

        # Detect duplicates
        logger.info("Detecting duplicates...")
        duplicates = self.detect_duplicates()
        logger.info(f"Found {len(duplicates)} duplicate groups")

        # Categorize content
        logger.info("Categorizing content...")
        categories = self.categorize_content()
        for category, files in categories.items():
            if files:
                logger.info(f"  {category}: {len(files)} files")

        # Generate organization plan
        logger.info("Generating organization plan...")
        self.generate_organization_plan()

        # Generate report
        logger.info("Generating analysis report...")
        report = self.generate_report()

        # Save analysis
        analysis_file = self.save_analysis()

        # Save report
        report_file = f"/Users/steven/Downloads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, "w") as f:
            f.write(report)

        logger.info(f"\nAnalysis complete!")
        logger.info(f"Report saved to: {report_file}")
        logger.info(f"Analysis data saved to: {analysis_file}")
        logger.info(f"Backup created at: {backup_path}")

        return {
            "report_file": report_file,
            "analysis_file": analysis_file,
            "backup_path": backup_path,
            "duplicates_found": len(duplicates),
            "total_files": self.analysis_data.get("total_files", 0),
            "total_size_gb": self.analysis_data.get("total_size", 0)
            / (CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024),
        }


def main():
    """Main function to run the Downloads organizer"""
    organizer = DownloadsOrganizer()

    try:
        results = organizer.run_full_analysis()

        logger.info(Path("\n") + "=" * 50)
        logger.info("ANALYSIS SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total files analyzed: {results['total_files']:,}")
        logger.info(f"Total size: {results['total_size_gb']:.2f} GB")
        logger.info(f"Duplicates found: {results['duplicates_found']}")
        logger.info(f"Report: {results['report_file']}")
        logger.info(f"Analysis data: {results['analysis_file']}")
        logger.info(f"Backup: {results['backup_path']}")

    except Exception as e:
        logger.info(f"Error during analysis: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
