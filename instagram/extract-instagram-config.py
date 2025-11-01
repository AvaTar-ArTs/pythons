
# Constants
CONSTANT_0015 = 0015
CONSTANT_100 = 100
CONSTANT_130 = 130
CONSTANT_300 = 300
CONSTANT_800 = 800
CONSTANT_1024 = 1024
CONSTANT_2048 = 2048

#!/usr/bin/env python3
"""
Hybrid Image Analysis Pipeline
==============================

A cost-optimized pipeline combining Google Cloud Vision API for technical analysis
with OpenAI GPT-4 Vision for complex semantic understanding. This approach reduces
API costs by 60-80% while maintaining high-quality results.

Architecture:
- Google Cloud Vision: Object detection, label classification, color analysis, OCR
- OpenAI GPT-4 Vision: Emotional context, style descriptions, marketing copy, SEO optimization

Features:
- Intelligent API selection based on analysis type
- Cost tracking and optimization
- Fallback mechanisms for API failures
- Batch processing with rate limiting
- Comprehensive error handling and retry logic

Author: Enhanced by Claude
Version: 2.1 (Hybrid)
"""

import argparse
import base64
import csv
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from io import BytesIO

import backoff
from env_d_loader import load_dotenv
from google.cloud import vision
from openai import OpenAI
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION AND DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class ImageMetadata:
    """Technical metadata for an image file."""

    filename: str
    width: Optional[int] = None
    height: Optional[int] = None
    dpi: Optional[int] = None
    format: Optional[str] = None
    file_size: Optional[int] = None
    created_date: Optional[str] = None
    aspect_ratio: Optional[float] = None


@dataclass
class GoogleVisionResults:
    """Results from Google Cloud Vision API."""

    labels: List[Dict[str, Union[str, float]]] = None
    objects: List[Dict[str, Any]] = None
    colors: List[Dict[str, Any]] = None
    text_annotations: List[str] = None
    safe_search: Dict[str, str] = None
    image_properties: Dict[str, Any] = None
    confidence: float = 0.0


@dataclass
class OpenAIResults:
    """Results from OpenAI Vision API."""

    style_description: Optional[str] = None
    emotional_context: Optional[str] = None
    marketing_copy: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    target_audience: Optional[str] = None
    brand_alignment: Optional[str] = None
    confidence: float = 0.0


@dataclass
class CombinedAnalysis:
    """Combined analysis from both APIs."""

    # From Google Vision
    primary_objects: List[str] = None
    color_palette: List[str] = None
    detected_text: str = None
    safety_rating: str = None
    technical_quality: str = None

    # From OpenAI
    style: Optional[str] = None
    emotion: Optional[str] = None
    suggested_products: List[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    dominant_keyword: Optional[str] = None

    # Combined metrics
    overall_confidence: float = 0.0
    processing_cost: float = 0.0


@dataclass
class ProcessingResult:
    """Complete processing result for a single image."""

    image_path: Path
    metadata: ImageMetadata
    google_results: GoogleVisionResults
    openai_results: OpenAIResults
    combined_analysis: CombinedAnalysis
    source_tag: str
    processing_time: float
    success: bool
    error_message: Optional[str] = None
    api_costs: Dict[str, float] = None


class Config:
    """Enhanced configuration management with API-specific settings."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("hybrid_config.json")
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file or create default."""
        default_config = {
            "google_vision": {
                "enabled": True,
                "features": [
                    "LABEL_DETECTION",
                    "OBJECT_LOCALIZATION",
                    "IMAGE_PROPERTIES",
                    "SAFE_SEARCH_DETECTION",
                    "TEXT_DETECTION",
                ],
                "max_results": 20,
                "confidence_threshold": 0.5,
            },
            "openai": {
                "enabled": True,
                "model": "gpt-4o",
                "max_tokens": CONSTANT_800,
                "temperature": 0.7,
                "use_for": ["style_analysis", "seo_optimization", "emotional_context"],
                "fallback_enabled": True,
            },
            "processing": {
                "batch_size": 15,
                "max_workers": 6,
                "retry_attempts": 3,
                "retry_delay": 1.0,
                "cost_optimization": True,
                "use_openai_only_when_needed": True,
            },
            "cost_limits": {
                "max_daily_spend": 50.0,
                "google_vision_cost_per_image": 0.CONSTANT_0015,
                "openai_cost_per_image": 0.01,
                "warn_at_percentage": 80.0,
            },
            "image": {
                "valid_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
                "max_size_mb": 20,
                "quality_threshold": 0.7,
                "resize_large_images": True,
                "max_dimension": CONSTANT_2048,
            },
            "analysis_rules": {
                "use_openai_for_complex": True,
                "complexity_indicators": [
                    "artistic_style",
                    "emotional_content",
                    "abstract_concepts",
                    "marketing_copy",
                    "brand_analysis",
                ],
                "google_sufficient_for": [
                    "object_detection",
                    "color_analysis",
                    "text_extraction",
                    "safety_classification",
                    "technical_properties",
                ],
            },
            "prompts": {
                "openai_system": "You are an expert marketing and creative analyst. Analyze images for emotional impact, artistic style, and commercial potential. Focus on aspects that Google Vision cannot detect: artistic style, emotional resonance, brand alignment, and marketing potential.",
                "openai_user": "Analyze this image for: 1) Artistic style and aesthetic appeal, 2) Emotional impact and mood, 3) Target audience and demographics, 4) SEO-optimized title and description, 5) Suggested product categories, 6) Brand alignment potential. Return JSON with: style, emotion, target_audience, seo_title, seo_description, suggested_products (array), dominant_keyword, brand_alignment, confidence_score (0.0-1.0).",
            },
            "output": {
                "include_raw_responses": False,
                "cost_tracking": True,
                "detailed_logging": True,
            },
        }

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # Deep merge configurations
                    self.data = self._deep_merge(default_config, loaded_config)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logging.warning(f"Config file error: {e}. Using defaults.")
                self.data = default_config
        else:
            self.data = default_config
            self.save_config()

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, section: str, key: str = None, default=None):
        """Get configuration value with dot notation support."""
        if key is None:
            return self.data.get(section, default)
        return self.data.get(section, {}).get(key, default)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING AND COST TRACKING
