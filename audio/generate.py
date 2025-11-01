"""
Main 24

This module provides functionality for main 24.

Author: Auto-generated
Date: 2025-11-01
"""

import csv

from generate_speech import generate_speech


def main():
    """main function."""

    csv_path = "/Users/steven/Music/quiz-talk/Gtrivia - Sheet1.csv"

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # Assuming 'Question' is the column name
            question_text = row["Question"]
            output_path = f"/ Users / steven / Music / quiz - talk / speech / question_{
                i + 1}.mp3"
            generate_speech(question_text, voice="shimmer", output_path=output_path)


if __name__ == "__main__":
    main()
