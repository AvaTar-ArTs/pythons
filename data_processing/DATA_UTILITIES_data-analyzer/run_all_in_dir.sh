#!/usr/bin/env zsh
# Process all MP4s in /Users/steven/Movies/invideo with 5-minute segments
conda activate hekate || { echo "activate hekate failed"; exit 1; }
python "$(dirname "$0")/analyzer_prompt_cli.py"   --video-dir "/Users/steven/Movies/invideo"   --segment-seconds 300
