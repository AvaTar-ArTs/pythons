#!/usr/bin/env python3
"""
Heavenly Hands Web Application - Production Ready
Integrated with ~/.env.d environment management
"""

import os
import sys
from pathlib import Path

# Load environment from ~/.env.d
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except ImportError:
    print("Warning: ~/.env.d loader not found. Using system environment variables.")

# Import the main application
from heavenly_hands_web import app

if __name__ == "__main__":
    # Production configuration
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"🏠 Starting Heavenly Hands Call Center on port {port}")
    print(f"🌐 Web interface: http://localhost:{port}")

    app.run(host='0.0.0.0', port=port, debug=debug)
