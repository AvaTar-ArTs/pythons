import os

from config import API_PARAM, PROMPT_TEMPLATE
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

load_dotenv()  # Load environment variables from .env.

# Define the API key


def clean_response(text: str) -> list[str]:
    text = text.strip().strip("[]").split("\n")
    return [t.strip().strip(",").strip('"') for t in text]


def generate_text_list(date: str) -> str:
    # Define the prompt for the API request
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": PROMPT_TEMPLATE + date + ":"},
    ]

    # Make the API request using the chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-4-1106-preview", messages=conversation, **API_PARAM
    )

    # Extract the generated text
    generated_text = response["choices"][0]["message"]["content"]

    return clean_response(generated_text)
