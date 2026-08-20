#!/usr/bin/env python3
"""
Enhanced 9MB Image Processor
Based on the proven 9mbs.py script with added aspect ratio support
Processes images to 300 DPI with various aspect ratios while maintaining file size under 9MB
"""

import os
from pathlib import Path

from PIL import Image, ImageOps

# Set a limit for maximum pixels to avoid decompression bomb error
Image.MAX_IMAGE_PIXELS = 178956970  # Default limit, can be adjusted or removed entirely using 'None'

def is_large_image(image_path):
    """Check if the image is too large based on pixel dimensions."""
    with Image.open(image_path) as img:
        width, height = img.size
        return (width * height) > Image.MAX_IMAGE_PIXELS

def calculate_target_dimensions(width_ratio, height_ratio, base_size=2000):
    """Calculate target dimensions for the aspect ratio"""
    if width_ratio >= height_ratio:
        # Landscape or square
        width = min(4000, base_size * width_ratio)
        height = int(width * height_ratio / width_ratio)
    else:
        # Portrait
        height = min(4000, base_size * height_ratio)
        width = int(height * width_ratio / height_ratio)
    
    return width, height

def resize_to_aspect_ratio(image, target_width, target_height, method='crop'):
    """Resize image to target dimensions while maintaining aspect ratio"""
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

def resize_image_to_max_size(image_path, output_path, max_size_mb=9, aspect_ratio=None, method='crop'):
    """Enhanced version that supports aspect ratios"""
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    target_dpi = (300, 300)  # Set target DPI

    if is_large_image(image_path):
        print(f"Skipping {os.path.basename(image_path)} - Image size exceeds the limit.")
        return False

    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        current_size = os.path.getsize(image_path)
        original_size = img.size

        # If aspect ratio is specified, resize to that ratio first
        if aspect_ratio:
            width_ratio, height_ratio = aspect_ratio
            target_width, target_height = calculate_target_dimensions(width_ratio, height_ratio)
            img = resize_to_aspect_ratio(img, target_width, target_height, method)
            print(f"Resized {os.path.basename(image_path)} to {aspect_ratio[0]}:{aspect_ratio[1]} aspect ratio ({img.size[0]}x{img.size[1]})")

        # Check if we need to resize for file size
        if current_size <= max_size_bytes and not aspect_ratio:
            print(f"{os.path.basename(image_path)} is already under {max_size_mb}MB, no resizing needed.")
            # Still save with proper DPI
            img.save(output_path, format="JPEG", dpi=target_dpi, quality=95, optimize=True)
            return True

        # Optimize file size if needed
        width, height = img.size
        quality = 95
        
        # Try different quality levels to get under size limit
        for test_quality in range(95, 20, -5):
            temp_img = img.copy()
            temp_img.save(output_path, format="JPEG", dpi=target_dpi, quality=test_quality, optimize=True)
            current_size = os.path.getsize(output_path)
            
            if current_size <= max_size_bytes:
                quality = test_quality
                break
        
        # If still too large, resize the image
        if current_size > max_size_bytes:
            reduction_factor = 0.9
            while current_size > max_size_bytes and reduction_factor > 0.1:
                new_width = int(width * reduction_factor)
                new_height = int(height * reduction_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img.save(output_path, format="JPEG", dpi=target_dpi, quality=quality, optimize=True)
                current_size = os.path.getsize(output_path)
                reduction_factor -= 0.1
                
                if reduction_factor <= 0.1:
                    print(f"Cannot resize {os.path.basename(image_path)} further without significant quality loss.")
                    break

        final_size = os.path.getsize(output_path)
        print(f"Processed {os.path.basename(image_path)}: {original_size} → {img.size} @ {quality}% quality, {final_size / (1024 * 1024):.2f} MB")
        return True

def process_images_with_aspect_ratios(directory, max_size_mb=9):
    """Process all images with multiple aspect ratios"""
    
    # Define aspect ratios to process
    aspect_ratios = {
        '16x9': (16, 9, '16:9'),
        '9x16': (9, 16, '9:16'),
        '1x1': (1, 1, '1:1'),
        '4x3': (4, 3, '4:3'),
        '3x4': (3, 4, '3:4'),
        '3x2': (3, 2, '3:2'),
        '2x3': (2, 3, '2:3'),
    }
    
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Find all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(Path(directory).glob(ext))
    
    if not image_files:
        print("No image files found in the directory.")
        return

    print("🖼️  ENHANCED 9MB IMAGE PROCESSOR")
    print("=" * 50)
    print(f"Found {len(image_files)} image files")
    print(f"Processing with {len(aspect_ratios)} aspect ratios")
    print("=" * 50)

    total_processed = 0
    total_successful = 0

    for ratio_name, (width_ratio, height_ratio, display_name) in aspect_ratios.items():
        print(f"\n📐 Processing {display_name}...")
        
        # Create output directory
        output_dir = os.path.join(directory, f"upscaled_{ratio_name}")
        os.makedirs(output_dir, exist_ok=True)
        
        successful = 0
        failed = 0
        
        for i, image_path in enumerate(image_files, 1):
            output_path = os.path.join(output_dir, f"upscaled_{image_path.name}")
            
            print(f"  [{i}/{len(image_files)}] {image_path.name}...", end=" ")
            
            try:
                success = resize_image_to_max_size(
                    str(image_path), 
                    output_path, 
                    max_size_mb, 
                    (width_ratio, height_ratio), 
                    'crop'
                )
                
                if success:
                    successful += 1
                    total_successful += 1
                    print("✅")
                else:
                    failed += 1
                    print("❌")
                
                total_processed += 1
                
            except Exception as e:
                failed += 1
                print(f"❌ Error: {e!s}")
        
        print(f"  📊 {display_name}: {successful} successful, {failed} failed")

    # Final summary
    print("\n🎉 BATCH PROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Total images processed: {total_processed}")
    print(f"Total successful: {total_successful}")
    print(f"Total failed: {total_processed - total_successful}")
    print("\n📁 Output directories created:")
    for ratio_name in aspect_ratios.keys():
        print(f"  • upscaled_{ratio_name}/")
    
    print("\n💡 All images are:")
    print("  • 300 DPI for print quality")
    print(f"  • Under {max_size_mb}MB file size")
    print("  • Optimized for web and print use")
    print("  • Cropped to exact aspect ratios")

def main():
    """Main function with interactive options"""
    print("🖼️  ENHANCED 9MB IMAGE PROCESSOR")
    print("=" * 50)
    print("Processes images to 300 DPI with various aspect ratios")
    print("Maintains file size under 9MB")
    print("=" * 50)
    
    # Use current directory by default
    current_dir = os.getcwd()
    print(f"\n📁 Working directory: {current_dir}")
    
    # Ask for confirmation
    use_current = input("\nUse current directory? (y/n, default: y): ").strip().lower()
    if use_current in ['n', 'no']:
        directory = input("Enter the directory path containing images: ")
    else:
        directory = current_dir
    
    max_size_mb = input("Enter the maximum file size in MB (default is 9MB): ").strip()
    max_size_mb = float(max_size_mb) if max_size_mb else 9
    
    print(f"\n🔄 Processing images in: {directory}")
    print(f"📏 Max file size: {max_size_mb}MB")
    print("🎯 Target DPI: 300")
    
    process_images_with_aspect_ratios(directory, max_size_mb)

if __name__ == "__main__":
    main()