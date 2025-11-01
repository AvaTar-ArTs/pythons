"""
Script 61

This module provides functionality for script 61.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_480 = 480
CONSTANT_600 = 600
CONSTANT_720 = 720
CONSTANT_854 = 854
CONSTANT_1080 = 1080
CONSTANT_1280 = 1280
CONSTANT_1800 = 1800
CONSTANT_1920 = 1920
CONSTANT_2000 = 2000
CONSTANT_2025 = 2025
CONSTANT_2160 = 2160
CONSTANT_3840 = 3840
CONSTANT_44100 = 44100
CONSTANT_48000 = 48000
CONSTANT_2000000 = 2000000
CONSTANT_5000000 = 5000000

#!/usr/bin/env python3
"""
Enhanced Content Analyzer with Deep Read and Content-Awareness

This script implements advanced content analysis capabilities including:
- Multi-modal analysis (visual + audio + text)
- Content classification and sentiment analysis
- Complexity scoring and engagement prediction
- Cross-modal correlation analysis
- Intelligent content organization
"""

import os
import json
import csv
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class EnhancedContentAnalyzer:
    def __init__(self, movies_dir: str):
        """__init__ function."""

        self.movies_dir = Path(movies_dir)
        self.analysis_dir = self.movies_dir / "analysis"
        self.output_dir = self.movies_dir / "enhanced_analysis"
        self.output_dir.mkdir(exist_ok=True)

        # Enhanced content patterns
        self.content_patterns = {
            "ai_generated": [
                r"assets_task_.*\.mp4",
                r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}.*\.mp4",
                r".*genid_.*\.mp4",
                r".*sora.*\.mp4",
                r".*ai.*art.*\.mp4",
            ],
            "gaming": [
                r".*ESO.*\.(mp4|mkv|webm)",
                r".*Elder Scrolls.*\.(mp4|mkv|webm)",
                r".*gaming.*\.(mp4|mkv|webm)",
                r".*stream.*\.(mp4|mkv|webm)",
                r".*gameplay.*\.(mp4|mkv|webm)",
                r".*trailer.*\.(mp4|mkv|webm)",
            ],
            "music": [
                r".*audio.*\.(mp3|m4a|wav)",
                r".*music.*\.(mp3|m4a|wav)",
                r".*song.*\.(mp3|m4a|wav)",
                r".*dance.*\.(mp4|gif)",
                r".*beat.*\.(mp3|m4a|wav)",
            ],
            "creative": [
                r".*art.*\.(mp4|gif)",
                r".*creative.*\.(mp4|gif)",
                r".*animation.*\.(mp4|gif)",
                r".*dance.*\.(mp4|gif)",
                r".*visual.*\.(mp4|gif)",
                r".*loop.*\.(mp4|gif)",
            ],
            "political": [
                r".*project.*CONSTANT_2025.*",
                r".*political.*",
                r".*conservative.*",
                r".*heritage.*",
                r".*government.*",
            ],
            "educational": [
                r".*tutorial.*\.(mp4|mov)",
                r".*how.*to.*\.(mp4|mov)",
                r".*guide.*\.(mp4|mov)",
                r".*lesson.*\.(mp4|mov)",
                r".*educational.*\.(mp4|mov)",
            ],
            "entertainment": [
                r".*comedy.*\.(mp4|mov)",
                r".*funny.*\.(mp4|mov)",
                r".*entertainment.*\.(mp4|mov)",
                r".*show.*\.(mp4|mov)",
            ],
        }

        # Enhanced sentiment analysis
        self.sentiment_keywords = {
            "positive": [
                "joy",
                "happy",
                "uplifting",
                "inspiring",
                "beautiful",
                "amazing",
                "wonderful",
                "exciting",
                "fantastic",
                "brilliant",
                "excellent",
                "great",
                "awesome",
                "love",
                "enjoy",
                "pleasure",
                "delight",
                "celebration",
                "success",
                "achievement",
            ],
            "negative": [
                "sad",
                "dark",
                "horror",
                "scary",
                "depressing",
                "angry",
                "fear",
                "terrible",
                "awful",
                "bad",
                "hate",
                "disappointing",
                "frustrating",
                "painful",
                "tragic",
                "disturbing",
                "upsetting",
                "worried",
                "concerned",
                "problem",
                "issue",
            ],
            "neutral": [
                "informative",
                "educational",
                "tutorial",
                "documentary",
                "news",
                "factual",
                "objective",
                "analytical",
                "technical",
                "procedural",
                "instructional",
                "explanatory",
                "descriptive",
                "informational",
            ],
            "energetic": [
                "dynamic",
                "energetic",
                "fast",
                "intense",
                "powerful",
                "dramatic",
                "action",
                "movement",
                "rhythm",
                "beat",
                "pulse",
                "vibrant",
                "lively",
                "active",
            ],
            "calm": [
                "peaceful",
                "calm",
                "serene",
                "gentle",
                "soft",
                "quiet",
                "relaxing",
                "meditative",
                "contemplative",
                "slow",
                "smooth",
                "tranquil",
                "zen",
            ],
        }

        # Visual style keywords
        self.visual_style_keywords = {
            "cinematic": ["cinematic", "movie", "film", "cinema", "dramatic", "epic"],
            "minimalist": ["minimal", "simple", "clean", "minimalist", "basic"],
            "colorful": ["colorful", "vibrant", "bright", "color", "rainbow", "vivid"],
            "dark": ["dark", "gloomy", "shadow", "black", "night", "moody"],
            "retro": ["retro", "vintage", "old", "classic", "nostalgic", "80s", "90s"],
            "futuristic": ["futuristic", "sci-fi", "cyber", "digital", "tech", "modern"],
        }

    def extract_enhanced_metadata(self, video_path: Path) -> Dict[str, Any]:
        """Extract comprehensive metadata from video files."""
        try:
            cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(video_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                format_info = data.get("format", {})
                streams = data.get("streams", [])

                # Find video and audio streams
                video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
                audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

                # Calculate aspect ratio
                width = int(video_stream.get("width", 0))
                height = int(video_stream.get("height", 0))
                aspect_ratio = width / height if height > 0 else 0

                # Determine resolution category
                resolution_category = self.categorize_resolution(width, height)

                # Calculate quality score
                quality_score = self.calculate_quality_score(video_stream, audio_stream)

                return {
                    "duration": float(format_info.get("duration", 0)),
                    "file_size": int(format_info.get("size", 0)),
                    "bit_rate": int(format_info.get("bit_rate", 0)),
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(aspect_ratio, 2),
                    "resolution_category": resolution_category,
                    "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                    "codec": video_stream.get("codec_name", "unknown"),
                    "audio_codec": audio_stream.get("codec_name", "unknown"),
                    "audio_channels": int(audio_stream.get("channels", 0)),
                    "audio_sample_rate": int(audio_stream.get("sample_rate", 0)),
                    "quality_score": quality_score,
                    "has_audio": bool(audio_stream),
                    "has_video": bool(video_stream),
                }
        except Exception as e:
            logger.warning(f"Could not extract metadata for {video_path}: {e}")

        return {}

    def categorize_resolution(self, width: int, height: int) -> str:
        """Categorize video resolution."""
        if width >= CONSTANT_3840 or height >= CONSTANT_2160:
            return "4K"
        elif width >= CONSTANT_1920 or height >= CONSTANT_1080:
            return "HD"
        elif width >= CONSTANT_1280 or height >= CONSTANT_720:
            return "HD_720"
        elif width >= CONSTANT_854 or height >= CONSTANT_480:
            return "SD"
        else:
            return "Low"

    def calculate_quality_score(self, video_stream: Dict, audio_stream: Dict) -> float:
        """Calculate overall quality score based on technical parameters."""
        score = 0

        # Video quality factors
        if video_stream:
            width = int(video_stream.get("width", 0))
            height = int(video_stream.get("height", 0))
            bit_rate = int(video_stream.get("bit_rate", 0))

            # Resolution score (0-3)
            if width >= CONSTANT_1920 and height >= CONSTANT_1080:
                score += 3
            elif width >= CONSTANT_1280 and height >= CONSTANT_720:
                score += 2
            elif width >= CONSTANT_854 and height >= CONSTANT_480:
                score += 1

            # Bitrate score (0-2)
            if bit_rate > CONSTANT_5000000:  # > 5 Mbps
                score += 2
            elif bit_rate > CONSTANT_2000000:  # > 2 Mbps
                score += 1

        # Audio quality factors
        if audio_stream:
            sample_rate = int(audio_stream.get("sample_rate", 0))
            channels = int(audio_stream.get("channels", 0))

            # Sample rate score (0-2)
            if sample_rate >= CONSTANT_48000:
                score += 2
            elif sample_rate >= CONSTANT_44100:
                score += 1

            # Channel score (0-1)
            if channels >= 2:
                score += 1

        return min(score / 8, 1.0)  # Normalize to 0-1

    def classify_content_type(self, filename: str, metadata: Dict[str, Any]) -> str:
        """Enhanced content type classification."""
        filename_lower = filename.lower()

        # Check filename patterns
        for content_type, patterns in self.content_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    return content_type

        # Additional classification based on metadata
        duration = metadata.get("duration", 0)
        has_audio = metadata.get("has_audio", False)
        has_video = metadata.get("has_video", False)

        # Short videos might be clips or GIFs
        if duration < 30 and has_video:
            return "short_clip"

        # Long videos might be documentaries or movies
        if duration > CONSTANT_1800:  # 30 minutes
            return "long_form"

        # Videos without audio might be silent films or visual content
        if has_video and not has_audio:
            return "silent_visual"

        return "unknown"

    def analyze_sentiment_enhanced(self, analysis_text: str, filename: str) -> Dict[str, Any]:
        """Enhanced sentiment analysis with multiple dimensions."""
        analysis_lower = analysis_text.lower()
        filename_lower = filename.lower()

        # Calculate sentiment scores
        sentiment_scores = {}
        for sentiment, keywords in self.sentiment_keywords.items():
            score = sum(1 for keyword in keywords if keyword in analysis_lower)
            sentiment_scores[sentiment] = score

        # Calculate filename sentiment
        filename_sentiment = 0
        for sentiment, keywords in self.sentiment_keywords.items():
            filename_sentiment += sum(1 for keyword in keywords if keyword in filename_lower)

        # Determine primary sentiment
        total_score = sum(sentiment_scores.values())
        if total_score > 0:
            primary_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[primary_sentiment] / total_score
        else:
            primary_sentiment = "neutral"
            confidence = 0.5

        # Calculate sentiment intensity
        intensity = min(total_score / 10, 1.0)  # Normalize to 0-1

        return {
            "primary_sentiment": primary_sentiment,
            "sentiment_confidence": round(confidence, 3),
            "sentiment_intensity": round(intensity, 3),
            "sentiment_scores": sentiment_scores,
            "filename_sentiment": filename_sentiment,
        }

    def analyze_visual_style(self, analysis_text: str, filename: str) -> Dict[str, Any]:
        """Analyze visual style characteristics."""
        text_lower = analysis_text.lower()
        filename_lower = filename.lower()

        style_scores = {}
        for style, keywords in self.visual_style_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            score += sum(1 for keyword in keywords if keyword in filename_lower)
            style_scores[style] = score

        # Determine primary visual style
        if sum(style_scores.values()) > 0:
            primary_style = max(style_scores, key=style_scores.get)
        else:
            primary_style = "unknown"

        return {"primary_visual_style": primary_style, "visual_style_scores": style_scores}

    def calculate_complexity_enhanced(self, analysis_text: str, metadata: Dict[str, Any]) -> Dict[str, float]:
        """Enhanced complexity calculation with multiple dimensions."""
        duration = metadata.get("duration", 0)
        file_size = metadata.get("file_size", 0)
        quality_score = metadata.get("quality_score", 0)

        # Text complexity
        analysis_length = len(analysis_text)
        word_count = len(analysis_text.split())
        sentence_count = len(re.findall(r"[.!?]+", analysis_text))

        # Theme complexity
        theme_count = len(re.findall(r"\*\*.*?\*\*", analysis_text))

        # Technical complexity
        technical_terms = len(
            re.findall(
                r"\b(technical|artistic|visual|audio|narrative|structure|technique|method|approach)\b",
                analysis_text.lower(),
            )
        )

        # Calculate complexity scores
        text_complexity = min(analysis_length / CONSTANT_2000, 5)  # Cap at 5
        duration_complexity = min(duration / CONSTANT_300, 3)  # Cap at 3
        theme_complexity = min(theme_count / 3, 2)  # Cap at 2
        technical_complexity = min(technical_terms / 5, 2)  # Cap at 2

        # Overall complexity
        overall_complexity = (text_complexity + duration_complexity + theme_complexity + technical_complexity) / 4

        return {
            "overall_complexity": round(overall_complexity, 2),
            "text_complexity": round(text_complexity, 2),
            "duration_complexity": round(duration_complexity, 2),
            "theme_complexity": round(theme_complexity, 2),
            "technical_complexity": round(technical_complexity, 2),
            "word_count": word_count,
            "sentence_count": sentence_count,
            "theme_count": theme_count,
        }

    def calculate_engagement_potential(
        self, metadata: Dict[str, Any], sentiment: Dict[str, Any], complexity: Dict[str, Any], content_type: str
    ) -> float:
        """Calculate engagement potential based on multiple factors."""
        factors = []

        # Duration factor (optimal range: 30 seconds to 10 minutes)
        duration = metadata.get("duration", 0)
        if 30 <= duration <= CONSTANT_600:  # 30 seconds to 10 minutes
            factors.append(1.0)
        elif duration < 30:
            factors.append(0.7)  # Too short
        elif duration <= CONSTANT_1800:  # Up to 30 minutes
            factors.append(0.8)  # Getting long
        else:
            factors.append(0.5)  # Very long

        # Quality factor
        quality_score = metadata.get("quality_score", 0)
        factors.append(quality_score)

        # Resolution factor
        resolution = metadata.get("resolution_category", "Low")
        resolution_scores = {"4K": 1.0, "HD": 0.9, "HD_720": 0.7, "SD": 0.5, "Low": 0.3}
        factors.append(resolution_scores.get(resolution, 0.3))

        # Sentiment factor
        sentiment_intensity = sentiment.get("sentiment_intensity", 0)
        factors.append(sentiment_intensity)

        # Complexity factor (moderate complexity is best)
        complexity_score = complexity.get("overall_complexity", 0)
        if 2 <= complexity_score <= 6:
            factors.append(1.0)
        else:
            factors.append(0.7)

        # Content type factor
        type_scores = {
            "ai_generated": 0.9,
            "creative": 0.8,
            "gaming": 0.7,
            "music": 0.8,
            "educational": 0.6,
            "entertainment": 0.9,
            "short_clip": 0.8,
            "unknown": 0.5,
        }
        factors.append(type_scores.get(content_type, 0.5))

        return round(sum(factors) / len(factors), 3)

    def extract_themes_enhanced(self, analysis_text: str) -> List[str]:
        """Extract themes with enhanced pattern matching."""
        themes = []

        # Extract from themes section
        theme_patterns = [r"themes?[:\s]*(.*?)(?:\n|$)", r"messages?[:\s]*(.*?)(?:\n|$)", r"ideas?[:\s]*(.*?)(?:\n|$)"]

        for pattern in theme_patterns:
            matches = re.findall(pattern, analysis_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by common separators
                theme_list = re.split(r"[,;]", match)
                themes.extend([theme.strip() for theme in theme_list if theme.strip()])

        # Extract from bold text (likely themes)
        bold_matches = re.findall(r"\*\*(.*?)\*\*", analysis_text)
        themes.extend([match.strip() for match in bold_matches if match.strip()])

        # Remove duplicates and limit to top 10
        unique_themes = list(dict.fromkeys(themes))[:10]
        return unique_themes

    def process_video_enhanced(self, video_path: Path) -> Dict[str, Any]:
        """Process a video file with enhanced analysis."""
        filename = video_path.name
        file_stem = video_path.stem

        # Basic file info
        file_info = {
            "filename": filename,
            "file_path": str(video_path.relative_to(self.movies_dir)),
            "file_size": video_path.stat().st_size,
            "creation_date": datetime.fromtimestamp(video_path.stat().st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modification_date": datetime.fromtimestamp(video_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "file_extension": video_path.suffix.lower(),
            "directory": str(video_path.parent.relative_to(self.movies_dir)),
        }

        # Extract enhanced metadata
        metadata = self.extract_enhanced_metadata(video_path)
        file_info.update(metadata)

        # Content classification
        content_type = self.classify_content_type(filename, metadata)
        file_info["content_type"] = content_type

        # Look for analysis file
        analysis_file = self.analysis_dir / f"{file_stem}_analysis.txt"
        if analysis_file.exists():
            try:
                with open(analysis_file, "r", encoding="utf-8") as f:
                    analysis_text = f.read()

                # Enhanced sentiment analysis
                sentiment_data = self.analyze_sentiment_enhanced(analysis_text, filename)
                file_info.update(sentiment_data)

                # Visual style analysis
                visual_style = self.analyze_visual_style(analysis_text, filename)
                file_info.update(visual_style)

                # Enhanced complexity analysis
                complexity_data = self.calculate_complexity_enhanced(analysis_text, metadata)
                file_info.update(complexity_data)

                # Extract themes
                themes = self.extract_themes_enhanced(analysis_text)
                file_info["themes"] = "; ".join(themes)

                # Calculate engagement potential
                engagement = self.calculate_engagement_potential(
                    metadata, sentiment_data, complexity_data, content_type
                )
                file_info["engagement_potential"] = engagement

                file_info["has_analysis"] = True
                file_info["analysis_length"] = len(analysis_text)

            except Exception as e:
                logger.warning(f"Could not process analysis file {analysis_file}: {e}")
                file_info["has_analysis"] = False
        else:
            file_info["has_analysis"] = False

        return file_info

    def generate_enhanced_csv(self):
        """Generate enhanced CSV with all improvements."""
        logger.info("Starting enhanced CSV generation with improvements...")

        # Find all video files
        video_extensions = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".wmv", ".flv", ".m4v"}
        video_files = []

        for ext in video_extensions:
            video_files.extend(self.movies_dir.rglob(f"*{ext}"))

        logger.info(f"Found {len(video_files)} video files to process")

        # Process each video file
        all_data = []
        for i, video_path in enumerate(video_files):
            if i % 50 == 0:
                logger.info(f"Processing file {i+1}/{len(video_files)}: {video_path.name}")

            try:
                file_data = self.process_video_enhanced(video_path)
                all_data.append(file_data)
            except Exception as e:
                logger.error(f"Error processing {video_path}: {e}")
                continue

        # Enhanced CSV columns
        columns = [
            "filename",
            "file_path",
            "file_size",
            "creation_date",
            "modification_date",
            "file_extension",
            "directory",
            "content_type",
            "duration",
            "width",
            "height",
            "aspect_ratio",
            "resolution_category",
            "fps",
            "codec",
            "bit_rate",
            "audio_codec",
            "audio_channels",
            "audio_sample_rate",
            "quality_score",
            "has_audio",
            "has_video",
            "has_analysis",
            "analysis_length",
            "themes",
            "primary_sentiment",
            "sentiment_confidence",
            "sentiment_intensity",
            "primary_visual_style",
            "overall_complexity",
            "text_complexity",
            "duration_complexity",
            "theme_complexity",
            "technical_complexity",
            "word_count",
            "sentence_count",
            "theme_count",
            "engagement_potential",
        ]

        # Write enhanced CSV
        output_csv = self.output_dir / "enhanced_content_analysis_improved.csv"
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

            for data in all_data:
                row = {col: data.get(col, "") for col in columns}
                writer.writerow(row)

        logger.info(f"Enhanced CSV generated: {output_csv}")
        logger.info(f"Processed {len(all_data)} files")

        # Generate enhanced summary
        self.generate_enhanced_summary(all_data)

        return output_csv

    def generate_enhanced_summary(self, data: List[Dict[str, Any]]):
        """Generate enhanced summary statistics."""
        total_files = len(data)
        analyzed_files = sum(1 for d in data if d.get("has_analysis", False))

        # Content type distribution
        content_types = {}
        for item in data:
            content_type = item.get("content_type", "unknown")
            content_types[content_type] = content_types.get(content_type, 0) + 1

        # Sentiment distribution
        sentiments = {}
        for item in data:
            sentiment = item.get("primary_sentiment", "unknown")
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1

        # Visual style distribution
        visual_styles = {}
        for item in data:
            style = item.get("primary_visual_style", "unknown")
            visual_styles[style] = visual_styles.get(style, 0) + 1

        # Calculate averages
        avg_complexity = statistics.mean([d.get("overall_complexity", 0) for d in data])
        avg_engagement = statistics.mean([d.get("engagement_potential", 0) for d in data])
        avg_quality = statistics.mean([d.get("quality_score", 0) for d in data])

        # Write enhanced summary
        summary_file = self.output_dir / "enhanced_analysis_summary.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("ENHANCED CONTENT ANALYSIS SUMMARY\n")
            f.write("=" * 60 + Path("\n\n"))
            f.write(f"Total Files Processed: {total_files}\n")
            f.write(f"Files with Analysis: {analyzed_files} ({analyzed_files/total_files*CONSTANT_100:.1f}%)\n")
            f.write(f"Average Complexity Score: {avg_complexity:.2f}/10\n")
            f.write(f"Average Engagement Potential: {avg_engagement:.2f}/1\n")
            f.write(f"Average Quality Score: {avg_quality:.2f}/1\n\n")

            f.write("CONTENT TYPE DISTRIBUTION:\n")
            f.write("-" * 40 + Path("\n"))
            for content_type, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
                percentage = count / total_files * CONSTANT_100
                f.write(f"{content_type}: {count} files ({percentage:.1f}%)\n")

            f.write("\nSENTIMENT DISTRIBUTION:\n")
            f.write("-" * 40 + Path("\n"))
            for sentiment, count in sorted(sentiments.items(), key=lambda x: x[1], reverse=True):
                percentage = count / total_files * CONSTANT_100
                f.write(f"{sentiment}: {count} files ({percentage:.1f}%)\n")

            f.write("\nVISUAL STYLE DISTRIBUTION:\n")
            f.write("-" * 40 + Path("\n"))
            for style, count in sorted(visual_styles.items(), key=lambda x: x[1], reverse=True):
                percentage = count / total_files * CONSTANT_100
                f.write(f"{style}: {count} files ({percentage:.1f}%)\n")

        logger.info(f"Enhanced summary saved to: {summary_file}")


def main():
    """Main function to run the enhanced analyzer."""
    movies_dir = Path("/Users/steven/Movies")

    if not os.path.exists(movies_dir):
        logger.error(f"Movies directory not found: {movies_dir}")
        return

    analyzer = EnhancedContentAnalyzer(movies_dir)
    csv_file = analyzer.generate_enhanced_csv()

    logger.info(f"\n✅ Enhanced CSV with improvements generated successfully!")
    logger.info(f"📁 Location: {csv_file}")
    logger.info(f"📊 Check enhanced_analysis/ for detailed statistics")


if __name__ == "__main__":
    main()
