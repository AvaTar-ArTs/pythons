# SimpleGallery 2.0 - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Activate Virtual Environment

```bash
cd /Users/steven/simplegallery/2.0
source activate.sh
```

Or manually:
```bash
source venv/bin/activate
```

### Step 2: Create a Gallery

```bash
python -m simplegallery.gallery_init -p /path/to/gallery --use-defaults
```

### Step 3: Build the Gallery

**Standard Gallery:**
```bash
python -m simplegallery.gallery_build -p /path/to/gallery
```

**Enhanced Gallery (with AI features):**
```bash
python -m simplegallery.enhanced_gallery_build \
    --enhanced \
    --ai-analysis \
    -p /path/to/gallery
```

---

## ✅ Verify Installation

```bash
source venv/bin/activate
python -c "import cv2, PIL, jinja2, selenium; print('✅ Ready!')"
```

---

## 📦 Installed Versions

- **OpenCV:** 4.12.0
- **Pillow:** 12.0.0
- **Jinja2:** 3.1.6
- **Selenium:** 4.38.0

---

## 🎯 Next Steps

1. Read `README.md` for full documentation
2. Check `ENHANCED_FEATURES.md` for AI features
3. See `UPGRADE_GUIDE.md` for migration help

---

**You're all set!** 🎉

