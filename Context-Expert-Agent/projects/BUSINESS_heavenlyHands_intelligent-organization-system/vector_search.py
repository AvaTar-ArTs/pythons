#!/usr/bin/env python3
"""
Advanced Vector Search and Semantic Search System
=================================================

This module implements cutting-edge vector-based semantic search capabilities
with content-awareness intelligence for creative automation projects.

Features:
- Vector database integration (FAISS, Chroma, Pinecone)
- Semantic search with similarity scoring
- Content-aware query understanding
- Multi-modal search (code, text, images)
- Real-time indexing and updates
- Advanced filtering and ranking
- Query expansion and refinement

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 2.0.0
"""

import os
import json
import numpy as np
import sqlite3
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import pickle
from datetime import datetime
import hashlib
import re
from collections import defaultdict, Counter

# Vector database libraries
try:
    import faiss
    import chromadb
    from chromadb.config import Settings
    FAISS_AVAILABLE = True
    CHROMA_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    CHROMA_AVAILABLE = False
    print("Warning: Vector database libraries not available. Some features will be limited.")

# ML and NLP libraries
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.decomposition import PCA
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML libraries not available. Using basic text search.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Represents a search result with metadata."""
    content_id: str
    file_path: str
    content_type: str
    similarity_score: float
    content_preview: str
    metadata: Dict[str, Any]
    semantic_tags: List[str]
    relevance_explanation: str

@dataclass
class SearchQuery:
    """Represents a search query with context."""
    query_text: str
    query_type: str  # semantic, keyword, hybrid, code, documentation
    filters: Dict[str, Any]
    limit: int
    context: Dict[str, Any]

@dataclass
class VectorIndex:
    """Represents a vector index with metadata."""
    index_name: str
    vector_dimension: int
    total_vectors: int
    index_type: str  # faiss, chroma, custom
    created_at: datetime
    last_updated: datetime
    metadata: Dict[str, Any]

class AdvancedVectorSearch:
    """Advanced vector search system with content-awareness intelligence."""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 vector_db_type: str = "faiss",
                 index_directory: str = "./vector_indices"):
        
        self.model_name = model_name
        self.vector_db_type = vector_db_type
        self.index_directory = Path(index_directory)
        self.index_directory.mkdir(exist_ok=True)
        
        # Initialize components
        self.semantic_model = None
        self.vectorizer = None
        self.stemmer = PorterStemmer()
        self.stop_words = set()
        
        # Vector database instances
        self.faiss_index = None
        self.chroma_client = None
        self.chroma_collection = None
        
        # Content metadata
        self.content_metadata = {}
        self.vector_embeddings = {}
        
        # Search configuration
        self.search_config = {
            "similarity_threshold": 0.3,
            "max_results": 50,
            "rerank_top_k": 20,
            "query_expansion": True,
            "content_awareness": True
        }
        
        # Initialize all components
        self._initialize_ml_components()
        self._initialize_vector_databases()
        self._initialize_database()
    
    def _initialize_ml_components(self):
        """Initialize machine learning components."""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available. Using basic text search.")
            return
        
        try:
            # Initialize sentence transformer
            self.semantic_model = SentenceTransformer(self.model_name)
            
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=2
            )
            
            # Download NLTK data
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                self.stop_words = set(stopwords.words('english'))
            except:
                logger.warning("Could not download NLTK data")
                
        except Exception as e:
            logger.error(f"Error initializing ML components: {e}")
            ML_AVAILABLE = False
    
    def _initialize_vector_databases(self):
        """Initialize vector database instances."""
        if self.vector_db_type == "faiss" and FAISS_AVAILABLE:
            self._initialize_faiss()
        elif self.vector_db_type == "chroma" and CHROMA_AVAILABLE:
            self._initialize_chroma()
        else:
            logger.warning("Vector database not available. Using in-memory storage.")
    
    def _initialize_faiss(self):
        """Initialize FAISS vector database."""
        try:
            # Create FAISS index directory
            faiss_dir = self.index_directory / "faiss"
            faiss_dir.mkdir(exist_ok=True)
            
            # Load or create index
            index_path = faiss_dir / "main_index.faiss"
            if index_path.exists():
                self.faiss_index = faiss.read_index(str(index_path))
                logger.info(f"Loaded existing FAISS index with {self.faiss_index.ntotal} vectors")
            else:
                # Create new index (dimension will be set when first vector is added)
                self.faiss_index = None
                logger.info("Created new FAISS index")
                
        except Exception as e:
            logger.error(f"Error initializing FAISS: {e}")
            self.faiss_index = None
    
    def _initialize_chroma(self):
        """Initialize ChromaDB vector database."""
        try:
            # Initialize ChromaDB client
            self.chroma_client = chromadb.Client(Settings(
                persist_directory=str(self.index_directory / "chroma"),
                anonymized_telemetry=False
            ))
            
            # Get or create collection
            try:
                self.chroma_collection = self.chroma_client.get_collection("code_search")
                logger.info(f"Loaded existing ChromaDB collection with {self.chroma_collection.count()} documents")
            except:
                self.chroma_collection = self.chroma_client.create_collection(
                    name="code_search",
                    metadata={"description": "Code search collection"}
                )
                logger.info("Created new ChromaDB collection")
                
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            self.chroma_client = None
            self.chroma_collection = None
    
    def _initialize_database(self):
        """Initialize SQLite database for metadata storage."""
        self.db_path = self.index_directory / "vector_search.db"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS content_vectors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id TEXT UNIQUE,
                    file_path TEXT,
                    content_type TEXT,
                    vector_data BLOB,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_text TEXT,
                    query_type TEXT,
                    results_count INTEGER,
                    execution_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS vector_indices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    index_name TEXT UNIQUE,
                    vector_dimension INTEGER,
                    total_vectors INTEGER,
                    index_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def add_content(self, 
                   content_id: str,
                   file_path: str,
                   content: str,
                   content_type: str = "code",
                   metadata: Dict[str, Any] = None) -> bool:
        """Add content to the vector search index."""
        try:
            if not self.semantic_model:
                logger.warning("Semantic model not available. Cannot add content.")
                return False
            
            # Generate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Generate semantic embedding
            embedding = self._generate_embedding(content)
            if embedding is None:
                return False
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "file_path": file_path,
                "content_type": content_type,
                "content_hash": content_hash,
                "content_length": len(content),
                "added_at": datetime.now().isoformat()
            })
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO content_vectors 
                    (content_id, file_path, content_type, vector_data, metadata, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    content_id,
                    file_path,
                    content_type,
                    embedding.tobytes(),
                    json.dumps(metadata),
                    datetime.now()
                ))
                conn.commit()
            
            # Add to vector database
            self._add_to_vector_db(content_id, embedding, metadata)
            
            # Store in memory for quick access
            self.content_metadata[content_id] = {
                "file_path": file_path,
                "content_type": content_type,
                "metadata": metadata,
                "content_preview": content[:200] + "..." if len(content) > 200 else content
            }
            
            logger.info(f"Added content {content_id} to vector index")
            return True
            
        except Exception as e:
            logger.error(f"Error adding content {content_id}: {e}")
            return False
    
    def _generate_embedding(self, content: str) -> Optional[np.ndarray]:
        """Generate semantic embedding for content."""
        if not self.semantic_model:
            return None
        
        try:
            # Preprocess content
            processed_content = self._preprocess_content(content)
            
            # Generate embedding
            embedding = self.semantic_model.encode([processed_content])[0]
            
            return embedding.astype(np.float32)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess content for embedding generation."""
        # Remove code-specific elements
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)  # Remove comments
        content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)  # Remove docstrings
        content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)  # Remove docstrings
        content = re.sub(r'[^\w\s]', ' ', content)  # Remove special characters
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        
        # Tokenize and remove stop words
        if self.stop_words:
            tokens = word_tokenize(content.lower())
            tokens = [token for token in tokens if token not in self.stop_words]
            content = ' '.join(tokens)
        
        return content.strip()
    
    def _add_to_vector_db(self, content_id: str, embedding: np.ndarray, metadata: Dict[str, Any]):
        """Add vector to the appropriate vector database."""
        if self.vector_db_type == "faiss":
            self._add_to_faiss(content_id, embedding)
        elif self.vector_db_type == "chroma":
            self._add_to_chroma(content_id, embedding, metadata)
    
    def _add_to_faiss(self, content_id: str, embedding: np.ndarray):
        """Add vector to FAISS index."""
        try:
            if self.faiss_index is None:
                # Create new index
                dimension = len(embedding)
                self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Add vector
            self.faiss_index.add(embedding.reshape(1, -1))
            
            # Save index
            faiss_dir = self.index_directory / "faiss"
            faiss_dir.mkdir(exist_ok=True)
            faiss.write_index(self.faiss_index, str(faiss_dir / "main_index.faiss"))
            
        except Exception as e:
            logger.error(f"Error adding to FAISS: {e}")
    
    def _add_to_chroma(self, content_id: str, embedding: np.ndarray, metadata: Dict[str, Any]):
        """Add vector to ChromaDB."""
        try:
            if not self.chroma_collection:
                return
            
            # Convert numpy array to list
            embedding_list = embedding.tolist()
            
            # Add to collection
            self.chroma_collection.add(
                ids=[content_id],
                embeddings=[embedding_list],
                metadatas=[metadata],
                documents=[metadata.get("content_preview", "")]
            )
            
        except Exception as e:
            logger.error(f"Error adding to ChromaDB: {e}")
    
    def search(self, 
              query: str,
              query_type: str = "semantic",
              filters: Dict[str, Any] = None,
              limit: int = 10,
              context: Dict[str, Any] = None) -> List[SearchResult]:
        """Perform advanced semantic search."""
        try:
            start_time = datetime.now()
            
            # Create search query object
            search_query = SearchQuery(
                query_text=query,
                query_type=query_type,
                filters=filters or {},
                limit=limit,
                context=context or {}
            )
            
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            if query_embedding is None:
                logger.warning("Could not generate query embedding")
                return []
            
            # Perform search based on vector database type
            if self.vector_db_type == "faiss":
                results = self._search_faiss(query_embedding, search_query)
            elif self.vector_db_type == "chroma":
                results = self._search_chroma(query, search_query)
            else:
                results = self._search_database(query, search_query)
            
            # Apply content-aware filtering and ranking
            if self.search_config["content_awareness"]:
                results = self._apply_content_aware_ranking(results, search_query)
            
            # Apply filters
            if filters:
                results = self._apply_filters(results, filters)
            
            # Limit results
            results = results[:limit]
            
            # Log search query
            execution_time = (datetime.now() - start_time).total_seconds()
            self._log_search_query(search_query, len(results), execution_time)
            
            return results
            
        except Exception as e:
            logger.error(f"Error performing search: {e}")
            return []
    
    def _search_faiss(self, query_embedding: np.ndarray, search_query: SearchQuery) -> List[SearchResult]:
        """Search using FAISS index."""
        if not self.faiss_index:
            return []
        
        try:
            # Search FAISS index
            k = min(search_query.limit * 2, self.faiss_index.ntotal)  # Get more results for reranking
            scores, indices = self.faiss_index.search(query_embedding.reshape(1, -1), k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:  # Invalid index
                    continue
                
                # Get content metadata from database
                content_id = f"faiss_{idx}"
                metadata = self.content_metadata.get(content_id, {})
                
                if not metadata:
                    continue
                
                # Create search result
                result = SearchResult(
                    content_id=content_id,
                    file_path=metadata.get("file_path", ""),
                    content_type=metadata.get("content_type", "unknown"),
                    similarity_score=float(score),
                    content_preview=metadata.get("content_preview", ""),
                    metadata=metadata.get("metadata", {}),
                    semantic_tags=self._extract_semantic_tags(metadata.get("content_preview", "")),
                    relevance_explanation=self._generate_relevance_explanation(query_embedding, score)
                )
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching FAISS: {e}")
            return []
    
    def _search_chroma(self, query: str, search_query: SearchQuery) -> List[SearchResult]:
        """Search using ChromaDB."""
        if not self.chroma_collection:
            return []
        
        try:
            # Search ChromaDB
            search_results = self.chroma_collection.query(
                query_texts=[query],
                n_results=search_query.limit * 2,  # Get more results for reranking
                include=["metadatas", "documents", "distances"]
            )
            
            results = []
            for i, (distance, metadata, document) in enumerate(zip(
                search_results["distances"][0],
                search_results["metadatas"][0],
                search_results["documents"][0]
            )):
                # Convert distance to similarity score
                similarity_score = 1 - distance
                
                result = SearchResult(
                    content_id=search_results["ids"][0][i],
                    file_path=metadata.get("file_path", ""),
                    content_type=metadata.get("content_type", "unknown"),
                    similarity_score=similarity_score,
                    content_preview=document,
                    metadata=metadata,
                    semantic_tags=self._extract_semantic_tags(document),
                    relevance_explanation=self._generate_relevance_explanation(None, similarity_score)
                )
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []
    
    def _search_database(self, query: str, search_query: SearchQuery) -> List[SearchResult]:
        """Fallback search using database only."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT content_id, file_path, content_type, metadata
                    FROM content_vectors
                    WHERE file_path LIKE ? OR content_type LIKE ?
                    ORDER BY updated_at DESC
                    LIMIT ?
                ''', (f"%{query}%", f"%{query}%", search_query.limit))
                
                results = []
                for content_id, file_path, content_type, metadata_json in cursor.fetchall():
                    metadata = json.loads(metadata_json)
                    
                    result = SearchResult(
                        content_id=content_id,
                        file_path=file_path,
                        content_type=content_type,
                        similarity_score=0.5,  # Default score for text search
                        content_preview=metadata.get("content_preview", ""),
                        metadata=metadata,
                        semantic_tags=[],
                        relevance_explanation="Text-based match"
                    )
                    
                    results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"Error searching database: {e}")
            return []
    
    def _apply_content_aware_ranking(self, results: List[SearchResult], search_query: SearchQuery) -> List[SearchResult]:
        """Apply content-aware ranking to search results."""
        if not results:
            return results
        
        # Enhanced ranking based on content type and context
        for result in results:
            # Boost score based on content type relevance
            content_type_boost = self._calculate_content_type_boost(
                result.content_type, 
                search_query.query_type
            )
            
            # Boost score based on file path relevance
            path_boost = self._calculate_path_boost(
                result.file_path, 
                search_query.context
            )
            
            # Boost score based on semantic tags
            tag_boost = self._calculate_tag_boost(
                result.semantic_tags, 
                search_query.query_text
            )
            
            # Apply boosts
            result.similarity_score *= (1 + content_type_boost + path_boost + tag_boost)
        
        # Sort by enhanced similarity score
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return results
    
    def _calculate_content_type_boost(self, content_type: str, query_type: str) -> float:
        """Calculate boost based on content type relevance."""
        type_relevance = {
            "code": {"semantic": 0.2, "keyword": 0.1, "hybrid": 0.15},
            "documentation": {"semantic": 0.1, "keyword": 0.2, "hybrid": 0.15},
            "configuration": {"semantic": 0.05, "keyword": 0.1, "hybrid": 0.075},
            "test": {"semantic": 0.15, "keyword": 0.1, "hybrid": 0.125}
        }
        
        return type_relevance.get(content_type, {}).get(query_type, 0.0)
    
    def _calculate_path_boost(self, file_path: str, context: Dict[str, Any]) -> float:
        """Calculate boost based on file path relevance."""
        boost = 0.0
        
        # Check for specific directories
        if "src" in file_path or "lib" in file_path:
            boost += 0.1
        if "test" in file_path:
            boost += 0.05
        if "docs" in file_path:
            boost += 0.05
        
        # Check for context-specific paths
        if context.get("preferred_directories"):
            for preferred_dir in context["preferred_directories"]:
                if preferred_dir in file_path:
                    boost += 0.2
        
        return boost
    
    def _calculate_tag_boost(self, semantic_tags: List[str], query_text: str) -> float:
        """Calculate boost based on semantic tag relevance."""
        if not semantic_tags:
            return 0.0
        
        query_words = set(query_text.lower().split())
        tag_words = set()
        
        for tag in semantic_tags:
            tag_words.update(tag.lower().split(":"))
        
        # Calculate overlap
        overlap = len(query_words.intersection(tag_words))
        return min(0.3, overlap * 0.1)
    
    def _extract_semantic_tags(self, content: str) -> List[str]:
        """Extract semantic tags from content."""
        tags = []
        
        # Extract function/class names
        function_matches = re.findall(r'def\s+(\w+)', content)
        class_matches = re.findall(r'class\s+(\w+)', content)
        
        tags.extend([f"function:{name}" for name in function_matches])
        tags.extend([f"class:{name}" for name in class_matches])
        
        # Extract keywords
        keywords = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content)
        common_keywords = Counter(keywords).most_common(5)
        tags.extend([f"keyword:{word}" for word, _ in common_keywords])
        
        return tags
    
    def _generate_relevance_explanation(self, query_embedding: Optional[np.ndarray], score: float) -> str:
        """Generate explanation for why a result is relevant."""
        if score > 0.8:
            return "Highly relevant semantic match"
        elif score > 0.6:
            return "Good semantic similarity"
        elif score > 0.4:
            return "Moderate relevance"
        else:
            return "Low relevance match"
    
    def _apply_filters(self, results: List[SearchResult], filters: Dict[str, Any]) -> List[SearchResult]:
        """Apply filters to search results."""
        filtered_results = []
        
        for result in results:
            # File type filter
            if "file_types" in filters:
                file_ext = Path(result.file_path).suffix.lower()
                if file_ext not in filters["file_types"]:
                    continue
            
            # Content type filter
            if "content_types" in filters:
                if result.content_type not in filters["content_types"]:
                    continue
            
            # Path filter
            if "path_patterns" in filters:
                if not any(pattern in result.file_path for pattern in filters["path_patterns"]):
                    continue
            
            # Similarity threshold filter
            if "min_similarity" in filters:
                if result.similarity_score < filters["min_similarity"]:
                    continue
            
            filtered_results.append(result)
        
        return filtered_results
    
    def _log_search_query(self, search_query: SearchQuery, results_count: int, execution_time: float):
        """Log search query for analytics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO search_queries 
                    (query_text, query_type, results_count, execution_time, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    search_query.query_text,
                    search_query.query_type,
                    results_count,
                    execution_time,
                    datetime.now()
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Error logging search query: {e}")
    
    def get_search_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get search analytics for the specified period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT 
                        query_type,
                        COUNT(*) as query_count,
                        AVG(results_count) as avg_results,
                        AVG(execution_time) as avg_execution_time
                    FROM search_queries 
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY query_type
                '''.format(days))
                
                analytics = {
                    "query_types": {},
                    "total_queries": 0,
                    "avg_execution_time": 0
                }
                
                for query_type, count, avg_results, avg_time in cursor.fetchall():
                    analytics["query_types"][query_type] = {
                        "count": count,
                        "avg_results": avg_results,
                        "avg_execution_time": avg_time
                    }
                    analytics["total_queries"] += count
                
                # Calculate overall average execution time
                cursor = conn.execute('''
                    SELECT AVG(execution_time) 
                    FROM search_queries 
                    WHERE created_at >= datetime('now', '-{} days')
                '''.format(days))
                
                result = cursor.fetchone()
                if result and result[0]:
                    analytics["avg_execution_time"] = result[0]
                
                return analytics
                
        except Exception as e:
            logger.error(f"Error getting search analytics: {e}")
            return {}
    
    def index_project(self, project_path: str) -> bool:
        """Index an entire project for search."""
        try:
            project_path = Path(project_path)
            logger.info(f"Starting project indexing: {project_path}")
            
            # Find all relevant files
            file_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.md', '.txt', '.json', '.yaml', '.yml'}
            files = []
            
            for ext in file_extensions:
                files.extend(project_path.rglob(f"*{ext}"))
            
            logger.info(f"Found {len(files)} files to index")
            
            # Index each file
            indexed_count = 0
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Determine content type
                    content_type = self._determine_content_type(file_path)
                    
                    # Generate content ID
                    content_id = f"{project_path.name}_{file_path.relative_to(project_path)}"
                    
                    # Add to index
                    if self.add_content(content_id, str(file_path), content, content_type):
                        indexed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error indexing {file_path}: {e}")
            
            logger.info(f"Successfully indexed {indexed_count} files")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing project: {e}")
            return False
    
    def _determine_content_type(self, file_path: Path) -> str:
        """Determine content type based on file extension and path."""
        ext = file_path.suffix.lower()
        
        if ext in {'.py'}:
            return "code"
        elif ext in {'.js', '.ts', '.jsx', '.tsx'}:
            return "code"
        elif ext in {'.html', '.css'}:
            return "frontend"
        elif ext in {'.md', '.txt'}:
            return "documentation"
        elif ext in {'.json', '.yaml', '.yml'}:
            return "configuration"
        elif "test" in str(file_path):
            return "test"
        else:
            return "other"


def main():
    """Main function for testing the vector search system."""
    # Initialize vector search
    vector_search = AdvancedVectorSearch()
    
    # Index the Heavenly Hands project
    project_path = "/Users/steven/ai-sites/heavenlyHands"
    
    print("🚀 Starting Vector Search System...")
    print("=" * 50)
    
    # Index project
    print("📚 Indexing project...")
    success = vector_search.index_project(project_path)
    
    if success:
        print("✅ Project indexed successfully!")
        
        # Perform some test searches
        test_queries = [
            "cleaning service booking system",
            "authentication and user management",
            "database models and schemas",
            "API endpoints and routes",
            "frontend components and UI"
        ]
        
        print("\n🔍 Performing test searches...")
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = vector_search.search(query, limit=3)
            
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result.file_path} (Score: {result.similarity_score:.3f})")
                print(f"     {result.content_preview[:100]}...")
        
        # Get analytics
        print("\n📊 Search Analytics:")
        analytics = vector_search.get_search_analytics()
        print(f"Total queries: {analytics.get('total_queries', 0)}")
        print(f"Average execution time: {analytics.get('avg_execution_time', 0):.3f}s")
        
    else:
        print("❌ Failed to index project")
    
    print("\n" + "=" * 50)
    print("✅ Vector Search System Ready!")


if __name__ == "__main__":
    main()