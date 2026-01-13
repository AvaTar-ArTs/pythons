#!/usr/bin/env python3
"""
Batch Image Upscaler
Processes all images in the current directory with different aspect ratios
"""

import io
import os
from pathlib import Path

from PIL import Image, ImageOps


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

def upscale_image(input_path, output_path, width_ratio, height_ratio, method='crop'):
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

def process_all_ratios():
    """Process all images with multiple aspect ratios"""
    
    # Define aspect ratios to process
    ratios = {
        '16x9': (16, 9, '16:9'),
        '9x16': (9, 16, '9:16'),
        '1x1': (1, 1, '1:1'),
        '4x3': (4, 3, '4:3'),
        '3x4': (3, 4, '3:4'),
        '3x2': (3, 2, '3:2'),
        '2x3': (2, 3, '2:3'),
    }
    
    # Find all JPG files
    current_dir = Path()
    image_files = list(current_dir.glob('*.jpg'))
    
    if not image_files:
        print("❌ No JPG files found in current directory")
        return
    
    print("🖼️  BATCH UPSCALER")
    print("=" * 50)
    print(f"Found {len(image_files)} JPG files")
    print(f"Processing with {len(ratios)} aspect ratios")
    print("=" * 50)
    
    total_processed = 0
    total_successful = 0
    
    for ratio_name, (width_ratio, height_ratio, display_name) in ratios.items():
        print(f"\n📐 Processing {display_name}...")
        
        # Create output directory
        output_dir = f"upscaled_{ratio_name}"
        os.makedirs(output_dir, exist_ok=True)
        
        successful = 0
        failed = 0
        
        for i, file_path in enumerate(image_files, 1):
            output_path = Path(output_dir) / f"upscaled_{file_path.name}"
            
            print(f"  [{i}/{len(image_files)}] {file_path.name}...", end=" ")
            
            result = upscale_image(file_path, output_path, width_ratio, height_ratio, 'crop')
            
            if result['success']:
                successful += 1
                total_successful += 1
                print(f"✅ {result['file_size_mb']:.1f}MB")
            else:
                failed += 1
                print(f"❌ {result['error']}")
            
            total_processed += 1
        
        print(f"  📊 {display_name}: {successful} successful, {failed} failed")
    
    # Final summary
    print("\n🎉 BATCH PROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Total images processed: {total_processed}")
    print(f"Total successful: {total_successful}")
    print(f"Total failed: {total_processed - total_successful}")
    print("\n📁 Output directories created:")
    for ratio_name in ratios.keys():
        print(f"  • upscaled_{ratio_name}/")
    
    print("\n💡 All images are:")
    print("  • 300 DPI for print quality")
    print("  • Under 9MB file size")
    print("  • Optimized for web and print use")

if __name__ == "__main__":
    process_all_ratios()