#!/usr/bin/env python3
# home-search-index/search_home_directory.py

"""
Home Directory Search System
This script provides search functionality for the indexed home directory
with enhanced filtering and aggregation capabilities.
"""

import os
import sys
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import sorting
from pathlib import Path
import json
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger('home_directory_searcher')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('search_home_directory.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

def search_documents(query_string, limit=10, category_filter=None, business_value_min=None, macos_tag_filter=None):
    """Search documents with enhanced filtering capabilities"""
    
    index_dir = Path('/Users/steven/home-search-index/index')
    
    if not index_dir.exists():
        print(f"Index not found at {index_dir}. Please run index_home_directory.py first.")
        return []
    
    try:
        # Open the index
        ix = open_dir(str(index_dir))
        
        # Create query parser for multiple fields
        parser = MultifieldParser(['title', 'content', 'semantic_tags', 'macos_tags', 'category'], schema=ix.schema)
        query = parser.parse(query_string)
        
        # Search with filters
        with ix.searcher() as searcher:
            # Build filter if needed
            filter_list = []
            if category_filter:
                from whoosh import query as whoosh_query
                filter_list.append(whoosh_query.Term('category', category_filter))
            
            if business_value_min is not None:
                from whoosh import query as whoosh_query
                filter_list.append(whoosh_query.NumericRange('business_value', start=float(business_value_min)))
            
            if macos_tag_filter:
                from whoosh import query as whoosh_query
                filter_list.append(whoosh_query.Term('macos_tags', macos_tag_filter))
            
            # Apply filters if any
            if filter_list:
                search_filter = filter_list[0]
                for f in filter_list[1:]:
                    search_filter &= f
                results = searcher.search(query, limit=limit, filter=search_filter)
            else:
                results = searcher.search(query, limit=limit)
            
            # Process results
            search_results = []
            for hit in results:
                result = {
                    'title': hit['title'],
                    'path': hit['path'],
                    'filename': hit['filename'],
                    'category': hit['category'],
                    'file_type': hit['file_type'],
                    'size_bytes': int(hit['size_bytes']) if hit.get('size_bytes') else 0,
                    'business_value': float(hit['business_value']) if hit.get('business_value') else 0.0,
                    'complexity': hit['complexity'] if hit.get('complexity') else 'unknown',
                    'semantic_tags': hit['semantic_tags'].split(',') if hit.get('semantic_tags') else [],
                    'macos_tags': hit['macos_tags'].split(',') if hit.get('macos_tags') else [],
                    'score': hit.score,
                    'content_snippet': hit.highlights('content') or (hit.get('content', '')[:200] + '...' if hit.get('content') else '')
                }
                search_results.append(result)
            
            return search_results
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return []

def aggregate_by_category():
    """Get document counts by category"""
    
    index_dir = Path('/Users/steven/home-search-index/index')
    
    if not index_dir.exists():
        print(f"Index not found at {index_dir}. Please run index_home_directory.py first.")
        return {}
    
    try:
        ix = open_dir(str(index_dir))
        
        with ix.searcher() as searcher:
            # Get all results to count categories
            all_results = searcher.search(ix.parser.parse("*"), limit=None)
            category_counts = {}
            for hit in all_results:
                cat = hit.get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            return category_counts
    
    except Exception as e:
        logger.error(f"Aggregation error: {e}")
        return {}

def aggregate_by_macos_tag():
    """Get document counts by macOS tag"""
    
    index_dir = Path('/Users/steven/home-search-index/index')
    
    if not index_dir.exists():
        print(f"Index not found at {index_dir}. Please run index_home_directory.py first.")
        return {}
    
    try:
        ix = open_dir(str(index_dir))
        
        with ix.searcher() as searcher:
            # Get all results to count macOS tags
            all_results = searcher.search(ix.parser.parse("*"), limit=None)
            tag_counts = {}
            for hit in all_results:
                macos_tags_str = hit.get('macos_tags', '')
                if macos_tags_str:
                    tags = macos_tags_str.split(',')
                    for tag in tags:
                        tag = tag.strip()
                        if tag:
                            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            return tag_counts
    
    except Exception as e:
        logger.error(f"Tag aggregation error: {e}")
        return {}

def print_search_results(results):
    """Print search results in a formatted way with tag information"""
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} results:\n")
    print(f"{'Score':<8} {'Title':<30} {'Category':<20} {'Path'}")
    print("-" * 100)
    
    for result in results:
        score = f"{result['score']:.2f}"
        title = result['title'][:29] + "..." if len(result['title']) > 29 else result['title']
        category = result['category']
        path = result['path']
        
        print(f"{score:<8} {title:<30} {category:<20} {path}")
        
        if result['content_snippet']:
            print(f"    Snippet: {result['content_snippet']}")
        
        # Show both semantic and macOS tags
        semantic_tags = ', '.join(result['semantic_tags'])
        macos_tags = ', '.join(result['macos_tags'])
        
        if semantic_tags:
            print(f"    Semantic Tags: {semantic_tags}")
        if macos_tags:
            print(f"    macOS Tags: {macos_tags}")
        
        print(f"    Business Value: {result['business_value']:.2f}")
        print(f"    Complexity: {result['complexity']}")
        print("-" * 100)

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_home_directory.py <query> [limit] [category_filter] [macos_tag_filter]")
        print("Example: python search_home_directory.py 'AI automation' 10")
        print("         python search_home_directory.py 'business strategy' 10 --category Strategic_Planning")
        print("         python search_home_directory.py 'important' 10 --macos_tag '⭐ Important'")
        return
    
    query_string = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    category_filter = sys.argv[3] if len(sys.argv) > 3 else None
    macos_tag_filter = sys.argv[4] if len(sys.argv) > 4 else None
    
    print(f"Searching for: '{query_string}' (limit: {limit})")
    if category_filter:
        print(f"Category filter: {category_filter}")
    if macos_tag_filter:
        print(f"macOS tag filter: {macos_tag_filter}")
    
    results = search_documents(query_string, limit=limit, category_filter=category_filter, macos_tag_filter=macos_tag_filter)
    print_search_results(results)
    
    # Also show category breakdown
    print("\nCategory breakdown:")
    categories = aggregate_by_category()
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count} documents")
    
    # Show macOS tag breakdown
    print("\nmacOS Tag breakdown:")
    macos_tags = aggregate_by_macos_tag()
    for tag, count in sorted(macos_tags.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {tag}: {count} documents")

if __name__ == "__main__":
    # If run without arguments, provide interactive mode
    if len(sys.argv) == 1:
        print("Interactive Home Directory Search with Tag Integration")
        print("=====================================================")
        
        while True:
            try:
                query = input("\nEnter search query (or 'quit' to exit): ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not query:
                    continue
                
                print("Optional filters:")
                category_filter = input("  Category filter (or Enter to skip): ").strip()
                if not category_filter:
                    category_filter = None
                
                macos_tag_filter = input("  macOS tag filter (or Enter to skip): ").strip()
                if not macos_tag_filter:
                    macos_tag_filter = None
                
                results = search_documents(query, limit=10, category_filter=category_filter, macos_tag_filter=macos_tag_filter)
                print_search_results(results)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        main()