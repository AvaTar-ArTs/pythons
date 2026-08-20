#!/usr/bin/env python3
"""
🎵 PROMPT & CSV ANALYZER ULTIMATE
==================================

1. Reads ALL existing CSVs (especially Suno/Nocturnemelodies)
2. Scans for prompts in HTML, MD, PDFs, TXT
3. Checks Notion exports
4. COMBINES everything into comprehensive CSVs
5. Links songs → URLs → prompts → lyrics

Output CSVs:
- MASTER_SONGS_COMBINED.csv - All songs with all data
- PROMPTS_DISCOVERED.csv - All prompts found
- NOCTURNE_COMPLETE.csv - Complete Nocturnemelodies data
- URLS_CATALOG.csv - All URLs extracted
"""

import os
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import pandas as pd


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
    source: str = ""  # Which CSV it came from
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Prompt:
    """Discovered prompt"""
    prompt_text: str
    prompt_type: str  # sora, music, image, text
    source_file: str
    related_song: str = ""
    related_url: str = ""
    context: str = ""
    quality_score: int = 0


@dataclass
class NotionEntry:
    """Notion database entry"""
    title: str
    content: str
    tags: List[str]
    url: str = ""
    created: str = ""
    source: str = ""


class PromptCSVAnalyzerUltimate:
    """
    Ultimate analyzer that combines everything
    """
    
    def __init__(self):
        self.songs: Dict[str, Song] = {}  # Key: unique ID
        self.prompts: List[Prompt] = []
        self.urls: Set[str] = set()
        self.notion_entries: List[NotionEntry] = []
        
        # Statistics
        self.stats = {
            'csvs_read': 0,
            'songs_found': 0,
            'prompts_found': 0,
            'urls_found': 0,
            'files_scanned': 0
        }
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🎵 PROMPT & CSV ANALYZER ULTIMATE")
        print("="*70)
        print()
        
        # Phase 1: Read existing CSVs
        print("📊 Phase 1: Reading Existing CSVs")
        print("-"*70)
        self._read_all_csvs()
        
        # Phase 2: Scan for prompts
        print("\n🔍 Phase 2: Scanning for Additional Prompts")
        print("-"*70)
        self._scan_for_prompts()
        
        # Phase 3: Check Notion
        print("\n📝 Phase 3: Checking Notion Exports")
        print("-"*70)
        self._check_notion()
        
        # Phase 4: Combine and output
        print("\n💾 Phase 4: Combining Data & Exporting CSVs")
        print("-"*70)
        self._export_all_csvs()
        
        # Phase 5: Generate report
        print("\n📊 Phase 5: Generating Report")
        print("-"*70)
        self._generate_report()
    
    def _read_all_csvs(self):
        """Read all existing CSV files"""
        csv_locations = [
            "/Users/steven/Music/nocTurneMeLoDieS/suno_backups/data/data/",
            "/Users/steven/Music/nocTurneMeLoDieS/",
            "/Users/steven/pythons/",
            "/Users/steven/Documents/",
            "/Users/steven/Downloads/"
        ]
        
        for location in csv_locations:
            if not Path(location).exists():
                continue
            
            for csv_file in Path(location).glob("*.csv"):
                self._read_csv_file(csv_file)
    
    def _read_csv_file(self, filepath: Path):
        """Read a single CSV file"""
        try:
            print(f"   📄 Reading: {filepath.name}")
            
            # Use pandas for robust CSV reading
            df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
            
            self.stats['csvs_read'] += 1
            
            # Detect CSV type and process accordingly
            if self._is_song_csv(df):
                self._process_song_csv(df, filepath.name)
            elif self._is_prompt_csv(df):
                self._process_prompt_csv(df, filepath.name)
            
            # Extract all URLs
            self._extract_urls_from_df(df)
            
        except Exception as e:
            print(f"      ⚠️  Error reading {filepath.name}: {e}")
    
    def _is_song_csv(self, df: pd.DataFrame) -> bool:
        """Check if CSV contains song data"""
        song_indicators = ['title', 'song', 'track', 'audio', 'url', 'prompt']
        columns_lower = [c.lower() for c in df.columns]
        return any(indicator in ' '.join(columns_lower) for indicator in song_indicators)
    
    def _is_prompt_csv(self, df: pd.DataFrame) -> bool:
        """Check if CSV contains prompt data"""
        prompt_indicators = ['prompt', 'instruction', 'system', 'user']
        columns_lower = [c.lower() for c in df.columns]
        return any(indicator in ' '.join(columns_lower) for indicator in prompt_indicators)
    
    def _process_song_csv(self, df: pd.DataFrame, source: str):
        """Process a song CSV"""
        for idx, row in df.iterrows():
            try:
                # Create unique ID
                song_id = self._generate_song_id(row)
                
                # Extract song data
                song = Song(
                    id=song_id,
                    title=self._safe_get(row, ['title', 'song_title', 'name']),
                    artist=self._safe_get(row, ['artist', 'creator', 'user']),
                    url=self._safe_get(row, ['url', 'link', 'song_url']),
                    audio_url=self._safe_get(row, ['audio_url', 'audio', 'mp3_url']),
                    image_url=self._safe_get(row, ['image_url', 'cover_url', 'thumbnail']),
                    video_url=self._safe_get(row, ['video_url', 'video']),
                    prompt=self._safe_get(row, ['prompt', 'gpt_description_prompt', 'description']),
                    lyrics=self._safe_get(row, ['lyrics', 'lyric', 'text']),
                    tags=self._safe_get(row, ['tags', 'style', 'genre']),
                    genre=self._safe_get(row, ['genre', 'style', 'type']),
                    duration=self._safe_get(row, ['duration', 'length']),
                    created_date=self._safe_get(row, ['created_at', 'date', 'created']),
                    play_count=self._safe_get(row, ['play_count', 'plays']),
                    source=source
                )
                
                # Store additional columns
                for col in df.columns:
                    if col not in ['title', 'artist', 'url', 'prompt', 'lyrics']:
                        song.additional_data[col] = str(row[col]) if pd.notna(row[col]) else ""
                
                # Merge with existing data if song already exists
                if song_id in self.songs:
                    self.songs[song_id] = self._merge_songs(self.songs[song_id], song)
                else:
                    self.songs[song_id] = song
                    self.stats['songs_found'] += 1
                
                # Extract prompt if present
                if song.prompt:
                    self.prompts.append(Prompt(
                        prompt_text=song.prompt,
                        prompt_type='music',
                        source_file=source,
                        related_song=song.title,
                        related_url=song.url,
                        quality_score=self._score_prompt(song.prompt)
                    ))
                    self.stats['prompts_found'] += 1
                
            except Exception:
                continue
    
    def _process_prompt_csv(self, df: pd.DataFrame, source: str):
        """Process a prompt CSV"""
        for idx, row in df.iterrows():
            try:
                prompt_text = self._safe_get(row, ['prompt', 'text', 'instruction'])
                if prompt_text:
                    self.prompts.append(Prompt(
                        prompt_text=prompt_text,
                        prompt_type=self._detect_prompt_type(prompt_text),
                        source_file=source,
                        context=self._safe_get(row, ['context', 'description']),
                        quality_score=self._score_prompt(prompt_text)
                    ))
                    self.stats['prompts_found'] += 1
            except:
                continue
    
    def _extract_urls_from_df(self, df: pd.DataFrame):
        """Extract all URLs from a dataframe"""
        for col in df.columns:
            if 'url' in col.lower() or 'link' in col.lower():
                for value in df[col]:
                    if pd.notna(value) and isinstance(value, str):
                        if value.startswith('http'):
                            self.urls.add(value)
                            self.stats['urls_found'] += 1
    
    def _safe_get(self, row, possible_columns: List[str]) -> str:
        """Safely get value from row using multiple possible column names"""
        for col in possible_columns:
            if col in row.index and pd.notna(row[col]):
                return str(row[col])
        return ""
    
    def _generate_song_id(self, row) -> str:
        """Generate unique song ID"""
        # Try to use existing ID field
        for id_field in ['id', 'song_id', 'track_id']:
            if id_field in row.index and pd.notna(row[id_field]):
                return str(row[id_field])
        
        # Generate from title and artist
        title = self._safe_get(row, ['title', 'song_title', 'name'])
        artist = self._safe_get(row, ['artist', 'creator'])
        
        if title:
            return f"{artist}_{title}".replace(' ', '_').replace('/', '_')[:100]
        
        return f"song_{hash(str(row))}"
    
    def _merge_songs(self, existing: Song, new: Song) -> Song:
        """Merge two song entries, keeping most complete data"""
        merged = Song(id=existing.id)
        
        # For each field, use non-empty value
        for field in ['title', 'artist', 'url', 'audio_url', 'image_url', 'video_url',
                      'prompt', 'lyrics', 'tags', 'genre', 'duration', 'created_date', 'play_count']:
            existing_val = getattr(existing, field)
            new_val = getattr(new, field)
            
            # Prefer longer/more complete value
            if len(new_val) > len(existing_val):
                setattr(merged, field, new_val)
            else:
                setattr(merged, field, existing_val)
        
        # Merge sources
        merged.source = f"{existing.source}, {new.source}"
        
        # Merge additional data
        merged.additional_data = {**existing.additional_data, **new.additional_data}
        
        return merged
    
    def _detect_prompt_type(self, prompt_text: str) -> str:
        """Detect prompt type"""
        text_lower = prompt_text.lower()
        
        if any(word in text_lower for word in ['sora', 'video', 'footage']):
            return 'sora'
        elif any(word in text_lower for word in ['song', 'music', 'melody', 'suno']):
            return 'music'
        elif any(word in text_lower for word in ['image', 'picture', 'photo', 'dall-e', 'midjourney']):
            return 'image'
        else:
            return 'text'
    
    def _score_prompt(self, prompt_text: str) -> int:
        """Score prompt quality 1-10"""
        if not prompt_text or len(prompt_text) < 20:
            return 1
        
        score = 5
        
        # Length bonus
        if 100 < len(prompt_text) < 1000:
            score += 2
        elif len(prompt_text) >= 1000:
            score += 3
        
        # Detail indicators
        detail_words = ['detailed', 'specific', 'cinematic', 'professional', 'high quality']
        score += sum(1 for word in detail_words if word in prompt_text.lower())
        
        return min(10, score)
    
    def _scan_for_prompts(self):
        """Scan for additional prompts in files"""
        search_paths = [
            "/Users/steven/pythons",
            "/Users/steven/Music/nocTurneMeLoDieS",
            "/Users/steven/workspace",
            "/Users/steven/Documents"
        ]
        
        extensions = {'.html', '.md', '.txt', '.json'}
        
        for search_path in search_paths:
            if not Path(search_path).exists():
                continue
            
            for root, dirs, files in os.walk(search_path):
                # Skip common ignore dirs
                dirs[:] = [d for d in dirs if d not in {
                    'node_modules', '.git', '__pycache__', 'venv'
                }]
                
                for file in files:
                    if Path(file).suffix in extensions:
                        self.stats['files_scanned'] += 1
                        self._scan_file_for_prompts(Path(root) / file)
    
    def _scan_file_for_prompts(self, filepath: Path):
        """Scan a file for prompts"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Look for prompt patterns
            patterns = [
                r'"prompt":\s*"(.+?)"',
                r'prompt:\s*(.+?)(?:\n|$)',
                r'Prompt:\s*(.+?)(?:\n|$)',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    prompt_text = match.group(1).strip()
                    if len(prompt_text) > 30:  # Meaningful prompts only
                        self.prompts.append(Prompt(
                            prompt_text=prompt_text,
                            prompt_type=self._detect_prompt_type(prompt_text),
                            source_file=str(filepath),
                            quality_score=self._score_prompt(prompt_text)
                        ))
                        self.stats['prompts_found'] += 1
                        print(f"   ✨ Found prompt in: {filepath.name}")
        except:
            pass
    
    def _check_notion(self):
        """Check for Notion exports"""
        notion_paths = [
            "/Users/steven/Documents",
            "/Users/steven/Downloads",
            "/Users/steven"
        ]
        
        for path in notion_paths:
            if not Path(path).exists():
                continue
            
            # Look for Notion exports (CSV or JSON)
            for export_file in Path(path).rglob("*notion*.csv"):
                print(f"   📝 Found Notion CSV: {export_file.name}")
                self._read_csv_file(export_file)
            
            for export_file in Path(path).rglob("*notion*.json"):
                print(f"   📝 Found Notion JSON: {export_file.name}")
                # Would parse JSON here
    
    def _export_all_csvs(self):
        """Export all data to comprehensive CSVs"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Master Songs CSV
        self._export_master_songs_csv(f"MASTER_SONGS_COMBINED_{timestamp}.csv")
        
        # 2. Prompts CSV
        self._export_prompts_csv(f"PROMPTS_DISCOVERED_{timestamp}.csv")
        
        # 3. Nocturnemelodies Complete CSV
        self._export_nocturne_csv(f"NOCTURNE_COMPLETE_{timestamp}.csv")
        
        # 4. URLs Catalog CSV
        self._export_urls_csv(f"URLS_CATALOG_{timestamp}.csv")
    
    def _export_master_songs_csv(self, filename: str):
        """Export master songs CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = [
                'ID', 'Title', 'Artist', 'URL', 'Audio_URL', 'Image_URL', 'Video_URL',
                'Prompt', 'Lyrics', 'Tags', 'Genre', 'Duration', 'Created_Date',
                'Play_Count', 'Source', 'Additional_Columns'
            ]
            writer.writerow(header)
            
            # Write songs
            for song in self.songs.values():
                row = [
                    song.id, song.title, song.artist, song.url, song.audio_url,
                    song.image_url, song.video_url, song.prompt, song.lyrics,
                    song.tags, song.genre, song.duration, song.created_date,
                    song.play_count, song.source,
                    json.dumps(song.additional_data) if song.additional_data else ""
                ]
                writer.writerow(row)
        
        print(f"   ✅ Exported: {filename}")
        print(f"      Songs: {len(self.songs)}")
    
    def _export_prompts_csv(self, filename: str):
        """Export prompts CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                'Prompt_Text', 'Type', 'Source_File', 'Related_Song',
                'Related_URL', 'Quality_Score', 'Context'
            ])
            
            for prompt in sorted(self.prompts, key=lambda p: p.quality_score, reverse=True):
                writer.writerow([
                    prompt.prompt_text, prompt.prompt_type, prompt.source_file,
                    prompt.related_song, prompt.related_url, prompt.quality_score,
                    prompt.context
                ])
        
        print(f"   ✅ Exported: {filename}")
        print(f"      Prompts: {len(self.prompts)}")
    
    def _export_nocturne_csv(self, filename: str):
        """Export Nocturnemelodies-specific CSV"""
        # Filter songs related to Nocturnemelodies
        nocturne_songs = {
            k: v for k, v in self.songs.items()
            if 'nocturne' in v.title.lower() or 
               'nocturne' in v.artist.lower() or
               'nocturnemelodies' in v.source.lower()
        }
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                'Title', 'Prompt', 'Lyrics', 'Audio_URL', 'Image_URL',
                'Tags', 'Genre', 'Duration', 'Created_Date', 'Source'
            ])
            
            for song in nocturne_songs.values():
                writer.writerow([
                    song.title, song.prompt, song.lyrics, song.audio_url,
                    song.image_url, song.tags, song.genre, song.duration,
                    song.created_date, song.source
                ])
        
        print(f"   ✅ Exported: {filename}")
        print(f"      Nocturne songs: {len(nocturne_songs)}")
    
    def _export_urls_csv(self, filename: str):
        """Export all URLs found"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['URL', 'Type', 'Found_In'])
            
            for url in sorted(self.urls):
                url_type = 'unknown'
                if 'audio' in url or '.mp3' in url:
                    url_type = 'audio'
                elif 'image' in url or '.jpg' in url or '.png' in url:
                    url_type = 'image'
                elif 'video' in url or '.mp4' in url:
                    url_type = 'video'
                elif 'suno' in url:
                    url_type = 'suno'
                
                writer.writerow([url, url_type, 'various'])
        
        print(f"   ✅ Exported: {filename}")
        print(f"      URLs: {len(self.urls)}")
    
    def _generate_report(self):
        """Generate final report"""
        print("\n" + "="*70)
        print("📊 FINAL ANALYSIS REPORT")
        print("="*70)
        print()
        print(f"CSVs Read: {self.stats['csvs_read']}")
        print(f"Songs Found (unique): {len(self.songs)}")
        print(f"Prompts Discovered: {len(self.prompts)}")
        print(f"URLs Extracted: {len(self.urls)}")
        print(f"Files Scanned: {self.stats['files_scanned']}")
        print()
        
        # Breakdown by prompt type
        prompt_types = defaultdict(int)
        for prompt in self.prompts:
            prompt_types[prompt.prompt_type] += 1
        
        print("Prompts by Type:")
        for ptype, count in sorted(prompt_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {ptype}: {count}")
        print()
        
        # High quality prompts
        high_quality = [p for p in self.prompts if p.quality_score >= 7]
        print(f"High-Quality Prompts (7+): {len(high_quality)}")
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE!")
        print("="*70)


def main():
    """Run the analyzer"""
    analyzer = PromptCSVAnalyzerUltimate()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()

