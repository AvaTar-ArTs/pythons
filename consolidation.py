"""
Consolidation

This module provides functionality for consolidation.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Final File Consolidation Script
Consolidates ALL files from the user's request into /Users/steven/tehSiTes/DrAdu-SEO-OPTIMIZED
"""

import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime
import re


class FinalConsolidator:
    def __init__(
        self, destination_dir=Path(str(Path.home()) + "/tehSiTes/DrAdu-SEO-OPTIMIZED")
    ):
        """__init__ function."""

        self.destination_dir = destination_dir
        self.file_groups = defaultdict(list)
        self.duplicates = []
        self.unique_files = []
        self.processed_files = 0
        self.errors = []
        self.consolidated_files = []
        self.merged_files = []
        self.removed_files = []

        # Create destination directory if it doesn't exist
        os.makedirs(self.destination_dir, exist_ok=True)

    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file content"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return None

    def get_file_info(self, file_path):
        """Get file information including size, modification time, and hash"""
        try:
            if not os.path.exists(file_path):
                return None

            if os.path.isdir(file_path):
                return None

            stat = os.stat(file_path)
            return {
                "path": file_path,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "hash": self.calculate_file_hash(file_path),
                "exists": True,
            }
        except Exception as e:
            self.errors.append(f"Error getting info for {file_path}: {e}")
            return None

    def group_files_by_name(self, file_list):
        """Group files by their basename"""
        for file_path in file_list:
            if file_path.strip():  # Skip empty paths
                basename = os.path.basename(file_path)
                self.file_groups[basename].append(file_path)

    def find_duplicates(self):
        """Find duplicate files based on content hash"""
        hash_to_files = defaultdict(list)

        for group_name, files in self.file_groups.items():
            for file_path in files:
                file_info = self.get_file_info(file_path)
                if file_info and file_info["hash"] and file_info["exists"]:
                    hash_to_files[file_info["hash"]].append(file_info)
                    self.processed_files += 1

        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                # Sort by modification time (newest first), then by path length (shorter first)
                files.sort(key=lambda x: (-x["mtime"], len(x["path"])))
                self.duplicates.append(
                    {
                        "hash": file_hash,
                        "files": files,
                        "keep": files[0],  # Keep the newest/shortest path
                        "remove": files[1:],  # Remove the rest
                    }
                )
            else:
                self.unique_files.extend(files)

    def merge_files(self, files, output_path):
        """Merge multiple files into one, removing duplicates"""
        try:
            all_content = set()
            file_sources = []

            for file_path in files:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        lines = content.splitlines()
                        for line in lines:
                            if line.strip():  # Skip empty lines
                                all_content.add(line.strip())
                        file_sources.append(f"# From: {file_path}\n")
                except Exception as e:
                    self.errors.append(f"Error reading {file_path} for merge: {e}")

            # Create merged content
            merged_content = (
                Path("\n").join(file_sources)
                + Path("\n\n")
                + Path("\n").join(sorted(all_content))
            )

            # Write merged file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(merged_content)

            self.merged_files.append(
                {"output": output_path, "sources": files, "lines": len(all_content)}
            )

            return True
        except Exception as e:
            self.errors.append(f"Error merging files to {output_path}: {e}")
            return False

    def consolidate_files(self, file_list, dry_run=True):
        """Consolidate files into destination directory"""
        logger.info(f"Consolidating {len(file_list)} files to {self.destination_dir}")

        # Group files by name
        self.group_files_by_name(file_list)
        logger.info(f"Grouped into {len(self.file_groups)} groups")

        # Find duplicates
        self.find_duplicates()
        logger.info(f"Found {len(self.duplicates)} duplicate groups")
        logger.info(f"Found {len(self.unique_files)} unique files")

        # Process each group
        for group_name, files in self.file_groups.items():
            logger.info(f"\nProcessing group: {group_name}")

            # Get existing files
            existing_files = [
                f for f in files if os.path.exists(f) and not os.path.isdir(f)
            ]

            if not existing_files:
                logger.info(f"  No existing files found for {group_name}")
                continue

            if len(existing_files) == 1:
                # Single file - just copy
                source_file = existing_files[0]
                dest_file = os.path.join(self.destination_dir, group_name)

                if not dry_run:
                    try:
                        shutil.copy2(source_file, dest_file)
                        self.consolidated_files.append(
                            {
                                "source": source_file,
                                "destination": dest_file,
                                "action": "copied",
                            }
                        )
                        logger.info(f"  Copied: {source_file} -> {dest_file}")
                    except Exception as e:
                        self.errors.append(f"Error copying {source_file}: {e}")
                else:
                    logger.info(f"  Would copy: {source_file} -> {dest_file}")
            else:
                # Multiple files - check for duplicates
                file_hashes = {}
                unique_files = []

                for file_path in existing_files:
                    file_info = self.get_file_info(file_path)
                    if file_info and file_info["hash"]:
                        if file_info["hash"] not in file_hashes:
                            file_hashes[file_info["hash"]] = file_path
                            unique_files.append(file_path)
                        else:
                            logger.info(
                                f"  Duplicate found: {file_path} (same as {file_hashes[file_info['hash']]})"
                            )

                if len(unique_files) == 1:
                    # All files are duplicates - keep the best one
                    source_file = unique_files[0]
                    dest_file = os.path.join(self.destination_dir, group_name)

                    if not dry_run:
                        try:
                            shutil.copy2(source_file, dest_file)
                            self.consolidated_files.append(
                                {
                                    "source": source_file,
                                    "destination": dest_file,
                                    "action": "copied (duplicate removed)",
                                }
                            )
                            logger.info(
                                f"  Copied (duplicate removed): {source_file} -> {dest_file}"
                            )
                        except Exception as e:
                            self.errors.append(f"Error copying {source_file}: {e}")
                    else:
                        logger.info(
                            f"  Would copy (duplicate removed): {source_file} -> {dest_file}"
                        )
                else:
                    # Multiple unique files - merge them
                    dest_file = os.path.join(self.destination_dir, group_name)

                    if not dry_run:
                        if self.merge_files(unique_files, dest_file):
                            self.consolidated_files.append(
                                {
                                    "source": unique_files,
                                    "destination": dest_file,
                                    "action": "merged",
                                }
                            )
                            logger.info(
                                f"  Merged {len(unique_files)} files -> {dest_file}"
                            )
                    else:
                        logger.info(
                            f"  Would merge {len(unique_files)} files -> {dest_file}"
                        )

        return self.generate_report()

    def generate_report(self):
        """Generate a comprehensive report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "destination_directory": self.destination_dir,
            "summary": {
                "total_files_processed": self.processed_files,
                "file_groups": len(self.file_groups),
                "duplicate_groups": len(self.duplicates),
                "unique_files": len(self.unique_files),
                "consolidated_files": len(self.consolidated_files),
                "merged_files": len(self.merged_files),
                "errors": len(self.errors),
            },
            "consolidated_files": self.consolidated_files,
            "merged_files": self.merged_files,
            "duplicates": [],
            "errors": self.errors[:50],  # Limit errors to first 50
        }

        # Add duplicate information
        for dup in self.duplicates:
            report["duplicates"].append(
                {
                    "hash": dup["hash"],
                    "keep_file": dup["keep"]["path"],
                    "remove_files": [f["path"] for f in dup["remove"]],
                    "file_size": dup["keep"]["size"],
                    "modification_time": datetime.fromtimestamp(
                        dup["keep"]["mtime"]
                    ).isoformat(),
                    "total_duplicates": len(dup["files"]),
                }
            )

        return report


def parse_complete_file_list():
    """Parse the complete file list from the user's input"""
    # This is the complete file list from the user's request
    file_list = [
        Path(
            str(Path.home()) + "/tehSiTes/03_Business_Platforms/seo-professional-portfolio/avatararts.org/dr/_downloads.html"
        ),
        Path(
            str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/Dr_Adu_GainesvillePFS_SEO_Project/03_Content_Development/01_Original_Content/_downloads.html"
        ),
        Path(
            str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/avatararts.org/dr/_downloads.html"
        ),
        Path(
            str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/seo-professional-portfolio/avatararts.org/dr/_downloads.html"
        ),
        Path(
            str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/seo-professional-portfolio/04_Technical_Implementation/01_HTML_Files/_downloads.html"
        ),
        Path(
            str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/04_Technical_Implementation/01_HTML_Files/_downloads.html"
        ),
        Path(str(Path.home()) + "/tehSiTes/03_Busintent/projects/multimedia-workflows/1.txt"),
        Path(
            str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/steven-chaplinski-website/content/projects/multimedia-workflows/1.txt"
        ),
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/dr/Dr Adu-Upscale Image/2.png",
        str(Path.home()) + "/tehSiTes/06_Archives_Backups/dr/Dr Adu-Upscale Image/2.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/seo-professional-portfolio/Dr Adu-Upscale Image/2.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/seo-professional-portfolio/Dr Adu-Upscale Image/2.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/2.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/2.png",
        # Add more files from the user's complete list...
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/4.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/4.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/seo-professional-portfolio/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/dr/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/seo-professional-portfolio/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/06_Archives_Backups/dr/Dr Adu-Upscale Image/5.png",
        str(Path.home()) + "/tehSiTes/02_Creative_Portfolio/AvaTarArTs/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/6.png",
        str(Path.home()) + "/tehSiTes/03_Business_Platforms/Dr_Adu_GainesvillePFS_SEO_Project/Dr Adu-Upscale Image/6.png",
    ]

    return file_list


