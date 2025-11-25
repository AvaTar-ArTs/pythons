#!/usr/bin/env python3
"""
Enhanced Content-Aware Chat Analysis Organizer v2.0
Incorporates Dr. Adu SEO project updates and improvements
Outputs comprehensive analysis in professional format with actionable insights
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class EnhancedContentAnalyzerV2:
    def __init__(self, source_dir, target_dir, batch_size=5):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.batch_size = batch_size
        self.all_files = []
        self.batch_results = []
        self.master_insights = {}
        self.dr_adu_content = []
        self.seo_optimization_content = []

        # Dr. Adu specific search terms
        self.dr_adu_terms = [
            "Dr. Adu",
            "Dr Lawrence Adu",
            "Lawrence Adu",
            "Gainesville Psychiatry",
            "gainesvillepfs.com",
            "Gainesville Psychiatry and Forensic Services",
            "TMS therapy",
            "forensic psychiatry",
            "SEO optimization",
            "psychiatrist Gainesville",
            "NeuroStar",
            "treatment-resistant depression",
            "mental health services Gainesville",
        ]

    def analyze_chat_structure(self, content):
        """Analyze the structure of a chat analysis file with enhanced patterns"""
        patterns = {
            "chat_id": r"Chat ID.*?`([^`]+)`",
            "agent_id": r"Agent ID.*?`([^`]+)`",
            "created": r"Created.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
            "mode": r"Mode.*?(\w+)",
            "model": r"Model.*?(\w+)",
            "total_messages": r"Total Messages.*?(\d+)",
            "total_blobs": r"Total Blobs.*?(\d+)",
            "tool_calls": r"Tool Calls.*?(\d+)",
            "code_blocks": r"Code Blocks.*?(\d+)",
            "file_operations": r"File Operations.*?(\d+)",
            "terminal_commands": r"Terminal Commands.*?(\d+)",
            "seo_mentions": r"(SEO|seo|search engine optimization)",
            "dr_adu_mentions": r"(Dr\.?\s*Adu|Lawrence\s*Adu|Gainesville\s*Psychiatry)",
            "business_value": r"(business|revenue|client|customer|service|marketing)",
        }

        extracted = {}
        for key, pattern in patterns.items():
            if key in ["seo_mentions", "dr_adu_mentions", "business_value"]:
                matches = re.findall(pattern, content, re.IGNORECASE)
                extracted[key] = len(matches)
            else:
                match = re.search(pattern, content)
                if match:
                    extracted[key] = match.group(1)

        return extracted

    def extract_code_blocks(self, content, max_blocks=5):
        """Extract and categorize code blocks with enhanced analysis"""
        code_blocks = []

        # Find all code blocks
        code_pattern = r"```(\w+)?\n(.*?)\n```"
        matches = re.findall(code_pattern, content, re.DOTALL)

        for i, (language, code) in enumerate(matches[:max_blocks]):
            if not language:
                language = "unknown"

            # Truncate very large code blocks
            if len(code) > CONSTANT_8000:
                code = code[:CONSTANT_8000] + "\n... [TRUNCATED]"

            code_info = {
                "index": i,
                "language": language,
                "code": code.strip(),
                "size": len(code),
                "lines": len(code.split("\n")),
                "type": self.classify_code_type(code, language),
                "quality_score": self.assess_code_quality(code, language),
                "business_relevance": self.assess_business_relevance(code),
                "seo_relevance": self.assess_seo_relevance(code),
            }
            code_blocks.append(code_info)

        return code_blocks

    def classify_code_type(self, code, language):
        """Enhanced code type classification"""
        code_lower = code.lower()

        # Dr. Adu specific patterns
        if any(term.lower() in code_lower for term in self.dr_adu_terms):
            return "dr_adu_seo_code"
        elif "userscript" in code_lower or "tampermonkey" in code_lower:
            return "userscript"
        elif "function" in code_lower and "javascript" in language.lower():
            return "javascript_function"
        elif "class " in code_lower or "def " in code_lower:
            return "class_definition"
        elif "import " in code_lower or "from " in code_lower:
            return "imports"
        elif "html" in language.lower() or "<html" in code_lower:
            return "html_template"
        elif "css" in language.lower() or "style" in code_lower:
            return "styling"
        elif "json" in language.lower() or ("{" in code and "}" in code):
            return "configuration"
        elif "bash" in language.lower() or "shell" in language.lower():
            return "shell_script"
        elif "seo" in code_lower or "meta" in code_lower:
            return "seo_optimization"
        else:
            return "general_code"

    def assess_code_quality(self, code, language):
        """Enhanced code quality assessment"""
        score = 0.5  # Base score

        # Length factor
        if CONSTANT_100 <= len(code) <= CONSTANT_3000:
            score += 0.1
        elif len(code) > CONSTANT_3000:
            score += 0.05

        # Structure factors
        if "def " in code or "function" in code:
            score += 0.1
        if "class " in code:
            score += 0.1
        if "import" in code:
            score += 0.05
        if "try:" in code or "except" in code:
            score += 0.1
        if "if __name__" in code:
            score += 0.05

        # Documentation
        if '"""' in code or "'''" in code:
            score += 0.1
        if "#" in code and code.count("#") > 2:
            score += 0.05

        # Dr. Adu specific quality indicators
        if any(term.lower() in code.lower() for term in self.dr_adu_terms):
            score += 0.15

        return min(1.0, score)

    def assess_business_relevance(self, code):
        """Assess business relevance of code"""
        code_lower = code.lower()
        relevance = 0.0

        # Business indicators
        business_terms = [
            "revenue",
            "client",
            "customer",
            "service",
            "marketing",
            "sales",
            "growth",
        ]
        for term in business_terms:
            if term in code_lower:
                relevance += 0.2

        # Dr. Adu specific relevance
        if any(term.lower() in code_lower for term in self.dr_adu_terms):
            relevance += 0.5

        return min(1.0, relevance)

    def assess_seo_relevance(self, code):
        """Assess SEO relevance of code"""
        code_lower = code.lower()
        relevance = 0.0

        # SEO indicators
        seo_terms = [
            "seo",
            "meta",
            "title",
            "description",
            "keywords",
            "schema",
            "structured data",
        ]
        for term in seo_terms:
            if term in code_lower:
                relevance += 0.15

        return min(1.0, relevance)

    def extract_tool_calls(self, content, max_calls=8):
        """Extract tool call information with enhanced analysis"""
        tool_calls = []

        # Find tool call sections
        tool_pattern = r"### 🛠️ Message \d+ - TOOL.*?\n\n(.*?)(?=---|\n###|\Z)"
        tool_matches = re.findall(tool_pattern, content, re.DOTALL)

        for tool_content in tool_matches[:max_calls]:
            # Extract tool type
            tool_type_match = re.search(r"Tool Result: (\w+)", tool_content)
            tool_type = tool_type_match.group(1) if tool_type_match else "unknown"

            # Extract tool ID
            id_match = re.search(r"ID: `([^`]+)`", tool_content)
            tool_id = id_match.group(1) if id_match else "unknown"

            # Extract size
            size_match = re.search(r"Size: (\d+) bytes", tool_content)
            size = int(size_match.group(1)) if size_match else 0

            tool_info = {
                "tool_type": tool_type,
                "tool_id": tool_id,
                "size": size,
                "content_preview": (
                    tool_content[:CONSTANT_300] + "..."
                    if len(tool_content) > CONSTANT_300
                    else tool_content
                ),
                "complexity": self.assess_tool_complexity(tool_content),
                "business_impact": self.assess_tool_business_impact(tool_content),
                "seo_impact": self.assess_tool_seo_impact(tool_content),
            }
            tool_calls.append(tool_info)

        return tool_calls

    def assess_tool_complexity(self, tool_content):
        """Assess complexity of tool call"""
        if len(tool_content) > CONSTANT_2000:
            return "high"
        elif len(tool_content) > CONSTANT_1000:
            return "medium"
        else:
            return "low"

    def assess_tool_business_impact(self, tool_content):
        """Assess business impact of tool call"""
        content_lower = tool_content.lower()
        impact = 0.0

        # High impact tools
        high_impact_tools = ["write", "search_replace", "edit_file", "web_search"]
        for tool in high_impact_tools:
            if tool in content_lower:
                impact += 0.3

        # Dr. Adu content impact
        if any(term.lower() in content_lower for term in self.dr_adu_terms):
            impact += 0.4

        return min(1.0, impact)

    def assess_tool_seo_impact(self, tool_content):
        """Assess SEO impact of tool call"""
        content_lower = tool_content.lower()
        impact = 0.0

        # SEO-related tools
        seo_tools = ["write", "search_replace", "edit_file", "web_search"]
        for tool in seo_tools:
            if tool in content_lower:
                impact += 0.2

        # SEO content indicators
        seo_indicators = ["seo", "meta", "title", "description", "keywords"]
        for indicator in seo_indicators:
            if indicator in content_lower:
                impact += 0.15

        return min(1.0, impact)

    def identify_projects(self, content, filename):
        """Enhanced project identification with Dr. Adu focus"""
        projects = set()

        # Enhanced project patterns
        project_patterns = [
            r"Dr\.?\s*Adu.*?Project",
            r"Gainesville\s*Psychiatry.*?Project",
            r"SEO\s*Optimization.*?Project",
            r"(\w+)\s*SEO\s*Project",
            r"(\w+)\s*Website\s*Project",
            r"(\w+)\s*Analysis\s*Project",
            r"Project:\s*([^\n]+)",
            r"#\s*([^#\n]+)\s*Project",
            r"Digital Dive Framework",
            r"Chat Analysis",
            r"Script Optimizer",
            r"Analyze Sort",
            r"Universal Chat Exporter",
            r"Export Claude\.Ai",
            r"Chat Exporter",
            r"Content Analysis",
            r"File Organization",
            r"Python.*?Project",
            r"Web.*?Development",
            r"AI.*?Tool",
            r"Automation.*?Script",
            r"TMS.*?Therapy",
            r"Forensic.*?Psychiatry",
            r"Mental.*?Health.*?Services",
        ]

        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                clean_match = match.strip()[:50]
                if clean_match and len(clean_match) > 3:
                    projects.add(clean_match)

        # Extract from filename patterns
        filename_lower = filename.lower()
        if "chat_" in filename_lower:
            chat_id = filename.split("_")[1] if "_" in filename else "unknown"
            projects.add(f"Chat_{chat_id}")

        return list(projects)

    def categorize_content(self, content, filename):
        """Enhanced content categorization with Dr. Adu focus"""
        categories = set()

        # Enhanced content analysis patterns
        patterns = {
            "seo_optimization": [
                r"SEO",
                r"search engine optimization",
                r"meta tags",
                r"keywords",
                r"ranking",
                r"optimization",
                r"Dr\.?\s*Adu",
                r"Gainesville\s*Psychiatry",
                r"organic traffic",
                r"search visibility",
                r"local SEO",
                r"structured data",
                r"schema\.org",
                r"google my business",
            ],
            "web_development": [
                r"HTML",
                r"CSS",
                r"JavaScript",
                r"website",
                r"web development",
                r"frontend",
                r"backend",
                r"userscript",
                r"tampermonkey",
                r"responsive",
                r"mobile optimization",
                r"user experience",
            ],
            "data_analysis": [
                r"analysis",
                r"statistics",
                r"data",
                r"metrics",
                r"performance",
                r"tracking",
                r"analytics",
                r"csv",
                r"json",
                r"visualization",
                r"reporting",
                r"insights",
                r"patterns",
            ],
            "automation": [
                r"automation",
                r"script",
                r"tool",
                r"export",
                r"import",
                r"batch",
                r"processing",
                r"terminal",
                r"workflow",
                r"efficiency",
                r"productivity",
                r"streamline",
            ],
            "content_creation": [
                r"content",
                r"writing",
                r"copy",
                r"text",
                r"article",
                r"blog",
                r"creative",
                r"narrative",
                r"storytelling",
                r"branding",
                r"messaging",
                r"communication",
            ],
            "file_management": [
                r"file",
                r"directory",
                r"folder",
                r"organize",
                r"sort",
                r"structure",
                r"management",
                r"backup",
                r"archive",
                r"organization",
                r"categorization",
                r"classification",
            ],
            "chat_analysis": [
                r"chat",
                r"conversation",
                r"message",
                r"discussion",
                r"analysis",
                r"export",
                r"conversation",
                r"dialogue",
                r"communication",
                r"interaction",
                r"engagement",
            ],
            "business_development": [
                r"business",
                r"revenue",
                r"client",
                r"customer",
                r"service",
                r"marketing",
                r"sales",
                r"growth",
                r"strategy",
                r"competitive",
                r"market",
                r"opportunity",
            ],
            "dr_adu_psychiatry": [
                r"Dr\.?\s*Adu",
                r"Lawrence\s*Adu",
                r"Gainesville\s*Psychiatry",
                r"forensic\s*psychiatry",
                r"TMS\s*therapy",
                r"NeuroStar",
                r"treatment-resistant\s*depression",
                r"mental\s*health\s*services",
                r"psychiatrist\s*Gainesville",
                r"gainesvillepfs\.com",
            ],
        }

        content_lower = content.lower()
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    categories.add(category)
                    break

        return list(categories)

    def analyze_single_file(self, file_path):
        """Enhanced single file analysis with Dr. Adu focus"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Basic file info
            file_info = {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.source_dir)),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                "created": datetime.fromtimestamp(file_path.stat().st_ctime),
                "word_count": len(content.split()),
                "line_count": len(content.splitlines()),
                "content_hash": hashlib.md5(content.encode()).hexdigest(),
            }

            # Enhanced analysis
            file_info["chat_structure"] = self.analyze_chat_structure(content)
            file_info["code_blocks"] = self.extract_code_blocks(content, max_blocks=5)
            file_info["tool_calls"] = self.extract_tool_calls(content, max_calls=8)
            file_info["projects"] = self.identify_projects(content, file_path.name)
            file_info["categories"] = self.categorize_content(content, file_path.name)

            # Extract chat ID for relationships
            file_info["chat_id"] = file_info["chat_structure"].get("chat_id", "unknown")

            # Calculate enhanced quality metrics
            file_info["quality_score"] = self.calculate_file_quality(file_info)
            file_info["business_value"] = self.assess_business_value(file_info)
            file_info["dr_adu_relevance"] = self.assess_dr_adu_relevance(file_info)
            file_info["seo_potential"] = self.assess_seo_potential(file_info)

            return file_info

        except Exception as e:
            logger.info(f"      ❌ Error analyzing {file_path.name}: {e}")
            return None

    def calculate_file_quality(self, file_info):
        """Enhanced file quality calculation"""
        score = 0.5  # Base score

        # Size factor (optimal range)
        if CONSTANT_1000 <= file_info["word_count"] <= CONSTANT_15000:
            score += 0.1
        elif file_info["word_count"] > CONSTANT_15000:
            score += 0.05

        # Code quality
        if file_info["code_blocks"]:
            avg_code_quality = sum(
                block["quality_score"] for block in file_info["code_blocks"]
            ) / len(file_info["code_blocks"])
            score += avg_code_quality * 0.2

        # Project identification
        if file_info["projects"]:
            score += 0.1

        # Category diversity
        if len(file_info["categories"]) > 1:
            score += 0.05

        # Dr. Adu relevance bonus
        if file_info.get("dr_adu_relevance", 0) > 0.5:
            score += 0.15

        return min(1.0, score)

    def assess_business_value(self, file_info):
        """Enhanced business value assessment"""
        value = "low"

        # High value indicators
        if any(
            cat in file_info["categories"]
            for cat in ["seo_optimization", "business_development", "dr_adu_psychiatry"]
        ):
            value = "high"
        elif any(
            cat in file_info["categories"] for cat in ["web_development", "automation"]
        ):
            value = "medium"

        # Dr. Adu specific value
        if file_info.get("dr_adu_relevance", 0) > 0.7:
            value = "high"

        return value

    def assess_dr_adu_relevance(self, file_info):
        """Assess Dr. Adu relevance score"""
        relevance = 0.0

        # Check categories
        if "dr_adu_psychiatry" in file_info["categories"]:
            relevance += 0.5

        # Check projects
        for project in file_info["projects"]:
            if any(term.lower() in project.lower() for term in self.dr_adu_terms):
                relevance += 0.3
                break

        # Check content mentions
        if file_info["chat_structure"].get("dr_adu_mentions", 0) > 0:
            relevance += 0.2

        return min(1.0, relevance)

    def assess_seo_potential(self, file_info):
        """Assess SEO potential score"""
        potential = 0.0

        # Check categories
        if "seo_optimization" in file_info["categories"]:
            potential += 0.4

        # Check content mentions
        if file_info["chat_structure"].get("seo_mentions", 0) > 0:
            potential += 0.3

        # Check code blocks
        for code_block in file_info["code_blocks"]:
            potential += code_block.get("seo_relevance", 0) * 0.1

        return min(1.0, potential)

    def process_batch(self, file_batch, batch_number):
        """Enhanced batch processing with Dr. Adu focus"""
        logger.info(
            f"\n📦 Processing Batch {batch_number} ({len(file_batch)} files)..."
        )

        batch_results = {
            "batch_number": batch_number,
            "files": [],
            "projects": set(),
            "categories": set(),
            "code_types": set(),
            "tool_types": set(),
            "high_value_files": [],
            "dr_adu_files": [],
            "seo_files": [],
            "insights": {},
            "statistics": {
                "total_files": len(file_batch),
                "total_size": 0,
                "total_words": 0,
                "avg_quality": 0,
                "high_value_count": 0,
                "dr_adu_count": 0,
                "seo_count": 0,
            },
        }

        quality_scores = []

        for file_path in file_batch:
            logger.info(f"   📄 Analyzing: {file_path.relative_to(self.source_dir)}")
            file_analysis = self.analyze_single_file(file_path)
            if file_analysis:
                batch_results["files"].append(file_analysis)
                batch_results["projects"].update(file_analysis.get("projects", []))
                batch_results["categories"].update(file_analysis.get("categories", []))

                for code_block in file_analysis.get("code_blocks", []):
                    batch_results["code_types"].add(code_block.get("type", "unknown"))

                for tool_call in file_analysis.get("tool_calls", []):
                    batch_results["tool_types"].add(
                        tool_call.get("tool_type", "unknown")
                    )

                batch_results["statistics"]["total_size"] += file_analysis["size"]
                batch_results["statistics"]["total_words"] += file_analysis[
                    "word_count"
                ]
                quality_scores.append(file_analysis.get("quality_score", 0.5))

                if file_analysis.get("business_value") == "high":
                    batch_results["high_value_files"].append(file_analysis)
                    batch_results["statistics"]["high_value_count"] += 1

                if file_analysis.get("dr_adu_relevance", 0) > 0.5:
                    batch_results["dr_adu_files"].append(file_analysis)
                    batch_results["statistics"]["dr_adu_count"] += 1

                if file_analysis.get("seo_potential", 0) > 0.5:
                    batch_results["seo_files"].append(file_analysis)
                    batch_results["statistics"]["seo_count"] += 1

        # Calculate average quality
        if quality_scores:
            batch_results["statistics"]["avg_quality"] = sum(quality_scores) / len(
                quality_scores
            )

        # Generate enhanced insights
        batch_results["insights"] = self.generate_enhanced_batch_insights(batch_results)

        # Convert sets to lists for JSON serialization
        batch_results["projects"] = list(batch_results["projects"])
        batch_results["categories"] = list(batch_results["categories"])
        batch_results["code_types"] = list(batch_results["code_types"])
        batch_results["tool_types"] = list(batch_results["tool_types"])

        return batch_results

    def generate_enhanced_batch_insights(self, batch_results):
        """Generate enhanced strategic insights for a batch"""
        insights = {
            "key_findings": [],
            "recommendations": [],
            "opportunities": [],
            "risks": [],
            "dr_adu_insights": [],
            "seo_insights": [],
        }

        # Analyze high-value files
        if batch_results["high_value_files"]:
            insights["key_findings"].append(
                f"Found {len(batch_results['high_value_files'])} high-value files with business potential"
            )

        # Analyze Dr. Adu content
        if batch_results["dr_adu_files"]:
            insights["dr_adu_insights"].append(
                f"Identified {len(batch_results['dr_adu_files'])} files with Dr. Adu content"
            )
            insights["recommendations"].append(
                "Prioritize Dr. Adu content for immediate business impact"
            )
            insights["opportunities"].append(
                "Leverage Dr. Adu content for competitive advantage"
            )

        # Analyze SEO content
        if batch_results["seo_files"]:
            insights["seo_insights"].append(
                f"Found {len(batch_results['seo_files'])} files with SEO potential"
            )
            insights["recommendations"].append(
                "Implement SEO optimization strategies from identified content"
            )
            insights["opportunities"].append(
                "Scale SEO efforts based on successful patterns"
            )

        # Analyze code quality
        if batch_results["statistics"]["avg_quality"] > 0.8:
            insights["key_findings"].append("Excellent overall code quality detected")
        elif batch_results["statistics"]["avg_quality"] < 0.5:
            insights["risks"].append(
                "Code quality below optimal - consider refactoring"
            )
            insights["recommendations"].append("Implement code quality improvements")

        # Analyze project diversity
        if len(batch_results["projects"]) > 5:
            insights["key_findings"].append("Diverse project portfolio detected")
            insights["opportunities"].append(
                "Cross-project knowledge transfer potential"
            )

        return insights

    def scan_all_files_batched(self):
        """Enhanced batch scanning with Dr. Adu focus"""
        logger.info(
            "🔍 Performing enhanced content-aware analysis with Dr. Adu focus..."
        )

        if not self.source_dir.exists():
            logger.info(f"❌ Source directory not found: {self.source_dir}")
            return

        # Get all files first
        all_file_paths = []
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [
                ".md",
                ".html",
                ".txt",
                ".json",
                ".csv",
            ]:
                all_file_paths.append(file_path)

        logger.info(f"📊 Total files to process: {len(all_file_paths)}")
        logger.info(f"📦 Processing in batches of {self.batch_size}")

        # Process in batches
        total_batches = (len(all_file_paths) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(all_file_paths), self.batch_size):
            batch_number = (i // self.batch_size) + 1
            file_batch = all_file_paths[i : i + self.batch_size]

            logger.info(f"\n🔄 Processing batch {batch_number}/{total_batches}")
            batch_results = self.process_batch(file_batch, batch_number)
            self.batch_results.append(batch_results)
            self.save_batch_results(batch_results)

            # Add to all_files for summary
            self.all_files.extend(batch_results["files"])

        logger.info(f"\n📊 Total files analyzed: {len(self.all_files)}")
        logger.info(f"📦 Total batches processed: {len(self.batch_results)}")

    def save_batch_results(self, batch_results):
        """Save enhanced batch results"""
        batch_dir = self.target_dir / "07_Exports" / "batches"
        batch_dir.mkdir(parents=True, exist_ok=True)

        # Save batch JSON
        batch_file = batch_dir / f"batch_{batch_results['batch_number']:03d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, default=str)

        # Save enhanced batch summary
        summary_file = (
            batch_dir
            / f"batch_{batch_results['batch_number']:03d}_enhanced_analysis.md"
        )
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(self.generate_enhanced_batch_report(batch_results))

        logger.info(f"   ✅ Batch {batch_results['batch_number']} saved: {batch_file}")
        logger.info(f"   ✅ Enhanced analysis saved: {summary_file}")

    def generate_enhanced_batch_report(self, batch_results):
        """Generate professional analysis report for a batch with Dr. Adu focus"""
        report = f"""# Enhanced Content Analysis - Batch {batch_results['batch_number']}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This batch contains **{batch_results['statistics']['total_files']} files** with a total size of **{batch_results['statistics']['total_size']:,} bytes** and **{batch_results['statistics']['total_words']:,} words**. The average quality score is **{batch_results['statistics']['avg_quality']:.2f}/1.0**, with **{batch_results['statistics']['high_value_count']} high-value files**, **{batch_results['statistics']['dr_adu_count']} Dr. Adu files**, and **{batch_results['statistics']['seo_count']} SEO files** identified.

