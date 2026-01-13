import csv

from openai import OpenAI

client = OpenAI(api_key="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")

# Replace 'your_api_key_here' with your actual OpenAI API key


def generate_speech(text, voice="shimmer", output_path="speech.mp3"):
    response = client.audio.create(
        model="text-davinci-003",  # Ensure this model supports the audio creation
        input=text,
        voice=voice,
        format="mp3",
    )
    with open(output_path, "wb") as file:
        file.write(response.content)


def main():
    # Update this path to where your CSV is located
    csv_path = "/Users/steven/Music/quiz-talk/Gtrivia - Sheet1.csv"

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # Assuming 'Question' is the column name
            question_text = row["Question"]
            output_path = f"./speech/question_{i + 1}.mp3"
            print(
                f"Generating speech for question {
                    i + 1}"
            )  # Feedback to user
            generate_speech(question_text, voice="shimmer", output_path=output_path)
            print(
                f"Generated speech for question {
                    i + 1} at {output_path}"
            )  # Success message


if __name__ == "__main__":
    main()
