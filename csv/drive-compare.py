"""
Drive Csv Compare

This module provides functionality for drive csv compare.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Compare CSV analysis results from both drives
"""

from pathlib import Path
import csv
import os
import pandas as pd
from collections import defaultdict


def load_csv_data(file_path):
    """Load CSV data and return as list of dictionaries"""
    if not os.path.exists(file_path):
        return []

    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def find_duplicates(data1, data2, file_type):
    """Find duplicate files between two datasets"""
    # Group by filename and size
    files1 = defaultdict(list)
    files2 = defaultdict(list)

    for item in data1:
        key = (item["File_Name"], item["File_Size_Bytes"])
        files1[key].append(item)

    for item in data2:
        key = (item["File_Name"], item["File_Size_Bytes"])
        files2[key].append(item)

    duplicates = []
    for key in files1:
        if key in files2:
            duplicates.append(
                {
                    "filename": key[0],
                    "size_bytes": key[1],
                    "file_type": file_type,
                    "drive1_files": files1[key],
                    "drive2_files": files2[key],
                }
            )

    return duplicates


def analyze_file_type(file_type, drive1_file, drive2_file):
    """Analyze a specific file type across both drives"""
    logger.info(f"\n=== {file_type} FILES ANALYSIS ===")

    # Load data
    data1 = load_csv_data(drive1_file)
    data2 = load_csv_data(drive2_file)

    logger.info(f"2T-Xx {file_type} files: {len(data1)}")
    logger.info(f"DeVonDaTa {file_type} files: {len(data2)}")

    if not data1 and not data2:
        logger.info("No data found for this file type")
        return

    # Calculate total sizes
    total_size1 = sum(int(item["File_Size_Bytes"]) for item in data1 if item["File_Size_Bytes"].isdigit())
    total_size2 = sum(int(item["File_Size_Bytes"]) for item in data2 if item["File_Size_Bytes"].isdigit())

    logger.info(f"2T-Xx total size: {total_size1 / CONSTANT_1024 / CONSTANT_1024:.1f} MB")
    logger.info(f"DeVonDaTa total size: {total_size2 / CONSTANT_1024 / CONSTANT_1024:.1f} MB")

    # Find duplicates
    duplicates = find_duplicates(data1, data2, file_type)
    logger.info(f"Duplicate files found: {len(duplicates)}")

    if duplicates:
        logger.info("Sample duplicates:")
        for dup in duplicates[:5]:
            logger.info(f"  {dup['filename']} ({dup['size_bytes']} bytes)")

    return {
        "file_type": file_type,
        "drive1_count": len(data1),
        "drive2_count": len(data2),
        "drive1_size_mb": total_size1 / CONSTANT_1024 / CONSTANT_1024,
        "drive2_size_mb": total_size2 / CONSTANT_1024 / CONSTANT_1024,
        "duplicates": len(duplicates),
        "duplicate_details": duplicates,
    }


def create_merge_recommendations(analysis_results):
    """Create merge recommendations based on analysis"""
    logger.info("\n=== MERGE RECOMMENDATIONS ===")

    recommendations = []

    for result in analysis_results:
        file_type = result["file_type"]
        drive1_count = result["drive1_count"]
        drive2_count = result["drive2_count"]
        duplicates = result["duplicates"]

        logger.info(f"\n{file_type} Files:")
        logger.info(f"  2T-Xx: {drive1_count} files")
        logger.info(f"  DeVonDaTa: {drive2_count} files")
        logger.info(f"  Duplicates: {duplicates}")

        if drive1_count > drive2_count:
            recommendation = "Keep 2T-Xx as primary, move unique from DeVonDaTa"
        elif drive2_count > drive1_count:
            recommendation = "Move DeVonDaTa files to 2T-Xx, organize together"
        else:
            recommendation = "Merge and organize both drives"

        logger.info(f"  Recommendation: {recommendation}")

        recommendations.append(
            {
                "file_type": file_type,
                "drive1_count": drive1_count,
                "drive2_count": drive2_count,
                "duplicates": duplicates,
                "recommendation": recommendation,
            }
        )

    return recommendations