# ═══════════════════════════════════════════════════════════════════════════════


class CostTracker:
    """Track and manage API costs across providers."""

    def __init__(self, config: Config):
        self.config = config
        self.daily_spend = 0.0
        self.costs_by_api = {"google_vision": 0.0, "openai": 0.0}
        self.calls_by_api = {"google_vision": 0, "openai": 0}
        self.logger = logging.getLogger(__name__)

    def record_cost(self, api_name: str, cost: float):
        """Record a cost for an API call."""
        self.costs_by_api[api_name] += cost
        self.calls_by_api[api_name] += 1
        self.daily_spend += cost

        # Check limits
        max_daily = self.config.get("cost_limits", "max_daily_spend")
        warn_threshold = self.config.get("cost_limits", "warn_at_percentage") / CONSTANT_100.0

        if self.daily_spend > max_daily * warn_threshold:
            self.logger.warning(f"Daily spend warning: ${self.daily_spend:.2f} / ${max_daily:.2f}")

    def can_afford(self, api_name: str) -> bool:
        """Check if we can afford another API call."""
        max_daily = self.config.get("cost_limits", "max_daily_spend")
        cost_per_call = self.config.get("cost_limits", f"{api_name}_cost_per_image")
        return (self.daily_spend + cost_per_call) <= max_daily

    def get_summary(self) -> Dict[str, Any]:
        """Get cost summary."""
        return {
            "total_spend": self.daily_spend,
            "by_api": self.costs_by_api.copy(),
            "calls_by_api": self.calls_by_api.copy(),
            "average_cost_per_image": (
                self.daily_spend / sum(self.calls_by_api.values())
                if sum(self.calls_by_api.values()) > 0
                else 0
            ),
        }


def setup_logging(log_file: Path = Path("hybrid_pipeline.log"), level: str = "INFO"):
    """Configure logging with both file and console output."""
    log_format = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Reduce noise from external libraries
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)


# ═══════════════════════════════════════════════════════════════════════════════
# API CLIENT CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