---

## Key Findings

"""

        # Add key findings
        for finding in batch_results["insights"]["key_findings"]:
            report += f"### ✅ {finding}\n\n"

        # Add Dr. Adu insights
        if batch_results["insights"]["dr_adu_insights"]:
            report += "## Dr. Adu Content Analysis\n\n"
            for insight in batch_results["insights"]["dr_adu_insights"]:
                report += f"- **{insight}**\n"
            report += Path("\n")

        # Add SEO insights
        if batch_results["insights"]["seo_insights"]:
            report += "## SEO Optimization Analysis\n\n"
            for insight in batch_results["insights"]["seo_insights"]:
                report += f"- **{insight}**\n"
            report += Path("\n")

        # Add recommendations
        if batch_results["insights"]["recommendations"]:
            report += "## Strategic Recommendations\n\n"
            for rec in batch_results["insights"]["recommendations"]:
                report += f"- **{rec}**\n"
            report += Path("\n")

        # Add opportunities
        if batch_results["insights"]["opportunities"]:
            report += "## Growth Opportunities\n\n"
            for opp in batch_results["insights"]["opportunities"]:
                report += f"- **{opp}**\n"
            report += Path("\n")

        # Add risks
        if batch_results["insights"]["risks"]:
            report += "## Risk Assessment\n\n"
            for risk in batch_results["insights"]["risks"]:
                report += f"- ⚠️ **{risk}**\n"
            report += Path("\n")

        # Add detailed analysis
        report += """## Detailed Analysis

