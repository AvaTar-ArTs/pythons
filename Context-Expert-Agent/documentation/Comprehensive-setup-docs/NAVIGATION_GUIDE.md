# 🗺️ Python Script Navigation Guide

*Complete guide to finding any Python script in your organized structure*

## 🚀 **QUICK SEARCH METHODS**

### **1. Command Line Search (Fastest)**
```bash
# Find any script by name
python whereis.py <script_name>

# Examples:
python whereis.py analyze
python whereis.py transcription
python whereis.py youtube
python whereis.py convert
python whereis.py organize

# Show all categories
python whereis.py --categories
```

### **2. Interactive Search (Most Comprehensive)**
```bash
# Start interactive search
python find_script.py

# Commands in interactive mode:
search analyze          # Search by script name
func transcription      # Find by functionality
tree                   # Show directory structure
category 1             # Show category contents (1-8)
help                   # Show help
quit                   # Exit
```

### **3. File System Search**
```bash
# Search by filename pattern
find . -name "*analyze*" -type f

# Search by content
grep -r "transcription" . --include="*.py"

# Search in specific category
find 01_core_ai_analysis -name "*.py" | head -10
```

## 📁 **DIRECTORY STRUCTURE OVERVIEW**

```
/Users/steven/Documents/python/
├── 01_core_ai_analysis/          # 576 scripts - AI & Analysis
│   ├── transcription/            # Audio/video transcription tools
│   ├── content_analysis/         # Text and content analysis
│   ├── data_processing/          # Data analysis and processing
│   └── ai_generation/            # AI content generation tools
│
├── 02_media_processing/          # 526 scripts - Media Processing
│   ├── image_tools/              # Image processing and manipulation
│   ├── video_tools/              # Video processing and editing
│   ├── audio_tools/              # Audio processing and conversion
│   └── format_conversion/        # File format conversion
│
├── 03_automation_platforms/      # 131 scripts - Platform Automation
│   ├── youtube_automation/       # YouTube content automation
│   ├── social_media_automation/  # Social media platform automation
│   ├── web_automation/           # Web scraping and automation
│   └── api_integrations/         # Third-party API integrations
│
├── 05_data_management/           # 43 scripts - Data Management
│   ├── data_collection/          # Data scraping and collection
│   ├── file_organization/        # File management and organization
│   ├── database_tools/           # Database and storage tools
│   └── backup_utilities/         # Backup and archival tools
│
├── 06_development_tools/         # 101 scripts - Development Tools
│   ├── testing_framework/        # Testing and debugging tools
│   ├── development_utilities/    # Development helper tools
│   ├── code_analysis/            # Code analysis and quality tools
│   └── deployment_tools/         # Deployment and distribution tools
│
└── [Previous structure preserved]
    ├── 01_core_tools/            # Original core tools
    ├── 02_youtube_automation/    # Original YouTube tools
    └── ... (previous organization)
```

## 🔍 **COMMON SCRIPT LOCATIONS**

### **Analysis Scripts:**
- **Main analysis**: `01_core_ai_analysis/transcription/`
- **Content analysis**: `01_core_ai_analysis/content_analysis/`
- **Data analysis**: `01_core_ai_analysis/data_processing/`
- **Image analysis**: `02_media_processing/image_tools/`

### **Transcription Scripts:**
- **Audio transcription**: `01_core_ai_analysis/transcription/`
- **Video transcription**: `01_core_ai_analysis/transcription/`
- **Whisper tools**: `01_core_ai_analysis/transcription/`

### **Media Processing:**
- **Image tools**: `02_media_processing/image_tools/`
- **Video tools**: `02_media_processing/video_tools/`
- **Audio tools**: `02_media_processing/audio_tools/`
- **Format conversion**: `02_media_processing/format_conversion/`

### **Automation Scripts:**
- **YouTube automation**: `03_automation_platforms/youtube_automation/`
- **Social media**: `03_automation_platforms/social_media_automation/`
- **Web scraping**: `03_automation_platforms/web_automation/`
- **API integrations**: `03_automation_platforms/api_integrations/`

### **Utility Scripts:**
- **File organization**: `05_data_management/file_organization/`
- **Development tools**: `06_development_tools/development_utilities/`
- **Testing tools**: `06_development_tools/testing_framework/`

## 📊 **SCRIPT STATISTICS**

