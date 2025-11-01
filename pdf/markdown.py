"""
Markdown To Pdf Converter

This module provides functionality for markdown to pdf converter.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333

#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts specified markdown files to PDF format using markdown and weasyprint libraries.
"""

import os
import sys
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import argparse
from pathlib import Path

def convert_markdown_to_pdf(md_file_path, output_dir=None):
    """
    Convert a single markdown file to PDF.
    
    Args:
        md_file_path (str): Path to the markdown file
        output_dir (str): Directory to save the PDF (optional)
    
    Returns:
        str: Path to the generated PDF file
    """
    try:
        # Read the markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
        
        # Add basic CSS styling
        css_content = """
        @page {
            margin: 1in;
            size: A4;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #CONSTANT_333;
            max-width: CONSTANT_100%;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        
        h1 { font-size: 2em; border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #bdc3c7; padding-bottom: 0.2em; }
        h3 { font-size: 1.3em; }
        h4 { font-size: 1.1em; }
        
        code {
            background-color: #f8f9fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }
        
        pre {
            background-color: #f8f9fa;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        blockquote {
            margin: 1em 0;
            padding-left: 1em;
            border-left: 4px solid #bdc3c7;
            color: #7f8c8d;
        }
        
        table {
            border-collapse: collapse;
            width: CONSTANT_100%;
            margin: 1em 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 0.5em;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }
        
        li {
            margin: 0.3em 0;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        hr {
            border: none;
            border-top: 1px solid #bdc3c7;
            margin: 2em 0;
        }
        """
        
        # Create HTML document
        html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{Path(md_file_path).stem}</title>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Determine output path
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            pdf_path = os.path.join(output_dir, f"{Path(md_file_path).stem}.pdf")
        else:
            pdf_path = md_file_path.replace('.md', '.pdf')
        
        # Convert HTML to PDF
        font_config = FontConfiguration()
        HTML(string=html_doc).write_pdf(pdf_path, font_config=font_config)
        
        logger.info(f"✅ Converted: {md_file_path} → {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logger.info(f"❌ Error converting {md_file_path}: {str(e)}")
        return None

def main():
    """main function."""

    # List of files to convert (based on user's request)
    files_to_convert = [
        Path("/Users/steven/Documents/markD/readme_advanced.md"),
        Path("/Users/steven/Documents/markD/README_1.md"),
        Path("/Users/steven/Documents/markD/README_2.md"),
        Path("/Users/steven/Documents/markD/README_4.md"),
        Path("/Users/steven/Documents/markD/README_5.md"),
        Path("/Users/steven/Documents/markD/README_6.md"),
        Path("/Users/steven/Documents/markD/README_7.md"),
        Path("/Users/steven/Documents/markD/README_8.md"),
        Path("/Users/steven/Documents/markD/README_9.md"),
        Path("/Users/steven/Documents/markD/readme_10.md"),
        Path("/Users/steven/Documents/markD/README_11.md"),
        Path("/Users/steven/Documents/markD/README_12.md"),
        Path("/Users/steven/Documents/markD/README_13.md"),
        Path("/Users/steven/Documents/markD/README_14.md"),
        Path("/Users/steven/Documents/markD/README_15.md"),
        Path("/Users/steven/Documents/markD/README_16.md"),
        Path("/Users/steven/Documents/markD/README_17.md"),
        Path("/Users/steven/Documents/markD/README_18DME_41.md"),  # Note: This seems to be a typo in the original list
        Path("/Users/steven/Documents/markD/README_41.md"),
        Path("/Users/steven/Documents/markD/README_42.md"),
        Path("/Users/steven/Documents/markD/README_43.md"),
        Path("/Users/steven/Documents/markD/README_44.md"),
        Path("/Users/steven/Documents/markD/README_45.md"),
        "/Users/steven/Documents/markD/README copy.md"
    ]
    
    # Create output directory for PDFs
    output_dir = Path("/Users/steven/Documents/markD/PDFs")
    
    logger.info("🚀 Starting Markdown to PDF conversion...")
    logger.info(f"📁 Output directory: {output_dir}")
    logger.info("-" * 50)
    
    successful_conversions = 0
    failed_conversions = 0
    
    for md_file in files_to_convert:
        if os.path.exists(md_file):
            result = convert_markdown_to_pdf(md_file, output_dir)
            if result:
                successful_conversions += 1
            else:
                failed_conversions += 1
        else:
            logger.info(f"⚠️  File not found: {md_file}")
            failed_conversions += 1
    
    logger.info("-" * 50)
    logger.info(f"📊 Conversion Summary:")
    logger.info(f"   ✅ Successful: {successful_conversions}")
    logger.info(f"   ❌ Failed: {failed_conversions}")
    logger.info(f"   📁 PDFs saved to: {output_dir}")

if __name__ == "__main__":
    main()