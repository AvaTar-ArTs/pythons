#!/usr/bin/env python3
"""
Content-Aware Management System - Digital Empire Content Optimization
Automatically manage, optimize, and organize content across all systems

Features:
- Automatic duplicate detection and resolution
- Content lifecycle management
- Cross-system content sharing
- SEO optimization across all content
- Automated content updates
"""

import os
import sqlite3
import hashlib
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ContentItem:
    """Represents a content item across the digital empire"""

    id: str
    title: str
    content: str
    content_type: str
    system: str
    file_path: str
    hash: str
    seo_score: float
    last_updated: str
    status: str


@dataclass
class DuplicateGroup:
    """Represents a group of duplicate content items"""

    id: str
    items: List[ContentItem]
    similarity_score: float
    recommended_action: str


class ContentManagementSystem:
    """Content-aware management system for the digital empire"""

    def __init__(self, db_path: str = "databases/content_management.db"):
        self.db_path = db_path
        self.systems = {
            "passive_income_empire": "Passive Income Empire",
            "avatararts_portfolio": "AvatarArts Portfolio",
            "cleanconnect_pro": "CleanConnect Pro",
            "seo_master_index": "SEO Master Index",
            "quantumforge_labs": "QuantumForgeLabs",
        }
        self._init_database()

    def _init_database(self):
        """Initialize content management database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Content items table
            cursor.execute('\''
                CREATE TABLE IF NOT EXISTS content_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT,
                    content_type TEXT,
                    system TEXT,
                    file_path TEXT,
                    hash TEXT UNIQUE,
                    seo_score REAL DEFAULT 0.0,
                    last_updated TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT
                )
            """)

            # Duplicate groups table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS duplicate_groups (
                    id TEXT PRIMARY KEY,
                    items TEXT,
                    similarity_score REAL,
                    recommended_action TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT
                )
            """)

            # Content relationships table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_relationships (
                    id TEXT PRIMARY KEY,
                    source_id TEXT,
                    target_id TEXT,
                    relationship_type TEXT,
                    strength REAL,
                    created_at TEXT
                )
            """)

            conn.commit()
            conn.close()
            logger.info("Content management database initialized")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def analyze_all_content(self) -> Dict[str, Any]:
        """Analyze all content across the digital empire"""
        try:
            analysis_results = {
                "total_files": 0,
                "total_content_items": 0,
                "duplicates_found": 0,
                "seo_optimization_opportunities": 0,
                "cross_system_opportunities": 0,
                "system_breakdown": {},
                "content_types": {},
                "duplicate_groups": [],
                "recommendations": [],
            }

            # Analyze each system
            for system_key, system_name in self.systems.items():
                system_results = self._analyze_system_content(system_key)
                analysis_results["system_breakdown"][system_name] = system_results
                analysis_results["total_files"] += system_results["total_files"]
                analysis_results["total_content_items"] += system_results[
                    "total_content_items"
                ]

            # Find duplicates across all systems
            duplicates = self._find_duplicates()
            analysis_results["duplicate_groups"] = duplicates
            analysis_results["duplicates_found"] = len(duplicates)

            # Generate recommendations
            recommendations = self._generate_recommendations(analysis_results)
            analysis_results["recommendations"] = recommendations

            return analysis_results

        except Exception as e:
            logger.error(f"Failed to analyze all content: {e}")
            return {}

    def _analyze_system_content(self, system_key: str) -> Dict[str, Any]:
        """Analyze content for a specific system"""
        try:
            system_path = self._get_system_path(system_key)
            if not system_path or not os.path.exists(system_path):
                return {"total_files": 0, "total_content_items": 0, "content_types": {}}

            content_items = []
            content_types = {}
            total_files = 0

            # Walk through system directory
            for root, dirs, files in os.walk(system_path):
                for file in files:
                    if self._is_content_file(file):
                        total_files += 1

                        try:
                            content = self._extract_content(file_path)
                            if content:
                                content_type = self._get_content_type(file)
                                content_types[content_type] = (
                                    content_types.get(content_type, 0) + 1
                                )

                                content_item = ContentItem(
                                    id=f"{system_key}_{len(content_items)}",
                                    title=self._extract_title(content, file),
                                    content=content,
                                    content_type=content_type,
                                    system=system_key,
                                    file_path=file_path,
                                    hash=self._calculate_hash(content),
                                    seo_score=self._calculate_seo_score(content),
                                    last_updated=datetime.datetime.now().isoformat(),
                                    status="active",
                                )

                                content_items.append(content_item)

                        except Exception as e:
                            logger.warning(f"Failed to process file {file_path}: {e}")

            return {
                "total_files": total_files,
                "total_content_items": len(content_items),
                "content_types": content_types,
                "content_items": content_items,
            }

        except Exception as e:
            logger.error(f"Failed to analyze system content for {system_key}: {e}")
            return {"total_files": 0, "total_content_items": 0, "content_types": {}}

    def _get_system_path(self, system_key: str) -> Optional[str]:
        """Get the path for a specific system"""
        system_paths = {
            "passive_income_empire": "passive-income-empire",
            "avatararts_portfolio": "AvaTarArTs",
            "cleanconnect_pro": "cleanconnect-pro",
            "seo_master_index": "00_SEO_Master_Index.md",
            "quantumforge_labs": "QuantumForgeLabs Portfolio Starter",
        }

        return system_paths.get(system_key)

    def _is_content_file(self, filename: str) -> bool:
        """Check if a file is a content file"""
        content_extensions = {
            ".md",
            ".txt",
            ".html",
            ".py",
            ".js",
            ".json",
            ".yml",
            ".yaml",
        }
        return any(filename.lower().endswith(ext) for ext in content_extensions)

    def _extract_content(self, file_path: str) -> Optional[str]:
        """Extract content from a file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return None

    def _extract_title(self, content: str, filename: str) -> str:
        """Extract title from content or filename"""
        # Try to extract from markdown header
        if content.startswith("#"):
            lines = content.split("\n")
            for line in lines[:5]:  # Check first 5 lines
                if line.strip().startswith("#"):
                    return line.strip().lstrip("#").strip()

        # Try to extract from HTML title
        title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()

        # Use filename as fallback
        return os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title()

    def _get_content_type(self, filename: str) -> str:
        """Get content type from filename"""
        ext = os.path.splitext(filename)[1].lower()

        type_mapping = {
            ".md": "markdown",
            ".txt": "text",
            ".html": "html",
            ".py": "python",
            ".js": "javascript",
            ".json": "json",
            ".yml": "yaml",
            ".yaml": "yaml",
        }

        return type_mapping.get(ext, "unknown")

    def _calculate_hash(self, content: str) -> str:
        """Calculate hash for content"""
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def _calculate_seo_score(self, content: str) -> float:
        """Calculate SEO score for content'\''
        try:
            score = 0.0

            # Check for title
            if re.search(r"<title>", content, re.IGNORECASE) or re.search(
                r"^#\s+", content
            ):
                score += 20

            # Check for meta description
            if re.search(r"<meta.*description", content, re.IGNORECASE):
                score += 15

            # Check for headings
            heading_count = len(re.findall(r"<h[1-6]>", content, re.IGNORECASE)) + len(
                re.findall(r"^#+\s+", content)
            )
            score += min(heading_count * 5, 25)

            # Check for images with alt text
            alt_text_count = len(re.findall(r"<img[^>]*alt=", content, re.IGNORECASE))
            score += min(alt_text_count * 3, 15)

            # Check for internal links
            internal_links = len(
                re.findall(r'href=[""\'](?!http)', content, re.IGNORECASE)
            )
            score += min(internal_links * 2, 10)

            # Check for content length
            word_count = len(content.split())
            if word_count > 300:
                score += 15
            elif word_count > 150:
                score += 10

            return min(score, 100.0)

        except Exception as e:
            logger.warning(f"Failed to calculate SEO score: {e}")
            return 0.0

    def _find_duplicates(self) -> List[DuplicateGroup]:
        """Find duplicate content across all systems"""
        try:
            duplicates = []

            # Get all content items
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, content, content_type, system, file_path, hash, seo_score
                FROM content_items
                ORDER BY hash
            """)

            items = cursor.fetchall()
            conn.close()

            # Group by hash
            hash_groups = {}
            for item in items:
                hash_val = item[6]
                if hash_val not in hash_groups:
                    hash_groups[hash_val] = []
                hash_groups[hash_val].append(item)

            # Create duplicate groups
            for hash_val, group_items in hash_groups.items():
                if len(group_items) > 1:
                    content_items = []
                    for item in group_items:
                        content_item = ContentItem(
                            id=item[0],
                            title=item[1],
                            content=item[2],
                            content_type=item[3],
                            system=item[4],
                            file_path=item[5],
                            hash=item[6],
                            seo_score=item[7],
                            last_updated=datetime.datetime.now().isoformat(),
                            status="active",
                        )
                        content_items.append(content_item)

                    # Calculate similarity score
                    similarity_score = self._calculate_similarity_score(content_items)

                    # Determine recommended action
                    recommended_action = self._determine_recommended_action(
                        content_items, similarity_score
                    )

                    duplicate_group = DuplicateGroup(
                        id=f"duplicate_{len(duplicates)}",
                        items=content_items,
                        similarity_score=similarity_score,
                        recommended_action=recommended_action,
                    )

                    duplicates.append(duplicate_group)

            return duplicates

        except Exception as e:
            logger.error(f"Failed to find duplicates: {e}")
            return []

    def _calculate_similarity_score(self, items: List[ContentItem]) -> float:
        """Calculate similarity score for a group of items"""
        if len(items) < 2:
            return 0.0

        # Simple similarity based on content length and title similarity
        content_lengths = [len(item.content) for item in items]
        avg_length = sum(content_lengths) / len(content_lengths)

        length_variance = sum(
            (length - avg_length) ** 2 for length in content_lengths
        ) / len(content_lengths)
        length_similarity = max(0, 100 - (length_variance / avg_length * 100))

        return min(length_similarity, 100.0)

    def _determine_recommended_action(:
        self, items: List[ContentItem], similarity_score: float
    ) -> str:
        """Determine recommended action for duplicate group"""
        if similarity_score > 90:
            return "merge_and_keep_best"
        elif similarity_score > 70:
            return "consolidate_content"
        elif similarity_score > 50:
            return "cross_reference"
        else:
            return "review_manually"

    def _generate_recommendations(:
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate optimization recommendations"""
        recommendations = []

        try:
            # Check for duplicate content
            if analysis_results["duplicates_found"] > 0:
                recommendations.append(
                    {
                        "type": "duplicate_content",
                        "count": analysis_results["duplicates_found"],
                        "recommendation": f"Found {analysis_results['duplicates_found']} duplicate content groups. Consider consolidating or cross-referencing.",
                    }
                )

            # Check for SEO optimization opportunities
            total_items = analysis_results["total_content_items"]
            if total_items > 0:
                recommendations.append(
                    {
                        "type": "seo_optimization",
                        "count": total_items,
                        "recommendation": f"Optimize SEO for {total_items} content items across all systems.",
                    }
                )

            # Check for cross-system opportunities
            systems = analysis_results["system_breakdown"]
            if len(systems) > 1:
                recommendations.append(
                    {
                        "type": "cross_system_integration",
                        "count": len(systems),
                        "recommendation": f"Integrate content across {len(systems)} systems for better user experience.",
                    }
                )

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")

        return recommendations

    def generate_content_report(self) -> str:
        """Generate comprehensive content analysis report"""
        try:
            analysis = self.analyze_all_content()

            report = f"""
# 📚 Content Management Report - Digital Empire
# Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Content Overview
- **Total Files**: {analysis.get("total_files", 0):,}
- **Total Content Items**: {analysis.get("total_content_items", 0):,}
- **Duplicates Found**: {analysis.get("duplicates_found", 0)}
- **SEO Opportunities**: {analysis.get("seo_optimization_opportunities", 0)}

## 🏢 Content by System
"""

            for system_name, system_data in analysis.get(
                "system_breakdown", {}
            ).items():
                report += f"""
### {system_name}
- **Files**: {system_data.get("total_files", 0):,}
- **Content Items**: {system_data.get("total_content_items", 0):,}
- **Content Types**: {", ".join(f"{k}: {v}" for k, v in system_data.get("content_types", {}).items())}
"""

            report += """
## 🔄 Duplicate Content Groups
"""

            for i, group in enumerate(
                analysis.get("duplicate_groups", [])[:10]
            ):  # Show first 10
                report += f"""
### Group {i + 1} (Similarity: {group.similarity_score:.1f}%)
- **Action**: {group.recommended_action}
- **Items**: {len(group.items)}
- **Systems**: {", ".join(set(item.system for item in group.items))}
"""

            report += """
## 🚀 Optimization Recommendations
"""

            for rec in analysis.get("recommendations", []):
                report += f"- **{rec['type'].replace('_', ' ').title()}**: {rec['recommendation']}\n"

            report += """
## 📈 Next Steps
1. Review and resolve duplicate content
2. Optimize SEO across all content
3. Implement cross-system content sharing
4. Set up automated content updates
5. Monitor content performance

---
*Generated by Content Management System*
"""

            return report

        except Exception as e:
            logger.error(f"Failed to generate content report: {e}")
            return f"Error generating report: {e}"


def main():
    """Main function for content management system"""
    try:
        print("📚 Content Management System - Digital Empire")
        print("=" * 50)

        cms = ContentManagementSystem()

        # Analyze all content
        print("Analyzing content across all systems...")
        analysis = cms.analyze_all_content()

        print("✅ Analysis complete!")
        print(f"   Total files: {analysis.get('total_files', 0):,}")
        print(f"   Content items: {analysis.get('total_content_items', 0):,}")
        print(f"   Duplicates found: {analysis.get('duplicates_found', 0)}")

        # Generate report
        report = cms.generate_content_report()
        print("\nGenerating content report...")

        # Save report
        with open("content_management_report.md", "w") as f:
            f.write(report)

        print("✅ Content report saved to content_management_report.md")

    except Exception as e:
        logger.error(f"Main function failed: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
