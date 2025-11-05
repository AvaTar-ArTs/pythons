from pathlib import Path
import os
import subprocess
import logging
from openai import OpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Constants
CONSTANT_300 = 300
CONSTANT_1000 = 1000


# Configure logging
logging.basicConfig(
    filename="video_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load environment variables
load_dotenv(dotenv_path=Path(str(Path.home()) + "/.env"))

# Directory paths
VIDEO_DIR = Path(str(Path.home()) + "/Movies/project2025/Media/")
TRANSCRIPT_DIR = Path(str(Path.home()) + "/Movies/project2025/Media/")
ANALYSIS_DIR = Path(str(Path.home()) + "/Movies/project2025/Media/")

# Create output directories if they don't exist.
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error(
        "OpenAI API key not found. Ensure it is correctly set in the environment."
    )
    raise ValueError("OpenAI API key not found.")

client = OpenAI(api_key=api_key)


# Split video into smaller segments
def split_video_to_segments(video_path, segment_length=CONSTANT_300):
    """Split the video into smaller segments."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(VIDEO_DIR, video_name + "_segments")
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-c",
        "copy",
        "-map",
        "0",
        "-segment_time",
        str(segment_length),
        "-f",
        "segment",
        "-reset_timestamps",
        "1",
        os.path.join(output_dir, video_name + "_%03d.mp4"),
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"Video {video_name} split into segments successfully.")
    except subprocess.CalledProcessError as error:
        logging.error(f"Error splitting video {video_name}: {error}")
        return []

    segments = sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".mp4")
        ]
    )
    return segments


# Transcribe video segments using Whisper
def transcribe_video_segment(file_path):
    """transcribe_video_segment function."""

    try:
        with open(file_path, "rb") as video_file:
            transcript_data = client.audio.transcribe(
                "whisper-1", video_file, response_format="verbose_json"
            )

        transcript_with_timestamps = [
            f"{format_timestamp(seg['start'])} -- {format_timestamp(seg['end'])}: {seg['text']}"
            for seg in transcript_data["segments"]
        ]

        return Path("\n").join(transcript_with_timestamps)
    except Exception as e:
        logging.error(f"Error transcribing video segment {file_path}: {e}")
        return ""

    # Format timestamps
    """format_timestamp function."""


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    """analyze_text_for_section function."""


# Analyze text using OpenAI API
def analyze_text_for_section(text, section_number):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers ",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following song transcript to extract: (1) main themeAnalyze the following transcript and associated content for {text}. Provide a comprehensive analysis covering:1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed. How do they connect to the broader narrative?2. **Emotional Tone**: What emotions are evoked, and how are they conveyed through the combination of audio and visuals? 3. **Narrative Arc**: Describe how this section contributes to the overall story or progression. Are there key turning points or developments?\n4. **Creator’s Intent**: What is the likely purpose or message the creator is trying to communicate? Is it to entertain, inform, inspire, or persuade?\n5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable metaphors, symbols, or visual/audio motifs that enhance the narrative or emotional impact.\n6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. How do they contribute to the overall experience?\n7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. Are there any standout moments?\n8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. How well does it resonate with its intended audience?\n9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\nTranscript:\n{text}",
                },
            ],
            max_tokens=CONSTANT_1000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error in analysis for Section {section_number}: {e}")
        return ""

    """process_video_by_section function."""


# Process video by sections
def process_video_by_section(video_file, segment_length=CONSTANT_300):
    segments = split_video_to_segments(video_file, segment_length)
    if not segments:
        return

    with ThreadPoolExecutor(max_workers=4) as executor:
        for index, segment in enumerate(segments):
            executor.submit(process_segment, segment, index + 1)
    """process_segment function."""


# Process each segment
def process_segment(segment, section_number):
    logging.info(f"Processing Section {section_number}: {segment}")
    transcript = transcribe_video_segment(segment)
    if transcript:
        transcript_file_path = os.path.join(
            TRANSCRIPT_DIR, f"section_{section_number}_transcript.txt"
        )
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        logging.info(
            f"Transcription saved for Section {section_number} at {transcript_file_path}"
        )

        analysis = analyze_text_for_section(transcript, section_number)
        if analysis:
            analysis_file_path = os.path.join(
                ANALYSIS_DIR, f"section_{section_number}_analysis.txt"
            )
            with open(analysis_file_path, "w") as f:
                f.write(analysis)
            logging.info(
                f"Analysis saved for Section {section_number} at {analysis_file_path}"
            )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        logging.error("Path to the MP4 file not provided.")
        sys.exit("Usage: python script.py <path_to_video_file>")

    video_file = sys.argv[1]
    process_video_by_section(video_file, segment_length=CONSTANT_300)
