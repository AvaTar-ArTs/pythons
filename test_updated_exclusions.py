#!/usr/bin/env python3
"""
Summary of test_updated_exclusions.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""


# Test script to verify that the scanner is using both file and directory exclusion patterns
import sys
import os

# Add the clean directory to the Python path
CLEAN_DIR = os.path.expanduser('~/clean')
if CLEAN_DIR not in sys.path:
    sys.path.insert(0, CLEAN_DIR)

print("Testing scanner exclusion patterns (updated)...")

try:
    # Import the exclusion patterns as they would be used in scanner.py
    from config import EXCLUDED_PATTERNS, EXCLUDED_DIRECTORIES
    print(f"✅ Successfully imported EXCLUDED_PATTERNS and EXCLUDED_DIRECTORIES from config.py")
    print(f"   File exclusion patterns: {len(EXCLUDED_PATTERNS)}")
    print(f"   Directory exclusion patterns: {len(EXCLUDED_DIRECTORIES)}")
    print(f"   Combined total: {len(EXCLUDED_PATTERNS) + len(EXCLUDED_DIRECTORIES)}")
    
    # Check a few key directory patterns to make sure they're comprehensive
    key_dir_patterns = ['.env.d/', '.secrets/', '.cursor/', '.claude/', '.gemini/', '.ollama/', 'backups/', 'archives/']
    found_dir_patterns = []
    
    for key in key_dir_patterns:
        if any(key.replace('/', '') in pat.lower() for pat in EXCLUDED_DIRECTORIES):
            found_dir_patterns.append(key)
    
    print(f"   Found key directory patterns: {found_dir_patterns}")
    
    # Now test importing in scanner.py style
    try:
        from scanner import ALL_EXCLUSION_PATTERNS
        print(f"✅ Scanner successfully imported combined exclusion patterns")
        print(f"   Scanner combined exclusion patterns count: {len(ALL_EXCLUSION_PATTERNS)}")
    except Exception as e:
        print(f"❌ Error importing combined exclusion patterns in scanner style: {e}")
        
except ImportError as e:
    print(f"❌ Could not import exclusion patterns from config.py: {e}")
    print("   This means the fallback patterns will be used instead.")

print("\nScanner exclusion functionality test completed.")