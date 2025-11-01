"""
Youtube Print Logo

This module provides functionality for youtube print logo.

Author: Auto-generated
Date: 2025-11-01
"""

# coding=utf-8
#!/usr/bin/env python3

from libs.animation import colorText

import logging

logger = logging.getLogger(__name__)


logo = """

[[black-bright-background]][[yellow]] ██▓ [[yellow]]███▄    █  [[yellow]] ██████ [[yellow]]▄▄▄█████▓ [[yellow]]▄▄▄         [[yellow]] ██▀███  [[yellow]]▓█████ [[yellow]] ██▓███   [[yellow]]▒█████   [[yellow]]██▀███  [[yellow]]▄▄▄█████▓[[reset]]
[[black-bright-background]][[yellow]]▓██▒ [[yellow]]██ ▀█   █ ▒[[yellow]]██    ▒ [[yellow]]▓  ██▒ ▓▒▒[[yellow]]████▄       [[yellow]]▓██ ▒ ██▒[[yellow]]▓█   ▀ [[yellow]]▓██░  ██▒▒[[yellow]]██▒  ██▒▓[[yellow]]██ ▒ ██▒[[yellow]]▓  ██▒ ▓▒[[reset]]
[[black-bright-background]][[yellow]]▒██▒▓[[yellow]]██  ▀█ ██▒░[[yellow]] ▓██▄   [[yellow]]▒ ▓██░ ▒░▒[[yellow]]██  ▀█▄     [[yellow]]▓██ ░▄█ ▒[[yellow]]▒███   [[yellow]]▓██░ ██▓▒▒[[yellow]]██░  ██▒▓[[yellow]]██ ░▄█ ▒[[yellow]]▒ ▓██░ ▒░[[reset]]
[[black-bright-background]][[yellow]]░██░▓[[yellow]]██▒  ▐▌██▒ [[yellow]] ▒   ██▒[[yellow]]░ ▓██▓ ░ ░[[yellow]]██▄▄▄▄██    [[yellow]]▒██▀▀█▄  [[yellow]]▒▓█  ▄ [[yellow]]▒██▄█▓▒ ▒▒[[yellow]]██   ██░▒[[yellow]]██▀▀█▄  [[yellow]]░ ▓██▓ ░ [[reset]]
[[black-bright-background]][[yellow]]░██░▒[[yellow]]██░   ▓██░▒[[yellow]]██████▒▒[[yellow]]  ▒██▒ ░  [[yellow]]▓█   ▓██▒   [[yellow]]░██▓ ▒██▒[[yellow]]░▒████▒[[yellow]]▒██▒ ░  ░░[[yellow]] ████▓▒░░[[yellow]]██▓ ▒██▒[[yellow]]  ▒██▒ ░ [[reset]]
[[black-bright-background]][[yellow]]░▓  ░[[yellow]] ▒░   ▒ ▒ ▒[[yellow]] ▒▓▒ ▒ ░[[yellow]]  ▒ ░░    [[yellow]]▒▒   ▓▒█░   [[yellow]]░ ▒▓ ░▒▓░[[yellow]]░░ ▒░ ░[[yellow]]▒▓▒░ ░  ░░[[yellow]] ▒░▒░▒░ ░[[yellow]] ▒▓ ░▒▓░[[yellow]]  ▒ ░░   [[reset]]
[[black-bright-background]][[yellow]] ▒ ░░[[yellow]] ░░   ░ ▒░░[[yellow]] ░▒  ░ ░[[yellow]]    ░     [[yellow]] ▒   ▒▒ ░   [[yellow]]  ░▒ ░ ▒░[[yellow]] ░ ░  ░[[yellow]]░▒ ░      [[yellow]] ░ ▒ ▒░  [[yellow]] ░▒ ░ ▒░[[yellow]]    ░    [[reset]]
[[black-bright-background]][[yellow]] ▒ ░ [[yellow]]  ░   ░ ░ ░[[yellow]]  ░  ░  [[yellow]]  ░       [[yellow]] ░   ▒      [[yellow]]  ░░   ░ [[yellow]]   ░   [[yellow]]░░       ░[[yellow]] ░ ░ ▒   [[yellow]] ░░   ░ [[yellow]]  ░      [[reset]]
[[black-bright-background]][[yellow]] ░   [[yellow]]        ░  [[yellow]]     ░  [[yellow]]          [[yellow]]     ░  ░   [[yellow]]   ░     [[yellow]]   ░  ░[[yellow]]          [[yellow]]   ░ ░   [[yellow]]  ░     [[yellow]]         [[reset]]
                                                                                                  

                                           
"""


def print_logo():
    """print_logo function."""

    logger.info(colorText(logo))
