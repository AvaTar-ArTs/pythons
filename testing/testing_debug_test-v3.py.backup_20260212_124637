#!/usr/bin/env python3
"""Quick test of V3 renamer functionality"""

from smart_content_renamer_v3 import CodeAnalyzer, NameGenerator
from pathlib import Path

# Test files
test_files = [
    "/Users/steven/Documents/pythons/smart_content_renamer_v2.py",
    "/Users/steven/Documents/pythons/adaptive-content-awareness.py",
]

print("?? Testing V3 Analysis Engine\n")
print("="*80)

for filepath in test_files:
    path = Path(filepath)
    if not path.exists():
        continue
    
    print(f"\n?? File: {path.name}")
    print("-" * 80)
    
    # Analyze
    analysis = CodeAnalyzer.analyze_python_file(path)
    
    print(f"Purpose: {analysis['purpose']}")
    print(f"Keywords: {', '.join(analysis['keywords'][:3])}")
    print(f"Patterns: {', '.join(analysis['patterns'])}")
    print(f"Functions: {len(analysis['functions'])} detected")
    print(f"Classes: {len(analysis['classes'])} detected")
    print(f"Quality: {analysis['quality_score']:.2f}")
    
    # Generate name
    new_name, confidence = NameGenerator.generate_semantic_name(analysis, '.py')
    print(f"\n? Suggested: {new_name} (confidence: {confidence:.2f})")

print("\n" + "="*80)
print("? Test complete!")
