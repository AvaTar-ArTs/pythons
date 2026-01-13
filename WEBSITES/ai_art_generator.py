#!/usr/bin/env python3
"""
🎨 AI Art Generator - Creative Asset Pack Creator
Generates high-quality AI art collections for sale
"""

import os
import json
import requests
import base64
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ArtStyle:
    """Art style configuration"""
    name: str
    description: str
    prompt_template: str
    style_keywords: List[str]
    color_palette: List[str]
    mood: str
    target_audience: str

class AIArtGenerator:
    """AI Art Generator for creating sellable art collections"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_path = Path("/Users/steven/ai-sites/retention-products-suite/digital-products/creative-asset-packs")
        self.output_path = self.base_path / "generated_art"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize art styles
        self.art_styles = self._initialize_art_styles()
        
    def _initialize_art_styles(self) -> List[ArtStyle]:
        """Initialize predefined art styles"""
        return [
            ArtStyle(
                name="Modern Minimalist",
                description="Clean, simple designs with bold colors and geometric shapes",
                prompt_template="Modern minimalist {subject}, {color_palette}, clean lines, geometric shapes, {mood}",
                style_keywords=["minimalist", "modern", "geometric", "clean", "bold"],
                color_palette=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
                mood="calm and professional",
                target_audience="business professionals, designers"
            ),
            ArtStyle(
                name="Vintage Retro",
                description="Nostalgic designs with warm colors and classic typography",
                prompt_template="Vintage retro {subject}, {color_palette}, aged texture, classic typography, {mood}",
                style_keywords=["vintage", "retro", "classic", "nostalgic", "warm"],
                color_palette=["#D4A574", "#8B4513", "#CD853F", "#DEB887", "#F5DEB3"],
                mood="warm and nostalgic",
                target_audience="vintage enthusiasts, collectors"
            ),
            ArtStyle(
                name="Cyberpunk Neon",
                description="Futuristic designs with neon colors and digital aesthetics",
                prompt_template="Cyberpunk neon {subject}, {color_palette}, glowing effects, digital art, {mood}",
                style_keywords=["cyberpunk", "neon", "futuristic", "digital", "glowing"],
                color_palette=["#00FFFF", "#FF00FF", "#00FF00", "#FFFF00", "#FF0080"],
                mood="energetic and futuristic",
                target_audience="gamers, tech enthusiasts, sci-fi fans"
            ),
            ArtStyle(
                name="Nature Organic",
                description="Natural designs with earth tones and organic shapes",
                prompt_template="Nature organic {subject}, {color_palette}, natural textures, organic shapes, {mood}",
                style_keywords=["nature", "organic", "natural", "earth", "botanical"],
                color_palette=["#228B22", "#8FBC8F", "#D2B48C", "#DEB887", "#F0E68C"],
                mood="peaceful and natural",
                target_audience="nature lovers, wellness enthusiasts"
            ),
            ArtStyle(
                name="Abstract Expressionist",
                description="Bold, expressive designs with vibrant colors and dynamic shapes",
                prompt_template="Abstract expressionist {subject}, {color_palette}, bold brushstrokes, dynamic composition, {mood}",
                style_keywords=["abstract", "expressionist", "bold", "dynamic", "vibrant"],
                color_palette=["#FF1493", "#00CED1", "#FFD700", "#FF4500", "#8A2BE2"],
                mood="energetic and expressive",
                target_audience="art collectors, creative professionals"
            )
        ]
    
    def generate_art_collection(self, style_name: str, collection_size: int = 20) -> Dict:
        """Generate a complete art collection"""
        style = next((s for s in self.art_styles if s.name == style_name), None)
        if not style:
            raise ValueError(f"Style '{style_name}' not found")
        
        logger.info(f"Generating {collection_size} artworks in {style_name} style")
        
        collection = {
            "style": style_name,
            "description": style.description,
            "target_audience": style.target_audience,
            "generated_at": datetime.now().isoformat(),
            "artworks": []
        }
        
        # Generate artworks
        for i in range(collection_size):
            try:
                artwork = self._generate_single_artwork(style, i + 1)
                collection["artworks"].append(artwork)
                logger.info(f"Generated artwork {i + 1}/{collection_size}")
            except Exception as e:
                logger.error(f"Error generating artwork {i + 1}: {e}")
                continue
        
        # Save collection metadata
        collection_path = self.output_path / f"{style_name.lower().replace(' ', '_')}_collection.json"
        with open(collection_path, 'w') as f:
            json.dump(collection, f, indent=2)
        
        # Generate collection preview
        self._generate_collection_preview(collection)
        
        return collection
    
    def _generate_single_artwork(self, style: ArtStyle, index: int) -> Dict:
        """Generate a single artwork"""
        subjects = [
            "landscape", "portrait", "cityscape", "abstract composition", "still life",
            "nature scene", "architectural detail", "geometric pattern", "floral arrangement",
            "urban environment", "seascape", "mountain vista", "forest path", "desert dunes"
        ]
        
        import random
        subject = random.choice(subjects)
        color = random.choice(style.color_palette)
        
        # Create prompt
        prompt = style.prompt_template.format(
            subject=subject,
            color_palette=color,
            mood=style.mood
        )
        
        # Generate image (mock implementation - replace with actual AI API)
        image_path = self._generate_mock_image(style, subject, index)
        
        artwork = {
            "id": f"{style.name.lower().replace(' ', '_')}_{index:03d}",
            "title": f"{style.name} {subject.title()} #{index}",
            "description": f"A {style.mood} {subject} in {style.name.lower()} style",
            "prompt": prompt,
            "style": style.name,
            "subject": subject,
            "color_palette": style.color_palette,
            "mood": style.mood,
            "image_path": str(image_path),
            "tags": style.style_keywords + [subject, style.mood],
            "pricing": {
                "standard": 9.99,
                "premium": 19.99,
                "commercial": 49.99
            },
            "licenses": ["personal", "commercial", "extended"],
            "dimensions": "1024x1024",
            "format": "PNG"
        }
        
        return artwork
    
    def _generate_mock_image(self, style: ArtStyle, subject: str, index: int) -> Path:
        """Generate a mock image (replace with actual AI generation)"""
        # Create a simple colored square as placeholder
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (1024, 1024), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple pattern based on style
        if "minimalist" in style.name.lower():
            # Draw geometric shapes
            for i in range(5):
                x = i * 200 + 50
                y = i * 150 + 50
                color = style.color_palette[i % len(style.color_palette)]
                draw.rectangle([x, y, x + 150, y + 100], fill=color)
        elif "vintage" in style.name.lower():
            # Draw vintage-style elements
            for i in range(3):
                x = i * 300 + 100
                y = i * 200 + 100
                color = style.color_palette[i % len(style.color_palette)]
                draw.ellipse([x, y, x + 200, y + 200], fill=color)
        else:
            # Draw abstract elements
            for i in range(8):
                x = (i % 4) * 250 + 50
                y = (i // 4) * 250 + 50
                color = style.color_palette[i % len(style.color_palette)]
                draw.polygon([(x, y), (x + 100, y + 50), (x + 50, y + 150)], fill=color)
        
        # Add text
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = f"{style.name}\n{subject.title()}\n#{index}"
        draw.text((50, 900), text, fill='black', font=font)
        
        # Save image
        image_path = self.output_path / f"{style.name.lower().replace(' ', '_')}_{index:03d}.png"
        img.save(image_path)
        
        return image_path
    
    def _generate_collection_preview(self, collection: Dict):
        """Generate a preview image for the collection"""
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a grid preview
        grid_size = 4
        cell_size = 200
        preview_size = grid_size * cell_size
        
        preview = Image.new('RGB', (preview_size, preview_size), color='white')
        draw = ImageDraw.Draw(preview)
        
        # Draw grid of artworks
        for i, artwork in enumerate(collection["artworks"][:16]):  # Max 16 for preview
            row = i // grid_size
            col = i % grid_size
            x = col * cell_size
            y = row * cell_size
            
            # Draw colored rectangle
            color = artwork["color_palette"][0] if artwork["color_palette"] else "#000000"
            draw.rectangle([x, y, x + cell_size - 2, y + cell_size - 2], fill=color)
            
            # Add artwork number
            draw.text((x + 10, y + 10), f"#{i + 1}", fill='white')
        
        # Save preview
        preview_path = self.output_path / f"{collection['style'].lower().replace(' ', '_')}_preview.png"
        preview.save(preview_path)
        
        logger.info(f"Collection preview saved to {preview_path}")
    
    def create_marketing_assets(self, collection: Dict):
        """Create marketing assets for the collection"""
        marketing_path = self.output_path / "marketing"
        marketing_path.mkdir(exist_ok=True)
        
        # Create collection description
        description = f"""
