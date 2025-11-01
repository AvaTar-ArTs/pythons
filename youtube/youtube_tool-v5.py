import csv
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_150 = 150
CONSTANT_300 = 300



# Initialize the OpenAI client
client = OpenAI()

def generate_base_prompt(question, options):
    # Combine question and options to generate a base prompt
    return f"Question: {question} Options: {', '.join(options)}"

def refine_prompt(prompt):
    # Refine the prompt using ChatGPT for more creativity
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a creative writer."},
                  {"role": "user", "content": prompt}],
        max_tokens=CONSTANT_150
    )
    return response.choices[0].message.content.strip()
    else:
        return "No response generated."

def create_image(prompt):
    # Generate an image using the refined prompt with DALL·E
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

def upscale_image(image_url):
    # Download and upscale the image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    new_size = (img.width * 2, img.height * 2)
    
     #Use LANCZOS resampling for better quality
    upscaled_img = img.resize(new_size, ImageResampling.LANCZOS)
    
    # Define the output path
    output_path = Path("upscaled_image.png")
    
    # Save the upscaled image
    upscaled_img.save(output_path, dpi=(CONSTANT_300, CONSTANT_300))
    
    # Return the path as a string
    return output_path.as_posix()
    
def text_to_speech(text):
    # Placeholder function for text-to-speech conversion
    return "audio_file_path_placeholder"

# Process the CSV
input_file = 'input.csv'
output_file = 'output.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Refined Prompt', 'Image URL', 'Upscaled Image Path', 'Question Audio', 'Option A Audio', 'Option B Audio', 'Option C Audio', 'Answer Audio']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        base_prompt = generate_base_prompt(row['Question'], [row['A'], row['B'], row['C']])
        refined_prompt = refine_prompt(base_prompt)
        image_url = create_image(refined_prompt)
        upscaled_image_path = upscale_image(image_url)
        
        row.update({
            'Refined Prompt': refined_prompt,
            'Image URL': image_url,
            'Upscaled Image Path': upscaled_image_path,
            'Question Audio': text_to_speech(row['Question']),
            'Option A Audio': text_to_speech(row['A']),
            'Option B Audio': text_to_speech(row['B']),
            'Option C Audio': text_to_speech(row['C']),
            'Answer Audio': text_to_speech(row['Answer']),
        })

        writer.writerow(row)

logger.info("Workflow completed.")
