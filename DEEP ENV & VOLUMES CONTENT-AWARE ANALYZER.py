#!/usr/bin/env python3
"""
🔍 DEEP ENV & VOLUMES CONTENT-AWARE ANALYZER
Comprehensive intelligent analysis of .env.d and /Volumes directories

Features:
- Environment variable and API key analysis (secure, no exposure)
- Multi-volume content-aware scanning
- File type distribution and patterns
- Content intelligence (metadata, relationships)
- Security audit (key validation, patterns)
- Resource mapping and opportunities
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import hashlib
import mimetypes
import subprocess

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from advanced_toolkit.file_intelligence import FileAnalyzer
    from advanced_toolkit.config_manager import ConfigManager
except ImportError:
    FileAnalyzer = None
    ConfigManager = None


@dataclass
class EnvFileAnalysis:
    """Analysis of an environment file"""

    filepath: str
    service_count: int
    api_keys: List[str]  # Just key names, not values
    services: List[str]
    file_size: int
    last_modified: datetime
    security_level: str  # "secure", "warning", "critical"
    issues: List[str]
    opportunities: List[str]


@dataclass
class VolumeAnalysis:
    """Analysis of a volume"""

    volume_name: str
    total_files: int
    total_size: int
    file_types: Dict[str, int]
    largest_files: List[Dict[str, Any]]
    directory_structure: Dict[str, int]
    content_categories: Dict[str, int]
    duplicates: List[str]
    opportunities: List[str]
    intelligence: Dict[str, Any]


@dataclass
class ComprehensiveAnalysis:
    """Complete analysis report"""

    env_analysis: Dict[str, EnvFileAnalysis]
    volumes_analysis: Dict[str, VolumeAnalysis]
    api_services: Set[str]
    total_api_keys: int
    security_issues: List[str]
    opportunities: List[str]
    resource_mapping: Dict[str, Any]
    recommendations: List[str]


class DeepEnvVolumesAnalyzer:
    """Deep content-aware analyzer for .env.d and volumes"""

    def __init__(self):
        self.env_dir = Path.home() / ".env.d"
        self.volumes_dir = Path("/Volumes")
        # FileAnalyzer requires db_path, so we'll skip it for now
        self.file_analyzer = None
        self.config_manager = ConfigManager() if ConfigManager else None

        # Known API service patterns
        self.api_patterns = {
            "openai": ["OPENAI_API_KEY", "OPENAI_ORG_ID"],
            "anthropic": ["ANTHROPIC_API_KEY", "CLAUDE_API_KEY"],
            "google": [
                "GOOGLE_API_KEY",
                "GEMINI_API_KEY",
                "GOOGLE_APPLICATION_CREDENTIALS",
            ],
            "groq": ["GROQ_API_KEY"],
            "xai": ["XAI_API_KEY", "GROK_API_KEY"],
            "perplexity": ["PERPLEXITY_API_KEY"],
            "cohere": ["COHERE_API_KEY"],
            "deepseek": ["DEEPSEEK_API_KEY"],
            "mistral": ["MISTRAL_API_KEY"],
            "together": ["TOGETHER_API_KEY"],
            "cerebras": ["CEREBRAS_API_KEY"],
            "openrouter": ["OPENROUTER_API_KEY"],
            "huggingface": ["HUGGINGFACE_API_KEY", "HF_TOKEN"],
            "replicate": ["REPLICATE_API_TOKEN"],
            "stability": ["STABILITY_API_KEY", "STABLE_DIFFUSION_API_KEY"],
            "elevenlabs": ["ELEVENLABS_API_KEY"],
            "suno": ["SUNO_API_KEY"],
            "make": ["MAKE_API_KEY", "MAKE_WEBHOOK_URL"],
            "n8n": ["N8N_API_KEY", "N8N_WEBHOOK_URL"],
            "airtable": ["AIRTABLE_API_KEY", "AIRTABLE_BASE_ID"],
            "notion": ["NOTION_API_KEY"],
            "discord": ["DISCORD_BOT_TOKEN", "DISCORD_WEBHOOK_URL"],
            "slack": ["SLACK_BOT_TOKEN", "SLACK_WEBHOOK_URL"],
            "twitter": ["TWITTER_API_KEY", "TWITTER_BEARER_TOKEN", "X_API_KEY"],
            "youtube": ["YOUTUBE_API_KEY", "YOUTUBE_CLIENT_ID"],
            "instagram": ["INSTAGRAM_ACCESS_TOKEN"],
            "tiktok": ["TIKTOK_ACCESS_TOKEN"],
            "stripe": ["STRIPE_API_KEY", "STRIPE_SECRET_KEY"],
            "paypal": ["PAYPAL_CLIENT_ID", "PAYPAL_SECRET"],
            "aws": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
            "azure": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"],
            "database": ["DATABASE_URL", "POSTGRES_URL", "MONGODB_URI"],
            "redis": ["REDIS_URL", "REDIS_HOST"],
            "s3": ["S3_BUCKET", "S3_ACCESS_KEY", "S3_SECRET_KEY"],
            "cloudflare": ["CLOUDFLARE_API_KEY", "CLOUDFLARE_ZONE_ID"],
            "vercel": ["VERCEL_API_TOKEN"],
            "netlify": ["NETLIFY_API_TOKEN"],
            "github": ["GITHUB_TOKEN", "GITHUB_PAT"],
            "gitlab": ["GITLAB_TOKEN"],
            "bitbucket": ["BITBUCKET_APP_PASSWORD"],
        }

    def analyze_all(self) -> ComprehensiveAnalysis:
        """Perform comprehensive analysis"""
        print("🔍 DEEP CONTENT-AWARE ANALYSIS")
        print("=" * 70)
        print()

        # Analyze .env.d
        print("1️⃣  Analyzing .env.d directory...")
        env_analysis = self.analyze_env_directory()

        # Analyze volumes
        print("\n2️⃣  Analyzing volumes...")
        volumes_analysis = self.analyze_volumes()

        # Generate insights
        print("\n3️⃣  Generating insights...")
        insights = self.generate_insights(env_analysis, volumes_analysis)

        return ComprehensiveAnalysis(
            env_analysis=env_analysis,
            volumes_analysis=volumes_analysis,
            api_services=insights["api_services"],
            total_api_keys=insights["total_api_keys"],
            security_issues=insights["security_issues"],
            opportunities=insights["opportunities"],
            resource_mapping=insights["resource_mapping"],
            recommendations=insights["recommendations"],
        )

    def analyze_env_directory(self) -> Dict[str, EnvFileAnalysis]:
        """Analyze all environment files"""
        env_files = {}

        if not self.env_dir.exists():
            print(f"   ⚠️  {self.env_dir} not found")
            return env_files

        # Find all .env files
        env_file_paths = list(self.env_dir.glob("*.env"))
        env_file_paths.extend(list(self.env_dir.glob("*.env.bak")))

        print(f"   Found {len(env_file_paths)} environment files")

        for env_file in env_file_paths:
            try:
                analysis = self.analyze_env_file(env_file)
                env_files[str(env_file.name)] = analysis
                print(
                    f"   ✅ {env_file.name}: {analysis.service_count} services, {len(analysis.api_keys)} keys"
                )
            except Exception as e:
                print(f"   ⚠️  Error analyzing {env_file.name}: {e}")

        return env_files

    def analyze_env_file(self, filepath: Path) -> EnvFileAnalysis:
        """Analyze a single environment file"""
        services = []
        api_keys = []
        issues = []
        opportunities = []

        try:
            with open(filepath, "r") as f:
                content = f.read()

            # Extract API keys (names only, not values)
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")

                    # Identify service
                    service = self.identify_service(key)
                    if service:
                        services.append(service)
                        api_keys.append(key)

                    # Check for issues
                    if not value or value == "":
                        issues.append(f"Empty value for {key}")
                    elif len(value) < 10:
                        issues.append(f"Potentially invalid key: {key} (too short)")

            # Identify services
            unique_services = list(set(services))

            # Security assessment
            security_level = "secure"
            if issues:
                security_level = "warning" if len(issues) < 5 else "critical"

            # Opportunities
            if "openai" in unique_services and "anthropic" not in unique_services:
                opportunities.append(
                    "Consider adding Claude API for multi-model support"
                )
            if "groq" in unique_services and "xai" not in unique_services:
                opportunities.append("Consider adding Grok API for real-time trends")

            # File stats
            stat = filepath.stat()

            return EnvFileAnalysis(
                filepath=str(filepath),
                service_count=len(unique_services),
                api_keys=api_keys,
                services=unique_services,
                file_size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                security_level=security_level,
                issues=issues,
                opportunities=opportunities,
            )
        except Exception as e:
            return EnvFileAnalysis(
                filepath=str(filepath),
                service_count=0,
                api_keys=[],
                services=[],
                file_size=0,
                last_modified=datetime.now(),
                security_level="error",
                issues=[f"Error reading file: {e}"],
                opportunities=[],
            )

    def identify_service(self, key: str) -> Optional[str]:
        """Identify API service from key name"""
        key_upper = key.upper()

        for service, patterns in self.api_patterns.items():
            for pattern in patterns:
                if pattern.upper() in key_upper:
                    return service

        return None

    def analyze_volumes(self) -> Dict[str, VolumeAnalysis]:
        """Analyze all volumes"""
        volumes_analysis = {}

        if not self.volumes_dir.exists():
            print(f"   ⚠️  {self.volumes_dir} not found")
            return volumes_analysis

        # Get volume directories (exclude system volumes)
        volumes = [
            v
            for v in self.volumes_dir.iterdir()
            if v.is_dir()
            and not v.name.startswith(".")
            and v.name not in ["Macintosh HD", "Preboot", "Recovery"]
        ]

        print(f"   Found {len(volumes)} volumes to analyze")

        for volume in volumes:
            try:
                print(f"   📦 Analyzing {volume.name}...")
                analysis = self.analyze_volume(volume)
                volumes_analysis[volume.name] = analysis
                print(
                    f"      ✅ {analysis.total_files:,} files, {self._format_size(analysis.total_size)}"
                )
            except Exception as e:
                print(f"      ⚠️  Error analyzing {volume.name}: {e}")

        return volumes_analysis

    def analyze_volume(self, volume_path: Path) -> VolumeAnalysis:
        """Deep content-aware analysis of a volume"""
        file_types = defaultdict(int)
        largest_files = []
        directory_structure = defaultdict(int)
        content_categories = defaultdict(int)
        duplicates = []
        opportunities = []

        total_files = 0
        total_size = 0

        # Walk through volume (limit depth for performance)
        try:
            for root, dirs, files in os.walk(str(volume_path), followlinks=False):
                # Limit depth
                depth = root.replace(str(volume_path), "").count(os.sep)
                if depth > 5:  # Limit to 5 levels deep
                    dirs[:] = []
                    continue

                # Analyze directories
                for d in dirs:
                    dir_path = Path(root) / d
                    directory_structure[d] += 1

                # Analyze files
                for f in files:
                    file_path = Path(root) / f

                    try:
                        if not file_path.exists():
                            continue

                        stat = file_path.stat()
                        file_size = stat.st_size
                        total_size += file_size
                        total_files += 1

                        # File type
                        ext = file_path.suffix.lower()
                        if ext:
                            file_types[ext] += 1
                        else:
                            file_types["no_extension"] += 1

                        # Content category
                        category = self.categorize_file(file_path, ext)
                        content_categories[category] += 1

                        # Track largest files
                        if file_size > 10 * 1024 * 1024:  # > 10MB
                            largest_files.append(
                                {
                                    "path": str(file_path.relative_to(volume_path)),
                                    "size": file_size,
                                    "type": ext,
                                    "category": category,
                                }
                            )

                        # Limit processing for performance
                        if total_files > 100000:  # Limit to 100k files
                            break

                    except (OSError, PermissionError):
                        continue

                if total_files > 100000:
                    break

        except (OSError, PermissionError) as e:
            print(f"      ⚠️  Permission error: {e}")

        # Sort largest files
        largest_files.sort(key=lambda x: x["size"], reverse=True)
        largest_files = largest_files[:50]  # Top 50

        # Generate opportunities
        if "python" in str(volume_path).lower() or ".py" in file_types:
            opportunities.append(
                "Python scripts detected - potential automation opportunities"
            )
        audio_exts = {".mp3", ".wav", ".flac"}
        image_exts = {".jpg", ".png", ".svg"}
        video_exts = {".mp4", ".mov"}
        if audio_exts.intersection(file_types.keys()):
            opportunities.append(
                "Audio files detected - music management system integration"
            )
        if image_exts.intersection(file_types.keys()):
            opportunities.append(
                "Image files detected - art gallery or print-on-demand opportunities"
            )
        if video_exts.intersection(file_types.keys()):
            opportunities.append(
                "Video files detected - content creation opportunities"
            )

        # Intelligence summary
        intelligence = {
            "dominant_file_type": (
                max(file_types.items(), key=lambda x: x[1])[0] if file_types else None
            ),
            "dominant_category": (
                max(content_categories.items(), key=lambda x: x[1])[0]
                if content_categories
                else None
            ),
            "avg_file_size": total_size / total_files if total_files > 0 else 0,
            "depth_analysis": dict(directory_structure),
        }

        return VolumeAnalysis(
            volume_name=volume_path.name,
            total_files=total_files,
            total_size=total_size,
            file_types=dict(file_types),
            largest_files=largest_files,
            directory_structure=dict(directory_structure),
            content_categories=dict(content_categories),
            duplicates=duplicates,
            opportunities=opportunities,
            intelligence=intelligence,
        )

    def categorize_file(self, filepath: Path, ext: str) -> str:
        """Categorize file by content type"""
        ext_lower = ext.lower()

        # Audio
        if ext_lower in [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"]:
            return "audio"

        # Video
        if ext_lower in [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"]:
            return "video"

        # Images
        if ext_lower in [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".webp",
            ".bmp",
            ".tiff",
        ]:
            return "image"

        # Documents
        if ext_lower in [".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"]:
            return "document"

        # Code
        if ext_lower in [
            ".py",
            ".js",
            ".ts",
            ".html",
            ".css",
            ".json",
            ".xml",
            ".yaml",
            ".yml",
        ]:
            return "code"

        # Archives
        if ext_lower in [".zip", ".tar", ".gz", ".rar", ".7z"]:
            return "archive"

        # Data
        if ext_lower in [".csv", ".xlsx", ".xls", ".db", ".sqlite", ".sql"]:
            return "data"

        # Other
        return "other"

    def generate_insights(
        self,
        env_analysis: Dict[str, EnvFileAnalysis],
        volumes_analysis: Dict[str, VolumeAnalysis],
    ) -> Dict[str, Any]:
        """Generate comprehensive insights"""

        # API Services
        all_services = set()
        total_keys = 0
        for analysis in env_analysis.values():
            all_services.update(analysis.services)
            total_keys += len(analysis.api_keys)

        # Security Issues
        security_issues = []
        for name, analysis in env_analysis.items():
            if analysis.security_level == "critical":
                security_issues.append(
                    f"Critical issues in {name}: {len(analysis.issues)} issues"
                )
            for issue in analysis.issues:
                security_issues.append(f"{name}: {issue}")

        # Opportunities
        opportunities = []

        # API opportunities
        if "openai" in all_services and "anthropic" not in all_services:
            opportunities.append("Add Claude API for multi-model AI orchestration")
        if "groq" in all_services and "xai" not in all_services:
            opportunities.append("Add Grok API for real-time trending content")
        if "openai" in all_services and "perplexity" not in all_services:
            opportunities.append("Add Perplexity API for search trend analysis")

        # Volume opportunities
        for vol_name, vol_analysis in volumes_analysis.items():
            opportunities.extend(vol_analysis.opportunities)

            # Specific opportunities based on content
            if vol_analysis.content_categories.get("audio", 0) > 100:
                opportunities.append(
                    f"{vol_name}: Large audio collection - integrate with music management system"
                )
            if vol_analysis.content_categories.get("image", 0) > 100:
                opportunities.append(
                    f"{vol_name}: Large image collection - art gallery or print-on-demand potential"
                )
            if vol_analysis.content_categories.get("code", 0) > 50:
                opportunities.append(
                    f"{vol_name}: Code files detected - automation script opportunities"
                )

        # Resource Mapping
        resource_mapping = {
            "api_services": set(all_services),
            "total_env_files": len(env_analysis),
            "total_volumes": len(volumes_analysis),
            "total_files_across_volumes": sum(
                v.total_files for v in volumes_analysis.values()
            ),
            "total_size_across_volumes": sum(
                v.total_size for v in volumes_analysis.values()
            ),
            "content_distribution": {},
        }

        # Content distribution
        for vol_name, vol_analysis in volumes_analysis.items():
            resource_mapping["content_distribution"][
                vol_name
            ] = vol_analysis.content_categories

        # Recommendations
        recommendations = []

        # Security
        if security_issues:
            recommendations.append(
                "Review and fix security issues in environment files"
            )

        # Organization
        if len(env_analysis) > 10:
            recommendations.append(
                "Consider consolidating environment files for easier management"
            )

        # Integration
        if all_services:
            recommendations.append(
                f"Leverage {len(all_services)} API services for multi-AI orchestration"
            )

        # Content
        total_audio = sum(
            v.content_categories.get("audio", 0) for v in volumes_analysis.values()
        )
        total_images = sum(
            v.content_categories.get("image", 0) for v in volumes_analysis.values()
        )
        if total_audio > 100:
            recommendations.append(
                f"Integrate {total_audio:,} audio files with music management system"
            )
        if total_images > 100:
            recommendations.append(
                f"Integrate {total_images:,} images with art gallery or print-on-demand system"
            )

        return {
            "api_services": set(all_services),
            "total_api_keys": total_keys,
            "security_issues": security_issues,
            "opportunities": opportunities,
            "resource_mapping": resource_mapping,
            "recommendations": recommendations,
        }

    def _format_size(self, size: int) -> str:
        """Format file size"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def save_analysis(self, analysis: ComprehensiveAnalysis, output_path: Path):
        """Save analysis to JSON and Markdown"""
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON export
        json_data = {
            "timestamp": timestamp,
            "env_analysis": {
                name: {
                    "filepath": a.filepath,
                    "service_count": a.service_count,
                    "services": a.services,
                    "api_key_count": len(a.api_keys),
                    "security_level": a.security_level,
                    "issues_count": len(a.issues),
                    "opportunities": a.opportunities,
                }
                for name, a in analysis.env_analysis.items()
            },
            "volumes_analysis": {
                name: {
                    "total_files": v.total_files,
                    "total_size": v.total_size,
                    "file_types": v.file_types,
                    "content_categories": v.content_categories,
                    "opportunities": v.opportunities,
                    "intelligence": v.intelligence,
                }
                for name, v in analysis.volumes_analysis.items()
            },
            "summary": {
                "total_api_services": len(analysis.api_services),
                "total_api_keys": analysis.total_api_keys,
                "security_issues_count": len(analysis.security_issues),
                "opportunities_count": len(analysis.opportunities),
                "recommendations_count": len(analysis.recommendations),
            },
        }

        json_file = output_path / f"env_volumes_analysis_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f, indent=2, default=str)

        # Markdown report
        md_file = output_path / f"ENV_VOLUMES_ANALYSIS_{timestamp}.md"
        with open(md_file, "w") as f:
            f.write(self.generate_markdown_report(analysis, timestamp))

        print(f"\n💾 Analysis saved:")
        print(f"   - JSON: {json_file.name}")
        print(f"   - Markdown: {md_file.name}")

    def generate_markdown_report(
        self, analysis: ComprehensiveAnalysis, timestamp: str
    ) -> str:
        """Generate comprehensive Markdown report"""
        report = f"""# 🔍 DEEP ENV & VOLUMES CONTENT-AWARE ANALYSIS
## Comprehensive Intelligence Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
**Analysis ID:** {timestamp}

---

## 📊 EXECUTIVE SUMMARY

### Environment Files (.env.d)
- **Total Files Analyzed:** {len(analysis.env_analysis)}
- **Total API Services:** {len(analysis.api_services)}
- **Total API Keys:** {analysis.total_api_keys}
- **Security Issues:** {len(analysis.security_issues)}

### Volumes Analysis
- **Volumes Analyzed:** {len(analysis.volumes_analysis)}
- **Total Files:** {sum(v.total_files for v in analysis.volumes_analysis.values()):,}
- **Total Size:** {self._format_size(sum(v.total_size for v in analysis.volumes_analysis.values()))}

---

## 🔐 ENVIRONMENT FILES ANALYSIS

"""

        for name, env in analysis.env_analysis.items():
            report += f"""### {name}

**Services:** {', '.join(env.services) if env.services else 'None'}
**API Keys:** {len(env.api_keys)}
**Security Level:** {env.security_level.upper()}
**Issues:** {len(env.issues)}
**Opportunities:** {len(env.opportunities)}

"""
            if env.issues:
                report += "**Issues:**\n"
                for issue in env.issues[:5]:  # Limit to 5
                    report += f"- {issue}\n"
                report += "\n"

            if env.opportunities:
                report += "**Opportunities:**\n"
                for opp in env.opportunities:
                    report += f"- {opp}\n"
                report += "\n"

        report += f"""
---

## 💾 VOLUMES ANALYSIS

"""

        for vol_name, vol in analysis.volumes_analysis.items():
            report += f"""### {vol_name}

**Total Files:** {vol.total_files:,}
**Total Size:** {self._format_size(vol.total_size)}
**Dominant File Type:** {vol.intelligence.get('dominant_file_type', 'N/A')}
**Dominant Category:** {vol.intelligence.get('dominant_category', 'N/A')}

#### Content Distribution
"""
            for category, count in sorted(
                vol.content_categories.items(), key=lambda x: x[1], reverse=True
            )[:10]:
                report += f"- **{category.title()}:** {count:,} files\n"

            report += "\n#### Top File Types\n"
            for ext, count in sorted(
                vol.file_types.items(), key=lambda x: x[1], reverse=True
            )[:10]:
                report += f"- **{ext or 'no extension'}:** {count:,} files\n"

            if vol.opportunities:
                report += "\n#### Opportunities\n"
                for opp in vol.opportunities:
                    report += f"- {opp}\n"

            report += "\n"

        report += f"""
---

## 🎯 API SERVICES INVENTORY

**Total Services:** {len(analysis.api_services)}

### Services Detected:
"""
        for service in sorted(analysis.api_services):
            report += f"- {service.title()}\n"

        report += f"""
---

## ⚠️ SECURITY ISSUES

**Total Issues:** {len(analysis.security_issues)}

"""
        for issue in analysis.security_issues[:20]:  # Limit to 20
            report += f"- {issue}\n"

        if len(analysis.security_issues) > 20:
            report += f"\n*... and {len(analysis.security_issues) - 20} more issues*\n"

        report += f"""
---

## 💡 OPPORTUNITIES

**Total Opportunities:** {len(analysis.opportunities)}

"""
        for opp in analysis.opportunities:
            report += f"- {opp}\n"

        report += f"""
---

## 📋 RECOMMENDATIONS

"""
        for rec in analysis.recommendations:
            report += f"- {rec}\n"

        report += f"""
---

## 🔗 RESOURCE MAPPING

### Content Distribution Across Volumes

"""
        for vol_name, categories in analysis.resource_mapping.get(
            "content_distribution", {}
        ).items():
            report += f"#### {vol_name}\n"
            for category, count in sorted(
                categories.items(), key=lambda x: x[1], reverse=True
            ):
                report += f"- {category.title()}: {count:,} files\n"
            report += "\n"

        report += f"""
---

**Analysis Complete** ✅

*This report was generated using deep content-aware analysis techniques.*
"""

        return report


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Deep ENV & Volumes Analyzer")
    parser.add_argument(
        "--output", default="~/analysis_reports", help="Output directory for reports"
    )
    parser.add_argument("--json-only", action="store_true", help="Generate JSON only")
    parser.add_argument("--md-only", action="store_true", help="Generate Markdown only")

    args = parser.parse_args()

    analyzer = DeepEnvVolumesAnalyzer()

    # Perform analysis
    analysis = analyzer.analyze_all()

    # Print summary
    print("\n" + "=" * 70)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"\nEnvironment Files: {len(analysis.env_analysis)}")
    print(f"API Services: {len(analysis.api_services)}")
    print(f"Total API Keys: {analysis.total_api_keys}")
    print(f"Volumes Analyzed: {len(analysis.volumes_analysis)}")
    print(
        f"Total Files: {sum(v.total_files for v in analysis.volumes_analysis.values()):,}"
    )
    print(f"Security Issues: {len(analysis.security_issues)}")
    print(f"Opportunities: {len(analysis.opportunities)}")
    print(f"Recommendations: {len(analysis.recommendations)}")

    # Save analysis
    if not args.md_only:
        output_dir = Path(args.output).expanduser()
        analyzer.save_analysis(analysis, output_dir)

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
