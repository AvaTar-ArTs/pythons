import os
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

from openai import OpenAI

client = OpenAI(api_key=YOUR_OPENAI_API_KEY)
import logging

from utilities.const import GPT_MODEL

# Configure OpenAI API

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("rephraser.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Rephrase:
    logger.info("Inside class Rephrase")

    def __init__(self, content):
        """__init__ function."""

        self.content = content

        """rephrase_with_gpt function."""

    def rephrase_with_gpt(self):
        prompt = (
            f'Rephrase the following sentence:\n"{self.content}"\n\nRewritten Sentence:'
        )
        response = client.completions.create(
            engine=GPT_MODEL,
            prompt=prompt,
            max_tokens=64,
            temperature=0.6,
            n=1,
            stop=None,
        )
        rephrased_sentence = response.choices[0].text.strip()
        return rephrased_sentence
        """rephrase_sentence function."""

    def rephrase_sentence(self):
        logger.info(f"Received sentence: {self.content}")
        rephrased_sentence = self.rephrase_with_gpt()
        logger.info(f"Rephrased sentence: {rephrased_sentence}")
        return rephrased_sentence


# rephrase = Rephrase(content)
# rephrase_response = rephrase.rephrase_sentence()
# json_obj = {"title": title, "content": rephrase_response}
