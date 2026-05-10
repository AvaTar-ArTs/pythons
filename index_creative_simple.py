#!/usr/bin/env python3
"""
Simple sequential indexing for NocturneMemory

Indexes key creative content directories one by one.
"""

import os
from pathlib import Path

from nocturnememory import NocturneMemory


def index_directory(memory: NocturneMemory, path: Path, description: str):
    """Index a single directory"""
    if not path.exists():
        print(f"⚠️  {description}: {path} not found")
        return 0

    print(f"📁 {description}: {path}")
    try:
        # Get all relevant files first
        files_to_index = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith("."):
                    continue
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # Check if extension matches any category
                for cat_config in memory.CREATIVE_CATEGORIES.values():
                    if ext in cat_config.get("file_extensions", []):
                        files_to_index.append(file_path)
                        break

        # Index files sequentially
        indexed = 0
        for file_path in files_to_index:
            try:
                # Quick check for categories
                ext = file_path.suffix.lower()
                categories = []
                for cat_name, cat_config in memory.CREATIVE_CATEGORIES.items():
                    if ext in cat_config.get("file_extensions", []):
                        categories.append((cat_name, cat_config))

                if categories and memory.index_file(file_path, categories):
                    indexed += 1

            except Exception as e:
                print(f"  ❌ Error indexing {file_path.name}: {e}")
                continue

        print(f"  ✅ Indexed {indexed} files")
        return indexed

    except Exception as e:
        print(f"  ❌ Error scanning {path}: {e}")
        return 0


def main():
    memory = NocturneMemory()

    print("🎨 NocturneMemory - Creative Content Indexing")
    print("=" * 50)

    total_indexed = 0

    # Index ALBUMS (lyrics, transcripts, analysis)
    albums_dir = Path(__file__).parent / "ALBUMS"
    total_indexed += index_directory(memory, albums_dir, "ALBUMS (lyrics/transcripts/analysis)")

    # Index docs
    docs_dir = Path(__file__).parent / "docs"
    total_indexed += index_directory(memory, docs_dir, "docs (analysis/prompts)")

    # Index data
    data_dir = Path(__file__).parent / "data"
    total_indexed += index_directory(memory, data_dir, "data (lyrics/analysis CSVs)")

    # Index web
    web_dir = Path(__file__).parent / "web"
    total_indexed += index_directory(memory, web_dir, "web (HTML prompts/analysis)")

    # Show final stats
    print(f"\n🎉 Total indexed: {total_indexed}")

    stats = memory.get_stats()
    print(f"Database: {stats['total_content']} content items")
    print(f"Search terms: {stats['search_terms']}")

    if stats.get("by_category"):
        print("\nBy category:")
        for category, count in stats["by_category"].items():
            print(f"  {category}: {count}")

    print(f"\n💾 Database location: {memory.db_path}")

    # Test search
    print("\n🔍 Testing search...")
    test_queries = ["lyrics", "prompt", "analysis"]
    for query in test_queries:
        results = memory.search(query, limit=3)
        print(f"  '{query}': {len(results)} results")


if __name__ == "__main__":
    main()
