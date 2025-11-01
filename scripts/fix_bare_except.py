
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
🔧 BARE EXCEPT FIXER
===================
Automatically detect and fix bare except clauses with intelligent
exception type suggestions based on code context.

Features:
✨ AST-based detection of bare except clauses
✨ Context-aware exception type suggestions
✨ Safe backup before modification
✨ Detailed fix report
✨ Dry-run mode for review
"""

import os
import sys
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    END = "\CONSTANT_033[0m"
    BOLD = "\CONSTANT_033[1m"

class BareExceptFixer:
    """Fix bare except clauses intelligently"""

    # Common exception patterns based on operations
    EXCEPTION_PATTERNS = {
        'file': ['OSError', 'IOError', 'FileNotFoundError'],
        'network': ['requests.RequestException', 'urllib.error.URLError', 'ConnectionError'],
        'json': ['json.JSONDecodeError', 'ValueError'],
        'import': ['ImportError', 'ModuleNotFoundError'],
        'key': ['KeyError', 'AttributeError'],
        'value': ['ValueError', 'TypeError'],
        'index': ['IndexError', 'KeyError'],
    }

    def __init__(self, target_dir: str, dry_run: bool = True):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"bare_except_backup_{timestamp}"

        self.stats = {
            'files_scanned': 0,
            'bare_excepts_found': 0,
            'files_fixed': 0,
            'fixes_applied': 0,
        }

        self.fixes = []

    def detect_context(self, code_before: str) -> str:
        """Detect what kind of operation might throw exception"""
        code_lower = code_before.lower()

        if any(word in code_lower for word in ['open(', 'read', 'write', 'file']):
            return 'file'
        elif any(word in code_lower for word in ['request', 'urllib', 'http', 'url']):
            return 'network'
        elif 'json' in code_lower:
            return 'json'
        elif 'import' in code_lower:
            return 'import'
        elif '[' in code_before and ']' in code_before:
            return 'index'
        elif any(word in code_lower for word in ['int(', 'float(', 'str(']):
            return 'value'

        return 'general'

    def suggest_exceptions(self, context: str) -> str:
        """Suggest appropriate exceptions"""
        if context in self.EXCEPTION_PATTERNS:
            exceptions = self.EXCEPTION_PATTERNS[context]
            if len(exceptions) == 1:
                return exceptions[0]
            return f"({', '.join(exceptions)})"

        return 'Exception'

    def find_bare_excepts(self, filepath: Path) -> List[Dict]:
        """Find all bare except clauses in file"""
        bare_excepts = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()

            # Parse AST
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    # Check if it's a bare except (no exception type)
                    if node.type is None:
                        line_num = node.lineno

                        # Get context (5 lines before)
                        context_start = max(0, line_num - 6)
                        context_lines = lines[context_start:line_num-1]
                        context_code = '\n'.join(context_lines)

                        # Detect operation type
                        context_type = self.detect_context(context_code)
                        suggested = self.suggest_exceptions(context_type)

                        bare_excepts.append({
                            'line': line_num,
                            'context_type': context_type,
                            'suggested': suggested,
                            'original_line': lines[line_num - 1] if line_num <= len(lines) else '',
                        })

        except SyntaxError:
            pass  # Skip files with syntax errors
        except Exception:
            pass

        return bare_excepts

    def fix_file(self, filepath: Path, bare_excepts: List[Dict]) -> bool:
        """Fix bare except clauses in file"""

        if not bare_excepts:
            return False

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Create backup
            if not self.dry_run:
                backup_path = self.backup_dir / filepath.relative_to(self.target_dir)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

            # Fix bare excepts (in reverse order to preserve line numbers)
            for except_info in reversed(bare_excepts):
                line_idx = except_info['line'] - 1
                original = lines[line_idx]

                # Preserve indentation
                indent = len(original) - len(original.lstrip())

                # Create fixed line
                suggested = except_info['suggested']
                fixed = f"{' ' * indent}except {suggested}:\n"

                # Apply fix
                if not self.dry_run:
                    lines[line_idx] = fixed

                self.fixes.append({
                    'file': str(filepath.relative_to(self.target_dir)),
                    'line': except_info['line'],
                    'original': original.strip(),
                    'fixed': fixed.strip(),
                    'context': except_info['context_type'],
                    'suggested': suggested,
                })

                self.stats['fixes_applied'] += 1

            # Write fixed file
            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

            self.stats['files_fixed'] += 1
            return True

        except Exception as e:
            logger.info(f"{Colors.RED}Error fixing {filepath}: {e}{Colors.END}")
            return False

    def scan_and_fix(self):
        """Scan directory and fix bare excepts"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔧 SCANNING FOR BARE EXCEPT CLAUSES")
        logger.info(f"{'='*80}{Colors.END}\n")

        python_files = list(self.target_dir.rglob("*.py"))

        # Skip backup directories
        python_files = [f for f in python_files if 'backup' not in str(f).lower()]

        logger.info(f"{Colors.GREEN}Scanning {len(python_files)} Python files...{Colors.END}\n")

        for idx, filepath in enumerate(python_files, 1):
            if idx % CONSTANT_100 == 0:
                logger.info(f"{Colors.YELLOW}Progress: {idx}/{len(python_files)}...{Colors.END}", end='\r')

            self.stats['files_scanned'] += 1

            bare_excepts = self.find_bare_excepts(filepath)

            if bare_excepts:
                self.stats['bare_excepts_found'] += len(bare_excepts)

                logger.info(f"\n{Colors.CYAN}📄 {filepath.relative_to(self.target_dir)}{Colors.END}")
                logger.info(f"   Found {len(bare_excepts)} bare except clause(s)")

                for except_info in bare_excepts:
                    logger.info(f"   Line {except_info['line']}: {Colors.YELLOW}{except_info['original_line'].strip()}{Colors.END}")
                    logger.info(f"   → Fix: {Colors.GREEN}except {except_info['suggested']}:{Colors.END}")

                # Apply fix
                self.fix_file(filepath, bare_excepts)

        logger.info(f"\n{Colors.GREEN}✅ Scan complete!{Colors.END}")

    def generate_report(self):
        """Generate fix report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"BARE_EXCEPT_FIX_REPORT_{timestamp}.md"
        csv_file = self.target_dir / f"bare_except_fixes_{timestamp}.csv"

        # Markdown report
        with open(report_file, 'w') as f:
            f.write("# 🔧 BARE EXCEPT FIX REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE FIX'}\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## 📊 FIX SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Files Scanned | {self.stats['files_scanned']:,} |\n")
            f.write(f"| Bare Excepts Found | {self.stats['bare_excepts_found']:,} |\n")
            f.write(f"| Files Fixed | {self.stats['files_fixed']:,} |\n")
            f.write(f"| Fixes Applied | {self.stats['fixes_applied']:,} |\n")
            if not self.dry_run:
                f.write(f"| Backup Location | `{self.backup_dir}` |\n")
            f.write(Path("\n"))

            # Fixes by context type
            f.write("## 🎯 FIXES BY CONTEXT TYPE\n\n")
            by_context = defaultdict(int)
            for fix in self.fixes:
                by_context[fix['context']] += 1

            for context, count in sorted(by_context.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{context}**: {count} fixes\n")
            f.write(Path("\n"))

            # Detailed fixes
            f.write("## 📝 DETAILED FIXES\n\n")

            by_file = defaultdict(list)
            for fix in self.fixes:
                by_file[fix['file']].append(fix)

            for file_path in sorted(by_file.keys()):
                fixes = by_file[file_path]
                f.write(f"### `{file_path}`\n")
                f.write(f"**Fixes:** {len(fixes)}\n\n")

                for fix in fixes:
                    f.write(f"**Line {fix['line']}**\n")
                    f.write(f"- Before: `{fix['original']}`\n")
                    f.write(f"- After: `{fix['fixed']}`\n")
                    f.write(f"- Context: {fix['context']}\n\n")

        # CSV export
        with open(csv_file, 'w') as f:
            f.write("file,line,original,fixed,context,suggested_exception\n")
            for fix in self.fixes:
                f.write(f'"{fix["file"]}",{fix["line"]},"{fix["original"]}","{fix["fixed"]}",{fix["context"]},{fix["suggested"]}\n')

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")

        return report_file, csv_file

    def run(self):
        """Run the fixer"""

        logger.info(f"{Colors.BOLD}{Colors.CYAN}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║                    🔧 BARE EXCEPT FIXER 🧠                                    ║")
        logger.info("║                                                                               ║")
        logger.info("║              Intelligent Exception Handling Improvement                      ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}🛡️ MODE: DRY RUN (no files will be modified){Colors.END}\n")
        else:
            logger.info(f"{Colors.RED}⚠️ MODE: LIVE FIX (files will be modified!){Colors.END}\n")

        # Scan and fix
        self.scan_and_fix()

        # Generate report
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✨ GENERATING REPORT")
        logger.info(f"{'='*80}{Colors.END}\n")

        self.generate_report()

        # Summary
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🚀 FIX COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(f"  Files Scanned: {Colors.CYAN}{self.stats['files_scanned']:,}{Colors.END}")
        logger.info(f"  Bare Excepts: {Colors.CYAN}{self.stats['bare_excepts_found']:,}{Colors.END}")
        logger.info(f"  Files Fixed: {Colors.CYAN}{self.stats['files_fixed']:,}{Colors.END}")
        logger.info(f"  Fixes Applied: {Colors.CYAN}{self.stats['fixes_applied']:,}{Colors.END}\n")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}⚠️ DRY RUN complete. Use --live to apply fixes.{Colors.END}\n")
        else:
            logger.info(f"{Colors.GREEN}✅ Fixes applied! Backups in: {self.backup_dir}{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🔧 Fix bare except clauses")
    parser.add_argument('--target', type=str, required=True, help='Target directory')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run (safe)')
    parser.add_argument('--live', action='store_true', help='Apply fixes')

    args = parser.parse_args()

    fixer = BareExceptFixer(args.target, dry_run=not args.live)
    fixer.run()


if __name__ == "__main__":
    main()
