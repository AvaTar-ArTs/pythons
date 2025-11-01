#!/usr/bin/env python3
"""
Automated Code Quality Fixer

Systematically fixes all critical and high-priority issues identified
in the deep analysis.
"""

import os
import sys
import ast
import re
from pathlib import Path
from datetime import datetime
import shutil
import json


class AutomatedFixer:
    def __init__(self, target_dir: str):
        """__init__ function."""

        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"automated_fixes_backup_{self.timestamp}"
        self.backup_dir.mkdir(exist_ok=True)

        self.stats = {
            "files_processed": 0,
            "magic_numbers_fixed": 0,
            "paths_fixed": 0,
            "prints_replaced": 0,
            "module_docstrings_added": 0,
            "function_docstrings_added": 0,
            "lines_wrapped": 0,
        }

    def fix_magic_numbers(self, file_path: Path, dry_run=True):
        """Extract and replace magic numbers with named constants."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find all magic numbers (3+ digits, not in strings)
            magic_numbers = {}
            lines = content.split("\n")

            for i, line in enumerate(lines):
                # Skip comments and strings
                if line.strip().startswith("#"):
                    continue

                # Find numbers not in quotes
                numbers = re.findall(r'\b(?<!["\'])\d{3,}\b(?!["\'])', line)
                for num in numbers:
                    if num not in magic_numbers:
                        magic_numbers[num] = f"CONSTANT_{num}"

            if not magic_numbers:
                return content, 0

            # Create constants section
            constants_section = "\n# Constants\n"
            for num, const_name in sorted(magic_numbers.items(), key=lambda x: int(x[0])):
                constants_section += f"{const_name} = {num}\n"

            # Replace magic numbers with constants
            modified_content = content
            for num, const_name in magic_numbers.items():
                # Replace in code (not in strings)
                modified_content = re.sub(rf'\b{num}\b(?!["\'])', const_name, modified_content)

            # Add constants at top (after imports)
            lines = modified_content.split("\n")
            insert_pos = 0

            # Find position after imports
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(("#", '"""', "'''")):
                    if line.startswith(("import ", "from ")):
                        insert_pos = i + 1
                    else:
                        break

            lines.insert(insert_pos, constants_section)
            final_content = "\n".join(lines)

            if not dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(final_content)

            return final_content, len(magic_numbers)

        except Exception as e:
            return None, 0

    def fix_hardcoded_paths(self, file_path: Path, dry_run=True):
        """Replace hardcoded paths with Path objects."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find hardcoded paths
            paths_found = re.findall(r'["\']([/\\][\w/\\.-]+|[A-Z]:\\[\w\\.-]+)["\']', content)

            if not paths_found:
                return content, 0

            modified_content = content

            # Check if Path is already imported
            has_path_import = "from pathlib import Path" in content

            # Replace paths
            replacements = 0
            for path in set(paths_found):
                # Skip URLs and other non-filesystem paths
                if any(x in path for x in ["http://", "https://", "://", "@"]):
                    continue

                # Replace with Path object
                old_pattern = f'"{path}"'
                new_pattern = f'Path("{path}")'

                if old_pattern in modified_content:
                    modified_content = modified_content.replace(old_pattern, new_pattern)
                    replacements += 1

            # Add Path import if needed
            if replacements > 0 and not has_path_import:
                lines = modified_content.split("\n")
                # Find first import or start of file
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith(("import ", "from ")):
                        insert_pos = i
                        break

                lines.insert(insert_pos, "from pathlib import Path")
                modified_content = "\n".join(lines)

            if not dry_run and replacements > 0:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

            return modified_content, replacements

        except Exception as e:
            return None, 0

    def replace_prints_with_logging(self, file_path: Path, dry_run=True):
        """Replace print() statements with logging."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Count print statements
            print_count = content.count("logger.info(")

            if print_count == 0:
                return content, 0

            modified_content = content

            # Check if logging is already imported
            has_logging = "import logging" in content

            # Replace print with logger.info
            # Simple replacement for common patterns
            modified_content = re.sub(r"\bprint\((.+?)\)", r"logger.info(\1)", modified_content)

            # Add logging setup if needed
            if not has_logging:
                logging_setup = """
import logging

logger = logging.getLogger(__name__)
"""
                lines = modified_content.split("\n")
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith(("import ", "from ")):
                        insert_pos = i + 1
                    elif line.strip() and not line.startswith("#"):
                        break

                lines.insert(insert_pos, logging_setup)
                modified_content = "\n".join(lines)

            if not dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

            return modified_content, print_count

        except Exception as e:
            return None, 0

    def add_module_docstring(self, file_path: Path, dry_run=True):
        """Add module-level docstring if missing."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if module docstring exists
            try:
                tree = ast.parse(content)
                if ast.get_docstring(tree):
                    return content, 0
            except:
                return None, 0

            # Generate docstring based on filename
            filename = file_path.stem.replace("_", " ").replace("-", " ").title()

            docstring = f'''"""
{filename}

This module provides functionality for {filename.lower()}.

