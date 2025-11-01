"""
Ai Tools Gpt Autofill 4

This module provides functionality for ai tools gpt autofill 4.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# CONFIG
load_dotenv(os.path.expanduser("~/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
CSV_PATH = Path(
    str(Path.home()) + "/Documents/python/clean/CSV/prompts_expanded_image_data-05-30-22-21.csv"
)
OUT_CSV = Path(
    str(Path.home()) + "/Documents/python/clean/CSV/filled_prompts_expanded_image_data-05-30-22-21.csv"
)
LOG_PATH = Path(str(Path.home()) + "/Documents/python/clean/CSV/fill_log.txt")

# List analytic fields and prompt fields to fill
ANALYSIS_FIELDS = [
    "main_subject",
    "style",
    "color_palette",
    "tags",
    "orientation",
    "suggested_products",
    "SEO_title",
    "SEO_description",
    "emotion",
    "safety_rating",
    "dominant_keyword",
]
PROMPT_PREFIX = "Prompt_"


def gpt_fill(context_dict, field, style=None):
    """gpt_fill function."""

    sys_prompt = (
        "You are a creative AI for print-on-demand design and SEO. "
        "Given image info and the current row's context, fill in the missing field with a relevant, detailed, SEO-optimized answer."
    )
    if style:
        user_prompt = (
            f"Given the context: {json.dumps(context_dict)}\n"
            f"Generate a product-ready, descriptive, SEO-friendly image prompt for the style: '{style}'."
        )
    else:
        user_prompt = (
            f"Given the context: {json.dumps(context_dict)}\n"
            f"Generate a creative and SEO-optimized value for the field '{field}'."
        )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=CONSTANT_200,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

    """fill_missing_fields function."""


def fill_missing_fields(in_csv, out_csv, log_file):
    with (
        open(in_csv, newline="", encoding="utf-8") as infile,
        open(out_csv, "w", newline="", encoding="utf-8") as outfile,
        open(log_file, "w", encoding="utf-8") as logf,
    ):
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(
            tqdm(reader, desc="Filling missing fields", unit="row")
        ):
            context = {k: v for k, v in row.items() if v.strip()}
            # Fill missing analytic fields
            for field in ANALYSIS_FIELDS:
                if field in row and not row[field].strip():
                    filled = gpt_fill(context, field)
                    row[field] = filled
                    logf.write(f"Row {idx+2}, field '{field}' filled: {filled}\n")
                    context[field] = filled
            # Fill missing prompt columns
            for field in fieldnames:
                if field.startswith(PROMPT_PREFIX) and not row[field].strip():
                    style = field.replace(PROMPT_PREFIX, "")
                    filled = gpt_fill(context, field, style=style)
                    row[field] = filled
                    logf.write(f"Row {idx+2}, field '{field}' filled: {filled}\n")
            writer.writerow(row)
    logger.info(
        f"\n✅ All missing fields filled. Output: {out_csv}\nLog of filled fields: {log_file}"
    )


if __name__ == "__main__":
    fill_missing_fields(CSV_PATH, OUT_CSV, LOG_PATH)
