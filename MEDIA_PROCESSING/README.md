# Consolidated Media Processor

A comprehensive tool for processing images, audio, and video files with unified interfaces.

## Features

- **Image processing**: resizing, upscaling, format conversion
- **Audio processing**: text-to-speech, format conversion
- **Video processing**: download, format conversion
- **Batch processing** with progress tracking
- **Comprehensive error handling** and logging
- **Configurable settings**
- **Type hints** and documentation

## Installation

```bash
cd /Users/steven/pythons/MEDIA_PROCESSING
python setup.py
```

This will:
1. Install required Python dependencies
2. Create an executable script in `~/bin/media-processor`

## Usage

### Command Line Interface

```bash
# Process images with multiple aspect ratios
media-processor process-images -i ./input_images -o ./output

# Upscale an image by 2x
media-processor upscale -i input.jpg -o output.jpg

# Convert image format
media-processor convert-format -i input.png -o output.jpg -f .jpg

# Convert text to speech
media-processor text-to-speech --text "Hello World" -o output.mp3 --lang en

# Convert audio format
media-processor convert-audio -i input.wav -o output.mp3 -f .mp3

# Download video
media-processor download-video --input URL -o output.mp4
```

### Supported Image Formats
- Input: JPG, JPEG, PNG, TIFF, BMP, WEBP
- Output: JPG, PNG, BMP, TIFF, WEBP

### Supported Audio Formats
- Input: MP3, WAV, FLAC, AAC, M4A, OGG
- Output: MP3, WAV, FLAC, AAC, M4A, OGG

### Supported Video Formats
- Input: MP4, AVI, MOV, MKV, WMV, FLV, WEBM
- Output: Same as input (for download)

## Configuration

The processor uses a default configuration, but you can customize:

- Maximum file size (default: 9.0 MB)
- Target DPI (default: 300)
- Base size for calculations (default: 2000)
- Maximum dimension (default: 4000)
- Quality range and step for optimization
- Batch size and worker count

## Requirements

- Python 3.7+
- macOS (for sips command - for image processing)
- ffmpeg (for audio/video conversion)
- Internet connection (for text-to-speech and video download)

## Dependencies

- Pillow: Image processing
- gTTS: Text-to-speech
- mutagen: Audio metadata
- requests: HTTP requests

## License

MIT License - feel free to modify and distribute.