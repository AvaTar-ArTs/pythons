#!/bin/bash
# Update GitHub Repository
# This script automatically updates the GitHub repository with all Python projects

GITHUB_URL="https://github.com/ichoake/python.git"
REPO_NAME="python"
UPLOAD_DIR="github_upload"

echo "🚀 GitHub Repository Auto Updater"
echo "=================================="
echo "Repository: $GITHUB_URL"
echo "Started at: $(date)"
echo ""

# Check if we're in the right directory
if [ ! -d "comprehensive_docs" ]; then
    echo "❌ Documentation not found. Please run analysis first:"
    echo "   python3 simple_analysis_and_docs.py"
    exit 1
fi

# Confirm before proceeding
echo "⚠️  This will update your GitHub repository with all Python projects."
echo "   Repository: $GITHUB_URL"
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Update cancelled"
    exit 1
fi

echo ""
echo "📁 Step 1: Preparing Repository..."
echo "----------------------------------"

# Create upload directory
if [ -d "$UPLOAD_DIR" ]; then
    rm -rf "$UPLOAD_DIR"
fi
mkdir -p "$UPLOAD_DIR"
echo "✅ Created upload directory: $UPLOAD_DIR"

echo ""
echo "📝 Step 2: Creating Main README..."
echo "----------------------------------"

# Copy main README
if [ -f "comprehensive_docs/README.md" ]; then
    cp "comprehensive_docs/README.md" "$UPLOAD_DIR/README.md"
    echo "✅ Copied main README.md"
else
    echo "⚠️  Main README not found, creating basic one"
    cat > "$UPLOAD_DIR/README.md" << 'EOF'
# 🐍 Python Projects Collection

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
EOF
fi

echo ""
echo "🏗️ Step 3: Creating Project Structure..."
echo "----------------------------------------"

# Copy project directories
PROJECTS=(
    "01_core_ai_analysis"
    "02_media_processing"
    "03_automation_platforms"
    "04_content_creation"
    "05_data_management"
    "06_development_tools"
    "07_business_setup"
    "08_archived"
    "00_shared_libraries"
    "github_repo"
)

COPIED_COUNT=0
for project in "${PROJECTS[@]}"; do
    if [ -d "$project" ]; then
        echo "📁 Copying project: $project"
        cp -r "$project" "$UPLOAD_DIR/"
        COPIED_COUNT=$((COPIED_COUNT + 1))
    fi
done

echo "✅ Copied $COPIED_COUNT projects"

echo ""
echo "📚 Step 4: Copying Documentation..."
echo "-----------------------------------"

# Copy documentation
if [ -d "comprehensive_docs" ]; then
    cp -r "comprehensive_docs" "$UPLOAD_DIR/docs"
    echo "✅ Copied comprehensive documentation"
fi

# Create docs index
cat > "$UPLOAD_DIR/docs/README.md" << 'EOF'
# 📚 Documentation

This directory contains comprehensive documentation for all Python projects.

## Available Documentation

- **README.md** - Main overview and project statistics
- **sphinx/** - Professional HTML documentation
- **pydoc/** - Automated API documentation
- **api/** - API reference
- **portfolio/** - Project portfolio showcase
- **projects/** - Individual project documentation

## Quick Access

- [Main Overview](../README.md)
- [Sphinx Documentation](sphinx/_build/html/index.html)
- [PyDoc Documentation](pydoc/index.html)
- [API Reference](api/index.md)
- [Portfolio](portfolio/README.md)

---

*This documentation was automatically generated*
EOF

echo "✅ Created documentation index"

echo ""
echo "📄 Step 5: Creating Repository Files..."
echo "---------------------------------------"

# Create requirements.txt
cat > "$UPLOAD_DIR/requirements.txt" << 'EOF'
# Python Projects Collection - Requirements
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
EOF

echo "✅ Created requirements.txt"

# Create LICENSE
cat > "$UPLOAD_DIR/LICENSE" << 'EOF'
MIT License

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
EOF

echo "✅ Created LICENSE file"

# Create .gitignore
cat > "$UPLOAD_DIR/.gitignore" << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

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
*.egg-info/
.installed.cfg
*.egg
MANIFEST

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

# Sphinx documentation
docs/_build/

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
*.temp
temp/
tmp/
logs/
EOF

echo "✅ Created .gitignore file"

echo ""
echo "🔄 Step 6: Git Operations..."
echo "----------------------------"

# Change to upload directory
cd "$UPLOAD_DIR"

# Initialize Git repository
if [ ! -d ".git" ]; then
    git init
    echo "✅ Initialized Git repository"
fi

# Add all files
git add .
echo "✅ Added all files to Git"

# Create commit
COMMIT_MSG="🚀 Auto-update: $(date '+%Y-%m-%d %H:%M:%S')

- Added comprehensive Python projects collection
- Generated professional documentation
- Created Sphinx and PyDoc documentation
- Added portfolio showcase
- Implemented quality analysis and scoring"

git commit -m "$COMMIT_MSG"
echo "✅ Created commit"

# Add remote origin
git remote remove origin 2>/dev/null || true
git remote add origin "$GITHUB_URL"
echo "✅ Added remote origin"

# Push to GitHub
echo "📤 Pushing to GitHub..."
if git push -u origin main; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "⚠️  Push failed, trying with master branch..."
    if git push -u origin master; then
        echo "✅ Successfully pushed to GitHub (master branch)!"
    else
        echo "❌ Push failed. Please check your GitHub access and try manually:"
        echo "   cd $UPLOAD_DIR"
        echo "   git push -u origin main"
        exit 1
    fi
fi

echo ""
echo "🎉 GitHub Repository Updated Successfully!"
echo "=========================================="
echo "Repository URL: $GITHUB_URL"
echo "Completed at: $(date)"
echo ""
echo "📁 What was uploaded:"
echo "  - All Python projects with documentation"
echo "  - Comprehensive analysis reports"
echo "  - Professional README files"
echo "  - Sphinx and PyDoc documentation"
echo "  - Portfolio showcase"
echo ""
echo "🌐 View your repository:"
echo "  $GITHUB_URL"
echo ""
echo "✨ Your Python projects are now live on GitHub!"