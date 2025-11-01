
# Constants
CONSTANT_300 = 300
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1200 = 1200
CONSTANT_1500 = 1500

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/consolidate_scripts.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/core_analysis/consolidate_scripts.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from termcolor import colored
from tqdm import tqdm
from typing import Dict, List, Optional, Union
from typing import Dict, List, Set, Tuple
import argparse
import csv
import hashlib
import json
import logging
import os
import pandas as pd
import shutil
import subprocess
import sys
import time

# Documentation from source files
        """Transcribe audio with detailed timestamps."""
        """Generate HTML album pages from song data."""
                html_content = f"""
        """Find files with identical content."""
        """Convert MP4 to MP3 using ffmpeg."""
        """Detailed content analysis with comprehensive evaluation."""
    """Comprehensive content generation tool with multiple generation modes."""
        """Create a report of the consolidation process."""
        """Generate quiz questions from transcript."""
        """Convert seconds to MM:SS format."""
    """Main function."""
        """Analyze multiple files in batch."""
        """Analyze content using the specified mode."""
    """Main function for command-line usage."""
        """Generate description for image using GPT-4 Vision."""
        """Merge all generation scripts into a comprehensive generator."""
        """YouTube Shorts-specific analysis."""
        """Generate descriptions for multiple images."""
    """Comprehensive content analysis tool with multiple analysis modes."""
        """Transcribe all audio files in a directory."""
        """Split audio into smaller segments."""
        """Calculate MD5 hash of file content."""
        """Create consolidated directory structure."""
        """Generate CSV from HTML song data."""
        """Merge all transcription scripts into a comprehensive transcriber."""
"""
        """Merge all analysis scripts into a comprehensive analyzer."""
        """Transcribe audio file using OpenAI Whisper."""
        """Main consolidation process."""
        """Basic content analysis."""
        """Transcript-specific analysis with timing considerations."""
    """Comprehensive transcription tool with multiple processing modes."""
        """Generate video content description."""
        """Remove duplicate files and keep only the best versions."""
        """Multimedia-specific analysis focusing on audio-visual synergy."""

Script Consolidation and Duplicate Removal Tool

