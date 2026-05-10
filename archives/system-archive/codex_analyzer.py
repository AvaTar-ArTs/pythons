#!/usr/bin/env python3
"""
Codex Analyzer - Analyzes codebase for AI codex configuration generation
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CodexPattern:
    """Represents a codex pattern for AI tools."""

    pattern_type: str  # 'function', 'class', 'module', 'api', 'config'
    name: str
    description: str
    file_path: str
    line_number: int
    parameters: List[str]
    return_type: Optional[str]
    complexity: int  # 1-10 scale
    ai_relevance: int  # 1-10 scale


class CodexAnalyzer:
    """Analyzes codebase for AI codex configuration generation."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.codex_patterns: List[CodexPattern] = []
        self.language_configs = {}

    def analyze(self) -> Dict:
        """Analyze codebase for codex configuration."""
        print("🤖 Analyzing codebase for codex configuration...")

        structure = {
            "languages_detected": set(),
            "frameworks_detected": set(),
            "patterns_found": [],
            "api_endpoints": [],
            "configuration_files": [],
            "test_patterns": [],
            "documentation_patterns": [],
            "codex_recommendations": {},
            "ai_tool_configs": {},
            "complexity_analysis": {},
            "code_quality_metrics": {},
        }

        # Analyze different file types
        self._analyze_python_files(structure)
        self._analyze_javascript_files(structure)
        self._analyze_config_files(structure)
        self._analyze_documentation_files(structure)

        # Generate codex recommendations
        self._generate_codex_recommendations(structure)

        # Generate AI tool configurations
        self._generate_ai_tool_configs(structure)

        print(
            f"   ✅ Codex analysis complete: {len(self.codex_patterns)} patterns found"
        )

        return structure

    def _analyze_python_files(self, structure: Dict):
        """Analyze Python files for codex patterns."""
        python_files = list(self.root_dir.rglob("*.py"))
        structure["languages_detected"].add("python")

        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                # Detect frameworks
                if "django" in content.lower():
                    structure["frameworks_detected"].add("django")
                if "flask" in content.lower():
                    structure["frameworks_detected"].add("flask")
                if "fastapi" in content.lower():
                    structure["frameworks_detected"].add("fastapi")
                if "pytest" in content.lower():
                    structure["frameworks_detected"].add("pytest")

                # Analyze functions and classes
                self._analyze_python_functions(file_path, lines, structure)
                self._analyze_python_classes(file_path, lines, structure)
                self._analyze_python_imports(file_path, lines, structure)

            except Exception:
                continue

    def _analyze_python_functions(:
        self, file_path: Path, lines: List[str], structure: Dict
    ):
        """Analyze Python functions for codex patterns."""
        for i, line in enumerate(lines):
            line = line.strip()

            # Function definitions
            if line.startswith("def ") and "(" in line:
                func_name = line.split("def ")[1].split("(")[0].strip()
                params = self._extract_function_params(line)
                return_type = self._extract_return_type(line)

                # Calculate complexity
                complexity = self._calculate_function_complexity(lines, i)

                # Calculate AI relevance
                ai_relevance = self._calculate_ai_relevance(
                    func_name, params, file_path
                )

                pattern = CodexPattern(
                    pattern_type="function",
                    name=func_name,
                    description=f"Function in {file_path.name}",
                    file_path=str(file_path),
                    line_number=i + 1,
                    parameters=params,
                    return_type=return_type,
                    complexity=complexity,
                    ai_relevance=ai_relevance,
                )

                self.codex_patterns.append(pattern)
                structure["patterns_found"].append(pattern)

    def _analyze_python_classes(:
        self, file_path: Path, lines: List[str], structure: Dict
    ):
        """Analyze Python classes for codex patterns."""
        for i, line in enumerate(lines):
            line = line.strip()

            # Class definitions
            if line.startswith("class ") and "(" in line:
                class_name = line.split("class ")[1].split("(")[0].strip()

                # Find methods in the class
                methods = self._find_class_methods(lines, i)

                pattern = CodexPattern(
                    pattern_type="class",
                    name=class_name,
                    description=f"Class in {file_path.name} with {len(methods)} methods",
                    file_path=str(file_path),
                    line_number=i + 1,
                    parameters=methods,
                    return_type=None,
                    complexity=self._calculate_class_complexity(lines, i),
                    ai_relevance=self._calculate_ai_relevance(
                        class_name, methods, file_path
                    ),
                )

                self.codex_patterns.append(pattern)
                structure["patterns_found"].append(pattern)

    def _analyze_python_imports(:
        self, file_path: Path, lines: List[str], structure: Dict
    ):
        """Analyze Python imports for dependencies."""
        imports = []
        for line in lines:
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                imports.append(line)

        if imports:
            pattern = CodexPattern(
                pattern_type="module",
                name=f"imports_{file_path.stem}",
                description=f"Import statements in {file_path.name}",
                file_path=str(file_path),
                line_number=1,
                parameters=imports,
                return_type=None,
                complexity=1,
                ai_relevance=5,
            )

            self.codex_patterns.append(pattern)

    def _analyze_javascript_files(self, structure: Dict):
        """Analyze JavaScript/TypeScript files for codex patterns."""
        js_files = list(self.root_dir.rglob("*.js")) + list(self.root_dir.rglob("*.ts"))
        structure["languages_detected"].add("javascript")

        for file_path in js_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                # Detect frameworks
                if "react" in content.lower():
                    structure["frameworks_detected"].add("react")
                if "vue" in content.lower():
                    structure["frameworks_detected"].add("vue")
                if "angular" in content.lower():
                    structure["frameworks_detected"].add("angular")
                if "express" in content.lower():
                    structure["frameworks_detected"].add("express")
                if "next" in content.lower():
                    structure["frameworks_detected"].add("nextjs")

                # Analyze functions and classes
                self._analyze_js_functions(file_path, lines, structure)
                self._analyze_js_classes(file_path, lines, structure)

            except Exception:
                continue

    def _analyze_js_functions(self, file_path: Path, lines: List[str], structure: Dict):
        """Analyze JavaScript functions for codex patterns."""
        for i, line in enumerate(lines):
            line = line.strip()

            # Function definitions
            if ("function " in line and "(" in line) or ("=>" in line):
                if "function " in line:
                    func_name = line.split("function ")[1].split("(")[0].strip()
                else:
                    func_name = f"arrow_function_{i}"

                params = self._extract_js_function_params(line)

                pattern = CodexPattern(
                    pattern_type="function",
                    name=func_name,
                    description=f"JavaScript function in {file_path.name}",
                    file_path=str(file_path),
                    line_number=i + 1,
                    parameters=params,
                    return_type=None,
                    complexity=self._calculate_js_complexity(lines, i),
                    ai_relevance=self._calculate_ai_relevance(
                        func_name, params, file_path
                    ),
                )

                self.codex_patterns.append(pattern)
                structure["patterns_found"].append(pattern)

    def _analyze_js_classes(self, file_path: Path, lines: List[str], structure: Dict):
        """Analyze JavaScript classes for codex patterns."""
        for i, line in enumerate(lines):
            line = line.strip()

            # Class definitions
            if line.startswith("class ") and "{" in line:
                class_name = line.split("class ")[1].split("{")[0].strip()

                pattern = CodexPattern(
                    pattern_type="class",
                    name=class_name,
                    description=f"JavaScript class in {file_path.name}",
                    file_path=str(file_path),
                    line_number=i + 1,
                    parameters=[],
                    return_type=None,
                    complexity=self._calculate_js_complexity(lines, i),
                    ai_relevance=self._calculate_ai_relevance(
                        class_name, [], file_path
                    ),
                )

                self.codex_patterns.append(pattern)
                structure["patterns_found"].append(pattern)

    def _analyze_config_files(self, structure: Dict):
        """Analyze configuration files for codex patterns."""
        config_files = []
        for ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".env"]:
            config_files.extend(self.root_dir.rglob(f"*{ext}"))

        for file_path in config_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse configuration
                config_data = self._parse_config_file(file_path, content)

                pattern = CodexPattern(
                    pattern_type="config",
                    name=file_path.name,
                    description=f"Configuration file: {file_path.name}",
                    file_path=str(file_path),
                    line_number=1,
                    parameters=list(config_data.keys())
                    if isinstance(config_data, dict)
                    else [],
                    return_type=None,
                    complexity=3,
                    ai_relevance=8,  # Config files are important for AI
                )

                self.codex_patterns.append(pattern)
                structure["configuration_files"].append(pattern)

            except Exception:
                continue

    def _analyze_documentation_files(self, structure: Dict):
        """Analyze documentation files for codex patterns."""
        doc_files = list(self.root_dir.rglob("*.md")) + list(
            self.root_dir.rglob("*.rst")
        )

        for file_path in doc_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract documentation patterns
                doc_patterns = self._extract_doc_patterns(content)

                if doc_patterns:
                    pattern = CodexPattern(
                        pattern_type="documentation",
                        name=file_path.name,
                        description=f"Documentation: {file_path.name}",
                        file_path=str(file_path),
                        line_number=1,
                        parameters=doc_patterns,
                        return_type=None,
                        complexity=2,
                        ai_relevance=7,
                    )

                    self.codex_patterns.append(pattern)
                    structure["documentation_patterns"].append(pattern)

            except Exception:
                continue

    def _extract_function_params(self, line: str) -> List[str]:
        """Extract function parameters from a function definition line."""
        if "(" not in line or ")" not in line:
            return []

        params_str = line.split("(")[1].split(")")[0].strip()
        if not params_str:
            return []

        # Simple parameter extraction
        params = [p.strip() for p in params_str.split(",")]
        return [p for p in params if p]

    def _extract_return_type(self, line: str) -> Optional[str]:
        """Extract return type annotation from function definition."""
        if "->" in line:
            return line.split("->")[1].strip().rstrip(":")
        return None

    def _extract_js_function_params(self, line: str) -> List[str]:
        """Extract parameters from JavaScript function definition."""
        if "(" not in line or ")" not in line:
            return []

        params_str = line.split("(")[1].split(")")[0].strip()
        if not params_str:
            return []

        params = [p.strip() for p in params_str.split(",")]
        return [p for p in params if p]

    def _calculate_function_complexity(self, lines: List[str], start_line: int) -> int:
        """Calculate complexity score for a function."""
        complexity = 1
        end_line = start_line

        # Find function end
        for i in range(start_line + 1, len(lines)):
            line = lines[i].strip()
            if line and not line.startswith(" ") and not line.startswith("\t"):
                end_line = i
                break

        # Count complexity indicators
        for i in range(start_line, end_line):
            line = lines[i].strip()
            if any(
                keyword in line
                for keyword in [
                    "if",
                    "elif",
                    "else",
                    "for",
                    "while",
                    "try",
                    "except",
                    "with",
                ]
            ):
                complexity += 1
            if "and" in line or "or" in line:
                complexity += 1

        return min(10, complexity)

    def _calculate_class_complexity(self, lines: List[str], start_line: int) -> int:
        """Calculate complexity score for a class."""
        complexity = 1
        method_count = 0

        # Count methods and their complexity
        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            if line.startswith("def ") and "(" in line:
                method_count += 1
                complexity += self._calculate_function_complexity(lines, i)

        return min(10, complexity)

    def _calculate_js_complexity(self, lines: List[str], start_line: int) -> int:
        """Calculate complexity score for JavaScript code."""
        complexity = 1

        # Count complexity indicators
        for i in range(start_line, min(start_line + 20, len(lines))):
            line = lines[i].strip()
            if any(
                keyword in line
                for keyword in [
                    "if",
                    "else",
                    "for",
                    "while",
                    "switch",
                    "case",
                    "try",
                    "catch",
                ]
            ):
                complexity += 1
            if "&&" in line or "||" in line:
                complexity += 1

        return min(10, complexity)

    def _calculate_ai_relevance(:
        self, name: str, params: List[str], file_path: Path
    ) -> int:
        """Calculate AI relevance score for a code pattern."""
        relevance = 5  # Base score

        # High relevance for common patterns
        if any(
            keyword in name.lower()
            for keyword in ["api", "endpoint", "handler", "service", "util", "helper"]
        ):
            relevance += 3

        # High relevance for configuration
        if file_path.suffix in [".json", ".yaml", ".yml", ".toml", ".ini"]:
            relevance += 2

        # High relevance for main files
        if file_path.name in ["main.py", "app.py", "index.js", "main.js"]:
            relevance += 2

        # High relevance for test files
        if "test" in file_path.name.lower():
            relevance += 1

        return min(10, relevance)

    def _find_class_methods(self, lines: List[str], class_start: int) -> List[str]:
        """Find methods in a Python class."""
        methods = []
        indent_level = None

        for i in range(class_start + 1, len(lines)):
            line = lines[i]
            if not line.strip():
                continue

            # Determine indentation level
            if indent_level is None and line.strip().startswith("def "):
                indent_level = len(line) - len(line.lstrip())

            # Check if we're still in the class
            if indent_level is not None and line.strip():
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and not line.strip().startswith(
                    "def "
                ):
                    break

            # Extract method names
            if line.strip().startswith("def "):
                method_name = line.strip().split("def ")[1].split("(")[0].strip()
                methods.append(method_name)

        return methods

    def _parse_config_file(self, file_path: Path, content: str) -> Dict:
        """Parse configuration file content."""
        try:
            if file_path.suffix == ".json":
                return json.loads(content)
            elif file_path.suffix in [".yaml", ".yml"]:
                import yaml

                return yaml.safe_load(content)
            elif file_path.suffix == ".toml":
                import toml

                return toml.loads(content)
            else:
                # Simple key-value parsing for other formats
                config = {}
                for line in content.split("\n"):
                    if "=" in line and not line.strip().startswith("#"):
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
                return config
        except Exception:
            return {}

    def _extract_doc_patterns(self, content: str) -> List[str]:
        """Extract documentation patterns from content."""
        patterns = []

        # Extract code blocks
        if "```" in content:
            patterns.append("code_blocks")

        # Extract API documentation
        if any(
            keyword in content.lower()
            for keyword in ["api", "endpoint", "route", "method"]
        ):
            patterns.append("api_documentation")

        # Extract configuration examples
        if any(
            keyword in content.lower() for keyword in ["config", "setting", "parameter"]
        ):
            patterns.append("configuration_docs")

        return patterns

    def _generate_codex_recommendations(self, structure: Dict):
        """Generate codex configuration recommendations."""
        recommendations = {
            "cursor_config": self._generate_cursor_config(),
            "github_copilot_config": self._generate_copilot_config(),
            "vscode_config": self._generate_vscode_config(),
            "ai_tool_suggestions": self._suggest_ai_tools(structure),
        }

        structure["codex_recommendations"] = recommendations

    def _generate_cursor_config(self) -> Dict:
        """Generate Cursor AI configuration."""
        return {
            "rules": [
                "Follow the existing code style and patterns",
                "Add comprehensive docstrings to all functions and classes",
                "Include type hints for better code understanding",
                "Write unit tests for new functionality",
                "Use meaningful variable and function names",
            ],
            "context_files": ["README.md", "requirements.txt", "package.json"],
            "ignore_patterns": ["__pycache__/", "node_modules/", "*.pyc", ".git/"],
        }

    def _generate_copilot_config(self) -> Dict:
        """Generate GitHub Copilot configuration."""
        return {
            "suggestions": {
                "enable_auto_complete": True,
                "enable_inline_suggestions": True,
                "enable_tab_completion": True,
            },
            "filters": {"min_confidence": 0.7, "max_suggestions": 5},
            "context": {
                "include_comments": True,
                "include_docstrings": True,
                "include_imports": True,
            },
        }

    def _generate_vscode_config(self) -> Dict:
        """Generate VS Code configuration."""
        return {
            "settings": {
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {"source.organizeImports": True},
            },
            "extensions": [
                "ms-python.python",
                "ms-python.pylint",
                "ms-python.black-formatter",
                "github.copilot",
                "ms-vscode.vscode-json",
            ],
        }

    def _suggest_ai_tools(self, structure: Dict) -> List[Dict]:
        """Suggest AI tools based on codebase analysis."""
        suggestions = []

        if "python" in structure["languages_detected"]:
            suggestions.append(
                {
                    "tool": "Cursor",
                    "reason": "Python codebase detected",
                    "config": "cursor_config",
                }
            )

        if "javascript" in structure["languages_detected"]:
            suggestions.append(
                {
                    "tool": "GitHub Copilot",
                    "reason": "JavaScript/TypeScript codebase detected",
                    "config": "copilot_config",
                }
            )

        if structure["frameworks_detected"]:
            suggestions.append(
                {
                    "tool": "Tabnine",
                    "reason": f"Framework detected: {', '.join(structure['frameworks_detected'])}",
                    "config": "tabnine_config",
                }
            )

        return suggestions

    def _generate_ai_tool_configs(self, structure: Dict):
        """Generate configurations for various AI tools."""
        configs = {
            "cursor": self._generate_cursor_config(),
            "copilot": self._generate_copilot_config(),
            "vscode": self._generate_vscode_config(),
            "tabnine": self._generate_tabnine_config(),
            "codeium": self._generate_codeium_config(),
        }

        structure["ai_tool_configs"] = configs

    def _generate_tabnine_config(self) -> Dict:
        """Generate Tabnine configuration."""
        return {
            "rules": [
                "Use consistent naming conventions",
                "Follow the project's coding style",
                "Add appropriate error handling",
                "Include meaningful comments",
            ],
            "context": {"max_context_lines": 20, "include_comments": True},
        }

    def _generate_codeium_config(self) -> Dict:
        """Generate Codeium configuration."""
        return {
            "settings": {
                "enable_autocomplete": True,
                "enable_chat": True,
                "enable_code_explanation": True,
            },
            "filters": {"min_confidence": 0.8, "max_suggestions": 3},
        }
