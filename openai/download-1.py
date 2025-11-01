"""
Script 156

This module provides functionality for script 156.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1200 = 1200
CONSTANT_1500 = 1500

#!/usr/bin/env python3
"""
Advanced Content Analyzer - Consolidated Analysis Script

This script consolidates all analysis functionality from multiple analysis scripts
into a comprehensive, feature-rich content analysis tool.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor
import time

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored
from tqdm import tqdm

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("content_analysis.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AdvancedContentAnalyzer:
    """Comprehensive content analysis tool with multiple analysis modes."""

    def __init__(self):
        """__init__ function."""

        self.client = client
        self.analysis_modes = {
            "basic": self._basic_analysis,
            "detailed": self._detailed_analysis,
            "multimedia": self._multimedia_analysis,
            "shorts": self._shorts_analysis,
            "transcript": self._transcript_analysis,
        }

    def _basic_analysis(self, text: str, context: str = "") -> str:
        """Basic content analysis."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert content analyzer. Provide a concise analysis of the given content.",
                },
                {"role": "user", "content": f"Analyze this content:\n\n{text}"},
            ],
            max_tokens=CONSTANT_500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def _detailed_analysis(self, text: str, context: str = "") -> str:
        """Detailed content analysis with comprehensive evaluation."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
                        "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
                        "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
                        "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following content: {text}\n\n"
                        "Provide a comprehensive analysis covering:\n\n"
                        "1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed.\n"
                        "2. **Emotional Tone**: What emotions are evoked, and how are they conveyed?\n"
                        "3. **Narrative Arc**: Describe how this content contributes to the overall story or progression.\n"
                        "4. **Creator's Intent**: What is the likely purpose or message the creator is trying to communicate?\n"
                        "5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable elements that enhance meaning.\n"
                        "6. **Storytelling Techniques**: Identify specific techniques used.\n"
                        "7. **Interplay Between Visuals and Audio**: Analyze how different elements work together.\n"
                        "8. **Audience Engagement and Impact**: Evaluate effectiveness in engaging viewers.\n"
                        "9. **Overall Effectiveness**: Summarize how these elements combine for impact."
                    ),
                },
            ],
            max_tokens=CONSTANT_1500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def _multimedia_analysis(self, text: str, context: str = "") -> str:
        """Multimedia-specific analysis focusing on audio-visual synergy."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in multimedia analysis. Focus on the synergy between audio and visual elements, "
                        "identifying central themes, emotional tones, narrative progression, and artistic intent. "
                        "Highlight how visual elements such as imagery, colors, and transitions interact with audio elements "
                        "like dialogue, music, and sound effects to convey meaning and evoke emotions."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this multimedia content: {text}\n\nContext: {context}",
                },
            ],
            max_tokens=CONSTANT_1200,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()

    def _shorts_analysis(self, text: str, context: str = "") -> str:
        """YouTube Shorts-specific analysis."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in short-form video content analysis. Focus on quick engagement, "
                        "viral potential, and the unique characteristics of short-form content. Analyze pacing, "
                        "hook effectiveness, and audience retention strategies."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this YouTube Shorts content: {text}\n\nContext: {context}",
                },
            ],
            max_tokens=CONSTANT_1000,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()

    def _transcript_analysis(self, text: str, context: str = "") -> str:
        """Transcript-specific analysis with timing considerations."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in transcript analysis. Focus on spoken content, dialogue patterns, "
                        "speaker characteristics, and the flow of conversation. Consider timing, pauses, and "
                        "conversational dynamics."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this transcript: {text}\n\nContext: {context}",
                },
            ],
            max_tokens=CONSTANT_1200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def analyze_content(
        self, text: str, mode: str = "detailed", context: str = ""
    ) -> str:
        """Analyze content using the specified mode."""
        if mode not in self.analysis_modes:
            raise ValueError(
                f"Invalid analysis mode: {mode}. Available modes: {list(self.analysis_modes.keys())}"
            )

        try:
            return self.analysis_modes[mode](text, context)
        except Exception as e:
            logger.error(f"Error in {mode} analysis: {e}")
            return f"Analysis failed: {str(e)}"

    def batch_analyze(
        self,
        files: List[Path],
        mode: str = "detailed",
        output_dir: Optional[Path] = None,
    ) -> Dict[Path, str]:
        """Analyze multiple files in batch."""
        if output_dir:
            output_dir.mkdir(exist_ok=True)

        results = {}

        for file_path in tqdm(files, desc="Analyzing files"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                analysis = self.analyze_content(content, mode, str(file_path))
                results[file_path] = analysis

                if output_dir:
                    output_file = output_dir / f"{file_path.stem}_analysis.txt"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(analysis)

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = f"Error: {str(e)}"

        return results


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Content Analyzer")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument(
        "-m",
        "--mode",
        choices=["basic", "detailed", "multimedia", "shorts", "transcript"],
        default="detailed",
        help="Analysis mode",
    )
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--text", help="Analyze text directly")

    args = parser.parse_args()

    analyzer = AdvancedContentAnalyzer()

    if args.text:
        result = analyzer.analyze_content(args.text, args.mode)
        logger.info(result)
    else:
        input_path = Path(args.input)
        if input_path.is_file():
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
            result = analyzer.analyze_content(content, args.mode, str(input_path))
            logger.info(result)
        elif input_path.is_dir():
            files = list(input_path.rglob("*.txt")) + list(input_path.rglob("*.md"))
            output_dir = (
                Path(args.output) if args.output else input_path / "analysis_output"
            )
            results = analyzer.batch_analyze(files, args.mode, output_dir)
            logger.info(f"Analyzed {len(results)} files. Results saved to {output_dir}")
        else:
            logger.info(f"Invalid input: {input_path}")


if __name__ == "__main__":
    main()
