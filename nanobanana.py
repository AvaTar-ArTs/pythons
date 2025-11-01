"""
Nanobanana

This module provides functionality for nanobanana.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
NanoBanana API Prompt Analyzer
Deep content-aware research on image/video prompts and NanoBanana API integration
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter, defaultdict
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class NanoBananaPromptAnalyzer:
    """Analyzes prompts and integrates with NanoBanana API for image/video generation"""

    def __init__(self, documents_root: Path):
        """__init__ function."""

        self.documents_root = documents_root
        self.prompt_collections = {
            "image_prompts": [],
            "video_prompts": [],
            "sora_prompts": [],
            "suno_prompts": [],
            "nanobanana_prompts": [],
            "dalle_prompts": [],
            "midjourney_prompts": [],
        }

        # NanoBanana API configuration
        self.nanobanana_config = {
            "base_url": "https://api.nanobananaapi.ai",
            "endpoints": {
                "generate": "/api/v1/nanobanana/generate",
                "task_details": "/api/v1/nanobanana/task/{task_id}",
            },
            "auth": "Bearer Token",
            "models": ["nanobanana-1.0", "veo3", "sora", "dalle-3"],
        }

        # Prompt patterns for different AI models
        self.prompt_patterns = {
            "dalle": [r"dall.*e", r"dalle", r"openai.*image", r"image.*generation"],
            "midjourney": [r"midjourney", r"mj", r"discord.*bot", r"--ar", r"--v"],
            "sora": [
                r"sora",
                r"video.*generation",
                r"txt.*to.*video",
                r"openai.*video",
            ],
            "suno": [
                r"suno",
                r"music.*generation",
                r"audio.*generation",
                r"song.*creation",
            ],
            "nanobanana": [r"nanobanana", r"veo3", r"video.*edit", r"image.*edit"],
        }

        # Content analysis keywords
        self.content_keywords = {
            "visual_style": [
                "cinematic",
                "photorealistic",
                "artistic",
                "stylized",
                "abstract",
                "vibrant",
                "moody",
                "dark",
                "bright",
                "colorful",
                "monochrome",
                "retro",
                "futuristic",
                "vintage",
                "modern",
                "classic",
            ],
            "composition": [
                "close-up",
                "wide-shot",
                "panoramic",
                "bird-eye",
                "low-angle",
                "high-angle",
                "dutch-angle",
                "overhead",
                "macro",
                "telephoto",
            ],
            "lighting": [
                "golden-hour",
                "blue-hour",
                "sunset",
                "sunrise",
                "moonlight",
                "studio-lighting",
                "natural-light",
                "dramatic",
                "soft",
                "harsh",
                "rim-light",
                "backlight",
                "side-light",
                "ambient",
            ],
            "mood": [
                "epic",
                "dramatic",
                "peaceful",
                "mysterious",
                "romantic",
                "melancholic",
                "hopeful",
                "nostalgic",
                "energetic",
                "calm",
                "tense",
                "joyful",
                "sad",
                "inspiring",
                "ominous",
            ],
            "technical": [
                "4k",
                "8k",
                "hd",
                "ultra-hd",
                "high-resolution",
                "crisp",
                "detailed",
                "sharp",
                "blur",
                "bokeh",
                "depth-of-field",
                "motion-blur",
                "slow-motion",
                "time-lapse",
                "hyperlapse",
            ],
        }

    def analyze_documents(self, max_depth: int = 6) -> Dict:
        """Analyze documents for prompt content with depth 6 search"""
        logger.info("🔍 Starting deep content-aware research on documents...")
        logger.info(f"📁 Target: {self.documents_root}")
        logger.info(f"🔍 Search depth: {max_depth}")
        logger.info("=" * 60)

        results = {
            "total_files_analyzed": 0,
            "prompt_files_found": 0,
            "prompt_collections": defaultdict(list),
            "api_integrations": [],
            "content_analysis": {},
            "recommendations": [],
        }

        # Search for prompt-related files
        prompt_files = self._find_prompt_files(max_depth)
        results["prompt_files_found"] = len(prompt_files)

        logger.info(f"📊 Found {len(prompt_files)} prompt-related files")

        # Analyze each file
        for file_path in prompt_files:
            try:
                analysis = self._analyze_prompt_file(file_path)
                if analysis:
                    results["prompt_collections"][analysis["type"]].append(analysis)
                    results["total_files_analyzed"] += 1
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")

        # Generate content analysis
        results["content_analysis"] = self._generate_content_analysis(
            results["prompt_collections"]
        )

        # Generate API integration recommendations
        results["api_integrations"] = self._generate_api_integrations(
            results["prompt_collections"]
        )

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _find_prompt_files(self, max_depth: int) -> List[Path]:
        """Find files containing prompt-related content"""
        prompt_files = []

        # Search patterns for different file types
        search_patterns = ["*.html", "*.md", "*.txt", "*.json", "*.py", "*.js", "*.css"]

        for pattern in search_patterns:
            for file_path in self.documents_root.rglob(pattern):
                if file_path.is_file() and self._is_prompt_related(file_path):
                    prompt_files.append(file_path)

        return prompt_files

    def _is_prompt_related(self, file_path: Path) -> bool:
        """Check if file contains prompt-related content"""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore").lower()

            # Check for prompt keywords
            prompt_keywords = [
                "prompt",
                "image generation",
                "video generation",
                "dall-e",
                "midjourney",
                "sora",
                "suno",
                "nanobanana",
                "veo3",
                "stable diffusion",
                "txt to video",
                "image to video",
                "text to image",
                "ai art",
                "generative art",
            ]

            return any(keyword in content for keyword in prompt_keywords)
        except Exception:
            return False

    def _analyze_prompt_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single prompt file"""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            analysis = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "type": self._classify_prompt_type(content),
                "prompts": self._extract_prompts(content),
                "keywords": self._extract_keywords(content),
                "visual_elements": self._extract_visual_elements(content),
                "technical_specs": self._extract_technical_specs(content),
                "api_mentions": self._extract_api_mentions(content),
                "content_length": len(content),
                "prompt_count": 0,
            }

            analysis["prompt_count"] = len(analysis["prompts"])

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return None

    def _classify_prompt_type(self, content: str) -> str:
        """Classify the type of prompt content"""
        content_lower = content.lower()

        for prompt_type, patterns in self.prompt_patterns.items():
            if any(re.search(pattern, content_lower) for pattern in patterns):
                return prompt_type

        # Default classification based on content
        if "video" in content_lower and "generation" in content_lower:
            return "video_prompts"
        elif "image" in content_lower and "generation" in content_lower:
            return "image_prompts"
        else:
            return "general_prompts"

    def _extract_prompts(self, content: str) -> List[Dict]:
        """Extract individual prompts from content"""
        prompts = []

        # Look for prompt patterns
        prompt_patterns = [
            r'prompt["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'description["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'prompt["\']?\s*[:=]\s*`([^`]+)`',
            r'description["\']?\s*[:=]\s*`([^`]+)`',
            r"<prompt>([^<]+)</prompt>",
            r"<description>([^<]+)</description>",
        ]

        for pattern in prompt_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:  # Filter out very short matches
                    prompts.append(
                        {
                            "text": match.strip(),
                            "length": len(match.strip()),
                            "type": "extracted",
                        }
                    )

        return prompts

    def _extract_keywords(self, content: str) -> Dict[str, List[str]]:
        """Extract keywords by category"""
        content_lower = content.lower()
        keywords = {}

        for category, words in self.content_keywords.items():
            found_words = [word for word in words if word in content_lower]
            if found_words:
                keywords[category] = found_words

        return keywords

    def _extract_visual_elements(self, content: str) -> List[str]:
        """Extract visual elements from content"""
        visual_elements = []

        # Common visual element patterns
        patterns = [
            r"(\d+:\d+)\s*aspect\s*ratio",
            r"(\d+[kK])\s*resolution",
            r"(cinematic|photorealistic|artistic|stylized)",
            r"(close-up|wide-shot|panoramic|bird-eye)",
            r"(golden-hour|blue-hour|sunset|sunrise)",
            r"(epic|dramatic|peaceful|mysterious)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            visual_elements.extend(matches)

        return list(set(visual_elements))

    def _extract_technical_specs(self, content: str) -> Dict[str, str]:
        """Extract technical specifications"""
        specs = {}

        # Resolution patterns
        resolution_match = re.search(r"(\d+[x×]\d+)", content)
        if resolution_match:
            specs["resolution"] = resolution_match.group(1)

        # Aspect ratio patterns
        aspect_match = re.search(r"(\d+:\d+)", content)
        if aspect_match:
            specs["aspect_ratio"] = aspect_match.group(1)

        # Quality patterns
        quality_match = re.search(
            r"(4[kK]|8[kK]|HD|UHD|ultra-hd)", content, re.IGNORECASE
        )
        if quality_match:
            specs["quality"] = quality_match.group(1)

        return specs

    def _extract_api_mentions(self, content: str) -> List[str]:
        """Extract API mentions from content"""
        apis = []
        content_lower = content.lower()

        api_keywords = [
            "openai",
            "dall-e",
            "sora",
            "suno",
            "nanobanana",
            "veo3",
            "midjourney",
            "stable diffusion",
            "runway",
            "pika",
            "leia",
        ]

        for api in api_keywords:
            if api in content_lower:
                apis.append(api)

        return apis

    def _generate_content_analysis(self, prompt_collections: Dict) -> Dict:
        """Generate comprehensive content analysis"""
        analysis = {
            "total_prompts": 0,
            "prompt_types": {},
            "common_keywords": {},
            "visual_trends": {},
            "technical_trends": {},
            "api_usage": {},
        }

        for prompt_type, files in prompt_collections.items():
            analysis["prompt_types"][prompt_type] = len(files)

            for file_data in files:
                analysis["total_prompts"] += file_data["prompt_count"]

                # Aggregate keywords
                for category, keywords in file_data["keywords"].items():
                    if category not in analysis["common_keywords"]:
                        analysis["common_keywords"][category] = Counter()
                    analysis["common_keywords"][category].update(keywords)

                # Aggregate API usage
                for api in file_data["api_mentions"]:
                    analysis["api_usage"][api] = analysis["api_usage"].get(api, 0) + 1

        return analysis

    def _generate_api_integrations(self, prompt_collections: Dict) -> List[Dict]:
        """Generate API integration recommendations"""
        integrations = []

        # NanoBanana API integration
        nanobanana_integration = {
            "api": "NanoBanana",
            "endpoint": self.nanobanana_config["endpoints"]["generate"],
            "use_cases": [
                "Image generation and editing",
                "Video generation and editing",
                "Text-to-video conversion",
                "Image-to-video conversion",
            ],
            "prompt_optimization": [
                "Use detailed descriptive prompts",
                "Include technical specifications",
                "Specify aspect ratios and resolution",
                "Add mood and style descriptors",
            ],
            "example_prompts": self._generate_nanobanana_examples(prompt_collections),
        }

        integrations.append(nanobanana_integration)

        return integrations

    def _generate_nanobanana_examples(self, prompt_collections: Dict) -> List[Dict]:
        """Generate example prompts for NanoBanana API"""
        examples = []

        # Extract high-quality prompts from collections
        for prompt_type, files in prompt_collections.items():
            for file_data in files:
                for prompt in file_data["prompts"][:3]:  # Take first 3 prompts
                    if len(prompt["text"]) > 50:  # Only substantial prompts
                        examples.append(
                            {
                                "original_prompt": prompt["text"],
                                "nanobanana_optimized": self._optimize_for_nanobanana(
                                    prompt["text"]
                                ),
                                "type": prompt_type,
                                "technical_specs": file_data["technical_specs"],
                            }
                        )

        return examples[:10]  # Return top 10 examples

    def _optimize_for_nanobanana(self, prompt: str) -> str:
        """Optimize a prompt for NanoBanana API"""
        # Add technical specifications if missing
        if "4k" not in prompt.lower() and "hd" not in prompt.lower():
            prompt += ", 4K resolution"

        if "cinematic" not in prompt.lower():
            prompt += ", cinematic quality"

        # Add style descriptors
        if "detailed" not in prompt.lower():
            prompt += ", highly detailed"

        return prompt

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Based on content analysis
        if results["content_analysis"]["total_prompts"] > CONSTANT_100:
            recommendations.append("Consider creating a centralized prompt database")

        if "nanobanana" in results["content_analysis"]["api_usage"]:
            recommendations.append(
                "Integrate NanoBanana API for advanced video generation"
            )

        if results["content_analysis"]["prompt_types"].get("image_prompts", 0) > 50:
            recommendations.append(
                "Implement batch image generation with NanoBanana API"
            )

        if results["content_analysis"]["prompt_types"].get("video_prompts", 0) > 20:
            recommendations.append("Set up automated video generation pipeline")

        return recommendations

    def generate_nanobanana_prompts(self, analysis_results: Dict) -> Dict:
        """Generate optimized prompts for NanoBanana API"""
        logger.info("🎨 Generating NanoBanana API optimized prompts...")

        nanobanana_prompts = {
            "image_generation": [],
            "video_generation": [],
            "image_editing": [],
            "video_editing": [],
        }

        # Process each prompt collection
        for prompt_type, files in analysis_results["prompt_collections"].items():
            for file_data in files:
                for prompt in file_data["prompts"]:
                    optimized = self._create_nanobanana_prompt(prompt, file_data)
                    if optimized:
                        nanobanana_prompts[optimized["category"]].append(optimized)

        return nanobanana_prompts

    def _create_nanobanana_prompt(
        self, prompt: Dict, file_data: Dict
    ) -> Optional[Dict]:
        """Create a NanoBanana-optimized prompt"""
        original_text = prompt["text"]

        # Determine category based on content
        if "video" in original_text.lower() or "motion" in original_text.lower():
            category = "video_generation"
        elif "edit" in original_text.lower() or "modify" in original_text.lower():
            category = (
                "image_editing" if "image" in original_text.lower() else "video_editing"
            )
        else:
            category = "image_generation"

        # Optimize the prompt
        optimized_text = self._optimize_for_nanobanana(original_text)

        return {
            "original_prompt": original_text,
            "optimized_prompt": optimized_text,
            "category": category,
            "technical_specs": file_data["technical_specs"],
            "keywords": file_data["keywords"],
            "api_endpoint": self.nanobanana_config["endpoints"]["generate"],
            "model": "nanobanana-1.0",
        }

    def export_analysis(self, results: Dict, output_path: Path):
        """Export analysis results to JSON"""
        output_path.write_text(json.dumps(results, indent=2, default=str))
        logger.info(f"📄 Analysis exported to {output_path}")

    def run_complete_analysis(self) -> Dict:
        """Run the complete analysis pipeline"""
        logger.info("🚀 Starting NanoBanana Prompt Analysis...")
        logger.info("=" * 60)

        # Analyze documents
        analysis_results = self.analyze_documents(max_depth=6)

        # Generate NanoBanana prompts
        nanobanana_prompts = self.generate_nanobanana_prompts(analysis_results)
        analysis_results["nanobanana_prompts"] = nanobanana_prompts

        # Export results
        output_path = self.documents_root / "nanobanana_analysis_results.json"
        self.export_analysis(analysis_results, output_path)

        # Print summary
        self._print_analysis_summary(analysis_results)

        return analysis_results

    def _print_analysis_summary(self, results: Dict):
        """Print analysis summary"""
        logger.info("\n📊 Analysis Summary:")
        logger.info("=" * 40)
        logger.info(f"📁 Files analyzed: {results['total_files_analyzed']}")
        logger.info(
            f"🎨 Total prompts found: {results['content_analysis']['total_prompts']}"
        )
        logger.info(f"🔧 API integrations: {len(results['api_integrations'])}")
        logger.info(f"💡 Recommendations: {len(results['recommendations'])}")

        logger.info("\n🎯 Prompt Types:")
        for prompt_type, count in results["content_analysis"]["prompt_types"].items():
            logger.info(f"   {prompt_type}: {count} files")

        logger.info("\n🔌 API Usage:")
        for api, count in results["content_analysis"]["api_usage"].items():
            logger.info(f"   {api}: {count} mentions")

        logger.info("\n💡 Recommendations:")
        for rec in results["recommendations"]:
            logger.info(f"   • {rec}")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="NanoBanana API Prompt Analyzer")
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.home() / "Documents",
        help="Documents directory to analyze (default: ~/Documents)",
    )
    parser.add_argument(
        "--depth", type=int, default=6, help="Search depth (default: 6)"
    )
    parser.add_argument("--export", type=Path, help="Export results to specific file")

    args = parser.parse_args()

    analyzer = NanoBananaPromptAnalyzer(args.path)
    results = analyzer.run_complete_analysis()

    if args.export:
        analyzer.export_analysis(results, args.export)


if __name__ == "__main__":
    main()
