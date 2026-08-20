#!/usr/bin/env python3
"""
Simple Interactive Image Upscaler
Easy-to-use script for upscaling images with different aspect ratios
"""

import io
import os
from pathlib import Path

from PIL import Image, ImageOps


def get_aspect_ratio_choice():
    """Get user's aspect ratio choice"""
    print("\n📐 Choose aspect ratio:")
    print("1. 16:9 (Widescreen)")
    print("2. 9:16 (Portrait)")
    print("3. 1:1 (Square)")
    print("4. 4:3 (Standard)")
    print("5. 3:4 (Portrait Standard)")
    print("6. 3:2 (Photo)")
    print("7. 2:3 (Portrait Photo)")
    print("8. 21:9 (Ultrawide)")
    print("9. 5:4 (Classic)")
    
    while True:
        choice = input("\nEnter choice (1-9): ").strip()
        ratios = {
            '1': (16, 9, '16:9'),
            '2': (9, 16, '9:16'),
            '3': (1, 1, '1:1'),
            '4': (4, 3, '4:3'),
            '5': (3, 4, '3:4'),
            '6': (3, 2, '3:2'),
            '7': (2, 3, '2:3'),
            '8': (21, 9, '21:9'),
            '9': (5, 4, '5:4'),
        }
        if choice in ratios:
            return ratios[choice]
        print("Invalid choice. Please enter 1-9.")

def get_resize_method():
    """Get user's resize method choice"""
    print("\n🎨 Choose resize method:")
    print("1. Crop (recommended) - Crop to fit ratio, may lose some content")
    print("2. Pad - Add white padding to fit ratio, keeps all content")
    print("3. Stretch - Stretch to fit ratio, may distort image")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        methods = {
            '1': 'crop',
            '2': 'pad', 
            '3': 'stretch'
        }
        if choice in methods:
            return methods[choice]
        print("Invalid choice. Please enter 1-3.")

def calculate_dimensions(width_ratio, height_ratio, target_dpi=300):
    """Calculate optimal dimensions for the aspect ratio"""
    base_size = 2000
    
    if width_ratio >= height_ratio:
        # Landscape or square
        width = min(4000, base_size * width_ratio)
        height = int(width * height_ratio / width_ratio)
    else:
        # Portrait
        height = min(4000, base_size * height_ratio)
        width = int(height * width_ratio / height_ratio)
    
    return width, height

def resize_image(image, target_width, target_height, method='crop'):
    """Resize image to target dimensions"""
    original_width, original_height = image.size
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height
    
    if method == 'crop':
        # Crop to fit target ratio
        if original_ratio > target_ratio:
            # Image is wider - crop width
            new_width = int(original_height * target_ratio)
            left = (original_width - new_width) // 2
            image = image.crop((left, 0, left + new_width, original_height))
        elif original_ratio < target_ratio:
            # Image is taller - crop height
            new_height = int(original_width / target_ratio)
            top = (original_height - new_height) // 2
            image = image.crop((0, top, original_width, top + new_height))
        
        return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    elif method == 'pad':
        # Pad to fit target ratio
        if original_ratio > target_ratio:
            # Image is wider - pad height
            new_height = int(original_width / target_ratio)
            padding = (new_height - original_height) // 2
            image = ImageOps.expand(image, (0, padding, 0, padding), fill='white')
        elif original_ratio < target_ratio:
            # Image is taller - pad width
            new_width = int(original_height * target_ratio)
            padding = (new_width - original_width) // 2
            image = ImageOps.expand(image, (padding, 0, padding, 0), fill='white')
        
        return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    else:  # stretch
        return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

def optimize_file_size(image, max_size_mb=9.0):
    """Optimize image to fit within file size limit"""
    max_size_bytes = max_size_mb * 1024 * 1024
    quality = 95
    
    # Convert to RGB if needed
    if image.mode in ('RGBA', 'LA', 'P'):
        image = image.convert('RGB')
    
    # Test different quality levels
    for test_quality in range(95, 20, -5):
        temp_buffer = io.BytesIO()
        image.save(temp_buffer, format='JPEG', quality=test_quality, optimize=True)
        temp_size = temp_buffer.tell()
        
        if temp_size <= max_size_bytes:
            quality = test_quality
            break
    
    return image, quality

def upscale_single_image(input_path, output_path, width_ratio, height_ratio, method='crop'):
    """Upscale a single image"""
    try:
        with Image.open(input_path) as image:
            # Convert to RGB if needed
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Calculate target dimensions
            target_width, target_height = calculate_dimensions(width_ratio, height_ratio)
            
            # Resize image
            resized_image = resize_image(image, target_width, target_height, method)
            
            # Optimize file size
            optimized_image, quality = optimize_file_size(resized_image)
            
            # Save with 300 DPI
            optimized_image.save(output_path, format='JPEG', quality=quality, 
                               optimize=True, dpi=(300, 300))
            
            file_size = os.path.getsize(output_path)
            
            return {
                'success': True,
                'original_size': image.size,
                'new_size': optimized_image.size,
                'file_size_mb': file_size / (1024 * 1024),
                'quality': quality
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    print("🖼️  IMAGE UPSCALER")
    print("=" * 50)
    print("Upscales images to 300 DPI with various aspect ratios")
    print("Keeps file size under 9MB")
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"\n📁 Working directory: {current_dir}")
    
    # Get aspect ratio
    width_ratio, height_ratio, ratio_name = get_aspect_ratio_choice()
    print(f"Selected: {ratio_name}")
    
    # Get resize method
    method = get_resize_method()
    print(f"Method: {method}")
    
    # Get file pattern
    pattern = input("\n📄 File pattern (e.g., *.jpg, *.png, or specific filename): ").strip()
    if not pattern:
        pattern = "*.jpg"
    
    # Find files
    files = list(Path(current_dir).glob(pattern))
    
    if not files:
        print(f"❌ No files found matching '{pattern}'")
        return
    
    print(f"\n📊 Found {len(files)} files to process")
    
    # Create output directory
    output_dir = f"upscaled_{ratio_name.replace(':', 'x')}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Process files
    successful = 0
    failed = 0
    
    print("\n🔄 Processing files...")
    print("=" * 50)
    
    for i, file_path in enumerate(files, 1):
        output_path = Path(output_dir) / f"upscaled_{file_path.name}"
        
        print(f"[{i}/{len(files)}] {file_path.name}...")
        
        result = upscale_single_image(file_path, output_path, width_ratio, height_ratio, method)
        
        if result['success']:
            successful += 1
            print(f"  ✅ {result['new_size']} @ {result['quality']}% quality, {result['file_size_mb']:.2f}MB")
        else:
            failed += 1
            print(f"  ❌ Error: {result['error']}")
    
    # Summary
    print("\n🎉 PROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Total files: {len(files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output directory: {output_dir}")
    
    if successful > 0:
        print("\n💡 Tips:")
        print("  • Images are saved at 300 DPI for print quality")
        print("  • File sizes are optimized to stay under 9MB")
        print("  • Original files are preserved")
        print(f"  • Check the '{output_dir}' folder for results")

if __name__ == "__main__":
    main()