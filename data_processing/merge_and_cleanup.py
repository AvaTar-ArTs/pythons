#!/usr/bin/env python3
"""
Python Backup Merge and Cleanup Tool
Merges multiple Python backup directories, removes duplicates, and organizes the final structure
"""

import argparse
import json
import os
import shutil
from datetime import datetime


class PythonBackupMerger:
    def __init__(self, analysis_file, duplicates_file, merge_plan_file):
        self.analysis_file = analysis_file
        self.duplicates_file = duplicates_file
        self.merge_plan_file = merge_plan_file
        self.analysis_data = None
        self.duplicates_data = None
        self.merge_plan = None
        self.merge_stats = {
            "files_copied": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": 0,
            "space_saved": 0,
        }

    def load_data(self):
        """Load analysis data from JSON files"""
        print("Loading analysis data...")

        with open(self.analysis_file, "r") as f:
            self.analysis_data = json.load(f)

        with open(self.duplicates_file, "r") as f:
            self.duplicates_data = json.load(f)

        with open(self.merge_plan_file, "r") as f:
            self.merge_plan = json.load(f)

        print(f"Loaded data for {self.analysis_data['unique_files']} unique files")
        print(f"Found {self.analysis_data['duplicate_groups']} duplicate groups")

    def create_output_directory(self, output_dir):
        """Create the output directory structure"""
        print(f"Creating output directory: {output_dir}")

        if os.path.exists(output_dir):
            print(f"Output directory already exists: {output_dir}")
            print("Removing existing directory and starting fresh...")
            shutil.rmtree(output_dir)

        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: {output_dir}")

    def copy_file_safely(self, source, destination):
        """Copy a file safely with error handling"""
        try:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Copy the file
            shutil.copy2(source, destination)
            self.merge_stats["files_copied"] += 1
            return True
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")
            self.merge_stats["errors"] += 1
            return False

    def merge_files(self, output_dir, dry_run=False):
        """Merge files according to the merge plan"""
        print(f"\n{'DRY RUN: ' if dry_run else ''}Merging files...")

        if dry_run:
            print("DRY RUN MODE - No files will actually be copied")

        # Create directories first
        for dir_path in self.merge_plan["directories_to_create"]:
            full_dir_path = os.path.join(output_dir, dir_path)
            if not dry_run:
                os.makedirs(full_dir_path, exist_ok=True)
            self.merge_stats["directories_created"] += 1
            print(f"Created directory: {full_dir_path}")

        # Copy files
        for file_info in self.merge_plan["files_to_copy"]:
            source = file_info["source"]
            destination = file_info["destination"]

            if not os.path.exists(source):
                print(f"Source file not found: {source}")
                self.merge_stats["files_skipped"] += 1
                continue

            if not dry_run:
                if self.copy_file_safely(source, destination):
                    print(f"Copied: {os.path.basename(source)}")
                else:
                    self.merge_stats["files_skipped"] += 1
            else:
                print(f"Would copy: {source} -> {destination}")
                self.merge_stats["files_copied"] += 1

    def create_duplicate_removal_script(self, output_dir):
        """Create a script to remove duplicate files from source directories"""
        script_content = f"""#!/bin/bash
# Duplicate Removal Script
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

echo "=== Python Backup Duplicate Removal Script ==="
echo "This script will remove duplicate files from the source directories"
echo "keeping only the most recent versions."
echo ""

# Backup directories to clean
BACKUP_DIRS=(
    "/Users/steven/Documents/python_backup_20251013_005711"
    "/Users/steven/Documents/python_backup_20251013_005814"
)

# Files to remove (based on analysis)
DUPLICATE_FILES=(
"""

        # Add duplicate files to the script
        for dup_group in self.duplicates_data["duplicate_groups"]:
            for duplicate in dup_group["duplicates"]:
                if not duplicate.get("is_zip_content", False):
                    script_content += f'    "{duplicate["path"]}"\n'

        script_content += """)
)

echo "Found ${#DUPLICATE_FILES[@]} duplicate files to remove"
echo ""

# Ask for confirmation
read -p "Do you want to proceed with removing duplicates? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 1
fi

echo "Removing duplicate files..."
removed_count=0
for file in "${DUPLICATE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Removing: $file"
        rm "$file"
        ((removed_count++))
    else
        echo "File not found: $file"
    fi
done

echo ""
echo "Removed $removed_count duplicate files"
echo "Operation completed."
"""

        script_path = os.path.join(output_dir, "remove_duplicates.sh")
        with open(script_path, "w") as f:
            f.write(script_content)

        # Make the script executable
        os.chmod(script_path, 0o755)
        print(f"Created duplicate removal script: {script_path}")

    def create_organization_script(self, output_dir):
        """Create a script to organize the merged directory"""
        script_content = f"\'"#!/bin/bash
