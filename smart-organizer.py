"""
Smart Organizer

This module provides functionality for smart organizer.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Smart File Organizer
Fixes filename mess AND organizes files by type into proper directories
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class SmartOrganizer:
    """Organizes files by type and fixes filename mess."""

    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path("/Users/steven/Documents/python")).expanduser()
        self.max_depth = 6

        # File type organization
        self.file_type_dirs = {
            ".html": Path(Path("/Users/steven/Documents/html")),
            ".md": Path(Path("/Users/steven/Documents/markdown")),
            ".csv": Path(Path("/Users/steven/Documents/csv")),
            ".pdf": Path(Path("/Users/steven/Documents/pdf")),
            ".json": Path(Path("/Users/steven/Documents/json")),
            ".txt": Path(Path("/Users/steven/Documents/text")),
            ".log": Path(Path("/Users/steven/Documents/logs")),
            ".png": Path(Path("/Users/steven/Documents/images")),
            ".jpg": Path(Path("/Users/steven/Documents/images")),
            ".jpeg": Path(Path("/Users/steven/Documents/images")),
            ".gif": Path(Path("/Users/steven/Documents/images")),
            ".svg": Path(Path("/Users/steven/Documents/images")),
            ".mp4": Path(Path("/Users/steven/Documents/videos")),
            ".mov": Path(Path("/Users/steven/Documents/videos")),
            ".avi": Path(Path("/Users/steven/Documents/videos")),
            ".zip": Path(Path("/Users/steven/Documents/archives")),
            ".tar": Path(Path("/Users/steven/Documents/archives")),
            ".gz": Path(Path("/Users/steven/Documents/archives")),
            ".exe": Path(Path("/Users/steven/Documents/executables")),
            ".dmg": Path(Path("/Users/steven/Documents/executables")),
            ".pkg": Path(Path("/Users/steven/Documents/executables")),
        }

        # Clean filename patterns
        self.cleanup_patterns = {
            "timestamps": [
                r"_\d{8}_\d{6}",  # _20251028_021746
                r"_\d{8}",  # _20251028
                r"_\d{6}",  # _021746
                r"_\d{4}-\d{2}-\d{2}",  # _2025-10-28
            ],
            "duplicates": [
                r"_\d+$",  # _1, _2, _3
                r"\(\d+\)$",  # (1), (2), (3)
                r"_\d+_\d+$",  # _1_2, _2_3
            ],
            "repetitive": [
                r"^documentation_documentation_documentation_",
                r"^documentation_documentation_",
                r"^documentation_",
                r"^web_resources_",
                r"^pydoc_html_",
                r"^html-generator_",
                r"^doc-generator_output_",
            ],
            "hash_suffixes": [
                r"_[a-f0-9]{8,}$",  # _a1a7b7066bc54
            ],
            "temp_suffixes": [
                r"_temp$",
                r"_tmp$",
                r"_backup$",
                r"_old$",
                r"_copy$",
            ],
            "from_suffixes": [
                r"_from_\w+$",  # _from_csv-processor
            ],
        }

        # Names to preserve (don't rename these)
        self.preserve_patterns = [
            r"^\d+days?\.py$",  # 15days.py
            r"^[a-z]{2,4}\.py$",  # docx.py, csvp.py
            r"^[A-Z][a-z]+[A-Z][a-z]+\.py$",  # TextToSpeech.py
            r"^[a-z]+[A-Z][a-z]+\.py$",  # botStories.py
            r"^[a-z]+_[a-z]+\.py$",  # file_utils.py
            r"^[A-Z][a-z]+\.py$",  # Calculator.py
        ]

    def analyze_files(self):
        """Analyze all files and create organization plan."""
        logger.info("🧠 SMART FILE ORGANIZER")
        logger.info("=" * 80)
        logger.info("Fixes filename mess AND organizes files by type")
        logger.info("HTML → ~/Documents/html, MD → ~/Documents/markdown, etc.")
        print()

        # Find all files
        all_files = []
        for file_path in self.root_path.rglob("*"):
            try:
                depth = len(file_path.relative_to(self.root_path).parts)
                if depth > self.max_depth:
                    continue
            except ValueError:
                continue

            if file_path.is_file():
                file_info = {
                    "path": file_path,
                    "name": file_path.name,
                    "extension": file_path.suffix.lower(),
                    "size": file_path.stat().st_size,
                    "depth": depth,
                }
                all_files.append(file_info)

        logger.info(f"   Found {len(all_files)} files to analyze")

        # Categorize files
        python_files = []
        other_files = []

        for file_info in all_files:
            if file_info["extension"] == ".py":
                python_files.append(file_info)
            else:
                other_files.append(file_info)

        logger.info(f"   Python files: {len(python_files)}")
        logger.info(f"   Other files: {len(other_files)}")

        return python_files, other_files

    def clean_filename(self, filename):
        """Clean a filename by removing problematic patterns."""
        if self._should_preserve_name(filename):
            return filename

        # Remove extension temporarily
        name, ext = os.path.splitext(filename)

        # Apply cleanup patterns
        for pattern_type, patterns in self.cleanup_patterns.items():
            for pattern in patterns:
                name = re.sub(pattern, "", name)

        # Clean up spaces and special chars
        name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
        name = re.sub(r"_{2,}", "_", name)  # Multiple underscores
        name = name.strip("_")

        # If name is too short, try to extract meaningful parts
        if len(name) < 3:
            meaningful_parts = self._extract_meaningful_parts(filename)
            if meaningful_parts:
                name = "_".join(meaningful_parts)
            else:
                name = "file"

        return name + ext

    def _should_preserve_name(self, filename):
        """Check if filename should be preserved."""
        for pattern in self.preserve_patterns:
            if re.match(pattern, filename):
                return True
        return False

    def _extract_meaningful_parts(self, filename):
        """Extract meaningful parts from filename."""
        parts = []
        words = re.split(r"[._-]", filename.lower())

        meaningless = {
            "documentation",
            "web",
            "resources",
            "package",
            "data",
            "html",
            "generator",
            "output",
            "docs",
            "pydoc",
            "blog",
            "versions",
            "config",
            "custom",
            "css",
            "temp",
            "tmp",
            "backup",
            "old",
            "copy",
            "file",
            "dir",
            "folder",
        }

        for word in words:
            if word and word not in meaningless and len(word) > 2:
                parts.append(word)

        return parts[:3]  # Limit to 3 parts

    def create_organization_plan(self, python_files, other_files):
        """Create organization plan for all files."""
        plan = {"python_renames": [], "file_moves": [], "directories_to_create": set()}

        # Handle Python files (rename but keep in place)
        for file_info in python_files:
            clean_name = self.clean_filename(file_info["name"])
            if clean_name != file_info["name"]:
                plan["python_renames"].append(
                    {
                        "old_path": file_info["path"],
                        "old_name": file_info["name"],
                        "new_name": clean_name,
                        "reason": self._get_cleanup_reason(
                            file_info["name"], clean_name
                        ),
                    }
                )

        # Handle other files (move to appropriate directories)
        for file_info in other_files:
            ext = file_info["extension"]
            if ext in self.file_type_dirs:
                target_dir = self.file_type_dirs[ext]
                plan["directories_to_create"].add(target_dir)

                clean_name = self.clean_filename(file_info["name"])
                target_path = target_dir / clean_name

                plan["file_moves"].append(
                    {
                        "old_path": file_info["path"],
                        "old_name": file_info["name"],
                        "new_path": target_path,
                        "new_name": clean_name,
                        "extension": ext,
                        "reason": f"Move {ext} file to {target_dir.name} directory",
                    }
                )

        return plan

    def _get_cleanup_reason(self, old_name, new_name):
        """Get reason for filename cleanup."""
        if old_name == new_name:
            return "No change needed"

        reasons = []

        if re.search(r"_\d{8}_\d{6}|_\d{8}", old_name):
            reasons.append("Removed timestamp")

        if re.search(r"_\d+$|\(\d+\)$", old_name):
            reasons.append("Removed duplicate numbers")

        if re.search(r"^documentation_documentation", old_name):
            reasons.append("Removed repetitive prefixes")

        if re.search(r"_[a-f0-9]{8,}$", old_name):
            reasons.append("Removed hash suffix")

        if re.search(r"[^a-zA-Z0-9._-]", old_name):
            reasons.append("Cleaned special characters")

        if len(new_name) < len(old_name):
            reasons.append("Shortened filename")

        return "; ".join(reasons) if reasons else "General cleanup"

    def create_execution_script(self, plan, output_file):
        """Create execution script."""
        logger.info(f"\n🚀 Creating execution script: {output_file}")

        script_content = f'''#!/usr/bin/env python3
"""
Smart File Organizer - Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_organization():
    """Execute the smart organization plan."""
    logger.info("🧠 EXECUTING SMART FILE ORGANIZATION")
    logger.info("=" * 60)
    logger.info("Fixes filename mess AND organizes files by type")
    print()
    
    # Create backup directory
    backup_dir = Path(Path("/Users/steven/smart_organizer_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Create target directories
    target_dirs = {[str(d) for d in plan['directories_to_create']]}
    for target_dir in target_dirs:
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created directory: {{target_dir}}")
    
    # Python file renames
    python_renames = {plan['python_renames']}
    logger.info(f"\\n🐍 Renaming {{len(python_renames)}} Python files...")
    
    for i, rename in enumerate(python_renames, 1):
        old_path = rename['old_path']
        new_path = old_path.parent / rename['new_name']
        
        logger.info(f"   {{i}}/{{len(python_renames)}}: {{rename['old_name']}} → {{rename['new_name']}}")
        logger.info(f"     Reason: {{rename['reason']}}")
        
        try:
            # Create backup
            backup_path = backup_dir / rename['old_name']
            shutil.copy2(old_path, backup_path)
            
            # Rename file
            old_path.rename(new_path)
            logger.info(f"     ✅ Success")
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
    
    # File moves
    file_moves = {plan['file_moves']}
    logger.info(f"\\n📁 Moving {{len(file_moves)}} files to organized directories...")
    
    for i, move in enumerate(file_moves, 1):
        old_path = move['old_path']
        new_path = move['new_path']
        
        logger.info(f"   {{i}}/{{len(file_moves)}}: {{move['old_name']}} → {{move['extension']}} directory")
        logger.info(f"     From: {{old_path}}")
        logger.info(f"     To: {{new_path}}")
        
        try:
            # Create backup
            backup_path = backup_dir / move['old_name']
            shutil.copy2(old_path, backup_path)
            
            # Move file
            shutil.move(str(old_path), str(new_path))
            logger.info(f"     ✅ Success")
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
    
    logger.info(f"\\n✅ Smart organization complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🐍 Python files cleaned and kept in place")
    logger.info(f"📁 Other files organized by type")
    logger.info(f"🔄 To rollback, use the backup directory")

if __name__ == "__main__":
    execute_organization()
'''

        with open(output_file, "w") as f:
            f.write(script_content)

        os.chmod(output_file, 0o755)
        logger.info(f"   Execution script created: {output_file}")

    def generate_report(self, plan):
        """Generate organization report."""
        logger.info(f"\n📊 ORGANIZATION REPORT")
        logger.info("=" * 80)

        logger.info(f"🐍 PYTHON FILE RENAMES")
        logger.info(f"   Files to rename: {len(plan['python_renames'])}")
        logger.info(f"   (Kept in ~/Documents/python)")

        logger.info(f"\n📁 FILE MOVES BY TYPE")
        file_moves = plan["file_moves"]
        by_extension = defaultdict(list)
        for move in file_moves:
            by_extension[move["extension"]].append(move)

        for ext, moves in by_extension.items():
            target_dir = self.file_type_dirs.get(ext, "Unknown")
            logger.info(f"   {ext}: {len(moves)} files → {target_dir}")

        logger.info(f"\n📁 DIRECTORIES TO CREATE")
        for target_dir in plan["directories_to_create"]:
            logger.info(f"   {target_dir}")

        logger.info(f"\n🔧 PYTHON RENAME EXAMPLES")
        for i, rename in enumerate(plan["python_renames"][:10], 1):
            logger.info(f"   {i}. {rename['old_name']} → {rename['new_name']}")
            logger.info(f"      Reason: {rename['reason']}")

        logger.info(f"\n📁 FILE MOVE EXAMPLES")
        for i, move in enumerate(file_moves[:10], 1):
            logger.info(f"   {i}. {move['old_name']} → {move['extension']} directory")
            logger.info(f"      From: {move['old_path']}")
            logger.info(f"      To: {move['new_path']}")


def main():
    """Main execution function."""
    logger.info("🧠 SMART FILE ORGANIZER")
    logger.info("=" * 80)
    logger.info("Fixes filename mess AND organizes files by type")
    logger.info("HTML → ~/Documents/html, MD → ~/Documents/markdown, etc.")
    print()

    organizer = SmartOrganizer()

    # Analyze files
    python_files, other_files = organizer.analyze_files()

    # Create organization plan
    plan = organizer.create_organization_plan(python_files, other_files)

    # Create execution script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    execution_script = f"/Users/steven/smart_organizer_{timestamp}.py"
    organizer.create_execution_script(plan, execution_script)

    # Generate report
    organizer.generate_report(plan)

    logger.info(f"\n💾 BACKUP & SAFETY")
    logger.info(f"   Execution script: {execution_script}")
    logger.info(f"   🛡️  All changes will be backed up!")

    logger.info(f"\n🚀 NEXT STEPS")
    logger.info(f"   1. Review the organization plan above")
    logger.info(f"   2. Run the execution script: python3 {execution_script}")
    logger.info(f"   3. Files will be organized by type!")

    logger.info(f"\n✅ SMART ORGANIZER READY!")
    logger.info(f"   This will fix the filename mess AND organize properly!")


if __name__ == "__main__":
    main()
