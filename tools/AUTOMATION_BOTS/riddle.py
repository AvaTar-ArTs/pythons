import csv
import logging
import os
from pathlib import Path
from pathlib import Path as PathLib

from dotenv import load_dotenv

from openai import OpenAI


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            line = line.removeprefix("export ")
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass


logger = logging.getLogger(__name__)


# Constants
CONSTANT_150 = 150


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up OpenAI API key


def fetch_riddles(number_of_riddles=3):
    """Function."""
    prompt_text = "Generate a sphinx riddle with a question, an answer, a correct response message, and an incorrect response message."
    messages = [
        {
            "role": "system",
            "content": "You are about to generate a series of sphinx riddles.",
        },
        {"role": "user", "content": prompt_text * number_of_riddles},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=CONSTANT_150 * number_of_riddles,
            n=1,
            stop=None,
        )
    except Exception as e:
        logger.info(f"Error fetching riddles: {e!s}")
        return []

    riddle_texts = response.choices[0].message.content.strip().split(Path("\n\n"))
    riddles = [
        dict(
            zip(
                ["query", "answer", "correct_response", "incorrect_response"],
                riddle_text.strip().split(Path("\n")),
            ),
        )
        for riddle_text in riddle_texts
        if len(riddle_text.strip().split(Path("\n"))) == 4
    ]
    return riddles[:number_of_riddles]


game_log = []


def play_dynamic_game_with_choices():
    try:
        number_of_riddles = int(input("How many riddles do you want to play with? "))
    except ValueError:
        logger.info("Please enter a valid number.")
        return

    riddles = fetch_riddles(number_of_riddles)
    if not riddles:
        return

    for idx, riddle in enumerate(riddles, start=1):
        logger.info(f"{idx}. {riddle['query']}")
        user_answer = input("Your answer: ").strip().lower()

        if user_answer == riddle["answer"]:
            logger.info(riddle["correct_response"])
            result = "Correct"
        else:
            logger.info(riddle["incorrect_response"])
            result = "Incorrect"

        game_log.append(
            {
                "riddle_question": riddle["query"],
                "user_answer": user_answer,
                "correct_answer": riddle["answer"],
                "result": result,
            },
        )


def output_to_csv(logs, filename="riddle_game_log.csv"):
    if logs:
        keys = logs[0].keys()
        with open(filename, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(logs)
        logger.info(f"Game log saved to {filename}")


if __name__ == "__main__":
    logger.info("\nSphinx: 'Ah, traveler! Solve my riddles, or be devoured by me.'\n")
    play_dynamic_game_with_choices()
    output_to_csv(game_log)