# Python Backup Organization Script
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

echo "=== Python Backup Organization Script ==="
echo "Organizing merged Python backup directory..."
echo ""

MERGED_DIR="{output_dir}"

# Create organized structure
mkdir -p "$MERGED_DIR/00_core"
mkdir -p "$MERGED_DIR/01_ai_tools"
mkdir -p "$MERGED_DIR/02_media_processing"
mkdir -p "$MERGED_DIR/03_automation"
mkdir -p "$MERGED_DIR/04_web_tools"
mkdir -p "$MERGED_DIR/05_utilities"
mkdir -p "$MERGED_DIR/06_experimental"
mkdir -p "$MERGED_DIR/07_archived"
mkdir -p "$MERGED_DIR/08_documentation"
mkdir -p "$MERGED_DIR/09_backups"

echo "Created organized directory structure"

# Move files to appropriate categories (example organization)
echo "Organizing files by category..."

# Core Python files
find "$MERGED_DIR" -name "*.py" -path "*/00_*" -exec mv {{}} "$MERGED_DIR/00_core/" \\; 2>/dev/null

# AI-related tools
find "$MERGED_DIR" -name "*.py" -path "*/01_*" -exec mv {{}} "$MERGED_DIR/01_ai_tools/" \\; 2>/dev/null

# Media processing
find "$MERGED_DIR" -name "*.py" -path "*/02_*" -exec mv {{}} "$MERGED_DIR/02_media_processing/" \\; 2>/dev/null

# Automation tools
find "$MERGED_DIR" -name "*.py" -path "*/03_*" -exec mv {{}} "$MERGED_DIR/03_automation/" \\; 2>/dev/null

# Web tools
find "$MERGED_DIR" -name "*.py" -path "*/04_*" -exec mv {{}} "$MERGED_DIR/04_web_tools/" \\; 2>/dev/null

# Utilities
find "$MERGED_DIR" -name "*.py" -path "*/05_*" -exec mv {{}} "$MERGED_DIR/05_utilities/" \\; 2>/dev/null

# Experimental
find "$MERGED_DIR" -name "*.py" -path "*/06_*" -exec mv {{}} "$MERGED_DIR/06_experimental/" \\; 2>/dev/null

# Archived
find "$MERGED_DIR" -name "*.py" -path "*/07_*" -exec mv {{}} "$MERGED_DIR/07_archived/" \\; 2>/dev/null

# Documentation
find "$MERGED_DIR" -name "*.md" -o -name "*.txt" -o -name "*.html" | head -100 | xargs -I {{}} mv {{}} "$MERGED_DIR/08_documentation/" 2>/dev/null

