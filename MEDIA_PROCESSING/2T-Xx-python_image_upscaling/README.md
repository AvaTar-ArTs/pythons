# 🖼️ Image Upscaling Toolkit

A comprehensive, refactored image processing toolkit for batch upscaling, aspect ratio conversion, and file size optimization.

## ✨ Features

- **Batch Processing**: Process multiple images with multiple aspect ratios
- **Aspect Ratio Support**: 9 standard aspect ratios (16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4)
- **File Size Optimization**: Automatic optimization to stay under 9MB (configurable)
- **Cross-Platform**: Works on macOS (sips), Linux, and Windows (PIL/Pillow)
- **Unified CLI**: Single command-line interface for all operations
- **Progress Tracking**: Visual progress bars for batch operations
- **Caching**: Smart caching to avoid reprocessing
- **Parallel Processing**: Multiprocessing support for faster batch operations

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install Pillow click tqdm

# Or use requirements.txt (coming soon)
```

### Basic Usage

#### Command Line Interface

```bash
# Batch process images with multiple aspect ratios
python -m cli.upscale_cli batch -i ./images -a 16x9 -a 1x1

# Simple upscale
python -m cli.upscale_cli upscale -i image.jpg -o upscaled.jpg --scale 2

# Convert web images
python -m cli.upscale_cli convert -i ./webp_images --format webp --target JPEG

# Show system info
python -m cli.upscale_cli info
```

#### Python API

```python
from core import UpscaleConfig, resize_to_aspect_ratio, optimize_file_size

# Create configuration
config = UpscaleConfig(max_file_size_mb=9.0, target_dpi=300)

# Resize image to aspect ratio
success, message = resize_to_aspect_ratio(
    "input.jpg",
    "output.jpg",
    target_width=3200,
    target_height=1800,
    method='crop'
)

# Optimize file size
opt_success, opt_message = optimize_file_size("output.jpg", max_size_mb=9.0)
```

## 📁 Project Structure

```
image_upscaling/
├── core/                    # Core utilities
│   ├── __init__.py         # Package exports
│   ├── config.py           # Configuration management
│   ├── exceptions.py        # Custom exceptions
│   ├── image_utils.py      # Image processing utilities
│   ├── cache.py            # Caching layer
│   └── parallel.py         # Parallel processing
├── cli/                     # Command-line interface
│   └── upscale_cli.py      # Unified CLI
├── batch_upscaler_v2.py    # Batch processing script
├── simple_upscaler_v2.py    # Simple upscaling script
├── web_upscaler_v2.py      # Web image conversion
└── README.md               # This file
```

## 🎯 Core Modules

### Configuration (`core/config.py`)

```python
from core import UpscaleConfig

config = UpscaleConfig(
    max_file_size_mb=9.0,      # Maximum file size
    target_dpi=300,             # Target DPI
    base_size=2000,             # Base dimension size
    max_dimension=4000,         # Maximum dimension
    quality_range=(90, 20),     # Quality range for optimization
    quality_step=10,            # Quality reduction step
    batch_size=5                # Batch processing size
)

# Get aspect ratio
width, height, name = config.get_aspect_ratio('16x9')
```

### Image Utilities (`core/image_utils.py`)

```python
from core import (
    get_image_processor,      # Auto-detect processor
    get_image_dimensions,      # Get image size
    calculate_target_dimensions,  # Calculate target size
    resize_to_aspect_ratio,    # Resize with aspect ratio
    optimize_file_size,        # Optimize file size
)

# Auto-detect processor (sips or PIL)
processor = get_image_processor()

# Get dimensions
width, height = get_image_dimensions("image.jpg")

# Calculate target dimensions
target_w, target_h = calculate_target_dimensions(16, 9, base_size=2000)

# Resize with aspect ratio
success, message = resize_to_aspect_ratio(
    "input.jpg", "output.jpg",
    target_width=3200, target_height=1800,
    method='crop'  # or 'pad' or 'stretch'
)

# Optimize file size
success, message = optimize_file_size("image.jpg", max_size_mb=9.0)
```

### Caching (`core/cache.py`)

```python
from core import cache_image_result, get_cached_result

