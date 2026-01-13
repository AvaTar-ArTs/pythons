#!/usr/bin/env python3
"""Webhook receiver - triggers workflows from external services"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, subprocess, os
from pathlib import Path

PORT = 8765
CONTENT_DIR = Path.home() / 'ai-sites' / 'content-management' / 'retention-hub'

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = json.loads(self.rfile.read(length))
        workflow = body.get('workflow')
        params = body.get('params', {})

        result = {'status': 'unknown', 'workflow': workflow}

        if workflow == 'generate_recipe':
            subprocess.run(['python3', str(CONTENT_DIR / 'recipes/generate_recipe.py')])
            result['status'] = 'triggered'
        elif workflow == 'daily_art':
            subprocess.run(['python3', str(CONTENT_DIR / 'daily-art/generate_daily_art.py')])
            result['status'] = 'triggered'
        elif workflow == 'weekly_music':
            subprocess.run(['python3', str(CONTENT_DIR / 'weekly-music/generate_weekly_playlist.py')])
            result['status'] = 'triggered'

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def log_message(self, format, *args):
        print(f"[webhook] {format % args}")

if __name__ == '__main__':
    print(f'🎣 Webhook receiver listening on http://localhost:{PORT}')
    print('Send POST: {"workflow": "generate_recipe"}')
    HTTPServer(('', PORT), WebhookHandler).serve_forever()
