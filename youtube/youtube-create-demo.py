"""
Youtube Create Demo Collection

This module provides functionality for youtube create demo collection.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
ChromaDB Cloud Client Application
"""

from pathlib import Path
import chromadb

import os
from dotenv import load_dotenv

load_dotenv()

# ChromaDB Cloud Configuration (hardcoded for reliability)
# To use environment variables instead, set: CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE
API_KEY = os.getenv('CHROMADB_API_KEY')
TENANT = os.getenv('CHROMADB_TENANT')
DATABASE = os.getenv('CHROMADB_DATABASE')

# Initialize ChromaDB Cloud Client
client = chromadb.CloudClient(
    api_key=API_KEY,
    tenant=TENANT,
    database=DATABASE
)

def create_demo_collection():
    """Create a demo collection with sample documents"""
    collection_name = "demo_collection"

    # Get or create collection
    try:
        collection = client.get_or_create_collection(name=collection_name)
        logger.info(f"\n✅ Collection '{collection_name}' ready")

        # Add sample documents
        collection.add(
            documents=[
                "ChromaDB is a vector database for AI applications",
                "Python makes it easy to work with embeddings",
                "Vector search enables semantic similarity matching",
                "AI applications need efficient storage for embeddings"
            ],
            metadatas=[
                {"source": "intro", "topic": "chromadb"},
                {"source": "intro", "topic": "python"},
                {"source": "intro", "topic": "search"},
                {"source": "intro", "topic": "ai"}
            ],
            ids=["doc1", "doc2", "doc3", "doc4"]
        )
        logger.info(f"✅ Added 4 sample documents")

        # Query the collection
        results = collection.query(
            query_texts=["Tell me about vector databases"],
            n_results=2
        )

        logger.info(f"\n🔍 Query: 'Tell me about vector databases'")
        logger.info(f"Top results:")
        for i, doc in enumerate(results['documents'][0], 1):
            logger.info(f"  {i}. {doc}")

        return collection

    except Exception as e:
        logger.info(f"❌ Error: {e}")
        return None

def main():
    """Main application entry point"""
    logger.info("ChromaDB Cloud Client initialized successfully!")
    logger.info(f"Tenant: {TENANT}")
    logger.info(f"Database: {DATABASE}")

    # List collections
    try:
        collections = client.list_collections()
        logger.info(f"\n📚 Available collections: {len(collections)}")
        for collection in collections:
            logger.info(f"  - {collection.name}")
    except Exception as e:
        logger.info(f"Error listing collections: {e}")
        return

    # Ask user if they want to create a demo collection
    if len(collections) == 0:
        logger.info(Path("\n") + "="*60)
        response = input("No collections found. Create a demo collection? (y/n): ")
        if response.lower() == 'y':
            create_demo_collection()

            # List collections again
            collections = client.list_collections()
            logger.info(f"\n📚 Collections after demo: {len(collections)}")
            for collection in collections:
                logger.info(f"  - {collection.name}")

if __name__ == "__main__":
    main()
