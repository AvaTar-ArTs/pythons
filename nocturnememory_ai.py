#!/usr/bin/env python3
"""
NocturneMemory AI - Enhanced Creative Content Cache with AI Analysis

Integrates with available APIs:
- OpenAI (GPT models for content analysis)
- Anthropic (Claude for creative analysis)
- Gemini (Google AI for multimodal analysis)
- Grok (xAI for creative insights)
- Together AI (for specialized models)

Enhanced analysis capabilities for:
- Deeper content understanding
- Creative prompt optimization
- Music analysis with AI insights
- Automatic content tagging and categorization
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

import requests
from dotenv import load_dotenv


class NocturneMemoryAI:
    """AI-enhanced creative content cache"""

    def __init__(self, cache_dir=None):
        self.cache_dir = Path(cache_dir or "~/nocTurneMeLoDieS/.memory").expanduser()
        self.db_path = self.cache_dir / "nocturnememory_ai.db"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load environment variables
        self.load_api_keys()

        # Initialize database
        self.init_database()

    def load_api_keys(self):
        """Load API keys from ~/.env.d/"""
        env_dir = Path.home() / ".env.d"

        # Load master consolidated if available
        master_env = env_dir / "MASTER_CONSOLIDATED.env"
        if master_env.exists():
            load_dotenv(master_env)
        else:
            # Load individual API files
            api_files = ["llm-apis.env", "gemini.env", "anthropic.env", "openai.env"]
            for api_file in api_files:
                env_file = env_dir / api_file
                if env_file.exists():
                    load_dotenv(env_file)

        # Set API keys
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY"),
            "grok": os.getenv("GROK_API_KEY"),
            "together": os.getenv("TOGETHER_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
        }

        # Test which APIs are available
        self.available_apis = {}
        for name, key in self.api_keys.items():
            if key:
                self.available_apis[name] = self.test_api(name, key)

    def test_api(self, name: str, key: str) -> bool:
        """Test if API key is working"""
        try:
            if name == "openai":
                # Simple OpenAI test
                response = requests.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {key}"},
                    timeout=5,
                )
                return response.status_code == 200

            elif name == "anthropic":
                # Simple Anthropic test
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
                    json={"messages": [], "max_tokens": 1},
                    timeout=5,
                )
                return response.status_code in [
                    200,
                    400,
                ]  # 400 is expected for empty messages

            elif name == "gemini":
                # Simple Gemini test
                response = requests.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={key}",
                    timeout=5,
                )
                return response.status_code == 200

            return True  # Assume other APIs work if key exists

        except Exception:
            return False

    def init_database(self):
        """Initialize the enhanced database with AI analysis tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Enhanced content index
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_index (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                category TEXT,
                confidence REAL,
                ai_confidence REAL,
                size_bytes INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                checksum TEXT,
                content_preview TEXT,
                metadata TEXT,
                ai_analysis TEXT
            )
        """
        )

        # AI analysis results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                api_used TEXT,
                analysis_type TEXT,
                analysis_result TEXT,
                confidence_score REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        # Creative insights
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS creative_insights (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                insight_type TEXT,
                insight_data TEXT,
                api_source TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        # Enhanced search index
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_index (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                search_term TEXT,
                category TEXT,
                weight REAL,
                ai_generated BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def analyze_with_ai(self, content: str, content_type: str, api_preference: str = None) -> dict[str, Any]:
        """Use AI to analyze content for deeper insights"""

        if not self.available_apis:
            return {"error": "No AI APIs available"}

        # Choose API (use preference or best available)
        api_to_use = api_preference or self.select_best_api(content_type)

        if not api_to_use or api_to_use not in self.available_apis:
            return {"error": f"Preferred API {api_to_use} not available"}

        try:
            if api_to_use == "openai":
                return self.analyze_with_openai(content, content_type)
            elif api_to_use == "anthropic":
                return self.analyze_with_anthropic(content, content_type)
            elif api_to_use == "gemini":
                return self.analyze_with_gemini(content, content_type)
            elif api_to_use == "grok":
                return self.analyze_with_grok(content, content_type)
            else:
                return {"error": f"Unsupported API: {api_to_use}"}

        except Exception as e:
            return {"error": f"AI analysis failed: {str(e)}"}

    def select_best_api(self, content_type: str) -> str:
        """Select the best API for a given content type"""
        api_priority = {
            "AI_Image_Prompts": ["gemini", "openai", "anthropic"],
            "Sora_Video_Prompts": ["openai", "anthropic", "gemini"],
            "Song_Lyrics": ["anthropic", "openai", "grok"],  # Creative analysis
            "Audio_Transcripts": ["openai", "anthropic", "gemini"],
            "Music_Analysis": ["openai", "anthropic", "grok"],
            "Source_Originals": ["gemini", "openai", "anthropic"],
        }

        preferred_apis = api_priority.get(content_type, ["openai", "anthropic", "gemini"])

        for api in preferred_apis:
            if api in self.available_apis:
                return api

        return list(self.available_apis.keys())[0] if self.available_apis else None

    def analyze_with_openai(self, content: str, content_type: str) -> dict[str, Any]:
        """Analyze content using OpenAI GPT"""
        api_key = self.api_keys["openai"]

        prompt_map = {
            "AI_Image_Prompts": "Analyze this AI image prompt. Extract: style, subject, mood, technical details, and suggest improvements.",
            "Sora_Video_Prompts": "Analyze this video generation prompt. Extract: visual style, narrative elements, techniques, and pacing suggestions.",
            "Song_Lyrics": "Analyze these song lyrics. Extract: themes, emotional tone, structure, and artistic merit.",
            "Audio_Transcripts": "Analyze this transcript. Extract: key topics, sentiment, speakers, and content summary.",
            "Music_Analysis": "Analyze this music analysis. Extract: insights, recommendations, and additional observations.",
            "Source_Originals": "Analyze this creative source file. Extract: content type, quality indicators, and usage suggestions.",
        }

        system_prompt = prompt_map.get(content_type, "Analyze this creative content and provide insights.")
        user_prompt = f"Content to analyze:\n\n{content[:2000]}"  # Limit content length

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",  # Use efficient model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 500,
                "temperature": 0.3,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            return {
                "api": "openai",
                "analysis": analysis,
                "confidence": 0.85,
                "model": "gpt-4o-mini",
            }
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")

    def analyze_with_anthropic(self, content: str, content_type: str) -> dict[str, Any]:
        """Analyze content using Anthropic Claude"""
        api_key = self.api_keys["anthropic"]

        prompt_map = {
            "AI_Image_Prompts": "You are a creative AI prompt engineer. Analyze this image prompt for artistic merit, clarity, and potential for generating compelling visuals.",
            "Song_Lyrics": "You are a music critic and songwriter. Analyze these lyrics for poetic quality, emotional depth, and musical potential.",
            "Sora_Video_Prompts": "You are a cinematographer. Analyze this video prompt for visual storytelling potential and technical feasibility.",
        }

        system_prompt = prompt_map.get(
            content_type,
            "You are a creative content analyst. Provide thoughtful analysis of this content.",
        )
        user_prompt = f"Content to analyze:\n\n{content[:2000]}"

        # Anthropic API requires messages array without system in the root
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-3-haiku-20240307",  # Efficient model
                "max_tokens": 500,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
                "temperature": 0.3,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            analysis = result["content"][0]["text"]
            return {
                "api": "anthropic",
                "analysis": analysis,
                "confidence": 0.9,
                "model": "claude-3-haiku",
            }
        else:
            # Fallback to simpler request for testing
            try:
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 100,
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Analyze this {content_type}: {content[:500]}",
                            }
                        ],
                        "temperature": 0.3,
                    },
                    timeout=30,
                )

                if response.status_code == 200:
                    result = response.json()
                    analysis = result["content"][0]["text"]
                    return {
                        "api": "anthropic",
                        "analysis": analysis,
                        "confidence": 0.9,
                        "model": "claude-3-haiku",
                    }
            except Exception:
                pass

            raise Exception(f"Anthropic API error: {response.status_code} - {response.text[:200]}")

    def analyze_with_gemini(self, content: str, content_type: str) -> dict[str, Any]:
        """Analyze content using Google Gemini"""
        api_key = self.api_keys["gemini"]

        prompt_map = {
            "AI_Image_Prompts": "As an AI image generation expert, analyze this prompt for visual quality and generation potential.",
            "Source_Originals": "As a content curator, analyze this source file for quality and creative value.",
        }

        system_prompt = prompt_map.get(content_type, "Analyze this creative content.")
        user_prompt = f"Content to analyze:\n\n{content[:2000]}"

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
                "generationConfig": {"maxOutputTokens": 500, "temperature": 0.3},
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            analysis = result["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "api": "gemini",
                "analysis": analysis,
                "confidence": 0.8,
                "model": "gemini-1.5-flash",
            }
        else:
            raise Exception(f"Gemini API error: {response.status_code}")

    def analyze_with_grok(self, content: str, content_type: str) -> dict[str, Any]:
        """Analyze content using Grok (xAI)"""
        api_key = self.api_keys["grok"]

        # Grok API endpoint (assuming similar to OpenAI format)
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "grok-beta",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Grok, a helpful AI. Analyze creative content with wit and insight.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this {content_type.replace('_', ' ')}:\n\n{content[:2000]}",
                    },
                ],
                "max_tokens": 500,
                "temperature": 0.4,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            return {
                "api": "grok",
                "analysis": analysis,
                "confidence": 0.85,
                "model": "grok-beta",
            }
        else:
            raise Exception(f"Grok API error: {response.status_code}")

    def enhanced_index_file(self, file_path: Path, categories: list[tuple]) -> bool:
        """Enhanced indexing with AI analysis"""
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

            # Basic analysis (same as original)
            best_category = None
            best_confidence = 0
            category_metadata = {}

            for cat_name, cat_config in categories:
                confidence, metadata = self.analyze_content_basic(content, cat_config)
                if confidence > best_confidence:
                    best_category = cat_name
                    best_confidence = confidence
                    category_metadata = metadata

            if best_confidence < 0.3:  # Minimum confidence threshold
                return False

            # AI-enhanced analysis
            ai_analysis = self.analyze_with_ai(content, best_category)

            # Store in database with AI insights
            return self.store_content_ai(
                file_path=file_path,
                category=best_category,
                confidence=best_confidence,
                ai_analysis=ai_analysis,
                size_bytes=file_size,
                checksum=checksum,
                content_preview=content[:1000],
                metadata=category_metadata,
            )

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return False

    # Include the basic analysis methods from the original NocturneMemory
    def analyze_content_basic(self, content: str, category_config: dict) -> tuple[float, dict]:
        """Basic content analysis (same as original)"""
        # [Copy the analyze_content method from nocturnememory.py]
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

    # Copy the metadata extraction methods from the original
    def extract_image_prompt_metadata(self, content: str) -> dict[str, Any]:
        # [Copy from original]
        metadata = {}
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

        subject_match = re.search(r"^(?:a |an )?([^-,\.\n]+?)(?:\s*[-,]|$)", content.strip(), re.IGNORECASE)
        if subject_match:
            metadata["subject"] = subject_match.group(1).strip()

        return metadata

    def extract_sora_prompt_metadata(self, content: str) -> dict[str, Any]:
        metadata = {}
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
        metadata = {}
        verses = len(re.findall(r"^\[Verse", content, re.MULTILINE | re.IGNORECASE))
        choruses = len(re.findall(r"^\[Chorus", content, re.MULTILINE | re.IGNORECASE))
        bridges = len(re.findall(r"^\[Bridge", content, re.MULTILINE | re.IGNORECASE))

        if verses:
            metadata["verses"] = verses
        if choruses:
            metadata["choruses"] = choruses
        if bridges:
            metadata["bridges"] = bridges

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
        metadata = {}
        timestamps = len(re.findall(r"\d{1,2}:\d{2}", content))
        if timestamps:
            metadata["segments"] = timestamps

        speakers = re.findall(r"(?:Speaker|Host|Guest)\s*\d*:", content, re.IGNORECASE)
        if speakers:
            metadata["speakers"] = len(set(speakers))

        return metadata

    def extract_analysis_metadata(self, content: str) -> dict[str, Any]:
        metadata = {}
        tempo_match = re.search(r"tempo.*(\d+).*bpm", content, re.IGNORECASE)
        if tempo_match:
            metadata["tempo"] = int(tempo_match.group(1))

        key_match = re.search(r"key.*([A-G][#b]?)\s*(major|minor)", content, re.IGNORECASE)
        if key_match:
            metadata["key"] = f"{key_match.group(1)} {key_match.group(2)}"

        genre_match = re.search(r"genre.*([a-zA-Z\s]+)", content, re.IGNORECASE)
        if genre_match:
            metadata["genre"] = genre_match.group(1).strip()

        return metadata

    def store_content_ai(
        self,
        file_path: Path,
        category: str,
        confidence: float,
        ai_analysis: dict,
        size_bytes: int,
        checksum: str,
        content_preview: str,
        metadata: dict,
    ) -> bool:
        """Store content with AI analysis in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            content_id = str(hashlib.md5(str(file_path).encode()).hexdigest())[:16]

            # Store main content index
            cursor.execute(
                """
                INSERT OR REPLACE INTO content_index
                (id, file_path, file_name, category, confidence, ai_confidence,
                 size_bytes, created_at, modified_at, checksum, content_preview,
                 metadata, ai_analysis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    content_id,
                    str(file_path),
                    file_path.name,
                    category,
                    confidence,
                    ai_analysis.get("confidence", 0.5),
                    size_bytes,
                    datetime.fromtimestamp(file_path.stat().st_ctime),
                    datetime.fromtimestamp(file_path.stat().st_mtime),
                    checksum,
                    content_preview,
                    json.dumps(metadata),
                    json.dumps(ai_analysis),
                ),
            )

            # Store AI analysis separately
            if "error" not in ai_analysis:
                analysis_id = f"{content_id}_{ai_analysis.get('api', 'unknown')}"
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO ai_analysis
                    (id, content_index_id, api_used, analysis_type, analysis_result,
                     confidence_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        analysis_id,
                        content_id,
                        ai_analysis.get("api"),
                        "content_analysis",
                        ai_analysis.get("analysis", ""),
                        ai_analysis.get("confidence", 0.5),
                        datetime.now(),
                    ),
                )

            # Build search index from content and AI analysis
            search_terms = set()

            # Extract terms from filename
            filename_terms = re.findall(r"\b\w{3,}\b", file_path.name.lower())
            search_terms.update(filename_terms)

            # Extract terms from content preview
            content_terms = re.findall(r"\b\w{3,}\b", content_preview.lower())
            search_terms.update(content_terms)

            # Extract terms from AI analysis if available
            if "error" not in ai_analysis and ai_analysis.get("analysis"):
                analysis_terms = re.findall(r"\b\w{3,}\b", ai_analysis["analysis"].lower())
                search_terms.update(analysis_terms[:20])  # Limit analysis terms

            # Store search terms
            for term in search_terms:
                if len(term) >= 3:  # Only meaningful terms
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO search_index
                        (id, content_index_id, search_term, category, weight, ai_generated)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            f"{content_id}_{term}",
                            content_id,
                            term,
                            category,
                            1.0,  # Base weight
                            "error" not in ai_analysis,
                        ),
                    )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error storing AI content: {e}")
            return False

    def scan_directory_ai(self, target_dir: str, recursive: bool = True, api_preference: str = None):
        """Scan directory for creative content with AI analysis"""
        target_path = Path(target_dir).expanduser().resolve()

        if not target_path.exists():
            print(f"Directory {target_path} does not exist")
            return

        print(f"🧠 AI-Enhanced Scanning {target_path} for creative content...")

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
                    if self.enhanced_index_file(file_path, relevant_categories):
                        indexed += 1

        print(f"✅ Indexed {indexed} creative content files with AI analysis")

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
                   ci.confidence, ci.ai_confidence, ci.content_preview
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
                    "ai_confidence": row[5] or 0,
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

        # AI analyses
        cursor.execute("SELECT COUNT(*) FROM ai_analysis")
        stats["ai_analyses"] = cursor.fetchone()[0]

        # Search terms
        cursor.execute("SELECT COUNT(*) FROM search_index")
        stats["search_terms"] = cursor.fetchone()[0]

        conn.close()
        return stats

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # Copy the CREATIVE_CATEGORIES from original
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
                ".csv",
                ".psd",
                ".aif",
                ".wav",
                ".flac",
            ],
            "content_indicators": ["original", "source", "master", "draft"],
        },
    }


def main():
    parser = argparse.ArgumentParser(description="NocturneMemory AI - Enhanced Creative Content Cache")
    parser.add_argument("command", choices=["scan", "search", "analyze", "stats"], help="Command to run")
    parser.add_argument("--path", help="Path to scan (for scan command)")
    parser.add_argument("--query", help="Search query (for search command)")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--api", help="Preferred API for analysis")
    parser.add_argument("--recursive", action="store_true", default=True, help="Scan recursively")

    args = parser.parse_args()

    memory = NocturneMemoryAI()

    print("🤖 NocturneMemory AI - Available APIs:")
    for api, available in memory.available_apis.items():
        status = "✅" if available else "❌"
        print(f"  {status} {api}")

    if args.command == "scan":
        if not args.path:
            print("Error: --path required for scan command")
            sys.exit(1)

        memory.scan_directory_ai(args.path, args.recursive, args.api)

    elif args.command == "analyze":
        if not args.path:
            print("Error: --path required for analyze command")
            sys.exit(1)

        # Analyze single file
        file_path = Path(args.path).expanduser().resolve()
        if file_path.exists() and file_path.is_file():
            ext = file_path.suffix.lower()
            categories = []
            for cat_name, cat_config in memory.CREATIVE_CATEGORIES.items():
                if ext in cat_config.get("file_extensions", []):
                    categories.append((cat_name, cat_config))

            if categories:
                success = memory.enhanced_index_file(file_path, categories)
                if success:
                    print("✅ File analyzed and indexed with AI insights")
                else:
                    print("❌ Failed to analyze file")
            else:
                print("❌ File type not supported for AI analysis")
        else:
            print("❌ File not found")

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
            if "ai_confidence" in result:
                print(f"   AI Confidence: {result['ai_confidence']:.2f}")
            print(f"   Path: {result['file_path']}")
            print(f"   Preview: {result['preview']}...")
            print()

    elif args.command == "stats":
        stats = memory.get_stats()
        print("NocturneMemory AI Statistics")
        print("=" * 35)
        print(f"Total content indexed: {stats['total_content']}")
        print(f"AI analyses performed: {stats.get('ai_analyses', 0)}")
        print(f"Search terms: {stats['search_terms']}")

        if stats.get("by_category"):
            print("\nBy category:")
            for category, count in stats["by_category"].items():
                print(f"  {category}: {count}")

        print(f"\n💾 Database: {memory.db_path}")


if __name__ == "__main__":
    main()
