"""
Etsy Image Metadata Refiner

This module provides functionality for etsy image metadata refiner.

Author: Auto-generated
Date: 2025-11-01
"""

import json
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logging.info("OpenAI client initialized successfully")
except Exception as e:
    logging.error(f"Initialization failed: {str(e)}")
    raise


# Retry decorator for API calls
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def analyze_image(row):
    """Analyze image metadata using OpenAI API with retry logic"""
    try:
        system_prompt = """You're an expert at analyzing image metadata for Etsy sellers. For each file:
        1. Suggest 1-3 categories based on filename/path
        2. Identify 3-5 keywords
        3. Flag quality issues (low DPI, small dimensions)
        Respond in JSON format: {category: [], keywords: [], quality_issues: []}"""

        user_prompt = f"""
        Analyze this image:
        - Filename: {row['Filename']}
        - Path: {row['Original Path']}
        - Dimensions: {row['Width']}x{row['Height']}
        - DPI: {row.get('DPI_X', 'N/A')}
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        return json.loads(response.choices[0].message.content)

    except json.JSONDecodeError:
        logging.error("Failed to parse JSON response")
        return {"category": [], "keywords": [], "quality_issues": []}
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        raise


def process_images(csv_path):
    """Process CSV file with image metadata"""
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        logging.info(f"Loaded {len(df)} records from {csv_path}")

        # Process rows
        results = []
        for index, row in df.iterrows():
            logging.info(f"Processing {index+1}/{len(df)}: {row['Filename']}")
            analysis = analyze_image(row)
            results.append(analysis)

        # Merge results
        result_df = pd.json_normalize(results)
        final_df = pd.concat([df, result_df], axis=1)

        # Save output
        output_path = csv_path.replace(".csv", "_analyzed.csv")
        final_df.to_csv(output_path, index=False)
        logging.info(f"Analysis complete. Saved to {output_path}")

        return final_df

    except Exception as e:
        logging.error(f"Processing failed: {str(e)}")
        raise


# Run the analysis
if __name__ == "__main__":
    csv_file = "image_data-03-16-16-32.csv"  # Update with your CSV path
    process_images(csv_file)