# Cache a result
cache_image_result(
    "image.jpg",
    "upscale",
    {"width": 3200, "height": 1800, "file_size_mb": 8.5},
    params={"scale": 2}
)

# Get cached result
cached = get_cached_result("image.jpg", "upscale", params={"scale": 2})
if cached:
    print("Using cached result!")
```

### Parallel Processing (`core/parallel.py`)

```python
from core import process_images_parallel

def process_image(image_path):
    # Your processing logic
    return (True, {"file_size_mb": 8.5})

# Process images in parallel
results = process_images_parallel(
    image_files=["img1.jpg", "img2.jpg", "img3.jpg"],
    process_func=process_image,
    max_workers=4,
    show_progress=True
)
```

## 📐 Aspect Ratios

Supported aspect ratios:

- `16x9` - Widescreen/Video (16:9)
- `9x16` - Portrait/Mobile (9:16)
- `1x1` - Square/Instagram (1:1)
- `4x3` - Classic (4:3)
- `3x4` - Portrait Classic (3:4)
- `3x2` - Photo (3:2)
- `2x3` - Portrait Photo (2:3)
- `21x9` - Ultrawide (21:9)
- `5x4` - Classic (5:4)

## 🔧 Configuration Options

### UpscaleConfig

| Option | Default | Description |
|--------|---------|-------------|
| `max_file_size_mb` | 9.0 | Maximum file size in MB |
| `target_dpi` | 300 | Target DPI for output |
| `base_size` | 2000 | Base dimension for calculations |
| `max_dimension` | 4000 | Maximum width or height |
| `quality_range` | (90, 20) | Quality range for optimization |
| `quality_step` | 10 | Quality reduction step size |
| `batch_size` | 5 | Images per batch |

## 🛠️ Resize Methods

- **crop**: Crop image to fit aspect ratio (centered)
- **pad**: Add white padding to fit aspect ratio
- **stretch**: Stretch image to fit (may distort)

## 📊 Performance

- **Sequential Processing**: ~1-2 images/second
- **Parallel Processing**: ~4-8 images/second (4 workers)
- **Caching**: Instant for cached results
- **File Size Optimization**: Automatic quality reduction

## 🐛 Error Handling

All functions use standardized exceptions:

```python
from core import (
    ImageProcessingError,
    DimensionError,
    ResizeError,
    OptimizationError,
    ProcessorNotFoundError,
    ImageFileNotFoundError,
)
```

## 📝 Examples

### Batch Process with Multiple Aspect Ratios

```python
from batch_upscaler_v2 import process_images_in_batches
from core import UpscaleConfig

config = UpscaleConfig(
    max_file_size_mb=9.0,
    batch_size=10
)

process_images_in_batches("./images", config)
```

### Simple Upscale

```python
from simple_upscaler_v2 import process_directory
from core import UpscaleConfig

config = UpscaleConfig()
process_directory("./input", "./output", config)
```

### Web Image Conversion

```python
from web_upscaler_v2 import process_directory
from core import UpscaleConfig

config = UpscaleConfig()
process_directory(
    "./webp_images",
    source_format='webp',
    target_format='JPEG',
    config=config,
    remove_original=False
)
```

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/

# Run with coverage
pytest --cov=core tests/
```

## 📚 Documentation

- **API Documentation**: See docstrings in core modules
- **Advanced Analysis**: See `ADVANCED_CONTENT_ANALYSIS.md`
- **Refactoring Roadmap**: See `REFACTORING_ROADMAP.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`

## 🤝 Contributing

This is a refactored codebase. When adding features:

1. Use core utilities from `core/` module
2. Follow existing patterns
3. Add type hints
4. Update documentation
5. Add tests

## 📄 License

[Your License Here]

## 🎉 Status

- ✅ Phase 1: Foundation - COMPLETE
- ✅ Phase 2: Consolidation - COMPLETE
- ✅ Phase 3: Enhancement - COMPLETE
- ⏳ Phase 4: Documentation - IN PROGRESS
- ⏳ Phase 5: Testing - PLANNED

---

**Version**: 2.0.0
**Last Updated**: 2024

