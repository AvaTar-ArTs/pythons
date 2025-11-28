#!/usr/bin/env python3
"""
Generate CSV files for all file types using the existing scripts
"""

import os
import sys
from datetime import datetime

# Import config to get source directory
import config

# Import the generate functions from each module
from audio import generate_dry_run_csv as generate_audio_csv
from img import generate_csv as generate_img_csv
from docs import generate_dry_run_csv as generate_docs_csv
from vids import generate_dry_run_csv as generate_vids_csv
from other import generate_dry_run_csv as generate_other_csv

def get_unique_file_path(base_path):
    """Get a unique file path if the file already exists"""
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def main():
    # Get source directory from command line or config
    if len(sys.argv) > 1:
        source_directory = sys.argv[1]
    else:
        # Try config first, then fallback to home directory
        source_directory = getattr(config, 'SOURCE_DIRECTORY', None)
        if not source_directory or not os.path.isdir(source_directory):
            # Try common alternatives
            alternatives = [
                os.path.expanduser("~/Music"),
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~"),
                "/Volumes/2T-Xx",
            ]
            for alt in alternatives:
                if os.path.isdir(alt):
                    source_directory = alt
                    print(f"⚠️  Config directory not found, using: {source_directory}")
                    break
    
    # Check if source directory exists
    if not source_directory or not os.path.isdir(source_directory):
        print(f"Error: Source directory does not exist: {source_directory}")
        print("Usage: python3 generate_all_csvs.py [directory_path]")
        print("Or update config.py with a valid directory path.")
        sys.exit(1)
    
    print("=" * 80)
    print("GENERATING CSV FILES FOR ALL FILE TYPES")
    print("=" * 80)
    print(f"Source Directory: {source_directory}")
    print()
    
    directories = [source_directory]
    current_dir = os.getcwd()
    timestamp = datetime.now().strftime("%m-%d-%H:%M")
    
    csv_files = {}
    
    # Generate Audio CSV
    print("🎵 Processing audio files...")
    try:
        csv_path = os.path.join(current_dir, f"audio-{timestamp}.csv")
        csv_path = get_unique_file_path(csv_path)
        generate_audio_csv(directories, csv_path)
        csv_files['audio'] = csv_path
        print(f"   ✅ Audio CSV saved: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"   ❌ Error processing audio: {e}")
        csv_files['audio'] = None
    
    print()
    
    # Generate Image CSV
    print("🖼️  Processing image files...")
    try:
        csv_path = os.path.join(current_dir, f"image_data-{timestamp}.csv")
        csv_path = get_unique_file_path(csv_path)
        generate_img_csv(directories, csv_path)
        csv_files['images'] = csv_path
        print(f"   ✅ Image CSV saved: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"   ❌ Error processing images: {e}")
        csv_files['images'] = None
    
    print()
    
    # Generate Documents CSV
    print("📄 Processing document files...")
    try:
        csv_path = os.path.join(current_dir, f"docs-{timestamp}.csv")
        csv_path = get_unique_file_path(csv_path)
        generate_docs_csv(directories, csv_path)
        csv_files['documents'] = csv_path
        print(f"   ✅ Documents CSV saved: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"   ❌ Error processing documents: {e}")
        csv_files['documents'] = None
    
    print()
    
    # Generate Video CSV
    print("🎬 Processing video files...")
    try:
        csv_path = os.path.join(current_dir, f"vids-{timestamp}.csv")
        csv_path = get_unique_file_path(csv_path)
        generate_vids_csv(directories, csv_path)
        csv_files['videos'] = csv_path
        print(f"   ✅ Video CSV saved: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"   ❌ Error processing videos: {e}")
        csv_files['videos'] = None
    
    print()
    
    # Generate Other Files CSV
    print("📦 Processing other files...")
    try:
        csv_path = os.path.join(current_dir, f"other-{timestamp}.csv")
        csv_path = get_unique_file_path(csv_path)
        generate_other_csv(directories, csv_path)
        csv_files['other'] = csv_path
        print(f"   ✅ Other files CSV saved: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"   ❌ Error processing other files: {e}")
        csv_files['other'] = None
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    for file_type, csv_path in csv_files.items():
        if csv_path:
            file_size = os.path.getsize(csv_path) / 1024  # Size in KB
            print(f"✅ {file_type.capitalize()}: {os.path.basename(csv_path)} ({file_size:.1f} KB)")
        else:
            print(f"❌ {file_type.capitalize()}: Failed to generate")
    
    print()
    print("=" * 80)
    print("✅ CSV GENERATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
