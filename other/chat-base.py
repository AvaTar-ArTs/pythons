"""
Summary of chat-base.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
# the Telegram trackings
from chatbase import Message


def TRChatBase(chat_id, message_text, intent):
    """TRChatBase function."""

    msg = Message(
        api_key=Config.CHAT_BASE_TOKEN,
        platform="Telegram",
        version="1.3",
        user_id=chat_id,
        message=message_text,
        intent=intent,
    )
    msg.send()
