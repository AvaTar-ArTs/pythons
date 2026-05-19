# Virtual Environment Setup - SimpleGallery 2.0

## ✅ Virtual Environment Created

A Python virtual environment has been created for SimpleGallery 2.0.

**Location:** `/Users/steven/simplegallery/2.0/venv/`

---

## 🚀 Quick Start

### Activate the Environment

**Option 1: Using the activation script**
```bash
cd /Users/steven/simplegallery/2.0
source activate.sh
```

**Option 2: Manual activation**
```bash
cd /Users/steven/simplegallery/2.0
source venv/bin/activate
```

**Option 3: For zsh/fish**
```bash
cd /Users/steven/simplegallery/2.0
source venv/bin/activate.fish  # fish shell
```

### Deactivate

```bash
deactivate
```

---

## 📦 Installed Dependencies

### Core Dependencies (Required)
- ✅ `jinja2>=3.0.0` - Template engine
- ✅ `Pillow>=9.0.0` - Image processing
- ✅ `opencv-python>=4.5.0` - Video/image processing
- ✅ `selenium>=4.0.0` - Web automation

### Enhanced Features (Optional)
To enable AI features, install additional dependencies:

```bash
source venv/bin/activate
pip install torch torchvision pytesseract
```

---

## 🧪 Verify Installation

```bash
source venv/bin/activate
python -c "import cv2, PIL, jinja2, selenium; print('✅ All dependencies installed!')"
```

---

## 📝 Usage Examples

### Standard Gallery

```bash
source venv/bin/activate
python -m simplegallery.gallery_init -p /path/to/gallery --use-defaults
python -m simplegallery.gallery_build -p /path/to/gallery
```

### Enhanced Gallery

```bash
source venv/bin/activate
python -m simplegallery.gallery_init -p /path/to/gallery --use-defaults
python -m simplegallery.enhanced_gallery_build --enhanced -p /path/to/gallery
```

---

## 🔧 Troubleshooting

### Import Errors

If you see import errors, ensure the virtual environment is activated:

```bash
source venv/bin/activate
which python  # Should show venv/bin/python
```

### Missing Dependencies

Reinstall dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Python Path Issues

The `activate.sh` script automatically sets `PYTHONPATH`. If you're using manual activation:

```bash
export PYTHONPATH="/Users/steven/simplegallery/2.0:$PYTHONPATH"
```

---

## 📊 Environment Info

- **Python Version:** Check with `python --version`
- **Virtual Environment:** `venv/` directory
- **Dependencies:** See `requirements.txt`
- **Activation Script:** `activate.sh`

---

## 💡 Tips

1. **Always activate** the virtual environment before using SimpleGallery 2.0
2. **Use the activation script** (`activate.sh`) for convenience
3. **Keep dependencies updated** with `pip install -r requirements.txt --upgrade`
4. **Install AI dependencies** only if you need enhanced features

---

**Happy coding!** 🚀

