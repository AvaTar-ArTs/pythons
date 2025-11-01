"""
Apply Improvements

This module provides functionality for apply improvements.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2025 = 2025

#!/usr/bin/env python3
"""
GitHub Repository Improvement Script
Applies common improvements to GitHub repositories
"""

import os
import shutil
from pathlib import Path
import argparse


def apply_improvements(repo_path: str, template_dir: str = "."):
    """Apply improvements to a repository."""
    repo_path = Path(repo_path)
    template_dir = Path(template_dir)

    logger.info(f"🔧 Applying improvements to {repo_path.name}")

    # Add README if missing
    if not (repo_path / "README.md").exists():
        if (template_dir / "README_template.md").exists():
            shutil.copy2(template_dir / "README_template.md", repo_path / "README.md")
            logger.info("✅ Added README.md")

    # Add .gitignore if missing
    if not (repo_path / ".gitignore").exists():
        # Determine project type and add appropriate .gitignore
        if (repo_path / "package.json").exists():
            gitignore_template = template_dir / "nodejs.gitignore"
        elif any((repo_path / "requirements.txt").exists(), (repo_path / "pyproject.toml").exists()):
            gitignore_template = template_dir / "python.gitignore"
        else:
            gitignore_template = template_dir / "python.gitignore"  # Default

        if gitignore_template.exists():
            shutil.copy2(gitignore_template, repo_path / ".gitignore")
            logger.info("✅ Added .gitignore")

    # Add LICENSE if missing
    if not (repo_path / "LICENSE").exists():
        license_content = """MIT License

Copyright (c) CONSTANT_2025 Steven

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open(repo_path / "LICENSE", "w") as f:
            f.write(license_content)
        logger.info("✅ Added LICENSE")

    # Add GitHub Actions if missing
    github_dir = repo_path / ".github" / "workflows"
    if not github_dir.exists():
        github_dir.mkdir(parents=True)

        # Add appropriate workflow based on project type
        if (repo_path / "package.json").exists():
            # Node.js workflow
            workflow_content = """name: Node.js CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]

    steps:
    - uses: actions/checkout@v4
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test
"""
        else:
            # Python workflow
            workflow_content = """name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test
      run: |
        python -m pytest
"""

        with open(github_dir / "ci.yml", "w") as f:
            f.write(workflow_content)
        logger.info("✅ Added GitHub Actions workflow")


def main():
    """main function."""

    parser = argparse.ArgumentParser(description="Apply improvements to GitHub repositories")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--template-dir", default=".", help="Directory containing templates")

    args = parser.parse_args()
    apply_improvements(args.repo_path, args.template_dir)


if __name__ == "__main__":
    main()
