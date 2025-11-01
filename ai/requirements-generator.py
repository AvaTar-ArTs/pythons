"""
Requirements Txt Generator

This module provides functionality for requirements txt generator.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Intelligent Requirements Generator
Analyzes Python files to extract and generate requirements.txt files.
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List
import json

# Standard library modules (don't include in requirements)
STDLIB_MODULES = {
    "abc",
    "argparse",
    "asyncio",
    "base64",
    "collections",
    "csv",
    "datetime",
    "functools",
    "hashlib",
    "io",
    "itertools",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "pickle",
    "random",
    "re",
    "shutil",
    "socket",
    "sqlite3",
    "subprocess",
    "sys",
    "tempfile",
    "threading",
    "time",
    "typing",
    "unittest",
    "urllib",
    "uuid",
    "warnings",
    "xml",
    "zipfile",
    "gzip",
    "tarfile",
    "copy",
    "enum",
    "dataclasses",
    "configparser",
    "queue",
    "string",
    "traceback",
    "multiprocessing",
    "concurrent",
    "email",
    "http",
    "html",
    "glob",
    "fnmatch",
}

# Known package mappings (import name -> package name)
PACKAGE_MAPPINGS = {
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "dateutil": "python-dateutil",
    "bs4": "beautifulsoup4",
    "selenium": "selenium",
    "requests": "requests",
    "numpy": "numpy",
    "pandas": "pandas",
    "flask": "Flask",
    "django": "Django",
    "fastapi": "fastapi",
    "torch": "torch",
    "tensorflow": "tensorflow",
    "keras": "keras",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "scipy": "scipy",
    "plotly": "plotly",
    "dash": "dash",
    "streamlit": "streamlit",
    "openai": "openai",
    "anthropic": "anthropic",
    "google": "google-api-python-client",
    "instabot": "instabot",
    "pytube": "pytube",
    "yt_dlp": "yt-dlp",
    "moviepy": "moviepy",
    "pydub": "pydub",
    "whisper": "openai-whisper",
    "transformers": "transformers",
    "diffusers": "diffusers",
    "langchain": "langchain",
    "chromadb": "chromadb",
    "pinecone": "pinecone-client",
    "redis": "redis",
    "pymongo": "pymongo",
    "sqlalchemy": "SQLAlchemy",
    "pytest": "pytest",
    "black": "black",
    "flake8": "flake8",
    "mypy": "mypy",
    "pylint": "pylint",
}


def extract_imports_from_file(file_path: Path) -> Set[str]:
    """Extract imported modules from a Python file."""
    imports = set()

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            try:
                tree = ast.parse(f.read(), filename=str(file_path))
            except SyntaxError:
                return imports

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split(".")[0]
                    imports.add(module_name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split(".")[0]
                    imports.add(module_name)
    except Exception:
        pass

    return imports


def analyze_directory(directory: Path) -> Dict[str, Set[str]]:
    """Analyze all Python files in a directory and extract imports."""
    all_imports = defaultdict(set)

    py_files = list(directory.rglob("*.py"))

    logger.info(f"📁 Analyzing {len(py_files)} Python files in {directory.name}/")

    for py_file in py_files:
        imports = extract_imports_from_file(py_file)
        for imp in imports:
            all_imports[imp].add(str(py_file.relative_to(directory)))

    return dict(all_imports)


def filter_third_party_packages(imports: Dict[str, Set[str]]) -> List[str]:
    """Filter to only third-party packages."""
    packages = []

    for module in sorted(imports.keys()):
        # Skip standard library
        if module in STDLIB_MODULES:
            continue

        # Skip local imports (single character or starts with underscore)
        if len(module) == 1 or module.startswith("_"):
            continue

        # Get package name (use mapping if available)
        package = PACKAGE_MAPPINGS.get(module, module)

        if package not in packages:
            packages.append(package)

    return sorted(packages)


def generate_requirements_file(packages: List[str], output_path: Path, category_name: str = None):
    """Generate requirements.txt file."""

    header = f"""# Requirements for {category_name or 'Python Projects'}
# Generated automatically by generate_requirements.py

"""

    content = header + "\n".join(packages) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    logger.info(f"✅ Created {output_path} with {len(packages)} packages")


def analyze_category_directories():
    """Analyze category directories and generate requirements."""

    base_dir = Path(".")

    # Find category directories
    category_dirs = [
        d
        for d in base_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and not d.name.startswith("_")
        and d.name not in ["docs", "functional_analysis", "organized_by_function"]
    ]

    logger.info(f"\n🔍 Found {len(category_dirs)} potential category directories\n")

    global_packages = set()
    category_requirements = {}

    for category_dir in category_dirs:
        py_files = list(category_dir.rglob("*.py"))

        if len(py_files) < 3:  # Skip directories with very few Python files
            continue

        logger.info(f"📦 Analyzing: {category_dir.name}")
        imports = analyze_directory(category_dir)
        packages = filter_third_party_packages(imports)

        if packages:
            category_requirements[category_dir.name] = packages
            global_packages.update(packages)

            # Generate category-specific requirements
            req_file = category_dir / "requirements.txt"
            generate_requirements_file(packages, req_file, category_dir.name)

    # Generate global requirements
    if global_packages:
        logger.info(f"\n📦 Generating global requirements.txt")
        generate_requirements_file(sorted(global_packages), base_dir / "requirements.txt", "All Projects")

    # Save analysis report
    report = {
        "total_categories": len(category_requirements),
        "total_packages": len(global_packages),
        "categories": {
            name: {"packages": packages, "count": len(packages)} for name, packages in category_requirements.items()
        },
    }

    report_path = base_dir / "requirements_analysis.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    logger.info(f"\n📊 Analysis report saved to: {report_path}")

    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 REQUIREMENTS ANALYSIS SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Categories analyzed: {len(category_requirements)}")
    logger.info(f"Unique packages found: {len(global_packages)}")
    logger.info(f"\n🏆 TOP PACKAGES:")

    # Count package frequency across categories
    package_freq = defaultdict(int)
    for packages in category_requirements.values():
        for pkg in packages:
            package_freq[pkg] += 1

    for i, (pkg, count) in enumerate(sorted(package_freq.items(), key=lambda x: x[1], reverse=True)[:15], 1):
        logger.info(f"   {i:2d}. {pkg:30} - used in {count} categories")


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate requirements.txt files by analyzing imports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all category directories
  python3 generate_requirements.py

  # Analyze specific directory
  python3 generate_requirements.py --dir my_project
        """,
    )

    parser.add_argument("--dir", type=str, help="Specific directory to analyze (default: all categories)")

    args = parser.parse_args()

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.exists():
            logger.info(f"❌ Directory not found: {args.dir}")
            return 1

        logger.info(f"📁 Analyzing: {dir_path}")
        imports = analyze_directory(dir_path)
        packages = filter_third_party_packages(imports)

        req_file = dir_path / "requirements.txt"
        generate_requirements_file(packages, req_file, dir_path.name)
    else:
        analyze_category_directories()

    return 0


if __name__ == "__main__":
    exit(main())
