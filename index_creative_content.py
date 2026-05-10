#!/usr/bin/env python3
"""
Index creative content for NocturneMemory

Scans key directories for:
- Image/Sora prompts (AI generation prompts)
- Lyrics and transcripts (song lyrics, audio transcripts)
- Analysis (music/metadata analysis)
- Originals (source files: PDF, JSON, MD, CSV, etc.)
"""

from pathlib import Path

from nocturnememory import NocturneMemory


def main():
    memory = NocturneMemory()

    print("🎨 NocturneMemory - Creative Content Indexing")
    print("=" * 50)

    # Index ALBUMS (lyrics, transcripts, analysis)
    albums_dir = Path(__file__).parent / "ALBUMS"
    if albums_dir.exists():
        print("📁 Indexing ALBUMS (lyrics, transcripts, analysis)...")
        memory.scan_directory(str(albums_dir))

    # Index docs (analysis, prompts)
    docs_dir = Path(__file__).parent / "docs"
    if docs_dir.exists():
        print("📁 Indexing docs (analysis, prompts)...")
        memory.scan_directory(str(docs_dir))

    # Index data (CSVs, JSON with lyrics/analysis)
    data_dir = Path(__file__).parent / "data"
    if data_dir.exists():
        print("📁 Indexing data (lyrics, analysis CSVs)...")
        memory.scan_directory(str(data_dir))

    # Index web content (HTML with prompts/analysis)
    web_dir = Path(__file__).parent / "web"
    if web_dir.exists():
        print("📁 Indexing web content (HTML with prompts/analysis)...")
        memory.scan_directory(str(web_dir))

    # Index home directory creative assets (limited scan)
    home_creative = Path.home()
    creative_dirs = [
        home_creative / "Documents" / "Prompts",
        home_creative / "Documents" / "Lyrics",
        home_creative / "Documents" / "Analysis",
        home_creative / "Desktop" / "Creative",
        home_creative / "Downloads" / "AI_Prompts",
    ]

    print("🏠 Scanning home directory for creative assets...")
    for creative_dir in creative_dirs:
        if creative_dir.exists():
            print(f"  📁 {creative_dir.name}")
            memory.scan_directory(str(creative_dir), recursive=False)  # Shallow scan

    # Show stats
    print("\n📊 Indexing Complete!")
    stats = memory.get_stats()
    print(f"Total content indexed: {stats['total_content']}")
    print(f"Search terms: {stats['search_terms']}")
    print()
    print("Content by category:")
    for category, count in stats.get("by_category", {}).items():
        print(f"  {category}: {count}")

    print(f"\n💾 Database: {memory.db_path}")

    # Example searches
    print("\n🔍 Example searches:")
    print("  python nocturnememory.py search --query 'cyberpunk city'")
    print("  python nocturnememory.py search --query 'love song lyrics' --category 'Song_Lyrics'")
    print("  python nocturnememory.py search --query 'tempo 140' --category 'Music_Analysis'")


if __name__ == "__main__":
    main()
