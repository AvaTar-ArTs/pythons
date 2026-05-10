#!/usr/bin/env python3
"""
~/.env.d Directory Analyzer
Comprehensive analysis of environment variable organization and security
"""

import os
# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import json
import re
import stat
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Set


class EnvDAnalyzer:
    """Comprehensive analyzer for ~/.env.d directory"""
    
    def __init__(self):
        self.env_d_path = PathLib.home() / ".env.d"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "scan_metadata": {
                "path": str(self.env_d_path),
                "timestamp": self.timestamp
            },
            "file_analysis": {},
            "key_analysis": {},
            "security_analysis": {},
            "organization_analysis": {},
            "recommendations": []
        }
    
    def analyze_files(self):
        """Analyze all .env files"""
        print("📁 Analyzing .env files...")
        
        files = list(self.env_d_path.glob("*.env"))
        file_data = {}
        
        all_keys = set()
        key_to_files = defaultdict(list)
        key_patterns = Counter()
        
        for env_file in files:
            try:
                file_info = {
                    "name": env_file.name,
                    "size": env_file.stat().st_size,
                    "lines": 0,
                    "keys": [],
                    "comments": 0,
                    "empty_lines": 0,
                    "export_statements": 0,
                    "has_quotes": 0,
                    "permissions": oct(env_file.stat().st_mode)[-3:]
                }
                
                with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    lines = content.splitlines()
                    file_info["lines"] = len(lines)
                    
                    for line in lines:
                        line = line.strip()
                        
                        if not line:
                            file_info["empty_lines"] += 1
                            continue
                        
                        if line.startswith("#"):
                            file_info["comments"] += 1
                            continue
                        
                        if line.startswith("export "):
                            file_info["export_statements"] += 1
                            line = line[7:]
                        
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Analyze key
                            file_info["keys"].append(key)
                            all_keys.add(key)
                            key_to_files[key].append(env_file.name)
                            
                            # Detect key patterns
                            if "_API_KEY" in key:
                                key_patterns["API_KEY"] += 1
                            if "_SECRET" in key:
                                key_patterns["SECRET"] += 1
                            if "_TOKEN" in key:
                                key_patterns["TOKEN"] += 1
                            if "_PASSWORD" in key:
                                key_patterns["PASSWORD"] += 1
                            if "_URL" in key:
                                key_patterns["URL"] += 1
                            
                            # Check for quotes
                            if value.startswith('"') or value.startswith("'"):
                                file_info["has_quotes"] += 1
                
                file_data[env_file.name] = file_info
                
            except Exception as e:
                print(f"   ⚠️  Error analyzing {env_file.name}: {e}")
        
        self.results["file_analysis"] = {
            "total_files": len(files),
            "files": file_data,
            "total_keys": len(all_keys),
            "unique_keys": list(all_keys),
            "key_patterns": dict(key_patterns)
        }
        
        # Find duplicate keys across files
        duplicates = {k: v for k, v in key_to_files.items() if len(v) > 1}
        self.results["key_analysis"]["duplicate_keys"] = duplicates
        
        print(f"   ✓ Analyzed {len(files)} files with {len(all_keys)} unique keys")
    
    def analyze_security(self):
        """Analyze security aspects"""
        print("🔒 Analyzing security...")
        
        security = {
            "file_permissions": {},
            "sensitive_keys": [],
            "potential_issues": []
        }
        
        files = list(self.env_d_path.glob("*.env"))
        
        for env_file in files:
            try:
                file_stat = env_file.stat()
                file_mode = file_stat.st_mode
                
                # Check permissions
                is_readable_by_others = bool(file_mode & stat.S_IROTH)
                is_writable_by_others = bool(file_mode & stat.S_IWOTH)
                is_readable_by_group = bool(file_mode & stat.S_IRGRP)
                is_writable_by_group = bool(file_mode & stat.S_IWGRP)
                
                perm_issues = []
                if is_readable_by_others:
                    perm_issues.append("readable by others")
                if is_writable_by_others:
                    perm_issues.append("writable by others")
                if is_readable_by_group:
                    perm_issues.append("readable by group")
                if is_writable_by_group:
                    perm_issues.append("writable by group")
                
                security["file_permissions"][env_file.name] = {
                    "octal": oct(file_mode)[-3:],
                    "issues": perm_issues
                }
                
                if perm_issues:
                    security["potential_issues"].append({
                        "file": env_file.name,
                        "type": "permissions",
                        "issues": perm_issues
                    })
                
            except Exception as e:
                pass
        
        # Find sensitive keys
        sensitive_patterns = [
            "API_KEY", "SECRET", "TOKEN", "PASSWORD", 
            "PRIVATE", "CREDENTIAL", "AUTH"
        ]
        
        for key in self.results["file_analysis"].get("unique_keys", []):
            if any(pattern in key.upper() for pattern in sensitive_patterns):
                security["sensitive_keys"].append(key)
        
        self.results["security_analysis"] = security
        print(f"   ✓ Security analysis complete")
    
    def analyze_organization(self):
        """Analyze organization patterns"""
        print("📊 Analyzing organization...")
        
        files = list(self.env_d_path.glob("*.env"))
        
        organization = {
            "naming_patterns": Counter(),
            "categories": defaultdict(list),
            "file_sizes": {},
            "key_distribution": {}
        }
        
        # Analyze naming patterns
        for env_file in files:
            name = env_file.name.replace(".env", "")
            
            # Detect naming patterns
            if "-" in name:
                organization["naming_patterns"]["hyphenated"] += 1
            if "_" in name:
                organization["naming_patterns"]["underscored"] += 1
            if name.isupper():
                organization["naming_patterns"]["uppercase"] += 1
            if name.islower():
                organization["naming_patterns"]["lowercase"] += 1
            
            # Categorize by name patterns
            name_lower = name.lower()
            if "api" in name_lower:
                organization["categories"]["api"].append(env_file.name)
            if "llm" in name_lower or "ai" in name_lower:
                organization["categories"]["ai-llm"].append(env_file.name)
            if "audio" in name_lower or "music" in name_lower:
                organization["categories"]["audio-music"].append(env_file.name)
            if "vector" in name_lower or "memory" in name_lower:
                organization["categories"]["vector-memory"].append(env_file.name)
            if "social" in name_lower or "instagram" in name_lower:
                organization["categories"]["social-media"].append(env_file.name)
            if "aws" in name_lower or "cloud" in name_lower:
                organization["categories"]["cloud"].append(env_file.name)
            if "master" in name_lower or "consolidated" in name_lower:
                organization["categories"]["consolidated"].append(env_file.name)
            else:
                organization["categories"]["other"].append(env_file.name)
        
        # File size distribution
        for env_file in files:
            size = env_file.stat().st_size
            organization["file_sizes"][env_file.name] = size
        
        # Key distribution per file
        for file_name, file_data in self.results["file_analysis"].get("files", {}).items():
            organization["key_distribution"][file_name] = len(file_data.get("keys", []))
        
        self.results["organization_analysis"] = {
            "naming_patterns": dict(organization["naming_patterns"]),
            "categories": {k: len(v) for k, v in organization["categories"].items()},
            "category_files": dict(organization["categories"]),
            "total_size": sum(organization["file_sizes"].values()),
            "avg_file_size": sum(organization["file_sizes"].values()) / len(files) if files else 0,
            "avg_keys_per_file": sum(organization["key_distribution"].values()) / len(files) if files else 0
        }
        
        print(f"   ✓ Organization analysis complete")
    
    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        print("💡 Generating recommendations...")
        
        recommendations = []
        
        # Security recommendations
        security_issues = self.results["security_analysis"].get("potential_issues", [])
        if security_issues:
            recommendations.append({
                "priority": "HIGH",
                "category": "Security",
                "issue": f"{len(security_issues)} files have permission issues",
                "recommendation": "Run: chmod 600 ~/.env.d/*.env to restrict access",
                "files_affected": len(security_issues)
            })
        
        # Duplicate key recommendations
        duplicates = self.results["key_analysis"].get("duplicate_keys", {})
        if duplicates:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Organization",
                "issue": f"{len(duplicates)} keys appear in multiple files",
                "recommendation": "Consider consolidating duplicate keys into a single file",
                "files_affected": len(duplicates)
            })
        
        # Organization recommendations
        categories = self.results["organization_analysis"].get("categories", {})
        if categories.get("other", 0) > 5:
            recommendations.append({
                "priority": "LOW",
                "category": "Organization",
                "issue": "Many files in 'other' category",
                "recommendation": "Consider better categorization or naming conventions",
                "files_affected": categories.get("other", 0)
            })
        
        # File size recommendations
        file_analysis = self.results["file_analysis"]
        large_files = [f for f, data in file_analysis.get("files", {}).items() 
                       if data.get("lines", 0) > 100]
        if large_files:
            recommendations.append({
                "priority": "LOW",
                "category": "Organization",
                "issue": f"{len(large_files)} files have >100 lines",
                "recommendation": "Consider splitting large files into logical groups",
                "files_affected": len(large_files)
            })
        
        self.results["recommendations"] = recommendations
        print(f"   ✓ Generated {len(recommendations)} recommendations")
    
    def save_results(self):
        """Save analysis results"""
        print("💾 Saving results...")
        
        output_path = PathLib.home() / "pythons" / f"ENV_D_ANALYSIS_{self.timestamp}"
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_path = output_path / "ENV_D_ANALYSIS.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Generate summary report
        self.generate_summary_report(output_path)
        
        print(f"   ✓ Results saved to {output_path}")
        return output_path
    
    def generate_summary_report(self, output_path: Path):
        """Generate human-readable summary"""
        report_path = output_path / "ENV_D_ANALYSIS_REPORT.md"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# ~/.env.d Directory Analysis Report\n\n")
            f.write(f"**Generated:** {self.timestamp}\n")
            f.write(f"**Path:** {self.env_d_path}\n\n")
            
            # File Analysis
            file_analysis = self.results["file_analysis"]
            f.write("## 📁 File Analysis\n\n")
            f.write(f"- **Total Files:** {file_analysis['total_files']}\n")
            f.write(f"- **Total Keys:** {file_analysis['total_keys']}\n")
            f.write(f"- **Unique Keys:** {len(file_analysis['unique_keys'])}\n\n")
            
            # Key Patterns
            f.write("## 🔑 Key Patterns\n\n")
            for pattern, count in file_analysis.get("key_patterns", {}).items():
                f.write(f"- **{pattern}:** {count} occurrences\n")
            f.write("\n")
            
            # Security
            security = self.results["security_analysis"]
            f.write("## 🔒 Security Analysis\n\n")
            f.write(f"- **Sensitive Keys Found:** {len(security.get('sensitive_keys', []))}\n")
            f.write(f"- **Permission Issues:** {len(security.get('potential_issues', []))}\n\n")
            
            if security.get("potential_issues"):
                f.write("### Files with Permission Issues\n\n")
                for issue in security["potential_issues"][:10]:
                    f.write(f"- **{issue['file']}:** {', '.join(issue['issues'])}\n")
                f.write("\n")
            
            # Organization
            org = self.results["organization_analysis"]
            f.write("## 📊 Organization Analysis\n\n")
            f.write(f"- **Total Size:** {org.get('total_size', 0) / 1024:.2f} KB\n")
            f.write(f"- **Average File Size:** {org.get('avg_file_size', 0) / 1024:.2f} KB\n")
            f.write(f"- **Average Keys per File:** {org.get('avg_keys_per_file', 0):.1f}\n\n")
            
            f.write("### Categories\n\n")
            for category, count in org.get("categories", {}).items():
                f.write(f"- **{category}:** {count} files\n")
            f.write("\n")
            
            # Duplicate Keys
            duplicates = self.results["key_analysis"].get("duplicate_keys", {})
            if duplicates:
                f.write("## 🔄 Duplicate Keys\n\n")
                f.write(f"Found {len(duplicates)} keys appearing in multiple files:\n\n")
                for key, files in list(duplicates.items())[:10]:
                    f.write(f"- **{key}:** appears in {len(files)} files\n")
                f.write("\n")
            
            # Recommendations
            f.write("## 💡 Recommendations\n\n")
            for rec in self.results["recommendations"]:
                f.write(f"### {rec['priority']} Priority: {rec['category']}\n\n")
                f.write(f"**Issue:** {rec['issue']}\n\n")
                f.write(f"**Recommendation:** {rec['recommendation']}\n\n")
                f.write(f"**Files Affected:** {rec['files_affected']}\n\n")
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting ~/.env.d Analysis")
        print("=" * 60)
        print(f"Path: {self.env_d_path}\n")
        
        if not self.env_d_path.exists():
            print("❌ ~/.env.d directory not found!")
            return None
        
        self.analyze_files()
        self.analyze_security()
        self.analyze_organization()
        self.generate_recommendations()
        
        output_path = self.save_results()
        
        print("\n" + "=" * 60)
        print("✅ Analysis Complete!")
        print(f"📁 Results saved to: {output_path}")
        print("=" * 60)
        
        return output_path


if __name__ == "__main__":
    analyzer = EnvDAnalyzer()
    analyzer.run_analysis()
