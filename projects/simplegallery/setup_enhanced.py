#!/usr/bin/env python3
"""
Setup script for SimpleGallery Enhanced Features
Installs additional dependencies and configures enhanced features
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path


def install_dependencies(optional=False):
    """Install required and optional dependencies"""
    print("Installing SimpleGallery Enhanced Features dependencies...")

    # Core dependencies (always required)
    core_deps = ["opencv-python", "Pillow", "numpy", "scikit-learn", "requests"]

    # Optional AI dependencies
    ai_deps = ["torch", "torchvision", "clip-by-openai", "pytesseract"]

    # Install core dependencies
    print("Installing core dependencies...")
    for dep in core_deps:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ Installed {dep}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {dep}: {e}")

    # Install optional AI dependencies if requested
    if optional:
        print("Installing optional AI dependencies...")
        for dep in ai_deps:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✓ Installed {dep}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {dep}: {e}")
                print(f"  Note: {dep} is optional and can be installed later")
    else:
        print("Skipping optional AI dependencies. Use --ai to install them.")


def create_enhanced_config(gallery_path="."):
    """Create enhanced configuration file"""
    config = {
        "enhanced": True,
        "ai_analysis": True,
        "content_tags": True,
        "quality_scoring": True,
        "face_detection": True,
        "color_analysis": True,
        "template": "enhanced",
        "models": {"resnet": True, "clip": True, "ocr": True, "face_detection": True},
        "confidence_threshold": 0.5,
        "cache_analysis": True,
        "batch_size": 10,
        "max_image_size": 2048,
    }

    config_path = os.path.join(gallery_path, "enhanced_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✓ Created enhanced configuration: {config_path}")
    return config_path


def copy_enhanced_assets(gallery_path="."):
    """Copy enhanced assets to gallery directory"""
    print("Copying enhanced assets...")

    # Get the package directory
    package_dir = Path(__file__).parent

    # Define asset mappings
    assets = {
        "templates/enhanced_index_template.jinja": "templates/",
        "templates/enhanced_gallery_macros.jinja": "templates/",
        "public/css/enhanced-main.css": "public/css/",
        "public/js/enhanced-main.js": "public/js/",
    }

    for src, dst in assets.items():
        src_path = package_dir / "data" / src
        dst_path = os.path.join(gallery_path, dst)

        # Create destination directory if it doesn't exist
        os.makedirs(dst_path, exist_ok=True)

        if src_path.exists():
            import shutil

            shutil.copy2(src_path, os.path.join(dst_path, os.path.basename(src)))
            print(f"✓ Copied {src}")
        else:
            print(f"✗ Asset not found: {src_path}")


def create_sample_gallery(gallery_path="."):
    """Create a sample enhanced gallery"""
    print("Creating sample enhanced gallery...")

    # Create basic gallery structure
    os.makedirs(os.path.join(gallery_path, "public", "images", "photos"), exist_ok=True)
    os.makedirs(
        os.path.join(gallery_path, "public", "images", "thumbnails"), exist_ok=True
    )
    os.makedirs(os.path.join(gallery_path, "templates"), exist_ok=True)

    # Create sample gallery.json
    gallery_config = {
        "images_data_file": "images_data.json",
        "public_path": "public",
        "templates_path": "templates",
        "images_path": "public/images/photos",
        "thumbnails_path": "public/images/thumbnails",
        "thumbnail_height": 160,
        "title": "Enhanced Sample Gallery",
        "description": "A sample gallery showcasing enhanced features",
        "background_photo": "",
        "url": "",
        "background_photo_offset": 30,
        "disable_captions": False,
        "enhanced": True,
        "template": "enhanced",
    }

    gallery_json_path = os.path.join(gallery_path, "gallery.json")
    with open(gallery_json_path, "w") as f:
        json.dump(gallery_config, f, indent=2)

    print(f"✓ Created sample gallery configuration: {gallery_json_path}")


def create_readme(gallery_path="."):
    """Create README for enhanced features"""
    readme_content = """# Enhanced SimpleGallery

This gallery has been enhanced with content-awareness features including:

## Features
- AI-powered content analysis
- Automatic quality scoring
- Face detection and analysis
- Color palette extraction
- Advanced search and filtering
- Modern responsive design

## Usage

### Build the gallery
```bash
python -m simplegallery.enhanced_gallery_build --enhanced --path .
```

### Build with AI features
```bash
python -m simplegallery.enhanced_gallery_build --enhanced --ai-analysis --path .
```

### Build with all features
```bash
python -m simplegallery.enhanced_gallery_build \\
  --enhanced \\
  --ai-analysis \\
  --content-tags \\
  --quality-scoring \\
  --face-detection \\
  --color-analysis \\
  --path .
```

## Configuration

Edit `enhanced_config.json` to customize AI models and analysis settings.

## Documentation

See `ENHANCED_FEATURES.md` for detailed documentation.
"""

    readme_path = os.path.join(gallery_path, "README_ENHANCED.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print(f"✓ Created enhanced README: {readme_path}")


def verify_installation():
    """Verify that enhanced features are properly installed"""
    print("Verifying installation...")

    try:
        # Test imports
        from simplegallery.enhanced_metadata import ContentAnalyzer
        from simplegallery.enhanced_gallery_build import build_enhanced_html

        print("✓ Enhanced modules imported successfully")

        # Test AI analyzer (if available)
        try:
            from simplegallery.ai_content_analyzer import AIContentAnalyzer

            AIContentAnalyzer()
            print("✓ AI analyzer initialized")
        except ImportError:
            print("⚠ AI analyzer not available (optional dependencies not installed)")

        print("✓ Installation verification completed")
        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(
        description="Setup SimpleGallery Enhanced Features"
    )
    parser.add_argument("--path", default=".", help="Gallery path")
    parser.add_argument("--ai", action="store_true", help="Install AI dependencies")
    parser.add_argument("--sample", action="store_true", help="Create sample gallery")
    parser.add_argument("--verify", action="store_true", help="Verify installation")

    args = parser.parse_args()

    print("SimpleGallery Enhanced Features Setup")
    print("=" * 40)

    # Install dependencies
    install_dependencies(optional=args.ai)

    # Create enhanced configuration
    create_enhanced_config(args.path)

    # Copy enhanced assets
    copy_enhanced_assets(args.path)

    # Create sample gallery if requested
    if args.sample:
        create_sample_gallery(args.path)
        create_readme(args.path)

    # Verify installation
    if args.verify:
        verify_installation()

    print("\nSetup completed!")
    print("\nNext steps:")
    print("1. Add your images to public/images/photos/")
    print("2. Run: python -m simplegallery.enhanced_gallery_build --enhanced --path .")
    print("3. Open public/index.html in your browser")

    if not args.ai:
        print("\nNote: Install AI dependencies with --ai for advanced features")


if __name__ == "__main__":
    main()
