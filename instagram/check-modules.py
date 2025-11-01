"""
Check Modules

This module provides functionality for check modules.

Author: Auto-generated
Date: 2025-11-01
"""

import sys

import logging

logger = logging.getLogger(__name__)


def check_modules():
    """check_modules function."""

    try:
        import requests
    except (requests.RequestException, urllib.error.URLError, ConnectionError):
        print_error("'requests' module not found!")
        print_status("run install_requirements.bat to install the modules")
        sys.exiprint_errort(0)

    try:
        import colorama
    except Exception as e:
        print_error("'colorama' package not installed!")
        print_status("run install_requirements.bat to install the modules")
        logger.info(e)
        sys.exit(0)

    try:
        import asyncio
    except (ImportError, ModuleNotFoundError):
        print_error("'asyncio' package not installed!")
        print_status("run install_requirements.bat to install the modules")
        sys.exit(0)

    try:
        import proxybroker
    except (ImportError, ModuleNotFoundError):
        print_error("'proxybroker' package not installed!")
        print_status("run install_requirements.bat to install the modules")
        sys.exit(0)

    try:
        import warnings
    except (ImportError, ModuleNotFoundError):
        print_error("'warnings' package not installed!")
        print_status("run install_requirements.bat to install the modules")
        sys.exit(0)

    import warnings

    warnings.filterwarnings("ignore")

    from colorama import init

    init()