def save_analysis_report(analysis_results, recommendations):
    """Save analysis report to CSV"""
    # Save detailed analysis
    with open("/Users/steven/drive_analysis_comparison.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "File_Type",
                "Drive1_Count",
                "Drive2_Count",
                "Drive1_Size_MB",
                "Drive2_Size_MB",
                "Duplicates",
                "Recommendation",
            ]
        )

        for result in analysis_results:
            writer.writerow(
                [
                    result["file_type"],
                    result["drive1_count"],
                    result["drive2_count"],
                    f"{result['drive1_size_mb']:.1f}",
                    f"{result['drive2_size_mb']:.1f}",
                    result["duplicates"],
                    recommendations[analysis_results.index(result)]["recommendation"],
                ]
            )

    # Save duplicate details
    all_duplicates = []
    for result in analysis_results:
        for dup in result["duplicate_details"]:
            all_duplicates.append(
                {
                    "file_type": dup["file_type"],
                    "filename": dup["filename"],
                    "size_bytes": dup["size_bytes"],
                    "drive1_path": dup["drive1_files"][0]["File_Path"] if dup["drive1_files"] else "",
                    "drive2_path": dup["drive2_files"][0]["File_Path"] if dup["drive2_files"] else "",
                    "action": "Keep 2T-Xx version",
                }
            )

    if all_duplicates:
        with open("/Users/steven/duplicate_files_found.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["File_Type", "Filename", "Size_Bytes", "Drive1_Path", "Drive2_Path", "Recommended_Action"])

            for dup in all_duplicates:
                writer.writerow(
                    [
                        dup["file_type"],
                        dup["filename"],
                        dup["size_bytes"],
                        dup["drive1_path"],
                        dup["drive2_path"],
                        dup["action"],
                    ]
                )

    logger.info(f"\nAnalysis saved to:")
    logger.info(f"  /Users/steven/drive_analysis_comparison.csv")
    logger.info(f"  /Users/steven/duplicate_files_found.csv")


def main():
    """main function."""

    logger.info("=== DRIVE CSV COMPARISON ANALYSIS ===")

    # Check if analysis directory exists
    analysis_dir = Path("/Users/steven/drive_analysis_output")
    if not os.path.exists(analysis_dir):
        logger.info(f"Analysis directory not found: {analysis_dir}")
        logger.info("Please run the batch analysis script first.")
        return

    # File type configurations
    file_types = [
        ("ZIP", "2T-Xx_zip_files.csv", "DeVonDaTa_zip_files.csv"),
        ("MP4", "2T-Xx_mp4_files.csv", "DeVonDaTa_mp4_files.csv"),
        ("JPG", "2T-Xx_jpg_files.csv", "DeVonDaTa_jpg_files.csv"),
        ("PNG", "2T-Xx_png_files.csv", "DeVonDaTa_png_files.csv"),
        ("MP3", "2T-Xx_mp3_files.csv", "DeVonDaTa_mp3_files.csv"),
        ("PDF", "2T-Xx_pdf_files.csv", "DeVonDaTa_pdf_files.csv"),
        ("PSD", "2T-Xx_psd_files.csv", "DeVonDaTa_psd_files.csv"),
    ]

    analysis_results = []

    # Analyze each file type
    for file_type, drive1_file, drive2_file in file_types:
        drive1_path = os.path.join(analysis_dir, drive1_file)
        drive2_path = os.path.join(analysis_dir, drive2_file)

        result = analyze_file_type(file_type, drive1_path, drive2_path)
        if result:
            analysis_results.append(result)

    # Create recommendations
    recommendations = create_merge_recommendations(analysis_results)

    # Save analysis report
    save_analysis_report(analysis_results, recommendations)

    logger.info("\n=== ANALYSIS COMPLETE ===")
    logger.info("Review the CSV files for detailed merge recommendations.")


if __name__ == "__main__":
    main()
