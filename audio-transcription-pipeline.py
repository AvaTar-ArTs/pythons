"""Shared audio transcription + analysis pipeline helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Optional

from openai import OpenAI

from .chat import run_chat_completion

# Constants
CONSTANT_1000 = 1000



def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"
def transcribe_audio(client: OpenAI, file_path: Path) -> str:
    with file_path.open("rb") as audio_file:
        transcript_data = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json")

    transcript_with_timestamps = []
    for segment in transcript_data.segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        transcript_with_timestamps.append(
            f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
        )

    return Path("\n").join(transcript_with_timestamps)
def analyze_transcript(
    client: OpenAI,
    *,
    transcript: str,
    section_name: str,
    system_prompt: str,
    user_template: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = CONSTANT_1000) -> str:
    user_prompt = user_template.format(text=transcript, section_name=section_name)
    return run_chat_completion(
        client,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens)

def iter_audio_files(audio_dir: Path, extensions: Iterable[str]) -> Iterable[Path]:
    for root, _, files in os.walk(audio_dir):
        for filename in files:
            if filename.lower().endswith(tuple(extensions)):
                yield Path(root) / filename


def process_directory(
    client: OpenAI,
    *,
    audio_dir: Path,
    transcript_dir: Path,
    analysis_dir: Path,
    system_prompt: str,
    user_template: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = CONSTANT_1000,
    extensions: Optional[Iterable[str]] = None) -> None:
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    extensions = tuple(e.lower() for e in (extensions or (".mp3")))

    for audio_file in iter_audio_files(audio_dir, extensions):
        stem = audio_file.stem

        transcript_text = transcribe_audio(client, audio_file)
        transcript_output = transcript_dir / f"{stem}_transcript.txt"
        transcript_output.write_text(transcript_text, encoding="utf-8")

        analysis_text = analyze_transcript(
            client,
            transcript=transcript_text,
            section_name=stem,
            system_prompt=system_prompt,
            user_template=user_template,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens)
        analysis_output = analysis_dir / f"{stem}_analysis.txt"
        analysis_output.write_text(analysis_text, encoding="utf-8")

