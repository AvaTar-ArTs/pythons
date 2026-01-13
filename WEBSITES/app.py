#!/usr/bin/env python3
"""
📱 Creative AI Mobile Studio - Mobile App Backend
Mobile-optimized AI content generation platform
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Database setup
DB_PATH = Path("/Users/steven/ai-sites/retention-products-suite/mobile-apps/creative_ai_mobile_studio/mobile_app.db")

def init_db():
    """Initialize mobile app database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            username TEXT,
            email TEXT,
            subscription_tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            project_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Content table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            content_type TEXT NOT NULL,
            content_data TEXT,
            prompt TEXT,
            ai_model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)
    
    # Usage tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action_type TEXT NOT NULL,
            content_type TEXT,
            tokens_used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Challenges table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            challenge_type TEXT NOT NULL,
            difficulty TEXT DEFAULT 'easy',
            points_reward INTEGER DEFAULT 10,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User achievements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_type TEXT NOT NULL,
            achievement_name TEXT NOT NULL,
            points_earned INTEGER DEFAULT 0,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

@dataclass
class MobileUser:
    """Mobile user data structure"""
    id: int
    device_id: str
    username: Optional[str]
    email: Optional[str]
    subscription_tier: str
    created_at: str
    last_active: str

class MobileAIClient:
    """Mobile-optimized AI client"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
    
    def generate_text(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate text optimized for mobile"""
        # Mock implementation - replace with actual API
        return f"Mobile-optimized text: {prompt[:50]}..."
    
    def generate_image(self, prompt: str, size: str = "512x512") -> str:
        """Generate image optimized for mobile"""
        # Mock implementation - replace with actual API
        return f"Mobile-optimized image: {prompt[:50]}..."
    
    def generate_audio(self, prompt: str, duration: int = 30) -> str:
        """Generate audio optimized for mobile"""
        # Mock implementation - replace with actual API
        return f"Mobile-optimized audio: {prompt[:50]}..."

# Initialize AI client
ai_client = MobileAIClient()

