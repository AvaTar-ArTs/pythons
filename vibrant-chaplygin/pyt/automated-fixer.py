class AutomatedFixer:
    """Automated code fixer"""

    def __init__(self, target_dir, backup_dir):
        self.target_dir = Path(target_dir)
        self.backup_dir = Path(backup_dir)

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

        return (
            magic_fixed
            + paths_fixed
            + prints_fixed
            + module_doc_added
            + func_docs_added
        ) > 0

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

        python_files = [
            f
            for f in python_files
            if not any(pattern in str(f) for pattern in exclude_patterns)
        ]

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
            f.write(
                f"- **Magic Numbers Fixed:** {self.stats['magic_numbers_fixed']:,}\n"
            )
            f.write(f"- **Hardcoded Paths Fixed:** {self.stats['paths_fixed']:,}\n")
            f.write(
                f"- **Print Statements Replaced:** {self.stats['prints_replaced']:,}\n"
            )
            f.write(
                f"- **Module Docstrings Added:** {self.stats['module_docstrings_added']:,}\n"
            )
            f.write(
                f"- **Function Docstrings Added:** {self.stats['function_docstrings_added']:,}\n\n"
            )

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
        logger.info(
            f"Module Docstrings Added: {self.stats['module_docstrings_added']:,}"
        )
        logger.info(
            f"Function Docstrings Added: {self.stats['function_docstrings_added']:,}"
        )
        logger.info(f"\nReport: {report_path}\n")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Automated Code Quality Fixer")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument(
        "--live", action="store_true", help="Apply fixes (default: dry run)"
    )
    parser.add_argument("--limit", type=int, help="Limit number of files")

    args = parser.parse_args()

    fixer = AutomatedFixer(args.target)
    fixer.run(dry_run=not args.live, limit=args.limit)


if __name__ == "__main__":
    main()
