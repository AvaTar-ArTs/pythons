import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_350 = 350
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_1048576 = 1048576
CONSTANT_1234567 = 1234567
CONSTANT_9437184 = 9437184
CONSTANT_1073741824 = 1073741824


# Configure logging
logger = logging.getLogger(__name__)


# Constants

import json

import requests
from instabot import Bot
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1048576
    GB_SIZE = CONSTANT_1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = CONSTANT_9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    max_likes_per_day = CONSTANT_1000, 
    max_unlikes_per_day = CONSTANT_1000, 
    max_follows_per_day = CONSTANT_350, 
    max_unfollows_per_day = CONSTANT_350, 
    max_comments_per_day = DEFAULT_BATCH_SIZE, 
    max_blocks_per_day = DEFAULT_BATCH_SIZE, 
    max_unblocks_per_day = DEFAULT_BATCH_SIZE, 
    max_likes_to_like = DEFAULT_BATCH_SIZE, 
    min_likes_to_like = 20, 
    max_messages_per_day = DPI_300, 
    like_delay = 10, 
    unlike_delay = 10, 
    follow_delay = DEFAULT_TIMEOUT, 
    unfollow_delay = DEFAULT_TIMEOUT, 
    comment_delay = 60, 
    block_delay = DEFAULT_TIMEOUT, 
    unblock_delay = DEFAULT_TIMEOUT, 
    message_delay = 60, 
    blocked_actions_sleep_delay = DPI_300, 
    save_logfile = False, 
    cookies = Mock()
    r = Mock()
    r = Mock()
    instance = Session.return_value
    generated_uuid = self.bot.api.generate_UUID(True)
    test_username = "abcdef"
    test_password = "passwordabc"
    keys = [


try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TestBot:
    def setup(self):
     """
     TODO: Add function documentation
     """
        self.USER_ID = CONSTANT_1234567
        self.USERNAME = "test_username"
        self.PASSWORD = "test_password"
        self.FULLNAME = "test_full_name"
        self.TOKEN = "abcdef123456"
        self.bot = Bot(
        )
        self.prepare_api(self.bot)
        self.bot.reset_counters()
        self.bot.reset_cache()

    def prepare_api(self, bot):
     """
     TODO: Add function documentation
     """
        bot.api.is_logged_in = True
        bot.api.session = requests.Session()

        cookies.return_value = {"csrftoken": self.TOKEN, "ds_user_id": self.USER_ID}
        bot.api.session.cookies.get_dict = cookies
        bot.api.set_user(self.USERNAME, self.PASSWORD)


class TestBotAPI(TestBot):
    @patch("instabot.API.load_uuid_and_cookie")
    def test_login(self, load_cookie_mock):
     """
     TODO: Add function documentation
     """
        self.bot = Bot(save_logfile = False)

        load_cookie_mock.side_effect = Exception()

        def mockreturn(*args, **kwargs):
         """
         TODO: Add function documentation
         """
            r.status_code = CONSTANT_200
            r.text = '{"status": "ok"}'
            return r

        def mockreturn_login(*args, **kwargs):
         """
         TODO: Add function documentation
         """
            r.status_code = CONSTANT_200
            r.text = json.dumps(
                {
                    "logged_in_user": {
                        "pk": self.USER_ID, 
                        "username": self.USERNAME, 
                        "full_name": self.FULLNAME, 
                    }, 
                    "status": "ok", 
                }
            )
            return r

        with patch("requests.Session") as Session:
            instance.get.return_value = mockreturn()
            instance.post.return_value = mockreturn_login()
            instance.cookies = requests.cookies.RequestsCookieJar()
            instance.cookies.update({"csrftoken": self.TOKEN, "ds_user_id": self.USER_ID})

            # this should be fixed acording to the new end_points

            # assert self.bot.api.login(
            #    username = self.USERNAME, 
            #    password = self.PASSWORD, 
            #    use_cookie = False, 
            #    use_uuid = False, 
            #    set_device = False, 
            # )

        # assert self.bot.api.username == self.USERNAME
        # assert self.bot.user_id == self.USER_ID
        # assert self.bot.api.is_logged_in
        # assert self.bot.api.uuid
        # assert self.bot.api.token

    def test_generate_uuid(self):
     """
     TODO: Add function documentation
     """
        from uuid import UUID


        assert isinstance(UUID(generated_uuid), UUID)
        assert UUID(generated_uuid).hex == generated_uuid.replace("-", "")

    def test_set_user(self):
     """
     TODO: Add function documentation
     """
        self.bot.api.set_user(test_username, test_password)

        assert self.bot.api.username == test_username
        assert self.bot.api.password == test_password
        assert hasattr(self.bot.api, "uuid")

    def test_reset_counters(self):
     """
     TODO: Add function documentation
     """
            "liked", 
            "unliked", 
            "followed", 
            "messages", 
            "unfollowed", 
            "commented", 
            "blocked", 
            "unblocked", 
        ]
        for key in keys:
            self.bot.total[key] = 1
            assert self.bot.total[key] == 1
        self.bot.reset_counters()
        for key in keys:
            assert self.bot.total[key] == 0


if __name__ == "__main__":
    main()
