import os
import xml.etree.ElementTree as ET
import json
from collections import defaultdict
from pathlib import Path


class ASLAnalyzer:
    def __init__(self, asl_file_path):
        self.asl_file_path = asl_file_path
        self.styles = []
        self.categories = defaultdict(list)

    def parse_asl(self):
        """Parse the ASL file directly if it's not a zip archive"""
        try:
            with open(self.asl_file_path, "r") as file:
                content = file.read()
                # Assuming the file is XML or similar format
                root = ET.fromstring(content)
                self.parse_xml_styles(root)
        except Exception as e:
            print(f"Error parsing ASL file: {e}")

    def parse_xml_styles(self, root):
        """Parse styles from XML structure - handles various ASL formats"""
        styles = []
        for style_elem in root.findall(".//style"):
            style_data = self.extract_style_data(style_elem)
            if style_data:
                styles.append(style_data)
        self.styles = styles

    def extract_style_data(self, style_elem):
        """Extract data from a style element"""
        try:
            name = style_elem.get("name", "Unnamed Style")
            style_data = {
                "name": name,
                "type": "layer_style",
                "effects": [],
                "colors": [],
                "metadata": {},
            }
            return style_data
        except Exception as e:
            print(f"Error extracting style data: {e}")
            return None

    def analyze_and_sort(self):
        """Main analysis and sorting method"""
        print("Starting ASL analysis...")
        self.parse_asl()
        print(f"Analysis complete! Found {len(self.styles)} styles.")


def main():
    asl_file_path = "/Users/steven/adobe_style_analysis/All Styles.asl"
    if not os.path.exists(asl_file_path):
        print(f"Error: ASL file not found at {asl_file_path}")
        return
    try:
        analyzer = ASLAnalyzer(asl_file_path)
        analyzer.analyze_and_sort()
    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
