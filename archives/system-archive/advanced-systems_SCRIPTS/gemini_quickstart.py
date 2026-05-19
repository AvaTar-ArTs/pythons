import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""Quickstart script for interacting with Google Gemini models."""

from __future__ import annotations

import os
import sys

import google.generativeai as genai


def main() -> int:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        msg = (
            "GOOGLE_API_KEY environment variable is not set. "
            "Sign in to Google AI Studio (https://aistudio.google.com), "
            "create an API key, then export it before running this script.\n"
            "Example:\n"
            "  export GOOGLE_API_KEY='your-key-here'\n"
        )
        print(msg, file=sys.stderr)
        return 1

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = "Give me a three bullet summary of why Gemini is useful for developers."
    response = model.generate_content(prompt)

    print("Prompt: ", prompt)
    print("\nGemini response:\n")
    print(response.text.strip())
    return 0


try:
        raise SystemExit(main())
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)