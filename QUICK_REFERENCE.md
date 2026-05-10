# ⚡ Quick Reference Guide

## 🎯 Common Tasks

### Finding Scripts by Purpose

| What You Need | Where to Look |
|---------------|---------------|
| API integrations | `apis/` or `tools/apis/` |
| Data analysis | `data_processing/` or `tools/data/` |
| File utilities | `file_operations/` or `tools/utils/` |
| Instagram bots | `MEDIA_PROCESSING/social_media/instagram/` |
| YouTube scripts | `MEDIA_PROCESSING/apis/youtube/` or `youtube/` |
| Image processing | `image_processing/` or `MEDIA_PROCESSING/image/` |
| Audio processing | `audio_processing/` or `MEDIA_PROCESSING/audio/` |
| Test files | `testing/` or `tools/testing/` |
| Config files | `config/` |
| LLM/AI scripts | `llm/` |

### Finding Scripts by Service

| Service | Location |
|---------|----------|
| Instagram | `MEDIA_PROCESSING/apis/instagram/`<br>`MEDIA_PROCESSING/social_media/instagram/` |
| YouTube | `MEDIA_PROCESSING/apis/youtube/`<br>`youtube/` |
| Audio APIs | `MEDIA_PROCESSING/apis/audio_apis/` |
| OpenAI | `llm/` (look for openai in filename) |

### Finding Scripts by Project

| Project | Location |
|---------|----------|
| Vibrant Chaplygin | `projects/vibrant-chaplygin/pyt/` |
| Simple Gallery | `projects/simplegallery/` |
| Media Processing | `MEDIA_PROCESSING/` |

---

## 📊 Directory Sizes

### Largest Directories
1. `projects/vibrant-chaplygin/pyt/` - 973 files
2. Root categories - 1,070 files (now organized)
3. `MEDIA_PROCESSING/` - 209 files
4. `tools/automation/scripts/` - 125 files
5. `youtube/` - 109 files

### Most Common Functionality
1. API-related - 1,853 files (44%)
2. Data processing - 703 files (17%)
3. Config - 653 files (15%)
4. File operations - 360 files (9%)
5. Audio processing - 321 files (8%)

---

## 🔍 Search Tips

### Using CSV Files

**Find files by functionality**:
```bash
# In PARENT_AWARE_ANALYSIS.csv
grep "api" PARENT_AWARE_ANALYSIS.csv | grep "aligned"

# Find misaligned files
grep "misaligned" PARENT_AWARE_ANALYSIS.csv
```

**Find files by folder**:
```bash
# In DEEP_FUNCTIONALITY_ANALYSIS.csv
grep "MEDIA_PROCESSING" DEEP_FUNCTIONALITY_ANALYSIS.csv
```

### Using File System

**Find Python files**:
```bash
find . -name "*.py" -type f | grep "instagram"
find . -name "*.py" -type f | grep "youtube"
```

**Count files in directory**:
```bash
ls -1 apis/*.py | wc -l
ls -1 tools/apis/*.py | wc -l
```

---

## 📁 Directory Map

```
~/pythons/
├── apis/                    # API scripts
├── data_processing/         # Data processing
├── file_operations/        # File utilities
├── audio_processing/        # Audio scripts
├── image_processing/       # Image scripts
├── automation/             # Automation
├── testing/                # Tests
├── config/                 # Config files
├── llm/                    # LLM scripts
├── other/                  # Miscellaneous
├── tools/                  # Tools directory
│   ├── apis/              # API tools
│   ├── data/              # Data tools
│   ├── utils/             # Utility tools
│   ├── testing/           # Test tools
│   └── automation/        # Automation tools
├── projects/               # Projects
│   ├── vibrant-chaplygin/
│   └── simplegallery/
├── MEDIA_PROCESSING/       # Media processing
│   ├── apis/              # Service APIs
│   ├── processing/        # Processing
│   ├── audio/             # Audio
│   ├── image/             # Image
│   ├── video/             # Video
│   └── social_media/      # Social media
└── [other directories]
```

---

## 🚨 Important Notes

### After Reorganization

1. **Imports may be broken** - Update imports in moved files
2. **Paths may need updating** - Fix hardcoded file paths
3. **Test your scripts** - Verify everything still works
4. **Check dependencies** - Ensure dependencies are still accessible

### File Locations Changed

- **1,303 files moved** during reorganization
- **Root level**: All files moved to categories
- **tools/**: 233 files organized into subfolders
- **MEDIA_PROCESSING/**: 54 files organized in social_media/

---

*Quick reference for navigating the reorganized structure*
