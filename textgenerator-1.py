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
import os

from dotenv import load_dotenv
from openai import OpenAI

from config import API_PARAM, PROMPT_TEMPLATE


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Constants
CONSTANT_1106 = 1106


client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# load_dotenv()  # Now using ~/.env.d/  # Load environment variables from .env.

# Define the API key


def clean_response(text: str) -> list[str]:
    """clean_response function."""

    text = text.strip().strip("[]").split(Path("\n"))
    return [t.strip().strip(",").strip('"') for t in text]

    """generate_text_list function."""


def generate_text_list(date: str) -> str:
    # Define the prompt for the API request
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": PROMPT_TEMPLATE + date + ":"},
    ]

    # Make the API request using the chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-4-CONSTANT_1106-preview", messages=conversation, **API_PARAM
    )

    # Extract the generated text
    generated_text = response["choices"][0]["message"]["content"]

    return clean_response(generated_text)
