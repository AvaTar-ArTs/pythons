from pathlib import Path
import csv
import os
import sys

from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_2000 = 2000


# BASE_DIR = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/mp3")
# CSV_OUTPUT = os.path.join(BASE_DIR, "final_song_data.csv")


def extract_duration_from_transcript(transcript_text):
    lines = transcript_text.strip().split(Path("\n"))
    last_line = lines[-1] if lines else ""
    if "--" in last_line:
        time_range = last_line.split("--")[-1].split(":")
        minutes = int(time_range[0].strip())
        seconds = int(time_range[1].strip().split()[0])
        return f"{minutes}:{str(seconds).zfill(2)}"
    return "0:00"
def get_all_song_data(base_dir):
    song_data = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        song_title = folder_name
        mp3_path = os.path.join(folder_path, f"{folder_name}.mp3")
        transcript_path = os.path.join(folder_path, f"{folder_name}_transcript.txt")
        analysis_path = os.path.join(folder_path, f"{folder_name}_analysis.txt")

        transcript_content = read_file_content(transcript_path)
        analysis_content = read_file_content(analysis_path)

        duration = extract_duration_from_transcript(transcript_content)
        lyrics = transcript_content.replace(Path("\n"), " ")
        keys = "Emotional Journey"
        genre = (
            "indie-folk reflective acoustic" if "folk" in analysis_content.lower() else "unknown"
        )

        song_data.append(
            {
                "Song Title": song_title,
                "MP3 File Path": mp3_path,
                "Transcript File": transcript_path,
                "Analysis File": analysis_path,
                "Transcript Content": transcript_content,
                "Analysis Content": analysis_content,
                "Time": duration,
                "Keys": keys,
                "Genre": genre,
                "Lyrics": lyrics,
            }
        )

    return song_data
def read_file_content(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
def write_to_csv(data, csv_path):
    if not data:
        logger.info("No data found to write.")
        return

    headers = list(data[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    logger.info(f"\n🥁 CSV saved to: {csv_path}")


if __name__ == "__main__":
    song_data = get_all_song_data(BASE_DIR)
    write_to_csv(song_data, CSV_OUTPUT)

load_dotenv(dotenv_path=Path(str(Path.home()) + "/.env"))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("❌ OpenAI API key not found. Please check your .env file.")
client = OpenAI(api_key=api_key)


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript_data = client.audio.transcribe(
            model="whisper-1", file=audio_file, response_format="verbose_json"
        )

    transcript_with_timestamps = []
    for segment in transcript_data.segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        transcript_with_timestamps.append(
            f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
        )

    return Path("\n").join(transcript_with_timestamps)


def analyze_text_for_section(transcript, section_number=1):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert multimedia analyst and storyteller. Your role is to deliver comprehensive, insightful, and "
                        "emotionally intelligent evaluations of audio-visual content. Your analyses should cover thematic depth, emotional tone, "
                        "narrative structure, artistic expression, technical execution, and audience engagement. Use vivid, descriptive language "
                        "and reference specific moments when necessary."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Please provide a thorough analysis of section {section_number} of the following transcript. Provide a comprehensive analysis covering Break down key elements with depth and clarity:\n\n"
                        "### 1. Central Themes and Messages\n"
                        "- Identify and interpret the primary themes.\n"
                        "- Are there any hidden or layered meanings?\n\n"
                        "### 2. Emotional Tone\n"
                        "- Describe the mood and emotional shifts.\n"
                        "- How do sound, rhythm, or possible visuals contribute to the emotion?\n\n"
                        "### 3. Narrative Arc and Structure\n"
                        "- How does this section move the story forward?\n"
                        "- Mention key transitions or turning points.\n\n"
                        "### 4. Creator’s Intent and Vision\n"
                        "- What might the creator be trying to say or express?\n"
                        "- How do multimedia elements (e.g., sound, visuals, pacing) support this vision?\n\n"
                        "### 5. Technical and Artistic Elements\n"
                        "- Comment on production techniques: editing, sound design, transitions, or special effects.\n"
                        "- How do these enhance storytelling?\n\n"
                        "### 6. Audience Impact and Engagement\n"
                        "- How effectively does it capture and maintain attention?\n"
                        "- What makes this portion memorable or emotionally resonant?\n\n"
                        f"### Transcript\n{transcript}"
                    ),
                },
            ],
            max_tokens=CONSTANT_2000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.info(f"Error analyzing text: {e}")
        return None


def process_audio_file(file_path, csv_data):
    base_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    song_dir = os.path.join(base_dir, file_name_no_ext)

    os.makedirs(song_dir, exist_ok=True)

    logger.info(f"🎼 Transcribing {file_name}...")
    transcript = transcribe_audio(file_path)
    transcript_path = os.path.join(song_dir, f"{file_name_no_ext}_transcript.txt")
    with open(transcript_path, "w") as f:
        f.write(transcript)
    logger.info(f"✅ Transcript saved: {transcript_path}")

    logger.info(f"🎭 Analyzing {file_name}...")
    analysis = analyze_text_for_section(transcript, file_name_no_ext)
    analysis_path = os.path.join(song_dir, f"{file_name_no_ext}_analysis.txt")
    with open(analysis_path, "w") as f:
        f.write(analysis)
    logger.info(f"✅ Analysis saved: {analysis_path}")

    csv_data.append(
        [
            file_name_no_ext,
            file_path,
            transcript_path,
            analysis_path,
            transcript,
            analysis,
        ]
    )


def process_audio_directory():
    audio_dir = input("Enter the directory containing MP3 files: ").strip()

    if not os.path.isdir(audio_dir):
        logger.info(f"❌ Invalid directory: {audio_dir}")
        sys.exit(1)

    logger.info(f"🔍 Scanning directory {audio_dir} for audio files...")
    csv_data = [
        [
            "Song Title",
            "MP3 File Path",
            "Transcript File",
            "Analysis File",
            "Transcript Content",
            "Analysis Content",
        ]
    ]

    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                logger.info(f"🎵 Found audio file: {file_path}")
                process_audio_file(file_path, csv_data)

    csv_path = os.path.join(audio_dir, Path(str(Path.home()) + "/Music/nocTurneMeLoDieS/mp4/song_data.csv"))
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    logger.info(f"📜 CSV file saved: {csv_path}")


if __name__ == "__main__":
    process_audio_directory()
