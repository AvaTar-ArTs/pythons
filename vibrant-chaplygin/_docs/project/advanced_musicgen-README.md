# Suno-Style Advanced AI Music Generator

This advanced prototype replicates the core functionality of Suno using open-source models and APIs.

## Key Features

- 🎼 Text-to-Lyrics using GPT-4o
- 🎹 Music generation using Meta’s MusicGen
- 🎤 Vocals using Bark (voice synthesis model)
- 🎧 Mixing with `pydub`

## Requirements

Install dependencies:

```bash
pip install openai torchaudio pydub
pip install git+https://github.com/facebookresearch/audiocraft.git
pip install git+https://github.com/suno-ai/bark.git
```

Install `ffmpeg` for audio processing if not already installed.

## Usage

```bash
python suno_advanced_musicgen.py
```

Enter a prompt like:
> A chill synthwave track about time travel and nostalgia

## Output Files

- `lyrics.txt`: Generated lyrics
- `instrumental.wav`: Backing track
- `vocals.wav`: Synthesized voice
- `final_song.wav`: Combined mix

---

🔧 Replace Bark/MusicGen with other models if needed for performance or quality.
