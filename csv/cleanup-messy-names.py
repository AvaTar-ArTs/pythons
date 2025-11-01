"""
Cleanup Messy Names

This module provides functionality for cleanup messy names.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
🔧 Fix Timestamped Files - Clean Up Messy Filenames
Automatically renames files with timestamps to clean, meaningful names
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TimestampedFileFixer:
    """Fix files with timestamp patterns in their names"""

    def __init__(self, project_root: Path):
        """__init__ function."""

        self.project_root = Path(project_root)
        self.files_renamed = 0
        self.rename_log = []

        # Patterns to identify timestamped files
        self.timestamp_patterns = [
            r"_\d{8}_\d{6}",  # _20251026_054918
            r"_\d{8}_\d{4}",  # _20251026_0549
            r"_\d{8}",  # _20251026
            r"_\d{6}_\d{6}",  # _101026_054918
            r"_\d{4}_\d{6}",  # _1026_054918
            r"_\d{10}",  # _1735123456 (unix timestamp)
            r"_\d{13}",  # _1735123456789 (millisecond timestamp)
        ]

        # File type mappings for better naming
        self.file_type_mappings = {
            "analysis": ["analysis", "analyze", "analyzer"],
            "documentation": ["doc", "documentation", "docs"],
            "api": ["api", "endpoint", "reference"],
            "report": ["report", "summary", "results"],
            "log": ["log", "logs", "logging"],
            "data": ["data", "json", "csv", "export"],
            "backup": ["backup", "bak", "old"],
            "config": ["config", "configuration", "settings"],
            "test": ["test", "testing", "spec"],
            "temp": ["temp", "temporary", "tmp"],
        }

    def is_timestamped_file(self, filename: str) -> bool:
        """Check if filename contains timestamp patterns"""
        for pattern in self.timestamp_patterns:
            if re.search(pattern, filename):
                return True
        return False

    def extract_file_type(self, filename: str) -> str:
        """Extract file type from filename"""
        filename_lower = filename.lower()

        for file_type, keywords in self.file_type_mappings.items():
            if any(keyword in filename_lower for keyword in keywords):
                return file_type

        # Check file extension
        if filename.endswith(".json"):
            return "data"
        elif filename.endswith(".md"):
            return "documentation"
        elif filename.endswith(".html"):
            return "documentation"
        elif filename.endswith(".log"):
            return "log"
        elif filename.endswith(".txt"):
            return "documentation"

        return "general"

    def clean_filename(self, filename: str) -> str:
        """Clean filename by removing timestamps and improving readability"""
        # Remove timestamp patterns
        cleaned = filename
        for pattern in self.timestamp_patterns:
            cleaned = re.sub(pattern, "", cleaned)

        # Remove multiple underscores
        cleaned = re.sub(r"_+", "_", cleaned)

        # Remove leading/trailing underscores
        cleaned = cleaned.strip("_")

        # Handle common patterns
        cleaned = cleaned.replace("__", "_")

        # If filename is too short or empty, use a default
        if len(cleaned) < 3 or cleaned in ["", ".json", ".md", ".html", ".log", ".txt"]:
            file_type = self.extract_file_type(filename)
            extension = Path(filename).suffix
            cleaned = f"{file_type}_file{extension}"

        return cleaned

    def suggest_better_name(self, filepath: Path) -> Tuple[str, str]:
        """Suggest a better name for a file"""
        current_name = filepath.name
        file_type = self.extract_file_type(current_name)

        # Get the directory context for better naming
        parent_dir = filepath.parent.name.lower()
        current_lower = current_name.lower()

        # Extract meaningful parts from filename
        meaningful_parts = []

        # Look for key terms in the filename
        key_terms = [
            "api",
            "analysis",
            "report",
            "log",
            "data",
            "config",
            "documentation",
            "miniforge",
            "environment",
            "comprehensive",
            "file",
            "organization",
            "recovery",
            "filename",
            "pydoc",
            "html",
            "json",
            "md",
        ]

        for term in key_terms:
            if term in current_lower:
                meaningful_parts.append(term)

        # Create context-aware names
        if "api" in current_lower or "api" in parent_dir:
            if "documentation" in current_lower:
                base_name = "api_documentation"
            else:
                base_name = "api_data"
        elif "analysis" in current_lower or "analyze" in current_lower:
            base_name = "analysis_results"
        elif "report" in current_lower:
            if "comprehensive" in current_lower:
                base_name = "comprehensive_report"
            elif "miniforge" in current_lower:
                base_name = "miniforge_environment_report"
            else:
                base_name = "generated_report"
        elif "log" in current_lower:
            if "recovery" in current_lower:
                base_name = "filename_recovery_log"
            else:
                base_name = "system_log"
        elif "data" in current_lower or "json" in current_lower:
            base_name = "processed_data"
        elif "config" in current_lower or "configuration" in current_lower:
            base_name = "configuration"
        elif "documentation" in current_lower or "pydoc" in current_lower:
            if "config" in current_lower:
                base_name = "pydoc_config"
            elif "diag" in current_lower:
                base_name = "pydoc_diagnostics"
            else:
                base_name = "documentation"
        elif "miniforge" in current_lower:
            base_name = "miniforge_environment_report"
        elif "comprehensive" in current_lower:
            base_name = "comprehensive_report"
        elif "filename" in current_lower and "recovery" in current_lower:
            base_name = "filename_recovery_log"
        else:
            # Use cleaned filename but make it more meaningful
            cleaned = self.clean_filename(current_name)
            if len(cleaned) < 5:
                base_name = f"{file_type}_file"
            else:
                base_name = cleaned

        # Add appropriate extension
        extension = filepath.suffix
        suggested_name = f"{base_name}{extension}"

        # Ensure uniqueness
        counter = 1
        original_suggested = suggested_name
        while (filepath.parent / suggested_name).exists() and suggested_name != current_name:
            name_part = original_suggested.rsplit(".", 1)[0]
            ext_part = original_suggested.rsplit(".", 1)[1] if "." in original_suggested else ""
            suggested_name = f"{name_part}_{counter}.{ext_part}" if ext_part else f"{name_part}_{counter}"
            counter += 1

        return suggested_name, file_type

    def find_timestamped_files(self, max_depth: int = 6) -> List[Path]:
        """Find all files with timestamp patterns within specified depth"""
        timestamped_files = []

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and self.is_timestamped_file(file_path.name):
                # Calculate depth relative to project root
                depth = len(file_path.relative_to(self.project_root).parts)
                if depth <= max_depth:
                    timestamped_files.append(file_path)
                else:
                    logger.debug(f"Skipping deep file: {file_path} (depth: {depth})")

        return timestamped_files

    def preview_renames(self, files: List[Path]) -> List[Dict]:
        """Preview what files will be renamed"""
        preview = []

        for file_path in files:
            suggested_name, file_type = self.suggest_better_name(file_path)

            preview.append(
                {
                    "current_path": str(file_path),
                    "current_name": file_path.name,
                    "suggested_name": suggested_name,
                    "file_type": file_type,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        return preview

    def apply_renames(self, files: List[Path], dry_run: bool = True) -> int:
        """Apply the renames"""
        renamed_count = 0

        for file_path in files:
            suggested_name, file_type = self.suggest_better_name(file_path)

            if suggested_name == file_path.name:
                continue

            new_path = file_path.parent / suggested_name

            if dry_run:
                logger.info(f"Would rename: {file_path.name} → {suggested_name}")
            else:
                try:
                    file_path.rename(new_path)
                    logger.info(f"✅ Renamed: {file_path.name} → {suggested_name}")

                    self.rename_log.append(
                        {
                            "original": str(file_path),
                            "new": str(new_path),
                            "timestamp": datetime.now().isoformat(),
                            "file_type": file_type,
                        }
                    )

                    renamed_count += 1
                    self.files_renamed += 1

                except Exception as e:
                    logger.error(f"❌ Error renaming {file_path.name}: {e}")

        return renamed_count

    def generate_report(self, preview_data: List[Dict], output_path: Path):
        """Generate a report of the renaming operation"""
        report_content = []

        report_content.append("# 🔧 Timestamped Files Cleanup Report")
        report_content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report_content.append("")

        # Statistics
        total_files = len(preview_data)
        file_types = {}
        total_size = 0

        for item in preview_data:
            file_type = item["file_type"]
            file_types[file_type] = file_types.get(file_type, 0) + 1
            total_size += item["size"]

        report_content.append("## 📊 Statistics")
        report_content.append(f"- **Total Files**: {total_files}")
        report_content.append(
            f"- **Total Size**: {total_size:,} bytes ({total_size / CONSTANT_1024 / CONSTANT_1024:.2f} MB)"
        )
        report_content.append("")

        report_content.append("## 📁 File Types")
        for file_type, count in sorted(file_types.items()):
            report_content.append(f"- **{file_type.title()}**: {count} files")
        report_content.append("")

        # File list
        report_content.append("## 📝 Files to Rename")
        report_content.append("")

        for i, item in enumerate(preview_data, 1):
            report_content.append(f"### {i}. {item['current_name']}")
            report_content.append(f"- **New Name**: `{item['suggested_name']}`")
            report_content.append(f"- **Type**: {item['file_type']}")
            report_content.append(f"- **Size**: {item['size']:,} bytes")
            report_content.append(f"- **Modified**: {item['modified']}")
            report_content.append(f"- **Path**: `{item['current_path']}`")
            report_content.append("")

        # Save report
        report_path = output_path / "timestamped_files_cleanup_report.md"
        report_path.write_text(Path("\n").join(report_content))
        logger.info(f"📄 Report saved: {report_path}")

    def run(self, dry_run: bool = True, max_depth: int = 6):
        """Main execution method"""
        logger.info(f"🔍 Scanning for timestamped files (max depth: {max_depth})...")

        # Find timestamped files
        timestamped_files = self.find_timestamped_files(max_depth)

        if not timestamped_files:
            logger.info("✅ No timestamped files found!")
            return

        logger.info(f"📁 Found {len(timestamped_files)} timestamped files")

        # Preview renames
        preview_data = self.preview_renames(timestamped_files)

        # Generate report
        self.generate_report(preview_data, self.project_root)

        # Show preview
        logger.info("\n📝 Preview of renames:")
        for item in preview_data[:10]:  # Show first 10
            logger.info(f"  {item['current_name']} → {item['suggested_name']}")

        if len(preview_data) > 10:
            logger.info(f"  ... and {len(preview_data) - 10} more files")

        # Apply renames
        if not dry_run:
            logger.info("\n🚀 Applying renames...")
            renamed_count = self.apply_renames(timestamped_files, dry_run=False)
            logger.info(f"✅ Successfully renamed {renamed_count} files")
        else:
            logger.info("\n💡 Run with --apply to execute renames")

        return preview_data


def main():
    """Command line interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Fix timestamped filenames")
    parser.add_argument("path", type=Path, nargs="?", default=Path.cwd(), help="Directory to scan")
    parser.add_argument("--apply", action="store_true", help="Actually rename files (default: dry run)")
    parser.add_argument("--depth", type=int, default=6, help="Maximum folder depth to scan (default: 6)")

    args = parser.parse_args()

    fixer = TimestampedFileFixer(args.path)
    fixer.run(dry_run=not args.apply, max_depth=args.depth)


if __name__ == "__main__":
    main()
