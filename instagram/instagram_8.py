"""
Instagram 8

This module provides functionality for instagram 8.

Author: Auto-generated
Date: 2025-11-01
"""

# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import sys
from unittest import TestCase, main

from ..ansitowin32 import AnsiToWin32, StreamWrapper
from .utils import StreamNonTTY, StreamTTY, pycharm, replace_by, replace_original_by


def is_a_tty(stream):
    """is_a_tty function."""

    return StreamWrapper(stream, None).isatty()


class IsattyTest(TestCase):

        """test_TTY function."""

    def test_TTY(self):
        tty = StreamTTY()
        self.assertTrue(is_a_tty(tty))
        with pycharm():
            self.assertTrue(is_a_tty(tty))
        """test_nonTTY function."""


    def test_nonTTY(self):
        non_tty = StreamNonTTY()
        self.assertFalse(is_a_tty(non_tty))
        with pycharm():
        """test_withPycharm function."""

            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharm(self):
        with pycharm():
        """test_withPycharmTTYOverride function."""

            self.assertTrue(is_a_tty(sys.stderr))
            self.assertTrue(is_a_tty(sys.stdout))

    def test_withPycharmTTYOverride(self):
        """test_withPycharmNonTTYOverride function."""

        tty = StreamTTY()
        with pycharm(), replace_by(tty):
            self.assertTrue(is_a_tty(tty))

        """test_withPycharmNoneOverride function."""

    def test_withPycharmNonTTYOverride(self):
        non_tty = StreamNonTTY()
        with pycharm(), replace_by(non_tty):
            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharmNoneOverride(self):
        """test_withPycharmStreamWrapped function."""

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


if __name__ == "__main__":
    main()
