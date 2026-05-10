# Changelog - SimpleGallery 2.0

## [2.0.0] - 2024-11-25

### 🎉 Major Release

#### Added
- **AI-Powered Content Analysis**
  - Object detection using ResNet and CLIP
  - Scene classification
  - Activity recognition
  - Complexity scoring

- **Enhanced Metadata Extraction**
  - Color palette analysis
  - Composition analysis
  - Face detection
  - Text extraction (OCR)
  - Quality scoring (A-D grades)

- **Enhanced UI**
  - Modern dark theme
  - Real-time search
  - Advanced filtering
  - Statistics dashboard
  - Quality badges
  - Content tags

- **New Build System**
  - `enhanced_gallery_build.py` for AI-powered galleries
  - Unified build interface
  - Enhanced template support

#### Changed
- **Modernized Selenium APIs**
  - Updated to Selenium 4.x API
  - Uses `By.XPATH`, `By.CLASS_NAME`
  - Uses `Service()` instead of `executable_path`

- **Security Improvements**
  - Environment variable support for credentials
  - Optional security features (right-click blocking)
  - Secure credential handling

- **Code Quality**
  - Consolidated build scripts
  - Eliminated code duplication
  - Improved error handling
  - Better template structure

#### Fixed
- Deprecated Selenium API usage
- Hardcoded credentials security issue
- Template duplication
- Background photo handling
- Empty images handling

#### Improved
- Template error handling
- Conditional rendering
- Code organization
- Documentation

---

## Migration Notes

### From 1.x to 2.0

1. **No Breaking Changes** - Existing galleries work as-is
2. **Enhanced Features** - Opt-in via `--enhanced` flag
3. **API Compatibility** - All existing APIs maintained
4. **Template Compatibility** - Standard templates unchanged

### Upgrading

```bash
# Standard gallery (no changes needed)
python -m simplegallery.gallery_build -p /path/to/gallery

# Enhanced gallery (new features)
python -m simplegallery.enhanced_gallery_build --enhanced -p /path/to/gallery
```

---

## Future Roadmap

### Planned Features
- Video analysis
- Audio analysis
- 3D analysis
- Style transfer
- Emotion recognition
- Location recognition

### API Improvements
- REST API
- GraphQL support
- WebSocket updates
- Batch API

---

*For detailed feature documentation, see `ENHANCED_FEATURES.md`*

