#!/usr/bin/env python3
"""Professional Repository Setup Script
Creates GitHub repositories for QuantumForge Labs services
"""

import os
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ProfessionalRepoSetup:
    """Sets up professional GitHub repositories."""

    def __init__(self, base_dir: str = "/Users/steven"):
        self.base_dir = Path(base_dir)
        self.portfolio_dir = self.base_dir / "professional_portfolio"
        self.github_dir = self.base_dir / "Documents" / "github"
        self.repositories = {
            "ai-ml-solutions": {
                "name": "AI/ML Solutions",
                "description": "AI/ML Development Services - Professional Python solutions for machine learning, deep learning, and artificial intelligence applications",
                "topics": [
                    "python",
                    "machine-learning",
                    "artificial-intelligence",
                    "deep-learning",
                    "tensorflow",
                    "pytorch",
                    "openai",
                    "nlp",
                    "computer-vision",
                    "data-science",
                ],
            },
            "media-processing-pro": {
                "name": "Media Processing Pro",
                "description": "Media Processing Pro - Professional Python solutions for image, video, and audio processing with advanced computer vision capabilities",
                "topics": [
                    "python",
                    "computer-vision",
                    "image-processing",
                    "video-processing",
                    "opencv",
                    "pillow",
                    "ffmpeg",
                    "media-processing",
                    "computer-graphics",
                ],
            },
            "automation-suite": {
                "name": "Automation Suite",
                "description": "Automation Suite - Professional Python solutions for web scraping, API integration, and business process automation",
                "topics": [
                    "python",
                    "automation",
                    "web-scraping",
                    "api-integration",
                    "selenium",
                    "requests",
                    "beautifulsoup",
                    "workflow-automation",
                    "business-process",
                ],
            },
            "data-engineering-pro": {
                "name": "Data Engineering Pro",
                "description": "Data Engineering Pro - Professional Python solutions for data pipelines, ETL processes, and analytics infrastructure",
                "topics": [
                    "python",
                    "data-engineering",
                    "etl",
                    "data-pipelines",
                    "pandas",
                    "numpy",
                    "apache-airflow",
                    "data-analytics",
                    "big-data",
                    "sql",
                ],
            },
            "dev-tools-pro": {
                "name": "Dev Tools Pro",
                "description": "Dev Tools Pro - Professional Python development tools, utilities, and productivity enhancements",
                "topics": [
                    "python",
                    "development-tools",
                    "utilities",
                    "productivity",
                    "cli-tools",
                    "code-analysis",
                    "testing",
                    "debugging",
                    "development-workflow",
                ],
            },
            "content-ai-studio": {
                "name": "Content AI Studio",
                "description": "Content AI Studio - Professional Python solutions for AI-powered content creation, natural language processing, and creative automation",
                "topics": [
                    "python",
                    "content-creation",
                    "nlp",
                    "text-processing",
                    "ai-writing",
                    "content-automation",
                    "creative-ai",
                    "language-models",
                    "text-generation",
                ],
            },
        }

    def setup_all_repositories(self):
        """Set up all professional repositories."""
        print("🚀 Professional Repository Setup")
        print("=" * 50)
        print(f"Portfolio directory: {self.portfolio_dir}")
        print(f"GitHub directory: {self.github_dir}")
        print()

        if not self.portfolio_dir.exists():
            print(f"❌ Portfolio directory not found: {self.portfolio_dir}")
            print("Please run the portfolio creation script first.")
            return

        # Create GitHub directory if it doesn't exist
        self.github_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        total_count = len(self.repositories)

        for repo_id, repo_info in self.repositories.items():
            print(f"📦 Setting up: {repo_info['name']}")
            print("-" * 30)

            try:
                self._setup_single_repository(repo_id, repo_info)
                success_count += 1
                print(f"✅ Successfully set up: {repo_info['name']}")
            except Exception as e:
                print(f"❌ Error setting up {repo_info['name']}: {e}")

            print()

        print("🎉 Repository Setup Complete!")
        print("=" * 50)
        print(f"Successfully set up: {success_count}/{total_count} repositories")
        print()

        if success_count > 0:
            print("📋 Next Steps:")
            print("1. Review the created repositories")
            print("2. Customize content for each service")
            print("3. Add example projects and code")
            print("4. Set up GitHub Pages for documentation")
            print("5. Start marketing your services")
            print()
            print("🔗 Repository URLs:")
            for repo_id in self.repositories.keys():
                print(f"   https://github.com/ichoake/{repo_id}")

    def _setup_single_repository(self, repo_id: str, repo_info: dict):
        """Set up a single repository."""
        try:
            # Create repository directory
            repo_dir = self.github_dir / repo_id
            repo_dir.mkdir(parents=True, exist_ok=True)

            # Copy content from portfolio
            source_dir = self.portfolio_dir / repo_id
            if source_dir.exists():
                self._copy_repository_content(source_dir, repo_dir)
                print(f"✅ Copied content to {repo_dir}")
            else:
                print(f"⚠️  Source directory not found: {source_dir}")
                # Create basic structure
                self._create_basic_repository_structure(repo_dir, repo_info)

            # Initialize Git repository
            self._initialize_git_repo(repo_dir)

            # Create GitHub repository
            self._create_github_repository(repo_id, repo_info)

            # Push to GitHub
            self._push_to_github(repo_dir, repo_id)

        except Exception as e:
            print(f"❌ Error in _setup_single_repository: {e}")
            raise

    def _copy_repository_content(self, source_dir: Path, target_dir: Path):
        """Copy content from source to target directory."""
        import shutil

        # Copy all files and directories
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, target_dir)
            elif item.is_dir():
                shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)

    def _create_basic_repository_structure(self, repo_dir: Path, repo_info: dict):
        '\''Create basic repository structure if source doesn't exist."""
        # Create README.md
        readme_content = f"""# {repo_info["name"]}

{repo_info["description"]}

## Services

- Custom Python development
- Professional consulting
- Project-based solutions
- Ongoing support and maintenance

## Contact

**Steven Choake**  
**QuantumForge Labs**  
Email: steven@quantumforgelabs.com  
Phone: (555) 123-4567  

## Pricing

- **Hourly Rate**: $150-300/hour
- **Project Rate**: $5,000-50,000+
- **Retainer**: $3,000-20,000/month

## Portfolio

View our complete portfolio at: https://github.com/ichoake/python

---

*Professional Python development services with guaranteed results.*
"""

        with open(repo_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

        # Create LICENSE
        license_content = """MIT License

Copyright (c) 2025 QuantumForge Labs

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

        with open(repo_dir / "LICENSE", "w", encoding="utf-8") as f:
            f.write(license_content)

        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

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
temp/
tmp/
"""

        with open(repo_dir / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)

    def _initialize_git_repo(self, repo_dir: Path):
        """Initialize Git repository."""
        try:
            # Change to repository directory
            os.chdir(repo_dir)

            # Initialize Git repository
            subprocess.run(["git", "init"], check=True)

            # Add all files
            subprocess.run(["git", "add", "."], check=True)

            # Create initial commit
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "Initial commit: Professional service repository",
                ],
                check=True,
            )

            # Set main branch
            subprocess.run(["git", "branch", "-M", "main"], check=True)

            print(f"✅ Git repository initialized in {repo_dir}")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git initialization failed: {e}")
        except Exception as e:
            print(f"⚠️  Error initializing Git: {e}")

    def _create_github_repository(self, repo_id: str, repo_info: dict):
        """Create GitHub repository using GitHub CLI."""
        try:
            # Check if GitHub CLI is available
            subprocess.run(["gh", "--version"], check=True, capture_output=True)

            # Create repository
            cmd = [
                "gh",
                "repo",
                "create",
                repo_id,
                "--public",
                "--description",
                repo_info["description"],
                "--add-readme",
            ]

            # Add topics
            for topic in repo_info["topics"]:
                cmd.extend(["--topic", topic])

            subprocess.run(cmd, check=True)
            print(f"✅ GitHub repository created: {repo_id}")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  GitHub CLI failed: {e}")
            print("Please create the repository manually at: https://github.com/new")
        except FileNotFoundError:
            print("⚠️  GitHub CLI not installed. Please install it first:")
            print("   brew install gh")
            print("   gh auth login")
        except Exception as e:
            print(f"⚠️  Error creating GitHub repository: {e}")

    def _push_to_github(self, repo_dir: Path, repo_id: str):
        """Push repository to GitHub."""
        try:
            # Change to repository directory
            os.chdir(repo_dir)

            # Add remote origin
            subprocess.run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    f"https://github.com/ichoake/{repo_id}.git",
                ],
                check=True,
            )

            # Push to GitHub
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print(f"✅ Successfully pushed to GitHub: {repo_id}")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Push failed: {e}")
            print("Please push manually:")
            print(f"   cd {repo_dir}")
            print(f"   git remote add origin https://github.com/ichoake/{repo_id}.git")
            print("   git push -u origin main")
        except Exception as e:
            print(f"⚠️  Error pushing to GitHub: {e}")


def main():
    """Main function to set up professional repositories.'\''
    setup = ProfessionalRepoSetup()

    print("🚀 Professional Repository Setup")
    print("=" * 50)
    print()

    response = input("Do you want to set up professional GitHub repositories? (y/N): ")
    if response.lower() != "y":
        print("❌ Setup cancelled")
        return

    setup.setup_all_repositories()

    print("\n✨ Professional repository setup complete!")
    print("\n📋 Next Steps:")
    print("1. Review the created repositories")
    print("2. Customize content for each service")
    print("3. Add example projects and code")
    print("4. Set up GitHub Pages for documentation")
    print("5. Start marketing your services")


if __name__ == "__main__":
    main()
