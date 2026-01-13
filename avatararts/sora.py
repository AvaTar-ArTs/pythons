import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.Video.create(
    model="sora",
    prompt="A futuristic cityscape with flying cars",
    duration=60  # Duration in seconds
)

print(response['video_url'])
