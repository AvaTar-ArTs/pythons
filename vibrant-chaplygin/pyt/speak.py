import csv

import openai

import logging

logger = logging.getLogger(__name__)


# Initialize the OpenAI client
client = openai()


def generate_speech(
    text, pause_duration="5s", voice="shimmer", output_path="speech.mp3"
):
    # Adding a pause using the SSML <break> tag
    # Assuming that 'text' contains something like "Option 3: <your text>"
    # and you want to insert a pause right after this before continuing with the answer
    modified_text = text.replace("Option 3:", f'Option 3:"/>')

    response = OpenAI.Audio.create(
        model="tts-1-hd",  # Ensure this model supports the audio creation
        input=modified_text,
        voice=voice,
        format="mp3",
        ssml=True,  # Indicate that the input text contains SSML
    )
    with open(output_path, "wb") as file:
        file.write(response.content)
def main():
    csv_path = "input.csv"  # Update this path to where your CSV is located

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            question_text = row["Question"]  # Assuming 'Question' is the column name
            output_path = (
                fstr(Path.home()) + "/Documents/quiz-talk/quiz329/question/question_{i+1}.mp3"
            )
            logger.info(f"Generating speech for question {i+1}")  # Feedback to user
            generate_speech(
                question_text,
                pause_duration="5s",
                voice="shimmer",
                output_path=output_path)
            print(
                f"Generated speech for question {i+1} at {output_path}"
            )  # Success message


if __name__ == "__main__":
    main()
