# ⚡ Quick Reference: Image Upscaling Module

## 🎯 At a Glance

- **Total Scripts:** 38
- **Lines of Code:** ~8,500
- **Primary Purpose:** Batch image upscaling with aspect ratio conversion
- **Platform:** macOS (primary), Cross-platform (secondary)
- **Status:** Functional but needs consolidation

---

## 🚀 Best Scripts to Use

### **For Production Use:**

1. **`improved_batch_upscaler_2_1.py`** ⭐⭐⭐
   - Best error handling
   - Progress tracking
   - Resume capability
   - Comprehensive logging

2. **`fixed_batch_upscaler_1.py`** ⭐⭐
   - Correct sips syntax
   - Reliable batch processing
   - Good for macOS

3. **`enhanced_9mbs.py`** ⭐⭐
   - Cross-platform (PIL)
   - Good aspect ratio support
   - Reliable processing

---

## 📐 Supported Aspect Ratios

```python
16:9  # Landscape/Video
9:16  # Portrait/Mobile
1:1   # Square/Instagram
4:3   # Classic
3:4   # Portrait Classic
3:2   # Photo
2:3   # Portrait Photo
```

---

## ⚙️ Common Configuration

```python
max_file_size_mb = 9.0      # Target file size
target_dpi = 300             # Print quality
base_size = 2000             # Base dimension
max_dimension = 4000          # Maximum dimension
batch_size = 5               # Images per batch
```

---

## 🔧 Quick Commands

### **Batch Upscaling (macOS)**
```bash
python fixed_batch_upscaler_1.py
```

### **Batch Upscaling (Cross-platform)**
```bash
python enhanced_9mbs.py
```

### **Advanced Batch Processing**
```bash
python improved_batch_upscaler_2_1.py
```

### **Gallery Generation**
```bash
python enhanced_batch_gallery_generator.py --pictures-path /path/to/images
```

---

## 📦 Dependencies

### **Required:**
- Python 3.8+
- Pillow (PIL) >= 10.0.0

### **Optional:**
- tqdm (progress bars)
- requests (API integration)
- jinja2 (gallery templates)

### **macOS Only:**
- sips (built-in system tool)

---

## 🎨 Processing Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **Crop** | Centers and crops to fit | Most common, preserves quality |
| **Pad** | Adds borders | When you need exact ratio |
| **Stretch** | Distorts to fit | Rarely used |

---

## ⚠️ Common Issues

### **Issue: "sips command not found"**
**Solution:** Use PIL-based scripts (`enhanced_9mbs.py`)

### **Issue: "Module 'common' not found"**
**Solution:** Create `common.py` or use different script

### **Issue: File size too large**
**Solution:** Scripts auto-optimize, but check quality settings

### **Issue: Out of memory**
**Solution:** Reduce batch size, process fewer images at once

---

## 📊 Performance Tips

1. **Use sips on macOS** - Faster than PIL
2. **Reduce batch size** - Lower memory usage
3. **Process in stages** - Handle large collections incrementally
4. **Use resume capability** - `improved_batch_upscaler_2_1.py` supports this

---

## 🔍 File Naming Patterns

- `*_batch_*.py` - Batch processing scripts
- `*_upscaler*.py` - Upscaling utilities
- `enhanced_*.py` - Enhanced versions
- `*_gallery*.py` - Gallery generation
- `*_vid*.py` - Video processing

---

## 📝 Quick Troubleshooting

| Problem | Quick Fix |
|--------|-----------|
| Script fails silently | Use `improved_batch_upscaler_2_1.py` (has logging) |
| Images not processing | Check file permissions, format support |
| Slow processing | Reduce batch size, check system resources |
| Wrong aspect ratio | Verify ratio calculation in script |
| File size too large | Script should auto-optimize, check quality range |

---

## 🎯 Use Case Matrix

| Use Case | Recommended Script |
|----------|-------------------|
| **Quick batch upscale** | `fixed_batch_upscaler_1.py` |
| **Cross-platform** | `enhanced_9mbs.py` |
| **Production workflow** | `improved_batch_upscaler_2_1.py` |
| **Gallery creation** | `enhanced_batch_gallery_generator.py` |
| **Single image** | `simple_upscaler.py` |
| **API integration** | `upscale_file.py` |

---

## 📚 Documentation Files

- **`ADVANCED_CONTENT_ANALYSIS.md`** - Comprehensive analysis
- **`REFACTORING_ROADMAP.md`** - Improvement plan
- **`DEPENDENCY_ANALYSIS.md`** - Dependency details
- **`QUICK_REFERENCE.md`** - This file

---

## 🔗 Key Functions

### **Dimension Calculation**
```python
calculate_target_dimensions(width_ratio, height_ratio, base_size=2000)
```

### **Resize to Aspect Ratio**
```python
resize_to_aspect_ratio(input_path, output_path, target_width, target_height)
```

### **Optimize File Size**
```python
optimize_file_size(image_path, max_size_mb=9.0)
```

---

## 💡 Pro Tips

1. **Start with small batch** - Test with 5-10 images first
2. **Check output directories** - Scripts create `upscaled_*` folders
3. **Monitor file sizes** - Verify they're under 9MB
4. **Use progress tracking** - Install `tqdm` for better UX
5. **Backup originals** - Scripts modify/create new files

---

## 🚨 Important Notes

- ⚠️ **macOS scripts** require `sips` (built-in)
- ⚠️ **Some scripts** have missing dependencies
- ⚠️ **Platform compatibility** varies by script
- ✅ **Most scripts** are functional and tested
- ✅ **Batch processing** is well-supported

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** Analysis Complete ✅

