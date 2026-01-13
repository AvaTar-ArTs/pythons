<!-- 🔍 DEEP ENV & VOLUMES CONTENT-AWARE ANALYZER
Organized, sorted, and improved analysis of .env.d and /Volumes directories. -->

#!/usr/bin/env python3

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import hashlib
import mimetypes
import subprocess

# Ensure parent directory is available for imports

sys.path.insert(0, str(Path(**file**).parent))

# Optional imports from advanced_toolkit (handle gracefully)

try:
from advanced_toolkit.file_intelligence import FileAnalyzer
from advanced_toolkit.config_manager import ConfigManager
except ImportError:
FileAnalyzer = None
ConfigManager = None

# =======================

# Data Classes & Types

# =======================

@dataclass
class EnvFileAnalysis:
filepath: str
service_count: int
api_keys: List[str]
services: List[str]
file_size: int
last_modified: datetime
security_level: str # "secure", "warning", "critical", "error"
issues: List[str]
opportunities: List[str]

@dataclass
class VolumeAnalysis:
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
env_analysis: Dict[str, EnvFileAnalysis]
volumes_analysis: Dict[str, VolumeAnalysis]
api_services: Set[str]
total_api_keys: int
security_issues: List[str]
opportunities: List[str]
resource_mapping: Dict[str, Any]
recommendations: List[str]

# =======================

# Analyzer Class

# =======================

