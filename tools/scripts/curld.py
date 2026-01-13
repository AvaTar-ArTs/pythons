import csv
import json
import os  # Import the os module
import subprocess


def generate_speech_curl(input_text, output_path, api_key):
    data = {"model": "tts-1", "input": input_text, "voice": "shimmer"}
    command = [
        "curl",
        "https://api.openai.com/v1/audio/speech",
        "-H",
        f"Authorization: Bearer {api_key}",
        "-H",
        "Content-Type: application/json",
        "-d",
        json.dumps(data),
        "--output",
        output_path,
    ]
    subprocess.run(command, check=True)


def main(csv_path, api_key, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            question_text = row["Question"]
            options_text = " ".join(
                [f"Option {n}: {row[f'Option {n}']}" for n in range(1, 4)]
            )
            correct_answer = f"Correct Answer: {row['Correct Answer']}"
            input_text = f"{question_text} {options_text} {correct_answer}"

            # Update output_path to include the output_folder
            output_path = os.path.join(output_folder, f"question_{i + 1}.mp3")
            print(f"Generating speech for question {i + 1}")
            generate_speech_curl(input_text, output_path, api_key)


if __name__ == "__main__":
    # Update to your CSV file path
    csv_path = "/Users/steven/Music/quiz-talk/Gtrivia - Sheet1.csv"
    # Replace with your OpenAI API key
    api_key = "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"
    # Specify your output folder path here
    output_folder = "/Users/steven/Music/quiz-talk/speech"
    main(csv_path, api_key, output_folder)
