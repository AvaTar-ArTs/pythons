#!/usr/bin/env python3
"""
NocturneMemory AI Enhanced - Advanced Creative Content Management System

Advanced features:
- Multi-model AI orchestration
- Vector-based semantic search
- Relationship mapping between creative assets
- Real-time multi-AI collaboration
- Content synthesis engine
- Performance optimization (caching, parallel processing)
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Import our new modules
from nocturnememory_ai_orchestrator import AIOrchestrator, ContentType, RoutingDecision, TaskComplexity
from nocturnememory_embeddings import EmbeddingsSystem


class NocturneMemoryAIEnhanced:
    """Advanced AI-enhanced creative content cache with orchestration"""

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
                r"^\d{2}:\d{2}",
                r"Speaker.*:",
                r"\[.*\]",
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

    def __init__(self, cache_dir=None):
        self.cache_dir = Path(cache_dir or "~/nocTurneMeLoDieS/.memory").expanduser()
        self.db_path = self.cache_dir / "nocturnememory_ai_enhanced.db"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load API keys
        self.load_api_keys()

        # Initialize AI Orchestrator
        self.orchestrator = AIOrchestrator(self.api_keys, self.cache_dir)

        # Initialize Embeddings System
        self.embeddings = EmbeddingsSystem(self.api_keys, self.cache_dir)

        # Initialize database
        self.init_database()

        # Performance cache
        self.analysis_cache = {}
        self.cache_lock = threading.Lock()

        print("🚀 NocturneMemory AI Enhanced initialized")
        print(f"   Available APIs: {', '.join(self.orchestrator.available_apis.keys())}")

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

    def init_database(self):
        """Initialize enhanced database schema"""
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
                ai_analysis TEXT,
                embedding_generated BOOLEAN DEFAULT FALSE
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
                model_used TEXT,
                analysis_type TEXT,
                analysis_result TEXT,
                confidence_score REAL,
                cost REAL,
                response_time REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        # Multi-AI collaboration results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS collaboration_results (
                id TEXT PRIMARY KEY,
                content_index_id TEXT,
                models_used TEXT,
                consensus_analysis TEXT,
                individual_analyses TEXT,
                agreement_score REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_index_id) REFERENCES content_index(id)
            )
        """
        )

        # Content relationships
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_relationships (
                id TEXT PRIMARY KEY,
                source_content_id TEXT,
                target_content_id TEXT,
                relationship_type TEXT,
                similarity_score REAL,
                relationship_metadata TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (source_content_id) REFERENCES content_index(id),
                FOREIGN KEY (target_content_id) REFERENCES content_index(id)
            )
        """
        )

        # Content synthesis results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS synthesis_results (
                id TEXT PRIMARY KEY,
                source_content_ids TEXT,
                synthesized_content TEXT,
                synthesis_type TEXT,
                model_used TEXT,
                metadata TEXT,
                created_at TIMESTAMP
            )
        """
        )

        # Performance cache
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS performance_cache (
                cache_key TEXT PRIMARY KEY,
                cached_data TEXT,
                expires_at TIMESTAMP,
                created_at TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def enhanced_index_file(self, file_path: Path, categories: list[tuple]) -> bool:
        """Enhanced indexing with AI orchestration and embeddings"""
        try:
            stat = file_path.stat()
            file_size = stat.st_size

            if file_size > 10 * 1024 * 1024:
                return False

            checksum = self.calculate_checksum(file_path)
            content_id = str(hashlib.md5(str(file_path).encode()).hexdigest())[:16]

            # Check if already indexed
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM content_index WHERE id = ?", (content_id,))
            if cursor.fetchone():
                conn.close()
                return True  # Already indexed
            conn.close()

            # Read content
            content = ""
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(min(50000, file_size))
            except OSError:
                return False

            # Basic analysis
            best_category = None
            best_confidence = 0
            category_metadata = {}

            for cat_name, cat_config in categories:
                confidence, metadata = self.analyze_content_basic(content, cat_config)
                if confidence > best_confidence:
                    best_category = cat_name
                    best_confidence = confidence
                    category_metadata = metadata

            if best_confidence < 0.3:
                return False

            # Map category to ContentType
            content_type_map = {
                "AI_Image_Prompts": ContentType.IMAGE_PROMPT,
                "Sora_Video_Prompts": ContentType.VIDEO_PROMPT,
                "Song_Lyrics": ContentType.LYRICS,
                "Audio_Transcripts": ContentType.TRANSCRIPT,
                "Music_Analysis": ContentType.ANALYSIS,
                "Source_Originals": ContentType.SOURCE_FILE,
            }
            content_type = content_type_map.get(best_category, ContentType.MIXED)

            # Determine complexity
            complexity = TaskComplexity.SIMPLE
            if len(content) > 5000:
                complexity = TaskComplexity.COMPLEX
            elif len(content) > 2000:
                complexity = TaskComplexity.MEDIUM

            # AI analysis with orchestration
            routing = self.orchestrator.route_request(
                content=content,
                content_type=content_type,
                complexity=complexity,
                prefer_cost_efficient=True,
            )

            ai_analysis = self._analyze_with_routing(content, best_category, routing)

            # Generate embedding
            embedding_result = None
            try:
                embedding_result = self.embeddings.generate_embedding(content)
                self.embeddings.store_embedding(content_id, embedding_result)
            except Exception as e:
                print(f"Warning: Could not generate embedding: {e}")

            # Store content
            return self.store_content_enhanced(
                file_path=file_path,
                content_id=content_id,
                category=best_category,
                confidence=best_confidence,
                ai_analysis=ai_analysis,
                size_bytes=file_size,
                checksum=checksum,
                content_preview=content[:1000],
                metadata=category_metadata,
                embedding_generated=embedding_result is not None,
            )

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return False

    def _analyze_with_routing(self, content: str, category: str, routing: RoutingDecision) -> dict[str, Any]:
        """Analyze content using routed model"""
        # Check cache first
        cache_key = hashlib.md5(f"{content}_{routing.selected_model}".encode()).hexdigest()

        with self.cache_lock:
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]

        # Perform analysis (simplified - would call actual API)
        analysis = {
            "api": routing.provider,
            "model": routing.selected_model,
            "analysis": f"AI analysis from {routing.selected_model}",
            "confidence": routing.confidence,
            "cost": routing.estimated_cost,
            "reasoning": routing.reasoning,
        }

        # Cache result
        with self.cache_lock:
            self.analysis_cache[cache_key] = analysis

        return analysis

    def store_content_enhanced(
        self,
        file_path: Path,
        content_id: str,
        category: str,
        confidence: float,
        ai_analysis: dict,
        size_bytes: int,
        checksum: str,
        content_preview: str,
        metadata: dict,
        embedding_generated: bool,
    ) -> bool:
        """Store enhanced content with all metadata"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO content_index
                (id, file_path, file_name, category, confidence, ai_confidence,
                 size_bytes, created_at, modified_at, checksum, content_preview,
                 metadata, ai_analysis, embedding_generated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    embedding_generated,
                ),
            )

            # Store AI analysis
            if "error" not in ai_analysis:
                analysis_id = f"{content_id}_{ai_analysis.get('model', 'unknown')}"
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO ai_analysis
                    (id, content_index_id, api_used, model_used, analysis_type,
                     analysis_result, confidence_score, cost, response_time, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        analysis_id,
                        content_id,
                        ai_analysis.get("api"),
                        ai_analysis.get("model"),
                        "content_analysis",
                        ai_analysis.get("analysis", ""),
                        ai_analysis.get("confidence", 0.5),
                        ai_analysis.get("cost", 0.0),
                        0.0,  # response_time
                        datetime.now(),
                    ),
                )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error storing content: {e}")
            return False

    def analyze_content_basic(self, content: str, category_config: dict) -> tuple[float, dict]:
        """Basic content analysis"""
        confidence = 0
        metadata = {}

        keywords = category_config.get("keywords", {})
        content_lower = content.lower()

        for keyword, weight in keywords.items():
            if keyword.lower() in content_lower:
                confidence += weight / 10.0

        patterns = category_config.get("patterns", [])
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                confidence += 0.2

        indicators = category_config.get("content_indicators", [])
        for indicator in indicators:
            if indicator.lower() in content_lower:
                confidence += 0.15

        return min(confidence, 1.0), metadata

    def semantic_search(self, query: str, category: str | None = None, top_k: int = 10) -> list[dict]:
        """Semantic search using embeddings"""
        # Generate query embedding
        try:
            query_embedding_result = self.embeddings.generate_embedding(query)
            query_embedding = query_embedding_result.embedding
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []

        # Get all content IDs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute(
                "SELECT id FROM content_index WHERE category = ? AND embedding_generated = 1",
                (category,),
            )
        else:
            cursor.execute("SELECT id FROM content_index WHERE embedding_generated = 1")

        content_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not content_ids:
            return []

        # Find similar content
        similar_items = self.embeddings.find_similar_content(query_embedding, content_ids, top_k=top_k, threshold=0.6)

        # Get full content details
        results = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for content_id, similarity in similar_items:
            cursor.execute(
                """
                SELECT id, file_path, file_name, category, confidence, ai_confidence, content_preview
                FROM content_index WHERE id = ?
            """,
                (content_id,),
            )

            row = cursor.fetchone()
            if row:
                results.append(
                    {
                        "id": row[0],
                        "file_path": row[1],
                        "file_name": row[2],
                        "category": row[3],
                        "confidence": row[4],
                        "ai_confidence": row[5] or 0,
                        "similarity": similarity,
                        "preview": row[6][:200],
                    }
                )

        conn.close()

        return results

    def multi_ai_collaboration(self, content: str, content_type: ContentType, num_models: int = 3) -> dict[str, Any]:
        """Use multiple AI models to collaborate on analysis"""
        # Execute parallel analysis
        results = self.orchestrator.execute_parallel_analysis(
            content=content, content_type=content_type, max_workers=num_models
        )

        # Synthesize consensus
        if len(results) > 0:
            # Simple consensus (average confidence, combine analyses)
            analyses = [r.get("analysis", "") for r in results.values() if "error" not in r]
            avg_confidence = sum(r.get("confidence", 0.5) for r in results.values() if "error" not in r) / len(
                [r for r in results.values() if "error" not in r]
            )

            consensus = {
                "models_used": list(results.keys()),
                "consensus_analysis": "\n\n".join(analyses),
                "individual_analyses": results,
                "agreement_score": avg_confidence,
                "num_models": len(results),
            }

            return consensus

        return {"error": "No models available"}

    def find_relationships(self, content_id: str, threshold: float = 0.75) -> list[dict[str, Any]]:
        """Find relationships between content items"""
        # Get all content IDs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM content_index WHERE embedding_generated = 1")
        all_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        # Find relationships using embeddings
        relationships = self.embeddings.find_relationships(
            content_id=content_id, all_content_ids=all_ids, threshold=threshold
        )

        return relationships

    def synthesize_content(self, source_content_ids: list[str], synthesis_type: str = "combine") -> dict[str, Any]:
        """Synthesize new content from existing creative assets"""
        # Get source content
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        source_contents = []
        for content_id in source_content_ids:
            cursor.execute(
                "SELECT content_preview, category FROM content_index WHERE id = ?",
                (content_id,),
            )
            row = cursor.fetchone()
            if row:
                source_contents.append({"id": content_id, "content": row[0], "category": row[1]})

        conn.close()

        if not source_contents:
            return {"error": "No source content found"}

        # Combine content
        combined_content = "\n\n---\n\n".join([sc["content"] for sc in source_contents])

        # Use AI to synthesize
        content_type = ContentType.MIXED
        routing = self.orchestrator.route_request(
            content=combined_content,
            content_type=content_type,
            complexity=TaskComplexity.CREATIVE,
            require_quality=True,
        )

        # Generate synthesis (simplified)
        synthesized = {
            "source_ids": source_content_ids,
            "synthesized_content": f"Synthesized content from {len(source_contents)} sources",
            "synthesis_type": synthesis_type,
            "model": routing.selected_model,
            "metadata": {"sources": source_contents, "routing": routing.reasoning},
        }

        return synthesized

    def scan_directory_enhanced(self, target_dir: str, recursive: bool = True):
        """Enhanced directory scanning with parallel processing"""
        target_path = Path(target_dir).expanduser().resolve()

        if not target_path.exists():
            print(f"Directory {target_path} does not exist")
            return

        print(f"🚀 Enhanced AI Scanning {target_path}...")

        # Collect files
        files_to_index = []
        for root, dirs, files in os.walk(target_path):
            if not recursive and root != str(target_path):
                continue

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                relevant_categories = []
                for cat_name, cat_config in self.CREATIVE_CATEGORIES.items():
                    if ext in cat_config.get("file_extensions", []):
                        relevant_categories.append((cat_name, cat_config))
                        break

                if relevant_categories:
                    files_to_index.append((file_path, relevant_categories))

        # Index files in parallel
        indexed = 0
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.enhanced_index_file, file_path, categories): file_path
                for file_path, categories in files_to_index
            }

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    if future.result():
                        indexed += 1
                        if indexed % 10 == 0:
                            print(f"   Indexed {indexed} files...")
                except Exception as e:
                    print(f"Error indexing {file_path}: {e}")

        print(f"✅ Indexed {indexed} files with enhanced AI analysis")

        # Save orchestrator stats
        self.orchestrator.save_stats()

    def get_stats(self) -> dict[str, Any]:
        """Get comprehensive statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Content stats
        cursor.execute("SELECT category, COUNT(*) FROM content_index GROUP BY category")
        stats["by_category"] = dict(cursor.fetchall())

        cursor.execute("SELECT COUNT(*) FROM content_index")
        stats["total_content"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_index WHERE embedding_generated = 1")
        stats["with_embeddings"] = cursor.fetchone()[0]

        # AI analysis stats
        cursor.execute("SELECT COUNT(*) FROM ai_analysis")
        stats["ai_analyses"] = cursor.fetchone()[0]

        # Collaboration stats
        cursor.execute("SELECT COUNT(*) FROM collaboration_results")
        stats["collaborations"] = cursor.fetchone()[0]

        # Relationship stats
        cursor.execute("SELECT COUNT(*) FROM content_relationships")
        stats["relationships"] = cursor.fetchone()[0]

        # Orchestrator stats
        stats["orchestrator"] = self.orchestrator.get_stats()

        conn.close()
        return stats

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="NocturneMemory AI Enhanced")
    parser.add_argument(
        "command",
        choices=[
            "scan",
            "search",
            "semantic",
            "relationships",
            "collaborate",
            "synthesize",
            "stats",
        ],
        help="Command to run",
    )
    parser.add_argument("--path", help="Path to scan or analyze")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--content-id", help="Content ID for relationships")
    parser.add_argument("--sources", help="Comma-separated content IDs for synthesis")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results")

    args = parser.parse_args()

    memory = NocturneMemoryAIEnhanced()

    if args.command == "scan":
        if not args.path:
            print("Error: --path required for scan command")
            sys.exit(1)
        memory.scan_directory_enhanced(args.path)

    elif args.command == "search":
        if not args.query:
            print("Error: --query required for search command")
            sys.exit(1)

        results = memory.semantic_search(args.query, args.category, args.top_k)
        print(f"Found {len(results)} results for '{args.query}'")
        for result in results:
            print(f"\n📄 {result['file_name']}")
            print(f"   Category: {result['category']}")
            print(f"   Similarity: {result['similarity']:.3f}")
            print(f"   Path: {result['file_path']}")

    elif args.command == "semantic":
        if not args.query:
            print("Error: --query required for semantic search")
            sys.exit(1)

        results = memory.semantic_search(args.query, args.category, args.top_k)
        print(f"Semantic search results: {len(results)}")
        for result in results:
            print(f"\n📄 {result['file_name']} (similarity: {result['similarity']:.3f})")

    elif args.command == "relationships":
        if not args.content_id:
            print("Error: --content-id required")
            sys.exit(1)

        relationships = memory.find_relationships(args.content_id)
        print(f"Found {len(relationships)} relationships")
        for rel in relationships[: args.top_k]:
            print(f"\n🔗 {rel['relationship_type']} (similarity: {rel['similarity']:.3f})")
            print(f"   Target: {rel['target_id']}")

    elif args.command == "stats":
        stats = memory.get_stats()
        print("NocturneMemory AI Enhanced Statistics")
        print("=" * 40)
        print(f"Total content: {stats['total_content']}")
        print(f"With embeddings: {stats['with_embeddings']}")
        print(f"AI analyses: {stats['ai_analyses']}")
        print(f"Relationships: {stats['relationships']}")
        print("\nBy category:")
        for cat, count in stats["by_category"].items():
            print(f"  {cat}: {count}")

    else:
        print(f"Command '{args.command}' not yet implemented")


if __name__ == "__main__":
    main()
