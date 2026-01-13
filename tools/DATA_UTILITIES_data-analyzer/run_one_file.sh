#!/usr/bin/env zsh
# Process a single file (edit VIDEO path)
conda activate hekate || { echo "activate hekate failed"; exit 1; }
VIDEO="/Users/steven/Movies/HeKaTe-saLome/input.mp4"
OUTDIR="/Users/steven/Movies/HeKaTe-saLome"
python "$(dirname "$0")/analyzer_prompt_cli.py"   --video "$VIDEO"   --outdir "$OUTDIR"   --segment-seconds 300
