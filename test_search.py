#!/usr/bin/env python3
# home-search-index/test_search.py

"""
Test script to verify the search functionality of the home directory indexing system
"""

import sys
import os
from pathlib import Path

# Add the home-search-index directory to the Python path
sys.path.insert(0, '/Users/steven/home-search-index')

def test_search_functionality():
    """Test the search functionality with sample queries"""
    try:
        from search_home_directory import search_documents
        
        print("Testing search functionality...")
        
        # Test 1: Basic search
        print("\n=== Test 1: Basic search for 'AI automation' ===")
        results = search_documents("AI automation", limit=5)
        print(f"Found {len(results)} results")
        for i, result in enumerate(results[:3]):  # Show first 3 results
            print(f"{i+1}. {result['title']} - {result['path']} (Score: {result['score']:.2f})")
            print(f"   Category: {result['category']}, Business Value: {result['business_value']:.2f}")
            if result['semantic_tags']:
                print(f"   Semantic Tags: {', '.join(result['semantic_tags'])}")
            if result['macos_tags']:
                print(f"   macOS Tags: {', '.join(result['macos_tags'])}")
            print()
        
        # Test 2: Category filter
        print("\n=== Test 2: Search with category filter ===")
        results = search_documents("strategy", limit=5, category_filter="Strategic_Planning")
        print(f"Found {len(results)} strategic planning documents")
        for i, result in enumerate(results):
            print(f"{i+1}. {result['title']} - {result['path']}")
        
        # Test 3: Business value filter
        print("\n=== Test 3: Search with business value filter ===")
        results = search_documents("business", limit=5, business_value_min=5.0)
        print(f"Found {len(results)} high-value business documents")
        for i, result in enumerate(results):
            print(f"{i+1}. {result['title']} - Business Value: {result['business_value']:.2f}")
        
        # Test 4: macOS tag filter
        print("\n=== Test 4: Search with macOS tag filter ===")
        results = search_documents("important", limit=5, macos_tag_filter="Important")
        print(f"Found {len(results)} documents with 'Important' macOS tag")
        for i, result in enumerate(results):
            print(f"{i+1}. {result['title']} - macOS Tags: {', '.join(result['macos_tags'])}")
        
        print("\n=== Search functionality tests completed successfully! ===")
        
    except ImportError as e:
        print(f"Error importing search module: {e}")
        print("Make sure the indexing process has completed and the modules are available.")
    except Exception as e:
        print(f"Error during search test: {e}")

def check_index_status():
    """Check the status of the index"""
    index_path = Path('/Users/steven/home-search-index/index')
    
    if index_path.exists():
        print("Index directory exists!")
        
        # Count files in index directory
        file_count = len(list(index_path.glob('*')))
        print(f"Number of files in index directory: {file_count}")
        
        # Check for index files
        toc_files = list(index_path.glob('*.toc'))
        print(f"TOC files found: {len(toc_files)}")
        
        # Check for lock files (indicates indexing in progress)
        lock_files = list(index_path.glob('*LOCK*'))
        if lock_files:
            print(f"Lock files found: {len(lock_files)} - Indexing may still be in progress")
        else:
            print("No lock files found - Indexing appears to be complete")
    else:
        print("Index directory does not exist yet. Indexing may still be in progress.")

def main():
    print("Home Directory Search System - Test Suite")
    print("=" * 50)
    
    # Check index status
    check_index_status()
    
    # Wait a moment for any ongoing indexing to settle
    import time
    time.sleep(2)
    
    # Test search functionality
    test_search_functionality()

if __name__ == "__main__":
    main()