#!/usr/bin/env python3
"""
NocturneMemory - AI Content Cache for AvatarArts

Intelligent indexing and search system for:
- Image/Sora prompts (AI generation prompts)
- Lyrics and transcripts (song lyrics, audio transcripts)
- Analysis (music/metadata analysis)
- Originals (source files: PDF, JSON, MD, CSV, etc.)

Inspired by AutoTagger patterns with specialized semantic categories for creative content.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


class NocturneMemory:
    """Intelligent cache for AvatarArts creative content"""

    # Specialized semantic categories for creative content
    CREATIVE_CATEGORIES = {
        "AI_Image_Prompts": {
            "keywords": {
                "portrait": 8,
                "landscape": 8,
                "digital art": 9,
                "concept art": 9,
                "photorealistic": 10,
                "anime": 8,
                "cyberpunk": 9,
                "fantasy": 9,
                "oil painting": 8,
                "watercolor": 8,
                "3d render": 9,
                "studio ghibli": 10,
            },
            "patterns": [
                r"^(?:a |an )?\w+ (?:portrait|landscape|still life)",
                r"digital art.*(?:by|in the style of)",
                r"photorealistic.*(?:render|image)",
                r"(?:anime|manga) style",
                r"cyberpunk.*(?:city|character)",
                r"fantasy.*(?:world|creature|character)",
            ],
            "file_extensions": [".txt", ".md", ".json"],
            "content_indicators": ["prompt", "generate", "create", "render"],
        },
        "Sora_Video_Prompts": {
            "keywords": {
                "cinematic": 10,
                "slow motion": 9,
                "time lapse": 9,
                "dolly zoom": 10,
                "establishing shot": 9,
                "montage": 8,
                "transition": 7,
                "fade": 7,
                "dramatic lighting": 8,
                "golden hour": 9,
                "blue hour": 9,
            },
            "patterns": [
                r"(?:cinematic|movie|film) scene",
                r"slow motion.*(?:falling|running|dancing)",
                r"time lapse.*(?:clouds|city|ocean)",
                r"montage of.*(?:memories|seasons|emotions)",
                r"dramatic.*(?:reveal|entrance|exit)",
            ],
            "file_extensions": [".txt", ".md", ".json"],
            "content_indicators": ["sora", "video", "cinematic", "scene", "montage"],
        },
        "Song_Lyrics": {
            "keywords": {
                "verse": 10,
                "chorus": 10,
                "bridge": 9,
                "hook": 8,
                "melody": 7,
                "rhythm": 7,
                "harmony": 7,
                "lyric": 10,
                "vocal": 8,
            },
            "patterns": [
                r"^\[Verse.*\]",
                r"^\[Chorus.*\]",
                r"^\[Bridge.*\]",
                r"(?:I|we|you|they) (?:sing|dance|cry|love|hate)",
                r"(?:heart|love|soul|dream) (?:breaks|flies|soars|dies)",
            ],
            "file_extensions": [".txt", ".md", ".json"],
            "content_indicators": ["lyrics", "verse", "chorus", "melody"],
        },
        "Audio_Transcripts": {
            "keywords": {
                "transcript": 10,
                "transcription": 9,
                "spoken": 7,
                "recorded": 7,
                "microphone": 6,
                "interview": 8,
                "podcast": 8,
                "narration": 8,
            },
            "patterns": [
                r"^\d{2}:\d{2}",  # Timestamp format
                r"Speaker.*:",
                r"\[.*\]",  # Bracketed annotations
                r"music plays|sound effect|background noise",
            ],
            "file_extensions": [".txt", ".md", ".json", ".srt"],
            "content_indicators": ["transcript", "recording", "interview", "spoken"],
        },
        "Music_Analysis": {
            "keywords": {
                "analysis": 10,
                "tempo": 8,
                "key": 8,
                "genre": 8,
                "mood": 9,
                "emotion": 7,
                "theme": 9,
                "motif": 7,
                "structure": 8,
                "composition": 9,
            },
            "patterns": [
                r"tempo.*(?:bpm|BPM)",
                r"key.*(?:major|minor|C|D|E|F|G|A|B)",
                r"genre.*(?:rock|pop|jazz|classical|electronic)",
                r"mood.*(?:happy|sad|energetic|calm)",
                r"theme.*(?:love|loss|hope|despair)",
            ],
            "file_extensions": [".txt", ".md", ".json", ".html"],
            "content_indicators": ["analysis", "tempo", "key", "genre", "mood"],
        },
        "Source_Originals": {
            "keywords": {
                "original": 8,
                "source": 8,
                "master": 7,
                "draft": 6,
                "version": 5,
                "backup": 5,
                "archive": 5,
            },
            "patterns": [
                r"original.*(?:file|document|recording)",
                r"source.*(?:material|code|content)",
                r"(?:v|version)[\d\.]+",
                r"(?:draft|final|master)[\s\d]*",
            ],
            "file_extensions": [
                ".pdf",
                ".docx",
                ".xlsx",
                ".psd",
                ".aif",
                ".wav",
                ".flac",
            ],
            "content_indicators": ["original", "source", "master", "draft"],
        },
    }

    def __init__(self, cache_dir=None):
        self.cache_dir = Path(cache_dir or "~/nocTurneMeLoDieS/.memory").expanduser()
        self.db_path = self.cache_dir / "nocturnememory.db"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database with specialized tables for creative content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main content index
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_index (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                category TEXT,
                confidence REAL,
                size_bytes INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                checksum TEXT,
                content_preview TEXT,
                metadata TEXT
            )
        """
        )

        # Specialized tables for different content types
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_prompts (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                prompt_type TEXT,  -- 'image' or 'sora'
                style TEXT,
                subject TEXT,
                mood TEXT,
                technical_details TEXT,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS song_content (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                content_type TEXT,  -- 'lyrics' or 'transcript'
                title TEXT,
                artist TEXT,
                key TEXT,
                tempo INTEGER,
                genre TEXT,
                mood TEXT,
                themes TEXT,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_content (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                analysis_type TEXT,
                subject_title TEXT,
                key_findings TEXT,
                recommendations TEXT,
                confidence_score REAL,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS source_files (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                file_type TEXT,
                format TEXT,
                quality TEXT,
                usage TEXT,
                version TEXT,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        # Search index for fast lookups
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_index (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                search_term TEXT,
                category TEXT,
                weight REAL,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def scan_directory(self, target_dir: str, recursive: bool = True):
        """Scan directory for creative content matching our categories"""
        target_path = Path(target_dir).expanduser().resolve()

        if not target_path.exists():
            print(f"Directory {target_path} does not exist")
            return

        print(f"🔍 Scanning {target_path} for creative content...")

        indexed = 0
        for root, dirs, files in os.walk(target_path):
            if not recursive and root != str(target_path):
                continue

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # Check if this file type is relevant to our categories
                relevant_categories = []
                for cat_name, cat_config in self.CREATIVE_CATEGORIES.items():
                    if ext in cat_config.get("file_extensions", []):
                        relevant_categories.append((cat_name, cat_config))
                        break  # Only check primary category match for now

                if relevant_categories:
                    if self.index_file(file_path, relevant_categories):
                        indexed += 1

        print(f"✅ Indexed {indexed} creative content files")

    def index_file(self, file_path: Path, categories: list[tuple]) -> bool:
        """Index a single file into the database"""
        try:
            stat = file_path.stat()
            file_size = stat.st_size

            # Skip files that are too large (>10MB)
            if file_size > 10 * 1024 * 1024:
                return False

            # Calculate checksum
            checksum = self.calculate_checksum(file_path)

            # Read content for analysis
            content = ""
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(min(50000, file_size))  # Read up to 50KB
            except OSError:
                return False

            # Analyze content against categories
            best_category = None
            best_confidence = 0
            category_metadata = {}

            for cat_name, cat_config in categories:
                confidence, metadata = self.analyze_content(content, cat_config)
                if confidence > best_confidence:
                    best_category = cat_name
                    best_confidence = confidence
                    category_metadata = metadata

            if best_confidence < 0.3:  # Minimum confidence threshold
                return False

            # Store in database
            return self.store_content(
                file_path=file_path,
                category=best_category,
                confidence=best_confidence,
                size_bytes=file_size,
                checksum=checksum,
                content_preview=content[:1000],
                metadata=category_metadata,
            )

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return False

    def analyze_content(self, content: str, category_config: dict) -> tuple[float, dict]:
        """Analyze content against category patterns and keywords"""
        confidence = 0
        metadata = {}

        # Keyword matching
        keywords = category_config.get("keywords", {})
        content_lower = content.lower()

        for keyword, weight in keywords.items():
            if keyword.lower() in content_lower:
                confidence += weight / 10.0  # Normalize to 0-1 scale

        # Pattern matching
        patterns = category_config.get("patterns", [])
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                confidence += 0.2

        # Content indicators
        indicators = category_config.get("content_indicators", [])
        for indicator in indicators:
            if indicator.lower() in content_lower:
                confidence += 0.15

        # Extract metadata based on category
        if "AI_Image_Prompts" in str(category_config):
            metadata = self.extract_image_prompt_metadata(content)
        elif "Sora_Video_Prompts" in str(category_config):
            metadata = self.extract_sora_prompt_metadata(content)
        elif "Song_Lyrics" in str(category_config):
            metadata = self.extract_lyrics_metadata(content)
        elif "Audio_Transcripts" in str(category_config):
            metadata = self.extract_transcript_metadata(content)
        elif "Music_Analysis" in str(category_config):
            metadata = self.extract_analysis_metadata(content)

        return min(confidence, 1.0), metadata

    def extract_image_prompt_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from AI image prompts"""
        metadata = {}

        # Extract style information
        style_patterns = [
            r"(?:in the style of|style of) ([^,\.\n]+)",
            r"digital art(?: by ([^,\.\n]+))?",
            r"(?:oil painting|watercolor|sketch|painting) (?:by ([^,\.\n]+))?",
        ]

        for pattern in style_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and match.group(1):
                metadata["style"] = match.group(1).strip()
                break

        # Extract subject
        subject_match = re.search(r"^(?:a |an )?([^-,\.\n]+?)(?:\s*[-,]|$)", content.strip(), re.IGNORECASE)
        if subject_match:
            metadata["subject"] = subject_match.group(1).strip()

        return metadata

    def extract_sora_prompt_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from Sora video prompts"""
        metadata = {}

        # Look for cinematic techniques
        techniques = []
        if "slow motion" in content.lower():
            techniques.append("slow_motion")
        if "time lapse" in content.lower():
            techniques.append("time_lapse")
        if "montage" in content.lower():
            techniques.append("montage")
        if "cinematic" in content.lower():
            techniques.append("cinematic")

        if techniques:
            metadata["techniques"] = techniques

        return metadata

    def extract_lyrics_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from song lyrics"""
        metadata = {}

        # Count verses and choruses
        verses = len(re.findall(r"^\[Verse", content, re.MULTILINE | re.IGNORECASE))
        choruses = len(re.findall(r"^\[Chorus", content, re.MULTILINE | re.IGNORECASE))
        bridges = len(re.findall(r"^\[Bridge", content, re.MULTILINE | re.IGNORECASE))

        if verses:
            metadata["verses"] = verses
        if choruses:
            metadata["choruses"] = choruses
        if bridges:
            metadata["bridges"] = bridges

        # Extract themes (simple keyword detection)
        theme_keywords = [
            "love",
            "heart",
            "dream",
            "soul",
            "pain",
            "hope",
            "dark",
            "light",
        ]
        themes = []
        content_lower = content.lower()
        for theme in theme_keywords:
            if theme in content_lower:
                themes.append(theme)

        if themes:
            metadata["themes"] = themes

        return metadata

    def extract_transcript_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from audio transcripts"""
        metadata = {}

        # Count timestamps
        timestamps = len(re.findall(r"\d{1,2}:\d{2}", content))
        if timestamps:
            metadata["segments"] = timestamps

        # Check for speakers
        speakers = re.findall(r"(?:Speaker|Host|Guest)\s*\d*:", content, re.IGNORECASE)
        if speakers:
            metadata["speakers"] = len(set(speakers))

        return metadata

    def extract_analysis_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from music analysis"""
        metadata = {}

        # Extract tempo
        tempo_match = re.search(r"tempo.*(\d+).*bpm", content, re.IGNORECASE)
        if tempo_match:
            metadata["tempo"] = int(tempo_match.group(1))

        # Extract key
        key_match = re.search(r"key.*([A-G][#b]?)\s*(major|minor)", content, re.IGNORECASE)
        if key_match:
            metadata["key"] = f"{key_match.group(1)} {key_match.group(2)}"

        # Extract genre
        genre_match = re.search(r"genre.*([a-zA-Z\s]+)", content, re.IGNORECASE)
        if genre_match:
            metadata["genre"] = genre_match.group(1).strip()

        return metadata

    def store_content(
        self,
        file_path: Path,
        category: str,
        confidence: float,
        size_bytes: int,
        checksum: str,
        content_preview: str,
        metadata: dict,
    ) -> bool:
        """Store content in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            content_id = str(hashlib.md5(str(file_path).encode()).hexdigest())[:16]

            # Insert main content index
            cursor.execute(
                """
                INSERT OR REPLACE INTO content_index
                (id, file_path, file_name, category, confidence, size_bytes,
                 created_at, modified_at, checksum, content_preview, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    content_id,
                    str(file_path),
                    file_path.name,
                    category,
                    confidence,
                    size_bytes,
                    datetime.fromtimestamp(file_path.stat().st_ctime),
                    datetime.fromtimestamp(file_path.stat().st_mtime),
                    checksum,
                    content_preview,
                    json.dumps(metadata),
                ),
            )

            # Store category-specific data
            if category == "AI_Image_Prompts":
                self.store_ai_prompt(content_id, metadata, "image")
            elif category == "Sora_Video_Prompts":
                self.store_ai_prompt(content_id, metadata, "sora")
            elif category in ["Song_Lyrics", "Audio_Transcripts"]:
                self.store_song_content(content_id, category, metadata)
            elif category == "Music_Analysis":
                self.store_analysis_content(content_id, metadata)
            elif category == "Source_Originals":
                self.store_source_file(content_id, metadata)

            # Build search index
            self.build_search_index(content_id, category, content_preview, metadata)

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error storing content: {e}")
            return False

    def store_ai_prompt(self, content_id: str, metadata: dict, prompt_type: str):
        """Store AI prompt data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO ai_prompts
            (id, content_index_id, prompt_type, style, subject, mood, technical_details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content_id,
                prompt_type,
                metadata.get("style"),
                metadata.get("subject"),
                metadata.get("mood"),
                json.dumps(metadata.get("techniques", [])),
            ),
        )

        conn.commit()
        conn.close()

    def store_song_content(self, content_id: str, content_type: str, metadata: dict):
        """Store song content data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO song_content
            (id, content_index_id, content_type, title, artist, key, tempo, genre, mood, themes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content_id,
                content_type.lower(),
                metadata.get("title"),
                metadata.get("artist"),
                metadata.get("key"),
                metadata.get("tempo"),
                metadata.get("genre"),
                metadata.get("mood"),
                json.dumps(metadata.get("themes", [])),
            ),
        )

        conn.commit()
        conn.close()

    def store_analysis_content(self, content_id: str, metadata: dict):
        """Store analysis content data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO analysis_content
            (id, content_index_id, analysis_type, subject_title, key_findings, recommendations, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content_id,
                "music_analysis",
                metadata.get("subject_title"),
                json.dumps(metadata.get("key_findings", [])),
                json.dumps(metadata.get("recommendations", [])),
                metadata.get("confidence_score", 0.8),
            ),
        )

        conn.commit()
        conn.close()

    def store_source_file(self, content_id: str, metadata: dict):
        """Store source file data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO source_files
            (id, content_index_id, file_type, format, quality, usage, version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content_id,
                metadata.get("file_type"),
                metadata.get("format"),
                metadata.get("quality"),
                metadata.get("usage"),
                metadata.get("version"),
            ),
        )

        conn.commit()
        conn.close()

    def build_search_index(self, content_id: str, category: str, content_preview: str, metadata: dict):
        """Build search index for fast lookups"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Extract searchable terms
        search_terms = set()

        # From content preview (first 500 chars)
        words = re.findall(r"\b\w{3,}\b", content_preview[:500].lower())
        search_terms.update(words[:20])  # Limit to avoid spam

        # From metadata
        for key, value in metadata.items():
            if isinstance(value, str):
                words = re.findall(r"\b\w{3,}\b", value.lower())
                search_terms.update(words[:5])
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        words = re.findall(r"\b\w{3,}\b", item.lower())
                        search_terms.update(words[:3])

        # Insert search terms
        for term in search_terms:
            term_id = f"{content_id}_{term}"
            cursor.execute(
                """
                INSERT OR REPLACE INTO search_index
                (id, content_index_id, search_term, category, weight)
                VALUES (?, ?, ?, ?, ?)
            """,
                (term_id, content_id, term, category, 1.0),
            )

        conn.commit()
        conn.close()

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def search(self, query: str, category: str | None = None, limit: int = 20) -> list[dict]:
        """Search the content index"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build search query
        query_terms = re.findall(r"\b\w{3,}\b", query.lower())
        if not query_terms:
            return []

        # Search for files containing any of the query terms
        placeholders = ",".join("?" * len(query_terms))
        category_filter = "AND ci.category = ?" if category else ""

        cursor.execute(
            f"""
            SELECT DISTINCT ci.id, ci.file_path, ci.file_name, ci.category,
                   ci.confidence, si.search_term, ci.content_preview
            FROM content_index ci
            JOIN search_index si ON ci.id = si.content_index_id
            WHERE si.search_term IN ({placeholders}) {category_filter}
            ORDER BY ci.confidence DESC
            LIMIT ?
        """,
            query_terms + ([category] if category else []) + [limit],
        )

        results = []
        seen = set()
        for row in cursor.fetchall():
            content_id = row[0]
            if content_id in seen:
                continue
            seen.add(content_id)

            results.append(
                {
                    "id": row[0],
                    "file_path": row[1],
                    "file_name": row[2],
                    "category": row[3],
                    "confidence": row[4],
                    "matched_term": row[5],
                    "preview": row[6][:200],
                }
            )

        conn.close()
        return results

    def get_stats(self) -> dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Content by category
        cursor.execute("SELECT category, COUNT(*) FROM content_index GROUP BY category")
        stats["by_category"] = dict(cursor.fetchall())

        # Total content
        cursor.execute("SELECT COUNT(*) FROM content_index")
        stats["total_content"] = cursor.fetchone()[0]

        # Search terms
        cursor.execute("SELECT COUNT(*) FROM search_index")
        stats["search_terms"] = cursor.fetchone()[0]

        conn.close()
        return stats


def main():
    parser = argparse.ArgumentParser(description="NocturneMemory - Creative Content Cache")
    parser.add_argument("command", choices=["scan", "search", "stats"], help="Command to run")
    parser.add_argument("--path", help="Path to scan (for scan command)")
    parser.add_argument("--query", help="Search query (for search command)")
    parser.add_argument("--category", help="Filter by category (for search command)")
    parser.add_argument("--recursive", action="store_true", default=True, help="Scan recursively")

    args = parser.parse_args()

    memory = NocturneMemory()

    if args.command == "scan":
        if not args.path:
            print("Error: --path required for scan command")
            sys.exit(1)
        memory.scan_directory(args.path, args.recursive)

    elif args.command == "search":
        if not args.query:
            print("Error: --query required for search command")
            sys.exit(1)

        results = memory.search(args.query, args.category)
        print(f"Found {len(results)} results for '{args.query}'")
        if args.category:
            print(f"Filtered by category: {args.category}")
        print()

        for result in results:
            print(f"📄 {result['file_name']}")
            print(f"   Category: {result['category']} (confidence: {result['confidence']:.2f})")
            print(f"   Path: {result['file_path']}")
            print(f"   Preview: {result['preview']}...")
            print()

    elif args.command == "stats":
        stats = memory.get_stats()
        print("NocturneMemory Statistics")
        print("=" * 30)
        print(f"Total content indexed: {stats['total_content']}")
        print(f"Search terms indexed: {stats['search_terms']}")
        print()
        print("Content by category:")
        for category, count in stats["by_category"].items():
            print(f"  {category}: {count}")
        print()
        print(f"Database: {memory.db_path}")


if __name__ == "__main__":
    main()
