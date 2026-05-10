#!/usr/bin/env python3
"""
Demo Working Systems - Showcase Functional Nocturne AI Capabilities

Demonstrates the systems that are actually working and their capabilities.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def demo_basic_ai():
    """Demo the basic NocturneMemory AI system"""
    print("🎯 NocturneMemory AI - Basic Multi-API System")
    print("=" * 50)

    try:
        # Import and run basic system
        sys.path.insert(0, ".")
        from nocturnememory_ai import NocturneMemoryAI

        memory = NocturneMemoryAI()

        # Show available APIs
        available = [api for api, status in memory.available_apis.items() if status]
        print(f"✅ APIs Available: {', '.join(available)}")

        # Test AI analysis on existing content
        if os.path.exists("test_lyrics.txt"):
            print("📝 Analyzing test lyrics with AI...")

            # Read content
            with open("test_lyrics.txt") as f:
                content = f.read()

            # Test analysis with first available API
            if available:
                api_choice = available[0]
                analysis = memory.analyze_with_ai(content, "Song_Lyrics", api_choice)

                if "error" not in analysis:
                    print("✅ AI Analysis Successful:")
                    print(f"   API: {analysis['api']}")
                    print(f"   Model: {analysis['model']}")
                    print(f"   Confidence: {analysis['confidence']:.2f}")
                    print("   Analysis Preview: " + analysis["analysis"][:200] + "...")
                else:
                    print(f"❌ Analysis failed: {analysis['error']}")
            else:
                print("❌ No APIs available for analysis")
        else:
            print("⚠️  Test content not found")

        # Show current stats
        stats = memory.get_stats()
        print("\n📊 Current Stats:")
        print(f"   Content indexed: {stats.get('total_content', 0)}")
        print(f"   AI analyses: {stats.get('ai_analyses', 0)}")
        print(f"   Search terms: {stats.get('search_terms', 0)}")

        return True

    except Exception as e:
        print(f"❌ Basic AI system failed: {e}")
        return False


def demo_ecosystem_discovery():
    """Demo ecosystem tool discovery"""
    print("\n🔧 NocturneNexus Enhanced - Ecosystem Discovery")
    print("=" * 50)

    try:
        # Import enhanced system
        from nocturne_nexus_enhanced import NocturneNexusEnhanced

        system = NocturneNexusEnhanced()

        print(f"✅ Discovered {len(system.ecosystem_tools)} ecosystem tools:")

        # Show tool categories
        categories = {}
        for tool_name, tool_path in system.ecosystem_tools.items():
            category = tool_name.split("_")[0] if "_" in tool_name else "other"
            categories[category] = categories.get(category, 0) + 1

        for category, count in categories.items():
            print(f"   • {category}: {count} tools")

        # Show first few tools
        print("\n🛠️  Sample Tools:")
        for i, (name, path) in enumerate(list(system.ecosystem_tools.items())[:3]):
            print(f"   {i + 1}. {name}: {path.name}")

        return True

    except Exception as e:
        print(f"❌ Ecosystem discovery failed: {e}")
        return False


def demo_musical_intelligence():
    """Demo NocturneMelodies musical analysis"""
    print("\n🎵 NocturneMelodies - Musical Intelligence")
    print("=" * 50)

    try:
        from nocturne_melodies import NocturneMelodies

        # Check if we have demo content
        demo_dir = Path("demo_content")
        if demo_dir.exists():
            print("🎼 Analyzing demo musical content...")

            system = NocturneMelodies()

            # Run analysis on demo content
            results = system.analyze_musical_content(str(demo_dir))

            print(f"✅ Analyzed {results['total_content_analyzed']} musical items")

            # Show key insights
            if results.get("nocturne_themes_identified"):
                themes = results["nocturne_themes_identified"][0]
                print(f"🌙 Nocturne Score: {themes.get('overall_nocturne_score', 0):.2f}")
                print("   Detected themes:")
                for theme in themes.get("nocturne_themes", []):
                    print(f"   • {theme['theme']} (intensity: {theme['intensity']:.2f})")

            if results.get("semantic_understanding", {}).get("core_concepts"):
                print(f"🧠 Core concepts identified: {len(results['semantic_understanding']['core_concepts'])}")

            # Generate report
            system.generate_nocturne_report()
            print("📊 Intelligence report generated")
        else:
            print("⚠️  Demo content not found - creating sample...")

            # Create sample content
            demo_dir.mkdir(exist_ok=True)
            sample_content = """[Verse 1]
In the velvet night where shadows softly fall
Moonlight whispers secrets to the ancient hall
Dreams take flight on wings of lunar light
Nocturne melodies fill the endless night

[Chorus]
Serene and beautiful, beyond compare
Stars compose symphonies in the midnight air
Peaceful contemplation in this sacred space
Nocturne embraces with its gentle grace"""

            with open(demo_dir / "sample_nocturne.txt", "w") as f:
                f.write(sample_content)

            print("✅ Sample nocturne content created")

        return True

    except Exception as e:
        print(f"❌ Musical intelligence demo failed: {e}")
        return False


def demo_content_search():
    """Demo content search capabilities"""
    print("\n🔍 Content Search & Discovery")
    print("=" * 50)

    try:
        sys.path.insert(0, ".")
        from nocturnememory_ai import NocturneMemoryAI

        memory = NocturneMemoryAI()

        # Test searches
        test_queries = ["lyrics", "nocturne", "AI", "music"]

        print("🧪 Testing search queries:")
        for query in test_queries:
            results = memory.search(query, limit=3)
            print(f"   '{query}': {len(results)} results")

            if results:
                print(f"      • {results[0]['file_name']} ({results[0]['category']})")

        # Show categories
        stats = memory.get_stats()
        if stats.get("categories"):
            print("\n📂 Content Categories:")
            for category, count in stats["categories"].items():
                print(f"   • {category}: {count} items")

        return True

    except Exception as e:
        print(f"❌ Content search demo failed: {e}")
        return False


def run_capability_showcase():
    """Run a showcase of all working capabilities"""
    print("🎪 Nocturne AI Systems - Working Capabilities Showcase")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    capabilities = [
        ("Basic AI Analysis", demo_basic_ai),
        ("Ecosystem Discovery", demo_ecosystem_discovery),
        ("Musical Intelligence", demo_musical_intelligence),
        ("Content Search", demo_content_search),
    ]

    results = {}
    for name, demo_func in capabilities:
        print(f"🎯 Testing: {name}")
        print("-" * 40)
        success = demo_func()
        results[name] = success
        print()

    # Generate summary
    print("🎯 CAPABILITY SHOWCASE SUMMARY")
    print("=" * 70)

    working = sum(1 for success in results.values() if success)
    total = len(results)

    print(f"📊 Capabilities Tested: {total}")
    print(f"✅ Working: {working}")
    print(f"❌ Not Working: {total - working}")
    if total > 0:
        print(f"   Success rate: {working / total * 100:.1f}%")

    print("\n🔍 Capability Status:")
    for name, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"   {status}: {name}")

    print(f"\n🏆 Overall Status: {'🎉 MOSTLY WORKING' if working >= total * 0.75 else '⚠️ NEEDS ATTENTION'}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Save results
    summary = {
        "showcase_completed": datetime.now().isoformat(),
        "capabilities_tested": results,
        "success_rate": working / total,
        "working_capabilities": working,
        "total_capabilities": total,
    }

    with open("capability_showcase_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n💾 Results saved to: capability_showcase_results.json")


if __name__ == "__main__":
    # Change to the correct directory
    os.chdir("/Users/steven/Music/nocTurneMeLoDieS")

    run_capability_showcase()
