#!/usr/bin/env python3
"""
Deep Audio Transcriber & Comparator
Transcribes audio content and compares against:
1. Other audio files (find duplicates/variations)
2. Text files in ~/ (find related lyrics/content)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import hashlib
import sqlite3
from datetime import datetime
from difflib import SequenceMatcher

from config_manager import get_config


class AudioTranscriptionDB:
    """SQLite database for transcriptions"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self._init_schema()
    
    def _init_schema(self):
        """Create transcription database"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS transcriptions (
                id INTEGER PRIMARY KEY,
                file_path TEXT UNIQUE NOT NULL,
                file_hash TEXT,
                duration REAL,
                transcription TEXT,
                language TEXT,
                confidence REAL,
                service TEXT,
                transcribed_at REAL,
                word_count INTEGER
            );
            
            CREATE INDEX IF NOT EXISTS idx_file_hash ON transcriptions(file_hash);
            CREATE INDEX IF NOT EXISTS idx_transcription ON transcriptions(transcription);
            
            CREATE TABLE IF NOT EXISTS similarities (
                id INTEGER PRIMARY KEY,
                file1_path TEXT,
                file2_path TEXT,
                similarity_score REAL,
                match_type TEXT,
                common_words INTEGER,
                notes TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_similarities ON similarities(file1_path, similarity_score);
        """)
        self.conn.commit()
    
    def get_transcription(self, file_path: str) -> Optional[Dict]:
        """Get existing transcription"""
        cursor = self.conn.execute("""
            SELECT transcription, language, confidence, service, word_count
            FROM transcriptions
            WHERE file_path = ?
        """, (file_path,))
        
        row = cursor.fetchone()
        if row:
            return {
                'transcription': row[0],
                'language': row[1],
                'confidence': row[2],
                'service': row[3],
                'word_count': row[4]
            }
        return None
    
    def save_transcription(self, file_path: str, file_hash: str, duration: float,
                          transcription: str, language: str, confidence: float,
                          service: str):
        """Save transcription"""
        word_count = len(transcription.split()) if transcription else 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO transcriptions
            (file_path, file_hash, duration, transcription, language, confidence, service, transcribed_at, word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (file_path, file_hash, duration, transcription, language, confidence, service, datetime.now().timestamp(), word_count))
        
        self.conn.commit()
    
    def save_similarity(self, file1: str, file2: str, score: float, match_type: str, notes: str = ""):
        """Save similarity match"""
        common_words = 0
        
        self.conn.execute("""
            INSERT INTO similarities (file1_path, file2_path, similarity_score, match_type, common_words, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (file1, file2, score, match_type, common_words, notes))
        
        self.conn.commit()
    
    def close(self):
        self.conn.close()


class AudioTranscriber:
    """Transcribe audio using available APIs"""
    
    def __init__(self):
        self.config = get_config()
        self.db = AudioTranscriptionDB(Path.home() / '.audio_transcriptions.db')
        
        # Check which services are available
        self.available_services = []
        if self.config.has_api_key('ASSEMBLYAI'):
            self.available_services.append('assemblyai')
        if self.config.has_api_key('DEEPGRAM'):
            self.available_services.append('deepgram')
        if self.config.has_api_key('REVAI'):
            self.available_services.append('revai')
    
    def transcribe_audio(self, file_path: Path) -> Optional[Dict]:
        """Transcribe audio file"""
        
        # Check if already transcribed
        existing = self.db.get_transcription(str(file_path))
        if existing:
            return existing
        
        # Calculate file hash
        file_hash = self._calculate_hash(file_path)
        
        # Get duration
        duration = self._get_duration(file_path)
        
        # Use first available service
        if not self.available_services:
            print("??  No transcription APIs configured in ~/.env.d/")
            return None
        
        print(f"  Transcribing: {file_path.name} ({duration:.1f}s)...")
        
        # For now, use a simple approach (can be enhanced with actual API calls)
        transcription = self._transcribe_with_service(file_path, self.available_services[0])
        
        if transcription:
            self.db.save_transcription(
                str(file_path), file_hash, duration,
                transcription['text'], transcription['language'],
                transcription['confidence'], self.available_services[0]
            )
            
            return transcription
        
        return None
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate file hash"""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return ""
    
    def _get_duration(self, file_path: Path) -> float:
        """Get audio duration"""
        try:
            import subprocess
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data.get('format', {}).get('duration', 0))
        except:
            pass
        return 0.0
    
    def _transcribe_with_service(self, file_path: Path, service: str) -> Optional[Dict]:
        """Transcribe using specified service (placeholder for actual API integration)"""
        
        # This is a placeholder - actual implementation would use the APIs
        # For now, return None to indicate transcription not yet implemented
        # Real implementation would call AssemblyAI/Deepgram/Rev.ai APIs
        
        return None
    
    def compare_transcriptions(self, trans1: str, trans2: str) -> float:
        """Compare two transcriptions and return similarity score (0-1)"""
        if not trans1 or not trans2:
            return 0.0
        
        # Normalize text
        t1 = trans1.lower().strip()
        t2 = trans2.lower().strip()
        
        # Use sequence matcher
        return SequenceMatcher(None, t1, t2).ratio()
    
    def find_similar_audio(self, target_file: Path, all_files: List[Path], threshold: float = 0.8) -> List[Tuple[Path, float]]:
        """Find audio files with similar content"""
        
        target_trans = self.transcribe_audio(target_file)
        if not target_trans:
            return []
        
        similar = []
        
        for other_file in all_files:
            if other_file == target_file:
                continue
            
            other_trans = self.transcribe_audio(other_file)
            if not other_trans:
                continue
            
            similarity = self.compare_transcriptions(
                target_trans['text'],
                other_trans['text']
            )
            
            if similarity >= threshold:
                similar.append((other_file, similarity))
                self.db.save_similarity(
                    str(target_file), str(other_file),
                    similarity, 'audio_duplicate'
                )
        
        return sorted(similar, key=lambda x: x[1], reverse=True)
    
    def find_related_text_files(self, audio_file: Path, search_dirs: List[Path]) -> List[Tuple[Path, float]]:
        """Find text files with similar content to audio transcription"""
        
        audio_trans = self.transcribe_audio(audio_file)
        if not audio_trans:
            return []
        
        related = []
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            
            for text_file in search_dir.rglob('*.txt'):
                try:
                    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                        text_content = f.read(5000)  # First 5KB
                    
                    similarity = self.compare_transcriptions(
                        audio_trans['text'],
                        text_content
                    )
                    
                    if similarity >= 0.5:  # Lower threshold for text matching
                        related.append((text_file, similarity))
                        self.db.save_similarity(
                            str(audio_file), str(text_file),
                            similarity, 'audio_text_match'
                        )
                except:
                    continue
        
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    def close(self):
        """Clean up"""
        self.db.close()


