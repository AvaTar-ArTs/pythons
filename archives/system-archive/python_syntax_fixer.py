#!/usr/bin/env python3
"""
Python Syntax Fixer and Code Organizer
Handles syntax errors gracefully and provides code quality improvements
"""

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import json


@dataclass
class SyntaxError:
    """Represents a syntax error with fix suggestions"""

    file_path: str
    line_number: int
    error_type: str
    error_message: str
    suggested_fix: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    auto_fixable: bool = False


@dataclass
class CodeQualityIssue:
    """Represents a code quality issue"""

    file_path: str
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    severity: str
    auto_fixable: bool = False


class PythonSyntaxFixer:
    """Advanced Python syntax fixer and code organizer"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.syntax_errors: List[SyntaxError] = []
        self.quality_issues: List[CodeQualityIssue] = []
        self.fixed_files: List[str] = []
        self.failed_files: List[str] = []

        # Common syntax error patterns and fixes
        self.error_patterns = {
            "print_statement": {
                "pattern": r"print\s+([^()].*)",
                "fix": r"print(\1)",
                "description": "Python 2 print statement needs parentheses",
            },
            "f_string_brackets": {
                "pattern": r'f"[^"]*\[[^"]*\[[^"]*"[^"]*\]',
                "fix": "Fix f-string bracket nesting",
                "description": "F-string with unmatched brackets",
            },
            "indentation_error": {
                "pattern": r"^\s*[^\s]",
                "fix": "Fix indentation",
                "description": "Inconsistent indentation",
            },
            "string_literal_eol": {
                "pattern": r'"[^"]*$',
                "fix": "Add closing quote",
                "description": "Unterminated string literal",
            },
        }

    def analyze_and_fix(self) -> Dict[str, Any]:
        """Analyze codebase and attempt to fix issues"""
        print("🔧 Analyzing Python codebase for syntax errors...")

        # Find all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"   Found {len(python_files)} Python files")

        # Analyze each file
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")

        # Attempt to fix issues
        self._attempt_fixes()

        # Generate quality report
        quality_report = self._generate_quality_report()

        return {
            "syntax_errors": self.syntax_errors,
            "quality_issues": self.quality_issues,
            "fixed_files": self.fixed_files,
            "failed_files": self.failed_files,
            "quality_report": quality_report,
            "summary": self._generate_summary(),
        }

    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file for syntax errors"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Try to parse the file
            try:
                ast.parse(content)
                # File is syntactically correct
                return
            except SyntaxError as e:
                # Record syntax error
                error = SyntaxError(
                    file_path=str(file_path),
                    line_number=e.lineno or 0,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    suggested_fix=self._suggest_fix(content, e),
                    severity=self._get_error_severity(e),
                    auto_fixable=self._is_auto_fixable(e),
                )
                self.syntax_errors.append(error)

        except UnicodeDecodeError:
            # Handle encoding issues
            error = SyntaxError(
                file_path=str(file_path),
                line_number=0,
                error_type="UnicodeDecodeError",
                error_message="Invalid UTF-8 encoding",
                suggested_fix="Convert to UTF-8 or fix encoding",
                severity="high",
                auto_fixable=True,
            )
            self.syntax_errors.append(error)

        except Exception as e:
            # Other errors
            error = SyntaxError(
                file_path=str(file_path),
                line_number=0,
                error_type=type(e).__name__,
                error_message=str(e),
                suggested_fix="Manual review required",
                severity="medium",
                auto_fixable=False,
            )
            self.syntax_errors.append(error)

    def _suggest_fix(self, content: str, error: SyntaxError) -> str:
        """Suggest a fix for a syntax error"""
        error_msg = str(error)

        # Print statement fixes
        if "Missing parentheses in call to" in error_msg and "print" in error_msg:
            return "Add parentheses around print statement arguments"

        # Indentation fixes
        if "unexpected indent" in error_msg or "unindent" in error_msg:
            return "Fix indentation - use 4 spaces consistently"

        # String literal fixes
        if "EOL while scanning string literal" in error_msg:
            return "Add closing quote to string literal"

        # F-string fixes
        if "f-string" in error_msg and "unmatched" in error_msg:
            return "Fix f-string bracket nesting or quotes"

        # General fixes
        if "invalid syntax" in error_msg:
            return "Review syntax around the error line"

        return "Manual review required"

    def _get_error_severity(self, error: SyntaxError) -> str:
        """Determine error severity"""
        error_msg = str(error)

        if "Missing parentheses" in error_msg:
            return "low"  # Easy to fix
        elif "unexpected indent" in error_msg or "unindent" in error_msg:
            return "medium"  # Moderate effort
        elif "EOL while scanning string literal" in error_msg:
            return "medium"  # Moderate effort
        elif "invalid syntax" in error_msg:
            return "high"  # Requires understanding
        else:
            return "critical"  # Complex issues

    def _is_auto_fixable(self, error: SyntaxError) -> bool:
        """Determine if error can be auto-fixed"""
        error_msg = str(error)

        # Auto-fixable errors
        if "Missing parentheses" in error_msg and "print" in error_msg:
            return True
        elif "unexpected indent" in error_msg or "unindent" in error_msg:
            return True
        elif "EOL while scanning string literal" in error_msg:
            return True

        return False

    def _attempt_fixes(self):
        """Attempt to automatically fix issues"""
        print("🔧 Attempting to fix auto-fixable issues...")

        for error in self.syntax_errors:
            if error.auto_fixable:
                try:
                    if self._fix_file(error):
                        self.fixed_files.append(error.file_path)
                        print(f"   ✅ Fixed: {error.file_path}")
                    else:
                        self.failed_files.append(error.file_path)
                        print(f"   ❌ Failed to fix: {error.file_path}")
                except Exception as e:
                    self.failed_files.append(error.file_path)
                    print(f"   ❌ Error fixing {error.file_path}: {e}")

    def _fix_file(self, error: SyntaxError) -> bool:
        """Attempt to fix a specific file"""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Apply fixes based on error type
            fixed_content = content

            # Fix print statements
            if (
                "Missing parentheses" in error.error_message
                and "print" in error.error_message
            ):
                fixed_content = self._fix_print_statements(fixed_content)

            # Fix indentation
            if (
                "unexpected indent" in error.error_message
                or "unindent" in error.error_message
            ):
                fixed_content = self._fix_indentation(fixed_content)

            # Fix string literals
            if "EOL while scanning string literal" in error.error_message:
                fixed_content = self._fix_string_literals(fixed_content)

            # Test if the fix worked
            try:
                ast.parse(fixed_content)
                # Fix worked, write back to file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                return True
            except SyntaxError:
                # Fix didn't work
                return False

        except Exception:
            return False

    def _fix_print_statements(self, content: str) -> str:
        """Fix Python 2 print statements"""
        # Simple regex to fix print statements
        # This is a basic implementation - more sophisticated parsing would be better
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Look for print statements without parentheses
            if re.match(r"^\s*print\s+[^(]", line):
                # Extract the print content
                match = re.match(r"^(\s*)print\s+(.+)$", line)
                if match:
                    indent = match.group(1)
                    print_content = match.group(2)
                    # Add parentheses
                    fixed_line = f"{indent}print({print_content})"
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _fix_indentation(self, content: str) -> str:
        """Fix indentation issues"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Convert tabs to spaces
            line = line.expandtabs(4)
            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _fix_string_literals(self, content: str) -> str:
        """Fix unterminated string literals"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Check for unterminated strings
            if line.count(""") % 2 == 1:
                # Odd number of quotes - likely unterminated
                if not line.strip().endswith("""):
                # Add closing quote
                line = line.rstrip() + "'"
            elif line.count("'") % 2 == 1:
                # Odd number of single quotes
                if not line.strip().endswith("'"):
                    line = line.rstrip() + "'"

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _generate_quality_report(self) -> Dict[str, Any]:
        """Generate code quality report"""
        total_files = len(list(self.root_dir.rglob("*.py")))
        error_count = len(self.syntax_errors)
        fixed_count = len(self.fixed_files)
        failed_count = len(self.failed_files)

        # Categorize errors by type
        error_types = defaultdict(int)
        for error in self.syntax_errors:
            error_types[error.error_type] += 1

        # Categorize by severity
        severity_counts = defaultdict(int)
        for error in self.syntax_errors:
            severity_counts[error.severity] += 1

        return {
            "total_files": total_files,
            "files_with_errors": error_count,
            "files_fixed": fixed_count,
            "files_failed": failed_count,
            "error_rate": (error_count / total_files * 100) if total_files > 0 else 0,
            "fix_success_rate": (fixed_count / error_count * 100)
            if error_count > 0
            else 0,
            "error_types": dict(error_types),
            "severity_distribution": dict(severity_counts),
            "most_common_errors": self._get_most_common_errors(),
        }

    def _get_most_common_errors(self) -> List[Tuple[str, int]]:
        """Get most common error types"""
        error_counts = defaultdict(int)
        for error in self.syntax_errors:
            error_counts[error.error_type] += 1

        return sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary"""
        return {
            "total_syntax_errors": len(self.syntax_errors),
            "auto_fixable_errors": sum(1 for e in self.syntax_errors if e.auto_fixable),
            "files_successfully_fixed": len(self.fixed_files),
            "files_failed_to_fix": len(self.failed_files),
            "overall_health_score": self._calculate_health_score(),
        }

    def _calculate_health_score(self) -> int:
        """Calculate overall code health score (0-100)"""
        total_files = len(list(self.root_dir.rglob("*.py")))
        error_count = len(self.syntax_errors)
        fixed_count = len(self.fixed_files)

        if total_files == 0:
            return 0

        # Base score
        base_score = 100

        # Deduct for errors
        error_penalty = (error_count / total_files) * 50

        # Bonus for successful fixes
        fix_bonus = (fixed_count / max(error_count, 1)) * 20

        score = base_score - error_penalty + fix_bonus
        return max(0, min(100, int(score)))

    def export_report(self, output_dir: str = "syntax_fix_report"):
        """Export analysis report"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"📁 Exporting syntax fix report to {output_dir}...")

        # Export syntax errors
        errors_data = []
        for error in self.syntax_errors:
            errors_data.append(
                {
                    "file_path": error.file_path,
                    "line_number": error.line_number,
                    "error_type": error.error_type,
                    "error_message": error.error_message,
                    "suggested_fix": error.suggested_fix,
                    "severity": error.severity,
                    "auto_fixable": error.auto_fixable,
                }
            )

        with open(output_path / "syntax_errors.json", "w") as f:
            json.dump(errors_data, f, indent=2)

        # Export quality report
        with open(output_path / "quality_report.json", "w") as f:
            json.dump(self._generate_quality_report(), f, indent=2)

        # Export summary
        with open(output_path / "summary.json", "w") as f:
            json.dump(self._generate_summary(), f, indent=2)

        # Export fixed files list
        with open(output_path / "fixed_files.txt", "w") as f:
            for file_path in self.fixed_files:
                f.write(f"{file_path}\n")

        # Export failed files list
        with open(output_path / "failed_files.txt", "w") as f:
            for file_path in self.failed_files:
                f.write(f"{file_path}\n")

        print(f"   ✅ Report exported to {output_dir}")


def main():
    """Main function for testing"""

    if len(sys.argv) != 2:
        print("Usage: python python_syntax_fixer.py <directory>")
        sys.exit(1)

    fixer = PythonSyntaxFixer(sys.argv[1])
    results = fixer.analyze_and_fix()

    print("\n🔧 Syntax Fix Results:")
    print(f"   📁 Total Files: {results['quality_report']['total_files']}")
    print(f"   ❌ Files with Errors: {results['quality_report']['files_with_errors']}")
    print(f"   ✅ Files Fixed: {results['quality_report']['files_fixed']}")
    print(f"   ❌ Files Failed: {results['quality_report']['files_failed']}")
    print(f"   📊 Error Rate: {results['quality_report']['error_rate']:.1f}%")
    print(
        f"   🎯 Fix Success Rate: {results['quality_report']['fix_success_rate']:.1f}%"
    )
    print(f"   🏆 Health Score: {results['summary']['overall_health_score']}/100")

    # Export report
    fixer.export_report("python_syntax_fix_report")


if __name__ == "__main__":
    main()
