#!/usr/bin/env python3
"""
Unified Batch Processor
Combines transcription and analysis in a single pipeline

Usage:
    # Process directory with transcription + analysis
    python batch_processor.py /path/to/audio --transcribe --analyze
    
    # Only transcribe
    python batch_processor.py /path/to/audio --transcribe
    
    # Only analyze existing transcripts
    python batch_processor.py /path/to/transcripts --analyze
"""

import os
import argparse
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
load_dotenv(os.path.expanduser("~/.env"))

from audio_transcriber import AudioTranscriber, TranscriptionProvider
from transcript_analyzer import TranscriptAnalyzer, AnalysisProvider, AnalysisType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BatchProcessor:
    """Unified batch processor for transcription and analysis."""

    def __init__(
        self,
        transcribe: bool = False,
        analyze: bool = False,
        transcription_provider: TranscriptionProvider = TranscriptionProvider.OPENAI,
        analysis_provider: AnalysisProvider = AnalysisProvider.OPENAI,
        analysis_type: AnalysisType = AnalysisType.GENERAL,
    ):
        self.transcribe = transcribe
        self.analyze = analyze

        self.transcriber = None
        if transcribe:
            try:
                self.transcriber = AudioTranscriber(provider=transcription_provider)
            except Exception as e:
                logger.error(f"Failed to initialize transcriber: {e}")
                raise

        self.analyzer = None
        if analyze:
            try:
                self.analyzer = TranscriptAnalyzer(
                    provider=analysis_provider, analysis_type=analysis_type
                )
            except Exception as e:
                logger.error(f"Failed to initialize analyzer: {e}")
                raise

    def process_directory(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        force: bool = False,
        transcription_model: Optional[str] = None,
        analysis_model: Optional[str] = None,
    ):
        """Process directory: transcribe audio and/or analyze transcripts."""
        if not output_dir:
            output_dir = input_dir

        transcripts_dir = output_dir / "transcripts"
        analysis_dir = output_dir / "analysis"

        # Step 1: Transcribe audio files
        if self.transcribe:
            logger.info("=" * 60)
            logger.info("STEP 1: Transcribing audio files")
            logger.info("=" * 60)
            self.transcriber.batch_transcribe(
                input_dir, transcripts_dir, force=force
            )
            logger.info(f"✓ Transcription complete. Transcripts saved to {transcripts_dir}")

        # Step 2: Analyze transcripts
        if self.analyze:
            logger.info("=" * 60)
            logger.info("STEP 2: Analyzing transcripts")
            logger.info("=" * 60)
            
            # Use transcripts_dir if we transcribed, otherwise use input_dir
            transcript_source = transcripts_dir if self.transcribe and transcripts_dir.exists() else input_dir
            
            self.analyzer.batch_analyze(
                transcript_source, analysis_dir, force=force, model=analysis_model
            )
            logger.info(f"✓ Analysis complete. Results saved to {analysis_dir}")

        logger.info("=" * 60)
        logger.info("Batch processing complete!")
        logger.info("=" * 60)


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Unified Batch Processor for Transcription and Analysis"
    )
    parser.add_argument("input", help="Input directory containing audio files or transcripts")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument(
        "--transcribe",
        action="store_true",
        help="Transcribe audio files",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze transcripts",
    )
    parser.add_argument(
        "--transcription-provider",
        choices=["openai", "local"],
        default="openai",
        help="Transcription provider (default: openai)",
    )
    parser.add_argument(
        "--analysis-provider",
        choices=["openai", "ollama"],
        default="openai",
        help="Analysis provider (default: openai)",
    )
    parser.add_argument(
        "--analysis-type",
        choices=["general", "music", "video", "podcast"],
        default="general",
        help="Analysis type (default: general)",
    )
    parser.add_argument(
        "--transcription-model",
        help="Transcription model name",
    )
    parser.add_argument(
        "--analysis-model",
        help="Analysis model name",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess existing files",
    )

    args = parser.parse_args()

    # At least one operation must be specified
    if not args.transcribe and not args.analyze:
        logger.error("Must specify at least one of --transcribe or --analyze")
        return

    try:
        processor = BatchProcessor(
            transcribe=args.transcribe,
            analyze=args.analyze,
            transcription_provider=TranscriptionProvider(args.transcription_provider),
            analysis_provider=AnalysisProvider(args.analysis_provider),
            analysis_type=AnalysisType(args.analysis_type),
        )

        input_path = Path(args.input)
        output_path = Path(args.output) if args.output else None

        processor.process_directory(
            input_path,
            output_path,
            force=args.force,
            transcription_model=args.transcription_model,
            analysis_model=args.analysis_model,
        )

    except Exception as e:
        logger.error(f"Batch processing failed: {e}")


if __name__ == "__main__":
    main()
