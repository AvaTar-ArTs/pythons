#!/bin/bash

# Load the environment variables from ~/.env
export $(grep -v '^#' ~/.env | xargs)

# Directory paths
MP4_DIR="/Users/steven/Music/AiMine"
IMAGE_DIR="/Users/steven/Pictures/covers"
OUTPUT_DIR="/Users/steven/Documents/python/mp3-mp4/done"

# Step 1: Process all MP3 files in the directory
for MP3_FILE in "$MP3_DIR"/*.mp4; do
    FILENAME=$(basename "$MP3_FILE" .mp3)

    echo "Processing: $FILENAME"

    # Step 2: Transcribe the MP3 file
    echo "Transcribing $FILENAME..."
    python3 /Users/steven/Movies/AutoTypographyh- lyrics/transcribe.py"$MP4_FILE" "$OUTPUT_DIR/${FILENAME}_transcript.txt"
    echo "Transcribed: $FILENAME"

    # Step 3: Analyze transcription
    echo "Analyzing transcript for $FILENAME..."
    python3 /Users/steven/Documents/python/mp3-mp4/analyze.py "$OUTPUT_DIR/${FILENAME}_transcript.txt" "$OUTPUT_DIR/${FILENAME}_analysis.txt"
    
    if [ -f "$OUTPUT_DIR/${FILENAME}_analysis.txt" ]; then
        echo "Analyzed: $FILENAME"

  
    echo "Completed processing: $FILENAME"
done

echo "All files processed!"
