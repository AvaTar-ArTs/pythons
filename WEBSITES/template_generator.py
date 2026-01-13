#!/usr/bin/env python3
"""
🛍️ Template Generator - Marketplace System
Generates high-quality templates for sale
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Template:
    """Template data structure"""
    id: str
    name: str
    description: str
    category: str
    subcategory: str
    price: float
    file_format: str
    dimensions: str
    tags: List[str]
    features: List[str]
    preview_url: str
    download_url: str
    created_at: str
    updated_at: str

class TemplateGenerator:
    """Template generator for marketplace"""
    
    def __init__(self):
        self.base_path = Path("/Users/steven/ai-sites/retention-products-suite/templates-marketplace")
        self.templates_path = self.base_path / "generated_templates"
        self.templates_path.mkdir(parents=True, exist_ok=True)
        
        # Template categories and configurations
        self.template_configs = self._initialize_template_configs()
        
    def _initialize_template_configs(self) -> Dict:
        """Initialize template configurations"""
        return {
            "website_templates": {
                "categories": ["business", "portfolio", "ecommerce", "blog", "landing"],
                "price_range": (29.99, 199.99),
                "formats": ["HTML", "WordPress", "React", "Vue"],
                "features": [
                    "Responsive Design", "SEO Optimized", "Mobile Friendly",
                    "Cross Browser Compatible", "Fast Loading", "Modern UI/UX"
                ]
            },
            "email_templates": {
                "categories": ["newsletter", "promotional", "transactional", "welcome", "followup"],
                "price_range": (9.99, 49.99),
                "formats": ["HTML", "Mailchimp", "Constant Contact", "SendGrid"],
                "features": [
                    "Mobile Responsive", "Dark Mode Support", "A/B Test Ready",
                    "Email Client Compatible", "Accessibility Compliant"
                ]
            },
            "social_media_templates": {
                "categories": ["instagram", "facebook", "twitter", "linkedin", "pinterest"],
                "price_range": (4.99, 24.99),
                "formats": ["PSD", "PNG", "JPG", "AI", "Figma"],
                "features": [
                    "High Resolution", "Multiple Sizes", "Easy to Customize",
                    "Brand Consistent", "Trendy Designs"
                ]
            },
            "presentation_templates": {
                "categories": ["business", "pitch", "education", "creative", "minimalist"],
                "price_range": (19.99, 99.99),
                "formats": ["PowerPoint", "Keynote", "Google Slides", "PDF"],
                "features": [
                    "Professional Design", "Easy to Edit", "Multiple Layouts",
                    "Charts & Graphs", "Icons & Illustrations"
                ]
            },
            "print_templates": {
                "categories": ["business_cards", "flyers", "posters", "brochures", "invitations"],
                "price_range": (7.99, 39.99),
                "formats": ["AI", "PSD", "PDF", "InDesign"],
                "features": [
                    "Print Ready", "High Resolution", "CMYK Color",
                    "Bleed Marks", "Multiple Sizes"
                ]
            }
        }
    
    def generate_template_collection(self, template_type: str, count: int = 20) -> List[Template]:
        """Generate a collection of templates"""
        logger.info(f"Generating {count} {template_type} templates")
        
        if template_type not in self.template_configs:
            raise ValueError(f"Template type '{template_type}' not supported")
        
        config = self.template_configs[template_type]
        templates = []
        
        for i in range(count):
            template = self._generate_single_template(template_type, config, i + 1)
            templates.append(template)
            
            # Generate template files
            self._generate_template_files(template)
        
        # Save collection metadata
        self._save_collection_metadata(template_type, templates)
        
        return templates
    
    def _generate_single_template(self, template_type: str, config: Dict, index: int) -> Template:
        """Generate a single template"""
        category = random.choice(config["categories"])
        subcategory = self._generate_subcategory(category)
        name = self._generate_template_name(template_type, category, index)
        
        template = Template(
            id=f"{template_type}_{category}_{index:03d}",
            name=name,
            description=self._generate_description(template_type, category, subcategory),
            category=template_type.replace("_", " ").title(),
            subcategory=subcategory,
            price=round(random.uniform(*config["price_range"]), 2),
            file_format=random.choice(config["formats"]),
            dimensions=self._generate_dimensions(template_type),
            tags=self._generate_tags(template_type, category),
            features=random.sample(config["features"], random.randint(3, 6)),
            preview_url=f"previews/{template_type}_{category}_{index:03d}_preview.jpg",
            download_url=f"downloads/{template_type}_{category}_{index:03d}.zip",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        return template
    
    def _generate_subcategory(self, category: str) -> str:
        """Generate subcategory based on category"""
        subcategories = {
            "business": ["corporate", "startup", "agency", "consulting"],
            "portfolio": ["creative", "developer", "designer", "photographer"],
            "ecommerce": ["fashion", "electronics", "food", "beauty"],
            "blog": ["lifestyle", "tech", "travel", "food"],
            "landing": ["saas", "app", "course", "event"],
            "newsletter": ["weekly", "monthly", "daily", "special"],
            "promotional": ["sale", "launch", "event", "seasonal"],
            "instagram": ["story", "post", "reel", "highlight"],
            "facebook": ["cover", "post", "ad", "event"],
            "business_cards": ["modern", "classic", "creative", "minimalist"]
        }
        
        return random.choice(subcategories.get(category, ["standard"]))
    
    def _generate_template_name(self, template_type: str, category: str, index: int) -> str:
        """Generate template name"""
        adjectives = ["Modern", "Elegant", "Creative", "Professional", "Minimalist", "Bold", "Clean", "Stylish"]
        nouns = ["Design", "Template", "Layout", "Theme", "Style", "Framework", "Kit", "Collection"]
        
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        
        return f"{adjective} {category.title()} {noun} #{index}"
    
    def _generate_description(self, template_type: str, category: str, subcategory: str) -> str:
        """Generate template description"""
        descriptions = {
            "website_templates": f"A stunning {subcategory} {category} website template perfect for modern businesses. Features responsive design, clean code, and professional aesthetics.",
            "email_templates": f"Professional {subcategory} email template designed for {category} campaigns. Mobile-responsive and email client compatible.",
            "social_media_templates": f"Eye-catching {subcategory} template for {category} social media posts. High-quality design that stands out in feeds.",
            "presentation_templates": f"Professional {subcategory} presentation template for {category} purposes. Clean design with multiple layout options.",
            "print_templates": f"High-quality {subcategory} {category} template ready for print. Professional design with proper bleed and margins."
        }
        
        return descriptions.get(template_type, f"Professional {category} template for {subcategory} use.")
    
    def _generate_dimensions(self, template_type: str) -> str:
        """Generate template dimensions"""
        dimensions = {
            "website_templates": ["1920x1080", "1440x900", "1366x768", "1280x720"],
            "email_templates": ["600x400", "600x600", "600x800", "600x1200"],
            "social_media_templates": ["1080x1080", "1080x1350", "1080x1920", "1200x630"],
            "presentation_templates": ["1920x1080", "1280x720", "1024x768", "1600x900"],
            "print_templates": ["8.5x11", "11x17", "A4", "A3", "5x7", "4x6"]
        }
        
        return random.choice(dimensions.get(template_type, ["1920x1080"]))
    
    def _generate_tags(self, template_type: str, category: str) -> List[str]:
        """Generate template tags"""
        base_tags = [template_type.replace("_", " "), category, "template", "design"]
        
        additional_tags = {
            "website_templates": ["responsive", "modern", "clean", "professional", "seo"],
            "email_templates": ["mobile", "responsive", "newsletter", "marketing", "html"],
            "social_media_templates": ["instagram", "facebook", "social", "marketing", "graphic"],
            "presentation_templates": ["powerpoint", "business", "corporate", "slides", "presentation"],
            "print_templates": ["print", "business", "marketing", "professional", "branding"]
        }
        
        tags = base_tags + random.sample(additional_tags.get(template_type, []), 3)
        return list(set(tags))  # Remove duplicates
    
    def _generate_template_files(self, template: Template):
        """Generate actual template files"""
        template_dir = self.templates_path / template.id
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate main template file
        self._generate_main_template_file(template, template_dir)
        
        # Generate preview image
        self._generate_preview_image(template, template_dir)
        
        # Generate documentation
        self._generate_documentation(template, template_dir)
        
        # Generate license file
        self._generate_license_file(template, template_dir)
        
        # Generate README
        self._generate_readme(template, template_dir)
    
    def _generate_main_template_file(self, template: Template, template_dir: Path):
        """Generate the main template file"""
        if template.file_format == "HTML":
            content = self._generate_html_template(template)
            file_path = template_dir / f"{template.id}.html"
        elif template.file_format == "PSD":
            content = self._generate_psd_placeholder(template)
            file_path = template_dir / f"{template.id}.psd"
        else:
            content = self._generate_generic_template(template)
            file_path = template_dir / f"{template.id}.{template.file_format.lower()}"
        
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _generate_html_template(self, template: Template) -> str:
        """Generate HTML template"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template.name}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            text-align: center;
        }}
        .header h1 {{
            font-size: 3rem;
            margin: 0;
            font-weight: 300;
        }}
        .header p {{
            font-size: 1.2rem;
            margin: 20px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 80px 0;
            text-align: center;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            margin: 60px 0;
        }}
        .feature {{
            padding: 40px 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .feature h3 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .cta {{
            background: #28a745;
            color: white;
            padding: 20px 40px;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            cursor: pointer;
            margin-top: 40px;
        }}
        .cta:hover {{
            background: #218838;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{template.name}</h1>
            <p>{template.description}</p>
        </header>
        
        <main class="content">
            <h2>Template Features</h2>
            <div class="features">
                {''.join(f'<div class="feature"><h3>{feature}</h3><p>Professional {feature.lower()} implementation</p></div>' for feature in template.features)}
            </div>
            
            <button class="cta">Get Started</button>
        </main>
    </div>
</body>
</html>"""
    
    def _generate_psd_placeholder(self, template: Template) -> str:
        """Generate PSD placeholder content"""
        return f"""PSD Template: {template.name}
Description: {template.description}
Dimensions: {template.dimensions}
Features: {', '.join(template.features)}
Created: {template.created_at}
Price: ${template.price}"""
    
    def _generate_generic_template(self, template: Template) -> str:
        """Generate generic template content"""
        return f"""Template: {template.name}
Description: {template.description}
Category: {template.category}
Subcategory: {template.subcategory}
Price: ${template.price}
Format: {template.file_format}
Dimensions: {template.dimensions}
Features: {', '.join(template.features)}
Tags: {', '.join(template.tags)}
Created: {template.created_at}"""
    
    def _generate_preview_image(self, template: Template, template_dir: Path):
        """Generate preview image (placeholder)"""
        preview_content = f"""Preview for {template.name}
{template.description}
Dimensions: {template.dimensions}
Price: ${template.price}
Features: {', '.join(template.features[:3])}..."""
        
        with open(template_dir / f"{template.id}_preview.txt", 'w') as f:
            f.write(preview_content)
    
    def _generate_documentation(self, template: Template, template_dir: Path):
        """Generate template documentation"""
        doc_content = f"""# {template.name}

## Description
{template.description}

## Features
{chr(10).join(f"- {feature}" for feature in template.features)}

## Technical Specifications
- **Format**: {template.file_format}
- **Dimensions**: {template.dimensions}
- **Category**: {template.category}
- **Subcategory**: {template.subcategory}

## Usage Instructions
1. Download the template files
2. Open in your preferred design software
3. Customize colors, text, and images
4. Export in your desired format

## License
This template is licensed for commercial use. See LICENSE file for details.

## Support
For support and customization requests, contact our team.

## Tags
{', '.join(template.tags)}
"""
        
        with open(template_dir / "DOCUMENTATION.md", 'w') as f:
            f.write(doc_content)
    
    def _generate_license_file(self, template: Template, template_dir: Path):
        """Generate license file"""
        license_content = f"""Template License Agreement

Template: {template.name}
Price: ${template.price}

LICENSE TERMS:

1. COMMERCIAL USE
   - This template may be used for commercial projects
   - Client work is permitted
   - Resale of the template itself is prohibited

2. MODIFICATIONS
   - You may modify the template as needed
   - Modified versions may be used commercially
   - Credit to original creator is appreciated but not required

3. DISTRIBUTION
   - Do not redistribute the original template files
   - Do not share with others who haven't purchased
   - Do not resell or sublicense

4. WARRANTY
   - Template provided "as is"
   - No warranty of fitness for particular purpose
   - Use at your own risk

5. TERMINATION
   - License terminates if terms are violated
   - No refunds for license termination

By using this template, you agree to these terms.
"""
        
        with open(template_dir / "LICENSE.txt", 'w') as f:
            f.write(license_content)
    
    def _generate_readme(self, template: Template, template_dir: Path):
        """Generate README file"""
        readme_content = f"""# {template.name}

{template.description}

## Quick Start
1. Download all files
2. Open the main template file
3. Customize to your needs
4. Export and use

## What's Included
- Main template file
- Documentation
- License information
- Preview image

## Support
Contact us for customization services and support.

## Price
${template.price}

---
Generated by Creative AI Empire Template Generator
"""
        
        with open(template_dir / "README.md", 'w') as f:
            f.write(readme_content)
    
    def _save_collection_metadata(self, template_type: str, templates: List[Template]):
        """Save collection metadata"""
        collection_data = {
            "template_type": template_type,
            "total_templates": len(templates),
            "generated_at": datetime.now().isoformat(),
            "templates": [
                {
                    "id": template.id,
                    "name": template.name,
                    "description": template.description,
                    "category": template.category,
                    "subcategory": template.subcategory,
                    "price": template.price,
                    "file_format": template.file_format,
                    "dimensions": template.dimensions,
                    "tags": template.tags,
                    "features": template.features,
                    "preview_url": template.preview_url,
                    "download_url": template.download_url
                }
                for template in templates
            ]
        }
        
        collection_path = self.templates_path / f"{template_type}_collection.json"
        with open(collection_path, 'w') as f:
            json.dump(collection_data, f, indent=2)
        
        logger.info(f"Collection metadata saved to {collection_path}")

def main():
    """Main function to generate templates"""
    generator = TemplateGenerator()
    
    print("🛍️ Template Generator - Marketplace System")
    print("=" * 50)
    
    # Generate templates for all types
    for template_type in generator.template_configs.keys():
        print(f"\n🛍️ Generating {template_type} templates...")
        try:
            templates = generator.generate_template_collection(template_type, 15)
            print(f"✅ Generated {len(templates)} {template_type} templates")
            
            # Calculate total value
            total_value = sum(template.price for template in templates)
            print(f"   Total value: ${total_value:.2f}")
            
        except Exception as e:
            print(f"❌ Error generating {template_type} templates: {e}")
    
    print(f"\n🎉 All templates generated!")
    print(f"📁 Output directory: {generator.templates_path}")

if __name__ == "__main__":
    main()