# API Routes
@app.route('/api/register', methods=['POST'])
def register_user():
    """Register new mobile user"""
    data = request.get_json()
    device_id = data.get('device_id')
    
    if not device_id:
        return jsonify({'error': 'Device ID required'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE device_id = ?", (device_id,))
    user = cursor.fetchone()
    
    if user:
        conn.close()
        return jsonify({'user_id': user[0], 'message': 'User already exists'})
    
    # Create new user
    cursor.execute("""
        INSERT INTO users (device_id, username, email, subscription_tier)
        VALUES (?, ?, ?, ?)
    """, (device_id, data.get('username'), data.get('email'), 'free'))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'user_id': user_id, 'message': 'User registered successfully'})

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    """Get user information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    conn.close()
    
    return jsonify({
        'id': user[0],
        'device_id': user[1],
        'username': user[2],
        'email': user[3],
        'subscription_tier': user[4],
        'created_at': user[5],
        'last_active': user[6]
    })

@app.route('/api/projects/<int:user_id>')
def get_projects(user_id):
    """Get user projects"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, COUNT(c.id) as content_count
        FROM projects p
        LEFT JOIN content c ON p.id = c.project_id
        WHERE p.user_id = ?
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """, (user_id,))
    
    projects = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': project[0],
        'name': project[2],
        'project_type': project[3],
        'status': project[4],
        'created_at': project[5],
        'content_count': project[6]
    } for project in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create new project"""
    data = request.get_json()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO projects (user_id, name, project_type)
        VALUES (?, ?, ?)
    """, (data['user_id'], data['name'], data['project_type']))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'project_id': project_id, 'message': 'Project created successfully'})

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate content for mobile"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    content_type = data.get('content_type')
    prompt = data.get('prompt')
    
    if not all([user_id, project_id, content_type, prompt]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check usage limits
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT subscription_tier FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # Check daily usage limit
    today = datetime.now().date()
    cursor.execute("""
        SELECT COUNT(*) FROM usage_tracking 
        WHERE user_id = ? AND DATE(created_at) = ?
    """, (user_id, today))
    
    daily_usage = cursor.fetchone()[0]
    daily_limit = 10 if user[0] == 'free' else 100 if user[0] == 'pro' else 1000
    
    if daily_usage >= daily_limit:
        conn.close()
        return jsonify({'error': 'Daily usage limit exceeded'}), 403
    
    # Generate content
    try:
        if content_type == 'text':
            content = ai_client.generate_text(prompt)
        elif content_type == 'image':
            content = ai_client.generate_image(prompt)
        elif content_type == 'audio':
            content = ai_client.generate_audio(prompt)
        else:
            return jsonify({'error': 'Unsupported content type'}), 400
        
        # Save content
        cursor.execute("""
            INSERT INTO content (project_id, content_type, content_data, prompt, ai_model)
            VALUES (?, ?, ?, ?, ?)
        """, (project_id, content_type, content, prompt, 'mobile-ai'))
        
        # Track usage
        cursor.execute("""
            INSERT INTO usage_tracking (user_id, action_type, content_type, tokens_used)
            VALUES (?, ?, ?, ?)
        """, (user_id, 'generate', content_type, len(prompt.split())))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'content': content,
            'usage_remaining': daily_limit - daily_usage - 1
        })
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/challenges')
def get_challenges():
    """Get available challenges"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM challenges 
        WHERE is_active = 1 
        ORDER BY difficulty, points_reward DESC
    """)
    
    challenges = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': challenge[0],
        'title': challenge[1],
        'description': challenge[2],
        'challenge_type': challenge[3],
        'difficulty': challenge[4],
        'points_reward': challenge[5]
    } for challenge in challenges])

@app.route('/api/achievements/<int:user_id>')
def get_achievements(user_id):
    """Get user achievements"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM achievements 
        WHERE user_id = ? 
        ORDER BY unlocked_at DESC
    """, (user_id,))
    
    achievements = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': achievement[0],
        'achievement_type': achievement[2],
        'achievement_name': achievement[3],
        'points_earned': achievement[4],
        'unlocked_at': achievement[5]
    } for achievement in achievements])

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get user leaderboard"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.username, u.device_id, 
               COALESCE(SUM(a.points_earned), 0) as total_points,
               COUNT(DISTINCT p.id) as project_count
        FROM users u
        LEFT JOIN achievements a ON u.id = a.user_id
        LEFT JOIN projects p ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY total_points DESC
        LIMIT 50
    """)
    
    leaderboard = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'username': user[0] or f"User {user[1][:8]}",
        'total_points': user[2],
        'project_count': user[3]
    } for user in leaderboard])

@app.route('/api/usage/<int:user_id>')
def get_usage_stats(user_id):
    """Get usage statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get daily usage
    today = datetime.now().date()
    cursor.execute("""
        SELECT COUNT(*) FROM usage_tracking 
        WHERE user_id = ? AND DATE(created_at) = ?
    """, (user_id, today))
    daily_usage = cursor.fetchone()[0]
    
    # Get weekly usage
    week_ago = today - timedelta(days=7)
    cursor.execute("""
        SELECT COUNT(*) FROM usage_tracking 
        WHERE user_id = ? AND DATE(created_at) >= ?
    """, (user_id, week_ago))
    weekly_usage = cursor.fetchone()[0]
    
    # Get usage by type
    cursor.execute("""
        SELECT content_type, COUNT(*) as count
        FROM usage_tracking 
        WHERE user_id = ? AND DATE(created_at) = ?
        GROUP BY content_type
    """, (user_id, today))
    usage_by_type = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'daily_usage': daily_usage,
        'weekly_usage': weekly_usage,
        'usage_by_type': {item[0]: item[1] for item in usage_by_type}
    })

@app.route('/api/notifications/<int:user_id>')
def get_notifications(user_id):
    """Get user notifications"""
    # Mock notifications - replace with actual notification system
    notifications = [
        {
            'id': 1,
            'title': 'Welcome to Creative AI Mobile!',
            'message': 'Start creating amazing content with AI',
            'type': 'welcome',
            'timestamp': datetime.now().isoformat()
        },
        {
            'id': 2,
            'title': 'Daily Challenge Available',
            'message': 'Complete today\'s creative challenge for bonus points!',
            'type': 'challenge',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    return jsonify(notifications)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)