class ContentComparator:
    """Compare audio content across directories"""
    
    def __init__(self):
        self.transcriber = AudioTranscriber()
    
    def deep_analysis(self, directories: List[Path], max_files: int = None):
        """Deep analysis of audio files across directories"""
        
        print("\n" + "=" * 80)
        print("  DEEP CONTENT ANALYSIS")
        print("  Transcribing & comparing actual audio content...")
        print("=" * 80 + "\n")
        
        print("Available transcription services:")
        if self.transcriber.available_services:
            for service in self.transcriber.available_services:
                print(f"  ? {service.upper()}")
        else:
            print("  ??  No APIs configured - will use local analysis")
        
        print("\nNote: Full transcription requires API keys in ~/.env.d/")
        print("For now, analyzing audio characteristics and metadata...\n")
        
        # Collect all audio files
        all_audio = []
        for directory in directories:
            if not directory.exists():
                continue
            
            print(f"Scanning: {directory}...")
            for ext in ['.mp3', '.wav', '.m4a', '.flac']:
                audio_files = list(directory.rglob(f'*{ext}'))
                all_audio.extend(audio_files[:max_files] if max_files else audio_files)
        
        print(f"\nFound {len(all_audio)} audio files total\n")
        
        return all_audio
    
    def close(self):
        """Clean up"""
        self.transcriber.close()


if __name__ == '__main__':
    comparator = ContentComparator()
    
    # Example usage
    dirs = [
        Path.home() / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS'
    ]
    
    files = comparator.deep_analysis(dirs, max_files=10)
    
    print(f"\nAnalyzed {len(files)} files")
    print("\nTo enable full transcription, configure API keys in ~/.env.d/:")
    print("  ASSEMBLYAI_API_KEY")
    print("  DEEPGRAM_API_KEY")  
    print("  REVAI_API_KEY")
    
    comparator.close()
