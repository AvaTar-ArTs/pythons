import sys
import os
import argparse

# Add parent directory to sys.path to allow imports from core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.processor import OpusReplica
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Map AI-identified categories to our visual templates
STYLE_MAP = {
    "viral": "high_energy",
    "educational": "minimalist",
    "other": "minimalist"
}

def run_pipeline(video_path: str):
    logger.info(f"Orchestrator starting pipeline for: {video_path}")
    
    # Initialize the core processor
    processor = OpusReplica(video_path)
    
    # 1. Get/Transcribe (Caching layer)
    processor.get_transcript()
    
    # 2. Identify Clips (AI-driven)
    clips = processor.identify_clips()
    
    # 3. Extract and Assemble
    for clip in clips:
        # Determine style based on category
        category = clip.get("category", "other")
        style = STYLE_MAP.get(category, "minimalist")
        
        logger.info(f"Mapping category '{category}' to style '{style}'")
        processor.extract_and_assemble(clip, style_name=style)
        
    logger.info("Pipeline execution complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Opus Clip Evolution Pipeline")
    parser.add_argument("--video", type=str, required=True, help="Path to the video file to process")
    args = parser.parse_args()
    
    video_file = os.path.abspath(args.video)
    
    if not os.path.exists(video_file):
        logger.error(f"Video file not found at {video_file}")
    else:
        run_pipeline(video_file)
