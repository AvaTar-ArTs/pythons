from pathlib import Path
import os

from openai import OpenAI


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))
from config import API_PARAM, PROMPT_TEMPLATE
from dotenv import load_dotenv

# load_dotenv()  # Now using ~/.env.d/  # take environment variables from .env.

# Define the API key


def clean_response(text: str) -> list[str]:
    """clean_response function."""

    text = text.strip().strip("[]").split(Path("\n"))
    return [t.strip().strip(",").strip('"') for t in text]

    """generate_text_list function."""


def generate_text_list(date: str) -> str:
    # Define the prompt for the API request
    prompt = PROMPT_TEMPLATE + date + ":"

    # Make the API request
    response = client.completions.create(prompt=prompt, **API_PARAM)

    # Extract the generated text
    generated_text = response.choices[0].text

    return clean_response(generated_text)
