# Changelog - SimpleGallery 2.1

All notable changes to SimpleGallery 2.1 will be documented in this file.

---

## [2.1.0] - 2024-11-25

### 🚀 Added

#### Configuration System
- Configuration validation with schema checking
- Automatic configuration migration from 2.0
- Smart defaults and auto-detection
- Environment variable support
- Configuration wizard (interactive setup)

#### Performance
- Parallel thumbnail generation (multiprocessing)
- Build caching system
- Incremental builds (only process changed files)
- Progress tracking and reporting
- Optimized image processing

#### Error Handling
- Structured logging system
- Enhanced error messages with suggestions
- Pre-build validation
- Error recovery mechanisms
- Detailed debug information

#### CLI Enhancements
- Verbose/debug mode (`-v`)
- Dry-run mode (`--dry-run`)
- Cache control (`--no-cache`)
- Parallel processing control (`--no-parallel`)
- Better help messages and documentation

#### Code Quality
- Type hints throughout codebase
- Better code organization
- Comprehensive docstrings
- Modern Python 3.10+ features
- Improved error handling

### 🔧 Changed

- **Configuration:** Enhanced with validation and migration
- **Build Process:** Faster with parallel processing and caching
- **Logging:** Structured logging instead of simple print statements
- **Error Messages:** More helpful with suggestions
- **CLI:** More options and better UX

### 🐛 Fixed

- Configuration validation issues
- Error handling edge cases
- Path resolution problems
- Template loading issues

### 📚 Documentation

- Comprehensive README
- Improvement documentation
- Migration guide
- Best practices guide

---

## Migration from 2.0

2.1 is **fully backward compatible** with 2.0. Simply use the 2.1 build script - configuration will automatically migrate.

---

*For detailed improvements, see IMPROVEMENTS_2.1.md*

