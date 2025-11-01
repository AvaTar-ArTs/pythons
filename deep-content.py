"""
Ai Deep

This module provides functionality for ai deep.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_120 = 120
CONSTANT_1000 = 1000
CONSTANT_5000 = 5000
CONSTANT_50000 = 50000
CONSTANT_100000 = 100000

#!/usr/bin/env python3
"""
AI-Powered Deep Analyzer with Content-Awareness
Combines structural analysis with AI-powered insights
"""

import os
import sys
import json
import re
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AIAnalysisResult:
    content_type: str
    structure: Dict[str, Any]
    key_insights: List[str]
    recommendations: List[str]
    technical_details: Dict[str, Any]
    ai_insights: Dict[str, Any]
    summary: str


class AIDeepAnalyzer:
    def __init__(self):
        """__init__ function."""

        self.content_patterns = {
            "prompt_engineering": [
                r"{{[^}]+}}",  # Template variables
                r"<[^>]+>",  # XML-like tags
                r"#+\s+",  # Headers
                r"```[\s\S]*?```",  # Code blocks
                r"&[a-zA-Z]+;",  # HTML entities
            ],
            "visual_design": [
                r"color|font|style|design|visual|image|graphic",
                r"typography|layout|composition|aesthetic",
                r"brand|identity|logo|icon",
            ],
            "narrative_structure": [
                r"story|narrative|plot|character|scene|setting",
                r"beginning|middle|end|arc|journey",
                r"conflict|resolution|theme|message",
            ],
            "technical_implementation": [
                r"api|endpoint|request|response|json|xml",
                r"function|method|class|variable|parameter",
                r"config|setting|option|parameter",
            ],
        }

    def detect_content_type(self, content: str) -> str:
        """Detect the type of content being analyzed"""
        content_lower = content.lower()

        if "prompt" in content_lower and "template" in content_lower:
            return "prompt_template"
        elif "{{" in content and "}}" in content:
            return "template_with_variables"
        elif (
            "<" in content and ">" in content and not content.count("<") > CONSTANT_100
        ):
            return "structured_markup"
        elif "```" in content:
            return "code_documentation"
        elif any(
            keyword in content_lower for keyword in ["story", "narrative", "character"]
        ):
            return "narrative_content"
        elif any(
            keyword in content_lower for keyword in ["api", "endpoint", "function"]
        ):
            return "technical_documentation"
        else:
            return "general_text"

    def analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze the structural elements of the content"""
        structure = {
            "length": len(content),
            "lines": len(content.split("\n")),
            "paragraphs": len([p for p in content.split("\n\n") if p.strip()]),
            "headers": len(re.findall(r"^#+\s+", content, re.MULTILINE)),
            "code_blocks": len(re.findall(r"```[\s\S]*?```", content)),
            "template_variables": len(re.findall(r"{{[^}]+}}", content)),
            "xml_tags": len(re.findall(r"<[^>]+>", content)),
            "html_entities": len(re.findall(r"&[a-zA-Z]+;", content)),
        }

        words = len(content.split())
        structure["word_count"] = words
        structure["avg_words_per_line"] = words / max(structure["lines"], 1)
        structure["avg_chars_per_line"] = len(content) / max(structure["lines"], 1)

        return structure

    def extract_key_insights(self, content: str, content_type: str) -> List[str]:
        """Extract key insights based on content type"""
        insights = []

        if content_type == "prompt_template":
            variables = re.findall(r"{{[^}]+}}", content)
            if variables:
                insights.append(
                    f"Uses {len(variables)} template variables for dynamic content"
                )

            sections = re.findall(r"#+\s+[^\n]+", content)
            if sections:
                insights.append(f"Organized into {len(sections)} clear sections")

            if "step" in content.lower() and "process" in content.lower():
                insights.append("Implements step-by-step processing methodology")

            if "target" in content.lower() and "audience" in content.lower():
                insights.append("Includes audience targeting considerations")

        elif content_type == "template_with_variables":
            var_types = set()
            for var in re.findall(r"{{[^}]+}}", content):
                var_clean = var.strip("{}").strip()
                if "_" in var_clean:
                    var_types.add("snake_case")
                elif var_clean.isupper():
                    var_types.add("UPPER_CASE")
                else:
                    var_types.add("mixed_case")

            insights.append(f"Uses {', '.join(var_types)} variable naming conventions")

        if "creative" in content.lower() or "artistic" in content.lower():
            insights.append("Emphasizes creative and artistic elements")

        if "technical" in content.lower() or "implementation" in content.lower():
            insights.append("Contains technical implementation details")

        if "user" in content.lower() and "experience" in content.lower():
            insights.append("Focuses on user experience considerations")

        return insights

    def generate_recommendations(
        self, content: str, content_type: str, structure: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []

        if structure["lines"] > CONSTANT_1000:
            recommendations.append(
                "Consider breaking into smaller, more manageable sections"
            )

        if structure["avg_chars_per_line"] > CONSTANT_100:
            recommendations.append(
                "Lines are quite long - consider adding line breaks for readability"
            )

        if structure["headers"] < 3 and structure["lines"] > CONSTANT_100:
            recommendations.append("Add more section headers to improve navigation")

        if content_type == "prompt_template":
            if structure["template_variables"] == 0:
                recommendations.append(
                    "Consider adding template variables for dynamic content"
                )

            if not re.search(r"#+\s+", content):
                recommendations.append(
                    "Add clear section headers to organize the prompt"
                )

            if not re.search(r"example|sample|demo", content, re.IGNORECASE):
                recommendations.append("Include examples or samples to clarify usage")

        if structure["word_count"] > CONSTANT_5000:
            recommendations.append(
                "Content is quite extensive - consider adding a table of contents"
            )

        if not re.search(r"conclusion|summary|wrap.up", content, re.IGNORECASE):
            recommendations.append("Add a conclusion or summary section")

        return recommendations

    def analyze_technical_details(self, content: str) -> Dict[str, Any]:
        """Analyze technical aspects of the content"""
        technical = {
            "encoding_issues": [],
            "formatting_consistency": True,
            "template_complexity": 0,
            "accessibility_concerns": [],
            "performance_considerations": [],
        }

        if "&#" in content:
            technical["encoding_issues"].append(
                "Contains HTML entities that may need decoding"
            )

        if "&amp;" in content or "&lt;" in content:
            technical["encoding_issues"].append("Contains HTML-encoded characters")

        lines = content.split("\n")
        indentations = [
            len(line) - len(line.lstrip()) for line in lines if line.strip()
        ]
        if len(set(indentations)) > 3:
            technical["formatting_consistency"] = False

        variables = re.findall(r"{{[^}]+}}", content)
        technical["template_complexity"] = len(variables)

        if not re.search(r"alt\s*=|aria-", content, re.IGNORECASE):
            technical["accessibility_concerns"].append(
                "No accessibility attributes found"
            )

        if len(content) > CONSTANT_100000:
            technical["performance_considerations"].append(
                "Large file size may impact loading performance"
            )

        return technical

    def run_ai_analysis(
        self, content: str, ai_service: str = "claude"
    ) -> Dict[str, Any]:
        """Run AI analysis on the content"""
        # Truncate content if too long for AI processing
        max_length = CONSTANT_50000  # Adjust based on AI service limits
        if len(content) > max_length:
            content_sample = (
                content[:max_length] + "\n\n[Content truncated for analysis...]"
            )
        else:
            content_sample = content

        # Create analysis prompt
        analysis_prompt = f"""
        Please provide a comprehensive analysis of this content. Focus on:

        1. **Content Structure & Organization**: How is the information organized? What patterns do you see?
        2. **Prompt Engineering Techniques**: What specific techniques are used for prompt design?
        3. **Visual Design Elements**: What visual and design considerations are present?
        4. **Narrative Flow**: How does the storytelling or information flow work?
        5. **Target Audience**: Who is this content designed for and how does it appeal to them?
        6. **Technical Implementation**: What technical aspects are noteworthy?
        7. **Strengths & Weaknesses**: What works well and what could be improved?
        8. **Creative Insights**: Any unique or innovative approaches used?

        Please provide specific examples from the content and actionable recommendations.

        Content to analyze:
        {content_sample}
        """

        try:
            if ai_service == "claude":
                # Use Claude CLI
                result = subprocess.run(
                    ["python3", os.path.expanduser("~/claude-cli.py"), analysis_prompt],
                    capture_output=True,
                    text=True,
                    timeout=CONSTANT_120,
                )
                if result.returncode == 0:
                    return {
                        "success": True,
                        "analysis": result.stdout,
                        "service": "claude",
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Claude analysis failed: {result.stderr}",
                        "service": "claude",
                    }
            elif ai_service == "xai":
                # Use xAI CLI
                result = subprocess.run(
                    ["python3", os.path.expanduser("~/xai-cli.py"), analysis_prompt],
                    capture_output=True,
                    text=True,
                    timeout=CONSTANT_120,
                )
                if result.returncode == 0:
                    return {
                        "success": True,
                        "analysis": result.stdout,
                        "service": "xai",
                    }
                else:
                    return {
                        "success": False,
                        "error": f"xAI analysis failed: {result.stderr}",
                        "service": "xai",
                    }
            else:
                return {
                    "success": False,
                    "error": f"Unsupported AI service: {ai_service}",
                    "service": ai_service,
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"AI analysis timed out after CONSTANT_120 seconds",
                "service": ai_service,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error running AI analysis: {e}",
                "service": ai_service,
            }

    def generate_summary(
        self, content_type: str, structure: Dict[str, Any], insights: List[str]
    ) -> str:
        """Generate a comprehensive summary"""
        summary_parts = []

        summary_parts.append(f"This is a {content_type.replace('_', ' ')} document")
        summary_parts.append(
            f"containing {structure['word_count']:,} words across {structure['lines']} lines"
        )

        if structure["template_variables"] > 0:
            summary_parts.append(
                f"with {structure['template_variables']} template variables"
            )

        if structure["headers"] > 0:
            summary_parts.append(f"organized into {structure['headers']} sections")

        if insights:
            key_insight = insights[0] if insights else "standard content"
            summary_parts.append(f"featuring {key_insight.lower()}")

        return ". ".join(summary_parts) + "."

    def analyze_file(
        self, file_path: str, ai_service: str = "claude"
    ) -> AIAnalysisResult:
        """Perform deep analysis of a file with AI insights"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

        # Detect content type
        content_type = self.detect_content_type(content)

        # Analyze structure
        structure = self.analyze_structure(content)

        # Extract insights
        insights = self.extract_key_insights(content, content_type)

        # Generate recommendations
        recommendations = self.generate_recommendations(
            content, content_type, structure
        )

        # Analyze technical details
        technical_details = self.analyze_technical_details(content)

        # Run AI analysis
        ai_insights = self.run_ai_analysis(content, ai_service)

        # Generate summary
        summary = self.generate_summary(content_type, structure, insights)

        return AIAnalysisResult(
            content_type=content_type,
            structure=structure,
            key_insights=insights,
            recommendations=recommendations,
            technical_details=technical_details,
            ai_insights=ai_insights,
            summary=summary,
        )

    def print_analysis(self, result: AIAnalysisResult, file_path: str):
        """Print formatted analysis results"""
        logger.info(
            f"\n🔍 AI-Powered Deep Analysis Report: {os.path.basename(file_path)}"
        )
        logger.info("=" * 80)

        logger.info(f"\n📋 SUMMARY:")
        logger.info(f"   {result.summary}")

        logger.info(f"\n🏗️  STRUCTURE ANALYSIS:")
        logger.info(f"   Content Type: {result.content_type.replace('_', ' ').title()}")
        logger.info(f"   Word Count: {result.structure['word_count']:,}")
        logger.info(f"   Lines: {result.structure['lines']:,}")
        logger.info(f"   Paragraphs: {result.structure['paragraphs']:,}")
        logger.info(f"   Headers: {result.structure['headers']:,}")
        logger.info(
            f"   Template Variables: {result.structure['template_variables']:,}"
        )
        logger.info(f"   Code Blocks: {result.structure['code_blocks']:,}")
        logger.info(
            f"   Average Words/Line: {result.structure['avg_words_per_line']:.1f}"
        )

        if result.key_insights:
            logger.info(f"\n💡 KEY INSIGHTS:")
            for i, insight in enumerate(result.key_insights, 1):
                logger.info(f"   {i}. {insight}")

        if result.recommendations:
            logger.info(f"\n🎯 RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations, 1):
                logger.info(f"   {i}. {rec}")

        logger.info(f"\n⚙️  TECHNICAL DETAILS:")
        logger.info(
            f"   Formatting Consistent: {'✅' if result.technical_details['formatting_consistency'] else '❌'}"
        )
        logger.info(
            f"   Template Complexity: {result.technical_details['template_complexity']}"
        )

        if result.technical_details["encoding_issues"]:
            logger.info(f"   Encoding Issues:")
            for issue in result.technical_details["encoding_issues"]:
                logger.info(f"     • {issue}")

        if result.technical_details["accessibility_concerns"]:
            logger.info(f"   Accessibility Concerns:")
            for concern in result.technical_details["accessibility_concerns"]:
                logger.info(f"     • {concern}")

        if result.technical_details["performance_considerations"]:
            logger.info(f"   Performance Considerations:")
            for consideration in result.technical_details["performance_considerations"]:
                logger.info(f"     • {consideration}")

        logger.info(
            f"\n🤖 AI ANALYSIS ({result.ai_insights.get('service', 'unknown').upper()}):"
        )
        if result.ai_insights.get("success", False):
            logger.info("   ✅ AI analysis completed successfully")
            logger.info(
                f"\n   {result.ai_insights.get('analysis', 'No analysis available')}"
            )
        else:
            logger.info("   ❌ AI analysis failed")
            logger.info(f"   Error: {result.ai_insights.get('error', 'Unknown error')}")


def main():
    """main function."""

    if len(sys.argv) < 2:
        logger.info("Usage: ai-deep-analyzer.py <file_path> [ai_service]")
        logger.info("Available AI services: claude, xai")
        sys.exit(1)

    file_path = sys.argv[1]
    ai_service = sys.argv[2] if len(sys.argv) > 2 else "claude"

    if not os.path.exists(file_path):
        logger.info(f"Error: File '{file_path}' not found")
        sys.exit(1)

    if ai_service not in ["claude", "xai"]:
        logger.info(
            f"Error: Unsupported AI service '{ai_service}'. Use 'claude' or 'xai'"
        )
        sys.exit(1)

    analyzer = AIDeepAnalyzer()

    try:
        logger.info(
            f"🔍 Analyzing {os.path.basename(file_path)} with {ai_service.upper()}..."
        )
        result = analyzer.analyze_file(file_path, ai_service)
        analyzer.print_analysis(result, file_path)
    except Exception as e:
        logger.info(f"Error analyzing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