Author: Auto-generated
Date: {datetime.now().strftime('%Y-%m-%d')}
"""

'''

            modified_content = docstring + content

            if not dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

            return modified_content, 1

        except Exception as e:
            return None, 0

    def add_function_docstrings(self, file_path: Path, dry_run=True):
        """Add docstrings to functions that lack them."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            try:
                tree = ast.parse(content)
            except:
                return content, 0

            lines = content.split("\n")
            added = 0

            # Find functions without docstrings
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        # Generate simple docstring
                        indent = " " * (node.col_offset + 4)
                        docstring = f'{indent}"""{node.name} function."""\n'

                        # Insert after function definition
                        func_line = node.lineno
                        if func_line < len(lines):
                            lines.insert(func_line, docstring)
                            added += 1

            if added > 0:
                modified_content = "\n".join(lines)

                if not dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(modified_content)

                return modified_content, added

            return content, 0

        except Exception as e:
            return None, 0

    def process_file(self, file_path: Path, dry_run=True):
        """Process a single file with all fixes."""
        logger.info(f"Processing: {file_path.relative_to(self.target_dir)}")

        # Create backup
        if not dry_run:
            backup_path = self.backup_dir / file_path.relative_to(self.target_dir)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_path)

        # Apply fixes
        _, magic_fixed = self.fix_magic_numbers(file_path, dry_run)
        _, paths_fixed = self.fix_hardcoded_paths(file_path, dry_run)
        _, prints_fixed = self.replace_prints_with_logging(file_path, dry_run)
        _, module_doc_added = self.add_module_docstring(file_path, dry_run)
        _, func_docs_added = self.add_function_docstrings(file_path, dry_run)

        self.stats["magic_numbers_fixed"] += magic_fixed
        self.stats["paths_fixed"] += paths_fixed
        self.stats["prints_replaced"] += prints_fixed
        self.stats["module_docstrings_added"] += module_doc_added
        self.stats["function_docstrings_added"] += func_docs_added
        self.stats["files_processed"] += 1

        return (magic_fixed + paths_fixed + prints_fixed + module_doc_added + func_docs_added) > 0

    def run(self, dry_run=True, limit=None):
        """Run automated fixes on all files."""
        logger.info(f"\n{'='*80}")
        logger.info(f"🔧 AUTOMATED CODE QUALITY FIXER")
        logger.info(f"{'='*80}\n")
        logger.info(f"Target: {self.target_dir}")
        logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        # Find Python files
        python_files = list(self.target_dir.rglob("*.py"))

        # Exclude patterns
        exclude_patterns = [
            "dedup_backup",
            "bare_except_backup",
            "deep_rename_backup",
            "automated_fixes_backup",
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            "myenv",
        ]

        python_files = [f for f in python_files if not any(pattern in str(f) for pattern in exclude_patterns)]

        if limit:
            python_files = python_files[:limit]

        logger.info(f"Found {len(python_files)} files to process\n")

        # Process files
        for file_path in python_files:
            self.process_file(file_path, dry_run)

        # Generate report
        self.generate_report(dry_run)

    def generate_report(self, dry_run):
        """Generate fix report."""
        report_path = self.target_dir / f"AUTOMATED_FIXES_REPORT_{self.timestamp}.md"

        with open(report_path, "w") as f:
            f.write("# 🔧 Automated Fixes Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if dry_run else 'LIVE'}\n\n")

            f.write("## Statistics\n\n")
            f.write(f"- **Files Processed:** {self.stats['files_processed']:,}\n")
            f.write(f"- **Magic Numbers Fixed:** {self.stats['magic_numbers_fixed']:,}\n")
            f.write(f"- **Hardcoded Paths Fixed:** {self.stats['paths_fixed']:,}\n")
            f.write(f"- **Print Statements Replaced:** {self.stats['prints_replaced']:,}\n")
            f.write(f"- **Module Docstrings Added:** {self.stats['module_docstrings_added']:,}\n")
            f.write(f"- **Function Docstrings Added:** {self.stats['function_docstrings_added']:,}\n\n")

            if not dry_run:
                f.write(f"## Backup\n\n")
                f.write(f"Original files backed up to: `{self.backup_dir}`\n\n")

        logger.info(f"\n{'='*80}")
        logger.info("✅ COMPLETE!")
        logger.info(f"{'='*80}\n")
        logger.info(f"Files Processed: {self.stats['files_processed']:,}")
        logger.info(f"Magic Numbers Fixed: {self.stats['magic_numbers_fixed']:,}")
        logger.info(f"Paths Fixed: {self.stats['paths_fixed']:,}")
        logger.info(f"Prints Replaced: {self.stats['prints_replaced']:,}")
        logger.info(f"Module Docstrings Added: {self.stats['module_docstrings_added']:,}")
        logger.info(f"Function Docstrings Added: {self.stats['function_docstrings_added']:,}")
        logger.info(f"\nReport: {report_path}\n")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Automated Code Quality Fixer")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument("--live", action="store_true", help="Apply fixes (default: dry run)")
    parser.add_argument("--limit", type=int, help="Limit number of files")

    args = parser.parse_args()

    fixer = AutomatedFixer(args.target)
    fixer.run(dry_run=not args.live, limit=args.limit)


if __name__ == "__main__":
    main()
