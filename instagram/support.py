"""
Test Bot Support

This module provides functionality for test bot support.

Author: Auto-generated
Date: 2025-11-01
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

import pytest

from .test_bot import TestBot

import logging

logger = logging.getLogger(__name__)



class TestBotSupport(TestBot):
    @pytest.mark.parametrize(
        "url,result",
        [
            ("https://google.com", ["https://google.com"]),
            ("google.com", ["google.com"]),
            ("google.com/search?q=instabot", ["google.com/search?q=instabot"]),
            (
                "https://google.com/search?q=instabot",
                ["https://google.com/search?q=instabot"],
            ),
            ("мвд.рф", ["мвд.рф"]),
            ("https://мвд.рф", ["https://мвд.рф"]),
            ("http://мвд.рф/news/", ["http://мвд.рф/news/"]),
            (
                "hello, google.com/search?q=test and bing.com",
                ["google.com/search?q=test", "bing.com"],
            ),
        ],
    )
    def test_extract_urls(self, url, result):
        """test_extract_urls function."""

        assert self.bot.extract_urls(url) == result

        """test_check_if_file_exist function."""

    def test_check_if_file_exist(self):
        test_file = open("test", "w")

        assert self.bot.check_if_file_exists("test")

        test_file.close()
        os.remove("test")
        """test_check_if_file_exist_fail function."""


    def test_check_if_file_exist_fail(self):
        assert not self.bot.check_if_file_exists("test")

    @pytest.mark.parametrize(
        """test_console_print function."""

        "verbosity,text,result", [(True, "test", "test"), (False, "test", "")]
    )
    def test_console_print(self, verbosity, text, result):
        self.bot.verbosity = verbosity
        try:
            if sys.version_info > (3,):
                from io import StringIO
            else:
                from StringIO import StringIO
            saved_stdout = sys.stdout
            out = StringIO()
            sys.stdout = out

            self.bot.console_print(text)

            output = out.getvalue().strip()
            assert output == result
        finally:
            sys.stdout = saved_stdout
