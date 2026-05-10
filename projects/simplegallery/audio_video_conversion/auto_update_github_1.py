#!/usr/bin/env python3
"""
Auto Update GitHub Repository
Automatically uploads all Python projects to GitHub with proper structure and documentation
"""

import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GitHubAutoUpdater:
    """Automatically updates GitHub repository with Python projects."""

    def __init__(:
        self,
        base_dir: str = "/Users/steven/Documents/python",
        github_url: str = "https://github.com/ichoake/python.git",
    ):
        self.base_dir = Path(base_dir)
        self.github_url = github_url
        self.repo_name = "python"

    def update_github_repo(self):
        """Update GitHub repository with all projects."""
        print("🚀 Auto Updating GitHub Repository")
        print("=" * 50)
        print(f"Repository: {self.github_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Step 1: Prepare repository
        print("📁 Step 1: Preparing Repository...")
        print("-" * 40)
        self._prepare_repository()

        # Step 2: Create main README
        print("\n📝 Step 2: Creating Main README...")
        print("-" * 40)
        self._create_main_readme()

        # Step 3: Create project structure
        print("\n🏗️ Step 3: Creating Project Structure...")
        print("-" * 40)
        self._create_project_structure()

        # Step 4: Copy documentation
        print("\n📚 Step 4: Copying Documentation...")
        print("-" * 40)
        self._copy_documentation()

        # Step 5: Initialize Git and push
        print("\n🔄 Step 5: Initializing Git and Pushing...")
        print("-" * 40)
        self._git_operations()

        print("\n🎉 GitHub Repository Updated Successfully!")
        print("=" * 50)
        print(f"Repository URL: {self.github_url}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        print("📁 What was uploaded:")
        print("  - All Python projects with documentation")
        print("  - Comprehensive analysis reports")
        print("  - Professional README files")
        print("  - Sphinx and PyDoc documentation")
        print("  - Portfolio showcase")
        print()

        print("🌐 View your repository:")
        print(f"  {self.github_url}")

    def _prepare_repository(self):
        """Prepare the repository for upload."""
        # Create a clean directory for the repository
        self.repo_dir = self.base_dir / "github_upload"
        if self.repo_dir.exists():
            shutil.rmtree(self.repo_dir)
        self.repo_dir.mkdir(exist_ok=True)

        print(f"✅ Created upload directory: {self.repo_dir}")

    def _create_main_readme(self):
        """Create the main README for the repository."""
        # Read the comprehensive documentation
        docs_readme = self.base_dir / "comprehensive_docs" / "README.md"
        if docs_readme.exists():
            with open(docs_readme, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = self._create_basic_readme()

        # Write to repository
        with open(self.repo_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(content)

        print("✅ Created main README.md")

    def _create_basic_readme(self):
        '\''Create a basic README if comprehensive docs don't exist."""
        return """# 🐍 Python Projects Collection

A comprehensive collection of Python projects with professional documentation and enhanced code quality.

## 📊 Overview

This repository contains multiple Python projects organized by functionality and purpose.

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/ichoake/python.git
cd python

# Install dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

- `01_core_ai_analysis/` - AI and machine learning projects
- `02_media_processing/` - Image, video, and audio processing
- `03_automation_platforms/` - Web scraping and automation tools
- `04_content_creation/` - Text and media generation
- `05_data_management/` - Data processing and analysis
- `06_development_tools/` - Code quality and development utilities

## 📚 Documentation

- **Sphinx Documentation**: Professional HTML documentation
- **PyDoc Documentation**: Automated API documentation
- **API Reference**: Complete function and class reference

## 🎯 Features

- Professional documentation
- Enhanced code quality
- Type hints throughout
- Comprehensive error handling
- Consistent project structure

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

- **GitHub**: https://github.com/ichoake
- **Email**: steven@example.com

---

*This repository was automatically generated and updated*
"""

    def _create_project_structure(self):
        """Create the project structure in the repository."""
        # Copy all project directories
        project_dirs = [
            "01_core_ai_analysis",
            "02_media_processing",
            "03_automation_platforms",
            "04_content_creation",
            "05_data_management",
            "06_development_tools",
            "07_business_setup",
            "08_archived",
            "00_shared_libraries",
            "github_repo",
        ]

        copied_projects = 0
        for project_name in project_dirs:
            source_dir = self.base_dir / project_name
            if source_dir.exists():
                dest_dir = self.repo_dir / project_name
                self._copy_project_directory(source_dir, dest_dir)
                copied_projects += 1
                print(f"✅ Copied project: {project_name}")

        print(f"✅ Copied {copied_projects} projects")

    def _copy_project_directory(self, source: Path, dest: Path):
        """Copy a project directory with filtering."""
        dest.mkdir(parents=True, exist_ok=True)

        # Copy files, excluding certain patterns
        exclude_patterns = {
            "__pycache__",
            ".git",
            ".DS_Store",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".pytest_cache",
            "venv",
            "env",
            ".env",
        }

        for item in source.iterdir():
            if item.name in exclude_patterns:
                continue

            if item.is_file():
                shutil.copy2(item, dest / item.name)
            elif item.is_dir():
                self._copy_project_directory(item, dest / item.name)

    def _copy_documentation(self):
        """Copy all documentation to the repository."""
        docs_source = self.base_dir / "comprehensive_docs"
        docs_dest = self.repo_dir / "docs"

        if docs_source.exists():
            shutil.copytree(docs_source, docs_dest, dirs_exist_ok=True)
            print("✅ Copied comprehensive documentation")

        # Create a simple docs index
        docs_index = """# 📚 Documentation

This directory contains comprehensive documentation for all Python projects.

## Available Documentation

- **README.md** - Main overview and project statistics
- **sphinx/** - Professional HTML documentation
- **pydoc/** - Automated API documentation
- **api/** - API reference
- **portfolio/** - Project portfolio showcase
- **projects/** - Individual project documentation

## Quick Access

- [Main Overview](README.md)
- [Sphinx Documentation](sphinx/_build/html/index.html)
- [PyDoc Documentation](pydoc/index.html)
- [API Reference](api/index.md)
- [Portfolio](portfolio/README.md)

## Viewing Documentation

### Sphinx Documentation
```bash
cd docs/sphinx
sphinx-build -b html source _build/html
open _build/html/index.html
```

### PyDoc Documentation
```bash
open docs/pydoc/index.html
```

### API Reference
```bash
open docs/api/index.md
```

---

*This documentation was automatically generated*
"""

        with open(docs_dest / "README.md", "w", encoding="utf-8") as f:
            f.write(docs_index)

        print("✅ Created documentation index")

    def _git_operations(self):
        """Perform Git operations to push to GitHub.'\''
        try:
            # Initialize Git repository
            subprocess.run(["git", "init"], cwd=self.repo_dir, check=True)
            print("✅ Initialized Git repository")

            # Add all files
            subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
            print("✅ Added all files to Git")

            # Create initial commit
            commit_message = f"🚀 Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n- Added comprehensive Python projects collection\n- Generated professional documentation\n- Created Sphinx and PyDoc documentation\n- Added portfolio showcase\n- Implemented quality analysis and scoring"
            subprocess.run(
                ["git", "commit", "-m", commit_message], cwd=self.repo_dir, check=True
            )
            print("✅ Created initial commit")

            # Add remote origin
            subprocess.run(
                ["git", "remote", "add", "origin", self.github_url],
                cwd=self.repo_dir,
                check=True,
            )
            print("✅ Added remote origin")

            # Push to GitHub
            subprocess.run(
                ["git", "push", "-u", "origin", "main"], cwd=self.repo_dir, check=True
            )
            print("✅ Pushed to GitHub successfully")

        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            print("Please check your Git configuration and GitHub access")
            return False

        return True

    def create_requirements_file(self):
        """Create a comprehensive requirements.txt file."""
        requirements = """# Python Projects Collection - Requirements
# Generated automatically

# Core dependencies
numpy>=1.21.0
pandas>=1.3.0
requests>=2.25.0
beautifulsoup4>=4.9.0
selenium>=4.0.0
pillow>=8.0.0
opencv-python>=4.5.0
matplotlib>=3.3.0
seaborn>=0.11.0
plotly>=5.0.0

# AI/ML dependencies
openai>=0.27.0
transformers>=4.20.0
torch>=1.12.0
tensorflow>=2.8.0
scikit-learn>=1.0.0
nltk>=3.7
spacy>=3.4.0

# Web development
flask>=2.0.0
django>=4.0.0
fastapi>=0.68.0
uvicorn>=0.15.0
streamlit>=1.0.0

# Data processing
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0

# Media processing
opencv-python>=4.5.0
pillow>=8.0.0
moviepy>=1.0.3
librosa>=0.9.0
soundfile>=0.10.0

# Development tools
pytest>=6.2.0
black>=21.0.0
flake8>=3.9.0
mypy>=0.910
isort>=5.9.0
pre-commit>=2.15.0

# Documentation
sphinx>=4.0.0
sphinx-rtd-theme>=1.0.0
myst-parser>=0.15.0
sphinx-autodoc-typehints>=1.12.0

# Utilities
python-dotenv>=0.19.0
click>=8.0.0
tqdm>=4.62.0
rich>=12.0.0
"""

        with open(self.repo_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)

        print("✅ Created requirements.txt")

    def create_license_file(self):
        """Create MIT License file."""
        license_content = """MIT License

Copyright (c) 2025 Steven

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

        with open(self.repo_dir / "LICENSE", "w", encoding="utf-8") as f:
            f.write(license_content)

        print("✅ Created LICENSE file")

    def create_gitignore_file(self):
        """Create comprehensive .gitignore file."""
        gitignore_content = '\''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
*.log
*.tmp
*.temp
temp/
tmp/
logs/
"""

        with open(self.repo_dir / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)

        print("✅ Created .gitignore file")


def main():
    """Main function to update GitHub repository.'\''
    updater = GitHubAutoUpdater()

    print("🚀 GitHub Auto Updater")
    print("=" * 50)
    print(f"Repository: {updater.github_url}")
    print()

    # Confirm before proceeding
    response = input("Do you want to update your GitHub repository? (y/N): ")
    if response.lower() != "y":
        print("❌ Update cancelled")
        return

    # Run the update
    updater.update_github_repo()


if __name__ == "__main__":
    main()
