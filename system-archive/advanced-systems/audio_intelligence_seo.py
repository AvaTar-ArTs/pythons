#!/usr/bin/env python3
"""
🎵 AUDIO INTELLIGENCE & SEO ANALYZER
====================================
AI-powered audio analysis, metadata extraction, and SEO optimization.

Features:
✨ AI-powered audio transcription & analysis
🎼 Metadata extraction (ID3, MP3, FLAC, etc.)
🔍 SEO-optimized descriptions & keywords
📊 Audio quality analysis (bitrate, sample rate, format)
🎯 Genre, mood, and tempo detection
🏷️ Smart tagging and categorization
📝 Automatic title and description generation
🔗 Podcast RSS feed metadata
📦 Batch processing for music libraries
🎨 Album art analysis integration
🌐 Web audio optimization recommendations
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import re
import hashlib

# Audio processing
try:
    import mutagen
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.wave import WAVE
    from mutagen.oggvorbis import OggVorbis
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("⚠️  Mutagen not available. Install: pip install mutagen")

# API Clients
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

import base64
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AudioIntelligence:
    """
    Intelligent audio analysis and SEO optimization system
    """

    def __init__(self):
        self.load_environment()
        self.initialize_clients()
        self.supported_formats = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma', '.opus'}

    def load_environment(self):
        """Load API keys from ~/.env.d/"""
        env_paths = [
            Path.home() / ".env.d" / "llm-apis.env",
            Path.home() / ".env.d" / "audio-music.env",
            Path.home() / ".env.d" / "gemini.env",
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                logger.info(f"✅ Loaded environment from {env_path}")

    def initialize_clients(self):
        """Initialize AI clients"""
        self.clients = {}

        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.clients['openai'] = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("✅ OpenAI (Whisper + GPT-4) initialized")

        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.clients['anthropic'] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            logger.info("✅ Anthropic Claude initialized")

        if GEMINI_AVAILABLE and os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.clients['gemini'] = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Google Gemini initialized")

        # Check for audio-specific APIs
        if os.getenv("DEEPGRAM_API_KEY"):
            logger.info("✅ Deepgram API key found (transcription)")

        if os.getenv("ASSEMBLYAI_API_KEY"):
            logger.info("✅ AssemblyAI API key found (transcription)")

        if not self.clients:
            logger.warning("⚠️  No AI clients available. Analysis will be limited.")

    # ============================================================================
    # 🔍 AUDIO ANALYSIS
    # ============================================================================

    async def analyze_audio(self, audio_path: Path) -> Dict[str, Any]:
        """
        Comprehensive audio analysis
        Returns technical details, AI analysis, and SEO recommendations
        """
        if not audio_path.exists():
            return {'error': 'Audio file not found'}

        result = {
            'file_path': str(audio_path),
            'file_name': audio_path.name,
            'analyzed_at': datetime.now().isoformat()
        }

        # Technical analysis
        result['technical'] = await self._analyze_technical(audio_path)

        # Metadata extraction
        result['metadata'] = self._extract_metadata(audio_path)

        # AI analysis (transcription + content analysis)
        result['ai_analysis'] = await self._analyze_with_ai(audio_path)

        # SEO optimization
        result['seo'] = await self._generate_seo_metadata(audio_path, result)

        # Quality score
        result['quality_score'] = self._calculate_quality_score(result)

        # Recommendations
        result['recommendations'] = self._generate_recommendations(result)

        return result

    async def _analyze_technical(self, audio_path: Path) -> Dict[str, Any]:
        """Extract technical audio information"""
        technical = {}

        try:
            if MUTAGEN_AVAILABLE:
                audio = mutagen.File(audio_path)

                if audio:
                    # Basic info
                    technical['format'] = audio.mime[0] if hasattr(audio, 'mime') else 'unknown'
                    technical['duration_seconds'] = getattr(audio.info, 'length', 0)
                    technical['duration_formatted'] = str(timedelta(seconds=int(technical['duration_seconds'])))

                    # Audio quality
                    technical['bitrate'] = getattr(audio.info, 'bitrate', 0)
                    technical['bitrate_kbps'] = round(technical['bitrate'] / 1000, 1) if technical['bitrate'] else 0
                    technical['sample_rate'] = getattr(audio.info, 'sample_rate', 0)
                    technical['channels'] = getattr(audio.info, 'channels', 0)

                    # File size
                    file_size = audio_path.stat().st_size
                    technical['file_size_bytes'] = file_size
                    technical['file_size_kb'] = round(file_size / 1024, 2)
                    technical['file_size_mb'] = round(file_size / (1024 * 1024), 2)

                    # Quality indicators
                    technical['is_lossless'] = audio_path.suffix.lower() in ['.flac', '.wav']
                    technical['is_high_quality'] = technical['bitrate_kbps'] >= 320 if technical['bitrate_kbps'] else False

            else:
                # Fallback without Mutagen
                file_size = audio_path.stat().st_size
                technical['file_size_bytes'] = file_size
                technical['file_size_kb'] = round(file_size / 1024, 2)
                technical['file_size_mb'] = round(file_size / (1024 * 1024), 2)
                technical['format'] = audio_path.suffix

        except Exception as e:
            logger.error(f"Technical analysis failed: {e}")
            technical['error'] = str(e)

        return technical

    def _extract_metadata(self, audio_path: Path) -> Dict[str, Any]:
        """Extract ID3 tags and other metadata"""
        metadata = {}

        try:
            if MUTAGEN_AVAILABLE:
                audio = mutagen.File(audio_path, easy=True)

                if audio:
                    # Common tags
                    metadata['title'] = audio.get('title', [''])[0] if 'title' in audio else ''
                    metadata['artist'] = audio.get('artist', [''])[0] if 'artist' in audio else ''
                    metadata['album'] = audio.get('album', [''])[0] if 'album' in audio else ''
                    metadata['genre'] = audio.get('genre', [''])[0] if 'genre' in audio else ''
                    metadata['date'] = audio.get('date', [''])[0] if 'date' in audio else ''
                    metadata['comment'] = audio.get('comment', [''])[0] if 'comment' in audio else ''

                    # Additional tags
                    metadata['album_artist'] = audio.get('albumartist', [''])[0] if 'albumartist' in audio else ''
                    metadata['composer'] = audio.get('composer', [''])[0] if 'composer' in audio else ''
                    metadata['bpm'] = audio.get('bpm', [''])[0] if 'bpm' in audio else ''

                    # Check for cover art
                    metadata['has_cover_art'] = self._check_cover_art(audio_path)

        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            metadata['error'] = str(e)

        return metadata

    def _check_cover_art(self, audio_path: Path) -> bool:
        """Check if audio file has embedded cover art"""
        try:
            if MUTAGEN_AVAILABLE:
                audio = mutagen.File(audio_path)

                # Check MP3
                if isinstance(audio, MP3):
                    return 'APIC:' in audio or len([k for k in audio.keys() if k.startswith('APIC')]) > 0

                # Check FLAC
                elif isinstance(audio, FLAC):
                    return len(audio.pictures) > 0

                # Check OGG
                elif isinstance(audio, OggVorbis):
                    return 'metadata_block_picture' in audio

        except:
            pass

        return False

    async def _analyze_with_ai(self, audio_path: Path) -> Dict[str, Any]:
        """
        Analyze audio using AI
        Includes transcription, genre detection, mood analysis
        """
        analysis = {}

        try:
            # Transcribe if speech audio
            transcription = await self._transcribe_audio(audio_path)
            if transcription:
                analysis['transcription'] = transcription

                # Analyze transcription
                content_analysis = await self._analyze_audio_content(transcription)
                analysis.update(content_analysis)

            # If no transcription, infer from filename and metadata
            if not transcription:
                analysis = self._infer_from_metadata(audio_path)

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            analysis['error'] = str(e)
            analysis = self._infer_from_metadata(audio_path)

        return analysis

    async def _transcribe_audio(self, audio_path: Path) -> Optional[str]:
        """Transcribe audio using Whisper or similar"""
        try:
            # Check file size (Whisper has 25MB limit)
            file_size_mb = audio_path.stat().st_size / (1024 * 1024)

            if file_size_mb > 25:
                logger.warning(f"File too large for transcription: {file_size_mb:.1f}MB")
                return None

            # Use OpenAI Whisper
            if 'openai' in self.clients:
                logger.info("Transcribing audio with Whisper...")

                with open(audio_path, 'rb') as audio_file:
                    response = self.clients['openai'].audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )

                return response if isinstance(response, str) else response.text

        except Exception as e:
            logger.error(f"Transcription failed: {e}")

        return None

    async def _analyze_audio_content(self, transcription: str) -> Dict[str, Any]:
        """Analyze audio content from transcription"""
        try:
            if 'anthropic' in self.clients:
                prompt = f"""Analyze this audio transcription and provide:

