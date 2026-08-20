# 🐍 Python Tools & Automation Collection

> A comprehensive collection of Python scripts and tools for automation, media processing, AI/ML, web scraping, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Maintained: Yes](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/ichoake/python)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains a curated collection of Python scripts and tools organized by functionality. The collection has been cleaned and optimized for production use, with over 1 million lines of obsolete code removed.

### 📊 Current Stats
- **Active Scripts**: ~460 Python files
- **Repository Size**: 1.8GB
- **Categories**: 40+ functional categories
- **Python Version**: 3.8+

## ✨ Key Features

### 🤖 AI & Machine Learning
- Advanced content analyzers
- Machine learning model utilities
- Natural language processing tools
- Image recognition scripts

### 🎬 Media Processing
- Audio transcription (Whisper integration)
- Video processing and conversion
- Image upscaling and enhancement
- Thumbnail generation
- Gallery creators

### 🌐 Web Automation
- Web scraping tools (BeautifulSoup, Selenium)
- API clients and wrappers
- Content downloaders
- Automated posting tools

### 📊 Data Management
- CSV/JSON/Excel processors
- Data analysis utilities
- Database management tools
- File organization systems

### 🔧 Development Tools
- Code quality analyzers
- Documentation generators
- Git automation scripts
- Project organizers

## 📁 Repository Structure

```
python/
├── 00_production/          # Production-ready scripts
├── 01_core_tools/          # Core utility functions
├── 01_experiments/         # Experimental features (limited)
├── 02_media_processing/    # Media tools
├── 02_youtube_automation/  # YouTube-specific tools
├── 03_ai_creative_tools/   # AI/ML utilities
├── 03_automation_platforms/# Automation frameworks
├── 03_utilities/           # General utilities
├── 04_ai_tools/            # AI integration tools
├── 04_content_creation/    # Content generation
├── 04_web_scraping/        # Web scraping tools
├── 05_audio_video/         # A/V processing
├── 05_data_management/     # Data handling
├── 06_development_tools/   # Dev utilities
├── 06_utilities/           # Additional utilities
├── 07_experimental/        # Experimental code
├── 08_archived/            # Archived projects
├── 09_documentation/       # Documentation
├── docs/                   # Generated documentation
├── functional_category_analyzer.py  # Script categorizer
├── .gitignore              # Comprehensive ignore rules
├── .gitattributes          # Git LFS configuration
└── .editorconfig           # Editor settings

```

## 🚀 Getting Started

### Prerequisites

```bash
# Required
Python 3.8+
pip or conda

# Optional (for specific features)
ffmpeg (for video processing)
git-lfs (for large files)
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ichoake/python.git
   cd python
   ```

2. **Install dependencies** (project-specific)
   ```bash
   # Each tool may have its own requirements
   pip install -r requirements.txt  # if available
   ```

3. **Configure API keys** (if needed)
   ```bash
   # Store sensitive data in ~/.env.d/
   mkdir -p ~/.env.d
   echo "YOUR_API_KEY=xxx" > ~/.env.d/project_name.env
   ```

### Quick Start

```bash
# Run the functional category analyzer
python3 functional_category_analyzer.py

# Check categorization results
cat functional_analysis/functional_summary_*.csv
```

## 💡 Usage Examples

### Media Processing

```python
# Example: Audio transcription
python transcriber.py --input audio.mp3 --output transcript.txt

# Example: Image upscaling
python upscaler.py --input image.jpg --scale 4x
```

### Web Scraping

```python
# Example: Web data extraction
python web_scraper.py --url https://example.com --output data.json
```

### Automation

```python
# Example: Batch file processing
python batch_processor.py --dir ./files --action convert
```

## 🔒 Security

### Best Practices Implemented

✅ **Comprehensive .gitignore** - Protects sensitive files
✅ **API Key Management** - Credentials stored in `~/.env.d/`
✅ **Git LFS** - Large file handling configured
✅ **SSH Authentication** - Secure GitHub access

### Important Notes

⚠️ **Never commit credentials** - Use environment variables
⚠️ **Review .gitignore** - Ensure sensitive patterns are covered
⚠️ **Use SSH keys** - Configured for GitHub authentication

## 📖 Documentation

- **Project READMEs**: Individual project documentation in `docs/projects/`
- **API Reference**: Generated documentation in `docs/api/`
- **Code Analysis**: Results from functional_category_analyzer.py

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🛠️ Tools Used

- **Python 3.8+**: Core language
- **Git LFS**: Large file storage
- **GitHub Actions**: CI/CD (planned)
- **Various Python libraries**: See individual project requirements

## 📝 Recent Changes

### 2025-10-26
- 🧹 Cleaned up 3,940 obsolete files (1M+ lines removed)
- ✅ Added comprehensive .gitignore with security patterns
- 🔐 Configured Git LFS for large files
- 📊 Added functional_category_analyzer.py
- 🔧 Added .editorconfig for code consistency
- 📚 Improved documentation

### 2025-10-14
- 📄 Generated comprehensive project documentation
- 🚀 Initial repository auto-update system

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/ichoake/python/issues)
- **Pull Requests**: [GitHub PRs](https://github.com/ichoake/python/pulls)
- **Documentation**: Check individual project READMEs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Python community for excellent libraries
- Open source contributors
- AI/ML community for models and tools

---

**Last Updated**: 2025-10-26
**Maintained by**: [@ichoake](https://github.com/ichoake)
**Repository**: [github.com/ichoake/python](https://github.com/ichoake/python)

