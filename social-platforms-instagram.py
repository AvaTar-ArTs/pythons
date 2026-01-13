"""
Configuration settings for the Transcription Analyzer
"""

# Whisper model options (smaller = faster, less accurate)
# Options: "tiny", "base", "small", "medium", "large"
WHISPER_MODEL = "base"

# OpenAI model for analysis
OPENAI_MODEL = "gpt-4o"

# Analysis settings
ANALYSIS_TEMPERATURE = 0.3
ANALYSIS_MAX_TOKENS = CONSTANT_2000

# File processing settings
SUPPORTED_AUDIO_FORMATS = [".mp3", ".mp4", ".MP3", ".MP4"]
AUDIO_QUALITY = "medium"  # Options: "low", "medium", "high"

# Output settings
INCLUDE_RAW_ANALYSIS = True
CREATE_SUMMARY_FILE = True
TIMESTAMP_FORMAT = "MM:SS"  # Options: "MM:SS", "HH:MM:SS"

# Chunking settings for long files
MAX_CHUNK_DURATION_MINUTES = 20  # Split files longer than this
CHUNK_OVERLAP_SECONDS = 30  # Overlap between chunks to avoid cutting words
MIN_CHUNK_DURATION_MINUTES = 5  # Minimum chunk size to avoid tiny fragments

# Logging settings
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"
LOG_TO_FILE = True
LOG_TO_CONSOLE = True
