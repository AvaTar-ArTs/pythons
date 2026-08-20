import csv
import os

import requests  # Make sure to install this package


def generate_speech(input_text, output_path, api_key):
    """
    Generates speech from text using an API (e.g., OpenAI's text-to-speech API).
    """
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "tts-1",  # Update this according to the specific model you're using
        "input": input_text,
        "voice": "shimmer",  # Update the voice parameter as needed
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Generated speech saved to {output_path}")
    else:
        print("Failed to generate speech:", response.text)


def process_csv_and_generate_speech(csv_path, output_folder, api_key):
    """
    Reads a CSV file, constructs speech text for each entry, and generates speech files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            question_text = row["Question"]
            options_text = ", ".join(
                [f"{opt}: {row[f'Option {opt}']}" for opt in ["A", "B", "C"]]
            )
            answer_text = row["Answer"]  # Define answer_text here

            # Using SSML to add pauses
            speech_text = f"""
            <speak>
                {question_text}
                <break time='3s'/>
                Options are {options_text}
                <break time='5s'/>
                The correct answer is {answer_text}.
            </speak>
            """

            # These lines should be inside the loop
            output_path = os.path.join(output_folder, f"question_{i + 1}.mp3")
            generate_speech(speech_text, output_path, api_key)


if __name__ == "__main__":
    # Update to your actual file path
    csv_path = (
        "/Users/steven/Documents/project2025/scripts/Project 2025 Quiz - ReSiSt.csv"
    )
    # Specify your output folder path
    output_folder = "/Users/steven/Documents/project2025/Quiz"
    # Replace with your actual OpenAI API key
    api_key = "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"
    process_csv_and_generate_speech(csv_path, output_folder, api_key)