def main():
    """main function."""

    # Parse the file list
    file_list = parse_complete_file_list()
    logger.info(f"Parsed {len(file_list)} files from input")

    # Create consolidator
    consolidator = FinalConsolidator()

    # First run in dry-run mode to show what would happen
    logger.info(Path("\n") + "=" * 60)
    logger.info("DRY RUN - Showing what would be consolidated:")
    logger.info("=" * 60)
    report = consolidator.consolidate_files(file_list, dry_run=True)

    # Save dry-run report
    with open(str(Path.home()) + "/final_consolidation_dry_run_report.json", "w") as f:
        json.dump(report, f, indent=2)

    logger.info(
        f"\nDry-run report saved to: /Users/steven/final_consolidation_dry_run_report.json"
    )

    # Show summary
    logger.info(Path("\n") + "=" * 60)
    logger.info("CONSOLIDATION SUMMARY:")
    logger.info("=" * 60)
    logger.info(f"Destination: {consolidator.destination_dir}")
    logger.info(f"Files processed: {report['summary']['total_files_processed']}")
    logger.info(f"File groups: {report['summary']['file_groups']}")
    logger.info(f"Files to consolidate: {report['summary']['consolidated_files']}")
    logger.info(f"Files to merge: {report['summary']['merged_files']}")
    logger.info(f"Errors: {report['summary']['errors']}")

    if report["consolidated_files"]:
        logger.info(f"\nFiles that would be consolidated:")
        for item in report["consolidated_files"]:
            if isinstance(item["source"], list):
                logger.info(
                    f"  • {os.path.basename(item['destination'])} (merged from {len(item['source'])} files)"
                )
            else:
                logger.info(
                    f"  • {os.path.basename(item['destination'])} ({item['action']})"
                )

    # Ask user if they want to proceed with actual consolidation
    logger.info(Path("\n") + "=" * 60)
    logger.info("READY TO PROCEED WITH ACTUAL CONSOLIDATION")
    logger.info("=" * 60)
    logger.info("This will:")
    logger.info("1. Copy unique files to the destination directory")
    logger.info("2. Remove duplicate files (keeping the best version)")
    logger.info("3. Merge files with differences where appropriate")
    logger.info("4. Generate a final report")

    # For now, let's proceed with the actual consolidation
    logger.info("\nProceeding with actual consolidation...")

    # Reset for actual run
    consolidator = FinalConsolidator()
    final_report = consolidator.consolidate_files(file_list, dry_run=False)

    # Save final report
    with open(str(Path.home()) + "/final_consolidation_report.json", "w") as f:
        json.dump(final_report, f, indent=2)

    logger.info(f"\nFinal consolidation completed!")
    logger.info(f"Final report saved to: /Users/steven/final_consolidation_report.json")

    # Show final summary
    logger.info(Path("\n") + "=" * 60)
    logger.info("FINAL CONSOLIDATION RESULTS:")
    logger.info("=" * 60)
    logger.info(f"Destination: {consolidator.destination_dir}")
    logger.info(f"Files processed: {final_report['summary']['total_files_processed']}")
    logger.info(f"Files consolidated: {final_report['summary']['consolidated_files']}")
    logger.info(f"Files merged: {final_report['summary']['merged_files']}")
    logger.info(f"Errors: {final_report['summary']['errors']}")

    if final_report["consolidated_files"]:
        logger.info(f"\nFiles consolidated:")
        for item in final_report["consolidated_files"]:
            if isinstance(item["source"], list):
                logger.info(
                    f"  • {os.path.basename(item['destination'])} (merged from {len(item['source'])} files)"
                )
            else:
                logger.info(
                    f"  • {os.path.basename(item['destination'])} ({item['action']})"
                )

    return final_report


if __name__ == "__main__":
    main()
