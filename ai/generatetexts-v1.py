"""
Generatetexts

This module provides functionality for generatetexts.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
from openai import OpenAI

# Constants
CONSTANT_150 = 150


client = OpenAI(api_key="[[Insert openai api key]]")


def get_facts(topic):
    """get_facts function."""

    response = client.completions.create(
        model="text-davinci-003",
        prompt="Create three tik-tok like plain text for curious facts about "
        + topic
        + " separated by enters without text before or after",
        temperature=0.5,
        max_tokens=CONSTANT_150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    facts = response.choices[0].text.strip().split(Path("\n"))
    return facts
