"""
Content Aware Csv Deduper

This module provides functionality for content aware csv deduper.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Content-Aware File Deduplication and Organization System
Analyzes CSV file inventory and provides intelligent deduplication recommendations
"""

import pandas as pd
import hashlib
import os
import re
from collections import defaultdict, Counter
from pathlib import Path
import json
from datetime import datetime
import argparse


class ContentAwareDeduplicator:
    def __init__(self, csv_file):
        """__init__ function."""

        self.csv_file = csv_file
        self.df = None
        self.duplicates = defaultdict(list)
        self.similar_files = defaultdict(list)
        self.analysis_results = {}

    def load_data(self):
        """Load and preprocess the CSV data"""
        logger.info("Loading CSV data...")
        self.df = pd.read_csv(self.csv_file)
        logger.info(f"Loaded {len(self.df)} files")

        # Clean and standardize data
        self.df["File Size"] = self.df["File Size"].str.replace(" KB", "").str.replace(" MB", "").str.replace(" GB", "")
        self.df["File Size"] = pd.to_numeric(self.df["File Size"], errors="coerce")

        # Extract file extensions
        self.df["Extension"] = self.df["Filename"].str.extract(r"\.([^.]+)$")[0]
        self.df["Base_Name"] = self.df["Filename"].str.replace(r"\.[^.]+$", "", regex=True)

        logger.info("Data preprocessing complete")

    def find_exact_duplicates(self):
        """Find files with identical names and sizes"""
        logger.info("Finding exact duplicates...")

        # Group by filename and size
        grouped = self.df.groupby(["Filename", "File Size"])

        for (filename, size), group in grouped:
            if len(group) > 1:
                self.duplicates[filename] = group.to_dict("records")

        logger.info(f"Found {len(self.duplicates)} files with exact duplicates")

    def find_similar_files(self):
        """Find files with similar names (content-aware)"""
        logger.info("Finding similar files...")

        # Group by extension for better analysis
        for ext in self.df["Extension"].dropna().unique():
            ext_files = self.df[self.df["Extension"] == ext]

            # Find similar base names
            base_names = ext_files["Base_Name"].tolist()

            for i, name1 in enumerate(base_names):
                for j, name2 in enumerate(base_names[i + 1 :], i + 1):
                    similarity = self.calculate_similarity(name1, name2)
                    if similarity > 0.7:  # 70% similarity threshold
                        file1 = ext_files.iloc[i]
                        file2 = ext_files.iloc[j]

                        key = f"{name1}_{ext}"
                        if key not in self.similar_files:
                            self.similar_files[key] = []

                        self.similar_files[key].extend([file1.to_dict(), file2.to_dict()])

        logger.info(f"Found {len(self.similar_files)} groups of similar files")

    def calculate_similarity(self, name1, name2):
        """Calculate similarity between two filenames"""
        # Remove common prefixes/suffixes
        name1_clean = re.sub(r"^(copy|backup|old|new|temp|tmp|_|-)", "", name1.lower())
        name2_clean = re.sub(r"^(copy|backup|old|new|temp|tmp|_|-)", "", name2.lower())

        # Remove numbers and special characters
        name1_clean = re.sub(r"[0-9_-]", "", name1_clean)
        name2_clean = re.sub(r"[0-9_-]", "", name2_clean)

        # Calculate Jaccard similarity
        set1 = set(name1_clean.split())
        set2 = set(name2_clean.split())

        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def analyze_file_patterns(self):
        """Analyze file patterns and categories"""
        logger.info("Analyzing file patterns...")

        patterns = {
            "python_files": self.df[self.df["Extension"] == "py"],
            "javascript_files": self.df[self.df["Extension"] == "js"],
            "html_files": self.df[self.df["Extension"] == "html"],
            "json_files": self.df[self.df["Extension"] == "json"],
            "markdown_files": self.df[self.df["Extension"] == "md"],
            "text_files": self.df[self.df["Extension"] == "txt"],
            "pdf_files": self.df[self.df["Extension"] == "pdf"],
        }

        self.analysis_results["file_types"] = {}
        for category, files in patterns.items():
            self.analysis_results["file_types"][category] = {
                "count": len(files),
                "total_size": files["File Size"].sum(),
                "avg_size": files["File Size"].mean(),
            }

        # Find common duplicate patterns
        common_duplicates = self.df["Filename"].value_counts()
        self.analysis_results["common_duplicates"] = common_duplicates.head(20).to_dict()

        logger.info("File pattern analysis complete")

    def generate_recommendations(self):
        """Generate deduplication recommendations"""
        logger.info("Generating recommendations...")

        recommendations = {
            "exact_duplicates": [],
            "similar_files": [],
            "large_files": [],
            "old_files": [],
            "organization_suggestions": [],
        }

        # Exact duplicates
        for filename, files in self.duplicates.items():
            if len(files) > 1:
                # Keep the most recent file
                files_sorted = sorted(files, key=lambda x: x["Creation Date"], reverse=True)
                keep_file = files_sorted[0]
                remove_files = files_sorted[1:]

                recommendations["exact_duplicates"].append(
                    {
                        "filename": filename,
                        "keep": keep_file,
                        "remove": remove_files,
                        "space_saved": sum(f["File Size"] for f in remove_files),
                    }
                )

        # Similar files
        for group_name, files in self.similar_files.items():
            if len(files) > 1:
                # Group by size to find potential duplicates
                size_groups = defaultdict(list)
                for file in files:
                    size_groups[file["File Size"]].append(file)

                for size, size_files in size_groups.items():
                    if len(size_files) > 1:
                        recommendations["similar_files"].append(
                            {"group": group_name, "files": size_files, "potential_duplicates": len(size_files)}
                        )

        # Large files
        large_files = self.df[self.df["File Size"] > CONSTANT_100]  # > 100MB
        recommendations["large_files"] = large_files.nlargest(20, "File Size").to_dict("records")

        # Old files (assuming older than 1 year)
        self.df["Creation Date"] = pd.to_datetime(self.df["Creation Date"], errors="coerce")
        old_files = self.df[self.df["Creation Date"] < "2024-01-01"]
        recommendations["old_files"] = old_files.nlargest(20, "File Size").to_dict("records")

        self.analysis_results["recommendations"] = recommendations

        logger.info("Recommendations generated")

    def generate_cleanup_script(self):
        """Generate a Python script for automated cleanup"""
        script_content = '''#!/usr/bin/env python3
"""
Auto-generated cleanup script based on content analysis
"""

import os
import shutil
from pathlib import Path

def cleanup_duplicates():
    """Remove duplicate files based on analysis"""
    
    # Exact duplicates to remove
    duplicates_to_remove = [
'''

        # Add exact duplicates to remove
        for rec in self.analysis_results["recommendations"]["exact_duplicates"]:
            for file_to_remove in rec["remove"]:
                script_content += f"        '{file_to_remove['Original Path']}/{file_to_remove['Filename']}',\n"

        script_content += """    ]
    
    removed_count = 0
    space_saved = 0
    
    for file_path in duplicates_to_remove:
        if os.path.exists(file_path):
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                removed_count += 1
                space_saved += file_size
                logger.info(f"Removed: {file_path}")
            except Exception as e:
                logger.info(f"Error removing {file_path}: {e}")
    
    logger.info(f"\\nCleanup complete: {removed_count} files removed, {space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB saved")

if __name__ == "__main__":
    cleanup_duplicates()
"""

        with open("/Users/steven/clean/auto_cleanup.py", "w") as f:
            f.write(script_content)

        logger.info("Cleanup script generated: /Users/steven/clean/auto_cleanup.py")

    def save_analysis_report(self):
        """Save detailed analysis report"""
        report = {
            "analysis_date": datetime.now().isoformat(),
            "total_files": len(self.df),
            "total_size": self.df["File Size"].sum(),
            "file_types": self.analysis_results["file_types"],
            "common_duplicates": self.analysis_results["common_duplicates"],
            "exact_duplicates_count": len(self.duplicates),
            "similar_files_count": len(self.similar_files),
            "recommendations": self.analysis_results["recommendations"],
        }

        with open("/Users/steven/clean/analysis_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)

        logger.info("Analysis report saved: /Users/steven/clean/analysis_report.json")

    def run_analysis(self):
        """Run complete analysis"""
        logger.info("Starting content-aware analysis...")

        self.load_data()
        self.find_exact_duplicates()
        self.find_similar_files()
        self.analyze_file_patterns()
        self.generate_recommendations()
        self.generate_cleanup_script()
        self.save_analysis_report()

        logger.info("\\nAnalysis complete!")
        logger.info(f"Found {len(self.duplicates)} exact duplicate groups")
        logger.info(f"Found {len(self.similar_files)} similar file groups")

        # Calculate potential space savings
        total_space_saved = 0
        for rec in self.analysis_results["recommendations"]["exact_duplicates"]:
            total_space_saved += rec["space_saved"]

        logger.info(f"Potential space savings: {total_space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")


def main():
    """main function."""

    parser = argparse.ArgumentParser(description="Content-Aware File Deduplication")
    parser.add_argument("csv_file", help="Path to CSV file inventory")

    args = parser.parse_args()

    deduplicator = ContentAwareDeduplicator(args.csv_file)
    deduplicator.run_analysis()


if __name__ == "__main__":
    main()
