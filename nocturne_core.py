#!/usr/bin/env python3
"""
NocturneCore - Streamlined AI Content Intelligence

A focused, lightweight approach to musical content analysis.
Combines AI insights with practical content management.
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load environment variables
env_dir = Path.home() / ".env.d"
for env_file in ["llm-apis.env", "MASTER_CONSOLIDATED.env"]:
    env_path = env_dir / env_file
    if env_path.exists():
        load_dotenv(env_path)


class NocturneCore:
    """Streamlined AI-powered content intelligence"""

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.data_dir = self.base_dir / "nocturne_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "nocturne_core.db"
        self.init_database()

    def init_database(self):
        """Initialize streamlined database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content (
                id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                type TEXT,
                category TEXT,
                ai_insights TEXT,
                metadata TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS insights (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                insight_type TEXT,
                insight_data TEXT,
                confidence REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def quick_scan(self, target_path: str) -> dict[str, Any]:
        """Quick, focused content scan"""
        print("🔍 NocturneCore - Quick Content Scan")
        print("=" * 40)

        results = {
            "target": target_path,
            "scanned_at": datetime.now().isoformat(),
            "content_found": [],
            "insights_generated": 0,
            "categories": {},
        }

        path_obj = Path(target_path).expanduser().resolve()

        for root, dirs, files in os.walk(path_obj):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                file_path.suffix.lower()

                # Quick content assessment
                content_type, category, insights = self.assess_content(file_path)

                if content_type:
                    content_item = {
                        "path": str(file_path),
                        "name": file,
                        "type": content_type,
                        "category": category,
                        "insights": insights,
                        "size": file_path.stat().st_size,
                    }

                    results["content_found"].append(content_item)
                    results["categories"][category] = results["categories"].get(category, 0) + 1

                    # Store in database
                    self.store_content(content_item)
                    results["insights_generated"] += len(insights)

        results["total_content"] = len(results["content_found"])
        self.save_results(results)

        print(f"✅ Scanned {results['total_content']} items")
        print(f"📊 Generated {results['insights_generated']} insights")
        print(f"🏷️  Categories: {', '.join(results['categories'].keys())}")

        return results

    def assess_content(self, file_path: Path) -> tuple[str, str, list[str]]:
        """Quick content assessment"""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()

        insights = []

        # Musical content detection
        if ext in [".txt", ".md", ".html"]:
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(2000).lower()

                # Lyrics detection
                if any(word in content for word in ["verse", "chorus", "lyrics", "melody"]):
                    insights.append("Contains lyrical content")
                    if any(word in content for word in ["night", "moon", "stars", "dream"]):
                        insights.append("Nocturne themes detected")
                        return "lyrics", "nocturne_lyrics", insights
                    return "lyrics", "song_lyrics", insights

                # Musical analysis detection
                if any(word in content for word in ["harmony", "chord", "tempo", "key", "melody"]):
                    insights.append("Musical theory content")
                    return "analysis", "musical_analysis", insights

                # AI prompts detection
                if any(word in content for word in ["prompt", "generate", "create", "render"]):
                    insights.append("AI generation prompts")
                    return "prompts", "ai_prompts", insights

            except OSError:
                pass

        # Audio files
        elif ext in [".mp3", ".wav", ".flac", ".midi"]:
            insights.append("Audio recording")
            return "audio", "music_recording", insights

        # Default
        if any(word in name for word in ["music", "song", "audio", "nocturne"]):
            insights.append("Music-related content")
            return "musical", "music_content", insights

        return "", "other", []

    def generate_ai_insights(self, content_list: list[dict]) -> dict[str, Any]:
        """Generate AI-powered insights for content"""
        print("🤖 Generating AI Insights...")

        insights = {
            "generated_at": datetime.now().isoformat(),
            "content_analyzed": len(content_list),
            "ai_insights": [],
            "thematic_analysis": {},
            "quality_assessment": {},
        }

        # Basic thematic analysis
        nocturne_content = [c for c in content_list if c.get("category") == "nocturne_lyrics"]
        musical_content = [c for c in content_list if "music" in c.get("category", "")]

        insights["thematic_analysis"] = {
            "nocturne_focused": len(nocturne_content),
            "musical_content": len(musical_content),
            "total_analyzed": len(content_list),
        }

        # Quality assessment
        high_quality = [c for c in content_list if len(c.get("insights", [])) > 1]
        insights["quality_assessment"] = {
            "high_quality_items": len(high_quality),
            "quality_score": len(high_quality) / max(len(content_list), 1),
        }

        # Store insights
        self.store_insights(insights)

        print(f"✅ Generated insights for {len(content_list)} content items")
        return insights

    def store_content(self, content: dict[str, Any]):
        """Store content in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        content_id = hashlib.md5(content["path"].encode()).hexdigest()[:16]

        cursor.execute(
            """
            INSERT OR REPLACE INTO content
            (id, path, name, type, category, ai_insights, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content["path"],
                content["name"],
                content.get("type", ""),
                content.get("category", ""),
                json.dumps(content.get("insights", [])),
                json.dumps({"size": content.get("size", 0)}),
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def store_insights(self, insights: dict[str, Any]):
        """Store insights in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        insight_id = hashlib.md5(str(insights).encode()).hexdigest()[:16]

        cursor.execute(
            """
            INSERT OR REPLACE INTO insights
            (id, content_id, insight_type, insight_data, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                insight_id,
                "global",  # Global insights
                "thematic_analysis",
                json.dumps(insights),
                0.8,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def save_results(self, results: dict[str, Any]):
        """Save scan results"""
        output_file = self.data_dir / "nocturne_scan_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"💾 Results saved to: {output_file}")

    def query_content(self, category: str = None, limit: int = 10) -> list[dict]:
        """Query content from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute(
                """
                SELECT path, name, type, category, ai_insights
                FROM content
                WHERE category = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (category, limit),
            )
        else:
            cursor.execute(
                """
                SELECT path, name, type, category, ai_insights
                FROM content
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "path": row[0],
                    "name": row[1],
                    "type": row[2],
                    "category": row[3],
                    "insights": json.loads(row[4]) if row[4] else [],
                }
            )

        conn.close()
        return results

    def generate_summary(self) -> dict[str, Any]:
        """Generate content summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        summary = {
            "generated_at": datetime.now().isoformat(),
            "total_content": 0,
            "categories": {},
            "types": {},
            "recent_activity": [],
        }

        # Total content
        cursor.execute("SELECT COUNT(*) FROM content")
        summary["total_content"] = cursor.fetchone()[0]

        # Categories breakdown
        cursor.execute("SELECT category, COUNT(*) FROM content GROUP BY category")
        summary["categories"] = dict(cursor.fetchall())

        # Types breakdown
        cursor.execute("SELECT type, COUNT(*) FROM content GROUP BY type")
        summary["types"] = dict(cursor.fetchall())

        # Recent content
        cursor.execute(
            """
            SELECT name, category, created_at
            FROM content
            ORDER BY created_at DESC
            LIMIT 5
        """
        )
        summary["recent_activity"] = [
            {"name": row[0], "category": row[1], "created": row[2]} for row in cursor.fetchall()
        ]

        conn.close()

        # Save summary
        summary_file = self.data_dir / "nocturne_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        return summary


def main():
    parser = argparse.ArgumentParser(description="NocturneCore - Streamlined AI Content Intelligence")
    parser.add_argument(
        "command",
        choices=["scan", "insights", "query", "summary"],
        help="Command to run",
    )
    parser.add_argument("--target", help="Target directory for scanning")
    parser.add_argument("--category", help="Category to query")
    parser.add_argument("--limit", type=int, default=10, help="Limit for queries")

    args = parser.parse_args()

    core = NocturneCore()

    if args.command == "scan":
        if not args.target:
            print("❌ --target required for scan command")
            sys.exit(1)

        results = core.quick_scan(args.target)
        print(f"🎵 NocturneCore scan complete: {results['total_content']} items found")

    elif args.command == "insights":
        # Generate insights for existing content
        content = core.query_content(limit=100)  # Get recent content
        insights = core.generate_ai_insights(content)
        print(f"🤖 Generated insights for {insights['content_analyzed']} items")

    elif args.command == "query":
        results = core.query_content(args.category, args.limit)
        print(f"📊 Found {len(results)} items" + (f" in category '{args.category}'" if args.category else ""))

        for item in results:
            print(f"  • {item['name']} ({item['category']})")
            if item["insights"]:
                print(f"    Insights: {', '.join(item['insights'])}")

    elif args.command == "summary":
        summary = core.generate_summary()
        print("🌙 NocturneCore Summary:")
        print(f"   Total content: {summary['total_content']}")
        print(f"   Categories: {len(summary['categories'])}")
        print(f"   Content types: {len(summary['types'])}")
        print("\n🏷️  Categories:")
        for cat, count in summary["categories"].items():
            print(f"   {cat}: {count}")
        print("\n📈 Recent Activity:")
        for item in summary["recent_activity"][:3]:
            print(f"   {item['name']} ({item['category']})")


if __name__ == "__main__":
    main()
