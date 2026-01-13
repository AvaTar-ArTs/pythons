from pathlib import Path
import os

import cv2
import pytesseract

import logging

logger = logging.getLogger(__name__)


# If you encounter issues with pytesseract finding Tesseract-OCR, specify the path as shown below
# pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'  # Update this path if necessary


def extract_text_from_video(video_path, output_file):
    """
    Extracts text from the given video file using OCR and saves the text to an output file.

    Args:
    video_path (str): The path to the video file.
    output_file (file): An open file object to write the extracted text.
    """
    cap = cv2.VideoCapture(video_path)
    frameRate = cap.get(5)  # frame rate

    while cap.isOpened():
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if not ret:
            break
        if frameId % (int(frameRate) * 1) == 0:  # Extract a frame every second
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, lang="eng")
            if text.strip() != "":  # Check if extracted text is not empty
                output_file.write(f"Extracted Text from Frame {frameId}:\n{text}\n\n")

    cap.release()


def process_videos_in_folder(folder_path, output_path):
    """
    Processes each video in the specified folder, extracting text and saving it to an output file.

    Args:
    folder_path (str): The path to the folder containing video files.
    output_path (str): The path to the output file where extracted texts will be saved.
    """
    with open(output_path, "w") as output_file:
        for video_name in os.listdir(folder_path):
            if video_name.endswith(
                (".mp4", ".avi", ".mov", ".webm")
            ):  # Include .webm in the list
                video_path = os.path.join(folder_path, video_name)
                logger.info(f"Processing {video_name}...")
                extract_text_from_video(video_path, output_file)


if __name__ == "__main__":
    folder_path = Path(
        str(Path.home()) + "/Movies/CoH-Grab"
    )  # Hardcoded path to your video folder
    output_path = input(
        "Enter the path for the output text file: "
    )  # Ask user for output file path
    process_videos_in_folder(folder_path, output_path)
    logger.info(f"Text extraction completed. Check the output file at {output_path}")
