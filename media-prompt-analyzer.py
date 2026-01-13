#!/usr/bin/env python3
"""
🎬 COMPLETE MEDIA & PROMPT ANALYZER
====================================

Comprehensive analysis of ALL your content:
✅ ~/Music/nocTurneMeLoDieS - All Suno CSVs, songs, prompts
✅ ~/Pictures - Images with EXIF data, AI generation prompts
✅ ~/Movies - Videos, subtitles, descriptions
✅ ~/pythons - Code, prompts, documentation
✅ All websites - HTML, MD, configs
✅ Notion exports - All data

Outputs:
1. MASTER_SONGS_COMBINED.csv - All songs + URLs + prompts + lyrics
2. PROMPTS_DISCOVERED.csv - All prompts (Sora, music, image, text)
3. IMAGES_CATALOG.csv - All images + metadata + generation prompts
4. VIDEOS_CATALOG.csv - All videos + subtitles + metadata
5. NOCTURNE_COMPLETE.csv - Complete Nocturnemelodies data
6. URLS_MASTER.csv - All URLs extracted
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS


@dataclass
class MediaFile:
    """Media file with metadata"""
    filepath: str
    filename: str
    file_type: str  # image, video, audio
    size_mb: float
    created_date: str
    modified_date: str
    width: int = 0
    height: int = 0
    duration: str = ""
    prompt: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    exif_data: Dict[str, Any] = field(default_factory=dict)
    related_files: List[str] = field(default_factory=list)


@dataclass
class Song:
    """Complete song data"""
    id: str = ""
    title: str = ""
    artist: str = ""
    url: str = ""
    audio_url: str = ""
    image_url: str = ""
    video_url: str = ""
    prompt: str = ""
    lyrics: str = ""
    tags: str = ""
    genre: str = ""
    duration: str = ""
    created_date: str = ""
    play_count: str = ""
    source: str = ""
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Prompt:
    """Discovered prompt"""
    prompt_text: str
    prompt_type: str  # sora, music, image, text, workflow
    source_file: str
    related_media: str = ""
    related_url: str = ""
    context: str = ""
    quality_score: int = 0
    timestamp: str = ""


class CompleteMediaPromptAnalyzer:
    """
    Ultimate analyzer for ALL content
    """
    
    def __init__(self):
        # Data stores
        self.songs: Dict[str, Song] = {}
        self.images: List[MediaFile] = []
        self.videos: List[MediaFile] = []
        self.prompts: List[Prompt] = []
        self.urls: Set[str] = set()
        
        # Stats
        self.stats = {
            'csvs_read': 0,
            'songs_found': 0,
            'images_found': 0,
            'videos_found': 0,
            'prompts_found': 0,
            'urls_found': 0,
            'files_scanned': 0
        }
    
    def run_complete_analysis(self):
        """Run complete analysis"""
        print("🎬 COMPLETE MEDIA & PROMPT ANALYZER")
        print("="*70)
        print()
        
        # Phase 1: Music & Suno CSVs
        print("🎵 Phase 1: Music & Suno CSVs (Nocturnemelodies)")
        print("-"*70)
        self._analyze_music_csvs()
        
        # Phase 2: Pictures
        print("\n🖼️  Phase 2: Pictures Directory")
        print("-"*70)
        self._analyze_pictures()
        
        # Phase 3: Movies
        print("\n🎬 Phase 3: Movies Directory")
        print("-"*70)
        self._analyze_movies()
        
        # Phase 4: Additional Prompts
        print("\n🔍 Phase 4: Scanning for Additional Prompts")
        print("-"*70)
        self._scan_all_prompts()
        
        # Phase 5: Export Everything
        print("\n💾 Phase 5: Exporting Comprehensive CSVs")
        print("-"*70)
        self._export_all_data()
        
        # Phase 6: Generate Report
        print("\n📊 Phase 6: Final Report")
        print("-"*70)
        self._generate_final_report()
    
    # ==================== MUSIC & SUNO ====================
    
    def _analyze_music_csvs(self):
        """Analyze all Suno/music CSVs"""
        music_paths = [
            "/Users/steven/Music/nocTurneMeLoDieS/suno_backups/data/data/",
            "/Users/steven/Music/nocTurneMeLoDieS/",
            "/Users/steven/Music/"
        ]
        
        for path in music_paths:
            if not Path(path).exists():
                continue
            
            for csv_file in Path(path).rglob("*.csv"):
                if csv_file.stat().st_size < 50 * 1024 * 1024:  # Skip files > 50MB
                    self._read_music_csv(csv_file)
    
    def _read_music_csv(self, filepath: Path):
        """Read a music CSV file"""
        try:
            print(f"   📄 Reading: {filepath.name}")
            df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip', low_memory=False)
            
            self.stats['csvs_read'] += 1
            
            # Process each row as potential song
            for idx, row in df.iterrows():
                song = self._extract_song_from_row(row, filepath.name)
                if song and song.title:
                    song_id = song.id or f"{song.artist}_{song.title}".replace(' ', '_')[:100]
                    
                    if song_id in self.songs:
                        self.songs[song_id] = self._merge_songs(self.songs[song_id], song)
                    else:
                        self.songs[song_id] = song
                        self.stats['songs_found'] += 1
                    
                    # Extract prompt
                    if song.prompt:
                        self.prompts.append(Prompt(
                            prompt_text=song.prompt,
                            prompt_type='music',
                            source_file=str(filepath),
                            related_media=song.title,
                            related_url=song.url,
                            quality_score=self._score_prompt(song.prompt),
                            timestamp=song.created_date
                        ))
                        self.stats['prompts_found'] += 1
                
                # Extract URLs
                for col in df.columns:
                    if 'url' in col.lower() and pd.notna(row[col]):
                        url = str(row[col])
                        if url.startswith('http'):
                            self.urls.add(url)
                            self.stats['urls_found'] += 1
                
        except Exception as e:
            print(f"      ⚠️  Error: {e}")
    
    def _extract_song_from_row(self, row, source: str) -> Song:
        """Extract song data from CSV row"""
        song = Song(source=source)
        
        # Map common column names
        column_mappings = {
            'title': ['title', 'song_title', 'name', 'track_name'],
            'artist': ['artist', 'creator', 'user', 'display_name'],
            'url': ['url', 'link', 'song_url', 'page_url'],
            'audio_url': ['audio_url', 'audio', 'mp3_url', 'audio_path'],
            'image_url': ['image_url', 'cover_url', 'thumbnail', 'image_path'],
            'video_url': ['video_url', 'video', 'video_path'],
            'prompt': ['prompt', 'gpt_description_prompt', 'description', 'metadata_prompt'],
            'lyrics': ['lyrics', 'lyric', 'text', 'metadata_text'],
            'tags': ['tags', 'style', 'metadata_tags'],
            'genre': ['genre', 'style', 'type'],
            'duration': ['duration', 'length'],
            'created_date': ['created_at', 'date', 'created', 'timestamp'],
            'play_count': ['play_count', 'plays']
        }
        
        for field, possible_cols in column_mappings.items():
            value = self._safe_get_from_row(row, possible_cols)
            setattr(song, field, value)
        
        # Generate ID
        if 'id' in row.index and pd.notna(row['id']):
            song.id = str(row['id'])
        
        return song
    
    def _safe_get_from_row(self, row, columns: List[str]) -> str:
        """Safely get value from row"""
        for col in columns:
            if col in row.index and pd.notna(row[col]):
                return str(row[col])
        return ""
    
    def _merge_songs(self, existing: Song, new: Song) -> Song:
        """Merge song data, keeping most complete"""
        for field in ['title', 'artist', 'url', 'audio_url', 'image_url', 'video_url',
                      'prompt', 'lyrics', 'tags', 'genre', 'duration', 'created_date']:
            new_val = getattr(new, field)
            if new_val and len(new_val) > len(getattr(existing, field)):
                setattr(existing, field, new_val)
        
        existing.source = f"{existing.source}, {new.source}"
        return existing
    
    # ==================== PICTURES ====================
    
    def _analyze_pictures(self):
        """Analyze Pictures directory"""
        pictures_path = Path("/Users/steven/Pictures")
        
        if not pictures_path.exists():
            print("   ⚠️  Pictures directory not found")
            return
        
        # Scan for images
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
        
        for img_file in pictures_path.rglob("*"):
            if img_file.suffix.lower() in image_extensions:
                self.stats['files_scanned'] += 1
                media = self._analyze_image(img_file)
                if media:
                    self.images.append(media)
                    self.stats['images_found'] += 1
                    
                    if media.prompt:
                        self.prompts.append(Prompt(
                            prompt_text=media.prompt,
                            prompt_type='image',
                            source_file=str(img_file),
                            related_media=media.filename,
                            quality_score=self._score_prompt(media.prompt)
                        ))
                        self.stats['prompts_found'] += 1
                
                # Check for accompanying metadata files
                self._check_metadata_files(img_file)
        
        print(f"   ✅ Found {self.stats['images_found']:,} images")
    
    def _analyze_image(self, filepath: Path) -> MediaFile:
        """Analyze a single image file"""
        try:
            stat = filepath.stat()
            
            media = MediaFile(
                filepath=str(filepath),
                filename=filepath.name,
                file_type='image',
                size_mb=stat.st_size / (1024 * 1024),
                created_date=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                modified_date=datetime.fromtimestamp(stat.st_mtime).isoformat()
            )
            
            # Try to get image dimensions and EXIF
            try:
                with Image.open(filepath) as img:
                    media.width, media.height = img.size
                    
                    # Extract EXIF data
                    exif = img.getexif()
                    if exif:
                        for tag_id, value in exif.items():
                            tag = TAGS.get(tag_id, tag_id)
                            media.exif_data[str(tag)] = str(value)
                            
                            # Look for prompts in EXIF (some AI tools save prompts here)
                            if isinstance(value, str):
                                if any(keyword in str(value).lower() for keyword in ['prompt', 'description', 'dalle', 'midjourney', 'stable diffusion']):
                                    media.prompt = str(value)
                        
                        # Check UserComment (common for AI images)
                        if 'UserComment' in media.exif_data:
                            media.prompt = media.exif_data['UserComment']
            except:
                pass
            
            # Extract prompt from filename if it contains indicators
            if any(keyword in filepath.name.lower() for keyword in ['dalle', 'midjourney', 'leonardo', 'sd', 'stablediffusion']):
                media.description = f"AI-generated image: {filepath.name}"
            
            return media
            
        except Exception:
            return None
    
    def _check_metadata_files(self, image_path: Path):
        """Check for metadata files accompanying an image"""
        # Look for .txt, .json files with same name
        base_name = image_path.stem
        
        for ext in ['.txt', '.json', '.meta']:
            meta_file = image_path.parent / f"{base_name}{ext}"
            if meta_file.exists():
                try:
                    content = meta_file.read_text(encoding='utf-8')
                    
                    # Extract prompts from metadata
                    if 'prompt' in content.lower():
                        # This is likely a prompt file
                        self.prompts.append(Prompt(
                            prompt_text=content[:1000],  # Limit length
                            prompt_type='image',
                            source_file=str(meta_file),
                            related_media=image_path.name,
                            quality_score=self._score_prompt(content)
                        ))
                        self.stats['prompts_found'] += 1
                        print(f"   📝 Found metadata for: {image_path.name}")
                except:
                    pass
    
    # ==================== MOVIES ====================
    
    def _analyze_movies(self):
        """Analyze Movies directory"""
        movies_path = Path("/Users/steven/Movies")
        
        if not movies_path.exists():
            print("   ⚠️  Movies directory not found")
            return
        
        video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.m4v', '.webm'}
        
        for video_file in movies_path.rglob("*"):
            if video_file.suffix.lower() in video_extensions:
                self.stats['files_scanned'] += 1
                media = self._analyze_video(video_file)
                if media:
                    self.videos.append(media)
                    self.stats['videos_found'] += 1
                
                # Check for subtitles and descriptions
                self._check_video_metadata(video_file)
        
        print(f"   ✅ Found {self.stats['videos_found']:,} videos")
    
    def _analyze_video(self, filepath: Path) -> MediaFile:
        """Analyze a video file"""
        try:
            stat = filepath.stat()
            
            media = MediaFile(
                filepath=str(filepath),
                filename=filepath.name,
                file_type='video',
                size_mb=stat.st_size / (1024 * 1024),
                created_date=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                modified_date=datetime.fromtimestamp(stat.st_mtime).isoformat()
            )
            
            # Check if filename contains Sora or AI indicators
            if any(keyword in filepath.name.lower() for keyword in ['sora', 'openai', 'ai-generated', 'runway']):
                media.description = f"AI-generated video: {filepath.name}"
                media.tags.append('AI-generated')
            
            return media
            
        except:
            return None
    
    def _check_video_metadata(self, video_path: Path):
        """Check for video metadata files"""
        base_name = video_path.stem
        
        # Check for subtitle files (.srt, .vtt)
        for ext in ['.srt', '.vtt', '.txt', '.json']:
            meta_file = video_path.parent / f"{base_name}{ext}"
            if meta_file.exists():
                try:
                    content = meta_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Check if contains Sora prompt
                    if 'sora' in content.lower() or 'prompt' in content.lower():
                        self.prompts.append(Prompt(
                            prompt_text=content[:1000],
                            prompt_type='sora',
                            source_file=str(meta_file),
                            related_media=video_path.name,
                            quality_score=self._score_prompt(content)
                        ))
                        self.stats['prompts_found'] += 1
                        print(f"   🎬 Found Sora prompt for: {video_path.name}")
                except:
                    pass
    
    # ==================== PROMPT SCANNING ====================
    
    def _scan_all_prompts(self):
        """Scan all directories for prompts"""
        scan_paths = [
            "/Users/steven/pythons",
            "/Users/steven/workspace",
            "/Users/steven/Documents",
            "/Users/steven/Downloads"
        ]
        
        for path in scan_paths:
            if Path(path).exists():
                self._scan_directory_for_prompts(Path(path))
    
    def _scan_directory_for_prompts(self, directory: Path):
        """Scan directory for prompt files"""
        prompt_extensions = {'.txt', '.md', '.json', '.html'}
        
        for file in directory.rglob("*"):
            if file.suffix.lower() in prompt_extensions:
                if file.stat().st_size < 1024 * 1024:  # < 1MB
                    self._extract_prompts_from_file(file)
    
    def _extract_prompts_from_file(self, filepath: Path):
        """Extract prompts from a file"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            
            # Prompt patterns
            patterns = [
                r'"prompt":\s*"(.+?)"',
                r'prompt:\s*(.+?)(?:\n|$)',
                r'Sora prompt:\s*(.+?)(?:\n|$)',
                r'Image prompt:\s*(.+?)(?:\n|$)',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    prompt_text = match.group(1).strip()
                    if 50 < len(prompt_text) < 2000:
                        self.prompts.append(Prompt(
                            prompt_text=prompt_text,
                            prompt_type=self._detect_prompt_type(prompt_text),
                            source_file=str(filepath),
                            quality_score=self._score_prompt(prompt_text)
                        ))
                        self.stats['prompts_found'] += 1
        except:
            pass
    
    def _detect_prompt_type(self, text: str) -> str:
        """Detect prompt type"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sora', 'video', 'footage', 'openai video']):
            return 'sora'
        elif any(word in text_lower for word in ['song', 'music', 'melody', 'suno']):
            return 'music'
        elif any(word in text_lower for word in ['image', 'picture', 'photo', 'dall-e', 'midjourney', 'leonardo']):
            return 'image'
        elif any(word in text_lower for word in ['workflow', 'automation', 'make.com', 'n8n']):
            return 'workflow'
        else:
            return 'text'
    
    def _score_prompt(self, text: str) -> int:
        """Score prompt quality 1-10"""
        if not text or len(text) < 20:
            return 1
        
        score = 5
        
        if 100 < len(text) < 1000:
            score += 2
        elif len(text) >= 1000:
            score += 3
        
        quality_words = ['detailed', 'cinematic', 'professional', 'high quality', 'specific']
        score += sum(1 for word in quality_words if word in text.lower())
        
        return min(10, score)
    
    # ==================== EXPORT ====================
    
    def _export_all_data(self):
        """Export all data to CSVs"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Master Songs
        self._export_songs_csv(f"MASTER_SONGS_COMBINED_{timestamp}.csv")
        
        # 2. All Prompts
        self._export_prompts_csv(f"PROMPTS_DISCOVERED_{timestamp}.csv")
        
        # 3. Images Catalog
        self._export_images_csv(f"IMAGES_CATALOG_{timestamp}.csv")
        
        # 4. Videos Catalog
        self._export_videos_csv(f"VIDEOS_CATALOG_{timestamp}.csv")
        
        # 5. Nocturne Complete
        self._export_nocturne_csv(f"NOCTURNE_COMPLETE_{timestamp}.csv")
        
        # 6. All URLs
        self._export_urls_csv(f"URLS_MASTER_{timestamp}.csv")
    
    def _export_songs_csv(self, filename: str):
        """Export songs CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Title', 'Artist', 'URL', 'Audio_URL', 'Image_URL', 'Video_URL',
                'Prompt', 'Lyrics', 'Tags', 'Genre', 'Duration', 'Created_Date',
                'Play_Count', 'Source'
            ])
            
            for song in self.songs.values():
                writer.writerow([
                    song.id, song.title, song.artist, song.url, song.audio_url,
                    song.image_url, song.video_url, song.prompt, song.lyrics,
                    song.tags, song.genre, song.duration, song.created_date,
                    song.play_count, song.source
                ])
        
        print(f"   ✅ {filename} - {len(self.songs)} songs")
    
    def _export_prompts_csv(self, filename: str):
        """Export prompts CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Type', 'Prompt_Text', 'Source_File', 'Related_Media',
                'Related_URL', 'Quality_Score', 'Timestamp'
            ])
            
            for prompt in sorted(self.prompts, key=lambda p: p.quality_score, reverse=True):
                writer.writerow([
                    prompt.prompt_type, prompt.prompt_text, prompt.source_file,
                    prompt.related_media, prompt.related_url, prompt.quality_score,
                    prompt.timestamp
                ])
        
        print(f"   ✅ {filename} - {len(self.prompts)} prompts")
    
    def _export_images_csv(self, filename: str):
        """Export images CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Path', 'Size_MB', 'Width', 'Height', 'Created_Date',
                'Prompt', 'Description', 'Tags', 'EXIF_Data'
            ])
            
            for img in self.images:
                writer.writerow([
                    img.filename, img.filepath, f"{img.size_mb:.2f}",
                    img.width, img.height, img.created_date,
                    img.prompt, img.description, ','.join(img.tags),
                    json.dumps(img.exif_data) if img.exif_data else ""
                ])
        
        print(f"   ✅ {filename} - {len(self.images)} images")
    
    def _export_videos_csv(self, filename: str):
        """Export videos CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Path', 'Size_MB', 'Created_Date',
                'Description', 'Tags', 'Related_Files'
            ])
            
            for video in self.videos:
                writer.writerow([
                    video.filename, video.filepath, f"{video.size_mb:.2f}",
                    video.created_date, video.description, ','.join(video.tags),
                    ','.join(video.related_files)
                ])
        
        print(f"   ✅ {filename} - {len(self.videos)} videos")
    
    def _export_nocturne_csv(self, filename: str):
        """Export Nocturnemelodies CSV"""
        nocturne_songs = {k: v for k, v in self.songs.items()
                          if 'nocturne' in v.title.lower() or 
                          'nocturne' in v.artist.lower() or
                          'nocturne' in v.source.lower()}
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Title', 'Prompt', 'Lyrics', 'Audio_URL', 'Image_URL',
                'Tags', 'Genre', 'Duration', 'Created_Date'
            ])
            
            for song in nocturne_songs.values():
                writer.writerow([
                    song.title, song.prompt, song.lyrics, song.audio_url,
                    song.image_url, song.tags, song.genre, song.duration,
                    song.created_date
                ])
        
        print(f"   ✅ {filename} - {len(nocturne_songs)} Nocturne songs")
    
    def _export_urls_csv(self, filename: str):
        """Export URLs CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Type'])
            
            for url in sorted(self.urls):
                url_type = 'other'
                if 'audio' in url or '.mp3' in url:
                    url_type = 'audio'
                elif 'image' in url or any(ext in url for ext in ['.jpg', '.png', '.webp']):
                    url_type = 'image'
                elif 'video' in url or '.mp4' in url:
                    url_type = 'video'
                elif 'suno' in url:
                    url_type = 'suno'
                
                writer.writerow([url, url_type])
        
        print(f"   ✅ {filename} - {len(self.urls)} URLs")
    
    # ==================== REPORT ====================
    
    def _generate_final_report(self):
        """Generate final report"""
        print("\n" + "="*70)
        print("📊 COMPLETE ANALYSIS REPORT")
        print("="*70)
        print()
        print(f"🎵 Songs: {len(self.songs):,}")
        print(f"🖼️  Images: {len(self.images):,}")
        print(f"🎬 Videos: {len(self.videos):,}")
        print(f"✨ Prompts: {len(self.prompts):,}")
        print(f"🔗 URLs: {len(self.urls):,}")
        print(f"📄 CSVs Read: {self.stats['csvs_read']}")
        print(f"📁 Files Scanned: {self.stats['files_scanned']:,}")
        print()
        
        # Prompt breakdown
        prompt_types = defaultdict(int)
        for p in self.prompts:
            prompt_types[p.prompt_type] += 1
        
        print("Prompts by Type:")
        for ptype, count in sorted(prompt_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {ptype.capitalize()}: {count}")
        
        high_quality = [p for p in self.prompts if p.quality_score >= 7]
        print(f"\nHigh-Quality Prompts (7+/10): {len(high_quality)}")
        
        print("\n" + "="*70)
        print("✅ COMPLETE ANALYSIS FINISHED!")
        print("="*70)


def main():
    """Run the complete analyzer"""
    analyzer = CompleteMediaPromptAnalyzer()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()