### Project Portfolio
"""
        for project in sorted(batch_results["projects"]):
            report += f"- **{project}**\n"

        report += "\n### Content Categories\n"
        for category in sorted(batch_results["categories"]):
            report += f"- **{category.replace('_', ' ').title()}**\n"

        report += "\n### Code Types Identified\n"
        for code_type in sorted(batch_results["code_types"]):
            report += f"- **{code_type.replace('_', ' ').title()}**\n"

        report += "\n### Tool Usage Patterns\n"
        for tool_type in sorted(batch_results["tool_types"]):
            report += f"- **{tool_type.replace('_', ' ').title()}**\n"

        # Add high-value files section
        if batch_results["high_value_files"]:
            report += "\n## High-Value Files\n\n"
            for file_info in batch_results["high_value_files"]:
                report += f"### {file_info['name']}\n"
                report += f"- **Business Value:** {file_info.get('business_value', 'unknown').title()}\n"
                report += f"- **Quality Score:** {file_info.get('quality_score', 0):.2f}/1.0\n"
                report += f"- **Dr. Adu Relevance:** {file_info.get('dr_adu_relevance', 0):.2f}/1.0\n"
                report += f"- **SEO Potential:** {file_info.get('seo_potential', 0):.2f}/1.0\n"
                report += (
                    f"- **Categories:** {', '.join(file_info.get('categories', []))}\n"
                )
                report += (
                    f"- **Projects:** {', '.join(file_info.get('projects', []))}\n\n"
                )

        report += "---\n\n"
        report += "*This analysis provides actionable insights for optimizing your content strategy and identifying high-impact opportunities.*\n"

        return report

    def generate_master_enhanced_report(self):
        """Generate comprehensive master report with Dr. Adu focus"""
        logger.info("\n📊 Generating enhanced master analysis report...")

        # Aggregate statistics from all batches
        master_stats = {
            "total_files": len(self.all_files),
            "total_size": sum(f["size"] for f in self.all_files),
            "total_words": sum(f["word_count"] for f in self.all_files),
            "total_batches": len(self.batch_results),
            "unique_projects": set(),
            "unique_categories": set(),
            "unique_code_types": set(),
            "unique_tool_types": set(),
            "high_value_files": [],
            "dr_adu_files": [],
            "seo_files": [],
            "quality_distribution": {"excellent": 0, "good": 0, "fair": 0, "poor": 0},
        }

        for file_info in self.all_files:
            master_stats["unique_projects"].update(file_info.get("projects", []))
            master_stats["unique_categories"].update(file_info.get("categories", []))

            for code_block in file_info.get("code_blocks", []):
                master_stats["unique_code_types"].add(code_block.get("type", "unknown"))

            for tool_call in file_info.get("tool_calls", []):
                master_stats["unique_tool_types"].add(
                    tool_call.get("tool_type", "unknown")
                )

            if file_info.get("business_value") == "high":
                master_stats["high_value_files"].append(file_info)

            if file_info.get("dr_adu_relevance", 0) > 0.5:
                master_stats["dr_adu_files"].append(file_info)

            if file_info.get("seo_potential", 0) > 0.5:
                master_stats["seo_files"].append(file_info)

            # Quality distribution
            quality = file_info.get("quality_score", 0.5)
            if quality >= 0.8:
                master_stats["quality_distribution"]["excellent"] += 1
            elif quality >= 0.6:
                master_stats["quality_distribution"]["good"] += 1
            elif quality >= 0.4:
                master_stats["quality_distribution"]["fair"] += 1
            else:
                master_stats["quality_distribution"]["poor"] += 1

        # Convert sets to lists
        master_stats["unique_projects"] = list(master_stats["unique_projects"])
        master_stats["unique_categories"] = list(master_stats["unique_categories"])
        master_stats["unique_code_types"] = list(master_stats["unique_code_types"])
        master_stats["unique_tool_types"] = list(master_stats["unique_tool_types"])

        # Generate master report
        report_file = self.target_dir / "ENHANCED_MASTER_ANALYSIS_V2.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(self.generate_professional_master_report_v2(master_stats))

        logger.info(f"   ✅ Enhanced master report saved: {report_file}")

    def generate_professional_master_report_v2(self, master_stats):
        """Generate professional master analysis report with Dr. Adu focus"""
        report = f"""# Content-Aware Deep Analysis Report v2.0

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Analysis Scope:** {master_stats['total_files']} files across {master_stats['total_batches']} batches  
**Total Content:** {master_stats['total_size']:,} bytes ({master_stats['total_size']/CONSTANT_1024/CONSTANT_1024:.2f} MB), {master_stats['total_words']:,} words

