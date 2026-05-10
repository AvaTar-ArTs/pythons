#!/usr/bin/env python3
"""
Python Codebase Organizer and Describer
Comprehensive analysis and organization system for Python codebases
"""

import ast
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict
import sys


@dataclass
class PythonFile:
    """Represents a Python file with metadata"""

    path: str
    name: str
    size: int
    lines: int
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    has_docstring: bool = False
    is_syntax_valid: bool = True
    error_message: Optional[str] = None
    category: str = "unknown"
    priority: int = 0  # 0=low, 1=medium, 2=high, 3=critical


@dataclass
class CodePattern:
    """Represents a code pattern or functionality"""

    name: str
    pattern_type: str  # 'youtube', 'ai', 'data', 'web', 'utility'
    files: List[str] = field(default_factory=list)
    description: str = ""
    complexity: int = 0
    dependencies: Set[str] = field(default_factory=set)


class PythonCodebaseOrganizer:
    """Advanced Python codebase organizer and analyzer"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.python_files: List[PythonFile] = []
        self.patterns: List[CodePattern] = []
        self.categories: Dict[str, List[str]] = defaultdict(list)
        self.duplicates: Dict[str, List[str]] = defaultdict(list)
        self.analysis_results: Dict[str, Any] = {}

        # Pattern detection rules
        self.pattern_rules = {
            "youtube": {
                "keywords": [
                    "youtube",
                    "yt_",
                    "video",
                    "download",
                    "playlist",
                    "channel",
                ],
                "imports": ["youtube_dl", "pytube", "googleapiclient"],
                "functions": ["download", "extract", "get_video", "playlist"],
            },
            "ai": {
                "keywords": [
                    "whisper",
                    "openai",
                    "dalle",
                    "gpt",
                    "ai_",
                    "transcribe",
                    "tts",
                ],
                "imports": ["openai", "whisper", "transformers", "torch"],
                "functions": ["transcribe", "generate", "analyze", "process"],
            },
            "data": {
                "keywords": ["csv", "data", "process", "analyze", "pandas", "numpy"],
                "imports": ["pandas", "numpy", "csv", "json"],
                "functions": ["process", "analyze", "convert", "export"],
            },
            "web": {
                "keywords": [
                    "scrape",
                    "requests",
                    "beautifulsoup",
                    "selenium",
                    "instagram",
                ],
                "imports": ["requests", "beautifulsoup4", "selenium", "urllib"],
                "functions": ["scrape", "get", "post", "parse"],
            },
            "utility": {
                "keywords": ["util", "helper", "common", "base", "config"],
                "imports": ["os", "sys", "pathlib", "json"],
                "functions": ["helper", "util", "config", "base"],
            },
        }

    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of the Python codebase"""
        print("🔍 Analyzing Python codebase...")

        # Find all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"   Found {len(python_files)} Python files")

        # Analyze each file
        for file_path in python_files:
            try:
                file_info = self._analyze_file(file_path)
                self.python_files.append(file_info)
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")

        # Detect patterns
        self._detect_patterns()

        # Categorize files
        self._categorize_files()

        # Find duplicates
        self._find_duplicates()

        # Generate organization suggestions
        suggestions = self._generate_organization_suggestions()

        # Calculate metrics
        metrics = self._calculate_metrics()

        self.analysis_results = {
            "files": self.python_files,
            "patterns": self.patterns,
            "categories": dict(self.categories),
            "duplicates": dict(self.duplicates),
            "suggestions": suggestions,
            "metrics": metrics,
            "summary": self._generate_summary(),
        }

        return self.analysis_results

    def _analyze_file(self, file_path: Path) -> PythonFile:
        """Analyze a single Python file"""
        file_info = PythonFile(
            path=str(file_path),
            name=file_path.name,
            size=file_path.stat().st_size,
            lines=0,
        )

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            file_info.lines = len(content.splitlines())

            # Try to parse the file
            try:
                tree = ast.parse(content)
                file_info.is_syntax_valid = True

                # Extract functions and classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        file_info.functions.append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        file_info.classes.append(node.name)
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        import_name = self._extract_import_name(node)
                        if import_name:
                            file_info.imports.append(import_name)

                # Check for docstring
                if (
                    tree.body
                    and isinstance(tree.body[0], ast.Expr)
                    and isinstance(tree.body[0].value, ast.Constant)
                    and isinstance(tree.body[0].value.value, str)
                ):
                    file_info.has_docstring = True

            except SyntaxError as e:
                file_info.is_syntax_valid = False
                file_info.error_message = str(e)
                file_info.priority = 3  # Critical - syntax error

        except UnicodeDecodeError:
            file_info.is_syntax_valid = False
            file_info.error_message = "Invalid UTF-8 encoding"
            file_info.priority = 3  # Critical - encoding error

        except Exception as e:
            file_info.is_syntax_valid = False
            file_info.error_message = str(e)
            file_info.priority = 2  # High - other error

        return file_info

    def _extract_import_name(self, node: ast.Import) -> Optional[str]:
        """Extract import name from import node"""
        if isinstance(node, ast.Import):
            return node.names[0].name if node.names else None
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                return node.module
            elif node.names:
                return node.names[0].name
        return None

    def _detect_patterns(self):
        """Detect code patterns and functionality"""
        print("   🔍 Detecting code patterns...")

        for pattern_name, rules in self.pattern_rules.items():
            pattern = CodePattern(
                name=pattern_name,
                pattern_type=pattern_name,
                description=f"Files related to {pattern_name} functionality",
            )

            for file_info in self.python_files:
                if not file_info.is_syntax_valid:
                    continue

                # Check keywords in filename
                filename_lower = file_info.name.lower()
                if any(keyword in filename_lower for keyword in rules["keywords"]):
                    pattern.files.append(file_info.path)
                    pattern.complexity += 1
                    continue

                # Check imports
                if any(imp in file_info.imports for imp in rules["imports"]):
                    pattern.files.append(file_info.path)
                    pattern.complexity += 1
                    continue

                # Check function names
                if any(func in file_info.functions for func in rules["functions"]):
                    pattern.files.append(file_info.path)
                    pattern.complexity += 1
                    continue

            if pattern.files:
                self.patterns.append(pattern)

    def _categorize_files(self):
        """Categorize files based on patterns and functionality"""
        print("   📂 Categorizing files...")

        for file_info in self.python_files:
            if not file_info.is_syntax_valid:
                self.categories["syntax_errors"].append(file_info.path)
                continue

            # Determine category based on patterns
            category = "utility"  # default

            for pattern in self.patterns:
                if file_info.path in pattern.files:
                    category = pattern.name
                    break

            # Additional categorization based on filename patterns
            filename_lower = file_info.name.lower()
            if "test" in filename_lower:
                category = "testing"
            elif "config" in filename_lower or "settings" in filename_lower:
                category = "configuration"
            elif "main" in filename_lower or "__main__" in filename_lower:
                category = "main"
            elif "init" in filename_lower:
                category = "package"

            self.categories[category].append(file_info.path)
            file_info.category = category

    def _find_duplicates(self):
        """Find duplicate or similar files"""
        print("   🔍 Finding duplicates...")

        # Group files by size and function count
        size_groups = defaultdict(list)
        for file_info in self.python_files:
            if file_info.is_syntax_valid:
                size_groups[file_info.size].append(file_info)

        # Find potential duplicates
        for size, files in size_groups.items():
            if len(files) > 1:
                # Check for similar function names
                for i, file1 in enumerate(files):
                    for file2 in files[i + 1 :]:
                        if self._are_files_similar(file1, file2):
                            self.duplicates[key] = [file1.path, file2.path]

    def _are_files_similar(self, file1: PythonFile, file2: PythonFile) -> bool:
        """Check if two files are similar"""
        # Check function overlap
        func_overlap = len(set(file1.functions) & set(file2.functions))
        total_functions = len(set(file1.functions) | set(file2.functions))

        if total_functions > 0:
            similarity = func_overlap / total_functions
            return similarity > 0.5  # 50% function overlap

        return False

    def _generate_organization_suggestions(self) -> List[Dict[str, Any]]:
        """Generate suggestions for code organization"""
        suggestions = []

        # Suggest package structure
        if len(self.patterns) > 1:
            suggestions.append(
                {
                    "type": "package_structure",
                    "title": "Create package structure",
                    "description": f"Organize {len(self.patterns)} detected patterns into packages",
                    "details": {
                        "patterns": [p.name for p in self.patterns],
                        "suggested_structure": self._suggest_package_structure(),
                    },
                }
            )

        # Suggest duplicate cleanup
        if self.duplicates:
            suggestions.append(
                {
                    "type": "duplicate_cleanup",
                    "title": "Remove duplicate files",
                    "description": f"Found {len(self.duplicates)} duplicate file groups",
                    "details": {
                        "duplicates": dict(self.duplicates),
                        "suggested_action": "Review and consolidate duplicate files",
                    },
                }
            )

        # Suggest syntax error fixes
        syntax_errors = [f for f in self.python_files if not f.is_syntax_valid]
        if syntax_errors:
            suggestions.append(
                {
                    "type": "syntax_fixes",
                    "title": "Fix syntax errors",
                    "description": f"Found {len(syntax_errors)} files with syntax errors",
                    "details": {
                        "error_files": [f.path for f in syntax_errors],
                        "suggested_action": "Fix syntax errors or remove broken files",
                    },
                }
            )

        return suggestions

    def _suggest_package_structure(self) -> Dict[str, List[str]]:
        """Suggest package structure based on patterns"""
        structure = {}

        for pattern in self.patterns:
            if pattern.files:
                structure[pattern.name] = pattern.files[:5]  # Show first 5 files

        return structure

    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate codebase metrics"""
        total_files = len(self.python_files)
        valid_files = sum(1 for f in self.python_files if f.is_syntax_valid)
        files_with_docs = sum(1 for f in self.python_files if f.has_docstring)

        total_lines = sum(f.lines for f in self.python_files)
        total_functions = sum(len(f.functions) for f in self.python_files)
        total_classes = sum(len(f.classes) for f in self.python_files)

        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "syntax_error_rate": ((total_files - valid_files) / total_files * 100)
            if total_files > 0
            else 0,
            "documentation_rate": (files_with_docs / valid_files * 100)
            if valid_files > 0
            else 0,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_functions_per_file": total_functions / valid_files
            if valid_files > 0
            else 0,
            "average_classes_per_file": total_classes / valid_files
            if valid_files > 0
            else 0,
            "patterns_detected": len(self.patterns),
            "duplicate_groups": len(self.duplicates),
        }

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary"""
        return {
            "total_files_analyzed": len(self.python_files),
            "patterns_found": len(self.patterns),
            "categories_created": len(self.categories),
            "duplicates_found": len(self.duplicates),
            "syntax_errors": sum(1 for f in self.python_files if not f.is_syntax_valid),
            "health_score": self._calculate_health_score(),
        }

    def _calculate_health_score(self) -> int:
        """Calculate overall codebase health score (0-100)"""
        total_files = len(self.python_files)
        if total_files == 0:
            return 0

        valid_files = sum(1 for f in self.python_files if f.is_syntax_valid)
        files_with_docs = sum(1 for f in self.python_files if f.has_docstring)

        # Base score
        base_score = 100

        # Deduct for syntax errors
        syntax_penalty = ((total_files - valid_files) / total_files) * 30

        # Deduct for lack of documentation
        doc_penalty = 0
        if valid_files > 0:
            doc_penalty = ((valid_files - files_with_docs) / valid_files) * 20

        # Bonus for good organization
        org_bonus = min(20, len(self.patterns) * 2)

        score = base_score - syntax_penalty - doc_penalty + org_bonus
        return max(0, min(100, int(score)))

    def export_analysis(self, output_dir: str = "python_analysis"):
        """Export analysis results"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"📁 Exporting analysis to {output_dir}...")

        # Export detailed analysis
        with open(output_path / "analysis_results.json", "w") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        # Export file list by category
        for category, files in self.categories.items():
            with open(output_path / f"{category}_files.txt", "w") as f:
                for file_path in files:
                    f.write(f"{file_path}\n")

        # Export pattern analysis
        with open(output_path / "patterns.json", "w") as f:
            patterns_data = []
            for pattern in self.patterns:
                patterns_data.append(
                    {
                        "name": pattern.name,
                        "type": pattern.pattern_type,
                        "file_count": len(pattern.files),
                        "complexity": pattern.complexity,
                        "description": pattern.description,
                        "files": pattern.files[:10],  # First 10 files
                    }
                )
            json.dump(patterns_data, f, indent=2)

        # Export duplicate analysis
        with open(output_path / "duplicates.json", "w") as f:
            json.dump(dict(self.duplicates), f, indent=2)

        # Export suggestions
        with open(output_path / "suggestions.json", "w") as f:
            json.dump(self.analysis_results["suggestions"], f, indent=2)

        print(f"   ✅ Analysis exported to {output_dir}")

    def create_organized_structure(self, output_dir: str = "organized_python"):
        """Create an organized version of the codebase"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"📁 Creating organized structure at {output_dir}...")

        # Create package structure
        for pattern in self.patterns:
            pattern_dir = output_path / pattern.name
            pattern_dir.mkdir(exist_ok=True)

            # Create __init__.py
            init_file = pattern_dir / "__init__.py"
            with open(init_file, "w") as f:
                f.write(f'\"\'"\n{pattern.description}\n'\''\n')

            # Copy files
            for file_path in pattern.files[:20]:  # Limit to first 20 files
                try:
                    src = Path(file_path)
                    dst = pattern_dir / src.name
                    shutil.copy2(src, dst)
                except Exception as e:
                    print(f"   ⚠️  Error copying {file_path}: {e}")

        # Create utility package
        util_dir = output_path / "utils"
        util_dir.mkdir(exist_ok=True)

        util_files = self.categories.get("utility", [])
        for file_path in util_files[:20]:  # Limit to first 20 files
            try:
                src = Path(file_path)
                dst = util_dir / src.name
                shutil.copy2(src, dst)
            except Exception as e:
                print(f"   ⚠️  Error copying {file_path}: {e}")

        # Create README
        readme_content = self._generate_readme()
        with open(output_path / "README.md", "w") as f:
            f.write(readme_content)

        print(f"   ✅ Organized structure created at {output_dir}")

    def _generate_readme(self) -> str:
        """Generate README for organized structure"""
        readme = "# Python Codebase Organization\n\n"
        readme += (
            "This directory contains an organized version of the Python codebase.\n\n"
        )

        readme += "## Structure\n\n"
        for pattern in self.patterns:
            readme += f"### {pattern.name.title()}\n"
            readme += f"{pattern.description}\n"
            readme += f"Files: {len(pattern.files)}\n\n"

        readme += "## Metrics\n\n"
        metrics = self.analysis_results["metrics"]
        readme += f"- Total Files: {metrics['total_files']}\n"
        readme += f"- Valid Files: {metrics['valid_files']}\n"
        readme += f"- Syntax Error Rate: {metrics['syntax_error_rate']:.1f}%\n"
        readme += f"- Documentation Rate: {metrics['documentation_rate']:.1f}%\n"
        readme += f"- Total Lines: {metrics['total_lines']:,}\n"
        readme += f"- Total Functions: {metrics['total_functions']:,}\n"
        readme += f"- Total Classes: {metrics['total_classes']:,}\n"

        return readme


def main():
    """Main function for testing"""

    if len(sys.argv) != 2:
        print("Usage: python python_codebase_organizer.py <directory>")
        sys.exit(1)

    organizer = PythonCodebaseOrganizer(sys.argv[1])
    results = organizer.analyze_codebase()

    print("\n📊 Analysis Results:")
    print(f"   📁 Total Files: {results['summary']['total_files_analyzed']}")
    print(f"   🎯 Patterns Found: {results['summary']['patterns_found']}")
    print(f"   📂 Categories: {results['summary']['categories_created']}")
    print(f"   🔄 Duplicates: {results['summary']['duplicates_found']}")
    print(f"   ❌ Syntax Errors: {results['summary']['syntax_errors']}")
    print(f"   🏆 Health Score: {results['summary']['health_score']}/100")

    # Export analysis
    organizer.export_analysis("python_codebase_analysis")

    # Create organized structure
    organizer.create_organized_structure("organized_python_codebase")


if __name__ == "__main__":
    main()
