#!/usr/bin/env python3
"""
Tag It All - Comprehensive Content Tagging System

Combines all Nocturne AI systems for complete content tagging:
- NocturneNexus deep intelligence analysis
- AutoTag multi-tier classification
- Emotional intelligence tagging
- Creative pattern recognition
- Semantic network mapping
"""

import argparse
import hashlib
import json
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


class TagItAll:
    """Comprehensive content tagging system"""

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.tagged_dir = self.base_dir / ".tagged"
        self.tagged_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.tagged_dir / "tag_it_all.db"

        # Import all available systems
        self.systems = self._load_available_systems()

        self.init_master_database()

    def _load_available_systems(self) -> dict[str, Any]:
        """Load all available tagging systems"""
        systems = {}

        # Try to import NocturneNexus
        try:
            sys.path.insert(0, str(self.base_dir))
            from nocturne_nexus import NocturneNexus

            systems["nexus"] = NocturneNexus()
            print("✅ NocturneNexus loaded")
        except ImportError:
            print("⚠️  NocturneNexus not available")

        # Try to import NocturneMelodies
        try:
            from nocturne_melodies import NocturneMelodies

            systems["melodies"] = NocturneMelodies()
            print("✅ NocturneMelodies loaded")
        except ImportError:
            print("⚠️  NocturneMelodies not available")

        # Try to import NocturneMemory AI
        try:
            from nocturnememory_ai import NocturneMemoryAI

            systems["memory"] = NocturneMemoryAI()
            print("✅ NocturneMemory AI loaded")
        except ImportError:
            print("⚠️  NocturneMemory AI not available")

        return systems

    def init_master_database(self):
        """Initialize the master tagging database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Master content tags table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS master_tags (
                id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                file_size INTEGER,
                created_at TIMESTAMP,
                last_analyzed TIMESTAMP,

                -- Basic classification
                content_type TEXT,
                primary_category TEXT,

                -- Intelligence scores
                intelligence_score REAL,
                emotional_depth REAL,
                semantic_density REAL,
                resonance_potential REAL,

                -- Tagging systems results
                nexus_tags TEXT,
                melodies_tags TEXT,
                memory_tags TEXT,
                autotag_results TEXT,

                -- Emotional intelligence
                emotional_profile TEXT,
                dominant_emotions TEXT,

                -- Creative analysis
                creative_patterns TEXT,
                artistic_techniques TEXT,

                -- Contextual relationships
                related_content TEXT,
                thematic_connections TEXT,

                -- Metadata
                all_tags TEXT,
                confidence_score REAL
            )
        """
        )

        # Tag relationships table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tag_relationships (
                id TEXT PRIMARY KEY,
                source_content_id TEXT,
                target_content_id TEXT,
                relationship_type TEXT,
                strength REAL,
                created_at TIMESTAMP
            )
        """
        )

        # Tag clusters table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tag_clusters (
                id TEXT PRIMARY KEY,
                cluster_name TEXT,
                cluster_type TEXT,
                content_ids TEXT,
                cluster_tags TEXT,
                created_at TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def tag_everything(self, target_path: str) -> dict[str, Any]:
        """Run comprehensive tagging on everything"""
        print("🏷️  Tag It All - Comprehensive Content Tagging")
        print("=" * 60)

        target_path_obj = Path(target_path).expanduser().resolve()

        tagging_results = {
            "target_path": str(target_path_obj),
            "started_at": datetime.now().isoformat(),
            "systems_used": list(self.systems.keys()),
            "content_processed": 0,
            "tags_applied": 0,
            "relationships_found": 0,
            "clusters_created": 0,
            "detailed_results": {},
        }

        print(f"🎯 Target: {target_path_obj}")
        print(f"🛠️  Systems available: {', '.join(self.systems.keys())}")

        # Phase 1: Multi-System Analysis
        print("\n🔍 Phase 1: Multi-System Content Analysis")
        system_results = self._run_multi_system_analysis(target_path_obj)
        tagging_results["detailed_results"]["system_analysis"] = system_results

        # Phase 2: Cross-System Tag Integration
        print("🔗 Phase 2: Cross-System Tag Integration")
        integrated_tags = self._integrate_cross_system_tags(system_results)
        tagging_results["detailed_results"]["integrated_tags"] = integrated_tags

        # Phase 3: Relationship Discovery
        print("🔗 Phase 3: Content Relationship Discovery")
        relationships = self._discover_content_relationships(system_results)
        tagging_results["detailed_results"]["relationships"] = relationships
        tagging_results["relationships_found"] = len(relationships)

        # Phase 4: Cluster Analysis
        print("📊 Phase 4: Tag Cluster Analysis")
        clusters = self._analyze_tag_clusters(system_results)
        tagging_results["detailed_results"]["clusters"] = clusters
        tagging_results["clusters_created"] = len(clusters)

        # Phase 5: Master Tag Synthesis
        print("🎨 Phase 5: Master Tag Synthesis")
        master_tags = self._synthesize_master_tags(system_results, integrated_tags, relationships, clusters)
        tagging_results["detailed_results"]["master_tags"] = master_tags

        # Store everything
        self._store_comprehensive_tags(master_tags)

        tagging_results["content_processed"] = len(master_tags)
        tagging_results["tags_applied"] = sum(len(tags.get("all_tags", [])) for tags in master_tags.values())
        tagging_results["completed_at"] = datetime.now().isoformat()

        # Save comprehensive results
        self._save_tagging_results(tagging_results)

        print("\n✅ Tagging Complete!")
        print(f"   📁 Content processed: {tagging_results['content_processed']}")
        print(f"   🏷️  Tags applied: {tagging_results['tags_applied']}")
        print(f"   🔗 Relationships found: {tagging_results['relationships_found']}")
        print(f"   📊 Clusters created: {tagging_results['clusters_created']}")

        return tagging_results

    def _run_multi_system_analysis(self, target_path: Path) -> dict[str, Any]:
        """Run analysis across all available systems"""
        system_results = {}

        # NocturneNexus analysis
        if "nexus" in self.systems:
            print("  🧠 Running NocturneNexus analysis...")
            try:
                nexus_results = self.systems["nexus"].deep_content_analysis(str(target_path))
                system_results["nexus"] = {
                    "success": True,
                    "content_analyzed": nexus_results.get("total_content_processed", 0),
                    "intelligence_layers": nexus_results.get("intelligence_layers", {}),
                    "emotional_landscape": nexus_results.get("emotional_landscape", {}),
                    "raw_results": nexus_results,
                }
            except Exception as e:
                system_results["nexus"] = {"success": False, "error": str(e)}

        # NocturneMelodies analysis
        if "melodies" in self.systems:
            print("  🌙 Running NocturneMelodies analysis...")
            try:
                melodies_results = self.systems["melodies"].analyze_musical_content(str(target_path))
                system_results["melodies"] = {
                    "success": True,
                    "content_analyzed": melodies_results.get("total_content_analyzed", 0),
                    "nocturne_themes": melodies_results.get("nocturne_themes_identified", []),
                    "melodic_analysis": melodies_results.get("melodic_analysis", []),
                    "raw_results": melodies_results,
                }
            except Exception as e:
                system_results["melodies"] = {"success": False, "error": str(e)}

        # NocturneMemory AI analysis
        if "memory" in self.systems:
            print("  🤖 Running NocturneMemory AI analysis...")
            try:
                memory_results = self.systems["memory"].run_multitier_autotag(str(target_path))
                system_results["memory"] = {
                    "success": True,
                    "tiers_completed": len(memory_results.get("tiers_completed", [])),
                    "content_processed": memory_results.get("total_content_analyzed", 0),
                    "raw_results": memory_results,
                }
            except Exception as e:
                system_results["memory"] = {"success": False, "error": str(e)}

        return system_results

    def _integrate_cross_system_tags(self, system_results: dict) -> dict[str, Any]:
        """Integrate tags across all systems"""
        integrated = {
            "unified_categories": {},
            "cross_system_consensus": {},
            "conflicting_tags": [],
            "tag_confidence_scores": {},
        }

        # Collect all categories from different systems
        all_categories = set()

        if "nexus" in system_results and system_results["nexus"]["success"]:
            nexus_data = system_results["nexus"]["raw_results"]
            discovered = nexus_data.get("intelligence_layers", {}).get("discovered_content", [])
            for item in discovered:
                cat = item.get("intelligence_profile", {}).get("primary_category", "")
                if cat:
                    all_categories.add(cat)

        if "melodies" in system_results and system_results["melodies"]["success"]:
            # Melodies focuses on musical content
            all_categories.add("musical_content")
            all_categories.add("nocturne_composition")

        integrated["unified_categories"] = list(all_categories)
        integrated["total_unique_categories"] = len(all_categories)

        return integrated

    def _discover_content_relationships(self, system_results: dict) -> list[dict]:
        """Discover relationships between content items"""
        relationships = []

        # Look for thematic connections in Nexus results
        if "nexus" in system_results and system_results["nexus"]["success"]:
            nexus_data = system_results["nexus"]["raw_results"]
            contextual_network = nexus_data.get("contextual_network", {})

            for cluster in contextual_network.get("relationship_clusters", []):
                relationships.append(
                    {
                        "type": "thematic_cluster",
                        "cluster_name": cluster.get("category", "unknown"),
                        "items": cluster.get("items", []),
                        "strength": cluster.get("cluster_strength", 0),
                        "source": "nexus_contextual",
                    }
                )

        # Look for emotional connections
        emotional_landscape = system_results.get("nexus", {}).get("raw_results", {}).get("emotional_landscape", {})
        dominant_emotions = emotional_landscape.get("dominant_emotions", {})

        for emotion, count in dominant_emotions.items():
            if count > 1:  # Multiple items share this emotion
                relationships.append(
                    {
                        "type": "emotional_connection",
                        "emotion": emotion,
                        "shared_by": count,
                        "source": "nexus_emotional",
                    }
                )

        return relationships

    def _analyze_tag_clusters(self, system_results: dict) -> list[dict]:
        """Analyze and create tag clusters"""
        clusters = []

        # Create clusters based on categories
        category_clusters = {}

        if "nexus" in system_results and system_results["nexus"]["success"]:
            discovered = (
                system_results["nexus"]["raw_results"].get("intelligence_layers", {}).get("discovered_content", [])
            )

            for item in discovered:
                category = item.get("intelligence_profile", {}).get("primary_category", "unknown")
                if category not in category_clusters:
                    category_clusters[category] = []
                category_clusters[category].append(item["path"])

        # Convert to cluster format
        for category, paths in category_clusters.items():
            if len(paths) > 1:  # Only create clusters with multiple items
                clusters.append(
                    {
                        "cluster_name": f"{category}_cluster",
                        "cluster_type": "categorical",
                        "content_count": len(paths),
                        "representative_paths": paths[:5],  # First 5 paths
                        "tags": [category, f"cluster_{len(paths)}_items"],
                    }
                )

        return clusters

    def _synthesize_master_tags(
        self,
        system_results: dict,
        integrated_tags: dict,
        relationships: list[dict],
        clusters: list[dict],
    ) -> dict[str, Any]:
        """Synthesize master tags for all content"""
        master_tags = {}

        # Process Nexus results
        if "nexus" in system_results and system_results["nexus"]["success"]:
            discovered = (
                system_results["nexus"]["raw_results"].get("intelligence_layers", {}).get("discovered_content", [])
            )

            for item in discovered:
                content_id = hashlib.md5(item["path"].encode()).hexdigest()[:16]
                profile = item.get("intelligence_profile", {})

                master_tags[content_id] = {
                    "path": item["path"],
                    "name": item["name"],
                    "content_type": profile.get("content_type", "unknown"),
                    "primary_category": profile.get("primary_category", "other"),
                    "intelligence_score": profile.get("intelligence_score", 0),
                    "emotional_depth": len(profile.get("emotional_indicators", [])),
                    "semantic_density": profile.get("semantic_density", 0),
                    "resonance_potential": profile.get("resonance_potential", 0),
                    "all_tags": self._generate_all_tags(item, profile),
                    "confidence_score": profile.get("intelligence_score", 0),
                    "from_systems": ["nexus"],
                }

        # Add system-specific enhancements
        for system_name, system_data in system_results.items():
            if system_data.get("success"):
                self._enhance_with_system_tags(master_tags, system_name, system_data)

        return master_tags

    def _generate_all_tags(self, item: dict, profile: dict) -> list[str]:
        """Generate comprehensive tag list for content"""
        tags = []

        # Content type tags
        content_type = profile.get("content_type", "")
        if content_type:
            tags.append(f"type:{content_type}")

        # Category tags
        category = profile.get("primary_category", "")
        if category:
            tags.append(f"category:{category}")

        # Emotional tags
        for emotion in profile.get("emotional_indicators", []):
            emotion_name = emotion.get("emotion", "")
            intensity = emotion.get("intensity", 0)
            if intensity > 0.5:  # Only high-intensity emotions
                tags.append(f"emotion:{emotion_name}")
                tags.append(f"emotion:{emotion_name}_{intensity:.1f}")

        # Contextual tags
        for marker in profile.get("contextual_markers", []):
            tags.append(f"context:{marker}")

        # Creative tags
        for pattern in profile.get("creative_elements", []):
            tags.append(f"creative:{pattern}")

        # Intelligence tags
        intelligence = profile.get("intelligence_score", 0)
        if intelligence > 0.8:
            tags.append("intelligence:high")
        elif intelligence > 0.5:
            tags.append("intelligence:medium")
        else:
            tags.append("intelligence:low")

        # Resonance tags
        resonance = profile.get("resonance_potential", 0)
        if resonance > 0.5:
            tags.append("resonance:high")
        elif resonance > 0.2:
            tags.append("resonance:medium")

        return tags

    def _enhance_with_system_tags(self, master_tags: dict, system_name: str, system_data: dict):
        """Enhance master tags with system-specific information"""
        for content_id, tags in master_tags.items():
            if system_name not in tags.get("from_systems", []):
                tags["from_systems"].append(system_name)

            # Add system-specific enhancements
            if system_name == "melodies" and system_data.get("success"):
                # Add musical intelligence tags
                tags["all_tags"].extend(["system:melodies", "musical_intelligence:analyzed"])

            elif system_name == "memory" and system_data.get("success"):
                # Add multi-tier autotag tags
                tags["all_tags"].extend(["system:memory", "autotag:multi_tier"])

    def _store_comprehensive_tags(self, master_tags: dict[str, Any]):
        """Store comprehensive tags in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for content_id, tag_data in master_tags.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO master_tags
                (id, path, name, file_size, created_at, last_analyzed,
                 content_type, primary_category, intelligence_score, emotional_depth,
                 semantic_density, resonance_potential, all_tags, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    content_id,
                    tag_data["path"],
                    tag_data["name"],
                    tag_data.get("file_size", 0),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    tag_data.get("content_type", ""),
                    tag_data.get("primary_category", ""),
                    tag_data.get("intelligence_score", 0),
                    tag_data.get("emotional_depth", 0),
                    tag_data.get("semantic_density", 0),
                    tag_data.get("resonance_potential", 0),
                    json.dumps(tag_data.get("all_tags", [])),
                    tag_data.get("confidence_score", 0),
                ),
            )

        conn.commit()
        conn.close()

        print(f"💾 Stored {len(master_tags)} comprehensive tag records")

    def _save_tagging_results(self, results: dict[str, Any]):
        """Save comprehensive tagging results"""
        output_file = self.tagged_dir / "tag_it_all_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"📄 Tagging results saved to: {output_file}")

    def generate_tagging_report(self) -> dict[str, Any]:
        """Generate comprehensive tagging report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "system": "TagItAll",
            "total_content_tagged": 0,
            "unique_tags_applied": 0,
            "tag_categories": {},
            "intelligence_distribution": {},
            "system_coverage": {},
            "top_tags": [],
        }

        # Get total content
        cursor.execute("SELECT COUNT(*) FROM master_tags")
        report["total_content_tagged"] = cursor.fetchone()[0]

        # Get tag statistics
        cursor.execute("SELECT all_tags FROM master_tags")
        all_tags_data = cursor.fetchall()

        tag_counts = {}
        for row in all_tags_data:
            tags = json.loads(row[0]) if row[0] else []
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        report["unique_tags_applied"] = len(tag_counts)

        # Get top 20 tags
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        report["top_tags"] = sorted_tags[:20]

        # Categorize tags
        tag_categories = {}
        for tag, count in tag_counts.items():
            if ":" in tag:
                category = tag.split(":")[0]
                tag_categories[category] = tag_categories.get(category, 0) + count
            else:
                tag_categories["general"] = tag_categories.get("general", 0) + count

        report["tag_categories"] = tag_categories

        # Intelligence score distribution
        cursor.execute("SELECT intelligence_score FROM master_tags")
        scores = [row[0] for row in cursor.fetchall() if row[0] is not None]

        if scores:
            report["intelligence_distribution"] = {
                "average": sum(scores) / len(scores),
                "high_intelligence": len([s for s in scores if s > 0.8]),
                "medium_intelligence": len([s for s in scores if 0.5 <= s <= 0.8]),
                "low_intelligence": len([s for s in scores if s < 0.5]),
            }

        conn.close()

        # Save report
        report_file = self.tagged_dir / "tagging_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    parser = argparse.ArgumentParser(description="Tag It All - Comprehensive Content Tagging System")
    parser.add_argument("command", choices=["tag", "report"], help="Command to run")
    parser.add_argument("--target", help="Target directory for comprehensive tagging")

    args = parser.parse_args()

    tagger = TagItAll()

    if args.command == "tag":
        if not args.target:
            print("❌ --target required for tag command")
            sys.exit(1)

        results = tagger.tag_everything(args.target)
        print(f"🏷️  Tag It All complete: {results['content_processed']} items comprehensively tagged")

    elif args.command == "report":
        report = tagger.generate_tagging_report()
        print("🏷️  Tag It All Report:")
        print(f"   Content tagged: {report['total_content_tagged']}")
        print(f"   Unique tags: {report['unique_tags_applied']}")
        print(f"   Tag categories: {len(report['tag_categories'])}")
        if report.get("intelligence_distribution"):
            intel = report["intelligence_distribution"]
            print(
                f"   Intelligence - Avg: {intel['average']:.2f}, High: {intel['high_intelligence']}, Medium: {intel['medium_intelligence']}"
            )


if __name__ == "__main__":
    main()
