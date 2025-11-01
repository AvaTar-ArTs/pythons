"""
Media Analysis Pipeline Gpt Claude

This module provides functionality for media analysis pipeline gpt claude.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_1024 = 1024
CONSTANT_1800 = 1800
CONSTANT_2000 = 2000
CONSTANT_3600 = 3600

#!/usr/bin/env python3
"""
ULTIMATE Media Analysis Pipeline - Simplified Edition
Uses only GPT-4o and Claude for reliability
"""

import os
import logging
import time
import json
import subprocess
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Now import other packages
try:
    from openai import OpenAI
    import anthropic
    from tqdm import tqdm
    import tenacity
except ImportError as e:
    logger.info(f"Import error: {e}")
    print(
        "Please install required packages with: pip install openai anthropic python-dotenv tqdm tenacity"
    )
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class LargeFileHandler:
    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir

    def extract_audio_from_video(self, media_path: Path) -> Path:
        """Extract audio from video files for processing"""
        temp_dir = self.base_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        audio_path = temp_dir / f"{media_path.stem}_audio.wav"

        # Use ffmpeg to extract audio
        cmd = [
            "ffmpeg",
            "-i",
            str(media_path),
            "-vn",  # No video
            "-acodec",
            "pcm_s16le",  # PCM audio
            "-ar",
            "16000",  # 16kHz sample rate
            "-ac",
            "1",  # Mono
            "-y",  # Overwrite output file
            str(audio_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=CONSTANT_1800)  # 30 min timeout
            return audio_path
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            logger.error(f"Failed to extract audio from {media_path}: {e}")
            raise

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_dir = self.base_dir / "temp"
        if temp_dir.exists():
            for file in temp_dir.glob("*"):
                try:
                    file.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete temp file {file}: {e}")


class UltimateMediaAnalyzer:
        """__init__ function."""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.setup_directories()
        self.setup_clients()
        self.file_handler = LargeFileHandler(self.base_dir)

    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            "transcripts",
            "analysis",
            "temp",
            "summaries",
            "embeddings",
            "exports",
            "cache",
        ]
        for dir_name in directories:
            (self.base_dir / dir_name).mkdir(exist_ok=True)

        logger.info(f"Analyzer initialized with base directory: {self.base_dir}")

    def setup_clients(self):
        """Initialize only GPT-4o and Claude clients"""
        # Check for API keys first
        required_keys = {"OPENAI_API_KEY": "OpenAI", "ANTHROPIC_API_KEY": "Anthropic"}

        missing_keys = [service for key, service in required_keys.items() if not os.getenv(key)]

        if missing_keys:
            logger.warning(
                f"Missing API keys for: {', '.join(missing_keys)}. Functionality will be limited."
            )

        # Initialize clients only if API keys are available
        try:
            self.openai_client = (
                OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
            )
            if self.openai_client:
                logger.info("OpenAI client initialized")
            else:
                logger.warning("OpenAI client not initialized - missing API key")

            self.anthropic_client = (
                anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                if os.getenv("ANTHROPIC_API_KEY")
                else None
            )
            if self.anthropic_client:
                logger.info("Anthropic client initialized")
            else:
                logger.warning("Anthropic client not initialized - missing API key")

        except Exception as e:
            logger.error(f"Failed to initialize API clients: {e}")
            self.openai_client = None
            self.anthropic_client = None

    def get_file_hash(self, file_path: Path) -> str:
        """Generate MD5 hash of file contents"""
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def check_cache(self, file_hash: str) -> Optional[Dict]:
        """Check if file has been processed before"""
        cache_file = self.base_dir / "cache" / f"{file_hash}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    cache_data = json.load(f)
                # Check if cache is still valid (less than 7 days old)
                cache_date = time.strptime(cache_data["timestamp"], "%Y-%m-%d %H:%M:%S")
                cache_time = time.mktime(cache_date)
                if time.time() - cache_time < 7 * 24 * CONSTANT_3600:  # 7 days
                    return cache_data
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logger.warning(f"Invalid cache file {cache_file}: {e}")
        return None

    def save_to_cache(self, file_hash: str, transcript: str, analysis: str):
        """Save results to cache"""
        cache_file = self.base_dir / "cache" / f"{file_hash}.json"
        cache_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "transcript": transcript,
            "analysis": analysis,
        }
        try:
            with open(cache_file, "w") as f:
                json.dump(cache_data, f)
        except Exception as e:
            logger.warning(f"Failed to save cache file {cache_file}: {e}")

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    )
    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio using OpenAI Whisper"""
        if not self.openai_client:
            return self._transcribe_fallback(audio_path)

        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="verbose_json"
                )
                return Path("\n").join(
                    f"{self.format_timestamp(seg.start)} -- {self.format_timestamp(seg.end)}: {seg.text}"
                    for seg in transcript.segments
                )
        except Exception as e:
            logger.error(f"OpenAI transcription failed: {e}")
            return self._transcribe_fallback(audio_path)

    def _transcribe_fallback(self, audio_path: Path) -> str:
        """Fallback transcription when APIs are unavailable"""
        logger.warning("Using fallback transcription - API unavailable")
        # Return a simple timestamped format
        file_size_mb = audio_path.stat().st_size / (CONSTANT_1024 * CONSTANT_1024)
        return f"00:00 -- 01:00: Audio file ({file_size_mb:.1f} MB). Transcription requires OpenAI API key."

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    )
    def analyze_content(self, content: str, context: str = "") -> str:
        """Analyze content using best available LLM (Claude preferred, then GPT-4o)"""
        # Try Claude first
        if self.anthropic_client:
            try:
                result = self._analyze_claude(content, context)
                if result and self.validate_analysis_format(result):
                    return result
            except Exception as e:
                logger.warning(f"Claude analysis failed: {e}")

        # Fall back to GPT-4o if Claude fails or is unavailable
        if self.openai_client:
            try:
                result = self._analyze_gpt4(content, context)
                if result and self.validate_analysis_format(result):
                    return result
            except Exception as e:
                logger.warning(f"GPT-4 analysis failed: {e}")

        # Fallback to template if all methods fail
        return self.generate_analysis_template(content)

    def validate_analysis_format(self, analysis: str) -> bool:
        """Validate the analysis output format"""
        required_sections = [
            "Central Themes and Messages",
            "Emotional Tone",
            "Narrative Arc",
            "Creator's Intent",
            "Significant Metaphors, Symbols, and Imagery",
            "Storytelling Techniques",
            "Interplay Between Visuals and Audio",
            "Audience Engagement and Impact",
            "Overall Effectiveness",
        ]

        return all(section in analysis for section in required_sections)

    def generate_analysis_template(self, content: str) -> str:
        """Generate analysis using template format"""
        template = """
### 1. Central Themes and Messages
Analysis of central themes and messages would appear here.

### 2. Emotional Tone
Analysis of emotional tone would appear here.

### 3. Narrative Arc
Analysis of narrative arc would appear here.

### 4. Creator's Intent
Analysis of creator's intent would appear here.

### 5. Significant Metaphors, Symbols, and Imagery
Analysis of metaphors, symbols, and imagery would appear here.

### 6. Storytelling Techniques
Analysis of storytelling techniques would appear here.

### 7. Interplay Between Visuals and Audio
Analysis of visuals and audio interplay would appear here.

### 8. Audience Engagement and Impact
Analysis of audience engagement and impact would appear here.

### 9. Overall Effectiveness
Overall effectiveness assessment would appear here.
"""
        return template

    def _analyze_claude(self, content: str, context: str) -> Optional[str]:
        """Analyze using Claude 3.5"""
        prompt = f"""
        As an expert media analyst, provide comprehensive analysis in this exact format:

        ### 1. Central Themes and Messages
        [Analyze the central themes and messages]

        ### 2. Emotional Tone
        [Analyze the emotional tone]

        ### 3. Narrative Arc
        [Analyze the narrative arc]

        ### 4. Creator's Intent
        [Analyze the creator's intent]

        ### 5. Significant Metaphors, Symbols, and Imagery
        [Analyze metaphors, symbols, and imagery]

        ### 6. Storytelling Techniques
        [Analyze storytelling techniques]

        ### 7. Interplay Between Visuals and Audio
        [Analyze the interplay between visuals and audio]

        ### 8. Audience Engagement and Impact
        [Analyze audience engagement and impact]

        ### 9. Overall Effectiveness
        [Provide overall assessment of effectiveness]

        Context: {context}
        Content: {content}
        """

        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=CONSTANT_2000,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return None

    def _analyze_gpt4(self, content: str, context: str) -> Optional[str]:
        """Analyze using GPT-4"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert media analyst. Provide analysis in the exact format specified with numbered sections.",
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nAnalyze this content using this exact format:\n\n### 1. Central Themes and Messages\n[Analysis]\n\n### 2. Emotional Tone\n[Analysis]\n\n### 3. Narrative Arc\n[Analysis]\n\n### 4. Creator's Intent\n[Analysis]\n\n### 5. Significant Metaphors, Symbols, and Imagery\n[Analysis]\n\n### 6. Storytelling Techniques\n[Analysis]\n\n### 7. Interplay Between Visuals and Audio\n[Analysis]\n\n### 8. Audience Engagement and Impact\n[Analysis]\n\n### 9. Overall Effectiveness\n[Analysis]\n\nContent: {content}",
                },
            ],
            max_tokens=CONSTANT_1800,
        )
        return response.choices[0].message.content

    def process_media_file(self, media_path: Path):
        """Process a single media file"""
        logger.info(f"Processing: {media_path.name}")

        try:
            # Check cache first
            file_hash = self.get_file_hash(media_path)
            cached_data = self.check_cache(file_hash)

            if cached_data:
                logger.info(f"Using cached results for {media_path.name}")
                self.save_results_formatted(
                    media_path, cached_data["transcript"], cached_data["analysis"]
                )
                return

            # For video files, extract audio first
            transcript = ""
            if media_path.suffix.lower() in [".mp4", ".mov", ".avi"]:
                audio_path = self.file_handler.extract_audio_from_video(media_path)
                transcript = self.transcribe_audio(audio_path)
                # Clean up audio file
                audio_path.unlink()
            elif media_path.suffix.lower() in [".mp3", ".wav", ".m4a"]:
                # For audio files, process directly
                transcript = self.transcribe_audio(media_path)
            else:
                logger.warning(f"Unsupported file format: {media_path.suffix}")
                transcript = f"00:00 -- 01:00: Unsupported file format: {media_path.suffix}"

            # Analyze content
            analysis = self.analyze_content(transcript, f"Analysis of {media_path.name}")

            # Save results
            self.save_results_formatted(media_path, transcript, analysis)

            # Save to cache
            self.save_to_cache(file_hash, transcript, analysis)

            logger.info(f"✅ Completed: {media_path.name}")

        except Exception as e:
            logger.error(f"❌ Failed to process {media_path.name}: {e}")
            # Save error result
            error_transcript = (
                "00:00 -- 01:00: Error processing file. Please check logs for details."
            )
            error_analysis = self.generate_analysis_template("")
            self.save_results_formatted(media_path, error_transcript, error_analysis)

    def save_results_formatted(self, media_path: Path, transcript: str, analysis: str):
        """Save analysis results in the specific format requested"""
        base_name = media_path.stem

        # Save in the exact format: Analysis {content} || Transcript {content}
        formatted_content = f"Analysis {{{analysis}}} || Transcript {{{transcript}}}"

        # Save to analysis directory
        analysis_file = self.base_dir / "analysis" / f"{base_name}_formatted.txt"
        analysis_file.write_text(formatted_content, encoding="utf-8")

        # Also save separate files for transcript and analysis
        transcript_file = self.base_dir / "transcripts" / f"{base_name}_transcript.txt"
        transcript_file.write_text(transcript, encoding="utf-8")

        analysis_only_file = self.base_dir / "analysis" / f"{base_name}_analysis.txt"
        analysis_only_file.write_text(analysis, encoding="utf-8")

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Format seconds into MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"

    def process_all_media_files(self):
        """Process all media files with progress tracking"""
        media_files = []

        for ext in ["*.mp3", "*.mp4", "*.wav", "*.m4a", "*.mov", "*.avi"]:
            media_files.extend(self.base_dir.glob(ext))

        logger.info(f"Found {len(media_files)} media files")

        # Process files with progress bar
        with tqdm(total=len(media_files), desc="Processing files") as pbar:
            for media_file in media_files:
                self.process_media_file(media_file)
                pbar.update(1)
                pbar.set_postfix(file=media_file.name[:20])


def main():
    """Main execution function"""
    logger.info("=== ULTIMATE Media Analysis Pipeline ===")
    logger.info("Simplified Edition (GPT-4o and Claude only)")

    base_dir_input = input("Enter media directory (press Enter for current): ").strip()
    base_dir = base_dir_input if base_dir_input else None

    analyzer = UltimateMediaAnalyzer(base_dir)

    try:
        # Process all media files
        analyzer.process_all_media_files()

        logger.info(f"\n✅ Analysis complete!")
        logger.info("Check 'transcripts' and 'analysis' folders for results.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        logger.info(f"\n❌ Error: {e}")
    finally:
        # Clean up any remaining temp files
        analyzer.file_handler.cleanup_temp_files()


if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import openai
        import anthropic
        from tqdm import tqdm
        import tenacity
    except ImportError as e:
        logger.info(f"Missing required package: {e}")
        logger.info("Please install with: pip install openai anthropic python-dotenv tqdm tenacity")