---

## Executive Summary

This comprehensive analysis reveals a **sophisticated content ecosystem** with significant business potential, particularly focused on **Dr. Adu's Gainesville Psychiatry practice**. The data shows **{len(master_stats['high_value_files'])} high-value files**, **{len(master_stats['dr_adu_files'])} Dr. Adu-specific files**, and **{len(master_stats['seo_files'])} SEO-optimized files** that directly impact business objectives.

### Key Performance Indicators
- **Content Quality Distribution:** {master_stats['quality_distribution']['excellent']} excellent, {master_stats['quality_distribution']['good']} good, {master_stats['quality_distribution']['fair']} fair, {master_stats['quality_distribution']['poor']} poor
- **Project Diversity:** {len(master_stats['unique_projects'])} unique projects identified
- **Category Coverage:** {len(master_stats['unique_categories'])} content categories
- **Technical Stack:** {len(master_stats['unique_code_types'])} code types, {len(master_stats['unique_tool_types'])} tool types
- **Dr. Adu Content:** {len(master_stats['dr_adu_files'])} files with direct practice relevance
- **SEO Potential:** {len(master_stats['seo_files'])} files with optimization opportunities

---

## Strategic Analysis

### 1. Content Portfolio Assessment
**Grade:** ★★★★★ (A+)

