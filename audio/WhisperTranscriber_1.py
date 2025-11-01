"""
Whispertranscriber 1

This module provides functionality for whispertranscriber 1.

Author: Auto-generated
Date: 2025-11-01
"""

# WhisperTranscriber
# src: https://github.com/VimWei/WhisperTranscriber
# Implement Whisper's basic parameter configuration
# Implement parameter control of srt output, so that verbatim srt can be achieved
# max_line_width，max_line_count，max_words_per_line
# Realize free switching of srt line breaking control: manual or automatic

import json
from pathlib import Path

import the
import whisper
import yaml

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000
CONSTANT_60000 = 60000
CONSTANT_3600000 = 3600000



def load_config(config_file="config.yaml"):
    """Load configuration file"""
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_media_files(config):
    """Get the list of media files to be processed"""
    input_dir = config["input"]["directory"]
    formats = config["input"]["formats"]
    specific_files = config["input"]["specific_files"]

    # Make sure the input directory exists
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        logger.info(f"Created input directory: {input_dir}")
        return []

    # If specific files are specified, only those files will be processed
    if specific_files:
        return [
            os.path.join(input_dir, f)
            for f in specific_files
            if os.path.exists(os.path.join(input_dir, f))
        ]

    # Otherwise process all supported formats in the directory
    media_files = []
    for format in formats:
        media_files.extend(str(p) for p in Path(input_dir).glob(f"*{format}"))

    return sorted(media_files)


def transcribe_audio(config_file="config.yaml"):
    """Use the configuration file's transcription function"""
    # Load configuration
    config = load_config(config_file)

    # Get the media file to be processed
    media_files = get_media_files(config)

    if not media_files:
        logger.info(f"No media files found in {config['input']['directory']}")
        logger.info(f"Supported formats: {', '.join(config['input']['formats'])}")
        return

    logger.info(f"Found {len(media_files)} files to process:")
    for file in media_files:
        logger.info(f"  - {os.path.basename(file)}")
    print()

    # Load the model
    model = whisper.load_model(
        config["model"]["name"], device=config["model"]["device"]
    )

    for audio in media_files:
        logger.info(f"Processing: {os.path.basename(audio)}")
        # Get the file name (remove the extension)
        base_name = os.path.splitext(os.path.basename(audio))[0]

        # Using the transcribe function
        result = model.transcribe(
            audio,
            language=config["transcription"]["language"],
            task=config["transcription"]["task"],
            temperature=config["transcription"]["temperature"],
            best_of=config["transcription"]["best_of"],
            beam_size=config["transcription"]["beam_size"],
            patience=config["transcription"]["patience"],
            length_penalty=config["transcription"]["length_penalty"],
            suppress_tokens=config["transcription"]["suppress_tokens"],
            initial_prompt=config["transcription"]["initial_prompt"],
            condition_on_previous_text=config["transcription"][
                "condition_on_previous_text"
            ],
            fp16=config["model"]["fp16"],
            word_timestamps=config["transcription"]["word_timestamps"],
            verbose=config["output"]["verbose"],
        )

        # Processing output
        formats = (
            config["output"]["format"]
            if config["output"]["format"] != "all"
            else ["txt", "vtt", "srt", "json"]
        )

        for fmt in formats:
            output_file = os.path.join(
                config["output"]["directory"], f"{base_name}.{fmt}"
            )
            if fmt == "txt":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["text"])
            elif fmt == "srt":
                # Manually process SRT output
                with open(output_file, "w", encoding="utf-8") as f:
                    if config["srt"]["use_default_line_breaks"]:
                        write_srt_with_default_line_breaks(result, f)
                    else:
                        write_srt_with_word_timestamps(
                            result,
                            f,
                            config["srt"]["max_line_width"],
                            config["srt"]["max_line_count"],
                            config["srt"]["max_words_per_line"],
                        )
            elif fmt == "vtt":
                with open(output_file, "w", encoding="utf-8") as f:
                    writer = whisper.utils.WriteVTT(config["output"]["directory"])
                    writer.write_result(result, f)
            elif fmt == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        if config["output"]["verbose"]:
            print(
                f"Transcription complete for {audio}. Output saved to {config['output']['directory']}"
            )


def write_srt_with_word_timestamps(
    """write_srt_with_word_timestamps function."""

    result, file, max_line_width=None, max_line_count=None, max_words_per_line=None
):
    # Initialize variables
    line_index = 1
    current_line = ""
    current_line_start = None
    current_line_end = None
    words_in_line = 0

    for segment in result["segments"]:
        for word in segment["words"]:
            # Check if line break is needed
            if (
                (
                    max_line_width
                    and len(current_line) + len(word["word"]) + 1 > max_line_width
                )
                or (max_words_per_line and words_in_line >= max_words_per_line)
                or (max_line_count and line_index >= max_line_count)
            ):
                # Write the current line
                if current_line_start is not None and current_line_end is not None:
                    print(
                        f"{line_index}\n{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n{current_line.strip()}\n",
                        file=file,
                    )
                # Reset the current line
                line_index += 1
                current_line = ""
                current_line_start = None
                current_line_end = None
                words_in_line = 0

            # Update the start and end times of the row
            if current_line_start is None:
                current_line_start = word["start"]
            current_line_end = word["end"]

            # Append words
            current_line += word["word"] + " "
            words_in_line += 1

    # Write the last line
    if current_line:
        if current_line_start is not None and current_line_end is not None:
            print(
                f"{line_index}\n{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n{current_line.strip()}\n",
                file=file,
            )


    """write_srt_with_default_line_breaks function."""

def write_srt_with_default_line_breaks(result, file):
    for segment in result["segments"]:
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip().replace("-->", "->")
        logger.info(f"{segment['id']}\n{start} --> {end}\n{text}\n", file=file)

    """format_timestamp function."""


def format_timestamp(seconds: float):
    milliseconds = int(seconds * CONSTANT_1000)
    hours = milliseconds // CONSTANT_3600000
    minutes = (milliseconds % CONSTANT_3600000) // CONSTANT_60000
    seconds = (milliseconds % CONSTANT_60000) // CONSTANT_1000
    milliseconds = milliseconds % CONSTANT_1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


if __name__ == "__main__":
    transcribe_audio()
