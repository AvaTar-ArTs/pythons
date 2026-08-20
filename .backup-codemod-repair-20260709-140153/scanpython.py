# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

from pathlib import Path
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


client = OpenAI(api_key=api_key)
import os

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please ensure it is set in your environment variables."
    )


def get_script_description(file_path):
    """get_script_description function."""

    with open(file_path, "r") as file:
        script_content = file.read()

    # OpenAI API call to get the script description
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert Python programmer."},
            {
                "role": "user",
                "content": f"Analyze the following Python script and describe its functionality:\n\n{script_content}",
            },
        ],
    )

    # Extract and return the description from the response
    description = response.choices[0].message.content.strip()
    return description

    """analyze_scripts function."""


def analyze_scripts(directory):
    descriptions = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(root, filename)
                description = get_script_description(file_path)
                descriptions[file_path] = description
    return descriptions


if __name__ == "__main__":
    # Update with your scripts directory
    scripts_directory = Path(str(Path.home()) + "/Documents/Python/")
    descriptions = analyze_scripts(scripts_directory)

    # Print out the descriptions
    for script, description in descriptions.items():
        logger.info(f"Script: {script}\nDescription: {description}\n{'-'*60}\n")
