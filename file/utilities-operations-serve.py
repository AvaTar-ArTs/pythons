"""
Utilities File Operations Serve 2

This module provides functionality for utilities file operations serve 2.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_8001 = 8001

#!/usr/bin/env python3
"""
Code Browser Server
Serves the visual code browser locally
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path


def serve_code_browser(port=CONSTANT_8001):
    """Serve the code browser on the specified port."""
    browser_path = Path(Path("/Users/steven/Documents/python/code_browser"))

    if not browser_path.exists():
        logger.info("❌ Code browser not found. Run create_code_browser.py first.")
        return

    os.chdir(browser_path)

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"🚀 Serving code browser at http://localhost:{port}")
        logger.info(f"📁 Serving from: {browser_path}")
        logger.info("🌐 Opening in browser...")
        logger.info("Press Ctrl+C to stop the server")

        # Open in browser
        webbrowser.open(f"http://localhost:{port}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("\n👋 Server stopped")


if __name__ == "__main__":
    import sys

    port = CONSTANT_8001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.info("❌ Invalid port number. Using default port CONSTANT_8001.")

    serve_code_browser(port)
