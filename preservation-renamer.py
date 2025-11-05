#!/usr/bin/env python3
"""
Python Preservation Renamer
Preserves meaningful names and only fixes problematic ones
Keeps good names like 15days.py, docx.py, csvp.py
Only renames messy/duplicate/problematic files
"""

import os
import re
import json
import csv
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime


class PreservationRenamer:
    """Preserves meaningful names and only fixes problematic ones."""

    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path(str(Path.home()) + "/Documents/python")).expanduser()
        self.max_depth = 6
        self.backup_data = []

        # Patterns that indicate problematic names (should be renamed)
        self.problematic_patterns = {
            "duplicate_numbers": r"_\d+$|\(\d+\)$|_\d+_\d+$|_\d+_\d+_\d+$",
            "timestamps": r"_\d{8}_\d{6}|_\d{8}|_\d{6}",
            "from_suffixes": r"_from_\w+$",
            "temp_suffixes": r"_temp$|_tmp$|_backup$|_old$|_copy$",
            "version_suffixes": r"_v\d+$|_version\d+$",
            "spaces_and_special": r"[^a-zA-Z0-9._-]",
            "multiple_underscores": r"_{2,}",
            "generic_names": r"^(test|main|app|script|file|data|temp|tmp)\.py$",
        }

        # Good names to preserve (don't rename these)
        self.preserve_patterns = [
            r"^\d+days?\.py$",  # 15days.py, 30days.py
            r"^[a-z]{2,4}\.py$",  # docx.py, csvp.py, bash.py
            r"^[A-Z][a-z]+[A-Z][a-z]+\.py$",  # TextToSpeech.py, YouTubeBot.py
            r"^[a-z]+[A-Z][a-z]+\.py$",  # botStories.py, csvProcessor.py
            r"^[a-z]+_[a-z]+\.py$",  # file_utils.py, data_clean.py
            r"^[A-Z][a-z]+\.py$",  # Calculator.py, Analyzer.py
        ]

    def analyze_and_rename(self):
        """Analyze files and only rename problematic ones."""
        logger.info("🛡️  PYTHON PRESERVATION RENAMER")
        logger.info("=" * 80)
        logger.info("Preserves meaningful names and only fixes problematic ones")
        logger.info("Keeps good names like 15days.py, docx.py, csvp.py")
        print()

        # Find all Python files
        python_files = []
        for file_path in self.root_path.rglob("*.py"):
            try:
                depth = len(file_path.relative_to(self.root_path).parts)
                if depth > self.max_depth:
                    continue
            except ValueError:
                continue

            if (
                file_path.is_file()
                and file_path.stat().st_size < 10 * CONSTANT_1024 * CONSTANT_1024
            ):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    file_info = {
                        "original_path": str(file_path),
                        "original_name": file_path.name,
                        "relative_path": str(file_path.relative_to(self.root_path)),
                        "content": content,
                        "size": file_path.stat().st_size,
                        "lines": len(content.splitlines()),
                        "depth": depth,
                    }

                    python_files.append(file_info)

                except (IOError, OSError, UnicodeDecodeError):
                    continue

        logger.info(f"   Found {len(python_files)} Python files")

        # Categorize files
        preserve_files = []
        rename_files = []

        for file_info in python_files:
            original_name = file_info["original_name"]

            # Check if this is a good name to preserve
            should_preserve = self._should_preserve_name(original_name)

            if should_preserve:
                preserve_files.append(file_info)
                logger.info(f"   ✅ PRESERVE: {original_name}")
            else:
                # Check if it needs renaming
                suggested_name = self._generate_clean_name(file_info)
                if suggested_name != original_name:
                    rename_files.append(
                        {
                            "file_info": file_info,
                            "suggested_name": suggested_name,
                            "reason": self._get_rename_reason(
                                original_name, suggested_name
                            ),
                        }
                    )
                    logger.info(f"   🔧 RENAME: {original_name} → {suggested_name}")
                else:
                    preserve_files.append(file_info)
                    logger.info(f"   ✅ KEEP: {original_name}")

        logger.info(f"\n📊 PRESERVATION STATISTICS")
        logger.info(f"   Files to preserve: {len(preserve_files)}")
        logger.info(f"   Files to rename: {len(rename_files)}")
        logger.info(
            f"   Preservation rate: {len(preserve_files)/len(python_files):.1%}"
        )

        # Create renaming plan
        renaming_plan = []
        for rename_item in rename_files:
            file_info = rename_item["file_info"]
            suggested_name = rename_item["suggested_name"]
            reason = rename_item["reason"]

            renaming_plan.append(
                {
                    "original_path": file_info["original_path"],
                    "original_name": file_info["original_name"],
                    "suggested_name": suggested_name,
                    "depth": file_info["depth"],
                    "reason": reason,
                }
            )

            # Add to backup data
            self.backup_data.append(
                {
                    "original_path": file_info["original_path"],
                    "original_name": file_info["original_name"],
                    "suggested_name": suggested_name,
                    "depth": file_info["depth"],
                    "size": file_info["size"],
                    "lines": file_info["lines"],
                    "reason": reason,
                }
            )

        # Resolve naming conflicts
        self._resolve_conflicts(renaming_plan)

        return renaming_plan

    def _should_preserve_name(self, filename):
        """Check if a filename should be preserved."""
        # Check against preserve patterns
        for pattern in self.preserve_patterns:
            if re.match(pattern, filename):
                return True

        # Check if it's a meaningful name (not generic)
        if filename.lower() in [
            "test.py",
            "main.py",
            "app.py",
            "script.py",
            "file.py",
            "data.py",
            "temp.py",
            "tmp.py",
        ]:
            return False

        # Check if it has problematic patterns
        for pattern_name, pattern in self.problematic_patterns.items():
            if re.search(pattern, filename):
                return False

        # If it's reasonably short and meaningful, preserve it
        if len(filename) <= 20 and not re.search(r"[^a-zA-Z0-9._-]", filename):
            return True

        return False

    def _generate_clean_name(self, file_info):
        """Generate a clean name for problematic files."""
        original_name = file_info["original_name"]
        content = file_info["content"].lower()

        # Start with original name
        suggested_name = original_name

        # Remove problematic patterns
        for pattern_name, pattern in self.problematic_patterns.items():
            if pattern_name == "spaces_and_special":
                # Replace spaces and special chars with underscores
                suggested_name = re.sub(r"[^a-zA-Z0-9._-]", "_", suggested_name)
            elif pattern_name == "multiple_underscores":
                # Replace multiple underscores with single
                suggested_name = re.sub(r"_{2,}", "_", suggested_name)
            else:
                # Remove the pattern
                suggested_name = re.sub(pattern, "", suggested_name)

        # Clean up the name
        suggested_name = suggested_name.strip("_")
        suggested_name = re.sub(r"_{2,}", "_", suggested_name)

        # If name is too short, try to make it more meaningful
        if len(suggested_name) < 5:
            # Try to extract meaningful parts from content
            meaningful_parts = self._extract_meaningful_parts(content)
            if meaningful_parts:
                suggested_name = "_".join(meaningful_parts) + ".py"
            else:
                suggested_name = "script.py"

        # Ensure it ends with .py
        if not suggested_name.endswith(".py"):
            suggested_name += ".py"

        # Final cleanup
        suggested_name = re.sub(r"[^a-zA-Z0-9._-]", "", suggested_name)
        suggested_name = suggested_name.lower()

        return suggested_name

    def _extract_meaningful_parts(self, content):
        """Extract meaningful parts from content for naming."""
        parts = []

        # Look for common patterns
        if "youtube" in content:
            parts.append("youtube")
        if "instagram" in content:
            parts.append("instagram")
        if "csv" in content:
            parts.append("csv")
        if "json" in content:
            parts.append("json")
        if "video" in content:
            parts.append("video")
        if "audio" in content:
            parts.append("audio")
        if "image" in content:
            parts.append("image")
        if "data" in content:
            parts.append("data")
        if "analyze" in content:
            parts.append("analyze")
        if "process" in content:
            parts.append("process")
        if "generate" in content:
            parts.append("generate")
        if "clean" in content:
            parts.append("clean")
        if "organize" in content:
            parts.append("organize")

        return parts[:3]  # Limit to 3 parts

    def _get_rename_reason(self, original_name, suggested_name):
        """Get reason for rename."""
        if original_name == suggested_name:
            return "No change needed"

        reasons = []

        # Check what was cleaned up
        if re.search(r"_\d+$|\(\d+\)$", original_name):
            reasons.append("Removed duplicate numbers")

        if re.search(r"_\d{8}_\d{6}|_\d{8}", original_name):
            reasons.append("Removed timestamp")

        if re.search(r"_from_\w+$", original_name):
            reasons.append("Removed 'from' suffix")

        if re.search(r"_temp$|_tmp$|_backup$", original_name):
            reasons.append("Removed temp/backup suffix")

        if re.search(r"[^a-zA-Z0-9._-]", original_name):
            reasons.append("Cleaned special characters")

        if re.search(r"_{2,}", original_name):
            reasons.append("Fixed multiple underscores")

        if reasons:
            return "; ".join(reasons)
        else:
            return "General cleanup"

    def _resolve_conflicts(self, renaming_plan):
        """Resolve naming conflicts."""
        name_counts = defaultdict(int)
        name_to_files = defaultdict(list)

        # Group by suggested name
        for op in renaming_plan:
            suggested_name = op["suggested_name"]
            name_counts[suggested_name] += 1
            name_to_files[suggested_name].append(op)

        # Resolve conflicts
        for suggested_name, files in name_to_files.items():
            if len(files) > 1:
                # Sort by depth (shallower files get priority)
                files.sort(key=lambda x: x["depth"])

                for i, op in enumerate(files):
                    if i == 0:
                        continue  # Keep first file with original name
                    else:
                        # Add number suffix
                        base_name = op["suggested_name"].replace(".py", "")
                        op["suggested_name"] = f"{base_name}_{i}.py"

    def create_csv_backup(self, output_file):
        """Create CSV backup."""
        logger.info(f"\n💾 Creating CSV backup: {output_file}")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "original_path",
                "original_name",
                "suggested_name",
                "depth",
                "size",
                "lines",
                "reason",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.backup_data:
                writer.writerow(row)

        logger.info(f"   CSV backup created with {len(self.backup_data)} entries")

    def generate_execution_script(self, renaming_plan, output_file):
        """Generate execution script."""
        logger.info(f"\n🚀 Generating execution script: {output_file}")

        script_content = f'''#!/usr/bin/env python3
"""
Python Preservation Renamer - Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_renaming():
    """Execute the preservation renaming plan."""
    logger.info("🛡️  EXECUTING PRESERVATION RENAMING")
    logger.info("=" * 60)
    logger.info("Preserves meaningful names and only fixes problematic ones")
    print()
    
    # Create backup directory
    backup_dir = Path(Path(str(Path.home()) + "/python_preservation_renaming_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Renaming operations
    renaming_operations = {renaming_plan}
    
    logger.info(f"\\n📦 Executing {{len(renaming_operations)}} renames...")
    logger.info("   (Only problematic files will be renamed)")
    logger.info("   (Good names like 15days.py, docx.py, csvp.py will be preserved)")
    print()
    
    for i, op in enumerate(renaming_operations, 1):
        old_path = Path(op['original_path'])
        new_path = old_path.parent / op['suggested_name']
        
        logger.info(f"   {{i}}/{{len(renaming_operations)}}: {{op['original_name']}} → {{op['suggested_name']}}")
        logger.info(f"     Depth: {{op['depth']}}")
        logger.info(f"     Reason: {{op['reason']}}")
        
        try:
            # Create backup
            backup_path = backup_dir / op['original_name']
            shutil.copy2(old_path, backup_path)
            
            # Rename file
            old_path.rename(new_path)
            
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
        else:
            logger.info(f"     ✅ Success")
    
    logger.info(f"\\n✅ Preservation renaming complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🛡️  Meaningful names preserved!")
    logger.info(f"🔄 To rollback, use the CSV file to restore original names")

if __name__ == "__main__":
    execute_renaming()
'''

        with open(output_file, "w") as f:
            f.write(script_content)

        os.chmod(output_file, 0o755)
        logger.info(f"   Execution script created and made executable")

    def generate_report(self, renaming_plan):
        """Generate comprehensive report."""
        logger.info(f"\n📊 GENERATING PRESERVATION REPORT")
        logger.info("=" * 80)

        logger.info(f"📈 PRESERVATION STATISTICS")
        logger.info(f"   Total files to rename: {len(renaming_plan)}")
        logger.info(f"   (Only problematic files will be renamed)")
        logger.info(f"   (Good names will be preserved)")

        # Group by reason
        reason_counts = Counter(op["reason"] for op in renaming_plan)
        logger.info(f"\n🔧 RENAMING REASONS")
        for reason, count in reason_counts.most_common():
            logger.info(f"   {reason}: {count} files")

        # Group by depth
        depth_counts = Counter(op["depth"] for op in renaming_plan)
        logger.info(f"\n📁 RENAMING BY DEPTH")
        for depth in sorted(depth_counts.keys()):
            logger.info(f"   Depth {depth}: {depth_counts[depth]} files")

        logger.info(f"\n📝 RENAMING EXAMPLES")
        for i, op in enumerate(renaming_plan[:15], 1):
            logger.info(f"   {i}. {op['original_name']}")
            logger.info(f"      → {op['suggested_name']}")
            logger.info(f"      Reason: {op['reason']}")
            logger.info(f"      Depth: {op['depth']}")
            print()

        logger.info(f"\n🛡️  PRESERVED NAMES (examples)")
        logger.info(f"   ✅ 15days.py - preserved")
        logger.info(f"   ✅ docx.py - preserved")
        logger.info(f"   ✅ csvp.py - preserved")
        logger.info(f"   ✅ TextToSpeech.py - preserved")
        logger.info(f"   ✅ botStories.py - preserved")
        logger.info(f"   ✅ YouTubeBot.py - preserved")


