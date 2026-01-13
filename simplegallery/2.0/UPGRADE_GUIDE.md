# SimpleGallery 2.0 Upgrade Guide

## 🚀 Upgrading from 1.x to 2.0

SimpleGallery 2.0 is **fully backward compatible** with 1.x. Your existing galleries will work without any changes.

---

## Quick Upgrade

### Option 1: Use 2.0 for New Galleries

Simply use the 2.0 version for new galleries:

```bash
cd /Users/steven/simplegallery/2.0
python -m simplegallery.gallery_init -p /path/to/new/gallery
python -m simplegallery.gallery_build -p /path/to/new/gallery
```

### Option 2: Upgrade Existing Gallery

To add enhanced features to an existing gallery:

```bash
cd /Users/steven/simplegallery/2.0
python -m simplegallery.enhanced_gallery_build \
    --enhanced \
    --ai-analysis \
    -p /path/to/existing/gallery
```

---

## What Changed?

### ✅ Backward Compatible
- All existing galleries work as-is
- Standard build process unchanged
- Template structure maintained
- API compatibility preserved

### 🆕 New Features (Opt-in)
- Enhanced build system
- AI-powered analysis
- Advanced UI
- Search and filtering

### 🔧 Improvements
- Modern Selenium APIs
- Secure credential handling
- Better error handling
- Improved templates

---

## Migration Steps

### 1. Backup Your Gallery

```bash
cp -r /path/to/gallery /path/to/gallery.backup
```

### 2. Test with 2.0

```bash
cd /Users/steven/simplegallery/2.0
python -m simplegallery.gallery_build -p /path/to/gallery
```

### 3. Verify

Open `public/index.html` in your browser to verify everything works.

### 4. (Optional) Enable Enhanced Features

```bash
python -m simplegallery.enhanced_gallery_build \
    --enhanced \
    -p /path/to/gallery
```

---

## Breaking Changes

**None!** SimpleGallery 2.0 is fully backward compatible.

---

## New Dependencies

### Standard Features
No new dependencies required.

### Enhanced Features (Optional)
```bash
pip install torch torchvision pytesseract
```

---

## Configuration Changes

### Standard Gallery
No configuration changes needed.

### Enhanced Gallery
Add to `gallery.json`:

```json
{
  "enhanced": true,
  "ai_analysis": true,
  "content_tags": true,
  "quality_scoring": true,
  "face_detection": true,
  "color_analysis": true,
  "template": "enhanced"
}
```

---

## Troubleshooting

### Import Errors
If you see import errors, ensure you're running from the 2.0 directory:

```bash
cd /Users/steven/simplegallery/2.0
python -m simplegallery.gallery_build -p /path/to/gallery
```

### Template Not Found
Ensure templates are in the correct location:
```
2.0/data/templates/
```

### Enhanced Features Not Working
Install optional dependencies:
```bash
pip install torch torchvision pytesseract
```

---

## Support

For issues or questions:
1. Check `README.md` for documentation
2. Review `ENHANCED_FEATURES.md` for feature details
3. See `CHANGELOG.md` for version history

---

**Happy Upgrading!** 🎉