# {collection['style']} Art Collection

## Description
{collection['description']}

## Target Audience
{collection['target_audience']}

## Collection Details
- **Total Artworks**: {len(collection['artworks'])}
- **Style**: {collection['style']}
- **Generated**: {collection['generated_at']}

## Pricing Tiers
- **Standard License**: $9.99 per artwork
- **Premium License**: $19.99 per artwork  
- **Commercial License**: $49.99 per artwork

## What's Included
- High-resolution PNG files (1024x1024)
- Multiple license options
- Commercial use rights
- Print-ready quality
- Instant download

## Perfect For
- Website designs
- Social media content
- Print materials
- Digital art collections
- Creative projects

## Tags
{', '.join(collection['artworks'][0]['tags'] if collection['artworks'] else [])}
"""
        
        with open(marketing_path / "collection_description.md", 'w') as f:
            f.write(description)
        
        # Create pricing table
        pricing_table = """
| License Type | Price | Usage Rights |
|--------------|-------|--------------|
| Personal | $9.99 | Personal projects only |
| Commercial | $19.99 | Commercial use, up to 10,000 copies |
| Extended | $49.99 | Unlimited commercial use |
| Collection Bundle | $149.99 | All artworks, all licenses |
"""
        
        with open(marketing_path / "pricing_table.md", 'w') as f:
            f.write(pricing_table)
        
        logger.info(f"Marketing assets created in {marketing_path}")

def main():
    """Main function to generate art collections"""
    generator = AIArtGenerator()
    
    print("🎨 AI Art Generator - Creative Asset Pack Creator")
    print("=" * 50)
    
    # Generate collections for all styles
    for style in generator.art_styles:
        print(f"\n🎨 Generating {style.name} collection...")
        try:
            collection = generator.generate_art_collection(style.name, 20)
            generator.create_marketing_assets(collection)
            print(f"✅ {style.name} collection generated successfully!")
            print(f"   - {len(collection['artworks'])} artworks created")
            print(f"   - Target audience: {style.target_audience}")
        except Exception as e:
            print(f"❌ Error generating {style.name} collection: {e}")
    
    print(f"\n🎉 All art collections generated!")
    print(f"📁 Output directory: {generator.output_path}")

if __name__ == "__main__":
    main()