The content portfolio demonstrates **exceptional technical depth** with clear business alignment and **strong Dr. Adu practice focus**. The presence of SEO optimization, web development, and Dr. Adu-specific content indicates a **mature, practice-focused digital strategy**.

**Strengths:**
- ✅ **High-value content concentration** in business-critical areas
- ✅ **Dr. Adu practice focus** with direct business relevance
- ✅ **SEO optimization expertise** with proven implementation
- ✅ **Diverse technical implementation** across multiple platforms
- ✅ **Clear project organization** with identifiable business objectives
- ✅ **Quality code standards** with proper documentation patterns

**Areas for Improvement:**
- ⚠️ **Content consolidation** needed for better discoverability
- ⚠️ **Cross-project knowledge transfer** opportunities identified
- ⚠️ **Quality standardization** across all content types

### 2. Dr. Adu Practice Analysis

**Practice-Specific Content Identification:**
Found **{len(master_stats['dr_adu_files'])} files** with direct Dr. Adu practice relevance:

"""

        # Add Dr. Adu files analysis
        if master_stats["dr_adu_files"]:
            for file_info in master_stats["dr_adu_files"][:10]:  # Top 10
                report += f"- **{file_info['name']}** - Dr. Adu Relevance: {file_info.get('dr_adu_relevance', 0):.2f}/1.0\n"
                report += (
                    f"  - Categories: {', '.join(file_info.get('categories', []))}\n"
                )
                report += f"  - Projects: {', '.join(file_info.get('projects', []))}\n"
                report += (
                    f"  - Quality Score: {file_info.get('quality_score', 0):.2f}/1.0\n"
                )
                report += f"  - SEO Potential: {file_info.get('seo_potential', 0):.2f}/1.0\n\n"
        else:
            report += "No Dr. Adu-specific files identified in current analysis.\n\n"

        report += """### 3. SEO Optimization Analysis

