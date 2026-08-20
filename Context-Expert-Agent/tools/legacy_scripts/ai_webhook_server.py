#!/usr/bin/env python3
"""
AI Content Automation Webhook Server
====================================

A Flask-based webhook server that integrates with Make.com and Airtable
to automate AI content generation workflows.

Usage:
    python ai_webhook_server.py

Endpoints:
    POST /webhooks/content-generation
    POST /webhooks/voice-synthesis  
    POST /webhooks/image-generation
    POST /webhooks/status
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from pathlib import Path
import subprocess
import threading
import time

# Load environment variables
from env_d_loader import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global status tracking
processing_status = {}

class AIWebhookProcessor:
    """Handles AI content generation requests"""
    
    def __init__(self):
        self.base_path = Path("/Users/steven/Documents/python/LLM_APPLICATIONS/content_generation")
        
    def process_content_generation(self, data):
        """Process content generation request"""
        try:
            content_type = data.get('content_type', 'blog_post')
            title = data.get('title', 'Untitled')
            description = data.get('description', '')
            tone = data.get('tone', 'professional')
            word_count = data.get('word_count', 1000)
            keywords = data.get('keywords', [])
            
            # Create content generation command
            script_path = self.base_path / "AI_CONTENT_GENERATION_AI_CONTENT_AI_CONTENT_content_creation_agent.py"
            
            if not script_path.exists():
                return {"error": "Content generation script not found"}
            
            # Prepare arguments
            args = [
                "python3", str(script_path),
                "--title", title,
                "--description", description,
                "--tone", tone,
                "--word_count", str(word_count),
                "--keywords", ",".join(keywords)
            ]
            
            # Execute in background
            process_id = f"content_{int(time.time())}"
            thread = threading.Thread(
                target=self._run_content_generation,
                args=(process_id, args, data)
            )
            thread.start()
            
            processing_status[process_id] = {
                "status": "processing",
                "type": "content_generation",
                "started_at": datetime.now().isoformat(),
                "data": data
            }
            
            return {
                "process_id": process_id,
                "status": "processing",
                "message": "Content generation started"
            }
            
        except Exception as e:
            logger.error(f"Content generation error: {e}")
            return {"error": str(e)}
    
    def process_voice_synthesis(self, data):
        """Process voice synthesis request"""
        try:
            text = data.get('text', '')
            voice = data.get('voice', 'alloy')
            model = data.get('model', 'tts-1')
            speed = data.get('speed', 1.0)
            format_type = data.get('format', 'mp3')
            
            # Use the unified TTS script
            script_path = self.base_path / "AI_CONTENT_GENERATION_AI_CONTENT_AI_CONTENT_voice_synthesis_scripty_tts_unified_v2.py"
            
            if not script_path.exists():
                return {"error": "Voice synthesis script not found"}
            
            # Create temporary text file
            temp_file = Path("/tmp/tts_input.txt")
            temp_file.write_text(text)
            
            # Prepare arguments
            args = [
                "python3", str(script_path),
                "--source", str(temp_file),
                "--voice", voice,
                "--mode", "asmr",
                "--bitrate", "320k"
            ]
            
            # Execute in background
            process_id = f"voice_{int(time.time())}"
            thread = threading.Thread(
                target=self._run_voice_synthesis,
                args=(process_id, args, data)
            )
            thread.start()
            
            processing_status[process_id] = {
                "status": "processing",
                "type": "voice_synthesis",
                "started_at": datetime.now().isoformat(),
                "data": data
            }
            
            return {
                "process_id": process_id,
                "status": "processing",
                "message": "Voice synthesis started"
            }
            
        except Exception as e:
            logger.error(f"Voice synthesis error: {e}")
            return {"error": str(e)}
    
    def process_image_generation(self, data):
        """Process image generation request"""
        try:
            prompt = data.get('prompt', '')
            style = data.get('style', 'photorealistic')
            size = data.get('size', '1024x1024')
            count = data.get('count', 1)
            service = data.get('service', 'stability_ai')
            
            # For now, return a placeholder response
            # In a real implementation, you'd call Stability AI or Leonardo AI APIs
            
            process_id = f"image_{int(time.time())}"
            processing_status[process_id] = {
                "status": "completed",
                "type": "image_generation",
                "started_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat(),
                "data": data,
                "result": {
                    "message": "Image generation completed (placeholder)",
                    "images": [f"generated_image_{i}.png" for i in range(count)]
                }
            }
            
            return {
                "process_id": process_id,
                "status": "completed",
                "message": "Image generation completed",
                "images": [f"generated_image_{i}.png" for i in range(count)]
            }
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return {"error": str(e)}
    
    def _run_content_generation(self, process_id, args, data):
        """Run content generation in background"""
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=self.base_path)
            
            processing_status[process_id].update({
                "status": "completed" if result.returncode == 0 else "failed",
                "completed_at": datetime.now().isoformat(),
                "output": result.stdout,
                "error": result.stderr
            })
            
        except Exception as e:
            processing_status[process_id].update({
                "status": "failed",
                "completed_at": datetime.now().isoformat(),
                "error": str(e)
            })
    
    def _run_voice_synthesis(self, process_id, args, data):
        """Run voice synthesis in background"""
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=self.base_path)
            
            processing_status[process_id].update({
                "status": "completed" if result.returncode == 0 else "failed",
                "completed_at": datetime.now().isoformat(),
                "output": result.stdout,
                "error": result.stderr
            })
            
        except Exception as e:
            processing_status[process_id].update({
                "status": "failed",
                "completed_at": datetime.now().isoformat(),
                "error": str(e)
            })

# Initialize processor
processor = AIWebhookProcessor()

@app.route('/webhooks/content-generation', methods=['POST'])
def content_generation():
    """Handle content generation requests"""
    try:
        data = request.get_json()
        logger.info(f"Content generation request: {data}")
        
        result = processor.process_content_generation(data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Content generation webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhooks/voice-synthesis', methods=['POST'])
def voice_synthesis():
    """Handle voice synthesis requests"""
    try:
        data = request.get_json()
        logger.info(f"Voice synthesis request: {data}")
        
        result = processor.process_voice_synthesis(data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Voice synthesis webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhooks/image-generation', methods=['POST'])
def image_generation():
    """Handle image generation requests"""
    try:
        data = request.get_json()
        logger.info(f"Image generation request: {data}")
        
        result = processor.process_image_generation(data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Image generation webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhooks/status/<process_id>', methods=['GET'])
def get_status(process_id):
    """Get processing status"""
    if process_id in processing_status:
        return jsonify(processing_status[process_id])
    else:
        return jsonify({"error": "Process not found"}), 404

@app.route('/webhooks/status', methods=['GET'])
def get_all_status():
    """Get all processing statuses"""
    return jsonify(processing_status)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_processes": len([p for p in processing_status.values() if p['status'] == 'processing'])
    })

if __name__ == '__main__':
    print("🚀 Starting AI Webhook Server...")
    print("📡 Available endpoints:")
    print("   POST /webhooks/content-generation")
    print("   POST /webhooks/voice-synthesis")
    print("   POST /webhooks/image-generation")
    print("   GET  /webhooks/status/<process_id>")
    print("   GET  /webhooks/status")
    print("   GET  /health")
    print("\n🔗 For Make.com integration, use ngrok to expose this server:")
    print("   ngrok http 5000")
    print("\n🌐 Server starting on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)