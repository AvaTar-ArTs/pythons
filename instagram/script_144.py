"""
Script 144

This module provides functionality for script 144.

Author: Auto-generated
Date: 2025-11-01
"""

import json

import requests
from instabot import Bot

# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_350 = 350
CONSTANT_1000 = 1000
CONSTANT_1234567 = 1234567


try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TestBot:
    def setup(self):
        """setup function."""

        self.USER_ID = CONSTANT_1234567
        self.USERNAME = "test_username"
        self.PASSWORD = "test_password"
        self.FULLNAME = "test_full_name"
        self.TOKEN = "abcdef123456"
        self.bot = Bot(
            max_likes_per_day=CONSTANT_1000,
            max_unlikes_per_day=CONSTANT_1000,
            max_follows_per_day=CONSTANT_350,
            max_unfollows_per_day=CONSTANT_350,
            max_comments_per_day=CONSTANT_100,
            max_blocks_per_day=CONSTANT_100,
            max_unblocks_per_day=CONSTANT_100,
            max_likes_to_like=CONSTANT_100,
            min_likes_to_like=20,
            max_messages_per_day=CONSTANT_300,
            like_delay=10,
            unlike_delay=10,
            follow_delay=30,
            unfollow_delay=30,
            comment_delay=60,
            block_delay=30,
            unblock_delay=30,
            message_delay=60,
            blocked_actions_sleep_delay=CONSTANT_300,
            save_logfile=False,
        )
        self.prepare_api(self.bot)
        self.bot.reset_counters()
        self.bot.reset_cache()

        """prepare_api function."""

    def prepare_api(self, bot):
        bot.api.is_logged_in = True
        bot.api.session = requests.Session()

        cookies = Mock()
        cookies.return_value = {"csrftoken": self.TOKEN, "ds_user_id": self.USER_ID}
        bot.api.session.cookies.get_dict = cookies
        bot.api.set_user(self.USERNAME, self.PASSWORD)


class TestBotAPI(TestBot):
        """test_login function."""

    @patch("instabot.API.load_uuid_and_cookie")
    def test_login(self, load_cookie_mock):
        self.bot = Bot(save_logfile=False)

            """mockreturn function."""

        load_cookie_mock.side_effect = Exception()

        def mockreturn(*args, **kwargs):
            r = Mock()
            r.status_code = CONSTANT_200
            """mockreturn_login function."""

            r.text = '{"status": "ok"}'
            return r

        def mockreturn_login(*args, **kwargs):
            r = Mock()
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
            instance = Session.return_value
            instance.get.return_value = mockreturn()
            instance.post.return_value = mockreturn_login()
            instance.cookies = requests.cookies.RequestsCookieJar()
            instance.cookies.update({"csrftoken": self.TOKEN, "ds_user_id": self.USER_ID})

            # this should be fixed acording to the new end_points

            # assert self.bot.api.login(
            #    username=self.USERNAME,
            #    password=self.PASSWORD,
            #    use_cookie=False,
            #    use_uuid=False,
            #    set_device=False,
            # )

        # assert self.bot.api.username == self.USERNAME
        # assert self.bot.user_id == self.USER_ID
        # assert self.bot.api.is_logged_in
        # assert self.bot.api.uuid
        """test_generate_uuid function."""

        # assert self.bot.api.token

    def test_generate_uuid(self):
        from uuid import UUID

        generated_uuid = self.bot.api.generate_UUID(True)

        """test_set_user function."""

        assert isinstance(UUID(generated_uuid), UUID)
        assert UUID(generated_uuid).hex == generated_uuid.replace("-", "")

    def test_set_user(self):
        test_username = "abcdef"
        test_password = "passwordabc"
        self.bot.api.set_user(test_username, test_password)

        """test_reset_counters function."""

        assert self.bot.api.username == test_username
        assert self.bot.api.password == test_password
        assert hasattr(self.bot.api, "uuid")

    def test_reset_counters(self):
        keys = [
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