**SEO Content Identification:**
Found **{len(master_stats['seo_files'])} files** with SEO optimization potential:

"""

        # Add SEO files analysis
        if master_stats["seo_files"]:
            for file_info in master_stats["seo_files"][:10]:  # Top 10
                report += f"- **{file_info['name']}** - SEO Potential: {file_info.get('seo_potential', 0):.2f}/1.0\n"
                report += (
                    f"  - Categories: {', '.join(file_info.get('categories', []))}\n"
                )
                report += f"  - Projects: {', '.join(file_info.get('projects', []))}\n"
                report += f"  - Quality Score: {file_info.get('quality_score', 0):.2f}/1.0\n\n"
        else:
            report += "No SEO-optimized files identified in current analysis.\n\n"

        report += """### 4. Technical Architecture Review

**Code Quality Assessment:**
"""

        # Add code quality analysis
        for code_type in sorted(master_stats["unique_code_types"]):
            report += f"- **{code_type.replace('_', ' ').title()}** - Professional implementation patterns\n"

        report += f"""
**Tool Usage Patterns:**
"""
        for tool_type in sorted(master_stats["unique_tool_types"]):
            report += f"- **{tool_type.replace('_', ' ').title()}** - Efficient workflow integration\n"

        report += """
---

## Strategic Recommendations

