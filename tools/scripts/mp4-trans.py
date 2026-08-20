from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os
import subprocess

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Directory paths
VIDEO_DIR = "/Users/steven/Movies/Kath/Katheria_and_Salome_The_Daughters_of_Destinay-30m_compressed_segments"  # Directory containing MP4 files
TRANSCRIPT_DIR = "/Users/steven/Movies/Kath/Katheria_and_Salome_The_Daughters_of_Destinay-30m_compressed_segments/transcribe"  # Directory to save transcripts
ANALYSIS_DIR = (
    "/Users/steven/Movies/Kath/analysis"  # Directory to save the analysis files
)

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Function to split the video into sections using ffmpeg
def split_video_to_segments(video_path, segment_length=300):
    """Split the video into smaller segments."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(VIDEO_DIR, video_name + "_segments")
    os.makedirs(output_dir, exist_ok=True)

    # Using ffmpeg to split the video into smaller segments
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
    subprocess.run(command)

    # List the generated segments
    segments = sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".mp4")
        ]
    )
    return segments


# Function to transcribe video segments using Whisper
def transcribe_video_segment(file_path):
    with open(file_path, "rb") as video_file:
        transcript_data = client.audio.transcribe(
            "whisper-1", video_file, response_format="verbose_json"
        )

        # Build the transcript with timestamps
        transcript_with_timestamps = []
        for segment in transcript_data.segments:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(
                f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
            )

        return "\n".join(transcript_with_timestamps)


# Helper function to format timestamps
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Function to analyze the transcript for a section
def analyze_text_for_section(text, section_number):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in narrative-driven image generation for DALL-E. Your goal is to analyze each section of the transcript to extract themes, emotions, key objects, lighting, and colors for visual storytelling.",
            },
            {
                "role": "user",
                "content": f"Analyze the following song transcript to extract: (1) main themes, (2) emotions, (3) key objects or characters for the images, (4) suggested lighting and color schemes, and (5) a recommended transition from one image to the next: {text}",
            },
        ],
        max_tokens=300,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# Main function to process large videos in sections
def process_video_by_section(video_file, segment_length=300):
    # Split video into smaller segments
    segments = split_video_to_segments(video_file, segment_length)

    # Process each segment
    for index, segment in enumerate(segments):
        section_number = index + 1
        print(f"Processing Section {section_number}: {segment}")

        # Step 1: Transcribe the segment
        transcript = transcribe_video_segment(segment)
        transcript_file_path = os.path.join(
            TRANSCRIPT_DIR, f"section_{section_number}_transcript.txt"
        )
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        print(
            f"Transcription saved for Section {section_number} at {transcript_file_path}"
        )

        # Step 2: Analyze the segment's transcript
        analysis = analyze_text_for_section(transcript, section_number)
        analysis_file_path = os.path.join(
            ANALYSIS_DIR, f"section_{section_number}_analysis.txt"
        )
        with open(analysis_file_path, "w") as f:
            f.write(analysis)
        print(f"Analysis saved for Section {section_number} at {analysis_file_path}")


if __name__ == "__main__":
    import sys

    video_files = [
        "/Users/steven/Movies/Kath/Katheria_and_Salome_The_Daughters_of_Destinay-30m_compressed.mp4",
        "/Users/steven/Movies/Kath/Katheria and Salome_ The Daughters of Di 15min.mp4",
    ]

    for video_file in video_files:
        process_video_by_section(
            video_file, segment_length=300
        )  # Break into 5-minute sections