class DeepEnvVolumesAnalyzer:
def **init**(self):
self.env_dir = Path.home() / '.env.d'
self.volumes_dir = Path('/Volumes')
self.file_analyzer = None
self.config_manager = ConfigManager() if ConfigManager else None

        # Sorted API patterns
        self.api_patterns = dict(sorted({
            'airtable':      ['AIRTABLE_API_KEY', 'AIRTABLE_BASE_ID'],
            'anthropic':     ['ANTHROPIC_API_KEY', 'CLAUDE_API_KEY'],
            'aws':           ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'],
            'azure':         ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT'],
            'bitbucket':     ['BITBUCKET_APP_PASSWORD'],
            'cerebras':      ['CEREBRAS_API_KEY'],
            'cloudflare':    ['CLOUDFLARE_API_KEY', 'CLOUDFLARE_ZONE_ID'],
            'cohere':        ['COHERE_API_KEY'],
            'database':      ['DATABASE_URL', 'POSTGRES_URL', 'MONGODB_URI'],
            'deepseek':      ['DEEPSEEK_API_KEY'],
            'discord':       ['DISCORD_BOT_TOKEN', 'DISCORD_WEBHOOK_URL'],
            'elevenlabs':    ['ELEVENLABS_API_KEY'],
            'github':        ['GITHUB_TOKEN', 'GITHUB_PAT'],
            'gitlab':        ['GITLAB_TOKEN'],
            'google':        ['GOOGLE_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS'],
            'groq':          ['GROQ_API_KEY'],
            'huggingface':   ['HUGGINGFACE_API_KEY', 'HF_TOKEN'],
            'instagram':     ['INSTAGRAM_ACCESS_TOKEN'],
            'make':          ['MAKE_API_KEY', 'MAKE_WEBHOOK_URL'],
            'mistral':       ['MISTRAL_API_KEY'],
            'netlify':       ['NETLIFY_API_TOKEN'],
            'n8n':           ['N8N_API_KEY', 'N8N_WEBHOOK_URL'],
            'notion':        ['NOTION_API_KEY'],
            'openai':        ['OPENAI_API_KEY', 'OPENAI_ORG_ID'],
            'openrouter':    ['OPENROUTER_API_KEY'],
            'paypal':        ['PAYPAL_CLIENT_ID', 'PAYPAL_SECRET'],
            'perplexity':    ['PERPLEXITY_API_KEY'],
            'redis':         ['REDIS_URL', 'REDIS_HOST'],
            'replicate':     ['REPLICATE_API_TOKEN'],
            's3':            ['S3_BUCKET', 'S3_ACCESS_KEY', 'S3_SECRET_KEY'],
            'slack':         ['SLACK_BOT_TOKEN', 'SLACK_WEBHOOK_URL'],
            'stability':     ['STABILITY_API_KEY', 'STABLE_DIFFUSION_API_KEY'],
            'stripe':        ['STRIPE_API_KEY', 'STRIPE_SECRET_KEY'],
            'suno':          ['SUNO_API_KEY'],
            'tiktok':        ['TIKTOK_ACCESS_TOKEN'],
            'together':      ['TOGETHER_API_KEY'],
            'twitter':       ['TWITTER_API_KEY', 'TWITTER_BEARER_TOKEN', 'X_API_KEY'],
            'vercel':        ['VERCEL_API_TOKEN'],
            'xai':           ['XAI_API_KEY', 'GROK_API_KEY'],
            'youtube':       ['YOUTUBE_API_KEY', 'YOUTUBE_CLIENT_ID'],
        }.items()))

    def analyze_all(self) -> ComprehensiveAnalysis:
        print("🔍 DEEP CONTENT-AWARE ANALYSIS")
        print("=" * 70)
        print()
        print("1️⃣  Analyzing .env.d directory...")
        env_analysis = self.analyze_env_directory()
        print("\n2️⃣  Analyzing volumes...")
        volumes_analysis = self.analyze_volumes()
        print("\n3️⃣  Generating insights...")
        insights = self.generate_insights(env_analysis, volumes_analysis)
        return ComprehensiveAnalysis(
            env_analysis=env_analysis,
            volumes_analysis=volumes_analysis,
            api_services=insights['api_services'],
            total_api_keys=insights['total_api_keys'],
            security_issues=insights['security_issues'],
            opportunities=insights['opportunities'],
            resource_mapping=insights['resource_mapping'],
            recommendations=insights['recommendations'],
        )

    def analyze_env_directory(self) -> Dict[str, EnvFileAnalysis]:
        env_files: Dict[str, EnvFileAnalysis] = {}
        if not self.env_dir.exists():
            print(f"   ⚠️  {self.env_dir} not found")
            return env_files

        env_file_paths = sorted(list(self.env_dir.glob('*.env')) + list(self.env_dir.glob('*.env.bak')), key=lambda p: p.name)
        print(f"   Found {len(env_file_paths)} environment files")
        for env_file in env_file_paths:
            try:
                analysis = self.analyze_env_file(env_file)
                env_files[env_file.name] = analysis
                print(f"   ✅ {env_file.name}: {analysis.service_count} services, {len(analysis.api_keys)} keys")
            except Exception as e:
                print(f"   ⚠️  Error analyzing {env_file.name}: {e}")
        return env_files

    def analyze_env_file(self, filepath: Path) -> EnvFileAnalysis:
        services: List[str] = []
        api_keys: List[str] = []
        issues: List[str] = []
        opportunities: List[str] = []

        try:
            with open(filepath, "r") as f:
                content = f.read()

            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')

                service = self.identify_service(key)
                if service:
                    services.append(service)
                    api_keys.append(key)

                if not value:
                    issues.append(f"Empty value for {key}")
                elif len(value) < 10:
                    issues.append(f"Potentially invalid key: {key} (too short)")

            unique_services = sorted(set(services))
            if len(issues) >= 5:
                security_level = "critical"
            elif issues:
                security_level = "warning"
            else:
                security_level = "secure"

            # Suggest new API integration
            if 'openai' in unique_services and 'anthropic' not in unique_services:
                opportunities.append("Consider adding Claude API for multi-model support")
            if 'groq' in unique_services and 'xai' not in unique_services:
                opportunities.append("Consider adding Grok API for real-time trends")

            stat = filepath.stat()
            return EnvFileAnalysis(
                filepath=str(filepath),
                service_count=len(unique_services),
                api_keys=sorted(api_keys),
                services=unique_services,
                file_size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                security_level=security_level,
                issues=sorted(issues),
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
                opportunities=[]
            )

    def identify_service(self, key: str) -> Optional[str]:
        key_upper = key.upper()
        for service, patterns in self.api_patterns.items():
            for pattern in patterns:
                if pattern.upper() in key_upper:
                    return service
        return None

    def analyze_volumes(self) -> Dict[str, VolumeAnalysis]:
        volumes_analysis: Dict[str, VolumeAnalysis] = {}
        if not self.volumes_dir.exists():
            print(f"   ⚠️  {self.volumes_dir} not found")
            return volumes_analysis

        volumes = sorted([
            v for v in self.volumes_dir.iterdir()
            if v.is_dir() and not v.name.startswith('.')
               and v.name not in ('Macintosh HD', 'Preboot', 'Recovery')
        ], key=lambda v: v.name)

        print(f"   Found {len(volumes)} volumes to analyze")
        for volume in volumes:
            try:
                print(f"   📦 Analyzing {volume.name}...")
                analysis = self.analyze_volume(volume)
                volumes_analysis[volume.name] = analysis
                print(f"      ✅ {analysis.total_files:,} files, {self._format_size(analysis.total_size)}")
            except Exception as e:
                print(f"      ⚠️  Error analyzing {volume.name}: {e}")

        return volumes_analysis

    def analyze_volume(self, volume_path: Path) -> VolumeAnalysis:
        file_types: Dict[str, int] = defaultdict(int)
        largest_files: List[Dict[str, Any]] = []
        directory_structure: Dict[str, int] = defaultdict(int)
        content_categories: Dict[str, int] = defaultdict(int)
        duplicates: List[str] = []
        opportunities: List[str] = []
        total_files = 0
        total_size = 0

        try:
            for root, dirs, files in os.walk(str(volume_path), followlinks=False):
                # Limit depth to avoid performance bottleneck
                if root.replace(str(volume_path), '').count(os.sep) > 5:
                    dirs.clear()
                    continue

                for d in dirs:
                    directory_structure[d] += 1

                for f in files:
                    file_path = Path(root) / f
                    try:
                        if not file_path.exists():
                            continue
                        stat = file_path.stat()
                        file_size = stat.st_size
                        total_size += file_size
                        total_files += 1

                        ext = file_path.suffix.lower()
                        file_types[ext or "no_extension"] += 1

                        category = self.categorize_file(file_path, ext)
                        content_categories[category] += 1

                        if file_size > 10 * 1024 * 1024:  # >10MB
                            largest_files.append({
                                "path": str(file_path.relative_to(volume_path)),
                                "size": file_size,
                                "type": ext,
                                "category": category,
                            })
                        if total_files > 100_000:  # Protect from deep traversal
                            break
                    except (OSError, PermissionError):
                        continue

                if total_files > 100_000:
                    break

        except (OSError, PermissionError) as e:
            print(f"      ⚠️  Permission error: {e}")

        largest_files = sorted(largest_files, key=lambda x: x['size'], reverse=True)[:50]

        if 'python' in str(volume_path).lower() or '.py' in file_types:
            opportunities.append("Python scripts detected - potential automation opportunities")
        audio_exts = {'.mp3', '.wav', '.flac'}
        image_exts = {'.jpg', '.png', '.svg'}
        video_exts = {'.mp4', '.mov'}
        if audio_exts.intersection(file_types.keys()):
            opportunities.append("Audio files detected - music management system integration")
        if image_exts.intersection(file_types.keys()):
            opportunities.append("Image files detected - art gallery or print-on-demand opportunities")
        if video_exts.intersection(file_types.keys()):
            opportunities.append("Video files detected - content creation opportunities")

        intelligence = {
            "dominant_file_type": max(file_types.items(), key=lambda x: x[1])[0] if file_types else None,
            "dominant_category": max(content_categories.items(), key=lambda x: x[1])[0] if content_categories else None,
            "avg_file_size": total_size / total_files if total_files else 0,
            "depth_analysis": dict(directory_structure),
        }

        return VolumeAnalysis(
            volume_name=volume_path.name,
            total_files=total_files,
            total_size=total_size,
            file_types=dict(sorted(file_types.items())),
            largest_files=largest_files,
            directory_structure=dict(sorted(directory_structure.items())),
            content_categories=dict(sorted(content_categories.items())),
            duplicates=duplicates,
            opportunities=sorted(opportunities),
            intelligence=intelligence,
        )

    def categorize_file(self, filepath: Path, ext: str) -> str:
        ext = ext.lower()
        for cat, exts in [
            ("audio",     {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"}),
            ("video",     {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}),
            ("image",     {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tiff"}),
            ("document",  {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"}),
            ("code",      {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".yml"}),
            ("archive",   {".zip", ".tar", ".gz", ".rar", ".7z"}),
            ("data",      {".csv", ".xlsx", ".xls", ".db", ".sqlite", ".sql"}),
        ]:
            if ext in exts:
                return cat
        return "other"

    def generate_insights(
        self,
        env_analysis: Dict[str, EnvFileAnalysis],
        volumes_analysis: Dict[str, VolumeAnalysis]
    ) -> Dict[str, Any]:

        all_services = {srv for a in env_analysis.values() for srv in a.services}
        total_keys = sum(len(a.api_keys) for a in env_analysis.values())

        security_issues = []
        for name, analysis in env_analysis.items():
            if analysis.security_level == 'critical':
                security_issues.append(f"Critical issues in {name}: {len(analysis.issues)} issues")
            for issue in sorted(analysis.issues):
                security_issues.append(f"{name}: {issue}")

        opportunities = []
        if 'openai' in all_services and 'anthropic' not in all_services:
            opportunities.append("Add Claude API for multi-model AI orchestration")
        if 'groq' in all_services and 'xai' not in all_services:
            opportunities.append("Add Grok API for real-time trending content")
        if 'openai' in all_services and 'perplexity' not in all_services:
            opportunities.append("Add Perplexity API for search trend analysis")

        for vol_name, vol_analysis in volumes_analysis.items():
            opportunities.extend(sorted(vol_analysis.opportunities))
            if vol_analysis.content_categories.get("audio", 0) > 100:
                opportunities.append(f"{vol_name}: Large audio collection - integrate with music management system")
            if vol_analysis.content_categories.get("image", 0) > 100:
                opportunities.append(f"{vol_name}: Large image collection - art gallery or print-on-demand potential")
            if vol_analysis.content_categories.get("code", 0) > 50:
                opportunities.append(f"{vol_name}: Code files detected - automation script opportunities")

        resource_mapping = {
            "api_services": set(all_services),
            "total_env_files": len(env_analysis),
            "total_volumes": len(volumes_analysis),
            "total_files_across_volumes": sum(v.total_files for v in volumes_analysis.values()),
            "total_size_across_volumes": sum(v.total_size for v in volumes_analysis.values()),
            "content_distribution": {
                vol_name: dict(sorted(vol.content_categories.items(), key=lambda x: x[0]))
                for vol_name, vol in sorted(volumes_analysis.items(), key=lambda x: x[0])
            }
        }

        recommendations = []
        if security_issues:
            recommendations.append("Review and fix security issues in environment files")
        if len(env_analysis) > 10:
            recommendations.append("Consider consolidating environment files for easier management")
        if all_services:
            recommendations.append(
                f"Leverage {len(all_services)} API services for multi-AI orchestration"
            )
        total_audio = sum(v.content_categories.get('audio', 0) for v in volumes_analysis.values())
        total_images = sum(v.content_categories.get('image', 0) for v in volumes_analysis.values())
        if total_audio > 100:
            recommendations.append(f"Integrate {total_audio:,} audio files with music management system")
        if total_images > 100:
            recommendations.append(f"Integrate {total_images:,} images with art gallery or print-on-demand system")

        return {
            "api_services": set(all_services),
            "total_api_keys": total_keys,
            "security_issues": security_issues,
            "opportunities": sorted(opportunities),
            "resource_mapping": resource_mapping,
            "recommendations": recommendations,
        }

    def _format_size(self, size: int) -> str:
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def save_analysis(self, analysis: ComprehensiveAnalysis, output_path: Path):
        output_path = Path(output_path).expanduser()
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

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
                for name, a in sorted(analysis.env_analysis.items())
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
                for name, v in sorted(analysis.volumes_analysis.items())
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

        md_file = output_path / f"ENV_VOLUMES_ANALYSIS_{timestamp}.md"
        with open(md_file, "w") as f:
            f.write(self.generate_markdown_report(analysis, timestamp))

        print(f"\n💾 Analysis saved:")
        print(f"   - JSON: {json_file.name}")
        print(f"   - Markdown: {md_file.name}")

    def generate_markdown_report(self, analysis: ComprehensiveAnalysis, timestamp: str) -> str:
        report = []
        report.append(f"# 🔍 DEEP ENV & VOLUMES CONTENT-AWARE ANALYSIS")
        report.append("## Comprehensive Intelligence Report\n")
        report.append(f"**Generated:** {datetime.now():%B %d, %Y at %H:%M:%S}")
        report.append(f"**Analysis ID:** {timestamp}\n")
        report.append("---\n")

        report.append("## 📊 EXECUTIVE SUMMARY\n")
        report.append("### Environment Files (.env.d)")
        report.append(f"- **Total Files Analyzed:** {len(analysis.env_analysis)}")
        report.append(f"- **Total API Services:** {len(analysis.api_services)}")
        report.append(f"- **Total API Keys:** {analysis.total_api_keys}")
        report.append(f"- **Security Issues:** {len(analysis.security_issues)}\n")

        report.append("### Volumes Analysis")
        total_files = sum(v.total_files for v in analysis.volumes_analysis.values())
        total_size = self._format_size(sum(v.total_size for v in analysis.volumes_analysis.values()))
        report.append(f"- **Volumes Analyzed:** {len(analysis.volumes_analysis)}")
        report.append(f"- **Total Files:** {total_files:,}")
        report.append(f"- **Total Size:** {total_size}\n")
        report.append("---\n")

        report.append("## 🔐 ENVIRONMENT FILES ANALYSIS\n")
        for name, env in sorted(analysis.env_analysis.items()):
            report.append(f"### {name}\n")
            report.append(f"**Services:** {', '.join(env.services) if env.services else 'None'}")
            report.append(f"**API Keys:** {len(env.api_keys)}")
            report.append(f"**Security Level:** {env.security_level.upper()}")
            report.append(f"**Issues:** {len(env.issues)}")
            report.append(f"**Opportunities:** {len(env.opportunities)}\n")
            if env.issues:
                report.append("**Issues:**")
                for issue in env.issues[:5]:
                    report.append(f"- {issue}")
                report.append("")
            if env.opportunities:
                report.append("**Opportunities:**")
                for opp in env.opportunities:
                    report.append(f"- {opp}")
                report.append("")

        report.append("---\n## 💾 VOLUMES ANALYSIS\n")
        for vol_name, vol in sorted(analysis.volumes_analysis.items()):
            report.append(f"### {vol_name}")
            report.append(f"**Total Files:** {vol.total_files:,}")
            report.append(f"**Total Size:** {self._format_size(vol.total_size)}")
            report.append(f"**Dominant File Type:** {vol.intelligence.get('dominant_file_type', 'N/A')}")
            report.append(f"**Dominant Category:** {vol.intelligence.get('dominant_category', 'N/A')}")
            report.append("\n#### Content Distribution")
            for category, count in sorted(vol.content_categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                report.append(f"- **{category.title()}:** {count:,} files")
            report.append("\n#### Top File Types")
            for ext, count in sorted(vol.file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
                pretty_ext = ext if ext and ext != 'no_extension' else 'no extension'
                report.append(f"- **{pretty_ext}:** {count:,} files")
            if vol.opportunities:
                report.append("\n#### Opportunities")
                for opp in vol.opportunities:
                    report.append(f"- {opp}")
            report.append("")

        report.append("---\n## 🎯 API SERVICES INVENTORY\n")
        report.append(f"**Total Services:** {len(analysis.api_services)}\n")
        report.append("### Services Detected:")
        for service in sorted(analysis.api_services):
            report.append(f"- {service.title()}")
        report.append("")

        report.append("---\n## ⚠️ SECURITY ISSUES\n")
        report.append(f"**Total Issues:** {len(analysis.security_issues)}\n")
        for issue in analysis.security_issues[:20]:
            report.append(f"- {issue}")
        if len(analysis.security_issues) > 20:
            report.append(f"\n*... and {len(analysis.security_issues) - 20} more issues*\n")

        report.append("---\n## 💡 OPPORTUNITIES\n")
        report.append(f"**Total Opportunities:** {len(analysis.opportunities)}\n")
        for opp in analysis.opportunities:
            report.append(f"- {opp}")
        report.append("")

        report.append("---\n## 📋 RECOMMENDATIONS\n")
        for rec in analysis.recommendations:
            report.append(f"- {rec}")
        report.append("")

        report.append("---\n## 🔗 RESOURCE MAPPING\n")
        report.append("### Content Distribution Across Volumes\n")
        content_dist = analysis.resource_mapping.get('content_distribution', {})
        for vol_name, categories in sorted(content_dist.items()):
            report.append(f"#### {vol_name}")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                report.append(f"- {category.title()}: {count:,} files")
            report.append("")
        report.append("---\n**Analysis Complete** ✅\n")
        report.append("*This report was generated using deep content-aware analysis techniques.*\n")
        return "\n".join(report)

# =======================

# Main Entrypoint

# =======================

def main():
parser = argparse.ArgumentParser(description="Deep ENV & Volumes Analyzer")
parser.add_argument("--output", default="~/analysis_reports", help="Output directory for reports")
parser.add_argument("--json-only", action="store_true", help="Generate JSON only")
parser.add_argument("--md-only", action="store_true", help="Generate Markdown only")
args = parser.parse_args()

    analyzer = DeepEnvVolumesAnalyzer()
    analysis = analyzer.analyze_all()

    print("\n" + "=" * 70)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"\nEnvironment Files: {len(analysis.env_analysis)}")
    print(f"API Services: {len(analysis.api_services)}")
    print(f"Total API Keys: {analysis.total_api_keys}")
    print(f"Volumes Analyzed: {len(analysis.volumes_analysis)}")
    print(f"Total Files: {sum(v.total_files for v in analysis.volumes_analysis.values()):,}")
    print(f"Security Issues: {len(analysis.security_issues)}")
    print(f"Opportunities: {len(analysis.opportunities)}")
    print(f"Recommendations: {len(analysis.recommendations)}")

    output_dir = Path(args.output).expanduser()
    if not args.md_only:
        analyzer.save_analysis(analysis, output_dir)
    print("\n✅ Analysis complete!")

if **name** == "**main**":
main()
