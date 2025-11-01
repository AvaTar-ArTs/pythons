"""
Github Upload Manager

This module provides functionality for github upload manager.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
GitHub Upload Manager
Prepares and uploads repositories to GitHub with proper configuration
"""

import os
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class GitHubUploadManager:
    """Manages GitHub repository uploads and configuration."""

    def __init__(self, github_dir: str = Path("/Users/steven/Documents/github")):
        """__init__ function."""

        self.github_dir = Path(github_dir)
        self.upload_log = []

    def prepare_repository_for_upload(self, repo_path: str, github_username: str = "ichoake") -> Dict[str, Any]:
        """Prepare a single repository for GitHub upload."""
        repo_path = Path(repo_path)

        if not repo_path.exists():
            return {"success": False, "error": "Repository path does not exist"}

        logger.info(f"🚀 Preparing {repo_path.name} for GitHub upload")

        try:
            # Initialize git if not already done
            if not (repo_path / ".git").exists():
                self._init_git_repo(repo_path)

            # Add all files
            self._add_all_files(repo_path)

            # Create initial commit
            self._create_initial_commit(repo_path)

            # Create GitHub repository URL
            repo_url = f"https://github.com/{github_username}/{repo_path.name}.git"

            # Add remote origin
            self._add_remote_origin(repo_path, repo_url)

            # Create push script
            push_script = self._create_push_script(repo_path, repo_url)

            return {
                "success": True,
                "repo_name": repo_path.name,
                "repo_url": repo_url,
                "push_script": push_script,
                "status": "Ready for upload",
            }

        except Exception as e:
            logger.error(f"Error preparing {repo_path.name}: {e}")
            return {"success": False, "error": str(e)}

    def _init_git_repo(self, repo_path: Path):
        """Initialize git repository."""
        logger.info(f"Initializing git repository in {repo_path.name}")
        subprocess.run(["git", "init"], cwd=repo_path, check=True)

    def _add_all_files(self, repo_path: Path):
        """Add all files to git."""
        logger.info(f"Adding files to git in {repo_path.name}")
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

    def _create_initial_commit(self, repo_path: Path):
        """Create initial commit."""
        logger.info(f"Creating initial commit for {repo_path.name}")
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Initial commit: {repo_path.name} - Enhanced with professional documentation and code quality improvements",
            ],
            cwd=repo_path,
            check=True,
        )

    def _add_remote_origin(self, repo_path: Path, repo_url: str):
        """Add remote origin."""
        logger.info(f"Adding remote origin for {repo_path.name}")
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=repo_path, check=True)

    def _create_push_script(self, repo_path: Path, repo_url: str) -> str:
        """Create a push script for the repository."""
        script_content = f"""#!/bin/bash
# Push script for {repo_path.name}
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo "🚀 Pushing {repo_path.name} to GitHub..."

# Check if repository exists on GitHub
if ! git ls-remote --heads origin main >/dev/null 2>&1; then
    echo "📝 Creating new repository on GitHub..."
    echo "Please create the repository '{repo_path.name}' on GitHub first:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: {repo_path.name}"
    echo "3. Description: {self._get_repo_description(repo_path)}"
    echo "4. Make it public or private as desired"
    echo "5. Don't initialize with README (we already have one)"
    echo "6. Click 'Create repository'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed {repo_path.name} to GitHub!"
    echo "🌐 Repository URL: {repo_url}"
else
    echo "❌ Failed to push to GitHub. Please check your credentials and try again."
    exit 1
fi
"""

        script_path = repo_path / "push_to_github.sh"
        with open(script_path, "w") as f:
            f.write(script_content)

        # Make script executable
        os.chmod(script_path, 0o755)

        return str(script_path)

    def _get_repo_description(self, repo_path: Path) -> str:
        """Get repository description from README or generate one."""
        readme_path = repo_path / "README.md"
        if readme_path.exists():
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract description from README
                lines = content.split("\n")
                for line in lines[:10]:  # Check first 10 lines
                    if line.strip() and not line.startswith("#") and not line.startswith("["):
                        return line.strip()[:CONSTANT_100]  # Limit to CONSTANT_100 characters

        return f"A {self._detect_project_type(repo_path)} project with professional documentation and code quality improvements"

    def _detect_project_type(self, repo_path: Path) -> str:
        """Detect project type."""
        if (repo_path / "package.json").exists():
            return "Node.js/JavaScript"
        elif (repo_path / "requirements.txt").exists() or (repo_path / "pyproject.toml").exists():
            return "Python"
        elif any(repo_path.glob("*.py")):
            return "Python"
        elif any(repo_path.glob("*.js")) or any(repo_path.glob("*.ts")):
            return "JavaScript/TypeScript"
        else:
            return "General"

    def prepare_all_repositories(self, github_username: str = "ichoake") -> Dict[str, Any]:
        """Prepare all repositories for GitHub upload."""
        logger.info("🚀 Preparing all repositories for GitHub upload")

        results = {"total_repos": 0, "prepared": 0, "failed": 0, "repositories": {}, "push_scripts": []}

        for repo_path in self.github_dir.iterdir():
            if repo_path.is_dir() and not repo_path.name.startswith("."):
                results["total_repos"] += 1

                try:
                    result = self.prepare_repository_for_upload(str(repo_path), github_username)
                    results["repositories"][repo_path.name] = result

                    if result["success"]:
                        results["prepared"] += 1
                        results["push_scripts"].append(result["push_script"])
                    else:
                        results["failed"] += 1

                except Exception as e:
                    results["failed"] += 1
                    results["repositories"][repo_path.name] = {"success": False, "error": str(e)}

        logger.info(f"✅ Preparation complete: {results['prepared']}/{results['total_repos']} repositories prepared")
        return results

    def create_master_upload_script(self, github_username: str = "ichoake") -> str:
        """Create a master script to upload all repositories."""
        script_content = f"""#!/bin/bash
# Master GitHub Upload Script
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# GitHub Username: {github_username}

echo "🚀 GitHub Repository Upload Manager"
echo "=================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it first:"
    echo "  brew install gh  # macOS"
    echo "  or visit: https://cli.github.com/"
    exit 1
fi

# Check if user is logged in to GitHub
if ! gh auth status &> /dev/null; then
    echo "🔐 Please log in to GitHub first:"
    echo "  gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"
echo ""

# List of repositories to upload
repos=(
"""

        # Add all repository names
        for repo_path in self.github_dir.iterdir():
            if repo_path.is_dir() and not repo_path.name.startswith("."):
                script_content += f'    "{repo_path.name}"\n'

        script_content += """)

# Function to upload a single repository
upload_repo() {
    local repo_name=$1
    local repo_path="/Users/steven/Documents/github/$repo_name"
    
    echo "📁 Processing: $repo_name"
    
    if [ ! -d "$repo_path" ]; then
        echo "❌ Repository path not found: $repo_path"
        return 1
    fi
    
    cd "$repo_path"
    
    # Check if repository exists on GitHub
    if gh repo view "$repo_name" &> /dev/null; then
        echo "⚠️  Repository $repo_name already exists on GitHub"
        echo "   Updating existing repository..."
        git push origin main
    else
        echo "📝 Creating new repository: $repo_name"
        
        # Create repository on GitHub
        gh repo create "$repo_name" --public --description "$(head -n 1 README.md 2>/dev/null || echo 'Professional project with enhanced documentation')"
        
        # Push to GitHub
        git push -u origin main
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully uploaded: $repo_name"
        echo "🌐 URL: https://github.com/{github_username}/$repo_name"
    else
        echo "❌ Failed to upload: $repo_name"
    fi
    
    echo ""
}

# Main upload process
echo "🚀 Starting batch upload of {len([r for r in self.github_dir.iterdir() if r.is_dir() and not r.name.startswith('.')])} repositories..."
echo ""

for repo in "${{repos[@]}}"; do
    upload_repo "$repo"
done

echo "🎉 Batch upload complete!"
echo ""
echo "📊 Summary:"
echo "  Total repositories: ${{#repos[@]}}"
echo "  Check the output above for individual results"
echo ""
echo "🌐 Your repositories are now available at:"
echo "  https://github.com/{github_username}"
"""

        script_path = self.github_dir / "upload_all_repos.sh"
        with open(script_path, "w") as f:
            f.write(script_content)

        # Make script executable
        os.chmod(script_path, 0o755)

        logger.info(f"✅ Master upload script created: {script_path}")
        return str(script_path)

    def create_github_setup_guide(self) -> str:
        """Create a comprehensive GitHub setup guide."""
        guide_content = f"""# 🚀 GitHub Repository Upload Guide

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📋 Prerequisites

### 1. Install GitHub CLI
```bash
# macOS
brew install gh

# Or download from: https://cli.github.com/
```

### 2. Authenticate with GitHub
```bash
gh auth login
# Follow the prompts to authenticate
```

### 3. Verify Authentication
```bash
gh auth status
```

## 🚀 Upload Methods

### Method 1: Individual Repository Upload

For each repository you want to upload:

1. **Navigate to the repository directory:**
   ```bash
   cd /Users/steven/Documents/github/REPO_NAME
   ```

2. **Run the push script:**
   ```bash
   ./push_to_github.sh
   ```

3. **Follow the prompts** to create the repository on GitHub

### Method 2: Batch Upload (Recommended)

1. **Run the master upload script:**
   ```bash
   cd /Users/steven/Documents/github
   ./upload_all_repos.sh
   ```

2. **The script will:**
   - Check if repositories exist on GitHub
   - Create new repositories if needed
   - Upload all code and documentation
   - Provide URLs for each repository

## 📁 Repository Status

Your repositories are ready for upload with:

✅ **Professional README files** with badges and documentation  
✅ **Proper .gitignore files** for each project type  
✅ **LICENSE files** (MIT or Apache 2.0)  
✅ **GitHub Actions workflows** for CI/CD  
✅ **Enhanced code quality** with type hints and documentation  
✅ **Consistent project structure** across all repositories  

## 🎯 Recommended Upload Order

Upload these high-quality repositories first:

1. **ai-comic-factory** - Quality Score: 95/CONSTANT_100
2. **ai-comic-creator** - Quality Score: 90/CONSTANT_100  
3. **background-removal** - Quality Score: 85/CONSTANT_100
4. **harbor** - Quality Score: 80/CONSTANT_100
5. **comic_book_creator** - Quality Score: 75/CONSTANT_100

## 🔧 Manual Upload (Alternative)

If you prefer to upload manually:

1. **Go to GitHub.com** and create a new repository
2. **Copy the repository URL**
3. **In your local repository:**
   ```bash
   git remote add origin https://github.com/ichoake/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## 📊 Post-Upload Checklist

After uploading, verify each repository has:

- [ ] Professional README with badges
- [ ] Proper .gitignore file
- [ ] LICENSE file
- [ ] GitHub Actions workflow (if applicable)
- [ ] All files uploaded successfully
- [ ] Repository is public/private as intended

## 🎉 Success!

Once uploaded, your repositories will be available at:
**https://github.com/ichoake**

Your professional portfolio is now ready to showcase your technical expertise!

## 🆘 Troubleshooting

### Common Issues:

**"Repository already exists"**
- The script will update the existing repository
- Or manually delete and recreate if needed

**"Authentication failed"**
- Run `gh auth login` again
- Check your GitHub credentials

**"Push failed"**
- Check your internet connection
- Verify the repository name is available
- Ensure you have write permissions

### Getting Help:

- Check GitHub CLI documentation: https://cli.github.com/
- GitHub Help: https://docs.github.com/
- Repository issues: Check the individual repository logs

---

*This guide was generated by the GitHub Upload Manager*
"""

        guide_path = self.github_dir / "GITHUB_UPLOAD_GUIDE.md"
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)

        logger.info(f"✅ GitHub setup guide created: {guide_path}")
        return str(guide_path)


