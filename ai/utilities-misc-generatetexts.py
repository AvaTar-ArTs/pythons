"""
Utilities Misc Generatetexts 3

This module provides functionality for utilities misc generatetexts 3.

Author: Auto-generated
Date: 2025-11-01
"""

import os
from pathlib import Path

# Constants
CONSTANT_150 = 150


# Load environment variables from ~/.env.d
def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if not key.startswith("source"):
                            os.environ[key] = value


load_env_d()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_facts(topic):
    """get_facts function."""

    response = client.completions.create(
        model="text-davinci-004",
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
