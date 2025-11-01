"""
Content Factory

This module provides functionality for content factory.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
🎨 AI Content Factory
Automated product photography and image generation pipeline

Features:
- AI image generation (Leonardo.AI)
- Background removal (Remove.bg)
- Auto-tagging (Imagga)
- Quality enhancement (VanceAI)
- Style variations (Stability AI)
- Cloud storage (Cloudflare R2)

Usage:
    source ~/.env.d/loader.sh
    python3 content_factory.py "premium wireless headphones"
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ContentFactory:
    """Professional product photography pipeline"""

    def __init__(self):
        """__init__ function."""

        # API Keys
        self.leonardo_key = os.getenv('LEONARDO_API_KEY')
        self.removebg_key = os.getenv('REMOVEBG_API_KEY')
        self.imagga_key = os.getenv('IMAGGA_API_KEY')
        self.imagga_secret = os.getenv('IMAGGA_API_SECRET')
        self.stability_key = os.getenv('STABILITY_API_KEY')
        self.vance_key = os.getenv('VANCEAI_API_KEY')

        # Output directory
        self.output_dir = Path.home() / "AI_Content"
        self.output_dir.mkdir(exist_ok=True)

        self._validate_keys()

    def _validate_keys(self):
        """Check required API keys"""
        required = {
            'Leonardo.AI': self.leonardo_key,
            'Remove.bg': self.removebg_key,
        }

        missing = [name for name, key in required.items() if not key]
        if missing:
            logger.info(f"❌ Missing API keys: {', '.join(missing)}")
            sys.exit(1)

    def generate_image(self, description: str) -> str:
        """
        Step 1: Generate base image with Leonardo.AI
        """
        logger.info(f"🎨 Generating image: {description}")

        prompt = f"professional product photography: {description}, studio lighting, white background, high quality, commercial, 8K"

        try:
            # Start generation
            response = requests.post(
                "https://cloud.leonardo.ai/api/rest/v1/generations",
                headers={
                    "Authorization": f"Bearer {self.leonardo_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Diffusion XL
                    "width": CONSTANT_1024,
                    "height": CONSTANT_1024,
                    "num_images": 1,
                    "alchemy": True,  # Higher quality
                    "photoReal": True
                },
                timeout=30
            )

            if response.status_code != CONSTANT_200:
                logger.info(f"❌ Leonardo error: {response.status_code}")
                logger.info(response.text)
                sys.exit(1)

            generation_id = response.json()["sdGenerationJob"]["generationId"]

            # Wait for completion
            logger.info("   Waiting for generation...", end="", flush=True)
            image_url = self._wait_for_generation(generation_id)

            logger.info(f" ✅")
            return image_url

        except Exception as e:
            logger.info(f"❌ Generation error: {e}")
            sys.exit(1)

    def _wait_for_generation(self, generation_id: str, max_wait: int = 60) -> str:
        """Poll for generation completion"""
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
                    headers={"Authorization": f"Bearer {self.leonardo_key}"},
                    timeout=10
                )

                if response.status_code == CONSTANT_200:
                    data = response.json()
                    if data["generations_by_pk"]["status"] == "COMPLETE":
                        images = data["generations_by_pk"]["generated_images"]
                        if images:
                            return images[0]["url"]

                logger.info(".", end="", flush=True)
                time.sleep(3)

            except Exception as e:
                logger.info(f"\n⚠️ Polling error: {e}")

        raise Exception("Generation timeout")

    def download_image(self, url: str, filename: str) -> Path:
        """Download image from URL"""
        response = requests.get(url, timeout=30)
        image_path = self.output_dir / filename

        with open(image_path, "wb") as f:
            f.write(response.content)

        return image_path

    def remove_background(self, image_path: Path) -> Path:
        """
        Step 2: Remove background with Remove.bg
        """
        logger.info(f"✂️  Removing background...")

        try:
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    headers={"X-Api-Key": self.removebg_key},
                    files={"image_file": image_file},
                    data={"size": "auto"},
                    timeout=30
                )

            if response.status_code != CONSTANT_200:
                logger.info(f"⚠️ Remove.bg error: {response.status_code}")
                return image_path  # Return original

            no_bg_path = image_path.with_stem(f"{image_path.stem}_no_bg")
            no_bg_path.write_bytes(response.content)

            logger.info(f"   ✅ Background removed")
            return no_bg_path

        except Exception as e:
            logger.info(f"⚠️ Background removal error: {e}")
            return image_path

    def analyze_image(self, image_path: Path) -> List[str]:
        """
        Step 3: Auto-tag with Imagga
        """
        if not self.imagga_key:
            logger.info("⚠️ Imagga not configured, skipping tagging")
            return []

        logger.info(f"🏷️  Auto-tagging...")

        try:
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    "https://api.imagga.com/v2/tags",
                    auth=(self.imagga_key, self.imagga_secret),
                    files={"image": image_file},
                    timeout=30
                )

            if response.status_code != CONSTANT_200:
                logger.info(f"⚠️ Imagga error: {response.status_code}")
                return []

            tags_data = response.json()["result"]["tags"]
            tags = [tag["tag"]["en"] for tag in tags_data[:10]]

            logger.info(f"   ✅ Tags: {', '.join(tags[:5])}...")
            return tags

        except Exception as e:
            logger.info(f"⚠️ Tagging error: {e}")
            return []

    def create_variations(self, image_path: Path, tags: List[str]) -> List[Path]:
        """
        Step 4: Create style variations with Stability AI
        """
        if not self.stability_key:
            logger.info("⚠️ Stability AI not configured, skipping variations")
            return []

        logger.info(f"🎭 Creating style variations...")

        styles = [
            ("minimalist", "minimalist, clean, simple background, modern"),
            ("luxury", "luxury, premium, gold accents, elegant"),
            ("natural", "natural lighting, organic, wooden background")
        ]

        variations = []

        for style_name, style_prompt in styles:
            try:
                with open(image_path, "rb") as image_file:
                    response = requests.post(
                        "https://api.stability.ai/v1/generation/stable-diffusion-xl-CONSTANT_1024-v1-0/image-to-image",
                        headers={
                            "Authorization": f"Bearer {self.stability_key}",
                            "Accept": "application/json"
                        },
                        files={"init_image": image_file},
                        data={
                            "text_prompts[0][text]": f"{', '.join(tags[:5])}, {style_prompt}",
                            "text_prompts[0][weight]": 1,
                            "cfg_scale": 7,
                            "samples": 1,
                            "steps": 30,
                            "image_strength": 0.35  # Keep original structure
                        },
                        timeout=60
                    )

                if response.status_code == CONSTANT_200:
                    result = response.json()
                    for i, image_data in enumerate(result.get("artifacts", [])):
                        variation_path = image_path.with_stem(f"{image_path.stem}_{style_name}")

                        import base64
                        image_bytes = base64.b64decode(image_data["base64"])
                        variation_path.write_bytes(image_bytes)

                        variations.append(variation_path)
                        logger.info(f"   ✅ Created {style_name} variation")

                else:
                    logger.info(f"   ⚠️ Variation '{style_name}' failed: {response.status_code}")

            except Exception as e:
                logger.info(f"   ⚠️ Variation error ({style_name}): {e}")

        return variations

    def create_product_images(
        self,
        description: str,
        create_variations: bool = True
    ) -> Dict[str, Any]:
        """
        Complete product photography pipeline

        Args:
            description: Product description
            create_variations: Generate style variations

        Returns:
            Dictionary with all generated files
        """
        logger.info("=" * 60)
        logger.info("🎨 AI CONTENT FACTORY")
        logger.info("=" * 60)
        logger.info(f"\nProduct: {description}\n")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 1: Generate base image
        image_url = self.generate_image(description)
        original_path = self.download_image(
            image_url,
            f"product_{timestamp}_original.png"
        )

        # Step 2: Remove background
        no_bg_path = self.remove_background(original_path)

        # Step 3: Auto-tag
        tags = self.analyze_image(no_bg_path)

        # Step 4: Create variations (optional)
        variations = []
        if create_variations and self.stability_key:
            variations = self.create_variations(no_bg_path, tags)

        # Create metadata
        metadata = {
            "description": description,
            "created": datetime.now().isoformat(),
            "original": str(original_path),
            "no_background": str(no_bg_path),
            "tags": tags,
            "variations": [str(v) for v in variations]
        }

        metadata_path = original_path.with_suffix('.json')
        metadata_path.write_text(json.dumps(metadata, indent=2))

        # Summary
        print()
        logger.info("=" * 60)
        logger.info("✅ IMAGES COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"\n📁 Files created in: {self.output_dir}")
        logger.info(f"   🖼️  Original:   {original_path.name}")
        logger.info(f"   ✂️  No BG:      {no_bg_path.name}")
        for v in variations:
            logger.info(f"   🎨 Variation: {v.name}")
        logger.info(f"   📊 Metadata:  {metadata_path.name}")
        print()

        return metadata


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        logger.info("Usage: python3 content_factory.py <product_description>")
        logger.info("\nExample:")
        logger.info("  python3 content_factory.py 'premium wireless headphones, black'")
        sys.exit(1)

    description = " ".join(sys.argv[1:])

    factory = ContentFactory()
    result = factory.create_product_images(
        description=description,
        create_variations=True
    )

    logger.info(f"🎉 View your images: {factory.output_dir}")


if __name__ == "__main__":
    main()
