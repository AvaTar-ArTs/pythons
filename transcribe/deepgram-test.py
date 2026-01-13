# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import httpx
import threading

import os
from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# load_dotenv()  # Now using ~/.env.d/

# The API key you created in step 1
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

# URL for the real-time streaming audio you would like to transcribe
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'

def main():
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        dg_connection = deepgram.listen.live.v('1')

        # Listen for any transcripts received from Deepgram and write them to the console
        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            logger.info(f'transcript: {sentence}')

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Create a websocket connection to Deepgram
        options = LiveOptions(
            smart_format=True, model="nova-2", language="en-US"
        )
        dg_connection.start(options)

        lock_exit = threading.Lock()
        exit = False
        # Listen for the connection to open and send streaming audio from the URL to Deepgram
        def myThread():
            with httpx.stream('GET', URL) as r:
                for data in r.iter_bytes():
                    lock_exit.acquire()
                    if exit:
                        break
                    lock_exit.release()

                    dg_connection.send(data)

        myHttp = threading.Thread(target=myThread)
        myHttp.start()

        input('Press Enter to stop transcription...\n')
        lock_exit.acquire()
        exit = True
        lock_exit.release()

        myHttp.join()

        # Indicate that we've finished by sending the close stream message
        dg_connection.finish()
        logger.info('Finished')

    except Exception as e:
        logger.info(f'Could not open socket: {e}')
        return

if __name__ == '__main__':
    main()
