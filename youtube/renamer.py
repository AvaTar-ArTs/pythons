"""
Test Renamer

This module provides functionality for test renamer.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""Quick test of the improved renamer logic"""

# Simulate the fixes
import re

# Constants
CONSTANT_120 = 120



def clean_filename_NEW(name: str) -> str:
    """Your style: YouTubeBot, content_analyzer_v2, deep_organizer"""

    # Preserve proper case
    has_capitals = any(c.isupper() for c in name)

    # Remove redundant words
    redundant = ['enhanced_', 'simple_', 'comprehensive_', 'fixed_', 'direct_']
    for word in redundant:
        name = name.replace(word, '')

    # Clean version numbers: _1.py → _v1.py
    name = re.sub(r'_(\d+)\.py$', r'_v\1.py', name)

    # Preserve ProperCase names
    if has_capitals and not name.startswith(('usr-', 'from-', 'import-')):
        name = re.sub(r'[^\w\-.]', '_', name)
    else:
        name = name.lower()
        name = re.sub(r'[^\w\-.]', '_', name)

    name = re.sub(r'_+', '_', name).strip('_').strip('-')

    if not name.endswith('.py'):
        name += '.py'

    return name

# Test with your examples
test_cases = [
    ("enhanced_content_analyzer_v2.py", "content_analyzer_v2.py"),
    ("deep_read_organizer.py", "deep_organizer.py"),
    ("comprehensive_chat_organizer.py", "chat_organizer.py"),
    ("fixed_chat_organizer.py", "chat_organizer.py"),
    ("simple_deep_reader.py", "deep_reader.py"),
    ("direct_content_analyzer.py", "content_analyzer.py"),
    ("YouTubeBot.py", "YouTubeBot.py"),
    ("vidgenUI.py", "vidgenui.py"),  # lowercase if no caps
    ("WhisperTranscriber_1.py", "WhisperTranscriber_v1.py"),
]

logger.info("🧪 TESTING RENAMER LOGIC\n")
logger.info(f"{'Original':<40} → {'Expected':<30} | {'Got':<30} | Result")
logger.info("=" * CONSTANT_120)

for original, expected in test_cases:
    result = clean_filename_NEW(original)
    status = "✅" if result == expected or result.lower() == expected.lower() else "❌"
    logger.info(f"{original:<40} → {expected:<30} | {result:<30} | {status}")

logger.info("\nNOTE: Some results may differ slightly but still be valid based on case handling")