### **By Category:**
- **01_core_ai_analysis**: 576 scripts (43.2%)
- **02_media_processing**: 526 scripts (39.4%)
- **03_automation_platforms**: 131 scripts (9.8%)
- **06_development_tools**: 101 scripts (7.6%)
- **05_data_management**: 43 scripts (3.2%)

### **By Functionality:**
- **Analysis**: 87 scripts
- **Generation**: 51 scripts
- **Testing**: 55 scripts
- **Organization**: 54 scripts
- **Automation**: 50 scripts
- **Transcription**: 37 scripts
- **Processing**: 30 scripts
- **Conversion**: 22 scripts
- **Scraping**: 15 scripts
- **Visualization**: 2 scripts

## 🎯 **SEARCH STRATEGIES**

### **1. By Script Name:**
```bash
# Exact name
python whereis.py transcription_analyzer.py

# Partial name
python whereis.py analyze

# Pattern matching
python whereis.py youtube
```

### **2. By Functionality:**
```bash
# Start interactive search
python find_script.py

# Then use:
func transcription    # Find transcription tools
func analysis        # Find analysis tools
func image          # Find image processing tools
func youtube        # Find YouTube tools
func convert        # Find conversion tools
```

### **3. By Category:**
```bash
# Show category contents
python find_script.py
# Then use:
category 1          # Show AI & Analysis tools
category 2          # Show Media Processing tools
category 3          # Show Automation tools
```

### **4. By Content:**
```bash
# Search file contents
grep -r "openai" . --include="*.py"
grep -r "whisper" . --include="*.py"
grep -r "youtube" . --include="*.py"
```

## 📋 **QUICK REFERENCE COMMANDS**

### **Essential Commands:**
```bash
# Find any script
python whereis.py <script_name>

# Interactive search
python find_script.py

# Show all categories
python whereis.py --categories

# Search by content
grep -r "keyword" . --include="*.py"

# List files in category
ls 01_core_ai_analysis/transcription/
```

### **Navigation Shortcuts:**
```bash
# Go to main categories
cd 01_core_ai_analysis/          # AI & Analysis
cd 02_media_processing/          # Media Processing
cd 03_automation_platforms/      # Automation
cd 05_data_management/           # Data Management
cd 06_development_tools/         # Development Tools

# Go to specific subcategories
cd 01_core_ai_analysis/transcription/
cd 02_media_processing/image_tools/
cd 03_automation_platforms/youtube_automation/
```

## 🗂️ **FILE ORGANIZATION PATTERNS**

### **Consolidated Groups:**
- Files with similar names are grouped in `*_consolidated/` folders
- Example: `analyze.py_consolidated/` contains multiple analyze scripts
- This reduces clutter and groups related functionality

### **Naming Conventions:**
- **Analysis scripts**: `analyze_*`, `*_analyzer.py`
- **Transcription scripts**: `*_transcribe*`, `whisper_*`
- **Conversion scripts**: `convert_*`, `*_converter.py`
- **YouTube scripts**: `youtube_*`, `yt_*`
- **Image scripts**: `img_*`, `image_*`, `*_image.py`

## 💡 **PRO TIPS**

### **1. Use the Interactive Search:**
- Most comprehensive search tool
- Shows context and descriptions
- Allows browsing by category

### **2. Check Consolidated Groups:**
- Look in `*_consolidated/` folders for similar scripts
- These contain related functionality grouped together

### **3. Use Content Search:**
- Search by functionality keywords
- Find scripts by what they do, not just their name

### **4. Browse by Category:**
- Each category has a specific purpose
- Use category numbers (1-8) for quick navigation

### **5. Check the Map Files:**
- `script_map_readable.txt` - Human-readable complete map
- `complete_script_map.json` - Machine-readable complete map

## 🆘 **TROUBLESHOOTING**

### **Can't Find a Script?**
1. Try partial name: `python whereis.py analyze`
2. Use interactive search: `python find_script.py`
3. Search by content: `grep -r "keyword" .`
4. Check consolidated groups: `ls */*_consolidated/`

### **Too Many Results?**
1. Be more specific with the name
2. Use category search: `category 1`
3. Use functionality search: `func transcription`

### **Script Not Working?**
1. Check if it's in the right category
2. Look for similar scripts in consolidated groups
3. Check dependencies and imports

---

**Remember**: Your scripts are now organized by **actual functionality and content**, not just filenames. Use the search tools to find what you need quickly! 🚀