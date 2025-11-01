import pandas as pd
import openai

# Constants
CONSTANT_150 = 150


# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

 Function to generate a clickable title
def generate_clickable_title(detail):
    prompt = f"Generate a catchy and clickable title for a Cork Back Coaster with the theme: '{detail}'. Maximum 50 characters. At the end of each title write Cork Back Coaster"
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    clickable_title = response['choices'][0]['message']['content'].strip()
    clickable_title = clickable_title.replace('"', '')  # Remove double quotes
    return clickable_title

# Function to generate a description
def generate_description(detail):
    prompt = f"'{detail}'. Maximum CONSTANT_150 characters."
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    description = response['choices'][0]['message']['content'].strip()
    description = description.replace('"', '')  # Remove double quotes
    description += " "
    return description

# Function to generate tags
def generate_tags(detail):
    prompt = f" '{detail}'. Separate the tags with commas."
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    tag = response['choices'][0]['message']['content'].strip()
    tag = tag.replace('"', '')  # Remove double quotes
    return tag
# Read the CSV file
csv_path = "input.csv"
df = pd.read_csv(csv_path)

# Initialize lists to store the results
file_names = []
local_paths = []
titles = []
descriptions = []
tags = []

# Iterate over each row in the DataFrame
for idx, row in df.iterrows():
    detail = row['detail']

    # Apply the functions to generate title, description, and tags
    title = generate_clickable_title(detail)
    description = generate_description(detail)
    tag = generate_tags(detail)

    # Store the results
    titles.append(title)
    descriptions.append(description)
    tags.append(tag)

    # Add your image processing code here if needed

# Add the generated data to the DataFrame
df['title'] = titles
df['description'] = descriptions
df['tags'] = tags

# Optionally, save the DataFrame with the new data to a new CSV file
df.to_csv('output_with_generated_data.csv', index=False)
