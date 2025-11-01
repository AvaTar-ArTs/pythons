"""
Transcription

This module provides functionality for transcription.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_2000 = 2000

#!/usr/bin/env python3
"""
Audio/Video Transcription and Analysis Tool
Converts MP4 to MP3, transcribes with timestamps, and provides GPT-4o analysis
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

import whisper
from moviepy.editor import VideoFileClip
from openai import OpenAI
from dotenv import load_dotenv
from audio_chunker import AudioChunker
import config

# Load environment variables from ~/.env
load_dotenv(os.path.expanduser("~/.env"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("transcription.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class TranscriptionAnalyzer:
    def __init__(self, openai_api_key: str):
        """Initialize the transcription analyzer with OpenAI API key."""
        self.client = OpenAI(api_key=openai_api_key)
        self.whisper_model = whisper.load_model(config.WHISPER_MODEL)
        self.chunker = AudioChunker()

    def convert_mp4_to_mp3(self, input_path: str, output_path: str) -> bool:
        """Convert MP4 file to MP3 format."""
        try:
            logger.info(f"Converting {input_path} to MP3...")
            video = VideoFileClip(input_path)
            audio = video.audio
            audio.write_audiofile(output_path, verbose=False, logger=None)
            audio.close()
            video.close()
            logger.info(f"Successfully converted to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error converting MP4 to MP3: {e}")
            return False

    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio file with timestamps using Whisper."""
        try:
            logger.info(f"Transcribing {audio_path}...")
            result = self.whisper_model.transcribe(audio_path, word_timestamps=True)

            # Format transcript with timestamps
            transcript_with_timestamps = []
            for segment in result["segments"]:
                start_time = self._format_timestamp(segment["start"])
                end_time = self._format_timestamp(segment["end"])
                text = segment["text"].strip()
                transcript_with_timestamps.append(f"[{start_time} - {end_time}] {text}")

            return {
                "full_transcript": result["text"],
                "timestamped_transcript": Path("\n").join(transcript_with_timestamps),
                "segments": result["segments"],
                "language": result.get("language", "unknown"),
            }
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return {}

    def analyze_transcript(
        self, transcript: str, language: str = "English"
    ) -> Dict[str, Any]:
        """Analyze transcript using GPT-4o."""
        try:
            logger.info("Analyzing transcript with GPT-4o...")

            prompt = f"""
            Please analyze the following transcript in {language} and provide a comprehensive analysis including:
            
            1. **Summary**: A concise overview of the main topics discussed
            2. **Key Points**: 5-7 most important points or insights
            3. **Topics/Themes**: Main themes and subjects covered
            4. **Sentiment**: Overall tone and emotional context
            5. **Action Items**: Any tasks, decisions, or next steps mentioned
            6. **Questions Raised**: Important questions that were asked or remain unanswered
            7. **Technical Terms**: Any specialized vocabulary or concepts mentioned
            8. **Duration Analysis**: Notable patterns in pacing or content distribution
            
            Transcript:
            {transcript}
            
            Please format your response as a structured JSON object with clear sections.
            """

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst specializing in transcript analysis. Provide detailed, structured analysis in JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=CONSTANT_2000,
            )

            analysis_text = response.choices[0].message.content

            # Try to parse as JSON, fallback to text if not valid JSON
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                analysis = {"raw_analysis": analysis_text, "format": "text"}

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing transcript: {e}")
            return {"error": str(e)}

    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def create_output_structure(self, input_file: Path) -> Dict[str, Path]:
        """Create organized folder structure for output files."""
        base_name = input_file.stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = input_file.parent / f"{base_name}_analysis_{timestamp}"

        # Create directories
        output_dir.mkdir(exist_ok=True)
        transcripts_dir = output_dir / "transcripts"
        analysis_dir = output_dir / "analysis"
        audio_dir = output_dir / "audio"

        for dir_path in [transcripts_dir, analysis_dir, audio_dir]:
            dir_path.mkdir(exist_ok=True)

        return {
            "base_dir": output_dir,
            "transcripts_dir": transcripts_dir,
            "analysis_dir": analysis_dir,
            "audio_dir": audio_dir,
        }

    def process_file(self, input_path: str) -> bool:
        """Process a single audio/video file through the complete pipeline."""
        input_file = Path(input_path)

        if not input_file.exists():
            logger.error(f"File not found: {input_path}")
            return False

        # Create output structure
        dirs = self.create_output_structure(input_file)

        try:
            # Step 1: Convert MP4 to MP3 if needed
            audio_path = input_file
            if input_file.suffix.lower() == ".mp4":
                audio_path = dirs["audio_dir"] / f"{input_file.stem}.mp3"
                if not self.convert_mp4_to_mp3(str(input_file), str(audio_path)):
                    return False

            # Step 2: Check if file needs chunking
            if self.chunker.should_split_file(str(audio_path)):
                logger.info(
                    f"File is longer than {config.MAX_CHUNK_DURATION_MINUTES} minutes, splitting into chunks..."
                )
                return self._process_long_file(input_file, audio_path, dirs)
            else:
                logger.info("File is short enough, processing normally...")
                return self._process_short_file(input_file, audio_path, dirs)

        except Exception as e:
            logger.error(f"Error processing file {input_file.name}: {e}")
            return False

    def _process_short_file(
        self, input_file: Path, audio_path: Path, dirs: dict
    ) -> bool:
        """Process a short file (no chunking needed)."""
        try:
            # Transcribe audio
            transcription_result = self.transcribe_audio(str(audio_path))
            if not transcription_result:
                return False

            # Save transcript files
            transcript_file = (
                dirs["transcripts_dir"] / f"{input_file.stem}_transcript.txt"
            )
            timestamped_file = (
                dirs["transcripts_dir"] / f"{input_file.stem}_timestamped.txt"
            )

            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(transcription_result["full_transcript"])

            with open(timestamped_file, "w", encoding="utf-8") as f:
                f.write(transcription_result["timestamped_transcript"])

            # Analyze transcript
            analysis = self.analyze_transcript(
                transcription_result["full_transcript"],
                transcription_result.get("language", "English"),
            )

            # Save analysis
            analysis_file = dirs["analysis_dir"] / f"{input_file.stem}_analysis.json"
            with open(analysis_file, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)

            # Create summary report
            self._create_summary_file(
                input_file, audio_path, dirs, transcription_result, analysis, False
            )

            logger.info(f"Successfully processed {input_file.name}")
            logger.info(f"Output directory: {dirs['base_dir']}")
            return True

        except Exception as e:
            logger.error(f"Error processing short file {input_file.name}: {e}")
            return False

    def _process_long_file(
        self, input_file: Path, audio_path: Path, dirs: dict
    ) -> bool:
        """Process a long file by splitting into chunks."""
        try:
            # Create chunks directory
            chunks_dir = dirs["base_dir"] / "chunks"
            chunks_dir.mkdir(exist_ok=True)

            # Split audio into chunks
            chunk_files = self.chunker.split_audio_file(str(audio_path), chunks_dir)
            if not chunk_files:
                logger.error("Failed to create audio chunks")
                return False

            logger.info(f"Created {len(chunk_files)} chunks, processing each...")

            # Process each chunk
            chunk_transcripts = []
            for i, chunk_file in enumerate(chunk_files, 1):
                logger.info(
                    f"Processing chunk {i}/{len(chunk_files)}: {Path(chunk_file).name}"
                )

                chunk_result = self.transcribe_audio(chunk_file)
                if chunk_result:
                    chunk_transcripts.append(chunk_result)

                    # Save individual chunk transcript
                    chunk_name = Path(chunk_file).stem
                    chunk_transcript_file = chunks_dir / f"{chunk_name}_transcript.txt"
                    with open(chunk_transcript_file, "w", encoding="utf-8") as f:
                        f.write(chunk_result["full_transcript"])
                else:
                    logger.warning(f"Failed to transcribe chunk {i}")
                    chunk_transcripts.append({})

            # Merge all chunk transcripts
            merged_transcript = self.chunker.merge_transcripts(
                chunk_transcripts, chunk_files
            )
            if not merged_transcript:
                logger.error("Failed to merge chunk transcripts")
                return False

            # Save merged transcript files
            transcript_file = (
                dirs["transcripts_dir"] / f"{input_file.stem}_transcript.txt"
            )
            timestamped_file = (
                dirs["transcripts_dir"] / f"{input_file.stem}_timestamped.txt"
            )

            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(merged_transcript["full_transcript"])

            with open(timestamped_file, "w", encoding="utf-8") as f:
                f.write(merged_transcript["timestamped_transcript"])

            # Analyze merged transcript
            analysis = self.analyze_transcript(
                merged_transcript["full_transcript"],
                merged_transcript.get("language", "English"),
            )

            # Add chunking info to analysis
            if isinstance(analysis, dict):
                analysis["chunking_info"] = {
                    "was_chunked": True,
                    "chunk_count": len(chunk_files),
                    "max_chunk_duration_minutes": config.MAX_CHUNK_DURATION_MINUTES,
                    "chunk_overlap_seconds": config.CHUNK_OVERLAP_SECONDS,
                }

            # Save analysis
            analysis_file = dirs["analysis_dir"] / f"{input_file.stem}_analysis.json"
            with open(analysis_file, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)

            # Create summary report
            self._create_summary_file(
                input_file,
                audio_path,
                dirs,
                merged_transcript,
                analysis,
                True,
                len(chunk_files),
            )

            # Clean up chunk files
            self.chunker.cleanup_chunks(chunk_files)

            logger.info(
                f"Successfully processed {input_file.name} ({len(chunk_files)} chunks)"
            )
            logger.info(f"Output directory: {dirs['base_dir']}")
            return True

        except Exception as e:
            logger.error(f"Error processing long file {input_file.name}: {e}")
            return False

    def _create_summary_file(
        self,
        input_file: Path,
        audio_path: Path,
        dirs: dict,
        transcription_result: dict,
        analysis: dict,
        was_chunked: bool,
        chunk_count: int = 0,
    ) -> None:
        """Create a summary report file."""
        try:
            summary_file = dirs["base_dir"] / f"{input_file.stem}_summary.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(f"Transcription and Analysis Summary\n")
                f.write(f"================================\n\n")
                f.write(f"Original File: {input_file.name}\n")
                f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"Language: {transcription_result.get('language', 'Unknown')}\n"
                )

                if was_chunked:
                    f.write(f"Processing: Chunked into {chunk_count} pieces\n")
                    f.write(
                        f"Max Chunk Duration: {config.MAX_CHUNK_DURATION_MINUTES} minutes\n"
                    )
                    f.write(f"Chunk Overlap: {config.CHUNK_OVERLAP_SECONDS} seconds\n")

                if "total_duration" in transcription_result:
                    f.write(
                        f"Duration: {self._format_timestamp(transcription_result['total_duration'])}\n"
                    )
                elif (
                    "segments" in transcription_result
                    and transcription_result["segments"]
                ):
                    f.write(
                        f"Duration: {self._format_timestamp(transcription_result['segments'][-1]['end'])}\n"
                    )

                f.write(f"\nFiles Created:\n")
                f.write(f"- Transcript: {input_file.stem}_transcript.txt\n")
                f.write(f"- Timestamped: {input_file.stem}_timestamped.txt\n")
                f.write(f"- Analysis: {input_file.stem}_analysis.json\n")
                if input_file.suffix.lower() == ".mp4":
                    f.write(f"- Audio: {audio_path.name}\n")
                if was_chunked:
                    f.write(f"- Chunks: {chunk_count} temporary files (cleaned up)\n")

                if (
                    was_chunked
                    and isinstance(analysis, dict)
                    and "chunking_info" in analysis
                ):
                    f.write(f"\nChunking Details:\n")
                    f.write(f"- Original file was split into {chunk_count} chunks\n")
                    f.write(
                        f"- Each chunk max {config.MAX_CHUNK_DURATION_MINUTES} minutes\n"
                    )
                    f.write(
                        f"- {config.CHUNK_OVERLAP_SECONDS}s overlap between chunks\n"
                    )
                    f.write(f"- Chunks processed individually and merged\n")

        except Exception as e:
            logger.warning(f"Could not create summary file: {e}")


def main():
    """Main function to run the transcription analyzer."""
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        logger.info(
            "Please set your OpenAI API key in a .env file or environment variable"
        )
        return

    # Initialize analyzer
    analyzer = TranscriptionAnalyzer(api_key)

    # Get input file from command line argument
    if len(sys.argv) != 2:
        logger.info("Usage: python transcription_analyzer.py <input_file>")
        logger.info("Supported formats: MP3, MP4")
        return

    input_file = sys.argv[1]

    # Validate file format
    supported_formats = [".mp3", ".mp4"]
    if not any(input_file.lower().endswith(ext) for ext in supported_formats):
        logger.error(
            f"Unsupported file format. Supported formats: {', '.join(supported_formats)}"
        )
        return

    # Process the file
    success = analyzer.process_file(input_file)
    if success:
        logger.info(f"\n✅ Successfully processed {input_file}")
    else:
        logger.info(f"\n❌ Failed to process {input_file}")
        sys.exit(1)


if __name__ == "__main__":
    main()
