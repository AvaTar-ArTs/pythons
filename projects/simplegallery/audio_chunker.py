"""
Audio chunking utilities for handling long files
"""

import logging
import os
from pathlib import Path
from typing import List, Tuple

from moviepy.editor import AudioFileClip

import config

logger = logging.getLogger(__name__)


class AudioChunker:
    def __init__(self):
        self.max_chunk_duration = (
            config.MAX_CHUNK_DURATION_MINUTES * 60
        )  # Convert to seconds
        self.chunk_overlap = config.CHUNK_OVERLAP_SECONDS
        self.min_chunk_duration = (
            config.MIN_CHUNK_DURATION_MINUTES * 60
        )  # Convert to seconds

    def get_audio_duration(self, audio_path: str) -> float:
        """Get the duration of an audio file in seconds."""
        try:
            with AudioFileClip(audio_path) as audio:
                return audio.duration
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 0.0

    def should_split_file(self, audio_path: str) -> bool:
        """Determine if a file should be split based on its duration."""
        duration = self.get_audio_duration(audio_path)
        return duration > self.max_chunk_duration

    def calculate_chunks(self, total_duration: float) -> List[Tuple[float, float]]:
        """Calculate chunk start and end times for splitting."""
        chunks = []
        current_start = 0.0

        while current_start < total_duration:
            # Calculate end time for this chunk
            current_end = min(current_start + self.max_chunk_duration, total_duration)

            # Adjust for minimum chunk duration
            if (
                current_end - current_start < self.min_chunk_duration
                and len(chunks) > 0
            ):
                # Merge with previous chunk if too small
                if chunks:
                    prev_start, prev_end = chunks[-1]
                    chunks[-1] = (prev_start, current_end)
                else:
                    chunks.append((current_start, current_end))
            else:
                chunks.append((current_start, current_end))

            # Move to next chunk with overlap
            current_start = current_end - self.chunk_overlap

            # Prevent infinite loop
            if current_start >= total_duration:
                break

        return chunks

    def split_audio_file(self, audio_path: str, output_dir: Path) -> List[str]:
        """Split an audio file into chunks and return list of chunk file paths."""
        try:
            duration = self.get_audio_duration(audio_path)
            if duration == 0:
                logger.error("Could not determine audio duration")
                return []

            logger.info(f"Audio duration: {duration / 60:.1f} minutes")

            if not self.should_split_file(audio_path):
                logger.info("File is short enough, no splitting needed")
                return [audio_path]

            chunks = self.calculate_chunks(duration)
            logger.info(f"Splitting into {len(chunks)} chunks")

            chunk_files = []
            audio_file = Path(audio_path)

            with AudioFileClip(audio_path) as audio:
                for i, (start_time, end_time) in enumerate(chunks, 1):
                    chunk_filename = f"{audio_file.stem}_chunk_{i:02d}.mp3"
                    chunk_path = output_dir / chunk_filename

                    logger.info(
                        f"Creating chunk {i}/{len(chunks)}: {start_time:.1f}s - {end_time:.1f}s"
                    )

                    # Extract chunk
                    chunk_audio = audio.subclip(start_time, end_time)
                    chunk_audio.write_audiofile(
                        str(chunk_path), verbose=False, logger=None, codec="mp3"
                    )
                    chunk_audio.close()

                    chunk_files.append(str(chunk_path))

            logger.info(f"Successfully created {len(chunk_files)} chunks")
            return chunk_files

        except Exception as e:
            logger.error(f"Error splitting audio file: {e}")
            return []

    def merge_transcripts(:
        self, chunk_transcripts: List[dict], chunk_files: List[str]
    ) -> dict:
        """Merge transcripts from multiple chunks into a single transcript."""
        try:
            # Combine all segments with adjusted timestamps
            all_segments = []
            current_time_offset = 0.0

            for i, (chunk_transcript, chunk_file) in enumerate(
                zip(chunk_transcripts, chunk_files)
            ):
                if not chunk_transcript or "segments" not in chunk_transcript:
                    continue

                # Adjust timestamps for this chunk
                for segment in chunk_transcript["segments"]:
                    adjusted_segment = segment.copy()
                    adjusted_segment["start"] += current_time_offset
                    adjusted_segment["end"] += current_time_offset
                    adjusted_segment["chunk"] = i + 1
                    adjusted_segment["chunk_file"] = Path(chunk_file).name
                    all_segments.append(adjusted_segment)

                # Calculate time offset for next chunk (accounting for overlap)
                if i < len(chunk_transcripts) - 1:  # Not the last chunk
                    chunk_duration = self.get_audio_duration(chunk_file)
                    current_time_offset += chunk_duration - self.chunk_overlap

            # Create merged transcript
            merged_transcript = {
                "full_transcript": " ".join(
                    segment["text"].strip() for segment in all_segments
                ),
                "segments": all_segments,
                "language": chunk_transcripts[0].get("language", "unknown")
                if chunk_transcripts
                else "unknown",
                "chunk_count": len(chunk_transcripts),
                "total_duration": current_time_offset,
            }

            # Create timestamped transcript
            timestamped_lines = []
            for segment in all_segments:
                start_time = self._format_timestamp(segment["start"])
                end_time = self._format_timestamp(segment["end"])
                chunk_info = (
                    f" [Chunk {segment['chunk']}]" if len(chunk_transcripts) > 1 else ""
                )
                text = segment["text"].strip()
                timestamped_lines.append(
                    f"[{start_time} - {end_time}]{chunk_info} {text}"
                )

            merged_transcript["timestamped_transcript"] = "\n".join(timestamped_lines)

            return merged_transcript

        except Exception as e:
            logger.error(f"Error merging transcripts: {e}")
            return {}

    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def cleanup_chunks(self, chunk_files: List[str]) -> None:
        """Clean up temporary chunk files."""
        for chunk_file in chunk_files:
            try:
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
                    logger.debug(f"Cleaned up chunk file: {chunk_file}")
            except Exception as e:
                logger.warning(f"Could not clean up chunk file {chunk_file}: {e}")
