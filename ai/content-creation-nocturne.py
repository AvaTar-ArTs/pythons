"""
Content Creation Nocturne Groq 1

This module provides functionality for content creation nocturne groq 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2023 = 2023

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/groq.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/generation/groq.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(dotenv_path=os.path.expanduser("~/.env"))

XAI_API_KEY = os.getenv("XAI_API_KEY")
image_url = "https://science.nasa.gov/wp-content/uploads/CONSTANT_2023/09/web-first-images-release.png"

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "high",
                },
            },
            {
                "type": "text",
                "text": "What's in this image?",
            },
        ],
    },
]

completion = client.chat.completions.create(
    model="grok-2-vision-latest",
    messages=messages,
    temperature=0.01,
)
logger.info(completion.choices[0].message.content)
