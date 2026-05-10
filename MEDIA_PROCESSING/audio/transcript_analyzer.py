#!/usr/bin/env python3
"""
Unified Transcript Analyzer
Supports both OpenAI GPT (cloud) and Ollama (local)

Usage:
    # OpenAI GPT analysis
    python transcript_analyzer.py transcript.txt --provider openai --type music

    # Ollama local analysis
    python transcript_analyzer.py transcript.txt --provider ollama --model llama3.1:8b-instruct

    # Batch analyze directory
    python transcript_analyzer.py /path/to/transcripts --batch
"""

import os
import json
import logging
import argparse
import random
import time
from pathlib import Path
from typing import Dict, Optional
from enum import Enum

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
                            value = value.strip().strip('\'').strip("\'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
load_dotenv(os.path.expanduser("~/.env"))

# Optional imports
try:
    from openai import OpenAI

    HAVE_OPENAI = True
except ImportError:
    HAVE_OPENAI = False

try:
    import requests

    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class AnalysisProvider(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"


class AnalysisType(Enum):
    GENERAL = "general"
    MUSIC = "music"
    VIDEO = "video"
    PODCAST = "podcast"


class TranscriptAnalyzer:
    """Unified transcript analysis tool supporting multiple backends and analysis types."""

    # Analysis prompts by type
    PROMPTS = {
        AnalysisType.GENERAL: {
            "system": "You are an expert content analyst. Provide detailed, structured analysis of transcripts.",
            "user_template": """Analyze the following transcript and provide:
1. **Summary**: Concise overview of main topics
2. **Key Points**: 5-7 most important insights
3. **Topics/Themes**: Main themes covered
4. **Sentiment**: Overall tone and emotional context
5. **Action Items**: Tasks, decisions, or next steps mentioned
6. **Questions Raised**: Important questions asked or unanswered
7. **Technical Terms**: Specialized vocabulary or concepts

Transcript:
{transcript}""",
        },
        AnalysisType.MUSIC: {
            "system": "You are an experienced language and music expert. Provide in-depth analysis of song lyrics.",
            "user_template": '\''Analyze the following song transcript:
1. **Central Themes and Meaning**: Main themes and message
2. **Emotional Tone**: Emotional tone and shifts
3. **Artist's Intent**: What the artist aims to express
4. **Metaphors, Symbols, and Imagery**: Notable metaphors and their significance
5. **Overall Emotional and Narrative Experience**: How elements create impact

Transcript:
{transcript}""",
        },
        AnalysisType.VIDEO: {
            "system": "You are an expert in multimedia analysis and storytelling.",
            "user_template": """Analyze this video transcript focusing on:
1. **Central Themes & Messages**: Primary ideas conveyed
2. **Emotional Tone**: Emotions evoked
3. **Narrative Arc**: Story progression and turning points
4. **Creator's Intent**: Purpose (entertain, inform, inspire, persuade)
5. **Metaphors, Symbols, and Imagery**: Notable visual/audio motifs
6. **Storytelling Techniques**: Pacing, transitions, effects
7. **Interplay Between Visuals and Audio**: How they work together
8. **Audience Engagement**: How effectively it captures attention
9. **Overall Effectiveness**: Cohesive, immersive experience

Transcript:
{transcript}""",
        },
        AnalysisType.PODCAST: {
            "system": "You are a podcast content analyst. Provide structured analysis of podcast transcripts.",
            "user_template": """Analyze this podcast transcript:
1. **Main Topics**: Primary subjects discussed
2. **Key Takeaways**: Most important insights
3. **Guest Expertise**: Areas of expertise highlighted
4. **Discussion Flow**: How topics transition
5. **Notable Quotes**: Memorable statements
6. **Actionable Insights**: Practical advice or steps
7. **Follow-up Topics**: Related subjects worth exploring

Transcript:
{transcript}'\'',
        },
    }

    def __init__(:
        self,
        provider: AnalysisProvider = AnalysisProvider.OPENAI,
        analysis_type: AnalysisType = AnalysisType.GENERAL,
    ):
        self.provider = provider
        self.analysis_type = analysis_type

        if provider == AnalysisProvider.OPENAI:
            if not HAVE_OPENAI:
                raise ImportError("openai package required for OpenAI provider")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found in environment. "
                    "Ensure it's set in ~/.env.d/*.env or ~/.env"
                )
            self.client = OpenAI(api_key=api_key)
        elif provider == AnalysisProvider.OLLAMA:
            if not HAVE_REQUESTS:
                raise ImportError("requests package required for Ollama provider")

    def retry_with_backoff(:
        self, func, max_attempts: int = 4, base_delay: float = 1.0, cap: float = 10.0
    ):
        """Exponential backoff with full jitter."""
        for attempt in range(1, max_attempts + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts:
                    raise
                sleep_time = min(cap, base_delay * (2 ** (attempt - 1)))
                sleep_time = random.uniform(0, sleep_time)
                logger.warning(
                    f"Attempt {attempt} failed with {e!r}; waiting {sleep_time:.2f}s before retry."
                )
                time.sleep(sleep_time)

    def analyze_openai(:
        self,
        transcript: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1500,
        temperature: float = 0.7,
    ) -> Optional[str]:
        """Analyze transcript using OpenAI GPT."""
        prompt_config = self.PROMPTS[self.analysis_type]

        def _call():
            return self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt_config["system"]},
                    {
                        "role": "user",
                        "content": prompt_config["user_template"].format(
                            transcript=transcript
                        ),
                    },
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )

        try:
            response = self.retry_with_backoff(_call, max_attempts=3)
            choice = response.choices[0]
            content = (
                getattr(choice.message, "content", None)
                if hasattr(choice, "message")
                else choice.text
            )
            return content.strip() if content else None
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return None

    def analyze_ollama(:
        self,
        transcript: str,
        model: str = "llama3.1:8b-instruct",
        timeout: int = 600,
    ) -> Optional[str]:
        """Analyze transcript using Ollama (local)."""
        # OLLAMA_HOST can be set in ~/.env.d/*.env or ~/.env
        ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        url = f"{ollama_host.rstrip('/')}/api/generate"

        prompt_config = self.PROMPTS[self.analysis_type]
        prompt = (
            f"{prompt_config['system']}\n\n"
            f"{prompt_config['user_template'].format(transcript=transcript)}\n\n"
            "Return a structured analysis with section headers."
        )

        try:
            resp = requests.post(
                url,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response") or json.dumps(data, indent=2)
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
            return None

    def analyze(:
        self, transcript: str, model: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """Analyze transcript using configured provider."""
        if self.provider == AnalysisProvider.OPENAI:
            return self.analyze_openai(
                transcript, model=model or "gpt-3.5-turbo", **kwargs
            )
        else:
            return self.analyze_ollama(
                transcript, model=model or "llama3.1:8b-instruct", **kwargs
            )

    def analyze_file(:
        self,
        transcript_path: Path,
        output_path: Optional[Path] = None,
        model: Optional[str] = None,
    ) -> Optional[str]:
        """Analyze transcript from file."""
        if not transcript_path.exists():
            logger.error(f"Transcript file not found: {transcript_path}")
            return None

        transcript = transcript_path.read_text(encoding="utf-8")
        analysis = self.analyze(transcript, model=model)

        if analysis and output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(analysis, encoding="utf-8")
            logger.info(f"Analysis saved to {output_path}")

        return analysis

    def batch_analyze(:
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        force: bool = False,
        model: Optional[str] = None,
    ) -> Dict[Path, Optional[str]]:
        """Analyze all transcript files in a directory."""
        if not output_dir:
            output_dir = input_dir / "analysis"
        output_dir.mkdir(parents=True, exist_ok=True)

        results = {}
        transcript_files = list(input_dir.rglob("*.txt")) + list(
            input_dir.rglob("*.transcript")
        )

        logger.info(f"Found {len(transcript_files)} transcript files")

        for transcript_path in transcript_files:
            try:
                output_path = output_dir / f"{transcript_path.stem}_analysis.txt"

                if output_path.exists() and not force:
                    logger.info(f"Skipping {transcript_path.name} (already exists)")
                    continue

                analysis = self.analyze_file(transcript_path, output_path, model=model)
                results[transcript_path] = analysis

                if analysis:
                    logger.info(f"✓ Analyzed {transcript_path.name}")

            except Exception as e:
                logger.error(f"Error analyzing {transcript_path}: {e}")
                results[transcript_path] = None

        return results


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Unified Transcript Analyzer")
    parser.add_argument("input", help="Input transcript file or directory")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama"],
        default="openai",
        help="Analysis provider (default: openai)",
    )
    parser.add_argument(
        "--type",
        choices=["general", "music", "video", "podcast"],
        default="general",
        help="Analysis type (default: general)",
    )
    parser.add_argument(
        "--model",
        help="Model name (gpt-3.5-turbo for OpenAI, llama3.1:8b-instruct for Ollama)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process directory in batch mode",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess existing analyses",
    )

    args = parser.parse_args()

    try:
        provider = AnalysisProvider(args.provider)
        analysis_type = AnalysisType(args.type)
        analyzer = TranscriptAnalyzer(provider=provider, analysis_type=analysis_type)
    except (ImportError, ValueError) as e:
        logger.error(f"Failed to initialize analyzer: {e}")
        return

    input_path = Path(args.input)

    if input_path.is_file() and not args.batch:
        output_path = (
            Path(args.output)
            if args.output
            else input_path.parent / f"{input_path.stem}_analysis.txt"
        )
        analysis = analyzer.analyze_file(input_path, output_path, model=args.model)
        if analysis:
            print(analysis)

    elif input_path.is_dir() or args.batch:
        output_dir = Path(args.output) if args.output else input_path / "analysis"
        results = analyzer.batch_analyze(
            input_path, output_dir, force=args.force, model=args.model
        )
        logger.info(
            f"Analyzed {len([r for r in results.values() if r])} files. Results saved to {output_dir}"
        )

    else:
        logger.error(f"Invalid input: {input_path}")


if __name__ == "__main__":
    main()
