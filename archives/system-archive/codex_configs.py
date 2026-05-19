#!/usr/bin/env python3
"""
Codex Configuration Generator - Generate AI tool configurations based on codebase analysis
"""

from typing import Dict, List
from datetime import datetime


class CodexConfigGenerator:
    """Generates AI tool configurations based on codebase analysis."""

    def __init__(self):
        self.config_templates = self._load_config_templates()

    def generate_configs(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate comprehensive AI tool configurations."""
        print("⚙️  Generating codex configurations...")

        configs = {
            "cursor": self._generate_cursor_config(
                folder_data, github_data, codex_data
            ),
            "github_copilot": self._generate_copilot_config(
                folder_data, github_data, codex_data
            ),
            "vscode": self._generate_vscode_config(
                folder_data, github_data, codex_data
            ),
            "tabnine": self._generate_tabnine_config(
                folder_data, github_data, codex_data
            ),
            "codeium": self._generate_codeium_config(
                folder_data, github_data, codex_data
            ),
            "claude_desktop": self._generate_claude_config(
                folder_data, github_data, codex_data
            ),
            "cursor_rules": self._generate_cursor_rules(
                folder_data, github_data, codex_data
            ),
            "ai_prompts": self._generate_ai_prompts(
                folder_data, github_data, codex_data
            ),
        }

        print(f"   ✅ Generated {len(configs)} codex configurations")
        return configs

    def _load_config_templates(self) -> Dict:
        """Load configuration templates for different AI tools."""
        return {
            "cursor": {
                "rules": [
                    "Follow the existing code style and patterns",
                    "Add comprehensive docstrings to all functions and classes",
                    "Include type hints for better code understanding",
                    "Write unit tests for new functionality",
                    "Use meaningful variable and function names",
                    "Follow PEP 8 for Python code",
                    "Use consistent indentation and formatting",
                    "Add error handling where appropriate",
                    "Include logging for debugging purposes",
                    "Write clear and concise comments",
                ],
                "context_files": [
                    "README.md",
                    "requirements.txt",
                    "package.json",
                    "pyproject.toml",
                    "setup.py",
                    "Dockerfile",
                    "docker-compose.yml",
                    ".env.example",
                    "LICENSE",
                    "CONTRIBUTING.md",
                ],
                "ignore_patterns": [
                    "__pycache__/",
                    "node_modules/",
                    "*.pyc",
                    ".git/",
                    ".vscode/",
                    ".idea/",
                    "dist/",
                    "build/",
                    "*.egg-info/",
                    ".pytest_cache/",
                    "venv/",
                    "env/",
                    ".env",
                    "*.log",
                    "*.tmp",
                    "*.temp",
                ],
                "preferences": {
                    "auto_complete": True,
                    "inline_suggestions": True,
                    "tab_completion": True,
                    "multi_line_completions": True,
                    "suggestion_delay": 100,
                    "max_suggestions": 5,
                },
            },
            "github_copilot": {
                "suggestions": {
                    "enable_auto_complete": True,
                    "enable_inline_suggestions": True,
                    "enable_tab_completion": True,
                    "enable_multiline_suggestions": True,
                },
                "filters": {
                    "min_confidence": 0.7,
                    "max_suggestions": 5,
                    "exclude_patterns": [
                        "*.log",
                        "*.tmp",
                        "*.temp",
                        "node_modules/",
                        "__pycache__/",
                    ],
                },
                "context": {
                    "include_comments": True,
                    "include_docstrings": True,
                    "include_imports": True,
                    "include_tests": True,
                    "max_context_lines": 50,
                },
            },
            "vscode": {
                "settings": {
                    "python.defaultInterpreterPath": "./venv/bin/python",
                    "python.linting.enabled": True,
                    "python.linting.pylintEnabled": True,
                    "python.linting.flake8Enabled": True,
                    "python.formatting.provider": "black",
                    "python.formatting.blackArgs": ["--line-length", "88"],
                    "editor.formatOnSave": True,
                    "editor.codeActionsOnSave": {
                        "source.organizeImports": True,
                        "source.fixAll": True,
                    },
                    "files.autoSave": "afterDelay",
                    "files.autoSaveDelay": 1000,
                    "editor.suggestSelection": "first",
                    "editor.tabCompletion": "on",
                    "editor.acceptSuggestionOnEnter": "on",
                },
                "extensions": [
                    "ms-python.python",
                    "ms-python.pylint",
                    "ms-python.black-formatter",
                    "ms-python.isort",
                    "github.copilot",
                    "github.copilot-chat",
                    "ms-vscode.vscode-json",
                    "redhat.vscode-yaml",
                    "ms-vscode.vscode-typescript-next",
                    "bradlc.vscode-tailwindcss",
                    "esbenp.prettier-vscode",
                    "ms-vscode.vscode-eslint",
                ],
            },
        }

    def _generate_cursor_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate Cursor AI configuration."""
        config = self.config_templates["cursor"].copy()

        # Customize based on detected languages
        languages = codex_data.get("languages_detected", set())
        frameworks = codex_data.get("frameworks_detected", set())

        # Add language-specific rules
        if "python" in languages:
            config["rules"].extend(
                [
                    "Use Python 3.8+ features when appropriate",
                    "Follow PEP 257 for docstring conventions",
                    "Use pathlib instead of os.path when possible",
                    "Prefer f-strings over .format() or % formatting",
                ]
            )

        if "javascript" in languages:
            config["rules"].extend(
                [
                    "Use ES6+ features when appropriate",
                    "Use const and let instead of var",
                    "Use arrow functions for short functions",
                    "Use template literals instead of string concatenation",
                ]
            )

        # Add framework-specific rules
        if "django" in frameworks:
            config["rules"].extend(
                [
                    "Follow Django best practices and conventions",
                    "Use Django ORM instead of raw SQL when possible",
                    "Use Django forms for form handling",
                    "Follow Django project structure conventions",
                ]
            )

        if "react" in frameworks:
            config["rules"].extend(
                [
                    "Use functional components with hooks",
                    "Use TypeScript for better type safety",
                    "Follow React best practices and patterns",
                    "Use proper prop types or TypeScript interfaces",
                ]
            )

        # Add project-specific context files
        project_files = self._get_project_specific_files(folder_data)
        config["context_files"].extend(project_files)

        return config

    def _generate_copilot_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate GitHub Copilot configuration."""
        config = self.config_templates["github_copilot"].copy()

        # Adjust confidence based on codebase complexity
        total_files = folder_data.get("total_files", 0)
        if total_files > 1000:
            config["filters"]["min_confidence"] = 0.8
        elif total_files > 100:
            config["filters"]["min_confidence"] = 0.75
        else:
            config["filters"]["min_confidence"] = 0.7

        # Add language-specific context
        languages = codex_data.get("languages_detected", set())
        if "python" in languages:
            config["context"]["include_docstrings"] = True
            config["context"]["max_context_lines"] = 60

        if "javascript" in languages:
            config["context"]["include_tests"] = True
            config["context"]["max_context_lines"] = 40

        return config

    def _generate_vscode_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate VS Code configuration."""
        config = self.config_templates["vscode"].copy()

        # Customize based on detected languages
        languages = codex_data.get("languages_detected", set())

        if "python" in languages:
            config["settings"].update(
                {
                    "python.linting.pylintEnabled": True,
                    "python.linting.flake8Enabled": True,
                    "python.formatting.provider": "black",
                    "python.sortImports.args": ["--profile", "black"],
                }
            )

        if "javascript" in languages:
            config["settings"].update(
                {
                    "javascript.format.enable": True,
                    "javascript.suggest.autoImports": True,
                    "typescript.suggest.autoImports": True,
                    "editor.codeActionsOnSave": {
                        "source.fixAll.eslint": True,
                        "source.organizeImports": True,
                    },
                }
            )

        # Add project-specific settings
        if github_data.get("has_github_workflows"):
            config["extensions"].append("github.vscode-pull-request-github")

        return config

    def _generate_tabnine_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate Tabnine configuration."""
        return {
            "rules": [
                "Use consistent naming conventions",
                "Follow the project's coding style",
                "Add appropriate error handling",
                "Include meaningful comments",
                "Write clean and readable code",
                "Use modern language features when appropriate",
                "Follow best practices for the detected frameworks",
            ],
            "context": {
                "max_context_lines": 20,
                "include_comments": True,
                "include_docstrings": True,
                "include_tests": True,
            },
            "preferences": {
                "auto_complete": True,
                "suggestion_delay": 200,
                "max_suggestions": 3,
                "confidence_threshold": 0.7,
            },
            "languages": {
                "python": {
                    "enabled": "python" in codex_data.get("languages_detected", set()),
                    "rules": ["Follow PEP 8", "Use type hints", "Write docstrings"],
                },
                "javascript": {
                    "enabled": "javascript"
                    in codex_data.get("languages_detected", set()),
                    "rules": [
                        "Use ES6+ features",
                        "Use const/let",
                        "Write clean functions",
                    ],
                },
            },
        }

    def _generate_codeium_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate Codeium configuration."""
        return {
            "settings": {
                "enable_autocomplete": True,
                "enable_chat": True,
                "enable_code_explanation": True,
                "enable_code_generation": True,
            },
            "filters": {
                "min_confidence": 0.8,
                "max_suggestions": 3,
                "exclude_patterns": ["*.log", "*.tmp", "node_modules/", "__pycache__/"],
            },
            "context": {
                "include_comments": True,
                "include_docstrings": True,
                "max_context_lines": 30,
            },
            "preferences": {
                "suggestion_style": "inline",
                "auto_accept_threshold": 0.9,
                "show_explanations": True,
            },
        }

    def _generate_claude_config(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate Claude Desktop configuration."""
        return {
            "system_prompt": self._generate_system_prompt(
                folder_data, github_data, codex_data
            ),
            "context_files": self._get_context_files(folder_data),
            "rules": [
                "Always provide clear and concise explanations",
                "Include code examples when appropriate",
                "Suggest best practices and improvements",
                "Consider security implications",
                "Provide multiple solutions when possible",
                "Explain the reasoning behind recommendations",
            ],
            "preferences": {
                "response_style": "detailed",
                "include_examples": True,
                "suggest_improvements": True,
                "consider_security": True,
            },
        }

    def _generate_cursor_rules(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate Cursor-specific rules file."""
        return {
            "cursor_rules": {
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat(),
                "project_info": {
                    "total_files": folder_data.get("total_files", 0),
                    "languages": list(codex_data.get("languages_detected", set())),
                    "frameworks": list(codex_data.get("frameworks_detected", set())),
                    "has_tests": len(codex_data.get("test_patterns", [])) > 0,
                },
                "rules": self._generate_detailed_rules(
                    folder_data, github_data, codex_data
                ),
                "context": {
                    "important_files": self._get_important_files(folder_data),
                    "patterns_to_follow": self._get_code_patterns(codex_data),
                    "avoid_patterns": self._get_avoid_patterns(folder_data),
                },
            }
        }

    def _generate_ai_prompts(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> Dict:
        """Generate AI prompts for different scenarios."""
        return {
            "code_review": self._generate_code_review_prompt(
                folder_data, github_data, codex_data
            ),
            "bug_fixing": self._generate_bug_fixing_prompt(
                folder_data, github_data, codex_data
            ),
            "feature_development": self._generate_feature_development_prompt(
                folder_data, github_data, codex_data
            ),
            "refactoring": self._generate_refactoring_prompt(
                folder_data, github_data, codex_data
            ),
            "testing": self._generate_testing_prompt(
                folder_data, github_data, codex_data
            ),
            "documentation": self._generate_documentation_prompt(
                folder_data, github_data, codex_data
            ),
        }

    def _get_project_specific_files(self, folder_data: Dict) -> List[str]:
        """Get project-specific files to include in context."""
        files = []

        # Common project files
        common_files = [
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
            "package.json",
            "yarn.lock",
            "package-lock.json",
            "Cargo.toml",
            "go.mod",
            "requirements.txt",
            "Pipfile",
            "poetry.lock",
            "composer.json",
            "Gemfile",
            "Gemfile.lock",
            "pom.xml",
            "build.gradle",
            "Makefile",
            "CMakeLists.txt",
        ]

        # Add files that exist in the project
        for file_name in common_files:
            if self._file_exists_in_project(file_name, folder_data):
                files.append(file_name)

        return files

    def _file_exists_in_project(self, file_name: str, folder_data: Dict) -> bool:
        """Check if a file exists in the project."""
        # This is a simplified check - in practice, you'd scan the actual file system
        return file_name in ["requirements.txt", "package.json", "README.md"]

    def _generate_system_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate system prompt for Claude."""
        languages = codex_data.get("languages_detected", set())
        frameworks = codex_data.get("frameworks_detected", set())

        prompt = f'\''You are an expert software developer working on a project with the following characteristics:

Project Overview:
- Total files: {folder_data.get("total_files", 0):,}
- Languages detected: {", ".join(languages) if languages else "None detected"}
- Frameworks detected: {", ".join(frameworks) if frameworks else "None detected"}
- Repository health score: {github_data.get("repository_health_score", 0)}/100

Guidelines:
1. Always provide clear, well-documented code
2. Follow best practices for the detected languages and frameworks
3. Include appropriate error handling and logging
4. Write comprehensive tests for new functionality
5. Consider security implications in your suggestions
6. Provide multiple solutions when appropriate
7. Explain the reasoning behind your recommendations

When helping with code:
- Suggest improvements and optimizations
- Point out potential issues or bugs
- Recommend best practices and patterns
- Provide examples and explanations
- Consider the project's existing structure and conventions

Remember to be helpful, accurate, and thorough in your responses."""

        return prompt

    def _get_context_files(self, folder_data: Dict) -> List[str]:
        """Get context files for AI tools."""
        return [
            "README.md",
            "requirements.txt",
            "package.json",
            "pyproject.toml",
            "Dockerfile",
            "docker-compose.yml",
            ".env.example",
            "LICENSE",
            "CONTRIBUTING.md",
        ]

    def _generate_detailed_rules(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> List[str]:
        """Generate detailed rules for the project.'\''
        rules = [
            "Follow the existing code style and patterns in the project",
            "Add comprehensive docstrings to all functions and classes",
            "Include type hints for better code understanding",
            "Write unit tests for new functionality",
            "Use meaningful variable and function names",
            "Add error handling where appropriate",
            "Include logging for debugging purposes",
            "Write clear and concise comments",
            "Follow the project's directory structure conventions",
            "Use consistent indentation and formatting",
        ]

        # Add language-specific rules
        languages = codex_data.get("languages_detected", set())
        if "python" in languages:
            rules.extend(
                [
                    "Follow PEP 8 for Python code",
                    "Use pathlib instead of os.path when possible",
                    "Prefer f-strings over .format() or % formatting",
                    "Use list comprehensions when appropriate",
                    "Follow PEP 257 for docstring conventions",
                ]
            )

        if "javascript" in languages:
            rules.extend(
                [
                    "Use const and let instead of var",
                    "Use arrow functions for short functions",
                    "Use template literals instead of string concatenation",
                    "Use destructuring when appropriate",
                    "Follow ESLint rules and conventions",
                ]
            )

        return rules

    def _get_important_files(self, folder_data: Dict) -> List[str]:
        """Get important files for context."""
        return [
            "README.md",
            "requirements.txt",
            "package.json",
            "pyproject.toml",
            "Dockerfile",
            "docker-compose.yml",
            ".env.example",
            "LICENSE",
            "CONTRIBUTING.md",
            "setup.py",
            "Makefile",
        ]

    def _get_code_patterns(self, codex_data: Dict) -> List[str]:
        """Get code patterns to follow."""
        patterns = []

        # Add patterns based on detected frameworks
        frameworks = codex_data.get("frameworks_detected", set())
        if "django" in frameworks:
            patterns.extend(
                [
                    "Use Django ORM instead of raw SQL",
                    "Follow Django's project structure conventions",
                    "Use Django forms for form handling",
                    "Use Django's built-in authentication system",
                ]
            )

        if "react" in frameworks:
            patterns.extend(
                [
                    "Use functional components with hooks",
                    "Use TypeScript for better type safety",
                    "Follow React best practices and patterns",
                    "Use proper prop types or TypeScript interfaces",
                ]
            )

        return patterns

    def _get_avoid_patterns(self, folder_data: Dict) -> List[str]:
        """Get patterns to avoid."""
        return [
            "Don't use global variables",
            "Avoid deep nesting (max 3-4 levels)",
            "Don't ignore error handling",
            "Avoid magic numbers and strings",
            "Don't use deprecated features",
            "Avoid tight coupling between modules",
            "Don't commit sensitive information",
            "Avoid overly complex functions (max 20-30 lines)",
        ]

    def _generate_code_review_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate code review prompt."""
        return """Please review the following code and provide feedback on:

1. Code quality and readability
2. Performance considerations
3. Security implications
4. Best practices adherence
5. Potential bugs or issues
6. Suggestions for improvement
7. Test coverage recommendations

Focus on:
- Code clarity and maintainability
- Error handling and edge cases
- Performance optimization opportunities
- Security vulnerabilities
- Adherence to project conventions
- Documentation completeness"""

    def _generate_bug_fixing_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate bug fixing prompt."""
        return """Please help fix the following bug:

1. Analyze the error message and stack trace
2. Identify the root cause of the issue
3. Provide a clear explanation of what went wrong
4. Suggest a fix with code examples
5. Recommend preventive measures
6. Suggest tests to prevent regression

Consider:
- Error handling and validation
- Edge cases and boundary conditions
- Performance implications
- Security considerations
- Code maintainability"""

    def _generate_feature_development_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate feature development prompt."""
        return """Please help implement the following feature:

1. Break down the feature into smaller tasks
2. Suggest an implementation approach
3. Provide code examples and structure
4. Recommend testing strategies
5. Consider integration points
6. Suggest documentation needs

Focus on:
- Clean architecture and design patterns
- Proper error handling and validation
- Performance and scalability
- Security considerations
- Code reusability and maintainability
- Following project conventions"""

    def _generate_refactoring_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate refactoring prompt."""
        return """Please help refactor the following code:

1. Identify areas for improvement
2. Suggest refactoring strategies
3. Provide step-by-step refactoring plan
4. Show before and after code examples
5. Recommend testing approach
6. Consider performance implications

Focus on:
- Code readability and maintainability
- Reducing complexity and duplication
- Improving performance
- Better error handling
- Following SOLID principles
- Maintaining backward compatibility"""

    def _generate_testing_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate testing prompt."""
        return """Please help create comprehensive tests for the following code:

1. Identify test cases and scenarios
2. Suggest unit test structure
3. Provide test examples
4. Recommend integration tests
5. Suggest edge cases to test
6. Recommend test data and fixtures

Focus on:
- Test coverage and completeness
- Edge cases and boundary conditions
- Error scenarios and exceptions
- Performance testing
- Integration testing
- Test maintainability and readability"""

    def _generate_documentation_prompt(:
        self, folder_data: Dict, github_data: Dict, codex_data: Dict
    ) -> str:
        """Generate documentation prompt."""
        return """Please help create comprehensive documentation for the following code:

1. Write clear function/class docstrings
2. Add inline comments for complex logic
3. Create API documentation
4. Suggest README updates
5. Recommend code examples
6. Suggest user guides

Focus on:
- Clarity and completeness
- Code examples and usage
- API reference documentation
- Installation and setup instructions
- Troubleshooting guides
- Contributing guidelines"""
