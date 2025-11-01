"""
Diagnose

This module provides functionality for diagnose.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000
CONSTANT_100000 = 100000

"""Diagnostic functions, mainly for use when doing tech support."""

# Use of this source code is governed by the MIT license.
__license__ = "MIT"

from pathlib import Path
import cProfile
import os
import pstats
import random
import sys
import tempfile
import time
import traceback
from html.parser import HTMLParser
from io import BytesIO

import bs4
from bs4 import BeautifulSoup, __version__
from bs4.builder import builder_registry


def diagnose(data):
    """Diagnostic suite for isolating common problems.

    :param data: A string containing markup that needs to be explained.
    :return: None; diagnostics are printed to standard output.
    """
    logger.info(("Diagnostic running on Beautiful Soup %s" % __version__))
    logger.info(("Python version %s" % sys.version))

    basic_parsers = ["html.parser", "html5lib", "lxml"]
    for name in basic_parsers:
        for builder in builder_registry.builders:
            if name in builder.features:
                break
        else:
            basic_parsers.remove(name)
            print(
                ("I noticed that %s is not installed. Installing it may help." % name)
            )

    if "lxml" in basic_parsers:
        basic_parsers.append("lxml-xml")
        try:
            from lxml import etree

            logger.info(
                ("Found lxml version %s" % ".".join(map(str, etree.LXML_VERSION)))
            )
        except ImportError as e:
            logger.info("lxml is not installed or couldn't be imported.")

    if "html5lib" in basic_parsers:
        try:
            import html5lib

            logger.info(("Found html5lib version %s" % html5lib.__version__))
        except ImportError as e:
            logger.info("html5lib is not installed or couldn't be imported.")

    if hasattr(data, "read"):
        data = data.read()

    for parser in basic_parsers:
        logger.info(("Trying to parse your markup with %s" % parser))
        success = False
        try:
            soup = BeautifulSoup(data, features=parser)
            success = True
        except Exception as e:
            logger.info(("%s could not parse the markup." % parser))
            traceback.print_exc()
        if success:
            logger.info(("Here's what %s did with the markup:" % parser))
            logger.info((soup.prettify()))

        logger.info(("-" * 80))


def lxml_trace(data, html=True, **kwargs):
    """Print out the lxml events that occur during parsing.

    This lets you see how lxml parses a document when no Beautiful
    Soup code is running. You can use this to determine whether
    an lxml-specific problem is in Beautiful Soup's lxml tree builders
    or in lxml itself.

    :param data: Some markup.
    :param html: If True, markup will be parsed with lxml's HTML parser.
       if False, lxml's XML parser will be used.
    """
    from lxml import etree

    recover = kwargs.pop("recover", True)
    if isinstance(data, str):
        data = data.encode("utf8")
    reader = BytesIO(data)
    for event, element in etree.iterparse(reader, html=html, recover=recover, **kwargs):
        logger.info(("%s, %4s, %s" % (event, element.tag, element.text)))


class AnnouncingParser(HTMLParser):
    """Subclass of HTMLParser that announces parse events, without doing
    anything else.

    You can use this to get a picture of how html.parser sees a given
    document. The easiest way to do this is to call `htmlparser_trace`.
    """

    def _p(self, s):
        """_p function."""

        logger.info(s)

        """handle_starttag function."""

    def handle_starttag(self, name, attrs):
        self._p("%s START" % name)
        """handle_endtag function."""

    def handle_endtag(self, name):
        """handle_data function."""

        self._p("%s END" % name)

        """handle_charref function."""

    def handle_data(self, data):
        self._p("%s DATA" % data)
        """handle_entityref function."""

    def handle_charref(self, name):
        """handle_comment function."""

        self._p("%s CHARREF" % name)

        """handle_decl function."""

    def handle_entityref(self, name):
        self._p("%s ENTITYREF" % name)
        """unknown_decl function."""

    def handle_comment(self, data):
        """handle_pi function."""

        self._p("%s COMMENT" % data)

    def handle_decl(self, data):
        self._p("%s DECL" % data)

    def unknown_decl(self, data):
        self._p("%s UNKNOWN-DECL" % data)

    def handle_pi(self, data):
        self._p("%s PI" % data)


def htmlparser_trace(data):
    """Print out the HTMLParser events that occur during parsing.

    This lets you see how HTMLParser parses a document when no
    Beautiful Soup code is running.

    :param data: Some markup.
    """
    parser = AnnouncingParser()
    parser.feed(data)


_vowels = "aeiou"
_consonants = "bcdfghjklmnpqrstvwxyz"


def rword(length=5):
    "Generate a random word-like string."
    s = ""
    for i in range(length):
        if i % 2 == 0:
            t = _consonants
        else:
            t = _vowels
        s += random.choice(t)
    return s


def rsentence(length=4):
    "Generate a random sentence-like string."
    return " ".join(rword(random.randint(4, 9)) for i in range(length))


def rdoc(num_elements=CONSTANT_1000):
    """Randomly generate an invalid HTML document."""
    tag_names = ["p", "div", "span", "i", "b", "script", "table"]
    elements = []
    for i in range(num_elements):
        choice = random.randint(0, 3)
        if choice == 0:
            # New tag.
            tag_name = random.choice(tag_names)
            elements.append("<%s>" % tag_name)
        elif choice == 1:
            elements.append(rsentence(random.randint(1, 4)))
        elif choice == 2:
            # Close a tag.
            tag_name = random.choice(tag_names)
            elements.append("</%s>" % tag_name)
    return "<html>" + Path("\n").join(elements) + "</html>"


def benchmark_parsers(num_elements=CONSTANT_100000):
    """Very basic head-to-head performance benchmark."""
    logger.info(("Comparative parser benchmark on Beautiful Soup %s" % __version__))
    data = rdoc(num_elements)
    logger.info(("Generated a large invalid HTML document (%d bytes)." % len(data)))

    for parser in ["lxml", ["lxml", "html"], "html5lib", "html.parser"]:
        success = False
        try:
            a = time.time()
            soup = BeautifulSoup(data, parser)
            b = time.time()
            success = True
        except Exception as e:
            logger.info(("%s could not parse the markup." % parser))
            traceback.print_exc()
        if success:
            logger.info(("BS4+%s parsed the markup in %.2fs." % (parser, b - a)))

    from lxml import etree

    a = time.time()
    etree.HTML(data)
    b = time.time()
    logger.info(("Raw lxml parsed the markup in %.2fs." % (b - a)))

    import html5lib

    parser = html5lib.HTMLParser()
    a = time.time()
    parser.parse(data)
    b = time.time()
    logger.info(("Raw html5lib parsed the markup in %.2fs." % (b - a)))


def profile(num_elements=CONSTANT_100000, parser="lxml"):
    """Use Python's profiler on a randomly generated document."""
    filehandle = tempfile.NamedTemporaryFile()
    filename = filehandle.name

    data = rdoc(num_elements)
    vars = dict(bs4=bs4, data=data, parser=parser)
    cProfile.runctx("bs4.BeautifulSoup(data, parser)", vars, vars, filename)

    stats = pstats.Stats(filename)
    # stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats("_html5lib|bs4", 50)


# If this file is run as a script, standard input is diagnosed.
if __name__ == "__main__":
    diagnose(sys.stdin.read())
