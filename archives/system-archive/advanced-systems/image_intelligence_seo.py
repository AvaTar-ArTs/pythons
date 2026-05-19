#!/usr/bin/env python3
"""
🖼️ IMAGE INTELLIGENCE & SEO ANALYZER
=====================================
AI-powered image analysis, optimization, and SEO metadata generation.

Features:
✨ AI-powered image captioning (GPT-4 Vision, Gemini Vision)
🏷️ Automatic alt text generation for accessibility
🔍 SEO-optimized filename suggestions
📊 Image quality and optimization analysis
🎨 Visual content analysis (colors, composition, subjects)
📝 Metadata extraction and enhancement (EXIF, IPTC)
🔗 Smart tagging and categorization
📦 Batch processing for entire directories
🌐 Web optimization recommendations
🎯 Integration-ready for content pipeline
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path
from collections import Counter
import re

# Image processing
try:
    from PIL import Image
    from PIL.ExifTags import TAGS

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL not available. Install: pip install Pillow")

# API Clients
try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

import base64
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImageIntelligence:
    """
    Intelligent image analysis and SEO optimization system
    """

    def __init__(self):
        self.load_environment()
        self.initialize_clients()
        self.supported_formats = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".tiff",
        }

    def load_environment(self):
        """Load API keys from ~/.env.d/"""
        env_paths = [
            Path.home() / ".env.d" / "llm-apis.env",
            Path.home() / ".env.d" / "art-vision.env",
            Path.home() / ".env.d" / "gemini.env",
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                logger.info(f"✅ Loaded environment from {env_path}")

    def initialize_clients(self):
        """Initialize AI vision clients"""
        self.clients = {}

        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.clients["openai"] = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("✅ OpenAI GPT-4 Vision initialized")

        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.clients["anthropic"] = Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            logger.info("✅ Anthropic Claude Vision initialized")

        if GEMINI_AVAILABLE and os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.clients["gemini"] = genai.GenerativeModel("gemini-pro-vision")
            logger.info("✅ Google Gemini Vision initialized")

        if not self.clients:
            logger.warning(
                "⚠️  No AI vision clients available. Image analysis will be limited."
            )

    # ============================================================================
    # 🔍 IMAGE ANALYSIS
    # ============================================================================

    async def analyze_image(self, image_path: Path) -> Dict[str, Any]:
        """
        Comprehensive image analysis
        Returns technical details, AI analysis, and SEO recommendations
        """
        if not image_path.exists():
            return {"error": "Image not found"}

        result = {
            "file_path": str(image_path),
            "file_name": image_path.name,
            "analyzed_at": datetime.now().isoformat(),
        }

        # Technical analysis
        result["technical"] = await self._analyze_technical(image_path)

        # AI vision analysis
        result["ai_analysis"] = await self._analyze_with_ai(image_path)

        # SEO optimization
        result["seo"] = await self._generate_seo_metadata(
            image_path, result["ai_analysis"]
        )

        # Quality score
        result["quality_score"] = self._calculate_quality_score(result)

        # Optimization recommendations
        result["recommendations"] = self._generate_recommendations(result)

        return result

    async def _analyze_technical(self, image_path: Path) -> Dict[str, Any]:
        """Extract technical image information"""
        technical = {}

        try:
            if PIL_AVAILABLE:
                with Image.open(image_path) as img:
                    technical["format"] = img.format
                    technical["mode"] = img.mode
                    technical["width"] = img.width
                    technical["height"] = img.height
                    technical["dimensions"] = f"{img.width}x{img.height}"
                    technical["aspect_ratio"] = round(img.width / img.height, 2)

                    # File size
                    file_size = image_path.stat().st_size
                    technical["file_size_bytes"] = file_size
                    technical["file_size_kb"] = round(file_size / 1024, 2)
                    technical["file_size_mb"] = round(file_size / (1024 * 1024), 2)

                    # EXIF data
                    exif_data = img.getexif()
                    if exif_data:
                        exif = {}
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            exif[tag] = str(value)
                        technical["exif"] = exif

                    # Color analysis
                    if img.mode == "RGB":
                        colors = img.getcolors(maxcolors=10)
                        if colors:
                            dominant_colors = sorted(colors, reverse=True)[:5]
                            technical["dominant_colors"] = [
                                {"count": count, "rgb": color}
                                for count, color in dominant_colors
                            ]
            else:
                # Fallback without PIL
                file_size = image_path.stat().st_size
                technical["file_size_bytes"] = file_size
                technical["file_size_kb"] = round(file_size / 1024, 2)
                technical["format"] = image_path.suffix

        except Exception as e:
            logger.error(f"Technical analysis failed: {e}")
            technical["error"] = str(e)

        return technical

    async def _analyze_with_ai(self, image_path: Path) -> Dict[str, Any]:
        """
        Analyze image using AI vision models
        Generates description, objects, scene analysis
        """
        analysis = {}

        try:
            # Encode image to base64
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            # Try GPT-4 Vision first
            if "openai" in self.clients:
                analysis = await self._analyze_with_gpt4_vision(image_path, image_data)

            # Fallback to Gemini Vision
            elif "gemini" in self.clients:
                analysis = await self._analyze_with_gemini_vision(image_path)

            # Fallback to basic analysis
            else:
                analysis = self._basic_image_analysis(image_path)

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            analysis["error"] = str(e)
            analysis["description"] = self._generate_basic_description(image_path)

        return analysis

    async def _analyze_with_gpt4_vision(:
        self, image_path: Path, image_data: str
    ) -> Dict[str, Any]:
        """Analyze image using GPT-4 Vision"""
        try:
            response = self.clients["openai"].chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this image and provide:
                                1. Detailed description (2-3 sentences)
                                2. Main subjects/objects (comma-separated list)
                                3. Scene/setting
                                4. Mood/tone
                                5. Suggested keywords for SEO (10 keywords)
                                6. Recommended alt text (descriptive, accessible)

                                Format as JSON with keys: description, objects, scene, mood, keywords, alt_text""",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            # Parse response
            content = response.choices[0].message.content

            # Try to extract JSON
            try:
                # Look for JSON in response
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    # Parse as text
                    analysis = {
                        "description": content[:200],
                        "provider": "gpt4-vision",
                        "raw_response": content,
                    }
            except:
                analysis = {"description": content, "provider": "gpt4-vision"}

            return analysis

        except Exception as e:
            logger.error(f"GPT-4 Vision failed: {e}")
            return {"error": str(e)}

    async def _analyze_with_gemini_vision(self, image_path: Path) -> Dict[str, Any]:
        """Analyze image using Gemini Vision"""
        try:
            if PIL_AVAILABLE:

                prompt = """Analyze this image and provide:
                1. Detailed description
                2. Main subjects/objects
                3. Scene/setting
                4. SEO keywords
                5. Alt text for accessibility
                """

                response = self.clients["gemini"].generate_content([prompt, img])

                return {"description": response.text, "provider": "gemini-vision"}
        except Exception as e:
            logger.error(f"Gemini Vision failed: {e}")
            return {"error": str(e)}

    def _basic_image_analysis(self, image_path: Path) -> Dict[str, Any]:
        """Basic analysis without AI vision"""
        # Extract info from filename and path
        name = image_path.stem

        # Clean filename for analysis
        clean_name = re.sub(r"[_-]", " ", name)
        clean_name = re.sub(r"\d+", "", clean_name).strip()

        return {
            "description": f"Image: {clean_name}",
            "inferred_subject": clean_name,
            "provider": "basic",
            "note": "AI vision not available. Install OpenAI or Google AI SDK.",
        }

    def _generate_basic_description(self, image_path: Path) -> str:
        """Generate basic description from filename"""
        name = image_path.stem
        clean = re.sub(r"[_-]", " ", name)
        return f"Image showing {clean}"

    # ============================================================================
    # 🌐 SEO OPTIMIZATION
    # ============================================================================

    async def _generate_seo_metadata(:
        self, image_path: Path, ai_analysis: Dict
    ) -> Dict[str, Any]:
        """Generate SEO-optimized metadata for image"""
        seo = {}

        # Alt text (crucial for accessibility and SEO)
        seo["alt_text"] = ai_analysis.get("alt_text") or self._generate_alt_text(
            image_path, ai_analysis
        )

        # Title attribute
        seo["title"] = self._generate_title(image_path, ai_analysis)

        # SEO-friendly filename
        seo["suggested_filename"] = self._generate_seo_filename(image_path, ai_analysis)

        # Keywords/tags
        seo["keywords"] = self._extract_keywords(ai_analysis)

        # Caption
        seo["caption"] = ai_analysis.get("description", "")[:200]

        # Image schema markup suggestion
        seo["schema_org"] = self._generate_schema_markup(image_path, seo)

        return seo

    def _generate_alt_text(self, image_path: Path, analysis: Dict) -> str:
        """Generate accessible alt text"""
        description = analysis.get("description", "")
        objects = analysis.get("objects", "")
        scene = analysis.get("scene", "")

        if description:
            # Clean and limit length (125 chars is recommended)
            alt = description.split(".")[0]  # First sentence
            alt = re.sub(r"\s+", " ", alt).strip()
            return alt[:125]
        elif objects:
            return f"{objects} in {scene}" if scene else objects
        else:
            # Fallback to filename
            name = image_path.stem
            return re.sub(r"[_-]", " ", name).title()

    def _generate_title(self, image_path: Path, analysis: Dict) -> str:
        """Generate title attribute"""
        description = analysis.get("description", "")
        if description:
            return description[:100]
        return image_path.stem.replace("_", " ").replace("-", " ").title()

    def _generate_seo_filename(self, image_path: Path, analysis: Dict) -> str:
        """Generate SEO-friendly filename"""
        # Use keywords or description
        keywords = analysis.get("keywords", [])
        objects = analysis.get("objects", "")

        if keywords and isinstance(keywords, list):
            base = "-".join(keywords[:5])
        elif objects:
            base = objects.replace(",", " ").replace(" ", "-")
        else:
            base = image_path.stem

        # Clean and format
        base = re.sub(r"[^a-z0-9-]", "", base.lower())
        base = re.sub(r"-+", "-", base).strip("-")

        # Add extension
        return f"{base}{image_path.suffix}"

    def _extract_keywords(self, analysis: Dict) -> List[str]:
        """Extract SEO keywords from analysis"""
        keywords = set()

        # From AI analysis
        if "keywords" in analysis:
            if isinstance(analysis["keywords"], list):
                keywords.update(analysis["keywords"])
            elif isinstance(analysis["keywords"], str):
                keywords.update(analysis["keywords"].split(","))

        # From objects
        if "objects" in analysis:
            objects = (
                analysis["objects"].split(",")
                if isinstance(analysis["objects"], str)
                else []
            )
            keywords.update([obj.strip() for obj in objects])

        # From scene
        if "scene" in analysis:
            keywords.add(analysis["scene"])

        # Clean and return
        cleaned = [kw.strip().lower() for kw in keywords if kw.strip()]
        return sorted(list(set(cleaned)))[:15]

    def _generate_schema_markup(self, image_path: Path, seo: Dict) -> Dict[str, Any]:
        """Generate Schema.org ImageObject markup"""
        return {
            "@context": "https://schema.org",
            "@type": "ImageObject",
            "name": seo.get("title", ""),
            "description": seo.get("alt_text", ""),
            "contentUrl": str(image_path.name),
            "keywords": ", ".join(seo.get("keywords", [])),
        }

    # ============================================================================
    # 📊 QUALITY SCORING & RECOMMENDATIONS
    # ============================================================================

    def _calculate_quality_score(self, analysis: Dict) -> Dict[str, Any]:
        """Calculate image quality score (0-100)"""
        scores = {}
        technical = analysis.get("technical", {})
        seo = analysis.get("seo", {})

        # Technical Quality (0-30 points)
        tech_score = 0

        # Resolution check
        width = technical.get("width", 0)
        height = technical.get("height", 0)
        if width >= 1920 or height >= 1080:
            tech_score += 10
        elif width >= 1280 or height >= 720:
            tech_score += 7
        elif width >= 800:
            tech_score += 5
        else:
            tech_score += 2

        # File size optimization
        size_kb = technical.get("file_size_kb", 0)
        if width and height:
            pixels = width * height
            ratio = size_kb / (pixels / 1000)  # KB per 1000 pixels
            if ratio < 50:  # Well optimized
                tech_score += 10
            elif ratio < 100:
                tech_score += 7
            else:
                tech_score += 3

        # Format check
        fmt = technical.get("format", "")
        if fmt in ["WEBP", "PNG", "JPEG"]:
            tech_score += 10
        elif fmt:
            tech_score += 5

        scores["technical"] = min(tech_score, 30)

        # SEO Quality (0-40 points)
        seo_score = 0

        # Alt text
        alt_text = seo.get("alt_text", "")
        if len(alt_text) > 50 and len(alt_text) < 125:
            seo_score += 15
        elif alt_text:
            seo_score += 10

        # Keywords
        keywords = seo.get("keywords", [])
        if len(keywords) >= 5:
            seo_score += 15
        elif len(keywords) >= 3:
            seo_score += 10
        elif keywords:
            seo_score += 5

        # Filename
        suggested = seo.get("suggested_filename", "")
        if suggested and "-" in suggested:
            seo_score += 10

        scores["seo"] = min(seo_score, 40)

        # Content Quality (0-30 points)
        content_score = 0
        ai_analysis = analysis.get("ai_analysis", {})

        # Description quality
        description = ai_analysis.get("description", "")
        if len(description) > 100:
            content_score += 15
        elif len(description) > 50:
            content_score += 10
        elif description:
            content_score += 5

        # Additional metadata
        if ai_analysis.get("objects"):
            content_score += 8
        if ai_analysis.get("scene"):
            content_score += 7

        scores["content"] = min(content_score, 30)

        # Total
        total = sum(scores.values())

        return {
            "total_score": round(total, 1),
            "grade": self._get_grade(total),
            "breakdown": scores,
        }

    def _get_grade(self, score: float) -> str:
        """Convert score to grade"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Average)"
        else:
            return "D (Needs Improvement)"

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        technical = analysis.get("technical", {})
        seo = analysis.get("seo", {})
        quality = analysis.get("quality_score", {})

        # Technical recommendations
        width = technical.get("width", 0)
        height = technical.get("height", 0)
        size_mb = technical.get("file_size_mb", 0)

        if width < 1200:
            recommendations.append(
                "⚠️ Resolution: Consider using higher resolution (min 1200px wide) for better quality"
            )

        if size_mb > 1:
            recommendations.append(
                "🗜️ Optimization: File size is large. Compress to under 1MB for faster loading"
            )

        if technical.get("format") not in ["WEBP", "PNG", "JPEG"]:
            recommendations.append(
                "🔄 Format: Convert to WebP or JPEG for better web compatibility"
            )

        # SEO recommendations
        alt_text = seo.get("alt_text", "")
        if len(alt_text) < 20:
            recommendations.append(
                "📝 Alt Text: Add more descriptive alt text (50-125 characters recommended)"
            )

        if len(seo.get("keywords", [])) < 5:
            recommendations.append(
                "🏷️ Keywords: Add more relevant keywords for better SEO"
            )

        current_name = Path(analysis["file_name"])
        suggested_name = seo.get("suggested_filename", "")
        if suggested_name and suggested_name != current_name.name:
            recommendations.append(
                f"📁 Filename: Rename to '{suggested_name}' for better SEO"
            )

        # Quality-based recommendations
        if quality.get("total_score", 0) < 70:
            recommendations.append(
                "🎯 Overall: Image needs optimization for web use. Focus on SEO metadata first."
            )

        if not recommendations:
            recommendations.append(
                "✅ Image is well-optimized! No major improvements needed."
            )

        return recommendations

    # ============================================================================
    # 🔨 BATCH PROCESSING
    # ============================================================================

    async def analyze_directory(:
        self, directory: Path, recursive: bool = True, output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Analyze all images in a directory
        """
        logger.info(f"🔍 Scanning directory: {directory}")

        # Find all images
        images = []
        if recursive:
            for ext in self.supported_formats:
                images.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in self.supported_formats:
                images.extend(directory.glob(f"*{ext}"))

        logger.info(f"📸 Found {len(images)} images")

        # Analyze each image
        results = []
        for i, image_path in enumerate(images, 1):
            logger.info(f"Analyzing {i}/{len(images)}: {image_path.name}")

            try:
                analysis = await self.analyze_image(image_path)
                results.append(analysis)

                # Rate limiting
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Failed to analyze {image_path.name}: {e}")
                results.append({"file_path": str(image_path), "error": str(e)})

        # Generate summary
        summary = self._generate_batch_summary(results)

        # Save results
        output_file = (
            directory
            / f"image_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(
                {"summary": summary, "results": results}, f, indent=2, default=str
            )

        logger.info(f"💾 Results saved to: {output_file}")

        return {"summary": summary, "results": results, "output_file": str(output_file)}

    def _generate_batch_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary statistics for batch analysis"""
        total = len(results)
        successful = len([r for r in results if "error" not in r])
        failed = total - successful

        # Average scores
        scores = [
            r.get("quality_score", {}).get("total_score", 0)
            for r in results
            if "quality_score" in r
        ]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Grade distribution
        grades = [
            r.get("quality_score", {}).get("grade", "Unknown")
            for r in results
            if "quality_score" in r
        ]
        grade_dist = Counter(grades)

        # Format distribution
        formats = [
            r.get("technical", {}).get("format", "Unknown")
            for r in results
            if "technical" in r
        ]
        format_dist = Counter(formats)

        # Total file size
        total_size_mb = sum(
            [
                r.get("technical", {}).get("file_size_mb", 0)
                for r in results
                if "technical" in r
            ]
        )

        return {
            "total_images": total,
            "successful": successful,
            "failed": failed,
            "average_score": round(avg_score, 1),
            "grade_distribution": dict(grade_dist),
            "format_distribution": dict(format_dist),
            "total_size_mb": round(total_size_mb, 2),
            "needs_optimization": len(
                [
                    r
                    for r in results
                    if r.get("quality_score", {}).get("total_score", 100) < 70
                ]
            ),
        }


# ============================================================================
# 🚀 MAIN & CLI
# ============================================================================


async def main():
    """Demo the image intelligence system"""
    import sys

    analyzer = ImageIntelligence()

    print("\n" + "=" * 80)
    print("🖼️  IMAGE INTELLIGENCE & SEO ANALYZER")
    print("=" * 80)

    # Check for command line arguments
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])

        if target_path.is_file():
            # Analyze single image
            print(f"\n📸 Analyzing single image: {target_path.name}")
            result = await analyzer.analyze_image(target_path)

            # Display results
            print("\n✅ Analysis Complete!")
            print(f"\n📊 Quality Score: {result['quality_score']['total_score']}/100")
            print(f"   Grade: {result['quality_score']['grade']}")

            print("\n🔍 SEO Metadata:")
            print(f"   Alt Text: {result['seo']['alt_text']}")
            print(f"   Suggested Filename: {result['seo']['suggested_filename']}")
            print(f"   Keywords: {', '.join(result['seo']['keywords'][:5])}")

            print("\n💡 Recommendations:")
            for rec in result["recommendations"]:
                print(f"   {rec}")

            # Save detailed results
            output_file = target_path.parent / f"{target_path.stem}_analysis.json"
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n💾 Detailed results saved to: {output_file}")

        elif target_path.is_dir():
            # Analyze directory
            print(f"\n📁 Analyzing directory: {target_path}")
            recursive = "--recursive" in sys.argv or "-r" in sys.argv

            result = await analyzer.analyze_directory(target_path, recursive=recursive)

            print("\n✅ Batch Analysis Complete!")
            print("\n📊 Summary:")
            for key, value in result["summary"].items():
                print(f"   {key}: {value}")

            print(f"\n💾 Full results saved to: {result['output_file']}")

    else:
        # Demo mode
        print("\n💡 Usage:")
        print(
            "   python image_intelligence_seo.py <image_file>     # Analyze single image"
        )
        print(
            "   python image_intelligence_seo.py <directory>      # Analyze directory"
        )
        print(
            "   python image_intelligence_seo.py <directory> -r   # Recursive analysis"
        )
        print("\n📝 Example:")
        print("   python image_intelligence_seo.py ~/pictures/photo.jpg")
        print("   python image_intelligence_seo.py ~/pictures -r")


if __name__ == "__main__":
    asyncio.run(main())
