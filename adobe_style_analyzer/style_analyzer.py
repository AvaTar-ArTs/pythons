import os
import zipfile
import xml.etree.ElementTree as ET
import json
from collections import defaultdict
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class ASLAnalyzer:
    def __init__(self, asl_file_path):
        self.asl_file_path = asl_file_path
        self.styles = []
        self.categories = defaultdict(list)

    def extract_asl(self):
        """Extract ASL file (which is a zip archive)"""
        extract_path = self.asl_file_path.replace('.asl', '_extracted')
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        with zipfile.ZipFile(self.asl_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return extract_path

    def parse_styles(self, extract_path):
        """Parse the ASL XML structure to extract style information"""
        xml_files = list(Path(extract_path).rglob('*.xml'))
        styles_xml = next((xml_file for xml_file in xml_files if 'styles' in str(xml_file).lower() or 'asl' in str(xml_file).lower()), None)
        if not styles_xml:
            styles_xml = xml_files[0] if xml_files else None
        if not styles_xml:
            raise FileNotFoundError("No XML files found in ASL archive")
        print(f"Parsing styles from: {styles_xml}")
        tree = ET.parse(styles_xml)
        root = tree.getroot()
        self.parse_xml_styles(root)

    def parse_xml_styles(self, root):
        """Parse styles from XML structure - handles various ASL formats"""
        styles = []
        for style_elem in root.findall('.//style'):
            style_data = self.extract_style_data(style_elem)
            if style_data:
                styles.append(style_data)
        for pattern_elem in root.findall('.//pattern'):
            style_data = self.extract_pattern_data(pattern_elem)
            if style_data:
                styles.append(style_data)
        if not styles:
            for elem in root.iter():
                if elem.get('name'):
                    style_data = self.extract_generic_style_data(elem)
                    if style_data:
                        styles.append(style_data)
        self.styles = styles

    def extract_style_data(self, style_elem):
        """Extract data from a style element"""
        try:
            name = style_elem.get('name', 'Unnamed Style')
            style_data = {
                'name': name,
                'type': 'layer_style',
                'effects': [],
                'colors': [],
                'metadata': {}
            }
            for effect in style_elem.findall('.//effect'):
                effect_type = effect.get('type', '')
                effect_data = {
                    'type': effect_type,
                    'parameters': {param.tag: param.text for param in effect}
                }
                style_data['effects'].append(effect_data)
            style_data['colors'] = self.extract_colors_from_effects(style_data['effects'])
            style_data['dominant_color'] = self.get_dominant_color(style_data['colors'])
            style_data['color_palette'] = self.generate_color_palette(style_data['colors'])
            return style_data
        except Exception as e:
            print(f"Error extracting style data: {e}")
            return None

    def extract_pattern_data(self, pattern_elem):
        """Extract data from a pattern element"""
        try:
            name = pattern_elem.get('name', 'Unnamed Pattern')
            return {
                'name': name,
                'type': 'pattern',
                'colors': self.extract_colors_from_pattern(pattern_elem),
                'metadata': {}
            }
        except Exception as e:
            print(f"Error extracting pattern data: {e}")
            return None

    def extract_generic_style_data(self, elem):
        """Extract style data from generic elements"""
        try:
            name = elem.get('name', 'Unnamed')
            return {
                'name': name,
                'type': 'generic',
                'metadata': dict(elem.attrib)
            }
        except Exception as e:
            print(f"Error extracting generic style data: {e}")
            return None

    def extract_colors_from_effects(self, effects):
        """Extract colors from style effects"""
        colors = set()
        for effect in effects:
            params = effect['parameters']
            for key, value in params.items():
                if value and any(color_term in key.lower() for color_term in ['color', 'rgb', 'hex', 'hue', 'tint']):
                    colors.update(self.parse_color_value(value))
        return list(colors)

    def extract_colors_from_pattern(self, pattern_elem):
        """Extract colors from pattern data"""
        colors = set()
        for child in pattern_elem:
            if 'color' in child.tag.lower() or (child.text and '#' in child.text):
                colors.update(self.parse_color_value(child.text))
        return list(colors)

    def parse_color_value(self, value):
        """Parse color values from various formats"""
        colors = set()
        if not value:
            return colors
        if '#' in value:
            hex_values = value.split('#')[1:]
            for hex_val in hex_values:
                if len(hex_val) >= 6:
                    colors.add(f"#{hex_val[:6]}")
        elif 'rgb' in value.lower():
            try:
                rgb_values = value.split('(')[1].split(')')[0].split(',')
                if len(rgb_values) >= 3:
                    r, g, b = map(int, rgb_values[:3])
                    colors.add(f"#{r:02x}{g:02x}{b:02x}")
            except ValueError:
                pass
        return colors

    def get_dominant_color(self, colors):
        """Determine the dominant color from a list"""
        return colors[0] if colors else "#808080"

    def generate_color_palette(self, colors):
        """Generate a color palette from extracted colors"""
        return colors[:5] if colors else ["#808080", "#a0a0a0", "#606060"]

    def categorize_styles(self):
        """Categorize styles based on their properties"""
        for style in self.styles:
            category = self.determine_style_category(style)
            self.categories[category].append(style)

    def determine_style_category(self, style):
        """Determine the category for a style based on its properties"""
        name_lower = style['name'].lower()
        effects = [effect['type'].lower() for effect in style['effects']]
        if any(word in name_lower for word in ['metal', 'chrome', 'gold', 'silver', 'steel']):
            return 'Metallic'
        elif any(word in name_lower for word in ['neon', 'glow', 'light', 'bright']):
            return 'Neon'
        elif any(word in name_lower for word in ['grunge', 'dirty', 'rust', 'distress']):
            return 'Grunge'
        elif any(word in name_lower for word in ['glass', 'crystal', 'transparent']):
            return 'Glass'
        elif any(word in name_lower for word in ['button', 'web', 'ui', 'interface']):
            return 'UI Elements'
        elif any(word in name_lower for word in ['text', 'font', 'type', 'typography']):
            return 'Text Effects'
        elif any(word in name_lower for word in ['gradient', 'colorful']):
            return 'Gradient'
        elif any(word in name_lower for word in ['pattern', 'texture']):
            return 'Patterns'
        elif any(word in name_lower for word in ['shadow', 'bevel', 'emboss']):
            return 'Basic Effects'
        else:
            return 'Miscellaneous'

    def generate_visual_preview(self, style, preview_size=(200, 150)):
        """Generate a visual preview of the style"""
        img = Image.new('RGB', preview_size, color='#2d2d2d')
        draw = ImageDraw.Draw(img)
        margin = 20
        shape_width = preview_size[0] - 2 * margin
        shape_height = preview_size[1] - 2 * margin
        shape_coords = [(margin, margin), (margin + shape_width, margin + shape_height)]
        fill_color = self.hex_to_rgb(style.get('dominant_color', '#808080'))
        draw.rectangle(shape_coords, fill=fill_color, outline='#ffffff', width=2)
        try:
            font = ImageFont.load_default()
            text_bbox = draw.textbbox((0, 0), style['name'], font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (preview_size[0] - text_width) // 2
            text_y = margin + shape_height + 5
            draw.text((text_x, text_y), style['name'], fill='#ffffff', font=font)
        except Exception as e:
            print(f"Error drawing text: {e}")
        return img

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def analyze_and_sort(self):
        """Main analysis and sorting method"""
        print("Starting ASL analysis...")
        extract_path = self.extract_asl()
        print("Parsing styles...")
        self.parse_styles(extract_path)
        print("Categorizing styles...")
        self.categorize_styles()
        print("Generating output...")
        self.generate_output()
        shutil.rmtree(extract_path)
        print(f"Analysis complete! Found {len(self.styles)} styles across {len(self.categories)} categories.")

    def generate_output(self):
        """Generate comprehensive output files"""
        output_dir = Path(self.asl_file_path).parent / "ASL_Analysis_Results"
        output_dir.mkdir(exist_ok=True)
        self.generate_json_report(output_dir)
        self.generate_category_folders(output_dir)
        self.generate_summary_report(output_dir)

    def generate_json_report(self, output_dir):
        """Generate detailed JSON report"""
        report = {
            'source_file': self.asl_file_path,
            'total_styles': len(self.styles),
            'categories': {},
            'analysis_summary': {
                'total_categories': len(self.categories),
                'styles_per_category': {cat: len(styles) for cat, styles in self.categories.items()}
            }
        }
        for category, styles in self.categories.items():
            report['categories'][category] = [{
                'name': style['name'],
                'type': style['type'],
                'dominant_color': style.get('dominant_color'),
                'color_palette': style.get('color_palette', []),
                'effect_count': len(style.get('effects', [])),
                'effect_types': [effect['type'] for effect in style.get('effects', [])]
            } for style in styles]
        with open(output_dir / 'asl_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)

    def generate_category_folders(self, output_dir):
        """Generate organized category folders with previews"""
        previews_dir = output_dir / "Previews"
        previews_dir.mkdir(exist_ok=True)
        for category, styles in self.categories.items():
            category_dir = previews_dir / category
            category_dir.mkdir(exist_ok=True)
            for style in styles:
                preview_img = self.generate_visual_preview(style)
                clean_name = "".join(c for c in style['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                preview_path = category_dir / f"{clean_name}.png"
                preview_img.save(preview_path)

    def generate_summary_report(self, output_dir):
        """Generate a human-readable summary report"""
        report_path = output_dir / "analysis_summary.md"
        with open(report_path, 'w') as f:
            f.write("# ASL Style Library Analysis Report\n\n")
            f.write(f"**Source File:** `{self.asl_file_path}`\n")
            f.write(f"**Total Styles Found:** {len(self.styles)}\n")
            f.write(f"**Categories Identified:** {len(self.categories)}\n\n")
            f.write("## Category Breakdown\n\n")
            for category, styles in sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"### {category} ({len(styles)} styles)\n")
                for style in styles[:5]:
                    f.write(f"- {style['name']}\n")
                    if style.get('color_palette'):
                        colors = ' '.join([f"`{color}`" for color in style['color_palette'][:3]])
                        f.write(f"  Colors: {colors}\n")
                if len(styles) > 5:
                    f.write(f"- ... and {len(styles) - 5} more\n")
                f.write("\n")
            f.write("## Style Statistics\n\n")
            f.write("| Category | Style Count | Percentage |\n")
            f.write("|----------|-------------|------------|\n")
            total_styles = len(self.styles)
            for category, styles in sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True):
                percentage = (len(styles) / total_styles) * 100
                f.write(f"| {category} | {len(styles)} | {percentage:.1f}% |\n")

def main():
    asl_file_path = input("Please enter the path to the ASL file: ")
    if not os.path.exists(asl_file_path):
        print(f"Error: ASL file not found at {asl_file_path}")
        print("Please check the path and try again.")
        return
    try:
        analyzer = ASLAnalyzer(asl_file_path)
        analyzer.analyze_and_sort()
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total styles analyzed: {len(analyzer.styles)}")
        print(f"Categories found: {len(analyzer.categories)}")
        print("\nCategory breakdown:")
        for category, styles in sorted(analyzer.categories.items(), key=lambda x: len(x[1]), reverse=True):
            percentage = (len(styles) / len(analyzer.styles)) * 100
            print(f"  {category}: {len(styles)} styles ({percentage:.1f}%)")
        output_dir = Path(asl_file_path).parent / "ASL_Analysis_Results"
        print(f"\nDetailed reports saved to: {output_dir}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
