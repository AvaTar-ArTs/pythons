#!/usr/bin/env python3
"""
Advanced Whisper JSON to CSV Processor

This script processes JSON files from Whisper and converts them to a structured CSV format.
It includes enhanced error handling, configuration options, and improved data processing.

Features:
- Configurable input/output directories
- Customizable headers
- Better error handling and logging
- Progress tracking
- Validation of processed data
"""

import json
import os
import sys
import logging
from pathlib import Path
from glob import glob
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd


class WhisperJsonProcessor:
    """Processes Whisper JSON files and converts them to CSV format."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the processor with configuration.
        
        Args:
            config: Configuration dictionary with processing options
        """
        self.config = config or self._get_default_config()
        self.setup_logging()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'input_dir': '/Users/steven/Documents/Whisper-Text/',
            'output_file': 'combined_output3.csv',
            'headers': [
                "Title",
                "Summary",
                "Quotes",
                "Chapters",
                "Show Notes",
                "Newsletter",
                "Blog post",
                "LinkedIn",
                "Instagram",
                "X [Twitter]",
                "youtube seo info",
                "short youtube seo",
                "seo-trendy",
                "Typog",
                "creative youtube seo",
            ],
            'recursive': True,
            'file_pattern': '**/*.json',
            'encoding': 'utf-8',
            'log_level': 'INFO',
            'validate_data': True,
        }
    
    def setup_logging(self):
        """Set up logging configuration."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=getattr(logging, self.config['log_level'].upper()),
            format=log_format,
            handlers=[
                logging.FileHandler('whisper_processor.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self) -> bool:
        """Validate configuration settings."""
        input_path = Path(self.config['input_dir'])
        
        if not input_path.exists():
            self.logger.error(f"Input directory does not exist: {input_path}")
            return False
            
        if not input_path.is_dir():
            self.logger.error(f"Input path is not a directory: {input_path}")
            return False
            
        return True
    
    def find_json_files(self) -> List[str]:
        """Find all JSON files based on configuration."""
        input_path = Path(self.config['input_dir'])
        pattern = self.config['file_pattern']
        
        if self.config['recursive']:
            full_pattern = input_path / pattern
        else:
            full_pattern = input_path / pattern.replace('**/', '')
        
        json_files = glob(str(full_pattern), recursive=self.config['recursive'])
        # Sort files using built-in sorted function (lexicographic order)
        json_files = sorted(json_files)

        self.logger.info(f"Found {len(json_files)} JSON files to process")
        return json_files
    
    def process_json_file(self, file_path: str) -> Optional[Dict[str, str]]:
        """
        Process a single JSON file and extract content based on headers.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dictionary with header-content mappings or None if error
        """
        try:
            with open(file_path, "r", encoding=self.config['encoding']) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return None

        if not isinstance(data, list):
            self.logger.warning(f"Invalid format in {file_path}: Expected list, got {type(data)}")
            return None

        content_map = {}
        for entry in data:
            if not isinstance(entry, dict):
                continue

            if "name" in entry and "results" in entry:
                original_name = entry["name"]
                # Case-insensitive header matching
                matched_header = next(
                    (h for h in self.config['headers'] if h.lower() == original_name.lower()), 
                    None
                )

                if matched_header:
                    content = entry["results"][0]["body"] if entry["results"] else ""

                    if matched_header in content_map:
                        self.logger.warning(f"Duplicate field '{matched_header}' in {file_path} - overwriting")

                    content_map[matched_header] = content

        # Create row data with all headers
        row_data = {col: content_map.get(col, "") for col in self.config['headers']}
        return row_data
    
    def validate_processed_row(self, row_data: Dict[str, str], file_path: str) -> bool:
        """
        Validate processed row data.
        
        Args:
            row_data: Processed row data
            file_path: Original file path for logging
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(row_data, dict):
            self.logger.error(f"Invalid row data type in {file_path}: {type(row_data)}")
            return False
            
        # Check for required fields if specified
        required_fields = self.config.get('required_fields', [])
        for field in required_fields:
            if field not in row_data or not row_data[field].strip():
                self.logger.warning(f"Missing required field '{field}' in {file_path}")
                return False
                
        return True
    
    def process_all_files(self) -> pd.DataFrame:
        """
        Process all JSON files and return a DataFrame.
        
        Returns:
            DataFrame with processed data
        """
        if not self.validate_config():
            raise ValueError("Configuration validation failed")
        
        json_files = self.find_json_files()
        if not json_files:
            self.logger.warning("No JSON files found to process")
            return pd.DataFrame(columns=self.config['headers'])
        
        data_list = []
        processed_count = 0
        error_count = 0
        
        self.logger.info(f"Starting to process {len(json_files)} files...")
        
        for i, file_path in enumerate(json_files, 1):
            self.logger.info(f"Processing [{i}/{len(json_files)}]: {Path(file_path).name}")
            
            row_data = self.process_json_file(file_path)
            
            if row_data is not None:
                if self.config['validate_data']:
                    if self.validate_processed_row(row_data, file_path):
                        data_list.append(row_data)
                        processed_count += 1
                    else:
                        error_count += 1
                else:
                    data_list.append(row_data)
                    processed_count += 1
            else:
                error_count += 1
        
        self.logger.info(f"Processing complete: {processed_count} successful, {error_count} errors")
        
        df = pd.DataFrame(data_list, columns=self.config['headers'])
        return df
    
    def save_dataframe(self, df: pd.DataFrame) -> str:
        """
        Save DataFrame to CSV file.
        
        Args:
            df: DataFrame to save
            
        Returns:
            Path to saved file
        """
        output_path = Path(self.config['input_dir']) / self.config['output_file']
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        
        self.logger.info(f"Saved CSV with {len(df)} rows to: {output_path}")
        return str(output_path)
    
    def run(self) -> str:
        """
        Run the complete processing pipeline.
        
        Returns:
            Path to the saved CSV file
        """
        self.logger.info("Starting Whisper JSON to CSV processing...")
        
        try:
            df = self.process_all_files()
            output_path = self.save_dataframe(df)
            
            self.logger.info("Processing completed successfully!")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise


def main():
    """Main entry point with command-line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Process Whisper JSON files and convert to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python whisper_json_csv_processor.py                           # Use default config
  python whisper_json_csv_processor.py --input-dir /path/to/dir # Custom input directory
  python whisper_json_csv_processor.py --output-file output.csv # Custom output file
        """
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Input directory containing JSON files'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output CSV filename'
    )
    
    parser.add_argument(
        '--config-file',
        type=str,
        help='Configuration file path (JSON format)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    
    # Load from config file if provided
    if args.config_file:
        try:
            with open(args.config_file, 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)
    
    # Override with command-line arguments
    if args.input_dir:
        config['input_dir'] = args.input_dir
    if args.output_file:
        config['output_file'] = args.output_file
    if args.log_level:
        config['log_level'] = args.log_level
    
    # Create processor and run
    processor = WhisperJsonProcessor(config)
    
    try:
        output_path = processor.run()
        print(f"✅ Success! Created CSV with {len(pd.read_csv(output_path))} rows at:\n{output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()