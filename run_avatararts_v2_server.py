#!/usr/bin/env python3
"""
Simple HTTP server for AvatarArts v2 website
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def run_server(port=8000):
    """Run a simple HTTP server to serve the AvatarArts v2 website"""
    
    # Change to the website directory
    website_dir = Path(__file__).parent / "avatararts-v2"
    os.chdir(website_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"Serving AvatarArts v2 website at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Open the website in the default browser
    webbrowser.open(f"http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()