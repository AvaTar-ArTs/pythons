"""
Quiz Tts

This module provides functionality for quiz tts.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Function to read the CSV file and generate trivia quiz questions
def generate_trivia_quiz(csv_path):
    """generate_trivia_quiz function."""

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract question and options from the row
        question = row["Question"]
        options = [row["Option1"], row["Option2"], row["Option3"], row["Option4"]]

        # Print the question
        logger.info(f"Question {index + 1}: {question}")

        # Print the options
        for i, option in enumerate(options):
            logger.info(f"{i + 1}. {option}")

        # Ask the user for the correct answer
        correct_answer = input("Enter the correct option number: ")

        # Validate the user input and provide feedback
        correct_option = chr(ord("A") + options.index(row["CorrectOption"]))
        if correct_answer.upper() == correct_option:
            logger.info("Correct!")
        else:
            logger.info(f"Wrong! The correct answer is: {correct_option}")


# Path to the CSV file
csv_path = Path(str(Path.home()) + "/Documents/trivia/Gtrivia.csv")

# Generate the trivia quiz
generate_trivia_quiz(csv_path)