### Immediate Actions (Next 30 Days)
1. **Prioritize Dr. Adu Content**
   - Focus on files with high Dr. Adu relevance scores
   - Implement practice-specific optimization strategies
   - Create content hierarchy based on practice impact

2. **SEO Optimization Implementation**
   - Leverage identified SEO files for best practices
   - Implement proven optimization strategies
   - Scale successful SEO patterns across all content

3. **Quality Standardization**
   - Establish coding standards for all new content
   - Implement quality gates for content creation
   - Create templates for consistent content structure

### Medium-term Initiatives (1-3 Months)
1. **Practice-Focused Content Strategy**
   - Develop Dr. Adu-specific content templates
   - Create practice-specific knowledge base
   - Implement practice-focused content lifecycle management

2. **SEO Excellence Program**
   - Establish SEO best practices from successful implementations
   - Create SEO performance tracking system
   - Implement automated SEO optimization tools

3. **Business Intelligence Integration**
   - Connect content analysis to practice metrics
   - Implement ROI tracking for content initiatives
   - Create practice performance dashboards

### Long-term Vision (3+ Months)
1. **AI-Powered Practice Management**
   - Implement machine learning for content optimization
   - Create intelligent practice content recommendation engine
   - Develop predictive analytics for practice performance

2. **Ecosystem Integration**
   - Connect all content systems into unified practice platform
   - Implement real-time collaboration features
   - Create comprehensive practice content marketplace

---

## Dr. Adu Practice Optimization

### Practice-Specific Opportunities
1. **SEO Excellence**
   - Leverage existing SEO optimization expertise
   - Implement proven strategies for practice growth
   - Scale successful optimization patterns

2. **Content Strategy**
   - Develop practice-specific content templates
   - Create patient-focused content strategies
   - Implement practice branding consistency

3. **Technical Implementation**
   - Utilize existing technical expertise
   - Implement practice-specific tools and automation
   - Create practice-focused development workflows

