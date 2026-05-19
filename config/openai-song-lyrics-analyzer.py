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
                            value = value.strip().strip('\'').strip("\'")
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

import os
from dotenv import load_dotenv
from openai import OpenAI


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Constants
CONSTANT_1050 = 1050


# Load environment variables from .env
# load_dotenv()  # Now using ~/.env.d/

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_text(text):
    """analyze_text function."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure you're using a chat model like gpt-3.5-turbo
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes song lyrics.",
            },
            {
                "role": "user",
                "content": f"Analyze the following song transcript and extract the main themes, emotions, and keywords: {text}",
            },
        ],
        max_tokens=CONSTANT_1050,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    import sys

    transcript_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(transcript_file, "r") as f:
        transcript = f.read()

    analysis = analyze_text(transcript)
    with open(output_file, "w") as f:
        f.write(analysis)
