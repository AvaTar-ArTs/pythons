#!/usr/bin/env python3
"""
NocturneMelodies - AI-Powered Musical Content Intelligence

Specialized evolution of NocturneMemory for musical content, melodies,
and creative context analysis. Focuses on nocturne themes, atmospheric music,
and deep creative intelligence.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
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


class NocturneMelodies:
    """AI-powered musical content intelligence system"""

    # Nocturne-specific musical categories
    NOCTURNE_CATEGORIES = {
        "Nocturne_Compositions": {
            "keywords": {
                "nocturne": 10,
                "night": 8,
                "moonlight": 9,
                "twilight": 8,
                "dusk": 7,
                "midnight": 9,
                "stars": 7,
                "dreams": 8,
                "serenade": 9,
                "lullaby": 8,
                "atmospheric": 7,
                "ethereal": 8,
                "introspective": 7,
                "melancholy": 6,
            },
            "themes": ["night", "dreams", "moon", "stars", "serenity", "reflection"],
            "moods": ["calm", "introspective", "dreamy", "peaceful", "melancholic"],
        },
        "Melodic_Content": {
            "keywords": {
                "melody": 10,
                "melodies": 10,
                "tune": 8,
                "harmony": 9,
                "chord": 7,
                "progression": 8,
                "rhythm": 7,
                "tempo": 6,
                "key": 6,
                "scale": 7,
            },
            "elements": ["melody", "harmony", "rhythm", "structure", "arrangement"],
        },
        "Lyric_Poetry": {
            "keywords": {
                "lyrics": 10,
                "verse": 8,
                "chorus": 9,
                "poetry": 8,
                "words": 6,
                "rhyme": 7,
                "metaphor": 8,
                "imagery": 9,
                "emotion": 8,
                "story": 7,
            },
            "styles": ["poetic", "narrative", "emotional", "metaphorical", "lyrical"],
        },
        "Musical_Analysis": {
            "keywords": {
                "analysis": 10,
                "theory": 8,
                "composition": 9,
                "structure": 8,
                "technique": 7,
                "style": 6,
                "genre": 7,
                "interpretation": 8,
            },
            "aspects": [
                "theory",
                "structure",
                "technique",
                "interpretation",
                "context",
            ],
        },
        "Creative_Context": {
            "keywords": {
                "inspiration": 9,
                "muse": 8,
                "creative": 7,
                "artistic": 6,
                "vision": 8,
                "concept": 7,
                "theme": 9,
                "narrative": 8,
                "storytelling": 8,
            },
            "contexts": ["inspiration", "creation", "performance", "interpretation"],
        },
    }

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.memory_dir = self.base_dir / ".nocturne_memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.memory_dir / "nocturne_melodies.db"

        # AutoTag integration for musical content
        self.autotag_scripts = {
            "main": "/Users/steven/AutoTag/scripts/autotag_main.py",
            "phase1": "/Users/steven/AutoTag/scripts/phase1_rapid_scan.py",
            "autotagger": "/Users/steven/AutoTagger/current/autotagger.py",
        }

        self.init_database()

    def init_database(self):
        """Initialize the NocturneMelodies database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Core musical content table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS musical_content (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                nocturne_category TEXT,
                musical_type TEXT,
                confidence REAL,
                emotional_tone TEXT,
                thematic_elements TEXT,
                melodic_complexity REAL,
                lyrical_depth REAL,
                creative_context TEXT,
                autotag_metadata TEXT,
                ai_analysis TEXT,
                size_bytes INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                content_hash TEXT
            )
        """
        )

        # Melodic analysis table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS melodic_analysis (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                melody_type TEXT,
                harmony_profile TEXT,
                rhythmic_pattern TEXT,
                key_signature TEXT,
                tempo_estimate TEXT,
                complexity_score REAL,
                emotional_mapping TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES musical_content(id)
            )
        """
        )

        # Lyrical analysis table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lyrical_analysis (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                poetic_style TEXT,
                thematic_depth REAL,
                emotional_intensity REAL,
                narrative_structure TEXT,
                metaphorical_density REAL,
                rhyme_scheme TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES musical_content(id)
            )
        """
        )

        # Nocturne context table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nocturne_context (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                atmospheric_quality REAL,
                nocturnal_theme TEXT,
                dreamlike_elements TEXT,
                introspective_depth REAL,
                serenity_index REAL,
                melancholy_score REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES musical_content(id)
            )
        """
        )

        # Multi-tier autotag results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS autotag_tiers (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                tier INTEGER,
                autotag_system TEXT,
                results TEXT,
                musical_insights TEXT,
                confidence REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES musical_content(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def analyze_musical_content(self, target_path: str) -> dict[str, Any]:
        """Comprehensive musical content analysis"""
        print("🌙 NocturneMelodies - Musical Content Analysis")
        print("=" * 50)

        results = {
            "analysis_target": target_path,
            "started_at": datetime.now().isoformat(),
            "musical_content_found": [],
            "nocturne_themes_identified": [],
            "melodic_analysis": [],
            "lyrical_insights": [],
            "creative_context": {},
        }

        # Phase 1: Content Discovery
        print("🎵 Phase 1: Musical Content Discovery")
        discovered_content = self._discover_musical_content(target_path)
        results["musical_content_found"] = discovered_content

        # Phase 2: Nocturne Theme Analysis
        print("🌙 Phase 2: Nocturne Theme Analysis")
        nocturne_themes = self._analyze_nocturne_themes(discovered_content)
        results["nocturne_themes_identified"] = nocturne_themes

        # Phase 3: Melodic Intelligence
        print("🎼 Phase 3: Melodic Intelligence Analysis")
        melodic_insights = self._analyze_melodic_intelligence(discovered_content)
        results["melodic_analysis"] = melodic_insights

        # Phase 4: Lyrical Depth Analysis
        print("📝 Phase 4: Lyrical Depth Analysis")
        lyrical_insights = self._analyze_lyrical_depth(discovered_content)
        results["lyrical_insights"] = lyrical_insights

        # Phase 5: Creative Context Integration
        print("🎨 Phase 5: Creative Context Integration")
        creative_context = self._integrate_creative_context(discovered_content)
        results["creative_context"] = creative_context

        # Phase 6: Multi-Tier AutoTag Integration
        print("🏷️  Phase 6: Multi-Tier AutoTag Integration")
        autotag_results = self._run_musical_autotag(target_path)
        results["autotag_integration"] = autotag_results

        results["completed_at"] = datetime.now().isoformat()
        results["total_content_analyzed"] = len(discovered_content)

        # Save comprehensive results
        self._save_musical_analysis(results)

        print(f"\n✅ Analysis Complete: {len(discovered_content)} musical items analyzed")
        return results

    def _discover_musical_content(self, target_path: str) -> list[dict[str, Any]]:
        """Discover and categorize musical content"""
        musical_content = []

        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # Check if this is musical content
                if self._is_musical_file(file_path):
                    try:
                        stat = file_path.stat()
                        content_preview = self._get_content_preview(file_path)

                        musical_item = {
                            "file_path": str(file_path),
                            "file_name": file,
                            "extension": ext,
                            "size_bytes": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "content_preview": content_preview,
                            "musical_type": self._classify_musical_type(file_path, content_preview),
                            "nocturne_potential": self._assess_nocturne_potential(content_preview),
                        }

                        musical_content.append(musical_item)

                        # Store in database
                        self._store_musical_content(musical_item)

                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

        return musical_content

    def _is_musical_file(self, file_path: Path) -> bool:
        """Determine if file contains musical content"""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()

        # File extensions
        musical_extensions = {
            ".txt",
            ".md",
            ".html",
            ".json",
            ".csv",
            ".mp3",
            ".wav",
            ".flac",
            ".midi",
        }

        # Keywords in filename
        musical_keywords = [
            "music",
            "song",
            "lyrics",
            "melody",
            "composition",
            "nocturne",
            "serenade",
            "lullaby",
            "harmony",
            "chord",
            "rhythm",
        ]

        if ext in musical_extensions:
            return True

        if any(keyword in name for keyword in musical_keywords):
            return True

        return False

    def _get_content_preview(self, file_path: Path, max_length: int = 2000) -> str:
        """Get content preview from file"""
        try:
            if file_path.suffix.lower() in [".txt", ".md", ".json", ".csv", ".html"]:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    return f.read(max_length)
            else:
                return f"Binary file: {file_path.suffix}"
        except Exception:
            return "Unable to read content"

    def _classify_musical_type(self, file_path: Path, content: str) -> str:
        """Classify the type of musical content"""
        ext = file_path.suffix.lower()
        content_lower = content.lower()

        # Audio files
        if ext in [".mp3", ".wav", ".flac", ".midi"]:
            return "audio_recording"

        # Lyrics and text content
        if any(word in content_lower for word in ["verse", "chorus", "lyrics", "melody"]):
            return "lyrics_composition"

        if any(word in content_lower for word in ["harmony", "chord", "progression", "key"]):
            return "musical_theory"

        if any(word in content_lower for word in ["nocturne", "serenade", "lullaby"]):
            return "nocturne_composition"

        if any(word in content_lower for word in ["analysis", "interpretation", "technique"]):
            return "musical_analysis"

        return "musical_content"

    def _assess_nocturne_potential(self, content: str) -> float:
        """Assess how nocturne-like the content is"""
        nocturne_keywords = [
            "night",
            "nocturne",
            "moonlight",
            "twilight",
            "midnight",
            "stars",
            "dream",
            "serenade",
            "lullaby",
            "peaceful",
            "introspective",
            "atmospheric",
            "ethereal",
            "melancholy",
            "serenity",
            "reflection",
        ]

        content_lower = content.lower()
        matches = sum(1 for keyword in nocturne_keywords if keyword in content_lower)

        # Normalize score (0-1)
        return min(matches / 5.0, 1.0)

    def _analyze_nocturne_themes(self, content_list: list[dict]) -> list[dict[str, Any]]:
        """Analyze nocturne themes across content"""
        themes_found = []

        for item in content_list:
            content = item.get("content_preview", "").lower()
            themes = []

            # Analyze thematic elements
            if any(word in content for word in ["night", "darkness", "midnight"]):
                themes.append({"theme": "nocturnal", "intensity": 0.9})

            if any(word in content for word in ["moon", "stars", "sky", "celestial"]):
                themes.append({"theme": "celestial", "intensity": 0.8})

            if any(word in content for word in ["dream", "sleep", "lullaby"]):
                themes.append({"theme": "dreamlike", "intensity": 0.85})

            if any(word in content for word in ["peace", "serenity", "calm"]):
                themes.append({"theme": "serene", "intensity": 0.75})

            if any(word in content for word in ["reflection", "introspection", "melancholy"]):
                themes.append({"theme": "introspective", "intensity": 0.8})

            if themes:
                themes_found.append(
                    {
                        "content": item["file_name"],
                        "nocturne_themes": themes,
                        "overall_nocturne_score": sum(t["intensity"] for t in themes) / len(themes),
                    }
                )

        return themes_found

    def _analyze_melodic_intelligence(self, content_list: list[dict]) -> list[dict[str, Any]]:
        """Analyze melodic intelligence in content"""
        melodic_insights = []

        for item in content_list:
            content = item.get("content_preview", "").lower()
            insights = {}

            # Analyze melodic elements
            if any(word in content for word in ["melody", "tune", "melodies"]):
                insights["melodic_content"] = True

            if any(word in content for word in ["harmony", "chord", "progression"]):
                insights["harmonic_structure"] = True

            if any(word in content for word in ["rhythm", "tempo", "beat"]):
                insights["rhythmic_elements"] = True

            # Extract key signatures, tempos if present
            key_match = re.search(r"key[:\s]+([A-G][#b]?(?:\s+major|\s+minor)?)", content, re.IGNORECASE)
            if key_match:
                insights["key_signature"] = key_match.group(1).strip()

            tempo_match = re.search(r"tempo[:\s]+(\d+(?:\s*bpm)?)", content, re.IGNORECASE)
            if tempo_match:
                insights["tempo"] = tempo_match.group(1).strip()

            if insights:
                melodic_insights.append(
                    {
                        "content": item["file_name"],
                        "melodic_insights": insights,
                        "complexity_score": len(insights) / 5.0,  # Normalize 0-1
                    }
                )

        return melodic_insights

    def _analyze_lyrical_depth(self, content_list: list[dict]) -> list[dict[str, Any]]:
        """Analyze lyrical depth and poetic quality"""
        lyrical_insights = []

        for item in content_list:
            content = item.get("content_preview", "")
            insights = {}

            # Analyze poetic elements
            if re.search(r"\b(verse|chorus|bridge|hook)\b", content, re.IGNORECASE):
                insights["structural_elements"] = True

            # Check for rhyme patterns (simple detection)
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            rhyme_words = []
            for line in lines[:10]:  # Check first 10 lines
                words = line.split()
                if words:
                    last_word = re.sub(r"[^\w]", "", words[-1].lower())
                    if len(last_word) > 2:
                        rhyme_words.append(last_word)

            if len(rhyme_words) >= 3:
                insights["rhyme_potential"] = len(set(rhyme_words[-3:])) < 3  # Simple rhyme detection

            # Emotional and thematic analysis
            emotional_words = [
                "love",
                "heart",
                "soul",
                "dream",
                "pain",
                "hope",
                "fear",
                "joy",
            ]
            emotional_count = sum(1 for word in emotional_words if word in content.lower())
            insights["emotional_intensity"] = min(emotional_count / 3.0, 1.0)

            # Metaphorical language
            metaphor_indicators = ["like", "as", "metaphor", "symbol", "represents"]
            metaphor_count = sum(1 for word in metaphor_indicators if word in content.lower())
            insights["metaphorical_density"] = min(metaphor_count / 2.0, 1.0)

            if insights:
                lyrical_insights.append(
                    {
                        "content": item["file_name"],
                        "lyrical_insights": insights,
                        "poetic_depth_score": sum(
                            insights.get(k, 0) for k in ["emotional_intensity", "metaphorical_density"]
                        )
                        / 2.0,
                    }
                )

        return lyrical_insights

    def _integrate_creative_context(self, content_list: list[dict]) -> dict[str, Any]:
        """Integrate creative context across all content"""
        context = {
            "overall_musical_theme": "nocturne_melodies",
            "atmospheric_qualities": [],
            "emotional_landscape": [],
            "creative_inspirations": [],
            "performance_contexts": [],
        }

        # Analyze overall context
        all_content = " ".join(item.get("content_preview", "") for item in content_list).lower()

        # Atmospheric qualities
        if "atmospheric" in all_content or "ethereal" in all_content:
            context["atmospheric_qualities"].append("ethereal_atmosphere")
        if "peaceful" in all_content or "calm" in all_content:
            context["atmospheric_qualities"].append("peaceful_serenity")
        if "dream" in all_content or "sleep" in all_content:
            context["atmospheric_qualities"].append("dreamlike_quality")

        # Emotional landscape
        emotional_themes = [
            "introspective",
            "melancholic",
            "hopeful",
            "reflective",
            "serene",
        ]
        for theme in emotional_themes:
            if theme in all_content:
                context["emotional_landscape"].append(theme)

        # Creative inspirations
        inspiration_keywords = [
            "moonlight",
            "stars",
            "night",
            "twilight",
            "dusk",
            "dawn",
        ]
        for keyword in inspiration_keywords:
            if keyword in all_content:
                context["creative_inspirations"].append(keyword)

        return context

    def _run_musical_autotag(self, target_path: str) -> dict[str, Any]:
        """Run multi-tier autotag specifically for musical content"""
        results = {"tiers_completed": [], "musical_insights": {}}

        # Tier 1: Musical Content Discovery
        try:
            cmd = [
                sys.executable,
                self.autotag_scripts["phase1"],
                "--path",
                target_path,
                "--output",
                str(self.memory_dir / "musical_scan.json"),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                results["tiers_completed"].append(
                    {
                        "tier": 1,
                        "name": "Musical Discovery",
                        "status": "success",
                        "musical_files_found": "processed",
                    }
                )
            else:
                results["tiers_completed"].append(
                    {
                        "tier": 1,
                        "name": "Musical Discovery",
                        "status": "error",
                        "message": result.stderr,
                    }
                )

        except Exception as e:
            results["tiers_completed"].append(
                {
                    "tier": 1,
                    "name": "Musical Discovery",
                    "status": "error",
                    "message": str(e),
                }
            )

        # Additional musical insights
        results["musical_insights"] = {
            "nocturne_focus": True,
            "melodic_intelligence": True,
            "lyrical_depth": True,
            "creative_context": True,
            "autotag_integration": True,
        }

        return results

    def _store_musical_content(self, content: dict[str, Any]):
        """Store musical content in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        content_id = hashlib.md5(content["file_path"].encode()).hexdigest()[:16]

        cursor.execute(
            """
            INSERT OR REPLACE INTO musical_content
            (id, file_path, file_name, nocturne_category, musical_type, confidence,
             emotional_tone, thematic_elements, autotag_metadata, size_bytes,
             created_at, modified_at, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content["file_path"],
                content["file_name"],
                "nocturne_melodies",  # Default category
                content.get("musical_type", "musical_content"),
                content.get("nocturne_potential", 0.5),
                "introspective",  # Default emotional tone
                json.dumps(["night", "dreams", "serenity"]),  # Default themes
                json.dumps({"autotag_integrated": True}),
                content["size_bytes"],
                content["modified"],
                content["modified"],
                hashlib.md5(content.get("content_preview", "").encode()).hexdigest(),
            ),
        )

        conn.commit()
        conn.close()

    def _save_musical_analysis(self, results: dict[str, Any]):
        """Save comprehensive musical analysis results"""
        output_file = self.memory_dir / "nocturne_melodies_analysis.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"🎼 NocturneMelodies analysis saved to: {output_file}")

    def generate_nocturne_report(self) -> dict[str, Any]:
        """Generate comprehensive nocturne melodies report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "system": "NocturneMelodies",
            "musical_content_indexed": 0,
            "nocturne_categories": {},
            "melodic_analysis_count": 0,
            "lyrical_analysis_count": 0,
            "creative_context_insights": {},
            "autotag_tiers_completed": 0,
        }

        # Get content statistics
        cursor.execute("SELECT COUNT(*) FROM musical_content")
        report["musical_content_indexed"] = cursor.fetchone()[0]

        cursor.execute("SELECT nocturne_category, COUNT(*) FROM musical_content GROUP BY nocturne_category")
        report["nocturne_categories"] = dict(cursor.fetchall())

        cursor.execute("SELECT COUNT(*) FROM melodic_analysis")
        report["melodic_analysis_count"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lyrical_analysis")
        report["lyrical_analysis_count"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM autotag_tiers")
        report["autotag_tiers_completed"] = cursor.fetchone()[0]

        conn.close()

        # Save report
        report_file = self.memory_dir / "nocturne_melodies_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"🌙 NocturneMelodies report saved to: {report_file}")
        return report


def main():
    parser = argparse.ArgumentParser(description="NocturneMelodies - AI-Powered Musical Content Intelligence")
    parser.add_argument("command", choices=["analyze", "report"], help="Command to run")
    parser.add_argument("--target", help="Target directory for musical analysis")

    args = parser.parse_args()

    system = NocturneMelodies()

    if args.command == "analyze":
        if not args.target:
            print("❌ --target required for analyze command")
            sys.exit(1)

        results = system.analyze_musical_content(args.target)
        print(f"🎵 NocturneMelodies analysis complete: {results['total_content_analyzed']} musical items processed")

    elif args.command == "report":
        report = system.generate_nocturne_report()
        print("🌙 NocturneMelodies Report:")
        print(f"   Musical content indexed: {report['musical_content_indexed']}")
        print(f"   Nocturne categories: {len(report['nocturne_categories'])}")
        print(f"   Melodic analyses: {report['melodic_analysis_count']}")
        print(f"   Lyrical analyses: {report['lyrical_analysis_count']}")
        print(f"   AutoTag tiers: {report['autotag_tiers_completed']}")


if __name__ == "__main__":
    main()
