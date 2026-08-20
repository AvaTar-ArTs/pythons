import os
import sys
import whisper
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_env_d

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

logger = logging.getLogger(__name__)


def transcribe_audio(model, file_path):
    """transcribe_audio function."""
    # Transcribe the audio file
    result = model.transcribe(file_path)
    return result["segments"]


def save_transcription(segments, output_file):
    with open(output_file, "w") as f:
        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")


def process_directory(model, source_directory):
    for root, _, files in os.walk(source_directory):
        for filename in files:
            if filename.lower().endswith(".mp3"):
                mp3_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]
                transcription_file = os.path.join(
                    root, f"{filename_no_ext}_transcription.txt"
                )

                # Transcribe the MP3
                segments = transcribe_audio(model, mp3_file)

                # Save the transcription
                save_transcription(segments, transcription_file)
                logger.info(f"Transcription saved to {transcription_file}")


def main():
    source_directory = input("Enter the path to the source directory: ")
    if not os.path.isdir(source_directory):
        logger.error(f"Invalid directory: {source_directory}")
        return
    model = whisper.load_model("base")
    process_directory(model, source_directory)


if __name__ == "__main__":
    main()
