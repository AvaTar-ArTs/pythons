"""
Software

This module provides functionality for software.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_400 = 400
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
Context-Efficient Software Architect Agent
Specialized expert for system design and architecture analysis.
"""

import sys
from pathlib import Path
from typing import Dict, List, Set
import ast
import json
from collections import defaultdict


class SoftwareArchitectAgent:
    """
    Lightweight agent specialized in software architecture analysis.
    Focuses on: design patterns, dependencies, modularity, scalability.
    """

    def __init__(self):
        """__init__ function."""

        self.design_patterns = {
            "singleton": ["__new__", "__instance"],
            "factory": ["create", "make", "build"],
            "observer": ["subscribe", "notify", "observer"],
            "decorator": ["@", "wrapper"],
            "strategy": ["strategy", "algorithm"],
        }

    def analyze_project(self, project_path: Path) -> Dict:
        """Analyze project architecture."""
        if not project_path.is_dir():
            project_path = project_path.parent

        python_files = list(project_path.rglob("*.py"))

        analysis = {
            "overview": self._get_project_overview(python_files),
            "structure": self._analyze_structure(python_files, project_path),
            "dependencies": self._analyze_dependencies(python_files),
            "patterns": self._detect_patterns(python_files),
            "recommendations": [],
        }

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)

        return analysis

    def _get_project_overview(self, files: List[Path]) -> Dict:
        """Get high-level project overview."""
        total_lines = 0
        total_functions = 0
        total_classes = 0

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.split("\n")
                total_lines += len([l for l in lines if l.strip()])

                tree = ast.parse(content)
                total_functions += len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                )
                total_classes += len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                )
            except (IndexError, KeyError):
                pass

        return {
            "total_files": len(files),
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "avg_lines_per_file": total_lines // len(files) if files else 0,
        }

    def _analyze_structure(self, files: List[Path], base_path: Path) -> Dict:
        """Analyze project structure and organization."""
        structure = {"depth": 0, "modules": defaultdict(list), "organization_score": 0}

        for file_path in files:
            rel_path = file_path.relative_to(base_path)
            depth = len(rel_path.parts) - 1
            structure["depth"] = max(structure["depth"], depth)

            if depth > 0:
                module = rel_path.parts[0]
                structure["modules"][module].append(str(rel_path))

        # Calculate organization score (0-CONSTANT_100)
        # Better organized projects have:
        # - Reasonable depth (2-4 levels)
        # - Similar-sized modules
        # - Clear separation of concerns

        score = CONSTANT_100
        if structure["depth"] > 5:
            score -= 20  # Too deep
        elif structure["depth"] < 2:
            score -= 10  # Too flat

        if len(structure["modules"]) > 20:
            score -= 15  # Too many top-level modules

        structure["organization_score"] = max(0, score)
        structure["modules"] = dict(structure["modules"])

        return structure

    def _analyze_dependencies(self, files: List[Path]) -> Dict:
        """Analyze import dependencies."""
        dependencies = {
            "internal": defaultdict(set),
            "external": set(),
            "circular": [],
            "coupling_score": 0,
        }

        file_imports = {}

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content)

                imports = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module.split(".")[0])

                file_imports[file_path.stem] = imports

                # Categorize imports
                stdlib_modules = {
                    "os",
                    "sys",
                    "json",
                    "re",
                    "pathlib",
                    "typing",
                    "collections",
                    "datetime",
                }
                for imp in imports:
                    if imp not in stdlib_modules:
                        dependencies["external"].add(imp)

            except (json.JSONDecodeError, ValueError):
                pass

        # Detect potential circular dependencies
        for file1, imports1 in file_imports.items():
            for file2, imports2 in file_imports.items():
                if file1 != file2:
                    if file2 in imports1 and file1 in imports2:
                        circular = tuple(sorted([file1, file2]))
                        if circular not in dependencies["circular"]:
                            dependencies["circular"].append(circular)

        # Calculate coupling score (lower is better)
        total_imports = sum(len(imports) for imports in file_imports.values())
        avg_imports = total_imports / len(file_imports) if file_imports else 0
        dependencies["coupling_score"] = min(CONSTANT_100, int(avg_imports * 10))

        dependencies["external"] = sorted(dependencies["external"])
        dependencies["internal"] = {
            k: list(v) for k, v in dependencies["internal"].items()
        }

        return dependencies

    def _detect_patterns(self, files: List[Path]) -> Dict:
        """Detect design patterns in use."""
        detected = defaultdict(list)

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Check for pattern indicators
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]

                        for pattern, indicators in self.design_patterns.items():
                            if any(
                                ind in " ".join(methods).lower() for ind in indicators
                            ):
                                detected[pattern].append(
                                    {
                                        "file": file_path.name,
                                        "class": node.name,
                                        "line": node.lineno,
                                    }
                                )

            except (OSError, IOError, FileNotFoundError):
                pass

        return dict(detected)

    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate architecture recommendations."""
        recommendations = []

        # Structure recommendations
        structure = analysis["structure"]
        if structure["depth"] > 5:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "structure",
                    "title": "Directory Structure Too Deep",
                    "description": f'Project has {structure["depth"]} levels of nesting. Consider flattening to improve navigability.',
                    "suggestion": "Group related modules and reduce nesting to 3-4 levels maximum.",
                }
            )

        if structure["organization_score"] < 70:
            recommendations.append(
                {
                    "priority": "low",
                    "category": "organization",
                    "title": "Improve Project Organization",
                    "description": f'Organization score: {structure["organization_score"]}/100',
                    "suggestion": "Consider reorganizing modules by feature or domain rather than by file type.",
                }
            )

        # Dependency recommendations
        dependencies = analysis["dependencies"]
        if dependencies["coupling_score"] > 50:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "coupling",
                    "title": "High Module Coupling",
                    "description": f'Coupling score: {dependencies["coupling_score"]}/CONSTANT_100. Modules are tightly coupled.',
                    "suggestion": "Apply dependency inversion and interface segregation principles to reduce coupling.",
                }
            )

        if dependencies["circular"]:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "dependencies",
                    "title": "Circular Dependencies Detected",
                    "description": f'Found {len(dependencies["circular"])} circular dependency pairs.',
                    "suggestion": "Refactor to break circular dependencies using interfaces or reorganization.",
                }
            )

        # Scale recommendations
        overview = analysis["overview"]
        if overview["avg_lines_per_file"] > CONSTANT_500:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "maintainability",
                    "title": "Large File Sizes",
                    "description": f'Average file size: {overview["avg_lines_per_file"]} lines',
                    "suggestion": "Break down large files into smaller, focused modules (target: CONSTANT_200-CONSTANT_400 lines).",
                }
            )

        # Pattern recommendations
        patterns = analysis["patterns"]
        if not patterns:
            recommendations.append(
                {
                    "priority": "low",
                    "category": "design",
                    "title": "Limited Design Pattern Usage",
                    "description": "No clear design patterns detected.",
                    "suggestion": "Consider applying design patterns like Factory, Strategy, or Observer where appropriate.",
                }
            )

        return recommendations

    def format_analysis(self, analysis: Dict) -> str:
        """Format analysis as readable report."""
        output = []

        output.append(Path("\n") + "=" * 80)
        output.append("🏛️  SOFTWARE ARCHITECTURE ANALYSIS")
        output.append("=" * 80 + Path("\n"))

        # Overview
        overview = analysis["overview"]
        output.append("📊 PROJECT OVERVIEW")
        output.append(f"  • Files: {overview['total_files']}")
        output.append(f"  • Total Lines: {overview['total_lines']:,}")
        output.append(f"  • Functions: {overview['total_functions']}")
        output.append(f"  • Classes: {overview['total_classes']}")
        output.append(f"  • Avg Lines/File: {overview['avg_lines_per_file']}")
        output.append("")

        # Structure
        structure = analysis["structure"]
        output.append("🏗️  PROJECT STRUCTURE")
        output.append(f"  • Max Depth: {structure['depth']} levels")
        output.append(f"  • Top-level Modules: {len(structure['modules'])}")
        output.append(f"  • Organization Score: {structure['organization_score']}/100")
        output.append("")

        # Dependencies
        dependencies = analysis["dependencies"]
        output.append("📦 DEPENDENCIES")
        output.append(f"  • External Packages: {len(dependencies['external'])}")
        if dependencies["external"][:5]:
            output.append(f"    - {', '.join(dependencies['external'][:5])}")
        output.append(
            f"  • Coupling Score: {dependencies['coupling_score']}/CONSTANT_100 {'⚠️' if dependencies['coupling_score'] > 50 else '✅'}"
        )
        if dependencies["circular"]:
            output.append(
                f"  • Circular Dependencies: {len(dependencies['circular'])} ⚠️"
            )
        output.append("")

        # Patterns
        patterns = analysis["patterns"]
        if patterns:
            output.append("🎨 DESIGN PATTERNS DETECTED")
            for pattern, occurrences in patterns.items():
                output.append(f"  • {pattern.title()}: {len(occurrences)} instance(s)")
            output.append("")

        # Recommendations
        recommendations = analysis["recommendations"]
        if recommendations:
            output.append("💡 RECOMMENDATIONS\n")
            priority_order = {"high": 0, "medium": 1, "low": 2}
            sorted_recs = sorted(
                recommendations, key=lambda x: priority_order.get(x["priority"], 3)
            )

            for i, rec in enumerate(sorted_recs, 1):
                emoji = {"high": "🔴", "medium": "🟡", "low": "🔵"}.get(
                    rec["priority"], "⚪"
                )
                output.append(
                    f"{i}. {emoji} {rec['title']} [{rec['priority'].upper()}]"
                )
                output.append(f"   Category: {rec['category']}")
                output.append(f"   {rec['description']}")
                output.append(f"   → {rec['suggestion']}")
                output.append("")

        return "\n".join(output)


def main():
    """Main entry point for software architect agent."""
    if len(sys.argv) < 2:
        logger.info("Usage: python software_architect.py <project_directory>")
        logger.info("\nContext-Efficient Software Architect Agent")
        logger.info("Analyzes project architecture for:")
        logger.info("  • Project structure and organization")
        logger.info("  • Module dependencies and coupling")
        logger.info("  • Design pattern usage")
        logger.info("  • Scalability and maintainability")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.exists():
        logger.info(f"❌ Path not found: {project_path}")
        sys.exit(1)

    agent = SoftwareArchitectAgent()
    analysis = agent.analyze_project(project_path)

    logger.info(agent.format_analysis(analysis))

    # Optionally save to JSON
    if "--json" in sys.argv:
        output_file = project_path / "architecture_analysis.json"
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        logger.info(f"\n📄 Full analysis saved to: {output_file}")


if __name__ == "__main__":
    main()
