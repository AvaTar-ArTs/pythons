# SimpleGallery 2.1

**Version:** 2.1.0  
**Status:** Advanced Edition  
**Release Date:** 2024-11-25

---

## 🚀 What's New in 2.1

SimpleGallery 2.1 is the **advanced edition** with significant improvements:

### ✨ Key Features

1. **Enhanced Configuration System**
   - Automatic validation
   - Smart defaults
   - Configuration migration
   - Environment variable support

2. **Performance Optimizations**
   - Parallel thumbnail generation
   - Build caching
   - Incremental builds
   - Progress tracking

3. **Better Error Handling**
   - Structured logging
   - Detailed error messages
   - Error recovery
   - Validation before processing

4. **Advanced CLI**
   - Verbose/debug modes
   - Dry-run mode
   - Progress indicators
   - Better help messages

5. **Code Quality**
   - Type hints
   - Better organization
   - Comprehensive documentation
   - Modern Python practices

---

## 📦 Installation

### Basic Installation

```bash
cd /Users/steven/simplegallery/2.1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### With Enhanced Features

```bash
pip install -r requirements.txt
pip install torch torchvision pytesseract  # Optional AI features
pip install tqdm rich  # Optional progress bars
```

---

## 🎯 Quick Start

### Initialize a Gallery

```bash
python -m simplegallery.gallery_init -p /path/to/gallery --use-defaults
```

### Build the Gallery

```bash
# Standard build
python -m simplegallery.gallery_build -p /path/to/gallery

# With verbose logging
python -m simplegallery.gallery_build -p /path/to/gallery -v

# Dry run (test without making changes)
python -m simplegallery.gallery_build -p /path/to/gallery --dry-run

# Disable caching
python -m simplegallery.gallery_build -p /path/to/gallery --no-cache

# Single-threaded mode
python -m simplegallery.gallery_build -p /path/to/gallery --no-parallel
```

### Build Large Gallery (2,500+ images)

```bash
# Large gallery with search and pagination
python -m simplegallery.large_gallery_build -p /path/to/gallery

# Custom images per page
python -m simplegallery.large_gallery_build -p /path/to/gallery --images-per-page 75

# With albums
python -m simplegallery.large_gallery_build -p /path/to/gallery --enable-albums
```

---

## 🔧 New CLI Options

### gallery-build

- `-v, --verbose` - Enable verbose/debug logging
- `--no-cache` - Disable build caching
- `--no-parallel` - Disable parallel processing
- `--dry-run` - Test configuration without making changes

### gallery-init

- `-v, --verbose` - Enable verbose logging
- `--wizard` - Run interactive configuration wizard

---

## 📊 Performance Improvements

### Parallel Processing

2.1 uses parallel processing for thumbnail generation, significantly speeding up builds for large galleries.

**Before (2.0):** Sequential processing  
**After (2.1):** Parallel processing (up to 8x faster on multi-core systems)

### Build Caching

Only processes changed files, making rebuilds much faster.

**First build:** Full processing  
**Subsequent builds:** Only changed files processed

---

## 🎨 Configuration Enhancements

### Auto-Detection

- Parent folder name as title
- Smart defaults
- Path validation
- Configuration migration

### Validation

- Pre-build validation
- Clear error messages
- Suggestions for fixes
- Configuration schema checking

---

## 📝 Logging

### Verbose Mode

```bash
python -m simplegallery.gallery_build -p /path/to/gallery -v
```

Shows detailed debug information including:
- Configuration details
- Processing steps
- Performance metrics
- File operations

### Standard Mode

Clean, user-friendly output with progress indicators.

---

## 🔍 What's Different from 2.0?

| Feature | 2.0 | 2.1 |
|---------|-----|-----|
| **Parallel Processing** | ❌ | ✅ |
| **Build Caching** | ❌ | ✅ |
| **Configuration Validation** | ⚠️ Basic | ✅ Advanced |
| **Error Handling** | ⚠️ Basic | ✅ Enhanced |
| **Logging** | ⚠️ Simple | ✅ Structured |
| **CLI Options** | ⚠️ Limited | ✅ Rich |
| **Type Hints** | ❌ | ✅ |
| **Documentation** | ⚠️ Basic | ✅ Comprehensive |

---

## 🚀 Migration from 2.0

2.1 is **fully backward compatible** with 2.0:

1. Copy your gallery to a new location (optional)
2. Use 2.1 build script
3. Configuration automatically migrates
4. All features work as before

**No breaking changes!**

---

## 📚 Documentation

- **IMPROVEMENTS_2.1.md** - Detailed improvements list
- **CHANGELOG.md** - Version history
- **LARGE_GALLERY_GUIDE.md** - Guide for large galleries (2,500+ images)
- **LARGE_GALLERY_FEATURES.md** - Large gallery features overview

---

## 🎯 Best Practices

1. **Use caching** for faster rebuilds (enabled by default)
2. **Enable parallel processing** for large galleries (enabled by default)
3. **Use verbose mode** when troubleshooting
4. **Run dry-run** before important builds
5. **Keep gallery.json** in version control

---

## 💡 Tips

- **Large galleries:** Use `--no-parallel` if you experience memory issues
- **Debugging:** Always use `-v` for verbose output
- **Testing:** Use `--dry-run` to validate configuration
- **Performance:** Keep `cache_enabled: true` for faster rebuilds

---

**SimpleGallery 2.1** - *Advanced. Fast. Reliable.* 🚀