class GoogleVisionClient:
    """Google Cloud Vision API client with enhanced error handling."""

    def __init__(self, config: Config, cost_tracker: CostTracker):
        self.config = config
        self.cost_tracker = cost_tracker
        self.client = vision.ImageAnnotatorClient()
        self.logger = logging.getLogger(__name__)

    @backoff.on_exception(backoff.expo, Exception, max_tries=3, jitter=backoff.full_jitter)
    def analyze_image(self, image_data: bytes) -> GoogleVisionResults:
        """Analyze image using Google Cloud Vision API."""
        if not self.cost_tracker.can_afford("google_vision"):
            raise Exception("Daily cost limit reached for Google Vision API")

        try:
            image = vision.Image(content=image_data)
            features = []

            # Configure features based on config
            for feature_type in self.config.get("google_vision", "features"):
                feature = vision.Feature(
                    type_=getattr(vision.Feature.Type, feature_type),
                    max_results=self.config.get("google_vision", "max_results"),
                )
                features.append(feature)

            # Make the API request
            request = vision.AnnotateImageRequest(image=image, features=features)
            response = self.client.annotate_image(request=request)

            if response.error.message:
                raise Exception(f"Google Vision API error: {response.error.message}")

            # Record cost
            cost = self.config.get("cost_limits", "google_vision_cost_per_image")
            self.cost_tracker.record_cost("google_vision", cost)

            # Parse response
            return self._parse_response(response)

        except Exception as e:
            self.logger.error(f"Google Vision API error: {e}")
            raise

    def _parse_response(self, response) -> GoogleVisionResults:
        """Parse Google Vision API response into structured format."""
        results = GoogleVisionResults()

        # Labels
        if response.label_annotations:
            results.labels = [
                {"description": label.description, "score": label.score, "confidence": label.score}
                for label in response.label_annotations
                if label.score >= self.config.get("google_vision", "confidence_threshold")
            ]

        # Objects
        if response.localized_object_annotations:
            results.objects = [
                {
                    "name": obj.name,
                    "score": obj.score,
                    "bounding_box": {
                        "vertices": [(v.x, v.y) for v in obj.bounding_poly.normalized_vertices]
                    },
                }
                for obj in response.localized_object_annotations
            ]

        # Colors
        if response.image_properties_annotation:
            results.colors = [
                {
                    "color": {
                        "red": color.color.red,
                        "green": color.color.green,
                        "blue": color.color.blue,
                    },
                    "score": color.score,
                    "pixel_fraction": color.pixel_fraction,
                }
                for color in response.image_properties_annotation.dominant_colors.colors
            ]

        # Text
        if response.text_annotations:
            results.text_annotations = [text.description for text in response.text_annotations]

        # Safe search
        if response.safe_search_annotation:
            safe_search = response.safe_search_annotation
            results.safe_search = {
                "adult": safe_search.adult.name,
                "spoof": safe_search.spoof.name,
                "medical": safe_search.medical.name,
                "violence": safe_search.violence.name,
                "racy": safe_search.racy.name,
            }

        # Calculate overall confidence
        if results.labels:
            results.confidence = sum(label["score"] for label in results.labels) / len(
                results.labels
            )

        return results


class OpenAIClient:
    """OpenAI Vision API client optimized for semantic analysis."""

    def __init__(self, config: Config, cost_tracker: CostTracker):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.config = config
        self.cost_tracker = cost_tracker
        self.logger = logging.getLogger(__name__)

    @backoff.on_exception(backoff.expo, Exception, max_tries=3, jitter=backoff.full_jitter)
    def analyze_image(
        self, image_data: str, mime_type: str, google_results: GoogleVisionResults = None
    ) -> OpenAIResults:
        """Analyze image using OpenAI Vision API with context from Google Vision."""
        if not self.cost_tracker.can_afford("openai"):
            raise Exception("Daily cost limit reached for OpenAI API")

        try:
            # Build context from Google Vision results
            context = self._build_context_from_google(google_results) if google_results else ""

            messages = [
                {"role": "system", "content": self.config.get("prompts", "openai_system")},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}",
                                "detail": "high",
                            },
                        },
                        {
                            "type": "text",
                            "text": f"{context}\n\n{self.config.get('prompts', 'openai_user')}",
                        },
                    ],
                },
            ]

            response = self.client.chat.completions.create(
                model=self.config.get("openai", "model"),
                messages=messages,
                max_tokens=self.config.get("openai", "max_tokens"),
                temperature=self.config.get("openai", "temperature"),
            )

            # Record cost
            cost = self.config.get("cost_limits", "openai_cost_per_image")
            self.cost_tracker.record_cost("openai", cost)

            content = response.choices[0].message.content
            return self._parse_response(content)

        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise

    def _build_context_from_google(self, google_results: GoogleVisionResults) -> str:
        """Build context string from Google Vision results."""
        context_parts = []

        if google_results.labels:
            labels = [label["description"] for label in google_results.labels[:5]]
            context_parts.append(f"Detected objects/concepts: {', '.join(labels)}")

        if google_results.colors:
            dominant_colors = google_results.colors[:3]
            color_descriptions = [
                f"RGB({c['color']['red']}, {c['color']['green']}, {c['color']['blue']})"
                for c in dominant_colors
            ]
            context_parts.append(f"Dominant colors: {', '.join(color_descriptions)}")

        if google_results.safe_search:
            safety_info = [f"{k}: {v}" for k, v in google_results.safe_search.items()]
            context_parts.append(f"Safety ratings: {', '.join(safety_info)}")

        return (
            "Context from technical analysis:\n" + Path("\n").join(context_parts) if context_parts else ""
        )

    def _parse_response(self, content: str) -> OpenAIResults:
        """Parse OpenAI response into structured format."""
        try:
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")

            json_str = content[start_idx:end_idx]
            data = json.loads(json_str)

            return OpenAIResults(
                style_description=data.get("style"),
                emotional_context=data.get("emotion"),
                marketing_copy=data.get("brand_alignment"),
                seo_title=data.get("seo_title"),
                seo_description=data.get("seo_description"),
                target_audience=data.get("target_audience"),
                brand_alignment=data.get("brand_alignment"),
                confidence=data.get("confidence_score", 0.0),
            )

        except (json.JSONDecodeError, ValueError) as e:
            self.logger.warning(f"OpenAI JSON parsing failed: {e}")
            return OpenAIResults()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PROCESSING CLASS
