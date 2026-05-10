import csv
import os

import requests
from pydub import AudioSegment

# Initialize the OpenAI client


def generate_speech(input_text, output_path, api_key):
    '\''
    Generates speech from text using an API (e.g., OpenAI's text-to-speech API).
    '\''
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


def calculate_text_duration(text, wpm=150):
    """
    Calculate the approximate duration of the text in seconds.
    """
    words = text.split()
    word_count = len(words)
    duration = word_count / (wpm / 60)  # Convert WPM to words per second
    return duration


def process_csv_and_generate_speech(csv_path, output_folder, api_key, total_duration):
    """
    Reads a CSV file, constructs speech text for each entry, and generates speech files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            question_text = row["Question"]
            options_text = ", ".join([f"{opt}: {row[opt]}" for opt in ["A", "B", "C"]])
            answer_text = row["Correct Answer"]

            # Construct the full text
            full_text = f"{question_text} Options are {options_text} The correct answer is {answer_text}."

            # Calculate the duration of the text
            text_duration = calculate_text_duration(full_text)

            # Calculate the additional time needed to reach the total duration
            additional_time = total_duration - text_duration

            # Distribute the additional time evenly across the breaks
            if additional_time > 0:
                num_breaks = 2  # Number of breaks in the SSML
                additional_break_time = additional_time / num_breaks
                additional_break_time_str = f"{additional_break_time:.1f}s"
            else:
                additional_break_time_str = "0s"

            # Using SSML to add pauses
            speech_text = f'\''
            <speak>
                {question_text}
                Options are {options_text}
                <break time='{additional_break_time_str}'/>
                The correct answer is {answer_text}.
                <break time='{additional_break_time_str}'/>
            </speak>
            '\''

            output_path = os.path.join(output_folder, f"question_{i + 1}.mp3")
            generate_speech(speech_text, output_path, api_key)

            # Ensure the final audio file duration is exactly total_duration
            # seconds
            audio = AudioSegment.from_file(output_path)
            audio_duration_ms = total_duration * 1000  # Convert seconds to milliseconds

            if len(audio) > audio_duration_ms:
                # Trim the audio if it's longer than the desired duration
                audio = audio[:audio_duration_ms]
            elif len(audio) < audio_duration_ms:
                # Pad the audio with silence if it's shorter than the desired
                # duration
                silence_duration = audio_duration_ms - len(audio)
                silence = AudioSegment.silent(duration=silence_duration)
                audio = audio + silence

            # Export the adjusted audio file
            audio.export(output_path, format="mp3")


if __name__ == "__main__":
    csv_path = input("Enter the path to the CSV file: ")
    output_folder = input("Enter the path to the output folder: ")
    api_key = "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"

    # Prompt for total duration
    total_duration = float(
        input("Enter the total duration for each audio file in seconds: ")
    )

    process_csv_and_generate_speech(csv_path, output_folder, api_key, total_duration)
