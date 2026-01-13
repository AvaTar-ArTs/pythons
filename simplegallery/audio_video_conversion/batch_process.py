#!/usr/bin/env python3
"""
Batch processing script for multiple audio/video files
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from transcription_analyzer import TranscriptionAnalyzer

# Load environment variables from ~/.env
load_dotenv(os.path.expanduser("~/.env"))

def main():
    """Process multiple files in a directory."""
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in a .env file or environment variable")
        return
    
    # Initialize analyzer
    analyzer = TranscriptionAnalyzer(api_key)
    
    # Get input directory from command line argument
    if len(sys.argv) != 2:
        print("Usage: python batch_process.py <input_directory>")
        print("Will process all MP3 and MP4 files in the directory")
        return
    
    input_dir = Path(sys.argv[1])
    
    if not input_dir.exists():
        print(f"ERROR: Directory {input_dir} does not exist")
        return
    
    # Find all supported files
    supported_files = []
    for pattern in ['*.mp3', '*.mp4', '*.MP3', '*.MP4']:
        supported_files.extend(input_dir.glob(pattern))
    
    if not supported_files:
        print(f"No MP3 or MP4 files found in {input_dir}")
        return
    
    print(f"Found {len(supported_files)} files to process:")
    for file in supported_files:
        print(f"  - {file.name}")
    
    # Process each file
    successful = 0
    failed = 0
    
    for file_path in supported_files:
        print(f"\n{'='*50}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*50}")
        
        if analyzer.process_file(str(file_path)):
            successful += 1
            print(f"✅ Successfully processed {file_path.name}")
        else:
            failed += 1
            print(f"❌ Failed to process {file_path.name}")
    
    print(f"\n{'='*50}")
    print("BATCH PROCESSING COMPLETE")
    print(f"{'='*50}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(supported_files)}")

if __name__ == "__main__":
    main()