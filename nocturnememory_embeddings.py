#!/usr/bin/env python3
"""
NocturneMemory Embeddings System - Vector-Based Semantic Search

Provides vector embeddings and semantic search capabilities:
- OpenAI text-embedding-3-small/large
- Gemini text-embedding-004
- Local fallback with sentence-transformers
- FAISS-based similarity search
- Relationship mapping via embeddings
"""

import hashlib
import pickle
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import requests

try:
    import faiss

    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: FAISS not available. Install with: pip install faiss-cpu")

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")


@dataclass
class EmbeddingResult:
    """Embedding generation result"""

    embedding: list[float]
    model: str
    dimension: int
    cost: float = 0.0


class EmbeddingsSystem:
    """Vector embeddings and semantic search system"""

    # Embedding model configurations
    EMBEDDING_MODELS = {
        "openai-small": {
            "name": "text-embedding-3-small",
            "dimension": 1536,
            "cost_per_1k_tokens": 0.02,
            "max_tokens": 8191,
        },
        "openai-large": {
            "name": "text-embedding-3-large",
            "dimension": 3072,
            "cost_per_1k_tokens": 0.13,
            "max_tokens": 8191,
        },
        "gemini": {
            "name": "text-embedding-004",
            "dimension": 768,
            "cost_per_1k_tokens": 0.01,
            "max_tokens": 2048,
        },
        "local": {
            "name": "all-MiniLM-L6-v2",
            "dimension": 384,
            "cost_per_1k_tokens": 0.0,
            "max_tokens": 512,
        },
    }

    def __init__(
        self,
        api_keys: dict[str, str],
        cache_dir: Path | None = None,
        use_local_fallback: bool = True,
    ):
        self.api_keys = api_keys
        self.cache_dir = cache_dir or Path.home() / ".nocTurneMeLoDieS" / ".memory"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_local_fallback = use_local_fallback

        # Initialize local model if available
        self.local_model = None
        if use_local_fallback and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.local_model = SentenceTransformer("all-MiniLM-L6-v2")
                print("✅ Local embedding model loaded")
            except Exception as e:
                print(f"Warning: Could not load local model: {e}")

        # FAISS index
        self.faiss_index = None
        self.embedding_dimension = None
        self.content_ids = []
        self.embeddings_cache = {}

        # Database for persistent storage
        self.db_path = self.cache_dir / "embeddings.db"
        self.init_database()

    def init_database(self):
        """Initialize embeddings database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Content embeddings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_embeddings (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                embedding_model TEXT,
                embedding_data BLOB,
                dimension INTEGER,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_index(id)
            )
        """
        )

        # Similarity relationships table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS similarity_relationships (
                id TEXT PRIMARY KEY,
                source_content_id TEXT,
                target_content_id TEXT,
                similarity_score REAL,
                relationship_type TEXT,
                embedding_model TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (source_content_id) REFERENCES content_index(id),
                FOREIGN KEY (target_content_id) REFERENCES content_index(id)
            )
        """
        )

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_id ON content_embeddings(content_id)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_similarity_source ON similarity_relationships(source_content_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_similarity_target ON similarity_relationships(target_content_id)"
        )

        conn.commit()
        conn.close()

    def generate_embedding(self, text: str, model: str = "auto", use_cache: bool = True) -> EmbeddingResult:
        """
        Generate embedding for text

        Args:
            text: Text to embed
            model: Model to use ('auto', 'openai-small', 'openai-large', 'gemini', 'local')
            use_cache: Use cached embeddings if available

        Returns:
            EmbeddingResult
        """
        # Check cache
        if use_cache:
            cache_key = hashlib.md5(f"{text}_{model}".encode()).hexdigest()
            if cache_key in self.embeddings_cache:
                return self.embeddings_cache[cache_key]

        # Auto-select model
        if model == "auto":
            model = self._select_best_model(text)

        # Generate embedding
        if model == "local" or (
            model == "auto" and not self.api_keys.get("openai") and not self.api_keys.get("gemini")
        ):
            result = self._generate_local_embedding(text)
        elif model.startswith("openai"):
            result = self._generate_openai_embedding(text, model)
        elif model == "gemini":
            result = self._generate_gemini_embedding(text)
        else:
            # Fallback to local
            result = self._generate_local_embedding(text)

        # Cache result
        if use_cache:
            self.embeddings_cache[cache_key] = result

        return result

    def _select_best_model(self, text: str) -> str:
        """Select best embedding model based on availability and text length"""
        text_length = len(text.split())

        # Prefer OpenAI if available
        if self.api_keys.get("openai"):
            if text_length <= 8000:
                return "openai-small"
            else:
                return "openai-large"

        # Fallback to Gemini
        if self.api_keys.get("gemini"):
            if text_length <= 2000:
                return "gemini"

        # Use local model
        return "local"

    def _generate_openai_embedding(self, text: str, model: str = "openai-small") -> EmbeddingResult:
        """Generate embedding using OpenAI API"""
        model_config = self.EMBEDDING_MODELS.get(model, self.EMBEDDING_MODELS["openai-small"])
        api_key = self.api_keys.get("openai")

        if not api_key:
            raise ValueError("OpenAI API key not available")

        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model_config["name"],
                "input": text[: model_config["max_tokens"] * 4],  # Rough token estimate
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            embedding = data["data"][0]["embedding"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            cost = (tokens / 1000) * model_config["cost_per_1k_tokens"]

            return EmbeddingResult(
                embedding=embedding,
                model=model_config["name"],
                dimension=model_config["dimension"],
                cost=cost,
            )
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")

    def _generate_gemini_embedding(self, text: str) -> EmbeddingResult:
        """Generate embedding using Gemini API"""
        model_config = self.EMBEDDING_MODELS["gemini"]
        api_key = self.api_keys.get("gemini")

        if not api_key:
            raise ValueError("Gemini API key not available")

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model_config['name']}:embedContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "model": f"models/{model_config['name']}",
                "content": {"parts": [{"text": text[: model_config["max_tokens"] * 4]}]},
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            embedding = data["embedding"]["values"]
            tokens = len(text.split())
            cost = (tokens / 1000) * model_config["cost_per_1k_tokens"]

            return EmbeddingResult(
                embedding=embedding,
                model=model_config["name"],
                dimension=model_config["dimension"],
                cost=cost,
            )
        else:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

    def _generate_local_embedding(self, text: str) -> EmbeddingResult:
        """Generate embedding using local sentence-transformers model"""
        if not self.local_model:
            raise ValueError("Local embedding model not available")

        embedding = self.local_model.encode(text, convert_to_numpy=True).tolist()

        return EmbeddingResult(
            embedding=embedding,
            model=self.EMBEDDING_MODELS["local"]["name"],
            dimension=self.EMBEDDING_MODELS["local"]["dimension"],
            cost=0.0,
        )

    def store_embedding(self, content_id: str, embedding_result: EmbeddingResult):
        """Store embedding in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        embedding_id = hashlib.md5(f"{content_id}_{embedding_result.model}".encode()).hexdigest()

        # Serialize embedding
        embedding_blob = pickle.dumps(embedding_result.embedding)

        cursor.execute(
            """
            INSERT OR REPLACE INTO content_embeddings
            (id, content_id, embedding_model, embedding_data, dimension, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                embedding_id,
                content_id,
                embedding_result.model,
                embedding_blob,
                embedding_result.dimension,
                datetime.now(),
            ),
        )

        conn.commit()
        conn.close()

    def get_embedding(self, content_id: str, model: str | None = None) -> list[float] | None:
        """Retrieve embedding from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if model:
            cursor.execute(
                """
                SELECT embedding_data FROM content_embeddings
                WHERE content_id = ? AND embedding_model = ?
                ORDER BY created_at DESC LIMIT 1
            """,
                (content_id, model),
            )
        else:
            cursor.execute(
                """
                SELECT embedding_data FROM content_embeddings
                WHERE content_id = ?
                ORDER BY created_at DESC LIMIT 1
            """,
                (content_id,),
            )

        row = cursor.fetchone()
        conn.close()

        if row:
            return pickle.loads(row[0])
        return None

    def cosine_similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Normalize
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(vec1, vec2) / (norm1 * norm2)

    def find_similar_content(
        self,
        query_embedding: list[float],
        content_ids: list[str],
        top_k: int = 10,
        threshold: float = 0.7,
    ) -> list[tuple[str, float]]:
        """
        Find similar content using embeddings

        Args:
            query_embedding: Query embedding vector
            content_ids: List of content IDs to search
            top_k: Number of results to return
            threshold: Minimum similarity threshold

        Returns:
            List of (content_id, similarity_score) tuples
        """
        similarities = []

        for content_id in content_ids:
            embedding = self.get_embedding(content_id)
            if embedding:
                similarity = self.cosine_similarity(query_embedding, embedding)
                if similarity >= threshold:
                    similarities.append((content_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def build_faiss_index(self, content_ids: list[str], dimension: int):
        """Build FAISS index for fast similarity search"""
        if not FAISS_AVAILABLE:
            raise ValueError("FAISS not available")

        self.embedding_dimension = dimension
        self.content_ids = content_ids

        # Create FAISS index (L2 distance, can be converted to cosine with normalization)
        self.faiss_index = faiss.IndexFlatL2(dimension)

        # Load embeddings and add to index
        embeddings_list = []
        valid_ids = []

        for content_id in content_ids:
            embedding = self.get_embedding(content_id)
            if embedding and len(embedding) == dimension:
                embeddings_list.append(embedding)
                valid_ids.append(content_id)

        if embeddings_list:
            embeddings_array = np.array(embeddings_list, dtype=np.float32)
            # Normalize for cosine similarity
            faiss.normalize_L2(embeddings_array)
            self.faiss_index.add(embeddings_array)
            self.content_ids = valid_ids

        return len(valid_ids)

    def search_faiss(self, query_embedding: list[float], top_k: int = 10) -> list[tuple[str, float]]:
        """Search using FAISS index"""
        if not self.faiss_index:
            raise ValueError("FAISS index not built")

        query_array = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_array)

        distances, indices = self.faiss_index.search(query_array, top_k)

        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.content_ids):
                # Convert L2 distance to similarity (1 - normalized distance)
                similarity = max(0.0, 1.0 - dist)
                results.append((self.content_ids[idx], similarity))

        return results

    def find_relationships(
        self,
        content_id: str,
        all_content_ids: list[str],
        threshold: float = 0.75,
        max_relationships: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Find relationships between content items

        Args:
            content_id: Source content ID
            all_content_ids: All content IDs to check
            threshold: Similarity threshold
            max_relationships: Maximum relationships to return

        Returns:
            List of relationship dictionaries
        """
        source_embedding = self.get_embedding(content_id)
        if not source_embedding:
            return []

        relationships = []

        for target_id in all_content_ids:
            if target_id == content_id:
                continue

            target_embedding = self.get_embedding(target_id)
            if target_embedding:
                similarity = self.cosine_similarity(source_embedding, target_embedding)

                if similarity >= threshold:
                    # Determine relationship type based on similarity
                    if similarity >= 0.9:
                        rel_type = "very_similar"
                    elif similarity >= 0.8:
                        rel_type = "similar"
                    else:
                        rel_type = "related"

                    relationships.append(
                        {
                            "source_id": content_id,
                            "target_id": target_id,
                            "similarity": similarity,
                            "relationship_type": rel_type,
                        }
                    )

        # Sort by similarity
        relationships.sort(key=lambda x: x["similarity"], reverse=True)

        # Store relationships in database
        self._store_relationships(relationships[:max_relationships])

        return relationships[:max_relationships]

    def _store_relationships(self, relationships: list[dict[str, Any]]):
        """Store relationships in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for rel in relationships:
            rel_id = hashlib.md5(f"{rel['source_id']}_{rel['target_id']}".encode()).hexdigest()

            cursor.execute(
                """
                INSERT OR REPLACE INTO similarity_relationships
                (id, source_content_id, target_content_id, similarity_score,
                 relationship_type, embedding_model, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    rel_id,
                    rel["source_id"],
                    rel["target_id"],
                    rel["similarity"],
                    rel["relationship_type"],
                    "auto",
                    datetime.now(),
                ),
            )

        conn.commit()
        conn.close()
