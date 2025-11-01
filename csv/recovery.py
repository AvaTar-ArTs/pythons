"""
Recovery

This module provides functionality for recovery.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Recovery Analyzer - Comprehensive analysis of Python backup locations
"""

import os
import csv
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class RecoveryAnalyzer:
    def __init__(self):
        """__init__ function."""

        self.backup_locations = [
            Path("/Volumes/2T-Xx/steven/Documents/Python-Backup"),
            Path("/Volumes/2T-Xx/steven/Documents/Python_backup_20240725_023301"),
            Path("/Volumes/2T-Xx/steven/Documents/python"),
            Path("/Volumes/2T-Xx/python"),
            Path("/Volumes/2T-Xx/AvaTarArTs/python"),
        ]

        self.target_dir = Path(Path("/Users/steven/Documents/python"))
        self.analysis_results = {
            "total_files": 0,
            "unique_files": 0,
            "duplicates": 0,
            "locations": {},
            "file_hashes": defaultdict(list),
            "missing_files": [],
            "recovery_plan": [],
        }

    def calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of file."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.info(f"Error hashing {file_path}: {e}")
            return None

    def scan_location(self, location):
        """Scan a backup location for Python files."""
        logger.info(f"🔍 Scanning: {location}")

        if not os.path.exists(location):
            logger.info(f"   ❌ Location not found: {location}")
            return

        location_files = []
        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        file_info = {
                            "path": file_path,
                            "name": file,
                            "size": os.path.getsize(file_path),
                            "hash": file_hash,
                            "location": location,
                        }
                        location_files.append(file_info)
                        self.analysis_results["file_hashes"][file_hash].append(file_info)

        self.analysis_results["locations"][location] = {"files": location_files, "count": len(location_files)}
        self.analysis_results["total_files"] += len(location_files)

        logger.info(f"   ✅ Found {len(location_files)} Python files")

    def analyze_duplicates(self):
        """Analyze duplicate files across locations."""
        logger.info("\n🔍 ANALYZING DUPLICATES")
        logger.info("=" * 40)

        duplicates = 0
        for file_hash, files in self.analysis_results["file_hashes"].items():
            if len(files) > 1:
                duplicates += len(files) - 1
                logger.info(f"   📄 {files[0]['name']} - {len(files)} copies")

        self.analysis_results["duplicates"] = duplicates
        self.analysis_results["unique_files"] = len(self.analysis_results["file_hashes"])

        logger.info(f"\n📊 DUPLICATE ANALYSIS:")
        logger.info(f"   Total files found: {self.analysis_results['total_files']}")
        logger.info(f"   Unique files: {self.analysis_results['unique_files']}")
        logger.info(f"   Duplicates: {duplicates}")

    def check_missing_files(self):
        """Check which files are missing from current python directory."""
        logger.info("\n🔍 CHECKING MISSING FILES")
        logger.info("=" * 40)

        current_files = set()
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".py"):
                    current_files.add(file)

        missing_count = 0
        for file_hash, files in self.analysis_results["file_hashes"].items():
            file_name = files[0]["name"]
            if file_name not in current_files:
                self.analysis_results["missing_files"].append(files[0])
                missing_count += 1

        logger.info(f"   📄 Files missing from current directory: {missing_count}")
        return missing_count

    def create_recovery_plan(self):
        """Create a recovery plan for missing files."""
        logger.info("\n📋 CREATING RECOVERY PLAN")
        logger.info("=" * 40)

        for file_info in self.analysis_results["missing_files"]:
            # Find the best copy (prefer largest file)
            best_copy = max(self.analysis_results["file_hashes"][file_info["hash"]], key=lambda x: x["size"])

            recovery_action = {
                "source": best_copy["path"],
                "destination": str(self.target_dir / best_copy["name"]),
                "size": best_copy["size"],
                "location": best_copy["location"],
            }
            self.analysis_results["recovery_plan"].append(recovery_action)

        logger.info(f"   📄 Files to recover: {len(self.analysis_results['recovery_plan'])}")

    def save_analysis_report(self):
        """Save detailed analysis report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"/Users/steven/Documents/python/recovery_analysis_{timestamp}.csv"

        with open(report_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["file_name", "file_size", "file_hash", "source_location", "is_duplicate", "needs_recovery"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file_hash, files in self.analysis_results["file_hashes"].items():
                is_duplicate = len(files) > 1
                needs_recovery = files[0] in self.analysis_results["missing_files"]

                for file_info in files:
                    writer.writerow(
                        {
                            "file_name": file_info["name"],
                            "file_size": file_info["size"],
                            "file_hash": file_hash,
                            "source_location": file_info["location"],
                            "is_duplicate": is_duplicate,
                            "needs_recovery": needs_recovery,
                        }
                    )

        logger.info(f"   📊 Analysis report saved: {report_file}")
        return report_file

    def run_analysis(self):
        """Run complete analysis."""
        logger.info("🔍 PYTHON RECOVERY ANALYSIS")
        logger.info("=" * 50)
        logger.info("Analyzing backup locations for Python file recovery")
        print()

        # Scan all locations
        for location in self.backup_locations:
            self.scan_location(location)

        # Analyze results
        self.analyze_duplicates()
        missing_count = self.check_missing_files()
        self.create_recovery_plan()

        # Save report
        report_file = self.save_analysis_report()

        logger.info(f"\n🎯 ANALYSIS COMPLETE!")
        logger.info(f"   📊 Total files found: {self.analysis_results['total_files']}")
        logger.info(f"   📄 Unique files: {self.analysis_results['unique_files']}")
        logger.info(f"   🔄 Duplicates: {self.analysis_results['duplicates']}")
        logger.info(f"   ❌ Missing files: {missing_count}")
        logger.info(f"   📋 Recovery plan: {len(self.analysis_results['recovery_plan'])} files")
        logger.info(f"   📊 Report saved: {report_file}")

        return self.analysis_results


def main():
    """main function."""

    analyzer = RecoveryAnalyzer()
    results = analyzer.run_analysis()

    logger.info(f"\n💡 NEXT STEPS:")
    logger.info(f"   1. Review the analysis report")
    logger.info(f"   2. Run recovery to restore missing files")
    logger.info(f"   3. Remove duplicates if needed")


if __name__ == "__main__":
    main()