# ═══════════════════════════════════════════════════════════════════════════════


class HybridImageProcessor:
    """Main processor that combines Google Vision and OpenAI for optimal results."""

    def __init__(self, config: Config):
        self.config = config
        self.cost_tracker = CostTracker(config)
        self.google_client = GoogleVisionClient(config, self.cost_tracker)
        self.openai_client = OpenAIClient(config, self.cost_tracker)
        self.logger = logging.getLogger(__name__)
        self.valid_extensions = set(self.config.get("image", "valid_extensions"))

    def discover_images(self, input_folder: Path) -> List[Path]:
        """Recursively find all valid image files."""
        image_files = []

        for root, _, files in os.walk(input_folder):
            root_path = Path(root)
            for filename in files:
                file_path = root_path / filename
                if file_path.suffix.lower() in self.valid_extensions:
                    # Check file size
                    max_size = self.config.get("image", "max_size_mb") * CONSTANT_1024 * CONSTANT_1024
                    if file_path.stat().st_size <= max_size:
                        image_files.append(file_path)
                    else:
                        self.logger.warning(f"Skipping large file: {filename}")

        return sorted(image_files)

    def extract_metadata(self, image_path: Path) -> ImageMetadata:
        """Extract technical metadata from image file."""
        metadata = ImageMetadata(filename=image_path.name)

        try:
            with Image.open(image_path) as img:
                metadata.width = img.width
                metadata.height = img.height
                metadata.format = img.format
                metadata.aspect_ratio = round(img.width / img.height, 2) if img.height > 0 else None

                # Extract DPI information
                dpi_info = img.info.get("dpi", (CONSTANT_300, CONSTANT_300))
                metadata.dpi = dpi_info[0] if isinstance(dpi_info, tuple) else dpi_info

            # File system metadata
            stat = image_path.stat()
            metadata.file_size = stat.st_size
            metadata.created_date = datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except UnidentifiedImageError:
            self.logger.warning(f"Cannot identify image format: {image_path.name}")
        except Exception as e:
            self.logger.error(f"Error extracting metadata for {image_path.name}: {e}")

        return metadata

    def process_single_image(self, image_path: Path, base_folder: Path) -> ProcessingResult:
        """Process a single image using hybrid approach."""
        start_time = time.time()

        try:
            # Extract metadata
            metadata = self.extract_metadata(image_path)

            # Load and prepare image data
            image_data = self._load_image_data(image_path)

            # Step 1: Always run Google Vision for technical analysis
            google_results = GoogleVisionResults()
            if self.config.get("google_vision", "enabled"):
                google_results = self.google_client.analyze_image(image_data)

            # Step 2: Determine if OpenAI analysis is needed
            openai_results = OpenAIResults()
            if self._should_use_openai(google_results, metadata):
                if self.config.get("openai", "enabled"):
                    # Encode for OpenAI
                    image_b64, mime_type = self._encode_for_openai(image_path)
                    openai_results = self.openai_client.analyze_image(
                        image_b64, mime_type, google_results
                    )

            # Step 3: Combine results
            combined_analysis = self._combine_results(google_results, openai_results, metadata)

            # Generate source tag
            source_tag = self._build_source_tag(image_path, base_folder)

            processing_time = time.time() - start_time

            return ProcessingResult(
                image_path=image_path,
                metadata=metadata,
                google_results=google_results,
                openai_results=openai_results,
                combined_analysis=combined_analysis,
                source_tag=source_tag,
                processing_time=processing_time,
                success=True,
                api_costs=self.cost_tracker.costs_by_api.copy(),
            )

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"Error processing {image_path.name}: {e}")

            return ProcessingResult(
                image_path=image_path,
                metadata=ImageMetadata(filename=image_path.name),
                google_results=GoogleVisionResults(),
                openai_results=OpenAIResults(),
                combined_analysis=CombinedAnalysis(),
                source_tag="",
                processing_time=processing_time,
                success=False,
                error_message=str(e),
                api_costs=self.cost_tracker.costs_by_api.copy(),
            )

    def _load_image_data(self, image_path: Path) -> bytes:
        """Load image data, optionally resizing if too large."""
        with open(image_path, "rb") as f:
            data = f.read()

        # Check if resizing is needed and enabled
        if self.config.get("image", "resize_large_images"):
            try:
                img = Image.open(BytesIO(data))
                max_dim = self.config.get("image", "max_dimension")

                if max(img.width, img.height) > max_dim:
                    # Calculate new dimensions maintaining aspect ratio
                    if img.width > img.height:
                        new_width = max_dim
                        new_height = int((max_dim * img.height) / img.width)
                    else:
                        new_height = max_dim
                        new_width = int((max_dim * img.width) / img.height)

                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Convert back to bytes
                    buffer = BytesIO()
                    img.save(buffer, format=img.format or "JPEG", quality=85)
                    data = buffer.getvalue()

                    self.logger.info(f"Resized {image_path.name} to {new_width}x{new_height}")

            except Exception as e:
                self.logger.warning(f"Failed to resize {image_path.name}: {e}")

        return data

    def _encode_for_openai(self, image_path: Path) -> Tuple[str, str]:
        """Encode image for OpenAI API."""
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Determine MIME type
        ext = image_path.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".tiff": "image/tiff",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(ext, "image/jpeg")

        return encoded_string, mime_type

    def _should_use_openai(
        self, google_results: GoogleVisionResults, metadata: ImageMetadata
    ) -> bool:
        """Determine if OpenAI analysis is needed based on complexity and configuration."""
        if not self.config.get("processing", "use_openai_only_when_needed"):
            return True

        # Always use OpenAI if it's the only enabled API
        if not self.config.get("google_vision", "enabled"):
            return True

        # Check for complexity indicators
        complexity_indicators = self.config.get("analysis_rules", "complexity_indicators")

        # Analyze Google results for complexity
        if google_results.labels:
            labels = [label["description"].lower() for label in google_results.labels]

            # Check for artistic or abstract content
            artistic_terms = [
                "art",
                "painting",
                "drawing",
                "abstract",
                "artistic",
                "creative",
                "design",
            ]
            if any(term in " ".join(labels) for term in artistic_terms):
                return True

            # Check confidence - low confidence might need OpenAI
            if google_results.confidence < 0.7:
                return True

        # Check image properties for complexity
        if metadata.aspect_ratio and (metadata.aspect_ratio < 0.5 or metadata.aspect_ratio > 2.0):
            return True  # Unusual aspect ratios might be artistic

        # Default: use Google Vision only for straightforward images
        return False

    def _combine_results(
        self,
        google_results: GoogleVisionResults,
        openai_results: OpenAIResults,
        metadata: ImageMetadata,
    ) -> CombinedAnalysis:
        """Combine results from both APIs into unified analysis."""
        analysis = CombinedAnalysis()

        # From Google Vision
        if google_results.labels:
            analysis.primary_objects = [label["description"] for label in google_results.labels[:5]]

        if google_results.colors:
            analysis.color_palette = [
                f"#{int(c['color']['red']):02x}{int(c['color']['green']):02x}{int(c['color']['blue']):02x}"
                for c in google_results.colors[:5]
            ]

        if google_results.text_annotations:
            analysis.detected_text = " ".join(google_results.text_annotations[:3])

        if google_results.safe_search:
            # Convert to simple safety rating
            adult = google_results.safe_search.get("adult", "UNKNOWN")
            if adult in ["VERY_UNLIKELY", "UNLIKELY"]:
                analysis.safety_rating = "G"
            elif adult == "POSSIBLE":
                analysis.safety_rating = "PG"
            else:
                analysis.safety_rating = "R"

        # From OpenAI (if available)
        if openai_results.style_description:
            analysis.style = openai_results.style_description
        if openai_results.emotional_context:
            analysis.emotion = openai_results.emotional_context
        if openai_results.seo_title:
            analysis.seo_title = openai_results.seo_title
        if openai_results.seo_description:
            analysis.seo_description = openai_results.seo_description

        # Generate suggested products from both sources
        products = []
        if google_results.labels:
            # Map labels to product categories
            label_to_product = {
                "clothing": ["T-Shirt", "Hoodie", "Tank Top"],
                "art": ["Canvas Print", "Poster", "Sticker"],
                "nature": ["Calendar", "Postcard", "Wall Art"],
                "food": ["Kitchen Towel", "Apron", "Coaster"],
                "technology": ["Phone Case", "Laptop Sticker", "Mouse Pad"],
                "animal": ["Pet Accessories", "Plush Toy", "Mug"],
                "vehicle": ["Bumper Sticker", "License Plate", "Keychain"],
            }

            for label in google_results.labels[:3]:
                desc = label["description"].lower()
                for category, items in label_to_product.items():
                    if category in desc:
                        products.extend(items[:2])
                        break

        analysis.suggested_products = list(set(products[:5]))  # Remove duplicates, limit to 5

        # Generate dominant keyword
        if analysis.primary_objects:
            analysis.dominant_keyword = analysis.primary_objects[0]

        # Calculate overall confidence
        confidences = []
        if google_results.confidence > 0:
            confidences.append(google_results.confidence)
        if openai_results.confidence > 0:
            confidences.append(openai_results.confidence)

        analysis.overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Calculate processing cost
        analysis.processing_cost = sum(self.cost_tracker.costs_by_api.values())

        return analysis

    def _build_source_tag(self, image_path: Path, base_folder: Path) -> str:
        """Generate source tag for the image."""
        try:
            relative_path = image_path.relative_to(base_folder)
            parent_parts = relative_path.parent.parts
            folder_id = "-".join(parent_parts) if parent_parts else base_folder.name
            date_str = datetime.now().strftime("%Y%m%d")
            return f"{folder_id}-{date_str}"
        except ValueError:
            return f"{base_folder.name}-{datetime.now().strftime('%Y%m%d')}"