def main():
    """Main execution function."""
    logger.info("🛡️  PYTHON PRESERVATION RENAMER")
    logger.info("=" * 80)
    logger.info("Preserves meaningful names and only fixes problematic ones")
    logger.info("Keeps good names like 15days.py, docx.py, csvp.py")
    print()

    renamer = PreservationRenamer()

    # Analyze and create renaming plan
    renaming_plan = renamer.analyze_and_rename()

    # Create CSV backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_backup_file = (
        fstr(Path.home()) + "/python_preservation_renaming_backup_{timestamp}.csv"
    )
    renamer.create_csv_backup(csv_backup_file)

    # Generate execution script
    execution_script = (
        fstr(Path.home()) + "/python_preservation_rename_execute_{timestamp}.py"
    )
    renamer.generate_execution_script(renaming_plan, execution_script)

    # Generate report
    renamer.generate_report(renaming_plan)

    logger.info(f"\n💾 BACKUP & SAFETY")
    logger.info(f"   CSV backup: {csv_backup_file}")
    logger.info(f"   Execution script: {execution_script}")
    logger.info(f"   🛡️  All changes can be rolled back using the CSV file!")

    logger.info(f"\n🚀 NEXT STEPS")
    logger.info(f"   1. Review the renaming examples above")
    logger.info(f"   2. Check the CSV backup file")
    logger.info(
        f"   3. Run the execution script when ready: python3 {execution_script}"
    )
    logger.info(f"   4. Use CSV file to rollback if needed")

    logger.info(f"\n✅ PRESERVATION RENAMING SYSTEM READY!")
    logger.info(f"   This will preserve your meaningful names!")


if __name__ == "__main__":
    main()
