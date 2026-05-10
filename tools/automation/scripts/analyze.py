import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of analyze.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# Function to analyze the transcript using GPT
def analyze_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in narrative-driven image generation for DALL-E. Your goal is to analyze song transcripts to extract themes, emotions, key objects, and visual styles that will help create dynamic, vibrant images for visual storytelling.",
            },
            {
                "role": "user",
                "content": f"Analyze the following song transcript to extract: (1) main themes, (2) emotions, (3) key objects or characters for the images, (4) suggested lighting and color schemes, and (5) a recommended transition from one image to the next: {text}",
            },
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


try:
        import sys
        transcript_file = sys.argv[1]
        output_file = sys.argv[2]
        with open(transcript_file, "r") as f:
            transcript = f.read()
        analysis = analyze_text(transcript)
        with open(output_file, "w") as f:
            f.write(analysis)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)