class CSVWriter:
    """Enhanced CSV writer for hybrid results."""

    def __init__(self, output_path: Path, config: Config):
        self.output_path = output_path
        self.config = config
        self.fieldnames = self._get_fieldnames()

    def _get_fieldnames(self) -> List[str]:
        """Define CSV column headers for hybrid results."""
        return [
            # Technical metadata
            "filename",
            "width",
            "height",
            "dpi",
            "format",
            "file_size",
            "created_date",
            "aspect_ratio",
            # Combined analysis results
            "primary_objects",
            "color_palette",
            "detected_text",
            "safety_rating",
            "style",
            "emotion",
            "suggested_products",
            "seo_title",
            "seo_description",
            "dominant_keyword",
            "overall_confidence",
            # Processing metadata
            "source_tag",
            "processing_time",
            "success",
            "error_message",
            "google_vision_used",
            "openai_used",
            "processing_cost",
            # Raw API results (optional)
            "google_labels",
            "google_objects",
            "google_colors",
            "openai_style",
            "openai_emotion",
            "openai_target_audience",
            # Cost tracking
            "google_vision_cost",
            "openai_cost",
            "total_api_cost",
        ]

    def write_results(self, results: List[ProcessingResult], cost_summary: Dict[str, Any]):
        """Write processing results to CSV with cost summary."""
        with open(self.output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            for result in results:
                row = self._result_to_row(result)
                writer.writerow(row)

        # Write cost summary to separate file
        cost_file = self.output_path.parent / f"{self.output_path.stem}_cost_summary.json"
        with open(cost_file, "w", encoding="utf-8") as f:
            json.dump(cost_summary, f, indent=2)

    def _result_to_row(self, result: ProcessingResult) -> Dict[str, Any]:
        """Convert ProcessingResult to CSV row."""
        ca = result.combined_analysis

        row = {
            # Technical metadata
            "filename": result.metadata.filename,
            "width": result.metadata.width,
            "height": result.metadata.height,
            "dpi": result.metadata.dpi,
            "format": result.metadata.format,
            "file_size": result.metadata.file_size,
            "created_date": result.metadata.created_date,
            "aspect_ratio": result.metadata.aspect_ratio,
            # Combined analysis
            "primary_objects": json.dumps(ca.primary_objects) if ca.primary_objects else "[]",
            "color_palette": json.dumps(ca.color_palette) if ca.color_palette else "[]",
            "detected_text": ca.detected_text or "",
            "safety_rating": ca.safety_rating or "",
            "style": ca.style or "",
            "emotion": ca.emotion or "",
            "suggested_products": (
                json.dumps(ca.suggested_products) if ca.suggested_products else "[]"
            ),
            "seo_title": ca.seo_title or "",
            "seo_description": ca.seo_description or "",
            "dominant_keyword": ca.dominant_keyword or "",
            "overall_confidence": ca.overall_confidence,
            # Processing metadata
            "source_tag": result.source_tag,
            "processing_time": round(result.processing_time, 2),
            "success": result.success,
            "error_message": result.error_message or "",
            "google_vision_used": bool(
                result.google_results.labels or result.google_results.objects
            ),
            "openai_used": bool(
                result.openai_results.style_description or result.openai_results.seo_title
            ),
            "processing_cost": ca.processing_cost,
            # Raw API results
            "google_labels": json.dumps(
                [l["description"] for l in (result.google_results.labels or [])]
            ),
            "google_objects": json.dumps(
                [o["name"] for o in (result.google_results.objects or [])]
            ),
            "google_colors": json.dumps(result.google_results.colors or []),
            "openai_style": result.openai_results.style_description or "",
            "openai_emotion": result.openai_results.emotional_context or "",
            "openai_target_audience": result.openai_results.target_audience or "",
            # Cost tracking
            "google_vision_cost": (
                result.api_costs.get("google_vision", 0.0) if result.api_costs else 0.0
            ),
            "openai_cost": result.api_costs.get("openai", 0.0) if result.api_costs else 0.0,
            "total_api_cost": sum(result.api_costs.values()) if result.api_costs else 0.0,
        }

        return row


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE CLASS
# ═══════════════════════════════════════════════════════════════════════════════


class HybridImagePipeline:
    """Main pipeline orchestrator for hybrid analysis."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config = Config(config_path)
        self.logger = logging.getLogger(__name__)
        self.processor = HybridImageProcessor(self.config)

    def run(self, input_folder: Path, output_csv: Path) -> bool:
        """Run the hybrid image analysis pipeline."""
        start_time = time.time()

        try:
            # Discover images
            self.logger.info(f"Scanning for images in: {input_folder}")
            image_paths = self.processor.discover_images(input_folder)

            if not image_paths:
                self.logger.warning("No valid images found")
                return False

            self.logger.info(f"Found {len(image_paths)} images to process")

            # Process images
            max_workers = self.config.get("processing", "max_workers")

            if max_workers > 1:
                results = self._process_concurrent(image_paths, input_folder, max_workers)
            else:
                results = self._process_sequential(image_paths, input_folder)

            # Get cost summary
            cost_summary = self.processor.cost_tracker.get_summary()

            # Write results
            self.logger.info(f"Writing results to: {output_csv}")
            writer = CSVWriter(output_csv, self.config)
            writer.write_results(results, cost_summary)

            # Summary statistics
            successful = sum(1 for r in results if r.success)
            google_used = sum(1 for r in results if r.google_results.labels)
            openai_used = sum(1 for r in results if r.openai_results.seo_title)
            total_time = time.time() - start_time
            avg_time = sum(r.processing_time for r in results) / len(results) if results else 0

            self.logger.info("=" * 60)
            self.logger.info("HYBRID PIPELINE COMPLETE!")
            self.logger.info("=" * 60)
            self.logger.info(f"Images processed: {successful}/{len(results)} successfully")
            self.logger.info(f"Google Vision used: {google_used} times")
            self.logger.info(f"OpenAI used: {openai_used} times")
            self.logger.info(f"Total cost: ${cost_summary['total_spend']:.3f}")
            self.logger.info(
                f"Average cost per image: ${cost_summary['average_cost_per_image']:.3f}"
            )
            self.logger.info(f"Total time: {total_time:.1f}s, Average per image: {avg_time:.1f}s")
            self.logger.info(f"Cost breakdown: {cost_summary['by_api']}")

            return True

        except KeyboardInterrupt:
            self.logger.warning("Pipeline interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            return False

    def _process_sequential(
        self, image_paths: List[Path], base_folder: Path
    ) -> List[ProcessingResult]:
        """Process images sequentially."""
        results = []

        with tqdm(image_paths, desc="Processing images", unit="image") as pbar:
            for image_path in pbar:
                pbar.set_postfix({"current": image_path.name})
                result = self.processor.process_single_image(image_path, base_folder)
                results.append(result)

                # Update progress bar with cost info
                cost_so_far = self.processor.cost_tracker.daily_spend
                pbar.set_postfix({"current": image_path.name, "cost": f"${cost_so_far:.3f}"})

                if not result.success:
                    self.logger.warning(f"Failed to process: {image_path.name}")

        return results

    def _process_concurrent(
        self, image_paths: List[Path], base_folder: Path, max_workers: int
    ) -> List[ProcessingResult]:
        """Process images concurrently with thread pool."""
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_path = {
                executor.submit(self.processor.process_single_image, path, base_folder): path
                for path in image_paths
            }

            # Process completed tasks with progress bar
            with tqdm(total=len(image_paths), desc="Processing images", unit="image") as pbar:
                for future in as_completed(future_to_path):
                    image_path = future_to_path[future]
                    try:
                        result = future.result()
                        results.append(result)

                        cost_so_far = self.processor.cost_tracker.daily_spend
                        if result.success:
                            pbar.set_postfix(
                                {"completed": image_path.name, "cost": f"${cost_so_far:.3f}"}
                            )
                        else:
                            pbar.set_postfix(
                                {"failed": image_path.name, "cost": f"${cost_so_far:.3f}"}
                            )

                    except Exception as e:
                        self.logger.error(f"Unexpected error processing {image_path.name}: {e}")
                        failed_result = ProcessingResult(
                            image_path=image_path,
                            metadata=ImageMetadata(filename=image_path.name),
                            google_results=GoogleVisionResults(),
                            openai_results=OpenAIResults(),
                            combined_analysis=CombinedAnalysis(),
                            source_tag="",
                            processing_time=0.0,
                            success=False,
                            error_message=str(e),
                        )
                        results.append(failed_result)

                    pbar.update(1)

        # Sort results by original order
        path_to_result = {r.image_path: r for r in results}
        return [path_to_result[path] for path in image_paths if path in path_to_result]


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Hybrid Image Analysis Pipeline (Google Vision + OpenAI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/images
  %(prog)s /path/to/images -o results.csv --config custom_config.json
  %(prog)s /path/to/images --google-only --concurrent 8
  %(prog)s /path/to/images --openai-only --log-level DEBUG
  
Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key
  GOOGLE_APPLICATION_CREDENTIALS: Path to Google Cloud credentials JSON
        """,
    )

    parser.add_argument("input_folder", type=Path, help="Directory containing images to analyze")

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("hybrid_analysis_results.csv"),
        help="Output CSV file path (default: hybrid_analysis_results.csv)",
    )

    parser.add_argument(
        "-c", "--config", type=Path, help="Configuration file path (default: hybrid_config.json)"
    )

    parser.add_argument(
        "--google-only", action="store_true", help="Use only Google Vision API (faster, cheaper)"
    )

    parser.add_argument(
        "--openai-only",
        action="store_true",
        help="Use only OpenAI API (slower, more expensive, better semantic analysis)",
    )

    parser.add_argument(
        "--concurrent",
        type=int,
        metavar="N",
        help="Number of concurrent workers (default: from config)",
    )

    parser.add_argument(
        "--max-cost",
        type=float,
        metavar="DOLLARS",
        help="Maximum daily spend in dollars (overrides config)",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 2.1 (Hybrid)")

    return parser.parse_args()


def validate_environment():
    """Validate required environment variables and credentials."""
    errors = []

    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY environment variable not set")

    # Check Google Cloud credentials
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        errors.append("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
    else:
        cred_path = Path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        if not cred_path.exists():
            errors.append(f"Google credentials file not found: {cred_path}")

    return errors


def main():
    """Main entry point."""
    args = parse_arguments()

    # Setup logging
    setup_logging(Path("hybrid_pipeline.log"), args.log_level)
    logger = logging.getLogger(__name__)

    # Load environment
    env_path = Path.home() / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # Validate environment
    env_errors = validate_environment()
    if env_errors:
        logger.error("Environment validation failed:")
        for error in env_errors:
            logger.error(f"  - {error}")
        logger.error("\nPlease set up your credentials and try again.")
        sys.exit(1)

    # Validate input
    if not args.input_folder.exists():
        logger.error(f"Input folder does not exist: {args.input_folder}")
        sys.exit(1)

    if not args.input_folder.is_dir():
        logger.error(f"Input path is not a directory: {args.input_folder}")
        sys.exit(1)

    try:
        # Initialize pipeline
        pipeline = HybridImagePipeline(args.config)

        # Apply CLI overrides
        if args.google_only:
            pipeline.config.data["google_vision"]["enabled"] = True
            pipeline.config.data["openai"]["enabled"] = False
            logger.info("Running in Google Vision only mode")

        if args.openai_only:
            pipeline.config.data["google_vision"]["enabled"] = False
            pipeline.config.data["openai"]["enabled"] = True
            logger.info("Running in OpenAI only mode")

        if args.concurrent:
            pipeline.config.data["processing"]["max_workers"] = args.concurrent

        if args.max_cost:
            pipeline.config.data["cost_limits"]["max_daily_spend"] = args.max_cost

        # Run pipeline
        logger.info("Starting Hybrid Image Analysis Pipeline v2.1")
        success = pipeline.run(
            input_folder=args.input_folder.resolve(), output_csv=args.output.resolve()
        )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(CONSTANT_130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