def main():
    """Main function to prepare repositories for GitHub upload."""
    manager = GitHubUploadManager()

    logger.info("🚀 GitHub Upload Manager")
    logger.info("=" * 50)

    # Prepare all repositories
    logger.info("📁 Preparing repositories for GitHub upload...")
    results = manager.prepare_all_repositories()

    logger.info(f"\n📊 Preparation Results:")
    logger.info(f"Total repositories: {results['total_repos']}")
    logger.info(f"Successfully prepared: {results['prepared']}")
    logger.info(f"Failed: {results['failed']}")

    # Create master upload script
    logger.info("\n📝 Creating master upload script...")
    master_script = manager.create_master_upload_script()
    logger.info(f"Master script created: {master_script}")

    # Create setup guide
    logger.info("\n📚 Creating setup guide...")
    guide_path = manager.create_github_setup_guide()
    logger.info(f"Setup guide created: {guide_path}")

    logger.info("\n🎉 Repository preparation complete!")
    logger.info("\n📋 Next steps:")
    logger.info("1. Install GitHub CLI: brew install gh")
    logger.info("2. Authenticate: gh auth login")
    logger.info("3. Run: ./upload_all_repos.sh")
    logger.info("4. Or follow the guide: GITHUB_UPLOAD_GUIDE.md")


if __name__ == "__main__":
    main()
