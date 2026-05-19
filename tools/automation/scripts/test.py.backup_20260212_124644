import csv

from openai import OpenAI

client = OpenAI()
# Set the API key directly on the openai module
OpenAI.api_key = "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"


def generate_speech(text, voice, output_path):
    try:
        # Ensure your text uses SSML for the pause
        response = client.audio.speech.create(
            model="tts-1", input=text, voice=voice, format="mp3"
        )
        with open(output_path, "wb") as file:
            file.write(response.content)
    except AttributeError:
        print(
            "The Audio attribute is not recognized. Check if your OpenAI client supports the Audio API."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    csv_path = "input.csv"  # Ensure this path points to your CSV file

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # Modify this line to build your SSML string with pauses
            # Example; adjust as needed
            question_text = f"{row['Question']}<break time='5s'/>"
            output_path = f"./question_{i + 1}.mp3"
            print(f"Generating speech for question {i + 1}")
            generate_speech(question_text, "shimmer", output_path)
            print(f"Generated speech for question {i + 1} at {output_path}")


if __name__ == "__main__":
    main()
