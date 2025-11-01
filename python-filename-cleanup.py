"""
Python Filename Cleanup System

This module provides functionality for python filename cleanup system.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Python Filename Cleanup System
Intelligent filename cleanup and standardization system
Removes timestamps, duplicates, and standardizes naming patterns
"""

import os
import re
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter


class FilenameCleanupSystem:
    """Comprehensive filename cleanup and standardization system."""

    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path(str(Path.home()) + "/Documents/python")).expanduser()
        self.cleanup_operations = []
        self.backup_data = []

        # Common patterns to clean up
        self.cleanup_patterns = {
            "timestamp_patterns": [
                r"_\d{8}_\d{6}",  # _20251027_145831
                r"_\d{8}",  # _20251027
                r"_\d{6}",  # _145831
                r"_\d{4}-\d{2}-\d{2}",  # _2025-10-27
                r"_\d{4}\d{2}\d{2}",  # _20251027
            ],
            "duplicate_patterns": [
                r"_\d+$",  # _1, _2, _3
                r"\(\d+\)$",  # (1), (2), (3)
                r"_\d+_\d+$",  # _1_2, _2_3
                r"_\d+_\d+_\d+$",  # _1_2_3
            ],
            "version_patterns": [
                r"_v\d+$",  # _v1, _v2
                r"_version\d+$",  # _version1
                r"_\d+\.\d+$",  # _1.0, _2.1
            ],
            "temp_patterns": [
                r"_temp$",  # _temp
                r"_tmp$",  # _tmp
                r"_backup$",  # _backup
                r"_old$",  # _old
                r"_copy$",  # _copy
            ],
            "from_patterns": [
                r"_from_\w+$",  # _from_csv-processor
                r"_from_\w+_\d+$",  # _from_csv-processor_1
            ],
        }

    def analyze_filename_patterns(self):
        """Analyze all files and identify cleanup opportunities."""
        logger.info("🔍 ANALYZING FILENAME PATTERNS")
        logger.info("=" * 80)

        all_files = []
        pattern_matches = defaultdict(list)

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                filename = file_path.name
                relative_path = str(file_path.relative_to(self.root_path))

                file_info = {
                    "original_path": str(file_path),
                    "original_name": filename,
                    "relative_path": relative_path,
                    "size": file_path.stat().st_size,
                    "extension": file_path.suffix,
                    "matches": [],
                }

                # Check for pattern matches
                for pattern_type, patterns in self.cleanup_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, filename):
                            file_info["matches"].append(
                                {
                                    "type": pattern_type,
                                    "pattern": pattern,
                                    "match": re.search(pattern, filename).group(),
                                }
                            )
                            pattern_matches[pattern_type].append(file_info)

                all_files.append(file_info)

        logger.info(f"   Analyzed {len(all_files)} files")
        logger.info(f"   Found pattern matches:")
        for pattern_type, matches in pattern_matches.items():
            logger.info(f"     {pattern_type}: {len(matches)} files")

        return all_files, pattern_matches

    def generate_cleanup_plan(self, all_files, pattern_matches):
        """Generate intelligent cleanup plan."""
        logger.info("\n🧠 GENERATING CLEANUP PLAN")
        logger.info("=" * 80)

        cleanup_plan = {
            "timestamp_cleanup": [],
            "duplicate_cleanup": [],
            "version_cleanup": [],
            "temp_cleanup": [],
            "from_cleanup": [],
            "standardization": [],
        }

        # Process each file
        for file_info in all_files:
            if not file_info["matches"]:
                continue

            original_name = file_info["original_name"]
            suggested_name = original_name

            # Apply cleanup patterns
            for match in file_info["matches"]:
                pattern_type = match["type"]
                pattern = match["pattern"]
                match_text = match["match"]

                if pattern_type == "timestamp_patterns":
                    suggested_name = re.sub(pattern, "", suggested_name)
                    cleanup_plan["timestamp_cleanup"].append(
                        {
                            "original": original_name,
                            "suggested": suggested_name,
                            "pattern": pattern,
                            "removed": match_text,
                        }
                    )

                elif pattern_type == "duplicate_patterns":
                    suggested_name = re.sub(pattern, "", suggested_name)
                    cleanup_plan["duplicate_cleanup"].append(
                        {
                            "original": original_name,
                            "suggested": suggested_name,
                            "pattern": pattern,
                            "removed": match_text,
                        }
                    )

                elif pattern_type == "version_patterns":
                    suggested_name = re.sub(pattern, "", suggested_name)
                    cleanup_plan["version_cleanup"].append(
                        {
                            "original": original_name,
                            "suggested": suggested_name,
                            "pattern": pattern,
                            "removed": match_text,
                        }
                    )

                elif pattern_type == "temp_patterns":
                    suggested_name = re.sub(pattern, "", suggested_name)
                    cleanup_plan["temp_cleanup"].append(
                        {
                            "original": original_name,
                            "suggested": suggested_name,
                            "pattern": pattern,
                            "removed": match_text,
                        }
                    )

                elif pattern_type == "from_patterns":
                    suggested_name = re.sub(pattern, "", suggested_name)
                    cleanup_plan["from_cleanup"].append(
                        {
                            "original": original_name,
                            "suggested": suggested_name,
                            "pattern": pattern,
                            "removed": match_text,
                        }
                    )

            # Standardize the name
            suggested_name = self._standardize_filename(suggested_name)

            if suggested_name != original_name:
                cleanup_plan["standardization"].append(
                    {
                        "original": original_name,
                        "suggested": suggested_name,
                        "file_info": file_info,
                    }
                )

        # Resolve naming conflicts
        self._resolve_naming_conflicts(cleanup_plan)

        return cleanup_plan

    def _standardize_filename(self, filename):
        """Standardize filename format."""
        # Remove multiple underscores
        filename = re.sub(r"_{2,}", "_", filename)

        # Remove leading/trailing underscores
        filename = filename.strip("_")

        # Convert to lowercase (except extensions)
        name, ext = os.path.splitext(filename)
        filename = name.lower() + ext

        # Replace spaces with underscores
        filename = filename.replace(" ", "_")

        # Remove special characters except dots, underscores, and hyphens
        filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)

        return filename

    def _resolve_naming_conflicts(self, cleanup_plan):
        """Resolve naming conflicts by adding numbers."""
        # Group by suggested name
        name_groups = defaultdict(list)

        for category, operations in cleanup_plan.items():
            if category == "standardization":
                for op in operations:
                    suggested_name = op["suggested"]
                    name_groups[suggested_name].append(op)

        # Resolve conflicts
        for suggested_name, operations in name_groups.items():
            if len(operations) > 1:
                # Sort by file size (larger files get priority)
                operations.sort(key=lambda x: x["file_info"]["size"], reverse=True)

                for i, op in enumerate(operations):
                    if i == 0:
                        # Keep the first (largest) file with original name
                        continue
                    else:
                        # Add number suffix
                        name, ext = os.path.splitext(op["suggested"])
                        op["suggested"] = f"{name}_{i}{ext}"

    def create_cleanup_script(self, cleanup_plan):
        """Create executable cleanup script."""
        logger.info("\n🚀 CREATING CLEANUP SCRIPT")
        logger.info("=" * 80)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_file = fstr(Path.home()) + "/python_filename_cleanup_execute_{timestamp}.py"

        script_content = f'''#!/usr/bin/env python3
"""
Python Filename Cleanup Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_cleanup():
    """Execute the filename cleanup plan."""
    logger.info("🔄 EXECUTING FILENAME CLEANUP")
    logger.info("=" * 60)
    
    # Create backup directory
    backup_dir = Path(Path(str(Path.home()) + "/python_filename_cleanup_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Cleanup operations
    cleanup_operations = {cleanup_plan}
    
    logger.info(f"\\n📦 Executing cleanup operations...")
    
    total_operations = sum(len(ops) for ops in cleanup_operations.values())
    current_operation = 0
    
    for category, operations in cleanup_operations.items():
        if not operations:
            continue
            
        logger.info(f"\\n🔧 Processing {{category}} ({{len(operations)}} operations)...")
        
        for i, op in enumerate(operations, 1):
            current_operation += 1
            
            if 'file_info' in op:
                # Standardization operation
                old_path = Path(op['file_info']['original_path'])
                new_name = op['suggested']
                new_path = old_path.parent / new_name
                
                logger.info(f"   {{current_operation}}/{{total_operations}}: {{op['original']}} → {{new_name}}")
                
                try:
                    # Create backup
                    backup_path = backup_dir / op['original']
                    shutil.copy2(old_path, backup_path)
                    
                    # Rename file
                    old_path.rename(new_path)
                    
                except Exception as e:
                    logger.info(f"     ❌ Error: {{e}}")
                else:
                    logger.info(f"     ✅ Success")
            else:
                # Pattern-based operation
                logger.info(f"   {{current_operation}}/{{total_operations}}: {{op['original']}} → {{op['suggested']}}")
                logger.info(f"     Pattern: {{op['pattern']}}")
                logger.info(f"     Removed: {{op['removed']}}")
    
    logger.info(f"\\n✅ Cleanup complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🔄 To rollback, use the CSV file to restore original names")

if __name__ == "__main__":
    execute_cleanup()
'''

        with open(script_file, "w") as f:
            f.write(script_content)

        # Make executable
        os.chmod(script_file, 0o755)

        logger.info(f"   Cleanup script created: {script_file}")
        return script_file

    def create_csv_backup(self, cleanup_plan):
        """Create CSV backup with old and new names."""
        logger.info("\n💾 CREATING CSV BACKUP")
        logger.info("=" * 80)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = fstr(Path.home()) + "/python_filename_cleanup_backup_{timestamp}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "original_path",
                "original_name",
                "suggested_name",
                "category",
                "pattern",
                "removed",
                "reason",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for category, operations in cleanup_plan.items():
                for op in operations:
                    if "file_info" in op:
                        # Standardization operation
                        writer.writerow(
                            {
                                "original_path": op["file_info"]["original_path"],
                                "original_name": op["original"],
                                "suggested_name": op["suggested"],
                                "category": category,
                                "pattern": "standardization",
                                "removed": "",
                                "reason": "Filename standardization",
                            }
                        )
                    else:
                        # Pattern-based operation
                        writer.writerow(
                            {
                                "original_path": "",
                                "original_name": op["original"],
                                "suggested_name": op["suggested"],
                                "category": category,
                                "pattern": op["pattern"],
                                "removed": op["removed"],
                                "reason": f'Remove {op["removed"]} pattern',
                            }
                        )

        logger.info(f"   CSV backup created: {csv_file}")
        return csv_file

    def generate_cleanup_report(self, cleanup_plan):
        """Generate comprehensive cleanup report."""
        logger.info("\n📊 GENERATING CLEANUP REPORT")
        logger.info("=" * 80)

        total_operations = sum(len(ops) for ops in cleanup_plan.values())

        logger.info(f"📈 CLEANUP STATISTICS")
        logger.info(f"   Total operations: {total_operations}")

        for category, operations in cleanup_plan.items():
            if operations:
                logger.info(
                    f"   {category.replace('_', ' ').title()}: {len(operations)} operations"
                )

        logger.info(f"\n📝 CLEANUP EXAMPLES")

        # Show examples from each category
        for category, operations in cleanup_plan.items():
            if operations:
                logger.info(f"\n🔧 {category.replace('_', ' ').title()}:")
                for op in operations[:5]:  # Show first 5 examples
                    logger.info(f"   {op['original']} → {op['suggested']}")
                    if "removed" in op and op["removed"]:
                        logger.info(f"     Removed: {op['removed']}")
                if len(operations) > 5:
                    logger.info(f"   ... and {len(operations) - 5} more")


