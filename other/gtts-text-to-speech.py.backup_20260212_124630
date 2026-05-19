import random

from gtts import gTTS
from utils import settings

# Constants
CONSTANT_5000 = 5000


class GTTS:
    def __init__(self):
        """__init__ function."""

        self.max_chars = CONSTANT_5000
        self.voices = []

        """run function."""

    def run(self, text, filepath):
        tts = gTTS(
            text=text,
            lang=settings.config["reddit"]["thread"]["post_lang"] or "en",
            slow=False,
        )
        tts.save(filepath)
        """randomvoice function."""

    def randomvoice(self):
        return random.choice(self.voices)