echo "Organization completed!"
echo "Merged directory: $MERGED_DIR"
"\'"

        script_path = os.path.join(output_dir, "organize_merged.sh")
        with open(script_path, "w") as f:
            f.write(script_content)

        os.chmod(script_path, 0o755)
        print(f"Created organization script: {script_path}")

    def generate_summary_report(self, output_dir):
        """Generate a comprehensive summary report"""
        report_content = f"""# Python Backup Merge and Cleanup Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Analysis Results

- **Total files analyzed:** {self.analysis_data["total_files_analyzed"]:,}
- **Unique files:** {self.analysis_data["unique_files"]:,}
- **Duplicate groups:** {self.analysis_data["duplicate_groups"]:,}
- **Total duplicates:** {self.analysis_data["total_duplicates"]:,}
- **Space that can be saved:** {self.analysis_data["space_saved_gb"]:.2f} GB

## Merge Statistics

- **Files copied:** {self.merge_stats["files_copied"]:,}
- **Files skipped:** {self.merge_stats["files_skipped"]:,}
- **Directories created:** {self.merge_stats["directories_created"]:,}
- **Errors encountered:** {self.merge_stats["errors"]:,}

## Directory Breakdown

"""

        for path, info in self.analysis_data["file_breakdown"].items():
            if info["file_count"] > 0:
                size_mb = info["total_size"] / (1024 * 1024)
                report_content += f"- **{os.path.basename(path)}:** {info['file_count']:,} files ({size_mb:.1f} MB)\n"

        report_content += f'\''

## Output Directory

The merged and deduplicated backup has been created at:
**{output_dir}**

## Next Steps

1. **Review the merged directory** to ensure all important files are present
2. **Run the organization script** (`organize_merged.sh`) to organize files by category
3. **Run the duplicate removal script** (`remove_duplicates.sh`) to clean up source directories
4. **Verify the cleanup** before removing the original backup directories

## Files Generated

- `remove_duplicates.sh` - Script to remove duplicates from source directories
- `organize_merged.sh` - Script to organize the merged directory
- `python_backup_analysis_*.json` - Detailed analysis data
- `python_backup_duplicates_*.json` - Duplicate file information
- `python_merge_plan_*.json` - Merge plan details

## Recommendations

1. **Test the merged directory** thoroughly before removing originals
2. **Keep backups** of the original directories until you're satisfied
3. **Consider compression** for long-term storage of the merged directory
4. **Regular cleanup** - Run this analysis periodically to prevent future duplication

---
*This report was generated by the Python Backup Analysis and Merge Tool*
"""

        report_path = os.path.join(output_dir, "MERGE_SUMMARY.md")
        with open(report_path, "w") as f:
            f.write(report_content)

        print(f"Generated summary report: {report_path}")

    def run_merge(self, output_dir, dry_run=False):
        """Run the complete merge process'\''
        print("=== Python Backup Merge and Cleanup Tool ===")

        # Load data
        self.load_data()

        # Create output directory
        self.create_output_directory(output_dir)

        # Merge files
        self.merge_files(output_dir, dry_run)

        # Create utility scripts
        self.create_duplicate_removal_script(output_dir)
        self.create_organization_script(output_dir)

        # Generate summary report
        self.generate_summary_report(output_dir)

        print("\n=== MERGE COMPLETE ===")
        print(f"Output directory: {output_dir}")
        print(f"Files processed: {self.merge_stats['files_copied']}")
        print(f"Errors: {self.merge_stats['errors']}")

        if not dry_run:
            print("\nNext steps:")
            print(f"1. Review the merged directory: {output_dir}")
            print(f"2. Run: cd {output_dir} && ./organize_merged.sh")
            print(f"3. Run: cd {output_dir} && ./remove_duplicates.sh")


def main():
    parser = argparse.ArgumentParser(
        description="Merge and cleanup Python backup directories"
    )
    parser.add_argument("--analysis", required=True, help="Path to analysis JSON file")
    parser.add_argument(
        "--duplicates", required=True, help="Path to duplicates JSON file"
    )
    parser.add_argument(
        "--merge-plan", required=True, help="Path to merge plan JSON file"
    )
    parser.add_argument(
        "--output", required=True, help="Output directory for merged backup"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without actually copying files",
    )

    args = parser.parse_args()

    merger = PythonBackupMerger(args.analysis, args.duplicates, args.merge_plan)
    merger.run_merge(args.output, args.dry_run)


if __name__ == "__main__":
    main()
