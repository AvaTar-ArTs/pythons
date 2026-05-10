#!/usr/bin/env python3
"""
NocturneNexus - Advanced AI Content Intelligence Network

Ultimate evolution of creative content analysis featuring:
- Deep emotional intelligence and sentiment analysis
- Complex contextual relationship mapping
- Multi-dimensional content understanding
- Creative pattern recognition and synthesis
- Semantic network analysis
- Emotional resonance mapping
- Contextual narrative intelligence
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
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


class NocturneNexus:
    """Advanced AI Content Intelligence Network"""

    # Emotional intelligence mappings
    EMOTIONAL_SPECTRUM = {
        "serene": ["peaceful", "calm", "tranquil", "serene", "soothing"],
        "melancholic": ["sad", "sorrowful", "wistful", "melancholy", "regretful"],
        "dreamy": ["dreamlike", "ethereal", "surreal", "imaginary", "visionary"],
        "introspective": ["reflective", "contemplative", "thoughtful", "meditative"],
        "romantic": ["love", "passion", "tender", "affectionate", "devoted"],
        "mystical": ["mysterious", "spiritual", "sacred", "divine", "transcendent"],
        "nocturnal": ["night", "darkness", "moonlight", "shadows", "midnight"],
        "celestial": ["stars", "cosmic", "heavenly", "astral", "infinite"],
    }

    # Contextual relationship patterns
    CONTEXT_PATTERNS = {
        "narrative_flow": ["beginning", "middle", "end", "climax", "resolution"],
        "emotional_arc": ["introduction", "rising", "peak", "falling", "conclusion"],
        "thematic_layers": [
            "surface",
            "subtext",
            "symbolism",
            "archetype",
            "universal",
        ],
        "creative_influence": ["inspiration", "influence", "homage", "transformation"],
    }

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.nexus_dir = self.base_dir / ".nexus"
        self.nexus_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.nexus_dir / "nocturne_nexus.db"
        self.init_nexus_database()

    def init_nexus_database(self):
        """Initialize the advanced nexus database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Core content intelligence
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_intelligence (
                id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                content_type TEXT,
                primary_category TEXT,
                emotional_profile TEXT,
                contextual_relationships TEXT,
                semantic_network TEXT,
                creative_metadata TEXT,
                intelligence_score REAL,
                resonance_index REAL,
                created_at TIMESTAMP,
                analyzed_at TIMESTAMP
            )
        """
        )

        # Emotional intelligence mapping
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS emotional_intelligence (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                emotion_spectrum TEXT,
                emotional_intensity REAL,
                sentiment_analysis TEXT,
                mood_progression TEXT,
                emotional_resonance REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_intelligence(id)
            )
        """
        )

        # Contextual relationship network
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contextual_network (
                id TEXT PRIMARY KEY,
                source_content_id TEXT,
                target_content_id TEXT,
                relationship_type TEXT,
                relationship_strength REAL,
                contextual_distance INTEGER,
                narrative_flow TEXT,
                thematic_connection TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (source_content_id) REFERENCES content_intelligence(id),
                FOREIGN KEY (target_content_id) REFERENCES content_intelligence(id)
            )
        """
        )

        # Creative pattern recognition
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS creative_patterns (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                pattern_type TEXT,
                pattern_recognition TEXT,
                creative_influence TEXT,
                artistic_technique TEXT,
                innovation_score REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_intelligence(id)
            )
        """
        )

        # Semantic understanding network
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_network (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                semantic_core TEXT,
                conceptual_layers TEXT,
                metaphorical_depth REAL,
                symbolic_meaning TEXT,
                interpretive_framework TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_intelligence(id)
            )
        """
        )

        # Content synthesis engine
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_synthesis (
                id TEXT PRIMARY KEY,
                synthesis_type TEXT,
                source_content_ids TEXT,
                synthesized_content TEXT,
                synthesis_quality REAL,
                creative_novelty REAL,
                emotional_impact REAL,
                created_at TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def deep_content_analysis(self, target_path: str) -> dict[str, Any]:
        """Perform deep, multi-dimensional content analysis"""
        print("🧠 NocturneNexus - Deep Content Intelligence Analysis")
        print("=" * 60)

        analysis = {
            "analysis_target": target_path,
            "initiated_at": datetime.now().isoformat(),
            "intelligence_layers": {},
            "emotional_landscape": {},
            "contextual_network": {},
            "creative_insights": {},
            "semantic_understanding": {},
        }

        # Phase 1: Content Discovery & Classification
        print("📊 Phase 1: Advanced Content Discovery")
        discovered_content = self.discover_content_intelligence(target_path)
        analysis["intelligence_layers"]["discovered_content"] = discovered_content

        # Phase 2: Emotional Intelligence Analysis
        print("💭 Phase 2: Emotional Intelligence Mapping")
        emotional_profile = self.analyze_emotional_intelligence(discovered_content)
        analysis["emotional_landscape"] = emotional_profile

        # Phase 3: Contextual Relationship Mapping
        print("🔗 Phase 3: Contextual Relationship Network")
        contextual_network = self.map_contextual_relationships(discovered_content)
        analysis["contextual_network"] = contextual_network

        # Phase 4: Creative Pattern Recognition
        print("🎨 Phase 4: Creative Pattern Recognition")
        creative_patterns = self.recognize_creative_patterns(discovered_content)
        analysis["creative_insights"] = creative_patterns

        # Phase 5: Semantic Network Analysis
        print("🧩 Phase 5: Semantic Network Analysis")
        semantic_network = self.analyze_semantic_network(discovered_content)
        analysis["semantic_understanding"] = semantic_network

        # Phase 6: Intelligence Synthesis
        print("🔮 Phase 6: Intelligence Synthesis")
        synthesis = self.synthesize_intelligence(analysis)
        analysis["intelligence_synthesis"] = synthesis

        analysis["completed_at"] = datetime.now().isoformat()
        analysis["total_content_processed"] = len(discovered_content)

        # Save comprehensive analysis
        self.save_nexus_analysis(analysis)

        print(f"\n✅ Deep Analysis Complete: {len(discovered_content)} content items processed")
        print(f"🧠 Intelligence layers: {len(analysis['intelligence_layers'])}")
        print(f"💭 Emotional dimensions: {len(analysis['emotional_landscape'])}")
        print(f"🔗 Relationship mappings: {len(analysis['contextual_network'])}")

        return analysis

    def discover_content_intelligence(self, target_path: str) -> list[dict[str, Any]]:
        """Advanced content discovery with intelligence scoring"""
        content_intelligence = []

        path_obj = Path(target_path).expanduser().resolve()

        for root, dirs, files in os.walk(path_obj):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file

                # Advanced content assessment
                intelligence_profile = self.assess_content_intelligence(file_path)

                if intelligence_profile["intelligence_score"] > 0.1:  # Minimum threshold
                    content_item = {
                        "path": str(file_path),
                        "name": file,
                        "intelligence_profile": intelligence_profile,
                        "file_metadata": {
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            "extension": file_path.suffix.lower(),
                        },
                    }

                    content_intelligence.append(content_item)
                    self.store_content_intelligence(content_item)

        return content_intelligence

    def assess_content_intelligence(self, file_path: Path) -> dict[str, Any]:
        """Comprehensive content intelligence assessment"""
        intelligence = {
            "content_type": "unknown",
            "primary_category": "other",
            "intelligence_score": 0.0,
            "emotional_indicators": [],
            "contextual_markers": [],
            "creative_elements": [],
            "semantic_density": 0.0,
            "resonance_potential": 0.0,
        }

        ext = file_path.suffix.lower()

        # Content type detection
        if ext in [".txt", ".md", ".html", ".json"]:
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(5000).lower()  # Larger sample for deep analysis

                # Musical content analysis
                musical_score = self.calculate_musical_intelligence(content)
                if musical_score > 0.3:
                    intelligence["content_type"] = "musical_content"
                    intelligence["intelligence_score"] += musical_score

                    # Nocturne-specific analysis
                    nocturne_score = self.calculate_nocturne_intelligence(content)
                    if nocturne_score > 0.5:
                        intelligence["primary_category"] = "nocturne_masterpiece"
                        intelligence["intelligence_score"] += nocturne_score
                    else:
                        intelligence["primary_category"] = "musical_composition"

                # Emotional intelligence analysis
                emotional_profile = self.analyze_emotional_spectrum(content)
                intelligence["emotional_indicators"] = emotional_profile["detected_emotions"]
                intelligence["intelligence_score"] += emotional_profile["emotional_depth"] * 0.3

                # Contextual intelligence
                contextual_markers = self.identify_contextual_markers(content)
                intelligence["contextual_markers"] = contextual_markers
                intelligence["intelligence_score"] += len(contextual_markers) * 0.1

                # Creative pattern recognition
                creative_elements = self.identify_creative_patterns(content)
                intelligence["creative_elements"] = creative_elements
                intelligence["intelligence_score"] += len(creative_elements) * 0.15

                # Semantic density calculation
                semantic_density = self.calculate_semantic_density(content)
                intelligence["semantic_density"] = semantic_density
                intelligence["intelligence_score"] += semantic_density * 0.2

                # Resonance potential
                resonance = self.calculate_resonance_potential(content)
                intelligence["resonance_potential"] = resonance

            except Exception as e:
                intelligence["error"] = str(e)

        elif ext in [".mp3", ".wav", ".flac", ".midi"]:
            intelligence["content_type"] = "audio_recording"
            intelligence["primary_category"] = "musical_performance"
            intelligence["intelligence_score"] = 0.7  # Audio files have inherent musical value

        # Normalize intelligence score
        intelligence["intelligence_score"] = min(intelligence["intelligence_score"], 1.0)

        return intelligence

    def calculate_musical_intelligence(self, content: str) -> float:
        """Calculate musical intelligence score"""
        musical_keywords = [
            "melody",
            "harmony",
            "chord",
            "rhythm",
            "tempo",
            "key",
            "scale",
            "verse",
            "chorus",
            "bridge",
            "lyrics",
            "song",
            "music",
            "tune",
            "composition",
            "arrangement",
            "orchestration",
            "symphony",
        ]

        score = 0
        content_lower = content.lower()

        for keyword in musical_keywords:
            if keyword in content_lower:
                score += 0.05  # Each musical keyword adds to intelligence

        # Bonus for structural elements
        if re.search(r"\[verse\s*\d*\]", content_lower):
            score += 0.1
        if re.search(r"\[chorus\]", content_lower):
            score += 0.1
        if any(word in content_lower for word in ["bridge", "solo", "coda"]):
            score += 0.1

        return min(score, 1.0)

    def calculate_nocturne_intelligence(self, content: str) -> float:
        """Calculate nocturne-specific intelligence"""
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
            "celestial",
            "cosmic",
        ]

        score = 0
        content_lower = content.lower()

        for keyword in nocturne_keywords:
            if keyword in content_lower:
                score += 0.08  # Higher weight for nocturne elements

        # Bonus for thematic combinations
        if any(word in content_lower for word in ["night", "darkness"]) and any(
            word in content_lower for word in ["peace", "serenity"]
        ):
            score += 0.2  # Nocturne signature combination

        if "nocturne" in content_lower:
            score += 0.3  # Explicit nocturne reference

        return min(score, 1.0)

    def analyze_emotional_spectrum(self, content: str) -> dict[str, Any]:
        """Analyze emotional spectrum in content"""
        detected_emotions = []
        emotional_depth = 0.0

        content_lower = content.lower()

        for emotion, keywords in self.EMOTIONAL_SPECTRUM.items():
            emotion_score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    emotion_score += 1

            if emotion_score > 0:
                detected_emotions.append({"emotion": emotion, "intensity": min(emotion_score / 3.0, 1.0)})
                emotional_depth += emotion_score / len(keywords)

        return {
            "detected_emotions": detected_emotions,
            "emotional_depth": min(emotional_depth, 1.0),
            "emotional_complexity": len(detected_emotions) / len(self.EMOTIONAL_SPECTRUM),
        }

    def identify_contextual_markers(self, content: str) -> list[str]:
        """Identify contextual relationship markers"""
        markers = []
        content_lower = content.lower()

        # Narrative flow markers
        if any(word in content_lower for word in ["beginning", "start", "introduction"]):
            markers.append("narrative_opening")
        if any(word in content_lower for word in ["climax", "peak", "crisis"]):
            markers.append("narrative_climax")
        if any(word in content_lower for word in ["end", "conclusion", "resolution"]):
            markers.append("narrative_closure")

        # Emotional arc markers
        if any(word in content_lower for word in ["rising", "building", "growing"]):
            markers.append("emotional_escalation")
        if any(word in content_lower for word in ["falling", "fading", "diminishing"]):
            markers.append("emotional_resolution")

        # Thematic layer markers
        if any(word in content_lower for word in ["symbol", "metaphor", "meaning"]):
            markers.append("symbolic_layer")
        if any(word in content_lower for word in ["universal", "archetype", "myth"]):
            markers.append("universal_theme")

        return markers

    def identify_creative_patterns(self, content: str) -> list[str]:
        """Identify creative patterns and techniques"""
        patterns = []
        content_lower = content.lower()

        # Literary devices
        if re.search(r"\b(like|as)\b.*\b(as|than)\b", content_lower):
            patterns.append("similie_metaphor")
        if re.search(r"\b(alliteration|assonance|consonance)\b", content_lower):
            patterns.append("sound_devices")

        # Musical patterns
        if re.search(r"\bchord\s+progression\b", content_lower):
            patterns.append("harmonic_progression")
        if re.search(r"\brhythmic\s+pattern\b", content_lower):
            patterns.append("rhythmic_motif")

        # Creative techniques
        if any(word in content_lower for word in ["inspiration", "muse", "creative"]):
            patterns.append("creative_inspiration")
        if any(word in content_lower for word in ["innovation", "original", "unique"]):
            patterns.append("innovative_approach")

        return patterns

    def calculate_semantic_density(self, content: str) -> float:
        """Calculate semantic density score"""
        words = re.findall(r"\b\w+\b", content.lower())
        unique_words = set(words)

        # Calculate lexical diversity
        lexical_diversity = len(unique_words) / max(len(words), 1)

        # Calculate conceptual density (words per sentence approximation)
        sentences = re.split(r"[.!?]+", content)
        avg_words_per_sentence = len(words) / max(len(sentences), 1)

        # Semantic density combines diversity and complexity
        density = (lexical_diversity * 0.6) + (min(avg_words_per_sentence / 20.0, 1.0) * 0.4)

        return min(density, 1.0)

    def calculate_resonance_potential(self, content: str) -> float:
        """Calculate emotional resonance potential"""
        resonance_factors = 0
        content_lower = content.lower()

        # Emotional triggers
        emotional_words = ["love", "fear", "joy", "sadness", "anger", "hope", "despair"]
        resonance_factors += sum(1 for word in emotional_words if word in content_lower)

        # Universal themes
        universal_themes = ["death", "birth", "love", "loss", "redemption", "sacrifice"]
        resonance_factors += sum(1 for theme in universal_themes if theme in content_lower) * 2

        # Intensity modifiers
        intensity_words = ["deeply", "profoundly", "intensely", "eternally", "forever"]
        resonance_factors += sum(1 for word in intensity_words if word in content_lower) * 1.5

        # Normalize to 0-1 scale
        return min(resonance_factors / 10.0, 1.0)

    def analyze_emotional_intelligence(self, content_list: list[dict]) -> dict[str, Any]:
        """Comprehensive emotional intelligence analysis"""
        emotional_landscape = {
            "dominant_emotions": {},
            "emotional_progression": [],
            "resonance_patterns": [],
            "emotional_complexity": 0.0,
        }

        all_emotions = []
        for item in content_list:
            profile = item.get("intelligence_profile", {})
            emotions = profile.get("emotional_indicators", [])
            all_emotions.extend([e["emotion"] for e in emotions])

        # Calculate dominant emotions
        emotion_counts = defaultdict(int)
        for emotion in all_emotions:
            emotion_counts[emotion] += 1

        emotional_landscape["dominant_emotions"] = dict(emotion_counts)

        # Calculate emotional complexity
        unique_emotions = len(set(all_emotions))
        emotional_landscape["emotional_complexity"] = unique_emotions / len(self.EMOTIONAL_SPECTRUM)

        return emotional_landscape

    def map_contextual_relationships(self, content_list: list[dict]) -> dict[str, Any]:
        """Map contextual relationships between content"""
        network = {
            "relationship_clusters": [],
            "narrative_threads": [],
            "thematic_connections": [],
            "contextual_distance_matrix": {},
        }

        # Simple relationship mapping based on categories
        categories = defaultdict(list)
        for item in content_list:
            category = item.get("intelligence_profile", {}).get("primary_category", "other")
            categories[category].append(item["name"])

        # Identify clusters
        for category, items in categories.items():
            if len(items) > 1:
                network["relationship_clusters"].append(
                    {
                        "category": category,
                        "items": items,
                        "cluster_strength": len(items) / len(content_list),
                    }
                )

        return network

    def recognize_creative_patterns(self, content_list: list[dict]) -> dict[str, Any]:
        """Recognize creative patterns across content"""
        patterns = {
            "recurring_themes": [],
            "creative_techniques": [],
            "innovative_elements": [],
            "pattern_frequency": {},
        }

        # Analyze patterns across all content
        all_patterns = []
        for item in content_list:
            creative_elements = item.get("intelligence_profile", {}).get("creative_elements", [])
            all_patterns.extend(creative_elements)

        # Calculate pattern frequency
        pattern_counts = defaultdict(int)
        for pattern in all_patterns:
            pattern_counts[pattern] += 1

        patterns["pattern_frequency"] = dict(pattern_counts)

        # Identify recurring themes
        recurring = [p for p, count in pattern_counts.items() if count > 1]
        patterns["recurring_themes"] = recurring

        return patterns

    def analyze_semantic_network(self, content_list: list[dict]) -> dict[str, Any]:
        """Analyze semantic network relationships"""
        semantic_network = {
            "core_concepts": [],
            "conceptual_clusters": [],
            "semantic_density_distribution": [],
            "meaningful_connections": [],
        }

        # Extract semantic features
        semantic_scores = []
        for item in content_list:
            density = item.get("intelligence_profile", {}).get("semantic_density", 0)
            semantic_scores.append({"content": item["name"], "semantic_density": density})

        semantic_network["semantic_density_distribution"] = semantic_scores

        # Identify high-semantic content
        high_semantic = [s for s in semantic_scores if s["semantic_density"] > 0.5]
        semantic_network["core_concepts"] = [s["content"] for s in high_semantic]

        return semantic_network

    def synthesize_intelligence(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Synthesize all intelligence layers into unified insights"""
        synthesis = {
            "overall_intelligence_score": 0.0,
            "dominant_narrative": "",
            "emotional_signature": "",
            "creative_profile": "",
            "recommendations": [],
        }

        # Calculate overall intelligence score
        content_count = analysis.get("total_content_processed", 0)
        emotional_layers = len(analysis.get("emotional_landscape", {}))
        contextual_connections = len(analysis.get("contextual_network", {}).get("relationship_clusters", []))

        synthesis["overall_intelligence_score"] = min(
            (content_count * 0.3 + emotional_layers * 0.3 + contextual_connections * 0.4) / 10.0,
            1.0,
        )

        # Determine dominant narrative
        dominant_emotions = analysis.get("emotional_landscape", {}).get("dominant_emotions", {})
        if dominant_emotions:
            top_emotion = max(dominant_emotions.items(), key=lambda x: x[1])
            synthesis["emotional_signature"] = f"Predominantly {top_emotion[0]} with {top_emotion[1]} expressions"

        # Generate recommendations
        if synthesis["overall_intelligence_score"] > 0.7:
            synthesis["recommendations"].append("High intelligence content - consider deeper analysis")
        if emotional_layers > 3:
            synthesis["recommendations"].append("Rich emotional landscape - potential for therapeutic applications")
        if contextual_connections > 2:
            synthesis["recommendations"].append("Strong interconnected themes - narrative potential identified")

        return synthesis

    def store_content_intelligence(self, content: dict[str, Any]):
        """Store content intelligence in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        content_id = hashlib.md5(content["path"].encode()).hexdigest()[:16]
        profile = content.get("intelligence_profile", {})

        cursor.execute(
            """
            INSERT OR REPLACE INTO content_intelligence
            (id, path, name, content_type, primary_category, emotional_profile,
             contextual_relationships, semantic_network, creative_metadata,
             intelligence_score, resonance_index, created_at, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                content_id,
                content["path"],
                content["name"],
                profile.get("content_type", "unknown"),
                profile.get("primary_category", "other"),
                json.dumps(profile.get("emotional_indicators", [])),
                json.dumps(profile.get("contextual_markers", [])),
                json.dumps({"semantic_density": profile.get("semantic_density", 0)}),
                json.dumps(profile.get("creative_elements", [])),
                profile.get("intelligence_score", 0),
                profile.get("resonance_potential", 0),
                content["file_metadata"]["modified"],
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def save_nexus_analysis(self, analysis: dict[str, Any]):
        """Save comprehensive nexus analysis"""
        output_file = self.nexus_dir / "nocturne_nexus_analysis.json"
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)

        print(f"🔮 Nexus analysis saved to: {output_file}")

    def generate_nexus_report(self) -> dict[str, Any]:
        """Generate comprehensive nexus intelligence report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "nexus_name": "NocturneNexus",
            "intelligence_metrics": {},
            "emotional_intelligence": {},
            "contextual_network": {},
            "creative_discovery": {},
            "semantic_insights": {},
        }

        # Intelligence metrics
        cursor.execute("SELECT COUNT(*), AVG(intelligence_score), AVG(resonance_index) FROM content_intelligence")
        count, avg_intelligence, avg_resonance = cursor.fetchone()
        report["intelligence_metrics"] = {
            "total_content_analyzed": count or 0,
            "average_intelligence_score": avg_intelligence or 0,
            "average_resonance_index": avg_resonance or 0,
        }

        # Category breakdown
        cursor.execute("SELECT primary_category, COUNT(*) FROM content_intelligence GROUP BY primary_category")
        report["intelligence_metrics"]["category_breakdown"] = dict(cursor.fetchall())

        conn.close()

        # Save report
        report_file = self.nexus_dir / "nocturne_nexus_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    parser = argparse.ArgumentParser(description="NocturneNexus - Advanced AI Content Intelligence Network")
    parser.add_argument("command", choices=["analyze", "report"], help="Command to run")
    parser.add_argument("--target", help="Target directory for deep analysis")

    args = parser.parse_args()

    nexus = NocturneNexus()

    if args.command == "analyze":
        if not args.target:
            print("❌ --target required for analyze command")
            sys.exit(1)

        results = nexus.deep_content_analysis(args.target)
        print(f"🔮 NocturneNexus deep analysis complete: {results['total_content_processed']} items processed")

    elif args.command == "report":
        report = nexus.generate_nexus_report()
        print("🔮 NocturneNexus Intelligence Report:")
        print(f"   Content analyzed: {report['intelligence_metrics']['total_content_analyzed']}")
        print(f"   Intelligence score: {report['intelligence_metrics']['average_intelligence_score']:.2f}")
        print(f"   Resonance index: {report['intelligence_metrics']['average_resonance_index']:.2f}")
        print(f"   Categories identified: {len(report['intelligence_metrics']['category_breakdown'])}")


if __name__ == "__main__":
    main()