This script consolidates, merges, and removes duplicates from the Python music processing scripts.
It creates optimized, consolidated versions with the best features from similar scripts.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScriptConsolidator:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.sorted_dir = self.base_dir / "Sorted"
        self.consolidated_dir = self.base_dir / "Consolidated"
        
        # Create consolidated directory structure
        self.consolidated_categories = {
            "analysis": "Content Analysis",
            "transcription": "Transcription & Speech",
            "generation": "Content Generation", 
            "processing": "File Processing",
            "web_scraping": "Web Scraping",
            "organization": "File Organization",
            "utilities": "Utilities"
        }
        
        # File hash cache for duplicate detection
        self.file_hashes = {}
        
        # Duplicate groups identified
        self.duplicate_groups = {
            "analyze_variants": [
                "analyze.py", "analyze 1.py", "analyze-1.py", "analyze_1.py",
                "analyze 2.py", "analyze 6.py", "analyze11.py", "analyze (1).py"
            ],
            "analyze_prompts": [
                "analyze-prompt.py", "analyze-prompt (1).py", "analyze-prompt_1.py",
                "analyze-prompt1.py", "analyze-promptr.py", "analyze-prompts.py",
                "analyze-prompts_1.py"
            ],
            "analyze_mp3": [
                "analyze-mp3-transcript-prompts.py", "analyze-mp3-transcript-prompts (1).py",
                "analyze-mp3-transcript-prompts_1.py"
            ],
            "analyze_shorts": [
                "analyze-shorts.py", "analyze-shorts_1.py", "analyze-shorts-info.py",
                "analyze-shorts-info_1.py"
            ],
            "transcribe_variants": [
                "transcribe.py", "transcribe (1).py", "transcribe 1.py", "transcribe_mp3.py"
            ],
            "generate_speech": [
                "generate_speech.py", "generate_speech 2.py", "generate_speech 2 (1).py",
                "generate_speech 2 2.py"
            ],
            "generate_csv": [
                "generate_song_csv.py", "generate_song_csv (1).py", "generate_songs_csv.py",
                "generate_songs_csv 1.py", "generate_songs_csv_1.py"
            ],
            "generate_album": [
                "generate_album_pages.py", "generate_album_html-pages.py",
                "generate_album_html-pages_fixed.py"
            ],
            "mp3_processing": [
                "mp3.py", "mp3_processor.py", "mp3_to_mp4.py", "mp3-mp4-coverimg.py",
                "mp3-mp4-coverimg copy.py", "Mp3toMp4ximg.py"
            ],
            "mp4_processing": [
                "mp4-mp4.py", "mp4tomp3.py", "mp4-transcript.py", "mp4-transcript_1.py"
            ],
            "suno_variants": [
                "suno-song-info.py", "suno-extract-song.py", "suno-csv-card-html-seo.py",
                "suno-csv-card-html-seo1.py", "suno-csv-card-html-seo2.py"
            ],
            "cover_processing": [
                "cover.py", "cover2.py"
            ],
            "quiz_variants": [
                "Quiz22s.py", "Quiz22sec.py", "QuizPrompts.py", "quiz-20.py"
            ]
        }

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def find_exact_duplicates(self) -> Dict[str, List[Path]]:
        """Find files with identical content."""
        hash_to_files = {}
        
        for category_dir in self.sorted_dir.iterdir():
            if category_dir.is_dir() and category_dir.name != "deprecated":
                for file_path in category_dir.glob("*.py"):
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        if file_hash not in hash_to_files:
                            hash_to_files[file_hash] = []
                        hash_to_files[file_hash].append(file_path)
        
        # Return only groups with duplicates
        return {h: files for h, files in hash_to_files.items() if len(files) > 1}

    def create_consolidated_directories(self):
        """Create consolidated directory structure."""
        logger.info("Creating consolidated directory structure...")
        
        # Create main consolidated directory
        self.consolidated_dir.mkdir(exist_ok=True)
        
        # Create category directories
        for category, description in self.consolidated_categories.items():
            category_dir = self.consolidated_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Create README for each category
            readme_path = category_dir / "README.md"
            with open(readme_path, 'w') as f:
                f.write(f"# {description}\n\n")
                f.write(f"Consolidated scripts for {description.lower()}.\n\n")
                f.write("## Consolidated Scripts:\n")
        
        logger.info("Consolidated directory structure created")

    def merge_analysis_scripts(self):
        """Merge all analysis scripts into a comprehensive analyzer."""
        logger.info("Merging analysis scripts...")
        
        # Find the best analysis script (largest, most complete)
        analysis_files = []
        for variant in self.duplicate_groups["analyze_variants"]:
            for category_dir in self.sorted_dir.iterdir():
                if category_dir.is_dir() and category_dir.name == "analysis":
                    file_path = category_dir / variant
                    if file_path.exists():
                        analysis_files.append(file_path)
        
        # Also include other analysis scripts
        for category_dir in self.sorted_dir.iterdir():
            if category_dir.is_dir() and category_dir.name == "analysis":
                for file_path in category_dir.glob("*.py"):
                    if file_path.name not in ["README.md"] and file_path not in analysis_files:
                        analysis_files.append(file_path)
        
        # Create consolidated analysis script
        consolidated_analyzer = self.consolidated_dir / "analysis" / "advanced_content_analyzer.py"
        
        with open(consolidated_analyzer, 'w') as f:
            f.write('''#!/usr/bin/env python3
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
    handlers=[
        logging.FileHandler("content_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedContentAnalyzer:
    """Comprehensive content analysis tool with multiple analysis modes."""
    
    def __init__(self):
        self.client = client
        self.analysis_modes = {
            "basic": self._basic_analysis,
            "detailed": self._detailed_analysis,
            "multimedia": self._multimedia_analysis,
            "shorts": self._shorts_analysis,
            "transcript": self._transcript_analysis
        }
    
    def _basic_analysis(self, text: str, context: str = "") -> str:
        """Basic content analysis."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert content analyzer. Provide a concise analysis of the given content."
                },
                {
                    "role": "user",
                    "content": f"Analyze this content:\\n\\n{text}"
                }
            ],
            max_tokens=CONSTANT_500,
            temperature=0.7
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
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following content: {text}\\n\\n"
                        "Provide a comprehensive analysis covering:\\n\\n"
                        "1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed.\\n"
                        "2. **Emotional Tone**: What emotions are evoked, and how are they conveyed?\\n"
                        "3. **Narrative Arc**: Describe how this content contributes to the overall story or progression.\\n"
                        "4. **Creator's Intent**: What is the likely purpose or message the creator is trying to communicate?\\n"
                        "5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable elements that enhance meaning.\\n"
                        "6. **Storytelling Techniques**: Identify specific techniques used.\\n"
                        "7. **Interplay Between Visuals and Audio**: Analyze how different elements work together.\\n"
                        "8. **Audience Engagement and Impact**: Evaluate effectiveness in engaging viewers.\\n"
                        "9. **Overall Effectiveness**: Summarize how these elements combine for impact."
                    )
                }
            ],
            max_tokens=CONSTANT_1500,
            temperature=0.7
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
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze this multimedia content: {text}\\n\\nContext: {context}"
                }
            ],
            max_tokens=CONSTANT_1200,
            temperature=0.8
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
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze this YouTube Shorts content: {text}\\n\\nContext: {context}"
                }
            ],
            max_tokens=CONSTANT_1000,
            temperature=0.8
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
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze this transcript: {text}\\n\\nContext: {context}"
                }
            ],
            max_tokens=CONSTANT_1200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def analyze_content(self, text: str, mode: str = "detailed", context: str = "") -> str:
        """Analyze content using the specified mode."""
        if mode not in self.analysis_modes:
            raise ValueError(f"Invalid analysis mode: {mode}. Available modes: {list(self.analysis_modes.keys())}")
        
        try:
            return self.analysis_modes[mode](text, context)
        except Exception as e:
            logger.error(f"Error in {mode} analysis: {e}")
            return f"Analysis failed: {str(e)}"
    
    def batch_analyze(self, files: List[Path], mode: str = "detailed", output_dir: Optional[Path] = None) -> Dict[Path, str]:
        """Analyze multiple files in batch."""
        if output_dir:
            output_dir.mkdir(exist_ok=True)
        
        results = {}
        
        for file_path in tqdm(files, desc="Analyzing files"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                analysis = self.analyze_content(content, mode, str(file_path))
                results[file_path] = analysis
                
                if output_dir:
                    output_file = output_dir / f"{file_path.stem}_analysis.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(analysis)
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = f"Error: {str(e)}"
        
        return results

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Content Analyzer")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-m", "--mode", choices=["basic", "detailed", "multimedia", "shorts", "transcript"], 
                       default="detailed", help="Analysis mode")
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
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            result = analyzer.analyze_content(content, args.mode, str(input_path))
            logger.info(result)
        elif input_path.is_dir():
            files = list(input_path.rglob("*.txt")) + list(input_path.rglob("*.md"))
            output_dir = Path(args.output) if args.output else input_path / "analysis_output"
            results = analyzer.batch_analyze(files, args.mode, output_dir)
            logger.info(f"Analyzed {len(results)} files. Results saved to {output_dir}")
        else:
            logger.info(f"Invalid input: {input_path}")

if __name__ == "__main__":
    main()
''')
        
        logger.info(f"Created consolidated analyzer: {consolidated_analyzer}")

    def merge_transcription_scripts(self):
        """Merge all transcription scripts into a comprehensive transcriber."""
        logger.info("Merging transcription scripts...")
        
        consolidated_transcriber = self.consolidated_dir / "transcription" / "advanced_transcriber.py"
        
        with open(consolidated_transcriber, 'w') as f:
            f.write('''#!/usr/bin/env python3
"""
Advanced Transcriber - Consolidated Transcription Script

This script consolidates all transcription functionality from multiple transcription scripts
into a comprehensive, feature-rich transcription tool.
"""

import os
import sys
import logging
import argparse
import subprocess
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
    handlers=[
        logging.FileHandler("transcription.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedTranscriber:
    """Comprehensive transcription tool with multiple processing modes."""
    
    def __init__(self):
        self.client = client
        self.supported_formats = ['.mp3', '.mp4', '.wav', '.m4a', '.flac']
    
    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def transcribe_audio(self, file_path: Path, model: str = "whisper-1", 
                        response_format: str = "verbose_json") -> Optional[Dict]:
        """Transcribe audio file using OpenAI Whisper."""
        try:
            with open(file_path, "rb") as audio_file:
                logger.info(f"Transcribing {file_path.name}...")
                transcript_data = client.audio.transcribe(
                    model=model,
                    file=audio_file,
                    response_format=response_format
                )
                return transcript_data
        except Exception as e:
            logger.error(f"Error transcribing {file_path}: {e}")
            return None
    
    def transcribe_with_timestamps(self, file_path: Path) -> Optional[str]:
        """Transcribe audio with detailed timestamps."""
        transcript_data = self.transcribe_audio(file_path)
        if not transcript_data:
            return None
        
        transcript_with_timestamps = []
        for segment in transcript_data.segments:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(
                f"{self.format_timestamp(start_time)} -- {self.format_timestamp(end_time)}: {text}"
            )
        
        return Path("\\n").join(transcript_with_timestamps)
    
    def convert_mp4_to_mp3(self, mp4_path: Path) -> Optional[Path]:
        """Convert MP4 to MP3 using ffmpeg."""
        mp3_path = mp4_path.with_suffix('.mp3')
        if mp3_path.exists():
            return mp3_path
        
        try:
            subprocess.run([
                "ffmpeg", "-i", str(mp4_path), "-q:a", "0", "-map", "a", str(mp3_path)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"Converted {mp4_path.name} to MP3")
            return mp3_path
        except Exception as e:
            logger.error(f"Error converting {mp4_path}: {e}")
            return None
    
    def split_audio(self, file_path: Path, segment_length: int = CONSTANT_300) -> List[Path]:
        """Split audio into smaller segments."""
        output_dir = file_path.parent / "segments"
        output_dir.mkdir(exist_ok=True)
        
        file_name_no_ext = file_path.stem
        command = [
            "ffmpeg", "-i", str(file_path), "-f", "segment",
            "-segment_time", str(segment_length), "-c", "copy",
            str(output_dir / f"{file_name_no_ext}_%03d.mp3")
        ]
        
        try:
            subprocess.run(command, check=True)
            return sorted(list(output_dir.glob("*.mp3")))
        except Exception as e:
            logger.error(f"Error splitting {file_path}: {e}")
            return []
    
    def batch_transcribe(self, input_dir: Path, output_dir: Optional[Path] = None) -> Dict[Path, str]:
        """Transcribe all audio files in a directory."""
        if not output_dir:
            output_dir = input_dir / "transcripts"
        output_dir.mkdir(exist_ok=True)
        
        results = {}
        audio_files = []
        
        # Find all audio files
        for ext in self.supported_formats:
            audio_files.extend(input_dir.rglob(f"*{ext}"))
        
        for file_path in tqdm(audio_files, desc="Transcribing files"):
            try:
                # Convert MP4 to MP3 if needed
                if file_path.suffix.lower() == '.mp4':
                    mp3_path = self.convert_mp4_to_mp3(file_path)
                    if mp3_path:
                        file_path = mp3_path
                
                # Transcribe
                transcript = self.transcribe_with_timestamps(file_path)
                if transcript:
                    output_file = output_dir / f"{file_path.stem}_transcript.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(transcript)
                    results[file_path] = transcript
                    logger.info(f"Transcribed {file_path.name}")
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = f"Error: {str(e)}"
        
        return results
    
    def generate_quiz_from_transcript(self, transcript: str, num_questions: int = 5) -> str:
        """Generate quiz questions from transcript."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"Generate {num_questions} quiz questions based on the following transcript. Make questions that test comprehension and key concepts."
                    },
                    {
                        "role": "user",
                        "content": f"Transcript:\\n{transcript}"
                    }
                ],
                max_tokens=CONSTANT_1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return f"Quiz generation failed: {str(e)}"

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Transcriber")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--convert", action="store_true", help="Convert MP4 to MP3 first")
    parser.add_argument("--split", type=int, help="Split audio into segments of specified length")
    parser.add_argument("--quiz", type=int, help="Generate quiz with specified number of questions")
    
    args = parser.parse_args()
    
    transcriber = AdvancedTranscriber()
    input_path = Path(args.input)
    
    if input_path.is_file():
        if args.convert and input_path.suffix.lower() == '.mp4':
            mp3_path = transcriber.convert_mp4_to_mp3(input_path)
            if mp3_path:
                input_path = mp3_path
        
        if args.split:
            segments = transcriber.split_audio(input_path, args.split)
            logger.info(f"Split into {len(segments)} segments")
            for segment in segments:
                logger.info(f"  {segment}")
        
        transcript = transcriber.transcribe_with_timestamps(input_path)
        if transcript:
            logger.info(transcript)
            
            if args.quiz:
                quiz = transcriber.generate_quiz_from_transcript(transcript, args.quiz)
                logger.info(Path("\\n") + "="*50)
                logger.info("QUIZ QUESTIONS:")
                logger.info("="*50)
                logger.info(quiz)
    
    elif input_path.is_dir():
        output_dir = Path(args.output) if args.output else input_path / "transcripts"
        results = transcriber.batch_transcribe(input_path, output_dir)
        logger.info(f"Transcribed {len(results)} files. Results saved to {output_dir}")
    
    else:
        logger.info(f"Invalid input: {input_path}")

if __name__ == "__main__":
    main()
''')
        
        logger.info(f"Created consolidated transcriber: {consolidated_transcriber}")

    def merge_generation_scripts(self):
        """Merge all generation scripts into a comprehensive generator."""
        logger.info("Merging generation scripts...")
        
        consolidated_generator = self.consolidated_dir / "generation" / "advanced_content_generator.py"
        
        with open(consolidated_generator, 'w') as f:
            f.write('''#!/usr/bin/env python3
"""
Advanced Content Generator - Consolidated Generation Script

This script consolidates all content generation functionality from multiple generation scripts
into a comprehensive, feature-rich content generation tool.
"""

import os
import sys
import logging
import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd
from bs4 import BeautifulSoup

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("content_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedContentGenerator:
    """Comprehensive content generation tool with multiple generation modes."""
    
    def __init__(self):
        self.client = client
    
    def generate_song_csv(self, html_files: List[Path], output_path: Path) -> bool:
        """Generate CSV from HTML song data."""
        try:
            song_details = []
            
            for html_file in html_files:
                with open(html_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, "html.parser")
                for item in soup.find_all("div", class_="css-79jxux"):
                    title_element = item.find("span", class_="text-primary")
                    song_url_element = item.find("a", href=True)
                    cover_url_element = item.find_previous_sibling("img", src=True)
                    genre_element = item.find("a", class_="hover:underline", href=True)
                    time_element = item.find("span", class_="text-mono")
                    
                    song_details.append({
                        "Song Title": title_element["title"] if title_element else "",
                        "Time": time_element.text.strip() if time_element else "",
                        "Genre": genre_element.text.strip() if genre_element else "",
                        "Song URL": song_url_element["href"] if song_url_element else "",
                        "Cover URL": cover_url_element["src"] if cover_url_element else "",
                        "Lyrics": "",
                        "Info": "",
                        "Keys": ""
                    })
            
            df = pd.DataFrame(song_details)
            df.to_csv(output_path, index=False)
            logger.info(f"Generated CSV with {len(song_details)} songs: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating song CSV: {e}")
            return False
    
    def generate_album_pages(self, song_data: List[Dict], output_dir: Path) -> bool:
        """Generate HTML album pages from song data."""
        try:
            output_dir.mkdir(exist_ok=True)
            
            for i, song in enumerate(song_data):
                html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{song.get('Song Title', 'Unknown')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .song-info {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .cover {{ max-width: 300px; height: auto; }}
    </style>
</head>
<body>
    <div class="song-info">
        <h1>{song.get('Song Title', 'Unknown')}</h1>
        <img src="{song.get('Cover URL', '')}" alt="Cover" class="cover">
        <p><strong>Genre:</strong> {song.get('Genre', 'Unknown')}</p>
        <p><strong>Duration:</strong> {song.get('Time', 'Unknown')}</p>
        <p><strong>URL:</strong> <a href="{song.get('Song URL', '')}">Listen</a></p>
        <p><strong>Lyrics:</strong> {song.get('Lyrics', 'Not available')}</p>
    </div>
</body>
</html>
"""
                output_file = output_dir / f"song_{i+1:03d}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            logger.info(f"Generated {len(song_data)} album pages in {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating album pages: {e}")
            return False
    
    def generate_image_description(self, image_url: str) -> str:
        """Generate description for image using GPT-4 Vision."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Create a detailed and descriptive image prompt for this image as if you were to recreate it."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=CONSTANT_300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating image description: {e}")
            return f"Description generation failed: {str(e)}"
    
    def generate_video_content(self, prompt: str, duration: int = 30) -> str:
        """Generate video content description."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a video content creator. Generate detailed video content based on the given prompt."
                    },
                    {
                        "role": "user",
                        "content": f"Create video content for: {prompt}\\nDuration: {duration} seconds"
                    }
                ],
                max_tokens=CONSTANT_500,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating video content: {e}")
            return f"Video generation failed: {str(e)}"
    
    def batch_generate_descriptions(self, image_urls: List[str], output_file: Path) -> bool:
        """Generate descriptions for multiple images."""
        try:
            descriptions = []
            
            for url in image_urls:
                description = self.generate_image_description(url)
                descriptions.append({"url": url, "description": description})
            
            df = pd.DataFrame(descriptions)
            df.to_csv(output_file, index=False)
            logger.info(f"Generated descriptions for {len(descriptions)} images: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error batch generating descriptions: {e}")
            return False

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Content Generator")
    parser.add_argument("--mode", choices=["csv", "html", "image", "video"], required=True,
                       help="Generation mode")
    parser.add_argument("--input", help="Input file or directory")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument("--urls", nargs="+", help="Image URLs for description generation")
    parser.add_argument("--prompt", help="Content prompt")
    
    args = parser.parse_args()
    
    generator = AdvancedContentGenerator()
    
    if args.mode == "csv" and args.input and args.output:
        html_files = [Path(f) for f in args.input.split(",")]
        generator.generate_song_csv(html_files, Path(args.output))
    
    elif args.mode == "html" and args.input and args.output:
        # Load song data from CSV
        df = pd.read_csv(args.input)
        song_data = df.to_dict('records')
        generator.generate_album_pages(song_data, Path(args.output))
    
    elif args.mode == "image" and args.urls and args.output:
        generator.batch_generate_descriptions(args.urls, Path(args.output))
    
    elif args.mode == "video" and args.prompt and args.output:
        content = generator.generate_video_content(args.prompt)
        with open(args.output, 'w') as f:
            f.write(content)
        logger.info(f"Video content generated: {args.output}")
    
    else:
        logger.info("Invalid arguments. Use --help for usage information.")

if __name__ == "__main__":
    main()
''')
        
        logger.info(f"Created consolidated generator: {consolidated_generator}")

    def remove_duplicates(self):
        """Remove duplicate files and keep only the best versions."""
        logger.info("Removing duplicate files...")
        
        # Find exact duplicates
        exact_duplicates = self.find_exact_duplicates()
        
        # Create archive directory for duplicates
        archive_dir = self.consolidated_dir / "archived_duplicates"
        archive_dir.mkdir(exist_ok=True)
        
        removed_count = 0
        
        for file_hash, files in exact_duplicates.items():
            if len(files) > 1:
                # Keep the largest file (most complete)
                files.sort(key=lambda x: x.stat().st_size, reverse=True)
                keep_file = files[0]
                duplicates = files[1:]
                
                logger.info(f"Keeping: {keep_file}")
                logger.info(f"Removing {len(duplicates)} duplicates")
                
                for duplicate in duplicates:
                    # Move to archive instead of deleting
                    archive_path = archive_dir / duplicate.name
                    counter = 1
                    while archive_path.exists():
                        archive_path = archive_dir / f"{duplicate.stem}_{counter}{duplicate.suffix}"
                        counter += 1
                    
                    shutil.move(str(duplicate), str(archive_path))
                    removed_count += 1
        
        logger.info(f"Removed {removed_count} duplicate files (archived in {archive_dir})")

    def consolidate_scripts(self):
        """Main consolidation process."""
        logger.info("Starting script consolidation process...")
        
        # Create consolidated directories
        self.create_consolidated_directories()
        
        # Merge scripts by category
        self.merge_analysis_scripts()
        self.merge_transcription_scripts()
        self.merge_generation_scripts()
        
        # Remove duplicates
        self.remove_duplicates()
        
        # Create summary report
        self.create_consolidation_report()
        
        logger.info("Script consolidation completed successfully!")

    def create_consolidation_report(self):
        """Create a report of the consolidation process."""
        report_path = self.consolidated_dir / "CONSOLIDATION_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write("# Script Consolidation Report\n\n")
            f.write(f"Generated: {os.popen('date').read().strip()}\n\n")
            
            f.write("## Summary\n\n")
            f.write("This report documents the consolidation of Python music processing scripts.\n\n")
            
            f.write("## Consolidated Scripts\n\n")
            f.write("### Analysis\n")
            f.write("- `advanced_content_analyzer.py` - Comprehensive content analysis tool\n\n")
            
            f.write("### Transcription\n")
            f.write("- `advanced_transcriber.py` - Comprehensive transcription tool\n\n")
            
            f.write("### Generation\n")
            f.write("- `advanced_content_generator.py` - Comprehensive content generation tool\n\n")
            
            f.write("## Duplicate Removal\n\n")
            f.write("Duplicate files have been identified and archived in the `archived_duplicates` directory.\n\n")
            
            f.write("## Usage\n\n")
            f.write("Each consolidated script can be used independently or as part of a larger workflow.\n")
            f.write("See individual script documentation for detailed usage instructions.\n")

def main():
    """Main function."""
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/python")
    consolidator = ScriptConsolidator(base_dir)
    consolidator.consolidate_scripts()

if __name__ == "__main__":
    main()