#!/usr/bin/env python3
"""
Example script showing how to create a gallery with the desired folder structure
"""

import os
import sys
import subprocess
from pathlib import Path

def create_gallery_structure(gallery_name, source_images_path=None):
    """
    Create a gallery with the structure:
    /path/to/GalleryName/
    ├── public/
    │   ├── css/
    │   ├── js/
    │   ├── images/
    │   │   ├── photos/
    │   │   └── thumbnails/
    │   └── index.html
    ├── templates/
    └── gallery.json
    """
    
    # Create main gallery directory
    gallery_path = Path(gallery_name)
    gallery_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    (gallery_path / "public" / "css").mkdir(parents=True, exist_ok=True)
    (gallery_path / "public" / "js").mkdir(parents=True, exist_ok=True)
    (gallery_path / "public" / "images" / "photos").mkdir(parents=True, exist_ok=True)
    (gallery_path / "public" / "images" / "thumbnails").mkdir(parents=True, exist_ok=True)
    (gallery_path / "templates").mkdir(exist_ok=True)
    
    print(f"Created gallery structure for: {gallery_name}")
    print(f"Gallery path: {gallery_path.absolute()}")
    
    # Copy images if source path provided
    if source_images_path and os.path.exists(source_images_path):
        import shutil
        source_path = Path(source_images_path)
        photos_dir = gallery_path / "public" / "images" / "photos"
        
        # Copy image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.mp4'}
        copied_count = 0
        
        for file_path in source_path.iterdir():
            if file_path.suffix.lower() in image_extensions:
                shutil.copy2(file_path, photos_dir / file_path.name)
                copied_count += 1
        
        print(f"Copied {copied_count} images to photos directory")
    
    # Create gallery.json
    gallery_config = {
        "images_data_file": "images_data.json",
        "public_path": "public",
        "templates_path": "templates",
        "images_path": "public/images/photos",
        "thumbnails_path": "public/images/thumbnails",
        "thumbnail_height": 160,
        "title": gallery_name,
        "description": "",
        "background_photo": "",
        "url": "",
        "background_photo_offset": 30,
        "disable_captions": False,
        "enhanced": True,
        "template": "enhanced"
    }
    
    config_path = gallery_path / "gallery.json"
    import json
    with open(config_path, "w") as f:
        json.dump(gallery_config, f, indent=2)
    
    print(f"Created gallery.json with title: {gallery_name}")
    
    return gallery_path

def build_enhanced_gallery(gallery_path):
    """Build the enhanced gallery"""
    print(f"Building enhanced gallery...")
    
    try:
        # Run the enhanced gallery build
        result = subprocess.run([
            sys.executable, "-m", "simplegallery.enhanced_gallery_build",
            "--enhanced",
            "--path", str(gallery_path)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Gallery built successfully!")
            print(f"Open: {gallery_path / 'public' / 'index.html'}")
        else:
            print(f"✗ Build failed: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Error building gallery: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python create_gallery_example.py <gallery_name> [source_images_path]")
        print("Example: python create_gallery_example.py AvatararTs /path/to/images")
        sys.exit(1)
    
    gallery_name = sys.argv[1]
    source_images_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create gallery structure
    gallery_path = create_gallery_structure(gallery_name, source_images_path)
    
    # Build the gallery
    build_enhanced_gallery(gallery_path)
    
    print(f"\nGallery created at: {gallery_path.absolute()}")
    print(f"Structure:")
    print(f"  {gallery_path}/")
    print(f"  ├── public/")
    print(f"  │   ├── css/")
    print(f"  │   ├── js/")
    print(f"  │   ├── images/")
    print(f"  │   │   ├── photos/")
    print(f"  │   │   └── thumbnails/")
    print(f"  │   └── index.html")
    print(f"  ├── templates/")
    print(f"  └── gallery.json")

if __name__ == "__main__":
    main()