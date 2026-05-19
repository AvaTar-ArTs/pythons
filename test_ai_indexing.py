#!/usr/bin/env python3
"""
Test script for NocturneMemory AI

Demonstrates AI-enhanced content indexing with available APIs.
"""

import sys
from pathlib import Path

from nocturnememory_ai import NocturneMemoryAI


def test_ai_apis():
    """Test available AI APIs"""
    print("🧪 Testing NocturneMemory AI APIs")
    print("=" * 40)

    memory = NocturneMemoryAI()

    print("\n🤖 Available APIs:")
    for api, available in memory.available_apis.items():
        status = "✅ Available" if available else "❌ Unavailable"
        key_status = "✅ Key loaded" if memory.api_keys.get(api) else "❌ No key"
        print(f"  {api}: {status} | {key_status}")

    if not memory.available_apis:
        print("\n❌ No AI APIs available. Please check your ~/.env.d/ configuration.")
        return False

    return True


def test_sample_analysis():
    """Test AI analysis on sample content"""
    print("\n🧠 Testing AI Content Analysis")
    print("=" * 40)

    memory = NocturneMemoryAI()

    # Sample content for testing
    test_content = {
        "AI_Image_Prompts": """
        A majestic cyberpunk cityscape at night, neon lights reflecting off wet streets,
        flying cars zooming between towering skyscrapers, holographic advertisements
        floating in the air, a mysterious figure in a trench coat walking through
        the rain, in the style of Blade Runner and Ghost in the Shell.
        """,
        "Song_Lyrics": """
        [Verse 1]
        In the shadows where the lost souls play
        Heart beats like thunder in the pouring rain
        Dreams we chase fade into the grey
        Love's sweet poison running through our veins

        [Chorus]
        We dance in the darkness, we cry in the light
        Broken hearts mending in the dead of night
        Whispers of forever, echoes of goodbye
        In this endless storm, we learn to fly
        """,
    }

    for content_type, content in test_content.items():
        print(f"\n📄 Analyzing {content_type}:")
        print("-" * 30)

        # Test AI analysis
        analysis = memory.analyze_with_ai(content, content_type)

        if "error" in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
        else:
            print(f"✅ API: {analysis['api']} ({analysis['model']})")
            print(f"📊 Confidence: {analysis['confidence']:.2f}")
            print(f"💭 Analysis:\n{analysis['analysis'][:300]}...")


def test_directory_scan():
    """Test scanning a sample directory"""
    print("\n📁 Testing Directory AI Scan")
    print("=" * 40)

    memory = NocturneMemoryAI()

    # Try to scan docs directory first
    docs_dir = Path(__file__).parent / "docs"
    if docs_dir.exists():
        print(f"Scanning docs directory: {docs_dir}")
        memory.scan_directory_ai(str(docs_dir), recursive=False)
    else:
        print("No docs directory found to scan")

    # Show stats
    stats = memory.get_stats()
    print("\n📊 Scan Results:")
    print(f"Total content: {stats['total_content']}")
    print(f"AI analyses: {stats.get('ai_analyses', 0)}")

    if stats.get("by_category"):
        print("By category:")
        for category, count in stats["by_category"].items():
            print(f"  {category}: {count}")


def main():
    print("🎨 NocturneMemory AI - Integration Test")
    print("=" * 50)

    # Test 1: API availability
    if not test_ai_apis():
        sys.exit(1)

    # Test 2: Sample analysis
    test_sample_analysis()

    # Test 3: Directory scan
    test_directory_scan()

    print("\n🎉 AI Integration test complete!")
    print("\n💡 Usage examples:")
    print("  python nocturnememory_ai.py scan --path ~/Documents/Prompts")
    print("  python nocturnememory_ai.py analyze --path my_prompt.txt --api openai")
    print("  python nocturnememory_ai.py search --query 'cyberpunk city' --category AI_Image_Prompts")


if __name__ == "__main__":
    main()