Transcription:
{transcription[:2000]}

Provide:
1. Content type (podcast, music, speech, interview, audiobook, etc.)
2. Main topics/themes (comma-separated)
3. Genre/category
4. Mood/tone
5. Target audience
6. SEO keywords (10 keywords)
7. Brief description (2-3 sentences)

Format as JSON with keys: content_type, topics, genre, mood, audience, keywords, description"""

                response = await self.clients['anthropic'].messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )

                content = response.content[0].text

                # Try to parse JSON
                try:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

                # Fallback to text parsing
                return {
                    'description': content[:500],
                    'provider': 'anthropic'
                }

        except Exception as e:
            logger.error(f"Content analysis failed: {e}")

        return {}

    def _infer_from_metadata(self, audio_path: Path) -> Dict[str, Any]:
        """Infer basic info from filename and metadata"""
        name = audio_path.stem
        metadata = self._extract_metadata(audio_path)

        # Clean filename
        clean_name = re.sub(r'[_-]', ' ', name)
        clean_name = re.sub(r'\d+', '', clean_name).strip()

        analysis = {
            'description': f"Audio: {metadata.get('title') or clean_name}",
            'inferred_title': metadata.get('title') or clean_name,
            'inferred_artist': metadata.get('artist', ''),
            'inferred_genre': metadata.get('genre', ''),
            'provider': 'metadata'
        }

        # Infer content type from filename/folder
        path_lower = str(audio_path).lower()
        if any(word in path_lower for word in ['podcast', 'episode', 'ep']):
            analysis['content_type'] = 'podcast'
        elif any(word in path_lower for word in ['music', 'song', 'track']):
            analysis['content_type'] = 'music'
        elif any(word in path_lower for word in ['speech', 'talk', 'lecture']):
            analysis['content_type'] = 'speech'
        else:
            analysis['content_type'] = 'audio'

        return analysis

    # ============================================================================
    # 🌐 SEO OPTIMIZATION
    # ============================================================================

    async def _generate_seo_metadata(self, audio_path: Path, analysis: Dict) -> Dict[str, Any]:
        """Generate SEO-optimized metadata for audio"""
        seo = {}
        metadata = analysis.get('metadata', {})
        ai = analysis.get('ai_analysis', {})

        # Title
        seo['title'] = self._generate_seo_title(audio_path, metadata, ai)

        # Description
        seo['description'] = self._generate_description(metadata, ai)

        # Keywords
        seo['keywords'] = self._extract_audio_keywords(metadata, ai)

        # SEO-friendly filename
        seo['suggested_filename'] = self._generate_seo_filename(audio_path, metadata, ai)

        # Audio schema markup
        seo['schema_org'] = self._generate_audio_schema(audio_path, seo, analysis)

        # Podcast-specific metadata (if applicable)
        if ai.get('content_type') == 'podcast':
            seo['podcast_metadata'] = self._generate_podcast_metadata(analysis)

        return seo

    def _generate_seo_title(self, audio_path: Path, metadata: Dict, ai: Dict) -> str:
        """Generate SEO-optimized title"""
        # Priority: existing title > AI title > filename
        if metadata.get('title'):
            title = metadata['title']
        elif ai.get('inferred_title'):
            title = ai['inferred_title']
        else:
            title = audio_path.stem.replace('_', ' ').replace('-', ' ').title()

        # Add artist if available
        artist = metadata.get('artist') or ai.get('inferred_artist')
        if artist:
            title = f"{artist} - {title}"

        return title[:100]

    def _generate_description(self, metadata: Dict, ai: Dict) -> str:
        """Generate description"""
        description = ai.get('description', '')

        if not description:
            # Build from metadata
            parts = []
            if metadata.get('artist'):
                parts.append(f"By {metadata['artist']}")
            if metadata.get('album'):
                parts.append(f"from the album {metadata['album']}")
            if metadata.get('genre'):
                parts.append(f"Genre: {metadata['genre']}")

            description = '. '.join(parts) if parts else "Audio track"

        return description[:300]

    def _extract_audio_keywords(self, metadata: Dict, ai: Dict) -> List[str]:
        """Extract SEO keywords"""
        keywords = set()

        # From AI analysis
        if 'keywords' in ai:
            if isinstance(ai['keywords'], list):
                keywords.update(ai['keywords'])
            elif isinstance(ai['keywords'], str):
                keywords.update(ai['keywords'].split(','))

        # From metadata
        if metadata.get('artist'):
            keywords.add(metadata['artist'].lower())
        if metadata.get('album'):
            keywords.add(metadata['album'].lower())
        if metadata.get('genre'):
            keywords.add(metadata['genre'].lower())

        # From topics
        if ai.get('topics'):
            topics = ai['topics'].split(',') if isinstance(ai['topics'], str) else ai['topics']
            keywords.update([t.strip().lower() for t in topics])

        # Clean and return
        cleaned = [kw.strip().lower() for kw in keywords if kw.strip()]
        return sorted(list(set(cleaned)))[:15]

    def _generate_seo_filename(self, audio_path: Path, metadata: Dict, ai: Dict) -> str:
        """Generate SEO-friendly filename"""
        # Use title or artist-title
        if metadata.get('title') and metadata.get('artist'):
            base = f"{metadata['artist']}-{metadata['title']}"
        elif metadata.get('title'):
            base = metadata['title']
        elif ai.get('inferred_title'):
            base = ai['inferred_title']
        else:
            base = audio_path.stem

        # Clean and format
        base = re.sub(r'[^a-z0-9\s-]', '', base.lower())
        base = re.sub(r'\s+', '-', base).strip('-')
        base = re.sub(r'-+', '-', base)

        return f"{base}{audio_path.suffix}"

    def _generate_audio_schema(self, audio_path: Path, seo: Dict, analysis: Dict) -> Dict[str, Any]:
        """Generate Schema.org AudioObject markup"""
        technical = analysis.get('technical', {})

        schema = {
            "@context": "https://schema.org",
            "@type": "AudioObject",
            "name": seo.get('title', ''),
            "description": seo.get('description', ''),
            "contentUrl": str(audio_path.name),
            "encodingFormat": technical.get('format', ''),
            "duration": f"PT{int(technical.get('duration_seconds', 0))}S"
        }

        # Add metadata if available
        metadata = analysis.get('metadata', {})
        if metadata.get('artist'):
            schema['creator'] = metadata['artist']

        if seo.get('keywords'):
            schema['keywords'] = ', '.join(seo['keywords'])

        return schema

    def _generate_podcast_metadata(self, analysis: Dict) -> Dict[str, Any]:
        """Generate podcast-specific metadata for RSS feeds"""
        return {
            'episode_type': 'full',
            'explicit': 'no',  # Would need content analysis to determine
            'duration': analysis.get('technical', {}).get('duration_formatted', ''),
            'subtitle': analysis.get('ai_analysis', {}).get('description', '')[:255]
        }

    # ============================================================================
    # 📊 QUALITY SCORING
    # ============================================================================

    def _calculate_quality_score(self, analysis: Dict) -> Dict[str, Any]:
        """Calculate audio quality score (0-100)"""
        scores = {}
        technical = analysis.get('technical', {})
        metadata = analysis.get('metadata', {})
        seo = analysis.get('seo', {})

        # Technical Quality (0-35 points)
        tech_score = 0

        # Bitrate
        bitrate = technical.get('bitrate_kbps', 0)
        if bitrate >= 320 or technical.get('is_lossless'):
            tech_score += 15
        elif bitrate >= 256:
            tech_score += 12
        elif bitrate >= 192:
            tech_score += 9
        elif bitrate >= 128:
            tech_score += 6
        else:
            tech_score += 3

        # Sample rate
        sample_rate = technical.get('sample_rate', 0)
        if sample_rate >= 48000:
            tech_score += 10
        elif sample_rate >= 44100:
            tech_score += 8
        elif sample_rate >= 32000:
            tech_score += 5
        else:
            tech_score += 2

        # Format
        if technical.get('is_lossless'):
            tech_score += 10
        elif technical.get('format') == 'audio/mp3':
            tech_score += 7
        else:
            tech_score += 5

        scores['technical'] = min(tech_score, 35)

        # Metadata Quality (0-30 points)
        meta_score = 0

        if metadata.get('title'):
            meta_score += 10
        if metadata.get('artist'):
            meta_score += 10
        if metadata.get('album'):
            meta_score += 5
        if metadata.get('genre'):
            meta_score += 3
        if metadata.get('has_cover_art'):
            meta_score += 2

        scores['metadata'] = min(meta_score, 30)

        # SEO Quality (0-35 points)
        seo_score = 0

        # Title
        title = seo.get('title', '')
        if len(title) > 10 and len(title) < 100:
            seo_score += 12
        elif title:
            seo_score += 8

        # Description
        desc = seo.get('description', '')
        if len(desc) > 50:
            seo_score += 12
        elif desc:
            seo_score += 6

        # Keywords
        keywords = seo.get('keywords', [])
        if len(keywords) >= 5:
            seo_score += 11
        elif len(keywords) >= 3:
            seo_score += 7
        elif keywords:
            seo_score += 3

        scores['seo'] = min(seo_score, 35)

        # Total
        total = sum(scores.values())

        return {
            'total_score': round(total, 1),
            'grade': self._get_grade(total),
            'breakdown': scores
        }

    def _get_grade(self, score: float) -> str:
        """Convert score to grade"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Average)"
        else:
            return "D (Needs Improvement)"

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        technical = analysis.get('technical', {})
        metadata = analysis.get('metadata', {})
        seo = analysis.get('seo', {})

        # Technical recommendations
        bitrate = technical.get('bitrate_kbps', 0)
        if bitrate < 192:
            recommendations.append("⚠️ Quality: Consider re-encoding at 256-320 kbps for better quality")

        file_size_mb = technical.get('file_size_mb', 0)
        if file_size_mb > 50:
            recommendations.append("🗜️ Optimization: Large file size. Consider compression for web streaming")

        # Metadata recommendations
        if not metadata.get('title'):
            recommendations.append("🏷️ Metadata: Add title tag for better organization")

        if not metadata.get('artist'):
            recommendations.append("👤 Metadata: Add artist/creator information")

        if not metadata.get('has_cover_art'):
            recommendations.append("🎨 Cover Art: Add album/cover art for better presentation")

        if not metadata.get('genre'):
            recommendations.append("🎼 Genre: Add genre tag for better categorization")

        # SEO recommendations
        if len(seo.get('keywords', [])) < 5:
            recommendations.append("🔍 SEO: Add more relevant keywords for discoverability")

        desc = seo.get('description', '')
        if len(desc) < 50:
            recommendations.append("📝 Description: Add detailed description (100-300 characters)")

        # Filename
        suggested = seo.get('suggested_filename', '')
        if suggested and suggested != Path(analysis['file_name']).name:
            recommendations.append(f"📁 Filename: Rename to '{suggested}' for better SEO")

        if not recommendations:
            recommendations.append("✅ Audio is well-optimized! No major improvements needed.")

        return recommendations

    # ============================================================================
    # 🔨 BATCH PROCESSING
    # ============================================================================

    async def analyze_directory(
        self,
        directory: Path,
        recursive: bool = True,
        skip_transcription: bool = False
    ) -> Dict[str, Any]:
        """Analyze all audio files in a directory"""
        logger.info(f"🔍 Scanning directory: {directory}")

        # Find all audio files
        audio_files = []
        if recursive:
            for ext in self.supported_formats:
                audio_files.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in self.supported_formats:
                audio_files.extend(directory.glob(f"*{ext}"))

        logger.info(f"🎵 Found {len(audio_files)} audio files")

        # Analyze each file
        results = []
        for i, audio_path in enumerate(audio_files, 1):
            logger.info(f"Analyzing {i}/{len(audio_files)}: {audio_path.name}")

            try:
                analysis = await self.analyze_audio(audio_path)
                results.append(analysis)

                # Rate limiting
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Failed to analyze {audio_path.name}: {e}")
                results.append({
                    'file_path': str(audio_path),
                    'error': str(e)
                })

        # Generate summary
        summary = self._generate_batch_summary(results)

        # Save results
        output_file = directory / f"audio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'summary': summary,
                'results': results
            }, f, indent=2, default=str)

        logger.info(f"💾 Results saved to: {output_file}")

        return {
            'summary': summary,
            'results': results,
            'output_file': str(output_file)
        }

    def _generate_batch_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary statistics"""
        total = len(results)
        successful = len([r for r in results if 'error' not in r])
        failed = total - successful

        # Average scores
        scores = [r.get('quality_score', {}).get('total_score', 0) for r in results if 'quality_score' in r]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Grade distribution
        grades = [r.get('quality_score', {}).get('grade', 'Unknown') for r in results if 'quality_score' in r]
        grade_dist = Counter(grades)

        # Format distribution
        formats = [r.get('technical', {}).get('format', 'Unknown') for r in results if 'technical' in r]
        format_dist = Counter(formats)

        # Total duration
        total_duration = sum([
            r.get('technical', {}).get('duration_seconds', 0)
            for r in results if 'technical' in r
        ])

        # Total file size
        total_size_mb = sum([
            r.get('technical', {}).get('file_size_mb', 0)
            for r in results if 'technical' in r
        ])

        return {
            'total_files': total,
            'successful': successful,
            'failed': failed,
            'average_score': round(avg_score, 1),
            'grade_distribution': dict(grade_dist),
            'format_distribution': dict(format_dist),
            'total_duration_hours': round(total_duration / 3600, 2),
            'total_size_mb': round(total_size_mb, 2),
            'total_size_gb': round(total_size_mb / 1024, 2),
            'needs_optimization': len([r for r in results if r.get('quality_score', {}).get('total_score', 100) < 70])
        }


# ============================================================================
# 🚀 MAIN & CLI
# ============================================================================

async def main():
    """Demo the audio intelligence system"""
    import sys

    analyzer = AudioIntelligence()

    print("\n" + "="*80)
    print("🎵  AUDIO INTELLIGENCE & SEO ANALYZER")
    print("="*80)

    # Check for command line arguments
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])

        if target_path.is_file():
            # Analyze single audio file
            print(f"\n🎵 Analyzing audio file: {target_path.name}")
            result = await analyzer.analyze_audio(target_path)

            # Display results
            print(f"\n✅ Analysis Complete!")
            print(f"\n📊 Quality Score: {result['quality_score']['total_score']}/100")
            print(f"   Grade: {result['quality_score']['grade']}")

            print(f"\n🔧 Technical:")
            tech = result['technical']
            print(f"   Format: {tech.get('format', 'Unknown')}")
            print(f"   Duration: {tech.get('duration_formatted', 'N/A')}")
            print(f"   Bitrate: {tech.get('bitrate_kbps', 0)} kbps")
            print(f"   File Size: {tech.get('file_size_mb', 0)} MB")

            print(f"\n🏷️ Metadata:")
            meta = result['metadata']
            print(f"   Title: {meta.get('title', 'Not set')}")
            print(f"   Artist: {meta.get('artist', 'Not set')}")
            print(f"   Album: {meta.get('album', 'Not set')}")
            print(f"   Genre: {meta.get('genre', 'Not set')}")

            print(f"\n🔍 SEO:")
            seo = result['seo']
            print(f"   Title: {seo['title']}")
            print(f"   Keywords: {', '.join(seo['keywords'][:5])}")
            print(f"   Suggested Filename: {seo['suggested_filename']}")

            print(f"\n💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"   {rec}")

            # Save detailed results
            output_file = target_path.parent / f"{target_path.stem}_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n💾 Detailed results saved to: {output_file}")

        elif target_path.is_dir():
            # Analyze directory
            print(f"\n📁 Analyzing directory: {target_path}")
            recursive = '--recursive' in sys.argv or '-r' in sys.argv

            result = await analyzer.analyze_directory(target_path, recursive=recursive)

            print(f"\n✅ Batch Analysis Complete!")
            print(f"\n📊 Summary:")
            for key, value in result['summary'].items():
                print(f"   {key}: {value}")

            print(f"\n💾 Full results saved to: {result['output_file']}")

    else:
        # Demo mode
        print("\n💡 Usage:")
        print("   python audio_intelligence_seo.py <audio_file>    # Analyze single file")
        print("   python audio_intelligence_seo.py <directory>     # Analyze directory")
        print("   python audio_intelligence_seo.py <directory> -r  # Recursive analysis")
        print("\n📝 Example:")
        print("   python audio_intelligence_seo.py ~/music/song.mp3")
        print("   python audio_intelligence_seo.py ~/music/album -r")


if __name__ == "__main__":
    asyncio.run(main())
