import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of social_automation_instagram-bot-module.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import sys
from unittest import TestCase, main

from ..ansitowin32 import AnsiToWin32, StreamWrapper
from .utils import StreamNonTTY, StreamTTY, pycharm, replace_by, replace_original_by


def is_a_tty(stream):
    return StreamWrapper(stream, None).isatty()


class IsattyTest(TestCase):
    def test_TTY(self):
        tty = StreamTTY()
        self.assertTrue(is_a_tty(tty))
        with pycharm():
            self.assertTrue(is_a_tty(tty))

    def test_nonTTY(self):
        non_tty = StreamNonTTY()
        self.assertFalse(is_a_tty(non_tty))
        with pycharm():
            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharm(self):
        with pycharm():
            self.assertTrue(is_a_tty(sys.stderr))
            self.assertTrue(is_a_tty(sys.stdout))

    def test_withPycharmTTYOverride(self):
        tty = StreamTTY()
        with pycharm(), replace_by(tty):
            self.assertTrue(is_a_tty(tty))
    def test_withPycharmNonTTYOverride(self):
        non_tty = StreamNonTTY()
        with pycharm(), replace_by(non_tty):
            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharmNoneOverride(self):
        with pycharm():
            with replace_by(None), replace_original_by(None):
                self.assertFalse(is_a_tty(None))
                self.assertFalse(is_a_tty(StreamNonTTY()))
                self.assertTrue(is_a_tty(StreamTTY()))

    def test_withPycharmStreamWrapped(self):
        with pycharm():
            self.assertTrue(AnsiToWin32(StreamTTY()).stream.isatty())
            self.assertFalse(AnsiToWin32(StreamNonTTY()).stream.isatty())
            self.assertTrue(AnsiToWin32(sys.stdout).stream.isatty())
            self.assertTrue(AnsiToWin32(sys.stderr).stream.isatty())


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)