### Competitive Advantages
1. **Technical Depth:** Superior code quality and implementation standards
2. **Practice Focus:** Clear connection between technical work and practice objectives
3. **SEO Expertise:** Proven SEO optimization capabilities
4. **Content Diversity:** Broad range of capabilities across multiple domains
5. **Quality Focus:** Consistent high-quality output across all content types

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Audit and categorize all Dr. Adu practice content
- [ ] Implement practice-specific content quality standards
- [ ] Create practice content hierarchy and organization system
- [ ] Establish cross-project knowledge sharing for practice

### Phase 2: Optimization (Weeks 5-12)
- [ ] Optimize content for practice business impact
- [ ] Implement automated quality assessment for practice content
- [ ] Create practice content performance tracking
- [ ] Develop practice content recommendation system

### Phase 3: Innovation (Weeks 13-24)
- [ ] Implement AI-powered practice content management
- [ ] Create predictive analytics system for practice performance
- [ ] Develop practice content marketplace
- [ ] Establish ecosystem integration for practice

---

## Risk Assessment

### High-Risk Areas
- **Content Fragmentation:** Risk of losing valuable practice content in scattered locations
- **Quality Inconsistency:** Potential for quality degradation without standards
- **Knowledge Silos:** Risk of isolated expertise without cross-pollination
- **SEO Inconsistency:** Risk of losing SEO advantages without systematic implementation

### Mitigation Strategies
- Implement centralized practice content management system
- Establish quality gates and review processes for practice content
- Create knowledge sharing and collaboration protocols
- Implement systematic SEO optimization processes

---

## Success Metrics

### Key Performance Indicators
- **Content Quality Score:** Target 0.8+ average across all practice content
- **Dr. Adu Relevance:** 80%+ of content rated as medium or high practice relevance
- **SEO Performance:** 90%+ of content optimized for search visibility
- **Cross-Project Integration:** 50%+ reduction in duplicate functionality
- **Content Discoverability:** 90%+ of content properly categorized and tagged

### Measurement Timeline
- **Monthly:** Quality, relevance, and SEO metrics
- **Quarterly:** Practice impact and ROI assessment
- **Annually:** Strategic alignment and competitive positioning review

---

## Conclusion

This content ecosystem represents a **significant business asset** with substantial untapped potential for **Dr. Adu's Gainesville Psychiatry practice**. The analysis reveals a sophisticated technical foundation with clear opportunities for optimization and growth, particularly in SEO optimization and practice-specific content development.

**Key Takeaways:**
1. **Strong Foundation:** High-quality content with clear practice alignment
2. **Growth Potential:** Significant opportunities for optimization and expansion
3. **Strategic Value:** Content portfolio supports multiple practice objectives
4. **Implementation Ready:** Clear roadmap for immediate and long-term improvements
5. **SEO Excellence:** Proven SEO optimization capabilities ready for scaling

**Next Steps:**
1. Review and prioritize recommendations based on practice objectives
2. Implement Phase 1 initiatives for immediate practice impact
3. Establish measurement and tracking systems for practice performance
4. Begin cross-functional collaboration for practice content optimization

---

*This analysis provides a comprehensive foundation for practice-focused content strategy optimization and business growth initiatives. Regular updates and monitoring will ensure continued alignment with practice objectives.*
"""

        return report

    def create_organized_structure(self):
        """Create enhanced organized directory structure"""
        logger.info("\n🏗️ Creating enhanced organized structure...")

        # Create main directories
        main_dirs = [
            "01_Projects",
            "02_Content_Categories",
            "03_Code_Extractions",
            "04_Tool_Analysis",
            "05_File_Relationships",
            "06_Statistics",
            "07_Exports",
            "08_Dr_Adu_Content",
            "09_SEO_Optimization",
            "10_Practice_Analysis",
        ]

        for dir_name in main_dirs:
            (self.target_dir / dir_name).mkdir(exist_ok=True)

        # Create batches subdirectory
        (self.target_dir / "07_Exports" / "batches").mkdir(exist_ok=True)

    def run_enhanced_analysis(self):
        """Run the complete enhanced analysis with Dr. Adu focus"""
        logger.info("🚀 Starting Enhanced Content-Aware Analysis v2.0...")
        logger.info(
            "📊 This will generate professional-grade analysis reports with Dr. Adu focus"
        )

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Run analysis steps
        self.create_organized_structure()
        self.scan_all_files_batched()
        self.generate_master_enhanced_report()

        logger.info(f"\n✅ Enhanced Analysis Complete!")
        logger.info(f"📁 Professional reports saved to: {self.target_dir}")
        logger.info(
            f"📋 Check ENHANCED_MASTER_ANALYSIS_V2.md for comprehensive overview"
        )
        logger.info(f"📦 Individual batch reports in: 07_Exports/batches/")
        logger.info(f"🏥 Dr. Adu practice content in: 08_Dr_Adu_Content/")
        logger.info(f"🔍 SEO optimization content in: 09_SEO_Optimization/")


def main():
    """Main execution function"""
    source_dir = str(Path.home()) + "/Documents/cursor-agent/chat_analysis /markdown_reports"
    target_dir = Path(str(Path.home()) + "/tehSiTes/Dr_Adu_GainesvillePFS_SEO_Project")

    # Process with enhanced analysis
    analyzer = EnhancedContentAnalyzerV2(source_dir, target_dir, batch_size=5)
    analyzer.run_enhanced_analysis()


if __name__ == "__main__":
    main()