def main():
    """Main execution function."""
    logger.info("🧹 PYTHON FILENAME CLEANUP SYSTEM")
    logger.info("=" * 80)
    logger.info("Intelligent filename cleanup and standardization system")
    logger.info("Removes timestamps, duplicates, and standardizes naming patterns")
    print()

    cleanup_system = FilenameCleanupSystem()

    # Analyze filename patterns
    all_files, pattern_matches = cleanup_system.analyze_filename_patterns()

    # Generate cleanup plan
    cleanup_plan = cleanup_system.generate_cleanup_plan(all_files, pattern_matches)

    # Create cleanup script
    script_file = cleanup_system.create_cleanup_script(cleanup_plan)

    # Create CSV backup
    csv_file = cleanup_system.create_csv_backup(cleanup_plan)

    # Generate report
    cleanup_system.generate_cleanup_report(cleanup_plan)

    logger.info(f"\n✅ FILENAME CLEANUP SYSTEM READY!")
    logger.info("=" * 80)
    logger.info(f"📁 CSV backup: {csv_file}")
    logger.info(f"🚀 Execution script: {script_file}")
    logger.info(f"🛡️  All changes can be rolled back using the CSV file!")

    logger.info(f"\n🎯 NEXT STEPS:")
    logger.info(f"   1. Review the cleanup examples above")
    logger.info(f"   2. Check the CSV backup file")
    logger.info(f"   3. Run the execution script when ready: python3 {script_file}")
    logger.info(f"   4. Use CSV file to rollback if needed")

    logger.info(f"\n📋 Filename cleanup system ready to execute!")


if __name__ == "__main__":
    main()
