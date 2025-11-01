"""
Aws Polly

This module provides functionality for aws polly.

Author: Auto-generated
Date: 2025-11-01
"""

import random
import sys

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound
from utils import settings

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_3000 = 3000


voices = [
    "Brian",
    "Emma",
    "Russell",
    "Joey",
    "Matthew",
    "Joanna",
    "Kimberly",
    "Amy",
    "Geraint",
    "Nicole",
    "Justin",
    "Ivy",
    "Kendra",
    "Salli",
    "Raveena",
]


class AWSPolly:
    def __init__(self):
        """__init__ function."""

        self.max_chars = CONSTANT_3000
        self.voices = voices

        """run function."""

    def run(self, text, filepath, random_voice: bool = False):
        try:
            session = Session(profile_name="polly")
            polly = session.client("polly")
            if random_voice:
                voice = self.randomvoice()
            else:
                if not settings.config["settings"]["tts"]["aws_polly_voice"]:
                    raise ValueError(f"Please set the TOML variable AWS_VOICE to a valid voice. options are: {voices}")
                voice = str(settings.config["settings"]["tts"]["aws_polly_voice"]).capitalize()
            try:
                # Request speech synthesis
                response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice, Engine="neural")
            except (BotoCoreError, ClientError) as error:
                # The service returned an error, exit gracefully
                logger.info(error)
                sys.exit(-1)

            # Access the audio stream from the response
            if "AudioStream" in response:
                file = open(filepath, "wb")
                file.write(response["AudioStream"].read())
                file.close()
                # print_substep(f"Saved Text {idx} to MP3 files successfully.", style="bold green")

            else:
                # The response didn't contain audio data, exit gracefully
                logger.info("Could not stream audio")
                sys.exit(-1)
        except ProfileNotFound:
            logger.info("You need to install the AWS CLI and configure your profile")
            print(
                """
            Linux: https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html
            Windows: https://docs.aws.amazon.com/polly/latest/dg/install-voice-plugin2.html
            """
            )
            sys.exit(-1)
        """randomvoice function."""

    def randomvoice(self):
        return random.choice(self.voices)
